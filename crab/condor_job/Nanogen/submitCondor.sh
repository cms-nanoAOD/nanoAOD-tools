#!/bin/bash
#REFERENCE
#https://github.com/florez/CONDOR

if [ "$#" -ne 2 ]; then                                                                 #check if input parameters are less than 3
  echo "Usage: $0 <year> <sample> " >&1
  echo "i.e  ./submitCondor_new.sh UL2016 Mc "
  exit 1
fi
if ! [ "$1" ]; then
  echo "$1 not found" >&2
  exit 1
fi

year=$1
sample=$2
crab_dir="/home/mikumar/t3store3/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab"

if ! [[ "UL2016" == "$year" ]]; then
    echo "wrong choice of year ["UL2016"]"
    exit 1
fi

if ! [[ "Mc" == "$sample" ]]; then
    echo "wrong choice of sample ["Mc"]"
    exit 1
fi

echo $year
echo $sample

#------------------------------------------------
#create the same datasetfile depending on year
#------------------------------------------------
Mc_common_channel="Tchannel_wtop1p0  Tchannel_wtop1p15 Tchannel_wtop1p3" #" Tchannel_wtop1p31  Tbarchannel_wtop0p55 Tbarchannel_wtop0p7  Tbarchannel_wtop0p85 Tbarchannel_wtop1p0 Tbarchannel_wtop1p15 Tbarchannel_wtop1p3   Tbarchannel_wtop1p45  Tchannel_wtop0p55  Tchannel_wtop0p7 Tchannel_wtop0p85  Tchannel_wtop1p0  Tchannel_wtop1p15 Tchannel_wtop1p3 Tchannel_wtop1p45" # Tbarchannel_wtop1p31" 
#"Tchannel_mtop1725_sum16 Tbarchannel_mtop1725_sum16"
#"Tchannel_mtop1695_sum16 Tchannel_mtop1715_sum16 Tchannel_mtop1735_sum16 Tchannel_mtop1755_sum16 Tbarchannel_mtop1715_sum16 Tbarchannel_mtop1755_sum16 Tbarchannel_mtop1785_sum16"
#"Tchannel_1695 Tchannel_1715 Tchannel_1735 Tchannel_1755 Tbarchannel_1695 Tbarchannel_1715 Tbarchannel_1735 Tbarchannel_1755"
 #"Tbarchannel_wtop1p31  Tchannel_wtop1p31  Tbarchannel_wtop0p55 Tbarchannel_wtop0p7  Tbarchannel_wtop0p85 Tbarchannel_wtop1p0 Tbarchannel_wtop1p15 Tbarchannel_wtop1p3   Tbarchannel_wtop1p45  Tchannel_wtop0p55  Tchannel_wtop0p7 Tchannel_wtop0p85  Tchannel_wtop1p0  Tchannel_wtop1p15 Tchannel_wtop1p3 Tchannel_wtop1p45" 

if [[ "UL2016" == "$year" ]]; then
     dataset_file=$crab_dir"/Gen_Study/dataset_UL2016_phy3.py"
     outputDir="/store/user/mikumar/RUN2_UL/MiniTree_condor/SIXTEEN_Nanogen/Mc_v10/"

     
	channels="${Mc_common_channel}" 
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
baseDir=$(pwd)"/$(cut -d'.' -f1 <<<"$localdir")_${year}_${sample}_$(date +"%d-%m-%Y")"
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

tar --exclude='.git' --exclude=${PhysicsTools}'/NanoAODTools/crab/condor_job'  --exclude=${PhysicsTools}'/NanoAODTools/crab/tree' --exclude=${PhysicsTools}'/NanoAODTools/crab/minitree' --exclude=${PhysicsTools}'/NanoAODTools/crab/Gen_Study_Sebastien' --exclude=${PhysicsTools}'/NanoAODTools/crab/efficiency' --exclude=${PhysicsTools}'/NanoAODTools/crab/lumi_n_pileup' --exclude=${PhysicsTools}'/NanoAODTools/crab/cutflow' --exclude=${PhysicsTools}'/NanoAODTools/crab/puWeight' --exclude=${PhysicsTools}'/NanoAODTools/crab/Effective_Number' --exclude=${PhysicsTools}'/NanoAODTools/crab/Lepton_trigger_efficiency' --exclude=${PhysicsTools}'/NanoAODTools/crab/DNN' --exclude=${PhysicsTools}'/NanoAODTools/crab/WorkSpace' -zcf $tarFile ${PhysicsTools}
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
    cp $crab_dir/Gen_Study/crab_script_NanoGen_minitree.py $outcond
    cp $crab_dir/Gen_Study/Gen_mass_reconstract_SingleTop_minitree.py $outcond
    cp $tarFile $outcond
    cd $outcond

    python prepare_input_filelist.py -y "$year" -s "$sample" -c "$channel"

    count=0
    input_files="All_input_files_"$channel".txt"
    input_file_list="inputFiles=["
    outputroot=${outputDir}${sample}"/"${channel}"/"
    file_tail=`tail -n 1 $input_files`

    if  [[ "$channel" == "Tchannel" || "$channel" == "Tbarchannel" || "$channel" == "ttbar_SemiLeptonic" || "$channel" == "ttbar_FullyLeptonic" ]]; then
        files_in_input_file_list=5
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
	     cp crab_script_NanoGen_minitree.py $count
	     cp Gen_mass_reconstract_SingleTop_minitree.py	$count 
	     cd $count

    	     input_file_list=$input_file_list"'root\://se01.indiacms.res.in/"$ntupleT2Path"' ] " #adding file in the inputfile list and close list for 10 files
	     #------------------------------------------------
             #Inshirt input files to the crab script
             #------------------------------------------------	
    	     #echo $input_file_list
	     echo $count
	     sed -i 's:INPUT:'"$input_file_list"':g'  crab_script_NanoGen_minitree.py
	     sed -i "s:INPUT:root\://se01.indiacms.res.in/${outputroot}tree_$count.root:g" condorSetup.sub
	     #echo "root\://se01.indiacms.res.in/${outputroot}tree_$count.root"
	     #condor_submit condorSetup.sub
	     cd ../		    	
             input_file_list="inputFiles=["
  	else
    	     input_file_list=${input_file_list}"'root\://se01.indiacms.res.in/"${ntupleT2Path}"' , "  #adding file in the inputfile list
  	fi
  
    done
done
