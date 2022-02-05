import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import numpy as np
from root_numpy import tree2array

class bffPreselProducer(Module):
    def beginJob(self):
        pass

    def endJob(self):
        pass

    def ptSel(self, obj, variation, met=0):
        if variation=="jerUp": pt = obj.pt_jerUp
        elif variation=="jerDown": pt = obj.pt_jerDown
        elif variation=="jesTotalUp": pt = obj.pt_jesTotalUp
        elif variation=="jesTotalDown": pt = obj.pt_jesTotalDown
        else: 
            if met: pt = obj.pt
            else:
                if self.isMC:
                    pt = obj.pt_nom
                else: pt = obj.pt
        return pt
    def bjetSel(self, jet, variation):
        btagWP = self.btagWP
        pt = self.ptSel(jet,variation)
        return ((pt > 20) & (self.select_btag(jet)) & (abs(jet.eta) < 2.4) & (jet.jetId > 3) & ((jet.puId & 1) | (pt>50)))
    def lightjetSel(self, jet, variation):
        btagWP = self.btagWP
        pt = self.ptSel(jet,variation)
        return ((pt > 30) & (not self.select_btag(jet)) & (abs(jet.eta) < 2.4) & (jet.jetId > 3) & ((jet.puId & 1) | (pt > 50)))
    def alljetSel(self, jet, variation):
        btagWP = self.btagWP
        return (self.bjetSel(jet, variation) or self.lightjetSel(jet, variation))
    def __init__(self, btagWP, triggers, btag_type="DeepCSV", isMC=False, dr_cut=False):
        self.triggers = triggers
        self.btagWP = btagWP
        #select different btags
        def deepcsv(jet):
            return jet.btagDeepB > self.btagWP
        def deepflavour(jet):
            return jet.btagDeepFlavB > self.btagWP
           #set right filtering function
        if btag_type=="DeepCSV":
            self.select_btag = deepcsv
        elif btag_type=="DeepFlavour":
            self.select_btag = deepflavour
        print("btag wp: {} type: {}".format(self.btagWP, btag_type))
        self.muSel = lambda x,pt: ((x.corrected_pt > pt) & (abs(x.eta) < 2.4) & (x.tightId > 0) 
                               & (x.pfRelIso04_all < 0.25))
        self.eleSel = lambda x,pt: ((x.pt > pt) & (abs(x.eta) < 2.4) & x.cutBased_HEEP > 0)
        self.diLepMass = -1
        self.lep_1 = ROOT.TLorentzVector()
        self.lep_2 = ROOT.TLorentzVector()
        self.isMC = isMC
        self.dr_cut = dr_cut
        self.sysDict = {}
        self.sysDict['nom']= {'lightJetSel': lambda sel:self.lightjetSel(sel,"nom"),
        'bjetSel': lambda sel:self.bjetSel(sel,"nom"),
        'alljetSel': lambda sel:self.alljetSel(sel,"nom"),
        'met': lambda sel:self.ptSel(sel,"nom",met=1)}
        pass

    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        '''
        In case of data, the b-tagging scale factors are not produced. 
        Check whether they were produced and if not, drop them from jet selections
        '''
        list_of_branches = wrappedOutputTree.tree().GetListOfBranches()
        self._triggers = [trigger for trigger in self.triggers if trigger in list_of_branches]
        print(self._triggers)
        if self.isMC:
            self.sysDict['jerUp']= {'lightJetSel': lambda sel:self.lightjetSel(sel,"jerUp"),
            'bjetSel': lambda sel:self.bjetSel(sel,"jerUp"),
            'alljetSel': lambda sel:self.alljetSel(sel,"jerUp"),
            'met': lambda sel:self.ptSel(sel,"jerUp", met=1)}
            self.sysDict['jerDown']= {'lightJetSel': lambda sel:self.lightjetSel(sel,"jerDown"),
            'bjetSel': lambda sel:self.bjetSel(sel,"jerDown"),
            'alljetSel': lambda sel:self.alljetSel(sel,"jerDown"),
            'met': lambda sel:self.ptSel(sel,"jerDown",met=1)}
            self.sysDict['jesTotalUp']= {'lightJetSel': lambda sel:self.lightjetSel(sel,"jesTotalUp"),
            'bjetSel': lambda sel:self.bjetSel(sel,"jesTotalUp"),
            'alljetSel': lambda sel:self.alljetSel(sel,"jesTotalUp"),
            'met': lambda sel:self.ptSel(sel,"jesTotalUp",met=1)}
            self.sysDict['jesTotalDown']= {'lightJetSel': lambda sel:self.lightjetSel(sel,"jesTotalDown"),
            'bjetSel': lambda sel:self.bjetSel(sel,"jesTotalDown"),
            'alljetSel': lambda sel:self.alljetSel(sel,"jesTotalDown"),
            'met': lambda sel:self.ptSel(sel,"jesTotalDown",met=1)}
        self.out = wrappedOutputTree
        for key in self.sysDict:
            self.out.branch("nBjets_{}".format(key), "F")
            self.out.branch("nSeljets_{}".format(key), "F")
            self.out.branch("JetSFWeight_{}".format(key), "F")
            self.out.branch("HTLT_{}".format(key), "F")
            self.out.branch("RelMET_{}".format(key), "F")
            self.out.branch("TMB_{}".format(key), "F")
            self.out.branch("TMBMin_{}".format(key), "F")
            self.out.branch("TMBMax_{}".format(key), "F")
            self.out.branch("SR1_{}".format(key), "I")
            self.out.branch("CR10_{}".format(key), "I")
            self.out.branch("CR11_{}".format(key), "I")
            self.out.branch("CR12_{}".format(key), "I")
            self.out.branch("CR13_{}".format(key), "I")
            self.out.branch("CR14_{}".format(key), "I")
            self.out.branch("SR2_{}".format(key), "I")
            self.out.branch("CR20_{}".format(key), "I")
            self.out.branch("CR21_{}".format(key), "I")
            self.out.branch("CR22_{}".format(key), "I")
            self.out.branch("CR23_{}".format(key), "I")
            self.out.branch("CR24_{}".format(key), "I")
        self.out.branch("DiLepMass", "F")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def selectDiMu(self, electrons, muons):
        if len(muons) != 2:
            return False
        if len(electrons) != 0:
            return False
        if (muons[0].charge+muons[1].charge) != 0:
            return False
        self.lep_1 = muons[0].p4()*(muons[0].corrected_pt/muons[0].pt)
        self.lep_2 = muons[1].p4()*(muons[1].corrected_pt/muons[1].pt)
        diLep = self.lep_1 + self.lep_2
        self.diLepMass = diLep.M()
        self.out.fillBranch("DiLepMass", self.diLepMass)
        return True
    def selectDiEle(self, electrons, muons):
        if len(electrons) != 2:
            return False
        if len(muons) != 0:
            return False
        if (electrons[0].charge+electrons[1].charge) != 0:
            return False
        self.lep_1 = electrons[0].p4()
        self.lep_2 = electrons[1].p4()
        diLep = self.lep_1 + self.lep_2
        self.diLepMass = diLep.M()
        self.out.fillBranch("DiLepMass", self.diLepMass)
        return True
    def selectEleMu(self, electrons, muons):
        if len(electrons) != 1:
            return False
        if len(muons) != 1:
            return False
        if (electrons[0].charge+muons[0].charge) != 0:
            return False
        self.lep_1 = electrons[0].p4()
        self.lep_2 = muons[0].p4()*(muons[0].corrected_pt/muons[0].pt)
        diLep = self.lep_1 + self.lep_2
        self.diLepMass = diLep.M()
        self.out.fillBranch("DiLepMass", self.diLepMass)
        return True

    def analyze(self, event):
        HLT_select = False
        for trigger in self._triggers:
            if event[trigger]: 
                HLT_select = 1
                break
        if not HLT_select: return False
        electrons = sorted(filter(lambda x: self.eleSel(x,53), Collection(event, "Electron")), key=lambda x: x.pt)
        muons = sorted(filter(lambda x: self.muSel(x,53), Collection(event, "Muon")), key=lambda x: x.corrected_pt)
        if self.isMC:
            MET = Object(event, "MET_T1Smear")
        else:
            MET = Object(event,"MET")
        electronsLowPt = sorted(filter(lambda x: self.eleSel(x,24), Collection(event, "Electron")), key=lambda x: x.pt)
        muonsLowPt = sorted(filter(lambda x: self.muSel(x,24), Collection(event, "Muon")), key=lambda x: x.corrected_pt)
        nLowPtLep = len(electronsLowPt)+len(muonsLowPt)
        isDiMu = self.selectDiMu(electrons, muons) and nLowPtLep<3
        isDiEle = self.selectDiEle(electrons, muons) and nLowPtLep<3
        isEleMu = self.selectEleMu(electrons, muons) and nLowPtLep<3
        if not (isDiMu or isDiEle or isEleMu):
            return False
        eventSelected = False
        for key in self.sysDict:
            lightJetSel = self.sysDict[key]['lightJetSel']
            bjetSel = self.sysDict[key]['bjetSel']
            alljetSel = self.sysDict[key]['alljetSel']
    
            """process event, return True (go to next module) or False (fail, go to next event)"""
            jets = sorted(filter(alljetSel, Collection(event, "Jet")), key=lambda x: self.ptSel(x,key))

            def minDR(x,ys):
                minDR = 9999
                for y in ys:
                    minDR =min(minDR, x.p4().DeltaR(y.p4()))
                return minDR

            muon_dr = [minDR(jet, muonsLowPt) for jet in jets]
            electron_dr = [minDR(jet, electronsLowPt) for jet in jets]
            dr_arr = np.array([muon_dr, electron_dr])
            dr_cut_arr =  dr_arr.min(axis=0) > .4
           
            if self.dr_cut:
                jets = np.array(jets)[dr_cut_arr]

            metPt = self.ptSel(MET,key,met=1)

            n_Bjets = len(filter(bjetSel, jets))
            n_lightjets = len(filter(lightJetSel, jets))
            self.out.fillBranch("nBjets_{}".format(key), n_Bjets)
            n_alljets = len(jets)
            self.out.fillBranch("nSeljets_{}".format(key), n_alljets)

            if n_alljets==1 or n_alljets==2:

                eventSelected = True

            jetSFWeight = 1
            if self.isMC:
                for j in jets:
                    jetSFWeight *= j.btagSF_deepcsv_M
            self.out.fillBranch("JetSFWeight_{}".format(key), jetSFWeight)

            htlt = (sum([j.pt for j in jets]) 
                   - sum([ele.pt for ele in electrons]) 
                   - sum([mu.corrected_pt for mu in muons]))
            self.out.fillBranch("HTLT_{}".format(key), htlt)
            
            self.out.fillBranch("RelMET_{}".format(key), metPt/self.diLepMass)
            isSR1  = isDiMu  & (n_Bjets == 1) & (n_lightjets == 0)
            isCR10 = isDiMu  & (n_Bjets == 0) & (n_lightjets == 1)
            isCR11 = isEleMu & (n_Bjets == 1) & (n_lightjets == 0)
            isCR12 = isEleMu & (n_Bjets == 0) & (n_lightjets == 1)
            isCR13 = isDiEle & (n_Bjets == 1) & (n_lightjets == 0)
            isCR14 = isDiEle & (n_Bjets == 0) & (n_lightjets == 1)
            isSR2  = isDiMu  & (n_Bjets >= 1) & (n_alljets == 2)
            isCR20 = isDiMu  & (n_Bjets == 0) & (n_alljets == 2)
            isCR21 = isEleMu & (n_Bjets >= 1) & (n_alljets == 2)
            isCR22 = isEleMu & (n_Bjets == 0) & (n_alljets == 2)
            isCR23 = isDiEle & (n_Bjets >= 1) & (n_alljets == 2)
            isCR24 = isDiEle & (n_Bjets == 0) & (n_alljets == 2)

            self.out.fillBranch("SR1_{}".format(key), isSR1)
            self.out.fillBranch("CR10_{}".format(key), isCR10)
            self.out.fillBranch("CR11_{}".format(key), isCR11)
            self.out.fillBranch("CR12_{}".format(key), isCR12)
            self.out.fillBranch("CR13_{}".format(key), isCR13)
            self.out.fillBranch("CR14_{}".format(key), isCR14)
            self.out.fillBranch("SR2_{}".format(key), isSR2)
            self.out.fillBranch("CR20_{}".format(key), isCR20)
            self.out.fillBranch("CR21_{}".format(key), isCR21)
            self.out.fillBranch("CR22_{}".format(key), isCR22)
            self.out.fillBranch("CR23_{}".format(key), isCR23)
            self.out.fillBranch("CR24_{}".format(key), isCR24)

            sbm = -1.
            sbmMin = -1.
            sbmMax = -1.

            if len(jets) == 1:
                sbm1 = (self.lep_1 + jets[0].p4()).M()
                sbm2 = (self.lep_2 + jets[0].p4()).M()
                sbm = min(sbm1, sbm2)
                sbmMin = sbm
                sbmMax = max(sbm1, sbm2)
            elif len(jets) == 2:
                l1j1mass = (self.lep_1 + jets[0].p4()).M()
                l1j2mass = (self.lep_1 + jets[1].p4()).M()
                l2j1mass = (self.lep_2 + jets[0].p4()).M()
                l2j2mass = (self.lep_2 + jets[1].p4()).M()
                if abs(l1j1mass - l2j2mass) < abs(l2j1mass - l1j2mass):
                    sbm = max(l1j1mass, l2j2mass)
                    sbmMin = min(l1j1mass, l2j2mass)
                    sbmMax = sbm
                else:
                    sbm = max(l1j2mass, l2j1mass)
                    sbmMin = min(l1j2mass, l2j1mass)
                    sbmMax = sbm
            else:
                pass
            self.out.fillBranch("TMB_{}".format(key), sbm)
            self.out.fillBranch("TMBMin_{}".format(key), sbmMin)
            self.out.fillBranch("TMBMax_{}".format(key), sbmMax)

        if eventSelected: return True
        else: return True

