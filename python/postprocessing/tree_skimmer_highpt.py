#!/bin/env python3
import os
import sys
import ROOT
import math
import datetime
import copy
from array import array
from skimtree_utils import *

if sys.argv[4] == 'remote':
    from samples import *
    Debug = False
else:
    from samples.samples import *
    Debug = True
sample = sample_dict[sys.argv[1]]
part_idx = sys.argv[2]
file_list = list(map(str, sys.argv[3].strip('[]').split(',')))
#print("file_list: ", file_list, "\nloop #1 over it")
#for infile in file_list:
    #print(infile)

MCReco = True
startTime = datetime.datetime.now()
print("Starting running at " + str(startTime))

ROOT.gROOT.SetBatch()

leadingjet_ptcut = 150.

chain = ROOT.TChain('Events')
#print(chain)
#print("loop #2 over file_list")
for infile in file_list: 
    #print("Adding %s to the chain" %(infile))
    chain.Add(infile)

print("Number of events in chain " + str(chain.GetEntries()))
print("Number of events in tree from chain " + str((chain.GetTree()).GetEntries()))
#print("Type of tree from chain " + str(type(chain.GetTree())))
#treechain = (ROOT.TTree)(chain.GetTree())
tree = InputTree(chain)
#print("Number of entries: " +str(tree.GetEntries()))
#print("tree: ", tree)
isMC = True
if ('Data' in sample.label):
    isMC = False

MCReco = MCReco * isMC

#++++++++++++++++++++++++++++++++++
#++   branching the new trees    ++
#++++++++++++++++++++++++++++++++++
outTreeFile = ROOT.TFile(sample.label+"_part"+str(part_idx)+".root", "RECREATE") #some name of the output file
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
nPDF = 0

systTree = systWeights()
systTree.prepareDefault(True, addQ2, addPDF, addTopPt, addVHF, addTTSplit)
systTree.addSelection("all")
systTree.initTreesSysts(trees, outTreeFile)

systTree.setWeightName("w_nominal",1.)
systTree.setWeightName("puSF",1.)
systTree.setWeightName("puUp",1.)
systTree.setWeightName("puDown",1.)
systTree.setWeightName("lepSF",1.)
systTree.setWeightName("lepUp",1.)
systTree.setWeightName("lepDown",1.)
systTree.setWeightName("PFSF",1.)
systTree.setWeightName("PFUp",1.)
systTree.setWeightName("PFDown",1.)


#++++++++++++++++++++++++++++++++++
#++     variables to branch      ++
#++++++++++++++++++++++++++++++++++

#++++++++++++++++++++++++++++++++++
#++         All category         ++
#++++++++++++++++++++++++++++++++++
isdileptonic = array.array('i', [0])
muon_pt = array.array('f', [0.])
muon_eta = array.array('f', [0.])
muon_phi = array.array('f', [0.])
muon_m = array.array('f', [0.])
muon_SF = array.array('f', [0.])
electron_pt = array.array('f', [0.])
electron_eta = array.array('f', [0.])
electron_phi = array.array('f', [0.])
electron_m = array.array('f', [0.])
electron_SF = array.array('f', [0.])

nJet_lowpt_all = array.array('i', [0])
nfatJet_all = array.array('i', [0])
nJet_pt100_all = array.array('i', [0])
nbJet_lowpt_all = array.array('i', [0])
nbJet_pt100_all = array.array('i', [0])
nlep_all  = array.array('i', [0])

Event_HT_all = array.array('f', [0.])

#Lepton
isEle_all = array.array('i', [0])
isMu_all = array.array('i', [0])

MET_pt_all = array.array('f', [0.])
MET_phi_all = array.array('f', [0.])

nPV_tot_all = array.array('f', [0.])
nPV_good_all = array.array('f', [0.])

w_nominal_all = array.array('f', [0.])
w_PDF_all = array.array('f', [0.]*110)
passed_mu_all = array.array('f', [0.])
passed_ele_all = array.array('f', [0.])
passed_ht_all = array.array('f', [0.])
passed_ph_all = array.array('f', [0.])
leadingjet_pt_all = array.array('f', [0.])
subleadingjet_pt_all = array.array('f', [0.])
leadingbjet_pt_all = array.array('f', [0.])
subleadingbjet_pt_all = array.array('f', [0.])


#++++++++++++++++++++++++++++++++++
#++   branching the new trees    ++
#++++++++++++++++++++++++++++++++++
systTree.branchTreesSysts(trees, "all", "njet_lowpt", outTreeFile, nJet_lowpt_all)
systTree.branchTreesSysts(trees, "all", "njet_pt100", outTreeFile, nJet_pt100_all)
systTree.branchTreesSysts(trees, "all", "nfatjet", outTreeFile, nfatJet_all)
systTree.branchTreesSysts(trees, "all", "nbjet_lowpt", outTreeFile, nbJet_lowpt_all)
systTree.branchTreesSysts(trees, "all", "nbjet_pt100", outTreeFile, nbJet_pt100_all)
systTree.branchTreesSysts(trees, "all", "passed_mu", outTreeFile, passed_mu_all)
systTree.branchTreesSysts(trees, "all", "passed_ele", outTreeFile, passed_ele_all)
systTree.branchTreesSysts(trees, "all", "passed_ht", outTreeFile, passed_ht_all)
systTree.branchTreesSysts(trees, "all", "passed_ph", outTreeFile, passed_ph_all)
systTree.branchTreesSysts(trees, "all", "nPV_good", outTreeFile, nPV_good_all)
systTree.branchTreesSysts(trees, "all", "nPV_tot", outTreeFile, nPV_tot_all)
systTree.branchTreesSysts(trees, "all", "isEle", outTreeFile, isEle_all)
systTree.branchTreesSysts(trees, "all", "isMu", outTreeFile, isMu_all)
systTree.branchTreesSysts(trees, "all", "Event_HT", outTreeFile, Event_HT_all)
systTree.branchTreesSysts(trees, "all", "MET_pt", outTreeFile, MET_pt_all)
systTree.branchTreesSysts(trees, "all", "MET_phi", outTreeFile, MET_phi_all)
systTree.branchTreesSysts(trees, "all", "isdileptonic", outTreeFile, isdileptonic)
systTree.branchTreesSysts(trees, "all", "muon_pt", outTreeFile, muon_pt)
systTree.branchTreesSysts(trees, "all", "muon_eta", outTreeFile, muon_eta)
systTree.branchTreesSysts(trees, "all", "muon_phi", outTreeFile, muon_phi)
systTree.branchTreesSysts(trees, "all", "muon_m", outTreeFile, muon_m)
systTree.branchTreesSysts(trees, "all", "muon_SF", outTreeFile, muon_SF)
systTree.branchTreesSysts(trees, "all", "electron_pt", outTreeFile, electron_pt)
systTree.branchTreesSysts(trees, "all", "electron_eta", outTreeFile, electron_eta)
systTree.branchTreesSysts(trees, "all", "electron_phi", outTreeFile, electron_phi)
systTree.branchTreesSysts(trees, "all", "electron_m", outTreeFile, electron_m)
systTree.branchTreesSysts(trees, "all", "electron_SF", outTreeFile, electron_SF)
#print("Is MC: " + str(isMC) + "      option addPDF: " + str(addPDF))
####################################################################################################################################################################################################################################

#++++++++++++++++++++++++++++++++++
#++      Efficiency studies      ++
#++++++++++++++++++++++++++++++++++
nbinseff = 10
h_eff_mu = ROOT.TH1D("h_eff_mu", "h_eff_mu", nbinseff, 0, nbinseff)
h_eff_ele = ROOT.TH1D("h_eff_ele", "h_eff_ele", nbinseff, 0, nbinseff)
#++++++++++++++++++++++++++++++++++
#++   looping over the events    ++
#++++++++++++++++++++++++++++++++++
for i in range(tree.GetEntries()):
    w_nominal_all[0] = 1.
    #++++++++++++++++++++++++++++++++++
    #++        taking objects        ++
    #++++++++++++++++++++++++++++++++++
    if Debug:
        #print("evento n. " + str(i))
        if i > 2000:
            break
    if not Debug and i%5000 == 0:
        print("Event #", i+1, " out of ", tree.GetEntries())
    event = Event(tree,i)
    electrons = Collection(event, "Electron")
    muons = Collection(event, "Muon")
    jets = Collection(event, "Jet")
    njets = len(jets)
    fatjets = Collection(event, "FatJet")
    HT = Object(event, "HT")
    PV = Object(event, "PV")
    HLT = Object(event, "HLT")
    Flag = Object(event, 'Flag')
    met = Object(event, "MET")
    MET = {'metPx': met.pt*ROOT.TMath.Cos(met.phi), 'metPy': met.pt*ROOT.TMath.Sin(met.phi)}
    
    h_eff_mu.Fill('Total', 1)
    h_eff_ele.Fill('Total', 1)

    chain.GetEntry(i)
    #++++++++++++++++++++++++++++++++++
    #++      defining variables      ++
    #++++++++++++++++++++++++++++++++++
    PF_SF = None
    PF_SFUp = None
    PF_SFDown = None
    PU_SF = None
    PU_SFUp = None
    PU_SFDown = None
    #++++++++++++++++++++++++++++++++++
    #++    starting the analysis     ++
    #++++++++++++++++++++++++++++++++++
    VetoMu = get_LooseMu(muons)
    goodMu = get_Mu(muons)
    VetoEle = get_LooseEle(electrons)
    goodEle = get_Ele(electrons)
    year = sample.year
    if(isMC):
        runPeriod = None
    else:
        runPeriod = sample.runP
    passMu, passEle, passHT, passPh, noTrigger = trig_map(HLT, year, runPeriod, chain.run)
    passed_mu_all[0] = int(passMu)
    passed_ele_all[0] = int(passEle)
    passed_ph_all[0] = int(passPh)
    passed_ht_all[0] = int(passHT)
    isDilepton = (len(goodMu) == 1) and (len(goodEle) == 1) and len(VetoMu) == 0 and len(VetoEle) == 0 and (passMu or passHT or passEle or passPh)

    double_counting = False
    if not isMC:
        double_counting = True
    #Double counting removal
    if('DataMu' in sample.label and passMu):
        double_counting = False
    if('DataHT' in sample.label and (passHT and not passMu and not passEle)):
        double_counting = False
    if year == '2018':
        if('DataEle' in sample.label and (passEle or passPh) and not passMu):
            double_counting = False
    else:
        if('DataEle' in sample.label and passEle and not passMu):
            double_counting = False
        if('DataPh' in sample.label and (passHT and not passMu and not passEle)):
            double_counting = False
    if double_counting:
        continue

    #######################################
    ## Removing events with HEM problem  ##
    #######################################
    passesMETHEMVeto = HEMveto(jets, electrons)
    if(year == "2018" and not passesMETHEMVeto):
        if(not isMC and chain.runNumber > 319077.):
            continue
        elif(isMC):
            w_nominal_all[0] *= 0.354

    ######################################
    ## Selecting only jets with pt>100  ##
    ######################################
    goodJets = get_Jet(jets, 100)
    bjets, nobjets = bjet_filter(goodJets, 'DeepFlv', 'M')
    nJet_pt100_all[0] = len(goodJets)
    nbJet_pt100_all[0] = len(bjets)
    #if Debug:
        #print("len bjets: ", len(bjets), "nbJet_pt100_all: ", nbJet_pt100_all[0])
    nfatJet_all[0] = len(fatjets)
    nJet_lowpt_all[0] = len(jets) - len(goodJets)
    nbJet_lowpt_all[0] = len(bjet_filter(jets, 'DeepFlv', 'M')[0]) - len(bjets)
    ##print(len(fatjets))

    #if (len(goodJets) < 2 or len(fatjets) < 2):
        #continue

    if(isDilepton):
        muon_pt[0] = goodMu[0].pt
        muon_eta[0] = goodMu[0].eta
        muon_phi[0] = goodMu[0].phi
        electron_pt[0] = goodEle[0].pt
        electron_eta[0] = goodEle[0].eta
        electron_phi[0] = goodEle[0].phi
        electron_m[0] = goodEle[0].mass
        if(isMC):
            muon_SF[0] = goodMu[0].effSF
            electron_SF[0] = goodEle[0].effSF
        isdileptonic[0] = 1
    else:
        ##print('Event %i not a good' %(i))
        continue

    if(isMC):
        PF_SF = chain.PrefireWeight
        PF_SFUp = chain.PrefireWeight_Up
        PF_SFDown = chain.PrefireWeight_Down
        systTree.setWeightName("PFSF", copy.deepcopy(PF_SF))
        systTree.setWeightName("PFUp", copy.deepcopy(PF_SFUp))
        systTree.setWeightName("PFDown", copy.deepcopy(PF_SFDown))

        if(year == 2017 or year == 2018): 
            PU_SF = chain.puWeight
            PU_SFUp = chain.puWeightUp
            PU_SFDown = chain.puWeightDown
        
            systTree.setWeightName("puSF", copy.deepcopy(PU_SF))
            systTree.setWeightName("puUp", copy.deepcopy(PU_SFUp))
            systTree.setWeightName("puDown", copy.deepcopy(PU_SFDown))
        
    nPV_good_all[0] = PV.npvsGood
    nPV_tot_all[0] = PV.npvs

    MET_pt_all[0] = met.pt
    MET_phi_all[0] = met.phi
    Event_HT_all[0] = HT.eventHT
        
    systTree.setWeightName("w_nominal",copy.deepcopy(w_nominal_all[0]))
    systTree.fillTreesSysts(trees, "all")

#trees[0].Print()
outTreeFile.cd()
systTree.writeTreesSysts(trees, outTreeFile)
print("Number of events in chain " + str(trees[0].GetEntries()))
endTime = datetime.datetime.now()
print("Ending running at " + str(endTime))
