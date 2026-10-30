import fileinput, string, sys, os, time, datetime,subprocess
sys.path.insert(0,'/home/mikumar/t3store3/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/tree')
import argparse as arg
sys.path.append('../tree')
parser = arg.ArgumentParser(description='inputs discription')
parser.add_argument('-y', '--year', dest='inputs', type=str, nargs=1, help="Year [ UL2016preVFP , UL2016postVFP , UL2017 , UL2018 ]")
parser.add_argument('-data',"--ISDATA", action="store_true", help="enbale this feature to run on data")
parser.add_argument('-local',"--ISlocal", action="store_true", help="enbale this featrure to count files locally")
args = parser.parse_args()

if args.inputs == None:
        print("USAGE: %s [-h] [-y <Data year>]"%(sys.argv [0]))
        sys.exit (1)

if args.inputs[0] not in [ 'UL2016preVFP' , 'UL2016postVFP' , 'UL2017' , 'UL2018']:
    print('Error: Incorrect choice of year, use -h for help')
    exit()

print("year = ",args.inputs[0])
year   = args.inputs[0]
date   = datetime.datetime.now()

import ROOT as R
R.gInterpreter.ProcessLine('#include "LHEWeightSign.C"')

if(year == 'UL2016preVFP'):
    from dataset_UL2016preVFP import *
    Datasets = Datasets_MC_UL2016APV
if(year == 'UL2016postVFP'):
    from dataset_UL2016postVFP import *
    Datasets = Datasets_MC_UL2016

if(year == 'UL2017'):
    from dataset_UL2017 import *
    Datasets = dict(Datasets_MC_UL2017, **Datasets_sys_MC_UL2017)
if(year == 'UL2018'):
    from dataset_UL2018 import *
    Datasets = dict(Datasets_MC_UL2018, **Datasets_sys_MC_UL2018)

MC_Data = "data" if args.ISDATA else "mc"

if(MC_Data=="mc"):
    Channels_commom = ['Tchannel','Tbarchannel','tw_antitop', 'tw_top','Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic','WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'WWTo2L2Nu', 'WWTolnulnu', 'WZTo2Q2L', 'ZZTo2Q2L','DYJetsToLL'] 

    Channel_QCD_mu = ['QCD_Pt-15To20_MuEnriched', 'QCD_Pt-20To30_MuEnriched', 'QCD_Pt-30To50_MuEnriched', 'QCD_Pt-50To80_MuEnriched', 'QCD_Pt-80To120_MuEnriched', 'QCD_Pt-120To170_MuEnriched', 'QCD_Pt-170To300_MuEnriched', 'QCD_Pt-300To470_MuEnriched', 'QCD_Pt-470To600_MuEnriched', 'QCD_Pt-600To800_MuEnriched', 'QCD_Pt-800To1000_MuEnriched', 'QCD_Pt-1000_MuEnriched']

    Channel_QCD_el = ['QCD_Pt-15to20_EMEnriched', 'QCD_Pt-20to30_EMEnriched', 'QCD_Pt-30to50_EMEnriched', 'QCD_Pt-50to80_EMEnriched', 'QCD_Pt-80to120_EMEnriched', 'QCD_Pt-120to170_EMEnriched' , 'QCD_Pt-170to300_EMEnriched', 'QCD_Pt-300toInf_EMEnriched' ]

    Channel_sys = ['Tchannel_QCDinspired', 'Tchannel_Gluonmove', 'Tchannel_TuneCP5up', 'Tchannel_TuneCP5down', 'Tchannel_erdON', 'Tbachannel_QCDinspired', 'Tbachannel_Gluonmove', 'Tbachannel_TuneCP5up', 'Tbachannel_TuneCP5down', 'Tbarchannel_erdON', 'ttbar_FullyLeptonic_QCDinspired', 'ttbar_FullyLeptonic_Gluonmove', 'ttbar_FullyLeptonic_erdON', 'ttbar_FullyLeptonic_TuneCPup', 'ttbar_FullyLeptonic_TuneCPdown', 'ttbar_SemiLeptonic_QCDinspired', 'ttbar_SemiLeptonic_Gluonmove', 'ttbar_SemiLeptonic_erdON', 'ttbar_SemiLeptonic_TuneCP5up', 'ttbar_SemiLeptonic_TuneCP5down',]

    Channels = Channels_commom + Channel_QCD_mu + Channel_QCD_el +Channel_sys 

elif(MC_Data=="data"):
        if(year=='UL2016preVFP'): Channels = [ 'Run2016B_ver1_'+Lep, 'Run2016B_ver2_'+Lep, 'Run2016C_HIPM_'+Lep, 'Run2016D_HIPM_'+Lep, 'Run2016E_HIPM_'+Lep, 'Run2016F_HIPM_'+Lep]
        if(year=='UL2016postVFP'): Channels = [ 'Run2016F_'+Lep, 'Run2016G_'+Lep, 'Run2016H_'+Lep]
        if(year=='UL2017'): Channels = [ 'Run2017B_'+Lep, 'Run2017C_'+Lep, 'Run2017D_'+Lep, 'Run2017E_'+Lep, 'Run2017F_'+Lep]
        if(year=='UL2018'): Channels = [ 'Run2018A_'+Lep,'Run2018B_'+Lep, 'Run2018C_'+Lep, 'Run2018D_'+Lep] 

#Channels = ['tw_top']
print(Channels)
print("len(Datasets) = ",len(Datasets))
    
#proceed=True
for i in range(0,len(Channels)):
    RequestName = Channels[i]
    print("\n-------     ", RequestName ,"      --------------")
    if(not args.ISlocal):
        if(RequestName in Datasets):
            Dataset = Datasets[RequestName]
        else:
            print( "RequestName '"+RequestName+"'does not find in the dataset")
            continue
        cmd_count = 'dasgoclient --query="file, dataset='+Dataset+'" | wc -l'
        #print cmd_count
        os.system(cmd_count)
        p = subprocess.Popen(cmd_count, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        #p_status = p.wait()

        #print output 

    else:
            year_folder = {'UL2016preVFP': 'SIXTEEN_preVFP', 'UL2016postVFP': 'SIXTEEN_postVFP', 'UL2017': 'SEVENTEEN', 'UL2018': 'EIGHTEEN'}
            cmd_command = 'ls /nfs/home/common/RUN2_UL/Tree_crab/'+year_folder[year]+'/**/'+RequestName+'/**/**/**/**/*.root | wc -l'
            os.system(cmd_command)
