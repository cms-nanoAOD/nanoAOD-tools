import ROOT
import os 
#import json_reader as jr

path = os.path.dirname(os.path.abspath(__file__))

class sample:
    def __init__(self, color, style, fill, leglabel, label):
        self.color = color
        self.style = style
        self.fill = fill
        self.leglabel = leglabel
        self.label = label

tag_2016 = 'RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8'
tag_2017 = 'RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8'
tag2_2017 = 'RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8'
tag_2018 = 'RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21'

###################################################################################################################################################################
############################################################                                           ############################################################
############################################################                    2016                   ############################################################
############################################################                                           ############################################################
###################################################################################################################################################################
################################ TTbar ################################
TT_incl_2016 = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_incl_2016")
TT_incl_2016.sigma = 831.76 #pb
TT_incl_2016.year = 2016
TT_incl_2016.dataset = "/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/"+tag_2016+"-v2/NANOAODSIM"

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
TT_Mtt_2016.components = [TT_incl_2016, TT_Mtt700to1000_2016, TT_Mtt1000toInf_2016]

TT_dilep_2016 = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_dilep_2016")
TT_dilep_2016.sigma = 831.76 #pb
TT_dilep_2016.year = 2016
TT_dilep_2016.dataset = "/TTTo2L2Nu_noSC_TuneCUETP8M2T4_13TeV-powheg-pythia8/"+tag_2016+"-v1/NANOAODSIM"
# /TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM
#/TTTo2L2Nu_noSC_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM
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
WJetsHT70to100_2016 = sample(ROOT.kGreen+2, 1, 1001, "W + Jets", "WJetsHT70to100_2016")
WJetsHT70to100_2016.sigma = 1353.0 * 1.21 #pb
WJetsHT70to100_2016.year = 2016
WJetsHT70to100_2016.dataset = "/WJetsToLNu_HT-70To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/"+tag_2016+"-v1/NANOAODSIM"
WJetsHT100to200_2016 = sample(ROOT.kGreen+2, 1, 1001, "W + Jets", "WJetsHT100to200_2016")
WJetsHT100to200_2016.sigma = 1345 * 1.21 #pb
WJetsHT100to200_2016.year = 2016
WJetsHT100to200_2016.dataset = "/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/"+tag_2016+"-v1/NANOAODSIM"
WJetsHT200to400_2016 = sample(ROOT.kGreen+2, 1, 1001, "W + Jets", "WJetsHT200to400_2016")
WJetsHT200to400_2016.sigma = 359.7 * 1.21 #pb
WJetsHT200to400_2016.year = 2016
WJetsHT200to400_2016.dataset = "/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/"+tag_2016+"-v1/NANOAODSIM"
#WJetsHT200to400_2016.files = jr.json_reader(path+"/WJets_HT200To400_2016.json")
WJetsHT400to600_2016 = sample(ROOT.kGreen+2, 1, 1001, "W + Jets", "WJetsHT400to600_2016")
WJetsHT400to600_2016.sigma = 48.91 * 1.21 #pb
WJetsHT400to600_2016.year = 2016
WJetsHT400to600_2016.dataset = "/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/"+tag_2016+"-v1/NANOAODSIM"
#WJetsHT400to600_2016.files = jr.json_reader(path+"/WJets_HT400To600_2016.json")
WJetsHT600to800_2016 = sample(ROOT.kGreen+2, 1, 1001, "W + Jets", "WJetsHT600to800_2016")
WJetsHT600to800_2016.sigma = 12.05 * 1.21 #pb
WJetsHT600to800_2016.year = 2016
WJetsHT600to800_2016.dataset = "/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/"+tag_2016+"-v1/NANOAODSIM"
#WJetsHT600to800_2016.files = jr.json_reader(path+"/WJets_HT600To800_2016.json")
WJetsHT800to1200_2016 = sample(ROOT.kGreen+2, 1, 1001, "W + Jets", "WJetsHT800to1200_2016")
WJetsHT800to1200_2016.sigma = 5.501 * 1.21 #pb
WJetsHT800to1200_2016.year = 2016
WJetsHT800to1200_2016.dataset = "/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/"+tag_2016+"-v1/NANOAODSIM"
#WJetsHT800to1200_2016.files = jr.json_reader(path+"/WJets_HT800To1200_2016.json")
WJetsHT1200to2500_2016 = sample(ROOT.kGreen+2, 1, 1001, "W + Jets", "WJetsHT1200to2500_2016")
WJetsHT1200to2500_2016.sigma = 1.329 * 1.21 #pb
WJetsHT1200to2500_2016.year = 2016
WJetsHT1200to2500_2016.dataset = "/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/"+tag_2016+"-v1/NANOAODSIM"
#WJetsHT1200to2500_2016.files = jr.json_reader(path+"/WJets_HT1200To2500_2016.json")
WJetsHT2500toInf_2016 = sample(ROOT.kGreen+2, 1, 1001, "W + Jets", "WJetsHT2500toInf_2016")
WJetsHT2500toInf_2016.sigma = 0.03216 * 1.2 #pb
WJetsHT2500toInf_2016.year = 2016
WJetsHT2500toInf_2016.dataset = "/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/"+tag_2016+"-v1/NANOAODSIM"
#WJetsHT2500toInf_2016.files = jr.json_reader(path+"/WJets_HT2500ToInf_2016.json")

WJets_2016 = sample(ROOT.kGreen+2, 1, 1001, "W + Jets", "WJets_2016")
WJets_2016.year = 2016
WJets_2016.components = [WJetsHT70to100_2016, WJetsHT100to200_2016, WJetsHT200to400_2016, WJetsHT400to600_2016, WJetsHT600to800_2016, WJetsHT800to1200_2016, WJetsHT1200to2500_2016, WJetsHT2500toInf_2016]
#WJets_2016.components = [WJetsHT100to200_2016, WJetsHT200to400_2016, WJetsHT400to600_2016, WJetsHT600to800_2016, WJetsHT800to1200_2016, WJetsHT1200to2500_2016, WJetsHT2500toInf_2016]

################################ Single Top ################################
ST_tch_t_2016 = sample(ROOT.kYellow, 1, 1001, "ST t-ch", "ST_tch_t_2016")
ST_tch_t_2016.sigma =  136.02 #pb
ST_tch_t_2016.year = 2016
#ST_tch_t_2016.dataset = "/ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/"+tag_2016+"-v1/NANOAODSIM"
ST_tch_t_2016.dataset = "/ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM"

ST_tch_tbar_2016 = sample(ROOT.kYellow, 1, 1001, "ST t-ch", "ST_tch_tbar_2016")
ST_tch_tbar_2016.sigma =  80.95 #pb
ST_tch_tbar_2016.year = 2016
ST_tch_tbar_2016.dataset = "/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/"+tag_2016+"-v1/NANOAODSIM"

ST_tW_t_2016 = sample(ROOT.kYellow, 1, 1001, "ST tW", "ST_tW_t_2016")
ST_tW_t_2016.sigma =  71.7/2 #pb
ST_tW_t_2016.year = 2016
ST_tW_t_2016.dataset = "/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/"+tag_2016+"_ext1-v1/NANOAODSIM"

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

################################ Signal Sample LH w/o SM Interference ################################
WP_M2000W200_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 2.0TeV(10%) RH", "WP_M2000W200_LH_2016")
WP_M2000W200_LH_2016.sigma = .148 
WP_M2000W200_LH_2016.year = 2016
WP_M2000W200_LH_2016.dataset = "/Wprimetotb_M2000W200_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M2000W400_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 2.0TeV(20%) RH", "WP_M2000W400_LH_2016")
WP_M2000W400_LH_2016.sigma = .07863 
WP_M2000W400_LH_2016.year = 2016
WP_M2000W400_LH_2016.dataset = "/Wprimetotb_M2000W400_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M2000W600_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 2.0TeV(30%) RH", "WP_M2000W600_LH_2016")
WP_M2000W600_LH_2016.sigma = .05403 
WP_M2000W600_LH_2016.year = 2016
WP_M2000W600_LH_2016.dataset = "/Wprimetotb_M2000W600_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M2400W240_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 2.4TeV(10%) RH", "WP_M2400W240_LH_2016")
WP_M2400W240_LH_2016.sigma = .05875 
WP_M2400W240_LH_2016.year = 2016
WP_M2400W240_LH_2016.dataset = "/Wprimetotb_M2400W240_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M2400W480_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 2.4TeV(20%) RH", "WP_M2400W480_LH_2016")
WP_M2400W480_LH_2016.sigma = .03287 
WP_M2400W480_LH_2016.year = 2016
WP_M2400W480_LH_2016.dataset = "/Wprimetotb_M2400W480_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M2400W720_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 2.4TeV(30%) RH", "WP_M2400W720_LH_2016")
WP_M2400W720_LH_2016.sigma = .02314 
WP_M2400W720_LH_2016.year = 2016
WP_M2400W720_LH_2016.dataset = "/Wprimetotb_M2400W720_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M2800W280_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 2.8TeV(10%) RH", "WP_M2800W280_LH_2016")
WP_M2800W280_LH_2016.sigma = .02556 
WP_M2800W280_LH_2016.year = 2016
WP_M2800W280_LH_2016.dataset = "/Wprimetotb_M2800W280_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v2/NANOAODSIM"

WP_M2800W560_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 2.8TeV(20%) RH", "WP_M2800W560_LH_2016")
WP_M2800W560_LH_2016.sigma = .01496 
WP_M2800W560_LH_2016.year = 2016
WP_M2800W560_LH_2016.dataset = "/Wprimetotb_M2800W560_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v2/NANOAODSIM"

WP_M2800W840_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 2.8TeV(30%) RH", "WP_M2800W840_LH_2016")
WP_M2800W840_LH_2016.sigma = .01115 
WP_M2800W840_LH_2016.year = 2016
WP_M2800W840_LH_2016.dataset = "/Wprimetotb_M2800W840_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M3200W320_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 3.2TeV(10%) RH", "WP_M3200W320_LH_2016")
WP_M3200W320_LH_2016.sigma = .01197 
WP_M3200W320_LH_2016.year = 2016
WP_M3200W320_LH_2016.dataset = "/Wprimetotb_M3200W320_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M3200W640_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 3.2TeV(20%) RH", "WP_M3200W640_LH_2016")
WP_M3200W640_LH_2016.sigma = .007494 
WP_M3200W640_LH_2016.year = 2016
WP_M3200W640_LH_2016.dataset = "/Wprimetotb_M3200W640_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M3200W960_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 3.2TeV(30%) RH", "WP_M3200W960_LH_2016")
WP_M3200W960_LH_2016.sigma = .005784 
WP_M3200W960_LH_2016.year = 2016
WP_M3200W960_LH_2016.dataset = "/Wprimetotb_M3200W960_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M3600W360_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 3.6TeV(10%) RH", "WP_M3600W360_LH_2016")
WP_M3600W360_LH_2016.sigma = .005971 
WP_M3600W360_LH_2016.year = 2016
WP_M3600W360_LH_2016.dataset = "/Wprimetotb_M3600W360_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M3600W720_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 3.6TeV(20%) RH", "WP_M3600W720_LH_2016")
WP_M3600W720_LH_2016.sigma = .004044 
WP_M3600W720_LH_2016.year = 2016
WP_M3600W720_LH_2016.dataset = "/Wprimetotb_M3600W720_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M3600W1080_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 3.6TeV(30%) RH", "WP_M3600W1080_LH_2016")
WP_M3600W1080_LH_2016.sigma = .003249 
WP_M3600W1080_LH_2016.year = 2016
WP_M3600W1080_LH_2016.dataset = "/Wprimetotb_M3600W1080_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M4000W400_LH_2016 = sample(ROOT.kAzure, 1, 1001, "W' 4.0TeV(10%) RH", "WP_M4000W400_LH_2016")
WP_M4000W400_LH_2016.sigma = .003271 
WP_M4000W400_LH_2016.year = 2016
WP_M4000W400_LH_2016.dataset = "/Wprimetotb_M4000W400_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M4000W800_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 4.0TeV(20%) RH", "WP_M4000W800_LH_2016")
WP_M4000W800_LH_2016.sigma = .002355 
WP_M4000W800_LH_2016.year = 2016
WP_M4000W800_LH_2016.dataset = "/Wprimetotb_M4000W800_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M4000W1200_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 4.0TeV(30%) RH", "WP_M4000W1200_LH_2016")
WP_M4000W1200_LH_2016.sigma = .00195 
WP_M4000W1200_LH_2016.year = 2016
WP_M4000W1200_LH_2016.dataset = "/Wprimetotb_M4000W1200_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M4400W440_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 4.4TeV(10%) RH", "WP_M4400W440_LH_2016")
WP_M4400W440_LH_2016.sigma = .001899 
WP_M4400W440_LH_2016.year = 2016
WP_M4400W440_LH_2016.dataset = "/Wprimetotb_M4400W440_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M4400W880_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 4.4TeV(20%) RH", "WP_M4400W880_LH_2016")
WP_M4400W880_LH_2016.sigma = .001437 
WP_M4400W880_LH_2016.year = 2016
WP_M4400W880_LH_2016.dataset = "/Wprimetotb_M4400W880_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M4400W1320_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 4.4TeV(30%) RH", "WP_M4400W1320_LH_2016")
WP_M4400W1320_LH_2016.sigma = .001232 
WP_M4400W1320_LH_2016.year = 2016
WP_M4400W1320_LH_2016.dataset = "/Wprimetotb_M4400W1320_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M4800W480_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 4.8TeV(10%) RH", "WP_M4800W480_LH_2016")
WP_M4800W480_LH_2016.sigma = .001173 
WP_M4800W480_LH_2016.year = 2016
WP_M4800W480_LH_2016.dataset = "/Wprimetotb_M4800W480_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M4800W960_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 4.8TeV(20%) RH", "WP_M4800W960_LH_2016")
WP_M4800W960_LH_2016.sigma = .00094 
WP_M4800W960_LH_2016.year = 2016
WP_M4800W960_LH_2016.dataset = "/Wprimetotb_M4800W960_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M4800W1440_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 4.8TeV(30%) RH", "WP_M4800W1440_LH_2016")
WP_M4800W1440_LH_2016.sigma = .0008208 
WP_M4800W1440_LH_2016.year = 2016
WP_M4800W1440_LH_2016.dataset = "/Wprimetotb_M4800W1440_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M5200W520_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 5.2TeV(10%) RH", "WP_M5200W520_LH_2016")
WP_M5200W520_LH_2016.sigma = .0007642 
WP_M5200W520_LH_2016.year = 2016
WP_M5200W520_LH_2016.dataset = "/Wprimetotb_M5200W520_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M5200W1040_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 5.2TeV(20%) RH", "WP_M5200W1040_LH_2016")
WP_M5200W1040_LH_2016.sigma = .0006335 
WP_M5200W1040_LH_2016.year = 2016
WP_M5200W1040_LH_2016.dataset = "/Wprimetotb_M5200W1040_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M5200W1560_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 5.2TeV(30%) RH", "WP_M5200W1560_LH_2016")
WP_M5200W1560_LH_2016.sigma = .0005667 
WP_M5200W1560_LH_2016.year = 2016
WP_M5200W1560_LH_2016.dataset = "/Wprimetotb_M5200W1560_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M5600W560_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 5.6TeV(10%) RH", "WP_M5600W560_LH_2016")
WP_M5600W560_LH_2016.sigma = .000518 
WP_M5600W560_LH_2016.year = 2016
WP_M5600W560_LH_2016.dataset = "/Wprimetotb_M5600W560_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M5600W1120_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 5.6TeV(20%) RH", "WP_M5600W1120_LH_2016")
WP_M5600W1120_LH_2016.sigma = .000449 
WP_M5600W1120_LH_2016.year = 2016
WP_M5600W1120_LH_2016.dataset = "/Wprimetotb_M5600W1120_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M5600W1680_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 5.6TeV(30%) RH", "WP_M5600W1680_LH_2016")
WP_M5600W1680_LH_2016.sigma = .0004055 
WP_M5600W1680_LH_2016.year = 2016
WP_M5600W1680_LH_2016.dataset = "/Wprimetotb_M5600W1680_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M6000W600_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 6.0TeV(10%) RH", "WP_M6000W600_LH_2016")
WP_M6000W600_LH_2016.sigma = .0003715 
WP_M6000W600_LH_2016.year = 2016
WP_M6000W600_LH_2016.dataset = "/Wprimetotb_M6000W600_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M6000W1200_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 6.0TeV(20%) RH", "WP_M6000W1200_LH_2016")
WP_M6000W1200_LH_2016.sigma = .0003255 
WP_M6000W1200_LH_2016.year = 2016
WP_M6000W1200_LH_2016.dataset = "/Wprimetotb_M6000W1200_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M6000W1800_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 6.0TeV(30%) RH", "WP_M6000W1800_LH_2016")
WP_M6000W1800_LH_2016.sigma = .0002973 
WP_M6000W1800_LH_2016.year = 2016
WP_M6000W1800_LH_2016.dataset = "/Wprimetotb_M6000W1800_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M2000W20_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 2.0TeV(1%) RH", "WP_M2000W20_LH_2016")
WP_M2000W20_LH_2016.sigma = 1.342 
WP_M2000W20_LH_2016.year = 2016
WP_M2000W20_LH_2016.dataset = "/Wprimetotb_M2000W20_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M2200W22_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 2.2TeV(1%) RH", "WP_M2200W22_LH_2016")
WP_M2200W22_LH_2016.sigma = .8111 
WP_M2200W22_LH_2016.year = 2016
WP_M2200W22_LH_2016.dataset = "/Wprimetotb_M2200W22_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M2400W24_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 2.4TeV(1%) RH", "WP_M2400W24_LH_2016")
WP_M2400W24_LH_2016.sigma = .5005 
WP_M2400W24_LH_2016.year = 2016
WP_M2400W24_LH_2016.dataset = "/Wprimetotb_M2400W24_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M2600W26_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 2.6TeV(1%) RH", "WP_M2600W26_LH_2016")
WP_M2600W26_LH_2016.sigma = .3115 
WP_M2600W26_LH_2016.year = 2016
WP_M2600W26_LH_2016.dataset = "/Wprimetotb_M2600W26_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M2800W28_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 2.8TeV(1%) RH", "WP_M2800W28_LH_2016")
WP_M2800W28_LH_2016.sigma = .1974 
WP_M2800W28_LH_2016.year = 2016
WP_M2800W28_LH_2016.dataset = "/Wprimetotb_M2800W28_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M3000W30_LH_2016 = sample(ROOT.kMagenta+2, 1, 1001, "W' 3.0TeV(1%) RH", "WP_M3000W30_LH_2016")
WP_M3000W30_LH_2016.sigma = .1271 
WP_M3000W30_LH_2016.year = 2016
WP_M3000W30_LH_2016.dataset = "/Wprimetotb_M3000W30_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v2/NANOAODSIM"

WP_M3200W32_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 3.2TeV(1%) RH", "WP_M3200W32_LH_2016")
WP_M3200W32_LH_2016.sigma = .08254 
WP_M3200W32_LH_2016.year = 2016
WP_M3200W32_LH_2016.dataset = "/Wprimetotb_M3200W32_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M3400W34_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 3.4TeV(1%) RH", "WP_M3400W34_LH_2016")
WP_M3400W34_LH_2016.sigma = .0544 
WP_M3400W34_LH_2016.year = 2016
WP_M3400W34_LH_2016.dataset = "/Wprimetotb_M3400W34_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M3600W36_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 3.6TeV(1%) RH", "WP_M3600W36_LH_2016")
WP_M3600W36_LH_2016.sigma = .03624 
WP_M3600W36_LH_2016.year = 2016
WP_M3600W36_LH_2016.dataset = "/Wprimetotb_M3600W36_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M3800W38_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 3.8TeV(1%) RH", "WP_M3800W38_LH_2016")
WP_M3800W38_LH_2016.sigma = .02449 
WP_M3800W38_LH_2016.year = 2016
WP_M3800W38_LH_2016.dataset = "/Wprimetotb_M3800W38_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M4000W40_LH_2016 = sample(ROOT.kGreen+2, 1, 1001, "W' 4.0TeV(1%) RH", "WP_M4000W40_LH_2016")
WP_M4000W40_LH_2016.sigma = .01679 
WP_M4000W40_LH_2016.year = 2016
WP_M4000W40_LH_2016.dataset = "/Wprimetotb_M4000W40_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M4200W42_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 4.2TeV(1%) RH", "WP_M4200W42_LH_2016")
WP_M4200W42_LH_2016.sigma = .01161 
WP_M4200W42_LH_2016.year = 2016
WP_M4200W42_LH_2016.dataset = "/Wprimetotb_M4200W42_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M4400W44_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 4.4TeV(1%) RH", "WP_M4400W44_LH_2016")
WP_M4400W44_LH_2016.sigma = .008501 
WP_M4400W44_LH_2016.year = 2016
WP_M4400W44_LH_2016.dataset = "/Wprimetotb_M4400W44_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M4600W46_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 4.6TeV(1%) RH", "WP_M4600W46_LH_2016")
WP_M4600W46_LH_2016.sigma = .006172 
WP_M4600W46_LH_2016.year = 2016
WP_M4600W46_LH_2016.dataset = "/Wprimetotb_M4600W46_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M4800W48_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 4.8TeV(1%) RH", "WP_M4800W48_LH_2016")
WP_M4800W48_LH_2016.sigma = .004538 
WP_M4800W48_LH_2016.year = 2016
WP_M4800W48_LH_2016.dataset = "/Wprimetotb_M4800W48_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M5000W50_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 5.0TeV(1%) RH", "WP_M5000W50_LH_2016")
WP_M5000W50_LH_2016.sigma = .003381 
WP_M5000W50_LH_2016.year = 2016
WP_M5000W50_LH_2016.dataset = "/Wprimetotb_M5000W50_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M5200W52_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 5.2TeV(1%) RH", "WP_M5200W52_LH_2016")
WP_M5200W52_LH_2016.sigma = .00254 
WP_M5200W52_LH_2016.year = 2016
WP_M5200W52_LH_2016.dataset = "/Wprimetotb_M5200W52_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M5400W54_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 5.4TeV(1%) RH", "WP_M5400W54_LH_2016")
WP_M5400W54_LH_2016.sigma = .001929 
WP_M5400W54_LH_2016.year = 2016
WP_M5400W54_LH_2016.dataset = "/Wprimetotb_M5400W54_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M5600W56_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 5.6TeV(1%) RH", "WP_M5600W56_LH_2016")
WP_M5600W56_LH_2016.sigma = .001476 
WP_M5600W56_LH_2016.year = 2016
WP_M5600W56_LH_2016.dataset = "/Wprimetotb_M5600W56_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M5800W58_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 5.8TeV(1%) RH", "WP_M5800W58_LH_2016")
WP_M5800W58_LH_2016.sigma = .001138 
WP_M5800W58_LH_2016.year = 2016
WP_M5800W58_LH_2016.dataset = "/Wprimetotb_M5800W58_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M6000W60_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 6.0TeV(1%) RH", "WP_M6000W60_LH_2016")
WP_M6000W60_LH_2016.sigma = .0008807 
WP_M6000W60_LH_2016.year = 2016
WP_M6000W60_LH_2016.dataset = "/Wprimetotb_M6000W60_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_LH_2016 = sample(ROOT.kBlue, 1, 1001, "W' LH", "WP_LH_2016")
WP_LH_2016.year = 2016
WP_LH_2016.components = [WP_M2000W200_LH_2016, WP_M2000W400_LH_2016, WP_M2000W600_LH_2016, WP_M2400W240_LH_2016, WP_M2400W480_LH_2016, WP_M2400W720_LH_2016, WP_M2800W280_LH_2016, WP_M2800W560_LH_2016, WP_M2800W840_LH_2016, WP_M3200W320_LH_2016, WP_M3200W640_LH_2016, WP_M3200W960_LH_2016, WP_M3600W360_LH_2016, WP_M3600W720_LH_2016, WP_M3600W1080_LH_2016, WP_M4000W400_LH_2016, WP_M4000W800_LH_2016, WP_M4000W1200_LH_2016, WP_M4400W440_LH_2016, WP_M4400W880_LH_2016, WP_M4400W1320_LH_2016, WP_M4800W480_LH_2016, WP_M4800W960_LH_2016, WP_M4800W1440_LH_2016, WP_M5200W520_LH_2016, WP_M5200W1040_LH_2016, WP_M5200W1560_LH_2016, WP_M5600W560_LH_2016, WP_M5600W1120_LH_2016, WP_M5600W1680_LH_2016, WP_M6000W600_LH_2016, WP_M6000W1200_LH_2016, WP_M6000W1800_LH_2016, WP_M2000W20_LH_2016, WP_M2200W22_LH_2016, WP_M2400W24_LH_2016, WP_M2600W26_LH_2016, WP_M2800W28_LH_2016, WP_M3000W30_LH_2016, WP_M3200W32_LH_2016, WP_M3400W34_LH_2016, WP_M3600W36_LH_2016, WP_M3800W38_LH_2016, WP_M4000W40_LH_2016, WP_M4200W42_LH_2016, WP_M4400W44_LH_2016, WP_M4600W46_LH_2016, WP_M4800W48_LH_2016, WP_M5000W50_LH_2016, WP_M5200W52_LH_2016, WP_M5400W54_LH_2016, WP_M5600W56_LH_2016, WP_M5800W58_LH_2016, WP_M6000W60_LH_2016]

################################ Signal Sample RH ################################
WP_M2000W200_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 2.0TeV(10%) RH", "WP_M2000W200_RH_2016")
WP_M2000W200_RH_2016.sigma = .154 
WP_M2000W200_RH_2016.year = 2016
WP_M2000W200_RH_2016.dataset = "/Wprimetotb_M2000W200_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M2000W400_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 2.0TeV(20%) RH", "WP_M2000W400_RH_2016")
WP_M2000W400_RH_2016.sigma = .08177 
WP_M2000W400_RH_2016.year = 2016
WP_M2000W400_RH_2016.dataset = "/Wprimetotb_M2000W400_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M2000W600_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 2.0TeV(30%) RH", "WP_M2000W600_RH_2016")
WP_M2000W600_RH_2016.sigma = .05617 
WP_M2000W600_RH_2016.year = 2016
WP_M2000W600_RH_2016.dataset = "/Wprimetotb_M2000W600_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M2400W240_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 2.4TeV(10%) RH", "WP_M2400W240_RH_2016")
WP_M2400W240_RH_2016.sigma = .06106 
WP_M2400W240_RH_2016.year = 2016
WP_M2400W240_RH_2016.dataset = "/Wprimetotb_M2400W240_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M2400W480_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 2.4TeV(20%) RH", "WP_M2400W480_RH_2016")
WP_M2400W480_RH_2016.sigma = .03416 
WP_M2400W480_RH_2016.year = 2016
WP_M2400W480_RH_2016.dataset = "/Wprimetotb_M2400W480_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M2400W720_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 2.4TeV(30%) RH", "WP_M2400W720_RH_2016")
WP_M2400W720_RH_2016.sigma = .02404 
WP_M2400W720_RH_2016.year = 2016
WP_M2400W720_RH_2016.dataset = "/Wprimetotb_M2400W720_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v2/NANOAODSIM"

WP_M2800W280_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 2.8TeV(10%) RH", "WP_M2800W280_RH_2016")
WP_M2800W280_RH_2016.sigma = .02655 
WP_M2800W280_RH_2016.year = 2016
WP_M2800W280_RH_2016.dataset = "/Wprimetotb_M2800W280_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M2800W560_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 2.8TeV(20%) RH", "WP_M2800W560_RH_2016")
WP_M2800W560_RH_2016.sigma = .01554 
WP_M2800W560_RH_2016.year = 2016
WP_M2800W560_RH_2016.dataset = "/Wprimetotb_M2800W560_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M2800W840_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 2.8TeV(30%) RH", "WP_M2800W840_RH_2016")
WP_M2800W840_RH_2016.sigma = .01158 
WP_M2800W840_RH_2016.year = 2016
WP_M2800W840_RH_2016.dataset = "/Wprimetotb_M2800W840_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M3200W320_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 3.2TeV(10%) RH", "WP_M3200W320_RH_2016")
WP_M3200W320_RH_2016.sigma = .01242 
WP_M3200W320_RH_2016.year = 2016
WP_M3200W320_RH_2016.dataset = "/Wprimetotb_M3200W320_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M3200W640_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 3.2TeV(20%) RH", "WP_M3200W640_RH_2016")
WP_M3200W640_RH_2016.sigma = .007778 
WP_M3200W640_RH_2016.year = 2016
WP_M3200W640_RH_2016.dataset = "/Wprimetotb_M3200W640_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M3200W960_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 3.2TeV(30%) RH", "WP_M3200W960_RH_2016")
WP_M3200W960_RH_2016.sigma = .006004 
WP_M3200W960_RH_2016.year = 2016
WP_M3200W960_RH_2016.dataset = "/Wprimetotb_M3200W960_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M3600W360_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 3.6TeV(10%) RH", "WP_M3600W360_RH_2016")
WP_M3600W360_RH_2016.sigma = .006191 
WP_M3600W360_RH_2016.year = 2016
WP_M3600W360_RH_2016.dataset = "/Wprimetotb_M3600W360_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M3600W720_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 3.6TeV(20%) RH", "WP_M3600W720_RH_2016")
WP_M3600W720_RH_2016.sigma = .004195 
WP_M3600W720_RH_2016.year = 2016
WP_M3600W720_RH_2016.dataset = "/Wprimetotb_M3600W720_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M3600W1080_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 3.6TeV(30%) RH", "WP_M3600W1080_RH_2016")
WP_M3600W1080_RH_2016.sigma = .003372 
WP_M3600W1080_RH_2016.year = 2016
WP_M3600W1080_RH_2016.dataset = "/Wprimetotb_M3600W1080_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M4000W400_RH_2016 = sample(ROOT.kMagenta, 1, 1001, "W' 4.0TeV(10%) RH", "WP_M4000W400_RH_2016")
WP_M4000W400_RH_2016.sigma = .00339 
WP_M4000W400_RH_2016.year = 2016
WP_M4000W400_RH_2016.dataset = "/Wprimetotb_M4000W400_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M4000W800_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 4.0TeV(20%) RH", "WP_M4000W800_RH_2016")
WP_M4000W800_RH_2016.sigma = .002443 
WP_M4000W800_RH_2016.year = 2016
WP_M4000W800_RH_2016.dataset = "/Wprimetotb_M4000W800_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M4000W1200_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 4.0TeV(30%) RH", "WP_M4000W1200_RH_2016")
WP_M4000W1200_RH_2016.sigma = .002024 
WP_M4000W1200_RH_2016.year = 2016
WP_M4000W1200_RH_2016.dataset = "/Wprimetotb_M4000W1200_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M4400W440_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 4.4TeV(10%) RH", "WP_M4400W440_RH_2016")
WP_M4400W440_RH_2016.sigma = .001967 
WP_M4400W440_RH_2016.year = 2016
WP_M4400W440_RH_2016.dataset = "/Wprimetotb_M4400W440_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M4400W880_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 4.4TeV(20%) RH", "WP_M4400W880_RH_2016")
WP_M4400W880_RH_2016.sigma = .001491 
WP_M4400W880_RH_2016.year = 2016
WP_M4400W880_RH_2016.dataset = "/Wprimetotb_M4400W880_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M4400W1320_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 4.4TeV(30%) RH", "WP_M4400W1320_RH_2016")
WP_M4400W1320_RH_2016.sigma = .001278 
WP_M4400W1320_RH_2016.year = 2016
WP_M4400W1320_RH_2016.dataset = "/Wprimetotb_M4400W1320_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M4800W480_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 4.8TeV(10%) RH", "WP_M4800W480_RH_2016")
WP_M4800W480_RH_2016.sigma = .001217 
WP_M4800W480_RH_2016.year = 2016
WP_M4800W480_RH_2016.dataset = "/Wprimetotb_M4800W480_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M4800W960_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 4.8TeV(20%) RH", "WP_M4800W960_RH_2016")
WP_M4800W960_RH_2016.sigma = .0009753 
WP_M4800W960_RH_2016.year = 2016
WP_M4800W960_RH_2016.dataset = "/Wprimetotb_M4800W960_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M4800W1440_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 4.8TeV(30%) RH", "WP_M4800W1440_RH_2016")
WP_M4800W1440_RH_2016.sigma = .0008519 
WP_M4800W1440_RH_2016.year = 2016
WP_M4800W1440_RH_2016.dataset = "/Wprimetotb_M4800W1440_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M5200W520_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 5.2TeV(10%) RH", "WP_M5200W520_RH_2016")
WP_M5200W520_RH_2016.sigma = .0007929 
WP_M5200W520_RH_2016.year = 2016
WP_M5200W520_RH_2016.dataset = "/Wprimetotb_M5200W520_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M5200W1040_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 5.2TeV(20%) RH", "WP_M5200W1040_RH_2016")
WP_M5200W1040_RH_2016.sigma = .0006573 
WP_M5200W1040_RH_2016.year = 2016
WP_M5200W1040_RH_2016.dataset = "/Wprimetotb_M5200W1040_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M5200W1560_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 5.2TeV(30%) RH", "WP_M5200W1560_RH_2016")
WP_M5200W1560_RH_2016.sigma = .0005882 
WP_M5200W1560_RH_2016.year = 2016
WP_M5200W1560_RH_2016.dataset = "/Wprimetotb_M5200W1560_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M5600W560_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 5.6TeV(10%) RH", "WP_M5600W560_RH_2016")
WP_M5600W560_RH_2016.sigma = .0005376 
WP_M5600W560_RH_2016.year = 2016
WP_M5600W560_RH_2016.dataset = "/Wprimetotb_M5600W560_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M5600W1120_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 5.6TeV(20%) RH", "WP_M5600W1120_RH_2016")
WP_M5600W1120_RH_2016.sigma = .000466 
WP_M5600W1120_RH_2016.year = 2016
WP_M5600W1120_RH_2016.dataset = "/Wprimetotb_M5600W1120_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M5600W1680_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 5.6TeV(30%) RH", "WP_M5600W1680_RH_2016")
WP_M5600W1680_RH_2016.sigma = .0004209 
WP_M5600W1680_RH_2016.year = 2016
WP_M5600W1680_RH_2016.dataset = "/Wprimetotb_M5600W1680_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M6000W600_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 6.0TeV(10%) RH", "WP_M6000W600_RH_2016")
WP_M6000W600_RH_2016.sigma = .0003858 
WP_M6000W600_RH_2016.year = 2016
WP_M6000W600_RH_2016.dataset = "/Wprimetotb_M6000W600_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M6000W1200_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 6.0TeV(20%) RH", "WP_M6000W1200_RH_2016")
WP_M6000W1200_RH_2016.sigma = .000338 
WP_M6000W1200_RH_2016.year = 2016
WP_M6000W1200_RH_2016.dataset = "/Wprimetotb_M6000W1200_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M6000W1800_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 6.0TeV(30%) RH", "WP_M6000W1800_RH_2016")
WP_M6000W1800_RH_2016.sigma = .0003086 
WP_M6000W1800_RH_2016.year = 2016
WP_M6000W1800_RH_2016.dataset = "/Wprimetotb_M6000W1800_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M2000W20_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 2.0TeV(1%) RH", "WP_M2000W20_RH_2016")
WP_M2000W20_RH_2016.sigma = 1.397 
WP_M2000W20_RH_2016.year = 2016
WP_M2000W20_RH_2016.dataset = "/Wprimetotb_M2000W20_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M2200W22_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 2.2TeV(1%) RH", "WP_M2200W22_RH_2016")
WP_M2200W22_RH_2016.sigma = .8439 
WP_M2200W22_RH_2016.year = 2016
WP_M2200W22_RH_2016.dataset = "/Wprimetotb_M2200W22_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M2400W24_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 2.4TeV(1%) RH", "WP_M2400W24_RH_2016")
WP_M2400W24_RH_2016.sigma = .5203 
WP_M2400W24_RH_2016.year = 2016
WP_M2400W24_RH_2016.dataset = "/Wprimetotb_M2400W24_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M2600W26_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 2.6TeV(1%) RH", "WP_M2600W26_RH_2016")
WP_M2600W26_RH_2016.sigma = .3236 
WP_M2600W26_RH_2016.year = 2016
WP_M2600W26_RH_2016.dataset = "/Wprimetotb_M2600W26_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M2800W28_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 2.8TeV(1%) RH", "WP_M2800W28_RH_2016")
WP_M2800W28_RH_2016.sigma = .2049 
WP_M2800W28_RH_2016.year = 2016
WP_M2800W28_RH_2016.dataset = "/Wprimetotb_M2800W28_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M3000W30_RH_2016 = sample(ROOT.kAzure, 1, 1001, "W' 3.0TeV(1%) RH", "WP_M3000W30_RH_2016")
WP_M3000W30_RH_2016.sigma = .1318 
WP_M3000W30_RH_2016.year = 2016
WP_M3000W30_RH_2016.dataset = "/Wprimetotb_M3000W30_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M3200W32_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 3.2TeV(1%) RH", "WP_M3200W32_RH_2016")
WP_M3200W32_RH_2016.sigma = .08553 
WP_M3200W32_RH_2016.year = 2016
WP_M3200W32_RH_2016.dataset = "/Wprimetotb_M3200W32_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M3400W34_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 3.4TeV(1%) RH", "WP_M3400W34_RH_2016")
WP_M3400W34_RH_2016.sigma = .05633 
WP_M3400W34_RH_2016.year = 2016
WP_M3400W34_RH_2016.dataset = "/Wprimetotb_M3400W34_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M3600W36_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 3.6TeV(1%) RH", "WP_M3600W36_RH_2016")
WP_M3600W36_RH_2016.sigma = .0375 
WP_M3600W36_RH_2016.year = 2016
WP_M3600W36_RH_2016.dataset = "/Wprimetotb_M3600W36_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M3800W38_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 3.8TeV(1%) RH", "WP_M3800W38_RH_2016")
WP_M3800W38_RH_2016.sigma = .02533 
WP_M3800W38_RH_2016.year = 2016
WP_M3800W38_RH_2016.dataset = "/Wprimetotb_M3800W38_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M4000W40_RH_2016 = sample(ROOT.kGreen+2, 1, 1001, "W' 4.0TeV(1%) RH", "WP_M4000W40_RH_2016")
WP_M4000W40_RH_2016.sigma = .01736 
WP_M4000W40_RH_2016.year = 2016
WP_M4000W40_RH_2016.dataset = "/Wprimetotb_M4000W40_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M4200W42_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 4.2TeV(1%) RH", "WP_M4200W42_RH_2016")
WP_M4200W42_RH_2016.sigma = .01208 
WP_M4200W42_RH_2016.year = 2016
WP_M4200W42_RH_2016.dataset = "/Wprimetotb_M4200W42_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M4400W44_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 4.4TeV(1%) RH", "WP_M4400W44_RH_2016")
WP_M4400W44_RH_2016.sigma = .00879 
WP_M4400W44_RH_2016.year = 2016
WP_M4400W44_RH_2016.dataset = "/Wprimetotb_M4400W44_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M4600W46_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 4.6TeV(1%) RH", "WP_M4600W46_RH_2016")
WP_M4600W46_RH_2016.sigma = .006384 
WP_M4600W46_RH_2016.year = 2016
WP_M4600W46_RH_2016.dataset = "/Wprimetotb_M4600W46_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M4800W48_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 4.8TeV(1%) RH", "WP_M4800W48_RH_2016")
WP_M4800W48_RH_2016.sigma = .004696 
WP_M4800W48_RH_2016.year = 2016
WP_M4800W48_RH_2016.dataset = "/Wprimetotb_M4800W48_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M5000W50_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 5.0TeV(1%) RH", "WP_M5000W50_RH_2016")
WP_M5000W50_RH_2016.sigma = .003501 
WP_M5000W50_RH_2016.year = 2016
WP_M5000W50_RH_2016.dataset = "/Wprimetotb_M5000W50_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M5200W52_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 5.2TeV(1%) RH", "WP_M5200W52_RH_2016")
WP_M5200W52_RH_2016.sigma = .002633 
WP_M5200W52_RH_2016.year = 2016
WP_M5200W52_RH_2016.dataset = "/Wprimetotb_M5200W52_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M5400W54_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 5.4TeV(1%) RH", "WP_M5400W54_RH_2016")
WP_M5400W54_RH_2016.sigma = .002008 
WP_M5400W54_RH_2016.year = 2016
WP_M5400W54_RH_2016.dataset = "/Wprimetotb_M5400W54_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M5600W56_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 5.6TeV(1%) RH", "WP_M5600W56_RH_2016")
WP_M5600W56_RH_2016.sigma = .001533 
WP_M5600W56_RH_2016.year = 2016
WP_M5600W56_RH_2016.dataset = "/Wprimetotb_M5600W56_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M5800W58_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 5.8TeV(1%) RH", "WP_M5800W58_RH_2016")
WP_M5800W58_RH_2016.sigma = .001182 
WP_M5800W58_RH_2016.year = 2016
WP_M5800W58_RH_2016.dataset = "/Wprimetotb_M5800W58_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M6000W60_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' 6.0TeV(1%) RH", "WP_M6000W60_RH_2016")
WP_M6000W60_RH_2016.sigma = .0009153 
WP_M6000W60_RH_2016.year = 2016
WP_M6000W60_RH_2016.dataset = "/Wprimetotb_M6000W60_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_RH_2016 = sample(ROOT.kBlue, 1, 1001, "W' RH", "WP_RH_2016")
WP_RH_2016.year = 2016
#WP_RH_2016.components = [WP_M2000W200_RH_2016, WP_M2000W400_RH_2016, WP_M2000W600_RH_2016, WP_M2400W240_RH_2016, WP_M2400W480_RH_2016, WP_M2400W720_RH_2016, WP_M2800W280_RH_2016, WP_M2800W560_RH_2016, WP_M2800W840_RH_2016, WP_M3200W320_RH_2016, WP_M3200W640_RH_2016, WP_M3200W960_RH_2016, WP_M3600W360_RH_2016, WP_M3600W720_RH_2016, WP_M3600W1080_RH_2016, WP_M4000W400_RH_2016, WP_M4000W800_RH_2016, WP_M4000W1200_RH_2016, WP_M4400W440_RH_2016, WP_M4400W880_RH_2016, WP_M4400W1320_RH_2016, WP_M4800W480_RH_2016, WP_M4800W960_RH_2016, WP_M4800W1440_RH_2016, WP_M5200W520_RH_2016, WP_M5200W1040_RH_2016, WP_M5200W1560_RH_2016, WP_M5600W560_RH_2016, WP_M5600W1120_RH_2016, WP_M5600W1680_RH_2016, WP_M6000W600_RH_2016, WP_M6000W1200_RH_2016, WP_M6000W1800_RH_2016, WP_M2000W20_RH_2016, WP_M2200W22_RH_2016, WP_M2400W24_RH_2016, WP_M2600W26_RH_2016, WP_M2800W28_RH_2016, WP_M3000W30_RH_2016, WP_M3200W32_RH_2016, WP_M3400W34_RH_2016, WP_M3600W36_RH_2016, WP_M3800W38_RH_2016, WP_M4000W40_RH_2016, WP_M4200W42_RH_2016, WP_M4400W44_RH_2016, WP_M4600W46_RH_2016, WP_M4800W48_RH_2016, WP_M5000W50_RH_2016, WP_M5200W52_RH_2016, WP_M5400W54_RH_2016, WP_M5600W56_RH_2016, WP_M5800W58_RH_2016, WP_M6000W60_RH_2016]
WP_RH_2016.components = [ WP_M2000W20_RH_2016, WP_M2200W22_RH_2016, WP_M2400W24_RH_2016, WP_M2600W26_RH_2016, WP_M2800W28_RH_2016, WP_M3000W30_RH_2016, WP_M3200W32_RH_2016, WP_M3400W34_RH_2016, WP_M3600W36_RH_2016, WP_M3800W38_RH_2016, WP_M4000W40_RH_2016, WP_M4200W42_RH_2016, WP_M4400W44_RH_2016, WP_M4600W46_RH_2016, WP_M4800W48_RH_2016, WP_M5000W50_RH_2016, WP_M5200W52_RH_2016, WP_M5400W54_RH_2016, WP_M5600W56_RH_2016, WP_M5800W58_RH_2016, WP_M6000W60_RH_2016]
#WP_RH_2016.components = [WP_M2000W20_RH_2016, WP_M3000W30_RH_2016, WP_M4000W40_RH_2016, WP_M4000W400_RH_2016]

WP_M1900_RH_COMP_2016 = sample(ROOT.kBlue, 1, 1001, "W' 1.9TeV(3%) RH", "WP_M1900_RH_COMP_2016")
WP_M1900_RH_COMP_2016.sigma = 0.14922
WP_M1900_RH_COMP_2016.year = 2016
WP_M1900_RH_COMP_2016.dataset = "/WprimeToTB_TToLep_M-1900_RH_TuneCUETP8M1_13TeV-comphep-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M3000_RH_COMP_2016 = sample(ROOT.kBlue, 1, 1001, "W' 3TeV(3%) RH", "WP_M3000_RH_COMP_2016")
WP_M3000_RH_COMP_2016.sigma = 0.010756
WP_M3000_RH_COMP_2016.year = 2016
WP_M3000_RH_COMP_2016.dataset = "/WprimeToTB_TToLep_M-3000_RH_TuneCUETP8M1_13TeV-comphep-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_M4000_RH_COMP_2016 = sample(ROOT.kBlue, 1, 1001, "W' 4TeV(3%) RH", "WP_M4000_RH_COMP_2016")
WP_M4000_RH_COMP_2016.sigma = 0.001425
WP_M4000_RH_COMP_2016.year = 2016
WP_M4000_RH_COMP_2016.dataset = "/WprimeToTB_TToLep_M-4000_RH_TuneCUETP8M1_13TeV-comphep-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WP_RH_COMP_2016 = sample(ROOT.kBlue, 1, 1001, "W' RH Comphep", "WP_RH_COMP_2016")
WP_RH_COMP_2016.year = 2016
WP_RH_COMP_2016.components = [WP_M1900_RH_COMP_2016, WP_M3000_RH_COMP_2016, WP_M4000_RH_COMP_2016]

###################################################################################################################################################################
############################################################                                           ############################################################
############################################################                    2017                   ############################################################
############################################################                                           ############################################################
###################################################################################################################################################################

################################ TTbar ################################
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

TT_semilep_2017 = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_SemiLep2017")
TT_semilep_2017.sigma = 831.76*0.438
TT_semilep_2017.year = 2017
TT_semilep_2017.dataset = "/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/"+tag2_2017+"-v1/NANOAODSIM"
# "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/" + tag2_2017 + "-v1/NANOAODSIM"

TT_Mtt_2017 = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_Mtt_2017")
TT_Mtt_2017.year = 2017
TT_Mtt_2017.components = [TT_semilep_2017] #[TT_Mtt700to1000_2017, TT_Mtt1000toInf_2017]

TT_dilep_2017 = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_dilep_2017")
TT_dilep_2017.sigma =  831.76 * 0.10 #pb
TT_dilep_2017.year = 2017
TT_dilep_2017.dataset = "/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/"+tag2_2017+"-v1/NANOAODSIM"

################################ WJets ################################
WJetsHT200to400_2017 = sample(ROOT.kGreen+2, 1, 1001, "W + Jets", "WJetsHT200to400_2017")
WJetsHT200to400_2017.sigma = 359.7 * 1.21 #pb
WJetsHT200to400_2017.year = 2017
WJetsHT200to400_2017.dataset = "/WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2017+"-v1/NANOAODSIM"
#WJetsHT200to400_2017.files = jr.json_reader(path+"/WJets_HT200To400_2017.json")

WJetsHT400to600_2017 = sample(ROOT.kGreen+2, 1, 1001, "W + Jets", "WJetsHT400to600_2017")
WJetsHT400to600_2017.sigma = 48.91 * 1.21 #pb
WJetsHT400to600_2017.year = 2017
WJetsHT400to600_2017.dataset = "/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2017+"-v1/NANOAODSIM"
#WJetsHT400to600_2017.files = jr.json_reader(path+"/WJets_HT400To600_2017.json")

WJetsHT600to800_2017 = sample(ROOT.kGreen+2, 1, 1001, "W + Jets", "WJetsHT600to800_2017")
WJetsHT600to800_2017.sigma = 12.05 * 1.21 #pb
WJetsHT600to800_2017.year = 2017
WJetsHT600to800_2017.dataset = "/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2017+"-v1/NANOAODSIM"
#WJetsHT600to800_2017.files = jr.json_reader(path+"/WJets_HT600To800_2017.json")

WJetsHT800to1200_2017 = sample(ROOT.kGreen+2, 1, 1001, "W + Jets", "WJetsHT800to1200_2017")
WJetsHT800to1200_2017.sigma = 5.501 * 1.21 #pb
WJetsHT800to1200_2017.year = 2017
WJetsHT800to1200_2017.dataset = "/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2017+"-v1/NANOAODSIM"
#WJetsHT800to1200_2017.files = jr.json_reader(path+"/WJets_HT800To1200_2017.json")

WJetsHT1200to2500_2017 = sample(ROOT.kGreen+2, 1, 1001, "W + Jets", "WJetsHT1200to2500_2017")
WJetsHT1200to2500_2017.sigma = 1.329 * 1.21 #pb
WJetsHT1200to2500_2017.year = 2017
WJetsHT1200to2500_2017.dataset = "/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2017+"-v1/NANOAODSIM"
#WJetsHT1200to2500_2017.files = jr.json_reader(path+"/WJets_HT1200To2500_2017.json")

WJetsHT2500toInf_2017 = sample(ROOT.kGreen+2, 1, 1001, "W + Jets", "WJetsHT2500toInf_2017")
WJetsHT2500toInf_2017.sigma = 0.03216 * 1.2 #pb
WJetsHT2500toInf_2017.year = 2017
WJetsHT2500toInf_2017.dataset = "/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2017+"-v1/NANOAODSIM"
#WJetsHT2500toInf_2017.files = jr.json_reader(path+"/WJets_HT2500ToInf_2017.json")

WJets_2017 = sample(ROOT.kGreen+2, 1, 1001, "W + Jets", "WJets_2017")
WJets_2017.year = 2017
WJets_2017.components = [WJetsHT200to400_2017, WJetsHT400to600_2017, WJetsHT600to800_2017, WJetsHT800to1200_2017, WJetsHT1200to2500_2017, WJetsHT2500toInf_2017]

################################ Single Top ################################
ST_tch_t_2017 = sample(ROOT.kYellow, 1, 1001, "ST t-ch", "ST_tch_t_2017")
ST_tch_t_2017.sigma =  136.02 #pb
ST_tch_t_2017.year = 2017
ST_tch_t_2017.dataset = "/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/"+tag2_2017+"-v1/NANOAODSIM"

ST_tch_tbar_2017 = sample(ROOT.kYellow, 1, 1001, "ST t-ch", "ST_tch_tbar_2017")
ST_tch_tbar_2017.sigma =  80.95 #pb
ST_tch_tbar_2017.year = 2017
ST_tch_tbar_2017.dataset = "/ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/"+tag_2017+"-v1/NANOAODSIM"

ST_tW_t_2017 = sample(ROOT.kYellow, 1, 1001, "ST tW", "ST_tW_t_2017")
ST_tW_t_2017.sigma =  71.7/2 #pb
ST_tW_t_2017.year = 2017
ST_tW_t_2017.dataset = "/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/"+tag_2017+"-v1/NANOAODSIM"

ST_tW_tbar_2017 = sample(ROOT.kYellow, 1, 1001, "ST tW", "ST_tW_tbar_2017")
ST_tW_tbar_2017.sigma = 71.7/2 #pb
ST_tW_tbar_2017.year = 2017
ST_tW_tbar_2017.dataset = "/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/"+tag_2017+"-v1/NANOAODSIM"

ST_sch_2017 = sample(ROOT.kYellow, 1, 1001, "ST s-ch", "ST_sch_2017")
ST_sch_2017.sigma = 10.32*0.324 #pb
ST_sch_2017.year = 2017
ST_sch_2017.dataset = "/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/"+tag_2017+"-v1/NANOAODSIM"

ST_2017 = sample(ROOT.kYellow, 1, 1001, "Single top", "ST_2017")
ST_2017.year = 2017
ST_2017.components = [ST_tch_t_2017, ST_tch_tbar_2017, ST_tW_t_2017, ST_tW_tbar_2017, ST_sch_2017]

################################ QCD ################################
QCDHT_300to500_2017 = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_300to500_2017")
QCDHT_300to500_2017.sigma = 347700 #pb
QCDHT_300to500_2017.year = 2017
QCDHT_300to500_2017.dataset = "/QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8/"+tag2_2017+"-v1/NANOAODSIM"
QCDHT_500to700_2017 = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_500to700_2017")
QCDHT_500to700_2017.sigma = 32100 #pb
QCDHT_500to700_2017.year = 2017
QCDHT_500to700_2017.dataset = "/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"
QCDHT_700to1000_2017 = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_700to1000_2017")
QCDHT_700to1000_2017.sigma = 6831 #pb
QCDHT_700to1000_2017.year = 2017
QCDHT_700to1000_2017.dataset = "/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/"+tag2_2017+"-v1/NANOAODSIM"
QCDHT_1000to1500_2017 = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_1000to1500_2017")
QCDHT_1000to1500_2017.sigma = 1207 #pb
QCDHT_1000to1500_2017.year = 2017
QCDHT_1000to1500_2017.dataset = "/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/"+tag2_2017+"-v1/NANOAODSIM"
QCDHT_1500to2000_2017 = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_1500to2000_2017")
QCDHT_1500to2000_2017.sigma = 119.9 #pb
QCDHT_1500to2000_2017.year = 2017
QCDHT_1500to2000_2017.dataset = "/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"
QCDHT_2000toInf_2017 = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_2000toInf_2017")
QCDHT_2000toInf_2017.sigma = 25.24 #pb
QCDHT_2000toInf_2017.year = 2017
QCDHT_2000toInf_2017.dataset = "/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"
QCD_2017 = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_2017")
QCD_2017.year = 2017
QCD_2017.components = [QCDHT_300to500_2017, QCDHT_500to700_2017, QCDHT_700to1000_2017, QCDHT_1000to1500_2017, QCDHT_1500to2000_2017, QCDHT_2000toInf_2017]

################################ Signal Sample LH w/o SM Interference ################################
WP_M2000W200_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 2.0TeV(10%) RH", "WP_M2000W200_LH_2017")
WP_M2000W200_LH_2017.sigma = .148 
WP_M2000W200_LH_2017.year = 2017
WP_M2000W200_LH_2017.dataset = "/Wprimetotb_M2000W200_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M2000W400_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 2.0TeV(20%) RH", "WP_M2000W400_LH_2017")
WP_M2000W400_LH_2017.sigma = .07863 
WP_M2000W400_LH_2017.year = 2017
WP_M2000W400_LH_2017.dataset = "/Wprimetotb_M2000W400_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M2000W600_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 2.0TeV(30%) RH", "WP_M2000W600_LH_2017")
WP_M2000W600_LH_2017.sigma = .05403 
WP_M2000W600_LH_2017.year = 2017
WP_M2000W600_LH_2017.dataset = "/Wprimetotb_M2000W600_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M2400W240_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 2.4TeV(10%) RH", "WP_M2400W240_LH_2017")
WP_M2400W240_LH_2017.sigma = .05875 
WP_M2400W240_LH_2017.year = 2017
WP_M2400W240_LH_2017.dataset = "/Wprimetotb_M2400W240_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M2400W480_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 2.4TeV(20%) RH", "WP_M2400W480_LH_2017")
WP_M2400W480_LH_2017.sigma = .03287 
WP_M2400W480_LH_2017.year = 2017
WP_M2400W480_LH_2017.dataset = "/Wprimetotb_M2400W480_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M2400W720_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 2.4TeV(30%) RH", "WP_M2400W720_LH_2017")
WP_M2400W720_LH_2017.sigma = .02314 
WP_M2400W720_LH_2017.year = 2017
WP_M2400W720_LH_2017.dataset = "/Wprimetotb_M2400W720_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M2800W280_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 2.8TeV(10%) RH", "WP_M2800W280_LH_2017")
WP_M2800W280_LH_2017.sigma = .02556 
WP_M2800W280_LH_2017.year = 2017
WP_M2800W280_LH_2017.dataset = "/Wprimetotb_M2800W280_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M2800W560_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 2.8TeV(20%) RH", "WP_M2800W560_LH_2017")
WP_M2800W560_LH_2017.sigma = .01496 
WP_M2800W560_LH_2017.year = 2017
WP_M2800W560_LH_2017.dataset = "/Wprimetotb_M2800W560_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M2800W840_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 2.8TeV(30%) RH", "WP_M2800W840_LH_2017")
WP_M2800W840_LH_2017.sigma = .01115 
WP_M2800W840_LH_2017.year = 2017
WP_M2800W840_LH_2017.dataset = "/Wprimetotb_M2800W840_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M3200W320_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 3.2TeV(10%) RH", "WP_M3200W320_LH_2017")
WP_M3200W320_LH_2017.sigma = .01197 
WP_M3200W320_LH_2017.year = 2017
WP_M3200W320_LH_2017.dataset = "/Wprimetotb_M3200W320_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M3200W640_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 3.2TeV(20%) RH", "WP_M3200W640_LH_2017")
WP_M3200W640_LH_2017.sigma = .007494 
WP_M3200W640_LH_2017.year = 2017
WP_M3200W640_LH_2017.dataset = "/Wprimetotb_M3200W640_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M3200W960_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 3.2TeV(30%) RH", "WP_M3200W960_LH_2017")
WP_M3200W960_LH_2017.sigma = .005784 
WP_M3200W960_LH_2017.year = 2017
WP_M3200W960_LH_2017.dataset = "/Wprimetotb_M3200W960_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M3600W360_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 3.6TeV(10%) RH", "WP_M3600W360_LH_2017")
WP_M3600W360_LH_2017.sigma = .005971 
WP_M3600W360_LH_2017.year = 2017
WP_M3600W360_LH_2017.dataset = "/Wprimetotb_M3600W360_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M3600W720_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 3.6TeV(20%) RH", "WP_M3600W720_LH_2017")
WP_M3600W720_LH_2017.sigma = .004044 
WP_M3600W720_LH_2017.year = 2017
WP_M3600W720_LH_2017.dataset = "/Wprimetotb_M3600W720_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M3600W1080_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 3.6TeV(30%) RH", "WP_M3600W1080_LH_2017")
WP_M3600W1080_LH_2017.sigma = .003249 
WP_M3600W1080_LH_2017.year = 2017
WP_M3600W1080_LH_2017.dataset = "/Wprimetotb_M3600W1080_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M4000W400_LH_2017 = sample(ROOT.kMagenta, 1, 1001, "W' 4.0TeV(10%) RH", "WP_M4000W400_LH_2017")
WP_M4000W400_LH_2017.sigma = .003271 
WP_M4000W400_LH_2017.year = 2017
WP_M4000W400_LH_2017.dataset = "/Wprimetotb_M4000W400_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M4000W800_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 4.0TeV(20%) RH", "WP_M4000W800_LH_2017")
WP_M4000W800_LH_2017.sigma = .002355 
WP_M4000W800_LH_2017.year = 2017
WP_M4000W800_LH_2017.dataset = "/Wprimetotb_M4000W800_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M4000W1200_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 4.0TeV(30%) RH", "WP_M4000W1200_LH_2017")
WP_M4000W1200_LH_2017.sigma = .00195 
WP_M4000W1200_LH_2017.year = 2017
WP_M4000W1200_LH_2017.dataset = "/Wprimetotb_M4000W1200_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M4400W440_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 4.4TeV(10%) RH", "WP_M4400W440_LH_2017")
WP_M4400W440_LH_2017.sigma = .001899 
WP_M4400W440_LH_2017.year = 2017
WP_M4400W440_LH_2017.dataset = "/Wprimetotb_M4400W440_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M4400W880_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 4.4TeV(20%) RH", "WP_M4400W880_LH_2017")
WP_M4400W880_LH_2017.sigma = .001437 
WP_M4400W880_LH_2017.year = 2017
WP_M4400W880_LH_2017.dataset = "/Wprimetotb_M4400W880_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M4400W1320_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 4.4TeV(30%) RH", "WP_M4400W1320_LH_2017")
WP_M4400W1320_LH_2017.sigma = .001232 
WP_M4400W1320_LH_2017.year = 2017
WP_M4400W1320_LH_2017.dataset = "/Wprimetotb_M4400W1320_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M4800W480_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 4.8TeV(10%) RH", "WP_M4800W480_LH_2017")
WP_M4800W480_LH_2017.sigma = .001173 
WP_M4800W480_LH_2017.year = 2017
WP_M4800W480_LH_2017.dataset = "/Wprimetotb_M4800W480_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M4800W960_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 4.8TeV(20%) RH", "WP_M4800W960_LH_2017")
WP_M4800W960_LH_2017.sigma = .00094 
WP_M4800W960_LH_2017.year = 2017
WP_M4800W960_LH_2017.dataset = "/Wprimetotb_M4800W960_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M4800W1440_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 4.8TeV(30%) RH", "WP_M4800W1440_LH_2017")
WP_M4800W1440_LH_2017.sigma = .0008208 
WP_M4800W1440_LH_2017.year = 2017
WP_M4800W1440_LH_2017.dataset = "/Wprimetotb_M4800W1440_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M5200W520_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 5.2TeV(10%) RH", "WP_M5200W520_LH_2017")
WP_M5200W520_LH_2017.sigma = .0007642 
WP_M5200W520_LH_2017.year = 2017
WP_M5200W520_LH_2017.dataset = "/Wprimetotb_M5200W520_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M5200W1040_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 5.2TeV(20%) RH", "WP_M5200W1040_LH_2017")
WP_M5200W1040_LH_2017.sigma = .0006335 
WP_M5200W1040_LH_2017.year = 2017
WP_M5200W1040_LH_2017.dataset = "/Wprimetotb_M5200W1040_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M5200W1560_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 5.2TeV(30%) RH", "WP_M5200W1560_LH_2017")
WP_M5200W1560_LH_2017.sigma = .0005667 
WP_M5200W1560_LH_2017.year = 2017
WP_M5200W1560_LH_2017.dataset = "/Wprimetotb_M5200W1560_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M5600W560_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 5.6TeV(10%) RH", "WP_M5600W560_LH_2017")
WP_M5600W560_LH_2017.sigma = .000518 
WP_M5600W560_LH_2017.year = 2017
WP_M5600W560_LH_2017.dataset = "/Wprimetotb_M5600W560_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M5600W1120_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 5.6TeV(20%) RH", "WP_M5600W1120_LH_2017")
WP_M5600W1120_LH_2017.sigma = .000449 
WP_M5600W1120_LH_2017.year = 2017
WP_M5600W1120_LH_2017.dataset = "/Wprimetotb_M5600W1120_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M5600W1680_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 5.6TeV(30%) RH", "WP_M5600W1680_LH_2017")
WP_M5600W1680_LH_2017.sigma = .0004055 
WP_M5600W1680_LH_2017.year = 2017
WP_M5600W1680_LH_2017.dataset = "/Wprimetotb_M5600W1680_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M6000W600_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 6.0TeV(10%) RH", "WP_M6000W600_LH_2017")
WP_M6000W600_LH_2017.sigma = .0003715 
WP_M6000W600_LH_2017.year = 2017
WP_M6000W600_LH_2017.dataset = "/Wprimetotb_M6000W600_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M6000W1200_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 6.0TeV(20%) RH", "WP_M6000W1200_LH_2017")
WP_M6000W1200_LH_2017.sigma = .0003255 
WP_M6000W1200_LH_2017.year = 2017
WP_M6000W1200_LH_2017.dataset = "/Wprimetotb_M6000W1200_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M6000W1800_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 6.0TeV(30%) RH", "WP_M6000W1800_LH_2017")
WP_M6000W1800_LH_2017.sigma = .0002973 
WP_M6000W1800_LH_2017.year = 2017
WP_M6000W1800_LH_2017.dataset = "/Wprimetotb_M6000W1800_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M2000W20_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 2.0TeV(1%) RH", "WP_M2000W20_LH_2017")
WP_M2000W20_LH_2017.sigma = 1.342 
WP_M2000W20_LH_2017.year = 2017
WP_M2000W20_LH_2017.dataset = "/Wprimetotb_M2000W20_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M2200W22_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 2.2TeV(1%) RH", "WP_M2200W22_LH_2017")
WP_M2200W22_LH_2017.sigma = .8111 
WP_M2200W22_LH_2017.year = 2017
WP_M2200W22_LH_2017.dataset = "/Wprimetotb_M2200W22_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M2400W24_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 2.4TeV(1%) RH", "WP_M2400W24_LH_2017")
WP_M2400W24_LH_2017.sigma = .5005 
WP_M2400W24_LH_2017.year = 2017
WP_M2400W24_LH_2017.dataset = "/Wprimetotb_M2400W24_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M2600W26_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 2.6TeV(1%) RH", "WP_M2600W26_LH_2017")
WP_M2600W26_LH_2017.sigma = .3115 
WP_M2600W26_LH_2017.year = 2017
WP_M2600W26_LH_2017.dataset = "/Wprimetotb_M2600W26_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M2800W28_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 2.8TeV(1%) RH", "WP_M2800W28_LH_2017")
WP_M2800W28_LH_2017.sigma = .1974 
WP_M2800W28_LH_2017.year = 2017
WP_M2800W28_LH_2017.dataset = "/Wprimetotb_M2800W28_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M3000W30_LH_2017 = sample(ROOT.kMagenta+2, 1, 1001, "W' 3.0TeV(1%) RH", "WP_M3000W30_LH_2017")
WP_M3000W30_LH_2017.sigma = .1271 
WP_M3000W30_LH_2017.year = 2017
WP_M3000W30_LH_2017.dataset = "/Wprimetotb_M3000W30_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M3200W32_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 3.2TeV(1%) RH", "WP_M3200W32_LH_2017")
WP_M3200W32_LH_2017.sigma = .08254 
WP_M3200W32_LH_2017.year = 2017
WP_M3200W32_LH_2017.dataset = "/Wprimetotb_M3200W32_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M3400W34_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 3.4TeV(1%) RH", "WP_M3400W34_LH_2017")
WP_M3400W34_LH_2017.sigma = .0544 
WP_M3400W34_LH_2017.year = 2017
WP_M3400W34_LH_2017.dataset = "/Wprimetotb_M3400W34_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M3600W36_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 3.6TeV(1%) RH", "WP_M3600W36_LH_2017")
WP_M3600W36_LH_2017.sigma = .03624 
WP_M3600W36_LH_2017.year = 2017
WP_M3600W36_LH_2017.dataset = "/Wprimetotb_M3600W36_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M3800W38_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 3.8TeV(1%) RH", "WP_M3800W38_LH_2017")
WP_M3800W38_LH_2017.sigma = .02449 
WP_M3800W38_LH_2017.year = 2017
WP_M3800W38_LH_2017.dataset = "/Wprimetotb_M3800W38_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M4000W40_LH_2017 = sample(ROOT.kGreen+2, 1, 1001, "W' 4.0TeV(1%) RH", "WP_M4000W40_LH_2017")
WP_M4000W40_LH_2017.sigma = .01679 
WP_M4000W40_LH_2017.year = 2017
WP_M4000W40_LH_2017.dataset = "/Wprimetotb_M4000W40_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M4200W42_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 4.2TeV(1%) RH", "WP_M4200W42_LH_2017")
WP_M4200W42_LH_2017.sigma = .01161 
WP_M4200W42_LH_2017.year = 2017
WP_M4200W42_LH_2017.dataset = "/Wprimetotb_M4200W42_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M4400W44_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 4.4TeV(1%) RH", "WP_M4400W44_LH_2017")
WP_M4400W44_LH_2017.sigma = .008501 
WP_M4400W44_LH_2017.year = 2017
WP_M4400W44_LH_2017.dataset = "/Wprimetotb_M4400W44_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M4600W46_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 4.6TeV(1%) RH", "WP_M4600W46_LH_2017")
WP_M4600W46_LH_2017.sigma = .006172 
WP_M4600W46_LH_2017.year = 2017
WP_M4600W46_LH_2017.dataset = "/Wprimetotb_M4600W46_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M4800W48_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 4.8TeV(1%) RH", "WP_M4800W48_LH_2017")
WP_M4800W48_LH_2017.sigma = .004538 
WP_M4800W48_LH_2017.year = 2017
WP_M4800W48_LH_2017.dataset = "/Wprimetotb_M4800W48_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M5000W50_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 5.0TeV(1%) RH", "WP_M5000W50_LH_2017")
WP_M5000W50_LH_2017.sigma = .003381 
WP_M5000W50_LH_2017.year = 2017
WP_M5000W50_LH_2017.dataset = "/Wprimetotb_M5000W50_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M5200W52_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 5.2TeV(1%) RH", "WP_M5200W52_LH_2017")
WP_M5200W52_LH_2017.sigma = .00254 
WP_M5200W52_LH_2017.year = 2017
WP_M5200W52_LH_2017.dataset = "/Wprimetotb_M5200W52_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M5400W54_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 5.4TeV(1%) RH", "WP_M5400W54_LH_2017")
WP_M5400W54_LH_2017.sigma = .001929 
WP_M5400W54_LH_2017.year = 2017
WP_M5400W54_LH_2017.dataset = "/Wprimetotb_M5400W54_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M5600W56_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 5.6TeV(1%) RH", "WP_M5600W56_LH_2017")
WP_M5600W56_LH_2017.sigma = .001476 
WP_M5600W56_LH_2017.year = 2017
WP_M5600W56_LH_2017.dataset = "/Wprimetotb_M5600W56_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M5800W58_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 5.8TeV(1%) RH", "WP_M5800W58_LH_2017")
WP_M5800W58_LH_2017.sigma = .001138 
WP_M5800W58_LH_2017.year = 2017
WP_M5800W58_LH_2017.dataset = "/Wprimetotb_M5800W58_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M6000W60_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 6.0TeV(1%) RH", "WP_M6000W60_LH_2017")
WP_M6000W60_LH_2017.sigma = .0008807 
WP_M6000W60_LH_2017.year = 2017
WP_M6000W60_LH_2017.dataset = "/Wprimetotb_M6000W60_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_LH_2017 = sample(ROOT.kBlue, 1, 1001, "W' LH", "WP_LH_2017")
WP_LH_2017.year = 2017
WP_LH_2017.components = [WP_M2000W200_LH_2017, WP_M2000W400_LH_2017, WP_M2000W600_LH_2017, WP_M2400W240_LH_2017, WP_M2400W480_LH_2017, WP_M2400W720_LH_2017, WP_M2800W280_LH_2017, WP_M2800W560_LH_2017, WP_M2800W840_LH_2017, WP_M3200W320_LH_2017, WP_M3200W640_LH_2017, WP_M3200W960_LH_2017, WP_M3600W360_LH_2017, WP_M3600W720_LH_2017, WP_M3600W1080_LH_2017, WP_M4000W400_LH_2017, WP_M4000W800_LH_2017, WP_M4000W1200_LH_2017, WP_M4400W440_LH_2017, WP_M4400W880_LH_2017, WP_M4400W1320_LH_2017, WP_M4800W480_LH_2017, WP_M4800W960_LH_2017, WP_M4800W1440_LH_2017, WP_M5200W520_LH_2017, WP_M5200W1040_LH_2017, WP_M5200W1560_LH_2017, WP_M5600W560_LH_2017, WP_M5600W1120_LH_2017, WP_M5600W1680_LH_2017, WP_M6000W600_LH_2017, WP_M6000W1200_LH_2017, WP_M6000W1800_LH_2017, WP_M2000W20_LH_2017, WP_M2200W22_LH_2017, WP_M2400W24_LH_2017, WP_M2600W26_LH_2017, WP_M2800W28_LH_2017, WP_M3000W30_LH_2017, WP_M3200W32_LH_2017, WP_M3400W34_LH_2017, WP_M3600W36_LH_2017, WP_M3800W38_LH_2017, WP_M4000W40_LH_2017, WP_M4200W42_LH_2017, WP_M4400W44_LH_2017, WP_M4600W46_LH_2017, WP_M4800W48_LH_2017, WP_M5000W50_LH_2017, WP_M5200W52_LH_2017, WP_M5400W54_LH_2017, WP_M5600W56_LH_2017, WP_M5800W58_LH_2017, WP_M6000W60_LH_2017]

################################ Signal Sample RH ################################
WP_M2000W200_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 2.0TeV(10%) RH", "WP_M2000W200_RH_2017")
WP_M2000W200_RH_2017.sigma = .154 
WP_M2000W200_RH_2017.year = 2017
WP_M2000W200_RH_2017.dataset = "/Wprimetotb_M2000W200_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M2000W400_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 2.0TeV(20%) RH", "WP_M2000W400_RH_2017")
WP_M2000W400_RH_2017.sigma = .08177 
WP_M2000W400_RH_2017.year = 2017
WP_M2000W400_RH_2017.dataset = "/Wprimetotb_M2000W400_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M2000W600_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 2.0TeV(30%) RH", "WP_M2000W600_RH_2017")
WP_M2000W600_RH_2017.sigma = .05617 
WP_M2000W600_RH_2017.year = 2017
WP_M2000W600_RH_2017.dataset = "/Wprimetotb_M2000W600_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M2400W240_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 2.4TeV(10%) RH", "WP_M2400W240_RH_2017")
WP_M2400W240_RH_2017.sigma = .06106 
WP_M2400W240_RH_2017.year = 2017
WP_M2400W240_RH_2017.dataset = "/Wprimetotb_M2400W240_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M2400W480_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 2.4TeV(20%) RH", "WP_M2400W480_RH_2017")
WP_M2400W480_RH_2017.sigma = .03416 
WP_M2400W480_RH_2017.year = 2017
WP_M2400W480_RH_2017.dataset = "/Wprimetotb_M2400W480_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M2400W720_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 2.4TeV(30%) RH", "WP_M2400W720_RH_2017")
WP_M2400W720_RH_2017.sigma = .02404 
WP_M2400W720_RH_2017.year = 2017
WP_M2400W720_RH_2017.dataset = "/Wprimetotb_M2400W720_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M2800W280_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 2.8TeV(10%) RH", "WP_M2800W280_RH_2017")
WP_M2800W280_RH_2017.sigma = .02655 
WP_M2800W280_RH_2017.year = 2017
WP_M2800W280_RH_2017.dataset = "/Wprimetotb_M2800W280_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M2800W560_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 2.8TeV(20%) RH", "WP_M2800W560_RH_2017")
WP_M2800W560_RH_2017.sigma = .01554 
WP_M2800W560_RH_2017.year = 2017
WP_M2800W560_RH_2017.dataset = "/Wprimetotb_M2800W560_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M2800W840_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 2.8TeV(30%) RH", "WP_M2800W840_RH_2017")
WP_M2800W840_RH_2017.sigma = .01158 
WP_M2800W840_RH_2017.year = 2017
WP_M2800W840_RH_2017.dataset = "/Wprimetotb_M2800W840_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M3200W320_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 3.2TeV(10%) RH", "WP_M3200W320_RH_2017")
WP_M3200W320_RH_2017.sigma = .01242 
WP_M3200W320_RH_2017.year = 2017
WP_M3200W320_RH_2017.dataset = "/Wprimetotb_M3200W320_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M3200W640_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 3.2TeV(20%) RH", "WP_M3200W640_RH_2017")
WP_M3200W640_RH_2017.sigma = .007778 
WP_M3200W640_RH_2017.year = 2017
WP_M3200W640_RH_2017.dataset = "/Wprimetotb_M3200W640_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M3200W960_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 3.2TeV(30%) RH", "WP_M3200W960_RH_2017")
WP_M3200W960_RH_2017.sigma = .006004 
WP_M3200W960_RH_2017.year = 2017
WP_M3200W960_RH_2017.dataset = "/Wprimetotb_M3200W960_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M3600W360_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 3.6TeV(10%) RH", "WP_M3600W360_RH_2017")
WP_M3600W360_RH_2017.sigma = .006191 
WP_M3600W360_RH_2017.year = 2017
WP_M3600W360_RH_2017.dataset = "/Wprimetotb_M3600W360_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M3600W720_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 3.6TeV(20%) RH", "WP_M3600W720_RH_2017")
WP_M3600W720_RH_2017.sigma = .004195 
WP_M3600W720_RH_2017.year = 2017
WP_M3600W720_RH_2017.dataset = "/Wprimetotb_M3600W720_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M3600W1080_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 3.6TeV(30%) RH", "WP_M3600W1080_RH_2017")
WP_M3600W1080_RH_2017.sigma = .003372 
WP_M3600W1080_RH_2017.year = 2017
WP_M3600W1080_RH_2017.dataset = "/Wprimetotb_M3600W1080_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M4000W400_RH_2017 = sample(ROOT.kMagenta, 1, 1001, "W' 4.0TeV(10%) RH", "WP_M4000W400_RH_2017")
WP_M4000W400_RH_2017.sigma = .00339 
WP_M4000W400_RH_2017.year = 2017
WP_M4000W400_RH_2017.dataset = "/Wprimetotb_M4000W400_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M4000W800_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 4.0TeV(20%) RH", "WP_M4000W800_RH_2017")
WP_M4000W800_RH_2017.sigma = .002443 
WP_M4000W800_RH_2017.year = 2017
WP_M4000W800_RH_2017.dataset = "/Wprimetotb_M4000W800_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M4000W1200_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 4.0TeV(30%) RH", "WP_M4000W1200_RH_2017")
WP_M4000W1200_RH_2017.sigma = .002024 
WP_M4000W1200_RH_2017.year = 2017
WP_M4000W1200_RH_2017.dataset = "/Wprimetotb_M4000W1200_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M4400W440_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 4.4TeV(10%) RH", "WP_M4400W440_RH_2017")
WP_M4400W440_RH_2017.sigma = .001967 
WP_M4400W440_RH_2017.year = 2017
WP_M4400W440_RH_2017.dataset = "/Wprimetotb_M4400W440_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M4400W880_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 4.4TeV(20%) RH", "WP_M4400W880_RH_2017")
WP_M4400W880_RH_2017.sigma = .001491 
WP_M4400W880_RH_2017.year = 2017
WP_M4400W880_RH_2017.dataset = "/Wprimetotb_M4400W880_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M4400W1320_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 4.4TeV(30%) RH", "WP_M4400W1320_RH_2017")
WP_M4400W1320_RH_2017.sigma = .001278 
WP_M4400W1320_RH_2017.year = 2017
WP_M4400W1320_RH_2017.dataset = "/Wprimetotb_M4400W1320_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M4800W480_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 4.8TeV(10%) RH", "WP_M4800W480_RH_2017")
WP_M4800W480_RH_2017.sigma = .001217 
WP_M4800W480_RH_2017.year = 2017
WP_M4800W480_RH_2017.dataset = "/Wprimetotb_M4800W480_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M4800W960_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 4.8TeV(20%) RH", "WP_M4800W960_RH_2017")
WP_M4800W960_RH_2017.sigma = .0009753 
WP_M4800W960_RH_2017.year = 2017
WP_M4800W960_RH_2017.dataset = "/Wprimetotb_M4800W960_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M4800W1440_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 4.8TeV(30%) RH", "WP_M4800W1440_RH_2017")
WP_M4800W1440_RH_2017.sigma = .0008519 
WP_M4800W1440_RH_2017.year = 2017
WP_M4800W1440_RH_2017.dataset = "/Wprimetotb_M4800W1440_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M5200W520_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 5.2TeV(10%) RH", "WP_M5200W520_RH_2017")
WP_M5200W520_RH_2017.sigma = .0007929 
WP_M5200W520_RH_2017.year = 2017
WP_M5200W520_RH_2017.dataset = "/Wprimetotb_M5200W520_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M5200W1040_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 5.2TeV(20%) RH", "WP_M5200W1040_RH_2017")
WP_M5200W1040_RH_2017.sigma = .0006573 
WP_M5200W1040_RH_2017.year = 2017
WP_M5200W1040_RH_2017.dataset = "/Wprimetotb_M5200W1040_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M5200W1560_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 5.2TeV(30%) RH", "WP_M5200W1560_RH_2017")
WP_M5200W1560_RH_2017.sigma = .0005882 
WP_M5200W1560_RH_2017.year = 2017
WP_M5200W1560_RH_2017.dataset = "/Wprimetotb_M5200W1560_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M5600W560_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 5.6TeV(10%) RH", "WP_M5600W560_RH_2017")
WP_M5600W560_RH_2017.sigma = .0005376 
WP_M5600W560_RH_2017.year = 2017
WP_M5600W560_RH_2017.dataset = "/Wprimetotb_M5600W560_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M5600W1120_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 5.6TeV(20%) RH", "WP_M5600W1120_RH_2017")
WP_M5600W1120_RH_2017.sigma = .000466 
WP_M5600W1120_RH_2017.year = 2017
WP_M5600W1120_RH_2017.dataset = "/Wprimetotb_M5600W1120_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M5600W1680_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 5.6TeV(30%) RH", "WP_M5600W1680_RH_2017")
WP_M5600W1680_RH_2017.sigma = .0004209 
WP_M5600W1680_RH_2017.year = 2017
WP_M5600W1680_RH_2017.dataset = "/Wprimetotb_M5600W1680_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M6000W600_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 6.0TeV(10%) RH", "WP_M6000W600_RH_2017")
WP_M6000W600_RH_2017.sigma = .0003858 
WP_M6000W600_RH_2017.year = 2017
WP_M6000W600_RH_2017.dataset = "/Wprimetotb_M6000W600_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M6000W1200_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 6.0TeV(20%) RH", "WP_M6000W1200_RH_2017")
WP_M6000W1200_RH_2017.sigma = .000338 
WP_M6000W1200_RH_2017.year = 2017
WP_M6000W1200_RH_2017.dataset = "/Wprimetotb_M6000W1200_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M6000W1800_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 6.0TeV(30%) RH", "WP_M6000W1800_RH_2017")
WP_M6000W1800_RH_2017.sigma = .0003086 
WP_M6000W1800_RH_2017.year = 2017
WP_M6000W1800_RH_2017.dataset = "/Wprimetotb_M6000W1800_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M2000W20_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 2.0TeV(1%) RH", "WP_M2000W20_RH_2017")
WP_M2000W20_RH_2017.sigma = 1.397 
WP_M2000W20_RH_2017.year = 2017
WP_M2000W20_RH_2017.dataset = "/Wprimetotb_M2000W20_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M2200W22_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 2.2TeV(1%) RH", "WP_M2200W22_RH_2017")
WP_M2200W22_RH_2017.sigma = .8439 
WP_M2200W22_RH_2017.year = 2017
WP_M2200W22_RH_2017.dataset = "/Wprimetotb_M2200W22_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M2400W24_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 2.4TeV(1%) RH", "WP_M2400W24_RH_2017")
WP_M2400W24_RH_2017.sigma = .5203 
WP_M2400W24_RH_2017.year = 2017
WP_M2400W24_RH_2017.dataset = "/Wprimetotb_M2400W24_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M2600W26_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 2.6TeV(1%) RH", "WP_M2600W26_RH_2017")
WP_M2600W26_RH_2017.sigma = .3236 
WP_M2600W26_RH_2017.year = 2017
WP_M2600W26_RH_2017.dataset = "/Wprimetotb_M2600W26_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M2800W28_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 2.8TeV(1%) RH", "WP_M2800W28_RH_2017")
WP_M2800W28_RH_2017.sigma = .2049 
WP_M2800W28_RH_2017.year = 2017
WP_M2800W28_RH_2017.dataset = "/Wprimetotb_M2800W28_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M3000W30_RH_2017 = sample(ROOT.kAzure, 1, 1001, "W' 3.0TeV(1%) RH", "WP_M3000W30_RH_2017")
WP_M3000W30_RH_2017.sigma = .1318 
WP_M3000W30_RH_2017.year = 2017
WP_M3000W30_RH_2017.dataset = "/Wprimetotb_M3000W30_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M3200W32_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 3.2TeV(1%) RH", "WP_M3200W32_RH_2017")
WP_M3200W32_RH_2017.sigma = .08553 
WP_M3200W32_RH_2017.year = 2017
WP_M3200W32_RH_2017.dataset = "/Wprimetotb_M3200W32_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M3400W34_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 3.4TeV(1%) RH", "WP_M3400W34_RH_2017")
WP_M3400W34_RH_2017.sigma = .05633 
WP_M3400W34_RH_2017.year = 2017
WP_M3400W34_RH_2017.dataset = "/Wprimetotb_M3400W34_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M3600W36_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 3.6TeV(1%) RH", "WP_M3600W36_RH_2017")
WP_M3600W36_RH_2017.sigma = .0375 
WP_M3600W36_RH_2017.year = 2017
WP_M3600W36_RH_2017.dataset = "/Wprimetotb_M3600W36_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M3800W38_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 3.8TeV(1%) RH", "WP_M3800W38_RH_2017")
WP_M3800W38_RH_2017.sigma = .02533 
WP_M3800W38_RH_2017.year = 2017
WP_M3800W38_RH_2017.dataset = "/Wprimetotb_M3800W38_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M4000W40_RH_2017 = sample(ROOT.kGreen+2, 1, 1001, "W' 4.0TeV(1%) RH", "WP_M4000W40_RH_2017")
WP_M4000W40_RH_2017.sigma = .01736 
WP_M4000W40_RH_2017.year = 2017
WP_M4000W40_RH_2017.dataset = "/Wprimetotb_M4000W40_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M4200W42_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 4.2TeV(1%) RH", "WP_M4200W42_RH_2017")
WP_M4200W42_RH_2017.sigma = .01208 
WP_M4200W42_RH_2017.year = 2017
WP_M4200W42_RH_2017.dataset = "/Wprimetotb_M4200W42_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M4400W44_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 4.4TeV(1%) RH", "WP_M4400W44_RH_2017")
WP_M4400W44_RH_2017.sigma = .00879 
WP_M4400W44_RH_2017.year = 2017
WP_M4400W44_RH_2017.dataset = "/Wprimetotb_M4400W44_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M4600W46_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 4.6TeV(1%) RH", "WP_M4600W46_RH_2017")
WP_M4600W46_RH_2017.sigma = .006384 
WP_M4600W46_RH_2017.year = 2017
WP_M4600W46_RH_2017.dataset = "/Wprimetotb_M4600W46_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M4800W48_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 4.8TeV(1%) RH", "WP_M4800W48_RH_2017")
WP_M4800W48_RH_2017.sigma = .004696 
WP_M4800W48_RH_2017.year = 2017
WP_M4800W48_RH_2017.dataset = "/Wprimetotb_M4800W48_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M5000W50_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 5.0TeV(1%) RH", "WP_M5000W50_RH_2017")
WP_M5000W50_RH_2017.sigma = .003501 
WP_M5000W50_RH_2017.year = 2017
WP_M5000W50_RH_2017.dataset = "/Wprimetotb_M5000W50_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M5200W52_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 5.2TeV(1%) RH", "WP_M5200W52_RH_2017")
WP_M5200W52_RH_2017.sigma = .002633 
WP_M5200W52_RH_2017.year = 2017
WP_M5200W52_RH_2017.dataset = "/Wprimetotb_M5200W52_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M5400W54_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 5.4TeV(1%) RH", "WP_M5400W54_RH_2017")
WP_M5400W54_RH_2017.sigma = .002008 
WP_M5400W54_RH_2017.year = 2017
WP_M5400W54_RH_2017.dataset = "/Wprimetotb_M5400W54_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M5600W56_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 5.6TeV(1%) RH", "WP_M5600W56_RH_2017")
WP_M5600W56_RH_2017.sigma = .001533 
WP_M5600W56_RH_2017.year = 2017
WP_M5600W56_RH_2017.dataset = "/Wprimetotb_M5600W56_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M5800W58_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 5.8TeV(1%) RH", "WP_M5800W58_RH_2017")
WP_M5800W58_RH_2017.sigma = .001182 
WP_M5800W58_RH_2017.year = 2017
WP_M5800W58_RH_2017.dataset = "/Wprimetotb_M5800W58_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_M6000W60_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' 6.0TeV(1%) RH", "WP_M6000W60_RH_2017")
WP_M6000W60_RH_2017.sigma = .0009153 
WP_M6000W60_RH_2017.year = 2017
WP_M6000W60_RH_2017.dataset = "/Wprimetotb_M6000W60_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WP_RH_2017 = sample(ROOT.kBlue, 1, 1001, "W' RH", "WP_RH_2017")
WP_RH_2017.year = 2017
WP_RH_2017.components = [WP_M2000W200_RH_2017, WP_M2000W400_RH_2017, WP_M2000W600_RH_2017, WP_M2400W240_RH_2017, WP_M2400W480_RH_2017, WP_M2400W720_RH_2017, WP_M2800W280_RH_2017, WP_M2800W560_RH_2017, WP_M2800W840_RH_2017, WP_M3200W320_RH_2017, WP_M3200W640_RH_2017, WP_M3200W960_RH_2017, WP_M3600W360_RH_2017, WP_M3600W720_RH_2017, WP_M3600W1080_RH_2017, WP_M4000W400_RH_2017, WP_M4000W800_RH_2017, WP_M4000W1200_RH_2017, WP_M4400W440_RH_2017, WP_M4400W880_RH_2017, WP_M4400W1320_RH_2017, WP_M4800W480_RH_2017, WP_M4800W960_RH_2017, WP_M4800W1440_RH_2017, WP_M5200W520_RH_2017, WP_M5200W1040_RH_2017, WP_M5200W1560_RH_2017, WP_M5600W560_RH_2017, WP_M5600W1120_RH_2017, WP_M5600W1680_RH_2017, WP_M6000W600_RH_2017, WP_M6000W1200_RH_2017, WP_M6000W1800_RH_2017, WP_M2000W20_RH_2017, WP_M2200W22_RH_2017, WP_M2400W24_RH_2017, WP_M2600W26_RH_2017, WP_M2800W28_RH_2017, WP_M3000W30_RH_2017, WP_M3200W32_RH_2017, WP_M3400W34_RH_2017, WP_M3600W36_RH_2017, WP_M3800W38_RH_2017, WP_M4000W40_RH_2017, WP_M4200W42_RH_2017, WP_M4400W44_RH_2017, WP_M4600W46_RH_2017, WP_M4800W48_RH_2017, WP_M5000W50_RH_2017, WP_M5200W52_RH_2017, WP_M5400W54_RH_2017, WP_M5600W56_RH_2017, WP_M5800W58_RH_2017, WP_M6000W60_RH_2017]

###################################################################################################################################################################
############################################################                                           ############################################################
############################################################                    2018                   ############################################################
############################################################                                           ############################################################
###################################################################################################################################################################

################################ TTbar ################################
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

TT_semilep_2018 = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_semilep_2018")
TT_semilep_2018.sigma = 831.76*0.438 #pb
TT_semilep_2018.year = 2018
TT_semilep_2018.dataset = "/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/" + tag_2018 + "-v1/NANOAODSIM"

TT_Mtt_2018 = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_Mtt_2018")
TT_Mtt_2018.year = 2018
#TT_Mtt_2018.components = [TT_semilep_2018]
TT_Mtt_2018.components = [TT_Mtt700to1000_2018, TT_Mtt1000toInf_2018]

TT_dilep_2018 = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_dilep_2018")
TT_dilep_2018.sigma =  831.76 * 0.10 #pb
TT_dilep_2018.year = 2018
TT_dilep_2018.dataset = "/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/"+tag_2018+"-v1/NANOAODSIM"

################################ WJets ################################
WJetsHT200to400_2018 = sample(ROOT.kGreen+2, 1, 1001, "W + Jets", "WJetsHT200to400_2018")
WJetsHT200to400_2018.sigma = 359.7 * 1.21 #pb
WJetsHT200to400_2018.year = 2018
WJetsHT200to400_2018.dataset = "/WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2018+"-v1/NANOAODSIM"
#WJetsHT200to400_2018.files = jr.json_reader(path+"/WJets_HT200To400_2018.json")

WJetsHT400to600_2018 = sample(ROOT.kGreen+2, 1, 1001, "W + Jets", "WJetsHT400to600_2018")
WJetsHT400to600_2018.sigma = 48.91 * 1.21 #pb
WJetsHT400to600_2018.year = 2018
WJetsHT400to600_2018.dataset = "/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2018+"-v1/NANOAODSIM"
#WJetsHT400to600_2018.files = jr.json_reader(path+"/WJets_HT400To600_2018.json")

WJetsHT600to800_2018 = sample(ROOT.kGreen+2, 1, 1001, "W + Jets", "WJetsHT600to800_2018")
WJetsHT600to800_2018.sigma = 12.05 * 1.21 #pb
WJetsHT600to800_2018.year = 2018
WJetsHT600to800_2018.dataset = "/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2018+"-v1/NANOAODSIM"
#WJetsHT600to800_2018.files = jr.json_reader(path+"/WJets_HT600To800_2018.json")

WJetsHT800to1200_2018 = sample(ROOT.kGreen+2, 1, 1001, "W + Jets", "WJetsHT800to1200_2018")
WJetsHT800to1200_2018.sigma = 5.501 * 1.21 #pb
WJetsHT800to1200_2018.year = 2018
WJetsHT800to1200_2018.dataset = "/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2018+"-v1/NANOAODSIM"
#WJetsHT800to1200_2018.files = jr.json_reader(path+"/WJets_HT800To1200_2018.json")

WJetsHT1200to2500_2018 = sample(ROOT.kGreen+2, 1, 1001, "W + Jets", "WJetsHT1200to2500_2018")
WJetsHT1200to2500_2018.sigma = 1.329 * 1.21 #pb
WJetsHT1200to2500_2018.year = 2018
WJetsHT1200to2500_2018.dataset = "/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2018+"-v1/NANOAODSIM"
#WJetsHT1200to2500_2018.files = jr.json_reader(path+"/WJets_HT1200To2500_2018.json")

WJetsHT2500toInf_2018 = sample(ROOT.kGreen+2, 1, 1001, "W + Jets", "WJetsHT2500toInf_2018")
WJetsHT2500toInf_2018.sigma = 0.03216 * 1.2 #pb
WJetsHT2500toInf_2018.year = 2018
WJetsHT2500toInf_2018.dataset = "/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2018+"-v1/NANOAODSIM"
#WJetsHT2500toInf_2018.files = jr.json_reader(path+"/WJets_HT2500ToInf_2018.json")

WJets_2018 = sample(ROOT.kGreen+2, 1, 1001, "W + Jets", "WJets_2018")
WJets_2018.year = 2018
WJets_2018.components = [WJetsHT200to400_2018, WJetsHT400to600_2018, WJetsHT600to800_2018, WJetsHT800to1200_2018, WJetsHT1200to2500_2018, WJetsHT2500toInf_2018]

################################ Single Top ################################
ST_tch_t_2018 = sample(ROOT.kYellow, 1, 1001, "ST t-ch", "ST_tch_t_2018")
ST_tch_t_2018.sigma =  136.02 #pb
ST_tch_t_2018.year = 2018
ST_tch_t_2018.dataset = "/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/"+tag_2018+"-v1/NANOAODSIM"

ST_tch_tbar_2018 = sample(ROOT.kYellow, 1, 1001, "ST t-ch", "ST_tch_tbar_2018")
ST_tch_tbar_2018.sigma =  80.95 #pb
ST_tch_tbar_2018.year = 2018
ST_tch_tbar_2018.dataset = "/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/"+tag_2018+"-v1/NANOAODSIM"

ST_tW_t_2018 = sample(ROOT.kYellow, 1, 1001, "ST tW", "ST_tW_t_2018")
ST_tW_t_2018.sigma =  71.7/2 #pb
ST_tW_t_2018.year = 2018
ST_tW_t_2018.dataset = "/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/"+tag_2018+"_ext1-v1/NANOAODSIM"

ST_tW_tbar_2018 = sample(ROOT.kYellow, 1, 1001, "ST tW", "ST_tW_tbar_2018")
ST_tW_tbar_2018.sigma = 71.7/2 #pb
ST_tW_tbar_2018.year = 2018
ST_tW_tbar_2018.dataset = "/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/"+tag_2018+"_ext1-v1/NANOAODSIM"

ST_sch_2018 = sample(ROOT.kYellow, 1, 1001, "ST s-ch", "ST_sch_2018")
ST_sch_2018.sigma = 10.32*0.324 #pb
ST_sch_2018.year = 2018
ST_sch_2018.dataset = "/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/"+tag_2018+"-v1/NANOAODSIM"

ST_2018 = sample(ROOT.kYellow, 1, 1001, "Single top", "ST_2018")
ST_2018.year = 2018
ST_2018.components = [ST_tch_t_2018, ST_tch_tbar_2018, ST_tW_t_2018, ST_tW_tbar_2018, ST_sch_2018]

################################ QCD ################################
QCDHT_300to500_2018 = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_300to500_2018")
QCDHT_300to500_2018.sigma = 347700 #pb
QCDHT_300to500_2018.year = 2018
QCDHT_300to500_2018.dataset = "/QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2018+"-v1/NANOAODSIM"
QCDHT_500to700_2018 = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_500to700_2018")
QCDHT_500to700_2018.sigma = 32100 #pb
QCDHT_500to700_2018.year = 2018
QCDHT_500to700_2018.dataset = "/QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2018+"-v1/NANOAODSIM"
QCDHT_700to1000_2018 = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_700to1000_2018")
QCDHT_700to1000_2018.sigma = 6831 #pb
QCDHT_700to1000_2018.year = 2018
QCDHT_700to1000_2018.dataset = "/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2018+"-v1/NANOAODSIM"
QCDHT_1000to1500_2018 = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_1000to1500_2018")
QCDHT_1000to1500_2018.sigma = 1207 #pb
QCDHT_1000to1500_2018.year = 2018
QCDHT_1000to1500_2018.dataset = "/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2018+"-v1/NANOAODSIM"
QCDHT_1500to2000_2018 = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_1500to2000_2018")
QCDHT_1500to2000_2018.sigma = 119.9 #pb
QCDHT_1500to2000_2018.year = 2018
QCDHT_1500to2000_2018.dataset = "/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2018+"-v1/NANOAODSIM"
QCDHT_2000toInf_2018 = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_2000toInf_2018")
QCDHT_2000toInf_2018.sigma = 25.24 #pb
QCDHT_2000toInf_2018.year = 2018
QCDHT_2000toInf_2018.dataset = "/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2018+"-v1/NANOAODSIM"

QCD_2018 = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_2018")
QCD_2018.year = 2018
QCD_2018.components = [QCDHT_300to500_2018, QCDHT_500to700_2018, QCDHT_700to1000_2018, QCDHT_1000to1500_2018, QCDHT_1500to2000_2018, QCDHT_2000toInf_2018]

################################ Signal Sample LH w/o SM Interference ################################
WP_M2000W200_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 2.0TeV(10%) RH", "WP_M2000W200_LH_2018")
WP_M2000W200_LH_2018.sigma = .148 
WP_M2000W200_LH_2018.year = 2018
WP_M2000W200_LH_2018.dataset = "/Wprimetotb_M2000W200_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M2000W400_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 2.0TeV(20%) RH", "WP_M2000W400_LH_2018")
WP_M2000W400_LH_2018.sigma = .07863 
WP_M2000W400_LH_2018.year = 2018
WP_M2000W400_LH_2018.dataset = "/Wprimetotb_M2000W400_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M2000W600_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 2.0TeV(30%) RH", "WP_M2000W600_LH_2018")
WP_M2000W600_LH_2018.sigma = .05403 
WP_M2000W600_LH_2018.year = 2018
WP_M2000W600_LH_2018.dataset = "/Wprimetotb_M2000W600_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M2400W240_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 2.4TeV(10%) RH", "WP_M2400W240_LH_2018")
WP_M2400W240_LH_2018.sigma = .05875 
WP_M2400W240_LH_2018.year = 2018
WP_M2400W240_LH_2018.dataset = "/Wprimetotb_M2400W240_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M2400W480_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 2.4TeV(20%) RH", "WP_M2400W480_LH_2018")
WP_M2400W480_LH_2018.sigma = .03287 
WP_M2400W480_LH_2018.year = 2018
WP_M2400W480_LH_2018.dataset = "/Wprimetotb_M2400W480_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M2400W720_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 2.4TeV(30%) RH", "WP_M2400W720_LH_2018")
WP_M2400W720_LH_2018.sigma = .02314 
WP_M2400W720_LH_2018.year = 2018
WP_M2400W720_LH_2018.dataset = "/Wprimetotb_M2400W720_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M2800W280_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 2.8TeV(10%) RH", "WP_M2800W280_LH_2018")
WP_M2800W280_LH_2018.sigma = .02556 
WP_M2800W280_LH_2018.year = 2018
WP_M2800W280_LH_2018.dataset = "/Wprimetotb_M2800W280_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M2800W560_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 2.8TeV(20%) RH", "WP_M2800W560_LH_2018")
WP_M2800W560_LH_2018.sigma = .01496 
WP_M2800W560_LH_2018.year = 2018
WP_M2800W560_LH_2018.dataset = "/Wprimetotb_M2800W560_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M2800W840_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 2.8TeV(30%) RH", "WP_M2800W840_LH_2018")
WP_M2800W840_LH_2018.sigma = .01115 
WP_M2800W840_LH_2018.year = 2018
WP_M2800W840_LH_2018.dataset = "/Wprimetotb_M2800W840_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M3200W320_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 3.2TeV(10%) RH", "WP_M3200W320_LH_2018")
WP_M3200W320_LH_2018.sigma = .01197 
WP_M3200W320_LH_2018.year = 2018
WP_M3200W320_LH_2018.dataset = "/Wprimetotb_M3200W320_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M3200W640_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 3.2TeV(20%) RH", "WP_M3200W640_LH_2018")
WP_M3200W640_LH_2018.sigma = .007494 
WP_M3200W640_LH_2018.year = 2018
WP_M3200W640_LH_2018.dataset = "/Wprimetotb_M3200W640_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M3200W960_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 3.2TeV(30%) RH", "WP_M3200W960_LH_2018")
WP_M3200W960_LH_2018.sigma = .005784 
WP_M3200W960_LH_2018.year = 2018
WP_M3200W960_LH_2018.dataset = "/Wprimetotb_M3200W960_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M3600W360_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 3.6TeV(10%) RH", "WP_M3600W360_LH_2018")
WP_M3600W360_LH_2018.sigma = .005971 
WP_M3600W360_LH_2018.year = 2018
WP_M3600W360_LH_2018.dataset = "/Wprimetotb_M3600W360_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M3600W720_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 3.6TeV(20%) RH", "WP_M3600W720_LH_2018")
WP_M3600W720_LH_2018.sigma = .004044 
WP_M3600W720_LH_2018.year = 2018
WP_M3600W720_LH_2018.dataset = "/Wprimetotb_M3600W720_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M3600W1080_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 3.6TeV(30%) RH", "WP_M3600W1080_LH_2018")
WP_M3600W1080_LH_2018.sigma = .003249 
WP_M3600W1080_LH_2018.year = 2018
WP_M3600W1080_LH_2018.dataset = "/Wprimetotb_M3600W1080_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M4000W400_LH_2018 = sample(ROOT.kMagenta, 1, 1001, "W' 4.0TeV(10%) RH", "WP_M4000W400_LH_2018")
WP_M4000W400_LH_2018.sigma = .003271 
WP_M4000W400_LH_2018.year = 2018
WP_M4000W400_LH_2018.dataset = "/Wprimetotb_M4000W400_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M4000W800_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 4.0TeV(20%) RH", "WP_M4000W800_LH_2018")
WP_M4000W800_LH_2018.sigma = .002355 
WP_M4000W800_LH_2018.year = 2018
WP_M4000W800_LH_2018.dataset = "/Wprimetotb_M4000W800_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M4000W1200_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 4.0TeV(30%) RH", "WP_M4000W1200_LH_2018")
WP_M4000W1200_LH_2018.sigma = .00195 
WP_M4000W1200_LH_2018.year = 2018
WP_M4000W1200_LH_2018.dataset = "/Wprimetotb_M4000W1200_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M4400W440_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 4.4TeV(10%) RH", "WP_M4400W440_LH_2018")
WP_M4400W440_LH_2018.sigma = .001899 
WP_M4400W440_LH_2018.year = 2018
WP_M4400W440_LH_2018.dataset = "/Wprimetotb_M4400W440_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M4400W880_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 4.4TeV(20%) RH", "WP_M4400W880_LH_2018")
WP_M4400W880_LH_2018.sigma = .001437 
WP_M4400W880_LH_2018.year = 2018
WP_M4400W880_LH_2018.dataset = "/Wprimetotb_M4400W880_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M4400W1320_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 4.4TeV(30%) RH", "WP_M4400W1320_LH_2018")
WP_M4400W1320_LH_2018.sigma = .001232 
WP_M4400W1320_LH_2018.year = 2018
WP_M4400W1320_LH_2018.dataset = "/Wprimetotb_M4400W1320_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M4800W480_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 4.8TeV(10%) RH", "WP_M4800W480_LH_2018")
WP_M4800W480_LH_2018.sigma = .001173 
WP_M4800W480_LH_2018.year = 2018
WP_M4800W480_LH_2018.dataset = "/Wprimetotb_M4800W480_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M4800W960_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 4.8TeV(20%) RH", "WP_M4800W960_LH_2018")
WP_M4800W960_LH_2018.sigma = .00094 
WP_M4800W960_LH_2018.year = 2018
WP_M4800W960_LH_2018.dataset = "/Wprimetotb_M4800W960_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M4800W1440_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 4.8TeV(30%) RH", "WP_M4800W1440_LH_2018")
WP_M4800W1440_LH_2018.sigma = .0008208 
WP_M4800W1440_LH_2018.year = 2018
WP_M4800W1440_LH_2018.dataset = "/Wprimetotb_M4800W1440_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M5200W520_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 5.2TeV(10%) RH", "WP_M5200W520_LH_2018")
WP_M5200W520_LH_2018.sigma = .0007642 
WP_M5200W520_LH_2018.year = 2018
WP_M5200W520_LH_2018.dataset = "/Wprimetotb_M5200W520_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M5200W1040_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 5.2TeV(20%) RH", "WP_M5200W1040_LH_2018")
WP_M5200W1040_LH_2018.sigma = .0006335 
WP_M5200W1040_LH_2018.year = 2018
WP_M5200W1040_LH_2018.dataset = "/Wprimetotb_M5200W1040_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M5200W1560_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 5.2TeV(30%) RH", "WP_M5200W1560_LH_2018")
WP_M5200W1560_LH_2018.sigma = .0005667 
WP_M5200W1560_LH_2018.year = 2018
WP_M5200W1560_LH_2018.dataset = "/Wprimetotb_M5200W1560_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M5600W560_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 5.6TeV(10%) RH", "WP_M5600W560_LH_2018")
WP_M5600W560_LH_2018.sigma = .000518 
WP_M5600W560_LH_2018.year = 2018
WP_M5600W560_LH_2018.dataset = "/Wprimetotb_M5600W560_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M5600W1120_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 5.6TeV(20%) RH", "WP_M5600W1120_LH_2018")
WP_M5600W1120_LH_2018.sigma = .000449 
WP_M5600W1120_LH_2018.year = 2018
WP_M5600W1120_LH_2018.dataset = "/Wprimetotb_M5600W1120_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M5600W1680_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 5.6TeV(30%) RH", "WP_M5600W1680_LH_2018")
WP_M5600W1680_LH_2018.sigma = .0004055 
WP_M5600W1680_LH_2018.year = 2018
WP_M5600W1680_LH_2018.dataset = "/Wprimetotb_M5600W1680_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M6000W600_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 6.0TeV(10%) RH", "WP_M6000W600_LH_2018")
WP_M6000W600_LH_2018.sigma = .0003715 
WP_M6000W600_LH_2018.year = 2018
WP_M6000W600_LH_2018.dataset = "/Wprimetotb_M6000W600_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M6000W1200_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 6.0TeV(20%) RH", "WP_M6000W1200_LH_2018")
WP_M6000W1200_LH_2018.sigma = .0003255 
WP_M6000W1200_LH_2018.year = 2018
WP_M6000W1200_LH_2018.dataset = "/Wprimetotb_M6000W1200_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M6000W1800_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 6.0TeV(30%) RH", "WP_M6000W1800_LH_2018")
WP_M6000W1800_LH_2018.sigma = .0002973 
WP_M6000W1800_LH_2018.year = 2018
WP_M6000W1800_LH_2018.dataset = "/Wprimetotb_M6000W1800_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M2000W20_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 2.0TeV(1%) RH", "WP_M2000W20_LH_2018")
WP_M2000W20_LH_2018.sigma = 1.342 
WP_M2000W20_LH_2018.year = 2018
WP_M2000W20_LH_2018.dataset = "/Wprimetotb_M2000W20_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M2200W22_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 2.2TeV(1%) RH", "WP_M2200W22_LH_2018")
WP_M2200W22_LH_2018.sigma = .8111 
WP_M2200W22_LH_2018.year = 2018
WP_M2200W22_LH_2018.dataset = "/Wprimetotb_M2200W22_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M2400W24_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 2.4TeV(1%) RH", "WP_M2400W24_LH_2018")
WP_M2400W24_LH_2018.sigma = .5005 
WP_M2400W24_LH_2018.year = 2018
WP_M2400W24_LH_2018.dataset = "/Wprimetotb_M2400W24_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M2600W26_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 2.6TeV(1%) RH", "WP_M2600W26_LH_2018")
WP_M2600W26_LH_2018.sigma = .3115 
WP_M2600W26_LH_2018.year = 2018
WP_M2600W26_LH_2018.dataset = "/Wprimetotb_M2600W26_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M2800W28_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 2.8TeV(1%) RH", "WP_M2800W28_LH_2018")
WP_M2800W28_LH_2018.sigma = .1974 
WP_M2800W28_LH_2018.year = 2018
WP_M2800W28_LH_2018.dataset = "/Wprimetotb_M2800W28_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M3000W30_LH_2018 = sample(ROOT.kMagenta+2, 1, 1001, "W' 3.0TeV(1%) RH", "WP_M3000W30_LH_2018")
WP_M3000W30_LH_2018.sigma = .1271 
WP_M3000W30_LH_2018.year = 2018
WP_M3000W30_LH_2018.dataset = "/Wprimetotb_M3000W30_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M3200W32_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 3.2TeV(1%) RH", "WP_M3200W32_LH_2018")
WP_M3200W32_LH_2018.sigma = .08254 
WP_M3200W32_LH_2018.year = 2018
WP_M3200W32_LH_2018.dataset = "/Wprimetotb_M3200W32_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M3400W34_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 3.4TeV(1%) RH", "WP_M3400W34_LH_2018")
WP_M3400W34_LH_2018.sigma = .0544 
WP_M3400W34_LH_2018.year = 2018
WP_M3400W34_LH_2018.dataset = "/Wprimetotb_M3400W34_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M3600W36_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 3.6TeV(1%) RH", "WP_M3600W36_LH_2018")
WP_M3600W36_LH_2018.sigma = .03624 
WP_M3600W36_LH_2018.year = 2018
WP_M3600W36_LH_2018.dataset = "/Wprimetotb_M3600W36_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M3800W38_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 3.8TeV(1%) RH", "WP_M3800W38_LH_2018")
WP_M3800W38_LH_2018.sigma = .02449 
WP_M3800W38_LH_2018.year = 2018
WP_M3800W38_LH_2018.dataset = "/Wprimetotb_M3800W38_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M4000W40_LH_2018 = sample(ROOT.kGreen+2, 1, 1001, "W' 4.0TeV(1%) RH", "WP_M4000W40_LH_2018")
WP_M4000W40_LH_2018.sigma = .01679 
WP_M4000W40_LH_2018.year = 2018
WP_M4000W40_LH_2018.dataset = "/Wprimetotb_M4000W40_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M4200W42_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 4.2TeV(1%) RH", "WP_M4200W42_LH_2018")
WP_M4200W42_LH_2018.sigma = .01161 
WP_M4200W42_LH_2018.year = 2018
WP_M4200W42_LH_2018.dataset = "/Wprimetotb_M4200W42_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M4400W44_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 4.4TeV(1%) RH", "WP_M4400W44_LH_2018")
WP_M4400W44_LH_2018.sigma = .008501 
WP_M4400W44_LH_2018.year = 2018
WP_M4400W44_LH_2018.dataset = "/Wprimetotb_M4400W44_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M4600W46_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 4.6TeV(1%) RH", "WP_M4600W46_LH_2018")
WP_M4600W46_LH_2018.sigma = .006172 
WP_M4600W46_LH_2018.year = 2018
WP_M4600W46_LH_2018.dataset = "/Wprimetotb_M4600W46_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M4800W48_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 4.8TeV(1%) RH", "WP_M4800W48_LH_2018")
WP_M4800W48_LH_2018.sigma = .004538 
WP_M4800W48_LH_2018.year = 2018
WP_M4800W48_LH_2018.dataset = "/Wprimetotb_M4800W48_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M5000W50_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 5.0TeV(1%) RH", "WP_M5000W50_LH_2018")
WP_M5000W50_LH_2018.sigma = .003381 
WP_M5000W50_LH_2018.year = 2018
WP_M5000W50_LH_2018.dataset = "/Wprimetotb_M5000W50_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M5200W52_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 5.2TeV(1%) RH", "WP_M5200W52_LH_2018")
WP_M5200W52_LH_2018.sigma = .00254 
WP_M5200W52_LH_2018.year = 2018
WP_M5200W52_LH_2018.dataset = "/Wprimetotb_M5200W52_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M5400W54_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 5.4TeV(1%) RH", "WP_M5400W54_LH_2018")
WP_M5400W54_LH_2018.sigma = .001929 
WP_M5400W54_LH_2018.year = 2018
WP_M5400W54_LH_2018.dataset = "/Wprimetotb_M5400W54_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M5600W56_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 5.6TeV(1%) RH", "WP_M5600W56_LH_2018")
WP_M5600W56_LH_2018.sigma = .001476 
WP_M5600W56_LH_2018.year = 2018
WP_M5600W56_LH_2018.dataset = "/Wprimetotb_M5600W56_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M5800W58_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 5.8TeV(1%) RH", "WP_M5800W58_LH_2018")
WP_M5800W58_LH_2018.sigma = .001138 
WP_M5800W58_LH_2018.year = 2018
WP_M5800W58_LH_2018.dataset = "/Wprimetotb_M5800W58_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M6000W60_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 6.0TeV(1%) RH", "WP_M6000W60_LH_2018")
WP_M6000W60_LH_2018.sigma = .0008807 
WP_M6000W60_LH_2018.year = 2018
WP_M6000W60_LH_2018.dataset = "/Wprimetotb_M6000W60_LH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_LH_2018 = sample(ROOT.kBlue, 1, 1001, "W' LH", "WP_LH_2018")
WP_LH_2018.year = 2018
WP_LH_2018.components = [WP_M2000W200_LH_2018, WP_M2000W400_LH_2018, WP_M2000W600_LH_2018, WP_M2400W240_LH_2018, WP_M2400W480_LH_2018, WP_M2400W720_LH_2018, WP_M2800W280_LH_2018, WP_M2800W560_LH_2018, WP_M2800W840_LH_2018, WP_M3200W320_LH_2018, WP_M3200W640_LH_2018, WP_M3200W960_LH_2018, WP_M3600W360_LH_2018, WP_M3600W720_LH_2018, WP_M3600W1080_LH_2018, WP_M4000W400_LH_2018, WP_M4000W800_LH_2018, WP_M4000W1200_LH_2018, WP_M4400W440_LH_2018, WP_M4400W880_LH_2018, WP_M4400W1320_LH_2018, WP_M4800W480_LH_2018, WP_M4800W960_LH_2018, WP_M4800W1440_LH_2018, WP_M5200W520_LH_2018, WP_M5200W1040_LH_2018, WP_M5200W1560_LH_2018, WP_M5600W560_LH_2018, WP_M5600W1120_LH_2018, WP_M5600W1680_LH_2018, WP_M6000W600_LH_2018, WP_M6000W1200_LH_2018, WP_M6000W1800_LH_2018, WP_M2000W20_LH_2018, WP_M2200W22_LH_2018, WP_M2400W24_LH_2018, WP_M2600W26_LH_2018, WP_M2800W28_LH_2018, WP_M3000W30_LH_2018, WP_M3200W32_LH_2018, WP_M3400W34_LH_2018, WP_M3600W36_LH_2018, WP_M3800W38_LH_2018, WP_M4000W40_LH_2018, WP_M4200W42_LH_2018, WP_M4400W44_LH_2018, WP_M4600W46_LH_2018, WP_M4800W48_LH_2018, WP_M5000W50_LH_2018, WP_M5200W52_LH_2018, WP_M5400W54_LH_2018, WP_M5600W56_LH_2018, WP_M5800W58_LH_2018, WP_M6000W60_LH_2018]

################################ Signal Sample RH ################################
WP_M2000W200_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 2.0TeV(10%) RH", "WP_M2000W200_RH_2018")
WP_M2000W200_RH_2018.sigma = .154 
WP_M2000W200_RH_2018.year = 2018
WP_M2000W200_RH_2018.dataset = "/Wprimetotb_M2000W200_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M2000W400_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 2.0TeV(20%) RH", "WP_M2000W400_RH_2018")
WP_M2000W400_RH_2018.sigma = .08177 
WP_M2000W400_RH_2018.year = 2018
WP_M2000W400_RH_2018.dataset = "/Wprimetotb_M2000W400_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M2000W600_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 2.0TeV(30%) RH", "WP_M2000W600_RH_2018")
WP_M2000W600_RH_2018.sigma = .05617 
WP_M2000W600_RH_2018.year = 2018
WP_M2000W600_RH_2018.dataset = "/Wprimetotb_M2000W600_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M2400W240_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 2.4TeV(10%) RH", "WP_M2400W240_RH_2018")
WP_M2400W240_RH_2018.sigma = .06106 
WP_M2400W240_RH_2018.year = 2018
WP_M2400W240_RH_2018.dataset = "/Wprimetotb_M2400W240_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M2400W480_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 2.4TeV(20%) RH", "WP_M2400W480_RH_2018")
WP_M2400W480_RH_2018.sigma = .03416 
WP_M2400W480_RH_2018.year = 2018
WP_M2400W480_RH_2018.dataset = "/Wprimetotb_M2400W480_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M2400W720_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 2.4TeV(30%) RH", "WP_M2400W720_RH_2018")
WP_M2400W720_RH_2018.sigma = .02404 
WP_M2400W720_RH_2018.year = 2018
WP_M2400W720_RH_2018.dataset = "/Wprimetotb_M2400W720_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M2800W280_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 2.8TeV(10%) RH", "WP_M2800W280_RH_2018")
WP_M2800W280_RH_2018.sigma = .02655 
WP_M2800W280_RH_2018.year = 2018
WP_M2800W280_RH_2018.dataset = "/Wprimetotb_M2800W280_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M2800W560_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 2.8TeV(20%) RH", "WP_M2800W560_RH_2018")
WP_M2800W560_RH_2018.sigma = .01554 
WP_M2800W560_RH_2018.year = 2018
WP_M2800W560_RH_2018.dataset = "/Wprimetotb_M2800W560_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M2800W840_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 2.8TeV(30%) RH", "WP_M2800W840_RH_2018")
WP_M2800W840_RH_2018.sigma = .01158 
WP_M2800W840_RH_2018.year = 2018
WP_M2800W840_RH_2018.dataset = "/Wprimetotb_M2800W840_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M3200W320_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 3.2TeV(10%) RH", "WP_M3200W320_RH_2018")
WP_M3200W320_RH_2018.sigma = .01242 
WP_M3200W320_RH_2018.year = 2018
WP_M3200W320_RH_2018.dataset = "/Wprimetotb_M3200W320_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M3200W640_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 3.2TeV(20%) RH", "WP_M3200W640_RH_2018")
WP_M3200W640_RH_2018.sigma = .007778 
WP_M3200W640_RH_2018.year = 2018
WP_M3200W640_RH_2018.dataset = "/Wprimetotb_M3200W640_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M3200W960_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 3.2TeV(30%) RH", "WP_M3200W960_RH_2018")
WP_M3200W960_RH_2018.sigma = .006004 
WP_M3200W960_RH_2018.year = 2018
WP_M3200W960_RH_2018.dataset = "/Wprimetotb_M3200W960_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M3600W360_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 3.6TeV(10%) RH", "WP_M3600W360_RH_2018")
WP_M3600W360_RH_2018.sigma = .006191 
WP_M3600W360_RH_2018.year = 2018
WP_M3600W360_RH_2018.dataset = "/Wprimetotb_M3600W360_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M3600W720_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 3.6TeV(20%) RH", "WP_M3600W720_RH_2018")
WP_M3600W720_RH_2018.sigma = .004195 
WP_M3600W720_RH_2018.year = 2018
WP_M3600W720_RH_2018.dataset = "/Wprimetotb_M3600W720_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M3600W1080_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 3.6TeV(30%) RH", "WP_M3600W1080_RH_2018")
WP_M3600W1080_RH_2018.sigma = .003372 
WP_M3600W1080_RH_2018.year = 2018
WP_M3600W1080_RH_2018.dataset = "/Wprimetotb_M3600W1080_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M4000W400_RH_2018 = sample(ROOT.kAzure, 1, 1001, "W' 4.0TeV(10%) RH", "WP_M4000W400_RH_2018")
WP_M4000W400_RH_2018.sigma = .00339 
WP_M4000W400_RH_2018.year = 2018
WP_M4000W400_RH_2018.dataset = "/Wprimetotb_M4000W400_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M4000W800_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 4.0TeV(20%) RH", "WP_M4000W800_RH_2018")
WP_M4000W800_RH_2018.sigma = .002443 
WP_M4000W800_RH_2018.year = 2018
WP_M4000W800_RH_2018.dataset = "/Wprimetotb_M4000W800_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M4000W1200_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 4.0TeV(30%) RH", "WP_M4000W1200_RH_2018")
WP_M4000W1200_RH_2018.sigma = .002024 
WP_M4000W1200_RH_2018.year = 2018
WP_M4000W1200_RH_2018.dataset = "/Wprimetotb_M4000W1200_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M4400W440_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 4.4TeV(10%) RH", "WP_M4400W440_RH_2018")
WP_M4400W440_RH_2018.sigma = .001967 
WP_M4400W440_RH_2018.year = 2018
WP_M4400W440_RH_2018.dataset = "/Wprimetotb_M4400W440_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M4400W880_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 4.4TeV(20%) RH", "WP_M4400W880_RH_2018")
WP_M4400W880_RH_2018.sigma = .001491 
WP_M4400W880_RH_2018.year = 2018
WP_M4400W880_RH_2018.dataset = "/Wprimetotb_M4400W880_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M4400W1320_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 4.4TeV(30%) RH", "WP_M4400W1320_RH_2018")
WP_M4400W1320_RH_2018.sigma = .001278 
WP_M4400W1320_RH_2018.year = 2018
WP_M4400W1320_RH_2018.dataset = "/Wprimetotb_M4400W1320_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M4800W480_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 4.8TeV(10%) RH", "WP_M4800W480_RH_2018")
WP_M4800W480_RH_2018.sigma = .001217 
WP_M4800W480_RH_2018.year = 2018
WP_M4800W480_RH_2018.dataset = "/Wprimetotb_M4800W480_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M4800W960_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 4.8TeV(20%) RH", "WP_M4800W960_RH_2018")
WP_M4800W960_RH_2018.sigma = .0009753 
WP_M4800W960_RH_2018.year = 2018
WP_M4800W960_RH_2018.dataset = "/Wprimetotb_M4800W960_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M4800W1440_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 4.8TeV(30%) RH", "WP_M4800W1440_RH_2018")
WP_M4800W1440_RH_2018.sigma = .0008519 
WP_M4800W1440_RH_2018.year = 2018
WP_M4800W1440_RH_2018.dataset = "/Wprimetotb_M4800W1440_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M5200W520_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 5.2TeV(10%) RH", "WP_M5200W520_RH_2018")
WP_M5200W520_RH_2018.sigma = .0007929 
WP_M5200W520_RH_2018.year = 2018
WP_M5200W520_RH_2018.dataset = "/Wprimetotb_M5200W520_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M5200W1040_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 5.2TeV(20%) RH", "WP_M5200W1040_RH_2018")
WP_M5200W1040_RH_2018.sigma = .0006573 
WP_M5200W1040_RH_2018.year = 2018
WP_M5200W1040_RH_2018.dataset = "/Wprimetotb_M5200W1040_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M5200W1560_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 5.2TeV(30%) RH", "WP_M5200W1560_RH_2018")
WP_M5200W1560_RH_2018.sigma = .0005882 
WP_M5200W1560_RH_2018.year = 2018
WP_M5200W1560_RH_2018.dataset = "/Wprimetotb_M5200W1560_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M5600W560_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 5.6TeV(10%) RH", "WP_M5600W560_RH_2018")
WP_M5600W560_RH_2018.sigma = .0005376 
WP_M5600W560_RH_2018.year = 2018
WP_M5600W560_RH_2018.dataset = "/Wprimetotb_M5600W560_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M5600W1120_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 5.6TeV(20%) RH", "WP_M5600W1120_RH_2018")
WP_M5600W1120_RH_2018.sigma = .000466 
WP_M5600W1120_RH_2018.year = 2018
WP_M5600W1120_RH_2018.dataset = "/Wprimetotb_M5600W1120_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M5600W1680_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 5.6TeV(30%) RH", "WP_M5600W1680_RH_2018")
WP_M5600W1680_RH_2018.sigma = .0004209 
WP_M5600W1680_RH_2018.year = 2018
WP_M5600W1680_RH_2018.dataset = "/Wprimetotb_M5600W1680_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M6000W600_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 6.0TeV(10%) RH", "WP_M6000W600_RH_2018")
WP_M6000W600_RH_2018.sigma = .0003858 
WP_M6000W600_RH_2018.year = 2018
WP_M6000W600_RH_2018.dataset = "/Wprimetotb_M6000W600_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M6000W1200_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 6.0TeV(20%) RH", "WP_M6000W1200_RH_2018")
WP_M6000W1200_RH_2018.sigma = .000338 
WP_M6000W1200_RH_2018.year = 2018
WP_M6000W1200_RH_2018.dataset = "/Wprimetotb_M6000W1200_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M6000W1800_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 6.0TeV(30%) RH", "WP_M6000W1800_RH_2018")
WP_M6000W1800_RH_2018.sigma = .0003086 
WP_M6000W1800_RH_2018.year = 2018
WP_M6000W1800_RH_2018.dataset = "/Wprimetotb_M6000W1800_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M2000W20_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 2.0TeV(1%) RH", "WP_M2000W20_RH_2018")
WP_M2000W20_RH_2018.sigma = 1.397 
WP_M2000W20_RH_2018.year = 2018
WP_M2000W20_RH_2018.dataset = "/Wprimetotb_M2000W20_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M2200W22_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 2.2TeV(1%) RH", "WP_M2200W22_RH_2018")
WP_M2200W22_RH_2018.sigma = .8439 
WP_M2200W22_RH_2018.year = 2018
WP_M2200W22_RH_2018.dataset = "/Wprimetotb_M2200W22_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M2400W24_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 2.4TeV(1%) RH", "WP_M2400W24_RH_2018")
WP_M2400W24_RH_2018.sigma = .5203 
WP_M2400W24_RH_2018.year = 2018
WP_M2400W24_RH_2018.dataset = "/Wprimetotb_M2400W24_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M2600W26_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 2.6TeV(1%) RH", "WP_M2600W26_RH_2018")
WP_M2600W26_RH_2018.sigma = .3236 
WP_M2600W26_RH_2018.year = 2018
WP_M2600W26_RH_2018.dataset = "/Wprimetotb_M2600W26_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M2800W28_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 2.8TeV(1%) RH", "WP_M2800W28_RH_2018")
WP_M2800W28_RH_2018.sigma = .2049 
WP_M2800W28_RH_2018.year = 2018
WP_M2800W28_RH_2018.dataset = "/Wprimetotb_M2800W28_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M3000W30_RH_2018 = sample(ROOT.kMagenta+2, 1, 1001, "W' 3.0TeV(1%) RH", "WP_M3000W30_RH_2018")
WP_M3000W30_RH_2018.sigma = .1318 
WP_M3000W30_RH_2018.year = 2018
WP_M3000W30_RH_2018.dataset = "/Wprimetotb_M3000W30_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M3200W32_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 3.2TeV(1%) RH", "WP_M3200W32_RH_2018")
WP_M3200W32_RH_2018.sigma = .08553 
WP_M3200W32_RH_2018.year = 2018
WP_M3200W32_RH_2018.dataset = "/Wprimetotb_M3200W32_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M3400W34_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 3.4TeV(1%) RH", "WP_M3400W34_RH_2018")
WP_M3400W34_RH_2018.sigma = .05633 
WP_M3400W34_RH_2018.year = 2018
WP_M3400W34_RH_2018.dataset = "/Wprimetotb_M3400W34_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M3600W36_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 3.6TeV(1%) RH", "WP_M3600W36_RH_2018")
WP_M3600W36_RH_2018.sigma = .0375 
WP_M3600W36_RH_2018.year = 2018
WP_M3600W36_RH_2018.dataset = "/Wprimetotb_M3600W36_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M3800W38_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 3.8TeV(1%) RH", "WP_M3800W38_RH_2018")
WP_M3800W38_RH_2018.sigma = .02533 
WP_M3800W38_RH_2018.year = 2018
WP_M3800W38_RH_2018.dataset = "/Wprimetotb_M3800W38_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M4000W40_RH_2018 = sample(ROOT.kGreen+2, 1, 1001, "W' 4.0TeV(1%) RH", "WP_M4000W40_RH_2018")
WP_M4000W40_RH_2018.sigma = .01736 
WP_M4000W40_RH_2018.year = 2018
WP_M4000W40_RH_2018.dataset = "/Wprimetotb_M4000W40_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M4200W42_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 4.2TeV(1%) RH", "WP_M4200W42_RH_2018")
WP_M4200W42_RH_2018.sigma = .01208 
WP_M4200W42_RH_2018.year = 2018
WP_M4200W42_RH_2018.dataset = "/Wprimetotb_M4200W42_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M4400W44_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 4.4TeV(1%) RH", "WP_M4400W44_RH_2018")
WP_M4400W44_RH_2018.sigma = .00879 
WP_M4400W44_RH_2018.year = 2018
WP_M4400W44_RH_2018.dataset = "/Wprimetotb_M4400W44_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M4600W46_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 4.6TeV(1%) RH", "WP_M4600W46_RH_2018")
WP_M4600W46_RH_2018.sigma = .006384 
WP_M4600W46_RH_2018.year = 2018
WP_M4600W46_RH_2018.dataset = "/Wprimetotb_M4600W46_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M4800W48_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 4.8TeV(1%) RH", "WP_M4800W48_RH_2018")
WP_M4800W48_RH_2018.sigma = .004696 
WP_M4800W48_RH_2018.year = 2018
WP_M4800W48_RH_2018.dataset = "/Wprimetotb_M4800W48_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M5000W50_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 5.0TeV(1%) RH", "WP_M5000W50_RH_2018")
WP_M5000W50_RH_2018.sigma = .003501 
WP_M5000W50_RH_2018.year = 2018
WP_M5000W50_RH_2018.dataset = "/Wprimetotb_M5000W50_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M5200W52_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 5.2TeV(1%) RH", "WP_M5200W52_RH_2018")
WP_M5200W52_RH_2018.sigma = .002633 
WP_M5200W52_RH_2018.year = 2018
WP_M5200W52_RH_2018.dataset = "/Wprimetotb_M5200W52_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M5400W54_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 5.4TeV(1%) RH", "WP_M5400W54_RH_2018")
WP_M5400W54_RH_2018.sigma = .002008 
WP_M5400W54_RH_2018.year = 2018
WP_M5400W54_RH_2018.dataset = "/Wprimetotb_M5400W54_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M5600W56_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 5.6TeV(1%) RH", "WP_M5600W56_RH_2018")
WP_M5600W56_RH_2018.sigma = .001533 
WP_M5600W56_RH_2018.year = 2018
WP_M5600W56_RH_2018.dataset = "/Wprimetotb_M5600W56_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M5800W58_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 5.8TeV(1%) RH", "WP_M5800W58_RH_2018")
WP_M5800W58_RH_2018.sigma = .001182 
WP_M5800W58_RH_2018.year = 2018
WP_M5800W58_RH_2018.dataset = "/Wprimetotb_M5800W58_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_M6000W60_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' 6.0TeV(1%) RH", "WP_M6000W60_RH_2018")
WP_M6000W60_RH_2018.sigma = .0009153 
WP_M6000W60_RH_2018.year = 2018
WP_M6000W60_RH_2018.dataset = "/Wprimetotb_M6000W60_RH_TuneCP5_13TeV-madgraph-pythia8/"+tag_2018+"-v1/NANOAODSIM"

WP_RH_2018 = sample(ROOT.kBlue, 1, 1001, "W' RH", "WP_RH_2018")
WP_RH_2018.year = 2018
WP_RH_2018.components = [WP_M2000W200_RH_2018, WP_M2000W400_RH_2018, WP_M2000W600_RH_2018, WP_M2400W240_RH_2018, WP_M2400W480_RH_2018, WP_M2400W720_RH_2018, WP_M2800W280_RH_2018, WP_M2800W560_RH_2018, WP_M2800W840_RH_2018, WP_M3200W320_RH_2018, WP_M3200W640_RH_2018, WP_M3200W960_RH_2018, WP_M3600W360_RH_2018, WP_M3600W720_RH_2018, WP_M3600W1080_RH_2018, WP_M4000W400_RH_2018, WP_M4000W800_RH_2018, WP_M4000W1200_RH_2018, WP_M4400W440_RH_2018, WP_M4400W880_RH_2018, WP_M4400W1320_RH_2018, WP_M4800W480_RH_2018, WP_M4800W960_RH_2018, WP_M4800W1440_RH_2018, WP_M5200W520_RH_2018, WP_M5200W1040_RH_2018, WP_M5200W1560_RH_2018, WP_M5600W560_RH_2018, WP_M5600W1120_RH_2018, WP_M5600W1680_RH_2018, WP_M6000W600_RH_2018, WP_M6000W1200_RH_2018, WP_M6000W1800_RH_2018, WP_M2000W20_RH_2018, WP_M2200W22_RH_2018, WP_M2400W24_RH_2018, WP_M2600W26_RH_2018, WP_M2800W28_RH_2018, WP_M3000W30_RH_2018, WP_M3200W32_RH_2018, WP_M3400W34_RH_2018, WP_M3600W36_RH_2018, WP_M3800W38_RH_2018, WP_M4000W40_RH_2018, WP_M4200W42_RH_2018, WP_M4400W44_RH_2018, WP_M4600W46_RH_2018, WP_M4800W48_RH_2018, WP_M5000W50_RH_2018, WP_M5200W52_RH_2018, WP_M5400W54_RH_2018, WP_M5600W56_RH_2018, WP_M5800W58_RH_2018, WP_M6000W60_RH_2018]


####################################################### Data #####################################################################################
tag_data = '02Apr2020'

DataMuB_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataMuB_2016")
DataMuB_2016.runP = 'B'
DataMuB_2016.year = 2016
DataMuB_2016.dataset = '/SingleMuon/Run2016B-'+tag_data + '_ver2-v1/NANOAOD'
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
DataEleB_2016.dataset = '/SingleElectron/Run2016B-'+tag_data + '_ver2-v1/NANOAOD'
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

DataPhB_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataPhB_2016")
DataPhB_2016.runP = 'B'
DataPhB_2016.year = 2016
DataPhB_2016.dataset = '/SinglePhoton/Run2016B-'+tag_data + '_ver2-v1/NANOAOD'
DataPhC_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataPhC_2016")
DataPhC_2016.runP = 'C'
DataPhC_2016.year = 2016
DataPhC_2016.dataset = '/SinglePhoton/Run2016C-'+tag_data + '-v1/NANOAOD'
DataPhD_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataPhD_2016")
DataPhD_2016.runP = 'D'
DataPhD_2016.year = 2016
DataPhD_2016.dataset = '/SinglePhoton/Run2016D-'+tag_data + '-v1/NANOAOD'
DataPhE_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataPhE_2016")
DataPhE_2016.runP = 'E'
DataPhE_2016.year = 2016
DataPhE_2016.dataset = '/SinglePhoton/Run2016E-'+tag_data + '-v1/NANOAOD'
DataPhF_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataPhF_2016")
DataPhF_2016.runP = 'F'
DataPhF_2016.year = 2016
DataPhF_2016.dataset = '/SinglePhoton/Run2016F-'+tag_data + '-v1/NANOAOD'
DataPhG_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataPhG_2016")
DataPhG_2016.runP = 'G'
DataPhG_2016.year = 2016
DataPhG_2016.dataset = '/SinglePhoton/Run2016G-'+tag_data + '-v1/NANOAOD'
DataPhH_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataPhH_2016")
DataPhH_2016.runP = 'H'
DataPhH_2016.year = 2016
DataPhH_2016.dataset = '/SinglePhoton/Run2016H-'+tag_data + '-v1/NANOAOD'
DataPh_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataPh_2016")
DataPh_2016.year = 2016
DataPh_2016.components = [DataPhB_2016, DataPhC_2016, DataPhD_2016, DataPhE_2016, DataPhF_2016, DataPhG_2016, DataPhH_2016]

DataHTB_2016 = sample(ROOT.kBlack, 1, 1001, "Data", "DataHTB_2016")
DataHTB_2016.runP = 'B'
DataHTB_2016.year = 2016
DataHTB_2016.dataset = '/JetHT/Run2016B-'+tag_data + '_ver2-v1/NANOAOD'
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

DataPhB_2017 = sample(ROOT.kBlack, 1, 1001, "Data", "DataPhB_2017")
DataPhB_2017.runP = 'B'
DataPhB_2017.year = 2017
DataPhB_2017.dataset = '/SinglePhoton/Run2017B-'+tag_data + '-v1/NANOAOD'
DataPhC_2017 = sample(ROOT.kBlack, 1, 1001, "Data", "DataPhC_2017")
DataPhC_2017.runP = 'C'
DataPhC_2017.year = 2017
DataPhC_2017.dataset = '/SinglePhoton/Run2017C-'+tag_data + '-v1/NANOAOD'
DataPhD_2017 = sample(ROOT.kBlack, 1, 1001, "Data", "DataPhD_2017")
DataPhD_2017.runP = 'D'
DataPhD_2017.year = 2017
DataPhD_2017.dataset = '/SinglePhoton/Run2017D-'+tag_data + '-v1/NANOAOD'
DataPhE_2017 = sample(ROOT.kBlack, 1, 1001, "Data", "DataPhE_2017")
DataPhE_2017.runP = 'E'
DataPhE_2017.year = 2017
DataPhE_2017.dataset = '/SinglePhoton/Run2017E-'+tag_data + '-v1/NANOAOD'
DataPhF_2017 = sample(ROOT.kBlack, 1, 1001, "Data", "DataPhF_2017")
DataPhF_2017.runP = 'F'
DataPhF_2017.year = 2017
DataPhF_2017.dataset = '/SinglePhoton/Run2017F-'+tag_data + '-v1/NANOAOD'
DataPh_2017 = sample(ROOT.kBlack, 1, 1001, "Data", "DataPh_2017")
DataPh_2017.year = 2017
DataPh_2017.components = [DataPhB_2017, DataPhC_2017, DataPhD_2017, DataPhE_2017, DataPhF_2017]

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
DataMu_2018 = sample(ROOT.kBlack, 1, 1001, "Data", "DataMu_2018")
DataMu_2018.year = 2018
DataMu_2018.components = [DataMuA_2018, DataMuB_2018, DataMuC_2018, DataMuD_2018]

DataEleA_2018 = sample(ROOT.kBlack, 1, 1001, "Data", "DataEleA_2018")
DataEleA_2018.runP = 'A'
DataEleA_2018.year = 2018
DataEleA_2018.dataset = '/EGamma/Run2018A-'+tag_data + '-v1/NANOAOD'
DataEleB_2018 = sample(ROOT.kBlack, 1, 1001, "Data", "DataEleB_2018")
DataEleB_2018.runP = 'B'
DataEleB_2018.year = 2018
DataEleB_2018.dataset = '/EGamma/Run2018C-'+tag_data + '-v1/NANOAOD'
DataEleC_2018 = sample(ROOT.kBlack, 1, 1001, "Data", "DataEleC_2018")
DataEleC_2018.runP = 'C'
DataEleC_2018.year = 2018
DataEleC_2018.dataset = '/EGamma/Run2018C-'+tag_data + '-v1/NANOAOD'
DataEleD_2018 = sample(ROOT.kBlack, 1, 1001, "Data", "DataEleD_2018")
DataEleD_2018.runP = 'D'
DataEleD_2018.year = 2018
DataEleD_2018.dataset = '/EGamma/Run2018D-'+tag_data + '-v1/NANOAOD'
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
DataHTC_2018.dataset = '/JetHT/Run2018C-'+tag_data + '-v2/NANOAOD'
DataHTD_2018 = sample(ROOT.kBlack, 1, 1001, "Data", "DataHTD_2018")
DataHTD_2018.runP = 'D'
DataHTD_2018.year = 2018
DataHTD_2018.dataset = '/JetHT/Run2018D-'+tag_data + '-v1/NANOAOD'
DataHT_2018 = sample(ROOT.kBlack, 1, 1001, "Data", "DataHT_2018")
DataHT_2018.year = 2018
DataHT_2018.components = [DataHTA_2018, DataHTB_2018, DataHTC_2018, DataHTD_2018]

sample_dict = {
    'TT_Mtt_2016':TT_Mtt_2016, 'TT_Mtt700to1000_2016':TT_Mtt700to1000_2016, 'TT_Mtt1000toInf_2016':TT_Mtt1000toInf_2016, 'TT_incl_2016':TT_incl_2016, 'TT_dilep_2016':TT_dilep_2016,
    'WJets_2016':WJets_2016, 'WJetsHT70to100_2016':WJetsHT70to100_2016, 'WJetsHT100to200_2016':WJetsHT100to200_2016, 'WJetsHT200to400_2016':WJetsHT200to400_2016, 'WJetsHT400to600_2016':WJetsHT400to600_2016, 'WJetsHT600to800_2016':WJetsHT600to800_2016, 'WJetsHT800to1200_2016':WJetsHT800to1200_2016, 'WJetsHT1200to2500_2016':WJetsHT1200to2500_2016, 'WJetsHT2500toInf_2016':WJetsHT2500toInf_2016,
    'ST_2016':ST_2016, 'ST_tch_t_2016':ST_tch_t_2016, 'ST_tch_tbar_2016':ST_tch_tbar_2016, 'ST_tW_t_2016':ST_tW_t_2016, 'ST_tW_tbar_2016':ST_tW_tbar_2016, 'ST_sch_2016':ST_sch_2016,
    'QCD_2016':QCD_2016, 'QCDHT_300to500_2016':QCDHT_300to500_2016, 'QCDHT_500to700_2016':QCDHT_500to700_2016, 'QCDHT_700to1000_2016':QCDHT_700to1000_2016, 'QCDHT_1000to1500_2016':QCDHT_1000to1500_2016, 'QCDHT_1500to2000_2016':QCDHT_1500to2000_2016, 'QCDHT_2000toInf_2016':QCDHT_2000toInf_2016,
    'WP_LH_2016':WP_LH_2016,'WP_M2000W200_LH_2016':WP_M2000W200_LH_2016, 'WP_M2000W400_LH_2016':WP_M2000W400_LH_2016, 'WP_M2000W600_LH_2016':WP_M2000W600_LH_2016, 'WP_M2400W240_LH_2016':WP_M2400W240_LH_2016, 'WP_M2400W480_LH_2016':WP_M2400W480_LH_2016, 'WP_M2400W720_LH_2016':WP_M2400W720_LH_2016, 'WP_M2800W280_LH_2016':WP_M2800W280_LH_2016, 'WP_M2800W560_LH_2016':WP_M2800W560_LH_2016, 'WP_M2800W840_LH_2016':WP_M2800W840_LH_2016, 'WP_M3200W320_LH_2016':WP_M3200W320_LH_2016, 'WP_M3200W640_LH_2016':WP_M3200W640_LH_2016, 'WP_M3200W960_LH_2016':WP_M3200W960_LH_2016, 'WP_M3600W360_LH_2016':WP_M3600W360_LH_2016, 'WP_M3600W720_LH_2016':WP_M3600W720_LH_2016, 'WP_M3600W1080_LH_2016':WP_M3600W1080_LH_2016, 'WP_M4000W400_LH_2016':WP_M4000W400_LH_2016, 'WP_M4000W800_LH_2016':WP_M4000W800_LH_2016, 'WP_M4000W1200_LH_2016':WP_M4000W1200_LH_2016, 'WP_M4400W440_LH_2016':WP_M4400W440_LH_2016, 'WP_M4400W880_LH_2016':WP_M4400W880_LH_2016, 'WP_M4400W1320_LH_2016':WP_M4400W1320_LH_2016, 'WP_M4800W480_LH_2016':WP_M4800W480_LH_2016, 'WP_M4800W960_LH_2016':WP_M4800W960_LH_2016, 'WP_M4800W1440_LH_2016':WP_M4800W1440_LH_2016, 'WP_M5200W520_LH_2016':WP_M5200W520_LH_2016, 'WP_M5200W1040_LH_2016':WP_M5200W1040_LH_2016, 'WP_M5200W1560_LH_2016':WP_M5200W1560_LH_2016, 'WP_M5600W560_LH_2016':WP_M5600W560_LH_2016, 'WP_M5600W1120_LH_2016':WP_M5600W1120_LH_2016, 'WP_M5600W1680_LH_2016':WP_M5600W1680_LH_2016, 'WP_M6000W600_LH_2016':WP_M6000W600_LH_2016, 'WP_M6000W1200_LH_2016':WP_M6000W1200_LH_2016, 'WP_M6000W1800_LH_2016':WP_M6000W1800_LH_2016, 'WP_M2000W20_LH_2016':WP_M2000W20_LH_2016, 'WP_M2200W22_LH_2016':WP_M2200W22_LH_2016, 'WP_M2400W24_LH_2016':WP_M2400W24_LH_2016, 'WP_M2600W26_LH_2016':WP_M2600W26_LH_2016, 'WP_M2800W28_LH_2016':WP_M2800W28_LH_2016, 'WP_M3000W30_LH_2016':WP_M3000W30_LH_2016, 'WP_M3200W32_LH_2016':WP_M3200W32_LH_2016, 'WP_M3400W34_LH_2016':WP_M3400W34_LH_2016, 'WP_M3600W36_LH_2016':WP_M3600W36_LH_2016, 'WP_M3800W38_LH_2016':WP_M3800W38_LH_2016, 'WP_M4000W40_LH_2016':WP_M4000W40_LH_2016, 'WP_M4200W42_LH_2016':WP_M4200W42_LH_2016, 'WP_M4400W44_LH_2016':WP_M4400W44_LH_2016, 'WP_M4600W46_LH_2016':WP_M4600W46_LH_2016, 'WP_M4800W48_LH_2016':WP_M4800W48_LH_2016, 'WP_M5000W50_LH_2016':WP_M5000W50_LH_2016, 'WP_M5200W52_LH_2016':WP_M5200W52_LH_2016, 'WP_M5400W54_LH_2016':WP_M5400W54_LH_2016, 'WP_M5600W56_LH_2016':WP_M5600W56_LH_2016, 'WP_M5800W58_LH_2016':WP_M5800W58_LH_2016, 'WP_M6000W60_LH_2016':WP_M6000W60_LH_2016,
    'WP_RH_2016':WP_RH_2016,'WP_M2000W200_RH_2016':WP_M2000W200_RH_2016, 'WP_M2000W400_RH_2016':WP_M2000W400_RH_2016, 'WP_M2000W600_RH_2016':WP_M2000W600_RH_2016, 'WP_M2400W240_RH_2016':WP_M2400W240_RH_2016, 'WP_M2400W480_RH_2016':WP_M2400W480_RH_2016, 'WP_M2400W720_RH_2016':WP_M2400W720_RH_2016, 'WP_M2800W280_RH_2016':WP_M2800W280_RH_2016, 'WP_M2800W560_RH_2016':WP_M2800W560_RH_2016, 'WP_M2800W840_RH_2016':WP_M2800W840_RH_2016, 'WP_M3200W320_RH_2016':WP_M3200W320_RH_2016, 'WP_M3200W640_RH_2016':WP_M3200W640_RH_2016, 'WP_M3200W960_RH_2016':WP_M3200W960_RH_2016, 'WP_M3600W360_RH_2016':WP_M3600W360_RH_2016, 'WP_M3600W720_RH_2016':WP_M3600W720_RH_2016, 'WP_M3600W1080_RH_2016':WP_M3600W1080_RH_2016, 'WP_M4000W400_RH_2016':WP_M4000W400_RH_2016, 'WP_M4000W800_RH_2016':WP_M4000W800_RH_2016, 'WP_M4000W1200_RH_2016':WP_M4000W1200_RH_2016, 'WP_M4400W440_RH_2016':WP_M4400W440_RH_2016, 'WP_M4400W880_RH_2016':WP_M4400W880_RH_2016, 'WP_M4400W1320_RH_2016':WP_M4400W1320_RH_2016, 'WP_M4800W480_RH_2016':WP_M4800W480_RH_2016, 'WP_M4800W960_RH_2016':WP_M4800W960_RH_2016, 'WP_M4800W1440_RH_2016':WP_M4800W1440_RH_2016, 'WP_M5200W520_RH_2016':WP_M5200W520_RH_2016, 'WP_M5200W1040_RH_2016':WP_M5200W1040_RH_2016, 'WP_M5200W1560_RH_2016':WP_M5200W1560_RH_2016, 'WP_M5600W560_RH_2016':WP_M5600W560_RH_2016, 'WP_M5600W1120_RH_2016':WP_M5600W1120_RH_2016, 'WP_M5600W1680_RH_2016':WP_M5600W1680_RH_2016, 'WP_M6000W600_RH_2016':WP_M6000W600_RH_2016, 'WP_M6000W1200_RH_2016':WP_M6000W1200_RH_2016, 'WP_M6000W1800_RH_2016':WP_M6000W1800_RH_2016, 'WP_M2000W20_RH_2016':WP_M2000W20_RH_2016, 'WP_M2200W22_RH_2016':WP_M2200W22_RH_2016, 'WP_M2400W24_RH_2016':WP_M2400W24_RH_2016, 'WP_M2600W26_RH_2016':WP_M2600W26_RH_2016, 'WP_M2800W28_RH_2016':WP_M2800W28_RH_2016, 'WP_M3000W30_RH_2016':WP_M3000W30_RH_2016, 'WP_M3200W32_RH_2016':WP_M3200W32_RH_2016, 'WP_M3400W34_RH_2016':WP_M3400W34_RH_2016, 'WP_M3600W36_RH_2016':WP_M3600W36_RH_2016, 'WP_M3800W38_RH_2016':WP_M3800W38_RH_2016, 'WP_M4000W40_RH_2016':WP_M4000W40_RH_2016, 'WP_M4200W42_RH_2016':WP_M4200W42_RH_2016, 'WP_M4400W44_RH_2016':WP_M4400W44_RH_2016, 'WP_M4600W46_RH_2016':WP_M4600W46_RH_2016, 'WP_M4800W48_RH_2016':WP_M4800W48_RH_2016, 'WP_M5000W50_RH_2016':WP_M5000W50_RH_2016, 'WP_M5200W52_RH_2016':WP_M5200W52_RH_2016, 'WP_M5400W54_RH_2016':WP_M5400W54_RH_2016, 'WP_M5600W56_RH_2016':WP_M5600W56_RH_2016, 'WP_M5800W58_RH_2016':WP_M5800W58_RH_2016, 'WP_M6000W60_RH_2016':WP_M6000W60_RH_2016,
    'WP_RH_COMP_2016':WP_RH_COMP_2016, 'WP_M1900_RH_COMP_2016':WP_M1900_RH_COMP_2016, 'WP_M3000_RH_COMP_2016':WP_M3000_RH_COMP_2016, 'WP_M4000_RH_COMP_2016':WP_M4000_RH_COMP_2016,
    'DataMu_2016':DataMu_2016, 'DataMuB_2016':DataMuB_2016,  'DataMuC_2016':DataMuC_2016, 'DataMuD_2016':DataMuD_2016, 'DataMuE_2016':DataMuE_2016, 'DataMuF_2016':DataMuF_2016, 'DataMuG_2016':DataMuG_2016, 'DataMuH_2016':DataMuH_2016,
    'DataEle_2016':DataEle_2016, 'DataEleB_2016':DataEleB_2016, 'DataEleC_2016':DataEleC_2016, 'DataEleD_2016':DataEleD_2016, 'DataEleE_2016':DataEleE_2016, 'DataEleF_2016':DataEleF_2016, 'DataEleG_2016':DataEleG_2016, 'DataEleH_2016':DataEleH_2016,
    'DataPh_2016':DataPh_2016, 'DataPhB_2016':DataPhB_2016, 'DataPhC_2016':DataPhC_2016, 'DataPhD_2016':DataPhD_2016, 'DataPhE_2016':DataPhE_2016, 'DataPhF_2016':DataPhF_2016, 'DataPhG_2016':DataPhG_2016, 'DataPhH_2016':DataPhH_2016,
    'DataHT_2016':DataHT_2016, 'DataHTB_2016':DataHTB_2016, 'DataHTC_2016':DataHTC_2016, 'DataHTD_2016':DataHTD_2016, 'DataHTE_2016':DataHTE_2016, 'DataHTF_2016':DataHTF_2016, 'DataHTG_2016':DataHTG_2016, 'DataHTH_2016':DataHTH_2016,
    'TT_Mtt_2017':TT_Mtt_2017, 'TT_Mtt700to1000_2017':TT_Mtt700to1000_2017, 'TT_Mtt1000toInf_2017':TT_Mtt1000toInf_2017, 'TT_dilep_2017':TT_dilep_2017, 'TT_SemiLep2017':TT_semilep_2017,
    'WJets_2017':WJets_2017, 'WJetsHT200to400_2017':WJetsHT200to400_2017, 'WJetsHT400to600_2017':WJetsHT400to600_2017, 'WJetsHT600to800_2017':WJetsHT600to800_2017, 'WJetsHT800to1200_2017':WJetsHT800to1200_2017, 'WJetsHT1200to2500_2017':WJetsHT1200to2500_2017, 'WJetsHT2500toInf_2017':WJetsHT2500toInf_2017,
    'ST_2017':ST_2017, 'ST_tch_t_2017':ST_tch_t_2017, 'ST_tch_tbar_2017':ST_tch_tbar_2017, 'ST_tW_t_2017':ST_tW_t_2017, 'ST_tW_tbar_2017':ST_tW_tbar_2017, 'ST_sch_2017':ST_sch_2017,
    'QCD_2017':QCD_2017, 'QCDHT_300to500_2017':QCDHT_300to500_2017, 'QCDHT_500to700_2017':QCDHT_500to700_2017, 'QCDHT_700to1000_2017':QCDHT_700to1000_2017, 'QCDHT_1000to1500_2017':QCDHT_1000to1500_2017, 'QCDHT_1500to2000_2017':QCDHT_1500to2000_2017, 'QCDHT_2000toInf_2017':QCDHT_2000toInf_2017,
    'WP_LH_2017':WP_LH_2017, 'WP_M2000W200_LH_2017':WP_M2000W200_LH_2017, 'WP_M2000W400_LH_2017':WP_M2000W400_LH_2017, 'WP_M2000W600_LH_2017':WP_M2000W600_LH_2017, 'WP_M2400W240_LH_2017':WP_M2400W240_LH_2017, 'WP_M2400W480_LH_2017':WP_M2400W480_LH_2017, 'WP_M2400W720_LH_2017':WP_M2400W720_LH_2017, 'WP_M2800W280_LH_2017':WP_M2800W280_LH_2017, 'WP_M2800W560_LH_2017':WP_M2800W560_LH_2017, 'WP_M2800W840_LH_2017':WP_M2800W840_LH_2017, 'WP_M3200W320_LH_2017':WP_M3200W320_LH_2017, 'WP_M3200W640_LH_2017':WP_M3200W640_LH_2017, 'WP_M3200W960_LH_2017':WP_M3200W960_LH_2017, 'WP_M3600W360_LH_2017':WP_M3600W360_LH_2017, 'WP_M3600W720_LH_2017':WP_M3600W720_LH_2017, 'WP_M3600W1080_LH_2017':WP_M3600W1080_LH_2017, 'WP_M4000W400_LH_2017':WP_M4000W400_LH_2017, 'WP_M4000W800_LH_2017':WP_M4000W800_LH_2017, 'WP_M4000W1200_LH_2017':WP_M4000W1200_LH_2017, 'WP_M4400W440_LH_2017':WP_M4400W440_LH_2017, 'WP_M4400W880_LH_2017':WP_M4400W880_LH_2017, 'WP_M4400W1320_LH_2017':WP_M4400W1320_LH_2017, 'WP_M4800W480_LH_2017':WP_M4800W480_LH_2017, 'WP_M4800W960_LH_2017':WP_M4800W960_LH_2017, 'WP_M4800W1440_LH_2017':WP_M4800W1440_LH_2017, 'WP_M5200W520_LH_2017':WP_M5200W520_LH_2017, 'WP_M5200W1040_LH_2017':WP_M5200W1040_LH_2017, 'WP_M5200W1560_LH_2017':WP_M5200W1560_LH_2017, 'WP_M5600W560_LH_2017':WP_M5600W560_LH_2017, 'WP_M5600W1120_LH_2017':WP_M5600W1120_LH_2017, 'WP_M5600W1680_LH_2017':WP_M5600W1680_LH_2017, 'WP_M6000W600_LH_2017':WP_M6000W600_LH_2017, 'WP_M6000W1200_LH_2017':WP_M6000W1200_LH_2017, 'WP_M6000W1800_LH_2017':WP_M6000W1800_LH_2017, 'WP_M2000W20_LH_2017':WP_M2000W20_LH_2017, 'WP_M2200W22_LH_2017':WP_M2200W22_LH_2017, 'WP_M2400W24_LH_2017':WP_M2400W24_LH_2017, 'WP_M2600W26_LH_2017':WP_M2600W26_LH_2017, 'WP_M2800W28_LH_2017':WP_M2800W28_LH_2017, 'WP_M3000W30_LH_2017':WP_M3000W30_LH_2017, 'WP_M3200W32_LH_2017':WP_M3200W32_LH_2017, 'WP_M3400W34_LH_2017':WP_M3400W34_LH_2017, 'WP_M3600W36_LH_2017':WP_M3600W36_LH_2017, 'WP_M3800W38_LH_2017':WP_M3800W38_LH_2017, 'WP_M4000W40_LH_2017':WP_M4000W40_LH_2017, 'WP_M4200W42_LH_2017':WP_M4200W42_LH_2017, 'WP_M4400W44_LH_2017':WP_M4400W44_LH_2017, 'WP_M4600W46_LH_2017':WP_M4600W46_LH_2017, 'WP_M4800W48_LH_2017':WP_M4800W48_LH_2017, 'WP_M5000W50_LH_2017':WP_M5000W50_LH_2017, 'WP_M5200W52_LH_2017':WP_M5200W52_LH_2017, 'WP_M5400W54_LH_2017':WP_M5400W54_LH_2017, 'WP_M5600W56_LH_2017':WP_M5600W56_LH_2017, 'WP_M5800W58_LH_2017':WP_M5800W58_LH_2017, 'WP_M6000W60_LH_2017':WP_M6000W60_LH_2017,
    'WP_RH_2017':WP_RH_2017, 'WP_M2000W200_RH_2017':WP_M2000W200_RH_2017, 'WP_M2000W400_RH_2017':WP_M2000W400_RH_2017, 'WP_M2000W600_RH_2017':WP_M2000W600_RH_2017, 'WP_M2400W240_RH_2017':WP_M2400W240_RH_2017, 'WP_M2400W480_RH_2017':WP_M2400W480_RH_2017, 'WP_M2400W720_RH_2017':WP_M2400W720_RH_2017, 'WP_M2800W280_RH_2017':WP_M2800W280_RH_2017, 'WP_M2800W560_RH_2017':WP_M2800W560_RH_2017, 'WP_M2800W840_RH_2017':WP_M2800W840_RH_2017, 'WP_M3200W320_RH_2017':WP_M3200W320_RH_2017, 'WP_M3200W640_RH_2017':WP_M3200W640_RH_2017, 'WP_M3200W960_RH_2017':WP_M3200W960_RH_2017, 'WP_M3600W360_RH_2017':WP_M3600W360_RH_2017, 'WP_M3600W720_RH_2017':WP_M3600W720_RH_2017, 'WP_M3600W1080_RH_2017':WP_M3600W1080_RH_2017, 'WP_M4000W400_RH_2017':WP_M4000W400_RH_2017, 'WP_M4000W800_RH_2017':WP_M4000W800_RH_2017, 'WP_M4000W1200_RH_2017':WP_M4000W1200_RH_2017, 'WP_M4400W440_RH_2017':WP_M4400W440_RH_2017, 'WP_M4400W880_RH_2017':WP_M4400W880_RH_2017, 'WP_M4400W1320_RH_2017':WP_M4400W1320_RH_2017, 'WP_M4800W480_RH_2017':WP_M4800W480_RH_2017, 'WP_M4800W960_RH_2017':WP_M4800W960_RH_2017, 'WP_M4800W1440_RH_2017':WP_M4800W1440_RH_2017, 'WP_M5200W520_RH_2017':WP_M5200W520_RH_2017, 'WP_M5200W1040_RH_2017':WP_M5200W1040_RH_2017, 'WP_M5200W1560_RH_2017':WP_M5200W1560_RH_2017, 'WP_M5600W560_RH_2017':WP_M5600W560_RH_2017, 'WP_M5600W1120_RH_2017':WP_M5600W1120_RH_2017, 'WP_M5600W1680_RH_2017':WP_M5600W1680_RH_2017, 'WP_M6000W600_RH_2017':WP_M6000W600_RH_2017, 'WP_M6000W1200_RH_2017':WP_M6000W1200_RH_2017, 'WP_M6000W1800_RH_2017':WP_M6000W1800_RH_2017, 'WP_M2000W20_RH_2017':WP_M2000W20_RH_2017, 'WP_M2200W22_RH_2017':WP_M2200W22_RH_2017, 'WP_M2400W24_RH_2017':WP_M2400W24_RH_2017, 'WP_M2600W26_RH_2017':WP_M2600W26_RH_2017, 'WP_M2800W28_RH_2017':WP_M2800W28_RH_2017, 'WP_M3000W30_RH_2017':WP_M3000W30_RH_2017, 'WP_M3200W32_RH_2017':WP_M3200W32_RH_2017, 'WP_M3400W34_RH_2017':WP_M3400W34_RH_2017, 'WP_M3600W36_RH_2017':WP_M3600W36_RH_2017, 'WP_M3800W38_RH_2017':WP_M3800W38_RH_2017, 'WP_M4000W40_RH_2017':WP_M4000W40_RH_2017, 'WP_M4200W42_RH_2017':WP_M4200W42_RH_2017, 'WP_M4400W44_RH_2017':WP_M4400W44_RH_2017, 'WP_M4600W46_RH_2017':WP_M4600W46_RH_2017, 'WP_M4800W48_RH_2017':WP_M4800W48_RH_2017, 'WP_M5000W50_RH_2017':WP_M5000W50_RH_2017, 'WP_M5200W52_RH_2017':WP_M5200W52_RH_2017, 'WP_M5400W54_RH_2017':WP_M5400W54_RH_2017, 'WP_M5600W56_RH_2017':WP_M5600W56_RH_2017, 'WP_M5800W58_RH_2017':WP_M5800W58_RH_2017, 'WP_M6000W60_RH_2017':WP_M6000W60_RH_2017,
    'DataMu_2017':DataMu_2017, 'DataMuB_2017':DataMuB_2017, 'DataMuC_2017':DataMuC_2017, 'DataMuD_2017':DataMuD_2017, 'DataMuE_2017':DataMuE_2017, 'DataMuF_2017':DataMuF_2017,
    'DataEle_2017':DataEle_2017, 'DataEleB_2017':DataEleB_2017, 'DataEleC_2017':DataEleC_2017, 'DataEleD_2017':DataEleD_2017, 'DataEleE_2017':DataEleE_2017, 'DataEleF_2017':DataEleF_2017,
    'DataPh_2017':DataPh_2017, 'DataPhB_2017':DataPhB_2017, 'DataPhC_2017':DataPhC_2017, 'DataPhD_2017':DataPhD_2017, 'DataPhE_2017':DataPhE_2017, 'DataPhF_2017':DataPhF_2017,
    'DataHT_2017':DataHT_2017, 'DataHTB_2017':DataHTB_2017, 'DataHTC_2017':DataHTC_2017, 'DataHTD_2017':DataHTD_2017, 'DataHTE_2017':DataHTE_2017, 'DataHTF_2017':DataHTF_2017,
    'TT_Mtt_2018':TT_Mtt_2018, 'TT_Mtt700to1000_2018':TT_Mtt700to1000_2018, 'TT_Mtt1000toInf_2018':TT_Mtt1000toInf_2018, 'TT_dilep_2018':TT_dilep_2018, 'TT_semilep_2018':TT_semilep_2018,
    'WJets_2018':WJets_2018, 'WJetsHT200to400_2018':WJetsHT200to400_2018, 'WJetsHT400to600_2018':WJetsHT400to600_2018, 'WJetsHT600to800_2018':WJetsHT600to800_2018, 'WJetsHT800to1200_2018':WJetsHT800to1200_2018, 'WJetsHT1200to2500_2018':WJetsHT1200to2500_2018, 'WJetsHT2500toInf_2018':WJetsHT2500toInf_2018,
    'ST_2018':ST_2018, 'ST_tch_t_2018':ST_tch_t_2018, 'ST_tch_tbar_2018':ST_tch_tbar_2018, 'ST_tW_t_2018':ST_tW_t_2018, 'ST_tW_tbar_2018':ST_tW_tbar_2018, 'ST_sch_2018':ST_sch_2018,
    'QCD_2018':QCD_2018, 'QCDHT_300to500_2018':QCDHT_300to500_2018, 'QCDHT_500to700_2018':QCDHT_500to700_2018, 'QCDHT_700to1000_2018':QCDHT_700to1000_2018, 'QCDHT_1000to1500_2018':QCDHT_1000to1500_2018, 'QCDHT_1500to2000_2018':QCDHT_1500to2000_2018, 'QCDHT_2000toInf_2018':QCDHT_2000toInf_2018,
    'WP_LH_2018':WP_LH_2018, 'WP_M2000W200_LH_2018':WP_M2000W200_LH_2018, 'WP_M2000W400_LH_2018':WP_M2000W400_LH_2018, 'WP_M2000W600_LH_2018':WP_M2000W600_LH_2018, 'WP_M2400W240_LH_2018':WP_M2400W240_LH_2018, 'WP_M2400W480_LH_2018':WP_M2400W480_LH_2018, 'WP_M2400W720_LH_2018':WP_M2400W720_LH_2018, 'WP_M2800W280_LH_2018':WP_M2800W280_LH_2018, 'WP_M2800W560_LH_2018':WP_M2800W560_LH_2018, 'WP_M2800W840_LH_2018':WP_M2800W840_LH_2018, 'WP_M3200W320_LH_2018':WP_M3200W320_LH_2018, 'WP_M3200W640_LH_2018':WP_M3200W640_LH_2018, 'WP_M3200W960_LH_2018':WP_M3200W960_LH_2018, 'WP_M3600W360_LH_2018':WP_M3600W360_LH_2018, 'WP_M3600W720_LH_2018':WP_M3600W720_LH_2018, 'WP_M3600W1080_LH_2018':WP_M3600W1080_LH_2018, 'WP_M4000W400_LH_2018':WP_M4000W400_LH_2018, 'WP_M4000W800_LH_2018':WP_M4000W800_LH_2018, 'WP_M4000W1200_LH_2018':WP_M4000W1200_LH_2018, 'WP_M4400W440_LH_2018':WP_M4400W440_LH_2018, 'WP_M4400W880_LH_2018':WP_M4400W880_LH_2018, 'WP_M4400W1320_LH_2018':WP_M4400W1320_LH_2018, 'WP_M4800W480_LH_2018':WP_M4800W480_LH_2018, 'WP_M4800W960_LH_2018':WP_M4800W960_LH_2018, 'WP_M4800W1440_LH_2018':WP_M4800W1440_LH_2018, 'WP_M5200W520_LH_2018':WP_M5200W520_LH_2018, 'WP_M5200W1040_LH_2018':WP_M5200W1040_LH_2018, 'WP_M5200W1560_LH_2018':WP_M5200W1560_LH_2018, 'WP_M5600W560_LH_2018':WP_M5600W560_LH_2018, 'WP_M5600W1120_LH_2018':WP_M5600W1120_LH_2018, 'WP_M5600W1680_LH_2018':WP_M5600W1680_LH_2018, 'WP_M6000W600_LH_2018':WP_M6000W600_LH_2018, 'WP_M6000W1200_LH_2018':WP_M6000W1200_LH_2018, 'WP_M6000W1800_LH_2018':WP_M6000W1800_LH_2018, 'WP_M2000W20_LH_2018':WP_M2000W20_LH_2018, 'WP_M2200W22_LH_2018':WP_M2200W22_LH_2018, 'WP_M2400W24_LH_2018':WP_M2400W24_LH_2018, 'WP_M2600W26_LH_2018':WP_M2600W26_LH_2018, 'WP_M2800W28_LH_2018':WP_M2800W28_LH_2018, 'WP_M3000W30_LH_2018':WP_M3000W30_LH_2018, 'WP_M3200W32_LH_2018':WP_M3200W32_LH_2018, 'WP_M3400W34_LH_2018':WP_M3400W34_LH_2018, 'WP_M3600W36_LH_2018':WP_M3600W36_LH_2018, 'WP_M3800W38_LH_2018':WP_M3800W38_LH_2018, 'WP_M4000W40_LH_2018':WP_M4000W40_LH_2018, 'WP_M4200W42_LH_2018':WP_M4200W42_LH_2018, 'WP_M4400W44_LH_2018':WP_M4400W44_LH_2018, 'WP_M4600W46_LH_2018':WP_M4600W46_LH_2018, 'WP_M4800W48_LH_2018':WP_M4800W48_LH_2018, 'WP_M5000W50_LH_2018':WP_M5000W50_LH_2018, 'WP_M5200W52_LH_2018':WP_M5200W52_LH_2018, 'WP_M5400W54_LH_2018':WP_M5400W54_LH_2018, 'WP_M5600W56_LH_2018':WP_M5600W56_LH_2018, 'WP_M5800W58_LH_2018':WP_M5800W58_LH_2018, 'WP_M6000W60_LH_2018':WP_M6000W60_LH_2018,
    'WP_RH_2018':WP_RH_2018, 'WP_M2000W200_RH_2018':WP_M2000W200_RH_2018, 'WP_M2000W400_RH_2018':WP_M2000W400_RH_2018, 'WP_M2000W600_RH_2018':WP_M2000W600_RH_2018, 'WP_M2400W240_RH_2018':WP_M2400W240_RH_2018, 'WP_M2400W480_RH_2018':WP_M2400W480_RH_2018, 'WP_M2400W720_RH_2018':WP_M2400W720_RH_2018, 'WP_M2800W280_RH_2018':WP_M2800W280_RH_2018, 'WP_M2800W560_RH_2018':WP_M2800W560_RH_2018, 'WP_M2800W840_RH_2018':WP_M2800W840_RH_2018, 'WP_M3200W320_RH_2018':WP_M3200W320_RH_2018, 'WP_M3200W640_RH_2018':WP_M3200W640_RH_2018, 'WP_M3200W960_RH_2018':WP_M3200W960_RH_2018, 'WP_M3600W360_RH_2018':WP_M3600W360_RH_2018, 'WP_M3600W720_RH_2018':WP_M3600W720_RH_2018, 'WP_M3600W1080_RH_2018':WP_M3600W1080_RH_2018, 'WP_M4000W400_RH_2018':WP_M4000W400_RH_2018, 'WP_M4000W800_RH_2018':WP_M4000W800_RH_2018, 'WP_M4000W1200_RH_2018':WP_M4000W1200_RH_2018, 'WP_M4400W440_RH_2018':WP_M4400W440_RH_2018, 'WP_M4400W880_RH_2018':WP_M4400W880_RH_2018, 'WP_M4400W1320_RH_2018':WP_M4400W1320_RH_2018, 'WP_M4800W480_RH_2018':WP_M4800W480_RH_2018, 'WP_M4800W960_RH_2018':WP_M4800W960_RH_2018, 'WP_M4800W1440_RH_2018':WP_M4800W1440_RH_2018, 'WP_M5200W520_RH_2018':WP_M5200W520_RH_2018, 'WP_M5200W1040_RH_2018':WP_M5200W1040_RH_2018, 'WP_M5200W1560_RH_2018':WP_M5200W1560_RH_2018, 'WP_M5600W560_RH_2018':WP_M5600W560_RH_2018, 'WP_M5600W1120_RH_2018':WP_M5600W1120_RH_2018, 'WP_M5600W1680_RH_2018':WP_M5600W1680_RH_2018, 'WP_M6000W600_RH_2018':WP_M6000W600_RH_2018, 'WP_M6000W1200_RH_2018':WP_M6000W1200_RH_2018, 'WP_M6000W1800_RH_2018':WP_M6000W1800_RH_2018, 'WP_M2000W20_RH_2018':WP_M2000W20_RH_2018, 'WP_M2200W22_RH_2018':WP_M2200W22_RH_2018, 'WP_M2400W24_RH_2018':WP_M2400W24_RH_2018, 'WP_M2600W26_RH_2018':WP_M2600W26_RH_2018, 'WP_M2800W28_RH_2018':WP_M2800W28_RH_2018, 'WP_M3000W30_RH_2018':WP_M3000W30_RH_2018, 'WP_M3200W32_RH_2018':WP_M3200W32_RH_2018, 'WP_M3400W34_RH_2018':WP_M3400W34_RH_2018, 'WP_M3600W36_RH_2018':WP_M3600W36_RH_2018, 'WP_M3800W38_RH_2018':WP_M3800W38_RH_2018, 'WP_M4000W40_RH_2018':WP_M4000W40_RH_2018, 'WP_M4200W42_RH_2018':WP_M4200W42_RH_2018, 'WP_M4400W44_RH_2018':WP_M4400W44_RH_2018, 'WP_M4600W46_RH_2018':WP_M4600W46_RH_2018, 'WP_M4800W48_RH_2018':WP_M4800W48_RH_2018, 'WP_M5000W50_RH_2018':WP_M5000W50_RH_2018, 'WP_M5200W52_RH_2018':WP_M5200W52_RH_2018, 'WP_M5400W54_RH_2018':WP_M5400W54_RH_2018, 'WP_M5600W56_RH_2018':WP_M5600W56_RH_2018, 'WP_M5800W58_RH_2018':WP_M5800W58_RH_2018, 'WP_M6000W60_RH_2018':WP_M6000W60_RH_2018,
    'DataMu_2018':DataMu_2018, 'DataMuA_2018':DataMuA_2018, 'DataMuB_2018':DataMuB_2018, 'DataMuC_2018':DataMuC_2018, 'DataMuD_2018':DataMuD_2018,
    'DataEle_2018':DataEle_2018, 'DataEleA_2018':DataEleA_2018, 'DataEleB_2018':DataEleB_2018, 'DataEleC_2018':DataEleC_2018, 'DataEleD_2018':DataEleD_2018,
    'DataHT_2018':DataHT_2018,'DataHTA_2018':DataHTA_2018,  'DataHTB_2018':DataHTB_2018, 'DataHTC_2018':DataHTC_2018, 'DataHTD_2018':DataHTD_2018,
}
