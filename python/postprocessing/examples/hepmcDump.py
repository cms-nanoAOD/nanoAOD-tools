import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class hepmcDump(Module, object):
    def __init__(self, *args, **kwargs):
        super(hepmcDump,self).__init__(*args, **kwargs)
        self.doCppOutput = kwargs.get('doCppOutput',False)
        self.hepmcDumpFileName = kwargs.get('fileName', "hepmc.dat")

        if "/hepmcDumpCppWorker_cc.so" not in ROOT.gSystem.GetLibraries():
            print "Load C++ hepmcDumpCppWorker worker module"
            base = os.getenv("NANOAODTOOLS_BASE")
            if base:
                ROOT.gROOT.ProcessLine(".L %s/src/hepmcDumpCppWorker.cc+O"%base)
            else:
                base = "%s/src/PhysicsTools/NanoAODTools"%os.getenv("CMSSW_BASE")
                ROOT.gSystem.Load("libPhysicsToolsNanoAODTools.so")
                ROOT.gROOT.ProcessLine(".L %s/interface/hepmcDumpCppWorker.h"%base)
        pass
    def beginJob(self):
        self.worker = ROOT.hepmcDumpCppWorker(self.hepmcDumpFileName)
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        super(hepmcDump,self).beginFile(inputFile, outputFile, inputTree, wrappedOutputTree)
        #self.worker.doCppOutput(wrappedOutputTree.tree())
        self.initReaders(inputTree)
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def initReaders(self,tree):
        self.eventNumber     = tree.valueReader("event")
        self.genWeight       = tree.valueReader("genWeight")
        self.Generator_x1    = tree.valueReader("Generator_x1")
        self.Generator_x2    = tree.valueReader("Generator_x2")
        self.nLHEScaleWeight = tree.valueReader("nLHEScaleWeight")
        self.LHEScaleWeight  = tree.arrayReader("LHEScaleWeight")
        self.nLHEPdfWeight   = tree.valueReader("nLHEPdfWeight")
        self.LHEPdfWeight    = tree.arrayReader("LHEPdfWeight")
        #self.worker.setGenEventInfo(self.eventNumber, self.genWeight) ## If you don't want to keep weights for the systematic uncertainty
        self.worker.setGenEventInfo(self.eventNumber, self.genWeight,
                                    self.Generator_x1, self.Generator_x2,
                                    self.nLHEScaleWeight, self.LHEScaleWeight,
                                    self.nLHEPdfWeight, self.LHEPdfWeight)

        self.nGenPart                 = tree.valueReader("nGenPart")
        self.GenPart_pt               = tree.arrayReader("GenPart_pt")
        self.GenPart_eta              = tree.arrayReader("GenPart_eta")
        self.GenPart_phi              = tree.arrayReader("GenPart_phi")
        self.GenPart_mass             = tree.arrayReader("GenPart_mass")
        self.GenPart_pdgId            = tree.arrayReader("GenPart_pdgId")
        self.GenPart_status           = tree.arrayReader("GenPart_status")
        self.GenPart_genPartIdxMother = tree.arrayReader("GenPart_genPartIdxMother")
        self.worker.setGenParticles(self.nGenPart,
                                    self.GenPart_pt, self.GenPart_eta, self.GenPart_phi, self.GenPart_mass,
                                    self.GenPart_pdgId, self.GenPart_status, self.GenPart_genPartIdxMother)

        self._ttreereaderversion = tree._ttreereaderversion
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        if event._tree._ttreereaderversion > self._ttreereaderversion:
            self.initReaders(event._tree)
        self.worker.genEvent()
        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

hepmc = lambda : hepmcDump(fileName="hepmc.dat")
 
