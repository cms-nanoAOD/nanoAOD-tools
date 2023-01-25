from CRABClient.UserUtilities import config as Configuration

from datetime import date 
import argparse
import os 

base = os.environ["CMSSW_BASE"]
user = os.environ["USER"]

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("--analysis", default=None, required=True, choices=["ggtautau","ggbb"], help="Choose the analysis for which the skimming is to be run (Required)")
parser.add_argument("--version", default=None, help="Name for the output folder. Default: 'skim_DATE_ANALYSIS', otherwise 'skim_DATE_ANALYSIS_VERSION'")
parser.add_argument("--crabDir", default=base+"/..", help="Output folder for crab project files. Default: '"+base+"/..'")
args = parser.parse_args()

version="skim_"+date.today().strftime("%b%d%Y")+"_"+args.analysis+("_"+str(args.version) if args.version else "")
print version


### General crab configuration ###
config = Configuration()

config.section_("General")
config.General.transferLogs = True
config.General.workArea = args.crabDir

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_ggOnly.sh'
config.JobType.inputFiles = ['crab_script_ggOnly.py', '../scripts/haddnano.py', 'keep_and_drop.txt']
config.JobType.sendPythonFolder = True
config.JobType.allowUndistributedCMSSW = True #shouldn't be necessary

config.section_("Data")
#config.Data.inputDBS = 'phys03' # shouldn't be necessary to define, since we are using local files. Defaults to 'global'.
config.Data.splitting = 'FileBased'
config.Data.allowNonValidInputDataset=True

config.Data.outLFNDirBase = '/store/user/'+user+'/'+version
config.Data.publication = False

config.section_("Site")
config.Site.storageSite = "T2_US_UCSD"
### General crab configuration ###


from sa import *
from allsamples import *
from CRABAPI.RawCommand import crabCommand

counter=1

for sample in XToYHToggbbSamples:

  path='/ceph/cms/store/user/evourlio/XtoYH_customNanoAOD/'+sample # Probably better to have a common /ceph area
  
  # MC
  if "Summer20UL1" in sample:
    config.Data.unitsPerJob = 10
    if "Summer20UL16" in sample and "APV" in sample:
      config.JobType.scriptArgs = ["arg=16a","arg="+args.analysis]
    elif "Summer20UL16" in sample:
      config.JobType.scriptArgs = ["arg=16b","arg="+args.analysis]
    elif "Summer20UL17" in sample:
      config.JobType.scriptArgs = ["arg=17","arg="+args.analysis]
    elif "Summer20UL18" in sample:
      config.JobType.scriptArgs = ["arg=18","arg="+args.analysis]
    else:
      print("Couldn't identify sample year/era: %s", sample)

  # Data
  elif "Run201" in sample:
    config.Data.unitsPerJob = 10
    if "Run2016" in sample and "HIPM" in sample:
      config.JobType.scriptArgs = ["arg=16aD","arg="+args.analysis]
      #config.Data.lumiMask = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt'
    elif "Run2016" in sample:
      config.JobType.scriptArgs = ["arg=16bD","arg="+args.analysis]
      #config.Data.lumiMask = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt'
    elif "Run2017" in sample:
      config.JobType.scriptArgs = ["arg=17D","arg="+args.analysis]
      #config.Data.lumiMask = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt'
    elif "Run2018" in sample:
      config.JobType.scriptArgs = ["arg=18D","arg="+args.analysis]
      #config.Data.lumiMask = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt'
    else:
      print("Couldn't identify sample year/era: %s", sample)

  else:
    print("Couldn't identify sample year/era: %s", sample)

  
  # Get files - it works at UCSD
  files=os.listdir(path)
  for i in range(len(files)):
    files[i]=path.replace("/ceph/cms", "")+"/"+files[i]
  
  config.Data.userInputFiles = files
  config.Data.totalUnits = len(files)


  opd = sample.split("/")[-1]
  lengthToFitName = 100-len(args.version+"-"+"-"+str(counter))
  shortName = args.version+"-"+opd[0:lengthToFitName]+"-"+str(counter)
  config.General.requestName = shortName
  config.Data.outputPrimaryDataset=opd[0:99]
  config.Data.outputDatasetTag = shortName
  print opd, len(files)
  crabCommand('submit', config = config, dryrun = False) ## dryrun = True for local test
  print "DONE\n"
  
  counter+=1
