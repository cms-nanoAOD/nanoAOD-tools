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

os.environ["X509_USER_PROXY"] = sys.argv[1]
print(os.environ["X509_USER_PROXY"]) 

def bjet_filter(jets, tagger, WP): #returns collections of b jets and no b jets
    # b-tag working points: mistagging efficiency tight = 0.1%, medium 1% and loose = 10% 
    WPbtagger = {'deepFlv_T': 0.7264, 'deepFlv_M': 0.2770, 'deepFlv_L': 0.0494, 'deepCSV_T': 0.7527, 'deepCSV_M': 0.4184, 'deepCSV_L': 0.1241}
    if(tagger == 'DeepFlv'):
        threshold = WPbtagger[str(tagger) + '_' + str(WP)]
        return list(filter(lambda x : x.btagDeepFlavB >= threshold, jets)), list(filter(lambda x : x.btagDeepFlavB < threshold, jets))
    elif(tagger == 'DeepCSV'):
        threshold = WPbtagger[str(tagger) + '_' + str(WP)]
        return list(filter(lambda x : x.btagDeepB >= threshold, jets)), list(filter(lambda x : x.btagDeepB < threshold, jets))
    else:
        print('Only DeepFlv and DeepCSV accepted! Pleae implement other taggers if you want them.')

fcName = sys.argv[2]
fc = ROOT.TFileCollection(fcName,fcName,fcName)
chain = ROOT.TChain('Events')
chain.AddFileInfoList(fc.GetList())
nEventsTot = chainNEvents.GetEntries()

tree = InputTree(chain.GetTree())
isMC = True
if ('Data' in fcName):
    isMC = False

#++++++++++++++++++++++++++++++++++
#++   branching the new trees    ++
#++++++++++++++++++++++++++++++++++
outTreeFile = ROOT.TFile(outdir+"/trees_"+sample+"_"+channel+".root", "RECREATE") #some name of the output file
trees = ROOT.TTree[10]
systZero = systWeights()
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

systZero.prepareDefault(True, addQ2, addPDF, addTopPt, addVHF, addTTSplit)

systTree = systWeights()
systTree.addSelection("signal");
systTree.initTreesSysts(trees, outTreeFile);

#++++++++++++++++++++++++++++++++++
#++   branching the new trees    ++
#++++++++++++++++++++++++++++++++++
# appena capito come si fa


#++++++++++++++++++++++++++++++++++
#++   looping over the events    ++
#++++++++++++++++++++++++++++++++++
for i in xrange(0,tree.GetEntries()):
    #for i in xrange(0,20):
    #++++++++++++++++++++++++++++++++++
    #++        taking objects        ++
    #++++++++++++++++++++++++++++++++++
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

    #++++++++++++++++++++++++++++++++++
    #++      defining variables      ++
    #++++++++++++++++++++++++++++++++++
    tightlep_p4 = ROOT.TLorentzVector()

    #++++++++++++++++++++++++++++++++++
    #++    starting the analysis     ++
    #++++++++++++++++++++++++++++++++++
    VetoMu = get_LooseMu(muons)
    goodMu = get_Mu(muons)
    VetoEle = get_LooseEle(electrons)
    goodEle = get_Ele(electrons)

    passMu, passEle, passHT, noTrigger = trig_map(HLT, year)

    isMuon = (len(goodMu) == 1) and (len(goodEle) == 0) and len(VetoMu) == 0 and len(VetoEle) == 0 and (passMu or passHT)
    isElectron = (len(goodMu) == 0) and (len(goodEle) == 1) and len(VetoMu) == 0 and len(VetoEle) == 0 and (passEle or passHT)
    if(isMuon):
        tightlep_p4.SetPtEtaPhiM(goodMu[0].pt,goodMu[0].eta,goodMu[0].phi,goodMu[0].mass)
    elif(isElectron):
        tightlep_p4.SetPtEtaPhiM(goodEle[0].pt,goodEle[0].eta,goodEle[0].phi,goodEle[0].mass)
    else:
        print('Not a good event')
        continue

    goodJets = get_Jet(jets, 25)
    bjets, nobjets = bjet_filter(goodJets, 'DeepFlv', 'M')

    recotop = TopUtilities()
    #AK4 RECO
    for bjet in bjets:
        bjet_p4 = ROOT.TLorentzVector()
        bjet_p4.SetPtEtaPhiM(bjet.pt, bjet.eta, bjet.phi, bjet.mass)
        mctopbjet_p4_pre = copy.deepcopy(bjet_p4)
        if deltaR(bjet_p4.Eta(), bjet_p4.Phi(), tightlep_p4.Eta(), tightlep_p4.Phi()) < 0.4:
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
                print 'p3'
            mctop_p4t.SetPz(0.)
            topgot_ak4 = True
