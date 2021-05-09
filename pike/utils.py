import sys
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path
from typing import Any, Dict


def noop(*args, **kwargs):
    """
    This does nothing
    """
    pass


def import_file(path: Path) -> Dict[str, Any]:
    """
    Import a module from a file path, returning its contents.
    """
    orig_bytecode = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    loader = SourceFileLoader(path.name, str(path))
    spec = spec_from_loader(path.name, loader)
    mod = module_from_spec(spec)
    loader.exec_module(mod)
    sys.dont_write_bytecode = orig_bytecode
    return vars(mod)


def to_spine_case(original: str) -> str:
    """
    Convert this_thing to this-thing.
    """
    return original.lower().replace("_", "-")
