import ROOT
import math, os,re, tarfile, tempfile
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import matchObjectCollection, matchObjectCollectionMultiple
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.JetReCalibrator import JetReCalibrator

class jetRecalib(Module):
    def __init__(self,  globalTag, archive, jetType = "AK4PFchs"):

        if "AK4" in jetType : 
            self.jetBranchName = "Jet"
        elif "AK8" in jetType :
            self.jetBranchName = "FatJet"
            self.subJetBranchName = "SubJet"
        else:
            raise ValueError("ERROR: Invalid jet type = '%s'!" % jetType)
        self.rhoBranchName = "fixedGridRhoFastjetAll"
        self.lenVar = "n" + self.jetBranchName        

        self.jesInputArchivePath = os.environ['CMSSW_BASE'] + "/src/PhysicsTools/NanoAODTools/data/jme/"
        # Text files are now tarred so must extract first into temporary directory (gets deleted during python memory management at script exit)
        self.jesArchive = tarfile.open(self.jesInputArchivePath+archive+".tgz", "r:gz")
        self.jesInputFilePath = tempfile.mkdtemp()
        self.jesArchive.extractall(self.jesInputFilePath)

        self.jetReCalibrator = JetReCalibrator(globalTag, jetType , True, self.jesInputFilePath, calculateSeparateCorrections = False, calculateType1METCorrection  = False)
	
        # load libraries for accessing JES scale factors and uncertainties from txt files
        for library in [ "libCondFormatsJetMETObjects", "libPhysicsToolsNanoAODTools" ]:
            if library not in ROOT.gSystem.GetLibraries():
                print("Load Library '%s'" % library.replace("lib", ""))
                ROOT.gSystem.Load(library)

    def beginJob(self):
	pass

    def endJob(self):
	pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("%s_pt_raw" % self.jetBranchName, "F", lenVar=self.lenVar)
        self.out.branch("%s_pt_nom" % self.jetBranchName, "F", lenVar=self.lenVar)
        self.out.branch("%s_mass_raw" % self.jetBranchName, "F", lenVar=self.lenVar)
        self.out.branch("%s_mass_nom" % self.jetBranchName, "F", lenVar=self.lenVar)
        self.out.branch("MET_pt_nom" , "F")
        self.out.branch("MET_phi_nom", "F")
            
                        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = Collection(event, self.jetBranchName )
        met = Object(event, "MET") 

        jets_pt_raw = []
        jets_pt_nom = []
        jets_mass_raw = []
        jets_mass_nom = []
        ( met_px,         met_py         ) = ( met.pt*math.cos(met.phi), met.pt*math.sin(met.phi) )
        ( met_px_nom, met_py_nom ) = ( met_px, met_py )
        met_px_nom = met_px
        met_py_nom = met_py
                
        rho = getattr(event, self.rhoBranchName)
        
        for jet in jets:
            jet_pt_raw = jet.pt*(1.-jet.rawFactor) #save raw jet pt
            jets_pt_raw.append(jet_pt_raw)

            jet_mass_raw = jet.mass*(1.-jet.rawFactor) #save raw jet mass
            jets_mass_raw.append(jet_mass_raw)

	    jet_pt=jet.pt
            (jet_pt, jet_mass) = self.jetReCalibrator.correct(jet,rho)
            jet_pt_nom           = jet_pt # don't smear resolution in data
            if jet_pt_nom < 0.0:
                jet_pt_nom *= -1.0
            jets_pt_nom    .append(jet_pt_nom)

            jet_mass_nom         = jet_mass
            if jet_mass_nom < 0.0:
                jet_mass_nom *= -1.0
            jets_mass_nom    .append(jet_mass_nom)

            if jet_pt_nom > 15.:
                jet_cosPhi = math.cos(jet.phi)
                jet_sinPhi = math.sin(jet.phi)
                met_px_nom = met_px_nom - (jet_pt_nom - jet.pt)*jet_cosPhi
                met_py_nom = met_py_nom - (jet_pt_nom - jet.pt)*jet_sinPhi
        self.out.fillBranch("%s_pt_raw" % self.jetBranchName, jets_pt_raw)
        self.out.fillBranch("%s_pt_nom" % self.jetBranchName, jets_pt_nom)
        self.out.fillBranch("%s_mass_raw" % self.jetBranchName, jets_mass_raw)
        self.out.fillBranch("%s_mass_nom" % self.jetBranchName, jets_mass_nom)
        self.out.fillBranch("MET_pt_nom", math.sqrt(met_px_nom**2 + met_py_nom**2))
        self.out.fillBranch("MET_phi_nom", math.atan2(met_py_nom, met_px_nom))        

        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
jetRecalib2016BCD = lambda : jetRecalib("Summer16_07Aug2017BCD_V11_DATA","Summer16_07Aug2017_V11_DATA")
jetRecalib2016EF = lambda : jetRecalib("Summer16_07Aug2017EF_V11_DATA","Summer16_07Aug2017_V11_DATA")
jetRecalib2016GH = lambda : jetRecalib("Summer16_07Aug2017GH_V11_DATA","Summer16_07Aug2017_V11_DATA")

jetRecalib2016BCDAK8Puppi = lambda : jetRecalib("Summer16_07Aug2017BCD_V11_DATA","Summer16_07Aug2017_V11_DATA", jetType="AK8PFPuppi")
jetRecalib2016EFAK8Puppi = lambda : jetRecalib("Summer16_07Aug2017EF_V11_DATA","Summer16_07Aug2017_V11_DATA", jetType="AK8PFPuppi")
jetRecalib2016GHAK8Puppi = lambda : jetRecalib("Summer16_07Aug2017GH_V11_DATA","Summer16_07Aug2017_V11_DATA",jetType="AK8PFPuppi")

jetRecalib2017B = lambda : jetRecalib("Fall17_17Nov2017B_V32_DATA","Fall17_17Nov2017_V32_DATA")
jetRecalib2017C = lambda : jetRecalib("Fall17_17Nov2017C_V32_DATA","Fall17_17Nov2017_V32_DATA")
jetRecalib2017DE = lambda : jetRecalib("Fall17_17Nov2017DE_V32_DATA","Fall17_17Nov2017_V32_DATA")
jetRecalib2017F = lambda : jetRecalib("Fall17_17Nov2017F_V32_DATA","Fall17_17Nov2017_V32_DATA")

jetRecalib2017BAK8Puppi = lambda : jetRecalib("Fall17_17Nov2017B_V32_DATA","Fall17_17Nov2017_V32_DATA",jetType="AK8PFPuppi")
jetRecalib2017CAK8Puppi = lambda : jetRecalib("Fall17_17Nov2017C_V32_DATA","Fall17_17Nov2017_V32_DATA",jetType="AK8PFPuppi")
jetRecalib2017DEAK8Puppi = lambda : jetRecalib("Fall17_17Nov2017DE_V32_DATA","Fall17_17Nov2017_V32_DATA", jetType="AK8PFPuppi")
jetRecalib2017FAK8Puppi = lambda : jetRecalib("Fall17_17Nov2017F_V32_DATA","Fall17_17Nov2017_V32_DATA",jetType="AK8PFPuppi")

jetRecalib2018A = lambda : jetRecalib("Autumn18_RunA_V8_DATA","Autumn18_V8_DATA")
jetRecalib2018B = lambda : jetRecalib("Autumn18_RunB_V8_DATA","Autumn18_V8_DATA")
jetRecalib2018C = lambda : jetRecalib("Autumn18_RunC_V8_DATA","Autumn18_V8_DATA")
jetRecalib2018D = lambda : jetRecalib("Autumn18_RunD_V8_DATA","Autumn18_V8_DATA")

jetRecalib2018AAK8Puppi = lambda : jetRecalib("Autumn18_RunA_V8_DATA","Autumn18_V8_DATA",jetType="AK8PFPuppi")
jetRecalib2018BAK8Puppi = lambda : jetRecalib("Autumn18_RunB_V8_DATA","Autumn18_V8_DATA",jetType="AK8PFPuppi")
jetRecalib2018CAK8Puppi = lambda : jetRecalib("Autumn18_RunC_V8_DATA","Autumn18_V8_DATA",jetType="AK8PFPuppi")
jetRecalib2018DAK8Puppi = lambda : jetRecalib("Autumn18_RunD_V8_DATA","Autumn18_V8_DATA",jetType="AK8PFPuppi")
