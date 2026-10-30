import fileinput, string, sys, os, time, subprocess
import argparse as arg

parser = arg.ArgumentParser(description='inputs discription')
parser.add_argument('-y', '--year', dest='inputs', type=str, nargs=1, help="Year [ UL2016preVFP , UL2016postVFP , UL2017 , UL2018 ]")
parser.add_argument('-s', '--sample', dest='samples', type=str, nargs=1, help="sample [ Mc , Data ]")
parser.add_argument('-l', '--lepton', dest='leptons', type=str, nargs=1, help="sample [ mu , el ]")

args = parser.parse_args()


if args.inputs == None:
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
elif args.samples[0] == "Data": lep = args.leptons[0]

print "year = ",args.inputs[0]
year   = args.inputs[0]
sample = args.samples[0]

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
    if sample=="Mc" : Datasets = Datasets_sys_MC_UL2018
    elif sample=="Data" and lep=="mu" : Datasets = Datasets_SingleMuon_data_UL2018
    elif sample=="Data" and lep=="el" : Datasets = Datasets_SingleElectron_data_UL2018

RequestNames = Datasets.keys()
print "len(Datasets) = ",len(Datasets)


print "Dataset size = ",len(Datasets)," RequestName size = ",len(RequestNames)

for i in range(0,len(RequestNames)):
    RN = "crab_"+RequestNames[i]+"_Minitree_2J1T1_"+year
    print "RequestName = ",RN
    cmd_crab_status = "crab status -d "+RN
    os.system(cmd_crab_status)  
    p = subprocess.Popen(cmd_crab_status, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    #print "Command output : ", output

    resubmit_job = 'NO'
    print "failed : ",output.count("failed")," memory : ",output.count("memory")
    if(output.count("failed")>=2 and output.count("memory")<2):resubmit_job = raw_input("enouter 'failed' twice should I resubmit the job : ")
    if(output.count("failed")>=3 and output.count("memory")>=2):resubmit_job = raw_input("enouter 'failed' twice should I resubmit the job : ")
    if(resubmit_job=="yes" or resubmit_job=="1"):
	cmd_crab_resubmit = "crab resubmit -d "+RN# + " --maxmemory 4000"#+" --maxjobruntime 2750"
	os.system(cmd_crab_resubmit)
    print "DONE ---------------------------crab status---------------------------------------------------------------------"
    cmd_crab_report = "crab report -d "+RN
    #os.system(cmd_crab_report)

    cms_crab_getoutput = "crab getoutput "+RN+" --xrootd --quantity=1 --jobids=1"
    #os.system(cms_crab_getoutput)

    cms_crab_getoutput = "crab getoutput "+RN+" --xrootd --quantity=1"# --jobids=1"
    #os.system(cms_crab_getoutput)

    cmd_crab_kill = "crab kill "+RN
    #os.system(cmd_crab_kill)

    cmd_crab_purge = "crab purge "+RN
    #os.system(cmd_crab_purge)
    print "DONE ---------------------------crab report---------------------------------------------------------------------"

    print "resubmit job status yes/no(1/0) = %s"%(resubmit_job)
    resubmit_job='No' 
    print "DONE -------------------------------------------------------------------------------------------------"
    #time.sleep(5) 
