# Pandas Flavor
**The easy way to write your own flavor of Pandas**

Pandas added an new (simple) API to register accessors with Pandas objects.
This package adds support for registering methods as well.

*What does this mean?*

It's super easy to custom functionality to Pandas DataFrames and Series.

Import this package. Write a simple python function. Register the function using one of the following decorators.

*Why?*

Pandas is super handy. Its general purpose is to be a "flexible and powerful data analysis/manipulation library".

**Pandas Flavor** allows you to tailor Pandas to specific fields or use cases.

Maybe you want to add new write methods to the Pandas DataFrame? Maybe you want custom plot functionality? Maybe something else?

## Register accessors

Accessors (in pandas) are objects attached to a attribute on the Pandas DataFrame/Series
that provide extra, specific functionality. For example, `pandas.DataFrame.plot` is an
accessor that provides plotting functionality.

Add an accessor by registering the function with the following decorator
and passing the decorator an accessor name.

```python
import pandas as pd
import pandas_flavor as pf

@pf.register_dataframe_accessor('my_flavor')
def is_cool(df):
    """Is my accessor cool?"""
    return True

# DataFrame.
df = DataFrame()

# Access this functionality
df.my_flavor.is_cool()
# Returns True
True
```

To see this in action, check out [pdvega](https://github.com/jakevdp/pdvega)! this
library adds a new plotting accessor for making Vega plots from pandas data.

## Register methods

Using this package, you can attach functions directly to Pandas objects. No
intermediate accessor is needed.

```python
import pandas as pd
import pandas_flavor as pf

@pf.register_dataframe_method
def is_cool(df):
    """Is my dataframe cool?"""
    return True

# DataFrame.
df = DataFrame()

# Access this functionality
df.is_cool()
# Returns True
True
```

To see in action, check out [PhyloPandas](https://github.com/Zsailer/phylopandas).
This library adds extra `to_` methods for writing DataFrames to various biological
sequencing file formats.
