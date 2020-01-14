import ROOT
import math, os, tarfile, tempfile, shutil
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import matchObjectCollection, matchObjectCollectionMultiple

class jetSmearer(Module):
    def __init__(self, globalTag, jetType = "AK4PFchs", jerInputFileName = "Spring16_25nsV10_MC_PtResolution_AK4PFchs.txt", jerUncertaintyInputFileName = "Spring16_25nsV10_MC_SF_AK4PFchs.txt", jmr_vals=[1.09, 1.14, 1.04]):
        
        #--------------------------------------------------------------------------------------------
        # CV: globalTag and jetType not yet used, as there is no consistent set of txt files for
        #     JES uncertainties and JER scale factors and uncertainties yet
        #--------------------------------------------------------------------------------------------
        
        # read jet energy resolution (JER) and JER scale factors and uncertainties
        # (the txt files were downloaded from https://github.com/cms-jet/JRDatabase/tree/master/textFiles/ )
        # Text files are now tarred so must extract first
        self.jerInputArchivePath = os.environ['CMSSW_BASE'] + "/src/PhysicsTools/NanoAODTools/data/jme/"
        self.jerTag = jerInputFileName[:jerInputFileName.find('_MC_')+len('_MC')]
        self.jerArchive = tarfile.open(self.jerInputArchivePath+self.jerTag+".tgz", "r:gz")
        self.jerInputFilePath = tempfile.mkdtemp()
        self.jerArchive.extractall(self.jerInputFilePath)
        self.jerInputFileName = jerInputFileName
        self.jerUncertaintyInputFileName = jerUncertaintyInputFileName
        
        self.jmr_vals = jmr_vals
        
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
        
        self.puppiJMRFile = ROOT.TFile.Open(os.environ['CMSSW_BASE'] + "/src/PhysicsTools/NanoAODTools/data/jme/puppiSoftdropResol.root")
        self.puppisd_resolution_cen = self.puppiJMRFile.Get("massResolution_0eta1v3")
        self.puppisd_resolution_for = self.puppiJMRFile.Get("massResolution_1v3eta2v5")
        
    def beginJob(self):
        # initialize JER scale factors and uncertainties
        # (cf. PhysicsTools/PatUtils/interface/SmearedJetProducerT.h )
        print("Loading jet energy resolutions (JER) from file '%s'" % os.path.join(self.jerInputFilePath, self.jerInputFileName))
        self.jer = ROOT.PyJetResolutionWrapper(os.path.join(self.jerInputFilePath, self.jerInputFileName))
        print("Loading JER scale factors and uncertainties from file '%s'" % os.path.join(self.jerInputFilePath, self.jerUncertaintyInputFileName))
        self.jerSF_and_Uncertainty = ROOT.PyJetResolutionScaleFactorWrapper(os.path.join(self.jerInputFilePath, self.jerUncertaintyInputFileName))
        
    def endJob(self):
        shutil.rmtree(self.jerInputFilePath)

    def setSeed(self,event):
        """Set seed deterministically."""
        # (cf. https://github.com/cms-sw/cmssw/blob/master/PhysicsTools/PatUtils/interface/SmearedJetProducerT.h)
        runnum  = long(event.run) << 20
        luminum = long(event.luminosityBlock) << 10
        evtnum  = event.event
        jet0eta = long(event.Jet_eta[0]/0.01 if event.nJet>0 else 0)
        seed    = 1L + runnum + evtnum + luminum + jet0eta
        self.rnd.SetSeed(seed)
        
    
    def getSmearedJetPt(self, jet, genJet, rho):
        ( jet_pt_nomVal, jet_pt_jerUpVal, jet_pt_jerDownVal ) = self.getSmearValsPt( jet, genJet, rho )
        return ( jet_pt_nomVal*jet.pt, jet_pt_jerUpVal*jet.pt, jet_pt_jerDownVal*jet.pt )
        
    
    def getSmearValsPt(self, jetIn, genJetIn, rho):
        
        if hasattr( jetIn, "p4"):
            jet = jetIn.p4()
        else:
            jet = jetIn
        if hasattr( genJetIn, "p4"):
            genJet = genJetIn.p4()
        else:
            genJet = genJetIn
        
        #--------------------------------------------------------------------------------------------
        # CV: Smear jet pT to account for measured difference in JER between data and simulation.
        #     The function computes the nominal smeared jet pT simultaneously with the JER up and down shifts,
        #     in order to use the same random number to smear all three (for consistency reasons).
        #
        #     The implementation of this function follows PhysicsTools/PatUtils/interface/SmearedJetProducerT.h 
        #
        #--------------------------------------------------------------------------------------------

        if not (jet.Perp() > 0.):
            print("WARNING: jet pT = %1.1f !!" % jet.Perp())
            return ( jet.Perp(), jet.Perp(), jet.Perp() )
        
        #--------------------------------------------------------------------------------------------
        # CV: define enums needed to access JER scale factors and uncertainties
        #    (cf. CondFormats/JetMETObjects/interface/JetResolutionObject.h) 
        enum_nominal         = 0
        enum_shift_up        = 2
        enum_shift_down      = 1
        #--------------------------------------------------------------------------------------------
        
        jet_pt_sf_and_uncertainty = {}
        for enum_central_or_shift in [ enum_nominal, enum_shift_up, enum_shift_down ]:
            self.params_sf_and_uncertainty.setJetEta(jet.Eta())
            self.params_sf_and_uncertainty.setJetPt(jet.Pt()) # Added bc. of pt dependency in 2018. Thanks to kschweiger!
            jet_pt_sf_and_uncertainty[enum_central_or_shift] = self.jerSF_and_Uncertainty.getScaleFactor(self.params_sf_and_uncertainty, enum_central_or_shift)
        
        smear_vals = {}
        if genJet:
          for central_or_shift in [ enum_nominal, enum_shift_up, enum_shift_down ]:
              #
              # Case 1: we have a "good" generator level jet matched to the reconstructed jet
              #
              dPt = jet.Perp() - genJet.Perp()
              smearFactor = 1. + (jet_pt_sf_and_uncertainty[central_or_shift] - 1.)*dPt/jet.Perp()
              
              # check that smeared jet energy remains positive,
              # as the direction of the jet would change ("flip") otherwise - and this is not what we want
              if (smearFactor*jet.Perp()) < 1.e-2:
                smearFactor = 1.e-2
              smear_vals[central_or_shift] = smearFactor
              
        else:
          self.params_resolution.setJetPt(jet.Perp())
          self.params_resolution.setJetEta(jet.Eta())
          self.params_resolution.setRho(rho)
          jet_pt_resolution = self.jer.getResolution(self.params_resolution)
          
          rand = self.rnd.Gaus(0,jet_pt_resolution)
          for central_or_shift in [ enum_nominal, enum_shift_up, enum_shift_down ]:
            if jet_pt_sf_and_uncertainty[central_or_shift] > 1.:
              #
              # Case 2: we don't have a generator level jet. Smear jet pT using a random Gaussian variation
              #
              smearFactor = 1. + rand * math.sqrt(jet_pt_sf_and_uncertainty[central_or_shift]**2 - 1.)
            else:
              #
              # Case 3: we cannot smear this jet, as we don't have a generator level jet and the resolution in data is better than the resolution in the simulation,
              #         so we would need to randomly "unsmear" the jet, which is impossible
              #
              smearFactor = 1.
            
            # check that smeared jet energy remains positive,
            # as the direction of the jet would change ("flip") otherwise - and this is not what we want
            if (smearFactor*jet.Perp()) < 1.e-2:
                smearFactor = 1.e-2
            smear_vals[central_or_shift] = smearFactor
        
        return ( smear_vals[enum_nominal], smear_vals[enum_shift_up], smear_vals[enum_shift_down] )
        
    
    def getSmearValsM(self, jetIn, genJetIn):
        
        #--------------------------------------------------------------------------------------------
        # LC: Procedure outline in https://twiki.cern.ch/twiki/bin/view/Sandbox/PUPPIJetMassScaleAndResolution
        #--------------------------------------------------------------------------------------------
        
        if hasattr( jetIn, "p4"):
            jet = jetIn.p4()
        else:
            jet = jetIn
        if hasattr( genJetIn, "p4"):
            genJet = genJetIn.p4()
        else:
            genJet = genJetIn
        
        #--------------------------------------------------------------------------------------------
        # CV: Smear jet m to account for measured difference in JER between data and simulation.
        #     The function computes the nominal smeared jet m simultaneously with the JER up and down shifts,
        #     in order to use the same random number to smear all three (for consistency reasons).
        #
        #     The implementation of this function follows PhysicsTools/PatUtils/interface/SmearedJetProducerT.h 
        #
        #--------------------------------------------------------------------------------------------
        
        if not (jet.M() > 0.):
            print("WARNING: jet m = %1.1f !!" % jet.M())
            return ( jet.M(), jet.M(), jet.M() )
        
        #--------------------------------------------------------------------------------------------
        # CV: define enums needed to access JER scale factors and uncertainties
        #    (cf. CondFormats/JetMETObjects/interface/JetResolutionObject.h) 
        enum_nominal         = 0
        enum_shift_up        = 2
        enum_shift_down      = 1
        #--------------------------------------------------------------------------------------------
        
        jet_m_sf_and_uncertainty = dict( zip( [enum_nominal, enum_shift_up, enum_shift_down], self.jmr_vals ) )
        
        smear_vals = {}
        if genJet:
          for central_or_shift in [ enum_nominal, enum_shift_up, enum_shift_down ]:
              #
              # Case 1: we have a "good" generator level jet matched to the reconstructed jet
              #
              dM = jet.M() - genJet.M()
              smearFactor = 1. + (jet_m_sf_and_uncertainty[central_or_shift] - 1.)*dM/jet.M()
              
              # check that smeared jet energy remains positive,
              # as the direction of the jet would change ("flip") otherwise - and this is not what we want
              if (smearFactor*jet.M()) < 1.e-2:
                smearFactor = 1.e-2
              smear_vals[central_or_shift] = smearFactor
            
        else:        
          # Get mass resolution
          if abs(jet.Eta()) <= 1.3:
            jet_m_resolution = self.puppisd_resolution_cen.Eval( jet.Pt() )
          else:
            jet_m_resolution = self.puppisd_resolution_for.Eval( jet.Pt() )
          rand = self.rnd.Gaus(0,jet_m_resolution)
          for central_or_shift in [ enum_nominal, enum_shift_up, enum_shift_down ]:
            if jet_m_sf_and_uncertainty[central_or_shift] > 1.:
              #
              # Case 2: we don't have a generator level jet. Smear jet m using a random Gaussian variation
              #
              smearFactor = rand * math.sqrt(jet_m_sf_and_uncertainty[central_or_shift]**2 - 1.)
            else:
              #
              # Case 3: we cannot smear this jet, as we don't have a generator level jet and the resolution in data is better than the resolution in the simulation,
              #         so we would need to randomly "unsmear" the jet, which is impossible
              #
              smearFactor = 1.
            
            # check that smeared jet energy remains positive,
            # as the direction of the jet would change ("flip") otherwise - and this is not what we want
            if (smearFactor*jet.M()) < 1.e-2:
               smearFactor = 1.e-2
            smear_vals[central_or_shift] = smearFactor
        
        return ( smear_vals[enum_nominal], smear_vals[enum_shift_up], smear_vals[enum_shift_down] )
    

