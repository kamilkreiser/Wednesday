#!/usr/bin/env python3
"""drafter_tamper_tg2.py — the gate's own tamper aimed at a REFUSAL CLASS, measured once for feasibility: the raced branch
resolves WITHOUT classifying (a plausible slip when wrapping the lookup in a race). Seat file, the drafter probe, and the WHOLE
shared suite under it; restore by git checkout + sha256; green again after."""
import hashlib, json, os, shutil, subprocess, datetime
SCR = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/9aed5a67-2729-4892-b685-13ab87142a58/scratchpad'
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-16_gate1004'
P = json.load(open(SCR + '/gate1004_draft_paths.json')); C = P['C']; W = P['W']
H = '6d077d3fe35cd5f3c09d394553d320e97b1abe32'; SH = C + '/Blockchain/Dev/packages/shared'
REL = 'Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts'; GUARD = C + '/' + REL
now = lambda: datetime.datetime.now().astimezone().strftime('%H:%M:%S')
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
def vt(label, files, env=None):
    out = W + '/vt_' + label + '.json'; e = dict(os.environ); e.update(env or {})
    p = subprocess.run(['npx', 'vitest', 'run', *files, '--reporter=json', '--outputFile=' + out], cwd=SH, env=e, capture_output=True, text=True, timeout=600)
    j = json.load(open(out)); shutil.copyfile(out, G + '/vt_' + label + '.json')
    fails = [(tr['name'].split('/')[-1], a['title'][:70]) for tr in j['testResults'] for a in tr['assertionResults'] if a['status'] == 'failed']
    print(now(), label, 'rc', p.returncode, 'files', len(j['testResults']), 'tests', j['numTotalTests'], 'passed', j['numPassedTests'], 'failed', j['numFailedTests'], 'reds:', fails[:30])
assert sha(GUARD).startswith('b546fc02578c8b1f')
probe = SH + '/src/__tests__/qa1004-drafter-probe-tg2.test.ts'; shutil.copyfile(G + '/qa1004-drafter-probe.test.ts', probe)
s = open(GUARD).read(); A = '    resolvePublicAddresses(url.hostname),\n'
print('anchor count', s.count(A)); assert s.count(A) == 1
M = '    lookup(url.hostname, { all: true, verbatim: true }).then((a) => ({ ok: true as const, addresses: a.map((x) => x.address) })),\n'
open(GUARD, 'w').write(s.replace(A, M)); t = open(GUARD).read(); print('marker count', t.count(M), 'anchor after', t.count(A)); assert t.count(M) == 1
vt('tg2_seat', ['src/__tests__/ks932-timeout-bounds-dns.test.ts'])
vt('tg2_probe', ['src/__tests__/qa1004-drafter-probe-tg2.test.ts'], {'QA1004_OUT': G + '/probe_tg2_rows.json'})
os.rename(probe, probe + '.quarantined')
vt('tg2_shared_full', [])
subprocess.run(['git', '-C', C, 'checkout', H, '--', REL]); print('restored', sha(GUARD).startswith('b546fc02578c8b1f'))
vt('tg2_after_seat', ['src/__tests__/ks932-timeout-bounds-dns.test.ts'])
