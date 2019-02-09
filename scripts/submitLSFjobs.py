#!/usr/bin/env python
import os, re
import commands
import math, time
import sys
import importlib
from PhysicsTools.NanoAODTools.samplesVH import sample

cwd=os.getcwd()
sys.path.append(cwd+"/batch/filelists/")

########## OPTIONS ##########

import optparse
usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)
parser.add_option('-b', '--base',         action='store', type='string', dest='base',         default='$CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/')
parser.add_option('-o', '--output',       action='store', type='string', dest='output',       default='')
parser.add_option('-c', '--cfg',          action='store', type='string', dest='cfg',          default='')
parser.add_option('-l', '--samplelists',  action='store', type='string', dest='samplelists',  default='base')
parser.add_option('-q', '--queue',        action='store', type='string', dest='queue',        default='local-cms-short')
parser.add_option('-s', '--preselection', action='store', type='string', dest='preselection', default='')
parser.add_option('-e', '--Nevent',       action='store', type="int",    dest='Nevent',       default=-1, help="Number of event for processing")
parser.add_option('-m', '--maxlsftime',   action='store', type='int',    dest='maxlsftime',   default=4)
parser.add_option('-p', '--eventspersec', action='store', type='int',    dest='eventspersec', default=25)

(options, args) = parser.parse_args()

print
if not os.path.exists(os.path.expandvars(options.base)):
    print '--- ERROR ---'
    print '  \''+options.base+'\' path not found expanding '+options.base
    print '  please point to the correct path to scripts/ using option \'-b $CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/\'' 
    print 
    exit()

if not os.path.exists(os.path.expandvars(options.base+options.cfg)):
    print '--- ERROR ---'
    print '  \''+options.cfg+'\' file not found in '+options.base+options.cfg
    print '  please point to a valid cfg file using option \'-c CFG-FILENAME\'' 
    print 
    exit()

path = os.getcwd()
if len(options.output) == 0 or os.path.exists(options.output):
    print '--- ERROR ---'
    print '  \''+options.output+'\' folder already exists or is null!'
    print '  please delete it or use a different name using option \'-o FOLDER-NAME\'' 
    print 
    exit()
os.system('mkdir '+options.output)


########## IMPORT SAMPLELIST ##########

samplelistmod = importlib.import_module('samplelist_'+options.samplelists)
samplelists = samplelistmod.samplelists


########## LOOP ON SAMPLELISTS ##########
#1 job/1 root file
for l in samplelists:
    tag=l.split("/")[-1].split('.')[0]
    if not tag in sample:
        if not '_Skim' in tag:
            print tag, 'not in samples\n'
            continue

    #dir= 'Run2016' if 'Run2016' in l else 'Summer16'
    print "one rootfile one job: processing rootfile --> %s" %l
    #file=open(os.path.expandvars(options.base+'filelists/'+dir+'/'+l+'.txt'),'r')
    #filelist = file.readlines()
    #splitting= max(int(float(sample[l]['nevents'])/(options.maxlsftime*3600*options.eventspersec)),1)
    #njobs    = int(len(filelist)/splitting)+1
    #sublists = [filelist[i:i+njobs] for i in range(0, len(filelist), njobs)]
    #print '\nSplitting',l,'in',len(sublists),'chunk(s) of approximately',njobs,'files each'
    lfold = options.output+'/'+tag
    os.system('mkdir '+lfold)
    if lfold.find('lustre')!= -1: outputbase = ""
    else: outputbase = options.base
    os.chdir(lfold)
 
#   ########## LOOP ON LSF JOB ##########
#    for x in range(len(sublists)):
#        lsubfold = lfold+'/'+str(x).zfill(4)
#        os.system('mkdir '+lsubfold)
#        os.chdir(lsubfold)
#        splitlist=open('list.txt','w')  
#        splitlist.write(''.join(str(x) for x in sublists[x]))
#        splitlist.close()
        
    with open('job.sh', 'w') as fout:
            #fout.write('#!/bin/bash\n')
            #fout.write('#BSUB -J '+l+'_'+str(x).zfill(4)+'\n')
        fout.write('echo "PWD:"\n')
        fout.write('pwd\n')
        fout.write('export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch\n')
        fout.write('source $VO_CMS_SW_DIR/cmsset_default.sh\n')
        fout.write('echo "environment:"\n')
        fout.write('echo\n')
        fout.write('env > local.env\n')
        fout.write('env\n')
        fout.write('# ulimit -v 3000000 # NO\n')
        fout.write('echo "copying job dir to worker"\n')
        fout.write('eval `scram runtime -sh`\n')
        fout.write('ls\n')
        fout.write('echo "running"\n')
        #fout.write('python '+options.base+options.cfg+' ./ '+l+' -c \"'+options.preselection+'\" -b \"'+options.base+options.keepdropmenu+'\" -I '+options.pythonmodule+'\n')
        fout.write('python '+options.base+options.cfg+' ./ '+l+' -c \"'+options.preselection+'\" -e %s\n' %options.Nevent)
        fout.write('exit $?\n') 
        fout.write('echo ""\n')
    os.system('chmod 755 job.sh')
        
    ########## SEND JOB ON LSF QUEUE ##########
    os.system('bsub -q '+options.queue+' -o logs < job.sh')
        #print 'filelist ' + l + ' - job nr ' + str(x).zfill(4) + ' -> submitted'
    os.chdir('../../')
   
print
print 'CURRENT JOB SUMMARY:'
os.system('bjobs')
print
