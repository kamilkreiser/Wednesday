#!/usr/bin/env python3
"""drafter_static.py — INCLUDING tsc (api-gateway's tsconfig excludes src/__tests__) at base and head, inclusion proven by --listFilesOnly,
error lines counted per file, a planted positive control (unused local in the ks1087 test, restored sha-identical); eslint JSON on the two
touched files at head and verification.ts at base. The including tsconfig is placed in the clone for the run and moved out by rename."""
import sys, os, json, re, subprocess
sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1008')
from drafterlib import *
GW = 'Blockchain/Dev/services/api-gateway'
TEST = 'src/__tests__/ks1087-workflow-approve-deletes-the-pending-document.test.ts'
CFG = {"extends": "./tsconfig.json", "compilerOptions": {"noEmit": True}, "include": ["src/**/*.ts"], "exclude": ["node_modules", "dist"]}
P('drafter_static', ts())
alltxt = []
def tsc(tree, tag):
    d = T[tree] + '/' + GW; cfg = d + '/tsconfig.qa-including.json'
    json.dump(CFG, open(cfg, 'w'))
    tscbin = T[tree] + '/Blockchain/Dev/node_modules/.bin/tsc'
    lf = subprocess.run([tscbin, '-p', 'tsconfig.qa-including.json', '--listFilesOnly'], cwd=d, capture_output=True, text=True).stdout
    own = [l for l in lf.splitlines() if (T[tree] + '/' + GW + '/src/') in l]
    tests = [l for l in own if '/__tests__/' in l]
    p = subprocess.run([tscbin, '-p', 'tsconfig.qa-including.json'], cwd=d, capture_output=True, text=True)
    errs = [l for l in p.stdout.splitlines() if re.match(r'^src/.*\(\d+,\d+\): error TS', l)]
    per = {}
    for e in errs: per[e.split('(')[0]] = per.get(e.split('(')[0], 0) + 1
    q = W + '/_quarantine_tsconfig.qa-including_%s_%s.json' % (tree, tag); os.rename(cfg, q)
    P('%s tree %s including tsc rc %d | own src files %d, __tests__ files %d, ks1087 listed %s | error lines %d in %d files | ks1087 %d | verification.ts %d' % (tag, tree, p.returncode, len(own), len(tests), any(TEST.split('/')[-1] in l for l in tests), len(errs), len(per), per.get(TEST, 0), per.get('src/routes/verification.ts', 0)))
    alltxt.append('==== %s %s\n%s' % (tree, tag, p.stdout))
    return set(re.sub(r'\(\d+,\d+\)', '', e) for e in errs), errs
eb, _ = tsc('base', 'T0'); eh, errs_h = tsc('head', 'T0')
P('error-line keys new at head (by file + code + message, line numbers stripped):', len(eh - eb), sorted(eh - eb)[:10], '| gone:', len(eb - eh))
for e in errs_h:
    if 'ks1087' in e or 'verification.ts' in e: P('   head error:', e[:220])
# positive control: plant an unused local in the ks1087 test (noUnusedLocals is on in the base tsconfig)
f = T['head'] + '/' + GW + '/' + TEST; pristine = sha(f)
edit(f, "const DOC_ID = 'doc-ks1087';\n", "const DOC_ID = 'doc-ks1087';\nfunction qaPlant() { const QA_UNUSED_PLANT = 1; }\n", [('QA_UNUSED_PLANT', 1)])
ec, errs_c = tsc('head', 'PLANT')
P('plant control: ks1087 errors', sum(1 for e in errs_c if 'ks1087' in e), [e[:160] for e in errs_c if 'ks1087' in e])
el = subprocess.run([T['head'] + '/Blockchain/Dev/node_modules/.bin/eslint', '-f', 'json', GW.replace('Blockchain/Dev/', '') + '/' + TEST], cwd=T['head'] + '/Blockchain/Dev', capture_output=True, text=True)
try:
    j = json.loads(el.stdout); P('plant control eslint on ks1087: errors', sum(x['errorCount'] for x in j), 'warnings', sum(x['warningCount'] for x in j), sorted(set(m.get('ruleId') for x in j for m in x['messages'])))
except Exception as e: P('plant control eslint unparsable rc', el.returncode, el.stderr[-300:])
restore('head', GW + '/' + TEST, pristine)
GWR = GW.replace('Blockchain/Dev/', '')  # eslint runs with cwd Blockchain/Dev: paths relative to it (first run passed Dev-prefixed paths: 'No files matching')
for tree, files in (('head', [GWR + '/' + TEST, GWR + '/src/routes/verification.ts']), ('base', [GWR + '/src/routes/verification.ts'])):
    el = subprocess.run([T[tree] + '/Blockchain/Dev/node_modules/.bin/eslint', '-f', 'json', *files], cwd=T[tree] + '/Blockchain/Dev', capture_output=True, text=True)
    try:
        j = json.loads(el.stdout)
        for x in j: P('eslint', tree, x['filePath'].split('/src/')[-1], 'errors', x['errorCount'], 'warnings', x['warningCount'], sorted((m.get('ruleId'), m['line']) for m in x['messages']))
    except Exception as e: P('eslint', tree, 'unparsable rc', el.returncode, el.stdout[:300], el.stderr[-500:])
open(GS + '/tsc_including.out', 'w').write('\n'.join(alltxt))
P('porcelain head', len(porcelain('head')), 'base', len(porcelain('base')))
P('end', ts())
