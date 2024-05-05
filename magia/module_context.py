from __future__ import annotations

import typing
from contextlib import contextmanager

if typing.TYPE_CHECKING:
    from .module import Module


class ModuleContext:
    """Describe stack of modules which are currently being constructed."""

    _instance: None | ModuleContext = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance._stack = []
        return cls._instance

    def push(self, module: Module):
        self._stack.append(module)

    @property
    def current(self) -> None | Module:
        if len(self._stack) == 0:
            return None
        return self._stack[-1]

    def pop(self):
        if len(self._stack) != 0:
            self._stack.pop()

    @property
    @contextmanager
    def disable(self):
        self.push(None)
        yield
        self.pop()
