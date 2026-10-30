from Get_Histogram_after_DNN_cuts import get_histogram_with_DNN_cut
from Propagate_rate_Uncertainity import propagate_rate_uncertainity
import ROOT as rt

def process_hdamp_ISR_FSR_systematics(lep,
                                 year,
                                 Variable,
                                 MCcut,
                                 DNNCut,
                                 File_with_mtwMassFit_weight_Iso,
                                 Fpaths_DNN_apply,
                                 Fpaths_orignal_minitree, # these original files are requied since PSweights are not stored while saveing the mtwfit weights
                                 hist_corr_assig,      # dictionary already filled elsewhere (used for adding histograms)
                                 X_axies,              # x-axis title for the histogram
                                 tag,
                                 gt_or_lt_tag,
                                 top_sig_cons,         # constraint for top signal uncertainty propagation
                                 top_bkg_cons,         # constraint for top background uncertainty propagation
                                 hist_to_return        # list to which the resulting histograms will be appended
                                 ):
    """
    Process the “same minitree” systematic variations.
    """
    # ==========================
    # Part 1: PSWeight systematics (ISR/FSR)
    # ==========================
    print("creating histogram for the sys samples from same minitree .............\n")
    
    # Define alternative systematics names (PSWeight indices)
    Alt_same_sys = ["PSWeight[0]", "PSWeight[2]", "PSWeight[1]", "PSWeight[3]"]
    Alt_same_sys_Name = ["ISRUp", "ISRDown", "FSRUp", "FSRDown"]

    channels_same_sys = ['Tchannel', 'Tbarchannel', 'tw_antitop', 'tw_top', 'Schannel', 'ttbar_SemiLeptonic', 'ttbar_FullyLeptonic']

    # These cuts are not used here; set as empty strings.
    QCDcut_same_sys = ""
    Datacut_same_sys = ""

    # Create dictionaries to hold histograms for this systematic
    hist_corr_assig_same_sys = {}
    hist_wron_assig_same_sys = {}

    # If the original variable is the log of topMass, change its name for this processing.
    if Variable == "TMath::Log(topMass)":
        Variable = "lntopMass"

    # Loop over the alternative systematics (PSWeight variations)
    for sys, sys_name in zip(Alt_same_sys, Alt_same_sys_Name):
        print("\n #################  ", sys, "############## \n")
        MCcut_same_sys = MCcut + "*" + sys
        # Get histograms with DNN cut applied for all channels in channels_same_sys
        hists_corr_same_sys, hists_wron_same_sys = get_histogram_with_DNN_cut(
            lep = lep, 
            year = year, 
            Variable=Variable, 
            channels = channels_same_sys  ,
            MCcut=MCcut_same_sys, 
            QCDcut = QCDcut_same_sys, 
            Datacut = Datacut_same_sys,
            DNNcut = DNNCut, 
            Filepaths_with_QCDWeight = File_with_mtwMassFit_weight_Iso, 
            Fpaths_DNN_score = Fpaths_DNN_apply,
            Fpaths_sys_samples = Fpaths_orignal_minitree
        )

        for channel_no, channel in enumerate(channels_same_sys):
            print(channel, " same sys")
            # Clone histograms so that original objects are not overwritten.
            hist_corr_assig_same_sys[channel] = hists_corr_same_sys[channel_no].Clone()
            hist_wron_assig_same_sys[channel] = hists_wron_same_sys[channel_no].Clone()
        
        # Free temporary histogram lists
        del hists_corr_same_sys, hists_wron_same_sys

        # Process the top signal: add histograms for "Tchannel" and "Tbarchannel"
        top_sig_same_sys = hist_corr_assig_same_sys["Tchannel"].Clone()
        top_sig_same_sys.Add(hist_corr_assig["Tbarchannel"])
        top_sig_same_sys.Print()
        top_sig_same_sys.SetLineColor(rt.kRed)
        top_sig_same_sys.SetLineWidth(2)
        top_sig_same_sys.GetXaxis().SetTitle(X_axies)
        top_sig_same_sys.SetName("top_sig_1725" + tag + gt_or_lt_tag + sys_name)
        propagate_rate_uncertainity(top_sig_same_sys, top_sig_cons)
        print("print after uncertinty propagation 2")
        top_sig_same_sys.Print()
        hist_to_return.append(top_sig_same_sys)
        
        # Process the mis-assigned (wrong) top background for single-top:
        missreco_single_top_bkg_same_sys = hist_wron_assig_same_sys["Tchannel"].Clone()
        missreco_single_top_bkg_same_sys.Add(hist_wron_assig_same_sys["Tbarchannel"])
        propagate_rate_uncertainity(missreco_single_top_bkg_same_sys, top_sig_cons)

        # Process the top background: start with the "tw_top" channel
        top_bkg_same_sys = hist_corr_assig_same_sys['tw_top'].Clone()
        missrecotop_bkg_same_sys = hist_wron_assig_same_sys['tw_top'].Clone()
        # Add contributions from the other channels
        for channel in ['tw_antitop', 'Schannel', 'ttbar_SemiLeptonic', 'ttbar_FullyLeptonic']:
            top_bkg_same_sys.Add(hist_corr_assig_same_sys[channel])
            missrecotop_bkg_same_sys.Add(hist_wron_assig_same_sys[channel])

        missrecotop_bkg_same_sys.SetLineColor(rt.kOrange-1)
        missrecotop_bkg_same_sys.SetLineWidth(2)

        propagate_rate_uncertainity(top_bkg_same_sys, top_bkg_cons)
        propagate_rate_uncertainity(missrecotop_bkg_same_sys, top_bkg_cons)

        # Add the background contribution to the top signal histogram and combine the mis-assigned parts
        top_sig_same_sys.Add(top_bkg_same_sys)
        missrecotop_bkg_same_sys.Add(missreco_single_top_bkg_same_sys)

        missrecotop_bkg_same_sys.SetName("top_bkg_1725" + tag + gt_or_lt_tag + sys_name)
        hist_to_return.append(missrecotop_bkg_same_sys)
    
    # Clean up the temporary dictionaries
    del hist_corr_assig_same_sys, hist_wron_assig_same_sys



    # ==========================
    # Part 2: hdamp systematics
    # ==========================



    print("\ncreating histogram for the ==hdamp== sys samples from same minitree .............\n")
    
    Alt_same_sys = ["hdamp_Up", "hdamp_Down"]
    Alt_same_sys_Name = ["hdampUp", "hdampDown"]

    # For hdamp systematics, the channels are split into two groups:

    channels_singale_top = ['Tchannel', 'Tbarchannel', 'tw_antitop', 'tw_top', 'Schannel']
    channels_hdamp_sys = ['ttbar_SemiLeptonic', 'ttbar_FullyLeptonic']
    
    QCDcut_same_sys = ""
    Datacut_same_sys = ""

    hist_corr_assig_same_sys = {}
    hist_wron_assig_same_sys = {}


    #for sys in Alt_same_sys:
    for sys, sys_name in zip(Alt_same_sys, Alt_same_sys_Name):
        print("\n #################  ", sys, "############## \n")
        MCcut_same_sys = MCcut + "*" + sys

        # First, get histograms for the hdamp channels
        hists_corr_same_sys, hists_wron_same_sys = get_histogram_with_DNN_cut(
            lep=lep, 
            year=year, 
            Variable=Variable, 
            channels=channels_hdamp_sys,
            MCcut=MCcut_same_sys, 
            QCDcut=QCDcut_same_sys, 
            Datacut=Datacut_same_sys,
            DNNcut=DNNCut, 
            Filepaths_with_QCDWeight=File_with_mtwMassFit_weight_Iso, 
            Fpaths_DNN_score=Fpaths_DNN_apply
        )
        for channel_no, channel in enumerate(channels_hdamp_sys):
            print(channel, " same sys")
            hist_corr_assig_same_sys[channel] = hists_corr_same_sys[channel_no].Clone()
            hist_wron_assig_same_sys[channel] = hists_wron_same_sys[channel_no].Clone()
        del hists_corr_same_sys, hists_wron_same_sys

        # Next, get histograms for the remaining channels
        hists_corr_same_sys, hists_wron_same_sys = get_histogram_with_DNN_cut(
            lep=lep, 
            year=year, 
            Variable=Variable, 
            channels=channels_singale_top,
            MCcut=MCcut, 
            QCDcut=QCDcut_same_sys, 
            Datacut=Datacut_same_sys,
            DNNcut=DNNCut, 
            Filepaths_with_QCDWeight=File_with_mtwMassFit_weight_Iso, 
            Fpaths_DNN_score=Fpaths_DNN_apply
        )
        for channel_no, channel in enumerate(channels_singale_top):
            print(channel, " same sys")
            hist_corr_assig_same_sys[channel] = hists_corr_same_sys[channel_no].Clone()
            hist_wron_assig_same_sys[channel] = hists_wron_same_sys[channel_no].Clone()
        del hists_corr_same_sys, hists_wron_same_sys

        # Process the top signal for hdamp systematic
        top_sig_same_sys = hist_corr_assig_same_sys["Tchannel"].Clone()
        top_sig_same_sys.Add(hist_corr_assig["Tbarchannel"])
        top_sig_same_sys.Print()
        top_sig_same_sys.SetLineColor(rt.kRed)
        top_sig_same_sys.SetLineWidth(2)
        top_sig_same_sys.GetXaxis().SetTitle(X_axies)
        top_sig_same_sys.SetName("top_sig_1725" + tag + gt_or_lt_tag + sys_name)
        propagate_rate_uncertainity(top_sig_same_sys, top_sig_cons)
        print("print after uncertinty propagation 3")
        top_sig_same_sys.Print()
        
        
        # Process the mis-assigned part for the hdamp systematic
        missreco_single_top_bkg_same_sys = hist_wron_assig_same_sys["Tchannel"].Clone()
        missreco_single_top_bkg_same_sys.Add(hist_wron_assig_same_sys["Tbarchannel"])
        propagate_rate_uncertainity(missreco_single_top_bkg_same_sys, top_sig_cons)

        # Process the top background for hdamp systematic
        top_bkg_same_sys = hist_corr_assig_same_sys['tw_top'].Clone()
        missrecotop_bkg_same_sys = hist_wron_assig_same_sys['tw_top'].Clone()
        for channel in ['tw_antitop', 'Schannel', 'ttbar_SemiLeptonic', 'ttbar_FullyLeptonic']:
            top_bkg_same_sys.Add(hist_corr_assig_same_sys[channel])
            missrecotop_bkg_same_sys.Add(hist_wron_assig_same_sys[channel])
        
        missrecotop_bkg_same_sys.SetLineColor(rt.kOrange-1)
        missrecotop_bkg_same_sys.SetLineWidth(2)

        propagate_rate_uncertainity(top_bkg_same_sys, top_bkg_cons)

        propagate_rate_uncertainity(missrecotop_bkg_same_sys, top_bkg_cons)

        top_sig_same_sys.Add(top_bkg_same_sys)
        hist_to_return.append(top_sig_same_sys)

        missrecotop_bkg_same_sys.Add(missreco_single_top_bkg_same_sys)

        missrecotop_bkg_same_sys.SetName("top_bkg_1725" + tag + gt_or_lt_tag + sys_name)
        hist_to_return.append(missrecotop_bkg_same_sys)
    
    # Clean up temporary dictionaries
    del hist_corr_assig_same_sys, hist_wron_assig_same_sys