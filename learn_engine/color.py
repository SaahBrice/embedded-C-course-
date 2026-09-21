from __future__ import annotations

import os
from dataclasses import dataclass
from typing import TextIO


RESET = "\033[0m"


@dataclass(frozen=True)
class Palette:
    enabled: bool

    @classmethod
    def for_stream(cls, stream: TextIO) -> "Palette":
        try:
            interactive = bool(stream.isatty())
        except (AttributeError, OSError):
            interactive = False
        return cls(interactive and "NO_COLOR" not in os.environ and os.environ.get("TERM") != "dumb")

    def paint(self, text: str, code: str) -> str:
        return f"\033[{code}m{text}{RESET}" if self.enabled else text

    def title(self, text: str) -> str:
        return self.paint(text, "1;36")

    def success(self, text: str) -> str:
        return self.paint(text, "1;32")

    def error(self, text: str) -> str:
        return self.paint(text, "1;31")

    def warning(self, text: str) -> str:
        return self.paint(text, "1;33")

    def info(self, text: str) -> str:
        return self.paint(text, "1;34")

    def accent(self, text: str) -> str:
        return self.paint(text, "1;35")

    def muted(self, text: str) -> str:
        return self.paint(text, "2;37")
