"""High-level correctionlib objects

"""
import json
from numbers import Integral
from typing import Any, Dict, Iterator, List, Mapping, Union

import numpy

import correctionlib._core
import correctionlib.version


def open_auto(filename: str) -> str:
    """Open a file and return its contents"""
    if filename.endswith(".json.gz"):
        import gzip

        with gzip.open(filename, "rt") as gzfile:
            return gzfile.read()
    elif filename.endswith(".json"):
        with open(filename) as file:
            return file.read()
    raise ValueError(f"{filename}: unrecognized file format, expected .json, .json.gz")


def model_auto(data: str) -> Any:
    """Read schema version from json object and construct appropriate model"""
    data = json.loads(data)
    if not isinstance(data, dict):
        raise ValueError("CorrectionSet is not a dictionary!")
    version = data.get("schema_version", None)
    if version is None:
        raise ValueError("CorrectionSet has no schema version!")
    if not isinstance(version, Integral):
        raise ValueError(f"CorrectionSet schema version ({version}) is not an integer!")
    if version == 1:
        import correctionlib.schemav1

        return correctionlib.schemav1.CorrectionSet.parse_obj(data)
    elif version == 2:
        import correctionlib.schemav2

        return correctionlib.schemav2.CorrectionSet.parse_obj(data)
    raise ValueError(f"Unknown CorrectionSet schema version ({version})")


class Correction:
    """High-level correction evaluator object

    This class is typically instantiated by accessing a named correction from
    a CorrectionSet object, rather than directly by construction.
    """

    def __init__(self, base: correctionlib._core.Correction, context: "CorrectionSet"):
        self._base = base
        self._name = base.name
        self._context = context

    def __getstate__(self) -> Dict[str, Any]:
        return {"_context": self._context, "_name": self._name}

    def __setstate__(self, state: Dict[str, Any]) -> None:
        self._context = state["_context"]
        self._name = state["_name"]
        self._base = self._context[self._name]._base

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._base.description

    @property
    def version(self) -> int:
        return self._base.version

    def evaluate(
        self, *args: Union["numpy.ndarray[Any, Any]", str, int, float]
    ) -> Union[float, "numpy.ndarray[Any, numpy.dtype[numpy.float64]]"]:
        # TODO: create a ufunc with numpy.vectorize in constructor?
        vargs = [arg for arg in args if isinstance(arg, numpy.ndarray)]
        if vargs:
            bargs = numpy.broadcast_arrays(*vargs)
            oshape = bargs[0].shape
            fargs = (arg.flatten() for arg in bargs)
            out = self._base.evalv(
                *(
                    next(fargs) if isinstance(arg, numpy.ndarray) else arg
                    for arg in args
                )
            )
            return out.reshape(oshape)
        return self._base.evaluate(*args)  # type: ignore


class CompoundCorrection:
    """High-level compound correction evaluator object

    This class is typically instantiated by accessing a named correction from
    a CorrectionSet object, rather than directly by construction.
    """

    def __init__(
        self, base: correctionlib._core.CompoundCorrection, context: "CorrectionSet"
    ):
        self._base = base
        self._name = base.name
        self._context = context

    def __getstate__(self) -> Dict[str, Any]:
        return {"_context": self._context, "_name": self._name}

    def __setstate__(self, state: Dict[str, Any]) -> None:
        self._context = state["_context"]
        self._name = state["_name"]
        self._base = self._context.compound[self._name]._base

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._base.description

    def evaluate(
        self, *args: Union["numpy.ndarray[Any, Any]", str, int, float]
    ) -> Union[float, "numpy.ndarray[Any, numpy.dtype[numpy.float64]]"]:
        # TODO: create a ufunc with numpy.vectorize in constructor?
        vargs = [arg for arg in args if isinstance(arg, numpy.ndarray)]
        if vargs:
            bargs = numpy.broadcast_arrays(*vargs)
            oshape = bargs[0].shape
            fargs = (arg.flatten() for arg in bargs)
            out = self._base.evalv(
                *(
                    next(fargs) if isinstance(arg, numpy.ndarray) else arg
                    for arg in args
                )
            )
            return out.reshape(oshape)
        return self._base.evaluate(*args)  # type: ignore


class _CompoundMap(Mapping[str, CompoundCorrection]):
    def __init__(
        self,
        base: Mapping[str, correctionlib._core.CompoundCorrection],
        context: "CorrectionSet",
    ):
        self._base = base
        self._context = context

    def __getitem__(self, key: str) -> CompoundCorrection:
        corr = self._base.__getitem__(key)
        return CompoundCorrection(corr, self._context)

    def __len__(self) -> int:
        return len(self._base)

    def __iter__(self) -> Iterator[str]:
        return iter(self._base)


class CorrectionSet(Mapping[str, Correction]):
    """High-level correction set evaluator object

    This class can be initialized directly from a string or model with compatible
    schema version, or can be initialized via the ``from_file`` or
    ``from_string`` factory methods. Corrections can be accessed
    via getitem syntax, e.g. ``cset["some correction"]``.
    """

    def __init__(self, data: Any):
        if isinstance(data, str):
            self._data = data
        else:
            self._data = data.json(exclude_unset=True)
        self._base = correctionlib._core.CorrectionSet.from_string(self._data)

    @classmethod
    def from_file(cls, filename: str) -> "CorrectionSet":
        return cls(open_auto(filename))

    @classmethod
    def from_string(cls, data: str) -> "CorrectionSet":
        return cls(data)

    def __getstate__(self) -> Dict[str, Any]:
        return {"_data": self._data}

    def __setstate__(self, state: Dict[str, Any]) -> None:
        self._data = state["_data"]
        self._base = correctionlib._core.CorrectionSet.from_string(self._data)

    def _ipython_key_completions_(self) -> List[str]:
        return list(self.keys())

    @property
    def schema_version(self) -> int:
        return self._base.schema_version

    def __getitem__(self, key: str) -> Correction:
        corr = self._base.__getitem__(key)
        return Correction(corr, self)

    def __len__(self) -> int:
        return len(self._base)

    def __iter__(self) -> Iterator[str]:
        return iter(self._base)

    @property
    def compound(self) -> _CompoundMap:
        return _CompoundMap(self._base.compound, self)
