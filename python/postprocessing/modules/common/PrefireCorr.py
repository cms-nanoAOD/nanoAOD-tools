import ROOT
import math
ROOT.PyConfig.IgnoreCommandLineOptions = True
import re
import os

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class PrefCorr(Module):
    def __init__(self, jetroot="L1prefiring_jetpt_2017BtoF.root", jetmapname="L1prefiring_jetpt_2017BtoF",
                 photonroot="L1prefiring_photonpt_2017BtoF.root", photonmapname="L1prefiring_photonpt_2017BtoF"):

        cmssw_base = os.getenv('CMSSW_BASE')

        self.photon_file = self.open_root(cmssw_base + "/src/PhysicsTools/NanoAODTools/data/prefire_maps/" + photonroot)
        self.photon_map = self.get_root_obj(self.photon_file, photonmapname)

        self.jet_file = self.open_root(cmssw_base + "/src/PhysicsTools/NanoAODTools/data/prefire_maps/" + jetroot)
        self.jet_map = self.get_root_obj(self.jet_file, jetmapname)

        self.UseEMpT = ("jetempt" in jetroot)

    def open_root(self, path):
        r_file = ROOT.TFile.Open(path)
        if not r_file.__nonzero__() or not r_file.IsOpen(): raise NameError('File ' + path + ' not open')
        return r_file

    def get_root_obj(self, root_file, obj_name):
        r_obj = root_file.Get(obj_name)
        if not r_obj.__nonzero__(): raise NameError('Root Object ' + obj_name + ' not found')
        return r_obj

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.branchnames = ["PrefireWeight", "PrefireWeight_Up", "PrefireWeight_Down"]
        for bname in self.branchnames:
          self.out.branch(bname, "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        jets = Collection(event,"Jet")

        # Options
        self.JetMinPt = 20 # Min/Max Values may need to be fixed for new maps
        self.JetMaxPt = 500
        self.JetMinEta = 2.0
        self.JetMaxEta = 3.0
        self.PhotonMinPt = 20
        self.PhotonMaxPt = 500
        self.PhotonMinEta = 2.0
        self.PhotonMaxEta = 3.0

        for i,bname in zip([0,1,-1], self.branchnames):
          self.variation = i
          prefw = 1.0

          for jid,jet in enumerate(jets): # First loop over all jets
            jetpf = 1.0
            PhotonInJet = []

            jetpt = jet.pt
            if self.UseEMpT: jetpt *= (jet.chEmEF + jet.neEmEF)

            if jetpt >= self.JetMinPt and abs(jet.eta) <= self.JetMaxEta and abs(jet.eta) >= self.JetMinEta:
              jetpf *= 1-self.GetPrefireProbability(self.jet_map, jet.eta, jetpt, self.JetMaxPt)

            phopf = self.EGvalue(event, jid)
            prefw *= min(jetpf,phopf) # The higher prefire-probablity between the jet and the lower-pt photon(s)/elecron(s) from the jet is chosen

          prefw *= self.EGvalue(event, -1) # Then loop over all photons/electrons not associated to jets
          self.out.fillBranch(bname, prefw)
        return True

    def EGvalue(self, event, jid):
      photons = Collection(event,"Photon")
      electrons = Collection(event,"Electron")
      phopf = 1.0
      PhotonInJet = []

      for pid,pho in enumerate(photons):
        if pho.jetIdx == jid:
          if pho.pt >= self.PhotonMinPt and abs(pho.eta) <= self.PhotonMaxEta and abs(pho.eta) >= self.PhotonMinEta:
            phopf_temp = 1-self.GetPrefireProbability(self.photon_map, pho.eta, pho.pt, self.PhotonMaxPt)

            elepf_temp = 1.0
            if pho.electronIdx > -1: # What if the electron corresponding to the photon would return a different value?
              if event.Electron_pt[pho.electronIdx] >= self.PhotonMinPt and abs(event.Electron_eta[pho.electronIdx]) <= self.PhotonMaxEta and abs(event.Electron_eta[pho.electronIdx]) >= self.PhotonMinEta:
                elepf_temp = 1-self.GetPrefireProbability(self.photon_map, event.Electron_eta[pho.electronIdx], event.Electron_pt[pho.electronIdx], self.PhotonMaxPt)

            phopf *= min(phopf_temp, elepf_temp) # The higher prefire-probablity between the photon and corresponding electron is chosen
            PhotonInJet.append(pid)

      for ele in electrons:
        if ele.jetIdx == jid and (ele.photonIdx not in PhotonInJet):
          if ele.pt >= self.PhotonMinPt and abs(ele.eta) <= self.PhotonMaxEta and abs(ele.eta) >= self.PhotonMinEta:
            phopf *= 1-self.GetPrefireProbability(self.photon_map, ele.eta, ele.pt, self.PhotonMaxPt)

      return phopf

    def GetPrefireProbability(self, Map, eta, pt, maxpt):
      bin = Map.FindBin(eta, min(pt, maxpt-0.01))
      pref_prob = Map.GetBinContent(bin)

      stat = Map.GetBinError(bin) # bin statistical uncertainty
      syst = 0.2*pref_prob # 20% of prefire rate

      if self.variation == 1: 
        pref_prob = min(pref_prob + math.sqrt(stat*stat + syst*syst), 1.0)
      if self.variation == -1:
        pref_prob = max(pref_prob - math.sqrt(stat*stat + syst*syst), 0.0)
      return pref_prob

