#!/bin/bash

Folder=$1
comd=$2
curr=$PWD
dest="/lustre/cmswork/hoh/NANO/SSLep/nanoskim/dataset-crab/2016/v17/"

if [ -z $Folder ] || [ -z $comd ];then
    echo "Select a crab folder or/and option"
    echo -e "EXP: ./util.sh \e[92mcrab folder\e[0m \e[91m1/2\e[0m"
    echo -e "\e[92mcrab folder : Run2016MC/DATA, ...\e[0m"
    echo -e "\e[91m1 : status\e[0m"
    echo -e "\e[91m2 : getoutput\e[0m "
    echo -e "\e[91m3 : kill\e[0m "
    echo -e "\e[91m4 : merge\e[0m "
    echo -e "\e[91m5 : purge\e[0m "
    exit
fi

echo -e "--- Looking at \e[32m${Folder}\e[0m ---"

for crablet in `ls ${Folder}`
do
    eval cd ${curr}
    name=`echo ${crablet} | awk -F 'crab_' '{print $2}'`
    if (( $comd < 4 ));then
	echo -e "\e[92m$crablet\e[0m"
	if [ $comd == 1 ];then
	    echo "$comd : status of job"
	    sleep 2
	    action="status"
	elif [ $comd == 2 ];then
	    echo "$comd : getoutput of job"
	    numoutputfiles=`ls ${Folder}/${crablet}/results/ | wc -l`
	    if [ $numoutputfiles != 0 ];then
		echo "roor file retrieved and exist"
		continue;
	    fi
	    action="getoutput"
	elif [ $comd == 3 ];then
	    echo "$comd : kill job"
	    sleep 2
	    action="kill"
	fi
	crab ${action} ${Folder}${crablet}
    elif [ $comd == 4 ];then
	echo -e "Mergining root files output in \e[92m$crablet\e[0m"
	eval cd ${curr}/${Folder}/${crablet}/results
	if [ -e "${name}.root" ];then
	    rm ${name}.root
	fi
	echo "python ${curr}/../scripts/haddnano.py ${name}.root *"
	python ${curr}/../scripts/haddnano.py ${dest}/${name}.root *
	ls
    elif [ $comd == 5 ];then
	echo -e "Purging root files output in \e[92m$crablet\e[0m"
	echo "rm ${curr}/${Folder}/${crablet}/results/*"
	rm ${curr}/${Folder}/${crablet}/results/${name}.root
    fi
done
