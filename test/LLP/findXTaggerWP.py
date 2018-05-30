import os
import sys
import math
import ROOT
import random
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module



        
class JetPerformance(Module):
    def __init__(self):
        pass
        
    def deltaPhi(self,phi1,phi2):
        res = phi1-phi2
        while (res>math.pi):
            res -= 2*math.pi
        while (res<=-math.pi):
            res += 2*math.pi
        return res 
        
    def deltaR(self,j1,j2):
        return math.sqrt(
            (j1.eta-j2.eta)**2+\
            self.deltaPhi(j1.phi,j2.phi)**2
        )
        
    def beginJob(self):
        self.trueLLP = []
        self.fakeLLP = []
        
        
    def endJob(self):
        sortedFakes = sorted(self.fakeLLP)
        sortedTrue = sorted(self.trueLLP)
        for rej in [10,50,100,500,1000,5000,10000]:
            print "wp: ",rej
            index = int(round((1.-1./rej)*(len(sortedFakes)-1)))
            print "\tindex: ",index,"/",len(sortedFakes)
            if index == len(sortedFakes):
                print "\tnot enough jets processed - got only ",len(sortedFakes)
            else:
                print "\ttagger value: ",sortedFakes[index]
                for i in reversed(range(len(sortedTrue))):
                    if sortedTrue[i]<sortedFakes[index]:
                        print "\tsignal efficiency: ",1.-1.*i/(len(sortedTrue)-1)
                        break
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        if inputFile.GetName().find("SMS-T1qqqq_ctau")>=0:
            self.blockFake = True
        else:
            self.blockFake = False
        print inputFile.GetName(),self.blockFake
        
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = Collection(event, "Jet")
        jettags = Collection(event, "llpdnnx")
        jetorigin = Collection(event, "jetorigin")

        for ijet,jet in enumerate(jets):
            if jet.jetId>0 and jet.pt>30. and math.fabs(jet.eta)<2.4:
                
                #put tag info into jets         
                if ijet<len(jettags) and ijet<len(jetorigin) and jettags[ijet].isLLP>=0.:
                    
                    if jetorigin[ijet].fromLLP>0.5:
                    #if jetorigin[ijet].isB>0.5 or jetorigin[ijet].isBB>0.5 or jetorigin[ijet].isGBB>0.5 or jetorigin[ijet].isLeptonic_B>0.5 or jetorigin[ijet].isLeptonic_C>0.5:
                        self.trueLLP.append(jettags[ijet].isLLP)
                        #self.trueLLP.append(jettags[ijet].isB)
                    elif jetorigin[ijet].isUD>0.5 or jetorigin[ijet].isS>0.5 or jetorigin[ijet].isG>0.5:
                        if not self.blockFake:
                            self.fakeLLP.append(jettags[ijet].isLLP)
                            #self.fakeLLP.append(jettags[ijet].isB)

        return False
        

files=[
    [
    "root://gfe02.grid.hep.ph.ic.ac.uk/pnfs/hep.ph.ic.ac.uk/data/cms/store/user/mkomm/LLP/NANOX_180425-v2/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8-evtgen/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8-evtgen/NANOX_180425-v2/180425_183639/0000/nano_20.root",
    "/vols/cms/mkomm/LLP/NANOX_180425-v2_eval/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8-evtgen/nano_20.root.friend",
    ],
    [
    "root://gfe02.grid.hep.ph.ic.ac.uk/pnfs/hep.ph.ic.ac.uk/data/cms/store/user/mkomm/LLP/NANOX_180425-v2/SMS-T1qqqq_ctau-1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/SMS-T1qqqq_ctau-1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOX_180425-v2/180425_183459/0000/nano_6.root",
    "/vols/cms/mkomm/LLP/NANOX_180425-v2_eval/SMS-T1qqqq_ctau-1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/nano_6.root.friend",
    ],
    [
    "root://gfe02.grid.hep.ph.ic.ac.uk/pnfs/hep.ph.ic.ac.uk/data/cms/store/user/mkomm/LLP/NANOX_180425-v2/SMS-T1qqqq_ctau-1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/SMS-T1qqqq_ctau-1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOX_180425-v2/180425_183459/0000/nano_7.root",
    "/vols/cms/mkomm/LLP/NANOX_180425-v2_eval/SMS-T1qqqq_ctau-1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/nano_7.root.friend",
    ]
]

'''
files=[
    [
    "root://gfe02.grid.hep.ph.ic.ac.uk/pnfs/hep.ph.ic.ac.uk/data/cms/store/user/mkomm/LLP/NANOX_180425-v2/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8-evtgen/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8-evtgen/NANOX_180425-v2/180425_183639/0000/nano_20.root",
    "/vols/cms/mkomm/LLP/NANOX_180425-v2_eval/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8-evtgen/nano_20.root.friend",
    ]
]
'''
'''
files = [
    [
        "root://gfe02.grid.hep.ph.ic.ac.uk/pnfs/hep.ph.ic.ac.uk/data/cms/store/user/mkomm/LLP/NANOX_180425-v2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOX_180425-v2/180425_182750/0000/nano_100.root",
        "/vols/cms/mkomm/LLP/NANOX_180425-v2_eval/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/nano_100.root.friend",
    ]
]
'''
p=PostProcessor(".",files,cut=None,branchsel=None,modules=[
    JetPerformance(),
],friend=False,noOut=True)
p.run()
