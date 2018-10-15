import os, time, sys

# Constants
path = '.'
verbose = 1
Datasets = ['MuonEG', 'DoubleMuon', 'DoubleEG','SingleMuon','SingleElectron'] # ['MuonEG', 'DoubleMuon', 'DoubleEG', 'SingleMuon', 'SingleElectron']
Eras     = ['B', 'C', 'D', 'E', 'F']
Year     = 2017
jsonName = 'lumisToProcess'
doCheckTime = True # To check the day and month of the creation
Day = 19
Month = 'Jul'



def GetDatasetInfo(d):
  c = (d.split('-'))[0].split('_')
  dataset = c[1]
  year    = (c[2][3:-1])
  era     = c[2][-1]
  if year.isdigit(): year = int(year)
  return dataset, year, era

def GetDatasets():
  dirs = []
  for d in os.listdir(path):
    if os.path.isdir(d): 
      if not d.startswith('crab_'): continue
      if doCheckTime:
        t = (time.ctime(os.path.getmtime(d))).split(' ')
        day = t[2]; month = t[1]
        if not day == str(Day): continue
        if not month == Month: continue
      dataset, year, era = GetDatasetInfo(d)
      if not dataset in Datasets: continue
      if not Year == year: continue
      if verbose >= 2: print ' >> Found dir for dataset ' + dataset + ', [year, era] = [' + str(year) + ', ' + era + ']: ', d
      dirs.append(d)
  return dirs

def CreateReports():
  ''' Execute crab report for all selected datasets... skips when dir/results exists '''
  f = GetDatasets()
  print ' >> Creating lumi json reports for %i datasets...'%len(f)
  for d in f:
    if os.path.isdir(d + '/results'): continue
    os.system('crab report ' + d)

def GetLumiPath(pathToDataset, jsonName = 'lumisToProcess'):
  if pathToDataset[-1] != '/': pathToDataset += '/'
  if not jsonName[-5:] == '.json': jsonName += '.json'
  command = 'brilcalc lumi -b "STABLE BEAMS" -u /fb -i '
  out = os.popen(command + pathToDataset + 'results/' + jsonName).read()
  outlines = out.split('\n'); i = -1; l = ''
  for line in outlines:
    i += 1
    if not 'totrecorded' in line: continue
    else: l = outlines[i+2]
  if l == '': 
    print 'ERROR: lumi not found...'
    return
  return float(l.split('|')[-2])

def GetLumi():
  paths = GetDatasets()
  for d in Datasets:
    totalLumi = 0
    for era in Eras:
      for p in paths:
       idataset, iyear, iera = GetDatasetInfo(p)
       if iera == era and idataset == d:
         lumi = GetLumiPath(p) 
         totalLumi += lumi
         print d + ' >> Run%i '%iyear + iera + ': ' + str(lumi)
    print d + ' >> Total lumi: ', totalLumi
    
GetLumi()
