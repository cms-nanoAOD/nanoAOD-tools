#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from  mhtProducer import *
p=PostProcessor(".",["../../../../NanoAOD/test/lzma.root"],"Jet_pt>150","keep_and_drop.txt",[mht()],provenance=True)
p.run()
