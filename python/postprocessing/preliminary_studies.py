import ROOT
import math
from array import array
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *

inputpath = "/eos/home-a/adeiorio/Wprime/nosynch/" 
inpfiles = ["Wprime_4000_RH",
            "TT_Mtt-700to1000",
            #"WJets",
            "QCD_Pt_600to800_1",
            "SingleMuon_Run2016G_1"]
#infile = ROOT.TFile.Open("/eos/home-a/adeiorio/Wprime/nosynch/.root")
#ROOT.gROOT.SetStyle('Plain')
#ROOT.gStyle.SetPalette(1)
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch()        # don't pop up canvases                                                                                                                                              
ROOT.TH1.SetDefaultSumw2()
#ROOT.TGaxis.SetMaxDigits(3)

def presel(PV, muons, electrons, jet):
    isVetoMu = False
    isVetoEle = False
    isGoodPV = (PV.ndof>4 and abs(PV.z)<20 and math.hypot(PV.x, PV.y)<2)
    for lep in muons:
        if(not(lep.tightId) and lep.looseId and lep.pt>35 and abs(lep.eta)<2.4):
            isVetoMu = True
        if(not(lep.tightId and lep.genPartIdx)):
            continue
        goodMu.append(lep)
    for lep in electrons:
        if(abs(lep.eta) > 1.4442 and abs(lep.eta) < 1.566):
            continue
        if(not(lep.mvaFall17V2noIso_WP90) and lep.mvaFall17V2noIso_WPL and lep.pt>35 and abs(lep.eta)<2.5):
            isVetoEle = True
        if(not(lep.mvaFall17V2noIso_WP90)):
            continue
        goodEle.append(lep)
    for j in jets:
        if abs(j.eta)<2.4 and j.pt>25:
            goodJet.append(j)

    isGoodEvent = ((((len(goodMu) >= 1) and (len(goodEle) == 0)) or ((len(goodMu) == 0) and (len(goodEle) >= 1))) and not isVetoMu and not isVetoEle and len(goodJet)>=2)
    goodEvent = isGoodPV and isGoodEvent
    return goodEvent

def print_hist(infile, hist, option = "HIST"):
    c1 = ROOT.TCanvas(infile + "_" + hist.GetTitle(), "c1", 50,50,700,600)
    hist.Draw(option)
    plotpath = "./plots/"
    c1.Print(plotpath + infile + "_" + hist.GetTitle() + ".png")
    c1.Print(plotpath + infile + "_" + hist.GetTitle() + ".root")

def save_hist(infile, hist, option = "HIST"):
     fout = ROOT.TFile.Open("./plots/"+ infile +".root", "UPDATE")
     fout.cd()
     hist.Write()
     fout.Close()

for inpfile in inpfiles:
    infile = ROOT.TFile.Open(inputpath + inpfile + ".root")
    tree = InputTree(infile.Events)

    #histogram booking
    nbins = 13
    nmin = 0
    nmax = 400
    edges = array('f',[0., 20., 40., 60., 80., 100., 130., 160., 190., 230., 270., 320., 360., 400.])
    h_muonpt_HLT = ROOT.TH1F("Muon_pt", "Muon_pt", nbins, edges)
    h_HLT_Mu50 = ROOT.TH1F("HLT_Mu50", "HLT_Mu50", nbins, edges)
    h_HLT_Mu55 = ROOT.TH1F("HLT_Mu55", "HLT_Mu55", nbins, edges)
    h_HLT_TkMu100 = ROOT.TH1F("HLT_TkMu100", "HLT_TkMu50", nbins, edges)
    h_HLT = ROOT.TH1F("HLT_OR", "HLT_OR", nbins, edges)
    ##histos muon
    h_drmin_ptrel_mu = ROOT.TH2F("h_drmin_ptrel_mu","DR_vs_pTrel_muon", 100, 0., 1.5, 100, 0., 300.)
    h_drmin_mu = ROOT.TH1F("h_drmin_mu","DR_muon", 100, 0., 1.5)
    h_MET_mu = ROOT.TH1F("h_MET_mu", "MET_distribution_muon", 100, 0, 500)
    h_leadingjet_mu = ROOT.TH1F("h_leadingjet_mu", "leadingjet_muon", 200, 0, 1000)
    h_subleadingjet_mu = ROOT.TH1F("h_subleadingjet_mu", "subleadingjet_muon", 200, 0, 1000)
    h_muonpt = ROOT.TH1F("h_muonpt", "muon_pt_distribution", 100, 0, 500)
    ##histos electron
    h_drmin_ptrel_e = ROOT.TH2F("h_drmin_ptrel_e","DR_vs_pTrel_electron", 100, 0., 1.5, 100, 0., 300.)
    h_MET_e = ROOT.TH1F("h_MET_e", "MET_distribution_electron", 100, 0, 500)
    h_leadingjet_e = ROOT.TH1F("h_leadingjet_e", "leadingjet_electron", 200, 0, 1000)
    h_subleadingjet_e = ROOT.TH1F("h_subleadingjet_e", "subleadingjet_electron", 200, 0, 1000)
    h_electronpt = ROOT.TH1F("h_electronpt", "electron_pt_distribution", 100, 0, 500)

    
    for i in xrange(0,tree.GetEntries()):
    #for i in xrange(0,10):
        event = Event(tree,i)
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        fatjets = Collection(event, "FatJet")
        PV = Object(event, "PV")
        met = Object(event, "MET")
        goodMu = []
        goodEle = []
        goodJet = []
        if not presel(PV, muons, electrons, jets):
            continue
        for muon in muons:
            if(muon.tightId==1 and muon.pt>50 and muon.genPartFlav==15 or muon.genPartFlav==1):
                jet,drmin = closest(muon, filter(lambda x : x.pt > 25 and abs(x.eta)<2.4, jets))
                ptrel = (jet.p4().Vect().Cross(muon.p4().Vect())).Mag()/muon.p4().Vect().Mag()
                h_drmin_ptrel_mu.Fill(drmin,ptrel)
                h_drmin_mu.Fill(drmin)
                h_leadingjet_mu.Fill(jets[0].pt)
                h_subleadingjet_mu.Fill(jets[1].pt)
                h_MET_mu.Fill(met.pt)
                h_muonpt.Fill(muon.pt)

        for electron in electrons:
            jet,drmin = closest(electron, jets)
            ptrel = (jet.p4().Vect().Cross(electron.p4().Vect())).Mag()/electron.p4().Vect().Mag()
            h_drmin_ptrel_e.Fill(drmin,ptrel)
            h_leadingjet_e.Fill(jets[0].pt)
            h_subleadingjet_e.Fill(jets[1].pt)
            h_MET_e.Fill(met.pt)
            h_electronpt.Fill(electron.pt)

    print_hist(inpfile, h_drmin_ptrel_mu, "COLZ")
    print_hist(inpfile, h_drmin_mu)
    print_hist(inpfile, h_leadingjet_mu)
    print_hist(inpfile, h_subleadingjet_mu)
    print_hist(inpfile, h_MET_mu)
    print_hist(inpfile, h_muonpt)
    print_hist(inpfile, h_drmin_ptrel_e, "COLZ")
    print_hist(inpfile, h_leadingjet_e)
    print_hist(inpfile, h_subleadingjet_e)
    print_hist(inpfile, h_MET_e)
    print_hist(inpfile, h_electronpt)

    save_hist(inpfile, h_drmin_ptrel_mu, "COLZ")
    save_hist(inpfile, h_drmin_mu)
    save_hist(inpfile, h_leadingjet_mu)
    save_hist(inpfile, h_subleadingjet_mu)
    save_hist(inpfile, h_MET_mu)
    save_hist(inpfile, h_muonpt)
    save_hist(inpfile, h_drmin_ptrel_e, "COLZ")
    save_hist(inpfile, h_leadingjet_e)
    save_hist(inpfile, h_subleadingjet_e)
    save_hist(inpfile, h_MET_e)
    save_hist(inpfile, h_electronpt)

'''
            h_muonpt_HLT.Fill(muon.pt)
            if(tree.HLT_Mu50):
                h_HLT_Mu50.Fill(muon.pt)
            if(tree.HLT_Mu55):
                h_HLT_Mu55.Fill(muon.pt)
            if(tree.HLT_TkMu50):
                h_HLT_TkMu100.Fill(muon.pt)
            if(tree.HLT_Mu50 or tree.HLT_Mu55 or tree.HLT_TkMu50):
                h_HLT.Fill(muon.pt)
#h_muonpt.Draw()
h_HLT_Mu50.Sumw2()
h_HLT_Mu50.Divide(h_muonpt_HLT)
h_HLT_Mu50.SetLineColor(ROOT.kGreen)
h_HLT_Mu50.Draw("E")
h_HLT_Mu55.Sumw2()
h_HLT_Mu55.Divide(h_muonpt_HLT)
h_HLT_Mu55.SetLineColor(ROOT.kRed)
h_HLT_Mu55.Draw("ESAME")
h_HLT_TkMu100.Sumw2()
h_HLT_TkMu100.Divide(h_muonpt_HLT)
h_HLT_TkMu100.SetLineColor(ROOT.kBlack)
h_HLT_TkMu100.Draw("ESAME")
h_HLT.Sumw2()
h_HLT.Divide(h_muonpt_HLT)
h_HLT.SetLineColor(ROOT.kYellow+2)
h_HLT.Draw("ESAME")
'''
#c1.BuildLegend()

