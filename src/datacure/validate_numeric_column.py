import pandas as pd
from typing import Optional


def validate_numeric_column(
    df: pd.DataFrame,
    column: str,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    allow_negative: bool = True
):
    """
    Validate a numeric column against logical and domain-specific constraints.

    This function performs diagnostic checks on a specified numeric column
    in a pandas DataFrame. It identifies values that fall outside an expected
    range or violate negative-value rules. The function does not modify the
    original DataFrame; instead, it returns a new DataFrame containing only
    the rows where violations occurred, along with a textual description of
    the issue found. This makes the function suitable for automated data
    validation pipelines, testing, and reporting.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing the numeric column to check.

    column : str
        The name of the numeric column to be validated. The function will
        raise a KeyError if this column is not found in the DataFrame.

    min_value : float, optional
        The minimum allowed value (inclusive). If provided, any value in the
        column that is strictly less than this threshold is considered a
        violation.

    max_value : float, optional
        The maximum allowed value (inclusive). If provided, any value in the
        column that is strictly greater than this threshold is considered a
        violation.

    allow_negative : bool, default=True
        When set to False, any negative numeric value will be treated as a
        violation, regardless of the specified `min_value`.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing all rows where at least one validation rule
        was broken. The returned DataFrame will contain all original columns
        plus an additional column named `"violation_reason"` describing the
        type of constraint that was violated. If the column contains no
        invalid values, an empty DataFrame is returned.

    Raises
    ------
    KeyError
        If the specified `column` is not present in the input DataFrame.

    TypeError
        If the specified column cannot be interpreted as numeric
        (e.g., contains non-numeric strings).

    Examples
    --------
    >>> violations = validate_numeric_column(
    ...     df,
    ...     column="age",
    ...     min_value=0,
    ...     max_value=120,
    ...     allow_negative=False
    ... )
    >>> violations.empty
    True

    Notes
    -----
    - This function is purely diagnostic and performs no in-place modification.
    - It is designed to be simple to test using small DataFrames with known
      invalid values.
    """
    pass
