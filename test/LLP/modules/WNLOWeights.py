import os
import sys
import math
import json
import ROOT
import random

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


class WNLOWeights(Module):
    def __init__(self):
        self.weightFile = os.path.expandvars("$CMSSW_BASE/src/PhysicsTools/NanoAODTools/data/nlo/enj.dat")
        self.histograms = {}
        
        f = open(self.weightFile)
        parseHist = False
        parseHeader = False
        
        histData = []
        histName = None
        for l in f:
            if parseHeader:
                parseHeader = False
                parseHist = True
                continue
                
            if l.startswith("# END HISTO1D"):
                if not parseHist or parseHeader:
                    print "Error while parsing hist file"
                    sys.ext(1)
                if histName==None:
                    print "Error while parsing hist file"
                    sys.ext(1)
                self.histograms[histName] = histData
                histData = []
                histName = None
                parseHist = False
                
            if parseHist:
                parts = l.split(" ")
                histData.append([
                    float(parts[0]),
                    float(parts[1]),
                    float(parts[2])
                ])
                
            if l.startswith("# BEGIN HISTO1D"):
                if parseHeader or parseHist:
                    print "Error while parsing hist file"
                    sys.ext(1)
                parseHeader = True
                histName = l.rsplit(" ",1)[1].replace("\r","").replace("\n","")
                continue
        f.close()
       
        
    def beginJob(self):
        pass
 
    def endJob(self):
        pass
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("wnloweight_nominal","F")
        self.out.branch("wnloweight_err1","F")
        self.out.branch("wnloweight_err2","F")
        self.out.branch("wnloweight_err3","F")
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def inDecay(self,particle,testFct,genParticles):
        motherIndex = particle.genPartIdxMother
        if motherIndex<0 or motherIndex>len(genParticles):
            return False
        if testFct(genParticles[motherIndex]):
            return True
        return self.inDecay(genParticles[motherIndex],testFct,genParticles) 
        
    def analyze(self, event):
        genParticles = Collection(event,'GenPart')
        
        neutrino = None
        lepton = None
        tauCandidate = None
        for genParticle in genParticles:
            if abs(genParticle.pdgId) in [12,14,16]:
                motherIndex = genParticle.genPartIdxMother
                if motherIndex>=0 and motherIndex<len(genParticles) and abs(genParticles[motherIndex].pdgId)==24:
                    if neutrino!=None:
                        return False
                    neutrino = genParticle.p4()
            if genParticle.status==1 and abs(genParticle.pdgId) in [11,13]:
                motherIndex = genParticle.genPartIdxMother
                if self.inDecay(genParticle, lambda p: abs(p.pdgId)==24, genParticles):
                    if lepton!=None:
                        return False
                    lepton = genParticle.p4()
            if abs(genParticle.pdgId)==15:
                motherIndex = genParticle.genPartIdxMother
                if motherIndex>=0 and motherIndex<len(genParticles) and abs(genParticles[motherIndex].pdgId)==24:
                    if tauCandidate!=None:
                        return False
                    tauCandidate = genParticle.p4()
                
        if lepton!=None:
            dressedP4 = ROOT.TLorentzVector(0,0,0,0)
            for genParticle in genParticles:
                if genParticle.status==1 and genParticle.pdgId==22:
                    if genParticle.p4().DeltaR(lepton):
                        dressedP4+=genParticle.p4()
            lepton += dressedP4
                        
                        
        if neutrino==None:
            return False
            
        if lepton==None and tauCandidate==None:
            return False
            
        if lepton==None:
            lepton = tauCandidate
            
        wboson = ROOT.TLorentzVector(0,0,0,0)
        wboson += lepton
        wboson += neutrino
        
        wpt = wboson.Pt()
        
        w = 1.
        err1 = 1.
        err2 = 1.
        err3 = 1.
        
        if wpt>30:
            for ibin in range(len(self.histograms['enj_pTV_K_NLO'])):
                if self.histograms['enj_pTV_K_NLO'][ibin][0]<=wpt and self.histograms['enj_pTV_K_NLO'][ibin][1]>wpt:
                    w = self.histograms['enj_pTV_K_NLO'][ibin][2]
                    err1 = self.histograms['enj_pTV_d1K_NLO'][ibin][2]
                    err2 = self.histograms['enj_pTV_d2K_NLO'][ibin][2]
                    err3 = self.histograms['enj_pTV_d3K_NLO'][ibin][2]
                    break

        self.out.fillBranch("wnloweight_nominal",w)
        self.out.fillBranch("wnloweight_err1",err1)
        self.out.fillBranch("wnloweight_err2",err2)
        self.out.fillBranch("wnloweight_err3",err3)
        return True
