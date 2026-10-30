#!/usr/bin/env python
"""
Run 2 UL jet veto maps (JERC recommendation, "Jet Veto Maps" -> Run 2).

  * Run 2: veto JETS whose axes lie in vetoed regions (do NOT reject the whole event).
  * A jet is subject to the veto only if it passes the nominal "loose selection":
        pT > 15 GeV, tight jet ID, PU jet ID for CHS jets with pT < 50 GeV,
        (chEmEF + neEmEF) < 0.9, no PF muon within dR < 0.2
  * Recommended maps (ROOT histogram names from the JERC page):
        2018 : h2hot_ul18_plus_hem1516_plus_hbp2m1            (tag Summer19UL18_V1)
        2017 : h2hot_ul17_plus_hep17_plus_hbpw89              (tag Summer19UL17_V2)
        2016 : h2hot_ul16_plus_hbm2_hbp12_qie11  AND  h2hot_mc (tag Summer19UL16_V0, same for APV and non-APV)

This module adds one branch per jet:  Jet_jetVetoed  (1 = jet must be removed, 0 = keep)
so that cut strings can use  "Jet_jetVetoed==0"  and python modules  "jet.jetVetoed==0".
"""
import os
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

JVM_DIR = os.environ['CMSSW_BASE'] + "/src/PhysicsTools/NanoAODTools/python/postprocessing/data/jetvetomaps/"

# file name (as you saved it in JVM_DIR) and the histogram(s) to apply; a jet is vetoed if ANY listed map flags it
JVM_CONFIG = {
    'UL2016preVFP' : ("JetVetoMap_UL16.root", ["h2hot_ul16_plus_hbm2_hbp12_qie11", "h2hot_mc"]),
    'UL2016postVFP': ("JetVetoMap_UL16.root", ["h2hot_ul16_plus_hbm2_hbp12_qie11", "h2hot_mc"]),
    'UL2017'       : ("JetVetoMap_UL17.root", ["h2hot_ul17_plus_hep17_plus_hbpw89"]),
    'UL2018'       : ("JetVetoMap_UL18.root", ["h2hot_ul18_plus_hem1516_and_hbp2m1"]),
}


class jetVetoMapProducer(Module):
    def __init__(self, dataYear):
        if dataYear not in JVM_CONFIG:
            raise RuntimeError("jetVetoMapProducer: unknown year %s" % dataYear)
        self.dataYear = dataYear
        # NanoAODv9 PU jet ID: loose/tight bits swapped in UL2016 -> loose = 1 (UL2016), 4 (UL2017/18)
        self.puIdLooseBit = 1 if dataYear.startswith('UL2016') else 4

        fname, hnames = JVM_CONFIG[dataYear]
        self._file = ROOT.TFile.Open(JVM_DIR + fname)
        if not self._file or self._file.IsZombie():
            raise RuntimeError("jetVetoMapProducer: cannot open %s" % (JVM_DIR + fname))
        self.maps = []
        for hname in hnames:
            h = self._file.Get(hname)
            if not h:
                raise RuntimeError("jetVetoMapProducer: map '%s' not found in %s" % (hname, fname))
            h.SetDirectory(0)
            self.maps.append(h)
            print("Jet veto map [%s] : %s : %s  (x axis: '%s', y axis: '%s')" % (
                dataYear, fname, hname, h.GetXaxis().GetTitle(), h.GetYaxis().GetTitle()))
        self._file.Close()

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("Jet_jetVetoed", "I", lenVar="nJet")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def passLooseSelection(self, jet, pfmuons):
        if jet.pt <= 15:
            return False
        if (jet.jetId & 2) == 0:                                   # tight jet ID
            return False
        if jet.pt < 50 and (jet.puId & self.puIdLooseBit) == 0:    # PU jet ID (loose WP) for CHS jets below 50 GeV
            return False
        if (jet.chEmEF + jet.neEmEF) >= 0.9:                       # EM fraction
            return False
        for mu in pfmuons:                                         # no PF muon within dR < 0.2
            if deltaR(jet.eta, jet.phi, mu.eta, mu.phi) < 0.2:
                return False
        return True

    def inVetoRegion(self, eta, phi):
        # maps are TH2 in (eta, phi); a non-zero bin content means the region is vetoed
        for h in self.maps:
            if h.GetBinContent(h.FindBin(eta, phi)) > 0:
                return True
        return False

    def analyze(self, event):
        jets = Collection(event, "Jet")
        pfmuons = [mu for mu in Collection(event, "Muon") if mu.isPFcand]
        flags = [1 if (self.passLooseSelection(jet, pfmuons) and self.inVetoRegion(jet.eta, jet.phi)) else 0
                 for jet in jets]
        self.out.fillBranch("Jet_jetVetoed", flags)
        return True


# constructors, same style as the other modules
jetVetoMap_UL2016preVFP  = lambda: jetVetoMapProducer('UL2016preVFP')
jetVetoMap_UL2016postVFP = lambda: jetVetoMapProducer('UL2016postVFP')
jetVetoMap_UL2017        = lambda: jetVetoMapProducer('UL2017')
jetVetoMap_UL2018        = lambda: jetVetoMapProducer('UL2018')
