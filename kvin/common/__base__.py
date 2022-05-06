from kvin.common import wraps

def base(*names):
    def _decorator(func):
        @wraps(func)
        def _wrapper(self, *args, **kwargs):
            
            if len(names) == 0:
                for b in self.__class__.__bases__:
                    if hasattr(b, func.__name__):
                        getattr(b, func.__name__)(self, *args, **kwargs)
            else:
                bases = list(map(lambda x: x.__name__, self.__class__.__bases__)) + \
                        list(map(lambda x: x.__qualname__, self.__class__.__bases__))
                for name in names:
                    getattr(self.__class__.__bases__[bases.index(name)], func.__name__)(self, *args, **kwargs)

            func(self, *args, **kwargs)
        return _wrapper
    return _decorator
