import fileinput, string, sys, os, time, subprocess

from dataset import *
#from dataset_2017 import *
#from dataset_2016_phy3 import*
if len(sys.argv) != 2:
        print "USAGE: %s <Data year>"%(sys.argv [0])
        sys.exit (1)
year   = sys.argv [1]

if(year == '2016'):
    Datasets = Datasets_Alt_MC_2016
    RequestName = RequestName_Alt_MC_2016
    #print(RequestName)
    #sys.exit()
#     Datasets = Datasets_SingleMuon_data_2016
#     RequestName = RequestName_SingleMuon_data_2016

#   Datasets = Datasets_SingleElectron_data_2016
#   RequestName = RequestName_SingleElectron_data_2016

if(year == '2017'):
#    Datasets = Datasets_MC_2017
#    RequestName = RequestName_MC_2017
   
     Datasets = Datasets_SingleMuon_data_2017
     RequestName = RequestName_SingleMuon_data_2017

#   Datasets = Datasets_SingleElectron_data_2017
#   RequestName = RequestName_SingleElectron_data_2017

print "Dataset size = ",len(Datasets)," RequestName size = ",len(RequestName)
for i in range(0,len(Datasets)):
    RN = "crab_"+RequestName[i]+"_Tree_2016"
    cmd_crab_status = "crab status -d "+RN
    os.system(cmd_crab_status)  
    p = subprocess.Popen(cmd_crab_status, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    #print "Command output : ", output

    resubmit_job = 'NO'
    if(output.count("failed")>=2):resubmit_job = raw_input("enouter 'failed' twice should I resubmit the job : ")
    if(resubmit_job=="yes" or resubmit_job=="1"):
	cmd_crab_resubmit = "crab resubmit -d "+RN +" --maxjobruntime 2750"
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
