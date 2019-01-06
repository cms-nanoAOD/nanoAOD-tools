#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from math import fabs
from PhysicsTools.NanoAODTools.analysis.helper.Cleaner import *

class Analysis(Module):
    def __init__(self):
	self.writeHistFile=True

    def beginJob(self,histFile=None,histDirName=None):
	Module.beginJob(self,histFile,histDirName)

	self.h_vpt=ROOT.TH1F('vpt',   'vpt',   100, 0, 800);self.addObject(self.h_vpt )
        self.h_vmass=ROOT.TH1F('vmass',   'vmass',   100, 0, 200);self.addObject(self.h_vmass )

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
        ElecList =filter(lambda x: (x.pt>10 and fabs(x.eta)<2.5 and x.cutBased==4), electrons)
        nElecList=len(ElecList)

        ## Muon
        muons = Collection(event, "Muon")
        MuonList =filter(lambda x: (x.pt>5 and fabs(x.eta)<2.5 and x.mediumId), muons)
        nMuonList=len(MuonList)

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
        nPhoton = len(PhotonList)

        ## Jets
        jets = Collection(event, "Jet")
        JetList =filter(lambda x: (x.pt>30 and fabs(x.eta)<2.5 and x.jetId>=2), jets)
        cleanFromlepton(JetList,ElecList)
        cleanFromlepton(JetList,MuonList)
        nJet = len(JetList)

        ## MET
        #METpt = event.MET_pt

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
        GEN=False
        for branch in event._tree.GetListOfBranches():
            if( branch.GetName() == "nGenPart" ):
                GEN=True
                break
        if GEN:
            # GEN Particles
            genparts = Collection(event, "GenPart")
            GenLists = filter(lambda x: x, genparts)
            # GEN candidates objects with status code 62
            theGenZ = FindGenParticle(GenLists, 23)
            theGenW = FindGenParticle(GenLists, 24)
            theGenTop = FindGenParticle(GenLists, 6)
            theGenAntiTop = FindGenParticle(GenLists, -6)
            # EWK Correction
            #####
            # TopPtReweighting correction
            #####
            
            ##Fill
            #if (theGenZ):
            #    ##FILL
            #if (theGenW):
            #    ##FILL
            
        ########################################
        #                ANALYSIS                                                   
        ######################################## 

        ##Categorization base on number of leptons and flavour combination.
        isOSmumu=False
        isOSee=False
        isOSemu=False
        isSSmumu=False
        isSSee=False
        #More then two lepton final state
        if nElecList>=2 or nMuonList>=2:
            if nElecList>=2 and nMuonList>=2:
                if MuonList[0].pt > ElecList[0].pt:
                    # same sign muon
                    if abs(MuonList[0].charge+MuonList[1].charge)==2:
                        isSSmumu=True
                    # opposite sign muon
                    elif abs(MuonList[0].charge+MuonList[1].charge)==0:
                        isOSmumu=True
                else:
                    # same sign electron
                    if abs(ElecList[0].charge+ElecList[1].charge)==2:
                        isSSee=True
                    # opposite sign electron
                    elif abs(ElecList[0].charge+ElecList[1].charge)==0:
                        isOSee=True
        # One lepton final state
        elif nElecList==1 or nMuonList==1:
            if nElecList==1 and nMuonList==1:
                # opposite sign; opposite flavor ; by construction electron is leading
                if abs(MuonList[0].charge+ElecList[0].charge)==0 and ElecList[0].pt > MuonList[0].pt:
                    isOSemu=True

        ########################################
        #       Reconstruction of V boson
        ########################################
                    
        ##Taking on only leading candidate 
        if isSSmumu or isOSmumu:
            Vpt = invariantMassPt(\
                MuonList[0].pt, MuonList[0].eta , MuonList[0].phi, MuonList[0].mass \
                    ,MuonList[1].pt, MuonList[1].eta , MuonList[1].phi, MuonList[1].mass \
                    )
            Vmass = invariantMass(\
                MuonList[0].pt, MuonList[0].eta , MuonList[0].phi, MuonList[0].mass \
                    ,MuonList[1].pt, MuonList[1].eta , MuonList[1].phi, MuonList[1].mass \
                    )
        elif isSSee or isOSee:
            Vpt = invariantMassPt(\
                ElecList[0].pt, ElecList[0].eta , ElecList[0].phi, ElecList[0].mass \
                    ,ElecList[1].pt, ElecList[1].eta , ElecList[1].phi, ElecList[1].mass \
                    )
            Vmass = invariantMass(\
                ElecList[0].pt, ElecList[0].eta , ElecList[0].phi, ElecList[0].mass \
                    ,ElecList[1].pt, ElecList[1].eta , ElecList[1].phi, ElecList[1].mass \
                    )
        elif isOSemu:
            Vpt = invariantMassPt(\
                ElecList[0].pt, ElecList[0].eta , ElecList[0].phi, ElecList[0].mass \
                    ,MuonList[0].pt, MuonList[0].eta , MuonList[0].phi, MuonList[0].mass \
                )
            Vmass = invariantMass(\
                ElecList[0].pt, ElecList[0].eta , ElecList[0].phi, ElecList[0].mass \
                    ,MuonList[0].pt, MuonList[0].eta , MuonList[0].phi, MuonList[0].mass \
                    )
        else:
            return False

        self.h_vpt.Fill(Vpt)
        self.h_vmass.Fill(Vmass)

        return True

preselection="Jet_pt[0] > 30"
files=["/Users/shoh/Project/Analysis/SSLep/NANOAOD/HWminusJ_HToWWTo2L2Nu_WToLNu_M125_13TeV_powheg_pythia8-v1.root"]
p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[Analysis()],noOut=True,histFileName="histOut.root",histDirName="plots")
p.run()
