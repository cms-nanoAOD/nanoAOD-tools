import ROOT
import numpy as np
import os,sys
import math
import random
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

def Check_rediation(Genparts,genpart_ori,ID_ori):
    radiation = False
    dauther_id = 999
    for ID,genpart in enumerate(Genparts):
        if(genpart.genPartIdxMother == ID_ori and genpart_ori.pdgId==genpart.pdgId):
            radiation = True
            dauther_id = ID
    return radiation, dauther_id
def mk_safe(fct, *args):
    try:
        return fct(*args)
    except Exception as e:
        if any('Error in function boost::math::erf_inv' in arg for arg in e.args):
            print('WARNING: catching exception and returning -1. Exception arguments: %s' % e.args)
            return -1.
        else:
            raise e


class NanoGenModule(Module):
    def __init__(self,datayear):
        self.writeHistFile=True
        self.datayear = datayear
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("top_ID_lastcopy","I")
        self.out.branch("atop_ID_lastcopy","I")

        self.out.branch("top_mass_gen_lastcopy", "F")
        self.out.branch("atop_mass_gen_lastcopy", "F")


        self.out.branch("top_pt_gen_lastcopy", "F")
        self.out.branch("atop_pt_gen_lastcopy", "F")

        self.out.branch("top_eta_gen_lastcopy", "F")
        self.out.branch("atop_eta_gen_lastcopy", "F")

        self.out.branch("top_phi_gen_lastcopy", "F")
        self.out.branch("atop_phi_gen_lastcopy", "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    ##Def of rapidity
    

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        # Get the desired arrays from the data
        #print(getattr(event,'event'))
        Genparts = Collection(event,"GenPart")
        genpartID = -1
        for genpart in Genparts:
            genpartID = genpartID+1
            if genpart.pdgId == 6:
                if (((genpart.statusFlags >> 13) & 0x1) > 0): # is last copy
                    self.out.fillBranch("top_mass_gen_lastcopy", genpart.mass)
                    self.out.fillBranch("top_pt_gen_lastcopy", genpart.pt)
                    self.out.fillBranch("top_eta_gen_lastcopy", genpart.eta)
                    self.out.fillBranch("top_ID_lastcopy", genpartID)
                    self.out.fillBranch("top_phi_gen_lastcopy", genpart.phi)
                   
            if genpart.pdgId == -6:
                if (((genpart.statusFlags >> 13) & 0x1) > 0):
                    self.out.fillBranch("atop_mass_gen_lastcopy", genpart.mass)
                    self.out.fillBranch("atop_pt_gen_lastcopy", genpart.pt)
                    self.out.fillBranch("atop_eta_gen_lastcopy", genpart.eta)
                    self.out.fillBranch("atop_ID_lastcopy", genpartID)
                    self.out.fillBranch("atop_phi_gen_lastcopy", genpart.phi)

        return True

NanoGenConstr_UL2016_Alt_mass_ttbar = lambda : NanoGenModule('UL2016')
