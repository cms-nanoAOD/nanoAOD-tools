def register_pyroot_binding() -> None:
    import os.path
    import sys

    import pkg_resources
    from cppyy import gbl

    # maybe not the most robust solution?
    if sys.platform.startswith("win32"):
        lib = pkg_resources.resource_filename(
            "correctionlib", os.path.join("lib", "correctionlib.dll")
        )
    elif sys.platform.startswith("darwin"):
        lib = pkg_resources.resource_filename(
            "correctionlib", os.path.join("lib", "libcorrectionlib.dylib")
        )
    else:
        lib = pkg_resources.resource_filename(
            "correctionlib", os.path.join("lib", "libcorrectionlib.so")
        )
    gbl.gSystem.Load(lib)
    gbl.gInterpreter.AddIncludePath(
        pkg_resources.resource_filename("correctionlib", "include")
    )
    gbl.gROOT.ProcessLine('#include "correction.h"')
