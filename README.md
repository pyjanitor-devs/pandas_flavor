# Pandas Flavor
**Flavor Pandas objects with your own methods and accessors.**

Easily register new methods and accessors with Pandas objects.

![](docs/_images/example.png)

Pandas added `register_series_accessor` and `register_dataframe_accessor` decorators
in 0.23. These extensions allow you to easily add new accessors to Pandas objects that
are persistent. This means, you can easily write your own flavor of the DataFrame.

To see an example, checkout [pdvega](). This library adds a new Vega plotting accessor
under the `vgplot` attribute and mirror the `plot` (matplotlib-based) accessor.

**Pandas Flavor** takes this extension module a step further and adds similar syntax
for registering new methods!

To see an example, check out [PhyloPandas](https://github.com/Zsailer/phylopandas).
This library adds extra `to_` methods for writing DataFrames to various biological
sequencing file formats.

## How it works
