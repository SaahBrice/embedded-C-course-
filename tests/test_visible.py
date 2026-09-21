from __future__ import annotations

import io
import shutil
import tempfile
import unittest
from pathlib import Path

from learn_engine.cli import main
from learn_engine.models import Attempt, CheckSpec, Mission
from learn_engine.progress import ProgressStore
from learn_engine.visible import VisibleRunner


class VisibleRunnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.attempt_root = self.root / "attempt"
        self.mission_root = self.root / "mission"
        (self.mission_root / "checks").mkdir(parents=True)
        self.attempt_root.mkdir()
        (self.attempt_root / "task.h").write_text("int twice(int value);\n")
        (self.attempt_root / "task.c").write_text(
            '#include "task.h"\nint twice(int value) { return value; }\n'
        )
        (self.mission_root / "checks" / "visible.c").write_text(
            """#include "task.h"
#include <stdio.h>
static unsigned number, failures;
static void check(int passed, const char *expression) {
    ++number;
    printf("Case %u\\n  Input/check: %s\\n  Expected: true\\n  Actual: %s\\n  Result: %s\\n",
           number, expression, passed ? "true" : "false", passed ? "PASS" : "FAIL");
    if (!passed) ++failures;
}
#define assert(expression) check(!!(expression), #expression)
int main(void) { assert(twice(2) == 4); return failures == 0 ? 0 : 1; }
"""
        )
        check = CheckSpec("contract", "Contract", "c_harness", True, {
            "sources": ["task.c"], "harness": "checks/test.c",
            "cflags": ["-std=c11", "-Wall", "-Wextra", "-Werror"], "timeout": 10,
        })
        self.mission = Mission(
            "twice", "Twice", "2.0.0", 1, 1, "write", 30, "host", (),
            ("multiply",), "starter", (), {}, (check,), self.mission_root,
        )
        self.attempt = Attempt("twice--001", "twice", "2.0.0", self.attempt_root)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_visible_driver_reports_expected_actual_and_failure(self) -> None:
        # Defect guarded: function-only work can be judged only by an opaque harness.
        result = VisibleRunner(self.root).run(self.mission, self.attempt)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Input/check: twice(2) == 4", result.stdout)
        self.assertIn("Expected: true", result.stdout)
        self.assertIn("Actual: false", result.stdout)
        self.assertIn("Result: FAIL", result.stdout)

    def test_visible_driver_exposes_real_compiler_diagnostics(self) -> None:
        # Defect guarded: warning-focused work is hidden behind a generic failure.
        (self.attempt_root / "task.c").write_text(
            '#include "task.h"\nint twice(int value) { int unused = value; return value; }\n'
        )
        result = VisibleRunner(self.root).run(self.mission, self.attempt)
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("unused", result.stderr)


class VisibleCliTests(unittest.TestCase):
    def test_run_executes_generated_visible_driver(self) -> None:
        repository = Path(__file__).resolve().parent.parent
        with tempfile.TemporaryDirectory() as temporary:
            state = Path(temporary)
            main(["start"], repository_root=repository, state_root=state,
                 stdout=io.StringIO(), stderr=io.StringIO())
            ProgressStore(state / "progress.json").complete(
                "first-build", "2.0.0", "first-build--001"
            )
            main(["continue"], repository_root=repository, state_root=state,
                 stdout=io.StringIO(), stderr=io.StringIO())
            mission = next((repository / "curriculum").rglob("002-workstation-orientation"))
            attempt = state / "attempts" / "workstation-orientation--001"
            shutil.copy2(mission / "reference" / "task.c", attempt / "task.c")
            output, errors = io.StringIO(), io.StringIO()
            code = main(["run"], repository_root=repository, state_root=state,
                        stdout=output, stderr=errors)
            self.assertEqual(code, 0, errors.getvalue())
            self.assertIn("Call and inputs: firmware_status(0U)", output.getvalue())
            self.assertIn("Actual return: -1", output.getvalue())
            self.assertIn("Expected condition:", output.getvalue())
            self.assertIn("Observed condition: true", output.getvalue())


if __name__ == "__main__":
    unittest.main()
