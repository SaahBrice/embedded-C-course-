from __future__ import annotations

import io
import os
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

from learn_engine.cli import main
from tests.helpers import write_mission


class TtyBuffer(io.StringIO):
    def isatty(self) -> bool:
        return True


class CliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.curriculum = self.root / "curriculum"
        write_mission(self.curriculum, "first", 10)
        write_mission(self.curriculum, "second", 20, prerequisites=("first",))
        self.state = self.root / "state"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_cli(self, *args: str):
        out, err = io.StringIO(), io.StringIO()
        code = main(list(args), repository_root=self.root, state_root=self.state, stdout=out, stderr=err)
        return code, out.getvalue(), err.getvalue()

    def test_map_marks_only_first_mission_available(self) -> None:
        # Defect guarded: strict campaign order is not visible or a locked mission appears playable.
        code, output, errors = self.run_cli("map")
        self.assertEqual(code, 0)
        self.assertIn("[READY] First", output)
        self.assertIn("[LOCKED] Second", output)
        self.assertEqual(errors, "")

    def test_tty_output_colors_semantic_map_states(self) -> None:
        # Defect guarded: an interactive terminal receives the same monochrome map as redirected output.
        output = TtyBuffer()
        with patch.dict(os.environ, {"TERM": "xterm-256color"}, clear=True):
            code = main(
                ["map"], repository_root=self.root, state_root=self.state,
                stdout=output, stderr=TtyBuffer(),
            )
        rendered = output.getvalue()
        self.assertEqual(code, 0)
        self.assertIn("\033[1;36mEmbedded C Career Map\033[0m", rendered)
        self.assertIn("\033[1;32m[READY]\033[0m", rendered)
        self.assertIn("\033[2;37m[LOCKED]\033[0m", rendered)

    def test_no_color_environment_disables_tty_colors(self) -> None:
        # Defect guarded: NO_COLOR is ignored and escape codes pollute an explicitly plain terminal.
        output = TtyBuffer()
        with patch.dict(os.environ, {"TERM": "xterm-256color", "NO_COLOR": "1"}, clear=True):
            code = main(
                ["map"], repository_root=self.root, state_root=self.state,
                stdout=output, stderr=TtyBuffer(),
            )
        self.assertEqual(code, 0)
        self.assertNotIn("\033[", output.getvalue())

    def test_start_test_submit_unlock_and_replay(self) -> None:
        # Defect guarded: submission unlocks without checks or replay overwrites the first attempt.
        code, started, _ = self.run_cli("start")
        self.assertEqual(code, 0)
        self.assertIn("first--001", started)

        code, _, errors = self.run_cli("submit")
        self.assertEqual(code, 1)
        self.assertIn("missing required file", errors)
        attempt = self.state / "attempts" / "first--001"
        (attempt / "answer.c").write_text("int main(void) { return 0; }\n", encoding="utf-8")

        code, output, _ = self.run_cli("submit")
        self.assertEqual(code, 0)
        self.assertIn("Sublevel complete", output)
        code, output, _ = self.run_cli("map")
        self.assertIn("[DONE] First", output)
        self.assertIn("[READY] Second", output)

        code, output, _ = self.run_cli("replay", "first")
        self.assertEqual(code, 0)
        self.assertIn("first--002", output)
        self.assertTrue((attempt / "answer.c").exists())

    def test_locked_start_and_uncompleted_replay_are_user_errors(self) -> None:
        # Defect guarded: the learner bypasses ordering or receives an engine-failure exit code.
        code, _, error = self.run_cli("start", "second")
        self.assertEqual(code, 1)
        self.assertIn("locked", error.lower())
        code, _, error = self.run_cli("replay", "first")
        self.assertEqual(code, 1)
        self.assertIn("not completed", error.lower())

    def test_workspace_cannot_forge_metadata_to_complete_locked_mission(self) -> None:
        # Defect guarded: learner-controlled .attempt.json selects a locked mission at submit time.
        self.run_cli("start")
        attempt = self.state / "attempts" / "first--001"
        (attempt / ".attempt.json").write_text(
            '{"id":"first--001","mission_id":"second","mission_version":"1.0.0"}',
            encoding="utf-8",
        )
        (attempt / "answer.c").write_text("int main(void) { return 0; }\n", encoding="utf-8")

        code, _, _ = self.run_cli("submit")
        map_output = self.run_cli("map")[1]

        self.assertEqual(code, 0)
        self.assertIn("[DONE] First", map_output)
        self.assertIn("[READY] Second", map_output)

    def test_hint_is_incremental_and_solution_does_not_complete(self) -> None:
        # Defect guarded: hints repeat forever or displaying a solution mutates progression.
        self.run_cli("start")
        code, hint, _ = self.run_cli("hint")
        self.assertEqual(code, 0)
        self.assertIn("Create answer.c", hint)
        code, _, error = self.run_cli("hint")
        self.assertEqual(code, 1)
        self.assertIn("No more hints", error)
        code, solution, _ = self.run_cli("solution")
        self.assertEqual(code, 0)
        self.assertIn("Useful learning content", solution)
        code, map_output, _ = self.run_cli("map")
        self.assertIn("[READY] First", map_output)

    def test_reset_requires_yes_and_removes_only_named_attempt(self) -> None:
        # Defect guarded: a broad or accidental reset erases learner state.
        self.run_cli("start")
        code, _, error = self.run_cli("reset", "first--001")
        self.assertEqual(code, 1)
        self.assertIn("--yes", error)
        code, output, _ = self.run_cli("reset", "first--001", "--yes")
        self.assertEqual(code, 0)
        self.assertIn("Reset first--001", output)

if __name__ == "__main__":
    unittest.main()
