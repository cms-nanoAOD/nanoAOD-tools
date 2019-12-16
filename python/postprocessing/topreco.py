import math as math
import cmath
import string
import io
import EquationSolver
import tools
import ROOT as root
import ROOT.TMath as TMath

class TopUtilities():
    def __init__(self):
        self.reco_qv = root.TLorentzVector()
        self.reco_topMt = 0.

    def NuMomentum(self,  leptonPx, leptonPy, leptonPz, leptonPt, leptonE, metPx, metPy):
        mW = 80.399
        
        MisET2 = (metPx**2. + metPy**2.)
        mu = (mW**2.)/2. + metPx*leptonPx + metPy*leptonPy
        a = (mu*leptonPz) / (leptonE**2. - leptonPz**2.)
        a2 = TMath.Power(a, 2.)

    def top4Momentum(self, lepton, jet, metPx, metPy):
        neutrino = self.NuMomentum(lepton.Px(), lepton.Py(), lepton.Pz(), lepton.Pt(), lepton.E, metPx, metPy)
        top = lepton + jet + neutrino
        return top

reco = TopUtilities()
lep = root.TLorentzVector(1.0, 5.0, 6.0, 9.)
jet = root.TLorentzVector(-5.0, 17.0, -8.0, 5.)
metPx = 9.
metPy = 10.

#reco.top4Momentum(lep, jet, metPx, metPy)
