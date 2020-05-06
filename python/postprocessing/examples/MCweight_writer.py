import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class MCweight_writer(Module):
    def __init__(self):
        self.writeHistFile=True

    def beginJob(self,histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName)
        self.h_genweight = ROOT.TH1F('h_genweight', 'h_genweight', 10, 0, 10)
        self.h_PDFweight = ROOT.TH1F()
        self.addObject(self.h_genweight)
        self.addObject(self.h_PDFweight)

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        Generator = Object(event, "Generator")
        LHEPdfWeight = Collection(event, 'LHEPdfWeight')
        if not len(LHEPdfWeight) == 0:
            self.h_PDFweight.SetNameTitle('h_PDFweight', 'h_PDFweight')
            self.h_PDFweight.SetBins(len(LHEPdfWeight), 0, len(LHEPdfWeight))
            for pdfw, i in zip(LHEPdfWeight, xrange(1, len(LHEPdfWeight)+1)):
                self.h_PDFweight.GetXaxis().SetBinLabel(i, 'pdf['+str(i)+']')
                self.h_PDFweight.AddBinContent(i, pdfw.__getattr__(""))
        self.h_genweight.Fill("SumEvents", 1)
        self.h_genweight.Fill("GenWeights", Generator.weight)
        return True
