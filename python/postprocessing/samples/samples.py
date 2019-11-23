import ROOT
import json_reader as jr

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
TT_Mtt700to1000_2016.files = jr.json_reader("TT_Mtt700to1000_2016.json")

TT_Mtt1000toInf_2016 = sample(ROOT.kRed, 1, 1001, "#mathrm{t#bar{t}}", "TT_Mtt1000toInf_2016")
TT_Mtt1000toInf_2016.sigma = 21.3 #pb
TT_Mtt1000toInf_2016 = "/TT_Mtt-1000toInf_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM"
TT_Mtt1000toInf_2016.files = jr.json_reader("TT_Mtt1000toInf_2016.json")

TT_Mtt_2016 = sample(ROOT.kRed, 1, 1001, "#mathrm{t#bar{t}}", "TT_Mtt")
TT_Mtt_2016.components = [TT_Mtt700to1000_2016, TT_Mtt1000toInf_2016]

'''
WJetsHT200to400 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJets")
WJetsHT200to400.sigma = 359.7 * 1.21 #pb
WJetsHT200to400.files = json_reader("")

WJetsHT400to600 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJets")
WJetsHT400to600.sigma = 48.91 * 1.21 #pb
WJetsHT400to600.files = json_reader("")

WJetsHT600to800 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJets")
WJetsHT600to800.sigma = 12.05 * 1.21 #pb
WJetsHT600to800.files = json_reader("")

WJetsHT800to1200 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJets")
WJetsHT800to1200.sigma = 5.501 * 1.21 #pb
WJetsHT800to1200.files = json_reader("")

WJetsHT1200to2500 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJets")
WJetsHT1200to2500.sigma = 1.329 * 1.21 #pb
WJetsHT1200to2500.files = json_reader("")

WJetsHT2500toInf = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJets")
WJetsHT2500toInf.sigma = 0.03216 * 1.2 #pb
WJetsHT2500toInf.files = json_reader("")

WJets = sample(ROOT.kGreen+2, 1, 1001, "W + Jets", "WJets")
WJets.components = [WJetsHT200to400, WJetsHT400to600, WJetsHT600to800, WJetsHT800to1200, WJetsHT1200to2500, WJetsHT2500toInf]
'''
