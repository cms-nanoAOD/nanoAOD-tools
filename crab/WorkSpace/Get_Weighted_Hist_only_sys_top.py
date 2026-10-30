import ROOT as rt
from Get_Histogram_after_DNN_cuts import get_histogram_with_DNN_cut
from Propagate_rate_Uncertainity import propagate_rate_uncertainity
def get_Weight_sys_top(lep,year,Variable,channels_weight_sys,MCcut,DNNcut,hist_sys_name,File_with_mtwMassFit_weight_Iso,Fpaths_DNN_apply,top_sig_cons,top_bkg_cons,Fpaths_sys_samples=None):
    QCDcut=""
    Datacut=""
    if(Fpaths_sys_samples==None):
        if(Variable=="TMath::Log(topMass)"): Variable="lntopMass"
        hists_corr_weight_sys,hists_wron_weight_sys =  get_histogram_with_DNN_cut(
            lep=lep,
            year=year,
            Variable=Variable,
            channels = channels_weight_sys,
            MCcut = MCcut ,
            QCDcut = QCDcut, 
            Datacut = Datacut, 
            DNNcut = DNNcut,
            Filepaths_with_QCDWeight = File_with_mtwMassFit_weight_Iso,
            Fpaths_DNN_score = Fpaths_DNN_apply,
            Fpaths_sys_samples = Fpaths_sys_samples
        )
        if(Variable=="lntopMass"):   Variable="TMath::Log(topMass)"
    else:
        hists_corr_weight_sys,hists_wron_weight_sys =  get_histogram_with_DNN_cut(
            lep=lep,
            year=year,
            Variable=Variable,
            channels = channels_weight_sys,
            MCcut = MCcut ,
            QCDcut = QCDcut, 
            Datacut = Datacut, 
            DNNcut = DNNcut,
            Filepaths_with_QCDWeight = File_with_mtwMassFit_weight_Iso,
            Fpaths_DNN_score = Fpaths_DNN_apply,
            Fpaths_sys_samples = Fpaths_sys_samples
        )
    hist_corr_assig_weight_sys = {}
    hist_wron_assig_weight_sys = {}
    for channel_no,channel in enumerate(channels_weight_sys):
        hist_corr_assig_weight_sys[channel] = hists_corr_weight_sys[channel_no].Clone()
        hist_wron_assig_weight_sys[channel] = hists_wron_weight_sys[channel_no].Clone()
    del hists_corr_weight_sys
    del hists_wron_weight_sys

    top_sig_weight_sys = hist_corr_assig_weight_sys["Tchannel"].Clone(); top_sig_weight_sys.Add(hist_corr_assig_weight_sys["Tbarchannel"]);

    top_bkg_weight_sys = hist_wron_assig_weight_sys["Tchannel"].Clone(); top_bkg_weight_sys.Add(hist_wron_assig_weight_sys["Tbarchannel"]);

    propagate_rate_uncertainity(top_sig_weight_sys, top_sig_cons)
    propagate_rate_uncertainity(top_bkg_weight_sys, top_sig_cons)

    top_bkg_weight_sys_corr = hist_corr_assig_weight_sys['tw_top'].Clone();
    top_bkg_weight_sys_wron = hist_wron_assig_weight_sys['tw_top'].Clone();
    for channel in ['tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic']:
        top_bkg_weight_sys_corr.Add(hist_corr_assig_weight_sys[channel])
        top_bkg_weight_sys_wron.Add(hist_wron_assig_weight_sys[channel])

    propagate_rate_uncertainity(top_bkg_weight_sys_corr, top_bkg_cons)
    propagate_rate_uncertainity(top_bkg_weight_sys_wron, top_bkg_cons)

    top_sig_weight_sys.Add(top_bkg_weight_sys_corr)
    top_bkg_weight_sys.Add(top_bkg_weight_sys_wron)

    top_sig_weight_sys.Print()
    top_bkg_weight_sys.Print()

    #hist_ST_Sig.GetYaxis().SetTitle("Fraction of events")
    can_ST = rt.TCanvas("can_ST","can_ST",600,600)
    rt.gStyle.SetOptStat(0)
    can_ST.cd()

    #pad1 = rt.TPad('pad1', 'pad1', 0.0, 0.18, 1.0, 0.990683)
    pad1 = rt.TPad('pad1', 'pad1', 0.0, 0.0, 1.0, 1.0)
    pad1.SetBottomMargin(0.089)
    pad1.SetTicky()
    pad1.SetTickx()
    pad1.Draw()
    pad1.cd()
    #hist_ST_Sig.GetYaxis().CenterTitle(1)
    top_sig_weight_sys.GetYaxis().SetTitleOffset(1.4)
    top_sig_weight_sys.GetYaxis().SetTitleSize(0.035)
    top_sig_weight_sys.GetYaxis().SetLabelSize(0.030)

    top_sig_weight_sys.SetLineColor(rt.kRed)
    top_bkg_weight_sys.SetLineColor(rt.kCyan+1)

    top_sig_weight_sys.Draw("hist")
    top_bkg_weight_sys.Draw("hist;same")

    can_ST.Update()
    fix_range = pad1.GetUymax()+0.15
    top_sig_weight_sys.SetMaximum(fix_range)
    top_sig_weight_sys.SetMinimum(0.001)

    legend_ST = rt.TLegend(0.60193646, 0.4548435, 0.7593552, 0.79026143)
    legend_ST.SetBorderSize(1)
    legend_ST.SetTextSize(0.045)
    legend_ST.SetLineColor(0)
    legend_ST.SetLineStyle(1)
    legend_ST.SetLineWidth(1)
    legend_ST.SetFillColor(0)
    legend_ST.SetFillStyle(1001)
    legend_ST.AddEntry(top_sig_weight_sys, "sig", "l")
    legend_ST.AddEntry(top_bkg_weight_sys, "bkg", "l")
    legend_ST.Draw()
    can_ST.Update()


    png = f"./Plots/{Variable}_{lep}_{year}.png"
    pdf = f"./Plots/{Variable}_{lep}_{year}.pdf"
    cpp = f"./Plots/{Variable}_{lep}_{year}.C"
    can_ST.SaveAs(png)
    can_ST.SaveAs(pdf)

    return top_sig_weight_sys,top_bkg_weight_sys