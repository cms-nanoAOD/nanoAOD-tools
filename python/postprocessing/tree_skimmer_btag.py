#!/bin/env python3
import os
##print(os.environ)
##print("**********************************************************************")
##print("**********************************************************************")
##print("**********************************************************************")
##print(str(os.environ.get('PYTHONPATH')))
##print(str(os.environ.get('PYTHON3PATH')))
import sys
##print("*************** This is system version info ***************************")
##print(sys.version_info)
#import platform
##print("*************** This is python version info ***************************")
##print(platform.python_version())
import ROOT
##print("Succesfully imported ROOT")
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
    Debug = False
sample = sample_dict[sys.argv[1]]
part_idx = sys.argv[2]
file_list = list(map(str, sys.argv[3].strip('[]').split(',')))
#print("file_list: ", file_list, "\nloop #1 over it")
#for infile in file_list:
    #print(infile)

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
#print("Number of events in tree from chain " + str((chain.GetTree()).GetEntries()))
#print("Type of tree from chain " + str(type(chain.GetTree())))
#treechain = (ROOT.TTree)(chain.GetTree())
tree = InputTree(chain)
print("Number of entries: " +str(tree.GetEntries()))
#print("tree: ", tree)
isMC = True
if ('Data' in sample.label):
    isMC = False

username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])
folder = 'vbtag'
if not os.path.exists("/eos/user/" + inituser + "/" + username + "/Wprime/nosynch/" + folder + "/" + sample.label):
    os.makedirs("/eos/user/" + inituser + "/" + username +"/Wprime/nosynch/" + folder + "/" + sample.label)
outpath = "/eos/user/" + inituser + "/" + username +"/Wprime/nosynch/" + folder + "/" + sample.label + "/"
#++++++++++++++++++++++++++++++++++
#++   branching the new trees    ++
#++++++++++++++++++++++++++++++++++
outTreeFile = ROOT.TFile(outpath + sample.label+"_part"+str(part_idx)+".root", "RECREATE") #some name of the output file

#++++++++++++++++++++++++++++++++++
#++         All category         ++
#++++++++++++++++++++++++++++++++++

#++++++++++++++++++++++++++++++++++
#++      Efficiency studies      ++
#++++++++++++++++++++++++++++++++++
ptNBins = 100
ptMin = 0
ptMax = 1000.
etaNBins = 60
etaMin = -3.
etaMax = 3.
ptbins = array.array('f', [100, 140, 200, 300, 600, 1000])
etabins = array.array('f', [0.0, 0.8, 1.6, 2.5])
nptbins = len(ptbins)-1
netabins = len(etabins)-1
h2_BTaggingEff_Denom_b    = ROOT.TH2D("h2_BTaggingEff_Denom_b", ";p_{T} [GeV];#eta", nptbins, ptbins, netabins, etabins)
h2_BTaggingEff_Denom_c    = ROOT.TH2D("h2_BTaggingEff_Denom_c", ";p_{T} [GeV];#eta", nptbins, ptbins, netabins, etabins)
h2_BTaggingEff_Denom_udsg = ROOT.TH2D("h2_BTaggingEff_Denom_udsg", ";p_{T} [GeV];#eta", nptbins, ptbins, netabins, etabins)
h2_BTaggingEff_Num_b    = ROOT.TH2D("h2_BTaggingEff_Num_b", ";p_{T} [GeV];#eta", nptbins, ptbins, netabins, etabins)
h2_BTaggingEff_Num_c    = ROOT.TH2D("h2_BTaggingEff_Num_c", ";p_{T} [GeV];#eta", nptbins, ptbins, netabins, etabins)
h2_BTaggingEff_Num_udsg = ROOT.TH2D("h2_BTaggingEff_Num_udsg", ";p_{T} [GeV];#eta", nptbins, ptbins, netabins, etabins)
#++++++++++++++++++++++++++++++++++
#++   looping over the events    ++
#++++++++++++++++++++++++++++++++++
for i in range(tree.GetEntries()):
    #++++++++++++++++++++++++++++++++++
    #++        taking objects        ++
    #++++++++++++++++++++++++++++++++++
    if Debug:
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
    HLT = Object(event, "HLT")

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
    isMuon = (len(goodMu) == 1) and (len(goodEle) == 0) and len(VetoMu) == 0 and len(VetoEle) == 0 and (passMu or passHT)
    isElectron = (len(goodMu) == 0) and (len(goodEle) == 1) and len(VetoMu) == 0 and len(VetoEle) == 0 and (passEle or passHT or passPh)

    if not (isMuon or isElectron):
        continue
    ######################################
    ## Selecting only jets with pt>100  ##
    ######################################
    goodJets = get_Jet(jets, 100)
    bjets, nobjets = bjet_filter(goodJets, 'DeepFlv', 'M')

    if (len(goodJets) < 2 or len(fatjets) < 2):
        continue

    for jet in goodJets:
        if(abs(jet.partonFlavour) == 5):
            h2_BTaggingEff_Denom_b.Fill(jet.pt, abs(jet.eta))
            if(len(bjet_filter([jet], 'DeepFlv', 'M')[0])==1):
                h2_BTaggingEff_Num_b.Fill(jet.pt, abs(jet.eta))
        elif(abs(jet.partonFlavour) == 4):
            h2_BTaggingEff_Denom_c.Fill(jet.pt, abs(jet.eta))
            if(len(bjet_filter([jet], 'DeepFlv', 'M')[0])==1):
                h2_BTaggingEff_Num_c.Fill(jet.pt, abs(jet.eta))
        else:
            h2_BTaggingEff_Denom_udsg.Fill(jet.pt, abs(jet.eta))
            if(len(bjet_filter([jet], 'DeepFlv', 'M')[0])==1):
                h2_BTaggingEff_Num_udsg.Fill(jet.pt, abs(jet.eta))

outTreeFile.cd()
h2_BTaggingEff_Denom_b.Write()
h2_BTaggingEff_Denom_c.Write()
h2_BTaggingEff_Denom_udsg.Write()
h2_BTaggingEff_Num_b.Write()
h2_BTaggingEff_Num_c.Write()
h2_BTaggingEff_Num_udsg.Write()
h2_Eff_b = ROOT.TEfficiency(h2_BTaggingEff_Num_b, h2_BTaggingEff_Denom_b)
h2_Eff_c = ROOT.TEfficiency(h2_BTaggingEff_Num_c, h2_BTaggingEff_Denom_c)
h2_Eff_udsg = ROOT.TEfficiency(h2_BTaggingEff_Num_udsg, h2_BTaggingEff_Denom_udsg)
h2_Eff_b.Write()
h2_Eff_c.Write()
h2_Eff_udsg.Write()

endTime = datetime.datetime.now()
print("Ending running at " + str(endTime))
