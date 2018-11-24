#!/usr/bin/env python
import os, sys
import ROOT
from math import fabs, cos, sin, tan, atan, exp, sqrt
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor


from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi, deltaR

class ExampleAnalysis(Module):
    def __init__(self):
	self.writeHistFile=True

    def beginJob(self,histFile=None,histDirName=None):
	Module.beginJob(self,histFile,histDirName)

	#self.h_vpt=ROOT.TH1F('sumpt',   'sumpt',   100, 0, 1000)
        #self.addObject(self.h_vpt )

        self.h_Ncj=ROOT.TH1D('NcleanJet',   'NcleanJet',   10, 0, 10)
        self.addObject(self.h_Ncj )
        
    def analyze(self, event):
        #eventSum = ROOT.TLorentzVector()

        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        genparts = Collection(event, "GenPart")

	#select events with at least 2 muons
	#if len(muons) >=2 :
	#  for lep in muons :     #loop on muons
        #    eventSum += lep.p4()
        #  for lep in electrons : #loop on electrons
        #    eventSum += lep.p4()
        #  for j in jets :       #loop on jets
        #    eventSum += j.p4()
        #  self.h_vpt.Fill(eventSum.Pt()) #fill histogram

        # Cleaning Jet
        Jet_Clean=[0]*len(jets)
        Jetpx=[0.]*len(jets)
        Jetpy=[0.]*len(jets)
        Jetpz=[0.]*len(jets)
        JetE=[0.]*len(jets)
        nGoodJet=0
        for num,jet in enumerate(jets) :
            Jet_Clean[num]=1
            Jetpx[num] = jet.pt * cos( jet.phi )
            Jetpy[num] = jet.pt * sin( jet.phi )
            Jetpz[num] = jet.pt / tan( 2 * atan( exp( -jet.eta ) ) )
            JetE[num]  = sqrt ( jet.pt* jet.pt + Jetpz[num]* Jetpz[num] )

            if fabs(jet.eta)>2.5: continue

            ##Cleaning each muon match within 0.4
            for numm,lep in enumerate(muons):
                if lep.pt<5.: continue
                if lep.mediumId==0: continue
                if deltaR(jet,lep) < 0.4:
                    Jet_Clean[num]=0
                    #it could be B-jet; b->muon+nu_mu ; b->electron+nu_ele
                    if jet.chHEF>0.15: Jet_Clean[num]=1
                    if jet.neHEF>0.15: Jet_Clean[num]=1
                    if jet.chHEF<0.1 and jet.neHEF>0.2: Jet_Clean[num]=1
                    if jet.puId==4 : Jet_Clean[num]=0
                    if jet.btagCMVA>0.8: Jet_Clean[num]=1

            for nummm,lep in enumerate(electrons):
                if lep.pt<15.: continue
                if lep.cutBased<4: continue
                if deltaR(jet,lep) < 0.4:
                    Jet_Clean[num]=0
                    if jet.chHEF>0.1: Jet_Clean[num]=1
                    if jet.chHEF<0.1 and jet.neHEF>0.2: Jet_Clean[num]=1
            if Jet_Clean[num]==1: nGoodJet+=1

        # Compute nearest distance between lepton and jets
        dRMuJet=[999.]*len(muons)
        dRElJet=[999.]*len(electrons)
        drm=999.
        dre=999.
        nGoodMuon=0
        nGoodElectron=0
        for numm,lep in enumerate(muons):
            if lep.mediumId==1: nGoodMuon+=1
            for njet,jet in enumerate(jets) :
                if Jet_Clean[njet]==0: continue
                dR=deltaR(lep,jet)
                if dR < dRMuJet:
                    drm = dR
            dRMuJet[numm]=drm

        for nummm,lep in enumerate(electrons):
            if lep.cutBased> 3: nGoodElectron+=1
            for njet,jet in enumerate(jets) :
                if Jet_Clean[njet]==0: continue
                dR=deltaR(lep,jet)
                if dR < dRElJet:
                    dre = dR
            dRElJet[nummm]=dre


        # HT Computation
        HTpt=0.
        HTphi=0.
        for num, jet in enumerate(jets):
            if jet.puId==4: continue
            if Jet_Clean[num]==0: continue
            if jet.pt<30.: continue # taken at 30 GeV                                                                                                                                 
            if fabs(jet.eta)>2.5: continue
            HTpt+=jet.pt
            HTphi+=jet.phi

        self.h_Ncj.Fill(nGoodJet)

        return True


preselection=""
files=["/Users/shoh/Projects/CMS/PhD/Analysis/SSl/NANOAOD/HWplusJ_HToWW_M125_13TeV_powheg_pythia8-v1.root",
       "/Users/shoh/Projects/CMS/PhD/Analysis/SSl/NANOAOD/HWminusJ_HToWW_M125_13TeV_powheg_pythia8-v1.root"]
p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[ExampleAnalysis()],noOut=True,histFileName="histOut.root",histDirName="plots")
p.run()
