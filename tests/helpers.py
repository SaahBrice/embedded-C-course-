from __future__ import annotations

from pathlib import Path


def write_levels(root: Path, levels: list[dict[str, object]]) -> None:
    lines = ["schema_version = 1", ""]
    for level in levels:
        sublevels = ", ".join(f'"{item}"' for item in level["sublevels"])
        sublevel_ids = list(level["sublevels"])
        final_battle = str(level["final_battle"])
        default_integrates = [item for item in sublevel_ids if item != final_battle][-3:]
        integrates = ", ".join(
            f'"{item}"' for item in level.get("final_integrates", default_integrates)
        )
        practice_entries = level.get("topic_practice", {
            item: sublevel_ids for item in sublevel_ids
        })
        outcomes = ", ".join(f'"{item}"' for item in level.get("learning_outcomes", ["Learn", "Build"]))
        lines.extend([
            "[[levels]]",
            f'id = "{level["id"]}"',
            f'title = "{level.get("title", str(level["id"]).title())}"',
            f'order = {level["order"]}',
            f'objective = "{level.get("objective", "Complete the level")}"',
            f'learning_outcomes = [{outcomes}]',
            f'overview = "{level["overview"]}"',
            f'sublevels = [{sublevels}]',
            f'final_battle = "{final_battle}"',
            f'final_integrates = [{integrates}]',
            "topic_practice = [",
            *(
                f'  {{ topic = "{topic}", sublevels = [{", ".join(fchr + item + fchr for item in practice)}] }},'
                for topic, practice in practice_entries.items()
                for fchr in ['"']
            ),
            "]",
            "",
        ])
        overview = root / str(level["overview"])
        overview.parent.mkdir(parents=True, exist_ok=True)
        overview.write_text(f'# {level.get("title", level["id"])}\n\nLevel overview.\n')
    (root / "levels.toml").write_text("\n".join(lines), encoding="utf-8")


def write_mission(
    root: Path,
    mission_id: str,
    order: int,
    *,
    prerequisites: tuple[str, ...] = (),
    title: str | None = None,
) -> Path:
    """Create a minimal real mission package for public-behaviour tests."""
    mission = root / f"{order:03d}-{mission_id}"
    (mission / "starter").mkdir(parents=True)
    (mission / "hints").mkdir()
    title = title or mission_id.replace("-", " ").title()
    prereq = ", ".join(f'"{item}"' for item in prerequisites)
    (mission / "level.toml").write_text(
        f'''id = "{mission_id}"
title = "{title}"
version = "1.0.0"
order = {order}
stage = 1
activity = "write"
duration_minutes = 45
platform = "host"
prerequisites = [{prereq}]
objectives = ["Practise the focused mission skill", "Produce a checked artifact"]
starter = "starter"
hints = ["hints/01.md"]

[content]
briefing = "briefing.md"
lesson = "lesson.md"
debrief = "debrief.md"
solution = "solution.md"

[[checks]]
id = "answer"
name = "Answer exists"
type = "file_exists"
path = "answer.c"
required = true
''',
        encoding="utf-8",
    )
    for name in ("briefing.md", "lesson.md", "debrief.md", "solution.md"):
        (mission / name).write_text(f"# {title}\n\nUseful learning content.\n", encoding="utf-8")
    (mission / "hints/01.md").write_text("# Hint\n\nCreate answer.c.\n", encoding="utf-8")
    return mission
