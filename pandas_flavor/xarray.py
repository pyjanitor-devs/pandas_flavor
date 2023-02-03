"""XArray support for pandas_flavor."""
from xarray import register_dataarray_accessor, register_dataset_accessor
from functools import wraps


def make_accessor_wrapper(method):
    """
    Makes an XArray-compatible accessor to wrap a method to be added to an
    xr.DataArray, xr.Dataset, or both.

    Args:
        method: A method which takes an XArray object and needed parameters.

    Returns:
        The result of calling ``method``.
    """

    class XRAccessor:
        """XArray accessor for a method."""

        def __init__(self, xr_obj):
            """Initialize the accessor.

            Args:
                xr_obj: The XArray object to which the accessor is attached.
            """
            self._xr_obj = xr_obj

        @wraps(method)
        def __call__(self, *args, **kwargs):
            """Call the method.

            Args:
                *args: Positional arguments to pass to the method.
                **kwargs: Keyword arguments to pass to the method.

            Returns:
                The result of calling ``method``.
            """

            return method(self._xr_obj, *args, **kwargs)

    return XRAccessor


def register_xarray_dataarray_method(method: callable):
    """Register a method on an XArray DataArray object.

    Args:
        method: A method which takes an XArray object and needed parameters.

    Returns:
        The method.
    """
    accessor_wrapper = make_accessor_wrapper(method)
    register_dataarray_accessor(method.__name__)(accessor_wrapper)

    return method


def register_xarray_dataset_method(method: callable):
    """Register a method on an XArray Dataset object.

    Args:
        method: A method which takes an XArray object and needed parameters.

    Returns:
        The method.
    """

    accessor_wrapper = make_accessor_wrapper(method)
    register_dataset_accessor(method.__name__)(accessor_wrapper)

    return method
