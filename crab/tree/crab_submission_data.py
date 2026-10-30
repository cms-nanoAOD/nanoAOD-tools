import fileinput, string, sys, os, time, datetime

from dataset_2016 import *
from dataset_2017 import *

if len(sys.argv) != 3:
        print "USAGE: %s <Data year> <lep_flaovur> "%(sys.argv [0])
        sys.exit (1)
year   = sys.argv [1]
lep    = sys.argv [2]
date   = datetime.datetime.now()

if(year == '2016'):
    outputDir = "/store/user/mikumar/RUN2/Tree_crab/SIXTEEN/Data_el_new/"#+lep+"/"
    if(lep=="mu"):
    	Datasets = Datasets_SingleMuon_data_2016
    	RequestName = RequestName_SingleMuon_data_2016
    if(lep=="el"):
     	Datasets = Datasets_SingleElectron_data_2016
     	RequestName = RequestName_SingleElectron_data_2016     

if(year == '2017'):
    outputDir = "/store/user/mikumar/RUN2/Tree_crab/SEVENTEEN/Data_mu/"#+lep+"/"
    if(lep=="mu"):
     	Datasets = Datasets_SingleMuon_data_2017
    	RequestName = RequestName_SingleMuon_data_2017
    if(lep=="el"):
     	Datasets = Datasets_SingleElectron_data_2017
     	RequestName = RequestName_SingleElectron_data_2017

print "\tlen(Datasets) = ",len(Datasets),"len(RequestName)\t",len(RequestName)
cfgfile = "crab_cfg_skimTree.py"
scriptfile = "crab_script_skimTree.py"

def replacemachine(fileName, sourceText, replaceText):
    ##################################################################
    for line in fileinput.input(fileName, inplace=True):
        if line.strip().startswith(sourceText):
        	line = replaceText
    	sys.stdout.write(line)
    print "All went well, the modifications are done"
    ##################################################################

for i in range(0,len(Datasets)):

    update_RequestName = "config.General.requestName = '"+RequestName[i]+"_Tree'\n" 
    update_Dataset = "config.Data.inputDataset = '"+Datasets[i]+"'\n"
    update_DirBase = "config.Data.outLFNDirBase = '"+outputDir+RequestName[i]+"'\n"
    update_DatasetTag = "config.Data.outputDatasetTag = 'Tree_"+date.strftime("%d")+"_"+date.strftime("%b")+date.strftime("%y")+"_"+RequestName[i]+"'\n"
    if(year=='2016'): update_Golgonjsonfile = "config.Data.lumiMask = 'Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'\n"
    elif(year=='2017'): update_Golgonjsonfile = "config.Data.lumiMask = 'Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'\n"
 
#    update_DatasetTag = "config.Data.outputDatasetTag = 'Tree_october_Seventeen_"+RequestName[i]+"'\n"
    update_InputFiles = "config.JobType.inputFiles = ['ElectronSF','MuonSF','crab_script_skimTree.py','scaleFactor.py','btv.py','jme.py','../../scripts/haddnano.py','keep_and_drop.txt','MainModule.py','Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt','Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt']\n"    
    if(year == '2016'):
	if(RequestName[i].find("el")!=-1): update_module = "\t\tmodules=[MainModuleConstr_data_2016_singleElectron(),jmeCorrections"+RequestName[i][:8]+"_DATA_AK4CHS()],\n"#,PrefCorr16()],\n" 
	if(RequestName[i].find("mu")!=-1): update_module = "\t\tmodules=[MainModuleConstr_data_2016_singleMuon(),jmeCorrections"+RequestName[i][:8]+"_DATA_AK4CHS()],\n"#,PrefCorr16()],\n"
    if(year == '2017'):
	if(RequestName[i].find("el")!=-1):update_module = "\t\tmodules=[MainModuleConstr_data_2017_singleElectron(),jmeCorrections"+RequestName[i][:8]+"_DATA_AK4CHS(),PrefCorr()],\n"
	if(RequestName[i].find("mu")!=-1):update_module = "\t\tmodules=[MainModuleConstr_data_2017_singleMuon(),jmeCorrections"+RequestName[i][:8]+"_DATA_AK4CHS(),PrefCorr()],\n"
    print update_module
    print "\tRequestName = ",update_RequestName ,"\tDatasets = ",update_Dataset,"\tDirBase = ",update_DirBase,"\tDatasetTag = ",update_DatasetTag	   
    print "\tInputFiles = ",update_InputFiles
    
    replacemachine(cfgfile,'config.General.requestName =', update_RequestName)
    replacemachine(cfgfile,'config.Data.inputDataset =', update_Dataset )
    replacemachine(cfgfile,'config.Data.outLFNDirBase =', update_DirBase )
    replacemachine(cfgfile,'config.Data.outputDatasetTag =', update_DatasetTag )
    replacemachine(cfgfile,'config.JobType.inputFiles =', update_InputFiles )
    replacemachine(cfgfile,'config.Data.lumiMask =', update_Golgonjsonfile )
    replacemachine(scriptfile,'modules=', update_module )

    cmd_crab_submit = "crab submit -c crab_cfg_skimTree.py"
    os.system(cmd_crab_submit)  
 
    #cmd_crab_kill = "crab kill -d crab_"+RequestName[i]
    #os.system(cmd_crab_kill)

    #cmd_rm_dir = "rm -rf crab_"+RequestName[i]
    #os.system(cmd_rm_dir)


    print "DONE -----",RequestName[i],"--------------------------------------------------------------------------------------------"
    time.sleep(10) 
