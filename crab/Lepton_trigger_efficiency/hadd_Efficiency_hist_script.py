import os, time ,sys

from dataset_2016 import *
from CRABAPI.RawCommand import crabCommand

if len(sys.argv) != 2:
        print "USAGE: %s <Data year>"%(sys.argv [0])
        sys.exit (1)
year   = sys.argv [1]

if(year == '2016'):
    Datasets = Datasets_2016
    RequestName = RequestName_2016
    DirBase = DirBase_2016



for i in range(0,1):#len(Datasets)):
    crabCommand('getoutput', dir = 'crab_'+RequestName[i])

    Dir = 'crab_'+RequestName[i]+'/results/'
    print Dir
    cmd_rm= "rm -rf "+Dir+"tree*"
    os.system(cmd_rm)
    cmd_rm= "rm -rf "+Dir+RequestName[i]+"_Tagging*"
    os.system(cmd_rm)

    cmd_ls= "ls -ltr "+Dir+"B_*"
    os.system(cmd_ls)

    cmd_hadd= "hadd -f "+Dir+RequestName[i]+"_Tagging_Efficiency.root "+Dir+'B_*'
    os.system(cmd_hadd)

    cmd_rm= "rm -rf "+Dir+"B_*"
    os.system(cmd_rm)
    time.sleep(5) 
    print "DONE -------------------------------------------------------------------------------------------------"
#import subprocess
#subprocess.call(["ls",Dir], stdout=open("hadd.txt",'w'))

