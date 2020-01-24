import logging
import coloredlogs

import gettext
import requests

import inspect
from functools import wraps

from . import configure

logger = logging.getLogger(__name__)
coloredlogs.install(level=configure.get('logging', 'status'), logger=logger)


def loads(langs):
    if langs == 'en':
        return gettext.translation('hexlightning', 'hexlightning/locale', languages=['en'])


def i18n():
    def decorator(f):
        param_name = 'message'
        sig = inspect.signature(f)
        if param_name not in sig.parameters:
            raise ValueError(
                "Wrapped function has no parameter message Object"
            )

        @wraps(f)
        def wrapper(*args, **kwargs):
            bound_arguments = sig.bind(*args, **kwargs)
            bound_arguments.apply_defaults()
            value = bound_arguments.arguments['message']

            # do something to get which language should use.
            load = loads('en')
            load.install()
            return f(*args, **kwargs)
        return wrapper
    return decorator
