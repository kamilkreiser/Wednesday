#!/usr/bin/env python3
"""drafter_audit_1033.py — #1033: the SHIPPED audit-gate.mjs + audit-locks.mjs from Blockchain/Dev in the drafter's own worktrees.
 H1 head 2cab54988, real baseline (29)                         expect gate rc 0 / locks rc 0, 0 CLEANUP
 H2 head, base bb848b828's baseline (31)                        expect CLEANUP naming exactly GHSA-3f6p-5ww8-9rcr + GHSA-rgwj-5xj2-c3m3
 B1 base bb848b828 (= develop's audit inputs), base baseline minus the 2 rows by JSON parse (bytes asserted == head's baseline)
                                                                NEGATIVE CONTROL: expect rc 1 naming exactly the 2
Bulk-advisory responses audit-locks receives are TEED in-process (fetch preload, no extra URL): mysql2 requested versions, vulnerable_versions,
severities. Shipped semver evaluates the boundary versions and every declarer / own-dependency edge of the moved entries (out/edges_*.json)."""
import datetime, hashlib, json, os, re, subprocess
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1033'
OUT = GS + '/out'
P = json.load(open(OUT + '/drafter_paths.json')); SCR = P['SCR']
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def load(): return '%.1f/%.1f/%.1f' % os.getloadavg()
TWO = sorted(['GHSA-3f6p-5ww8-9rcr', 'GHSA-rgwj-5xj2-c3m3'])
TEE = SCR + '/tee_fetch.mjs'
open(TEE, 'w').write(r'''import { appendFileSync } from 'node:fs';
const real = globalThis.fetch;
globalThis.fetch = async (url, init) => {
  const res = await real(url, init);
  if (String(url).includes('/security/advisories/bulk') && process.env.QA_TEE_OUT) {
    const txt = await res.clone().text(); const req = JSON.parse(init?.body ?? '{}'); const j = JSON.parse(txt) || {};
    const pick = (o) => Object.fromEntries(['mysql2', 'express'].map(k => [k, o[k] ?? null]));
    appendFileSync(process.env.QA_TEE_OUT, JSON.stringify({ status: res.status, req: pick(req), res: pick(j), resKeys: Object.keys(j).length, reqKeys: Object.keys(req).length }) + '\n');
  }
  return res;
};
''')
print('drafter_audit_1033 start', now(), 'load', load())
for t in ('head', 'base'):
    d = SCR + '/wt_%s/Blockchain/Dev/scripts/audit' % t
    s0 = hashlib.sha256(open(d + '/package-lock.json', 'rb').read()).hexdigest()[:16]
    p = subprocess.run(['npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund'], cwd=d, capture_output=True, text=True)
    print(t, 'scripts/audit npm ci rc', p.returncode, p.stderr[-300:].strip(), '| lock sha', s0, '->', hashlib.sha256(open(d + '/package-lock.json', 'rb').read()).hexdigest()[:16],
          '| root node_modules present (must be False)', os.path.exists(SCR + '/wt_%s/Blockchain/Dev/node_modules' % t), now(), 'load', load())
base_bl_path = SCR + '/wt_base/Blockchain/Dev/scripts/audit/audit-baseline.json'
head_bl_bytes = open(SCR + '/wt_head/Blockchain/Dev/scripts/audit/audit-baseline.json', 'rb').read()
copies = {'base31': SCR + '/baseline_base31_copy.json', 'minus2': SCR + '/baseline_base_minus2.json'}
open(copies['base31'], 'wb').write(open(base_bl_path, 'rb').read())
j = json.load(open(base_bl_path)); popped = sorted(k for k in TWO if j['accepted'].pop(k, None) is not None)
txt = json.dumps(j, indent=2, ensure_ascii=False) + '\n'; open(copies['minus2'], 'w').write(txt)
print('B1 baseline = base minus', popped, '| rows', len(j['accepted']), '| bytes == head baseline:', txt.encode() == head_bl_bytes)
RUNS = [('H1', 'head', None), ('H2', 'head', copies['base31']), ('B1', 'base', copies['minus2']), ('B0', 'base', None)]
for tag, t, blpath in RUNS:
    dev = SCR + '/wt_%s/Blockchain/Dev' % t
    for gate in ('audit-gate', 'audit-locks'):
        env = dict(os.environ); env.pop('AUDIT_BASELINE_PATH', None)
        if blpath: env['AUDIT_BASELINE_PATH'] = blpath
        tee = OUT + '/%s_%s.tee.jsonl' % (tag, gate)
        env['QA_TEE_OUT'] = tee; env['NODE_OPTIONS'] = '--import=' + TEE
        t0, l0 = now(), load(); p = subprocess.run(['node', 'scripts/audit/%s.mjs' % gate], cwd=dev, env=env, capture_output=True, text=True, timeout=500)
        text = p.stdout + '\n--stderr--\n' + p.stderr
        open(OUT + '/%s_%s.out' % (tag, gate), 'w').write(text)
        summ = [l.strip()[:150] for l in text.splitlines() if re.search(r'(distinct advisories|standalone lockfiles|advisories match)', l)]
        cleanup = text.split('CLEANUP', 1)[1] if 'CLEANUP' in text else ''
        fail = text.split('FAIL', 1)[1] if 'FAIL' in text else ''
        ids = lambda s: sorted(set(re.findall(r'GHSA-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}', s)))
        fam = [l.strip()[:170] for l in text.splitlines() if re.search(r'mysql2|pinned:|in \d+ lock', l)][:10]
        print('%s %s %s baseline=%s rc %d %s->%s load %s | %s | CLEANUP ids %s | FAIL-section ids %s | mysql2 lines %s' % (tag, t, gate,
              os.path.basename(blpath) if blpath else 'real', p.returncode, t0, now(), l0, summ, ids(cleanup.split('FAIL')[0]), ids(fail), fam))
sv = SCR + '/wt_head/Blockchain/Dev/scripts/audit/node_modules/semver/index.js'
node = r'''
import { readFileSync, readdirSync } from 'node:fs';
const semver = (await import(process.env.SEMVER)).default;
console.log('shipped semver', JSON.parse(readFileSync(new URL('./package.json', process.env.SEMVER), 'utf8')).version);
const seen = {};
for (const f of readdirSync(process.env.OUT).filter(f => f.endsWith('.tee.jsonl')).sort()) {
  for (const line of readFileSync(process.env.OUT + '/' + f, 'utf8').split('\n').filter(Boolean)) {
    const r = JSON.parse(line);
    if (r.req.mysql2) console.log(`${f} request mysql2 ${JSON.stringify(r.req.mysql2)} status ${r.status} | control express requested ${!!r.req.express}`);
    for (const a of r.res.mysql2 ?? []) seen[String(a.url).split('/').pop()] = [a.severity, a.vulnerable_versions, a.title];
  }
}
const vs = ['3.15.3', '3.21.9', '3.22.0', '3.23.0', '3.23.1', '3.23.2', '4.0.0'];
for (const [id, [sev, rng, title]] of Object.entries(seen)) {
  console.log(`ADVISORY mysql2 ${id} ${sev} vulnerable_versions=${JSON.stringify(rng)} :: ` + vs.map(v => `${v}:${semver.satisfies(v, rng, { includePrerelease: true })}`).join(' ') + ` :: ${title}`);
}
for (const which of ['root', 'originate']) {
  const edges = JSON.parse(readFileSync(`${process.env.OUT}/edges_${which}.json`, 'utf8'));
  let bad = 0;
  for (const [kind, who, sect, name, rng, ver] of edges) {
    const ok = ver ? semver.satisfies(ver, rng) : (sect !== 'dependencies');
    if (!ok) bad++;
    console.log(`EDGE ${which} ${ok ? 'ok ' : 'BAD'} ${kind} ${who} ${sect} ${name} ${rng} -> ${ver}`);
  }
  console.log(`EDGES ${which}: ${edges.length} checked, ${bad} BAD`);
}
console.log(`CONTROL prisma pin "3.15.3" admits 3.15.3=${semver.satisfies('3.15.3', '3.15.3')} 3.23.1=${semver.satisfies('3.23.1', '3.15.3')}`);
'''
open(SCR + '/semver_probe.mjs', 'w').write(node)
p = subprocess.run(['node', SCR + '/semver_probe.mjs'], cwd=SCR, env=dict(os.environ, SEMVER='file://' + sv, OUT=OUT), capture_output=True, text=True, timeout=120)
print(p.stdout, p.stderr[-800:])
print('done', now(), 'load', load())
