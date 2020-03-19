from WMCore.Configuration import Configuration

config = Configuration()
config.section_('General')
config.General.requestName = 'DataMu_RunF2017'
config.General.transferLogs=True
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script_prova.py','../scripts/haddnano.py']
config.JobType.sendPythonFolder = True
config.section_('Data')
config.Data.inputDataset = '/SingleMuon/Run2017F-Nano25Oct2019-v1/NANOAOD'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 3
config.Data.outLFNDirBase = '/store/user/%s/%s' % ('adeiorio', 'OutDir')
config.Data.publication = False
config.Data.outputDatasetTag = 'DataMu_RunF2017'
config.section_('Site')
config.Site.storageSite = 'T2_IT_Pisa'
