from pathlib import Path
import subprocess
import sys

learner = Path(sys.argv[1])
build = Path(sys.argv[2])

def run(argv):
    completed = subprocess.run(argv, text=True, capture_output=True, check=False)
    if completed.returncode:
        print(completed.stdout, end='')
        print(completed.stderr, end='', file=sys.stderr)
        raise SystemExit(completed.returncode)

make_prefix = build / 'make-prefix'
run(['make', '-C', str(learner), 'clean', 'all', 'install', f'PREFIX={make_prefix}'])
cmake_build = build / 'cmake-build'
cmake_prefix = build / 'cmake-prefix'
run(['cmake', '-S', str(learner), '-B', str(cmake_build), f'-DCMAKE_INSTALL_PREFIX={cmake_prefix}'])
run(['cmake', '--build', str(cmake_build)])
run(['cmake', '--install', str(cmake_build)])
consumer = build / 'consumer.c'
consumer.write_text('#include <rq.h>\n#include <string.h>\nint main(void){return strcmp(rq_version(),"1.0.0");}\n')
exe = build / 'consumer'
run(['cc', '-std=c11', '-Wall', '-Wextra', '-Wpedantic', '-Werror', f'-I{cmake_prefix / "include"}', str(consumer), str(cmake_prefix / 'lib' / 'librq.a'), '-o', str(exe)])
run([str(exe)])
print('Make build/install and CMake relocated consumer passed')
