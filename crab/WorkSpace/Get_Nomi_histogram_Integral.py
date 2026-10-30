import ROOT as rt
import numpy as np
#import scipy.integrate as sp
import argparse as arg
import math
from Histogram_discribtions import get_histogram_distciption

def Nomi_QCD_NoNQCD_Integral(lep="mu",year="UL2017",Variable="mtwMass",MCcut = "Xsec_wgt*LHEWeightSign*puWeight*muSF*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF*(dR_bJet_lJet>0.4)*(mtwMass>50)",Datacut = "(dR_bJet_lJet>0.4)*(mtwMass>50)",EvtWeight_Fpaths_Iso = {},Data_AntiIso_Fpath={},Fpaths_DNN_score = {}):
    print
    print("calculating integral of qcd and non qcd without dnn cut .. .. .. .. .. .. ... .......")
    if(lep=="mu"):
            lepton = "Muon"
    elif(lep=="el"):
            lepton = "Electron"
    #print(lepton)
    
    Variable,X_axies,Y_axies,lest_bin,max_bin,Num_bin = get_histogram_distciption(Variable)
    print(Variable, X_axies," ",Y_axies," ",lest_bin," ",max_bin," ",Num_bin)
    
    channels = ['Tchannel' , 'Tbarchannel','tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic', 'WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJetsToLL', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L', 'QCD']
    
    hist = {}
    WAssihist = {}
    infiles = {}
    intree = {}

    if(Variable=="t_ch_CAsi"):
        BINS = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,1.0]
        print("redefine assymatic histogram bins ", BINS)
        hist_tch_CAssig_temp = rt.TH1F('hist_sig_CAssig_temp', '', len(BINS)-1,np.array(BINS))
        hist_tch_WAssig_temp = rt.TH1F('hist_sig_WAssig_temp', '', len(BINS)-1,np.array(BINS))
        hist_ttbar_CAssig_temp = rt.TH1F('hist_bkg_CAssig_temp', '', len(BINS)-1,np.array(BINS))
        hist_ttbar_WAssig_temp = rt.TH1F('hist_big_WAssig_temp', '', len(BINS)-1,np.array(BINS))
        hist_EWK_temp = rt.TH1F('hist_EWK_temp', '', len(BINS)-1,np.array(BINS))
        hist_QCD_temp = rt.TH1F('hist_QCD_temp', '', len(BINS)-1,np.array(BINS))      
   
    else: 
        hist_tch_CAssig_temp = rt.TH1F('hist_sig_CAssig_temp', '', Num_bin, lest_bin, max_bin)
        hist_tch_WAssig_temp = rt.TH1F('hist_sig_WAssig_temp', '', Num_bin, lest_bin, max_bin)
        hist_ttbar_CAssig_temp = rt.TH1F('hist_bkg_CAssig_temp', '', Num_bin, lest_bin, max_bin)
        hist_ttbar_WAssig_temp = rt.TH1F('hist_big_WAssig_temp', '', Num_bin, lest_bin, max_bin)
        hist_EWK_temp = rt.TH1F('hist_EWK_temp', '', Num_bin, lest_bin, max_bin)
        hist_QCD_temp = rt.TH1F('hist_QCD_temp', '', Num_bin, lest_bin, max_bin)
    rt.gStyle.SetOptStat(0)
    
    hist_tch_CAssig_temp.SetLineColor(rt.kRed);hist_tch_CAssig_temp.SetLineWidth(2)
    hist_tch_CAssig_temp.GetXaxis().SetTitle(X_axies)
    hist_tch_CAssig_temp.GetYaxis().SetTitle(Y_axies)  
    
    hist_tch_WAssig_temp.SetLineColor(rt.kBlue); hist_tch_WAssig_temp.SetLineWidth(2)
    hist_ttbar_CAssig_temp.SetLineColor(rt.kOrange-1); hist_ttbar_CAssig_temp.SetLineWidth(2)
    hist_ttbar_WAssig_temp.SetLineColor(rt.kCyan+1); hist_ttbar_WAssig_temp.SetLineWidth(2)
    hist_EWK_temp.SetLineColor(rt.kMagenta); hist_EWK_temp.SetLineWidth(2)
    hist_QCD_temp.SetLineColor(rt.kGray); hist_QCD_temp.SetLineWidth(2)
    print
    print(EvtWeight_Fpaths_Iso )
    for channel in channels:
        if(channel=="QCD"): 
                print(channel, " ", Data_AntiIso_Fpath)
                print(channel, " ", Fpaths_DNN_score[channel])
                infiles[channel] = rt.TFile(Data_AntiIso_Fpath, 'READ')
        else:
                print(channel, " ", EvtWeight_Fpaths_Iso[channel])
                print(channel, " ", Fpaths_DNN_score[channel])
                infiles[channel] = rt.TFile(EvtWeight_Fpaths_Iso[channel], 'READ')
    
        intree[channel] = infiles[channel].Get('Events')
        intree[channel].AddFriend("Events",Fpaths_DNN_score[channel])
        if(Variable=="t_ch_CAsi"):
                BINS = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,1.0]
                print("redefine assymatic histogram bins ", BINS)
                hist[channel] = rt.TH1F('hist' + channel, '',len(BINS)-1,np.array(BINS))
                WAssihist[channel] = rt.TH1F('temphist' + channel, '', len(BINS)-1,np.array(BINS))
        else:
                hist[channel] = rt.TH1F('hist' + channel, '', Num_bin, lest_bin, max_bin)
                WAssihist[channel] = rt.TH1F('temphist' + channel, '', Num_bin, lest_bin, max_bin)
    
        if(channel=='Tchannel' or channel=='Tbarchannel'):
            Mccut_corr_assi = MCcut +"*(bJetpartonFlavour*"+lepton+"Charge==5)"
            #print "Mccut_corr_assi : ",Mccut_corr_assi
            intree[channel].Project('hist' + channel, Variable, Mccut_corr_assi) 
            Mccut_wron_assi = MCcut+"*(bJetpartonFlavour*"+lepton+"Charge!=5)"
            intree[channel].Project('temphist' + channel, Variable,Mccut_wron_assi)
            #print "Mccut_wron_assi : ",Mccut_wron_assi
            hist_tch_CAssig_temp.Add(hist[channel])
            hist_tch_WAssig_temp.Add(WAssihist[channel])
            #hist[channel].Print()
            #WAssihist[channel].Print()
        elif(channel=='tw_top'  or channel=='tw_antitop' or channel=='Schannel' or channel=='ttbar_SemiLeptonic' or channel=='ttbar_FullyLeptonic'):
            intree[channel].Project('hist' + channel, Variable,MCcut+"*(bJetpartonFlavour*"+lepton+"Charge==5)")
            intree[channel].Project('temphist' + channel, Variable,MCcut+"*(bJetpartonFlavour*"+lepton+"Charge!=5)")
            hist_ttbar_CAssig_temp.Add(hist[channel])
            hist_ttbar_WAssig_temp.Add(WAssihist[channel])
            #hist[channel].Print()
            #WAssihist[channel].Print()
        elif(channel=='QCD'):
            intree[channel].Project('hist' + channel, Variable,Datacut)
            hist_QCD_temp.Add(hist[channel])
            #hist_QCD_temp.Print()
        else:
            #print MCcut
            intree[channel].Project('hist' + channel,Variable,MCcut)
            hist_EWK_temp.Add(hist[channel])
            #hist[channel].Print()
    
    NonQCD_Inte = (hist_tch_CAssig_temp.Integral(0,Num_bin+1)+hist_tch_WAssig_temp.Integral(0,Num_bin+1)+hist_ttbar_CAssig_temp.Integral(0,Num_bin+1)+hist_ttbar_WAssig_temp.Integral(0,Num_bin+1)+hist_EWK_temp.Integral(0,Num_bin+1))
    QCD_Inte = (hist_QCD_temp.Integral(0,Num_bin+1))
    print 
    print("NonQCD_Inte: ",NonQCD_Inte," QCD_Inte: ",QCD_Inte)
    
    return NonQCD_Inte,QCD_Inte

def Nomi_QCD_Integral(lep="mu",year="UL2017",Variable="mtwMass",Datacut = "(dR_bJet_lJet>0.4)*(mtwMass>50)",Data_AntiIso_Fpath={}, Fpaths_DNN_score = {}):
    print
    print("calculating integral of qcd without dnn cut .. .. .. .. .. .. ... .......")
    if(lep=="mu"):
            lepton = "Muon"
    elif(lep=="el"):
            lepton = "Electron"
    #print(lepton)
    
    Variable,X_axies,Y_axies,lest_bin,max_bin,Num_bin = get_histogram_distciption(Variable)
    print(X_axies," ",Y_axies," ",lest_bin," ",max_bin," ",Num_bin)

    channel = "QCD"
    hist = {}
    infiles = {}
    intree = {}


    if(Variable=="t_ch_CAsi"):
        BINS = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,1.0]
        print("redefine assymatic histogram bins ", BINS)
        hist_QCD_temp = rt.TH1F('hist_QCD_temp', '', len(BINS)-1,np.array(BINS))      
   
    else: 
        hist_QCD_temp = rt.TH1F('hist_QCD_temp', '', Num_bin, lest_bin, max_bin)
    rt.gStyle.SetOptStat(0)
    

    hist_QCD_temp.SetLineColor(rt.kGray); hist_QCD_temp.SetLineWidth(2)
    if(channel=="QCD"):
        print(channel, " ", Data_AntiIso_Fpath)
        print(channel, " ", Fpaths_DNN_score[channel])
        infiles[channel] = rt.TFile(Data_AntiIso_Fpath, 'READ')
    
    intree[channel] = infiles[channel].Get('Events')
    intree[channel].AddFriend("Events",Fpaths_DNN_score[channel])
    if(Variable=="t_ch_CAsi"):
         BINS = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,1.0]
         print("redefine assymatic histogram bins ", BINS)
         hist[channel] = rt.TH1F('hist' + channel, '',len(BINS)-1,np.array(BINS))
    else:
         hist[channel] = rt.TH1F('hist' + channel, '', Num_bin, lest_bin, max_bin)

    if(channel=='QCD'):
         intree[channel].Project('hist' + channel, Variable,Datacut)
         hist_QCD_temp.Add(hist[channel])
         #hist_QCD_temp.Print()
        
    QCD_Inte = (hist_QCD_temp.Integral(0,Num_bin+1))
    print 
    print(" QCD_Inte: ",QCD_Inte)

    return QCD_Inte

def Nomi_NoNQCD_Integral(lep="mu",year="UL2017",Variable="mtwMass",MCcut = "Xsec_wgt*LHEWeightSign*puWeight*muSF*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF*(dR_bJet_lJet>0.4)*(mtwMass>50)",EvtWeight_Fpaths_Iso = {},Fpaths_DNN_score = {}):
    print
    print("calculating integral of qcd and non qcd without dnn cut .. .. .. .. .. .. ... .......")
    if(lep=="mu"):
            lepton = "Muon"
    elif(lep=="el"):
            lepton = "Electron"
    #print(lepton)
    
    Variable,X_axies,Y_axies,lest_bin,max_bin,Num_bin = get_histogram_distciption(Variable)
    print(Variable, X_axies," ",Y_axies," ",lest_bin," ",max_bin," ",Num_bin)
    
    channels = ['Tchannel' , 'Tbarchannel','tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic', 'WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJets', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L' ]
    
    hist = {}
    WAssihist = {}
    infiles = {}
    intree = {}

    if(Variable=="t_ch_CAsi"):
        BINS = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,1.0]
        print("redefine assymatic histogram bins ", BINS)
        hist_tch_CAssig_temp = rt.TH1F('hist_sig_CAssig_temp', '', len(BINS)-1,np.array(BINS))
        hist_tch_WAssig_temp = rt.TH1F('hist_sig_WAssig_temp', '', len(BINS)-1,np.array(BINS))
        hist_ttbar_CAssig_temp = rt.TH1F('hist_bkg_CAssig_temp', '', len(BINS)-1,np.array(BINS))
        hist_ttbar_WAssig_temp = rt.TH1F('hist_big_WAssig_temp', '', len(BINS)-1,np.array(BINS))
        hist_EWK_temp = rt.TH1F('hist_EWK_temp', '', len(BINS)-1,np.array(BINS))
   
    else: 
        hist_tch_CAssig_temp = rt.TH1F('hist_sig_CAssig_temp', '', Num_bin, lest_bin, max_bin)
        hist_tch_WAssig_temp = rt.TH1F('hist_sig_WAssig_temp', '', Num_bin, lest_bin, max_bin)
        hist_ttbar_CAssig_temp = rt.TH1F('hist_bkg_CAssig_temp', '', Num_bin, lest_bin, max_bin)
        hist_ttbar_WAssig_temp = rt.TH1F('hist_big_WAssig_temp', '', Num_bin, lest_bin, max_bin)
        hist_EWK_temp = rt.TH1F('hist_EWK_temp', '', Num_bin, lest_bin, max_bin)
    rt.gStyle.SetOptStat(0)
    
    hist_tch_CAssig_temp.SetLineColor(rt.kRed);hist_tch_CAssig_temp.SetLineWidth(2)
    hist_tch_CAssig_temp.GetXaxis().SetTitle(X_axies)
    hist_tch_CAssig_temp.GetYaxis().SetTitle(Y_axies)  
    
    hist_tch_WAssig_temp.SetLineColor(rt.kBlue); hist_tch_WAssig_temp.SetLineWidth(2)
    hist_ttbar_CAssig_temp.SetLineColor(rt.kOrange-1); hist_ttbar_CAssig_temp.SetLineWidth(2)
    hist_ttbar_WAssig_temp.SetLineColor(rt.kCyan+1); hist_ttbar_WAssig_temp.SetLineWidth(2)
    hist_EWK_temp.SetLineColor(rt.kMagenta); hist_EWK_temp.SetLineWidth(2)
    print
    for channel in channels:
        print(channel, " ", EvtWeight_Fpaths_Iso[channel])
        print(channel, " ", Fpaths_DNN_score[channel])
        infiles[channel] = rt.TFile(EvtWeight_Fpaths_Iso[channel], 'READ')
    
        intree[channel] = infiles[channel].Get('Events')
        intree[channel].AddFriend("Events",Fpaths_DNN_score[channel])
        if(Variable=="t_ch_CAsi"):
                BINS = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,1.0]
                print("redefine assymatic histogram bins ", BINS)
                hist[channel] = rt.TH1F('hist' + channel, '',len(BINS)-1,np.array(BINS))
                WAssihist[channel] = rt.TH1F('temphist' + channel, '', len(BINS)-1,np.array(BINS))
        else:
                hist[channel] = rt.TH1F('hist' + channel, '', Num_bin, lest_bin, max_bin)
                WAssihist[channel] = rt.TH1F('temphist' + channel, '', Num_bin, lest_bin, max_bin)
    
        if(channel=='Tchannel' or channel=='Tbarchannel'):
            Mccut_corr_assi = MCcut +"*(bJetpartonFlavour*"+lepton+"Charge==5)"
            #print "Mccut_corr_assi : ",Mccut_corr_assi
            intree[channel].Project('hist' + channel, Variable, Mccut_corr_assi) 
            Mccut_wron_assi = MCcut+"*(bJetpartonFlavour*"+lepton+"Charge!=5)"
            intree[channel].Project('temphist' + channel, Variable,Mccut_wron_assi)
            #print "Mccut_wron_assi : ",Mccut_wron_assi
            hist_tch_CAssig_temp.Add(hist[channel])
            hist_tch_WAssig_temp.Add(WAssihist[channel])
            #hist[channel].Print()
            #WAssihist[channel].Print()
        elif(channel=='tw_top'  or channel=='tw_antitop' or channel=='Schannel' or channel=='ttbar_SemiLeptonic' or channel=='ttbar_FullyLeptonic'):
            intree[channel].Project('hist' + channel, Variable,MCcut+"*(bJetpartonFlavour*"+lepton+"Charge==5)")
            intree[channel].Project('temphist' + channel, Variable,MCcut+"*(bJetpartonFlavour*"+lepton+"Charge!=5)")
            hist_ttbar_CAssig_temp.Add(hist[channel])
            hist_ttbar_WAssig_temp.Add(WAssihist[channel])
            #hist[channel].Print()
            #WAssihist[channel].Print()
        else:
            #print MCcut
            intree[channel].Project('hist' + channel,Variable,MCcut)
            hist_EWK_temp.Add(hist[channel])
            #hist[channel].Print()
    
    NonQCD_Inte = (hist_tch_CAssig_temp.Integral(0,Num_bin+1)+hist_tch_WAssig_temp.Integral(0,Num_bin+1)+hist_ttbar_CAssig_temp.Integral(0,Num_bin+1)+hist_ttbar_WAssig_temp.Integral(0,Num_bin+1)+hist_EWK_temp.Integral(0,Num_bin+1))
    print 
    print("NonQCD_Inte: ",NonQCD_Inte)
    
    return NonQCD_Inte

if __name__ == "__main__":

        parser = arg.ArgumentParser(description='inputs discription')
        parser.add_argument('-l', '--lepton', dest='lepton', type=str, nargs=1, help="lepton [ el  mu ]")
        parser.add_argument('-y', '--year  ', dest='year', type=str, nargs=1, help="Year [ ULpreVFP2016  ULpostVFP2016  UL2017  UL2018 ]")
        parser.add_argument('-v', '--var  ', dest='var', type=str, nargs=1, help="var [ lntopMass topMass t_ch_CAsi]")

        args = parser.parse_args()

        if (args.year == None or args.lepton == None):
                print("USAGE: %s [-h] [-y <Data year> -l <lepton>]"%(sys.argv [0]))
                sys.exit (1)

        if args.year[0] not in ['ULpreVFP2016', 'ULpostVFP2016','UL2017','UL2018']:
                print('Error: Incorrect choice of year, use -h for help')
                exit()

        if args.lepton[0] not in ['el','mu']:
                print('Error: Incorrect choice of lepton, use -h for help')
                exit()

        #print
        #print(args)

        lep = args.lepton[0]
        year= args.year[0]
        Variable = args.var[0]



        NonQCD_Inte,QCD_Inte =  Nomi_QCD_NoNQCD_Integral(lep,year,Variable)
        print("NonQCD_Inte: ",NonQCD_Inte," QCD_Inte: ",QCD_Inte)

        NonQCD_Inte,QCD_Inte =  Nomi_QCD_Integral(lep,year,Variable)
        print("QCD_Inte: ",QCD_Inte)    
        #c1.Print('Plots/'+year+'_'+lep+'_'+Variable+'.png')#'_cut_tch_CAssig_p_ttbar_CAssigGT0p4.png')
        #c1.Print('Plots/'+year+'_'+lep+'_'+Variable+'.pdf')#'_cut_tch_CAssig_p_ttbar_CAssigGT0p4.pdf')


      
