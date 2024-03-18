"""Tracing extension demo."""

import time

import pandas as pd

import pandas_flavor as pf


@pf.register_dataframe_method
def my_method(df: pd.DataFrame) -> pd.DataFrame:
    """Transpose the DataFrame.

    Args:
        df: The DataFrame to transpose.

    Returns:
        The transposed DataFrame.
    """
    print("my_method called")
    return df.transpose()


@pf.register_dataframe_method
def another_method(df: pd.DataFrame, new_col_d) -> pd.DataFrame:
    """Adds a new column to the DataFrame.

    Args:
        df (DataFrame): The DataFrame to add the column to.
        new_col_d (dict): A dictionary of column names and values.

    Returns:
        DataFrame: The DataFrame with the new column.
    """
    print("another_method called")
    for col, v in new_col_d.items():
        df[col] = v
    return df


class tracer:
    """A simple tracer for method calls."""

    @staticmethod
    def create_tracer(*args):
        """Creates a tracer.

        Args:
            *args: Variable length argument list for the tracer.

        Returns:
            The created tracer.
        """
        return tracer()

    def __init__(self):
        """Initialize the tracer."""
        self.method_name = None
        self.start_ts = None
        self.end_ts = None

    def __enter__(self):
        """Enter the tracer.

        Returns:
            The tracer.
        """
        return self

    def handle_start_method_call(
        self, method_name, method_signature, method_args, method_kwagrs
    ):
        """Handle the start of a method call.

        Args:
            method_name: The name of the method.
            method_signature: The signature of the method.
            method_args: The arguments of the method.
            method_kwagrs: The keyword arguments of the method.

        Returns:
            The arguments and keyword arguments of the method.
        """
        self.method_name = method_name
        self.start_ts = time.time()
        return method_args, method_kwagrs

    def handle_end_method_call(self, ret):
        """Handle the end of a method call.

        Args:
            ret: The return value of the method.
        """
        self.end_ts = time.time()

    def __exit__(self, exc_type, value, traceback):
        """Exit the tracer.

        Args:
            exc_type: The type of the exception.
            value: The value of the exception.
            traceback: The traceback of the exception.
        """
        call_dur = self.end_ts - self.start_ts
        print(f"method {self.method_name} took {call_dur} secs to execute")


pf.register.method_call_ctx_factory = tracer.create_tracer
s_df = pd.DataFrame([[i + j for i in range(10)] for j in range(10)])
res_df = s_df.my_method().another_method({"new_col": "new value"})
print(res_df)
