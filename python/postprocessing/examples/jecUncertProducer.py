import ROOT
import os
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class jecUncertProducer(Module):
    def __init__(self,globalTag,uncerts=["Total"],jetFlavour="AK4PFchs"):
	self.uncerts=[(x,"Jet_jecUncert%s"%x) for x in uncerts]
        self.unc_factorized_path = "%s/%s_UncertaintySources_%s.txt" % ("%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/jec/" % os.environ['CMSSW_BASE'], globalTag, jetFlavour)


    def beginJob(self):
        self.factorizedUncertainties = {}
        for u,n in self.uncerts:
            pars = ROOT.JetCorrectorParameters(self.unc_factorized_path, u);
            unc = ROOT.JetCorrectionUncertainty(pars)
            self.factorizedUncertainties[u] = unc


    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
	for u,branchname in self.uncerts :
	        self.out.branch(branchname, "F", lenVar="nJet")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = Collection(event, "Jet")
	for u,branchname in self.uncerts :
	    uworker=self.factorizedUncertainties[u]
	    jetUn=[]
       	    for j in jets :
        	uworker.setJetEta(j.eta)
        	uworker.setJetPt(j.pt)
		jetUn.append(uworker.getUncertainty(True))
  	    self.out.fillBranch(branchname, jetUn)
        return True

allUncerts=[
        "AbsoluteStat",
        "AbsoluteScale",
        "AbsoluteFlavMap",
        "AbsoluteMPFBias",
        "Fragmentation",
        "SinglePionECAL",
        "SinglePionHCAL",
        "FlavorQCD",
        "TimePtEta",
        "RelativeJEREC1",
        "RelativeJEREC2",
        "RelativeJERHF",
        "RelativePtBB",
        "RelativePtEC1",
        "RelativePtEC2",
        "RelativePtHF",
        "RelativeBal",
        "RelativeFSR",
        "RelativeStatFSR",
        "RelativeStatEC",
        "RelativeStatHF",
        "PileUpDataMC",
        "PileUpPtRef",
        "PileUpPtBB",
        "PileUpPtEC1",
        "PileUpPtEC2",
        "PileUpPtHF",
        "PileUpMuZero",
        "PileUpEnvelope",
        "SubTotalPileUp",
        "SubTotalRelative",
        "SubTotalPt",
        "SubTotalScale",
        "SubTotalAbsolute",
        "SubTotalMC",
        "Total",
        "TotalNoFlavor",
        "TotalNoTime",
        "TotalNoFlavorNoTime",
        "FlavorZJet",
        "FlavorPhotonJet",
        "FlavorPureGluon",
        "FlavorPureQuark",
        "FlavorPureCharm",
        "FlavorPureBottom",
        "TimeRunBCD",
        "TimeRunEF",
        "TimeRunG",
        "TimeRunH",
        "CorrelationGroupMPFInSitu",
        "CorrelationGroupIntercalibration",
        "CorrelationGroupbJES",
        "CorrelationGroupFlavor",
        "CorrelationGroupUncorrelated",
]

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

jecUncert = lambda : jecUncertProducer( "Summer16_23Sep2016V4_MC")
jecUncertAll = lambda : jecUncertProducer( "Summer16_23Sep2016V4_MC",allUncerts)

