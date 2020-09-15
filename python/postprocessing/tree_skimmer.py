#!/bin/env python3
import os
#print(os.environ)
#print("**********************************************************************")
#print("**********************************************************************")
#print("**********************************************************************")
#print(str(os.environ.get('PYTHONPATH')))
#print(str(os.environ.get('PYTHON3PATH')))
import sys
#print("*************** This is system version info ***************************")
#print(sys.version_info)
#import platform
#print("*************** This is python version info ***************************")
#print(platform.python_version())
import ROOT
#print("Succesfully imported ROOT")
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
print("file_list: ", file_list, "\nloop #1 over it")
for infile in file_list:
    print(infile)

MCReco = True
DeltaFilter = True
TriggerStudy = False # True #
bjetSwitch = False # True #
startTime = datetime.datetime.now()
print("Starting running at " + str(startTime))

ROOT.gROOT.SetBatch()

leadingjet_ptcut = 150.

chain = ROOT.TChain('Events')
print(chain)
print("loop #2 over file_list")
for infile in file_list: 
    print("Adding %s to the chain" %(infile))
    chain.Add(infile)

print("Number of events in chain " + str(chain.GetEntries()))
print("Number of events in tree from chain " + str((chain.GetTree()).GetEntries()))
print("Type of tree from chain " + str(type(chain.GetTree())))
#treechain = (ROOT.TTree)(chain.GetTree())
tree = InputTree(chain)
print("Number of entries: " +str(tree.GetEntries()))
print("tree: ", tree)
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
addPDF = True
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
'''
systTree.setWeightName("btagUp",1.)
systTree.setWeightName("btagDown",1.)
systTree.setWeightName("mistagUp",1.)
systTree.setWeightName("mistagDown",1.)
systTree.setWeightName("puUp",1.)
systTree.setWeightName("puDown",1.)
'''
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
#Reconstructed Wprime
if MCReco:
    MC_Wprime_pt_all = array.array('f', [0.])
    MC_Wprime_eta_all = array.array('f', [0.])
    MC_Wprime_phi_all = array.array('f', [0.])
    MC_Wprime_m_all = array.array('f', [0.])
    MC_Wprime_mt_all = array.array('f', [0.])
    GenPart_Wprime_pt_all = array.array('f', [0.])
    GenPart_Wprime_eta_all = array.array('f', [0.])
    GenPart_Wprime_phi_all = array.array('f', [0.])
    GenPart_Wprime_m_all = array.array('f', [0.])
    GenPart_Wprime_mt_all = array.array('f', [0.])
closest_Wprime_pt_all = array.array('f', [0.])
closest_Wprime_eta_all = array.array('f', [0.])
closest_Wprime_phi_all = array.array('f', [0.])
closest_Wprime_m_all = array.array('f', [0.])
closest_Wprime_mt_all = array.array('f', [0.])
chi_Wprime_pt_all = array.array('f', [0.])
chi_Wprime_eta_all = array.array('f', [0.])
chi_Wprime_phi_all = array.array('f', [0.])
chi_Wprime_m_all = array.array('f', [0.])
chi_Wprime_mt_all = array.array('f', [0.])
sublead_Wprime_pt_all = array.array('f', [0.])
sublead_Wprime_eta_all = array.array('f', [0.])
sublead_Wprime_phi_all = array.array('f', [0.])
sublead_Wprime_m_all = array.array('f', [0.])
sublead_Wprime_mt_all = array.array('f', [0.])
best_Wprime_pt_all = array.array('f', [0.])
best_Wprime_eta_all = array.array('f', [0.])
best_Wprime_phi_all = array.array('f', [0.])
best_Wprime_m_all = array.array('f', [0.])
best_Wprime_mt_all = array.array('f', [0.])

#Reconstructed Top
if MCReco:
    MC_RecoTop_pt_all = array.array('f', [0.])
    MC_RecoTop_eta_all = array.array('f', [0.])
    MC_RecoTop_phi_all = array.array('f', [0.])
    MC_RecoTop_m_all = array.array('f', [0.])
    MC_RecoTop_mt_all = array.array('f', [0.])
    GenPart_Top_pt_all = array.array('f', [0.])
    GenPart_Top_eta_all = array.array('f', [0.])
    GenPart_Top_phi_all = array.array('f', [0.])
    GenPart_Top_m_all = array.array('f', [0.])
    GenPart_Top_mt_all = array.array('f', [0.])
    MC_RecoTop_isNeg_all = array.array('i', [0])
    MC_RecoTop_chi2_all = array.array('i', [0])
    if(TriggerStudy):
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
closest_RecoTop_pt_all = array.array('f', [0.])
closest_RecoTop_eta_all = array.array('f', [0.])
closest_RecoTop_phi_all = array.array('f', [0.])
closest_RecoTop_m_all = array.array('f', [0.])
closest_RecoTop_mt_all = array.array('f', [0.])
closest_RecoTop_isNeg_all = array.array('i', [0])
closest_RecoTop_chi2_all = array.array('i', [0])
closest_RecoTop_costheta_all = array.array('f', [0.])
closest_RecoTop_costhetalep_all = array.array('f', [0.])
chi_RecoTop_pt_all = array.array('f', [0.])
chi_RecoTop_eta_all = array.array('f', [0.])
chi_RecoTop_phi_all = array.array('f', [0.])
chi_RecoTop_m_all = array.array('f', [0.])
chi_RecoTop_mt_all = array.array('f', [0.])
chi_RecoTop_isNeg_all = array.array('i', [0])
chi_RecoTop_chi2_all = array.array('i', [0])
chi_RecoTop_costheta_all = array.array('f', [0.])
chi_RecoTop_costhetalep_all = array.array('f', [0.])
sublead_RecoTop_pt_all = array.array('f', [0.])
sublead_RecoTop_eta_all = array.array('f', [0.])
sublead_RecoTop_phi_all = array.array('f', [0.])
sublead_RecoTop_m_all = array.array('f', [0.])
sublead_RecoTop_mt_all = array.array('f', [0.])
sublead_RecoTop_isNeg_all = array.array('i', [0])
sublead_RecoTop_chi2_all = array.array('i', [0])
sublead_RecoTop_costheta_all = array.array('f', [0.])
sublead_RecoTop_costhetalep_all = array.array('f', [0.])
best_RecoTop_pt_all = array.array('f', [0.])
best_RecoTop_eta_all = array.array('f', [0.])
best_RecoTop_phi_all = array.array('f', [0.])
best_RecoTop_m_all = array.array('f', [0.])
best_RecoTop_mt_all = array.array('f', [0.])
best_RecoTop_isNeg_all = array.array('i', [0])
best_RecoTop_chi2_all = array.array('i', [0])
best_RecoTop_costheta_all = array.array('f', [0.])
best_RecoTop_costhetalep_all = array.array('f', [0.])

nJet_lowpt_all = array.array('i', [0])
nfatJet_all = array.array('i', [0])
nJet_pt100_all = array.array('i', [0])
nbJet_lowpt_all = array.array('i', [0])
nbJet_pt100_all = array.array('i', [0])
nlep_all  = array.array('i', [0])

#Jet produced after top semilep decay
if MCReco:
    MC_TopJet_pt_all = array.array('f', [0.])
    MC_TopJet_eta_all = array.array('f', [0.])
    MC_TopJet_phi_all = array.array('f', [0.])
    MC_TopJet_m_all = array.array('f', [0.])
    MC_TopJet_dRLepJet_all = array.array('f', [0])
closest_TopJet_pt_all = array.array('f', [0.])
closest_TopJet_eta_all = array.array('f', [0.])
closest_TopJet_phi_all = array.array('f', [0.])
closest_TopJet_m_all = array.array('f', [0.])
closest_TopJet_isBTagged_all = array.array('i', [0])
closest_TopJet_dRLepJet_all = array.array('f', [0])
chi_TopJet_pt_all = array.array('f', [0.])
chi_TopJet_eta_all = array.array('f', [0.])
chi_TopJet_phi_all = array.array('f', [0.])
chi_TopJet_m_all = array.array('f', [0.])
chi_TopJet_isBTagged_all = array.array('i', [0])
chi_TopJet_dRLepJet_all = array.array('f', [0])
sublead_TopJet_pt_all = array.array('f', [0.])
sublead_TopJet_eta_all = array.array('f', [0.])
sublead_TopJet_phi_all = array.array('f', [0.])
sublead_TopJet_m_all = array.array('f', [0.])
sublead_TopJet_isBTagged_all = array.array('i', [0])
sublead_TopJet_dRLepJet_all = array.array('f', [0])
best_TopJet_pt_all = array.array('f', [0.])
best_TopJet_eta_all = array.array('f', [0.])
best_TopJet_phi_all = array.array('f', [0.])
best_TopJet_m_all = array.array('f', [0.])
best_TopJet_isBTagged_all = array.array('i', [0])
best_TopJet_btagscore_all = array.array('f', [0])
best_TopJet_dRLepJet_all = array.array('f', [0])

Event_HT_all = array.array('f', [0.])

'''
closest_TopJet_isDFL_all = array.array('i', [0])
closest_TopJet_isDFM_all = array.array('i', [0])
closest_TopJet_isDFT_all = array.array('i', [0])
closest_TopJet_isDCL_all = array.array('i', [0])
closest_TopJet_isDCM_all = array.array('i', [0])
closest_TopJet_isDCT_all = array.array('i', [0])
chi_TopJet_isDFL_all = array.array('i', [0])
chi_TopJet_isDFM_all = array.array('i', [0])
chi_TopJet_isDFT_all = array.array('i', [0])
chi_TopJet_isDCL_all = array.array('i', [0])
chi_TopJet_isDCM_all = array.array('i', [0])
chi_TopJet_isDCT_all = array.array('i', [0])
sublead_TopJet_isDFL_all = array.array('i', [0])
sublead_TopJet_isDFM_all = array.array('i', [0])
sublead_TopJet_isDFT_all = array.array('i', [0])
sublead_TopJet_isDCL_all = array.array('i', [0])
sublead_TopJet_isDCM_all = array.array('i', [0])
sublead_TopJet_isDCT_all = array.array('i', [0])
best_TopJet_isDFL_all = array.array('i', [0])
best_TopJet_isDFM_all = array.array('i', [0])
best_TopJet_isDFT_all = array.array('i', [0])
best_TopJet_isDCL_all = array.array('i', [0])
best_TopJet_isDCM_all = array.array('i', [0])
best_TopJet_isDCT_all = array.array('i', [0])
'''

#Prompt jet from Wprime decay
if MCReco:
    MC_WpJet_pt_all = array.array('f', [0.])
    MC_WpJet_eta_all = array.array('f', [0.])
    MC_WpJet_phi_all = array.array('f', [0.])
    MC_WpJet_m_all = array.array('f', [0.])
    GenPart_Bottom_pt_all = array.array('f', [0.])
    GenPart_Bottom_eta_all = array.array('f', [0.])
    GenPart_Bottom_phi_all = array.array('f', [0.])
    GenPart_Bottom_m_all = array.array('f', [0.])
closest_WpJet_pt_all = array.array('f', [0.])
closest_WpJet_eta_all = array.array('f', [0.])
closest_WpJet_phi_all = array.array('f', [0.])
closest_WpJet_m_all = array.array('f', [0.])
closest_WpJet_isBTagged_all = array.array('i', [0])
chi_WpJet_pt_all = array.array('f', [0.])
chi_WpJet_eta_all = array.array('f', [0.])
chi_WpJet_phi_all = array.array('f', [0.])
chi_WpJet_m_all = array.array('f', [0.])
chi_WpJet_isBTagged_all = array.array('i', [0])
sublead_WpJet_pt_all = array.array('f', [0.])
sublead_WpJet_eta_all = array.array('f', [0.])
sublead_WpJet_phi_all = array.array('f', [0.])
sublead_WpJet_m_all = array.array('f', [0.])
sublead_WpJet_isBTagged_all = array.array('i', [0])
best_WpJet_pt_all = array.array('f', [0.])
best_WpJet_eta_all = array.array('f', [0.])
best_WpJet_phi_all = array.array('f', [0.])
best_WpJet_m_all = array.array('f', [0.])
best_WpJet_isBTagged_all = array.array('i', [0])
best_WpJet_btagscore_all = array.array('f', [0])
'''
closest_WpJet_isDFL_all = array.array('i', [0])
closest_WpJet_isDFM_all = array.array('i', [0])
closest_WpJet_isDFT_all = array.array('i', [0])
closest_WpJet_isDCL_all = array.array('i', [0])
closest_WpJet_isDCM_all = array.array('i', [0])
closest_WpJet_isDCT_all = array.array('i', [0])
chi_WpJet_isDFL_all = array.array('i', [0])
chi_WpJet_isDFM_all = array.array('i', [0])
chi_WpJet_isDFT_all = array.array('i', [0])
chi_WpJet_isDCL_all = array.array('i', [0])
chi_WpJet_isDCM_all = array.array('i', [0])
chi_WpJet_isDCT_all = array.array('i', [0])
sublead_WpJet_isDFL_all = array.array('i', [0])
sublead_WpJet_isDFM_all = array.array('i', [0])
sublead_WpJet_isDFT_all = array.array('i', [0])
sublead_WpJet_isDCL_all = array.array('i', [0])
sublead_WpJet_isDCM_all = array.array('i', [0])
sublead_WpJet_isDCT_all = array.array('i', [0])
best_WpJet_isDFL_all = array.array('i', [0])
best_WpJet_isDFM_all = array.array('i', [0])
best_WpJet_isDFT_all = array.array('i', [0])
best_WpJet_isDCL_all = array.array('i', [0])
best_WpJet_isDCM_all = array.array('i', [0])
best_WpJet_isDCT_all = array.array('i', [0])
'''

#Lepton
lepton_pt_all = array.array('f', [0.])
lepton_eta_all = array.array('f', [0.])
lepton_phi_all = array.array('f', [0.])
lepton_miniIso_all = array.array('f', [0.])
lepton_stdIso_all = array.array('f', [0.])
lepMET_deltaPhi_all = array.array('f', [0.])
isEle_all = array.array('i', [0])
isMu_all = array.array('i', [0])

MET_pt_all = array.array('f', [0.])
MET_phi_all = array.array('f', [0.])

nPV_tot_all = array.array('f', [0.])
nPV_good_all = array.array('f', [0.])
mtw_all = array.array('f', [0.])
#mtt = array.array('f', [0.])

w_nominal_all = array.array('f', [0.])
w_PDF_all = array.array('f', [0.]*110)
passed_mu_all = array.array('f', [0.])
passed_ele_all = array.array('f', [0.])
passed_ht_all = array.array('f', [0.])
leadingjet_pt_all = array.array('f', [0.])
subleadingjet_pt_all = array.array('f', [0.])
leadingbjet_pt_all = array.array('f', [0.])
subleadingbjet_pt_all = array.array('f', [0.])

leadingjets_deltaPhi = array.array('f', [0.])
leadingjets_deltaEta = array.array('f', [0.])
leadingjets_deltaR = array.array('f', [0.])
leadingjets_pt = array.array('f', [0.])
bjets_deltaPhi = array.array('f', [0.])
bjets_deltaEta = array.array('f', [0.])
bjets_deltaR = array.array('f', [0.])
bjets_pt = array.array('f', [0.])
had_global_thrust = array.array('f', [0.])
had_central_thrust = array.array('f', [0.])
ovr_global_thrust = array.array('f', [0.])
ovr_central_thrust = array.array('f', [0.])
deltaR_lep_closestjet = array.array('f', [0.])
deltaR_lep_leadingjet = array.array('f', [0.])
deltaR_lep_subleadingjet = array.array('f', [0.])
ptrel_leadAK4_closestAK8 = array.array('f', [0.])
deltaR_leadAK4_closestAK8 = array.array('f', [0.])
ptrel_subleadAK4_closestAK8 = array.array('f', [0.])
deltaR_subleadAK4_closestAK8 = array.array('f', [0.])
ptrel_besttopAK4_closestAK8 = array.array('f', [0.])
deltaR_besttopAK4_closestAK8 = array.array('f', [0.])
ptrel_chitopAK4_closestAK8 = array.array('f', [0.])
deltaR_chitopAK4_closestAK8 = array.array('f', [0.])
ptrel_bestWAK4_closestAK8 = array.array('f', [0.])
deltaR_bestWAK4_closestAK8 = array.array('f', [0.])
ptrel_chiWAK4_closestAK8 = array.array('f', [0.])
deltaR_chiWAK4_closestAK8 = array.array('f', [0.])
best_topW_jets_pt = array.array('f', [0.])
best_topW_jets_deltaR = array.array('f', [0.])
best_topW_jets_deltaphi = array.array('f', [0.])
chi_topW_jets_pt = array.array('f', [0.])
chi_topW_jets_deltaR = array.array('f', [0.])
chi_topW_jets_deltaphi = array.array('f', [0.])

#FatJet
topAK8_area = array.array('f', [0.])
topAK8_btag = array.array('f', [0.])
topAK8_ttagMD = array.array('f', [0.])
topAK8_ttag = array.array('f', [0.])
topAK8_eta = array.array('f', [0.])
topAK8_m = array.array('f', [0.])
topAK8_mSD = array.array('f', [0.])
topAK8_phi = array.array('f', [0.])
topAK8_pt = array.array('f', [0.])
topAK8_tau1 = array.array('f', [0.])
topAK8_tau2 = array.array('f', [0.])
topAK8_tau3 = array.array('f', [0.])
topAK8_tau4 = array.array('f', [0.])

WprAK8_area = array.array('f', [0.])
WprAK8_btag = array.array('f', [0.])
WprAK8_ttagMD = array.array('f', [0.])
WprAK8_ttag = array.array('f', [0.])
WprAK8_eta = array.array('f', [0.])
WprAK8_m = array.array('f', [0.])
WprAK8_mSD = array.array('f', [0.])
WprAK8_phi = array.array('f', [0.])
WprAK8_pt = array.array('f', [0.])
WprAK8_tau1 = array.array('f', [0.])
WprAK8_tau2 = array.array('f', [0.])
WprAK8_tau3 = array.array('f', [0.])
WprAK8_tau4 = array.array('f', [0.])
#FatJet_electronIdx3SJ
#FatJet_genJetAK8Idx
#FatJet_hadronFlavour
#FatJet_jetId Int_tJet ID flags bit1 is loose (always false in 2017 since it does not exist), bit2 is tight, bit3 is tightLepVeto
#FatJet_lsf3 Float_tLepton Subjet Fraction (3 subjets)
#FatJet_muonIdx3SJ
#FatJet_n2b1 Float_tN2 with beta=1
#FatJet_n3b1 Float_tN3 with beta=1
#FatJet_nBHadrons UChar_tnumber of b-hadrons
#FatJet_nCHadrons UChar_tnumber of c-hadrons

#++++++++++++++++++++++++++++++++++
#++   branching the new trees    ++
#++++++++++++++++++++++++++++++++++
if MCReco:
    systTree.branchTreesSysts(trees, "all", "MC_Wprime_pt", outTreeFile, MC_Wprime_pt_all)
    systTree.branchTreesSysts(trees, "all", "MC_Wprime_eta", outTreeFile, MC_Wprime_eta_all)
    systTree.branchTreesSysts(trees, "all", "MC_Wprime_phi", outTreeFile, MC_Wprime_phi_all)
    systTree.branchTreesSysts(trees, "all", "MC_Wprime_m", outTreeFile, MC_Wprime_m_all)
    systTree.branchTreesSysts(trees, "all", "MC_Wprime_mt", outTreeFile, MC_Wprime_mt_all)
    systTree.branchTreesSysts(trees, "all", "GenPart_Wprime_pt", outTreeFile, GenPart_Wprime_pt_all)
    systTree.branchTreesSysts(trees, "all", "GenPart_Wprime_eta", outTreeFile, GenPart_Wprime_eta_all)
    systTree.branchTreesSysts(trees, "all", "GenPart_Wprime_phi", outTreeFile, GenPart_Wprime_phi_all)
    systTree.branchTreesSysts(trees, "all", "GenPart_Wprime_m", outTreeFile, GenPart_Wprime_m_all)
    systTree.branchTreesSysts(trees, "all", "GenPart_Wprime_mt", outTreeFile, GenPart_Wprime_mt_all)
systTree.branchTreesSysts(trees, "all", "closest_Wprime_pt", outTreeFile, closest_Wprime_pt_all)
systTree.branchTreesSysts(trees, "all", "closest_Wprime_eta", outTreeFile, closest_Wprime_eta_all)
systTree.branchTreesSysts(trees, "all", "closest_Wprime_phi", outTreeFile, closest_Wprime_phi_all)
systTree.branchTreesSysts(trees, "all", "closest_Wprime_m", outTreeFile, closest_Wprime_m_all)
systTree.branchTreesSysts(trees, "all", "closest_Wprime_mt", outTreeFile, closest_Wprime_mt_all)
systTree.branchTreesSysts(trees, "all", "chi_Wprime_pt", outTreeFile, chi_Wprime_pt_all)
systTree.branchTreesSysts(trees, "all", "chi_Wprime_eta", outTreeFile, chi_Wprime_eta_all)
systTree.branchTreesSysts(trees, "all", "chi_Wprime_phi", outTreeFile, chi_Wprime_phi_all)
systTree.branchTreesSysts(trees, "all", "chi_Wprime_m", outTreeFile, chi_Wprime_m_all)
systTree.branchTreesSysts(trees, "all", "chi_Wprime_mt", outTreeFile, chi_Wprime_mt_all)
systTree.branchTreesSysts(trees, "all", "sublead_Wprime_pt", outTreeFile, sublead_Wprime_pt_all)
systTree.branchTreesSysts(trees, "all", "sublead_Wprime_eta", outTreeFile, sublead_Wprime_eta_all)
systTree.branchTreesSysts(trees, "all", "sublead_Wprime_phi", outTreeFile, sublead_Wprime_phi_all)
systTree.branchTreesSysts(trees, "all", "sublead_Wprime_m", outTreeFile, sublead_Wprime_m_all)
systTree.branchTreesSysts(trees, "all", "sublead_Wprime_mt", outTreeFile, sublead_Wprime_mt_all)
systTree.branchTreesSysts(trees, "all", "best_Wprime_pt", outTreeFile, best_Wprime_pt_all)
systTree.branchTreesSysts(trees, "all", "best_Wprime_eta", outTreeFile, best_Wprime_eta_all)
systTree.branchTreesSysts(trees, "all", "best_Wprime_phi", outTreeFile, best_Wprime_phi_all)
systTree.branchTreesSysts(trees, "all", "best_Wprime_m", outTreeFile, best_Wprime_m_all)
systTree.branchTreesSysts(trees, "all", "best_Wprime_mt", outTreeFile, best_Wprime_mt_all)

systTree.branchTreesSysts(trees, "all", "njet_lowpt", outTreeFile, nJet_lowpt_all)
systTree.branchTreesSysts(trees, "all", "njet_pt100", outTreeFile, nJet_pt100_all)
systTree.branchTreesSysts(trees, "all", "nfatjet", outTreeFile, nfatJet_all)
systTree.branchTreesSysts(trees, "all", "nbjet_lowpt", outTreeFile, nbJet_lowpt_all)
systTree.branchTreesSysts(trees, "all", "nbjet_pt100", outTreeFile, nbJet_pt100_all)
systTree.branchTreesSysts(trees, "all", "leadingjet_pt", outTreeFile, leadingjet_pt_all)
systTree.branchTreesSysts(trees, "all", "subleadingjet_pt", outTreeFile, subleadingjet_pt_all)
systTree.branchTreesSysts(trees, "all", "leadingbjet_pt", outTreeFile, leadingbjet_pt_all)
systTree.branchTreesSysts(trees, "all", "subleadingbjet_pt", outTreeFile, subleadingbjet_pt_all)
systTree.branchTreesSysts(trees, "all", "leadingjets_deltaR", outTreeFile, leadingjets_deltaR)
systTree.branchTreesSysts(trees, "all", "leadingjets_deltaPhi", outTreeFile, leadingjets_deltaPhi)
systTree.branchTreesSysts(trees, "all", "leadingjets_deltaEta", outTreeFile, leadingjets_deltaEta)
systTree.branchTreesSysts(trees, "all", "leadingjets_pt", outTreeFile, leadingjets_pt)
systTree.branchTreesSysts(trees, "all", "bjets_deltaR", outTreeFile, bjets_deltaR)
systTree.branchTreesSysts(trees, "all", "bjets_deltaPhi", outTreeFile, bjets_deltaPhi)
systTree.branchTreesSysts(trees, "all", "bjets_deltaEta", outTreeFile, bjets_deltaEta)
systTree.branchTreesSysts(trees, "all", "bjets_pt", outTreeFile, bjets_pt)
systTree.branchTreesSysts(trees, "all", "had_global_thrust", outTreeFile, had_global_thrust)
systTree.branchTreesSysts(trees, "all", "had_central_thrust", outTreeFile, had_central_thrust)
systTree.branchTreesSysts(trees, "all", "ovr_global_thrust", outTreeFile, ovr_global_thrust)
systTree.branchTreesSysts(trees, "all", "ovr_central_thrust", outTreeFile, ovr_central_thrust)
systTree.branchTreesSysts(trees, "all", "deltaR_lep_closestjet", outTreeFile, deltaR_lep_closestjet)
systTree.branchTreesSysts(trees, "all", "deltaR_lep_leadingjet", outTreeFile, deltaR_lep_leadingjet)
systTree.branchTreesSysts(trees, "all", "deltaR_lep_subleadingjet", outTreeFile, deltaR_lep_subleadingjet)
if MCReco:
    systTree.branchTreesSysts(trees, "all", "MC_top_pt", outTreeFile, MC_RecoTop_pt_all)
    systTree.branchTreesSysts(trees, "all", "MC_top_eta", outTreeFile, MC_RecoTop_eta_all)
    systTree.branchTreesSysts(trees, "all", "MC_top_phi", outTreeFile, MC_RecoTop_phi_all)
    systTree.branchTreesSysts(trees, "all", "MC_top_m", outTreeFile, MC_RecoTop_m_all)
    systTree.branchTreesSysts(trees, "all", "MC_top_mt", outTreeFile, MC_RecoTop_mt_all)
    systTree.branchTreesSysts(trees, "all", "GenPart_top_pt", outTreeFile, GenPart_Top_pt_all)
    systTree.branchTreesSysts(trees, "all", "GenPart_top_eta", outTreeFile, GenPart_Top_eta_all)
    systTree.branchTreesSysts(trees, "all", "GenPart_top_phi", outTreeFile, GenPart_Top_phi_all)
    systTree.branchTreesSysts(trees, "all", "GenPart_top_m", outTreeFile, GenPart_Top_m_all)
    systTree.branchTreesSysts(trees, "all", "GenPart_top_mt", outTreeFile, GenPart_Top_mt_all)
    systTree.branchTreesSysts(trees, "all", "MC_top_isNeg", outTreeFile, MC_RecoTop_isNeg_all)
systTree.branchTreesSysts(trees, "all", "closest_top_pt", outTreeFile, closest_RecoTop_pt_all)
systTree.branchTreesSysts(trees, "all", "closest_top_eta", outTreeFile, closest_RecoTop_eta_all)
systTree.branchTreesSysts(trees, "all", "closest_top_phi", outTreeFile, closest_RecoTop_phi_all)
systTree.branchTreesSysts(trees, "all", "closest_top_m", outTreeFile, closest_RecoTop_m_all)
systTree.branchTreesSysts(trees, "all", "closest_top_mt", outTreeFile, closest_RecoTop_mt_all)
systTree.branchTreesSysts(trees, "all", "closest_top_costheta", outTreeFile, closest_RecoTop_costheta_all)
systTree.branchTreesSysts(trees, "all", "closest_top_costhetalep", outTreeFile, closest_RecoTop_costhetalep_all)
systTree.branchTreesSysts(trees, "all", "closest_top_isNeg", outTreeFile, closest_RecoTop_isNeg_all)
systTree.branchTreesSysts(trees, "all", "chi_top_pt", outTreeFile, chi_RecoTop_pt_all)
systTree.branchTreesSysts(trees, "all", "chi_top_eta", outTreeFile, chi_RecoTop_eta_all)
systTree.branchTreesSysts(trees, "all", "chi_top_phi", outTreeFile, chi_RecoTop_phi_all)
systTree.branchTreesSysts(trees, "all", "chi_top_m", outTreeFile, chi_RecoTop_m_all)
systTree.branchTreesSysts(trees, "all", "chi_top_costheta", outTreeFile, chi_RecoTop_costheta_all)
systTree.branchTreesSysts(trees, "all", "chi_top_costhetalep", outTreeFile, chi_RecoTop_costhetalep_all)
systTree.branchTreesSysts(trees, "all", "chi_top_mt", outTreeFile, chi_RecoTop_mt_all)
systTree.branchTreesSysts(trees, "all", "chi_top_isNeg", outTreeFile, chi_RecoTop_isNeg_all)
systTree.branchTreesSysts(trees, "all", "sublead_top_pt", outTreeFile, sublead_RecoTop_pt_all)
systTree.branchTreesSysts(trees, "all", "sublead_top_eta", outTreeFile, sublead_RecoTop_eta_all)
systTree.branchTreesSysts(trees, "all", "sublead_top_phi", outTreeFile, sublead_RecoTop_phi_all)
systTree.branchTreesSysts(trees, "all", "sublead_top_m", outTreeFile, sublead_RecoTop_m_all)
systTree.branchTreesSysts(trees, "all", "sublead_top_costheta", outTreeFile, sublead_RecoTop_costheta_all)
systTree.branchTreesSysts(trees, "all", "sublead_top_costhetalep", outTreeFile, sublead_RecoTop_costhetalep_all)
systTree.branchTreesSysts(trees, "all", "sublead_top_mt", outTreeFile, sublead_RecoTop_mt_all)
systTree.branchTreesSysts(trees, "all", "sublead_top_isNeg", outTreeFile, sublead_RecoTop_isNeg_all)
systTree.branchTreesSysts(trees, "all", "best_top_pt", outTreeFile, best_RecoTop_pt_all)
systTree.branchTreesSysts(trees, "all", "best_top_eta", outTreeFile, best_RecoTop_eta_all)
systTree.branchTreesSysts(trees, "all", "best_top_phi", outTreeFile, best_RecoTop_phi_all)
systTree.branchTreesSysts(trees, "all", "best_top_m", outTreeFile, best_RecoTop_m_all)
systTree.branchTreesSysts(trees, "all", "best_top_costheta", outTreeFile, best_RecoTop_costheta_all)
systTree.branchTreesSysts(trees, "all", "best_top_costhetalep", outTreeFile, best_RecoTop_costhetalep_all)
systTree.branchTreesSysts(trees, "all", "best_top_mt", outTreeFile, best_RecoTop_mt_all)
systTree.branchTreesSysts(trees, "all", "best_top_isNeg", outTreeFile, best_RecoTop_isNeg_all)

if MCReco:
    systTree.branchTreesSysts(trees, "all", "MC_topjet_pt", outTreeFile, MC_TopJet_pt_all)
    systTree.branchTreesSysts(trees, "all", "MC_topjet_eta", outTreeFile, MC_TopJet_eta_all)
    systTree.branchTreesSysts(trees, "all", "MC_topjet_phi", outTreeFile, MC_TopJet_phi_all)
    systTree.branchTreesSysts(trees, "all", "MC_topjet_m", outTreeFile, MC_TopJet_m_all)
    systTree.branchTreesSysts(trees, "all", "MC_topjet_dRLepJet", outTreeFile, MC_TopJet_dRLepJet_all)
systTree.branchTreesSysts(trees, "all", "closest_topjet_pt", outTreeFile, closest_TopJet_pt_all)
systTree.branchTreesSysts(trees, "all", "closest_topjet_eta", outTreeFile, closest_TopJet_eta_all)
systTree.branchTreesSysts(trees, "all", "closest_topjet_phi", outTreeFile, closest_TopJet_phi_all)
systTree.branchTreesSysts(trees, "all", "closest_topjet_m", outTreeFile, closest_TopJet_m_all)
systTree.branchTreesSysts(trees, "all", "closest_topjet_isbtag", outTreeFile, closest_TopJet_isBTagged_all)
systTree.branchTreesSysts(trees, "all", "closest_topjet_dRLepJet", outTreeFile, closest_TopJet_dRLepJet_all)
systTree.branchTreesSysts(trees, "all", "chi_topjet_pt", outTreeFile, chi_TopJet_pt_all)
systTree.branchTreesSysts(trees, "all", "chi_topjet_eta", outTreeFile, chi_TopJet_eta_all)
systTree.branchTreesSysts(trees, "all", "chi_topjet_phi", outTreeFile, chi_TopJet_phi_all)
systTree.branchTreesSysts(trees, "all", "chi_topjet_m", outTreeFile, chi_TopJet_m_all)
systTree.branchTreesSysts(trees, "all", "chi_topjet_isbtag", outTreeFile, chi_TopJet_isBTagged_all)
systTree.branchTreesSysts(trees, "all", "chi_topjet_dRLepJet", outTreeFile, chi_TopJet_dRLepJet_all)
systTree.branchTreesSysts(trees, "all", "sublead_topjet_pt", outTreeFile, sublead_TopJet_pt_all)
systTree.branchTreesSysts(trees, "all", "sublead_topjet_eta", outTreeFile, sublead_TopJet_eta_all)
systTree.branchTreesSysts(trees, "all", "sublead_topjet_phi", outTreeFile, sublead_TopJet_phi_all)
systTree.branchTreesSysts(trees, "all", "sublead_topjet_m", outTreeFile, sublead_TopJet_m_all)
systTree.branchTreesSysts(trees, "all", "sublead_topjet_isbtag", outTreeFile, sublead_TopJet_isBTagged_all)
systTree.branchTreesSysts(trees, "all", "sublead_topjet_dRLepJet", outTreeFile, sublead_TopJet_dRLepJet_all)
systTree.branchTreesSysts(trees, "all", "best_topjet_pt", outTreeFile, best_TopJet_pt_all)
systTree.branchTreesSysts(trees, "all", "best_topjet_eta", outTreeFile, best_TopJet_eta_all)
systTree.branchTreesSysts(trees, "all", "best_topjet_phi", outTreeFile, best_TopJet_phi_all)
systTree.branchTreesSysts(trees, "all", "best_topjet_m", outTreeFile, best_TopJet_m_all)
systTree.branchTreesSysts(trees, "all", "best_topjet_isbtag", outTreeFile, best_TopJet_isBTagged_all)
systTree.branchTreesSysts(trees, "all", "best_topjet_btagscore", outTreeFile, best_TopJet_btagscore_all)
systTree.branchTreesSysts(trees, "all", "best_topjet_dRLepJet", outTreeFile, best_TopJet_dRLepJet_all)

if MCReco:
    systTree.branchTreesSysts(trees, "all", "MC_Wpjet_pt", outTreeFile, MC_WpJet_pt_all)
    systTree.branchTreesSysts(trees, "all", "MC_Wpjet_eta", outTreeFile, MC_WpJet_eta_all)
    systTree.branchTreesSysts(trees, "all", "MC_Wpjet_phi", outTreeFile, MC_WpJet_phi_all)
    systTree.branchTreesSysts(trees, "all", "MC_Wpjet_m", outTreeFile, MC_WpJet_m_all)
    systTree.branchTreesSysts(trees, "all", "GenPart_bottom_pt", outTreeFile, GenPart_Bottom_pt_all)
    systTree.branchTreesSysts(trees, "all", "GenPart_bottom_eta", outTreeFile, GenPart_Bottom_eta_all)
    systTree.branchTreesSysts(trees, "all", "GenPart_bottom_phi", outTreeFile, GenPart_Bottom_phi_all)
    systTree.branchTreesSysts(trees, "all", "GenPart_bottom_m", outTreeFile, GenPart_Bottom_m_all)
systTree.branchTreesSysts(trees, "all", "closest_Wpjet_pt", outTreeFile, closest_WpJet_pt_all)
systTree.branchTreesSysts(trees, "all", "closest_Wpjet_eta", outTreeFile, closest_WpJet_eta_all)
systTree.branchTreesSysts(trees, "all", "closest_Wpjet_phi", outTreeFile, closest_WpJet_phi_all)
systTree.branchTreesSysts(trees, "all", "closest_Wpjet_m", outTreeFile, closest_WpJet_m_all)
systTree.branchTreesSysts(trees, "all", "closest_Wpjet_isbtag", outTreeFile, closest_WpJet_isBTagged_all)
systTree.branchTreesSysts(trees, "all", "chi_Wpjet_pt", outTreeFile, chi_WpJet_pt_all)
systTree.branchTreesSysts(trees, "all", "chi_Wpjet_eta", outTreeFile, chi_WpJet_eta_all)
systTree.branchTreesSysts(trees, "all", "chi_Wpjet_phi", outTreeFile, chi_WpJet_phi_all)
systTree.branchTreesSysts(trees, "all", "chi_Wpjet_m", outTreeFile, chi_WpJet_m_all)
systTree.branchTreesSysts(trees, "all", "chi_Wpjet_isbtag", outTreeFile, chi_WpJet_isBTagged_all)
systTree.branchTreesSysts(trees, "all", "sublead_Wpjet_pt", outTreeFile, sublead_WpJet_pt_all)
systTree.branchTreesSysts(trees, "all", "sublead_Wpjet_eta", outTreeFile, sublead_WpJet_eta_all)
systTree.branchTreesSysts(trees, "all", "sublead_Wpjet_phi", outTreeFile, sublead_WpJet_phi_all)
systTree.branchTreesSysts(trees, "all", "sublead_Wpjet_m", outTreeFile, sublead_WpJet_m_all)
systTree.branchTreesSysts(trees, "all", "sublead_Wpjet_isbtag", outTreeFile, sublead_WpJet_isBTagged_all)
systTree.branchTreesSysts(trees, "all", "best_Wpjet_pt", outTreeFile, best_WpJet_pt_all)
systTree.branchTreesSysts(trees, "all", "best_Wpjet_eta", outTreeFile, best_WpJet_eta_all)
systTree.branchTreesSysts(trees, "all", "best_Wpjet_phi", outTreeFile, best_WpJet_phi_all)
systTree.branchTreesSysts(trees, "all", "best_Wpjet_m", outTreeFile, best_WpJet_m_all)
systTree.branchTreesSysts(trees, "all", "best_Wpjet_isbtag", outTreeFile, best_WpJet_isBTagged_all)
systTree.branchTreesSysts(trees, "all", "best_Wpjet_btagscore", outTreeFile, best_WpJet_btagscore_all)
systTree.branchTreesSysts(trees, "all", "lepton_pt", outTreeFile, lepton_pt_all)
systTree.branchTreesSysts(trees, "all", "lepton_eta", outTreeFile, lepton_eta_all)
systTree.branchTreesSysts(trees, "all", "lepton_phi", outTreeFile, lepton_phi_all)
systTree.branchTreesSysts(trees, "all", "lepton_miniIso", outTreeFile, lepton_miniIso_all)
systTree.branchTreesSysts(trees, "all", "lepton_stdIso", outTreeFile, lepton_stdIso_all)
systTree.branchTreesSysts(trees, "all", "lepMET_deltaphi", outTreeFile, lepMET_deltaPhi_all)
systTree.branchTreesSysts(trees, "all", "passed_mu", outTreeFile, passed_mu_all)
systTree.branchTreesSysts(trees, "all", "passed_ele", outTreeFile, passed_ele_all)
systTree.branchTreesSysts(trees, "all", "passed_ht", outTreeFile, passed_ht_all)
systTree.branchTreesSysts(trees, "all", "nPV_good", outTreeFile, nPV_good_all)
systTree.branchTreesSysts(trees, "all", "nPV_tot", outTreeFile, nPV_tot_all)
systTree.branchTreesSysts(trees, "all", "isEle", outTreeFile, isEle_all)
systTree.branchTreesSysts(trees, "all", "isMu", outTreeFile, isMu_all)
systTree.branchTreesSysts(trees, "all", "Event_HT", outTreeFile, Event_HT_all)
systTree.branchTreesSysts(trees, "all", "MET_pt", outTreeFile, MET_pt_all)
systTree.branchTreesSysts(trees, "all", "MET_phi", outTreeFile, MET_phi_all)
systTree.branchTreesSysts(trees, "all", "mtw", outTreeFile, mtw_all)
systTree.branchTreesSysts(trees, "all", "ptrel_leadAK4_closestAK8", outTreeFile, ptrel_leadAK4_closestAK8)
systTree.branchTreesSysts(trees, "all", "deltaR_leadAK4_closestAK8", outTreeFile, deltaR_leadAK4_closestAK8)
systTree.branchTreesSysts(trees, "all", "ptrel_subleadAK4_closestAK8", outTreeFile, ptrel_subleadAK4_closestAK8)
systTree.branchTreesSysts(trees, "all", "deltaR_subleadAK4_closestAK8", outTreeFile, deltaR_subleadAK4_closestAK8)
systTree.branchTreesSysts(trees, "all", "ptrel_besttopAK4_closestAK8", outTreeFile, ptrel_besttopAK4_closestAK8)
systTree.branchTreesSysts(trees, "all", "deltaR_besttopAK4_closestAK8", outTreeFile, deltaR_besttopAK4_closestAK8)
systTree.branchTreesSysts(trees, "all", "ptrel_chitopAK4_closestAK8", outTreeFile, ptrel_chitopAK4_closestAK8)
systTree.branchTreesSysts(trees, "all", "deltaR_chitopAK4_closestAK8", outTreeFile, deltaR_chitopAK4_closestAK8)
systTree.branchTreesSysts(trees, "all", "ptrel_bestWAK4_closestAK8", outTreeFile, ptrel_bestWAK4_closestAK8)
systTree.branchTreesSysts(trees, "all", "deltaR_bestWAK4_closestAK8", outTreeFile, deltaR_bestWAK4_closestAK8)
systTree.branchTreesSysts(trees, "all", "ptrel_chiWAK4_closestAK8", outTreeFile, ptrel_chiWAK4_closestAK8)
systTree.branchTreesSysts(trees, "all", "deltaR_chiWAK4_closestAK8", outTreeFile, deltaR_chiWAK4_closestAK8)
systTree.branchTreesSysts(trees, "all", "best_topW_jets_pt", outTreeFile, best_topW_jets_pt)
systTree.branchTreesSysts(trees, "all", "best_topW_jets_deltaR", outTreeFile, best_topW_jets_deltaR)
systTree.branchTreesSysts(trees, "all", "best_topW_jets_deltaPhi", outTreeFile, best_topW_jets_deltaphi)
systTree.branchTreesSysts(trees, "all", "chi_topW_jets_pt", outTreeFile, chi_topW_jets_pt)
systTree.branchTreesSysts(trees, "all", "chi_topW_jets_deltaR", outTreeFile, chi_topW_jets_deltaR)
systTree.branchTreesSysts(trees, "all", "chi_topW_jets_deltaPhi", outTreeFile, chi_topW_jets_deltaphi)

#Fat jet
systTree.branchTreesSysts(trees, "all", "topAK8_area", outTreeFile, topAK8_area)
systTree.branchTreesSysts(trees, "all", "topAK8_btag", outTreeFile, topAK8_btag)
systTree.branchTreesSysts(trees, "all", "topAK8_ttagMD", outTreeFile, topAK8_ttagMD)
systTree.branchTreesSysts(trees, "all", "topAK8_ttag", outTreeFile, topAK8_ttag)
systTree.branchTreesSysts(trees, "all", "topAK8_eta", outTreeFile, topAK8_eta)
systTree.branchTreesSysts(trees, "all", "topAK8_m", outTreeFile, topAK8_m)
systTree.branchTreesSysts(trees, "all", "topAK8_mSD", outTreeFile, topAK8_mSD)
systTree.branchTreesSysts(trees, "all", "topAK8_phi", outTreeFile, topAK8_phi)
systTree.branchTreesSysts(trees, "all", "topAK8_pt", outTreeFile, topAK8_pt)
systTree.branchTreesSysts(trees, "all", "topAK8_tau1", outTreeFile, topAK8_tau1)
systTree.branchTreesSysts(trees, "all", "topAK8_tau2", outTreeFile, topAK8_tau2)
systTree.branchTreesSysts(trees, "all", "topAK8_tau3", outTreeFile, topAK8_tau3)
systTree.branchTreesSysts(trees, "all", "topAK8_tau4", outTreeFile, topAK8_tau4)

systTree.branchTreesSysts(trees, "all", "WprAK8_area", outTreeFile, WprAK8_area)
systTree.branchTreesSysts(trees, "all", "WprAK8_btag", outTreeFile, WprAK8_btag)
systTree.branchTreesSysts(trees, "all", "WprAK8_ttagMD", outTreeFile, WprAK8_ttagMD)
systTree.branchTreesSysts(trees, "all", "WprAK8_ttag", outTreeFile, WprAK8_ttag)
systTree.branchTreesSysts(trees, "all", "WprAK8_eta", outTreeFile, WprAK8_eta)
systTree.branchTreesSysts(trees, "all", "WprAK8_m", outTreeFile, WprAK8_m)
systTree.branchTreesSysts(trees, "all", "WprAK8_mSD", outTreeFile, WprAK8_mSD)
systTree.branchTreesSysts(trees, "all", "WprAK8_phi", outTreeFile, WprAK8_phi)
systTree.branchTreesSysts(trees, "all", "WprAK8_pt", outTreeFile, WprAK8_pt)
systTree.branchTreesSysts(trees, "all", "WprAK8_tau1", outTreeFile, WprAK8_tau1)
systTree.branchTreesSysts(trees, "all", "WprAK8_tau2", outTreeFile, WprAK8_tau2)
systTree.branchTreesSysts(trees, "all", "WprAK8_tau3", outTreeFile, WprAK8_tau3)
systTree.branchTreesSysts(trees, "all", "WprAK8_tau4", outTreeFile, WprAK8_tau4)

if(TriggerStudy):
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
print("Is MC: " + str(isMC) + "      option addPDF: " + str(addPDF))
if(isMC and addPDF):
    systTree.branchTreesSysts(trees, "all", "w_PDF", outTreeFile, w_PDF_all)
if('TT_' in sample.label): 
    systTree.branchTreesSysts(trees, "all", "nlep", outTreeFile, nlep_all)
####################################################################################################################################################################################################################################

#++++++++++++++++++++++++++++++++++
#++      taking MC weights       ++
#++++++++++++++++++++++++++++++++++
#print("isMC: ", isMC)
if(isMC):
    h_genweight = ROOT.TH1F()
    h_genweight.SetNameTitle('h_genweight', 'h_genweight')
    h_PDFweight = ROOT.TH1F()
    h_PDFweight.SetNameTitle("h_PDFweight","h_PDFweight")
    print(file_list)
    print("loop #3 over file_list")
    for infile in file_list: 
        if Debug:
            print(infile)
            print("entered file_list loop #3")    
            print("Getting the histos from %s" %(infile))
        newfile = ROOT.TFile.Open(infile)
        dirc = ROOT.TDirectory()
        dirc = newfile.Get("plots")
        #h_genw_tmp = ROOT.TH1F(newfile.Get("plots/h_genweight"))
        h_genw_tmp = ROOT.TH1F(dirc.Get("h_genweight"))
        if Debug:
            print("in newfile: ")
            dirc.Get("h_genweight").Print()
            print("in macro: ")
            h_genw_tmp.Print()
        
        if(dirc.GetListOfKeys().Contains("h_PDFweight")):
            #h_pdfw_tmp = ROOT.TH1F(newfile.Get("plots/h_PDFweight"))
            h_pdfw_tmp = ROOT.TH1F(dirc.Get("h_PDFweight"))
            print("in newfile: ")
            dirc.Get("h_PDFweight").Print()
            print("in macro: ")
            h_pdfw_tmp.Print()

            if(ROOT.TH1F(h_PDFweight).Integral() < 1.):
                h_PDFweight.SetBins(h_pdfw_tmp.GetXaxis().GetNbins(), h_pdfw_tmp.GetXaxis().GetXmin(), h_pdfw_tmp.GetXaxis().GetXmax())
                print("h_genweight first bin content is %f and h_PDFweight has %f bins" %(ROOT.TH1F(dirc.Get("h_genweight")).GetBinContent(1), ROOT.TH1F(dirc.Get("h_PDFweight")).GetNbinsX()))
            h_PDFweight.Add(h_pdfw_tmp)
        else:
            addPDF = False
        if(ROOT.TH1F(h_genweight).Integral() < 1.):
            h_genweight.SetBins(h_genw_tmp.GetXaxis().GetNbins(), h_genw_tmp.GetXaxis().GetXmin(), h_genw_tmp.GetXaxis().GetXmax())
        h_genweight.Add(h_genw_tmp)
    print("h_genweight first bin content is %f and h_PDFweight has %f bins" %(h_genweight.GetBinContent(1), h_PDFweight.GetNbinsX()))


#++++++++++++++++++++++++++++++++++
#++      Efficiency studies      ++
#++++++++++++++++++++++++++++++++++


print("Total number of events: ", tree.GetEntries())

neutrino_failed = 0
nrecochi = 0
nrecoclosest = 0
nrecosublead = 0
nrecobest = 0
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
        print("evento n. " + str(i))
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
    genpart = None
    
    h_eff_mu.Fill('Total', 1)
    h_eff_ele.Fill('Total', 1)
    if isMC:
        genpart = Collection(event, "GenPart")
        LHE = Collection(event, "LHEPart")
        chain.GetEntry(i)
    #++++++++++++++++++++++++++++++++++
    #++      defining variables      ++
    #++++++++++++++++++++++++++++++++++
    tightlep = None
    tightlep_p4 = None
    tightlep_p4t = None
    tightlep_SF = None
    tightlep_SFUp = None
    tightlep_SFDown = None
    recomet_p4t = None
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
    passMu, passEle, passHT, noTrigger = trig_map(HLT, year, runPeriod)
    passed_mu_all[0] = int(passMu)
    passed_ele_all[0] = int(passEle)
    passed_ht_all[0] = int(passHT)
    isDilepton = False
    isMuon = (len(goodMu) == 1) and (len(goodEle) == 0) and len(VetoMu) == 0 and len(VetoEle) == 0 and (passMu or passHT)
    isElectron = (len(goodMu) == 0) and (len(goodEle) == 1) and len(VetoMu) == 0 and len(VetoEle) == 0 and (passEle or passHT)

    #Double counting removal
    if('DataHT' in sample.label and (passMu or passEle)):
        continue
    if('DataEle' in sample.label and (passMu or not passEle)):
        continue
    if('DataMu' in sample.label and (passEle or not passMu)):
        continue

    if len(goodMu) == 1:
        h_eff_mu.Fill('Good Mu', 1)
        if len(goodEle) == 0:
            h_eff_mu.Fill('Good Ele', 1)
        if len(VetoMu) == 0:
            h_eff_mu.Fill('Veto Mu', 1)
        if len(VetoEle) == 0:
            h_eff_mu.Fill('Veto Ele', 1)
    if len(goodEle) == 1:
        h_eff_ele.Fill('Good Ele', 1)
        if len(goodMu) == 0:
            h_eff_ele.Fill('Good Mu', 1)
        if len(VetoMu) == 0:
            h_eff_ele.Fill('Veto Mu', 1)
        if len(VetoEle) == 0:
            h_eff_ele.Fill('Veto Ele', 1)

    ######################################
    ## Selecting only jets with pt>100  ##
    ######################################
    btagreco = False
    goodJets = get_Jet(jets, 100)
    bjets, nobjets = bjet_filter(goodJets, 'DeepFlv', 'M')
    if(len(bjets) > 1):
        btagreco = True
    nJet_pt100_all[0] = len(goodJets)
    nbJet_pt100_all[0] = len(bjets)
    if Debug:
        print("len bjets: ", len(bjets), "nbJet_pt100_all: ", nbJet_pt100_all[0])
    nfatJet_all[0] = len(fatjets)
    nJet_lowpt_all[0] = len(jets) - len(goodJets)
    nbJet_lowpt_all[0] = len(bjet_filter(jets, 'DeepFlv', 'M')[0]) - len(bjets)
    #print(len(fatjets))
    #++++++++++++++++++++++++++++++++++
    #++    plots for lep-jet dis     ++
    #++++++++++++++++++++++++++++++++++
    #lepjet,drmin = closest(tightlep, get_Jet(jets, 15))
    #ptrel = get_ptrel(tightlep, lepjet)
    #if(isMuon):
    #    h_drmin_ptrel_mu.Fill(drmin,ptrel)
    if(len(goodJets) >= 2):
        if isMuon:
            h_eff_mu.Fill('good jets >2', int(isMuon))
        elif isElectron:
            h_eff_ele.Fill('good jets >2', int(isElectron))
    if(len(fatjets) >= 2):
        if isMuon:
            h_eff_mu.Fill('fat jets >2', int(isMuon))
        elif isElectron:
            h_eff_ele.Fill('fat jets >2', int(isElectron))

    if (len(goodJets) < 2 or len(fatjets) < 2):
        continue

    if isMuon:
        h_eff_mu.Fill('passMu+jetsel', int(isMuon))
    elif isElectron:
        h_eff_ele.Fill('passEle+jetsel', int(isElectron))

    if(TriggerStudy):
        isdileptonic[0] = 0
        isDilepton = (len(goodMu) == 1) and (len(goodEle) == 1) and len(VetoMu) == 0 and len(VetoEle) == 0 and (passMu or passHT or passEle)
    if(isMuon):
        isEle_all[0] = 0
        isMu_all[0] = 1
        tightlep = goodMu[0]
        tightlep_p4 = copy.deepcopy(tightlep.p4())#ROOT.TLorentzVector()
        #tightlep_p4.SetPtEtaPhiM(goodMu[0].pt,goodMu[0].eta,goodMu[0].phi,goodMu[0].mass)
        tightlep_p4t = copy.deepcopy(tightlep.p4())
        tightlep_p4t.SetPz(0.)
        if(isMC):
            tightlep_SF = goodMu[0].effSF
            tightlep_SFUp = goodMu[0].effSF_errUp
            tightlep_SFDown = goodMu[0].effSF_errDown
            systTree.setWeightName("lepSF", copy.deepcopy(tightlep_SF))
            systTree.setWeightName("lepUp", copy.deepcopy(tightlep_SFUp))
            systTree.setWeightName("lepDown", copy.deepcopy(tightlep_SFDown))
    elif(isElectron):
        isEle_all[0] = 1
        isMu_all[0] = 0
        tightlep = goodEle[0]
        tightlep_p4 = ROOT.TLorentzVector()
        tightlep_p4.SetPtEtaPhiM(goodEle[0].pt,goodEle[0].eta,goodEle[0].phi,goodEle[0].mass)
        tightlep_p4t = copy.deepcopy(tightlep.p4())
        tightlep_p4t.SetPz(0.)
        if(isMC):
            tightlep_SF = goodEle[0].effSF
            tightlep_SFUp = goodEle[0].effSF_errUp
            tightlep_SFDown = goodEle[0].effSF_errDown
            systTree.setWeightName("lepSF", copy.deepcopy(tightlep_SF))
            systTree.setWeightName("lepUp", copy.deepcopy(tightlep_SFUp))
            systTree.setWeightName("lepDown", copy.deepcopy(tightlep_SFDown))
    elif(isDilepton and TriggerStudy):
        muon_pt[0] = goodMu[0].pt
        muon_eta[0] = goodMu[0].eta
        muon_phi[0] = goodMu[0].phi
        muon_SF[0] = goodMu[0].effSF
        electron_pt[0] = goodEle[0].pt
        electron_eta[0] = goodEle[0].eta
        electron_phi[0] = goodEle[0].phi
        electron_m[0] = goodEle[0].mass
        electron_SF[0] = goodEle[0].effSF
        isdileptonic[0] = 1
    else:
        #print('Event %i not a good' %(i))
        continue

    recotop = TopUtilities()
    #veto on events with "pathological" reco neutrino
    tent_neutrino = recotop.NuMomentum(tightlep.p4().Px(), tightlep.p4().Py(), tightlep.p4().Pz(), tightlep.p4().Pt(), tightlep.p4().E(), MET['metPx'], MET['metPy'])
    #print(" <<<<<<<<<<<<<<<<<<<<<<<< lepton is %f " %tightlep.p4().M())
    if tent_neutrino[0] == None:
        neutrino_failed += 1
        continue

    if(isMC):
        PF_SF = chain.PrefireWeight
        PF_SFUp = chain.PrefireWeight_Up
        PF_SFDown = chain.PrefireWeight_Down
        systTree.setWeightName("PFSF", copy.deepcopy(PF_SF))
        systTree.setWeightName("PFUp", copy.deepcopy(PF_SFUp))
        systTree.setWeightName("PFDown", copy.deepcopy(PF_SFDown))

        '''
        PU_SF = chain.PrefireWeight
        PU_SFUp = chain.PrefireWeight_Up
        PU_SFDown = chain.PrefireWeight_Down
        systTree.setWeightName("PUSF", copy.deepcopy(PU_SF))
        systTree.setWeightName("puUp", copy.deepcopy(PU_SFUp))
        systTree.setWeightName("puDown", copy.deepcopy(PU_SFDown))
        '''

    recomet_p4t = ROOT.TLorentzVector()
    recomet_p4t.SetPtEtaPhiM(met.pt, 0., met.phi, 0)

    nPV_good_all[0] = PV.npvsGood
    nPV_tot_all[0] = PV.npvs

    if tightlep != None:
        #print("ev #", i, ": tightlep exists")
        lepton_pt_all[0] = tightlep_p4.Pt()
        lepton_eta_all[0] = tightlep_p4.Eta()
        lepton_phi_all[0] = tightlep_p4.Phi()
        lepton_miniIso_all[0] = tightlep.miniPFRelIso_all
        if(isMuon):
            lepton_stdIso_all[0] = tightlep.pfIsoId
        MET_pt_all[0] = met.pt
        MET_phi_all[0] = met.phi
        Event_HT_all[0] = HT.eventHT

    else:
        lepton_pt_all[0] = -100.
        lepton_eta_all[0] = -100.
        lepton_phi_all[0] = -100.
        lepton_miniIso_all[0] = -100.
        MET_pt_all[0] = -100.
        MET_phi_all[0] = -100.
        Event_HT_all[0] = -100.

    # requiring mtt < 700 to merge inclusive tt with the mtt > 700
    if('TT_incl' in sample.label):
        top_q4 = ROOT.TLorentzVector()  
        antitop_q4 = ROOT.TLorentzVector()  
        tt_q4 = ROOT.TLorentzVector()  
        for genp in genpart:
            if(genp.genPartIdxMother == 0 and genp.pdgId == 6):
                top_q4.SetPtEtaPhiM(genp.pt, genp.eta, genp.phi, genp.mass)
            elif(genp.genPartIdxMother == 0 and genp.pdgId == -6):
                antitop_q4.SetPtEtaPhiM(genp.pt, genp.eta, genp.phi, genp.mass)
        tt_q4 = top_q4 + antitop_q4
        #mtt[0] = tt_q4.M()
        if(tt_q4.M() > 700.):
            w_nominal_all[0] *= 0 #trick to make the events with mtt > 700 count zero
        else:
            w_nominal_all[0] = 1.

    # trying to understand the composition of the ttbar background
    if('TT_' in sample.label):
        lhe_ele = 0
        lhe_mu = 0
        lhe_tau = 0
        nlep_all[0] = 0
        for lhep in LHE:
            if(abs(lhep.pdgId) == 11):
                lhe_ele += 1
            elif(abs(lhep.pdgId) == 13):
                lhe_mu += 1
            elif(abs(lhep.pdgId) == 15):
               for genp in genpart:
                   #print("pdg id " + str(genp.pdgId) + " and mother is " + str(genp.genPartIdxMother))
                   if((abs(genp.pdgId) == 11 or abs(genp.pdgId) == 13) and genp.genPartIdxMother > 0):
                       #print(" with pdg id " + str(genpart[int(genp.genPartIdxMother)].pdgId))
                       abs(genpart[genp.genPartIdxMother].pdgId) == 15
                       lhe_tau += 1 #inventare un modo per contare eventi leptonici da tau
        nlep_all[0] = lhe_ele + lhe_mu + lhe_tau

    # checking the top 4-vector at LHE level 
    if Debug:
        for genp in genpart:
            if(abs(genp.pdgId) == 6):
                top_q4 = ROOT.TLorentzVector()
                top_q4.SetPtEtaPhiM(genp.pt, genp.eta, genp.phi, genp.mass)
                #print( " top 4-vector at GEN level is (%f, %f, %f, %f) and mass %f "%(genp.pt, genp.eta, genp.phi, top_q4.E(), top_q4.M()))

    lepMET_deltaPhi_all[0] = deltaPhi(tightlep_p4.Phi(), met.phi)
    mtw_all[0] = math.sqrt(2*tightlep_p4.Pt() * met.pt *(1-math.cos(abs(deltaPhi(tightlep_p4.Phi(), met.phi)))))

    mcbjets = None
    mclepton = None

    if(len(bjets) >= 2):
        bjets_deltaR[0] = deltaR(bjets[0].eta, bjets[0].phi, bjets[1].eta, bjets[1].phi)
        bjets_deltaPhi[0] = deltaPhi(bjets[0].phi, bjets[1].phi)
        bjets_deltaEta[0] = bjets[0].eta - bjets[1].eta
        leadingbjet_p4 = ROOT.TLorentzVector()
        subleadingbjet_p4 = ROOT.TLorentzVector()
        leadingbjet_p4.SetPtEtaPhiM(bjets[0].pt, bjets[0].eta, bjets[0].phi, bjets[0].mass)
        subleadingbjet_p4.SetPtEtaPhiM(bjets[1].pt, bjets[1].eta, bjets[1].phi, bjets[1].mass)
        bjets_pt[0] = (leadingbjet_p4 + subleadingbjet_p4).Pt()
    else:
        bjets_deltaR[0] = -999.
        bjets_deltaPhi[0] = -999.
        bjets_deltaEta[0] = -999.
        bjets_pt[0] = -999.

    #MCtruth event reconstruction
    if MCReco:

        #GenParticles
        gentopFound = False
        genbottFound = False
        gentop_p4 = ROOT.TLorentzVector()
        genbott_p4 = ROOT.TLorentzVector()
        for genp in genpart:
            if gentopFound == True and genbottFound == True:
                break
            if genp.genPartIdxMother == 0:
                if abs(genp.pdgId) == 6 and gentopFound == False:
                    gentop_p4.SetPtEtaPhiM(genp.pt, genp.eta, genp.phi, genp.mass)
                    if Debug:
                        print( "top genp: ", genp.pt, genp.phi, genp.eta, genp.mass, genp.pdgId)
                        print( "(loop) gentop: ", gentop_p4.Pt(), gentop_p4.Phi(), gentop_p4.Eta(), gentop_p4.M())
                    gentopFound = True
                elif abs(genp.pdgId) == 5 and genbottFound == False:
                    genbott_p4.SetPtEtaPhiM(genp.pt, genp.eta, genp.phi, genp.mass)
                    if Debug:
                        print( "bott genp: ", genp.pt, genp.phi, genp.eta, genp.mass, genp.pdgId)
                        print( "(loop) genbott: ", genbott_p4.Pt(), genbott_p4.Phi(), genbott_p4.Eta(), genbott_p4.M())
                    genbottFound = True
            else:
                continue
        
        #print gentop, genbott
        if gentopFound and genbottFound:
            genWprime_p4 = gentop_p4 + genbott_p4
            GenPart_Wprime_m_all[0] = genWprime_p4.M()
            GenPart_Wprime_mt_all[0] = genWprime_p4.Mt()
            GenPart_Wprime_pt_all[0] = genWprime_p4.Pt()
            GenPart_Wprime_eta_all[0] = genWprime_p4.Eta()
            GenPart_Wprime_phi_all[0] = genWprime_p4.Phi()
            GenPart_Top_m_all[0] = gentop_p4.M()
            GenPart_Top_mt_all[0] = gentop_p4.Mt()
            GenPart_Top_pt_all[0] = gentop_p4.Pt()
            GenPart_Top_eta_all[0] = gentop_p4.Eta()
            GenPart_Top_phi_all[0] = gentop_p4.Phi()
            GenPart_Bottom_m_all[0] = genbott_p4.M()
            GenPart_Bottom_pt_all[0] = genbott_p4.Pt()
            GenPart_Bottom_eta_all[0] = genbott_p4.Eta()
            GenPart_Bottom_phi_all[0] = genbott_p4.Phi()
        else:
            GenPart_Wprime_m_all[0] = -100.
            GenPart_Wprime_mt_all[0] = -100.
            GenPart_Wprime_pt_all[0] = -100.
            GenPart_Wprime_eta_all[0] = -100.
            GenPart_Wprime_phi_all[0] = -100.
            GenPart_Top_m_all[0] = -100.
            GenPart_Top_mt_all[0] = -100.
            GenPart_Top_pt_all[0] = -100.
            GenPart_Top_eta_all[0] = -100.
            GenPart_Top_phi_all[0] = -100.
            GenPart_Bottom_m_all[0] = -100.
            GenPart_Bottom_pt_all[0] = -100.
            GenPart_Bottom_eta_all[0] = -100.
            GenPart_Bottom_phi_all[0] = -100.
        
        mcbjets = mcbjet_filter(jets)
        mctfound = False
        if isMuon:
            for muon in goodMu:
                if (muon.genPartFlav == 1 or muon.genPartFlav == 15) and not mctfound:
                    mclepton = muon
                    mctfound = True
                    if mclepton.genPartIdx == -1 and Debug:
                        print( 'MCTruth reconstruction not properly working - lepton step')
        elif isElectron:
            for ele in goodEle:
                if (ele.genPartFlav == 1 or ele.genPartFlav == 15) and not mctfound:
                    mclepton = ele
                    mctfound = True
                    if mclepton.genPartIdx == -1 and Debug:
                        print( 'MCTruth reconstruction not properly working - lepton step')
        else:
            mclepton = None

        mctop_p4 = None
        mctop_p4t = None
        IsmcNeg = False
        mcdR_lepjet = None
        Mcpromptbjet_p4 = None
        mctopbjet_p4 = None
        mctopbjet_p4_pre = None
        mcpromptbjet_p4t = None
        bjetcheck = True
        topgot_ak4 = False
        Wpgot_ak4 = False

        if mclepton != None:
            mcbjets = mcbjet_filter(jets)
            
            if len(mcbjets)>2:
                bjetcheck = False

            mcWprime_p4 = ROOT.TLorentzVector()
            mcWprime_p4t = ROOT.TLorentzVector()
            mclepton_p4 = ROOT.TLorentzVector()
            mclepton_p4.SetPtEtaPhiM(mclepton.pt, mclepton.eta, mclepton.phi, mclepton.mass)
            bottjets = sameflav_filter(mcbjets, 5)
            abottjets = sameflav_filter(mcbjets, -5)
            
            for bjet in mcbjets:
                bjet_p4 = ROOT.TLorentzVector()
                bjet_p4.SetPtEtaPhiM(bjet.pt, bjet.eta, bjet.phi, bjet.mass)

                if abs(bjet.partonFlavour)!=5:
                    print( 'bfilter not properly working')
                    continue

                blepflav = genpart[mclepton.genPartIdx].pdgId*bjet.partonFlavour

                if bjet.hadronFlavour == 5:
                    if blepflav < 0 and not topgot_ak4:
                        mctopbjet_p4_pre = copy.deepcopy(bjet_p4)
                        '''
                        if deltaR(bjet_p4.Eta(), bjet_p4.Phi(), mclepton_p4.Eta(), mclepton_p4.Phi()) < 0.4:
                        bjet_p4 -= mclepton_p4
                        '''

                        mctopbjet_p4 = bjet_p4
                        mctop_p4, IsmcNeg, mcdR_lepjet = recotop.top4Momentum(mclepton_p4, bjet_p4, MET['metPx'], MET['metPy'])
                        IsmcNeg = IsmcNeg*DeltaFilter
                        #print( "MC top mass is %f " %mctop_p4.M())
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

        if topgot_ak4 and Wpgot_ak4 and mclepton != None:
            mcWprime_p4 = mctop_p4 + mcpromptbjet_p4
            mcWprime_p4t = mctop_p4t + mcpromptbjet_p4t
            mcChi2_topmass = Chi_TopMass(mctop_p4.M())
            MC_Wprime_m_all[0] = mcWprime_p4.M()
            MC_Wprime_m_all[0] = mcWprime_p4.M()
            MC_Wprime_mt_all[0] = mcWprime_p4t.M()
            MC_Wprime_pt_all[0] = mcWprime_p4.Pt()
            MC_Wprime_eta_all[0] = mcWprime_p4.Eta()
            MC_Wprime_phi_all[0] = mcWprime_p4.Phi()
            MC_RecoTop_m_all[0] = mctop_p4.M()
            MC_RecoTop_mt_all[0] = mctop_p4t.M()
            MC_RecoTop_pt_all[0] = mctop_p4.Pt()
            MC_RecoTop_eta_all[0] = mctop_p4.Eta()
            MC_RecoTop_phi_all[0] = mctop_p4.Phi()
            MC_RecoTop_isNeg_all[0] = int(IsmcNeg)
            MC_TopJet_m_all[0] = mctopbjet_p4.M()
            MC_TopJet_pt_all[0] = mctopbjet_p4.Pt()
            MC_TopJet_eta_all[0] = mctopbjet_p4.Eta()
            MC_TopJet_phi_all[0] = mctopbjet_p4.Phi()
            MC_TopJet_dRLepJet_all[0] = copy.deepcopy(mcdR_lepjet)
            MC_WpJet_m_all[0] = mcpromptbjet_p4.M()
            MC_WpJet_pt_all[0] = mcpromptbjet_p4.Pt()
            MC_WpJet_eta_all[0] = mcpromptbjet_p4.Eta()
            MC_WpJet_phi_all[0] = mcpromptbjet_p4.Phi()
        else:
            MC_Wprime_m_all[0] = -100.
            MC_Wprime_mt_all[0] = -100.
            MC_Wprime_pt_all[0] = -100.
            MC_Wprime_eta_all[0] = -100.
            MC_Wprime_phi_all[0] = -100.
            MC_RecoTop_m_all[0] = -100.
            MC_RecoTop_mt_all[0] = -100.
            MC_RecoTop_pt_all[0] = -100.
            MC_RecoTop_eta_all[0] = -100.
            MC_RecoTop_phi_all[0] = -100.
            MC_RecoTop_isNeg_all[0] = -1
            MC_TopJet_m_all[0] = -100.
            MC_TopJet_pt_all[0] = -100.
            MC_TopJet_eta_all[0] = -100.
            MC_TopJet_phi_all[0] = -100.
            MC_TopJet_dRLepJet_all[0] = -100.
            MC_WpJet_m_all[0] = -100.
            MC_WpJet_pt_all[0] = -100.
            MC_WpJet_eta_all[0] = -100.
            MC_WpJet_phi_all[0] = -100.

    #DetReco(nstruction)
    if tightlep != None:
        ovrthrust, hadthrust = event_thrust(tightlep, jets, met)
        ovr_global_thrust[0] = copy.deepcopy(ovrthrust)
        ovr_central_thrust[0] = copy.deepcopy(round((1. - ovrthrust), 5))
        had_global_thrust[0] = copy.deepcopy(hadthrust)
        had_central_thrust[0] = copy.deepcopy(round((1. - hadthrust), 5))
        closj, dR_lj = closest(tightlep, goodJets)
        deltaR_lep_closestjet[0] = copy.deepcopy(dR_lj)

    closAK8, dR_leadAK4AK8 = closest(jets[0], fatjets)
    ptrel_leadAK4_closestAK8[0] = goodJets[0].pt/closAK8.pt
    deltaR_leadAK4_closestAK8[0] = copy.deepcopy(dR_leadAK4AK8)
    subclosAK8, dR_subleadAK4AK8 = closest(jets[1], fatjets)
    ptrel_subleadAK4_closestAK8[0] = goodJets[1].pt/subclosAK8.pt
    deltaR_subleadAK4_closestAK8[0] = copy.deepcopy(dR_subleadAK4AK8)
    leadingjet_pt_all[0] = jets[0].pt
    subleadingjet_pt_all[0] = jets[1].pt
    leadingbjet_pt_all[0] = 0.
    subleadingbjet_pt_all[0] = 0.
    
    if len(bjets) != 0:
        leadingbjet_pt_all[0] = bjets[0].pt
    if len(bjets) > 1:
        subleadingbjet_pt_all[0] = bjets[1].pt

    leadingjets_deltaR[0] = deltaR(jets[0].eta, jets[0].phi, jets[1].eta, jets[1].phi)
    leadingjets_deltaPhi[0] = deltaPhi(jets[0].phi, jets[1].phi)
    leadingjets_deltaEta[0] = jets[0].eta - jets[1].eta
    leadingjet_p4 = ROOT.TLorentzVector()
    subleadingjet_p4 = ROOT.TLorentzVector()
    leadingjet_p4.SetPtEtaPhiM(jets[0].pt, jets[0].eta, jets[0].phi, jets[0].mass)
    subleadingjet_p4.SetPtEtaPhiM(jets[1].pt, jets[1].eta, jets[1].phi, jets[1].mass)
    leadingjets_pt[0] = (leadingjet_p4 + subleadingjet_p4).Pt()
    deltaR_lep_leadingjet[0] = copy.deepcopy(deltaR(tightlep, jets[0]))
    deltaR_lep_subleadingjet[0] = copy.deepcopy(deltaR(tightlep, jets[1]))

    highptJets = get_Jet(goodJets, leadingjet_ptcut)
    if len(highptJets) < 1:
        continue

    if btagreco:
        goodJets = copy.copy(bjets)
        highptJets = get_Jet(goodJets, leadingjet_ptcut)

    closest_promptjet = None
    closest_promptjet_p4t = None
    closest_jet_p4 = None
    closest_jet_p4t = None
    closest_jet_p4_pre = None
    closest_dR_lepjet = None
    chi_promptjet = None
    chi_promptjet_p4t = None
    chi_jet_p4 = None
    chi_jet_p4t = None
    chi_jet_p4_pre = None
    chi_dR_lepjet = None
    sublead_promptjet = goodJets[0]
    sublead_promptjet_p4t = None
    sublead_jet_p4 = None
    sublead_jet_p4t = None
    sublead_jet_p4_pre = None
    sublead_dR_lepjet = None
    best_promptjet = None
    best_promptjet_p4t = None
    best_jet_p4 = None
    best_jet_p4t = None
    best_dR_lepjet = None
    DeltaR_nujet = 100.
    DeltaR_Idx = 0
    tm_chi = 1000000.
    tm_Idx = 0
    mtop_p4 = None

    btag_countings_sublead = 0
    btag_countings_closest = 0
    btag_countings_chi = 0
    btag_countings_best = 0

    #dR_lepjet = []
    #jet reconstructing top with the smallest chi2 p4                                

    for k in range(len(goodJets)):
        temp_dR = None
        mtop_p4, isdetrecoNeg, temp_dR = recotop.top4Momentum(tightlep.p4(), goodJets[k].p4(), MET['metPx'], MET['metPy'])
        #dR_lepjet.append(copy.deepcopy(temp_dR))
        if mtop_p4 is None:
            continue
        chi = Chi_TopMass(mtop_p4.M())
        if chi < tm_chi:
            tm_chi = chi
            tm_Idx = k
    
    chi_jet_p4_pre = copy.deepcopy(goodJets[tm_Idx].p4())
    chi_jet = goodJets[tm_Idx]
   
    chi_jet_p4 = chi_jet_p4_pre
    if tm_Idx == 0:
        if len(highptJets) > 1:
            chi_promptjet = highptJets[1]
        else:
            chi_promptjet = goodJets[1]
    else:
        chi_promptjet = goodJets[0]

    #Switching jets if Wpjet is btagged and topbjet isn't    
    #bjet_p4 = ROOT.TLorentzVector()
    #nobjet_p4 = ROOT.TLorentzVector()
    bjet = None
    nobjet = None
    is_chi_topjet_btag = None
    is_chi_Wpjet_btag = None
    
    is_chi_topjet_btag = int(len(bjet_filter([chi_jet], 'DeepFlv', 'M')[0]))
    is_chi_Wpjet_btag = int(len(bjet_filter([chi_promptjet], 'DeepFlv', 'M')[0]))
    if is_chi_topjet_btag == 0 and is_chi_Wpjet_btag == 1 and bjetSwitch:
        #print("is topjet btag: ", is_chi_topjet_btag, "is Wpjet btag: ", is_chi_Wpjet_btag)
        #print("chi_topjet: ", chi_jet, "chi_promptjet", chi_promptjet)
        bjet = copy.copy(chi_promptjet)
        nobjet = copy.copy(chi_jet)
        #bjet_p4 = chi_promptjet.p4()
        #nobjet_p4 = chi_jet.p4()
        #chi_jet_p4 = copy.deepcopy(bjet_p4)
        #chi_promptjet_p4 = copy.deepcopy(nobjet_p4)
        #print("bjet: ", bjet, "nobjet: ", nobjet)
        #print(chi_jet_p4.Print())
        #print(chi_promptjet.p4().Print())
        chi_jet = copy.copy(bjet)
        chi_promptjet = copy.copy(nobjet)
        #print("chi_topjet: ", chi_jet, "chi_promptjet", chi_promptjet)
        #print("bjet: ", bjet, "nobjet: ", nobjet)
        chi_jet_p4 = chi_jet.p4()
        chi_promptjet_p4 = chi_promptjet.p4()
        #print(chi_jet_p4.Print())
        #print(chi_promptjet_p4.Print())

    ## Chi top reconstruction
    chi_recotop_p4, IsNeg_chi, chi_dR_lepjet = recotop.top4Momentum(tightlep.p4(), chi_jet_p4, MET['metPx'], MET['metPy'])
    IsNeg_chi = IsNeg_chi * DeltaFilter
    #btag_countings_chi = len(bjet_filter([chi_promptjet, chi_jet], 'DeepFlv', 'M')[0])
    closAK8, dR_besttopAK4AK8 = closest(chi_jet, fatjets)
    ptrel_chitopAK4_closestAK8[0] = chi_jet.pt/closAK8.pt
    deltaR_chitopAK4_closestAK8[0] = copy.deepcopy(dR_besttopAK4AK8)

    chi_jet_p4t = copy.deepcopy(chi_jet_p4)
    chi_jet_p4t.SetPz(0.)
    chi_recotop_p4t = tightlep_p4t + chi_jet_p4t + recomet_p4t
    chi_promptjet_p4t = copy.deepcopy(chi_promptjet.p4())
    chi_promptjet_p4t.SetPz(0.)
    if Debug:
        print( "  Is Neg chi " + str(IsNeg_chi) )
        print( " ================= lep 4-vector is (%f, %f, %f ,%f) " %(tightlep.p4().Pt(), tightlep.p4().Eta(), tightlep.p4().Phi(), tightlep.p4().E() ))
        print( " ================= chi jet 4-vector is (%f, %f, %f ,%f) " %(chi_jet_p4.Pt(), chi_jet_p4.Eta(), chi_jet_p4.Phi(), chi_jet_p4.E() ))
        print( " ================= chi top 4-vector is (%f, %f, %f ,%f) " %(chi_recotop_p4.Pt(), chi_recotop_p4.Eta(), chi_recotop_p4.Phi(), chi_recotop_p4.E() ))
        print( " ================= MET vector is (%f, %f) " %(MET['metPx'], MET['metPy']))
        print( " ================= Chi top mass is %f " %chi_recotop_p4.M())
    if chi_recotop_p4 != None:
        nrecochi += 1
        chi_RecoTop_costheta_all[0] = recotop.costhetapol(tightlep.p4(), chi_promptjet.p4(), chi_recotop_p4) 
        chi_RecoTop_costhetalep_all[0] = recotop.costhetapollep(tightlep.p4(), chi_recotop_p4) 

    #jet closest to MET p4                                                              
    closest_jet, detrecodR = closest(tightlep, goodJets)
    closest_jet_p4_pre = copy.deepcopy(closest_jet.p4())
    closest_jet_p4 = closest_jet_p4_pre
    
    if closest_jet == goodJets[0]:
        if len(highptJets) > 1:
            closest_promptjet = highptJets[1]
        else:
            closest_promptjet = goodJets[1]
    else:
        closest_promptjet = goodJets[0]

    
    #Switching jets if Wpjet is btagged and topbjet isn't
    bjet = None
    nobjet = None
    is_closest_topjet_btag = None
    is_closest_Wpjet_btag = None

    is_closest_topjet_btag = int(len(bjet_filter([closest_jet], 'DeepFlv', 'M')[0]))
    is_closest_Wpjet_btag = int(len(bjet_filter([closest_promptjet], 'DeepFlv', 'M')[0]))
    if is_closest_topjet_btag == 0 and is_closest_Wpjet_btag == 1 and bjetSwitch:
        #print("is topjet btag: ", is_closest_topjet_btag, "is Wpjet btag: ", is_closest_Wpjet_btag)
        #print("closest_topjet: ", closest_jet, "closest_promptjet", closest_promptjet)
        bjet = copy.copy(closest_promptjet)
        nobjet = copy.copy(closest_jet)
        #bjet_p4 = closest_promptjet.p4()
        #nobjet_p4 = closest_jet.p4()
        #closest_jet_p4 = copy.deepcopy(bjet_p4)
        #closest_promptjet_p4 = copy.deepcopy(nobjet_p4)
        #print("bjet: ", bjet, "nobjet: ", nobjet)
        #print(closest_jet_p4.Print())
        #print(closest_promptjet.p4().Print())
        closest_jet = copy.copy(bjet)
        closest_promptjet = copy.copy(nobjet)
        #print("closest_topjet: ", closest_jet, "closest_promptjet", closest_promptjet)
        #print("bjet: ", bjet, "nobjet: ", nobjet)
        closest_jet_p4 = closest_jet.p4()
        closest_promptjet_p4 = closest_promptjet.p4()
        #print(closest_jet_p4.Print())
        #print(closest_promptjet_p4.Print())
    
    ## Closest top reconstruction
    closest_recotop_p4, IsNeg_closest, closest_dR_lepjet = recotop.top4Momentum(tightlep.p4(), closest_jet_p4, MET['metPx'], MET['metPy'])
    IsNeg_closest = IsNeg_closest * DeltaFilter
    btag_countings_closest = len(bjet_filter([closest_promptjet, closest_jet], 'DeepFlv', 'M')[0])
    closest_jet_p4t = copy.deepcopy(closest_jet_p4)
    closest_jet_p4t.SetPz(0.)
    closest_recotop_p4t = tightlep_p4t + closest_jet_p4t + recomet_p4t
    closest_promptjet_p4t = copy.deepcopy(closest_promptjet.p4())
    closest_promptjet_p4t.SetPz(0.)
    if closest_recotop_p4 != None:
        nrecochi += 1
        closest_RecoTop_costheta_all[0] = recotop.costhetapol(tightlep.p4(), closest_promptjet.p4(), closest_recotop_p4) 
        closest_RecoTop_costhetalep_all[0] = recotop.costhetapollep(tightlep.p4(), closest_recotop_p4)

    #subleading jet reconstruction                                                      
    if len(highptJets) > 1:
        sublead_jet_p4_pre = copy.deepcopy(highptJets[1].p4())
        sublead_jet = highptJets[1]
    else:
        sublead_jet_p4_pre = copy.deepcopy(goodJets[1].p4())
        sublead_jet = goodJets[1]
    
    sublead_jet_p4 = sublead_jet_p4_pre
    
    #Switching jets if Wpjet is btagged and topbjet isn't
    bjet = None
    nobjet = None
    is_sublead_topjet_btag = None
    is_sublead_Wpjet_btag = None

    is_sublead_topjet_btag = int(len(bjet_filter([sublead_jet], 'DeepFlv', 'M')[0]))
    is_sublead_Wpjet_btag = int(len(bjet_filter([sublead_promptjet], 'DeepFlv', 'M')[0]))
    if is_sublead_topjet_btag == 0 and is_sublead_Wpjet_btag == 1 and bjetSwitch:
        #print("is topjet btag: ", is_sublead_topjet_btag, "is Wpjet btag: ", is_sublead_Wpjet_btag)
        #print("sublead_topjet: ", sublead_jet, "sublead_promptjet", sublead_promptjet)
        bjet = copy.copy(sublead_promptjet)
        nobjet = copy.copy(sublead_jet)
        #bjet_p4 = sublead_promptjet.p4()
        #nobjet_p4 = sublead_jet.p4()
        #sublead_jet_p4 = copy.deepcopy(bjet_p4)
        #sublead_promptjet_p4 = copy.deepcopy(nobjet_p4)
        #print("bjet: ", bjet, "nobjet: ", nobjet)
        #print(sublead_jet_p4.Print())
        #print(sublead_promptjet.p4().Print())
        sublead_jet = copy.copy(bjet)
        sublead_promptjet = copy.copy(nobjet)
        #print("sublead_topjet: ", sublead_jet, "sublead_promptjet", sublead_promptjet)
        #print("bjet: ", bjet, "nobjet: ", nobjet)
        sublead_jet_p4 = sublead_jet.p4()
        sublead_promptjet_p4 = sublead_promptjet.p4()
        #print(sublead_jet_p4.Print())
        #print(sublead_promptjet_p4.Print())
   

    ## Subleading top reconstruction
    sublead_recotop_p4, IsNeg_sublead, sublead_dR_lepjet = recotop.top4Momentum(tightlep.p4(), sublead_jet_p4, MET['metPx'], MET['metPy'])
    IsNeg_sublead = IsNeg_sublead * DeltaFilter
    sublead_jet_p4t = copy.deepcopy(sublead_jet_p4)
    sublead_jet_p4t.SetPz(0.)
    sublead_recotop_p4t = tightlep_p4t + sublead_jet_p4t + recomet_p4t
    sublead_promptjet_p4t = copy.deepcopy(sublead_promptjet.p4())
    sublead_promptjet_p4t.SetPz(0.)
    if sublead_recotop_p4 != None:
        nrecochi += 1
        sublead_RecoTop_costheta_all[0] = recotop.costhetapol(tightlep.p4(), sublead_promptjet.p4(), sublead_recotop_p4) 
        sublead_RecoTop_costhetalep_all[0] = recotop.costhetapollep(tightlep.p4(), sublead_recotop_p4)

    btag_countings_sublead = len(bjet_filter([sublead_promptjet, sublead_jet], 'DeepFlv', 'M')[0])

    #best jet reconstruction                                                           
    best_recotop_p4 = None
    IsNeg_best = None
    best_dR_lepjet = None
    is_best_topjet_btag = None
    is_best_Wpjet_btag = None

    if chi_jet_p4_pre == closest_jet_p4_pre:
        #print("\tchi == closest")
        best_jet_p4 = copy.deepcopy(chi_jet_p4)
        best_jet = chi_jet
        best_promptjet = chi_promptjet
        best_recotop_p4 = chi_recotop_p4
        IsNeg_best = IsNeg_chi
        best_dR_lepjet = chi_dR_lepjet
        is_best_topjet_btag = copy.deepcopy(is_chi_topjet_btag)
        is_best_Wpjet_btag = copy.deepcopy(is_chi_Wpjet_btag)
    elif sublead_jet_p4_pre == chi_jet_p4_pre:
        #print("\tchi == sublead")
        best_jet_p4 = copy.deepcopy(chi_jet_p4)
        best_jet = chi_jet
        best_promptjet = chi_promptjet
        best_recotop_p4 = chi_recotop_p4
        IsNeg_best = IsNeg_chi
        best_dR_lepjet = chi_dR_lepjet
        is_best_topjet_btag = copy.deepcopy(is_chi_topjet_btag)
        is_best_Wpjet_btag = copy.deepcopy(is_chi_Wpjet_btag)
    elif sublead_jet_p4_pre == closest_jet_p4_pre:
        #print("\tsublead == closest")
        best_jet_p4 = copy.deepcopy(sublead_jet_p4)
        best_jet = sublead_jet
        best_promptjet = sublead_promptjet
        best_recotop_p4 = sublead_recotop_p4
        IsNeg_best = IsNeg_sublead
        best_dR_lepjet = sublead_dR_lepjet
        is_best_topjet_btag = copy.deepcopy(is_sublead_topjet_btag)
        is_best_Wpjet_btag = copy.deepcopy(is_sublead_Wpjet_btag)
    else:
        #print("\tchi != closest != sublead")
        best_jet_p4 = copy.deepcopy(chi_jet_p4)
        best_jet = chi_jet
        best_promptjet = chi_promptjet
        best_recotop_p4 = chi_recotop_p4
        IsNeg_best = IsNeg_chi
        best_dR_lepjet = chi_dR_lepjet
        is_best_topjet_btag = copy.deepcopy(is_chi_topjet_btag)
        is_best_Wpjet_btag = copy.deepcopy(is_chi_Wpjet_btag)
    #print( " ================= best top mass is %f " %best_recotop_p4.M())

    #print("best_topjet: ", best_jet, "best_promptjet", best_promptjet)

    '''
    #Switching jets if Wpjet is btagged and topbjet isn't
    bjet = None
    nobjet = None
    if is_best_topjet_btag == 0 and is_best_Wpjet_btag == 1 and bjetSwitch:
        print("is topjet btag: ", is_best_topjet_btag, "is Wpjet btag: ", is_best_Wpjet_btag)
        bjet = copy.copy(best_promptjet)
        nobjet = copy.copy(best_jet)
        #bjet_p4 = best_promptjet.p4()
        #nobjet_p4 = best_jet.p4()
        #best_jet_p4 = copy.deepcopy(bjet_p4)
        #best_promptjet_p4 = copy.deepcopy(nobjet_p4)
        print("bjet: ", bjet, "nobjet: ", nobjet)
        print(best_jet_p4.Print())
        print(best_promptjet.p4().Print())
        best_jet = copy.copy(bjet)
        best_promptjet = copy.copy(nobjet)
        print("best_topjet: ", best_jet, "best_promptjet", best_promptjet)
        print("bjet: ", bjet, "nobjet: ", nobjet)
        best_jet_p4 = best_jet.p4()
        best_promptjet_p4 = best_promptjet.p4()
        print(best_jet_p4.Print())
        print(best_promptjet_p4.Print())
    '''

    IsNeg_best = IsNeg_best * DeltaFilter
    best_jet_p4t = copy.deepcopy(best_jet_p4)
    best_jet_p4t.SetPz(0.)
    best_recotop_p4t = tightlep_p4t + best_jet_p4t + recomet_p4t
    best_promptjet_p4t = copy.deepcopy(best_promptjet.p4())
    best_promptjet_p4t.SetPz(0.)
    closAK8, dR_besttopAK4AK8 = closest(best_jet, fatjets)
    ptrel_besttopAK4_closestAK8[0] = best_jet.pt/closAK8.pt
    deltaR_besttopAK4_closestAK8[0] = copy.deepcopy(dR_besttopAK4AK8)

    topAK8_area[0] = closAK8.area
    topAK8_btag[0] = closAK8.btagDeepB
    topAK8_ttagMD[0] = closAK8.deepTagMD_TvsQCD
    topAK8_ttag[0] = closAK8.deepTag_TvsQCD
    topAK8_eta[0] = closAK8.eta
    topAK8_m[0] = closAK8.mass
    topAK8_mSD[0] = closAK8.msoftdrop
    topAK8_phi[0] = closAK8.phi
    topAK8_pt[0] = closAK8.pt
    topAK8_tau1[0] = closAK8.tau1
    topAK8_tau2[0] = closAK8.tau2
    topAK8_tau3[0] = closAK8.tau3
    topAK8_tau4[0] = closAK8.tau4

    if best_recotop_p4 != None:
        nrecobest += 1
        best_RecoTop_costheta_all[0] = recotop.costhetapol(tightlep.p4(), best_promptjet.p4(), best_recotop_p4) 
        best_RecoTop_costhetalep_all[0] = recotop.costhetapollep(tightlep.p4(), best_recotop_p4)
    
    #tag_countings_best = len(bjet_filter([best_promptjet, best_jet], 'DeepFlv', 'M')[0])

    #Wprime reco                                                                        
    if closest_recotop_p4 != None and tightlep != None:
        closest_Wprime_p4 = closest_recotop_p4 + closest_promptjet.p4()
        closest_Wprime_p4t = closest_recotop_p4t + closest_promptjet_p4t
        closest_Wprime_m_all[0] = closest_Wprime_p4.M()
        closest_Wprime_mt_all[0] = closest_Wprime_p4t.M()
        closest_Wprime_pt_all[0] = closest_Wprime_p4.Pt()
        closest_Wprime_eta_all[0] = closest_Wprime_p4.Eta()
        closest_Wprime_phi_all[0] = closest_Wprime_p4.Phi()
        closest_RecoTop_m_all[0] = closest_recotop_p4.M()
        closest_RecoTop_mt_all[0] = closest_recotop_p4t.M()
        closest_RecoTop_pt_all[0] = closest_recotop_p4.Pt()
        closest_RecoTop_eta_all[0] = closest_recotop_p4.Eta()
        closest_RecoTop_phi_all[0] = closest_recotop_p4.Phi()
        closest_RecoTop_isNeg_all[0] = int(IsNeg_closest)
        closest_TopJet_m_all[0] = closest_jet_p4.M()
        closest_TopJet_pt_all[0] = closest_jet_p4.Pt()
        closest_TopJet_eta_all[0] = closest_jet_p4.Eta()
        closest_TopJet_phi_all[0] = closest_jet_p4.Phi()
        closest_TopJet_isBTagged_all[0] = copy.deepcopy(is_closest_topjet_btag) #int(len(bjet_filter([closest_jet], 'DeepFlv', 'M')[0]))
        #print("closest_TopJet_isBTagged: ", closest_TopJet_isBTagged_all[0])
        closest_TopJet_dRLepJet_all[0] = copy.deepcopy(closest_dR_lepjet)
        closest_WpJet_m_all[0] = closest_promptjet.p4().M()
        closest_WpJet_pt_all[0] = closest_promptjet.p4().Pt()
        closest_WpJet_eta_all[0] = closest_promptjet.p4().Eta()
        closest_WpJet_phi_all[0] = closest_promptjet.p4().Phi()
        closest_WpJet_isBTagged_all[0] = copy.deepcopy(is_closest_Wpjet_btag) #int(len(bjet_filter([closest_promptjet], 'DeepFlv', 'M')[0]))
        #print("closest_WpJet_isBTagged: ", closest_WpJet_isBTagged_all[0])
        #print( "closest W' mass: ", closest_Wprime_p4.M())
    else:
        closest_Wprime_m_all[0] = -100.
        closest_Wprime_mt_all[0] = -100.
        closest_Wprime_pt_all[0] = -100.
        closest_Wprime_eta_all[0] = -100.
        closest_Wprime_phi_all[0] = -100.
        closest_RecoTop_m_all[0] = -100.
        closest_RecoTop_mt_all[0] = -100.
        closest_RecoTop_pt_all[0] = -100.
        closest_RecoTop_eta_all[0] = -100.
        closest_RecoTop_phi_all[0] = -100.
        closest_RecoTop_isNeg_all[0] = -1
        closest_TopJet_m_all[0] = -100.
        closest_TopJet_pt_all[0] = -100.
        closest_TopJet_eta_all[0] = -100.
        closest_TopJet_phi_all[0] = -100.
        closest_TopJet_isBTagged_all[0] = -1
        closest_TopJet_dRLepJet_all[0] = -100.
        closest_WpJet_m_all[0] = -100.
        closest_WpJet_pt_all[0] = -100.
        closest_WpJet_eta_all[0] = -100.
        closest_WpJet_phi_all[0] = -100.
        closest_WpJet_isBTagged_all[0] = -1

    if chi_recotop_p4 != None and tightlep != None:
        chi_Wprime_p4 = chi_recotop_p4 + chi_promptjet.p4()
        chi_Wprime_p4t = chi_recotop_p4t + chi_promptjet_p4t
        chi_Wprime_m_all[0] = chi_Wprime_p4.M()
        chi_Wprime_mt_all[0] = chi_Wprime_p4t.M()
        chi_Wprime_pt_all[0] = chi_Wprime_p4.Pt()
        chi_Wprime_eta_all[0] = chi_Wprime_p4.Eta()
        chi_Wprime_phi_all[0] = chi_Wprime_p4.Phi()
        chi_RecoTop_m_all[0] = chi_recotop_p4.M()
        chi_RecoTop_mt_all[0] = chi_recotop_p4t.M()
        chi_RecoTop_pt_all[0] = chi_recotop_p4.Pt()
        chi_RecoTop_eta_all[0] = chi_recotop_p4.Eta()
        chi_RecoTop_phi_all[0] = chi_recotop_p4.Phi()
        chi_RecoTop_isNeg_all[0] = int(IsNeg_chi)
        chi_TopJet_m_all[0] = chi_jet_p4.M()
        chi_TopJet_pt_all[0] = chi_jet_p4.Pt()
        chi_TopJet_eta_all[0] = chi_jet_p4.Eta()
        chi_TopJet_phi_all[0] = chi_jet_p4.Phi()
        chi_TopJet_isBTagged_all[0] = copy.deepcopy(is_chi_topjet_btag) #int(len(bjet_filter([chi_jet], 'DeepFlv', 'M')[0]))
        #print("chi_TopJet_isBTagged: ", chi_TopJet_isBTagged_all[0])
        chi_TopJet_dRLepJet_all[0] = copy.deepcopy(chi_dR_lepjet)
        chi_WpJet_m_all[0] = chi_promptjet.p4().M()
        chi_WpJet_pt_all[0] = chi_promptjet.p4().Pt()
        chi_WpJet_eta_all[0] = chi_promptjet.p4().Eta()
        chi_WpJet_phi_all[0] = chi_promptjet.p4().Phi()
        chi_WpJet_isBTagged_all[0] = copy.deepcopy(is_chi_Wpjet_btag) #int(len(bjet_filter([chi_promptjet], 'DeepFlv', 'M')[0]))
        #print("chi_WpJet_isBTagged: ", chi_WpJet_isBTagged_all[0])
        closAK8, dR_bestWAK4AK8 = closest(chi_promptjet, fatjets) 
        ptrel_bestWAK4_closestAK8[0] = chi_promptjet.pt/closAK8.pt
        deltaR_bestWAK4_closestAK8[0] = copy.deepcopy(dR_bestWAK4AK8)
        chi_topW_jets_pt[0] = (chi_jet_p4 + chi_promptjet.p4()).Pt()
        chi_topW_jets_deltaR[0] = deltaR(chi_jet_p4.Eta(), chi_jet_p4.Phi(), chi_promptjet.p4().Eta(), chi_promptjet.p4().Phi())
        chi_topW_jets_deltaphi[0] = deltaPhi(chi_jet_p4.Phi(), chi_promptjet.p4().Phi())
        #print("chi W' mass: ", chi_Wprime_p4.M())
    else:
        chi_Wprime_m_all[0] = -100.
        chi_Wprime_mt_all[0] = -100.
        chi_Wprime_pt_all[0] = -100.
        chi_Wprime_eta_all[0] = -100.
        chi_Wprime_phi_all[0] = -100.
        chi_RecoTop_m_all[0] = -100.
        chi_RecoTop_mt_all[0] = -100.
        chi_RecoTop_pt_all[0] = -100.
        chi_RecoTop_eta_all[0] = -100.
        chi_RecoTop_phi_all[0] = -100.
        chi_RecoTop_isNeg_all[0] = -1
        chi_TopJet_m_all[0] = -100.
        chi_TopJet_pt_all[0] = -100.
        chi_TopJet_eta_all[0] = -100.
        chi_TopJet_phi_all[0] = -100.
        chi_TopJet_isBTagged_all[0] = -1
        chi_TopJet_dRLepJet_all[0] = -100.
        chi_WpJet_m_all[0] = -100.
        chi_WpJet_pt_all[0] = -100.
        chi_WpJet_eta_all[0] = -100.
        chi_WpJet_phi_all[0] = -100.
        chi_WpJet_isBTagged_all[0] = -1

    if sublead_recotop_p4 != None and tightlep != None:
        sublead_Wprime_p4 = sublead_recotop_p4 + sublead_promptjet.p4()
        sublead_Wprime_p4t = sublead_recotop_p4t + sublead_promptjet_p4t
        sublead_Wprime_m_all[0] = sublead_Wprime_p4.M()
        sublead_Wprime_mt_all[0] = sublead_Wprime_p4t.M()
        sublead_Wprime_pt_all[0] = sublead_Wprime_p4.Pt()
        sublead_Wprime_eta_all[0] = sublead_Wprime_p4.Eta()
        sublead_Wprime_phi_all[0] = sublead_Wprime_p4.Phi()
        sublead_RecoTop_m_all[0] = sublead_recotop_p4.M()
        sublead_RecoTop_mt_all[0] = sublead_recotop_p4t.M()
        sublead_RecoTop_pt_all[0] = sublead_recotop_p4.Pt()
        sublead_RecoTop_eta_all[0] = sublead_recotop_p4.Eta()
        sublead_RecoTop_phi_all[0] = sublead_recotop_p4.Phi()
        sublead_RecoTop_isNeg_all[0] = int(IsNeg_sublead)
        sublead_TopJet_m_all[0] = sublead_jet_p4.M()
        sublead_TopJet_pt_all[0] = sublead_jet_p4.Pt()
        sublead_TopJet_eta_all[0] = sublead_jet_p4.Eta()
        sublead_TopJet_phi_all[0] = sublead_jet_p4.Phi()
        sublead_TopJet_isBTagged_all[0] = copy.deepcopy(is_sublead_topjet_btag) #int(len(bjet_filter([sublead_jet], 'DeepFlv', 'M')[0]))
        #print("sublead_TopJet_isBTagged: ", sublead_TopJet_isBTagged_all[0])
        sublead_TopJet_dRLepJet_all[0] = copy.deepcopy(sublead_dR_lepjet)
        sublead_WpJet_m_all[0] = sublead_promptjet.p4().M()
        sublead_WpJet_pt_all[0] = sublead_promptjet.p4().Pt()
        sublead_WpJet_eta_all[0] = sublead_promptjet.p4().Eta()
        sublead_WpJet_phi_all[0] = sublead_promptjet.p4().Phi()
        sublead_WpJet_isBTagged_all[0] = copy.deepcopy(is_sublead_Wpjet_btag) #int(len(bjet_filter([sublead_promptjet], 'DeepFlv', 'M')[0]))
        #print("sublead_WpJet_isBTagged: ", sublead_WpJet_isBTagged_all[0])
        #print( "sublead W' mass: ", sublead_Wprime_p4.M())
    else:
        sublead_Wprime_m_all[0] = -100.
        sublead_Wprime_mt_all[0] = -100.
        sublead_Wprime_pt_all[0] = -100.
        sublead_Wprime_eta_all[0] = -100.
        sublead_Wprime_phi_all[0] = -100.
        sublead_RecoTop_m_all[0] = -100.
        sublead_RecoTop_mt_all[0] = -100.
        sublead_RecoTop_pt_all[0] = -100.
        sublead_RecoTop_eta_all[0] = -100.
        sublead_RecoTop_phi_all[0] = -100.
        sublead_RecoTop_isNeg_all[0] = -1
        sublead_TopJet_dRLepJet_all[0] = -100.
        sublead_TopJet_m_all[0] = -100.
        sublead_TopJet_pt_all[0] = -100.
        sublead_TopJet_eta_all[0] = -100.
        sublead_TopJet_phi_all[0] = -100.
        sublead_TopJet_isBTagged_all[0] = -1
        sublead_WpJet_m_all[0] = -100.
        sublead_WpJet_pt_all[0] = -100.
        sublead_WpJet_eta_all[0] = -100.
        sublead_WpJet_phi_all[0] = -100.
        sublead_WpJet_isBTagged_all[0] = -1

    if best_recotop_p4 != None and tightlep != None:
        best_Wprime_p4 = best_recotop_p4 + best_promptjet.p4()
        best_Wprime_p4t = best_recotop_p4t + best_promptjet_p4t
        best_Wprime_m_all[0] = best_Wprime_p4.M()
        best_Wprime_mt_all[0] = best_Wprime_p4t.M()
        best_Wprime_pt_all[0] = best_Wprime_p4.Pt()
        best_Wprime_eta_all[0] = best_Wprime_p4.Eta()
        best_Wprime_phi_all[0] = best_Wprime_p4.Phi()
        best_RecoTop_m_all[0] = best_recotop_p4.M()
        best_RecoTop_mt_all[0] = best_recotop_p4t.M()
        best_RecoTop_pt_all[0] = best_recotop_p4.Pt()
        best_RecoTop_eta_all[0] = best_recotop_p4.Eta()
        best_RecoTop_phi_all[0] = best_recotop_p4.Phi()
        best_RecoTop_isNeg_all[0] = int(IsNeg_best)
        best_TopJet_m_all[0] = best_jet_p4.M()
        best_TopJet_pt_all[0] = best_jet_p4.Pt()
        best_TopJet_eta_all[0] = best_jet_p4.Eta()
        best_TopJet_phi_all[0] = best_jet_p4.Phi()
        best_TopJet_isBTagged_all[0] = copy.deepcopy(is_best_topjet_btag) #int(len(bjet_filter([best_jet], 'DeepFlv', 'M')[0]))
        #print("best_TopJet_isBTagged: ", best_TopJet_isBTagged_all[0])
        best_TopJet_btagscore_all[0] = best_jet.btagDeepFlavB
        best_TopJet_dRLepJet_all[0] = copy.deepcopy(best_dR_lepjet)
        best_WpJet_m_all[0] = best_promptjet.p4().M()
        best_WpJet_pt_all[0] = best_promptjet.p4().Pt()
        best_WpJet_eta_all[0] = best_promptjet.p4().Eta()
        best_WpJet_phi_all[0] = best_promptjet.p4().Phi()
        best_WpJet_isBTagged_all[0] = copy.deepcopy(is_best_Wpjet_btag) #int(len(bjet_filter([best_promptjet], 'DeepFlv', 'M')[0]))
        #print("best_WpJet_isBTagged: ", best_WpJet_isBTagged_all[0])
        best_WpJet_btagscore_all[0] = best_promptjet.btagDeepFlavB
        closAK8, dR_bestWAK4AK8 = closest(best_promptjet, fatjets) 
        ptrel_bestWAK4_closestAK8[0] = best_promptjet.pt/closAK8.pt
        deltaR_bestWAK4_closestAK8[0] = copy.deepcopy(dR_bestWAK4AK8)
        best_topW_jets_pt[0] = (best_jet_p4 + best_promptjet.p4()).Pt()
        best_topW_jets_deltaR[0] = deltaR(best_jet_p4.Eta(), best_jet_p4.Phi(), best_promptjet.p4().Eta(), best_promptjet.p4().Phi())
        best_topW_jets_deltaphi[0] = deltaPhi(best_jet_p4.Phi(), best_promptjet.p4().Phi())
        WprAK8_area[0] = closAK8.area
        WprAK8_btag[0] = closAK8.btagDeepB
        WprAK8_ttagMD[0] = closAK8.deepTagMD_TvsQCD
        WprAK8_ttag[0] = closAK8.deepTag_TvsQCD
        WprAK8_eta[0] = closAK8.eta
        WprAK8_m[0] = closAK8.mass
        WprAK8_mSD[0] = closAK8.msoftdrop
        WprAK8_phi[0] = closAK8.phi
        WprAK8_pt[0] = closAK8.pt
        WprAK8_tau1[0] = closAK8.tau1
        WprAK8_tau2[0] = closAK8.tau2
        WprAK8_tau3[0] = closAK8.tau3
        WprAK8_tau4[0] = closAK8.tau4
        #print( "best W' mass: ", best_Wprime_p4.M())
    else:
        best_Wprime_m_all[0] = -100.
        best_Wprime_mt_all[0] = -100.
        best_Wprime_pt_all[0] = -100.
        best_Wprime_eta_all[0] = -100.
        best_Wprime_phi_all[0] = -100.
        best_RecoTop_m_all[0] = -100.
        best_RecoTop_mt_all[0] = -100.
        best_RecoTop_pt_all[0] = -100.
        best_RecoTop_eta_all[0] = -100.
        best_RecoTop_phi_all[0] = -100.
        best_RecoTop_isNeg_all[0] = -1
        best_TopJet_m_all[0] = -100.
        best_TopJet_pt_all[0] = -100.
        best_TopJet_eta_all[0] = -100.
        best_TopJet_phi_all[0] = -100.
        best_TopJet_isBTagged_all[0] = -1
        best_TopJet_btagscore_all[0] = -100.
        #print(type(best_TopJet_btagscore_all[0]))
        best_TopJet_dRLepJet_all[0] = -100.
        best_WpJet_m_all[0] = -100.
        best_WpJet_pt_all[0] = -100.
        best_WpJet_eta_all[0] = -100.
        best_WpJet_phi_all[0] = -100.                    
        best_WpJet_isBTagged_all[0] = -1
        best_WpJet_btagscore_all[0] = -100.
        
    systTree.setWeightName("w_nominal",copy.deepcopy(w_nominal_all[0]))
    systTree.fillTreesSysts(trees, "all")

if Debug:
    print("Event with neutrino failed: ", neutrino_failed, " out of ", str(50000))
else:
    print("Event with neutrino failed: ", neutrino_failed, " out of ", tree.GetEntries())

#trees[0].Print()
outTreeFile.cd()
if(isMC):
    print("h_genweight first bin content is %f and h_PDFweight has %f bins" %(h_genweight.GetBinContent(1), h_PDFweight.GetNbinsX()))
    h_genweight.Write()
    h_PDFweight.Write()
    h_eff_mu.Write()
    h_eff_ele.Write()
systTree.writeTreesSysts(trees, outTreeFile)

endTime = datetime.datetime.now()
print("Ending running at " + str(endTime))
