#!/usr/bin/env python3
"""drafter_apply_check.py - the READY against the BASE worktree of the drafter clone with `git apply --check -v` ONLY (writes nothing).
Run 1 (kept: drafter_apply_check.first-run-unsplit-depends-on-old-contents.out): the whole patch, without and with --recount.
Run 2 (kept: drafter_apply_check.second-run-docstring-edit-syntaxerror.out): this script's own docstring edit broke it (the drafter's slip).
Now: the whole patch, then SPLIT PER FILE as the seat did (`--recount --directory=Blockchain/Dev`), verbose, so the product hunk's offset is printed. Never rm; stderr kept."""
import subprocess, json, datetime
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1016'
PATHS = json.load(open(GS + '/drafter_paths.json')); T = PATHS['trees']; W = PATHS['W']
READY = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1072_ornith35b-q4_PASS-7of7_2026-09-15.diff.md'
t = open(READY).read(); body = t.split('```diff\n', 1)[1].rsplit('```', 1)[0]
print('drafter_apply_check', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), 'patch bytes', len(body))
def check(label, text, extra):
    f = W + '/ready_ks1072.%s.patch' % label; open(f, 'w').write(text)
    p = subprocess.run(['git', '-C', T['base'], 'apply', '--check', '-v', *extra, '--directory=Blockchain/Dev', f], capture_output=True, text=True)
    print('---', label, extra, 'rc', p.returncode); print((p.stdout + p.stderr).strip())
check('whole', body, []); check('whole', body, ['--recount'])
parts = body.split('--- a/services/api-gateway/src/routes/verification.ts'); assert len(parts) == 2
check('split-test-file', parts[0], []); check('split-test-file', parts[0], ['--recount'])
prod = '--- a/services/api-gateway/src/routes/verification.ts' + parts[1]
check('split-product-file', prod, []); check('split-product-file', prod, ['--recount'])
p = subprocess.run(['git', '-C', T['base'], 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True); print('base tracked porcelain after', len(p.stdout.splitlines()))
