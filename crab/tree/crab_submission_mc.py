import fileinput, string, sys, os, time, datetime

from dataset_2016 import *
from dataset_2017 import *
if len(sys.argv) != 2:
        print "USAGE: %s <Data year>"%(sys.argv [0])
        sys.exit (1)
year   = sys.argv [1]
date   = datetime.datetime.now()

if(year == '2016'):
    outputDir = "/store/user/mikumar/RUN2/Tree_crab/SIXTEEN/MC/dR_len_with_jet/"
    Datasets = Datasets_MC_2016
    RequestName = RequestName_MC_2016
if(year == '2017'):
    outputDir = "/store/user/mikumar/RUN2/Tree_crab/SEVENTEEN/MC/dR_len_with_jet/"
    Datasets = Datasets_Alt_MC_2017
    RequestName = RequestName_Alt_MC_2017

print "len(Datasets) = ",len(Datasets),"len(RequestName)\t",len(RequestName)
cfgfile = "crab_cfg.py"
scriptfile = "crab_script.py"

def replacemachine(fileName, sourceText, replaceText):
    ##################################################################
    for line in fileinput.input(fileName, inplace=True):
        if line.strip().startswith(sourceText):
        	line = replaceText
    	sys.stdout.write(line)
    print "All went well, the modifications are done"
    ##################################################################

for i in range(0,1):#len(Datasets)):
    update_RequestName = "config.General.requestName = '"+RequestName[i]+"_Tree_"+year+"'\n" 
    update_Dataset = "config.Data.inputDataset = '"+Datasets[i]+"'\n"
    update_DirBase = "config.Data.outLFNDirBase = '"+outputDir+RequestName[i]+"'\n"
    update_DatasetTag = "config.Data.outputDatasetTag = 'Tree_October_SEVENTEEN_"+RequestName[i]+"'\n"
    update_DatasetTag = "config.Data.outputDatasetTag = 'Tree_"+date.strftime("%d")+"_"+date.strftime("%b")+date.strftime("%y")+"_MC"+year+"_"+RequestName[i]+"'\n"
    update_InputFiles = "config.JobType.inputFiles = ['ElectronSF','MuonSF','clean.txt','crab_efficiency.py','crab_script.py','scaleFactor.py','../scripts/haddnano.py','keep_and_drop.txt','MainModule.py','EfficiencyModule.py']\n"    
    if(year == '2016'):update_module = "\t\tmodules=[MainModuleConstr_mc_2016(),btagSF2016(),puWeight_2016(),jmeCorrections2016_MC_AK4CHS()],\n"
    if(year == '2017'):update_module = "\t\tmodules=[MainModuleConstr_mc_2017(),btagSF2017(),puWeight_2017(),jmeCorrections2017_MC_AK4CHS()],\n"
    print "RequestName = ",update_RequestName ,"\tDatasets = ",update_Dataset,"\tDirBase = ",update_DirBase,"\tDatasetTag = ",update_DatasetTag 
    print "InputFiles = ",update_InputFiles

    replacemachine(cfgfile,'config.General.requestName =', update_RequestName)
    replacemachine(cfgfile,'config.Data.inputDataset =', update_Dataset )
    replacemachine(cfgfile,'config.Data.outLFNDirBase =', update_DirBase )
    replacemachine(cfgfile,'config.Data.outputDatasetTag =', update_DatasetTag )
    replacemachine(cfgfile,'config.JobType.inputFiles =', update_InputFiles )
    replacemachine(scriptfile,'modules=', update_module ) 

    cmd_crab_submit = "crab submit -c crab_cfg.py"
    #os.system(cmd_crab_submit)  
 
    #cmd_crab_kill = "crab kill -d crab_"+RequestName[i]
    #os.system(cmd_crab_kill)

    #cmd_rm_dir = "rm -rf crab_"+RequestName[i]
    #os.system(cmd_rm_dir)


    print "DONE -----",RequestName[i],"--------------------------------------------------------------------------------------------"
    time.sleep(10) 
