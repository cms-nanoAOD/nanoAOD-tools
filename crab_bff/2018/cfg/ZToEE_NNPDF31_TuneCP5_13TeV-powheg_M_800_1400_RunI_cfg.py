from WMCore.Configuration import Configuration

config = Configuration()

config.section_('General')
config.General.requestName = 'ZToEE_NNPDF31_TuneCP5_13TeV-powheg_M_800_1400_RunI'
config.General.transferLogs = True
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_mc.sh'
# hadd nano will not be needed once nano tools are in cmssw
config.JobType.inputFiles = ['job_2018_mc_crab.py', '../../scripts/haddnano.py', 'keep_and_drop_bff.txt']
config.JobType.sendPythonFolder = True
config.section_('Data')
config.Data.inputDataset = '/ZToEE_NNPDF31_TuneCP5_13TeV-powheg_M_800_1400/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM'
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 2

config.Data.outLFNDirBase = '/store/group/phys_exotica/bffZprime/nanoAODskimmed/2018'
config.Data.publication = False
config.Data.outputDatasetTag = 'ZToEE_NNPDF31_TuneCP5_13TeV-powheg_M_800_1400_RunI'
config.section_('Site')
config.Site.storageSite = 'T2_CH_CERN'
# config.section_('User')
#config.User.voGroup = 'dcms'
config.JobType.allowUndistributedCMSSW = True
