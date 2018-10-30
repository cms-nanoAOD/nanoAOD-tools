import ROOT 

from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class TriggerBitFilter(Module):
    def __init__(self, triggers=[], vetotriggers=[]):
        self.triggers = triggers
        self.vetotriggers = vetotriggers


    def beginJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        # if no triggers are required, vetos are also not applied 
        if len(self.triggers) == 0: return True
        
        passesTrigger = False; passesVeto = True

        for trig in self.triggers:
            if not hasattr(event, trig):
                raise RuntimeError('[%s] Event does not have flag for %s'%(__name__,trig))
            
            if getattr(event,trig): passesTrigger = True

        if not passesTrigger: return False

        for trig in self.vetotriggers:
            if not hasattr(event, trig):
                raise RuntimeError('[%s] Event does not have flag for %s'%(__name__,trig))
            
            if getattr(event,trig): return False

        return True
        

triggerBitFilter = lambda x :  TriggerBitFilter()
