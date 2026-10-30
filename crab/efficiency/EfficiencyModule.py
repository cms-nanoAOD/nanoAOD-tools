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
    def __init__(self,datayear,jetSelection):
        self.jetSel = jetSelection
	self.writeHistFile=True
	self.datayear = datayear

    def beginJob(self,histFile=None,histDirName=None):
	Module.beginJob(self,histFile,histDirName)
	self.list_of_hist = ["FlavourB_Wp_pass_No",
			"FlavourB_Wp_pass_BL",
			"FlavourB_Wp_pass_BM",
			"FlavourB_Wp_pass_BT",
			"FlavourC_Wp_pass_No",
			"FlavourC_Wp_pass_BL",
                	"FlavourC_Wp_pass_BM",
                	"FlavourC_Wp_pass_BT",
			"FlavourL_Wp_pass_No",
			"FlavourL_Wp_pass_BL",
                	"FlavourL_Wp_pass_BM",
                	"FlavourL_Wp_pass_BT"]

	if(self.datayear=='2016'):
    	    Pt_Edges = np.array([20.0,30.0,50.0,70.0,100.0,140.0,200.0,300.0,600.0,1000.0],dtype='float64')
    	    Eta_Edges = np.array([0.0,0.2,0.7,1.4,2.0,2.2,2.3,2.5],dtype='float64')

	elif(self.datayear=='2017'):
            Pt_Edges = np.array([20.0,30.0,50.0,70.0,100.0,140.0,200.0,300.0,600.0,1000.0],dtype='float64')
            Eta_Edges = np.array([0.0,0.2,0.8,1.6,2.0,2.2,2.3,2.5],dtype='float64')

	for i in range(0, len(self.list_of_hist)):
	    self.list_of_hist[i] = ROOT.TH2D(self.list_of_hist[i],"",len(Pt_Edges)-1,Pt_Edges,len(Eta_Edges)-1,Eta_Edges)
	    #self.list_of_hist[i] = ROOT.TH2D(self.list_of_hist[i],"",100,0.0,1000.0,50,-5.0,5.0)
	for i in range(0,len(self.list_of_hist)):
	    self.addObject(self.list_of_hist[i])

    def analyze(self, event):
	if(self.datayear=='2016'):	
	    DeepcsvL = 0.1241
            DeepcsvM = 0.4184
            DeepcsvT = 0.7527
	if(self.datayear=='2017'):
            DeepcsvL = 0.1522
            DeepcsvM = 0.4941
            DeepcsvT = 0.8001

        jets = Collection(event, "Jet")
	#print "number of jets in event = ", len(jets)
        for ijet in filter(self.jetSel,jets):
            #print "jet_pt = ", ijet.pt
            #print "jet_hadronFlavour = ",ijet.hadronFlavour
            #print "jet_DeepB = ",jet_DeepB
            if(abs(ijet.hadronFlavour)==5):
		self.list_of_hist[0].Fill(ijet.pt,abs(ijet.eta))
		if(ijet.btagDeepB>DeepcsvL):
                    self.list_of_hist[1].Fill(ijet.pt,abs(ijet.eta))
		if(ijet.btagDeepB>DeepcsvM):
                    self.list_of_hist[2].Fill(ijet.pt,abs(ijet.eta))
		if(ijet.btagDeepB>DeepcsvT):
                    self.list_of_hist[3].Fill(ijet.pt,abs(ijet.eta))
	    elif(abs(ijet.hadronFlavour)==4):
		self.list_of_hist[4].Fill(ijet.pt,abs(ijet.eta))
		if(ijet.btagDeepB>DeepcsvL):
                    self.list_of_hist[5].Fill(ijet.pt,abs(ijet.eta))
                if(ijet.btagDeepB>DeepcsvM):
                    self.list_of_hist[6].Fill(ijet.pt,abs(ijet.eta))
                if(ijet.btagDeepB>DeepcsvT):
                    self.list_of_hist[7].Fill(ijet.pt,abs(ijet.eta))
	    else:
		self.list_of_hist[8].Fill(ijet.pt,abs(ijet.eta))
		if(ijet.btagDeepB>DeepcsvL):
                    self.list_of_hist[9].Fill(ijet.pt,abs(ijet.eta))
                if(ijet.btagDeepB>DeepcsvM):
                    self.list_of_hist[10].Fill(ijet.pt,abs(ijet.eta))
                if(ijet.btagDeepB>DeepcsvT):
                    self.list_of_hist[11].Fill(ijet.pt,abs(ijet.eta))
	
        return True

EfficiencyConstr_2016 = lambda : EfficiencyModule('2016',jetSelection= lambda j : j.pt > 20)
EfficiencyConstr_2017 = lambda : EfficiencyModule('2017',jetSelection= lambda j : j.pt > 20)
#preselection="Jet_pt > 200 && Entry$<500 "
#files=["root://cms-xrd-global.cern.ch///store/mc/RunIISummer16NanoAODv3/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/NANOAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/120000/E4046A1B-A2E1-E811-8878-0025905B85DC.root"]
#p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[EfficiencyModule()],noOut=True,histFileName="B_DeepCSV_Efficiency.root",histDirName="Tchanelbar")
#p.run()

