import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class mhtProducer(Module):
    def __init__(self, jetSelection, muonSelection, electronSelection):
        self.jetSel = jetSelection
        self.muSel = muonSelection
        self.elSel = electronSelection
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("MHT_pt",  "F");
        self.out.branch("MHT_phi", "F");
        self.out.branch("Jet_mhtCleaning", "b", lenVar="nJet")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        njets = len(jets)
        mht = ROOT.TLorentzVector()
        for lep in filter(self.muSel,muons):
            mht += lep.p4()
        for lep in filter(self.elSel,electrons):
            mht += lep.p4()
        goodjet = [ 0 for i in xrange(njets) ]
        for i,j in enumerate(jets):
            if not self.jetSel(j): continue
            if j.muonIdx1 != -1 and j.muonIdx1 < njets:
                if self.muSel(muons[j.muonIdx1]): continue # prefer the muon
            if j.muonIdx2 != -1 and j.muonIdx2 < njets:
                if self.muSel(muons[j.muonIdx2]): continue # prefer the muon
            if j.electronIdx1 != -1 and j.electronIdx1 < njets:
                if self.elSel(electrons[j.electronIdx1]): continue # prefer the electron
            if j.electronIdx2 != -1 and j.electronIdx2 < njets:
                if self.elSel(electrons[j.electronIdx2]): continue # prefer the electron
            goodjet[i] = 1
            mht += j.p4()
        self.out.fillBranch("MHT_pt", mht.Pt())
        self.out.fillBranch("MHT_phi", -mht.Phi()) # note the minus
        self.out.fillBranch("Jet_mhtCleaning", goodjet)
        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

mht = lambda : mhtProducer( lambda j : j.pt > 40, 
                            lambda mu : mu.pt > 20 and mu.miniPFRelIso_all < 0.2,
                            lambda el : el.pt > 20 and el.miniPFRelIso_all < 0.2 ) 
 
