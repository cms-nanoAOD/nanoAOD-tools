#!/usr/bin/env python
import os
import sys
import ROOT
import math
from array import array
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import InputTree
from PhysicsTools.NanoAODTools.postprocessing.topreco import *
from PhysicsTools.NanoAODTools.postprocessing.skimtree import *

def Chi_TopMass(mT):
    sigma = 28.8273
    mST = 174.729
    chi = ( ROOT.TMath.Power((mST-mT), 2.) ) / ( ROOT.TMath.Power(sigma, 2.))
    return chi

#os.environ["X509_USER_PROXY"] = sys.argv[1]
#print(os.environ["X509_USER_PROXY"]) 

def bjet_filter(jets, tagger, WP): #returns collections of b jets and no b jets (discriminated with btaggers)
    # b-tag working points: mistagging efficiency tight = 0.1%, medium 1% and loose = 10% 
    WPbtagger = {'DeepFlv_T': 0.7264, 'DeepFlv_M': 0.2770, 'DeepFlv_L': 0.0494, 'DeepCSV_T': 0.7527, 'DeepCSV_M': 0.4184, 'DeepCSV_L': 0.1241}
    if(tagger == 'DeepFlv'):
        threshold = WPbtagger[str(tagger) + '_' + str(WP)]
        return list(filter(lambda x : x.btagDeepFlavB >= threshold, jets)), list(filter(lambda x : x.btagDeepFlavB < threshold, jets))
    elif(tagger == 'DeepCSV'):
        threshold = WPbtagger[str(tagger) + '_' + str(WP)]
        return list(filter(lambda x : x.btagDeepB >= threshold, jets)), list(filter(lambda x : x.btagDeepB < threshold, jets))
    else:
        print('Only DeepFlv and DeepCSV accepted! Pleae implement other taggers if you want them.')

def mcbjet_filter(jets): #returns a collection of only b-gen jets (to use only for MC samples)
    return list(filter(lambda x : x.partonFlavour == -5 or x.partonFlavour == 5, jets))

def sameflav_filter(jets, flav): #returns a collection of only b-gen jets (to use only forMC samples)                       
    return list(filter(lambda x : x.partonFlavour == flav, jets))

DeltaFilter = True
leadingjet_ptcut = 150.

'''
fcName = sys.argv[2]
fc = ROOT.TFileCollection(fcName,fcName,fcName)
chain = ROOT.TChain('Events')
chain.AddFileInfoList(fc.GetList())
nEventsTot = chainNEvents.GetEntries()

'''
#tree = InputTree(chain.GetTree())
inp = ROOT.TFile.Open("/eos/home-a/adeiorio/Wprime/nosynch/WJetsHT200to400_2017/WJetsHT200to400_2017.root")
tree = InputTree(inp.Events)
isMC = True
'''
if ('Data' in fcName):
    isMC = False
'''
#++++++++++++++++++++++++++++++++++
#++   branching the new trees    ++
#++++++++++++++++++++++++++++++++++
#outTreeFile = ROOT.TFile(outdir+"/trees_"+sample+"_"+channel+".root", "RECREATE") #some name of the output file
outTreeFile = ROOT.TFile("./trees/prova.root", "RECREATE") #some name of the output file
trees = []
for i in range(10):
    trees.append(None)
#systZero = systWeights()
# defining the operations to be done with the systWeights class
maxSysts = 0
addPDF = False
addQ2 = False
addTopPt = False
addVHF = False
addTTSplit = False
addTopTagging = False
addWTagging = False
addTrigSF = False
addPDF = False
addQ2 = False
addTopTagging = False
addWTagging = False
addTopPt = False
addVHF = False
addTrigSF = False
nPDF = 0

systTree = systWeights()
systTree.prepareDefault(True, addQ2, addPDF, addTopPt, addVHF, addTTSplit)
systTree.addSelection("signal")
systTree.initTreesSysts(trees, outTreeFile)

print trees

#++++++++++++++++++++++++++++++++++
#++     variables to branch      ++
#++++++++++++++++++++++++++++++++++
prova = array.array('f', )
for i in range(4):
    prova.append(0.)

#++++++++++++++++++++++++++++++++++
#++   branching the new trees    ++
#++++++++++++++++++++++++++++++++++
# appena capito come si fa
systTree.branchTreesSysts(trees, "signal", "prova", outTreeFile, prova)

#++++++++++++++++++++++++++++++++++
#++   looping over the events    ++
#++++++++++++++++++++++++++++++++++
for i in xrange(0,tree.GetEntries()):
    #for i in xrange(0,20):
    #++++++++++++++++++++++++++++++++++
    #++        taking objects        ++
    #++++++++++++++++++++++++++++++++++
    if i > 1000:
        break

    for k in range(len(prova)):
        prova[k] = 0.

    event = Event(tree,i)
    electrons = Collection(event, "Electron")
    muons = Collection(event, "Muon")
    jets = Collection(event, "Jet")
    fatjets = Collection(event, "FatJet")
    PV = Object(event, "PV")
    HLT = Object(event, "HLT")
    Flag = Object(event, 'Flag')
    met = Object(event, "MET")
    MET = {'metPx': met.pt*ROOT.TMath.Cos(met.phi), 'metPy': met.pt*ROOT.TMath.Sin(met.phi)}
    genpart = None
    if isMC:
        genpart = Collection(event, "GenPart")

    #++++++++++++++++++++++++++++++++++
    #++      defining variables      ++
    #++++++++++++++++++++++++++++++++++
    tightlep = None
    tightlep_p4 = ROOT.TLorentzVector()
    tightlep_p4t = ROOT.TLorentzVector()
    recomet_p4t = ROOT.TLorentzVector()
    recomet_p4t.SetPtEtaPhiM(met.pt, 0., met.phi, 0)

    #++++++++++++++++++++++++++++++++++
    #++    starting the analysis     ++
    #++++++++++++++++++++++++++++++++++
    VetoMu = get_LooseMu(muons)
    goodMu = get_Mu(muons)
    VetoEle = get_LooseEle(electrons)
    goodEle = get_Ele(electrons)
    year = 2017

    passMu, passEle, passHT, noTrigger = trig_map(HLT, year)

    isMuon = (len(goodMu) == 1) and (len(goodEle) == 0) and len(VetoMu) == 0 and len(VetoEle) == 0 and (passMu or passHT)
    isElectron = (len(goodMu) == 0) and (len(goodEle) == 1) and len(VetoMu) == 0 and len(VetoEle) == 0 and (passEle or passHT)
    if(isMuon):
        tightlep = goodMu[0]
        tightlep_p4.SetPtEtaPhiM(goodMu[0].pt,goodMu[0].eta,goodMu[0].phi,goodMu[0].mass)
        tightlep_p4t = copy.deepcopy(tightlep_p4)
        tightlep_p4t.SetPz(0.)
    elif(isElectron):
        tightlep = goodEle[0]
        tightlep_p4.SetPtEtaPhiM(goodEle[0].pt,goodEle[0].eta,goodEle[0].phi,goodEle[0].mass)
        tightlep_p4t = copy.deepcopy(tightlep_p4)
        tightlep_p4t.SetPz(0.)
    else:
        print('Not a good event')
        continue

    goodJets = get_Jet(jets, 25)
    bjets, nobjets = bjet_filter(goodJets, 'DeepFlv', 'M')
    mcbjets = None
    mclepton = None

    recotop = TopUtilities()

    #MCtruth event reconstruction                                                      
    if isMC:
        mcbjets = mcbjet_filter(goodJets)

        mctfound = False
        if isMuon:
            for muon in goodMu:
                if (muon.genPartFlav == 1 or muon.genPartFlav == 15) and not mctfound:
                    mclepton = muon
                    mctfound = True
                    if mclepton.genPartIdx == -1:
                        print 'MCTruth reconstruction not properly working - lepton step'
                        continue
        elif isElectron:
            for ele in goodEle:
                if (ele.genPartFlav == 1 or ele.genPartFlav == 15) and not mctfound:
                    mclepton = ele
                    mctfound = True
                    if mclepton.genPartIdx == -1:
                        print 'MCTruth reconstruction not properly working - lepton step'
                        continue


        if mclepton is None:
            continue

        mctop_p4 = None
        mctop_p4t = None
        IsmcNeg = False
        mcpromptbjet_p4 = None
        mctopbjet_p4 = None
        mctopbjet_p4_pre = None
        mcpromptbjet_p4t = None
        bjetcheck = True
        mcbjets = mcbjet_filter(jets)
        
        if len(mcbjets)>2:
            bjetcheck = False

        mclepton_p4 = ROOT.TLorentzVector()
        mclepton_p4.SetPtEtaPhiM(mclepton.pt, mclepton.eta, mclepton.phi, mclepton.mass)

        mcWprime_p4 = ROOT.TLorentzVector()
        mcWprime_p4t = ROOT.TLorentzVector()

        topgot_ak4 = False
        Wpgot_ak4 = False

        bottjets = sameflav_filter(mcbjets, 5)
        abottjets = sameflav_filter(mcbjets, -5)

        for bjet in mcbjets:
            bjet_p4 = ROOT.TLorentzVector()
            bjet_p4.SetPtEtaPhiM(bjet.pt, bjet.eta, bjet.phi, bjet.mass)

            if abs(bjet.partonFlavour)!=5:
                print 'bfilter not properly working'
                continue

            blepflav = genpart[mclepton.genPartIdx].pdgId*bjet.partonFlavour

            if bjet.hadronFlavour == 5:
                if blepflav < 0 and not topgot_ak4:
                    mctopbjet_p4_pre = copy.deepcopy(bjet_p4)
             
                    if deltaR(bjet_p4.Eta(), bjet_p4.Phi(), mclepton_p4.Eta(), mclepton_p4.Phi()) < 0.4:
                        bjet_p4 -= mclepton_p4
                    
                    mctopbjet_p4 = bjet_p4
                    mctop_p4, IsmcNeg = recotop.top4Momentum(mclepton_p4, bjet_p4, MET['metPx'], MET['metPy'])
                    IsmcNeg = IsmcNeg*DeltaFilter

                    if mctop_p4 is None:
                        continue
                        
                    mclepton_p4t = copy.deepcopy(mclepton_p4)
                    mclepton_p4t.SetPz(0.)
                    bjet_p4t = copy.deepcopy(bjet_p4)
                    bjet_p4t.SetPz(0.)
                    met_p4t = ROOT.TLorentzVector()
                    met_p4t.SetPtEtaPhiM(met.pt, 0., met.phi, 0)
                    mctop_p4t = mclepton_p4t + bjet_p4t + met_p4t
                    if mctop_p4t.Pz() !=0:
                        mctop_p4t.SetPz(0.)
                    topgot_ak4 = True

                elif blepflav > 0 and not Wpgot_ak4:
                    mcpromptbjet_p4 = bjet_p4
                    mcpromptbjet_p4t = copy.deepcopy(bjet_p4)
                    mcpromptbjet_p4t.SetPz(0.)
                    Wpgot_ak4 = True

        if topgot_ak4 and Wpgot_ak4:
            mcWprime_p4 = mctop_p4 + mcpromptbjet_p4
            mcWprime_p4t = mctop_p4t + mcpromptbjet_p4t
            mcChi2_topmass = Chi_TopMass(mctop_p4.M())
    
    #DetReco(nstruction)
    if len(goodJets) < 2:
        continue
        
    highptJets = get_Jet(goodJets, leadingjet_ptcut)
    if len(highptJets) < 1:
        continue

    closest_promptjet = None
    closest_promptjet_p4t = None
    closest_jet_p4 = None
    closest_jet_p4t = None
    closest_jet_p4_pre = None
    chi_promptjet = None
    chi_promptjet_p4t = None
    chi_jet_p4 = None
    chi_jet_p4t = None
    chi_jet_p4_pre = None
    sublead_promptjet = highptJets[0]
    sublead_promptjet_p4t = None
    sublead_jet_p4 = None
    sublead_jet_p4t = None
    sublead_jet_p4_pre = None
    best_promptjet = None
    best_promptjet_p4t = None
    best_jet_p4 = None
    best_jet_p4t = None
    DeltaR_nujet = 100.
    DeltaR_Idx = 0
    tm_chi = 1000.
    tm_Idx = 0
    mtop_p4 = None

    btag_countings_sublead = 0
    btag_countings_closest = 0
    btag_countings_chi = 0
    btag_countings_best = 0

    #jet reconstructing top with the smallest chi2 p4                                
    for k in range(len(goodJets)):
        mtop_p4, isdetrecoNeg = recotop.top4Momentum(tightlep_p4, goodJets[k].p4(), MET['metPx'], MET['metPy'])
        if mtop_p4 is None:
            continue
        chi = Chi_TopMass(mtop_p4.M())
        if chi < tm_chi:
            tm_chi = chi
            tm_Idx = k
    
    chi_jet_p4_pre = goodJets[tm_Idx].p4()
    chi_jet = goodJets[tm_Idx]
    if deltaR(chi_jet_p4_pre.Eta(), chi_jet_p4_pre.Phi(), tightlep.eta, tightlep.phi)\
 < 0.4:
        chi_jet_p4 = chi_jet_p4_pre - tightlep_p4
    else:
        chi_jet_p4 = chi_jet_p4_pre
    if tm_Idx == 0:
        if len(highptJets) > 1:
            chi_promptjet = highptJets[1]
        else:
            chi_promptjet = goodJets[1]
    else:
        chi_promptjet = highptJets[0]
        
    chi_recotop_p4, IsNeg_chi = recotop.top4Momentum(tightlep_p4, chi_jet_p4, MET['metPx'], MET['metPy'])
    IsNeg_chi = IsNeg_chi * DeltaFilter

    btag_countings_chi = len(bjet_filter([chi_promptjet, chi_jet], 'DeepFlv', 'M'))

    chi_jet_p4t = copy.deepcopy(chi_jet_p4)
    chi_jet_p4t.SetPz(0.)
    chi_recotop_p4t = tightlep_p4t + chi_jet_p4t + recomet_p4t
    chi_promptjet_p4t = copy.deepcopy(chi_promptjet.p4())
    chi_promptjet_p4t.SetPz(0.)

    #jet closest to MET p4                                                              
    closest_jet, detrecodR = closest(tightlep, goodJets)
    closest_jet_p4_pre = closest_jet.p4()
    
    if deltaR(closest_jet.eta, closest_jet.phi, tightlep.eta, tightlep.phi) < 0.4:
        closest_jet_p4 = closest_jet_p4_pre - tightlep_p4
    else:
        closest_jet_p4 = closest_jet_p4_pre
    
    if closest_jet == goodJets[0]:
        if len(highptJets) > 1:
            closest_promptjet = highptJets[1]
        else:
            closest_promptjet = goodJets[1]
    else:
        closest_promptjet = highptJets[0]

    closest_recotop_p4, IsNeg_closest = recotop.top4Momentum(tightlep_p4, closest_jet_p4, MET['metPx'], MET['metPy'])
    IsNeg_closest = IsNeg_closest * DeltaFilter

    btag_countings_closest = len(bjet_filter([closest_promptjet, closest_jet], 'DeepFlv', 'M'))

    closest_jet_p4t = copy.deepcopy(closest_jet_p4)
    closest_jet_p4t.SetPz(0.)
    closest_recotop_p4t = tightlep_p4t + closest_jet_p4t + recomet_p4t
    closest_promptjet_p4t = copy.deepcopy(closest_promptjet.p4())
    closest_promptjet_p4t.SetPz(0.)

    #subleading jet reconstruction                                                      
    if len(highptJets) > 1:
        sublead_jet_p4_pre = highptJets[1].p4()
        sublead_jet = highptJets[1]
    else:
        sublead_jet_p4_pre = goodJets[1].p4()

        sublead_jet = goodJets[1]
    if deltaR(sublead_jet_p4_pre.Eta(), sublead_jet_p4_pre.Phi(), tightlep.eta, tightlep.phi) < 0.4:
        sublead_jet_p4 = sublead_jet_p4_pre - tightlep_p4
    else:
        sublead_jet_p4 = sublead_jet_p4_pre

    sublead_recotop_p4, IsNeg_sublead = recotop.top4Momentum(tightlep_p4, sublead_jet_p4, MET['metPx'], MET['metPy'])
    IsNeg_sublead = IsNeg_sublead * DeltaFilter

    sublead_jet_p4t = copy.deepcopy(sublead_jet_p4)
    sublead_jet_p4t.SetPz(0.)
    sublead_recotop_p4t = tightlep_p4t + sublead_jet_p4t + recomet_p4t
    sublead_promptjet_p4t = copy.deepcopy(sublead_promptjet.p4())
    sublead_promptjet_p4t.SetPz(0.)

    btag_countings_sublead = len(bjet_filter([sublead_promptjet, sublead_jet], 'DeepFlv', 'M'))

    #best jet reconstruction                                                           
    BestFound = False
    best_recotop_p4 = None
    IsNeg_best = None
    if sublead_jet_p4_pre == closest_jet_p4_pre:
        best_jet_p4 = sublead_jet_p4
        best_jet = sublead_jet
        best_promptjet = sublead_promptjet
        BestFound = True
    elif sublead_jet_p4_pre == chi_jet_p4_pre:
        best_jet_p4 = sublead_jet_p4
        best_jet = sublead_jet
        best_promptjet = sublead_promptjet
        BestFound = True
    elif chi_jet_p4_pre == closest_jet_p4_pre:
        best_jet_p4 = chi_jet_p4
        best_jet = chi_jet
        best_promptjet = chi_promptjet
        BestFound = True

    if not BestFound:
        best_jet_p4 = chi_jet_p4
        best_jet = chi_jet
        best_promptjet = chi_promptjet
        BestFound = True

    if BestFound:
        best_recotop_p4, IsNeg_best = recotop.top4Momentum(tightlep_p4, best_jet_p4, MET['metPx'], MET['metPy'])
        IsNeg_best = IsNeg_best * DeltaFilter
        best_jet_p4t = copy.deepcopy(best_jet_p4)
        best_jet_p4t.SetPz(0.)
        best_recotop_p4t = tightlep_p4t + best_jet_p4t + recomet_p4t
        best_promptjet_p4t = copy.deepcopy(best_promptjet.p4())
        best_promptjet_p4t.SetPz(0.)

        btag_countings_best = len(bjet_filter([best_promptjet, best_jet], 'DeepFlv', 'M'))

    #Wprime reco                                                                        
    if closest_recotop_p4 != None :
        closest_Wprime_p4 = closest_recotop_p4 + closest_promptjet.p4()
        closest_Wprime_p4t = closest_recotop_p4t + closest_promptjet_p4t
        prova[0] = closest_Wprime_p4.M()

    if chi_recotop_p4 != None :
        chi_Wprime_p4 = chi_recotop_p4 + chi_promptjet.p4()
        chi_Wprime_p4t = chi_recotop_p4t + chi_promptjet_p4t
        prova[1] = chi_Wprime_p4.M()

    if sublead_recotop_p4 != None :
        sublead_Wprime_p4 = sublead_recotop_p4 + sublead_promptjet.p4()
        sublead_Wprime_p4t = sublead_recotop_p4t + sublead_promptjet_p4t
        prova[2] = sublead_Wprime_p4.M()

    if best_recotop_p4 != None :
        best_Wprime_p4 = best_recotop_p4 + best_promptjet.p4()
        best_Wprime_p4t = best_recotop_p4t + best_promptjet_p4t
        prova[3] = best_Wprime_p4.M()

    systTree.fillTreesSysts(trees,"signal")

trees[0].Print()
systTree.writeTreesSysts(trees, outTreeFile)
