import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class countHistogramsProducer(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.h_nevents=ROOT.TH1F('nEvents',   'nEvents',   1, 0, 1)
        #self.h_nweightedevents=ROOT.TH1F('nWeightedEvents',   'nWeightedEvents',   1, 0, 1)

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        prevdir = ROOT.gDirectory
        outputFile.cd()
        self.h_nevents.Write()
        #self.h_nweightedevents.Write()
        prevdir.cd()        
    def analyze(self, event):
        self.h_nevents.Fill(0.5)
        
        #if genWeight.genWeight > 0:
        #    self.h_nweightedevents.Fill(0.5)
        #else:
        #    self.h_nweightedevents.Fill(-0.5)

        return True

countHistogramsModule = lambda : countHistogramsProducer() 

