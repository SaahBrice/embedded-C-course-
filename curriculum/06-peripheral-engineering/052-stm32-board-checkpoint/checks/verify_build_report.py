from pathlib import Path
import sys
report = (Path(sys.argv[1]) / 'build-report.txt').read_text()
required = ('NUCLEO-C031C6', 'Build command:', 'ELF:', 'Machine: ARM')
missing = [item for item in required if item not in report]
if missing:
    print('build report missing: ' + ', '.join(missing), file=sys.stderr)
    raise SystemExit(1)
print('structured ARM build report recorded')
