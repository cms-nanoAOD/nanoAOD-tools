#!/bin/bash

set -e
DIR=""
#1 data; 2 mc-short; 3 mc-long; 4 testdata; 5 testmc
#MODE=3
samplelist=("2016_Data_VH" "2016_MC_VH_short" "2016_MC_VH_long")
queuelist=("local-cms-long" "local-cms-short" "local-cms-long")
prodfolder=("14-Data2016_VH_long" "14-MC_VH_short" "14-MC_VH_long")

#samplelist=("testMC" "testData")
#queuelist=("local-cms-short" "local-cms-short")
#prodfolder=("00-testMC" "00-testData")

#samplelist=("testData")
#queuelist=("local-cms-short")
#prodfolder=("00-testData")

len=${#samplelist[@]}

for ((i=0;i<$len;i++)); do
    echo -e  "${samplelist[$i]} submitting to ${queuelist[$i]}" 
    python scripts/submitLSFjobs.py \
	--queue ${queuelist[$i]} \
	--cfg producer.py \
	--preselection "( (Muon_pt[0]>5 && Muon_mediumId[0]>0 ) || (Electron_pt[0]>15 && Electron_cutBased[0]>0 && Muon_pt[0]>5 && Muon_mediumId[0]>0 ) )" \
	--Nevent -1 \
	--samplelists ${samplelist[$i]} \
	--out Prod_v${prodfolder[$i]}
    echo -e "Prod_v${prodfolder[$i]} created."
done
