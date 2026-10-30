#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from jme import *

from MinitreeModule import *
from cut_strings import *
from hdamp_variation_module import *
from btv_readfromJson import *
from jetVetoMapProducer import *

treecut = cut_2J1T1_mu_UL2017 #+ "&& Entry$<100"
#inputFiles=["root://se01.indiacms.res.in//store/user/mikumar/RUN2_UL/Tree_crab/SIXTEEN/MC_preVFP_v2/Tbarchannel/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/Tree_06_Aug22_MCUL2016preVFP_Tbarchannel/220806_112911/0000/tree_14.root"]
#inputFiles=["root://se01.indiacms.res.in//store/user/mikumar/RUN2_UL/Tree_crab/SIXTEEN/Data_preVFP_mu/Run2016D-HIPM_mu/SingleMuon/Tree_04_Jun22_Run2016D-HIPM_mu/220604_165834/0000/tree_1.root"]
inputFiles=['/nfs/home/common/RUN2_UL/Tree_crab/SEVENTEEN/MC/ttbar_FullyLeptonic/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/Tree_13_May23_MCUL2017_ttbar_FullyLeptonic/230513_180158/0000/tree_1.root']

jvm_dir = "jvm_tmp"
jvm_inputs = inputFiles() if callable(inputFiles) else inputFiles   # CRAB gives a function, condor/local give a list
p_jvm = PostProcessor(jvm_dir, jvm_inputs, None, postfix="", modules=[jvmModule], compression="LZ4:1", provenance=False, fwkJobReport=False, jsonInput=runsAndLumis())
p_jvm.run()
jvmFiles = [os.path.join(jvm_dir, os.path.basename(f)) for f in jvm_inputs]
print("jet-veto-map files (pass 1 output) : %s" % jvmFiles)

p=PostProcessor(".",
		jvmFiles,
		treecut,
		modules=[btagSFUL2017(),MinitreeModuleConstr2J1T1_mu_mc_UL2016preVFP(), jmeCorrectionsULRun2016C_preVFP_DATA_AK4CHS()],#hdamp_vari_mainModule()],
		outputbranchsel="keep_and_drop_mu_Minitree.txt",
		provenance=True,
		#fwkJobReport=True,
		jsonInput=runsAndLumis())
		
p.run()

for f in jvmFiles:
    if os.path.exists(f): os.remove(f)

print("DONE")
