from __future__ import annotations

import tempfile
import json
import unittest
from pathlib import Path
from unittest import mock

from learn_engine.attempts import AttemptStore
from learn_engine.catalog import Catalog
from learn_engine.errors import AttemptError
from tests.helpers import write_mission


class AttemptStoreTests(unittest.TestCase):
    def mission(self, root: Path):
        curriculum = root / "curriculum"
        package = write_mission(curriculum, "first", 10)
        (package / "starter" / "main.c").write_text("original\n", encoding="utf-8")
        return Catalog.load(curriculum).by_id("first"), package

    def test_start_copies_source_and_resume_preserves_work(self) -> None:
        # Defect guarded: editing an attempt mutates curriculum or resume resets work.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mission, package = self.mission(root)
            store = AttemptStore(root / ".learn" / "attempts")

            first = store.start(mission)
            (first.path / "main.c").write_text("learner edit\n", encoding="utf-8")
            resumed = store.start(mission)

            self.assertEqual(first.id, resumed.id)
            self.assertEqual((resumed.path / "main.c").read_text(), "learner edit\n")
            self.assertEqual((package / "starter" / "main.c").read_text(), "original\n")
            self.assertEqual(
                (first.path / "BRIEFING.md").read_text(encoding="utf-8"),
                (package / "briefing.md").read_text(encoding="utf-8"),
            )

    def test_replay_creates_fresh_numbered_attempt(self) -> None:
        # Defect guarded: replay overwrites the completed working directory.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mission, _ = self.mission(root)
            store = AttemptStore(root / ".learn" / "attempts")
            first = store.start(mission)
            (first.path / "main.c").write_text("changed\n", encoding="utf-8")

            replay = store.replay(mission)

            self.assertEqual((first.id, replay.id), ("first--001", "first--002"))
            self.assertEqual((replay.path / "main.c").read_text(), "original\n")

    def test_replay_uses_next_highest_number_after_middle_reset(self) -> None:
        # Defect guarded: deleting attempt 002 makes len-based numbering collide with existing 003.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mission, _ = self.mission(root)
            store = AttemptStore(root / ".learn" / "attempts")
            store.start(mission)
            second = store.replay(mission)
            store.replay(mission)
            store.reset(second.id, confirmed=True)

            fourth = store.replay(mission)

            self.assertEqual(fourth.id, "first--004")

    def test_resume_uses_numeric_order_after_attempt_999(self) -> None:
        # Defect guarded: lexicographic ordering resumes 999 instead of attempt 1000.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mission, _ = self.mission(root)
            attempts_root = root / ".learn" / "attempts"
            for number in (998, 999, 1000):
                attempt_id = f"first--{number:03d}"
                path = attempts_root / attempt_id
                path.mkdir(parents=True)
                metadata = root / ".learn" / "attempt-metadata" / f"{attempt_id}.json"
                metadata.parent.mkdir(parents=True, exist_ok=True)
                metadata.write_text(json.dumps({
                    "id": attempt_id,
                    "mission_id": "first",
                    "mission_version": "1.0.0",
                    "hints_seen": 0,
                }), encoding="utf-8")

            resumed = AttemptStore(attempts_root).start(mission)

            self.assertEqual(resumed.id, "first--1000")

    def test_reset_requires_confirmation_and_rejects_traversal(self) -> None:
        # Defect guarded: reset deletes an attempt or outside path without explicit scope.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mission, _ = self.mission(root)
            store = AttemptStore(root / ".learn" / "attempts")
            attempt = store.start(mission)
            with self.assertRaisesRegex(AttemptError, "confirmation"):
                store.reset(attempt.id, confirmed=False)
            with self.assertRaisesRegex(AttemptError, "invalid attempt id"):
                store.reset("../outside", confirmed=True)
            self.assertTrue(attempt.path.exists())
            store.reset(attempt.id, confirmed=True)
            self.assertFalse(attempt.path.exists())

    def test_failed_metadata_write_leaves_no_orphan_and_can_retry(self) -> None:
        # Defect guarded: interruption after copying starter files leaves an unusable numbered attempt.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mission, _ = self.mission(root)
            store = AttemptStore(root / ".learn" / "attempts")

            with mock.patch.object(
                Path, "write_text",
                side_effect=AttemptError("simulated interrupted metadata write"),
            ):
                with self.assertRaisesRegex(AttemptError, "metadata write"):
                    store.start(mission)

            attempts = root / ".learn" / "attempts"
            metadata = root / ".learn" / "attempt-metadata"
            self.assertEqual(list(attempts.iterdir()) if attempts.exists() else [], [])
            self.assertEqual(list(metadata.iterdir()) if metadata.exists() else [], [])

            recovered = store.start(mission)
            self.assertEqual(recovered.id, "first--001")
            self.assertEqual((recovered.path / "main.c").read_text(), "original\n")

    def test_attempt_numbers_survive_reset_and_ignore_malformed_directories(self) -> None:
        # Defect guarded: deleting a workspace reuses its evidence ID, or a junk suffix crashes discovery.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mission, _ = self.mission(root)
            store = AttemptStore(root / ".learn" / "attempts")
            first = store.start(mission)
            (store.root / "first--12junk").mkdir()
            (store.root / "first--not-a-number").mkdir()

            store.reset(first.id, confirmed=True)
            second = store.replay(mission)

            self.assertEqual(second.id, "first--002")
            self.assertTrue((root / ".learn" / "attempt-sequences.json").is_file())

    def test_completion_evidence_attempt_cannot_be_reset(self) -> None:
        # Defect guarded: reset deletes the workspace named by immutable completion evidence.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mission, _ = self.mission(root)
            initial = AttemptStore(root / ".learn" / "attempts").start(mission)
            protected = AttemptStore(
                root / ".learn" / "attempts", protected_attempt_ids={initial.id}
            )

            with self.assertRaisesRegex(AttemptError, "completion evidence"):
                protected.reset(initial.id, confirmed=True)

            self.assertTrue(initial.path.is_dir())

    def test_resume_rejects_an_attempt_from_an_older_mission_version(self) -> None:
        # Defect guarded: changed mission checks are applied to a stale workspace without warning.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mission, _ = self.mission(root)
            store = AttemptStore(root / ".learn" / "attempts")
            store.start(mission)
            changed = mission.__class__(
                mission.id, mission.title, "2.0.0", mission.order, mission.stage,
                mission.activity, mission.duration_minutes, mission.platform,
                mission.prerequisites, mission.objectives, mission.starter,
                mission.hints, mission.content, mission.checks, mission.root,
            )

            with self.assertRaisesRegex(AttemptError, "fresh attempt"):
                store.start(changed)

            fresh = store.start(changed, force_new=True)
            self.assertEqual((fresh.id, fresh.mission_version), ("first--002", "2.0.0"))


if __name__ == "__main__":
    unittest.main()
