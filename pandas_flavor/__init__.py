"""Top-level API for pandas-flavor."""
from .register import (
    register_dataframe_accessor,
    register_dataframe_method,
    register_series_accessor,
    register_series_method,
)
from .xarray import (
    register_xarray_dataarray_method,
    register_xarray_dataset_method,
)

__all__ = [
    "register_series_method",
    "register_series_accessor",
    "register_dataframe_method",
    "register_dataframe_accessor",
    "register_xarray_dataarray_method",
    "register_xarray_dataset_method",
]
