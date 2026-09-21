from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


class HostSimulationTests(unittest.TestCase):
    def test_host_peripheral_library_builds_and_passes_c_harness(self) -> None:
        # Defect guarded: simulation APIs drift or state/reset/boundary behavior is wrong.
        completed = subprocess.run(
            ["make", "clean", "all", "test"],
            cwd=ROOT / "platforms" / "host",
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("host simulation: 9 suites passed", completed.stdout)

    def test_host_peripheral_library_cleans_all_outputs(self) -> None:
        # Defect guarded: newly added simulator modules leave untracked binaries or objects after clean.
        completed = subprocess.run(
            ["make", "clean", "test", "clean"],
            cwd=ROOT / "platforms" / "host",
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertFalse((ROOT / "platforms" / "host" / "tests" / "test_sim").exists())
        self.assertFalse((ROOT / "platforms" / "host" / "liblearnsim.a").exists())


if __name__ == "__main__":
    unittest.main()
