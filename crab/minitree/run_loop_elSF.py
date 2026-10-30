import fileinput, string, sys, os, time, subprocess
import argparse as arg

parser = arg.ArgumentParser(description='inputs discription')
parser.add_argument('-y', '--year', dest='inputs', type=str, nargs=1, help="Year [ UL2016preVFP , UL2016postVFP , UL2017 , UL2018 ]")
parser.add_argument('-s', '--sample', dest='samples', type=str, nargs=1, help="sample [ Mc_Nomi , Mc_Alt , Mc_sys , Data ]")
parser.add_argument('-l', '--lepton', dest='leptons', type=str, nargs=1, help="sample [ mu , el ]")
parser.add_argument('-r', '--region', dest='regions', type=str, nargs=1, help="sample [ 2J1T1 , 2J1T0 ]")
parser.add_argument('-c', '--channel', dest='channels', type=str, nargs=1, help="sample [ TChannel, TbarChannel ]")
args = parser.parse_args()

print(args)
if args.inputs[0] == None:
        print("USAGE: %s [-h] [-y <Data year>]"%(sys.argv [0]))
        sys.exit (1)

if args.inputs[0] not in ['UL2016preVFP', 'UL2016postVFP','UL2017','UL2018']:
    print('Error: Incorrect choice of year, use -h for help')
    exit()
if args.samples[0] not in ['Mc_Nomi', 'Mc_Alt', 'Mc_sys', 'Data']:
    print('Error: Incorrect choice of sample type, use -h for help')
    exit()
elif args.samples[0] == "Data" and args.leptons[0] not in ['mu','el']:
    print('Error: Incorrect choice of lepton type, use -h for help')
    exit()
#elif args.samples[0] == "Data": lep = args.leptons[0]
lep = args.leptons[0]

if args.regions[0] not in [ '2J1T1' , '2J1T0', '2J0T1' , '2J0T0', '3J1T1' , '3J1T0', '3J2T1' , '3J2T0', '2J1L0T1', '2J1L0T0']:
        print("Error: Incorrect choice of region, use -h for help")
        sys.exit (1)


print("year = ",args.inputs[0])
year   = args.inputs[0]
sample = args.samples[0]
region = args.regions[0]
channel = args.channels[0]

if(year == 'UL2016preVFP'):
    from dataset_UL2016preVFP_phy3 import *
    if sample=="Mc_Nomi" : Datasets = Datasets_MC_UL2016APV
    if sample=="Mc_Alt" : Datasets = Datasets_Alt_MC_UL2016APV
    if sample=="Mc_sys" : Datasets = Datasets_sys_MC_UL2016APV
    elif sample=="Data" and lep=="mu" : Datasets = Datasets_SingleMuon_data_UL2016APV
    elif sample=="Data" and lep=="el" : Datasets = Datasets = Datasets_SingleElectron_data_UL2016APV
if(year == 'UL2016postVFP'):
    from dataset_UL2016postVFP_phy3 import *
    if sample=="Mc_Nomi" : Datasets = Datasets_MC_UL2016
    if sample=="Mc_Alt" : Datasets = Datasets_Alt_MC_UL2016
    if sample=="Mc_sys" : Datasets = Datasets_sys_MC_UL2016
    elif sample=="Data" and lep=="mu" : Datasets = Datasets_SingleMuon_data_UL2016
    elif sample=="Data" and lep=="el" : Datasets = Datasets_SingleElectron_data_UL2016
if(year == 'UL2017'):
    from dataset_UL2017_phy3 import *
    if sample=="Mc_Nomi" : Datasets = Datasets_MC_UL2017
    if sample=="Mc_Alt" : Datasets = Datasets_Alt_MC_UL2017
    if sample=="Mc_sys" : Datasets = Datasets_sys_MC_UL2017
    elif sample=="Data" and lep=="mu" : Datasets = Datasets_SingleMuon_data_UL2017
    elif sample=="Data" and lep=="el" : Datasets = Datasets_SingleElectron_data_UL2017
if(year == 'UL2018'):
    from dataset_UL2018_phy3 import *
    if sample=="Mc_Nomi" : Datasets = Datasets_MC_UL2018
    if sample=="Mc_Alt" : Datasets = Datasets_Alt_MC_UL2018
    if sample=="Mc_sys" : Datasets = Datasets_sys_MC_UL2018
    elif sample=="Data" and lep=="mu" : Datasets = Datasets_SingleMuon_data_UL2018
    elif sample=="Data" and lep=="el" : Datasets = Datasets_SingleElectron_data_UL2018

#RequestNames = []
#RequestNames.append(channel)
#Datasets.keys()
#print("len(Datasets) = ",len(Datasets))
#print("Dataset size = ",len(Datasets)," RequestName size = ",len(RequestNames))

def replacemachine(fileName, sourceText, replaceText):
    print( "editing ",fileName,)
    ##################################################################
    for line in fileinput.input(fileName, inplace=True):
        if line.strip().startswith(sourceText):
                line = replaceText
        sys.stdout.write(line)
    print("All went well, the modifications are done")
    ##################################################################

crab_scriptfile = "crab_script_Minitree.py"



channels = ['Tchannel' , 'Tbarchannel','tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic', 'WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJets', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L','QCD']
for channel in channels:
    Input_files="inputFiles=['/nfs/home/common/RUN2_UL/Minitree_ui/SEVENTEEN/minitree/Mc/"+region+"/Minitree_"+channel+"_"+region+"_el.root']"
    replacemachine(crab_scriptfile,'inputFiles=',Input_files+'\n')
    cmd_run= 'python3 '+crab_scriptfile
    os.system(cmd_run)
