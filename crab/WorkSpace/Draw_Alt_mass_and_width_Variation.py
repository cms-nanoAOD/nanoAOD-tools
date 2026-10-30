import ROOT
import argparse as arg
from Hist_style import *
parser = arg.ArgumentParser(description='inputs discription')
parser.add_argument('-l', '--lepton', dest='lepton', type=str, default=["mu"],nargs=1, help="lepton [ el  mu ]")
parser.add_argument('-y', '--year  ', dest='year', type=str, default=["UL2018"] ,nargs=1, help="Year [ ULpreVFP2016  ULpostVFP2016  UL2017  UL2018 ]")
parser.add_argument('-mass', '--mass ', dest='mass',  action="store_true", help="Enable this feature if alternate mass need to plot")
parser.add_argument('-width', '--width ', dest='width',  action="store_true", help="Enable this feature if alternate mass need to plot")
args = parser.parse_args()


lep = args.lepton[0]
year= args.year[0]
masssample=args.mass
widthsample=args.width
# Open the ROOT file
input_file = ROOT.TFile("Hist_for_workspace/Combine_Input_lntopMass_histograms_"+year+"_"+lep+"_gteq0p7.root", "READ")

# Check if the file is open successfully
if input_file.IsOpen():
    print("File opened successfully")
else:
    print("Error opening the file")
    exit()

# Get the histogram by name
histogram_names_mass = ["1695","1715","1725","1735","1755"]
legend_names_mass = ["m_{t} = 169.5 GeV", "m_{t} = 171.5 GeV", "m_{t} = 172.5 GeV", "m_{t} = 173.5 GeV", "m_{t} = 175.5 GeV"]
colors_mass = [ROOT.kRed, ROOT.kBlue,ROOT.kBlack, ROOT.kGreen, ROOT.kOrange, ]
    
histogram_names_width = ['190','170','150','1725','130','090','075']
legend_names_width = ["#Gamma_{t} = 1.90 GeV", "#Gamma_{t} = 1.70 GeV", "#Gamma_{t} = 1.50 GeV","#Gamma_{t} = 1.31 GeV","#Gamma_{t} = 1.30GeV","#Gamma_{t} = 0.90 GeV","#Gamma_{t} = 0.75 GeV"]
colors_width = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kBlack, ROOT.kOrange, ROOT.kCyan, ROOT.kMagenta ]   
# Create a canvas and pad

canvas = ROOT.TCanvas("canvas", "canvas", 700, 600)
pad = ROOT.TPad("pad", "Pad", 0.1, 0.1, 0.9, 0.9)
pad.Draw()
pad.cd()

# Create a legend
legend = ROOT.TLegend(0.6, 0.6, 0.88, 0.88)
legend.SetLineWidth(0)
if(masssample):
    for i,mass in  enumerate(histogram_names_mass):
        histogram = input_file.Get(lep+"jets/top_sig_"+mass+"_UL18_gt")
        #histogram.Print()
        # Check if the histogram exists
        if histogram:
            print('Histogram '+"top_sig_"+mass+"_UL18_gt"+' found')
        else:
            print('Histogram '+"top_sig_"+mass+"_UL18_gt"+' not found')
            exit()

        # Set the line color to black
        histogram.SetLineColor(colors_mass[i])
        histogram.SetLineWidth(2)

        # Draw the histogram
        if(i==0):
            histogram.GetYaxis().SetTitle('Events')
            histogram.GetXaxis().SetTitle('m_{i}/ (1 GeV)')
            histogram.GetXaxis().SetTitleSize(0.04)
            histogram.GetYaxis().SetTitleOffset(1.35)
            histogram.GetYaxis().SetTitleSize(0.04)
            histogram.SetTitle(" ")
            histogram.Draw("hist")
        else:
            histogram.Draw("hist;same")
        legend.AddEntry(histogram, legend_names_mass[i], "l")

if(widthsample):
    for i,width in  enumerate(histogram_names_width):
        histogram = input_file.Get(lep+"jets/top_sig_"+width+"_UL18_gt")
        #histogram.Print()
        # Check if the histogram exists
        if histogram:
            print('Histogram '+"top_sig_"+width+"_UL18_gt"+' found')
        else:
            print('Histogram '+"top_sig_"+width+"_UL18_gt"+' not found')
            exit()

        # Set the line color to black
        histogram.SetLineColor(colors_width[i])

        # Draw the histogram
        if(i==0):
            histogram.GetYaxis().SetTitle('Events')
            histogram.GetXaxis().SetTitle('m_{i}/ (1 GeV)')
            histogram.GetXaxis().SetTitleSize(0.04)
            histogram.GetYaxis().SetTitleOffset(1.35)
            histogram.GetYaxis().SetTitleSize(0.04)
            histogram.SetTitle(" ")
            histogram.Draw("hist")
            
        else:
            histogram.Draw("hist;same")
        legend.AddEntry(histogram, legend_names_width[i], "l")
        
    
legend.Draw()
cmstag = getCMSpre_tag(x1=0.285, y1=0.86, x2=0.395, y2=0.88)
leptontag = leptonjet_tag(lep="mu",x1=0.33, y1=0.82, x2=0.35, y2=0.84,region="2J1T")
Yeartag = year_tag(dataYear="UL2016preVFP",x1=0.85, y1=0.9, x2=0.9, y2=0.97)
  
cmstag.Draw()    
leptontag.Draw()
Yeartag.Draw()
    
# Show the canvas
canvas.Update()
canvas.Modified()
if(masssample):
    canvas.SaveAs("Plots/Alt_mass_variation_DNNgt0p7.pdf")
    canvas.SaveAs("Plots/Alt_mass_variation_DNNgt0p7.png")
if(widthsample):
    canvas.SaveAs("Plots/Alt_width_variation_DNNgt0p7.pdf")
    canvas.SaveAs("Plots/Alt_width_variation_DNNgt0p7.png")
# Keep the program running
#ROOT.gApplication.Run()

# Close the input file
input_file.Close()
