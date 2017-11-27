import ROOT
import math, os
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import matchObjectCollection

class jetSmearer(Module):
    def __init__(self, globalTag, jetType = "AK4PFchs", jerInputFileName = "Spring16_25nsV10_MC_PtResolution_AK4PFchs.txt", jerUncertaintyInputFileName = "Spring16_25nsV10_MC_SF_AK4PFchs.txt"):

        #--------------------------------------------------------------------------------------------
        # CV: globalTag and jetType not yet used, as there is no consistent set of txt files for
        #     JES uncertainties and JER scale factors and uncertainties yet
        #--------------------------------------------------------------------------------------------

        # read jet energy resolution (JER) and JER scale factors and uncertainties
        # (the txt files were downloaded from https://github.com/cms-jet/JRDatabase/tree/master/textFiles/Spring16_25nsV10_MC )
        self.jerInputFilePath = os.environ['CMSSW_BASE'] + "/src/PhysicsTools/NanoAODTools/data/jme/"
        self.jerInputFileName = jerInputFileName
        self.jerUncertaintyInputFileName = jerUncertaintyInputFileName

        self.params_sf_and_uncertainty = ROOT.PyJetParametersWrapper()
        self.params_resolution = ROOT.PyJetParametersWrapper()

        # initialize random number generator
        # (needed for jet pT smearing)
        self.rnd = ROOT.TRandom3(12345)

        # load libraries for accessing JER scale factors and uncertainties from txt files
        for library in [ "libCondFormatsJetMETObjects", "libPhysicsToolsNanoAODTools" ]:
            if library not in ROOT.gSystem.GetLibraries():
                print("Load Library '%s'" % library.replace("lib", ""))
                ROOT.gSystem.Load(library)

    def beginJob(self):

        # initialize JER scale factors and uncertainties
        # (cf. PhysicsTools/PatUtils/interface/SmearedJetProducerT.h )
        print("Loading jet energy resolutions (JER) from file '%s'" % os.path.join(self.jerInputFilePath, self.jerInputFileName))
        self.jer = ROOT.PyJetResolutionWrapper(os.path.join(self.jerInputFilePath, self.jerInputFileName))
        print("Loading JER scale factors and uncertainties from file '%s'" % os.path.join(self.jerInputFilePath, self.jerUncertaintyInputFileName))
        self.jerSF_and_Uncertainty = ROOT.PyJetResolutionScaleFactorWrapper(os.path.join(self.jerInputFilePath, self.jerUncertaintyInputFileName))

    def endJob(self):
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

        self.params_resolution.setJetPt(jet.pt)
        self.params_resolution.setJetEta(jet.eta)
        self.params_resolution.setRho(rho)
        jet_pt_resolution = self.jer.getResolution(self.params_resolution)

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
            self.params_sf_and_uncertainty.setJetEta(jet.eta)
            jet_pt_sf_and_uncertainty[central_or_shift] = self.jerSF_and_Uncertainty.getScaleFactor(self.params_sf_and_uncertainty, enum_central_or_shift)

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
                sigma = jet_pt_resolution*math.sqrt(jet_pt_sf_and_uncertainty[central_or_shift]**2 - 1.)
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
    
