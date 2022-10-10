from functools import partial, update_wrapper, WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES

def wraps(wrapped, assigned = WRAPPER_ASSIGNMENTS + ("__args__",), updated = WRAPPER_UPDATES):
    if not hasattr(wrapped, "__args__"):
        setattr(wrapped, "__args__", wrapped.__code__.co_varnames[:wrapped.__code__.co_argcount])
    return partial(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated)
  
from kvin.common import __define__
def define(name, default=None, readonly=False, validation=None, on_value_changed=None): return __define__.define(name, default, readonly, validation, on_value_changed)

from kvin.common import __validator__
def validate(Type: type, arg: str, **kwargs): return __validator__.validate(Type, arg, **kwargs)

from kvin.common import __base__
def base(*args): return __base__.base(*args)

from common import __setproperty__
from common.__setproperty__ import NOT_EXISTS_BEHAVIORS
def setproperty(isnotexists: NOT_EXISTS_BEHAVIORS=NOT_EXISTS_BEHAVIORS.IGNORE): return __setproperty__.setproperty(isnotexists)
