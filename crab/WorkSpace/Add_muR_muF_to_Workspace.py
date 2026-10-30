from Get_Weighted_Hist_only_sys_EWK import get_Weight_sys_EWK
from Get_Weighted_Hist_only_sys_top import get_Weight_sys_top
from Propagate_rate_Uncertainity import propagate_rate_uncertainity

def process_muR_muF_systematics(lep,
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
    Process mur MuF weight systematics.
    """

    print("\n  ================    MUR mUF weight systemtics   ==============\n")
    sys_muR_muF = ['muR', 'muF']
    sys_variations = ["Up", "Down"]  # This list is defined but not used further.
    for variation in sys_variations:
        for variation_no, sys in enumerate(sys_muR_muF):
            print(f"\n #################  {sys} {variation}  ############## \n")
            MCcut_sys_muR_muF = (f"Xsec_wgt*LHEWeightSign*puWeight*{lep}SF*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF*{sys}_{variation}"
                +f"*(dR_bJet_lJet>0.4)*(mtwMass>50)*mtw_weight_50GeVCut"
            )
            topSig_hists_syst, topBkg_hists_syst = get_Weight_sys_top(
                lep=lep,
                year=year,
                Variable=Variable,
                channels_weight_sys=channels_top_only,
                MCcut=MCcut_sys_muR_muF,
                DNNcut=DNNCut,
                hist_sys_name=f"_ {lep}{sys}{variation}",
                File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,
                Fpaths_DNN_apply=Fpaths_DNN_apply,
                top_sig_cons=top_sig_cons,
                top_bkg_cons=top_bkg_cons
            )
            topSig_hists_syst.SetName(f"top_sig_1725{tag}{gt_or_lt_tag}{sys}{variation}")
            topBkg_hists_syst.SetName(f"top_bkg_1725{tag}{gt_or_lt_tag}{sys}{variation}")
            hist_to_return.append(topSig_hists_syst.Clone())
            hist_to_return.append(topBkg_hists_syst.Clone())
            del topSig_hists_syst, topBkg_hists_syst

            signal_EWK_hist_sys = get_Weight_sys_EWK(
                lep=lep,
                year=year,
                Variable=Variable,
                channels_weight_sys=channels_EWK_only,
                MCcut = MCcut_sys_muR_muF,
                DNNcut = "(t_ch_CAsi>=0.7) ", 
                hist_sys_name=f"_{lep}{sys}{variation}",
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
                MCcut = MCcut_sys_muR_muF,
                DNNcut = "(t_ch_CAsi>=0.3) ", 
                hist_sys_name=f"_{lep}{sys}{variation}",
                File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,
                Fpaths_DNN_apply=Fpaths_DNN_apply,
                EWK_cons=EWK_bkg_cons
            )
            control_region_sys_EWK_Integral = Control_EWK_hist_sys.Integral()

            EWK_hists_syst = Control_EWK_hist_sys.Clone()
            EWK_hists_syst.SetName(f"EWK_bkg{tag}{gt_or_lt_tag}{sys}{variation}")
            EWK_hists_syst.Scale(signal_region_EWK_Integral/control_region_sys_EWK_Integral)
            del control_region_sys_EWK_Integral
            propagate_rate_uncertainity(EWK_hists_syst, EWK_bkg_cons)
            hist_to_return.append(EWK_hists_syst.Clone())

    print(f"{DNNCut = }")
    del sys_muR_muF, sys_variations
