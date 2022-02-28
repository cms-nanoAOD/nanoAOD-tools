import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import numpy as np

class bffBtagEffProducer(Module):
    def __init__(self, btagWP, btag_type="DeepCSV"):
        self.alljetSel = lambda j: ((j.pt > 20) & (abs(j.eta) < 2.4) & ((j.jetId >> 1) & 1) & ((j.puId & 1) | (j.pt>50)))
        self.isMC = True
        self.btagWP = btagWP
        def deepcsv(jet):
            return jet.btagDeepB > self.btagWP
        def deepflavour(jet):
            return jet.btagDeepFlavB > self.btagWP
           #set right filtering function
        if btag_type=="DeepCSV":
            self.select_btag = deepcsv
        elif btag_type=="DeepFlavour":
            self.select_btag = deepflavour
            
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        '''
        In case of data, the b-tagging scale factors are not produced. 
        Check whether they were produced and if not, drop them from jet selections
        '''
        if wrappedOutputTree.tree().GetListOfBranches().FindObject("Jet_btagSF"):
            self.isMC = True
        else: 
            self.isMC = False

        self.out = wrappedOutputTree
        self.Pass = ROOT.std.vector(ROOT.std.vector('int'))()
        self.Total= ROOT.std.vector(ROOT.std.vector('int'))()
        self.out._tree.Branch("PassBtag", self.Pass)
        self.out._tree.Branch("TotalBtag",self.Total)

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = sorted(filter(self.alljetSel, Collection(event, "Jet")), key=lambda x: x.pt)


        jetPt = [20.,30.,50.,70.,100.,140.,200.,300.,600.,1000.]
        self.Pass.clear()
        Dummy1 = ROOT.std.vector('int')()
        Dummy1.resize(10,0)
        self.Pass.resize(3,Dummy1)
        self.Total.clear()
        Dummy2 = ROOT.std.vector('int')()
        Dummy2.resize(10,0)
        self.Total.resize(3,Dummy2)

        if self.isMC:
            for j in jets:
                bin = 9
                for k in reversed(jetPt):
                    if j.pt>k:
                        break
                    bin-=1
                if bin>=0:
                  flavor = 2
                  if j.genJetIdx>=0:
                      if j.hadronFlavour==5:
                          flavor=0
                      elif j.hadronFlavour==4:
                          flavor=1
                  if self.select_btag(j): 
                      self.Pass[flavor][bin] += 1
                  self.Total[flavor][bin]+= 1
	else:
            pass
        self.out._tree.Fill()

        return True


# define modules using the syntax 'name = lambda: constructor'
# to avoid having them loaded when not needed

bffBtagEffModuleConstr2016 = lambda: bffBtagEffProducer(0.6321) #medium btagging DeepCSV wp RunIISummer16, 17Jul2018 rereco
bffBtagEffModuleConstr2017 = lambda: bffBtagEffProducer(0.4941) #medium btagging DeepCSV wp RunIIFall17, 17Nov2017 
bffBtagEffModuleConstr2018 = lambda: bffBtagEffProducer(0.4184) #medium btagging DeepCSV wp RunIIAutumn18, 17Sep2018

