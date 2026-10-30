import numpy
import pytest

import correctionlib._core as core
from correctionlib import schemav2 as schema


def wrap(*corrs):
    cset = schema.CorrectionSet(
        schema_version=schema.VERSION,
        corrections=list(corrs),
    )
    return core.CorrectionSet.from_string(cset.json())


def test_core_vectorized():
    cset = wrap(
        schema.Correction(
            name="test",
            version=1,
            inputs=[
                schema.Variable(name="a", type="real"),
                schema.Variable(name="b", type="int"),
                schema.Variable(name="c", type="string"),
            ],
            output=schema.Variable(name="a scale", type="real"),
            data={
                "nodetype": "category",
                "input": "b",
                "content": [
                    {
                        "key": 1,
                        "value": {
                            "nodetype": "formula",
                            "expression": "x",
                            "parser": "TFormula",
                            "variables": ["a"],
                        },
                    }
                ],
                "default": -99.0,
            },
        )
    )
    corr = cset["test"]

    assert corr.evaluate(0.3, 1, "") == 0.3
    assert corr.evalv(0.3, 1, "") == 0.3
    numpy.testing.assert_array_equal(
        corr.evalv(numpy.full(10, 0.3), 1, ""),
        numpy.full(10, 0.3),
    )
    numpy.testing.assert_array_equal(
        corr.evalv(0.3, numpy.full(10, 1), ""),
        numpy.full(10, 0.3),
    )
    numpy.testing.assert_array_equal(
        corr.evalv(numpy.full(10, 0.3), numpy.full(10, 1), ""),
        numpy.full(10, 0.3),
    )
    with pytest.raises(ValueError):
        corr.evalv(numpy.full(5, 0.3), numpy.full(10, 1), "")
    with pytest.raises(ValueError):
        corr.evalv(numpy.full((10, 2), 0.3), 1, "")
    with pytest.raises(ValueError):
        corr.evalv(0.3)
    with pytest.raises(ValueError):
        corr.evalv(0.3, 1, 1, 1)
    with pytest.raises(ValueError):
        corr.evalv(0.3, 1, numpy.full(10, "asdf"))

    a = numpy.linspace(-3, 3, 100)
    b = numpy.arange(100) % 3
    numpy.testing.assert_array_equal(
        corr.evalv(a, b, ""),
        numpy.where(b == 1, a, -99.0),
    )
