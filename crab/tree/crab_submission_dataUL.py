import fileinput, string, sys, os, time, datetime
import argparse as arg 
import re

parser = arg.ArgumentParser(description='inputs discription')
parser.add_argument('-y', '--year', dest='years', type=str, nargs=1, help="Year [ UL2016preVFP , UL2016postVFP , UL2017 , UL2018]")
parser.add_argument('-l', '--lep', dest='leptons', type=str, nargs=1, help="lepton [ el , mu ]")


args = parser.parse_args()

if (args.years == None or args.leptons == None):
        print "USAGE: %s [-h] [-y <Data year> -l <lepton>]"%(sys.argv [0])
        sys.exit (1)

if args.years[0] not in ['UL2016preVFP','UL2016postVFP','UL2017','UL2018']:
    print('Error: Incorrect choice of year, use -h for help')
    exit()

if args.leptons[0] not in ['el','mu']:
    print('Error: Incorrect choice of lepton, use -h for help')
    exit()


print "year = ",args.years[0]
print "lepton = ",args.leptons[0]
lep    = args.leptons[0]
year   = args.years[0]
date   = datetime.datetime.now()

if(year == 'UL2016preVFP'):                                                                         
    outputDir = "/store/user/mikumar/RUN2_UL/Tree_crab/SIXTEEN/Data_preVFP_"+lep+"/"          
    from dataset_UL2016preVFP import *
    if(lep=="mu"):
        Datasets = Datasets_SingleMuon_data_UL2016APV                                                   
    if(lep=="el"):
        Datasets = Datasets_SingleElectron_data_UL2016APV 

if(year == 'UL2016postVFP'):
    outputDir = "/store/user/mikumar/RUN2_UL/Tree_crab/SIXTEEN/Data_postVFP_"+lep+"/"
    from dataset_UL2016postVFP import *
    if(lep=="mu"):
    	Datasets = Datasets_SingleMuon_data_UL2016
    if(lep=="el"):
     	Datasets = Datasets_SingleElectron_data_UL2016

if(year == 'UL2017'):
    outputDir = "/store/user/mikumar/RUN2_UL/Tree_crab/SEVENTEEN/Data_"+lep+"/"
    from dataset_UL2017 import *
    if(lep=="mu"):
     	Datasets = Datasets_SingleMuon_data_UL2017
    if(lep=="el"):
     	Datasets = Datasets_SingleElectron_data_UL2017

if(year == 'UL2018'):
    outputDir = "/store/user/mikumar/RUN2_UL/Tree_crab/EIGHTEEN/Data_"+lep+"/"
    from dataset_UL2018 import *
    if(lep=="mu"):
        Datasets = Datasets_SingleMuon_data_UL2018_GT36
    if(lep=="el"):
        Datasets = Datasets_SingleElectron_data_UL2018

RequestNames = Datasets.keys()
print "\tlen(Datasets) = ",len(Datasets)
print RequestNames
cfgfile = "crab_cfg_skimTree.py"
scriptfile = "crab_script_skimTree.py"

def replacemachine(fileName, sourceText, replaceText):
    ##################################################################
    for line in fileinput.input(fileName, inplace=True):
        if line.strip().startswith(sourceText):
        	line = replaceText
    	sys.stdout.write(line)
    print "All went well, the modifications are done"
    ##################################################################

for i in range(0,len(RequestNames)):
    RequestName = RequestNames[i]
    Dataset = Datasets[RequestName]
    print Dataset
    print RequestName
    update_RequestName = "config.General.requestName = '"+RequestName+"_Tree_"+year+"'\n" 
    update_Dataset = "config.Data.inputDataset = '"+Dataset+"'\n"
    update_DirBase = "config.Data.outLFNDirBase = '"+outputDir+RequestName+"'\n"
    update_DatasetTag = "config.Data.outputDatasetTag = 'Tree_"+date.strftime("%d")+"_"+date.strftime("%b")+date.strftime("%y")+"_"+RequestName+"'\n"
    if(year=='UL2016postVFP' or year=='UL2016preVFP'): update_Golgonjsonfile = "config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt'\n"
    elif(year=='UL2017'): update_Golgonjsonfile = "config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt'\n"
    elif(year=='UL2018'): update_Golgonjsonfile = "config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt'\n"
    update_site = "config.Site.storageSite = 'T3_CH_CERNBOX'\n" #'T2_IN_TIFR'\n"
    update_data_splitting = "config.Data.splitting = 'LumiBased'\n"
    update_data_unitsPerJon = "config.Data.unitsPerJob = 150\n"
    update_publication = "config.Data.publication = False\n"
    print update_Golgonjsonfile
 
#    update_DatasetTag = "config.Data.outputDatasetTag = 'Tree_october_Seventeen_"+RequestName[i]+"'\n"
    update_InputFiles = "config.JobType.inputFiles = ['crab_script_skimTree.py','../../scripts/haddnano.py','keep_and_drop.txt','MainModule.py']\n"    
    if(lep=="el"): update_module = "\t\tmodules=[MainModuleConstr_data_"+year+"_singleElectron()],\n"
    if(lep=="mu"): update_module = "\t\tmodules=[MainModuleConstr_data_"+year+"_singleMuon()],\n"
    print update_module
    print "\tRequestName = ",update_RequestName ,"\tDatasets = ",update_Dataset,"\tDirBase = ",update_DirBase,"\tDatasetTag = ",update_DatasetTag	   
    print "\tInputFiles = ",update_InputFiles
    
    replacemachine(cfgfile,'config.General.requestName =', update_RequestName)
    replacemachine(cfgfile,'config.Data.inputDataset =', update_Dataset )
    replacemachine(cfgfile,'config.Data.outLFNDirBase =', update_DirBase )
    replacemachine(cfgfile,'config.Data.outputDatasetTag =', update_DatasetTag )
    replacemachine(cfgfile,'config.JobType.inputFiles =', update_InputFiles )
    replacemachine(cfgfile,'config.Data.lumiMask =', update_Golgonjsonfile )
    replacemachine(cfgfile,'"""config.Data.lumiMask ="""', update_Golgonjsonfile )
    replacemachine(cfgfile,'config.Site.storageSite =', update_site )
    replacemachine(cfgfile,'config.Data.splitting =', update_data_splitting )
    replacemachine(cfgfile,'config.Data.unitsPerJob =', update_data_unitsPerJon )
    replacemachine(cfgfile,'config.Data.publication =', update_publication )
    replacemachine(scriptfile,'modules=', update_module )

    cmd_crab_submit = "crab submit -c crab_cfg_skimTree.py"
    os.system(cmd_crab_submit)  
 
    #cmd_crab_kill = "crab kill -d crab_"+RequestName[i]
    #os.system(cmd_crab_kill)

    #cmd_rm_dir = "rm -rf crab_"+RequestName[i]
    #os.system(cmd_rm_dir)


    print "DONE -----",RequestName,"--------------------------------------------------------------------------------------------"
    #time.sleep(10) """
