#!/usr/bin/env python
import os, sys
import ROOT
from math import fabs, cos, sin, tan, atan, exp, sqrt
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.operational.cleaningStudy import cleaningStudy
#import PhysicsTools.NanoAODTools.postprocessing.operational.cleaningStudy

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi, deltaR

from GenScouting import *

Mlep=[13,-13]
Mneu=[14,-14]
Elep=[11,-11]
Eneu=[12,-12]
Tlep=[15,-15]
Tneu=[16,-16]
lightquarks=[21,1,2,3,4,-1,-2,-3,-4]
bquarks=[-5,5]
Wboson=[24,-24]
Hboson=[25]
Zboson=[23]
FinalState=[62,44,22]

DEBUG=False

def getPt(pO):
    return pO.pt

class signalAnalysis(Module):
    def __init__(self):
	self.writeHistFile=True

    def beginJob(self,histFile=None,histDirName=None):
	Module.beginJob(self,histFile,histDirName)
        VAR=[]
        #Global Variable
        self.h_nevent = ROOT.TH1D('nevent', 'nevent', 2, 0.5, 1.5); VAR.append(self.h_nevent)
        self.h_whww    = ROOT.TH1F('whww',   'whww counter',   2, 0.5, 1.5); VAR.append(self.h_whww)
        self.h_hww      = ROOT.TH1F('hww',   'hww counter',   2, 0.5, 1.5); VAR.append(self.h_hww)
        self.h_hw    = ROOT.TH1F('hw',   'hw counter',   2, 0.5, 1.5); VAR.append(self.h_hw)
        self.h_wh    = ROOT.TH1F('wh',   'wh counter',   2, 0.5, 1.5); VAR.append(self.h_wh)

        self.h_zhzz    = ROOT.TH1F('zhzz',   'zhzz counter',   2, 0.5, 1.5); VAR.append(self.h_zhzz)
        self.h_hzz      = ROOT.TH1F('hzz',   'hzz counter',   2, 0.5, 1.5); VAR.append(self.h_hzz)
        self.h_hz    = ROOT.TH1F('hz',   'hz counter',   2, 0.5, 1.5); VAR.append(self.h_hz)
        self.h_zh    = ROOT.TH1F('zh',   'zh counter',   2, 0.5, 1.5); VAR.append(self.h_zh)
        
        #Kinematics of Physics Objects
        #leading Pt of Muon
        self.h_m1pt = ROOT.TH1D('m1pt', 'Leading Muon Pt', 25, 0, 800); VAR.append(self.h_m1pt)
        self.h_m1eta = ROOT.TH1D('m1eta', 'Leading Muon Eta', 10, -4.5, 5.5); VAR.append(self.h_m1eta)
        self.h_m1phi = ROOT.TH1D('m1phi', 'Leading Muon Phi', 10, 0, 3.5); VAR.append(self.h_m1phi)
        self.h_m1ch = ROOT.TH1D('m1ch', 'Leading Muon Charge', 3, -1.5, 1.5); VAR.append(self.h_m1ch)

        #leading Pt of Electron
        self.h_e1pt = ROOT.TH1D('e1pt', 'Leading Electron Pt', 25, 0, 800); VAR.append(self.h_e1pt)
	self.h_e1eta = ROOT.TH1D('e1eta', 'Leading Electron Eta', 10, -4.5, 5.5); VAR.append(self.h_e1eta)
        self.h_e1phi = ROOT.TH1D('e1phi', 'Leading Electron Phi', 10, 0, 3.5); VAR.append(self.h_e1phi)
        self.h_e1ch = ROOT.TH1D('e1ch', 'Leading Electron Charge', 3, -1.5, 1.5); VAR.append(self.h_e1ch)

        #leading Pt of Jet
        self.h_j1pt = ROOT.TH1D('j1pt', 'Leading Jet Pt', 25, 0, 800); VAR.append(self.h_j1pt)
	self.h_j1eta = ROOT.TH1D('j1eta', 'Leading Jet Eta', 10, -4.5, 5.5); VAR.append(self.h_j1eta)
        self.h_j1phi = ROOT.TH1D('j1phi', 'Leading Jet Phi', 10, 0, 3.5); VAR.append(self.h_j1phi)

        #Subleading Pt of Muon
        self.h_m2pt = ROOT.TH1D('m2pt', 'Subleading Muon Pt', 25, 0, 800); VAR.append(self.h_m2pt)
	self.h_m2eta = ROOT.TH1D('m2eta', 'Subleading Muon Eta', 10, -4.5, 5.5); VAR.append(self.h_m2eta)
        self.h_m2phi = ROOT.TH1D('m2phi', 'Subleading Muon Phi', 10, 0, 3.5); VAR.append(self.h_m2phi)
        self.h_m2ch = ROOT.TH1D('m2ch', 'SubLeading Muon Charge', 3, -1.5, 1.5); VAR.append(self.h_m2ch)

        #Subleading Pt of Electron
        self.h_e2pt = ROOT.TH1D('e2pt', 'SubLeading Electron Pt', 25, 0, 800); VAR.append(self.h_e2pt)
	self.h_e2eta = ROOT.TH1D('e2eta', 'SubLeading Electron Eta', 10, -4.5, 5.5); VAR.append(self.h_e2eta)
        self.h_e2phi = ROOT.TH1D('e2phi', 'SubLeading Electron Phi', 10, 0, 3.5); VAR.append(self.h_e2phi)
        self.h_e2ch = ROOT.TH1D('e2ch', 'SubLeading Electron Charge', 3, -1.5, 1.5); VAR.append(self.h_e2ch)

        #Subleading Pt of Jet
        self.h_j2pt = ROOT.TH1D('j2pt', 'SubLeading Jet Pt', 25, 0, 800); VAR.append(self.h_j2pt)
	self.h_j2eta = ROOT.TH1D('j2eta', 'SubLeading Jet Eta', 10, -4.5, 5.5); VAR.append(self.h_j2eta)
        self.h_j2phi = ROOT.TH1D('j2phi', 'SubLeading Jet Phi', 10, 0, 3.5); VAR.append(self.h_j2phi)

        #SubSubleading Pt of Jet                                                                                                     
        self.h_j3pt = ROOT.TH1D('j3pt', 'SubSubLeading Jet Pt', 25, 0, 800); VAR.append(self.h_j3pt)
	self.h_j3eta = ROOT.TH1D('j3eta', 'SubSubLeading Jet Eta', 10, -4.5, 5.5); VAR.append(self.h_j3eta)
        self.h_j3phi = ROOT.TH1D('j3phi', 'SubSubLeading Jet Phi', 10, 0, 3.5); VAR.append(self.h_j3phi)

        ### Boson Kinematics ###
        #Triggering W boson, W -> lnu
        self.h_w1pt = ROOT.TH1D('w1pt', 'Triggered Leptonic W boson Pt', 25, 0, 1000); VAR.append(self.h_w1pt)
        self.h_w1eta = ROOT.TH1D('w1eta', 'Triggered Leptonic W boson Eta', 10, -4.5, 5.5); VAR.append(self.h_w1eta)
        self.h_w1phi = ROOT.TH1D('w1phi', 'Triggered Leptonic W boson Phi', 10, 0, 3.5); VAR.append(self.h_w1phi)
        self.h_w1ch = ROOT.TH1D('w1ch', 'Triggered Leptonic W boson Charge', 3, -1.5, 1.5); VAR.append(self.h_w1ch)
        self.h_w1mass = ROOT.TH1D('w1mass', 'Triggered Leptonic W boson Mass', 25, 0, 500); VAR.append(self.h_w1mass)
        
        #Leptonic W, W -> lnu
        self.h_w2pt = ROOT.TH1D('w2pt', 'Leptonic W boson Pt', 25, 0, 1000); VAR.append(self.h_w2pt)
        self.h_w2eta = ROOT.TH1D('w2eta', 'Leptonic W boson Eta', 10, -4.5, 5.5); VAR.append(self.h_w2eta)
        self.h_w2phi = ROOT.TH1D('w2phi', 'Leptonic W boson Phi', 10, 0, 3.5); VAR.append(self.h_w2phi)
        self.h_w2ch = ROOT.TH1D('w2ch', 'Leptonic W boson Charge', 3, -1.5, 1.5); VAR.append(self.h_w2ch)
        self.h_w2mass = ROOT.TH1D('w2mass', 'Leptonic W boson Mass', 25, 0, 500); VAR.append(self.h_w2mass)

        #Hadronic W, W -> jj
        self.h_w3pt = ROOT.TH1D('w3pt', 'Hadronic W boson Pt', 25, 0, 1000); VAR.append(self.h_w3pt)
	self.h_w3eta = ROOT.TH1D('w3eta', 'Hadronic W boson Eta', 10, -4.5, 5.5); VAR.append(self.h_w3eta)
        self.h_w3phi = ROOT.TH1D('w3phi', 'Hadronic W boson Phi', 10, 0, 3.5); VAR.append(self.h_w3phi)
        self.h_w3ch = ROOT.TH1D('w3ch', 'Hadronic W boson Charge', 3, -1.5, 1.5); VAR.append(self.h_w3ch)
        self.h_w3mass = ROOT.TH1D('w3mass', 'Hadronic W boson Mass', 25, 0, 500); VAR.append(self.h_w3mass)

        #WH
        self.h_w4pt = ROOT.TH1D('w4pt', 'WH W boson Pt', 25, 0, 1000); VAR.append(self.h_w4pt)
        self.h_w4eta = ROOT.TH1D('w4eta', 'WH W boson Eta', 10, -4.5, 5.5); VAR.append(self.h_w4eta)
        self.h_w4phi = ROOT.TH1D('w4phi', 'WH W boson Phi', 10, 0, 3.5); VAR.append(self.h_w4phi)
        self.h_w4ch = ROOT.TH1D('w4ch', 'WH W boson Charge', 3, -1.5, 1.5); VAR.append(self.h_w4ch)
        self.h_w4mass = ROOT.TH1D('w4mass', 'WH W boson Mass', 25, 0, 500); VAR.append(self.h_w4mass)

        #Higgs, Higgs-> W+ W-
        self.h_h1pt = ROOT.TH1D('h1pt', 'Higgs boson Pt', 25, 0, 1000); VAR.append(self.h_h1pt)
        self.h_h1eta = ROOT.TH1D('h1eta', 'Higgs boson Eta', 10, -4.5, 5.5); VAR.append(self.h_h1eta)
        self.h_h1phi = ROOT.TH1D('h1phi', 'Higgs boson Phi', 10, 0, 3.5); VAR.append(self.h_h1phi)
        self.h_h1ch = ROOT.TH1D('h1ch', 'Higgs boson Charge', 3, -1.5, 1.5); VAR.append(self.h_h1ch)
        self.h_h1mass = ROOT.TH1D('h1mass', 'Higgs boson Mass', 25, 0, 500); VAR.append(self.h_h1mass)

        for obj in VAR:
            self.addObject(obj)

    def endJob(self):
        Module.endJob(self)                
        
    def analyze(self, event): #Each event operation
        #self.Nevents+=1
        if DEBUG: print "Begin Events ======"
        #READ Collection
        electrons    = Collection(event, "Electron")
        muons        = Collection(event, "Muon")
        jets         = Collection(event, "Jet")
        genparts     = Collection(event, "GenPart")
        gendressleps = Collection(event, "GenDressedLepton")
        genjets      = Collection(event, "GenJet" )
        genjetak8s   = Collection(event, "GenJetAK8")
        
        #genmets      = event.GenMET

        #READ Vector
        JetE= Object(event,"JetE")
        dRMuJet= Object(event,"dRMuJet")
        dRElJet= Object(event,"dRElJet")

        #READ Scalar
        nGoodJet= event.nGoodJet
        nGoodMuon= event.nGoodMuon
        nGoodElectron= event.nGoodElectron
        nGoodTau= event.nGoodTau
        nGoodPhoton= event.nGoodPhoton

        isOSmumu= event.isOSmumu
        isOSemu= event.isOSemu
        isSSmumu= event.isSSmumu

        HTpt= event.HTpt
        HTphi= event.HTphi
        Zweight= event.Zweight

        ##
        genMuon = []
        genElectron = []
        genJet = []
        genBJet = []
        genW = []
        genH = []
        genZ = []
        genMneu = []
        genEneu = []
        for gen in genparts:
            if gen.pdgId in Mlep and gen.status==1:
                genMuon.append(gen)
            if gen.pdgId in Elep and gen.status==1:
                genElectron.append(gen)
            if gen.pdgId in lightquarks and gen.status==1:
                genJet.append(gen)
            if gen.pdgId in bquarks and gen.status==1:
                genBJet.append(gen)
            if gen.pdgId in Zboson:
                genZ.append(gen)
            if gen.pdgId in Wboson: #and gen.status==62:
                genW.append(gen)
            if gen.pdgId in Hboson: #and gen.status==62:
                genH.append(gen)
            if gen.pdgId in Mneu and gen.status==1:
                genMneu.append(gen)
            if gen.pdgId in Eneu and gen.status==1:
                genEneu.append(gen)

        #Pt ordered at descending order 
        genMuon.sort(key=getPt, reverse=True)
        genElectron.sort(key=getPt, reverse=True)
        genJet.sort(key=getPt, reverse=True)
        genBJet.sort(key=getPt, reverse=True)
        genW.sort(key=getPt, reverse=True)
        genZ.sort(key=getPt, reverse=True)
        genH.sort(key=getPt, reverse=True)
        genMneu.sort(key=getPt, reverse=True)
        genEneu.sort(key=getPt, reverse=True)

        ##scouting
        #DaughterList ; Motherlist
        Display(Mlep+Mneu+Elep+Eneu,Wboson+Tlep+Tneu,genparts)
        
        #Muon final states
        #Trigger W has status 62 --> 44 --> 22
        #W from Higgs has status 22 (W) --> 62 (H) --> 44 (H) --> 22 (H)  
        wtriggered=False
        wleptonic1=False
        wleptonic2=False
        nwleptonic=0
        
        ztriggered=False
        zleptonic1=False
        zleptonic2=False
        nzleptonic=0

        whww=0
        hww=0
        hw=0
        wh=0

        zhzz=0
        hzz=0
        hz=0
        zh=0
        
        Wsign=[]
        Zsign=[]
        ZMuSign=[]

        GenMuonIndex=[]
        for num,gen in enumerate(genMuon):
            if DEBUG: print "With daughter ",num,"th gen with pdgId : ", gen.pdgId ,", status : ", gen.status,", mass : ", gen.mass,", statusFlags : ", gen.statusFlags
            #Trigger W has status 62 --> 44 --> 22
            #62--> (outgoing subprocess particle with primordial kT included) particles produced by beam-remnant treatment
            #44--> (outgoing shifted by a branching) particles produced by initial-state-showers
            #22--> (outgoing) particles of the hardest subprocess
            
            ### WBOSON CANDIDATE
            moId=gen.genPartIdxMother
            if genparts[moId].pdgId in Wboson and genparts[moId].status==62:
                if DEBUG: print WARNING,"Trigger W has status 62 --> 44 --> 22",ENDC
                if DEBUG: print "With Mother pdgId : ", genparts[moId].pdgId,", status : ", genparts[moId].status,", mass : ", genparts[moId].mass,", statusFlags : ", genparts[moId].statusFlags
                moId1=genparts[moId].genPartIdxMother
                if genparts[moId1].pdgId in Wboson and genparts[moId1].status in FinalState:
                    if DEBUG: print "With 1st grandmother pdgId : ", genparts[moId1].pdgId,", status : ", genparts[moId1].status,", mass : ", genparts[moId1].mass,", statusFlags : ", genparts[moId1].statusFlags
                    moId2=genparts[moId1].genPartIdxMother
                    if genparts[moId2].pdgId in Wboson and genparts[moId1].status in FinalState:
                        if DEBUG: print "With 2nd grandmother pdgId : ", genparts[moId2].pdgId,", status : ", genparts[moId2].status,", mass : ", genparts[moId2].mass,", statusFlags : ", genparts[moId2].statusFlags
                        if DEBUG: print OKGREEN,"Jackpot",ENDC
                        wtriggered=True
                        whww+=1
                        wh+=1
                        
            #W from Higgs has status 22 (W) --> 62 (H) --> 44 (H) --> 22 (H)
            elif genparts[moId].pdgId in Wboson and genparts[moId].status==22:
                if DEBUG: print	WARNING,"W from Higgs has status 22 (W) --> 62 (H) --> 44 (H) --> 22 (H)",ENDC
                if DEBUG: print "With Mother pdgId : ", genparts[moId].pdgId,", status : ", genparts[moId].status,", mass : ", genparts[moId].mass,", status\
Flags : ", genparts[moId].statusFlags
                Wsign.append(genparts[moId].pdgId)
                moId1=genparts[moId].genPartIdxMother
                if genparts[moId1].pdgId in Hboson and genparts[moId1].status in FinalState:
                    if DEBUG: print "With 1st grandmother pdgId : ", genparts[moId1].pdgId,", status : ", genparts[moId1].status,", mass : ", genparts[moId1].mass,", statusFlags : ", genparts[moId1].statusFlags
                    moId2=genparts[moId1].genPartIdxMother
                    if genparts[moId1].pdgId in Hboson and genparts[moId1].status in FinalState:
                        if DEBUG: print "With 2nd grandmother pdgId : ", genparts[moId1].pdgId,", status : ", genparts[moId1].status,", mass : ", genparts[moId1].mass,", statusFlags : ", genparts[moId1].statusFlags
                        nwleptonic+=1
                        if nwleptonic==1:
                            wleptonic1=True
                            whww+=1
                            hww+=1
                            hw+=1
                            if DEBUG: print OKBLUE,"Found 1 W leptonically decay from Higgs",ENDC
                        elif nwleptonic==2:
                            if len(Wsign)==2 and Wsign[0]+Wsign[1]==0:
                                wleptonic2=True
                                whww+=1
                                hww+=1
                                if DEBUG: print OKGREEN,"Jackpot! Found 2 W leptonically decay from Higgs",ENDC
                        elif nleptonic>2:
                            print FAIL,"something wrong, you have three W",ENDC
                            exit()
            else:
                if DEBUG: print FAIL,"Uninterested Muon decay from :",ENDC
                if DEBUG: print FAIL,"With Mother pdgId : ", genparts[moId].pdgId,", status : ", genparts[moId].status,", mass : ", genparts[moId].mass,", statusFlags : ", genparts[moId].statusFlags,ENDC
                        
        self.h_nevent.Fill(1)
        if DEBUG: print "End Events ======"
        if whww==3:
            if DEBUG: print "WHWW = ", whww
            self.h_whww.Fill(1)
            #exit()
        if wh==1:
            self.h_wh.Fill(1)
        if hww==2:
            self.h_hww.Fill(1)
        if hw==1:
            self.h_hw.Fill(1)

            
        return True


preselection=""
skimmed_files=[]

files=["/Users/shoh/Projects/CMS/PhD/Analysis/SSl/NANOAOD/HWplusJ_HToWW_M125_13TeV_powheg_pythia8-v1.root",
       "/Users/shoh/Projects/CMS/PhD/Analysis/SSl/NANOAOD/HWminusJ_HToWW_M125_13TeV_powheg_pythia8-v1.root"]

#files=["/Users/shoh/Projects/CMS/PhD/Analysis/SSl/NANOAOD/VHToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8.root"]

for f in files:
    skimmed_files.append(f.split("/")[-1].split(".")[0]+"_Skim.root")

print skimmed_files

mod=import_module('PhysicsTools.NanoAODTools.postprocessing.operational.cleaningStudy')
obj = sys.modules['PhysicsTools.NanoAODTools.postprocessing.operational.cleaningStudy']
nevent=10000

#Producer=PostProcessor(".",files,cut=preselection,branchsel="keep_and_drop_VH.txt",modules=[getattr(obj,'cleaning')()],maxevent=nevent)
Analyzer=PostProcessor(".",skimmed_files,cut=preselection,branchsel=None,modules=[signalAnalysis()],maxevent=nevent,noOut=True,histFileName="VH.root",histDirName="plots")

#for p in [Producer,Analyzer]:
for p in [Analyzer]:
    print "Running ", p
    p.run()
