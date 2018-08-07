import os
import sys
import math
import json
import ROOT
import random
import numpy
import time
from importlib import import_module

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

if (ROOT.gSystem.Load("libPhysicsToolsNanoAODTools.so")!=0):
    print "Cannot load 'libPhysicsToolsNanoAODTools'"
    sys.exit(1)

class TaggerEvaluation(Module):

    def __init__(
        self,
        modelPath,
        inputCollections = [lambda event: Collection(event, "Jet")],
        outputName = "llpdnnx",
        predictionLabels = ["B","C","UDS","G","LLP"],
        logctauValues = range(-3,5),#[0],
        globalOptions={"isData":False}
    ):
        self.globalOptions = globalOptions
        self.inputCollections = inputCollections
        self.ctauLabels = []
        self.predictionLabels = predictionLabels
        for ctauValue in logctauValues:
            if ctauValue==0:
                self.ctauLabels.append("0")
            elif ctauValue>0:
                self.ctauLabels.append("1"+(("0")*ctauValue))
            elif ctauValue<0:
                self.ctauLabels.append("0p"+(("0")*(ctauValue-1))+"1")
        self.logctau = numpy.array(logctauValues,dtype=numpy.float32)
        
        self.modelPath = modelPath
        self.outputName = outputName
 
    def beginJob(self):
        pass
        
    def endJob(self):
        pass
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.setup(inputTree)
        
    def setupTFEval(self,tree,modelFile,featureDict):
        tfEval = ROOT.TFEval()
        if (not tfEval.loadGraph(modelFile)):
            sys.exit(1)
            
        tfEval.addOutputNodeName("prediction")
        print "--- Model: ",modelFile," ---"
        for groupName,featureCfg in featureDict.iteritems():
            if featureCfg.has_key("max"):
                print "building group ... %s, shape=[%i,%i]"%(groupName,featureCfg["max"],len(featureCfg["branches"]))
                lengthBranch = ROOT.TFEval.BranchAccessor(tree.arrayReader(featureCfg["length"]))
                featureGroup = ROOT.TFEval.ArrayFeatureGroup(
                    groupName,
                    len(featureCfg["branches"]),
                    featureCfg["max"],
                    lengthBranch
                )
                for branchName in featureCfg["branches"]:
                    #print " + add feature: ",branchName
                    featureGroup.addFeature(ROOT.TFEval.BranchAccessor(tree.arrayReader(branchName)))
                tfEval.addFeatureGroup(featureGroup)
            else:
                print "building group ... %s, shape=[%i]"%(groupName,len(featureCfg["branches"]))
                featureGroup = ROOT.TFEval.ValueFeatureGroup(
                    groupName,
                    len(featureCfg["branches"])
                )
                for branchName in featureCfg["branches"]:
                    #print " + add feature: ",branchName
                    featureGroup.addFeature(ROOT.TFEval.BranchAccessor(tree.arrayReader(branchName)))
                tfEval.addFeatureGroup(featureGroup)
                
        return tfEval
        
    def setup(self,tree):
        #load dynamically from file
        featureDict = import_module('feature_dict').featureDict
        self.tfEvalParametric = self.setupTFEval(tree,self.modelPath,featureDict)
        
        genFeatureGroup = ROOT.TFEval.ValueFeatureGroup("gen",1)
        self.nJets = 0
        genFeatureGroup.addFeature(ROOT.TFEval.PyAccessor(lambda: self.nJets, lambda jetIndex,batchIndex: self.logctau[batchIndex%len(self.logctau)]))
        self.tfEvalParametric.addFeatureGroup(genFeatureGroup)
        
        self._ttreereaderversion = tree._ttreereaderversion
        
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def analyze(self, event):
        jetorigin = Collection(event, "jetorigin")
        
        jetIndexMapPerCollection = [] #maps indices back to jets in collections
        jetOriginIndices = set() #superset of all indices to evaluate
        
        
        for jetCollection in self.inputCollections:
            jets = jetCollection(event)
            jetIndexMap = {}
            for ijet,jet in enumerate(jets):
                if jet._index>=len(jetorigin):
                    #this is very strange - why has it not been filled?
                    continue
                jetOriginIndices.add(jet._index)
                jetIndexMap[ijet] = jet._index
            jetIndexMapPerCollection.append(jetIndexMap)
            
        jetOriginIndices = list(jetOriginIndices)
        
        evaluationIndices = []
        for index in jetOriginIndices:
            evaluationIndices.extend([index]*len(self.logctau))
                
        if event._tree._ttreereaderversion > self._ttreereaderversion:
            self.setup(event._tree)
            
        self.nJets = len(jetorigin)
        if len(jetOriginIndices)==0:
            return True
            
        evaluationIndices = numpy.array(evaluationIndices,numpy.int64)
            
        #print evaluationIndices,len(evaluationIndices)
        result = self.tfEvalParametric.evaluate(
            evaluationIndices.shape[0],
            evaluationIndices
        )
        
        for icollection,jetMap in enumerate(jetIndexMapPerCollection):
            for ijet,originJetIndex in jetMap.iteritems():
                jet = self.inputCollections[icollection](event)[ijet]
                
                for ictau in range(len(self.logctau)):
                    outputPosition = jetOriginIndices.index(originJetIndex)*len(self.logctau)+ictau
                    if outputPosition<0:
                        print "Error - position should not be < 0"
                        sys.exit(1)
                    prediction = result.get("prediction",outputPosition)
                    for iclass, classLabel in enumerate(self.predictionLabels):
                        setattr(jet,self.ctauLabels[ictau]+"_"+classLabel,prediction[iclass])
        
       
        
        return True
