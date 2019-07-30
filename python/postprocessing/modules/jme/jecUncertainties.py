import ROOT
import os
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class jecUncertProducer(Module):
    def __init__(self,globalTag,uncerts=["Total"],jetFlavour="AK4PFchs",jetColl="Jet", doCppOutput=False):
        self.jetColl = jetColl
        self.uncerts=[(x,jetColl+"_jecUncert%s"%x) for x in uncerts]
        self.unc_factorized_path = "%s/%s_UncertaintySources_%s.txt" % ("%s/src/PhysicsTools/NanoAODTools/data/jme/" % os.environ['CMSSW_BASE'], globalTag, jetFlavour)

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
        jets = Collection(event, self.jetColl)
	for u,branchname in self.uncerts :
	    uworker=self.factorizedUncertainties[u]
	    jetUn=[]
       	    for j in jets :
        	uworker.setJetEta(j.eta)
        	uworker.setJetPt(j.pt)
		jetUn.append(uworker.getUncertainty(True))
  	    self.out.fillBranch(branchname, jetUn)
        return True

class jecUncertProducerCpp(jecUncertProducer,object):
    def __init__(self,*args,**kwargs):
        super(jecUncertProducerCpp,self).__init__(*args, **kwargs)
        self.doCppOutput = kwargs.get('doCppOutput',False)

        if "/jecUncertProducerCppWorker_cc.so" not in ROOT.gSystem.GetLibraries():
            print "Load C++ jecUncertProducerCppWorker worker module"
            base = os.getenv("NANOAODTOOLS_BASE")
            if base:
                ROOT.gROOT.ProcessLine(".L %s/src/jecUncertProducerCppWorker.cc+O"%base)
            else:
                base = "%s/src/PhysicsTools/NanoAODTools"%os.getenv("CMSSW_BASE")
                ROOT.gSystem.Load("libPhysicsToolsNanoAODTools.so")
                ROOT.gROOT.ProcessLine(".L %s/interface/jecUncertProducerCppWorker.h"%base)

    def beginJob(self):
        self.vec_uncerts = ROOT.std.vector(str)()
        for x in self.uncerts: self.vec_uncerts.push_back(x[0])
        self.worker = ROOT.jecUncertProducerCppWorker(self.unc_factorized_path,self.vec_uncerts)

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        if not self.doCppOutput:
            super(jecUncertProducerCpp,self).beginFile(inputFile, outputFile, inputTree, wrappedOutputTree)
        else:
            self.worker.doCppOutput(wrappedOutputTree.tree())
        self.initReaders(inputTree)

    def initReaders(self,tree):
        self.nJet = tree.valueReader("nJet")
        self.Jet_pt = tree.arrayReader(self.jetColl+"_pt")
        self.Jet_eta = tree.arrayReader(self.jetColl+"_eta")
        self.worker.setJets(self.nJet,self.Jet_pt,self.Jet_eta)
        self._ttreereaderversion = tree._ttreereaderversion

    def analyze(self, event):
        if event._tree._ttreereaderversion > self._ttreereaderversion:
            self.initReaders(event._tree)
        if self.doCppOutput:
            self.worker.fillAllUnc()
            return True
        for i,(x,branchname) in enumerate(self.uncerts):
            self.out.fillBranch(branchname,self.worker.getUnc(i))
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

# python looper
# you can re-use the uncertainty values in modules running after this one in the same event loop
jecUncert = lambda : jecUncertProducer( "Summer16_07Aug2017_V11_MC")
jecUncertAll = lambda : jecUncertProducer( "Summer16_07Aug2017_V11_MC",allUncerts)

# python looper with C++ helper to calculate uncertainties, faster
# you can re-use the uncertainty values in modules running after this one in the same event loop
jecUncert_cpp = lambda : jecUncertProducerCpp( "Summer16_07Aug2017_V11_MC")
jecUncertAll_cpp = lambda : jecUncertProducerCpp( "Summer16_07Aug2017_V11_MC",allUncerts)

# python looper with C++ helper also writing the output, fastest
# you cannot re-use the uncertainty values in modules running after this one in the same event loop
jecUncert_cppOut = lambda : jecUncertProducerCpp( "Summer16_07Aug2017_V11_MC",doCppOutput=True)
jecUncertAll_cppOut = lambda : jecUncertProducerCpp( "Summer16_07Aug2017_V11_MC",allUncerts,doCppOutput=True)


jecUncertAK4Puppi = lambda : jecUncertProducer( "Summer16_07Aug2017_V11_MC", jetFlavour="AK4PFPuppi")
jecUncertAK8Puppi = lambda : jecUncertProducer( "Summer16_07Aug2017_V11_MC", jetFlavour="AK8PFPuppi", jetColl="FatJet" )
