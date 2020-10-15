import ROOT
'''
Class to hold the four-vectors of jets (and their groomed versions, if desired) with
kinematic systematic uncertainties applied such as the JEC, JER, JMS, JMR.
These four-vectors need to be updated very often so we want a small
helper structure to facilitate. Also keep a reference to the original object
to access the non-kinematic information.

This assumes that "jetmetUncertainties" has been run and uses that tree output structure.
'''


class JetSysColl:
    def __init__(self, jets, systs, sel=lambda x: True):
        self.jets_ = jets  # Hold a single copy of the original jet list
        # Hold many systematic variations, copy p4 and sd mass.
        self.coll_ = {}
        self.systs_ = systs
        self.add_systs(self.systs_, sel)

    def jets_raw(self):
        return self.jets_

    def __getitem__(self, syst):
        if syst in list(self.coll_.keys()):
            return self.coll_[syst]
        else:
            # If this systematic does not exist, use nominal
            return self.coll_[0]

    def __setitem__(self, syst, val):
        self.coll_[syst] = val

    def add_systs(self, systs, sel=lambda x: True):
        for syst in systs:
            self.coll_[syst] = {}
            for i, j in enumerate(self.jets_raw()):
                if sel(j):
                    self.coll_[syst][i] = JetSysObj(i, self.jets_raw())


class JetSysObj:
    def __init__(self, idx, jets):
        # Index in the original array for unmodified values
        self.idx = idx
        self.jets_ = jets
        # This is where the four-vector will change
        self.p4_ = jets[idx].p4()
        self.msd_ = 0.0  # This is where the groomed mass will change
        # Keep access to these for sorting + matching
        self.eta = jets[idx].eta
        self.phi = jets[idx].phi  # ^^

    def p4(self):
        return self.p4_

    def raw(self):
        return self.jets_[self.idx]

    def msd(self):
        return self.msd_

    def __lt__(self, other):
        return self.idx < other.idx

    def __le__(self, other):
        return self.idx <= other.idx

    def __gt__(self, other):
        return self.idx > other.idx

    def __ge__(self, other):
        return self.idx >= other.idx

    def __str__(self):
        s = ' (%6.2f,%4.2f,%4.2f,%6.2f : %6.2f)' % (self.p4_.Perp(
        ), self.p4_.Eta(), self.p4_.Phi(), self.p4_.M(), self.msd_)
        return s
