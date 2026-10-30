import math
import pickle

import correctionlib
import correctionlib.schemav2


def test_compound():
    cset = correctionlib.schemav2.CorrectionSet.parse_obj(
        {
            "schema_version": 2,
            "corrections": [
                {
                    "name": "level1",
                    "description": "something flat",
                    "inputs": [],
                    "output": {"name": "l1sf", "type": "real"},
                    "version": 1,
                    "data": 1.1,
                },
                {
                    "name": "level2",
                    "description": "something that depends on pt and eta",
                    "inputs": [
                        {"name": "pt", "type": "real"},
                        {"name": "eta", "type": "real"},
                    ],
                    "output": {"name": "l2sf", "type": "real"},
                    "version": 1,
                    "data": {
                        "nodetype": "formula",
                        "parser": "TFormula",
                        "variables": ["pt", "eta"],
                        "expression": "1 + 0.1*log10(x) + 0.1*y",
                    },
                },
            ],
            "compound_corrections": [
                {
                    "name": "l1l2",
                    "output": {"name": "sf", "type": "real"},
                    "inputs": [
                        {"name": "pt", "type": "real"},
                        {"name": "eta", "type": "real"},
                    ],
                    "inputs_update": ["pt"],
                    "input_op": "*",
                    "output_op": "last",
                    "stack": ["level1", "level2"],
                },
                {
                    "name": "multiplied",
                    "output": {"name": "sf", "type": "real"},
                    "inputs": [
                        {"name": "eta", "type": "real"},
                        {"name": "pt", "type": "real"},
                    ],
                    "inputs_update": [],
                    "input_op": "*",
                    "output_op": "*",
                    "stack": ["level2", "level1"],
                },
            ],
        }
    )
    cset = correctionlib.CorrectionSet.from_string(cset.json())
    corr = cset.compound["l1l2"]
    assert corr.evaluate(10.0, 1.2) == 1 + 0.1 * math.log10(10 * 1.1) + 0.1 * 1.2
    assert corr.evaluate(10.0, 0.0) == 1 + 0.1 * math.log10(10 * 1.1)

    corr = cset.compound["multiplied"]
    assert corr.evaluate(1.2, 10.0) == 1.1 * (1 + 0.1 * math.log10(10) + 0.1 * 1.2)
    assert corr.evaluate(0.0, 10.0) == (1 + 0.1 * math.log10(10)) * 1.1

    corr2 = pickle.loads(pickle.dumps(corr))
    assert corr2.evaluate(0.0, 10.0) == (1 + 0.1 * math.log10(10)) * 1.1
