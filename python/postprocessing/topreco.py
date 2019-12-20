import math as math
import cmath
import string
import io
import copy
import EquationSolver
import tools
import ROOT
import ROOT.TMath as TMath

class TopUtilities():
    def __init__(self, lepton = None, jet = None, MET = None):
        self.reco_topqv = ROOT.TLorentzVector()
        self.reco_topMt = 0.
        self.neutrino = ROOT.TLorentzVector()
        self.lepton = copy.deepcopy(lepton)
        self.IsParticle = True
        self.IsReco = False

        if not lepton is None and not jet is None and not MET is None:
            self.RecoTop4Momentum(lepton, jet, MET['metPx'], MET['metPy'])
            self.RecoTopMtw(lepton, jet, MET['metPx'], MET['metPy'])
            self.IsReco = True

    def RecoNuMomentum(self,  leptonPx, leptonPy, leptonPz, leptonPt, leptonE, metPx, metPy):
        mW = 80.399
        
        MisET2 = (metPx**2. + metPy**2.)
        mu = (mW**2.)/2. + metPx*leptonPx + metPy*leptonPy
        a = (mu*leptonPz) / (TMath.Power(leptonE, 2.) - TMath.Power(leptonPz, 2.))
        a2 = TMath.Power(a, 2.)
        b = TMath.Power(leptonE, 2.)*(MisET2) - TMath.Power(mu, 2.)/TMath.Power(leptonE, 2.) - TMath.Power(leptonPz, 2.)

        p4nu_rec = ROOT.TLorentzVector()
        p4W_rec = ROOT.TLorentzVector()
        p4b_rec = ROOT.TLorentzVector()
        p4Top_rec = ROOT.TLorentzVector()
        p4lep_rec = ROOT.TLorentzVector()
        neutrino = ROOT.TLorentzVector()

        p4lep_rec.SetPxPyPzE(leptonPx, leptonPy, leptonPz, leptonE)
        p40_rec = ROOT.TLorentzVector(0.0, 0.0, 0.0, 0.0)

        if (a2-b) > 0:
            root = TMath.Power((a2-b), 0.5)
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

            EquationCoeff1 = {'a': 1,
                             'b': (-3 * pylep * mW / ptlep),
                             'c': (((mW**2.) * (2. * pylep**2.) / (ptlep**2)) + mW**2. - (4. * pxlep**3. * metpx / ptlep**2) - (4. * pxlep**2. * pylep * metpy / ptlep**2)),
                             'd': ((4. * pxlep**2. * mW * metpy / ptlep) - pylep * mW**3. / ptlep)}

            EquationCoeff2 = EquationCoeff1.copy()
            EquationCoeff2['b'] = - EquationCoeff2['b']
            EquationCoeff2['d'] = - EquationCoeff2['d']
            #solutions1 = EquationSolver.EqSolv(EquationCoeff1,'','','')
            #solutions2 = EquationSolver.EqSolv(EquationCoeff2,'','','')

            solutions = [EquationSolver.EqSolv(EquationCoeff1,'','',''), EquationSolver.EqSolv(EquationCoeff2,'','','')]
            
            deltaMin = 14000.**2.
            zeroValue = - mW**2./(4.*pxlep)
            minPx = 0.
            minPy = 0.

            ncoeff = ['x1', 'x2', 'x3']

            for j in range(2):
                for i in ncoeff:
                    if solutions[j][i] < 0.:
                        continue

                    p_x = (solutions[j][i]**2. - mW**2.) / (4.*pxlep)
                    p_y = ((mW**2.)*pylep + 2.*pxlep*pylep*p_x - mW*ptlep*solutions[j][i]) / (2*pxlep**2.)
                    Delta2 = (p_x - metpx)**2. + (p_y - metpy)**2.

                    if Delta2 < deltaMin and Delta2 > 0 :
                        deltaMin = Delta2
                        minPx = p_x
                        minPy = p_y
                    
            pyZeroValue = mW**2.*pxlep + 2.*pylep*zeroValue
            delta2ZeroValue = (zeroValue - metpx)**2. + (pyZeroValue - metpy)**2.

            if deltaMin == 14000.**2. :
                return neutrino

            if delta2ZeroValue < deltaMin :
                deltaMin = delta2ZeroValue
                minPx = zeroValue
                minPy = pyZeroValue

            mu_Minimum = mW**2./2. + minPx*pxlep*minPy*pylep
            a_Minimum = (mu_Minimum*leptonPz) / (leptonE**2. - leptonPz**2.)
            pznu = a_Minimum
            Enu = TMath.Power((minPx**2. + minPy**2. + pznu**2.), 0.5)
            p4nu_rec.SetPxPyPzE(minPx, minPy, pznu, Enu)

            neutrino = p4nu_rec
            
        self.neutrino = neutrino
#        return neutrino

    def RecoTop4Momentum(self, lepton, jet, metPx, metPy):
        topMt = self.RecoTopMtw(lepton, jet, metPx, metPy)
        '''if topMt == None:
            self.reco_topqv = None
            self.neutrino = None
            return None'''

        leptonPx = lepton.Px()
        leptonPy = lepton.Py()
        leptonPz = lepton.Pz()
        leptonPt = lepton.Pt()
        leptonE = lepton.Energy()

        self.RecoNuMomentum(leptonPx, leptonPy, leptonPz, leptonPt, leptonE, metPx, metPy)
        top = lepton + jet + self.neutrino

        self.reco_topqv = top
        
    def RecoTopMtw(self, lepton, jet, metPx, metPy):
        lb = lepton + jet
        mlb2 = lb.M2()
        ptlb = lb.Pt()
        pxlb = lb.Px()
        pylb = lb.Py()
        
        if mlb2 < 0.:
            self.reco_topMt = None
            self.IsParticle = False
            return None
        
        etlb = TMath.Power((mlb2 + ptlb**2.), 0.5)
        metPt = TMath.Power(metPx**2. + metPy**2.)

        self.reco_topMt = TMath.Power((mlb2 + 2.*(etlb*metPt - pxlb*metPx - pylb*metPy)), 0.5)

    def top4Momentum(self, lepton = None, jet = None, MET = None):
        if self.IsReco:
            return self.reco_topqv

        if (not lepton is None and not jet is None and not MET is None and self.IsReco) or not self.IsReco:
            self.RecoTop4Momentum(lepton, jet, MET['metPx'], MET['metPy'])
            self.IsReco = True
            return self.reco_topqv
            
    def topMtw(self):
        if self.IsReco:
            return self.reco_topMt

        if (not lepton is None and not jet is None and not MET is None and self.IsReco) or not self.IsReco:
            self.RecoTop4Mtw(lepton, jet, MET['metPx'], MET['metPy'])
            self.IsReco = True
            return self.reco_topMt

    def neutrino(self):
        if self.IsReco:
            return self.neutrino
        else:
            return None

    def IsAcceptable(self):
        return IsParticle


lep = ROOT.TLorentzVector(1.04, 5.08, 6.07, 9.56)
jet = ROOT.TLorentzVector(-5.03, 17.07, -8.06, 5.98)
MET={'metPx': 9.45,
     'metPy': 10.67}

'''
#First way to use the class
reco = TopUtilities(lep, jet, MET)
vector = reco.top4Momentum()
if not (vector is None):
    print vector.Print()

#Second way to use the class
reco = TopUtilities()
vector = reco.top4Momentum(lep, jet, MET)
if not (vector is None):
    print vector.Print()
'''

