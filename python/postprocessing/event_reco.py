import ROOT
import math
from array import array
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *
from PhysicsTools.NanoAODTools.postprocessing.framework.preskimming import preSkim
print "PhysicsTools implemented"

from preliminary_tools import *
print "Agostino's tools implemented"

from topreco import *
print "Andrea's tools implemented"

inputpath = "/eos/home-a/adeiorio/Wprime/nosynch/"
inpfiles = ["Wprime_4000_RH"
            #,"TT_Mtt-700to1000"
            #,"WJets"
            #,"QCD_Pt_600to800_1"
            #,"SingleMuon_Run2016G_1"
]

print "input pathed"

#ROOT.gROOT.SetStyle('Plain')
#ROOT.gStyle.SetPalette(1)   
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch()        # don't pop up canvases
ROOT.TH1.SetDefaultSumw2()
#ROOT.TGaxis.SetMaxDigits(3)
print "root setted"

def bjet_filter(jets): #returns a collection of only b-gen jets (to use only for MC samples)
    return list(filter(lambda x : x.partonFlavour == -5 or x.partonFlavour == 5, jets))

def sameflav_filter(jets, flav): #returns a collection of only b-gen jets (to use only for MC samples)
    return list(filter(lambda x : x.partonFlavour == flav, jets))

for inpfile in inpfiles:
    filetoopen = inputpath + inpfile
    infile = ROOT.TFile.Open(filetoopen + ".root")
    tree = InputTree(infile.Events)
    print '%s opened' %(filetoopen)
    
    #histo booking
    nbins_edges = 15
    nbins = 120
    nmin = 0
    nmax = 2400
    wnbins = 150
    wnmin = 0
    wnmax = 6000
    
    edges = array('f',[0., 20., 40., 60., 80., 100., 130., 160., 190., 230., 270., 320., 360., 400., 700., 1000.])
    h_mclepton_pt = {'electron': ROOT.TH1F("MC_Electron_pt", "MC_Electron_pt", nbins, nmin, nmax),
                     'muon': ROOT.TH1F("MC_Muon_pt", "MC_Muon_pt", nbins, nmin, nmax)
                    }
    h_mclepton_eta = {'electron': ROOT.TH1F("MC_Electron_eta", "MC_Electron_eta", nbins, nmin, nmax),
                     'muon': ROOT.TH1F("MC_Muon_eta", "MC_Muon_eta", nbins, nmin, nmax)
                    }
    h_mcbjet_pt = {'Wbjet_ev2': ROOT.TH1F("MC_ev2_Wbjet_pt", "MC_ev2_Wbjet_pt", nbins, nmin, nmax),
                   'topbjet_ev2': ROOT.TH1F("MC_ev2_topbjet_pt", "MC_ev2_topbjet_pt", nbins, nmin, nmax),
                   'Wbjet': ROOT.TH1F("MC_Wbjet_pt", "MC_Wbjet_pt", nbins, nmin, nmax),
                   'topbjet': ROOT.TH1F("MC_topbjet_pt", "MC_topbjet_pt", nbins, nmin, nmax),
                   }
    h_mcWprime_mass = {'all': ROOT.TH1F("MC_Wprime_mass", "MC_Wprime_mass", wnbins, wnmin, wnmax),
                       'ev2': ROOT.TH1F("MC_ev2_Wprime_mass", "MC_ev2_Wprime_mass", wnbins, wnmin, wnmax),
                       }
    #preselection
    badflag = 0
    badevt = 0
    HLTriggered = 0
    LepTriggered = 0
    JetTriggered = 0
    m2bjetev = 0
    nmctruth_ev = 0
    nentries = tree.GetEntries()
    print 'n entries: %i' %(nentries)

    for i in xrange(0,tree.GetEntries()):
        last = False

        if i == (nentries-1):
            last = True
        
        event = Event(tree,i)
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        fatjets = Collection(event, "FatJet")
        genpart = Collection(event, "GenPart")
        PV = Object(event, "PV")
        met = Object(event, "MET")
        HLT = Object(event, "HLT")
        Flag = Object(event, 'Flag')
        #it will be an ele or a muon, use isEle and isMu to recover lepton flavour
        lepton = None
        lepton_p4 = None
        mclepton = None
        mclepton_p4 = None

        if last:
            print 'all object extracted'

        if not pass_MET(Flag):
            badflag += 1
            continue

        goodEvt, isMu, isEle = presel(PV, muons, electrons, jets)

        if goodEvt and isMu and isEle:
            #print str(goodEvt) + ' ' + str(isMu) + ' ' + str(isEle)
            print 'presel algo not properly working here'
            continue
        
        if not goodEvt:
            badevt += 1
            continue

        #HLTriggering + mclepton finding
        if isMu:
            if(HLT.Mu50 or HLT.TkMu50):
                lepton = muons[0]
                mctfound = False
                for muon in muons:
                    if (muon.genPartFlav == 1 or muon.genPartFlav == 15) and not mctfound:
                        mclepton = muon
                        mctfound = True
                        if mclepton.genPartIdx == -1:
                            print 'MCTruth reconstruction not properly working - lepton step'
                            continue
    

        if isEle:
            if(HLT.Ele115_CaloIdVT_GsfTrkIdT):
                lepton = electrons[0]
                mctfound = False
                for electron in electrons:
                    if (electron.genPartFlav == 1 or electron.genPartFlav == 15) and not mctfound:
                        mclepton = electron
                        mctfound = True
                        if mclepton.genPartIdx == -1:
                            print 'MCTruth reconstruction not properly working - lepton step'
                            continue
    
        if lepton is None:
            continue
        else:
            HLTriggered += 1
            #print 'HLTriggered'
            
        #MCruth event reconstruction
        
        mctop_p4 = None
        mcpromptbjet_p4 = None
        bjetcheck = True
        bjets = bjet_filter(jets)
        if len(bjets)>2:
            #print 'Warning! More than 2 bjet from MCTruth in ev #%i' %i
            bjetcheck = False
            m2bjetev += 1
        '''
        else:
            for bjet in bjets:
                if bjet.partonFlavour == 5:
                    h_mcbjet_pt['bjet'].Fill(bjet.pt)
                else:
                    h_mcbjet_pt['antibjet'].Fill(bjet.pt)
        '''
        
        if mclepton is not None:
            nmctruth_ev += 1
            mclepton_p4 = ROOT.TLorentzVector()
            mclepton_p4.SetPtEtaPhiM(mclepton.pt, mclepton.eta, mclepton.phi, mclepton.mass)
            if isMu:
                h_mclepton_pt['muon'].Fill(mclepton.pt)
            elif isEle:
                h_mclepton_pt['electron'].Fill(mclepton.pt)
            
            MCWprime_p4 = ROOT.TLorentzVector()

            topgot = False
            Wpgot = False

            bottjets = sameflav_filter(bjets, 5)
            abottjets = sameflav_filter(bjets, -5)

            #if bjetcheck:
             
            for bjet in bjets:
                bjet_p4 = ROOT.TLorentzVector()
                bjet_p4.SetPtEtaPhiM(bjet.pt, bjet.eta, bjet.phi, bjet.mass)

                if abs(bjet.partonFlavour)!=5:
                    print 'bfilter not properly working'
                    continue
            
                blepflav = genpart[mclepton.genPartIdx].pdgId*bjet.partonFlavour

                if blepflav < 0 and not topgot:
                    mctop_p4 = mclepton_p4 + bjet_p4
                    h_mcbjet_pt['topbjet'].Fill(bjet_p4.Pt())
                    if bjetcheck:
                        h_mcbjet_pt['topbjet_ev2'].Fill(bjet_p4.Pt())
                    topgot = True
                elif blepflav > 0 and not Wpgot:
                    mcpromptbjet_p4 = bjet_p4
                    h_mcbjet_pt['Wbjet'].Fill(bjet_p4.Pt())
                    if bjetcheck:
                        h_mcbjet_pt['Wbjet_ev2'].Fill(bjet_p4.Pt())
                    Wpgot = True
            
            if topgot and Wpgot:
                MCWprime_p4 = mctop_p4 + mcpromptbjet_p4
                h_mcWprime_mass['all'].Fill(MCWprime_p4.M())
                if bjetcheck:
                    h_mcWprime_mass['ev2'].Fill(MCWprime_p4.M())
            

        #LepTriggering

        if isMu:
            if not (lepton.tightId or lepton.pt > 50):
                continue
            else:
                LepTriggered += 1

        if isEle:
            if not (lepton.mvaFall17V2noIso_WP90 or lepton.pt > 50):
                continue
            else:
                LepTriggered += 1
            

        #JetTriggering
        goodjets = get_Jet(jets, 35)
        if len(goodjets)<1:
            continue
        else:
            JetTriggered += 1
    
    
    #histo printing and saving
    
    for value in h_mclepton_pt.values():
        print_hist(inpfile, value)
        save_hist(inpfile, value)
    
    for value in h_mcbjet_pt.values():
        print_hist(inpfile, value)
        save_hist(inpfile, value)
    
    for value in h_mcWprime_mass.values():
        print_hist(inpfile, value)
        save_hist(inpfile, value)
    
    print 'Total events: %d     ||     Bad MET flag events %d     ||     Bad events %d      ||     Events with more than 2 mcbjets %d' %(tree.GetEntries(), badflag, badevt, m2bjetev)
        #tree.Scan("GenPart_genPartIdxMother:GenPart_pdgId")#, "GenPart_pdgId==-11 || GenPart_pdgId==11")
        #tree.Scan("Muon_genPartIdx", "(HLT_Mu50 || HLT_TkMu50 || HLT_Ele115_CaloIdVT_GsfTrkIdT) && Muon_genPartIdx == -1")
        #tree.Scan("GenPart_pdgId[GenPart_genPartIdxMother[Electron_genPartIdx]]:GenPart_pdgId[Electron_genPartIdx]:GenPart_pdgId[GenPart_genPartIdxMother[Muon_genPartIdx]]:GenPart_pdgId[Muon_genPartIdx]", "(Electron_genPartIdx != (-1) && Muon_genPartIdx != (-1) && (GenPart_pdgId[GenPart_genPartIdxMother[Electron_genPartIdx]] == GenPart_pdgId[Electron_genPartIdx] || GenPart_pdgId[GenPart_genPartIdxMother[Muon_genPartIdx]] == GenPart_pdgId[Muon_genPartIdx]))")


