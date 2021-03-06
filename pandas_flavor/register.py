from functools import wraps
from .pandas_internals import (register_series_accessor,
                              register_dataframe_accessor)
from pandas.core.frame import DataFrame


def register_dataframe_method(method):
    """Register a function as a method attached to the Pandas DataFrame.

    Example
    -------

    .. code-block:: python

        @register_dataframe_method
        def print_column(df, col):
            '''Print the dataframe column given'''
            print(df[col])
    """
    def inner(*args, **kwargs):

        class AccessorMethod(object):


            def __init__(self, pandas_obj):
                self._obj = pandas_obj

            @wraps(method)
            def __call__(self, *args, **kwargs):
                return method(self._obj, *args, **kwargs)

        register_dataframe_accessor(method.__name__)(AccessorMethod)

        return method

    return inner()


def register_series_method(method):
    """Register a function as a method attached to the Pandas Series.
    """
    def inner(*args, **kwargs):
        class AccessorMethod(object):
            __doc__ = method.__doc__

            def __init__(self, pandas_obj):
                self._obj = pandas_obj

            @wraps(method)
            def __call__(self, *args, **kwargs):
                return method(self._obj, *args, **kwargs)

        register_series_accessor(method.__name__)(AccessorMethod)

        return method

    return inner()


def register_series_and_dataframe_method(_func=None, **decorator_kwargs):
    """Register a function as a method attached to the Pandas Series or DataFrame
    Method should be written as a function to apply on each column or each row

    Can optionally include arguments to pass to pd.DataFrame.apply() such as axis=1

    Please note that if the operation can be vectorized, register_dataframe_method will
    likely yield higher performance as this decorator will always use pd.DataFrame.apply()

    Example
    -------

    .. code-block:: python

        @register_series_method
        def total_pct_change(df):
            return (df.iloc[-1] - df.iloc[0]) / df.iloc[0]
    """
    def inner_wrapper(method):
        def inner(*args, **kwargs):
            class SerAccessorMethod(object):
                __doc__ = method.__doc__

                def __init__(self, pandas_obj):
                    self._obj = pandas_obj

                @wraps(method)
                def __call__(self, *args, **kwargs):
                    return method(self._obj, *args, **kwargs)

            class DFAccessorMethod(object):
                __doc__ = method.__doc__

                def __init__(self, pandas_obj):
                    self._obj = pandas_obj

                @wraps(method)
                def __call__(self, *args, **kwargs):
                    kwargs = {**decorator_kwargs, **kwargs}
                    return DataFrame.apply(self._obj, method, args=args, **kwargs)

            register_series_accessor(method.__name__)(SerAccessorMethod)
            register_dataframe_accessor(method.__name__)(DFAccessorMethod)

            return method

        return inner()

    if _func is None:
        return inner_wrapper
    else:
        return inner_wrapper(_func)