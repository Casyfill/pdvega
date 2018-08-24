import ast
import json
import importlib
from hashlib import md5

from itertools import tee, chain


def dict_hash(dct):
    """Return a hash of the contents of a dictionary"""
    dct_s = json.dumps(dct, sort_keys=True)

    try:
        m = md5(dct_s)
    except TypeError:
        m = md5(dct_s.encode())

    return m.hexdigest()


def exec_then_eval(code, namespace=None):
    """Exec a code block & return evaluation of the last line"""
    # TODO: make this less brittle.
    namespace = namespace or {}

    block = ast.parse(code, mode='exec')
    last = ast.Expression(block.body.pop().value)

    exec(compile(block, '<string>', mode='exec'), namespace)
    return eval(compile(last, '<string>', mode='eval'), namespace)


def import_obj(clsname, default_module=None):
    """
    Import the object given by clsname.
    If default_module is specified, import from this module.
    """
    if default_module is not None:
        if not clsname.startswith(default_module + '.'):
            clsname = '{0}.{1}'.format(default_module, clsname)
    mod, clsname = clsname.rsplit('.', 1)
    mod = importlib.import_module(mod)
    try:
        obj = getattr(mod, clsname)
    except AttributeError:
        raise ImportError('Cannot import {0} from {1}'.format(clsname, mod))
    return obj



def strip_vl_extension(filename):
    """Strip the vega-lite extension (either vl.json or json) from filename"""
    for ext in ['.vl.json', '.json']:
        if filename.endswith(ext):
            return filename[:-len(ext)]
    else:
        return filename


def prev_this_next(it, sentinel=None):
    """Utility to return (prev, this, next) tuples from an iterator"""
    i1, i2, i3 = tee(it, 3)
    next(i3, None)
    return zip(chain([sentinel], i1), i2, chain(i3, [sentinel]))
