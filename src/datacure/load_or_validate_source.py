import io
import re
import csv
import requests
import pandas as pd
from dateutil.parser import parse
from pathlib import Path
from typing import Tuple, Optional
from dataclasses import dataclass, asdict

ILLEGAL_COLHD_PATTERN = re.compile(r"[^\w]")

class DataLoadError(Exception):
    pass

@dataclass
class ChangeReport:
    delimiter: Optional[str] = None
    columns_renamed: dict = None
    trimmed_cells: int = 0
    illegal_chars_fixed: int = 0
    shape_before: Tuple[int, int] = None
    shape_after: Tuple[int, int] = None

    def to_dict(self):
        return asdict(self)
    
#------------------------------------------------------------
# functions for internal use
def _read_text_from_source(source: str) -> str:
    """Read text from URL or local path."""
    
    # ---- HTTP / HTTPS ----
    if source.lower().startswith(("http://", "https://")):
        try:
            r = requests.get(source, timeout=10)
            r.raise_for_status()
            return r.text
        except Exception as e:
            raise DataLoadError(f"Unable to download file: {e}")

    # ---- Local file path ----
    path = Path(source)
    if path.exists():
        try:
            return path.read_text(encoding="utf-8")
        except Exception as e:
            raise DataLoadError(f"Unable to read local file: {e}")

    raise DataLoadError(
        "Source must be a valid http/https URL or existing file path"
    )

def _detect_delimiter(sample: str) -> str:
    try:
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(sample)
        return dialect.delimiter
    except Exception:
        return "," #fallback

def is_date(s):
    try:
        parse(s, fuzzy=False)
        return True
    except:
        return False
    
#------------------------------------------------------------

def load_or_validate_source(
        dataframe: Optional[pd.DataFrame] = None,
        source: Optional[str] = None,        
        expected_min_cols: int = 1,
        sample_size: int = 2048,
) -> Tuple[pd.DataFrame, ChangeReport]:
    """
    Load a CSV from a path/URL or validate and clean a provided DataFrame.

    Parameters
    ----------
    dataframe: pandas.DataFrame, optional
        An already-loaded DataFrame to validate and clean.  
    source : str, optional
        Path or URL to a CSV file.
        HTTP/HTTPS URLs and local filesystem paths are supported.           
    expected_min_cols : int, optional
        Minimum number of columns expected after loading (default: 2). Used to
        detect probable delimiter or corruption issues.
    sample_size : int, optional
        Number of characters to sample from the source when sniffing the
        delimiter and detecting basic corruption (default: 2048).

    Returns
    -------
    tuple[pandas.DataFrame, ChangeReport]
        df : pandas.DataFrame
            Cleaned and validated DataFrame. Cleaning includes normalizing
            column headers (strip, whitespace -> underscore, replace illegal
            chars with underscores) and trimming string cells.
        report : ChangeReport
            Report of changes and metadata (detected delimiter, renamed
            columns mapping, counts of trimmed cells and illegal-char fixes,
            shape before/after).

    Raises
    ------
    TypeError
        If `source` is neither a string nor a pandas.DataFrame.
    DataLoadError
        On I/O or parsing failures and validation errors, including:
        - unable to read/download source
        - inconsistent column counts in sample (possible corruption)
        - first row looks like data instead of header
        - pandas failed to parse CSV
        - resulting DataFrame is empty or has fewer than `expected_min_cols`

    Notes
    -----
    - Delimiter detection uses csv.Sniffer on a sample; falls back to ',' on failure.
    - When `source` is a DataFrame, it is copied and validated; no I/O is performed.

    Examples
    --------
    >>> df, rpt = load_or_validate_source(source="data.csv")
    >>> df, rpt = load_or_validate_source(dataframe=existing_df)
    """
    
    report = ChangeReport(columns_renamed = {})

    # LOAD
    if dataframe is not None:
        df = dataframe.copy()
        report.shape_before = df.shape

    elif source is not None:               
        # extracting a small preview of the downloaded file before processing
        text = _read_text_from_source(source)
        sample = text[:sample_size]

        # Auto detect delimiter
        delim = _detect_delimiter(sample)
        report.delimiter = delim
        print(f"Detected delimiter: '{delim}'")

        # Identify basic corruption
        lines = sample.splitlines()[:10]
        counts = [l.count(delim) for l in lines if l]
        print(delim, counts)
        if max(counts) - min(counts) > 2:
            raise DataLoadError("Inconsistent column counts - possible corruption")
        
        # First row header or data?
        # if any(ch.isdigit() for ch in lines[0]):            
        if any(ch.isdigit() for ch in lines[0]) or any(is_date(ch) for ch in lines[0].split(delim)):
            raise DataLoadError("First row looks like data instead of header")
        try:
            df = pd.read_csv(io.StringIO(text), delimiter=delim)
            report.shape_before = df.shape
        except Exception as e:
            raise DataLoadError(f"Pandas failed to read CSV: {e}")
        
    else:
        raise TypeError("source must be either URL/file path or DataFrame")
    
    # VALIDATIONS
    if df.empty:
        raise DataLoadError("DataFrame is empty")
    
    if df.shape[1] < expected_min_cols:
        raise DataLoadError("Too few columns - possible delimiter issue")
    
    # PRELIMINARY CLEANING
    new_cols = []
    illegal_fixes = 0

    for col in df.columns:
        orig = str(col)
        cleaned = orig.strip()
        cleaned = re.sub(r"\s+", "_", cleaned)
        fixed = ILLEGAL_COLHD_PATTERN.sub("", cleaned)
        if fixed != cleaned:
            illegal_fixes += 1

        if fixed != orig:
            report.columns_renamed[orig] = fixed

        new_cols.append(fixed)

    df.columns = new_cols
    report.illegal_chars_fixed = illegal_fixes

    # ---------- Trim table cell values ----------
    trimmed = 0
    for c in df.select_dtypes(include=["object", "string"]).columns:
        before = df[c].copy()
        #df[c] = df[c].astype(str).str.strip()
        df[c] = df[c].apply(lambda x: x.strip() if isinstance(x, str) else x)
        trimmed += (before != df[c]).sum()

    report.trimmed_cells = int(trimmed)
    report.shape_after = df.shape

    return df, report