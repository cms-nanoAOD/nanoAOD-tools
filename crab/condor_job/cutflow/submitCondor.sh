#!/bin/bash
#REFERENCE
#https://github.com/florez/CONDOR

if [ "$#" -ne 4 ]; then                                                                 #check if input parameters are less than 3
  echo "Usage: $0 <year> <sample> <lep> <region>" >&1
  echo "i.e  ./submitCondor_new.sh UL2016preVFP Mc mu 2J1T1"
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

if ! [[ "Mc" == "$sample" || "Data" == "$sample" ]]; then
    echo "wrong choice of sample ["Mc Data"]"
    exit 1
fi

if ! [[ "mu" == "$lep" || "el" == "$lep" ]]; then
    echo "wrong choice of lepton ["el mu"]"
    exit 1
fi

if ! [[ "2J1T1" == "$region" || "2J1T0" == "$region" ]]; then
    echo "wrong choice of lepton ["2J1T1 2J1T0"]"
    exit 1
fi
#------------------------------------------------
#create the same datasetfile depending on year
#------------------------------------------------
common_mc_sample="Tchannel Tbarchannel tw_top tw_antitop Schannel ttbar_SemiLeptonic ttbar_FullyLeptonic WJetsToLNu_0J WJetsToLNu_1J WJetsToLNu_2J DYJets WWTo2L2Nu WZTo2Q2L ZZTo2Q2L" #Tchannel"
Mc_QCD_mu="QCD_Pt-15To20_MuEnriched QCD_Pt-20To30_MuEnriched QCD_Pt-30To50_MuEnriched QCD_Pt-50To80_MuEnriched QCD_Pt-80To120_MuEnriched QCD_Pt-120To170_MuEnriched QCD_Pt-170To300_MuEnriched QCD_Pt-300To470_MuEnriched QCD_Pt-470To600_MuEnriched QCD_Pt-600To800_MuEnriched QCD_Pt-800To1000_MuEnriched QCD_Pt-1000_MuEnriched"
Mc_QCD_el="QCD_Pt-30to50_EMEnriched QCD_Pt-50to80_EMEnriched QCD_Pt-80to120_EMEnriched QCD_Pt-120to170_EMEnriched QCD_Pt-170to300_EMEnriched QCD_Pt-300toInf_EMEnriched"

if [[ "UL2016preVFP" == "$year" ]]; then
     dataset_file=$crab_dir"/minitree/dataset_UL2016preVFP_phy3.py"
     outputDir="/store/user/mikumar/RUN2_UL/cutFlow_condor/SIXTEEN_preVFP_v5/"

     if [[ $sample == "Mc" && $lep == "mu" ]]; then
	channels="${common_mc_sample} ${Mc_QCD_mu}"
	#Tchannel Tbarchannel 
     fi
     if [[ $sample == "Mc" && $lep == "el" ]]; then
        channels="${common_mc_sample} ${Mc_QCD_el}"
     fi

     if [[ $sample == "Data" && $lep == "mu" ]]; then
     	channels="Run2016E_preVFP_mu Run2016B_preVFP_mu Run2016D_preVFP_mu Run2016C_preVFP_mu Run2016F_preVFP_mu"
     fi
     
     if [[ $sample == "Data" && $lep == "el" ]]; then
     	channels="Run2016E_preVFP_el Run2016B_preVFP_el Run2016D_preVFP_el Run2016C_preVFP_el Run2016F_preVFP_el"
     fi

elif  [[ "UL2016postVFP" == "$year" ]]; then
     dataset_file=$crab_dir"/minitree/dataset_UL2016postVFP_phy3.py"
     outputDir="/store/user/mikumar/RUN2_UL/cutFlow_condor/SIXTEEN_postVFP_v5/"

     if [[ $sample == "Mc" && $lep == "mu" ]]; then
        channels="${common_mc_sample} ${Mc_QCD_mu}" 
     fi
     if [[ $sample == "Mc" && $lep == "el" ]]; then
        channels="${common_mc_sample} ${Mc_QCD_el}"
     fi

     if [[ $sample == "Data" && $lep == "mu" ]]; then
        channels="Run2016F_postVFP_mu Run2016G_postVFP_mu Run2016H_postVFP_mu"
     fi

     if [[ $sample == "Data" && $lep == "el" ]]; then
        channels="Run2016F_postVFP_el Run2016G_postVFP_el Run2016H_postVFP_el"
     fi


elif  [[ "UL2017" == "$year" ]]; then
     dataset_file=$crab_dir"/minitree/dataset_UL2017_phy3.py"
     outputDir="/store/user/mikumar/RUN2_UL/cutFlow_condor/SEVENTEEN_new_v5/"

     if [[ $sample == "Mc" && $lep == "mu" ]]; then
        channels="${common_mc_sample} ${Mc_QCD_mu}"
     fi

     if [[ $sample == "Mc" && $lep == "el" ]]; then
        channels="${common_mc_sample} ${Mc_QCD_el}"
     fi

     if [[ $sample == "Data" && $lep == "mu" ]]; then
        channels="Run2017B_mu Run2017C_mu Run2017D_mu Run2017E_mu Run2017F_mu"
     fi

     if [[ $sample == "Data" && $lep == "el" ]]; then
        channels="Run2017B_el Run2017C_el Run2017D_el Run2017E_el Run2017F_el"
     fi

elif  [[ "UL2018" == "$year" ]]; then
     dataset_file=$crab_dir"/minitree/dataset_UL2018_phy3.py"
     outputDir="/store/user/mikumar/RUN2_UL/cutFlow_condor/EIGHTEEN/"
     if [[ $sample == "Mc" &&  $lep == "mu" ]]; then
	channels="${common_mc_sample} ${Mc_QCD_mu}"
     fi
     if [[ $sample == "Mc" && $lep == "el" ]]; then
        channels="${common_mc_sample} ${Mc_QCD_el}"
     fi
     if [[ $sample == "Data" && $lep == "mu" ]]; then
     	channels="Run2017C_mu"
     fi
     
     if [[ $sample == "Data" && $lep == "el" ]]; then
     	channels="Run2017C_el"
     fi

fi

if ! [ -e "$dataset_file" ]; then
  echo "$dataset_file not found" >&2
  exit 1
fi



#------------------------------------------------
#create a directory where all the outputs will be
#stored, for different merged ntuple input files
#------------------------------------------------
#file=$dataset_file
localdir=$(basename $dataset_file)  #get the file name from the dataset_file path 
baseDir=$(pwd)"/$(cut -d'.' -f1 <<<"$localdir")_${region}_${lep}_${sample}_$(date +"%d-%m-%Y")"
echo $localdir
echo $baseDir 
#baseDir="/home/mikumar/tryout2/out_log_$(cut -d'_' -f2 <<<"$year")_$(date +"%d-%m-%Y")"
mkdir -p $baseDir


#-----------------
#create tar file
#-----------------
#tarFile=$baseDir/cutflow.tar.gz
#rm -rf $tarFile
#PhysicsTools=${crab_dir}/../../../PhysicsTools

#tar --exclude='.git' --exclude=${PhysicsTools}'/NanoAODTools/crab/condor_job'  --exclude=${PhysicsTools}'/NanoAODTools/crab/tree' --exclude=${PhysicsTools}'/NanoAODTools/crab/Gen_Study' --exclude=${PhysicsTools}'/NanoAODTools/crab/Gen_Study_Sebastien' --exclude=${PhysicsTools}'/NanoAODTools/crab/efficiency' --exclude=${PhysicsTools}'/NanoAODTools/crab/lumi_n_pileup' --exclude=${PhysicsTools}'/NanoAODTools/crab/minitree' --exclude=${PhysicsTools}'/NanoAODTools/crab/puWeight' --exclude=${PhysicsTools}'/NanoAODTools/crab/Effective_Number' -zcf $tarFile ${PhysicsTools}
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
    cp $dataset_file  $outcond
    cp prepare_input_filelist.py $outcond
    cp $crab_dir/cutflow/condor_script_cutflow.py $outcond
    cp $crab_dir/cutflow/cutflowModule_new.py  $outcond
    #cp $tarFile $outcond
    cd $outcond

    python prepare_input_filelist.py -y "$year" -s "$sample" -l "$lep" -r "$region" -c "$channel"

    count=0
    input_files="All_input_files_"$channel".txt"
    input_file_list_10="inputFiles=["
    outputroot=${outputDir}${sample}"/"${region}"_"${lep}"/"${channel}"/"
    file_tail=`tail -n 1 $input_files`

    cat $input_files | while read ntupleT2Path
    do
  	#----------------------------------------------
  	# increase the counter to count the files
  	#----------------------------------------------
  	((count++))
  	#if [[ $count%10==0 || $ntupleT2Path == $file_tail ]]; then
  	#if [[ $count%10 -eq 0 || $ntupleT2Path == $file_tail ]]; then

	     mkdir -p $count
	     #------------------------------------------------
    	     #copy important script to the final condor direcrtory
    	     #------------------------------------------------
	     cp condorSetup.sub $count
	     cp runAtCondor.sh $count
	     cp cutflowModule_new.py $count
	     cp condor_script_cutflow.py $count 
	     cd $count
         
    	     input_file_list_10=$input_file_list_10"'root\://se01.indiacms.res.in/"$ntupleT2Path"' ] " #adding file in the inputfile list and close list for 10 files
	     #------------------------------------------------
             #Inshirt input files to the crab script
             #------------------------------------------------	
    	     #echo $input_file_list_10
	     echo $count
	     sed -i 's:INPUT:'"$input_file_list_10"':g' condor_script_cutflow.py 
	     sed -i "s:INPUT:root\://se01.indiacms.res.in/${outputroot}Cutflow_hist_$count.root $channel $count:g" condorSetup.sub
	     #echo "root\://se01.indiacms.res.in/${outputroot}tree_$count.root"
	     condor_submit condorSetup.sub
	     cd ../		    	
             input_file_list_10="inputFiles=["
  	#else
    	#     input_file_list_10=${input_file_list_10}"'root\://se01.indiacms.res.in/"${ntupleT2Path}"' , "  #adding file in the inputfile list
  	#fi
  
  #condor_submit condorSetup.sub
    done
    #sleep 1800
done
