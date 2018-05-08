import ROOT
import os, types
from math import *
from PhysicsTools.HeppyCore.utils.deltar import *

class JetReCalibrator:
    def __init__(self,globalTag,jetFlavour,doResidualJECs,jecPath,upToLevel=3,
                 calculateSeparateCorrections=False,
                 calculateType1METCorrection=False, type1METParams={'jetPtThreshold':15., 'skipEMfractionThreshold':0.9, 'skipMuons':True} ):
        """Create a corrector object that reads the payloads from the text dumps of a global tag under
            CMGTools/RootTools/data/jec  (see the getJec.py there to make the dumps).
           It will apply the L1,L2,L3 and possibly the residual corrections to the jets.
           If configured to do so, it will also compute the type1 MET corrections."""
        self.globalTag = globalTag
        self.jetFlavour = jetFlavour
        self.doResidualJECs = doResidualJECs
        self.jecPath = jecPath
        self.upToLevel = upToLevel
        self.calculateType1METCorr = calculateType1METCorrection
        self.type1METParams  = type1METParams
        # Make base corrections
        path = os.path.expandvars(jecPath) #"%s/src/CMGTools/RootTools/data/jec" % os.environ['CMSSW_BASE'];
        self.L1JetPar  = ROOT.JetCorrectorParameters("%s/%s_L1FastJet_%s.txt" % (path,globalTag,jetFlavour),"");
        self.L2JetPar  = ROOT.JetCorrectorParameters("%s/%s_L2Relative_%s.txt" % (path,globalTag,jetFlavour),"");
        self.L3JetPar  = ROOT.JetCorrectorParameters("%s/%s_L3Absolute_%s.txt" % (path,globalTag,jetFlavour),"");
        self.vPar = ROOT.vector(ROOT.JetCorrectorParameters)()
        self.vPar.push_back(self.L1JetPar);
        if upToLevel >= 2: self.vPar.push_back(self.L2JetPar);
        if upToLevel >= 3: self.vPar.push_back(self.L3JetPar);
        # Add residuals if needed
        if doResidualJECs : 
            self.ResJetPar = ROOT.JetCorrectorParameters("%s/%s_L2L3Residual_%s.txt" % (path,globalTag,jetFlavour))
            self.vPar.push_back(self.ResJetPar);
        #Step3 (Construct a FactorizedJetCorrector object) 
        self.JetCorrector = ROOT.FactorizedJetCorrector(self.vPar)
        if os.path.exists("%s/%s_Uncertainty_%s.txt" % (path,globalTag,jetFlavour)):
            self.JetUncertainty = ROOT.JetCorrectionUncertainty("%s/%s_Uncertainty_%s.txt" % (path,globalTag,jetFlavour));
        elif os.path.exists("%s/Uncertainty_FAKE.txt" % path):
            self.JetUncertainty = ROOT.JetCorrectionUncertainty("%s/Uncertainty_FAKE.txt" % path);
        else:
            print 'Missing JEC uncertainty file "%s/%s_Uncertainty_%s.txt", so jet energy uncertainties will not be available' % (path,globalTag,jetFlavour)
            self.JetUncertainty = None
        self.separateJetCorrectors = {}
        if calculateSeparateCorrections or calculateType1METCorrection:
            self.vParL1 = ROOT.vector(ROOT.JetCorrectorParameters)()
            self.vParL1.push_back(self.L1JetPar)
            self.separateJetCorrectors["L1"] = ROOT.FactorizedJetCorrector(self.vParL1)
            if upToLevel >= 2 and calculateSeparateCorrections:
                self.vParL2 = ROOT.vector(ROOT.JetCorrectorParameters)()
                for i in [self.L1JetPar,self.L2JetPar]: self.vParL2.push_back(i)
                self.separateJetCorrectors["L1L2"] = ROOT.FactorizedJetCorrector(self.vParL2)
            if upToLevel >= 3 and calculateSeparateCorrections:
                self.vParL3 = ROOT.vector(ROOT.JetCorrectorParameters)()
                for i in [self.L1JetPar,self.L2JetPar,self.L3JetPar]: self.vParL3.push_back(i)
                self.separateJetCorrectors["L1L2L3"] = ROOT.FactorizedJetCorrector(self.vParL3)
            if doResidualJECs and calculateSeparateCorrections:
                self.vParL3Res = ROOT.vector(ROOT.JetCorrectorParameters)()
                for i in [self.L1JetPar,self.L2JetPar,self.L3JetPar,self.ResJetPar]: self.vParL3Res.push_back(i)
                self.separateJetCorrectors["L1L2L3Res"] = ROOT.FactorizedJetCorrector(self.vParL3Res)

    def getCorrection(self,jet,rho,delta=0,corrector=None):
        if not corrector: corrector = self.JetCorrector
        if corrector != self.JetCorrector and delta!=0: raise RuntimeError('Configuration not supported')
        corrector.setJetEta(jet.eta)
        corrector.setJetPt(jet.pt*(1.-jet.rawFactor))
        corrector.setJetA(jet.area)
        corrector.setRho(rho)
        corr = corrector.getCorrection()
        if delta != 0:
            if not self.JetUncertainty: raise RuntimeError("Jet energy scale uncertainty shifts requested, but not available")
            self.JetUncertainty.setJetEta(jet.eta())
            self.JetUncertainty.setJetPt(corr * jet.pt() * jet.rawFactor())
            try:
                jet.jetEnergyCorrUncertainty = self.JetUncertainty.getUncertainty(True) 
            except RuntimeError as r:
                print "Caught %s when getting uncertainty for jet of pt %.1f, eta %.2f\n" % (r,corr * jet.pt() * jet.rawFactor(),jet.eta())
                jet.jetEnergyCorrUncertainty = 0.5
            #print "   jet with corr pt %6.2f has an uncertainty %.2f " % (jet.pt()*jet.rawFactor()*corr, jet.jetEnergyCorrUncertainty)
            corr *= max(0, 1+delta*jet.jetEnergyCorrUncertainty)
        return corr


    def correct(self,jet,rho,delta=0,addCorr=False,addShifts=False, metShift=[0,0]):
        """Corrects a jet energy (optionally shifting it also by delta times the JEC uncertainty)

           If addCorr, set jet.corr to the correction.
           If addShifts, set also the +1 and -1 jet shifts 

           The metShift vector will accumulate the x and y changes to the MET from the JEC, i.e. the 
           negative difference between the new and old jet momentum, for jets eligible for type1 MET 
           corrections, and after subtracting muons. The pt cut is applied to the new corrected pt.
           This shift can be applied on top of the *OLD TYPE1 MET*, but only if there was no change 
           in the L1 corrections nor in the definition of the type1 MET (e.g. jet pt cuts).

        """
        raw = 1.-jet.rawFactor  
        corr = self.getCorrection(jet,rho,delta)
        if corr <= 0:
            return jet.pt
        newpt = jet.pt*raw*corr
        return newpt


