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
        a = (mu*leptonPz) / (TMath.Power(leptonE, 2.) - TMath.Power(leptonPz, 2.))
        a2 = TMath.Power(a, 2.)
        b = TMath.Power(leptonE, 2.)*(MisET2) - TMath.Power(mu, 2.)/TMath.Power(leptonE, 2.) - TMath.Power(leptonPz, 2.)

        p4nu_rec = root.TLorentzVector()
        p4W_rec = root.TLorentzVector()
        p4b_rec = root.TLorentzVector()
        p4Top_rec = root.TLorentzVector()
        p4lep_rec = root.TLorentzVector()
        neutrino = root.TLorentzVector()

        p4lep_rec.SetPxPyPzE(leptonPx, leptonPy, leptonPz, leptonE)
        p40_rec = root.TLorentzVector(0.0, 0.0, 0.0, 0.0)

        if (a2-b) > 0:
            root = TMath((a2-b), 0.5)
            pz1 = a + root
            pz2 = a - root
            nNuSol = 2
            pznu = 0.0

            if abs(pz1) > abs(pz2):
                pznu = pz2
            else:
                pznu = pz1

            Enu = TMath.Power((MisET2 + pznu**2), 0.5)
            p4nu_rec.SetPxPyPzE(metPx, metPy, pznu, Enu)
            neutrino = p4nu_rec

        else:
            ptlep = leptonPt
            pxlep = leptonPx
            pylep = leptonPy
            metpx = metPx
            metpy = metPy

            EquationCoeff = {'a': 1,
                             'b': (-3 * pylep * mW / ptlep),
                             'c': (((mW**2.) * (2. * pylep**2.) / (ptlep**2)) + mW**2. - (4. * pxlep**3. * metpx / ptlep**2) - (4. * pxlep**2. * pylep * metpy / ptlep**2)),
                             'd': ((4. * pxlep**2. * mW * metpy / ptlep) - pylep * mW**3. / ptlep)}
        
        return neutrino

    def top4Momentum(self, lepton, jet, metPx, metPy):
        leptonPx = lepton.Px()
        leptonPy = lepton.Py()
        leptonPz = lepton.Pz()
        leptonPt = lepton.Pt()
        leptonE = lepton.Energy()
        neutrino = self.NuMomentum(leptonPx, leptonPy, leptonPz, leptonPt, leptonE, metPx, metPy)
        top = lepton + jet + neutrino
        #print top.Pt(), top.Eta(), top.Phi(), top.E()
        return top

'''reco = TopUtilities()
lep = root.TLorentzVector(1.04, 5.08, 6.07, 9.56)
jet = root.TLorentzVector(-5.03, 17.07, -8.06, 5.98)
metPx = 9.45
metPy = 10.67

vector = reco.top4Momentum(lep, jet, metPx, metPy)'''
