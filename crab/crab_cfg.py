from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB

config = Configuration()
config.section_('General')
config.General.requestName = 'TT_Mtt700to1000_2016'
config.General.transferLogs=True
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script_prova.py','../scripts/haddnano.py']
config.JobType.sendPythonFolder = True
config.section_('Data')
config.Data.inputDataset = '/TT_Mtt-700to1000_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.outLFNDirBase = '/store/user/%s/%s' % (getUsernameFromSiteDB(), 'OutDir')
config.Data.publication = False
config.Data.outputDatasetTag = 'TT_Mtt700to1000_2016'
config.section_('Site')
config.Site.storageSite = 'T2_IT_Pisa'
