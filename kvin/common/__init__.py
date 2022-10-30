from functools import partial, update_wrapper, WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES
from enum import IntFlag
    
def wraps(wrapped, assigned = WRAPPER_ASSIGNMENTS + ("__args__",), updated = WRAPPER_UPDATES):
    if not hasattr(wrapped, "__args__"):
        setattr(wrapped, "__args__", wrapped.__code__.co_varnames[:wrapped.__code__.co_argcount])
    return partial(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated)

class ARGTYPE(IntFlag):
    POSITIONAL = 1
    KEYWORD = 2
    VARIDIC = 4

def __get_arg(argname, argnames, args):
    
    if argname in argnames:
        idx = argnames.index(argname) - (1 if "self" in argnames else 0)
        
        # 引数あり
        if len(args) > idx:
            return idx, args[idx]
        
        # 引数あり（省略）
        else:
            return None, None
        
    else:
        # 引数なし
        return None, None

def get_arg(func, argname, args, kwargs):
    
    # self
    if argname == "self":
        return None
    
    # keyword
    if argname in kwargs:
        return kwargs[argname]
    
    # psitional
    if hasattr(func, "__args__"):
        argnames = func.__args__
    else:
        argnames = func.__code__.co_varnames[:func.__code__.co_argcount]
        
    return __get_arg(argname, argnames, args)
    
def get_args(func, args, kwargs, argtype=ARGTYPE.POSITIONAL|ARGTYPE.KEYWORD):
    
    result = {}
    
    if hasattr(func, "__args__"):
        argnames = func.__args__
    else:
        argnames = func.__code__.co_varnames[:func.__code__.co_argcount]
        
    # positional
    if ARGTYPE.POSITIONAL in argtype:
        for a in argnames:
            if a != "self":
                argidx, argval = __get_arg(a, argnames, args)
                if argidx is not None:
                    result[a] = argval
                    
    # keyword
    if ARGTYPE.KEYWORD in argtype:
        for k in kwargs:
            result[k] = kwargs[k]
            
    # varidic
    if ARGTYPE.VARIDIC in argtype:
        cnt1 = len(argnames) - (1 if "self" in argnames else 0)
        cnt2 = len(args)
        
        if cnt1 < cnt2:
            result["args"] = [args[i] for i in range(cnt1, cnt2, 1)]
            
    return result

from .base import base
from .define import define
from .setproperty import setproperty
from .setproperty import NOT_EXISTS_BEHAVIORS
from .foreach import foreach
