#!/usr/bin/env python
import os, sys
import ROOT
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
#from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor


from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class EfficiencyModule(Module):
    def __init__(self,datayear,jetSelection,TightEleSelection,LooseEleSelection):
        self.jetSel = jetSelection
        self.TightEleSel = TightEleSelection
        self.LooseEleSel = LooseEleSelection
        
	self.writeHistFile=True
	self.datayear = datayear

    def beginJob(self,histFile=None,histDirName=None):
	Module.beginJob(self,histFile,histDirName)
	self.list_of_hist = [
                        "Event_total",
                        "Event_HLT_Ele35",
			"Event_HLT_Ele30_eta2p1_crossJet",
			"Event_HLT_IsoMu27",
			"Event_Event_HLT_Ele35_HLT_IsoMu27", 
			"Event_Event_HLT_Ele35_HLT_Ele30_eta2p1_crossJet",  
			"Event_HLT_Ele30_eta2p1_crossJet_HLT_IsoMu27",
			"Event_HLT_Ele30_eta2p1_crossJet_HLT_IsoMu27_HLT_Ele30_eta2p1_crossJet"
        ]

	if(self.datayear=='UL2017'):
            Pt_Edges = np.array([10,20,35,50,100,200,500],dtype='float64')
            Eta_Edges = np.array([-2.5,-2.1,-1.566,-1.4442, -0.8, 0.0, 0.8, 1.4442, 1.566, 2.1, 2.5],dtype='float64')

	for i in range(0, len(self.list_of_hist)):
	    self.list_of_hist[i] = ROOT.TH2D(self.list_of_hist[i],"",len(Eta_Edges)-1,Eta_Edges,len(Pt_Edges)-1,Pt_Edges)

	for i in range(0,len(self.list_of_hist)):
	    self.addObject(self.list_of_hist[i])

    def analyze(self, event):
	if(self.datayear=='UL2017'):
            Num_jet = 2
            Tight_electron = 1
            Loose_electron = 0
            Ele_trigger = "HLT_Ele35_WPTight_Gsf"
            EleJet_cross_trigger = "HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned"
            Muon_trigger = "HLT_IsoMu27"

        jets = Collection(event, "Jet")
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
	#print "number of jets in event = ", len(jets)

        jet_counter = 0 
        for ijet in filter(self.jetSel,jets):
            jet_counter+=1
            #print "jet_pt = ", ijet.pt
            #print "jet_hadronFlavour = ",ijet.hadronFlavour
            #print "jet_DeepB = ",jet_DeepB
        #print "nJet",getattr(event,"nJet")," ",jet_counter

        loose_ele_counter = 0
        tight_ele_counter = 0
        tight_Ele = []
        for ele in filter(self.TightEleSel,electrons):
            tight_ele_counter+=1 
            tight_Ele.append(ele)

        for ele in filter(self.LooseEleSel,electrons):
            loose_ele_counter+=1
            
        if(jet_counter>=2 and loose_ele_counter==0 and tight_ele_counter==1):
            Ele_trig = getattr(event,Ele_trigger)
            Muon_trig = getattr(event,Muon_trigger)
            Ele_cross_trig = getattr(event,Ele_trigger)
            #print "len_tight_el: ", len(tight_Ele),"Ele_trig: ",Ele_trig, "Muon_trig: ",Muon_trig, "Ele_cross_trig: ",Ele_cross_trig
            for Ele in tight_Ele:    
	        self.list_of_hist[0].Fill(Ele.eta+Ele.deltaEtaSC,Ele.pt) #Event_total
	        if(getattr(event,Ele_trigger)==1):
                    self.list_of_hist[1].Fill(Ele.eta+Ele.deltaEtaSC,Ele.pt)  #Event_HLT_Ele35
	        if(getattr(event,EleJet_cross_trigger)==1):
                    self.list_of_hist[2].Fill(Ele.eta+Ele.deltaEtaSC,Ele.pt)  #Event_HLT_Ele30_eta2p1_crossJet
	        if(getattr(event,Muon_trigger)==1):
                    self.list_of_hist[3].Fill(Ele.eta+Ele.deltaEtaSC,Ele.pt)  #Event_HLT_IsoMu27
            if(getattr(event,Muon_trigger)==1 and getattr(event,Ele_trigger)==1): 
                    self.list_of_hist[4].Fill(Ele.eta+Ele.deltaEtaSC,Ele.pt)                            #Event_Event_HLT_Ele35_HLT_IsoMu27
            if(getattr(event,Ele_trigger)==1 and getattr(event,EleJet_cross_trigger)==1):
                    self.list_of_hist[5].Fill(Ele.eta+Ele.deltaEtaSC,Ele.pt)                  #Event_Event_HLT_Ele35_HLT_Ele30_eta2p1_crossJet
            if(getattr(event,Muon_trigger)==1 and getattr(event,EleJet_cross_trigger)==1):
                    self.list_of_hist[6].Fill(Ele.eta+Ele.deltaEtaSC,Ele.pt)                  #Event_HLT_Ele30_eta2p1_crossJet_HLT_IsoMu27
            if(getattr(event,Muon_trigger)==1 and getattr(event,Ele_trigger)==1 and getattr(event,EleJet_cross_trigger)==1):
                    self.list_of_hist[7].Fill(Ele.eta+Ele.deltaEtaSC,Ele.pt) #Event_HLT_Ele30_eta2p1_crossJet_HLT_IsoMu27_HLT_Ele30_eta2p1_crossJet
        else: print(jet_counter," ",loose_ele_counter," ",tight_ele_counter,"----------------")
        return True

EfficiencyConstr_UL2017 = lambda : EfficiencyModule('UL2017',jetSelection= lambda j : j.pt > 40, TightEleSelection = lambda e : e.cutBased == 4,LooseEleSelection = lambda e : e.cutBased < 3)


#preselection="Entry$<500 "
#files=["root://cms-xrd-global.cern.ch///store/mc/RunIISummer16NanoAODv3/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/NANOAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/120000/E4046A1B-A2E1-E811-8878-0025905B85DC.root"]
#files=["60250C73-6FA0-8246-8085-33EF0DEB619D.root"]
#p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[EfficiencyModule()],noOut=True,histFileName="Ele_trigger_hist.root",histDirName="Events_2D_hist")
#p.run()
