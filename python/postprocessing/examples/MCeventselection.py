#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
#from importlib import import_module
#from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *

import math as m
from array import array



class eventProducer(Module):
	def __init__(self, jetSelection): #, jetSelection):
                self.jetSel = jetSelection
                self.puppimetBranchName= "PuppiMET"
                self.rawmetBranchName= "RawMET"
                self.pfmetBranchName= "MET"
                self.flagBranchName= "Flag"
                self.hltBranchName= "HLT"
		pass
	def beginJob(self):
                pass
        def endJob(self):
                pass
        def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
                self.out = wrappedOutputTree
                #self.out.branch("Photon_px","F");
                #self.out.branch("Photon_py","F");
                #self.out.branch("MET_px", "F");
                #self.out.branch("MET_py", "F");
                self.out.branch("Photon_px", "F");
                self.out.branch("Photon_py", "F");
                self.out.branch("Tight_Photon_pt_test", "F");
                self.out.branch("uparallel_PFMET", "F");
                self.out.branch("uparpendicular_PFMET", "F");
                self.out.branch("uparallel_RawMET", "F");
                self.out.branch("uparpendicular_RawMET", "F");
                self.out.branch("uparallel_PuppiMET", "F");
                self.out.branch("uparpendicular_PuppiMET", "F");
                self.out.branch("Tight_Photon_pt", "F");
                self.out.branch("Gen_pdgID", "I");
                self.out.branch("Gen_Photon_pt", "F");
        def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
                pass
	def analyze(self, event):
		photons = Collection(event, "Photon")
                gen = Collection(event, "GenPart")
        	jets = Collection(event, "Jet")
		electrons = Collection(event, "Electron")
		muons = Collection(event, "Muon")
                puppimet= Object(event, self.puppimetBranchName)
                rawmet= Object(event, self.rawmetBranchName)
                pfmet = Object(event, self.pfmetBranchName)
                flag= Object(event,self.flagBranchName)
                hlt= Object(event, self.hltBranchName)
                
		#select events with eaxctly one tight photon, at least one jet, no loose electron or muon
                tightjet = 0
		onetightphoton = 0
		looseelectron = 0
		loosemuon = 0
		for j in filter(self.jetSel,jets):
	            	if(j.jetId>1 and abs(j.eta) < 2.4 and j.pt > 40): tightjet += 1 #Jet ID flags bit1 is loose (always false in 2017), bit2 is tight, bit3 is tightLepVeto: jetId = Var("userInt('tightIdLepVeto')*4+userInt('tightId')*2+userInt('looseId')"
	       	tightpho = filter(lambda p : abs(p.eta) < 1.44 and p.pt > 50 and p.cutBasedBitmap==7, photons) #cut-based ID bitmap, Fall17 V1, 2^(0:loose, 1:medium, 2:tight) 
                if len(tightpho) == 1: onetightphoton += 1
		for ele in electrons:
	            if(ele.cutBased_Fall17_V1>2 and ele.pt > 10):  looseelectron += 1 #Int_t cut-based ID Fall17 V1 (0:fail, 1:veto, 2:loose, 3:medium, 4:tight) if(ele.cutBased_Fall17_V1==1):
		for mu in muons:
			 if(mu.looseId==1 and mu.pt > 10): loosemuon += 1 #Bool_t muon is loose muon if(mu.looseId==1):
                if( hlt.Photon50_R9Id90_HE10_IsoM ==1 or  hlt.Photon75_R9Id90_HE10_IsoM ==1 or hlt.Photon90_R9Id90_HE10_IsoM ==1 or hlt.Photon120_R9Id90_HE10_IsoM == 1 or hlt.Photon165_R9Id90_HE10_IsoM ==1): #Using the HLT Trigger 
                     if(tightjet >0 and onetightphoton > 0 and looseelectron == 0  and loosemuon == 0 and  flag.BadPFMuonFilter == 1 and flag.ecalBadCalibFilter == 1 and flag.globalTightHalo2016Filter == 1 and flag.HBHENoiseFilter==1 and flag.HBHENoiseIsoFilter ==1 and flag.EcalDeadCellTriggerPrimitiveFilter==1 and flag.eeBadScFilter==1): #Using Filter and photon and jet selection
                  	 photon_px= 0 
                         photon_py= 0 
                         Tight_Photon_pt= 0
                         for tp in tightpho:
                                photon_px= photon_px+tp.pt*m.cos(tp.phi)
                                photon_py= photon_py+tp.pt*m.sin(tp.phi)
                                Tight_Photon_pt= Tight_Photon_pt+tp.pt
                         pfmet_px= pfmet.pt*m.cos(pfmet.phi)
                         pfmet_py= pfmet.pt*m.sin(pfmet.phi)
                         #pfmet_px= shiftedPt(pat::MET::JetResUp)*m.cos(pfmet.phi)
                         puppimet_px= puppimet.pt*m.cos(puppimet.phi)
                         puppimet_py= puppimet.pt*m.sin(puppimet.phi)
                         rawmet_px= rawmet.pt*m.cos(rawmet.phi)
                         rawmet_py= rawmet.pt*m.sin(rawmet.phi)

                         #ux= -met_px-photon_px
                         #uy= -met_py-photon_py
                         uparpendicular_pf= ((-pfmet_px-photon_px)*photon_py-(-pfmet_py-photon_py)*photon_px)/tp.pt
                         uparallal_pf= ((-pfmet_px-photon_px)*photon_px+(-pfmet_py-photon_py)*photon_py)/tp.pt
                         uparpendicular_puppi= ((-puppimet_px-photon_px)*photon_py-(-puppimet_py-photon_py)*photon_px)/tp.pt
                         uparallal_puppi= ((-puppimet_px-photon_px)*photon_px+(-puppimet_py-photon_py)*photon_py)/tp.pt
                         uparpendicular_raw= ((-rawmet_px-photon_px)*photon_py-(-rawmet_py-photon_py)*photon_px)/tp.pt
                         uparallal_raw= ((-rawmet_px-photon_px)*photon_px+(-rawmet_py-photon_py)*photon_py)/tp.pt
                         
                         self.out.fillBranch("Photon_px", photon_px)
                         self.out.fillBranch("Photon_py", photon_py)
                         self.out.fillBranch("Tight_Photon_pt_test", tp.pt)
                         
                         self.out.fillBranch("uparallel_PFMET", uparallal_pf)
                         self.out.fillBranch("uparpendicular_PFMET", uparpendicular_pf)

			 self.out.fillBranch("uparallel_PuppiMET", uparallal_puppi)
                         self.out.fillBranch("uparpendicular_PuppiMET", uparpendicular_puppi)
 
                         self.out.fillBranch("uparallel_RawMET", uparallal_raw)
                         self.out.fillBranch("uparpendicular_RawMET", uparpendicular_raw)


                         self.out.fillBranch("Tight_Photon_pt", Tight_Photon_pt)
                         for g in gen:
                             if g.pdgId == 22:
                                 self.out.fillBranch("Gen_Photon_pt", g.pt)
                                 self.out.fillBranch("Gen_pdgID", g.pdgId)
                                 break
                   #self.Write()
	        	 return True
               # histFileName.Write()
#files=["root://cms-xrd-global.cern.ch//store/data/Run2018B/EGamma/NANOAOD/Nano1June2019-v1/40000/FF35DAD8-2E4B-0345-AFB7-CAA340AD0BC9.root"]
#p=PostProcessor(".",files,branchsel=None,modules=[eventselection()],maxEntries=10000,noOut=True,histFileName="histOut.root",histDirName="plots")
#p.run()

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
#eventselectionTest = lambda : eventProducer(hltSelection= lambda hlts : hlts.Photon50_R9Id90_HE10_IsoM==1 or hlts.Photon75_R9Id90_HE10_IsoM==1 or hlts.Photon90_R9Id90_HE10_IsoM==1 or hlts.Photon120_R9Id90_HE10_IsoM==1)
MCeventselectionTest = lambda : eventProducer(jetSelection= lambda j : j.pt>40)
