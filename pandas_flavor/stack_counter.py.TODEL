class StackCounter:
    def __init__(self, scf):
        self.scf = scf
        
    def __enter__(self):
        #print("StackCounter:__enter__", id(self))
        self.scf.level += 1
        return self

    def __exit__(self, type, value, traceback):
        #print("StackCounter:__exit__", id(self))
        self.scf.level -= 1
        
class SCF:
    def __init__(self):
        self.level = 0
        
    def get_sc(self):
        return StackCounter(self)

global_scf = SCF()
