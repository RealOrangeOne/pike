from argparse import Namespace
from inspect import Parameter as InspectParameter
from inspect import Signature
from typing import Any, Callable, NamedTuple, Optional, Type

import docstring_parser

from .utils import to_spine_case


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

    def run(self, args: Namespace):
        task_args = []
        task_kwargs = {}
        for p in self.parameters:
            arg_value = getattr(args, p.name)
            if p.is_var_positional:
                task_args.extend(arg_value)
            else:
                task_kwargs[p.name] = arg_value

        return self.method(*task_args, **task_kwargs)
