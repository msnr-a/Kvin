from . import wraps
from functools import singledispatch
from re import fullmatch
from sys import maxsize

@singledispatch
def validate(Type: type, arg: str, **kwargs):
    def _decorator(func):
        @wraps(func)
        def _wrapper(self, *args, **kwdargs):

            # 引数名
            if hasattr(func, "__args__"):
                argnames = func.__args__
            else:
                argnames = func.__code__.co_varnames[:func.__code__.co_argcount]

            # 引数
            value = args[argnames.index(arg) - 1]
            
            try:
                
                # 型チェック
                if not (type(value) is Type): raise TypeError(f"must be {Type}.")
                
                # 値チェック
                validate(value, **kwargs)
                
            except Exception as ex:
                raise type(ex)(f"{func.__qualname__} : '{arg}' {ex}") from ex
                
            # function実行
            return func(self, *args, **kwdargs)
            
        return _wrapper
    return _decorator

@validate.register
def _(value: int, Max=maxsize, Min=-maxsize):

    # 最小値
    if value < Min:
        raise ValueError(f"must be greater than {Min}.")
        
    # 最大値
    if Max < value:
        raise ValueError(f"must be less than {Max}.")
        
    # OK
    return value

@validate.register
def _(value: float, Max=maxsize, Min=-maxsize):
    
    # 最小値
    if value < Min:
        raise ValueError(f"must be greater than {Min}.")
        
    # 最大値
    if Max < value:
        raise ValueError(f"must be less than {Max}.")
        
    # OK
    return value

@validate.register
def _(value: str, maxLength=-1, minLength=-1, pattern=None):
    
    # 最小文字数
    if (-1 < minLength):
        if (len(value) < minLength):
            raise ValueError(f"length must be greater than {minLength - 1}.")
            
    # 最大文字数
    if (-1 < maxLength):
        if (maxLength < len(value)):
            raise ValueError(f"length must be less than {maxLength + 1}.")
            
    # 正規表現
    if not (pattern is None):
        if re.fullmatch(pattern, value) is None:
            raise ValueError(f"'must match the pattern {{{pattern}}}.")
            
    # OK
    return value
