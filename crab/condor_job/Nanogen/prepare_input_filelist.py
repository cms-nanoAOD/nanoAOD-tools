import fileinput, string, sys, os, time, subprocess
import argparse as arg

parser = arg.ArgumentParser(description='inputs discription')
parser.add_argument('-y', '--year', dest='inputs', type=str, nargs=1, help="Year [ UL2016 ]")
parser.add_argument('-s', '--sample', dest='samples', type=str, nargs=1, help="sample [ Mc ]")
parser.add_argument('-c', '--channel', dest='channels', type=str, nargs=1, help="sample [ Tbarchannel_wtop0p55 ]")
args = parser.parse_args()

print args
if args.inputs[0] == None:
        print "USAGE: %s [-h] [-y <Data year>]"%(sys.argv [0])
        sys.exit (1)

if args.inputs[0] not in ['UL2016']:
    print('Error: Incorrect choice of year, use -h for help')
    exit()
if args.samples[0] not in ['Mc']:
    print('Error: Incorrect choice of sample type, use -h for help')
    exit()


print "year = ",args.inputs[0]
year   = args.inputs[0]
sample = args.samples[0]
channel = args.channels[0]

if(year == 'UL2016'):
    from dataset_UL2016_phy3 import *
    if sample=="Mc" : Datasets = Datasets_MC_UL2016

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

crab_scriptfile = "crab_script_NanoGen_minitree.py"


for i in range(0,len(RequestNames)):
    RequestName = RequestNames[i]
    Dataset = Datasets[RequestNames[i]][0]

    print RequestName, " : ", Dataset

    Input_files="All_input_files_"+RequestName+".txt"
    cmd_dasgoclint = 'dasgoclient -query="file dataset='+Dataset+' instance=prod/phys03" > '+Input_files
    print cmd_dasgoclint
    os.system(cmd_dasgoclint) 
    cmd_dasgoclint = 'dasgoclient -query="file dataset='+Dataset+' instance=prod/phys03"'
    os.system(cmd_dasgoclint)

    Inputline = 'INPUT\n'

    replacemachine(crab_scriptfile,'inputFiles=',Inputline)

