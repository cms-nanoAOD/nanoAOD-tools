import os
import sys
import math
import json
import ROOT
import random

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from utils import getGraph,getHist,combineHist2D,getSFPtEta

class MuonSelection(Module):

    def __init__(
        self,
        inputCollection = lambda event: Collection(event, "Muon"),
        outputName = "tightMuons",
        muonMinPt = 26.,
        muonMaxEta = 2.4,
        storeKinematics=['pt','eta'],
        storeWeights=False,
        globalOptions={"isData":False}
    ):
        self.globalOptions = globalOptions
        self.inputCollection = inputCollection
        self.outputName = outputName
        self.muonMinPt = muonMinPt
        self.muonMaxEta = muonMaxEta
        self.storeKinematics = storeKinematics
        self.storeWeights = storeWeights
        
        if not self.globalOptions["isData"]:
            #tracking efficiency
            self.trackSF = getGraph(
                "PhysicsTools/NanoAODTools/data/muon/track_EfficienciesAndSF_RunBtoH.root",
                "ratio_eff_aeta_dr030e030_corr"
            )
            
            #id efficiency
            idTightSFBToF = getHist(
                "PhysicsTools/NanoAODTools/data/muon/id_EfficienciesAndSF_RunBtoF.root",
                "MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/pt_abseta_ratio"
            )
            idTightSFGToH = getHist(
                "PhysicsTools/NanoAODTools/data/muon/id_EfficienciesAndSF_RunGtoH.root",
                "MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/pt_abseta_ratio"
            )
            self.idTightSFHist = combineHist2D(
                idTightSFBToF,
                idTightSFGToH,
                1.-16226.5/35916.4,
                16226.5/35916.4
            )
            
            #iso efficiency
            isoTightSFBToF = getHist(
                "PhysicsTools/NanoAODTools/data/muon/iso_EfficienciesAndSF_RunBtoF.root",
                "TightISO_TightID_pt_eta/pt_abseta_ratio"
            )
            isoTightSFGToH = getHist(
                "PhysicsTools/NanoAODTools/data/muon/iso_EfficienciesAndSF_RunGtoH.root",
                "TightISO_TightID_pt_eta/pt_abseta_ratio"
            )
            self.isoTightSFHist = combineHist2D(
                isoTightSFBToF,
                isoTightSFGToH,
                1.-16226.5/35916.4,
                16226.5/35916.4
            )
 
    def beginJob(self):
        pass
        
    def endJob(self):
        pass
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("n"+self.outputName,"I")

        for variable in self.storeKinematics:
            self.out.branch(self.outputName+"_"+variable,"F",lenVar="n"+self.outputName)
            
        if not self.globalOptions["isData"] and self.storeWeights:
            self.out.branch(self.outputName+"_weight_track_nominal","F")
        
            self.out.branch(self.outputName+"_weight_id_nominal","F")
            self.out.branch(self.outputName+"_weight_id_up","F")
            self.out.branch(self.outputName+"_weight_id_down","F")
            
            self.out.branch(self.outputName+"_weight_iso_nominal","F")
            self.out.branch(self.outputName+"_weight_iso_up","F")
            self.out.branch(self.outputName+"_weight_iso_down","F")
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        muons = self.inputCollection(event)
        
        selectedMuons = []
        unselectedMuons = []
        
        weight_track_nominal = 1.0
        
        weight_id_nominal = 1.0
        weight_id_up = 1.0
        weight_id_down = 1.0
        
        weight_iso_nominal = 1.0
        weight_iso_up = 1.0
        weight_iso_down = 1.0
        
        #https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonIdRun2#Tight_Muon
        for muon in muons:
            if muon.pt>self.muonMinPt and math.fabs(muon.eta)<self.muonMaxEta and (muon.tightId==1) and (muon.pfRelIso04_all<0.15):
                selectedMuons.append(muon)
                if not self.globalOptions["isData"] and self.storeWeights:
                    weight_track_nominal*=self.trackSF.Eval(math.fabs(muon.eta))
                    
                    weight_id,weight_id_err = getSFPtEta(self.idTightSFHist,muon.pt,muon.eta)
                    weight_id_nominal*=weight_id
                    weight_id_up*=(weight_id+weight_id_err)
                    weight_id_down*=(weight_id-weight_id_err)
                    
                    weight_iso,weight_iso_err = getSFPtEta(self.isoTightSFHist,muon.pt,muon.eta)
                    weight_iso_nominal*=weight_iso
                    weight_iso_up*=(weight_iso+weight_iso_err)
                    weight_iso_down*=(weight_iso-weight_iso_err)
            else:
                unselectedMuons.append(muon)
  
        self.out.fillBranch("n"+self.outputName,len(selectedMuons))
        for variable in self.storeKinematics:
            self.out.fillBranch(self.outputName+"_"+variable,map(lambda muon: getattr(muon,variable),selectedMuons))
        
        if not self.globalOptions["isData"] and self.storeWeights:
            self.out.fillBranch(self.outputName+"_weight_track_nominal",weight_track_nominal)
            
            self.out.fillBranch(self.outputName+"_weight_id_nominal",weight_id_nominal)
            self.out.fillBranch(self.outputName+"_weight_id_up",weight_id_up)
            self.out.fillBranch(self.outputName+"_weight_id_down",weight_id_down)
            
            self.out.fillBranch(self.outputName+"_weight_iso_nominal",weight_iso_nominal)
            self.out.fillBranch(self.outputName+"_weight_iso_up",weight_iso_up)
            self.out.fillBranch(self.outputName+"_weight_iso_down",weight_iso_down)

        setattr(event,self.outputName,selectedMuons)
        setattr(event,self.outputName+"_unselected",unselectedMuons)

        return True
        
