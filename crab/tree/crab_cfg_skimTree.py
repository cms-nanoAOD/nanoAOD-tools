from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config

config = Configuration()

config.section_("General")

config.General.requestName = 'DYJetsToLL_Tree_UL2016postVFP'

config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_skimTree.sh'
config.JobType.maxMemoryMB = 4000
config.JobType.inputFiles = ['crab_script_skimTree.py','../../scripts/haddnano.py','keep_and_drop.txt','MainModule.py']
#config.JobType.sendPythonFolder=True
config.section_("Data")

config.Data.inputDataset = '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1/NANOAODSIM'

config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
#config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt'

config.Data.outLFNDirBase = '/store/user/mikumar/RUN2_UL/Tree_crab/SIXTEEN/MC_postVFP/DYJetsToLL'

config.Data.publication = False

config.Data.outputDatasetTag = 'Tree_14_Jul24_MCUL2016postVFP_DYJetsToLL'

config.section_("Site")
config.Site.storageSite = 'T3_CH_CERNBOX'
