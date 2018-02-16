# Pandas Flavor
**The easy way to write your own flavor of Pandas**

Pandas added an new (simple) API to register accessors with Pandas objects.
This package does two things:
1. adds support for registering methods as well.
2. makes each of these functions backwards compatible with older versions of Pandas.

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
df.my_flavor.row_by_value('x', 10)

# x    10
# y     0
# Name: 0, dtype: int64
```

To see this in action, check out [pdvega](https://github.com/jakevdp/pdvega) and
[PhyloPandas](https://github.com/Zsailer/phylopandas)!


## Register methods

Using this package, you can attach functions directly to Pandas objects. No
intermediate accessor is needed.

```python
import pandas as pd
import pandas_flavor as pf

@pf.register_dataframe_method
def row_by_value(df, col, value):
    """Slice out row from DataFrame by a value."""
    return df[df[col] == value].squeeze()

```

```python
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
