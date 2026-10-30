import fileinput, string, sys, os, time, datetime

from dataset_2016_phy3 import *
from dataset_2017_phy3 import *

if len(sys.argv) != 3:
        print "USAGE: %s <Data year>  <lep_flaovur>"%(sys.argv [0])
        sys.exit (1)
year   = sys.argv [1]
lep    = sys.argv [2]
date   = datetime.datetime.now()

if(year == '2016'):
    outputDir = "/store/user/mikumar/RUN2/MiniTree_crab/SIXTEEN/Data_new/"
    if(lep=="mu"):
    	Datasets = Datasets_SingleMuon_data_2016
    	RequestName = RequestName_SingleMuon_data_2016
    if(lep=="el"):
    	Datasets = Datasets_SingleElectron_data_2016
    	RequestName = RequestName_SingleElectron_data_2016     
if(year == '2017'):
    outputDir = "/store/user/mikumar/RUN2/MiniTree_crab/SEVENTEEN/Data/"
    if(lep=="mu"):
    	Datasets = Datasets_SingleMuon_data_2017
    	RequestName = RequestName_SingleMuon_data_2017
    if(lep=="el"):
    	Datasets = Datasets_SingleElectron_data_2017
    	RequestName = RequestName_SingleElectron_data_2017

print "len(Datasets) = ",len(Datasets),"\tlen(RequestName) = ",len(RequestName)
cfgfile = "crab_cfg_Minitree.py"
module_cut = "crab_script_Minitree.py"
MinitreeModule = "MinitreeModule.py"

def replacemachine(fileName, sourceText, replaceText):
    print "editing ",fileName,
    ##################################################################
    for line in fileinput.input(fileName, inplace=True):
        if line.strip().startswith(sourceText):
        	line = replaceText
    	sys.stdout.write(line)
    print "All went well, the modifications are done"
    ##################################################################

for i in range(0,len(Datasets)):
    region_tag = "2J0T1"
    update_RequestName = "config.General.requestName = '"+RequestName[i]+"_Minitree_"+region_tag+"_"+year+"'\n" 
    update_Dataset = "config.Data.inputDataset = '"+Datasets[i]+"'\n"
    update_DirBase = "config.Data.outLFNDirBase = '"+outputDir+region_tag+"_"+lep+"_new/"+RequestName[i]+"'\n"
    update_DatasetTag = "config.Data.outputDatasetTag = 'MiniTree_"+date.strftime("%d")+"_"+date.strftime("%b")+date.strftime("%y")+"_"+RequestName[i]+"'\n"
    update_InputFiles = "config.JobType.inputFiles = ['crab_script_Minitree.py','../../scripts/haddnano.py','Mc_prob_cal_forBweght.py','foxwol_n_fourmomentumSolver.py','MinitreeModule.py','cut_strings.py','keep_and_drop_mu_Minitree.txt','keep_and_drop_el_Minitree.txt']\n"    
    cut_string = "treecut = cut_"+region_tag+"_"+lep+"_"+year+"\n"
    #cut_string = "treecut = cut_1L0TJet_"+region_tag+"_"+lep+"_"+year+"\n"
    modules = "\t\tmodules=[MinitreeModuleConstr"+region_tag+"_"+lep+"_data_"+year+"()],\n"
    branchsel = '\t\toutputbranchsel="keep_and_drop_'+lep+'_Minitree.txt",\n' 

    print "\t"+cut_string
    print modules
    print branchsel
    print "\t RequestName = ",update_RequestName
    print "\tDatasets = ",update_Dataset
    print "\tDirBase = ",update_DirBase
    print "\tDatasetTag = ",update_DatasetTag	   
    print "\t",update_InputFiles
 
    replacemachine(cfgfile,'config.General.requestName =', update_RequestName)
    replacemachine(cfgfile,'config.Data.inputDataset =', update_Dataset )
    replacemachine(cfgfile,'config.Data.outLFNDirBase =', update_DirBase )
    replacemachine(cfgfile,'config.Data.outputDatasetTag =', update_DatasetTag )
    replacemachine(cfgfile,'config.JobType.inputFiles =', update_InputFiles )
    replacemachine(module_cut,'treecut =', cut_string )
    replacemachine(module_cut,'modules=', modules )
    replacemachine(module_cut,'outputbranchsel=', branchsel )

    cmd_crab_submit = "crab submit -c crab_cfg_Minitree.py"
    os.system(cmd_crab_submit)  
 
    #cmd_crab_kill = "crab kill -d crab_"+RequestName[i]
    #os.system(cmd_crab_kill)

    #cmd_rm_dir = "rm -rf crab_"+RequestName[i]
    #os.system(cmd_rm_dir)

    print "DONE -----",i,"---",region_tag,"---",RequestName[i],"---------------------------------------------------------------------------------------"
    print 
 
    #time.sleep(10) 
