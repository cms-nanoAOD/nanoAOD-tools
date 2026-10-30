from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config#, getUsernameFromSiteDB

config = Configuration()

config.section_("General")

config.General.requestName = 'Tchannel_mtop1695_Tree_UL2016_Alt_mass'

config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_NanoGen_skimtree.sh'
#config.JobType.maxMemoryMB = 4000
config.JobType.inputFiles = ['crab_script_NanoGen_skimtree.py','Gen_mass_reconstract_ttbar.py','../../scripts/haddnano.py','clean_All_keep_GenPart.txt','Gen_mass_reconstract_SingleTop.py','Gen_mass_functions.py']
#config.JobType.sendPythonFolder=True # this configration line has been deprecated
config.section_("Data")

config.Data.inputDataset = '/ST_t-channel_top_4f_InclusiveDecays_mtop1695_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM'

config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1

config.Data.outLFNDirBase = '/store/user/mikumar/RUN2_UL/Tree_crab/SIXTEEN/Mc_NANOGEN_v9/Tchannel_mtop1695'

config.Data.publication = False

config.Data.outputDatasetTag = 'Tree_06_Jan26_MCUL2016_Alt_mass_Tchannel_mtop1695_v9'

config.section_("Site")
config.Site.storageSite = 'T3_CH_CERNBOX'

#config.Site.storageSite = "T2_CH_CERN"
#config.section_("User")
#config.User.voGroup = 'dcms'
