"""Tests for pandas series and dataframe method registration."""

import pandas_flavor as pf
import pandas as pd


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
