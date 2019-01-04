#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor


from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class Analysis(Module):
    def __init__(self):
	self.writeHistFile=True

    def beginJob(self,histFile=None,histDirName=None):
	Module.beginJob(self,histFile,histDirName)

	self.h_vpt=ROOT.TH1F('sumpt',   'sumpt',   100, 0, 1000)
        self.addObject(self.h_vpt )

    def analyze(self, event):
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        eventSum = ROOT.TLorentzVector()

	#select events with at least 2 muons
	if len(muons) >=2 :
	  for lep in muons :     #loop on muons
            eventSum += lep.p4()
          for lep in electrons : #loop on electrons
            eventSum += lep.p4()
          for j in jets :       #loop on jets
            eventSum += j.p4()
          self.h_vpt.Fill(eventSum.Pt()) #fill histogram

        return True

preselection="Jet_pt[0] > 250"
files=[" root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/2CE738F9-C212-E811-BD0E-EC0D9A8222CE.root"]
p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[Analysis()],noOut=True,histFileName="histOut.root",histDirName="plots")
p.run()
