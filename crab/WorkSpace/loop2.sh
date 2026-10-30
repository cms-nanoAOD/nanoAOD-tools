# Define the arrays
YEARS=("UL2018") #"UL2016preVFP" "UL2016postVFP" "UL2017" )
LEP=("mu") #"el" "mu")



# if command -v nvidia-smi &>/dev/null && nvidia-smi -L &>/dev/null; then
# 	echo "GPU detected, running with GPU configuration"

# 	# prepare a list of commands
# 	commands=()

# 	for year in "${YEARS[@]}"; do
# 	    for lepton in "${LEP[@]}"; do
# 	        for threshold in $(seq 0.70 0.05 0.70); do
# 	            #commands+=("python3 Create_mtopFit_Workspace_input_file.py -y $year -l $lepton -DC '(t_ch_CAsi>=${threshold})' -v lntopMass -pdf_sys -muR_muF_sys")
# 	            commands+=('python3 Create_mtopFit_Workspace_input_file.py -y '"$year"' -l '"$lepton"' -DC "(t_ch_CAsi>='"${threshold}"')" -v lntopMass -pdf_sys -muR_muF_sys')
# 	        done
# 	    done
# 	done

# 	#printf "%s\n" "${commands[@]}" | parallel -j4
# 	printf "%s\n" "${commands[@]}" | xargs -P 4 -I {} bash -c "{}"
# else
# Loop through each combination
echo "CPU detected, running with GPU configuration"
for year in "${YEARS[@]}"; do
	for lepton in "${LEP[@]}"; do
		for threshold in $(seq 0.70 0.05 0.70); do
			echo "Running for Year: $year, Lepton: $lepton, threshold: $threshold"
			python3 Create_mtopFit_Workspace_input_file.py \
				-y "$year" \
				-l "$lepton" \
				-DC "(t_ch_CAsi>=${threshold})" \
				-v lntopMass \
				#-Alt_center_mass #-Alt # -pdf_sys -muR_muF_sys
		done
	done
done
# fi


########## Prallel processig at GPU  #######################


