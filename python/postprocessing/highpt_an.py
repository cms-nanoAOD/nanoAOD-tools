import ROOT
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
import os
import optparse
import sys

usage = 'python submit_condor.py -d dataset_name -f destination_folder'
parser = optparse.OptionParser(usage)
parser.add_option('-d', '--dat', dest='dat', type=str, default = '', help='Please enter a dataset name')
#parser.add_option('-u', '--user', dest='us', type='string', default = 'ade', help="")
(opt, args) = parser.parse_args()
#Insert here your uid... you can see it typing echo $uid

if not(opt.dat in sample_dict.keys()):
    print sample_dict.keys()
dataset = sample_dict[opt.dat]
samples = []

if hasattr(dataset, 'components'): # How to check whether this exists or not
    samples = [sample for sample in dataset.components]# Method exists and was used.
else:
    print "You are launching a single sample and not an entire bunch of samples"
    samples.append(dataset)

print("sample, isTight, isHighPt, isMCTight, isMCHighPt")
for sample in samples:
    infile = ROOT.TFile.Open("/eos/user/a/adeiorio/Wprime/nosynch/highpt/" + sample.label + ".root")
    tree = infile.Get("Events")
    print(sample.label, tree.GetEntries("isTight"), tree.GetEntries("isHighPt"), tree.GetEntries("isMCTight"), tree.GetEntries("isMCHighPt"))
