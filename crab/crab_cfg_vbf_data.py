from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB

config = Configuration()

config.section_("General")
config.General.requestName = 'MET_dataset'
config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_vbf_data.sh'
config.JobType.inputFiles = ['crab_script_vbf_data.py','../scripts/haddnano.py'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder	 = True
config.section_("Data")
#config.Data.inputDataset = '/DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 30000
#config.Data.unitsPerJob = 2
#config.Data.totalUnits = 10

config.Data.outLFNDirBase = '/store/user/vmilosev'
config.Data.publication = False
#config.Data.outputDatasetTag = 'NanoTestPost'
config.section_("Site")
config.Site.storageSite = "T2_UK_London_IC"

#config.Site.storageSite = "T2_CH_CERN"
#config.section_("User")
#config.User.voGroup = 'dcms'



if 1 == 1:

    from CRABAPI.RawCommand import crabCommand
    from CRABClient.ClientExceptions import ClientException
    from httplib import HTTPException

    # We want to put all the CRAB project directories from the tasks we submit here into one common directory.
    # That's why we need to set this parameter (here or above in the configuration file, it does not matter, we will not overwrite it).

    def submit(inconfig):
        try:
            crabCommand('submit', config = inconfig)
#            crabCommand('status')
        except HTTPException as hte:
            print "Failed submitting task: %s" % (hte.headers)
        except ClientException as cle:
            print "Failed submitting task: %s" % (cle)

    #############################################################################################
    ## From now on that's what users should modify: this is the a-la-CRAB2 configuration part. ##
    #############################################################################################

    tasks=list()
    json= '/afs/cern.ch/work/v/vmilosev/VBFHToInv-nanoAOD-tools/181020/CMSSW_10_2_5/src/PhysicsTools/NanoAODTools/crab/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt'
    #Runs
    tasks.append(('MET-2017B-24Oct18-v3','/MET/Run2017B-31Mar2018-v1/NANOAOD',json))
    tasks.append(('MET-2017C-24Oct18-v3','/MET/Run2017C-31Mar2018-v1/NANOAOD',json))
    tasks.append(('MET-2017D-24Oct18-v3','/MET/Run2017D-31Mar2018-v1/NANOAOD',json))
    tasks.append(('MET-2017E-24Oct18-v3','/MET/Run2017E-31Mar2018-v1/NANOAOD',json))
    tasks.append(('MET-2017F-24Oct18-v3','/MET/Run2017F-31Mar2018-v1/NANOAOD',json))
    
 
    for task in tasks:
        print task[0]
        config.General.requestName = task[0]
        config.Data.inputDataset = task[1]
        config.Data.outputDatasetTag = 'NanoTest'+task[0]
        config.Data.lumiMask = task[2]
        submit(config)
