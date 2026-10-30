import ROOT as R
#import numpy as np
import sys
#NE729Q
#87088309
def get_hist(DIR,input_File):

	can = R.TCanvas("can","can") 
	#can->Divide(1,2);
	M_top_gen = R.RooRealVar("M_top_gen","m_{t,Gen}",169.0,187.0)
	#create RooDataHist
	#------------------------------------------------i
	#read the file to get the hustogrms
	Filename = R.TFile(DIR+input_File+".root","Read")
	#Get the file and director where historgrams are stored for muon final state
	Dir = Filename.GetDirectory("MC_TCH_MASS")
	#Get Mc histograms of gen top mass
	
	top_sig_mu = Dir.Get("t_mass")
	top_sig_mu.GetXaxis().SetRangeUser(169.0,174.0)
	top_sig_mu.Draw()
	raw_input()
	#return Res

def get_hitogram_from_tree(DIR,input_file,treename,h1,Var,cut):
	#read the file to get the hustogrms
        Filename = R.TFile(DIR+input_file+".root","Read")
	#Get the tree from the file 
        tree = Filename.Get(treename)
	R.gROOT.cd()
	#project histogram
	tree.Project(h1.GetName(),Var,cut)
	#h1.Draw()
	return h1
def Breitwignerfit(h,input_file):
	#define canvas
	can_Breitwigner = R.TCanvas("can_bw","can_bw") 
	#define roo var to fit
	maxBin = h.GetBinLowEdge(h.GetNbinsX()) + h.GetBinWidth(h.GetNbinsX())
	lowBin = h.GetBinLowEdge(1)
	nbins = h.GetNbinsX()

	mtop = R.RooRealVar("mtop","m_{t}",lowBin,maxBin)
	mtop.setRange("signal",lowBin,maxBin)
	#define roodata hist
	data = R.RooDataHist("data","data",R.RooArgList(mtop),h)
	#define fame to plot
        frame = mtop.frame(R.RooFit.Bins(nbins),R.RooFit.Title("mtop"))
	#plot data on fame
        data.plotOn(frame,R.RooFit.MarkerSize(0.9) )
	#deine papameter to  dfinet the breit wigner shape
	mean = R.RooRealVar("mean","mean",172.5,lowBin,maxBin)
        width = R.RooRealVar("width","width",1.31,0.1,5)
	#deine pdf
        BW = R.RooBreitWigner ("BW","BW",mtop,mean,width)
	#model = BW.asTF(R.RooArgList(mtop))
	#define Normalization
        Norm = R.RooRealVar("Norm","Norm",2000,1,100000000)
        #define model
        model = R.RooAddPdf("model","Total Model",R.RooArgList(BW),R.RooArgList(Norm))

        #RooFitResult* res;
        res = model.fitTo(data, R.RooFit.SumW2Error(R.kTRUE),R.RooFit.Save())
	#res = hist.Fit(model.GetName(), 'ILS', '')
        #draw fit on frame
        model.plotOn(frame, R.RooFit.Name("BW"))
        model.paramOn(frame,R.RooFit.Layout(0.55, 0.85, 0.85))

	#norm = BW.createIntegral(R.RooArgSet(mtop))#,R.RooFit.Range("signal"))
	#norm = h.Integral()/BW.createIntegral(R.RooArgSet(mtop)).getValV()
  	#BW.SetParameter(0, mean.getValV()*norm);
  	#BW.SetParameter(1, width.getValV()*norm);
	#print h.Integral()
	#print norm.getVal() ," ---------------------------------------------------"
	#print Norm.getVal() ," ---------------------------------------------------"
	pad1 = R.TPad('pad1', 'pad1', 0.0, 0.195259, 1.0, 0.990683)
        pad1.SetBottomMargin(0.089)
        pad1.SetTicky()
        pad1.SetTickx()
	pad1.Draw()
	pad1.cd()

        frame.Draw()
	can_Breitwigner.Update()
	#convert fit pdf into histogram
	#fitModel_hist= BW.createHistogram("fitModel",mtop, R.RooFit.Binning(25))
	#fitModel_hist.Sumw2()
	#fitModel_hist.SetNameTitle("FitModel_Hist","")
	#fitModel_hist.Scale(Norm.getVal()/fitModel_hist.Integral())


	fitData_hist= data.createHistogram("fitData",mtop, R.RooFit.Binning(20))
	fitData_hist.Sumw2()
	fitData_hist.SetNameTitle("Data_Hist","")

	fitModel_hist= model.createHistogram("fitModel",mtop, R.RooFit.Binning(20))
	fitModel_hist.Sumw2()
	fitModel_hist.SetNameTitle("Model_Hist","");
	fitModel_hist.Scale(Norm.getVal()/fitModel_hist.Integral())

	gr_mu = R.TGraphAsymmErrors(fitModel_hist,fitData_hist,"pois");



	fitModel_hist.SetMarkerStyle(20)
	fitModel_hist.SetMarkerColor(R.kRed)
		
	fitModel_hist.Draw("same")

	can_Breitwigner.cd()

	pad2 = R.TPad("pad2", "pad2", 0.0, 0.0, 1.0, 0.2621035)
	pad2.SetTopMargin(0.0)
	pad2.SetBottomMargin(0.3)
	pad2.SetGridy()
	pad2.SetTicky()
	pad2.SetTickx()
	pad2.Draw()
	pad2.cd() 
	#ratio = fitModel_hist.Clone()
	#ratio = hist.Divide(model)
	#ratio.Divide(h1)	
	#ratio = frame.pullHist();
	#ratio.SetMarkerColor(R.kBlack)i
	
	#ratio.SetStats(R.kFALSE)
	gr_mu.SetMarkerStyle(20)
	gr_mu.GetYaxis().SetTitle("Fit/MC")
        gr_mu.GetXaxis().SetTitle("m_{t}")
        gr_mu.GetYaxis().CenterTitle(1)
        gr_mu.GetYaxis().SetTitleOffset(0.3)
        gr_mu.GetYaxis().SetTitleSize(0.15)
        gr_mu.GetXaxis().SetTitleSize(0.15)
        gr_mu.GetYaxis().SetLabelSize(0.1)
        gr_mu.GetXaxis().SetLabelSize(0.15)
	gr_mu.GetXaxis().SetRangeUser(lowBin,maxBin)
	gr_mu.SetMaximum(1.35)
        gr_mu.SetMinimum(0.65)
        c = gr_mu.GetYaxis()
        c.SetNdivisions(4)
        c.SetTickSize(0.01)
        d = gr_mu.GetXaxis()
        d.SetNdivisions(20)
        d.SetTickSize(0.03)
	
	gr_mu.Draw("APE1")
	can_Breitwigner.Update()
        can_Breitwigner.Draw()
	can_Breitwigner.Print("Plots/BW_fit_"+input_file+".png")
	raw_input()
        #return res; 
def kinfitresiltCOmpaire(DIR,input_file,treename,h1,Var,cut):

	h1.Sumw2()
        cut = ""

        hist = get_hitogram_from_tree(DIR,input_file,treename,h1,Var+"_gen",cut)
        hist_gen = hist.Clone() 
        hist_gen.SetLineColor(R.kRed)
      	hist_gen.SetLineWidth(2)
	hist_gen.SetTitle("")
	hist_gen.Scale(1/hist_gen.Integral())
	if(hist_gen.Integral()>1): hist_gen.Scale(1/hist_gen.Integral())

  	hist_gen.GetXaxis().SetTitle(Var)
	
        hist = get_hitogram_from_tree(DIR,input_file,treename,h1,Var,cut)
        hist_reco = hist.Clone()
        hist_reco.SetLineColor(R.kGreen)
	hist_reco.SetLineWidth(2)
	if(hist_reco.Integral()>1): hist_reco.Scale(1/hist_reco.Integral())

        hist = get_hitogram_from_tree(DIR,input_file,treename,h1,Var+"_kin",cut)
        hist_kin = hist.Clone()
        hist_kin.SetLineColor(R.kBlue)
	hist_kin.SetLineWidth(2)
	if(hist_kin.Integral()>1): hist_kin.Scale(1/hist_kin.Integral())
	

	can = R.TCanvas("can","can",600,600)
        can.cd()
	R.gStyle.SetOptStat(0)

        #hist_gen.Draw("hist")
        hist_reco.Draw("hist")
        hist_kin.Draw("hist;same")

	legend = R.TLegend(0.60193646, 0.5548435, 0.8093552, 0.79026143)
        legend.SetBorderSize(1)
        legend.SetTextSize(0.045)
        legend.SetLineColor(0)
        legend.SetLineStyle(1)
        legend.SetLineWidth(1)
        legend.SetFillColor(0)
        legend.SetFillStyle(1001)
        #legend.SetHeader("beNDC", "C")
        legend.AddEntry(hist_gen, "Gen", "l")
        legend.AddEntry(hist_reco, "Reco", "l")
        legend.AddEntry(hist_kin, "KinFit", "l")

	legend.Draw("same")

	canvasname = "Plots/"+Var+"_KinFit_Vs_Gen&reco"
        can.Print(canvasname+".png")
		
        raw_input()



if __name__ == "__main__":
	#get_hist("top_mass_reconstracted_el.root")
	#DIR = "/grid_mnt/t3storage3/mikumar/Run2/SIXTEEN/minitree/Mc/Gen/"
	#DIR = "/grid_mnt/t3storage3/mikumar/Run2/SIXTEEN/minitree/Mc/Gen/"
	#DIR = "/home/mikumar/t3store3/workarea/Nanoaod_tools/CMSSW_9_4_9/src/PhysicsTools/NanoAODTools/crab/Gen_Study/"
	DIR = "/home/mikumar/t3store3/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/Gen_Study/"
	input_file = "Minitree_Tbarchannel_2J1T1_mu_Skim"
	treename = "Events"
	Var = "topMass"

	if(Var=="MuonPt" ):
	     h1 = R.TH1D(Var,Var,30,0.0,150.0)
	elif(Var=="Pt_nu" or Var=="Px_nu" or  Var=="Py_nu" or  Var=="Pz_nu"):
             h1 = R.TH1D(Var,Var,40,0.0,400.0)
	elif(Var=="MuonEta"):
             h1 = R.TH1D(Var,Var,25,-2.5,2.5)
	elif(Var=="MuonPhi"):
             h1 = R.TH1D(Var,Var,50,-5,5)
	elif(Var=="MuonMass" or Var=="Mass_nu" ):
             h1 = R.TH1D(Var,Var,50,-1,1)
	elif(Var=="mtwMass"):
	     h1 = R.TH1D(Var,Var,20,0,200)
	elif(Var=="topPt"):
             h1 = R.TH1D(Var,Var,20,0,200)
	elif(Var=="topMass"):
             h1 = R.TH1D(Var,Var,80,0,400)

	cut = ""
	kinfitresiltCOmpaire(DIR,input_file,treename,h1,Var,cut)




	#for input_file in ["Minitree_Tbarchannel_2J1T1_mu_Skim"]:#["Minitree_TTTo2L2Nu_widthx1p15"]:#["Minitree_Tbarchannel_wtop1p3"]:#,"Minitree_Tbarchannel_wtop1p15","Minitree_Tbarchannel_wtop0p85","Minitree_Tbarchannel_wtop0p7","Minitree_Tchannel_wtop1p15","Minitree_Tchannel_wtop0p85","Minitree_Tchannel_wtop0p7"]:
	#for input_file in ["tCh_top_w0p7_full"]:
		#hist = get_hitogram_from_tree(DIR,input_file,treename,h1,Var,cut)
		#hist.Scale(1/hist.Integral())
		#Breitwignerfit(hist,input_file)
		#BreitwignerWOfit(hist)
		#hist.Draw("hist")"""
	#for input_file in ["tCh_top_w0p7_full"]:
		#hist = get_hist(DIR,input_file)
	
