# crab sumission and validation of the skim trees

## Warnings

* python/postprocessing/modules/common/PrefireCorr16.py is not there in new setup ------> No worries prefire weights are provided in nanoaod files

* jecredo option has been removed check why------> Does't matter because redo option was for fat jets not for AK4 jets

## Crab submission for MC skimtree

* Lines in crab_cfg_skimTree.py must check before submission:
                for data:
                        config.Data.lumiMask = <path to Json file>

		these chages chages has to be done before we run "crab_submission_mcUL.py" or "crab_submission_dataUL.py" since these file can not modify the line starting with "#"
		other configuration are taken care by "crab_submission_mcUL.py" and "crab_submission_dataUL.py" file

* Crab submission for UL mc/data samples can be done using "crab_submission_mcUL.py" file using the following commond:

		python crab_submission_mcUL.py  -y UL2016preVFP -h (-y stands for year -h stands for help, Script have to run without -h option otherwise it prints the help option only)
		python crab_submission_dataUL.py  -y UL2016preVFP -h (-y stands for year -h stands for help, Script have to run without -h option otherwise it prints the help option only)

* For new User 
	1. user name <mikumar> and the site name <T2_IN_TIFR> must be changed in "crab_submission_mcUL.py" and "crab_submission_dataUL.py" accordingly
	2. outputDir = "/store/user/<username>/RUN2_UL/Tree_crab/SIXTEEN/MC_preVFP/check/" (need to chage storege unit accordingly)
	3. config.Site.storageSite = "<sitename>" (need to chage storege unit accordingly)

## Recomdation  UL16preVFP
	
* 	pdmv  
	https://twiki.cern.ch/twiki/bin/view/CMS/PdmV  
	https://twiki.cern.ch/twiki/bin/view/CMS/PdmVRun2LegacyAnalysis
 
		Global Tags:

    			Data: 106X_dataRun2_v35
    			MC 2016APV: 106X_mcRun2_asymptotic_preVFP_v11

*	Btagging (RunIISummer20UL16)
	https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL16preVFP

		DeepJet=DeepFlavour 
		input csv file:
			reshaping_deepJet_106XUL16preVFP_v2.csv (problem)    	csv (iterativeFit shape correction)
			wp_deepJet_106XUL16preVFP_v2.csv (problem)		csv (WP only) 

			old version finle name remain the same 
			
			loose 	0.0508 
			medium 	0.2598 
			tight 	0.6502
						
			measurement_types we are used right now depends on btv_flavour. 0: Comb, 1:comb, 2:incl , shapevariation:  "iterativefit"

	          For precision measurements on top physics, it is recommended to use the "mujets" scale factors, as statistically independent. 
	
*	jecTagsMC (Summer19UL16APV_V7_MC)	
        https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC

			inputfile: 
				Summer19UL16APV_V7_MC.tar.gz     
			GT:
				Summer19UL16APV_V7_MC.tar.gz   
				(GT for Summer20UL samples is 106X_mcRun2_asymptotic_preVFP_v11)

*	jecTagsData (Summer19UL16_V7_DATA  )
        https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC

                        inputfiles:
                                Summer19UL16_V7_all.tar.gz
                        GT:     
				106X_dataRun2_v35
	
*	jerMC (2016)
	https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution

		inputfile:
			Summer20UL16APV_JRV3_MC.tar.gz

*	jerData (2016)
        https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution

                inputfile:
                      	Summer20UL16APV_JRV3_DATA.tar.gz
			Please note that JER-SF files for data just contain unity and are not supposed to be used in the analyses. They are needed for internal consistence of the framework, i.e. currently CMSSW requires the JER-SF file also for data for compatibility. 

*       PUID
        https://twiki.cern.ch/twiki/bin/viewauth/CMS/PileupJetIDUL
                inputfile:
                        https://gitlab.cern.ch/cms-nanoAOD/jsonpog-integration/-/tree/master/POG/JME/2016preVFP_UL -> jmar.json.gz
                        correclation libraries are installed with python2 acc to https://cms-nanoaod.github.io/correctionlib/install.html#inside-cmssw
                        

*	MET
	https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETRun2Corrections#Implementation
 
		The jet collection used in Type-I corrections for PF MET is AK4PFchs jets with JES corrected Pt>15 GeV (using the L1L2L3 -L1 scheme). 
		The jets that are used to correct MET are also required to have electromagnetic energy fraction smaller than 0.9 and not to be overlapping with the pf muon candidate. 

	https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2#2016_data_and_MC_UL

		MetFilter applied (UL2016)as OR comnibanation of flags listed below

		|filter 		|NanoAOD flag used 			| bit	|
 		|:---------------------:|:-------------------------------------:|:------|
		|primary vertex filter  |Flag_goodVertices 			| 1	| 	 
		|beam halo filter 	|Flag_globalSuperTightHalo2016Filter	|1	|
		|HBHE noise filter 	|Flag_HBHENoiseFilter			|1	|
		|HBHEiso noise filter 	|Flag_HBHENoiseIsoFilter		| 1	|
		|ECAL TP filter 	|Flag_EcalDeadCellTriggerPrimitiveFilter|1	|
		|Bad PF Muon Filter 	|Flag_BadPFMuonFilter			|1	| 
		|Bad PF Muon Dz Filter 	|Flag_BadPFMuonDzFilter			|1	|
		|ee badSC noise filter 	|Flag_eeBadScFilter			|1	|
 
*	Pileup weight / minimum bias x-sec (When using UltraLegacy samples)
	https://twiki.cern.ch/twiki/bin/view/CMS/PileupJSONFileforData

		inputfiles:
			/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/PileUp/UltraLegacy/

		In all those directories you will find (as indicated in the file name) histograms corresponding to the following values of the pp inelastic cross section: 
		69200 ub (recommended central value), 66000 ub (central value - 4.6%), 72400 ub (central value + 4.6%), 80000 ub (conventional value used for the public plots, 
		agreed with ATLAS years ago).

		(100 bins from PrelLum13TeV not reommended ) In Nanoaod tool we are using the following file where up down variation root files are add in subdiretories  :
			pufile_dataUL2016 = "/src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/PileupHistogram-UL2016-100bins_withVar.root" 
						three histogram namly : 
								KEY: TH1F	pileup;1	
								KEY: TH1F	pileup_plus;1	
								KEY: TH1F	pileup_minus;1		
			pufile_mcUL2016 = "/src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/mcPileupUL2016.root" 
						one histogram namely:
								KEY: TH1F	pu_mc;1

*	MuonPog
	https://twiki.cern.ch/twiki/bin/view/CMS/MuonPOG	
	https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonUL2016#Medium_pT_from_15_to_120_GeV

		scale factor = (L(BCDEF)*sf(BCDEF) + L(GH)*sf(GH))/(L(BCDEF)+L(GH)) 

		Input files:
			ID:
				Efficiencies_muon_generalTracks_Z_Run2016_UL_HIPM_ID.root #BCDEF (required for ISO>0.2) (reading "hist NUM_TightID_DEN_TrackerMuons_abseta_pt" ?? old "MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/pt_abseta_ratio")
				Efficiencies_muon_generalTracks_Z_Run2016_UL_ID.root ##GH	(required for ISO>0.2)
		
				EfficienciesAndSF_Run2016_UL_HIPM_ID_SF_0p06.root (personly created for iso<0.06 and need to update this is taken from lagecy samples and renamed acc.) 
				EfficienciesAndSF_Run2016_UL_ID_SF_0p06.root (personly created for iso<0.06 and need to update this taken from lagecy samples and renamed acc.)				

			ISO:
				Efficiencies_muon_generalTracks_Z_Run2016_UL_HIPM_ISO.root ##BCDEF (remonnded but we are not using them for iso>0.2 and we retrun SF=1) 
				Efficiencies_muon_generalTracks_Z_Run2016_UL_ISO.root #GH (remonnded but we are not using them for iso>0.2 and we retrun SF=1)

				EfficienciesAndSF_Run2016_UL_HIPM_ISO_SF_0p06.root (personly created for iso<0.06 and need to update this is taken from lagecy samples and renamed acc.)
                        	EfficienciesAndSF_Run2016_UL_ISO_SF_0p06.root  (personly created for iso<0.06 and need to update this taken from lagecy samples and renamed acc.)	

			TRI:
				Trigger efficiency: provided in json formet only ((remonnded but we are not using them for iso>0.2 and we retrun SF=1))

				EfficienciesAndSF_Run2016_UL_HIPM_Trigger_SF_0p06.root (personly created for iso<0.06 and need to update this is taken from lagecy samples and renamed acc.)
				EfficienciesAndSF_Run2016_UL_Trigger_SF_0p06.root (personly created for iso<0.06 and need to update this taken from lagecy samples and renamed acc.)

*	EgammaPog
	https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammaUL2016To2018#SFs_for_Electrons_UL_2016_preVFP
		
		Input files:
			Cut Based ID 	Veto : 
						/eos/cms/store/group/phys_egamma/SF-Repository/UL16/preVFP/Electrons/Veto/egammaEffi.txt_Ele_Veto_preVFP_EGM2D.root 	
	
			Cut Based ID    Tight :
						/eos/cms/store/group/phys_egamma/SF-Repository/UL16/preVFP/Electrons/Tight/egammaEffi.txt_Ele_Tight_preVFP_EGM2D.root
	
			Cut Based ID    Trigger :
						TRI_Tight    : ElectronSF/Run2_UL_TRI_SF_by_Mukund/UL2016_preVFP_Tight.root  # privatly produced Trigger+tightid
                        			TRI_Veto    :  ElectronSF/Run2_UL_TRI_SF_by_Mukund/UL2016_preVFP_Veto.root   #privatly produced Trigger_vetoid
        

*	LumiSectionsJSONFile
	https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideGoodLumiSectionsJSONFile (json file paths are taken from here)
	https://twiki.cern.ch/twiki/bin/view/CMS/TWikiLUM#CurRec (these recommadation seems old)
	https://twiki.cern.ch/twiki/bin/view/CMS/PdmVDataReprocessingUL2016 (RunNumbers)
	
		Golden Json file : 2016 data: visit lxplus and it is located at /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt 

## Recomdation UL16postVFP 

*	pdmv 
	https://twiki.cern.ch/twiki/bin/view/CMS/PdmV
	https://twiki.cern.ch/twiki/bin/view/CMS/PdmVRun2LegacyAnalysis
	
		Global Tags:

    			Data: 106X_dataRun2_v35
    			MC 2016: 106X_mcRun2_asymptotic_v17

*	Btagging ( RunIISummer20UL16)
	https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL16postVFP

		DeepJet=DeepFlavour 	
		input csv file:
			reshaping_deepJet_106XUL16postVFP_v3.csv (problem)	csv (iterativeFit shape correction)
			wp_deepJet_106XUL16postVFP_v3.csv(problem)		csv (WP only)
	
			old version file name remain the same
							
			loose 	0.0480 
			medium 	0.2489
			tight 	0.6377
		For precision measurements on top physics, it is recommended to use the "mujets" scale factors, as statistically independent.  

*	jecTagsMC (Summer19UL16_V7_MC)
	https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC
	
		inputfile: 
			Summer19UL16_V7_MC.tar.gz   
		GT: 
			106X_mcRun2_asymptotic_v17 
			(GT for Summer20UL samples is 106X_mcRun2_asymptotic_v17)

*	jecTagsData (Summer19UL16_V7_DATA  )
	https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC

                        inputfiles:
				Summer19UL16_V7_all.tar.gz
			GT: 	
				106X_dataRun2_v35

*	jerMC (2016)
	https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution

                inputfile:
                         Summer20UL16_JRV3_MC.tar.gz

*	jerData (2016)
	https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution

                inputfile:
			Summer20UL16_JRV3_DATA.tar.gz
			Please note that JER-SF files for data just contain unity and are not supposed to be used in the analyses. They are needed for internal consistence of the framework, i.e. currently CMSSW requires the JER-SF file also for data for compatibility. 

*       PUID
        https://twiki.cern.ch/twiki/bin/viewauth/CMS/PileupJetIDUL
                inputfile:
                        https://gitlab.cern.ch/cms-nanoAOD/jsonpog-integration/-/tree/master/POG/JME/2016postVFP_UL -> jmar.json.gz
                        correclation libraries are installed with python2 acc to https://cms-nanoaod.github.io/correctionlib/install.html#inside-cmssw

*	MET
	https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETRun2Corrections#Implementation

                The jet collection used in Type-I corrections for PF MET is AK4PFchs jets with JES corrected Pt>15 GeV (using the L1L2L3 -L1 scheme). 
                The jets that are used to correct MET are also required to have electromagnetic energy fraction smaller than 0.9 and not to be overlapping with the pf muon candidate.

	https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2#2016_data_and_MC_UL

                MetFilter applied (UL2016) as OR comnibanation of flags listed below

                |filter                 |NanoAOD flag used                      | bit   | 
                |:---------------------:|:-------------------------------------:|:------|
                |primary vertex filter  |Flag_goodVertices                      |   1    |                        
                |beam halo filter       |Flag_globalSuperTightHalo2016Filter    |   1    |
                |HBHE noise filter      |Flag_HBHENoiseFilter                   |   1    |
                |HBHEiso noise filter   |Flag_HBHENoiseIsoFilter                |   1    |
                |ECAL TP filter         |Flag_EcalDeadCellTriggerPrimitiveFilter|   1    |
                |Bad PF Muon Filter     |Flag_BadPFMuonFilter                   |   1    | 
                |Bad PF Muon Dz Filter  |Flag_BadPFMuonDzFilter                 |   1    |
                |ee badSC noise filter  |Flag_eeBadScFilter                     |   1    |

	
*	Pileup weight / minimum bias x-sec (When using UltraLegacy samples)
	https://twiki.cern.ch/twiki/bin/view/CMS/PileupJSONFileforData

                inputfiles:
                        /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/PileUp/UltraLegacy/

                In all those directories you will find (as indicated in the file name) histograms corresponding to the following values of the pp inelastic cross section:
                69200 ub (recommended central value), 66000 ub (central value - 4.6%), 72400 ub (central value + 4.6%), 80000 ub (conventional value used for the public plots,
                agreed with ATLAS years ago).

                (100 bins from PrelLum13TeV not reommended )In Nanoaod tool we are using the following file where up down variation root files are add in subdiretories (100 bin from recommded) :
			pufile_dataUL2016 = "/src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/PileupHistogram-UL2016-100bins_withVar.root"
                        pufile_mcUL2016 = "/src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/mcPileupUL2016.root"	

*	MuonPog
	https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonUL2016#Medium_pT_from_15_to_120_GeV

		scale factor = (L(BCDEF)*sf(BCDEF) + L(GH)*sf(GH))/(L(BCDEF)+L(GH)) 
		
		Input files:
                        ID:
                                Efficiencies_muon_generalTracks_Z_Run2016_UL_HIPM_ID.root #BCDEF (required for ISO>0.2) (reading hist "NUM_TightID_DEN_TrackerMuons_abseta_pt" ?? old "MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/pt_abseta_ratio")
                                Efficiencies_muon_generalTracks_Z_Run2016_UL_ID.root ##GH       (required for ISO>0.2)

                                EfficienciesAndSF_Run2016_UL_HIPM_ID_SF_0p06.root (personly created for iso<0.06 and need to update this is taken from lagecy samples and renamed acc.)
                                EfficienciesAndSF_Run2016_UL_ID_SF_0p06.root (personly created for iso<0.06 and need to update this taken from lagecy samples and renamed acc.)

                        ISO:
                                Efficiencies_muon_generalTracks_Z_Run2016_UL_HIPM_ISO.root ##BCDEF (remonnded but we are not using them for iso>0.2 and we retrun SF=1)
                                Efficiencies_muon_generalTracks_Z_Run2016_UL_ISO.root #GH (remonnded but we are not using them for iso>0.2 and we retrun SF=1)

                                EfficienciesAndSF_Run2016_UL_HIPM_ISO_SF_0p06.root (personly created for iso<0.06 and need to update this is taken from lagecy samples and renamed acc.)
                                EfficienciesAndSF_Run2016_UL_ISO_SF_0p06.root  (personly created for iso<0.06 and need to update this taken from lagecy samples and renamed acc.)

                        TRI:
                                Trigger efficiency: provided in json formet only ((remonnded but we are not using them for iso>0.2 and we retrun SF=1))

                                EfficienciesAndSF_Run2016_UL_HIPM_Trigger_SF_0p06.root (personly created for iso<0.06 and need to update this is taken from lagecy samples and renamed acc.)
                                EfficienciesAndSF_Run2016_UL_Trigger_SF_0p06.root (personly created for iso<0.06 and need to update this taken from lagecy samples and renamed acc.)

*	EgammaPog
	https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammaUL2016To2018#SFs_for_Electrons_UL_2016_postVF

                Input files:
                        Cut Based ID    Veto :
                                                /eos/cms/store/group/phys_egamma/SF-Repository/UL16/postVFP/Electrons/Veto/egammaEffi.txt_Ele_Veto_postVFP_EGM2D.root (recommonded) (histogram reading "EGamma_SF2D")
						scp  /eos/cms/store/group/phys_egamma/SF-Repository/UL16/postVFP/Electrons/Veto/egammaEffi.txt_EGM2D.root egammaEffi.txt_Ele_Veto_postVFP_EGM2D.root 

                        Cut Based ID    Tight :
                                                /eos/cms/store/group/phys_egamma/SF-Repository/UL16/postVFP/Electrons/Tight/egammaEffi.txt_Ele_Tight_postVFP_EGM2D.root (recommonded)
						scp /eos/cms/store/group/phys_egamma/SF-Repository/UL16/postVFP/Electrons/Tight/egammaEffi.txt_EGM2D.root egammaEffi.txt_Ele_Tight_postVFP_EGM2D.root


                        Cut Based ID    Trigger :
						TRI_Tight    : ElectronSF/Run2_UL_TRI_SF_by_Mukund/UL2016_postVFP_Tight.root # privaltly produced trigger_tightID
                        			TRI_Veto    :  ElectronSF/Run2_UL_TRI_SF_by_Mukund/UL2016_postVFP_Veto.root # privatly produced # tigger+veto
                                                
 
*	LumiSectionsJSONFile
        https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideGoodLumiSectionsJSONFile (json file paths are taken from here)
        https://twiki.cern.ch/twiki/bin/view/CMS/TWikiLUM#CurRec (these recommadation seems old)
        https://twiki.cern.ch/twiki/bin/view/CMS/PdmVDataReprocessingUL2016 (RunNumbers)

		Golden Json file : 2016 data: visit lxplus and it is located at /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt

## Recomdation  UL17 

*	pdmv
        https://twiki.cern.ch/twiki/bin/view/CMS/PdmV
        https://twiki.cern.ch/twiki/bin/view/CMS/PdmVRun2LegacyAnalysis
 
		Global Tags:

    			Data: 106X_dataRun2_v35
    			MC 2017: 106X_mc2017_realistic_v9
	
*	Btagging (RunIISummer19UL17 )
	https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL17

        	DeepJet=DeepFlavour 
                input csv file: 
                        reshaping_deepJet_106XUL17_v3.csv (problem because of chages applied)       csv (iterativeFit shape correction)
                        wp_deepJet_106XUL17_v3.csv  (problem because of chages applied)             csv (WP only)

			DeepJet_106XUL17SF_V2p1.csv             csv (iterativeFit shape correction +  WP)
                        DeepJet_106XUL17SF_WPonly_V2p1.csv      csv (WP only)

                        loose   0.0532  
                        medium  0.3040           
                        tight   0.7476
		For precision measurements on top physics, it is recommended to use the "mujets" scale factors, as statistically independent. 
	
*	jecTagsMC (Summer19UL17 V5 )
	https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC
		
		inputfile: 
			Summer19UL17_V5_MC.tar.gz   
		GT: 	
			106X_mc2017_realistic_v8  
			(GT for Summer20UL samples is 106X_mc2017_realistic_v9)

*	jecTagsData (Summer19UL17 )
	https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC

                        inputfiles:
                                Summer19UL17_RunB_V5_DATA.tar.gz
                                Summer19UL17_RunC_V5_DATA.tar.gz
                                Summer19UL17_RunD_V5_DATA.tar.gz
                                Summer19UL17_RunE_V5_DATA.tar.gz
                                Summer19UL17_RunF_V5_DATA.tar.gz
                        GT:     
				106X_dataRun2_v33

* 	jerMC (Summer19UL17)
        https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution

                inputfile:
                         Summer19UL17_JRV2_MC.tar.gz

*	jerData (Summer19UL17)
        https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution

                inputfile:
                        Summer19UL17_JRV2_DATA.tar.gz
			Please note that JER-SF files for data just contain unity and are not supposed to be used in the analyses. They are needed for internal consistence of the framework, i.e. currently CMSSW requires the JER-SF file also for data for compatibility. 

*       PUID
        https://twiki.cern.ch/twiki/bin/viewauth/CMS/PileupJetIDUL
                inputfile:
                        https://gitlab.cern.ch/cms-nanoAOD/jsonpog-integration/-/tree/master/POG/JME/2017_UL -> jmar.json.gz
                        correclation libraries are installed with python2 acc to https://cms-nanoaod.github.io/correctionlib/install.html#inside-cmssw

*	MET
	https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETRun2Corrections#Implementation

                The jet collection used in Type-I corrections for PF MET is AK4PFchs jets with JES corrected Pt>15 GeV (using the L1L2L3 -L1 scheme). 
                The jets that are used to correct MET are also required to have electromagnetic energy fraction smaller than 0.9 and not to be overlapping with the pf muon candidate.

	https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2#2018_2017_data_and_MC_UL

                MetFilter applied (UL2017) as OR comnibanation of flags listed below

                |filter                 |NanoAOD flag used                      | bit   | 
                |:---------------------:|:-------------------------------------:|:------|
                |primary vertex filter  |Flag_goodVertices                      |   1    |                        
                |beam halo filter       |Flag_globalSuperTightHalo2016Filter    |   1    |
                |HBHE noise filter      |Flag_HBHENoiseFilter                   |   1    |
                |HBHEiso noise filter   |Flag_HBHENoiseIsoFilter                |   1    |
                |ECAL TP filter         |Flag_EcalDeadCellTriggerPrimitiveFilter|   1    |
                |Bad PF Muon Filter     |Flag_BadPFMuonFilter                   |   1    | 
                |Bad PF Muon Dz Filter  |Flag_BadPFMuonDzFilter                 |   1    |
                |ee badSC noise filter  |Flag_eeBadScFilter                     |   1    |
		|ECAL bad calibration filter update |Flag_ecalBadCalibFilter	|   1 	| 


*	Pileup weight / minimum bias x-sec( did not say )
        https://twiki.cern.ch/twiki/bin/view/CMS/PileupJSONFileforData

                inputfiles:
                        /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/PileUp/UltraLegacy/

	        In all those directories you will find (as indicated in the file name) histograms corresponding to the following values of the pp inelastic cross section:
                69200 ub (recommended central value), 66000 ub (central value - 4.6%), 72400 ub (central value + 4.6%), 80000 ub (conventional value used for the public plots,
                agreed with ATLAS years ago).

                (100 bins from PrelLum13TeV not reommended )In Nanoaod tool we are using the following file where up down variation root files are add in subdiretories  :
			pufile_dataUL2017 = "/src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/PileupHistogram-UL2017-100bins_withVar.root" 
			pufile_mcUL2017 = "/src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/mcPileupUL2017.root"			

*	MuonPog
	https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonLegacy2017#Medium_pT_from_15_to_120_GeV

                Input files:
                        ID:
				RunBCDEF_SF_ID_syst.root # BCDEF (required for ISO>0.2) (reading "NUM_TightID_DEN_genTracks_pt_abseta" ?? old "NUM_TightID_DEN_genTracks")

				EfficienciesAndSF_BC_ID_SF_0p06.root #BC (personly created for iso<0.06 and need to update this is taken from lagecy samples)
                        	EfficienciesAndSF_DE_ID_SF_0p06.root #DE (personly created for iso<0.06 and need to update this is taken from lagecy samples)
                        	EfficienciesAndSF_F_ID_SF_0p06.root #F (personly created for iso<0.06 and need to update this is taken from lagecy samples)

                        ISO:
				RunBCDEF_SF_ISO_syst.root #BCDEF (remonnded but we are not using them for iso>0.2 and we retrun SF=1)

				EfficienciesAndSF_BC_ISO_SF_0p06.root #BC (personly created for iso<0.06 and need to update this is taken from lagecy samples)
                        	EfficienciesAndSF_DE_ISO_SF_0p06.root #DE (personly created for iso<0.06 and need to update this is taken from lagecy samples)
                        	EfficienciesAndSF_F_ISO_SF_0p06.root #F (personly created for iso<0.06 and need to update this is taken from lagecy samples)
 
	
                        TRI:
				EfficienciesAndSF_RunBtoF_Nov17Nov2017.root #BCDEF  (remonnded but we are not using them for iso>0.2 and we retrun SF=1)

				EfficienciesAndSF_BC_TRI_SF_0p06.root #BC (personly created for iso<0.06 and need to update this is taken from lagecy samples)
                        	EfficienciesAndSF_F_TRI_SF_0p06.root #DE (personly created for iso<0.06 and need to update this is taken from lagecy samples)
                        	EfficienciesAndSF_DE_TRI_SF_0p06.root #F (personly created for iso<0.06 and need to update this is taken from lagecy samples)



*	EgammaPog
        https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammaUL2016To2018#SFs_for_Electrons_UL_2017

                Input files:
                        Cut Based ID    Veto :
                                                /eos/cms/store/group/phys_egamma/SF-Repository/UL17/Electrons/Veto/egammaEffi.txt_EGM2D_Veto_UL17.root (recommonded) (histogram reading "EGamma_SF2D")
						scp /eos/cms/store/group/phys_egamma/SF-Repository/UL17/Electrons/Veto/passingVeto94XV2/egammaEffi.txt_EGM2D.root egammaEffi.txt_EGM2D_Veto_UL17.root


                        Cut Based ID    Tight :
                                                /eos/cms/store/group/phys_egamma/SF-Repository/UL17/Electrons/Tight/egammaEffi.txt_EGM2D_Tight_UL17.root
						scp /eos/cms/store/group/phys_egamma/SF-Repository/UL17/Electrons/Tight/passingTight94XV2/egammaEffi.txt_EGM2D.root egammaEffi.txt_EGM2D_Tight_UL17.root

                        Cut Based ID    Trigger :
		        	TRI_Tight    : ElectronSF/Run2_UL_TRI_SF_by_Mukund/UL2017_Tight.root # privatly produced trigger+TightID
                        	TRI_Veto'    : 'ElectronSF/Run2_UL_TRI_SF_by_Mukund/UL2017_Veto.root # privatlay produced Trigger_VetoID
 

                                                
*	LumiSectionsJSONFile
        https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideGoodLumiSectionsJSONFile (json file paths are taken from here)
        https://twiki.cern.ch/twiki/bin/view/CMS/TWikiLUM#CurRec (these recommadation seems old)
        https://twiki.cern.ch/twiki/bin/view/CMS/PdmVDataReprocessingUL2017 (RunNumbers)

		 Golden Json file : 2017 data: visit lxplus and it is located at /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt

## Recomdation UL18

*	pdmv
        https://twiki.cern.ch/twiki/bin/view/CMS/PdmV
        https://twiki.cern.ch/twiki/bin/view/CMS/PdmVRun2LegacyAnalysis 

		Global Tags:

    			Data: 106X_dataRun2_v35
    			MC 2018: 106X_upgrade2018_realistic_v16_L1v1
 
*	Btagging (RunIISummer19UL18)
	https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation106XUL18

		DeepJet=DeepFlavour
			reshaping_deepJet_106XUL18_v2.csv (problem because of chages applied) 	csv (iterativeFit shape correction)
			wp_deepJet_106XUL18_v2.csv	(problem because of chages applied) 	csv (WP only)
		
			DeepJet_106XUL18SF_V1p1.csv		csv (iterativeFit shape correction + fix wp)
			DeepJet_106XUL18SF_WPonly_V1p1.csv	csv (WP only)
	
			loose 	0.0490 
			medium 	0.2783 
			tight 	0.7100 
		For precision measurements on top physics, it is recommended to use the "mujets" scale factors, as statistically independent. 	 

*	jecTagsMC (Summer19UL18 V5)
        https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC

                inputfile: 
			Summer19UL18_V5_MC.tar.gz   
		GT: 
			106X_upgrade2018_realistic_v15_L1v1  
			(GT for Summer20UL samples is 106X_upgrade2018_realistic_v16_L1v1)

*	jecTagsData (Summer19UL18 )
        https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC

                        inputfiles:
                                Summer19UL18_RunA_V5_DATA.tar.gz
                                Summer19UL18_RunB_V5_DATA.tar.gz
                                Summer19UL18_RunC_V5_DATA.tar.gz
                                Summer19UL18_RunD_V5_DATA.tar.gz
                        GT :    
				106X_dataRun2_v33 (GT for Summer20UL samples is )

*	jerMC (Summer19UL18)
        https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution

                inputfile:
                       	Summer19UL18_JRV2_MC.tar.gz

*	jerData (Summer19UL18)
        https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution
	
                inputfile:
                        Summer19UL18_JRV2_DATA.tar.gz
			Please note that JER-SF files for data just contain unity and are not supposed to be used in the analyses. They are needed for internal consistence of the framework, i.e. currently CMSSW requires the JER-SF file also for data for compatibility. 

*       PUID
        https://twiki.cern.ch/twiki/bin/viewauth/CMS/PileupJetIDUL
                inputfile:
                        https://gitlab.cern.ch/cms-nanoAOD/jsonpog-integration/-/tree/master/POG/JME/2018_UL -> jmar.json.gz
                        correclation libraries are installed with python2 acc to https://cms-nanoaod.github.io/correctionlib/install.html#inside-cmssw


*	 MET
         https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETRun2Corrections#Implementation

                The jet collection used in Type-I corrections for PF MET is AK4PFchs jets with JES corrected Pt>15 GeV (using the L1L2L3 -L1 scheme). 
                The jets that are used to correct MET are also required to have electromagnetic energy fraction smaller than 0.9 and not to be overlapping with the pf muon candidate.
	

	 https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2#2018_2017_data_and_MC_UL

                MetFilter applied (UL2018) as OR comnibanation of flags listed below

                |filter                 |NanoAOD flag used                      | bit   |
                |:---------------------:|:-------------------------------------:|:------|
                |primary vertex filter  |Flag_goodVertices                      |   1    |
                |beam halo filter       |Flag_globalSuperTightHalo2016Filter    |   1    |
                |HBHE noise filter      |Flag_HBHENoiseFilter                   |   1    |
                |HBHEiso noise filter   |Flag_HBHENoiseIsoFilter                |   1    |
                |ECAL TP filter         |Flag_EcalDeadCellTriggerPrimitiveFilter|   1    |
                |Bad PF Muon Filter     |Flag_BadPFMuonFilter                   |   1    |
                |Bad PF Muon Dz Filter  |Flag_BadPFMuonDzFilter                 |   1    |
                |ee badSC noise filter  |Flag_eeBadScFilter                     |   1    |
                |ECAL bad calibration filter update |Flag_ecalBadCalibFilter    |   1    |

*	 Pileup weight / minimum bias x-sec (When using UltraLegacy samples)
         https://twiki.cern.ch/twiki/bin/view/CMS/PileupJSONFileforData

                inputfiles:
                        /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/PileUp/UltraLegacy/i

		In all those directories you will find (as indicated in the file name) histograms corresponding to the following values of the pp inelastic cross section:
                69200 ub (recommended central value), 66000 ub (central value - 4.6%), 72400 ub (central value + 4.6%), 80000 ub (conventional value used for the public plots,
                agreed with ATLAS years ago).

                (100 bins from PrelLum13TeV not reommended ) In Nanoaod tool we are using the following file where up down variation root files are add in subdiretories  :
			pufile_dataUL2018 = "/src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/PileupHistogram-UL2018-100bins_withVar.root"
			pufile_mcUL2018 = "/src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/mcPileupUL2018.root"
	
*	MuonPog
	https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonLegacy2018#Medium_pT_from_15_to_120_GeV

	 	Input files:
                        ID:
				RunABCD_SF_ID.root (required for ISO>0.2)


                        ISO:
				RunABCD_SF_ISO.root

                        TRI:
				EfficienciesAndSF_2018Data_BeforeMuonHLTUpdate.root  (remonnded but we are not using them for iso>0.2 and we retrun SF=1)
				EfficienciesAndSF_2018Data_AfterMuonHLTUpdate.root    (remonnded but we are not using them for iso>0.2 and we retrun SF=1)
				
				The lumi-weighted average of the two scale factors can be applied to the whole period:
    				run < 316361: 8950.82 \pb referred as before HLT update
				run >= 316361: 50789.75 \pb referred as after HLT update
    				brilcalc lumi -b "STABLE BEAMS" -u "/pb" --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_BRIL.json -i /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt 

*	EgammaPog
       	https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammaUL2016To2018#SFs_for_Electrons_UL_2018 

                Input files:
                        Cut Based ID    Veto :
                                                /eos/cms/store/group/phys_egamma/SF-Repository/UL18/Electrons/Veto/egammaEffi.txt_Ele_Veto_EGM2D.root (recommndetion) (histogram reading "EGamma_SF2D")
						scp /eos/cms/store/group/phys_egamma/SF-Repository/UL18/Electrons/Veto/passingVeto94XV2/egammaEffi.txt_EGM2D.root egammaEffi.txt_Ele_Veto_EGM2D.root

                        Cut Based ID    Tight :
                                                /eos/cms/store/group/phys_egamma/SF-Repository/UL18/Electrons/Tight/egammaEffi.txt_Ele_Tight_EGM2D.root
						scp /eos/cms/store/group/phys_egamma/SF-Repository/UL18/Electrons/Tight/passingTight94XV2/egammaEffi.txt_EGM2D.root egammaEffi.txt_Ele_Tight_EGM2D.root

                        Cut Based ID    Trigger :
                                                TRI_Tight : ElectronSF/Run2_UL_TRI_SF_by_Mukund/UL2018_Tight.root # privatly producec Tigger+TightID
						TRI_Veto  : ElectronSF/Run2_UL_TRI_SF_by_Mukund/UL2018_Veto.root # privatly produced Trigger_vetoID

*	LumiSectionsJSONFile
        https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideGoodLumiSectionsJSONFile (json file paths are taken from here)
        https://twiki.cern.ch/twiki/bin/view/CMS/TWikiLUM#CurRec (these recommadation seems old)
        https://twiki.cern.ch/twiki/bin/view/CMS/PdmVDataReprocessingUL2018 (RunNumbers)
		
		 Golden Json file : 2018 data: visit lxplus and it is located at /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt 


## Specific check while swiching b/w year data and mc processing 

*      	Btagging evoluvation

     		#EfficiencyModule.py (we are not using it now this was for fix wp only and now we moved to iterativeFit)
     		1. Check the efficiency are calculted with the recommaded lose, midium and tight criteria  at "https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation"
		2. check we are using correct Module producer while creating efficiency file "EfficiencyConstr_2016"

* 	Tree crab

     		#MainModule.py
     		1. chose the right module Run "Year" as function
		2. Look at the correctorlly written dleverd luminocity "TotalLumi" for the lepton sale factor
		
		#scaleFactor.py
		1. Check the paths for the efficiency file are correctly provided "mu_fpath" and "el_fpath"

	 	#btagSFProducer.py
	 	1. check the recomandaion for the csv file at "https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation" if reco chage then put new csv file in data and update module with new file name
	 	2. check the Module producer we are going to run "btagSF2016"
 
		#puWeightProducer.py
		1.check you runing right module "puWeight_2016()"

		#jmeModule
		1.check the JEC recomation at "https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC" if it reco change the then put the new tar ball in data and chage the "jecTagsMC and jecTagsDATA" in jetmetHelperRun2.py
		2.if JEC reco chage the check the "globalTag" in  jetmetUncertainties.py
		3.check the JER recomandation at "https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution#Run2_JER_uncertainty_correlation" if the reco chaged the put the new taball in data and chage the "jerTagsMC" in jetmetHelperRun2.py

## Get the data set name for minitree submission
* Use "check_crab_status.py" file to check the crab status for all the submitted dataset
* Save the output of the "check_crab_status.py" in .txt or .py file
* Run "find_phy3_dataset.py" with saved file as a input. This will find and print the array of phys3 datset names.

## Invalidation of wrongly produced dataset
* Get the  array of the wrongly produced dataset as mension above
* copy and pest the the array in "invalidate.py" file as datasets = [your array of datasets] and run it with python. 
