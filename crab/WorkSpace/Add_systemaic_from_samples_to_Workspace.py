from Get_Histogram_after_DNN_cuts import get_histogram_with_DNN_cut
from Propagate_rate_Uncertainity import propagate_rate_uncertainity
import ROOT as rt

def process_systematics_from_diffrent_samples(
                                lep,
                                 year,
                                 yearDir,
                                 Variable,
                                 MCcut,
                                 DNNCut,
                                 File_with_mtwMassFit_weight_Iso,
                                 Fpaths_DNN_apply,
                                 hist_corr_assig,      # dictionary already filled elsewhere (used for adding histograms)
                                 X_axies,              # x-axis title for the histogram
                                 tag,
                                 gt_or_lt_tag,
                                 top_sig_cons,         # constraint for top signal uncertainty propagation
                                 top_bkg_cons,         # constraint for top background uncertainty propagation
                                 Nominal_sig_Normalization,
                                 Nominal_topbkg_Normalization,
                                 hist_to_return        # list to which the resulting histograms will be appended
                                 ):
    """
    Process the systematic variations from diffrent samples.
    """
    if Variable == "TMath::Log(topMass)":
        Variable = "lntopMass"

    systs = ["erdON","Gluonmove","QCDinspired","TuneCP5up","TuneCP5down"]
    sys_Names = ["erdON","Gluonmove","QCDinspired","TuneCP5up","TuneCP5down"]

    # For hdamp systematics, the channels are split into two groups:

    channels_systematic_samples = ['Tchannel', 'Tbarchannel', 'ttbar_SemiLeptonic', 'ttbar_FullyLeptonic']
    channels_normal = [ 'tw_antitop', 'tw_top', 'Schannel']
    
    QCDcut_same_sys = ""
    Datacut_same_sys = ""

    hist_corr_assig_sys = {}
    hist_wron_assig_sys = {}


    for sys,sys_name in zip(systs, sys_Names):
        sample_files,sample_DNN_files = {},{}
        for channel in channels_systematic_samples:
            sample_files[channel] = f"/feynman/home/dphp/mk277705/work/RUN2_UL/Minitree_corr_bweight_with_mtwMassFit_Scale/{yearDir[year]}/2J1T1/sys_N_Alt/{year}_{channel}_{sys}_Apply_all_{lep}.root"
            sample_DNN_files[channel] = f"/feynman/home/dphp/mk277705/work/RUN2_UL/DNN_outputs_without_mtwCut_corr_bweight/{yearDir[year]}/2J1T1/Apply_all/sys_N_Alt/{year}_{channel}_{sys}_Apply_all_{lep}.root"
        print("\n #################  ", sys, "############## \n")
        
        # First, get histograms for the hdamp channels
        hists_corr_sys, hists_wron_sys = get_histogram_with_DNN_cut(
            lep=lep, 
            year=year, 
            Variable=Variable, 
            channels=channels_systematic_samples,
            MCcut=MCcut, 
            QCDcut=QCDcut_same_sys, 
            Datacut=Datacut_same_sys,
            DNNcut=DNNCut, 
            Filepaths_with_QCDWeight=sample_files, 
            Fpaths_DNN_score=sample_DNN_files
        )
        
        for channel_no, channel in enumerate(channels_systematic_samples):
            hist_corr_assig_sys[channel] = hists_corr_sys[channel_no].Clone()
            hist_wron_assig_sys[channel] = hists_wron_sys[channel_no].Clone()
        del hists_corr_sys, hists_wron_sys

        # Next, get histograms for the remaining channels
        hists_corr_sys, hists_wron_sys = get_histogram_with_DNN_cut(
            lep=lep, 
            year=year, 
            Variable=Variable, 
            channels=channels_normal,
            MCcut=MCcut, 
            QCDcut=QCDcut_same_sys, 
            Datacut=Datacut_same_sys,
            DNNcut=DNNCut, 
            Filepaths_with_QCDWeight=File_with_mtwMassFit_weight_Iso, 
            Fpaths_DNN_score=Fpaths_DNN_apply
        )
        for channel_no, channel in enumerate(channels_normal):
            hist_corr_assig_sys[channel] = hists_corr_sys[channel_no].Clone()
            hist_wron_assig_sys[channel] = hists_wron_sys[channel_no].Clone()
        del hists_corr_sys, hists_wron_sys
        
        # Process the top signal for hdamp systematic
        corr_assig_sig_sys = hist_corr_assig_sys["Tchannel"].Clone()
        corr_assig_sig_sys.Add(hist_corr_assig["Tbarchannel"])

        wron_assig_sig_sys = hist_wron_assig_sys["Tchannel"].Clone()
        wron_assig_sig_sys.Add(hist_wron_assig_sys["Tbarchannel"])

        corr_assig_sig_sys.Print()
        corr_assig_sig_sys.SetLineColor(rt.kRed)
        corr_assig_sig_sys.SetLineWidth(2)
        corr_assig_sig_sys.GetXaxis().SetTitle(X_axies)
        corr_assig_sig_sys.SetName("top_sig_1725" + tag + gt_or_lt_tag + sys_name)
        propagate_rate_uncertainity(corr_assig_sig_sys, top_sig_cons)
        propagate_rate_uncertainity(wron_assig_sig_sys, top_sig_cons)

        # Process the top background for hdamp systematic
        corr_assig_top_bkg_sys = hist_corr_assig_sys['tw_top'].Clone()
        wron_assig_top_bkg_sys = hist_wron_assig_sys['tw_top'].Clone()
        for channel in ['tw_antitop', 'Schannel', 'ttbar_SemiLeptonic', 'ttbar_FullyLeptonic']:
            corr_assig_top_bkg_sys.Add(hist_corr_assig_sys[channel])
            wron_assig_top_bkg_sys.Add(hist_wron_assig_sys[channel])
        
        wron_assig_top_bkg_sys.SetLineColor(rt.kOrange-1)
        wron_assig_top_bkg_sys.SetLineWidth(2)

        propagate_rate_uncertainity(corr_assig_top_bkg_sys, top_bkg_cons)
        propagate_rate_uncertainity(wron_assig_top_bkg_sys, top_bkg_cons)

        corr_assig_sig_sys.Add(corr_assig_top_bkg_sys)
        corr_assig_sig_sys.Scale(Nominal_sig_Normalization/corr_assig_sig_sys.Integral())
        hist_to_return.append(corr_assig_sig_sys)

        wron_assig_top_bkg_sys.Add(wron_assig_top_bkg_sys)
        print(f'{Nominal_topbkg_Normalization  = }')
        print(f'sys {wron_assig_top_bkg_sys.Integral()  = }')
        wron_assig_top_bkg_sys.Scale(Nominal_topbkg_Normalization/wron_assig_top_bkg_sys.Integral())
        print(f'sys {wron_assig_top_bkg_sys.Integral()  = }')

        wron_assig_top_bkg_sys.SetName("top_bkg_1725" + tag + gt_or_lt_tag + sys_name)
        hist_to_return.append(wron_assig_top_bkg_sys)
    
    # Clean up temporary dictionaries
    del hist_corr_assig_sys, hist_wron_assig_sys
    