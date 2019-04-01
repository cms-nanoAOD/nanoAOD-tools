#!/bin/bash

set -e
#monoX=("${monoZp[@]}" "${monoHs[@]}")
#SAMPLE="/lustre/cmswork/sleardin/data/"
#SAMPLE="/lustre/cmsdata/NANOAOD/v00/"
SAMPLE="/lustre/cmswork/hoh/NANO/SSLep/data/"
year="2016"

if [ -e samples.py ] || [ -e samples1.py ] ;then
    rm samples*.py
fi

total=`(eval cd ${SAMPLE}; ls -l | wc -l )`
echo "Total Root Files found = $total"
for sample in `ls ${SAMPLE}`
do

    #file name without root extension
    filename=$(basename "$sample")
    filename="${filename%.*}"

    var=$((var+1))

    if [ $var -eq 1 ];then
	echo "sample = {" > samples1.py
	#echo "samples = { " > samples2.py
    fi
    ######################################################
    #read number of event from tree
    if [ ! -e "eventReader.py" ];then
	echo "Missing eventReader.py , EXITING"
	exit 0
    else
	echo "reading number of event from ${sample}"
	numEvent=`python eventReader.py --nevent --r ${SAMPLE}${sample}`
	xsec=`python eventReader.py --xsec --r ${SAMPLE}${sample}`
	matcheff=`python eventReader.py --matcheff --r ${SAMPLE}${sample}`
	kfactor=`python eventReader.py --kfactor --r ${SAMPLE}${sample}`
    fi

    echo -e "\t'${filename}': {"         >> samples1.py
    echo -e "\t'nevents' : ${numEvent}," >> samples1.py
    echo -e "\t'xsec'    : ${xsec},"          >> samples1.py
    echo -e "\t'matcheff': ${matcheff},"          >> samples1.py
    echo -e "\t'kfactor' : ${kfactor},"          >> samples1.py
    echo -e "\t\t},"                     >> samples1.py

    ##########################################################
    
done

echo -e "}"                 >> samples1.py 
#echo -e "}"                 >> samples2.py      

#cat samples1.py samples2.py > samples.py
#rm samples1.py samples2.py
cat samples1.py legends_${year}.py > samples.py
rm samples1.py