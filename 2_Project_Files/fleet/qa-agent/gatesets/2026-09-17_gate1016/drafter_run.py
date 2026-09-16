#!/usr/bin/env python3
"""drafter_run.py — #1016 (KS-1072) drafter runs in the drafter's OWN clone (drafter_paths.json). Stages:
  probe <tree> <TZ>   copy qa1016-drafter-probe.test.ts into the tree, run it alone (vitest JSON) with TZ=<TZ>, rows -> probe_rows_<tree>_<tz>.json, quarantine the copy by rename
  suite <tree>...     the whole api-gateway suite (JSON reporter) + project tsc -p . rc
  tamper <row>...     a text-anchored tamper on the HEAD tree's verification.ts (anchor count 1, marker asserted), project tsc rc, WHOLE api-gateway suite,
                      the probe (TZ=UTC) under the tamper, restore by `git checkout --` in the CLONE with sha256 asserted
  readyfile           the READY's own 150-line test file (with tier1Absent) SOLO on head and base, beside the pushed file SOLO (tier1Absent dead-flag check)
  guard               the pushed ks1072 file SOLO with its originate stub answering a confirmed tier-1 document (the seat's source guard as a tier witness)
Never rm; stderr kept in the outputs; NODE_ENV popped for the runner."""
import subprocess, os, json, sys, datetime, shutil, hashlib, re
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1016'
PATHS = json.load(open(GS + '/drafter_paths.json')); W = PATHS['W']; T = PATHS['trees']
GW = 'Blockchain/Dev/services/api-gateway'
KS = 'src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts'
def ts(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
QD = W + '/_quarantine_2026-09-17'
def quarantine(path, tag):
    os.makedirs(QD, exist_ok=True); os.rename(path, QD + '/%s.%s.%s' % (tag, datetime.datetime.now().strftime('%H%M%S%f'), os.path.basename(path)))
def vitest(tree, files, label, env_extra=None):
    cwd = T[tree] + '/' + GW; out = W + '/json_%s.json' % label
    env = dict(os.environ); env.pop('NODE_ENV', None); env.update(env_extra or {})
    t0 = datetime.datetime.now()
    p = subprocess.run([T[tree] + '/Blockchain/Dev/node_modules/.bin/vitest', 'run', *files, '--reporter=json', '--outputFile=' + out], cwd=cwd, env=env, capture_output=True, text=True)
    dt = (datetime.datetime.now() - t0).total_seconds()
    try: j = json.load(open(out))
    except Exception: P(ts(), label, 'NO JSON rc', p.returncode, 'stderr tail:', p.stderr[-2500:]); return None
    notpassed = [(tr['name'].split('/src/')[-1], a['fullName'], a['status'], (a.get('failureMessages') or [''])[0].split('\n')[0][:200]) for tr in j['testResults'] for a in tr['assertionResults'] if a['status'] != 'passed']
    suite_msgs = [(tr['name'].split('/src/')[-1], tr.get('message', '')[:300]) for tr in j['testResults'] if tr.get('message')]
    r = dict(label=label, tree=tree, rc=p.returncode, files=len(j['testResults']), tests=j['numTotalTests'], passed=j['numPassedTests'], failed=j['numFailedTests'], pending=j.get('numPendingTests'), failed_suites=j.get('numFailedTestSuites'), success=j.get('success'), secs=round(dt, 1))
    P(ts(), json.dumps(r))
    for x in notpassed: P('   NOT-PASSED', x)
    for x in suite_msgs: P('   SUITE MSG', x)
    if p.returncode != 0 and not notpassed: P('   stderr tail:', p.stderr[-1500:])
    r['notpassed'] = notpassed; json.dump(r, open(GS + '/vt_%s.json' % label, 'w'), indent=1)
    return r
def porcelain(tree):
    rc = subprocess.run(['git', '-C', T[tree], 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True)
    return len(rc.stdout.splitlines()), rc.stderr.strip()[:200]
def probe(tree, tz, tag):
    dst = T[tree] + '/' + GW + '/src/__tests__/qa1016-drafter-probe.test.ts'
    shutil.copyfile(GS + '/qa1016-drafter-probe.test.ts', dst)
    outp = GS + '/probe_rows_%s.json' % tag
    vitest(tree, ['src/__tests__/qa1016-drafter-probe.test.ts'], 'probe_' + tag, {'QA1016_OUT': outp, 'TZ': tz})
    quarantine(dst, tree)
    return json.load(open(outp))['rows']
# tamper rows: (id, old, new) on verification.ts at head; each old must count 1 in the pristine file
TIE_OLD = "return (Date.parse(b.confirmedAt) || 0) - (Date.parse(a.confirmedAt) || 0);"
ROWS = {
 'TA': ("                if (byBlock !== 0) return byBlock;\n                " + TIE_OLD + "\n", "                return byBlock; /* QA-TAMPER-TA */\n"),
 'TV': (TIE_OLD, "return (Date.parse(a.confirmedAt) || 0) - (Date.parse(b.confirmedAt) || 0); /* QA-TAMPER-TV */"),
 'TB': ("const byBlock = (b.blockNumber || 0) - (a.blockNumber || 0);", "const byBlock = (a.blockNumber || 0) - (b.blockNumber || 0); /* QA-TAMPER-TB */"),
 'TN': (TIE_OLD, "return Date.parse(b.confirmedAt) - Date.parse(a.confirmedAt); /* QA-TAMPER-TN */"),
 'TI': ("              const latest = anchors.slice().sort(", "              // qa inert comment /* QA-TAMPER-TI */\n              const latest = anchors.slice().sort("),
 'G-CTRL': (TIE_OLD, "return -1; /* QA-TAMPER-G-CTRL */"),
 'G-OLDEST': (TIE_OLD, "return (Date.parse(a.confirmedAt) || Infinity) - (Date.parse(b.confirmedAt) || Infinity); /* QA-TAMPER-G-OLDEST */"),
}
stage, args = sys.argv[1], sys.argv[2:]
P('drafter_run', stage, args, datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
if stage == 'probe':
    tree, tz = args
    rows = probe(tree, tz, '%s_%s' % (tree, tz.replace('/', '-')))
    for r in rows: P('  ', json.dumps(r))
    P('tracked porcelain', tree, *porcelain(tree))
elif stage == 'suite':
    for tree in args:
        vitest(tree, [], 'suite_' + tree)
        t0 = datetime.datetime.now()
        p = subprocess.run([T[tree] + '/Blockchain/Dev/node_modules/.bin/tsc', '--noEmit', '-p', '.'], cwd=T[tree] + '/' + GW, capture_output=True, text=True)
        P(ts(), 'project tsc -p . tree', tree, 'rc', p.returncode, 'lines', len((p.stdout + p.stderr).splitlines()), 'secs', (datetime.datetime.now() - t0).seconds)
        P('tracked porcelain', tree, *porcelain(tree))
elif stage == 'tamper':
    path = T['head'] + '/' + GW + '/src/routes/verification.ts'
    for rid in args:
        old, new = ROWS[rid]
        n0, e0 = porcelain('head'); assert n0 == 0, ('porcelain before', rid, n0, e0)
        pristine = sha(path); s = open(path).read(); n = s.count(old); assert n == 1, (rid, 'anchor count', n)
        open(path, 'w').write(s.replace(old, new))
        assert open(path).read().count('QA-TAMPER-' + rid) == 1 and sha(path) != pristine, (rid, 'marker')
        P(rid, 'landed: anchor 1, marker 1, sha', pristine[:12], '->', sha(path)[:12])
        tsc = subprocess.run([T['head'] + '/Blockchain/Dev/node_modules/.bin/tsc', '--noEmit', '-p', '.'], cwd=T['head'] + '/' + GW, capture_output=True, text=True)
        P('   project tsc rc', tsc.returncode, (tsc.stdout + tsc.stderr).strip()[:300])
        vitest('head', [], 'tamper_' + rid)
        rows = probe('head', 'UTC', 'tamper_%s' % rid)
        P('   probe rows under', rid, json.dumps([(r['id'], r['txHash'], r['confidence']) for r in rows]))
        rc = subprocess.run(['git', '-C', T['head'], 'checkout', '--', GW + '/src/routes/verification.ts'], capture_output=True, text=True)
        assert rc.returncode == 0, rc.stderr
        assert sha(path) == pristine, 'restore sha mismatch'
        P('   restored sha-identical', pristine[:12], '| porcelain', *porcelain('head'))
elif stage == 'readyfile':
    READY = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1072_ornith35b-q4_PASS-7of7_2026-09-15.diff.md'
    t = open(READY).read(); body = t.split('```diff\n', 1)[1].rsplit('```', 1)[0]
    sec = body.split('--- a/services/api-gateway/src/routes/verification.ts')[0]
    lines = sec.splitlines(); i = [k for k, l in enumerate(lines) if l.startswith('@@')][0]
    content = '\n'.join(l[1:] for l in lines[i + 1:]) + '\n'
    assert content.count('\n') == 150 and content.count('tier1Absent') == 2, (content.count('\n'), content.count('tier1Absent'))
    for tree in ('head', 'base'):
        dst = T[tree] + '/' + GW + '/src/__tests__/qa1016-ready-verbatim.test.ts'
        open(dst, 'w').write(content); P('READY test (150 lines, tier1Absent x2: declared + assigned, never read) copied into', tree, 'sha', sha(dst)[:12])
        vitest(tree, ['src/__tests__/qa1016-ready-verbatim.test.ts'], 'readyfile_' + tree)
        quarantine(dst, tree)
    for tree in ('head', 'base'):
        if tree == 'base':
            dst = T['base'] + '/' + GW + '/' + KS; shutil.copyfile(T['head'] + '/' + GW + '/' + KS, dst); P('pushed ks1072 file copied into base (red-before-green)')
        vitest(tree, [KS], 'pushedfile_' + tree)
        if tree == 'base': quarantine(dst, 'base')
elif stage == 'guard':
    f = T['head'] + '/' + GW + '/' + KS; pristine = sha(f); s = open(f).read()
    old = "  originate = http.createServer((_req, res) => {\n"
    new = "  originate = http.createServer((_req, res) => { /* QA-GUARD-T1 */\n    res.writeHead(200, jsonHead); res.end(JSON.stringify({ id: DOC_ID, contentHash: CONTENT_HASH, blockchain: { txHash: 'f'.repeat(64), blockHeight: 7, status: 'confirmed' } })); return;\n"
    assert s.count(old) == 1; open(f, 'w').write(s.replace(old, new)); assert open(f).read().count('QA-GUARD-T1') == 1
    P('GT-T1 landed (tier 1 answers a confirmed blob, txHash f*64); file sha', pristine[:12], '->', sha(f)[:12])
    vitest('head', [KS], 'guard_GT-T1')
    rc = subprocess.run(['git', '-C', T['head'], 'checkout', '--', GW + '/' + KS], capture_output=True, text=True); assert rc.returncode == 0, rc.stderr
    assert sha(f) == pristine; P('restored sha-identical', pristine[:12], '| porcelain', *porcelain('head'))
P('drafter_run end', ts())
