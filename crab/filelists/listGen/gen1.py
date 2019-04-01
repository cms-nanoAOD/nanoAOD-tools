#!/bin/python

import sys, os
import json
from subprocess import Popen, PIPE

cwd=os.getcwd()
sys.path.append(cwd+"/../datasets/")

from Run2016.DATA import data as data16
from Run2016.MC import mc as mc16
from Run2017.DATA import data as data17
from Run2017.MC import mc as mc17
from Run2018.DATA import data as data18
from Run2018.MC import mc as mc18

option="-json"
query="summary dataset=/HWminusJ_HToWW_M125_13TeV_powheg_pythia8/RunIISummer16NanoAODv4-PUMoriond17_Nano14Dec2018_102X_mcRun2_asymptotic_v6-v1/NANOAODSIM"

p = Popen('dasgoclient %s --query "%s"'%(option,query), stdout=PIPE, shell=True)
pipe=p.stdout.read()

jsondata = json.loads(pipe)
print jsondata[0]['summary'][0]['nevents']
