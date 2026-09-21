from __future__ import annotations

from .color import Palette
from .models import CheckResult, MissionResult


def render_check(result: CheckResult, palette: Palette | None = None) -> str:
    palette = palette or Palette(False)
    mark = "PASS" if result.passed else "FAIL"
    colored_mark = palette.success(f"[{mark}]") if result.passed else palette.error(f"[{mark}]")
    lines = [f"{colored_mark} {result.name}: {result.message}"]
    if result.stdout.strip():
        lines.extend((f"  {palette.info('stdout:')}", *[f"    {line}" for line in result.stdout.rstrip().splitlines()]))
    if result.stderr.strip():
        lines.extend((f"  {palette.warning('stderr:')}", *[f"    {line}" for line in result.stderr.rstrip().splitlines()]))
    return "\n".join(lines)


def render_result(result: MissionResult, palette: Palette | None = None) -> str:
    return "\n".join(render_check(check, palette) for check in result.checks) + "\n"


def render_markdown(content: str, palette: Palette) -> str:
    """Apply light terminal styling while leaving redirected Markdown unchanged."""
    lines: list[str] = []
    in_code = False
    for line in content.splitlines(keepends=True):
        bare = line.rstrip("\r\n")
        ending = line[len(bare):]
        if bare.lstrip().startswith("```"):
            lines.append(palette.accent(bare) + ending)
            in_code = not in_code
        elif not in_code and bare.startswith("#"):
            lines.append(palette.title(bare) + ending)
        elif not in_code and bare.startswith(">"):
            lines.append(palette.warning(bare) + ending)
        elif not in_code and bare.startswith("- "):
            lines.append(palette.info("•") + bare[1:] + ending)
        else:
            lines.append(line)
    return "".join(lines)
