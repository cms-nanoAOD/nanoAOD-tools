import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class skipNRecoLeps(Module):
    def __init__(self):
        self.minelpt  = 18
        self.minmupt  = 18
        self.maxeleta = 2.5
        self.maxmueta = 2.5
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        #jets = Collection(event, 'Jet')
        elec = Collection(event, 'Electron')
        muon = Collection(event, 'Muon')

        nlepgood = 0
        for mu in muon:
          if mu.pt > self.minmupt and abs(mu.eta) < self.maxmueta and (mu.tightId or mu.mediumId): nlepgood += 1
        for el in elec:
          if el.pt > self.minelpt and abs(el.eta) < self.maxeleta and (el.cutBased >= 4): nlepgood += 1

        return nlepgood >= 2


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

skimRecoLeps = lambda : skipNRecoLeps()
 
