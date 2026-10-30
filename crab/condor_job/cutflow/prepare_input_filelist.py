import fileinput, string, sys, os, time, subprocess
import argparse as arg

parser = arg.ArgumentParser(description='inputs discription')
parser.add_argument('-y', '--year', dest='inputs', type=str, nargs=1, help="Year [ UL2016preVFP , UL2016postVFP , UL2017 , UL2018 ]")
parser.add_argument('-s', '--sample', dest='samples', type=str, nargs=1, help="sample [ Mc , Data ]")
parser.add_argument('-l', '--lepton', dest='leptons', type=str, nargs=1, help="sample [ mu , el ]")
parser.add_argument('-r', '--region', dest='regions', type=str, nargs=1, help="sample [ 2J1T1 , 2J1T0 ]")
parser.add_argument('-c', '--channel', dest='channels', type=str, nargs=1, help="sample [ TChannel, TbarChannel ]")
args = parser.parse_args()

print args
if args.inputs[0] == None:
        print "USAGE: %s [-h] [-y <Data year>]"%(sys.argv [0])
        sys.exit (1)

if args.inputs[0] not in ['UL2016preVFP', 'UL2016postVFP','UL2017','UL2018']:
    print('Error: Incorrect choice of year, use -h for help')
    exit()
if args.samples[0] not in ['Mc', 'Data']:
    print('Error: Incorrect choice of sample type, use -h for help')
    exit()
elif args.samples[0] == "Data" and args.leptons[0] not in ['mu','el']:
    print('Error: Incorrect choice of lepton type, use -h for help')
    exit()
#elif args.samples[0] == "Data": lep = args.leptons[0]
lep = args.leptons[0]

if args.regions[0] not in [ '2J1T1' , '2J1T0' ]:
        print "Error: Incorrect choice of region, use -h for help"
        sys.exit (1)


print "year = ",args.inputs[0]
year   = args.inputs[0]
sample = args.samples[0]
region = args.regions[0]
channel = args.channels[0]

if(year == 'UL2016preVFP'):
    from dataset_UL2016preVFP_phy3 import *
    if sample=="Mc" : Datasets = Datasets_MC_UL2016APV
    elif sample=="Data" and lep=="mu" : Datasets = Datasets_SingleMuon_data_UL2016APV
    elif sample=="Data" and lep=="el" : Datasets = Datasets = Datasets_SingleElectron_data_UL2016APV
if(year == 'UL2016postVFP'):
    from dataset_UL2016postVFP_phy3 import *
    if sample=="Mc" : Datasets = Datasets_MC_UL2016
    elif sample=="Data" and lep=="mu" : Datasets = Datasets_SingleMuon_data_UL2016
    elif sample=="Data" and lep=="el" : Datasets = Datasets_SingleElectron_data_UL2016
if(year == 'UL2017'):
    from dataset_UL2017_phy3 import *
    if sample=="Mc" : Datasets = Datasets_MC_UL2017
    elif sample=="Data" and lep=="mu" : Datasets = Datasets_SingleMuon_data_UL2017
    elif sample=="Data" and lep=="el" : Datasets = Datasets_SingleElectron_data_UL2017
if(year == 'UL2018'):
    from dataset_UL2018_phy3 import *
    if sample=="Mc" : Datasets = Datasets_MC_UL2018
    elif sample=="Data" and lep=="mu" : Datasets = Datasets_SingleMuon_data_UL2018
    elif sample=="Data" and lep=="el" : Datasets = Datasets_SingleElectron_data_UL2018

RequestNames = []
RequestNames.append(channel)
#Datasets.keys()
print "len(Datasets) = ",len(Datasets)
print "Dataset size = ",len(Datasets)," RequestName size = ",len(RequestNames)

def replacemachine(fileName, sourceText, replaceText):
    print "editing ",fileName,
    ##################################################################
    for line in fileinput.input(fileName, inplace=True):
        if line.strip().startswith(sourceText):
                line = replaceText
        sys.stdout.write(line)
    print "All went well, the modifications are done"
    ##################################################################

crab_scriptfile = "condor_script_cutflow.py"
MainModule = "cutflowModule_new.py"


for i in range(0,len(RequestNames)):
    if(sample == "Data"):
    	RequestName = RequestNames[i]
    	Dataset = Datasets[RequestNames[i]]
    else:
	RequestName = RequestNames[i]
        Dataset = Datasets[RequestNames[i]][0]
        NumberOfEvents = Datasets[RequestNames[i]][1]
        Xsection = Datasets[RequestNames[i]][2]

    print RequestName, " : ", Dataset

    Input_files="All_input_files_"+RequestName+".txt"
    cmd_dasgoclint = 'dasgoclient -query="file dataset='+Dataset+' instance=prod/phys03" > '+Input_files
    os.system(cmd_dasgoclint) 

    region_tag = region
    if(sample == "Mc"): 
    	update_NumberOfEvents = "\t\tNEvents = "+NumberOfEvents+"\n"
    	update_Xsection = "\t\tx_sec = "+Xsection+"\n"
    	modules = "modules=cutflowModuleConstr_"+region_tag+"_"+lep+"_mc_"+year+"()\n"
    else:
	modules = "modules=cutflowModuleConstr_"+region_tag+"_"+lep+"_data_"+year+"()\n"

    print modules
    if(sample == "Mc"): 
    	print "\tNumber of Events = ",NumberOfEvents  
    	print "\tXsection = ",Xsection	   

    	replacemachine(MainModule,'NEvents = ', update_NumberOfEvents )
    	replacemachine(MainModule,'x_sec = ',update_Xsection)

    replacemachine(crab_scriptfile,'modules=', modules )
    replacemachine(crab_scriptfile,'#inputFiles=','\n')
    replacemachine(crab_scriptfile,'inputFiles=','INPUT\n')
