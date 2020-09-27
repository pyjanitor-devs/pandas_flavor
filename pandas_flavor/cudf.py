from functools import wraps

from cudf.api.extensions import (
    register_dataframe_accessor,
    register_series_accessor
)


def register_cudf_method(method):
    """Register a function as a method attached to the cuDF DataFrame.

    Example
    -------

    .. code-block:: python

        @register_cudf_method
        def print_column(df, col):
            '''Print the dataframe column given'''
            print(df[col])
    """

    def inner(*args, **kwargs):
        class AccessorMethod(object):
            def __init__(self, cudf_obj):
                self._obj = cudf_obj

            @wraps(method)
            def __call__(self, *args, **kwargs):
                return method(self._obj, *args, **kwargs)

        register_dataframe_accessor(method.__name__)(AccessorMethod)

        return method

    return inner()


def register_cuseries_method(method):
    """Register a function as a method attached to the cuDF Series."""

    def inner(*args, **kwargs):
        class AccessorMethod(object):
            __doc__ = method.__doc__

            def __init__(self, cudf_obj):
                self._obj = cudf_obj

            @wraps(method)
            def __call__(self, *args, **kwargs):
                return method(self._obj, *args, **kwargs)

        register_series_accessor(method.__name__)(AccessorMethod)

        return method

    return inner()
