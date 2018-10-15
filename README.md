# nanoAOD-tools
Tools for working with NanoAOD (requiring only python + root, not CMSSW)

## Checkout instructions: PAF

You need to install a recent version of CMSSW

    cmsrel CMSSW_9_4_6
    cd CMSSW_9_4_6/src
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

Set the modules used in the analysis in crab_script.py and crab_script_data.py.
Set the crab options in crab_cfg.py (only to run manually).

To send jobs, run this script and follow the instructions:

    python SubmitDatasets.py

To run on several datasets, edit the txt files in the /datasets folder.

## Run in local:

The code is prepared to run an example. After setting the enviroment:

    cd PhysicsTools/NanoAODTools/python/postprocessing/
    python NanoPAFprepare.py

This shoud run on a nanoAOD file and produce an output.

## Some important info:

#### What is this doing? It reads a nanoAOD and:
- Applies a string-like skim
- Use the module skimNRecoLeps to select events with 2 leptons with pT > 18, eta < 2.5
- Removes plenty of branches
- Produces PU weights
- Produces Count / SumWeights histograms
- Changes the name of the main tree 'Events' to 'tree'
- Changes the output name and copies the output to a T2
- Adds jet energy uncertianties (although too many branches are produced...)

#### What am I missing?
- Some high-level variables: it would be nice to produce at this level some variables such as:
     lepton pt ratio, lepton pt rel, n ISR jets...
- LHE weights: they exist in nanoAOD but the format may be different from what is expected
- Functions to produce more skims??
