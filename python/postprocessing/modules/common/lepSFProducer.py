import ROOT
import os
import numpy as np
import json
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class lepSFProducer(Module):
    def __init__(self, muonSelectionTag, electronSelectionTag):
        self.mu_f_name = ["trigger","ID","ISO"]
        self.mu_f_sys_name = ["ID","ISO"]
        #2016 muon legacy
        if muonSelectionTag=="muonSF_2016_GH_legacy":
            self.mu_weights = [1]
            self.mu_f=[["EfficienciesAndSF_Period4.root",
                  "EfficienciesStudies_2016_legacy_rereco_rootfiles_RunGH_SF_ID.root",
                  "EfficienciesStudies_2016_legacy_rereco_rootfiles_RunGH_SF_ISO.root"]]
            self.mu_h = ["Mu50_OR_TkMu50_PtEtaBins/pt_abseta_ratio",
                    "NUM_TightID_DEN_genTracks_eta_pt",
                    "NUM_LooseRelIso_DEN_TightIDandIPCut_eta_pt"]
            self.mu_sys_f=[["EfficienciesStudies_2016_legacy_rereco_systematic_RunGH_SF_ID.root",
                    "EfficienciesStudies_2016_legacy_rereco_systematic_RunGH_SF_ISO.root"]]
            self.mu_sys_h = ["NUM_TightID_DEN_genTracks_eta_pt_syst",
                    "NUM_LooseRelIso_DEN_TightIDandIPCut_eta_pt_syst"]

        if muonSelectionTag=="muonSF_2016_BCDEF_legacy":
            self.mu_weights = [1]
            self.mu_f=[["EfficienciesAndSF_RunBtoF.root",
                  "EfficienciesStudies_2016_legacy_rereco_rootfiles_RunBCDEF_SF_ID.root",
                  "EfficienciesStudies_2016_legacy_rereco_rootfiles_RunBCDEF_SF_ISO.root"]]
            self.mu_h = ["Mu50_OR_TkMu50_PtEtaBins/pt_abseta_ratio",
                    "NUM_TightID_DEN_genTracks_eta_pt",
                    "NUM_LooseRelIso_DEN_TightIDandIPCut_eta_pt"]
            self.mu_sys_f=[["EfficienciesStudies_2016_legacy_rereco_systematic_RunBCDEF_SF_ID.root",
                    "EfficienciesStudies_2016_legacy_rereco_systematic_RunBCDEF_SF_ISO.root"]]
            self.mu_sys_h = ["NUM_TightID_DEN_genTracks_eta_pt_syst",
                    "NUM_LooseRelIso_DEN_TightIDandIPCut_eta_pt_syst"]


        if muonSelectionTag=="muonSF_2016_weighted_legacy":
            self.mu_weights = [0.549334044,1-0.549334044] #luminositiy weighted for different trigger menus
            self.mu_f=[
                  ["EfficienciesAndSF_RunBtoF.root",
                  "EfficienciesStudies_2016_legacy_rereco_rootfiles_RunBCDEF_SF_ID.root",
                  "EfficienciesStudies_2016_legacy_rereco_rootfiles_RunBCDEF_SF_ISO.root"],
                  ["EfficienciesAndSF_Period4.root", #check this
                  "EfficienciesStudies_2016_legacy_rereco_rootfiles_RunGH_SF_ID.root",
                  "EfficienciesStudies_2016_legacy_rereco_rootfiles_RunGH_SF_ISO.root"]
                  ]
            self.mu_h = ["Mu50_OR_TkMu50_PtEtaBins/pt_abseta_ratio",
                    "NUM_TightID_DEN_genTracks_eta_pt",
                    "NUM_LooseRelIso_DEN_TightIDandIPCut_eta_pt"]
            self.mu_sys_f=[["EfficienciesStudies_2016_legacy_rereco_systematic_RunBCDEF_SF_ID.root",
                    "EfficienciesStudies_2016_legacy_rereco_systematic_RunBCDEF_SF_ISO.root"],
                    ["EfficienciesStudies_2016_legacy_rereco_systematic_RunGH_SF_ID.root",
                    "EfficienciesStudies_2016_legacy_rereco_systematic_RunGH_SF_ISO.root"]]
            self.mu_sys_h = ["NUM_TightID_DEN_genTracks_eta_pt_syst",
                    "NUM_LooseRelIso_DEN_TightIDandIPCut_eta_pt_syst"]

        #2016 muon
        if muonSelectionTag=="muonSF_2016_BCDEF":
            self.mu_weights = [1]
            mu_f=[["EfficienciesAndSF_RunBtoF.root",
                  "EfficienciesAndSF_BCDEF.root",
                  "EfficienciesAndSF_BCDEF-2.root"]]
            mu_h = ["Mu50_OR_TkMu50_PtEtaBins/pt_abseta_ratio",
                    "TightISO_TightID_pt_eta/pt_abseta_ratio",
                    "LooseISO_TightID_pt_eta/pt_abseta_ratio"]
        if muonSelectionTag=="muonSF_2016_GH":
            self.mu_weights = [1]
            mu_f=[["EfficienciesAndSF_Period4.root",
                  "EfficienciesAndSF_GH.root",
                  "EfficienciesAndSF_GH-2.root"]]
            mu_h = ["Mu50_OR_TkMu50_PtEtaBins/pt_abseta_ratio",
                    "TightISO_TightID_pt_eta/pt_abseta_ratio",
                    "LooseISO_TightID_pt_eta/pt_abseta_ratio"]
        #2017 muon
        if muonSelectionTag=="muonSF_2017":
            self.mu_weights = [1]
            self.mu_f=[["EfficienciesAndSF_RunBtoF_Nov17Nov2017.root",
                  "RunBCDEF_SF_ID_2017.root",
                  "RunBCDEF_SF_ISO_2017.root"]]
            self.mu_h = ["Mu50_PtEtaBins/pt_abseta_ratio",
                    "NUM_TightID_DEN_genTracks_pt_abseta",
                    "NUM_LooseRelIso_DEN_TightIDandIPCut_pt_abseta"]
            self.mu_sys_f=[["RunBCDEF_2017_SF_ID_syst.root",
                    "RunBCDEF_2017_SF_ISO_syst.root"]]
            self.mu_sys_h = ["NUM_TightID_DEN_genTracks_pt_abseta_syst",
                    "NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta_syst"]
        #2018 muon
        if muonSelectionTag=="muonSF_2018_beforeHLT":
            self.mu_weights = [1]
            self.mu_f=[["EfficienciesStudies_2018_trigger_EfficienciesAndSF_2018Data_BeforeMuonHLTUpdate.root",
                  "EfficienciesStudies_2018_rootfiles_RunABCD_SF_ID.root",
                  "EfficienciesStudies_2018_rootfiles_RunABCD_SF_ISO.root"]]
            self.mu_h = ["Mu50_OR_OldMu100_OR_TkMu100_PtEtaBins/pt_abseta_ratio",
                    "NUM_TightID_DEN_TrackerMuons_pt_abseta",
                    "NUM_LooseRelIso_DEN_TightIDandIPCut_pt_abseta"]
            self.mu_sys_f=[["EfficienciesStudies_2018_rootfiles_RunABCD_SF_ID.root",
                    "EfficienciesStudies_2018_rootfiles_RunABCD_SF_ISO.root"]]
            self.mu_sys_h = ["NUM_TightID_DEN_TrackerMuons_pt_abseta_syst",
                    "NUM_LooseRelIso_DEN_TightIDandIPCut_pt_abseta_syst"]
        if muonSelectionTag=="muonSF_2018_afterHLT":
            self.mu_weights = [1]
            self.mu_f=[["EfficienciesStudies_2018_trigger_EfficienciesAndSF_2018Data_AfterMuonHLTUpdate.root",
                  "EfficienciesStudies_2018_rootfiles_RunABCD_SF_ID.root",
                  "EfficienciesStudies_2018_rootfiles_RunABCD_SF_ISO.root"]]
            self.mu_h = ["Mu50_OR_OldMu100_OR_TkMu100_PtEtaBins/pt_abseta_ratio",
                    "NUM_TightID_DEN_TrackerMuons_pt_abseta",
                    "NUM_LooseRelIso_DEN_TightIDandIPCut_pt_abseta"]
            self.mu_sys_f=[["EfficienciesStudies_2018_rootfiles_RunABCD_SF_ID.root",
                    "EfficienciesStudies_2018_rootfiles_RunABCD_SF_ISO.root"]]
            self.mu_sys_h = ["NUM_TightID_DEN_TrackerMuons_pt_abseta_syst",
                    "NUM_LooseRelIso_DEN_TightIDandIPCut_pt_abseta_syst"]
        if muonSelectionTag=="muonSF_2018_weighted":
            self.mu_weights = [0.1593444345,1-0.1593444345] #luminositiy weighted for different trigger menus
            self.mu_f=[["EfficienciesStudies_2018_trigger_EfficienciesAndSF_2018Data_BeforeMuonHLTUpdate.root",
                  "EfficienciesStudies_2018_rootfiles_RunABCD_SF_ID.root",
                  "EfficienciesStudies_2018_rootfiles_RunABCD_SF_ISO.root"],
                  ["EfficienciesStudies_2018_trigger_EfficienciesAndSF_2018Data_AfterMuonHLTUpdate.root",
                  "EfficienciesStudies_2018_rootfiles_RunABCD_SF_ID.root",
                  "EfficienciesStudies_2018_rootfiles_RunABCD_SF_ISO.root"]]
            self.mu_h = ["Mu50_OR_OldMu100_OR_TkMu100_PtEtaBins/pt_abseta_ratio",
                    "NUM_TightID_DEN_TrackerMuons_pt_abseta",
                    "NUM_LooseRelIso_DEN_TightIDandIPCut_pt_abseta"]
            self.mu_sys_f=[["EfficienciesStudies_2018_rootfiles_RunABCD_SF_ID.root",
                    "EfficienciesStudies_2018_rootfiles_RunABCD_SF_ISO.root"],
                    ["EfficienciesStudies_2018_rootfiles_RunABCD_SF_ID.root",
                    "EfficienciesStudies_2018_rootfiles_RunABCD_SF_ISO.root"]]
            self.mu_sys_h = ["NUM_TightID_DEN_TrackerMuons_pt_abseta_syst",
                    "NUM_LooseRelIso_DEN_TightIDandIPCut_pt_abseta_syst"]
        #egamma
        if electronSelectionTag=="egamma_2016_legacy":
            self.el_SF_EB = 0.971
            self.el_SF_EE = 0.983
            self.el_stat_EB = 0.001
            self.el_stat_EE = 0.001
            self.el_sys_EB = [.01,0.0022,.03]
            self.el_sys_EE = [.01,0.0143,.04]
        if electronSelectionTag=="egamma_2017":
            self.el_SF_EB = 0.967
            self.el_SF_EE = 0.973
            self.el_stat_EE = 0.001
            self.el_stat_EB = 0.002
            self.el_sys_EB = [.01,0.0022,.03]
            self.el_sys_EE = [.02,0.0143,.05]
        if electronSelectionTag=="egamma_2018":
            self.el_SF_EB = 0.969
            self.el_SF_EE = 0.984
            self.el_stat_EE = 0.000
            self.el_stat_EB = 0.001
            self.el_sys_EB = [.01,0.0022,.03]
            self.el_sys_EE = [.02,0.0143,.05]

        self.mu_sys_f = [["%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/leptonSF/"
            % os.environ['CMSSW_BASE'] + f for f in f_list] for f_list in self.mu_sys_f]
        self.mu_f = [["%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/leptonSF/"
            % os.environ['CMSSW_BASE'] + f for f in f_list] for f_list in self.mu_f]

        if "/LeptonEfficiencyCorrector_cc.so" not in ROOT.gSystem.GetLibraries(
        ):
            print("Load C++ Worker")
            ROOT.gROOT.ProcessLine(
                ".L %s/src/PhysicsTools/NanoAODTools/python/postprocessing/helpers/LeptonEfficiencyCorrector.cc+"

                % os.environ['CMSSW_BASE'])
    def beginJob(self):
        self._worker_mu = [[] for i in range(len(self.mu_f))]
        for i in range(len(self.mu_f)):
            for j, f_list in enumerate(self.mu_f[i]):
                print f_list
                roo_vec_file = ROOT.std.vector(str)(1)
                roo_vec_hist = ROOT.std.vector(str)(1)
                roo_vec_file[0] = f_list
                roo_vec_hist[0] = self.mu_h[j]
                self._worker_mu[i].append( ROOT.LeptonEfficiencyCorrector(roo_vec_file,roo_vec_hist) )
        self._worker_sys_mu = [[] for i in range(len(self.mu_f))]
        for i in range(len(self.mu_sys_f)):
            for j, f_list in enumerate(self.mu_sys_f[i]):
                roo_vec_file = ROOT.std.vector(str)(1)
                roo_vec_hist = ROOT.std.vector(str)(1)
                roo_vec_file[0] = f_list
                roo_vec_hist[0] = self.mu_sys_h[j]
                self._worker_sys_mu[i].append( ROOT.LeptonEfficiencyCorrector(roo_vec_file,roo_vec_hist) )
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for type_SF in self.mu_f_name:
            self.out.branch("Muon_effSF_{}".format(type_SF), "F", lenVar="nMuon")
            self.out.branch("Muon_effSF_stat_{}".format(type_SF), "F", lenVar="nMuon")
        for type_SF in self.mu_f_sys_name:
            self.out.branch("Muon_effSF_sys_{}".format(type_SF), "F", lenVar="nMuon")
        self.out.branch("Electron_effSF", "F", lenVar="nElectron")
        self.out.branch("Electron_effSF_stat", "F", lenVar="nElectron")
        self.out.branch("Electron_effSF_sys", "F", lenVar="nElectron")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def computeSFlist(self, worker, hist_names, muons, error):
            sf_mu = [[] for i in range(len(worker))]
            for i in range(len(worker)):
                for j in range(len(worker[i])):
                    LEC_object = worker[i][j]
                    if "abseta" in hist_names[j]: pdgId = 13
                    else: pdgId = 99999
                    if not error: sf_mu[i].append([LEC_object.getSF(pdgId,mu.pt,mu.eta) for mu in muons ])
                    else: sf_mu[i].append([LEC_object.getSFErr(pdgId,mu.pt,mu.eta) for mu in muons ])
            averaged_sf_mu = np.multiply(self.mu_weights[0], sf_mu[0])
            for i in range(len(sf_mu)-1):
                averaged_sf_mu = np.add(averaged_sf_mu,np.multiply(self.mu_weights[i+1],sf_mu[i+1]))
            return averaged_sf_mu
    def computeElSF(self, el):
        eT = el.p4().Et()
        eta = el.eta
        if abs(eta) > 1.566 and abs(eta) < 2.5: SF = self.el_SF_EE
        elif abs(eta) < 1.4442: SF = self.el_SF_EB
        else: return 0
        return SF
    def computeElSys(self, el):
        eT = el.p4().Et()
        eta = el.eta
        if abs(eta) > 1.566 and abs(eta) < 2.5: sys_variables = self.el_sys_EE
        elif abs(eta) < 1.4442: sys_variables = self.el_sys_EB
        else: return -1
        if eT < 90: return sys_variables[0]
        else: return min((1+(eT-90)*sys_variables[1])/100,sys_variables[2])
    def computeElStat(self, el):
        eta = el.eta
        if abs(eta) > 1.566 and abs(eta) < 2.5: stat_variables = self.el_stat_EE
        elif abs(eta) < 1.4442: stat_variables = self.el_stat_EE
        else: return -0
        return stat_variables
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        muons = Collection(event, "Muon")
        electrons = Collection(event, "Electron")

        averaged_sf_mu = self.computeSFlist(self._worker_mu,self.mu_h,muons,False)
        averaged_sf_mu_stat = self.computeSFlist(self._worker_mu,self.mu_h,muons,True)
        averaged_sf_mu_sys = self.computeSFlist(self._worker_sys_mu,self.mu_sys_h,muons,True)

        for i, type_SF in enumerate(self.mu_f_name):
            self.out.fillBranch("Muon_effSF_{}".format(type_SF), averaged_sf_mu[i])
            self.out.fillBranch("Muon_effSF_stat_{}".format(type_SF), averaged_sf_mu_stat[i])
        for i, type_SF in enumerate(self.mu_f_sys_name):
            self.out.fillBranch("Muon_effSF_sys_{}".format(type_SF), averaged_sf_mu_sys[i])

        sf_el =  map(self.computeElSF, electrons)
        el_sys =  map(self.computeElSys, electrons)
        el_sys = np.multiply(el_sys,sf_el)
        el_stat = map(self.computeElStat, electrons)

        self.out.fillBranch("Electron_effSF", sf_el)
        self.out.fillBranch("Electron_effSF_stat", el_stat)
        self.out.fillBranch("Electron_effSF_sys", el_sys)
        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

lepSF2016 = lambda : lepSFProducer( "muonSF_2016_weighted_legacy", "egamma_2016_legacy") #MC
lepSF2016_GH_legacy = lambda : lepSFProducer( "muonSF_2016_GH_legacy", "egamma_2016_legacy")
lepSF2016_BtoF_legacy = lambda : lepSFProducer( "muonSF_2016_BCDEF_legacy", "egamma_2016_legacy")

lepSF2017 = lambda : lepSFProducer( "muonSF_2017", "egamma_2017")

lepSF2018 = lambda : lepSFProducer( "muonSF_2018_weighted", "egamma_2018") #MC
lepSF2018_beforeHLT = lambda : lepSFProducer( "muonSF_2018_beforeHLT", "egamma_2018")
lepSF2018_afterHLT = lambda : lepSFProducer( "muonSF_2018_afterHLT", "egamma_2018")
