

import ROOT
import array
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Object 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class vbfhmmProducer(Module):
    def __init__(self, jetSelection, muSelection, data, year="2016"):
        self.jetSel = jetSelection
        self.muSel = muSelection
        self.data = data
        self.year = year
        self.jesVariation = ['pt', 'pt_nom', 'pt_jesAbsoluteStatDown', 'pt_jesAbsoluteScaleDown', 'pt_jesAbsoluteFlavMapDown', 'pt_jesAbsoluteMPFBiasDown', 'pt_jesFragmentationDown', 'pt_jesSinglePionECALDown', 'pt_jesSinglePionHCALDown', 'pt_jesFlavorQCDDown', 'pt_jesTimePtEtaDown', 'pt_jesRelativeJEREC1Down', 'pt_jesRelativeJEREC2Down', 'pt_jesRelativeJERHFDown', 'pt_jesRelativePtBBDown', 'pt_jesRelativePtEC1Down', 'pt_jesRelativePtEC2Down', 'pt_jesRelativePtHFDown', 'pt_jesRelativeBalDown', 'pt_jesRelativeSampleDown', 'pt_jesRelativeFSRDown', 'pt_jesRelativeStatFSRDown', 'pt_jesRelativeStatECDown', 'pt_jesRelativeStatHFDown', 'pt_jesPileUpDataMCDown', 'pt_jesPileUpPtRefDown', 'pt_jesPileUpPtBBDown', 'pt_jesPileUpPtEC1Down', 'pt_jesPileUpPtEC2Down', 'pt_jesPileUpPtHFDown', 'pt_jesPileUpMuZeroDown', 'pt_jesPileUpEnvelopeDown', 'pt_jesSubTotalPileUpDown', 'pt_jesSubTotalRelativeDown', 'pt_jesSubTotalPtDown', 'pt_jesSubTotalScaleDown', 'pt_jesSubTotalAbsoluteDown', 'pt_jesSubTotalMCDown', 'pt_jesTotalDown', 'pt_jesTotalNoFlavorDown', 'pt_jesTotalNoTimeDown', 'pt_jesTotalNoFlavorNoTimeDown', 'pt_jesFlavorZJetDown', 'pt_jesFlavorPhotonJetDown', 'pt_jesFlavorPureGluonDown', 'pt_jesFlavorPureQuarkDown', 'pt_jesFlavorPureCharmDown', 'pt_jesFlavorPureBottomDown', 'pt_jesCorrelationGroupMPFInSituDown', 'pt_jesCorrelationGroupIntercalibrationDown', 'pt_jesCorrelationGroupbJESDown', 'pt_jesCorrelationGroupFlavorDown', 'pt_jesCorrelationGroupUncorrelatedDown', 'pt_jesAbsoluteStatUp', 'pt_jesAbsoluteScaleUp', 'pt_jesAbsoluteFlavMapUp', 'pt_jesAbsoluteMPFBiasUp', 'pt_jesFragmentationUp', 'pt_jesSinglePionECALUp', 'pt_jesSinglePionHCALUp', 'pt_jesFlavorQCDUp', 'pt_jesTimePtEtaUp', 'pt_jesRelativeJEREC1Up', 'pt_jesRelativeJEREC2Up', 'pt_jesRelativeJERHFUp', 'pt_jesRelativePtBBUp', 'pt_jesRelativePtEC1Up', 'pt_jesRelativePtEC2Up', 'pt_jesRelativePtHFUp', 'pt_jesRelativeBalUp', 'pt_jesRelativeSampleUp', 'pt_jesRelativeFSRUp', 'pt_jesRelativeStatFSRUp', 'pt_jesRelativeStatECUp', 'pt_jesRelativeStatHFUp', 'pt_jesPileUpDataMCUp', 'pt_jesPileUpPtRefUp', 'pt_jesPileUpPtBBUp', 'pt_jesPileUpPtEC1Up', 'pt_jesPileUpPtEC2Up', 'pt_jesPileUpPtHFUp', 'pt_jesPileUpMuZeroUp', 'pt_jesPileUpEnvelopeUp', 'pt_jesSubTotalPileUpUp', 'pt_jesSubTotalRelativeUp', 'pt_jesSubTotalPtUp', 'pt_jesSubTotalScaleUp', 'pt_jesSubTotalAbsoluteUp', 'pt_jesSubTotalMCUp', 'pt_jesTotalUp', 'pt_jesTotalNoFlavorUp', 'pt_jesTotalNoTimeUp', 'pt_jesTotalNoFlavorNoTimeUp', 'pt_jesFlavorZJetUp', 'pt_jesFlavorPhotonJetUp', 'pt_jesFlavorPureGluonUp', 'pt_jesFlavorPureQuarkUp', 'pt_jesFlavorPureCharmUp', 'pt_jesFlavorPureBottomUp', 'pt_jesCorrelationGroupMPFInSituUp', 'pt_jesCorrelationGroupIntercalibrationUp', 'pt_jesCorrelationGroupbJESUp', 'pt_jesCorrelationGroupFlavorUp', 'pt_jesCorrelationGroupUncorrelatedUp']
        if year == "2016" : self.jesVariation = self.jesVariation + ['pt_jesTimeRunBCDDown', 'pt_jesTimeRunEFDown', 'pt_jesTimeRunGHDown', 'pt_jesTimeRunBCDUp', 'pt_jesTimeRunEFUp', 'pt_jesTimeRunGHUp']
        if year == "2017" : self.jesVariation = self.jesVariation + ['pt_jesTimeRunBDown', 'pt_jesTimeRunCDown', 'pt_jesTimeRunDEDown', 'pt_jesTimeRunFDown', 'pt_jesTimeRunBUp', 'pt_jesTimeRunCUp', 'pt_jesTimeRunDEUp', 'pt_jesTimeRunFUp']
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("EventMass",  "F");
        self.out.branch("MuonMass",  "F");
        self.out.branch("qqMass",  "F");
        #self.out.branch("Jet_photonIdx1", "I", 1, "nJet");
        #self.out.branch("Jet_photonIdx2", "I", 1, "nJet");
        #self.out.branch("jetIdx1",  "I");
        #self.out.branch("jetIdx2",  "I");
        self.out.branch("selectionVBF",  "B");
        self.out.branch("selectionInclusive",  "B");
        #self.out.branch("jetNumber",  "I");
        #self.out.branch("bjetNumber",  "I");
        self.out.branch("muonNumber",  "I");
        #self.out.branch("Jet_VBFselected", "F", 1, "nJet");
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def mqq(self, jets):
        j1 = ROOT.TLorentzVector()
        j2 = ROOT.TLorentzVector()
        j1.SetPtEtaPhiM(jets[0].PT,jets[0].eta, jets[0].phi, jets[0].mass_nom if not self.data and self.year != "2018" else jets[0].mass)
        j2.SetPtEtaPhiM(jets[1].PT,jets[1].eta, jets[1].phi, jets[1].mass_nom if not self.data and self.year != "2018" else jets[1].mass)
        return (j1+j2).M()
        
    def analyze(self, event):
        
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        photons = Collection(event, "Photon")
        fsrPhoton = Collection(event, "FsrPhoton")

        eventSum = ROOT.TLorentzVector()
        
        mu1_charge = 0
        count_mu = 0
        dimuonSelection = False
        RaffaeleRequest = False
        mu1 = ROOT.TLorentzVector()
        mu2 = ROOT.TLorentzVector()
        dimuonMass = 0
        
        
        selectedJet = {}
        selectedJet["criteria1"] = {}
        selectedJet["criteria2"] = {}
        



        if self.data :
            if self.year == "2018" : self.jesVariation =  ['pt_nom']
            else : self.jesVariation =  ['pt']
        
        
        jet1_jesTotalDown = ROOT.TLorentzVector()
        jet2_jesTotalDown = ROOT.TLorentzVector()
        jet1_jerUp = ROOT.TLorentzVector()
        jet2_jerUp = ROOT.TLorentzVector()
        jet1_jerDown = ROOT.TLorentzVector()
        jet2_jerDown = ROOT.TLorentzVector()
        
        if len(filter(self.muSel,muons)) < 2:
            return False
        muonNumber = len(filter(self.muSel,muons))
        for lep in muons :
            muon_corrected_p4 = ROOT.TLorentzVector()
            lep.FSR_p4 = ROOT.TLorentzVector()
            muon_corrected_p4.SetPtEtaPhiM(lep.corrected_pt , lep.eta, lep.phi, lep.mass)
            lep.iso = lep.pfRelIso04_all
            lep.correctedROC_pt = lep.corrected_pt
            #if lep.iso_FSR < 0.8 : 
                #lep.FSR_p4.SetPtEtaPhiM(lep.pt_FSR , lep.eta_FSR, lep.phi_FSR, 0)
                #lep.correctedROC_pt = (muon_corrected_p4 + lep.FSR_p4).Pt()
                #lep.iso = (lep.pfRelIso04_all*lep.pt-lep.pt_FSR)/lep.correctedROC_pt
            if lep.fsrPhotonIdx!=-1 and fsrPhoton[ lep.fsrPhotonIdx].relIso03 <0.8 and fsrPhoton[ lep.fsrPhotonIdx].dROverEt2 < 0.019 :
                lep.FSR_p4.SetPtEtaPhiM(fsrPhoton[ lep.fsrPhotonIdx].pt,fsrPhoton[
                lep.fsrPhotonIdx].eta,fsrPhoton[ lep.fsrPhotonIdx].phi, 0)
                lep.correctedROC_pt = (muon_corrected_p4 + lep.FSR_p4).Pt()
                lep.iso = (lep.pfRelIso04_all*lep.pt-lep.FSR_p4.Pt())/lep.correctedROC_pt
                
            eventSum += lep.p4()
            if lep.iso<0.25 and abs(lep.pdgId)==13 and lep.mediumId and lep.correctedROC_pt>20 and not dimuonSelection :

                if count_mu == 1 and (lep.charge*mu1_charge)<0: # and lep.mediumId 
                    mu2.SetPtEtaPhiM(lep.corrected_pt,lep.eta, lep.phi, 0.105658375)
                    dimuonSelection = True
                if count_mu == 0  :
                    mu1.SetPtEtaPhiM(lep.corrected_pt,lep.eta, lep.phi, 0.105658375)#105,6583745(24) MeV
                    mu1_charge = lep.charge
                    count_mu +=1
        
        #if not dimuonSelection : return False           
        #if max(mu1.Pt(), mu2.Pt())<28 : return False # muons are ordered in lep.pt, not in lep.pt_corrected
        #if min(mu1.Pt(), mu2.Pt())<9  : return False # muons are ordered in lep.pt, not in lep.pt_corrected
    

              
        #dimuon = mu1 + mu2
        dimuonMass = 0
        if dimuonSelection : dimuonMass = (mu1 + mu2).M()
        #if dimuon.M()<70 or dimuon.M()>110 :
        #if dimuonMass<0.1  :
            #return False
                


        muonfilter = lambda j : (j.muonIdx1==-1 or muons[j.muonIdx1].iso>0.25 or not muons[j.muonIdx1].mediumId or muons[j.muonIdx1].correctedROC_pt<20) and (j.muonIdx2==-1 or muons[j.muonIdx2].iso>0.25 or not muons[j.muonIdx2].mediumId or muons[j.muonIdx2].correctedROC_pt<20)
        #electronfilter = lambda j : (j.electronIdx1==-1 or electrons[j.electronIdx1].pfRelIso03_all>0.25 or abs(electrons[j.electronIdx1].dz) > 0.2 or abs(electrons[j.electronIdx1].dxy) > 0.05) and(j.electronIdx2==-1 or electrons[j.electronIdx2].pfRelIso03_all>0.25 or abs(electrons[j.electronIdx2].dz) > 0.2 or abs(electrons[j.electronIdx2].dxy) > 0.05)
        
        
        
        jetFilter1      = lambda j : (j.jetId>0 and (j.pt>50 or j.puId>0  ) and abs(j.eta)<4.7 and (abs(j.eta)<2.5 or j.puId>6 or j.pt>50))
        jetFilter2      = lambda j : (j.jetId>0 and (j.pt>50 or j.puId>0  ) and abs(j.eta)<4.7 )
        jetFilter2_2017 = lambda j : (j.jetId>0 and (j.pt>50 or j.puId17>0) and abs(j.eta)<4.7 )
        jetFilter3_2017 = lambda j : (j.jetId>0 and (j.pt>50 or j.puId17>0) and abs(j.eta)<4.7 ) and (j.puId17 > 6 or abs(j.eta) < 2.65 or abs(j.eta) > 3.1 )
                
                
        jetsNolep = [j for j in jets if muonfilter(j)]

        
        if len(jetsNolep) < 2:
            return False
        
        if self.year!="2017" : 
            for j in jetsNolep : j.puId17 = j.puId
        
        passAtLeastOne=False
        for vn in self.jesVariation:
            for j in jetsNolep:
                j.PT=getattr(j, vn)
            sortedJets=sorted(jetsNolep,key=lambda j : j.PT, reverse=True)
            jetsCriteria1=[j for j in sortedJets if jetFilter1(j)]
            jetsCriteria2=[j for j in sortedJets if jetFilter2(j)]
            jetsCriteria2_2017=[j for j in sortedJets if jetFilter2_2017(j)]
            jetsCriteria3_2017=[j for j in sortedJets if jetFilter3_2017(j)]
            if ( len(jetsCriteria1)>=2 and jetsCriteria1[0].PT > 35 and jetsCriteria1[1].PT > 25 and self.mqq(jetsCriteria1) > 250 ) : passAtLeastOne=True
            if ( len(jetsCriteria2)>=2 and jetsCriteria2[0].PT > 35 and jetsCriteria2[1].PT > 25 and self.mqq(jetsCriteria2) > 250 ) : passAtLeastOne=True
            if ( len(jetsCriteria2_2017)>=2 and jetsCriteria2_2017[0].PT > 35 and jetsCriteria2_2017[1].PT > 25 and self.mqq(jetsCriteria2_2017) > 250 ) : passAtLeastOne=True
            if ( len(jetsCriteria3_2017)>=2 and jetsCriteria3_2017[0].PT > 35 and jetsCriteria3_2017[1].PT > 25 and self.mqq(jetsCriteria3_2017) > 250 ) : passAtLeastOne=True
        
        dijetMass = 0    
 
        if not passAtLeastOne : return False


        #self.out.fillBranch("EventMass",eventSum.M())
        self.out.fillBranch("MuonMass",dimuonMass)
        self.out.fillBranch("qqMass",dijetMass)
        #self.out.fillBranch("jetIdx1",jetIdx1)
        #self.out.fillBranch("jetIdx2",jetIdx2)
        #self.out.fillBranch("jetNumber",jetNumber)
        #self.out.fillBranch("bjetNumber",bjetNumber)
        self.out.fillBranch("muonNumber",muonNumber)
        #self.out.fillBranch("Jet_photonIdx1",Jet_photonIdx1)
        #self.out.fillBranch("Jet_photonIdx2",Jet_photonIdx2)
        #self.out.fillBranch("Jet_VBFselected",VBFselectedJet)
        return True
    
    
    
vbfhmmModule2016 = lambda : vbfhmmProducer(jetSelection= lambda j : j.pt > 15, muSelection= lambda mu : mu.pt > 9, data = False, year="2016") 
vbfhmmModule2017 = lambda : vbfhmmProducer(jetSelection= lambda j : j.pt > 15, muSelection= lambda mu : mu.pt > 9, data = False, year="2017") 
vbfhmmModule2018 = lambda : vbfhmmProducer(jetSelection= lambda j : j.pt > 15, muSelection= lambda mu : mu.pt > 9, data = False, year="2018") 

vbfhmmModuleDATA18 = lambda : vbfhmmProducer(jetSelection= lambda j : j.pt > 15, muSelection= lambda mu : mu.pt > 9, data = True, year="2018") 
vbfhmmModuleDATA   = lambda : vbfhmmProducer(jetSelection= lambda j : j.pt > 15, muSelection= lambda mu : mu.pt > 9, data = True) 




