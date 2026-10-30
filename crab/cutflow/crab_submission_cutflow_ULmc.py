import fileinput, string, sys, os, time, datetime
import argparse as arg

parser = arg.ArgumentParser(description='inputs discription')
parser.add_argument('-y', '--year', dest='years', type=str, nargs=1, help="Year [ UL2016preVFP , UL2016postVFP , UL2017 , UL2018 ]")
parser.add_argument('-l', '--lep', dest='leptons', type=str, nargs=1, help="lepton [ el , mu ]")
parser.add_argument('-s', '--sample', dest='samples', type=str, nargs=1, help="lepton [ mc , data ]")

args = parser.parse_args()

if (args.years == None or args.leptons == None):
        print "USAGE: %s [-h] [-y <Data year> -l <lepton>]"%(sys.argv [0])
        sys.exit (1)

if args.years[0] not in ['UL2016preVFP', 'UL2016postVFP','UL2017','UL2018']:
    print('Error: Incorrect choice of year, use -h for help')
    exit()

if args.leptons[0] not in ['el','mu']:
    print('Error: Incorrect choice of lepton, use -h for help')
    exit()

if args.samples[0] not in ['mc','data']:
    print('Error: Incorrect choice of sample, use -h for help')
    exit()


print "year = ",args.years[0]
print "lepton = ",args.leptons[0]
year   = args.years[0]
lep    = args.leptons[0]
date   = datetime.datetime.now()
sample = args.samples[0]

if(year == 'UL2016preVFP'):
    from dataset_UL2016preVFP_phy3 import *
    Datasets = Datasets_MC_UL2016APV
    if(sample=="mc"): 
    	outputDir = "/store/user/mikumar/RUN2_UL/Cutflow_crab/SIXTEEN/MC/"
    else:
	outputDir = "/store/user/mikumar/RUN2_UL/Cutflow_crab/SIXTEEN/Data/"
if(year == 'UL2016postVFP'):
    from dataset_UL2016postVFP_phy3 import *
    Datasets = Datasets_MC_UL2016
    if(sample=="mc"):
    	outputDir = "/store/user/mikumar/RUN2_UL/Cutflow_crab/SIXTEEN/MC/"
    else:
	outputDir = "/store/user/mikumar/RUN2_UL/Cutflow_crab/SIXTEEN/Data/"
if(year == 'UL2017'):
    from dataset_UL2017_phy3 import *
    Datasets = Datasets_MC_UL2017
    if(sample=="mc"):
    	outputDir = "/store/user/mikumar/RUN2_UL/Cutflow_crab/SEVENTEEN/MC/"
    else:
	outputDir = "/store/user/mikumar/RUN2_UL/Cutflow_crab/SEVENTEEN/Data/"

RequestNames = Datasets.keys()
print RequestNames
print "len(Datasets) = ",len(Datasets)
cfgfile = "crab_cfg_Minitree.py"
crab_scriptfile = "crab_script_Minitree.py"
MinitreeModule = "MinitreeModule.py"



cfgfile = "crab_cfg_cutflow.py"
cutflowModule = "cutflowModule.py"
crab_Module = "crab_script_cutflow.py"

def replacemachine(fileName, sourceText, replaceText):
    ##################################################################
    print "editing ",fileName,
    for line in fileinput.input(fileName, inplace=True):
        if line.strip().startswith(sourceText):
        	line = replaceText
    	sys.stdout.write(line)
    print "All went well, the modifications are done"
    ##################################################################

for i in range(0,len(Datasets)):
    RequestName = RequestNames[i]
    Dataset = Datasets[RequestNames[i]][0]
    if(sample=="mc"):
    	NumberOfEvents = Datasets[RequestNames[i]][1]
    	Xsection = Datasets[RequestNames[i]][2]
    
    #if(i>18 and i<=30): continuei
    region_tag = "2J1T1" 
    update_RequestName = "config.General.requestName = '"+RequestName+"_cutflow"+region_tag+"_"+lep+"_"+year+"'\n" 
    update_Dataset = "config.Data.inputDataset = '"+Dataset+"'\n"
    update_DirBase = "config.Data.outLFNDirBase = '/store/user/mikumar/RUN2/cutflow_crab/SIXTEEN/Mc/"+region_tag+"_"+lep+"/"+RequestName+"'\n"
    update_DatasetTag = "config.Data.outputDatasetTag = 'CutFlow_"+date.strftime("%d")+"_"+date.strftime("%b")+date.strftime("%y")+"_"+RequestName+"'\n"

    modules = "\t\tmodules=[cutflowModuleConstr_"+region_tag+"_"+lep+"_mc_"+year+"()],\n"
    if(sample=="mc"):
    	update_InputFiles = "config.JobType.inputFiles = ['ElectronSF','MuonSF','scaleFactor.py','crab_script_cutflow.py','../../scripts/haddnano.py','Mc_prob_cal_forBweght.py','cutflowModule.py','clean.txt']\n"   
    	update_NumberOfEvents = "\t\tNEvents = "+NumberOfEvents+"\n"
    	update_Xsection = "\t\tx_sec = "+Xsection+"\n"
    else:
	update_InputFiles = "config.JobType.inputFiles = ['scaleFactor.py','crab_script_cutflow.py','../../scripts/haddnano.py','Mc_prob_cal_forBweght.py','cutflowModule.py','clean.txt']\n"


    print "RequestName = ",update_RequestName ,"\tDataset = ",update_Dataset,"\tDirBase = ",update_DirBase,"\tDatasetTag = ",update_DatasetTag,"\tNumber of Events = ",NumberOfEvents,"\tXsection = ",Xsection	   
    print "InputFiles = ",update_InputFiles

    replacemachine(cfgfile,'config.General.requestName =', update_RequestName)
    replacemachine(cfgfile,'config.Data.inputDataset =', update_Dataset )
    replacemachine(cfgfile,'config.Data.outLFNDirBase =', update_DirBase )
    replacemachine(cfgfile,'config.Data.outputDatasetTag =', update_DatasetTag )
    replacemachine(cfgfile,'config.JobType.inputFiles =', update_InputFiles )
    replacemachine(crab_Module,'modules=', modules )
    if(sample=="mc"):
    	replacemachine(cutflowModule,'NEvents = ', update_NumberOfEvents )
    	replacemachine(cutflowModule,'x_sec = ',update_Xsection)


    #cmd_rm_dir = "rm -rf crab_"+RequestName+"_cutflow2J1T0_el_mc"
    #os.system(cmd_rm_dir)

    cmd_crab_submit = "crab submit -c crab_cfg_cutflow.py"
    #os.system(cmd_crab_submit)  
 
    cmd_crab_kill = "crab kill -d crab_"+RequestName+"_cutflow2J1T1"
    #os.system(cmd_crab_kill)



    print "DONE ---i = ",i,"--",RequestName,"--------------------------------------------------------------------------------------------"
    #time.sleep(10) 
