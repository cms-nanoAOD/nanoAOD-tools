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
                self.out.branch("diele_mass", "F");
                self.out.branch("ele_px", "F");
                self.out.branch("ele_py", "F");
                self.out.branch("uparallel_PFMET", "F");
                self.out.branch("uparpendicular_PFMET", "F");
                self.out.branch("uparallel_RawMET", "F");
                self.out.branch("uparpendicular_RawMET", "F");
                self.out.branch("uparallel_PuppiMET", "F");
                self.out.branch("uparpendicular_PuppiMET", "F");
                #self.out.branch("Gen_pdgID", "I");
                #self.out.branch("Gen_ele_pt", "F");
        def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
                pass
	def analyze(self, event):
        	jets = Collection(event, "Jet")
		electrons = Collection(event, "Electron")
		muons = Collection(event, "Muon")
                puppimet= Object(event, self.puppimetBranchName)
                rawmet= Object(event, self.rawmetBranchName)
                pfmet = Object(event, self.pfmetBranchName)
                flag= Object(event,self.flagBranchName)
                hlt= Object(event, self.hltBranchName)
                tightjet= 0 
                ele_count1 = 0
                ele_count2 = 0                
		#select events with eaxctly one tight photon, at least one jet, no loose electron or muon
                #print("Event")                
                for j in filter(self.jetSel,jets):
                     if(j.jetId>1 and abs(j.eta) < 2.5 ): tightjet += 1
                ele1  =filter(lambda e1 : abs(e1.eta) < 1.44  and e1.pt > 10 and e1.cutBased_Fall17_V1>1 and e1.charge == -1, electrons)
                if len(ele1) == 1: ele_count1 +=1 
                ele2  =filter(lambda e2 : abs(e2.eta) < 1.44  and e2.pt > 10 and e2.cutBased_Fall17_V1>1 and e2.charge == 1, electrons)
                if len(ele2) == 1: ele_count2 +=1
                if(hlt.Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ == 1):
                    if(tightjet >0 and ele_count1 > 0 and ele_count2 > 0 and flag.BadPFMuonFilter == 1 and flag.ecalBadCalibFilter == 1 and flag.globalTightHalo2016Filter == 1 and flag.HBHENoiseFilter==1 and flag.HBHENoiseIsoFilter ==1 and flag.EcalDeadCellTriggerPrimitiveFilter==1 and flag.eeBadScFilter==1):     
                       ele_px= 9999
                       ele_py= 9999
                       eeMass= 9999
                       for electron1 in ele1: 
                         for electron2 in ele2: 
                            temp_Mass = m.sqrt(2.0*electron1.pt*electron2.pt*(m.cosh(electron1.eta - electron2.eta) - m.cos(electron1.phi - electron2.phi)))
                            if (temp_Mass > 81 and temp_Mass < 101):
                               eeMass = temp_Mass   
                               ele_px= electron1.pt*m.cos(electron1.phi) + electron2.pt*m.cos(electron2.phi) 
                               ele_py= electron1.pt*m.sin(electron1.phi) + electron2.pt*m.sin(electron2.phi)
                       diEMass = eeMass
                       ele_pt = m.sqrt(ele_px*ele_px + ele_py*ele_py)
                       pfmet_px= pfmet.pt*m.cos(pfmet.phi)
                       pfmet_py= pfmet.pt*m.sin(pfmet.phi)
                       puppimet_px= puppimet.pt*m.cos(puppimet.phi)
                       puppimet_py= puppimet.pt*m.sin(puppimet.phi)
                       rawmet_px= rawmet.pt*m.cos(rawmet.phi)
                       rawmet_py= rawmet.pt*m.sin(rawmet.phi)

                       uparpendicular_pf= ((-pfmet_px-ele_px)*ele_py-(-pfmet_py-ele_py)*ele_px)/ele_pt
                       uparallal_pf= ((-pfmet_px-ele_px)*ele_px+(-pfmet_py-ele_py)*ele_py)/ele_pt
                       uparpendicular_puppi= ((-puppimet_px-ele_px)*ele_py-(-puppimet_py-ele_py)*ele_px)/ele_pt
                       uparallal_puppi= ((-puppimet_px-ele_px)*ele_px+(-puppimet_py-ele_py)*ele_py)/ele_pt
                       uparpendicular_raw= ((-rawmet_px-ele_px)*ele_py-(-rawmet_py-ele_py)*ele_px)/ele_pt
                       uparallal_raw= ((-rawmet_px-ele_px)*ele_px+(-rawmet_py-ele_py)*ele_py)/ele_pt


                       self.out.fillBranch("diele_mass", diEMass)
                       self.out.fillBranch("ele_px", ele_px)
                       self.out.fillBranch("ele_py", ele_py)

                       self.out.fillBranch("uparallel_PFMET", uparallal_pf)
                       self.out.fillBranch("uparpendicular_PFMET", uparpendicular_pf)

                       self.out.fillBranch("uparallel_PuppiMET", uparallal_puppi)
                       self.out.fillBranch("uparpendicular_PuppiMET", uparpendicular_puppi)
                       self.out.fillBranch("uparallel_RawMET", uparallal_raw)
                       self.out.fillBranch("uparpendicular_RawMET", uparpendicular_raw)
                
                       #for g in gen:
                       # if abs(g.pdgId) == 11:
                       #       self.out.fillBranch("Gen_ele_pt", g.pt)
                       #       self.out.fillBranch("Gen_pdgID", g.pdgId)
                       #       break
                   #self.Write()
                       return True
                                           
#files=["root://cms-xrd-global.cern.ch//store/data/Run2018B/EGamma/NANOAOD/Nano1June2019-v1/40000/FF35DAD8-2E4B-0345-AFB7-CAA340AD0BC9.root"]
#p=PostProcessor(".",files,branchsel=None,modules=[eventselection()],maxEntries=10000,noOut=True,histFileName="histOut.root",histDirName="plots")
#p.run()

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
#eventselectionTest = lambda : eventProducer(hltSelection= lambda hlts : hlts.Photon50_R9Id90_HE10_IsoM==1 or hlts.Photon75_R9Id90_HE10_IsoM==1 or hlts.Photon90_R9Id90_HE10_IsoM==1 or hlts.Photon120_R9Id90_HE10_IsoM==1)
ZToeeTest = lambda : eventProducer(jetSelection= lambda j : j.pt>40)
