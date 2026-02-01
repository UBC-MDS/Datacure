# Welcome to Datacure

|  |  |
|------------------------------------|------------------------------------|
| Documentation | [![Docs](https://img.shields.io/badge/docs-gh--pages-blue)](https://ubc-mds.github.io/DSCI_524_group20_datacure/) |
| CI/CD | [![CI](https://github.com/UBC-MDS/DSCI_524_group20_datacure/actions/workflows/build.yml/badge.svg)](https://github.com/UBC-MDS/DSCI_524_group20_datacure/actions/workflows/build.yml) [![codecov](https://codecov.io/github/ubc-mds/dsci_524_group20_datacure/branch/codecov_implementation/graph/badge.svg?token=qqHGXk6De9)](https://codecov.io/github/ubc-mds/dsci_524_group20_datacure)|
| Package | [![Test PyPI Version](https://img.shields.io/badge/TestPyPI-datacure-orange)](https://test.pypi.org/project/datacure/) [![Supported Python Versions](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/) |
| Meta | [![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](CODE_OF_CONDUCT.md) |


Datacure is a project designed to streamline data validation and cleaning process. It provides a multi-layered approach moving from high-level structural checks to granular value-level verification to achieve data integrity. By catching data errors early, it ensures the datasets is model-ready.

**Table Level Integrity**

Robustly load and clean tabular data from either a CSV file (via a local path or URL) or an existing pandas DataFrame. Evaluates the overall structure of the DataFrame to prevent downstream failures

-   `load_or_validate_source(df, source, expected_min_cols, sample_size)`
    - Input flexibility: Accepts either a CSV file (from a local path or URL) or an existing pandas DataFrame.
    - Automatic delimiter detection: For CSVs, detects the delimiter using a sample of the file and handles common formatting issues.
    - Corruption checks: Identifies inconsistencies such as mismatched column counts and ensures the first row is a proper header rather than data.
    - Column header cleaning: Strips leading and trailing whitespace, replaces internal spaces with underscores, substitutes illegal characters with underscores.
    - Data cleaning: Trims leading and trailing whitespace from all string values in the table.
    - Change reporting: Returns a ChangeReport object summarizing all modifications made during loading and cleaning.


**Categorical and Datetime Validation**

Evaluates whether categorical and datetime columns in a DataFrame conform to predefined schemas to prevent errors in analysis and modeling.

-   `validate_categorical_schema(df, column, allowed_categories)`
    - Checks whether all non-missing values in a categorical column belong to a predefined set of allowed categories.
    - Identifies and reports invalid category values at the row level.
    - Returns a pass/fail validation status along with a structured table of invalid records.


-   `validate_datetime_schema(df, columns, datetime_format, coerce_invalid=False)`
    - Checks whether datetime columns conform to a specified datetime format.
    - Identifies and reports invalid datetime values at the row level.
    -  Optionally (`coerce_invalid=True`) returns a copy of the DataFrame where valid values are converted to specified datetime type.

**Numeric EDA Plotting**

Provides a set of exploratory data analysis (EDA) focused on numeric columns. These functions will assist in quickly assessing distribution shapes, detect outliers and evaluate correlations

-   `plot_numeric_distributions(df)`
    - Generates histogram‑based distribution plots for all numeric columns.
    - Helps identify skewness, modality, and potential outliers across variables.


**Numeric value checks**

Numeric value checks ensure that numerical columns contain valid and meaningful values. These checks help detect outliers, impossible values, and violations of constraints that should logically apply to the data.
-  `validate_numeric_column(df, column, min_value,max_value,allow_negative)`
   - Verifys that numeric values fall within an expected range.
   - Detects negative values where they are not allowed
   - Identifies values that violate domain-specific boundaries.
   
While standard libraries like Pandas provide tools to transform data, **Datacure** provides the rules to validate it. By focusing on data cleaning - structural integrity, column consistency, and value range constraints - it allows developers to build more resilient data pipelines with less boilerplate code.

## Installation for Users
Install the package form Test PyPI running the below command in your terminal:
```bash
pip install -i https://test.pypi.org/simple/ datacure
```

## Setting up the Development Environment
1. Clone the repository to your local machine by opening your terminal and run the following commands:
``` bash
git clone https://github.com/UBC-MDS/DSCI_524_group20_datacure.git
cd DSCI_524_group20_datacure
``` 
2. Create the conda environment from `environment.yml`:
``` bash
conda env create -f environment.yml
```
3. Activate the environment:
``` bash
conda activate dsci_524_proj_env 
```

## Installing the package
You can install this package into your preferred Python environment using pip:
``` bash
pip install -e .
```

## Running Tests
You can run tests to validate all functions in the package using pytest:
``` bash
pytest -v
```
-v provides a verbose output showing the names of all tests and if they passed or not.

## Build Documentation
### Option 1 (Recommended): Build using Hatch
This option installs all required documentation dependencies automatically and builds the documentation:
``` bash
hatch run docs:build
```
### Option 2 (Optional): Live preview locally (requires Quarto installed)
If not already installed, you can install quarto from [link](https://quarto.org/docs/get-started/).
To generate the API reference pages and preview the documentation website run:
``` bash
quartodoc build --watch
quarto preview
```

## Example use:
``` python
import pandas as pd
from datacure import load_or_validate_source
from datacure import validate_datetime_schema
from datacure import validate_categorical_schema
from datacure import validate_numeric_column
from datacure import plots

df = pd.DataFrame({
    "#program": [" academic ", "general", "unknown", "special"],
    "start date": ["2023-01-01", "2023-02-01", "01-03-2023", "2023/04/01"],
    "duration": [12, 8, -5, 15]
})

# Load or Validate source
df, report = load_or_validate_source.load_or_validate_source(
    dataframe=df,
    expected_min_cols=3
)
print("Loaded DataFrame:")
print(df)
print("Change Report:")
print(report)

# Validate categorial schema
cat_result = validate_categorical_schema.validate_categorical_schema(
    df,
    column="program",
    allowed_categories=["academic", "general", "unknown", "special"]
)
print("Categorical Validation Result:")
print(cat_result)

# Validate datetime format
dt_result = validate_datetime_schema.validate_datetime_schema(
    df,
    columns=["start_date"],
    datetime_format="%Y-%m-%d"
)
print("Date Validation Result:")
print(dt_result)

# Validate numeric column
num_result = validate_numeric_column.validate_numeric_column(
    df,
    column="duration",
    min_value=0,
    max_value=24,
    allow_negative=False
)
print("Numeric Validation Result:")
print(num_result)

# Generate plots
plots.plot_numeric_distributions(df)
```

## Contributors
-   Jose Davila
-   Ssemakula Peter Wasswa
-   Yanxin Liang
-   Shruti Sasi

## Copyright
-   Copyright © 2026 Jose Davila , Ssemakula Peter Wasswa , Yanxin Liang , Shruti Sasi.
-   Free software distributed under the [MIT License](./LICENSE).
