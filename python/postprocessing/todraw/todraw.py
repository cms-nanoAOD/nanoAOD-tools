import ROOT
import ROOT.TMath as TMath
import math
from array import array
from PhysicsTools.NanoAODTools.postprocessing.tools import *
import copy

print "Agostino's tools implemented"

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch()        # don't pop up canvases                                                                                     
ROOT.TH1.SetDefaultSumw2()
ROOT.TGaxis.SetMaxDigits(3)

inputpath = "./"

inpfiles = ["TT_Mtt-700to1000",
            "WJets_2016",  
            "WJets_2017",  
            #"QCD_Pt_600to800_1",
            #"SingleMuon_Run2016G_1",
            "Wprimetotb_M2000W20_RH_TuneCP5_13TeV-madgraph-pythia8",
            "Wprimetotb_M3000W300_RH_TuneCP5_13TeV-madgraph-pythia8",
            "Wprimetotb_M4000W400_RH_TuneCP5_13TeV-madgraph-pythia8"
]

ptcuts = [#"250",
          "350"
]

noneg = {'noneg': 'without #Delta < 0 sol.'
}
isneg = {'IsNeg': 'only #Delta < 0 sol.'
}

ptlabels = {'250': 'pt > 250 GeV',
            '350': 'pt > 350 GeV'
}

masscuts = {'Wprimetotb_M4000W400_RH_TuneCP5_13TeV-madgraph-pythia8': "5200",
            'Wprimetotb_M3000W300_RH_TuneCP5_13TeV-madgraph-pythia8': "3900",
            'Wprimetotb_M2000W20_RH_TuneCP5_13TeV-madgraph-pythia8': "2060",
            'TT_Mtt-700to1000': "1200",
}

topmasscuts = {#'400': 'm_{top} < 400 GeV',
               '500': 'm_{top} < 500 GeV',
}

masslabels = {'Wprimetotb_M4000W400_RH_TuneCP5_13TeV-madgraph-pythia8': "m(W') > 5.2 TeV",
              'Wprimetotb_M3000W300_RH_TuneCP5_13TeV-madgraph-pythia8': "m(W') > 3.9 TeV",
              'Wprimetotb_M2000W20_RH_TuneCP5_13TeV-madgraph-pythia8': "m(W') > 2.06 TeV",
              'TT_Mtt-700to1000': "m(W') > 1.2 TeV"
}

plotstodraw = []

plotnt = [#"MC_recotop_Wprime_massesratio",
          #"DetReco_sublead_recotop_Wprime_massesratio",
          #"DetReco_closest_recotop_Wprime_massesratio",
          #"DetReco_chimass_recotop_Wprime_massesratio",
          #"DetReco_best_recotop_Wprime_massesratio"
          #"DetReco_chi_vs_sublead_pt"
          #"MC_chimass",
          #"DetReco_chimass_chisquare",
          #"MC_closest_deltaR",
          #"DetReco_closest_deltaR",
          #"MC_subleading_pt",
          #"DetReco_sublead_subleading_pt",
          #"sublead_DetReco_Wjet_pt",
          #"closest_DetReco_Wjet_pt",
          #"chimass_DetReco_Wjet_pt",
          #"sublead_sublead_DetReco_recotop_mass",
          #"closest_DetReco_recotop_mass",
          #"chi_DetReco_recotop_mass",
          #"DetReco_efficiencies",
          #"MCEff_sublead_Lep_Wprime_mass": 'TGraphAsymmErrors',
          #"MC_Lep_Wprime_mass",
          #"MC_IsNeg_Lep_Wprime_transverse_mass",
          #"MC_IsNeg_Lep_Wprime_mass",
          #"DetReco_sublead_Lep_Wprime_mass",
          #"DetReco_closest_Lep_Wprime_mass",
          #"DetReco_chimass_Lep_Wprime_mass",
          #"DetReco_best_Lep_Wprime_mass",
          #"DetReco_best_IsNeg_Lep_Wprime_transverse_mass",   
          #"DetReco_BTagEff_best_0Mbtag_Lep_Wprime_mass",
          #"DetReco_BTagEff_best_1Mbtag_Lep_Wprime_mass",
          #"DetReco_BTagEff_best_IsNeg_0Mbtag_Lep_Wprime_transverse_mass",
          #"DetReco_BTagEff_best_IsNeg_1Mbtag_Lep_Wprime_transverse_mass",
          #"DetReco_BTagEff_best_IsNeg_2Mbtag_Lep_Wprime_transverse_mass",
          "DetReco_BTagEff_best_2Mbtag_Lep_Wprime_mass",
          #"DetReco_best_0Mbtag_Lep_Wprime_mass",   
          #"DetReco_best_1Mbtag_Lep_Wprime_mass",   
          #"DetReco_best_2Mbtag_Lep_Wprime_mass",   
          #"DetReco_best_IsNeg_0Mbtag_Lep_Wprime_transverse_mass",   
          #"DetReco_best_IsNeg_1Mbtag_Lep_Wprime_transverse_mass",
          #"DetReco_best_IsNeg_2Mbtag_Lep_Wprime_transverse_mass",
          #"DetReco_btag_efficiencies_best",
          #"DetReco_best_2Mbtag_Lep_Wprime_mass",   
          #"DetReco_best_IsNeg_Lep_Wprime_mass",   
          #"MC_Ele_Wprime_mass",
          #"DetReco_sublead_Ele_Wprime_mass",
          #"DetReco_closest_Ele_Wprime_mass",
          #"DetReco_chimass_Ele_Wprime_mass",
          #"DetReco_best_Ele_Wprime_mass", 
          #"MC_Mu_Wprime_mass",
          #"DetReco_sublead_Mu_Wprime_mass",
          #"DetReco_closest_Mu_Wprime_mass",
          #"DetReco_chimass_Mu_Wprime_mass",
          #"DetReco_best_Mu_Wprime_mass", 
          #"sublead_DetReco_Wjet_pt": 'TH1F',
          #"closest_DetReco_Wjet_pt": 'TH1F',
          #"chimass_DetReco_Wjet_pt": 'TH1F',
]

recocatlabels = ["MC",
                 "sublead",
                 "closest",
                 "chi",
                 "best"
]

samplelabels = {"Wprimetotb_M4000W400_RH": "W'RH m=4TeV w=0.4TeV",
                "Wprimetotb_M3000W300_RH": "W'RH m=3TeV w=0.3TeV",
                "Wprimetotb_M2000W20_RH": "W'RH m=2TeV w=20GeV",
                "TT_Mtt-700to1000": "ttbar 0.7to1.0",
                "WJets_2016": "W+jets (2016)",
                "WJets_2017": "W+jets (2017)"
}

btaggerlabels = {#"DeepFlv": "DeepFlv",
                 "DeepCSV": "DeepCSV"
}

wplabels = {"L": "Loose",
            "M": "Medium",
            "T": "Tight"
}

nbtaglabels = {"noLbtag": "not Lbtagged",
               "_Lbtag": "Lbtagged",
               "noMbtag": "not Mbtagged",
               "_Mbtag": "Mbtagged",
               "noTbtag": "not Tbtagged",
               "_Tbtag": "Tbtagged",
               "0Lbtag": "0 Lbtagged",
               "1Lbtag": "1 Lbtagged",
               "2Lbtag": "2 Lbtagged",
               "0Mbtag": "0 Mbtagged",
               "1Mbtag": "1 Mbtagged",
               "2Mbtag": "2 Mbtagged",
               "0Tbtag": "0 Tbtagged",
               "1Tbtag": "1 Tbtagged",
               "2Tbtag": "2 Tbtagged"
}

LogSc = True

isPtCut = True
isMassCut = False
isTopMassCut = False
NoNeg = False
BTagging = True
SampleLabels = True
NoNegLabels = False
IsNegLabels = False
CatLabels = False
PtLabels = False
MassLabels = False
TopMassLabels = False
BTagLabels = False
WPLabels = False
NBTagLabels = True
Together = False #flag to take or not the sample with only pt cut
toScale = True
Stack = False

for inpfile in inpfiles:
    nfile = None
    nfile = inputpath + inpfile
    infiles = None
    infiles = []
    if isPtCut:
        for key in ptcuts:
            fptcut = nfile + '_lpt' + key
            ftoopen = fptcut + '.root'
            if Together:
                infiles.append(ftoopen)
                print ftoopen
            if NoNeg:
                for key in noneg.keys():
                    ftoopen = fptcut + '_' + key + '.root'
                    infiles.append(ftoopen)
            if isMassCut:
                for key, value in masscuts.items():
                    if key == inpfile:
                        ftoopen = fptcut + '_mw' + value + '.root'
                        infiles.append(ftoopen)
            if isTopMassCut:
                for key, value in topmasscuts.items():
                    ftoopen = fptcut + '_mt' + key + '.root'
                    print ftoopen
                    infiles.append(ftoopen)
            if BTagging:
                for key, value in btaggerlabels.items():
                    ftoopen = fptcut + '_' + value + '.root'
                    print ftoopen
                    infiles.append(ftoopen)

    for infile in infiles:
        plots = []
        inputf = None
        inputf = ROOT.TFile.Open(infile)
        
        for key in plotnt:
            try:
                plot = copy.deepcopy(ROOT.gROOT.FindObject(str(key)).Clone())
            except:
                continue
            new_title = ""
            new_name = ""
        
            if SampleLabels:
                for label, string in samplelabels.items():
                    if label in infile:
                        new_title = new_title + string
                        new_name = new_name + label
            
            if CatLabels:
                for label in recocatlabels:
                    if label in key:
                        if new_title != "":
                            new_title = new_title + " "
                        if new_name != "":
                            new_name = new_name + "_"
                        new_title = new_title + label
                        new_name = new_name + label
            if PtLabels:
                for label, string in ptlabels.items():
                    if ('lpt'+label) in infile:
                        if new_title != "":
                            new_title = new_title + " "
                        if new_name != "":
                            new_name = new_name + "_"
                        new_title = new_title + string
                        new_name = new_name + "pt" + label
            if TopMassLabels:
                for label, string in topmasscuts.items():
                    if ('mt'+label) in infile:
                        if new_title != "":
                            new_title = new_title + " "
                        if new_name != "":
                            new_name = new_name + "_"
                        new_title = new_title + string
                        new_name = new_name + "mt" + label
            
            if MassLabels:
                for label, string in masscuts.items():
                    if ('mw' + string) in infile:
                        if new_title != "":
                            new_title = new_title + " "
                        if new_name != "":
                            new_name = new_name + "_"
                        new_title = new_title + masslabels[label]
                        new_name = new_name + "mw" + string

            if NoNegLabels and not ('IsNeg' in str(plot.GetName())):
                for label, string in noneg.items():
                    if label in infile:
                        if new_title != "":
                            new_title = new_title + " "
                        if new_name != "":
                            new_name = new_name + "_"
                        new_title = new_title + string
                        new_name = new_name + label

            if IsNegLabels:
                for label, string in isneg.items():
                    if label in str(plot.GetName()):
                        if new_title != "":
                            new_title = new_title + " "
                        if new_name != "":
                            new_name = new_name + "_"
                        new_title = new_title + string
                        new_name = new_name + label

            if BTagLabels:
                for label, string in btaggerlabels.items():
                    if label in str(plot.GetName()):
                        if new_title != "":
                            new_title = new_title + " "
                        if new_name != "":
                            new_name = new_name + "_"
                        new_title = new_title + string
                        new_name = new_name + label

            if WPLabels:
                for label, string in wplabels.items():
                    if label in str(plot.GetName()):
                        if new_title != "":
                            new_title = new_title + " "
                        if new_name != "":
                            new_name = new_name + "_"
                        new_title = new_title + string
                        new_name = new_name + label

            if NBTagLabels:
                for label, string in nbtaglabels.items():
                    if label in str(plot.GetName()):
                        if new_title != "":
                            new_title = new_title + " "
                        if new_name != "":
                            new_name = new_name + "_"
                        new_title = new_title + string
                        new_name = new_name + label

            plot.SetTitle(new_title)
            plot.SetName(new_name)
            if toScale and not (isinstance(plot, ROOT.TEfficiency) or isinstance(plot, ROOT.TGraphAsymmErrors)):
                key = 'DetReco_countings'
                entries_plot = None
                entries_plot = copy.deepcopy(ROOT.gROOT.FindObject(str(key)).Clone())
                entries = 1./entries_plot.GetBinContent(1)
                #print entries_plot.GetBinContent(1)
                plot.Scale(entries)
                plot.GetYaxis().SetTitle("#varepsilon")
            plotstodraw.append(copy.deepcopy(plot))

print plotstodraw

if isinstance(plotstodraw[0], ROOT.TH1F):
    if Stack:
        print_hist("", "plots", plotstodraw, "hist", LogSc, Stack)
    else:
        print_hist("", "plots", plotstodraw, "nostack hist", LogSc, Stack)
else:
    print_hist("", "plots", plotstodraw, "AP", LogSc)

