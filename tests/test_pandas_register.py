"""Tests for pandas series and dataframe method registration."""

import pandas_flavor as pf
import pandas as pd
from pandas.core.groupby.generic import DataFrameGroupBy


def test_register_dataframe_method():
    """Test register_dataframe_method."""

    @pf.register_dataframe_method
    def dummy_func(df: pd.DataFrame) -> pd.DataFrame:
        """Dummy function.

        Args:
            df: a pandas DataFrame

        Returns:
            df: A pandas DataFrame.
        """
        return df

    df = pd.DataFrame()
    df.dummy_func()


def test_register_series_method():
    """Test register_series_method."""

    @pf.register_series_method
    def dummy_func(s: pd.Series) -> pd.Series:
        """Dummy func.

        Args:
            s: A pandas Series.

        Returns:
            s: A pandas Series.
        """
        return s

    ser = pd.Series()
    ser.dummy_func()


def test_register_groupby_method():
    """Test register_groupby_method."""

    @pf.register_groupby_method
    def dummy_func(by: DataFrameGroupBy) -> DataFrameGroupBy:
        """Dummy func.

        Args:
            by: A DataFrameGroupBy object.

        Returns:
            DataFrameGroupBy.
        """
        return by

    df = pd.DataFrame(
        {
            "Animal": ["Falcon"],
            "Max Speed": [380.0],
        }
    )
    by = df.groupby("Animal")
    by.dummy_func()
