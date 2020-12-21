import ROOT
import math
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *

class highpt(Module):
    def __init__(self):
        pass 
    def beginJob(self):
        pass
    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("isTight",  "F")
        self.out.branch("isMCTight",  "F")
        self.out.branch("isHighPt",  "F")
        self.out.branch("isMCHighPt",  "F")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        fatjets = Collection(event, "FatJet")
        PV = Object(event, "PV")

        isGoodPV = (PV.ndof>4 and abs(PV.z)<20 and math.hypot(PV.x, PV.y)<2)

        goodMu = list(filter(lambda x : x.tightId and x.pt > 55 and abs(x.eta) < 2.4 and x.miniPFRelIso_all < 0.1, muons))
        highMu = list(filter(lambda x : x.highPtId == 2 and x.pt > 55 and abs(x.eta) < 2.4 and x.miniPFRelIso_all < 0.1, muons))
        looseMu = list(filter(lambda x : x.looseId and not x.tightId and x.pt > 35 and x.miniPFRelIso_all < 0.4 and abs(x.eta) < 2.4, muons))
        goodEle = list(filter(lambda x : x.mvaFall17V2noIso_WP90 and x.miniPFRelIso_all < 0.1 and ((abs(x.eta) < 1.4442) or (abs(x.eta) > 1.566 and abs(x.eta) < 2.5)), electrons))
        looseEle = list(filter(lambda x : x.mvaFall17V2noIso_WPL and not x.mvaFall17V2noIso_WP90 and x.miniPFRelIso_all < 0.4 and x.pt > 35 and ((abs(x.eta) < 1.4442) or (abs(x.eta) > 1.566 and abs(x.eta)< 2.5)), electrons))
        goodJet = list(filter(lambda x : x.jetId >= 2 and abs(x.eta) < 2.4 and x.pt > 100, jets))

        isGoodEvent = (((len(goodMu) == 1) and (len(goodEle) == 0)) and len(goodJet)>=1 and len(fatjets) > 1)
        isHighEvent = (((len(highMu) == 1) and (len(goodEle) == 0)) and len(goodJet)>=1 and len(fatjets) > 1)

        self.out.fillBranch("isTight", int(isGoodEvent and isGoodPV))
        self.out.fillBranch("isMCTight", int(isGoodEvent and isGoodPV and (goodMu[0].genPartFlav == 1 or goodMu[0].genPartFlav == 15)))
        self.out.fillBranch("isHighPt", int(isHighEvent and isGoodPV))
        self.out.fillBranch("isMCHighPt", int(isHighEvent and isGoodPV and (highMu[0].genPartFlav == 1 or highMu[0].genPartFlav == 15)))

        return isGoodPV and (isGoodEvent or isHighEvent)

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
#MySelectorModuleConstr = lambda : exampleProducer(jetetaSelection= lambda j : abs(j.eta)<2.4) 
