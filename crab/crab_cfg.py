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
config.Data.inputDataset = '/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/arizzi-NanoTest2-507dabe3d10b654abb8ddc59357bce9a/USER'
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

