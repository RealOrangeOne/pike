from pike.utils import noop


def test_noop():
    assert noop() is None
    assert noop("foo", bar="baz") is None
