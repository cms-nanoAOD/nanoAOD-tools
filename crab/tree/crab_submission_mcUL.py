import fileinput, string, sys, os, time, datetime
import argparse as arg
from tqdm import tqdm

parser = arg.ArgumentParser(description='inputs discription')
parser.add_argument('-y', '--year', dest='inputs', type=str, nargs=1, help="Year [UL2016preVFP, UL2016postVFP, UL2017, UL2018]")
args = parser.parse_args()


if args.inputs == None:
        print("USAGE: %s [-h] [-y <Data year>]"%(sys.argv [0]))
        sys.exit (1)

if args.inputs[0] not in ['UL2016preVFP', 'UL2016postVFP','UL2017','UL2018']:
    print('Error: Incorrect choice of year, use -h for help')
    exit()

print("year = ",args.inputs[0])
year   = args.inputs[0]
date   = datetime.datetime.now()

if(year == 'UL2016preVFP'):
    from dataset_UL2016preVFP import *
    outputDir = "/store/user/mikumar/RUN2_UL/Tree_crab/SIXTEEN/MC_preVFP/"
    Datasets = Datasets_sys_MC_UL2016APV
if(year == 'UL2016postVFP'):
    from dataset_UL2016postVFP import *
    outputDir = "/store/user/mikumar/RUN2_UL/Tree_crab/SIXTEEN/MC_postVFP/"
    Datasets = Datasets_sys_MC_UL2016

if(year == 'UL2017'):
    from dataset_UL2017 import *
    outputDir = "/store/user/mikumar/RUN2_UL/Tree_crab/SEVENTEEN/MC/"
    Datasets = Datasets_sys_MC_UL2017

if(year == 'UL2018'):
    from dataset_UL2018 import *
    outputDir = "/store/user/mikumar/RUN2_UL/Tree_crab/EIGHTEEN/MC/"
    #Datasets = Datasets_MC_UL2018
    Datasets = Datasets_sys_MC_UL2018

RequestNames = Datasets.keys()
print(RequestNames)
print("len(Datasets) = ",len(Datasets))

cfgfile = "crab_cfg_skimTree.py"
scriptfile = "crab_script_skimTree.py"

def replacemachine(fileName, sourceText, replaceText):
    ##################################################################
    for line in fileinput.input(fileName, inplace=True):
        if line.strip().startswith(sourceText):
        	line = replaceText
        sys.stdout.write(line)
    print("All went well, the modifications are done")
    ##################################################################

#print RequestName
for RequestName in tqdm(RequestNames):
#for RequestName in ["ttbar_SemiLeptonic_erdON"]: #","WJetsToLNu_0J_v2","WJetsToLNu_2J"]:
    Dataset = Datasets[RequestName]
    print(RequestName, " : ",Dataset)
    update_RequestName = "config.General.requestName = '"+RequestName+"_Tree_"+year+"'\n" 
    update_Dataset = "config.Data.inputDataset = '"+Dataset+"'\n"
    update_DirBase = "config.Data.outLFNDirBase = '"+outputDir+RequestName+"'\n"
    update_DatasetTag = "config.Data.outputDatasetTag = 'Tree_"+date.strftime("%d")+"_"+date.strftime("%b")+date.strftime("%y")+"_MC"+year+"_"+RequestName+"'\n"
    update_InputFiles = "config.JobType.inputFiles = ['crab_script_skimTree.py','../../scripts/haddnano.py','keep_and_drop.txt','MainModule.py']\n"    
    update_site = "config.Site.storageSite = 'T3_CH_CERNBOX'\n" #'T2_IN_TIFR'\n"
    update_module = "\t\tmodules=[MainModuleConstr_mc_"+year+"(),puWeight_"+year+"()],\n"
    update_data_splitting = "config.Data.splitting = 'FileBased'\n" 
    update_data_unitsPerJon = "config.Data.unitsPerJob = 1\n"
    update_Golgonjsonfile = '"""config.Data.lumiMask ="""\n'
    update_publication = "config.Data.publication = False\n"

    print("RequestName = ",update_RequestName ,"\tDatasets = ",update_Dataset,"\tDirBase = ",update_DirBase,"\tDatasetTag = ",update_DatasetTag) 
    print("InputFiles = ",update_InputFiles)
    print(update_site)
    print(update_module)

    replacemachine(cfgfile,'config.General.requestName =', update_RequestName)
    replacemachine(cfgfile,'config.Data.inputDataset =', update_Dataset )
    replacemachine(cfgfile,'config.Data.outLFNDirBase =', update_DirBase )
    replacemachine(cfgfile,'config.Data.outputDatasetTag =', update_DatasetTag )
    replacemachine(cfgfile,'config.JobType.inputFiles =', update_InputFiles )
    replacemachine(cfgfile,'config.Site.storageSite =', update_site )
    replacemachine(cfgfile,'config.Data.splitting =', update_data_splitting )
    replacemachine(cfgfile,'config.Data.unitsPerJob =', update_data_unitsPerJon )
    replacemachine(cfgfile,'config.Data.publication =', update_publication )
    replacemachine(cfgfile,'config.Data.lumiMask =', update_Golgonjsonfile )
    replacemachine(scriptfile,'modules=', update_module ) 

    cmd_crab_submit = "crab submit -c "+cfgfile
    #os.system(cmd_crab_submit)
 
    #cmd_crab_kill = "crab kill -d crab_"+RequestName
    #os.system(cmd_crab_kill)

    #cmd_rm_dir = "rm -rf crab_"+RequestName
    #os.system(cmd_rm_dir)


    print("DONE -----",RequestName,"--------------------------------------------------------------------------------------------")
    time.sleep(10)
