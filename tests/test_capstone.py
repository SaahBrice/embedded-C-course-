from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CAPSTONE = ROOT / "capstone" / "reference"


class CapstoneTests(unittest.TestCase):
    def run_checked(self, argv: list[str], cwd: Path) -> str:
        result = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout

    def test_make_capstone_tests_and_demo(self) -> None:
        # Defect guarded: logger modules compile separately but failure policies break in integration.
        output = self.run_checked(["make", "clean", "all", "test"], CAPSTONE)
        self.assertIn("data_logger: 7 suites passed", output)
        demo = self.run_checked([str(CAPSTONE / "logger_demo")], CAPSTONE)
        self.assertIn("stored=3 transported=3 pending=0", demo)

    def test_cmake_and_ctest(self) -> None:
        # Defect guarded: the documented second build system or exported module graph drifts.
        with tempfile.TemporaryDirectory() as tmp:
            build = Path(tmp) / "build"
            self.run_checked(["cmake", "-S", str(CAPSTONE), "-B", str(build)], ROOT)
            self.run_checked(["cmake", "--build", str(build)], ROOT)
            output = self.run_checked(["ctest", "--test-dir", str(build), "--output-on-failure"], ROOT)
            self.assertIn("100% tests passed", output)


if __name__ == "__main__":
    unittest.main()
