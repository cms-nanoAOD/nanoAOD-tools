import pytest

from correctionlib._core import CorrectionSet


def test_evaluator_validation():
    bad_json = [
        '{"schema_version":2, "corrections": [9]}',
        '{"schema_version":2, "corrections": [{}]}',
        '{"schema_version":2, "corrections": [{"name": 3}]}',
        '{"schema_version":2, "corrections": [{"name": "hi"}]}',
        '{"schema_version":2, "corrections": [{"name": "hi", "version": 1}]}',
        '{"schema_version":2, "corrections": [{"name": "hi", "version": "3"}]}',
        '{"schema_version":2, "corrections": [{"name": "hi", "version": 2}]}',
        '{"schema_version":2, "corrections": [{"name": "hi", "version": 2, "output": 3}]}',
        '{"schema_version":2, "corrections": [{"name": "hi", "version": 2, "output": []}]}',
        '{"schema_version":2, "corrections": [{"name": "hi", "version": 2, "output": {}}]}',
        '{"schema_version":2, "corrections": [{"name": "hi", "version": 2, "output": {"name": "hi"}}]}',
        '{"schema_version":2, "corrections": [{"name": "hi", "version": 2, "output": {"name": "hi","type": 2}}]}',
        '{"schema_version":2, "corrections": [{"name": "hi", "version": 2, "output": {"name": "hi","type": "s"}}]}',
        '{"schema_version":2, "corrections": [{"name": "hi", "version": 2, "output": {"name": "hi","type": "str"}}]}',
        '{"schema_version":2, "corrections": [{"name": "hi", "version": 2, "output": {"name": "hi","type": "string"}}]}',
        '{"schema_version":2, "corrections": [{"name": "hi", "version": 2, "output": {"name": "hi","type": "string", "description": 3}}]}',
        '{"schema_version":2, "corrections": [{"name": "hi", "version": 2, "output": {"name": "hi","type": "string", "description": null}}]}',
        '{"schema_version":2, "corrections": [{"name": "hi", "version": 2, "output": {"name": "hi","type": "string"}}]}',
        '{"schema_version":2, "corrections": [{"name": "hi", "version": 2, "output": {"name": "hi","type": "string"}, "inputs": []}]}',
        '{"schema_version":2, "corrections": [{"name": "hi", "version": 2, "output": {"name": "hi","type": "string"}, "inputs": [], "data": 1}]}',
        '{"schema_version":2, "corrections": [{"name": "hi", "version": 2, "output": {"name": "hi","type": "real"}, "inputs": [], "data": 1}]}',
        '{"schema_version":2, "corrections": [{"name": "hi", "version": 2, "output": {"name": "hi","type": "real"}, "inputs": [], "data": {"nodetype": 3}}]}',
        '{"schema_version":2, "corrections": [{"name": "hi", "version": 2, "output": {"name": "hi","type": "real"}, "inputs": [], "data": {"nodetype": "blah"}}]}',
        '{"schema_version":2, "corrections": [{"name": "hi", "version": 2, "output": {"name": "hi","type": "real"}, "inputs": [], "data": {"nodetype": "category", "input": "blah"}}]}',
        '{"schema_version":2, "corrections": [{"name": "hi", "version": 2, "output": {"name": "hi","type": "real"}, "inputs": [{"name":"blah", "type": "int"}], "data": {"nodetype": "category", "input": "blah", "content": [3]}}]}',
        '{"schema_version":2, "corrections": [{"name": "hi", "version": 2, "output": {"name": "hi","type": "real"}, "inputs": [{"name":"blah", "type": "int"}], "data": {"nodetype": "category", "input": "blah", "content": [{"key": null, "value": 3}]}}]}',
        '{"schema_version":2, "corrections": [{"name": "hi", "version": 2, "output": {"name": "hi","type": "real"}, "inputs": [{"name":"blah", "type": "int"}], "data": {"nodetype": "category", "input": "blah", "content": [{"key": 1.2, "val": 3}]}}]}',
        '{"schema_version":2, "corrections": [{"name": "hi", "version": 2, "output": {"name": "hi","type": "real"}, "inputs": [{"name":"blah", "type": "int"}], "data": {"nodetype": "category", "input": "blah", "content": [{"key": "a", "value": 3.0}]}}]}',
        '{"schema_version":2, "corrections": [{"name": "hi", "version": 2, "output": {"name": "hi","type": "real"}, "inputs": [{"name":"blah", "type": "int"}], "data": {"nodetype": "category", "input": "blah", "content": [{"key": 1, "value": 3.0}], "default": "f"}}]}',
        '{"schema_version":2, "corrections": [{"name": "hi", "version": 2, "output": {"name": "hi","type": "real"}, "inputs": [{"name":"blah", "type": "int"}], "data": {"nodetype": "formula"}}]}',
    ]

    for json in bad_json:
        with pytest.raises(RuntimeError):
            CorrectionSet.from_string(json)
