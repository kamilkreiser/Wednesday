#!/usr/bin/env python3
"""Drafter read: compare each READY diff's `+` lines against the head bytes of the file the seat says it came from.
Reads local files only (READY diffs + the head files saved by gh_read.py). Usage: ready_vs_head.py <gateset dir>"""
import sys, re, difflib, hashlib, datetime
G = sys.argv[1]
N = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/'
PAIRS = [
    ('F3', N + 'READY_KS-1123-F3_ornith35b-q8_TESTONLY-PASS-7of7_2026-09-15.diff.md',
     G + '/gh/pr1002_head_Blockchain__Dev__services__api-gateway__src____tests____ks1123-f3-empty-status-is-off-chain.test.ts'),
    ('F2', N + 'READY_KS-1123-F2_ornith35b-q8_TESTONLY-PASS-7of7_2026-09-15.diff.md',
     G + '/gh/pr1002_head_Blockchain__Dev__services__api-gateway__src____tests____ks1123-f2-anchor-failed-stale-confidence.test.ts'),
]
print('read at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
for tag, ready, headp in PAIRS:
    txt = open(ready, encoding='utf-8').read()
    blocks = re.findall(r'```diff\n(.*?)\n```', txt, re.S)
    print(f'\n{tag}: READY {ready.split("/")[-1]} diff blocks={len(blocks)}')
    lines = []
    for b in blocks:
        hunk = re.search(r'^@@ -0,0 \+1,(\d+) @@', b, re.M)
        print('  hunk header +count:', hunk.group(1) if hunk else None)
        for ln in b.split('\n'):
            if ln.startswith('+++') or not ln.startswith('+'):
                continue
            lines.append(ln[1:])
    head = open(headp, encoding='utf-8').read()
    hl = head.split('\n')
    if hl and hl[-1] == '':
        hl = hl[:-1]
    print(f'  READY + lines={len(lines)} head lines={len(hl)} identical={lines == hl}')
    print('  sha256 READY-joined', hashlib.sha256(('\n'.join(lines) + '\n').encode()).hexdigest()[:16], 'head', hashlib.sha256(head.encode()).hexdigest()[:16])
    d = list(difflib.unified_diff(lines, hl, 'READY', 'head', lineterm='', n=0))
    print(f'  unified diff lines={len(d)}')
    for x in d[:80]:
        print('   ', x)
