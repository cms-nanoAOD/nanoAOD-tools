from WMCore.Configuration import Configuration
config = Configuration()

# https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3ConfigurationFile

config.section_("General")
config.General.requestName = 'NanoLocalDir'
config.General.transferLogs=True

config.section_("JobType")/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/PromptReco/Cert_314472-317391_13TeV_PromptReco_Collisions18_JSON.txt
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script.py','../scripts/haddnano.py', '../python/postprocessing/SlimFile.txt'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder	 = True

config.section_("Data")
config.Data.inputDataset = '/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'LumiBased' #for data

#https://twiki.cern.ch/twiki/bin/view/CMS/PdmV2017Analysis#DATA
#https://hypernews.cern.ch/HyperNews/CMS/get/physics-validation/3009.html
#config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Final/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt' # 41.86/fb
#config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt'  # 41.29/fb

#https://twiki.cern.ch/twiki/bin/view/CMS/PdmV2018Analysis#DATA
#https://hypernews.cern.ch/HyperNews/CMS/get/physics-validation/3103.html
#config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/PromptReco/Cert_314472-317391_13TeV_PromptReco_Collisions18_JSON.txt' # 14.383/fb

config.Data.unitsPerJob = 1
config.Data.totalUnits = 3
#config.Data.inputDBS='phys03'
config.Data.outLFNDirBase = '/store/user/username/nanoAODcrab'
config.Data.publication = True
config.Data.outputDatasetTag = 'Test17May2018'

config.section_("Site")
config.Site.storageSite = "T2_ES_IFCA"

