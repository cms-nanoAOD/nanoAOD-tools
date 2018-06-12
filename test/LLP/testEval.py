import os
import sys
import math
import ROOT
import random
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

if (ROOT.gSystem.Load("libPhysicsToolsNanoAODTools.so")!=0):
    print "Cannot load 'libPhysicsToolsNanoAODTools'"
    sys.exit(1)

class exampleProducer(Module):
    def __init__(self):
        pass
        
    def beginJob(self):
        pass
        
    def endJob(self):
        pass
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree

        self.setupEval(inputTree)
        
        
    def setupEval(self,tree):
        self.tfEval = ROOT.TFEval()
        globalFeatures = ROOT.TFEval.ValueFeatureGroup("globalvars",2)
        globalFeatures.addFeature(tree.arrayReader("global_pt"))
        globalFeatures.addFeature(tree.arrayReader("global_eta"))
        print globalFeatures
        self.tfEval.addFeatureGroup(globalFeatures)
        
        self._ttreereaderversion = tree._ttreereaderversion
        
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        
        jets = Collection(event, "global")
        
        if event._tree._ttreereaderversion > self._ttreereaderversion:
            self.setupEval(event._tree)
        
        for ijet,jet in enumerate(jets):

            result = self.tfEval.evaluate(ijet)
            print ijet,jet.eta,result[0]
            '''
            #print self.blub
            print len(result),"=",
            for i in range(len(result)):
                print result[i],
            #print "/",event.global_pt[ijet]
            print
            '''
        return True
        
files=[
    [
    "root://gfe02.grid.hep.ph.ic.ac.uk/pnfs/hep.ph.ic.ac.uk/data/cms/store/user/mkomm/LLP/NANOX_180425-v2/SMS-T1qqqq_ctau-1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/SMS-T1qqqq_ctau-1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOX_180425-v2/180425_183459/0000/nano_6.root",
    "/vols/cms/mkomm/LLP/NANOX_180425-v2_eval/SMS-T1qqqq_ctau-1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/nano_6.root.friend",
    ]
]

'''
files=[
    [
    "root://gfe02.grid.hep.ph.ic.ac.uk/pnfs/hep.ph.ic.ac.uk/data/cms/store/user/mkomm/LLP/NANOX_180425-v2/SingleMuon_Run2016B-03Feb2017_ver2-v2/SingleMuon/Run2016B-03Feb2017_ver2-v2_NANOX_180425-v2/180425_185224/0000/nano_100.root",
    "/vols/cms/mkomm/LLP/NANOX_180425-v2_eval/SingleMuon_Run2016B-03Feb2017_ver2-v2/nano_100.root.friend"
    ]
]
'''
'''
files = [
    [
        "root://gfe02.grid.hep.ph.ic.ac.uk/pnfs/hep.ph.ic.ac.uk/data/cms/store/user/mkomm/LLP/NANOX_180425-v2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOX_180425-v2/180425_182750/0000/nano_100.root",
        "/vols/cms/mkomm/LLP/NANOX_180425-v2_eval/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/nano_100.root.friend",
    ]
]
'''
'''
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
'''
p=PostProcessor('.',files,cut=None,branchsel=None,modules=[
    exampleProducer()
],friend=True)
p.run()


