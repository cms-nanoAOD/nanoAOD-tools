import ROOT
import numpy as np
import re, itertools
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
_rootLeafType2rootBranchType = { 'UChar_t':'b', 'Char_t':'B', 'UInt_t':'i', 'Int_t':'I', 'Float_t':'F', 'Double_t':'D', 'ULong64_t':'l', 'Long64_t':'L', 'Bool_t':'O' }

class collectionMerger(Module):

    def __init__(self,input,output,sortkey = lambda x : x.pt):
        self.input = input
        self.output = output
        self.nInputs = len(self.input)
        self.sortkey = lambda (obj,j,i) : sortkey(obj)
        self.branchType = {}
        self.nullValue = []
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

        self.nullValue = [ 0.0 if self.branchType[br] in ['Float_t','Double_t'] else 0 for br in self.brlist_all]

        self.out = wrappedOutputTree
        for br in self.brlist_all:
            self.out.branch("%s_%s"%(self.output,br), _rootLeafType2rootBranchType[self.branchType[br]], lenVar="n%s"%self.output)

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def filterBranchNames(self,branches,collection):
        out = []
        for br in branches:
            name = br.GetName()
            if not re.match(collection+'_.*',name): continue
            out.append(name.replace(collection+'_',''))
            self.branchType[out[-1]] = br.FindLeaf(br.GetName()).GetTypeName()
        return out

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        coll = [Collection(event,x) for x in self.input]
        objects = sorted([(coll[j][i],j,i) for j in xrange(self.nInputs) for i in xrange(len(coll[j]))], key = self.sortkey)
        for bridx,br in enumerate(self.brlist_all):
            out = []
            nullvalue = self.nullValue[bridx]
            for obj,j,i in objects:
                val = getattr(obj,br) if self.is_there[bridx][j] else nullvalue
                if type(val)==str: val = ord(val)
                out.append(val)
            self.out.fillBranch("%s_%s"%(self.output,br), out)
        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

lepMerger = lambda : collectionMerger(input=["Electron","Muon"],output="Lepton")

