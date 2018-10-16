import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class skipNRecoLeps(Module):
    def __init__(self):
        self.minelpt  = 10
        self.minmupt  = 10
        self.maxeleta = 2.5
        self.maxmueta = 2.5
        self.prescaleIdx = -1
        self.prescaleFromSkim = 5

    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.wrappedOutputTree = wrappedOutputTree
        self.wrappedOutputTree.branch('prescaleFromSkim','F')

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):

        elec = Collection(event, 'Electron')
        muon = Collection(event, 'Muon')

        isoAndIDCuts = lambda  x : x.miniPFRelIso_all < 0.1  and x.dxy < 0.05 and x.dz < 0.1 and x.sip3d < 8 

        goodElec = filter( lambda x : x.pt > self.minelpt and abs(x.eta) < self.maxeleta and x.mvaFall17noIso_WPL and isoAndIDCuts(x) , elec)
        goodMuon = filter( lambda x : x.pt > self.minmupt and abs(x.eta) < self.maxmueta  and x.tightId and isoAndIDCuts(x), muon)

        nlepgood = len(goodElec+goodMuon)

        return nlepgood >1 
            
            


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

skimRecoLeps = lambda : skipNRecoLeps()
 
