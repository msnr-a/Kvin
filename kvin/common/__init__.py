from functools import partial, update_wrapper, WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES

def wraps(wrapped, assigned = WRAPPER_ASSIGNMENTS + ("__args__",), updated = WRAPPER_UPDATES):
    if not hasattr(wrapped, "__args__"):
        setattr(wrapped, "__args__", wrapped.__code__.co_varnames[:wrapped.__code__.co_argcount])
    return partial(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated)
  
from kvin.common import __define__
def define(name, default=None, readonly=False, validation=None, on_value_changed=None): return __define__.define(name, default, readonly, validation, on_value_changed)
