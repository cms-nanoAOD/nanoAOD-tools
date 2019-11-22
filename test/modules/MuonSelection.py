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
    NONE = 4

    def __init__(
        self,
        inputCollection = lambda event: Collection(event, "Muon"),
        outputName = "tightMuons",
        muonID = TIGHT,
        muonIso = TIGHT,
        muonMinPt = 29.,
        muonMaxEta = 2.4,
        muonMaxDxy = 1.e9,
        muonMaxDz = 1.e9,
        muonMinDxy = 0.,
        muonMinDz = 0.,
        storeKinematics=['pt','eta'],
        storeWeights=False,
        globalOptions={"isData":False, "year":2016}
    ):
        
        self.globalOptions = globalOptions
        self.inputCollection = inputCollection
        self.outputName = outputName
        self.muonMinPt = muonMinPt
        self.muonMaxEta = muonMaxEta
        self.muonMaxDxy = muonMaxDxy
        self.muonMaxDz = muonMaxDz
        self.muonMinDxy = muonMinDxy
        self.muonMinDz = muonMinDz
        self.storeKinematics = storeKinematics
        self.storeWeights = storeWeights

        if self.globalOptions["year"] == 2016:
            
            #tight id efficiency
            idTightSFBToF = getHist(
                "PhysicsTools/NanoAODTools/data/muon/2016/RunBCDEF_SF_ID.root",
                "NUM_TightID_DEN_genTracks_eta_pt"
            )
            idTightSFGToH = getHist(
                "PhysicsTools/NanoAODTools/data/muon/2016/RunGH_SF_ID.root",
                "NUM_TightID_DEN_genTracks_eta_pt"
            )
            self.idTightSFHist = combineHist2D(
                idTightSFBToF,
                idTightSFGToH,
                1.-16226.5/35916.4,
                16226.5/35916.4
            )
            
            #loose id efficiency
            idLooseSFBToF = getHist(
                "PhysicsTools/NanoAODTools/data/muon/2016/RunBCDEF_SF_ID.root",
                "NUM_LooseID_DEN_genTracks_eta_pt"
            )
            idLooseSFGToH = getHist(
                "PhysicsTools/NanoAODTools/data/muon/2016/RunGH_SF_ID.root",
                "NUM_LooseID_DEN_genTracks_eta_pt"
            )

            self.idLooseSFHist = combineHist2D(
                idLooseSFBToF,
                idLooseSFGToH,
                1.-16226.5/35916.4,
                16226.5/35916.4
            )
            
            
            #tight iso and tight id efficiency
            isoTightTightSFBToF = getHist(
                "PhysicsTools/NanoAODTools/data/muon/2016/RunBCDEF_SF_ISO.root",
                "NUM_TightRelIso_DEN_TightIDandIPCut_eta_pt"
            )
            isoTightTightSFGToH = getHist(
                "PhysicsTools/NanoAODTools/data/muon/2016/RunGH_SF_ISO.root",
                "NUM_TightRelIso_DEN_TightIDandIPCut_eta_pt"
            )
            self.isoTightTightSFHist = combineHist2D(
                isoTightTightSFBToF,
                isoTightTightSFGToH,
                1.-16226.5/35916.4,
                16226.5/35916.4
            )
            
            #loose iso and loose id efficiency
            isoLooseLooseSFBToF = getHist(
                "PhysicsTools/NanoAODTools/data/muon/2016/RunBCDEF_SF_ISO.root",
                "NUM_LooseRelIso_DEN_LooseID_eta_pt"
            )
            isoLooseLooseSFGToH = getHist(
                "PhysicsTools/NanoAODTools/data/muon/2016/RunGH_SF_ISO.root",
                "NUM_LooseRelIso_DEN_LooseID_eta_pt"
            )
            self.isoLooseLooseSFHist = combineHist2D(
                isoLooseLooseSFBToF,
                isoLooseLooseSFGToH,
                1.-16226.5/35916.4,
                16226.5/35916.4
            )

        elif self.globalOptions["year"] == 2017:
            
            #tight id efficiency
            idTightSFHist = getHist(
                "PhysicsTools/NanoAODTools/data/muon/2017/RunBCDEF_SF_ID.root",
                "NUM_TightID_DEN_genTracks_pt_abseta"
            )
            
            #loose id efficiency
            idLooseSFHist = getHist(
                "PhysicsTools/NanoAODTools/data/muon/2017/RunBCDEF_SF_ID.root",
                "NUM_LooseID_DEN_genTracks_pt_abseta"
            )
            
            #tight iso and tight id efficiency
            isoTightTightSFHist = getHist(
                "PhysicsTools/NanoAODTools/data/muon/2017/RunBCDEF_SF_ISO.root",
                "NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta"
            )
            
            #loose iso and loose id efficiency
            isoLooseLooseSFHist = getHist(
                "PhysicsTools/NanoAODTools/data/muon/2017/RunBCDEF_SF_ISO.root",
                "NUM_LooseRelIso_DEN_LooseID_pt_abseta"
            )

        elif self.globalOptions["year"] == 2018:

            #tight id efficiency
            idTightSFHist = getHist(
                "PhysicsTools/NanoAODTools/data/muon/2018/EfficienciesStudies_2018_rootfiles_RunABCD_SF_ID.root",
                "NUM_TightID_DEN_TrackerMuons_pt_abseta"
            )
            
            #loose id efficiency
            idLooseSFHist = getHist(
                "PhysicsTools/NanoAODTools/data/muon/2018/EfficienciesStudies_2018_rootfiles_RunABCD_SF_ID.root",
                "NUM_LooseID_DEN_TrackerMuons_pt_abseta"
            )
            
            #tight iso and tight id efficiency
            isoTightTightSFHist = getHist(
                "PhysicsTools/NanoAODTools/data/muon/2018/EfficienciesStudies_2018_rootfiles_RunABCD_SF_ISO.root",
                "NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta"
            )
            
            #loose iso and loose id efficiency
            isoLooseLooseSFHist = getHist(
                "PhysicsTools/NanoAODTools/data/muon/2018/EfficienciesStudies_2018_rootfiles_RunABCD_SF_ISO.root",
                "NUM_LooseRelIso_DEN_LooseID_pt_abseta"
            )

        else:
            print "Error - invalid year"
            sys.exit(1)

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
        elif muonIso==MuonSelection.NONE:
            self.muonIso = lambda muon: muon.pfRelIso04_all<1e9
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
            if muon.pt>muonMinPt and math.fabs(muon.eta)<self.muonMaxEta and self.muonId(muon) and self.muonIso(muon) and math.fabs(muon.dxy) > self.muonMinDxy and math.fabs(muon.dz) > self.muonMinDz and math.fabs(muon.dxy) < self.muonMaxDxy and math.fabs(muon.dz) < self.muonMaxDz:
                selectedMuons.append(muon)
                if not self.globalOptions["isData"] and self.storeWeights:
                    if self.globalOptions["year"] == 2016:
                        weight_id,weight_id_err = getSFPtEta(self.muonIdSF,muon.pt,muon.eta)
                    elif self.globalOptions["year"] == 2017 or self.globalOptions["year"] == 2018:
                        weight_id,weight_id_err = getSFPtEta(self.muonIdSF,abs(muon.eta),muon.pt)
                    weight_id_nominal*=weight_id
                    weight_id_up*=(weight_id+weight_id_err)
                    weight_id_down*=(weight_id-weight_id_err)
                    
                    if self.globalOptions["year"] == 2016:
                        weight_iso,weight_iso_err = getSFPtEta(self.muonIsoSF,muon.pt,muon.eta)
                    elif self.globalOptions["year"] == 2017 or self.globalOptions["year"] == 2018:
                        weight_iso,weight_iso_err = getSFPtEta(self.muonIsoSF,abs(muon.eta),muon.pt)
                    weight_iso_nominal*=weight_iso
                    weight_iso_up*=(weight_iso+weight_iso_err)
                    weight_iso_down*=(weight_iso-weight_iso_err)
            else:
                unselectedMuons.append(muon)
  
        self.out.fillBranch("n"+self.outputName,len(selectedMuons))
        for variable in self.storeKinematics:
            self.out.fillBranch(self.outputName+"_"+variable,map(lambda muon: getattr(muon,variable),selectedMuons))
        
        if not self.globalOptions["isData"] and self.storeWeights:
            
            self.out.fillBranch(self.outputName+"_weight_id_nominal",weight_id_nominal)
            self.out.fillBranch(self.outputName+"_weight_id_up",weight_id_up)
            self.out.fillBranch(self.outputName+"_weight_id_down",weight_id_down)
            
            self.out.fillBranch(self.outputName+"_weight_iso_nominal",weight_iso_nominal)
            self.out.fillBranch(self.outputName+"_weight_iso_up",weight_iso_up)
            self.out.fillBranch(self.outputName+"_weight_iso_down",weight_iso_down)

        setattr(event,self.outputName,selectedMuons)
        setattr(event,self.outputName+"_unselected",unselectedMuons)

        return True
