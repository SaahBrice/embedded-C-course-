#!/usr/bin/env bash
set -euo pipefail

project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)
export PYTHONDONTWRITEBYTECODE=1

cleanup() {
    make -C "$project_root/platforms/host" clean >/dev/null
    make -C "$project_root/platforms/stm32c031" clean >/dev/null
    make -C "$project_root/library/record_queue" clean >/dev/null
    make -C "$project_root/examples/library-consumer" clean >/dev/null
    make -C "$project_root/capstone/reference" clean >/dev/null
    "$project_root/scripts/clean_python_cache.sh" "$project_root"
}
trap cleanup EXIT

cleanup
cd "$project_root"
python3 -m unittest discover -s tests -v
./learn validate --all-solutions
make -C platforms/host clean all test
make -C platforms/stm32c031 clean host-test target-contract-test target-build
make -C library/record_queue clean all test
make -C examples/library-consumer clean all test
make -C capstone/reference clean all test
./learn doctor
./learn map >/dev/null

echo "ALL CHECKS PASSED: engine, 11 levels, 96 sublevels, starters, solutions, visible drivers, nine simulator suites, STM32 host/adapter contracts, real Cortex-M0+ ELF, libraries, capstone, and docs."
