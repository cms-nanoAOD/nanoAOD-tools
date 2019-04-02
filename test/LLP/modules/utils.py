import os
import sys
import math
import ROOT
import random

class PhysicsObject(object):
    def __init__(self,obj,pt=0.,eta=0.,phi=0.,mass=0.,keys=[]):
        self._obj = obj
        self._index = self._obj._index
        self.__dict__["pt"] = pt
        self.__dict__["eta"] = eta
        self.__dict__["phi"] = phi
        self.__dict__["mass"] = mass
        for k in keys:
            self.__dict__[k] = getattr(obj,k)
            
    def p4(self):
        ret = ROOT.TLorentzVector()
        ret.SetPtEtaPhiM(self.pt,self.eta,self.phi,self.mass)
        return ret
        
    def originalP4(self):
        return self._obj.p4()
        
    def __str__(self):
        return self._obj.__str__()
        

        
def deltaPhi(phi1,phi2):
    res = phi1-phi2
    while (res>math.pi):
        res -= 2*math.pi
    while (res<=-math.pi):
        res += 2*math.pi
    return res
    
def deltaR(j1,j2):
    return math.sqrt(
        (j1.eta-j2.eta)**2+\
        deltaPhi(j1.phi,j2.phi)**2
    )
    
def getCtauLabel(logctau):
    if logctau==0:
        return "0"
    elif logctau>0:
        return "1"+(("0")*logctau)
    elif logctau<0:
        return "0p"+(("0")*(abs(logctau)-1))+"1"


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
     
def getX(hist, x):
    xbin = hist.GetXaxis().FindBin(x)
    
    return hist.GetBinContent(xbin), hist.GetBinError(xbin)
    
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
    
def getSFPt(hist,pt):
    ptBin = hist.GetXaxis().FindBin(pt)
    
    return hist.GetBinContent(ptBin),hist.GetBinError(ptBin)
 
