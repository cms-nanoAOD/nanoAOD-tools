#!/bin/bash

outDir="."
#fileIn="/Users/shoh/Projects/CMS/PhD/Analysis/SSL/NANOAOD/HWminusJ_HToWW_M125_13TeV_powheg_pythia8-v1.root"
fileIn="/Users/shoh/Projects/CMS/PhD/Analysis/SSL/NANOAOD/DYJetsToLL_Pt-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext2-v1.root"
#fileIn="/Users/shoh/Projects/CMS/PhD/Analysis/SSL/NANOAOD/VHToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8.root"

#preselection=""
branches="scripts/keep_and_drop_VH.txt"
bIn="scripts/keep_and_drop_Input.txt"
bOut="scripts/keep_and_drop_Output.txt"
#module="PhysicsTools.NanoAODTools.postprocessing.modules.analysis.exampleModule exampleModuleConstr"
#module2="PhysicsTools.NanoAODTools.postprocessing.modules.analysis.exampleModule exampleModuleConstr"
module="PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer puWeight"
#module="PhysicsTools.NanoAODTools.analysis.Producer_pf producer"
#maxevent="2000"
maxevent=$1

if [ -z "$maxevent" ]
then
    echo "No argument maxevent supplied"
    echo "Example : ./producer.sh maxevent"
    exit
else
    python scripts/nano_postproc.py $outDir $fileIn -I $module -E ${maxevent} --bi ${bIn} --bo ${bOut}  #-b ${branches} #--bi ${bIn} --bo ${bOut}
fi
