from WMCore.Configuration import Configuration

config = Configuration()
config.section_('General')
config.General.requestName = 'DataMu_RunB2017'
config.General.transferLogs=True
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script.py','../scripts/haddnano.py', '../scripts/keep_and_drop.txt']
config.JobType.sendPythonFolder = True
config.section_('Data')
config.Data.inputDataset = '/SingleMuon/Run2017B-Nano25Oct2019-v1/NANOAOD'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt'
config.Data.unitsPerJob = 25
config.Data.outLFNDirBase = '/store/user/%s/%s' % ('adeiorio', 'OutDir')
config.Data.publication = False
config.Data.outputDatasetTag = 'DataMu_RunB2017'
config.section_('Site')
config.Site.storageSite = 'T2_IT_Pisa'
