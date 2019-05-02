#!/bin/bash

outDir="."

##Signal

#fileIn="/lustre/cmswork/hoh/NANO/SSLep/data/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v2.root"
fileIn="/lustre/cmswork/hoh/NANO/SSLep/data/SingleElectronRun2016B-03Feb2017_ver2-v2.root"

#preselection=""
branches="scripts/keep_and_drop_VH.txt"
bIn="scripts/keep_and_drop_Input.txt"
bOut="scripts/keep_and_drop_Output.txt"
#module="PhysicsTools.NanoAODTools.postprocessing.modules.analysis.exampleModule exampleModuleConstr"
#module2="PhysicsTools.NanoAODTools.postprocessing.modules.analysis.exampleModule exampleModuleConstr"
#module="PhysicsTools.NanoAODTools.analysis.Producer producer"
module="PhysicsTools.NanoAODTools.postprocessing.modules.common.lepSFProducer lepSF"

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
