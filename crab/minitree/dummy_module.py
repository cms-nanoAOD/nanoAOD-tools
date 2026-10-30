##https://twiki.cern.ch/twiki/bin/viewauth/CMS/MLReweighting
import onnxruntime as ort
import ROOT
import numpy as np
import os,sys
import math
import random
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from scaleFactor import *

def mk_safe(fct, *args):
    try:
        return fct(*args)
    except Exception as e:
        if any('Error in function boost::math::erf_inv' in arg for arg in e.args):
            print('WARNING: catching exception and returning -1. Exception arguments: %s' % e.args)
            return -1.
        else:
            raise e

class dummy_producer(Module):
    def __init__(self,Isolation,dataYear):
        self.Isolation = Isolation
        self.dataYear = dataYear
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("elSF_v2","F")
        if(self.Isolation==True):
            self.out.branch("Electron_SF_Iso_v2",  "F")
            self.out.branch("Electron_SF_Iso_v2_IDUp",  "F")
            self.out.branch("Electron_SF_Iso_v2_IDDown",  "F")
            self.out.branch("Electron_SF_Iso_v2_TrigUp",  "F")
            self.out.branch("Electron_SF_Iso_v2_TrigDown",  "F")
        elif(self.Isolation==False):
            self.out.branch("Electron_SF_Veto_v2",  "F")
            self.out.branch("Electron_SF_Veto_v2_IDUp",  "F")
            self.out.branch("Electron_SF_Veto_v2_IDDown",  "F")
            self.out.branch("Electron_SF_Veto_v2_TrigUp",  "F")
            self.out.branch("Electron_SF_Veto_v2_TrigDown",  "F")

        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    ##Def of rapidity
    
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        el_pt = getattr(event,'ElectronPt')
        el_eta = getattr(event,'ElectronSCEta')

        if(self.Isolation==True):
            
            Electron_SF_Iso_v2 = create_elSF(self.dataYear,el_pt,el_eta,"Tight","noSyst")
            elSF =  Electron_SF_Iso_v2
            #print(elSF)
            Electron_SF_Iso_v2_IDUp = create_elSF(self.dataYear,el_pt,el_eta,"Tight","IDUp")
            Electron_SF_Iso_v2_IDDown = create_elSF(self.dataYear,el_pt,el_eta,"Tight","IDDown")
            Electron_SF_Iso_v2_TrigUp = create_elSF(self.dataYear,el_pt,el_eta,"Tight","TrigUp")
            Electron_SF_Iso_v2_TrigDown = create_elSF(self.dataYear,el_pt,el_eta,"Tight","TrigDown")
        
            self.out.fillBranch("Electron_SF_Iso_v2", Electron_SF_Iso_v2)
            self.out.fillBranch("Electron_SF_Iso_v2_IDUp",Electron_SF_Iso_v2_IDUp)
            self.out.fillBranch("Electron_SF_Iso_v2_IDDown",Electron_SF_Iso_v2_IDDown)
            self.out.fillBranch("Electron_SF_Iso_v2_TrigUp",Electron_SF_Iso_v2_TrigUp)
            self.out.fillBranch("Electron_SF_Iso_v2_TrigDown",Electron_SF_Iso_v2_TrigDown)

        elif(self.Isolation==False):
            Electron_SF_Veto_v2 = create_elSF(self.dataYear,el_pt,el_eta,"Veto","noSyst")
            elSF =  Electron_SF_Veto_v2
            Electron_SF_Veto_v2_IDUp = create_elSF(self.dataYear,el_pt,el_eta,"Veto","IDUp")
            Electron_SF_Veto_v2_IDDown = create_elSF(self.dataYear,el_pt,el_eta,"Veto","IDDown")
            Electron_SF_Veto_v2_TrigUp = create_elSF(self.dataYear,el_pt,el_eta,"Veto","TrigUp")
            Electron_SF_Veto_v2_TrigDown = create_elSF(self.dataYear,el_pt,el_eta,"Veto","TrigDown")

            self.out.fillBranch("Electron_SF_Veto_v2", Electron_SF_Veto_v2)
            self.out.fillBranch("Electron_SF_Veto_v2_IDUp",Electron_SF_Veto_v2_IDUp)
            self.out.fillBranch("Electron_SF_Veto_v2_IDDown",Electron_SF_Veto_v2_IDDown)
            self.out.fillBranch("Electron_SF_Veto_v2_TrigUp",Electron_SF_Veto_v2_TrigUp)
            self.out.fillBranch("Electron_SF_Veto_v2_TrigDown",Electron_SF_Veto_v2_TrigDown)
        self.out.fillBranch("elSF_v2", elSF)
        return True

dummy_mainModule = lambda : dummy_producer()    
dummy_mainModule_2J1T1_UL2017 = lambda : dummy_producer(True,'UL2017')
dummy_mainModule_2J1T0_UL2017 = lambda : dummy_producer(False,'UL2017')