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

for inpfile in inpfiles:
    filetoopen = inputpath + inpfile
    infile = ROOT.TFile.Open(filetoopen + ".root")
    tree = InputTree(infile.Events)
    print '%s opened' %(filetoopen)
    
    #histo booking

    #preselection

    badflag = 0
    badevt = 0
    unHLTriggered = 0
    unLepTriggered = 0
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
        PV = Object(event, "PV")
        met = Object(event, "MET")
        HLT = Object(event, "HLT")
        Flag = Object(event, 'Flag')
        lepton = None

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

        #HLTriggering
        if isMu:
            if(HLT.Mu50 or HLT.TkMu50):
                lepton = muons[0]

        if isEle:
            if(HLT.Ele115_CaloIdVT_GsfTrkIdT):
                lepton = electrons[0]

        if lepton is None:
            unHLTriggered += 1
            continue

        #LepTriggering
        if isMu:
            if not lepton.tightId:
                unLepTriggered += 1
                continue

        if lepton.pt < 50:
            unLepTriggered += 1
            continue
          
        HT = get_HT(jets)
