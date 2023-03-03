# method_call_ctx_factory - tracing extention of pandas_flavor

`method_call_ctx_factory` global var defined in [pandas_flavor/register.py](https://github.com/pyjanitor-devs/pandas_flavor/blob/c60bfd43adbcc304b3455055af73ed9fc9ac10d1/pandas_flavor/register.py#L8) is used
to allow the methods registered via `pandas_flavors` to be traced.

Default value of `method_call_ctx_factory` is None.

Starting version 0.5.0 `pandas_flavor` implements the way to pass registered method name, signature and parameters to
be handled by user-defined object when the call is made. To allow this the user of pandas_flavor must set 
`method_call_ctx_factory` to refer to function with signature `(method_name: str, method_args: list, method_kwargs: dict) -> tracing_ctx`.
`tracing_ctx` should be class which implements methods with signatures as below:

```python
class tracing_ctx:
    def __enter__(self) -> None: pass
    def __exit__(self, type, value, traceback): -> None: pass
    def handle_start_method_call(self, method_name: str, 
                                 method_signature: inspect.Signature,
                                 method_args: list,
                                 method_kwargs: dict) -> (list, dict): pass
    def handle_end_method_call(self, method_ret: object) -> None: pass
```

During method call `pandas_flavor` will create object of class `tracing_ctx` then will use that object to enter *with* code block.
`handle_start_method_call` and `handle_end_method_call` will be called before and after actual method call. The input arguments 
and return object of actual method call will be passed to corresponding `tracing_ctx` method.

So `handle_start_method_call` and `handle_end_method_call` will have the chance to implement required tracing logic.
Aslo, __exit__ method will be called if any exception would occur. This way it is possible to handle the situation of 
actual method ends by raising exception.

The example of tracer class implementation and factory function registration is given in [tracing_ext-demo.py](/docs/tracing_ext-demo.py)
