from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class CheckSpec:
    id: str
    name: str
    type: str
    required: bool
    config: dict[str, Any]


@dataclass(frozen=True, slots=True)
class Mission:
    id: str
    title: str
    version: str
    order: int
    stage: int
    activity: str
    duration_minutes: int
    platform: str
    prerequisites: tuple[str, ...]
    objectives: tuple[str, ...]
    starter: str
    hints: tuple[str, ...]
    content: dict[str, str]
    checks: tuple[CheckSpec, ...]
    root: Path

    @property
    def manifest_path(self) -> Path:
        return self.root / "level.toml"

    def content_path(self, key: str) -> Path:
        return self.root / self.content[key]


@dataclass(frozen=True, slots=True)
class CourseLevel:
    id: str
    title: str
    order: int
    objective: str
    learning_outcomes: tuple[str, ...]
    overview: Path
    sublevel_ids: tuple[str, ...]
    final_battle_id: str
    final_integrates: tuple[str, ...]
    topic_practice: dict[str, tuple[str, ...]]


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    mission_id: str
    message: str


@dataclass(frozen=True, slots=True)
class Attempt:
    id: str
    mission_id: str
    mission_version: str
    path: Path


@dataclass(frozen=True, slots=True)
class CheckResult:
    check_id: str
    name: str
    passed: bool
    category: str
    message: str
    stdout: str = ""
    stderr: str = ""
    exit_code: int | None = None


@dataclass(frozen=True, slots=True)
class MissionResult:
    passed: bool
    checks: tuple[CheckResult, ...]

