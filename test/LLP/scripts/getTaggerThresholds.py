import ROOT
import numpy
import random
import math
import os
import re
import json
import uproot

cvscale = 1.0

fontScale = 750./650.

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(0)
ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(1111)
ROOT.gStyle.SetPadTopMargin(0.08)
ROOT.gStyle.SetPadLeftMargin(0.145)
ROOT.gStyle.SetPadRightMargin(0.26)
ROOT.gStyle.SetPadBottomMargin(0.15)
ROOT.gStyle.SetStatFontSize(0.025)

ROOT.gStyle.SetOptFit()
ROOT.gStyle.SetOptStat(0)

# For the canvas:
ROOT.gStyle.SetCanvasBorderMode(0)
ROOT.gStyle.SetCanvasColor(ROOT.kWhite)
ROOT.gStyle.SetCanvasDefH(700) #Height of canvas
ROOT.gStyle.SetCanvasDefW(800) #Width of canvas
ROOT.gStyle.SetCanvasDefX(0)   #POsition on screen
ROOT.gStyle.SetCanvasDefY(0)

# For the Pad:
ROOT.gStyle.SetPadBorderMode(0)
# ROOT.gStyle.SetPadBorderSize(Width_t size = 1)
ROOT.gStyle.SetPadColor(ROOT.kWhite)
#ROOT.gStyle.SetPadGridX(True)
#ROOT.gStyle.SetPadGridY(True)
ROOT.gStyle.SetGridColor(ROOT.kBlack)
ROOT.gStyle.SetGridStyle(2)
ROOT.gStyle.SetGridWidth(1)

# For the frame:

ROOT.gStyle.SetFrameBorderMode(0)
ROOT.gStyle.SetFrameBorderSize(0)
ROOT.gStyle.SetFrameFillColor(0)
ROOT.gStyle.SetFrameFillStyle(0)
ROOT.gStyle.SetFrameLineColor(1)
ROOT.gStyle.SetFrameLineStyle(1)
ROOT.gStyle.SetFrameLineWidth(0)

# For the histo:
# ROOT.gStyle.SetHistFillColor(1)
# ROOT.gStyle.SetHistFillStyle(0)
# ROOT.gStyle.SetLegoInnerR(Float_t rad = 0.5)
# ROOT.gStyle.SetNumberContours(Int_t number = 20)

ROOT.gStyle.SetEndErrorSize(2)
#ROOT.gStyle.SetErrorMarker(20)
ROOT.gStyle.SetErrorX(0.)

ROOT.gStyle.SetMarkerStyle(20)
#ROOT.gStyle.SetMarkerStyle(20)

#For the fit/function:
ROOT.gStyle.SetOptFit(1)
ROOT.gStyle.SetFitFormat("5.4g")
ROOT.gStyle.SetFuncColor(2)
ROOT.gStyle.SetFuncStyle(1)
ROOT.gStyle.SetFuncWidth(1)

#For the date:
ROOT.gStyle.SetOptDate(0)
# ROOT.gStyle.SetDateX(Float_t x = 0.01)
# ROOT.gStyle.SetDateY(Float_t y = 0.01)

# For the statistics box:
ROOT.gStyle.SetOptFile(0)
ROOT.gStyle.SetOptStat(0) # To display the mean and RMS:   SetOptStat("mr")
ROOT.gStyle.SetStatColor(ROOT.kWhite)
ROOT.gStyle.SetStatFont(42)
ROOT.gStyle.SetStatFontSize(0.025)
ROOT.gStyle.SetStatTextColor(1)
ROOT.gStyle.SetStatFormat("6.4g")
ROOT.gStyle.SetStatBorderSize(1)
ROOT.gStyle.SetStatH(0.1)
ROOT.gStyle.SetStatW(0.15)

ROOT.gStyle.SetHatchesSpacing(1)
ROOT.gStyle.SetHatchesLineWidth(2)

# ROOT.gStyle.SetStaROOT.TStyle(Style_t style = 1001)
# ROOT.gStyle.SetStatX(Float_t x = 0)
# ROOT.gStyle.SetStatY(Float_t y = 0)


#ROOT.gROOT.ForceStyle(True)
#end modified

# For the Global title:

ROOT.gStyle.SetOptTitle(0)

# ROOT.gStyle.SetTitleH(0) # Set the height of the title box
# ROOT.gStyle.SetTitleW(0) # Set the width of the title box
#ROOT.gStyle.SetTitleX(0.35) # Set the position of the title box
#ROOT.gStyle.SetTitleY(0.986) # Set the position of the title box
# ROOT.gStyle.SetTitleStyle(Style_t style = 1001)
#ROOT.gStyle.SetTitleBorderSize(0)

# For the axis titles:
ROOT.gStyle.SetTitleColor(1, "XYZ")
ROOT.gStyle.SetTitleFont(43, "XYZ")
ROOT.gStyle.SetTitleSize(31*cvscale*fontScale, "XYZ")
# ROOT.gStyle.SetTitleXSize(Float_t size = 0.02) # Another way to set the size?
# ROOT.gStyle.SetTitleYSize(Float_t size = 0.02)
ROOT.gStyle.SetTitleXOffset(1.2)
#ROOT.gStyle.SetTitleYOffset(1.2)
ROOT.gStyle.SetTitleOffset(1.2, "YZ") # Another way to set the Offset

# For the axis labels:

ROOT.gStyle.SetLabelColor(1, "XYZ")
ROOT.gStyle.SetLabelFont(43, "XYZ")
ROOT.gStyle.SetLabelOffset(0.0077, "XYZ")
ROOT.gStyle.SetLabelSize(28*cvscale*fontScale, "XYZ")
#ROOT.gStyle.SetLabelSize(0.04, "XYZ")

# For the axis:

ROOT.gStyle.SetAxisColor(1, "XYZ")
ROOT.gStyle.SetAxisColor(1, "XYZ")
ROOT.gStyle.SetStripDecimals(True)
ROOT.gStyle.SetTickLength(0.03, "Y")
ROOT.gStyle.SetTickLength(0.05, "X")
ROOT.gStyle.SetNdivisions(1005, "X")
ROOT.gStyle.SetNdivisions(506, "Y")

ROOT.gStyle.SetPadTickX(1)  # To get tick marks on the opposite side of the frame
ROOT.gStyle.SetPadTickY(1)

# Change for log plots:
ROOT.gStyle.SetOptLogx(0)
ROOT.gStyle.SetOptLogy(0)
ROOT.gStyle.SetOptLogz(0)

#ROOT.gStyle.SetPalette(1) #(1,0)

# another top group addition

# Postscript options:
#ROOT.gStyle.SetPaperSize(20., 20.)
#ROOT.gStyle.SetPaperSize(ROOT.TStyle.kA4)
#ROOT.gStyle.SetPaperSize(27., 29.7)
#ROOT.gStyle.SetPaperSize(27., 29.7)
ROOT.gStyle.SetPaperSize(8.5*1.4*cvscale,7.0*1.4*cvscale)
ROOT.TGaxis.SetMaxDigits(3)
ROOT.gStyle.SetLineScalePS(2)

# ROOT.gStyle.SetLineStyleString(Int_t i, const char* text)
# ROOT.gStyle.SetHeaderPS(const char* header)
# ROOT.gStyle.SetTitlePS(const char* pstitle)
#ROOT.gStyle.SetColorModelPS(1)

# ROOT.gStyle.SetBarOffset(Float_t baroff = 0.5)
# ROOT.gStyle.SetBarWidth(Float_t barwidth = 0.5)
# ROOT.gStyle.SetPaintTextFormat(const char* format = "g")
# ROOT.gStyle.SetPalette(Int_t ncolors = 0, Int_t* colors = 0)
# ROOT.gStyle.SetTimeOffset(Double_t toffset)
# ROOT.gStyle.SetHistMinimumZero(kTRUE)

ROOT.gStyle.SetPaintTextFormat("3.0f")

NRGBs = 5
NCont = 8

stops = numpy.array( [0.00, 0.34, 0.61, 0.84, 1.00] )
red  = numpy.array( [0.00, 0.00, 0.87, 1.00, 0.51] )
green = numpy.array( [0.00, 0.81, 1.00, 0.20, 0.00] )
blue = numpy.array( [0.51, 1.00, 0.12, 0.00, 0.00] )

colWheelDark = ROOT.TColor.CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont)

for i in range(NRGBs):
    red[i]=min(1,red[i]*1.1+0.25)
    green[i]=min(1,green[i]*1.1+0.25)
    blue[i]=min(1,blue[i]*1.1+0.25)

colWheel = ROOT.TColor.CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont)
ROOT.gStyle.SetNumberContours(NCont)
ROOT.gRandom.SetSeed(123)

colors=[]
def hex2rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16)/255.0 for i in range(0, lv, lv // 3))

def newColor(red,green,blue):
    newColor.colorindex+=1
    color=ROOT.TColor(newColor.colorindex,red,green,blue)
    colors.append(color)
    return color
    
newColor.colorindex=301

def getDarkerColor(color):
    darkerColor=newColor(color.GetRed()*0.6,color.GetGreen()*0.6,color.GetBlue()*0.6)
    return darkerColor

extensions = {
    "WToLNu_0J_13TeV-amcatnloFXFX-pythia8":"WToLNu_0J_13TeV-amcatnloFXFX-pythia8",
    "WToLNu_0J_13TeV-amcatnloFXFX-pythia8_ext1":"WToLNu_0J_13TeV-amcatnloFXFX-pythia8",
    
    "WToLNu_1J_13TeV-amcatnloFXFX-pythia8":"WToLNu_1J_13TeV-amcatnloFXFX-pythia8",
    "WToLNu_1J_13TeV-amcatnloFXFX-pythia8_ext1":"WToLNu_1J_13TeV-amcatnloFXFX-pythia8",
    "WToLNu_1J_13TeV-amcatnloFXFX-pythia8_ext3":"WToLNu_1J_13TeV-amcatnloFXFX-pythia8",
    
    "WToLNu_2J_13TeV-amcatnloFXFX-pythia8_ext1":"WToLNu_2J_13TeV-amcatnloFXFX-pythia8",
    "WToLNu_2J_13TeV-amcatnloFXFX-pythia8_ext2":"WToLNu_2J_13TeV-amcatnloFXFX-pythia8",
    "WToLNu_2J_13TeV-amcatnloFXFX-pythia8_ext3":"WToLNu_2J_13TeV-amcatnloFXFX-pythia8",
    
    "DYJetsToNuNu_PtZ-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8":"DYJetsToNuNu_PtZ-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
    "DYJetsToNuNu_PtZ-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext1":"DYJetsToNuNu_PtZ-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
    "DYJetsToNuNu_PtZ-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext4":"DYJetsToNuNu_PtZ-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",

    "DYJetsToNuNu_PtZ-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8":"DYJetsToNuNu_PtZ-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
    "DYJetsToNuNu_PtZ-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext1":"DYJetsToNuNu_PtZ-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
    "DYJetsToNuNu_PtZ-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext4":"DYJetsToNuNu_PtZ-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
    
    "DYJetsToNuNu_PtZ-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8":"DYJetsToNuNu_PtZ-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
    "DYJetsToNuNu_PtZ-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext1":"DYJetsToNuNu_PtZ-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",

    "DYJetsToNuNu_PtZ-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8":"DYJetsToNuNu_PtZ-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
    "DYJetsToNuNu_PtZ-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext1":"DYJetsToNuNu_PtZ-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",    

}

xsecs = {

    # Drell-Yan + jets
    # NLO
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#DY_Z
    "DYJetsToLL_M-50_HT-70to100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":169.9*1.23,
    "DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":147.40*1.23,
    "DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":40.99*1.23,
    "DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":5.678*1.23,
    "DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":1.367*1.23,
    "DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":0.6304*1.23,
    "DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":0.1514*1.23,
    "DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":0.003565*1.23,
    
    "DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8":18610,
    "DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8":1921.8*3,
    
    # QCD (multijet)
    # LO
    "QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":27990000.,
    "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":1712000.,
    "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":347700.,
    "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":32100.,
    "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":6831.,
    "QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":1207.,
    "QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":119.9,
    "QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":25.24,
    
    #https://cms-pdmv.cern.ch/mcm/requests?page=-1&dataset_name=QCD_Pt_*to*_TuneCUETP8M1_13TeV_pythia8&member_of_campaign=RunIIFall14GS
    "QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8":140932000,
    "QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8":19204300,
    "QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8":2762530,
    "QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8":471100,
    "QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8":117276,
    "QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8":7823,
    "QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8":648.2,
    "QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8":186.9,
    "QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8":32.293,
    "QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8":9.4183,
    "QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8":0.84265,
    "QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8":0.114943,
    "QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8":0.00682981,
    "QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8":0.000165445,
    
    
    # Single-top
    # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec#Single_top_t_channel_cross_secti
    # NLO
    "ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1": 10.32,
    "ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1": 80.95,
    "ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1": 136.02,
    "ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1": 71.7/2.,
    "ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1": 71.7/2.,
    
    # TTbar
    # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO (mtop=172.5 GeV)
    # missing
    "TT_TuneCUETP8M2T4_13TeV-powheg-pythia8-evtgen": 831.76,
    "TT_TuneCUETP8M2T4_13TeV-powheg-pythia8": 831.76,
    # NLO
    "TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8": 831.76,
    # LO
    "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": 831.76,
    "TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": 2.666535,
    "TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": 1.098082,
    "TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": 0.198748, 
    "TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": 0.002368413,
    "TTJets_SingleLeptFromTbar_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8": 831.76*0.5*(1-3*0.1086)*(3*0.1086)*2,
    "TTJets_SingleLeptFromT_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8": 831.76*0.5*(1-3*0.1086)*(3*0.1086)*2,

    # W->l nu + jets
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns
    # NLO
    "WJetsToLNu_HT-70To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": 1319,#*1.21, 
    "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": 1345,#*1.21, 
    "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": 359.7,#*1.21, 
    "WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": 48.91,#*1.21, 
    "WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": 12.05,#*1.21, 
    "WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": 5.501,#*1.21, 
    "WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": 1.329,#*1.21, 
    "WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": 0.03216,#*1.21, 
    
    "WToLNu_0J_13TeV-amcatnloFXFX-pythia8": 49670.,
    "WToLNu_1J_13TeV-amcatnloFXFX-pythia8": 8264.,
    "WToLNu_2J_13TeV-amcatnloFXFX-pythia8": 3226.,
    
    # Z -> nu nu + jets
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns
    # LO
    "ZJetsToNuNu_HT-100To200_13TeV-madgraph": 280.35*1.23 ,
    "ZJetsToNuNu_HT-200To400_13TeV-madgraph": 77.67*1.23 ,
    "ZJetsToNuNu_HT-400To600_13TeV-madgraph": 10.73*1.23 ,
    "ZJetsToNuNu_HT-600To800_13TeV-madgraph": 2.559*1.23 ,
    "ZJetsToNuNu_HT-800to1200_13TeV-madgraph": 1.1796*1.23 ,
    "ZJetsToNuNu_HT-1200To2500_13TeV-madgraph": 0.28833*1.23 ,
    "ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph": 0.006945*1.23 ,
    
    # Z -> nu nu + jets
    # MCM
    # NLO
    "DYJetsToNuNu_PtZ-50To100_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8": 593.9*3,
    "DYJetsToNuNu_PtZ-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8": 55.03*3,
    "DYJetsToNuNu_PtZ-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8": 2.082*3,
    "DYJetsToNuNu_PtZ-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8": 0.2816*3,
    "DYJetsToNuNu_PtZ-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8": 0.02639*3,
    
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
    # NNLO
    "WW_TuneCUETP8M1_13TeV-pythia8": 118.7,
    
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Diboson
    # NLO
    "WZ_TuneCUETP8M1_13TeV-pythia8": 47.13,
    "ZZ_TuneCUETP8M1_13TeV-pythia8": 16.523,
}


with open('eventyields.json',) as f:
    genweights = json.load(f)
    
def getProcessDict(filePath):
    processDict = {}
    for processFolder in os.listdir(filePath):
        #print "reading ",processFolder,"...",
        processName = processFolder
        if extensions.has_key(processFolder):
            processName = extensions[processFolder]
            
        if not processDict.has_key(processName):
            processDict[processName] = {
                "files":[],
                "weight":"weightnotfound",
                "xsec":0,
                "integral":0
            }
        for f in os.listdir(os.path.join(filePath,processFolder)):
            fullFilePath = os.path.join(filePath,processFolder,f)
            processDict[processName]["files"].append(fullFilePath)

        #print len(processDict[processName]["files"]),
       
        #if xsecs.has_key(processFolder) and genweights.has_key(processFolder):
        if xsecs.has_key(processName):
            #print genweights[processFolder]["sum"],genweights[processFolder]["weighted"]
            processDict[processName]["xsec"] = xsecs[processName]
            processDict[processName]["integral"] += genweights[processFolder]["weighted"]
        #else: 
        #    print 'noxsec'
        
    for processName in sorted(processDict.keys()):
        if processDict[processName]["integral"]>0:
            processDict[processName]["weight"] = processDict[processName]["xsec"]/processDict[processName]["integral"]
        #print processName,len(processDict[processName]["files"]),processDict[processName]["weight"]
    return processDict
    


def createArrayFast(fileName,processDict,processList,preselection,isData=False):
    if os.path.exists(fileName):
        data = numpy.load(fileName)
        selectedEvents = {}
        for k in data.keys():
            selectedEvents[k] = numpy.copy(data[k])
        return selectedEvents


    selectedEvents = {"tagger_da":[],"tagger_noda":[],"weights":[],"ht":[],"mht":[], "njets":[]}

    for backgroundSample in processList:
        print "processing ... ",backgroundSample
        weight = processDict[backgroundSample]['weight']
        for inputFile in processDict[backgroundSample]["files"]:
            f = uproot.open(inputFile,localsource=lambda p: uproot.source.file.FileSource(p,**uproot.FileSource.defaults))
            tree = f['Friends']
            if len(tree['nselectedJets_nominal'])==0:
                continue
            srSelection = selectionSRArray(tree)
            if not srSelection.any():
                continue
            taggerResultsNoDA = []
            taggerResultsDA = []
            keysFound = True
            for ctau in ["0p01","0p1","0","10","100","1000","10000"]:
                taggerResultsPerCtauNoDA = []
                taggerResultsPerCtauDA = []
                for m in range(5):
                    if "llpdnnx_noda_nominal_%s_LLP_min%i"%(ctau,m) in tree.keys():
                        taggerResultsPerCtauNoDA.append(tree["llpdnnx_noda_nominal_%s_LLP_min%i"%(ctau,m)].array()[srSelection])
                    else:
                        print "key ","llpdnnx_noda_nominal_%s_LLP_min%i "%(ctau,m)," not found in file ",inputFile
                        keysFound = False
                    
                    if "llpdnnx_da_nominal_%s_LLP_min%i"%(ctau,m) in tree.keys():
                        taggerResultsPerCtauDA.append(tree["llpdnnx_da_nominal_%s_LLP_min%i"%(ctau,m)].array()[srSelection])
                    else:
                        keysFound = False
                        print "key ","llpdnnx_da_nominal_%s_LLP_min%i "%(ctau,m)," not found in file ",inputFile
                    
                taggerResultsPerCtauNoDA = numpy.stack(taggerResultsPerCtauNoDA,axis=1)
                taggerResultsPerCtauDA = numpy.stack(taggerResultsPerCtauDA,axis=1)
                taggerResultsNoDA.append(taggerResultsPerCtauNoDA)
                taggerResultsDA.append(taggerResultsPerCtauDA)
            taggerResultsNoDA = numpy.stack(taggerResultsNoDA,axis=1)
            taggerResultsDA = numpy.stack(taggerResultsDA,axis=1)

            if not keysFound:
                continue 
            selectedEvents["tagger_noda"].append(taggerResultsNoDA)
            selectedEvents["tagger_da"].append(taggerResultsDA)
                
            selectedEvents["ht"].append(
                tree["nominal_ht"].array()[srSelection]
            )
            selectedEvents["njets"].append(
                tree["nselectedJets_nominal"].array()[srSelection]
            )
            selectedEvents["mht"].append(
                tree["nominal_mht"].array()[srSelection]
            )
            if not isData:
                selectedEvents["weights"].append(
                    tree["genweight"].array()[srSelection]*tree['puweight'].array()[srSelection]*weight
                )
    
    selectedEvents["tagger_noda"] = numpy.nan_to_num(numpy.concatenate(selectedEvents["tagger_noda"],axis=0))
    selectedEvents["tagger_da"] = numpy.nan_to_num(numpy.concatenate(selectedEvents["tagger_da"],axis=0))
    selectedEvents["ht"] = numpy.concatenate(selectedEvents["ht"],axis=0)
    selectedEvents["mht"] = numpy.concatenate(selectedEvents["mht"],axis=0)
    selectedEvents["njets"] = numpy.concatenate(selectedEvents["njets"],axis=0)
    selectedEvents["weights"] = numpy.concatenate(selectedEvents["weights"],axis=0)

    #print selectedEvents["tagger"].shape
    #print selectedEvents["ht"].shape

    numpy.savez(fileName,**selectedEvents)
    
    return selectedEvents

    
        
def getThreholds(array,varIndex,htThres,ht=lambda x:x>-1,mht=lambda x:x>-1,njets=lambda x:x>-1):
    
    njetsSelected = array["njets"]

    def getWpByEv(sel,ntag,nev):
        tagger = array["tagger_noda"][sel,varIndex,ntag]
        weight = 36000.*array["weights"][sel] 
        taggerSortIndices = numpy.argsort(tagger)
        taggerSorted = tagger[taggerSortIndices]
        weightSorted = weight[taggerSortIndices]
        weightSortedCumSum = numpy.cumsum(weightSorted)
        weightSortedCumSum = weightSortedCumSum[-1]-weightSortedCumSum
        
        thresholds = []
        for i in range(len(taggerSorted)):
            if weightSortedCumSum[i]<nev and weightSortedCumSum[i-1]>nev:
                print "[",taggerSorted[i],weightSortedCumSum[i],"]",
                thresholds.append(taggerSorted[i-1])
        print 
        return thresholds[-1]
                
        
    def getEvByWp(sel,ntag,thres):
        tagger = array["tagger_noda"][sel,varIndex,ntag]
        weight = 36000.*array["weights"][sel] 
        weightSelected = weight[tagger>thres]
        weightSum = numpy.sum(weightSelected)
        return weightSum,len(weightSelected)


    nEv = 3.
    print "="*100
    wpM = min([
        getWpByEv((array["ht"]>800.)*(array["njets"]<4.5),1,nEv),
        getWpByEv((array["ht"]>800.)*(array["njets"]<5.5)*(array["njets"]>4.5),1,nEv),
        getWpByEv((array["ht"]>800.)*(array["njets"]>5.5),2,nEv),
        getWpByEv((array["ht"]<800.)*(array["njets"]<4.5),1,nEv),
        getWpByEv((array["ht"]<800.)*(array["njets"]<5.5)*(array["njets"]>4.5),1,nEv),
        getWpByEv((array["ht"]<800.)*(array["njets"]>5.5),2,nEv)
    ])
    print "-"*100
    print "%1.4f"%wpM
    print "-"*100 
    print "%6.1f (%6.1f)  "%(getEvByWp((array["ht"]>800.)*(array["njets"]<4.5),1,wpM)),
    print "%6.1f (%6.1f)  "%(getEvByWp((array["ht"]>800.)*(array["njets"]<5.5)*(array["njets"]>4.5),1,wpM)),
    print "%6.1f (%6.1f)  "%(getEvByWp((array["ht"]>800.)*(array["njets"]>5.5),2,wpM))
    print "%6.1f (%6.1f)  "%(getEvByWp((array["ht"]<800.)*(array["njets"]<4.5),1,wpM)),
    print "%6.1f (%6.1f)  "%(getEvByWp((array["ht"]<800.)*(array["njets"]<5.5)*(array["njets"]>4.5),1,wpM)),
    print "%6.1f (%6.1f)  "%(getEvByWp((array["ht"]<800.)*(array["njets"]>5.5),2,wpM))
    print
    
    
    '''
    wpM = min([
        getWpByEv((array["ht"]>800.)*(array["njets"]<4.5),1,nEv),
        getWpByEv((array["ht"]>800.)*(array["njets"]<5.5)*(array["njets"]>4.5),1,nEv),
        getWpByEv((array["ht"]>800.)*(array["njets"]>5.5),2,nEv),
        getWpByEv((array["ht"]<800.)*(array["njets"]<4.5),1,nEv),
        getWpByEv((array["ht"]<800.)*(array["njets"]<5.5)*(array["njets"]>4.5),1,nEv),
        getWpByEv((array["ht"]<800.)*(array["njets"]>5.5),2,nEv)
    ])
    print "-"*100
    print "%1.4f"%wpM
    print "-"*100 
    print "%6.1f (%6.1f)  "%(getEvByWp((array["ht"]>800.)*(array["njets"]<4.5),1,wpM)),
    print "%6.1f (%6.1f)  "%(getEvByWp((array["ht"]>800.)*(array["njets"]<5.5)*(array["njets"]>4.5),1,wpM)),
    print "%6.1f (%6.1f)  "%(getEvByWp((array["ht"]>800.)*(array["njets"]>5.5),2,wpM))
    print "%6.1f (%6.1f)  "%(getEvByWp((array["ht"]<800.)*(array["njets"]<4.5),1,wpM)),
    print "%6.1f (%6.1f)  "%(getEvByWp((array["ht"]<800.)*(array["njets"]<5.5)*(array["njets"]>4.5),1,wpM)),
    print "%6.1f (%6.1f)  "%(getEvByWp((array["ht"]<800.)*(array["njets"]>5.5),2,wpM))
    print
    '''

    return wpM
    

    
    
        
    
def selectionSR(chain):
    if chain.nselectedJets_nominal<3:
        return False
    if chain.nominal_mht<300:
        return False
    if chain.nominal_mht/chain.nominal_met>1.25:
        return False
    if chain.nominal_minPhi<0.2:
        return False
    return True
    
def selectionSRArray(chain):
    sel = (chain["nselectedJets_nominal"].array()>2.5)\
          *(chain["nvetoFwdJets_nominal"].array()<0.5)\
          *(chain["nominal_mht"].array()>300)\
          *((chain["nominal_mht"].array()/chain["nominal_met"].array())<1.25)\
          *(chain["nominal_minPhi"].array()>0.2)
    return sel

def selectionDimuonCR(chain):
    return (chain["nselectedJets_nominal"].array()>1.5)\
           *(chain["nvetoFwdJets_nominal"].array()<0.5)\
           *(chain["IsoMuTrigger_flag"].array()>0.5)\
           *(chain["nvetoElectrons"].array()>0.5)\
           *(chain["nvetoMuons"].array()>0.5)\
           *(chain["ntightMuons"].array()==2)\
           *(chain["nvetoMuons"].array()>0.5)\
           *(chain["muonsys_mass"].array()>10.)
    
processDictSR = getProcessDict("/vols/cms/mkomm/LLP/NANOX_MC_new_SR")
processDictCR = getProcessDict("/vols/cms/mkomm/LLP/NANOX_MC_new_CR")


mcArraySR = createArrayFast("thresholdDict_SR_new.npz",processDictSR,[
    "DYJetsToNuNu_PtZ-50To100_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
    "DYJetsToNuNu_PtZ-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
    "DYJetsToNuNu_PtZ-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
    "DYJetsToNuNu_PtZ-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
    "DYJetsToNuNu_PtZ-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
    
    "TT_TuneCUETP8M2T4_13TeV-powheg-pythia8",
    
    "ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1",
    "ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1",
    
    "WToLNu_0J_13TeV-amcatnloFXFX-pythia8",
    "WToLNu_1J_13TeV-amcatnloFXFX-pythia8",
    "WToLNu_2J_13TeV-amcatnloFXFX-pythia8",
],preselection=selectionSR)

mcArrayDimuonCR = createArrayFast("thresholdDict_dimuonCR_mc_new.npz",processDictCR,[
    "DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
    "DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
    "TT_TuneCUETP8M2T4_13TeV-powheg-pythia8",
],preselection=selectionDimuonCR)

dataArrayDimuonCR = createArrayFast("thresholdDict_dimuonCR_data_new.npz",processDictCR,[
    "SingleMuon_Run2016B-03Feb2017_ver2-v2",
    "SingleMuon_Run2016C-03Feb2017-v1",
    "SingleMuon_Run2016D-03Feb2017-v1",
    "SingleMuon_Run2016D-03Feb2017-v1",
    "SingleMuon_Run2016E-03Feb2017-v1",
    "SingleMuon_Run2016F-03Feb2017-v1",
    "SingleMuon_Run2016G-03Feb2017-v1",
    "SingleMuon_Run2016H-03Feb2017_ver2-v1",
    "SingleMuon_Run2016H-03Feb2017_ver3-v1"
],preselection=selectionDimuonCR,isData=True)


    
metSymbol = "p#kern[-0.8]{ }#lower[0.3]{#scale[0.7]{T}}#kern[-2.3]{ }#lower[-0.8]{#scale[0.7]{miss}}"
metSymbol_lc = "p#kern[-0.8]{ }#lower[0.3]{#scale[0.7]{T}#kern[-2.3]{ }#lower[-0.8]{#scale[0.7]{miss,#kern[-0.5]{ }#mu-corr.}}}"
minDPhiSymbol = "#Delta#phi#lower[-0.05]{*}#kern[-1.9]{ }#lower[0.3]{#scale[0.7]{min}}"
htSymbol = "H#kern[-0.7]{ }#lower[0.3]{#scale[0.7]{T}}"
mhtSymbol = "H#kern[-0.7]{ }#lower[0.3]{#scale[0.7]{T}}#kern[-2.2]{ }#lower[-0.8]{#scale[0.7]{miss}}"
rSymbol = mhtSymbol+"#lower[0.05]{#scale[1.2]{/}}"+metSymbol
rSymbol_lc = mhtSymbol+"#lower[0.05]{#scale[1.2]{/}}"+metSymbol_lc
mzSymbol = "m#lower[0.3]{#scale[0.7]{#mu#mu}}"

ctauSymbol=[
    ["c#tau#kern[-0.5]{ }=#kern[-0.5]{ }10#kern[-0.5]{ }#mum","0p01"],
    ["c#tau#kern[-0.5]{ }=#kern[-0.5]{ }100#kern[-0.5]{ }#mum","0p1"],
    ["c#tau#kern[-0.5]{ }=#kern[-0.5]{ }1#kern[-0.5]{ }mm","0"],
    ["c#tau#kern[-0.5]{ }=#kern[-0.5]{ }10#kern[-0.5]{ }mm","10"],
    ["c#tau#kern[-0.5]{ }=#kern[-0.5]{ }100#kern[-0.5]{ }mm","100"],
    ["c#tau#kern[-0.5]{ }=#kern[-0.5]{ }1#kern[-0.5]{ }m","1000"],
    ["c#tau#kern[-0.5]{ }=#kern[-0.5]{ }10#kern[-0.5]{ }m","10000"],
]

for varIndex in range(mcArraySR["tagger_noda"].shape[1]):
    print "-"*60.
    print "var",varIndex,ctauSymbol[varIndex][1]
    
    thresholds = getThreholds(mcArraySR,varIndex,htThres)


    
    
    
