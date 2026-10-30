import ROOT as R
#import numpy as np
import sys
#NE729Q
#87088309
def get_hist(input_File):

	can = R.TCanvas("can","can") 
	#can->Divide(1,2);
	M_top_gen = R.RooRealVar("M_top_gen","m_{t,Gen}",166.0,179)
	#create RooDataHist
	#------------------------------------------------i
	#read the file to get the hustogrms
	Filename = R.TFile(input_File,"Read")
	#Get the file and director where historgrams are stored for muon final state
	Dir = Filename.GetDirectory("Histograms")
	#Get Mc histograms of gen top mass
	
	top_sig_mu = Dir.Get("top_mass")

	top_sig_mu.Draw()
	input()
	#return Res

def get_hitogram_from_tree(input_file,treename,h1,Var,cut):
	#read the file to get the hustogrms
        Filename = R.TFile(input_file,"Read")
	#Get the tree from the file 
        tree = Filename.Get(treename)
	R.gROOT.cd()
	#project histogram
	tree.Project(h1.GetName(),Var,cut)
	#h1.Draw()
	return h1
def Breitwignerfit(h):
	#define canvas
	can_Breitwigner = R.TCanvas("can_bw","can_bw") 
	#define roo var to fit
	mtop = R.RooRealVar("mtop","m_{t}",166.0,179.0)
	mtop.setRange("signal",166.0,179.0)
	#define roodata hist
	data = R.RooDataHist("data","data",R.RooArgList(mtop),h)
	#define fame to plot
        frame = mtop.frame(R.RooFit.Bins(52),R.RooFit.Title("mtop"))
	#plot data on fame
        data.plotOn(frame,R.RooFit.MarkerSize(0.9) )
	#deine papameter to  dfinet the breit wigner shape
	mean = R.RooRealVar("mean","mean",172.5,171.0,175)
        width = R.RooRealVar("width","width",1.31,0.5,2)
	#deine pdf
        BW = R.RooBreitWigner ("BW","BW",mtop,mean,width)
	#define Normalization
        Norm = R.RooRealVar("Norm","Norm",2000,1,100000)
        #define model
        model = R.RooAddPdf("model","Total Model",R.RooArgList(BW),R.RooArgList(Norm))

        #RooFitResult* res;
        res = model.fitTo(data, R.RooFit.SumW2Error(R.kTRUE),R.RooFit.Save())
        #draw fit on frame
        model.plotOn(frame, R.RooFit.Name("BW"))
        model.paramOn(frame,R.RooFit.Layout(0.55, 0.85, 0.85))

	#norm = BW.createIntegral(R.RooArgSet(mtop))#,R.RooFit.Range("signal"))
	#norm = h.Integral()/BW.createIntegral(R.RooArgSet(mtop)).getValV()
  	#BW.SetParameter(0, mean.getValV()*norm);
  	#BW.SetParameter(1, width.getValV()*norm);
	#print h.Integral()
	#print norm.getVal() ," ---------------------------------------------------"
	print Norm.getVal() ," ---------------------------------------------------"
	pad1 = R.TPad('pad1', 'pad1', 0.0, 0.195259, 1.0, 0.990683)
        pad1.SetBottomMargin(0.089)
        pad1.SetTicky()
        pad1.SetTickx()
	pad1.Draw()
	pad1.cd()

        frame.Draw()
	can_Breitwigner.Update()
	#convert fit pdf into histogram
	fitModel_hist= BW.createHistogram("fitModel",mtop, R.RooFit.Binning(52))
	fitModel_hist.Sumw2()
	fitModel_hist.SetNameTitle("FitModel_Hist","")
	fitModel_hist.Scale(Norm.getVal())
	fitModel_hist.SetMarkerStyle(20)
	fitModel_hist.SetMarkerColor(R.kRed)
	for i in range (0,fitModel_hist.GetNbinsX()):
		fitModel_hist.SetBinError(i+1,1/R.TMath.Sqrt(fitModel_hist.GetBinContent(i+1)))
		
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
	ratio = fitModel_hist.Clone()
	ratio.Divide(h1)	
	ratio.SetMarkerColor(R.kBlack)
	ratio.Draw()
	
	ratio.SetStats(R.kFALSE)
	ratio.GetYaxis().SetTitle("Fit/MC")
        ratio.GetXaxis().SetTitle("m_{t}")
        ratio.GetYaxis().CenterTitle(1)
        ratio.GetYaxis().SetTitleOffset(0.3)
        ratio.GetYaxis().SetTitleSize(0.15)
        ratio.GetXaxis().SetTitleSize(0.15)
        ratio.GetYaxis().SetLabelSize(0.1)
        ratio.GetXaxis().SetLabelSize(0.15)
	ratio.SetMaximum(1.545665)
        ratio.SetMinimum(0.164544)
        c = ratio.GetYaxis()
        c.SetNdivisions(10)
        c.SetTickSize(0.01)
        d = ratio.GetXaxis()
        d.SetNdivisions(10)
        d.SetTickSize(0.03)
	
	can_Breitwigner.Update()
        can_Breitwigner.Draw()
	raw_input()
        #return res; 
def BreitwignerWOfit(h):
	#define canvas

        can_BreitwignerWOfit = R.TCanvas("can_bw_WOfit","can_bw_WOfit") 
        #define roo var to fit
        mtop = R.RooRealVar("mtop","m_{t}",166.0,179.0)
        mtop.setRange("signal",166.0,179.0)
        #define roodata hist
        data = R.RooDataHist("data","data",R.RooArgList(mtop),h)
        #define fame to plot
        frame = mtop.frame(R.RooFit.Bins(52),R.RooFit.Title("mtop"))
        #plot data on fame
        data.plotOn(frame,R.RooFit.MarkerSize(0.9) )
        #deine papameter to  dfinet the breit wigner shape
        mean = R.RooRealVar("mean","mean",172.5)
        width = R.RooRealVar("width","width",1.455)
        #deine pdf
        BW = R.RooBreitWigner ("BW","BW",mtop,mean,width)
        #define Normalization
        Norm = R.RooRealVar("Norm","Norm",h.Integral())
        #define model
        model = R.RooAddPdf("model","Total Model",R.RooArgList(BW),R.RooArgList(Norm))

        #draw fit on frame
        #BW.plotOn(frame, R.RooFit.Name("BW"))
        model.paramOn(frame,R.RooFit.Layout(0.55, 0.85, 0.85))

        #norm = BW.createIntegral(R.RooArgSet(mtop))#,R.RooFit.Range("signal"))
        #norm = h.Integral()/BW.createIntegral(R.RooArgSet(mtop)).getValV()
        #BW.SetParameter(0, mean.getValV()*norm);
        #BW.SetParameter(1, width.getValV()*norm);
        #print h.Integral()
        #print norm.getVal() ," ---------------------------------------------------"
        print Norm.getVal() ," ---------------------------------------------------"
        pad1 = R.TPad('pad1', 'pad1', 0.0, 0.195259, 1.0, 0.990683)
        pad1.SetBottomMargin(0.089)
        pad1.SetTicky()
        pad1.SetTickx()
        pad1.Draw()
        pad1.cd()	

	frame.Draw()
        can_BreitwignerWOfit.Update()
        #convert fit pdf into histogram
        fitModel_hist= BW.createHistogram("fitModel",mtop, R.RooFit.Binning(52))
        fitModel_hist.Sumw2()
        fitModel_hist.SetNameTitle("FitModel_Hist","")
        fitModel_hist.Scale(Norm.getVal())
        fitModel_hist.SetMarkerStyle(20)
        fitModel_hist.SetMarkerColor(R.kRed)
        for i in range (0,fitModel_hist.GetNbinsX()):
                fitModel_hist.SetBinError(i+1,1/R.TMath.Sqrt(fitModel_hist.GetBinContent(i+1)))

        fitModel_hist.Draw("same")

        can_BreitwignerWOfit.cd()

        pad2 = R.TPad("pad2", "pad2", 0.0, 0.0, 1.0, 0.2621035)
        pad2.SetTopMargin(0.0)
        pad2.SetBottomMargin(0.3)
        pad2.SetGridy()
        pad2.SetTicky()
        pad2.SetTickx()
        pad2.Draw()
        pad2.cd()
        ratio = fitModel_hist.Clone()
        ratio.Divide(h1)
        ratio.SetMarkerColor(R.kBlack)
        ratio.Draw()

        ratio.SetStats(R.kFALSE)
        ratio.GetYaxis().SetTitle("Fit/MC")
        ratio.GetXaxis().SetTitle("m_{t}")
        ratio.GetYaxis().CenterTitle(1)
        ratio.GetYaxis().SetTitleOffset(0.3)
        ratio.GetYaxis().SetTitleSize(0.15)
        ratio.GetXaxis().SetTitleSize(0.15)
        ratio.GetYaxis().SetLabelSize(0.1)
        ratio.GetXaxis().SetLabelSize(0.15)
        ratio.SetMaximum(1.545665)
        ratio.SetMinimum(0.164544)
        c = ratio.GetYaxis()
        c.SetNdivisions(10)
        c.SetTickSize(0.01)
        d = ratio.GetXaxis()
        d.SetNdivisions(10)
        d.SetTickSize(0.03)

        can_BreitwignerWOfit.Update()
        can_BreitwignerWOfit.Draw()

	raw_input()

if __name__ == "__main__":
	#get_hist("top_mass_reconstracted_el.root")
	input_file = "/grid_mnt/t3storage3/mikumar/Run2/SIXTEEN/minitree/Mc/Gen/Minitree_TTTo2L2Nu_widthx0p7.root"
	#"/home/mikumar/t3store3/workarea/CMSSW_9_4_9/src/PhysicsTools/NanoAODTools/crab/Rootfiles/Gen_mass_tree_tchannel_mu.root"
	h1 = R.TH1D("top_mass","top_mass",52,166.0,179.0)	
	treename = "Events"
	Var = "top_mass_gen"
	cut = "Event_wgt*L1PreFiringWeight_Nom*(mtwMass>50)"
	hist = get_hitogram_from_tree(input_file,treename,h1,Var,cut)
	Breitwignerfit(hist)
	BreitwignerWOfit(hist)
	#hist.Draw()
