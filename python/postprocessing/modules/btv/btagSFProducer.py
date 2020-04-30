import ROOT
import os
from itertools import chain

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

def is_relevant_syst_for_shape_corr(flavor_btv, syst, jesSystsForShape=["jes"]):
    """Returns true if a flavor/syst combination is relevant"""
    jesSysts = list(chain(*[ ("up_" + j, "down_" + j) for j in jesSystsForShape ]))

    if flavor_btv == 0:
        return syst in [ "central",
                         "up_lf", "down_lf",
                         "up_hfstats1", "down_hfstats1",
                         "up_hfstats2", "down_hfstats2" ] + jesSysts
    elif flavor_btv == 1:
        return syst in [ "central",
                         "up_cferr1", "down_cferr1",
                         "up_cferr2", "down_cferr2" ]
    elif flavor_btv == 2:
        return syst in [ "central",
                         "up_hf", "down_hf",
                         "up_lfstats1", "down_lfstats1",
                         "up_lfstats2", "down_lfstats2" ] + jesSysts
    else:
        raise ValueError("ERROR: Undefined flavor = %i!!" % flavor_btv)
    return True

class btagSFProducer(Module):
    """Calculate btagging scale factors
    """
    def __init__(self, era, algo='csvv2', selectedWPs=['M', 'shape_corr'], sfFileName=None, verbose=0, jesSystsForShape=["jes"]):

        self.era = era
        self.algo = algo.lower()
        self.selectedWPs = selectedWPs
        self.verbose = verbose
        self.jesSystsForShape = jesSystsForShape

        # CV: Return value of BTagCalibrationReader::eval_auto_bounds() is zero
        #     in case jet abs(eta) > 2.4 !!
        self.max_abs_eta = 2.4

        # define measurement type for each flavor
        self.inputFilePath = os.environ['CMSSW_BASE'] + "/src/PhysicsTools/NanoAODTools/data/btagSF/"
        self.inputFileName = sfFileName
        self.measurement_types = None
        self.supported_wp = None
        supported_btagSF = {
            'csvv2' : {
                '2016' : {
                    'inputFileName' : "btagSF_CSVv2_ichep2016.csv",
                    'measurement_types' : {
                        0 : "comb",  # b
                        1 : "comb",  # c
                        2 : "incl"   # light
                    },
                    'supported_wp' : [ "L", "M", "T", "shape_corr" ]
                },
                '2017' : {
                    'inputFileName' : "CSVv2_94XSF_V2_B_F.csv",
                    'measurement_types' : {
                        0 : "comb",  # b
                        1 : "comb",  # c
                        2 : "incl"   # light
                    },
                    'supported_wp' : [ "L", "M", "T", "shape_corr"]
                }
            },
            'deepcsv' : {
                'Legacy2016' : {
                    'inputFileName' : "DeepCSV_2016LegacySF_V1.csv",
                    'measurement_types' : {
                        0 : "comb",  # b
                        1 : "comb",  # c
                        2 : "incl"   # light
                    },
                    'supported_wp' : [ "L", "M", "T", "shape_corr"]
                },
                '2017' : {
                    'inputFileName' : "DeepCSV_94XSF_V4_B_F.csv",
                    'measurement_types' : {
                        0 : "comb",  # b
                        1 : "comb",  # c
                        2 : "incl"   # light
                    },
                    'supported_wp' : [ "L", "M", "T", "shape_corr"]
                },
                '2018' : {
                    'inputFileName' : "DeepCSV_102XSF_V1.csv",
                    'measurement_types' : {
                        0 : "comb",  # b
                        1 : "comb",  # c
                        2 : "incl"   # light
                    },
                    'supported_wp' : [ "L", "M", "T", "shape_corr"]
                }
            },
            'deepjet' : {
                'Legacy2016' : {
                    'inputFileName' : "DeepJet_2016LegacySF_V1.csv",
                    'measurement_types' : {
                        0 : "comb",  # b
                        1 : "comb",  # c
                        2 : "incl"   # light
                    },
                    'supported_wp' : [ "L", "M", "T", "shape_corr"]
                },
                '2017' : {
                    'inputFileName' : "DeepFlavour_94XSF_V3_B_F.csv",
                    'measurement_types' : {
                        0 : "comb",  # b
                        1 : "comb",  # c
                        2 : "incl"   # light
                    },
                    'supported_wp' : [ "L", "M", "T", "shape_corr"]
                },
                '2018' : {
                    'inputFileName' : "DeepJet_102XSF_V1.csv",
                    'measurement_types' : {
                        0 : "comb",  # b
                        1 : "comb",  # c
                        2 : "incl"   # light
                    },
                    'supported_wp' : [ "L", "M", "T", "shape_corr"]
                }
            },
            'cmva' : {
                '2016' : {
                    'inputFileName' : "btagSF_cMVAv2_ichep2016.csv",
                    'measurement_types' : {
                        0 : "ttbar", # b
                        1 : "ttbar", # c
                        2 : "incl"   # light
                    },
                    'supported_wp' : [ "L", "M", "T", "shape_corr" ]
                }
            }
        }

        supported_algos = []
        for algo in supported_btagSF.keys():
            if self.era in supported_btagSF[algo].keys():
                supported_algos.append(algo)
        if self.algo in supported_btagSF.keys():
            if self.era in supported_btagSF[self.algo].keys():
                if self.inputFileName is None:
                    self.inputFileName = supported_btagSF[self.algo][self.era]['inputFileName']
                self.measurement_types = supported_btagSF[self.algo][self.era]['measurement_types']
                self.supported_wp = supported_btagSF[self.algo][self.era]['supported_wp']
            else:
                raise ValueError("ERROR: Algorithm '%s' not supported for era = '%s'! Please choose among { %s }." % (self.algo, self.era, supported_algos))
        else:
            raise ValueError("ERROR: Algorithm '%s' not supported for era = '%s'! Please choose among { %s }." % (self.algo, self.era, supported_algos))
        for wp in self.selectedWPs:
            if wp not in self.supported_wp:
                raise ValueError("ERROR: Working point '%s' not supported for algo = '%s' and era = '%s'! Please choose among { %s }." % (wp, self.algo, self.era, self.supported_wp))

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
        for syst in [ 'lf', 'hf',
                      'hfstats1', 'hfstats2',
                      'lfstats1', 'lfstats2',
                      'cferr1', 'cferr2' ] + self.jesSystsForShape:
            self.systs_shape_corr.append("up_%s" % syst)
            self.systs_shape_corr.append("down_%s" % syst)
        self.central_and_systs_shape_corr = [ "central" ]
        self.central_and_systs_shape_corr.extend(self.systs_shape_corr)

        self.branchNames_central_and_systs = {}
        for wp in self.selectedWPs:
            branchNames = {}
            if wp == 'shape_corr':
                central_and_systs = self.central_and_systs_shape_corr
                baseBranchName = 'Jet_btagSF_{}_shape'.format(self.algo)
            else:
                central_and_systs = self.central_and_systs
                baseBranchName = 'Jet_btagSF_{}_{}'.format(self.algo, wp)
            for central_or_syst in central_and_systs:
                if central_or_syst == "central":
                    branchNames[central_or_syst] = baseBranchName
                else:
                    branchNames[central_or_syst] = baseBranchName + '_' + central_or_syst
            self.branchNames_central_and_systs[wp] = branchNames

    def beginJob(self):
        # initialize BTagCalibrationReader
        # (cf. https://twiki.cern.ch/twiki/bin/viewauth/CMS/BTagCalibration )
        self.calibration = ROOT.BTagCalibration(self.algo, os.path.join(self.inputFilePath, self.inputFileName))
        self.readers = {}
        for wp in self.selectedWPs:
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
        for central_or_syst in self.branchNames_central_and_systs.values():
            for branch in central_or_syst.values():
                self.out.branch(branch, "F", lenVar="nJet")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def getReader(self, wp):
        """
            Get btag scale factor reader.
            Convert working points: input is 'L', 'M', 'T', 'shape_corr' to 0, 1, 2, 3
        """
        wp_btv = { "l" : 0, "m" : 1, "t" : 2, "shape_corr" : 3 }.get(wp.lower(), None)
        if wp_btv == None or not wp_btv in self.readers.keys():
            if self.verbose > 0:
                print("WARNING: Unknown working point '%s', setting b-tagging SF reader to None!" % wp)
            return None
        return self.readers[wp_btv]

    def getFlavorBTV(self, flavor):
        '''
            Maps hadronFlavor to BTV flavor:
            Note the flavor convention: hadronFlavor is b = 5, c = 4, f = 0
            Convert them to the btagging group convention of 0, 1, 2
        '''
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
        return flavor_btv

    def getSFs(self, jet_data, syst, reader,  measurement_type = 'auto', shape_corr = False):
        if reader is None:
            if self.verbose > 0:
                print("WARNING: Reader not available, setting b-tagging SF to -1!")
            for i in range(len(jet_data)):
                yield 1
            raise StopIteration
        for idx, (pt, eta, flavor_btv, discr) in enumerate(jet_data):
            epsilon = 1.e-3
            max_abs_eta = self.max_abs_eta
            if eta <= -max_abs_eta:
                eta = -max_abs_eta + epsilon
            if eta >= +max_abs_eta:
                eta = +max_abs_eta - epsilon
            # evaluate SF
            sf = None
            if shape_corr:
                if is_relevant_syst_for_shape_corr(flavor_btv, syst, self.jesSystsForShape):
                    sf = reader.eval_auto_bounds(syst, flavor_btv, eta, pt, discr)
                else:
                    sf = reader.eval_auto_bounds('central', flavor_btv, eta, pt, discr)
            else:
                sf = reader.eval_auto_bounds(syst, flavor_btv, eta, pt)
            # check if SF is OK
            if sf < 0.01:
                if self.verbose > 0:
                    print("jet #%i: pT = %1.1f, eta = %1.1f, discr = %1.3f, flavor = %i" % (idx, pt, eta, discr, flavor_btv))
                sf = 1.
            yield sf


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = Collection(event, "Jet")

        discr = None
        if self.algo == "csvv2":
            discr = "btagCSVV2"
        elif self.algo == "deepcsv":
            discr = "btagDeepB"
        elif self.algo == "cmva":
            discr = "btagCMVA"
        elif self.algo == "deepjet":
            discr = "btagDeepFlavB"
        else:
            raise ValueError("ERROR: Invalid algorithm '%s'!" % self.algo)

        preloaded_jets = [(jet.pt, jet.eta, self.getFlavorBTV(jet.hadronFlavour), getattr(jet, discr)) for jet in jets]
        for wp in self.selectedWPs:
            reader = self.getReader(wp)
            isShape = ( wp == 'shape_corr' )
            central_and_systs = ( self.central_and_systs_shape_corr if isShape else self.central_and_systs )
            for central_or_syst in central_and_systs:
                scale_factors = list(self.getSFs(preloaded_jets, central_or_syst, reader, 'auto', isShape))
                self.out.fillBranch(self.branchNames_central_and_systs[wp][central_or_syst], scale_factors)

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

btagSF2016 = lambda : btagSFProducer("2016")
btagSF2017 = lambda : btagSFProducer("2017")
