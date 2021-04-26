from inspect import Parameter as InspectParameter
from inspect import Signature, getmodule
from pathlib import Path
from typing import Any, Callable, NamedTuple, Optional, Set, Type

import docstring_parser

from .utils import import_file, to_spine_case


class Parameter(NamedTuple):
    name: str
    display_name: str
    kind: int
    param_type: Optional[Type]
    default: Any
    description: Optional[str]

    @property
    def has_default(self):
        return self.default != InspectParameter.empty

    @property
    def is_var_positional(self):
        return self.kind == InspectParameter.VAR_POSITIONAL


class Task(NamedTuple):
    name: str
    method: Callable

    @classmethod
    def from_callable(cls, method: Callable):
        return cls(name=to_spine_case(method.__name__), method=method)

    @property
    def signature(self):
        return Signature.from_callable(self.method)

    @property
    def parsed_docstring(self):
        return docstring_parser.parse(self.method.__doc__)

    @property
    def description(self):
        return (
            self.parsed_docstring.short_description
            or self.parsed_docstring.long_description
        )

    @property
    def parameters(self):
        params = []
        param_help = {a.arg_name: a.description for a in self.parsed_docstring.params}
        for p in self.signature.parameters.values():
            params.append(
                Parameter(
                    name=p.name,
                    display_name=to_spine_case(p.name),
                    kind=p.kind,
                    param_type=p.annotation
                    if p.annotation != InspectParameter.empty
                    else None,
                    description=param_help.get(p.name),
                    default=p.default,
                )
            )
        return params


class TaskRegistry:
    """
    Keep track of tasks
    """

    _tasks: Set[Task]

    def __init__(self, pikefile: Path):
        self.pikefile = pikefile
        self._tasks = set()

    def _load(self):
        """
        Actually load the tasks
        """
        self._tasks.clear()
        pikefile_data = import_file(self.pikefile)
        for name, val in pikefile_data.items():
            if name.startswith("_"):
                continue

            if not callable(val):
                continue

            if getmodule(val) is not None:
                continue

            self._tasks.add(Task.from_callable(val))

    @property
    def tasks(self) -> Set[Task]:
        if not self._tasks:
            self._load()

        return self._tasks
