"""Register functions as methods of Pandas DataFrame and Series."""
from functools import wraps
from pandas.api.extensions import (
    register_series_accessor,
    register_dataframe_accessor,
)
import inspect

method_call_ctx_factory = None


def handle_pandas_extension_call(method, method_signature, obj, args, kwargs):
    """Handle pandas extension call.

    This function is called when the user calls
    a pandas DataFrame object's method.
    The pandas extension mechanism passes args and kwargs
    of the original method call as it is applied to obj.

    Our implementation uses the global variable `method_call_ctx_factory`.

    `method_call_ctx_factory` can be either None or an abstract class.

    When `method_call_ctx_factory` is None,
    the implementation calls the registered method
    with unmodified args and kwargs and returns underlying method result.

    When `method_call_ctx_factory` is not None,
    `method_call_ctx_factory` is expected to refer to
    the function to create the context object.
    The context object will be used to process
    inputs and outputs of `method` calls.
    It is also possible that
    the context object method `handle_start_method_call`
    will modify original args and kwargs before `method` call.

    `method_call_ctx_factory` is a function
    that should have the following signature:

     `f(method_name: str, args: list, kwargs: dict) -> MethodCallCtx`


    MethodCallCtx is an abstract class:
    class MethodCallCtx(abc.ABC):

        @abstractmethod
        def __enter__(self) -> None:
            raise NotImplemented

        @abstractmethod
        def __exit__(self, exc_type, exc_value, traceback) -> None:
            raise NotImplemented

        @abstractmethod
        def handle_start_method_call(self, method_name: str, method_signature: inspect.Signature, method_args: list, method_kwargs: dict) -> tuple(list, dict):
            raise NotImplemented

        @abstractmethod
        def handle_end_method_call(self, ret: object) -> None:
            raise NotImplemented


    Args:
        method (callable): method object as registered by decorator
            register_dataframe_method (or register_series_method)
        method_signature: signature of method as returned by inspect.signature
        obj: Dataframe or Series
        args: The arguments to pass to the registered method.
        kwargs: The keyword arguments to pass to the registered method.

    Returns:
        object`: The result of calling of the method.
    """  # noqa: E501

    global method_call_ctx_factory
    with method_call_ctx_factory(
        method.__name__, args, kwargs
    ) as method_call_ctx:
        if method_call_ctx is None:  # nullcontext __enter__ returns None
            ret = method(obj, *args, **kwargs)
        else:
            all_args = tuple([obj] + list(args))
            (
                new_args,
                new_kwargs,
            ) = method_call_ctx.handle_start_method_call(
                method.__name__, method_signature, all_args, kwargs
            )
            args = new_args[1:]
            kwargs = new_kwargs

            ret = method(obj, *args, **kwargs)

            method_call_ctx.handle_end_method_call(ret)

        return ret


def register_dataframe_method(method):
    """Register a function as a method attached to the Pandas DataFrame.

    Example:

        @register_dataframe_method
        def print_column(df, col):
            '''Print the dataframe column given'''
            print(df[col])

    Args:
        method (callable): callable to register as a dataframe method.

    Returns:
        callable: The original method.
    """

    method_signature = inspect.signature(method)

    def inner(*args, **kwargs):
        """Inner function to register the method.

        This function is called when the user
        decorates a function with register_dataframe_method.

        Args:
            *args: The arguments to pass to the registered method.
            **kwargs: The keyword arguments to pass to the registered method.

        Returns:
            method: The original method.
        """

        class AccessorMethod(object):
            """DataFrame Accessor method class."""

            def __init__(self, pandas_obj):
                """Initialize the accessor method class.

                Args:
                    pandas_obj (pandas.DataFrame): The pandas DataFrame object.
                """
                self._obj = pandas_obj

            @wraps(method)
            def __call__(self, *args, **kwargs):
                """Call the accessor method.

                Args:
                    *args: The arguments to pass to the registered method.
                    **kwargs: The keyword arguments to pass
                        to the registered method.

                Returns:
                    object: The result of calling of the method.
                """
                global method_call_ctx_factory
                if method_call_ctx_factory is None:
                    return method(self._obj, *args, **kwargs)

                return handle_pandas_extension_call(
                    method, method_signature, self._obj, args, kwargs
                )

        register_dataframe_accessor(method.__name__)(AccessorMethod)

        return method

    return inner()


def register_series_method(method):
    """Register a function as a method attached to the Pandas Series.

    Args:
        method (callable): callable to register as a series method.

    Returns:
        callable: The original method.
    """

    method_signature = inspect.signature(method)

    def inner(*args, **kwargs):
        """Inner function to register the method.

        Args:
            *args: The arguments to pass to the registered method.
            **kwargs: The keyword arguments to pass to the registered method.

        Returns:
            method: The original method.
        """

        class AccessorMethod(object):
            """Series Accessor method class."""

            __doc__ = method.__doc__

            def __init__(self, pandas_obj):
                """Initialize the accessor method class.

                Args:
                    pandas_obj (pandas.Series): The pandas Series object.
                """
                self._obj = pandas_obj

            @wraps(method)
            def __call__(self, *args, **kwargs):
                """Call the accessor method.

                Args:
                    *args: The arguments to pass to the registered method.
                    **kwargs: The keyword arguments to pass
                        to the registered method.

                Returns:
                    object: The result of calling of the method.
                """
                global method_call_ctx_factory
                if method_call_ctx_factory is None:
                    return method(self._obj, *args, **kwargs)

                return handle_pandas_extension_call(
                    method, method_signature, self._obj, args, kwargs
                )

        register_series_accessor(method.__name__)(AccessorMethod)

        return method

    return inner()
