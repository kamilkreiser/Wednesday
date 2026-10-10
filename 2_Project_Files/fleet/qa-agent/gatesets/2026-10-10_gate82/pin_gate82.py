#!/usr/bin/env python3
"""pin_gate82.py — (re)writes kit.json `script_sha256` for the 9 files the launcher pins. Run after ANY edit to a pinned file:
    PYTHONDONTWRITEBYTECODE=1 python3 <kit>/pin_gate82.py
It touches ONLY kit.json (no other file). The launcher refuses rc 31 on a mismatch and rc 30 on a missing, empty or unpinned file.
KIT_REPORT.md, RULINGS_wednesday.md and kit.json itself are NOT pinned (Wednesday edits them)."""
import hashlib, json, os, sys
D = os.path.dirname(os.path.abspath(__file__)); FILES = 'lib_gate82.py c1_pin_gate82.py c2_code_gate82.py c3_cells_gate82.py gh_gate82.py probe_rotate_gate82.ts.txt prompt_gate82.txt launch_qa_secuura_gate82.sh repin_and_launch_gate82.sh'.split()
k = json.load(open(os.path.join(D, 'kit.json'))); k['script_sha256'] = {f: hashlib.sha256(open(os.path.join(D, f), 'rb').read()).hexdigest() for f in FILES}
json.dump(k, open(os.path.join(D, 'kit.json'), 'w'), indent=1, ensure_ascii=False)
for f in FILES: print('%s  %s' % (k['script_sha256'][f][:12], f))
