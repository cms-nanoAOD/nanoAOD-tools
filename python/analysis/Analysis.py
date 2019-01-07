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
from PhysicsTools.NanoAODTools.analysis.helper.GenScouting import *

class Analysis(Module):
    def __init__(self):
	self.writeHistFile=True

    def beginJob(self,histFile=None,histDirName=None):
	Module.beginJob(self,histFile,histDirName)

        self.h_isOSmumu =ROOT.TH1D('isOSmumu', 'isOSmumu', 2,-0.5,1.5); self.addObject(self.h_isOSmumu )
        self.h_isOSee   =ROOT.TH1D('isOSee', 'isOSee', 2,-0.5,1.5); self.addObject(self.h_isOSee )
        self.h_isOSemu  =ROOT.TH1D('isOSemu', 'isOSemu', 2,-0.5,1.5); self.addObject(self.h_isOSemu )
        self.h_isSSmumu =ROOT.TH1D('isSSmumu', 'isSSmumu', 2,-0.5,1.5); self.addObject(self.h_isSSmumu )
        self.h_isSSee   =ROOT.TH1D('isSSee', 'isSSee', 2,-0.5,1.5); self.addObject(self.h_isSSee )

	self.h_vpt=ROOT.TH1F('vpt',   'vpt',   100, 0, 800);self.addObject(self.h_vpt )
        self.h_vmass=ROOT.TH1F('vmass',   'vmass',   100, 0, 200);self.addObject(self.h_vmass )

        ## GEN signal
        #self.h_w1 =ROOT.TH1D('isOSmumu', 'isOSmumu', 2,-0.5,1.5); self.addObject(self.h_w1 )

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
            theGenZ = FindGenParticle(GenLists, [23,-23])
            theGenW = FindGenParticle(GenLists, [24,-24])
            theGenTop = FindGenParticle(GenLists, [6])
            theGenAntiTop = FindGenParticle(GenLists, [-6])

            #byID
            # w -> ll (62)
            # h -> w -> ll (22)
            theGenW1 = FindGenParticlebyStatus(GenLists, [24,-24], 62)
            theGenW2 = FindGenParticlebyStatus(GenLists, [24,-24], 22)

            if len(theGenW)>0:
                print "===EVENT START==="
                print "NtheGenZ = ", len(theGenZ)
                print "NtheGenW = ", len(theGenW)
                print "NtheGenTop = ", len(theGenTop)
                print "NtheGenAntiTop = ", len(theGenAntiTop)
                print "===EVENT END==="

            if len(theGenW1)>0 or len(theGenW2)>0:
                print "===EVENT START==="
                print "NtheGenW1 = ", len(theGenW1)
                print "NtheGenW2 = ", len(theGenW2)
                print "===EVENT END==="

            # EWK Correction
            #####
            # TopPtReweighting correction
            #####
            
            ##Fill
            #if (theGenZ):
            #    ##FILL
            #if (theGenW):
            #    ##FILL

            ## SIGNAL STUDY
            
            
        ########################################
        #                ANALYSIS                                                   
        ######################################## 

        ##Categorization base on number of leptons and flavour combination.
        isOSmumu=0; isOSee=0; isOSemu=0; isSSmumu=0; isSSee=0
        #More then two lepton final state
        if nElecList>=2 or nMuonList>=2:
            if nElecList>=2 and nMuonList>=2:
                if MuonList[0].pt > ElecList[0].pt:
                    # same sign muon
                    if abs(MuonList[0].charge+MuonList[1].charge)==2:
                        isSSmumu=1
                    # opposite sign muon
                    elif abs(MuonList[0].charge+MuonList[1].charge)==0:
                        isOSmumu=1
                else:
                    # same sign electron
                    if abs(ElecList[0].charge+ElecList[1].charge)==2:
                        isSSee=1
                    # opposite sign electron
                    elif abs(ElecList[0].charge+ElecList[1].charge)==0:
                        isOSee=1
        # One lepton final state
        elif nElecList==1 or nMuonList==1:
            if nElecList==1 and nMuonList==1:
                # opposite sign; opposite flavor ; by construction electron is leading
                if abs(MuonList[0].charge+ElecList[0].charge)==0 and ElecList[0].pt > MuonList[0].pt:
                    isOSemu=1

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
        
        ## Fill
        self.h_isOSmumu.Fill(isOSmumu)
        self.h_isOSee.Fill(isOSee)
        self.h_isOSemu.Fill(isOSemu)
        self.h_isSSmumu.Fill(isSSmumu)
        self.h_isSSee.Fill(isSSee)

        self.h_vpt.Fill(Vpt)
        self.h_vmass.Fill(Vmass)

        return True

preselection="Jet_pt[0] > 30"
files=["/Users/shoh/Project/Analysis/SSLep/NANOAOD/HWminusJ_HToWWTo2L2Nu_WToLNu_M125_13TeV_powheg_pythia8-v1.root"]
p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[Analysis()],noOut=True,histFileName="histOut.root",histDirName="plots")
p.run()
