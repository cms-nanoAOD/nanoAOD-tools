import json
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

class JSONFileFilter:
    def __init__(self,fname):
        self.keep = {}
        for _run,lumis in json.load(open(fname, 'r')).iteritems():
            run = long(_run)
            if run not in self.keep: self.keep[run] = []
            self.keep[run] += lumis
        for run in self.keep.keys():
            if len(self.keep[run])==0: del self.keep[run]
    def filterRunLumi(self,run,lumi):
        try:
            for (l1,l2) in self.keep[run]:
                if l1 <= lumi and lumi <= l2: return True
            return False
        except KeyError:
            return False
    def filterRunOnly(self,run):
        return (run in self.keep)
    def runCut(self):
        return "%d <= run && run <= %s" % (min(self.keep.iterkeys()), max(self.keep.iterkeys()))
    def filterEList(self, tree, elist):
        #FIXME this can be optimized for sure
        tree.SetBranchStatus("*", 0)
        tree.SetBranchStatus('run',1)
        tree.SetBranchStatus('luminosityBlock',1)
        filteredList = ROOT.TEntryList('filteredList','filteredList')
        if elist:
            for i in xrange(elist.GetN()):
                entry = elist.GetEntry(0) if i == 0 else elist.Next()
                tree.GetEntry(entry)
                if self.filterRunLumi(tree.run, tree.luminosityBlock):
                    filteredList.Enter(entry)
        else:
            for entry in xrange(tree.GetEntries()):
                tree.GetEntry(entry)
                if self.filterRunLumi(tree.run, tree.luminosityBlock):
                    filteredList.Enter(entry)
        tree.SetBranchStatus("*", 1)
        return filteredList
                

def preSkim(tree, jsonFile = None, cutstring = None):
    if jsonFile == None and cutstring == None: 
        return None,None
    cut = None
    jsonFilter = None
    if jsonFile != None:
        jsonFilter = JSONFileFilter(jsonFile)
        cut = jsonFilter.runCut()
    if cutstring != None: 
        cut = "(%s) && (%s)" % (cutstring, cut) if cut else cutstring
    tree.Draw('>>elist',cut,"entrylist")
    elist = ROOT.gDirectory.Get('elist')
    if jsonFile:
        elist = jsonFilter.filterEList(tree,elist)
    return elist,jsonFilter
