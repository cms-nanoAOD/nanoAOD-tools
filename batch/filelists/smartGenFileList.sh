#!/bin/bash

files=`ls -v /lustre/cmswork/hoh/NANO/SSLep/data/*.root`
#files=`ls -v /lustre/cmswork/hoh/NANO/SSLep/dataskim/*.root`
valS=0
valL=0

if [ -e samplelist_shortQ.py ];then
    rm samplelist_shortQ.py
fi

if [ -e samplelist_longQ.py ];then
    rm samplelist_longQ.py
fi

for rootfile in $files
do
    byte=`ls -l ${rootfile} | awk -F ' ' '{print $5}'`
    z=$(($byte / 1000000000))

    if (( $z < 10 ));then
	((valS+=1))
	if [ "$valS" == "1" ];then
	    echo -e "#!/usr/bin/env python\n" > script1
	    echo -e "samplelists=[" >> script1
	else
	    echo -e "\t'$rootfile'," >> script1
	fi
    elif (( $z > 10 ));then
	((valL+=1))
	if [ "$valL" == "1" ];then
            echo -e "#!/usr/bin/env python\n" > script2
            echo -e "samplelists=[" >> script2
        else
            echo -e "\t'$rootfile'," >> script2
        fi
    fi

done

echo -e "]" >> script1
echo -e "]" >> script2
mv script1 samplelist_shortQ.py
mv script2 samplelist_longQ.py