import pytest
import pandas as pd
from io import StringIO
from pathlib import Path
from unittest.mock import patch
from datacure.load_or_validate_source import load_or_validate_source, DataLoadError

DATA_DIR = Path(__file__).parent / "../data"

# -------------------- HELPER --------------------
def get_path(filename):
    return str(DATA_DIR / filename)


# -------------------- TESTS --------------------
def test_exception_no_source_or_df():
    """If neither dataframe nor source is provided, it should raise error."""
    with pytest.raises(TypeError, match="source must be either URL/file path or DataFrame"):
        load_or_validate_source()

def test_dataframe_overrides_url():
    """If a dataframe is provided, it should be used even if URL is passed."""
    df_input = pd.DataFrame({"A": [1, 2]})
    df, rpt = load_or_validate_source(source="http://fakeurl.com/file.csv",dataframe=df_input)
    assert df.equals(df_input)
    assert rpt.shape_before == (2, 1)

# def test_download_file_mock(monkeypatch):
#     """Check if code can 'download' a file from URL (mocked)."""
#     sample_path = get_path("good.csv")
#     with patch("datacure.load_or_validate_source._read_text_from_source") as mock_read:
#         mock_read.return_value = open(sample_path).read()
#         df, rpt = load_or_validate_source(source="http://fakeurl.com/file.csv")
#         assert not df.empty
#         assert rpt.delimiter == ","

def test_access_file_path():
    """Check if code can 'access' a file from file path."""
    sample_path = get_path("good.csv")
    df, rpt = load_or_validate_source(source=sample_path)
    assert not df.empty
    assert rpt.delimiter == ","

def test_access_unsupported_file_type():
    """Check if code returns error for unsupported file type."""
    sample_path = get_path("excel_data.xlsx")
    with pytest.raises(DataLoadError, match="Unable to read local file"):
        load_or_validate_source(source=sample_path)
   
def test_download_file():
    """Check if code can 'download' a file from URL"""
    df, rpt = load_or_validate_source(source="https://raw.githubusercontent.com/ttimbers/canlang/master/inst/extdata/victoria_lang.tsv")
    assert not df.empty
    assert rpt.delimiter == "\t"

def test_download_from_non_existent_url():
    """Check if code can 'download' a file from non existing URL"""
    with pytest.raises(DataLoadError, match="Unable to download file"):
        load_or_validate_source(source="https://testurl")

def test_delimiter_detection():
    """Check that non-comma delimiters are detected correctly."""
    sample_path = get_path("delimiter_pipe.csv")
    df, rpt = load_or_validate_source(source=sample_path)
    assert rpt.delimiter == "|"
    assert df.shape[1] > 1


def test_column_count_inconsistent():
    """Check for DataLoadError if columns are inconsistent."""
    sample_path = get_path("shifted_columns.csv")
    with pytest.raises(DataLoadError, match="Inconsistent column counts"):
        load_or_validate_source(source=sample_path)


def test_empty_dataframe_or_file():
    """Check error when source is empty."""
    sample_path = get_path("empty.csv")
    with pytest.raises(DataLoadError, match="empty"):
        load_or_validate_source(source=sample_path)
    empty_df = pd.DataFrame()
    with pytest.raises(DataLoadError, match="empty"):
        load_or_validate_source(dataframe=empty_df)


def test_no_header_row():
    """Check error when first row looks like data."""
    sample_path = get_path("no_header_delimiter_tab.csv")
    with pytest.raises(DataLoadError, match="First row looks like data"):
        load_or_validate_source(source=sample_path)


def test_illegal_char_and_whitespace_in_header():
    """Check header cleaning."""
    sample_path = get_path("illegal_header.csv")
    df, rpt = load_or_validate_source(source=sample_path)    
    # Original headers should be mapped in report
    assert "  #lang known  " in rpt.columns_renamed
    assert df.columns[7] == "lang_known"  # internal space replaced, illegal chars -> _
    # Leading/trailing spaces removed
    for col in df.columns:
        assert not col.startswith(" ")
        assert not col.endswith(" ")


def test_internal_space_replaced_with_underscore():
    sample_path = get_path("illegal_header.csv")
    df, rpt = load_or_validate_source(source=sample_path)
    # Internal spaces in header replaced
    assert "most_at_work" in df.columns or "most_at_home" in df.columns


def test_trim_data_cells():
    sample_path = get_path("illegal_header.csv")
    df, rpt = load_or_validate_source(source=sample_path)
    # Leading/trailing spaces removed from cell values
    for col in df.select_dtypes(include=["object"]).columns:
        for val in df[col]:
            assert val == val.strip()