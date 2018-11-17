import ROOT
import os
from math import fabs
from array import array

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi, deltaR, closest

class objCleaning(Module): # MHT producer, unclean jets only (no lepton overlap cleaning, no jet selection)
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
        self.out = wrappedOutputTree
        #CleanObjectCollection
        self.out.branch("cleanedJet" ,"I", 30);
        self.out.branch("cleanedMuon",  "I", 30);
        self.out.branch("cleanedElectron",  "I", 30);

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def initReaders(self,tree): # this function gets the pointers to Value and ArrayReaders and sets them in the C++ worker class
        self._ttreereaderversion = tree._ttreereaderversion # self._ttreereaderversion must be set AFTER all calls to tree.valueReader or tree.arrayReader

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        if event._tree._ttreereaderversion > self._ttreereaderversion: # do this check at every event, as other modules might have read further branches
            self.initReaders(event._tree)
        # do NOT access other branches in python between the check/call to initReaders and the call to C++ worker code

        # Collection
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        
        # Cleaning Jet
        Jet_Clean=[0]*30
        for num,jet in enumerate(jets) :
            Jet_Clean[num]=1
            if jet.puId<4: continue;
            if jet.pt<30: continue;
            if fabs(jet.eta)>2.5: continue;
            #Cleaning from muon
            drMinMu = 999.
            for lep in muons:
                #if lep.jetIdx!=-1: continue;#Looking at Muon that associated with jet
                if lep.mediumId==0: continue;
                if lep.pt<5: continue;
                dr = deltaR(lep,jet)
                if dr < drMinMu:
                    drMinMu = dr

            if drMinMu<0.4:
                Jet_Clean[num]=0
                if jet.chHEF>0.1: Jet_Clean[num]=1
                if jet.neHEF>0.2: Jet_Clean[num]=1

            drMinE = 999.
            for lep in electrons:
                if lep.cutBased<4: continue;
                if lep.pt<15: continue;
                dr = deltaR(lep,jet)
                if dr < drMinE:
                    drMinE = dr

            if drMinE<0.4:
                Jet_Clean[num]=0
                if jet.chHEF>0.1: Jet_Clean[num]=1
                if jet.neHEF>0.2: Jet_Clean[num]=1
        
                
        self.out.fillBranch("cleanedJet", Jet_Clean);
        return True
        
# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

cleaning = lambda : objCleaning()
