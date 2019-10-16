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
    TIGHT = 1
    MEDIUM = 2
    LOOSE = 3

    def __init__(
        self,
        inputCollection = lambda event: Collection(event, "Muon"),
        outputName = "tightMuons",
        muonID = TIGHT,
        muonIso = TIGHT,
        muonMinPt = 29.,
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
        
        #tracking efficiency
        self.trackSF = getGraph(
            "PhysicsTools/NanoAODTools/data/muon/track_EfficienciesAndSF_RunBtoH.root",
            "ratio_eff_aeta_dr030e030_corr"
        )
        
        #tight id efficiency
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
        
        #medium id efficiency
        idMediumSFBToF = getHist(
            "PhysicsTools/NanoAODTools/data/muon/id_EfficienciesAndSF_RunBtoF.root",
            "MC_NUM_MediumID_DEN_genTracks_PAR_pt_eta/pt_abseta_ratio"
        )
        idMediumSFGToH = getHist(
            "PhysicsTools/NanoAODTools/data/muon/id_EfficienciesAndSF_RunGtoH.root",
            "MC_NUM_MediumID_DEN_genTracks_PAR_pt_eta/pt_abseta_ratio"
        )
        self.idMediumSFHist = combineHist2D(
            idMediumSFBToF,
            idMediumSFGToH,
            1.-16226.5/35916.4,
            16226.5/35916.4
        )
        
        #loose id efficiency
        idLooseSFBToF = getHist(
            "PhysicsTools/NanoAODTools/data/muon/id_EfficienciesAndSF_RunBtoF.root",
            "MC_NUM_LooseID_DEN_genTracks_PAR_pt_eta/pt_abseta_ratio"
        )
        idLooseSFGToH = getHist(
            "PhysicsTools/NanoAODTools/data/muon/id_EfficienciesAndSF_RunGtoH.root",
            "MC_NUM_LooseID_DEN_genTracks_PAR_pt_eta/pt_abseta_ratio"
        )
        self.idLooseSFHist = combineHist2D(
            idLooseSFBToF,
            idLooseSFGToH,
            1.-16226.5/35916.4,
            16226.5/35916.4
        )
        
        
        
        #tight iso and tight id efficiency
        isoTightTightSFBToF = getHist(
            "PhysicsTools/NanoAODTools/data/muon/iso_EfficienciesAndSF_RunBtoF.root",
            "TightISO_TightID_pt_eta/pt_abseta_ratio"
        )
        isoTightTightSFGToH = getHist(
            "PhysicsTools/NanoAODTools/data/muon/iso_EfficienciesAndSF_RunGtoH.root",
            "TightISO_TightID_pt_eta/pt_abseta_ratio"
        )
        self.isoTightTightSFHist = combineHist2D(
            isoTightTightSFBToF,
            isoTightTightSFGToH,
            1.-16226.5/35916.4,
            16226.5/35916.4
        )
        
        #tight iso and medium id efficiency
        isoTightMediumSFBToF = getHist(
            "PhysicsTools/NanoAODTools/data/muon/iso_EfficienciesAndSF_RunBtoF.root",
            "TightISO_MediumID_pt_eta/pt_abseta_ratio"
        )
        isoTightMediumSFGToH = getHist(
            "PhysicsTools/NanoAODTools/data/muon/iso_EfficienciesAndSF_RunGtoH.root",
            "TightISO_MediumID_pt_eta/pt_abseta_ratio"
        )
        self.isoTightMediumSFHist = combineHist2D(
            isoTightMediumSFBToF,
            isoTightMediumSFGToH,
            1.-16226.5/35916.4,
            16226.5/35916.4
        )
        
        #loose iso and medium id efficiency
        isoLooseMediumSFBToF = getHist(
            "PhysicsTools/NanoAODTools/data/muon/iso_EfficienciesAndSF_RunBtoF.root",
            "LooseISO_MediumID_pt_eta/pt_abseta_ratio"
        )
        isoLooseMediumSFGToH = getHist(
            "PhysicsTools/NanoAODTools/data/muon/iso_EfficienciesAndSF_RunGtoH.root",
            "LooseISO_MediumID_pt_eta/pt_abseta_ratio"
        )
        self.isoLooseMediumSFHist = combineHist2D(
            isoLooseMediumSFBToF,
            isoLooseMediumSFGToH,
            1.-16226.5/35916.4,
            16226.5/35916.4
        )
        
        #loose iso and loose id efficiency
        isoLooseLooseSFBToF = getHist(
            "PhysicsTools/NanoAODTools/data/muon/iso_EfficienciesAndSF_RunBtoF.root",
            "LooseISO_LooseID_pt_eta/pt_abseta_ratio"
        )
        isoLooseLooseSFGToH = getHist(
            "PhysicsTools/NanoAODTools/data/muon/iso_EfficienciesAndSF_RunGtoH.root",
            "LooseISO_LooseID_pt_eta/pt_abseta_ratio"
        )
        self.isoLooseLooseSFHist = combineHist2D(
            isoLooseLooseSFBToF,
            isoLooseLooseSFGToH,
            1.-16226.5/35916.4,
            16226.5/35916.4
        )
            
        if muonID==MuonSelection.TIGHT:
            self.muonId = lambda muon: muon.tightId==1
            self.muonIdSF = self.idTightSFHist
        elif muonID==MuonSelection.MEDIUM:
            self.muonId = lambda muon: muon.mediumId==1
            self.muonIdSF = self.idMediumSFHist
        elif muonID==MuonSelection.LOOSE:
            self.muonId = lambda muon: muon.isPFcand==1
            self.muonIdSF = self.idLooseSFHist
        else:
            print "Error - undefined muon id flag"
            sys.exit(1)
            
        if muonIso==MuonSelection.TIGHT:
            self.muonIso = lambda muon: muon.pfRelIso04_all<0.15
            if muonID==MuonSelection.TIGHT:
                self.muonIsoSF = self.isoTightTightSFHist
            elif muonID==MuonSelection.MEDIUM:
                self.muonIsoSF = self.isoTightMediumSFHist
            elif muonID==MuonSelection.LOOSE:
                self.muonIsoSF = self.isoTightLooseSFHist
        elif muonIso==MuonSelection.MEDIUM:
            print "Error - no medium working point for muon isolation!"
            sys.exit(1)
        elif muonIso==MuonSelection.LOOSE:
            self.muonIso = lambda muon: muon.pfRelIso04_all<0.25
            if muonID==MuonSelection.TIGHT:
                self.muonIsoSF = self.isoLooseTightSFHist
            elif muonID==MuonSelection.MEDIUM:
                self.muonIsoSF = self.isoLooseMediumSFHist
            elif muonID==MuonSelection.LOOSE:
                self.muonIsoSF = self.isoLooseLooseSFHist
        else:
            print "Error - undefined muon id flag"
            sys.exit(1)
            
 
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
            if type(self.muonMinPt)==type([]):
                muonMinPt = self.muonMinPt[min(len(selectedMuons),len(self.muonMinPt)-1)]
            else:
                muonMinPt = self.muonMinPt
            if muon.pt>muonMinPt and math.fabs(muon.eta)<self.muonMaxEta and self.muonId(muon) and self.muonIso(muon):
                selectedMuons.append(muon)
                if not self.globalOptions["isData"] and self.storeWeights:
                    weight_track_nominal*=self.trackSF.Eval(math.fabs(muon.eta))
                    
                    weight_id,weight_id_err = getSFPtEta(self.muonIdSF,muon.pt,muon.eta)
                    weight_id_nominal*=weight_id
                    weight_id_up*=(weight_id+weight_id_err)
                    weight_id_down*=(weight_id-weight_id_err)
                    
                    weight_iso,weight_iso_err = getSFPtEta(self.muonIsoSF,muon.pt,muon.eta)
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
        
