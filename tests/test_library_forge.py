from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
LIBRARY = ROOT / "library" / "record_queue"
CONSUMER = ROOT / "examples" / "library-consumer"


class LibraryForgeTests(unittest.TestCase):
    def run_checked(self, argv: list[str], cwd: Path) -> str:
        completed = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, check=False)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        return completed.stdout

    def test_make_library_and_separate_consumer(self) -> None:
        # Defect guarded: the library passes internally but its public header or consumer link is broken.
        output = self.run_checked(["make", "clean", "all", "test"], LIBRARY)
        self.assertIn("record_queue: 5 suites passed", output)
        output = self.run_checked(["make", "clean", "all", "test"], CONSUMER)
        self.assertIn("record_queue 1.0.0: value=42", output)

    def test_cmake_install_and_find_package_consumer(self) -> None:
        # Defect guarded: packaging relies on source-relative includes and fails after installation.
        with tempfile.TemporaryDirectory() as tmp:
            temporary = Path(tmp)
            build = temporary / "library-build"
            prefix = temporary / "install"
            consumer_build = temporary / "consumer-build"
            self.run_checked([
                "cmake", "-S", str(LIBRARY), "-B", str(build),
                f"-DCMAKE_INSTALL_PREFIX={prefix}",
            ], ROOT)
            self.run_checked(["cmake", "--build", str(build)], ROOT)
            self.run_checked(["ctest", "--test-dir", str(build), "--output-on-failure"], ROOT)
            self.run_checked(["cmake", "--install", str(build)], ROOT)
            self.run_checked([
                "cmake", "-S", str(CONSUMER), "-B", str(consumer_build),
                f"-DCMAKE_PREFIX_PATH={prefix}",
            ], ROOT)
            self.run_checked(["cmake", "--build", str(consumer_build)], ROOT)
            output = self.run_checked([str(consumer_build / "record_queue_consumer")], ROOT)
            self.assertEqual(output.strip(), "record_queue 1.0.0: value=42")

    def test_public_queue_type_hides_ring_indices_and_storage(self) -> None:
        # Defect guarded: consumers couple to head/tail/record fields and prevent internal library changes.
        self.run_checked(["make", "clean", "all"], LIBRARY)
        with tempfile.TemporaryDirectory() as tmp:
            probe = Path(tmp) / "probe.c"
            probe.write_text(
                '#include "record_queue.h"\n'
                'size_t inspect(struct record_queue *queue) { return queue->head + queue->tail; }\n',
                encoding="utf-8",
            )
            completed = subprocess.run(
                ["cc", "-std=c11", "-Wall", "-Wextra", "-Werror", "-I", str(LIBRARY / "include"), "-c", str(probe)],
                cwd=Path(tmp), capture_output=True, text=True, check=False,
            )
            self.assertNotEqual(completed.returncode, 0, "private queue fields unexpectedly compiled")


if __name__ == "__main__":
    unittest.main()
