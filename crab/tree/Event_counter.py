import fileinput, string, sys, os, time, datetime,subprocess
import argparse as arg

parser = arg.ArgumentParser(description='inputs discription')
parser.add_argument('-y', '--year', dest='inputs', type=str, nargs=1, help="Year [UL2016preVFP, UL2016postVFP, UL2017, UL2018]")
args = parser.parse_args()


if args.inputs == None:
        print "USAGE: %s [-h] [-y <Data year>]"%(sys.argv [0])
        sys.exit (1)

if args.inputs[0] not in ['UL2016preVFP' , 'UL2016postVFP' , 'UL2017' , 'UL2018']:
    print('Error: Incorrect choice of year, use -h for help')
    exit()

print "year = ",args.inputs[0]
year   = args.inputs[0]
date   = datetime.datetime.now()

if(year == 'UL2016preVFP'):
    from dataset_UL2016preVFP import *
    Datasets = Datasets_MC_UL2016APV
if(year == 'UL2016postVFP'):
    from dataset_UL2016postVFP import *
    Datasets = Datasets_MC_UL2016

if(year == 'UL2017'):
    from dataset_UL2017 import *
    Datasets = Datasets_MC_UL2017

RequestNames = Datasets.keys()
print RequestNames
print "len(Datasets) = ",len(Datasets)

for i in range(0,len(RequestNames)):
    RequestName = RequestNames[i]
    Dataset = Datasets[RequestName]

    print 
    cmd_count = 'dasgoclient --query="file, dataset='+Dataset+' | sum(file.nevents)"'
    print cmd_count
    os.system(cmd_count)
    p = subprocess.Popen(cmd_count, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    #p_status = p.wait()

    print RequestName," : ",output[19:] 
 
