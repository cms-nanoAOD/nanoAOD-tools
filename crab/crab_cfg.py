import sys
from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB

config = Configuration()

version = "Z178"
#version = "141"



era = "2016"
data = "MC"
f=open(sys.argv[1]) 
if sys.argv[1].startswith("samples_2016") : era = "2016"
if sys.argv[1].startswith("samples_2017") : era = "2017"
if sys.argv[1].startswith("samples_2018") : era = "2018"


config.section_("General")
config.General.requestName = 'NanoPost8'
config.General.transferLogs=True
config.General.workArea = '/afs/cern.ch/work/g/gimandor/public/testNANOAOD'#+version
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'

if era == "2016" : config.JobType.scriptExe = 'crab_script2016.sh'
if era == "2017" : config.JobType.scriptExe = 'crab_script2017.sh'
if era == "2018" : 
    if   version.endswith("A") : config.JobType.scriptExe = 'crab_script2018A.py'
    elif version.endswith("B") : config.JobType.scriptExe = 'crab_script2018B.py'
    elif version.endswith("C") : config.JobType.scriptExe = 'crab_script2018C.py'
    elif version.endswith("D") : config.JobType.scriptExe = 'crab_script2018D.py'
    else : config.JobType.scriptExe = 'crab_script2018.sh'


if era == "2016" : config.JobType.inputFiles = ['crab_script2016.py','../scripts/haddnano.py']
if era == "2017" : config.JobType.inputFiles = ['crab_script2017.py','../scripts/haddnano.py']
if era == "2018" : 
    if   version.endswith("A") : config.JobType.inputFiles = ['crab_script2018A.py','../scripts/haddnano.py']
    elif version.endswith("B") : config.JobType.inputFiles = ['crab_script2018B.py','../scripts/haddnano.py']
    elif version.endswith("C") : config.JobType.inputFiles = ['crab_script2018C.py','../scripts/haddnano.py']
    elif version.endswith("D") : config.JobType.inputFiles = ['crab_script2018D.py','../scripts/haddnano.py']
    else : config.JobType.inputFiles = ['crab_script2018.py','../scripts/haddnano.py']


print config.JobType.inputFiles
#config.JobType.inputFiles = ['crab_script.py','../scripts/haddnano.py'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder	 = True
config.section_("Data")
#config.Data.inputDataset = '/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PUMoriond17_94X_mcRun2_asymptotic_v2-v1/NANOAODSIM'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.allowNonValidInputDataset=True
#config.Data.splitting = 'Automatic'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 5
#config.Data.totalUnits = 2000
#config.Data.inputDBS='global'#'phys03'
config.Data.outLFNDirBase = '/store/user/gimandor/'
config.Data.publication = True
config.Data.outputDatasetTag = 'NanoTestPost5'
#config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions16/13TeV/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt'
config.section_("Site")
#config.Site.storageSite = "T2_IT_Bari"
config.Site.storageSite = "T2_IT_Legnaro"
#config.Site.storageSite = "T2_IT_Pisa"



sites=['T2_IT_Pisa']
extentionPostname = ["_ext10", "_ext9", "_ext8", "_ext7", "_ext6", "_ext5", "_ext4", "_ext3", "_ext2", "_ext1"]







if __name__ == '__main__':

    #era = "2016"
    #data = "MC"
    #f=open(sys.argv[1]) 
    #if sys.argv[1].startswith("samples_2016") : era = "2016"
    #if sys.argv[1].startswith("samples_2017") : era = "2017"
    #if sys.argv[1].startswith("samples_2018") : era = "2018"

    version = era + "_V" + version
    
    content = f.readlines()
    content = [x.strip() for x in content]
    content = list(filter(lambda x: len(x) > 0, content))
    from CRABAPI.RawCommand import crabCommand
    n=200
    oldRequestName = ""
    for dataset in content :
        
        
        if not (dataset[0].startswith("/"))  : continue
        ext = ""
        prod = str(dataset.split('/')[-1])
        if prod.startswith("NANO")  : config.Data.inputDBS = 'global'
        if prod == "USER" :           config.Data.inputDBS = 'phys03'
        config.Data.inputDataset = dataset
        config.Data.unitsPerJob = 1


        requestName = dataset.split('/')[1]+"_"+version
        if oldRequestName.startswith(requestName) :
            ext = extentionPostname.pop()
            requestName = requestName + ext
            #print requestName
        else :
            extentionPostname = ["_ext10", "_ext9", "_ext8", "_ext7", "_ext6", "_ext5", "_ext4", "_ext3", "_ext2", "_ext1"]
        oldRequestName = requestName
        
        if requestName.startswith("SingleMuon") : 
            if era == "2016" : config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt'
            if era == "2017" : config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt'
            if era == "2018" : config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt'
        

        #if requestName.startswith("SingleMuon") : data = "data"
        #else : data = "MC"
        #config.JobType.scriptArgs = [data, era]
        
        config.General.requestName = requestName
        config.Data.outputDatasetTag = dataset.split('/')[2][:30]+"_"+version + ext
        crabCommand('submit', config = config)
        
        
        


        
