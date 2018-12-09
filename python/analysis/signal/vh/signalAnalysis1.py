import ROOT
import os
from math import fabs, cos, sin, tan, atan, exp, sqrt
from array import array

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi, deltaR, closest, matchObjectCollection

class signalAnalysis(Module):
    def __init__(self):
        self.writeHistFile=True
        self.Genpart = False
        self.Nevents = 0
        pass
    def beginJob(self):
        Module.beginJob(self,histFile,histDirName)
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.initReaders(inputTree) # initReaders must be called in beginFile
        self.FilesName=inputFile
        self.out = wrappedOutputTree
        #CleanObjectCollection
        self.out.branch("Jet_Clean" ,"I", 0, "nJet_Clean", "nJet_Clean", False)
        self.out.branch("Jet_Tight" ,"I", 0, "nJet_Tight", "nJet_Tight", False)
        self.out.branch("Muon_Medium",  "I", 0, "nMuon_Medium", "nMuon_Medium", False)
        self.out.branch("Electron_Medium",  "I", 0, "nElectron_Medium", "nElectron_Medium", False)
        self.out.branch("Tau_Clean",  "I", 0, "nTau_Clean", "nTau_Clean", False)
        self.out.branch("Photon_Clean",  "I", 0, "nTau_Clean", "nTau_Clean", False)
        self.out.branch("JetE",  "F", 0, "nJetE", "nJetE", False) ###
        self.out.branch("dRMuJet",  "F", 0, "ndRMuJet", "ndRMuJet", False)
        self.out.branch("dRElJet",  "F", 0, "ndRElJet", "ndRElJet", False)

        self.out.branch("nGoodJet", "I")
        self.out.branch("nGoodMuon", "I")
        self.out.branch("nGoodElectron", "I")
        self.out.branch("nGoodTau", "I")
        self.out.branch("nGoodPhoton", "I")

        self.out.branch("isOSmumu", "I")
        self.out.branch("isOSemu", "I")
        self.out.branch("isSSmumu", "I")

        self.out.branch("HTpt",  "F")
        self.out.branch("HTphi", "F")
        self.out.branch("Zweight","F")

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

        #Select good LEPTON, on specific kinematics
        mupt=5
        muiso=0.25 #iso03
        for nmu,lep in enumerate(muons):
            if lep.pt<mupt: continue
            if lep.pfRelIso03_all>muiso: continue
            if fabs(lep.eta)>2.4: continue #central muon
            if lep.tightId:
                Muon_Tight[nmu]=1
            elif lep.mediumId:
                Muon_Medium[nmu]=1

        elept=15
        eleiso=0.25 #iso03
        for nele,lep in enumerate(electrons):
            if lep.pt<elept: continue
            if lep.pfRelIso03_all>eleiso: continue
            if fabs(lep.eta)>2.4: continue #central muon 
            if lep.cutBased==4:
                Electron_Tight[nele]=1
            elif lep.cutBased>3:
                Electron_Medium[nele]=1

        #Clean Tau from muon and electron
        taupt=18
        for ntau,tau in enumerate(taus):
            if tau.pt<taupt: continue
            if fabs(tau.eta)>2.3: continue
            if tau.idDecayMode!=1: continue
            #Clean from muons
            for nmu,lep in enumerate(muons):
                if Muon_Medium[nmu]!=1: continue
                if deltaR(tau,lep)<0.4:
                    Tau_Clean[ntau]=0
                else:
                    Tau_Clean[ntau]=1
            #Clean from electrons
            for nele,lep in enumerate(electrons):
                if Electron_Medium[nele]!=1: continue
                if deltaR(tau,lep)<0.4:
                    Tau_Clean[ntau]=0
                else:
                    Tau_Clean[ntau]=1

        #Clean photon from muon and electron
        phopt=15
        phoid=1 #cutBased 0:fail, 1::loose, 2:medium, 3:tight
        for npho,pho in enumerate(photons):
            if pho.pt<phopt: continue
            if fabs(pho.eta)>2.5: continue
            if pho.cutBased!=1: continue
            #Clean from muons
            for nmu,lep in enumerate(muons):
                if Muon_Medium[nmu]!=1: continue
                if deltaR(pho,lep)<0.4:
                    Photon_Clean[npho]=0
                else:
                    Photon_Clean[npho]=1
            #Clean from electrons
            for nele,lep in enumerate(electrons):
                if Electron_Medium[nele]!=1: continue
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
            if jet.puId<jetpuid: continue
            if jet.pt<jetpt: continue
            if jet.jetId<1: continue ##???
            if fabs(jet.eta)>jeteta: continue
            if jet.jetId==3: Jet_Tight[njet]=1
            
            #assmuonid1=jet.muonIdx1
            #assmuonid2=jet.muonIdx2
            #asseleid1=jet.electronIdx1
            #asseleid2=jet.electronIdx2

            for nmu,lep in enumerate(muons):
                if Muon_Medium[nmu]!=1: continue
                dr = deltaR(jet,lep)
                if dr<drm:
                    drm=dr
                    
                if dr<0.4:
                    Jet_Clean[njet]=0
                    if jet.chHEF > 0.1: Jet_Clean[njet]=1
                    if jet.neHEF > 0.2: Jet_Clean[njet]=1
                else:
                    Jet_Clean[njet]=1
            dRMuJet[njet]=drm
                        
            for nele,lep in enumerate(electrons):
                if Electron_Medium[nele]!=1: continue
                dr = deltaR(jet,lep)
                if dr<dre:
                    dre=dr
                    
                if dr<0.4:
                    Jet_Clean[njet]=0
                    if jet.chHEF > 0.1: Jet_Clean[njet]=1
                    if jet.neHEF > 0.2: Jet_Clean[njet]=1
                else:
                    Jet_Clean[njet]=1
            dRElJet[njet]=dre
            
        ###############

        # HT Computation
        HTpt=0.
        HTphi=0.
        for num, jet in enumerate(jets):
            #if jet.puId==4: continue
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

        ## ANALYSIS
        isOSmumu=0
        isOSemu=0
        isSSmumu=0
        ##Analysis OSmumu
        if nGoodMuon==2 or nGoodMuon>2:
            if (muons[0].charge!=muons[1].charge):
                isOSmumu=1
            elif (muons[0].charge==muons[1].charge):
                isSSmumu=1
        elif nGoodMuon>0 and nGoodElectron>0:
            if (electrons[0].charge!=muons[0].charge):
                isOSemu=1

        self.out.fillBranch("Jet_Clean", Jet_Clean)
        self.out.fillBranch("Jet_Tight", Jet_Tight)
        self.out.fillBranch("Muon_Medium", Muon_Medium)
        self.out.fillBranch("Electron_Medium", Electron_Medium)
        self.out.fillBranch("Tau_Clean", Tau_Clean)
        self.out.fillBranch("Photon_Clean", Photon_Clean)
        self.out.fillBranch("dRMuJet", dRMuJet)
        self.out.fillBranch("dRElJet", dRElJet)
        #self.out.fillBranch("JetE", JetE)

        self.out.fillBranch("nGoodJet", nGoodJet)
        self.out.fillBranch("nGoodMuon", nGoodMuon)
        self.out.fillBranch("nGoodElectron", nGoodElectron)
        self.out.fillBranch("nGoodTau", nGoodTau)
        self.out.fillBranch("nGoodPhoton", nGoodPhoton)

        self.out.fillBranch("isOSmumu", isOSmumu)
        self.out.fillBranch("isOSemu", isOSemu)
        self.out.fillBranch("isSSmumu", isSSmumu)
        
        self.out.fillBranch("HTpt", HTpt)
        self.out.fillBranch("HTphi", HTphi)
        self.out.fillBranch("Zweight", Zweight)

        #if self.Nevents==100: 
        return True
        
# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

cleaning = lambda : cleaningStudy()
