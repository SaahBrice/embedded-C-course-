from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import TextIO

from .attempts import AttemptStore
from .catalog import Catalog
from .checkers import CheckerRegistry
from .color import Palette
from .errors import AttemptError, CatalogError, LearnError, ProgressError
from .doctor import TOOLS, tool_version
from .models import CourseLevel, Mission, MissionResult
from .progress import Progress, ProgressStore
from .visible import VisibleRunner
from .render import render_markdown, render_result
from .runner import MissionRunner


class UserCommandError(LearnError):
    pass


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="./learn",
        description="Embedded C Career Game — learn by doing real engineering work.",
    )
    commands = parser.add_subparsers(dest="command")
    commands.add_parser("map", help="show campaign progress")
    start = commands.add_parser("start", help="start or resume the next sublevel")
    start.add_argument("sublevel", nargs="?", help="optional level or sublevel id")
    start.add_argument("--new", action="store_true", help="create a fresh attempt")
    commands.add_parser("continue", help="continue with the next required sublevel")
    commands.add_parser("status", help="show the active level, sublevel, and attempt")
    commands.add_parser("level", help="read the current level overview")
    sublevels = commands.add_parser("sublevels", help="show DONE, READY, and LOCKED sublevels")
    sublevels.add_argument("level_id", nargs="?")
    commands.add_parser("lesson", help="read the active sublevel briefing and lesson")
    commands.add_parser("test", help="run checks without completing the sublevel")
    commands.add_parser("run", help="compile and run all visible examples for the active exercise")
    commands.add_parser("hint", help="reveal the next hint")
    commands.add_parser("solution", help="read the full explanation or model solution")
    commands.add_parser("submit", help="run checks and complete a passing sublevel")
    replay = commands.add_parser("replay", help="replay a completed sublevel")
    replay.add_argument("sublevel")
    replay_final = commands.add_parser("replay-final", help="replay a cleared level's final battle")
    replay_final.add_argument("level_id")
    reset = commands.add_parser("reset", help="remove one named attempt")
    reset.add_argument("attempt_id")
    reset.add_argument("--yes", action="store_true", help="confirm this attempt reset")
    validate = commands.add_parser("validate", help="validate all curriculum packages")
    validate.add_argument("--all-solutions", action="store_true")
    commands.add_parser("doctor", help="inspect required and optional development tools")
    return parser


def _next_mission(catalog: Catalog, progress: Progress) -> Mission | None:
    for mission in catalog.ordered_missions():
        if mission.id not in progress.completed:
            return mission
    return None


def _accessible(mission: Mission, current: Mission | None, progress: Progress) -> bool:
    return mission.id in progress.completed or (current is not None and mission.id == current.id)


def _level_complete(level: CourseLevel, progress: Progress) -> bool:
    return level.id in progress.cleared_levels


def _current_level(catalog: Catalog, progress: Progress) -> CourseLevel | None:
    current = _next_mission(catalog, progress)
    return catalog.level_for(current.id) if current is not None else None


def _write_sublevels(
    catalog: Catalog, level: CourseLevel, progress: Progress, stream: TextIO, palette: Palette,
) -> None:
    current = _next_mission(catalog, progress)
    stream.write(palette.title(f"Level {level.order}: {level.title}") + "\n")
    for index, mission in enumerate(catalog.sublevels(level), 1):
        if mission.id in progress.completed:
            state = "DONE"
        elif current is not None and mission.id == current.id:
            state = "READY"
        else:
            state = "LOCKED"
        label = " FINAL BATTLE" if mission.id == level.final_battle_id else ""
        stream.write(f"  [{state}] {index}. {mission.title}{label} ({mission.id})\n")


def _active(attempts: AttemptStore, catalog: Catalog):
    attempt = attempts.active()
    if attempt is None:
        raise UserCommandError("No active attempt. Run './learn start' first.")
    return catalog.by_id(attempt.mission_id), attempt


def _run_checks(
    runner: MissionRunner,
    mission: Mission,
    attempt,
    stdout: TextIO,
    stderr: TextIO,
) -> tuple[int, MissionResult]:
    result = runner.test(mission, attempt)
    stream = stdout if result.passed else stderr
    output = render_result(result, Palette.for_stream(stream))
    if result.passed:
        stdout.write(output)
        return 0, result
    error_categories = {check.category for check in result.checks if not check.passed}
    stderr.write(output)
    if error_categories & {"configuration_error", "engine_error", "missing_tool"}:
        return 2, result
    return 1, result


def main(
    argv: list[str] | None = None,
    *,
    repository_root: Path | None = None,
    state_root: Path | None = None,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    out_color = Palette.for_stream(stdout)
    err_color = Palette.for_stream(stderr)
    parser = _parser()
    if not argv:
        parser.print_help(file=stdout)
        return 0
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code)

    root = (repository_root or Path(__file__).resolve().parent.parent).resolve()
    state = (state_root or root / ".learn").resolve()

    if args.command == "doctor":
        stdout.write(out_color.title("Embedded C tool doctor") + "\n")
        for label, executable in TOOLS:
            version = tool_version(executable)
            status = out_color.warning(version) if version == "not found" else out_color.success(version)
            stdout.write(f"  {out_color.info(label)}: {status}\n")
        stdout.write(out_color.muted("Doctor is read-only: no build, USB access, or flash operation was performed.") + "\n")
        return 0

    try:
        catalog = Catalog.load(root / "curriculum")
        progress_store = ProgressStore(state / "progress.json")
        progress = progress_store.load()
        attempts = AttemptStore(state / "attempts")
        runner = MissionRunner(CheckerRegistry(root))

        if args.command == "map":
            current = _next_mission(catalog, progress)
            stdout.write(out_color.title("Embedded C Career Map") + "\n")
            def marker(state_name: str) -> str:
                value = f"[{state_name}]"
                if state_name in {"CLEARED", "DONE"}:
                    return out_color.info(value)
                if state_name == "READY":
                    return out_color.success(value)
                return out_color.muted(value)
            for level in catalog.levels():
                if _level_complete(level, progress):
                    status = "CLEARED"
                elif current is not None and current.id in level.sublevel_ids:
                    status = "READY"
                else:
                    status = "LOCKED"
                stdout.write(f"{marker(status)} Level {level.order}: {level.title} ({level.id})\n")
                for mission in catalog.sublevels(level):
                    if mission.id in progress.completed:
                        sublevel_status = "DONE"
                    elif current is not None and mission.id == current.id:
                        sublevel_status = "READY"
                    else:
                        sublevel_status = "LOCKED"
                    battle = " FINAL BATTLE" if mission.id == level.final_battle_id else ""
                    stdout.write(
                        f"    {marker(sublevel_status)} {mission.title}{battle} ({mission.id})\n"
                    )
            if current is None:
                stdout.write(out_color.success("Campaign complete — every sublevel and final battle is replayable.") + "\n")
            return 0

        if args.command in {"start", "continue"}:
            current = _next_mission(catalog, progress)
            requested = args.sublevel if args.command == "start" else None
            if requested:
                if requested in {level.id for level in catalog.levels()}:
                    level = catalog.level_by_id(requested)
                    mission = next(
                        (item for item in catalog.sublevels(level) if item.id not in progress.completed),
                        catalog.final_battle(level),
                    )
                else:
                    mission = catalog.by_id(requested)
            else:
                if current is None:
                    raise UserCommandError("Campaign complete. Use './learn replay <sublevel>' or './learn replay-final <level>'.")
                mission = current
            if not _accessible(mission, current, progress):
                raise UserCommandError(f"Sublevel {mission.id!r} is locked. Complete earlier sublevels first.")
            level = catalog.level_for(mission.id)
            first_level_entry = not any(
                attempts.has_attempt_for(sublevel_id) for sublevel_id in level.sublevel_ids
            )
            attempt = attempts.start(mission, force_new=getattr(args, "new", False))
            if first_level_entry and not _level_complete(level, progress):
                stdout.write(render_markdown(level.overview.read_text(encoding="utf-8"), out_color))
                stdout.write("\n\n")
            stdout.write(
                f"{out_color.title(f'Level {level.order}: {level.title}')}\n"
                f"{out_color.info('Sublevel:')} {mission.title}"
                f"{' — FINAL BATTLE' if mission.id == level.final_battle_id else ''}\n"
                f"{out_color.info('Attempt:')} {attempt.id}\n"
                f"{out_color.info('Workspace:')} {attempt.path}\n\n"
            )
            stdout.write(render_markdown(mission.content_path("briefing").read_text(encoding="utf-8"), out_color))
            stdout.write(
                "\n" + out_color.success(
                    f"Open {attempt.path / 'BRIEFING.md'}, edit the named source file, then run './learn run' or './learn test'."
                ) + "\n"
            )
            return 0

        if args.command == "status":
            mission, attempt = _active(attempts, catalog)
            level = catalog.level_for(mission.id)
            stdout.write(
                f"{out_color.title('Active level:')} {level.title} ({level.id})\n"
                f"{out_color.title('Active sublevel:')} {mission.title} ({mission.id})"
                f"{' — FINAL BATTLE' if mission.id == level.final_battle_id else ''}\n"
                f"{out_color.info('Attempt:')} {attempt.id}\n"
                f"{out_color.info('Workspace:')} {attempt.path}\n"
                f"{out_color.info('Briefing file:')} {attempt.path / 'BRIEFING.md'}\n"
            )
            return 0

        if args.command == "level":
            active = attempts.active()
            if active is not None:
                level = catalog.level_for(active.mission_id)
            else:
                level = _current_level(catalog, progress)
                if level is None:
                    raise UserCommandError("The campaign is complete; choose a level from './learn map'.")
            stdout.write(render_markdown(level.overview.read_text(encoding="utf-8"), out_color))
            return 0

        if args.command == "sublevels":
            if args.level_id:
                level = catalog.level_by_id(args.level_id)
            else:
                active = attempts.active()
                level = (
                    catalog.level_for(active.mission_id) if active is not None
                    else _current_level(catalog, progress)
                )
                if level is None:
                    raise UserCommandError("The campaign is complete; provide a level id from './learn map'.")
            _write_sublevels(catalog, level, progress, stdout, out_color)
            return 0

        if args.command == "lesson":
            mission, _ = _active(attempts, catalog)
            stdout.write(render_markdown(mission.content_path("briefing").read_text(encoding="utf-8"), out_color))
            stdout.write("\n\n")
            stdout.write(render_markdown(mission.content_path("lesson").read_text(encoding="utf-8"), out_color))
            return 0

        if args.command == "hint":
            mission, attempt = _active(attempts, catalog)
            index = attempts.reveal_hint(attempt.id, len(mission.hints))
            stdout.write(render_markdown(mission.root.joinpath(mission.hints[index]).read_text(encoding="utf-8"), out_color))
            return 0

        if args.command == "solution":
            mission, _ = _active(attempts, catalog)
            stdout.write(render_markdown(mission.content_path("solution").read_text(encoding="utf-8"), out_color))
            return 0

        if args.command == "test":
            mission, attempt = _active(attempts, catalog)
            return _run_checks(runner, mission, attempt, stdout, stderr)[0]

        if args.command == "run":
            mission, attempt = _active(attempts, catalog)
            visible_runner = VisibleRunner(root)
            if not visible_runner.available(mission):
                return _run_checks(runner, mission, attempt, stdout, stderr)[0]
            result = visible_runner.run(mission, attempt)
            stream = stdout if result.exit_code == 0 else stderr
            palette = out_color if result.exit_code == 0 else err_color
            stream.write(palette.title(f"Visible run: {mission.title}") + "\n")
            stream.write(result.stdout)
            stream.write(result.stderr)
            stream.write(
                palette.success("Visible examples passed.")
                if result.exit_code == 0 else
                palette.warning("Visible run found a problem; the failed expression above shows the case to inspect.")
            )
            stream.write("\n")
            return result.exit_code

        if args.command == "submit":
            mission, attempt = _active(attempts, catalog)
            level = catalog.level_for(mission.id)
            exit_code, result = _run_checks(runner, mission, attempt, stdout, stderr)
            if not result.passed:
                return exit_code
            progress_store.complete(mission.id, mission.version, attempt.id)
            progress = progress_store.load()
            stdout.write(out_color.success(f"Sublevel complete: {mission.title}") + "\n\n")
            stdout.write(render_markdown(mission.content_path("debrief").read_text(encoding="utf-8"), out_color))
            battle_completed = (
                mission.id == level.final_battle_id
                and all(item in progress.completed for item in level.sublevel_ids)
            )
            if battle_completed:
                progress_store.clear_level(level.id, mission.id, attempt.id)
                progress = progress_store.load()
                stdout.write(
                    "\n" + out_color.success(
                        f"LEVEL CLEARED: {level.title}. The next level is now unlocked."
                    ) + "\n"
                )
            else:
                next_sublevel = _next_mission(catalog, progress)
                if next_sublevel is not None:
                    stdout.write(
                        "\n" + out_color.success(
                            f"Next sublevel unlocked: {next_sublevel.title}. Run './learn continue'."
                        ) + "\n"
                    )
            return 0

        if args.command == "replay":
            mission = catalog.by_id(args.sublevel)
            if mission.id not in progress.completed:
                raise UserCommandError(f"Sublevel {mission.id!r} is not completed and cannot be replayed.")
            attempt = attempts.replay(mission)
            stdout.write(
                f"{out_color.success('Replay created:')} {attempt.id}\n"
                f"{out_color.info('Workspace:')} {attempt.path}\n"
            )
            return 0

        if args.command == "replay-final":
            level = catalog.level_by_id(args.level_id)
            if not _level_complete(level, progress):
                raise UserCommandError(f"Level {level.id!r} is not cleared yet.")
            battle = catalog.final_battle(level)
            attempt = attempts.replay(battle)
            stdout.write(
                f"{out_color.success('Final battle replay created:')} {attempt.id}\n"
                f"{out_color.info('Workspace:')} {attempt.path}\n"
                f"{out_color.info('Briefing file:')} {attempt.path / 'BRIEFING.md'}\n"
            )
            return 0

        if args.command == "reset":
            if not args.yes:
                raise UserCommandError("Reset was not performed. Add --yes to confirm this one attempt.")
            attempts.reset(args.attempt_id, confirmed=True)
            stdout.write(out_color.warning(f"Reset {args.attempt_id}. Completion history was not changed.") + "\n")
            return 0

        if args.command == "validate":
            from .authoring import CurriculumValidator

            report = CurriculumValidator(root, runner).validate_all(
                catalog, run_solutions=args.all_solutions
            )
            stream = stdout if report.ok else stderr
            stream.write(report.render())
            return 0 if report.ok else 2
        raise UserCommandError(f"unknown command {args.command!r}")
    except UserCommandError as exc:
        stderr.write(err_color.error(f"Error: {exc}") + "\n")
        return 1
    except AttemptError as exc:
        stderr.write(err_color.error(f"Error: {exc}") + "\n")
        return 1
    except (CatalogError, ProgressError, OSError) as exc:
        stderr.write(err_color.error(f"Engine error: {exc}") + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
