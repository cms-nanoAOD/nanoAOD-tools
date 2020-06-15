import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class MCweight_writer(Module):
    def __init__(self):
        self.writeHistFile=True

    def beginJob(self,histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName)
        self.h_genweight = ROOT.TH1F('h_genweight', 'h_genweight', 10, 0, 9)
        self.h_q2weight = ROOT.TH1F('h_q2weight', 'h_q2weight', 8, 0, 7)
        self.h_psweight = ROOT.TH1F('h_psweight', 'h_psweight', 4, 0, 3)
        self.h_PDFweight = ROOT.TH1F()
        self.addObject(self.h_genweight)
        self.addObject(self.h_q2weight)
        self.addObject(self.h_psweight)
        self.addObject(self.h_PDFweight)

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        Generator = Object(event, "Generator")
        LHEPdfWeight = Collection(event, 'LHEPdfWeight')
        LHEScaleWeight = Collection(event, 'LHEScaleWeight')
        PSWeight = Collection(event, 'PSWeight')
        if not len(LHEPdfWeight) == 0:
            self.h_PDFweight.SetNameTitle('h_PDFweight', 'h_PDFweight')
            self.h_PDFweight.SetBins(len(LHEPdfWeight), 0, len(LHEPdfWeight))
            for pdfw, i in zip(LHEPdfWeight, xrange(1, len(LHEPdfWeight)+1)):
                self.h_PDFweight.GetXaxis().SetBinLabel(i, 'pdf['+str(i)+']')
                self.h_PDFweight.AddBinContent(i, pdfw.__getattr__(""))
        if not len(LHEScaleWeight) == 0: #LHE scale variation weights (w_var / w_nominal); [0] is muR=0.5 muF=0.5 hdamp=mt=272.7225 ; [1] is muR=0.5 muF=1 hdamp=mt=272.7225 ; [2] is muR=0.5 muF=2 hdamp=mt=272.7225 ; [3] is muR=1 muF=0.5 hdamp=mt=272.7225 ; [4] is muR=1 muF=1 hdamp=mt=272.7225 ; [5] is muR=1 muF=2 hdamp=mt=272.7225 ; [6] is muR=2 muF=0.5 hdamp=mt=272.7225 ; [7] is muR=2 muF=1 hdamp=mt=272.7225 ; [8] is muR=2 muF=2 hdamp=mt=272.7225
            self.h_q2weight.Fill('muR=0.5 muF=0.5', LHEScaleWeight[0].__getattr__(""))
            self.h_q2weight.Fill('muR=0.5 muF=1', LHEScaleWeight[1].__getattr__(""))
            self.h_q2weight.Fill('muR=0.5 muF=2', LHEScaleWeight[2].__getattr__(""))
            self.h_q2weight.Fill('muR=1 muF=0.5', LHEScaleWeight[3].__getattr__(""))
            self.h_q2weight.Fill('muR=1 muF=2', LHEScaleWeight[5].__getattr__(""))
            self.h_q2weight.Fill('muR=2 muF=0.5', LHEScaleWeight[6].__getattr__(""))
            self.h_q2weight.Fill('muR=2 muF=1', LHEScaleWeight[7].__getattr__(""))
            self.h_q2weight.Fill('muR=2 muF=2', LHEScaleWeight[8].__getattr__(""))
        if not len(PSWeight) == 0: #PS weights (w_var / w_nominal); [0] is ISR=0.5 FSR=1; [1] is ISR=1 FSR=0.5; [2] is ISR=2 FSR=1; [3] is ISR=1 FSR=2
            self.h_psweight.Fill('ISRdown', PSWeight[0].__getattr__(""))
            self.h_psweight.Fill('FSRdown', PSWeight[1].__getattr__(""))
            self.h_psweight.Fill('ISRup', PSWeight[2].__getattr__(""))
            self.h_psweight.Fill('FSRup', PSWeight[3].__getattr__(""))
        self.h_genweight.Fill("SumEvents", 1)
        self.h_genweight.Fill("GenWeights", Generator.weight)

        return True
