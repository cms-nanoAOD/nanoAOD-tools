#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

import MinitreeModule as minitree
import cut_strings  as cs
import hdamp_ttbar_variation_module as hdamp
import btv_readfromJson as btv
import gen_info_module as genInfo
import dummy_module as dummy
import jme as JME
import argparse
from jetVetoMapProducer import jetVetoMapProducer 

#python3 crab_script_Minitree_local.py  -d Schannel -t 2J1T1_el_mc_UL2016postVFP -o /nfs/home/common/RUN2_UL/Minitree_trial/SIXTEEN_postVFP/2J1T1/el/Schannel/ -n 1 -p /nfs/home/common/RUN2_UL/Tree_crab/SIXTEEN_postVFP/MC/Schannel/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/Tree_04_Jul23_MCUL2016postVFP_Schannel/230704_145222/0000/tree_1.root   &> /nfs/home/common/RUN2_UL/Minitree_trial/SIXTEEN_postVFP/2J1T1/el/Schannel/log/log_1.txt

import uproot

def check_and_rerun(root_file_path, splitting=2, threshold=500000):
    """
    Check the number of events in a ROOT file and return event split indices
    if event count exceeds threshold.
    
    Parameters:
        root_file_path (str): Path to the ROOT file.
        splitting (int): Number of chunks to split the events into. Default is 2.
        threshold (int): Minimum number of events to trigger splitting. Default is 50000.
        
    Returns:
        list: List of event split indices [0, idx1, idx2, ..., total_events]
    """
    with uproot.open(root_file_path) as file:
        try:
            tree = file["Events"]  # Adjust to your actual TTree name
            event_ids = tree["event"].array(library="np")
        except KeyError as e:
            print(f"Missing key in ROOT file: {e}")
            return []

        total_events = len(event_ids)
        print("Total number of events:", total_events)

        if total_events <= threshold:
            print("Event count is within threshold. No splitting needed.")
            return [0, total_events]

        # Split into approximately equal chunks
        step = total_events // splitting
        splits = [i * step for i in range(splitting)]
        if splits[-1] != total_events:
            splits.append(total_events)

        print(f"Splitting into {splitting} chunks: {splits}")
        return splits


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-p', '--path', dest='path',  nargs='+',type=str, default='', help="Path to input file")
parser.add_argument('-d', '--dataset', dest='dataset', type=str, default='', help="Dataset")
parser.add_argument('-t', '--tag', dest='tag', type=str, default='', help="year and mode tag")
parser.add_argument('-o', '--out', dest='out_dir', type=str, default='', help="output_dir")
parser.add_argument('-n', '--lognum', dest='lognum', type=str, default='', help="log txt file number")
parser.add_argument('-data',"--ISDATA", action="store_true", help="enbale this feature to run on data")

args = parser.parse_args()
print('--------------------')
print(args)


region = args.tag.split('_')[0]
lep = args.tag.split('_')[1]
year = args.tag.split('_')[3]

dataset = args.dataset
inputFiles = args.path
#num = inputFiles[0].split('/')[-1].split('.')[0].split('_')[-1]
file_str=""
for File in inputFiles: file_str +=File+" "


if(args.ISDATA): print("\n python3 crab_script_Minitree_local.py  -d "+dataset+" -t "+args.tag +" -o "+args.out_dir+ " -n "+ args.lognum +" -p "+ file_str +" -data  &> "+args.out_dir+"log/log_"+args.lognum+".txt\n")
else: print("\n python3 crab_script_Minitree_local.py  -d "+dataset+" -t "+args.tag +" -o "+args.out_dir+ " -n "+ args.lognum +" -p "+ file_str + "  &> "+args.out_dir+"log/log_"+args.lognum+".txt\n")
if(('2016preVFP' in year) and args.ISDATA):
		poststing = '_'+dataset.split("_")[1] # required to define the module of jme correction for data
else:
	poststing = ""


split_jobs_perfile = 2 
Events_split = check_and_rerun(inputFiles[0],splitting=split_jobs_perfile) 
print(f'{Events_split = }')

for evts in range(len(Events_split[:-1])):

    #Minitree_module = getattr(mt , 'MinitreeModuleConstr' + args.tag)
    treecut = getattr(cs, 'cut_' + region + '_' + lep + '_' + year)  #+ " && Entry$<500" #+ " && event>=182500 && event <= 182721 " + " && Entry$<500"
    btvmodule = getattr(btv,'btagSF'+year)
    jmeCorrection = getattr(JME,'jmeCorrections'+year+'_MC_AK4CHS')
    hdampmodule = getattr(hdamp,'hdamp_vari_mainModule')
    geninfomodule =  getattr(genInfo,'gen_info_Module')
    
    Met_filter_UL16 = " && (Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_BadPFMuonDzFilter && Flag_eeBadScFilter)==1"
    Met_filter_UL17_UL18 = " && (Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_BadPFMuonDzFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter)==1"
    if(year in ["UL2017", "UL2018"]): treecut = treecut+Met_filter_UL17_UL18	
    elif(year in ["UL2016preVFP", "UL2016postVFP"]): treecut = treecut+Met_filter_UL16
    
    if(args.ISDATA):
    	minitreemodule = getattr(minitree,'MinitreeModuleConstr'+region+'_'+lep+'_data_'+year)
    	jmeCorrection = getattr(JME, "jmeCorrectionsUL"+dataset.split('_')[0]+poststing+"_DATA_AK4CHS")
    else:
    	minitreemodule = getattr(minitree,'MinitreeModuleConstr'+region+'_'+lep+'_mc_'+year)
    	jmeCorrection = getattr(JME,'jmeCorrections'+year+'_MC_AK4CHS')
    
    if( (dataset in ['ttbar_SemiLeptonic','ttbar_FullyLeptonic']) and region == "2J1T1"):
    	runmodules = [btvmodule(),minitreemodule(dataset),jmeCorrection(),hdampmodule(),geninfomodule()]
    elif((dataset in ['Tchannel' , 'Tbarchannel','tw_top', 'tw_antitop', 'Schannel']) and region == "2J1T1"):
    	runmodules = [btvmodule(),minitreemodule(dataset),jmeCorrection(),geninfomodule()]
    elif('Run' in dataset):
    	runmodules =[minitreemodule(),jmeCorrection()]
    elif(('QCDinspired' in dataset) or ('Gluonmove' in dataset) or ('TuneCP5' in dataset) or ('TuneCP5down' in dataset) or ('erdON' in dataset)):
    	runmodules = [btvmodule(),minitreemodule(dataset)]
    else:
    	runmodules = [btvmodule(),minitreemodule(dataset),jmeCorrection()]
    
    print('\n year : ',year)
    print('\n treecut : ',treecut)
    print('\n inputFiles : ',inputFiles)
    #@print('file number : ',num)
    print('\n modules imported : ','btagSF'+year,'MinitreeModuleConstr'+region+'_'+lep+'_mc_'+year,'MinitreeModuleConstr'+region+'_'+lep+'_data_'+year,'jmeCorrections'+year+'_MC_AK4CHS'," jmeCorrectionsUL"+dataset.split('_')[0]+poststing+"_DATA_AK4CHS",'hdamp_vari_mainModule')
    print('\n modules run : ',runmodules)

    print('--------------------')

    print(f'\n{Events_split[evts]}:{Events_split[evts+1]}')
    #treecut = treecut+f" && Entry$>={Events_split[evts]} && Entry$<{Events_split[evts+1]}"
    entry_cut = f"Entry$>={Events_split[evts]} && Entry$<{Events_split[evts+1]}"
    postfix = f"_{Events_split[evts]}_{Events_split[evts+1]}"
    print('\n treecut : ',treecut)
    print('\n entry range : ',entry_cut)
    print('\n postfix : ',postfix)

    jvm_dir = os.path.join(args.out_dir, "jvm_tmp_" + args.lognum)
    p_jvm = PostProcessor(jvm_dir, inputFiles, entry_cut, postfix="", modules=[jetVetoMapProducer(year)], compression="LZ4:1", provenance=False, fwkJobReport=False, jsonInput=runsAndLumis())
    p_jvm.run()
    jvmFiles = [os.path.join(jvm_dir, os.path.basename(f)) for f in inputFiles]
    print('\n jet-veto-map files (pass 1 output) : ', jvmFiles)

    p=PostProcessor(args.out_dir,
    	jvmFiles,
		treecut,
        postfix = postfix,
		modules=runmodules,
        outputbranchsel="keep_and_drop_"+lep+"_Minitree.txt",
		provenance=True,
		fwkJobReport=False,
		jsonInput=runsAndLumis())
    p.run()

    for f in jvmFiles:
        if os.path.exists(f): os.remove(f)
    if os.path.isdir(jvm_dir) and not os.listdir(jvm_dir): os.rmdir(jvm_dir)
print("DONE")
