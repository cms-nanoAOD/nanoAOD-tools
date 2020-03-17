import ROOT
import json_reader as jr
import os 

path = os.path.dirname(os.path.abspath(__file__))

class sample:
    def __init__(self, color, style, fill, leglabel, label):
        self.color = color
        self.style = style
        self.fill = fill
        self.leglabel = leglabel
        self.label = label

tag_2016 = 'RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7'
tag_2017 = 'RunIIFall17NanoAODv6-PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7'
tag_2018 = 'RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20'

TT_Mtt700to1000_2016 = sample(ROOT.kRed, 1, 1001, "#mathrm{t#bar{t}}", "TT_Mtt700to1000_2016")
TT_Mtt700to1000_2016.sigma = 80.5 #pb
TT_Mtt700to1000_2016.dataset = "/TT_Mtt-700to1000_TuneCUETP8M2T4_13TeV-powheg-pythia8/"+tag_2016+"-v2/NANOAODSIM"
TT_Mtt700to1000_2016.files = jr.json_reader(""+path+"/TT_Mtt700to1000_2016.json")

TT_Mtt1000toInf_2016 = sample(ROOT.kRed, 1, 1001, "#mathrm{t#bar{t}}", "TT_Mtt1000toInf_2016")
TT_Mtt1000toInf_2016.sigma = 21.3 #pb
TT_Mtt1000toInf_2016.dataset = "/TT_Mtt-1000toInf_TuneCUETP8M2T4_13TeV-powheg-pythia8/"+tag_2016+"-v2/NANOAODSIM"
TT_Mtt1000toInf_2016.files = jr.json_reader(""+path+"/TT_Mtt1000toInf_2016.json")

TT_Mtt_2016 = sample(ROOT.kRed, 1, 1001, "#mathrm{t#bar{t}}", "TT_Mtt_2016")
TT_Mtt_2016.components = [TT_Mtt700to1000_2016, TT_Mtt1000toInf_2016]

WJetsHT200to400_2016 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT200to400_2016")
WJetsHT200to400_2016.sigma = 359.7 * 1.21 #pb
WJetsHT200to400_2016.dataset = "/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/"+tag_2016+"-v1/NANOAODSIM"
WJetsHT200to400_2016.files = jr.json_reader(""+path+"/WJets_HT200To400_2016.json")

WJetsHT400to600_2016 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT400to600_2016")
WJetsHT400to600_2016.sigma = 48.91 * 1.21 #pb
WJetsHT400to600_2016.dataset = "/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/"+tag_2016+"-v1/NANOAODSIM"
WJetsHT400to600_2016.files = jr.json_reader(""+path+"/WJets_HT400To600_2016.json")

WJetsHT600to800_2016 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT600to800_2016")
WJetsHT600to800_2016.sigma = 12.05 * 1.21 #pb
WJetsHT600to800_2016.dataset = "/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/"+tag_2016+"-v1/NANOAODSIM"
WJetsHT600to800_2016.files = jr.json_reader(""+path+"/WJets_HT600To800_2016.json")

WJetsHT800to1200_2016 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT800to1200_2016")
WJetsHT800to1200_2016.sigma = 5.501 * 1.21 #pb
WJetsHT800to1200_2016.dataset = "/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/"+tag_2016+"-v1/NANOAODSIM"
WJetsHT800to1200_2016.files = jr.json_reader(""+path+"/WJets_HT800To1200_2016.json")

WJetsHT1200to2500_2016 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT1200to2500_2016")
WJetsHT1200to2500_2016.sigma = 1.329 * 1.21 #pb
WJetsHT1200to2500_2016.dataset = "/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/"+tag_2016+"-v1/NANOAODSIM"
WJetsHT1200to2500_2016.files = jr.json_reader(""+path+"/WJets_HT1200To2500_2016.json")

WJetsHT2500toInf_2016 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT2500toInf_2016")
WJetsHT2500toInf_2016.sigma = 0.03216 * 1.2 #pb
WJetsHT2500toInf_2016.dataset = "/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/"+tag_2016+"-v1/NANOAODSIM"
WJetsHT2500toInf_2016.files = jr.json_reader(""+path+"/WJets_HT2500ToInf_2016.json")

WJets_2016 = sample(ROOT.kGreen+2, 1, 1001, "W + Jets", "WJets_2016")
WJets_2016.components = [WJetsHT200to400_2016, WJetsHT400to600_2016, WJetsHT600to800_2016, WJetsHT800to1200_2016, WJetsHT1200to2500_2016, WJetsHT2500toInf_2016]

TT_Mtt700to1000_2017 = sample(ROOT.kRed, 1, 1001, "#mathrm{t#bar{t}}", "TT_Mtt700to1000_2017")
TT_Mtt700to1000_2017.sigma = 80.5 #pb
TT_Mtt700to1000_2017.dataset = "/TT_Mtt-700to1000_TuneCP5_13TeV-powheg-pythia8/"+tag_2017+"-v2/NANOAODSIM"
TT_Mtt700to1000_2017.files = jr.json_reader(""+path+"/TT_Mtt700to1000_2017.json")

TT_Mtt1000toInf_2017 = sample(ROOT.kRed, 1, 1001, "#mathrm{t#bar{t}}", "TT_Mtt1000toInf_2017")
TT_Mtt1000toInf_2017.sigma = 21.3 #pb
TT_Mtt1000toInf_2017.dataset = "/TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8/"+tag_2017+"-v1/NANOAODSIM"
TT_Mtt1000toInf_2017.files = jr.json_reader(""+path+"/TT_Mtt1000toInf_2017.json")

TT_Mtt_2017 = sample(ROOT.kRed, 1, 1001, "#mathrm{t#bar{t}}", "TT_Mtt_2017")
TT_Mtt_2017.components = [TT_Mtt700to1000_2017, TT_Mtt1000toInf_2017]

WJetsHT200to400_2017 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT200to400_2017")
WJetsHT200to400_2017.sigma = 359.7 * 1.21 #pb
WJetsHT200to400_2017.dataset = "/WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2017+"-v1/NANOAODSIM"
WJetsHT200to400_2017.files = jr.json_reader(""+path+"/WJets_HT200To400_2017.json")

WJetsHT400to600_2017 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT400to600_2017")
WJetsHT400to600_2017.sigma = 48.91 * 1.21 #pb
WJetsHT400to600_2017.dataset = "/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2017+"-v1/NANOAODSIM"
WJetsHT400to600_2017.files = jr.json_reader(""+path+"/WJets_HT400To600_2017.json")

WJetsHT600to800_2017 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT600to800_2017")
WJetsHT600to800_2017.sigma = 12.05 * 1.21 #pb
WJetsHT600to800_2017.dataset = "/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2017+"-v1/NANOAODSIM"
WJetsHT600to800_2017.files = jr.json_reader(""+path+"/WJets_HT600To800_2017.json")

WJetsHT800to1200_2017 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT800to1200_2017")
WJetsHT800to1200_2017.sigma = 5.501 * 1.21 #pb
WJetsHT800to1200_2017.dataset = "/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2017+"-v1/NANOAODSIM"
WJetsHT800to1200_2017.files = jr.json_reader(""+path+"/WJets_HT800To1200_2017.json")

WJetsHT1200to2500_2017 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT1200to2500_2017")
WJetsHT1200to2500_2017.sigma = 1.329 * 1.21 #pb
WJetsHT1200to2500_2017.dataset = "/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2017+"-v1/NANOAODSIM"
WJetsHT1200to2500_2017.files = jr.json_reader(""+path+"/WJets_HT1200To2500_2017.json")

WJetsHT2500toInf_2017 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT2500toInf_2017")
WJetsHT2500toInf_2017.sigma = 0.03216 * 1.2 #pb
WJetsHT2500toInf_2017.dataset = "/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2017+"-v1/NANOAODSIM"
WJetsHT2500toInf_2017.files = jr.json_reader(""+path+"/WJets_HT2500ToInf_2017.json")

WJets_2017 = sample(ROOT.kGreen+2, 1, 1001, "W + Jets", "WJets_2017")
WJets_2017.components = [WJetsHT200to400_2017, WJetsHT400to600_2017, WJetsHT600to800_2017, WJetsHT800to1200_2017, WJetsHT1200to2500_2017, WJetsHT2500toInf_2017]

TT_Mtt700to1000_2018 = sample(ROOT.kRed, 1, 1001, "#mathrm{t#bar{t}}", "TT_Mtt700to1000_2018")
TT_Mtt700to1000_2018.sigma = 80.5 #pb

TT_Mtt700to1000_2018.dataset = "/TT_Mtt-700to1000_TuneCP5_13TeV-powheg-pythia8/"+tag_2018+"-v1/NANOAODSIM"
TT_Mtt700to1000_2018.files = jr.json_reader(""+path+"/TT_Mtt700to1000_2018.json")

TT_Mtt1000toInf_2018 = sample(ROOT.kRed, 1, 1001, "#mathrm{t#bar{t}}", "TT_Mtt1000toInf_2018")
TT_Mtt1000toInf_2018.sigma = 21.3 #pb
TT_Mtt1000toInf_2018.dataset = "/TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8/"+tag_2018+"-v1/NANOAODSIM"
TT_Mtt1000toInf_2018.files = jr.json_reader(""+path+"/TT_Mtt1000toInf_2018.json")

TT_Mtt_2018 = sample(ROOT.kRed, 1, 1001, "#mathrm{t#bar{t}}", "TT_Mtt_2018")
TT_Mtt_2018.components = [TT_Mtt700to1000_2018, TT_Mtt1000toInf_2018]

WJetsHT200to400_2018 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT200to400_2018")
WJetsHT200to400_2018.sigma = 359.7 * 1.21 #pb
WJetsHT200to400_2018.dataset = "/WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2018+"-v1/NANOAODSIM"
WJetsHT200to400_2018.files = jr.json_reader(""+path+"/WJets_HT200To400_2018.json")

WJetsHT400to600_2018 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT400to600_2018")
WJetsHT400to600_2018.sigma = 48.91 * 1.21 #pb
WJetsHT400to600_2018.dataset = "/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2018+"-v1/NANOAODSIM"
WJetsHT400to600_2018.files = jr.json_reader(""+path+"/WJets_HT400To600_2018.json")

WJetsHT600to800_2018 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT600to800_2018")
WJetsHT600to800_2018.sigma = 12.05 * 1.21 #pb
WJetsHT600to800_2018.dataset = "/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2018+"-v1/NANOAODSIM"
WJetsHT600to800_2018.files = jr.json_reader(""+path+"/WJets_HT600To800_2018.json")

WJetsHT800to1200_2018 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT800to1200_2018")
WJetsHT800to1200_2018.sigma = 5.501 * 1.21 #pb
WJetsHT800to1200_2018.dataset = "/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2018+"-v1/NANOAODSIM"
WJetsHT800to1200_2018.files = jr.json_reader(""+path+"/WJets_HT800To1200_2018.json")

WJetsHT1200to2500_2018 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT1200to2500_2018")
WJetsHT1200to2500_2018.sigma = 1.329 * 1.21 #pb
WJetsHT1200to2500_2018.dataset = "/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2018+"-v1/NANOAODSIM"
WJetsHT1200to2500_2018.files = jr.json_reader(""+path+"/WJets_HT1200To2500_2018.json")

WJetsHT2500toInf_2018 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT2500toInf_2018")
WJetsHT2500toInf_2018.sigma = 0.03216 * 1.2 #pb
WJetsHT2500toInf_2018.dataset = "/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2018+"-v1/NANOAODSIM"
WJetsHT2500toInf_2018.files = jr.json_reader(""+path+"/WJets_HT2500ToInf_2018.json")

WJets_2018 = sample(ROOT.kGreen+2, 1, 1001, "W + Jets", "WJets_2018")
WJets_2018.components = [WJetsHT200to400_2018, WJetsHT400to600_2018, WJetsHT600to800_2018, WJetsHT800to1200_2018, WJetsHT1200to2500_2018, WJetsHT2500toInf_2018]
