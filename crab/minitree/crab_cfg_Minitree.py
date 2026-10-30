from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config#, getUsernameFromSiteDB

config = Configuration()

config.section_("General")

#2016 MC
config.General.requestName = 'Run2016C_preVFP_mu_Minitree_2J1T1_UL2016preVFP'

config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_Minitree.sh'
config.JobType.inputFiles = ['crab_script_Minitree.py','../../scripts/haddnano.py','foxwol_n_fourmomentumSolver.py','MinitreeModule.py','cut_strings.py','keep_and_drop_mu_Minitree.txt','keep_and_drop_el_Minitree.txt','jme.py','Mc_prob_cal_forBweght.py','scaleFactor.py','KinFit.C']
#hadd nano will not be needed once nano tools are in cmssw
#config.JobType.outputFiles = ['B_DeepCSV_Efficiency.root']
config.JobType.sendPythonFolder	 = True
config.section_("Data")

config.Data.inputDataset = '/SingleMuon/mikumar-Tree_20_Apr22_Run2016C-HIPM_mu-11cca84e9421f041a8fcb7fd41edd277/USER'

config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
#config.Data.totalUnits = 1

config.Data.outLFNDirBase = '/store/user/mikumar/RUN2/MiniTree_crab/SIXTEEN/Data/check/2J1T1_mu_new/Run2016C_preVFP_mu'

config.Data.publication = False

config.Data.outputDatasetTag = 'MiniTree_02_May22_Run2016C_preVFP_mu'

config.section_("Site")
config.Site.storageSite = 'T2_IN_TIFR'
#config.Site.whitelist = ['T2_IN_TIFR']

#config.Site.storageSite = "T2_CH_CERN"
#config.section_("User")
#config.User.voGroup = 'dcms'

