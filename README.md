# Pandas Flavor
**The easy way to write your own flavor of Pandas**

Pandas 0.23 added a (simple) API for registering accessors with Pandas objects.

Pandas-flavor extends Pandas' extension API by:
1. adding support for registering methods as well.
2. making each of these functions backwards compatible with older versions of Pandas.

***What does this mean?***

It is now simpler to add custom functionality to Pandas DataFrames and Series.

Import this package. Write a simple python function. Register the function using one of the following decorators.

***Why?***

Pandas is super handy. Its general purpose is to be a "flexible and powerful data analysis/manipulation library".

**Pandas Flavor** allows you add functionality that tailors Pandas to specific fields or use cases.

Maybe you want to add new write methods to the Pandas DataFrame? Maybe you want custom plot functionality? Maybe something else?

## Register accessors

Accessors (in pandas) are objects attached to a attribute on the Pandas DataFrame/Series
that provide extra, specific functionality. For example, `pandas.DataFrame.plot` is an
accessor that provides plotting functionality.

Add an accessor by registering the function with the following decorator
and passing the decorator an accessor name.


```python
# my_flavor.py

import pandas as pd
import pandas_flavor as pf

@pf.register_dataframe_accessor('my_flavor')
class MyFlavor(object):

  def __init__(self, data):
    self._data

    def row_by_value(self, col, value):
        """Slice out row from DataFrame by a value."""
        return self._data[self._data[col] == value].squeeze()

```

Every dataframe now has this accessor as an attribute.
```python
import my_flavor

# DataFrame.
df = pd.DataFrame(data={
  "x": [10, 20, 25],
  "y": [0, 2, 5]
})

# Print DataFrame
print(df)

# x  y
# 0  10  0
# 1  20  2
# 2  25  5

# Access this functionality
df.my_flavor.row_by_value('x', 10)

# x    10
# y     0
# Name: 0, dtype: int64
```

To see this in action, check out [pdvega](https://github.com/jakevdp/pdvega),
[PhyloPandas](https://github.com/Zsailer/phylopandas), and [pyjanitor](https://github.com/ericmjl/pyjanitor)!


## Register methods

Using this package, you can attach functions directly to Pandas objects. No
intermediate accessor is needed.

```python
# my_flavor.py

import pandas as pd
import pandas_flavor as pf

@pf.register_dataframe_method
def row_by_value(df, col, value):
    """Slice out row from DataFrame by a value."""
    return df[df[col] == value].squeeze()

```

```python
import my_flavor

# DataFrame.
df = DataFrame(data={
  "x": [10, 20, 25],
  "y": [0, 2, 5]
})

# Print DataFrame
print(df)

# x  y
# 0  10  0
# 1  20  2
# 2  25  5

# Access this functionality
df.row_by_value('x', 10)

# x    10
# y     0
# Name: 0, dtype: int64
```

## Available Methods

- **register_dataframe_method**: register a method directly with a pandas DataFrame.
- **register_dataframe_accessor**: register an accessor (and it's methods) with a pandas DataFrame.
- **register_series_method**: register a methods directly with a pandas Series.
- **register_series_accessor**: register an accessor (and it's methods) with a pandas Series.

## Installation

You can install using **pip**:
```
pip install pandas_flavor
```
or conda (thanks @ericmjl)!
```
conda install -c conda-forge pandas-flavor
```

## Contributing

Pull requests are always welcome! If you find a bug, don't hestitate to open an issue or submit a PR. If you're not sure how to do that, check out this [simple guide](https://github.com/Zsailer/guide-to-working-as-team-on-github).

If you have a feature request, please open an issue or submit a PR!

## TL;DR

Pandas 0.23 introduced a simpler API for [extending Pandas](https://pandas.pydata.org/pandas-docs/stable/development/extending.html#extending-pandas). This API provided two key decorators, `register_dataframe_accessor` and `register_series_accessor`, that enable users to register **accessors** with Pandas DataFrames and Series. 

Pandas Flavor originated as a library to backport these decorators to older versions of Pandas (<0.23). While doing the backporting, it became clear that registering **methods** directly to Pandas objects might be a desired feature as well.[*](#footnote) 

<a name="footnote">*</a>*It is likely that Pandas deliberately chose not implement to this feature. If everyone starts monkeypatching DataFrames with their custom methods, it could lead to confusion in the Pandas community. The preferred Pandas approach is to namespace your methods by registering an accessor that contains your custom methods.* 

**So how does method registration work?**

When you register a method, Pandas flavor actually creates and registers a (this is subtle, but important) **custom accessor class that mimics** the behavior of a method by:
1. inheriting the docstring of your function
2. overriding the `__call__` method to call your function.
