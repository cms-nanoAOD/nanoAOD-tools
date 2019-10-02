import sys
from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB


config = Configuration()

version = "Z185"



era = "2016"
data = "MC"
era = sys.argv[1]
f=open("samples_"+era+".txt") 


config.section_("General")
config.General.transferLogs=True
config.General.workArea = '/afs/cern.ch/work/g/gimandor/public/testNANOAOD'#+version
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'

config.JobType.scriptExe = 'crab_script'+era+'.sh'
config.JobType.inputFiles = ['crab_script'+era+'.py','../scripts/haddnano.py']

if version.endswith("A") or version.endswith("B") or version.endswith("C") or version.endswith("D") :
    config.JobType.scriptExe = 'crab_script'+era+version[-1]+'.sh'
    config.JobType.inputFiles = ['crab_script'+era+version[-1]+'.py','../scripts/haddnano.py']


print "inputFiles ", config.JobType.inputFiles
config.JobType.sendPythonFolder	 = True
config.section_("Data")
#config.Data.inputDataset = '/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PUMoriond17_94X_mcRun2_asymptotic_v2-v1/NANOAODSIM'
config.Data.inputDBS = 'global'
#config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.allowNonValidInputDataset=True
#config.Data.splitting = 'Automatic'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 1

config.Data.outLFNDirBase = '/store/user/gimandor/'
config.Data.publication = True
config.Data.outputDatasetTag = 'NanoTestPost5'
config.section_("Site")
#config.Site.storageSite = "T2_IT_Bari"
config.Site.storageSite = "T2_IT_Legnaro"
#config.Site.storageSite = "T2_IT_Pisa"



sites=['T2_IT_Pisa']
ext = ["", "_ext1", "_ext2", "_ext3", "_ext4", "_ext5", "_ext6", "_ext7", "_ext8", "_ext9", "_ext10"]


import dictionary2016
import dictionary2017
import dictionary2018

dictionary = dictionary2016.dictionary16
if era == "2017" : dictionary = dictionary2017.dictionary17
if era == "2018" : dictionary = dictionary2018.dictionary18

from CRABAPI.RawCommand import crabCommand

if __name__ == '__main__':


    for sName in dictionary.keys() : 
        for n in range(len(dictionary[sName])) :
            
            config.Data.inputDataset = dictionary[sName][n]
            
            if sName.startswith("SingleMuon") : 
                if era == "2016" : config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt'
                if era == "2017" : config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt'
                if era == "2018" : config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt'
        

            config.General.requestName = sName+ ext[n] + "_" + era + "_V" + version 
            config.Data.outputDatasetTag = dictionary[sName][n].split('/')[2].split("-")[0]+"_"+version + ext[n]
            crabCommand('submit', config = config)




        
