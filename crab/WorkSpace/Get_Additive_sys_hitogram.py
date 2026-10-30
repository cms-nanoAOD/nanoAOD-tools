import ROOT as rt
import numpy as np
from Histogram_discribtions import get_histogram_distciption 
from Get_Histogram_after_DNN_cuts import get_histogram_with_DNN_cut
from Get_Nomi_histogram_Integral import Nomi_QCD_NoNQCD_Integral,Nomi_QCD_Integral,Nomi_NoNQCD_Integral 
from Overflow_N_Underflowbin import DrawOverflow_N_DrawUnderflow
from QCD_Non_QCD_Normalization import *

def propagate_rate_uncertainity(hist, uncert):
    for i in range(1,hist.GetXaxis().GetNbins()+1):
        if hist.GetBinContent(i) != 0:
            hist.SetBinError(i, hist.GetBinContent(i) * uncert * 0.01)


def Get_additive_sys_samples(
                                lep="mu",
                                year="UL2017",
                                Variable="lntopMass",
                                MCcut = "Xsec_wgt*LHEWeightSign*puWeight*muSF*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF*(dR_bJet_lJet>0.4)*(mtwMass>50)*mtw_weight_50GeVCut",
                                QCDcut="(dR_bJet_lJet>0.4)*(mtwMass>50)*mtw_weight_50GeVCut", 
                                DNNCut=">=0.0",
                                hist_sys_name="muSF_up"):

    print('============================================')
    print("MCcut = ",MCcut)
    print('============================================')
    if(lep=="mu"):
            lepton = "Muon"
    elif(lep=="el"):
            lepton = "Electron"
    print(lepton)
    
    Variable,X_axies,Y_axies,lest_bin,max_bin,Num_bin = get_histogram_distciption(Variable)
    print(X_axies," ",Y_axies," ",lest_bin," ",max_bin," ",Num_bin)
                
    yearDir={
                'UL2016preVFP' :  "SIXTEEN_preVFP",
                'UL2016postVFP' : "SIXTEEN_postVFP",
                'UL2017' : "SEVENTEEN",
                'UL2018' : "EIGHTEEN"}
    Combine_year_tag={
                'UL2016preVFP' :  "_ULpre16",
                'UL2016postVFP' : "_ULpost16",
                'UL2017' : "_UL17",
                'UL2018' : "_UL18"}

    ################### Genral Dir and selection ##################################################

    #applydir = '/home/mikumar/t3store3/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/DNN/DNN_output_without_mtwCut/2J1T1/Apply_all/'
    applydir = '/home/mikumar/t3store/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/DNN/DNN_output_without_mtwCut/2J1T1/Apply_all/'
    Datacut = "(dR_bJet_lJet>0.4)*(mtwMass>50)"
    DNNcut_str = "*(t_ch_CAsi"+DNNCut+")" 
    hist_to_return = [] 
    #################### Nimonal Samples MC ########################################################
 

    channels_Nomi = ['Tchannel' , 'Tbarchannel','tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic', 'WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJetsToLL', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L',"QCD"]


    Fpaths_DNN_apply = {}
    EvtWeight_Fpaths_Iso = {}
    Data_AntiIso_Fpath = "" 
    for channel in channels_Nomi:
            Fpaths_DNN_apply[channel] = applydir+year+'_'+channel+'_Apply_all_'+lep+'.root' # prepare dict for the in put files
            EvtWeight_Fpaths_Iso[channel] = "/home/mikumar/t3store/workarea/Nanoaod_tools/CMSSW_10_2_28/src/Run2UL_Analysis/stack_plots_before_ML/Minitree_with_mtw_weight/2J1T1/"+year+'_'+channel+'_Apply_all_'+lep+'.root'
            #if(channel=="QCD"): Data_AntiIso_Fpath =  "/grid_mnt/t3storage3/mikumar/UL_Run2/"+yearDir[year]+"/minitree/Mc/2J1T0/Minitree_Data"+year+"_2J1T0_"+lep+".root"
    
               
    #print EvtWeight_Fpaths_Iso
      
    if(Variable=="TMath::Log(topMass)"): Variable="lntopMass"
    # claculation of the scale QCD and NonQCD
    #NonQCD_Inte,QCD_Inte = Nomi_QCD_NoNQCD_Integral(lep,year,Variable,MCcut,Datacut,EvtWeight_Fpaths_Iso,Data_AntiIso_Fpath,Fpaths_DNN_apply)
    #QCD_Inte_v2 = Nomi_QCD_Integral(lep,year,Variable,Datacut,Data_AntiIso_Fpath,Fpaths_DNN_apply)
    #NonQCD_Inte = Nomi_NoNQCD_Integral(lep,year,Variable,MCcut,EvtWeight_Fpaths_Iso,Fpaths_DNN_apply)
    # get histogram with DNN cut
    hists_corr,hists_wron =  get_histogram_with_DNN_cut(lep,year,Variable,channels_Nomi[:-1], MCcut , QCDcut, Datacut , DNNCut ,EvtWeight_Fpaths_Iso,Fpaths_DNN_apply)
    if(Variable=="lntopMass"):   Variable="TMath::Log(topMass)" 
    del Fpaths_DNN_apply
    del EvtWeight_Fpaths_Iso
    del Data_AntiIso_Fpath

    #print "NonQCD_Inte : ",NonQCD_Inte
    #MCSF = NonQCDScale_mtwFit[lep][year]/NonQCD_Inte
    #QCDSF = QCDScale_mtwFit[lep][year]/QCD_Inte
    print
    #print "MCSF: ",MCSF#," QCDSF: ",QCDSF

    hist_corr_assig = {}
    hist_wron_assig = {}

    for channel_no,channel in enumerate(channels_Nomi[:-1]):
        if(channel in ["Tchannel","Tbarchannel"]):
                propagate_rate_uncertainity(hists_corr[channel_no], 15.0)
                propagate_rate_uncertainity(hists_wron[channel_no], 15.0)
                
        elif(channel in ['tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic']):
                propagate_rate_uncertainity(hists_corr[channel_no], 6.0)
                propagate_rate_uncertainity(hists_wron[channel_no], 6.0)
        else:
                propagate_rate_uncertainity(hists_corr[channel_no], 10.0)
                propagate_rate_uncertainity(hists_wron[channel_no], 10.0)
        hist_corr_assig[channel] = hists_corr[channel_no].Clone()
        hist_wron_assig[channel] = hists_wron[channel_no].Clone()
        #hist_corr_assig[channel].Scale(MCSF)
        #hist_wron_assig[channel].Scale(MCSF)        

    del hists_corr
    del hists_wron
        
    #print hist_corr_assig
    print(hist_wron_assig)
    top_sig_Nomi = hist_corr_assig["Tchannel"].Clone(); top_sig_Nomi.Add(hist_corr_assig["Tbarchannel"]);
    top_sig_Nomi.Add(hist_wron_assig["Tchannel"]); top_sig_Nomi.Add(hist_wron_assig["Tbarchannel"]);
    top_sig_Nomi.SetLineColor(rt.kRed);top_sig_Nomi.SetLineWidth(2)
    top_sig_Nomi.GetXaxis().SetTitle(X_axies)
    top_sig_Nomi.SetName("top_sig_1725"+Combine_year_tag[year]+hist_sys_name)

    top_bkg_Nomi = hist_corr_assig['tw_top'].Clone(); top_bkg_Nomi.Add(hist_wron_assig['tw_top'])    
    for channel in ['tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic']:
        top_bkg_Nomi.Add(hist_corr_assig[channel]); top_bkg_Nomi.Add(hist_wron_assig[channel]) 
    top_bkg_Nomi.SetLineColor(rt.kOrange-1); top_bkg_Nomi.SetLineWidth(2)
    top_bkg_Nomi.SetName("top_bkg_1725"+Combine_year_tag[year]+hist_sys_name)
    

    hist_EWK = hist_corr_assig["WJetsToLNu_0J"]; hist_EWK.Add(hist_wron_assig["WJetsToLNu_0J"])
    for channel in ['WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJetsToLL', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L']:
        hist_EWK.Add(hist_corr_assig[channel]); hist_EWK.Add(hist_wron_assig[channel])
    hist_EWK.SetLineColor(rt.kMagenta); hist_EWK.SetLineWidth(2)
    hist_EWK.SetName("EWK_bkg"+Combine_year_tag[year]+hist_sys_name)

    #for i in range(1,top_sig_Nomi.GetNbinsX()+1):
    #    print "--------------------"
    #    print "top sig : ",top_sig_Nomi.GetBinContent(i), top_sig_Nomi.GetBinError(i)
    #    print "top bkg : ",top_bkg_Nomi.GetBinContent(i), top_bkg_Nomi.GetBinError(i)
    #    print "EWK bkg : ",hist_EWK.GetBinContent(i), hist_EWK.GetBinError(i)

    #----------------- Add Nomi histograms ------------------ #
    hist_to_return.append(top_sig_Nomi)
    hist_to_return.append(top_bkg_Nomi)
    hist_to_return.append(hist_EWK)

    return hist_to_return
   #########################  Additive systematic ###########################


def Get_samples_hist_wo_NonQCD_Norm(lep="mu",year="UL2017",Variable="lntopMass",MCcut = "Xsec_wgt*LHEWeightSign*puWeight*muSF*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF*(dR_bJet_lJet>0.4)*(mtwMass>50)",Channels = [], region = "2J1T",DNNCut=">=0.0",hist_sys_name="muSF_up"):
    print("MCcut = ",MCcut)
    if(lep=="mu"):
            lepton = "Muon"
    elif(lep=="el"):
            lepton = "Electron"
    print(lepton)
    
    Variable,X_axies,Y_axies,lest_bin,max_bin,Num_bin = get_histogram_distciption(Variable)
    print(X_axies," ",Y_axies," ",lest_bin," ",max_bin," ",Num_bin)
                
    yearDir={
                'UL2016preVFP' :  "SIXTEEN_preVFP",
                'UL2016postVFP' : "SIXTEEN_postVFP",
                'UL2017' : "SEVENTEEN",
                'UL2018' : "EIGHTEEN"}
    Combine_year_tag={
                'UL2016preVFP' :  "ULpre16",
                'UL2016postVFP' : "ULpost16",
                'UL2017' : "UL17",
                'UL2018' : "UL18"}
    


    #################### Genral Dir and selection ##################################################
    
    applydir = '/home/mikumar/t3store3/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/DNN/DNN_output_without_mtwCut/'+region+'1/Apply_all/'
    Datacut = "(dR_bJet_lJet>0.4)*(mtwMass>50)"
    DNNcut_str = "*(t_ch_CAsi"+DNNCut+")" 
    hist_to_return = [] 
    #################### Nimonal Samples MC ########################################################
 

    channels_Nomi = Channels #['Tchannel' , 'Tbarchannel','tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic', 'WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJetsToLL', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L',"QCD"]


    Fpaths_DNN_apply = {}
    EvtWeight_Fpaths_Iso = {}
    Data_AntiIso_Fpath = "" 
    for channel in channels_Nomi:
            Fpaths_DNN_apply[channel] = applydir+year+'_'+channel+'_Apply_all_'+lep+'.root' # prepare dict for the in put files
            EvtWeight_Fpaths_Iso[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/"+yearDir[year]+"/minitree/Mc/"+region+"1/Minitree_"+channel+"_"+region+"1_"+lep+".root"
            #if(channel=="QCD"): Data_AntiIso_Fpath =  "/grid_mnt/t3storage3/mikumar/UL_Run2/"+yearDir[year]+"/minitree/Mc/2J1T0/Minitree_Data"+year+"_2J1T0_"+lep+".root"
    
               
    #print EvtWeight_Fpaths_Iso
      
    if(Variable=="TMath::Log(topMass)"): Variable="lntopMass"
    # get histogram with DNN cut
    hists_corr,hists_wron =  get_histogram_with_DNN_cut(lep,year,Variable,channels_Nomi, MCcut , Datacut , DNNCut ,EvtWeight_Fpaths_Iso,Fpaths_DNN_apply)
    if(Variable=="lntopMass"):   Variable="TMath::Log(topMass)" 
    del Fpaths_DNN_apply
    del EvtWeight_Fpaths_Iso
    del Data_AntiIso_Fpath

    hist_corr_assig = {}
    hist_wron_assig = {}

    for channel_no,channel in enumerate(channels_Nomi):
        if(channel in ["Tchannel","Tbarchannel"]):
                propagate_rate_uncertainity(hists_corr[channel_no], 15.0)
                propagate_rate_uncertainity(hists_wron[channel_no], 15.0)
                
        elif(channel in ['tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic']):
                propagate_rate_uncertainity(hists_corr[channel_no], 6.0)
                propagate_rate_uncertainity(hists_wron[channel_no], 6.0)
        else:
                propagate_rate_uncertainity(hists_corr[channel_no], 10.0)
                propagate_rate_uncertainity(hists_wron[channel_no], 10.0)
        hist_corr_assig[channel] = hists_corr[channel_no].Clone()
        hist_wron_assig[channel] = hists_wron[channel_no].Clone()

    del hists_corr
    del hists_wron
        
    #print hist_corr_assig
    #print hist_wron_assig
    if("Tchannel" in hist_corr_assig):
        top_sig_Nomi = hist_corr_assig["Tchannel"].Clone(); top_sig_Nomi.Add(hist_corr_assig["Tbarchannel"]);
        top_sig_Nomi.Add(hist_wron_assig["Tchannel"]); top_sig_Nomi.Add(hist_wron_assig["Tbarchannel"]);
        top_sig_Nomi.SetLineColor(rt.kRed);top_sig_Nomi.SetLineWidth(2)
        top_sig_Nomi.GetXaxis().SetTitle(X_axies)
        
        if(not("tw_top" in hist_corr_assig)):top_bkg_Nomi = hist_corr_assig["Tchannel"].Clone();  top_bkg_Nomi.Reset()
        if(not("WJetsToLNu_0J" in hist_corr_assig)): hist_EWK = hist_corr_assig["Tchannel"].Clone();  hist_EWK.Reset()

    if("tw_top" in hist_corr_assig):
        top_bkg_Nomi = hist_corr_assig['tw_top'].Clone(); top_bkg_Nomi.Add(hist_wron_assig['tw_top'])    
        for channel in ['tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic']:
            top_bkg_Nomi.Add(hist_corr_assig[channel]); top_bkg_Nomi.Add(hist_wron_assig[channel]) 
        
        if(not("Tchannel" in hist_corr_assig)): top_sig_Nomi = hist_corr_assig["tw_top"].Clone();  top_sig_Nomi.Reset()
        if(not("WJetsToLNu_0J" in hist_corr_assig)): hist_EWK = hist_corr_assig["tw_top"].Clone();  hist_EWK.Reset()
    
    if("WJetsToLNu_0J" in hist_corr_assig):
        hist_EWK = hist_corr_assig["WJetsToLNu_0J"].Clone(); hist_EWK.Add(hist_wron_assig["WJetsToLNu_0J"])
        for channel in ['WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJetsToLL', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L']:
            hist_EWK.Add(hist_corr_assig[channel]); hist_EWK.Add(hist_wron_assig[channel])
            
        if(not("tw_top" in hist_corr_assig)): top_bkg_Nomi = hist_corr_assig["WJetsToLNu_0J"].Clone();  top_bkg_Nomi.Reset()
        if(not("Tchannel" in hist_corr_assig)): top_sig_Nomi = hist_corr_assig["WJetsToLNu_0J"].Clone();  top_sig_Nomi.Reset()

    top_sig_Nomi.SetName("top_sig_1725"+Combine_year_tag[year]+hist_sys_name)
    top_bkg_Nomi.SetLineColor(rt.kOrange-1); top_bkg_Nomi.SetLineWidth(2)
    top_bkg_Nomi.SetName("top_bkg_1725"+Combine_year_tag[year]+hist_sys_name)
    hist_EWK.SetLineColor(rt.kMagenta); hist_EWK.SetLineWidth(2)
    hist_EWK.SetName("EWK_bkg"+Combine_year_tag[year]+hist_sys_name)

    #for i in range(1,top_sig_Nomi.GetNbinsX()+1):
    #    print "--------------------"
    #    print "top sig : ",top_sig_Nomi.GetBinContent(i), top_sig_Nomi.GetBinError(i)
    #    print "top bkg : ",top_bkg_Nomi.GetBinContent(i), top_bkg_Nomi.GetBinError(i)
    #    print "EWK bkg : ",hist_EWK.GetBinContent(i), hist_EWK.GetBinError(i)

    #----------------- Add Nomi histograms ------------------ #
    hist_to_return.append(top_sig_Nomi)
    hist_to_return.append(top_bkg_Nomi)
    hist_to_return.append(hist_EWK)

    return hist_to_return
   #########################  Additive systematic ###########################


       
if __name__ == "__main__":
    hists=Get_additive_sys_samples(lep="mu",year="UL2017",Variable="lntopMass",MCcut = "Xsec_wgt*LHEWeightSign*puWeight*Muon_SF_IsoUp*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF*(dR_bJet_lJet>0.4)*(mtwMass>50)",DNNCut=">=0.0",hist_sys_name="muSF_up")
    for Hist in hists: 
       Hist.Print()
