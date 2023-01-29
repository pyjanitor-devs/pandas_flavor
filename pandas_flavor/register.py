from functools import wraps
from pandas.api.extensions import register_series_accessor, register_dataframe_accessor
import inspect
from contextlib import nullcontext

method_call_ctx_factory = None

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

    method_signature = inspect.signature(method)

    def inner(*args, **kwargs):
        class AccessorMethod(object):
            def __init__(self, pandas_obj):
                self._obj = pandas_obj

            @wraps(method)
            def __call__(self, *args, **kwargs):
                global method_call_ctx_factory
                method_call_ctx = method_call_ctx_factory(method.__name__, args, kwargs) if method_call_ctx_factory else nullcontext()
                with method_call_ctx:
                    if not isinstance(method_call_ctx, nullcontext):
                        all_args = tuple([self._obj] + list(args))
                        new_args, new_kwargs = method_call_ctx.handle_start_method_call(method.__name__, method_signature, all_args, kwargs)
                        args = new_args[1:]; kwargs = new_kwargs

                    ret = method(self._obj, *args, **kwargs)

                    if not isinstance(method_call_ctx, nullcontext):
                        method_call_ctx.handle_end_method_call(ret)

                    return ret

        register_dataframe_accessor(method.__name__)(AccessorMethod)

        return method

    return inner()


def register_series_method(method):
    """Register a function as a method attached to the Pandas Series."""

    method_signature = inspect.signature(method)
    
    def inner(*args, **kwargs):
        class AccessorMethod(object):
            __doc__ = method.__doc__

            def __init__(self, pandas_obj):
                self._obj = pandas_obj

            @wraps(method)
            def __call__(self, *args, **kwargs):
                global method_call_ctx_factory
                method_call_ctx = method_call_ctx_factory(method.__name__, args, kwargs) if method_call_ctx_factory else nullcontext()
                with method_call_ctx:
                    if not isinstance(method_call_ctx, nullcontext):
                        all_args = tuple([self._obj] + list(args))
                        new_args, new_kwargs = method_call_ctx.handle_start_method_call(method.__name__, method_signature, all_args, kwargs)
                        args = new_args[1:]; kwargs = new_kwargs

                    ret = method(self._obj, *args, **kwargs)

                    if not isinstance(method_call_ctx, nullcontext):
                        method_call_ctx.handle_end_method_call(ret)

                    return ret

        register_series_accessor(method.__name__)(AccessorMethod)

        return method

    return inner()
