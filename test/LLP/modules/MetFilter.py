import os
import sys
import math
import json
import ROOT
import random

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class MetFilter(Module):
    def __init__(self,globalOptions={"isData":False}):
        self.globalOptions=globalOptions
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.nEvents = 0
        
        self.nHalo = 0
        self.nHBHENoise = 0
        self.nIsoNoise = 0
        self.nDeadCell = 0
        self.nTotal = 0
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        #pass
        print "Total passed %i"%(self.nEvents)
        print "halo: %.1f%%"%(100.-100.*self.nHalo/self.nEvents)
        print "noise: %.1f%%"%(100.-100.*self.nHBHENoise/self.nEvents)
        print "iso: %.1f%%"%(100.-100.*self.nIsoNoise/self.nEvents)
        print "cell: %.1f%%"%(100.-100.*self.nDeadCell/self.nEvents)
        print "total: %.1f%%"%(100.-100.*self.nTotal/self.nEvents)
        
    def analyze(self, event):
        #https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFiltersRun2#Moriond_2017
        
        if event.Flag_goodVertices==0:
            return False
        
        self.nEvents+=1
        
        accepted = True
        
        if event.Flag_globalTightHalo2016Filter==0:
            #return False
            self.nHalo+=1
            accepted = False
            
        if event.Flag_HBHENoiseFilter==0:
            #return False
            self.nHBHENoise+=1
            accepted = False
            
        if event.Flag_HBHENoiseIsoFilter==0:
            #return False
            self.nIsoNoise+=1
            accepted = False
            
        if event.Flag_EcalDeadCellTriggerPrimitiveFilter==0:
            #return False
            self.nDeadCell+=1
            accepted = False
            
        if not accepted:
            self.nTotal+=1
            
        if self.globalOptions["isData"] and event.Flag_eeBadScFilter==0: #not suggested on MC
            return False
        
        return True
        
