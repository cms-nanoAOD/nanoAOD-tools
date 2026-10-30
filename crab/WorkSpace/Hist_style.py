import ROOT as rt
import numpy as np

def getregion_tag(region="2J1T",x1=2, y1=0.91, x2=3, y2=205):
        cntrl = rt.TPaveText(x1,y1,x2,y2,"brNDC")
        cntrl.SetFillStyle(0)
        cntrl.SetBorderSize(0)
        cntrl.SetMargin(0)
        cntrl.SetTextFont(42)
        cntrl.SetTextSize(0.035)
        cntrl.SetTextAlign(13)
        cntrl.AddText(region)
        return cntrl

def getCMSpre_tag(x1=0.385, y1=0.86, x2=0.495, y2=0.88):
        cntrl = rt.TPaveText(x1,y1,x2,y2,"brNDC")
        cntrl.SetFillStyle(0)
        cntrl.SetBorderSize(0)
        cntrl.SetMargin(0)
        cntrl.SetTextFont(42)
        cntrl.SetTextSize(0.05)
        cntrl.SetTextAlign(33)
        cntrl.AddText("#bf{CMS} #it{Preliminary}")
        return cntrl

def leptonjet_tag(lep="mu",x1=0.25, y1=0.82, x2=0.28, y2=0.84,region="2J1T"):
        cntrl = rt.TPaveText(x1,y1,x2,y2,"brNDC")
        cntrl.SetFillStyle(0)
        cntrl.SetBorderSize(0)
        cntrl.SetMargin(0)
        cntrl.SetTextFont(42)
        cntrl.SetTextSize(0.05)
        cntrl.SetTextAlign(33)
        if(lep=="mu"):cntrl.AddText("#it{#mu+jets},"+region)
        if(lep=="el"):cntrl.AddText("#it{e+jets},"+region)
        return cntrl

def year_tag(dataYear="UL2016preVFP",x1=0.948, y1=0.8555, x2=0.95, y2=0.84):
        cntrl = rt.TPaveText(x1,y1,x2,y2,"brNDC")
        cntrl.SetFillStyle(0)
        cntrl.SetBorderSize(0)
        cntrl.SetMargin(0)
        cntrl.SetTextFont(42)
        cntrl.SetTextSize(0.035)
        cntrl.SetTextAlign(33)
        if(dataYear=="UL2016preVFP" or dataYear=="ULpreVFP2016"): cntrl.AddText("19.5 fb^{-1} (13 TeV, 2016preVFP)")
        if(dataYear=="UL2016postVFP" or dataYear=="ULpostVFP2016"): cntrl.AddText("16.8 fb^{-1} (13 TeV, 2016postVFP)")
        if(dataYear=="UL2017"): cntrl.AddText("41.5 fb^{-1} (13 TeV, 2017)")
        if(dataYear=="UL2018"): cntrl.AddText("59.2 fb^{-1} (13 TeV, 2018)")
        return cntrl
