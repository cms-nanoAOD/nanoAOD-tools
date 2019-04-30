#!/bin/bash

#files=`ls -v /lustre/cmswork/hoh/NANO/SSLep/data/*.root`
#files=`ls -v /lustre/cmswork/hoh/NANO/SSLep/dataskim/*.root`
#files=`ls -v /lustre/cmswork/hoh/NANO/SSLep/SkimDatav2/*.root`
files=`ls -v /lustre/cmswork/hoh/NANO/PrivateSignal/signals/LO-v1/Wplushwwlvjj_M125_Madspin_slc6_amd64_gcc481_CMSSW_7_1_30/*.root`

valS=0
valL=0

Threshold=30

if [ -e samplelist_SkimshortQ.py ];then
    rm samplelist_SkimshortQ.py
fi

if [ -e samplelist_SkimlongQ.py ];then
    rm samplelist_SkimlongQ.py
fi

for rootfile in $files
do
    byte=`ls -l ${rootfile} | awk -F ' ' '{print $5}'`
    z=$(($byte / 1000000000))

    if (( $z < $Threshold ));then
	echo "$rootfile with byte --> $z GB ; thus SHORT Queue"
	((valS+=1))
	if [ "$valS" == "1" ];then
	    echo -e "#!/usr/bin/env python\n" > script1
	    echo -e "samplelists=[" >> script1
	    echo -e "\t'$rootfile'," >> script1
	else
	    echo -e "\t'$rootfile'," >> script1
	fi
    elif (( $z >= $Threshold ));then
	echo "$rootfile with byte --> $z GB ; thus LONG Queue"
	((valL+=1))
	if [ "$valL" == "1" ];then
            echo -e "#!/usr/bin/env python\n" > script2
            echo -e "samplelists=[" >> script2
	    echo -e "\t'$rootfile'," >> script2
        else
            echo -e "\t'$rootfile'," >> script2
        fi
    fi

done

echo -e "]" >> script1
echo -e "]" >> script2
mv script1 samplelist_SkimshortQ.py
mv script2 samplelist_SkimlongQ.py
echo "========================="
echo "samplelist_SkimshortQ.py with $valS root files"
echo "samplelist_SkimlongQ.py with $valL root files"
echo "========================="