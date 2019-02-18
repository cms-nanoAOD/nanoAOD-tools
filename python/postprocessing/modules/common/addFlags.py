import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


class AddFlags(Module):
      def __init__(self, flags):
            self.flags = flags
            
      def beginJob(self):
            pass
      def endJob(self):
            pass
      def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
            self.out = wrappedOutputTree
            for flag in self.flags:
                  self.out.branch(*flag[0])

      def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
            pass

      def analyze(self, event):
            for flag in self.flags:
                  self.out.fillBranch( flag[0][0], flag[1](event))
            return True


