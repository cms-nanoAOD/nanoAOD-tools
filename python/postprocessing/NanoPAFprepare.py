#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from framework.postprocessor import PostProcessor

### INPUT FILE
filepath = ['/afs/cern.ch/work/j/jrgonzal/public/pruebaNanoAOD/8EAB6B64-9210-E811-B19D-FA163E759AE3.root']
#filepath = ['/nfs/fanae/user/juanr/nanoAOD/CMSSW_9_4_6/src/PhysicsTools/NanoAODTools/python/postprocessing/skimtree.root']

### OUTPUT
outdir = '.'

### SKIM 
cut = '(nElectron + nMuon) >= 2 && Jet_pt > 200' # nGenDressedLepton >= 2

### SLIM FILE
slimfile = "SlimFile.txt"

### MODULES
### Include modules to compute derivate quantities or calculate uncertainties
from modules.jme.jetmetUncertainties import *
from modules.common.puWeightProducer import *
from modules.skimNRecoLeps import *
mod = [puAutoWeight(), skimRecoLeps()] # countHistogramsProducer(), jetmetUncertainties2017All()

p=PostProcessor(outdir,filepath,cut,slimfile,mod,provenance=True,outputbranchsel=slimfile)
p.run()
