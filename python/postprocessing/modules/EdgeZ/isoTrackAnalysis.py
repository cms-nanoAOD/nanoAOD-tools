import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

def IPnISOcuts(cand):
    if abs(cand.dz)  > 0.1: return False
    if abs(cand.dxy) > 0.2: return False
    if cand.pfRelIso03_chg*cand.pt > 5: return False
    if cand.pfRelIso03_chg > 0.2: return False
    return True

def isClean(cand, coll):
    for l in coll: 
        if deltaR(cand,l) < 0.2: return False
    return True

class IsoTrackAnalysis(Module):
    def __init__(self):
        self.brList = [('pdgId','I'), ('pt','F'), ('eta','F'), ('phi','F'), ('dz','F'), ('dxy','F'), ('pfRelIso03_chg','F')]

    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch('nPFHad10','I')
        self.out.branch('nPFLep5','I')

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        tracks = [ o for o in Collection(event, 'IsoTrack') ]
        muon   = [ o for o in Collection(event, 'Muon')     ]
        elec   = [ o for o in Collection(event, 'Electron') ]

        nPFHad10 = 0; nPFLep5 = 0

        ret = {}
        for br,ty in self.brList: ret[br] = [] 

        ## Leptons
        for cand in muon+elec: 
            if not cand.isPFcand: continue
            if abs(cand.pdgId) == 11: pt = cand.pt / cand.eCorr
            else: pt = cand.pt
            if pt < 5 or abs(cand.eta) > 2.4: continue
            if abs(cand.dz)  > 0.1: continue
            if abs(cand.dxy) > 0.2: continue
            if cand.pfRelIso03_chg*pt > 5: continue
            if cand.pfRelIso03_chg > 0.2: continue
            nPFLep5 = nPFLep5 + 1 

        for cand in tracks:
            if not cand.isPFcand   : continue 
            if not cand.fromPV     : continue
            if cand.isFromLostTrack: continue
            if abs(cand.pdgId) == 11 or abs(cand.pdgId) == 13:
                if cand.pt < 5 or abs(cand.eta) > 2.4: continue
                if not IPnISOcuts(cand): continue
                # cleaning at the end so its faster
                if not isClean(cand, muon+elec): continue
                nPFLep5 = nPFLep5 + 1 
                    
            else: 
                pt = cand.pt 
                if pt < 10 or abs(cand.eta) > 2.4: continue
                if not IPnISOcuts(cand): continue
                if not isClean(cand, muon+elec): continue
                nPFHad10 = nPFHad10 + 1 

            

        self.out.fillBranch("nPFHad10",nPFHad10)
        self.out.fillBranch("nPFLep5", nPFLep5)
        
        return True
        



