from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from learn_engine.catalog import Catalog
from learn_engine.errors import CatalogError
from tests.helpers import write_levels, write_mission


class CatalogTests(unittest.TestCase):
    def test_discovers_missions_in_declared_order_not_directory_order(self) -> None:
        # Defect guarded: filesystem order accidentally determines progression.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_mission(root, "second", 20, prerequisites=("first",))
            write_mission(root, "first", 10)

            catalog = Catalog.load(root)

            self.assertEqual([m.id for m in catalog.ordered_missions()], ["first", "second"])
            self.assertEqual(catalog.by_id("second").prerequisites, ("first",))
            self.assertEqual(
                catalog.by_id("first").objectives,
                ("Practise the focused mission skill", "Produce a checked artifact"),
            )

    def test_rejects_duplicate_ids(self) -> None:
        # Defect guarded: a progress ID ambiguously refers to two missions.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_mission(root / "a", "same", 10)
            write_mission(root / "b", "same", 20)
            with self.assertRaisesRegex(CatalogError, "duplicate mission id"):
                Catalog.load(root)

    def test_rejects_missing_prerequisite(self) -> None:
        # Defect guarded: a mission is permanently locked by a misspelled dependency.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_mission(root, "orphan", 10, prerequisites=("missing",))
            with self.assertRaisesRegex(CatalogError, "unknown prerequisite"):
                Catalog.load(root)

    def test_rejects_prerequisite_cycle(self) -> None:
        # Defect guarded: circular prerequisites make progression impossible.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_mission(root / "a", "a", 10, prerequisites=("b",))
            write_mission(root / "b", "b", 20, prerequisites=("a",))
            with self.assertRaisesRegex(CatalogError, "cycle"):
                Catalog.load(root)

    def test_rejects_unknown_manifest_content_and_check_keys(self) -> None:
        # Defect guarded: misspelled manifest fields are silently ignored and weaken assessment.
        mutations = (
            ("platform = \"host\"", "platform = \"host\"\nsurprise = true", "top-level"),
            ("solution = \"solution.md\"", "solution = \"solution.md\"\nextra = \"x.md\"", "content"),
            ("required = true", "required = true\nsurprise = true", "check"),
        )
        for original, replacement, label in mutations:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                package = write_mission(root, "first", 10)
                manifest = package / "level.toml"
                manifest.write_text(
                    manifest.read_text(encoding="utf-8").replace(original, replacement),
                    encoding="utf-8",
                )
                with self.assertRaisesRegex(CatalogError, "unknown"):
                    Catalog.load(root)

    def test_requires_at_least_two_learning_objectives(self) -> None:
        # Defect guarded: a mission ships without enough explicit learning outcomes.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = write_mission(root, "first", 10)
            manifest = package / "level.toml"
            manifest.write_text(
                manifest.read_text(encoding="utf-8").replace(
                    'objectives = ["Practise the focused mission skill", "Produce a checked artifact"]',
                    'objectives = ["Practise the focused mission skill"]',
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(CatalogError, "at least two"):
                Catalog.load(root)

    def test_declarative_levels_group_ordered_sublevels_and_one_final_battle(self) -> None:
        # Defect guarded: stages are only labels and cannot drive a level/sublevel campaign.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_mission(root, "one", 10)
            write_mission(root, "battle", 20, prerequisites=("one",))
            write_levels(root, [{
                "id": "basics", "title": "Basics", "order": 1,
                "overview": "overviews/basics.md",
                "sublevels": ["one", "battle"], "final_battle": "battle",
            }])

            catalog = Catalog.load(root)
            level = catalog.level_by_id("basics")

            self.assertEqual([item.id for item in catalog.sublevels(level)], ["one", "battle"])
            self.assertEqual(catalog.final_battle(level).id, "battle")
            self.assertEqual(catalog.level_for("one").id, "basics")

    def test_level_manifest_rejects_missing_duplicate_or_nonfinal_battle(self) -> None:
        # Defect guarded: a sublevel belongs to no level, two levels, or an arbitrary battle.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_mission(root, "one", 10)
            write_mission(root, "two", 20, prerequisites=("one",))
            write_levels(root, [{
                "id": "bad", "order": 1, "overview": "bad.md",
                "sublevels": ["one", "one"], "final_battle": "one",
            }])
            with self.assertRaisesRegex(CatalogError, "exactly one level|duplicate"):
                Catalog.load(root)


if __name__ == "__main__":
    unittest.main()
