#from WMCore.Configuration import Configuration
#from CRABClient.UserUtilities import config #getUsernameFromSiteDB
from CRABClient.UserUtilities import config as Configuration

version="__TEST-SamplesV9-noPresel"

import os 
base = os.environ["CMSSW_BASE"]

config = Configuration()

config.section_("General")
config.General.requestName = 'skimNano-TestUL'
config.General.transferLogs = True
 
config.General.workArea = base+'/..'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_ggOnly.sh'
#config.JobType.scriptArgs= "foo"
# hadd nano will not be needed once nano tools are in cmssw
config.JobType.inputFiles = ['crab_script_ggOnly.py', '../scripts/haddnano.py', 'keep_and_drop.txt']
config.JobType.sendPythonFolder = True

config.JobType.allowUndistributedCMSSW = True #shouldn't be necessary

config.section_("Data")
#config.Data.inputDataset = '/DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'
config.Data.inputDBS = 'phys03'
#config.Data.inputDBS = 'global'

mc16a=["/hadoop/cms/store/user/fsetti/Summer20UL_nanoAODv9/GluGluToHHTo2G2Tau_node_cHHH1_TuneCP5_13TeV-powheg-pythia8_2016_APV_final"]
mc16b=["/hadoop/cms/store/user/fsetti/Summer20UL_nanoAODv9/GluGluToHHTo2G2Tau_node_cHHH1_TuneCP5_13TeV-powheg-pythia8_2016_final",]
mc17=["/hadoop/cms/store/user/fsetti/Summer20UL_nanoAODv9/GluGluToHHTo2G2Tau_node_cHHH1_TuneCP5_13TeV-powheg-pythia8_2017_final",]
mc18=["/hadoop/cms/store/user/fsetti/Summer20UL_nanoAODv9/GluGluToHHTo2G2Tau_node_cHHH1_TuneCP5_13TeV-powheg-pythia8_2018_final",]

from sa import *
from allsamples import allsamples

config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 1 
config.Data.totalUnits = 333 #override

config.Data.outLFNDirBase = '/store/user/${USER}/skimNano-TestUL'+version # cannot getUsernameFromSiteDB
config.Data.publication = False
#config.Data.outputDatasetTag = 'skimNano-TestUL'+version

config.section_("Site")
config.Site.storageSite = "T2_US_UCSD"

from CRABAPI.RawCommand import crabCommand

import genf

counter=1002

opds={}

for sample in allsamples:
  
    path='/ceph/cms/store/user/fsetti/Summer20UL_nanoAODv9/'+sample
    
    if sample in mc16A:
      config.JobType.scriptArgs=["arg=16a"] #it seems this is not working without the = sign!!!
      path=mc16A[sample]
      #config.Data.inputDataset=sample
    if sample in mc16:
      config.JobType.scriptArgs=["arg=16b"]
      path=mc16[sample]
      #config.Data.inputDataset=sample
    if sample in mc17:
      config.JobType.scriptArgs=["arg=17"]
      path=mc17[sample]
      #config.Data.inputDataset=sample
    if sample in mc18:
      config.JobType.scriptArgs=["arg=18"]
      path=mc18[sample]
      #config.Data.inputDataset=sample
      
    if sample in data16A:
      config.JobType.scriptArgs=["arg=16aD"] #it seems this is not working without the = sign!!!
      #config.Data.lumiMask = 'Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt'
      #config.Data.inputDataset=sample
    if sample in data16:
      config.JobType.scriptArgs=["arg=16bD"]
      #config.Data.lumiMask = 'Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt'
      #config.Data.inputDataset=sample
    if sample in data17:
      config.JobType.scriptArgs=["arg=17D"]
      #config.Data.lumiMask = 'Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt'
      #config.Data.inputDataset=sample
    if sample in data18:
      config.JobType.scriptArgs=["arg=18D"]
      #config.Data.lumiMask = 'Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt'
      #config.Data.inputDataset=sample        

    opd=sample.split("/")[-1]
    config.Data.outputPrimaryDataset=opd
    
    #get files - it works at ucsd
    files=os.listdir(path)
    for i in range(len(files)):
      #print path
      #files[i]=path.replace("/home/users/fsetti/HHggTauTau/HggNanoAnalysis/EFT_reweight","/store/user/legianni")+"/"+files[i]
      #print files[i]
      files[i]=path.replace("/ceph/cms", "")+"/"+files[i]
      #print files[i]
   
    print files
    
    config.Data.allowNonValidInputDataset=True
    config.Data.userInputFiles=files
    config.Data.totalUnits = len(files)

    config.Data.outputDatasetTag = 'skimNano-TestUL_'+sample.split("/")[-1]+"_TESTS"
    config.General.requestName = 'skimNano-TestUL'+sample.split("/")[-1][0:30]+"--"+str(counter)
    #print config.General
    print config.JobType
    opd=opd.replace("_MINIAODSIM_final","").split("-106")[0].split("-4cores5k")[0]
    print opd, len(opd)
    config.Data.outputPrimaryDataset=opd
    config.Data.outputDatasetTag = 'skimNano-TestUL_'+opd+"_TESTS"
    #config.General.requestName = 'skimNano-TestUL'+opd+"--"+str(counter)
    #print files[0:2]
#    crabCommand('submit', config = config, dryrun = False) ## dryrun = True for local test
    print "DONE"
    
    counter+=1
    
    #break
