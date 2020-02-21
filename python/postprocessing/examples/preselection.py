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
        self.out.branch("EventHT",  "F") 
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
        goodMu = []
        goodEle = []
        goodJet = []
        eventSum = ROOT.TLorentzVector()

        isGoodPV = (PV.ndof>4 and abs(PV.z)<20 and math.hypot(PV.x, PV.y)<2)
        for lep in muons:
            if(not(lep.tightId) and lep.looseId and lep.pt>35 and abs(lep.eta)<2.4):
                isVetoMu = True
            if(not(lep.tightId)):
                continue
            goodMu.append(lep)
            eventSum += lep.p4()          
        for lep in electrons:
            if(abs(lep.eta) > 1.4442 and abs(lep.eta) < 1.566):
                continue
            if(not(lep.mvaFall17V2noIso_WP90) and lep.mvaFall17V2noIso_WPL and lep.pt>35 and abs(lep.eta)<2.5):
                isVetoEle = True
            if(not(lep.mvaFall17V2noIso_WP90)):
                continue
            goodEle.append(lep)
            eventSum += lep.p4()        

        for j in jets:
            if abs(j.eta)<2.4 and j.pt>25:
                goodJet.append(j)
                eventSum += j.p4()

        self.out.fillBranch("EventHT",eventSum.Pt())

        isGoodEvent = ((((len(goodMu) >= 1) and (len(goodEle) == 0)) or ((len(goodMu) == 0) and (len(goodEle) >= 1))) and not isVetoMu and not isVetoEle and len(goodJet)>=1)
        goodEvent = isGoodPV and isGoodEvent
        #if(goodEvent):
            #print "No. Mu = ", len(goodMu), " No. Ele = ", len(goodEle), " veto Mu is ", not isVetoMu, " veto Ele is ", not isVetoEle, " No. barrel jets = ", len(goodJet)
        return goodEvent


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
#MySelectorModuleConstr = lambda : exampleProducer(jetetaSelection= lambda j : abs(j.eta)<2.4) 
 
