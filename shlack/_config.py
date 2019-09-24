"""Utilities for reading config files.

Underscore in the name to prevent collison with existing config module. Also this is 
not a user-facing submodule so I don't care about prettiness.
"""
import os
from importlib import util as importutil


def string_to_module(s):
    """Read the python code in a string into a module.

    Parameters
    ----------
    s : str
        Python code in a string.

    Returns
    -------
    module : module
        A module object containing the resulting module.

    """
    spec = importutil.spec_from_loader("_module", loader=None)
    module = importutil.module_from_spec(spec)
    exec(s, module.__dict__)
    return module


def file_to_module(filepath):
    """Return a module object from the code in a python file.

     Parameters
    ----------
    filepath : str
        Path to a python file.

    Returns
    -------
    module : module
        A module object containing the resulting module.

    """
    with open(filepath, "r") as fh:
        return string_to_module(fh.read())


def dict_to_module(d):
    """Convert a dict to a module object with one attribute per key.

    Parameters
    ----------
    d : Dict[str, any]
        Dictionary to convert.

    Returns
    -------
    module : module
        A module object containing the values of the dictionary.

    """
    # make an empty python code string. we will add to this
    code = ""

    for k, v in d.items():
        code += '\n%s="%s"' % (k, v)

    return string_to_module(code)


def env_to_module(*vars):
    """Read environment variables into a python module.

    Parameters
    ----------
    *vars : str
        Names of the env variables to read into the module.

    Returns
    -------
    module : module
        A module object containing the values of the keys which are defined.

    """
    return dict_to_module({k: os.getenv(k) for k in vars if os.getenv(k) is not None})


def extract_config(keywords, modules):
    """Extract config from one or more modules.

    This function includes logic to select config from the first module in which
    it is found.

    Parameters
    ----------
    keywords : iterable[str]
        An iterable of string objects, containing keys to extract.
    modules : iterable[module]
        An iterable of modules (or regular python objects) in which to look for said 
        keys.

    Returns
    -------
    config : dict[str, any]
        A dictionary containing one key per keyword with values from the first module
        it was found within.

    """
    return {
        k: next((getattr(m, k) for m in modules if hasattr(m, k)), None)
        for k in keywords
    }


def module_to_dict(module, dunder=False):
    """Convert a module to a dictionary.

    Parameters
    ----------
    module : module
        A module object.
    dunder : bool
        Option to include "dunder" attributes. Default False.

    Returns
    -------
    dict[str, any]
        A dictionary containing the module attributes.

    """
    return {
        k: getattr(module, k)
        for k in dir(module)
        if not (k.startswith("__") and k.endswith("__")) or dunder
    }
