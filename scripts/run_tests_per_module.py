#!/usr/bin/env python3
import subprocess, os
from pathlib import Path
root = Path('apps')
results = []
for p in sorted(root.iterdir()):
    if not p.is_dir() or p.name == 'nexora-home':
        continue
    test_file = p / f'test_{p.name}.py'
    if not test_file.exists():
        # fallback to any test_*.py
        tests = list(p.glob('test_*.py'))
        if not tests:
            continue
        test_file = tests[0]
    env = os.environ.copy()
    env['PYTHONPATH'] = str(p) + (':' + env.get('PYTHONPATH','') if env.get('PYTHONPATH') else '')
    print(f"Running {test_file} with PYTHONPATH={env['PYTHONPATH']}")
    proc = subprocess.run(['pytest', str(test_file), '-q'], env=env, capture_output=True, text=True)
    ok = proc.returncode == 0
    print(proc.stdout)
    if proc.stderr:
        print(proc.stderr)
    results.append((p.name, ok, proc.returncode))

print('\nSummary:')
for name, ok, code in results:
    print(f"{name}: {'OK' if ok else 'FAIL'} (code {code})")
