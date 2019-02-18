#!/bin/bash

DIR="/Users/shoh/Projects/CMS/PhD/Analysis/SSL/NANOAOD/"
nEvent=1000

for file in "HWplusJ_HToWW_M125_13TeV_powheg_pythia8-v1.root" "HWminusJ_HToWW_M125_13TeV_powheg_pythia8-v1.root" "VHToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8.root"
do
    echo "python scripts/producer.py ./ $DIR$file -c \"\" -e $nEvent"
    python scripts/producer.py ./ $DIR$file -c "" -e $nEvent
done
