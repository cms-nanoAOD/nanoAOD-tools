from WMCore.Configuration import Configuration
#from CRABClient.UserUtilities import config, getUsernameFromSiteDB
from CRABClient.UserUtilities import getUsernameFromSiteDB
from subprocess import call, check_output

import sys, os
from re import findall

### CHECK THAT CMS env and it is correct
pwd = os.environ['PWD']
if 'CMSSW_VERSION' not in os.environ:
    print "Do cmsenv!"
    exit(0)
version = os.environ['CMSSW_VERSION']
ok = False
for dir in reversed(pwd.split('/')):
    if version == dir :
        ok = True
        break
if not ok:
    print "Do (redo) cmsenv (2) !"
    exit(0)

config = Configuration()

config.section_("General")
config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh' #script executing in CRAB, need prod.py
config.JobType.inputFiles = [ 'prod.py' , '../scripts/haddnano.py' , '../scripts/keep_and_drop_Input.txt' , '../scripts/keep_and_drop_Output.txt' ] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder	 = True
config.section_("Data")
config.Data.inputDBS = 'global'
config.Data.outLFNDirBase = '/store/user/%s/NanoProd' % (getUsernameFromSiteDB())
config.Data.publication = False
config.section_("Site")
config.Site.storageSite = "T2_IT_Legnaro"


if __name__ == '__main__':

    from CRABAPI.RawCommand import crabCommand
    from CRABClient.ClientExceptions import ClientException
    from httplib import HTTPException
    import sys, os
    import importlib
    from optparse import OptionParser

    cwd=os.getcwd()
    
    parser = OptionParser(usage="%prog -y Year -t DataType")
    parser.add_option("-y", "--year", action="store", dest="year", type="string", default="", help="Specify Year of Run: 2016, 2017, 2018")
    parser.add_option("-t", "--datatype", action="store", dest="datatype", type="string", default="", help="Specify data type: MC, DATA")

    (options, args) = parser.parse_args()

    if options.year=="" or options.datatype=="" :
        parser.print_help()
        sys.exit(1)

    if options.year not in ['2016','2017','2018']:
        print "ENTER Collider Year: 2016,2017,2018"
        sys.exit(1)

    if options.datatype not in ['MC','DATA','mc']:
        print "ENTER EITHER MC OR DATA"
        sys.exit(1)
    
    sys.path.append(cwd+"/filelists/datasets/Run%s/" %options.year)
    DL=importlib.import_module('%s' %options.datatype)
    mc=DL.mc
    config.General.workArea = 'Run%s%s' %(options.year, options.datatype) 
    
    def submit(config):
        if len(sys.argv) ==1:
            ## book the command and run python                                                                                                                                       
            cmd = "python " + sys.argv[0] + " '" + config.General.requestName + "'"
            print "calling: "+cmd
            call(cmd,shell=True)
            return
        if len(sys.argv) > 1:
            ## if it is not in the request try the next                                                                                                                              
            if sys.argv[1] !=       config.General.requestName: return
            ###                                                                                                                                                                      
            print "--- Submitting " + "\033[01;32m" + config.General.requestName + "\033[00m"   + " ---"
            
            config.Data.outputDatasetTag = config.General.requestName
            try:
                crabCommand('submit', config = config)
            except HTTPException as hte:
                print "Failed submitting task: %s" % (hte.headers)
            except ClientException as cle:
                print "Failed submitting task: %s" % (cle)

    def setdata(value="True"):
        if value=='True':
            config.Data.splitting = 'LumiBased'
            url = "https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions16/13TeV/ReReco/Final/"
            config.Data.lumiMask = url + "Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt"
        else:
            config.Data.lumiMask = None
            config.Data.splitting = 'FileBased'

        #for idx,par in enumerate(config.JobType.pyCfgParams):
        #    if "isData" in par:
        #        config.JobType.pyCfgParams[idx] = "isData=" + value
        #        return

    def submitList(l):
        for ll in l:
            split = ll.split('/')                                                     

            ##config.Data.inputDataset
            if split[1] == "lustre":
                ##reading rootfile from a dataset txt
                config.Data.userInputFiles = open(ll).readlines()
                config.Data.outputPrimaryDataset = split[-1].split('.')[0]
            else:
                ##reading each dataset in a txt                                                                                                                                
                config.Data.inputDataset = ll
                print 'config.Data.inputDataset = ', ll

            ##config.General.requestName
            if split[-1]=='NANOAODSIM':
                config.General.requestName = ll.split('/')[1]+'-'+ll.split('/')[-2].split('-')[-1]
                print 'config.General.requestName = ', ll.split('/')[1]+'-'+ll.split('/')[-2].split('-')[-1]
            elif 'ext' in split[-2]:
                ext = findall('ext[0-9]+',split[-2])
                if len(ext)>0:
                    config.General.requestName = split[1] + '_' + ext[0]
                else:
                    config.General.requestName = split[1]
            else:
                #private file                                                                                                                                                        
                config.General.requestName = split[-1].split('.')[0]
            #submit(config)


    #############################################################################################
    ## From now on that's what users should modify: this is the a-la-CRAB2 configuration part. ##
    #############################################################################################
    # EXAMPLE of submitting userInput file, --> /lustre/cmswork/hoh/NANO/SSLep/nanoskim/CMSSW_10_2_10/src/PhysicsTools/NanoAODTools/crab/datatest.txt (SPECIFY FULLPATH)

    ## 2016
    setdata("False")
    config.Data.splitting = 'FileBased'
    config.Data.unitsPerJob = 2

    submitList(mc)

    #setdata("True")
    #config.Data.splitting = 'FileBased'
    #config.Data.unitsPerJob = 2

    #submitList(mc)
