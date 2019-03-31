#!/bin/bash

Folder=$1

comd=$2

if [ -z $Folder ] || [ -z $comd ];then
    echo "Select a crab folder or/and option"
    echo -e "EXP: ./util.sh \e[92mcrab folder\e[0m \e[91m1/2\e[0m"
    echo -e "\e[92mcrab folder : Run2016MC/DATA, ...\e[0m"
    echo -e "\e[91m1 : status\e[0m"
    echo -e "\e[91m2 : getoutput\e[0m "
    echo -e "\e[91m3 : kill\e[0m "
    exit
fi

echo -e "--- Looking at \e[32m${Folder}\e[0m ---"

for crablet in `ls ${Folder}`
do
    echo -e "\e[92m$crablet\e[0m"
    if [ $comd == 1 ];then
	action="status"
    elif [ $comd == 2 ];then
	action="getoutput"
    elif [ $comd == 3 ];then
	action="kill"
    fi
    crab ${action} ${Folder}${crablet}
done
