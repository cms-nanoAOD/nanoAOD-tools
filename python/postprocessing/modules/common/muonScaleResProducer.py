import ROOT
import os
import random
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class muonScaleResProducer(Module):
    def __init__(self, rc_file):
        p_postproc = '%s/src/PhysicsTools/NanoAODTools/python/postprocessing' % os.environ['CMSSW_BASE']
        self.file_path = p_postproc + '/data/muonScaleRes/' + rc_file
        if "/RoccoR_cc.so" not in ROOT.gSystem.GetLibraries():
            print "Loading C++ Helper: RoccoR.cc"
            ROOT.gROOT.ProcessLine(".L %s/helpers/RoccoR.cc+" % p_postproc)

    def beginJob(self):
        self._roccor = ROOT.RoccoR(self.file_path)

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("Muon_pt_corrected", "F", lenVar="nMuon")
        self.out.branch("Muon_ptErr", "F", lenVar="nMuon")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        muons = Collection(event, "Muon")
        roccor = self._roccor
        is_mc = getattr(event, 'GenJet_pt', False) and True

        if is_mc:
            u1 = random.uniform(0.0, 1.0)
            u2 = random.uniform(0.0, 1.0)
            ptCorr = list(mu.pt * roccor.kScaleAndSmearMC(mu.charge, mu.pt, mu.eta, mu.phi, mu.nTrackerLayers, u1, u2) for mu in muons)
            ptErr  = list(mu.pt * roccor.kScaleAndSmearMCerror(mu.charge, mu.pt, mu.eta, mu.phi, mu.nTrackerLayers, u1, u2) for mu in muons)
        else:
            ptCorr = list(mu.pt * roccor.kScaleDT(mu.charge, mu.pt, mu.eta, mu.phi) for mu in muons)
            ptErr  = list(mu.pt * roccor.kScaleDTerror(mu.charge, mu.pt, mu.eta, mu.phi) for mu in muons)

        self.out.fillBranch("Muon_pt_corrected", ptCorr)
        self.out.fillBranch("Muon_ptErr",  ptCorr)

        return True


muonScaleRes2017 = lambda : muonScaleResProducer('RoccoR2017v0.txt')
