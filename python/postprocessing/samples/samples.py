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
    
TT_Mtt700to1000_2016 = sample(ROOT.kRed, 1, 1001, "#mathrm{t#bar{t}}", "TT_Mtt700to1000_2016")
TT_Mtt700to1000_2016.sigma = 80.5 #pb
TT_Mtt700to1000_2016.dataset = "/TT_Mtt-700to1000_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM"
TT_Mtt700to1000_2016.files = jr.json_reader(""+path+"/TT_Mtt700to1000_2016.json")

TT_Mtt1000toInf_2016 = sample(ROOT.kRed, 1, 1001, "#mathrm{t#bar{t}}", "TT_Mtt1000toInf_2016")
TT_Mtt1000toInf_2016.sigma = 21.3 #pb
TT_Mtt1000toInf_2016.dataset = "/TT_Mtt-1000toInf_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM"
TT_Mtt1000toInf_2016.files = jr.json_reader(""+path+"/TT_Mtt1000toInf_2016.json")

TT_Mtt_2016 = sample(ROOT.kRed, 1, 1001, "#mathrm{t#bar{t}}", "TT_Mtt")
TT_Mtt_2016.components = [TT_Mtt700to1000_2016, TT_Mtt1000toInf_2016]

WJetsHT200to400_2016 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJets")
WJetsHT200to400_2016.sigma = 359.7 * 1.21 #pb
WJetsHT200to400_2016.dataset = ""
WJetsHT200to400_2016.files = jr.json_reader(""+path+"/WJets_HT200To400_2016.json")

WJetsHT400to600_2016 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJets")
WJetsHT400to600_2016.sigma = 48.91 * 1.21 #pb
WJetsHT400to600_2016.dataset = ""
WJetsHT400to600_2016.files = jr.json_reader(""+path+"/WJets_HT400To600_2016.json")

WJetsHT600to800_2016 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJets")
WJetsHT600to800_2016.sigma = 12.05 * 1.21 #pb
WJetsHT600to800_2016.dataset = ""
WJetsHT600to800_2016.files = jr.json_reader(""+path+"/WJets_HT600To800_2016.json")

WJetsHT800to1200_2016 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJets")
WJetsHT800to1200_2016.sigma = 5.501 * 1.21 #pb
WJetsHT800to1200_2016.dataset = ""
WJetsHT800to1200_2016.files = jr.json_reader(""+path+"/WJets_HT800To1200_2016.json")

WJetsHT1200to2500_2016 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJets")
WJetsHT1200to2500_2016.sigma = 1.329 * 1.21 #pb
WJetsHT1200to2500_2016.dataset = ""
WJetsHT1200to2500_2016.files = jr.json_reader(""+path+"/WJets_HT1200To2500_2016.json")

WJetsHT2500toInf_2016 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJets")
WJetsHT2500toInf_2016.sigma = 0.03216 * 1.2 #pb
WJetsHT2500toInf_2016.dataset = ""
WJetsHT2500toInf_2016.files = jr.json_reader(""+path+"/WJets_HT2500ToInf_2016.json")

WJets_2016 = sample(ROOT.kGreen+2, 1, 1001, "W + Jets", "WJets")
WJets_2016.components = [WJetsHT200to400_2016, WJetsHT400to600_2016, WJetsHT600to800_2016, WJetsHT800to1200_2016, WJetsHT1200to2500_2016, WJetsHT2500toInf_2016]
