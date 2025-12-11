#!/usr/bin/env python3
import pathlib
root = pathlib.Path('apps')
for p in sorted(root.iterdir()):
    if not p.is_dir():
        continue
    test_files = list(p.glob('test_*.py'))
    for tf in test_files:
        text = tf.read_text()
        if "sys.path.insert(0, os.path.dirname(__file__))" in text:
            continue
        header = "import sys, os\nsys.path.insert(0, os.path.dirname(__file__))\n\n"
        tf.write_text(header + text)
        print('patched', tf)
