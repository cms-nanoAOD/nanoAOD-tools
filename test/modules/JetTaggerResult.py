import os
import sys
import math
import json
import ROOT
import random

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from utils import deltaR,getCtauLabel

class JetTaggerResult(Module):

    def __init__(
        self,
        inputCollection = lambda event: Collection(event, "Jet"),
        taggerName = "llpdnnx",
        outputName = "selectedJets",
        predictionLabels = ["B","C","UDS","G","LLP"],
        logctauValues = range(-3,5),
        globalOptions={"isData":False}
    ):
        self.globalOptions = globalOptions
        self.taggerName = taggerName
        self.outputName = outputName
        self.inputCollection = inputCollection
        self.predictionLabels = predictionLabels
        self.logctauValues = logctauValues
 
    def beginJob(self):
        pass
        
    def endJob(self):
        pass
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        for ctau in self.logctauValues:
            for label in self.predictionLabels:
                self.out.branch(self.outputName+"_"+self.taggerName+"_"+getCtauLabel(ctau)+"_"+label,"F",lenVar="n"+self.outputName)
        
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
            
        jets = self.inputCollection(event)
        
        taggerResults = {ctau: {className: [-1.]*len(jets) for className in self.predictionLabels} for ctau in self.logctauValues}
        for ijet,jet in enumerate(jets):
            if not hasattr(jet,self.taggerName):
                print "WARNING - jet ",jet," has no ",self.taggerName," result stored -> skip"
                continue
            predictions = getattr(jet,self.taggerName)
            for ctau in self.logctauValues:
                for label in self.predictionLabels:
                    taggerResults[ctau][label][ijet]=predictions[ctau][label]
                    
        for ctau in self.logctauValues:
            for label in self.predictionLabels:
                self.out.fillBranch(self.outputName+"_"+self.taggerName+"_"+getCtauLabel(ctau)+"_"+label,taggerResults[ctau][label])
        
        
        return True
        
