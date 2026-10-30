# cmseenv needed

#python Create_DNNFit_Workspace_input_file.py -y UL2016postVFP -l mu -v t_ch_CAsi -DC ">=0.0"
#python Create_DNNFit_Workspace_input_file.py -y UL2016postVFP -l el -v t_ch_CAsi -DC ">=0.0"

#python Create_DNNFit_Workspace_input_file.py -y UL2016preVFP -l mu  -v t_ch_CAsi -DC ">=0.0"
#python Create_DNNFit_Workspace_input_file.py -y UL2016preVFP -l el  -v t_ch_CAsi -DC ">=0.0"

#python Create_DNNFit_Workspace_input_file.py -y UL2017 -l mu  -v t_ch_CAsi -DC ">=0.0"
#python Create_DNNFit_Workspace_input_file.py -y UL2017 -l el  -v t_ch_CAsi -DC ">=0.0"

#python3 Create_DNNFit_Workspace_input_file.py -y UL2018 -l mu -v t_ch_CAsi -DC ">=0.0"
#python Create_DNNFit_Workspace_input_file.py -y UL2018 -l el -v t_ch_CAsi -DC ">=0.0"


#python Create_mtopFit_Workspace_input_file.py -y UL2018 -l mu -DC "(t_ch_CAsi>=0.3)" -v  lntopMass
#python Create_mtopFit_Workspace_input_file.py -y UL2018 -l el -DC "(t_ch_CAsi>=0.3)" -v  lntopMass

#python Create_mtopFit_Workspace_input_file.py -y UL2018 -l mu -DC "(t_ch_CAsi>=0.5)*(t_ch_CAsi<0.7)" -v  lntopMass
#python Create_mtopFit_Workspace_input_file.py -y UL2018 -l el -DC "(t_ch_CAsi>=0.5)*(t_ch_CAsi<0.7)" -v  lntopMass

#python3 Create_mtopFit_Workspace_input_file.py -y UL2018 -l mu -DC "(t_ch_CAsi>=0.7) " -v  lntopMass -f ~/work/HiggsCombine/CMSSW_12_3_4/src/Combine_Run2/fitDiagnostics_M1725_DNNfit_UL2018.root # -Alt  -samesys
#python3 Create_mtopFit_Workspace_input_file.py -y UL2018 -l el -DC "(t_ch_CAsi>=0.7) " -v  lntopMass -f ~/work/HiggsCombine/CMSSW_12_3_4/src/Combine_Run2/fitDiagnostics_M1725_DNNfit_UL2018.root # -Alt  -samesys
#python3 Create_mtopFit_Workspace_input_file.py -y UL2018 -l mu -DC "(t_ch_CAsi>=0.3) " -v  lntopMass -f ~/work/HiggsCombine/CMSSW_12_3_4/src/Combine_Run2/fitDiagnostics_M1725_DNNfit_UL2018.root # -Alt  -samesys
#python3 Create_mtopFit_Workspace_input_file.py -y UL2018 -l el -DC "(t_ch_CAsi>=0.3) " -v  lntopMass -f ~/work/HiggsCombine/CMSSW_12_3_4/src/Combine_Run2/fitDiagnostics_M1725_DNNfit_UL2018.root # -Alt  -samesys


#python Create_mtopFit_Workspace_input_file.py -y UL2018 -l mu -DC "(t_ch_CAsi>=0.5)*(t_ch_CAsi<0.7) " -v  lntopMass -f /home/mikumar/t3store/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/fitDiagnostics_M1725_DNNfit_UL2018.root # -Alt -f /home/mikumar/t3store/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/ROOT/fitDiagnostics_M1725_DNNfit_Run2.root -samesys -Alt
#python Create_mtopFit_Workspace_input_file.py -y UL2018 -l mu -DC "(t_ch_CAsi>=0.3)" -v  lntopMass -f /home/mikumar/t3store/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/ROOT/fitDiagnostics_M1725_DNNfit_UL2018.root #-f /home/mikumar/t3store/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/ROOT/fitDiagnostics_M1725_DNNfit_Run2.root
#python Create_mtopFit_Workspace_input_file.py -y UL2018 -l mu -DC "(t_ch_CAsi>=0.7)" -v  lntopMass -f /home/mikumar/t3store/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/ROOT/fitDiagnostics_M1725_DNNfit_Run2.root
#python validation_stackplot_fromhistfiles.py -y UL2018 -l mu -v  lntopMass -f1 /home/mikumar/t3store/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/WorkSpace/Hist_for_workspace/Combine_Input_topMass_histograms_UL2018_mu_gteq0p7.root 

#python Create_mtopFit_Workspace_input_file.py -y UL2018 -l el -DC "(t_ch_CAsi>=0.7)" -v  lntopMass  -f /home/mikumar/t3store/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/ROOT/fitDiagnostics_M1725_DNNfit_UL2018.root #-f /home/mikumar/t3store/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/ROOT/fitDiagnostics_M1725_DNNfit_Run2.root -samesys -Alt
#python Create_mtopFit_Workspace_input_file.py -y UL2018 -l el -DC "(t_ch_CAsi>=0.3)" -v  lntopMass -f /home/mikumar/t3store/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/ROOT/fitDiagnostics_M1725_DNNfit_UL2018.root #-f /home/mikumar/t3store/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/ROOT/fitDiagnostics_M1725_DNNfit_Run2.root
#python Create_mtopFit_Workspace_input_file.py -y UL2018 -l el -DC "<0.7" -v  lntopMass -f /home/mikumar/t3store/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/ROOT/fitDiagnostics_M1725_DNNfit_Run2.root
#python validation_stackplot_fromhistfiles.py -y UL2018 -l el -v  lntopMass -f1 /home/mikumar/t3store/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/WorkSpace/Hist_for_workspace/Combine_Input_topMass_histograms_UL2018_el_gteq0p7.root  




python3 Create_mtopFit_Workspace_input_file.py -y UL2018 -l mu -DC "(t_ch_CAsi>=0.7) " -v  lntopMass  -Alt  -allsys # -samesys 
python3 Create_mtopFit_Workspace_input_file.py -y UL2018 -l el -DC "(t_ch_CAsi>=0.7) " -v  lntopMass  -Alt  -allsys # -samesys
#python3 Create_mtopFit_Workspace_input_file.py -y UL2018 -l mu -DC "(t_ch_CAsi>=0.5)*(t_ch_CAsi<0.7) " -v  lntopMass  -Alt  # -samesys
#python3 Create_mtopFit_Workspace_input_file.py -y UL2018 -l el -DC "(t_ch_CAsi>=0.5)*(t_ch_CAsi<0.7) " -v  lntopMass  -Alt  # -samesys
#python3 Create_mtopFit_Workspace_input_file.py -y UL2018 -l mu -DC "(t_ch_CAsi>=0.3) " -v  lntopMass
#python3 Create_mtopFit_Workspace_input_file.py -y UL2018 -l el -DC "(t_ch_CAsi>=0.3) " -v  lntopMass 


#python3 Create_mtopFit_Workspace_input_file.py -y UL2017 -l mu -DC "(t_ch_CAsi>=0.7) " -v  lntopMass  -Alt  -allsys # -samesys
#python3 Create_mtopFit_Workspace_input_file.py -y UL2017 -l el -DC "(t_ch_CAsi>=0.7) " -v  lntopMass  -Alt  -allsys # -samesys
#python3 Create_mtopFit_Workspace_input_file.py -y UL2017 -l mu -DC "(t_ch_CAsi>=0.5)*(t_ch_CAsi<0.7) " -v  lntopMass  -Alt  # -samesys
#python3 Create_mtopFit_Workspace_input_file.py -y UL2017 -l el -DC "(t_ch_CAsi>=0.5)*(t_ch_CAsi<0.7) " -v  lntopMass  -Alt  # -samesys
#python3 Create_mtopFit_Workspace_input_file.py -y UL2017 -l mu -DC "(t_ch_CAsi>=0.3) " -v  lntopMass
#python3 Create_mtopFit_Workspace_input_file.py -y UL2017 -l el -DC "(t_ch_CAsi>=0.3) " -v  lntopMass

#python3 Create_mtopFit_Workspace_input_file.py -y UL2016preVFP -l mu -DC "(t_ch_CAsi>=0.7) " -v  lntopMass  -Alt  -allsys # -samesys
#python3 Create_mtopFit_Workspace_input_file.py -y UL2016preVFP -l el -DC "(t_ch_CAsi>=0.7) " -v  lntopMass  -Alt  -allsys # -samesys
#python3 Create_mtopFit_Workspace_input_file.py -y UL2016preVFP -l mu -DC "(t_ch_CAsi>=0.5)*(t_ch_CAsi<0.7) " -v  lntopMass  -Alt  # -samesys
#python3 Create_mtopFit_Workspace_input_file.py -y UL2016preVFP -l el -DC "(t_ch_CAsi>=0.5)*(t_ch_CAsi<0.7) " -v  lntopMass  -Alt  # -samesys
#python3 Create_mtopFit_Workspace_input_file.py -y UL2016preVFP -l mu -DC "(t_ch_CAsi>=0.3) " -v  lntopMass
#python3 Create_mtopFit_Workspace_input_file.py -y UL2016preVFP -l el -DC "(t_ch_CAsi>=0.3) " -v  lntopMass

#python3 Create_mtopFit_Workspace_input_file.py -y UL2016postVFP -l mu -DC "(t_ch_CAsi>=0.7) " -v  lntopMass  -Alt  -allsys # -samesys
#python3 Create_mtopFit_Workspace_input_file.py -y UL2016postVFP -l el -DC "(t_ch_CAsi>=0.7) " -v  lntopMass  -Alt  -allsys # -samesys
#python3 Create_mtopFit_Workspace_input_file.py -y UL2016postVFP -l mu -DC "(t_ch_CAsi>=0.5)*(t_ch_CAsi<0.7) " -v  lntopMass  -Alt  # -samesys
#python3 Create_mtopFit_Workspace_input_file.py -y UL2016postVFP -l el -DC "(t_ch_CAsi>=0.5)*(t_ch_CAsi<0.7) " -v  lntopMass  -Alt  # -samesys
#python3 Create_mtopFit_Workspace_input_file.py -y UL2016postVFP -l mu -DC "(t_ch_CAsi>=0.3) " -v  lntopMass 
#python3 Create_mtopFit_Workspace_input_file.py -y UL2016postVFP -l el -DC "(t_ch_CAsi>=0.3) " -v  lntopMass 



#python3 Create_mtopFit_Workspace_input_file_roodataset.py -y UL2018 -l mu -DC "(t_ch_CAsi>=0.7)" -v  lntopMass  # # -Alt  -samesys

#python Create_mtopFit_Workspace_input_file.py -y UL2017 -l mu  -DC "(t_ch_CAsi>=0.7)" -v  lntopMass -f /home/mikumar/t3store/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/ROOT/fitDiagnostics_M1725_DNNfit_Run2.root
#python Create_mtopFit_Workspace_input_file.py -y UL2017 -l mu  -DC "(t_ch_CAsi>=0.3)" -v  lntopMass -f /home/mikumar/t3store/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/ROOT/fitDiagnostics_M1725_DNNfit_Run2.root
#python Create_mtopFit_Workspace_input_file.py -y UL2017 -l mu  -DC "(t_ch_CAsi<0.7)" -v  lntopMass -f /home/mikumar/t3store/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/ROOT/fitDiagnostics_M1725_DNNfit_Run2.root

#python validation_stackplot_fromhistfiles.py -y UL2017 -l mu -v  lntopMass -f1 /home/mikumar/t3store/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/WorkSpace/Hist_for_workspace/Combine_Input_lntopMass_histograms_UL2017_mu.root 

#python Create_mtopFit_Workspace_input_file.py -y UL2017 -l el  -DC ">=0.7" -v  lntopMass -f /home/mikumar/t3store/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/ROOT/fitDiagnostics_M1725_DNNfit_Run2.root
#python Create_mtopFit_Workspace_input_file.py -y UL2017 -l el  -DC ">=0.3" -v  lntopMass -f /home/mikumar/t3store/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/ROOT/fitDiagnostics_M1725_DNNfit_Run2.root
#python Create_mtopFit_Workspace_input_file.py -y UL2017 -l el  -DC "<0.7" -v  lntopMass -f /home/mikumar/t3store/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/ROOT/fitDiagnostics_M1725_DNNfit_Run2.root
#python validation_stackplot_fromhistfiles.py -y UL2017 -l el  -v  lntopMass -f1 /home/mikumar/t3store/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/WorkSpace/Hist_for_workspace/Combine_Input_lntopMass_histograms_UL2017_el.root 

#python Create_mtopFit_Workspace_input_file.py -y UL2016preVFP -l mu  -DC ">=0.7" -v  lntopMass -f /home/mikumar/t3store/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/ROOT/fitDiagnostics_M1725_DNNfit_Run2.root
#python Create_mtopFit_Workspace_input_file.py -y UL2016preVFP -l mu  -DC ">=0.3" -v  lntopMass -f /home/mikumar/t3store/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/ROOT/fitDiagnostics_M1725_DNNfit_Run2.root
#python Create_mtopFit_Workspace_input_file.py -y UL2016preVFP -l mu  -DC "<0.7" -v  lntopMass -f /home/mikumar/t3store/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/ROOT/fitDiagnostics_M1725_DNNfit_Run2.root
#python validation_stackplot_fromhistfiles.py -y UL2016preVFP -l mu -v  lntopMass -f1 /home/mikumar/t3store/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/WorkSpace/Hist_for_workspace/Combine_Input_lntopMass_histograms_UL2016preVFP_mu.root

#python Create_mtopFit_Workspace_input_file.py -y UL2016preVFP -l el  -DC ">=0.7" -v  lntopMass -f /home/mikumar/t3store/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/ROOT/fitDiagnostics_M1725_DNNfit_Run2.root
#python Create_mtopFit_Workspace_input_file.py -y UL2016preVFP -l el  -DC ">=0.3" -v  lntopMass -f /home/mikumar/t3store/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/ROOT/fitDiagnostics_M1725_DNNfit_Run2.root
#python Create_mtopFit_Workspace_input_file.py -y UL2016preVFP -l el  -DC "<0.7" -v  lntopMass -f /home/mikumar/t3store/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/ROOT/fitDiagnostics_M1725_DNNfit_Run2.root
#python validation_stackplot_fromhistfiles.py -y UL2016preVFP -l el -v  lntopMass -f1 /home/mikumar/t3store/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/WorkSpace/Hist_for_workspace/Combine_Input_lntopMass_histograms_UL2016preVFP_el.root

#python Create_mtopFit_Workspace_input_file.py -y UL2016postVFP -l mu  -DC ">=0.7" -v  lntopMass -f /home/mikumar/t3store/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/ROOT/fitDiagnostics_M1725_DNNfit_Run2.root
#python Create_mtopFit_Workspace_input_file.py -y UL2016postVFP -l mu  -DC ">=0.3" -v  lntopMass -f /home/mikumar/t3store/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/ROOT/fitDiagnostics_M1725_DNNfit_Run2.root
#python Create_mtopFit_Workspace_input_file.py -y UL2016postVFP -l mu  -DC "<0.7" -v  lntopMass -f /home/mikumar/t3store/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/ROOT/fitDiagnostics_M1725_DNNfit_Run2.root
#python validation_stackplot_fromhistfiles.py -y UL2016postVFP -l mu -v  lntopMass -f1 /home/mikumar/t3store/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/WorkSpace/Hist_for_workspace/Combine_Input_lntopMass_histograms_UL2016postVFP_mu.root

#python Create_mtopFit_Workspace_input_file.py -y UL2016postVFP -l el  -DC ">=0.7" -v  lntopMass -f /home/mikumar/t3store/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/ROOT/fitDiagnostics_M1725_DNNfit_Run2.root
#python Create_mtopFit_Workspace_input_file.py -y UL2016postVFP -l el  -DC ">=0.3" -v  lntopMass -f /home/mikumar/t3store/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/ROOT/fitDiagnostics_M1725_DNNfit_Run2.root
#python Create_mtopFit_Workspace_input_file.py -y UL2016postVFP -l el  -DC "<0.7" -v  lntopMass -f /home/mikumar/t3store/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/ROOT/fitDiagnostics_M1725_DNNfit_Run2.root
#python validation_stackplot_fromhistfiles.py -y UL2016postVFP -l el -v  lntopMass -f1 /home/mikumar/t3store/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/WorkSpace/Hist_for_workspace/Combine_Input_lntopMass_histograms_UL2016postVFP_el.root

