from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from learn_engine.checkers import CheckerRegistry
from learn_engine.models import Attempt, CheckSpec, Mission
from learn_engine.runner import MissionRunner


class CheckerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.attempt_path = self.root / "attempt"
        self.attempt_path.mkdir()
        self.attempt = Attempt("demo--001", "demo", "1.0.0", self.attempt_path)
        self.registry = CheckerRegistry(repository_root=self.root)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def spec(self, check_type: str, **config):
        return CheckSpec("check", "Focused check", check_type, True, config)

    def test_file_and_text_checkers_report_observable_results(self) -> None:
        # Defect guarded: declarative checks pass missing or incorrect learner artifacts.
        missing = self.registry.run(self.spec("file_exists", path="answer.c"), self.attempt)
        self.assertFalse(missing.passed)
        self.assertEqual(missing.category, "learner_failure")

        (self.attempt_path / "answer.c").write_text("int answer = 42;\n", encoding="utf-8")
        exists = self.registry.run(self.spec("file_exists", path="answer.c"), self.attempt)
        contains = self.registry.run(
            self.spec("text_regex", path="answer.c", pattern=r"answer\s*=\s*42"), self.attempt
        )
        self.assertTrue(exists.passed)
        self.assertTrue(contains.passed)

    def test_command_preserves_output_and_classifies_exit(self) -> None:
        # Defect guarded: compiler/test evidence is discarded or mislabeled as engine failure.
        result = self.registry.run(
            self.spec(
                "command",
                argv=["python3", "-c", "import sys; print('out'); print('err', file=sys.stderr); sys.exit(3)"],
            ),
            self.attempt,
        )
        self.assertFalse(result.passed)
        self.assertEqual(result.category, "learner_failure")
        self.assertEqual(result.exit_code, 3)
        self.assertEqual(result.stdout.strip(), "out")
        self.assertEqual(result.stderr.strip(), "err")

    def test_command_distinguishes_missing_tool_and_timeout(self) -> None:
        # Defect guarded: unavailable tooling and hung checks are blamed on learner code.
        missing = self.registry.run(
            self.spec("command", argv=["definitely-not-an-installed-tool-92741"]), self.attempt
        )
        timed_out = self.registry.run(
            self.spec("command", argv=["python3", "-c", "import time; time.sleep(5)"], timeout=0.05),
            self.attempt,
        )
        self.assertEqual(missing.category, "missing_tool")
        self.assertEqual(timed_out.category, "timeout")
        self.assertIn("timed out", timed_out.message)

    def test_paths_cannot_escape_attempt(self) -> None:
        # Defect guarded: a mission check reads arbitrary files outside the attempt.
        result = self.registry.run(self.spec("file_exists", path="../secret"), self.attempt)
        self.assertEqual(result.category, "configuration_error")

    def test_runner_ignores_optional_failure_for_completion(self) -> None:
        # Defect guarded: an optional stretch check incorrectly blocks progression.
        required = CheckSpec("required", "Required", "file_exists", True, {"path": "ok.c"})
        optional = CheckSpec("optional", "Optional", "file_exists", False, {"path": "bonus.c"})
        (self.attempt_path / "ok.c").write_text("ok", encoding="utf-8")
        mission = Mission(
            "demo", "Demo", "1.0.0", 10, 1, "write", 45, "host", (),
            ("Pass the required check",), "starter", (),
            {"briefing": "briefing.md", "lesson": "lesson.md", "debrief": "debrief.md", "solution": "solution.md"},
            (required, optional), self.root,
        )
        result = MissionRunner(self.registry).test(mission, self.attempt)
        self.assertTrue(result.passed)
        self.assertFalse(result.checks[1].passed)

    def test_c_harness_uses_immutable_mission_test_not_attempt_build_files(self) -> None:
        # Defect guarded: learner can edit Makefile/expected.txt and bypass the real acceptance test.
        mission_root = self.root / "mission"
        (mission_root / "checks").mkdir(parents=True)
        (mission_root / "checks" / "test.c").write_text(
            "int add(int, int); int main(void) { return add(20, 22) == 42 ? 0 : 1; }\n",
            encoding="utf-8",
        )
        (self.attempt_path / "task.c").write_text("int add(int a,int b){(void)a;(void)b;return 0;}\n")
        (self.attempt_path / "Makefile").write_text("test:\n\t@true\n", encoding="utf-8")
        spec = self.spec("c_harness", sources=["task.c"], harness="checks/test.c")
        mission = Mission(
            "demo", "Demo", "1.0.0", 10, 1, "write", 45, "host", (),
            ("Implement checked addition",), "starter", (),
            {"briefing": "briefing.md", "lesson": "lesson.md", "debrief": "debrief.md", "solution": "solution.md"},
            (spec,), mission_root,
        )

        failing = self.registry.run(spec, self.attempt, mission)
        self.assertFalse(failing.passed)
        (self.attempt_path / "task.c").write_text("int add(int a,int b){return a+b;}\n")
        passing = self.registry.run(spec, self.attempt, mission)
        self.assertTrue(passing.passed, passing.stderr)

    def test_markdown_response_requires_structure_and_substance_without_magic_token(self) -> None:
        # Defect guarded: an analysis mission passes by copying one published marker token.
        path = self.attempt_path / "answer.md"
        spec = self.spec(
            "markdown_response",
            path="answer.md",
            headings=["Prediction", "Evidence", "Decision"],
            minimum_words=30,
        )
        path.write_text("FINAL: MAGIC\n", encoding="utf-8")
        self.assertFalse(self.registry.run(spec, self.attempt).passed)
        path.write_text(
            "# Analysis\n\n## Prediction\nThe value changes after the load.\n\n"
            "## Evidence\nThe trace shows a read, mask, and write while preserving unrelated bits. "
            "The zero and maximum field cases remain inside the field width.\n\n"
            "## Decision\nUse an unsigned mask and shift, validate the input range first, and perform one explicit update.\n",
            encoding="utf-8",
        )
        self.assertTrue(self.registry.run(spec, self.attempt).passed)

    def test_markdown_response_rejects_empty_repetitive_and_concept_free_prose(self) -> None:
        # Defect guarded: headings plus repeated filler satisfy an analysis assessment.
        path = self.attempt_path / "analysis.md"
        spec = self.spec(
            "markdown_response",
            path="analysis.md",
            headings=["Prediction", "Evidence", "Decision"],
            minimum_words=12,
            minimum_section_words=3,
            minimum_unique_words=10,
            maximum_word_fraction=0.20,
            required_concept_groups=[
                ["volatile", "observable"],
                ["interrupt", "isr"],
                ["atomic", "critical section"],
            ],
        )
        cases = (
            "## Prediction\n\n## Evidence\ninterrupt trace data\n\n## Decision\natomic update now\n",
            "## Prediction\nfiller filler filler filler\n\n## Evidence\nfiller filler filler filler\n\n## Decision\nfiller filler filler filler\n",
            "## Prediction\nvalue may change later\n\n## Evidence\nthe trace records each update\n\n## Decision\nuse a guarded state change\n",
        )
        for content in cases:
            path.write_text(content, encoding="utf-8")
            self.assertFalse(self.registry.run(spec, self.attempt).passed)

        path.write_text(
            "## Prediction\nThe volatile value remains observable.\n\n"
            "## Evidence\nAn interrupt trace captures changing state.\n\n"
            "## Decision\nUse one atomic critical section boundary.\n",
            encoding="utf-8",
        )
        self.assertTrue(self.registry.run(spec, self.attempt).passed)

    def test_c_harness_uses_copied_learner_tree_and_repository_support_without_path_leaks(self) -> None:
        # Defect guarded: simulator support is unavailable, or learner code runs with repository access exported.
        support = self.root / "support"
        (support / "include").mkdir(parents=True)
        (support / "src").mkdir()
        (support / "include" / "support.h").write_text("int base_value(void);\n", encoding="utf-8")
        (support / "src" / "support.c").write_text(
            '#include "support.h"\nint base_value(void){return 40;}\n', encoding="utf-8"
        )
        mission_root = self.root / "mission"
        (mission_root / "checks").mkdir(parents=True)
        (mission_root / "checks" / "test.c").write_text(
            '#include <stdlib.h>\nint answer(void);\nint main(void){'
            'return getenv("LEARN_REPOSITORY") == 0 && answer() == 42 ? 0 : 1;}\n',
            encoding="utf-8",
        )
        (self.attempt_path / "src").mkdir()
        (self.attempt_path / "include").mkdir()
        (self.attempt_path / "include" / "task.h").write_text("int answer(void);\n", encoding="utf-8")
        (self.attempt_path / "src" / "task.c").write_text(
            '#include "../include/task.h"\n#include "support.h"\n'
            'int answer(void){return base_value()+2;}\n', encoding="utf-8"
        )
        spec = self.spec(
            "c_harness", sources=["src/task.c"], harness="checks/test.c",
            support_sources=["support/src/support.c"],
            support_include_dirs=["support/include"],
        )
        mission = Mission(
            "demo", "Demo", "1.0.0", 10, 1, "write", 45, "host", (),
            ("Use simulator support", "Preserve private repository paths"), "starter", (),
            {"briefing": "briefing.md", "lesson": "lesson.md", "debrief": "debrief.md", "solution": "solution.md"},
            (spec,), mission_root,
        )

        result = self.registry.run(spec, self.attempt, mission)

        self.assertTrue(result.passed, result.stderr)

    def test_c_program_strictly_checks_stdout_and_exit_status(self) -> None:
        # Defect guarded: a compilable program passes despite producing the wrong observable result.
        (self.attempt_path / "main.c").write_text(
            '#include <stdio.h>\nint main(void){puts("ready");return 3;}\n', encoding="utf-8"
        )
        passing = self.registry.run(
            self.spec("c_program", sources=["main.c"], expected_stdout="ready\n", expected_exit=3),
            self.attempt,
        )
        wrong = self.registry.run(
            self.spec("c_program", sources=["main.c"], expected_stdout="wrong\n", expected_exit=3),
            self.attempt,
        )
        self.assertTrue(passing.passed, passing.stderr)
        self.assertFalse(wrong.passed)

    def test_c_test_pair_requires_tests_to_kill_the_defective_implementation(self) -> None:
        # Defect guarded: learner tests pass without distinguishing correct and defective behavior.
        mission_root = self.root / "mission-pair"
        (mission_root / "checks").mkdir(parents=True)
        (mission_root / "checks" / "good.c").write_text("int answer(void){return 42;}\n", encoding="utf-8")
        (mission_root / "checks" / "bad.c").write_text("int answer(void){return 0;}\n", encoding="utf-8")
        test_path = self.attempt_path / "test.c"
        test_path.write_text("int answer(void);int main(void){return answer()==42?0:1;}\n", encoding="utf-8")
        spec = self.spec(
            "c_test_pair", test_sources=["test.c"],
            good_source="checks/good.c", defective_source="checks/bad.c",
        )
        mission = Mission(
            "demo", "Demo", "1.0.0", 10, 1, "write", 45, "host", (),
            ("Test correct behavior", "Reject a known defect"), "starter", (),
            {"briefing": "briefing.md", "lesson": "lesson.md", "debrief": "debrief.md", "solution": "solution.md"},
            (spec,), mission_root,
        )
        self.assertTrue(self.registry.run(spec, self.attempt, mission).passed)
        test_path.write_text("int main(void){return 0;}\n", encoding="utf-8")
        self.assertFalse(self.registry.run(spec, self.attempt, mission).passed)

    def test_project_harness_receives_only_copied_attempt_and_empty_build_directory(self) -> None:
        # Defect guarded: a trusted project checker mutates learner work or inherits repository path exports.
        (self.attempt_path / "project.txt").write_text("learner project\n", encoding="utf-8")
        mission_root = self.root / "mission-project"
        (mission_root / "checks").mkdir(parents=True)
        (mission_root / "checks" / "verify.py").write_text(
            "import os, pathlib, sys\n"
            "attempt, build = map(pathlib.Path, sys.argv[1:])\n"
            "assert pathlib.Path.cwd() == build and not any(build.iterdir())\n"
            "assert (attempt / 'project.txt').read_text() == 'learner project\\n'\n"
            "assert 'LEARN_REPOSITORY' not in os.environ and 'LEARN_ATTEMPT' not in os.environ\n",
            encoding="utf-8",
        )
        spec = self.spec("project_harness", harness="checks/verify.py", timeout=3)
        mission = Mission(
            "demo", "Demo", "1.0.0", 10, 1, "project", 45, "host", (),
            ("Build a project", "Verify its behavior"), "starter", (),
            {"briefing": "briefing.md", "lesson": "lesson.md", "debrief": "debrief.md", "solution": "solution.md"},
            (spec,), mission_root,
        )
        self.assertTrue(self.registry.run(spec, self.attempt, mission).passed)

    def test_manual_evidence_is_structured_and_explicitly_not_machine_verified(self) -> None:
        # Defect guarded: a free-form claim is presented as proof that physical hardware worked.
        evidence = self.attempt_path / "hardware.json"
        spec = self.spec(
            "manual_evidence", path="hardware.json",
            required_fields=["board", "observations", "performed_on_hardware"],
        )
        evidence.write_text(
            '{"board":"NUCLEO-C031C6","observations":"LED toggled","performed_on_hardware":true}\n',
            encoding="utf-8",
        )
        result = self.registry.run(spec, self.attempt)
        self.assertTrue(result.passed)
        self.assertIn("not machine-verified", result.message)
        evidence.write_text('{"board":"","observations":[],"performed_on_hardware":false}\n', encoding="utf-8")
        self.assertFalse(self.registry.run(spec, self.attempt).passed)

    def test_new_checker_configuration_is_rejected_statically(self) -> None:
        # Defect guarded: malformed advanced checker configuration ships until a learner executes it.
        mission_root = self.root / "static-mission"
        (mission_root / "checks").mkdir(parents=True)
        for name in ("test.c", "good.c", "bad.c", "verify.py"):
            (mission_root / "checks" / name).write_text("placeholder\n", encoding="utf-8")
        mission = Mission(
            "demo", "Demo", "1.0.0", 10, 1, "write", 45, "host", (),
            ("Validate configuration", "Fail before learner execution"), "starter", (),
            {"briefing": "briefing.md", "lesson": "lesson.md", "debrief": "debrief.md", "solution": "solution.md"},
            (), mission_root,
        )
        malformed = (
            self.spec(
                "markdown_response", path="answer.md", headings=["Evidence"], minimum_words=10,
                required_concept_groups=[],
            ),
            self.spec("c_program", sources=["../main.c"], expected_stdout="", expected_exit=0),
            self.spec(
                "c_test_pair", test_sources=[], good_source="checks/good.c",
                defective_source="checks/bad.c",
            ),
            self.spec("project_harness", harness="../verify.py"),
            self.spec("manual_evidence", path="evidence.json", required_fields=[]),
        )

        issues = [self.registry.configuration_issue(spec, mission) for spec in malformed]

        self.assertTrue(all(issue is not None and "invalid" in issue for issue in issues), issues)

if __name__ == "__main__":
    unittest.main()
