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
parser.add_option('-p', '--plot', dest='plot', default = False, action='store_true', help='Default make no plots')
parser.add_option('-s', '--stack', dest='stack', default = False, action='store_true', help='Default make no stacks')
parser.add_option('-L', '--lep', dest='lep', type='string', default = 'muon', help='Default make muon analysis')
parser.add_option('-S', '--syst', dest='syst', type='string', default = 'all', help='Default all systematics added')
parser.add_option('-C', '--cut', dest='cut', type='string', default = 'DetReco_Lepton_m>0', help='Default no cut')
parser.add_option('-y', '--year', dest='year', type='string', default = 'all', help='Default 2016, 2017 and 2018 are included')
#parser.add_option('-T', '--topol', dest='topol', type='string', default = 'all', help='Default all njmt')
parser.add_option('-d', '--dat', dest='dat', type='string', default = 'all', help="")
(opt, args) = parser.parse_args()

filerepo = '/eos/user/a/adeiorio/Wprime/nosynch/'
ROOT.gROOT.SetBatch() # don't pop up canvases

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
          print "Number of entries of the file %s are %s" %(filerepo + sample.label + "/"  + sample.label + "_merged.root", (check.Get("events_signal")).GetEntries())

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
               tree = infile.Get('events_signal')
               tree.SetBranchStatus('w_nominal', 0)
               tree.SetBranchStatus('w_PDF', 0)
               outfile =  ROOT.TFile.Open(filerepo + sample.label + "/"  + sample.label + ".root","RECREATE")
               tree_new = tree.CloneTree(0)
               print("Getting the histos from %s" %(infile))
               h_genw_tmp = ROOT.TH1F(infile.Get("h_genweight_add"))
               h_pdfw_tmp = ROOT.TH1F(infile.Get("h_PDFweight_add"))
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
    newstring = cut.replace(">=","_GE_").replace(">","_G_").replace(" ","").replace("&&","_AND_").replace("||","_OR_").replace("<=","_LE_").replace("<","_L_").replace(".","p").replace("(","").replace(")","").replace("==","_EQ_").replace("=","_EQ_").replace("*","_AND_").replace("+","_OR_")
    return newstring

def plot(lep, reg, variable, sample, cut_tag, syst):
     print "plotting ", variable._name, " ", cut_tag, " ", syst
     ROOT.TH1.SetDefaultSumw2()
     f1 = ROOT.TFile.Open(filerepo + sample.label + "/"  + sample.label + ".root")
     treename = "events_signal"
     if(cut_tag == ""):
          histoname = "h_"+reg+"_"+variable._name
     else:
          histoname = "h_"+reg+"_"+variable._name+"_"+cut_tag
     nbins = variable._nbins
     h1 = ROOT.TH1F(histoname, variable._name+"_"+reg, variable._nbins, variable._xmin, variable._xmax)
     h1.Sumw2()
     if 'muon' in lep: 
          cut  = variable._taglio+ '*isMu'
          if not 'Data' in sample.label:
               cut += '*passed_mu'
     elif 'electron' in lep:
          cut  = variable._taglio + '*isEle*passed_ele'
          if not 'Data' in sample.label:
               cut += '*passed_mu'
     print str(cut)
     foutput = "plot/"+lep+"/"+ sample.label +"_"+lep+".root"
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
     print treename
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

def makestack(lep_, reg_, variabile_, samples_, cut_tag_, syst_):
     histo = []
     tmp = ROOT.TH1F()
     h = ROOT.TH1F()
     hsig = ROOT.TH1F()
     h_err = ROOT.TH1F()
     h_bkg_err = ROOT.TH1F()
     err_up = []
     err_down =  []
     print "Variabile:", variabile_._name
     ROOT.gROOT.SetStyle('Plain')
     ROOT.gStyle.SetPalette(1)
     ROOT.gStyle.SetOptStat(0)
     ROOT.TH1.SetDefaultSumw2()
     if cut_tag_=="":
          histoname = "h_"+reg_+"_"+variabile_._name
          stackname = "stack_"+reg_+"_"+variabile_._name
          canvasname = "stack_"+reg_+"_"+variabile_._name+"_"+lep_
     else:
          histoname = "h_"+reg_+"_"+variabile_._name+"_"+cut_tag_
          stackname = "stack_"+reg_+"_"+variabile_._name+"_"+cut_tag_
          canvasname = "stack_"+reg_+"_"+variabile_._name+"_"+cut_tag_+"_"+lep_
     stack = ROOT.THStack(stackname, variabile_._name)
     leg_stack = ROOT.TLegend(0.45,0.66,0.94,0.88)
     signal = False
     infile = []
     print samples_
     for s in samples_:
          if(syst_==""):
               outfile="stack_"+str(lep_).strip('[]')+".root"
               infile.append(ROOT.TFile.Open("plot/"+lep+"/"+ s.label +"_"+lep+".root"))
          else:
               outfile="stack_"+syst_+"_"+str(lep_).strip('[]')+".root"
               infile.append(ROOT.TFile.Open("plot/"+lep+"/"+ s.label +"_"+lep+"_"+syst_+".root"))
     i=0
     for s in samples_:
          infile[i].cd()
          print "opening file: ", infile[i].GetName()
          tmp = (ROOT.TH1F)(infile[i].Get(histoname))
          tmp.SetLineColor(ROOT.kBlack)
          tmp.SetName(s.leglabel)
          if('Data' in s.label):
               hdata = ROOT.TH1F(tmp.Clone(""))
               hdata.SetMarkerStyle(20)
               hdata.SetMarkerSize(0.9)
               leg_stack.AddEntry(hdata, "Data", "lp")
          else:
               tmp.SetOption("HIST SAME")
               tmp.SetTitle("")
               tmp.SetFillColor(s.color)
               histo.append(tmp.Clone(""))
               stack.Add(tmp.Clone(""))
               #hratio.Add(tmp)
          i+=1
          tmp.Reset("ICES")
     for hist in reversed(histo):
          if not ('Data' in hist.GetName()):
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
     logscale = True # False #
     if(logscale):
          pad1.SetLogy()
          stack.SetMaximum(maximum*10000)
     else:
          stack.SetMaximum(maximum*1.6)
     stack.SetMinimum(0.01)
     stack.Draw("HIST")
     step = float(variabile_._xmax - variabile_._xmin)/float(variabile_._nbins)
     print str(step)
     if "GeV" in variabile_._title:
          if step.is_integer():
               ytitle = "Events/%.0f GeV" %step
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
          hsig.SetLineColor(ROOT.kBlue)
          hsig.SetLineWidth(3)
          
          hsig.SetMarkerSize(0.)
          hsig.SetMarkerColor(ROOT.kBlue)
          hsig.Scale(1000)
          hsig.Draw("same L")
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
          
     lumi_sqrtS = "35.9 fb^{-1}  (13 TeV)"
     
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
     c1.Print("stack/"+canvasname+".png")
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

dataset_dict = {'2016':[],'2017':[],'2018':[]}
if(opt.dat!= 'all'):
     if not(opt.dat in sample_dict.keys()):
          print sample_dict.keys()
     dataset_names = map(str, opt.dat.strip('[]').split(','))
     print dataset_names
     samples = []
     [samples.append(sample_dict[dataset_name]) for dataset_name in dataset_names]
     [dataset_dict[str(sample.year)].append(sample) for sample in samples]
else:
     dataset_dict = {'2016':[DataMu_2016, DataEle_2016, TT_Mtt_2016, WJets_2016],'2017':[DataMu_2017, DataEle_2017, TT_Mtt_2017, WJets_2017],'2018':[DataMu_2018, DataEle_2018, TT_Mtt_2018, WJets_2018]}
print(dataset_dict)

years = []
if(opt.year!='all'):
     years = map(str,opt.year.strip('[]').split(','))
else:
     years = ['2016','2017','2018']
print(years)

leptons = map(str,opt.lep.strip('[]').split(',')) 

cut = opt.cut #default cut must be obvious, for example DetReco_Lepton_m>0
if opt.cut == "DetReco_Lepton_m>0":
     cut_tag = ""
else:
     cut_tag = cutToTag(opt.cut)

lumi = {'2016': 35.89, "2017": 41.53, "2018": 57.3}

variables = []
wzero = 'w_nominal'
#variables.append(variabile('DetReco_Lepton_pt', 'lepton p_{T} [GeV]', wzero+'*('+cut+')', 200, 0, 1200))
variables.append(variabile('DetReco_Lepton_pt', 'lepton p_{T} [GeV]', wzero+'*('+cut+')', 100, 0, 1200))
variables.append(variabile('DetReco_Lepton_eta', 'lepton #eta', wzero+'*('+cut+')', 48, -2.4, 2.4))
variables.append(variabile('DetReco_Lepton_phi', 'lepton #phi',  wzero+'*('+cut+')',20,-3.2,3.2))
#variables.append(variabile('DetReco_Lepton_m', 'lepton mass [GeV]', wzero+'*('+cut+')', 75, 0.101, 0.110))
variables.append(variabile('MET_pt', "Missing transverse momentum [GeV]",wzero+'*('+cut+')', 100, 0, 1000))
variables.append(variabile('Event_HT', 'event HT', wzero+'*('+cut+')', 70, 0, 1400))
variables.append(variabile('MET_phi', 'Missing transverse momentum #phi',  wzero+'*('+cut+')',20,-3.2,3.2))

for year in years:
     for sample in dataset_dict[year]:
          if(opt.merpart):
               mergepart(sample)
          if(opt.lumi):
               lumi_writer(sample, lumi[year])
          if(opt.mertree):
               mergetree(sample)

for year in years:
     for lep in leptons:
          dataset_new = dataset_dict[year]
          if lep == 'muon' and sample_dict['DataEle_'+str(year)] in dataset_new:
               dataset_new.remove(sample_dict['DataEle_'+str(year)])
          elif lep == 'electron' and sample_dict['DataMu_'+str(year)] in dataset_new:
               dataset_new.remove(sample_dict['DataMu_'+str(year)])
          for sample in dataset_new:
               if(opt.plot):
                    for var in variables:
                         plot(lep, 'SR', var, sample, cut_tag, "")
          if(opt.stack):
               for var in variables:
                    makestack(lep, 'SR', var, dataset_new, cut_tag, "")
#if hasattr(dataset_dict[str(year)], 'components'): # How to check whether this exists or not
#     samples = [sample for sample in dataset.components]# Method exists and was used.
#else:
#     print "You are launching a single sample and not an entire bunch of samples"
#     samples.append(dataset)

#lumi_mu = {'2016': 36.47, '2017':  41.54,'2018':  59.96}
#lumi_ele = {'2016': 36.47, '2017':  36.75,'2018':  59.96}
