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

#var
parameters=['cross_section','accuracy','total_uncertainty','kFactor','reweighting','refs','comments']
dasDict = {}
procDict = {}
samName="samplesVH"
##Authentication
#p0 = Popen('cern-get-sso-cookie -u https://cms-gen-dev.cern.ch/xsdb -o cookie.txt -krb', stdout=PIPE, shell=True)

option="-json"
year=16
megalist16 = data16+mc16
megalist17 = data17+mc17
megalist18 = data18+mc18

for i,mc in enumerate([megalist16,megalist17,megalist18]):
    empty=[]
    procDict.clear()
    AnaLists = open( 'samplesVH%s.py'%(year+i) , "wt" )
    AnaLists.write('sample = {\n')
    for das in mc:
        dasDict.clear()
        query="summary dataset=%s"%das
        procname=query.split('/')[1]
        #print 'dasgoclient %s --query "%s"'%(option,query)
        p1 = Popen('dasgoclient %s --query "%s"'%(option,query), stdout=PIPE, shell=True)
        pipe1=p1.stdout.read()
        json1 = json.loads(pipe1)
        dasDict['nevents']=json1[0]['summary'][0]['nevents']
        
        if procname not in ['SingleMuon','SingleElectron','DoubleMuon']:
            print 'curl --silent -X POST https://cms-gen-dev.cern.ch/xsdb/api/search -L --cookie cookie.txt  -H "Content-Type:application/json" --data \'{"process_name":"%s"}\''%(procname)
            p2 = Popen('curl --silent -X POST https://cms-gen-dev.cern.ch/xsdb/api/search -L --cookie cookie.txt  -H "Content-Type:application/json" --data \'{"process_name":"%s"}\''%(procname), stdout=PIPE, shell=True)
            pipe2=p2.stdout.read()
            json2 = json.loads(pipe2)
            if len(json2)==0: 
                empty.append(procname)
                for var in parameters:
                    dasDict['%s'%var] = 1.0
            else:
                for var in parameters:
                    if var not in json2[0]:
                        dasDict['%s'%var] = 1.0
                    else:
                        dasDict['%s'%var] = str(json2[0]['%s'%var])
            
        else:
            for var in parameters:
                dasDict['%s'%var] = 1.0

        # write to file
        if procname not in ['SingleMuon','SingleElectron','DoubleMuon']:
            AnaLists.write('\t\'%s\' : {\n' % (procname))
        else:
            AnaLists.write('\t\'%s\' : {\n' % (procname+query.split('/')[2]))
        AnaLists.write('\t\'nevents\' : %s,\n' % int(dasDict['nevents']))
        AnaLists.write('\t\'xsec\' : %s,\n' % float(dasDict['cross_section']))
        AnaLists.write('\t\'xmatcheff\' : 1.0,\n')
        AnaLists.write('\t\'kfactor\' : %s,\n' % float(dasDict['kFactor']))
        AnaLists.write('\t\t},\n')
    AnaLists.write('}\n')
    AnaLists.write('\n')
    AnaLists.close()
    os.system("cat templates/legends.py >> samplesVH%s.py"%(year+i))

    print "Empty entry for 20%s samples:" %(year+i)
    print empty
