import pandas as pd


def validate_categorical_schema(df, column, allowed_categories):
    """
    Validate that a categorical column conforms to a predefined allowed-value schema.

    This function checks whether all non-missing values in ``df[column]`` are
    contained in ``allowed_categories``. Missing values (NaN/None) are ignored.
    Values not in ``allowed_categories`` are reported in ``invalid_records``.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the categorical column.
    column : str
        Name of the categorical column to validate.
    allowed_categories : Sequence
        An iterable of allowed category values (e.g., list, set, tuple).

    Returns
    -------
    dict
        A validation summary containing:

        status : {'pass', 'fail'}
            Overall validation status.
        invalid_records : pandas.DataFrame
            A DataFrame with columns ['index', 'column', 'raw_value'].
    """

    # check input
    if df is None or df.empty:
        raise ValueError("`df` must be a non-empty pandas DataFrame.")

    if column is None or not isinstance(column, str) or column.strip() == "":
        raise ValueError("`column` must be a non-empty string.")

    if allowed_categories is None or len(allowed_categories) == 0:
        raise ValueError("`allowed_categories` must be a non-empty sequence.")

    if column not in df.columns:
        raise KeyError(f"Column '{column}' not found in DataFrame")

    allowed_set = set(allowed_categories)
    invalid_rows = []

    # validate values 
    for idx, value in df[column].items():
        if pd.isna(value):
            continue
        if value not in allowed_set:
            invalid_rows.append({"index": idx, 
                                 "column": column, 
                                 "raw_value": value})

    invalid_records = pd.DataFrame(invalid_rows, 
                                   columns=["index", "column", "raw_value"])
    status = "pass" if invalid_records.empty else "fail"

    return {
        "status": status,
        "invalid_records": invalid_records,
    }