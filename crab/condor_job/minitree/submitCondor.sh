#!/bin/bash
#REFERENCE
#https://github.com/florez/CONDOR

if [ "$#" -ne 4 ]; then                                                                 #check if input parameters are less than 3
  echo "Usage: $0 <year> <sample> <lep> <region>" >&1
  echo "i.e  ./submitCondor_new.sh < UL2016preVFP > < Mc_Nomi / Mc_Alt / Mc_sys / Data > < mu / el > < 2J1T1 / 3J1T >"
  exit 1
fi
if ! [ "$1" ]; then
  echo "$1 not found" >&2
  exit 1
fi

year=$1
sample=$2
lep=$3
region=$4
crab_dir="/home/mikumar/t3store3/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab"

if ! [[ "UL2016preVFP" == "$year" || "UL2016postVFP" == "$year" || "UL2017" == "$year" || "UL2018" == "$year" ]]; then
    echo "wrong choice of year ["UL2016preVFP UL2016postVFP UL2017 UL2018"]"
    exit 1
fi

if ! [[ "Mc_Nomi" == "$sample" || "Mc_Alt" == "$sample" || "Mc_sys" == "$sample" || "Data" == "$sample" ]]; then
    echo "wrong choice of sample ["Mc_Nomi Mc_Alt Mc_sys Data"]"
    exit 1
fi

if ! [[ "mu" == "$lep" || "el" == "$lep" ]]; then
    echo "wrong choice of lepton ["el mu"]"
    exit 1
fi

if ! [[ "2J1T1" == "$region" || "2J1T0" == "$region" || "2J0T1" == "$region" || "2J0T0" == "$region" || "3J1T1" == "$region" || "3J1T0" == "$region" || "3J2T1" == "$region" || "3J2T0" == "$region" || "2J1L0T1" == "$region" || "2J1L0T0" == "$region" ]]; then
    echo "wrong choice of lepton ["2J1T1 2J1T0 2J0T1 2J0T0 3J1T1 3J1T0 3J2T1 3J2T0 2J1L0T1 2J1L0T0 "]"
    exit 1
fi
#------------------------------------------------
#create the same datasetfile depending on year
#------------------------------------------------
Mc_Nomi_channel="Tchannel Tbarchannel tw_top tw_antitop Schannel ttbar_SemiLeptonic ttbar_FullyLeptonic WJetsToLNu_0J WJetsToLNu_1J WJetsToLNu_2J DYJets WWTo2L2Nu WZTo2Q2L ZZTo2Q2L" #Tchannel
Mc_QCD_mu="QCD_Pt-15To20_MuEnriched QCD_Pt-20To30_MuEnriched QCD_Pt-30To50_MuEnriched QCD_Pt-50To80_MuEnriched QCD_Pt-80To120_MuEnriched QCD_Pt-120To170_MuEnriched QCD_Pt-170To300_MuEnriched QCD_Pt-300To470_MuEnriched QCD_Pt-470To600_MuEnriched QCD_Pt-600To800_MuEnriched QCD_Pt-800To1000_MuEnriched QCD_Pt-1000_MuEnriched"
Mc_QCD_el="QCD_Pt-30to50_EMEnriched QCD_Pt-50to80_EMEnriched QCD_Pt-80to120_EMEnriched QCD_Pt-120to170_EMEnriched QCD_Pt-170to300_EMEnriched QCD_Pt-300toInf_EMEnriched"
Mc_Alt_channel="Tbarchannel_mtop1695 ttbar_SemiLeptonic_mtop1695   ttbar_FullyLeptonic_mtop1695   Tbarchannel_mtop1735   ttbar_FullyLeptonic_widthx0p55   ttbar_FullyLeptonic_widthx0p7   ttbar_FullyLeptonic_mtop1735   Tbarchannel_mtop1715   ttbar_FullyLeptonic_widthx1p3   ttbar_FullyLeptonic_mtop1755   ttbar_FullyLeptonic_widthx1p45   ttbar_FullyLeptonic_mtop1715   Tchannel_mtop1715   ttbar_SemiLeptonic_mtop1755   ttbar_SemiLeptonic_mtop1735   ttbar_SemiLeptonic_mtop1715   ttbar_FullyLeptonic_widthx0p85   Tbarchannel_mtop1755   Tchannel_mtop1695   ttbar_FullyLeptonic_widthx1p15   Tchannel_mtop1735   Tchannel_mtop1755"
Mc_sys_channel="Tchannel_TuneCP5CR2  Tchannel_TuneCP5CR1   Tchannel_hdampdown   Tbarchannel_hdampdown   Tchannel_TuneCP5down   Tbarchannel_hdampup   Tchannel_hdampup   Tbarchannel_TuneCP5down   Tchannel_erdON   Tchannel_TuneCP5up   Tbarchannel_TuneCP5up   Tbarchannel_erdON   Tbarchannel_TuneCP5CR1   Tbarchannel_TuneCP5CR2"

if [[ "UL2016preVFP" == "$year" ]]; then
     dataset_file=$crab_dir"/minitree/dataset_UL2016preVFP_phy3.py"
     outputDir="/store/user/mikumar/RUN2_UL/MiniTree_condor/SIXTEEN_preVFP_v5/"

     if [[ $sample == "Mc_Nomi" && $lep == "mu" ]]; then
	channels="${Mc_Nomi_channel} ${Mc_QCD_mu}"
     fi
     if [[ $sample == "Mc_Nomi" && $lep == "el" ]]; then
        channels="${Mc_Nomi_channel} ${Mc_QCD_el}"
     fi
     if [[ $sample == "Data" && $lep == "mu" ]]; then
     	channels="Run2016B_preVFP_mu Run2016C_preVFP_mu Run2016D_preVFP_mu Run2016E_preVFP_mu Run2016F_preVFP_mu"
     fi
     
     if [[ $sample == "Data" && $lep == "el" ]]; then
     	channels="Run2016B_preVFP_el Run2016C_preVFP_el Run2016D_preVFP_el Run2016E_preVFP_el Run2016F_preVFP_el"
     fi

elif  [[ "UL2016postVFP" == "$year" ]]; then
     dataset_file=$crab_dir"/minitree/dataset_UL2016postVFP_phy3.py"
     outputDir="/store/user/mikumar/RUN2_UL/MiniTree_condor/SIXTEEN_postVFP_v5/"
 
     if [[ $sample == "Mc_Nomi" && $lep == "mu" ]]; then
        channels="${Mc_Nomi_channel} ${Mc_QCD_mu}" 
     fi
     if [[ $sample == "Mc_Nomi" && $lep == "el" ]]; then
        channels="${Mc_Nomi_channel} ${Mc_QCD_el}"
     fi

     if [[ $sample == "Data" && $lep == "mu" ]]; then
        channels="Run2016F_postVFP_mu Run2016G_postVFP_mu Run2016H_postVFP_mu"
     fi

     if [[ $sample == "Data" && $lep == "el" ]]; then
        channels="Run2016F_postVFP_el Run2016G_postVFP_el Run2016H_postVFP_el"
     fi


elif  [[ "UL2017" == "$year" ]]; then
     dataset_file=$crab_dir"/minitree/dataset_UL2017_phy3.py"
     outputDir="/store/user/mikumar/RUN2_UL/MiniTree_condor/SEVENTEEN_v5/"
     if [[ $sample == "Mc_Nomi" && $lep == "mu" ]]; then
	channels="${Mc_Nomi_channel}  ${Mc_QCD_mu}"
     fi

     if [[ $sample == "Mc_Nomi" && $lep == "el" ]]; then
        channels="${Mc_Nomi_channel} ${Mc_QCD_el}"
     fi

     if [[ $sample == "Data" && $lep == "mu" ]]; then
        channels="Run2017B_mu Run2017C_mu Run2017D_mu Run2017E_mu Run2017F_mu"
     fi

     if [[ $sample == "Data" && $lep == "el" ]]; then
        channels="Run2017B_el Run2017C_el Run2017D_el Run2017E_el Run2017F_el"
     fi

elif  [[ "UL2018" == "$year" ]]; then
     dataset_file=$crab_dir"/minitree/dataset_UL2018_phy3.py"
     outputDir="/store/user/mikumar/RUN2_UL/MiniTree_condor/EIGHTEEN/"
     if [[ $sample == "Mc_Nomi" && $lep == "mu" ]]; then
	channels="${Mc_Nomi_channel}  ${Mc_QCD_mu}"
     fi
     if [[ $sample == "Mc_Nomi" && $lep == "el" ]]; then
        channels="${Mc_Nomi_channel}  ${Mc_QCD_el}"
     fi
     if [[ $sample == "Data" && $lep == "mu" ]]; then
     	channels="Run2017C_mu"
     fi
     
     if [[ $sample == "Data" && $lep == "el" ]]; then
     	channels="Run2017C_el"
     fi

fi

if [[ $sample == "Mc_Alt" ]]; then
    channels="${Mc_Alt_channel}"
fi
if [[ $sample == "Mc_sys" ]]; then
    channels="${Mc_sys_channel}"
fi

if ! [ -e "$dataset_file" ]; then
  echo "$dataset_file not found" >&2
  exit 1
fi



#------------------------------------------------
#create a directory where all the outputs will be
#stored, for different merged ntuple input files
#------------------------------------------------
file=$dataset_file
localdir=$(basename $dataset_file)  #get the file name from the dataset_file path 
baseDir=$(pwd)"/$(cut -d'.' -f1 <<<"$localdir")_${region}_${lep}_${sample}_$(date +"%d-%m-%Y")"
echo $localdir
echo $baseDir 
#baseDir="/home/mikumar/tryout2/out_log_$(cut -d'_' -f2 <<<"$year")_$(date +"%d-%m-%Y")"
mkdir -p $baseDir


#-----------------
#create tar file
#-----------------
tarFile=$baseDir/minitree.tar.gz
rm -rf $tarFile
PhysicsTools=${crab_dir}/../../../PhysicsTools
echo $tarFile " -------------------" ${crab_dir} "------------"${PhysicsTools}

tar --exclude='.git' --exclude=${PhysicsTools}'/NanoAODTools/crab/DNN' --exclude=${PhysicsTools}'/NanoAODTools/crab/condor_job'  --exclude=${PhysicsTools}'/NanoAODTools/crab/tree' --exclude=${PhysicsTools}'/NanoAODTools/crab/Gen_Study' --exclude=${PhysicsTools}'/NanoAODTools/crab/Gen_Study_Sebastien' --exclude=${PhysicsTools}'/NanoAODTools/crab/efficiency' --exclude=${PhysicsTools}'/NanoAODTools/crab/lumi_n_pileup' --exclude=${PhysicsTools}'/NanoAODTools/crab/cutflow' --exclude=${PhysicsTools}'/NanoAODTools/crab/puWeight' --exclude=${PhysicsTools}'/NanoAODTools/crab/Effective_Number' --exclude=${PhysicsTools}'/NanoAODTools/crab/Lepton_trigger_efficiency' -zcf $tarFile ${PhysicsTools} 
echo "file zipped ..... "
#echo $channels
echo $channels
for channel in $channels; do
    echo $channel
    #------------------------------------------------
    #Run python script to create input txt file using the dataset name
    #------------------------------------------------
    mkdir "$baseDir""/""$channel"
    outcond="$baseDir""/""$channel"
    #------------------------------------------------
    #copy inportant script to the condor direcrtory
    #------------------------------------------------
    cp condorSetup.sub $outcond
    cp runAtCondor.sh $outcond
    cp $file $outcond
    cp prepare_input_filelist.py $outcond
    cp $crab_dir/minitree/crab_script_Minitree.py $outcond
    cp $crab_dir/minitree/MinitreeModule.py $outcond
    cp $tarFile $outcond
    cd $outcond

    python prepare_input_filelist.py -y "$year" -s "$sample" -l "$lep" -r "$region" -c "$channel"

    count=0
    input_files="All_input_files_"$channel".txt"
    input_file_list="inputFiles=["
    outputroot=${outputDir}${sample}"/"${region}"_"${lep}"/"${channel}"/"
    file_tail=`tail -n 1 $input_files`

    if  [[ "$channel" == *"Run"* ]]; then
        files_in_input_file_list=10
    else files_in_input_file_list=1
    fi
        
    cat $input_files | while read ntupleT2Path
    do
  	#----------------------------------------------
  	# increase the counter to count the files
  	#----------------------------------------------
  	((count++))
  	#if [[ $count%10==0 || $ntupleT2Path == $file_tail ]]; then
  	if [[ $count%$files_in_input_file_list -eq 0 || $ntupleT2Path == $file_tail ]]; then

	     mkdir -p $count
	     #------------------------------------------------
    	     #copy important script to the final condor direcrtory
    	     #------------------------------------------------
	     cp condorSetup.sub $count
	     cp runAtCondor.sh $count
	     cp MinitreeModule.py $count
	     cp crab_script_Minitree.py	$count 
	     cd $count

    	     input_file_list=$input_file_list"'root\://se01.indiacms.res.in/"$ntupleT2Path"' ] " #adding file in the inputfile list and close list for 10 files
	     #------------------------------------------------
             #Inshirt input files to the crab script
             #------------------------------------------------	
    	     #echo $input_file_list
	     echo $count
             #echo $input_file_list
	     sed -i 's:INPUT:'"$input_file_list"':g' crab_script_Minitree.py 
	     sed -i "s:INPUT:root\://se01.indiacms.res.in/${outputroot}tree_$count.root:g" condorSetup.sub
	     #echo "root\://se01.indiacms.res.in/${outputroot}tree_$count.root"
	     condor_submit condorSetup.sub
	     cd ../		    	
             input_file_list="inputFiles=["
  	else
    	     input_file_list=${input_file_list}"'root\://se01.indiacms.res.in/"${ntupleT2Path}"' , "  #adding file in the inputfile list
  	fi
  
    done
done
