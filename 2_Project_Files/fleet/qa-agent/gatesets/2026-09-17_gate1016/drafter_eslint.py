#!/usr/bin/env python3
"""drafter_eslint.py — #1016 eslint (flat config Blockchain/Dev/eslint.config.mjs, run from Blockchain/Dev) on verification.ts base/head, the ks1072 test at head,
and the READY's verbatim 150-line test (placed at head, quarantined by rename); positive control = a planted unused const in a copy of the ks1072 test. Never rm."""
import subprocess, json, os, datetime, hashlib, collections
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1016'
PATHS = json.load(open(GS + '/drafter_paths.json')); W = PATHS['W']; T = PATHS['trees']
def ts(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
V = 'services/api-gateway/src/routes/verification.ts'; K = 'services/api-gateway/src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts'
def lint(tree, rels, label):
    d = T[tree] + '/Blockchain/Dev'
    p = subprocess.run([d + '/node_modules/.bin/eslint', '-f', 'json', *rels], cwd=d, capture_output=True, text=True)
    try: j = json.loads(p.stdout)
    except Exception: print(ts(), label, 'NO JSON rc', p.returncode, p.stderr[-800:], flush=True); return
    for f in j:
        rules = collections.Counter(m.get('ruleId') for m in f['messages'])
        print(ts(), label, tree, f['filePath'].split('/src/')[-1], 'errors', f['errorCount'], 'warnings', f['warningCount'], dict(rules), '| lines', sorted(m['line'] for m in f['messages']), '| rc', p.returncode, flush=True)
print('drafter_eslint start', ts())
lint('base', [V], 'verification.ts')
lint('head', [V, K], 'pr-files')
QD = W + '/_quarantine_2026-09-17'; os.makedirs(QD, exist_ok=True)
READY = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1072_ornith35b-q4_PASS-7of7_2026-09-15.diff.md'
t = open(READY).read(); body = t.split('```diff\n', 1)[1].rsplit('```', 1)[0]; sec = body.split('--- a/services/api-gateway/src/routes/verification.ts')[0]
lines = sec.splitlines(); i = [k for k, l in enumerate(lines) if l.startswith('@@')][0]; content = '\n'.join(l[1:] for l in lines[i + 1:]) + '\n'
rp = 'services/api-gateway/src/__tests__/qa1016-ready-verbatim.test.ts'; open(T['head'] + '/Blockchain/Dev/' + rp, 'w').write(content)
lint('head', [rp], 'READY-verbatim-150')
os.rename(T['head'] + '/Blockchain/Dev/' + rp, QD + '/eslint.ready.%s.test.ts' % datetime.datetime.now().strftime('%H%M%S'))
pp = 'services/api-gateway/src/__tests__/qa1016-plant.test.ts'; s = open(T['head'] + '/Blockchain/Dev/' + K).read()
anchor = "const DOC_ID = 'doc-ks1072';"; assert s.count(anchor) == 1
open(T['head'] + '/Blockchain/Dev/' + pp, 'w').write(s.replace(anchor, anchor + "\nconst QA_UNUSED_PLANT = 'a'.repeat(64);"))
lint('head', [pp], 'PLANT-control')
os.rename(T['head'] + '/Blockchain/Dev/' + pp, QD + '/eslint.plant.%s.test.ts' % datetime.datetime.now().strftime('%H%M%S'))
print('drafter_eslint end', ts())
