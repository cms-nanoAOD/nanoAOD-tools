import ROOT
import numpy as np
import os,sys
import math
import random
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


def mk_safe(fct, *args):
    try:
        return fct(*args)
    except Exception as e:
        if any('Error in function boost::math::erf_inv' in arg for arg in e.args):
            print('WARNING: catching exception and returning -1. Exception arguments: %s' % e.args)
            return -1.
        else:
            raise e

def top_pt_sf(pt):
    return 0.103 * math.exp(-0.0118 * pt) - 0.000134 * pt + 0.973


class gen_info(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("top_Ngenpart","F")
        self.out.branch("top_mass","F")
        self.out.branch("atop_Ngenpart","F")
        self.out.branch("atop_mass","F")
        self.out.branch("top_pt","F")
        self.out.branch("atop_pt","F")
        self.out.branch("top_pt_SF","F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        # Get the desired arrays from the data
        Genparts = Collection(event,"GenPart")
        Ngenpart_counter = -1
        ptop_Ngenpart,patop_Ngenpart = -1,-1
        top_mass,atop_mass = -99,-99
        top_pt           = -99
        atop_pt          = -99
        for genpart in Genparts:
            Ngenpart_counter += 1
            if (genpart.pdgId == 6 and ((genpart.statusFlags >> 13) & 0x1) > 0):
                    ptop_Ngenpart = Ngenpart_counter
                    top_mass = genpart.mass
                    top_pt        = genpart.pt
            if (genpart.pdgId == -6 and ((genpart.statusFlags >> 13) & 0x1) > 0):
                    patop_Ngenpart = Ngenpart_counter
                    atop_mass = genpart.mass
                    atop_pt        = genpart.pt

        if top_pt > 0 and atop_pt > 0:
            sf_t          = top_pt_sf(top_pt)
            sf_tbar       = top_pt_sf(atop_pt)
            top_pt_SF = math.sqrt(sf_t * sf_tbar)
        else:
            top_pt_SF = 1.0 

        self.out.fillBranch("top_Ngenpart",ptop_Ngenpart)
        self.out.fillBranch("atop_Ngenpart",patop_Ngenpart)
        self.out.fillBranch("top_mass",top_mass)
        self.out.fillBranch("atop_mass",atop_mass)
        self.out.fillBranch("top_pt",top_pt)
        self.out.fillBranch("atop_pt",atop_pt)
        self.out.fillBranch("top_pt_SF", top_pt_SF)

        return True

gen_info_Module = lambda : gen_info()    
