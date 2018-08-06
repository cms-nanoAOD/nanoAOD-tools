import os
import sys
import math
import ROOT
import random

def getHist(relFileName,histName):
    rootFile = ROOT.TFile(os.path.expandvars("$CMSSW_BASE/src/"+relFileName))
    hist = rootFile.Get(histName)
    if not hist:
        raise Exception("Hist file '"+histName+"' not found in file '"+relFileName+"'")
    hist = hist.Clone(histName+str(random.random()))
    hist.SetDirectory(0)
    rootFile.Close()
    return hist
    
def getGraph(relFileName,graphName):
    rootFile = ROOT.TFile(os.path.expandvars("$CMSSW_BASE/src/"+relFileName))
    graph = rootFile.Get(graphName)
    if not graph:
        raise Exception("Graph file '"+graphName+"' not found in file '"+relFileName+"'")
    graph = graph.Clone(graphName+str(random.random()))
    rootFile.Close()
    return graph
        
def combineHist2D(hist1,hist2,w1,w2):
    result = hist1.Clone(hist1.GetName()+hist2.GetName())
    result.SetDirectory(0)
    for ibin in range(hist1.GetNbinsX()):
        for jbin in range(hist2.GetNbinsX()):
            result.SetBinContent(ibin+1,jbin+1,
                w1*hist1.GetBinContent(ibin+1,jbin+1)+\
                w2*hist2.GetBinContent(ibin+1,jbin+1)
            )
            result.SetBinError(ibin+1,jbin+1,
                math.sqrt(
                    (w1*hist1.GetBinError(ibin+1,jbin+1))**2+\
                    (w2*hist2.GetBinError(ibin+1,jbin+1))**2
                )
            )
    return result
    
def getSFPtEta(hist,pt,eta):
    ptBin = hist.GetXaxis().FindBin(pt)
    etaBin = hist.GetYaxis().FindBin(math.fabs(eta))
    
    if ptBin==0:
        ptBin=1
    if ptBin>hist.GetNbinsX():
        ptBin=hist.GetNbinsX()
        
    if etaBin==0:
        etaBin = 1
    if etaBin>hist.GetNbinsY():
        etaBin=hist.GetNbinsY()
        
    return hist.GetBinContent(ptBin,etaBin),hist.GetBinError(ptBin,etaBin)
    
