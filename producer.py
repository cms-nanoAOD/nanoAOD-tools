#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from optparse import OptionParser
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.analysis.Producer import producer


if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] Nevents fileIN")

    parser.add_option("-e", "--Nevent",dest="Nevent", type="int", default=-1, help="Number of event for processing")
    
    (options, args) = parser.parse_args()

    if len(args) < 1 :
        parser.print_help()
        sys.exit(1)

    preselection=""
    bIn="keep_and_drop_Input.txt"
    bOut="keep_and_drop_Output.txt"
    print "options.Nevent = ", options.Nevent
    Nevents=options.Nevent
    files=args
    #files=[
    #    "/Users/shoh/Projects/CMS/PhD/Analysis/SSL/NANOAOD/HWminusJ_HToWW_M125_13TeV_powheg_pythia8-v1.root",
    #    "/Users/shoh/Projects/CMS/PhD/Analysis/SSL/NANOAOD/HWplusJ_HToWW_M125_13TeV_powheg_pythia8-v1.root",
    #]
    
    p=PostProcessor(
        "."\
        ,files\
        ,cut=preselection\
        ,branchsel=bIn\
        ,modules=[producer()]
        ,maxevent=Nevents
        ,outputbranchsel=bOut
    )
    
    p.run()
