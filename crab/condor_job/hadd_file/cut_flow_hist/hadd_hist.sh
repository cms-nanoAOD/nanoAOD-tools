#!/bin/bash
export t2_dir="$1"
export dest_dir="$2"
export channel="$3"

numFile=`eval xrdfs se01.indiacms.res.in ls /cms$t2_dir | grep -wc "root"`
echo -e "$numFile Files"
if [ $numFile -ne 0 ]; then
	flag=$((numFile % 10 ))
	count=0
	echo -e "$flag"
    for file in `xrdfs se01.indiacms.res.in ls /cms$t2_dir | grep \\root | awk '{print $1}'`; do
		echo "${file:4}" 
		count=$((count + 1 ))
		blockCount=$((count % 10 ))
		blockID=$((count / 10 ))
        if [ $flag -eq 0 ]; then
			if [ $blockCount -ne 0 ]; then
				array_name[$((blockCount - 1 ))]="root://se01.indiacms.res.in/${file:4}"
			else
				echo -e "$count \t  $blockCount \t $blockID"
				tmpMerge_name[$((blockID - 1 ))]="$dest_dir/tempMerge_$blockID.root"

				echo -e "hadd ${tmpMerge_name[$((blockID - 1 ))]} \t ${array_name[*]} \t root://se01.indiacms.res.in/${file:4}"
#				hadd ${tmpMerge_name[$((blockID - 1 ))]} ${array_name[*]} root://se01.indiacms.res.in/$t2_dir$file
				hadd ${tmpMerge_name[$((blockID - 1 ))]} ${array_name[*]} root://se01.indiacms.res.in/${file:4}	
			fi
		else
			if [ $blockCount -ne 0 ] && [ $count -lt $numFile ]; then		
				array_name[$((blockCount - 1 ))]="root://se01.indiacms.res.in/${file:4}"
			else
				if [ $count -ne $numFile ]; then
					echo -e "$count \t  $blockCount \t $blockID"
					tmpMerge_name[$((blockID - 1 ))]="$dest_dir/tempMerge_$blockID.root"

					echo -e "hadd ${tmpMerge_name[$((blockID - 1 ))]} \t ${array_name[*]} \t root://se01.indiacms.res.in/${file:4}"
#					hadd ${tmpMerge_name[$((blockID - 1 ))]} ${array_name[*]} root://se01.indiacms.res.in/$t2_dir$file
                    hadd ${tmpMerge_name[$((blockID - 1 ))]} ${array_name[*]} root://se01.indiacms.res.in/${file:4}
				else
					blockID=$((blockID + 1 ))
					echo -e "$count \t  $blockCount \t $blockID"
					tmpMerge_name[$((blockID - 1))]="$dest_dir/tempMerge_$blockID.root"	

					echo -e "hadd ${tmpMerge_name[$((blockID - 1 ))]} \t ${array_name[*]:0:$((blockCount - 1 ))} \t root://se01.indiacms.res.in/${file:4}"
#					hadd ${tmpMerge_name[$((blockID - 1 ))]} ${array_name[*]} root://se01.indiacms.res.in/$t2_dir$file
					hadd ${tmpMerge_name[$((blockID - 1 ))]} ${array_name[*]:0:$((blockCount - 1 ))} root://se01.indiacms.res.in/${file:4}
				fi		
			fi	
		fi

    done
    echo -e "hadd $dest_dir/$channel.root \t ${tmpMerge_name[*]}"
    hadd $dest_dir/$channel.root ${tmpMerge_name[*]}	
else
	echo -e "Already hadd-ed"
fi
unset array_name
echo -e "${#array_name[@]}"
unset tmpMerge_name
echo -e "${#tmpMerge_name[@]}"

