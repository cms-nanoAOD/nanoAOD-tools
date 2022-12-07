'''
source of the scaling
https://hmei.web.cern.ch/hmei/Hgg/notes/photon_scale_uncertainty_UL.html


 Key: EB_in : |Eta| 0-1 EB_out: |Eta| 1-1.4442

UL16 Pre-VFP

EB_in Gain 12 : 0.05% EB_in Gain 6 : 0.5% EB_in Gain 1 : 2.0%

EB_out Gain 12 : 0.075% EB_out Gain 6 : 0.5% EB_out Gain 1 : 2.0%

EE Gain 12 : 0.15% EE Gain 6 : 1.0% EE Gain 1 : 3.%

UL16 Post-VFP

EB_in Gain 12 : 0.05% EB_in Gain 6 : 0.5% EB_in Gain 1 : 2.0%

EB_out Gain 12 : 0.075% EB_out Gain 6 : 0.5% EB_out Gain 1 : 2.0%

EE Gain 12 : 0.15% EE Gain 6 : 1.0% EE Gain 1 : 3.%

UL17

EB Gain 12 : 0.05% EB Gain 6 : 0.5% EB Gain 1 : 1.0%

EE Gain 12 : 0.1% EE Gain 6 : 0.5% EE Gain 1 : 2.%

UL18

EB Gain 12 : 0.05% EB Gain 6 : 0.5% EB Gain 1 : 1.0%

EE Gain 12 : 0.125% EE Gain 6 : 0.75% EE Gain 1 : 2.% '''


import ROOT
import os
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 

import json,array

class gammaSFProducer(Module):
    def __init__(self, year="2016"):
        #load helper modules if any
        #load data files
        self.year=year
        self.sysdict={

		"UL16Pre-VFP" :{ "EBin":{12 : 0.05, 6 : 0.5, 1 : 2.0}, "EBout":{12 : 0.075, 6 : 0.5, 1 : 2.0}, "EE":{12 : 0.15,  6 : 1.0,  1 : 3.0} },
		"UL16Post-VFP":{ "EBin":{12 : 0.05, 6 : 0.5, 1 : 2.0}, "EBout":{12 : 0.075, 6 : 0.5, 1 : 2.0}, "EE":{12 : 0.15,  6 : 1.0,  1 : 3.0} },
                "UL17"        :{ "EBin":{12 : 0.05, 6 : 0.5, 1 : 1.0}, "EBout":{12 : 0.05,  6 : 0.5, 1 : 1.0}, "EE":{12 : 0.1,   6 : 0.5,  1 : 2.0} },
                "UL18"        :{ "EBin":{12 : 0.05, 6 : 0.5, 1 : 1.0}, "EBout":{12 : 0.05,  6 : 0.5, 1 : 1.0}, "EE":{12 : 0.125, 6 : 0.75, 1 : 2.0} }
        }        


    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        for ud in ["Up", "Down"]:
            self.out.branch("Photon_pt_Scale"+ud, "F", lenVar="nPhoton")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def getSFUpDown(self, period, eta, EB, EE, Gain ):
        
        etaBin="bin"
        if EE:
           etaBin="EE"
        elif EB:
           if (eta<1. ):
             etaBin="EBin"
           else:
             etaBin="EBout"
 		        
        try:
           unc=self.sysdict[period][etaBin][Gain]
        except:
           unc =0.
        #print unc,"check", period, etaBin, Gain,"inputs", period, eta, EB, EE, Gain
        return unc


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
       
        photons = Collection(event, "Photon")
        
        pts=np.array([pho.pt for pho in photons])


        sf_photons = np.array([ self.getSFUpDown(self.year, abs(pho.eta), pho.isScEtaEB, pho.isScEtaEE, pho.seedGain) for pho in photons])
        pt_up=pts*(1+sf_photons/100.)
        pt_down=pts*(1-sf_photons/100.)
        self.out.fillBranch("Photon_pt_ScaleUp", pt_up)
        self.out.fillBranch("Photon_pt_ScaleDown", pt_down)

        return True


gammaSF_UL16PreVFP  = lambda : gammaSFProducer(year="UL16Pre-VFP")
gammaSF_UL16PostVFP = lambda : gammaSFProducer(year="UL16Post-VFP")
gammaSF_UL17         = lambda : gammaSFProducer(year="UL17")
gammaSF_UL18         = lambda : gammaSFProducer(year="UL18")

