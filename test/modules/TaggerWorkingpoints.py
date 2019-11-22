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
        globalOptions={"isData":False}
    ):
        self.globalOptions = globalOptions
        self.inputCollection = inputCollection
        self.outputName = outputName
        self.predictionLabels = predictionLabels
        self.logctauValues = logctauValues
        self.multiplicities = multiplicities
        self.logctauLabels = map(lambda ctau: getCtauLabel(ctau),logctauValues)
        self.taggerName = taggerName

        self.thresholds = {      
            -3: 0.37245617939,
            -2: 0.368606702814,
            -1: 0.343856976757,
            0: 0.436759756336,
            1: 0.557319806347,
            2: 0.64487092329,
            3: 0.565088437328,
            4: 0.590826915035
        }
        
 
    def beginJob(self):
        pass
        
    def endJob(self):
        pass
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        for ctau in self.logctauValues:
            for label in self.predictionLabels:
                for m in self.multiplicities:
                    self.out.branch(self.outputName+"_"+getCtauLabel(ctau)+"_"+label+"_min"+str(m),"F")
            if not self.globalOptions["isData"]:
                for label in ["LLP"]:
                    self.out.branch(self.outputName+"_"+getCtauLabel(ctau)+"_n"+label+"True","I")
                    self.out.branch(self.outputName+"_"+getCtauLabel(ctau)+"_n"+label+"TrueTaggedLLP","I")
                    
                if self.saveAllLabels:
                    self.out.branch(self.outputName+"_"+getCtauLabel(ctau)+"_"+label,"F", lenVar="nselectedJets")

                for m in self.multiplicities:
                    self.out.branch(self.outputName+"_"+getCtauLabel(ctau)+"_"+label+"_min"+str(m),"F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = self.inputCollection(event)
        
        predictionsPerCtauAndClass = {ctau: {className: [] for className in self.predictionLabels} for ctau in self.logctauValues}
        for ijet,jet in enumerate(jets):
            if not hasattr(jet,self.taggerName):
                print "WARNING - jet ",jet," has no ",self.taggerName," result stored -> skip"
                continue
            predictions = getattr(jet,self.taggerName)
            for ctau in self.logctauValues:
                for label in self.predictionLabels:
                    predictionsPerCtauAndClass[ctau][label].append(predictions[ctau][label])
                    
        if not self.globalOptions["isData"]:
            for ctau in self.logctauValues:
                nTrue = {}
                nTrueTaggedLLP = {}
                for label in ["B","C","UDS","G","LLP","PU"]:
                    nTrue[label] = 0
                    nTrueTaggedLLP[label] = 0
                for jet in jets:
                    if not hasattr(jet,self.taggerName):
                        continue
                    #print jet.__dict__.keys()
                    predictions = getattr(jet,self.taggerName)
                    for label in ["B","C","UDS","G","LLP","PU"]:
                        if hasattr(jet,"is"+label) and getattr(jet,"is"+label):
                            nTrue[label]+=1
                            if predictions[ctau]['LLP']>self.thresholds[ctau]:
                                nTrueTaggedLLP[label]+=1
                #print ctau,nTrue,nTrueTagged
                
        for ctau in self.logctauValues:
            for label in self.predictionLabels:

                predictionsPerCtauAndClass[ctau][label] = sorted(predictionsPerCtauAndClass[ctau][label],reverse=True)

                for m in self.multiplicities:
                    if m<len(predictionsPerCtauAndClass[ctau][label]):
                        self.out.fillBranch(self.outputName+"_"+getCtauLabel(ctau)+"_"+label+"_min"+str(m),predictionsPerCtauAndClass[ctau][label][m])
                    else:
                        self.out.fillBranch(self.outputName+"_"+getCtauLabel(ctau)+"_"+label+"_min"+str(m),0)

            if not self.globalOptions["isData"]:
                 for label in ["LLP"]:
                    self.out.fillBranch(self.outputName+"_"+getCtauLabel(ctau)+"_n"+label+"True",nTrue[label])
                    self.out.fillBranch(self.outputName+"_"+getCtauLabel(ctau)+"_n"+label+"TrueTaggedLLP",nTrueTaggedLLP[label])
                        
                    
        for ctau in self.logctauValues:
            for label in self.predictionLabels:
                predictionsPerCtauAndClass[ctau][label] = sorted(predictionsPerCtauAndClass[ctau][label],reverse=True)
                for m in self.multiplicities:
                    if m<len(predictionsPerCtauAndClass[ctau][label]):
                        self.out.fillBranch(self.outputName+"_"+getCtauLabel(ctau)+"_"+label+"_min"+str(m),predictionsPerCtauAndClass[ctau][label][m])
                    else:
                        self.out.fillBranch(self.outputName+"_"+getCtauLabel(ctau)+"_"+label+"_min"+str(m),0)
        
        return True
