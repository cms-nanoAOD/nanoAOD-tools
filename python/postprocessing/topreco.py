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
    def __init__(self):
        if False:
            print 'ok'

    def NuMomentum(self,  leptonPx, leptonPy, leptonPz, leptonPt, leptonE, metPx, metPy):
        mW = 80.399
        '''
        print leptonPx
        print leptonPy
        print leptonPz
        print leptonPt
        print leptonE
        print metPx
        print metPy
        '''
        MisET2 = (metPx**2. + metPy**2.)
        mu = (mW**2.)/2. + metPx*leptonPx + metPy*leptonPy
        a = mu*leptonPz/leptonPt**2
        a2 = a**2.
        b = (leptonE**2.*MisET2 - mu**2.)/leptonPt**2
        '''
        print MisET2
        print mu
        print a
        print a2
        print b
        '''
        p4nu_rec = ROOT.TLorentzVector()
        p4W_rec = ROOT.TLorentzVector()
        p4b_rec = ROOT.TLorentzVector()
        p4Top_rec = ROOT.TLorentzVector()
        p4lep_rec = ROOT.TLorentzVector()
        neutrino = ROOT.TLorentzVector()

        p4lep_rec.SetPxPyPzE(leptonPx, leptonPy, leptonPz, leptonE)
        p40_rec = ROOT.TLorentzVector(0.0, 0.0, 0.0, 0.0)

        if (a2-b) > 0:
            root = (a2-b)**0.5
            pz1 = a + root
            pz2 = a - root
            nNuSol = 2
            pznu = 0.0
            if abs(pz1) > abs(pz2):
                pznu = pz2
            else:
                pznu = pz1

            Enu = (MisET2 + pznu**2)**0.5
            p4nu_rec.SetPxPyPzE(metPx, metPy, pznu, Enu)
            neutrino = p4nu_rec
        else:
            ptlep = leptonPt
            pxlep = leptonPx
            pylep = leptonPy
            metpx = metPx
            metpy = metPy

            EquationCoeff1 = [1,
                              (-3 * pylep * mW / ptlep),
                              (((mW**2.) * (2. * pylep**2.) / (ptlep**2)) + mW**2. - (4. * pxlep**3. * metpx / ptlep**2) - (4. * pxlep**2. * pylep * metpy / ptlep**2)),
                              ((4. * pxlep**2. * mW * metpy / ptlep) - pylep * mW**3. / ptlep)
                              ]

            EquationCoeff2 = copy.copy(EquationCoeff1)
            EquationCoeff2[1] = - EquationCoeff2[1]
            EquationCoeff2[3] = - EquationCoeff2[3]
            #solutions1 = EquationSolver.EqSolv(EquationCoeff1,'','','')
            #solutions2 = EquationSolver.EqSolv(EquationCoeff2,'','','')

            solutions = [EquationSolver.EqSolv(EquationCoeff1,'','',''), EquationSolver.EqSolv(EquationCoeff2,'','','')]

            deltaMin = 14000.**2.
            zeroValue = - mW**2./(4.*pxlep)
            minPx = 0.
            minPy = 0.

            ncoeff = ['x1', 'x2', 'x3']

            for j in range(2):
                for value in solutions[j]:
                    if value < 0.:
                        continue
                    p_x = (value**2. - mW**2.) / (4.*pxlep)
                    p_y = ((mW**2.)*pylep + 2.*pxlep*pylep*p_x - mW*ptlep*value) / (2*pxlep**2.)
                    Delta2 = (p_x - metpx)**2. + (p_y - metpy)**2.
                    if Delta2 < deltaMin and Delta2 > 0:
                        deltaMin = copy.copy(Delta2)
                        minPx = copy.copy(p_x)
                        minPy = copy.copy(p_y)

            pyZeroValue = mW**2.*pxlep + 2.*pylep*zeroValue
            delta2ZeroValue = (zeroValue - metpx)**2. + (pyZeroValue - metpy)**2.

            if deltaMin == 14000.**2. :
                return neutrino

            if delta2ZeroValue < deltaMin :
                deltaMin = copy.copy(delta2ZeroValue)
                minPx = copy.copy(zeroValue)
                minPy = copy.copy(pyZeroValue)

            mu_Minimum = mW**2./2. + minPx*pxlep*minPy*pylep
            a_Minimum = (mu_Minimum*leptonPz) / (leptonE**2. - leptonPz**2.)
            pznu = a_Minimum
            Enu = TMath.Power((minPx**2. + minPy**2. + pznu**2.), 0.5)
            p4nu_rec.SetPxPyPzE(minPx, minPy, pznu, Enu)

            neutrino = p4nu_rec
            
        return neutrino

    def top4Momentum(self, lepton, jet, metPx, metPy):
        #topMt = self.topMtw(lepton, jet, metPx, metPy)
        '''if topMt == None:
            self.reco_topqv = None
            self.neutrino = None
            return None'''

        leptonPx = lepton.Px()
        leptonPy = lepton.Py()
        leptonPz = lepton.Pz()
        leptonPt = lepton.Pt()
        leptonE = lepton.Energy()

        neutrino = self.NuMomentum(leptonPx, leptonPy, leptonPz, leptonPt, leptonE, metPx, metPy)
        top = lepton + jet + neutrino

        return top
        
    def topMtw(self, lepton, jet, metPx, metPy):
        lb = lepton + jet
        mlb2 = lb.M2()
        ptlb = lb.Pt()
        pxlb = lb.Px()
        pylb = lb.Py()
        
        '''
        if mlb2 < 0.:
            self.reco_topMt = None
            self.IsParticle = False
            return None
        '''

        etlb = TMath.Power((mlb2 + ptlb**2.), 0.5)
        metPt = TMath.Power((metPx**2. + metPy**2.), 0.5)

        return TMath.Power((mlb2 + 2.*(etlb*metPt - pxlb*metPx - pylb*metPy)), 0.5)


lep = ROOT.TLorentzVector()
lep.SetPxPyPzE(-167.04, 56.08, -996.07, 9.56)
jet = ROOT.TLorentzVector()
jet.SetPxPyPzE(-50.03, 1117.07, -856.06, 10.98)
MET={'metPx': 90.45,
     'metPy': 109.67}

#way to use the class
reco = TopUtilities()
vector = reco.top4Momentum(lep, jet, MET['metPx'], MET['metPy'])
if not (vector is None):
    print vector.Print()
