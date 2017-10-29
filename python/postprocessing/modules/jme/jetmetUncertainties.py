import ROOT
import math, os
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

#----------------------------------------------------------------------------------------------------
# CV: global functions copied from PhysicsTools/HeppyCore/python/utils/deltar.py

def deltaPhi(p1, p2):
    '''Computes delta phi, handling periodic limit conditions.'''
    res = p1 - p2
    while res > math.pi:
        res -= 2*math.pi
    while res < -math.pi:
        res += 2*math.pi
    return res

def deltaR2(e1, p1, e2=None, p2=None):
    '''Take either 4 arguments (eta,phi, eta,phi) or two particles that have 'eta', 'phi' methods)'''
    if (e2 == None and p2 == None):
        return deltaR2(e1.eta, e1.phi, p1.eta, p1.phi)
    de = e1 - e2
    dp = deltaPhi(p1, p2)
    return de*de + dp*dp

def bestMatch(ptc, matchCollection):
    '''Return the best match to ptc in matchCollection,
    which is the closest ptc in delta R,
    together with the squared distance dR2 between ptc
    and the match.'''
    deltaR2Min = float('+inf')
    bm = None
    for match in matchCollection:
        dR2 = deltaR2(ptc, match)
        if dR2 < deltaR2Min:
            deltaR2Min = dR2
            bm = match
    return bm, deltaR2Min

def matchObjectCollection(ptcs, matchCollection, deltaRMax = 0.4, filter = lambda x,y : True):
    pairs = {}
    if len(ptcs)==0:
        return pairs
    if len(matchCollection)==0:
        return dict( list(zip(ptcs, [None]*len(ptcs))) )
    dR2Max = deltaRMax ** 2
    for ptc in ptcs:
        bm, dr2 = bestMatch( ptc, [ mob for mob in matchCollection if filter(object,mob) ] )
        if dr2 < dR2Max:
            pairs[ptc] = bm
        else:
            pairs[ptc] = None
    return pairs
#----------------------------------------------------------------------------------------------------

def square(x):
    return x*x

class jetmetUncertaintiesProducer(Module):
    def __init__(self, globalTag, jesUncertainties = [ "Total" ], jetType = "AK4PFchs"):

        #--------------------------------------------------------------------------------------------
        # CV: gloabTag and jetType not yet used, as there is no consistent set of txt files for
        #     JES uncertainties and JER scale factors and uncertainties yet
        #--------------------------------------------------------------------------------------------

        self.jesUncertainties = jesUncertainties

        # smear jet pT to account for measured difference in JER between data and simulation.
        self.applyJERCorr = True

        self.jetBranchName = "Jet"
        self.genJetBranchName = "GenJet"
        self.metBranchName = "MET"
        self.rhoBranchName = "fixedGridRhoFastjetAll"

        # read jet energy scale (JES) uncertainties
        self.jesInputFilePath = os.environ['CMSSW_BASE'] + "/src/PhysicsTools/NanoAODTools/data/jme/"
        if len(jesUncertainties) == 1 and jesUncertainties[0] == "Total":
            self.jesUncertaintyInputFileName = "Summer16_23Sep2016V4_MC_Uncertainty_AK4PFchs.txt"
        else:
            self.jesUncertaintyInputFileName = "Summer16_23Sep2016V4_MC_UncertaintySources_AK4PFchs.txt"

        # read jet energy resolution (JER) and JER scale factors and uncertainties
        # (the txt files were downloaded from https://github.com/cms-jet/JRDatabase/tree/master/textFiles/Spring16_25nsV10_MC )
        self.jerInputFilePath = os.environ['CMSSW_BASE'] + "/src/PhysicsTools/NanoAODTools/data/jme/"
        self.jerInputFileName = "Spring16_25nsV10_MC_PtResolution_AK4PFchs.txt" 
        self.jerUncertaintyInputFileName = "Spring16_25nsV10_MC_SF_AK4PFchs.txt"

        # initialize random number generator
        # (needed for jet pT smearing)
        self.rnd = ROOT.TRandom3(12345)

        # define energy threshold below which jets are considered as "unclustered energy"
        # (cf. JetMETCorrections/Type1MET/python/correctionTermsPfMetType1Type2_cff.py )
        self.unclEnThreshold = 15.

        # load libraries for accessing JES and JER scale factors and uncertainties from txt files
        for library in [ "libCondFormatsJetMETObjects", "libPhysicsToolsNanoAODTools" ]:
            if library not in ROOT.gSystem.GetLibraries():
                print("Load Library '%s'" % library.replace("lib", ""))
                ROOT.gSystem.Load(library)

    def beginJob(self):

        print("Loading jet energy scale (JES) uncertainties from file '%s'" % os.path.join(self.jesInputFilePath, self.jesUncertaintyInputFileName))
        self.jesUncertainty = ROOT.JetCorrectionUncertainty(os.path.join(self.jesInputFilePath, self.jesUncertaintyInputFileName))

        # initialize JER scale factors and uncertainties
        # (cf. PhysicsTools/PatUtils/interface/SmearedJetProducerT.h )
        print("Loading jet energy resolutions (JER) from file '%s'" % os.path.join(self.jerInputFilePath, self.jerInputFileName))
        self.jer = ROOT.PyJetResolutionWrapper(os.path.join(self.jerInputFilePath, self.jerInputFileName))
        print("Loading JER scale factors and uncertainties from file '%s'" % os.path.join(self.jerInputFilePath, self.jerUncertaintyInputFileName))
        self.jerSF_and_Uncertainty = ROOT.PyJetResolutionScaleFactorWrapper(os.path.join(self.jerInputFilePath, self.jerUncertaintyInputFileName))

    def endJob(self):
        pass

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

    def getSmearedJetPt(self, jet, genJet, rho):

        #--------------------------------------------------------------------------------------------
        # CV: Smear jet pT to account for measured difference in JER between data and simulation.
        #     The function computes the nominal smeared jet pT simultaneously with the JER up and down shifts,
        #     in order to use the same random number to smear all three (for consistency reasons).
        #
        #     The implementation of this function follows PhysicsTools/PatUtils/interface/SmearedJetProducerT.h 
        #
        #--------------------------------------------------------------------------------------------

        if not (jet.pt > 0.):
            print("WARNING: jet pT = %1.1f !!" % jet.pt)
            return ( jet.pt, jet.pt, jet.pt )
        
        #--------------------------------------------------------------------------------------------
        # CV: define enums needed to access JER scale factors and uncertainties
        #    (cf. CondFormats/JetMETObjects/interface/JetResolutionObject.h) 
        enum_nominal         = 0
        enum_shift_up        = 2
        enum_shift_down      = 1
        #--------------------------------------------------------------------------------------------

        params_resolution = ROOT.PyJetParametersWrapper()
        params_resolution.setJetPt(jet.pt)
        params_resolution.setJetEta(jet.eta)
        params_resolution.setRho(rho)
        jet_pt_resolution = self.jer.getResolution(params_resolution)

        jet_pt_sf_and_uncertainty = {}
        for central_or_shift in [ 'nominal', 'jerUp', 'jerDown' ]:
            enum_central_or_shift = None
            if central_or_shift == "nominal":
                enum_central_or_shift = enum_nominal
            elif central_or_shift == "jerUp":
                enum_central_or_shift = enum_shift_up
            elif central_or_shift == "jerDown":
                enum_central_or_shift = enum_shift_down
            else:
                raise ValueError("ERROR: Undefined central_or_shift = '%s' !!" % central_or_shift)
            params_sf_and_uncertainty = ROOT.PyJetParametersWrapper()
            params_sf_and_uncertainty.setJetEta(jet.eta)
            jet_pt_sf_and_uncertainty[central_or_shift] = self.jerSF_and_Uncertainty.getScaleFactor(params_sf_and_uncertainty, enum_central_or_shift)

        # generate random number with flat distribution between 0 and 1
        u = self.rnd.Rndm()

        jet_pt_smeared = {}
        for central_or_shift in [ 'nominal', 'jerUp', 'jerDown' ]:

            smearFactor = None
            if genJet:
                #
                # Case 1: we have a "good" generator level jet matched to the reconstructed jet
                #
                dPt = jet.pt - genJet.pt
                smearFactor = 1. + (jet_pt_sf_and_uncertainty[central_or_shift] - 1.)*dPt/jet.pt
            elif jet_pt_sf_and_uncertainty[central_or_shift] > 1.:
                #
                # Case 2: we don't have a generator level jet. Smear jet pT using a random Gaussian variation
                #
                sigma = jet_pt_resolution*math.sqrt(square(jet_pt_sf_and_uncertainty[central_or_shift]) - 1.)
                smearFactor = 1. + u
            else:
                #
                # Case 3: we cannot smear this jet, as we don't have a generator level jet and the resolution in data is better than the resolution in the simulation,
                #         so we would need to randomly "unsmear" the jet, which is impossible
                #
                smearFactor = 1.

            # check that smeared jet energy remains positive,
            # as the direction of the jet would change ("flip") otherwise - and this is not what we want
            if (smearFactor*jet.pt) < 1.e-2:
                smearFactor = 1.e-2/jet.pt

            jet_pt_smeared[central_or_shift] = smearFactor*jet.pt
        
        return ( jet_pt_smeared['nominal'], jet_pt_smeared['jerUp'], jet_pt_smeared['jerDown'] )
    
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
            ( jet_pt_smeared, jet_pt_jerUp, jet_pt_jerDown ) = self.getSmearedJetPt(jet, genJet, rho)
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
                self.jesUncertainty.setJetPt(jet_pt_ref)
                self.jesUncertainty.setJetEta(jet.eta)
                delta = self.jesUncertainty.getUncertainty(True)
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
        self.out.fillBranch("%s_pt_smeared" % self.metBranchName, math.sqrt(square(met_px_smeared) + square(met_py_smeared)))
        self.out.fillBranch("%s_phi_smeared" % self.metBranchName, math.atan2(met_py_smeared, met_px_smeared))
        self.out.fillBranch("%s_pt_jerUp" % self.jetBranchName, jets_pt_jerUp)
        self.out.fillBranch("%s_pt_jerUp" % self.metBranchName, math.sqrt(square(met_px_jerUp) + square(met_py_jerUp)))
        self.out.fillBranch("%s_phi_jerUp" % self.metBranchName, math.atan2(met_py_jerUp, met_px_jerUp))
        self.out.fillBranch("%s_pt_jerDown" % self.jetBranchName, jets_pt_jerDown)
        self.out.fillBranch("%s_pt_jerDown" % self.metBranchName, math.sqrt(square(met_px_jerDown) + square(met_py_jerDown)))
        self.out.fillBranch("%s_phi_jerDown" % self.metBranchName, math.atan2(met_py_jerDown, met_px_jerDown))
        for jesUncertainty in self.jesUncertainties:
            self.out.fillBranch("%s_pt_jes%sUp" % (self.jetBranchName, jesUncertainty), jets_pt_jesUp[jesUncertainty])
            self.out.fillBranch("%s_pt_jes%sUp" % (self.metBranchName, jesUncertainty), math.sqrt(square(met_px_jesUp[jesUncertainty]) + square(met_py_jesUp[jesUncertainty])))
            self.out.fillBranch("%s_phi_jes%sUp" % (self.metBranchName, jesUncertainty), math.atan2(met_py_jesUp[jesUncertainty], met_px_jesUp[jesUncertainty]))
            self.out.fillBranch("%s_pt_jes%sDown" % (self.jetBranchName, jesUncertainty), jets_pt_jesDown[jesUncertainty])
            self.out.fillBranch("%s_pt_jes%sDown" % (self.metBranchName, jesUncertainty), math.sqrt(square(met_px_jesDown[jesUncertainty]) + square(met_py_jesDown[jesUncertainty])))
            self.out.fillBranch("%s_phi_jes%sDown" % (self.metBranchName, jesUncertainty), math.atan2(met_py_jesDown[jesUncertainty], met_px_jesDown[jesUncertainty]))
        self.out.fillBranch("%s_pt_unclustEnUp" % self.metBranchName, math.sqrt(square(met_px_unclEnUp) + square(met_py_unclEnUp)))
        self.out.fillBranch("%s_phi_unclustEnUp" % self.metBranchName, math.atan2(met_py_unclEnUp, met_px_unclEnUp))
        self.out.fillBranch("%s_pt_unclustEnDown" % self.metBranchName, math.sqrt(square(met_px_unclEnDown) + square(met_py_unclEnDown)))
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

jetmetUncertainties = lambda : jetmetUncertaintiesProducer("Summer16_23Sep2016V4_MC", [ "Total" ])
jetmetUncertaintiesAll = lambda : jetmetUncertaintiesProducer("Summer16_23Sep2016V4_MC", jesUncertaintySources)
