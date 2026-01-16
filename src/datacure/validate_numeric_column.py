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
     # --- Defensive checks ---
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame.")

    if column not in df.columns:
        raise KeyError(f"Column '{column}' not found in DataFrame.")

    # Check that the column is numeric
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise TypeError(
            f"Column '{column}' must be numeric, "
            f"but has dtype {df[column].dtype}."
        )

    # Work on a copy of the column to avoid modifying df
    series = df[column]

    # Ignore missing values
    non_missing = series.dropna()

    # --- Build violation masks ---
    violation_reasons = {}

    if not allow_negative:
        neg_mask = non_missing < 0
        violation_reasons["negative"] = neg_mask

    if min_value is not None:
        min_mask = non_missing < min_value
        violation_reasons["below_min"] = min_mask

    if max_value is not None:
        max_mask = non_missing > max_value
        violation_reasons["above_max"] = max_mask

    if not violation_reasons:
        # No rules to validate against
        return pd.DataFrame(columns=list(df.columns) + ["violation_reason"])

    # Combine all violation masks
    combined_mask = pd.Series(False, index=non_missing.index)
    for mask in violation_reasons.values():
        combined_mask = combined_mask | mask

    violating_indices = combined_mask[combined_mask].index

    if len(violating_indices) == 0:
        return pd.DataFrame(columns=list(df.columns) + ["violation_reason"])

    # --- Build violation_reason column ---
    reasons = []
    for idx in violating_indices:
        row_reasons = []
        value = series.loc[idx]

        if not allow_negative and value < 0:
            row_reasons.append("negative value not allowed")

        if min_value is not None and value < min_value:
            row_reasons.append(f"value below minimum ({min_value})")

        if max_value is not None and value > max_value:
            row_reasons.append(f"value above maximum ({max_value})")

        reasons.append("; ".join(row_reasons))

    # --- Construct output DataFrame ---
    violations_df = df.loc[violating_indices].copy()
    violations_df["violation_reason"] = reasons

    return violations_df
