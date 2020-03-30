import os, commands
import optparse
from ROOT import *
from variabile import variabile


def plot(variable, cut, syst):
     print "plotting ", variable._name, " ", cut, " ", syst
     ROOT.gROOT.SetBatch()        # don't pop up canvases
     ROOT.TH1.SetDefaultSumw2()
     f1 = TFile.Open("trees_lumi/"+lep+"/trees_"+channel+"_"+lep+".root")
     treename = "events_"+njmt
     if(cut_tag == ""):
          histoname = "h_"+njmt+"_"+variable._name
     else:
          histoname = "h_"+njmt+"_"+variable._name+"_"+cut_tag
     nbins = variable._nbins
     h1 = TH1F(histoname, variable._name+"_"+channel, nbins, variable._xmin, variable._xmax)
     h1.Sumw2()
     if(channel == "Data"):
         taglio = variable._taglio
         foutput = "Plot/"+lep+"/"+channel+"_"+lep+".root"
     else:
        if(syst==""):
            taglio = variable._taglio+"*w_nominal"
            foutput = "Plot/"+lep+"/"+channel+"_"+lep+".root"
            if(channel == "WJets_ext" and lep.startswith("electron")):
                taglio = variable._taglio+"*w_nominal*(abs(w)<10)"
        '''
        elif(syst.startswith("jer") or syst.startswith("jes")):
            taglio = variable._taglio+"*w_nominal"
            treename = "events_"+njmt+"_"+syst
            foutput = "Plot/"+lep+"/"+channel+"_"+lep+"_"+syst+".root"
            if(channel == "WJets_ext" and lep.startswith("electron")):
                taglio = variable._taglio+"*w_nominal*(abs(w)<10)"
        '''
     print treename
     f1.Get(treename).Project(histoname,variable._name,taglio)
     h1.SetBinContent(1, h1.GetBinContent(0) + h1.GetBinContent(1))
     h1.SetBinError(1, math.sqrt(pow(h1.GetBinError(0),2) + pow(h1.GetBinError(1),2)))
     h1.SetBinContent(nbins, h1.GetBinContent(nbins) + h1.GetBinContent(nbins+1))
     h1.SetBinError(nbins, math.sqrt(pow(h1.GetBinError(nbins),2) + pow(h1.GetBinError(nbins+1),2)))
     for i in range(0, nbins+1):
          content = h1.GetBinContent(i)
          if(content<0.):
               h1.SetBinContent(i, 0.)
     fout = TFile.Open(foutput, "UPDATE")
     fout.cd()
     h1.Write()
     fout.Close()
     f1.Close()


def makestack(njmt_, variabile_, syst_, samples_, cut_tag_, lep_):
    histo = []
    tmp = ROOT.TH1F()
    h = ROOT.TH1F()
    h_err = ROOT.TH1F()
    h_bkg_err = ROOT.TH1F()
    err_up = []
    err_down =  []

    print "Variabile:", variabile_._name
    ROOT.gROOT.Reset()
    ROOT.gROOT.SetStyle('Plain')
    ROOT.gStyle.SetPalette(1)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gROOT.SetBatch()        # don't pop up canvases
    ROOT.TH1.SetDefaultSumw2()
    ROOT.TGaxis.SetMaxDigits(3)
    setTDRStyle()

    if cut_tag_=="":
        histoname = "h_"+njmt_+"_"+variabile_._name
        stackname = "Stack_"+njmt_+"_"+variabile_._name
        canvasname = "Stack_"+njmt_+"_"+variabile_._name+"_"+lep_
    else:
        histoname = "h_"+njmt_+"_"+variabile_._name+"_"+cut_tag_
        stackname = "Stack_"+njmt_+"_"+variabile_._name+"_"+cut_tag_
        canvasname = "Stack_"+njmt_+"_"+variabile_._name+"_"+cut_tag_+"_"+lep_
    stack = ROOT.THStack(stackname, variabile_._name)
    leg_stack = ROOT.TLegend(0.45,0.56,0.94,0.88)
    signal=False
    infile =[]
    #Adding data file
    fdata = TFile.Open("Plot/"+str(lep_).strip('[]')+"/Data_"+str(lep_).strip('[]')+".root")
    hdata = (TH1F)(fdata.Get(histoname))
    hdata.SetLineColor(kBlack)
    hdata.SetMarkerStyle(20)
    hdata.SetMarkerSize(0.9)

    leg_stack.AddEntry(hdata, "Data", "lp")
    hsig = hdata.Clone("")
    hsig.Reset("ICES")
    hratio = hdata.Clone("")
    hratio.Reset("ICES")
    for s in samples_:
        if s.leglabel=="t, t-ch_sd": signal=True
        if(syst_==""):
            outfile="Stack_"+str(lep_).strip('[]')+".root"
            infile.append(TFile.Open("Plot/"+str(lep_).strip('[]')+"/"+s.label+"_"+str(lep_).strip('[]')+".root"))
        else:
            outfile="Stack_"+syst_+"_"+str(lep_).strip('[]')+".root"
            infile.append(TFile.Open("Plot/"+str(lep_).strip('[]')+"/"+s.label+"_"+str(lep_).strip('[]')+"_"+syst_+".root"))
    i=0
    for s in samples_:
        infile[i].cd()
        print "opening file: ", infile[i].GetName()
        tmp = (TH1F)(infile[i].Get(histoname))
        tmp.SetOption("HIST SAME")
        tmp.SetLineColor(kBlack)
        tmp.SetTitle("")
        tmp.SetName(s.leglabel)
        tmp.SetFillColor(s.color)
        if(signal):
             if (tmp.GetName())=="t, t-ch_sd" or (tmp.GetName())=="t, t-ch_p_sd":
                  print "parz", tmp.Integral()
                  hsig.Add(tmp.Clone(""))

                  hsig.SetName("t_sd")
                  hsig.SetTitle("")
             else:
                  histo.append(tmp.Clone(""))
                  stack.Add(tmp.Clone(""))
                  hratio.Add(tmp)
        else:
             histo.append(tmp.Clone(""))
             stack.Add(tmp.Clone(""))
             hratio.Add(tmp)
        i+=1
        #err_up,err_down = systerr(err_up, err_down, tmp, histoname, s, lep_)

        tmp.Reset("ICES")
    print "segnale somma", hsig.Integral()
    if(signal):
         leg_stack.AddEntry(hsig, "ST_{q,b}+ST_{b,q}(#times 1000)", "l")
    for hist in reversed(histo):
        if (hist.GetName())!="t_sd":
            leg_stack.AddEntry(hist, hist.GetName(), "f")
    #style options                                                                                                                                                                                                                   
    leg_stack.SetNColumns(2)
    leg_stack.SetFillColor(0)
    leg_stack.SetFillStyle(0)
    leg_stack.SetTextFont(42)
    leg_stack.SetTextSize(20)
    leg_stack.SetBorderSize(0)
    leg_stack.SetTextSize(0.055)
    c1 = ROOT.TCanvas(canvasname,"c1",50,50,700,600)
    c1.SetFillColor(0)
    c1.SetBorderMode(0)
    c1.SetFrameFillStyle(0)
    c1.SetFrameBorderMode(0)
    c1.SetLeftMargin( 0.12 )
    c1.SetRightMargin( 0.9 )
    c1.SetTopMargin( 1 )
    c1.SetBottomMargin(-1)
    c1.SetTickx(1)
    c1.SetTicky(1)
    c1.cd()

    pad1= ROOT.TPad("pad1", "pad1", 0, 0.31 , 1, 1)
    pad1.SetTopMargin(0.1)
    pad1.SetBottomMargin(0.02)
    pad1.SetLeftMargin(0.12)
    pad1.SetRightMargin(0.05)
    pad1.SetBorderMode(0)
    pad1.SetTickx(1)
    pad1.SetTicky(1)
    pad1.Draw()
    pad1.cd()

    maximum = max(stack.GetMaximum(),hdata.GetMaximum())
    logscale = False # True #                                                                                                                                                                                                        
    if(logscale):
         pad1.SetLogy()
         stack.SetMaximum(maximum*10000)
    else:
         stack.SetMaximum(maximum*1.6)

    stack.Draw("HIST")
    step = float(variabile_._xmax - variabile_._xmin)/float(variabile_._nbins)
    print str(step)
    if "GeV" in variabile_._title:
         if step.is_integer():
              ytitle = "Events/%.0f   GeV" %step
         else:
              ytitle = "Events/%.2f GeV" %step
    else:
         ytitle = "Events/%.2f units" %step
    stack.GetYaxis().SetTitle(ytitle)
    stack.GetYaxis().SetTitleFont(42)
    stack.GetXaxis().SetLabelOffset(1.8)
    stack.GetYaxis().SetTitleOffset(0.85)
    stack.GetXaxis().SetLabelSize(0.15)
    stack.GetYaxis().SetLabelSize(0.07)
    stack.GetYaxis().SetTitleSize(0.07)
    stack.SetTitle("")
    if(signal):
        hsig.SetLineStyle(9)
        hsig.SetLineColor(kBlue)
        hsig.SetLineWidth(3)

        hsig.SetMarkerSize(0.)
        hsig.SetMarkerColor(kBlue)
        hsig.Scale(1000)
        hsig.Draw("same L")
    h_err = stack.GetStack().Last().Clone("h_err")
    h_err.SetLineWidth(100)
    h_err.SetFillStyle(3154)
    h_err.SetMarkerSize(0)
    h_err.SetFillColor(ROOT.kGray+2)
    h_err.Draw("e2same0")
    leg_stack.AddEntry(h_err, "Stat. Unc.", "f")
    hdata.Draw("eSAMEpx0")
    leg_stack.Draw("same")

    CMS_lumi.writeExtraText = 1
    CMS_lumi.extraText = ""
    if(njmt_=="2j1t"):
        nJmT="2j1t"
    elif(njmt_=="3j1t"):
        nJmT="3j1t"
    elif(njmt_=="3j2t"):
        nJmT="3j2t"
    if str(lep_).strip('[]') == "muon":
         lep_tag = "#mu+"
    elif str(lep_).strip('[]') == "electron":
         lep_tag = "e+"

    lumi_sqrtS = "35.9 fb^{-1}  (13 TeV)"

    iPeriod = 0
    iPos = 11
    CMS_lumi(pad1, lumi_sqrtS, iPos, lep_tag+str(nJmT))
    hratio=stack.GetStack().Last()

    c1.cd()
    pad2= ROOT.TPad("pad2", "pad2", 0, 0.01 , 1, 0.30)
    pad2.SetTopMargin(0.05)
    pad2.SetBottomMargin(0.45)
    pad2.SetLeftMargin(0.12)
    pad2.SetRightMargin(0.05)
    ROOT.gStyle.SetHatchesSpacing(2)
    ROOT.gStyle.SetHatchesLineWidth(2)
    c1.cd()
    pad2.Draw()
    pad2.cd()
    ratio = hdata.Clone("ratio")
    ratio.SetLineColor(kBlack)
    ratio.SetMaximum(2)
    ratio.SetMinimum(0)
    ratio.Sumw2()
    ratio.SetStats(0)

    ratio.Divide(hratio)
    ratio.SetMarkerStyle(20)
    ratio.SetMarkerSize(0.9)
    ratio.Draw("epx0e0")
    ratio.SetTitle("")

    h_bkg_err = hratio.Clone("h_err")
    h_bkg_err.Reset()
    h_bkg_err.Sumw2()
    for i in range(1,hratio.GetNbinsX()+1):
        h_bkg_err.SetBinContent(i,1)
        if(hratio.GetBinContent(i)):
            h_bkg_err.SetBinError(i, (hratio.GetBinError(i)/hratio.GetBinContent(i)))
        else:
            h_bkg_err.SetBinError(i, 10^(-99))
    h_bkg_err.SetLineWidth(100)

    h_bkg_err.SetMarkerSize(0)
    h_bkg_err.SetFillColor(ROOT.kGray+1)
    h_bkg_err.Draw("e20same")

    f1 = ROOT.TLine(variabile_._xmin, 1., variabile_._xmax,1.)
    f1.SetLineColor(ROOT.kBlack)
    f1.SetLineStyle(ROOT.kDashed)
    f1.Draw("same")

    ratio.GetYaxis().SetTitle("Data / MC")
    ratio.GetYaxis().SetNdivisions(503)
    ratio.GetXaxis().SetLabelFont(42)
    ratio.GetYaxis().SetLabelFont(42)
    ratio.GetXaxis().SetTitleFont(42)
    ratio.GetYaxis().SetTitleFont(42)
    ratio.GetXaxis().SetTitleOffset(1.1)
    ratio.GetYaxis().SetTitleOffset(0.35)
    ratio.GetXaxis().SetLabelSize(0.15)
    ratio.GetYaxis().SetLabelSize(0.15)
    ratio.GetXaxis().SetTitleSize(0.16)
    ratio.GetYaxis().SetTitleSize(0.16)
    ratio.GetYaxis().SetRangeUser(0.8,1.2)
    ratio.GetXaxis().SetTitle(variabile_._title)
    ratio.GetXaxis().SetLabelOffset(0.04)
    ratio.GetYaxis().SetLabelOffset(0.02)
    ratio.Draw("epx0e0same")

    c1.cd()
    ROOT.TGaxis.SetMaxDigits(3)
    c1.RedrawAxis()
    pad2.RedrawAxis()
    c1.Update()
    c1.Print("Stack/"+canvasname+".pdf")
    c1.Print("Stack/"+canvasname+".png")
    fdata.Close()
    i=0
    for s in samples_:
        infile[i].Close()
        i+=1
    del histo
    del tmp
    del h
    del hsig
    del hratio
    del c1
    del stack
    del pad1
    del pad2




lumi_mu = {'2016': 36.47, '2017':  41.54,'2018':  59.96}
lumi_ele = {'2016': 36.47, '2017':  36.75,'2018':  59.96}
peso_lumi = (lumi*sigma*1000/n_uncut)



