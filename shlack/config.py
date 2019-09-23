"""Utilities for reading config files."""
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
    # make an empty python code string. we will add to this
    code = ""

    # add one line per variable if its value is defined.
    for var in vars:
        val = os.getenv(var)
        if val is not None:
            code += '\n%s="%s"' % (var, val)

    return string_to_module(code)


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
