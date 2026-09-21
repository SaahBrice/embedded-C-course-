from __future__ import annotations

import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from learn_engine.cli import main
from learn_engine.catalog import Catalog
from tests.helpers import write_levels, write_mission


class EndToEndTests(unittest.TestCase):
    def test_real_level_one_flow_starts_with_main_and_clears_only_at_battle(self) -> None:
        # Defect guarded: fixtures pass while the shipped first level has stale
        # ordering, no copied briefing, opaque runs, or derived-only clearance.
        repository = Path(__file__).resolve().parent.parent
        catalog = Catalog.load(repository / "curriculum")
        level = catalog.levels()[0]

        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state"

            def run(*args: str):
                out, err = io.StringIO(), io.StringIO()
                code = main(
                    list(args), repository_root=repository, state_root=state,
                    stdout=out, stderr=err,
                )
                return code, out.getvalue(), err.getvalue()

            initial = run("map")[1]
            self.assertIn("[READY] Build Your First C Program", initial)
            self.assertIn("[LOCKED] Implement Your First Firmware Function", initial)
            self.assertIn("[LOCKED] Level 2:", initial)

            for index, mission in enumerate(catalog.sublevels(level)):
                started = run("start" if index == 0 else "continue")
                self.assertEqual(started[0], 0, started[2])
                attempt = state / "attempts" / f"{mission.id}--001"
                self.assertTrue((attempt / "BRIEFING.md").is_file())
                shutil.copytree(mission.root / "reference", attempt, dirs_exist_ok=True)
                if mission.id == "workstation-orientation":
                    visible = run("run")
                    self.assertEqual(visible[0], 0, visible[2])
                    self.assertIn("Actual return: -1", visible[1])
                submitted = run("submit")
                self.assertEqual(submitted[0], 0, submitted[2])
                if mission.id != level.final_battle_id:
                    self.assertNotIn("LEVEL CLEARED", submitted[1])
                else:
                    self.assertIn("LEVEL CLEARED: Orientation and Toolchain", submitted[1])

            progress = json.loads((state / "progress.json").read_text(encoding="utf-8"))
            self.assertEqual(
                progress["cleared_levels"][level.id]["final_battle_id"],
                level.final_battle_id,
            )
            campaign = run("map")[1]
            self.assertIn("[CLEARED] Level 1:", campaign)
            self.assertIn("[READY] Level 2:", campaign)
            self.assertIn("Final battle replay created", run("replay-final", level.id)[1])

    def test_fresh_learner_flow_crosses_every_engine_layer(self) -> None:
        # Defect guarded: individually working units are not connected into a playable loop.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            curriculum = root / "curriculum"
            write_mission(curriculum, "compile", 10)
            write_mission(curriculum, "debug", 20, prerequisites=("compile",))
            state = root / "learner-state"

            def run(*args: str):
                out, err = io.StringIO(), io.StringIO()
                code = main(list(args), repository_root=root, state_root=state, stdout=out, stderr=err)
                return code, out.getvalue(), err.getvalue()

            self.assertIn("[READY] Compile", run("map")[1])
            self.assertIn("compile--001", run("start")[1])
            self.assertEqual(run("test")[0], 1)
            (state / "attempts" / "compile--001" / "answer.c").write_text(
                "int main(void) { return 0; }\n", encoding="utf-8"
            )
            self.assertEqual(run("test")[0], 0)
            self.assertEqual(run("submit")[0], 0)
            self.assertIn("[READY] Debug", run("map")[1])
            self.assertIn("compile--002", run("replay", "compile")[1])
            self.assertIn("compile--002", run("start", "compile")[1])

    def test_final_battle_clears_level_and_unlocks_next_level(self) -> None:
        # Defect guarded: completing any sublevel clears a level, or the final
        # battle fails to unlock the next level and remains unreplayable.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            curriculum = root / "curriculum"
            write_mission(curriculum, "lesson", 10)
            write_mission(curriculum, "battle", 20, prerequisites=("lesson",))
            write_mission(curriculum, "next", 30, prerequisites=("battle",))
            write_mission(curriculum, "next-battle", 40, prerequisites=("next",))
            write_levels(curriculum, [
                {"id": "level-one", "title": "Level One", "order": 1,
                 "overview": "overviews/one.md", "sublevels": ["lesson", "battle"],
                 "final_battle": "battle"},
                {"id": "level-two", "title": "Level Two", "order": 2,
                 "overview": "overviews/two.md", "sublevels": ["next", "next-battle"],
                 "final_battle": "next-battle"},
            ])
            state = root / "state"

            def run(*args: str):
                out, err = io.StringIO(), io.StringIO()
                code = main(list(args), repository_root=root, state_root=state, stdout=out, stderr=err)
                return code, out.getvalue(), err.getvalue()

            started = run("start")[1]
            self.assertIn("Level overview", started)
            self.assertTrue((state / "attempts/lesson--001/BRIEFING.md").is_file())
            self.assertNotIn("Level overview", run("start")[1])
            (state / "attempts/lesson--001/answer.c").write_text("code\n")
            first_submit = run("submit")[1]
            self.assertNotIn("LEVEL CLEARED", first_submit)
            self.assertIn("Next sublevel unlocked", first_submit)
            run("continue")
            (state / "attempts/battle--001/answer.c").write_text("code\n")
            battle_submit = run("submit")[1]
            self.assertIn("LEVEL CLEARED: Level One", battle_submit)
            stored = json.loads((state / "progress.json").read_text(encoding="utf-8"))
            self.assertEqual(
                stored["cleared_levels"]["level-one"]["final_battle_id"], "battle"
            )
            campaign = run("map")[1]
            self.assertIn("[CLEARED] Level 1: Level One", campaign)
            self.assertIn("[READY] Level 2: Level Two", campaign)
            self.assertIn("Final battle replay created", run("replay-final", "level-one")[1])


if __name__ == "__main__":
    unittest.main()
