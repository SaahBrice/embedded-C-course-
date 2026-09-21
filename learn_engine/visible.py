from __future__ import annotations

import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from .models import Attempt, Mission


@dataclass(frozen=True, slots=True)
class VisibleRunResult:
    exit_code: int
    stdout: str = ""
    stderr: str = ""


class VisibleRunner:
    """Give a function-only sublevel a trusted temporary main and visible cases."""

    def __init__(self, repository_root: Path):
        self.repository_root = repository_root.resolve()

    @staticmethod
    def available(mission: Mission) -> bool:
        return (mission.root / "checks" / "visible.c").is_file()

    def run(self, mission: Mission, attempt: Attempt) -> VisibleRunResult:
        harness = (mission.root / "checks" / "visible.c").resolve()
        if mission.root not in harness.parents or not harness.is_file():
            return VisibleRunResult(2, stderr="This sublevel has no visible C driver.\n")
        check = next((item for item in mission.checks if item.type == "c_harness"), None)
        if check is None:
            return VisibleRunResult(2, stderr="This sublevel does not use a C harness.\n")
        try:
            sources = [self._attempt_file(attempt, item) for item in check.config["sources"]]
            flags = [str(item) for item in check.config.get("cflags", [])]
            compiler = str(check.config.get("compiler", "cc"))
            timeout = float(check.config.get("timeout", 20))
            support = [self._repository_file(item) for item in check.config.get("support_sources", [])]
            includes = [self._repository_directory(item) for item in check.config.get("support_include_dirs", [])]
        except (KeyError, TypeError, ValueError) as exc:
            return VisibleRunResult(2, stderr=f"Invalid visible-run configuration: {exc}\n")
        include_args = [argument for path in includes for argument in ("-I", str(path))]
        with tempfile.TemporaryDirectory(prefix=f"learn-run-{mission.id}-") as temporary:
            executable = Path(temporary) / "visible-run"
            built = self._execute([
                compiler, *flags, "-I", str(attempt.path), *include_args,
                *map(str, sources), str(harness), *map(str, support), "-o", str(executable),
            ], timeout)
            if built.exit_code != 0:
                return built
            return self._execute([str(executable)], timeout)

    @staticmethod
    def _execute(command: list[str], timeout: float) -> VisibleRunResult:
        try:
            completed = subprocess.run(
                command, text=True, capture_output=True, timeout=timeout, check=False
            )
            return VisibleRunResult(completed.returncode, completed.stdout, completed.stderr)
        except FileNotFoundError as exc:
            return VisibleRunResult(2, stderr=f"Required tool not found: {exc.filename}\n")
        except subprocess.TimeoutExpired as exc:
            return VisibleRunResult(
                2, stdout=exc.stdout or "",
                stderr=(exc.stderr or "") + "Visible run timed out.\n",
            )

    @staticmethod
    def _attempt_file(attempt: Attempt, value: object) -> Path:
        if not isinstance(value, str):
            raise TypeError("source path must be text")
        path = (attempt.path / value).resolve()
        if attempt.path not in path.parents or not path.is_file():
            raise ValueError(f"missing learner source: {value}")
        return path

    def _repository_file(self, value: object) -> Path:
        if not isinstance(value, str):
            raise TypeError("support source path must be text")
        path = (self.repository_root / value).resolve()
        if self.repository_root not in path.parents or not path.is_file():
            raise ValueError(f"invalid support source: {value}")
        return path

    def _repository_directory(self, value: object) -> Path:
        if not isinstance(value, str):
            raise TypeError("include path must be text")
        path = (self.repository_root / value).resolve()
        if self.repository_root not in path.parents or not path.is_dir():
            raise ValueError(f"invalid support include: {value}")
        return path
