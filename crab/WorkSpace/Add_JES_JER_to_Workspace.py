from Get_Weighted_Hist_only_sys_EWK import get_Weight_sys_EWK
from Get_Weighted_Hist_only_sys_top import get_Weight_sys_top
from Propagate_rate_Uncertainity import propagate_rate_uncertainity

def process_JER_JES_systematics(
                                lep,
                                year,
                                Variable,
                                MCcut,
                                DNNCut,
                                tag, 
                                gt_or_lt_tag,
                                File_with_mtwMassFit_weight_Iso, 
                                Fpaths_DNN_apply,
                                signal_region_EWK_Integral,
                                top_sig_cons,
                                top_bkg_cons,
                                EWK_bkg_cons,
                                Control_EWK_hist,
                                channels_top_only,
                                channels_EWK_only, 
                                hist_to_return
    ):
    print(f"{lep = }")
    # JES Systematic Variations
    sys_JES = ["jesAbsoluteStat",'jesAbsoluteMPFBias','jesFragmentation','jesSinglePionECAL','jesSinglePionHCAL',
                'jesTimePtEta','jesRelativeJEREC1','jesRelativeJEREC2','jesRelativeJERHF','jesRelativePtBB','jesRelativePtEC1',
                'jesRelativePtEC2','jesRelativePtHF','jesRelativeBal','jesRelativeSample','jesRelativeFSR','jesRelativeStatEC',
                'jesRelativeStatHF','jesPileUpDataMC','jesPileUpPtRef','jesPileUpPtBB','jesPileUpPtEC1','jesPileUpPtEC2',
                'jesPileUpPtHF',"jesAbsoluteScale", "jesFlavorQCD", "jesRelativeStatFSR"]
    
    sys_variation = ["Up", "Down"]
    Fpaths_sys_samples_top, Fpaths_sys_samples_EWK = {}, {}

    for channel in channels_top_only:
        Fpaths_sys_samples_top[channel] = f"/feynman/home/dphp/mk277705/work/RUN2_UL/Minitree_corr_bweight/JER_JES_Trees/JERtree_{year}_{channel}_2J1T1_{lep}.root"
    
    for channel in channels_EWK_only:
        Fpaths_sys_samples_EWK[channel] = f"/feynman/home/dphp/mk277705/work/RUN2_UL/Minitree_corr_bweight/JER_JES_Trees/JERtree_{year}_{channel}_2J1T1_{lep}.root"
    
    for sys in sys_JES:
        for variation in sys_variation:
            print("\n #################  ", sys + variation, "############## \n")
            MCcut_jes_sys = MCcut.replace("*bWeight*",f"*bWeight_{sys}_{variation}*")
            print(f"{MCcut = }")

            if Variable == "TMath::Log(topMass)":
                Variable = f"lntopMass_{sys}{variation}"

            topSig_hists_JES_syst, topBkg_hists_JES_syst = get_Weight_sys_top(
                lep=lep,
                year=year,
                Variable=Variable,
                channels_weight_sys=channels_top_only,
                MCcut=MCcut_jes_sys,
                DNNcut=DNNCut,
                hist_sys_name=f"_{lep}{sys}", 
                File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso, 
                Fpaths_DNN_apply=Fpaths_DNN_apply,
                top_sig_cons=top_sig_cons,
                top_bkg_cons=top_bkg_cons,
                Fpaths_sys_samples=Fpaths_sys_samples_top
            )

            topSig_hists_JES_syst.SetName(f"top_sig_1725{tag}{gt_or_lt_tag}{sys}{variation}")
            topBkg_hists_JES_syst.SetName(f"top_bkg_1725{tag}{gt_or_lt_tag}{sys}{variation}")
            hist_to_return.extend([topSig_hists_JES_syst.Clone(), topBkg_hists_JES_syst.Clone()])

            del topSig_hists_JES_syst, topBkg_hists_JES_syst

            signal_EWK_hists_syst_JES = get_Weight_sys_EWK(
                lep=lep,
                year=year,
                Variable=Variable,
                channels_weight_sys=channels_EWK_only,
                MCcut = MCcut_jes_sys,
                DNNcut = "(t_ch_CAsi>=0.7) ", 
                hist_sys_name=f"_{lep}{sys}",
                File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,
                Fpaths_DNN_apply=Fpaths_DNN_apply,
                EWK_cons=EWK_bkg_cons,
                Fpaths_sys_samples=Fpaths_sys_samples_EWK
            )

            signal_region_EWK_Integral = signal_EWK_hists_syst_JES.Integral()

            Control_EWK_hists_syst_JES = get_Weight_sys_EWK(
                lep=lep,
                year=year,
                Variable=Variable,
                channels_weight_sys=channels_EWK_only,
                MCcut = MCcut_jes_sys,
                DNNcut = "(t_ch_CAsi>=0.3) ", 
                hist_sys_name=f"_{lep}{sys}",
                File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,
                Fpaths_DNN_apply=Fpaths_DNN_apply,
                EWK_cons=EWK_bkg_cons,
                Fpaths_sys_samples=Fpaths_sys_samples_EWK
            )
            sys_EWK_jes_Integral_control = Control_EWK_hists_syst_JES.Integral()

            EWK_hists_syst_JES = Control_EWK_hists_syst_JES.Clone()
            EWK_hists_syst_JES.SetName(f"EWK_bkg{tag}{gt_or_lt_tag}{sys}{variation}")
            EWK_hists_syst_JES.Scale(signal_region_EWK_Integral/sys_EWK_jes_Integral_control)
            del sys_EWK_jes_Integral_control
            propagate_rate_uncertainity(EWK_hists_syst_JES, EWK_bkg_cons)
            hist_to_return.append(EWK_hists_syst_JES.Clone())

            del EWK_hists_syst_JES
            if "lntopMass_" in Variable:
                Variable = "TMath::Log(topMass)"
    del sys_JES


    # # JES Systematic Variations
    # sys_JES = ['jesAbsoluteScale',"jesFlavorQCD","jesRelativeStatFSR"] 
    
    # sys_variation = ["Up", "Down"]
    # Fpaths_sys_samples_top, Fpaths_sys_samples_EWK = {}, {}

    # for channel in channels_top_only:
    #     Fpaths_sys_samples_top[channel] = f"/feynman/home/dphp/mk277705/work/RUN2_UL/Minitree_corr_bweight/JER_JES_Trees/JERtree_{year}_{channel}_2J1T1_{lep}_v2.root"
    
    # for channel in channels_EWK_only:
    #     Fpaths_sys_samples_EWK[channel] = f"/feynman/home/dphp/mk277705/work/RUN2_UL/Minitree_corr_bweight/JER_JES_Trees/JERtree_{year}_{channel}_2J1T1_{lep}_v2.root"
    
    # for sys in sys_JES:
    #     for variation in sys_variation:
    #         print("\n #################  ", sys + variation, "############## \n")
    #         print(f"{MCcut = }")

    #         if Variable == "TMath::Log(topMass)":
    #             Variable = f"lntopMass_{sys}{variation}"

    #         topSig_hists_JES_syst, topBkg_hists_JES_syst = get_Weight_sys_top(
    #             lep=lep,
    #             year=year,
    #             Variable=Variable,
    #             channels_weight_sys=channels_top_only,
    #             MCcut=MCcut,
    #             DNNcut=DNNCut,
    #             hist_sys_name=f"_{lep}{sys}", 
    #             File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso, 
    #             Fpaths_DNN_apply=Fpaths_DNN_apply,
    #             top_sig_cons=top_sig_cons,
    #             top_bkg_cons=top_bkg_cons,
    #             Fpaths_sys_samples=Fpaths_sys_samples_top
    #         )

    #         topSig_hists_JES_syst.SetName(f"top_sig_1725{tag}{gt_or_lt_tag}{sys}{variation}")
    #         topBkg_hists_JES_syst.SetName(f"top_bkg_1725{tag}{gt_or_lt_tag}{sys}{variation}")
    #         hist_to_return.extend([topSig_hists_JES_syst.Clone(), topBkg_hists_JES_syst.Clone()])

    #         del topSig_hists_JES_syst, topBkg_hists_JES_syst

    #         signal_EWK_hists_syst_JES = get_Weight_sys_EWK(
    #             lep=lep,
    #             year=year,
    #             Variable=Variable,
    #             channels_weight_sys=channels_EWK_only,
    #             MCcut = MCcut,
    #             DNNcut = "(t_ch_CAsi>=0.7) ", 
    #             hist_sys_name=f"_{lep}{sys}",
    #             File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,
    #             Fpaths_DNN_apply=Fpaths_DNN_apply,
    #             EWK_cons=EWK_bkg_cons,
    #             Fpaths_sys_samples=Fpaths_sys_samples_EWK
    #         )

    #         signal_region_EWK_Integral = signal_EWK_hists_syst_JES.Integral()

    #         Control_EWK_hists_syst_JES = get_Weight_sys_EWK(
    #             lep=lep,
    #             year=year,
    #             Variable=Variable,
    #             channels_weight_sys=channels_EWK_only,
    #             MCcut = MCcut,
    #             DNNcut = "(t_ch_CAsi>=0.3) ", 
    #             hist_sys_name=f"_{lep}{sys}",
    #             File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,
    #             Fpaths_DNN_apply=Fpaths_DNN_apply,
    #             EWK_cons=EWK_bkg_cons,
    #             Fpaths_sys_samples=Fpaths_sys_samples_EWK
    #         )
    #         sys_EWK_jes_Integral_control = Control_EWK_hists_syst_JES.Integral()

    #         EWK_hists_syst_JES = Control_EWK_hists_syst_JES.Clone()
    #         EWK_hists_syst_JES.SetName(f"EWK_bkg{tag}{gt_or_lt_tag}{sys}{variation}")
    #         EWK_hists_syst_JES.Scale(signal_region_EWK_Integral/sys_EWK_jes_Integral_control)
    #         del sys_EWK_jes_Integral_control
    #         propagate_rate_uncertainity(EWK_hists_syst_JES, EWK_bkg_cons)
    #         hist_to_return.append(EWK_hists_syst_JES.Clone())

    #         del EWK_hists_syst_JES
    #         if "lntopMass_" in Variable:
    #             Variable = "TMath::Log(topMass)"
    # del sys_JES

    # JER Systematic Variations
    sys_JER = ['jer0', 'jer1', 'jer2', 'jer3',
                'jer4', 'jer5']

    Fpaths_sys_samples_top, Fpaths_sys_samples_EWK = {}, {}
    for channel in channels_top_only:
        Fpaths_sys_samples_top[channel] = f"/feynman/home/dphp/mk277705/work/RUN2_UL/Minitree_corr_bweight/JER_JES_Trees/JERtree_{year}_{channel}_2J1T1_{lep}.root"
    for channel in channels_EWK_only:
        Fpaths_sys_samples_EWK[channel] = f"/feynman/home/dphp/mk277705/work/RUN2_UL/Minitree_corr_bweight/JER_JES_Trees/JERtree_{year}_{channel}_2J1T1_{lep}.root"

    for sys in sys_JER:
        for variation in sys_variation:
            print("\n #################  ", sys + variation, "############## \n")
            print(f"{MCcut = }")

            if Variable == "TMath::Log(topMass)":
                Variable = f"lntopMass_{sys}{variation}"

            topSig_hists_JER_syst, topBkg_hists_JER_syst = get_Weight_sys_top(
                lep=lep,
                year=year,
                Variable=Variable,
                channels_weight_sys=channels_top_only,
                MCcut=MCcut,
                DNNcut=DNNCut,
                hist_sys_name=f"_{lep}{sys}",
                File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,
                Fpaths_DNN_apply=Fpaths_DNN_apply,
                top_sig_cons=top_sig_cons,
                top_bkg_cons=top_bkg_cons,
                Fpaths_sys_samples=Fpaths_sys_samples_top
            )

            topSig_hists_JER_syst.SetName(f"top_sig_1725{tag}{gt_or_lt_tag}{sys}{variation}")
            topBkg_hists_JER_syst.SetName(f"top_bkg_1725{tag}{gt_or_lt_tag}{sys}{variation}")
            hist_to_return.extend([topSig_hists_JER_syst.Clone(), topBkg_hists_JER_syst.Clone()])

            del topSig_hists_JER_syst, topBkg_hists_JER_syst
            print(f'{MCcut = }')
            signal_EWK_hists_syst_JER = get_Weight_sys_EWK(
                lep=lep,
                year=year,
                Variable=Variable,
                channels_weight_sys=channels_EWK_only,
                MCcut = MCcut,
                DNNcut = "(t_ch_CAsi>=0.7) ", 
                hist_sys_name=f"_{lep}{sys}",
                File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,
                Fpaths_DNN_apply=Fpaths_DNN_apply,
                EWK_cons=EWK_bkg_cons,
                Fpaths_sys_samples=Fpaths_sys_samples_EWK
            )
            signal_region_EWK_Integral = signal_EWK_hists_syst_JER.Integral()

            Control_EWK_hists_syst_JER = get_Weight_sys_EWK(
                lep=lep,
                year=year,
                Variable=Variable,
                channels_weight_sys=channels_EWK_only,
                MCcut = MCcut,
                DNNcut = "(t_ch_CAsi>=0.3) ", 
                hist_sys_name=f"_{lep}{sys}",
                File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,
                Fpaths_DNN_apply=Fpaths_DNN_apply,
                EWK_cons=EWK_bkg_cons,
                Fpaths_sys_samples=Fpaths_sys_samples_EWK
            )
            sys_EWK_Integral_control = Control_EWK_hists_syst_JER.Integral()

            EWK_hists_syst_JER = Control_EWK_hists_syst_JER.Clone()
            EWK_hists_syst_JER.SetName(f"EWK_bkg{tag}{gt_or_lt_tag}{sys}{variation}")
            EWK_hists_syst_JER.Scale(signal_region_EWK_Integral/sys_EWK_Integral_control)
            del sys_EWK_Integral_control
            propagate_rate_uncertainity(EWK_hists_syst_JER, EWK_bkg_cons)
            hist_to_return.append(EWK_hists_syst_JER.Clone())

            del EWK_hists_syst_JER
            if "lntopMass_" in Variable:
                Variable = "TMath::Log(topMass)"
    del sys_JER
