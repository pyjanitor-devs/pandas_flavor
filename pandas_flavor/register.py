import ipdb
from functools import wraps
from pandas.api.extensions import register_series_accessor, register_dataframe_accessor
from . import stack_counter

start_method_call = None

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
                with stack_counter.global_scf.get_sc() as sc:
                    #ipdb.set_trace()
                            
                    method_call_obj = None
                    if sc.scf.level == 1:
                        global start_method_call
                        if start_method_call:
                            method_call_obj = start_method_call(self._obj, method.__name__, args, kwargs)
                    
                    ret = method(self._obj, *args, **kwargs)

                    if method_call_obj:
                        method_call_obj.handle_end_method_call(ret)
                    
                    return ret

        register_dataframe_accessor(method.__name__)(AccessorMethod)

        return method

    return inner()


def register_series_method(method):
    """Register a function as a method attached to the Pandas Series."""

    def inner(*args, **kwargs):
        class AccessorMethod(object):
            __doc__ = method.__doc__

            def __init__(self, pandas_obj):
                self._obj = pandas_obj

            @wraps(method)
            def __call__(self, *args, **kwargs):
                with stack_counter.global_scf.get_sc() as sc:
                    method_call_obj = None
                    if sc.scf.level <= 2:
                        global start_method_call
                        if start_method_call:
                            method_call_obj = start_method_call(self._obj, method.__name__, args, kwargs)
                            
                    ret = method(self._obj, *args, **kwargs)

                    if method_call_obj:
                        method_call_obj.handle_end_method_call(ret)
                        
                    return ret

        register_series_accessor(method.__name__)(AccessorMethod)

        return method

    return inner()
