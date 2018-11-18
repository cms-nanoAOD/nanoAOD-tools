import ROOT as r
import ROOT
import os
from ROOT import TTree, TFile, TLorentzVector, AddressOf, gROOT
from math import fabs
from array import array

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi, deltaR, closest
        
class signalStudy(Module): # MHT producer, unclean jets only (no lepton overlap cleaning, no jet selection)
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
        self.out.branch("cleanedJet" ,"I", 100);
        self.out.branch("cleanedMuon",  "I", 100);
        self.out.branch("cleanedElectron",  "I", 100);
        self.out.branch("JetMuon_MindR",  "F", 100);
        self.out.branch("JetElectron_MindR",  "F", 100);
        self.out.branch("MHTju_pt",  "F");
        self.out.branch("MHTju_phi", "F");
        self.out.branch("ZPtCorr","F");

        #Signal kinematics
        #basic kinematics
        self.out.branch("W0pt",  "F");
        self.out.branch("W1pt",  "F");
        self.out.branch("W2pt",  "F");
        self.out.branch("W3pt",  "F");
        self.out.branch("Hpt",  "F");
        self.out.branch("q1pt",  "F");
        self.out.branch("q2pt",  "F");
        self.out.branch("lep1pt",  "F");
        self.out.branch("lep2pt",  "F");
        self.out.branch("lep3pt",  "F");
        #composite kinematics
        self.out.branch("W1W2dPhi",  "F");
        self.out.branch("W1W3dPhi",  "F");
        self.out.branch("W2W3dPhi",  "F");
        self.out.branch("HW3dPhi",  "F");
        self.out.branch("lep1lep2dPhi",  "F");
        self.out.branch("lep1lep3Phi",  "F");
        self.out.branch("lep2lep3dPhi",  "F");
        self.out.branch("q1q2dPhi",  "F");
        

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
        Jet_Clean=[0]*100
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

        # Cleaning on lepton
        Muon_Clean=[0]*100
        Muon_DRjet=[0.]*100
        DRMuJet=999.
        Electron_Clean=[0]*100
        Electron_DRjet=[0.]*100
        DRElJet=999.
        for numMu,lep in enumerate(muons):
            #find the nearest cleanjet
            for numjet, jet in enumerate(jets):
                if (Jet_Clean[numjet]==0): continue;
                dr = deltaR(lep,jet)
                if dr < DRMuJet:
                    DRMuJet = dr
            Muon_DRjet[numMu]= DRMuJet #distance between muon-jet

            if self.Genpart:
                # match gen stable and final muon
                valuepair=closest(lep,genparts, lambda x,y: True if y.status==1 and y.pdgId==x.pdgId else False) #stable genpart; same flavor
                if valuepair[1]>0.04: continue; #within DR<0.04
                Muon_Clean[numMu]=1
            elif not self.Genpart:
                Muon_Clean[numMu]=1 #Its data
                #momID=valuepair[0].genPartIdxMother # mother of gen muon
                #print "Mother of gen-muon status : ", genparts[momID].status, " and pdgId : ", genparts[momID].pdgId
                #grandmomID=genparts[momID].genPartIdxMother # grandmother of mother of gen muon
                #print "Grandmother of gen-muon status : ", genparts[grandmomID].status, " and pdgId : ", genparts[grandmomID].pdgId

        for numEl,lep in enumerate(electrons):
            #find the nearest cleanjet
            for numjet, jet in enumerate(jets):
                if (Jet_Clean[numjet]==0): continue;
                dr = deltaR(lep,jet)
                if dr < DRElJet:
                    DRElJet = dr
            Electron_DRjet[numEl]= DRElJet #distance between electron-jet

            if self.Genpart:
                # match gen stable and final electron
                valuepair=closest(lep,genparts, lambda x,y: True if y.status==1 and y.pdgId==x.pdgId else False)
                if valuepair[1]>0.04: continue;
                Electron_Clean[numEl]=1
            elif not self.Genpart:
                Electron_Clean[numEl]=1 #Its data

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

        # find the reconstructed muon and genpart
        
            
        self.out.fillBranch("cleanedJet", Jet_Clean);
        self.out.fillBranch("cleanedMuon", Muon_Clean);
        self.out.fillBranch("cleanedElectron", Electron_Clean);
        self.out.fillBranch("JetMuon_MindR", Muon_DRjet);
        self.out.fillBranch("JetElectron_MindR", Electron_DRjet);
        self.out.fillBranch("MHTju_pt", HTpt)
        self.out.fillBranch("MHTju_phi", HTphi)
        self.out.fillBranch("ZPtCorr", Zweight);
        return True
        
# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

signal = lambda : signalStudy()
