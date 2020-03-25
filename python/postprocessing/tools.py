import ROOT
import copy as copy
from math import *
from array import array
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *
from PhysicsTools.NanoAODTools.postprocessing.framework.preskimming import preSkim

#ROOT.gROOT.SetStyle('Plain')
#ROOT.gStyle.SetPalette(1)
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch()        # don't pop up canvases                                                                                                                                              
ROOT.TH1.SetDefaultSumw2()
ROOT.TGaxis.SetMaxDigits(3)

colors = [ROOT.kBlue,
          ROOT.kBlack,
          ROOT.kRed,
          ROOT.kGreen+2,
          ROOT.kMagenta+2,
          ROOT.kAzure+6
]



#### ========= UTILITIES =======================
def deltaPhi(phi1,phi2):
    ## Catch if being called with two objects
    if type(phi1) != float and type(phi1) != int:
        phi1 = phi1.phi
    if type(phi2) != float and type(phi2) != int:
        phi2 = phi2.phi
    ## Otherwise
    dphi = (phi1-phi2)
    while dphi >  pi: dphi -= 2*pi
    while dphi < -pi: dphi += 2*pi
    return dphi

def deltaR(eta1,phi1,eta2=None,phi2=None):
    ## catch if called with objects
    if eta2 == None:
        return deltaR(eta1.eta,eta1.phi,phi1.eta,phi1.phi)
    ## otherwise
    return hypot(eta1-eta2, deltaPhi(phi1,phi2))

def closest(obj,collection,presel=lambda x,y: True):
    ret = None; drMin = 999
    for x in collection:
        if not presel(obj,x): continue
        dr = deltaR(obj,x)
        if dr < drMin: 
            ret = x; drMin = dr
    return (ret,drMin)

def matchObjectCollection(objs,collection,dRmax=0.4,presel=lambda x,y: True):
    pairs = {}
    if len(objs)==0:
        return pairs
    if len(collection)==0:
        return dict( list(zip(objs, [None]*len(objs))) )
    for obj in objs:
        ( bm, dR ) = closest(obj, [ mobj for mobj in collection if presel(obj,mobj) ])
        if dR < dRmax:
            pairs[obj] = bm
        else:
            pairs[obj] = None
    return pairs

def matchObjectCollectionMultiple(objs,collection,dRmax=0.4,presel=lambda x,y: True):
    pairs = {}
    if len(objs)==0:
        return pairs
    if len(collection)==0:
        return dict( list(zip(objs, [None]*len(objs))) )
    for obj in objs:
        matched = [] 
        for c in collection :
            if presel(obj,c) and deltaR( obj, c ) < dRmax :
                matched.append( c )
        pairs[obj] = matched
    return pairs

def pass_MET(flag): #returns the True if the event pass the MET Filter requiriments otherwise False
    return flag.goodVertices and flag.globalSuperTightHalo2016Filter and flag.HBHENoiseFilter and flag.HBHENoiseIsoFilter and flag.EcalDeadCellTriggerPrimitiveFilter and flag.BadPFMuonFilter

def get_Mu(muons): #returns a collection of muons that pass the selection performed by the filter function
    return list(filter(lambda x : x.tightId and abs(x.eta) < 2.4 and x.miniPFRelIso_all < 0.1, muons))

def get_LooseMu(muons): #returns a collection of muons that pass the selection performed by the filter function
    return list(filter(lambda x : x.looseId and not x.tightId and x.pt > 35 and x.miniPFRelIso_all < 0.4 and abs(x.eta) < 2.4, muons))

def get_Ele(electrons): #returns a collection of electrons that pass the selection performed by the filter function
    return list(filter(lambda x : x.mvaFall17V2noIso_WP90 and x.miniPFRelIso_all < 0.1 and ((abs(x.eta) < 1.4442) or (abs(x.eta) > 1.566 and abs(x.eta) < 2.5)), electrons))

def get_LooseEle(electrons): #returns a collection of electrons that pass the selection performed by the filter function
    return list(filter(lambda x : x.mvaFall17V2noIso_WPL and not x.mvaFall17V2noIso_WP90 and x.miniPFRelIso_all < 0.4 and x.pt > 35 and ((abs(x.eta) < 1.4442) or (abs(x.eta) > 1.566 and abs(x.eta)< 2.5)), electrons))

def get_Jet(jets, pt): #returns a collection of jets that pass the selection performed by the filter function
    return list(filter(lambda x : x.jetId >= 2 and abs(x.eta) < 2.4 and x.pt > pt, jets))

def get_HT(jets):
    HT = 0.
    for jet in jets:
        HT += jet.pt
    return HT

def trig_map(HLT):
    passMu = False
    passEle = False
    passHT = False
    noTrigger = False
    if(HLT.Mu50 or HLT.TkMu50):
        passMu = True
    elif(HLT.Ele115_CaloIdVT_GsfTrkIdT):
        passEle = True  
    elif(HLT.PFHT800 or HLT.PFHT900):
        passHT = True
    else:
        noTrigger = True
    return passMu, passEle, passHT, noTrigger

def get_ptrel(lepton, jet):
    ptrel = ((jet.p4()-lepton.p4()).Vect().Cross(lepton.p4().Vect())).Mag()/(jet.p4().Vect().Mag())
    return ptrel
 
def presel(PV, muons, electrons, jets): #returns three booleans: goodEvent assure the presence of at least a good lepton vetoing the presence of additional loose leptons, goodMuEvt is for good muon event, goodEleEvt is for good muon event   
    isGoodPV = (PV.ndof>4 and abs(PV.z)<20 and hypot(PV.x, PV.y)<2) #basic requirements on the PV's goodness
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
 
def print_hist(infile, plotpath, hist, option = "HIST", log = False, stack = False):
    if not(isinstance(hist, list)):
        c1 = ROOT.TCanvas(infile + "_" + hist.GetName(), "c1", 50,50,700,600)
        hist.Draw(option)            
        c1.Print(plotpath + "/" + infile + "_" + hist.GetName() + ".png")
        c1.Print(plotpath + "/" + infile + "_" + hist.GetName() + ".root")
    elif isinstance(hist, list) and len(hist) > 1:
        c1 = ROOT.TCanvas(infile + "_" + hist[0].GetName(), "c1", 50,50,700,600)
        if not (infile == ""):
            c1 = ROOT.TCanvas(infile + "_" + hist[0].GetName() + '_comparison', "c1", 50,50,700,600)
        else:
            c1 = ROOT.TCanvas('comparison', "c1", 50,50,700,600)

        if isinstance(hist[0], ROOT.TGraph) or isinstance(hist[0], ROOT.TGraphAsymmErrors):
            i = 0
            mg = ROOT.TMultiGraph('mg', hist[0].GetTitle()+';'+hist[0].GetXaxis().GetTitle()+';'+hist[0].GetYaxis().GetTitle())
            for h in hist:
                h.SetLineColor(colors[i])
                mg.Add(h)
                i += 1
            print mg
            
            #cap = hist[0].GetXaxis().GetTitle()
            mg.SetMinimum(0.001)
            mg.Draw(option)
            Low = hist[0].GetXaxis().GetBinLowEdge(1)
            Nbin = hist[0].GetXaxis().GetNbins()
            High = hist[0].GetXaxis().GetBinUpEdge(Nbin)
            mg.GetXaxis().Set(Nbin, Low, High)
            
            for i in range(hist[0].GetXaxis().GetNbins()):
                u = i + 1
                mg.GetXaxis().SetBinLabel(u, hist[0].GetXaxis().GetBinLabel(u))
            
        elif isinstance(hist[0], ROOT.TEfficiency):
            i = 0
            mg = ROOT.TMultiGraph('mg', hist[0].GetTitle()+';'+hist[0].CreateGraph().GetXaxis().GetTitle()+';'+hist[0].CreateGraph().GetYaxis().GetTitle())

            for h in hist:
                print h
                h.SetLineColor(colors[i])
                mg.Add(h.CreateGraph())
                i += 1
            mg.SetMaximum(1.1)
            mg.SetMinimum(0.001)
            mg.Draw(option)
            
        elif isinstance(hist[0], ROOT.TH1F):
            mg = ROOT.THStack()
            i = 0
            for h in hist:
                h.SetLineColor(colors[i])
                if stack:
                    h.SetFillColor(colors[i])
                mg.Add(h)
                i += 1
            mg.Draw(option)
            mg.GetXaxis().SetTitle(hist[0].GetXaxis().GetTitle())
            mg.GetYaxis().SetTitle(hist[0].GetYaxis().GetTitle())
        else:
            for h in hist:
                h.Draw(option+'SAME')

        #c1.Modified()
        #c1.Update()
        if log:
            c1.SetLogy(1)
        c1.Pad().Modified()
        c1.Pad().Update()
        c1.BuildLegend()
        #c1.Modified()
        #c1.Update()
        c1.Pad().Modified()
        c1.Pad().Update()
        
        if not (infile == ""):
            c1.Print(plotpath + "/" + infile + "_" + hist[0].GetName() + '_comparison.png')
            c1.Print(plotpath + "/" + infile + "_" + hist[0].GetName() + '_comparison.root')
        else:
            c1.Print(plotpath + "/" + 'comparison.png')
            c1.Print(plotpath + "/" + 'comparison.root')

def save_hist(infile, plotpath, hist, option = "HIST"):
     fout = ROOT.TFile.Open(plotpath + "/" + infile +".root", "UPDATE")
     fout.cd()
     hist.Write()
     fout.Close()

def miniisoscan(isMu,threshold, lepton):
    for lepton in leptons:
        if(isMC and (lepton.genPartFlav == 1 or lepton.genPartFlav == 15)):
            totalMClep += 1.
            if (lepton.miniPFRelIso_all < threshold):
                if (lepton.pt > 50):
                    lepmatch_iso0p1_pt_50 += 1.
                if (lepton.pt > 75):
                    lepmatch_iso0p1_pt_75 += 1.
                if (lepton.pt > 100):
                    lepmatch_iso0p1_pt_100 += 1.
                if (lepton.pt > 125):
                    lepmatch_iso0p1_pt_125 += 1.
        if not(isMC and (lepton.genPartFlav == 1 or lepton.genPartFlav == 15)):
            totalnoMClep += 1.
            if (lepton.miniPFRelIso_all < threshold):
                if (lepton.pt > 50):
                    lepnomatch_iso0p1_pt_50 += 1.
                if (lepton.pt > 75):
                    lepnomatch_iso0p1_pt_75 += 1.
                if (lepton.pt > 100):
                    lepnomatch_iso0p1_pt_100 += 1.
                if (lepton.pt > 125):
                    lepnomatch_iso0p1_pt_125 += 1.
    return totalMClep,lepmatch_iso0p1_pt_50,lepmatch_iso0p1_pt_75,lepmatch_iso0p1_pt_100,lepmatch_iso0p1_pt_125,totalnoMClep,lepnomatch_iso0p1_pt_50,lepnomatch_iso0p1_pt_75,lepnomatch_iso0p1_pt_100,lepnomatch_iso0p1_pt_125
