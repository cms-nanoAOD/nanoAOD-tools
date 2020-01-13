import ROOT
import math
from array import array
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *
from PhysicsTools.NanoAODTools.postprocessing.framework.preskimming import preSkim

inputpath = "/eos/home-a/adeiorio/Wprime/nosynch/" 
inpfiles = ["Wprime_4000_RH"
#            ,"TT_Mtt-700to1000"
            #"WJets",
            #,"QCD_Pt_600to800_1"
            #"SingleMuon_Run2016G_1"
        ]

#ROOT.gROOT.SetStyle('Plain')
#ROOT.gStyle.SetPalette(1)
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch()        # don't pop up canvases                                                                                                                                              
ROOT.TH1.SetDefaultSumw2()
#ROOT.TGaxis.SetMaxDigits(3)

def pass_MET(flag): #returns the True if the event pass the MET Filter requiriments otherwise False
    return flag.goodVertices and flag.globalSuperTightHalo2016Filter and flag.HBHENoiseFilter and flag.HBHENoiseIsoFilter and flag.EcalDeadCellTriggerPrimitiveFilter and flag.BadPFMuonFilter

def get_Mu(muons): #returns a collection of muons that pass the selection performed by the filter function
    return list(filter(lambda x : x.tightId and abs(x.eta) < 2.4, muons))

def get_LooseMu(muons): #returns a collection of muons that pass the selection performed by the filter function
    return list(filter(lambda x : x.looseId and not x.tightId and x.pt > 35 and abs(x.eta) < 2.4, muons))

def get_Ele(electrons): #returns a collection of electrons that pass the selection performed by the filter function
    return list(filter(lambda x : x.mvaFall17V2noIso_WP90 and abs(x.eta) < 1.4442 and abs(x.eta) > 1.566 and abs(x.eta) < 2.5, electrons))

def get_LooseEle(electrons): #returns a collection of electrons that pass the selection performed by the filter function
    return list(filter(lambda x : x.mvaFall17V2noIso_WPL and not x.mvaFall17V2noIso_WP90 and abs(x.eta) < 1.4442 and abs(x.eta) > 1.566 and x.pt > 35 and abs(x.eta) < 2.5, electrons))

def get_Jet(jets, pt): #returns a collection of jets that pass the selection performed by the filter function
    return list(filter(lambda x : x.jetId >= 2 and abs(x.eta) < 2.4 and x.pt > pt, jets))
 
def presel(PV, muons, electrons, jet): #returns three booleans: goodEvent assure the presence of at least a good lepton vetoing the presence of additional loose leptons, goodMuEvt is for good muon event, goodEleEvt is for good muon event   
    isGoodPV = (PV.ndof>4 and abs(PV.z)<20 and math.hypot(PV.x, PV.y)<2) #basic requirements on the PV's goodness
    VetoMu = get_LooseMu(muons)
    goodMu = get_Mu(muons)
    VetoEle = get_LooseEle(electrons)
    goodEle = get_Ele(electrons)
    goodJet = get_Jet(jets, 25)

    isGoodEvent = ((((len(goodMu) >= 1) and (len(goodEle) == 0)) or ((len(goodMu) == 0) and (len(goodEle) >= 1))) and len(VetoMu) == 0 and len(VetoEle) == 0 and len(goodJet) >= 2)
    isMuon = (len(goodMu) >= 1) and (len(goodEle) == 0) and len(VetoMu) == 0 and len(VetoEle) == 0 and len(goodJet) >= 2
    isElectron = (len(goodMu) == 0) and (len(goodEle) >= 1) and len(VetoMu) == 0 and len(VetoEle) == 0 and len(goodJet) >= 2
    goodEvent = isGoodPV and isGoodEvent
    goodMuEvt = isGoodPV and isMuon
    goodEleEvt = isGoodPV and isElectron
    return goodEvent, goodMuEvt, goodEleEvt

def print_hist(infile, hist, option = "HIST"):
    plotpath = "./plots/"
    if not(isinstance(hist, list)):
        c1 = ROOT.TCanvas(infile + "_" + hist.GetTitle(), "c1", 50,50,700,600)
        hist.Draw(option)
        c1.Print(plotpath + infile + "_" + hist.GetTitle() + ".png")
        c1.Print(plotpath + infile + "_" + hist.GetTitle() + ".root")
    else:
        c1 = ROOT.TCanvas(infile + "_" + hist[0].GetTitle() + '_comparison', "c1", 50,50,700,600)
        for h in hist:
            h.Draw(option+'SAME')
        c1.BuildLegend()
        c1.Print(plotpath + infile + "_" + hist[0].GetTitle() + '_comparison' + ".png")
        c1.Print(plotpath + infile + "_" + hist[0].GetTitle() + '_comparison' + ".root")

def save_hist(infile, hist, option = "HIST"):
     fout = ROOT.TFile.Open("./plots/"+ infile +".root", "UPDATE")
     fout.cd()
     hist.Write()
     fout.Close()

for inpfile in inpfiles:
    infile = ROOT.TFile.Open(inputpath + inpfile + ".root")
    tree = InputTree(infile.Events)

    #histogram booking
    nbins = 15
    nmin = 0
    nmax = 400
    edges = array('f',[0., 20., 40., 60., 80., 100., 130., 160., 190., 230., 270., 320., 360., 400., 700.,1000.])
    h_muonpt_HLT = ROOT.TH1F("Muon_pt", "Muon_pt", nbins, edges)
    h_HLT_Mu50 = ROOT.TH1F("HLT_Mu50", "HLT_Mu50", nbins, edges)
    h_HLT_TkMu50 = ROOT.TH1F("HLT_TkMu50", "HLT_TkMu50", nbins, edges)
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

    badflag = 0 
    badevt = 0
    
    for i in xrange(0,tree.GetEntries()):
    #for i in xrange(0,10):
        event = Event(tree,i)
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        fatjets = Collection(event, "FatJet")
        PV = Object(event, "PV")
        met = Object(event, "MET")
        HLT = Object(event, "HLT")
        Flag = Object(event, 'Flag')
        goodMu = []
        goodEle = []
        goodJet = []
        if not pass_MET(Flag):
            badflag += 1
            continue
        goodEvt, isMu, isEle = presel(PV, muons, electrons, jets)
        if goodEvt and isMu and isEle:
            print str(goodEvt) + ' ' + str(isMu) + ' ' + str(isEle) 
        if not goodEvt:
            badevt += 1
            continue
        if isMu:
            for muon in muons:
                if(muon.tightId==1 and muon.pt>50):
                    goodjets = get_Jet(jets, 35)
                    if len(goodjets)>0:
                        jet,drmin = closest(muon, goodjets)
                        ptrel = (jet.p4().Vect().Cross(muon.p4().Vect())).Mag()/muon.p4().Vect().Mag()
                        h_drmin_ptrel_mu.Fill(drmin,ptrel)
                        h_drmin_mu.Fill(drmin)
                        h_leadingjet_mu.Fill(jets[0].pt)
                        h_subleadingjet_mu.Fill(jets[1].pt)
                        h_MET_mu.Fill(met.pt)
                        h_muonpt.Fill(muon.pt)
            h_muonpt_HLT.Fill(muons[0].pt)
            #print str(tree.HLT_Mu50)
            if(HLT.Mu50):
                h_HLT_Mu50.Fill(muons[0].pt)
            if(HLT.TkMu50):
                h_HLT_TkMu50.Fill(muons[0].pt)
            if(HLT.Mu50 or HLT.TkMu50):
                h_HLT.Fill(muons[0].pt)

        #h_muonpt.Draw()
        if isEle:
            for electron in electrons:
                if(electron.mvaFall17V2noIso_WP90 and (electron.genPartFlav==15 or electron.genPartFlav==1)):
                    goodjets = get_Jet(jets, 35)
                    if len(goodjets)>0:
                        jet,drmin = closest(muon, goodjets)
                        ptrel = (jet.p4().Vect().Cross(electron.p4().Vect())).Mag()/electron.p4().Vect().Mag()
                        h_drmin_ptrel_e.Fill(drmin,ptrel)
                        h_leadingjet_e.Fill(jets[0].pt)
                        h_subleadingjet_e.Fill(jets[1].pt)
                        h_MET_e.Fill(met.pt)
                        h_electronpt.Fill(electron.pt)

    print 'Total events: %d     ||     Bad MET flag events %d     ||     Bad events %d' %(tree.GetEntries(), badflag, badevt)
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

    h_HLT_Mu50.Sumw2()
    h_HLT_Mu50.Divide(h_muonpt_HLT)
    h_HLT_Mu50.SetLineColor(ROOT.kGreen)
    save_hist(inpfile, h_HLT_Mu50)
    print_hist(inpfile, h_HLT_Mu50)
    h_HLT_TkMu50.Sumw2()
    h_HLT_TkMu50.Divide(h_muonpt_HLT)
    h_HLT_TkMu50.SetLineColor(ROOT.kBlack)
    save_hist(inpfile, h_HLT_TkMu50)
    print_hist(inpfile, h_HLT_TkMu50)
    h_HLT.Sumw2()
    h_HLT.Divide(h_muonpt_HLT)
    #h_HLT.SetLineColor(ROOT.kYellow+2)
    save_hist(inpfile, h_HLT)
    print_hist(inpfile, h_HLT)
    print_hist(inpfile, [h_HLT_Mu50, h_HLT_TkMu50, h_HLT], 'E')

