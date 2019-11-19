from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
from optparse import OptionParser
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *

def getOptions():
    """                                                                                                                                                                                      
    Parse and return the arguments provided by the user.
    """
    usage = ('usage: python submit_all.py -d DIR -C CHANNEL')
    parser = OptionParser(usage=usage)
    parser.add_option("-s", "--sample", dest="sample", help=("The sample name you want submit "), metavar="SAMPLE")
    parser.add_option("-d", "--dir", dest="dir", help=("The crab directory you want to use "), metavar="DIR")
    (options, args) = parser.parse_args()
    if options.sample == None or options.dir == None:
        parser.error(usage)
    return options

option = getOptions()

config = Configuration()
config.section_("General")
config.General.requestName = option.sample.label
config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script.py']#,'../scripts/haddnano.py'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder	 = True
config.section_("Data")
config.Data.inputDataset = option.sample.dataset
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 2
config.Data.totalUnits = 10
config.Data.outLFNDirBase = '/store/user/%s/%s' % (getUsernameFromSiteDB(), option.dir)
config.Data.publication = False
config.Data.outputDatasetTag = option.sample.label
config.section_("Site")
config.Site.storageSite = "T2_IT_Pisa"

#config.Site.storageSite = "T2_CH_CERN"
#config.section_("User")
#config.User.voGroup = 'dcms'

