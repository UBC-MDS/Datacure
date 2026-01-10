def check_categories(df, column, allowed_categories):
    """
    Validate that all values in a categorical column belong to a predefined set.

    This function performs a strict schema validation by checking whether all
    values in the specified categorical column are contained in the provided
    list of allowed categories.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the categorical column.
    column : str
        Name of the categorical column to validate.
    allowed_categories : list
        A list of allowed category values. 

    Returns
    -------
    dict
        A validation summary containing:
        - column: column name
        - allowed_categories: the provided allowed category list
        - invalid_values: unique values not in the allowed categories
        - invalid_rows: indices of rows with invalid categories
        - invalid_count: number of invalid rows
        - passed: whether the column passes the validation

    """
    pass




def check_datetime_format(df, columns, datetime_format):
    """
    Validate that datetime values in one or more columns follow a specific format.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the datetime column(s).
    columns : list of str
        a list of datetime column names to validate.
    datetime_format : str
        Expected datetime format (e.g., '%Y-%m-%d').

    Returns
    -------
    str or dict
        If all specified columns fully conform to the expected datetime format,
        returns a confirmation message:
            "All specified columns follow the expected datetime format."

        Otherwise, returns a dictionary keyed by column name. Each value contains
        a validation summary for that column:
        - invalid_rows: indices of rows that fail format validation
        - invalid_count: number of invalid rows
        - valid_ratio: proportion of successfully parsed values
    """
    pass
