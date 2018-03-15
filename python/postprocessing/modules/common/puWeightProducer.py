import ROOT
import os
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class puWeightProducer(Module):
    def __init__(self,myfile,targetfile,myhist="pileup",targethist="pileup",name="puWeight",norm=True,verbose=False,nvtx_var="Pileup_nTrueInt"):
        self.targeth = self.loadHisto(targetfile,targethist)
        self.fixLargeWeights = True
	if myfile != "auto" :
		self.autoPU=False
	        self.myh = self.loadHisto(myfile,myhist)
	else :
        	self.fixLargeWeights = False #AR: it seems to crash with it, to be deugged
		self.autoPU=True
		ROOT.gROOT.cd()
		self.myh=self.targeth.Clone("autoPU")
		self.myh.Reset()
        self.name = name
        self.norm = norm
        self.verbose = verbose
        self.nvtxVar = nvtx_var
       
        #Try to load module via python dictionaries
        try:
            ROOT.gSystem.Load("libPhysicsToolsNanoAODTools")
            dummy = ROOT.WeightCalculatorFromHistogram
        #Load it via ROOT ACLIC. NB: this creates the object file in the CMSSW directory,
        #causing problems if many jobs are working from the same CMSSW directory
        except Exception as e:
            print "Could not load module via python, trying via ROOT", e
            if "/WeightCalculatorFromHistogram_cc.so" not in ROOT.gSystem.GetLibraries():
                print "Load C++ Worker"
                ROOT.gROOT.ProcessLine(".L %s/src/PhysicsTools/NanoAODTools/src/WeightCalculatorFromHistogram.cc++" % os.environ['CMSSW_BASE'])
            dummy = ROOT.WeightCalculatorFromHistogram
    def loadHisto(self,filename,hname):
        tf = ROOT.TFile.Open(filename)
        hist = tf.Get(hname)
        hist.SetDirectory(None)
        tf.Close()
        return hist
    def beginJob(self):
	pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
	if self.autoPU :
                self.myh.Reset()
		print "Computing PU profile for this file"
		ROOT.gROOT.cd()
		inputFile.Get("Events").Project("autoPU",self.nvtxVar)#doitfrom inputFile
		if outputFile : 
		    outputFile.cd()
		    self.myh.Write()    
        self._worker = ROOT.WeightCalculatorFromHistogram(self.myh,self.targeth,self.norm,self.fixLargeWeights,self.verbose)
        self.out = wrappedOutputTree
        self.out.branch(self.name, "F")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        if hasattr(event,self.nvtxVar):
            nvtx = int(getattr(event,self.nvtxVar))
            weight = self._worker.getWeight(nvtx) if nvtx < self.myh.GetNbinsX() else 1
        else: weight = 1
        self.out.fillBranch(self.name,weight)
        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

pufile_mc="%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/pileup_profile_Summer16.root" % os.environ['CMSSW_BASE']
pufile_data="%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/PileupData_GoldenJSON_Full2016.root" % os.environ['CMSSW_BASE']
puWeight = lambda : puWeightProducer(pufile_mc,pufile_data,"pu_mc","pileup",verbose=False)

pufile_data2017="%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/Run2017-example.root" % os.environ['CMSSW_BASE']
puAutoWeight = lambda : puWeightProducer("auto",pufile_data2017,"pu_mc","pileup",verbose=False)
