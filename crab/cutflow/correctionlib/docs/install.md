# Installation

This package provides both a C++ evaluator with python bindings and
a set of python tools to convert, validate, and inspect files with corrections
It is installed as a python package (see e.g.
[this tutorial](https://packaging.python.org/tutorials/installing-packages/)
for an introduction), using [scikit-build](https://scikit-build.readthedocs.io/)
and thus [CMake](https://cmake.org/), for the C++ components.
Builds have been tested in Windows, OS X, and Linux, and the python bindings
can be compiled against both python2 (with limited functionality) and python3,
as well as from within a CMSSW environment.
Note that CMSSW ``11_2_X`` and above has ROOT accessible from python 3.

## Inside CMSSW

For CMSSW releases from the `11_3_X` branch on, correctionlib is included
as the `py3-correctionlib` tool, and from the `12_1_X` branch version 2.0,
which has the schema version 2.0 that is used by most of the corrections.
If the tool included in CMSSW supports the version you want to use,
no additional installation is needed.
The package version can also be found with the command-line tool:
```bash
correction config --version
```

For older release cycles the package can be installed in the user area with
```bash
python3 -m pip install --user --no-binary=correctionlib correctionlib
```
for python3.
Alternatively, [this script](https://gist.github.com/pieterdavid/8f43f302e9f8a71f92702101600b7ddb),
can be used to install a `py3-correctionlib` tool similar to the one provided in more recent releases,
or a `py2-correctionlib` tool with limited functionality.

The package can be built as follows:
```bash
git clone --recursive git@github.com:cms-nanoAOD/correctionlib.git
cd correctionlib
make PYTHON=python
make install  # set PREFIX=... to change from default (./correctionlib)
```
where `python` is the name of the python scram tool you intend to link against.
This will output a `correctionlib` directory that acts as a python package, and can be moved where needed.

## Outside CMSSW

To install in an environment that has python 3, you can simply
```bash
python3 -m pip install correctionlib
```
(possibly with `--user`, or in a virtualenv, etc.)
```{admonition} Wheels or installing from source?
The above command will try to use python wheels, prebuilt binary packages,
since it is faster and more efficient.
When using the C++ evaluator, e.g. from ROOT or a standalone executable,
the C++ ABI needs to be compatible, otherwise you will get linker errors.
To avoid this pass the `--no-binary=correctionlib` option to `pip install`,
which will start from the source package and build the C++ components in your environment.
```

If you wish to install the latest development version, this should work:
```bash
python3 -m pip install git+https://github.com/cms-nanoAOD/correctionlib.git
```

## With python 2 (outside CMSSW)

To compile with python2 support, consider using python 3 :).
If you considered that and still want to use python2, the following recipe may work
to install only the `correctionlib._core` evaluator,
which allows to use the C++ evaluator from python2 and python3
(the schema tools and high-level bindings are python3-only):
```bash
git clone --recursive git@github.com:cms-nanoAOD/correctionlib.git
cd correctionlib
make PYTHON=python2
make install  # set PREFIX=... to change from default (./correctionlib)
```
This will output a `correctionlib` directory that acts as a python package, and can be moved where needed.

## Usage from python and C++

After the installation following one of the recipes above,
the correctionlib python package should be available,
as well as the `correction` command-line utility.
In case the latter is not on your path for some reason, it can also be invoked via
`python3 -m correctionlib.cli`.

The C++ evaluator library is distributed as part of the python package, and it can be
linked to directly without using python. If you are using CMake you can depend on it by including
the output of `correction config --cmake` in your cmake invocation. A complete cmake
example that builds a user C++ application against correctionlib and ROOT RDataFrame
can be [found here](https://gist.github.com/pieterdavid/a560e65658386d70a1720cb5afe4d3e9).

For manual compilation, include and linking definitions can similarly be found via `correction config --cflags --ldflags`.
For example, the demo application can be compiled with:
```bash
wget https://raw.githubusercontent.com/cms-nanoAOD/correctionlib/master/src/demo.cc
g++ $(correction config --cflags --ldflags --rpath) demo.cc -o demo
```
