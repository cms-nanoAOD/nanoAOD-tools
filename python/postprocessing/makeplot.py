import os, commands
import sys
import optparse
import ROOT
import math
from variabile import variabile
from CMS_lumi import CMS_lumi
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from array import array

usage = 'python makeplot.py'
parser = optparse.OptionParser(usage)
parser.add_option('--merpart', dest='merpart', default = False, action='store_true', help='Default parts are not merged')
parser.add_option('--mertree', dest='mertree', default = False, action='store_true', help='Default make no file is merged')
parser.add_option('--lumi', dest='lumi', default = False, action='store_true', help='Default do not write the normalization weights')
parser.add_option('--sel', dest='sel', default = False, action='store_true', help='Default do not apply any selection')
parser.add_option('-p', '--plot', dest='plot', default = False, action='store_true', help='Default make no plots')
parser.add_option('-s', '--stack', dest='stack', default = False, action='store_true', help='Default make no stacks')
parser.add_option('-N', '--notstacked', dest='tostack', default = True, action='store_false', help='Default make plots stacked')
parser.add_option('-L', '--lep', dest='lep', type='string', default = 'muon', help='Default make muon analysis')
parser.add_option('-S', '--syst', dest='syst', type='string', default = 'all', help='Default all systematics added')
parser.add_option('-C', '--cut', dest='cut', type='string', default = 'lepton_eta>-10.', help='Default no cut')
parser.add_option('-y', '--year', dest='year', type='string', default = 'all', help='Default 2016, 2017 and 2018 are included')
parser.add_option('-f', '--folder', dest='folder', type='string', default = 'v6', help='Default folder is v0')
#parser.add_option('-T', '--topol', dest='topol', type='string', default = 'all', help='Default all njmt')
parser.add_option('-d', '--dat', dest='dat', type='string', default = 'all', help="")
(opt, args) = parser.parse_args()

folder = opt.folder

#filerepo = '/eos/user/a/apiccine/Wprime/nosynch/v13/'
filerepo = '/eos/user/'+str(os.environ.get('USER')[0])+'/'+str(os.environ.get('USER'))+'/Wprime/nosynch/' + folder + '/'
plotrepo = '/eos/user/'+str(os.environ.get('USER')[0])+'/'+str(os.environ.get('USER'))+'/Wprime/nosynch/' + folder + '/'#_topjet/'#/only_Wpjetbtag_ev1btag/'

ROOT.gROOT.SetBatch() # don't pop up canvases
if not os.path.exists(plotrepo + 'plot/muon'):
     os.makedirs(plotrepo + 'plot/muon')
if not os.path.exists(plotrepo + 'plot/electron'):
     os.makedirs(plotrepo + 'plot/electron')
if not os.path.exists(plotrepo + 'stack'):
     os.makedirs(plotrepo + 'stack')

def mergepart(dataset):
     samples = []
     if hasattr(dataset, 'components'): # How to check whether this exists or not
          samples = [sample for sample in dataset.components]# Method exists and was used.
     else:
          samples.append(dataset)
     for sample in samples:
          add = "hadd -f " + filerepo + sample.label + "/"  + sample.label + "_merged.root " + filerepo + sample.label + "/"  + sample.label + "_part*.root" 
          print add
          os.system(str(add))
          check = ROOT.TFile.Open(filerepo + sample.label + "/"  + sample.label + "_merged.root ")
          print "Number of entries of the file %s are %s" %(filerepo + sample.label + "/"  + sample.label + "_merged.root", (check.Get("events_nominal")).GetEntries())
          #print "Number of entries of the file %s are %s" %(filerepo + sample.label + "/"  + sample.label + "_merged.root", (check.Get("events_all")).GetEntries())

def mergetree(sample):
     if not os.path.exists(filerepo + sample.label):
          os.makedirs(filerepo + sample.label)
     if hasattr(sample, 'components'): # How to check whether this exists or not
          add = "hadd -f " + filerepo + sample.label + "/"  + sample.label + ".root" 
          for comp in sample.components:
               add += " " + filerepo + comp.label + "/"  + comp.label + ".root" 
          print add
          os.system(str(add))

def lumi_writer(dataset, lumi):
     samples = []
     if hasattr(dataset, 'components'): # How to check whether this exists or not
          samples = [sample for sample in dataset.components]# Method exists and was used.
     else:
          samples.append(dataset)
     for sample in samples:
          if not ('Data' in sample.label or 'TT_dilep' in sample.label):
               infile =  ROOT.TFile.Open(filerepo + sample.label + "/"  + sample.label + "_merged.root")
               tree = infile.Get('events_nominal')
               treejesup = infile.Get('events_jesUp')
               treejesdown = infile.Get('events_jesDown')
               treejerup = infile.Get('events_jerUp')
               treejerdown = infile.Get('events_jerDown')
               tree.SetBranchStatus('w_nominal', 0)
               tree.SetBranchStatus('w_PDF', 0)
               treejesup.SetBranchStatus('w_nominal', 0)
               treejesdown.SetBranchStatus('w_nominal', 0)
               treejerup.SetBranchStatus('w_nominal', 0)
               treejerdown.SetBranchStatus('w_nominal', 0)
               outfile = ROOT.TFile.Open(filerepo + sample.label + "/"  + sample.label + ".root","RECREATE")
               tree_new = tree.CloneTree(0)
               treejesup_new = treejesup.CloneTree(0)
               treejesdown_new = treejesdown.CloneTree(0)
               treejerup_new = treejerup.CloneTree(0)
               treejerdown_new = treejerdown.CloneTree(0)
               tree.SetBranchStatus('w_nominal', 1)
               tree.SetBranchStatus('w_PDF', 1)
               treejesup.SetBranchStatus('w_nominal', 1)
               treejesdown.SetBranchStatus('w_nominal', 1)
               treejerup.SetBranchStatus('w_nominal', 1)
               treejerdown.SetBranchStatus('w_nominal', 1)
               print("Getting the histos from %s" %(infile))
               h_genw_tmp = ROOT.TH1F(infile.Get("h_genweight"))
               h_pdfw_tmp = ROOT.TH1F(infile.Get("h_PDFweight"))
               nbins = h_pdfw_tmp.GetXaxis().GetNbins()
               print("h_genweight first bin content is %f and h_PDFweight has %f bins" %(h_genw_tmp.GetBinContent(1), nbins))
               w_nom = array('f', [0.]) 
               w_nomjesup = array('f', [0.]) 
               w_nomjesdown = array('f', [0.]) 
               w_nomjerup = array('f', [0.]) 
               w_nomjerdown = array('f', [0.]) 
               w_PDF = array('f', [0.]*nbins)
               print(nbins)
               print(len(w_PDF))
               tree_new.Branch('w_nominal', w_nom, 'w_nominal/F')
               tree_new.Branch('w_PDF', w_PDF, 'w_PDF/F')
               treejesup_new.Branch('w_nominal', w_nomjesup, 'w_nominal/F')
               treejesdown_new.Branch('w_nominal', w_nomjesdown, 'w_nominal/F')
               treejerup_new.Branch('w_nominal', w_nomjerup, 'w_nominal/F')
               treejerdown_new.Branch('w_nominal', w_nomjerdown, 'w_nominal/F')
               for event in xrange(0, tree.GetEntries()):
                    tree.GetEntry(event)
                    if event%10000==1:
                         #print("Processing event %s     complete %s percent" %(event, 100*event/tree.GetEntries()))
                         sys.stdout.write("\rProcessing event {}     complete {} percent".format(event, 100*event/tree.GetEntries()))
                    w_nom[0] = tree.w_nominal * sample.sigma * lumi * 1000./float(h_genw_tmp.GetBinContent(1))
                    for i in xrange(1, nbins):
                         w_PDF[i] = h_pdfw_tmp.GetBinContent(i+1)/h_genw_tmp.GetBinContent(2) 
                    tree_new.Fill()
               outfile.cd()
               tree_new.Write()
               infile.cd()
               for event in xrange(0, treejesup.GetEntries()):
                    treejesup.GetEntry(event)
                    if event%10000==1:
                         #print("Processing event %s     complete %s percent" %(event, 100*event/tree.GetEntries()))
                         sys.stdout.write("\rProcessing event {}     complete {} percent".format(event, 100*event/treejesup.GetEntries()))
                    w_nomjesup[0] = treejesup.w_nominal * sample.sigma * lumi * 1000./float(h_genw_tmp.GetBinContent(1))
                    treejesup_new.Fill()
               outfile.cd()
               treejesup_new.Write()
               infile.cd()
               for event in xrange(0, treejesdown.GetEntries()):
                    treejesdown.GetEntry(event)
                    if event%10000==1:
                         #print("Processing event %s     complete %s percent" %(event, 100*event/tree.GetEntries()))
                         sys.stdout.write("\rProcessing event {}     complete {} percent".format(event, 100*event/treejesdown.GetEntries()))
                    w_nomjesdown[0] = treejesdown.w_nominal * sample.sigma * lumi * 1000./float(h_genw_tmp.GetBinContent(1))
                    treejesdown_new.Fill()
               outfile.cd()
               treejesdown_new.Write()
               infile.cd()
               for event in xrange(0, treejerup.GetEntries()):
                    treejerup.GetEntry(event)
                    if event%10000==1:
                         #print("Processing event %s     complete %s percent" %(event, 100*event/tree.GetEntries()))
                         sys.stdout.write("\rProcessing event {}     complete {} percent".format(event, 100*event/treejerup.GetEntries()))
                    w_nomjerup[0] = treejerup.w_nominal * sample.sigma * lumi * 1000./float(h_genw_tmp.GetBinContent(1))
                    treejerup_new.Fill()
               outfile.cd()
               treejerup_new.Write()
               infile.cd()
               for event in xrange(0, treejerdown.GetEntries()):
                    treejerdown.GetEntry(event)
                    if event%10000==1:
                         #print("Processing event %s     complete %s percent" %(event, 100*event/tree.GetEntries()))
                         sys.stdout.write("\rProcessing event {}     complete {} percent".format(event, 100*event/treejerdown.GetEntries()))
                    w_nomjerdown[0] = treejerdown.w_nominal * sample.sigma * lumi * 1000./float(h_genw_tmp.GetBinContent(1))
                    treejerdown_new.Fill()
               outfile.cd()
               treejerdown_new.Write()
               outfile.Close()
               print('\n')
          else:
               os.popen("mv " + filerepo + sample.label + "/"  + sample.label + "_merged.root " + filerepo + sample.label + "/"  + sample.label + ".root")

def cutToTag(cut):
    newstring = cut.replace("-", "neg").replace(">=","_GE_").replace(">","_G_").replace(" ","").replace("&&","_AND_").replace("||","_OR_").replace("<=","_LE_").replace("<","_L_").replace(".","p").replace("(","").replace(")","").replace("==","_EQ_").replace("!=","_NEQ_").replace("=","_EQ_").replace("*","_AND_").replace("+","_OR_")
    return newstring

def plot(lep, reg, variable, sample, cut_tag, syst):
     print "plotting ", variable._name, " for sample ", sample.label, " with cut ", cut_tag, " ", syst,
     ROOT.TH1.SetDefaultSumw2()
     f1 = ROOT.TFile.Open(filerepo + sample.label + "/"  + sample.label + ".root")
     treename = "events_nominal"
     if(cut_tag == ""):
          if variable._name=='WprAK8_tau2/WprAK8_tau1':
               histoname = "h_" + reg + "_WprAK8_tau21"
          elif variable._name== 'WprAK8_tau3/WprAK8_tau2':
               histoname =  "h_" + reg + "_WprAK8_tau32"
          else:
               histoname = "h_" + reg + "_" + variable._name
     else:
          if variable._name=='WprAK8_tau2/WprAK8_tau1':
               histoname = "h_" + reg + "_WprAK8_tau21_" + cut_tag
          elif variable._name== 'WprAK8_tau3/WprAK8_tau2':
               histoname =  "h_" + reg + "_WprAK8_tau32_" + cut_tag
          else:
               histoname = "h_" + reg + "_" + variable._name + "_" + cut_tag
     nbins = 0
     h1 = ROOT.TH1F()
     if variable._nbins == None:
          nbins = len(variable._xarray)-1
          h1 = ROOT.TH1F(histoname, variable._name + "_" + reg, nbins, variable._xarray)
     else:
          nbins = variable._nbins
          h1 = ROOT.TH1F(histoname, variable._name + "_" + reg, variable._nbins, variable._xmin, variable._xmax)
     h1.Sumw2()
     if 'muon' in lep: 
          cut = variable._taglio + '*isMu'
          #if not 'Data' in sample.label:
          #cut += '*passed_mu*(1-passed_ht)'
          #cut += '*passed_ht*(1-passed_mu)*(1-passed_ele)'
          '''
          if 'DataMu' in sample.label:
               cut += '*passed_ht*(passed_mu)'
          elif 'DataHT' in sample.label:
               cut += '*passed_ht*(1-passed_mu)'
          else:
               cut += '*passed_ht'
          '''
     elif 'electron' in lep:
          cut  = variable._taglio + '*isEle'
          if 'MC' in variable._name:
               cut = cut + "*(" + str(variable._name) + "!=-100.)"
          #if not 'Data' in sample.label: 
          #cut += '*passed_ht*(1-passed_ele)'
          #cut += '*passed_ele'
     #if 'MC' in variable._name:
     #if not 'Data' in sample.label:
          #cut = cut + "*(MC_Wprime_m!=-100.)"
     print str(cut)
     foutput = plotrepo + "plot/" + lep + "/" + sample.label + "_" + lep+".root"
     if not 'Data' in sample.label: 
          if(syst.startswith("jer") or syst.startswith("jes")):
               treename = "events_"+syst
               foutput = plotrepo + "plot/" + lep + "/" + sample.label + "_" + lep + "_" + syst + ".root"
          elif(syst == ""):
               foutput = plotrepo + "plot/" + lep + "/" + sample.label + "_" + lep + ".root"
          else:
               foutput = plotrepo + "plot/" + lep + "/" + sample.label + "_" + lep + "_" + syst + ".root"

     #print treename
     f1.Get(treename).Project(histoname,variable._name,cut)
     #if not 'Data' in sample.label:
     #     h1.Scale((7.5)/35.89)
     h1.SetBinContent(1, h1.GetBinContent(0) + h1.GetBinContent(1))
     h1.SetBinError(1, math.sqrt(pow(h1.GetBinError(0),2) + pow(h1.GetBinError(1),2)))
     h1.SetBinContent(nbins, h1.GetBinContent(nbins) + h1.GetBinContent(nbins+1))
     h1.SetBinError(nbins, math.sqrt(pow(h1.GetBinError(nbins),2) + pow(h1.GetBinError(nbins+1),2)))
     for i in range(0, nbins+1):
          content = h1.GetBinContent(i)
          if(content<0.):
               h1.SetBinContent(i, 0.)
     fout = ROOT.TFile.Open(foutput, "UPDATE")
     fout.cd()
     h1.Write()
     fout.Close()
     f1.Close()

def makestack(lep_, reg_, variabile_, samples_, cut_tag_, syst_, lumi):
     os.system('set LD_PRELOAD=libtcmalloc.so')
     if variabile_._name=='WprAK8_tau2/WprAK8_tau1':
          variabile_._name = 'WprAK8_tau21' 
     elif variabile_._name== 'WprAK8_tau3/WprAK8_tau2':
          variabile_._name = 'WprAK8_tau32'
     infile = {}
     histo = []
     tmp = ROOT.TH1F()
     h = ROOT.TH1F()
     hdata = ROOT.TH1F()
     nbins = 0
     xmin = 0.
     xmax = 100.
     if variabile_._nbins == None:
          nbins = len(variabile_._xarray)-1
          hdata = ROOT.TH1F('h','h', nbins, variabile_._xarray)
          xmin = variabile_._xarray[0]
          xmax = variabile_._xarray[-1]
     else:
          nbins = variabile_._nbins
          hdata = ROOT.TH1F('h','h', variabile_._nbins, variabile_._xmin, variabile_._xmax)
          xmin = variabile_._xmin
          xmax = variabile_._xmax
     h_sig = []
     h_err = ROOT.TH1F()
     h_bkg_err = ROOT.TH1F()
     blind = False
     print "Variabile:", variabile_._name
     ROOT.gROOT.SetStyle('Plain')
     ROOT.gStyle.SetPalette(1)
     ROOT.gStyle.SetOptStat(0)
     ROOT.TH1.SetDefaultSumw2()
     if(cut_tag_ == ""):
          histoname = "h_" + reg_ + "_" + variabile_._name
          stackname = "stack_" + reg_ + "_" + variabile_._name
          canvasname = "stack_" + reg_ + "_" + variabile_._name + "_" + lep_ + "_" + str(samples_[0].year)
     else:
          histoname = "h_"+reg_+"_"+variabile_._name+"_"+cut_tag_
          stackname = "stack_"+reg_+"_"+variabile_._name+"_"+cut_tag_
          canvasname = "stack_"+reg_+"_"+variabile_._name+"_"+cut_tag_+"_"+lep_ + "_" + str(samples_[0].year)
     if("selection_AND_best_Wpjet_isbtag_AND_best_topjet_isbtag" in cut_tag_ ) or ("selection_AND_best_topjet_isbtag_AND_best_Wpjet_isbtag" in cut_tag_ ) or  ("selection_AND_best_topjet_isbtag_EQ_0_AND_best_Wpjet_isbtag" in cut_tag_ ):
          blind = True
     blind = False
     stack = ROOT.THStack(stackname, variabile_._name)
     leg_stack = ROOT.TLegend(0.33,0.62,0.91,0.87)
     signal = False

     print samples_
     for s in samples_:
          if('WP' in s.label):
               signal = True
          if(syst_ == ""):
               outfile = plotrepo + "stack_" + str(lep_).strip('[]') + ".root"
               infile[s.label] = ROOT.TFile.Open(plotrepo + "plot/" + lep + "/" + s.label + "_" + lep + ".root")
          else:
               outfile = plotrepo + "stack_"+syst_+"_"+str(lep_).strip('[]')+".root"
               infile[s.label] = ROOT.TFile.Open(plotrepo + "plot/" + lep + "/" + s.label + "_" + lep + "_" + syst_ + ".root")
     i = 0

     for s in samples_:
          infile[s.label].cd()
          print "opening file: ", infile[s.label].GetName()
          if('Data' in s.label):
               if ("GenPart" in variabile_._name) or ("MC_" in variabile_._name):
                    continue
          tmp = (ROOT.TH1F)(infile[s.label].Get(histoname))
          tmp.SetLineColor(ROOT.kBlack)
          tmp.SetName(s.leglabel)
          if('Data' in s.label):
               if ("GenPart" in variabile_._name) or ("MC_" in variabile_._name):
                    continue
               hdata.Add(ROOT.TH1F(tmp.Clone("")))
               hdata.SetMarkerStyle(20)
               hdata.SetMarkerSize(0.9)
               if(i == 0 and not blind): # trick to add Data flag to legend only once
                    leg_stack.AddEntry(hdata, "Data", "ep")
               i += 1
          elif('WP' in s.label):
               #tmp.SetLineStyle(9)
               if opt.tostack:
                    tmp.SetLineColor(s.color)
               else:
                    tmp.SetLineColor(s.color)
               #tmp.SetLineWidth(3)
               tmp.SetMarkerSize(0.)
               tmp.SetMarkerColor(s.color)
               h_sig.append(ROOT.TH1F(tmp.Clone("")))
          else:
               tmp.SetOption("HIST SAME")
               tmp.SetTitle("")
               if opt.tostack:
                    tmp.SetFillColor(s.color)
               else:
                    tmp.SetLineColor(s.color)
               histo.append(tmp.Clone(""))
               stack.Add(tmp.Clone(""))
          tmp.Reset("ICES")
     for hist in reversed(histo):
          if not ('Data' in hist.GetName()):
               leg_stack.AddEntry(hist, hist.GetName(), "f")
     #style options
     print "Is it blind? " + str(blind)
     leg_stack.SetNColumns(2)
     leg_stack.SetFillColor(0)
     leg_stack.SetFillStyle(0)
     leg_stack.SetTextFont(42)
     leg_stack.SetBorderSize(0)
     leg_stack.SetTextSize(0.05)
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
     if not blind:
          maximum = max(stack.GetMaximum(),hdata.GetMaximum())
     else:
          maximum = stack.GetMaximum()
     logscale = True # False #
     if(logscale):
          pad1.SetLogy()
          stack.SetMaximum(maximum*1000)
     else:
          stack.SetMaximum(maximum*1.6)
     stack.SetMinimum(0.01)
     if opt.tostack:
          stack.Draw("HIST")
     else:
          stack.Draw("HIST NOSTACK")
     if variabile_._nbins == None:
          ytitle = "Events / bin width"
     else:
          step = float(variabile_._xmax - variabile_._xmin)/float(variabile_._nbins)
          print str(step)
          if "GeV" in variabile_._title:
               if step.is_integer():
                    ytitle = "Events / %.0f GeV" %step
               else:
                    ytitle = "Events / %.2f GeV" %step
          else:
               if step.is_integer():
                    ytitle = "Events / %.0f units" %step
               else:
                    ytitle = "Events / %.2f units" %step
     stack.GetYaxis().SetTitle(ytitle)
     stack.GetYaxis().SetTitleFont(42)
     stack.GetXaxis().SetLabelOffset(1.8)
     stack.GetYaxis().SetTitleOffset(0.85)
     stack.GetXaxis().SetLabelSize(0.15)
     stack.GetYaxis().SetLabelSize(0.07)
     stack.GetYaxis().SetTitleSize(0.07)
     stack.SetTitle("")
     if(signal):
          for hsig in h_sig:
               #hsig.Scale(1000)
               hsig.Draw("same")
               leg_stack.AddEntry(hsig, hsig.GetName(), "l")
     h_err = stack.GetStack().Last().Clone("h_err")
     h_err.SetLineWidth(100)
     h_err.SetFillStyle(3154)
     h_err.SetMarkerSize(0)
     h_err.SetFillColor(ROOT.kGray+2)
     h_err.Draw("e2same0")
     leg_stack.AddEntry(h_err, "Stat. Unc.", "f")
     if not blind: 
          print(hdata.Integral())
          hdata.Draw("eSAMEpx0")
     else:
          hdata = stack.GetStack().Last().Clone("h_data")
     leg_stack.Draw("same")

     CMS_lumi.writeExtraText = 1
     CMS_lumi.extraText = ""
     if str(lep_).strip('[]') == "muon":
          lep_tag = "#mu+"
     elif str(lep_).strip('[]') == "electron":
          lep_tag = "e+"
          
     lumi_sqrtS = "%s fb^{-1}  (13 TeV)"%(lumi)
     
     iPeriod = 0
     iPos = 11
     CMS_lumi(pad1, lumi_sqrtS, iPos, lep_tag+str(reg_))
     hratio = stack.GetStack().Last()
     
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
     ratio.SetLineColor(ROOT.kBlack)
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
     
     f1 = ROOT.TLine(xmin, 1., xmax,1.)
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
     ratio.GetYaxis().SetRangeUser(0.,2.0)
     ratio.GetXaxis().SetTitle(variabile_._title)
     ratio.GetXaxis().SetLabelOffset(0.04)
     ratio.GetYaxis().SetLabelOffset(0.02)
     ratio.Draw("epx0e0same")

     c1.cd()
     #ROOT.TGaxis.SetMaxDigits(3)
     c1.RedrawAxis()
     pad2.RedrawAxis()
     c1.Update()
     c1.Print(plotrepo + "stack/"+canvasname+".png")
     c1.Print(plotrepo + "stack/"+canvasname+".pdf")
     del histo
     tmp.Delete()
     h.Delete()
     del tmp
     del h
     del h_sig
     h_err.Delete()
     del h_err
     h_bkg_err.Delete()
     del h_bkg_err
     hratio.Delete()
     del hratio
     stack.Delete()
     del stack
     pad1.Delete()
     del pad1
     pad2.Delete()
     del pad2
     c1.Delete()
     del c1
     for s in samples_:
          infile[s.label].Close()
          infile[s.label].Delete()
     os.system('set LD_PRELOAD=libtcmalloc.so')

dataset_dict = {'2016':[],'2017':[],'2018':[]}
if(opt.dat!= 'all'):
     if not(opt.dat in sample_dict.keys()):
          print sample_dict.keys()
     dataset_names = map(str, opt.dat.strip('[]').split(','))
     #print dataset_names.keys()
     samples = []
     [samples.append(sample_dict[dataset_name]) for dataset_name in dataset_names]
     [dataset_dict[str(sample.year)].append(sample) for sample in samples]
else:
     dataset_dict = {
          '2016':[DataMu_2016, DataEle_2016, DataHT_2016, ST_2016, QCD_2016, TT_Mtt_2016, WJets_2016, WP_M2000W20_RH_2016, WP_M3000W30_RH_2016, WP_M4000W40_RH_2016, WP_M5000W50_RH_2016, WP_M6000W60_RH_2016],
          #'2016':[DataHTG_2016, DataMuG_2016, ST_2016, QCD_2016, TT_Mtt_2016, WJets_2016, WP_M2000W20_RH_2016, WP_M3000W30_RH_2016, WP_M4000W40_RH_2016, WP_M4000W400_RH_2016],
          #'2017':[DataMu_2017, DataEle_2017, DataHT_2017, ST_2017, QCD_2017, TT_Mtt_2017, WJets_2017, WP_M2000W20_RH_2017, WP_M3000W30_RH_2017, WP_M4000W40_RH_2017, WP_M4000W400_RH_2017],
          '2017':[DataMu_2017, DataEle_2017, DataPh_2017, DataHT_2017, ST_2017, QCD_2017, TT_Mtt_2017, WJets_2017, WP_M2000W20_RH_2017, WP_M3000W30_RH_2017, WP_M4000W40_RH_2017, WP_M5000W50_RH_2017, WP_M6000W60_RH_2017],
          '2018':[DataMu_2018, DataEle_2018, DataHT_2018, ST_2018, QCD_2018, TT_Mtt_2018, WJets_2018, WP_M2000W20_RH_2018, WP_M3000W30_RH_2018, WP_M4000W40_RH_2018, WP_M5000W50_RH_2018, WP_M6000W60_RH_2018],
     }
#print(dataset_dict.keys())

years = []
if(opt.year!='all'):
     years = map(str,opt.year.strip('[]').split(','))
else:
     years = ['2016','2017','2018']
print(years)

leptons = map(str,opt.lep.split(',')) 

cut = opt.cut #default cut must be obvious, for example lepton_eta>-10.
if opt.cut == "lepton_eta>-10." and not opt.sel:
     cut_dict = {'muon':"lepton_pt>55", #&&MET_pt>80",#&&best_topjet_isbtag==0&&best_Wpjet_isbtag==1&&nbjet_pt100==1", 
                 'electron':"lepton_pt>50&&abs(lepton_eta)<2.2"#&&MET_pt>80"#&&best_topjet_isbtag==0&&best_Wpjet_isbtag==1&&nbjet_pt100==1",
     }
     cut_tag = ""
else:
     if opt.sel:
          cut_dict = {'muon':"MET_pt>120&&lepton_pt>55&&leadingjet_pt>300&&subleadingjet_pt>150&&" + cut, 
                      'electron':"MET_pt>120&&lepton_pt>50&&leadingjet_pt>300&&subleadingjet_pt>150&&abs(lepton_eta)<2.2&&" + cut
          }
          #cut_dict = {'muon':"MET_pt>120&&lepton_pt>180&&leadingjets_pt>350&&best_top_pt>250&&" + cut, 
          #            'electron':"MET_pt>120&&lepton_pt>180&&leadingjets_pt>350&&best_top_pt>250&&" + cut
          #}
          if opt.cut != "lepton_eta>-10.":
               cut_tag = 'selection_AND_' + cutToTag(opt.cut) 
          else:
               cut_tag = 'selection' 
     else:
          cut_dict = {'muon':cut, 'electron':cut}
          cut_tag = cutToTag(opt.cut)

lumi = {'2016': 35.9, "2017": 41.53, "2018": 59.7}

#
systematics = []
if opt.syst!="all" and opt.syst!="noSyst":
     for syst in (opt.syst).split(","):
          systematics.append(syst)
elif opt.syst!="all" and opt.syst=="noSyst":
    systematics.append("") #di default per syst="" alla variabile si applica il peso standard incluso nella macro macro_plot.C
else:
     systematics = ["", "jesUp",  "jesDown",  "jerUp",  "jerDown", "PFUp", "PFDown", "puUp", "puDown", "btagUp", "btagDown", "mistagUp", "mistagDown"]

for year in years:
     for sample in dataset_dict[year]:
          if(opt.merpart):
               mergepart(sample)
          if(opt.lumi):
               lumi_writer(sample, lumi[year])
          if(opt.mertree):
               if not('WP' in sample.label):
                    mergetree(sample)

for year in years:
     for lep in leptons:
          dataset_new = dataset_dict[year]
          #if lep == 'muon' and sample_dict['DataEle_'+str(year)] in dataset_new:
               #dataset_new.remove(sample_dict['DataEle_'+str(year)])
          #elif lep == 'electron' and sample_dict['DataMu_'+str(year)] in dataset_new:
               #dataset_new.remove(sample_dict['DataMu_'+str(year)])
          variables = []
          wzero = 'w_nominal*PFSF*puSF*lepSF*trigSF'#*btagSF'
          cut = cut_dict[lep]
          #variables.append(variabile('lepton_pt', 'lepton p_{T} [GeV]', wzero+'*('+cut+')', None, None, None,  array('f', [55., 60., 65., 80., 100., 130., 200., 300., 400., 600., 800., 1000.])))
          variables.append(variabile('lepton_pt', 'lepton p_{T} [GeV]', wzero+'*('+cut+')', 50, 0, 1200))
          '''
          #------->   plot nota
          variables.append(variabile('njet_pt100', 'no. of jets with p_{T} > 100 GeV',  wzero+'*('+cut+')', 8, 1.5, 9.5))
          variables.append(variabile('nbjet_pt100', 'no. of b jets with p_{T} > 100 GeV',  wzero+'*('+cut+')', 7, -0.5, 6.5))
          variables.append(variabile('leadingjet_pt', 'leading jet p_{T} [GeV]',  wzero+'*('+cut+')', None, None, None,  array('f', [150., 180., 230, 280., 350., 400., 480., 560., 650., 740., 840., 940., 1050., 1200., 1350., 1500., 1650., 1800., 1950., 2100., 2300.])))
          variables.append(variabile('subleadingjet_pt', 'subleading jet p_{T} [GeV]',  wzero+'*('+cut+')', None, None, None,  array('f', [100., 120., 150., 180., 230, 280., 340., 400., 480., 560., 650., 740., 840., 940., 1050., 1200., 1350., 1500., 1650., 1800.])))

          #variables.append(variabile('MET_pt', "Missing transverse momentum [GeV]",wzero+'*('+cut+')', None, None, None,  array('f', [0., 50., 100., 120., 150., 180., 230, 280., 340., 400., 480., 560., 650., 740., 840., 940., 1050.])))

          variables.append(variabile('lepton_eta', 'lepton #eta', wzero+'*('+cut+')', 48, -2.4, 2.4))
          variables.append(variabile('lepton_phi', 'lepton #phi',  wzero+'*('+cut+')', 20, -3.14, 3.14))
          '''
          #variables.append(variabile('nPV_good', 'n good PV', wzero+'*('+cut+')', 120, 0, 120))
          #variables.append(variabile('nPV_tot', 'total n PV', wzero+'*('+cut+')', 120, 0, 120))

          #variables.append(variabile('best_Wprime_m', 'Wprime mass [GeV] (best)',  wzero+'*(best_Wprime_m>0&&'+cut+')',  74, 80, 6000))
          #variables.append(variabile('best_top_m', 'top mass [GeV] (best)',  wzero+'*(best_top_m>0&&'+cut+')',  46, 80, 1000))

          #variables.append(variabile('best_Wprime_m', 'Wprime mass [GeV] (best)',  wzero+'*(best_Wprime_m>0&&'+cut+')', None, None, None,  array('f', [100., 120., 150., 180., 230, 280., 340., 400., 480., 560., 650., 740., 840., 940., 1050., 1200., 1350., 1500., 1650., 1800., 1950., 2100., 2300., 2500., 2750., 3000., 3250., 3500., 3750., 4000., 4500., 5000., 6000.])))
          #variables.append(variabile('best_Wprime_m', 'Wprime mass [GeV] (best)',  wzero+'*(best_Wprime_m>0&&'+cut+')', None, None, None,  array('f', [1000., 1250., 1500., 1750., 2000., 2250., 2500., 2750., 3000., 3500., 4000., 5000.])))
          #variables.append(variabile('best_top_m', 'top mass [GeV] (best)',  wzero+'*(best_top_m>0&&'+cut+')', None, None, None,  array('f', [80., 100., 120., 150., 180., 230, 280., 340., 400., 480., 560., 650., 740., 840., 940., 1050.])))

          #variables.append(variabile('leadingjets_pt', 'leadings jets system p_{T} [GeV]',  wzero+'*('+cut+')', 150, 0, 3000))
          #variables.append(variabile('leadingjets_pt', 'leadings jets system p_{T} [GeV]',  wzero+'*('+cut+')', None, None, None,  array('f', [100., 120., 150., 180., 230, 280., 340., 400., 480., 560., 650., 740., 840., 940., 1050., 1200., 1350., 1500., 1650., 1800., 1950., 2100., 2300., 2500., 2750., 3000.,])))

          #variables.append(variabile('best_top_pt', 'top p_{T} [GeV] (best)',  wzero+'*(best_top_pt>0&&'+cut+')', 40, 0, 1000))

          #variables.append(variabile('topAK8_mSD', 'topAK8 soft drop mass [GeV]', wzero+'*('+cut+')', None, None, None,  array('f', [0., 30., 55., 70., 90., 110., 130., 150., 175., 200., 225., 250., 275., 300., 350., 400.])))
          '''
          variables.append(variabile('mtw', 'W boson transverse mass [GeV]',  wzero+'*('+cut+')', None, None, None,  array('f', [55., 60., 65., 80., 100., 130., 200., 300., 400., 500.])))
          variables.append(variabile('mtw', 'W boson transverse mass [GeV]',  wzero+'*('+cut+')', 100, 0, 500))
          variables.append(variabile('njet_pt100', 'no. of jets with p_{T} > 100 GeV',  wzero+'*('+cut+')', 8, 1.5, 9.5))
          variables.append(variabile('nbjet_pt100', 'no. of b jets with p_{T} > 100 GeV',  wzero+'*('+cut+')', 7, -0.5, 6.5))
          variables.append(variabile('leadingjet_pt', 'leading jet p_{T} [GeV]',  wzero+'*('+cut+')', 150, 0, 3000))
          variables.append(variabile('subleadingjet_pt', 'subleading jet p_{T} [GeV]',  wzero+'*('+cut+')', 150, 0, 3000))          

          variables.append(variabile('chi_top_m', 'top mass [GeV] (chimass)',  wzero+'*(chi_top_m>0&&'+cut+')',  None, None, None,  array('f', [80., 100., 120., 150., 180., 230, 280., 340., 400., 480., 560., 650., 740., 840., 940., 1050.])))
          variables.append(variabile('chi_Wprime_m', 'Wprime mass [GeV] (chimass)',  wzero+'*(chi_Wprime_m>0&&'+cut+')', None, None, None,  array('f', [100., 120., 150., 180., 230, 280., 340., 400., 480., 560., 650., 740., 840., 940., 1050., 1200., 1350., 1500., 1650., 1800., 1950., 2100., 2300., 2500., 2750., 3000., 3250., 3500., 3750., 4000., 4500., 5000., 6000.])))
          variables.append(variabile('closest_top_m', 'top mass [GeV] (closest)',  wzero+'*(closest_top_m>0&&'+cut+')', None, None, None,  array('f', [80., 100., 120., 150., 180., 230, 280., 340., 400., 480., 560., 650., 740., 840., 940., 1050.])))
          variables.append(variabile('closest_Wprime_m', 'Wprime mass [GeV] (closest)',  wzero+'*(closest_Wprime_m>0&&'+cut+')', None, None, None,  array('f', [100., 120., 150., 180., 230, 280., 340., 400., 480., 560., 650., 740., 840., 940., 1050., 1200., 1350., 1500., 1650., 1800., 1950., 2100., 2300., 2500., 2750., 3000., 3250., 3500., 3750., 4000., 4500., 5000., 6000.])))
          variables.append(variabile('sublead_Wprime_m', 'Wprime mass [GeV] (sublead)',  wzero+'*(sublead_Wprime_m>0&&'+cut+')', None, None, None,  array('f', [100., 120., 150., 180., 230, 280., 340., 400., 480., 560., 650., 740., 840., 940., 1050., 1200., 1350., 1500., 1650., 1800., 1950., 2100., 2300., 2500., 2750., 3000., 3250., 3500., 3750., 4000., 4500., 5000., 6000.])))
          variables.append(variabile('sublead_top_m', 'top mass [GeV] (sublead)',  wzero+'*(sublead_top_m>0&&'+cut+')', None, None, None,  array('f', [80., 100., 120., 150., 180., 230, 280., 340., 400., 480., 560., 650., 740., 840., 940., 1050.])))

          variables.append(variabile('WprAK8_tau2/WprAK8_tau1', 'WprAK8 tau21', wzero+'*('+cut+')', 80, 0, 1.))
          variables.append(variabile('WprAK8_tau3/WprAK8_tau2', 'WprAK8 tau32', wzero+'*('+cut+')', 60, 0, 1.))
          variables.append(variabile('WprAK8_tau2', 'WprAK8 tau 2', wzero+'*('+cut+')', 60, 0, .6))
          variables.append(variabile('WprAK8_tau3', 'WprAK8 tau 3', wzero+'*('+cut+')', 40, 0, .4))
          variables.append(variabile('WprAK8_ttagMD', 'WprAK8 t tag MD', wzero+'*(WprAK8_ttagMD>-1&&'+cut+')', 20, 0, 1.0))

          variables.append(variabile('deltaR_lep_closestjet', '#DeltaR lep closest jet',  wzero+'*('+cut+')', 50, 0, 5))
          variables.append(variabile('deltaR_lep_leadingjet', '#DeltaR lep lead jet',  wzero+'*('+cut+')', 50, 0, 5))
          variables.append(variabile('deltaR_lep_subleadingjet', '#DeltaR lep sub-lead jet',  wzero+'*('+cut+')', 50, 0, 5))
          variables.append(variabile('lepMET_deltaphi', '#Delta#phi(l, MET)',  wzero+'*('+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('jet1pt_jet2pt', 'p_{T}^{j_{1}}/p_{T}^{j_{2}}',  wzero+'*('+cut+')', 50, 1, 10))
          variables.append(variabile('MET_HT', 'MET/HT',  wzero+'*('+cut+')', 100, 0, 50))
          variables.append(variabile('lepMETpt_HT_nominal', 'p_{T}(l, MET)/HT',  wzero+'*('+cut+')', 100, 0, 50))


          variables.append(variabile('lepton_miniIso', 'lepton miniIso',  wzero+'*('+cut+')', 100, 0, 0.1))
          #variables.append(variabile('lepton_stdIso', 'lepton std Iso',  wzero+'*('+cut+')', 5, -0.5, 4.5))
          variables.append(variabile('best_top_m', 'top mass [GeV] (best)',  wzero+'*(best_top_m>0&&'+cut+')', 46, 80, 1000))
          variables.append(variabile('Event_HT', 'event HT [GeV]', wzero+'*('+cut+')', 70, 0, 1400))
          variables.append(variabile('MET_phi', 'Missing transverse momentum #phi',  wzero+'*('+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('njet_lowpt', 'no. of jets with 25 < p_{T} < 100 GeV',  wzero+'*('+cut+')', 8, 1.5, 9.5))
          variables.append(variabile('nbjet_lowpt', 'no. of b jets with 25 < p_{T} < 100 GeV',  wzero+'*('+cut+')', 9, -0.5, 8.5))
          variables.append(variabile('nfatjet', 'no. of AK8 jets',  wzero+'*('+cut+')', 5, 1.5, 6.5))
          variables.append(variabile('WprAK8_tau1', 'WprAK8 tau 1', wzero+'*('+cut+')', 80, 0, .8))
          variables.append(variabile('WprAK8_tau4', 'WprAK8 tau 4', wzero+'*('+cut+')', 20, 0, .2))
          variables.append(variabile('WprAK8_m', 'WprAK8 mass [GeV]', wzero+'*('+cut+')', 40, 0, 400))
          variables.append(variabile('WprAK8_mSD', 'WprAK8 soft drop mass [GeV]', wzero+'*('+cut+')', 40, 0, 400))
          variables.append(variabile('deltaR_bestWAK4_closestAK8', '#DeltaR (best)W\' AK4 closest AK8',  wzero+'*('+cut+')', 50, 0, 5))
          variables.append(variabile('best_topjet_isbtag', 'top jet b tagged (best)',  wzero+'*('+cut+')', 2, -0.5, 1.5))
          variables.append(variabile('best_Wpjet_isbtag', "W' jet b tagged (best)",  wzero+'*('+cut+')', 2, -0.5, 1.5))
          variables.append(variabile('MC_Wpjet_pt', "MCtruth W' jet p_{T} [GeV]",  wzero+'*('+cut+')', 150, 0, 3000))
          variables.append(variabile('MC_topjet_pt', "MCtruth top jet p_{T} [GeV]",  wzero+'*('+cut+')', 150, 0, 3000))
          variables.append(variabile('MC_top_pt', "MCtruth top p_{T} [GeV]",  wzero+'*('+cut+')', 150, 0, 3000))
          variables.append(variabile('MC_top_m', "MCtruth top m [GeV]",  wzero+'*('+cut+')', 46, 80, 1000))
          variables.append(variabile('MC_Wprime_pt', 'Wprime p_{T} [GeV] (MC)',  wzero+'*(MC_Wprime_pt>0&&'+cut+')', 150, 0, 3000))
          variables.append(variabile('MC_Wprime_eta', 'Wprime #eta (MC)', wzero+'*(MC_Wprime_eta>-10.&&'+cut+')', 48, -4., 4.))
          variables.append(variabile('MC_Wprime_phi', 'Wprime #phi (MC)',  wzero+'*(MC_Wprime_phi>-4.&&'+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('MC_Wprime_m', 'Wprime mass [GeV] (MC)',  wzero+'*(MC_Wprime_m>0&&'+cut+')',  61, 80, 5000))
          
          variables.append(variabile('bjets_pt', 'leading bjets system p_{T} [GeV]',  wzero+'*('+cut+')', 150, 0, 3000))
          variables.append(variabile('topAK8_area', 'topAK8 area', wzero+'*('+cut+')', 30, 1.5, 3.0))
          variables.append(variabile('topAK8_btag', 'topAK8 b tag ', wzero+'*(topAK8_btag>-1&&'+cut+')', 20, 0, 1.0))
          variables.append(variabile('topAK8_ttagMD', 'topAK8 t tag MD', wzero+'*(topAK8_ttagMD>-1&&'+cut+')', 20, 0, 1.0))
          variables.append(variabile('topAK8_ttag', 'topAK8 t tag', wzero+'*(topAK8_ttag>-1&&'+cut+')', 20, 0, 1.0))
          variables.append(variabile('topAK8_eta', 'topAK8 #eta', wzero+'*('+cut+')', 48, -4.8, 4.8)) 
          variables.append(variabile('topAK8_m', 'topAK8 mass [GeV]', wzero+'*('+cut+')', 40, 0, 400))
          variables.append(variabile('topAK8_phi', 'topAK8 #phi', wzero+'*('+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('topAK8_pt', 'topAK8 p_{T} [GeV]', wzero+'*('+cut+')', 200, 0, 2000))
          variables.append(variabile('topAK8_tau1', 'topAK8 tau 1', wzero+'*('+cut+')', 80, 0, .8))
          variables.append(variabile('topAK8_tau2', 'topAK8 tau 2', wzero+'*('+cut+')', 60, 0, .6))
          variables.append(variabile('topAK8_tau3', 'topAK8 tau 3', wzero+'*('+cut+')', 40, 0, .4))
          variables.append(variabile('topAK8_tau4', 'topAK8 tau 4', wzero+'*('+cut+')', 20, 0, .2))
          
          variables.append(variabile('leadingbjet_pt', 'leading bjet p_{T} [GeV]',  wzero+'*('+cut+')', 150, 0, 3000))
          variables.append(variabile('subleadingbjet_pt', 'subleading bjet p_{T} [GeV]',  wzero+'*('+cut+')', 150, 0, 3000))          
          variables.append(variabile('best_top_eta', 'top #eta (best)', wzero+'*(best_top_eta>-10.&&'+cut+')', 48, -4., 4.))
          variables.append(variabile('best_top_phi', 'top #phi (best)',  wzero+'*(best_top_phi>-4.&&'+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('chi_top_pt', 'top p_{T} [GeV] (chimass)',  wzero+'*(chi_top_pt>0&&'+cut+')', 150, 0, 3000))
          variables.append(variabile('chi_top_eta', 'top #eta (chimass)', wzero+'*(chi_top_eta>-10.&&'+cut+')', 48, -4., 4.))
          variables.append(variabile('chi_top_phi', 'top #phi (chimass)',  wzero+'*(chi_top_phi>-4.&&'+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('closest_top_pt', 'top p_{T} [GeV] (closest)',  wzero+'*(closest_top_pt>0&&'+cut+')', 150, 0, 3000))
          variables.append(variabile('closest_top_eta', 'top #eta (closest)', wzero+'*(closest_top_eta>-10.&&'+cut+')', 48, -4., 4.))
          variables.append(variabile('closest_top_phi', 'top #phi (closest)',  wzero+'*(closest_top_phi>-4.&&'+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('sublead_top_pt', 'top p_{T} [GeV] (sublead)',  wzero+'*(sublead_top_pt>0&&'+cut+')', 150, 0, 3000))
          variables.append(variabile('sublead_top_eta', 'top #eta (sublead)', wzero+'*(sublead_top_eta>-10.&&'+cut+')', 48, -4., 4.))
          variables.append(variabile('sublead_top_phi', 'top #phi (sublead)',  wzero+'*(sublead_top_phi>-4.&&'+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('GenPart_top_pt', 'top p_{T} [GeV] (GenPart)',  wzero+'*(GenPart_top_pt>0&&'+cut+')', 150, 0, 3000))
          variables.append(variabile('GenPart_top_eta', 'top #eta (GenPart)', wzero+'*(GenPart_top_eta>-10.&&'+cut+')', 48, -4., 4.))
          variables.append(variabile('GenPart_top_phi', 'top #phi (GenPart)',  wzero+'*(GenPart_top_phi>-4.&&'+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('GenPart_top_m', 'top mass [GeV] (GenPart)',  wzero+'*(GenPart_top_m>0&&'+cut+')', 46, 80, 1000))
          variables.append(variabile('GenPart_bottom_pt', 'bottom p_{T} [GeV] (GenPart)',  wzero+'*(GenPart_bottom_pt>0&&'+cut+')', 150, 0, 3000))
          variables.append(variabile('GenPart_bottom_eta', 'bottom #eta (GenPart)', wzero+'*(GenPart_bottom_eta>-10.&&'+cut+')', 48, -4., 4.))
          variables.append(variabile('GenPart_bottom_phi', 'bottom #phi (GenPart)',  wzero+'*(GenPart_bottom_phi>-4.&&'+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('GenPart_bottom_m', 'bottom mass [GeV] (GenPart)',  wzero+'*(GenPart_bottom_m>0&&'+cut+')',  92, 80, 1000))
          variables.append(variabile('chi_Wprime_pt', 'Wprime p_{T} [GeV] (chimass)',  wzero+'*(chi_Wprime_pt>0&&'+cut+')', 150, 0, 3000))
          variables.append(variabile('chi_Wprime_eta', 'Wprime #eta (chimass)', wzero+'*(chi_Wprime_eta>-10.&&'+cut+')', 48, -4., 4.))
          variables.append(variabile('chi_Wprime_phi', 'Wprime #phi (chimass)',  wzero+'*(chi_Wprime_phi>-4.&&'+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('best_Wprime_pt', 'Wprime p_{T} [GeV] (best)',  wzero+'*(best_Wprime_pt>0&&'+cut+')', 150, 0, 3000))
          variables.append(variabile('best_Wprime_eta', 'Wprime #eta (best)', wzero+'*(best_Wprime_eta>-10.&&'+cut+')', 48, -4., 4.))
          variables.append(variabile('best_Wprime_phi', 'Wprime #phi (best)',  wzero+'*(best_Wprime_phi>-4.&&'+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('closest_Wprime_pt', 'Wprime p_{T} [GeV] (closest)',  wzero+'*(closest_Wprime_pt>0&&'+cut+')', 150, 0, 3000))
          variables.append(variabile('closest_Wprime_eta', 'Wprime #eta (closest)', wzero+'*(closest_Wprime_eta>-10.&&'+cut+')', 48, -4., 4.))
          variables.append(variabile('closest_Wprime_phi', 'Wprime #phi (closest)',  wzero+'*(closest_Wprime_phi>-4.&&'+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('sublead_Wprime_pt', 'Wprime p_{T} [GeV] (sublead)',  wzero+'*(sublead_Wprime_pt>0&&'+cut+')', 150, 0, 3000))
          variables.append(variabile('sublead_Wprime_eta', 'Wprime #eta (sublead)', wzero+'*(sublead_Wprime_eta>-10.&&'+cut+')', 48, -4., 4.))
          variables.append(variabile('sublead_Wprime_phi', 'Wprime #phi (sublead)',  wzero+'*(sublead_Wprime_phi>-4.&&'+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('GenPart_Wprime_pt', 'Wprime p_{T} [GeV] (GenPart)',  wzero+'*(GenPart_Wprime_pt>0&&'+cut+')', 150, 0, 3000))
          variables.append(variabile('GenPart_Wprime_eta', 'Wprime #eta (GenPart)', wzero+'*(GenPart_Wprime_eta>-10.&&'+cut+')', 48, -4., 4.))
          variables.append(variabile('GenPart_Wprime_phi', 'Wprime #phi (GenPart)',  wzero+'*(GenPart_Wprime_phi>-4.&&'+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('GenPart_Wprime_m', 'Wprime mass [GeV] (GenPart)',  wzero+'*(GenPart_Wprime_m>0&&'+cut+')',  61, 80, 5000))
          variables.append(variabile('sublead_topjet_pt', 'sub leading jet p_{T} [GeV]',  wzero+'*('+cut+')', 150, 0, 3000))
          variables.append(variabile('sublead_topjet_eta', 'sub leading jet #eta',  wzero+'*('+cut+')', 48, -2.4, 2.4))
          variables.append(variabile('closest_topjet_eta', 'closest top jet #eta',  wzero+'*('+cut+')', 48, -2.4, 2.4))
          variables.append(variabile('closest_topjet_pt', 'closest top jet p_{T} [GeV]',  wzero+'*('+cut+')', 150, 0, 3000))
          variables.append(variabile('chi_topjet_eta', 'chi top jet #eta',  wzero+'*('+cut+')', 48, -2.4, 2.4))
          variables.append(variabile('chi_topjet_pt', 'chi top jet p_{T} [GeV]',  wzero+'*('+cut+')', 150, 0, 3000))
          variables.append(variabile('best_topjet_eta', 'best top jet #eta',  wzero+'*('+cut+')', 48, -2.4, 2.4))
          variables.append(variabile('best_topjet_pt', 'best top jet p_{T} [GeV]',  wzero+'*('+cut+')', 150, 0, 3000))
          variables.append(variabile('sublead_Wpjet_pt', '(sublead) leading jet p_{T} [GeV] ',  wzero+'*('+cut+')', 150, 0, 3000))
          variables.append(variabile('closest_Wpjet_pt', '(closest) leading jet p_{T} [GeV] ',  wzero+'*('+cut+')', 150, 0, 3000))
          variables.append(variabile('best_Wpjet_pt', '(best) leading jet p_{T} [GeV] ',  wzero+'*('+cut+')', 150, 0, 3000))
          variables.append(variabile('chi_Wpjet_pt', '(chimass) leading jet p_{T} [GeV] ',  wzero+'*('+cut+')', 150, 0, 3000))
          
          variables.append(variabile('sublead_Wpjet_eta', 'leading jet #eta',  wzero+'*('+cut+')', 48, -2.4, 2.4))
          variables.append(variabile('sublead_Wpjet_isbtag', 'leading jet b tagged',  wzero+'*('+cut+')', 2, -0.5, 1.5))

          variables.append(variabile('leadingjets_deltaR', 'leadings jets #DeltaR',  wzero+'*('+cut+')', 10, 0, 5))
          variables.append(variabile('leadingjets_deltaPhi', 'leadings jets #Delta#phi',  wzero+'*('+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('leadingjets_deltaEta', 'leadings jets #Delta#eta',  wzero+'*('+cut+')', 48, -4.8, 4.8))
          variables.append(variabile('bjets_deltaR', 'b jets #DeltaR',  wzero+'*(bjets_deltaR>-50.&&'+cut+')', 10, 0, 5))
          variables.append(variabile('bjets_deltaPhi', 'b jets #Delta#phi',  wzero+'*(bjets_deltaPhi>-50.&&'+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('bjets_deltaEta', 'b jets #Delta#eta',  wzero+'*(bjets_deltaEta>-50.&&'+cut+')', 48, -4.8, 4.8))
          variables.append(variabile('bjets_pt', 'b jets system p_{T} [GeV]',  wzero+'*(bjets_pt>-10.&&'+cut+')', 150, 0, 3000))
          variables.append(variabile('had_global_thrust', 'hadronic global thrust',  wzero+'*('+cut+')', 20, 0.5, 1))
          variables.append(variabile('had_central_thrust', 'hadronic transverse thrust',  wzero+'*('+cut+')', 20, 0, 0.5))
          variables.append(variabile('ovr_global_thrust', 'event global thrust',  wzero+'*('+cut+')', 20, 0.5, 1))
          variables.append(variabile('ovr_central_thrust', 'event transverse thrust',  wzero+'*('+cut+')', 20, 0, 0.5))
          variables.append(variabile('best_topjet_dRLepJet', '#DeltaR lep jet (best crit)',  wzero+'*('+cut+')', 50, 0, 5))
          variables.append(variabile('closest_topjet_dRLepJet', '#DeltaR lep jet (closest crit)',  wzero+'*('+cut+')', 50, 0, 5))
          variables.append(variabile('sublead_topjet_dRLepJet', '#DeltaR lep jet (sublead crit)',  wzero+'*('+cut+')', 50, 0, 5))
          variables.append(variabile('chi_topjet_dRLepJet', '#DeltaR lep jet (chi crit)',  wzero+'*('+cut+')', 50, 0, 5))
          variables.append(variabile('ptrel_leadAK4_closestAK8', 'pt rel leading AK4 closest AK8',  wzero+'*('+cut+')', 50, 0, 5))
          variables.append(variabile('deltaR_leadAK4_closestAK8', '#DeltaR leading AK4 closest AK8',  wzero+'*('+cut+')',  20, 0, 2))
          variables.append(variabile('ptrel_subleadAK4_closestAK8', 'pt rel sub-leading AK4 closest AK8',  wzero+'*('+cut+')', 50, 0, 5))
          variables.append(variabile('deltaR_subleadAK4_closestAK8', '#DeltaR sub-leading AK4 closest AK8',  wzero+'*('+cut+')', 50, 0, 5))
          variables.append(variabile('ptrel_besttopAK4_closestAK8', 'pt rel (best)top AK4 closest AK8',  wzero+'*('+cut+')', 50, 0, 5))
          variables.append(variabile('deltaR_besttopAK4_closestAK8', '#DeltaR (best)top AK4 closest AK8',  wzero+'*('+cut+')', 50, 0, 5))
          variables.append(variabile('ptrel_bestWAK4_closestAK8', 'pt rel (best)W\' AK4 closest AK8',  wzero+'*('+cut+')', 50, 0, 5))
          variables.append(variabile('best_topW_jets_pt', 'jets (t+W\') p_{T} [GeV] (best)',  wzero+'*('+cut+')', 150, 0, 1500))
          variables.append(variabile('best_topW_jets_deltaR', '#DeltaR jets (t+W\') (best)',  wzero+'*('+cut+')', 50, 0, 5))
          variables.append(variabile('best_topW_jets_deltaPhi', '#Delta #phi jets (t+W\') (best)',  wzero+'*('+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('ptrel_chitopAK4_closestAK8', 'pt rel (chi)top AK4 closest AK8',  wzero+'*('+cut+')', 50, 0, 5))
          variables.append(variabile('deltaR_chitopAK4_closestAK8', '#DeltaR (chi)top AK4 closest AK8',  wzero+'*('+cut+')', 50, 0, 5))
          variables.append(variabile('ptrel_chiWAK4_closestAK8', 'pt rel (chi)W\' AK4 closest AK8',  wzero+'*('+cut+')', 50, 0, 5))
          variables.append(variabile('deltaR_chiWAK4_closestAK8', '#DeltaR (chi)W\' AK4 closest AK8',  wzero+'*('+cut+')', 50, 0, 5))
          variables.append(variabile('chi_topW_jets_pt', 'jets (t+W\') p_{T} [GeV] (chi)',  wzero+'*('+cut+')', 150, 0, 1500))
          variables.append(variabile('chi_topW_jets_deltaR', '#DeltaR jets (t+W\') (chi)',  wzero+'*('+cut+')', 50, 0, 5))
          variables.append(variabile('chi_topW_jets_deltaPhi', '#Delta #phi jets (t+W\') (chi)',  wzero+'*('+cut+')', 20, -3.14, 3.14))
          
          variables.append(variabile('best_top_costhetalep', 'cos #theta (lepton)', wzero+'*('+cut+')', 50, 0, 1))
          variables.append(variabile('best_top_costheta', 'cos #theta', wzero+'*('+cut+')', 50, 0, 1))

          variables.append(variabile('WprAK8_area',  "W' AK8 area", wzero+'*('+cut+')', 30, 1.5, 3.0))
          variables.append(variabile('WprAK8_btag', 'WprAK8 b tag ', wzero+'*(WprAK8_btag>-1&&'+cut+')', 20, 0, 1.0))
          variables.append(variabile('WprAK8_ttagMD', 'WprAK8 t tag MD', wzero+'*(WprAK8_ttagMD>-1&&'+cut+')', 20, 0, 1.0))
          variables.append(variabile('WprAK8_ttag', 'WprAK8 t tag', wzero+'*(WprAK8_ttag>-1&&'+cut+')', 20, 0, 1.0))
          variables.append(variabile('WprAK8_eta', 'WprAK8 #eta', wzero+'*('+cut+')', 48, -4.8, 4.8)) 
          variables.append(variabile('WprAK8_phi', 'WprAK8 #phi', wzero+'*('+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('WprAK8_pt', 'WprAK8 p_{T} [GeV]', wzero+'*('+cut+')', 200, 0, 2000))
          '''
          for sample in dataset_new:
               if(opt.plot):
                    for syst in systematics:
                         for var in variables:
                              if (("GenPart" in var._name) or ("MC_" in var._name)) and "Data" in sample.label:
                                   continue
                              plot(lep, 'jets', var, sample, cut_tag, syst)
          if(opt.stack):
               #for syst in systematics:
               for var in variables:
                    os.system('set LD_PRELOAD=libtcmalloc.so')
                    makestack(lep, 'jets', var, dataset_new, cut_tag, "", lumi[str(year)])
                    os.system('set LD_PRELOAD=libtcmalloc.so')
          #if lep == 'muon':
               #dataset_new.append(sample_dict['DataEle_'+str(year)])
          #elif lep == 'electron':
               #dataset_new.append(sample_dict['DataMu_'+str(year)])
          
