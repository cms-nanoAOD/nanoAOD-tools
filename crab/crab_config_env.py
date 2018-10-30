# crab_config_env, mainly taken from heppy_crab_config_env
# https://github.com/CERN-PH-CMG/cmgtools-lite/blob/94X_dev/TTHAnalysis/cfg/crab/heppy_crab_config_env.py
# here we set all crab options that are not fixed


import imp, os
file = open( "crab_config.py", 'r' )
cfg = imp.load_source( 'cfg', "crab_config.py", file)
config = cfg.config

print "Will send dataset", os.environ["DATASET"]

config.General.requestName = os.environ["DATASET_NAME"] + "_" + os.environ["PROD_LABEL"] # task name

config.General.workArea = 'crab_' + os.environ["DATASET_NAME"] + "_" + os.environ["PROD_LABEL"] # crab dir name

# this will divide task in *exactly* NJOBS jobs (for this we need JobType.pluginName = 'PrivateMC' and Data.splitting = 'EventBased')
config.Data.unitsPerJob = 1
config.Data.totalUnits = 10000

config.JobType.inputFiles.append(os.environ["CFG_FILE"])
# arguments to pass to scriptExe. They have to be like "arg=value". 
config.JobType.scriptArgs = ["--cfg_file="+os.environ["CFG_FILE"].split('/')[-1]]
try: config.JobType.inputFiles.extend(os.environ["FILESTOSHIP"].split(','))
except KeyError: pass
#if os.environ["ONLYUNPACKED"]!="True": config.JobType.outputFiles.append("heppyOutput.tgz")

#final output: /store/user/$USER/output_dir/cmg_version/production_label/dataset/$date_$time/0000/foo.bar
config.Data.outLFNDirBase += '/' + os.environ["STAGEOUTREMDIR"] + '/' + os.environ["PROD_LABEL"]

config.Data.inputDataset=os.environ["DATASET"]

#try: config.Data.lumiMask = os.environ["LUMIJSON"]
#except KeyError: pass

config.Site.storageSite = os.environ["OUTSITE"]

try: config.Site.whitelist = os.environ["WHITESITES"].split(',')
except KeyError: pass

try: config.JobType.scriptArgs += ["nevents="+os.environ["MAXNUMEVENTS"]]
except KeyError: pass
