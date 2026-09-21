from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


class MaintenanceScriptTests(unittest.TestCase):
    def test_python_cache_cleanup_removes_only_generated_python_cache(self) -> None:
        """Defect guarded: the integrated gate leaves Python bytecode debris behind."""
        with tempfile.TemporaryDirectory() as temporary:
            fixture = Path(temporary) / "course"
            cache = fixture / "learn_engine" / "__pycache__"
            preserved = fixture / "curriculum" / "cache-notes"
            cache.mkdir(parents=True)
            preserved.mkdir(parents=True)
            (cache / "module.cpython-312.pyc").write_bytes(b"generated")
            (fixture / "learn_engine" / "loose.pyc").write_bytes(b"generated")
            (preserved / "notes.txt").write_text("keep me\n", encoding="utf-8")

            source = ROOT / "scripts" / "clean_python_cache.sh"
            result = subprocess.run(
                ["bash", str(source), str(fixture)], text=True, capture_output=True, check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(cache.exists())
            self.assertFalse((fixture / "learn_engine" / "loose.pyc").exists())
            self.assertEqual((preserved / "notes.txt").read_text(encoding="utf-8"), "keep me\n")

if __name__ == "__main__":
    unittest.main()
