from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config

config = Configuration()

config.section_("General")

#2016 MC
config.General.requestName = 'QCD_Pt-300toInf_EMEnriched_Effi'

config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['clean.txt','crab_efficiency.py','../scripts/haddnano.py','keep_and_drop.txt','EfficiencyModule.py'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.outputFiles = ['B_DeepCSV_Efficiency.root']
config.JobType.sendPythonFolder	 = True
config.section_("Data")

#2016 MC
config.Data.inputDataset = '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM'

#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 1

#2016 MC
config.Data.outLFNDirBase = '/store/user/mikumar/RUN2/Efficiency_crab/Seventeen/QCD_Pt-300toInf_EMEnriched'

config.Data.publication = False

#2016 MC
config.Data.outputDatasetTag = 'Effi_sep_seventeen_QCD_Pt-300toInf_EMEnriched'

config.section_("Site")
config.Site.storageSite = "T2_IN_TIFR"

#config.Site.storageSite = "T2_CH_CERN"
#config.section_("User")
#config.User.voGroup = 'dcms'
