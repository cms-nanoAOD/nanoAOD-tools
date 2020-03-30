from WMCore.Configuration import Configuration

config = Configuration()
config.section_('General')
config.General.requestName = 'TT_Mtt1000toInf_2017'
config.General.transferLogs=True
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script.py','../scripts/haddnano.py', '../scripts/keep_and_drop.txt']
config.JobType.sendPythonFolder = True
config.section_('Data')
config.Data.inputDataset = '/TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv6-PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1/NANOAODSIM'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 2
config.Data.outLFNDirBase = '/store/user/%s/%s' % ('adeiorio', 'OutDir')
config.Data.publication = False
config.Data.outputDatasetTag = 'TT_Mtt1000toInf_2017'
config.section_('Site')
config.Site.storageSite = 'T2_IT_Pisa'
