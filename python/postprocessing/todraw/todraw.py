import ROOT
import ROOT.TMath as TMath
import math
from array import array
from PhysicsTools.NanoAODTools.postprocessing.tools import *
import copy
from kFactors import *

print "tools implemented"

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch()        # don't pop up canvases                                                                                     
ROOT.TH1.SetDefaultSumw2()
ROOT.TGaxis.SetMaxDigits(3)

inputpath = "/eos/user/a/apiccine/Wprime/nosynch/v7_apc/plot/"
outputpath = "/eos/user/a/apiccine/Wprime/nosynch/v7_apc/comparison/"
inpfiles = ["TT_Mtt_2016",
            "WJets_2016",  
            #"WJets_2017",  
            "QCD_2016",
            "WP_M2000W20_RH_2016",
            "WP_M3000W30_RH_2016",
            "WP_M4000W40_RH_2016",
            "WP_M4000W400_RH_2016",
]

plotnt = {'recotop': ["h_jets_best_top_pt",
                      "h_jets_chi_top_pt",
                      "h_jets_closest_top_pt",
                      "h_jets_sublead_top_pt",
                      "h_jets_leadingbjet_pt",
                      "h_jets_subleadingbjet_pt",
                      "h_jets_MC_top_pt",
                      "h_jets_GenPart_top_pt",
                  ],
          'Wpjet': ["h_jets_best_Wpjet_pt",
                    "h_jets_chi_Wpjet_pt",
                    "h_jets_closest_Wpjet_pt",
                    "h_jets_sublead_Wpjet_pt",
                    "h_jets_leadingbjet_pt",
                    "h_jets_subleadingbjet_pt",
                    "h_jets_MC_Wpjet_pt",
                    "h_jets_GenPart_bottom_pt",
                ],
          'topjet': ["h_jets_best_topjet_pt",
                     "h_jets_chi_topjet_pt",
                     "h_jets_closest_topjet_pt",
                     "h_jets_sublead_topjet_pt",
                     "h_jets_leadingbjet_pt",
                     "h_jets_subleadingbjet_pt",
                     "h_jets_MC_topjet_pt",
                     "h_jets_GenPart_top_pt",
                 ],
}

lepton = ['electron',
          'muon',
      ]

recocolor = {'GenPart': ROOT.kBlack,
             'MC': ROOT.kBlue,
             'closest': ROOT.kGreen+1,
             'chi': ROOT.kViolet-1,
             'sublead': ROOT.kGray,
             'best': ROOT.kRed,
             'leadingbjet': ROOT.kOrange-3,
             'subleadingbjet': ROOT.kGray+2,
}

sigma = {
    "TT_Mtt-700to1000": 80.5,
    "WJets_2016": 0.03216 * kFacQCD["WJetsHT2500toInf"],
    "WJets_2017": 0.03216 * kFacQCD["WJetsHT2500toInf"],
    "Wprimetotb_M2000W20_RH_TuneCP5_13TeV-madgraph-pythia8": 0.11459,
    "Wprimetotb_M3000W300_RH_TuneCP5_13TeV-madgraph-pythia8": 0.010756,
    "Wprimetotb_M4000W400_RH_TuneCP5_13TeV-madgraph-pythia8": 0.001425,
}

lumi = {
    "2016": 35.9,
    "2017": 41.53,
    "2018": 57.3,
}

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


recocatlabels = ["MC",
                 "sublead",
                 "closest",
                 "chi",
                 "best",
                 "GenPart",
]

samplelabels = {"TT_Mtt_2016": "ttbar",
                "WJets_2016": "W+jets",
                "QCD_2016": "QCD",
                "WP_M2000W20_RH_2016": "W'_{RH} m=2TeV w=20GeV",
                "WP_M3000W30_RH_2016": "W'_{RH} m=3TeV w=30GeV",
                "WP_M4000W40_RH_2016": "W'_{RH} m=4TeV w=40GeV",
                "WP_M4000W400_RH_2016": "W'_{RH} m=4TeV w=400GeV",
}

btaggerlabels = {"DeepFlv": "DeepFlv",
                 #"DeepCSV": "DeepCSV"
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

CompPlot = True
isPtCut = False
isMassCut = False
isTopMassCut = False
NoNeg = False
BTagging = False
SampleLabels = False
NoNegLabels = False
IsNegLabels = False
CatLabels = False
PtLabels = False
MassLabels = False
TopMassLabels = False
BTagLabels = False
WPLabels = False
NBTagLabels = False
Together = False #flag to take or not the sample with only pt cut
toScale = 0
Stack = False

for lep in lepton:
    print lep
        
    for inpfile in inpfiles:
        nfile = None
        nfile = inputpath
        nfile = nfile + str(lep) + "/" + inpfile +"_" + str(lep)
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
                            infiles.append(ftoopen)

        if CompPlot:
            ftoopen = nfile + ".root"
            infiles.append(ftoopen)

        for infile in infiles:
            plots = []
            inputf = None
            inputf = ROOT.TFile.Open(infile)

            for quant, plots in plotnt.items():#2tab
                for idx, key in enumerate(plots):
                    if idx > 4:
                        break
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

                    if CompPlot:
                        for reco in recocolor.keys():
                            if reco in str(plot.GetName()):
                                new_title = copy.deepcopy(reco)
                                new_name = str(plot.GetName())

                    plot.SetTitle(new_title)
                    plot.SetName(new_name)


                    if toScale > 0 and not (isinstance(plot, ROOT.TEfficiency) or isinstance(plot, ROOT.TGraphAsymmErrors)):
                        ky = 'DetReco_countings'
                        entries_plot = None
                        entries_plot = copy.deepcopy(ROOT.gROOT.FindObject(str(ky)).Clone())
                        entries = 1./entries_plot.GetBinContent(1)
                        #print entries_plot.GetBinContent(1)
                        if (toScale == 2):
                            print entries
                            for k, value in sigma.items():
                                if k in infile:
                                    entries = entries * value * 1000.
                                    print value, entries
                            if '2017' in infile:
                                entries = entries * lumi['2017']
                                print lumi['2017'], entries
                            elif '2018' in infile:
                                entries = entries * lumi['2018']
                                print lumi['2018'], entries
                            else:
                                entries = entries * lumi['2016']
                                print lumi['2016'], entries
                        plot.Scale(entries)
                        plot.GetYaxis().SetTitle("#varepsilon")
                    
                    plotstodraw.append(copy.deepcopy(plot))

            inputf.Close()

print plotstodraw
'''


if isinstance(plotstodraw[0], ROOT.TH1F):
    if Stack:
        print_hist("", "plots", plotstodraw, "hist", LogSc, Stack)
    else:
        print_hist("", "plots", plotstodraw, "nostack hist", LogSc, Stack)
else:
    print_hist("", "plots", plotstodraw, "AP", LogSc)
'''
