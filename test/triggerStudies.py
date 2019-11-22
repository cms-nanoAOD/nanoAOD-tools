import os
import sys
import math
import argparse
import ROOT
import numpy as np
import random
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from pprint import pprint

class MuonSelection(Module):
    def __init__(self):
        self.vetoPt = 15.
        self.vetoEta = 2.5
        self.loosePt = 26.
        self.looseEta = 2.5
        self.tightPt = 26.
        self.tightEta = 2.4
        self.vetoIso = 25
        self.looseIso = 25
        self.tightIso = 15
        
    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("n_veto_muons","I")
        self.out.branch("n_loose_muons","I")
        self.out.branch("n_tight_muons","I")
        self.out.branch("muon_trigger","I")
       
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    def analyze(self, event):

        """process event, return True (go to next module) or False (fail, go to next event)"""

        muons = Collection(event, "Muon")
        
        event.selectedMuons = {
            "veto":[],
            "loose":[],
            "tight":[],
        }
        
        for muon in muons:

            if muon.pt > self.tightPt and abs(muon.eta) < self.tightEta and muon.pfRelIso04_all < self.tightIso and muon.tightId:
                event.selectedMuons["tight"].append(muon)

            if muon.pt > self.loosePt and abs(muon.eta) < self.looseEta and muon.pfRelIso04_all < self.looseIso:
                event.selectedMuons["loose"].append(muon)

            if muon.pt > self.vetoPt and abs(muon.eta) < self.vetoEta and muon.pfRelIso04_all < self.vetoIso:
                event.selectedMuons["veto"].append(muon)

    	self.out.fillBranch("n_veto_muons",len(event.selectedMuons["veto"]))
    	self.out.fillBranch("n_loose_muons",len(event.selectedMuons["loose"]))
    	self.out.fillBranch("n_tight_muons",len(event.selectedMuons["tight"]))
        self.out.fillBranch("muon_trigger", event.HLT_IsoMu24 or event.HLT_IsoTkMu24)
    	return True

class ElectronSelection(Module):
    def __init__(self):

        self.vetoPt = 15.
        self.vetoEta = 2.5
        
        self.loosePt = 35.
        self.looseEta = 2.5

        self.tightPt = 35.
        self.tightEta = 2.5
    
    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("n_veto_electrons","I")
        self.out.branch("n_loose_electrons","I")
        self.out.branch("n_tight_electrons","I")
        self.out.branch("electron_trigger","I")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        
        event.selectedElectrons = {"veto":[], "loose":[], "tight":[]}

        for electron in electrons:
            if electron.pt>self.loosePt and math.fabs(electron.eta)<self.looseEta and electron.cutBased>0:
                event.selectedElectrons["loose"].append(electron)

            if electron.pt>self.tightPt and math.fabs(electron.eta)<self.tightEta and electron.cutBased==3:
                event.selectedElectrons["tight"].append(electron)


            if electron.pt>self.vetoPt and math.fabs(electron.eta)<self.vetoEta and electron.cutBased==0:
                event.selectedElectrons["veto"].append(electron)


    	self.out.fillBranch("n_veto_electrons",len(event.selectedElectrons["veto"]))
    	self.out.fillBranch("n_loose_electrons",len(event.selectedElectrons["loose"]))
    	self.out.fillBranch("n_tight_electrons",len(event.selectedElectrons["tight"]))
        self.out.fillBranch("electron_trigger", event.HLT_Ele27_WPTight_Gsf)

        return True
    
class JetSelection(Module):
    def __init__(self,getLeptonCollection=lambda x:None, process=None):
        self.getLeptonCollection = getLeptonCollection
        self.process = process
        self.jetGroups = {
            "central":lambda jet: jet.jetId > 0 and jet.pt>30. and math.fabs(jet.eta)<2.4,
            "forward":lambda jet: jet.pt>50. and math.fabs(jet.eta) > 2.4,
            "failId":lambda jet: jet.jetId == 0 and jet.pt>30. and math.fabs(jet.eta)<2.4
        }

    def beginJob(self):
        pass
    
    def endJob(self):
        pass

    def notLepton(self, jet, leptons):
        for lepton in leptons:
            if lepton.p4().DeltaR(jet.p4()) < 0.4:
                return False
        return True

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree

        if "SMS" in self.process:
            self.out.branch("llpinfo_llp_mass", "F")
            self.out.branch("llpinfo_lsp_mass", "F")
            self.out.branch("isDisplaced", "I")

        if "SMS" in self.process or "TT_Tune" in self.process:
            self.out.branch("genWeight", "F")

        self.out.branch("MET_pt", "F")
        self.out.branch("MET_NoMu", "F")
        self.out.branch("HLT_PFMETNoMu120_PFMHTNoMu120_IDTight", "I")
        self.out.branch("HLT_MonoCentralPFJet80_PFMETNoMu90_PFMHTNoMu90_IDTight", "I")
        self.out.branch("HLT_MonoCentralPFJet80_PFMETNoMu100_PFMHTNoMu100_IDTight", "I")
        self.out.branch("HLT_MonoCentralPFJet80_PFMETNoMu110_PFMHTNoMu110_IDTight", "I")
        self.out.branch("HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight", "I")
        self.out.branch("HLT_PFHT900", "I")
        self.out.branch("nCentralJets", "I")
        self.out.branch("nForwardJets", "I")
        self.out.branch("jetIdVeto", "I")

        for group in self.jetGroups.keys():
            
            self.out.branch("jet1_pt_"+group,"F")
            self.out.branch("jet1_jetId_"+group,"F")
            self.out.branch("jet1_chEmEF_"+group, "F")
            self.out.branch("jet1_chHEF_"+group, "F")
            self.out.branch("jet1_neEmEF_"+group, "F")
            self.out.branch("jet1_neHEF_"+group, "F")
            self.out.branch("jet1_CHM_"+group, "F")
            self.out.branch("jet1_nConstituents_"+group, "F")
            self.out.branch("jet2_pt_"+group,"F")
            self.out.branch("jet2_jetId_"+group,"F")
            self.out.branch("ht_"+group,"F")
            self.out.branch("mht_NoMu_"+group, "F")
            self.out.branch("mht_"+group,"F")
            self.out.branch("R_NoMu_"+group, "F")
            self.out.branch("R_"+group, "F")
            if "SMS" in self.process:
                self.out.branch("jet1_fromLLP_"+group,"F")
                self.out.branch("jet1_displacement_"+group,"F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = Collection(event, "Jet")
        if "SMS" in self.process:
            jetorigin = Collection(event, "jetorigin")
        event.selectedJets = {}
        
        for group,groupSelector in self.jetGroups.iteritems():
            event.selectedJets[group] = {
                "loose":[],
                "ht":0.0,
                "mht":0.0,
                }
            
            vecsum = ROOT.TLorentzVector()

            for ijet,jet in enumerate(jets):

                if groupSelector(jet) and self.notLepton(jet, event.selectedMuons["loose"]):
                                   
                    event.selectedJets[group]["loose"].append(jet)
                    event.selectedJets[group]["ht"]+=jet.pt
                    vecsum += -jet.p4()
                    event.selectedJets[group]["mht"] = vecsum.Pt()
                    
            if len(event.selectedJets[group]["loose"])>0:
                jet = event.selectedJets[group]["loose"][0]
                self.out.fillBranch("jet1_pt_"+group,jet.pt)
                self.out.fillBranch("jet1_jetId_"+group,jet.jetId)
                self.out.fillBranch("jet1_chEmEF_"+group, jet.chEmEF )
                self.out.fillBranch("jet1_chHEF_"+group, jet.chHEF )
                self.out.fillBranch("jet1_neEmEF_"+group, jet.neEmEF )
                self.out.fillBranch("jet1_neHEF_"+group, jet.neHEF )
                self.out.fillBranch("jet1_CHM_"+group, jet.CHM )
                self.out.fillBranch("jet1_nConstituents_"+group, jet.nConstituents )
                if "SMS" in self.process:
                    origin = jetorigin[0]
                    self.out.fillBranch("jet1_fromLLP_"+group, origin.fromLLP)
                    self.out.fillBranch("jet1_displacement_"+group, origin.displacement)

                if jet.pt < 80:
                    return False

            if len(event.selectedJets[group]["loose"])>1:
                jet = event.selectedJets[group]["loose"][1]
                self.out.fillBranch("jet2_pt_"+group,jet.pt)
                self.out.fillBranch("jet2_jetId_"+group,jet.jetId)


            self.out.fillBranch("ht_"+group, event.selectedJets[group]["ht"])
            self.out.fillBranch("mht_"+group, event.selectedJets[group]["mht"])

            mht_NoMu = vecsum
            for muon in event.selectedMuons["loose"]:
                    mht_NoMu += muon.p4()
            event.selectedJets[group]["mht_NoMu"] = mht_NoMu.Pt()

            self.out.fillBranch("mht_NoMu_"+group, event.selectedJets[group]["mht_NoMu"])
            self.out.fillBranch("HLT_PFMETNoMu120_PFMHTNoMu120_IDTight",event.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight)
            self.out.fillBranch("HLT_PFHT900",event.HLT_PFHT900)

            if "Run2016H" not in self.process:
                self.out.fillBranch("HLT_MonoCentralPFJet80_PFMETNoMu90_PFMHTNoMu90_IDTight", event.HLT_MonoCentralPFJet80_PFMETNoMu90_PFMHTNoMu90_IDTight)
                self.out.fillBranch("HLT_MonoCentralPFJet80_PFMETNoMu100_PFMHTNoMu100_IDTight", event.HLT_MonoCentralPFJet80_PFMETNoMu100_PFMHTNoMu100_IDTight)
            self.out.fillBranch("HLT_MonoCentralPFJet80_PFMETNoMu110_PFMHTNoMu110_IDTight", event.HLT_MonoCentralPFJet80_PFMETNoMu110_PFMHTNoMu110_IDTight)
            self.out.fillBranch("HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight", event.HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight)
 
        met_vector = ROOT.TLorentzVector(event.MET_pt*math.cos(event.MET_phi), event.MET_pt*math.sin(event.MET_phi), 0, 0)
        met_vector_NoMu = met_vector
        for muon in event.selectedMuons["loose"]:
            met_vector_NoMu += muon.p4()
        self.out.fillBranch("MET_pt", event.MET_pt)
        self.out.fillBranch("MET_NoMu", met_vector_NoMu.Pt() )

        for group,groupSelector in self.jetGroups.iteritems():
            self.out.fillBranch("R_NoMu_"+group, event.selectedJets[group]["mht_NoMu"]/met_vector_NoMu.Pt() )
            self.out.fillBranch("R_"+group, event.selectedJets[group]["mht"]/event.MET_pt )

        self.out.fillBranch("nCentralJets", len(event.selectedJets["central"]["loose"]))
        self.out.fillBranch("nForwardJets", len(event.selectedJets["forward"]["loose"]))

        if "SMS" in self.process:
            self.out.fillBranch("llpinfo_llp_mass", int(round(event.llpinfo_llp_mass[0]/100.)*100))
            self.out.fillBranch("llpinfo_lsp_mass", int(round(event.llpinfo_lsp_mass[0]/100.)*100))

        if "SMS" in self.process or "TT_Tune" in self.process:
            self.out.fillBranch("genWeight", event.genWeight)

        jet_veto = 0
        if len(event.selectedJets["failId"]["loose"]) > 0:
            jet_veto = 1
        self.out.fillBranch("jetIdVeto", jet_veto)

        return True

class EventSkim(Module):
    def __init__(self,selection=lambda event: True):
        self.selection = selection
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        return self.selection(event)

class MetFilter(Module):
    def __init__(self, globalOptions={"isData":False}, process=None):
        self.globalOptions=globalOptions
        self.process = process
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        #https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFiltersRun2#Moriond_2017
        if event.Flag_goodVertices==0:
            return False
        if event.Flag_globalTightHalo2016Filter==0:
            return False
        if event.Flag_HBHENoiseFilter==0:
            return False
        if event.Flag_HBHENoiseIsoFilter==0:
            return False
        if event.Flag_EcalDeadCellTriggerPrimitiveFilter==0:
            return False
        if self.globalOptions["isData"] and event.Flag_eeBadScFilter==0: #not suggested on MC
            return False
        return True
 
        
files = []

parser = argparse.ArgumentParser()
parser.add_argument('--input', dest='inputFiles', action='append',default=[])
parser.add_argument('output', nargs=1)

args = parser.parse_args()

print "inputs:",len(args.inputFiles)
f =  args.inputFiles[0]
print f

for inputFile in args.inputFiles:
    rootFile = ROOT.TFile.Open(inputFile)
    if not rootFile:
        print "CRITICAL - file '"+inputFile+"' not found!"
        sys.exit(1)
    tree = rootFile.Get("Events")
    if not tree:
        print "CRITICAL - 'Events' tree not found in file '"+inputFile+"'!"
        sys.exit(1)
    print " - ",inputFile,", events=",tree.GetEntries()
    
print "output directory:",args.output[0]


modules = [MuonSelection(),
        ElectronSelection(),
        JetSelection(getLeptonCollection=lambda event:event.selectedMuons["loose"], process=f),
        MetFilter(process=f)
        ]

modules.append(EventSkim(selection=lambda event: len(event.selectedJets["central"]["loose"])>2))
modules.append(EventSkim(selection=lambda event: len(event.selectedJets["forward"]["loose"])==0))

if "SingleMu" in f:
    modules.append(EventSkim(selection=lambda event: event.muon_trigger))
    modules.append(EventSkim(selection=lambda event: event.n_veto_electrons == 0))

elif "SingleEle" in f:
    modules.append(EventSkim(selection=lambda event: event.electron_trigger))
    modules.append(EventSkim(selection=lambda event: event.n_veto_muons == 0))

elif "TT" in f:
    modules.append(EventSkim(selection=lambda event: event.electron_trigger or event.muon_trigger))

p=PostProcessor(args.output[0],[args.inputFiles],cut=None,branchsel=None,modules=modules, friend=True, maxEvents=-1)
p.run()
