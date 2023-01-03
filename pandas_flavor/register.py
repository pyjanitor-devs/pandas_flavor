import ipdb
from functools import wraps
import inspect
from pandas.api.extensions import register_series_accessor, register_dataframe_accessor
from . import stack_counter

handle_pandas_method_call = None

class LambdaCall:
    def __init__(self, func):
        self.func = func
        self.ret = None

    def __call__(self, *args, **kwargs):
        self.ret = self.func(*args, **kwargs)
        return self.ret

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
            def __call__(self, *args, **orig_kwargs):
                with stack_counter.global_scf.get_sc() as sc:
                    #ipdb.set_trace()
                    kwargs = {}
                    for k, arg in orig_kwargs.items():
                        if method.__name__ == 'assign' and inspect.isfunction(arg):
                            print('got got that')
                            #ipdb.set_trace()
                            kwargs[k] = LambdaCall(arg)
                        else:
                            kwargs[k] = arg

                    ret = method(self._obj, *args, **kwargs)

                    if sc.scf.level == 1:
                        #print("pf dataframe __call__")
                        global handle_pandas_method_call
                        if handle_pandas_method_call:
                            handle_pandas_method_call(self._obj, method.__name__, args, kwargs, ret)
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
                    ret = method(self._obj, *args, **kwargs)
                    if sc.scf.level <= 2:
                        #ipdb.set_trace()
                        print("pf series __call__")
                        global handle_pandas_method_call
                        if handle_pandas_method_call:
                            handle_pandas_method_call(self._obj, method.__name__, args, kwargs, ret)
                    return ret

        register_series_accessor(method.__name__)(AccessorMethod)

        return method

    return inner()
