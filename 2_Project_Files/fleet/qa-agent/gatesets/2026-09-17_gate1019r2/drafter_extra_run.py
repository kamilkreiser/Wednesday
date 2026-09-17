#!/usr/bin/env python3
"""drafter_extra_run.py TREE... — copy qa1019r2-drafter-extra.test.ts (derived from round 1's GATE harness: SHAPES replaced by 23 extra dot/param/reference spellings;
a 'mount' stage appended) into each tree as src/__tests__/qa1019r2-drafter-extra.test.ts, run SOLO (QA_STAGES verdict,test,prod,mount + originate), rows ->
rows/rows_extra_<tree>.json and rows/rows_extra_origin_<tree>.json, quarantine by rename. Same vitest path as drafter_run.py."""
import os, sys, json, shutil, hashlib, subprocess, datetime
GSD = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, GSD)
import drafter_run as R
h = 'qa1019r2-drafter-extra.test.ts'
for tree in sys.argv[1:]:
    dst = R.T[tree] + '/' + R.GW + '/src/__tests__/' + h
    shutil.copyfile(GSD + '/' + h, dst); R.P('copied', h, 'sha', hashlib.sha256(open(dst, 'rb').read()).hexdigest()[:12], 'into', tree)
    try:
        R.vitest(tree, ['src/__tests__/' + h], 'extra_' + tree, {'QA_OUT': GSD + '/rows/rows_extra_%s.json' % tree, 'QA_STAGES': 'verdict,test,prod,mount'})
        R.vitest(tree, ['src/__tests__/' + h], 'extra_origin_' + tree, {'QA_OUT': GSD + '/rows/rows_extra_origin_%s.json' % tree, 'QA_STAGES': 'originate'})
    finally:
        R.quarantine(dst)
    r = subprocess.run(['git', '-C', R.T[tree], 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True); R.P('tracked porcelain', tree, len(r.stdout.splitlines()))
