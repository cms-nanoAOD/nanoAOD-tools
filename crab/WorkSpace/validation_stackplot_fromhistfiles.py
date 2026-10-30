import sys
import ROOT as rt
import argparse as arg
from mlfitNormsToText import *

parser = arg.ArgumentParser(description='inputs discription')
parser.add_argument('-l', '--lepton', dest='lepton', type=str, nargs=1, help="lepton [ el  mu ]")
parser.add_argument('-y', '--year  ', dest='year', type=str, nargs=1, help="Year [ ULpreVFP2016  ULpostVFP2016  UL2017  UL2018 ]")
#parser.add_argument('-f1', '--combine_InFile ', dest='combine_InFile', type=str, nargs=1, help="combine Input file which has histogram files i.e /home/mikumar/t3store3/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/WorkSpace/Hist_for_workspace/Combine_Input_t_ch_CAsi_histograms_UL2017_mu.root")
parser.add_argument('-v', '--var  ', dest='var', type=str, nargs=1, help="var [ mtwMass lntopMass topMass t_ch_CAsi]")
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

print("\n",args)

def propagate_rate_uncertainity(hist, uncert):
    for i in range(1,hist.GetXaxis().GetNbins()+1):
        if hist.GetBinContent(i) != 0:
            hist.SetBinError(i, hist.GetBinContent(i) * uncert * 0.01)

from Hist_style import *

def reset_stack_range(stack, xmin, xmax):
    histograms = stack.GetHists()
    for hist in histograms:
        hist.GetXaxis().SetRangeUser(xmin, xmax)

def stack_plot_from_histfile(lep='mu',dataYear='2016',Combine_InFile="Hist_for_workspace/Combine_Input_t_ch_CAsi_histograms_UL2017_mu.root",Variable="mtwMass"):
        Combine_year_tag={
                'UL2016preVFP' :  "_ULpre16",
                'UL2016postVFP' : "_ULpost16",
                'UL2017' : "_UL17",
                'UL2018' : "_UL18"} 
        if('gt' in Combine_InFile):gt_or_lt_tag = '_gt'
        if('lt' in Combine_InFile):gt_or_lt_tag = '_lt'
        tag = Combine_year_tag[year] 

        #Filename = "/home/mikumar/t3store3/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/WorkSpace/Hist_for_workspace/Combine_Input_histograms_"+year+"_"+lep+".root" 
        
        
        File = rt.TFile(Combine_InFile,"Read")
        del Combine_InFile

        #File = rt.TFile("Histogram_input_2016_Run2_controlRegionF0p2T0p82_stat_full.root","Read")
        Dir = File.GetDirectory(lep+'jets')

        top_sig = Dir.Get("top_sig_1725"+tag+gt_or_lt_tag)
        top_sig.SetFillColor(rt.kRed)
        top_sig.SetLineColor(rt.kRed)


        top_bkg = Dir.Get("top_bkg_1725"+tag+gt_or_lt_tag)
        top_bkg.SetFillColor(rt.kOrange-1)
        top_bkg.SetLineColor(rt.kOrange-1)


        EWK_bkg = Dir.Get("EWK_bkg"+tag+gt_or_lt_tag)
        EWK_bkg.SetFillColor(rt.kGreen-2)
        EWK_bkg.SetLineColor(rt.kGreen-2)


        QCD_bkg = Dir.Get("QCD_DD"+tag+gt_or_lt_tag)
        QCD_bkg.SetFillColor(rt.kGray)
        QCD_bkg.SetLineColor(rt.kGray)
        #for Bin in range(0,EWK_bkg.GetNbinsX()+1):
              #print("Bin : %s, (%s,%s)"%(Bin,EWK_bkg.GetBinContent(Bin),EWK_bkg.GetBinError(Bin)))

        tag = Combine_year_tag[year]
        #for i in range(1,top_sig.GetNbinsX()+1):
        #        print "--------------------"
        #        print "top sig : ",top_sig.GetBinContent(i), top_sig.GetBinError(i)
        #        print "top BKG : ",top_bkg.GetBinContent(i), top_bkg.GetBinError(i)
        #        print "EWK BKG : ",EWK_bkg.GetBinContent(i), EWK_bkg.GetBinError(i)
        #        print "QCD DDD : ",QCD_bkg.GetBinContent(i), QCD_bkg.GetBinError(i)
 
        print(top_sig.Integral()," ",top_bkg.Integral()," ",EWK_bkg.Integral()," ",QCD_bkg.Integral())
        
        hMC = top_sig.Clone()
        hMC.Add(top_bkg)
        hMC.Add(EWK_bkg)
        hMC.Add(QCD_bkg)
            #hMC.GetXaxis().SetRangeUser(0.0, 150)

        hMC_unct_band = hMC.Clone()
        #hMC_unct_band.GetXaxis.SetLabelSize(0.0)
        hMC_unct_band.SetLineColor(rt.kGray+3)
        hMC_unct_band.SetFillColor(rt.kGray+3)
        hMC_unct_band.SetFillStyle(3018)
        #hMC_unct_band.GetXaxis().SetRangeUser(0.0, 150)

        Data = Dir.Get("data_obs")
        Data.SetMarkerColor(1)
        Data.SetMarkerStyle(20)
        Data.SetLineColor(rt.kBlack)
            #Data.GetXaxis().SetRangeUser(0.0, 150)

        if(Variable!="lntopMass"):legend1 = rt.TLegend(0.50, 0.79, 0.85, 0.88)
        else: legend1 = rt.TLegend(0.48, 0.79, 0.83, 0.88)
        legend1.SetBorderSize(1)
        legend1.SetTextSize(0.045)
        legend1.SetLineColor(0)
        legend1.SetLineStyle(1)
        legend1.SetLineWidth(1)
        legend1.SetFillColor(0)
        legend1.SetFillStyle(1001)
        #legend.SetHeader("beNDC", "C")
        
        legend1.AddEntry(top_sig, "corr. top","f")#"Corr. top ", "f")
        legend1.AddEntry(top_bkg, "incorr. top", "f")#"InCorr. top ", "f")
        
        

        if(Variable!="lntopMass"):legend2 = rt.TLegend(0.51, 0.70, 0.85, 0.79)
        else:legend2 = rt.TLegend(0.49, 0.74, 0.83, 0.79)
        legend2.SetNColumns(2)
        legend2.SetBorderSize(1)
        legend2.SetTextSize(0.045)
        legend2.SetLineColor(0)
        legend2.SetLineStyle(1)
        legend2.SetLineWidth(1)
        legend2.SetFillColor(0)
        legend2.SetFillStyle(1001)
        #legend.SetHeader("beNDC", "C")
        legend2.AddEntry(QCD_bkg, "QCD", "f")
        legend2.AddEntry(EWK_bkg, "V+Jets, VV", "f")
        #legend2.AddEntry(Data, "Data", "ple1")

        #legend.AddEntry(hMC,"Total Unc.","f")



        myComingCanvases = rt.TCanvas("c1","", 800,700)
        myComingCanvases.cd()
        rt.TGaxis.SetMaxDigits(3)

        top_sig.GetXaxis().SetTitle(top_sig.GetXaxis().GetTitle()) 
        hs = rt.THStack("hs",";"+top_sig.GetXaxis().GetTitle()+";Events")
        hs.Add(QCD_bkg)
        hs.Add(EWK_bkg)
        hs.Add(top_bkg)
        hs.Add(top_sig)
        hs.SetMaximum(Data.GetMaximum() * 1.2)
        
        #hs.GetHistogram().GetXaxis().SetRangeUser(0.0, 150.0)
            #reset_stack_range(hs, 0.0, 150)

        if(Variable!="lntopMass"): pad1 = rt.TPad('pad1', 'pad1', 0.0, 0.195259, 1.0, 0.990683)
        else: pad1 = rt.TPad('pad1', 'pad1', 0.0, 0.0, 1.0, 0.990683)

        pad1.SetBottomMargin(0.089)
        pad1.SetTicky()
        pad1.SetTickx()
        #pad1.SetRightMargin(0.143)
        logscale_activation = False
        if('DNN' in top_sig.GetXaxis().GetTitle()):
            logscale_activation = True
            pad1.SetLogy()
        pad1.Draw()
        pad1.cd()
        myComingCanvases.Update()
        if(logscale_activation):
                fix_range = pad1.GetUymax()*100000000 
        else:    
                fix_range = Data.GetMaximum() * 1.6#pad1.GetUymax() + (pad1.GetUymax() / 3.0)
        print("fix_range = ",pad1.GetUymax())
        hs.SetMaximum(fix_range)
        hs.SetMinimum(0.001)
        #hs.GetYaxis().SetMaxDigits(3)


        hs.Draw("hist")
        legend1.Draw()
        legend2.Draw()

        CMSpreliminary = getCMSpre_tag(0.33, 0.84, 0.41, 0.88)
        CMSpreliminary.Draw("same")
        lepjet_tag = leptonjet_tag(lep,0.27, 0.80, 0.38, 0.83)
        lepjet_tag.Draw("same")
        #region_tag = getregion_tag("2J1T", 0.17, 0.92, 0.22, 0.96)
        #region_tag.Draw("same")
        yearNlumitag = year_tag(year,0.82, 0.92, 0.9, 0.96)
        yearNlumitag.Draw("same")

        myComingCanvases.Update()
        hMC_unct_band.Draw("E2;same")
        
        for Bin in range(0,hMC_unct_band.GetNbinsX()+1):
              print("Bin : %s, (%s,%s)"%(Bin,hMC_unct_band.GetBinContent(Bin),hMC_unct_band.GetBinError(Bin)))
        myComingCanvases.Update()

######################################## if it tis top mass comment out below this #######
        if(Variable!="lntopMass"):
            Data.Draw("Same;E1")
            myComingCanvases.Update()

            myComingCanvases.cd()
            pad2 = rt.TPad("pad2", "pad2", 0.0, 0.0, 1.0, 0.2621035)
            pad2.SetTopMargin(0.0)
            pad2.SetBottomMargin(0.3)
            pad2.SetGridy()
            pad2.SetTicky()
            pad2.SetTickx()
            pad2.Draw()
            pad2.cd()

            #print Data.GetBinContent(6)
            #print hMC.GetBinContent(6)
            h_ratio = rt.TGraphAsymmErrors(Data, hMC, 'pois')
            #h_ratio.Print()
            axis = h_ratio.GetXaxis()
            axis.SetLimits(Data.GetXaxis().GetXmin(), Data.GetXaxis().GetXmax())
            h_ratio.SetMarkerColor(1)
            h_ratio.SetMarkerStyle(20)
            h_ratio.SetMarkerSize(0.89)
            h_ratio.SetLineColor(rt.kBlack)


            h2_ratio = Data.Clone()
            h2_ratio.Divide(hMC)
            nbin = h2_ratio.GetXaxis().GetNbins()
            #ledge = h2_ratio.GetXaxis().GetXmin()
            #uedge = h2_ratio.GetXaxis().GetXmax()
            band = top_sig.Clone();band.Reset();band.SetTitle("")  #rt.TH1D('Band', '', nbin, ledge, uedge)
            rt.gStyle.SetOptStat(0)
            for i in range(nbin):
                band.SetBinContent(i+1, 1.0)
                if (hMC.GetBinContent(i+1)!=0 and Data.GetBinContent(i+1)!=0):
                    err = (hMC.GetBinError(i+1) * h2_ratio.GetBinContent(i+1)) / hMC.GetBinContent(i+1)
                elif (hMC.GetBinContent(i+1)!=0 and Data.GetBinContent(i+1)==0):
                    err = 1#hMC.GetBinError(i+1) / hMC.GetBinContent(i+1)
                else:
                    err = 0
                band.SetBinError(i+1, err)

            band.SetFillColor(rt.kGray+3)
            band.SetFillStyle(3354) 
            band.GetYaxis().SetTitle("Data/MC")
            band.GetXaxis().SetTitle(top_sig.GetXaxis().GetTitle()) 
            #band.GetXaxis().SetTitle(Data.GetXaxis().GetTitle())
            band.GetYaxis().CenterTitle(1) 
            band.GetYaxis().SetTitleOffset(0.35)              
            band.GetYaxis().SetTitleSize(0.12)
            band.GetXaxis().SetTitleSize(0.12)
            band.GetYaxis().SetLabelSize(0.07)
            band.GetXaxis().SetLabelSize(0.1)
            band.SetMaximum(1.545665)
            band.SetMinimum(0.464544)
            c = band.GetYaxis()
            c.SetNdivisions(10)
            c.SetTickSize(0.01)
            d = band.GetXaxis()
            d.SetNdivisions(10)
            d.SetTickSize(0.03)

            band.Draw('E2')
            h_ratio.Draw('PE1, SAME')

    ######################################## if it tis top mass comment out above this #######

            myComingCanvases.cd()
            myComingCanvases.Update()

            #raw_input()

        
        myComingCanvases.Print("Plots/"+Variable+"_validation_"+lep+"_"+dataYear+"_prefit.png")
        myComingCanvases.Print("Plots/"+Variable+"_validation_"+lep+"_"+dataYear+"_prefit.pdf")
        

if __name__ == "__main__":

        lep = args.lepton[0]
        year= args.year[0]
        Combine_InFile = f"Hist_for_workspace/Combine_Input_lntopMass_histograms_{year}_{lep}_gteq0p70_withoutDNNfit_rebin.root"
        Variable = args.var[0]
        stack_plot_from_histfile(lep,year,Combine_InFile,Variable)

