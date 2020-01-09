import sys
from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB


config = Configuration()

version = "PROD_7_7"

datasetToTest = [] ## if empty, run on all datasets
#datasetToTest = ["/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/arizzi-RunIISummer16MiniAODv3_FSRmyNanoProdMc2017_NANOV4a_017_realistic_v14-v1-35a58109e00c38928fe6fe04f08bafb3/USER"] ## if empty, run on all datasets
#datasetToTest = ["/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/arizzi-RunIISummer16MiniAODv3_FSRmyNanoProdMc2018_NANOV4c_018_realistic_v15-v1-f77ac490c2015e446b4336e158bd70bc/USER"] ## if empty, run on all datasets
#datasetToTest = ["/DYJetsToLL_M-105To160_TuneCP5_PSweights_13TeV-amcatnloFXFX-pythia8/arizzi-RunIISummer16MiniAODv3_FSRmyNanoProdMc2017_NANOV4i_017_realistic_v14-v1-35a58109e00c38928fe6fe04f08bafb3/USER"] ## if empty, run on all datasets
#datasetToTest = ['/DYJetsToLL_M-105To160_TuneCP5_PSweights_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19-v1/NANOAODSIM']

requestsToSkip = [
]

requestsToTest = [ 
#"PROD_7_7_DY105VBF_2016AMCPY_ext2",
#"PROD_7_7_DY105VBF_2016AMCPY_ext1"
#"PROD_7_7_DY1J_2016AMCPY",
"PROD_7_7_DY1J_2016AMCPY_ext1",
"PROD_7_7_DY2J_2016AMCPY_ext1"
#"PROD_7_7_WminusHmm_2016POWPY",
#"PROD_6_3_bbHmm_2016AMCPY",
#"PROD_6_4_DY105VBF_2016MGPY",
#"PROD_7_2_DY105_2018AMCPY",
#"PROD_7_3_ZmmJJ_2016POWPY",
#"PROD_6_2_ZmmJJv5_2016POWPY"
#"PROD_7_3_STs_2016AMCPY",
#"PROD_7_3_STwtbar_2016POWPY",
#"PROD_7_3_STwt_2016POWPY",
#"PROD_7_3_STtbar_2016POW_MADSPIN_PY",
#"PROD_7_3_STt_2016POW_MADSPIN_PY",
#"PROD_7_4_TT_2016POWPY",
#"PROD_7_3_TTlep_2016POWPY",
#"PROD_7_3_TTsemi_2016POWPY",
#"PROD_7_3_TThad_2016POWPY",
#"PROD_7_3_TT_2016POWHERWIG",
#"PROD_7_1_SingleMuonRun2016"
#"PROD_6_4_DY105VBF_2016AMCPY"
## if empty, run on all datasets
#"PROD_4_1_others_2017",
#"PROD_4_1_others_2018",
#"PROD_4_1_d_W2J_2018AMCPY_ext1",
#    "PROD_2_0_EWKZ_2018MGHERWIG",
#    "PROD_2_0_WWJJlnln_2017MGPY",
#    "PROD_2_0_EWKZ105_2016MGHERWIG",
] ## if empty, run on all datasets



#def getModuleSettingsFromDataset(dataset):
    #datasetTag = dataset.split("/")[2]
    #if "RunIIAutumn18" in datasetTag: return 'mc2018'
    #elif "RunIIFall17" in datasetTag: return 'mc2017'
    #elif "RunIISummer16" in datasetTag: return 'mc2016'
    #elif "Run2016" in datasetTag: return 'data2016'
    #elif "Run2017" in datasetTag: return 'data2017'
    #elif "Run2018A" in datasetTag: return 'data2018A'
    #elif "Run2018B" in datasetTag: return 'data2018B'
    #elif "Run2018C" in datasetTag: return 'data2018C'
    #elif "Run2018D" in datasetTag: return 'data2018D'
    #else: raise Exception("Unable to find module settings for %s"%dataset)

def getModuleSettingsFromSampleName(sample):
    if   "_2018" in sample: return 'mc2018'
    elif "_2017" in sample: return 'mc2017'
    elif "_2016" in sample: return 'mc2016'
    #elif "RunIISummer16NanoAODv6" in datasetTag: return 'mc2016'
    #elif "RunIISummer16NanoAODv5" in datasetTag: return 'mc2016'
    elif "nlu-RunIISummer16MiniAODv3" in sample: return 'mc2016'
    elif "FSRmyNanoProdMc2017" in sample: return 'mc2017'
    elif "FSRmyNanoProdMc2018" in sample: return 'mc2018'
    elif "SingleMuon" in sample: return 'data2016'
    elif "Run2016" in sample: return 'data2016'
    elif "Run2017" in sample: return 'data2017'
    elif "Run2018A" in sample: return 'data2018A'
    elif "Run2018B" in sample: return 'data2018B'
    elif "Run2018C" in sample: return 'data2018C'
    elif "Run2018D" in sample: return 'data2018D'
    else: raise Exception("Unable to find module settings for %s"%dataset)

config.section_("General")
config.General.transferLogs=True
config.General.workArea = '/home/users/sdonato/scratchssd/crab/'#+version
config.General.workArea = '/afs/cern.ch/work/g/gimandor/public/testNANOAOD'#+version

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
#config.JobType.psetName = 'PSet1.py'
#config.JobType.maxMemoryMB=2500

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
#config.Data.unitsPerJob = 10
config.Data.unitsPerJob = 1
#config.Data.totalUnits = 1 ## for testing


config.Data.outLFNDirBase = '/store/user/sdonato/'+version+'/'
config.Data.outLFNDirBase = '/store/user/gimandor/'+version+'/'
config.Data.publication = True
config.section_("Site")
config.Site.ignoreGlobalBlacklist = True
#config.Data.ignoreLocality = True
#config.Site.storageSite = "T2_IT_Bari"
config.Site.storageSite = "T2_IT_Legnaro"
#config.Site.storageSite = "T2_IT_Pisa"

#config.Data.ignoreLocality = True
#config.Site.whitelist = ['T2_US_*']

config.JobType.allowUndistributedCMSSW = True

from datasets2016NANOv6 import data2016, mc2016
#from datasets2016AndreaV7 import data2016, mc2016
from datasets2017AndreaV7 import data2017, mc2017
from datasets2018AndreaV7 import data2018, mc2018

#from datasets2018NANOv6 import data2018, mc2018
#from datasetsTest import data2018, mc2018

datasetsNames = ["mc2016","mc2017","mc2018","data2016","data2017","data2018"]
#datasetsNames = ["mc2017","data2017", "mc2016","data2016"]
datasetsNames = ["mc2018","data2018"]
datasetsNames = ["mc2016","data2016"]
#datasetsNames = ["mc2017", "mc2018"]

from checker import checkDatasets
#checkDatasets(datasetsNames, globals())

from CRABAPI.RawCommand import crabCommand

requestNames = set()
if __name__ == '__main__':
    for datasetsName in datasetsNames:
        datasets = globals()[datasetsName]
        samples = datasets.keys()
        for sample in samples:
            for dataset in datasets[sample]:
                if type(dataset) != str: continue
#                print "New job"
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
		print requestName
                if requestName in requestsToSkip: continue
                #print "requestName and requestsToTest 1 ", requestName, requestsToTest
                if requestsToTest and not requestName in requestsToTest: continue ## run only requestsToTest, if filled 
                #print "requestName and requestsToTest 2 ", requestName, requestsToTest
                config.General.requestName = requestName
                config.Data.outputDatasetTag = version+"_"+dataset.split("/")[-2]
#                config.JobType.scriptExe = 'crab_script_%s.sh'%getModuleSettingsFromDataset(dataset)
                print "AAA ", sample
                config.JobType.scriptExe = 'crab_script_%s.sh'%getModuleSettingsFromSampleName(sample)
                print
                print config
                print
#                try:
                if True:
                    crabCommand('submit', config = config, dryrun = False) ## dryrun = True for local test
                    print "DONE"
 #               except:
 #                   print('crab submission failed. Move the the next job. %s'%requestName)
