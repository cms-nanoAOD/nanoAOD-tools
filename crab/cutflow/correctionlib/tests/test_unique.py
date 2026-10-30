import pytest

import correctionlib.schemav2


def test_unique():
    def make(name):
        return {
            "name": name,
            "description": "",
            "inputs": [],
            "output": {"name": "out", "type": "real"},
            "version": 1,
            "data": 1.1,
        }

    def makec(name):
        return {
            "name": name,
            "output": {"name": "out", "type": "real"},
            "inputs": [],
            "inputs_update": [],
            "input_op": "*",
            "output_op": "last",
            "stack": [],
        }

    correctionlib.schemav2.CorrectionSet.parse_obj(
        {
            "schema_version": 2,
            "corrections": [make("thing1"), make("thing2")],
            "compound_corrections": [makec("thing1"), makec("thing2")],
        }
    )

    with pytest.raises(ValueError):
        correctionlib.schemav2.CorrectionSet.parse_obj(
            {"schema_version": 2, "corrections": [make("thing1"), make("thing1")]}
        )

    with pytest.raises(ValueError):
        correctionlib.schemav2.CorrectionSet.parse_obj(
            {
                "schema_version": 2,
                "corrections": [make("thing1"), make("thing1")],
                "compound_corrections": [makec("thing"), makec("thing")],
            }
        )
