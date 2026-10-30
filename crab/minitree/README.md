# crab sumission for Minitrees

## Requirements from skimtrees
* Published dataset names
* Number of Events in the sample
* Gen level cross section for each process


## Get the data set name for minitree submission
* Use "check_crab_status.py" file to check the crab status for all the submitted dataset
* Save the output of the "check_crab_status.py" in .txt or .py file
* Run "find_phy3_dataset.py" with saved file as a input. This will find and print the array of phys3 datset names.

## Get Number of events in a samples
* go to ../tree/ directory
* Run Event_counter.py -y <datayear>
* This will print the Number of Events of each dataset for the dataset used for given year

## Gen level cross section for each process
* links for the cross-section https://docs.google.com/spreadsheets/d/1aJ2PXRApwRIDCp6VdSjSJhuDhSP-Tt_Xk2JCO6nmjuY/edit?usp=sharing
* For now the cross-section can be took from dataset.py files for lagecy sample (but the numbers in these file are in array and very confusing) 

## Crab submission for MC/data minitree crab

* Crab submission for UL mc samples can be done using "crab_submission_Minitree_mcUL.py" file using the following commond:

	python crab_submission_Minitree_mcUL.py  -y UL2016preVFP -l mu -h (-y stands for year -h stands for help, Script have to run without -h option otherwise it prints the help option only)
	python crab_submission_Minitree_dataUL.py -y UL2016preVFP -l mu -h (-y stands for year -h stands for help, Script have to run without -h option otherwise it prints the help option only)

* new User 
	1. user name <mikumar> and the site name <T2_IN_TIFR> must be changed in "crab_submission_Minitree_mcUL.py" and "crab_submission_Minitree_dataUL.py" accordingly
	2. outputDir = "/store/user/<username>/RUN2_UL/Tree_crab/SIXTEEN/MC_preVFP/check/" (need to chage storege unit accordingly)
	3. config.Site.storageSite = "<sitename>" (need to chage storege unit accordingly)

