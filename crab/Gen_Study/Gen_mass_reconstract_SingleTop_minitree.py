#!/usr/bin/env python3
import os, sys
import ROOT 
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from Gen_mass_functions import *
class NanoGenModule_minitree(Module):
    def __init__(self,datayear):
        self.writeHistFile=True
        self.datayear = datayear
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        return True

NanoGenConstr_UL2016_minitree = lambda : NanoGenModule_minitree('UL2016')
