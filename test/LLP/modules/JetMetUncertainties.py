import os
import sys
import math
import json
import ROOT
import random

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import matchObjectCollection, matchObjectCollectionMultiple
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import jetmetUncertaintiesProducer

from utils import PhysicsObject

class JetMetUncertainties(jetmetUncertaintiesProducer):
    def __init__(
        self, era, globalTag, jesUncertainties = [ "Total" ], jetType = "AK4PFchs", redoJEC=False, noGroom=False,
        globalOptions={"isData":False}
    ):
        jetmetUncertaintiesProducer.__init__(self, era, globalTag, jesUncertainties = [ "Total" ], jetType = "AK4PFchs", redoJEC=False, noGroom=False)
        self.globalOptions = globalOptions
        
    def beginJob(self):
        jetmetUncertaintiesProducer.beginJob(self)
        
    def endJob(self):
        jetmetUncertaintiesProducer.endJob(self)
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        #jetmetUncertaintiesProducer.beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree)
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        jetmetUncertaintiesProducer.endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree)
        
    def analyze(self, event):
        jets = Collection(event, self.jetBranchName )
        genJets = Collection(event, self.genJetBranchName )


        jets_pt_nom = []
        jets_pt_jerUp   = []
        jets_pt_jerDown = []
        jets_pt_jesUp   = {}
        jets_pt_jesDown = {}

        for jesUncertainty in self.jesUncertainties:
            jets_pt_jesUp[jesUncertainty]   = []
            jets_pt_jesDown[jesUncertainty] = []

        if self.corrMET :
            met = Object(event, self.metBranchName)
            met.px = met.pt*math.cos(met.phi)
            met.py = met.pt*math.sin(met.phi)
            
            met.px_jerNominal,met.py_jerNominal = met.px,met.py
            met.px_jerUp,met.py_jerUp = met.px,met.py
            met.px_jerDown,met.py_jerDown = met.px,met.py
            
            met.px_jesUp,met.py_jesUp = {},{}
            met.px_jesDown,met.py_jesDown = {},{}
            for jesUncertainty in self.jesUncertainties:
                met.px_jesUp[jesUncertainty],met.py_jesUp[jesUncertainty] = met.px,met.py
                met.px_jesDown[jesUncertainty],met.py_jesDown[jesUncertainty] = met.px,met.py

        
                
        rho = getattr(event, self.rhoBranchName)

        # match reconstructed jets to generator level ones
        # (needed to evaluate JER scale factors and uncertainties)
        pairs = matchObjectCollection(jets, genJets)
        
        for jet in jets:
            #jet_jes = PhysicsObject(jet)
            #print jet_jes.p4().Pt()
            genJet = pairs[jet]
                
                
            # evaluate JER scale factors and uncertainties
            # (cf. https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution and https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyResolution )
            #these are the smear factors => use for energy instead of pT!!!
            ( jet_pt_jerNomVal, jet_pt_jerUpVal, jet_pt_jerDownVal ) = self.jetSmearer.getSmearValsPt(jet, genJet, rho)
	    
            if self.redoJEC:
                jet.pt = self.jetReCalibrator.correct(jet,rho)
                
            jet.pt_jerNominal = jet_pt_jerNomVal *jet.pt
            if jet.pt_jerNominal < 0.0:
                jet.pt_jerNominal *= -1.0

            jet.pt_jerUp = jet_pt_jerUpVal  *jet.pt
            jet.pt_jerDown = jet_pt_jerDownVal*jet.pt
            
            jet.pt_jesUp   = {}
            jet.pt_jesDown = {}
        
            for jesUncertainty in self.jesUncertainties:
                # (cf. https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyCorrections#JetCorUncertainties )
                self.jesUncertainty[jesUncertainty].setJetPt(jet.pt_jerNominal)
                self.jesUncertainty[jesUncertainty].setJetEta(jet.eta)
                delta = self.jesUncertainty[jesUncertainty].getUncertainty(True)
                jet.pt_jesUp[jesUncertainty]   = jet.pt_jerNominal*(1. + delta)
                jet.pt_jesDown[jesUncertainty] = jet.pt_jerNominal*(1. - delta)
                
            
            # progate JER and JES corrections and uncertainties to MET
            if self.corrMET and jet.pt_jerNominal > self.unclEnThreshold:
                jet_cosPhi = math.cos(jet.phi)
                jet_sinPhi = math.sin(jet.phi)
                
                #propagate nominal jet energy smearing 
                met.px_jerNominal = met.px - (jet.pt_jerNominal - jet.pt)*jet_cosPhi
                met.py_jerNominal = met.py - (jet.pt_jerNominal - jet.pt)*jet_sinPhi
               
                met.px_jerUp   = met.px_jerUp   - (jet.pt_jerUp   - jet.pt_jerNominal)*jet_cosPhi
                met.py_jerUp   = met.py_jerUp   - (jet.pt_jerUp   - jet.pt_jerNominal)*jet_sinPhi
                met.px_jerDown = met.px_jerDown - (jet.pt_jerDown - jet.pt_jerNominal)*jet_cosPhi
                met.py_jerDown = met.py_jerDown - (jet.pt_jerDown - jet.pt_jerNominal)*jet_sinPhi
                for jesUncertainty in self.jesUncertainties:
                    met.px_jesUp[jesUncertainty]   = met.px_jesUp[jesUncertainty]   - (jet.pt_jesUp[jesUncertainty]   - jet.pt_jerNominal)*jet_cosPhi
                    met.py_jesUp[jesUncertainty]   = met.py_jesUp[jesUncertainty]   - (jet.pt_jesUp[jesUncertainty]   - jet.pt_jerNominal)*jet_sinPhi
                    met.px_jesDown[jesUncertainty] = met.px_jesDown[jesUncertainty] - (jet.pt_jesDown[jesUncertainty] - jet.pt_jerNominal)*jet_cosPhi
                    met.py_jesDown[jesUncertainty] = met.py_jesDown[jesUncertainty] - (jet.pt_jesDown[jesUncertainty] - jet.pt_jerNominal)*jet_sinPhi
        
        # propagate "unclustered energy" uncertainty to MET
        if self.corrMET:
            met.px_unclEnUp,   met.py_unclEnUp = met.px, met.py
            met.px_unclEnDown, met.py_unclEnDown = met.px, met.py
            met_deltaPx_unclEn = getattr(event, self.metBranchName + "_MetUnclustEnUpDeltaX")
            met_deltaPy_unclEn = getattr(event, self.metBranchName + "_MetUnclustEnUpDeltaY")
            met.px_unclEnUp    = met.px_unclEnUp   + met_deltaPx_unclEn
            met.py_unclEnUp    = met.py_unclEnUp   + met_deltaPy_unclEn
            met.px_unclEnDown  = met.px_unclEnDown - met_deltaPx_unclEn
            met.py_unclEnDown  = met.py_unclEnDown - met_deltaPy_unclEn

            # propagate effect of jet energy smearing to MET            
            met.px_jerUp   = met.px_jerUp   + (met.px_jerNominal - met.px)
            met.py_jerUp   = met.py_jerUp   + (met.py_jerNominal - met.py)
            met.px_jerDown = met.px_jerDown + (met.px_jerNominal - met.px)
            met.py_jerDown = met.py_jerDown + (met.py_jerNominal - met.py)
            for jesUncertainty in self.jesUncertainties:
                met.px_jesUp[jesUncertainty]   = met.px_jesUp[jesUncertainty]   + (met.px_jerNominal - met.px)
                met.py_jesUp[jesUncertainty]   = met.py_jesUp[jesUncertainty]   + (met.py_jerNominal - met.py)
                met.px_jesDown[jesUncertainty] = met.px_jesDown[jesUncertainty] + (met.px_jerNominal - met.px)
                met.py_jesDown[jesUncertainty] = met.py_jesDown[jesUncertainty] + (met.py_jerNominal - met.py)
            met.px_unclEnUp    = met.px_unclEnUp   + (met.px_jerNominal - met.px)
            met.py_unclEnUp    = met.py_unclEnUp   + (met.py_jerNominal - met.py)
            met.px_unclEnDown  = met.px_unclEnDown + (met.px_jerNominal - met.px)
            met.py_unclEnDown  = met.py_unclEnDown + (met.py_jerNominal - met.py)
            
            
        

        def getJetsSyst(systName="nominal",variation=0):
            if variation not in [0,-1,1]:
                print "Error - variation needs to be either [0,-1,1]!"
                sys.exit(1)
            systJets = []
            for jet in jets:
                systJet = PhysicsObject(jet,
                    pt=jet.pt,eta=jet.eta,phi=jet.phi,mass=jet.mass,
                    keys=[
                        "jetId",
                        "hadronFlavour",
                        "partonFlavour",
                        "genJetIdx",
                        "puId"
                    ]
                )
                if systName=="nominal": 
                    systJet.pt = jet.pt_jerNominal
                elif systName=="jer":
                    if variation==1:
                        systJet.pt = jet.pt_jerUp
                    elif variation==-1:
                        systJet.pt = jet.pt_jerDown
                    else:
                        print "Error - 'jer' variation needs to be either [-1,1]!"
                        sys.exit(1)
                elif systName.startswith("jes"):
                    subvariation = "Total"
                    if systName.find(':')>0:
                        subvariation = systName.split(':',1)[1]
                    if subvariation not in self.jesUncertainties:
                        print "Error - 'jes' subvariation with name '"+subvariation+"' has not been calculated"
                        sys.exit(1)
                    if variation==1:
                        systJet.pt = jet.pt_jesUp[subvariation]
                    elif variation==-1:
                        systJet.pt = jet.pt_jesDown[subvariation]
                    else:
                        print "Error - 'jer' variation needs to be either [-1,1]!"
                        sys.exit(1)
                else:
                    print "Error - unknown systematic '"+str(systName)+"'"
                    sys.exit(1)
                    
                systJets.append(systJet)
                
            #sort decreasing in pt
            systJets = sorted(systJets,key=lambda jet: -jet.pt)
                
            return systJets
            
            
            
        def getMetSyst(systName="nominal",variation=0):
            if variation not in [0,-1,1]:
                print "Error - variation needs to be either [0,-1,1]!"
                sys.exit(1)
            systMet = PhysicsObject(met,pt=met.pt,phi=met.phi)
            if systName=="nominal": 
                systMet.px = met.px_jerNominal
                systMet.py = met.py_jerNominal
            elif systName=="jer":
                if variation==1:
                    systMet.px = met.px_jerUp
                    systMet.py = met.py_jerUp
                elif variation==-1:
                    systMet.px = met.px_jerDown
                    systMet.py = met.py_jerDown
                else:
                    print "Error - 'jer' variation needs to be either [-1,1]!"
                    sys.exit(1)
            elif systName.startswith("jes"):
                subvariation = "Total"
                if systName.find(':')>0:
                    subvariation = systName.split(':',1)[1]
                if variation==1:
                    systMet.px = met.px_jesUp[subvariation]
                    systMet.py = met.py_jesUp[subvariation]
                elif variation==-1:
                    systMet.px = met.px_jesDown[subvariation]
                    systMet.py = met.py_jesDown[subvariation]
                else:
                    print "Error - 'jer' variation needs to be either [-1,1]!"
                    sys.exit(1)
            elif systName=="unclEn":
                if variation==1:
                    systMet.px = met.px_unclEnUp
                    systMet.py = met.py_unclEnUp
                elif variation==-1:
                    systMet.px = met.px_unclEnDown
                    systMet.py = met.py_unclEnDown
                else:
                    print "Error - 'jer' variation needs to be either [-1,1]!"
                    sys.exit(1)
            else:
                print "Error - unknown systematic '"+str(systName)+"'"
                sys.exit(1)

            systMet.phi = math.atan2(systMet.py,systMet.px)
            systMet.pt = math.sqrt(systMet.px**2+systMet.py**2)
                
            return systMet

        
        event.jets_nominal = getJetsSyst("nominal",0)
        
        
        event.met_nominal = getMetSyst("nominal",0)
        
        #print map(lambda j: j.pt, jets),met.pt
        #print map(lambda j: j.pt, event.jets_nominal),event.met_nominal.pt
        #print
        event.jets_jerUp = getJetsSyst("jer",1)
        event.met_jerUp = getMetSyst("jer",1)
        event.jets_jerDown = getJetsSyst("jer",-1)
        event.met_jerDown = getMetSyst("jer",-1)
        
        event.jets_jesUp = {}
        event.met_jesUp = {}
        event.jets_jesDown = {}
        event.met_jesDown = {}
        for jesUncertainty in self.jesUncertainties:
            event.jets_jesUp[jesUncertainty] = getJetsSyst("jes:"+jesUncertainty,1)
            event.met_jesUp[jesUncertainty] = getMetSyst("jes:"+jesUncertainty,1)
            event.jets_jesDown[jesUncertainty] = getJetsSyst("jes:"+jesUncertainty,-1)
            event.met_jesDown[jesUncertainty] = getMetSyst("jes:"+jesUncertainty,-1)
            
        event.met_unclEnUp = getMetSyst("unclEn",1)
        event.met_unclEnDown = getMetSyst("unclEn",-1)
        
        return True
        
