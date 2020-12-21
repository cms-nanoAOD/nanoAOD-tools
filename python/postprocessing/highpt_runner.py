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

for sample in samples:
    f = open("../../crab/macros/files/" + sample.label + "_highpt.txt", "r")
    files_list = f.read().splitlines()
    print(str(len(files_list)))
    print("hadd $EOSSPACE/Wprime/nosynch/highpt/" + sample.label + ".root " + " ".join(e for e in files_list))
    os.popen("hadd -f /eos/user/a/adeiorio/Wprime/nosynch/highpt/" + sample.label + ".root " + " ".join(e for e in files_list) + " &")
          
