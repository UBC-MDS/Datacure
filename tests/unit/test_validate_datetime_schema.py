import pandas as pd
import pytest
import pandas.testing as pdt

from datacure.validate_datetime_schema import validate_datetime_schema


# case 1: All datetime values are valid (with NA ignored), so validation should pass
def test_validate_datetime_schema_all_valid_pass():
    df = pd.DataFrame(
        {"date": ["2025-01-01", "2025-12-31", None]},
        index=[0, 2, 5])
    out = validate_datetime_schema(df, ["date"], "%Y-%m-%d", coerce_invalid=False)

    assert out["status"] == "pass"
    assert out["invalid_records"].empty


# case 2: A single invalid datetime value should be recorded with its index, column, and raw value
def test_validate_datetime_schema_single_invalid_records_row():
    df = pd.DataFrame(
        {"date": ["2025-01-01", "2025-13-01"]},
        index=[1, 3])
    out = validate_datetime_schema(df, ["date"], "%Y-%m-%d", coerce_invalid=False)

    assert out["status"] == "fail"
    inv = out["invalid_records"]
    assert len(inv) == 1
    assert inv.iloc[0]["index"] == 3
    assert inv.iloc[0]["column"] == "date"
    assert inv.iloc[0]["raw_value"] == "2025-13-01"


#case 3: With coercion enabled, uncoercible values should be logged as invalid and validated_df should be correctly coerced
def test_validate_datetime_schema_coerce_invalid_logs_uncoercible():
    df = pd.DataFrame(
        {"date": ["2025-01-01", "not-a-date", "2025-03-01"]},
        index=[0, 4, 6])

    out = validate_datetime_schema(df, ["date"], "%Y-%m-%d", coerce_invalid=True)

    expected_validated_df = pd.DataFrame(
        {"date": [pd.Timestamp("2025-01-01"), pd.NaT, pd.Timestamp("2025-03-01")]},
        index=[0, 4, 6],
    )

    expected_invalid_records = pd.DataFrame(
        {"index": [4], "column": ["date"], "raw_value": ["not-a-date"]}
    )

    assert out["status"] == "fail"
    assert out["validated_df"] is not df
    pdt.assert_frame_equal(
        out["validated_df"].astype("datetime64[ns]"),
        expected_validated_df.astype("datetime64[ns]")
    )
    pdt.assert_frame_equal(out["invalid_records"], expected_invalid_records)


# case 4: Referencing a non-existent column should raise a KeyError
def test_validate_datetime_schema_missing_column_raises_keyerror():
    df = pd.DataFrame(
        {"other": ["2025-01-01"]}, index=[0])
    with pytest.raises(KeyError):
        validate_datetime_schema(df, ["date"], "%Y-%m-%d")


# case 5: Using a different datetime_format argument should validate correctly
def test_validate_datetime_schema_different_datetime_format():
    df = pd.DataFrame(
        {"date": ["01/31/2025", "12/25/2025"]}, index=[1, 2])
    out = validate_datetime_schema(df, ["date"], "%m/%d/%Y")

    assert out["status"] == "pass"
    assert out["invalid_records"].empty



# case 6: Column specified for validation is not present in the DataFrame
def test_validate_datetime_schema_column_not_in_df_raises_error():
    df = pd.DataFrame(
        {"start_date": ["2025-01-01"]}, index=[0])
    with pytest.raises(KeyError):
        validate_datetime_schema(df, ["end_date"], "%Y-%m-%d")


# case 7: coerce_invalid=True should successfully convert all valid strings to datetime and return a correct DataFrame
def test_validate_datetime_schema_coerce_all_valid_outputs_correct_df():
    df = pd.DataFrame(
        {"date": ["2025-01-01", "2025-03-15", "2025-12-31", None]},
        index=[0, 2, 5, 9])

    out = validate_datetime_schema(df, ["date"], "%Y-%m-%d", coerce_invalid=True)

    expected_validated_df = pd.DataFrame(
        {
            "date": [
                pd.Timestamp("2025-01-01"),
                pd.Timestamp("2025-03-15"),
                pd.Timestamp("2025-12-31"),
                pd.NaT,  # NA should remain NA/NaT depending on implementation
            ]
        },
        index=[0, 2, 5, 9],
    )

    expected_validated_df["date"] = pd.to_datetime(expected_validated_df["date"])

    expected_invalid_records = pd.DataFrame(columns=["index", "column", "raw_value"])
    
    pdt.assert_frame_equal(
        out["validated_df"].astype("datetime64[ns]"),
        expected_validated_df.astype("datetime64[ns]")
    )
    pdt.assert_frame_equal(out["invalid_records"], expected_invalid_records)
    assert out["status"] == "pass"