import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import itertools

from PhysicsTools.NanoAODTools.postprocessing.modules.jme.JetReCalibrator import JetReCalibrator

class l1JetCalibrations(Module):
    def __init__(self, globalTag):
        self.jesInputFilePath = os.environ['CMSSW_BASE'] + "/src/PhysicsTools/NanoAODTools/data/jme/"
        self.jetReCalibrator = JetReCalibrator(globalTag, 'AK4PFchs' , True, self.jesInputFilePath, calculateSeparateCorrections = True, calculateType1METCorrection=True)
        pass
    def beginJob(self):
        pass
    
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.wrappedOutputTree = wrappedOutputTree
        self.wrappedOutputTree.branch('Jet_l1corrFactor','F', lenVar='nJet')

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):

        jets = Collection(event, 'Jet')
        
        rho = getattr(event, 'fixedGridRhoFastjetAll')
        l1corrFactors = []

        for jet in jets:
            l1corrFactors.append(  self.jetReCalibrator.getCorrection(jet,rho,corrector=self.jetReCalibrator.separateJetCorrectors["L1"]))

        self.wrappedOutputTree.fillBranch("Jet_l1corrFactor", l1corrFactors)

        
        
        
        return True
