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
        self.h_nevents=ROOT.TH1D('nEvents',   'nEvents',   1, 0, 1)
#        self.h_nweightedevents=ROOT.TH1D('nWeightedEvents',   'nWeightedEvents',   1, 0, 1) #kept for backwards compatibility, please move to nEventsGenWeighted
        self.h_neventsgenweighted=ROOT.TH1D('nEventsGenWeighted',   'nEventsGenWeighted',   1, 0, 1)

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        prevdir = ROOT.gDirectory
        outputFile.cd()
        self.h_nevents.Write()
#        self.h_nweightedevents.Write()
        self.h_neventsgenweighted.Write()
        prevdir.cd()        
    def analyze(self, event):
        self.h_nevents.Fill(0.5)

        if hasattr(event,'Generator_weight') and event.Generator_weight < 0:
            self.h_neventsgenweighted.Fill(0.5,-1)
#            self.h_nweightedevents.Fill(-0.5)
        else:    
            self.h_neventsgenweighted.Fill(0.5)
#            self.h_nweightedevents.Fill(0.5)

        return True

countHistogramsModule = lambda : countHistogramsProducer() 

