#!/bin/bash

set -e
DIR=""

samplelist=("samplelist_shortQ" "samplelist_longQ")
queuelist=("local-cms-short" "local-cms-long")
prodfolder=("skim-shortQ" "skim-longQ")

len=${#samplelist[@]}

for ((i=0;i<$len;i++)); do
    echo -e  "${samplelist[$i]} submitting to ${queuelist[$i]}" 
    python scripts/submitLSFjobs.py \
	--queue ${queuelist[$i]} \
	--cfg skim.py \
	--preselection "( (Muon_pt[0]>5 && Muon_mediumId[0]>0) || (Electron_pt[0]>15 && Electron_cutBased[0]>0) ) || ( (Muon_pt[0]>5 && Muon_mediumId[0]>0) && (Electron_pt[0]>15 && Electron_cutBased[0]>0) )" \
	--Nevent -1 \
	--samplelists ${samplelist[$i]} \
	--out Prod_v${prodfolder[$i]}
    echo -e "Prod_v${prodfolder[$i]} created."
done
