import ROOT
import os
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

def is_relevant_syst_for_shape_corr(flavor_btv, syst):
    """Returns true if a flavor/syst combination is relevant"""
    if flavor_btv == 0:
        return syst in [ "central",
                         "up_jes", "down_jes",
                         "up_lf", "down_lf",
                         "up_hfstats1", "down_hfstats1",
                         "up_hfstats2", "down_hfstats2" ]
    elif flavor_btv == 1:
        return syst in [ "central",
                         "up_cferr1", "down_cferr1",
                         "up_cferr2", "down_cferr2" ]
    elif flavor_btv == 2:
        return syst in [ "central",
                         "up_jes", "down_jes",
                         "up_hf", "down_hf",
                         "up_lfstats1", "down_lfstats1",
                         "up_lfstats2", "down_lfstats2" ]
    else:
        raise ValueError("ERROR: Undefined flavor = %i!!" % flavor_btv)
    return True

class btagSFProducer(Module):
    """Calculate btagging scale factors
        algo has to be either 'csvv2' or 'cmva'
    """
    def __init__(self, algo = 'csvv2', verbose = 1):

        self.algo = algo.lower()

        self.verbose = verbose

        # CV: Return value of BTagCalibrationReader::eval_auto_bounds() is zero
        #     in case no SF is defined for a given jet pT and eta in the btagSF.csv file !!
        #
        #     In the current version of the btagSF.csv files this is the case for jet pT < 30 GeV or abs(eta) > 2.4
        #
        self.max_abs_eta = 2.4
        self.min_pt = 30.
        self.max_pt = 670.

        # define measurement type for each flavor
        self.inputFilePath = os.environ['CMSSW_BASE'] + "/src/PhysicsTools/NanoAODTools/data/btagSF/"
        self.inputFileName = None
        self.measurement_types = None
        if self.algo == "csvv2":
            self.inputFileName = "btagSF_CSVv2_ichep2016.csv"
            print("Loading btagSF weights for CSV (v2) algorithm from file '%s'" % os.path.join(self.inputFilePath, self.inputFileName))
            self.measurement_types = {
                0 : "comb",  # b
                1 : "comb",  # c
                2 : "incl"   # light
            }
        elif self.algo == "cmva":
            self.inputFileName = "btagSF_cMVAv2_ichep2016.csv"
            print("Loading btagSF weights for cMVA algorithm from file '%s'" % os.path.join(self.inputFilePath, self.inputFileName))
            self.measurement_types = {
                0 : "ttbar", # b
                1 : "ttbar", # c
                2 : "incl"   # light
            }
        else:
            raise ValueError("ERROR: Invalid algorithm '%s'! Please choose either 'csvv2' or 'cmva'." % algo)

        # load libraries for accessing b-tag scale factors (SFs) from conditions database
        for library in [ "libCondFormatsBTauObjects", "libCondToolsBTau" ]:
            if library not in ROOT.gSystem.GetLibraries():
                print("Load Library '%s'" % library.replace("lib", ""))
                ROOT.gSystem.Load(library)

        # define systematic uncertainties
        self.systs = []
        self.systs.append("up")
        self.systs.append("down")
        self.central_and_systs = [ "central" ]
        self.central_and_systs.extend(self.systs)

        self.systs_shape_corr = []
        for syst in [ 'jes',
                      'lf', 'hf',
                      'hfstats1', 'hfstats2',
                      'lfstats1', 'lfstats2',
                      'cferr1', 'cferr2' ]:
            self.systs_shape_corr.append("up_%s" % syst)
            self.systs_shape_corr.append("down_%s" % syst)
        self.central_and_systs_shape_corr = [ "central" ]
        self.central_and_systs_shape_corr.extend(self.systs_shape_corr)

        self.branchNames_central_and_systs = {}
        for central_or_syst in self.central_and_systs:
            if central_or_syst == "central":
                self.branchNames_central_and_systs[central_or_syst] = "Jet_btagSF"
            else:
                self.branchNames_central_and_systs[central_or_syst] = "Jet_btagSF_%s" % central_or_syst

        self.branchNames_central_and_systs_shape_corr = {}
        for central_or_syst in self.central_and_systs_shape_corr:
            if central_or_syst == "central":
                self.branchNames_central_and_systs_shape_corr[central_or_syst] = "Jet_btagSF_shape"
            else:
                self.branchNames_central_and_systs_shape_corr[central_or_syst] = "Jet_btagSF_shape_%s" % central_or_syst

    def beginJob(self):
        # initialize BTagCalibrationReader
        # (cf. https://twiki.cern.ch/twiki/bin/viewauth/CMS/BTagCalibration )
        self.calibration = ROOT.BTagCalibration(self.algo, os.path.join(self.inputFilePath, self.inputFileName))
        self.readers = {}
        for wp in [ "L", "M", "T", "shape_corr" ]:
            wp_btv = { "l" : 0, "m" : 1, "t" : 2, "shape_corr" : 3 }.get(wp.lower(), None)
            syts = None
            if wp_btv in [ 0, 1, 2 ]:
                systs = self.systs
            else:
                systs = self.systs_shape_corr
            v_systs = getattr(ROOT, 'vector<string>')()
            for syst in systs:
                v_systs.push_back(syst)
            reader = ROOT.BTagCalibrationReader(wp_btv, 'central', v_systs)
            for flavor_btv in [ 0, 1, 2 ]:
                if wp == "shape_corr":
                    reader.load(self.calibration, flavor_btv, 'iterativefit')
                else:
                    reader.load(self.calibration, flavor_btv, self.measurement_types[flavor_btv])
            self.readers[wp_btv] = reader

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for central_or_syst in self.central_and_systs:
            self.out.branch(self.branchNames_central_and_systs[central_or_syst], "F", lenVar="nJet")
        for central_or_syst in self.central_and_systs_shape_corr:
            self.out.branch(self.branchNames_central_and_systs_shape_corr[central_or_syst], "F", lenVar="nJet")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def getSF(self, pt, eta, flavor, syst = 'central', wp = 'M', measurement_type = 'auto', shape_corr = False, discr = 0.):
        """Evaluate the SFs.
            Note the flavor convention: hadronFlavor is b = 5, c = 4, f = 0
            Convert them to the btagging group convention of 0 ,1, 2

            Same for working points: input is 'L', 'M', 'T'
            Convert to 0, 1, 2

            Automatically checks if values are in allowed range

            If unknown wp/syst/mtype/flavor, returns -1.0
        """

        ##if not (pt > self.min_pt and pt < self.max_pt and abs(eta) < self.max_abs_eta):
        ##    return 1.

        flavor_btv = None
        if abs(flavor) == 5:
            flavor_btv = 0
        elif abs(flavor) == 4:
            flavor_btv = 1
        elif abs(flavor) in [ 0, 1, 2, 3, 21 ]:
            flavor_btv = 2
        else:
            if self.verbose > 0:
                print("WARNING: Unknown flavor '%s', setting b-tagging SF to -1!" % repr(flavor))
            return -1.

        if shape_corr:
            wp = "shape_corr"
        wp_btv = { "l" : 0, "m" : 1, "t" : 2, "shape_corr" : 3 }.get(wp.lower(), None)
        if wp_btv == None or not wp_btv in self.readers.keys():
            if self.verbose > 0:
                print("WARNING: Unknown working point '%s', setting b-tagging SF to -1!" % wp)
            return -1.
        reader = self.readers[wp_btv]

        syst = syst.lower()

        # evaluate SF
        sf = None
        if shape_corr:
            if is_relevant_syst_for_shape_corr(flavor_btv, syst):
                sf = reader.eval_auto_bounds(syst, flavor_btv, eta, pt, discr)
            else:
                sf = reader.eval_auto_bounds('central', flavor_btv, eta, pt, discr)
        else:
            sf = reader.eval_auto_bounds(syst, flavor_btv, eta, pt)
        return sf

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = Collection(event, "Jet")

        discr = None
        if self.algo == "csvv2":
            discr = "btagDeepB"
        elif self.algo == "cmva":
            discr = "btagCMVA"
        else:
            raise ValueError("ERROR: Invalid algorithm '%s'! Please choose either 'csvv2' or 'cmva'." % self.algo)

        for central_or_syst in self.central_and_systs:
            scale_factors = []
            for idx, jet in enumerate(jets):
                sf = self.getSF(jet.pt, jet.eta, jet.partonFlavour, central_or_syst, 'M', 'auto', False, getattr(jet, discr))
                if self.verbose > 0 and sf < 0.01:
                    print("jet #%i: pT = %1.1f, eta = %1.1f, discr = %1.3f, flavor = %i" % (idx, jet.pt, jet.eta, getattr(jet, discr), jet.partonFlavour))
                scale_factors.append(sf)
            self.out.fillBranch(self.branchNames_central_and_systs[central_or_syst], scale_factors)
            #print(self.branchNames_central_and_systs[central_or_syst], scale_factors)
        for central_or_syst in self.central_and_systs_shape_corr:
            scale_factors = []
            for idx, jet in enumerate(jets):
                sf = self.getSF(jet.pt, jet.eta, jet.partonFlavour, central_or_syst, 'shape_corr', 'auto', True, getattr(jet, discr))
                if self.verbose > 0 and sf < 0.01:
                    print("jet #%i: pT = %1.1f, eta = %1.1f, discr = %1.3f, flavor = %i" % (idx, jet.pt, jet.eta, getattr(jet, discr), jet.partonFlavour))
                scale_factors.append(sf)
            self.out.fillBranch(self.branchNames_central_and_systs_shape_corr[central_or_syst], scale_factors)
            #print(self.branchNames_central_and_systs_shape_corr[central_or_syst], scale_factors)
        #print('-' * 120)

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

btagSF = lambda : btagSFProducer()

