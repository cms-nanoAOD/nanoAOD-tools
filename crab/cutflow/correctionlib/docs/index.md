# correctionlib

The purpose of this library is to provide a well-structured JSON data format for a
wide variety of ad-hoc correction factors encountered in a typical HEP analysis and
a companion evaluation tool suitable for use in C++ and python programs.
Here we restrict our definition of correction factors to a class of functions with
scalar inputs that produce a scalar output.


In python, the function signature is:

```python
from typing import Union

def f(*args: Union[str,int,float]) -> float:
    return ...
```

In C++, the evaluator implements this currently as:
```cpp
double Correction::evaluate(const std::vector<std::variant<int, double, std::string>>& values) const;
```

The supported function classes include:

  * multi-dimensional binned lookups;
  * binned lookups pointing to multi-argument formulas with a restricted
    math function set (`exp`, `sqrt`, etc.);
  * categorical (string or integer enumeration) maps;
  * input transforms (updating one input value in place); and
  * compositions of the above.

Each function type is represented by a "node" in a call graph and holds all
of its parameters in a JSON structure, described by the JSON schema.
Possible future extension nodes might include weigted sums (which, when composed with
the others, could represent a BDT) and perhaps simple MLPs.

The tool should provide:

  * standardized, versioned [JSON schemas](https://json-schema.org/);
  * forward-porting tools (to migrate data written in older schema versions); and
  * a well-optimized C++ evaluator and python bindings (with numpy vectorization support).

This tool will definitely not provide:

  * support for `TLorentzVector` or other object-type inputs (such tools should be written
    as a higher-level tool depending on this library as a low-level tool)

Formula support currently includes a mostly-complete subset of the ROOT library `TFormula` class,
and is implemented in a threadsafe standalone manner. The parsing grammar is formally defined
and parsed through the use of a header-only [PEG parser library](https://github.com/yhirose/cpp-peglib).
The supported features mirror CMSSW's [reco::formulaEvaluator](https://github.com/cms-sw/cmssw/pull/11516)
and fully passes the test suite for that utility with the purposeful exception of the `TMath::` namespace.
The python bindings may be able to call into [numexpr](https://numexpr.readthedocs.io/en/latest/user_guide.html),
though, due to the tree-like structure of the corrections, it may prove difficult to exploit vectorization
at levels other than the entrypoint.

```{toctree}
---
maxdepth: 2
caption: Contents
glob:
---
Introduction <self>
install
highlevel
schemav1
schemav2
convert
core
```


## Indices and tables

* {ref}`genindex`
* {ref}`modindex`
* {ref}`search`
