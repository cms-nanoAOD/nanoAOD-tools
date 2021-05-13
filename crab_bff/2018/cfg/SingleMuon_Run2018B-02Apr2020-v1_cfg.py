from WMCore.Configuration import Configuration

config = Configuration()

config.section_('General')
config.General.requestName = 'SingleMuon_Run2018B-02Apr2020-v1'
config.General.transferLogs = True
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_data.sh'
# hadd nano will not be needed once nano tools are in cmssw
config.JobType.inputFiles = ['job_2018_data_crab.py', '../../scripts/haddnano.py', 'keep_and_drop_bff.txt', 'Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt']
config.JobType.sendPythonFolder = True
config.section_('Data')
config.Data.inputDataset = '/SingleMuon/Run2018B-02Apr2020-v1/NANOAOD'
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 2
config.Data.lumiMask = 'Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt'

config.Data.outLFNDirBase = '/store/group/phys_exotica/bffZprime/nanoAODskimmed/2018'
config.Data.publication = False
config.Data.outputDatasetTag = 'SingleMuon_Run2018B-02Apr2020-v1'
config.section_('Site')
config.Site.storageSite = 'T2_CH_CERN'
# config.section_('User')
#config.User.voGroup = 'dcms'
config.JobType.allowUndistributedCMSSW = True
