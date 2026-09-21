from __future__ import annotations

import re
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path

from .catalog import Catalog
from .models import Attempt
from .runner import MissionRunner


_ACTIVITIES = {
    "predict", "write", "debug", "trace", "refactor", "review",
    "datasheet", "design", "simulate", "hardware", "integrate", "project",
}
_PLATFORMS = {"host", "sim", "stm32", "concept"}


@dataclass(frozen=True, slots=True)
class AuthoringIssue:
    mission_id: str
    message: str


@dataclass(frozen=True, slots=True)
class ValidationReport:
    mission_count: int
    solution_pass_count: int
    solution_checks_requested: bool
    issues: tuple[AuthoringIssue, ...]

    @property
    def ok(self) -> bool:
        return not self.issues

    def render(self) -> str:
        noun = "sublevel" if self.mission_count == 1 else "sublevels"
        lines = [f"Validated {self.mission_count} {noun}."]
        if self.solution_checks_requested:
            noun = "reference solution" if self.solution_pass_count == 1 else "reference solutions"
            lines.append(f"{self.solution_pass_count} {noun} passed.")
        if self.issues:
            lines.append(f"Found {len(self.issues)} curriculum issue(s):")
            lines.extend(f"  - {issue.mission_id}: {issue.message}" for issue in self.issues)
        else:
            lines.append("Curriculum is valid.")
        return "\n".join(lines) + "\n"


class CurriculumValidator:
    def __init__(self, repository_root: Path, runner: MissionRunner):
        self.repository_root = repository_root.resolve()
        self.runner = runner

    def validate_all(self, catalog: Catalog, run_solutions: bool = False) -> ValidationReport:
        issues: list[AuthoringIssue] = []
        solution_passes = 0
        ordered = catalog.ordered_missions()
        if catalog.declarative_levels:
            signatures: dict[tuple[object, ...], str] = {}
            for level in catalog.levels():
                sublevels = catalog.sublevels(level)
                if len(sublevels) < 5:
                    issues.append(AuthoringIssue(level.id, "a level must contain at least five sublevels"))
                if len(level.final_integrates) < 3:
                    issues.append(AuthoringIssue(
                        level.id, "a final battle must integrate at least three earlier sublevels"
                    ))
                for topic, practice_ids in level.topic_practice.items():
                    if len(practice_ids) < 5:
                        issues.append(AuthoringIssue(
                            level.id,
                            f"topic {topic!r} must be reinforced by at least five coding sublevels",
                        ))
                covered = set().union(*map(set, level.topic_practice.values()))
                if covered != set(level.sublevel_ids):
                    issues.append(AuthoringIssue(
                        level.id, "topic practice clusters must cover every sublevel"
                    ))
                for sublevel in sublevels:
                    starter_files = tuple(
                        (
                            path.relative_to(sublevel.root / sublevel.starter).as_posix(),
                            self._normalized_starter(path),
                        )
                        for path in sorted((sublevel.root / sublevel.starter).rglob("*"))
                        if path.is_file()
                    )
                    briefing_path = sublevel.content_path("briefing")
                    briefing = briefing_path.read_text(encoding="utf-8") if briefing_path.is_file() else ""
                    contract = (
                        briefing.split("## Your task", 1)[1].split("##", 1)[0].strip()
                        if "## Your task" in briefing else ""
                    )
                    checks = tuple(
                        (check.type, repr(sorted(check.config.items())))
                        for check in sublevel.checks
                    )
                    signature = (starter_files, contract, checks)
                    previous = signatures.get(signature)
                    if previous is not None:
                        issues.append(AuthoringIssue(
                            level.id,
                            f"duplicate sublevel exercise: {previous!r} and {sublevel.id!r} reuse starter, contract, and tests",
                        ))
                    else:
                        signatures[signature] = sublevel.id
        for index, mission in enumerate(ordered):
            if mission.activity not in _ACTIVITIES:
                issues.append(AuthoringIssue(mission.id, f"unsupported activity {mission.activity!r}"))
            if mission.platform not in _PLATFORMS:
                issues.append(AuthoringIssue(mission.id, f"unsupported platform {mission.platform!r}"))
            if not 20 <= mission.duration_minutes <= 120:
                issues.append(AuthoringIssue(
                    mission.id, "duration_minutes must be between 20 and 120"
                ))
            if index == 0 and mission.prerequisites:
                issues.append(AuthoringIssue(mission.id, "the first mission must have no prerequisite"))
            if index > 0 and ordered[index - 1].id not in mission.prerequisites:
                issues.append(AuthoringIssue(
                    mission.id, f"strict campaign order must include prerequisite {ordered[index - 1].id!r}"
                ))

            for check in mission.checks:
                issue = self.runner.registry.configuration_issue(check, mission)
                if issue is not None:
                    issues.append(AuthoringIssue(mission.id, issue))

            starter = mission.root / mission.starter
            if not starter.is_dir():
                issues.append(AuthoringIssue(mission.id, f"starter directory is missing: {mission.starter}"))
            for key, relative in mission.content.items():
                path = mission.root / relative
                if not path.is_file():
                    issues.append(AuthoringIssue(mission.id, f"missing content file for {key}: {relative}"))
                elif not path.read_text(encoding="utf-8").strip():
                    issues.append(AuthoringIssue(mission.id, f"empty content file for {key}: {relative}"))
            if not mission.hints:
                issues.append(AuthoringIssue(mission.id, "at least one hint is required"))
            for relative in mission.hints:
                path = mission.root / relative
                if not path.is_file():
                    issues.append(AuthoringIssue(mission.id, f"missing hint file: {relative}"))
                elif not path.read_text(encoding="utf-8").strip():
                    issues.append(AuthoringIssue(mission.id, f"empty hint file: {relative}"))
            reference = mission.root / "reference"
            if not reference.is_dir():
                issues.append(AuthoringIssue(mission.id, "reference directory is missing"))
            if run_solutions and reference.is_dir():
                with tempfile.TemporaryDirectory(prefix=f"learn-{mission.id}-") as tmp:
                    attempt_path = Path(tmp) / "attempt"
                    shutil.copytree(reference, attempt_path)
                    attempt = Attempt(
                        f"{mission.id}--reference", mission.id, mission.version, attempt_path
                    )
                    result = self.runner.test(mission, attempt, include_advisory=False)
                    if result.passed:
                        solution_passes += 1
                    else:
                        for check in result.checks:
                            if not check.passed:
                                issues.append(AuthoringIssue(
                                    mission.id,
                                    f"reference failed {check.name}: {check.message}"
                                ))
        return ValidationReport(
            mission_count=len(ordered),
            solution_pass_count=solution_passes,
            solution_checks_requested=run_solutions,
            issues=tuple(issues),
        )

    @staticmethod
    def _normalized_starter(path: Path) -> bytes:
        """Ignore decorative C comments when detecting relabelled exercises."""
        payload = path.read_bytes()
        if path.suffix not in {".c", ".h"}:
            return payload
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError:
            return payload
        text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
        text = re.sub(r"//[^\n]*", "", text)
        return re.sub(r"\s+", " ", text).strip().encode("utf-8")
