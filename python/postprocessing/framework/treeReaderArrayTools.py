import types
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

def InputTree(tree,entrylist=None):
    """add to the PyROOT wrapper of a TTree a TTreeReader and methods readBranch, arrayReader, valueReader""" 
    if hasattr(tree, '_ttreereader'): return tree # don't initialize twice
    tree.entry = -1
    tree._entrylist = entrylist
    tree._ttreereader = ROOT.TTreeReader(tree,tree._entrylist)
    tree._ttreereader.SetEntry(0)
    tree._ttrvs = {}
    tree._ttras = {}
    tree._leafTypes = {}
    tree._ttreereaderversion = 1
    tree.arrayReader = types.MethodType(getArrayReader, tree)
    tree.valueReader = types.MethodType(getValueReader, tree)
    tree.readBranch = types.MethodType(readBranch, tree)
    tree.gotoEntry = types.MethodType(_gotoEntry, tree)
    tree.readAllBranches = types.MethodType(_readAllBranches, tree)
    tree.entries = tree._ttreereader.GetEntries(False)
    tree._extrabranches={}
    return tree

def getArrayReader(tree, branchName, isClean=False):
    """Make a reader for branch branchName containing a variable-length value array. 
       If you are sure nobody has yet read from the tree, you can set isClean to True and save some overhead."""
    if branchName not in tree._ttras:
       if not tree.GetBranch(branchName): raise RuntimeError, "Can't find branch '%s'" % branchName
       leaf = tree.GetBranch(branchName).GetLeaf(branchName)
       if not leaf.GetLen() == 0: raise RuntimeError, "Branch %s is not a variable-length value array" % branchName
       typ = leaf.GetTypeName()
       tree._ttras[branchName] = _makeArrayReader(tree, typ, branchName, remakeAllFirst=not(isClean))
    return tree._ttras[branchName]

def getValueReader(tree, branchName, isClean=False):
    """Make a reader for branch branchName containing a single value. 
       If you are sure nobody has yet read from the tree, you can set isClean to True and save some overhead."""
    if branchName not in tree._ttrvs:
       if not tree.GetBranch(branchName): raise RuntimeError, "Can't find branch '%s'" % branchName
       leaf = tree.GetBranch(branchName).GetLeaf(branchName)
       if not leaf.GetLen() == 1: raise RuntimeError, "Branch %s is not a value" % branchName
       typ = leaf.GetTypeName()
       tree._ttrvs[branchName] = _makeValueReader(tree, typ, branchName, remakeAllFirst=not(isClean))
    return tree._ttrvs[branchName]

def clearExtraBranches(tree):
    tree._extrabranches = {}

def setExtraBranch(tree,name,val):
    tree._extrabranches[name] = val

def readBranch(tree, branchName):
    """Return the branch value if the branch is a value, and a TreeReaderArray if the branch is an array"""
    if branchName in tree._extrabranches:
        return tree._extrabranches[branchName]
    elif branchName in tree._ttras:
        return tree._ttras[branchName]
    elif branchName in tree._ttrvs: 
        ret = tree._ttrvs[branchName].Get()[0]
        return ord(ret) if type(ret)==str else ret
    else:
        branch = tree.GetBranch(branchName)
        if not branch: raise RuntimeError, "Unknown branch %s" % branchName
        leaf = branch.GetLeaf(branchName)
        typ = leaf.GetTypeName()
        if leaf.GetLen() == 1 and not bool(leaf.GetLeafCount()): 
            ret = _makeValueReader(tree, typ, branchName).Get()[0]
            return ord(ret) if type(ret)==str else ret
        else:
            return _makeArrayReader(tree, typ, branchName)
        

####### PRIVATE IMPLEMENTATION PART #######

def _makeArrayReader(tree, typ, nam, remakeAllFirst=True):
    if remakeAllFirst: _remakeAllReaders(tree) 
    ttra = ROOT.TTreeReaderArray(typ)(tree._ttreereader, nam)
    tree._leafTypes[nam] = typ
    tree._ttras[nam] = ttra;
    tree._ttreereader.SetEntry(tree.entry)
    return tree._ttras[nam]

def _makeValueReader(tree, typ, nam, remakeAllFirst=True):
    if remakeAllFirst: _remakeAllReaders(tree) 
    ttrv = ROOT.TTreeReaderValue(typ)(tree._ttreereader, nam)
    tree._leafTypes[nam] = typ
    tree._ttrvs[nam] = ttrv
    tree._ttreereader.SetEntry(tree.entry)
    return tree._ttrvs[nam]

def _remakeAllReaders(tree):
    _ttreereader = ROOT.TTreeReader(tree, getattr(tree, '_entrylist', None))
    _ttrvs = {}
    for k in tree._ttrvs.iterkeys():
        _ttrvs[k] = ROOT.TTreeReaderValue(tree._leafTypes[k])(_ttreereader,k)
    _ttras = {}
    for k in tree._ttras.iterkeys():
        _ttras[k] = ROOT.TTreeReaderArray(tree._leafTypes[k])(_ttreereader,k)
    tree._ttrvs = _ttrvs
    tree._ttras = _ttras
    tree._ttreereader = _ttreereader
    tree._ttreereaderversion += 1

def _readAllBranches(tree):
    tree.GetEntry(_currentTreeEntry(tree))

def _currentTreeEntry(tree):
    if tree._entrylist:
        return tree._entrylist.GetEntry(tree.entry)
    else:
        return tree.entry

def _gotoEntry(tree, entry):
    if tree.entry != entry:
        if (tree.entry == entry-1):
            tree._ttreereader.Next()
        else:
            tree._ttreereader.SetEntry(entry)
        tree.entry = entry

