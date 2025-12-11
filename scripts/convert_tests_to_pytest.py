#!/usr/bin/env python3
"""Convert apps/*/tests.py files to pytest-discoverable names test_<module>.py

This script copies each tests.py to a new file test_<module>.py next to it.
"""
import pathlib
root = pathlib.Path('apps')
for p in sorted(root.iterdir()):
    if not p.is_dir():
        continue
    src = p / 'tests.py'
    if not src.exists():
        continue
    dst = p / f'test_{p.name.replace("-","_")}.py'
    if dst.exists():
        continue
    text = src.read_text()
    dst.write_text(text)
    print('created', dst)
