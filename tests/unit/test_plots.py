
from datacure.plots import plot_numeric_distributions

import pytest
import pandas as pd
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

def test_plot_numeric_distributions_valid_df():
    """ Test plotting only valid numeric columns."""
    df = pd.DataFrame({
        "a": [1, 2, 3],
        "b": [4.5, 5.5, 6.5],
        "c": ["x", "y", "z"]
    })
    
    plot_numeric_distributions(df)

    assert  len(plt.get_fignums())== 1
    plt.close("all")

def test_plot_numeric_distributions_non_df():
    """ Test error is raised if given non pandas dataframe as input"""
    with pytest.raises(TypeError):
        plot_numeric_distributions([1,2,3,"a"])


def test_plot_numeric_distributions_no_numeric_columns():
    """Test that error is raised when no numeric columns exist in input dataframe"""
    df = pd.DataFrame({
        "a": ["x", "y"],
        "b": ["c", "d"]
    })

    with pytest.raises(ValueError):
        plot_numeric_distributions(df)