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
        self.inputCollection = inputCollection
        self.outputName = outputName
 
    def beginJob(self):
        pass
        
    def endJob(self):
        pass
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        for feature in self.features:
            self.out.branch(self.outputName+"_"+feature,"F",lenVar="n"+self.outputName)
            
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        if self.globalOptions['isData']:
            return True
            
        jets = self.inputCollection(event)
        
        jetGlobal = Collection(event,"global")
        
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
        
        

        for ijet,jet in enumerate(jets):
            if jet._index<len(jetGlobal) and jet._index<len(jetOrigin):
                if math.fabs(jet.eta-jetGlobal[jet._index].eta)>0.01:
                    print "Warning - no proper match between jetorigin and nanoaod jets"
                    continue
                else:
                    
                    svoffset = 0
                    cpfoffset = 0
                    npfoffset = 0
                    for i in range(jet._index):
                        svoffset+=int(round(jetNSV[i].length))
                        cpfoffset+=int(round(jetNCPF[i].length))
                        npfoffset+=int(round(jetNNPF[i].length))
                    
                    
                    
                        
        
        return True
        
