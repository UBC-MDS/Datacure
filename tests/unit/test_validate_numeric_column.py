import pandas as pd
import pytest

from datacure.validate_numeric_column import validate_numeric_column


def test_validate_numeric_column_returns_empty_when_no_violations():
    df = pd.DataFrame({"x": [1, 2, 3]})
    out = validate_numeric_column(df, "x", min_value=1, max_value=3, allow_negative=True)
    assert isinstance(out, pd.DataFrame)
    assert out.empty


def test_validate_numeric_column_flags_out_of_range_values():
    df = pd.DataFrame({"x": [0, 5, 10]})
    out = validate_numeric_column(df, "x", min_value=1, max_value=9, allow_negative=True)
    # should flag rows with 0 and 10
    assert len(out) == 2
    assert "violation_reason" in out.columns
    assert set(out["x"].tolist()) == {0, 10}


def test_validate_numeric_column_flags_negative_values_when_not_allowed():
    df = pd.DataFrame({"x": [-1, 0, 1]})
    out = validate_numeric_column(df, "x", allow_negative=False)
    assert len(out) == 1
    assert out["x"].iloc[0] == -1
    assert "negative" in out["violation_reason"].iloc[0].lower()


def test_validate_numeric_column_ignores_missing_values():
    df = pd.DataFrame({"x": [1.0, None, 3.0]})
    out = validate_numeric_column(df, "x", min_value=0, max_value=5, allow_negative=True)
    assert out.empty


def test_validate_numeric_column_raises_for_missing_column():
    df = pd.DataFrame({"x": [1, 2, 3]})
    with pytest.raises(KeyError):
        validate_numeric_column(df, "y")


def test_validate_numeric_column_raises_for_non_numeric_column():
    df = pd.DataFrame({"x": ["a", "b"]})
    with pytest.raises(TypeError):
        validate_numeric_column(df, "x", min_value=0, max_value=10)
