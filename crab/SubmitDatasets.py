import getpass
import os
import sys

# Default option for the verbose
verbose   = False

def GetName_cfg(datasetName, isData = False):
  ''' Returns the name of the cfg file for a given dataset '''
  if datasetName[0] != '/': datasetName = '/' + datasetName
  tag = datasetName[1 : datasetName[1:].find('/')+1]
  genTag = datasetName[ datasetName[1:].find('/')+1 :]
  genTag = genTag[:genTag[1:].find('/')+1]
  a = genTag.find('_ext')
  if a > 0: tag += genTag[a+1:a+5]
  if(isData): tag += genTag.replace('/','_')
  filename = 'crab_cfg_' + tag + '.py'
  return filename


def CheckPathDataset(path):
  ''' Check if the name exists in local folder or in dataset folder '''
  if(os.path.isfile(path)): return path
  if(os.path.isfile(path+'.txt')): return path+'.txt'
  path = 'datasets/' + path
  if(os.path.isfile(path)): return path
  if(os.path.isfile(path+'.txt')): return path+'.txt'
  return ''
 
def GuessIsData(path):
  ''' Returns False if the dataset file seems to correspond to mc, True otherwise '''
  name = path.replace('datasets', '')
  if name.find('mc') >= 0 or name.find('MC') >= 0: return False
  elif name.find('data') >= 0 or name.find('Data') >= 0 or name.find('DATA') >= 0: return True
  else: 
    if 'NANOAOD' in path:
      if 'NANOAODSIM' in path: return False
      else: return True

def GuessYear(path):
  if   'Run2018' in path: return 18
  elif 'Run2017' in path: return 17
  elif 'Run2016' in path: return 16
  elif '2018'    in path: return 18
  elif '2017'    in path: return 17
  elif '2016'    in path: return 16

def CrateCrab_cfg(datasetName, isData = False, isTest = False, productionTag = 'prodTest', year = 0):
  ''' Creates a cfg file to send crab jobs to analyze a given dataset '''
  # CONSTANTS
  tier = "T2_ES_IFCA"
  unitsperjob = 1

  # Set according to datasetName
  filename = GetName_cfg(datasetName, isData)
  localdir = filename[9:-3]

  # Set according to username
  username = getpass.getuser()
  basedir = '/store/user/' + username + '/nanoAODcrab'

  # Detect if it's MC or DATA and set parameters
  strSplitting = "FileBased"; # MC
  lumiMask = ''
  crabScript = 'crab_script.py'
  if(isData): 
    strSplitting = "LumiBased";
    crabScript = 'crab_script_data.py'
    if   year == 17: lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt'  # 41.29/fb
    elif year == 18: lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/PromptReco/Cert_314472-316271_13TeV_PromptReco_Collisions18_JSON.txt' # 7.93/fb
    #https://twiki.cern.ch/twiki/bin/view/CMS/PdmV2018Analysis#DATA

  # Set according to input parameters
  totalUnits = 1000000 # test
  if isTest: totalUnits = 3
  prodTag = productionTag

  t_localdir     = "config.General.requestName = '"  + localdir + "'\n"
  t_inputfiles   = "config.JobType.inputFiles = ['" + crabScript + "','../scripts/haddnano.py', '../python/postprocessing/SlimFile.txt']\n"
  t_inputdataset = "config.Data.inputDataset = '" + datasetName + "'\n" 
  t_totalunits   = "config.Data.totalUnits = " + str(totalUnits) + "\n"
  t_unitsperjob  = "config.Data.unitsPerJob = " + str(unitsperjob) + "\n"
  t_splitting    = "config.Data.splitting = '" + strSplitting + "'\n"
  t_basedir      = "config.Data.outLFNDirBase = '" + basedir + "'\n"
  t_datasetTag = "config.Data.outputDatasetTag = '" + prodTag + "'\n" 
  t_tier = "config.Site.storageSite = '" + tier + "'\n"
  t_lumiMask = "config.Data.lumiMask = '" + lumiMask + "'\n"
 
  text = "from WMCore.Configuration import Configuration\n"
  text += "config = Configuration()\nconfig.section_('General')\n"
  text += t_localdir
  text += "config.General.transferLogs=True\nconfig.section_('JobType')\nconfig.JobType.pluginName = 'Analysis'\n"
  text += "config.JobType.psetName = 'PSet.py'\nconfig.JobType.scriptExe = 'crab_script.sh'\nconfig.JobType.sendPythonFolder	 = True\n"
  text += t_inputfiles
  text += "config.section_('Data')\n"
  text += t_inputdataset
  text += "config.Data.inputDBS = 'global'\n"
  text += t_splitting
  if isData: text += t_lumiMask
  text += t_unitsperjob
  text += t_totalunits
  text += t_basedir
  text += "config.Data.publication = False\n"
  text += t_datasetTag
  text += "config.section_('Site')\n"
  text += t_tier

  f = open(filename, 'w')
  f.write(text)
  f.close()
  os.system('chmod a+x ' + filename)
  if verbose: print '   >> Created cfg file: ', filename



def SubmitDatasets(path, isTest = False, prodName = 'prodTest', doPretend = False):
  path = CheckPathDataset(path)
  if(path == ''):
    print 'ERROR: dataset not found'
    return
  isData = GuessIsData(path)
  year   = GuessYear(path)
  if verbose: 
    if isData: print 'Opening path: ', path, '(DATA)'
    else: print  'Opening path: ', path, '(MC)'
  f = open(path, 'r')
  for line in f:
    line = line.replace(' ', '')
    line = line.replace('\t', '')
    line = line.replace('\n', '')
    line = line.replace('\r', '')
    if line == '': continue
    if line[0] == '#': continue
    if line.find('#') > 0: line = line[:line.find('#')]
    if len(line) <= 1: continue
    cfgName = GetName_cfg(line, isData)
    if verbose: print 'Creating cfg file for dataset: ', line
    CrateCrab_cfg(line, isData, isTest, prodName, year)
    if not doPretend:
      os.system('crab submit -c ' + cfgName)
      if not os.path.isdir(prodName): os.mkdir(prodName)
      os.rename(cfgName, prodname + '/' + cfgName)
      #os.remove(cfgName)

#SubmitDatasets('data2017')

arguments = sys.argv[1:]
narg = len(arguments)

# Variables to set
dotest    = False
doPretend = False
doDataset = False
prodName  = ''
datasetName = ''

if narg == 0:
  print ' > Usage:'
  print ' >>> python SubmitDatasets.py NameOfDatasetFile --option1 arg1 --option2'
  print ' '
  print ' > Options:'
  print ' > --test'
  print ' >   Sends a job per sample'
  print ' > --prodName name'
  print ' >   Set a name for the production. Example: may23'
  print ' > --verbose (or -v)'
  print ' > --dataset /dataset/name/'
  print ' >   Runs on a given dataset'
  print ' > --pretend'
  print ' >   Only creates the cfg file; does not send jobs'
  print ' '
  print ' > Examples:'
  print ' >   python SubmitDatasets.py data2018 -v --prodName may28'
  print ' >   python SubmitDatasets.py --dataset /TT_TuneCUETP8M2T4_mtop1665_13TeV-powheg-pythia8/RunIISummer16NanoAOD-PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/NANOAODSIM -v --test'
  print ' >   python SubmitDatasets.py --dataset /TT_TuneCUETP8M2T4_mtop1665_13TeV-powheg-pythia8/RunIISummer16NanoAOD-PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/NANOAODSIM -v --pretend'

else:
  # SET ARGUMENTS AND OPTIONS
  i = 0
  if not arguments[0].startswith('--'): datasetName = arguments[0]
  for arg in arguments:
    i+=1
    if arg.startswith('--'):
      a = arg[2:]
      if   a == 'test'       : dotest      = True
      elif a == 'verbose'    : verbose     = True
      elif a == 'pretend'    : doPretend   = True
      elif a == 'dataset': 
        datasetName = arguments[i]
        doDataset   = True
      elif a == 'prodName'   : prodName    = arguments[i]
    elif arg.startswith('-'):
      a = arg[1:]
      if a == 'v': verbose = True

  if doDataset:
    if verbose: print 'Creating cfg file for dataset: ', datasetName
    doData = GuessIsData(datasetName)
    year   = GuessYear(datasetName)
    cfgName = GetName_cfg(datasetName, forceData)
    CrateCrab_cfg(datasetName, doData, dotest, prodName, year)
    if not doPretend:
      os.system('crab submit -c ' + cfgName)
      if not os.path.isdir(prodName): os.mkdir(prodName)
      os.rename(cfgName, prodname + '/' + cfgName)
      #os.remove(cfgName)

  else:
    SubmitDatasets(datasetName, dotest, prodName, doPretend)
