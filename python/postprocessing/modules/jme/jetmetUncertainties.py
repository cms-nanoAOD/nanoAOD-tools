import ROOT
import math, os,re, tarfile, tempfile, shutil
import numpy as np
import itertools
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import matchObjectCollection, matchObjectCollectionMultiple
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetSmearer import jetSmearer
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.JetReCalibrator import JetReCalibrator

class jetmetUncertaintiesProducer(Module):
    def __init__(self, era, globalTag, jesUncertainties = [ "Total" ], archive=None, globalTagProd=None, jetType = "AK4PFchs", metBranchName="MET", jerTag="", isData=False, applySmearing=True):

        # globalTagProd only needs to be defined if METFixEE2017 is to be recorrected, and should be the GT that was used for the production of the nanoAOD files
        self.era = era
        self.isData = isData
        self.applySmearing = applySmearing if not isData else False # if set to true, Jet_pt_nom will have JER applied. not to be switched on for data.

        self.metBranchName = metBranchName
        self.rhoBranchName = "fixedGridRhoFastjetAll"
        #--------------------------------------------------------------------------------------------
        # CV: globalTag and jetType not yet used in the jet smearer, as there is no consistent set of 
        #     txt files for JES uncertainties and JER scale factors and uncertainties yet
        #--------------------------------------------------------------------------------------------

        self.jesUncertainties = jesUncertainties

        # smear jet pT to account for measured difference in JER between data and simulation.
        if jerTag != "":
            self.jerInputFileName = jerTag + "_PtResolution_" + jetType + ".txt"
            self.jerUncertaintyInputFileName = jerTag + "_SF_"  + jetType + ".txt"
        else:
            print "WARNING: jerTag is empty!!! This module will soon be deprecated! Please use jetmetHelperRun2 in the future."
            if era == "2016":
                self.jerInputFileName = "Summer16_25nsV1_MC_PtResolution_" + jetType + ".txt"
                self.jerUncertaintyInputFileName = "Summer16_25nsV1_MC_SF_" + jetType + ".txt"
            elif era == "2017" or era == "2018": ## use 2017 JER for 2018 for the time being
                self.jerInputFileName = "Fall17_V3_MC_PtResolution_" + jetType + ".txt"
                self.jerUncertaintyInputFileName = "Fall17_V3_MC_SF_" + jetType + ".txt"
            elif era == "2018" and False: ## jetSmearer not working with 2018 JERs yet
                self.jerInputFileName = "Autumn18_V7_MC_PtResolution_" + jetType + ".txt"
                self.jerUncertaintyInputFileName = "Autumn18_V7_MC_SF_" + jetType + ".txt"

        self.jetSmearer = jetSmearer(globalTag, jetType, self.jerInputFileName, self.jerUncertaintyInputFileName)

        if "AK4" in jetType : 
            self.jetBranchName = "Jet"
            self.genJetBranchName = "GenJet"
            self.genSubJetBranchName = None
        else:
            raise ValueError("ERROR: Invalid jet type = '%s'!" % jetType)
        self.lenVar = "n" + self.jetBranchName

        # read jet energy scale (JES) uncertainties
        # (downloaded from https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC )
        self.jesInputArchivePath = os.environ['CMSSW_BASE'] + "/src/PhysicsTools/NanoAODTools/data/jme/"
        # Text files are now tarred so must extract first into temporary directory (gets deleted during python memory management at script exit)
        self.jesArchive = tarfile.open(self.jesInputArchivePath+globalTag+".tgz", "r:gz") if not archive else tarfile.open(self.jesInputArchivePath+archive+".tgz", "r:gz")
        self.jesInputFilePath = tempfile.mkdtemp()
        self.jesArchive.extractall(self.jesInputFilePath)
        
        # to fully re-calculate type-1 MET the JEC that are currently applied are also needed. IS THAT EVEN CORRECT?


        if len(jesUncertainties) == 1 and jesUncertainties[0] == "Total":
            self.jesUncertaintyInputFileName = globalTag + "_Uncertainty_" + jetType + ".txt"
        else:
            self.jesUncertaintyInputFileName = globalTag + "_UncertaintySources_" + jetType + ".txt"

        # read all uncertainty source names from the loaded file
        if jesUncertainties[0] == "All":
            with open(self.jesInputFilePath+'/'+self.jesUncertaintyInputFileName) as f:
                lines = f.read().split("\n")
                sources = filter(lambda x: x.startswith("[") and x.endswith("]"), lines)
                sources = map(lambda x: x[1:-1], sources)
                self.jesUncertainties = sources

        # Define the jet recalibrator            
        self.jetReCalibrator = JetReCalibrator(globalTag, jetType , True, self.jesInputFilePath, calculateSeparateCorrections = False, calculateType1METCorrection  = False)

        # Define the recalibrator for level 1 corrections only
        self.jetReCalibratorL1  = JetReCalibrator(globalTag, jetType , False, self.jesInputFilePath, calculateSeparateCorrections = True, calculateType1METCorrection  = False, upToLevel=1)

        # Define the recalibrators for GT used in nanoAOD production (only needed to reproduce 2017 v2 MET)
        if globalTagProd:
          self.jetReCalibratorProd    = JetReCalibrator(globalTagProd, jetType , True, self.jesInputFilePath, calculateSeparateCorrections = False, calculateType1METCorrection  = False)
          self.jetReCalibratorProdL1  = JetReCalibrator(globalTagProd, jetType , False, self.jesInputFilePath, calculateSeparateCorrections = True, calculateType1METCorrection  = False, upToLevel=1)
        else:
          self.jetReCalibratorProd    = False
          self.jetReCalibratorProdL1  = False

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
            jesUncertainty_label = jesUncertainty
            if jesUncertainty == 'Total' and len(self.jesUncertainties) == 1:
                jesUncertainty_label = ''
            pars = ROOT.JetCorrectorParameters(os.path.join(self.jesInputFilePath, self.jesUncertaintyInputFileName),jesUncertainty_label)
            self.jesUncertainty[jesUncertainty] = ROOT.JetCorrectionUncertainty(pars)    

        if not self.isData:
            self.jetSmearer.beginJob()

    def endJob(self):
        if not self.isData:
            self.jetSmearer.endJob()
        shutil.rmtree(self.jesInputFilePath)

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("%s_pt_raw" % self.jetBranchName, "F", lenVar=self.lenVar)
        self.out.branch("%s_pt_nom" % self.jetBranchName, "F", lenVar=self.lenVar)
        self.out.branch("%s_mass_raw" % self.jetBranchName, "F", lenVar=self.lenVar)
        self.out.branch("%s_mass_nom" % self.jetBranchName, "F", lenVar=self.lenVar)
        self.out.branch("%s_corr_JEC" % self.jetBranchName, "F", lenVar=self.lenVar)
        self.out.branch("%s_corr_JER" % self.jetBranchName, "F", lenVar=self.lenVar)

        self.out.branch("%s_pt_nom" % self.metBranchName, "F")
        self.out.branch("%s_phi_nom" % self.metBranchName, "F")

        if not self.isData:
          self.out.branch("%s_pt_jer" % self.metBranchName, "F")
          self.out.branch("%s_phi_jer" % self.metBranchName, "F")
        
          for shift in [ "Up", "Down" ]:
              self.out.branch("%s_pt_jer%s" % (self.jetBranchName, shift), "F", lenVar=self.lenVar)
              self.out.branch("%s_mass_jer%s" % (self.jetBranchName, shift), "F", lenVar=self.lenVar)
              
              self.out.branch("%s_pt_jer%s" % (self.metBranchName, shift), "F")
              self.out.branch("%s_phi_jer%s" % (self.metBranchName, shift), "F")
              for jesUncertainty in self.jesUncertainties:
                  self.out.branch("%s_pt_jes%s%s" % (self.jetBranchName, jesUncertainty, shift), "F", lenVar=self.lenVar)
                  self.out.branch("%s_mass_jes%s%s" % (self.jetBranchName, jesUncertainty, shift), "F", lenVar=self.lenVar)

                  self.out.branch("%s_pt_jes%s%s" % (self.metBranchName, jesUncertainty, shift), "F")
                  self.out.branch("%s_phi_jes%s%s" % (self.metBranchName, jesUncertainty, shift), "F")
              self.out.branch("%s_pt_unclustEn%s" % (self.metBranchName, shift), "F")
              self.out.branch("%s_phi_unclustEn%s" % (self.metBranchName, shift), "F")
                        
        self.isV5NanoAOD = hasattr(inputTree, "Jet_muonSubtrFactor")
        print "nanoAODv5?", self.isV5NanoAOD


    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets      = Collection(event, self.jetBranchName )
        nJet      = event.nJet
        lowPtJets = Collection(event, "CorrT1METJet" ) if self.isV5NanoAOD else []
        muons     = Collection(event, "Muon" ) # to subtract out of the jets for proper type-1 MET corrections
        if not self.isData:
          genJets   = Collection(event, self.genJetBranchName )
        
        # prepare the low pt jets (they don't have a rawFactor)
        for jet in lowPtJets:
          jet.pt        = jet.rawPt
          jet.rawFactor = 0
          jet.mass      = 0
          # the following dummy values should be removed once the values are kept in nanoAOD
          jet.neEmEF    = 0
          jet.chEmEF    = 0

        if not self.isData:
            self.jetSmearer.setSeed(event)
        
        jets_pt_raw = []
        jets_pt_jer = []
        jets_pt_nom = []

        jets_mass_raw = []
        jets_mass_nom = []
        
        jets_corr_JEC = []
        jets_corr_JER = []
        
        jets_pt_jerUp   = []
        jets_pt_jerDown = []
        jets_pt_jesUp   = {}
        jets_pt_jesDown = {}
        
        jets_mass_jerUp   = []
        jets_mass_jerDown = []
        jets_mass_jesUp   = {}
        jets_mass_jesDown = {}

        for jesUncertainty in self.jesUncertainties:
            jets_pt_jesUp[jesUncertainty]   = []
            jets_pt_jesDown[jesUncertainty] = []
            jets_mass_jesUp[jesUncertainty]   = []
            jets_mass_jesDown[jesUncertainty] = []
        
        met     = Object(event, self.metBranchName)
        rawmet  = Object(event, "RawMET")
        defmet  = Object(event, "MET")

        ( t1met_px,       t1met_py       ) = ( met.pt*math.cos(met.phi), met.pt*math.sin(met.phi) )
        ( def_met_px,     def_met_py     ) = ( defmet.pt*math.cos(defmet.phi),   defmet.pt*math.sin(defmet.phi) )
        ( met_px,         met_py         ) = ( rawmet.pt*math.cos(rawmet.phi), rawmet.pt*math.sin(rawmet.phi) )
        ( met_px_nom,     met_py_nom     ) = ( met_px, met_py )
        ( met_px_jer,     met_py_jer     ) = ( met_px, met_py )
        ( met_px_jerUp,   met_py_jerUp   ) = ( met_px, met_py )
        ( met_px_jerDown, met_py_jerDown ) = ( met_px, met_py )
        ( met_px_jesUp,   met_py_jesUp   ) = ( {}, {} )
        ( met_px_jesDown, met_py_jesDown ) = ( {}, {} )

        for jesUncertainty in self.jesUncertainties:
            met_px_jesUp[jesUncertainty]   = met_px
            met_py_jesUp[jesUncertainty]   = met_py
            met_px_jesDown[jesUncertainty] = met_px
            met_py_jesDown[jesUncertainty] = met_py

        # variables needed for re-applying JECs to 2017 v2 MET
        delta_x_T1Jet, delta_y_T1Jet = 0, 0
        delta_x_rawJet, delta_y_rawJet = 0, 0
        
        rho = getattr(event, self.rhoBranchName)
        
        # match reconstructed jets to generator level ones
        # (needed to evaluate JER scale factors and uncertainties)
        if not self.isData:
          pairs = matchObjectCollection(jets, genJets)
          lowPtPairs = matchObjectCollection(lowPtJets, genJets)
          pairs.update(lowPtPairs)

        for iJet, jet in enumerate(itertools.chain(jets, lowPtJets)):
            #jet pt and mass corrections
            jet_pt = jet.pt
            jet_mass = jet.mass
            jet_pt_orig = jet_pt
            rawFactor = jet.rawFactor

            #redo JECs if desired
            if hasattr(jet, "rawFactor"):
                jet_rawpt = jet_pt * (1 - jet.rawFactor)
                jet_rawmass = jet_mass * (1 - jet.rawFactor)
            else:
                jet_rawpt = -1.0 * jet_pt #If factor not present factor will be saved as -1
                jet_rawmass = -1.0 * jet_mass #If factor not present factor will be saved as -1

            (jet_pt, jet_mass)    = self.jetReCalibrator.correct(jet,rho)
            (jet_pt_l1, jet_mass_l1) = self.jetReCalibratorL1.correct(jet,rho)
            jet.pt = jet_pt
            jet.mass = jet_mass

            # Get the JEC factors
            jec   = jet_pt/jet_rawpt
            jecL1 = jet_pt_l1/jet_rawpt
            if self.jetReCalibratorProd:
              jecProd = self.jetReCalibratorProd.correct(jet,rho)[0]/jet_rawpt
              jecL1Prod = self.jetReCalibratorProdL1.correct(jet,rho)[0]/jet_rawpt

            if not self.isData:
              genJet = pairs[jet]
            
            # get the jet for type-1 MET
            newjet = ROOT.TLorentzVector()
            if self.isV5NanoAOD:
                newjet.SetPtEtaPhiM(jet_pt_orig*(1-jet.rawFactor)*(1-jet.muonSubtrFactor), jet.eta, jet.phi, jet.mass )
                muon_pt = jet_pt_orig*(1-jet.rawFactor)*jet.muonSubtrFactor
            else:
                newjet.SetPtEtaPhiM(jet_pt_orig*(1-jet.rawFactor), jet.eta, jet.phi, jet.mass )
                muon_pt = 0
                if hasattr(jet, 'muonIdx1'):
                  if jet.muonIdx1>-1:
                      if muons[jet.muonIdx1].isGlobal:
                        newjet = newjet - muons[jet.muonIdx1].p4()
                        muon_pt += muons[jet.muonIdx1].pt
                  if jet.muonIdx2>-1:
                      if muons[jet.muonIdx2].isGlobal:
                        newjet = newjet - muons[jet.muonIdx2].p4()
                        muon_pt += muons[jet.muonIdx2].pt

            # set the jet pt to the muon subtracted raw pt
            jet.pt = newjet.Pt()
            jet.rawFactor = 0
            # get the proper jet pts for type-1 MET. only correct the non-mu fraction of the jet. if the corrected pt>15, use the corrected jet, otherwise use raw
            jet_pt_noMuL1L2L3 = jet.pt*jec    if jet.pt*jec > self.unclEnThreshold else jet.pt
            jet_pt_noMuL1     = jet.pt*jecL1  if jet.pt*jec > self.unclEnThreshold else jet.pt

            # this step is only needed for v2 MET in 2017 when different JECs are applied compared to the nanoAOD production
            if self.jetReCalibratorProd:
              jet_pt_noMuProdL1L2L3   = jet.pt*jecProd    if jet.pt*jecProd > self.unclEnThreshold else jet.pt
              jet_pt_noMuProdL1       = jet.pt*jecL1Prod  if jet.pt*jecProd > self.unclEnThreshold else jet.pt
            else:
              jet_pt_noMuProdL1L2L3 = jet_pt_noMuL1L2L3
              jet_pt_noMuProdL1     = jet_pt_noMuL1

            ## setting jet back to central values
            jet.pt          = jet_pt
            jet.rawFactor   = rawFactor

            # evaluate JER scale factors and uncertainties
            # (cf. https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution and https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyResolution )
            if not self.isData:
              ( jet_pt_jerNomVal, jet_pt_jerUpVal, jet_pt_jerDownVal ) = self.jetSmearer.getSmearValsPt(jet, genJet, rho)
            else:
              # if you want to do something with JER in data, please add it here.
              ( jet_pt_jerNomVal, jet_pt_jerUpVal, jet_pt_jerDownVal ) = (1,1,1)
            
            # these are the important jet pt values
            #jet_pt_nom      = jet_pt if jet_pt > 0 else 0
            jet_pt_nom      = jet_pt * jet_pt_jerNomVal if self.applySmearing else jet_pt
            jet_pt_L1L2L3   = jet_pt_noMuL1L2L3 + muon_pt
            jet_pt_L1       = jet_pt_noMuL1     + muon_pt

            # not nice, but needed for METv2 in 2017
            jet_pt_prodL1L2L3   = jet_pt_noMuProdL1L2L3 + muon_pt
            jet_pt_prodL1       = jet_pt_noMuProdL1     + muon_pt

            if self.metBranchName == 'METFixEE2017':
                # get the delta for removing L1L2L3-L1 corrected jets (corrected with GT from nanoAOD production!!) in the EE region from the default MET branch.
                if jet_pt_prodL1L2L3 > self.unclEnThreshold and 2.65<abs(jet.eta)<3.14 and jet_rawpt < 50:
                    delta_x_T1Jet  += (jet_pt_prodL1L2L3-jet_pt_prodL1) * math.cos(jet.phi) + jet_rawpt * math.cos(jet.phi)
                    delta_y_T1Jet  += (jet_pt_prodL1L2L3-jet_pt_prodL1) * math.sin(jet.phi) + jet_rawpt * math.sin(jet.phi)

                # get the delta for removing raw jets in the EE region from the raw MET
                if jet_pt_prodL1L2L3 > self.unclEnThreshold and 2.65<abs(jet.eta)<3.14 and jet_rawpt < 50:
                    delta_x_rawJet += jet_rawpt * math.cos(jet.phi)
                    delta_y_rawJet += jet_rawpt * math.sin(jet.phi)



            # don't store the low pt jets in the Jet_pt_nom branch
            if iJet < nJet:
                jets_pt_raw     .append(jet_rawpt)
                jets_pt_nom     .append(jet_pt_nom)
                jets_mass_raw   .append(jet_rawmass)
                jets_corr_JEC   .append(jet_pt/jet_rawpt)
                jets_corr_JER   .append(jet_pt_jerNomVal)  # can be used to undo JER

                # no need to do this for low pt jets
                jet_mass_nom           = jet_pt_jerNomVal*jet_mass if self.applySmearing else jet_mass
                if jet_mass_nom < 0.0:
                    jet_mass_nom *= -1.0
                jets_mass_nom    .append(jet_mass_nom)

            if not self.isData:
              jet_pt_jerUp         = jet_pt_jerUpVal  *jet_pt
              jet_pt_jerDown       = jet_pt_jerDownVal*jet_pt

              # evaluate JES uncertainties
              jet_pt_jesUp     = {}
              jet_pt_jesDown   = {}
              jet_pt_jesUpT1   = {}
              jet_pt_jesDownT1 = {}

              jet_mass_jesUp   = {}
              jet_mass_jesDown = {}

              # don't store the low pt jets in the Jet_pt_nom branch
              if iJet < nJet:
                  jets_pt_jerUp    .append(jet_pt_jerUpVal*jet_pt)
                  jets_pt_jerDown  .append(jet_pt_jerDownVal*jet_pt)
                  jets_mass_jerUp  .append(jet_pt_jerUpVal   *jet_mass)
                  jets_mass_jerDown.append(jet_pt_jerDownVal *jet_mass)
              
              for jesUncertainty in self.jesUncertainties:
                  # (cf. https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyCorrections#JetCorUncertainties )
                  self.jesUncertainty[jesUncertainty].setJetPt(jet_pt_nom)
                  self.jesUncertainty[jesUncertainty].setJetEta(jet.eta)
                  delta = self.jesUncertainty[jesUncertainty].getUncertainty(True)
                  jet_pt_jesUp[jesUncertainty]   = jet_pt_nom*(1. + delta)
                  jet_pt_jesDown[jesUncertainty] = jet_pt_nom*(1. - delta)
                  if iJet < nJet:
                    jets_pt_jesUp[jesUncertainty].append(jet_pt_jesUp[jesUncertainty])
                    jets_pt_jesDown[jesUncertainty].append(jet_pt_jesDown[jesUncertainty])
                    jet_mass_jesUp   [jesUncertainty] = jet_mass_nom*(1. + delta)
                    jet_mass_jesDown [jesUncertainty] = jet_mass_nom*(1. - delta)
                    jets_mass_jesUp  [jesUncertainty].append(jet_mass_jesUp[jesUncertainty])
                    jets_mass_jesDown[jesUncertainty].append(jet_mass_jesDown[jesUncertainty])
                  
                  # redo JES variations for T1 MET
                  self.jesUncertainty[jesUncertainty].setJetPt(jet_pt_L1L2L3)
                  self.jesUncertainty[jesUncertainty].setJetEta(jet.eta)
                  delta = self.jesUncertainty[jesUncertainty].getUncertainty(True)
                  jet_pt_jesUpT1[jesUncertainty]   = jet_pt_L1L2L3*(1. + delta)
                  jet_pt_jesDownT1[jesUncertainty] = jet_pt_L1L2L3*(1. - delta)


            # progate JER and JES corrections and uncertainties to MET
            if jet_pt_L1L2L3 > self.unclEnThreshold and (jet.neEmEF+jet.chEmEF) < 0.9:
                if not ( self.metBranchName == 'METFixEE2017' and 2.65<abs(jet.eta)<3.14 and jet.pt*(1-jet.rawFactor)<50 ): # do not re-correct for jets that aren't included in METv2 recipe
                    jet_cosPhi = math.cos(jet.phi)
                    jet_sinPhi = math.sin(jet.phi)
                    met_px_nom     = met_px_nom     - (jet_pt_L1L2L3  - jet_pt_L1)*jet_cosPhi 
                    met_py_nom     = met_py_nom     - (jet_pt_L1L2L3  - jet_pt_L1)*jet_sinPhi 
                    if not self.isData:
                      met_px_jer     = met_px_jer     - (jet_pt_L1L2L3*jet_pt_jerNomVal   - jet_pt_L1)*jet_cosPhi 
                      met_py_jer     = met_py_jer     - (jet_pt_L1L2L3*jet_pt_jerNomVal   - jet_pt_L1)*jet_sinPhi 
                      met_px_jerUp   = met_px_jerUp   - (jet_pt_L1L2L3*jet_pt_jerUpVal    - jet_pt_L1)*jet_cosPhi 
                      met_py_jerUp   = met_py_jerUp   - (jet_pt_L1L2L3*jet_pt_jerUpVal    - jet_pt_L1)*jet_sinPhi 
                      met_px_jerDown = met_px_jerDown - (jet_pt_L1L2L3*jet_pt_jerDownVal  - jet_pt_L1)*jet_cosPhi 
                      met_py_jerDown = met_py_jerDown - (jet_pt_L1L2L3*jet_pt_jerDownVal  - jet_pt_L1)*jet_sinPhi 
                      for jesUncertainty in self.jesUncertainties:
                          met_px_jesUp[jesUncertainty]   = met_px_jesUp[jesUncertainty]   - (jet_pt_jesUpT1[jesUncertainty]   - jet_pt_L1)*jet_cosPhi
                          met_py_jesUp[jesUncertainty]   = met_py_jesUp[jesUncertainty]   - (jet_pt_jesUpT1[jesUncertainty]   - jet_pt_L1)*jet_sinPhi
                          met_px_jesDown[jesUncertainty] = met_px_jesDown[jesUncertainty] - (jet_pt_jesDownT1[jesUncertainty] - jet_pt_L1)*jet_cosPhi
                          met_py_jesDown[jesUncertainty] = met_py_jesDown[jesUncertainty] - (jet_pt_jesDownT1[jesUncertainty] - jet_pt_L1)*jet_sinPhi


        # propagate "unclustered energy" uncertainty to MET
        if self.metBranchName == 'METFixEE2017':
            # Remove the L1L2L3-L1 corrected jets in the EE region from the default MET branch
            def_met_px += delta_x_T1Jet
            def_met_py += delta_y_T1Jet

            # get unclustered energy part that is removed in the v2 recipe
            met_unclEE_x = def_met_px - t1met_px
            met_unclEE_y = def_met_py - t1met_py

            # finalize the v2 recipe for the rawMET by removing the unclustered part in the EE region
            met_px_nom += delta_x_rawJet - met_unclEE_x 
            met_py_nom += delta_y_rawJet - met_unclEE_y
            
            if not self.isData:
              met_px_jerUp += delta_x_rawJet - met_unclEE_x
              met_py_jerUp += delta_y_rawJet - met_unclEE_y
              met_px_jerDown += delta_x_rawJet - met_unclEE_x
              met_py_jerDown += delta_y_rawJet - met_unclEE_y
              for jesUncertainty in self.jesUncertainties:
                  met_px_jesUp[jesUncertainty] += delta_x_rawJet - met_unclEE_x
                  met_py_jesUp[jesUncertainty] += delta_y_rawJet - met_unclEE_y
                  met_px_jesDown[jesUncertainty] += delta_x_rawJet - met_unclEE_x
                  met_py_jesDown[jesUncertainty] += delta_y_rawJet - met_unclEE_y


        if not self.isData:
          ( met_px_unclEnUp,   met_py_unclEnUp   ) = ( met_px_nom, met_py_nom )
          ( met_px_unclEnDown, met_py_unclEnDown ) = ( met_px_nom, met_py_nom )
          met_deltaPx_unclEn = getattr(event, self.metBranchName + "_MetUnclustEnUpDeltaX")
          met_deltaPy_unclEn = getattr(event, self.metBranchName + "_MetUnclustEnUpDeltaY")
          met_px_unclEnUp    = met_px_unclEnUp   + met_deltaPx_unclEn
          met_py_unclEnUp    = met_py_unclEnUp   + met_deltaPy_unclEn
          met_px_unclEnDown  = met_px_unclEnDown - met_deltaPx_unclEn
          met_py_unclEnDown  = met_py_unclEnDown - met_deltaPy_unclEn


        self.out.fillBranch("%s_pt_raw" % self.jetBranchName, jets_pt_raw)
        self.out.fillBranch("%s_pt_nom" % self.jetBranchName, jets_pt_nom)
        self.out.fillBranch("%s_corr_JEC" % self.jetBranchName, jets_corr_JEC)
        self.out.fillBranch("%s_corr_JER" % self.jetBranchName, jets_corr_JER)
        if not self.isData:
          self.out.fillBranch("%s_pt_jerUp" % self.jetBranchName, jets_pt_jerUp)
          self.out.fillBranch("%s_pt_jerDown" % self.jetBranchName, jets_pt_jerDown)
            
        self.out.fillBranch("%s_pt_nom" % self.metBranchName, math.sqrt(met_px_nom**2 + met_py_nom**2))
        self.out.fillBranch("%s_phi_nom" % self.metBranchName, math.atan2(met_py_nom, met_px_nom))        

        self.out.fillBranch("%s_mass_raw" % self.jetBranchName, jets_mass_raw)
        self.out.fillBranch("%s_mass_nom" % self.jetBranchName, jets_mass_nom)

        if not self.isData:
            self.out.fillBranch("%s_mass_jerUp" % self.jetBranchName, jets_mass_jerUp)
            self.out.fillBranch("%s_mass_jerDown" % self.jetBranchName, jets_mass_jerDown)


        if not self.isData:
          self.out.fillBranch("%s_pt_jer" % self.metBranchName, math.sqrt(met_px_jer**2 + met_py_jer**2))
          self.out.fillBranch("%s_phi_jer" % self.metBranchName, math.atan2(met_py_jer, met_px_jer))        
          self.out.fillBranch("%s_pt_jerUp" % self.metBranchName, math.sqrt(met_px_jerUp**2 + met_py_jerUp**2))
          self.out.fillBranch("%s_phi_jerUp" % self.metBranchName, math.atan2(met_py_jerUp, met_px_jerUp))        
          self.out.fillBranch("%s_pt_jerDown" % self.metBranchName, math.sqrt(met_px_jerDown**2 + met_py_jerDown**2))
          self.out.fillBranch("%s_phi_jerDown" % self.metBranchName, math.atan2(met_py_jerDown, met_px_jerDown))
              
          for jesUncertainty in self.jesUncertainties:
              self.out.fillBranch("%s_pt_jes%sUp" % (self.jetBranchName, jesUncertainty), jets_pt_jesUp[jesUncertainty])
              self.out.fillBranch("%s_pt_jes%sDown" % (self.jetBranchName, jesUncertainty), jets_pt_jesDown[jesUncertainty])
              
              self.out.fillBranch("%s_pt_jes%sUp" % (self.metBranchName, jesUncertainty), math.sqrt(met_px_jesUp[jesUncertainty]**2 + met_py_jesUp[jesUncertainty]**2))
              self.out.fillBranch("%s_phi_jes%sUp" % (self.metBranchName, jesUncertainty), math.atan2(met_py_jesUp[jesUncertainty], met_px_jesUp[jesUncertainty]))
              self.out.fillBranch("%s_pt_jes%sDown" % (self.metBranchName, jesUncertainty), math.sqrt(met_px_jesDown[jesUncertainty]**2 + met_py_jesDown[jesUncertainty]**2))
              self.out.fillBranch("%s_phi_jes%sDown" % (self.metBranchName, jesUncertainty), math.atan2(met_py_jesDown[jesUncertainty], met_px_jesDown[jesUncertainty]))
              
              self.out.fillBranch("%s_mass_jes%sUp" % (self.jetBranchName, jesUncertainty), jets_mass_jesUp[jesUncertainty])
              self.out.fillBranch("%s_mass_jes%sDown" % (self.jetBranchName, jesUncertainty), jets_mass_jesDown[jesUncertainty])

          self.out.fillBranch("%s_pt_unclustEnUp" % self.metBranchName, math.sqrt(met_px_unclEnUp**2 + met_py_unclEnUp**2))
          self.out.fillBranch("%s_phi_unclustEnUp" % self.metBranchName, math.atan2(met_py_unclEnUp, met_px_unclEnUp))
          self.out.fillBranch("%s_pt_unclustEnDown" % self.metBranchName, math.sqrt(met_px_unclEnDown**2 + met_py_unclEnDown**2))
          self.out.fillBranch("%s_phi_unclustEnDown" % self.metBranchName, math.atan2(met_py_unclEnDown, met_px_unclEnDown))

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
jetmetUncertainties2016 = lambda : jetmetUncertaintiesProducer("2016", "Summer16_07Aug2017_V11_MC", [ "Total" ])
jetmetUncertainties2016All = lambda : jetmetUncertaintiesProducer("2016", "Summer16_07Aug2017_V11_MC", [ "All" ])

jetmetUncertainties2017 = lambda : jetmetUncertaintiesProducer("2017", "Fall17_17Nov2017_V32_MC", [ "Total" ])
jetmetUncertainties2017METv2 = lambda : jetmetUncertaintiesProducer("2017", "Fall17_17Nov2017_V32_MC", metBranchName='METFixEE2017')
jetmetUncertainties2017All = lambda : jetmetUncertaintiesProducer("2017", "Fall17_17Nov2017_V32_MC", [ "All" ])

jetmetUncertainties2018 = lambda : jetmetUncertaintiesProducer("2018", "Autumn18_V8_MC", [ "Total" ])
jetmetUncertainties2018Data = lambda : jetmetUncertaintiesProducer("2018", "Autumn18_RunB_V8_DATA", archive="Autumn18_V8_DATA", isData=True)
jetmetUncertainties2018All = lambda : jetmetUncertaintiesProducer("2018", "Autumn18_V8_MC", [ "All" ])

jetmetUncertainties2016AK4Puppi = lambda : jetmetUncertaintiesProducer("2016", "Summer16_07Aug2017_V11_MC", [ "Total" ], jetType="AK4PFPuppi")
jetmetUncertainties2016AK4PuppiAll = lambda : jetmetUncertaintiesProducer("2016", "Summer16_07Aug2017_V11_MC",  [ "All" ], jetType="AK4PFPuppi")

jetmetUncertainties2017AK4Puppi = lambda : jetmetUncertaintiesProducer("2017", "Fall17_17Nov2017_V32_MC", [ "Total" ], jetType="AK4PFPuppi")
jetmetUncertainties2017AK4PuppiAll = lambda : jetmetUncertaintiesProducer("2017", "Fall17_17Nov2017_V32_MC",  [ "All" ], jetType="AK4PFPuppi")

jetmetUncertainties2018AK4Puppi = lambda : jetmetUncertaintiesProducer("2018", "Autumn18_V8_MC", [ "Total" ], jetType="AK4PFPuppi")
jetmetUncertainties2018AK4PuppiAll = lambda : jetmetUncertaintiesProducer("2018", "Autumn18_V8_MC",  [ "All" ], jetType="AK4PFPuppi")

