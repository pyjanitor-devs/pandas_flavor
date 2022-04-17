"""Top-level API for pandas-flavor."""
import lazy_loader as lazy

__getattr__, __dir__, __all__ = lazy.attach(
    __name__,
    submod_attrs={
        "register": [
            "register_series_method",
            "register_series_accessor",
            "register_dataframe_method",
            "register_dataframe_accessor",
        ],
        "xarray": [
            "register_xarray_dataarray_method",
            "register_xarray_dataset_method",
        ],
    },
)
# from .register import (
#     register_series_method,
#     register_series_accessor,
#     register_dataframe_method,
#     register_dataframe_accessor,
# )
# from .xarray import (
#     register_xarray_dataarray_method,
#     register_xarray_dataset_method,
# )

# __all__ = [
#     "register_series_method",
#     "register_series_accessor",
#     "register_dataframe_method",
#     "register_dataframe_accessor",
#     "register_xarray_dataarray_method",
#     "register_xarray_dataset_method",
# ]
