#from WMCore.Configuration import Configuration
#from CRABClient.UserUtilities import config #getUsernameFromSiteDB
from CRABClient.UserUtilities import config as Configuration

version="__T"

import os 
base = os.environ["CMSSW_BASE"]

config = Configuration()

config.section_("General")
config.General.requestName = 'skimNano-TestUL'
config.General.transferLogs = True
 
config.General.workArea = base+'/..'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_ggOnly.sh'
#config.JobType.scriptArgs= "foo"
# hadd nano will not be needed once nano tools are in cmssw
config.JobType.inputFiles = ['crab_script_ggOnly.py', '../scripts/haddnano.py', 'keep_and_drop.txt']
config.JobType.sendPythonFolder = True

config.JobType.allowUndistributedCMSSW = True #shouldn't be necessary

config.section_("Data")
#config.Data.inputDataset = '/DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'
config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'


aaa=[
"/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM",
"/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v2/NANOAODSIM",
"/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM",
"/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
]


mc16a=["/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM",]
mc16b=["/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v2/NANOAODSIM",]
mc17=["/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM",]
mc18=["/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",]

#drwxrwxr-x 11 fsetti fsetti 4,0K 15 feb 16.58 /hadoop/cms/store/user/fsetti/Summer20UL_nanoAODv9/GluGluToHHTo2G2Tau_node_cHHH1_TuneCP5_13TeV-powheg-pythia8_2016_APV_final
#drwxrwxr-x 11 fsetti fsetti 4,0K 15 feb 19.08 /hadoop/cms/store/user/fsetti/Summer20UL_nanoAODv9/GluGluToHHTo2G2Tau_node_cHHH1_TuneCP5_13TeV-powheg-pythia8_2016_final
#drwxrwxr-x 21 fsetti fsetti 4,0K 15 feb 19.36 /hadoop/cms/store/user/fsetti/Summer20UL_nanoAODv9/GluGluToHHTo2G2Tau_node_cHHH1_TuneCP5_13TeV-powheg-pythia8_2018_final
#drwxrwxr-x 21 fsetti fsetti 4,0K 15 feb 21.09 /hadoop/cms/store/user/fsetti/Summer20UL_nanoAODv9/GluGluToHHTo2G2Tau_node_cHHH1_TuneCP5_13TeV-powheg-pythia8_2017_final


#config.Data.splitting = 'FileBased'
config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 10
config.Data.totalUnits = 10 #override

config.Data.outLFNDirBase = '/store/user/legianni/skimNano-TestUL'+version # cannot getUsernameFromSiteDB
config.Data.publication = False
#config.Data.outputDatasetTag = 'skimNano-TestUL'+version

config.section_("Site")
config.Site.storageSite = "T2_US_UCSD"

from CRABAPI.RawCommand import crabCommand



counter=21

opds={}

for sample in aaa:
  
    path=""
    
    if sample in mc16a:
      config.JobType.scriptArgs=["arg=16a"] #it seems this is not working without the = sign!!!
      config.Data.inputDataset=sample
    if sample in mc16b:
      config.JobType.scriptArgs=["arg=16b"]
      config.Data.inputDataset=sample
    if sample in mc17:
      config.JobType.scriptArgs=["arg=17"]
      config.Data.inputDataset=sample
    if sample in mc18:
      config.JobType.scriptArgs=["arg=18"]
      config.Data.inputDataset=sample


    config.Data.outputDatasetTag = 'skimNano-TestUL_'+sample.split("/")[1].split("-")[0]+"_"+sample.split("/")[2].split("-")[0]
    config.General.requestName = 'skimNano-TestUL'+sample.split("/")[1][0:30]+"--"+str(counter)
    print config
    crabCommand('submit', config = config, dryrun = False) ## dryrun = True for local test
    print "DONE"
    
    counter+=1
    
    #break
