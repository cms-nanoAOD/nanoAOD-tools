#import scipy.integrate as sp
import math
import sys
import argparse as arg
import ROOT as R
 
from Get_Histogram_after_DNN_cuts import get_histogram_with_DNN_cut
from Get_Nomi_histogram_Integral import Nomi_QCD_Integral 
from Overflow_N_Underflowbin import DrawOverflow_N_DrawUnderflow
from Get_Additive_sys_hitogram import Get_samples_hist_wo_NonQCD_Norm

def propagate_rate_uncertainity(hist, uncert):
    for i in range(1,hist.GetXaxis().GetNbins()+1):
        if hist.GetBinContent(i) != 0:
            hist.SetBinError(i, hist.GetBinContent(i) * uncert * 0.01)

################################# DNN scale ################ get from the lepton chage ratio max diff of Data amd MC ###########

def compare_shapes(lep="mu",year="UL2017",Variable="lntopMass",region="3J2T"):
    if(lep=="mu"):
            lepton = "Muon"
    elif(lep=="el"):
            lepton = "Electron"
    print(lepton)
    

    #####  Nominal MC samples #######

    print("\n #################   Nominal hist ############## \n")
    hist_to_return = [] 
    applydir = '/home/mikumar/t3store3/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/DNN/DNN_output_without_mtwCut/Apply_all/'
    MCcut = "Xsec_wgt*LHEWeightSign*puWeight*"+lep+"SF*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF*(dR_bJet_lJet>0.4)*(mtwMass>50)" 
    Datacut = "(dR_bJet_lJet>0.4)*(mtwMass>50)"
    DNNcut_str = "*(t_ch_CAsi>="+DNNCut+")" 
    yearDir={
                'ULpreVFP2016' :  "SIXTEEN_preVFP",
                'ULpostVFP2016' : "SIXTEEN_postVFP",
                'UL2017' : "SEVENTEEN",
        } 

    if(region=="2J1L0T"): channels = ['WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJets', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L']
    elif(region=="3J2T"): channels = ['tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic']
    elif (region=="2J1T"): channels = ['tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic','WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJets', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L']

    else:
	print("we are not using any shape from "+region+" region , teminating the code")
	sys.exit(1)

    hists_Nomi = Get_samples_hist_wo_NonQCD_Norm(lep=lep,year=year,Variable=Variable,MCcut = MCcut,Channels=channels,region=region,DNNCut=DNNCut,hist_sys_name="")
    for Hist in hists_Nomi:
        hist_to_return.append(Hist.Clone())
    del hists_Nomi

    return hist_to_return


if __name__ == "__main__":
    parser = arg.ArgumentParser(description='inputs discription')
    parser.add_argument('-l', '--lepton', dest='lepton', type=str, nargs=1, help="lepton [ el  mu ]")
    parser.add_argument('-y', '--year  ', dest='year', type=str, nargs=1, help="Year [ ULpreVFP2016  ULpostVFP2016  UL2017  UL2018 ]")
    parser.add_argument('-v', '--var  ', dest='var', type=str, nargs=1, help="var [ lntopMass topMass t_ch_CAsi]")
    parser.add_argument('-DC', '--DNNCut  ', dest='DNNCut', type=str, nargs=1, help="if need to apply DNNCut [ 0.0 ,0.7]")
    parser.add_argument('-r', '--region', dest='regions', type=str, nargs=1, help="sample [ 2J1T , 3J1T , 2J1L0T , 3J2T , 2J0T ]")

    args = parser.parse_args()

    if (args.year == None or args.lepton == None):
        print("USAGE: %s [-h] [-y <Data year> -l <lepton>] -v <variable>"%(sys.argv [0]))
        sys.exit (1)

    if args.year[0] not in ['ULpreVFP2016', 'ULpostVFP2016','UL2017','UL2018']:
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
    DNNCut = args.DNNCut[0]
    region = args.regions[0]
 
    hists_2J1T = compare_shapes(lep,year,Variable,"2J1T")
    hists_comp = compare_shapes(lep,year,Variable,region) #return Tchannel, ttbar, wjets 

    legend = R.TLegend(0.40193646, 0.5548435, 0.8093552, 0.79026143)
    legend.SetBorderSize(1)
    legend.SetTextSize(0.045)
    legend.SetLineColor(0)
    legend.SetLineStyle(1)
    legend.SetLineWidth(1)
    legend.SetFillColor(0)
    legend.SetFillStyle(1001)
    
    if(region == "3J2T"):
        hist_comp = hists_comp[1]; hist_comp.Scale(1/hist_comp.Integral())
        hist_2J1T = hists_2J1T[1]; hist_2J1T.Scale(1/hist_2J1T.Integral())
        legend.AddEntry(hist_comp, "(3J2T) ttbar shape", "l")
        legend.AddEntry(hist_2J1T, "(2J1T) ttbar shape","l")
    if(region == "2J1L0T"):
        hist_comp = hists_comp[2]; hist_comp.Scale(1/hist_comp.Integral())
        hist_2J1T = hists_2J1T[2]; hist_2J1T.Scale(1/hist_2J1T.Integral())
        legend.AddEntry(hist_comp, "(2J1L0T) w+jets shape", "l")
        legend.AddEntry(hist_2J1T, "(2J1T) w+jets shape","l")

    hist_comp.SetLineColor(R.kRed)
    hist_2J1T.SetLineColor(R.kBlue)
    
    myComingCanvases = R.TCanvas("c1","", 600,600,600,600)
    R.gStyle.SetOptStat(0)
    myComingCanvases.cd()
    R.TGaxis.SetMaxDigits(3)
    
    pad1 = R.TPad('pad1', 'pad1', 0.0, 0.195259, 1.0, 0.990683)
    pad1.SetBottomMargin(0.089)
    pad1.SetTicky()
    pad1.SetTickx()
    pad1.Draw()
    pad1.cd()
    hist_comp.SetTitle("")
    hist_comp.GetYaxis().SetTitle("Unit Normalization") 
    hist_comp.Draw("hist")
    hist_2J1T.Draw("hist;same")
    legend.Draw("same")
    
    myComingCanvases.Update()

    myComingCanvases.cd()
    pad2 = R.TPad("pad2", "pad2", 0.0, 0.0, 1.0, 0.2621035)
    pad2.SetTopMargin(0.0)
    pad2.SetBottomMargin(0.3)
    pad2.SetGridy()
    pad2.SetTicky()
    pad2.SetTickx()
    pad2.Draw()
    pad2.cd()

    h2_ratio = hist_comp.Clone()
    h2_ratio.Divide(hist_2J1T)
    
    h2_ratio.SetTitle("")
    h2_ratio.GetYaxis().SetTitle("Ratio") 
    h2_ratio.GetXaxis().SetTitle(hist_2J1T.GetXaxis().GetTitle()) 
    h2_ratio.GetYaxis().CenterTitle(1) 
    h2_ratio.GetYaxis().SetTitleOffset(0.35)              
    h2_ratio.GetYaxis().SetTitleSize(0.12)
    h2_ratio.GetXaxis().SetTitleSize(0.12)
    h2_ratio.GetYaxis().SetLabelSize(0.07)
    h2_ratio.GetXaxis().SetLabelSize(0.1)
    h2_ratio.SetMaximum(1.5)
    h2_ratio.SetMinimum(0.5)
    c = h2_ratio.GetYaxis()
    c.SetNdivisions(10)
    c.SetTickSize(0.01)
    d = h2_ratio.GetXaxis()
    d.SetNdivisions(10)
    d.SetTickSize(0.03)
    
    h2_ratio.Draw('PE1')
    myComingCanvases.Update()
    

    raw_input()
    

    
        
   
    
