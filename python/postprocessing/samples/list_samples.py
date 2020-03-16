import os


#os.system("voms-proxy-init -voms cms -rfc")
def dasgo(dataset, outfile):
    os.system("dasgoclient -query='file dataset=" + dataset + " ' --json >& " + outfile +".json" )

class dataset:
    pass

tag_2016 = 'RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7'
tag_2017 = 'RunIIFall17NanoAODv6-PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7'
tag_2018 = 'RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20'

WJets_2016 = dataset()
WJets_2016.name = "WJets"
WJets_2016.year = "2016"
WJets_2016.tag = "WJetsToLNu"
WJets_2016.HTsteps = ["HT-200To400", "HT-400To600", "HT-600To800", "HT-800To1200", "HT-1200To2500", "HT-2500ToInf"] #strip("-") for outfile name
WJets_2016.suffix = "_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/"+tag_2016+"-v1/NANOAODSIM"

WJets_2017 = dataset()
WJets_2017.name = "WJets"
WJets_2017.year = "2017"
WJets_2017.tag = "WJetsToLNu"
WJets_2017.HTsteps = ["HT-200To400", "HT-400To600", "HT-600To800", "HT-800To1200", "HT-1200To2500", "HT-2500ToInf"] #strip("-") for outfile name
WJets_2017.suffix = "_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2017+"-v1/NANOAODSIM"

WJets_2018 = dataset()
WJets_2018.name = "WJets"
WJets_2018.year = "2018"
WJets_2018.tag = "WJetsToLNu"
WJets_2018.HTsteps = ["HT-200To400", "HT-400To600", "HT-600To800", "HT-800To1200", "HT-1200To2500", "HT-2500ToInf"] #strip("-") for outfile name
WJets_2018.suffix = "_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2018+"-v1/NANOAODSIM"  

TT_2016 = dataset()
TT_2016.name = "TT"
TT_2016.year = "2016"
TT_2016.tag = "TT"
TT_2016.HTsteps = ["Mtt-700to1000", "Mtt-1000toInf"] #strip("-") for outfile name
TT_2016.suffix = "_TuneCUETP8M2T4_13TeV-powheg-pythia8/"+tag_2016+"-v2/NANOAODSIM"  

TT_2017 = dataset()
TT_2017.name = "TT"
TT_2017.year = "2017"
TT_2017.tag = "TT"
TT_2017.HTsteps = ["Mtt-700to1000", "Mtt-1000toInf"] #strip("-") for outfile name
TT_2017.suffix = "_TuneCP5_13TeV-powheg-pythia8/"+tag_2017+"-v1/NANOAODSIM"

TT_2018 = dataset()
TT_2018.name = "TT"
TT_2018.year = "2018"
TT_2018.tag = "TT"
TT_2018.HTsteps = ["Mtt-700to1000", "Mtt-1000toInf"] #strip("-") for outfile name
TT_2018.suffix =  "_TuneCP5_13TeV-powheg-pythia8/"+tag_2018+"-v1/NANOAODSIM"

datasets = [TT_2016, TT_2017, TT_2018, WJets_2016, WJets_2017, WJets_2018]

for data in datasets:
    for step in data.HTsteps:
        dasgo("/"+data.tag+"_"+step+data.suffix, data.name+"_"+step.replace("-","")+"_"+data.year)
        print "Writing files of /"+data.tag+"_"+step+data.suffix
        #os.system("more " +  data.name+"_"+step.replace("-","")+"_"+data.year+".json")






