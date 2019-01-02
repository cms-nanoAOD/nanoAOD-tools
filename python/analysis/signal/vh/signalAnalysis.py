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
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi, deltaR, matchObjectCollectionMultiple

from GenScouting import *

All=[1, 2, 3, 4, 5, 6, 11, 12, 13, 14, 15, 16, 21, 23, 24, 25]

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

        self.h_trigw      = ROOT.TH1F('trigw',   'trigw counter',   5, 0.5, 5.5); VAR.append(self.h_trigw)
        self.h_whqq      = ROOT.TH1F('whqq',   'whqq counter',   5, 0.5, 5.5); VAR.append(self.h_whqq)
        self.h_hwlnu      = ROOT.TH1F('hwlnu',   'hwlnu counter',   5, 0.5, 5.5); VAR.append(self.h_hwlnu)
        
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
        
        #listing
        #if DEBUG: Display(All,All,genparts)

        #preselect leptons
        TightElectron=[]
        for ele in electrons:
            if ele.pt>10 and fabs(ele.eta)<2.5 and ele.cutBased>3:
                TightElectron.append(ele)
        nTightElectron=len(TightElectron)
        
        TightMuon=[]
        for mu in muons:
            if mu.pt>5 and fabs(mu.eta)<2.5 and mu.tightId:
                TightMuon.append(mu)
        nTightMuon=len(TightMuon)

        #Cleaning
        cleanJet=cleanFromLepton(jets,TightMuon)
        cleanJet=cleanFromLepton(cleanJet,TightElectron)
        cleanJet=filter(lambda j : j.pt>25, cleanJet)
        cleanJet=filter(lambda j : fabs(j.eta)<2.5, cleanJet)
        nJets=len(cleanJet)
        
        #Gen List
        subGenparts=filterGenParticle(All,genparts)
        genWcands=daughterFinder(subGenparts,[24],genparts)
        genHWcands=daughterFinder(subGenparts,[25],genparts)
        allgen=genWcands[0]+genHWcands[0]
     
        #match to RECO-level
        #muon
        recoWMuon=recoFinder(muons,allgen)
        recoWElectron=recoFinder(electrons,allgen)
        #recoWjj=recoFinder(cleanJet,allgen,False)
        recoWMuon.sort(key=getPt, reverse=True)
        recoWElectron.sort(key=getPt, reverse=True)
        #recoWjj.sort(key=getPt, reverse=True)

        #if len(recoWMuon)==3:
        #    print "SS MUON"
        #    print "recoWMuon[0].pdgId = ", recoWMuon[0].pdgId
        #    print "recoWMuon[1].pdgId = ", recoWMuon[1].pdgId
        #    print "recoWMuon[2].pdgId = ", recoWMuon[2].pdgId
        #if len(recoWElectron)==3:
        #    print "SS Electron"
        #    print "recoWElectron[0].pdgId = ", recoWElectron[0].pdgId
        #    print "recoWElectron[1].pdgId = ", recoWElectron[1].pdgId
        #    print "recoWElectron[2].pdgId = ", recoWElectron[2].pdgId

        #if len(recoWMuon)==1 and len(recoWElectron)==1:
        #    if recoWMuon[0].pdgId==13 and recoWElectron[0].pdgId==11:
        #        print "OS Muon and Electron"
        #        print "recoWMuon[0].pdgId = ", recoWMuon[0].pdgId
        #        print "recoWElectron[0].pdgId = ", recoWElectron[0].pdgId
            
        return True


preselection=""
skimmed_files=[]

#skimmed_files=["/Users/shoh/Projects/CMS/PhD/Analysis/SSl/NANOAOD/HWplusJ_HToWW_M125_13TeV_powheg_pythia8-v1.root",
#       "/Users/shoh/Projects/CMS/PhD/Analysis/SSl/NANOAOD/HWminusJ_HToWW_M125_13TeV_powheg_pythia8-v1.root"]
skimmed_files=["/Users/shoh/Projects/CMS/PhD/Analysis/SSl/NANOAOD/VHToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8.root"]

#files=["/Users/shoh/Projects/CMS/PhD/Analysis/SSl/NANOAOD/VHToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8.root"]

#for f in files:
#    skimmed_files.append(f.split("/")[-1].split(".")[0]+"_Skim.root")

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
