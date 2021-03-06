"""
An example pikefile
"""

from functools import wraps

VARIABLE = "foo"


def do_thing(thing: str):
    """
    Do a thing, and do it perfectly

    :param thing: The thing to do
    """
    print("Doing", thing)


def _private_task():
    pass


def _task_wrapper(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        f(*args, **kwargs)

    return wrapper


@_task_wrapper
def wrapped_task(thing: str = "Rap"):
    pass
