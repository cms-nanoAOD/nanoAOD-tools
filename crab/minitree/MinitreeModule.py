import ROOT
import os,sys
import math
import random
import gzip
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from Mc_prob_cal_forBweght import *
from foxwol_n_fourmomentumSolver import *
from scaleFactor import *
from correctionlib import *

# Load CorrectionSet


ROOT.gInterpreter.ProcessLine('#include "KinFit.C"')


def mk_safe(fct, *args):
    try:
        return fct(*args)
    except Exception as e:
        if any('Error in function boost::math::erf_inv' in arg for arg in e.args):
            print('WARNING: catching exception and returning -1. Exception arguments: %s' % e.args)
            return -1.
        else:
            raise e

"""def MuonRC_cal_MC(roccor,genparticles,genIdx,Mucharge,Mupt,Mueta,Muphi,MunTrackerLayers):                                           #Rochester correction
        if genIdx >= 0 and genIdx < len(genparticles):
           genMu = genparticles[genIdx]
           MuonPt_corr = Mupt * mk_safe(roccor.kSpreadMC, Mucharge, Mupt, Mueta, Muphi, genparticles[genIdx].pt)
           MuonPt_corr_error = Mupt*mk_safe(roccor.kSpreadMCerror, Mucharge, Mupt, Mueta, Muphi, genparticles[genIdx].pt)
           #print MuonPt_corr," ", MuonPt_corr_error
        else:
           u1 = random.uniform(0.0, 1.0)
           MuonPt_corr=Mupt*mk_safe(roccor.kSmearMC, Mucharge, Mupt, Mueta, Muphi, MunTrackerLayers, u1)
           MuonPt_corr_error = Mupt*mk_safe(roccor.kSmearMCerror, Mucharge, Mupt, Mueta, Muphi, MunTrackerLayers, u1)
        return MuonPt_corr,MuonPt_corr_error

def MuonRC_cal_Data(roccor,Mucharge,Mupt,Mueta,Muphi):
        MuonPt_corr = Mupt * mk_safe(roccor.kScaleDT,Mucharge, Mupt, Mueta, Muphi)
        MuonPt_corr_error = Mupt * mk_safe(roccor.kScaleDTerror,Mucharge, Mupt, Mueta, Muphi)
        return MuonPt_corr,MuonPt_corr_error """

class MinitreeProducer(Module):
    def __init__(self,Total_Njets,BTag_Njets,Isolation,letopn_flv,isMC,dataYear,MCsample=None):
        self.Total_Njets = Total_Njets 
        self.BTag_Njets = BTag_Njets
        self.Isolation = Isolation
        self.letopn_flv = letopn_flv
        self.isMC = isMC
        self.dataYear = dataYear
        self.MCsample = MCsample 
        print("year : ",self.dataYear)
        if(self.isMC):
             PATH = "%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/" % os.environ['CMSSW_BASE']
             JetPUJetID_effi_file={
             'UL2016preVFP'  :  PATH+"jmar_PUID_UL2016preVFP.json.gz",
             'UL2016postVFP' :  PATH+"jmar_PUID_UL2016postVFP.json.gz",
             'UL2017'        :  PATH+"jmar_PUID_UL2017.json.gz",
             'UL2018'        :  PATH+"jmar_PUID_UL2018.json.gz"}
                   
             if JetPUJetID_effi_file[self.dataYear].endswith(".json.gz"):
                with gzip.open(JetPUJetID_effi_file[self.dataYear],'rt') as file:
                        data = file.read().strip()
                        self.evaluator = CorrectionSet.from_string(data)
             else:
                        self.evaluator = CorrectionSet.from_file(JetPUJetID_effi_file[self.dataYear])

        """rc_corrections={
                '2016' : 'RoccoR2016.txt',
                '2017' : 'RoccoR2017.txt',
                '2018' : 'RoccoR2018.txt'}      
        rc_dir = 'roccor.Run2.v3'
        p_postproc = '%s/src/PhysicsTools/NanoAODTools/python/postprocessing' % os.environ['CMSSW_BASE']
        p_roccor = p_postproc + '/data/' + rc_dir
        if "/RoccoR_cc.so" not in ROOT.gSystem.GetLibraries():
            p_helper = '%s/RoccoR.cc' % p_roccor
            print 'Loading C++ helper from ' + p_helper
            ROOT.gROOT.ProcessLine('.L ' + p_helper)
        self._roccor = ROOT.RoccoR(p_roccor + '/' + rc_corrections[self.dataYear])"""

    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        if(self.letopn_flv == 'mu'):
             self.out.branch("MuonPt","F")
             self.out.branch("MuonEta","F")
             self.out.branch("MuonPhi","F")
             self.out.branch("MuonMass","F")
             self.out.branch("MuonE","F")
             self.out.branch("MuonCharge","I")
             self.out.branch("nMuon_sel",  "I")

             self.out.branch("MuonPt_kin", "F")
             self.out.branch("MuonEta_kin", "F")
             self.out.branch("MuonPhi_kin", "F")
             self.out.branch("MuonMass_kin", "F")

             if(self.isMC==True):
                self.out.branch("muSF","F")
                self.out.branch("Muon_SF_Iso",  "F")
                self.out.branch("Muon_SF_IsoUp",  "F")
                self.out.branch("Muon_SF_IsoDown",  "F")
                self.out.branch("Muon_SF_Iso_IDUp",  "F")
                self.out.branch("Muon_SF_Iso_IDDown",  "F")
                self.out.branch("Muon_SF_Iso_TrigUp",  "F")
                self.out.branch("Muon_SF_Iso_TrigDown",  "F")
                self.out.branch("Muon_RelIso", "F")
                self.out.branch("nMuon_sel",  "I")

             """self.out.branch("Muon_corrected_pt", "F")
             self.out.branch("Muon_correctedUp_pt", "F")
             self.out.branch("Muon_correctedDown_pt", "F")
             self.out.branch("mtwMass_RC_corr", "F")""" 
        
        if(self.letopn_flv == 'el'):
             self.out.branch("ElectronPt","F")
             self.out.branch("ElectronEta","F")
             self.out.branch("ElectronSCEta","F")
             self.out.branch("ElectronPhi","F")
             self.out.branch("ElectronMass","F")
             self.out.branch("ElectronE","F")   
             self.out.branch("ElectronCharge","I")
             self.out.branch("Electron_CutbasedID",  "I")
             self.out.branch("nElectron_sel",  "I")

             self.out.branch("ElectronPt_kin", "F")
             self.out.branch("ElectronEta_kin", "F")
             self.out.branch("ElectronPhi_kin", "F")
             self.out.branch("ElectronMass_kin", "F")

             if(self.isMC==True):
                self.out.branch("elSF","F")
                self.out.branch("Electron_SF_Iso",  "F")
                self.out.branch("Electron_SF_Iso_IDUp",  "F")
                self.out.branch("Electron_SF_Iso_IDDown",  "F")
                self.out.branch("Electron_SF_Iso_TrigUp",  "F")
                self.out.branch("Electron_SF_Iso_TrigDown",  "F")
                self.out.branch("Electron_SF_Veto",  "F")
                self.out.branch("Electron_SF_Veto_IDUp",  "F")
                self.out.branch("Electron_SF_Veto_IDDown",  "F")
                self.out.branch("Electron_SF_Veto_TrigUp",  "F")
                self.out.branch("Electron_SF_Veto_TrigDown",  "F")
                self.out.branch("Electron_SF_Reco",        "F")
                self.out.branch("Electron_SF_Veto_Reco", "F")
                self.out.branch("Electron_SF_Iso_RecoUp", "F")
                self.out.branch("Electron_SF_Iso_RecoDown","F")
                self.out.branch("Electron_SF_Veto_RecoUp",   "F")
                self.out.branch("Electron_SF_Veto_RecoDown",  "F")
        self.out.branch("Px_nu","F")
        self.out.branch("Py_nu","F")
        self.out.branch("Pz_nu","F")

        self.out.branch("Pt_nu_kin", "F")
        self.out.branch("Eta_nu_kin", "F")
        self.out.branch("Phi_nu_kin", "F")
        self.out.branch("Mass_nu_kin", "F")
        
        self.out.branch("Px_nu_kin", "F")
        self.out.branch("Py_nu_kin", "F")
        self.out.branch("Pz_nu_kin", "F")

        self.out.branch("mtwMass","F")
        self.out.branch("mtwMass_kin", "F")

        self.out.branch("bJetMass",  "F")
        self.out.branch("bJetPt",  "F")
        self.out.branch("bJetEta",  "F")
        self.out.branch("abs_bJetEta",  "F")
        self.out.branch("bJetPhi",  "F")
        self.out.branch("bJetdeepJet",  "F")
        self.out.branch("nbjet_sel",  "I")
        if(self.isMC==True):
                self.out.branch("bJethadronFlavour",  "F")
                self.out.branch("bJetpartonFlavour",  "F")
                self.out.branch("bJetPUJetID_SF",  "F")
                self.out.branch("bJetPUJetID_SF_up",  "F")
                self.out.branch("bJetPUJetID_SF_down",  "F")
        
        self.out.branch("MinDR_lep_lnbJet",  "F")
        self.out.branch("lJetMass",  "F")
        self.out.branch("lJetPt",  "F")
        self.out.branch("lJetEta",  "F")
        self.out.branch("abs_lJetEta",  "F")
        self.out.branch("lJetPhi",  "F")
        self.out.branch("lJetdeepJet",  "F")
        self.out.branch("nljet_sel",  "I")
        if(self.isMC==True):
                self.out.branch("lJethadronFlavour",  "F")
                self.out.branch("lJetpartonFlavour",  "F")
                self.out.branch("lJetPUJetID_SF",  "F")
                self.out.branch("lJetPUJetID_SF_up",  "F")
                self.out.branch("lJetPUJetID_SF_down",  "F")

        if(self.Total_Njets == 3 and  (self.BTag_Njets == 1 or self.BTag_Njets == 2)):
            self.out.branch("oJetPUJetID_SF",  "F")
            self.out.branch("oJetPUJetID_SF_up",  "F")
            self.out.branch("oJetPUJetID_SF_down",  "F")
            self.out.branch("oJetMass",  "F")
            self.out.branch("oJetPt",  "F")
            self.out.branch("oJetEta",  "F")
            self.out.branch("abs_oJetEta",  "F")
            self.out.branch("oJetPhi",  "F")
            self.out.branch("oJetdeepJet",  "F")
            self.out.branch("nojet_sel",  "I")
            if(self.isMC==True):
                self.out.branch("oJethadronFlavour",  "F")
                self.out.branch("oJetpartonFlavour", "F")
                self.out.branch("oJetPUJetID_SF",  "F")
                self.out.branch("oJetPUJetID_SF_up",  "F")
                self.out.branch("oJetPUJetID_SF_down",  "F")

        self.out.branch("FW1", "F")
        self.out.branch("FW2", "F")
        self.out.branch("FW3", "F")

        self.out.branch("topMass", "F")

        self.out.branch("topPt_kin", "F")
        self.out.branch("topEta_kin", "F")
        self.out.branch("topPhi_kin", "F")
        self.out.branch("topMass_kin", "F")

        self.out.branch("topPt", "F")
        self.out.branch("cosThetaStar", "F")
        self.out.branch("cosThetaStar", "F")
        self.out.branch("mlb", "F")
        self.out.branch("E_lb","F")
        self.out.branch("p_lb","F")
        self.out.branch("theta_lb", "F")
        self.out.branch("jetpTSum","F")
        self.out.branch("hardJetMass", "F")
        self.out.branch("lJetMass", "F")
        self.out.branch("diJetMass","F")
        self.out.branch("dEta_bJet_lJet","F")
        self.out.branch("dEta_top_lJet","F")
        if(self.letopn_flv == 'mu'):
            self.out.branch("dEta_mu_bJet","F")
            self.out.branch("dEta_mu_lJet","F")
            self.out.branch("dPhi_mu_bJet","F")
            self.out.branch("dPhi_mu_met","F")
            self.out.branch("dPhi_mu_lJet","F" )
            self.out.branch("dR_mu_bJet","F" )          
            self.out.branch("dR_mu_lJet","F") 
        
        if(self.letopn_flv == 'el'):
            self.out.branch("dEta_el_bJet","F")
            self.out.branch("dEta_el_lJet","F")
            self.out.branch("dPhi_el_bJet","F")
            self.out.branch("dPhi_el_met","F")
            self.out.branch("dPhi_el_lJet","F" )
            self.out.branch("dR_el_bJet","F" )
            self.out.branch("dR_el_lJet","F")

        self.out.branch("dPhi_bJet_lJet","F")
        self.out.branch("dPhi_top_lJet", "F")
        self.out.branch("dR_bJet_lJet","F") 
        self.out.branch("dR_top_lJet","F") 
        if(self.isMC==True):
            self.out.branch("Xsec_wgt","F")
            self.out.branch("Event_wgt","F")
            self.out.branch("LHEWeightSign","F")
            self.shape_systs = ["Central","lf","hf","cferr1","cferr2","lfstats1","lfstats2","hfstats1","hfstats2","jes"]
            self.B_tag_jes_variation = ["jesAbsoluteStat",'jesAbsoluteMPFBias','jesFragmentation','jesSinglePionECAL','jesSinglePionHCAL','jesTimePtEta','jesRelativeJEREC1','jesRelativeJEREC2','jesRelativeJERHF','jesRelativePtBB','jesRelativePtEC1','jesRelativePtEC2','jesRelativePtHF','jesRelativeBal','jesRelativeSample','jesRelativeFSR','jesRelativeStatEC','jesRelativeStatHF','jesPileUpDataMC','jesPileUpPtRef','jesPileUpPtBB','jesPileUpPtEC1','jesPileUpPtEC2','jesPileUpPtHF',"jesAbsoluteScale", "jesFlavorQCD", "jesRelativeStatFSR"]
            for syst in self.shape_systs:
                if(syst == "Central"):self.out.branch("bWeight","F")
                else: self.out.branch("bWeight_"+syst,  "F",lenVar="2")
            self.out.branch("bWeight_jes_variation_up",  "F",lenVar=str(len(self.B_tag_jes_variation)))
            self.out.branch("bWeight_jes_variation_down",  "F",lenVar=str(len(self.B_tag_jes_variation)))
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        if(self.isMC):
            TotalLumi={
                '2016' : 35855,
                '2017' : 41529,
                '2018' : 41520,
                'UL2016preVFP' :  19521,
                'UL2016postVFP' : 16812,
                'UL2017' : 41529,
                'UL2018' : 59222}
        if(self.isMC):
                from Xsec_Nevent import MCsample_Nevent_Xsec
                x_sec = float(MCsample_Nevent_Xsec[self.dataYear][self.MCsample][1])
                NEvents = float(MCsample_Nevent_Xsec[self.dataYear][self.MCsample][0])
                
                Xsec_wgt = (x_sec*TotalLumi[self.dataYear])/NEvents
        #print Xsec_wgt
        muons = Collection(event, "Muon")
        electrons = Collection(event, "Electron")
        lepton4v = ROOT.TLorentzVector()
        lepton4v_kin = ROOT.TLorentzVector()
        Nu4v_kin = ROOT.TLorentzVector()
        w4v_kin = ROOT.TLorentzVector()
        leptonSF = 0
        leptonCharge = 0
        #print self.letopn_flv




        ######---------------------  Scale factor calculation begin  -------------------------################



        #print "self.isMC = ",self.isMC
        pt_Thes_mu={
                '2016' : 26,
                '2017' : 30,
                '2018' : None,
                'UL2016preVFP' : 26,
                'UL2016postVFP' : 26,
                'UL2017' : 30,
                'UL2018' : 26} #need to check the trigger
        pt_Thes_el={
                '2016' : 35,
                '2017' : 37,
                '2018' : None,
                'UL2016preVFP' : 35,
                'UL2016postVFP' : 35,
                'UL2017' : 35,
                'UL2018' : 35} #need to check the trigger
        
        if(self.isMC):
            Ele_EtaSC,Electron_SF_Iso,Electron_SF_Iso_IDUp,Electron_SF_Iso_IDDown,Electron_SF_Iso_TrigUp,Electron_SF_Iso_TrigDown,Electron_SF_Veto,Electron_SF_Veto_IDUp,Electron_SF_Veto_IDDown,Electron_SF_Veto_TrigUp,Electron_SF_Veto_TrigDown,Electron_CutbasedID=(-999 for i in range(12))
            Muon_SF_Iso,Muon_SF_IsoUp,Muon_SF_IsoDown,Muon_SF_Iso_IDUp,Muon_SF_Iso_IDDown,Muon_SF_Iso_TrigUp,Muon_SF_Iso_TrigDown,Muon_SF_Veto,Muon_SF_Veto_IDUp,Muon_SF_Veto_IDDown,Muon_SF_Veto_TrigUp,Muon_SF_Veto_TrigDown,Muon_RelIso=(-999 for i in range(13))    
            if(self.letopn_flv=="el"):
                 count=0
                 #Jetpt = getattr(event,'Jet_pt')
                 #jetpt = Jetpt[0]

                 nElectron_sel = -1
                 for lep in electrons :
                    nElectron_sel = nElectron_sel+1
                    if(  (self.Isolation==True) and lep.pt>pt_Thes_el[self.dataYear] and abs(lep.eta)<2.1 and lep.cutBased==4 and (abs(lep.EtaSC)<1.4442 or abs(lep.EtaSC)>1.5660) and ((abs(lep.EtaSC)<=1.479 and abs(lep.dz)< 0.10 and abs(lep.dxy)< 0.05) or (abs(lep.EtaSC)> 1.479 and abs(lep.dz)< 0.20 and abs(lep.dxy)< 0.10)) ):
                        
                        Electron_SF_Iso, Electron_SF_Reco = create_elSF(self.dataYear,lep.pt,lep.EtaSC,"Tight","noSyst")
                        Electron_SF_Iso_IDUp, _ = create_elSF(self.dataYear,lep.pt,lep.EtaSC,"Tight","IDUp")
                        Electron_SF_Iso_IDDown, _ = create_elSF(self.dataYear,lep.pt,lep.EtaSC,"Tight","IDDown")
                        Electron_SF_Iso_TrigUp, _ = create_elSF(self.dataYear,lep.pt,lep.EtaSC,"Tight","TrigUp")
                        Electron_SF_Iso_TrigDown, _ = create_elSF(self.dataYear,lep.pt,lep.EtaSC,"Tight","TrigDown")
                        Electron_SF_Iso_RecoUp,_  = create_elSF(self.dataYear,lep.pt,lep.EtaSC,"Tight","RecoUp")
                        Electron_SF_Iso_RecoDown, _  = create_elSF(self.dataYear,lep.pt,lep.EtaSC,"Tight","RecoDown")


                        lepton4v=lep.p4()
                        leptonCharge = lep.charge
                        leptonSF = Electron_SF_Iso
                        ElectronSCEta = lep.EtaSC
                        Electron_CutbasedID = lep.cutBased


                        #print 'elSF_Iso=',Electron_SF_Iso
                        self.out.fillBranch("nElectron_sel",nElectron_sel)
                        self.out.fillBranch("Electron_CutbasedID",Electron_CutbasedID)
                        self.out.fillBranch("Electron_SF_Iso", Electron_SF_Iso)
                        self.out.fillBranch("Electron_SF_Iso_IDUp",Electron_SF_Iso_IDUp)
                        self.out.fillBranch("Electron_SF_Iso_IDDown",Electron_SF_Iso_IDDown)
                        self.out.fillBranch("Electron_SF_Iso_TrigUp",Electron_SF_Iso_TrigUp)
                        self.out.fillBranch("Electron_SF_Iso_TrigDown",Electron_SF_Iso_TrigDown)
                        self.out.fillBranch("Electron_SF_Reco",         Electron_SF_Reco)
                        self.out.fillBranch("Electron_SF_Iso_RecoUp",  Electron_SF_Iso_RecoUp)
                        self.out.fillBranch("Electron_SF_Iso_RecoDown",Electron_SF_Iso_RecoDown)


                    elif( (self.Isolation==False) and lep.pt>pt_Thes_el[self.dataYear] and abs(lep.eta)<2.1 and lep.cutBased!=4 and lep.cutBased>=1 and (abs(lep.EtaSC)<1.4442 or abs(lep.EtaSC)>1.5660) and ((abs(lep.EtaSC)<=1.479 and abs(lep.dz)< 0.10 and abs(lep.dxy)< 0.05) or (abs(lep.EtaSC)> 1.479 and abs(lep.dz)< 0.20 and abs(lep.dxy)< 0.10)) ):

                        Electron_SF_Veto, Electron_SF_Veto_Reco = create_elSF(self.dataYear,lep.pt,lep.EtaSC,"Veto","noSyst")
                        Electron_SF_Veto_IDUp, _ = create_elSF(self.dataYear,lep.pt,lep.EtaSC,"Veto","IDUp")
                        Electron_SF_Veto_IDDown, _ = create_elSF(self.dataYear,lep.pt,lep.EtaSC,"Veto","IDDown")
                        Electron_SF_Veto_TrigUp, _ = create_elSF(self.dataYear,lep.pt,lep.EtaSC,"Veto","TrigUp")
                        Electron_SF_Veto_TrigDown, _ = create_elSF(self.dataYear,lep.pt,lep.EtaSC,"Veto","TrigDown")
                        Electron_SF_Veto_RecoUp, _  = create_elSF(self.dataYear,lep.pt,lep.EtaSC,"Veto","RecoUp")
                        Electron_SF_Veto_RecoDown,_ = create_elSF(self.dataYear,lep.pt,lep.EtaSC,"Veto","RecoDown")

        
                        lepton4v=lep.p4()
                        leptonCharge = lep.charge
                        leptonSF = Electron_SF_Veto
                        ElectronSCEta = lep.EtaSC
                        Electron_CutbasedID = lep.cutBased

                        #print 'elSF_Iso=',Electron_SF_Veto
                        self.out.fillBranch("nElectron_sel",nElectron_sel)
                        self.out.fillBranch("Electron_CutbasedID",Electron_CutbasedID)
                        self.out.fillBranch("Electron_SF_Veto", Electron_SF_Veto)
                        self.out.fillBranch("Electron_SF_Veto_IDUp",Electron_SF_Veto_IDUp)
                        self.out.fillBranch("Electron_SF_Veto_IDDown",Electron_SF_Veto_IDDown)
                        self.out.fillBranch("Electron_SF_Veto_TrigUp",Electron_SF_Veto_TrigUp)
                        self.out.fillBranch("Electron_SF_Veto_TrigDown",Electron_SF_Veto_TrigDown)
                        self.out.fillBranch("Electron_SF_Veto_Reco", Electron_SF_Veto_Reco)
                        self.out.fillBranch("Electron_SF_Veto_RecoUp",   Electron_SF_Veto_RecoUp)
                        self.out.fillBranch("Electron_SF_Veto_RecoDown",  Electron_SF_Veto_RecoDown)

            if(self.letopn_flv=="mu"):
                 nMuon_sel = -1
                 for lep in muons :
                    nMuon_sel = nMuon_sel+1
                    if(   ((self.Isolation==True)  and lep.pt>pt_Thes_mu[self.dataYear] and abs(lep.eta)<2.4 and lep.pfRelIso04_all<0.06 and lep.tightId==1)   or
                          ((self.Isolation==False) and lep.pt>pt_Thes_mu[self.dataYear] and abs(lep.eta)<2.4 and lep.pfRelIso04_all>0.2  and lep.tightId==1)    ):

                        Muon_RelIso = lep.pfRelIso04_all

                        Muon_SF_Iso = create_muSF(self.dataYear,lep.pt,lep.eta,lep.pfRelIso04_all,TotalLumi[self.dataYear],"noSyst")
                        Muon_SF_IsoUp = create_muSF(self.dataYear,lep.pt,lep.eta,lep.pfRelIso04_all,TotalLumi[self.dataYear],"IsoUp")
                        Muon_SF_IsoDown = create_muSF(self.dataYear,lep.pt,lep.eta,lep.pfRelIso04_all,TotalLumi[self.dataYear],"IsoDown")
                        Muon_SF_Iso_IDUp = create_muSF(self.dataYear,lep.pt,lep.eta,lep.pfRelIso04_all,TotalLumi[self.dataYear],"IDUp") 
                        Muon_SF_Iso_IDDown = create_muSF(self.dataYear,lep.pt,lep.eta,lep.pfRelIso04_all,TotalLumi[self.dataYear],"IDDown")
                        Muon_SF_Iso_TrigUp = create_muSF(self.dataYear,lep.pt,lep.eta,lep.pfRelIso04_all,TotalLumi[self.dataYear],"TrigUp")
                        Muon_SF_Iso_TrigDown = create_muSF(self.dataYear,lep.pt,lep.eta,lep.pfRelIso04_all,TotalLumi[self.dataYear],"TrigDown")

                        lepton4v=lep.p4()
                        leptonCharge = lep.charge
                        leptonSF = Muon_SF_Iso
                        #print 'muSF_Iso = ',Muon_SF_Iso

                        self.out.fillBranch("nMuon_sel",nMuon_sel)
                        self.out.fillBranch("Muon_RelIso", Muon_RelIso)
                        self.out.fillBranch("Muon_SF_Iso", Muon_SF_Iso)
                        self.out.fillBranch("Muon_SF_IsoUp", Muon_SF_IsoUp)
                        self.out.fillBranch("Muon_SF_IsoDown", Muon_SF_IsoDown)
                        self.out.fillBranch("Muon_SF_Iso_IDUp",Muon_SF_Iso_IDUp)
                        self.out.fillBranch("Muon_SF_Iso_IDDown",Muon_SF_Iso_IDDown)
                        self.out.fillBranch("Muon_SF_Iso_TrigUp",Muon_SF_Iso_TrigUp)
                        self.out.fillBranch("Muon_SF_Iso_TrigDown",Muon_SF_Iso_TrigDown)
                 
            #print "----------------------------------------------------------------->"

            ######---------------------  Scale factor calculation begin  -------------------------################











        ########## -----------------------   isolated lapton selection for data --------------------###################

        if(self.letopn_flv=="mu" and self.isMC==False):
            for lep in muons:
                #print "muonpt = %s muoneta = %s muoniso = %s muonid = %s iso = %s"%(lep.pt,lep.eta,lep.pfRelIso04_all,lep.tightId,self.Isolation)
                if((self.Isolation==True) and lep.pt>pt_Thes_mu[self.dataYear] and abs(lep.eta)<2.4 and lep.pfRelIso04_all<0.06 and lep.tightId==1):
                    lepton4v=lep.p4()
                    leptonCharge = lep.charge
                    #print "musf = ",leptonSF
                    #print "mu phi = ",lep.phi
                elif((self.Isolation==False) and lep.pt>pt_Thes_mu[self.dataYear] and abs(lep.eta)<2.4 and lep.pfRelIso04_all>0.2 and lep.tightId==1):
                    #print "criteria passed"
                    lepton4v=lep.p4()
                    leptonCharge = lep.charge

        if(self.letopn_flv=="el" and self.isMC==False):
            for lep in electrons:
                if((self.Isolation==True) and lep.pt>pt_Thes_el[self.dataYear] and abs(lep.eta)<2.1 and lep.cutBased==4 and (abs(lep.EtaSC)<1.4442 or abs(lep.EtaSC)>1.5660) and ((abs(lep.EtaSC)<=1.479 and abs(lep.dz)< 0.10 and abs(lep.dxy)< 0.05) or (abs(lep.EtaSC)> 1.479 and abs(lep.dz)< 0.20 and abs(lep.dxy)< 0.10))):
                    lepton4v=lep.p4()
                    ElectronSCEta = lep.EtaSC
                    leptonCharge = lep.charge
                    Electron_CutbasedID = lep.cutBased
                    self.out.fillBranch("Electron_CutbasedID",Electron_CutbasedID)

                if((self.Isolation==False) and lep.pt>pt_Thes_el[self.dataYear] and abs(lep.eta)<2.1 and lep.cutBased!=4 and lep.cutBased>=1 and (abs(lep.EtaSC)<1.4442 or abs(lep.EtaSC)>1.5660) and ((abs(lep.EtaSC)<=1.479 and abs(lep.dz)< 0.10 and abs(lep.dxy)< 0.05) or (abs(lep.EtaSC)> 1.479 and abs(lep.dz)< 0.20 and abs(lep.dxy)< 0.10))):
                    lepton4v=lep.p4()   
                    ElectronSCEta = lep.EtaSC
                    leptonCharge = lep.charge
                    Electron_CutbasedID = lep.cutBased
                    self.out.fillBranch("Electron_CutbasedID",Electron_CutbasedID)


        ######### ------------------------- lepton selction done -------------------------------  ####################







        ####### -------------------------  nu_z and mtw calcualtion ---------------------------  ###############
                
        #print "muonpx = %s muonpy = %s muonpz = %s muonE = %s"%(lepton4v.Px(),lepton4v.Py(),lepton4v.Pz(),lepton4v.E())
        leptonPt = lepton4v.Pt()
        leptonEta = lepton4v.Eta()
        leptonPhi = lepton4v.Phi()
        #print "leptonPhi = ",leptonPhi
        leptonMass = lepton4v.M()
        leptonE = lepton4v.E()
        met = getattr(event,'MET_pt')
        metphi =getattr(event,'MET_phi')
        #print "math.sqrt() = ",pow((leptonPt+met),2)-pow((leptonPt*math.cos(leptonPhi)+met*math.cos(metphi)),2)-pow((leptonPt*math.sin(leptonPhi)+met*math.sin(metphi)),2)
        #print "math.cos(leptonPhi) = ",math.cos(leptonPhi)," ",leptonPhi
        Px_nu = met*math.cos(metphi)
        #print "math.sin(leptonPhi) = ",math.sin(leptonPhi)," ",leptonPhi
        Py_nu = met*math.sin(metphi)
        mtwMass = math.sqrt(abs(pow((leptonPt+met),2)-pow((leptonPt*math.cos(leptonPhi)+met*math.cos(metphi)),2)-pow((leptonPt*math.sin(leptonPhi)+met*math.sin(metphi)),2)));

        neutrino4v = ROOT.TLorentzVector()
        neutrino4v = solveNu4Momentum(lepton4v,met*math.cos(metphi),met*math.sin(metphi))
        Pz_nu = neutrino4v.Pz() 


        ############ -----------------  nu_z and mtw calcualtion done ----------------------################


        #############-----------------   kinfit --------------------------#############
        kinfit_vec_comp_XYZE = ROOT.PerfomFit(lepton4v,neutrino4v)


        lepton4v_kin.SetPxPyPzE(kinfit_vec_comp_XYZE.at(0),kinfit_vec_comp_XYZE.at(1),kinfit_vec_comp_XYZE.at(2),kinfit_vec_comp_XYZE.at(3))
        Nu4v_kin.SetPxPyPzE(kinfit_vec_comp_XYZE.at(4),kinfit_vec_comp_XYZE.at(5),kinfit_vec_comp_XYZE.at(6),kinfit_vec_comp_XYZE.at(7))

        if(self.letopn_flv=='mu'):
                self.out.fillBranch("MuonPt_kin", lepton4v_kin.Pt())
                self.out.fillBranch("MuonEta_kin", lepton4v_kin.Eta())
                self.out.fillBranch("MuonPhi_kin", lepton4v_kin.Phi())
                self.out.fillBranch("MuonMass_kin", lepton4v_kin.M())
        elif(self.letopn_flv=='el'):
                 self.out.fillBranch("ElectronPt_kin", lepton4v_kin.Pt())
                 self.out.fillBranch("ElectronEta_kin", lepton4v_kin.Eta())
                 self.out.fillBranch("ElectronPhi_kin", lepton4v_kin.Phi())
                 self.out.fillBranch("ElectronMass_kin", lepton4v_kin.M())

        self.out.fillBranch("Pt_nu_kin", Nu4v_kin.Pt())
        self.out.fillBranch("Eta_nu_kin", Nu4v_kin.Eta())
        self.out.fillBranch("Phi_nu_kin", Nu4v_kin.Phi())
        self.out.fillBranch("Mass_nu_kin", Nu4v_kin.M())

        self.out.fillBranch("Px_nu_kin", Nu4v_kin.Px())
        self.out.fillBranch("Py_nu_kin", Nu4v_kin.Py())
        self.out.fillBranch("Pz_nu_kin", Nu4v_kin.Pz()) 
                
        mtwMass_kin = math.sqrt(abs(pow((lepton4v_kin.Pt()+Nu4v_kin.Pt()),2)-pow((lepton4v_kin.Pt()*math.cos(lepton4v_kin.Phi())+Nu4v_kin.Pt()*math.cos(Nu4v_kin.Phi())),2)-pow((lepton4v_kin.Pt()*math.sin(lepton4v_kin.Phi())+Nu4v_kin.Pt()*math.sin( Nu4v_kin.Phi())),2)))

        w4v_kin = lepton4v_kin + Nu4v_kin       
        ##########--------------------------kifit done ------------------- ##################



        ###########  -------------------  jet slection ---------------------- ##########################


        
        jets = Collection(event, "Jet")

        #for jet in jet_id:
            #print jet.pt
        bJet4v = ROOT.TLorentzVector()
        lJet4v = ROOT.TLorentzVector()
        oJet4v = ROOT.TLorentzVector(0.,0.,0.,0.)
        top4v = ROOT.TLorentzVector()
        jet_id = []
        btagjet_id = [] 
        njet4v = ROOT.TLorentzVector()
        #drs = getattr(event,"dR_Ljet_Isomu") 
        #for i in (0,len(drs)):
           #print "dr = ",drs[i]

        puId_loose_bit = 1 if self.dataYear.startswith('UL2016') else 4
        for jet in filter(lambda j:(j.pt>40 and abs(j.eta)<4.7 and j.jetVetoed==0 and j.jetId!=0 and (j.pt>=50 or (j.puId & puId_loose_bit)!=0)), jets):
            njet4v.SetPtEtaPhiM(jet.pt,jet.eta,jet.phi,jet.mass)
            if(lepton4v.DeltaR(njet4v)>0.4): 
                jet_id.append(jet)
                #print lepton4v.DeltaR(njet4n)
        #print "jet_id = ",jet_id
        Tight_b_tag_crite={
                'UL2016preVFP' : 0.6502, # https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL16postVFP
                'UL2016postVFP' : 0.6377, # https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL16postVFP
                'UL2017' : 0.7476, # https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL17
                'UL2018' : 0.7100} # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation106XUL18
        Lose_b_tag_crite={
                'UL2016preVFP' : 0.0480,
                'UL2016postVFP' :0.0480,
                'UL2017' : 0.0532,
                'UL2018' : 0.0490}
        Tight_b_tag_eta_cut = {
            "UL2016preVFP": 2.4,
            "UL2016postVFP": 2.4,
            "UL2017": 2.5,
            "UL2018": 2.5,
        }
        for jet in jet_id:
            njet4v.SetPtEtaPhiM(jet.pt,jet.eta,jet.phi,jet.mass)
            #print lepton4v.DeltaR(njet4v)
            #print jet.btagDeepFlavB," ",jet.eta
        #print getattr(event,'event');
        
        for jet in filter(lambda j:(j.btagDeepFlavB>Tight_b_tag_crite[self.dataYear] and abs(j.eta)<Tight_b_tag_eta_cut[self.dataYear]), jet_id):
            btagjet_id.append(jet) 
        #print("btagJet_id = ", btagjet_id)
        #if(len(btagjet_id)):   return True
        if(self.Total_Njets == 2 and  self.BTag_Njets == 1 and len(btagjet_id)==0):
                for jet in filter(lambda j:(j.btagDeepFlavB>Lose_b_tag_crite[self.dataYear] and abs(j.eta)<Tight_b_tag_eta_cut[self.dataYear]), jet_id):
                        btagjet_id.append(jet)
                #print len(btagjet_id)
        #print len(jet_id)," ",len(btagjet_id)
        #print "--------------------------------------2 J 1 T-----------------------------"
        if( self.Total_Njets == 2 and  self.BTag_Njets == 1):
            #print "--------------------------------------2 J 1 T-----------------------------"
            for jet in jet_id:
                if(jet==btagjet_id[0]):
                     [bJetMass,bJetPt,bJetEta,abs_bJetEta,bJetPhi,bJetdeepJet,bJet4v]=CollectJetInfo(jet)
                     if(self.isMC==True):
                           bJethadronFlavour=jet.hadronFlavour    
                           bJetpartonFlavour=jet.partonFlavour
                     #print "Dr bjet inside 2J1T con = ",lepton4v.DeltaR(bJet4v)
                else:
                     [lJetMass,lJetPt,lJetEta,abs_lJetEta,lJetPhi,lJetdeepJet,lJet4v]=CollectJetInfo(jet)       
                     if(self.isMC==True):
                         lJethadronFlavour=jet.hadronFlavour
                         lJetpartonFlavour=jet.partonFlavour
            del_theta = math.cos(lJet4v.Angle(bJet4v.Vect()))
            Foxwol_h1 = wolformvalue2J(poly1(del_theta),bJetPt,lJetPt)
            Foxwol_h2 = wolformvalue2J(poly2(del_theta),bJetPt,lJetPt)       
            Foxwol_h3 = wolformvalue2J(poly3(del_theta),bJetPt,lJetPt)
            oJetPt = 0.   #This is required when we calculate "hardJetMass" 
                     #          //cout<<"costheta="<<cos(lJet4v->Angle(bJet4v->Vect()))<<";poly1="<<poly1(cos(lJet4v->Angle(bJet4v->Vect())))<<";bJetPt="<<bJetPt<<";ljetPt="<<lJetPt<<";Foxwol_h1="<<Foxwol_h1<<endl;  
        elif(self.Total_Njets == 2 and  self.BTag_Njets == 0):
            #print "--------------------------------------2 J 0 T-----------------------------"
            for jet in jet_id:
                if(jet==jet_id[0]): 
                    deepjet_score0 =jet.btagDeepFlavB
                    eta0 = abs(jet.eta)
                if(jet==jet_id[1]): 
                    deepjet_score1 =jet.btagDeepFlavB
                    eta1 = abs(jet.eta)
            #print  "score0 = %s; score1 = %s" %( deepjet_score0,deepjet_score1)
            if(deepjet_score0<-1.0 and deepjet_score1<-1.0):
                if(eta0<eta1):
                    for jet in jet_id:
                        if(jet==jet_id[0]):
                             btagjet_id.append(jet)     
                             [bJetMass,bJetPt,bJetEta,abs_bJetEta,bJetPhi,bJetdeepJet,bJet4v]=CollectJetInfo(jet)
                             if(self.isMC==True):
                                 bJethadronFlavour=jet.hadronFlavour
                                 bJetpartonFlavour=jet.partonFlavour
                        else:
                             [lJetMass,lJetPt,lJetEta,abs_lJetEta,lJetPhi,lJetdeepJet,lJet4v]=CollectJetInfo(jet)
                             if(self.isMC==True):
                                 lJethadronFlavour=jet.hadronFlavour
                                 lJetpartonFlavour=jet.partonFlavour
                else:
                    for jet in jet_id:
                        if(jet==jet_id[1]):
                             btagjet_id.append(jet)
                             [bJetMass,bJetPt,bJetEta,abs_bJetEta,bJetPhi,bJetdeepJet,bJet4v]=CollectJetInfo(jet)
                             if(self.isMC==True):
                                 bJethadronFlavour=jet.hadronFlavour
                                 bJetpartonFlavour=jet.partonFlavour
                        else:
                             [lJetMass,lJetPt,lJetEta,abs_lJetEta,lJetPhi,lJetdeepJet,lJet4v]=CollectJetInfo(jet)       
                             if(self.isMC==True):
                                 lJethadronFlavour=jet.hadronFlavour
                                 lJetpartonFlavour=jet.partonFlavour
            else:
                #print "both score are not less than -1"
                if(deepjet_score0 > deepjet_score1):
                    #print "jet0 score > jet1 score "
                    for jet in jet_id:
                        if(jet==jet_id[0]):
                             btagjet_id.append(jet)
                             [bJetMass,bJetPt,bJetEta,abs_bJetEta,bJetPhi,bJetdeepJet,bJet4v]=CollectJetInfo(jet)
                             if(self.isMC==True):
                                  bJethadronFlavour=jet.hadronFlavour
                                  bJetpartonFlavour=jet.partonFlavour
                             #print "bJetMass = %s; bJetPt = %s; bJetEta = %s; abs_bJetEta = %s; bJetPhi = %s; bJetdeepJet = %s; bJethadronFlavour = %s; bJet4vM = %s; " %(bJetMass,bJetPt,bJetEta,abs_bJetEta,bJetPhi,bJetdeepJet,bJethadronFlavour,bJet4v.M())
                        else:
                             [lJetMass,lJetPt,lJetEta,abs_lJetEta,lJetPhi,lJetdeepJet,lJet4v]=CollectJetInfo(jet)       
                             if(self.isMC==True):
                                 lJethadronFlavour=jet.hadronFlavour
                                 lJetpartonFlavour=jet.partonFlavour
                else:
                    for jet in jet_id:
                        if(jet==jet_id[1]):
                             btagjet_id.append(jet)
                             [bJetMass,bJetPt,bJetEta,abs_bJetEta,bJetPhi,bJetdeepJet,bJet4v]=CollectJetInfo(jet)
                             if(self.isMC==True):
                                   bJethadronFlavour=jet.hadronFlavour
                                   bJetpartonFlavour=jet.partonFlavour
                        else:
                             [lJetMass,lJetPt,lJetEta,abs_lJetEta,lJetPhi,lJetdeepJet,lJet4v]=CollectJetInfo(jet)
                             if(self.isMC==True):
                                 lJethadronFlavour=jet.hadronFlavour
                                 lJetpartonFlavour=jet.partonFlavour
            del_theta=math.cos(lJet4v.Angle(bJet4v.Vect()))
            Foxwol_h1=wolformvalue2J(poly1(del_theta),bJetPt,lJetPt)
            Foxwol_h2=wolformvalue2J(poly2(del_theta),bJetPt,lJetPt)
            Foxwol_h3=wolformvalue2J(poly3(del_theta),bJetPt,lJetPt)
            oJetPt = 0.   #This is required when we calculate "hardJetMass" 
        elif(self.Total_Njets == 3 and  self.BTag_Njets == 1):
            #print "--------------------------------------3 J 1 T-----------------------------"
            jet_compaired=[]
            for jet in jet_id:
                #print "jet Pt = ", jet.pt
                if(jet==btagjet_id[0]):
                     #print "btagjet_id = ",jet
                     [bJetMass,bJetPt,bJetEta,abs_bJetEta,bJetPhi,bJetdeepJet,bJet4v]=CollectJetInfo(jet)
                     if(self.isMC==True):
                           bJethadronFlavour=jet.hadronFlavour
                           bJetpartonFlavour=jet.partonFlavour
                else:
                     jet_compaired.append(jet)
            #print "comaired jet ids = ",jet_compaired
            for jet in jet_compaired:
                if(jet==jet_compaired[0]):
                    eta0 = jet.eta
                if(jet==jet_compaired[1]):
                    eta1 = jet.eta
            #print "eta0 = %s; eta1 = %s" %(eta0,eta1)
            for jet in jet_compaired:
                if(abs(eta0)>abs(eta1)):
                    if(jet==jet_compaired[0]):
                        [lJetMass,lJetPt,lJetEta,abs_lJetEta,lJetPhi,lJetdeepJet,lJet4v]=CollectJetInfo(jet)
                        if(self.isMC==True):
                            lJethadronFlavour=jet.hadronFlavour
                            lJetpartonFlavour=jet.partonFlavour
                    else:       
                        [oJetMass,oJetPt,oJetEta,abs_oJetEta,oJetPhi,oJetdeepJet,oJet4v]=CollectJetInfo(jet)
                        if(self.isMC==True):
                            oJethadronFlavour=jet.hadronFlavour
                            oJetpartonFlavour=jet.partonFlavour
                else:
                    if(jet==jet_compaired[1]):
                        [lJetMass,lJetPt,lJetEta,abs_lJetEta,lJetPhi,lJetdeepJet,lJet4v]=CollectJetInfo(jet)
                        if(self.isMC==True):
                            lJethadronFlavour=jet.hadronFlavour
                            lJetpartonFlavour=jet.partonFlavour
                    else:                       
                        [oJetMass,oJetPt,oJetEta,abs_oJetEta,oJetPhi,oJetdeepJet,oJet4v]=CollectJetInfo(jet)
                        if(self.isMC==True):
                            oJethadronFlavour=jet.hadronFlavour
                            oJetpartonFlavour=jet.partonFlavour
            [Foxwol_h1,Foxwol_h2,Foxwol_h3]=wolformvalue3J(bJet4v,lJet4v,oJet4v)
        elif(self.Total_Njets == 3 and  self.BTag_Njets == 2):
            #print "--------------------------------------3 J 2 T-----------------------------"
            dummyjet_id=[]
            for jet in jet_id:
                if(jet!=btagjet_id[0] and jet!=btagjet_id[1]):
                    [lJetMass,lJetPt,lJetEta,abs_lJetEta,lJetPhi,lJetdeepJet,lJet4v]=CollectJetInfo(jet)        
                    if(self.isMC==True):
                        lJethadronFlavour=jet.hadronFlavour
                        lJetpartonFlavour=jet.partonFlavour
            dummybjet0 = ROOT.TLorentzVector()
            dummybjet1 = ROOT.TLorentzVector()
            dummytop0 = ROOT.TLorentzVector()
            dummytop1 = ROOT.TLorentzVector()
            for jet in btagjet_id:
                if(jet==btagjet_id[0]): 
                    dummybjet0 = jet.p4()
                if(jet==btagjet_id[1]):
                    dummybjet1 = jet.p4()
            dummytop0= lepton4v+dummybjet0+neutrino4v
            topmass_bjet0=dummytop0.M()
            dummytop1= lepton4v+dummybjet1+neutrino4v
            topmass_bjet1=dummytop1.M()
            for jet in btagjet_id:
                if(abs(topmass_bjet0 - 172.5)<abs(topmass_bjet1 - 172.5)):
                    if(jet==btagjet_id[0]):
                        dummyjet_id.append(jet)
                        [bJetMass,bJetPt,bJetEta,abs_bJetEta,bJetPhi,bJetdeepJet,bJet4v]=CollectJetInfo(jet)
                        if(self.isMC==True):
                            bJethadronFlavour=jet.hadronFlavour
                            bJetpartonFlavour=jet.partonFlavour
                    else:
                        [oJetMass,oJetPt,oJetEta,abs_oJetEta,oJetPhi,oJetdeepJet,oJet4v]=CollectJetInfo(jet)
                        if(self.isMC==True):
                            oJethadronFlavour=jet.hadronFlavour
                            oJetpartonFlavour=jet.partonFlavour
                else:
                    if(jet==btagjet_id[1]):
                        dummyjet_id.append(jet)
                        [bJetMass,bJetPt,bJetEta,abs_bJetEta,bJetPhi,bJetdeepJet,bJet4v]=CollectJetInfo(jet)
                        if(self.isMC==True):
                            bJethadronFlavour=jet.hadronFlavour
                            bJetpartonFlavour=jet.partonFlavour
                    else:
                        [oJetMass,oJetPt,oJetEta,abs_oJetEta,oJetPhi,oJetdeepJet,oJet4v]=CollectJetInfo(jet)
                        if(self.isMC==True):
                            oJethadronFlavour=jet.hadronFlavour
                            oJetpartonFlavour=jet.partonFlavour
            [Foxwol_h1,Foxwol_h2,Foxwol_h3]=wolformvalue3J(bJet4v,lJet4v,oJet4v)

        #if(self.Total_Njets == 3 and  self.BTag_Njets == 2): 
            #btagjet_id.clear()
            #btagjet_id = dummyjet_id
        
        if(self.isMC==True):
            if(lJetPt<50):
                lJetPUJetID_SF = self.evaluator["PUJetID_eff"].evaluate(abs(lJetEta), lJetPt, "nom","L")
                lJetPUJetID_SF_up = self.evaluator["PUJetID_eff"].evaluate(abs(lJetEta), lJetPt, "up","L")
                lJetPUJetID_SF_down = self.evaluator["PUJetID_eff"].evaluate(abs(lJetEta), lJetPt, "down","L")
                #print "lJetPUJetID_SF : ",lJetPUJetID_SF_down," : ",lJetPUJetID_SF," : ",lJetPUJetID_SF_up," [ ",abs(lJetEta)," ",lJetPt," ]"
            else:
                lJetPUJetID_SF,lJetPUJetID_SF_up,lJetPUJetID_SF_down = 1.0,1.0,1.0
            if(bJetPt<50):
                bJetPUJetID_SF = self.evaluator["PUJetID_eff"].evaluate(abs(bJetEta), bJetPt, "nom","L")
                bJetPUJetID_SF_up = self.evaluator["PUJetID_eff"].evaluate(abs(bJetEta), bJetPt, "up","L")
                bJetPUJetID_SF_down = self.evaluator["PUJetID_eff"].evaluate(abs(bJetEta), bJetPt, "down","L")
                #print "bJetPUJetID_SF : ",bJetPUJetID_SF_down," : ",bJetPUJetID_SF," : ",bJetPUJetID_SF_up," [ ",abs(bJetEta)," ",bJetPt," ]"
            else:
                bJetPUJetID_SF,bJetPUJetID_SF_up,bJetPUJetID_SF_down = 1,1,1
                
            if(self.Total_Njets == 3):
                if(oJetPt<50): 
                        oJetPUJetID_SF = self.evaluator["PUJetID_eff"].evaluate(abs(oJetEta), oJetPt, "nom","L")
                        oJetPUJetID_SF_up = self.evaluator["PUJetID_eff"].evaluate(abs(oJetEta), oJetPt, "up","L")
                        oJetPUJetID_SF_down = self.evaluator["PUJetID_eff"].evaluate(abs(oJetEta), oJetPt, "down","L")
                        #print "ojetPUJetID_SF : ",oJetPUJetID_SF_down," : ",oJetPUJetID_SF," : ",oJetPUJetID_SF_up," [ ",abs(oJetEta)," ",oJetPt," ]"
                else:
                        oJetPUJetID_SF,oJetPUJetID_SF_up,oJetPUJetID_SF_down = 1.0,1.0,1.0
                
            bWeight = Get_B_tagging_sys_sf("Central",jet_id)
            for syst in self.shape_systs:
                if(syst=="Central"): 
                        self.out.fillBranch("bWeight", bWeight)
                else:
                        self.out.fillBranch("bWeight_"+syst,[Get_B_tagging_sys_sf(syst+"_up",jet_id),Get_B_tagging_sys_sf(syst+"_down",jet_id)])
            sf_jesup,sf_jesdown = Get_B_tagging_jes_sf(jet_id)
            self.out.fillBranch("bWeight_jes_variation_up",sf_jesup)
            self.out.fillBranch("bWeight_jes_variation_down",sf_jesdown)            
        top4v_kin = lepton4v_kin + bJet4v + Nu4v_kin 
        top4v = lepton4v + bJet4v + neutrino4v
        topMass=top4v.M()
        topPt=top4v.Pt()

        self.out.fillBranch("topPt_kin", top4v_kin.Pt())
        self.out.fillBranch("topEta_kin", top4v_kin.Eta())
        self.out.fillBranch("topPhi_kin", top4v_kin.Phi())
        self.out.fillBranch("topMass_kin", top4v_kin.M())       

        njet_sel = -1
        Jetpt = getattr(event,'Jet_pt')
        JetEta = getattr(event,'Jet_eta')
        Jetphi = getattr(event,'Jet_phi')
        for jet in jets:
            njet_sel = njet_sel+1
            if(Jetpt[njet_sel]==bJetPt and JetEta[njet_sel]==bJetEta and Jetphi[njet_sel]==bJetPhi): nbjet_sel = njet_sel
            if(Jetpt[njet_sel]==lJetPt and JetEta[njet_sel]==lJetEta and Jetphi[njet_sel]==lJetPhi): nljet_sel = njet_sel
            if(self.Total_Njets==3):
                 if(Jetpt[njet_sel]==oJetPt and JetEta[njet_sel]==oJetEta and Jetphi[njet_sel]==oJetPhi): nojet_sel = njet_sel
                
        

        mlb = (lepton4v+bJet4v).M()
        E_lb = (lepton4v+bJet4v).E()
        p_lb = (lepton4v+bJet4v).P()
        theta_lb = (lepton4v+bJet4v).Theta()
        jetpTSum = bJetPt+lJetPt
        if(bJetPt>=lJetPt and bJetPt>=oJetPt):hardJetMass = bJet4v.M()
        elif(lJetPt>=bJetPt and lJetPt>=oJetPt):hardJetMass = lJet4v.M()
        elif(oJetPt>=lJetPt and oJetPt>=bJetPt):hardJetMass = oJet4v.M()
        lJetMass = lJet4v.M()
        diJetMass = (lJet4v+bJet4v).M()
        if(self.letopn_flv == 'mu'):
            dEta_mu_bJet = abs(bJet4v.Eta()-lepton4v.Eta())        #in loretz vector class there is no function avalable for Delta Eta
            dEta_mu_lJet = abs(lJet4v.Eta() - lepton4v.Eta()) 
            dPhi_mu_bJet = lepton4v.DeltaPhi(bJet4v) 
            dPhi_mu_met = ROOT.TVector2.Phi_mpi_pi(lepton4v.Phi() - metphi)  #Phi_mpi_pi gives angle -pi to pi
            dPhi_mu_lJet = lepton4v.DeltaPhi(lJet4v)
            dR_mu_bJet = lepton4v.DeltaR(bJet4v)
            dR_mu_lJet = lepton4v.DeltaR(lJet4v) 
        if(self.letopn_flv == 'el'):
            dEta_el_bJet = abs(bJet4v.Eta()-lepton4v.Eta())        #in loretz vector class there is no function avalable for Delta Eta
            dEta_el_lJet = abs(lJet4v.Eta() - lepton4v.Eta())
            dPhi_el_bJet = lepton4v.DeltaPhi(bJet4v)
            dPhi_el_met = ROOT.TVector2.Phi_mpi_pi(lepton4v.Phi() - metphi)  #Phi_mpi_pi gives angle -pi to pi
            dPhi_el_lJet = lepton4v.DeltaPhi(lJet4v)
            dR_el_bJet = lepton4v.DeltaR(bJet4v)
            dR_el_lJet = lepton4v.DeltaR(lJet4v)
        dEta_bJet_lJet = abs(lJet4v.Eta() - bJet4v.Eta()) 
        dEta_top_lJet = abs(lJet4v.Eta() - top4v.Eta())                         
        
        dPhi_bJet_lJet = bJet4v.DeltaPhi(lJet4v)
        dPhi_top_lJet = top4v.DeltaPhi(lJet4v)

        dR_bJet_lJet = bJet4v.DeltaR(lJet4v) 
        dR_top_lJet = top4v.DeltaR(lJet4v)
        
        MinDR_lep_lnbJet = min(lepton4v.DeltaR(bJet4v),lepton4v.DeltaR(lJet4v))
        
        lep4v_for_transformation = ROOT.TLorentzVector()
        lJet4v_for_transformation = ROOT.TLorentzVector()
        lep4v_for_transformation = lepton4v
        lJet4v_for_transformation = lJet4v       #storing the untranformed lepton4v and ljetv
        bx= top4v.BoostVector().X()
        by= top4v.BoostVector().Y() #calculation the lorezboost commponent of top
        bz= top4v.BoostVector().Z()
        lep4v_for_transformation.Boost(-bx, -by, -bz) #loretz tranformation of lepton4v and ljetv
        lJet4v_for_transformation.Boost(-bx, -by, -bz)
        cosThetaStar = math.cos(lep4v_for_transformation.Angle(lJet4v_for_transformation.Vect()))

        try:
             LHEWeightSign = getattr(event,'LHEWeight_originalXWGTUP')/abs(getattr(event,'LHEWeight_originalXWGTUP'))
        except:
             LHEWeightSign = 1

        if(self.isMC==True):
             Event_wgt = Xsec_wgt*LHEWeightSign*(getattr(event,'puWeight'))*leptonSF*bWeight

             self.out.fillBranch("LHEWeightSign",LHEWeightSign)
             self.out.fillBranch("Xsec_wgt",Xsec_wgt )
             self.out.fillBranch("Event_wgt",Event_wgt)
 
        self.out.fillBranch("MinDR_lep_lnbJet",MinDR_lep_lnbJet)
        self.out.fillBranch("bJetMass", bJetMass)
        self.out.fillBranch("bJetPt", bJetPt )
        self.out.fillBranch("bJetEta", bJetEta )
        self.out.fillBranch("abs_bJetEta", abs_bJetEta )
        self.out.fillBranch("bJetPhi", bJetPhi )
        self.out.fillBranch("bJetdeepJet", bJetdeepJet )
        self.out.fillBranch("nbjet_sel",nbjet_sel)
        if(self.isMC==True):
            self.out.fillBranch("bJethadronFlavour", bJethadronFlavour )
            self.out.fillBranch("bJetpartonFlavour", bJetpartonFlavour)
            self.out.fillBranch("bJetPUJetID_SF", bJetPUJetID_SF )
            self.out.fillBranch("bJetPUJetID_SF_up", bJetPUJetID_SF_up )
            self.out.fillBranch("bJetPUJetID_SF_down", bJetPUJetID_SF_down )


        self.out.fillBranch("lJetMass", lJetMass )
        self.out.fillBranch("lJetPt", lJetPt )
        self.out.fillBranch("lJetEta", lJetEta )
        self.out.fillBranch("abs_lJetEta", abs_lJetEta )
        self.out.fillBranch("lJetPhi", lJetPhi )
        self.out.fillBranch("lJetdeepJet", lJetdeepJet )
        self.out.fillBranch("nljet_sel", nljet_sel)
        if(self.isMC==True):
            self.out.fillBranch("lJethadronFlavour", lJethadronFlavour )
            self.out.fillBranch("lJetpartonFlavour", lJetpartonFlavour)
            self.out.fillBranch("lJetPUJetID_SF", lJetPUJetID_SF )
            self.out.fillBranch("lJetPUJetID_SF_up", lJetPUJetID_SF_up )
            self.out.fillBranch("lJetPUJetID_SF_down", lJetPUJetID_SF_down )

        if(self.Total_Njets == 3 and  (self.BTag_Njets == 1 or self.BTag_Njets == 2)):
            self.out.fillBranch("oJetMass", oJetMass )
            self.out.fillBranch("oJetPt", oJetPt )
            self.out.fillBranch("oJetEta", oJetEta )
            self.out.fillBranch("abs_oJetEta", abs_oJetEta )
            self.out.fillBranch("oJetPhi", oJetPhi )
            self.out.fillBranch("oJetdeepJet", oJetdeepJet )
            self.out.fillBranch("nojet_sel", nojet_sel)
            if(self.isMC==True):
                self.out.fillBranch("oJethadronFlavour", oJethadronFlavour )
                self.out.fillBranch("oJetpartonFlavour", oJetpartonFlavour )
                self.out.fillBranch("oJetPUJetID_SF", oJetPUJetID_SF )  
                self.out.fillBranch("oJetPUJetID_SF_up", oJetPUJetID_SF_up )
                self.out.fillBranch("oJetPUJetID_SF_down", oJetPUJetID_SF_down )

        self.out.fillBranch("Px_nu", Px_nu)
        self.out.fillBranch("Py_nu", Py_nu)
        self.out.fillBranch("Pz_nu", Pz_nu)
        self.out.fillBranch("FW1", Foxwol_h1)
        self.out.fillBranch("FW2", Foxwol_h2)
        self.out.fillBranch("FW3", Foxwol_h3)
        self.out.fillBranch("mtwMass",mtwMass)
        self.out.fillBranch("mtwMass_kin",mtwMass_kin)
        self.out.fillBranch("topMass", topMass)
        self.out.fillBranch("topPt", topPt)
        self.out.fillBranch("cosThetaStar", cosThetaStar)
        self.out.fillBranch("mlb", mlb )
        self.out.fillBranch("E_lb",E_lb )
        self.out.fillBranch("p_lb",p_lb )
        self.out.fillBranch("theta_lb", theta_lb)
        self.out.fillBranch("jetpTSum",jetpTSum )
        self.out.fillBranch("hardJetMass", hardJetMass )
        self.out.fillBranch("lJetMass", lJetMass)
        self.out.fillBranch("diJetMass",diJetMass )
        if(self.letopn_flv == 'mu'):
            self.out.fillBranch("MuonPt",leptonPt)
            self.out.fillBranch("MuonEta",leptonEta)
            self.out.fillBranch("MuonPhi",leptonPhi)
            self.out.fillBranch("MuonMass",leptonMass)
            self.out.fillBranch("MuonE",leptonE)
            self.out.fillBranch("MuonCharge",leptonCharge)
            self.out.fillBranch("dEta_mu_bJet",dEta_mu_bJet )
            self.out.fillBranch("dEta_mu_lJet",dEta_mu_lJet )
            self.out.fillBranch("dPhi_mu_bJet",dPhi_mu_bJet )
            self.out.fillBranch("dPhi_mu_met",dPhi_mu_met )
            self.out.fillBranch("dPhi_mu_lJet",dPhi_mu_lJet )
            self.out.fillBranch("dR_mu_bJet",dR_mu_bJet)        
            self.out.fillBranch("dR_mu_lJet",dR_mu_lJet )
            if(self.isMC==True):self.out.fillBranch("muSF",leptonSF) 

        if(self.letopn_flv == 'el'):
            self.out.fillBranch("ElectronPt",leptonPt)
            self.out.fillBranch("ElectronEta",leptonEta)
            self.out.fillBranch("ElectronPhi",leptonPhi)
            self.out.fillBranch("ElectronMass",leptonMass)
            self.out.fillBranch("ElectronE",leptonE)
            self.out.fillBranch("ElectronCharge",leptonCharge)
            self.out.fillBranch("ElectronSCEta",ElectronSCEta)
            self.out.fillBranch("dEta_el_bJet",dEta_el_bJet )
            self.out.fillBranch("dEta_el_lJet",dEta_el_lJet )
            self.out.fillBranch("dPhi_el_bJet",dPhi_el_bJet )
            self.out.fillBranch("dPhi_el_met",dPhi_el_met )
            self.out.fillBranch("dPhi_el_lJet",dPhi_el_lJet )
            self.out.fillBranch("dR_el_bJet",dR_el_bJet )
            self.out.fillBranch("dR_el_lJet",dR_el_lJet )
            if(self.isMC==True):self.out.fillBranch("elSF",leptonSF)

        self.out.fillBranch("dEta_bJet_lJet",dEta_bJet_lJet )
        self.out.fillBranch("dEta_top_lJet",dEta_top_lJet )
        self.out.fillBranch("dPhi_bJet_lJet",dPhi_bJet_lJet )
        self.out.fillBranch("dPhi_top_lJet", dPhi_top_lJet )
        self.out.fillBranch("dR_bJet_lJet",dR_bJet_lJet ) 
        self.out.fillBranch("dR_top_lJet",dR_top_lJet ) 
        #print '--------------------------------------------------------------------------------'
        #print(getattr(event,'event'))
        return True

#----------------------------------------------2J1T------------------------------------------------


MinitreeModuleConstr2J1T1_mu_mc_UL2016preVFP = lambda MCsample : MinitreeProducer(2,1,True,'mu',True,'UL2016preVFP',MCsample)
MinitreeModuleConstr2J1T1_mu_data_UL2016preVFP = lambda : MinitreeProducer(2,1,True,'mu',False,'UL2016preVFP')
MinitreeModuleConstr2J1T1_el_mc_UL2016preVFP = lambda MCsample : MinitreeProducer(2,1,True,'el',True,'UL2016preVFP',MCsample)
MinitreeModuleConstr2J1T1_el_data_UL2016preVFP = lambda : MinitreeProducer(2,1,True,'el',False,'UL2016preVFP')

MinitreeModuleConstr2J1T1_mu_mc_UL2016postVFP = lambda MCsample : MinitreeProducer(2,1,True,'mu',True,'UL2016postVFP',MCsample)
MinitreeModuleConstr2J1T1_mu_data_UL2016postVFP = lambda : MinitreeProducer(2,1,True,'mu',False,'UL2016postVFP')
MinitreeModuleConstr2J1T1_el_mc_UL2016postVFP = lambda MCsample : MinitreeProducer(2,1,True,'el',True,'UL2016postVFP',MCsample)
MinitreeModuleConstr2J1T1_el_data_UL2016postVFP = lambda : MinitreeProducer(2,1,True,'el',False,'UL2016postVFP')

MinitreeModuleConstr2J1T0_mu_mc_UL2016preVFP = lambda MCsample : MinitreeProducer(2,1,False,'mu',True,'UL2016preVFP',MCsample)
MinitreeModuleConstr2J1T0_mu_data_UL2016preVFP = lambda : MinitreeProducer(2,1,False,'mu',False,'UL2016preVFP')
MinitreeModuleConstr2J1T0_el_mc_UL2016preVFP = lambda MCsample : MinitreeProducer(2,1,False,'el',True,'UL2016preVFP',MCsample)
MinitreeModuleConstr2J1T0_el_data_UL2016preVFP = lambda : MinitreeProducer(2,1,False,'el',False,'UL2016preVFP')

MinitreeModuleConstr2J1T0_mu_mc_UL2016postVFP = lambda MCsample : MinitreeProducer(2,1,False,'mu',True,'UL2016postVFP',MCsample)
MinitreeModuleConstr2J1T0_mu_data_UL2016postVFP = lambda : MinitreeProducer(2,1,False,'mu',False,'UL2016postVFP')
MinitreeModuleConstr2J1T0_el_mc_UL2016postVFP = lambda MCsample : MinitreeProducer(2,1,False,'el',True,'UL2016postVFP',MCsample)
MinitreeModuleConstr2J1T0_el_data_UL2016postVFP = lambda : MinitreeProducer(2,1,False,'el',False,'UL2016postVFP')

MinitreeModuleConstr2J1T1_mu_mc_UL2017 = lambda MCsample : MinitreeProducer(2,1,True,'mu',True,'UL2017',MCsample)
MinitreeModuleConstr2J1T1_mu_data_UL2017 = lambda : MinitreeProducer(2,1,True,'mu',False,'UL2017')
MinitreeModuleConstr2J1T1_el_mc_UL2017 = lambda MCsample : MinitreeProducer(2,1,True,'el',True,'UL2017',MCsample)
MinitreeModuleConstr2J1T1_el_data_UL2017 = lambda : MinitreeProducer(2,1,True,'el',False,'UL2017')

MinitreeModuleConstr2J1T0_mu_mc_UL2017 = lambda MCsample : MinitreeProducer(2,1,False,'mu',True,'UL2017',MCsample)
MinitreeModuleConstr2J1T0_mu_data_UL2017 = lambda : MinitreeProducer(2,1,False,'mu',False,'UL2017')
MinitreeModuleConstr2J1T0_el_mc_UL2017 = lambda MCsample : MinitreeProducer(2,1,False,'el',True,'UL2017',MCsample)
MinitreeModuleConstr2J1T0_el_data_UL2017 = lambda : MinitreeProducer(2,1,False,'el',False,'UL2017')

MinitreeModuleConstr2J1T1_mu_mc_UL2018 = lambda MCsample : MinitreeProducer(2,1,True,'mu',True,'UL2018',MCsample)
MinitreeModuleConstr2J1T1_mu_data_UL2018 = lambda : MinitreeProducer(2,1,True,'mu',False,'UL2018')
MinitreeModuleConstr2J1T1_el_mc_UL2018 = lambda MCsample : MinitreeProducer(2,1,True,'el',True,'UL2018',MCsample)
MinitreeModuleConstr2J1T1_el_data_UL2018 = lambda : MinitreeProducer(2,1,True,'el',False,'UL2018')

MinitreeModuleConstr2J1T0_mu_mc_UL2018 = lambda MCsample : MinitreeProducer(2,1,False,'mu',True,'UL2018',MCsample)
MinitreeModuleConstr2J1T0_mu_data_UL2018 = lambda : MinitreeProducer(2,1,False,'mu',False,'UL2018')
MinitreeModuleConstr2J1T0_el_mc_UL2018 = lambda MCsample : MinitreeProducer(2,1,False,'el',True,'UL2018',MCsample)
MinitreeModuleConstr2J1T0_el_data_UL2018 = lambda : MinitreeProducer(2,1,False,'el',False,'UL2018')

#----------------------------------------------2J0T------------------------------------------------


MinitreeModuleConstr2J0T1_mu_mc_UL2016preVFP = lambda MCsample : MinitreeProducer(2,0,True,'mu',True,'UL2016preVFP',MCsample)
MinitreeModuleConstr2J0T1_mu_data_UL2016preVFP = lambda : MinitreeProducer(2,0,True,'mu',False,'UL2016preVFP')
MinitreeModuleConstr2J0T1_el_mc_UL2016preVFP = lambda MCsample : MinitreeProducer(2,0,True,'el',True,'UL2016preVFP',MCsample)
MinitreeModuleConstr2J0T1_el_data_UL2016preVFP = lambda : MinitreeProducer(2,0,True,'el',False,'UL2016preVFP')

MinitreeModuleConstr2J0T0_mu_mc_UL2016preVFP = lambda MCsample : MinitreeProducer(2,0,False,'mu',True,'UL2016preVFP',MCsample)
MinitreeModuleConstr2J0T0_mu_data_UL2016preVFP = lambda : MinitreeProducer(2,0,False,'mu',False,'UL2016preVFP')
MinitreeModuleConstr2J0T0_el_mc_UL2016preVFP = lambda MCsample : MinitreeProducer(2,0,False,'el',True,'UL2016preVFP',MCsample)
MinitreeModuleConstr2J0T0_el_data_UL2016preVFP = lambda : MinitreeProducer(2,0,False,'el',False,'UL2016preVFP')

MinitreeModuleConstr2J0T1_mu_mc_UL2016postVFP = lambda MCsample : MinitreeProducer(2,0,True,'mu',True,'UL2016postVFP',MCsample)
MinitreeModuleConstr2J0T1_mu_data_UL2016postVFP = lambda : MinitreeProducer(2,0,True,'mu',False,'UL2016postVFP')
MinitreeModuleConstr2J0T1_el_mc_UL2016postVFP = lambda MCsample : MinitreeProducer(2,0,True,'el',True,'UL2016postVFP',MCsample)
MinitreeModuleConstr2J0T1_el_data_UL2016postVFP = lambda : MinitreeProducer(2,0,True,'el',False,'UL2016postVFP')

MinitreeModuleConstr2J0T0_mu_mc_UL2016postVFP = lambda MCsample : MinitreeProducer(2,0,False,'mu',True,'UL2016postVFP',MCsample)
MinitreeModuleConstr2J0T0_mu_data_UL2016postVFP = lambda : MinitreeProducer(2,0,False,'mu',False,'UL2016postVFP')
MinitreeModuleConstr2J0T0_el_mc_UL2016postVFP = lambda MCsample : MinitreeProducer(2,0,False,'el',True,'UL2016postVFP',MCsample)
MinitreeModuleConstr2J0T0_el_data_UL2016postVFP = lambda : MinitreeProducer(2,0,False,'el',False,'UL2016postVFP')

MinitreeModuleConstr2J0T1_mu_mc_UL2017 = lambda MCsample : MinitreeProducer(2,0,True,'mu',True,'UL2017',MCsample)
MinitreeModuleConstr2J0T1_mu_data_UL2017 = lambda : MinitreeProducer(2,0,True,'mu',False,'UL2017')
MinitreeModuleConstr2J0T1_el_mc_UL2017 = lambda MCsample : MinitreeProducer(2,0,True,'el',True,'UL2017',MCsample)
MinitreeModuleConstr2J0T1_el_data_UL2017 = lambda : MinitreeProducer(2,0,True,'el',False,'UL2017')

MinitreeModuleConstr2J0T0_mu_mc_UL2017 = lambda MCsample : MinitreeProducer(2,0,False,'mu',True,'UL2017',MCsample)
MinitreeModuleConstr2J0T0_mu_data_UL2017 = lambda : MinitreeProducer(2,0,False,'mu',False,'UL2017')
MinitreeModuleConstr2J0T0_el_mc_UL2017 = lambda MCsample : MinitreeProducer(2,0,False,'el',True,'UL2017',MCsample)
MinitreeModuleConstr2J0T0_el_data_UL2017 = lambda : MinitreeProducer(2,0,False,'el',False,'UL2017')

MinitreeModuleConstr2J0T1_mu_mc_UL2018 = lambda MCsample : MinitreeProducer(2,0,True,'mu',True,'UL2018',MCsample)
MinitreeModuleConstr2J0T1_mu_data_UL2018 = lambda : MinitreeProducer(2,0,True,'mu',False,'UL2018')
MinitreeModuleConstr2J0T1_el_mc_UL2018 = lambda MCsample : MinitreeProducer(2,0,True,'el',True,'UL2018',MCsample)
MinitreeModuleConstr2J0T1_el_data_UL2018 = lambda : MinitreeProducer(2,0,True,'el',False,'UL2018')

MinitreeModuleConstr2J0T0_mu_mc_UL2018 = lambda MCsample : MinitreeProducer(2,0,False,'mu',True,'UL2018',MCsample)
MinitreeModuleConstr2J0T0_mu_data_UL2018 = lambda : MinitreeProducer(2,0,False,'mu',False,'UL2018')
MinitreeModuleConstr2J0T0_el_mc_UL2018 = lambda MCsample : MinitreeProducer(2,0,False,'el',True,'UL2018',MCsample)
MinitreeModuleConstr2J0T0_el_data_UL2018 = lambda : MinitreeProducer(2,0,False,'el',False,'UL2018')

#----------------------------------------------3J1T-----------------------------------------------

MinitreeModuleConstr3J1T1_mu_mc_UL2016preVFP = lambda MCsample : MinitreeProducer(3,1,True,'mu',True,'UL2016preVFP',MCsample)
MinitreeModuleConstr3J1T1_mu_data_UL2016preVFP = lambda : MinitreeProducer(3,1,True,'mu',False,'UL2016preVFP')
MinitreeModuleConstr3J1T1_el_mc_UL2016preVFP = lambda MCsample : MinitreeProducer(3,1,True,'el',True,'UL2016preVFP',MCsample)
MinitreeModuleConstr3J1T1_el_data_UL2016preVFP = lambda : MinitreeProducer(3,1,True,'el',False,'UL2016preVFP')

MinitreeModuleConstr3J1T0_mu_mc_UL2016preVFP = lambda MCsample : MinitreeProducer(3,1,False,'mu',True,'UL2016preVFP',MCsample)
MinitreeModuleConstr3J1T0_mu_data_UL2016preVFP = lambda : MinitreeProducer(3,1,False,'mu',False,'UL2016preVFP')
MinitreeModuleConstr3J1T0_el_mc_UL2016preVFP = lambda MCsample : MinitreeProducer(3,1,False,'el',True,'UL2016preVFP',MCsample)
MinitreeModuleConstr3J1T0_el_data_UL2016preVFP = lambda : MinitreeProducer(3,1,False,'el',False,'UL2016preVFP')

MinitreeModuleConstr3J1T1_mu_mc_UL2016postVFP = lambda MCsample : MinitreeProducer(3,1,True,'mu',True,'UL2016postVFP',MCsample)
MinitreeModuleConstr3J1T1_mu_data_UL2016postVFP = lambda : MinitreeProducer(3,1,True,'mu',False,'UL2016postVFP')
MinitreeModuleConstr3J1T1_el_mc_UL2016postVFP = lambda MCsample : MinitreeProducer(3,1,True,'el',True,'UL2016postVFP',MCsample)
MinitreeModuleConstr3J1T1_el_data_UL2016postVFP = lambda : MinitreeProducer(3,1,True,'el',False,'UL2016postVFP')

MinitreeModuleConstr3J1T0_mu_mc_UL2016postVFP = lambda MCsample : MinitreeProducer(3,1,False,'mu',True,'UL2016postVFP',MCsample)
MinitreeModuleConstr3J1T0_mu_data_UL2016postVFP = lambda : MinitreeProducer(3,1,False,'mu',False,'UL2016postVFP')
MinitreeModuleConstr3J1T0_el_mc_UL2016postVFP = lambda MCsample : MinitreeProducer(3,1,False,'el',True,'UL2016postVFP',MCsample)
MinitreeModuleConstr3J1T0_el_data_UL2016postVFP = lambda : MinitreeProducer(3,1,False,'el',False,'UL2016postVFP')

MinitreeModuleConstr3J1T1_mu_mc_UL2017 = lambda MCsample : MinitreeProducer(3,1,True,'mu',True,'UL2017',MCsample)
MinitreeModuleConstr3J1T1_mu_data_UL2017 = lambda : MinitreeProducer(3,1,True,'mu',False,'UL2017')
MinitreeModuleConstr3J1T1_el_mc_UL2017 = lambda MCsample : MinitreeProducer(3,1,True,'el',True,'UL2017',MCsample)
MinitreeModuleConstr3J1T1_el_data_UL2017 = lambda : MinitreeProducer(3,1,True,'el',False,'UL2017')

MinitreeModuleConstr3J1T0_mu_mc_UL2017 = lambda MCsample : MinitreeProducer(3,1,False,'mu',True,'UL2017',MCsample)
MinitreeModuleConstr3J1T0_mu_data_UL2017 = lambda : MinitreeProducer(3,1,False,'mu',False,'UL2017')
MinitreeModuleConstr3J1T0_el_mc_UL2017 = lambda MCsample : MinitreeProducer(3,1,False,'el',True,'UL2017',MCsample)
MinitreeModuleConstr3J1T0_el_data_UL2017 = lambda : MinitreeProducer(3,1,False,'el',False,'UL2017')

MinitreeModuleConstr3J1T1_mu_mc_UL2018 = lambda MCsample : MinitreeProducer(3,1,True,'mu',True,'UL2018',MCsample)
MinitreeModuleConstr3J1T1_mu_data_UL2018 = lambda : MinitreeProducer(3,1,True,'mu',False,'UL2018')
MinitreeModuleConstr3J1T1_el_mc_UL2018 = lambda MCsample : MinitreeProducer(3,1,True,'el',True,'UL2018',MCsample)
MinitreeModuleConstr3J1T1_el_data_UL2018 = lambda : MinitreeProducer(3,1,True,'el',False,'UL2018')

MinitreeModuleConstr3J1T0_mu_mc_UL2018 = lambda MCsample : MinitreeProducer(3,1,False,'mu',True,'UL2018',MCsample)
MinitreeModuleConstr3J1T0_mu_data_UL2018 = lambda : MinitreeProducer(3,1,False,'mu',False,'UL2018')
MinitreeModuleConstr3J1T0_el_mc_UL2018 = lambda MCsample : MinitreeProducer(3,1,False,'el',True,'UL2018',MCsample)
MinitreeModuleConstr3J1T0_el_data_UL2018 = lambda : MinitreeProducer(3,1,False,'el',False,'UL2018')

#------------------------------------------3J2T---------------------------------------------------


MinitreeModuleConstr3J2T1_mu_mc_UL2016preVFP = lambda MCsample : MinitreeProducer(3,2,True,'mu',True,'UL2016preVFP',MCsample)
MinitreeModuleConstr3J2T1_mu_data_UL2016preVFP = lambda : MinitreeProducer(3,2,True,'mu',False,'UL2016preVFP')
MinitreeModuleConstr3J2T1_el_mc_UL2016preVFP = lambda MCsample : MinitreeProducer(3,2,True,'el',True,'UL2016preVFP',MCsample)
MinitreeModuleConstr3J2T1_el_data_UL2016preVFP = lambda : MinitreeProducer(3,2,True,'el',False,'UL2016preVFP')

MinitreeModuleConstr3J2T0_mu_mc_UL2016preVFP = lambda MCsample : MinitreeProducer(3,2,False,'mu',True,'UL2016preVFP',MCsample)
MinitreeModuleConstr3J2T0_mu_data_UL2016preVFP = lambda : MinitreeProducer(3,2,False,'mu',False,'UL2016preVFP')
MinitreeModuleConstr3J2T0_el_mc_UL2016preVFP = lambda MCsample : MinitreeProducer(3,2,False,'el',True,'UL2016preVFP',MCsample)
MinitreeModuleConstr3J2T0_el_data_UL2016preVFP = lambda : MinitreeProducer(3,2,False,'el',False,'UL2016preVFP')

MinitreeModuleConstr3J2T1_mu_mc_UL2016postVFP = lambda MCsample : MinitreeProducer(3,2,True,'mu',True,'UL2016postVFP',MCsample)
MinitreeModuleConstr3J2T1_mu_data_UL2016postVFP = lambda : MinitreeProducer(3,2,True,'mu',False,'UL2016postVFP')
MinitreeModuleConstr3J2T1_el_mc_UL2016postVFP = lambda MCsample : MinitreeProducer(3,2,True,'el',True,'UL2016postVFP',MCsample)
MinitreeModuleConstr3J2T1_el_data_UL2016postVFP = lambda : MinitreeProducer(3,2,True,'el',False,'UL2016postVFP')

MinitreeModuleConstr3J2T0_mu_mc_UL2016postVFP = lambda MCsample : MinitreeProducer(3,2,False,'mu',True,'UL2016postVFP',MCsample)
MinitreeModuleConstr3J2T0_mu_data_UL2016postVFP = lambda : MinitreeProducer(3,2,False,'mu',False,'UL2016postVFP')
MinitreeModuleConstr3J2T0_el_mc_UL2016postVFP = lambda MCsample : MinitreeProducer(3,2,False,'el',True,'UL2016postVFP',MCsample)
MinitreeModuleConstr3J2T0_el_data_UL2016postVFP = lambda : MinitreeProducer(3,2,False,'el',False,'UL2016postVFP')

MinitreeModuleConstr3J2T1_mu_mc_UL2017 = lambda MCsample : MinitreeProducer(3,2,True,'mu',True,'UL2017',MCsample)
MinitreeModuleConstr3J2T1_mu_data_UL2017 = lambda : MinitreeProducer(3,2,True,'mu',False,'UL2017')
MinitreeModuleConstr3J2T1_el_mc_UL2017 = lambda MCsample : MinitreeProducer(3,2,True,'el',True,'UL2017',MCsample)
MinitreeModuleConstr3J2T1_el_data_UL2017 = lambda : MinitreeProducer(3,2,True,'el',False,'UL2017')

MinitreeModuleConstr3J2T0_mu_mc_UL2017 = lambda MCsample : MinitreeProducer(3,2,False,'mu',True,'UL2017',MCsample)
MinitreeModuleConstr3J2T0_mu_data_UL2017 = lambda : MinitreeProducer(3,2,False,'mu',False,'UL2017')
MinitreeModuleConstr3J2T0_el_mc_UL2017 = lambda MCsample : MinitreeProducer(3,2,False,'el',True,'UL2017',MCsample)
MinitreeModuleConstr3J2T0_el_data_UL2017 = lambda : MinitreeProducer(3,2,False,'el',False,'UL2017')

MinitreeModuleConstr3J2T1_mu_mc_UL2018 = lambda MCsample : MinitreeProducer(3,2,True,'mu',True,'UL2018',MCsample)
MinitreeModuleConstr3J2T1_mu_data_UL2018 = lambda : MinitreeProducer(3,2,True,'mu',False,'UL2018')
MinitreeModuleConstr3J2T1_el_mc_UL2018 = lambda MCsample : MinitreeProducer(3,2,True,'el',True,'UL2018',MCsample)
MinitreeModuleConstr3J2T1_el_data_UL2018 = lambda : MinitreeProducer(3,2,True,'el',False,'UL2018')

MinitreeModuleConstr3J2T0_mu_mc_UL2018 = lambda MCsample : MinitreeProducer(3,2,False,'mu',True,'UL2018',MCsample)
MinitreeModuleConstr3J2T0_mu_data_UL2018 = lambda : MinitreeProducer(3,2,False,'mu',False,'UL2018')
MinitreeModuleConstr3J2T0_el_mc_UL2018 = lambda MCsample : MinitreeProducer(3,2,False,'el',True,'UL2018',MCsample)
MinitreeModuleConstr3J2T0_el_data_UL2018 = lambda : MinitreeProducer(3,2,False,'el',False,'UL2018')
#------------------------------------------ 2J1L0T---------------------------------------------------------

MinitreeModuleConstr2J1L0T1_mu_mc_UL2016preVFP = lambda MCsample : MinitreeProducer(2,1,True,'mu',True,'UL2016preVFP',MCsample)
MinitreeModuleConstr2J1L0T1_mu_data_UL2016preVFP = lambda : MinitreeProducer(2,1,True,'mu',False,'UL2016preVFP')
MinitreeModuleConstr2J1L0T1_el_mc_UL2016preVFP = lambda MCsample : MinitreeProducer(2,1,True,'el',True,'UL2016preVFP',MCsample)
MinitreeModuleConstr2J1L0T1_el_data_UL2016preVFP = lambda : MinitreeProducer(2,1,True,'el',False,'UL2016preVFP')

MinitreeModuleConstr2J1L0T0_mu_mc_UL2016preVFP = lambda MCsample : MinitreeProducer(2,1,False,'mu',True,'UL2016preVFP',MCsample)
MinitreeModuleConstr2J1L0T0_mu_data_UL2016preVFP = lambda : MinitreeProducer(2,1,False,'mu',False,'UL2016preVFP')
MinitreeModuleConstr2J1L0T0_el_mc_UL2016preVFP = lambda MCsample : MinitreeProducer(2,1,False,'el',True,'UL2016preVFP',MCsample)
MinitreeModuleConstr2J1L0T0_el_data_UL2016preVFP = lambda : MinitreeProducer(2,1,False,'el',False,'UL2016preVFP')

MinitreeModuleConstr2J1L0T1_mu_mc_UL2016postVFP = lambda MCsample : MinitreeProducer(2,1,True,'mu',True,'UL2016postVFP',MCsample)
MinitreeModuleConstr2J1L0T1_mu_data_UL2016postVFP = lambda : MinitreeProducer(2,1,True,'mu',False,'UL2016postVFP')
MinitreeModuleConstr2J1L0T1_el_mc_UL2016postVFP = lambda MCsample : MinitreeProducer(2,1,True,'el',True,'UL2016postVFP',MCsample)
MinitreeModuleConstr2J1L0T1_el_data_UL2016postVFP = lambda : MinitreeProducer(2,1,True,'el',False,'UL2016postVFP')

MinitreeModuleConstr2J1L0T0_mu_mc_UL2016postVFP = lambda MCsample : MinitreeProducer(2,1,False,'mu',True,'UL2016postVFP',MCsample)
MinitreeModuleConstr2J1L0T0_mu_data_UL2016postVFP = lambda : MinitreeProducer(2,1,False,'mu',False,'UL2016postVFP')
MinitreeModuleConstr2J1L0T0_el_mc_UL2016postVFP = lambda MCsample : MinitreeProducer(2,1,False,'el',True,'UL2016postVFP',MCsample)
MinitreeModuleConstr2J1L0T0_el_data_UL2016postVFP = lambda : MinitreeProducer(2,1,False,'el',False,'UL2016postVFP')

MinitreeModuleConstr2J1L0T1_mu_mc_UL2017 = lambda MCsample : MinitreeProducer(2,1,True,'mu',True,'UL2017',MCsample)
MinitreeModuleConstr2J1L0T1_mu_data_UL2017 = lambda : MinitreeProducer(2,1,True,'mu',False,'UL2017')
MinitreeModuleConstr2J1L0T1_el_mc_UL2017 = lambda MCsample : MinitreeProducer(2,1,True,'el',True,'UL2017',MCsample)
MinitreeModuleConstr2J1L0T1_el_data_UL2017 = lambda : MinitreeProducer(2,1,True,'el',False,'UL2017')

MinitreeModuleConstr2J1L0T0_mu_mc_UL2017 = lambda MCsample : MinitreeProducer(2,1,False,'mu',True,'UL2017',MCsample)
MinitreeModuleConstr2J1L0T0_mu_data_UL2017 = lambda : MinitreeProducer(2,1,False,'mu',False,'UL2017')
MinitreeModuleConstr2J1L0T0_el_mc_UL2017 = lambda MCsample : MinitreeProducer(2,1,False,'el',True,'UL2017',MCsample)
MinitreeModuleConstr2J1L0T0_el_data_UL2017 = lambda : MinitreeProducer(2,1,False,'el',False,'UL2017')

MinitreeModuleConstr2J1L0T1_mu_mc_UL2018 = lambda MCsample : MinitreeProducer(2,1,True,'mu',True,'UL2018',MCsample)
MinitreeModuleConstr2J1L0T1_mu_data_UL2018 = lambda : MinitreeProducer(2,1,True,'mu',False,'UL2018')
MinitreeModuleConstr2J1L0T1_el_mc_UL2018 = lambda MCsample : MinitreeProducer(2,1,True,'el',True,'UL2018',MCsample)
MinitreeModuleConstr2J1L0T1_el_data_UL2018 = lambda : MinitreeProducer(2,1,True,'el',False,'UL2018')

MinitreeModuleConstr2J1L0T0_mu_mc_UL2018 = lambda MCsample : MinitreeProducer(2,1,False,'mu',True,'UL2018',MCsample)
MinitreeModuleConstr2J1L0T0_mu_data_UL2018 = lambda : MinitreeProducer(2,1,False,'mu',False,'UL2018')
MinitreeModuleConstr2J1L0T0_el_mc_UL2018 = lambda MCsample : MinitreeProducer(2,1,False,'el',True,'UL2018',MCsample)
MinitreeModuleConstr2J1L0T0_el_data_UL2018 = lambda : MinitreeProducer(2,1,False,'el',False,'UL2018')
