#!/usr/bin/env python
import os,sys
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
sys.path.insert(0, '../minitree/')
import cut_strings  as cs
import btv_readfromJson as btv

import cutflowModule as cf

import argparse

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


if(args.ISDATA): print("\n python3 crab_script_cutflow_local.py  -d "+dataset+" -t "+args.tag +" -o "+args.out_dir+ " -n "+ args.lognum +" -p "+ file_str +" -data  &> "+args.out_dir+"log/log_"+args.lognum+".txt\n")
else: print("\n python3 crab_script_cutflow_local.py  -d "+dataset+" -t "+args.tag +" -o "+args.out_dir+ " -n "+ args.lognum +" -p "+ file_str + "  &> "+args.out_dir+"log/log_"+args.lognum+".txt\n")
if(year in ['UL2016_preVFP','UL2016_postVFP']):
	poststing = "_"+year.split("_")[-1] # required to define the module of jme correction for data
else:
	poststing = ""



#Minitree_module = getattr(mt , 'MinitreeModuleConstr' + args.tag)
treecut = ""#event==118517315"#nGenJet>0" #Entry$<500" nGenDressedLepton>0
btvmodule = getattr(btv,'btagSF'+year)

if(args.ISDATA):
	cutflowmodule = getattr(cf,'cutflowModuleConstr_'+region+'_'+lep+'_data_'+year)
	runmodules = [cutflowmodule()]
else:
	cutflowmodule = getattr(cf,'cutflowModuleConstr_'+region+'_'+lep+'_mc_'+year)
	runmodules = [btvmodule(), cutflowmodule(dataset)] #btvmodule(),




print('\n treecut : ',treecut)
print('\n inputFiles : ',inputFiles)
#@print('file number : ',num)
print('\n modules imported : ','btagSF'+year,'cutflowModuleConstr_'+region+'_'+lep+'_mc_'+year)
print('\n modules run : ',runmodules)

print('--------------------')
print(type(runmodules))
#inputFiles = ['/nfs/home/common/RUN2_UL/Tree_crab/SEVENTEEN/MC/ttbar_FullyLeptonic/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/Tree_13_May23_MCUL2017_ttbar_FullyLeptonic/230513_180158/0000/tree_10.root']
p=PostProcessor(
	args.out_dir,
	inputFiles,
	treecut,   #in cutflow there should not be any cut
	modules=runmodules,
	outputbranchsel="clean.txt",
	provenance=True,
	fwkJobReport=False,
	jsonInput=runsAndLumis(),
	friend=True,
	noOut=False,
	histFileName=args.out_dir+"/Cutflow_hist_"+args.lognum+".root",
	histDirName="histograms")
p.run()
print("Done")
