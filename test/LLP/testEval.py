import os
import sys
import math
import ROOT
import random
import numpy
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

if (ROOT.gSystem.Load("libPhysicsToolsNanoAODTools.so")!=0):
    print "Cannot load 'libPhysicsToolsNanoAODTools'"
    sys.exit(1)


#load dynamically from file
featureDict = import_module('feature_dict').featureDict


class exampleProducer(Module):
    def __init__(self):
        pass
        
    def beginJob(self):
        self.nEvents = 0
        self.nLLP = {
            -3:[0,0],
            0:[0,0],
            3:[0,0],
        }
        
    def endJob(self):
        for ctau_value in self.nLLP.keys(): 
            print ctau_value,100.*self.nLLP[ctau_value][0]/(self.nLLP[ctau_value][0]+self.nLLP[ctau_value][1])
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.setupEval(inputTree)
        
        
    def setupEval(self,tree):
        self.tfEval = ROOT.TFEval()
        if (not self.tfEval.loadGraph("model_epoch.pb")):
            sys.exit(1)
            
        self.tfEval.addOutputNodeName("prediction")
            
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
                    print " + add feature: ",branchName
                    featureGroup.addFeature(ROOT.TFEval.BranchAccessor(tree.arrayReader(branchName)))
                self.tfEval.addFeatureGroup(featureGroup)
            else:
                print "building group ... %s, shape=[%i]"%(groupName,len(featureCfg["branches"]))
                featureGroup = ROOT.TFEval.ValueFeatureGroup(
                    groupName,
                    len(featureCfg["branches"])
                )
                for branchName in featureCfg["branches"]:
                    print " + add feature: ",branchName
                    featureGroup.addFeature(ROOT.TFEval.BranchAccessor(tree.arrayReader(branchName)))
                self.tfEval.addFeatureGroup(featureGroup)
                
        genFeatureGroup = ROOT.TFEval.ValueFeatureGroup("gen",1)
        self.nJets = 0
        self.logctau = 0
        genFeatureGroup.addFeature(ROOT.TFEval.PyAccessor(lambda: self.nJets, lambda x: self.logctau))
        self.tfEval.addFeatureGroup(genFeatureGroup)
        
        self._ttreereaderversion = tree._ttreereaderversion
        
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        
        jets = Collection(event, "Jet")
        jetorigin = Collection(event, "jetorigin")
        
        for ijet in range(len(jetorigin)):
            if jetorigin[ijet].fromLLP>0.5 and jets[ijet].pt>20 and math.fabs(jets[ijet].eta)<2.4:
                
                
                #NOTE: one cannot access any other branches between setup & call to evaluate
                if event._tree._ttreereaderversion > self._ttreereaderversion:
                    self.setupEval(event._tree)
                    
                self.nJets = len(jets)
                #print ijet,":",
                for ctau_value in self.nLLP.keys():
                    
                    self.logctau = 1.*ctau_value
                    result = self.tfEval.evaluate(ijet)
                    prediction = result.get("prediction")
                    predicted_class = numpy.argmax(prediction)
                    if predicted_class==4:
                        self.nLLP[ctau_value][0]+=1
                    else:
                        self.nLLP[ctau_value][1]+=1
                    #print predicted_class, #index 4 is LLP class
                #print
        
        return True
        
     
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--isData', dest='isData', action='store_true',default=False)
parser.add_argument('--input', dest='inputFiles', action='append',default=[])
parser.add_argument('output', nargs=1)

args = parser.parse_args()

print "isData:",args.isData
print "inputs:",len(args.inputFiles)
for inputFile in args.inputFiles:
    rootFile = ROOT.TFile.Open(inputFile)
    if not rootFile:
        print "CRITICAL - file '"+inputFile+"' not found!"
        sys.exit(1)
    tree = rootFile.Get("Events")
    if not tree:
        print "CRITICAL - 'Events' tree not found in file '"+inputFile+"'!"
        sys.exit(1)
    print " - ",inputFile,", events=",tree.GetEntries()
    
print "output directory:",args.output[0]

p=PostProcessor('.',[args.inputFiles],cut=None,branchsel=None,modules=[
    exampleProducer()
],friend=True)
p.run()


