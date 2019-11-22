import os
import sys
import math
import json
import ROOT
import random

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from utils import deltaR

class JetTruthFlags(Module):

    def __init__(
        self,
        inputCollection = lambda event: Collection(event, "Jet"),
        outputName = "centralJets",
        flags={
            'isB':['isB','isBB','isGBB','isLeptonic_B','isLeptonic_C'],
            'isC':['isC','isCC','isGCC'],
            'isUDS':['isS','isUD'],
            'isG':['isG'],
            'isLLP':['fromLLP'],
            'isPU':['isPU']
        },
        globalOptions={"isData":False}
    ):
        self.globalOptions = globalOptions
        self.flags = flags
        self.inputCollection = inputCollection
        self.outputName = outputName
 
    def beginJob(self):
        pass
        
    def endJob(self):
        pass
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        '''
        if not self.globalOptions['isData']:
            self.out.branch(self.outputName+"_nsv","I",lenVar="n"+self.outputName)
            self.out.branch(self.outputName+"_svxysig","F",lenVar="n"+self.outputName)
            for k in sorted(self.flags.keys()):
                self.out.branch(self.outputName+"_"+k,"F",lenVar="n"+self.outputName)
        '''
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        if self.globalOptions['isData']:
            return True
            
        jets = self.inputCollection(event)
        jetOrigin = Collection(event,"jetorigin")
        jetNSV = Collection(event,"svlength")
        jetSV = Collection(event,"sv")
        jetGlobal = Collection(event,"global")
        
        flavors = {}
        
        nsv = [0]*len(jets)
        svxysig = [-2.]*len(jets)
        
        for k in sorted(self.flags.keys()):
            flavors[k] = [-1.]*len(jets)
            self.out.branch(self.outputName+"_"+k,"F",lenVar="n"+self.outputName)

        for ijet,jet in enumerate(jets):
            if jet._index<len(jetGlobal) and jet._index<len(jetOrigin):
                if math.fabs(jet.eta-jetGlobal[jet._index].eta)>0.01:
                    print "Warning - no proper match between jetorigin and nanoaod jets"    
                    #print jet.pt,jet.eta,jetGlobal[jet._index].pt,jetGlobal[jet._index].eta
                    for k in sorted(self.flags.keys()):
                        setattr(jet,k,False)
                    continue
                else:
                    nsv[ijet] = int(round(jetNSV[jet._index].length))
                    offset = 0
                    for i in range(jet._index):
                        offset+=int(round(jetNSV[i].length))
                    for isv in range(offset,offset+int(round(jetNSV[jet._index].length))):
                        svxysig[ijet] = max(svxysig[ijet],jetSV[isv].dxysig)
                    for k in sorted(self.flags.keys()):
                        flavorFlag = 0.
                        for originFlag in self.flags[k]:
                            flagValue = getattr(jetOrigin[jet._index],originFlag)
                            if (flagValue>0.5):
                                flavorFlag = 1.
                                break
                        flavors[k][ijet]=flavorFlag
                        setattr(jet,k,flavorFlag>0.5)
        '''
        self.out.fillBranch(self.outputName+"_nsv",nsv)
        self.out.fillBranch(self.outputName+"_svxysig",svxysig)
        '''
                        
        for k in sorted(self.flags.keys()):
            self.out.fillBranch(self.outputName+"_"+k,flavors[k])
        return True
        
