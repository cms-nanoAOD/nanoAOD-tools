# How To Hgg Skimming

This branch contains the skimming code for the SnT Hgg analyses. The basic instructions on how to use it follow:

## Setup
```bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc700
cd skimming/directory
cmsrel CMSSW_10_6_30
cd CMSSW_10_6_30/src
cmsenv
git cms-init
git remote add cmstas git@github.com:cmstas/cmssw.git
git fetch cmstas
git checkout CMSSW_10_6_30_nanoAODtoolsHHggXX
git cms-addpkg CondFormats/BTauObjects
scram b -j 4
git clone git@github.com:cmstas/nanoAOD-tools.git PhysicsTools/NanoAODTools
cd PhysicsTools/NanoAODTools
git checkout HHggXX
scram b -j 4
```

## Usage
```bash
cd skimming/directory/CMSSW_10_6_30/src/PhysicsTools/NanoAODTools/crab
cmsenv
source /cvmfs/cms.cern.ch/common/crab-setup.sh
```

To select the samples to be skimmed, the `allsamples.py` needs to be modified, possibly also `sa.py`, if a new sample is added. The `make_samples.py` scripts helps with the creation of those files.

The skimming can be run on crab with the following command:

```bash
python crab_cfg_ggOnly.py --analysis ggbb --version test
```

where the `analysis` flag defines the skimmming configuration ("ggtautau" or "ggbb" for now) and the `version` flag defines the skimming tag.

The `crab_cfg_ggOnly.py` script contains the crab configuration. The execution script on crab is `crab_script_ggOnly.sh`, which calls `crab_script_ggOnly.py` to run the postprocessor.

Finally, the `keep_and_drop.txt` file defines the trimming to applied.
