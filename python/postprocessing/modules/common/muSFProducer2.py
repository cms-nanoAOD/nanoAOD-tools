import ROOT
import os
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

#../python/postprocessing/data/leptonSF/Efficiencies_muon_generalTracks_Z_Run2016_UL_HIPM_ID.root   ../python/postprocessing/data/leptonSF/Efficiencies_muon_generalTracks_Z_Run2016_UL_ID.root   ../python/postprocessing/data/leptonSF/Efficiencies_muon_generalTracks_Z_Run2017_UL_ID.root   ../python/postprocessing/data/leptonSF/Efficiencies_muon_generalTracks_Z_Run2018_UL_ID.root
#../python/postprocessing/data/leptonSF/Efficiencies_muon_generalTracks_Z_Run2016_UL_HIPM_ISO.root  ../python/postprocessing/data/leptonSF/Efficiencies_muon_generalTracks_Z_Run2016_UL_ISO.root  ../python/postprocessing/data/leptonSF/Efficiencies_muon_generalTracks_Z_Run2017_UL_ISO.root  ../python/postprocessing/data/leptonSF/Efficiencies_muon_generalTracks_Z_Run2018_UL_ISO.root

muFileDict={ '2016' : ['Run2016_UL_HIPM_', 'Run2016_UL2_'],
             '2017' : ['Run2017_UL_'],
             '2018' : ['Run2018_UL_']
           }


class lepSFProducerV2(Module):
    def __init__(self, lepFlavour="Muon", cut= "Trigger", histos=["IsoMu24_OR_IsoTkMu24_PtEtaBins/pt_abseta_ratio"], useAbseta=True, ptEtaAxis=True,dataYear="2016", runPeriod="B"):
        self.lepFlavour = lepFlavour
        self.histos = [h for h in histos]
        self.branchName = self.lepFlavour + "_" + cut
        if dataYear=="2016" and runPeriod=="H" : self.branchName = self.branchName + "_eraGH"
        self.useAbseta = useAbseta
        self.ptEtaAxis = ptEtaAxis
        for p in muFileDict[dataYear]:
            if runPeriod in p:
                effFile = p
        effFile += (cut + ".root")

        self.effFile = "%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/leptonSF/Efficiencies_muon_generalTracks_Z_%s" % (os.environ['CMSSW_BASE'], effFile)
        try:
            ROOT.gSystem.Load("libPhysicsToolsNanoAODTools")
            dummy = ROOT.WeightCalculatorFromHistogram
        except Exception as e:
            print "Could not load module via python, trying via ROOT", e
            if "/WeightCalculatorFromHistogram_cc.so" not in ROOT.gSystem.GetLibraries():
                print "Loading C++ helper from %s/src/PhysicsTools/NanoAODTools/src/WeightCalculatorFromHistogram.cc" % os.environ['CMSSW_BASE']
                ROOT.gROOT.ProcessLine(".L %s/src/PhysicsTools/NanoAODTools/src/WeightCalculatorFromHistogram.cc++" % os.environ['CMSSW_BASE'])
            dummy = ROOT.WeightCalculatorFromHistogram
        #print "Will Read scale factors for " + cut + " from " + self.effFile
        #print self.histos

    def beginJob(self):
        #print self.branchName
        print self.effFile, self.histos[0]
        self._worker_lep_SF = ROOT.WeightCalculatorFromHistogram(self.loadHisto(self.effFile, self.histos[0]))
        if len(self.histos) > 1:
            self._worker_lep_SFstat = ROOT.WeightCalculatorFromHistogram(self.loadHisto(self.effFile, self.histos[1]))
            if len(self.histos) > 2:
                self._worker_lep_SFsyst = ROOT.WeightCalculatorFromHistogram(self.loadHisto(self.effFile, self.histos[2]))
    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch(self.branchName + "_SF", "F", lenVar="n" + self.lepFlavour)
        self.out.branch(self.branchName + "_SFstat", "F", lenVar="n" + self.lepFlavour)
        self.out.branch(self.branchName + "_SFsyst", "F", lenVar="n" + self.lepFlavour)
        #self.out.branch("Electron_effSF", "F", lenVar="nElectron")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def loadHisto(self,filename,hname):
        #print "Trying to read ",hname, " from file:", filename
        tf = ROOT.TFile.Open(filename)
        hist = tf.Get(hname)
        #print hist.GetName()
        hist.SetDirectory(0)
        tf.Close()
        return hist

    def getSF(self, lepPt, lepEta):
        if self.useAbseta:
            lepEta = abs(lepEta)
        return self._worker_lep_SF.getWeight(lepPt, lepEta ) if self.ptEtaAxis else self._worker_lep_SF.getWeight(lepEta, lepPt )

    def getSFstaterr(self, lepPt, lepEta):
        if self.useAbseta:
            lepEta = abs(lepEta)
        return self._worker_lep_SFstat.getWeightErr(lepPt, lepEta ) if self.ptEtaAxis else self._worker_lep_SFstat.getWeightErr(lepEta, lepPt )

    def getSFsysterr(self, lepPt, lepEta):
        if self.useAbseta:
            lepEta = abs(lepEta)
        return self._worker_lep_SFsyst.getWeightErr(lepPt, lepEta ) if self.ptEtaAxis else self._worker_lep_SFsyst.getWeightErr(lepEta, lepPt )

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        leptons = Collection(event, self.lepFlavour)
        sf_lep = [ self.getSF(lep.pt,lep.eta) for lep in leptons ]
        if (len(self.histos) > 2):
            sf_lep_stat = [ self.getSFstaterr(lep.pt, lep.eta) for lep in leptons ]
            sf_lep_syst = [ self.getSFsysterr(lep.pt, lep.eta) for lep in leptons ]
        elif(len(self.histos) > 1):
            sf_lep_stat = [ self.getSFstaterr(lep.pt, lep.eta) for lep in leptons ]
            sf_lep_syst = [ 0.005 for lep in leptons ]
        else:
            sf_lep_stat = [ 0.005 for lep in leptons ]
            sf_lep_syst = [ 0.005 for lep in leptons ]
        self.out.fillBranch(self.branchName + "_SF", sf_lep)
        self.out.fillBranch(self.branchName + "_SFstat", sf_lep_stat)
        self.out.fillBranch(self.branchName + "_SFsyst", sf_lep_syst)
        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

#lepSF = lambda : lepSFProducer( "LooseWP_2016", "GPMVA90_2016")


##Muon SF
idHisto = {2016: ["NUM_LooseID_DEN_TrackerMuons_abseta_pt", "NUM_LooseID_DEN_TrackerMuons_abseta_pt_stat", "NUM_LooseID_DEN_TrackerMuons_abseta_pt_syst"], 
           2017: ["NUM_LooseID_DEN_TrackerMuons_abseta_pt", "NUM_LooseID_DEN_TrackerMuons_abseta_pt_stat", "NUM_LooseID_DEN_TrackerMuons_abseta_pt_syst"],
           2018: ["NUM_LooseID_DEN_TrackerMuons_abseta_pt", "NUM_LooseID_DEN_TrackerMuons_abseta_pt_stat", "NUM_LooseID_DEN_TrackerMuons_abseta_pt_syst"]
           }

isoHisto = {2016: ["NUM_LooseRelIso_DEN_LooseID_abseta_pt", "NUM_LooseRelIso_DEN_LooseID_abseta_pt_stat", "NUM_LooseRelIso_DEN_LooseID_abseta_pt_syst"],
            2017: ["NUM_LooseRelIso_DEN_LooseID_abseta_pt", "NUM_LooseRelIso_DEN_LooseID_abseta_pt_stat", "NUM_LooseRelIso_DEN_LooseID_abseta_pt_syst"],
            2018: ["NUM_LooseRelIso_DEN_LooseID_abseta_pt", "NUM_LooseRelIso_DEN_LooseID_abseta_pt_stat", "NUM_LooseRelIso_DEN_LooseID_abseta_pt_syst"]
}

##This is required beacuse for 2016 ID SF, binning is done for eta;x-axis is eta
##But in any case, maybe useful if POG decides to switch from abs(eta) to eta
##Not used for Trigger
useAbsEta = { 2016 : True, 2017 : True, 2018 : True}
ptEtaAxis = { 2016 : True, 2017 : True, 2018 : True}

lepSFID2016_B   = lambda : lepSFProducerV2(lepFlavour="Muon", cut = "ID", histos=idHisto[2016], dataYear="2016", runPeriod="UL_HIPM", useAbseta=useAbsEta[2016], ptEtaAxis=ptEtaAxis[2016])
lepSFISO2016_B  = lambda : lepSFProducerV2(lepFlavour="Muon", cut = "ISO", histos=isoHisto[2016], dataYear="2016", runPeriod="UL_HIPM", useAbseta=useAbsEta[2016], ptEtaAxis=ptEtaAxis[2016])

lepSFID2016_H   = lambda : lepSFProducerV2(lepFlavour="Muon", cut = "ID", histos=idHisto[2016], dataYear="2016", runPeriod="UL2", useAbseta=useAbsEta[2016], ptEtaAxis=ptEtaAxis[2016])
lepSFISO2016_H  = lambda : lepSFProducerV2(lepFlavour="Muon", cut = "ISO", histos=isoHisto[2016], dataYear="2016", runPeriod="UL2", useAbseta=useAbsEta[2016], ptEtaAxis=ptEtaAxis[2016])

lepSFID2017   = lambda : lepSFProducerV2(lepFlavour="Muon", cut = "ID", histos=idHisto[2017], dataYear="2017", runPeriod="UL", useAbseta=useAbsEta[2017], ptEtaAxis=ptEtaAxis[2017])
lepSFISO2017  = lambda : lepSFProducerV2(lepFlavour="Muon", cut = "ISO", histos=isoHisto[2017], dataYear="2017", runPeriod="UL", useAbseta=useAbsEta[2017], ptEtaAxis=ptEtaAxis[2017])

lepSFID2018   = lambda : lepSFProducerV2(lepFlavour="Muon", cut = "ID", histos=idHisto[2018], dataYear="2018", runPeriod="UL", useAbseta=useAbsEta[2018], ptEtaAxis=ptEtaAxis[2018])
lepSFISO2018  = lambda : lepSFProducerV2(lepFlavour="Muon", cut = "ISO", histos=isoHisto[2018], dataYear="2018", runPeriod="UL", useAbseta=useAbsEta[2018], ptEtaAxis=ptEtaAxis[2018])

#source
#https://raw.githubusercontent.com/gmandorl/nanoAOD-tools/master/python/postprocessing/modules/common/lepSFProducer_v2.py
