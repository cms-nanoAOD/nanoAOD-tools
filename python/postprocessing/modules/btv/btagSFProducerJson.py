from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
import ROOT
import os
from itertools import chain
import correctionlib
import numpy as np

ROOT.PyConfig.IgnoreCommandLineOptions = True


def is_relevant_syst_for_shape_corr(flavor_btv, syst, jesSystsForShape=["jes"]):
    """Returns true if a flavor/syst combination is relevant"""
    jesSysts = list(chain(*[("up_" + j, "down_" + j)
                            for j in jesSystsForShape]))

    if flavor_btv == 5:
        return syst in ["central",
                        "up_lf", "down_lf",
                        "up_hfstats1", "down_hfstats1",
                        "up_hfstats2", "down_hfstats2"] + jesSysts
    elif flavor_btv == 4:
        return syst in ["central",
                        "up_cferr1", "down_cferr1",
                        "up_cferr2", "down_cferr2"]
    elif flavor_btv == 0:
        return syst in ["central",
                        "up_hf", "down_hf",
                        "up_lfstats1", "down_lfstats1",
                        "up_lfstats2", "down_lfstats2"] + jesSysts
    else:
        raise ValueError("ERROR: Undefined flavor = %i!!" % flavor_btv)
    return True


class btagSFProducer(Module):
    """Calculate btagging scale factors
    """

    def __init__(
            self, era, algo='csvv2', selectedWPs=['M', 'shape_corr'],
            sfFileName=None, verbose=0, jesSystsForShape=["jes","jesAbsoluteStat",'jesAbsoluteMPFBias','jesFragmentation','jesSinglePionECAL','jesSinglePionHCAL','jesTimePtEta','jesRelativeJEREC1','jesRelativeJEREC2','jesRelativeJERHF','jesRelativePtBB','jesRelativePtEC1','jesRelativePtEC2','jesRelativePtHF','jesRelativeBal','jesRelativeSample','jesRelativeFSR','jesRelativeStatEC','jesRelativeStatHF','jesPileUpDataMC','jesPileUpPtRef','jesPileUpPtBB','jesPileUpPtEC1','jesPileUpPtEC2','jesPileUpPtHF',"jesAbsoluteScale", "jesFlavorQCD", "jesRelativeStatFSR"]
    ):
        self.era = era
        self.algo = algo
        self.selectedWPs = selectedWPs
        self.verbose = verbose
        self.jesSystsForShape = jesSystsForShape
        # CV: Return value of BTagCalibrationReader::eval_auto_bounds() is zero
        # in case jet abs(eta) > 2.4 !!
        self.max_abs_eta = 2.5
        # define measurement type for each flavor
        self.inputFilePath = "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/BTV/"
        self.inputFileName = sfFileName
        self.measurement_types = None
        self.supported_wp = None
        supported_btagSF = {
            'deepCSV': {
                'UL2017': {
                    'inputFileName': "2017_UL/btagging.json.gz",
                    'measurement_types': {
                        5: "comb",  # b
                        4: "comb",  # c
                        0: "incl"   # light
                    },
                    'supported_wp': ["L", "M", "T", "shape_corr"]
                },
		        'UL2018': {
                    'inputFileName': "2018_UL/btagging.json.gz",
                    'measurement_types': {
                        5: "comb",  # b
                        4: "comb",  # c
                        0: "incl"   # light
                    },
                    'supported_wp': ["L", "M", "T", "shape_corr"]
                },
            },
            'deepJet': {
                'UL2016preVFP': {
                    'inputFileName': "2016preVFP_UL/btagging.json.gz",
                    'measurement_types': {
                        5: "comb",  # b
                        4: "comb",  # c
                        0: "incl"   # light
                    },
                    'supported_wp': ["L", "M", "T", "shape_corr"]
                },
                'UL2016postVFP': {
                    'inputFileName': "2016postVFP_UL/btagging.json.gz",
                    'measurement_types': {
                        5: "comb",  # b
                        4: "comb",  # c
                        0: "incl"   # light
                    },
                    'supported_wp': ["L", "M", "T", "shape_corr"]
                },
                'UL2017': {
                    'inputFileName': "2017_UL/btagging.json.gz",
                    'measurement_types': {
                        5: "comb",  # b
                        4: "comb",  # c
                        0: "incl"   # light
                    },
                    'supported_wp': ["L", "M", "T", "shape_corr"]
                },
                'UL2018': {
                    'inputFileName': "2018_UL/btagging.json.gz",
                    'measurement_types': {
                        5: "comb",  # b
                        4: "comb",  # c
                        0: "incl"   # light
                    },
                    'supported_wp': ["L", "M", "T", "shape_corr"]
                },	
            }
        }

        supported_algos = []
        for algo in list(supported_btagSF.keys()):
            if self.era in list(supported_btagSF[algo].keys()):
                supported_algos.append(algo)
        if self.algo in list(supported_btagSF.keys()):
            if self.era in list(supported_btagSF[self.algo].keys()):
                if self.inputFileName is None:
                    self.inputFileName = supported_btagSF[self.algo][self.era]['inputFileName']
                self.measurement_types = supported_btagSF[self.algo][self.era]['measurement_types']
                self.supported_wp = supported_btagSF[self.algo][self.era]['supported_wp']
            else:
                raise ValueError("ERROR: Algorithm '%s' not supported for era = '%s'! Please choose among { %s }." % (
                    self.algo, self.era, supported_algos))
        else:
            raise ValueError("ERROR: Algorithm '%s' not supported for era = '%s'! Please choose among { %s }." % (
                self.algo, self.era, supported_algos))
        for wp in self.selectedWPs:
            if wp not in self.supported_wp:
                raise ValueError("ERROR: Working point '%s' not supported for algo = '%s' and era = '%s'! Please choose among { %s }." % (
                    wp, self.algo, self.era, self.supported_wp))

        # define systematic uncertainties
        self.systs = []
        self.systs.append("up")
        self.systs.append("down")
        self.central_and_systs = ["central"]
        self.central_and_systs.extend(self.systs)

        self.systs_shape_corr = []
        for syst in ['lf', 'hf',
                     'hfstats1', 'hfstats2',
                     'lfstats1', 'lfstats2',
                     'cferr1', 'cferr2'] + self.jesSystsForShape:
            self.systs_shape_corr.append("up_%s" % syst)
            self.systs_shape_corr.append("down_%s" % syst)
        self.central_and_systs_shape_corr = ["central"]
        self.central_and_systs_shape_corr.extend(self.systs_shape_corr)

        self.branchNames_central_and_systs = {}
        for wp in self.selectedWPs:
            branchNames = {}
            if wp == 'shape_corr':
                central_and_systs = self.central_and_systs_shape_corr
                baseBranchName = 'Jet_btagSF_{}_shape'.format(self.algo.lower())
            else:
                central_and_systs = self.central_and_systs
                baseBranchName = 'Jet_btagSF_{}_{}'.format(self.algo.lower(), wp)
            for central_or_syst in central_and_systs:
                if central_or_syst == "central":
                    branchNames[central_or_syst] = baseBranchName
                else:
                    branchNames[central_or_syst] = baseBranchName + \
                        '_' + central_or_syst
            self.branchNames_central_and_systs[wp] = branchNames

    def beginJob(self):
        # initialize BTagCalibrationReader
        # (cf. https://twiki.cern.ch/twiki/bin/viewauth/CMS/BTagCalibration )
        self.calibration = correctionlib.CorrectionSet.from_file(os.path.join(self.inputFilePath, self.inputFileName))
        self.readers = {}
        for wp in self.selectedWPs:
            #wp_btv = {"l": 0, "m": 1, "t": 2,
            #          "shape_corr": 3}.get(wp.lower(), None)
            syts = None
            if wp in ["L", "M", "T"]:
                systs = self.systs
            else:
                systs = self.systs_shape_corr
            if wp == "shape_corr":
                reader = lambda systematic, flavor, abdeta, pt, disc: self.calibration[self.algo + "_shape"].evaluate(systematic, flavor, abdeta, pt, disc)
            else:
                reader = lambda systematic, flavor, abdeta, pt: self.calibration[self.algo + "_comb"].evaluate(systematic, wp, flavor, abdeta, pt)
            self.readers[wp] = reader

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for central_or_syst in list(self.branchNames_central_and_systs.values()):
            for branch in list(central_or_syst.values()):
                self.out.branch(branch, "F", lenVar="nJet")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def getReader(self, wp):
        """
            Get btag scale factor reader.
            Convert working points: input is 'L', 'M', 'T', 'shape_corr' to 0, 1, 2, 3
        """
        if wp is None or wp not in list(self.readers.keys()):
            if self.verbose > 0:
                print(
                    "WARNING: Unknown working point '%s', setting b-tagging SF reader to None!" % wp)
            return None
        return self.readers[wp]

    def getFlavorBTV(self, flavor):
        '''
            Maps hadronFlavor to BTV flavor:
            Note the flavor convention: hadronFlavor is b = 5, c = 4, f = 0
            Convert them to the btagging group convention of 0, 1, 2
        '''
        flavor_btv = None
        if abs(flavor) == 5:
            flavor_btv = 5
        elif abs(flavor) == 4:
            flavor_btv = 4
        elif abs(flavor) in [0, 1, 2, 3, 21]:
            flavor_btv = 0
        else:
            if self.verbose > 0:
                print(
                    "WARNING: Unknown flavor '%s', setting b-tagging SF to -1!" % repr(flavor))
            return -1.
        return flavor_btv

    def getSFs(self, jet_data, syst, reader, measurement_type='auto', shape_corr=False):
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
                    sf = reader.eval_auto_bounds(
                        syst, flavor_btv, eta, pt, discr)
                else:
                    sf = reader.eval_auto_bounds(
                        'central', flavor_btv, eta, pt, discr)
            else:
                sf = reader.eval_auto_bounds(syst, flavor_btv, eta, pt)
            # check if SF is OK
            if sf < 0.01:
                if self.verbose > 0:
                    print("jet #%i: pT = %1.1f, eta = %1.1f, discr = %1.3f, flavor = %i" % (
                        idx, pt, eta, discr, flavor_btv))
                sf = 1.
            yield sf

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = Collection(event, "Jet")

        discr = None
        if self.algo == "deepCSV":
            discr = "btagDeepB"
        elif self.algo == "deepJet":
            discr = "btagDeepFlavB"
        else:
            raise ValueError("ERROR: Invalid algorithm '%s'!" % self.algo)
        
        jets_flav = np.array([int(jet.hadronFlavour) for jet in jets])
        jets_abseta_dummy = [np.abs(jet.eta) for jet in jets]
        jets_eta = []
        for AbsEta in jets_abseta_dummy:
            if AbsEta >= 2.5: jets_eta.append(2.5-0.001)
            else: jets_eta.append(AbsEta)
        jets_eta = np.array(jets_eta)
        jets_pt = np.array([jet.pt for jet in jets])
        jets_disc = np.array([getattr(jet, discr) for jet in jets])
        #preloaded_jets = [(jet.pt, jet.eta, self.getFlavorBTV(
        #    jet.hadronFlavour), getattr(jet, discr)) for jet in jets]
        
        for wp in self.selectedWPs:
            reader = self.getReader(wp)
            isShape = (wp == 'shape_corr')
            central_and_systs = (
                self.central_and_systs_shape_corr if isShape else self.central_and_systs)
            #print(jets_flav, jets_eta, jets_pt, jets_disc)
            for central_or_syst in central_and_systs:
                #print(central_or_syst)
                scale_factors_eta_corrected = []
                if isShape: 
                    if 'cferr' in central_or_syst:
                        scale_factors = []
                        for i in range(len(jets_flav)):
                            if jets_flav[i] in [4]:scale_factors.append(reader(central_or_syst, 4, jets_eta[i], jets_pt[i], jets_disc[i]))
                            else: scale_factors.append(reader("central", jets_flav[i], jets_eta[i], jets_pt[i], jets_disc[i]))
                    elif ('lf' in central_or_syst or ('hf' in central_or_syst) or ('jes' in central_or_syst)):
                        scale_factors = []
                        for i in range(len(jets_flav)):
                            if jets_flav[i] in [4]: scale_factors.append(reader("central", jets_flav[i], jets_eta[i], jets_pt[i], jets_disc[i]))
                            else: scale_factors.append(reader(central_or_syst, jets_flav[i], jets_eta[i], jets_pt[i], jets_disc[i]))
                    else:
                        scale_factors = []
                        for i in range(len(jets_flav)):
                            scale_factors.append(reader(central_or_syst, jets_flav[i], jets_eta[i], jets_pt[i], jets_disc[i]))
                        #if jets_flav[i] == 4: print(scale_factors[i], jets_flav[i], jets_eta[i], jets_pt[i], jets_disc[i])
                else: scale_factors = reader(central_or_syst, jets_flav, jets_eta, jets_pt)
                for i,AbsEta in enumerate(jets_abseta_dummy):
                     if(AbsEta >= 2.5): 
                          scale_factors_eta_corrected.append(1)
                     else: 
                          scale_factors_eta_corrected.append(scale_factors[i])
                #print(f'{jets_abseta_dummy = }')
                #print(f'{scale_factors = }')
                #print(f'{scale_factors_eta_corrected = }')
                self.out.fillBranch(
                    self.branchNames_central_and_systs[wp][central_or_syst], scale_factors_eta_corrected)
        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed


btagSF2016 = lambda: btagSFProducer("2016")
btagSF2017 = lambda: btagSFProducer("2017")
