from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from learn_engine.authoring import CurriculumValidator
from learn_engine.catalog import Catalog
from learn_engine.checkers import CheckerRegistry
from learn_engine.runner import MissionRunner
from tests.helpers import write_levels, write_mission


class AuthoringValidatorTests(unittest.TestCase):
    def validator(self, root: Path):
        return CurriculumValidator(root, MissionRunner(CheckerRegistry(root)))

    def make_valid(self, root: Path):
        mission = write_mission(root / "curriculum", "first", 10)
        (mission / "reference").mkdir()
        (mission / "reference" / "answer.c").write_text("int main(void){return 0;}\n", encoding="utf-8")
        return Catalog.load(root / "curriculum")

    def test_valid_package_and_reference_solution_pass(self) -> None:
        # Defect guarded: the validator rejects authorable content or skips solution execution.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = self.validator(root).validate_all(self.make_valid(root), run_solutions=True)
            self.assertTrue(report.ok, report.render())
            self.assertIn("1 sublevel", report.render())
            self.assertIn("1 reference solution passed", report.render())

    def test_reports_missing_content_hint_starter_and_reference(self) -> None:
        # Defect guarded: an incomplete package ships and fails only after a learner starts it.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            catalog = self.make_valid(root)
            mission = catalog.by_id("first")
            (mission.root / "lesson.md").unlink()
            (mission.root / "hints/01.md").unlink()
            (mission.root / "starter").rmdir()
            for item in (mission.root / "reference").iterdir():
                item.unlink()
            (mission.root / "reference").rmdir()

            report = self.validator(root).validate_all(catalog, run_solutions=True)

            self.assertFalse(report.ok)
            rendered = report.render()
            for phrase in ("missing content", "missing hint", "starter directory", "reference directory"):
                self.assertIn(phrase, rendered)

    def test_reference_failure_names_mission_and_check(self) -> None:
        # Defect guarded: a reference answer that cannot pass is published without actionable evidence.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            catalog = self.make_valid(root)
            (catalog.by_id("first").root / "reference" / "answer.c").unlink()

            report = self.validator(root).validate_all(catalog, run_solutions=True)

            self.assertFalse(report.ok)
            self.assertIn("first", report.render())
            self.assertIn("Answer exists", report.render())

    def test_rejects_unsupported_checker_without_running_solutions(self) -> None:
        # Defect guarded: a typo in a checker type ships because validation notices it only while executing answers.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            catalog = self.make_valid(root)
            manifest = catalog.by_id("first").manifest_path
            manifest.write_text(
                manifest.read_text(encoding="utf-8").replace(
                    'type = "file_exists"', 'type = "not_a_checker"'
                ),
                encoding="utf-8",
            )
            catalog = Catalog.load(root / "curriculum")

            report = self.validator(root).validate_all(catalog, run_solutions=False)

            self.assertFalse(report.ok)
            self.assertIn("unsupported checker type", report.render())

    def test_level_validation_rejects_fewer_than_five_or_duplicate_sublevels(self) -> None:
        # Defect guarded: one exercise is presented as several sublevels by changing only its name.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            previous = None
            ids = []
            for index in range(5):
                mission_id = f"same-{index}"
                package = write_mission(
                    root / "curriculum", mission_id, (index + 1) * 10,
                    prerequisites=(() if previous is None else (previous,)),
                )
                (package / "reference").mkdir()
                ids.append(mission_id)
                previous = mission_id
            write_levels(root / "curriculum", [{
                "id": "duplicates", "order": 1, "overview": "overview.md",
                "sublevels": ids, "final_battle": ids[-1],
            }])
            catalog = Catalog.load(root / "curriculum")
            report = self.validator(root).validate_all(catalog)
            self.assertFalse(report.ok)
            self.assertIn("duplicate sublevel exercise", report.render())


if __name__ == "__main__":
    unittest.main()
