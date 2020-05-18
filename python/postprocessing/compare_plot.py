import os, commands
import optparse
from ROOT import *

filenames = ["Wprime_4000_RH", "TT_Mtt-700to1000", "WJets"]

histos = []
histos.append("h_leadingjet_mu")
histos.append("h_subleadingjet_mu")
histos.append("h_MET_mu")
histos.append("h_muonpt")
histos.append("h_leadingjet_e")
histos.append("h_subleadingjet_e")
histos.append("h_MET_e")
histos.append("h_electronpt")

infile = []
gStyle.SetPalette(1)
gStyle.SetOptStat(0)
gROOT.SetBatch()        # don't pop up canvases

scale = True
rebin = False #True

for fil in filenames:
     infile.append(TFile.Open("./plots/"+fil+".root"))
for hist in histos:
     h_WJ = TH1F()
     h_SIG = TH1F()
     h_TT = TH1F()
     c1 = TCanvas(str(hist),"c1",50,50,700,600)
     leg = TLegend(0.7,0.7,0.9,0.9)
     for inf in infile:
          inf.cd()
          tmp = (inf.Get(hist)).Clone()
          if scale:
               tmp.Scale(1./tmp.Integral())
          if rebin:
               tmp.Rebin(4)
          if("WJets" in inf.GetName()):
               h_WJ = tmp.Clone()
               h_WJ.SetLineColor(kGreen)
          if("TT_Mtt" in inf.GetName()):
               h_TT = tmp.Clone()
               h_TT.SetLineColor(kBlue)
          if("Wprime" in inf.GetName()):
               h_SIG = tmp.Clone()
               h_SIG.SetLineColor(kRed)
               print h_SIG.Integral()
          tmp.Reset("ICES")
     c1.cd()
     maximum = max(h_WJ.GetMaximum(), h_TT.GetMaximum(), h_SIG.GetMaximum())
     h_WJ.SetMaximum(maximum*1.5)
     h_WJ.Draw("HIST")
     leg.AddEntry(h_WJ, "WJets", "l")
     h_TT.Draw("HISTSAME")
     leg.AddEntry(h_TT, "t#bar{t}", "l")
     h_SIG.Draw("HISTSAME")
     leg.AddEntry(h_SIG, "W prime", "l")
     leg.Draw("SAME")
     c1.Update()
     c1.Print("./plots/"+hist+".png")
     #c1.Print(pathout+"/"+lep+"/"+hist+".png")
     #c1.Print(pathout+"/"+lep+"/"+hist+".root")
     c1.Close()
