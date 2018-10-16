#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from framework.postprocessor import PostProcessor

### INPUT FILE
filepath = ['5E621211-8B42-E811-9903-001E67F8FA2E.root']


### OUTPUT
outdir = '.'

### SKIM 

### SLIM FILE
slimfile = "SlimFile.txt"

### MODULES
### Include modules to compute derivate quantities or calculate uncertainties
from modules.jme.jetmetUncertainties import *
from modules.common.puWeightProducer import *
from modules.EdgeZ.skimNRecoLeps import *

mod = [puAutoWeight(), skimRecoLeps()] 

p=PostProcessor(outdir,filepath,'',slimfile,mod,provenance=True,outputbranchsel=slimfile)
p.run()
