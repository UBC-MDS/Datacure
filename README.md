# Welcome to Datacure

|  |  |
|------------------------------------|------------------------------------|
| Package | [![Latest PyPI Version](https://img.shields.io/pypi/v/datacure.svg)](https://pypi.org/project/datacure/) [![Supported Python Versions](https://img.shields.io/pypi/pyversions/datacure.svg)](https://pypi.org/project/datacure/) |
| Meta | [![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](CODE_OF_CONDUCT.md) |

*TODO: the above badges that indicate python version and package version will only work if your package is on PyPI. If you don't plan to publish to PyPI, you can remove them.*

Datacure is a project designed to streamline data validation and cleaning process. It provides a multi-layered approach moving from high-level structural checks to granular value-level verification to achieve data integrity. By catching data errors early, it ensures the datasets is model-ready.

**Table Level Integrity**

Evaluates the overall structure of the DataFrame to prevent downstream failures

-   `check_table_structure` 
    - Detecting if the table is completely empty (no rows or no columns).
    - Checking column headers for spaces or special characters that may break code.
    - Identifying leading or trailing spaces within string cells across the table.
    - Flagging inconsistencies that indicate improper loading or formatting.


**Categorical and Datetime Validation**

Evaluates whether categorical and datetime columns in a DataFrame conform to predefined schemas to prevent errors in analysis and modeling.

-   `check_categories(df, column, allowed_categories)`
    - Validates that all values in a specified categorical column belong to a predefined set of allowed categories.
    - Reports invalid category values, their row indices, and a pass/fail status.

-   `check_datetime_format(df, columns, datetime_format)`
    - Validates that one or more datetime columns conform to a specified datetime format.
    - Returns either a success message or detailed diagnostics for columns that fail validation.


While standard libraries like Pandas provide tools to transform data, **Datacure** provides the rules to validate it. By focusing on data cleaning - structural integrity, column consistency, and value range constraints - it allows developers to build more resilient data pipelines with less boilerplate code.

## Get started

You can install this package into your preferred Python environment using pip:

``` bash
$ pip install datacure
```

TODO: Add a brief example of how to use the package to this section

To use datacure in your code:

``` python
import pandas as pd
from datacure import check_categories, check_datetime_format

df = pd.DataFrame({
    "program": ["academic", "general", "unknown"],
    "start_date": ["2023-01-01", "2023-02-01", "01-03-2023"]
})

# Check categorical column
result_categorical = check_categories(
    df, 
    column="program",
    allowed_categories=["academic", "general", "vocational"]
)

# Check datetime format
result_date = check_datetime_format(
    df,
    columns=["start_date"],
    datetime_format="%Y-%m-%d"
)
```

## Contributors

-   Jose Davila

-   Ssemakula Peter Wasswa

-   Yanxin Liang

-   Shruti Sasi

## Copyright

-   Copyright © 2026 Jose Davila , Ssemakula Peter Wasswa , Yanxin Liang , Shruti Sasi.
-   Free software distributed under the [MIT License](./LICENSE).