import ROOT
import ROOT.TMath as TMath
import math
from array import array
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from PhysicsTools.NanoAODTools.postprocessing.skimtree_utils import *
import copy
from kFactors import *

print "tools implemented"

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch()        # don't pop up canvases                                                                                     
ROOT.TH1.SetDefaultSumw2()
ROOT.TGaxis.SetMaxDigits(3)

inputpath = "/eos/user/a/apiccine/Wprime/nosynch/v8/plot/"
outputpath = "/eos/user/a/apiccine/Wprime/nosynch/v8/comparison/"
inpfiles = ["TT_Mtt_2016",
            "WJets_2016",  
            #"WJets_2017",  
            "QCD_2016",
            "WP_M2000W20_RH_2016",
            "WP_M3000W30_RH_2016",
            "WP_M4000W40_RH_2016",
            "WP_M4000W400_RH_2016",
]

plotnt = {('recotop', 'Reco Top p_{T} [GeV]'): ["h_jets_best_top_pt",
                                                #"h_jets_chi_top_pt",
                                                #"h_jets_closest_top_pt",
                                                #"h_jets_sublead_top_pt",
                                                "h_jets_leadingbjet_pt",
                                                "h_jets_subleadingbjet_pt",
                                                "h_jets_MC_top_pt",
                                                "h_jets_GenPart_top_pt",
                  ],
          ('Wpjet', "W' bjet p_{T} [GeV]"): ["h_jets_best_Wpjet_pt",
                                             #"h_jets_chi_Wpjet_pt",
                                             #"h_jets_closest_Wpjet_pt",
                                             #"h_jets_sublead_Wpjet_pt",
                                             "h_jets_leadingbjet_pt",
                                             "h_jets_subleadingbjet_pt",
                                             "h_jets_MC_Wpjet_pt",
                                             "h_jets_GenPart_bottom_pt",
                ],
          ('topjet', "Top jet p_{T} [GeV]"): ["h_jets_best_topjet_pt",
                                              #"h_jets_chi_topjet_pt",
                                              #"h_jets_closest_topjet_pt",
                                              #"h_jets_sublead_topjet_pt",
                                              "h_jets_leadingbjet_pt",
                                              "h_jets_subleadingbjet_pt",
                                              "h_jets_MC_topjet_pt",
                                              "h_jets_GenPart_top_pt",
                 ],
}

lepton = ['electron',
          #'muon',
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

samplelabels = {"TT_Mtt_2016": "ttbar",
                "WJets_2016": "W+jets",
                "QCD_2016": "QCD",
                "WP_M2000W20_RH_2016": "W'_{RH} m=2TeV w=20GeV",
                "WP_M3000W30_RH_2016": "W'_{RH} m=3TeV w=30GeV",
                "WP_M4000W40_RH_2016": "W'_{RH} m=4TeV w=40GeV",
                "WP_M4000W400_RH_2016": "W'_{RH} m=4TeV w=400GeV",
}

LogSc = False #True #

CompPlot = True
SampleLabels = False
toScale = 0
AllPlot = True
Stack = False

optstack = "hist"

if not Stack:
    optstack = optstack + " nostack"


for lep in lepton:
        
    for inpfile in inpfiles:
        nfile = None
        nfile = inputpath
        nfile = nfile + str(lep) + "/" + inpfile +"_" + str(lep)

        infile = nfile + ".root"
        
        plots = []
        inputf = None
        inputf = ROOT.TFile.Open(infile)

        for quant, plots in plotnt.items():#2tab

            plotstodraw = []
            for key in plots:
                try:
                    plot = copy.deepcopy(ROOT.gROOT.FindObject(str(key)).Clone())
                except:
                    continue
                new_title = ""
                new_name = ""
                color = None

                if SampleLabels:
                    for label, string in samplelabels.items():
                        if label in infile:
                            new_title = new_title + string
                            new_name = new_name + label

                if CompPlot:
                    for reco in recocolor.keys():
                        if reco in str(plot.GetName()):
                            new_title = copy.deepcopy(reco) + ";" + quant[1] +";Countings"
                            new_name = inpfile + "_" + quant[0] + "_" + reco
                            print new_name, new_title
                            color = recocolor[reco]

                plot.SetTitle(new_title)
                plot.SetName(new_name)
                plot.SetLineColor(color)   
                plotstodraw.append(copy.deepcopy(plot))

            print plotstodraw
        
            outp = outputpath + str(lep)
        
            if isinstance(plotstodraw[0], ROOT.TH1F):
                print_hist("", outp, plotstodraw, optstack, LogSc, AllPlot)
            else:
                print_hist("", outp, plotstodraw, "AP", LogSc)

        inputf.Close()
