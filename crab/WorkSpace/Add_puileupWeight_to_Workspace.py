from Get_Weighted_Hist_only_sys_EWK import get_Weight_sys_EWK
from Get_Weighted_Hist_only_sys_top import get_Weight_sys_top
from Propagate_rate_Uncertainity import propagate_rate_uncertainity

def process_pileupweight_systematics(lep,
                                year,
                                Variable,
                                DNNCut,
                                tag,
                                gt_or_lt_tag,
                                File_with_mtwMassFit_weight_Iso,
                                Fpaths_DNN_apply,
                                signal_region_EWK_Integral,
                                top_sig_cons,
                                top_bkg_cons,
                                EWK_bkg_cons,
                                channels_top_only,
                                channels_EWK_only,
                                hist_to_return):
    """
    Process pileup weight systematics.
    """

    print("\n  ================    Pileup weight systemtics   ==============\n")
    sys_pileup = ["puWeightUp", "puWeightDown"]
    sys_variation = ["Up", "Down"]  # This list is defined but not used further.
    for variation_no, sys in enumerate(sys_pileup):
        print("\n #################  ", sys, "############## \n")
        MCcut_sys_pileup = (
            "Xsec_wgt*LHEWeightSign*" + sys + "*" + lep +
            "SF*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF"
            "*(dR_bJet_lJet>0.4)*(mtwMass>50)*mtw_weight_50GeVCut"
        )
        topSig_hists_syst, topBkg_hists_syst = get_Weight_sys_top(
            lep=lep,
            year=year,
            Variable=Variable,
            channels_weight_sys=channels_top_only,
            MCcut=MCcut_sys_pileup,
            DNNcut=DNNCut,
            hist_sys_name="_" + lep + sys,
            File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,
            Fpaths_DNN_apply=Fpaths_DNN_apply,
            top_sig_cons=top_sig_cons,
            top_bkg_cons=top_bkg_cons
        )
        topSig_hists_syst.SetName("top_sig_1725" + tag + gt_or_lt_tag + sys)
        topBkg_hists_syst.SetName("top_bkg_1725" + tag + gt_or_lt_tag + sys)
        hist_to_return.append(topSig_hists_syst.Clone())
        hist_to_return.append(topBkg_hists_syst.Clone())
        del topSig_hists_syst, topBkg_hists_syst

        # EWK_hists_syst = get_Weight_sys_EWK(
        #     lep=lep,
        #     year=year,
        #     Variable=Variable,
        #     channels_weight_sys=channels_EWK_only,
        #     MCcut=MCcut_sys_pileup,
        #     DNNcut=DNNCut,
        #     hist_sys_name=f"_{lep}{sys}",
        #     File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,
        #     Fpaths_DNN_apply=Fpaths_DNN_apply,
        #     EWK_cons=EWK_bkg_cons
        # )
        # sys_EWK_Integral = EWK_hists_syst.Integral()
        # del EWK_hists_syst

        signal_EWK_hist_sys = get_Weight_sys_EWK(
            lep=lep,
            year=year,
            Variable=Variable,
            channels_weight_sys=channels_EWK_only,
            MCcut = MCcut_sys_pileup,
            DNNcut = "(t_ch_CAsi>=0.7) ", 
            hist_sys_name=f"_{lep}{sys}",
            File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,
            Fpaths_DNN_apply=Fpaths_DNN_apply,
            EWK_cons=EWK_bkg_cons
        )
        signal_region_EWK_Integral = signal_EWK_hist_sys.Integral()

        Control_EWK_hist_sys = get_Weight_sys_EWK(
            lep=lep,
            year=year,
            Variable=Variable,
            channels_weight_sys=channels_EWK_only,
            MCcut = MCcut_sys_pileup,
            DNNcut = "(t_ch_CAsi>=0.3) ", 
            hist_sys_name=f"_{lep}{sys}",
            File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,
            Fpaths_DNN_apply=Fpaths_DNN_apply,
            EWK_cons=EWK_bkg_cons
        )
        control_region_sys_EWK_Integral = Control_EWK_hist_sys.Integral()

        EWK_hists_syst = Control_EWK_hist_sys.Clone()
        EWK_hists_syst.SetName("EWK_bkg" + tag + gt_or_lt_tag + sys)
        EWK_hists_syst.Scale(signal_region_EWK_Integral/control_region_sys_EWK_Integral)
        del control_region_sys_EWK_Integral
        propagate_rate_uncertainity(EWK_hists_syst, EWK_bkg_cons)
        hist_to_return.append(EWK_hists_syst.Clone())

    print(f"{DNNCut = }")
    del sys_pileup, sys_variation
