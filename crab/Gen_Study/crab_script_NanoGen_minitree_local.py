#!/usr/bin/env python
import os
import argparse

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from Gen_mass_reconstract_SingleTop_minitree import *

#python3 crab_script_minitree_local.py -o /nfs/home/common/RUN2_UL/Minitree_trial/SIXTEEN_postVFP/2J1T1/el/Schannel/ -n 1 -p /nfs/home/common/RUN2_UL/Tree_crab/SIXTEEN_postVFP/MC/Schannel/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/Tree_04_Jul23_MCUL2016postVFP_Schannel/230704_145222/0000/tree_1.root   &> /nfs/home/common/RUN2_UL/Minitree_trial/SIXTEEN_postVFP/2J1T1/el/Schannel/log/log_1.txt

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-p', '--path', dest='path',  nargs='+',type=str, default='', help="Path to input file")
parser.add_argument('-o', '--out', dest='out_dir', type=str, default='', help="output_dir")
parser.add_argument('-n', '--lognum', dest='lognum', type=str, default='', help="log txt file number")

args = parser.parse_args()
print('--------------------')
print(args)



inputFiles = args.path
#num = inputFiles[0].split('/')[-1].split('.')[0].split('_')[-1]
file_str=""
for File in inputFiles: file_str +=File+" "


print("\n python3 crab_script_minitree_local.py   -o "+args.out_dir+ " -n "+ args.lognum +" -p "+ file_str + "  &> "+args.out_dir+"log/log_"+args.lognum+".txt\n")
poststing = ""



#Minitree_module = getattr(mt , 'MinitreeModuleConstr' + args.tag)
treecut = "top_mass_gen>=0 && top_mass_gen_reco>=0" #" && event>=182500 && event <= 182721 " + " && Entry$<500"
b_jet_reco_cut = " && (bpart_pt_gen/bjet_pt_gen) >0.5"

treecut = treecut+b_jet_reco_cut
runmodules = [NanoGenConstr_UL2016_minitree()]

print('\n treecut : ',treecut)
print('\n inputFiles : ',inputFiles)
#@print('file number : ',num)
print('\n modules run : ',runmodules)

print('--------------------')


p=PostProcessor(args.out_dir,
    	inputFiles,
		treecut,
		modules=runmodules,
		provenance=True,
		fwkJobReport=False,
		jsonInput=runsAndLumis())
p.run()
print("DONE")
