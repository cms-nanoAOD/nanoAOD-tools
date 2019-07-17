import os
import sys
import math
import json
import ROOT
import random

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from utils import deltaR

class JetFeatures(Module):

    def __init__(
        self,
        inputCollection = lambda event: Collection(event, "Jet"),
        outputName = "selectedJets",
        features=[
            
        ],
        globalOptions={"isData":False}
    ):
        self.globalOptions = globalOptions
        self.features = features
        self.outputName = outputName
        self.inputCollection = inputCollection
 
    def beginJob(self):
        pass
        
    def endJob(self):
        pass
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        self.out.branch(self.outputName+"_nsv","F",lenVar="n"+self.outputName)
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
            
        jets = self.inputCollection(event)
        jetGlobal = Collection(event,"global")
        jetOrigin = Collection(event,"jetorigin")
        
        jetNSV = Collection(event,"svlength")
        jetSV = Collection(event,"sv")
        
        jetNCPF = Collection(event,"cpflength")
        jetCPF = Collection(event,"cpf")
        
        jetNNPF = Collection(event,"npflength")
        jetNPF = Collection(event,"npf")

        #allocate output
        jetFeatures = {}
        for feature in self.features:
            jetFeatures[feature] = [0 for _ in range(len(jets))]

        selectedJets = []
        nsvs = []

        for ijet,jet in enumerate(jets):
            if jet.pt < 30.:
                continue
            selectedJets.append(jet)
            setattr(jet, "nsv", jetNSV[ijet].length)
            nsvs.append(jet.nsv)

        self.out.fillBranch(self.outputName+"_nsv", nsvs)
        setattr(event, self.outputName, selectedJets)
                    
        return True
