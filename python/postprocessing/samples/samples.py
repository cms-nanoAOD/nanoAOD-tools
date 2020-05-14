import ROOT
#import json_reader as jr
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

################################ TTbar ################################
TT_Mtt700to1000_2016 = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_Mtt700to1000_2016")
TT_Mtt700to1000_2016.sigma = 80.5 #pb
TT_Mtt700to1000_2016.year = 2016
TT_Mtt700to1000_2016.dataset = "/TT_Mtt-700to1000_TuneCUETP8M2T4_13TeV-powheg-pythia8/"+tag_2016+"-v1/NANOAODSIM"
#TT_Mtt700to1000_2016.files = jr.json_reader(path+"/TT_Mtt700to1000_2016.json")

TT_Mtt1000toInf_2016 = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_Mtt1000toInf_2016")
TT_Mtt1000toInf_2016.sigma = 21.3 #pb
TT_Mtt1000toInf_2016.year = 2016
TT_Mtt1000toInf_2016.dataset = "/TT_Mtt-1000toInf_TuneCUETP8M2T4_13TeV-powheg-pythia8/"+tag_2016+"-v1/NANOAODSIM"
#TT_Mtt1000toInf_2016.files = jr.json_reader(path+"/TT_Mtt1000toInf_2016.json")

TT_Mtt_2016 = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_Mtt_2016")
TT_Mtt_2016.year = 2016
TT_Mtt_2016.components = [TT_Mtt700to1000_2016, TT_Mtt1000toInf_2016]

################################ QCD ################################
QCDHT_300to500_2016 = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_300to500_2016")
QCDHT_300to500_2016.sigma = 347700 #pb
QCDHT_300to500_2016.year = 2016
QCDHT_300to500_2016.dataset = "/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/"+tag_2016+"-v1/NANOAODSIM"
QCDHT_500to700_2016 = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_500to700_2016")
QCDHT_500to700_2016.sigma = 32100 #pb
QCDHT_500to700_2016.year = 2016
QCDHT_500to700_2016.dataset = "/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/"+tag_2016+"-v1/NANOAODSIM"
QCDHT_700to1000_2016 = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_700to1000_2016")
QCDHT_700to1000_2016.sigma = 6831 #pb
QCDHT_700to1000_2016.year = 2016
QCDHT_700to1000_2016.dataset = "/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/"+tag_2016+"-v1/NANOAODSIM"
QCDHT_1000to1500_2016 = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_1000to1500_2016")
QCDHT_1000to1500_2016.sigma = 1207 #pb
QCDHT_1000to1500_2016.year = 2016
QCDHT_1000to1500_2016.dataset = "/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/"+tag_2016+"-v1/NANOAODSIM"
QCDHT_1500to2000_2016 = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_1500to2000_2016")
QCDHT_1500to2000_2016.sigma = 119.9 #pb
QCDHT_1500to2000_2016.year = 2016
QCDHT_1500to2000_2016.dataset = "/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/"+tag_2016+"-v1/NANOAODSIM"
QCDHT_2000toInf_2016 = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_2000toInf_2016")
QCDHT_2000toInf_2016.sigma = 25.24 #pb
QCDHT_2000toInf_2016.year = 2016
QCDHT_2000toInf_2016.dataset = "/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/"+tag_2016+"-v1/NANOAODSIM"

QCD_2016 = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_2016")
QCD_2016.year = 2016
QCD_2016.components = [QCDHT_300to500_2016, QCDHT_500to700_2016, QCDHT_700to1000_2016, QCDHT_1000to1500_2016, QCDHT_1500to2000_2016, QCDHT_2000toInf_2016]

################################ WJets ################################
WJetsHT200to400_2016 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT200to400_2016")
WJetsHT200to400_2016.sigma = 359.7 * 1.21 #pb
WJetsHT200to400_2016.year = 2016
WJetsHT200to400_2016.dataset = "/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/"+tag_2016+"-v1/NANOAODSIM"
#WJetsHT200to400_2016.files = jr.json_reader(path+"/WJets_HT200To400_2016.json")

WJetsHT400to600_2016 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT400to600_2016")
WJetsHT400to600_2016.sigma = 48.91 * 1.21 #pb
WJetsHT400to600_2016.year = 2016
WJetsHT400to600_2016.dataset = "/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/"+tag_2016+"-v1/NANOAODSIM"
#WJetsHT400to600_2016.files = jr.json_reader(path+"/WJets_HT400To600_2016.json")

WJetsHT600to800_2016 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT600to800_2016")
WJetsHT600to800_2016.sigma = 12.05 * 1.21 #pb
WJetsHT600to800_2016.year = 2016
WJetsHT600to800_2016.dataset = "/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/"+tag_2016+"-v1/NANOAODSIM"
#WJetsHT600to800_2016.files = jr.json_reader(path+"/WJets_HT600To800_2016.json")

WJetsHT800to1200_2016 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT800to1200_2016")
WJetsHT800to1200_2016.sigma = 5.501 * 1.21 #pb
WJetsHT800to1200_2016.year = 2016
WJetsHT800to1200_2016.dataset = "/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/"+tag_2016+"-v1/NANOAODSIM"
#WJetsHT800to1200_2016.files = jr.json_reader(path+"/WJets_HT800To1200_2016.json")

WJetsHT1200to2500_2016 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT1200to2500_2016")
WJetsHT1200to2500_2016.sigma = 1.329 * 1.21 #pb
WJetsHT1200to2500_2016.year = 2016
WJetsHT1200to2500_2016.dataset = "/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/"+tag_2016+"-v1/NANOAODSIM"
#WJetsHT1200to2500_2016.files = jr.json_reader(path+"/WJets_HT1200To2500_2016.json")

WJetsHT2500toInf_2016 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT2500toInf_2016")
WJetsHT2500toInf_2016.sigma = 0.03216 * 1.2 #pb
WJetsHT2500toInf_2016.year = 2016
WJetsHT2500toInf_2016.dataset = "/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/"+tag_2016+"-v1/NANOAODSIM"
#WJetsHT2500toInf_2016.files = jr.json_reader(path+"/WJets_HT2500ToInf_2016.json")

WJets_2016 = sample(ROOT.kGreen+2, 1, 1001, "W + Jets", "WJets_2016")
WJets_2016.year = 2016
WJets_2016.components = [WJetsHT200to400_2016, WJetsHT400to600_2016, WJetsHT600to800_2016, WJetsHT800to1200_2016, WJetsHT1200to2500_2016, WJetsHT2500toInf_2016]

################################ Single Top ################################
ST_tch_t_2016 = sample(ROOT.kYellow, 1, 1001, "ST t-ch", "ST_tch_t_2016")
ST_tch_t_2016.sigma =  136.02 #pb
ST_tch_t_2016.year = 2016
ST_tch_t_2016.dataset = "/ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/"+tag_2016+"-v1/NANOAODSIM"

ST_tch_tbar_2016 = sample(ROOT.kYellow, 1, 1001, "ST t-ch", "ST_tch_tbar_2016")
ST_tch_tbar_2016.sigma =  80.95 #pb
ST_tch_tbar_2016.year = 2016
ST_tch_tbar_2016.dataset = "/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/"+tag_2016+"-v1/NANOAODSIM"

ST_tW_t_2016 = sample(ROOT.kYellow, 1, 1001, "ST tW", "ST_tW_t_2016")
ST_tW_t_2016.sigma =  71.7/2 #pb
ST_tW_t_2016.year = 2016
ST_tW_t_2016.dataset = "/ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/"+tag_2016+"-v1/NANOAODSIM"

ST_tW_tbar_2016 = sample(ROOT.kYellow, 1, 1001, "ST tW", "ST_tW_tbar_2016")
ST_tW_tbar_2016.sigma = 71.7/2 #pb
ST_tW_tbar_2016.year = 2016
ST_tW_tbar_2016.dataset = "/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/"+tag_2016+"_ext1-v1/NANOAODSIM"

ST_sch_2016 = sample(ROOT.kYellow, 1, 1001, "ST s-ch", "ST_sch_2016")
ST_sch_2016.sigma = 10.32 #pb
ST_sch_2016.year = 2016
ST_sch_2016.dataset = "/ST_s-channel_4f_InclusiveDecays_13TeV-amcatnlo-pythia8/"+tag_2016+"-v1/NANOAODSIM"

ST_2016 = sample(ROOT.kYellow, 1, 1001, "Single top", "ST_2016")
ST_2016.year = 2016
ST_2016.components = [ST_tch_t_2016, ST_tch_tbar_2016, ST_tW_t_2016, ST_tW_tbar_2016, ST_sch_2016]

################################ Signal Sample ################################
WP_M2000W20_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 2TeV(1%) RH", "WP_M2000W20_RH_2016")
WP_M2000W20_RH_2016.sigma = 1
WP_M2000W20_RH_2016.year = 2016
WP_M2000W20_RH_2016.dataset = "/Wprimetotb_M2000W20_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M3000W30_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 3TeV(1%) RH", "WP_M3000W30_RH_2016")
WP_M3000W30_RH_2016.sigma = 1
WP_M3000W30_RH_2016.year = 2016
WP_M3000W30_RH_2016.dataset = "/Wprimetotb_M3000W30_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

'''
WP_M3000W300_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 3TeV(10%) RH", "WP_M3000W300_RH_2016")
WP_M3000W300_RH_2016.sigma = 
WP_M3000W300_RH_2016.year = 2016
WP_M3000W300_RH_2016.dataset = "/Wprimetotb_M3000W300_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M3000W600_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 3TeV(20%) RH", "WP_M3000W600_RH_2016")
WP_M3000W600_RH_2016.sigma = 
WP_M3000W600_RH_2016.year = 2016
WP_M3000W600_RH_2016.dataset = "/Wprimetotb_M3000W600_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"
'''
WP_M4000W40_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 4TeV(1%) RH", "WP_M4000W40_RH_2016")
WP_M4000W40_RH_2016.sigma = 1
WP_M4000W40_RH_2016.year = 2016
WP_M4000W40_RH_2016.dataset = "/Wprimetotb_M4000W40_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M4000W400_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 4TeV(10%) RH", "WP_M4000W400_RH_2016")
WP_M4000W400_RH_2016.sigma = 1
WP_M4000W400_RH_2016.year = 2016
WP_M4000W400_RH_2016.dataset = "/Wprimetotb_M4000W400_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' RH", "WP_RH_2016")
WP_RH_2016.year = 2016
WP_RH_2016.components = [WP_M2000W20_RH_2016, WP_M3000W30_RH_2016, WP_M4000W40_RH_2016, WP_M4000W400_RH_2016]

TT_Mtt700to1000_2017 = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_Mtt700to1000_2017")
TT_Mtt700to1000_2017.sigma = 80.5 #pb
TT_Mtt700to1000_2017.year = 2017
TT_Mtt700to1000_2017.dataset = "/TT_Mtt-700to1000_TuneCP5_13TeV-powheg-pythia8/"+tag_2017+"-v2/NANOAODSIM"
#TT_Mtt700to1000_2017.files = jr.json_reader(path+"/TT_Mtt700to1000_2017.json")

TT_Mtt1000toInf_2017 = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_Mtt1000toInf_2017")
TT_Mtt1000toInf_2017.sigma = 21.3 #pb
TT_Mtt1000toInf_2017.year = 2017
TT_Mtt1000toInf_2017.dataset = "/TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8/"+tag_2017+"-v1/NANOAODSIM"
#TT_Mtt1000toInf_2017.files = jr.json_reader(path+"/TT_Mtt1000toInf_2017.json")

TT_Mtt_2017 = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_Mtt_2017")
TT_Mtt_2017.year = 2017
TT_Mtt_2017.components = [TT_Mtt700to1000_2017, TT_Mtt1000toInf_2017]

WJetsHT200to400_2017 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT200to400_2017")
WJetsHT200to400_2017.sigma = 359.7 * 1.21 #pb
WJetsHT200to400_2017.year = 2017
WJetsHT200to400_2017.dataset = "/WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2017+"-v1/NANOAODSIM"
#WJetsHT200to400_2017.files = jr.json_reader(path+"/WJets_HT200To400_2017.json")

WJetsHT400to600_2017 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT400to600_2017")
WJetsHT400to600_2017.sigma = 48.91 * 1.21 #pb
WJetsHT400to600_2017.year = 2017
WJetsHT400to600_2017.dataset = "/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2017+"-v1/NANOAODSIM"
#WJetsHT400to600_2017.files = jr.json_reader(path+"/WJets_HT400To600_2017.json")

WJetsHT600to800_2017 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT600to800_2017")
WJetsHT600to800_2017.sigma = 12.05 * 1.21 #pb
WJetsHT600to800_2017.year = 2017
WJetsHT600to800_2017.dataset = "/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2017+"-v1/NANOAODSIM"
#WJetsHT600to800_2017.files = jr.json_reader(path+"/WJets_HT600To800_2017.json")

WJetsHT800to1200_2017 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT800to1200_2017")
WJetsHT800to1200_2017.sigma = 5.501 * 1.21 #pb
WJetsHT800to1200_2017.year = 2017
WJetsHT800to1200_2017.dataset = "/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2017+"-v1/NANOAODSIM"
#WJetsHT800to1200_2017.files = jr.json_reader(path+"/WJets_HT800To1200_2017.json")

WJetsHT1200to2500_2017 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT1200to2500_2017")
WJetsHT1200to2500_2017.sigma = 1.329 * 1.21 #pb
WJetsHT1200to2500_2017.year = 2017
WJetsHT1200to2500_2017.dataset = "/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2017+"-v1/NANOAODSIM"
#WJetsHT1200to2500_2017.files = jr.json_reader(path+"/WJets_HT1200To2500_2017.json")

WJetsHT2500toInf_2017 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT2500toInf_2017")
WJetsHT2500toInf_2017.sigma = 0.03216 * 1.2 #pb
WJetsHT2500toInf_2017.year = 2017
WJetsHT2500toInf_2017.dataset = "/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2017+"-v1/NANOAODSIM"
#WJetsHT2500toInf_2017.files = jr.json_reader(path+"/WJets_HT2500ToInf_2017.json")

WJets_2017 = sample(ROOT.kGreen+2, 1, 1001, "W + Jets", "WJets_2017")
WJets_2017.year = 2017
WJets_2017.components = [WJetsHT200to400_2017, WJetsHT400to600_2017, WJetsHT600to800_2017, WJetsHT800to1200_2017, WJetsHT1200to2500_2017, WJetsHT2500toInf_2017]

TT_Mtt700to1000_2018 = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_Mtt700to1000_2018")
TT_Mtt700to1000_2018.sigma = 80.5 #pb
TT_Mtt700to1000_2018.year = 2018
TT_Mtt700to1000_2018.dataset = "/TT_Mtt-700to1000_TuneCP5_13TeV-powheg-pythia8/"+tag_2018+"-v1/NANOAODSIM"
#TT_Mtt700to1000_2018.files = jr.json_reader(path+"/TT_Mtt700to1000_2018.json")

TT_Mtt1000toInf_2018 = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_Mtt1000toInf_2018")
TT_Mtt1000toInf_2018.sigma = 21.3 #pb
TT_Mtt1000toInf_2018.year = 2018
TT_Mtt1000toInf_2018.dataset = "/TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8/"+tag_2018+"-v1/NANOAODSIM"
#TT_Mtt1000toInf_2018.files = jr.json_reader(path+"/TT_Mtt1000toInf_2018.json")

TT_Mtt_2018 = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_Mtt_2018")
TT_Mtt_2018.year = 2018
TT_Mtt_2018.components = [TT_Mtt700to1000_2018, TT_Mtt1000toInf_2018]

WJetsHT200to400_2018 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT200to400_2018")
WJetsHT200to400_2018.sigma = 359.7 * 1.21 #pb
WJetsHT200to400_2018.year = 2018
WJetsHT200to400_2018.dataset = "/WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2018+"-v1/NANOAODSIM"
#WJetsHT200to400_2018.files = jr.json_reader(path+"/WJets_HT200To400_2018.json")

WJetsHT400to600_2018 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT400to600_2018")
WJetsHT400to600_2018.sigma = 48.91 * 1.21 #pb
WJetsHT400to600_2018.year = 2018
WJetsHT400to600_2018.dataset = "/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2018+"-v1/NANOAODSIM"
#WJetsHT400to600_2018.files = jr.json_reader(path+"/WJets_HT400To600_2018.json")

WJetsHT600to800_2018 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT600to800_2018")
WJetsHT600to800_2018.sigma = 12.05 * 1.21 #pb
WJetsHT600to800_2018.year = 2018
WJetsHT600to800_2018.dataset = "/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2018+"-v1/NANOAODSIM"
#WJetsHT600to800_2018.files = jr.json_reader(path+"/WJets_HT600To800_2018.json")

WJetsHT800to1200_2018 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT800to1200_2018")
WJetsHT800to1200_2018.sigma = 5.501 * 1.21 #pb
WJetsHT800to1200_2018.year = 2018
WJetsHT800to1200_2018.dataset = "/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2018+"-v1/NANOAODSIM"
#WJetsHT800to1200_2018.files = jr.json_reader(path+"/WJets_HT800To1200_2018.json")

WJetsHT1200to2500_2018 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT1200to2500_2018")
WJetsHT1200to2500_2018.sigma = 1.329 * 1.21 #pb
WJetsHT1200to2500_2018.year = 2018
WJetsHT1200to2500_2018.dataset = "/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2018+"-v1/NANOAODSIM"
#WJetsHT1200to2500_2018.files = jr.json_reader(path+"/WJets_HT1200To2500_2018.json")

WJetsHT2500toInf_2018 = sample(ROOT.kYellow-7, 1, 1001, "W + Jets", "WJetsHT2500toInf_2018")
WJetsHT2500toInf_2018.sigma = 0.03216 * 1.2 #pb
WJetsHT2500toInf_2018.year = 2018
WJetsHT2500toInf_2018.dataset = "/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2018+"-v1/NANOAODSIM"
#WJetsHT2500toInf_2018.files = jr.json_reader(path+"/WJets_HT2500ToInf_2018.json")

WJets_2018 = sample(ROOT.kGreen+2, 1, 1001, "W + Jets", "WJets_2018")
WJets_2018.year = 2018
WJets_2018.components = [WJetsHT200to400_2018, WJetsHT400to600_2018, WJetsHT600to800_2018, WJetsHT800to1200_2018, WJetsHT1200to2500_2018, WJetsHT2500toInf_2018]

#Data datasets
tag_data = 'Nano25Oct2019'

DataMuB_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataMuB_2016")
DataMuB_2016.runP = 'B'
DataMuB_2016.year = 2016
DataMuB_2016.dataset = '/SingleMuon/Run2016B_ver2-'+tag_data + '_ver2-v1/NANOAOD'
DataMuC_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataMuC_2016")
DataMuC_2016.runP = 'C'
DataMuC_2016.year = 2016
DataMuC_2016.dataset = '/SingleMuon/Run2016C-'+tag_data + '-v1/NANOAOD'
DataMuD_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataMuD_2016")
DataMuD_2016.runP = 'D'
DataMuD_2016.year = 2016
DataMuD_2016.dataset = '/SingleMuon/Run2016D-'+tag_data + '-v1/NANOAOD'
DataMuE_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataMuE_2016")
DataMuE_2016.runP = 'E'
DataMuE_2016.year = 2016
DataMuE_2016.dataset = '/SingleMuon/Run2016E-'+tag_data + '-v1/NANOAOD'
DataMuF_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataMuF_2016")
DataMuF_2016.runP = 'F'
DataMuF_2016.year = 2016
DataMuF_2016.dataset = '/SingleMuon/Run2016F-'+tag_data + '-v1/NANOAOD'
DataMuG_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataMuG_2016")
DataMuG_2016.runP = 'G'
DataMuG_2016.year = 2016
DataMuG_2016.dataset = '/SingleMuon/Run2016G-'+tag_data + '-v1/NANOAOD'
DataMuH_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataMuH_2016")
DataMuH_2016.runP = 'H'
DataMuH_2016.year = 2016
DataMuH_2016.dataset = '/SingleMuon/Run2016H-'+tag_data + '-v1/NANOAOD'
DataMu_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataMu_2016")
DataMu_2016.year = 2016
DataMu_2016.components = [DataMuB_2016, DataMuC_2016, DataMuD_2016, DataMuE_2016, DataMuF_2016, DataMuG_2016, DataMuH_2016]

DataEleB_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataEleB_2016")
DataEleB_2016.runP = 'B'
DataEleB_2016.year = 2016
DataEleB_2016.dataset = '/SingleElectron/Run2016B_ver2-'+tag_data + '_ver2-v1/NANOAOD'
DataEleC_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataEleC_2016")
DataEleC_2016.runP = 'C'
DataEleC_2016.year = 2016
DataEleC_2016.dataset = '/SingleElectron/Run2016C-'+tag_data + '-v1/NANOAOD'
DataEleD_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataEleD_2016")
DataEleD_2016.runP = 'D'
DataEleD_2016.year = 2016
DataEleD_2016.dataset = '/SingleElectron/Run2016D-'+tag_data + '-v1/NANOAOD'
DataEleE_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataEleE_2016")
DataEleE_2016.runP = 'E'
DataEleE_2016.year = 2016
DataEleE_2016.dataset = '/SingleElectron/Run2016E-'+tag_data + '-v1/NANOAOD'
DataEleF_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataEleF_2016")
DataEleF_2016.runP = 'F'
DataEleF_2016.year = 2016
DataEleF_2016.dataset = '/SingleElectron/Run2016F-'+tag_data + '-v1/NANOAOD'
DataEleG_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataEleG_2016")
DataEleG_2016.runP = 'G'
DataEleG_2016.year = 2016
DataEleG_2016.dataset = '/SingleElectron/Run2016G-'+tag_data + '-v1/NANOAOD'
DataEleH_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataEleH_2016")
DataEleH_2016.runP = 'H'
DataEleH_2016.year = 2016
DataEleH_2016.dataset = '/SingleElectron/Run2016H-'+tag_data + '-v1/NANOAOD'
DataEle_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataEle_2016")
DataEle_2016.year = 2016
DataEle_2016.components = [DataEleB_2016, DataEleC_2016, DataEleD_2016, DataEleE_2016, DataEleF_2016, DataEleG_2016, DataEleH_2016]

DataHTB_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataHTB_2016")
DataHTB_2016.runP = 'B'
DataHTB_2016.year = 2016
DataHTB_2016.dataset = '/JetHT/Run2016B_ver2-'+tag_data + '_ver2-v1/NANOAOD'
DataHTC_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataHTC_2016")
DataHTC_2016.runP = 'C'
DataHTC_2016.year = 2016
DataHTC_2016.dataset = '/JetHT/Run2016C-'+tag_data + '-v1/NANOAOD'
DataHTD_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataHTD_2016")
DataHTD_2016.runP = 'D'
DataHTD_2016.year = 2016
DataHTD_2016.dataset = '/JetHT/Run2016D-'+tag_data + '-v1/NANOAOD'
DataHTE_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataHTE_2016")
DataHTE_2016.runP = 'E'
DataHTE_2016.year = 2016
DataHTE_2016.dataset = '/JetHT/Run2016E-'+tag_data + '-v1/NANOAOD'
DataHTF_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataHTF_2016")
DataHTF_2016.runP = 'F'
DataHTF_2016.year = 2016
DataHTF_2016.dataset = '/JetHT/Run2016F-'+tag_data + '-v1/NANOAOD'
DataHTG_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataHTG_2016")
DataHTG_2016.runP = 'G'
DataHTG_2016.year = 2016
DataHTG_2016.dataset = '/JetHT/Run2016G-'+tag_data + '-v1/NANOAOD'
DataHTH_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataHTH_2016")
DataHTH_2016.runP = 'H'
DataHTH_2016.year = 2016
DataHTH_2016.dataset = '/JetHT/Run2016H-'+tag_data + '-v1/NANOAOD'
DataHT_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataHT_2016")
DataHT_2016.year = 2016
DataHT_2016.components = [DataHTB_2016, DataHTC_2016, DataHTD_2016, DataHTE_2016, DataHTF_2016, DataHTG_2016, DataHTH_2016]

DataMuB_2017 = sample(ROOT.kBlack, 1, 1001, "Data", "DataMuB_2017")
DataMuB_2017.runP = 'B'
DataMuB_2017.year = 2017
DataMuB_2017.dataset = '/SingleMuon/Run2017B-'+tag_data + '-v1/NANOAOD'
DataMuC_2017 = sample(ROOT.kBlack, 1, 1001, "Data", "DataMuC_2017")
DataMuC_2017.runP = 'C'
DataMuC_2017.year = 2017
DataMuC_2017.dataset = '/SingleMuon/Run2017C-'+tag_data + '-v1/NANOAOD'
DataMuD_2017 = sample(ROOT.kBlack, 1, 1001, "Data", "DataMuD_2017")
DataMuD_2017.runP = 'D'
DataMuD_2017.year = 2017
DataMuD_2017.dataset = '/SingleMuon/Run2017D-'+tag_data + '-v1/NANOAOD'
DataMuE_2017 = sample(ROOT.kBlack, 1, 1001, "Data", "DataMuE_2017")
DataMuE_2017.runP = 'E'
DataMuE_2017.year = 2017
DataMuE_2017.dataset = '/SingleMuon/Run2017E-'+tag_data + '-v1/NANOAOD'
DataMuF_2017 = sample(ROOT.kBlack, 1, 1001, "Data", "DataMuF_2017")
DataMuF_2017.runP = 'F'
DataMuF_2017.year = 2017
DataMuF_2017.dataset = '/SingleMuon/Run2017F-'+tag_data + '-v1/NANOAOD'
DataMu_2017 = sample(ROOT.kBlack, 1, 1001, "Data", "DataMu_2017")
DataMu_2017.year = 2017
DataMu_2017.components = [DataMuB_2017, DataMuC_2017, DataMuD_2017, DataMuE_2017, DataMuF_2017]

DataEleB_2017 = sample(ROOT.kBlack, 1, 1001, "Data", "DataEleB_2017")
DataEleB_2017.runP = 'B'
DataEleB_2017.year = 2017
DataEleB_2017.dataset = '/SingleElectron/Run2017B-'+tag_data + '-v1/NANOAOD'
DataEleC_2017 = sample(ROOT.kBlack, 1, 1001, "Data", "DataEleC_2017")
DataEleC_2017.runP = 'C'
DataEleC_2017.year = 2017
DataEleC_2017.dataset = '/SingleElectron/Run2017C-'+tag_data + '-v1/NANOAOD'
DataEleD_2017 = sample(ROOT.kBlack, 1, 1001, "Data", "DataEleD_2017")
DataEleD_2017.runP = 'D'
DataEleD_2017.year = 2017
DataEleD_2017.dataset = '/SingleElectron/Run2017D-'+tag_data + '-v1/NANOAOD'
DataEleE_2017 = sample(ROOT.kBlack, 1, 1001, "Data", "DataEleE_2017")
DataEleE_2017.runP = 'E'
DataEleE_2017.year = 2017
DataEleE_2017.dataset = '/SingleElectron/Run2017E-'+tag_data + '-v1/NANOAOD'
DataEleF_2017 = sample(ROOT.kBlack, 1, 1001, "Data", "DataEleF_2017")
DataEleF_2017.runP = 'F'
DataEleF_2017.year = 2017
DataEleF_2017.dataset = '/SingleElectron/Run2017F-'+tag_data + '-v1/NANOAOD'
DataEle_2017 = sample(ROOT.kBlack, 1, 1001, "Data", "DataEle_2017")
DataEle_2017.year = 2017
DataEle_2017.components = [DataEleB_2017, DataEleC_2017, DataEleD_2017, DataEleE_2017, DataEleF_2017]

DataHTB_2017 = sample(ROOT.kBlack, 1, 1001, "Data", "DataHTB_2017")
DataHTB_2017.runP = 'B'
DataHTB_2017.year = 2017
DataHTB_2017.dataset = '/JetHT/Run2017B-'+tag_data + '-v1/NANOAOD'
DataHTC_2017 = sample(ROOT.kBlack, 1, 1001, "Data", "DataHTC_2017")
DataHTC_2017.runP = 'C'
DataHTC_2017.year = 2017
DataHTC_2017.dataset = '/JetHT/Run2017C-'+tag_data + '-v1/NANOAOD'
DataHTD_2017 = sample(ROOT.kBlack, 1, 1001, "Data", "DataHTD_2017")
DataHTD_2017.runP = 'D'
DataHTD_2017.year = 2017
DataHTD_2017.dataset = '/JetHT/Run2017D-'+tag_data + '-v1/NANOAOD'
DataHTE_2017 = sample(ROOT.kBlack, 1, 1001, "Data", "DataHTE_2017")
DataHTE_2017.runP = 'E'
DataHTE_2017.year = 2017
DataHTE_2017.dataset = '/JetHT/Run2017E-'+tag_data + '-v1/NANOAOD'
DataHTF_2017 = sample(ROOT.kBlack, 1, 1001, "Data", "DataHTF_2017")
DataHTF_2017.runP = 'F'
DataHTF_2017.year = 2017
DataHTF_2017.dataset = '/JetHT/Run2017F-'+tag_data + '-v1/NANOAOD'
DataHT_2017 = sample(ROOT.kBlack, 1, 1001, "Data", "DataHT_2017")
DataHT_2017.year = 2017
DataHT_2017.components = [DataHTB_2017, DataHTC_2017, DataHTD_2017, DataHTE_2017, DataHTF_2017]

DataMuA_2018 = sample(ROOT.kBlack, 1, 1001, "Data", "DataMuA_2018")
DataMuA_2018.runP = 'A'
DataMuA_2018.year = 2018
DataMuA_2018.dataset = '/SingleMuon/Run2018A-'+tag_data + '-v1/NANOAOD'
DataMuB_2018 = sample(ROOT.kBlack, 1, 1001, "Data", "DataMuB_2018")
DataMuB_2018.runP = 'B'
DataMuB_2018.year = 2018
DataMuB_2018.dataset = '/SingleMuon/Run2018C-'+tag_data + '-v1/NANOAOD'
DataMuC_2018 = sample(ROOT.kBlack, 1, 1001, "Data", "DataMuC_2018")
DataMuC_2018.runP = 'C'
DataMuC_2018.year = 2018
DataMuC_2018.dataset = '/SingleMuon/Run2018C-'+tag_data + '-v1/NANOAOD'
DataMuD_2018 = sample(ROOT.kBlack, 1, 1001, "Data", "DataMuD_2018")
DataMuD_2018.runP = 'D'
DataMuD_2018.year = 2018
DataMuD_2018.dataset = '/SingleMuon/Run2018D-'+tag_data + '-v1/NANOAOD'
DataMu_2018 = sample(ROOT.kBlack, 1, 1001, "Data", "DataDataMu_2018")
DataMu_2018.year = 2018
DataMu_2018.components = [DataMuA_2018, DataMuB_2018, DataMuC_2018, DataMuD_2018]

DataEleA_2018 = sample(ROOT.kBlack, 1, 1001, "Data", "DataEleA_2018")
DataEleA_2018.runP = 'A'
DataEleA_2018.year = 2018
DataEleA_2018.dataset = '/SingleElectron/Run2018A-'+tag_data + '-v1/NANOAOD'
DataEleB_2018 = sample(ROOT.kBlack, 1, 1001, "Data", "DataEleB_2018")
DataEleB_2018.runP = 'B'
DataEleB_2018.year = 2018
DataEleB_2018.dataset = '/SingleElectron/Run2018C-'+tag_data + '-v1/NANOAOD'
DataEleC_2018 = sample(ROOT.kBlack, 1, 1001, "Data", "DataEleC_2018")
DataEleC_2018.runP = 'C'
DataEleC_2018.year = 2018
DataEleC_2018.dataset = '/SingleElectron/Run2018C-'+tag_data + '-v1/NANOAOD'
DataEleD_2018 = sample(ROOT.kBlack, 1, 1001, "Data", "DataEleD_2018")
DataEleD_2018.runP = 'D'
DataEleD_2018.year = 2018
DataEleD_2018.dataset = '/SingleElectron/Run2018D-'+tag_data + '-v1/NANOAOD'
DataEle_2018 = sample(ROOT.kBlack, 1, 1001, "Data", "DataEle_2018")
DataEle_2018.year = 2018
DataEle_2018.components = [DataEleA_2018, DataEleB_2018, DataEleC_2018, DataEleD_2018]

DataHTA_2018 = sample(ROOT.kBlack, 1, 1001, "Data", "DataHTA_2018")
DataHTA_2018.runP = 'A'
DataHTA_2018.year = 2018
DataHTA_2018.dataset = '/JetHT/Run2018A-'+tag_data + '-v1/NANOAOD'
DataHTB_2018 = sample(ROOT.kBlack, 1, 1001, "Data", "DataHTB_2018")
DataHTB_2018.runP = 'B'
DataHTB_2018.year = 2018
DataHTB_2018.dataset = '/JetHT/Run2018B-'+tag_data + '-v1/NANOAOD'
DataHTC_2018 = sample(ROOT.kBlack, 1, 1001, "Data", "DataHTC_2018")
DataHTC_2018.runP = 'C'
DataHTC_2018.year = 2018
DataHTC_2018.dataset = '/JetHT/Run2018C-'+tag_data + '-v1/NANOAOD'
DataHTD_2018 = sample(ROOT.kBlack, 1, 1001, "Data", "DataHTD_2018")
DataHTD_2018.runP = 'D'
DataHTD_2018.year = 2018
DataHTD_2018.dataset = '/JetHT/Run2018D-'+tag_data + '-v1/NANOAOD'
DataHT_2018 = sample(ROOT.kBlack, 1, 1001, "Data", "DataHT_2018")
DataHT_2018.year = 2018
DataHT_2018.components = [DataHTA_2018, DataHTB_2018, DataHTC_2018, DataHTD_2018]

sample_dict = {
    'TT_Mtt_2016':TT_Mtt_2016, 'TT_Mtt700to1000_2016':TT_Mtt700to1000_2016, 'TT_Mtt1000toInf_2016':TT_Mtt1000toInf_2016,
    'WJets_2016':WJets_2016, 'WJetsHT200to400_2016':WJetsHT200to400_2016, 'WJetsHT400to600_2016':WJetsHT400to600_2016, 'WJetsHT600to800_2016':WJetsHT600to800_2016, 'WJetsHT800to1200_2016':WJetsHT800to1200_2016, 'WJetsHT1200to2500_2016':WJetsHT1200to2500_2016, 'WJetsHT2500toInf_2016':WJetsHT2500toInf_2016,
    'ST_2016':ST_2016, 'ST_tch_t_2016':ST_tch_t_2016, 'ST_tch_tbar_2016':ST_tch_tbar_2016, 'ST_tW_t_2016':ST_tW_t_2016, 'ST_tW_tbar_2016':ST_tW_tbar_2016, 'ST_sch_2016':ST_sch_2016,
    'QCD_2016':QCD_2016, 'QCDHT_300to500_2016':QCDHT_300to500_2016, 'QCDHT_500to700_2016':QCDHT_500to700_2016, 'QCDHT_700to1000_2016':QCDHT_700to1000_2016, 'QCDHT_1000to1500_2016':QCDHT_1000to1500_2016, 'QCDHT_1500to2000_2016':QCDHT_1500to2000_2016, 'QCDHT_2000toInf_2016':QCDHT_2000toInf_2016,
    'WP_RH_2016':WP_RH_2016, 'WP_M2000W20_RH_2016':WP_M2000W20_RH_2016, 'WP_M3000W30_RH_2016':WP_M3000W30_RH_2016, 'WP_M4000W40_RH_2016':WP_M4000W40_RH_2016, 'WP_M4000W400_RH_2016':WP_M4000W400_RH_2016,
    'DataMu_2016':DataMu_2016, 'DataMuB_2016':DataMuB_2016,  'DataMuC_2016':DataMuC_2016, 'DataMuD_2016':DataMuD_2016, 'DataMuE_2016':DataMuE_2016, 'DataMuF_2016':DataMuF_2016, 'DataMuG_2016':DataMuG_2016, 'DataMuH_2016':DataMuH_2016,
    'DataEle_2016':DataEle_2016, 'DataEleB_2016':DataEleB_2016, 'DataEleC_2016':DataEleC_2016, 'DataEleD_2016':DataEleD_2016, 'DataEleE_2016':DataEleE_2016, 'DataEleF_2016':DataEleF_2016, 'DataEleG_2016':DataEleG_2016, 'DataEleH_2016':DataEleH_2016,
    'DataHT_2016':DataHT_2016, 'DataHTB_2016':DataHTB_2016, 'DataHTC_2016':DataHTC_2016, 'DataHTD_2016':DataHTD_2016, 'DataHTE_2016':DataHTE_2016, 'DataHTF_2016':DataHTF_2016, 'DataHTG_2016':DataHTG_2016, 'DataHTH_2016':DataHTH_2016,
    'TT_Mtt_2017':TT_Mtt_2017, 'TT_Mtt700to1000_2017':TT_Mtt700to1000_2017, 'TT_Mtt1000toInf_2017':TT_Mtt1000toInf_2017,
    'WJets_2017':WJets_2017, 'WJetsHT200to400_2017':WJetsHT200to400_2017, 'WJetsHT400to600_2017':WJetsHT400to600_2017, 'WJetsHT600to800_2017':WJetsHT600to800_2017, 'WJetsHT800to1200_2017':WJetsHT800to1200_2017, 'WJetsHT1200to2500_2017':WJetsHT1200to2500_2017, 'WJetsHT2500toInf_2017':WJetsHT2500toInf_2017,
    'DataMu_2017':DataMu_2017, 'DataMuB_2017':DataMuB_2017, 'DataMuC_2017':DataMuC_2017, 'DataMuD_2017':DataMuD_2017, 'DataMuE_2017':DataMuE_2017, 'DataMuF_2017':DataMuF_2017,
    'DataEle_2017':DataEle_2017, 'DataEleB_2017':DataEleB_2017, 'DataEleC_2017':DataEleC_2017, 'DataEleD_2017':DataEleD_2017, 'DataEleE_2017':DataEleE_2017, 'DataEleF_2017':DataEleF_2017,
    'DataHT_2017':DataHT_2017, 'DataHTB_2017':DataHTB_2017, 'DataHTC_2017':DataHTC_2017, 'DataHTD_2017':DataHTD_2017, 'DataHTE_2017':DataHTE_2017, 'DataHTF_2017':DataHTF_2017,
    'TT_Mtt_2018':TT_Mtt_2018, 'TT_Mtt700to1000_2018':TT_Mtt700to1000_2018, 'TT_Mtt1000toInf_2018':TT_Mtt1000toInf_2018,
    'WJets_2018':WJets_2018, 'WJetsHT200to400_2018':WJetsHT200to400_2018, 'WJetsHT400to600_2018':WJetsHT400to600_2018, 'WJetsHT600to800_2018':WJetsHT600to800_2018, 'WJetsHT800to1200_2018':WJetsHT800to1200_2018, 'WJetsHT1200to2500_2018':WJetsHT1200to2500_2018, 'WJetsHT2500toInf_2018':WJetsHT2500toInf_2018,
    'DataMu_2018':DataMu_2018, 'DataMuA_2018':DataMuA_2018, 'DataMuB_2018':DataMuB_2018, 'DataMuC_2018':DataMuC_2018, 'DataMuD_2018':DataMuD_2018,
    'DataEle_2018':DataEle_2018, 'DataEleA_2018':DataEleA_2018, 'DataEleB_2018':DataEleB_2018, 'DataEleC_2018':DataEleC_2018, 'DataEleD_2018':DataEleD_2018,
    'DataHT_2018':DataHT_2018,'DataHTA_2018':DataHTA_2018,  'DataHTB_2018':DataHTB_2018, 'DataHTC_2018':DataHTC_2018, 'DataHTD_2018':DataHTD_2018,

}
