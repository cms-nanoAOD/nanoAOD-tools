import pickle

import numpy
import pytest

import correctionlib
from correctionlib import schemav2 as model


def test_highlevel():
    cset = correctionlib.CorrectionSet(
        model.CorrectionSet(
            schema_version=model.VERSION,
            corrections=[
                model.Correction(
                    name="test corr",
                    version=2,
                    inputs=[
                        model.Variable(name="a", type="real"),
                        model.Variable(name="b", type="real"),
                    ],
                    output=model.Variable(name="a scale", type="real"),
                    data=1.234,
                )
            ],
        )
    )
    assert set(cset) == {"test corr"}
    sf = cset["test corr"]
    assert sf.version == 2
    assert sf.description == ""

    with pytest.raises(RuntimeError):
        sf.evaluate(0, 1.2, 35.0, 0.01)

    assert sf.evaluate(1.0, 1.0) == 1.234
    numpy.testing.assert_array_equal(
        sf.evaluate(numpy.ones((3, 4)), 1.0),
        numpy.full((3, 4), 1.234),
    )
    numpy.testing.assert_array_equal(
        sf.evaluate(numpy.ones((3, 4)), numpy.ones(4)),
        numpy.full((3, 4), 1.234),
    )

    sf2 = pickle.loads(pickle.dumps(sf))
    assert sf2.evaluate(1.0, 1.0) == 1.234
