# crab_config, mainly taken from heppy_crab_config
# https://github.com/CERN-PH-CMG/cmgtools-lite/blob/94X_dev/TTHAnalysis/cfg/crab/heppy_crab_config.py

import os
from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'

config.JobType.inputFiles = ['crab_script.py','../scripts/haddnano.py','../python/postprocessing/SlimFile.txt',
                             'options.json'] 
config.JobType.sendPythonFolder=True

config.section_("Data")
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'LumiBased' #for data

config.Data.outLFNDirBase = '/store/user/' + os.environ["USER"]
config.Data.publication = False

config.section_("Site")

