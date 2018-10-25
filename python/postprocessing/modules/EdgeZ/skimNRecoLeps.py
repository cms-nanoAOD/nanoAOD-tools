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

        lep = Collection(event, 'LepGood')
        print lep
        return len(lep) >1 
            
            


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

skimRecoLeps = lambda : skipNRecoLeps()
 
