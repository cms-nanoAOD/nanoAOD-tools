import ROOT as rt
import numpy as np
from Hist_style import *
 
filedir = "Hist_for_workspace/"


files_to_read_roc = [
                        'Combine_Input_histograms_UL2017_mu.root',
]

colors = [2,3,4,6,7,216]
makerstyle = [87,20,21,22,23,34]
masses = ["1695","1715","1725","1735","1755"]
legend_txt = ["m_{t} 169.5 GeV","m_{t} 171.5 GeV","m_{t} 172.5 GeV","m_{t} 173.5 GeV","m_{t} 175.5 GeV",]

inputfile = rt.TFile(filedir+files_to_read_roc[0],'read')

c1 = rt.TCanvas('c1', '', 800, 800, 800, 800)
c1.cd()

mass_hist_array = []
for i,mass in enumerate(masses):
        print mass
        mass_hist = inputfile.Get("mujets/top_sig_"+mass)
        mass_hist.Print()
        mass_hist.SetLineColor(colors[i])
        mass_hist.SetLineWidth(2)        
        if(i==0): mass_hist.Draw("hist")
        else: mass_hist.Draw("hist;same")
        mass_hist_array.append(mass_hist)


c1.Update()

legend = rt.TLegend(0.10193646, 0.518435, 0.3293552, 0.83026143)
legend.Clear()
#legend.SetNColumns(2)
legend.SetBorderSize(1)
legend.SetTextSize(0.04)
legend.SetLineColor(0)
legend.SetLineStyle(1)
legend.SetLineWidth(1)
legend.SetFillColor(0)
legend.SetFillStyle(1001)

for i,mass in enumerate(masses):
     legend.AddEntry(mass_hist_array[i], legend_txt[i], "l")

legend.Draw("same")
c1.Update()
raw_input()
c1.Print('Plots/Compare_Hist.png')
c1.Print('Plots/Compare_Hist.pdf') 
