import os, commands
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
parser.add_option('-L', '--lep', dest='lep', type='string', default = 'muon', help='Default make muon analysis')
parser.add_option('-S', '--syst', dest='syst', type='string', default = 'all', help='Default all systematics added')
parser.add_option('-C', '--cut', dest='cut', type='string', default = 'lepton_eta>-10.', help='Default no cut')
parser.add_option('-y', '--year', dest='year', type='string', default = 'all', help='Default 2016, 2017 and 2018 are included')
parser.add_option('-f', '--folder', dest='folder', type='string', default = 'v1', help='Default folder is v0')
#parser.add_option('-T', '--topol', dest='topol', type='string', default = 'all', help='Default all njmt')
parser.add_option('-d', '--dat', dest='dat', type='string', default = 'all', help="")
(opt, args) = parser.parse_args()

folder = opt.folder
#filerepo = '/eos/user/a/adeiorio/Wprime/nosynch/' + folder + '/'
filerepo = '/eos/user/a/apiccine/Wprime/nosynch/' + folder + '/'
ROOT.gROOT.SetBatch() # don't pop up canvases
if not os.path.exists(filerepo + 'plot/muon'):
     os.makedirs(filerepo + 'plot/muon')
if not os.path.exists(filerepo + 'plot/electron'):
     os.makedirs(filerepo + 'plot/electron')
if not os.path.exists(filerepo + 'stack'):
     os.makedirs(filerepo + 'stack')

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
          print "Number of entries of the file %s are %s" %(filerepo + sample.label + "/"  + sample.label + "_merged.root", (check.Get("events_all")).GetEntries())

def mergetree(sample):
     if not os.path.exists(filerepo + sample.label):
          os.makedirs(filerepo + sample.label)
     add = "hadd -f " + filerepo + sample.label + "/"  + sample.label + ".root" 
     for comp in sample.components:
          add+= " " + filerepo + comp.label + "/"  + comp.label + ".root" 
     print add
     os.system(str(add))

def lumi_writer(dataset, lumi):
     samples = []
     if hasattr(dataset, 'components'): # How to check whether this exists or not
          samples = [sample for sample in dataset.components]# Method exists and was used.
     else:
          samples.append(dataset)
     for sample in samples:
          if not 'Data' in sample.label:
               infile =  ROOT.TFile.Open(filerepo + sample.label + "/"  + sample.label + "_merged.root")
               tree = infile.Get('events_all')
               tree.SetBranchStatus('w_nominal', 0)
               tree.SetBranchStatus('w_PDF', 0)
               outfile =  ROOT.TFile.Open(filerepo + sample.label + "/"  + sample.label + ".root","RECREATE")
               tree_new = tree.CloneTree(0)
               print("Getting the histos from %s" %(infile))
               h_genw_tmp = ROOT.TH1F(infile.Get("h_genweight"))
               h_pdfw_tmp = ROOT.TH1F(infile.Get("h_PDFweight"))
               nbins = h_pdfw_tmp.GetXaxis().GetNbins()
               print("h_genweight first bin content is %f and h_PDFweight has %f bins" %(h_genw_tmp.GetBinContent(1), nbins))
               w_nom = array('f', [0.]) 
               w_PDF = array('f', [0.]*nbins)
               print(nbins)
               print(len(w_PDF))
               tree_new.Branch('w_nominal', w_nom, 'w_nominal/F')
               tree_new.Branch('w_PDF', w_PDF, 'w_PDF/F')
               tree.SetBranchStatus('w_nominal', 1)
               for event in xrange(0, tree.GetEntries()):
                    tree.GetEntry(event)
                    if event%10000==1:
                         print("Processing event %s     complete %s percent" %(event, 100*event/tree.GetEntries()))
                    if not (tree.w_nominal==0):
                         w_nom[0] = tree.w_nominal * sample.sigma * lumi * 1000./float(h_genw_tmp.GetBinContent(1))
                    else:
                         w_nom[0] = sample.sigma * lumi * 1000./float(h_genw_tmp.GetBinContent(1))
                    for i in xrange(1, nbins):
                         w_PDF[i] = h_pdfw_tmp.GetBinContent(i+1)/h_genw_tmp.GetBinContent(2) 
                    tree_new.Fill()
               tree_new.Write()
               outfile.Close()
          else:
               os.popen("mv " + filerepo + sample.label + "/"  + sample.label + "_merged.root " + filerepo + sample.label + "/"  + sample.label + ".root")

def cutToTag(cut):
    newstring = cut.replace("-", "neg").replace(">=","_GE_").replace(">","_G_").replace(" ","").replace("&&","_AND_").replace("||","_OR_").replace("<=","_LE_").replace("<","_L_").replace(".","p").replace("(","").replace(")","").replace("==","_EQ_").replace("!=","_NEQ_").replace("=","_EQ_").replace("*","_AND_").replace("+","_OR_")
    return newstring

def plot(lep, reg, variable, sample, cut_tag, syst):
     print "plotting ", variable._name, " for sample ", sample.label, " with cut ", cut_tag, " ", syst,
     ROOT.TH1.SetDefaultSumw2()
     f1 = ROOT.TFile.Open(filerepo + sample.label + "/"  + sample.label + ".root")
     treename = "events_all"
     if(cut_tag == ""):
          histoname = "h_" + reg + "_" + variable._name
     else:
          histoname = "h_" + reg + "_" + variable._name + "_" + cut_tag
     nbins = variable._nbins
     h1 = ROOT.TH1F(histoname, variable._name + "_" + reg, variable._nbins, variable._xmin, variable._xmax)
     h1.Sumw2()
     if 'muon' in lep: 
          cut  = variable._taglio+ '*isMu'
          #if not 'Data' in sample.label:
               #cut += '*passed_mu'
     elif 'electron' in lep:
          cut  = variable._taglio + '*isEle'
          #if not 'Data' in sample.label:
               #cut += '*passed_ele'
     print str(cut)
     foutput = filerepo + "plot/" + lep + "/" + sample.label + "_" + lep+".root"
     '''
     else:
          if(syst==""):
            taglio = variable._taglio+"*w_nominal"
            foutput = "Plot/"+lep+"/"+channel+"_"+lep+".root"
        elif(syst.startswith("jer") or syst.startswith("jes")):
            taglio = variable._taglio+"*w_nominal"
            treename = "events_"+reg+"_"+syst
            foutput = "Plot/"+lep+"/"+channel+"_"+lep+"_"+syst+".root"
            if(channel == "WJets_ext" and lep.startswith("electron")):
                taglio = variable._taglio+"*w_nominal*(abs(w)<10)"
     '''
     #print treename
     f1.Get(treename).Project(histoname,variable._name,cut)
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
     infile = {}
     histo = []
     tmp = ROOT.TH1F()
     h = ROOT.TH1F()
     hdata = ROOT.TH1F('h','h', variabile_._nbins, variabile_._xmin, variabile_._xmax)
     h_sig = []
     h_err = ROOT.TH1F()
     h_bkg_err = ROOT.TH1F()
     print "Variabile:", variabile_._name
     ROOT.gROOT.SetStyle('Plain')
     ROOT.gStyle.SetPalette(1)
     ROOT.gStyle.SetOptStat(0)
     ROOT.TH1.SetDefaultSumw2()
     if(cut_tag_ == ""):
          histoname = "h_" + reg_ + "_" + variabile_._name
          stackname = "stack_" + reg_ + "_" + variabile_._name
          canvasname = "stack_" + reg_ + "_" + variabile_._name + "_" + lep_
     else:
          histoname = "h_"+reg_+"_"+variabile_._name+"_"+cut_tag_
          stackname = "stack_"+reg_+"_"+variabile_._name+"_"+cut_tag_
          canvasname = "stack_"+reg_+"_"+variabile_._name+"_"+cut_tag_+"_"+lep_
     stack = ROOT.THStack(stackname, variabile_._name)
     leg_stack = ROOT.TLegend(0.33,0.62,0.91,0.87)
     signal = False

     print samples_
     for s in samples_:
          if('WP' in s.label):
               signal = True
          if(syst_ == ""):
               outfile = filerepo + "stack_" + str(lep_).strip('[]') + ".root"
               infile[s.label] = ROOT.TFile.Open(filerepo + "plot/" + lep + "/" + s.label + "_" + lep + ".root")
          else:
               outfile = filerepo + "stack_"+syst_+"_"+str(lep_).strip('[]')+".root"
               infile[s.label] = ROOT.TFile.Open(filerepo + "plot/" + lep + "/" + s.label + "_" + lep + "_" + syst_ + ".root")
     i = 0

     for s in samples_:
          infile[s.label].cd()
          print "opening file: ", infile[s.label].GetName()
          tmp = (ROOT.TH1F)(infile[s.label].Get(histoname))
          tmp.SetLineColor(ROOT.kBlack)
          tmp.SetName(s.leglabel)
          if('Data' in s.label):
               hdata.Add(ROOT.TH1F(tmp.Clone("")))
               hdata.SetMarkerStyle(20)
               hdata.SetMarkerSize(0.9)
               if(i == 0): # trick to add Data flag to legend only once
                    leg_stack.AddEntry(hdata, "Data", "ep")
               i += 1
          elif('WP' in s.label):
               #tmp.SetLineStyle(9)
               tmp.SetLineColor(s.color)
               #tmp.SetLineWidth(3)
               tmp.SetMarkerSize(0.)
               tmp.SetMarkerColor(s.color)
               h_sig.append(ROOT.TH1F(tmp.Clone("")))
          else:
               tmp.SetOption("HIST SAME")
               tmp.SetTitle("")
               tmp.SetFillColor(s.color)
               histo.append(tmp.Clone(""))
               stack.Add(tmp.Clone(""))
          tmp.Reset("ICES")
     for hist in reversed(histo):
          if not ('Data' in hist.GetName()):
               leg_stack.AddEntry(hist, hist.GetName(), "f")
     #style options
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

     maximum = max(stack.GetMaximum(),hdata.GetMaximum())
     logscale = True # False #
     if(logscale):
          pad1.SetLogy()
          stack.SetMaximum(maximum*1000)
     else:
          stack.SetMaximum(maximum*1.6)
     stack.SetMinimum(0.01)
     stack.Draw("HIST")
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
               hsig.Draw("same L")
               leg_stack.AddEntry(hsig, hsig.GetName(), "l")
     h_err = stack.GetStack().Last().Clone("h_err")
     h_err.SetLineWidth(100)
     h_err.SetFillStyle(3154)
     h_err.SetMarkerSize(0)
     h_err.SetFillColor(ROOT.kGray+2)
     h_err.Draw("e2same0")
     leg_stack.AddEntry(h_err, "Stat. Unc.", "f")
     print(hdata.Integral())
     hdata.Draw("eSAMEpx0")
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
     #c1.Print("stack/"+canvasname+".pdf")
     c1.Print(filerepo + "stack/"+canvasname+".png")
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
          '2016':[DataMu_2016, DataEle_2016, DataHT_2016, ST_2016, QCD_2016, TT_Mtt_2016, WJets_2016, WP_M2000W20_RH_2016, WP_M3000W30_RH_2016, WP_M4000W40_RH_2016, WP_M4000W400_RH_2016],
          '2017':[DataMu_2017, DataEle_2017, TT_Mtt_2017, WJets_2017],
          '2018':[DataMu_2018, DataEle_2018, TT_Mtt_2018, WJets_2018]}
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
     cut_dict = {'muon':"lepton_eta>-10.", 'electron':"lepton_eta>-10."}
     cut_tag = ""
else:
     if opt.sel:
          cut_dict = {'muon':"lepton_pt>125&&leadingjet_pt>300&&subleadingjet_pt>150&&" + cut, 'electron':"MET_pt>125&&lepton_pt>50&&leadingjet_pt>300&&subleadingjet_pt>150&&" + cut}
          if opt.cut != "lepton_eta>-10.":
               cut_tag = 'selection_AND_' + cutToTag(opt.cut) 
          else:
               cut_tag = 'selection' 
     else:
          cut_dict = {'muon':cut, 'electron':cut}
          cut_tag = cutToTag(opt.cut)

lumi = {'2016': 35.89, "2017": 41.53, "2018": 59.7}


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
          if lep == 'muon' and sample_dict['DataEle_'+str(year)] in dataset_new:
               dataset_new.remove(sample_dict['DataEle_'+str(year)])
          elif lep == 'electron' and sample_dict['DataMu_'+str(year)] in dataset_new:
               dataset_new.remove(sample_dict['DataMu_'+str(year)])

          variables = []
          wzero = 'w_nominal'
          cut = cut_dict[lep]
          #variables.append(variabile('lepton_pt', 'lepton p_{T} [GeV]', wzero+'*('+cut+')', 200, 0, 1200))
          variables.append(variabile('lepton_pt', 'lepton p_{T} [GeV]', wzero+'*('+cut+')', 100, 0, 1200))
          variables.append(variabile('lepton_eta', 'lepton #eta', wzero+'*('+cut+')', 48, -2.4, 2.4))
          variables.append(variabile('lepton_phi', 'lepton #phi',  wzero+'*('+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('lepton_miniIso', 'lepton miniIso',  wzero+'*('+cut+')', 100, 0, 0.1))
          variables.append(variabile('lepMET_deltaphi', '#Delta#phi(l, MET)',  wzero+'*('+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('deltaR_lep_closestjet', '#DeltaR lep closest jet',  wzero+'*('+cut+')', 50, 0, 5))
          variables.append(variabile('deltaR_lep_leadingjet', '#DeltaR lep lead jet',  wzero+'*('+cut+')', 50, 0, 5))
          variables.append(variabile('deltaR_lep_subleadingjet', '#DeltaR lep sub-lead jet',  wzero+'*('+cut+')', 50, 0, 5))
          variables.append(variabile('MET_pt', "Missing transverse momentum [GeV]",wzero+'*('+cut+')', 100, 0, 1000))
          variables.append(variabile('Event_HT', 'event HT [GeV]', wzero+'*('+cut+')', 70, 0, 1400))
          variables.append(variabile('MET_phi', 'Missing transverse momentum #phi',  wzero+'*('+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('best_top_pt', 'top p_{T} [GeV] (best)',  wzero+'*(best_top_pt>0&&'+cut+')', 100, 0, 1200))
          variables.append(variabile('best_top_eta', 'top #eta (best)', wzero+'*(best_top_eta>-10.&&'+cut+')', 48, -4., 4.))
          variables.append(variabile('best_top_phi', 'top #phi (best)',  wzero+'*(best_top_phi>-4.&&'+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('best_top_m', 'top mass [GeV] (best)',  wzero+'*(best_top_m>0&&'+cut+')',  392, 80, 4000))
          variables.append(variabile('chi_top_pt', 'top p_{T} [GeV] (chimass)',  wzero+'*(chi_top_pt>0&&'+cut+')', 100, 0, 1200))
          variables.append(variabile('chi_top_eta', 'top #eta (chimass)', wzero+'*(chi_top_eta>-10.&&'+cut+')', 48, -4., 4.))
          variables.append(variabile('chi_top_phi', 'top #phi (chimass)',  wzero+'*(chi_top_phi>-4.&&'+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('chi_top_m', 'top mass [GeV] (chimass)',  wzero+'*(chi_top_m>0&&'+cut+')',  392, 80, 4000))
          variables.append(variabile('closest_top_pt', 'top p_{T} [GeV] (closest)',  wzero+'*(closest_top_pt>0&&'+cut+')', 100, 0, 1200))
          variables.append(variabile('closest_top_eta', 'top #eta (closest)', wzero+'*(closest_top_eta>-10.&&'+cut+')', 48, -4., 4.))
          variables.append(variabile('closest_top_phi', 'top #phi (closest)',  wzero+'*(closest_top_phi>-4.&&'+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('closest_top_m', 'top mass [GeV] (closest)',  wzero+'*(closest_top_m>0&&'+cut+')',  392, 80, 4000))
          variables.append(variabile('sublead_top_pt', 'top p_{T} [GeV] (sublead)',  wzero+'*(sublead_top_pt>0&&'+cut+')', 100, 0, 1200))
          variables.append(variabile('sublead_top_eta', 'top #eta (sublead)', wzero+'*(sublead_top_eta>-10.&&'+cut+')', 48, -4., 4.))
          variables.append(variabile('sublead_top_phi', 'top #phi (sublead)',  wzero+'*(sublead_top_phi>-4.&&'+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('sublead_top_m', 'top mass [GeV] (sublead)',  wzero+'*(sublead_top_m>0&&'+cut+')',  392, 80, 4000))
          variables.append(variabile('chi_Wprime_pt', 'Wprime p_{T} [GeV] (chimass)',  wzero+'*(chi_Wprime_pt>0&&'+cut+')', 350, 0, 4200))
          variables.append(variabile('chi_Wprime_eta', 'Wprime #eta (chimass)', wzero+'*(chi_Wprime_eta>-10.&&'+cut+')', 48, -4., 4.))
          variables.append(variabile('chi_Wprime_phi', 'Wprime #phi (chimass)',  wzero+'*(chi_Wprime_phi>-4.&&'+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('chi_Wprime_m', 'Wprime mass [GeV] (chimass)',  wzero+'*(chi_Wprime_m>0&&'+cut+')',  250, 80, 6000))
          variables.append(variabile('best_Wprime_pt', 'Wprime p_{T} [GeV] (best)',  wzero+'*(best_Wprime_pt>0&&'+cut+')', 350, 0, 4200))
          variables.append(variabile('best_Wprime_eta', 'Wprime #eta (best)', wzero+'*(best_Wprime_eta>-10.&&'+cut+')', 48, -4., 4.))
          variables.append(variabile('best_Wprime_phi', 'Wprime #phi (best)',  wzero+'*(best_Wprime_phi>-4.&&'+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('best_Wprime_m', 'Wprime mass [GeV] (best)',  wzero+'*(best_Wprime_m>0&&'+cut+')',  250, 80, 6000))
          variables.append(variabile('closest_Wprime_pt', 'Wprime p_{T} [GeV] (closest)',  wzero+'*(closest_Wprime_pt>0&&'+cut+')', 350, 0, 4200))
          variables.append(variabile('closest_Wprime_eta', 'Wprime #eta (closest)', wzero+'*(closest_Wprime_eta>-10.&&'+cut+')', 48, -4., 4.))
          variables.append(variabile('closest_Wprime_phi', 'Wprime #phi (closest)',  wzero+'*(closest_Wprime_phi>-4.&&'+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('closest_Wprime_m', 'Wprime mass [GeV] (closest)',  wzero+'*(closest_Wprime_m>0&&'+cut+')',  250, 80, 6000))
          variables.append(variabile('sublead_Wprime_pt', 'Wprime p_{T} [GeV] (sublead)',  wzero+'*(sublead_Wprime_pt>0&&'+cut+')', 350, 0, 4200))
          variables.append(variabile('sublead_Wprime_eta', 'Wprime #eta (sublead)', wzero+'*(sublead_Wprime_eta>-10.&&'+cut+')', 48, -4., 4.))
          variables.append(variabile('sublead_Wprime_phi', 'Wprime #phi (sublead)',  wzero+'*(sublead_Wprime_phi>-4.&&'+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('sublead_Wprime_m', 'Wprime mass [GeV] (sublead)',  wzero+'*(sublead_Wprime_m>0&&'+cut+')',  250, 80, 6000))
          #variables.append(variabile('sublead_topjet_pt', 'sub leading jet p_{T} [GeV]',  wzero+'*('+cut+')', 100, 0, 1200))
          #variables.append(variabile('sublead_topjet_eta', 'sub leading jet #eta',  wzero+'*('+cut+')', 48, -2.4, 2.4))
          #variables.append(variabile('sublead_Wpjet_pt', 'leading jet p_{T} [GeV]',  wzero+'*('+cut+')', 100, 0, 2000))
          #variables.append(variabile('sublead_Wpjet_eta', 'leading jet #eta',  wzero+'*('+cut+')', 48, -2.4, 2.4))
          variables.append(variabile('sublead_Wpjet_isbtag', 'leading jet b tagged',  wzero+'*('+cut+')', 2, -0.5, 1.5))
          variables.append(variabile('njet_lowpt', 'no. of jets with p_{T} < 100 GeV',  wzero+'*('+cut+')', 8, 1.5, 9.5))
          variables.append(variabile('njet_pt100', 'no. of jets with p_{T} > 100 GeV',  wzero+'*('+cut+')', 8, 1.5, 9.5))
          variables.append(variabile('nbjet_lowpt', 'no. of b jets with p_{T} < 100 GeV',  wzero+'*('+cut+')', 9, -0.5, 8.5))
          variables.append(variabile('nbJet_pt100', 'no. of b jets with p_{T} > 100 GeV',  wzero+'*('+cut+')', 7, -0.5, 6.5))
          variables.append(variabile('leadingjet_pt', 'leading jet p_{T} [GeV]',  wzero+'*('+cut+')', 100, 150, 2000))
          variables.append(variabile('subleadingjet_pt', 'sub leading jet p_{T} [GeV]',  wzero+'*('+cut+')', 100, 0, 2000))
          variables.append(variabile('leadingjets_deltaR', 'leadings jets #DeltaR',  wzero+'*('+cut+')', 10, 0, 5))
          variables.append(variabile('leadingjets_deltaPhi', 'leadings jets #Delta#phi',  wzero+'*('+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('leadingjets_deltaEta', 'leadings jets #Delta#eta',  wzero+'*('+cut+')', 48, -4.8, 4.8))
          variables.append(variabile('leadingjets_pt', 'leadings jets system p_{T} [GeV]',  wzero+'*('+cut+')', 100, 0, 2000))
          variables.append(variabile('bjets_deltaR', 'b jets #DeltaR',  wzero+'*(bjets_deltaR>-50.&&'+cut+')', 10, 0, 5))
          variables.append(variabile('bjets_deltaPhi', 'b jets #Delta#phi',  wzero+'*(bjets_deltaPhi>-50.&&'+cut+')', 20, -3.14, 3.14))
          variables.append(variabile('bjets_deltaEta', 'b jets #Delta#eta',  wzero+'*(bjets_deltaEta>-50.&&'+cut+')', 48, -4.8, 4.8))
          variables.append(variabile('bjets_pt', 'b jets system p_{T} [GeV]',  wzero+'*(bjets_pt>-10.&&'+cut+')', 100, 0, 2000))
          variables.append(variabile('mtw', 'W boson transverse mass [GeV]',  wzero+'*('+cut+')', 100, 0, 500))
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
          variables.append(variabile('deltaR_bestWAK4_closestAK8', '#DeltaR (best)W\' AK4 closest AK8',  wzero+'*('+cut+')', 50, 0, 5))
          variables.append(variabile('best_topW_jets_pt', 'jets (t+W\') p_{T} [GeV] (best)',  wzero+'*('+cut+')', 150, 0, 1500))
          #variables.append(variabile('best_topW_jets_deltaR', '#DeltaR jets (t+W\') (best)',  wzero+'*('+cut+')', 50, 0, 5))
          #variables.append(variabile('best_topW_jets_deltaPhi', '#Delta #phi jets (t+W\') (best)',  wzero+'*('+cut+')', 20, -3.14, 3.14))
          #variables.append(variabile('ptrel_chitopAK4_closestAK8', 'pt rel (chi)top AK4 closest AK8',  wzero+'*('+cut+')', 50, 0, 5))
          #variables.append(variabile('deltaR_chitopAK4_closestAK8', '#DeltaR (chi)top AK4 closest AK8',  wzero+'*('+cut+')', 50, 0, 5))
          #variables.append(variabile('ptrel_chiWAK4_closestAK8', 'pt rel (chi)W\' AK4 closest AK8',  wzero+'*('+cut+')', 50, 0, 5))
          #variables.append(variabile('deltaR_chiWAK4_closestAK8', '#DeltaR (chi)W\' AK4 closest AK8',  wzero+'*('+cut+')', 50, 0, 5))
          #variables.append(variabile('chi_topW_jets_pt', 'jets (t+W\') p_{T} [GeV] (chi)',  wzero+'*('+cut+')', 150, 0, 1500))
          #variables.append(variabile('chi_topW_jets_deltaR', '#DeltaR jets (t+W\') (chi)',  wzero+'*('+cut+')', 50, 0, 5))
          #variables.append(variabile('chi_topW_jets_deltaPhi', '#Delta #phi jets (t+W\') (chi)',  wzero+'*('+cut+')', 20, -3.14, 3.14))

          #variables.append(variabile('nPV_good', 'n good PV', wzero+'*('+cut+')', 120, 0, 120))
          #variables.append(variabile('nPV_tot', 'total n PV', wzero+'*('+cut+')', 120, 0, 120))
          for sample in dataset_new:
               if(opt.plot):
                    for var in variables:
                         plot(lep, 'jets', var, sample, cut_tag, "")
          if(opt.stack):
               for var in variables:
                    os.system('set LD_PRELOAD=libtcmalloc.so')
                    makestack(lep, 'jets', var, dataset_new, cut_tag, "", lumi[str(year)])
                    os.system('set LD_PRELOAD=libtcmalloc.so')
