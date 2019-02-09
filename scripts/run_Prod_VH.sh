#!/bin/bash

set -e
DIR=""
#1 data; 2 mc-short; 3 mc-long; 4 testdata; 5 testmc
#MODE=3
#samplelist=("2016_Data_VH" "2016_MC_VH_short" "2016_MC_VH_long" "2017_Data_VH")
#queuelist=("local-cms-long" "local-cms-short" "local-cms-long" "local-cms-long")
#prodfolder=("14-Data2016_VH_long" "14-MC_VH_short" "14-MC_VH_long" "14-Data2017_VH_long")
samplelist=("test")
queuelist=("local-cms-short")
prodfolder=("test-short")

#samplelist=("2016_Data_VH_reprocess" "2016_MC_VH_short_reprocess" "2016_MC_VH_long_reprocess") 
#queuelist=("local-cms-long" "local-cms-short" "local-cms-long")
#prodfolder=("09-Data_VH_long_reprocess" "09-MC_VH_short_reprocess" "09-MC_VH_long_reprocess")

#samplelist=("2017_Data_VH_reprocess")
#queuelist=("local-cms-short")
#prodfolder=("09-Data2017_VH_long_reprocess")

#PreSelection="Muon_pt[0]>17 && Muon_pt[1]>8 && Muon_mediumId[0]>0 && Muon_pfRelIso03_all[0]<0.15 && Electron_pt[0]>20 && Electron_cutBased[0]>2 && Electron_pfRelIso03_all[0]<0.1"

#PreSelection="Jet_pt>30 && Jet_jetId>0 && Jet_puId>4 && fabs(Jet_eta)<2.5 "
#PreSelection="Muon_mediumId>0 && Electron_cutBased>0"

#( ( Muon_pt[0]>25 && Muon_pt[1]>8 && Muon_pfRelIso03_all[0]<0.15 ) || ( Electron_pt[0]>20 && Muon_pt[0]>20 && Electron_cutBased[0]>2 && Electron_pfRelIso03_all[0]<0.1 && Muon_pfRelIso03_all[0]<0.15 ) )

len=${#samplelist[@]}

for ((i=0;i<$len;i++)); do
    echo -e  "${samplelist[$i]} submitting to ${queuelist[$i]}" 
    python scripts/submitLSFjobs.py \
	--queue ${queuelist[$i]} \
	--cfg producer.py \
	--preselection "( (Muon_pt[0]>5 && Muon_mediumId[0]>0 && Muon_pfRelIso03_all[0]<0.15 ) || (Electron_pt[0]>15 && Electron_cutBased[0]>0 && Electron_pfRelIso03_all[0]<0.15 && Muon_pt[0]>5 && Muon_mediumId[0]>0 ) )" \
	--samplelists ${samplelist[$i]} \
	--out Prod_v${prodfolder[$i]}
    echo -e "Prod_v${prodfolder[$i]} created."
done
