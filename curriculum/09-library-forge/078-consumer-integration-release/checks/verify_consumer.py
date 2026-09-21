from pathlib import Path
import subprocess
import sys

learner = Path(sys.argv[1])
build = Path(sys.argv[2])
prefix = build / 'installed'
(prefix / 'include').mkdir(parents=True)
(prefix / 'lib').mkdir(parents=True)
(prefix / 'include' / 'rq.h').write_text(
    '#ifndef RQ_H\n#define RQ_H\nconst char *rq_version(void);\nint rq_add(int left,int right);\n#endif\n'
)
implementation = build / 'rq.c'
implementation.write_text(
    '#include "rq.h"\nconst char *rq_version(void){return "1.0.0";}\nint rq_add(int left,int right){return left+right;}\n'
)
obj = build / 'rq.o'
archive = prefix / 'lib' / 'librq.a'

def run(argv):
    completed = subprocess.run(argv, text=True, capture_output=True, check=False)
    if completed.returncode:
        print(completed.stdout, end='')
        print(completed.stderr, end='', file=sys.stderr)
        raise SystemExit(completed.returncode)

flags = ['-std=c11', '-Wall', '-Wextra', '-Wpedantic', '-Werror']
run(['cc', *flags, '-I', str(prefix / 'include'), '-c', str(implementation), '-o', str(obj)])
run(['ar', 'rcs', str(archive), str(obj)])
executable = build / 'consumer'
run(['cc', *flags, '-I', str(prefix / 'include'), str(learner / 'consumer.c'), str(archive), '-o', str(executable)])
run([str(executable)])
print('Relocated consumer compiled, linked, and ran against installed-only paths')
