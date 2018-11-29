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
        multiplicities = range(0,5),
        globalOptions={"isData":False},
        saveAllLabels = False,
    ):
        self.globalOptions = globalOptions
        self.inputCollection = inputCollection
        self.outputName = outputName
        self.predictionLabels = predictionLabels
        self.logctauValues = logctauValues
        self.multiplicities = multiplicities
        self.logctauLabels = map(lambda ctau: getCtauLabel(ctau),logctauValues)
        self.taggerName = taggerName
        self.saveAllLabels = saveAllLabels
        
 
    def beginJob(self):
        pass
        
    def endJob(self):
        pass
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        for ctau in self.logctauValues:
            for label in self.predictionLabels:
                if self.saveAllLabels:
                    self.out.branch(self.outputName+"_"+getCtauLabel(ctau)+"_"+label,"F", lenVar="nJet")
                else:
                    for m in self.multiplicities:
                        self.out.branch(self.outputName+"_"+getCtauLabel(ctau)+"_"+label+"_min"+str(m),"F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = self.inputCollection(event)
        
        predictionsPerCtauAndClass = {ctau: {className: [] for className in self.predictionLabels} for ctau in self.logctauValues}
        for jet in jets:
            if not hasattr(jet,self.taggerName):
                print "WARNING - jet ",jet," has no ",self.taggerName," result stored -> skip"
                continue
            predictions = getattr(jet,self.taggerName)
            for ctau in self.logctauValues:
                for label in self.predictionLabels:
                    predictionsPerCtauAndClass[ctau][label].append(predictions[ctau][label])
        for ctau in self.logctauValues:
            for label in self.predictionLabels:
                predictionsPerCtauAndClass[ctau][label] = sorted(predictionsPerCtauAndClass[ctau][label],reverse=True)
                if self.saveAllLabels:
                    self.out.fillBranch(self.outputName+"_"+getCtauLabel(ctau)+"_"+label, predictionsPerCtauAndClass[ctau][label])
                else:

                    for m in self.multiplicities:
                        if m<len(predictionsPerCtauAndClass[ctau][label]):
                            self.out.fillBranch(self.outputName+"_"+getCtauLabel(ctau)+"_"+label+"_min"+str(m),predictionsPerCtauAndClass[ctau][label][m])
                        else:
                            self.out.fillBranch(self.outputName+"_"+getCtauLabel(ctau)+"_"+label+"_min"+str(m),0)

        return True
        
