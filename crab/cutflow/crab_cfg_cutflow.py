from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config#, getUsernameFromSiteDB

config = Configuration()

config.section_("General")

#2016 MC
config.General.requestName = 'Tbarchannel_cutflow2J1T1_mu_UL2016preVFP'

config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_cutflow.sh'
config.JobType.inputFiles = ['ElectronSF','MuonSF','scaleFactor.py','crab_script_cutflow.py','../../scripts/haddnano.py','Mc_prob_cal_forBweght.py','cutflowModule.py','clean.txt']
#hadd nano will not be needed once nano tools are in cmssw
config.JobType.outputFiles = ['Cutflow_hist.root']
config.JobType.sendPythonFolder	 = True
config.section_("Data")

config.Data.inputDataset = '/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/mikumar-Tree_22_Apr22_MCUL2016preVFP_Tbarchannel_check-8957b29c601d60219f5188b9be2eb225/USER'

config.Data.inputDBS = 'phys03'
#config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'LumiBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 1
#config.Data.totalUnits = 1

config.Data.outLFNDirBase = '/store/user/mikumar/RUN2/cutflow_crab/SIXTEEN/Mc/2J1T1_mu/Tbarchannel'

config.Data.publication = False

config.Data.outputDatasetTag = 'CutFlow_11_May22_Tbarchannel'

config.section_("Site")
config.Site.storageSite = "T2_IN_TIFR"

#config.Site.storageSite = "T2_CH_CERN"
#config.section_("User")
#config.User.voGroup = 'dcms'
