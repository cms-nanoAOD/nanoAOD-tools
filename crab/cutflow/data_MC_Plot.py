#!/usr/bin/env python
import os,sys
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-l', '--lepton', dest='lepton', type=str, default='el', help="lepton flavor [ el , mu ]")
parser.add_argument('-y', '--year', dest='year', type=str, default='UL2018', help=" UL2017 UL2016preVFP UL2016postVFP UL2018 ")

args = parser.parse_args()
print('--------------------')
print(args)


Lep = args.lepton
year = args.year

import csv
import ROOT
sys.path.insert(1, '/home/mikumar/t3store/workarea/Nanoaod_tools/CMSSW_10_2_28/src/Run2UL_Analysis/stack_plots_before_ML')
from Hist_style import *
data = {}  # A dictionary to store the data

def propagate_rate_uncertainity(hist, uncert):
    for i in range(1,hist.GetXaxis().GetNbins()+1):
        if hist.GetBinContent(i) != 0:
            hist.SetBinError(i, hist.GetBinContent(i) * uncert * 0.01)


with open('cutflow_'+year+'_'+Lep+'.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')  # Use tab as the delimiter
    for row in reader:
        channel = row[0]
        print(channel)
        if(channel in ["Cuts"]):
            cuts = [value.strip() for value in row[2:-2]]
        else:
            #val = [int(value.strip()) for value in row[1:-1]]
            #print val
            try:
                cuts = [int(value.strip()) for value in row[2:-2]]  # Convert values to integers
            except:
                cuts = val = [value.strip() for value in row[2:-2]]
                print("Warning..... can not converted into the numbers : ",cuts)
        data[channel] = cuts

#print(type(data['Tchannel'][0]),data['Tchannel'])

channel_colors = {
    "Tchannel": ROOT.kRed,
    "Tbarchannel": ROOT.kRed,
    "Total": ROOT.kBlack,
    "TWChannel": ROOT.kCyan+1,
    "TbarWChannel": ROOT.kCyan+1,
    "SChannel": ROOT.kCyan+1,
    "TTbar Semi": ROOT.kOrange-1,
    "TTbar Fully": ROOT.kOrange-1,
    "Wp0Jets": ROOT.kGreen+2,
    "Wp1Jets": ROOT.kGreen+2,
    "Wp2Jets": ROOT.kGreen+2,
    "DYJets": ROOT.kBlue,
    "WWTo2L2NU": ROOT.kMagenta,
    "WZTo2L2Q": ROOT.kMagenta,
    "ZZTo2L2Q": ROOT.kMagenta,
    "QCD" :  ROOT.kGray
    
}

# Create a ROOT TCanvas
canvas = ROOT.TCanvas("can", "can", 800, 700)


# Create a TLegend
legend = ROOT.TLegend(0.55, 0.65, 0.87, 0.85)
legend.SetNColumns(3)
legend.SetBorderSize(1)
legend.SetTextSize(0.045)
#legend.SetLabelFont(42)
legend.SetLineColor(0)
legend.SetLineStyle(1)
legend.SetLineWidth(1)
legend.SetFillColor(0)
legend.SetFillStyle(1001)
            
# Create THStack for the stack plot
stack = ROOT.THStack("stack", "")

# Convert the data dictionary into TH1 histograms and add them to the stack
hists = {}
for channel, cuts in data.items():
    #print(channel)
    #print(cuts)
    if(channel in ["Cuts"]): continue
    hists[channel] = ROOT.TH1F(channel, channel, len(cuts), 0, len(cuts))
    for i, cut_value in enumerate(cuts):
        if(isinstance(cut_value,int)):
            hists[channel].SetBinContent(i + 1, cut_value)
            hists[channel].GetXaxis().SetBinLabel(i+1,data['Cuts'][i])
        
    #hist.GetXaxis().SetLabelSize(10.4)
    hists[channel].SetFillColor(channel_colors.get(channel, ROOT.kBlack))
    hists[channel].SetLineColor(channel_colors.get(channel, ROOT.kBlack))

channels =  ['Tchannel','Tbarchannel',"TWChannel","TbarWChannel","SChannel","TTbar Semi","TTbar Fully","Wp0Jets","Wp1Jets","Wp2Jets","DYJets","WWTo2L2NU","WZTo2L2Q","ZZTo2L2Q",'QCD']  

for channel in channels:
        if(channel in ['Tchannel','Tbarchannel']): propagate_rate_uncertainity(hists[channel], 15.0)
        elif(channel in ["TWChannel","TbarWChannel","SChannel","TTbar Semi","TTbar Fully"]): propagate_rate_uncertainity(hists[channel], 6.0)
        elif(channel in ["QCD"]):propagate_rate_uncertainity(hists[channel], 50.0)
        else: propagate_rate_uncertainity(hists[channel], 10.0)
        try:
            hMC.Add(hists[channel])
        except:
            hMC = hists[channel].Clone()
        #if(channel in ['Tbarchannel']):#,"TWChannel","TbarWChannel","SChannel","TTbar Semi","TTbar Fully",]):
        stack.Add(hists[channel])


#print(data['data'])

hMC.SetLineColor(ROOT.kGray+3)
hMC.SetFillColor(ROOT.kGray+3)
#hMC.SetFillStyle(3018)
hMC.SetMarkerColor(ROOT.kRed+3)
hMC.SetMarkerStyle(34)


pad1 = ROOT.TPad("pad1", "pad1", 0.0,0.2831916,1.0,0.97)
pad1.SetBottomMargin(0.11)
pad1.SetTopMargin(0.12)
pad1.SetLeftMargin(0.11)
pad1.SetBottomMargin(0.015)
pad1.SetTicky()
pad1.SetTickx()
pad1.SetLogy()
pad1.Draw()
pad1.cd()

# Draw the stack plot
stack.SetMinimum(1e4)
stack.SetMaximum(1e12)
stack.Draw("hist")
stack.GetXaxis().SetTitle("Cuts")
stack.GetXaxis().SetTitleSize(0.05)
stack.GetYaxis().SetLabelSize(0.06)
stack.GetYaxis().SetLabelFont(42)
stack.GetYaxis().SetTitle("Yields     ")
stack.GetYaxis().SetTitleOffset(1.2)
stack.GetYaxis().SetTitleSize(0.05)
stack.GetXaxis().SetLabelSize(0.05)



# Compare with the "data" channel (assuming you have "data" as one of the channels)
data_hist = ROOT.TH1F("data", "data", len(data["data"]), 0, len(data["data"]))
for i, cut_value in enumerate(data["data"]):
    data_hist.SetBinContent(i + 1, cut_value)
data_hist.SetMarkerColor(1)
data_hist.SetMarkerStyle(20)
data_hist.SetLineColor(ROOT.kBlack)

#for i in range(1,len(cuts)):
   #print(hMC.GetBinContent(i),hMC.GetBinError(i))

#hMC.Draw("P;same")
data_hist.Draw("E1;same")
#raw_input()
# Save or display the plot
# Draw the legend
legend.AddEntry(data_hist, "data", "pe1")
legend.AddEntry(hists["Tchannel"], "t-ch.", "f")
legend.AddEntry(hists["TWChannel"], "tw+S-ch.", "f")
legend.AddEntry(hists["TTbar Semi"], "t #bar t", "f")
legend.AddEntry(hists["WWTo2L2NU"], "VV", "f")
legend.AddEntry(hists["Wp0Jets"], "W+Jets", "f")
legend.AddEntry(hists["QCD"], "QCD", "f")
legend.AddEntry(hists["DYJets"], "Z+Jets", "f")
legend.Draw()

CMSpreliminary = getCMSInt_tag(0.30, 0.815, 0.365, 0.855)
CMSpreliminary.Draw("same")
lepjet_tag = leptonjet_tag(Lep,0.24, 0.765, 0.35, 0.795)
lepjet_tag.Draw("same")
yearNlumitag = year_tag(year,0.78,0.92,0.9,0.96)
yearNlumitag.Draw("same")
canvas.Update()

canvas.cd()
pad2 = rt.TPad("pad2", "pad2", 0.0,0.01,1.0,0.290)
pad2.SetTopMargin(0.0)
pad2.SetBottomMargin(0.3)
pad2.SetLeftMargin(0.11)
pad2.SetGridy()
pad2.SetTicky()
pad2.SetTickx()
pad2.Draw()
pad2.cd()


Ratio_hist = rt.TGraphAsymmErrors(data_hist, hMC, "pois")
axis = Ratio_hist.GetXaxis()
axis.SetLimits(hists["Tchannel"].GetXaxis().GetXmin(), hists["Tchannel"].GetXaxis().GetXmax())
Ratio_hist.SetMarkerColor(1)
Ratio_hist.SetMarkerStyle(20)
Ratio_hist.SetMarkerSize(0.89)
Ratio_hist.SetLineColor(rt.kBlack)



band = None
nBin = None
lEdge = None
uEdge = None
err = None
dummyData = None
dummyData = data_hist.Clone()
dummyData.Divide(hMC)
nBin = dummyData.GetXaxis().GetNbins()
lEdge = dummyData.GetXaxis().GetXmin()
uEdge = dummyData.GetXaxis().GetXmax()
bandTitle = "Band_data_MC ratio"

band = rt.TH1F(bandTitle, "", nBin, lEdge, uEdge)
rt.gStyle.SetOptStat(0)



for nn in range(nBin):
    band.SetBinContent(nn + 1, 1.0)

    if hMC.GetBinContent(nn + 1) != 0 and data_hist.GetBinContent(nn + 1) != 0:
        err = (hMC.GetBinError(nn + 1)) * (dummyData.GetBinContent(nn + 1)) / hMC.GetBinContent(nn + 1)
    else:
        if data_hist.GetBinContent(nn + 1) == 0 and hMC.GetBinContent(nn + 1) != 0:
            err = (hMC.GetBinError(nn + 1)) / hMC.GetBinContent(nn + 1)
        else:
            err = 0.0
    band.SetBinError(nn + 1, err)

band.SetFillColor(rt.kGray + 3)
band.SetFillStyle(3354)
band.GetYaxis().SetTitle("#frac{Data}{MC}")
band.GetYaxis().CenterTitle(1)
band.GetYaxis().SetTitleOffset(0.4)
band.GetYaxis().SetLabelSize(0.12)
band.GetYaxis().SetLabelFont(42)
#band.GetXaxis().SetTitle(hists["Tchannel"].GetXaxis().GetTitle())
band.GetXaxis().SetLabelSize(0.1)
band.GetXaxis().SetLabelFont(42)
band.GetYaxis().SetTitleSize(0.12)
band.GetXaxis().SetTitleSize(0.12)
band.GetXaxis().SetLabelSize(0.15)
band.GetXaxis().SetTitleOffset(0.4)


for channel, cuts in data.items():
    for i, cut_value in enumerate(cuts):
        if(isinstance(cut_value,int)):
            band.GetXaxis().SetBinLabel(i+1,"   "+data['Cuts'][i])

band.SetMaximum(1.745665)
band.SetMinimum(0.0064544)
c = band.GetYaxis()
c.SetNdivisions(6)
c.SetTickSize(0.01)
d = band.GetXaxis()
d.SetNdivisions(10)
d.SetTickSize(0.03)

band.Draw("E2")
Ratio_hist.Draw("PE1SAME")


canvas.SaveAs("Plots/stack_plot_cutflow_"+year+"_"+Lep+".png")
canvas.SaveAs("Plots/stack_plot_cutflow_"+year+"_"+Lep+".pdf")
