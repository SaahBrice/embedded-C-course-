from __future__ import annotations

import unittest
import hashlib
import re
import shutil
import subprocess
import tempfile
import tomllib
from pathlib import Path

from learn_engine.authoring import CurriculumValidator
from learn_engine.catalog import Catalog
from learn_engine.checkers import CheckerRegistry
from learn_engine.models import Attempt
from learn_engine.visible import VisibleRunner
from learn_engine.runner import MissionRunner


ROOT = Path(__file__).resolve().parent.parent


class CompleteCurriculumTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = Catalog.load(ROOT / "curriculum")

    def test_complete_campaign_scope_order_and_activity_mix(self) -> None:
        # Defect guarded: the shipped "complete" course omits a stage/topic or becomes repetitive.
        missions = self.catalog.ordered_missions()
        self.assertEqual(len(missions), 96)
        self.assertEqual({mission.stage for mission in missions}, set(range(1, 12)))
        self.assertGreaterEqual(len({mission.activity for mission in missions}), 10)
        required_ids = {
            "first-build", "binary-and-hex", "functions", "pointers", "memory-lifetime",
            "structs-unions-enums", "headers-and-linking", "undefined-behavior",
            "fixed-width-integers", "register-masks", "const-and-volatile", "datasheet-reading",
            "gpio", "interrupts", "timers", "uart", "adc", "pwm", "spi", "i2c",
            "state-machines", "event-loops", "ring-buffers", "callbacks", "hal-design",
            "unit-testing", "gdb-debugging", "sanitizers", "static-analysis", "concurrency",
            "api-design", "semantic-versioning", "packaging", "startup-code", "linker-scripts",
            "real-time-analysis", "rtos-concepts", "stm32-board-checkpoint", "data-logger-release",
        }
        self.assertEqual(required_ids - {mission.id for mission in missions}, set())
        for previous, current in zip(missions, missions[1:]):
            self.assertIn(previous.id, current.prerequisites)

    def test_complete_program_is_the_first_sublevel(self) -> None:
        # Defect guarded: a beginner is forced into declaration/definition and
        # unsigned-status semantics before seeing one whole runnable program.
        ids = [mission.id for mission in self.catalog.ordered_missions()[:2]]
        self.assertEqual(ids, ["first-build", "workstation-orientation"])
        first_level = self.catalog.levels()[0]
        self.assertEqual(first_level.sublevel_ids[:2], tuple(ids))

    def test_course_has_declarative_levels_distinct_sublevels_and_final_battles(self) -> None:
        # Defect guarded: repeated test modes are relabeled as sublevels or a
        # level has no single synthesis challenge at its end.
        self.assertTrue(self.catalog.declarative_levels)
        self.assertEqual(len(self.catalog.levels()), 11)
        seen: set[str] = set()
        for level in self.catalog.levels():
            sublevels = self.catalog.sublevels(level)
            with self.subTest(level=level.id):
                self.assertGreaterEqual(len(sublevels), 5)
                self.assertEqual(level.final_battle_id, sublevels[-1].id)
                self.assertGreaterEqual(len(level.final_integrates), 3)
                self.assertTrue(set(level.final_integrates) < set(level.sublevel_ids))
                self.assertNotIn(level.final_battle_id, level.final_integrates)
                for topic, practice_ids in level.topic_practice.items():
                    self.assertGreaterEqual(len(practice_ids), 5, topic)
                    self.assertEqual(len(set(practice_ids)), len(practice_ids), topic)
                    self.assertTrue(set(practice_ids) <= set(level.sublevel_ids), topic)
                self.assertEqual(
                    set().union(*map(set, level.topic_practice.values())),
                    set(level.sublevel_ids),
                )
                overview = level.overview.read_text(encoding="utf-8")
                for heading in (
                    "## Main objective", "## What you should know before starting",
                    "## Ordered sublevels", "## Final battle",
                ):
                    self.assertIn(heading, overview)
                fingerprints = {
                    (
                        tuple(
                            path.read_bytes()
                            for path in sorted((mission.root / "starter").rglob("*"))
                            if path.is_file()
                        ),
                        mission.content_path("briefing").read_bytes(),
                        tuple((check.type, repr(check.config)) for check in mission.checks),
                    )
                    for mission in sublevels
                }
                self.assertEqual(len(fingerprints), len(sublevels))
            seen.update(item.id for item in sublevels)
        self.assertEqual(seen, {item.id for item in self.catalog.ordered_missions()})

    def test_final_battles_are_integrative_coding_artifacts(self) -> None:
        # Defect guarded: a narrow one-function exercise is labelled a final
        # battle without actually combining earlier interfaces and skills.
        for level in self.catalog.levels():
            battle = self.catalog.final_battle(level)
            deterministic = list(battle.checks)
            with self.subTest(level=level.id):
                self.assertEqual(len(deterministic), 1)
                if deterministic[0].type == "c_harness":
                    header = (battle.root / "starter" / "task.h").read_text(encoding="utf-8")
                    declarations = re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\s*\([^;{}]*\)\s*;", header)
                    self.assertGreaterEqual(len(declarations), 3)
                else:
                    self.assertIn(deterministic[0].type, {"project_harness", "c_test_pair"})

    def test_lessons_are_substantive_and_objective_driven(self) -> None:
        # Defect guarded: generated level shells pass structure checks but do not teach the topic.
        for mission in self.catalog.ordered_missions():
            lesson = mission.content_path("lesson").read_text(encoding="utf-8")
            with self.subTest(mission=mission.id):
                self.assertGreaterEqual(len(lesson.split()), 180)
                self.assertIn("## What you are doing", lesson)
                self.assertIn("## Files you will edit", lesson)
                self.assertIn("## Required behavior", lesson)
                self.assertIn("## A practical way to begin", lesson)
                self.assertIn("## Common mistake", lesson)
                self.assertIn("## Success looks like", lesson)
                self.assertGreaterEqual(len(mission.objectives), 2)
                self.assertGreaterEqual(len(mission.hints), 3)

    def test_teaching_artifacts_are_specific_instead_of_repeated_filler(self) -> None:
        # Defect guarded: a generator changes only the title while publishing the same lesson/hint.
        missions = self.catalog.ordered_missions()
        for relative in ("lesson.md", "hints/01.md", "hints/02.md", "hints/03.md"):
            bodies = [(mission.root / relative).read_text(encoding="utf-8") for mission in missions]
            with self.subTest(relative=relative):
                self.assertEqual(len(bodies), len(set(bodies)))
        banned = "Implement every public function declared in task.h"
        for mission in missions:
            with self.subTest(mission=mission.id):
                self.assertNotIn(banned, "\n".join(
                    path.read_text(encoding="utf-8")
                    for path in (mission.root / mission.starter).rglob("*") if path.is_file()
                ))

    def test_all_reference_solutions_pass(self) -> None:
        # Defect guarded: a learner is assigned an exercise whose own model answer cannot pass.
        runner = MissionRunner(CheckerRegistry(ROOT))
        report = CurriculumValidator(ROOT, runner).validate_all(self.catalog, run_solutions=True)
        self.assertTrue(report.ok, report.render())
        self.assertEqual(report.solution_pass_count, len(self.catalog.ordered_missions()))

    def test_assessments_are_substantive_and_mission_specific(self) -> None:
        # Defect guarded: structurally valid missions pass via editable expected files or magic tokens.
        c_hashes: set[str] = set()
        c_count = 0
        for mission in self.catalog.ordered_missions():
            check_types = {check.type for check in mission.checks}
            with self.subTest(mission=mission.id):
                self.assertNotIn("text_regex", check_types)
                self.assertNotIn("markdown_response", check_types)
                self.assertTrue(check_types & {"c_harness", "c_program", "c_test_pair", "project_harness"})
                if "c_harness" in check_types:
                    c_count += 1
                    source = (mission.root / "reference" / "task.c").read_bytes()
                    digest = hashlib.sha256(source).hexdigest()
                    self.assertNotIn(digest, c_hashes)
                    c_hashes.add(digest)
                    self.assertTrue((mission.root / "checks" / "test.c").is_file())
        self.assertGreaterEqual(c_count, 90)

    def test_no_mission_requires_reflection_or_prose_quotas(self) -> None:
        # Defect guarded: practical work is blocked by a reflection or essay requirement.
        for mission in self.catalog.ordered_missions():
            with self.subTest(mission=mission.id):
                self.assertFalse(any(check.type == "markdown_response" for check in mission.checks))
                self.assertFalse(any(path.name in {"reflection.md", "answer.md"} for path in mission.root.rglob("*")))
                briefing = mission.content_path("briefing").read_text(encoding="utf-8")
                headings = re.findall(r"^## .+$", briefing, flags=re.MULTILINE)
                self.assertEqual(headings, [
                    "## Your task",
                    "## Why firmware engineers care",
                    "## Read the function signature",
                    "## Concrete examples",
                    "## Expected failure behavior",
                ])
                self.assertIn("./learn run", briefing)
                self.assertIn("./learn test", briefing)
                self.assertIn("curriculum/", briefing)

    def test_briefings_are_individually_specific_not_template_twins(self) -> None:
        # Defect guarded: changing only titles/contracts makes generated prose
        # look complete while leaving the learner with repeated filler.
        normalized: list[tuple[str, set[str]]] = []
        for mission in self.catalog.ordered_missions():
            briefing = mission.content_path("briefing").read_text(encoding="utf-8")
            prose = re.sub(r"```.*?```", "", briefing, flags=re.DOTALL)
            words = re.findall(r"[a-z0-9_]+", prose.casefold())
            with self.subTest(mission=mission.id):
                self.assertGreaterEqual(len(words), 100)
                self.assertIn("## Concrete examples", briefing)
                self.assertNotIn("Implement the declared interface.", briefing)
                self.assertNotIn("Handle boundaries correctly.", briefing)
                self.assertNotIn("The concrete engineering ticket is:", briefing)
            normalized.append((mission.id, set(words)))
        closest = (0.0, "", "")
        for index, (left_id, left) in enumerate(normalized):
            for right_id, right in normalized[index + 1:]:
                ratio = len(left & right) / len(left | right)
                if ratio > closest[0]:
                    closest = (ratio, left_id, right_id)
        # Shared operational instructions are intentionally consistent.  A
        # pair above this ceiling is still so similar that its concrete
        # firmware situation and concept explanation did not distinguish it.
        self.assertLess(closest[0], 0.89, closest)

    def test_generated_visible_drivers_report_real_call_returns(self) -> None:
        # Defect guarded: visible execution reports only whether a whole assert
        # became true and hides the learner function's actual return value.
        mission = self.catalog.by_id("workstation-orientation")
        visible = (mission.root / "checks" / "visible.c").read_text(encoding="utf-8")
        self.assertIn("Actual return:", visible)
        self.assertIn("Call and inputs:", visible)

    def test_first_sublevel_unambiguously_explains_the_function_only_job(self) -> None:
        # Defect guarded: a new learner cannot tell whether to add main, edit the
        # declaration, or define the function in task.c.
        briefing = self.catalog.by_id("workstation-orientation").content_path(
            "briefing"
        ).read_text(encoding="utf-8")
        for detail in (
            "define the function", "declared in `task.h`", "must **not** create `main`",
            "harnesses provide `main`", "unsigned", "`U` suffix",
            "firmware_status(0U)", "firmware_status(1U)", "firmware_status(42U)",
            "return `-1`", "return `0`",
        ):
            self.assertIn(detail, briefing)

    def test_all_published_sublevels_have_unique_coding_contracts(self) -> None:
        # Defect guarded: an old exercise is copied under a new topic title.
        fingerprints: set[tuple[object, ...]] = set()
        for mission in self.catalog.ordered_missions():
            briefing = mission.content_path("briefing").read_text(encoding="utf-8")
            contract = briefing.split("## Your task", 1)[1].split("##", 1)[0].strip()
            check_material = []
            for check in mission.checks:
                trusted = ""
                for field in ("harness", "good_source", "defective_source"):
                    relative = check.config.get(field)
                    if isinstance(relative, str) and (mission.root / relative).is_file():
                        trusted += (mission.root / relative).read_text(encoding="utf-8")
                check_material.append((check.type, repr(sorted(check.config.items())), trusted))
            fingerprint = (contract, tuple(check_material))
            with self.subTest(mission=mission.id):
                self.assertNotIn(fingerprint, fingerprints)
            fingerprints.add(fingerprint)
        self.assertEqual(len(fingerprints), 96)

    def test_compiler_warnings_briefing_explains_the_actual_problem(self) -> None:
        # Defect guarded: the briefing repeats abstract contract language without
        # telling a learner what the function means or which cases must work.
        briefing = self.catalog.by_id("compiler-warnings").content_path("briefing").read_text(
            encoding="utf-8"
        )
        for detail in (
            "12-bit ADC", "0 through 4095", "reference_mv", "out_mv",
            "code = 4095", "4096", "must not write", "uint32_t",
        ):
            self.assertIn(detail, briefing)
        self.assertIn("## Read the function signature", briefing)
        self.assertIn("## Concrete examples", briefing)
        self.assertIn("## Why firmware engineers care", briefing)

    def test_each_function_sublevel_has_a_visible_driver(self) -> None:
        # Defect guarded: a function-only sublevel offers only an opaque pass/fail exercise.
        function_missions = 0
        for mission in self.catalog.ordered_missions():
            if any(check.type == "c_harness" for check in mission.checks):
                function_missions += 1
                briefing = mission.content_path("briefing").read_text(encoding="utf-8")
                harness = mission.root / "checks" / "visible.c"
                with self.subTest(mission=mission.id):
                    self.assertTrue(harness.is_file())
                    self.assertIn("VISIBLE_CASE_COUNT", harness.read_text(encoding="utf-8"))
                    self.assertRegex(briefing, r"(?:provide|supplies) `main`")
        self.assertGreaterEqual(function_missions, 90)

    def test_course_uses_only_bounded_local_checks(self) -> None:
        # Defect guarded: a network-dependent or source-mutating assessment is
        # added to the learner's run, test, or submit path.
        allowed = {
            "file_exists", "text_regex", "markdown_response", "command", "c_harness",
            "c_program", "c_test_pair", "project_harness", "manual_evidence",
        }
        for mission in self.catalog.ordered_missions():
            with self.subTest(mission=mission.id):
                self.assertTrue({check.type for check in mission.checks} <= allowed)
                self.assertFalse(any(mission.root.rglob("*-rubric.md")))

    def test_every_visible_driver_accepts_its_reference_solution(self) -> None:
        # Defect guarded: a generated visible bridge disagrees with the sublevel's
        # authoritative harness or fails to link simulator support.
        visible = VisibleRunner(ROOT)
        with tempfile.TemporaryDirectory(prefix="visible-references-") as temporary:
            temporary_root = Path(temporary)
            for mission in self.catalog.ordered_missions():
                if not visible.available(mission):
                    continue
                attempt_root = temporary_root / mission.id
                shutil.copytree(mission.root / "reference", attempt_root)
                attempt = Attempt(
                    f"{mission.id}--reference", mission.id, mission.version, attempt_root
                )
                result = visible.run(mission, attempt)
                with self.subTest(mission=mission.id):
                    self.assertEqual(result.exit_code, 0, result.stdout + result.stderr)

    def test_representative_artifacts_match_their_ticket(self) -> None:
        # Defect guarded: per-stage boilerplate is published as an unrelated topic solution.
        expected_symbols = {
            "strings": "buffer_append",
            "uart": "uart_line_feed",
            "register-masks": "register_field_write",
            "state-machines": "controller_transition",
            "ring-buffers": "byte_ring_push",
            "integer-overflow": "checked_scale",
            "record-serialization": "record_serialize",
            "data-logger-integration": "logger_capture",
        }
        for mission_id, symbol in expected_symbols.items():
            mission = self.catalog.by_id(mission_id)
            with self.subTest(mission=mission_id):
                self.assertIn(symbol, (mission.root / "reference" / "task.c").read_text(encoding="utf-8"))
                self.assertIn(symbol, mission.content_path("lesson").read_text(encoding="utf-8"))

        sanitizer = self.catalog.by_id("sanitizers")
        flags = next(check.config.get("cflags", []) for check in sanitizer.checks if check.type == "c_harness")
        self.assertTrue(any("sanitize" in flag for flag in flags))

    def test_special_missions_use_authentic_assessment_shapes(self) -> None:
        # Defect guarded: tickets promise programs, learner tests, debugging, or installs but check a toy function/prose.
        expected = {
            "first-build": {"c_program"},
            "unit-testing": {"c_test_pair"},
            "packaging": {"project_harness"},
            "consumer-integration-release": {"project_harness"},
            "stm32-board-checkpoint": {"project_harness", "manual_evidence"},
        }
        for mission_id, expected_types in expected.items():
            mission = self.catalog.by_id(mission_id)
            with self.subTest(mission=mission_id):
                self.assertEqual({check.type for check in mission.checks}, expected_types)
        first = self.catalog.by_id("first-build")
        self.assertTrue((first.root / "starter" / "main.c").is_file())
        self.assertIn("int main(", (first.root / "reference" / "main.c").read_text(encoding="utf-8"))
        unit = self.catalog.by_id("unit-testing")
        self.assertTrue((unit.root / "starter" / "test.c").is_file())
        self.assertTrue((unit.root / "checks" / "good_module.c").is_file())
        self.assertTrue((unit.root / "checks" / "defective_module.c").is_file())
        debug = self.catalog.by_id("gdb-debugging")
        self.assertTrue((debug.root / "starter" / "gdb-transcript.txt").is_file())
        self.assertTrue((debug.root / "starter" / "faulty.c").is_file())

    def test_simulator_missions_link_and_call_the_shared_simulator(self) -> None:
        # Defect guarded: a mission labelled sim checks only pure arithmetic and never links the simulator.
        sim_missions = [mission for mission in self.catalog.ordered_missions() if mission.platform == "sim"]
        self.assertGreaterEqual(len(sim_missions), 12)
        for mission in sim_missions:
            harnesses = [check for check in mission.checks if check.type == "c_harness"]
            with self.subTest(mission=mission.id):
                self.assertEqual(len(harnesses), 1)
                config = harnesses[0].config
                self.assertTrue(config.get("support_sources"))
                self.assertEqual(config.get("support_include_dirs"), ["platforms/host/include"])
                combined = "\n".join(
                    (mission.root / area / "task.c").read_text(encoding="utf-8")
                    for area in ("starter", "reference")
                ) + (mission.root / "checks" / "test.c").read_text(encoding="utf-8")
                self.assertRegex(combined, r"\bsim_[a-z0-9_]+\s*\(")

    def test_pointer_lab_uses_pointer_and_count_contract(self) -> None:
        # Defect guarded: relationally comparing unrelated pointers invokes undefined behavior.
        mission = self.catalog.by_id("pointers")
        header = (mission.root / "reference" / "task.h").read_text(encoding="utf-8")
        harness = (mission.root / "checks" / "test.c").read_text(encoding="utf-8")
        self.assertIn("const int32_t *values, size_t count", header)
        self.assertNotRegex((mission.root / "reference" / "task.c").read_text(encoding="utf-8"), r"end\s*<\s*begin")
        self.assertIn("NULL, 0U", harness)
        self.assertIn("SIZE_MAX", harness)

    def test_generated_curriculum_reproduces_shipped_artifacts(self) -> None:
        # Defect guarded: hand-edited mission packages drift from the declared generator authority.
        with tempfile.TemporaryDirectory(prefix="curriculum-regeneration-") as tmp:
            generated = Path(tmp) / "curriculum"
            completed = subprocess.run(
                ["python3", "tools/build_curriculum.py", "--output", str(generated)],
                cwd=ROOT, capture_output=True, text=True, check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            shipped_files = {p.relative_to(ROOT / "curriculum") for p in (ROOT / "curriculum").rglob("*") if p.is_file()}
            generated_files = {p.relative_to(generated) for p in generated.rglob("*") if p.is_file()}
            self.assertEqual(generated_files, shipped_files)
            for relative in shipped_files:
                self.assertEqual((generated / relative).read_bytes(), (ROOT / "curriculum" / relative).read_bytes(), str(relative))

    def test_every_starter_requires_learner_work(self) -> None:
        # Defect guarded: a verbose starter satisfies its own assessment before the learner edits anything.
        runner = MissionRunner(CheckerRegistry(ROOT))
        unexpectedly_passing: list[str] = []
        for mission in self.catalog.ordered_missions():
            with tempfile.TemporaryDirectory(prefix=f"starter-{mission.id}-") as tmp:
                attempt_path = Path(tmp) / "attempt"
                shutil.copytree(mission.root / mission.starter, attempt_path)
                attempt = Attempt(
                    f"{mission.id}--starter", mission.id, mission.version, attempt_path
                )
                if runner.test(mission, attempt).passed:
                    unexpectedly_passing.append(mission.id)
        self.assertEqual(unexpectedly_passing, [])


if __name__ == "__main__":
    unittest.main()
