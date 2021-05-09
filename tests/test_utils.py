import inspect
import os.path
from importlib._bootstrap_external import _PYCACHE
from importlib.util import cache_from_source

from pike.utils import import_file, noop, to_spine_case


def test_noop():
    assert noop() is None
    assert noop("foo", bar="baz") is None


def test_import_file(root):
    test_file = root / "pike" / "utils.py"
    mod_vars = import_file(test_file)
    assert "import_file" in mod_vars

    assert inspect.getsource(mod_vars["import_file"]) == inspect.getsource(import_file)
    assert inspect.getsource(mod_vars["noop"]) == inspect.getsource(noop)


def test_import_file_creates_no_bytecode(example_pikefile):
    bytecode_path = cache_from_source(str(example_pikefile))
    assert not os.path.exists(bytecode_path)
    import_file(example_pikefile)
    assert not os.path.exists(bytecode_path)
    bytecode_dir = os.path.dirname(bytecode_path)
    assert bytecode_dir.endswith(_PYCACHE)
    assert not os.path.exists(bytecode_dir)


def test_spine_case():
    assert to_spine_case("foo_BAR") == "foo-bar"
