import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class MCweight_writer(Module):
    def __init__(self):
        self.writeHistFile=True

    def beginJob(self,histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName)
        self.h_genweight=ROOT.TH1F('h_genweight', 'h_genweight', 100, 0, 1000)
        self.addObject(self.h_genweight)

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        Generator = Object(event, "Generator")
        self.h_genweight.Fill("GenWeights", Generator.weight)
        return True #need to be always True because it needs to write the weights of all the events.
