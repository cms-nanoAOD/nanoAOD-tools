import ROOT
import math
from array import array
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *

inputpath = "/eos/home-a/adeiorio/Wprime/nosynch/" 
inpfiles = ['Wprime_4000_RH'
            #,"TT_Mtt-700to1000"
            #,'TT_Mtt-1000toInf_2016_1'
            #,"WJets"
            #,'QCD_Pt_600to800_1'
            #"SingleMuon_Run2016G_1"
            #,'Wprimetotb_M2000W20_RH_MG_8'
            ,'Wprimetotb_M4000W400_RH_MG_1'
            ,'TT_Incl_2016_1'
        ]

#ROOT.gROOT.SetStyle('Plain')
#ROOT.gStyle.SetPalette(1)
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch()        # don't pop up canvases                                                                                                                                              
ROOT.TH1.SetDefaultSumw2()
#ROOT.TGaxis.SetMaxDigits(3)

plotpath = './plots/'

# b-tag working points: mistagging efficiency tight = 0.1%, medium 1% and loose = 10% 
deepFlv_T = 0.7264 
deepFlv_M = 0.2770 
deepFlv_L = 0.0494 
deepCSV_T = 0.7527 
deepCSV_M = 0.4184 
deepCSV_L = 0.1241 

for inpfile in inpfiles:
    infile = ROOT.TFile.Open(inputpath + inpfile + ".root")
    tree = InputTree(infile.Events)
    isMC = True
    if ('SingleMuon' or 'SingleElectron' in inpfile):
        isMC = False
    #histogram booking
    nbins = 15
    nmin = 0
    nmax = 400
    edges = array('f',[0., 20., 40., 60., 80., 100., 130., 160., 190., 230., 270., 320., 360., 400., 700., 1000.])
    edges_HT = array('f',[0., 200., 400., 600., 800., 1000., 1200., 1400., 1600., 1800., 2000., 2200., 2400., 2800., 3400., 4000.])
    h_muonpt_HLT = ROOT.TH1F("Muon_pt", "Muon_pt", nbins, edges)
    h_HLT_Mu50 = ROOT.TH1F("HLT_Mu50", "HLT_Mu50", nbins, edges)
    h_HLT_TkMu50 = ROOT.TH1F("HLT_TkMu50", "HLT_TkMu50", nbins, edges)
    h_HLT = ROOT.TH1F("HLT_OR", "HLT_OR", nbins, edges)

    h_mu_HT_binned =  ROOT.TH1F("HT_MuTrg", "Event_HT_MuonTriggered", nbins, edges_HT)
    h_ele_HT_binned =  ROOT.TH1F("HT_EleTrg", "Event_HT_MuonTriggered", nbins, edges_HT)
    h_electronpt_HLT = ROOT.TH1F("Electron_pt", "Electron_pt", nbins, edges)
    h_HLT_Ele115 = ROOT.TH1F("HLT_Ele115", "HLT_Ele115", nbins, edges)

    h_HT = ROOT.TH1F("HT", "Event_HT", nbins, edges_HT)
    h_HT_mu = ROOT.TH1F("HT_Mu", "Event_HT_Mu", nbins, edges_HT)
    h_HT_ele = ROOT.TH1F("HT_E", "Event_HT_E", nbins, edges_HT)
    h_HLT_HT = ROOT.TH1F("HLT_HT", "HLT_HT", nbins, edges_HT)
    h_HLT_HT_muon = ROOT.TH1F("HLT_HLT_MU_OR", "HLT_HLT_MU_OR", nbins, edges_HT)
    h_HLT_HT_electron = ROOT.TH1F("HLT_HT_ELE_OR", "HLT_HLT_ELE_OR", nbins, edges_HT)
    h_electron_trigger_den = ROOT.TH1F("HLT_ELE_OR_den", "HLT_ELE_OR", nbins, edges)
    h_electron_trigger_num = ROOT.TH1F("HLT_ELE_OR_num", "HLT_ELE_OR", nbins, edges)
    h_muon_trigger_den = ROOT.TH1F("HLT_MU_OR_den", "HLT_MU_OR", nbins, edges)
    h_muon_trigger_num = ROOT.TH1F("HLT_MU_OR_num", "HLT_MU_OR", nbins, edges)

    h_HT_distr = ROOT.TH1F("HT_distr", "Event_HT", 500, 0., 5000.)

    #histos muon
    h_drmin_ptrel_mu = ROOT.TH2F("h_drmin_ptrel_mu","DR_vs_pTrel_muon", 100, 0., 1.5, 100, 0., 100.)
    h_drmin_mu = ROOT.TH1F("h_drmin_mu","DR_muon", 100, 0., 1.5)
    h_MET_mu = ROOT.TH1F("h_MET_mu", "MET_distribution_muon", 100, 0, 500)
    h_leadingjet_mu = ROOT.TH1F("h_leadingjet_mu", "leadingjet_muon", 200, 0, 1000)
    h_subleadingjet_mu = ROOT.TH1F("h_subleadingjet_mu", "subleadingjet_muon", 200, 0, 1000)
    h_muonpt = ROOT.TH1F("h_muonpt", "muon_pt_distribution", nbins, edges)
    h_muonpt_miniiso_medium = ROOT.TH1F("h_muonpt_miniisoMedium", "MiniIsoMedium;muon_pt", nbins, edges)
    h_muonpt_miniiso_tight = ROOT.TH1F("h_muonpt_miniisotight", "MiniIsoTight;muon_pt", nbins, edges)
    h_muonpt_miniiso_medium_false = ROOT.TH1F("h_muonpt_miniisoMedium_false", "MiniIsoMedium;muon_pt", nbins, edges)
    h_muonpt_miniiso_tight_false = ROOT.TH1F("h_muonpt_miniisotight_false", "MiniIsoTight;muon_pt", nbins, edges)
    h_miniiso_muon_matched = ROOT.TH1F("h_muon_miniiso_matched", "Muon_miniiso_right; miniiso; Events/bin", 100, 0., 1.)
    h_miniiso_muon_nomatched = ROOT.TH1F("h_muon_miniiso_nomatched", "Muon_miniiso_wrong; miniiso; Events/bin", 100, 0., 1.)
    h_miniiso_pt_muon_matched = ROOT.TH2F("h_muon_miniiso_pt_matched", "Muon_miniiso_pt_right; miniiso; Muon pt [GeV]", 100, 0., .4, 200, 0, 1000)
    h_miniiso_pt_muon_nomatched = ROOT.TH2F("h_muon_miniiso_pt_nomatched", "Muon_miniiso_pt_wrong; miniiso; Muon pt [GeV]", 100, 0., .4, 200, 0, 1000)
    #histos electron
    h_drmin_ptrel_e = ROOT.TH2F("h_drmin_ptrel_e","DR_vs_pTrel_electron", 100, 0., 1.5, 100, 0., 100.)
    h_MET_e = ROOT.TH1F("h_MET_e", "MET_distribution_electron", 100, 0, 500)
    h_leadingjet_e = ROOT.TH1F("h_leadingjet_e", "leadingjet_electron", 200, 0, 1000)
    h_subleadingjet_e = ROOT.TH1F("h_subleadingjet_e", "subleadingjet_electron", 200, 0, 1000)
    h_electronpt = ROOT.TH1F("h_electronpt", "electron_pt_distribution", 100, 0, 500)
    h_electroneta = ROOT.TH1F("h_electroneta", "Electron_eta_distribution; #eta; Events/bin", 100, -3., 3.)
    h_miniiso_electron_matched = ROOT.TH1F("h_electron_miniiso_matched", "Electron_miniiso_right; miniiso; Events/bin", 100, 0., 1.)
    h_miniiso_electron_nomatched = ROOT.TH1F("h_electron_miniiso_nomatched", "Electron_miniiso_wrong; miniiso; Events/bin", 100, 0., 1.)
    h_miniiso_pt_electron_matched = ROOT.TH2F("h_electron_miniiso_pt_matched", "Electron_miniiso_pt_right; miniiso; Electron pt [GeV]", 100, 0., .4, 200, 0, 1000)
    h_miniiso_pt_electron_nomatched = ROOT.TH2F("h_electron_miniiso_pt_nomatched", "Electron_miniiso_pt_wrong; miniiso; Electron pt [GeV]", 100, 0., .4, 200, 0, 1000)
    #histos jets
    h_btag_den = ROOT.TH1F("btag_den", "b tagging efficiency", nbins, edges)
    h_mistag_den = ROOT.TH1F("mistag_den", "mis-tagging efficiency", nbins, edges)
    h_btag_DeepCSV_T_num = ROOT.TH1F("btag_DeepCSV_T_num", "b tagging efficiency", nbins, edges)
    h_btag_DeepFlv_T_num = ROOT.TH1F("btag_DeepFlv_T_num", "b tagging efficiency", nbins, edges)
    h_mistag_DeepCSV_T_num = ROOT.TH1F("mistag_DeepCSV_T_num", "b tagging efficiency", nbins, edges)
    h_mistag_DeepFlv_T_num = ROOT.TH1F("mistag_DeepFlv_T_num", "b tagging efficiency", nbins, edges)
    h_btag_DeepCSV_M_num = ROOT.TH1F("btag_DeepCSV_M_num", "b tagging efficiency", nbins, edges)
    h_btag_DeepFlv_M_num = ROOT.TH1F("btag_DeepFlv_M_num", "b tagging efficiency", nbins, edges)
    h_mistag_DeepCSV_M_num = ROOT.TH1F("mistag_DeepCSV_M_num", "b tagging efficiency", nbins, edges)
    h_mistag_DeepFlv_M_num = ROOT.TH1F("mistag_DeepFlv_M_num", "b tagging efficiency", nbins, edges)
    h_btag_DeepCSV_L_num = ROOT.TH1F("btag_DeepCSV_L_num", "b tagging efficiency", nbins, edges)
    h_btag_DeepFlv_L_num = ROOT.TH1F("btag_DeepFlv_L_num", "b tagging efficiency", nbins, edges)
    h_mistag_DeepCSV_L_num = ROOT.TH1F("mistag_DeepCSV_L_num", "b tagging efficiency", nbins, edges)
    h_mistag_DeepFlv_L_num = ROOT.TH1F("mistag_DeepFlv_L_num", "b tagging efficiency", nbins, edges)

    badflag = 0 
    badevt = 0

    mumatch_iso0p1_pt_50 = 0.
    mumatch_iso0p1_pt_75 = 0.
    mumatch_iso0p1_pt_100 = 0.
    mumatch_iso0p1_pt_125 = 0.
    mumatch_iso0p2_pt_50 = 0.
    mumatch_iso0p2_pt_75 = 0.   
    mumatch_iso0p2_pt_100 = 0.    
    mumatch_iso0p2_pt_125 = 0.    
    elematch_iso0p1_pt_50 = 0.    
    elematch_iso0p1_pt_75 = 0.    
    elematch_iso0p1_pt_100 = 0.    
    elematch_iso0p1_pt_125 = 0.    
    elematch_iso0p2_pt_50 = 0.
    elematch_iso0p2_pt_75 = 0.   
    elematch_iso0p2_pt_100 = 0.    
    elematch_iso0p2_pt_125 = 0.

    munomatch_iso0p1_pt_50 = 0.    
    munomatch_iso0p1_pt_75 = 0.    
    munomatch_iso0p1_pt_100 = 0.    
    munomatch_iso0p1_pt_125 = 0.    
    munomatch_iso0p2_pt_50 = 0.    
    munomatch_iso0p2_pt_75 = 0.    
    munomatch_iso0p2_pt_100 = 0.    
    munomatch_iso0p2_pt_125 = 0.    
    elenomatch_iso0p1_pt_50 = 0.    
    elenomatch_iso0p1_pt_75 = 0.    
    elenomatch_iso0p1_pt_100 = 0.    
    elenomatch_iso0p1_pt_125 = 0.    
    elenomatch_iso0p2_pt_50 = 0.
    elenomatch_iso0p2_pt_75 = 0.  
    elenomatch_iso0p2_pt_100 = 0.    
    elenomatch_iso0p2_pt_125 = 0.

    totalMCmu = 0.
    totalMCele = 0.
    totalnoMCmu = 0.
    totalnoMCele = 0.
    
    total_mu_ptrel_drmin = 0.
    good_mu_ptrel_drmin = 0.
    total_ele_ptrel_drmin = 0.
    good_ele_ptrel_drmin = 0.

    # bool flags
    dominiisoscan = False
    trigger = True

    if not (dominiisoscan):
        totalMCmu = 1.
        totalMCele = 1.
        totalnoMCmu = 1.
        totalnoMCele = 1.
        total_mu_ptrel_drmin = 1.
        good_mu_ptrel_drmin = 1.
        total_ele_ptrel_drmin = 1.
        good_ele_ptrel_drmin = 1.


    for i in xrange(0,tree.GetEntries()):
    #for i in xrange(0,20):
        event = Event(tree,i)
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        fatjets = Collection(event, "FatJet")
        PV = Object(event, "PV")
        met = Object(event, "MET")
        HLT = Object(event, "HLT")
        Flag = Object(event, 'Flag')

        if trigger:
            isGoodPV = (PV.ndof>4 and abs(PV.z)<20 and math.hypot(PV.x, PV.y)<2) #basic requirements on the PV's goodness
            if(pass_MET(Flag) and isGoodPV):
                VetoMu = get_LooseMu(muons)
                goodMu = get_Mu(muons)
                VetoEle = get_LooseEle(electrons)
                goodEle = get_Ele(electrons)
                if(HLT.Mu50 or HLT.TkMu50):
                    if len(VetoMu) == 0 and len(VetoEle) == 0 and len(list(filter(lambda x : x.miniPFRelIso_all < 0.1, goodEle))) == 1:
                        for ele in list(filter(lambda x : x.miniPFRelIso_all < 0.1, goodEle)):
                            h_electron_trigger_den.Fill(ele.pt)
                            if(HLT.PFHT800 or HLT.PFHT900 or HLT.Ele115_CaloIdVT_GsfTrkIdT): 
                                h_electron_trigger_num.Fill(ele.pt)
                if(HLT.Ele115_CaloIdVT_GsfTrkIdT):
                    if len(VetoMu) == 0 and len(VetoEle) == 0 and len(list(filter(lambda x : x.miniPFRelIso_all < 0.1, goodMu))) == 1:
                        for muon in list(filter(lambda x : x.miniPFRelIso_all < 0.1, goodMu)):
                            h_muon_trigger_den.Fill(muon.pt)
                            if(HLT.PFHT800 or HLT.PFHT900 or HLT.Mu50 or HLT.TkMu50): 
                                h_muon_trigger_num.Fill(muon.pt)
        if not pass_MET(Flag):
            badflag += 1
            continue
        goodEvt, isMu, isEle = presel(PV, muons, electrons, jets)
        if goodEvt and isMu and isEle:
            print str(goodEvt) + ' ' + str(isMu) + ' ' + str(isEle) 
        if not goodEvt:
            badevt += 1
            continue
        HT = get_HT(jets)

        if isMu:
            if(dominiisoscan):
                totalMCmu,mumatch_iso0p1_pt_50,mumatch_iso0p1_pt_75,mumatch_iso0p1_pt_100,mumatch_iso0p1_pt_125,totalnoMCmu,munomatch_iso0p1_pt_50,munomatch_iso0p1_pt_75,munomatch_iso0p1_pt_100,munomatch_iso0p1_pt_125 = miniisoscan(isMu,0.1,muons)
                totalMCmu,mumatch_iso0p2_pt_50,mumatch_iso0p2_pt_75,mumatch_iso0p2_pt_100,mumatch_iso0p2_pt_125,totalnoMCmu,munomatch_iso0p2_pt_50,munomatch_iso0p2_pt_75,munomatch_iso0p2_pt_100,munomatch_iso0p2_pt_125 = miniisoscan(isMu,0.2,muons)
            for muon in muons:
                if(muon.genPartFlav == 1 or muon.genPartFlav == 15):
                    h_miniiso_muon_matched.Fill(muon.miniPFRelIso_all)
                    h_miniiso_pt_muon_matched.Fill(muon.miniPFRelIso_all, muon.pt)
                    h_muonpt.Fill(muon.pt)
                if not(isMC and (muon.genPartFlav == 1 or muon.genPartFlav == 15)):
                    h_miniiso_muon_nomatched.Fill(muon.miniPFRelIso_all)
                    h_miniiso_pt_muon_nomatched.Fill(muon.miniPFRelIso_all, muon.pt)
                if(muon.tightId==1 and muon.pt>50):
                    goodjets = get_Jet(jets, 15)
                    if len(goodjets)>0:
                        total_mu_ptrel_drmin += 1.
                        jet,drmin = closest(muon, goodjets)
                        ptrel = get_ptrel(muon, jet)
                        if(ptrel > 50 or drmin > 0.4):
                            good_mu_ptrel_drmin += 1.
                        #print str(ptrel) + ' dai TLorentz: ' + str(muon.p4().Vect().Perp(jet.p4().Vect()))
                        h_drmin_ptrel_mu.Fill(drmin,ptrel)
                        h_drmin_mu.Fill(drmin)
                    if((muon.miniIsoId == 2 or muon.miniIsoId == 3 or muon.miniIsoId == 4) and (isMC and (muon.genPartFlav == 1 or muon.genPartFlav == 15))):
                        h_muonpt_miniiso_medium.Fill(muon.pt)
                    if(muon.miniIsoId == 3 or muon.miniIsoId == 4 and (isMC and (muon.genPartFlav == 1 or muon.genPartFlav == 15))):
                        h_muonpt_miniiso_tight.Fill(muon.pt)
                    if((muon.miniIsoId == 2 or muon.miniIsoId == 3 or muon.miniIsoId == 4) and not(isMC and (muon.genPartFlav == 1 or muon.genPartFlav == 15))):
                        h_muonpt_miniiso_medium_false.Fill(muon.pt)
                    if(muon.miniIsoId == 3 or muon.miniIsoId == 4 and not (isMC and (muon.genPartFlav == 1 or muon.genPartFlav == 15))):
                        h_muonpt_miniiso_tight_false.Fill(muon.pt)
            h_leadingjet_mu.Fill(jets[0].pt)
            h_subleadingjet_mu.Fill(jets[1].pt)
            h_MET_mu.Fill(met.pt)
            h_muonpt_HLT.Fill(muons[0].pt)
            #print str(tree.HLT_Mu50)
            if(HLT.Mu50):
                h_HLT_Mu50.Fill(muons[0].pt)
            if(HLT.TkMu50):
                h_HLT_TkMu50.Fill(muons[0].pt)
            if(HLT.Mu50 or HLT.TkMu50):
                h_HLT.Fill(muons[0].pt)
                h_mu_HT_binned.Fill(HT)
            h_HT.Fill(HT)
            h_HT_mu.Fill(HT)
            if(HLT.PFHT800 or HLT.PFHT900):
                h_HLT_HT.Fill(HT)
            if(HLT.PFHT800 or HLT.PFHT900 or HLT.Mu50 or HLT.TkMu50):
                h_HLT_HT_muon.Fill(HT)

        #h_muonpt.Draw()
        if isEle:
            if(dominiisoscan):
                totalMCele,elematch_iso0p1_pt_50,elematch_iso0p1_pt_75,elematch_iso0p1_pt_100,elematch_iso0p1_pt_125,totalnoMCele,elenomatch_iso0p1_pt_50,elenomatch_iso0p1_pt_75,elenomatch_iso0p1_pt_100,elenomatch_iso0p1_pt_125 = miniisoscan(isEle,0.1,electrons)
                totalMCele,elematch_iso0p2_pt_50,elematch_iso0p2_pt_75,elematch_iso0p2_pt_100,elematch_iso0p2_pt_125,totalnoMCele,elenomatch_iso0p2_pt_50,elenomatch_iso0p2_pt_75,elenomatch_iso0p2_pt_100,elenomatch_iso0p2_pt_125 = miniisoscan(isEle,0.2,electrons)
            for electron in electrons:
                if(electron.genPartFlav == 1 or electron.genPartFlav == 15):
                    h_miniiso_electron_matched.Fill(electron.miniPFRelIso_all)
                    h_miniiso_pt_electron_matched.Fill(electron.miniPFRelIso_all, electron.pt)
                    h_electronpt.Fill(electron.pt)
                if not(isMC and (electron.genPartFlav == 1 or electron.genPartFlav == 15)):
                    h_miniiso_electron_nomatched.Fill(electron.miniPFRelIso_all)
                    h_miniiso_pt_electron_nomatched.Fill(electron.miniPFRelIso_all, electron.pt)
                if(electron.mvaFall17V2noIso_WP90 and electron.pt > 50):
                    goodjets = get_Jet(jets, 15)
                    if len(goodjets)>0:
                        jet,drmin = closest(electron, goodjets)
                        ptrel = get_ptrel(electron, jet)
                        total_ele_ptrel_drmin += 1.
                        if(ptrel > 60 or drmin > 0.4):
                            good_ele_ptrel_drmin += 1.
                        h_drmin_ptrel_e.Fill(drmin,ptrel)
                        h_electronpt.Fill(electron.pt)
                    h_electroneta.Fill(electron.eta)
            h_leadingjet_e.Fill(jets[0].pt)
            h_subleadingjet_e.Fill(jets[1].pt)
            h_MET_e.Fill(met.pt)
            h_electronpt_HLT.Fill(electrons[0].pt)
            #print str(tree.HLT_Mu50)
            if(HLT.Ele115_CaloIdVT_GsfTrkIdT):
                h_HLT_Ele115.Fill(electrons[0].pt)
                h_ele_HT_binned.Fill(HT)
            h_HT.Fill(HT)
            h_HT_ele.Fill(HT)
            if(HLT.PFHT800 or HLT.PFHT900):
                h_HLT_HT.Fill(HT)
            if(HLT.PFHT800 or HLT.PFHT900 or HLT.Ele115_CaloIdVT_GsfTrkIdT):
                h_HLT_HT_electron.Fill(HT)

        if isMu or isEle:
            for jet in jets:
                if(abs(jet.partonFlavour) == 5 and jet.hadronFlavour == 5):
                    h_btag_den.Fill(jet.pt)
                if(not abs(jet.partonFlavour) == 5 and not jet.hadronFlavour == 5):
                    h_mistag_den.Fill(jet.pt)
                if(jet.btagDeepB > deepCSV_L and abs(jet.partonFlavour) == 5 and jet.hadronFlavour == 5):
                    h_btag_DeepCSV_L_num.Fill(jet.pt)
                if(jet.btagDeepB > deepCSV_L and not abs(jet.partonFlavour) == 5 and not jet.hadronFlavour == 5):
                    h_mistag_DeepCSV_L_num.Fill(jet.pt)
                if(jet.btagDeepFlavB > deepFlv_L and abs(jet.partonFlavour) == 5 and jet.hadronFlavour == 5):
                    h_btag_DeepFlv_L_num.Fill(jet.pt)
                if(jet.btagDeepFlavB > deepFlv_L and not abs(jet.partonFlavour) == 5 and not jet.hadronFlavour == 5):
                    h_mistag_DeepFlv_L_num.Fill(jet.pt)
                if(jet.btagDeepB > deepCSV_M and abs(jet.partonFlavour) == 5 and jet.hadronFlavour == 5):
                    h_btag_DeepCSV_M_num.Fill(jet.pt)
                if(jet.btagDeepB > deepCSV_M and not abs(jet.partonFlavour) == 5 and not jet.hadronFlavour == 5):
                    h_mistag_DeepCSV_M_num.Fill(jet.pt)
                if(jet.btagDeepFlavB > deepFlv_M and abs(jet.partonFlavour) == 5 and jet.hadronFlavour == 5):
                    h_btag_DeepFlv_M_num.Fill(jet.pt)
                if(jet.btagDeepFlavB > deepFlv_M and not abs(jet.partonFlavour) == 5 and not jet.hadronFlavour == 5):
                    h_mistag_DeepFlv_M_num.Fill(jet.pt)
                if(jet.btagDeepB > deepCSV_T and abs(jet.partonFlavour) == 5 and jet.hadronFlavour == 5):
                    h_btag_DeepCSV_T_num.Fill(jet.pt)
                if(jet.btagDeepB > deepCSV_T and not abs(jet.partonFlavour) == 5 and not jet.hadronFlavour == 5):
                    h_mistag_DeepCSV_T_num.Fill(jet.pt)
                if(jet.btagDeepFlavB > deepFlv_T and abs(jet.partonFlavour) == 5 and jet.hadronFlavour == 5):
                    h_btag_DeepFlv_T_num.Fill(jet.pt)
                if(jet.btagDeepFlavB > deepFlv_T and not abs(jet.partonFlavour) == 5 and not jet.hadronFlavour == 5):
                    h_mistag_DeepFlv_T_num.Fill(jet.pt)
                
    print 'Total events: %d     ||     Bad MET flag events %d     ||     Bad events %d' %(tree.GetEntries(), badflag, badevt)
    print totalMCmu
    if (miniisoscan):
        print  ' %.2f percent and %.2f percent and %.2f percent and  %.2f ' %(mumatch_iso0p1_pt_50/totalMCmu*100, mumatch_iso0p1_pt_75/totalMCmu*100, mumatch_iso0p1_pt_100/totalMCmu*100, mumatch_iso0p1_pt_125/totalMCmu*100),
        print ' and %.2f percent and %.2f percent and %.2f percent and %.2f \\\\' %(mumatch_iso0p2_pt_50/totalMCmu*100, mumatch_iso0p2_pt_75/totalMCmu*100, mumatch_iso0p2_pt_100/totalMCmu*100, mumatch_iso0p2_pt_125/totalMCmu*100)
        print ' %.2f percent and %.2f percent and %.2f percent and %.2f '  %(munomatch_iso0p1_pt_50/totalnoMCmu*100, munomatch_iso0p1_pt_75/totalnoMCmu*100, munomatch_iso0p1_pt_100/totalnoMCmu*100, munomatch_iso0p1_pt_125/totalnoMCmu*100),
        print ' and %.2f percent and %.2f percent and %.2f percent and %.2f \\\\'  %(munomatch_iso0p2_pt_50/totalnoMCmu*100, munomatch_iso0p2_pt_75/totalnoMCmu*100, munomatch_iso0p2_pt_100/totalnoMCmu*100, munomatch_iso0p2_pt_125/totalnoMCmu*100)
        print ' %.2f percent and %.2f percent and %.2f percent and %.2f ' %(elematch_iso0p1_pt_50/totalMCele*100, elematch_iso0p1_pt_75/totalMCele*100, elematch_iso0p1_pt_100/totalMCele*100, elematch_iso0p1_pt_125/totalMCele*100),
        print ' and %.2f percent and %.2f percent and %.2f percent and %.2f \\\\' %(elematch_iso0p2_pt_50/totalMCele*100, elematch_iso0p2_pt_75/totalMCele*100, elematch_iso0p2_pt_100/totalMCele*100, elematch_iso0p2_pt_125/totalMCele*100)
        print ' %.2f percent and %.2f percent and %.2f percent and %.2f '  %(elenomatch_iso0p1_pt_50/totalnoMCele*100, elenomatch_iso0p1_pt_75/totalnoMCele*100, elenomatch_iso0p1_pt_100/totalnoMCele*100, elenomatch_iso0p1_pt_125/totalnoMCele*100),
        print ' and %.2f percent and %.2f percent and %.2f percent and %.2f \\\\'  %(elenomatch_iso0p2_pt_50/totalnoMCele*100, elenomatch_iso0p2_pt_75/totalnoMCele*100, elenomatch_iso0p2_pt_100/totalnoMCele*100, elenomatch_iso0p2_pt_125/totalnoMCele*100)
        print '2D cut muon %.2f electron %.2f \\\\'  %(good_mu_ptrel_drmin/total_mu_ptrel_drmin*100, good_ele_ptrel_drmin/total_ele_ptrel_drmin*100)
    print_hist(inpfile, plotpath, h_drmin_ptrel_mu, "COLZ",1)
    print_hist(inpfile, plotpath, h_drmin_mu)
    print_hist(inpfile, plotpath, h_leadingjet_mu)
    print_hist(inpfile, plotpath, h_subleadingjet_mu)
    print_hist(inpfile, plotpath, h_MET_mu)
    print_hist(inpfile, plotpath, h_muonpt)
    print_hist(inpfile, plotpath, h_drmin_ptrel_e, "COLZ",1)
    print_hist(inpfile, plotpath, h_leadingjet_e)
    print_hist(inpfile, plotpath, h_subleadingjet_e)
    print_hist(inpfile, plotpath, h_MET_e)
    print_hist(inpfile, plotpath, h_electronpt)
    print_hist(inpfile, plotpath, h_electroneta)
    print_hist(inpfile, plotpath, h_HT)
    print_hist(inpfile, plotpath, h_ele_HT_binned)
    print_hist(inpfile, plotpath, h_mu_HT_binned)

    save_hist(inpfile, plotpath, h_drmin_ptrel_mu, "COLZ")
    save_hist(inpfile, plotpath, h_drmin_mu)
    save_hist(inpfile, plotpath, h_leadingjet_mu)
    save_hist(inpfile, plotpath, h_subleadingjet_mu)
    save_hist(inpfile, plotpath, h_MET_mu)
    save_hist(inpfile, plotpath, h_muonpt)
    save_hist(inpfile, plotpath, h_drmin_ptrel_e, "COLZ")
    save_hist(inpfile, plotpath, h_leadingjet_e)
    save_hist(inpfile, plotpath, h_subleadingjet_e)
    save_hist(inpfile, plotpath, h_MET_e)
    save_hist(inpfile, plotpath, h_electronpt)
    save_hist(inpfile, plotpath, h_electroneta)
    save_hist(inpfile, plotpath, h_HT)
    save_hist(inpfile, plotpath, h_miniiso_electron_nomatched)
    save_hist(inpfile, plotpath, h_miniiso_electron_matched)

    save_hist(inpfile, plotpath, h_miniiso_pt_electron_nomatched, "COLZ")
    save_hist(inpfile, plotpath, h_miniiso_pt_electron_matched, "COLZ")
    print_hist(inpfile, plotpath, h_miniiso_pt_electron_nomatched, "COLZ", 1)
    print_hist(inpfile, plotpath, h_miniiso_pt_electron_matched, "COLZ", 1)

    save_hist(inpfile, plotpath, h_miniiso_pt_muon_nomatched, "COLZ")
    save_hist(inpfile, plotpath, h_miniiso_pt_muon_matched, "COLZ")
    print_hist(inpfile, plotpath, h_miniiso_pt_muon_nomatched, "COLZ", 1)
    print_hist(inpfile, plotpath, h_miniiso_pt_muon_matched, "COLZ", 1)

    h_miniiso_electron_nomatched.SetLineColor(ROOT.kRed)
    print_hist(inpfile, plotpath, [h_miniiso_electron_matched, h_miniiso_electron_nomatched])

    h_HLT_Mu50Eff = ROOT.TEfficiency(h_HLT_Mu50, h_muonpt_HLT)
    h_HLT_Mu50Eff.SetTitle("HLT_Mu50; muon_pt [GeV];#epsilon")
    h_HLT_Mu50Eff.SetLineColor(ROOT.kGreen)
    save_hist(inpfile, plotpath, h_HLT_Mu50Eff)
    print_hist(inpfile, plotpath, h_HLT_Mu50Eff, 'AP')
    h_HLT_TkMu50Eff = ROOT.TEfficiency(h_HLT_TkMu50, h_muonpt_HLT)
    h_HLT_TkMu50Eff.SetTitle("HLT_TkMu50; muon_pt [GeV];#epsilon")
    h_HLT_TkMu50Eff.SetLineColor(ROOT.kRed)
    save_hist(inpfile, plotpath, h_HLT_TkMu50Eff)
    print_hist(inpfile, plotpath, h_HLT_TkMu50Eff, 'AP')
    h_HLTEff = ROOT.TEfficiency(h_HLT, h_muonpt_HLT)
    h_HLTEff.SetTitle("HLT_Mu_OR; muon_pt [GeV];#epsilon")
    h_HLTEff.SetLineColor(ROOT.kBlue)
    save_hist(inpfile, plotpath, h_HLTEff)
    print_hist(inpfile, plotpath, h_HLTEff)
    print_hist(inpfile, plotpath, [h_HLT_Mu50Eff, h_HLT_TkMu50Eff, h_HLTEff], 'AP')

    h_miniiso_mediumEff = ROOT.TEfficiency(h_muonpt_miniiso_medium, h_muonpt)
    h_miniiso_mediumEff.SetTitle("MiniIsoMedium; muon_pt [GeV];#epsilon")
    h_miniiso_mediumEff.SetLineColor(ROOT.kRed)
    save_hist(inpfile, plotpath, h_miniiso_mediumEff)
    print_hist(inpfile, plotpath, h_miniiso_mediumEff)
    h_miniiso_tightEff = ROOT.TEfficiency(h_muonpt_miniiso_tight, h_muonpt)
    h_miniiso_tightEff.SetTitle("MiniIsoTight; muon_pt [GeV];#epsilon")
    h_miniiso_tightEff.SetLineColor(ROOT.kBlue)
    save_hist(inpfile, plotpath, h_miniiso_tightEff)
    print_hist(inpfile, plotpath, h_miniiso_tightEff)
    print_hist(inpfile, plotpath, [h_miniiso_mediumEff, h_miniiso_tightEff], 'AP')

    h_HLT_Ele115Eff = ROOT.TEfficiency(h_HLT_Ele115, h_electronpt_HLT)
    h_HLT_Ele115Eff.SetTitle("HLT_Ele115_CaloIdVT_GsfTrkIdT; electron_pt [GeV];#epsilon")
    save_hist(inpfile, plotpath, h_HLT_Ele115Eff)
    print_hist(inpfile, plotpath, h_HLT_Ele115Eff, 'AP')

    h_HLT_HTEff = ROOT.TEfficiency(h_HLT_HT, h_HT)
    h_HLT_HTEff.SetTitle("HLT_PFHT_800_OR_900; Event HT [GeV];#epsilon")
    h_HLT_HTEff.SetLineColor(ROOT.kBlue)
    save_hist(inpfile, plotpath, h_HLT_HTEff)
    print_hist(inpfile, plotpath, h_HLT_HTEff, 'AP')
    h_HLT_HT_muonEff = ROOT.TEfficiency(h_HLT_HT_muon, h_HT_mu)
    h_HLT_HT_muonEff.SetTitle("HLT_PFHT_800_OR_900_Muon_50; Event HT [GeV];#epsilon")
    h_HLT_HT_muonEff.SetLineColor(ROOT.kGreen)
    save_hist(inpfile, plotpath, h_HLT_HT_muonEff)
    print_hist(inpfile, plotpath, h_HLT_HT_muonEff, 'AP')
    h_HLT_HT_electronEff = ROOT.TEfficiency(h_HLT_HT_electron, h_HT_ele)
    h_HLT_HT_electronEff.SetTitle("HLT_PFHT_800_OR_900_Electron_115; Event HT [GeV];#epsilon")
    h_HLT_HT_electronEff.SetLineColor(ROOT.kRed)
    save_hist(inpfile, plotpath, h_HLT_HT_electronEff)
    print_hist(inpfile, plotpath, h_HLT_HT_electronEff, 'AP')
    print_hist(inpfile, plotpath, [h_HLT_HT_electronEff, h_HLT_HT_muonEff, h_HLT_HTEff], 'AP')

    #Lepton trigger efficiency in HT bins
    h_HLT_Muon_HTEff = ROOT.TEfficiency(h_mu_HT_binned, h_HT_mu)
    h_HLT_Muon_HTEff.SetTitle("HLT_Muon_50_HT_binned; Event HT [GeV];#epsilon")
    h_HLT_Muon_HTEff.SetLineColor(ROOT.kBlue)
    save_hist(inpfile, plotpath, h_HLT_Muon_HTEff)
    print_hist(inpfile, plotpath, h_HLT_Muon_HTEff, 'AP')
    h_HLT_Electron_HTEff = ROOT.TEfficiency(h_ele_HT_binned, h_HT_ele)
    h_HLT_Electron_HTEff.SetTitle("HLT_Electron_115_HT_binned; Event HT [GeV];#epsilon")
    h_HLT_Electron_HTEff.SetLineColor(ROOT.kBlue)
    save_hist(inpfile, plotpath, h_HLT_Electron_HTEff)
    print_hist(inpfile, plotpath, h_HLT_Electron_HTEff, 'AP')
    #trigger in dileptonic ttbar
    h_HLT_Electron_pt_dilepEff = ROOT.TEfficiency(h_electron_trigger_num, h_electron_trigger_den)
    h_HLT_Electron_pt_dilepEff.SetTitle("HLT_Electron_115_pt_binned_dilep; Electron pt [GeV]; #epsilon")
    h_HLT_Electron_pt_dilepEff.SetLineColor(ROOT.kBlue)
    save_hist(inpfile, plotpath, h_HLT_Electron_pt_dilepEff)
    print_hist(inpfile, plotpath, h_HLT_Electron_pt_dilepEff, 'AP')
    h_HLT_Muon_pt_dilepEff = ROOT.TEfficiency(h_muon_trigger_num, h_muon_trigger_den)
    h_HLT_Muon_pt_dilepEff.SetTitle("HLT_Muon_115_pt_binned_dilep; Muon pt [GeV]; #epsilon")
    h_HLT_Muon_pt_dilepEff.SetLineColor(ROOT.kBlue)
    save_hist(inpfile, plotpath, h_HLT_Muon_pt_dilepEff)
    print_hist(inpfile, plotpath, h_HLT_Muon_pt_dilepEff, 'AP')

    h_btag_DeepCSV_L_Eff = ROOT.TEfficiency(h_btag_DeepCSV_L_num, h_btag_den)
    h_btag_DeepCSV_L_Eff.SetTitle("btag_DeepCSV_L_Efficiency; b-jet pt [GeV]; #epsilon")
    h_btag_DeepCSV_L_Eff.SetLineColor(ROOT.kBlue)
    save_hist(inpfile, plotpath, h_btag_DeepCSV_L_Eff)
    print_hist(inpfile, plotpath, h_btag_DeepCSV_L_Eff, 'AP')
    h_btag_DeepCSV_M_Eff = ROOT.TEfficiency(h_btag_DeepCSV_M_num, h_btag_den)
    h_btag_DeepCSV_M_Eff.SetTitle("btag_DeepCSV_M_Efficiency; b-jet pt [GeV]; #epsilon")
    h_btag_DeepCSV_M_Eff.SetLineColor(ROOT.kGreen)
    save_hist(inpfile, plotpath, h_btag_DeepCSV_M_Eff)
    print_hist(inpfile, plotpath, h_btag_DeepCSV_M_Eff, 'AP')
    h_btag_DeepCSV_T_Eff = ROOT.TEfficiency(h_btag_DeepCSV_T_num, h_btag_den)
    h_btag_DeepCSV_T_Eff.SetTitle("btag_DeepCSV_T_Efficiency; b-jet pt [GeV]; #epsilon")
    h_btag_DeepCSV_T_Eff.SetLineColor(ROOT.kRed)
    save_hist(inpfile, plotpath, h_btag_DeepCSV_T_Eff)
    print_hist(inpfile, plotpath, h_btag_DeepCSV_T_Eff, 'AP')
    print_hist(inpfile, plotpath, [h_btag_DeepCSV_T_Eff, h_btag_DeepCSV_M_Eff, h_btag_DeepCSV_L_Eff], 'AP')

    h_mistag_DeepCSV_L_Eff = ROOT.TEfficiency(h_mistag_DeepCSV_L_num, h_mistag_den)
    h_mistag_DeepCSV_L_Eff.SetTitle("mistag_DeepCSV_L_Efficiency; b-jet pt [GeV]; #epsilon")
    h_mistag_DeepCSV_L_Eff.SetLineColor(ROOT.kBlue)
    save_hist(inpfile, plotpath, h_mistag_DeepCSV_L_Eff)
    print_hist(inpfile, plotpath, h_mistag_DeepCSV_L_Eff, 'AP')
    h_mistag_DeepCSV_M_Eff = ROOT.TEfficiency(h_mistag_DeepCSV_M_num, h_mistag_den)
    h_mistag_DeepCSV_M_Eff.SetTitle("mistag_DeepCSV_M_Efficiency; b-jet pt [GeV]; #epsilon")
    h_mistag_DeepCSV_M_Eff.SetLineColor(ROOT.kGreen)
    save_hist(inpfile, plotpath, h_mistag_DeepCSV_M_Eff)
    print_hist(inpfile, plotpath, h_mistag_DeepCSV_M_Eff, 'AP')
    h_mistag_DeepCSV_T_Eff = ROOT.TEfficiency(h_mistag_DeepCSV_T_num, h_mistag_den)
    h_mistag_DeepCSV_T_Eff.SetTitle("mistag_DeepCSV_T_Efficiency; b-jet pt [GeV]; #epsilon")
    h_mistag_DeepCSV_T_Eff.SetLineColor(ROOT.kRed)
    save_hist(inpfile, plotpath, h_mistag_DeepCSV_T_Eff)
    print_hist(inpfile, plotpath, h_mistag_DeepCSV_T_Eff, 'AP')
    print_hist(inpfile, plotpath, [h_mistag_DeepCSV_T_Eff, h_mistag_DeepCSV_M_Eff, h_mistag_DeepCSV_L_Eff], 'AP')

    h_btag_DeepFlv_L_Eff = ROOT.TEfficiency(h_btag_DeepFlv_L_num, h_btag_den)
    h_btag_DeepFlv_L_Eff.SetTitle("btag_DeepFlv_L_Efficiency; b-jet pt [GeV]; #epsilon")
    h_btag_DeepFlv_L_Eff.SetLineColor(ROOT.kBlue)
    save_hist(inpfile, plotpath, h_btag_DeepFlv_L_Eff)
    print_hist(inpfile, plotpath, h_btag_DeepFlv_L_Eff, 'AP')
    h_btag_DeepFlv_M_Eff = ROOT.TEfficiency(h_btag_DeepFlv_M_num, h_btag_den)
    h_btag_DeepFlv_M_Eff.SetTitle("btag_DeepFlv_M_Efficiency; b-jet pt [GeV]; #epsilon")
    h_btag_DeepFlv_M_Eff.SetLineColor(ROOT.kGreen)
    save_hist(inpfile, plotpath, h_btag_DeepFlv_M_Eff)
    print_hist(inpfile, plotpath, h_btag_DeepFlv_M_Eff, 'AP')
    h_btag_DeepFlv_T_Eff = ROOT.TEfficiency(h_btag_DeepFlv_T_num, h_btag_den)
    h_btag_DeepFlv_T_Eff.SetTitle("btag_DeepFlv_T_Efficiency; b-jet pt [GeV]; #epsilon")
    h_btag_DeepFlv_T_Eff.SetLineColor(ROOT.kRed)
    save_hist(inpfile, plotpath, h_btag_DeepFlv_T_Eff)
    print_hist(inpfile, plotpath, h_btag_DeepFlv_T_Eff, 'AP')
    print_hist(inpfile, plotpath, [h_btag_DeepFlv_T_Eff, h_btag_DeepFlv_M_Eff, h_btag_DeepFlv_L_Eff], 'AP')

    h_mistag_DeepFlv_L_Eff = ROOT.TEfficiency(h_mistag_DeepFlv_L_num, h_mistag_den)
    h_mistag_DeepFlv_L_Eff.SetTitle("mistag_DeepFlv_L_Efficiency; b-jet pt [GeV]; #epsilon")
    h_mistag_DeepFlv_L_Eff.SetLineColor(ROOT.kBlue)
    save_hist(inpfile, plotpath, h_mistag_DeepFlv_L_Eff)
    print_hist(inpfile, plotpath, h_mistag_DeepFlv_L_Eff, 'AP')
    h_mistag_DeepFlv_M_Eff = ROOT.TEfficiency(h_mistag_DeepFlv_M_num, h_mistag_den)
    h_mistag_DeepFlv_M_Eff.SetTitle("mistag_DeepFlv_M_Efficiency; b-jet pt [GeV]; #epsilon")
    h_mistag_DeepFlv_M_Eff.SetLineColor(ROOT.kGreen)
    save_hist(inpfile, plotpath, h_mistag_DeepFlv_M_Eff)
    print_hist(inpfile, plotpath, h_mistag_DeepFlv_M_Eff, 'AP')
    h_mistag_DeepFlv_T_Eff = ROOT.TEfficiency(h_mistag_DeepFlv_T_num, h_mistag_den)
    h_mistag_DeepFlv_T_Eff.SetTitle("mistag_DeepFlv_T_Efficiency; b-jet pt [GeV]; #epsilon")
    h_mistag_DeepFlv_T_Eff.SetLineColor(ROOT.kRed)
    save_hist(inpfile, plotpath, h_mistag_DeepFlv_T_Eff)
    print_hist(inpfile, plotpath, h_mistag_DeepFlv_T_Eff, 'AP')
    print_hist(inpfile, plotpath, [h_mistag_DeepFlv_T_Eff, h_mistag_DeepFlv_M_Eff, h_mistag_DeepFlv_L_Eff], 'AP')
