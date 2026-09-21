from __future__ import annotations

import re
import tomllib
from pathlib import Path
from typing import Any

from .errors import CatalogError
from .models import CheckSpec, CourseLevel, Mission, ValidationIssue


_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
_REQUIRED_TOP_LEVEL = {
    "id", "title", "version", "order", "stage", "activity",
    "duration_minutes", "platform", "prerequisites", "starter",
    "objectives", "hints", "content", "checks",
}
_REQUIRED_CONTENT = {"briefing", "lesson", "debrief", "solution"}
_REQUIRED_CHECK = {"id", "name", "type", "required"}
_CHECK_CONFIG_KEYS = {
    "file_exists": {"path"},
    "text_regex": {"path", "pattern"},
    "markdown_response": {
        "path", "headings", "minimum_words", "minimum_section_words",
        "minimum_unique_words", "maximum_word_fraction", "required_concept_groups",
    },
    "command": {"argv", "timeout"},
    "c_harness": {
        "sources", "harness", "cflags", "compiler", "timeout",
        "support_sources", "support_include_dirs",
    },
    "c_program": {
        "sources", "expected_stdout", "expected_exit", "stdin", "args",
        "cflags", "compiler", "timeout",
    },
    "c_test_pair": {
        "test_sources", "good_source", "defective_source", "cflags", "compiler", "timeout",
    },
    "project_harness": {"harness", "timeout"},
    "manual_evidence": {"path", "required_fields"},
}
_ALL_CHECK_CONFIG_KEYS = set().union(*_CHECK_CONFIG_KEYS.values())


def _relative_path(value: str, field: str) -> str:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise CatalogError(f"{field} must be a safe relative path: {value!r}")
    return value


def _expect(data: dict[str, Any], key: str, kind: type, source: Path) -> Any:
    if key not in data or not isinstance(data[key], kind):
        raise CatalogError(f"{source}: {key!r} must be {kind.__name__}")
    return data[key]


def load_mission(manifest: Path) -> Mission:
    try:
        with manifest.open("rb") as stream:
            data = tomllib.load(stream)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise CatalogError(f"cannot read {manifest}: {exc}") from exc

    missing = sorted(_REQUIRED_TOP_LEVEL - data.keys())
    if missing:
        raise CatalogError(f"{manifest}: missing fields: {', '.join(missing)}")
    unknown = sorted(data.keys() - _REQUIRED_TOP_LEVEL)
    if unknown:
        raise CatalogError(f"{manifest}: unknown top-level fields: {', '.join(unknown)}")

    mission_id = _expect(data, "id", str, manifest)
    if not _ID_RE.fullmatch(mission_id):
        raise CatalogError(f"{manifest}: invalid mission id {mission_id!r}")
    order = _expect(data, "order", int, manifest)
    stage = _expect(data, "stage", int, manifest)
    duration = _expect(data, "duration_minutes", int, manifest)
    if order < 0 or stage < 1 or duration < 1:
        raise CatalogError(f"{manifest}: order, stage, and duration must be positive")

    prereqs = _expect(data, "prerequisites", list, manifest)
    objectives = _expect(data, "objectives", list, manifest)
    hints = _expect(data, "hints", list, manifest)
    if len(objectives) < 2 or not all(isinstance(item, str) and item.strip() for item in objectives):
        raise CatalogError(f"{manifest}: objectives must contain at least two non-empty strings")
    if not all(isinstance(item, str) for item in prereqs + hints):
        raise CatalogError(f"{manifest}: prerequisites and hints must contain strings")
    starter = _relative_path(_expect(data, "starter", str, manifest), "starter")
    safe_hints = tuple(_relative_path(item, "hint") for item in hints)

    content = _expect(data, "content", dict, manifest)
    missing_content = sorted(_REQUIRED_CONTENT - content.keys())
    if missing_content:
        raise CatalogError(f"{manifest}: missing content fields: {', '.join(missing_content)}")
    unknown_content = sorted(content.keys() - _REQUIRED_CONTENT)
    if unknown_content:
        raise CatalogError(f"{manifest}: unknown content fields: {', '.join(unknown_content)}")
    safe_content: dict[str, str] = {}
    for key in _REQUIRED_CONTENT:
        safe_content[key] = _relative_path(_expect(content, key, str, manifest), f"content.{key}")

    raw_checks = _expect(data, "checks", list, manifest)
    if not raw_checks:
        raise CatalogError(f"{manifest}: at least one check is required")
    checks: list[CheckSpec] = []
    seen_checks: set[str] = set()
    for raw in raw_checks:
        if not isinstance(raw, dict):
            raise CatalogError(f"{manifest}: each check must be a table")
        missing_check = sorted(_REQUIRED_CHECK - raw.keys())
        if missing_check:
            raise CatalogError(f"{manifest}: check missing fields: {', '.join(missing_check)}")
        check_type = _expect(raw, "type", str, manifest)
        allowed_config = _CHECK_CONFIG_KEYS.get(check_type, _ALL_CHECK_CONFIG_KEYS)
        unknown_check = sorted(raw.keys() - _REQUIRED_CHECK - allowed_config)
        if unknown_check:
            raise CatalogError(f"{manifest}: unknown check fields: {', '.join(unknown_check)}")
        check_id = _expect(raw, "id", str, manifest)
        if check_id in seen_checks:
            raise CatalogError(f"{manifest}: duplicate check id {check_id!r}")
        seen_checks.add(check_id)
        config = {k: v for k, v in raw.items() if k not in _REQUIRED_CHECK}
        for path_key in ("path",):
            if path_key in config and isinstance(config[path_key], str):
                config[path_key] = _relative_path(config[path_key], f"check.{path_key}")
        checks.append(CheckSpec(
            id=check_id,
            name=_expect(raw, "name", str, manifest),
            type=check_type,
            required=_expect(raw, "required", bool, manifest),
            config=config,
        ))

    return Mission(
        id=mission_id,
        title=_expect(data, "title", str, manifest),
        version=_expect(data, "version", str, manifest),
        order=order,
        stage=stage,
        activity=_expect(data, "activity", str, manifest),
        duration_minutes=duration,
        platform=_expect(data, "platform", str, manifest),
        prerequisites=tuple(prereqs),
        objectives=tuple(objectives),
        starter=starter,
        hints=safe_hints,
        content=safe_content,
        checks=tuple(checks),
        root=manifest.parent.resolve(),
    )


class Catalog:
    def __init__(
        self, root: Path, missions: tuple[Mission, ...], levels: tuple[CourseLevel, ...],
        *, declarative_levels: bool,
    ):
        self.root = root.resolve()
        self._missions = missions
        self._by_id = {mission.id: mission for mission in missions}
        self._levels = levels
        self._levels_by_id = {level.id: level for level in levels}
        self.declarative_levels = declarative_levels
        self._level_by_sublevel = {
            sublevel_id: level for level in levels for sublevel_id in level.sublevel_ids
        }

    @classmethod
    def load(cls, root: Path) -> "Catalog":
        root = root.resolve()
        missions = tuple(load_mission(path) for path in sorted(root.rglob("level.toml")))
        if not missions:
            raise CatalogError(f"no missions found under {root}")

        by_id: dict[str, Mission] = {}
        orders: dict[int, str] = {}
        for mission in missions:
            if mission.id in by_id:
                raise CatalogError(f"duplicate mission id {mission.id!r}")
            if mission.order in orders:
                raise CatalogError(
                    f"duplicate mission order {mission.order}: {orders[mission.order]!r} and {mission.id!r}"
                )
            by_id[mission.id] = mission
            orders[mission.order] = mission.id

        for mission in missions:
            for prerequisite in mission.prerequisites:
                if prerequisite not in by_id:
                    raise CatalogError(
                        f"mission {mission.id!r} has unknown prerequisite {prerequisite!r}"
                    )

        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(mission_id: str) -> None:
            if mission_id in visiting:
                raise CatalogError(f"prerequisite cycle includes {mission_id!r}")
            if mission_id in visited:
                return
            visiting.add(mission_id)
            for prerequisite in by_id[mission_id].prerequisites:
                visit(prerequisite)
            visiting.remove(mission_id)
            visited.add(mission_id)

        for mission_id in by_id:
            visit(mission_id)
        levels_path = root / "levels.toml"
        if levels_path.is_file():
            levels = cls._load_levels(levels_path, missions, root)
            declarative = True
        else:
            grouped: dict[int, list[Mission]] = {}
            for mission in sorted(missions, key=lambda item: (item.order, item.id)):
                grouped.setdefault(mission.stage, []).append(mission)
            levels = tuple(
                CourseLevel(
                    id=f"stage-{stage}", title=f"Stage {stage}", order=stage,
                    objective=f"Complete stage {stage}",
                    learning_outcomes=("Complete each sublevel", "Pass the final battle"),
                    overview=items[0].content_path("briefing"),
                    sublevel_ids=tuple(item.id for item in items),
                    final_battle_id=items[-1].id,
                    final_integrates=tuple(item.id for item in items[:-1][-3:]),
                    topic_practice={
                        item.id: tuple(candidate.id for candidate in items)
                        for item in items
                    },
                )
                for stage, items in sorted(grouped.items())
            )
            declarative = False
        return cls(root, missions, levels, declarative_levels=declarative)

    @staticmethod
    def _load_levels(path: Path, missions: tuple[Mission, ...], root: Path) -> tuple[CourseLevel, ...]:
        try:
            with path.open("rb") as stream:
                document = tomllib.load(stream)
        except (OSError, tomllib.TOMLDecodeError) as exc:
            raise CatalogError(f"cannot read {path}: {exc}") from exc
        if set(document) != {"schema_version", "levels"} or document.get("schema_version") != 1:
            raise CatalogError(f"{path}: expected level schema_version 1 and a levels array")
        raw_levels = document.get("levels")
        if not isinstance(raw_levels, list) or not raw_levels:
            raise CatalogError(f"{path}: levels must be a non-empty array")
        mission_ids = {mission.id for mission in missions}
        assigned: list[str] = []
        seen_ids: set[str] = set()
        seen_orders: set[int] = set()
        levels: list[CourseLevel] = []
        required = {
            "id", "title", "order", "objective", "learning_outcomes", "overview",
            "sublevels", "final_battle", "final_integrates", "topic_practice",
        }
        for raw in raw_levels:
            if not isinstance(raw, dict) or set(raw) != required:
                raise CatalogError(
                    f"{path}: every level must contain exactly {', '.join(sorted(required))}"
                )
            level_id = raw["id"]
            order = raw["order"]
            sublevels = raw["sublevels"]
            outcomes = raw["learning_outcomes"]
            if not isinstance(level_id, str) or not _ID_RE.fullmatch(level_id) or level_id in seen_ids:
                raise CatalogError(f"{path}: invalid or duplicate level id {level_id!r}")
            if not isinstance(order, int) or isinstance(order, bool) or order < 1 or order in seen_orders:
                raise CatalogError(f"{path}: invalid or duplicate level order {order!r}")
            if not isinstance(sublevels, list) or not sublevels or not all(
                isinstance(item, str) for item in sublevels
            ):
                raise CatalogError(f"{path}: level {level_id!r} needs a non-empty sublevels array")
            if len(set(sublevels)) != len(sublevels):
                raise CatalogError(f"{path}: level {level_id!r} has duplicate sublevels")
            unknown = set(sublevels) - mission_ids
            if unknown:
                raise CatalogError(
                    f"{path}: level {level_id!r} has unknown sublevels: {', '.join(sorted(unknown))}"
                )
            final_battle = raw["final_battle"]
            if final_battle != sublevels[-1]:
                raise CatalogError(f"{path}: level {level_id!r} final battle must be its last sublevel")
            final_integrates = raw["final_integrates"]
            if (
                not isinstance(final_integrates, list)
                or not final_integrates
                or not all(isinstance(item, str) for item in final_integrates)
                or len(set(final_integrates)) != len(final_integrates)
                or not set(final_integrates) < set(sublevels)
                or final_battle in final_integrates
            ):
                raise CatalogError(
                    f"{path}: level {level_id!r} final_integrates must name unique earlier sublevels"
                )
            raw_practice = raw["topic_practice"]
            if not isinstance(raw_practice, list) or not raw_practice:
                raise CatalogError(f"{path}: level {level_id!r} needs topic_practice entries")
            topic_practice: dict[str, tuple[str, ...]] = {}
            for entry in raw_practice:
                if not isinstance(entry, dict) or set(entry) != {"topic", "sublevels"}:
                    raise CatalogError(
                        f"{path}: level {level_id!r} topic_practice entries need topic and sublevels"
                    )
                topic = entry["topic"]
                practice = entry["sublevels"]
                if (
                    not isinstance(topic, str)
                    or not topic.strip()
                    or topic in topic_practice
                    or not isinstance(practice, list)
                    or not practice
                    or not all(isinstance(item, str) for item in practice)
                    or len(set(practice)) != len(practice)
                    or not set(practice) <= set(sublevels)
                ):
                    raise CatalogError(
                        f"{path}: invalid topic_practice coverage for {topic!r}"
                    )
                topic_practice[topic] = tuple(practice)
            covered_sublevels = set().union(*map(set, topic_practice.values()))
            if covered_sublevels != set(sublevels):
                raise CatalogError(
                    f"{path}: topic_practice clusters must cover every sublevel"
                )
            if not isinstance(outcomes, list) or len(outcomes) < 2 or not all(
                isinstance(item, str) and item.strip() for item in outcomes
            ):
                raise CatalogError(f"{path}: level {level_id!r} needs at least two learning outcomes")
            overview_value = raw["overview"]
            if not isinstance(overview_value, str):
                raise CatalogError(f"{path}: level {level_id!r} overview must be a path")
            overview = (root / _relative_path(overview_value, "level.overview")).resolve()
            if root not in overview.parents or not overview.is_file():
                raise CatalogError(f"{path}: missing level overview {overview_value!r}")
            for field in ("title", "objective"):
                if not isinstance(raw[field], str) or not raw[field].strip():
                    raise CatalogError(f"{path}: level {level_id!r} {field} must not be empty")
            seen_ids.add(level_id)
            seen_orders.add(order)
            assigned.extend(sublevels)
            levels.append(CourseLevel(
                level_id, raw["title"], order, raw["objective"], tuple(outcomes), overview,
                tuple(sublevels), final_battle, tuple(final_integrates), topic_practice,
            ))
        expected = [
            mission.id for mission in sorted(missions, key=lambda item: (item.order, item.id))
        ]
        if assigned != expected:
            raise CatalogError(
                f"{path}: every sublevel must appear in exactly one level and preserve campaign order"
            )
        return tuple(sorted(levels, key=lambda item: (item.order, item.id)))

    def ordered_missions(self) -> tuple[Mission, ...]:
        return tuple(sorted(self._missions, key=lambda mission: (mission.order, mission.id)))

    def by_id(self, mission_id: str) -> Mission:
        try:
            return self._by_id[mission_id]
        except KeyError as exc:
            raise CatalogError(f"unknown mission {mission_id!r}") from exc

    def levels(self) -> tuple[CourseLevel, ...]:
        return self._levels

    def level_by_id(self, level_id: str) -> CourseLevel:
        try:
            return self._levels_by_id[level_id]
        except KeyError as exc:
            raise CatalogError(f"unknown level {level_id!r}") from exc

    def level_for(self, sublevel_id: str) -> CourseLevel:
        try:
            return self._level_by_sublevel[sublevel_id]
        except KeyError as exc:
            raise CatalogError(f"sublevel {sublevel_id!r} does not belong to a level") from exc

    def sublevels(self, level: CourseLevel) -> tuple[Mission, ...]:
        return tuple(self.by_id(item) for item in level.sublevel_ids)

    def final_battle(self, level: CourseLevel) -> Mission:
        return self.by_id(level.final_battle_id)

    def validate(self) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        for mission in self.ordered_missions():
            for path in mission.content.values():
                if not (mission.root / path).is_file():
                    issues.append(ValidationIssue(mission.id, f"missing content file: {path}"))
            for path in mission.hints:
                if not (mission.root / path).is_file():
                    issues.append(ValidationIssue(mission.id, f"missing hint file: {path}"))
            if not (mission.root / mission.starter).is_dir():
                issues.append(ValidationIssue(mission.id, f"missing starter directory: {mission.starter}"))
        return issues
