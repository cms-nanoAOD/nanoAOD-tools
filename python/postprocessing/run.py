#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.branchselection import BranchSelection 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import InputTree 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import eventLoop 
from PhysicsTools.NanoAODTools.postprocessing.framework.output import FriendOutput, FullOutput 
from PhysicsTools.NanoAODTools.postprocessing.framework.preskimming import preSkim

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] outputDir inputFiles")
    parser.add_option("-s", "--postfix",dest="postfix", type="string", default=None, help="Postfix which will be appended to the file name (default: _Friend for friends, _Skim for skims)")
    parser.add_option("-J", "--json",  dest="json", type="string", default=None, help="Select events using this JSON file")
    parser.add_option("-c", "--cut",  dest="cut", type="string", default=None, help="Cut string")
    parser.add_option("-b", "--branch-selection",  dest="branchsel", type="string", default=None, help="Branch selection")
    parser.add_option("--friend",  dest="friend", action="store_true", default=False, help="Produce friend trees in output (current default is to produce full trees)")
    parser.add_option("--full",  dest="friend", action="store_false",  default=False, help="Produce full trees in output (this is the current default)")
    parser.add_option("--noout",  dest="noOut", action="store_true",  default=False, help="Do not produce output, just run modules")
    parser.add_option("--justcount",   dest="justcount", default=False, action="store_true",  help="Just report the number of selected events") 
    parser.add_option("-I", "--import", dest="imports",  type="string", default=[], action="append", nargs=2, help="Import modules (python package, comma-separated list of ");
    parser.add_option("-z", "--compression",  dest="compression", type="string", default=("LZMA:9"), help="Compression: none, or (algo):(level) ")

    (options, args) = parser.parse_args()

    if options.friend:
        if options.cut or options.json: raise RuntimeError("Can't apply JSON or cut selection when producing friends")

    if not options.noOut:
        outdir = args[0]; args = args[1:]
        outpostfix = options.postfix if options.postfix != None else ("_Friend" if options.friend else "_Skim")
        branchsel = BranchSelection(options.branchsel) if options.branchsel else None
        if options.compression != "none":
            ROOT.gInterpreter.ProcessLine("#include <Compression.h>")
            (algo, level) = options.compression.split(":")
            compressionLevel = int(level)
            if   algo == "LZMA": compressionAlgo  = ROOT.ROOT.kLZMA
            elif algo == "ZLIB": compressionAlgo  = ROOT.ROOT.kZLIB
            else: raise RuntimeError("Unsupported compression %s" % algo)
        else:
            compressionLevel = 0 

    if not options.noOut:
        print "Will write selected trees to "+outdir
        if not options.justcount:
            if not os.path.exists(outdir):
                os.system("mkdir -p "+outdir)

    modules = []
    for mod, names in options.imports: 
        import_module(mod)
        obj = sys.modules[mod]
        selnames = names.split(",")
        for name in dir(obj):
            if name[0] == "_": continue
            if name in selnames:
                print "Loading %s from %s " % (name, mod)
                modules.append(getattr(obj,name)())
    if options.noOut:
        if len(modules) == 0: 
            raise RuntimeError("Running with --noout and no modules does nothing!")

    for m in modules: m.beginJob()

    fullClone = (len(modules) == 0)

    for fname in args:
        # open input file
        inFile = ROOT.TFile.Open(fname)

        #get input tree
        inTree = inFile.Get("Events")

        # pre-skimming
        elist = preSkim(inTree, options.json, options.cut)
        if options.justcount:
            print 'Would select %d entries from %s'%(elist.GetN() if elist else inTree.GetEntries(), fname)
            continue

        if fullClone:
            # no need of a reader (no event loop), but set up the elist if available
            if elist: inTree.SetEntryList(elist)
        else:
            # initialize reader
            inTree = InputTree(inTree, elist) 

        # prepare output file
        outFileName = os.path.join(outdir, os.path.basename(fname).replace(".root",outpostfix+".root"))
        outFile = ROOT.TFile.Open(outFileName, "RECREATE", "", compressionLevel)
        if compressionLevel: outFile.SetCompressionAlgorithm(compressionAlgo)

        # prepare output tree
        if options.friend:
            outTree = FriendOutput(inFile, inTree, outFile)
        else:
            # FIXME process the other TTrees if there is a JSON
            outTree = FullOutput(inFile, inTree, outFile, branchSelection = branchsel, fullClone = fullClone)

        # process events, if needed
        if not fullClone:
            (nall, npass, time) = eventLoop(modules, inFile, outFile, inTree, outTree)
            print 'Processed %d entries from %s, selected %d entries' % (nall, fname, npass)
        else:
            print 'Selected %d entries from %s' % (outTree.tree().GetEntries(), fname)

        # now write the output
        outTree.write()
        outFile.Close()
        print "Done %s" % outFileName

    for m in modules: m.endJob()
