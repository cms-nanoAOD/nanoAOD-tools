import ROOT
import math, os
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import matchObjectCollection
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetSmearer import jetSmearer

class jetmetUncertaintiesProducer(Module):
    def __init__(self, era, globalTag, jesUncertainties = [ "Total" ], jetType = "AK4PFchs"):

        self.era = era

        #--------------------------------------------------------------------------------------------
        # CV: globalTag and jetType not yet used, as there is no consistent set of txt files for
        #     JES uncertainties and JER scale factors and uncertainties yet
        #--------------------------------------------------------------------------------------------

        self.jesUncertainties = jesUncertainties

        # smear jet pT to account for measured difference in JER between data and simulation.
        self.applyJERCorr = True
        self.jerInputFileName = "Spring16_25nsV10_MC_PtResolution_AK4PFchs.txt"
        self.jerUncertaintyInputFileName = "Spring16_25nsV10_MC_SF_AK4PFchs.txt"
        self.jetSmearer = jetSmearer(globalTag, jetType, self.jerInputFileName, self.jerUncertaintyInputFileName)

        self.jetBranchName = "Jet"
        self.genJetBranchName = "GenJet"
        self.metBranchName = "MET"
        self.rhoBranchName = "fixedGridRhoFastjetAll"

        # read jet energy scale (JES) uncertainties
        self.jesInputFilePath = os.environ['CMSSW_BASE'] + "/src/PhysicsTools/NanoAODTools/data/jme/"
        if len(jesUncertainties) == 1 and jesUncertainties[0] == "Total":
            if self.era == "2016":
                self.jesUncertaintyInputFileName = "Summer16_23Sep2016V4_MC_Uncertainty_AK4PFchs.txt"
            elif self.era == "2017":
                self.jesUncertaintyInputFileName = "Fall17_17Nov2017_V4_MC_Uncertainty_AK4PFchs.txt"
            else:
                raise ValueError("ERROR: Invalid era = '%s'!" % self.era)
        else:
            # 'UncertaintySources' file not yet updated for RunIIFall2017 MC
            self.jesUncertaintyInputFileName = "Summer16_23Sep2016V4_MC_UncertaintySources_AK4PFchs.txt"

        # define energy threshold below which jets are considered as "unclustered energy"
        # (cf. JetMETCorrections/Type1MET/python/correctionTermsPfMetType1Type2_cff.py )
        self.unclEnThreshold = 15.

        # load libraries for accessing JES scale factors and uncertainties from txt files
        for library in [ "libCondFormatsJetMETObjects", "libPhysicsToolsNanoAODTools" ]:
            if library not in ROOT.gSystem.GetLibraries():
                print("Load Library '%s'" % library.replace("lib", ""))
                ROOT.gSystem.Load(library)

    def beginJob(self):

        print("Loading jet energy scale (JES) uncertainties from file '%s'" % os.path.join(self.jesInputFilePath, self.jesUncertaintyInputFileName))
        #self.jesUncertainty = ROOT.JetCorrectionUncertainty(os.path.join(self.jesInputFilePath, self.jesUncertaintyInputFileName))
    
        self.jesUncertainty = {} 
        # implementation didn't seem to work for factorized JEC, try again another way
        for jesUncertainty in self.jesUncertainties:
            jesUncertainty_label = '' if (jesUncertainty == 'Total' and len(self.jesUncertainties) == 1) else jesUncertainty
            pars = ROOT.JetCorrectorParameters(os.path.join(self.jesInputFilePath, self.jesUncertaintyInputFileName),jesUncertainty_label)
            self.jesUncertainty[jesUncertainty] = ROOT.JetCorrectionUncertainty(pars)    

        self.jetSmearer.beginJob()

    def endJob(self):

        self.jetSmearer.endJob()

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("%s_pt_smeared" % self.jetBranchName, "F", lenVar="nJet")
        self.out.branch("%s_pt_smeared" % self.metBranchName, "F")
        self.out.branch("%s_phi_smeared" % self.metBranchName, "F")
        for shift in [ "Up", "Down" ]:
            self.out.branch("%s_pt_jer%s" % (self.jetBranchName, shift), "F", lenVar="nJet")
            self.out.branch("%s_pt_jer%s" % (self.metBranchName, shift), "F")
            self.out.branch("%s_phi_jer%s" % (self.metBranchName, shift), "F")
            for jesUncertainty in self.jesUncertainties:
                self.out.branch("%s_pt_jes%s%s" % (self.jetBranchName, jesUncertainty, shift), "F", lenVar="nJet")
                self.out.branch("%s_pt_jes%s%s" % (self.metBranchName, jesUncertainty, shift), "F")
                self.out.branch("%s_phi_jes%s%s" % (self.metBranchName, jesUncertainty, shift), "F")
            self.out.branch("%s_pt_unclustEn%s" % (self.metBranchName, shift), "F")
            self.out.branch("%s_phi_unclustEn%s" % (self.metBranchName, shift), "F")
                        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = Collection(event, self.jetBranchName )
        genJets = Collection(event, self.genJetBranchName )

        jets_pt_smeared = []
        jets_pt_jerUp   = []
        jets_pt_jerDown = []
        jets_pt_jesUp   = {}
        jets_pt_jesDown = {}
        for jesUncertainty in self.jesUncertainties:
            jets_pt_jesUp[jesUncertainty]   = []
            jets_pt_jesDown[jesUncertainty] = []

        met = Object(event, self.metBranchName)
        ( met_px,         met_py         ) = ( met.pt*math.cos(met.phi), met.pt*math.sin(met.phi) )
        ( met_px_smeared, met_py_smeared ) = ( met_px, met_py )
        ( met_px_jerUp,   met_py_jerUp   ) = ( met_px, met_py )
        ( met_px_jerDown, met_py_jerDown ) = ( met_px, met_py )
        ( met_px_jesUp,   met_py_jesUp   ) = ( {}, {} )
        ( met_px_jesDown, met_py_jesDown ) = ( {}, {} )
        for jesUncertainty in self.jesUncertainties:
            met_px_jesUp[jesUncertainty]   = met_px
            met_py_jesUp[jesUncertainty]   = met_py
            met_px_jesDown[jesUncertainty] = met_px
            met_py_jesDown[jesUncertainty] = met_py

        rho = getattr(event, self.rhoBranchName)

        # match reconstructed jets to generator level ones
        # (needed to evaluate JER scale factors and uncertainties)
        pairs = matchObjectCollection(jets, genJets)
        
        for jet in jets:
            genJet = pairs[jet]
            # evaluate JER scale factors and uncertainties
            # (cf. https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution and https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyResolution )
            ( jet_pt_smeared, jet_pt_jerUp, jet_pt_jerDown ) = self.jetSmearer.getSmearedJetPt(jet, genJet, rho)
            jet_pt_ref = None
            if self.applyJERCorr:
                jet_pt_ref     = jet_pt_smeared
            else:
                jet_pt_ref     = jet.pt
                jet_pt_jerUp   = jet_pt_jerUp*jet.pt/jet_pt_smeared
                jet_pt_jerDown = jet_pt_jerDown*jet.pt/jet_pt_smeared
            jets_pt_smeared.append(jet_pt_smeared)
            jets_pt_jerUp.append(jet_pt_jerUp)
            jets_pt_jerDown.append(jet_pt_jerDown)

            # evaluate JES uncertainties
            jet_pt_jesUp   = {}
            jet_pt_jesDown = {}
            for jesUncertainty in self.jesUncertainties:
                # (cf. https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyCorrections#JetCorUncertainties )
                self.jesUncertainty[jesUncertainty].setJetPt(jet_pt_ref)
                self.jesUncertainty[jesUncertainty].setJetEta(jet.eta)
                delta = self.jesUncertainty[jesUncertainty].getUncertainty(True)
                jet_pt_jesUp[jesUncertainty]   = jet_pt_ref*(1. + delta)
                jet_pt_jesDown[jesUncertainty] = jet_pt_ref*(1. - delta)
                jets_pt_jesUp[jesUncertainty].append(jet_pt_jesUp[jesUncertainty])
                jets_pt_jesDown[jesUncertainty].append(jet_pt_jesDown[jesUncertainty])

            # progate JER and JES corrections and uncertainties to MET
            if jet_pt_ref > self.unclEnThreshold:
                jet_cosPhi = math.cos(jet.phi)
                jet_sinPhi = math.sin(jet.phi)
                if self.applyJERCorr:
                    met_px_smeared = met_px_smeared - (jet_pt_smeared - jet.pt)*jet_cosPhi
                    met_py_smeared = met_py_smeared - (jet_pt_smeared - jet.pt)*jet_sinPhi
                met_px_jerUp   = met_px_jerUp   - (jet_pt_jerUp   - jet_pt_ref)*jet_cosPhi
                met_py_jerUp   = met_py_jerUp   - (jet_pt_jerUp   - jet_pt_ref)*jet_sinPhi
                met_px_jerDown = met_px_jerDown - (jet_pt_jerDown - jet_pt_ref)*jet_cosPhi
                met_py_jerDown = met_py_jerDown - (jet_pt_jerDown - jet_pt_ref)*jet_sinPhi
                for jesUncertainty in self.jesUncertainties:
                    met_px_jesUp[jesUncertainty]   = met_px_jesUp[jesUncertainty]   - (jet_pt_jesUp[jesUncertainty]   - jet_pt_ref)*jet_cosPhi
                    met_py_jesUp[jesUncertainty]   = met_py_jesUp[jesUncertainty]   - (jet_pt_jesUp[jesUncertainty]   - jet_pt_ref)*jet_sinPhi
                    met_px_jesDown[jesUncertainty] = met_px_jesDown[jesUncertainty] - (jet_pt_jesDown[jesUncertainty] - jet_pt_ref)*jet_cosPhi
                    met_py_jesDown[jesUncertainty] = met_py_jesDown[jesUncertainty] - (jet_pt_jesDown[jesUncertainty] - jet_pt_ref)*jet_sinPhi

        # propagate "unclustered energy" uncertainty to MET
        ( met_px_unclEnUp,   met_py_unclEnUp   ) = ( met_px, met_py )
        ( met_px_unclEnDown, met_py_unclEnDown ) = ( met_px, met_py )
        met_deltaPx_unclEn = getattr(event, self.metBranchName + "_MetUnclustEnUpDeltaX")
        met_deltaPy_unclEn = getattr(event, self.metBranchName + "_MetUnclustEnUpDeltaY")
        met_px_unclEnUp    = met_px_unclEnUp   + met_deltaPx_unclEn
        met_py_unclEnUp    = met_py_unclEnUp   + met_deltaPy_unclEn
        met_px_unclEnDown  = met_px_unclEnDown - met_deltaPx_unclEn
        met_py_unclEnDown  = met_py_unclEnDown - met_deltaPy_unclEn

        # propagate effect of jet energy smearing to MET
        if self.applyJERCorr:            
            met_px_jerUp   = met_px_jerUp   + (met_px_smeared - met_px)
            met_py_jerUp   = met_py_jerUp   + (met_py_smeared - met_py)
            met_px_jerDown = met_px_jerDown + (met_px_smeared - met_px)
            met_py_jerDown = met_py_jerDown + (met_py_smeared - met_py)
            for jesUncertainty in self.jesUncertainties:
                met_px_jesUp[jesUncertainty]   = met_px_jesUp[jesUncertainty]   + (met_px_smeared - met_px)
                met_py_jesUp[jesUncertainty]   = met_py_jesUp[jesUncertainty]   + (met_py_smeared - met_py)
                met_px_jesDown[jesUncertainty] = met_px_jesDown[jesUncertainty] + (met_px_smeared - met_px)
                met_py_jesDown[jesUncertainty] = met_py_jesDown[jesUncertainty] + (met_py_smeared - met_py)
            met_px_unclEnUp    = met_px_unclEnUp   + (met_px_smeared - met_px)
            met_py_unclEnUp    = met_py_unclEnUp   + (met_py_smeared - met_py)
            met_px_unclEnDown  = met_px_unclEnDown + (met_px_smeared - met_px)
            met_py_unclEnDown  = met_py_unclEnDown + (met_py_smeared - met_py)

        self.out.fillBranch("%s_pt_smeared" % self.jetBranchName, jets_pt_smeared)
        self.out.fillBranch("%s_pt_smeared" % self.metBranchName, math.sqrt(met_px_smeared**2 + met_py_smeared**2))
        self.out.fillBranch("%s_phi_smeared" % self.metBranchName, math.atan2(met_py_smeared, met_px_smeared))
        self.out.fillBranch("%s_pt_jerUp" % self.jetBranchName, jets_pt_jerUp)
        self.out.fillBranch("%s_pt_jerUp" % self.metBranchName, math.sqrt(met_px_jerUp**2 + met_py_jerUp**2))
        self.out.fillBranch("%s_phi_jerUp" % self.metBranchName, math.atan2(met_py_jerUp, met_px_jerUp))
        self.out.fillBranch("%s_pt_jerDown" % self.jetBranchName, jets_pt_jerDown)
        self.out.fillBranch("%s_pt_jerDown" % self.metBranchName, math.sqrt(met_px_jerDown**2 + met_py_jerDown**2))
        self.out.fillBranch("%s_phi_jerDown" % self.metBranchName, math.atan2(met_py_jerDown, met_px_jerDown))
        for jesUncertainty in self.jesUncertainties:
            self.out.fillBranch("%s_pt_jes%sUp" % (self.jetBranchName, jesUncertainty), jets_pt_jesUp[jesUncertainty])
            self.out.fillBranch("%s_pt_jes%sUp" % (self.metBranchName, jesUncertainty), math.sqrt(met_px_jesUp[jesUncertainty]**2 + met_py_jesUp[jesUncertainty]**2))
            self.out.fillBranch("%s_phi_jes%sUp" % (self.metBranchName, jesUncertainty), math.atan2(met_py_jesUp[jesUncertainty], met_px_jesUp[jesUncertainty]))
            self.out.fillBranch("%s_pt_jes%sDown" % (self.jetBranchName, jesUncertainty), jets_pt_jesDown[jesUncertainty])
            self.out.fillBranch("%s_pt_jes%sDown" % (self.metBranchName, jesUncertainty), math.sqrt(met_px_jesDown[jesUncertainty]**2 + met_py_jesDown[jesUncertainty]**2))
            self.out.fillBranch("%s_phi_jes%sDown" % (self.metBranchName, jesUncertainty), math.atan2(met_py_jesDown[jesUncertainty], met_px_jesDown[jesUncertainty]))
        self.out.fillBranch("%s_pt_unclustEnUp" % self.metBranchName, math.sqrt(met_px_unclEnUp**2 + met_py_unclEnUp**2))
        self.out.fillBranch("%s_phi_unclustEnUp" % self.metBranchName, math.atan2(met_py_unclEnUp, met_px_unclEnUp))
        self.out.fillBranch("%s_pt_unclustEnDown" % self.metBranchName, math.sqrt(met_px_unclEnDown**2 + met_py_unclEnDown**2))
        self.out.fillBranch("%s_phi_unclustEnDown" % self.metBranchName, math.atan2(met_py_unclEnDown, met_px_unclEnDown))

        return True

jesUncertaintySources = [
    "AbsoluteStat",
    "AbsoluteScale",
    "AbsoluteFlavMap",
    "AbsoluteMPFBias",
    "Fragmentation",
    "SinglePionECAL",
    "SinglePionHCAL",
    "FlavorQCD",
    "TimePtEta",
    "RelativeJEREC1",
    "RelativeJEREC2",
    "RelativeJERHF",
    "RelativePtBB",
    "RelativePtEC1",
    "RelativePtEC2",
    "RelativePtHF",
    "RelativeBal",
    "RelativeFSR",
    "RelativeStatFSR",
    "RelativeStatEC",
    "RelativeStatHF",
    "PileUpDataMC",
    "PileUpPtRef",
    "PileUpPtBB",
    "PileUpPtEC1",
    "PileUpPtEC2",
    "PileUpPtHF",
    "PileUpMuZero",
    "PileUpEnvelope",
    "SubTotalPileUp",
    "SubTotalRelative",
    "SubTotalPt",
    "SubTotalScale",
    "SubTotalAbsolute",
    "SubTotalMC",
    "Total",
    "TotalNoFlavor",
    "TotalNoTime",
    "TotalNoFlavorNoTime",
    "FlavorZJet",
    "FlavorPhotonJet",
    "FlavorPureGluon",
    "FlavorPureQuark",
    "FlavorPureCharm",
    "FlavorPureBottom",
    "TimeRunBCD",
    "TimeRunEF",
    "TimeRunG",
    "TimeRunH",
    "CorrelationGroupMPFInSitu",
    "CorrelationGroupIntercalibration",
    "CorrelationGroupbJES",
    "CorrelationGroupFlavor",
    "CorrelationGroupUncorrelated",
]

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

jetmetUncertainties2016 = lambda : jetmetUncertaintiesProducer("2016", "Summer16_23Sep2016V4_MC", [ "Total" ])
jetmetUncertainties2016All = lambda : jetmetUncertaintiesProducer("2016", "Summer16_23Sep2016V4_MC", jesUncertaintySources)
jetmetUncertainties2017 = lambda : jetmetUncertaintiesProducer("2017", "Fall17_17Nov2017_V4_MC", [ "Total" ])
jetmetUncertainties2017All = lambda : jetmetUncertaintiesProducer("2017", "Summer16_23Sep2016V4_MC", jesUncertaintySources)

