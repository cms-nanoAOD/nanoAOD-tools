#!/usr/bin/env python
import os, sys
import ROOT
from math import fabs, cos, sin, tan, atan, exp, sqrt
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.operational.cleaningStudy import cleaningStudy
#import PhysicsTools.NanoAODTools.postprocessing.operational.cleaningStudy

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi, deltaR

class signalAnalysis(Module):
    def __init__(self):
	self.writeHistFile=True
        self.Genpart = False
        self.Nevents = 0

    def beginJob(self,histFile=None,histDirName=None):
	Module.beginJob(self,histFile,histDirName)
        VAR=[]
        self.h_nevent=ROOT.TH1D('nevent', 'nevent', 10, 0, 1000); VAR.append(self.h_vpt)
	self.h_vpt=ROOT.TH1F('sumpt',   'sumpt',   100, 0, 1000); VAR.append(self.h_vpt)
        
        

        self.addObject(self.h_vpt )
        #self.h_Ncj=ROOT.TH1D('NcleanJet',   'NcleanJet',   10, 0, 10)
        #self.addObject(self.h_Ncj )
        
    def analyze(self, event):
        #eventSum = ROOT.TLorentzVector()

        #READ Collection
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        genparts = Collection(event, "GenPart")

        #READ Vector
        JetE= Object(event,"JetE")
        dRMuJet= Object(event,"dRMuJet")
        dRElJet= Object(event,"dRElJet")

        #READ Scalar
        nGoodJet= event.nGoodJet
        nGoodMuon= event.nGoodMuon
        nGoodElectron= event.nGoodElectron
        nGoodTau= event.nGoodTau
        nGoodPhoton= event.nGoodPhoton

        isOSmumu= event.isOSmumu
        isOSemu= event.isOSemu
        isSSmumu= event.isSSmumu

        HTpt= event.HTpt
        HTphi= event.HTphi
        Zweight= event.Zweight
        
        #select events with at least 2 muons
	#if len(muons) >=2 :
	#  for lep in muons :     #loop on muons
        #    eventSum += lep.p4()
        #  for lep in electrons : #loop on electrons
        #    eventSum += lep.p4()
        #  for j in jets :       #loop on jets
        #    eventSum += j.p4()
        #  self.h_vpt.Fill(eventSum.Pt()) #fill histogram

        # Cleaning Jet

        # HT Computation
        HTpt=0.
        HTphi=0.
        for num, jet in enumerate(jets):
            #if jet.puId==4: continue
            if jet.Clean==0: continue
            if jet.pt<30.: continue # taken at 30 GeV                                                                                                                                 
            if fabs(jet.eta)>2.5: continue
            HTpt+=jet.pt
            HTphi+=jet.phi

        #self.h_Ncj.Fill(nGoodJet)
        self.h_vpt.Fill(HTpt)
        return True


preselection=""
skimmed_files=[]

files=["/Users/shoh/Projects/CMS/PhD/Analysis/SSl/NANOAOD/HWplusJ_HToWW_M125_13TeV_powheg_pythia8-v1.root",
       "/Users/shoh/Projects/CMS/PhD/Analysis/SSl/NANOAOD/HWminusJ_HToWW_M125_13TeV_powheg_pythia8-v1.root"]

for f in files:
    skimmed_files.append(f.split("/")[-1].split(".")[0]+"_Skim.root")
    
mod=import_module('PhysicsTools.NanoAODTools.postprocessing.operational.cleaningStudy')
obj = sys.modules['PhysicsTools.NanoAODTools.postprocessing.operational.cleaningStudy']
nevent=30000

#Producer=PostProcessor(".",files,cut=preselection,branchsel="keep_and_drop_VH.txt",modules=[getattr(obj,'cleaning')()],maxevent=nevent)
Analyzer=PostProcessor(".",skimmed_files,cut=preselection,branchsel=None,modules=[signalAnalysis()],maxevent=nevent,noOut=True,histFileName="VH.root",histDirName="plots")

#for p in [Producer,Analyzer]:
for p in [Analyzer]:
    print "Running ", p
    p.run()
