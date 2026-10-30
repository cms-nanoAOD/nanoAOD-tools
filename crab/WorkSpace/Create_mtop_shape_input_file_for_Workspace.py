import ROOT as rt
import numpy as np
#import scipy.integrate as sp
import argparse as arg
import math
import sys, os
from rich.console import Console
console = Console()

parser = arg.ArgumentParser(description='inputs discription')
parser.add_argument('-l', '--lepton', dest='lepton', type=str, nargs=1, help="lepton [ el  mu ]")
parser.add_argument('-y', '--year  ', dest='year', type=str, nargs=1, help="Year [ UL2016preVFP  UL2016postVFP  UL2017  UL2018 ]")
parser.add_argument('-v', '--var  ', dest='var', type=str, nargs=1, help="var [ lntopMass topMass t_ch_CAsi]")
parser.add_argument('-f', '--fitdignostic_outFile ', dest='fitdignostic_outFile', type=str, default=[ None ],nargs=1, help="DNNFit dignostic output file which has histogram files i.e /home/mikumar/t3store3/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/fitDiagnostics_M1725_DNNfit_UL2017.root")
parser.add_argument('-DC', '--DNNCut  ', dest='DNNCut', type=str, nargs=1, help="if need to apply DNNCut [ >=0.0 ,>=0.7]")
parser.add_argument('-Alt', '--is_Alt_samp_add ', dest='is_Alt_samp_add',  action="store_true", help="Enable this feature if alternate mass and width variation from gen weights will be added")
parser.add_argument('-lepSF_sys', '--is_lepSF_sys ', dest='is_lepSF_sys_add',  action="store_true", help="Enable this feature if weights depent lepSF sys will be added lepSF")
parser.add_argument('-puWeight_sys', '--is_puWeight_sys ', dest='is_puWeight_sys_add',  action="store_true", help="Enable this feature if weights depent puWeightUp ")
parser.add_argument('-muR_muF_sys', '--is_muR_muF_sys ', dest='is_muR_muF_sys_add',  action="store_true", help="Enable this feature if weights depent muR muF")
parser.add_argument('-pdf_sys', '--is_pdf_sys ', dest='is_pdf_sys_add',  action="store_true", help="Enable this feature if weights depent pdf sys")
parser.add_argument('-Bweight_sys', '--is_Bweight_sys ', dest='is_Bweight_sys_add',  action="store_true", help="Enable this feature if weights depent Bweight sys will be added lepSF")
parser.add_argument('-colorReconnect_sys', '--is_color_reconection_sys_add ', dest='is_color_reconection_sys_add',  action="store_true", help="Enable this feature if sys samples for color reconnection need to be added")
parser.add_argument('-JES_JER_sys', '--is_JES_JER_sys_add', dest='is_JES_JER_sys_add',  action="store_true", help="Enable this feature if sys samples for JES and JER")
parser.add_argument('-ISR_FSR_sys', '--is_ISR_FSR_sys_add ', dest='is_ISR_FSR_sys_add',  action="store_true", help="Enable this feature if weights depent iSR FSR and hdamp will be added")
parser.add_argument('-allsys', '--is_all_sys_add ', dest='is_all_sys_add',  action="store_true", help="Enable this feature if sys samples from minitree weights will be added")
args = parser.parse_args()

if (args.year == None or args.lepton == None):
        print("USAGE: %s [-h] [-y <Data year> -l <lepton>] -v <variable>"%(sys.argv [0]))
        sys.exit (1)

if args.year[0] not in ['UL2016preVFP', 'UL2016postVFP','UL2017','UL2018']:
    print('Error: Incorrect choice of year, use -h for help')
    exit()

if args.lepton[0] not in ['el','mu']:
    print('Error: Incorrect choice of lepton, use -h for help')
    exit()

if (args.var == None):
        print("Error: Incorrect choice of Variable, use -v <variable>"%(sys.argv [0]))
        sys.exit (1)

print(args)



lep = args.lepton[0]
year= args.year[0]
Variable = args.var[0]
DNNFit_rescale_file = args.fitdignostic_outFile[0]
DNNCut = args.DNNCut[0]
isAltSample=args.is_Alt_samp_add
allsys = args.is_all_sys_add
colorReconect = args.is_color_reconection_sys_add
JES_JERSys = args.is_JES_JER_sys_add 
lepSF_sys = args.is_lepSF_sys_add
Bweight_sys = args.is_Bweight_sys_add
puWeight_sys = args.is_puWeight_sys_add
muR_muF_sys = args.is_muR_muF_sys_add
pdf_sys = args.is_pdf_sys_add
isr_fsr_sys = args.is_ISR_FSR_sys_add

if(DNNFit_rescale_file!=None):
    if(os.path.isfile(DNNFit_rescale_file)): print("Reading the Normalization form the "+DNNFit_rescale_file)
    else:
        print(DNNFit_rescale_file, " does not exist")
        exit(0)

print("DNNcut = ",DNNCut)
gt_or_lt_tag = ''
if('>' in DNNCut):gt_or_lt_tag = gt_or_lt_tag+'_gt'
if('<' in DNNCut):gt_or_lt_tag = gt_or_lt_tag+'_lt'


from Histogram_discribtions import get_histogram_distciption 
from Get_Histogram_after_DNN_cuts import get_histogram_with_DNN_cut
from Overflow_N_Underflowbin import DrawOverflow_N_DrawUnderflow
from mlfitNormsToText import *
from create_Alt_sample import alt_hypotheis_sample,alt_hypotheis_sample_from_nanoaod_samples

from Propagate_rate_Uncertainity import propagate_rate_uncertainity
from Get_Weighted_Hist_only_sys_EWK import get_Weight_sys_EWK
from Get_Weighted_Hist_only_sys_top import get_Weight_sys_top

def Create_Workspace_input_file(lep="mu",year="UL2017",Variable="lntopMass"):

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

    tag = Combine_year_tag[year]

    #################### Genral Dir and selection ##################################################
    
    #applydir = '/home/mikumar/t3store/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/DNN/DNN_output_without_mtwCut/2J1T1/Apply_all/'
    applydir = '/feynman/home/dphp/mk277705/work/RUN2_UL/DNN_outputs_without_mtwCut_corr_bweight/'+yearDir[year]+'/2J1T1/Apply_all/'
    MCcut = "Xsec_wgt*LHEWeightSign*puWeight*"+lep+"SF*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF*(dR_bJet_lJet>0.4)*(mtwMass>50)*mtw_weight_50GeVCut" 
    Datacut = "(dR_bJet_lJet>0.4)*(mtwMass>50)"
    QCDcut = "(dR_bJet_lJet>0.4)*(mtwMass>50)*mtw_weight_50GeVCut"
    DNNcut_str = "*"+DNNCut 
    hist_to_return = [] 
    #################### Nimonal Samples MC ########################################################
 

    channels_Nomi = ['Tchannel' , 'Tbarchannel','tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic', 'WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJetsToLL', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L','QCD']
    channels_top_only = ['Tchannel' , 'Tbarchannel','tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic']

    Fpaths_DNN_apply = {}
    File_with_mtwMassFit_weight_Iso = {}
    Data_AntiIso_Fpath = "" 
    for channel in channels_Nomi:
            Fpaths_DNN_apply[channel] = applydir+year+'_'+channel+'_Apply_all_'+lep+'.root' # prepare dict for the in put files
            #File_with_mtwMassFit_weight_Iso[channel] = "/nfs/home/common/RUN2_UL/Minitree_corr_bweight_with_mtwMassFit_Scale/"+yearDir[year]+"/2J1T1/"+year+'_'+channel+'_Apply_all_'+lep+'.root'
            #if(channel=="QCD"): Data_AntiIso_Fpath =  "/nfs/home/common/RUN2_UL/Minitree_corr_bweight_with_mtwMassFit_Scale/"+yearDir[year]+"/2J1T1/"+year+'_'+channel+'_Apply_all_'+lep+'.root'
            File_with_mtwMassFit_weight_Iso[channel] = "/feynman/home/dphp/mk277705/work/RUN2_UL/Minitree_corr_bweight_with_mtwMassFit_Scale_new/"+yearDir[year]+"/2J1T1/"+year+'_'+channel+'_Apply_all_'+lep+'.root'
            if(channel=="QCD"): Data_AntiIso_Fpath =  "/feynman/home/dphp/mk277705/work/RUN2_UL/Minitree_corr_bweight_with_mtwMassFit_Scale/"+yearDir[year]+"/2J1T1/"+year+'_'+channel+'_Apply_all_'+lep+'.root'

    #print File_with_mtwMassFit_weight_Iso

    if(Variable=="TMath::Log(topMass)"): Variable="lntopMass"
    # get histogram with DNN cut
    print(type(QCDcut),"=======================")
    hists_corr,hists_wron =  get_histogram_with_DNN_cut(lep,year,Variable,channels_Nomi[:-1], MCcut ,QCDcut, Datacut , DNNCut ,File_with_mtwMassFit_weight_Iso,Fpaths_DNN_apply)
    if(Variable=="lntopMass"):   Variable="TMath::Log(topMass)" 
    del Data_AntiIso_Fpath

    hist_corr_assig = {}
    hist_wron_assig = {}

    for channel_no,channel in enumerate(channels_Nomi[:-1]):
        hist_corr_assig[channel] = hists_corr[channel_no].Clone()
        hist_wron_assig[channel] = hists_wron[channel_no].Clone()
        if(channel in ['Tchannel' , 'Tbarchannel']):
            print("===========================================")
            hist_corr_assig[channel].Print()
            print("===========================================")

    del hists_corr
    del hists_wron

    top_sig_cons = 6.0 ; top_sig_DNNfitrescale = 1.0
    top_bkg_cons = 5.0  ; top_bkg_DNNfitrescale = 1.0
    EWK_bkg_cons = 6.0 ; EWK_bkg_DNNfitrescale = 1.0
    QCD_bkg_cons = 50.0 ; QCD_bkg_DNNfitrescale = 1.0

    if(DNNFit_rescale_file!=None):
        from Get_DNNFit_rescale_parameters import get_DNNFit_rescale_parameters
        rescale_info = get_DNNFit_rescale_parameters(
            DNNFit_rescale_file=DNNFit_rescale_file,
            year=year,
            lep=lep,
            tag=tag
        )


    print("top_sig_cons = %s ; top_bkg_cons = %s ; EWK_bkg_cons = %s ; QCD_bkg_cons = %s" % (top_sig_cons, top_bkg_cons, EWK_bkg_cons, QCD_bkg_cons))
    print("top_sig_DNNfitrescale = %s ; top_bkg_DNNfitrescale = %s ; EWK_bkg_DNNfitrescale = %s ; QCD_bkg_DNNfitrescale = %s "%(top_sig_DNNfitrescale, top_bkg_DNNfitrescale, EWK_bkg_DNNfitrescale, QCD_bkg_DNNfitrescale))
    top_sig_Nomi = hist_corr_assig["Tchannel"].Clone(); top_sig_Nomi.Add(hist_corr_assig["Tbarchannel"]);
    top_sig_Nomi.Print()
    top_sig_Nomi.Scale(top_sig_DNNfitrescale) 
    top_sig_Nomi.SetLineColor(rt.kRed);top_sig_Nomi.SetLineWidth(2)
    top_sig_Nomi.GetXaxis().SetTitle(X_axies)
    top_sig_Nomi.SetName("top_sig_1725"+tag+gt_or_lt_tag)
    console.log(f"Signal corr. recons. hist  {top_sig_Nomi.Integral() = }", style="green")
    propagate_rate_uncertainity(top_sig_Nomi, top_sig_cons)
    print("print after uncertinty propagation 1")
    top_sig_Nomi.Print()

    missreco_single_top_bkg = hist_wron_assig["Tchannel"].Clone(); missreco_single_top_bkg.Add(hist_wron_assig["Tbarchannel"]);
    missreco_single_top_bkg.Scale(top_sig_DNNfitrescale)
    propagate_rate_uncertainity(missreco_single_top_bkg, top_sig_cons)
    
    

    top_bkg_Nomi = hist_corr_assig['tw_top'].Clone(); missrecotop_bkg_Nomi = hist_wron_assig['tw_top'].Clone();
    for channel in ['tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic']:
        top_bkg_Nomi.Add(hist_corr_assig[channel]); missrecotop_bkg_Nomi.Add(hist_wron_assig[channel])
    missrecotop_bkg_Nomi.SetLineColor(rt.kOrange-1); missrecotop_bkg_Nomi.SetLineWidth(2)

    top_bkg_Nomi.Scale(top_bkg_DNNfitrescale)
    propagate_rate_uncertainity(top_bkg_Nomi, top_bkg_cons)

    missrecotop_bkg_Nomi.Scale(top_bkg_DNNfitrescale)
    propagate_rate_uncertainity(missrecotop_bkg_Nomi, top_bkg_cons)

    # =========== for new constrained defined histograms ==========================#
    top_sig_cons_hist = top_sig_Nomi
    top_bkg_cons_hist = top_bkg_Nomi

    missreco_top_sig_cons_hist = missreco_single_top_bkg
    missreco_top_bkg_cons_hist = missrecotop_bkg_Nomi

    top_sig_total_cons_hist = top_sig_cons_hist.Clone()
    top_bkg_cons_hist.Print()
    console.log(f"top bkg corr. recons. hist  {top_bkg_cons_hist.Integral() = }", style="green")
    top_sig_total_cons_hist.Add(top_bkg_cons_hist)
    missrecotop_bkg_total_cons_hist = missreco_top_sig_cons_hist.Clone()
    missrecotop_bkg_total_cons_hist.Add(missreco_top_bkg_cons_hist)

    print("\n===================  "+year+"    ========================")
    print("cons_top_sig            lnN     %.3f     -        - "%((1+(top_sig_cons/100))*(top_sig_cons_hist.Integral()/top_sig_total_cons_hist.Integral())+(1+(top_bkg_cons/100))*(top_bkg_cons_hist.Integral()/top_sig_total_cons_hist.Integral())))
    print("cons_top_bkg            lnN     -        -        %.3f "%((1+(top_sig_cons/100))*(missreco_top_sig_cons_hist.Integral()/missrecotop_bkg_total_cons_hist.Integral())+(1+(top_bkg_cons/100))*(missreco_top_bkg_cons_hist.Integral()/missrecotop_bkg_total_cons_hist.Integral())))
    print("===========================================\n")

    # =====================================#

    top_sig_Nomi.Add(top_bkg_Nomi)    
    missrecotop_bkg_Nomi.Add(missreco_single_top_bkg)

    missrecotop_bkg_Nomi.SetName("top_bkg_1725"+tag+gt_or_lt_tag)
    

    hist_EWK = hist_corr_assig["WJetsToLNu_0J"].Clone();hist_EWK.Add(hist_wron_assig["WJetsToLNu_0J"])
    for channel in ['WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJetsToLL', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L']:
        hist_EWK.Add(hist_corr_assig[channel]); hist_EWK.Add(hist_wron_assig[channel])
    hist_EWK.SetLineColor(rt.kMagenta); hist_EWK.SetLineWidth(2)
    hist_EWK.Scale(EWK_bkg_DNNfitrescale)
    signal_region_EWK_Integral = hist_EWK.Integral()


    hist_EWK_signal_region = hist_EWK.Clone()
    hist_EWK_signal_region.Print()
    hist_EWK_signal_region.SetName("EWK_bkg_SR"+tag+gt_or_lt_tag)
    propagate_rate_uncertainity(hist_EWK_signal_region, EWK_bkg_cons)
    hist_EWK_signal_region.Print()
    
    channels_EWK_only = ['WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJetsToLL', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L']
    
    CR_EWK_hist = get_Weight_sys_EWK(
        lep=lep,year=year,
        Variable=Variable,
        channels_weight_sys=channels_EWK_only,
        MCcut = MCcut,
        DNNcut = "(t_ch_CAsi>=0.3) * ((t_ch_CAsi<0.7)) ", 
        hist_sys_name="_"+lep,
        File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,
        Fpaths_DNN_apply=Fpaths_DNN_apply,
        EWK_cons=EWK_bkg_cons
    )
 
    CR_EWK_hist.SetName("EWK_bkg_CR"+tag+gt_or_lt_tag)
    propagate_rate_uncertainity(CR_EWK_hist, EWK_bkg_cons)
    CR_EWK_hist.Print()

    
    CR_SR_EWK_hist = get_Weight_sys_EWK(
        lep=lep,year=year,
        Variable=Variable,
        channels_weight_sys=channels_EWK_only,
        MCcut = MCcut,
        DNNcut = "(t_ch_CAsi>=0.3) ", 
        hist_sys_name="_"+lep,
        File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,
        Fpaths_DNN_apply=Fpaths_DNN_apply,
        EWK_cons=EWK_bkg_cons
    )
    print("===============================================================================")
    CR_SR_EWK_Integral = CR_SR_EWK_hist.Integral()
    hist_EWK = CR_SR_EWK_hist.Clone()
    hist_EWK.Scale(signal_region_EWK_Integral/CR_SR_EWK_Integral)
    hist_EWK.Print()
    hist_EWK.SetName("EWK_bkg"+tag+gt_or_lt_tag)
    propagate_rate_uncertainity(hist_EWK, EWK_bkg_cons)
    hist_EWK.Print()

    

    #################### Data and DD QCD  ######################################################## 
    print    
    print("Data and DDQCD with ", DNNcut_str, " .. .. .. .... ..... ...")
    print

    hs = {}
    infiles = {}
    intree = {}
    Fpaths_DNN_apply_data = {}
    rt.gStyle.SetOptStat(0)

    Data_AntiIso_Fpath = ""
    Data_Iso_Fpath = "" 
    for channel in ["QCD","Data"+year]:
           Fpaths_DNN_apply_data[channel] = applydir+year+'_'+channel+'_Apply_all_'+lep+'.root' # prepare dict for the in put files
    Data_AntiIso_Fpath =  "~/work/RUN2_UL/Minitree_with_mtw_weight/2J1T1/"+year+'_QCD_Apply_all_'+lep+'.root'
    Data_Iso_Fpath =  "~/work/RUN2_UL/Minitree_with_mtw_weight/2J1T1/"+year+'_'+channel+'_Apply_all_'+lep+'.root'

    #print Fpaths_DNN_apply

    for channel_no,channel in enumerate(["QCD","Data"+year]):
        if(channel=="QCD"):
                print(channel, " ", Data_AntiIso_Fpath)
                print(channel, " ", Fpaths_DNN_apply_data[channel])
                infiles[channel] = rt.TFile.Open(Data_AntiIso_Fpath, 'READ')
        else:
                print(channel, " ", Data_Iso_Fpath)
                print(channel, " ", Fpaths_DNN_apply_data[channel])
                infiles[channel] = rt.TFile.Open(Data_Iso_Fpath, 'READ')

        intree[channel] = infiles[channel].Get('Events')
        intree[channel].AddFriend ("Events",Fpaths_DNN_apply_data[channel])

        hs[channel] = rt.TH1F('hs' + channel, '', Num_bin, lest_bin, max_bin)
        #rt.gROOT.cd()
        if(channel=="QCD"):
            print(type(QCDcut),type(DNNcut_str))
            intree[channel].Project('hs' + channel, Variable,QCDcut+DNNcut_str)
        else:
            intree[channel].Project('hs' + channel, Variable,Datacut+DNNcut_str)
        #hs[channel] = DrawOverflow_N_DrawUnderflow(hs[channel])
        #hs[channel].Print()
    del Fpaths_DNN_apply_data   
    rt.gROOT.cd()
    Data = hs['Data'+year].Clone()
    DDQCD = hs['QCD'].Clone()
    #DDQCD.Scale(QCDSF)
    DDQCD.SetName("QCD_DD"+tag+gt_or_lt_tag)
    DDQCD.Scale(QCD_bkg_DNNfitrescale)
    propagate_rate_uncertainity(DDQCD, QCD_bkg_cons)
    #for i in range(1,DDQCD.GetNbinsX()+1):
    #    print "--------------------"
    #    print "QCD DDD : ",DDQCD.GetBinContent(i), DDQCD.GetBinError(i)
    DDQCD.Print()

    DDQCD_subs_data = Data.Clone()
    DDQCD_subs_data.Add(DDQCD,-1)

    DDQCD_subs_data.SetName("data_obs")
    print('True QCD substracted data ---- >')
    DDQCD_subs_data.Print()

    Total_MC_for_fit = top_sig_Nomi.Clone()
    Total_MC_for_fit.Add(missrecotop_bkg_Nomi)
    Total_MC_for_fit.Add(hist_EWK)
    Total_MC_for_fit.SetLineColor(rt.kBlack)
    Total_MC_for_fit.SetName("data_obs")
    print("MC saved as data ---- >")
    Total_MC_for_fit.Print()


    DDQCD.SetLineColor(rt.kGray); DDQCD.SetLineWidth(2)
    
    del hs
    del Data_Iso_Fpath,Data_AntiIso_Fpath 



    #----------------- Add Nomi histograms ------------------ #
    hist_to_return.append(top_sig_Nomi)
    hist_to_return.append(missrecotop_bkg_Nomi)
    hist_to_return.append(hist_EWK)
    hist_to_return.append(hist_EWK_signal_region)
    hist_to_return.append(CR_EWK_hist)
    hist_to_return.append(DDQCD)
    #hist_to_return.append(DDQCD_subs_data) #since analysis is blind
    hist_to_return.append(Total_MC_for_fit)
    sys_only_for_signal_names = ["ISRUp", "ISRDown", "FSRUp", "FSRDown", "hdampUp", "hdampDown","erdON","Gluonmove","QCDinspired","TuneCP5up","TuneCP5down",'AlphaSUp', 'AlphaSDown']
    sys_only_for_signal_names += [f"pdf{i}" for i in range(1, 101)]
    for sys_for_signal_name in sys_only_for_signal_names:
        hist_copy_EWK = hist_EWK.Clone()
        hist_copy_EWK.SetName("EWK_bkg"+tag+gt_or_lt_tag+sys_for_signal_name)
        hist_to_return.append(hist_copy_EWK)
        del hist_copy_EWK



    #################### ALternate mass and width  #################################################### 

    #top_sig_DNNfitrescale=1 ; top_bkg_DNNfitrescale = 1
    if(isAltSample or allsys):
        print("creating histogram for the Alt mass and with samples .............")
        print()
        Alt_mass_weights = ["Mtop1695", "Mtop1705", "Mtop1710","Mtop1715", "Mtop1735", "Mtop1745","Mtop1755"]
        Alt_width_weights = ["Wtop190", "Wtop170", "Wtop150","Wtop130", "Wtop110","Wtop090","Wtop075"]

        channels_alt = ['Tchannel','Tbarchannel','tw_antitop', 'tw_top','Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic']


        weight_file = {}
        for Channel_alt in channels_alt:
            #weight_file[Channel_alt] = "/home/mikumar/t3store/workarea/Nanoaod_tools/CMSSW_10_2_28/src/Run2UL_Analysis/NanoGen/GenWeight/GenWeight_"+Channel_alt+"_"+lep+"_"+year+".root"
            weight_file[Channel_alt] = "/feynman/home/dphp/mk277705/work/HiggsCombine/CMSSW_12_3_4/src/Run2UL_Analysis/NanoGen/GenWeight/GenWeight_"+Channel_alt+"_"+lep+"_"+year+"_new.root"

        for weight in Alt_mass_weights:
            print("\n #################  ", weight, "############## \n")
            hist_mass = alt_hypotheis_sample(lepton,Variable,MCcut,DNNcut_str,weight,weight_file,File_with_mtwMassFit_weight_Iso,Fpaths_DNN_apply,top_sig_DNNfitrescale,top_bkg_DNNfitrescale,top_sig_cons,top_bkg_cons)
            hist_mass.SetName("top_sig_"+weight.split("top")[1]+tag+gt_or_lt_tag)
            hist_mass.Print()
            hist_to_return.append(hist_mass)
            
            
        for weight in Alt_width_weights:
            print("\n #################  ", weight, "############## \n")
            hist_width = alt_hypotheis_sample(lepton,Variable,MCcut,DNNcut_str,weight,weight_file,File_with_mtwMassFit_weight_Iso,Fpaths_DNN_apply,top_sig_DNNfitrescale,top_bkg_DNNfitrescale,top_sig_cons,top_bkg_cons)
            hist_width.Print()
            hist_width.SetName("top_sig_"+weight.split("top")[1]+tag+gt_or_lt_tag)
            hist_to_return.append(hist_width)
        del weight_file
        #del File_with_mtwMassFit_weight_Iso,Fpaths_DNN_apply,weight_file
    
        # Include ttbar alternate mass sample shaped for validation of the rewaiting method
        if(Variable=="TMath::Log(topMass)"): Variable="lntopMass"
        # get histogram with DNN cut
        print(type(QCDcut),"=======================")
        channels_Alt_mass_ttbar_samples = ['ttbar_SemiLeptonic']
        hists_corr,hists_wron =  get_histogram_with_DNN_cut(lep,year,Variable,channels_Nomi[:-1], MCcut ,QCDcut, Datacut , DNNCut ,File_with_mtwMassFit_weight_Iso,Fpaths_DNN_apply)
        # if(Variable=="lntopMass"):   Variable="TMath::Log(topMass)" 
        # for mass in ["Mtop1715", "Mtop1735"]:
        #     print(f"\n ################# processing the {mass} from the samples ############## \n")
        #     hist_mass = alt_hypotheis_sample_from_nanoaod_samples(lepton,Variable,MCcut,DNNcut_str,File_with_mtwMassFit_weight_Iso,Fpaths_DNN_apply,top_sig_DNNfitrescale,top_bkg_DNNfitrescale,top_sig_cons,top_bkg_cons)
        #     hist_mass.SetName("top_sig_"+weight.split("top")[1]+tag+gt_or_lt_tag)
        #     hist_mass.Print()
        #     hist_to_return.append(hist_mass)



    #################### Systematic  ############################# 

    ####################    ISR FSR  hdamp  (from weights) ##################
    if(isr_fsr_sys or allsys):
        Fpaths_orignal_minitree = {}
        for channel in channels_top_only:
            Fpaths_orignal_minitree[channel] = f"/feynman/home/dphp/mk277705/work/RUN2_UL/Minitree_corr_bweight/{yearDir[year]}/2J1T1/Minitree_{channel}_2J1T1_{lep}.root"
    
        from Add_hdamp_ISR_FSR_to_Workspace import process_hdamp_ISR_FSR_systematics
        process_hdamp_ISR_FSR_systematics(
            lep=lep,
            year=year,
            Variable=Variable,
            MCcut=MCcut,
            DNNCut=DNNCut,
            File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,
            Fpaths_DNN_apply=Fpaths_DNN_apply,
            Fpaths_orignal_minitree = Fpaths_orignal_minitree, # these original files are requied since PSweights are not stored while saveing the mtwfit weights
            hist_corr_assig=hist_corr_assig,
            X_axies=X_axies,
            tag=tag,
            gt_or_lt_tag=gt_or_lt_tag,
            top_sig_cons=top_sig_cons,
            top_bkg_cons=top_bkg_cons,
            hist_to_return=hist_to_return
        )
        del Fpaths_orignal_minitree


    #####   lepton SF  ######
    if(allsys or lepSF_sys):
        from Add_lepSF_to_Workspace import process_lep_SF_systematics
        process_lep_SF_systematics(
            lep=lep,
            year=year,
            Variable=Variable,
            DNNCut=DNNCut,
            tag=tag,
            gt_or_lt_tag=gt_or_lt_tag,
            File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,
            Fpaths_DNN_apply=Fpaths_DNN_apply,
            signal_region_EWK_Integral = signal_region_EWK_Integral,
            top_sig_cons=top_sig_cons,
            top_bkg_cons=top_bkg_cons,
            EWK_bkg_cons=EWK_bkg_cons,
            channels_top_only=channels_top_only,
            channels_EWK_only=channels_EWK_only,
            hist_to_return=hist_to_return
        )

    #####   puileup  ######
    if(allsys or puWeight_sys):
        from Add_puileupWeight_to_Workspace import process_pileupweight_systematics
        process_pileupweight_systematics(
            lep=lep,
            year=year,
            Variable=Variable,
            DNNCut=DNNCut,
            tag=tag,
            gt_or_lt_tag=gt_or_lt_tag,
            File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,
            Fpaths_DNN_apply=Fpaths_DNN_apply,
            signal_region_EWK_Integral=signal_region_EWK_Integral,
            top_sig_cons=top_sig_cons,
            top_bkg_cons=top_bkg_cons,
            EWK_bkg_cons=EWK_bkg_cons,
            channels_top_only=channels_top_only,
            channels_EWK_only=channels_EWK_only,
            hist_to_return=hist_to_return
        )
    if(allsys or muR_muF_sys):
        from Add_muR_muF_to_Workspace import process_muR_muF_systematics
        process_muR_muF_systematics(
            lep=lep,
            year=year,
            Variable=Variable,
            DNNCut=DNNCut,
            tag=tag,
            gt_or_lt_tag=gt_or_lt_tag,
            File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,
            Fpaths_DNN_apply=Fpaths_DNN_apply,
            signal_region_EWK_Integral=signal_region_EWK_Integral,
            top_sig_cons=top_sig_cons,
            top_bkg_cons=top_bkg_cons,
            EWK_bkg_cons=EWK_bkg_cons,
            channels_top_only=channels_top_only,
            channels_EWK_only=channels_EWK_only,
            hist_to_return=hist_to_return
        )
    
    if(allsys or pdf_sys):
        from Add_pdf_to_Workspace import process_pdf_systematics
        process_pdf_systematics(
            lep=lep,
            year=year,
            Variable=Variable,
            DNNCut=DNNCut,
            tag=tag,
            gt_or_lt_tag=gt_or_lt_tag,
            File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,
            Fpaths_DNN_apply=Fpaths_DNN_apply,
            signal_region_EWK_Integral=signal_region_EWK_Integral,
            top_sig_cons=top_sig_cons,
            top_bkg_cons=top_bkg_cons,
            EWK_bkg_cons=EWK_bkg_cons,
            channels_top_only=channels_top_only,
            channels_EWK_only=channels_EWK_only,
            hist_to_return=hist_to_return
        )

    #####   bWeight  ######
    if(allsys or Bweight_sys ):
        from Add_Bweight_to_Workspace import process_bjet_systematics
        process_bjet_systematics(
            lep=lep,
            year=year,
            Variable=Variable,
            DNNCut=DNNCut,
            tag=tag,
            gt_or_lt_tag=gt_or_lt_tag,
            File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,
            Fpaths_DNN_apply=Fpaths_DNN_apply,
            signal_region_EWK_Integral = signal_region_EWK_Integral,
            top_sig_cons=top_sig_cons,
            top_bkg_cons=top_bkg_cons,
            EWK_bkg_cons=EWK_bkg_cons,
            channels_top_only=channels_top_only,
            channels_EWK_only=channels_EWK_only,
            hist_to_return=hist_to_return
        )

    #####   JES JER  ######
    if(allsys or JES_JERSys):
        from Add_JES_JER_to_Workspace import process_JER_JES_systematics
        # Now call the function using keyword arguments.
        print(f"{lep = }")
        process_JER_JES_systematics(
            lep=lep,
            year=year,
            Variable=Variable,
            MCcut=MCcut,
            DNNCut=DNNCut,
            tag=tag,
            gt_or_lt_tag=gt_or_lt_tag,
            File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,
            Fpaths_DNN_apply=Fpaths_DNN_apply,
            signal_region_EWK_Integral = signal_region_EWK_Integral,
            top_sig_cons=top_sig_cons,
            top_bkg_cons=top_bkg_cons,
            EWK_bkg_cons=EWK_bkg_cons,
            Control_EWK_hist=CR_SR_EWK_hist,
            channels_top_only=channels_top_only,
            channels_EWK_only=channels_EWK_only,
            hist_to_return=hist_to_return
        )

    # #####   other sample Sys  ######
    if(allsys or colorReconect):
        print("'n creating histogram for the systematic from diffrent samples\n")
        from Add_systemaic_from_samples_to_Workspace import process_systematics_from_diffrent_samples
        process_systematics_from_diffrent_samples(
            lep=lep,
            year=year,
            yearDir = yearDir,
            Variable=Variable,
            MCcut=MCcut,
            DNNCut=DNNCut,
            File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,
            Fpaths_DNN_apply=Fpaths_DNN_apply,
            hist_corr_assig=hist_corr_assig,
            X_axies=X_axies,
            tag=tag,
            gt_or_lt_tag=gt_or_lt_tag,
            top_sig_cons=top_sig_cons,
            top_bkg_cons=top_bkg_cons,
            Nominal_sig_Normalization=top_sig_Nomi.Integral(),
            Nominal_topbkg_Normalization= missrecotop_bkg_Nomi.Integral(),
            hist_to_return=hist_to_return
        )


    print("total number of histogram shaved :", len(hist_to_return))
    return hist_to_return


if __name__ == "__main__":
    
    
   #  if(">=0.7" in DNNCut and DNNFit_rescale_file!=None):
   #          output_file = "Hist_for_workspace/Combine_Input_"+Variable+"_histograms_"+year+"_"+lep+"_gteq0p7_withDNNfit_rebin.root"
   #  elif("<0.7" in DNNCut and "0.5" in DNNCut and DNNFit_rescale_file!=None): 
   #          output_file = "Hist_for_workspace/Combine_Input_"+Variable+"_histograms_"+year+"_"+lep+"_lt0p7gteq0p5_withDNNfit_rebin.root"
   #  elif(">=0.3" in DNNCut and "<0.7" in DNNCut and DNNFit_rescale_file!=None):
   #          output_file = "Hist_for_workspace/Combine_Input_"+Variable+"_histograms_"+year+"_"+lep+"_lt0p7gteq0p3_withDNNfit_rebin.root"
   #  elif(">=0.3" in DNNCut and DNNFit_rescale_file!=None):
   #          output_file = "Hist_for_workspace/Combine_Input_"+Variable+"_histograms_"+year+"_"+lep+"_gteq0p3_withDNNfit_rebin.root"        
   #  elif(">=0.7" in DNNCut and DNNFit_rescale_file==None):
   #          output_file = "Hist_for_workspace/Combine_Input_"+Variable+"_histograms_"+year+"_"+lep+"_gteq0p7_withoutDNNfit_rebin.root"
   #  elif("<0.7" in DNNCut and "0.5" in DNNCut and DNNFit_rescale_file==None):
   #          output_file = "Hist_for_workspace/Combine_Input_"+Variable+"_histograms_"+year+"_"+lep+"_lt0p7gteq0p5_withoutDNNfit_rebin.root"
   #  elif(">=0.3" in DNNCut and "<0.7" in DNNCut and DNNFit_rescale_file==None):
   #          output_file = "Hist_for_workspace/Combine_Input_"+Variable+"_histograms_"+year+"_"+lep+"_lt0p7gteq0p3_withoutDNNfit_rebin.root"
   #  elif(">=0.3" in DNNCut and DNNFit_rescale_file==None):
   #          output_file = "Hist_for_workspace/Combine_Input_"+Variable+"_histograms_"+year+"_"+lep+"_gteq0p3_withoutDNNfit_rebin.root"
   #  elif(">=0.1" in DNNCut and DNNFit_rescale_file==None):
   #          output_file = "Hist_for_workspace/Combine_Input_"+Variable+"_histograms_"+year+"_"+lep+"_gteq0p1_withoutDNNfit_rebin.root"
   #  else:
   #      print("something wrong with DNNcut")
   #      exit(0)

    if(">=" in DNNCut and "<" in DNNCut):
        DNNCut_vlaue = "0p"+DNNCut.split('.')[1].split(' ')[0]+"to0p"+DNNCut.split('<0.')[1].split(')')[0]
    elif(">=" in DNNCut):
        DNNCut_vlaue = "0p"+DNNCut.split('.')[1].split(')')[0]
    
    output_file = "Hist_for_workspace/Combine_Input_"+Variable+"_histograms_"+year+"_"+lep+"_gteq"+DNNCut_vlaue+"_withoutDNNfit_rebin_15_Bin.root"
    print(output_file)
    hists = Create_Workspace_input_file(lep,year,Variable) 
    outfile = rt.TFile(output_file,"recreate")
    outfile.cd()
    Dir_mu = outfile.mkdir(lep+"jets")
    Dir_mu.cd()
    
    for hist in hists:
        hist.Write()
        
    rt.gROOT.cd()

    outfile.Close()
    print("File write into "+output_file+" and saved")
    
