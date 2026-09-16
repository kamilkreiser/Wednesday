#!/usr/bin/env python3
"""drafter_ready_compare.py — #1015: (1) READY fenced diff vs the pushed blobs (product +/- lines; the test section's 139 + lines as an ordered
subsequence of commit-1 6e30fe9f5 and of head 77145ce84, every other line listed); (2) the casts-only claim for commit 2, by transpiling both
blobs with the TypeScript API (types erased, comments removed) and diffing the emitted JS. Read verbs only on the checkout (git show)."""
import subprocess, re, sys, json, difflib, os, datetime
sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1015')
from drafterlib import *
R = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
READY = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1018_ornith35b-q8_PASS-7of7-REANCHORED-TDZINLINED_2026-09-15.diff.md'
B, C1, H = '523f283c6cd2550263ec9869dc5ee722be40df4e', '6e30fe9f5ea3abd8414bfe69db2356d31c2da4d6', '77145ce84353534ba381688d5bbd16ff9ff27aef'
AU = 'Blockchain/Dev/services/auth/src/'
TF = AU + '__tests__/ks1018-security-correctness-three-verification-store-reads.test.ts'
UF = AU + 'routes/users.ts'
def show(sha, path): return subprocess.run(['git', '-C', R, 'show', sha + ':' + path], capture_output=True, text=True, check=True).stdout
P('ready_compare', ts())
md = open(READY).read()
body = md.split('```diff\n', 1)[1].rsplit('```', 1)[0]
secs = re.split(r'(?m)^(?=--- )', body)
secs = [s for s in secs if s.startswith('--- ')]
P('READY sections', len(secs), [s.split('\n')[1] for s in secs])
prod, test = secs[0], secs[1]
hunks = re.findall(r'(?m)^@@ .*@@', test); P('test section hunk headers', hunks)
tplus = [l[1:] for l in test.split('\n') if l.startswith('+') and not l.startswith('+++')]
P('test section + lines', len(tplus))
for label, sha in (('commit1', C1), ('head', H)):
    f = show(sha, TF).split('\n')
    if f and f[-1] == '': f = f[:-1]
    sm = difflib.SequenceMatcher(None, tplus, f, autojunk=False)
    matched = sum(b.size for b in sm.get_matching_blocks())
    P('  %s blob lines %d | READY + lines matched in order %d of %d' % (label, len(f), matched, len(tplus)))
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal': continue
        P('   ', op, 'READY[%d:%d]' % (i1, i2), '->', '%s[%d:%d]' % (label, j1, j2))
        for x in tplus[i1:i2]: P('      - READY  |', x[:150])
        for x in f[j1:j2]: P('      + %-6s |' % label, x[:150])
pplus = [l[1:] for l in prod.split('\n') if l.startswith('+') and not l.startswith('+++')]
pminus = [l[1:] for l in prod.split('\n') if l.startswith('-') and not l.startswith('---')]
d = subprocess.run(['git', '-C', R, 'diff', '-U0', B, H, '--', UF], capture_output=True, text=True, check=True).stdout
dplus = [l[1:] for l in d.split('\n') if l.startswith('+') and not l.startswith('+++')]
dminus = [l[1:] for l in d.split('\n') if l.startswith('-') and not l.startswith('---')]
P('product READY +%d -%d | pushed diff base..head +%d -%d | + equal in order: %s | - equal in order: %s' % (len(pplus), len(pminus), len(dplus), len(dminus), pplus == dplus, pminus == dminus))
P('users.ts blob c1 == head:', show(C1, UF) == show(H, UF))
# casts-only: transpile both test blobs, types erased, comments removed
node = T['head'] + '/Blockchain/Dev/node_modules/typescript'
js = r'''
const ts = require(process.argv[1]); const fs = require('fs');
for (const f of [process.argv[2], process.argv[3]]) {
  const out = ts.transpileModule(fs.readFileSync(f, 'utf8'), { compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.ESNext, removeComments: true } }).outputText;
  fs.writeFileSync(f + '.js', out);
}
'''
w = os.path.dirname(T['head']) + '/casts'
os.makedirs(w, exist_ok=True)
open(w + '/c1.ts', 'w').write(show(C1, TF)); open(w + '/head.ts', 'w').write(show(H, TF))
p = subprocess.run(['node', '-e', js, node, w + '/c1.ts', w + '/head.ts'], capture_output=True, text=True); P('transpile rc', p.returncode, p.stderr[-300:])
a, b = open(w + '/c1.ts.js').read().split('\n'), open(w + '/head.ts.js').read().split('\n')
dl = [l for l in difflib.unified_diff(a, b, 'c1.js', 'head.js', n=0, lineterm='')]
P('emitted-JS diff lines (types erased, comments removed):', len(dl))
for l in dl: P('   ', l[:200])
# control: a runtime edit must show up in the same instrument
open(w + '/head_ctl.ts', 'w').write(show(H, TF).replace("expect(lines).toHaveLength(1);", "expect(lines).toHaveLength(2);", 1))
p = subprocess.run(['node', '-e', js, node, w + '/c1.ts', w + '/head_ctl.ts'], capture_output=True, text=True)
c = open(w + '/head_ctl.ts.js').read().split('\n')
P('CONTROL (a planted runtime edit toHaveLength(1)->(2)) emitted-JS diff lines:', len([l for l in difflib.unified_diff(b, c, n=0, lineterm='')]))
P('end', ts())
