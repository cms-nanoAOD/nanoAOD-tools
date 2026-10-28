import fileinput, string, sys, os, time, subprocess
import argparse as arg

parser = arg.ArgumentParser(description='inputs discription')  
parser.add_argument('-d', '--dir', dest='CondorDir', type=str, nargs=1, help="condor directory")
parser.add_argument('-s', '--sample', dest='samples', type=str, nargs=1, help="sample [ Mc , Data ]")
parser.add_argument('-y', '--year', dest='years', type=str, nargs=1, help="Year [ UL2016preVFP , UL2016postVFP , UL2017 , UL2018 ]")
parser.add_argument('-l', '--lepton', dest='leptons', type=str, nargs=1, help="sample [ mu , el ]")

args = parser.parse_args()
import ROOT as rt

if args.CondorDir == None:
	print "USAGE: %s [-h] [-d <condor directory>]"%(sys.argv [0])
        sys.exit (1) 
if args.years[0] not in ['UL2016preVFP', 'UL2016postVFP','UL2017','UL2018']:
    print('Error: Incorrect choice of year, use -h for help')
    sys.exit(1)
if args.leptons[0] not in ['mu','el']:
    print('Error: Incorrect choice of lepton type, use -h for help')
    sys.exit(1)

CondorDir=args.CondorDir[0]
if not (os.path.isdir(CondorDir)):
	print "Dir", " '",CondorDir,"' "," does not exist" 
	sys.exit (1)


def get_dirs(rootdir):
    Dirs=[]
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            #print(d)
	    Dirs.append(d)
            #listdirs(d)
    return Dirs

def find_files(search_path):
   result = []
   # Wlaking top-down from the root
   for root, dir, files in os.walk(search_path):
   	for filename in files:
	    if filename.endswith('_phy3.py'):
		#print root+'/'+str(filename)
         	result.append(root+'/'+str(filename))
		if(len(result)==1): break
	    if(len(result)==1): break
   return result

datasets_file=find_files(CondorDir)
datasets_file=datasets_file[0]
print datasets_file
print str(datasets_file.rsplit(".")[0])
sys.path.insert(0,str(datasets_file.rsplit(".")[0].rsplit("/",1)[0]))
#datasetspy=__import__(str(datasets_file.rsplit(".")[0].rsplit("/",1)[1]))

lep = args.leptons[0]
year   = args.years[0]
sample = args.samples[0]

if(year == 'UL2016preVFP'):
    from dataset_UL2016preVFP_phy3 import *
    if sample=="Mc" : Datasets = Datasets_MC_UL2016APV
    elif sample=="Data" and lep=="mu" : Datasets = Datasets_SingleMuon_data_UL2016APV
    elif sample=="Data" and lep=="el" : Datasets = Datasets = Datasets_SingleElectron_data_UL2016APV
if(year == 'UL2016postVFP'):
    from dataset_UL2016postVFP_phy3 import *
    if sample=="Mc" : Datasets = Datasets_MC_UL2016
    elif sample=="Data" and lep=="mu" : Datasets = Datasets_SingleMuon_data_UL2016
    elif sample=="Data" and lep=="el" : Datasets = Datasets_SingleElectron_data_UL2016
if(year == 'UL2017'):
    from dataset_UL2017_phy3 import *
    if sample=="Mc" : Datasets = Datasets_MC_UL2017
    elif sample=="Data" and lep=="mu" : Datasets = Datasets_SingleMuon_data_UL2017
    elif sample=="Data" and lep=="el" : Datasets = Datasets_SingleElectron_data_UL2017


channels=['Tchannel']
#channels=Datasets.keys()
print channels
print 
print "-----------------------------------------    chacking     --------------------------------"
print
cwd = os.getcwd()
for channel in channels:
    if((lep=="el" and "MuEnriched" in channel) or (lep=="mu" and "EMEnriched" in channel)):
        continue
    if not (os.path.isdir(CondorDir+"/"+channel)):
        print
        proceed = raw_input(CondorDir+"/"+channel +"  does not exist; you can skip this press 1/Yes and press other key to exit : ")
        if(proceed=="1" or proceed=="yes"): continue
        else: exit()
    Dirs=get_dirs(CondorDir+"/"+channel)
    i=0
    treeEntries=0
    cutflowEntries=0
    for Dir in Dirs:
        i=i+1
        print "================",i,"=============="
        cmd_grep = 'grep "inputFiles" '+Dir+'/condor_script_cutflow.py'
        print Dir+'/condor_script_cutflow.py'       
        p = subprocess.Popen(cmd_grep, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()

        if(output.count("inputFiles")>0): 
            file = output.rsplit("'")[1]
            print file

            InFile = rt.TFile.Open(file,"READ")
            Tree = InFile.Get("Events")
            cut_2J1T1_el_UL2016postVFP = "HLT_Ele32_eta2p1_WPTight_Gsf==1 && (Sum$(Electron_pt>35 && abs(Electron_eta)<2.1 && Electron_cutBased==4 && (abs(Electron_EtaSC)<1.4442 || abs(Electron_EtaSC)>1.5660) && ((abs(Electron_EtaSC)<=1.479 && abs(Electron_dz)< 0.10 && abs(Electron_dxy)< 0.05) || (abs(Electron_EtaSC)> 1.479 && abs(Electron_dz)< 0.20 && abs(Electron_dxy)< 0.10)))==1) && (Sum$(Electron_cutBased>=1 && Electron_pt>15 && abs(Electron_eta)<2.5 && ((abs(Electron_EtaSC)<=1.479 && abs(Electron_dz)< 0.10 && abs(Electron_dxy)< 0.05) || (abs(Electron_EtaSC)> 1.479 && abs(Electron_dz)< 0.20 && abs(Electron_dxy)< 0.10)))==1) && (Sum$(Muon_looseId==1 && Muon_pt>10 && abs(Muon_eta)<2.4 && Muon_pfRelIso04_all<0.2)==0) && (Sum$(Jet_pt>40 && abs(Jet_eta)<4.7 && Jet_jetId!=0 && (Jet_pt>=50 || (Jet_puId & 4)!=0) && Jet_dR_Ljet_Isoel>0.4)==2) && (Sum$(Jet_pt>40 && Jet_jetId!=0 && (Jet_pt>=50 || (Jet_puId & 4)!=0) && abs(Jet_eta)<2.4 && Jet_dR_Ljet_Isoel>0.4 && Jet_btagDeepFlavB>0.6377)==1)"
            cut_2J1T1_el_UL2016preVFP = "HLT_Ele32_eta2p1_WPTight_Gsf==1 && (Sum$(Electron_pt>35 && abs(Electron_eta)<2.1 && Electron_cutBased==4 && (abs(Electron_EtaSC)<1.4442 || abs(Electron_EtaSC)>1.5660) && ((abs(Electron_EtaSC)<=1.479 && abs(Electron_dz)< 0.10 && abs(Electron_dxy)< 0.05) || (abs(Electron_EtaSC)> 1.479 && abs(Electron_dz)< 0.20 && abs(Electron_dxy)< 0.10)))==1) && (Sum$(Electron_cutBased>=1 && Electron_pt>15 && abs(Electron_eta)<2.5 && ((abs(Electron_EtaSC)<=1.479 && abs(Electron_dz)< 0.10 && abs(Electron_dxy)< 0.05) || (abs(Electron_EtaSC)> 1.479 && abs(Electron_dz)< 0.20 && abs(Electron_dxy)< 0.10)))==1) && (Sum$(Muon_looseId==1 && Muon_pt>10 && abs(Muon_eta)<2.4 && Muon_pfRelIso04_all<0.2)==0) && (Sum$(Jet_pt>40 && abs(Jet_eta)<4.7 && Jet_jetId!=0 && (Jet_pt>=50 || (Jet_puId & 4)!=0) && Jet_dR_Ljet_Isoel>0.4)==2) && (Sum$(Jet_pt>40 && Jet_jetId!=0 && (Jet_pt>=50 || (Jet_puId & 4)!=0) && abs(Jet_eta)<2.4 && Jet_dR_Ljet_Isoel>0.4 && Jet_btagDeepFlavB>0.6502)==1)"

            cut = cut_2J1T1_el_UL2016postVFP
            TEntry = Tree.GetEntries(cut)
            print  TEntry
            treeEntries=treeEntries+TEntry

        cmd_grep = 'grep "Arguments" '+Dir+'/condorSetup.sub'
        p = subprocess.Popen(cmd_grep, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
        #print Dir+'/condorSetup.sub'
        if(output.count("Arguments")>0):
            file = output.rsplit(" ")[-5]
            print file
            cmd_analise_cutflow = "python Analize_Cutflow_histogram.py -f "+file
            os.system(cmd_analise_cutflow)
        print
        print "treeEntries : ",treeEntries
            

