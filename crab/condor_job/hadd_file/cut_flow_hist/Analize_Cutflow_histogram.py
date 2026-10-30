import ROOT
import sys
import argparse as arg
parser = arg.ArgumentParser(description='inputs discription')
parser.add_argument('-f', '--file', dest='inputfile', type=str, nargs=1, help="Cutflow.root")
args = parser.parse_args()

#if len(sys.argv) != 2:
 #       print "USAGE: %s <inputfile name>"%(sys.argv [0])
  #      sys.exit (1)

input_ROOTfile=args.inputfile[0]
infile=ROOT.TFile.Open(input_ROOTfile,"READ")
#f = open("demofile2.txt", "a")

Hist = infile.Get("histograms/Nocut_npvs")
Entries = Hist.GetEntries()
#print Hist.GetName() ,"  \t\tEntries =", Entries ," Integral =",Hist.Integral()
print Hist.Integral()

Hist = infile.Get("histograms/trig_sel_npvs")
Entries = Hist.GetEntries()
#print Hist.GetName() ,"  \tEntries =", Entries ," Integral =",Hist.Integral()
print Hist.Integral()

Hist = infile.Get("histograms/tight_lep_sel_npvs")
Entries = Hist.GetEntries()
#print Hist.GetName() ,"  \tEntries =", Entries ," Integral =",Hist.Integral()
print Hist.Integral()

Hist = infile.Get("histograms/losse_lep_veto_npvs")
Entries = Hist.GetEntries()
#print Hist.GetName() ,"  \tEntries =", Entries ," Integral =",Hist.Integral()
print Hist.Integral()

Hist = infile.Get("histograms/sec_lep_veto_npvs")
Entries = Hist.GetEntries()
#print Hist.GetName() ,"  \tEntries =", Entries ," Integral =",Hist.Integral()
print Hist.Integral()

Hist = infile.Get("histograms/jet_sel_npvs")
Entries = Hist.GetEntries()
#print Hist.GetName() ,"  \t\tEntries =", Entries ," Integral =",Hist.Integral()
print Hist.Integral()

Hist = infile.Get("histograms/b_tag_jet_sel_npvs")
Entries = Hist.GetEntries()
#print Hist.GetName() ,"  \tEntries =", Entries ," Integral =",Hist.Integral()
print Hist.Integral()
