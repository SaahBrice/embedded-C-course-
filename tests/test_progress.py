from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from learn_engine.errors import ProgressError
from learn_engine.progress import ProgressStore


class ProgressStoreTests(unittest.TestCase):
    def test_empty_store_and_versioned_completion_round_trip(self) -> None:
        # Defect guarded: first run crashes or loses mission version/attempt evidence.
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state" / "progress.json"
            store = ProgressStore(path)
            self.assertEqual(store.load().completed, {})

            store.complete("first-program", "1.2.0", "first-program--001")
            entry = store.load().completed["first-program"]

            self.assertEqual(entry.version, "1.2.0")
            self.assertEqual(entry.attempt_id, "first-program--001")
            self.assertTrue(entry.completed_at.endswith("Z"))

    def test_corrupt_progress_is_reported_not_discarded(self) -> None:
        # Defect guarded: corrupt progress silently resets a learner's history.
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "progress.json"
            path.write_text("not json", encoding="utf-8")
            with self.assertRaisesRegex(ProgressError, "cannot read progress"):
                ProgressStore(path).load()
            self.assertEqual(path.read_text(encoding="utf-8"), "not json")

    def test_complete_replaces_file_atomically_without_temp_residue(self) -> None:
        # Defect guarded: interrupted writes expose partial JSON or stale temp files.
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "progress.json"
            store = ProgressStore(path)
            store.complete("one", "1.0.0", "one--001")
            json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(list(Path(tmp).glob("*.tmp")), [])

    def test_replay_completion_preserves_original_completion_evidence(self) -> None:
        # Defect guarded: submitting a replay erases the attempt and timestamp that first unlocked the mission.
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "progress.json"
            store = ProgressStore(path)
            store.complete("mission", "1.0.0", "mission--001")
            original = store.load().completed["mission"]

            store.complete("mission", "1.1.0", "mission--002")
            replayed = store.load().completed["mission"]

            self.assertEqual(replayed, original)

    def test_level_clearance_is_persisted_with_final_battle_evidence(self) -> None:
        # Defect guarded: the UI merely derives a cleared level transiently and
        # loses the explicit level result or records it before the battle.
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "progress.json"
            store = ProgressStore(path)
            store.complete("ordinary", "2.0.0", "ordinary--001")
            self.assertEqual(store.load().cleared_levels, {})

            store.clear_level("level-one", "battle", "battle--001")
            clearance = store.load().cleared_levels["level-one"]

            self.assertEqual(clearance.final_battle_id, "battle")
            self.assertEqual(clearance.attempt_id, "battle--001")
            self.assertTrue(clearance.completed_at.endswith("Z"))
            document = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(document["schema_version"], 2)
            self.assertIn("level-one", document["cleared_levels"])


if __name__ == "__main__":
    unittest.main()
