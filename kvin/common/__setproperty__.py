
from common import wraps
from enum import IntEnum
from enum import IntFlag

class NOT_EXISTS_BEHAVIORS(IntEnum):
    IGNORE = 0
    MAKE_PROPERTY = 1
    THROW_EXCEPTION = 2
    
def setproperty(isnotexists: NOT_EXISTS_BEHAVIORS=NOT_EXISTS_BEHAVIORS.IGNORE):
    def _decorator(func):
        @wraps(func)
        def _wrapper(self, *args, **kwargs):
            
            # 引数取得
            arg = get_args(func, args, kwargs)
            
            for a in arg:
                if hasattr(self.__class__, a):
                    setattr(self, a, arg[a])
                else:
                    if isnotexists == NOT_EXISTS_BEHAVIORS.IGNORE:
                        pass
                    elif isnotexists == NOT_EXISTS_BEHAVIORS.MAKE_PROPERTY:
                        setattr(self, a, arg[a])
                    elif isnotexists == NOT_EXISTS_BEHAVIORS.THROW_EXCEPTION:
                        raise AttributeError("")
                    else:
                        TypeError("")
            
            return func(self, *args, **kwargs)
        return _wrapper
    return _decorator

setproperty.NOT_EXISTS_BEHAVIORS = NOT_EXISTS_BEHAVIORS

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
        
    return __get_arg(argname, argnames, args)[1]

class ARGTYPE(IntFlag):
    POSITIONAL = 1
    KEYWORD = 2
    VARIDIC = 4
    
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

get_args.ARGTYPE = ARGTYPE
