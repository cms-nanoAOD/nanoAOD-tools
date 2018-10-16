#!/usr/bin/env python
import os
import sys
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

### SKIM 
cut = ''

### SLIM FILE
slimfile = "SlimFile.txt"

from optparse import OptionParser
import imp 

parser = OptionParser(usage='%prog [options]')
parser.add_option('--cfg_file', type="string", dest='cfg_file', help='Config file containing PostProcessor instance')

(options, args) = parser.parse_args()


handle = open(options.cfg_file,'r')
print 'here1 '
cfo = imp.load_source(options.cfg_file.rstrip('py'), options.cfg_file, handle)
print 'here2'
cfo.POSTPROCESSOR.run()

print "DONE"
os.system("ls -lR")
