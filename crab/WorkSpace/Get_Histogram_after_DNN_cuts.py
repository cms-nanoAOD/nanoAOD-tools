import sys
import ROOT as rt
import numpy as np
import argparse as arg
import math
import numpy as np

#print(args)
from Histogram_discribtions import get_histogram_distciption
from Overflow_N_Underflowbin import DrawOverflow_N_DrawUnderflow 

def get_histogram_with_DNN_cut(
                                lep="mu",
                                year="UL2017",
                                Variable="lntopMass",
                                channels = ['Tchannel' , 'Tbarchannel','tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic', 'WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJetsToLL', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L'],
                                MCcut = "Xsec_wgt*LHEWeightSign*puWeight*muSF*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF*(dR_bJet_lJet>0.4)*(mtwMass>50)",
                                QCDcut = "(dR_bJet_lJet>0.4)*(mtwMass>50)*mtw_weight_50GeVCut",
                                Datacut = "(dR_bJet_lJet>0.4)*(mtwMass>50)",
                                DNNcut="(t_ch_CAsi>=0.7)",
                                Fpaths_DNN_score = {},
                                Filepaths_with_QCDWeight = {},
                                Fpaths_sys_samples = {}):

    print(type(DNNcut))
    #DNNcut="*(t_ch_CAsi>=0.3)*(t_ch_CAsi"+DNNcut+")"
    DNNcut="*"+DNNcut
    if(lep=="mu"):
            lepton = "Muon"
    elif(lep=="el"):
            lepton = "Electron"

    Variable,X_axies,Y_axies,lest_bin,max_bin,Num_bin = get_histogram_distciption(Variable)
    print(X_axies," ",Y_axies," ",lest_bin," ",max_bin," ",Num_bin)

    print
    print("############################   analising the event with the DNN cut applid ", DNNcut, "  ##################")
    print("lepton = ",lep)
    print("Variable = ",Variable)
    print
    # Initializing lists for histogram, TFile, TTree of Iso
    histo_corr_Array = []
    histo_wron_Array = []
    #intree = []
    rt.gROOT.cd()

    print(Variable)
    print("bining: ",Num_bin,", ",lest_bin,", ", max_bin)

    if(Variable=="t_ch_CAsi"):
        BINS = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,1.0]
        print("redefine assymatic histogram bins ", BINS)
        histo_corr = rt.TH1F('histo_corr', Variable, len(BINS)-1,np.array(BINS))
        histo_wron = rt.TH1F('histo_wron', Variable, len(BINS)-1,np.array(BINS))
    if("Log" in Variable and "topMass" in Variable):
        symatic_BINS = np.linspace(lest_bin,max_bin,Num_bin+1)
        Assymatic_BINS = symatic_BINS #np.concatenate(([symatic_BINS[0]], symatic_BINS[3:-3], [symatic_BINS[-1]]))
        print("redefine assymatic histogram bins ", Assymatic_BINS)
        histo_corr = rt.TH1F('histo_corr', Variable, len(Assymatic_BINS)-1,Assymatic_BINS)
        histo_wron = rt.TH1F('histo_wron', Variable, len(Assymatic_BINS)-1,Assymatic_BINS)
    else:
        histo_corr = rt.TH1F('histo_corr', Variable, Num_bin,lest_bin,max_bin)
        histo_wron = rt.TH1F('histo_wron', Variable, Num_bin,lest_bin,max_bin)

#histo_corr.Sumw2()
    MCcut_corr_Assig = MCcut+DNNcut+"*(bJetpartonFlavour*"+lepton+"Charge==5)"
    MCcut_wron_Assig = MCcut+DNNcut+"*(bJetpartonFlavour*"+lepton+"Charge!=5)"
    for channel in channels:
            print("\n",channel, "  ", Filepaths_with_QCDWeight[channel])
            print(channel, "  ", Fpaths_DNN_score[channel])
            if Fpaths_sys_samples is not None and channel in Fpaths_sys_samples: 
                 print(channel, "  ", Fpaths_sys_samples[channel])
            histo_corr.Reset()
            histo_wron.Reset()
            
            #print filenamei
            MCFile = rt.TFile.Open(Filepaths_with_QCDWeight[channel],'Read')
            intree = MCFile.Get('Events')
            intree.AddFriend ("Events",Fpaths_DNN_score[channel])
            if Fpaths_sys_samples is not None and channel in Fpaths_sys_samples: 
                intree.AddFriend ("Events",Fpaths_sys_samples[channel])
        #intree[-1].Print()
            rt.gROOT.cd()
            print("\nProjecting :",Variable," with cut : ",MCcut_corr_Assig)
            intree.Project('histo_corr', Variable, MCcut_corr_Assig)
            intree.Project('histo_wron', Variable, MCcut_wron_Assig)
            # Define the dataset
            #histo_corr_flowBin = DrawOverflow_N_DrawUnderflow(histo_corr)
            #histo_wron_flowBin = DrawOverflow_N_DrawUnderflow(histo_wron)
            histo_corr_flowBin = histo_corr
            histo_wron_flowBin = histo_wron

            rt.gROOT.cd()
            histo_corr_Array.append(histo_corr_flowBin.Clone())
            histo_wron_Array.append(histo_wron_flowBin.Clone())
            histo_corr_Array[-1].SetName(channel)
            histo_wron_Array[-1].SetName(channel)
            histo_corr_flowBin.Print()
            histo_wron_flowBin.Print()
            
            del intree
            del histo_corr_flowBin
            del histo_wron_flowBin

    histo_corr_Array[0].GetXaxis().SetTitle(X_axies)
    histo_wron_Array[0].GetXaxis().SetTitle(X_axies)

    return histo_corr_Array,histo_wron_Array

def get_dataset_with_DNN_cut(
                                lep="mu",
                                year="UL2017",
                                Variable="lntopMass",
                                channels = ['Tchannel' , 'Tbarchannel','tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic', 'WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJetsToLL', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L'],
                                MCcut = "Xsec_wgt*LHEWeightSign*puWeight*muSF*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF*(dR_bJet_lJet>0.4)*(mtwMass>50)",
                                QCDcut = "(dR_bJet_lJet>0.4)*(mtwMass>50)*mtw_weight_50GeVCut",
                                Datacut = "(dR_bJet_lJet>0.4)*(mtwMass>50)",
                                DNNcut="(t_ch_CAsi>=0.7)",
                                Fpaths_DNN_score = {},
                                Filepaths_with_QCDWeight = {}):

    print(type(DNNcut))
    #DNNcut="*(t_ch_CAsi>=0.3)*(t_ch_CAsi"+DNNcut+")"
    DNNcut="*"+DNNcut
    if(lep=="mu"):
            lepton = "Muon"
    elif(lep=="el"):
            lepton = "Electron"

    Variable,X_axies,Y_axies,lest_bin,max_bin,Num_bin = get_histogram_distciption(Variable)
    print(X_axies," ",Y_axies," ",lest_bin," ",max_bin," ",Num_bin)

    print
    print("############################   analising the event with the DNN cut applid ", DNNcut, "  ##################")
    print("lepton = ",lep)
    print("Variable = ",Variable)
    print
    # Initializing lists for histogram, TFile, TTree of Iso
    dataset_corr_Array = []
    dataset_wron_Array = []
    #intree = []
    rt.gROOT.cd()

    print(Variable)
    print("bining: ",Num_bin,", ",lest_bin,", ", max_bin)

    MCcut_corr_Assig = MCcut+DNNcut+"* (bJetpartonFlavour * "+lepton+"Charge == 5)"
    MCcut_wron_Assig = MCcut+DNNcut+"* (bJetpartonFlavour * "+lepton+"Charge != 5)"

    MCcut_corr_Assig_cut = '(dR_bJet_lJet > 0.4) * (mtwMass > 50) * (t_ch_CAsi >= 0.7) * (bJetpartonFlavour * MuonCharge == 5)'
    MCcut_wron_Assig_cut = '(dR_bJet_lJet > 0.4) * (mtwMass > 50) * (t_ch_CAsi >= 0.7) * (bJetpartonFlavour * MuonCharge != 5)'
    Variable = "topmass"

    # Define the RooRealVar variables
    topmass = rt.RooRealVar("topMass", "topMass", 100, 400)
    lnmtop = rt.RooFormulaVar("lnmtop", "TMath::Log(topMass)", rt.RooArgList(topmass))

    # cut variables
    t_ch_CAsi = rt.RooRealVar("t_ch_CAsi", "t_ch_CAsi", 0, 1)
    mtwMass = rt.RooRealVar("mtwMass", "mtwMass", 0, 1000)
    dR_bJet_lJet =  rt.RooRealVar("dR_bJet_lJet", "dR_bJet_lJet", 0, 1000)
    bJetpartonFlavour = rt.RooRealVar("bJetpartonFlavour", "bJetpartonFlavour", -6, 6)
    MuonCharge = rt.RooRealVar("MuonCharge", "MuonCharge", -2, 2)

    Xsec_wgt = rt.RooRealVar("Xsec_wgt", "Xsec_wgt", 0, 10000)
    LHEWeightSign  = rt.RooRealVar("LHEWeightSign", "LHEWeightSign", 0, 10000)
    muSF = rt.RooRealVar("muSF", "muSF", 0, 10000)
    puWeight = rt.RooRealVar("puWeight", "puWeight", 0, 10000)
    L1PreFiringWeight_Nom = rt.RooRealVar("L1PreFiringWeight_Nom", "L1PreFiringWeight_Nom", 0, 10000)
    bWeight = rt.RooRealVar("bWeight", "bWeight", 0, 10000)
    bJetPUJetID_SF = rt.RooRealVar("bJetPUJetID_SF", "bJetPUJetID_SF", 0, 10000)
    lJetPUJetID_SF = rt.RooRealVar("lJetPUJetID_SF", "lJetPUJetID_SF", 0, 10000)
    mtw_weight_50GeVCut = rt.RooRealVar("mtw_weight_50GeVCut","mtw_weight_50GeVCut", 0, 10000)

    weight_str = rt.RooFormulaVar("weight_str","Xsec_wgt*LHEWeightSign*muSF*puWeight*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF*mtw_weight_50GeVCut",rt.RooArgList(Xsec_wgt,LHEWeightSign,muSF,puWeight,L1PreFiringWeight_Nom,bWeight,bJetPUJetID_SF,lJetPUJetID_SF,mtw_weight_50GeVCut))
    print(channels)
    for channel in channels:
            print(channel, "  ", Filepaths_with_QCDWeight[channel])
            print(channel, "  ", Fpaths_DNN_score[channel])
            #print filenamei
            MCFile = rt.TFile.Open(Filepaths_with_QCDWeight[channel],'Read')
            intree = MCFile.Get('Events')
            intree.AddFriend ("Events",Fpaths_DNN_score[channel])
        #intree[-1].Print()
            rt.gROOT.cd()
            print(f'{MCcut_corr_Assig = }')

            # Define the RooArgSet with only the variables needed
            variables = rt.RooArgSet(topmass,dR_bJet_lJet, mtwMass, bJetpartonFlavour, MuonCharge,t_ch_CAsi,t_ch_CAsi,Xsec_wgt,LHEWeightSign,muSF,puWeight,L1PreFiringWeight_Nom,bWeight,bJetPUJetID_SF,lJetPUJetID_SF,mtw_weight_50GeVCut)

            # Create the RooDataSet with the given cut and weight
            dataset_corr = rt.RooDataSet("dataset_corr", "dataset_corr", variables, rt.RooFit.Import(intree), rt.RooFit.Cut(MCcut_corr_Assig_cut))
            dataset_wron = rt.RooDataSet("dataset_wron", "dataset_wron", variables, rt.RooFit.Import(intree), rt.RooFit.Cut(MCcut_wron_Assig_cut))
            weight_corr = dataset_corr.addColumn(weight_str)
            weight_wron = dataset_wron.addColumn(weight_str)
            wdataset_corr = rt.RooDataSet(dataset_corr.GetName(), dataset_corr.GetTitle(), dataset_corr, dataset_corr.get(), "", weight_corr.GetName())
            wdataset_wron = rt.RooDataSet(dataset_wron.GetName(), dataset_wron.GetTitle(), dataset_wron, dataset_wron.get(), "", weight_wron.GetName())

            dataset_corr.Print()
            wdataset_corr.Print()

            dataset_wron.Print()
            wdataset_wron.Print()

            can_mu = rt.TCanvas("ln_mtop_mu","ln_mtop_mu",1300,600)
            can_mu.Divide(2,1)
            can_mu.cd(1)
            # Construct plot frame
            frame = topmass.frame(rt.RooFit.Title("without weight"))#,rt.RooFit.Range(rt.TMath.Log(100), rt.TMath.Log(400)))
            # Plot data using sum-of-weights-squared error rather than Poisson errors
            dataset_wron.plotOn(frame)
            frame.Draw()
            can_mu.Update()

            can_mu.cd(2)
            # Construct plot frame
            wframe = topmass.frame(rt.RooFit.Title("with weight"))
            # Plot data using sum-of-weights-squared error rather than Poisson errors
            wdataset_wron.plotOn(wframe)
            wframe.Draw()
            can_mu.Update()
            can_mu.Print("data.png")

            rt.gROOT.cd()
            dataset_corr_Array.append(wdataset_corr.Clone())
            dataset_wron_Array.append(wdataset_wron.Clone())
            dataset_corr_Array[-1].SetName(channel)
            dataset_wron_Array[-1].SetName(channel)

            del intree

    """histo_corr_Array[0].GetXaxis().SetTitle(X_axies)
    histo_wron_Array[0].GetXaxis().SetTitle(X_axies)"""

    return dataset_corr_Array,dataset_wron_Array


if __name__ == '__main__':
   
        parser = arg.ArgumentParser(description='inputs discription')
        parser.add_argument('-l', '--lepton', dest='lepton', type=str, nargs=1, help="lepton [ el  mu ]")
        parser.add_argument('-y', '--year  ', dest='year', type=str, nargs=1, help="Year [ ULpreVFP2016  ULpostVFP2016  UL2017  UL2018 ]")
        parser.add_argument('-v', '--var  ', dest='var', type=str, nargs=1, help="var [ lntopMass topMass t_ch_CAsi]")

        args = parser.parse_args()

        if (args.year == None or args.lepton == None):
                print("USAGE: %s [-h] [-y <Data year> -l <lepton>]"%(sys.argv [0]))
                sys.exit (1)

        if args.year[0] not in ['UL2016preVFP', 'UL2016postVFP','UL2017','UL2018']:
                print('Error: Incorrect choice of year, use -h for help')
                exit()

        if args.lepton[0] not in ['el','mu']:
                print('Error: Incorrect choice of lepton, use -h for help')
                exit()

        lep = args.lepton[0]
        year= args.year[0]
        Variable = args.var[0]

        channels = ['Tchannel']#, 'Tbarchannel', 'tw_top', 'tw_antitop', 'Schannel',
           #'ttbar', 'WToLNu_0J', 'WToLNu_1J', 'WToLNu_2J', 'DYJetsToLL',
           #'WWTo1L1Nu2Q', 'WWTo2L2Nu', 'WZTo1L1Nu2Q', 'WZTo2L2Q', 'ZZTo2L2Q',
           #'QCD']
        
        for channel in channels:
           Fpaths_DNN_score[channel] = applydir+year+'_'+channel+'_Apply_all_'+lep+'.root' # prepare dict for the in put files
           if(year=="UL2016preVFP"): 
               Filepaths_with_QCDWeight[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_preVFP/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"
           elif(year=="UL2016postVFP"):
               Filepaths_with_QCDWeight[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_postVFP/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"
           elif(year=="UL2017"):
               Filepaths_with_QCDWeight[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/SEVENTEEN/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"
           elif(year=="UL2018"):
               Filepaths_with_QCDWeight[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/EIGHTEEN/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"

        applydir = 'DNN_output_without_mtwCut/Apply_all/' 
        hists_corr,hists_wron = get_histogram_with_DNN_cut(lep,year,Variable)
        print(len(hists))
        for hist in hists:
             hist.Print()


