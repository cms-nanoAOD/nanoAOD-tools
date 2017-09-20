# nanoAOD-tools
Tools for working with NanoAOD (requiring only python + root, not CMSSW)

## checkout instructions: standalone

You need to setup python 2.7 and a recent ROOT version first.

    git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git NanoAODTools
    cd NanoAODTools
    source standalone/env_standalone.sh

Repeat the source command at the beginning of every session.

It will create a build directory the first time it is run. This directory should never be committed.

Also, do not commit any of the empty init.py files created by the script.

## checkout instructions: CMSSW

    cd $CMSSW_BASE/src
    git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools

