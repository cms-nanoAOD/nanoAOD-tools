#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from math import fabs
from PhysicsTools.NanoAODTools.analysis.helper.helper import *

class Analysis(Module):
    def __init__(self):
	self.writeHistFile=True

    def beginJob(self,histFile=None,histDirName=None):
	Module.beginJob(self,histFile,histDirName)

        ## Global Variables
        self.h_eventNumber =ROOT.TH1D('eventNumber', 'EventNumber', 2,0,2); self.addObject(self.h_eventNumber )
        self.h_runNumber =ROOT.TH1D('runNumber', 'runNumber', 2,0,2); self.addObject(self.h_runNumber )
        
        self.h_isOSmumu =ROOT.TH1D('isOSmumu', 'isOSmumu', 2,-0.5,1.5); self.addObject(self.h_isOSmumu )
        self.h_isOSee   =ROOT.TH1D('isOSee', 'isOSee', 2,-0.5,1.5); self.addObject(self.h_isOSee )
        self.h_isOSemu  =ROOT.TH1D('isOSemu', 'isOSemu', 2,-0.5,1.5); self.addObject(self.h_isOSemu )
        self.h_isSSmumu =ROOT.TH1D('isSSmumu', 'isSSmumu', 2,-0.5,1.5); self.addObject(self.h_isSSmumu )
        self.h_isSSee   =ROOT.TH1D('isSSee', 'isSSee', 2,-0.5,1.5); self.addObject(self.h_isSSee )

        ##Gen-level Objects
        genDict={}
        for objects in ["Mu","Elec"]:
            for num in range(1,4):
                key="gen_%s%s" %(objects,num)
                genDict["h_"+key+"pt"]=ROOT.TH1F(key+'pt',   '',   100, 0, 800)
                genDict["h_"+key+"eta"]=ROOT.TH1F(key+'eta',   '',   10, -5.5, 4.5)
                genDict["h_"+key+"phi"]=ROOT.TH1F(key+'phi',   '',   10, 0, 4)
        for key, value in sorted(genDict.iteritems()):
            self.addObject(value)
            
        ## RECO-GEN matched objects
        genrecoDict={}
        for objects in ["Mu","Elec"]:
            for num in range(1,4):
                key="genreco_%s%s" %(objects,num)
                genrecoDict["h_"+key+"pt"]=ROOT.TH1F(key+'pt',   '',   100, 0, 800)
		genrecoDict["h_"+key+"eta"]=ROOT.TH1F(key+'eta',   '',   10, -5.5, 4.5)
                genrecoDict["h_"+key+"phi"]=ROOT.TH1F(key+'phi',   '',   10, 0, 4)
        for key, value in sorted(genrecoDict.iteritems()):
            self.addObject(value)

        #GenW
        self.h_gen_W1pt  = ROOT.TH1F('gen_W1pt',   'Gen-level leading pt W pt',   100, 0, 800);self.addObject(self.h_gen_W1pt )
        self.h_gen_W1eta = ROOT.TH1F('gen_W1eta',   'Gen-level leading pt W eta',   10, -5.5, 4.5);self.addObject(self.h_gen_W1eta )
        self.h_gen_W1phi = ROOT.TH1F('gen_W1phi',   'Gen-level leading pt W phi',   10, 0, 4);self.addObject(self.h_gen_W1phi )

        self.h_gen_Z1pt  = ROOT.TH1F('gen_Z1pt',   'Gen-level leading pt Z pt',   100, 0, 800);self.addObject(self.h_gen_Z1pt )
        self.h_gen_Z1eta = ROOT.TH1F('gen_Z1eta',   'Gen-level leading pt Z eta',   10, -5.5, 4.5);self.addObject(self.h_gen_Z1eta )
        self.h_gen_Z1phi = ROOT.TH1F('gen_Z1phi',   'Gen-level leading pt Z phi',   10, 0, 4);self.addObject(self.h_gen_Z1phi )
        self.h_gen_Zptcorr = ROOT.TH1F('h_genZptcorr',   'Gen-level leading pt GenZpt Correction',   50, -10, 10);self.addObject(self.h_gen_Zptcorr )
        
        ##Reco-level Objects
        self.h_reco_nMu = ROOT.TH1F('reco_nMu',   'Reco-level number of Muon',   15, -0.5, 14.5);self.addObject(self.h_reco_nMu )
        self.h_reco_nEle = ROOT.TH1F('reco_nEle',   'Reco-level number of Electron',   15, -0.5, 14.5);self.addObject(self.h_reco_nEle )
        self.h_reco_nTau = ROOT.TH1F('reco_nTau',   'Reco-level number of Tau',   15, -0.5, 14.5);self.addObject(self.h_reco_nTau )
        self.h_reco_nPho = ROOT.TH1F('reco_nPho',   'Reco-level number of photon',   15, -0.5, 14.5);self.addObject(self.h_reco_nPho )
        self.h_reco_nJet = ROOT.TH1F('reco_nJet',   'Reco-level number of jet',   15, -0.5, 14.5);self.addObject(self.h_reco_nJet )

        recoDict={}
        for objects in ["Mu","Elec","Tau","Pho","Jet"]:
            for num in range(1,4):
                key="reco_%s%s" %(objects,num)
                recoDict["h_"+key+"pt"]=ROOT.TH1F(key+'pt',   '',   100, 0, 800)
		recoDict["h_"+key+"eta"]=ROOT.TH1F(key+'eta',   '',   10, -5.5, 4.5)
                recoDict["h_"+key+"phi"]=ROOT.TH1F(key+'phi',   '',   10, 0, 4)
        for key, value in sorted(recoDict.iteritems()):
            self.addObject(value)

        self.h_reco_Metpt  = ROOT.TH1F('reco_Metpt',   'Reco-level MET pt',   100, 0, 1000); self.addObject(self.h_reco_Metpt )
        self.h_reco_Metet  = ROOT.TH1F('reco_Metet',   'Reco-level MET et',   100, 0, 1000); self.addObject(self.h_reco_Metet )
        self.h_reco_Metphi = ROOT.TH1F('reco_Metphi',   'Reco-level MET phi',   10, 0, 4);   self.addObject(self.h_reco_Metphi )
        
        #Composite Objects
        self.h_vpt=ROOT.TH1F('vpt',   'vpt',   100, 0, 800);self.addObject(self.h_vpt )
        self.h_vmass=ROOT.TH1F('vmass',   'vmass',   100, 0, 200);self.addObject(self.h_vmass )
        
        self.h_htpt  = ROOT.TH1F('htpt',   'Hadronic Activity Pt',   100, 0, 1000);self.addObject(self.h_htpt )
        self.h_htphi  = ROOT.TH1F('htphi',   'Hadronic Activity Pho',   10, 0, 4);self.addObject(self.h_htphi )

        ## GEN signal
        #self.h_w1 =ROOT.TH1D('isOSmumu', 'isOSmumu', 2,-0.5,1.5); self.addObject(self.h_w1 )
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.FilesName=inputFile
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):

        ########################################
        #            READ OBJECTS
        ########################################
        ## PU
        ####
        ## Trigger
        ####
        
        ## Electron
        electrons = Collection(event, "Electron")
        ElecList =filter(lambda x: (x.pt>15 and x.cutBased>3 and x.pfRelIso03_all<0.25), electrons)
        nEle = len(ElecList)

        ## Muon
        muons = Collection(event, "Muon")
        MuonList =filter(lambda x: (x.pt>5 and x.mediumId>0 and x.pfRelIso03_all<0.25), muons)
        nMu =len(MuonList)

        ## Taus
        taus = Collection(event, "Tau")
        TauList =filter(lambda x: (x.pt>5 and fabs(x.eta)<2.5), taus)
        cleanFromlepton(TauList,ElecList)
        cleanFromlepton(TauList,MuonList)
        nTau = len(TauList)
        
        ## Photon
        photons = Collection(event, "Photon")
        PhotonList =filter(lambda x: (x.pt>5 and fabs(x.eta)<2.5), photons)
        cleanFromlepton(PhotonList,ElecList)
        cleanFromlepton(PhotonList,MuonList)
        nPho = len(PhotonList)

        ## Jets
        jets = Collection(event, "Jet")
        JetList =filter(lambda x: (x.pt>30 and fabs(x.eta)<2.5 and x.jetId>0 and x.puId>4), jets)
        #NOTE: cleaning by SSLep analysis Prescription
        cleanFromleptonSS(JetList,ElecList)
        cleanFromleptonSS(JetList,MuonList)
        #cleanFromlepton(JetList,TauList)
        
        nJet = len(JetList)

        #SUMHT
        htObj = ROOT.TLorentzVector()
        for jet in JetList:
            htObj+=jet.p4()
        #htpt = reduce(lambda x, y:x.p4()+y.p4(), JetList)
        self.h_htpt.Fill(htObj.Pt())
        self.h_htphi.Fill(htObj.Phi())
        
        ## MET
        self.h_reco_Metpt.Fill(event.MET_pt)
        self.h_reco_Metphi.Fill(event.MET_phi)
        self.h_reco_Metpt.Fill(event.MET_sumEt)

        ## GenJet
        genjets = Collection(event, "GenJet")
        
        ########################################
        #                GEN LEVEL
        ########################################

        ## Gen Weight
        ####
        ## Lhe Particles
        ####
        ## Mc Stitching
        ####
        ## GenParticle
        if "nGenPart" in event._tree.GetListOfBranches():
            # GEN Particles
            genparts = Collection(event, "GenPart")
            GenLists = filter(lambda x: x, genparts)

            ## GEN candidates objects
            # Gen V
            theGenZ = FindGenParticle(GenLists, [23],22)
            theGenW = FindGenParticle(GenLists, [24,-24],22)
                
            for gen in theGenW:
                #print "pdgId = ", gen.pdgId , " ; pt = ", gen.pt , " ; mon = ", genparts[gen.genPartIdxMother].pdgId
                if genparts[gen.genPartIdxMother].pdgId!=25:
                    self.h_gen_W1pt.Fill(gen.pt)
                    self.h_gen_W1eta.Fill(gen.eta)
                    self.h_gen_W1phi.Fill(gen.phi)
            # Gen Top
            theGenTop = FindGenParticle(GenLists, [6],1)
            theGenAntiTop = FindGenParticle(GenLists, [-6],1)

            # GEN Leptons
            genLepton = FindGenParticle(GenLists, [13,-13,11,-11],1)
            genNeutrino = FindGenParticle(GenLists, [12,-12,14,-14],1)
            genHadron = FindGenParticle(GenLists, [1,2,3,4,5,-1,-2,-3,-4,-5],1)
            
            genLep = filter(lambda x: ( isGenMother(x,[24,-24,25],62,genparts) and (x.pt>5 if abs(x.pdgId)==13 else x.pt>15) ), genLepton)
            
            #GEN-RECO matching
            pairMu=genRecoFinder(genLep,MuonList)
            pairElec=genRecoFinder(genLep,ElecList)

            for num,pair in enumerate(pairMu):

                getattr( self, "gen_Mu%spt" %(num+1) ).Fill(pair[0].pt)
                getattr( self, "gen_Mu%seta" %(num+1) ).Fill(pair[0].eta)
                getattr( self, "gen_Mu%sphi" %(num+1) ).Fill(pair[0].phi)

                getattr( self, "genreco_Mu%spt" %(num+1) ).Fill(pair[1].pt)
		getattr( self, "genreco_Mu%seta" %(num+1) ).Fill(pair[1].eta)
                getattr( self, "genreco_Mu%sphi" %(num+1) ).Fill(pair[1].phi)
                                
            for num,pair in enumerate(pairElec):
                
                getattr( self, "gen_Elec%spt" %(num+1) ).Fill(pair[0].pt)
		getattr( self, "gen_Elec%seta" %(num+1) ).Fill(pair[0].eta)
                getattr( self, "gen_Elec%sphi" %(num+1) ).Fill(pair[0].phi)

                getattr( self, "genreco_Elec%spt" %(num+1) ).Fill(pair[1].pt)
                getattr( self, "genreco_Elec%seta" %(num+1) ).Fill(pair[1].eta)
                getattr( self, "genreco_Elec%sphi" %(num+1) ).Fill(pair[1].phi)
                
            #Perform PtZ correction computation
            Zweight = 1.
            NgenZ=0
            if "DYJetsToLL" in self.FilesName.GetName().split('/')[-1].split('_')[0]:
                for genZ in theGenZ:
                    NgenZ+=1
                    if NgenZ>1: continue
                    Zpt=genZ.pt
                    Zeta=genZ.eta
                    Zphi=genZ.phi
                    #Ugo's Prescription
                    if Zpt<20: Zweight=1.2
                    if Zpt>20 and Zpt<30: Zweight=1.
                    if Zpt>30 and Zpt<40: Zweight=0.75
                    if Zpt>40 and Zpt<50: Zweight=0.65
                    if Zpt>50 and Zpt<200: Zweight=0.65-0.00034*Zpt
                    if Zpt>200: Zweight=0.6
                    self.h_gen_Z1pt.Fill(Zpt)
                    self.h_gen_Z1eta.Fill(Zeta)
                    self.h_gen_Z1phi.Fill(Zphi)
        self.h_genZptcorr.Fill(Zweight)

        ########################################
        #                ANALYSIS               ### TOMORROW CONTINUE HERE
        ########################################
        
        ##Categorization base on number of leptons and flavour combination.
        isOSmumu=0; isOSee=0; isOSemu=0; isSSmumu=0; isSSee=0
        if nMu>=2 or nEle>=2:
            if nMu>=2 and nEle>=2:
                #Leading Pt Muon take precedence
                if MuonList[0].pt > ElecList[0].pt:
                    if MuonList[0].charge!=MuonList[1].charge:
                        isOSmumu=1
                    elif  MuonList[0].charge==MuonList[1].charge:
                        isSSmumu=1
                else:
                    if ElecList[0].charge!=ElecList[0].charge:
                        isOSee=1
                    elif ElecList[0].charge==ElecList[0].charge:
                        isSSee=1
            elif nMu>=2:
                if MuonList[0].charge!=MuonList[1].charge:
                    isOSmumu=1
                elif MuonList[0].charge==MuonList[1].charge:
                    isSSmumu=1
            elif nEle>=2:
                if ElecList[0].charge!=ElecList[0].charge:
                    isOSee=1
                elif ElecList[0].charge==ElecList[0].charge:
                    isSSee=1
        elif nMu==1 and nEle==1:
            if MuonList[0].pt < ElecList[0].pt:
                isOSemu=1

        ########################################
        #       Reconstruction of V boson
        ########################################

        ## Interesting Phase Space
        Vpt=999.
        Vmass=999.
        if isOSmumu or isOSee or isSSmumu or isSSee:
            if isSSmumu or isOSmumu:
                V=MuonList[0].p4()+MuonList[1].p4()
                Vpt=V.Pt()
                Vmass=V.M()

            elif isOSee or isSSee:
                V=ElecList[0].p4()+ElecList[1].p4()
                Vpt=V.Pt()
                Vmass=V.M()
        elif isOSemu:
            V=ElecList[0].p4()+MuonList[0].p4()
            Vpt=V.Pt()
            Vmass=V.M()
        
        ## Fill
        self.h_isOSmumu.Fill(isOSmumu)
        self.h_isOSee.Fill(isOSee)
        self.h_isOSemu.Fill(isOSemu)
        self.h_isSSmumu.Fill(isSSmumu)
        self.h_isSSee.Fill(isSSee)
        
        self.h_vpt.Fill(Vpt)
        self.h_vmass.Fill(Vmass)
        
        ##Filling RECO Object
        self.h_reco_nMu.Fill(nMu)
        self.h_reco_nEle.Fill(nEle)
        self.h_reco_nTau.Fill(nTau)
        self.h_reco_nPho.Fill(nPho)
        self.h_reco_nJet.Fill(nJet)
        
        for collection in [ ElecList , MuonList , TauList , PhotonList , JetList ]:

            for num,reco in enumerate(collection):
                if num>=3: continue
                token="Elec"
                if reco._prefix.split('_')[0]=="Muon":
                    token="Mu"
                elif reco._prefix.split('_')[0]=="Tau":
                    token="Tau"
                elif reco._prefix.split('_')[0]=="Photon":
                    token="Pho"
                elif reco._prefix.split('_')[0]=="Jet":
                    token="Jet"
                elif reco._prefix.split('_')[0]!="Electron":
                    print "ERROR"
                    exit()
                    
                getattr( self, "reco_%s%spt" %(token,num+1) ).Fill(reco.pt)
                getattr( self, "reco_%s%seta" %(token,num+1) ).Fill(reco.eta)
                getattr( self, "reco_%s%sphi" %(token,num+1) ).Fill(reco.phi)

        return True

DIR="/Users/shoh/Projects/CMS/PhD/Analysis/SSL/NANOAOD/"

preselection=""

files=[
    #DIR+"HWminusJ_HToWWTo2L2Nu_WToLNu_M125_13TeV_powheg_pythia8-v1.root",
    #DIR+"HWplusJ_HToWWTo2L2Nu_WToLNu_M125_13TeV_powheg_pythia8-v1.root",
    #DIR+"HWminusJ_HToWW_M125_13TeV_powheg_pythia8-v1.root",
    #DIR+"HWplusJ_HToWW_M125_13TeV_powheg_pythia8-v1.root",
    #DIR+"VHToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8.root",
    DIR+"DYJetsToLL_Pt-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext2-v1.root",
]
nEvent=30000

p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[Analysis()],maxevent=nEvent,noOut=True,histFileName="Flat_"+files[0].split('/')[-1],histDirName="plots")
p.run()
