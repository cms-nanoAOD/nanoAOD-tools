from Get_Weighted_Hist_only_sys_EWK import get_Weight_sys_EWK
from Get_Weighted_Hist_only_sys_top import get_Weight_sys_top
from Propagate_rate_Uncertainity import propagate_rate_uncertainity

def process_lep_SF_systematics(lep,
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
    Process lepton scale factor (SF) weight systematics.
    """
    if(lep=="mu"):
            lepton = "Muon"
    elif(lep=="el"):
            lepton = "Electron"
    print(lepton)

    print("\n  ================    lepton SF weight systemtics   ==============\n")
    sys_lep_SF = {
        "el": ["SF_Iso_IDUp", "SF_Iso_IDDown", "SF_Iso_TrigUp", "SF_Iso_TrigDown"],
            #"SF_Veto_IDUp", "SF_Veto_IDDown", "SF_Veto_TrigUp", "SF_Veto_TrigDown"],
        "mu": ["SF_IsoUp", "SF_IsoDown", "SF_Iso_IDUp", "SF_Iso_IDDown", "SF_Iso_TrigUp", "SF_Iso_TrigDown"]
    }
    for sys in sys_lep_SF[lep]:
        print("\n #################  ", sys, "############## \n")
        MCcut_sys_lep_SF = (
            "Xsec_wgt*LHEWeightSign*puWeight*" + lepton + "_" + sys +
            "*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF"
            "*(dR_bJet_lJet>0.4)*(mtwMass>50)*mtw_weight_50GeVCut"
        )
        topSig_hists_syst, topBkg_hists_syst = get_Weight_sys_top(
            lep=lep,
            year=year,
            Variable=Variable,
            channels_weight_sys=channels_top_only,
            MCcut=MCcut_sys_lep_SF,
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

        signal_EWK_hists_syst = get_Weight_sys_EWK(
                lep=lep,
                year=year,
                Variable=Variable,
                channels_weight_sys=channels_EWK_only,
                MCcut = MCcut_sys_lep_SF,
                DNNcut = "(t_ch_CAsi>=0.7) ", 
                hist_sys_name=f"_{lep}{sys}",
                File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,
                Fpaths_DNN_apply=Fpaths_DNN_apply,
                EWK_cons=EWK_bkg_cons
        )
        signal_region_EWK_Integral = signal_EWK_hists_syst.Integral()

        Control_EWK_hists_syst = get_Weight_sys_EWK(
                lep=lep,
                year=year,
                Variable=Variable,
                channels_weight_sys=channels_EWK_only,
                MCcut = MCcut_sys_lep_SF,
                DNNcut = "(t_ch_CAsi>=0.3) ", 
                hist_sys_name=f"_{lep}{sys}",
                File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,
                Fpaths_DNN_apply=Fpaths_DNN_apply,
                EWK_cons=EWK_bkg_cons
        )
        sys_EWK_Integral_control = Control_EWK_hists_syst.Integral()

        EWK_hists_syst= Control_EWK_hists_syst.Clone()
        EWK_hists_syst.SetName(f"EWK_bkg{tag}{gt_or_lt_tag}{sys}")
        EWK_hists_syst.Scale(signal_region_EWK_Integral/sys_EWK_Integral_control)
        del sys_EWK_Integral_control
        propagate_rate_uncertainity(EWK_hists_syst, EWK_bkg_cons)
        hist_to_return.append(EWK_hists_syst.Clone())
        del EWK_hists_syst