from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'NanoPost1'
config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script.py','../scripts/haddnano.py'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder	 = True
config.section_("Data")
config.Data.inputDataset = '/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PUMoriond17_94X_mcRun2_asymptotic_v2-v1/NANOAODSIM'
config.Data.inputDBS = 'global'
#config.Data.splitting = 'FileBased'
config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 100
config.Data.totalUnits = 2000
config.Data.inputDBS='phys03'
config.Data.outLFNDirBase = '/store/user/arizzi/NanoPost/'
config.Data.publication = True
config.Data.outputDatasetTag = 'NanoTestPost'
config.section_("Site")
config.Site.storageSite = "T2_IT_Bari"

