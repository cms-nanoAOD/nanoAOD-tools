import ROOT
import os
from math import fabs
from array import array

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi, deltaR, closest, matchObjectCollectionMultiple

class cleaningStudy(Module): # MHT producer, unclean jets only (no lepton overlap cleaning, no jet selection)
    def __init__(self):
        #if "/mhtjuProducerCppWorker_cc.so" not in ROOT.gSystem.GetLibraries():
        #    print "Load C++ mhtjuProducerCppWorker worker module"
        #    base = os.getenv("NANOAODTOOLS_BASE")
        #    if base:
        #        ROOT.gROOT.ProcessLine(".L %s/src/mhtjuProducerCppWorker.cc+O"%base)
        #    else:
        #        base = "%s/src/PhysicsTools/NanoAODTools"%os.getenv("CMSSW_BASE")
        #        ROOT.gSystem.Load("libPhysicsToolsNanoAODTools.so")
        #        ROOT.gROOT.ProcessLine(".L %s/interface/mhtjuProducerCppWorker.h"%base)
        #self.worker = ROOT.mhtjuProducerCppWorker()
        self.Genpart = False
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.initReaders(inputTree) # initReaders must be called in beginFile
        self.FilesName=inputFile
        self.out = wrappedOutputTree
        #CleanObjectCollection
        self.out.branch("cleanedJet" ,"I", 0, "nCleanedJet", "nCleanedJet", False);
        self.out.branch("cleanedMuon",  "I", 0, "nCleanedMuon", "nCleanedMuon", False);
        self.out.branch("cleanedElectron",  "I", 0, "nCleanedElectron", "nCleanedElectron", False);
        self.out.branch("JetMuon_MindR",  "F");
        self.out.branch("JetElectron_MindR",  "F");

        self.out.branch("MHTju_pt",  "F");
        self.out.branch("MHTju_phi", "F");
        self.out.branch("ZPtCorr","F");

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def initReaders(self,tree): # this function gets the pointers to Value and ArrayReaders and sets them in the C++ worker class
        self._ttreereaderversion = tree._ttreereaderversion # self._ttreereaderversion must be set AFTER all calls to tree.valueReader or tree.arrayReader
        for branch in tree.GetListOfBranches():
            if( branch.GetName() == "nGenPart" ):
                self.Genpart=True
                print "nGenPart exist, this is MC"
                break
            
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        if event._tree._ttreereaderversion > self._ttreereaderversion: # do this check at every event, as other modules might have read further branches
            self.initReaders(event._tree)
        # do NOT access other branches in python between the check/call to initReaders and the call to C++ worker code

        # Collection
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        if self.Genpart:
            genparts = Collection(event, "GenPart")
        
        # Cleaning Jet
        Jet_Clean=[0]*len(jets)

        for num,jet in enumerate(jets) :
            Jet_Clean[num]=1
            if jet.puId<4 and jet.pt<30 and fabs(jet.eta)>2.5: continue
            
            for numm,lep in enumerate(muons):
                if lep.pt<5 and lep.mediumId==0: continue
                if deltaR(jet,lep) < 0.4:
                    Jet_Clean[num]=0
                    if jet.chHEF>0.1: Jet_Clean[num]=1
                    if jet.neHEF>0.2: Jet_Clean[num]=1

            for nummm,lep in enumerate(electrons):
                if lep.pt<15 and lep.cutBased<4: continue     
                if deltaR(jet,lep) < 0.4:
                    Jet_Clean[num]=0
                    if jet.chHEF>0.1: Jet_Clean[num]=1
                    if jet.neHEF>0.2: Jet_Clean[num]=1

        # Cleaning leptons
        Muon_Clean=[0]*len(muons)
        Electron_Clean=[0]*len(electrons)
        dRMuJet=999.
        dRElJet=999.
        for numm,lep in enumerate(muons):
            Muon_Clean[numm]=1
            for jet in jets :
                dR=deltaR(lep,jet)
                if dR < dRMuJet:
                    dRMuJet = dR
                if dR < 0.4:
                    Muon_Clean[numm]=0
        for nummm,lep in enumerate(electrons):
            Electron_Clean[nummm]=1
            for jet in jets :
                dR=deltaR(lep,jet)
                if dR < dRElJet:
                    dRElJet = dR
                if dR < 0.4:
                    Electron_Clean[nummm]=0
                
        # HT Computation
        HTpt=0.
        HTphi=0.
        for num, jet in enumerate(jets):
            if jet.puId<4: continue;
            if jet.pt<30: continue;
            if fabs(jet.eta)>2.5: continue;
            if Jet_Clean[num]==0: continue;
            HTpt+=jet.pt
            HTphi+=jet.phi
        
        # Perform PtZ correction computation
        Zweight = 1.
        NgenZ=0
        if self.Genpart and "DYJetsToLL" in self.FilesName.GetName().split('/')[-1].split('_')[0]:
            for gen in genparts:
                if gen.pdgId!=23: continue;
                if gen.status!=62: continue;
                NgenZ+=1
                if NgenZ!=1: continue;
                Zpt=gen.pt
                if Zpt<20: Zweight=1.2
                if Zpt>20 and Zpt<30: Zweight=1.
                if Zpt>30 and Zpt<40: Zweight=0.75
                if Zpt>40 and Zpt<50: Zweight=0.65
                if Zpt>50 and Zpt<200: Zweight=0.65-0.00034*Zpt
                if Zpt>200: Zweight=0.6

        self.out.fillBranch("cleanedJet", Jet_Clean);
        self.out.fillBranch("cleanedMuon", Muon_Clean);
        self.out.fillBranch("cleanedElectron", Electron_Clean);
        self.out.fillBranch("JetMuon_MindR", dRMuJet);
        self.out.fillBranch("JetElectron_MindR", dRElJet);
        
        self.out.fillBranch("MHTju_pt", HTpt)
        self.out.fillBranch("MHTju_phi", HTphi)
        self.out.fillBranch("ZPtCorr", Zweight);
        return True
        
# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

cleaning = lambda : cleaningStudy()
