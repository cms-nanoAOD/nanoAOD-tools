import os
import sys
import math
import json
import ROOT
import random

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from utils import deltaR

class JetSelection(Module):

    def __init__(
        self,
        inputCollection = lambda event: Collection(event, "Jet"),
        leptonCollection = lambda event: event.tightMuons,
        outputName = "centralJets",
        jetMinPt = 30.,
        jetMaxEta = 2.4,
        dRCleaning = 0.4,
        storeKinematics=['pt','eta'],
        globalOptions={"isData":False}
    ):
        self.globalOptions = globalOptions
        self.inputCollection = inputCollection
        self.leptonCollection = leptonCollection
        self.outputName = outputName
        self.jetMinPt = jetMinPt
        self.jetMaxEta = jetMaxEta
        self.dRCleaning = dRCleaning
        self.storeKinematics = storeKinematics
        
 
    def beginJob(self):
        pass
        
    def endJob(self):
        pass
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("n"+self.outputName,"I")
        
        for variable in self.storeKinematics:
            self.out.branch(self.outputName+"_"+variable,"F",lenVar="n"+self.outputName)

        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = self.inputCollection(event)
        
        selectedJets = []
        unselectedJets = []
        
        for jet in jets:
            if jet.pt>self.jetMinPt and math.fabs(jet.eta)<self.jetMaxEta and (jet.jetId>0):
                leptons = self.leptonCollection(event)
                if leptons!=None and len(leptons)>0:
                    mindr = min(map(lambda lepton: deltaR(lepton,jet),leptons))
                    if mindr<self.dRCleaning:
                        unselectedJets.append(jet)
                        continue
                selectedJets.append(jet)
            else:
                unselectedJets.append(jet)
                
  
        self.out.fillBranch("n"+self.outputName,len(selectedJets))
        for variable in self.storeKinematics:
            self.out.fillBranch(self.outputName+"_"+variable,map(lambda jet: getattr(jet,variable),selectedJets))
            
        setattr(event,self.outputName,selectedJets)
        setattr(event,self.outputName+"_unselected",unselectedJets)
        
        return True
        
