# Lambda NanoAOD Tools (taken from cmsNanoaod tool)
Tools for working with NanoAOD (requiring only python + root, not CMSSW)

# UNDER DEVELOPMENT

## To-do list

  Rewritten lambdaframework, more consistent with postprocesser definition with plotter.

 - [ ] Postprocesser interface (SiewYan)
 - [ ] Chain of steps , specify which module is running (SiewYan+Matteo)
 - [ ] Production, the correct ntuple use (SiewYan+Matteo)
 - [ ] Collection of module:
    - [ ] Lepton maker (jet cleaning+WP compute) (SiewYan)
    - [ ] Muon maker (jet cleaning+WP compute) (Matteo)
    - [ ] Electron Maker (jet cleaning+WP compute) (SiewYan)
    - [ ] Jet maker (jet cleaning+WP compute) (Matteo)
    - [ ] MET maker (MET cleaner) (SiewYan)
    - [ ] Derived/analysis-specific Variable compute (need to declare in variables.py) (SiewYan + Matteo)
    - [ ] Trigger maker ? (SiewYan+Matteo)
 - [ ] Data folder hosting variable, SF, WP (SiewYan)
 - [ ] Plotting (kinda taking care of...) (SiewYan)
 - [ ] Making datacard (Matteo)
 - [ ] Using combine limit (SiewYan)

## Checkout instructions: standalone

You need to setup python 2.7 and a recent ROOT version first.

    git clone https://github.com/LambdaFramework/nanoAOD-tools.git NanoAODTools
    cd NanoAODTools
    bash standalone/env_standalone.sh build
    source standalone/env_standalone.sh

Repeat only the last command at the beginning of every session.

Please never commit neither the build directory, nor the empty init.py files created by the script.

## Checkout instructions: CMSSW

    cd $CMSSW_BASE/src
    git clone https://github.com/LambdaFramework/nanoAOD-tools.git PhysicsTools/NanoAODTools
    cd PhysicsTools/NanoAODTools
    cmsenv
    scram b

## General instructions to run the post-processing step
