import os


#os.system("voms-proxy-init -voms cms -rfc")
def dasgo(dataset, outfile):
    os.system("dasgoclient -query='file dataset=" + dataset + " ' --json >& " + outfile +".json" )

class dataset:
    pass
'''
# WJets 2018
/WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19-v1/NANOAODSIM
/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19-v1/NANOAODSIM
/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19-v1/NANOAODSIM
/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19-v1/NANOAODSIM
/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19-v1/NANOAODSIM
/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19-v1/NANOAODSIM

# WJets 2017
/WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM
/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM
/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM
/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM
/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM
/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM

# WJets 2016
/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM
/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM
/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM
/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM
/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM
/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM

# TT 2016
/TT_Mtt-700to1000_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM
/TT_Mtt-1000toInf_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM
'''
WJets_2016 = dataset()
WJets_2016.name = "WJets"
WJets_2016.year = "2016"
WJets_2016.tag = "WJetsToLNu"
WJets_2016.HTsteps = ["HT-200To400", "HT-400To600", "HT-600To800", "HT-800To1200", "HT-1200To2500", "HT-2500ToInf"] #strip("-") for outfile name
WJets_2016.suffix = "_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM"

WJets_2017 = dataset()
WJets_2017.name = "WJets"
WJets_2017.year = "2017"
WJets_2017.tag = "WJetsToLNu"
WJets_2017.HTsteps = ["HT-200To400", "HT-400To600", "HT-600To800", "HT-800To1200", "HT-1200To2500", "HT-2500ToInf"] #strip("-") for outfile name
WJets_2017.suffix = "_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM"

WJets_2018 = dataset()
WJets_2018.name = "WJets"
WJets_2018.year = "2018"
WJets_2018.tag = "WJetsToLNu"
WJets_2018.HTsteps = ["HT-200To400", "HT-400To600", "HT-600To800", "HT-800To1200", "HT-1200To2500", "HT-2500ToInf"] #strip("-") for outfile name
WJets_2018.suffix = "_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19-v1/NANOAODSIM"  

TT_2016 = dataset()
TT_2016.name = "TT"
TT_2016.year = "2016"
TT_2016.tag = "TT"
TT_2016.HTsteps = ["Mtt-700to1000", "Mtt-1000toInf"] #strip("-") for outfile name
TT_2016.suffix = "_TuneCUETP8M2T4_13TeV-powheg-pythia8*/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM"  

datasets = [TT_2016, WJets_2016, WJets_2017, WJets_2018]

for data in datasets:
    for step in data.HTsteps:
        dasgo("/"+data.tag+"_"+step+data.suffix, data.name+"_"+step.replace("-","")+"_"+data.year)
        print "Writing files of /"+data.tag+"_"+step+data.suffix
        #os.system("more " +  data.name+"_"+step.replace("-","")+"_"+data.year+".json")






