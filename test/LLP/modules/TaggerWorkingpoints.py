import os
import sys
import math
import json
import ROOT
import random

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from utils import deltaR,getCtauLabel

class TaggerWorkingpoints(Module):

    def __init__(
        self,
        inputCollection = lambda event: Collection(event, "Jet"),
        taggerName = "llpdnnx",
        outputName = "llpdnnx",
        predictionLabels = ["B","C","UDS","G","LLP"],
        logctauValues = range(-3,5),
        globalOptions={"isData":False}
    ):
        self.globalOptions = globalOptions
        self.inputCollection = inputCollection
        self.outputName = outputName
        self.predictionLabels = predictionLabels
        self.logctauValues = logctauValues
        self.logctauLabels = map(lambda ctau: getCtauLabel(ctau),logctauValues)
        self.taggerName = taggerName
 
    def beginJob(self):
        pass
        
    def endJob(self):
        pass
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        for ctau in self.logctauValues:
            for label in self.predictionLabels:
                self.out.branch(self.outputName+"_"+getCtauLabel(ctau)+"_"+label+"_max","F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = self.inputCollection(event)
        
        maxPredictions = {ctau: {className: 0. for className in self.predictionLabels} for ctau in self.logctauValues}
        for jet in jets:
            if not hasattr(jet,self.taggerName):
                print "WARNING - jet ",jet," has no ",self.taggerName," result stored -> skip"
                continue
            predictions = getattr(jet,self.taggerName)
            for ctau in self.logctauValues:
                for label in self.predictionLabels:
                    maxPredictions[ctau][label]=max(maxPredictions[ctau][label],predictions[ctau][label])
        for ctau in self.logctauValues:
            for label in self.predictionLabels:
                self.out.fillBranch(self.outputName+"_"+getCtauLabel(ctau)+"_"+label+"_max",maxPredictions[ctau][label])
        
        return True
        
