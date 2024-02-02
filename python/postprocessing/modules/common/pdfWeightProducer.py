import ROOT
import math, os,re
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class pdfWeightProducer(Module):
    #def __init__(self):

    #def beginJob(self):

    #def endJob(self):

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("LHEPdfWeightUp", "F")
        self.out.branch("LHEPdfWeightDown", "F")
                        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        pdfWeightUp = -99.
        pdfWeightDown = -99.

        if hasattr(event,"LHEPdfWeight"):
            self.pdfWeightList = [  i for i in event.LHEPdfWeight ]

            if len(self.pdfWeightList) > 1:
                w = np.std(self.pdfWeightList)
                pdfWeightUp = 1. + abs(w)
                pdfWeightDown = 1. - abs(w)

        self.out.fillBranch("LHEPdfWeightUp", pdfWeightUp)
        self.out.fillBranch("LHEPdfWeightDown", pdfWeightDown)
            
        return True
