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
    ):
        self.outputName = outputName
        self.inputCollection = inputCollection
 
    def beginJob(self):
        pass
        
    def endJob(self):
        pass
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
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

        selectedJets = []
        nsvs = []
        nnpfs = []
        ncpfs = []

        for ijet,jet in enumerate(jets):
            if jet.pt < 30.:
                continue
            selectedJets.append(jet)
            setattr(jet, "nsv", jetNSV[ijet].length)
            setattr(jet, "nnpf", jetNNPF[ijet].length)
            setattr(jet, "ncpf", jetNCPF[ijet].length)
            nsvs.append(jet.nsv)
            nnpfs.append(jet.nnpf)
            ncpfs.append(jet.ncpf)

        setattr(event, self.outputName, selectedJets)
                    
        return True
