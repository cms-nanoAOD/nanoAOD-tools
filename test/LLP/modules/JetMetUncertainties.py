import os
import sys
import math
import json
import ROOT
import random

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jecUncertainties import jecUncertProducerCpp


class JetMetUncertainties(jecUncertProducerCpp):
    def __init__(
        self,
        globalTag,uncerts=["Total"],jetFlavour="AK4PFchs",jetColl="Jet", doCppOutput=True,
        globalOptions={"isData":False}
    ):
        jecUncertProducerCpp.__init__(self,globalTag,uncerts=["Total"],jetFlavour="AK4PFchs",jetColl="Jet", doCppOutput=True)
        self.globalOptions = globalOptions
        
    def beginJob(self):
        jecUncertProducerCpp.beginJob(self)
        
    def endJob(self):
        jecUncertProducerCpp.endJob(self)
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        jecUncertProducerCpp.beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree)
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        jecUncertProducerCpp.endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree)
        
    def analyze(self, event):
        return self.analyze(self, event)
        
