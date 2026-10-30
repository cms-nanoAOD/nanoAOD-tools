from typing import List, Optional, Union

from pydantic import BaseModel

try:
    from typing import Literal  # type: ignore
except ImportError:
    from typing_extensions import Literal


VERSION = 1


class Model(BaseModel):
    class Config:
        extra = "forbid"


class Variable(Model):
    name: str
    type: Literal["string", "int", "real"]
    "Implicitly 64 bit integer and double-precision floating point?"
    description: Optional[str]
    # TODO: clamping behavior for out of range?


class Formula(Model):
    # TODO: nodetype: Literal["formula"]
    expression: str
    parser: Literal["TFormula", "numexpr"]
    parameters: List[int]
    "Index to Correction.inputs[]"


# py3.7+: ForwardRef can be used instead of strings
Content = Union["Binning", "MultiBinning", "Category", Formula, float]


class Binning(Model):
    nodetype: Literal["binning"]
    edges: List[float]
    "Edges of the binning, where edges[i] <= x < edges[i+1] => f(x, ...) = content[i](...)"
    content: List[Content]


class MultiBinning(Model):
    """N-dimensional rectangular binning"""

    nodetype: Literal["multibinning"]
    edges: List[List[float]]
    """Bin edges for each input

    C-ordered array, e.g. content[d1*d2*d3*i0 + d2*d3*i1 + d3*i2 + i3] corresponds
    to the element at i0 in dimension 0, i1 in dimension 1, etc. and d0 = len(edges[0])-1, etc.
    """
    content: List[Content]


class Category(Model):
    nodetype: Literal["category"]
    # TODO: should be Union[List[str], List[int]]
    keys: List[Union[str, int]]
    content: List[Content]


Binning.update_forward_refs()
MultiBinning.update_forward_refs()
Category.update_forward_refs()


class Correction(Model):
    name: str
    "A useful name"
    description: Optional[str]
    "Detailed description of the correction"
    version: int
    "Version"
    inputs: List[Variable]
    output: Variable
    data: Content


class CorrectionSet(Model):
    schema_version: Literal[VERSION]
    "Schema version"
    corrections: List[Correction]


if __name__ == "__main__":
    import os
    import sys

    dirname = sys.argv[-1]
    with open(os.path.join(dirname, f"schemav{VERSION}.json"), "w") as fout:
        fout.write(CorrectionSet.schema_json(indent=4))
