import ROOT

class CollectionSkimmer:
    def __init__(self, outName, srcColl, maxSize=100, saveSelectedIndices=False, padSelectedIndicesWith=None, saveTagForAll=False):
        """Read from a collection called srcColl (eg. 'Jet'), write out to a collection called outName (e.g. 'CleanJet')
           Clone the variables specified in the ints and floats list (e.g. 'mcMatchId', 'pt', ...)
           maxSize fixes the maximum allowed number of entries in the output."""
        self._maxSize = maxSize
        self._ints   = []
        self._uchars = []
        self._floats = []
        self._bools  = []
        self._srcColl = srcColl
        self._saveSelectedIndices = saveSelectedIndices
        self._padSelectedIndicesWith = padSelectedIndicesWith
        self._saveTagForAll = saveTagForAll
        self._impl = ROOT.CollectionSkimmer(outName,srcColl,saveSelectedIndices,saveTagForAll)
        self._iprefix = srcColl + "_"
        self._ttreereaderversion = -1
    def initInputTree(self,tree):
        """To be called to initialize the input tree. 
           initEvent also takes care of re-calling it if needed"""
        if len(self._ints)+len(self._floats)+len(self._uchars) +len(self._bools) == 0: # dump all branches
            _brlist = tree.GetListOfBranches()
            branches = [_brlist.At(i) for i in xrange(_brlist.GetEntries())]
           
            for br in branches:
                name = br.GetName()
                typ  = br.FindLeaf(br.GetName()).GetTypeName()
                if not name.startswith(self._srcColl+'_'): continue
                if typ not in ['Int_t','Float_t','UChar_t','Bool_t']:
                    raise RuntimeError("Unsupported type %s for branch %s"%(typ,name))
                if   typ == 'Int_t'  : self._ints  .append( name.replace(self._srcColl+'_',''))
                elif typ == 'Float_t': self._floats.append( name.replace(self._srcColl+'_',''))
                elif typ == 'UChar_t': self._uchars.append( name.replace(self._srcColl+'_',''))
                elif typ == 'Bool_t' : self._bools .append( name.replace(self._srcColl+'_',''))
        
        for i in self._ints:   self._impl.copyInt(i, tree.arrayReader(self._iprefix+i))
        for f in self._floats: self._impl.copyFloat(f, tree.arrayReader(self._iprefix+f))
        for u in self._uchars: self._impl.copyUChar(u, tree.arrayReader(self._iprefix+u))
        for b in self._bools:  self._impl.copyBool (b, tree.arrayReader(self._iprefix+b))
        if self._saveTagForAll: self._impl.srcCount(tree.valueReader('n'+self._iprefix[:-1]))
        self._ttreereaderversion = tree._ttreereaderversion

    def initOutputTree(self,outpytree):
        """To be called once when defining the output PyTree, to declare the branches"""
        self._impl.makeBranches(outpytree._tree, self._maxSize, (self._padSelectedIndicesWith!=None), self._padSelectedIndicesWith if (self._padSelectedIndicesWith!=None) else -1)
    def initEvent(self,event):
        """To be called at the beginning of every event.
           Returns true if the underlying TTreeReader has changed"""
        if self._ttreereaderversion != event._tree._ttreereaderversion:
            self.initInputTree(event._tree)
            self._impl.clear()
            return True
        else:
            self._impl.clear()
            return False
    def cppImpl(self):
        """Get the C++ CollectionSkimmer instance, to pass to possible C++ worker code"""
        return self._impl
    def clear(self): 
        """Clear the list of output objects (note: initEvent does it already)"""
        self._impl.clear()
    def push_back(self,iSrc): 
        """Select one object (if passing an int) or many objects (if passing std::vector<int>) for output"""
        self._impl.push_back(iSrc)
    def push_back_all(self,iSrcList): 
        """Select a python list of objects for output"""
        for iSrc in iSrcList:
            self._impl.push_back(iSrc)
    def resize(self,newSize): 
        """Fix the size of the output collection (to be called before with copy() or [] for out-of-order filling)"""
        self._impl.reSize(newSize)
    def copy(self,iSrc,iTo):
        """Copy input object of index iSrc into output iTo (you must have called resize with a suitable size before)"""
        self._impl.copy(iSrc,iTo)
    def __setitem__(self,iTo,iSrc):
        """Set output at the specified index iTo to be a copy of the input at iSrc (note that the order is reversed wrt copy())"""
        self._impl.copy(iSrc,iTo)
    def size(self):
        """Return the number of selected items in this event"""
        return self._impl.size()
    def __len__(self):
        """Return the number of selected items in this event"""
        return self._impl.size()
