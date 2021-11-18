from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os
from math import log

def fill_stdvec(lst):
    try:
        vec = ROOT.std.vector["float"]()
    except AttributeError: # pre-war pyROOT
        vec = ROOT.std.vector("float")()
    for i in lst: vec.push_back(float(i))
    return vec

class TopLeptonMVAProducer(Module):
    def __init__(self, weightFileMuons, weightFileElectrons):
        weightFileMuons = os.path.join(os.getenv("CMSSW_BASE"), "src", "PhysicsTools", "NanoAODTools", "data", "TOP", weightFileMuons)
        # could use ROOT.TMVA.Experimental.RReader if a postwar ROOT version is available
        self.readerMuons = ROOT.TMVA.Reader("dxylog:miniIsoCharged:miniIsoNeutral:pTRel:sip3d:segmentCompatibility:ptRatio:bTagDeepJetClosestJet:pt:trackMultClosestJet:etaAbs:dzlog:relIso", "")
        self.muonMVAName = "BDT::BDTG_cuts200_depth4_trees1000_shrinkage0p1_muon"
        self.readerMuons.BookMVA(self.muonMVAName, weightFileMuons)
        weightFileElectrons = os.path.join(os.getenv("CMSSW_BASE"), "src", "PhysicsTools", "NanoAODTools", "data", "TOP", weightFileElectrons)
        self.readerElectrons = ROOT.TMVA.Reader("dxylog:miniIsoCharged:miniIsoNeutral:pTRel:sip3d:mvaIdFall17v2noIso:ptRatio:bTagDeepJetClosestJet:pt:trackMultClosestJet:etaAbs:dzlog:relIso", "")
        self.electronMVAName = "BDT::BDTG_cuts200_depth4_trees1000_shrinkage0p1_elec"
        self.readerElectrons.BookMVA(self.electronMVAName, weightFileElectrons)

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("Muon_topLeptonMVA", "F", lenVar="nMuon")
        self.out.branch("Electron_topLeptonMVA", "F", lenVar="nElectron")

    def analyze(self, event):
        jets = Collection(event, "Jet")

        electrons = Collection(event, "Electron")
        electronMVAs = []
        for electron in electrons:
            electron_jet = jets[electron.jetIdx] if (electron.jetIdx >= 0 and electron.jetIdx < len(jets)) else None

            dxylog = log(abs(electron.dxy)) if abs(electron.dxy) > 0. else 0.
            miniIsoCharged = electron.miniPFRelIso_chg
            miniIsoNeutral = electron.miniPFRelIso_all - electron.miniPFRelIso_chg
            pTRel = electron.jetPtRelv2
            sip3d = electron.sip3d
            mvaIdFall17v2noIso = electron.mvaFall17V2noIso
            ptRatio = min(1. / (electron.jetRelIso + 1.), 1.5) if electron_jet else (1. / (electron.jetRelIso + 1.))
            # MVA input:
            #         ptRatio = userCand('jetForLepJetVar').isNonnull()?
            #                       min(userFloat('ptRatio'),1.5) :
            #                       1.0/(1.0+userFloat('PFIsoAll04')/pt)
            # jetRelIso definition:
            #         jetRelIso = userCand('jetForLepJetVar').isNonnull()?
            #                       (1./userFloat('ptRatio'))-1. : 
            #                       userFloat('PFIsoAll04')/pt
            bTagDeepJetClosestJet = max(electron_jet.btagDeepFlavB, 0.) if electron_jet else 0.
            pt = electron.pt
            trackMultClosestJet = electron.jetNDauCharged if hasattr(electron, "jetNDauCharged") else electron.jetNDauChargedMVASel # different name in topNanoAOD
            etaAbs = abs(electron.eta)
            dzlog = log(abs(electron.dz)) if abs(electron.dz) > 0. else 0.
            relIso = electron.pfRelIso03_all

            mvaInputs = fill_stdvec([dxylog, miniIsoCharged, miniIsoNeutral, pTRel, sip3d, mvaIdFall17v2noIso, ptRatio, bTagDeepJetClosestJet, pt, trackMultClosestJet, etaAbs, dzlog, relIso])
            electronMVAs.append(self.readerElectrons.EvaluateMVA(mvaInputs, self.electronMVAName))

        muons = Collection(event, "Muon")
        muonMVAs = []
        for muon in muons:
            muon_jet = jets[muon.jetIdx] if (muon.jetIdx >= 0 and muon.jetIdx < len(jets)) else None

            dxylog = log(abs(muon.dxy)) if abs(muon.dxy) > 0. else 0.
            miniIsoCharged = muon.miniPFRelIso_chg
            miniIsoNeutral = muon.miniPFRelIso_all - muon.miniPFRelIso_chg
            pTRel = muon.jetPtRelv2
            sip3d = muon.sip3d
            segmentCompatibility = muon.segmentComp
            ptRatio = min(1. / (muon.jetRelIso + 1.), 1.5) if muon_jet else (1. / (muon.jetRelIso + 1.))
            # MVA input:
            #         ptRatio = userCand('jetForLepJetVar').isNonnull()?
            #                      min(userFloat('ptRatio'),1.5) :
            #                      1.0/(1.0+(pfIsolationR04().sumChargedHadronPt + max(pfIsolationR04().sumNeutralHadronEt + pfIsolationR04().sumPhotonEt - pfIsolationR04().sumPUPt/2,0.0))/pt)"),
            # jetRelIso definition:
            #         jetRelIso = userCand('jetForLepJetVar').isNonnull()?
            #                         (1./userFloat('ptRatio'))-1. :
            #                         (pfIsolationR04().sumChargedHadronPt + max(pfIsolationR04().sumNeutralHadronEt + pfIsolationR04().sumPhotonEt - pfIsolationR04().sumPUPt/2,0.0))/pt
            bTagDeepJetClosestJet = max(muon_jet.btagDeepFlavB, 0.) if muon_jet else 0.
            pt = muon.pt
            trackMultClosestJet = muon.jetNDauCharged if hasattr(muon, "jetNDauCharged") else muon.jetNDauChargedMVASel # different name in topNanoAOD
            etaAbs = abs(muon.eta)
            dzlog = log(abs(muon.dz)) if abs(muon.dz) > 0. else 0.
            relIso = muon.pfRelIso03_all

            mvaInputs = fill_stdvec([dxylog, miniIsoCharged, miniIsoNeutral, pTRel, sip3d, segmentCompatibility, ptRatio, bTagDeepJetClosestJet, pt, trackMultClosestJet, etaAbs, dzlog, relIso])
            muonMVAs.append(self.readerMuons.EvaluateMVA(mvaInputs, self.muonMVAName))

        self.out.fillBranch("Electron_topLeptonMVA", electronMVAs)
        self.out.fillBranch("Muon_topLeptonMVA", muonMVAs)

        return True

def getLeptonMVAProducer(year):
    return lambda: TopLeptonMVAProducer("TMVA_BDTG_TOP_muon_" + year + ".weights.xml", "TMVA_BDTG_TOP_elec_" + year + ".weights.xml")

topLeptonMVA2016 = getLeptonMVAProducer("2016")
topLeptonMVA2017 = getLeptonMVAProducer("2017")
topLeptonMVA2018 = getLeptonMVAProducer("2018")
