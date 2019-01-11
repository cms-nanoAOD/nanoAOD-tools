import ROOT
import os
from math import fabs, cos, sin, tan, atan, exp, sqrt
from array import array

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi, deltaR, closest, matchObjectCollection

class bareCleaning(Module):
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
        self.Nevents = 0
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
        self.out.branch("cleanedJet" ,"I", 0, "nCleanedJet", "nCleanedJet", False)
        self.out.branch("cleanedMuon",  "I", 0, "nCleanedMuon", "nCleanedMuon", False)
        self.out.branch("cleanedElectron",  "I", 0, "nCleanedElectron", "nCleanedElectron", False)
        self.out.branch("cleanedTau",  "I", 0, "nCleanedTau", "nCleanedTau", False)
        self.out.branch("cleanedPhoton",  "I", 0, "nCleanedPhoton", "nCleanedPhoton", False)
        self.out.branch("JetE",  "F", 0, "nJetE", "nJetE", False) ###
        self.out.branch("MuonJet_MindR",  "F", 0, "nMuonJet", "nMuonJet", False)
        self.out.branch("ElecJet_MindR",  "F", 0, "nElecJet", "nElecJet", False)

        self.out.branch("nGoodJet", "I")
        self.out.branch("nGoodMuon", "I")
        self.out.branch("nGoodElectron", "I")
        self.out.branch("nGoodTau", "I")
        self.out.branch("nGoodPhoton", "I")

        self.out.branch("MHTju_pt",  "F")
        self.out.branch("MHTju_phi", "F")
        self.out.branch("ZPtCorr","F")

        self.Nevents+=1

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
        taus = Collection(event, "Tau")
        photons = Collection(event, "Photon")
            
        # Cleaning Jet wrt muon #preliminary cleaning
        Jet_Clean=[0]*len(jets)
        Jet_Tight=[0]*len(jets)
        Muon_Medium=[0]*len(muons)
        Electron_Medium=[0]*len(electrons)
        Muon_Tight=[0]*len(muons)
        Electron_Tight=[0]*len(electrons)
        Tau_Clean=[0]*len(taus)
        Photon_Clean=[0]*len(photons)
        #Jetpx=[0.]*len(jets)
        #Jetpy=[0.]*len(jets)
        #Jetpz=[0.]*len(jets)
        #JetE=[0.]*len(jets)

        #Clean Lepton First, on specific kinematics
        for nmu,lep in enumerate(muons):
            if lep.tightId:
                Muon_Tight[nmu]=1
            elif lep.mediumId:
                Muon_Medium[nmu]=1

        for nele,lep in enumerate(electrons):
            if lep.cutBased==4:
                Electron_Tight[nele]=1
            elif lep.cutBased>1:
                Electron_Medium[nele]=1

        #Clean Tau from muon and electron
        for ntau,tau in enumerate(taus):
            #if tau.idDecayMode!=1: continue
            for nmu,lep in enumerate(muons):
                if deltaR(tau,lep)<0.4:
                    Tau_Clean[ntau]=0
                else:
                    Tau_Clean[ntau]=1
                    
            for nele,lep in enumerate(electrons):
                if deltaR(tau,lep)<0.4:
                    Tau_Clean[ntau]=0
                else:
                    Tau_Clean[ntau]=1

        #Clean photon from muon and electron
        for npho,pho in enumerate(photons):
            for nmu,lep in enumerate(muons):
                if deltaR(pho,lep)<0.4:
                    Photon_Clean[npho]=0
                else:
                    Photon_Clean[npho]=1
                    
            for nele,lep in enumerate(electrons):
                if deltaR(pho,lep)<0.4:
                    Photon_Clean[npho]=0
                else:
                    Photon_Clean[npho]=1

        #Clean jet from muon and electron
        jetpt=30
        jeteta=2.5
        jetid=1
        jetpuid=4
        dRMuJet=[999.]*len(jets)
        dRElJet=[999.]*len(jets) 
        drm=999.
        dre=999.
        for njet,jet in enumerate(jets):

            for nmu,lep in enumerate(muons):
                dr = deltaR(jet,lep)
                if dr<drm:
                    drm=dr
                    
                if dr<0.4:
                    Jet_Clean[njet]=0
                else:
                    Jet_Clean[njet]=1
            dRMuJet[njet]=drm
                        
            for nele,lep in enumerate(electrons):
                dr = deltaR(jet,lep)
                if dr<dre:
                    dre=dr
                    
                if dr<0.4:
                    Jet_Clean[njet]=0
                else:
                    Jet_Clean[njet]=1
            dRElJet[njet]=dre
            
        ###############

        # HT Computation
        HTpt=0.
        HTphi=0.
        for num, jet in enumerate(jets):
            if jet.puId==4: continue
            if Jet_Clean[num]==0: continue
            if jet.pt<30.: continue # taken at 30 GeV
            if fabs(jet.eta)>2.5: continue
            
            HTpt = HTpt + jet.pt
            HTphi = HTphi + jet.phi
            
        '''
        #Link lepton to genpart
        if self.Genpart: #only for MC
            Muon_GenMotherIdx=[-1]*len(muons)
            for num,lep in enumerate(muons):
                Muon_GenMotherIdx[num]=-1
                for gennum,gen in enumerate(genparts):
                     if gen.status!=1: continue
                     if gen.pdgId!=lep.pdgId: continue
                     delR=deltaR(lep,gen)
                     if delR>0.4: continue
                     Muon_mom=gen.genPartIdxMother
                     if genparts[Muon_mom].pdgId == lep.pdgId:
                         Muon_GenMotherIdx[num]=gennum

            Ele_GenMotherIdx=[-1]*len(electrons)
            for num,lep in enumerate(electrons):
                Ele_GenMotherIdx[num]=-1
		for gennum,gen in enumerate(genparts):
                    if gen.status!=1: continue
                    if gen.pdgId!=lep.pdgId: continue
                    delR=deltaR(lep,gen)
                    if delR>0.4: continue
                    Ele_mom=gen.genPartIdxMother
                    if genparts[Ele_mom].pdgId == lep.pdgId:
                        Ele_GenMotherIdx[num]=gennum
        '''
        
        # Perform PtZ correction computation
        Zweight = 1.
        NgenZ=0
        if self.Genpart and "DYJetsToLL" in self.FilesName.GetName().split('/')[-1].split('_')[0]:
            for gen in genparts:
                if gen.pdgId!=23: continue;
                if gen.status!=62: continue;
                NgenZ+=1
                if NgenZ>1: continue;
                Zpt=gen.pt
                if Zpt<20: Zweight=1.2
                if Zpt>20 and Zpt<30: Zweight=1.
                if Zpt>30 and Zpt<40: Zweight=0.75
                if Zpt>40 and Zpt<50: Zweight=0.65
                if Zpt>50 and Zpt<200: Zweight=0.65-0.00034*Zpt
                if Zpt>200: Zweight=0.6

                
        ##count good physics objects                                                                                                                  
        nGoodJet=0
        nGoodMuon=0
        nGoodElectron=0
        nGoodTau=0
        nGoodPhoton=0
        for num,obj in enumerate(jets):
            if Jet_Clean[num]==1: nGoodJet+=1
        for num,obj in enumerate(muons):
            if Muon_Medium[num]==1: nGoodMuon+=1
        for num,obj in enumerate(electrons):
            if Electron_Medium[num]==1: nGoodElectron+=1
        for num,obj in enumerate(taus):
            if Tau_Clean[num]==1: nGoodTau+=1
        for num,obj in enumerate(photons):
            if Photon_Clean[num]==1: nGoodPhoton+=1
            

        self.out.fillBranch("cleanedJet", Jet_Clean)
        self.out.fillBranch("cleanedMuon", Muon_Medium)
        self.out.fillBranch("cleanedElectron", Electron_Medium)
        self.out.fillBranch("cleanedTau", Tau_Clean)
        self.out.fillBranch("cleanedPhoton", Photon_Clean)
        self.out.fillBranch("MuonJet_MindR", dRMuJet)
        self.out.fillBranch("ElecJet_MindR", dRElJet)
        #self.out.fillBranch("JetE", JetE)

        self.out.fillBranch("nGoodJet", nGoodJet)
        self.out.fillBranch("nGoodMuon", nGoodMuon)
        self.out.fillBranch("nGoodElectron", nGoodElectron)
        self.out.fillBranch("nGoodTau", nGoodTau)
        self.out.fillBranch("nGoodPhoton", nGoodPhoton)
        
        self.out.fillBranch("MHTju_pt", HTpt)
        self.out.fillBranch("MHTju_phi", HTphi)
        self.out.fillBranch("ZPtCorr", Zweight)

        #if self.Nevents==100: 
        return True
        
# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

cleaning = lambda : bareCleaning()
