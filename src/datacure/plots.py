import pandas as pd
import matplotlib.pyplot as plt
import math

def plot_numeric_distributions(df):
    """
    Plot distribution histograms for all numeric columns.

    Generates a grid of histogram plots to help visualize the
    distribution, skewness, and potential outliers in each
    numeric column. This function is intended as a exploratory 
    tool for understanding the shape of the data.

    Parameters
    ----------
    df : pandas.DataFrame
        The input dataset containing numeric columns.

    Returns
    -------
    None
        Displays histogram plots for each numeric column.

    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        raise ValueError("DataFrame contains no numeric columns")

    num_cols = numeric_df.shape[1]
    cols = math.ceil(math.sqrt(num_cols))
    rows = math.ceil(num_cols / cols)

    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows))
    axes = axes.flatten() if num_cols > 1 else [axes]

    for ax, column in zip(axes, numeric_df.columns):
        ax.hist(numeric_df[column].dropna(), bins=20)
        ax.set_title(column)

    # Remove unused subplots
    for ax in axes[num_cols:]:
        ax.remove()

    plt.tight_layout()
    plt.show()
