import ROOT
import os
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.JetReCalibrator import JetReCalibrator

class addSUSYvars(Module):
    def GetFileNameJEC(self):
      if not self.isData: return "Fall17_17Nov2017_V6_MC"
      else: return 'Fall17_17Nov2017' + self.era + '_V6_DATA'

    def jetLepAwareJEC(self,lep,jet,L1corr):
      p4l = lep.p4(); l = ROOT.TLorentzVector(p4l.Px(),p4l.Py(),p4l.Pz(),p4l.E())
      if not hasattr(jet,'rawFactor'): return l 
      rf = jet.rawFactor
      p4j = jet.p4(); j = ROOT.TLorentzVector(p4j.Px(),p4j.Py(),p4j.Pz(),p4j.E())
      if ((j*jet.rawFactor-l).Rho()<1e-4): return l 
      j = (j*rf - l*(1.0/L1corr)) * (1/rf) + l
      return j

    def ptRelv2(self,lep,jet,L1corr): # use only if jetAna.calculateSeparateCorrections==True
      m = self.jetLepAwareJEC(lep,jet,L1corr)
      p4l = lep.p4(); l = ROOT.TLorentzVector(p4l.Px(),p4l.Py(),p4l.Pz(),p4l.E())
      if ((m-l).Rho()<1e-4): return 0 # lep.jet==lep (no match) or jet containing only the lepton
      return l.Perp((m-l).Vect())

    def __init__(self, isData, era=''):
      self.isData = isData
      self.era = era
 
      fileNameJEC = self.GetFileNameJEC()
      jetType = "AK4PFchs"
      jesInputFilePath = os.environ['CMSSW_BASE'] + "/src/PhysicsTools/NanoAODTools/data/jme/"
      self.jetReCalibrator = JetReCalibrator(fileNameJEC, jetType , True, jesInputFilePath, upToLevel=1)

    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("Electron_ptRel",  "F", lenVar = "nElectron");
        self.out.branch("Electron_ptRatio",  "F", lenVar = "nElectron");
        self.out.branch("Electron_SUSYmva",  "F", lenVar = "nElectron");
        self.out.branch("Muon_ptRel",  "F", lenVar = 'nMuon');
        self.out.branch("Muon_ptRatio",  "F", lenVar = 'nMuon');
        self.out.branch("Muon_SUSYmva",  "F", lenVar = 'nMuon');
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        Electron_ptRel = []; Electron_ptRatio = []; Electron_SUSYmva = []; 
        Muon_ptRel = [];     Muon_ptRatio = [];     Muon_SUSYmva = [];
        ptRel = -999; ptRatio = -999; mva = -999;
        elecs = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets  = Collection(event, "Jet")
        rho = getattr(event, "fixedGridRhoFastjetAll")
        eventSum = ROOT.TLorentzVector()
        for lep in muons :
            pt = lep.pt
            eta = lep.eta
            miniIsoCharged = lep.miniPFRelIso_chg
            miniIsoNeutrals= lep.miniPFRelIso_all - lep.miniPFRelIso_chg
            dB = lep.dxy # ???? 
            dz = lep.dz
            segmentCompatibility = lep.segmentComp
            combRelIsoPF04dBeta = lep.pfRelIso04_all
            #miniIsoPhotons = 
    #theTree->SetBranchAddress("fixedGridRhoFastjetAll", &fixedGridRhoFastjetAll);
    #theTree->SetBranchAddress("Loose", &Loose);
    #theTree->SetBranchAddress("Medium2016", &Medium2016);
    #theTree->SetBranchAddress("tkPtError", &tkPtError);
    #theTree->SetBranchAddress("JetNDauCharged",&JetNDauCharged);

sum(
(deltaR(x.eta(),x.phi(),lepton.jet.eta(),lepton.jet.phi())<=0.4 and x.charge()!=0 and x.fromPV()>1 and x.hasTrackDetails() and qualityTrk(x.pseudoTrack(),lepton.associatedVertex))
 for x in lepton.jet.daughterPtrVector()
) 
if hasattr(lepton,'jet') and lepton.jet != lepton else 0, 
help="n charged daughters (with selection for ttH lepMVA) of nearest jet"),

            if lep.jetIdx < 0: 
              corr    = 1
              ptRel   = -1
              ptRatio = -1
            else: 
              jet     = jets[lep.jetIdx]
              corr    = self.jetReCalibrator.getCorrection(jet, rho)
              ptRel   = self.ptRelv2(lep, jet, corr)
              ptRatio = lep.pt/self.jetLepAwareJEC(lep, jet, corr).Pt()
              csv     = jet.btagCSVV2
            Muon_ptRel.append(ptRel)
            Muon_ptRatio.append(ptRatio)
            Muon_SUSYmva.append(mva)

        for lep in elecs:
           eventSum += lep.p4()

        self.out.fillBranch("Electron_ptRel",  Electron_ptRel); # Must be a list with len = nElectron
        self.out.fillBranch("Electron_ptRatio",  Electron_ptRatio);
        self.out.fillBranch("Electron_SUSYmva",  Electron_SUSYmva);
        self.out.fillBranch("Muon_ptRel",  Muon_ptRel);
        self.out.fillBranch("Muon_ptRatio",  Muon_ptRatio);
        self.out.fillBranch("Muon_SUSYmva",  Muon_SUSYmva);
        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

addSUSYvarsMC   = lambda : addSUSYvars(False) 
addSUSYvarsDataB = lambda : addSUSYvars(True,'B') 
addSUSYvarsDataC = lambda : addSUSYvars(True,'C') 
addSUSYvarsDataD = lambda : addSUSYvars(True,'D') 
addSUSYvarsDataE = lambda : addSUSYvars(True,'E') 
addSUSYvarsDataF = lambda : addSUSYvars(True,'F') 
 

################################################################################
################################################################################
################################################################################

'''
    NTupleVariable("jetPtRatiov2", lambda lepton: lepton.pt()/jetLepAwareJEC(lepton).Pt() if hasattr(lepton,'jet') else -1, help="pt(lepton)/[rawpt(jet-PU-lep)*L2L3Res+pt(lepton)]"),

NTupleVariable("jetPtRelv2", lambda lepton : ptRelv2(lepton) if hasattr(lepton,'jet') else -1, help="pt of the lepton transverse to the jet axis (subtracting the lepton) - v2"),

################################################################################

'''
