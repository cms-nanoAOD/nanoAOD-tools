import ROOT as rt
import numpy as np
#import scipy.integrate as sp
import argparse as arg
import math
import sys 
parser = arg.ArgumentParser(description='inputs discription')
parser.add_argument('-l', '--lepton', dest='lepton', type=str, nargs=1, help="lepton [ el  mu ]")
parser.add_argument('-y', '--year  ', dest='year', type=str, nargs=1, help="Year [ UL2016preVFP  UL2016postVFP  UL2017  UL2018 ]")
parser.add_argument('-v', '--var  ', dest='var', type=str, nargs=1, help="var [ lntopMass topMass t_ch_CAsi]")
#parser.add_argument('-DS', '--DNNscale  ', dest='DNNscale', type=str, nargs=1, help="if need to apply DNNscale [ 0 , 1]")
parser.add_argument('-DC', '--DNNCut  ', dest='DNNCut', type=str, nargs=1, help="if need to apply DNNCut [ >=0.0 ,>=0.7]")

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
DNN_rescale = 0 #args.DNNscale[0]
DNNCut = args.DNNCut[0]
from Histogram_discribtions import get_histogram_distciption 
from Get_Histogram_after_DNN_cuts import get_histogram_with_DNN_cut
from Get_Nomi_histogram_Integral import Nomi_QCD_Integral 
from Overflow_N_Underflowbin import DrawOverflow_N_DrawUnderflow
from QCD_Non_QCD_Normalization import *
from Get_Additive_sys_hitogram import *

def propagate_rate_uncertainity(hist, uncert):
    for i in range(1,hist.GetXaxis().GetNbins()+1):
        if hist.GetBinContent(i) != 0:
            hist.SetBinError(i, hist.GetBinContent(i) * uncert * 0.01)

################################# DNN scale ################ get from the lepton chage ratio max diff of Data amd MC ###########

def Create_Workspace_input_file(lep="mu",year="UL2017",Variable="lntopMass"):
    if(lep=="mu"):
            lepton = "Muon"
    elif(lep=="el"):
            lepton = "Electron"
    print(lepton)
    
    yearDir={
                'UL2016preVFP' :  "SIXTEEN_preVFP",
                'UL2016postVFP' : "SIXTEEN_postVFP",
                'UL2017' : "SEVENTEEN",
        } 
    Combine_year_tag={
                'UL2016preVFP' :  "_ULpre16",
                'UL2016postVFP' : "_ULpost16",
                'UL2017' : "_UL17",
                'UL2018' : "_UL18"}

    hist_to_return = [] 
    applydir = '/home/mikumar/t3store/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/DNN/DNN_output_without_mtwCut/2J1T1/Apply_all/'
    #applydir = '/home/mikumar/t3store/workarea/Nanoaod_tools/CMSSW_10_2_28/src/Run2UL_Analysis/stack_plots_before_ML/Minitree_with_mtw_weight/2J1T1'
    MCcut = "Xsec_wgt*LHEWeightSign*puWeight*"+lep+"SF*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF*(dR_bJet_lJet>0.4)*(mtwMass>50)*mtw_weight_50GeVCut" 
    QCDcut = "(dR_bJet_lJet>0.4)*(mtwMass>50)*mtw_weight_50GeVCut"
    Datacut = "(dR_bJet_lJet>0.4)*(mtwMass>50)"
    DNNcut_str = "*(t_ch_CAsi"+DNNCut+")"
 
    """##### shapes from control region ############
  
    ttbar_bkg_channels = ['tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic']
    EWK_bkg_channels = ['WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJets', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L']
    hists_3J2T_con = Get_samples_hist_wo_NonQCD_Norm(lep=lep,year=year,Variable=Variable,MCcut = MCcut,Channels=ttbar_bkg_channels,region="3J2T",DNNCut=DNNCut,hist_sys_name="")
    hists_2J1L0T_con = Get_samples_hist_wo_NonQCD_Norm(lep=lep,year=year,Variable=Variable,MCcut = MCcut,Channels=EWK_bkg_channels,region="2J1L0T",DNNCut=DNNCut,hist_sys_name="")
    del ttbar_bkg_channels
    del EWK_bkg_channels"""




    #####  Nominal MC samples #######
    print("\n #################   Nominal hist ############## \n")
    hists_Nomi = Get_additive_sys_samples(lep=lep,year=year,Variable=Variable,MCcut = MCcut,QCDcut=QCDcut,DNNCut=DNNCut,hist_sys_name="")
    
    hist_to_return.append(hists_Nomi[1].Clone())
    hist_to_return.append(hists_Nomi[2].Clone())
    hist_to_return.append(hists_Nomi[0].Clone())
    del hists_Nomi

    #################### Data and DD QCD  ######################################################## 
   
 
    hs = {}
    infiles = {}
    intree = {}
    Fpaths_DNN_apply = {}
    rt.gStyle.SetOptStat(0)
    
    #Data_AntiIso_Fpath = ""
    #Data_Iso_Fpath = "" 
    EvtWeight_Fpaths = {}
    for channel in ["QCD","Data"+year]:
        Fpaths_DNN_apply[channel] = applydir+year+'_'+channel+'_Apply_all_'+lep+'.root' # prepare dict for the in put files
        EvtWeight_Fpaths[channel] = "/home/mikumar/t3store/workarea/Nanoaod_tools/CMSSW_10_2_28/src/Run2UL_Analysis/stack_plots_before_ML/Minitree_with_mtw_weight/2J1T1/"+year+'_'+channel+'_Apply_all_'+lep+'.root'
    #Data_AntiIso_Fpath =  "/grid_mnt/t3storage3/mikumar/UL_Run2/"+yearDir[year]+"/minitree/Mc/2J1T0/Minitree_Data"+year+"_2J1T0_"+lep+".root"
    #Data_Iso_Fpath =  "/grid_mnt/t3storage3/mikumar/UL_Run2/"+yearDir[year]+"/minitree/Mc/2J1T1/Minitree_Data"+year+"_2J1T1_"+lep+".root"
    
    print    
    print("Data and DDQCD with ", DNNcut_str, " .. .. .. .... ..... ...")
    print
    #QCD_Inte = Nomi_QCD_Integral(lep,year,Variable,Datacut,Data_AntiIso_Fpath,Fpaths_DNN_apply)

    #print "QCD_Inte : ",QCD_Inte
    #QCDSF = QCDScale_mtwFit[lep][year]/QCD_Inte
    print
    #print Fpaths_DNN_apply

    for channel_no,channel in enumerate(["QCD","Data"+year]):
        #if(channel=="QCD"):
                #print channel, " ", Data_AntiIso_Fpath
                #print channel, " ", Fpaths_DNN_apply[channel]
                #infiles[channel] = rt.TFile.Open(Data_AntiIso_Fpath, 'READ')
        #else:
        #        print channel, " ", Data_Iso_Fpath
        #        print channel, " ", Fpaths_DNN_apply[channel]
        #        infiles[channel] = rt.TFile.Open(Data_Iso_Fpath, 'READ')
        infiles[channel] = rt.TFile.Open(Fpaths_DNN_apply[channel], 'READ')
        intree[channel] = infiles[channel].Get('Events')
        intree[channel].AddFriend ("Events",EvtWeight_Fpaths[channel])
  
        if(Variable=="t_ch_CAsi"):
                BINS = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,1.0]
                print("redefine assymatic histogram bins ", BINS)
                hs[channel] = rt.TH1F('hs' + channel, '', len(BINS)-1,np.array(BINS))
        else:
                Variable,X_axies,Y_axies,lest_bin,max_bin,Num_bin = get_histogram_distciption(Variable)
                hs[channel] = rt.TH1F('hs' + channel, '', Num_bin, lest_bin, max_bin)
        #rt.gROOT.cd()
    
        if('QCD' in channel):
                intree[channel].Project('hs' + channel, Variable,QCDcut+DNNcut_str)
        else:
                intree[channel].Project('hs' + channel, Variable,Datacut+DNNcut_str)
        #hs[channel] = DrawOverflow_N_DrawUnderflow(hs[channel])
        #hs[channel].Print()
        
    rt.gROOT.cd()
    Data = hs['Data'+year].Clone()
    DDQCD = hs['QCD'].Clone()
    #DDQCD.Scale(QCDSF)
    DDQCD.SetName("QCD_DD"+Combine_year_tag[year])
    propagate_rate_uncertainity(DDQCD, 50.0)
    #for i in range(1,DDQCD.GetNbinsX()+1):
    #    print "--------------------"
    #    print "QCD DDD : ",DDQCD.GetBinContent(i), DDQCD.GetBinError(i)
    DDQCD.Print()

    Data.SetName("data_obs")
    Data.Print()

    DDQCD.SetLineColor(rt.kGray); DDQCD.SetLineWidth(2)
    
    del hs
    #del Data_Iso_Fpath,Data_AntiIso_Fpath



    #----------------- Add Nomi histograms ------------------ #
    hist_to_return.append(DDQCD)
    hist_to_return.append(Data)

   #########################  Additive systematic ###########################

   
    #####  lepton SF ####### 
    sys_additive = {"el":["SF_Iso_IDUp", "SF_Iso_IDDown", "SF_Iso_TrigUp", "SF_Iso_TrigDown","SF_Veto_IDUp", "SF_Veto_IDDown", "SF_Veto_TrigUp", "SF_Veto_TrigDown"],
                    "mu":["SF_IsoUp", "SF_IsoDown", "SF_Iso_IDUp", "SF_Iso_IDDown", "SF_Iso_TrigUp", "SF_Iso_TrigDown"]
    }
    for sys in sys_additive[lep]:
        
        print("\n #################  ", sys, "############## \n")
        hists_syst = Get_additive_sys_samples(lep=lep,year=year,Variable=Variable,MCcut = "Xsec_wgt*LHEWeightSign*puWeight*"+lepton+"_"+sys+"*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF*(dR_bJet_lJet>0.4)*(mtwMass>50)*mtw_weight_50GeVCut",QCDcut=QCDcut,DNNCut=DNNCut,hist_sys_name="_"+lep+sys)
        for Hist in hists_syst:
            hist_to_return.append(Hist.Clone())
        del hists_syst
    del sys_additive
    #####   puileup  ######

    sys_pileup = ["puWeightUp","puWeightDown"]
    sys_variation = ["Up","Down"]
    for variation_no,sys in enumerate(sys_pileup):
        print("\n #################  ", sys, "############## \n")
        hists_syst = Get_additive_sys_samples(lep=lep,year=year,Variable=Variable,MCcut = "Xsec_wgt*LHEWeightSign*"+sys+"*"+lep+"SF*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF*(dR_bJet_lJet>0.4)*(mtwMass>50)*mtw_weight_50GeVCut",QCDcut=QCDcut,DNNCut=DNNCut,hist_sys_name="_puWeight"+sys_variation[variation_no])
        for Hist in hists_syst:
            hist_to_return.append(Hist.Clone())
        del hists_syst
    del sys_pileup,sys_variation

    sys_bWeight = ["bWeight_lf","bWeight_hf" , "bWeight_cferr1", "bWeight_cferr2", "bWeight_lfstats1", "bWeight_lfstats2", "bWeight_hfstats1", "bWeight_hfstats2", "bWeight_jes"]
    sys_variation = ["Up","Down"]
    for sys in sys_bWeight:
        for variation_no,variation in enumerate(sys_variation):
            hists_syst = Get_additive_sys_samples(lep=lep,year=year,Variable=Variable,MCcut = "Xsec_wgt*LHEWeightSign*puWeight*"+lep+"SF*L1PreFiringWeight_Nom*"+sys+variation+"*bJetPUJetID_SF*lJetPUJetID_SF*(dR_bJet_lJet>0.4)*(mtwMass>50)*mtw_weight_50GeVCut",QCDcut=QCDcut,DNNCut=DNNCut,hist_sys_name="_"+sys+variation)
            for Hist in hists_syst:
                hist_to_return.append(Hist.Clone())
            del hists_syst


    #################### ALternate mass and width  #################################################### 

    
    """print "creating histogram for the Alt mass and with samples ............."
    print 
    Alt_mass = ["1695","1715","1735","1755"]
    Alt_width = ["0p55","0p7","1p3","1p45"]
    channels_Alt_ttbar_semi = []
    channels_Alt_ttbar_full_mass = []
    channels_Alt_ttbar_full_width = []
    channels_Alt_tch = []
    channels_Alt_tbarch = []
    for mass in Alt_mass:
        channels_Alt_ttbar_semi.append("ttbar_SemiLeptonic_mtop"+mass)
        channels_Alt_ttbar_full_mass.append("ttbar_FullyLeptonic_mtop"+mass)
        channels_Alt_tch.append("Tchannel_mtop"+mass)
        channels_Alt_tbarch.append("Tbarchannel_mtop"+mass)
    for width in Alt_width:
        channels_Alt_ttbar_full_width.append("ttbar_FullyLeptonic_widthx"+width)

    channels_Alt= channels_Alt_tch+channels_Alt_tbarch+channels_Alt_ttbar_semi+channels_Alt_ttbar_full_mass +channels_Alt_ttbar_full_width
    
    del channels_Alt_tch
    del channels_Alt_tbarch 
    del channels_Alt_ttbar_semi
    del channels_Alt_ttbar_full_mass
    
    Fpaths_DNN_apply = {}
    EvtWeight_Fpaths_Iso = {}
    
    for channel in channels_Alt:
            Fpaths_DNN_apply[channel] = applydir+"sys_N_Alt/"+year+'_'+channel+'_Apply_all_'+lep+'.root' # prepare dict for the in put files
            EvtWeight_Fpaths_Iso[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/"+yearDir[year]+"/minitree/Mc/2J1T1_Alt/Minitree_"+channel+"_2J1T1_"+lep+".root"
    
    #print Fpaths_DNN_apply
    #print EvtWeight_Fpaths_Iso   
    if(Variable=="TMath::Log(topMass)"): Variable="lntopMass"
    # get histogram with DNN cut
    hists_corr,hists_wron =  get_histogram_with_DNN_cut(lep,year,Variable,channels_Alt, MCcut , QCDcut,Datacut , DNNCut ,EvtWeight_Fpaths_Iso,Fpaths_DNN_apply)
    if(Variable=="lntopMass"):   Variable="TMath::Log(topMass)" 
    del Fpaths_DNN_apply
    del EvtWeight_Fpaths_Iso

    hist_corr_assig = {}
    hist_wron_assig = {}
    
    #MCSF = 1 
    #QCDSF = 1
    for channel_no,channel in enumerate(channels_Alt):
        hist_corr_assig[channel] = hists_corr[channel_no].Clone()
        hist_wron_assig[channel] = hists_wron[channel_no].Clone()
        hist_corr_assig[channel].Scale(MCSF)
        hist_wron_assig[channel].Scale(MCSF)        
    
    del hists_corr
    del hists_wron
    top_sig_alt = {}
    top_bkg_alt = {}
   

    for mass in Alt_mass:
        top_sig_alt["top_sig_"+mass] = rt.TH1F('top_sig_'+mass, '', Num_bin, lest_bin, max_bin)
        top_bkg_alt["top_bkg_"+mass] = rt.TH1F('top_bkg_'+mass, '', Num_bin, lest_bin, max_bin)

        top_sig_alt["top_sig_"+mass].Add(hist_corr_assig["Tchannel_mtop"+mass])
        top_sig_alt["top_sig_"+mass].Add(hist_corr_assig["Tbarchannel_mtop"+mass])

        top_bkg_alt["top_bkg_"+mass].Add(hist_wron_assig["Tchannel_mtop"+mass])
        top_bkg_alt["top_bkg_"+mass].Add(hist_wron_assig["Tbarchannel_mtop"+mass])
        top_bkg_alt["top_bkg_"+mass].Add(hist_corr_assig["ttbar_SemiLeptonic_mtop"+mass])
        top_bkg_alt["top_bkg_"+mass].Add(hist_wron_assig["ttbar_SemiLeptonic_mtop"+mass])
        top_bkg_alt["top_bkg_"+mass].Add(hist_corr_assig["ttbar_FullyLeptonic_mtop"+mass])
        top_bkg_alt["top_bkg_"+mass].Add(hist_wron_assig["ttbar_FullyLeptonic_mtop"+mass])

    for width in Alt_width:
        top_bkg_alt["top_bkg_Nomix"+width] = rt.TH1F('top_bkg_Nomix'+width, '', Num_bin, lest_bin, max_bin)
        top_bkg_alt["top_bkg_Nomix"+width].Add(hist_corr_assig["ttbar_FullyLeptonic_widthx"+width])
        top_bkg_alt["top_bkg_Nomix"+width].Add(hist_wron_assig["ttbar_FullyLeptonic_widthx"+width])
        
        

    del hist_corr_assig
    del hist_wron_assig
 
    for mass in Alt_mass:
        hist_to_return.append(top_sig_alt["top_sig_"+mass]) 
        hist_to_return.append(top_bkg_alt["top_bkg_"+mass])
    del Alt_mass

    for width in Alt_width:
        hist_to_return.append(top_bkg_alt["top_bkg_Nomix"+width])

    del Alt_width
    del top_sig_alt
    del top_bkg_alt

    #################### Systematic samples  #################################################### 

    print "creating histogram for the systematic samples ............."
    print
    systs = ['TuneCP5CR2',  'TuneCP5CR1',   'hdampdown',    'hdampup', 'TuneCP5up',   'TuneCP5down',  'erdON' ]
   
    channels_sys_tch = []
    channels_sys_tbarch = []

    for syst in systs:
        channels_sys_tch.append("Tchannel_"+syst)
        channels_sys_tbarch.append("Tbarchannel_"+syst)

    Channels_systs = channels_sys_tch+channels_sys_tbarch      
    
    Fpaths_DNN_apply = {}
    EvtWeight_Fpaths_Iso = {}

    for channel in Channels_systs:
           Fpaths_DNN_apply[channel] = applydir+"sys_N_Alt/"+year+'_'+channel+'_Apply_all_'+lep+'.root' # prepare dict for the in put files
           EvtWeight_Fpaths_Iso[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/"+yearDir[year]+"/minitree/Mc/2J1T1_sys/Minitree_"+channel+"_2J1T1_"+lep+".root"

    #print Fpaths_DNN_apply
    #print EvtWeight_Fpaths_Iso   
    if(Variable=="TMath::Log(topMass)"): Variable="lntopMass"
    # get histogram with DNN cut
    hists_corr,hists_wron =  get_histogram_with_DNN_cut(lep,year,Variable,Channels_systs, MCcut , QCDcut, Datacut , DNNCut ,EvtWeight_Fpaths_Iso,Fpaths_DNN_apply)
    if(Variable=="lntopMass"):   Variable="TMath::Log(topMass)"
    del Fpaths_DNN_apply
    del EvtWeight_Fpaths_Iso

    hist_corr_assig = {}
    hist_wron_assig = {}

    #MCSF = 1
    #QCDSF = 1
    for channel_no,channel in enumerate(Channels_systs):
        hist_corr_assig[channel] = hists_corr[channel_no].Clone()
        hist_wron_assig[channel] = hists_wron[channel_no].Clone()
        hist_corr_assig[channel].Scale(MCSF)
        hist_wron_assig[channel].Scale(MCSF)

    del hists_corr
    del hists_wron

    top_sig_sys = {}
    top_bkg_sys = {}

    
    for syst in systs:
        top_sig_sys["top_sig_"+syst] = rt.TH1F('top_sig_'+syst, '', Num_bin, lest_bin, max_bin)
        top_bkg_sys["top_bkg_"+syst] = rt.TH1F('top_bkg_'+syst, '', Num_bin, lest_bin, max_bin)

        top_sig_sys["top_sig_"+syst].Add(hist_corr_assig["Tchannel_"+syst])
        top_sig_sys["top_sig_"+syst].Add(hist_corr_assig["Tbarchannel_"+syst])

        top_bkg_sys["top_bkg_"+syst].Add(hist_wron_assig["Tchannel_"+syst])
        top_bkg_sys["top_bkg_"+syst].Add(hist_wron_assig["Tbarchannel_"+syst])


    del hist_corr_assig
    del hist_wron_assig

   



    for syst in systs:
        hist_to_return.append(top_sig_sys["top_sig_"+syst])
        hist_to_return.append(top_bkg_sys["top_bkg_"+syst])
    del top_sig_sys
    del top_bkg_sys
    del systs"""


   #----------------- Add Altrenate mass and width samples ------------#

       

    return hist_to_return


if __name__ == "__main__":
    
    hists = Create_Workspace_input_file(lep,year,Variable) 
    
    output_file = "Hist_for_workspace/Combine_DNNFit_Input_"+Variable+"_histograms_"+year+"_"+lep+".root"
  
    outfile = rt.TFile(output_file,"recreate")
    outfile.cd()
    Dir_mu = outfile.mkdir(lep+"jets")
    Dir_mu.cd()
    
    for hist in hists:
        hist.Write()
        
    rt.gROOT.cd()

    outfile.Close()
    print("File write into "+output_file+" and saved")
    
