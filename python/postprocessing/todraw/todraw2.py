import ROOT
import ROOT.TMath as TMath
import math
from array import array
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from PhysicsTools.NanoAODTools.postprocessing.skimtree_utils import *
import copy
from kFactors import *
import optparse
import os

print "tools implemented"

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch()        # don't pop up canvases                                              
ROOT.TH1.SetDefaultSumw2()
ROOT.TGaxis.SetMaxDigits(3)

usage = 'python todraw2.py'
parser = optparse.OptionParser(usage)
parser.add_option('-c', '--crit', dest='crit', type = 'string', default = 'best', help='Default criterion is best')
parser.add_option('-r', '--reg', dest='region', type = 'string', default = 'incl', help='Default region is inclusive')
parser.add_option('-f', '--folder', dest='fold', type = 'string', default = 'v10', help='Default folder is v10')
parser.add_option('--sel', dest='sel', default = False, action='store_true', help='Default do not apply any selection') 
(opt, args) = parser.parse_args()

crit = opt.crit

region = ''

if opt.region == 'incl':
    region = 'inclusive'
elif opt.region == '2b':
    region = 'reco2btag'
elif opt.region == 'topb':
    region = 'recotopbtag'
elif opt.region == 'Wpb':
    region = 'recoWpbtag'
elif opt.region == '0b':
    region = 'reco0btag'

inputpath = "/eos/user/a/apiccine/Wprime/nosynch/" + opt.fold + "/" + region + "/plot/"
outputpath = "/eos/user/a/apiccine/Wprime/nosynch/" + opt.fold + "/" + region + "/comparison/"

lepton = ['electron',
          'muon',
      ]

if not os.path.exists(outputpath):
     os.makedirs(outputpath)

for lep in lepton:
    if not os.path.exists(outputpath + "/" + lep + "/"):
        os.makedirs(outputpath + "/" + lep + "/")

inpfiles = ["TT_Mtt_2016",
            "WJets_2016",  
            #"WJets_2017",  
            "QCD_2016",
            "WP_M2000W20_RH_2016",
            "WP_M3000W30_RH_2016",
            "WP_M4000W40_RH_2016",
            "WP_M4000W400_RH_2016",
]

plotnt = {('recotop_pt', 'Reco Top p_{T} [GeV]'): ["h_jets_best_top_pt",
                                                   "h_jets_chi_top_pt",
                                                   "h_jets_closest_top_pt",
                                                   "h_jets_sublead_top_pt",
                                                   "h_jets_leadingbjet_pt",
                                                   "h_jets_subleadingbjet_pt",
                                                   "h_jets_MC_top_pt",
                                                   "h_jets_GenPart_top_pt",
                  ],
          ('recotop_mass', 'Reco Top mass [GeV]'): ["h_jets_best_top_m",
                                                    "h_jets_chi_top_m",
                                                    "h_jets_closest_top_m",
                                                    "h_jets_sublead_top_m",
                                                    #"h_jets_leadingbjet_pt",
                                                    #"h_jets_subleadingbjet_pt",
                                                    "h_jets_MC_top_m",
                                                    "h_jets_GenPart_top_m",
                  ],
          ('Wpjet_pt', "W' bjet p_{T} [GeV]"): ["h_jets_best_Wpjet_pt",
                                                "h_jets_chi_Wpjet_pt",
                                                "h_jets_closest_Wpjet_pt",
                                                "h_jets_sublead_Wpjet_pt",
                                                "h_jets_leadingbjet_pt",
                                                "h_jets_subleadingbjet_pt",
                                                "h_jets_MC_Wpjet_pt",
                                                "h_jets_GenPart_bottom_pt",
                ],
          ('topjet_pt', "Top jet p_{T} [GeV]"): ["h_jets_best_topjet_pt",
                                                 "h_jets_chi_topjet_pt",
                                                 "h_jets_closest_topjet_pt",
                                                 "h_jets_sublead_topjet_pt",
                                                 "h_jets_leadingbjet_pt",
                                                 "h_jets_subleadingbjet_pt",
                                                 "h_jets_MC_topjet_pt",
                                                 #"h_jets_GenPart_top_pt",
                 ],
}

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

LogSc = True #False #

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
            for pi, key in enumerate(plots):
                if pi < 4:
                    if not crit in key:
                        continue
                
                npd = str(copy.deepcopy(key))
                if opt.sel:
                    npd = npd + "_selection"

                #print npd, inputf.Get(npd)#ROOT.gROOT.FindObject(str(key))
                
                try:
                    plot = copy.deepcopy(ROOT.gROOT.FindObject(str(npd)).Clone())
                    print plot
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
                            if reco == 'leadingbjet' and 'subleadingb' in str(plot.GetName()):
                                continue
                            new_title = copy.deepcopy(reco) + ";" + quant[1] +";Countings"
                            new_name = inpfile + "_" + quant[0] + "_" + reco
                            print new_name, new_title
                            color = recocolor[reco]
                            break

                plot.SetTitle(new_title)
                plot.SetName(new_name)
                plot.SetLineColor(color)   
                plotstodraw.append(copy.deepcopy(plot))

            print plotstodraw
        
            outp = outputpath + str(lep)
        
            if isinstance(plotstodraw[0], ROOT.TH1F):
                print_hist("", outp, plotstodraw, optstack, LogSc, AllPlot, inpfile)
            else:
                print_hist("", outp, plotstodraw, "AP", LogSc, inpfile)

        inputf.Close()
        
