import fileinput, string, sys, os, time, datetime,subprocess
import argparse as arg
sys.path.append('../tree')
parser = arg.ArgumentParser(description='inputs discription')
parser.add_argument('-y', '--year', dest='inputs', type=str, nargs=1, help="Year [ UL2016preVFP , UL2016postVFP , UL2017 , UL2018, 'Gen_UL2016_width', 'Gen_UL2016_Mass' ]")
args = parser.parse_args()

if args.inputs == None:
        print("USAGE: %s [-h] [-y <Data year>]"%(sys.argv [0]))
        sys.exit (1)

if args.inputs[0] not in [ 'UL2016preVFP' , 'UL2016postVFP' , 'UL2017' , 'UL2018', 'Gen_UL2016_width', 'Gen_UL2016_Mass']:
    print('Error: Incorrect choice of year, use -h for help')
    exit()

print("\nyear = ",args.inputs[0])
year   = args.inputs[0]
date   = datetime.datetime.now()


import ROOT as R
R.gInterpreter.ProcessLine('#include "LHEWeightSign.C"')

if(year == 'UL2016preVFP'):
    from dataset_UL2016preVFP import *
    Datasets = Datasets_sys_MC_UL2016APV
if(year == 'UL2016postVFP'):
    from dataset_UL2016postVFP import *
    Datasets = Datasets_sys_MC_UL2016
if(year == 'UL2017'):
    from dataset_UL2017 import *
    Datasets = Datasets_sys_MC_UL2017
if(year == 'UL2018'):
    from dataset_UL2018 import *
    Datasets = Datasets_Alt_MC_UL2018
if(year == 'Gen_UL2016_width'):
    sys.path.append("../Gen_Study")
    from dataset_UL2016_v2 import *
    Datasets = Datasets_AltWidth_MC_UL2016
if(year == 'Gen_UL2016_Mass'):
    sys.path.append("../Gen_Study")
    from dataset_UL2016_v2 import *
    Datasets = Datasets_AltMass_MC_UL2016

#RequestNames = ["QCD_Pt-15To20_MuEnriched", "QCD_Pt-20To30_MuEnriched", "QCD_Pt-30To50_MuEnriched", "QCD_Pt-50To80_MuEnriched", "QCD_Pt-80To120_MuEnriched", "QCD_Pt-120To170_MuEnriched", "QCD_Pt-170To300_MuEnriched", "QCD_Pt-300To470_MuEnriched", "QCD_Pt-470To600_MuEnriched", "QCD_Pt-600To800_MuEnriched", "QCD_Pt-800To1000_MuEnriched", "QCD_Pt-1000_MuEnriched", "QCD_Pt-15to20_EMEnriched", "QCD_Pt-20to30_EMEnriched", "QCD_Pt-30to50_EMEnriched", "QCD_Pt-50to80_EMEnriched", "QCD_Pt-80to120_EMEnriched", "QCD_Pt-120to170_EMEnriched", "QCD_Pt-170to300_EMEnriched", "QCD_Pt-300toInf_EMEnriched", "Tchannel", "Tbarchannel", "tw_top", "tw_antitop", "Schannel", "ttbar_SemiLeptonic", "ttbar_FullyLeptonic", "WJetsToLNu_0J", "WJetsToLNu_1J", "WJetsToLNu_2J", "DYJets", "WWTolnulnu", "WZTo2Q2L", "ZZTo2Q2L"] 
RequestNames_dataset = Datasets.keys()
#RequestNames = ["ttbar_FullyLeptonic_TuneCP5down"]#["WJetsToLNu_0J_v2","WJetsToLNu_2J"] #["DYJetsToLL"]
print(RequestNames_dataset)
print("len(Datasets) = ",len(Datasets))
    
#proceed=True
for RequestName in RequestNames_dataset:
    #RequestName = RequestNames[i]
    #if("channel" in RequestName): continue
    #print(Datasets.keys())
    if(RequestName in RequestNames_dataset):
    	Dataset = Datasets[RequestName]
    else:
        print( "RequestName '"+RequestName+"'does not find in the dataset")
        print(RequestNames_dataset)
        continue
    print
    #if("ttbar_SemiLeptonic" not in RequestName):continue
    print("---------------------------------------     ", RequestName ,"      ---------------------------------")
    #if(proceed==True):continue
    cmd_count = 'dasgoclient --query="file, dataset='+Dataset+' | sum(file.nevents)"'
    #print cmd_count
    os.system(cmd_count)
    p = subprocess.Popen(cmd_count, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    #p_status = p.wait()

    print(" Number of Events : ", round(float(output[19:])/1000000,2) )

    if(True):#not(RequestName.find("QCD")!=-1)): 
    		cmd_dasgoclint = 'dasgoclient -query="file dataset='+Dataset+'" > filename.txt'
    		#print cmd_dasgoclint
    		os.system(cmd_dasgoclint) 
  
    		R.LHEWeightSign()
	
