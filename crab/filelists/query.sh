#!/bin/bash

function Query () {
    #Construct query                                                                                                                                                                                                          
    if [[ "$1" == "MC" ]];then
	token="mc"
	if [[ "$2" == "2016" ]];then
            dataset="/${3}/RunIISummer16NanoAODv4-*_Nano14Dec2018_102X_mcRun2_asymptotic_v6-v*/NANOAODSIM"
	elif [[ "$2" == "2017" ]];then
            dataset="/${3}/RunIIFall17NanoAODv4-*_Nano14Dec2018*/NANOAODSIM"
	elif [[ "$2" == "2018" ]];then
            dataset="/${3}/RunIIAutumn18NanoAODv4-Nano14Dec2018*/NANOAODSIM"
	else
            echo NULL year
            exit
	fi
    elif [[ "$1" == "DATA" ]];then
	token="data"
	if [[ "$2" == "2016" ]];then
            dataset="/${3}/Run2016*-Nano14Dec2018*-v*/NANOAOD"
	elif [[ "$2" == "2017" ]];then
            dataset="/${3}/Run2017*-Nano14Dec2018*-v*/NANOAOD"
	elif [[ "$2" == "2018" ]];then
            dataset="/${3}/Run2018*-Nano14Dec2018*-v*/NANOAOD"
	else
            echo NULL year
            exit
	fi
    fi
    #Getting the dataset
    if [[ "$4" != "1" ]];then
	sign=">>"
    else
	sign=">"
    fi
    
    path="datasets/Run${2}/$token.txt"
    query1="dasgoclient --limit=0 --query=\"dataset=${dataset}\" ${sign} ${path}"
    eval $query1

}

function List () {
    version=`echo ${1} | awk -F '-' '{print $NF}' | awk -F '/' '{print $1}'`
    name=`echo ${1} | awk -F '/' '{print $2}'`
    ERA=""
    if [[ "$name" == "SingleElectron" ]] || [[ "$name" == "SingleMuon" ]] || [[ "$name" == "DoubleMuon" ]];then
	letter=`echo ${1} | awk -F 'Run' '{print $2}' | awk -F '-' '{print $1}'`
	ERA="Run${letter}"
    fi
    query2="dasgoclient --limit=0 --query=\"file dataset=${1}\" > filelists/Run${2}/${name}${ERA}-${version}.txt"
    echo $query2
    eval $query2
    #add director
    #US --> root://cmsxrootd.fnal.gov/ ; Eu --> root://xrootd-cms.infn.it/ ; global --> root://cms-xrd-global.cern.ch/
    sed -i -e 's/^/root:\/\/xrootd-cms.infn.it\//' filelists/Run${2}/${name}${ERA}-${version}.txt
    echo Created filelist filelists/Run${2}/${name}${ERA}-${version}.txt
}

############################## END OF FUNCTION

if [[ "$1" != "2016" ]] && [[ "$1" != "2017" ]] && [[ "$1" != "2018" ]]
then
    echo 1st argument correspond to year of data/mc
    echo specify 2016 or 2017 or 2018
    exit
else
    year=$1  
    if [ -e "datasets/Run${year}" ];then
	rm -r datasets/Run${year}
    fi
    mkdir -p datasets/Run${year}
fi

# Step1 query dataset
### Execute
echo file reads: "$PWD/nametmp"

VAR=0
while IFS= read -r var
do
    ((VAR+=1))
    name=`echo $var | awk -F ' ' '{print $1}'`
    datatype=`echo $var | awk -F ' ' '{print $2}'`
    echo Query $datatype $year $name
    Query $datatype $year $name $VAR
done < "$PWD/nametmp"

#if [ ! -e "dataset.txt" ];then
#    echo dataset.txt does not exist, exiting
#    exit
#fi

#if [ -d "filelists/Run$year" ];then
#    rm -r filelists/Run${year}
#fi
#mkdir -p filelists/Run${year}

## Step2 make filelist
#echo file reads: "$PWD/dataset.txt"
#while IFS= read -r line
#do
#    echo List $line $year
#    List $line $year
#done < "$PWD/dataset.txt"

######## overriden
cat datasets/Run${year}/mc.txt | sed 's/$/\",/' | sed -e 's/^/\t\"/' | sed '1i\mc = [\' | sed -e "\$a ]" > datasets/Run${year}/MC.py
cat datasets/Run${year}/data.txt | sed 's/$/\",/' | sed -e 's/^/\t\"/' | sed '1i\data = [\' | sed -e "\$a ]" > datasets/Run${year}/DATA.py
rm datasets/Run${year}/mc.txt datasets/Run${year}/data.txt