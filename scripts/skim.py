#!/usr/bin/env python

#####
##
## SCRIPT FOR BATCH SUBMISSION
##
####

import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from optparse import OptionParser
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

execfolder=os.environ["CMSSW_BASE"]

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] Nevents fileIN")

    parser.add_option("-e", "--Nevent",dest="Nevent", type="int", default=-1, help="Number of event for processing")
    parser.add_option("-c", "--cut",  dest="cut", type="string", default=None, help="Cut string")
    
    (options, args) = parser.parse_args()
    
    if len(args) < 1 :
        parser.print_help()
        sys.exit(1)

    Nevents=options.Nevent
    preselection=options.cut
    OutDir=args[0]
    Infiles=["%s"%args[1]]
    
    p=PostProcessor( OutDir , Infiles , cut=preselection , maxevent=Nevents )

    p.run()
