import os
import sys
import math
import json
import ROOT
import random

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from utils import deltaR,deltaPhi

class EventObservables(Module):

    def __init__(
        self,
        inputCollection = lambda event: Collection(event, "Jet"),
        metInput = lambda event: Object(event, "MET"),
        outputName = "centralJets",
        globalOptions={"isData":False}
    ):
        self.globalOptions = globalOptions
        self.inputCollection = inputCollection
        self.metInput = metInput
        self.outputName = outputName

    def beginJob(self):
        pass
        
    def endJob(self):
        pass
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch(self.outputName+"_ht","F")
        self.out.branch(self.outputName+"_mht","F")
        self.out.branch(self.outputName+"_mheta","F")
        self.out.branch(self.outputName+"_mass","F")
        self.out.branch(self.outputName+"_met","F")
        #self.out.branch(self.outputName+"_xmetRatio","F")
        #self.out.branch(self.outputName+"_xmetDphi","F")
        self.out.branch(self.outputName+"_minPhi","F")
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        objs = self.inputCollection(event)
        met = self.metInput(event)
        vectorSum = ROOT.TLorentzVector()
        scalarPtSum = 0.0
        for obj in objs:
            vectorSum+=obj.p4()
            scalarPtSum+=obj.pt
            
        self.out.fillBranch(self.outputName+"_ht",scalarPtSum)
        setattr(event,self.outputName+"_ht",scalarPtSum)
        self.out.fillBranch(self.outputName+"_mht",vectorSum.Pt())
        setattr(event,self.outputName+"_mht",vectorSum.Pt())
        self.out.fillBranch(self.outputName+"_mheta",vectorSum.Eta())
        setattr(event,self.outputName+"_mheta",vectorSum.Eta())
        self.out.fillBranch(self.outputName+"_mass",vectorSum.M())
        setattr(event,self.outputName+"_mass",vectorSum.M())
        self.out.fillBranch(self.outputName+"_met",met.pt)
        setattr(event,self.outputName+"_met",met.pt)
        
        '''
        #MET=MHT+X => X = MET-MHT
        met_px = met.pt*math.sin(met.phi)
        met_py = met.pt*math.cos(met.phi)
        missingX = met_px-vectorSum.Px()
        missingY = met_py-vectorSum.Py()
        missingPhi = math.atan2(missingY,missingX)
        xmetRatio = math.sqrt(missingX**2+missingY**2)/max(1e-10,met.pt)
        xmetDphi = math.fabs(deltaPhi(met.phi,missingPhi))
        
        self.out.fillBranch(self.outputName+"_xmetRatio",xmetRatio)
        setattr(event,self.outputName+"_xmetRatio",xmetRatio)
        
        self.out.fillBranch(self.outputName+"_xmetDphi",xmetDphi)
        setattr(event,self.outputName+"_xmetDphi",xmetDphi)
        '''
        minPhi = math.pi
        for obj in objs:
            negSum = -(vectorSum-obj.p4())
            minPhi = min(minPhi,math.fabs(deltaPhi(negSum.Phi(),obj.phi)))
        self.out.fillBranch(self.outputName+"_minPhi",minPhi)
        setattr(event,self.outputName+"_minPhi",minPhi)
        return True
        
