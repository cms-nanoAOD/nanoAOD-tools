# nanoAOD-tools
Tools for working with NanoAOD (requiring only python + root, not CMSSW)

## Checkout instructions: standalone

You need to setup python 2.7 and a recent ROOT version first.

    git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git NanoAODTools
    cd NanoAODTools
    bash standalone/env_standalone.sh build
    source standalone/env_standalone.sh

Repeat only the last command at the beginning of every session.

Please never commit neither the build directory, nor the empty init.py files created by the script.

## Checkout instructions: CMSSW

    cd $CMSSW_BASE/src
    git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools

## General instructions to run the post-processing step

The script to run the post-processing step is `scripts/nano_postproc.py`.

The basic syntax of the command is the following:

    python scripts/nano_postproc.py /path/to/output_directory /path/to/input_tree.root

Here is a summary of its features:
* the `-s`,`--postfix` option is used to specify the suffix that will be appended to the input file name to obtain the output file name. It defaults to *_Friend* in friend mode, *_Skim* in full mode.
* the `-c`,`--cut` option is used to pass a string expression (using the same syntax as in TTree::Draw) that will be used to select events. It cannot be used in friend mode.
* the `-J`,`--json` option is used to pass the name of a JSON file that will be used to select events. It cannot be used in friend mode.
* if run with the `--full` option (default), the output will be a full nanoAOD file. If run with the `--friend` option, instead, the output will be a friend tree that can be attached to the input tree. In the latter case, it is not possible to apply any kind of event selection, as the number of entries in the parent and friend tree must be the same.
* the `-b`,`--branch-selection` option is used to pass the name of a file containing directives to keep or drop branches from the output tree. The file should contain one directive among `keep`/`drop` (wildcards allowed as in TTree::SetBranchStatus) or `keepmatch`/`dropmatch` (python regexp matching the branch name) per line, as shown in the [this](python/postprocessing/examples/keep_and_drop.txt) example file.
  * `--bi` and `--bo` allows to specify the keep/drop file separately for input and output trees.  
* the `--justcount` option will cause the script to printout the number of selected events, without actually writing the output file.

Please run with `--help` for a complete list of options.

## How to write and run modules

It is possible to import modules that will be run on each entry passing the event selection, and can be used to calculate new variables that will be included in the output tree (both in friend and full mode) or to apply event filter decisions.

We will use `python/postprocessing/examples/mhtProducer.py` as an example.

The module definition [file](python/postprocessing/examples/mhtProducer.py), containing the constructor:

    mht = lambda : mhtProducer( lambda j : j.pt > 40, 
                                lambda mu : mu.pt > 20 and mu.miniPFIso_all/mu.pt < 0.2,
                                lambda el : el.pt > 20 and el.miniPFIso_all/el.pt < 0.2 ) 

should be imported using the following syntax:

`python scripts/nano_postproc.py -I PhysicsTools.NanoAODTools.postprocessing.examples.mhtProducer mht`

Let us now examine the structure of the `mhtProducer` module class. All modules must inherit from `PhysicsTools.NanoAODTools.postprocessing.framework.eventloop.Module`.
* the `__init__` constructor function should be used to set the module options.
* the `beginFile` function should create the branches that you want to add to the output file, calling the `branch(branchname, typecode, lenVar)` method of `wrappedOutputTree`. `typecode` should be the ROOT TBranch type ("F" for float, "I" for int etc.). `lenVar` should be the name of the variable holding the length of array branches (for instance, `branch("Electron_myNewVar","F","nElectron")`). If the `lenVar` branch does not exist already - it can happen if you create a new collection, see an example [here](python/postprocessing/examples/collectionMerger.py)) - it will be automatically created.
* the `analyze` function is called on each event. It should return `True` if the event is to be retained, `False` if it should be dropped.

The event interface, defined in `PhysicsTools.NanoAODTools.postprocessing.framework.datamodule`, allows to dynamically construct views of objects organized in collections, based on the branch names, for instance:

    electrons = Collection(event, "Electron")
    if len(electrons)>1: print electrons[0].someVar+electrons[1].someVar
    electrons_highpt = filter(lambda x: x.pt>50, electrons)

and this will access the elements of the `Electron_someVar`, `Electron_pt` branch arrays. Event variables can be accessed simply by `event.someVar`, for instance `event.rho`.

The output branches should be filled calling the `fillBranch(branchname, value)` method of `wrappedOutputTree`. `value` should be the desired value for single-value branches, an iterable with the correct length for array branches. It is not necessary to fill the `lenVar` branch explicitly, as this is done automatically using the length of the passed iterable.

## Keep/drop branches
See the effect of keep/drop instructions by running:
```
python scripts/nano_postproc.py outDir /eos/user/a/andrey/f.root -I PhysicsTools.NanoAODTools.postprocessing.examples.exampleModule exampleModule -s _exaModu_keepdrop --bi scripts/keep_and_drop_input.txt --bo scripts/keep_and_drop_output.txt
```
comparing to:
```
python scripts/nano_postproc.py outDir /eos/user/a/andrey/f.root -I PhysicsTools.NanoAODTools.postprocessing.examples.exampleModule exampleModule -s _exaModu
```
The output branch created by exampleModule produces the same result in both cases. But thefirst one drops all other branches when creating output tree. It also runs faster.

