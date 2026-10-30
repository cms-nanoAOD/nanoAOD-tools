import fileinput, string, sys, os, time, datetime

from dataset_2016_phy3 import *
from dataset_2017_phy3 import *

if len(sys.argv) != 3:
        print "USAGE: %s <Data year> %s <lep_flaovur>"%(sys.argv [0])
        sys.exit (1)
year   = sys.argv [1]
lep    = sys.argv [2]
date   = datetime.datetime.now()

if(year == '2016'):
    outputDir = "/store/user/mikumar/RUN2/MiniTree_crab/SIXTEEN/MC/dR_len_with_Jet/"
    Datasets = Datasets_MC_2016
    RequestName = RequestName_MC_2016
    NumberOfEvents = NumberOfEvents_MC_2016 
    Xsection = Xsection_MC_2016
if(year == '2017'):
    outputDir = "/store/user/mikumar/RUN2/MiniTree_crab/SEVENTEEN/MC/dR_len_with_Jet/"
    Datasets = Datasets_MC_2017
    RequestName = RequestName_MC_2017
    NumberOfEvents = NumberOfEvents_MC_2017
    Xsection = Xsection_MC_2017

print "len(Datasets) = ",len(Datasets),"\tlen(RequestName) = ",len(RequestName), "\tNumberOfEvents = ",len(NumberOfEvents),"\t Xsection = ", len(Xsection)
cfgfile = "crab_cfg_Minitree.py"
crab_scriptfile = "crab_script_Minitree.py"
#bweight_cal = "Mc_prob_cal_forBweght.py"
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
    #if(i>=19 and i<=30 and year == '2017'):continue
    #if(i>=19 and i<=29 and year == '2016'):continue
    if(lep=="el" and RequestName[i].find("MuEnriched")!=-1 and RequestName[i].find("QCD")!=-1): continue
    if(lep=="mu" and RequestName[i].find("EMEnriched")!=-1 and RequestName[i].find("QCD")!=-1): continue
    region_tag = "2J1L0T0"
    #if "mtop" in RequestName[i] and region_tag == "2J0T1":region_tag = "2J1T1"
    #if "mtop" in RequestName[i] and region_tag == "2J0T0":region_tag = "2J1T0"
    update_RequestName = "config.General.requestName = '"+RequestName[i]+"_Minitree_"+region_tag+"_"+lep+"_"+year+"'\n" 
    update_Dataset = "config.Data.inputDataset = '"+Datasets[i]+"'\n"
    #update_DirBase = "config.Data.outLFNDirBase = '"+outputDir+region_tag+"_"+lep+"/"+RequestName[i]+"'\n"
    update_DirBase = "config.Data.outLFNDirBase = '"+outputDir+region_tag+"_"+lep+"/"+RequestName[i]+"'\n"
    update_DatasetTag = "config.Data.outputDatasetTag = 'MiniTree_"+date.strftime("%d")+"_"+date.strftime("%b")+date.strftime("%y")+"_MC"+year+"_"+RequestName[i]+"_"+region_tag+"'\n"
    update_InputFiles = "config.JobType.inputFiles = ['crab_script_Minitree.py','../../scripts/haddnano.py','Mc_prob_cal_forBweght.py','foxwol_n_fourmomentumSolver.py','MinitreeModule.py','cut_strings.py','keep_and_drop_mu_Minitree.txt','keep_and_drop_el_Minitree.txt']\n"
    cut_string = "treecut = cut_"+region_tag+"_"+lep+"_"+year+"\n"
    modules = "\t\tmodules=[MinitreeModuleConstr"+region_tag+"_"+lep+"_mc_"+year+"()],\n"
    branchsel = '\t\toutputbranchsel="keep_and_drop_'+lep+'_Minitree.txt",\n' 
     
    update_NumberOfEvents = "\t\tNEvents = "+NumberOfEvents[i]+"\n"
    update_Xsection = "\t\tx_sec = "+Xsection[i]+"\n"

    print "\t"+cut_string 
    print modules
    print branchsel 
    print "\tRequestName: ",update_RequestName  
    print "\tDatasets = ",update_Dataset  
    print "\tDirBase = ",update_DirBase  
    print "\tDatasetTag = ",update_DatasetTag  
    print "\tNumber of Events = ",NumberOfEvents[i]  
    print "\tXsection = ",Xsection[i]	   
    print "InputFiles: ",update_InputFiles  
    #print "update_effi_file: ", update_effi_file

    replacemachine(cfgfile,'config.General.requestName =', update_RequestName)
    replacemachine(cfgfile,'config.Data.inputDataset =', update_Dataset )
    replacemachine(cfgfile,'config.Data.outLFNDirBase =', update_DirBase )
    replacemachine(cfgfile,'config.Data.outputDatasetTag =', update_DatasetTag )
    replacemachine(cfgfile,'config.JobType.inputFiles =', update_InputFiles )
    replacemachine(crab_scriptfile,'treecut =', cut_string )
    replacemachine(crab_scriptfile,'modules=', modules )
    replacemachine(crab_scriptfile,'outputbranchsel=', branchsel )
    #replacemachine(bweight_cal,'Effi_FIle = ROOT.TFile(', update_effi_file )
    replacemachine(MinitreeModule,'NEvents = ', update_NumberOfEvents )
    replacemachine(MinitreeModule,'x_sec = ',update_Xsection)


    #cmd_crab_kill = "crab purge crab_2016/crab_MiniTree_2016/2J1T1/crab_"+RequestName[i]+"_Minitree2J1T1_mu"
    #os.system(cmd_crab_kill)

    #cmd_rm_dir = "rm -rf crab_"+RequestName[i]+"_Minitree2J1T0_el"
    #os.system(cmd_rm_dir)

    cmd_crab_submit = "crab submit -c crab_cfg_Minitree.py"
    os.system(cmd_crab_submit)  
 


    #cmd_rm_dir = "rm -rf crab_"+RequestName[i]+"_2J1T1MiniTr_mu_mc"
    #os.system(cmd_rm_dir)


    print "DONE -----",i,"---",region_tag,"---",RequestName[i],"---",NumberOfEvents[i],"-----",Xsection[i], "-------------------------------------------------------------------"
    time.sleep(10)
    
