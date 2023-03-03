import pandas as pd
import pandas_flavor as pf
import time

@pf.register_dataframe_method
def my_method(df: pd.DataFrame) -> pd.DataFrame:
    print("my_method called")
    return df.transpose()

@pf.register_dataframe_method
def another_method(df: pd.DataFrame, new_col_d) -> pd.DataFrame:
    print("another_method called")
    for col, v in new_col_d.items():
        df[col] = v
    return df

class tracer:
    @staticmethod
    def create_tracer(*args):
        return tracer()
    
    def __init__(self):
        self.method_name = None
        self.start_ts = None
        self.end_ts = None
        
    def __enter__(self):
        return self
        
    def handle_start_method_call(self,
                                 method_name,
                                 method_signature,
                                 method_args,
                                 method_kwagrs):
        self.method_name = method_name
        self.start_ts = time.time()
        return method_args, method_kwagrs

    def handle_end_method_call(self, ret):
        self.end_ts = time.time()

    def __exit__(self, exc_type, value, traceback):
        call_dur = self.end_ts - self.start_ts
        print(f"method {self.method_name} took {call_dur} secs to execute")


pf.register.method_call_ctx_factory = tracer.create_tracer
s_df = pd.DataFrame([[i + j for i in range(10)] for j in range(10)])
res_df = s_df.my_method().another_method({'new_col': 'new value'})
print(res_df)
