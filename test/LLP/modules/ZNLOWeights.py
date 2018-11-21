import os
import sys
import math
import json
import ROOT
import random

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class ZNLOWeights(Module):
    def __init__(self):
        self.weightFile = os.path.expandvars("$CMSSW_BASE/src/PhysicsTools/NanoAODTools/data/zboson/dynlo.root")
        
    def beginJob(self):
        f = ROOT.TFile.Open(self.weightFile)
        self.weightHist = f.Get("weight").Clone("weight"+str(random.random()))
        self.weightHist.SetDirectory(0)
        f.Close()
 
    def endJob(self):
        pass
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("znloweight_nominal","F")
        self.out.branch("znloweight_up","F")
        self.out.branch("znloweight_down","F")
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def analyze(self, event):
        w = 1.
        wUp = 1.
        wDown = 1.
        if event.LHE_HTIncoming>100.:
            ibin = self.weightHist.GetXaxis().FindBin(event.LHE_Vpt)
            if ibin<=1:
                ibin=1
            if ibin>=self.weightHist.GetNbinsX():
                ibin=self.weightHist.GetNbinsX()
            w = self.weightHist.GetBinContent(ibin)
            wUp = w+self.weightHist.GetBinError(ibin)
            wDown = w-self.weightHist.GetBinError(ibin)
        
        self.out.fillBranch("znloweight_nominal",w)
        self.out.fillBranch("znloweight_up",wUp)
        self.out.fillBranch("znloweight_down",wDown)
        return True
