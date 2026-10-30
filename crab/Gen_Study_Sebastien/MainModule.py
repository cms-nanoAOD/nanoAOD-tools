import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from Gen_mass_functions import *

class MainProducer(Module):
    def __init__(self):
	pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
	self.out.branch("top_mass_gen", "F")	

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
	Genparts = Collection(event,"GenPart")
	for genpart in Genparts:
	    if(abs(genpart.pdgId)==6):
		motheridx =  genpart.genPartIdxMother
                PDG = genpart.pdgId
                motherPDG,Gmotheridx,GmotherPDG = findMother(motheridx,Genparts)
		if(abs(motherPDG!=6)):
		    top_mass_gen = genpart.mass
                    #self.top_mass_hist.Fill(genpart.mass)
                    self.out.fillBranch("top_mass_gen", top_mass_gen)
        return True


# define modules using the pt_Thes_mu[self.datayear]syntax 'name = lambda : constructor' to avoid having them loaded when not needed

MainModuleConstr_Gen = lambda : MainProducer()
