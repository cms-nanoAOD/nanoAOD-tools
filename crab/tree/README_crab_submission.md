Crab submission for MC skimtree
 	1. Lines in crab_cfg_skimTree.py must check before submission:
		for MC:
			config.Data.splitting = 'FileBased'
			config.Data.unitsPerJob = 1
			config.Data.publication = True
		for data:
			config.Data.splitting = 'LumiBased'
			config.Data.unitsPerJob = 150 
			config.Data.lumiMask = <path to Json file> 
			config.Data.publication = True

		other configuration are taken care by "crab_submission_mcUL.py" file

 	2. Crab submission for UL mc samples can be done using "crab_submission_mcUL.py" file using the following commond:

	 	python crab_submission_mcUL.py  -y UL2016preVFP -h (-y stands for year -h stands for help, Script have to run without -h option otherwise it prints the help option only)

		for new User user name <mikumar> and the site name <T2_IN_TIFR> must be changes accordingly

			a. outputDir = "/store/user/<username>/RUN2_UL/Tree_crab/SIXTEEN/MC_preVFP/check/"
			b. config.Site.storageSite = "<sitename>" (need to chage storege unit accordingly)
 
