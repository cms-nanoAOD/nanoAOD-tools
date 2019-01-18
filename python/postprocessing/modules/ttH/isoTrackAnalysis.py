import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


class IsoTrackAnalysis(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.wrappedOutputTree = wrappedOutputTree
        self.wrappedOutputTree.branch('nPFHad10','I')
        self.wrappedOutputTree.branch('nPFLep5','I')

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        tracks = [ o for o in Collection(event, 'IsoTrack') ]
        muon   = [ o for o in Collection(event, 'Muon')     ]
        elec   = [ o for o in Collection(event, 'Electron') ]

        nPFHad10 = 0; nPFLep5 = 0

        for cand in tracks+muon+elec: 
            if not cand.isPFcand: continue 
            if hasattr(cand,'fromPV') and not getattr(cand,'fromPV'): continue # check only for IsoTracks, for Leptons should be true
            if abs(cand.pdgId) == 11 or abs(cand.pdgId) == 13:
                if abs(cand.pdgId) == 11: pt = cand.pt * cand.eCorr
                else: pt = cand.pt
                if pt < 5 or abs(cand.eta) > 2.4: continue
                if abs(cand.dz)  > 0.1: continue
                if abs(cand.dxy) > 0.2: continue
                if cand.pfRelIso03_chg*pt > 5: continue
                if cand.pfRelIso03_chg > 0.2: continue
                nPFLep5 = nPFLep5 + 1 
            else: 
                if cand.pt < 10 or abs(cand.eta) > 2.4: continue
                if abs(cand.dz)  > 0.1: continue
                if abs(cand.dxy) > 0.2: continue
                if cand.pfRelIso03_chg*cand.pt > 5: continue
                if cand.pfRelIso03_chg > 0.2: continue
                nPFHad10 = nPFHad10 + 1 

        self.wrappedOutputTree.fillBranch("nPFHad10",nPFHad10)
        self.wrappedOutputTree.fillBranch("nPFLep5", nPFLep5)
        
        return True
        

isoTrackAnalysis = lambda : IsoTrackAnalysis()

