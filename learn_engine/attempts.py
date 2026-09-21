from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
from pathlib import Path

from .errors import AttemptError
from .models import Attempt, Mission


_ATTEMPT_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*--[0-9]{3,}$")


def _atomic_write_text(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", delete=False,
        ) as stream:
            temporary = Path(stream.name)
        temporary.write_text(payload, encoding="utf-8")
        with temporary.open("rb") as stream:
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except (OSError, AttemptError) as exc:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
        if isinstance(exc, AttemptError):
            raise
        raise AttemptError(f"cannot save {path.name}: {exc}") from exc


class AttemptStore:
    def __init__(self, root: Path, protected_attempt_ids: set[str] | frozenset[str] = frozenset()):
        self.root = root.resolve()
        self.protected_attempt_ids = frozenset(protected_attempt_ids)

    def start(self, mission: Mission, force_new: bool = False) -> Attempt:
        existing = self._for_mission(mission.id)
        if existing and not force_new:
            attempt = self.get(existing[-1].name)
            if attempt.mission_version != mission.version:
                raise AttemptError(
                    f"attempt {attempt.id!r} was created for sublevel version "
                    f"{attempt.mission_version}, but the current version is {mission.version}; "
                    f"start a fresh attempt with './learn start {mission.id} --new'"
                )
        else:
            recorded = self._sequence_for(mission.id)
            discovered = max(
                (int(path.name.rsplit("--", 1)[1]) for path in existing), default=0
            )
            next_number = max(recorded, discovered) + 1
            attempt = self._create(mission, next_number)
            self._record_sequence(mission.id, next_number)
        self._set_active(attempt.id)
        return attempt

    def replay(self, mission: Mission) -> Attempt:
        return self.start(mission, force_new=True)

    def has_attempt_for(self, mission_id: str) -> bool:
        """Return whether this learner has ever opened the named sublevel."""
        return bool(self._for_mission(mission_id))

    def get(self, attempt_id: str) -> Attempt:
        path = self._safe_path(attempt_id)
        metadata_path = self._metadata_path(attempt_id)
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            if metadata.get("id") != attempt_id:
                raise ValueError("attempt ID mismatch")
            mission_id = metadata["mission_id"]
            mission_version = metadata["mission_version"]
            if not isinstance(mission_id, str) or not isinstance(mission_version, str):
                raise ValueError("invalid attempt metadata")
        except (OSError, json.JSONDecodeError, KeyError, ValueError, TypeError) as exc:
            raise AttemptError(f"cannot read attempt {attempt_id!r}: {exc}") from exc
        return Attempt(attempt_id, mission_id, mission_version, path)

    def reset(self, attempt_id: str, confirmed: bool = False) -> None:
        path = self._safe_path(attempt_id)
        if not confirmed:
            raise AttemptError("reset requires explicit confirmation")
        if attempt_id in self.protected_attempt_ids:
            raise AttemptError(
                f"attempt {attempt_id!r} is completion evidence and cannot be reset"
            )
        if not path.is_dir():
            raise AttemptError(f"unknown attempt {attempt_id!r}")
        shutil.rmtree(path)
        self._metadata_path(attempt_id).unlink(missing_ok=True)
        if self.active_id() == attempt_id:
            self._active_path().unlink(missing_ok=True)

    def active_id(self) -> str | None:
        path = self._active_path()
        if not path.exists():
            return None
        try:
            attempt_id = path.read_text(encoding="utf-8").strip()
        except OSError as exc:
            raise AttemptError(f"cannot read active attempt: {exc}") from exc
        self._safe_path(attempt_id)
        return attempt_id

    def active(self) -> Attempt | None:
        attempt_id = self.active_id()
        if attempt_id is None:
            return None
        return self.get(attempt_id)

    def reveal_hint(self, attempt_id: str, total: int) -> int:
        attempt = self.get(attempt_id)
        metadata_path = self._metadata_path(attempt.id)
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        seen = metadata.get("hints_seen", 0)
        if not isinstance(seen, int) or seen < 0:
            raise AttemptError(f"invalid hint state for {attempt_id!r}")
        if seen >= total:
            raise AttemptError("No more hints are available for this sublevel.")
        metadata["hints_seen"] = seen + 1
        _atomic_write_text(metadata_path, json.dumps(metadata, indent=2, sort_keys=True) + "\n")
        return seen

    def _for_mission(self, mission_id: str) -> list[Path]:
        if not self.root.exists():
            return []
        pattern = re.compile(rf"^{re.escape(mission_id)}--([0-9]{{3,}})$")
        matches: list[tuple[int, Path]] = []
        for path in self.root.iterdir():
            match = pattern.fullmatch(path.name)
            if match is not None and path.is_dir():
                matches.append((int(match.group(1)), path))
        return sorted(
            (path for _, path in matches),
            key=lambda path: int(path.name.rsplit("--", 1)[1]),
        )

    def _sequence_path(self) -> Path:
        return self.root.parent / "attempt-sequences.json"

    def _load_sequences(self) -> dict[str, int]:
        path = self._sequence_path()
        if not path.exists():
            return {}
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(raw, dict) or not all(
                isinstance(key, str)
                and isinstance(value, int)
                and not isinstance(value, bool)
                and value >= 0
                for key, value in raw.items()
            ):
                raise ValueError("expected an object of non-negative integer counters")
            return raw
        except (OSError, json.JSONDecodeError, ValueError, TypeError) as exc:
            raise AttemptError(f"cannot read attempt sequence state: {exc}") from exc

    def _sequence_for(self, mission_id: str) -> int:
        return self._load_sequences().get(mission_id, 0)

    def _record_sequence(self, mission_id: str, number: int) -> None:
        sequences = self._load_sequences()
        sequences[mission_id] = max(sequences.get(mission_id, 0), number)
        _atomic_write_text(
            self._sequence_path(), json.dumps(sequences, indent=2, sort_keys=True) + "\n"
        )

    def _safe_path(self, attempt_id: str) -> Path:
        if not _ATTEMPT_ID_RE.fullmatch(attempt_id):
            raise AttemptError(f"invalid attempt id {attempt_id!r}")
        path = (self.root / attempt_id).resolve()
        if path.parent != self.root:
            raise AttemptError(f"invalid attempt id {attempt_id!r}")
        return path

    def _create(self, mission: Mission, number: int) -> Attempt:
        source = (mission.root / mission.starter).resolve()
        if source.parent != mission.root and mission.root not in source.parents:
            raise AttemptError(f"starter for {mission.id!r} escapes its sublevel directory")
        if not source.is_dir():
            raise AttemptError(f"starter directory is missing for sublevel {mission.id!r}")
        for item in source.rglob("*"):
            if item.is_symlink():
                raise AttemptError(f"starter for {mission.id!r} contains a symlink: {item.name}")
        self.root.mkdir(parents=True, exist_ok=True)
        attempt_id = f"{mission.id}--{number:03d}"
        destination = self._safe_path(attempt_id)
        if destination.exists():
            raise AttemptError(f"attempt already exists: {attempt_id}")
        metadata = {
            "id": attempt_id,
            "mission_id": mission.id,
            "mission_version": mission.version,
            "hints_seen": 0,
        }
        metadata_path = self._metadata_path(attempt_id)
        staging = (self.root / f".{attempt_id}.creating").resolve()
        if staging.parent != self.root:
            raise AttemptError(f"invalid attempt staging path for {attempt_id!r}")
        if staging.exists():
            shutil.rmtree(staging)
        metadata_path.unlink(missing_ok=True)
        try:
            shutil.copytree(source, staging)
            shutil.copy2(mission.content_path("briefing"), staging / "BRIEFING.md")
            _atomic_write_text(
                metadata_path, json.dumps(metadata, indent=2, sort_keys=True) + "\n"
            )
            os.replace(staging, destination)
        except (OSError, AttemptError) as exc:
            if staging.exists():
                shutil.rmtree(staging)
            metadata_path.unlink(missing_ok=True)
            if isinstance(exc, AttemptError):
                raise
            raise AttemptError(f"cannot create attempt {attempt_id!r}: {exc}") from exc
        return Attempt(attempt_id, mission.id, mission.version, destination)

    def _active_path(self) -> Path:
        return self.root.parent / "active-attempt"

    def _metadata_path(self, attempt_id: str) -> Path:
        self._safe_path(attempt_id)
        return self.root.parent / "attempt-metadata" / f"{attempt_id}.json"

    def _set_active(self, attempt_id: str) -> None:
        self.root.parent.mkdir(parents=True, exist_ok=True)
        _atomic_write_text(self._active_path(), attempt_id + "\n")
