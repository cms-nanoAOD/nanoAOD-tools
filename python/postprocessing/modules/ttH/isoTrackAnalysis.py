import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


class IsoTrackAnalysis(Module):
    def __init__(self, storeCollection=False):
        self.storeCollection = storeCollection
        self.brList = [('pdgId','I'), ('pt','F'), ('eta','F'), ('phi','F'), ('dz','F'), ('dxy','F'), ('pfRelIso03_chg','F')]

    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch('nPFHad10','I')
        self.out.branch('nPFLep5','I')
        if self.storeCollection:
            self.out.branch('nEdgeIsoTracks','I')
            for br,ty in self.brList: 
                self.out.branch('EdgeIsoTracks_%s'%br,ty, lenVar='nEdgeIsoTracks')

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        tracks = [ o for o in Collection(event, 'IsoTrack') ]
        muon   = [ o for o in Collection(event, 'Muon')     ]
        elec   = [ o for o in Collection(event, 'Electron') ]

        nPFHad10 = 0; nPFLep5 = 0

        ret = {}
        for br,ty in self.brList: ret[br] = [] 

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
                pt = cand.pt 
                if pt < 10 or abs(cand.eta) > 2.4: continue
                if abs(cand.dz)  > 0.1: continue
                if abs(cand.dxy) > 0.2: continue
                if cand.pfRelIso03_chg*cand.pt > 5: continue
                if cand.pfRelIso03_chg > 0.2: continue
                nPFHad10 = nPFHad10 + 1 

            # if it goes all the way here it means it has passed one way of another
            if self.storeCollection:
                for br,ty in self.brList:
                    ret[br].append( getattr(cand, br) if br != 'pt' else pt)


        self.out.fillBranch("nPFHad10",nPFHad10)
        self.out.fillBranch("nPFLep5", nPFLep5)
        if self.storeCollection:
            self.out.fillBranch('nEdgeIsoTracks', nPFHad10+nPFLep5)
            for br, ty in self.brList:
                self.out.fillBranch('EdgeIsoTracks_%s'%br, ret[br])
        
        return True
        



