"""The command checker is implemented by :class:`CheckerRegistry`.

This compatibility module gives future checker extensions one stable import path.
"""

from . import CheckerRegistry

__all__ = ["CheckerRegistry"]
