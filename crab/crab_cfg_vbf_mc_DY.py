from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB

config = Configuration()

config.section_("General")
config.General.requestName = 'DYJetsToLL_1J_MC_test_two_modules'
config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_vbf_mc.sh'
config.JobType.inputFiles = ['crab_script_vbf_mc.py','../scripts/haddnano.py'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder	 = True
config.section_("Data")
config.Data.inputDataset = '/DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'Automatic'
#config.Data.splitting = 'EventAwareLumiBased'
#config.Data.unitsPerJob = 2
#config.Data.totalUnits = 10

config.Data.outLFNDirBase = '/store/user/vmilosev'
config.Data.publication = False
config.Data.outputDatasetTag = 'NanoTestPostDY'
config.section_("Site")
config.Site.storageSite = "T2_UK_London_IC"

#config.Site.storageSite = "T2_CH_CERN"
#config.section_("User")
#config.User.voGroup = 'dcms'

