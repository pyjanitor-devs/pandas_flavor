try:
    # Import register decorators from pandas >= 0.23
    from pandas.api.extensions import (register_dataframe_accessor,
                                       register_series_accessor)
except ImportError:
    from pandas import DataFrame, Series

    try:
        from pandas.core.accessor import AccessorProperty
    except ImportError:  # Pandas before 0.22.0
        from pandas.core.base import AccessorProperty

    # Define register decorators for pandas < 0.23
    class register_dataframe_accessor(object):
        """Register custom accessor on DataFrame."""
        def __init__(self, name):
            self.name = name

        def __call__(self, accessor):
            setattr(DataFrame, self.name, AccessorProperty(accessor, accessor))

    class register_series_accessor(object):
        """Register custom accessor on Series."""
        def __init__(self, name):
            self.name = name

        def __call__(self, accessor):
            setattr(Series, self.name, AccessorProperty(accessor, accessor))
