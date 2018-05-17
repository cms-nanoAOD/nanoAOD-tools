# nanoAOD-tools
Tools for working with NanoAOD (requiring only python + root, not CMSSW)

## Checkout instructions: PAF

You need to install a recent version of CMSSW

    cmsrel CMSSW_9_4_6_patch1
    cd CMSSW_9_4_6_patch1/src
    cmsenv

Clone the code from the Oviedo-PAF group.

    git clone https://github.com/Oviedo-PAF/nanoAOD-tools.git PhysicsTools/NanoAODTools
    scram b


## How to run on CRAB

Set the enviroment.

    cmsenv
    source /cvmfs/cms.cern.ch/crab3/crab.sh

Move to the directory:
 
    cd PhysicsTools/NanoAODTools/crab

Prepare the files: 

    crab_cfg.py
    crab_script.py
    PSet.py

Send jobs:

    crab submit -c crab_script.sh


## Some important info:

#### What is this doing? It reads a nanoAOD and:
- Applies a string-like skim
- Removes plenty of branches
- Produces PU weights
- Produces Count / SumWeights histograms
- Changes the name of the main tree 'Events' to 'tree'
- Changes the output name and copies the output to a T2

#### What am I missing?
- Jet energy uncertianties (module is ready, but produces too many branches...)
- Functions to perform more useful skims (e.g.: 2 leptons with pT > x, 2 tight leptons, etc...)
- Some high-level variables: it would be nice to produce at this level some variables such as:
     lepton pt ratio, lepton pt rel, n ISR jets...
- LHE weights: they exist in nanoAOD but the format may be different from what is expected
