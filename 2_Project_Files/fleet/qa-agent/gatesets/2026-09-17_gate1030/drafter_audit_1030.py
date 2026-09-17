#!/usr/bin/env python3
"""drafter_audit_1030.py — #1030: the SHIPPED audit-gate.mjs + audit-locks.mjs from Blockchain/Dev in the drafter's own worktrees.
 H1 head e43af4934, real baseline (31)            expect gate rc 0 / locks rc 0, 0 CLEANUP
 H2 head, merge-base 20ab16f9a's baseline (32)     expect CLEANUP naming exactly GHSA-82fw-gwwq-j7x9
 B1 merge-base 20ab16f9a (= develop's audit inputs), head's baseline (31)  expect rc 1 naming exactly GHSA-82fw
Bulk-advisory responses the shipped audit-locks receives are TEED in-process (preload, no extra URL): vitest + @vitest/mocker requested versions,
vulnerable_versions, severities. Shipped semver evaluates every census version from the lock parse. scripts/audit `npm ci --ignore-scripts`."""
import datetime, hashlib, json, os, re, subprocess
import json as _j
SCR = _j.load(open('/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1030/drafter_paths.json'))['SCR']
GS = os.path.dirname(os.path.abspath(__file__)); OUT = GS + '/out'; os.makedirs(OUT, exist_ok=True)
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
TWO = ['GHSA-82fw-gwwq-j7x9']
TEE = SCR + '/tee_fetch.mjs'
open(TEE, 'w').write(r'''import { appendFileSync } from 'node:fs';
const real = globalThis.fetch;
globalThis.fetch = async (url, init) => {
  const res = await real(url, init);
  if (String(url).includes('/security/advisories/bulk') && process.env.QA_TEE_OUT) {
    const txt = await res.clone().text(); const req = JSON.parse(init?.body ?? '{}'); const j = JSON.parse(txt) || {};
    const pick = (o) => Object.fromEntries(['vitest', '@vitest/mocker'].map(k => [k, o[k] ?? null]));
    appendFileSync(process.env.QA_TEE_OUT, JSON.stringify({ status: res.status, req: pick(req), res: pick(j), resKeys: Object.keys(j).length, reqKeys: Object.keys(req).length }) + '\n');
  }
  return res;
};
''')
for t in ('head', 'base'):
    d = SCR + '/wt_%s/Blockchain/Dev/scripts/audit' % t
    s0 = hashlib.sha256(open(d + '/package-lock.json', 'rb').read()).hexdigest()[:16]
    p = subprocess.run(['npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund'], cwd=d, capture_output=True, text=True)
    print(t, 'scripts/audit npm ci rc', p.returncode, '| lock sha', s0, '->', hashlib.sha256(open(d + '/package-lock.json', 'rb').read()).hexdigest()[:16],
          '| root node_modules present (must be False)', os.path.exists(SCR + '/wt_%s/Blockchain/Dev/node_modules' % t), now())
copies = {}
for t in ('head', 'base'):
    copies[t] = SCR + '/baseline_%s_copy.json' % t
    open(copies[t], 'wb').write(open(SCR + '/wt_%s/Blockchain/Dev/scripts/audit/audit-baseline.json' % t, 'rb').read())
RUNS = [('H1', 'head', None), ('H2', 'head', copies['base']), ('B1', 'base', copies['head'])]
for tag, t, blpath in RUNS:
    dev = SCR + '/wt_%s/Blockchain/Dev' % t
    for gate in ('audit-gate', 'audit-locks'):
        env = dict(os.environ); env.pop('AUDIT_BASELINE_PATH', None)
        if blpath: env['AUDIT_BASELINE_PATH'] = blpath
        tee = OUT + '/%s_%s.tee.jsonl' % (tag, gate)
        env['QA_TEE_OUT'] = tee; env['NODE_OPTIONS'] = '--import=' + TEE
        t0 = now(); p = subprocess.run(['node', 'scripts/audit/%s.mjs' % gate], cwd=dev, env=env, capture_output=True, text=True, timeout=500)
        text = p.stdout + '\n--stderr--\n' + p.stderr
        open(OUT + '/%s_%s.out' % (tag, gate), 'w').write(text)
        summ = [l.strip()[:130] for l in text.splitlines() if re.search(r'(distinct advisories|standalone lockfiles|advisories match)', l)]
        cleanup = text.split('CLEANUP', 1)[1] if 'CLEANUP' in text else ''
        fail = text.split('FAIL', 1)[1] if 'FAIL' in text else ''
        ids = lambda s: sorted(set(re.findall(r'GHSA-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}', s)))
        fam = [l.strip()[:150] for l in text.splitlines() if 'vitest' in l or 'pinned:' in l][:10]
        print('%s %s %s baseline=%s rc %d %s->%s | %s | CLEANUP ids %s | FAIL-section ids %s | family lines %s' % (tag, t, gate,
              os.path.basename(blpath) if blpath else 'real', p.returncode, t0, now(), summ, ids(cleanup.split('FAIL')[0]), ids(fail), fam))
# the teed advisory data + shipped semver over every census version
sv = SCR + '/wt_head/Blockchain/Dev/scripts/audit/node_modules/semver/index.js'
node = r'''
import { readFileSync, readdirSync } from 'node:fs';
const semver = (await import(process.env.SEMVER)).default;
const seen = {};
for (const f of readdirSync(process.env.OUT).filter(f => f.endsWith('.tee.jsonl'))) {
  for (const line of readFileSync(process.env.OUT + '/' + f, 'utf8').split('\n').filter(Boolean)) {
    const r = JSON.parse(line);
    for (const pkg of ['vitest', '@vitest/mocker']) {
      if (r.req[pkg]) console.log(`${f} request ${pkg} ${JSON.stringify(r.req[pkg])} status ${r.status}`);
      for (const a of r.res[pkg] ?? []) seen[pkg + ' ' + String(a.url).split('/').pop()] = [a.severity, a.vulnerable_versions];
    }
  }
}
const versions = { 'vitest': ['4.1.9', '4.1.10', '4.1.11', '4.1.12', '4.2.0', '3.2.4', '4.0.0-beta.1'], '@vitest/mocker': ['4.1.9', '4.1.10', '4.1.11', '4.2.0', '3.2.4'] };
for (const [k, [sev, rng]] of Object.entries(seen)) {
  const pkg = k.split(' ')[0];
  console.log(`ADVISORY ${k} ${sev} vulnerable_versions=${JSON.stringify(rng)} :: ` + versions[pkg].map(v => `${v}:${semver.satisfies(v, rng)}`).join(' '));
}
console.log(`lexical trap '4.1.10' < '4.1.9' = ${'4.1.10' < '4.1.9'} ; semver.lt = ${semver.lt('4.1.10', '4.1.9')}`);
for (const [who, rng, v] of [['manifest vitest', '^4.1.11', '4.1.11'], ['manifest vitest old', '^4.1.9', '4.1.11'], ['vitest -> @vitest/mocker', '4.1.11', '4.1.11']])
  console.log(`declarer ${who} ${rng}: ${v} inside=${semver.satisfies(v, rng)} | control 4.1.10 inside=${semver.satisfies('4.1.10', rng)} 5.0.0 inside=${semver.satisfies('5.0.0', rng)}`);
'''
open(SCR + '/semver_probe.mjs', 'w').write(node)
p = subprocess.run(['node', SCR + '/semver_probe.mjs'], cwd=SCR, env=dict(os.environ, SEMVER='file://' + sv, OUT=OUT), capture_output=True, text=True, timeout=120)
print(p.stdout, p.stderr[-800:])
print('done', now())
