#!/bin/bash

set -e
DIR=""
#1 data; 2 mc-short; 3 mc-long; 4 testdata; 5 testmc
#MODE=3
samplelist=("AUX")
queuelist=("local-cms-long")
prodfolder=("AUX")

len=${#samplelist[@]}

for ((i=0;i<$len;i++)); do
    echo -e  "${samplelist[$i]} submitting to ${queuelist[$i]}" 
    python scripts/submitLSFjobs.py \
	--queue ${queuelist[$i]} \
	--cfg producer.py \
	--preselection "( (Muon_pt[0]>5 && Muon_mediumId[0]>0) || (Electron_pt[0]>15 && Electron_cutBased[0]>0) ) || ( (Muon_pt[0]>5 && Muon_mediumId[0]>0) && (Electron_pt[0]>15 &&  Electron_cutBased[0]>0) )" \
	--samplelists ${samplelist[$i]} \
	--out Prod_v${prodfolder[$i]}
    echo -e "Prod_v${prodfolder[$i]} created."
done
