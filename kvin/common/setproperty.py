from . import wraps
from . import get_args
from enum import IntEnum

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

