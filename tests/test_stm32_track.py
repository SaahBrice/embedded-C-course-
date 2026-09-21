from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from learn_engine.cli import main


ROOT = Path(__file__).resolve().parent.parent
PLATFORM = ROOT / "platforms" / "stm32c031"


class Stm32TrackTests(unittest.TestCase):
    def test_board_project_host_contract_builds(self) -> None:
        # Defect guarded: portable app and STM32 adapter contract drift before hardware is available.
        completed = subprocess.run(
            ["make", "clean", "host-test", "clean"], cwd=PLATFORM,
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("stm32 app host contract: passed", completed.stdout)
        self.assertFalse((PLATFORM / "host" / "test_app").exists())

    def test_target_adapter_initializes_and_propagates_hardware_failures(self) -> None:
        # Defect guarded: GPIO/UART mappings are only text-checked, or HAL UART failures are discarded.
        completed = subprocess.run(
            ["make", "clean", "target-contract-test", "clean"], cwd=PLATFORM,
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("stm32 target adapter contract: passed", completed.stdout)
        self.assertFalse((PLATFORM / "host" / "test_target_adapter").exists())

    def test_target_project_rejects_missing_pinned_cube_dependency(self) -> None:
        # Defect guarded: a target build silently uses missing, unpinned, or downloaded vendor sources.
        completed = subprocess.run(
            [
                "make", "-C", str(PLATFORM / "target_project"), "dependency-check",
                "STM32CUBE_C0=/definitely/missing/STM32CubeC0",
            ],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        self.assertEqual(completed.returncode, 2, completed.stdout + completed.stderr)
        self.assertIn("STM32CubeC0 v1.4.1", completed.stdout + completed.stderr)
        self.assertIn("e044287c0582f76d55455426355f133553368d52", completed.stdout + completed.stderr)
        self.assertIn("does not download", completed.stdout + completed.stderr)

    def test_target_project_builds_and_identifies_a_real_arm_elf(self) -> None:
        # Defect guarded: the full gate claims target support after exercising
        # only a host fake-HAL build.
        completed = subprocess.run(
            ["make", "target-build"], cwd=PLATFORM,
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("Machine:", completed.stdout)
        self.assertIn("ARM", completed.stdout)
        self.assertIn("FLASH:", completed.stdout)
        self.assertTrue(
            (PLATFORM / "target_project" / "build" / "nucleo-c031c6.elf").is_file()
        )

    def test_documented_board_mappings_match_official_manual(self) -> None:
        # Defect guarded: wrong LED/button/VCP pins make a correct first hardware lab appear broken.
        board = (PLATFORM / "common" / "include" / "board_pins.h").read_text(encoding="utf-8")
        self.assertIn("BOARD_LED_GPIO_SUFFIX A", board)
        self.assertIn("BOARD_LED_PIN 5U", board)
        self.assertIn("BOARD_BUTTON_GPIO_SUFFIX C", board)
        self.assertIn("BOARD_BUTTON_PIN 13U", board)
        self.assertIn("BOARD_VCP_TX_GPIO_SUFFIX A", board)
        self.assertIn("BOARD_VCP_TX_PIN 2U", board)
        self.assertIn("BOARD_VCP_RX_GPIO_SUFFIX A", board)
        self.assertIn("BOARD_VCP_RX_PIN 3U", board)

    def test_doctor_is_read_only_and_reports_missing_cross_tools(self) -> None:
        # Defect guarded: environment diagnosis flashes hardware or hides unavailable prerequisites.
        with tempfile.TemporaryDirectory() as tmp:
            empty_path = Path(tmp)
            out_path = empty_path / "doctor.txt"
            env = os.environ.copy()
            env["PATH"] = str(empty_path)
            completed = subprocess.run(
                ["/usr/bin/python3", str(PLATFORM / "doctor.py")],
                env=env, capture_output=True, text=True, check=False,
            )
            out_path.write_text(completed.stdout, encoding="utf-8")
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("arm-none-eabi-gcc: not found", completed.stdout)
            self.assertIn("No build, USB access, or flash operation was performed", completed.stdout)

    def test_flash_script_requires_explicit_confirmation_before_tool_lookup(self) -> None:
        # Defect guarded: a routine test or accidental script call mutates the connected board.
        completed = subprocess.run(
            [str(PLATFORM / "flash.sh"), "firmware.elf"], cwd=PLATFORM,
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(completed.returncode, 2)
        self.assertIn("--yes", completed.stderr)

    def test_openocd_fallback_rejects_unsafe_firmware_path_before_invocation(self) -> None:
        # Defect guarded: a firmware path is interpolated into OpenOCD's Tcl command language.
        with tempfile.TemporaryDirectory() as tmp:
            temporary = Path(tmp)
            firmware = temporary / "firmware;shutdown.elf"
            firmware.write_bytes(b"ELF")
            fake_bin = temporary / "bin"
            fake_bin.mkdir()
            marker = temporary / "openocd-invoked"
            openocd = fake_bin / "openocd"
            openocd.write_text(
                "#!/bin/sh\n: > \"$OPENOCD_MARKER\"\n",
                encoding="utf-8",
            )
            openocd.chmod(0o755)
            env = os.environ.copy()
            env["PATH"] = f"{fake_bin}:/usr/bin:/bin"
            env["OPENOCD_MARKER"] = str(marker)

            completed = subprocess.run(
                [str(PLATFORM / "flash.sh"), "--yes", str(firmware)],
                cwd=PLATFORM, env=env, capture_output=True, text=True, check=False,
            )

            self.assertEqual(completed.returncode, 2, completed.stdout + completed.stderr)
            self.assertIn("cannot be represented safely", completed.stderr)
            self.assertFalse(marker.exists())


if __name__ == "__main__":
    unittest.main()
