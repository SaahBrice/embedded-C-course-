from __future__ import annotations

import json
import os
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .errors import ProgressError


@dataclass(frozen=True, slots=True)
class Completion:
    version: str
    attempt_id: str
    completed_at: str


@dataclass(frozen=True, slots=True)
class LevelClearance:
    final_battle_id: str
    attempt_id: str
    completed_at: str


@dataclass(frozen=True, slots=True)
class Progress:
    schema_version: int = 2
    completed: dict[str, Completion] = field(default_factory=dict)
    cleared_levels: dict[str, LevelClearance] = field(default_factory=dict)


class ProgressStore:
    def __init__(self, path: Path):
        self.path = path.resolve()

    def load(self) -> Progress:
        if not self.path.exists():
            return Progress()
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(raw, dict) or raw.get("schema_version") != 2:
                raise ValueError("unsupported schema_version")
            completed_raw = raw.get("completed", {})
            if not isinstance(completed_raw, dict):
                raise ValueError("completed must be an object")
            completed: dict[str, Completion] = {}
            for mission_id, value in completed_raw.items():
                if not isinstance(mission_id, str) or not isinstance(value, dict):
                    raise ValueError("invalid completion entry")
                version = value.get("version")
                attempt_id = value.get("attempt_id")
                completed_at = value.get("completed_at")
                if not all(isinstance(item, str) for item in (version, attempt_id, completed_at)):
                    raise ValueError(f"invalid completion for {mission_id}")
                completed[mission_id] = Completion(version, attempt_id, completed_at)
            cleared_raw = raw.get("cleared_levels", {})
            if not isinstance(cleared_raw, dict):
                raise ValueError("cleared_levels must be an object")
            cleared: dict[str, LevelClearance] = {}
            for level_id, value in cleared_raw.items():
                if not isinstance(level_id, str) or not isinstance(value, dict):
                    raise ValueError("invalid level clearance entry")
                final_battle_id = value.get("final_battle_id")
                attempt_id = value.get("attempt_id")
                completed_at = value.get("completed_at")
                if not all(
                    isinstance(item, str) and item
                    for item in (final_battle_id, attempt_id, completed_at)
                ):
                    raise ValueError(f"invalid level clearance for {level_id}")
                cleared[level_id] = LevelClearance(
                    final_battle_id, attempt_id, completed_at
                )
            return Progress(completed=completed, cleared_levels=cleared)
        except (OSError, json.JSONDecodeError, ValueError, TypeError) as exc:
            raise ProgressError(f"cannot read progress from {self.path}: {exc}") from exc

    def complete(self, mission_id: str, version: str, attempt_id: str) -> None:
        progress = self.load()
        if mission_id in progress.completed:
            return
        completed = dict(progress.completed)
        completed[mission_id] = Completion(
            version=version,
            attempt_id=attempt_id,
            completed_at=datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        )
        self._save(Progress(completed=completed, cleared_levels=progress.cleared_levels))

    def clear_level(self, level_id: str, final_battle_id: str, attempt_id: str) -> None:
        progress = self.load()
        if level_id in progress.cleared_levels:
            return
        cleared = dict(progress.cleared_levels)
        cleared[level_id] = LevelClearance(
            final_battle_id=final_battle_id,
            attempt_id=attempt_id,
            completed_at=datetime.now(timezone.utc).isoformat(timespec="seconds").replace(
                "+00:00", "Z"
            ),
        )
        self._save(Progress(completed=progress.completed, cleared_levels=cleared))

    def _save(self, progress: Progress) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data: dict[str, Any] = {
            "schema_version": progress.schema_version,
            "completed": {
                mission_id: {
                    "version": entry.version,
                    "attempt_id": entry.attempt_id,
                    "completed_at": entry.completed_at,
                }
                for mission_id, entry in sorted(progress.completed.items())
            },
            "cleared_levels": {
                level_id: {
                    "final_battle_id": entry.final_battle_id,
                    "attempt_id": entry.attempt_id,
                    "completed_at": entry.completed_at,
                }
                for level_id, entry in sorted(progress.cleared_levels.items())
            },
        }
        payload = json.dumps(data, indent=2, sort_keys=True) + "\n"
        temporary: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                "w", encoding="utf-8", dir=self.path.parent, prefix=f".{self.path.name}.",
                suffix=".tmp", delete=False,
            ) as stream:
                temporary = Path(stream.name)
                stream.write(payload)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, self.path)
        except OSError as exc:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
            raise ProgressError(f"cannot save progress to {self.path}: {exc}") from exc
