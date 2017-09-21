import ROOT
import numpy as np
import itertools
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
_rootLeafType2rootBranchType = { 'UChar_t':'b', 'Char_t':'B', 'UInt_t':'i', 'Int_t':'I', 'Float_t':'F', 'Double_t':'D', 'ULong64_t':'l', 'Long64_t':'L', 'Bool_t':'O' }

class collectionMerger(Module):

    def __init__(self,input,output,sortkey = lambda x : x.pt,reverse=True,selector=None,maxObjects=None):
        self.input = input
        self.output = output
        self.nInputs = len(self.input)
        self.sortkey = lambda (obj,j,i) : sortkey(obj)
        self.reverse = reverse
        self.selector = [(selector[coll] if coll in selector else (lambda x: True)) for coll in self.input] if selector else None # pass dict([(collection_name,lambda obj : selection(obj)])
        self.maxObjects = maxObjects # save only the first maxObjects objects passing the selection in the merged collection
        self.branchType = {}
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        _brlist = inputTree.GetListOfBranches()
        branches = [_brlist.At(i) for i in xrange(_brlist.GetEntries())]
        self.brlist_sep = [self.filterBranchNames(branches,x) for x in self.input]
        self.brlist_all = set(itertools.chain(*(self.brlist_sep)))

        self.is_there = np.zeros(shape=(len(self.brlist_all),self.nInputs),dtype=bool)
        for bridx,br in enumerate(self.brlist_all):
            for j in xrange(self.nInputs):
                if br in self.brlist_sep[j]: self.is_there[bridx][j]=True

        self.out = wrappedOutputTree
        for br in self.brlist_all:
            self.out.branch("%s_%s"%(self.output,br), _rootLeafType2rootBranchType[self.branchType[br]], lenVar="n%s"%self.output)

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def filterBranchNames(self,branches,collection):
        out = []
        for br in branches:
            name = br.GetName()
            if not name.startswith(collection+'_'): continue
            out.append(name.replace(collection+'_',''))
            self.branchType[out[-1]] = br.FindLeaf(br.GetName()).GetTypeName()
        return out

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        coll = [Collection(event,x) for x in self.input]
        objects = [(coll[j][i],j,i) for j in xrange(self.nInputs) for i in xrange(len(coll[j]))]
        if self.selector: objects=filter(lambda (obj,j,i) : self.selector[j](obj), objects)
        objects.sort(key = self.sortkey, reverse = self.reverse)
        if self.maxObjects: objects = objects[:self.maxObjects]
        for bridx,br in enumerate(self.brlist_all):
            out = []
            for obj,j,i in objects:
                out.append(getattr(obj,br) if self.is_there[bridx][j] else 0)
            self.out.fillBranch("%s_%s"%(self.output,br), out)
        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

lepMerger = lambda : collectionMerger(input=["Electron","Muon"],output="Lepton")
lepMerger_exampleSelection = lambda : collectionMerger(input=["Electron","Muon"],output="Lepton", # this will keep only the two leading leptons among electrons with pt > 20 and muons with pt > 40
                                                       maxObjects=2,
                                                       selector=dict([("Electron",lambda x : x.pt>20),("Muon",lambda x : x.pt>40)]),
                                                       )
