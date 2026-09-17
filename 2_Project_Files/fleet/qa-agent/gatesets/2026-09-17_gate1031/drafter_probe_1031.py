#!/usr/bin/env python3
"""drafter_probe_1031.py — copy src/qa1031-drafter-probe.test.ts into src/qa_probe/ of the head and dev trees IN THE DRAFTER CLONE (never the checkout) and run it
alone (--testMatch on qa_probe: the default __tests__ testMatch never collects it; originate's tsconfig excludes *.test.ts); rows to out/rows_probe_<tree>.json;
a dev-vs-head table with the verdict columns; a STORED != SERVED census at head. The whole-suite denominator is re-asserted unpolluted after the probe copy."""
import json, subprocess, datetime, os, shutil, hashlib
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1031'
paths = json.load(open(GS + '/out/drafter_paths.json'))
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def now(f='%H:%M:%S %Z'): return datetime.datetime.now().astimezone().strftime(f)
srcf = GS + '/src/qa1031-drafter-probe.test.ts'; P('probe sha256', hashlib.sha256(open(srcf, 'rb').read()).hexdigest()[:16], now('%Y-%m-%d %H:%M:%S %Z'))
res = {}
for name in ('head', 'dev'):
    o = paths['trees'][name] + '/Blockchain/Dev/services/originate'; bin_ = paths['trees'][name] + '/Blockchain/Dev/node_modules/.bin/'
    d = o + '/src/qa_probe'; os.makedirs(d, exist_ok=True); shutil.copyfile(srcf, d + '/qa1031-drafter-probe.test.ts')
    out = GS + '/out/rows_probe_%s.json' % name; jo = GS + '/out/probe_jest_%s.json' % name
    p = subprocess.run([bin_ + 'jest', '--testMatch', '**/qa_probe/*.test.ts', '--json', '--outputFile', jo], cwd=o, capture_output=True, text=True, env=dict(os.environ, QA1031_ROWS_OUT=out, CI='1'))
    open(GS + '/out/probe_jest_%s.stderr' % name, 'w').write(p.stderr)
    j = json.load(open(jo)); P(name, now(), 'jest rc', p.returncode, 'tests', j['numTotalTests'], 'failed', j['numFailedTests'], 'suites', j['numTotalTestSuites'])
    if j['numFailedTests'] or j['numTotalTestSuites'] != 1: P(p.stderr[-3000:])
    res[name] = {(r['who'], r['id']): r for r in json.load(open(out))}
    lf = subprocess.run([bin_ + 'jest', '--listTests'], cwd=o, capture_output=True, text=True).stdout
    P('  default testMatch collects the probe:', 'qa_probe' in lf, '| default suite files listed', len([l for l in lf.splitlines() if l.strip()]))
F = lambda r: '%s %s d=%s st=%s/%s srv=%s/%s sc=%s up=%s hs=%s an=%s pv=%s' % (r.get('status'), r.get('code'), r.get('derivedSaved'), json.dumps(r.get('storedType')), json.dumps(r.get('storedDataType'), ensure_ascii=True)[:24], json.dumps(r.get('servedGET'), ensure_ascii=True)[:24], json.dumps(r.get('servedList'), ensure_ascii=True)[:24], r.get('saveCertification'), r.get('signUpstream'), r.get('holderStub'), r.get('anchorsUpstream'), r.get('provenance'))
P('legend: d=derived rows saved, st=stored type/stored data.documentType, srv=served GET/list, sc=saveCertification calls, up=issuer-certs sign hits, hs=users/stub hits, an=anchors hits, pv=recordActionProvenance calls')
relabel_head = []
for k in res['head']:
    h = res['head'][k]; dv = res['dev'].get(k, {})
    P('%-9s %-44s | dev %-118s | head %-118s | pred: %s' % (k[0], k[1][:44], F(dv), F(h), h.get('predicted')))
    if h.get('derivedSaved') and h.get('storedEqServed') is False: relabel_head.append((k, h.get('storedType'), h.get('servedGET')))
P('HEAD rows with a derived row STORED != SERVED (GET):', len(relabel_head))
for x in relabel_head: P('   ', x)
P('end', now())
