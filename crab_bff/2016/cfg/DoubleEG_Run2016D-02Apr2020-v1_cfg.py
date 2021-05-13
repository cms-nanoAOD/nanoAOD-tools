from WMCore.Configuration import Configuration

config = Configuration()

config.section_('General')
config.General.requestName = 'DoubleEG_Run2016D-02Apr2020-v1'
config.General.transferLogs = True
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_data.sh'
# hadd nano will not be needed once nano tools are in cmssw
config.JobType.inputFiles = ['job_2016_data_crab.py', '../../scripts/haddnano.py', 'keep_and_drop_bff.txt', 'Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt'] 
config.JobType.sendPythonFolder = True
config.section_('Data')
config.Data.inputDataset = '/DoubleEG/Run2016D-02Apr2020-v1/NANOAOD'
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 2
config.Data.lumiMask = 'Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt'

config.Data.outLFNDirBase = '/store/group/phys_exotica/bffZprime/nanoAODskimmed/crab/2016'
config.Data.publication = False
config.Data.outputDatasetTag = 'DoubleEG_Run2016D-02Apr2020-v1'
config.section_('Site')
config.Site.storageSite = 'T2_CH_CERN'
# config.section_('User')
#config.User.voGroup = 'dcms'
config.JobType.allowUndistributedCMSSW = True
