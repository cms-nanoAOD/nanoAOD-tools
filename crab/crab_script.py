#!/usr/bin/env python
import os
import sys
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis


# get options from the json
from PhysicsTools.NanoAODTools.python.postprocessing.framework.crabhelper import _crabGlobalOptions
jfile = open ('options.json', 'r')
opts=json.loads(jfile.readline())
for k,v in opts.iteritems():
    _crabGlobalOptions[k]=v
jfile.close()

from optparse import OptionParser
import imp 

parser = OptionParser(usage='%prog [options]')
parser.add_option('--cfg_file', type="string", dest='cfg_file', help='Config file containing PostProcessor instance')

(options, args) = parser.parse_args()


handle = open(options.cfg_file,'r')
cfo = imp.load_source(options.cfg_file.rstrip('py'), options.cfg_file, handle)
cfo.POSTPROCESSOR.run()


