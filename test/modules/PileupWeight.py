import os
import sys
import math
import json
import ROOT
import random
import numpy

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class PileupWeight(Module):
    def __init__(
        self,
        mcFile =  os.path.expandvars("$CMSSW_BASE/src/PhysicsTools/NanoAODTools/data/pu/pileup.root"),
        dataFile = os.path.expandvars("$CMSSW_BASE/src/PhysicsTools/NanoAODTools/data/pu/PU69000.root"),
        outputName ="puweight",
        processName=None,
        globalOptions={"isData":False}
    ):
        self.mcFile = mcFile
        self.dataFile = dataFile
        self.outputName = outputName
        self.globalOptions = globalOptions
        self.processName = processName
        
    def beginJob(self):
        if not self.globalOptions["isData"]:
            self.mcHistPerProcess = {}
            fMC = ROOT.TFile(self.mcFile)
            if not fMC:
                print "ERROR: Cannot find pileup file: ",self.mcFile
                sys.exit(1)
            for k in fMC.GetListOfKeys():
                self.mcHistPerProcess[k.GetName()] = fMC.Get(k.GetName()).Clone(k.GetName()+str(random.random()))
                self.mcHistPerProcess[k.GetName()].SetDirectory(0)
            fMC.Close()
            
            
            fData = ROOT.TFile(self.dataFile)
            if not fData:
                print "ERROR: Cannot find pileup file: ",self.dataFile
                sys.exit(1)
                
            self.dataHist = fData.Get("pileup").Clone("pileup"+str(random.random()))
            self.dataHist.SetDirectory(0)
           
            
        
    def getWeight(self,nTrueInteractions):
        mcBin = self.mcHist.FindBin(nTrueInteractions)
        dataBin = self.dataHist.FindBin(nTrueInteractions)
        w = self.dataHist.GetBinContent(dataBin)/(self.mcHist.GetBinContent(mcBin)+self.mcHist.Integral()*0.0001)
        if w>5.:
            w = 0
        return w
        
    def endJob(self):
        pass
        
    def normHist(self,hist):
        #normalization makes weight independent of binning scheme/range of histograms
        hist.Scale(1./hist.Integral())
        for ibin in range(hist.GetNbinsX()):
            w = hist.GetBinWidth(ibin+1)
            c = hist.GetBinContent(ibin+1)
            hist.SetBinContent(ibin+1,c/w)
            
    '''
    def interpolateHist(self,hist,binning):
        newHist = ROOT.TH1F("new"+hist.GetName()+str(random.random()),"",
            len(binning)-1,binning
        )
        newHist.SetDirectory(0)
        for ibin in range(1,newHist.GetNbinsX()-1):
            oldBin = hist.GetXaxis().FindBin(newHist.GetBinCenter(ibin+1))
            if newHist.GetBinCenter(ibin+1)>hist.GetBinCenter(oldBin):
                leftC = hist.GetBinContent(oldBin)
                leftP = hist.GetBinCenter(oldBin)
                
                rightC = hist.GetBinContent(oldBin+1)
                rightP = hist.GetBinCenter(oldBin+1)
            else:
                leftC = hist.GetBinContent(oldBin-1)
                leftP = hist.GetBinCenter(oldBin-1)
                
                rightC = hist.GetBinContent(oldBin)
                rightP = hist.GetBinCenter(oldBin)
            
            frac = (newHist.GetBinCenter(ibin+1)-leftP)/(rightP-leftP)
            interC = frac*leftC+(1-frac)*rightC
            newHist.SetBinContent(interC)
    '''
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        if not self.globalOptions["isData"]:
            self.mcHist = None
            for process in self.mcHistPerProcess.keys():
                processName = inputFile.GetName()
                if self.processName!=None:
                    processName = self.processName
                if processName.find(process)>=0:
                    self.mcHist = self.mcHistPerProcess[process]
                    break
            if self.mcHist==None:
                print "ERROR: Cannot find pileup profile for file: "+inputFile.GetName()
                sys.exit(1)
                 
            self.normHist(self.mcHist)
            self.normHist(self.dataHist)

            self.out.branch(self.outputName,"F")
            self.sum2 = 0
            self.sum = 0
            self.n = 0
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        if not self.globalOptions["isData"] and self.n>0 and (self.sum2/(1.*self.n))>(self.sum**2/(1.*self.n**2)):
            avg = 1.*self.sum/self.n
            sig = math.sqrt(self.sum2/(1.*self.n)-self.sum**2/(1.*self.n**2))
            print "Average pileup weight (%s): %6.3f +- %6.3f"%(self.outputName,avg,sig)
        
    def analyze(self, event):
        if not self.globalOptions["isData"]:
            puWeight = 1.
            puWeight = self.getWeight(event.Pileup_nTrueInt)
            self.n += 1
            self.sum+=puWeight
            self.sum2+=puWeight**2
            self.out.fillBranch(self.outputName,puWeight)
        return True
        
