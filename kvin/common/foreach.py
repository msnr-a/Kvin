from collections.abc import ValuesView
from . import wraps
from . import get_arg

def foreach(*names, **yield_return):
    def _decorator(func):
        @wraps(func)
        def _wrapper(self, *args, **kwargs):
            
            yr = True if (yield_return.get("yield_return")) == True else False
            
            idxs = []
            vals = []

            if len(names) == 0:
                if __isarray(args[0]):
                    idxs = [0]
                    vals = [args[0]]
                else:
                    return func(self, *args, **kwargs)
            else:
                for n in names:
                    i, v = get_arg(func, n, args, kwargs)
                    if __isarray(v):
                        idxs += [i]
                        vals += [v]
            
            if len(idxs) == 0:
                return func(self, *args, **kwargs)
            
            args2 = []
            for val in zip(*vals):
                arg = list(args)
                for i, v in zip(idxs, val):
                    arg[i] = v
                args2 += [arg]
            
            if yr:
                def yield_return_func(idxs, vals, args, kwargs):
                    for a in args2:
                        yield func(self, *a, **kwargs)
                return yield_return_func(idxs, vals, args, kwargs)
            else:
                def array_return_func(idxs, vals, args, kwargs):
                    result = []
                    for a in args2:
                        result += [func(self, *a, **kwargs)]
                    return result
                return array_return_func(idxs, vals, args, kwargs)

        return _wrapper
    return _decorator

def __isarray(value):
    if isinstance(value, str): return False
    if hasattr(value, "__iter__"): return True
    return False
