#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from optparse import OptionParser
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.analysis.Producer import producer

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

    bIn="%s/src/PhysicsTools/NanoAODTools/scripts/keep_and_drop_Input.txt" %execfolder
    bOut="%s/src/PhysicsTools/NanoAODTools/scripts/keep_and_drop_Output.txt" %execfolder
    Nevents=options.Nevent
    preselection=options.cut
    OutDir=args[0]
    Infiles=["%s"%args[1]]
    
    #files=[
    #    "/Users/shoh/Projects/CMS/PhD/Analysis/SSL/NANOAOD/HWminusJ_HToWW_M125_13TeV_powheg_pythia8-v1.root",
    #    "/Users/shoh/Projects/CMS/PhD/Analysis/SSL/NANOAOD/HWplusJ_HToWW_M125_13TeV_powheg_pythia8-v1.root",
    #]
    
    p=PostProcessor( OutDir , Infiles , cut=preselection , branchsel=bIn , modules=[producer()] , maxevent=Nevents , outputbranchsel=bOut )
    
    p.run()
