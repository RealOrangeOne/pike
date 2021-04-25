from inspect import Parameter as InspectParameter
from inspect import Signature, getmodule
from pathlib import Path
from typing import Any, Callable, NamedTuple, Optional, Set, Type

from .utils import import_file


class Parameter(NamedTuple):
    name: str
    kind: int
    param_type: Optional[Type]
    default: Any

    @property
    def has_default(self):
        return self.default != InspectParameter.empty

    @property
    def is_var_positional(self):
        return self.kind == InspectParameter.VAR_POSITIONAL


class Task(NamedTuple):
    name: str
    method: Callable

    @property
    def signature(self):
        return Signature.from_callable(self.method)

    @property
    def parameters(self):
        params = []
        for p in self.signature.parameters.values():
            params.append(
                Parameter(
                    name=p.name,
                    kind=p.kind,
                    param_type=p.annotation
                    if p.annotation != InspectParameter.empty
                    else None,
                    default=p.default,
                )
            )
        return params


def load_tasks(pikefile: Path) -> Set[Task]:
    pikefile_data = import_file(pikefile)
    tasks = set()
    for name, val in pikefile_data.items():
        if name.startswith("_"):
            continue

        if not callable(val):
            continue

        if getmodule(val) is not None:
            continue

        tasks.add(Task(name=name, method=val))

    return tasks
