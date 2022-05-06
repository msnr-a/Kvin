from functools import partial, update_wrapper, WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES

def wraps(wrapped, assigned = WRAPPER_ASSIGNMENTS + ("__args__",), updated = WRAPPER_UPDATES):
    if not hasattr(wrapped, "__args__"):
        setattr(wrapped, "__args__", wrapped.__code__.co_varnames[:wrapped.__code__.co_argcount])
    return partial(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated)
