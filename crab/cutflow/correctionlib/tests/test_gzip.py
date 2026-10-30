import gzip
import sys

import pytest

import correctionlib._core as core


def test_gzip(tmp_path):
    tmpname = str(tmp_path / "corr.json.gz")
    with gzip.open(tmpname, "wt") as fout:
        fout.write(
            '{"schema_version": 2, "description": "something", "corrections": []}'
        )

    if sys.platform.startswith("win"):
        with pytest.raises(RuntimeError):
            core.CorrectionSet.from_file(tmpname)
    else:
        core.CorrectionSet.from_file(tmpname)
