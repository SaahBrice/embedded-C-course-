from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


class DocumentationTests(unittest.TestCase):
    def test_required_guides_exist_without_placeholders(self) -> None:
        # Defect guarded: code ships without enough instructions to play or extend it.
        paths = [
            ROOT / "README.md",
            ROOT / "docs" / "GETTING_STARTED.md",
            ROOT / "docs" / "CURRICULUM.md",
            ROOT / "docs" / "AUTHORING.md",
            ROOT / "docs" / "STM32_SETUP.md",
        ]
        for path in paths:
            with self.subTest(path=path):
                content = path.read_text(encoding="utf-8")
                self.assertGreater(len(content.split()), 100)
                self.assertNotIn("TBD", content)
                self.assertNotIn("TODO", content)

    def test_documented_first_commands_execute(self) -> None:
        # Defect guarded: the onboarding commands are stale or the launcher is not executable.
        for command, expected in (
            (["./learn"], "Embedded C Career Game"),
            (["./learn", "doctor"], "read-only"),
            (["./learn", "map"], "[READY]"),
            (["./learn", "validate"], "Curriculum is valid"),
        ):
            with self.subTest(command=command):
                result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn(expected, result.stdout)

    def test_learner_guides_require_practical_work_not_reflections(self) -> None:
        # Defect guarded: regenerated missions stop requiring prose but onboarding still instructs it.
        for relative in ("README.md", "docs/GETTING_STARTED.md", "docs/CURRICULUM.md"):
            content = (ROOT / relative).read_text(encoding="utf-8").casefold()
            self.assertNotIn("reflection.md", content, relative)
            self.assertNotIn("analysis labs require", content, relative)

    def test_guides_describe_levels_sublevels_and_no_obsolete_command(self) -> None:
        # Defect guarded: onboarding teaches the removed repeated-test workflow.
        combined = "\n".join(
            (ROOT / relative).read_text(encoding="utf-8")
            for relative in ("README.md", "docs/GETTING_STARTED.md", "docs/CURRICULUM.md")
        ).casefold()
        self.assertIn("sublevel", combined)
        self.assertIn("final battle", combined)
        self.assertIn("./learn continue", combined)
        self.assertIn("./learn replay-final", combined)
        self.assertNotIn("./learn practice", combined)
        self.assertNotIn("five-round", combined)


if __name__ == "__main__":
    unittest.main()
