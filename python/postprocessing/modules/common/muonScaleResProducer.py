import ROOT
import os
import random
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


def mk_safe(fct, *args):
    try:
        return fct(*args)
    except Exception as e:
        if any('Error in function boost::math::erf_inv' in arg for arg in e.args):
            print 'WARNING: catching exception and returning -1. Exception arguments: %s' % e.args
            return -1.
        else:
            raise e


class muonScaleResProducer(Module):
    def __init__(self, rc_dir, rc_corrections):
        self.is_2017 = '2017' in rc_dir
        p_postproc = '%s/src/PhysicsTools/NanoAODTools/python/postprocessing' % os.environ['CMSSW_BASE']
        p_roccor = p_postproc + '/data/' + rc_dir
        if "/RoccoR_cc.so" not in ROOT.gSystem.GetLibraries():
            p_helper = '%s/RoccoR.cc' % p_roccor
            print 'Loading C++ helper from ' + p_helper
            ROOT.gROOT.ProcessLine('.L ' + p_helper)
        self._roccor = ROOT.RoccoR(p_roccor + '/' + rc_corrections)

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("Muon_pt_corrected", "F", lenVar="nMuon")
        if self.is_2017:
            self.out.branch("Muon_pt_sys_uncert", "F", lenVar="nMuon")
        self.is_mc = bool(inputTree.GetBranch("GenJet_pt"))

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        muons = Collection(event, "Muon")
        roccor = self._roccor

        if self.is_mc:
            u1 = random.uniform(0.0, 1.0)
            u2 = random.uniform(0.0, 1.0)
            pt_corr = list(
                mu.pt * mk_safe(
                    roccor.kScaleAndSmearMC,
                    mu.charge, mu.pt, mu.eta, mu.phi, mu.nTrackerLayers, u1, u2
                ) for mu in muons)
            if self.is_2017:
                pt_err = list(
                    mu.pt * mk_safe(
                        roccor.kScaleAndSmearMCerror,
                        mu.charge, mu.pt, mu.eta, mu.phi, mu.nTrackerLayers, u1, u2
                    ) for mu in muons)
        else:
            pt_corr = list(
                mu.pt * mk_safe(
                    roccor.kScaleDT,
                    mu.charge, mu.pt, mu.eta, mu.phi
                ) for mu in muons)
            if self.is_2017:
                pt_err = list(
                    mu.pt * mk_safe(
                        roccor.kScaleDTerror,
                        mu.charge, mu.pt, mu.eta, mu.phi
                    ) for mu in muons)

        self.out.fillBranch("Muon_pt_corrected", pt_corr)
        if self.is_2017:
            self.out.fillBranch("Muon_pt_sys_uncert",  pt_err)

        return True


# the Rochester guys don't supply a unified interface. The 2016 corrections come as many files in a
# directory and the 2017 correction are in a single file.

muonScaleRes2017 = lambda : muonScaleResProducer('roccor.2017.v0', 'RoccoR2017v0.txt')
muonScaleRes2016 = lambda : muonScaleResProducer('roccor.2016.v3', 'rcdata.2016.v3')
