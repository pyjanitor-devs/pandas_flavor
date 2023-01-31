from functools import wraps
from pandas.api.extensions import (
    register_series_accessor,
    register_dataframe_accessor,
)
import inspect
from contextlib import nullcontext

method_call_ctx_factory = None


def handle_pandas_extention_call(method, method_signature, obj, args, kwargs):
    """
    This function is called when the user calls the registered method on pandas dataframe object.
    pandas extention mechanism passes args and kwargs of original method call as it was applied to obj

    Implementation uses global var *method_call_ctx_factory"

    a) case when *method_call_ctx_factory* is None
    In this case the implementation calls the registered method with unmodified args and kwargs and returns underlying method result.

    b) case when *method_call_ctx_factory* is not None
    In this case *method_call_ctx_factory* expected to refer to the function to create the context object. The context object will be used
    to process inputs and outputs of *method* call. It is also possible that the context object method *handle_start_method_call*
    will modify original args and kwargs before *method* call.

    method_call_ctx_factory function signature: (method_name: str, args: list, kwargs: dict) -> MethodCallCtx

    MethodCallCtx is an abstract class:
    class MethodCallCtx(abc.ABC):
        @abstractmethod
        def __enter__(self) -> None: raise NotImplemented
        @abstractmethod
        def __exit__(self, exc_type, exc_value, traceback) -> None: raise NotImplemented
        @abstractmethod
        def handle_start_method_call(self, method_name: str, method_signature: inspect.Signature, method_args: list, method_kwargs: dict) -> tuple(list, dict): raise NotImplemented
        @abstractmethod
        def handle_end_method_call(self, ret: object) -> None: raise NotImplemented


    Parameters
    ----------
    method :
        method object as registered by decorator register_dataframe_method (or register_series_method)
    method_signature :
        signature of method as returned by inspect.signature
    obj :
        pandas object - Dataframe or Series
    *args : list
        The arguments to pass to the registered method.
    **kwargs : dict
        The keyword arguments to pass to the registered method.

    Returns
    -------
    object :
        The result of calling of the method.
    """

    global method_call_ctx_factory

    method_call_ctx = (
        method_call_ctx_factory(method.__name__, args, kwargs)
        if method_call_ctx_factory
        else nullcontext()
    )

    with method_call_ctx:
        if not isinstance(method_call_ctx, nullcontext):
            all_args = tuple([obj] + list(args))
            (new_args, new_kwargs,) = method_call_ctx.handle_start_method_call(
                method.__name__, method_signature, all_args, kwargs
            )
            args = new_args[1:]
            kwargs = new_kwargs

        ret = method(obj, *args, **kwargs)

        if not isinstance(method_call_ctx, nullcontext):
            method_call_ctx.handle_end_method_call(ret)

        return ret


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
                return handle_pandas_extention_call(
                    method, method_signature, self._obj, args, kwargs
                )

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
                return handle_pandas_extention_call(
                    method, method_signature, self._obj, args, kwargs
                )

        register_series_accessor(method.__name__)(AccessorMethod)

        return method

    return inner()
