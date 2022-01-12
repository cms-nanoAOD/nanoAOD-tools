mc_template='''from WMCore.Configuration import Configuration

config = Configuration()

config.section_('General')
config.General.requestName = '{requestName}'
config.General.transferLogs = False
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_mc_{btag_type}.sh'
# hadd nano will not be needed once nano tools are in cmssw
config.JobType.inputFiles = ['job_mc_crab_{btag_type}.py', '../../scripts/haddnano.py', 'keep_and_drop_bff.txt']
config.JobType.sendPythonFolder = True
config.section_('Data')
config.Data.inputDataset = '{das}'
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 2

config.Data.outLFNDirBase = '/store/group/phys_exotica/bffZprime/nanoAODskimmed/crab/{era}'
config.Data.publication = False
config.Data.outputDatasetTag = '{outputName}_{btag_type}'
config.section_('Site')
config.Site.storageSite = 'T2_CH_CERN'
# config.section_('User')
#config.User.voGroup = 'dcms'
config.JobType.allowUndistributedCMSSW = True
'''
data_template='''from WMCore.Configuration import Configuration

config = Configuration()

config.section_('General')
config.General.requestName = '{requestName}'
config.General.transferLogs = False
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_data_{btag_type}.sh'
# hadd nano will not be needed once nano tools are in cmssw
config.JobType.inputFiles = ['job_data_crab_{btag_type}.py', '../../scripts/haddnano.py', 'keep_and_drop_bff.txt', '{json}''] 
config.JobType.sendPythonFolder = True
config.section_('Data')
config.Data.inputDataset = '{das}'
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 1
config.Data.lumiMask = '{json}''

config.Data.outLFNDirBase = '/store/group/phys_exotica/bffZprime/nanoAODskimmed/crab/{era}'
config.Data.publication = False
config.Data.outputDatasetTag = '{outputName}_{btag_type}'
config.section_('Site')
config.Site.storageSite = 'T2_CH_CERN'
# config.section_('User')
#config.User.voGroup = 'dcms'
config.JobType.allowUndistributedCMSSW = True
'''
