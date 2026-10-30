from Get_Weighted_Hist_only_sys_EWK import get_Weight_sys_EWK
from Get_Weighted_Hist_only_sys_top import get_Weight_sys_top
from Propagate_rate_Uncertainity import propagate_rate_uncertainity

def process_bjet_systematics(lep,
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
    Process B jet weight systematics.
    """
    print("\n  ================    B jet weight systemtics   ==============\n")
    jes_missing = [jesAbsoluteScale, jesFlavorQCD, jesRelativeStatFSR]
    jes_spliting = ["jes","jesAbsoluteStat",'jesAbsoluteMPFBias','jesFragmentation','jesSinglePionECAL','jesSinglePionHCAL','jesTimePtEta','jesRelativeJEREC1',
                    'jesRelativeJEREC2','jesRelativeJERHF','jesRelativePtBB','jesRelativePtEC1','jesRelativePtEC2','jesRelativePtHF','jesRelativeBal','jesRelativeSample',
                    'jesRelativeFSR','jesRelativeStatEC','jesRelativeStatHF','jesPileUpDataMC','jesPileUpPtRef','jesPileUpPtBB','jesPileUpPtEC1','jesPileUpPtEC2','jesPileUpPtHF']
    sys_bWeight = ["bWeight_lf", "bWeight_hf", "bWeight_cferr1", "bWeight_cferr2",
                   "bWeight_lfstats1", "bWeight_lfstats2", "bWeight_hfstats1", "bWeight_hfstats2", "bWeight_jes", "bWeight_jes_variation_up", "bWeight_jes_variation_down"]
    sys_variation = ["Up", "Down"]
    for sys in sys_bWeight:
        for variation_no, variation in enumerate(sys_variation):
            print("\n #################  ", sys + variation, "############## \n")
            MCcut_sys_bWeight = (
                "Xsec_wgt*LHEWeightSign*puWeight*" + lep +
                "SF*L1PreFiringWeight_Nom*" + sys + variation +
                "*bJetPUJetID_SF*lJetPUJetID_SF*(dR_bJet_lJet>0.4)"
                "*(mtwMass>50)*mtw_weight_50GeVCut"
            )
            topSig_hists_syst, topBkg_hists_syst = get_Weight_sys_top(
                lep=lep,
                year=year,
                Variable=Variable,
                channels_weight_sys=channels_top_only,
                MCcut=MCcut_sys_bWeight,
                DNNcut=DNNCut,
                hist_sys_name="_" + lep + sys,
                File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,
                Fpaths_DNN_apply=Fpaths_DNN_apply,
                top_sig_cons=top_sig_cons,
                top_bkg_cons=top_bkg_cons
            )
            topSig_hists_syst.SetName("top_sig_1725" + tag + gt_or_lt_tag + sys + variation)
            topBkg_hists_syst.SetName("top_bkg_1725" + tag + gt_or_lt_tag + sys + variation)
            hist_to_return.append(topSig_hists_syst.Clone())
            hist_to_return.append(topBkg_hists_syst.Clone())
            del topSig_hists_syst, topBkg_hists_syst

            signal_EWK_hist_sys = get_Weight_sys_EWK(
                lep=lep,
                year=year,
                Variable=Variable,
                channels_weight_sys=channels_EWK_only,
                MCcut = MCcut_sys_bWeight,
                DNNcut = "(t_ch_CAsi>=0.7) ", 
                hist_sys_name=f"_{lep}{sys}",
                File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,
                Fpaths_DNN_apply=Fpaths_DNN_apply,
                EWK_cons=EWK_bkg_cons
            )
            signal_region_EWK_Integral = signal_EWK_hist_sys.Integral()

            Control_EWK_hists_syst = get_Weight_sys_EWK(
                lep=lep,
                year=year,
                Variable=Variable,
                channels_weight_sys=channels_EWK_only,
                MCcut = MCcut_sys_bWeight,
                DNNcut = "(t_ch_CAsi>=0.3) ", 
                hist_sys_name=f"_{lep}{sys}",
                File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,
                Fpaths_DNN_apply=Fpaths_DNN_apply,
                EWK_cons=EWK_bkg_cons
            )
            sys_EWK_Integral_control = Control_EWK_hists_syst.Integral()

            EWK_hists_syst = Control_EWK_hists_syst.Clone()
            EWK_hists_syst.SetName(f"EWK_bkg{tag}{gt_or_lt_tag}{sys}{variation}")
            EWK_hists_syst.Scale(signal_region_EWK_Integral/sys_EWK_Integral_control)
            del sys_EWK_Integral_control
            propagate_rate_uncertainity(EWK_hists_syst, EWK_bkg_cons)
            hist_to_return.append(EWK_hists_syst.Clone())
            del EWK_hists_syst
    del sys_bWeight, sys_variation
