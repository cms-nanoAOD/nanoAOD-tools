template_data='''from WMCore.Configuration import Configuration

config = Configuration()

config.section_('General')
config.General.requestName = '{NanoPost1}'
config.General.transferLogs = True
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_data.sh'
# hadd nano will not be needed once nano tools are in cmssw
config.JobType.inputFiles = ['job_2017_data_crab.py', '../../scripts/haddnano.py', 'keep_and_drop_bff.txt', 'Cert_314472-325175_13TeV_17SeptEarlyReReco2017ABC_PromptEraD_Collisions18_JSON.txt']
config.JobType.sendPythonFolder = True
config.section_('Data')
config.Data.inputDataset = '{das}'
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 2
config.Data.lumiMask = 'Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt'

config.Data.outLFNDirBase = '/store/group/phys_exotica/bffZprime/nanoAODskimmed/2017'
config.Data.publication = False
config.Data.outputDatasetTag = '{NanoTestPost}'
config.section_('Site')
config.Site.storageSite = 'T2_CH_CERN'
# config.section_('User')
#config.User.voGroup = 'dcms'
config.JobType.allowUndistributedCMSSW = True
'''
