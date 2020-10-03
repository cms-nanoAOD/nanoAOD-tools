import ROOT
import math
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *

class preselection(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("HT_eventHT",  "F") 
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        goodEvent = False
        isVetoMu = False
        isVetoEle = False
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        fatjets = Collection(event, "FatJet")
        PV = Object(event, "PV")
        goodEle = []
        goodJet = []
        eventSum = ROOT.TLorentzVector()

        isGoodPV = (PV.ndof>4 and abs(PV.z)<20 and math.hypot(PV.x, PV.y)<2)

        goodMu = list(filter(lambda x : x.tightId and abs(x.eta) < 2.4 and x.miniPFRelIso_all < 0.1, muons))
        looseMu = list(filter(lambda x : x.looseId and not x.tightId and x.pt > 35 and x.miniPFRelIso_all < 0.4 and abs(x.eta) < 2.4, muons))
        goodEle = list(filter(lambda x : x.mvaFall17V2noIso_WP90 and x.miniPFRelIso_all < 0.1 and ((abs(x.eta) < 1.4442) or (abs(x.eta) > 1.566 and abs(x.eta) < 2.5)), electrons))
        looseEle = list(filter(lambda x : x.mvaFall17V2noIso_WPL and not x.mvaFall17V2noIso_WP90 and x.miniPFRelIso_all < 0.4 and x.pt > 35 and ((abs(x.eta) < 1.4442) or (abs(x.eta) > 1.566 and abs(x.eta)< 2.5)), electrons))
        goodJet = list(filter(lambda x : x.jetId >= 2 and abs(x.eta) < 2.4 and x.pt > 25, jets))

        for j in goodJet:
            eventSum += j.p4()

        self.out.fillBranch("HT_eventHT", eventSum.Pt())

        isGoodEvent = ((((len(goodMu) >= 1) and (len(goodEle) == 0)) or ((len(goodMu) == 0) and (len(goodEle) >= 1))) and len(goodJet)>=1)
        goodEvent = isGoodPV and isGoodEvent
        #if(goodEvent):
            #print "No. Mu = ", len(goodMu), " No. Ele = ", len(goodEle), " veto Mu is ", not isVetoMu, " veto Ele is ", not isVetoEle, " No. barrel jets = ", len(goodJet)
        return goodEvent

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
#MySelectorModuleConstr = lambda : exampleProducer(jetetaSelection= lambda j : abs(j.eta)<2.4) 
