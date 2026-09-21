#!/usr/bin/env bash
set -euo pipefail

script_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)
target_root=${1:-$script_root}
target_root=$(cd "$target_root" && pwd -P)

if [[ "$target_root" == "/" || ! -d "$target_root/learn_engine" || ! -d "$target_root/curriculum" ]]; then
    echo "Refusing to clean an unrecognized course root: $target_root" >&2
    exit 2
fi

while IFS= read -r -d '' cache_dir; do
    rm -rf -- "$cache_dir"
done < <(find "$target_root" -type d -name __pycache__ -prune -print0)

find "$target_root" -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete
