import os, commands
import optparse
import math
from ROOT import *

usage = 'python nevents.py'
parser = optparse.OptionParser(usage)
parser.add_option('-f', '--folder', dest='folder', type='string', default = 'v6', help='Default folder is v0')
#parser.add_option('-L', '--lep', dest='lep', type='string', default='muon', help='Default checks integrals of muon systematics')
(opt, args) = parser.parse_args()

folder = opt.folder
pathin = '/eos/user/a/adeiorio/Wprime/nosynch/' + folder + '/plot/'
#pathout = opt.pathout

gStyle.SetPalette(1)
gStyle.SetOptStat(0)
gROOT.SetBatch()        # don't pop up canvases

leptons = {
     "muon":["h_jets_lepton_pt"],
     "electron":["h_jets_lepton_pt"]
}

integrals = []
errors = []

samples = {
     'DataMu_2016':'DataMuon', 'DataEle_2016':'DataElectron', 'DataHT_2016':'DataHT', 'ST_2016':'Single top', 'QCD_2016':'QCD', 'TT_Mtt_2016':'\\ttbar', 'WJets_2016':'\\wjets', 'WP_M2000W20_RH_2016':'\\PWpr 2\\tev(1\%)', 'WP_M3000W30_RH_2016':'\\PWpr 3\\tev(1\%)', 'WP_M4000W40_RH_2016':'\\PWpr 4\\tev(1\%)', 'WP_M4000W400_RH_2016':'\\PWpr 4\\tev(10\%)'
     }

def getSumError(_list):
     return math.sqrt(reduce(lambda x, y: x + y, list(map(lambda x: x**2, _list))))

def getSumSquared(_list):
     return reduce(lambda x, y: x + y, list(map(lambda x: x**2, _list)))

def getSignificance(_list):
     sign = []
     total = getSumSquared(_list)
     for el in _list:
          sign.append(100*(el**2/total))
#          print el, total 
     return sign

tex = True # False #
signif = False # True #
e = 0
for lep in leptons.keys():
     p = ""
     for hist in leptons[lep]:
          if lep == "muon" and hist == "h_2j1t_BDT_ST_vs_All_mtw_G_50": 
               region = "muon_2j1t"
          elif lep == "muon" and hist == "h_3j1t_BDT_STsd_vs_All_sr_3j1t_mtw_G_50_AND_etajprime_G_2p5": 
               region = "muon_3j1t_forward"
          elif lep == "muon" and hist == "h_3j2t_BDT_ST_vs_TT_3j2t":
               region = "muon_3j2t"
          elif lep == "electron" and hist == "h_2j1t_BDT_ST_vs_All_mtw_G_50": 
               region = "electron_2j1t"
          elif lep == "electron" and hist == "h_3j1t_BDT_STsd_vs_All_sr_3j1t_mtw_G_50_AND_etajprime_G_2p5": 
               region = "electron_3j1t_forward"
          elif lep == "electron" and hist == "h_3j2t_BDT_ST_vs_TT_3j2t":
               region = "electron_3j2t"
          if(signif):
               infile = TFile.Open(pathin+"/Data_"+lep+".root")
               tmp = (TH1F)(infile.Get(hist))
               for i in range(1,tmp.GetNbinsX()+1):
                    errors_bin = []
                    total_bin = 0
                    st_bin = 0
                    for s, sname in samples.iteritems():
                         error = Double(0)
                         infile = TFile.Open(pathin+"/"+s+"_"+lep+".root")
                         tmp = (TH1F)(infile.Get(hist))
                         errors_bin.append(tmp.GetBinError(i))
                         total_bin += tmp.GetBinContent(i)
                         if s == "ST_tch":
                              st_bin = tmp.GetBinContent(i)
                    #print "Relative uncertainty %-20s %-8s, bin %-2i" %(hist, lep, i)
                    b = 100*st_bin/total_bin
                    if(b>100): 
                         p += " mcstat_"+region+"_ST_tch_bin"+str(i)
                    for s, el in zip(samples.keys(), errors_bin):
                         sign = 100*el/total_bin
                         if(sign>2 and s!="ST_tch_sd"): # and s!="DDQCD" and s!="ST_sch" and s!="VV" and s=="WJets"
                              e+=1
                              #print "%-10s %-4.2f %8s %2i %-0.2f " %(s, el, region, i, sign)
                              p += " mcstat_"+region+"_"+s+"_bin"+str(i)
               #print e
          if(tex):
               print "**********************************************"
               print "\\begin{table}[]"
               print "\\begin{center}"
               print "\\caption{\label{tab:%s_%s} }" %(hist,lep)
               print "\\begin{tabular}{l|c}"
               print "Process  & Integral $\pm$  Uncertainty \\\\ " 
               print "\\hline"
               integrals = []
               errors = []
               integrals_data = []
               errors_data = []
               for s, sname in samples.iteritems():
                    if((lep == 'muon' and 'DataEle' in s) or (lep == 'electron' and 'DataMu' in s)):
                         continue
                    error = Double(0)
                    infile = TFile.Open(pathin + "/" + lep + "/" + s + "_" + lep + ".root")
                    tmp = (TH1F)(infile.Get(hist))
                    if not 'Data' in s:
                         integrals.append(tmp.IntegralAndError(1,tmp.GetNbinsX()+1, error))
                         errors.append(error)
                         if(tex):
                              print "%-10s  & %-6i $\pm$  %-3i \\\\ " %(sname,integrals[-1],errors[-1])
                         tmp.Reset("ICES")
                    else:
                         integrals_data.append(tmp.IntegralAndError(1,tmp.GetNbinsX()+1, error))
                         errors_data.append(error)

          if(tex):
               print "\\hline"
               print "Total MC  & %-6i $\pm$  %-3i \\\\ " %(sum(integrals),getSumError(errors))
               print "\\hline"
               print "Data  & %-6i $\pm$  %-3i \\\\ " %(sum(integrals_data),getSumError(errors_data))
               print "\\end{tabular}"
               print "\\end{center}"
               print "\\end{table}"

     if(signif):
          print p

