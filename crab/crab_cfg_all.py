import sys
from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB


config = Configuration()

version = "PROD_4_0"

datasetToTest = [] ## if empty, run on all datasets
#datasetToTest = ['/DYJetsToLL_M-105To160_TuneCP5_PSweights_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19-v1/NANOAODSIM']

requestsToSkip = [
]

requestsToTest = [ ## if empty, run on all datasets
#    "PROD_2_0_EWKZ_2018MGHERWIG",
#    "PROD_2_0_WWJJlnln_2017MGPY",
#    "PROD_2_0_EWKZ105_2016MGHERWIG",
] ## if empty, run on all datasets


def getModuleSettingsFromDataset(dataset):
    datasetTag = dataset.split("/")[2]
    if "RunIIAutumn18" in datasetTag: return 'mc2018'
    elif "RunIIFall17" in datasetTag: return 'mc2017'
    elif "RunIISummer16" in datasetTag: return 'mc2016'
    elif "Run2016" in datasetTag: return 'data2016'
    elif "Run2017" in datasetTag: return 'data2017'
    elif "Run2018A" in datasetTag: return 'data2018A'
    elif "Run2018B" in datasetTag: return 'data2018B'
    elif "Run2018C" in datasetTag: return 'data2018C'
    elif "Run2018D" in datasetTag: return 'data2018D'
    else: raise Exception("Unable to find module settings for %s"%dataset)


config.section_("General")
config.General.transferLogs=True
config.General.workArea = '/home/users/sdonato/scratchssd/crab/'#+version
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'

config.JobType.inputFiles = ['crab_script_all.py','checker.py','../scripts/haddnano.py']

print "inputFiles ", config.JobType.inputFiles
config.JobType.sendPythonFolder         = True
config.section_("Data")
#config.Data.inputDataset = '/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PUMoriond17_94X_mcRun2_asymptotic_v2-v1/NANOAODSIM'
config.Data.inputDBS = 'global'
#config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.allowNonValidInputDataset=True
#config.Data.splitting = 'Automatic'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 1
#config.Data.totalUnits = 1 ## for testing

config.Data.outLFNDirBase = '/store/user/sdonato/'+version+'/'
config.Data.publication = True
config.section_("Site")
#config.Site.storageSite = "T2_IT_Bari"
config.Site.storageSite = "T2_IT_Legnaro"
#config.Site.storageSite = "T2_IT_Pisa"

config.JobType.allowUndistributedCMSSW = True

from datasets2016 import data2016, mc2016
from datasets2017 import data2017, mc2017
from datasets2018 import data2018, mc2018
#from datasetsTest import data2018, mc2018

datasetsNames = ["data2018", "mc2018", "data2017", "mc2017", "data2016", "mc2016"]

from checker import checkDatasets
checkDatasets(datasetsNames, globals())

from CRABAPI.RawCommand import crabCommand

requestNames = set()
if __name__ == '__main__':
    for datasetsName in datasetsNames:
        datasets = globals()[datasetsName]
        samples = datasets.keys()
        for sample in samples:
            for dataset in datasets[sample]:
                print "New job"
                if datasetToTest and not dataset in datasetToTest: continue ## run only datasetToTest, if filled 
                config.Data.inputDataset = dataset
                config.Data.lumiMask = None
                if dataset == data2016 : 
                    config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt'
                if dataset == data2017 : 
                    config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt'
                if dataset == data2018 : 
                    config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt'
                ext = ''
                if "_ext" in dataset: 
                    ext = '_ext' + dataset.split("_ext")[1][0]
                requestName = version + "_" + sample +  ext
                while requestName in requestNames:
                    requestName = requestName+"_"        
                requestNames.add(requestName)
                if requestName in requestsToSkip: continue
                if requestsToTest and not requestName in requestsToTest: continue ## run only requestsToTest, if filled 
                config.General.requestName = requestName
                config.Data.outputDatasetTag = version+"_"+dataset.split("/")[-2]
                config.JobType.scriptExe = 'crab_script_%s.sh'%getModuleSettingsFromDataset(dataset)
                print
                print config
                print
                try:
                    crabCommand('submit', config = config, dryrun = False) ## dryrun = True for local test
                    print "DONE"
                except:
                    print('crab submission failed. Move the the next job')
