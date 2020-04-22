from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
import os
import optparse
import sys

usage = 'python submit_crab.py'
parser = optparse.OptionParser(usage)
parser.add_option('-d', '--dat', dest='dat', type=str, default = '', help='Please enter a dataset name')
parser.add_option('--status', dest = 'status', default = False, action = 'store_true', help = 'Default do not check the status')
parser.add_option('-s', '--sub', dest = 'sub', default = False, action = 'store_true', help = 'Default do not submit')
parser.add_option('-k', '--kill', dest = 'kill', default = False, action = 'store_true', help = 'Default do not kill')
parser.add_option('-r', '--resub', dest = 'resub', default = False, action = 'store_true', help = 'Default do not resubmit')
parser.add_option('-g', '--gout', dest = 'gout', default = False, action = 'store_true', help = 'Default do not do getoutput')
(opt, args) = parser.parse_args()

def sub_writer(sample):
    f = open("condor.sub", "w")
    f.write("Proxy_filename          = x509up\n")
    f.write("Proxy_path              = /afs/cern.ch/user/"+str(os.environ.get('USER')[0])+"/"+str(os.environ.get('USER'))+"/private/$(Proxy_filename)\n")
    f.write("arguments               = $(Proxy_path) dataset\n")

    f.write("should_transfer_files   = YES\n")
    f.write("when_to_transfer_output = ON_EXIT\n")
    #f.write("transfer_output_files   = ""\n") #This command only transfer back files to the submitting directory. Alll the output files will anyway be present in the 'output' directory
    f.write("transfer_input_files    = $(Proxy_path),input2.txt,input3.txt\n")
    
    f.write("executable              = python skim_tree.py\n")
    f.write("input                   = input.txt\n")
    f.write("output                  = /eos/user/"+str(os.environ.get('USER')[0])+"/"+str(os.environ.get('USER'))+"/Wprime/nosynch/" + sample.label +"/out.$(ClusterId).$(ProcId)\n")
    f.write("error                   = /eos/user/"+str(os.environ.get('USER')[0])+"/"+str(os.environ.get('USER'))+"/Wprime/nosynch/" + sample.label +"/err.$(ClusterId).$(ProcId)\n")
    f.write("log                     = /eos/user/"+str(os.environ.get('USER')[0])+"/"+str(os.environ.get('USER'))+"/Wprime/nosynch/" + sample.label +"/log.$(ClusterId).$(ProcId)\n")
    f.write("queue 100\n")




dataset = sample_dict[opt.dat]
samples = []

if hasattr(dataset, 'components'): # How to check whether this exists or not
    samples = [sample for sample in dataset.components]# Method exists and was used.
else:
    print "You are launching a single sample and not an entire bunch of samples"
    samples.append(dataset)

#Writing the configuration file                                                                                                                                                                                                     
for sample in samples:
    if not os.path.exists("/eos/user/"+str(os.environ.get('USER')[0]) + "/"+str(os.environ.get('USER'))+"/Wprime/nosynch/" + sample.label):
        os.makedirs("/eos/user/"+str(os.environ.get('USER')[0]) + "/"+str(os.environ.get('USER'))+"/Wprime/nosynch/" + sample.label)
    sub_writer(sample)
    os.system('condor_submit condor.sub')
