from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
import os
import optparse
import sys

usage = 'python submit_condor.py -d dataset_name'
parser = optparse.OptionParser(usage)
parser.add_option('-d', '--dat', dest='dat', type=str, default = '', help='Please enter a dataset name')
(opt, args) = parser.parse_args()

def sub_writer(sample, n, files):
    f = open("condor.sub", "w")
    f.write("Proxy_filename          = x509up_103214\n")
    f.write("Proxy_path              = /tmp/$(Proxy_filename)\n")

    f.write("should_transfer_files   = YES\n")
    f.write("when_to_transfer_output = ON_EXIT\n")
    f.write("transfer_input_files    = $(Proxy_path)\n")
    f.write("transfer_output_remaps  = \""+ sample.label + "_part" + str(n) + ".root=/eos/user/"+str(os.environ.get('USER')[0])+"/"+str(os.environ.get('USER'))+"/Wprime/nosynch/" + sample.label +"/"+ sample.label + "_part" + str(n) + ".root\"\n")

    f.write("executable              = tree_skimmer.py\n")
    f.write("arguments               = $(Proxy_path) " + sample.label + " " + str(n) + " " + str(files) + "\n")
    #f.write("input                   = input.txt\n")

    f.write("output                  = condor/output/"+ sample.label + "_part" + str(n) + ".out\n")
    f.write("error                   = condor/error/"+ sample.label + "_part" + str(n) + ".err\n")
    f.write("log                     = condor/log/"+ sample.label + "_part" + str(n) + ".log\n")

    f.write("queue\n")

if not(opt.dat in sample_dict.keys()):
    print sample_dict.keys()
dataset = sample_dict[opt.dat]
samples = []

if hasattr(dataset, 'components'): # How to check whether this exists or not
    samples = [sample for sample in dataset.components]# Method exists and was used.
else:
    print "You are launching a single sample and not an entire bunch of samples"
    samples.append(dataset)

if not os.path.exists("condor/output"):
    os.makedirs("condor/output")
if not os.path.exists("condor/error"):
    os.makedirs("condor/error")
if not os.path.exists("condor/log"):
    os.makedirs("condor/log")

split = 50
#Writing the configuration file                                                                                                                                                                                                     
for sample in samples:
    isMC = True
    if('Data' in sample.label):
        isMC = False
    if not os.path.exists("/eos/user/"+str(os.environ.get('USER')[0]) + "/"+str(os.environ.get('USER'))+"/Wprime/nosynch/" + sample.label):
        os.makedirs("/eos/user/"+str(os.environ.get('USER')[0]) + "/"+str(os.environ.get('USER'))+"/Wprime/nosynch/" + sample.label)
    f = open("../../crab/macros/files/" + sample.label + ".txt", "r")
    files_list = f.read().splitlines()
    print(str(len(files_list)))
    if(isMC):
        for i, files in enumerate(files_list):
            sub_writer(sample, i, files)
            #os.popen('condor_submit condor.sub')
            print('condor_submit condor.sub')
            #os.popen("python tree_skimmer.py  /tmp/x509up_103214 " + str(sample) + " " + str(i) + " " + str(files) + "/")
            print("python tree_skimmer.py  /tmp/x509up_103214 " + sample.label + " " + str(i) + " " + str(files))
    else:
        for i in range(len(files_list)/split+1):
            sub_writer(sample, i,  ",".join( e for e in files_list[split*i:split*(i+1)]))
            #os.popen('condor_submit condor.sub')
            #os.popen("python tree_skimmer.py /tmp/x509up_103214 " + str(sample) + " " + str(i) + " " + ",".join( e for e in files_list[split*i:split*(i+1)]))
            print("python tree_skimmer.py /tmp/x509up_103214 " + sample.label + " " + str(i) + " " + ",".join( e for e in files_list[split*i:split*(i+1)]))
            #print("***************************************************")
            #print(i, str( files_list[split*i:split*(i+1)]))
            #print(str(len( files_list[split*i:split*(i+1)]))) 
            #print("***************************************************\n")
