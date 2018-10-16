import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import itertools

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
        self.prescaleIdx += 1 
        #jets = Collection(event, 'Jet')
        elec = Collection(event, 'Electron')
        muon = Collection(event, 'Muon')

        goodElec = filter( lambda x : x.pt > self.minelpt and abs(x.eta) < self.maxeleta and x.mvaFall17noIso_WPL and x.sip3d < 8 , elec)
        goodMuon = filter( lambda x : x.pt > self.minmupt and abs(x.eta) < self.maxmueta and x.sip3d < 8, muon)

        nlepgood = len(goodElec+goodMuon)

        if nlepgood < 2: return False

        hasSS = False
        for l1,l2 in itertools.product(goodElec+goodMuon, goodElec+goodMuon):
            if l1==l2: continue
            if l1.charge*l2.charge > 0 : 
                hasSS=True; break

        if hasSS: 
            self.wrappedOutputTree.fillBranch('prescaleFromSkim', 1)
            return True
        else: 
            if self.prescaleIdx%self.prescaleFromSkim == 0:
                self.wrappedOutputTree.fillBranch('prescaleFromSkim', self.prescaleFromSkim)
                return True
            else:
                return False

            
            


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

skimRecoLeps = lambda : skipNRecoLeps()
 
