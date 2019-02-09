#!/bin/bash

#files=`ls -v /lustre/cmswork/hoh/NANO/SSLep/datav4-skim/*.root`
files=`ls -v /lustre/cmsdata/NANOAOD/v00/*.root`
val=0

if [ -e samplelist.py ];then
    rm samplelist.py
fi

for rootfile in $files
do
    ((val+=1))
    if [ "$val" == "1" ];then
	echo -e "#!/usr/bin/env python\n" > script
	echo -e "samplelists=[" >> script
    else
	echo -e "\t'$rootfile'," >> script
    fi
done

echo -e "]" >> script
mv script samplelist.py