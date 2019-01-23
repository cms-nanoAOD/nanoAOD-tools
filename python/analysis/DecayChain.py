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

class DecayChain(Module):
    def __init__(self):
	self.writeHistFile=True

    def beginJob(self,histFile=None,histDirName=None):
	Module.beginJob(self,histFile,histDirName)

        '''
        self.h_isOSmumu =ROOT.TH1D('isOSmumu', 'isOSmumu', 2,-0.5,1.5); self.addObject(self.h_isOSmumu )
        self.h_isOSee   =ROOT.TH1D('isOSee', 'isOSee', 2,-0.5,1.5); self.addObject(self.h_isOSee )
        self.h_isOSemu  =ROOT.TH1D('isOSemu', 'isOSemu', 2,-0.5,1.5); self.addObject(self.h_isOSemu )
        self.h_isSSmumu =ROOT.TH1D('isSSmumu', 'isSSmumu', 2,-0.5,1.5); self.addObject(self.h_isSSmumu )
        self.h_isSSee   =ROOT.TH1D('isSSee', 'isSSee', 2,-0.5,1.5); self.addObject(self.h_isSSee )

	self.h_vpt=ROOT.TH1F('vpt',   'vpt',   100, 0, 800);self.addObject(self.h_vpt )
        self.h_vmass=ROOT.TH1F('vmass',   'vmass',   100, 0, 200);self.addObject(self.h_vmass )

        ##Gen-level Objects
        self.h_gen_Mu1pt  = ROOT.TH1F('gen_Mu1pt',   'Gen-level leading pt muon pt',   100, 0, 800);self.addObject(self.h_gen_Mu1pt )
        self.h_gen_Mu1eta = ROOT.TH1F('gen_Mu1eta',   'Gen-level leading pt muon eta',   10, -5.5, 4.5);self.addObject(self.h_gen_Mu1eta )
        self.h_gen_Mu1phi = ROOT.TH1F('gen_Mu1phi',   'Gen-level leading pt muon phi',   10, 0, 4);self.addObject(self.h_gen_Mu1phi )

        self.h_gen_Mu2pt  = ROOT.TH1F('gen_Mu2pt',   'Gen-level subleading pt muon pt',   100, 0, 800);self.addObject(self.h_gen_Mu2pt )
        self.h_gen_Mu2eta = ROOT.TH1F('gen_Mu2eta',   'Gen-level subleading pt muon eta',   10, -5.5, 4.5);self.addObject(self.h_gen_Mu2eta )
        self.h_gen_Mu2phi = ROOT.TH1F('gen_Mu2phi',   'Gen-level subleading pt muon phi',   10, 0, 4);self.addObject(self.h_gen_Mu2phi )

        self.h_gen_Mu3pt  = ROOT.TH1F('gen_Mu3pt',   'Gen-level subsubleading pt muon pt',   100, 0, 800);self.addObject(self.h_gen_Mu3pt )
        self.h_gen_Mu3eta = ROOT.TH1F('gen_Mu3eta',   'Gen-level subsubleading pt muon eta',   10, -5.5, 4.5);self.addObject(self.h_gen_Mu3eta )
        self.h_gen_Mu3phi = ROOT.TH1F('gen_Mu3phi',   'Gen-level subsubleading pt muon phi',   10, 0, 4);self.addObject(self.h_gen_Mu3phi )

        self.h_gen_Elec1pt  = ROOT.TH1F('gen_Elec1pt',   'Gen-level leading pt electron pt',   100, 0, 800);self.addObject(self.h_gen_Elec1pt )
        self.h_gen_Elec1eta = ROOT.TH1F('gen_Elec1eta',   'Gen-level leading pt electron eta',   10, -5.5, 4.5);self.addObject(self.h_gen_Elec1eta )
        self.h_gen_Elec1phi = ROOT.TH1F('gen_Elec1phi',   'Gen-level leading pt electron phi',   10, 0, 4);self.addObject(self.h_gen_Elec1phi )

        self.h_gen_Elec2pt  = ROOT.TH1F('gen_Elec2pt',   'Gen-level subleading pt electron pt',   100, 0, 800);self.addObject(self.h_gen_Elec2pt )
	self.h_gen_Elec2eta = ROOT.TH1F('gen_Elec2eta',   'Gen-level subleading pt electron eta',   10, -5.5, 4.5);self.addObject(self.h_gen_Elec2eta )
        self.h_gen_Elec2phi = ROOT.TH1F('gen_Elec2phi',   'Gen-level subleading pt electron phi',   10, 0, 4);self.addObject(self.h_gen_Elec2phi )

        self.h_gen_Elec3pt  = ROOT.TH1F('gen_Elec3pt',   'Gen-level subsubleading pt electron pt',   100, 0, 800);self.addObject(self.h_gen_Elec3pt )
        self.h_gen_Elec3eta = ROOT.TH1F('gen_Elec3eta',   'Gen-level subsubleading pt electron eta',   10, -5.5, 4.5);self.addObject(self.h_gen_Elec3eta )
        self.h_gen_Elec3phi = ROOT.TH1F('gen_Elec3phi',   'Gen-level subsubleading pt electron phi',   10, 0, 4);self.addObject(self.h_gen_Elec3phi )

        ##Reco-level Objects
        self.h_reco_Mu1pt  = ROOT.TH1F('reco_Mu1pt',   'Reco-level leading pt muon pt',   100, 0, 800);self.addObject(self.h_reco_Mu1pt )
        self.h_reco_Mu1eta = ROOT.TH1F('reco_Mu1eta',   'Reco-level leading pt muon eta',   10, -5.5, 4.5);self.addObject(self.h_reco_Mu1eta )
        self.h_reco_Mu1phi = ROOT.TH1F('reco_Mu1phi',   'Reco-level leading pt muon phi',   10, 0, 4);self.addObject(self.h_reco_Mu1phi )

        self.h_reco_Mu2pt  = ROOT.TH1F('reco_Mu2pt',   'Reco-level subleading pt muon pt',   100, 0, 800);self.addObject(self.h_reco_Mu2pt )
        self.h_reco_Mu2eta = ROOT.TH1F('reco_Mu2eta',   'Reco-level subleading pt muon eta',   10, -5.5, 4.5);self.addObject(self.h_reco_Mu2eta )
        self.h_reco_Mu2phi = ROOT.TH1F('reco_Mu2phi',   'Reco-level subleading pt muon phi',   10, 0, 4);self.addObject(self.h_reco_Mu2phi )

        self.h_reco_Mu3pt  = ROOT.TH1F('reco_Mu3pt',   'Reco-level subsubleading pt muon pt',   100, 0, 800);self.addObject(self.h_reco_Mu3pt )
        self.h_reco_Mu3eta = ROOT.TH1F('reco_Mu3eta',   'Reco-level subsubleading pt muon eta',   10, -5.5, 4.5);self.addObject(self.h_reco_Mu3eta )
        self.h_reco_Mu3phi = ROOT.TH1F('reco_Mu3phi',   'Reco-level subsubleading pt muon phi',   10, 0, 4);self.addObject(self.h_reco_Mu3phi )

        self.h_reco_Elec1pt  = ROOT.TH1F('reco_Elec1pt',   'Reco-level leading pt electron pt',   100, 0, 800);self.addObject(self.h_reco_Elec1pt )
        self.h_reco_Elec1eta = ROOT.TH1F('reco_Elec1eta',   'Reco-level leading pt electron eta',   10, -5.5, 4.5);self.addObject(self.h_reco_Elec1eta )
        self.h_reco_Elec1phi = ROOT.TH1F('reco_Elec1phi',   'Reco-level leading pt electron phi',   10, 0, 4);self.addObject(self.h_reco_Elec1phi )

        self.h_reco_Elec2pt  = ROOT.TH1F('reco_Elec2pt',   'Reco-level subleading pt electron pt',   100, 0, 800);self.addObject(self.h_reco_Elec2pt )
        self.h_reco_Elec2eta = ROOT.TH1F('reco_Elec2eta',   'Reco-level subleading pt electron eta',   10, -5.5, 4.5);self.addObject(self.h_reco_Elec2eta )
        self.h_reco_Elec2phi = ROOT.TH1F('reco_Elec2phi',   'Reco-level subleading pt electron phi',   10, 0, 4);self.addObject(self.h_reco_Elec2phi )

        self.h_reco_Elec3pt  = ROOT.TH1F('reco_Elec3pt',   'Reco-level subsubleading pt electron pt',   100, 0, 800);self.addObject(self.h_reco_Elec3pt )
        self.h_reco_Elec3eta = ROOT.TH1F('reco_Elec3eta',   'Reco-level subsubleading pt electron eta',   10, -5.5, 4.5);self.addObject(self.h_reco_Elec3eta )
        self.h_reco_Elec3phi = ROOT.TH1F('reco_Elec3phi',   'Reco-level subsubleading pt electron phi',   10, 0, 4);self.addObject(self.h_reco_Elec3phi )

        ## GEN signal
        #self.h_w1 =ROOT.TH1D('isOSmumu', 'isOSmumu', 2,-0.5,1.5); self.addObject(self.h_w1 )
        '''
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
            #theGenZ = FindGenParticle(GenLists, [23,-23])
            #theGenW = FindGenParticle(GenLists, [24,-24])
            #theGenTop = FindGenParticle(GenLists, [6])
            #theGenAntiTop = FindGenParticle(GenLists, [-6])
        counter=0
        eventDecayChain={}
        for genOBJ in GenLists:
            decayChain=[]
            if genOBJ.status==1:
                counter+=1
                moId=genOBJ.genPartIdxMother
                decayChain.append([genOBJ.pdgId,genOBJ.status,bitwiseDecoder(genOBJ.statusFlags)])
                while moId!=-1:
                    decayChain.append([GenLists[moId].pdgId,GenLists[moId].status,bitwiseDecoder(GenLists[moId].statusFlags)])
                    moId=GenLists[moId].genPartIdxMother
                eventDecayChain["%s"%counter]=decayChain
        
        print "===Begins Event==="
        print "counter = ", counter
        for key, value in eventDecayChain.iteritems():
            print " "
            print "--> Stable particle ", key," has a decay chain of :"
            print value
            print " "
        print "===End Event==="
                
        '''
            theWDecays1 = FindGenParticlebyStatus(GenLists, [11,-11,13,-13], 1, 62)
            theWDecays2 = FindGenParticlebyStatus(GenLists, [11,-11,13,-13], 1, 22)

            #mat = genRecoFinder(ElecList+MuonList,theWDecays1+theWDecays2)
            #print "mat = ", mat

            #if len(theWDecays1)==1 and len(theWDecays2)==2:
                #Reco matching with electron
            RecoMatchList = genRecoFinder(ElecList+MuonList,theWDecays1+theWDecays2)
                #print "RecoMatchList = ", RecoMatchList
            RecoMatchList.sort(key=getPt, reverse=True)
                #print "RecoMatchList = ", RecoMatchList
            elef=0
            muonf=0
            for num,match in enumerate(RecoMatchList):
                if abs(match[0].pdgId)==11:
                    elef+=1
                    if elef==1:
                        #RECO
                        self.h_reco_Elec1pt.Fill(match[0].pt)
                        self.h_reco_Elec1eta.Fill(match[0].eta)
                        self.h_reco_Elec1phi.Fill(match[0].phi)
                        #GEN
                        self.h_gen_Elec1pt.Fill(match[1].pt)
                        self.h_gen_Elec1eta.Fill(match[1].eta)
                        self.h_gen_Elec1phi.Fill(match[1].phi)
                            
                    elif elef==2:
                        #RECO
                        self.h_reco_Elec2pt.Fill(match[0].pt)
                        self.h_reco_Elec2eta.Fill(match[0].eta)
                        self.h_reco_Elec2phi.Fill(match[0].phi)
                        #GEN
                        self.h_gen_Elec2pt.Fill(match[1].pt)
                        self.h_gen_Elec2eta.Fill(match[1].eta)
                        self.h_gen_Elec2phi.Fill(match[1].phi)
                            
                    elif elef==3:
                        #RECO
                        self.h_reco_Elec3pt.Fill(match[0].pt)
                        self.h_reco_Elec3eta.Fill(match[0].eta)
                        self.h_reco_Elec3phi.Fill(match[0].phi)
                        #GEN
                        self.h_gen_Elec3pt.Fill(match[1].pt)
                        self.h_gen_Elec3eta.Fill(match[1].eta)
                        self.h_gen_Elec3phi.Fill(match[1].phi)
                        
                elif abs(match[0].pdgId)==13:
                    muonf+=1
                    if muonf==1:
                        #RECO
                        self.h_reco_Mu1pt.Fill(match[0].pt)
                        self.h_reco_Mu1eta.Fill(match[0].eta)
                        self.h_reco_Mu1phi.Fill(match[0].phi)
                        #GEN
                        self.h_gen_Mu1pt.Fill(match[1].pt)
                        self.h_gen_Mu1eta.Fill(match[1].eta)
                        self.h_gen_Mu1phi.Fill(match[1].phi)
                            
                    elif muonf==2:
                        #RECO
                        self.h_reco_Mu2pt.Fill(match[0].pt)
                        self.h_reco_Mu2eta.Fill(match[0].eta)
                        self.h_reco_Mu2phi.Fill(match[0].phi)
                        #GEN
                        self.h_gen_Mu2pt.Fill(match[1].pt)
                        self.h_gen_Mu2eta.Fill(match[1].eta)
                        self.h_gen_Mu2phi.Fill(match[1].phi)

                    elif muonf==3:
                        #RECO
                        self.h_reco_Mu3pt.Fill(match[0].pt)
                        self.h_reco_Mu3eta.Fill(match[0].eta)
                        self.h_reco_Mu3phi.Fill(match[0].phi)
                        #GEN
                        self.h_gen_Mu3pt.Fill(match[1].pt)
                        self.h_gen_Mu3eta.Fill(match[1].eta)
                        self.h_gen_Mu3phi.Fill(match[1].phi)

              
            # W Boson
            #byID
            # w -> lv (44,62)
            # h -> w -> ll (22,62)
            theGenW1 = FindGenParticlebyStatus(GenLists, [24,-24], 62, 44)
            theGenW2 = FindGenParticlebyStatus(GenLists, [24,-24], 22, 62)

            # lepton


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
                    elif MuonList[0].charge + MuonList[1].charge==0:
                        isOSmumu=1
                else:
                    # same sign electron
                    if abs(ElecList[0].charge+ElecList[1].charge)==2:
                        isSSee=1
                    # opposite sign electron
                    elif ElecList[0].charge + ElecList[1].charge==0:
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
        '''
        return True

DIR="/Users/shoh/Projects/CMS/PhD/Analysis/SSL/NANOAOD/"

preselection=""

files=[
    #DIR+"HWminusJ_HToWWTo2L2Nu_WToLNu_M125_13TeV_powheg_pythia8-v1.root",
    #DIR+"HWplusJ_HToWWTo2L2Nu_WToLNu_M125_13TeV_powheg_pythia8-v1.root",
    #DIR+"HWminusJ_HToWW_M125_13TeV_powheg_pythia8-v1.root",
    #DIR+"HWplusJ_HToWW_M125_13TeV_powheg_pythia8-v1.root",
    DIR+"VHToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8.root",
]
p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[DecayChain()],noOut=True,histFileName="vh.root",histDirName="plots")
p.run()
