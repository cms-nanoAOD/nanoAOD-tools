from WMCore.Configuration import Configuration
#from CRABClient.UserUtilities import config, getUsernameFromSiteDB
from CRABClient.UserUtilities import getUsernameFromSiteDB
from subprocess import call, check_output

import sys, os
from re import findall
import time

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
config.General.transferLogs=False
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh' #script executing in CRAB, need prod.py
config.JobType.inputFiles = [ 'prod.py' , '../scripts/haddnano.py' , '../scripts/keep_and_drop_Input.txt' , '../scripts/keep_and_drop_Output.txt' ] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder	 = True
config.JobType.maxMemoryMB = 2500
config.JobType.priority = 999
config.section_("Data")
config.Data.inputDBS = 'global'
config.Data.outLFNDirBase = '/store/user/%s/NanoProdv1' % (getUsernameFromSiteDB())
config.Data.publication = False
config.section_("Site")
#config.Site.whitelist = [ 'T2_IT_Legnaro' , 'T2_IT_Bari ' , 'T2_IT_Pisa' , 'T2_IT_Rome ' , 'T2_AT_Vienna' , 'T2_BE_UCL' , 'T2_CH_CERN ' , 'T2_DE_DESY' , 'T2_DE_RWTH' , 'T2_UK_London_Brunel' , 'T2_HU_Budapest' , 'T2_CN_Beijing' , 'T2_CH_CSCS_HPC' , 'T2_US_MIT' , 'T3_US_FNALLPC' ]
config.Site.storageSite = "T2_IT_Legnaro"


if __name__ == '__main__':

    from CRABAPI.RawCommand import crabCommand
    from CRABClient.ClientExceptions import ClientException
    from httplib import HTTPException
    import sys, os
    import importlib
    from optparse import OptionParser

    cwd=os.getcwd()
    
    parser = OptionParser(usage="%prog -y Year")
    parser.add_option("-y", "--year", action="store", dest="year", type="string", default="", help="Specify Year of Run: 2016, 2017, 2018")
    #parser.add_option("-t", "--datatype", action="store", dest="datatype", type="string", default="", help="Specify data type: MC, DATA")

    (options, args) = parser.parse_args()

    if options.year=="":
        parser.print_help()
        sys.exit(1)

    if options.year not in ['2016','2017','2018']:
        print "ENTER Collider Year: 2016,2017,2018"
        sys.exit(1)
    
    sys.path.append(cwd+"/filelists/datasets/Run%s/" %options.year)
    #config.General.workArea = 'Run%s%s' %(options.year, options.datatype) 
    
    def submit(config):
        if len(sys.argv) ==1:
            ## book the command and run python                                                                                                                  
            cmd = "python " + sys.argv[0] + " '" + config.General.requestName + "'"
            print "calling: "+cmd
            call(cmd,shell=True)
            return
        if len(sys.argv) > 1:
            ## if it is not in the request try the next                                                                                                                       
            #if sys.argv[1] !=       config.General.requestName: return
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
            DL=importlib.import_module('DATA')
            global data
            data=DL.data
            config.General.workArea = 'Run%sDATA' %options.year
            config.Data.splitting = 'LumiBased'
            config.Data.unitsPerJob = 100
            #NJOBS=500
            #config.Data.totalUnits = config.Data.unitsPerJob*NJOBS #58962
            
            ##Generate too much file
            #config.Data.splitting = 'EventAwareLumiBased'
            #config.Data.unitsPerJob = 12000
            
            #NOTE : 2016 is Era dependent:
            if options.year == "2016":
                token = options.year.split('0')[1]
                url = "https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions%s/13TeV/ReReco/Final/" %token
                config.Data.lumiMask = url + "Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt"
            if options.year == "2017":
                token = options.year.split('0')[1]
                url = "https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions%s/13TeV/ReReco/" %token
                config.Data.lumiMask = url + "Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt"
            elif options.year == "2018":
                token = options.year.split('0')[1]
                url = "https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions%s/13TeV/ReReco/" %token
                config.Data.lumiMask = url + "Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt"
                
        else:
            DL=importlib.import_module('MC')
            global mc
            mc=DL.mc
            config.General.workArea = 'Run%sMC' %options.year

            config.Data.lumiMask = None
            config.Data.splitting = 'FileBased' #EventBased
            config.Data.unitsPerJob = 2 #number of files per jobs
            NJOBS=5
            config.Data.totalUnits = config.Data.unitsPerJob*NJOBS

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
                #print 'config.Data.inputDataset = ', ll
                
            ##config.General.requestName
            if split[-1] == "NANOAODSIM":
                config.General.requestName = ll.split('/')[1]+'-'+ll.split('/')[-2].split('-')[-1]
                #print 'config.General.requestName = ', ll.split('/')[1]+'-'+ll.split('/')[-2].split('-')[-1]
            elif split[-1] == "NANOAOD":
                config.General.requestName = ll.split('/')[1]+"_"+ll.split('/')[2].split('-')[0]+"_"+ll.split('/')[2].split('-')[2]
                #print 'config.General.requestName = ', ll.split('/')[1]+"_"+ll.split('/')[2].split('-')[0]+"_"+ll.split('/')[2].split('-')[2]
            #elif 'ext' in split[-2]:
            #    ext = findall('ext[0-9]+',split[-2])
            #    if len(ext)>0:
            #        config.General.requestName = split[1] + '_' + ext[0]
            #    else:
            #        config.General.requestName = split[1]
            #else:
            #    #private file                                                                                                                                              
            #    config.General.requestName = split[-1].split('.')[0]
            '''
                if options.year == "2016":
                    #url="%s/src/PhysicsTools/NanoAODTools/data/GoldenJSON/Run2016/" %os.environ['CMSSW_BASE']
                    url="https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions16/13TeV/Era/ReReco/"
                    era=split[2].split('-')[0].split('Run%s' %options.year)[1]
                    if era in ['B','B_ver1','B_ver2']:
                        config.Data.lumiMask = url + "Cert_272007-275376_13TeV_23Sep2016ReReco_Collisions16_JSON_eraB.txt"
                        print "--- \033[93m ERA DEPENDENT 2016 RUN = %s \033[00m ---" %era
                    elif era in ['C']:
                        config.Data.lumiMask = url + "Cert_275657-276283_13TeV_23Sep2016ReReco_Collisions16_JSON_eraC.txt"
                        print "--- \033[93m ERA DEPENDENT 2016 RUN = %s \033[00m ---" %era
                    elif era in ['D']:
                        config.Data.lumiMask = url + "Cert_276315-276811_13TeV_23Sep2016ReReco_Collisions16_JSON_eraD.txt"
                        print "--- \033[93m ERA DEPENDENT 2016 RUN = %s \033[00m ---" %era
                    elif era in ['E']:
                        config.Data.lumiMask = url + "Cert_276831-277420_13TeV_23Sep2016ReReco_Collisions16_JSON_eraE.txt"
                        print "--- \033[93m ERA DEPENDENT 2016 RUN = %s \033[00m ---" %era
                    elif era in ['F']:
                        config.Data.lumiMask = url + "Cert_277772-278808_13TeV_23Sep2016ReReco_Collisions16_JSON_eraF.txt"
                        print "--- \033[93m ERA DEPENDENT 2016 RUN = %s \033[00m ---" %era
                    elif era in ['G']:
                        config.Data.lumiMask = url + "Cert_278820-280385_13TeV_23Sep2016ReReco_Collisions16_JSON_eraG.txt"
                        print "--- \033[93m ERA DEPENDENT 2016 RUN = %s \033[00m ---" %era
                    elif era in ['H']:
                        config.Data.lumiMask = url + "Cert_280919-284044_13TeV_PromptReco_Collisions16_JSON_eraH.txt" #--> ?
                        print "--- \033[93m ERA DEPENDENT 2016 RUN = %s \033[00m ---" %era
                else:
                    print "ERROR on 2016 cert id, quitting"
                    exit
            '''

            #submit(config)


    #############################################################################################
    ## From now on that's what users should modify: this is the a-la-CRAB2 configuration part. ##
    #############################################################################################
    # EXAMPLE of submitting userInput file, --> /lustre/cmswork/hoh/NANO/SSLep/nanoskim/CMSSW_10_2_10/src/PhysicsTools/NanoAODTools/crab/datatest.txt (SPECIFY FULLPATH)
    start_time = time.time()

    setdata("False")
    submitList(mc)
    
    setdata("True")
    submitList(data)

    print("--- %s seconds ---" % (time.time() - start_time))
    print("--- %s minutes ---" % ( (time.time() - start_time)/60. ))
    print("--- %s hours ---" % ( (time.time() - start_time)/3600. ))
