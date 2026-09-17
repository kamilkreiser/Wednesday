#!/usr/bin/env python3
"""drafter_run_1028.py STAGE [TREE...] — #1028 drafter runs in the drafter's own clone (drafter_paths.json). Derived from gate1023/drafter_run.py + drafter_tamper.py.
  suite  TREE... : whole api-gateway suite (vitest JSON) + project tsc --noEmit -p . rc
  tamper         : the tamper table at HEAD, each row on the WHOLE api-gateway suite, denominator asserted = T0's, pending 0, project tsc rc per row
                   (non-zero = VOID), anchor count asserted 1 + marker asserted, restore by bytes (sha asserted) + git diff --quiet
  probe  TREE... : write the real-app probe from the template to <tree>/Blockchain/Dev/qa_probe_1028/ (OUTSIDE services/api-gateway), run SOLO through a
                   scratch vitest config, assert the probe is NOT in the service's tsc program (--listFilesOnly) nor its whole-suite collection (head only),
                   rows -> out/rows_<tree>.json, quarantine the probe dir by rename
Never rm; stderr kept per run; NODE_ENV popped (vitest sets test)."""
import subprocess, os, json, sys, datetime, hashlib, re
GSD = os.path.dirname(os.path.abspath(__file__)); OUTD = GSD + '/out'; os.makedirs(OUTD + '/vt', exist_ok=True)
PA = json.load(open(GSD + '/drafter_paths.json')); W = PA['W']; C = PA['C']; T = PA['trees']; SHA = PA['sha']
GW = 'Blockchain/Dev/services/api-gateway'; AUREL = 'src/middleware/auth.ts'; TH = 'src/utils/trustHeaders.ts'
def ts(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def sha(b): return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
def quarantine(p):
    q = W + '/_quarantine_2026-09-17'; os.makedirs(q, exist_ok=True)
    d = q + '/' + datetime.datetime.now().strftime('%H%M%S%f') + '.' + p.replace('/', '__')[-120:]; os.rename(p, d); P('quarantined', p.split('/Blockchain/')[-1], '->', d.split('/')[-1])
def vitest(tree, files, label, env_extra=None, config=None):
    cwd = T[tree] + '/' + GW; out = W + '/json_%s.json' % label
    env = dict(os.environ); env.pop('NODE_ENV', None); env.update(env_extra or {})
    t0 = datetime.datetime.now()
    cmd = [T[tree] + '/Blockchain/Dev/node_modules/.bin/vitest', 'run', *files, '--reporter=json', '--outputFile=' + out] + (['--config', config] if config else [])
    p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    open(W + '/stderr_%s.txt' % label, 'w').write(p.stderr); open(W + '/stdout_%s.txt' % label, 'w').write(p.stdout)
    try: j = json.load(open(out))
    except Exception: P(ts(), label, 'NO JSON (INVALID, not a red) rc', p.returncode, 'stderr tail:', p.stderr[-1500:]); return None
    np = [(tr['name'].split('/src/')[-1], a['fullName'], a['status'], (a.get('failureMessages') or [''])[0][:400]) for tr in j['testResults'] for a in tr['assertionResults'] if a['status'] != 'passed']
    sm = [(tr['name'].split('/src/')[-1], tr.get('message', '')[:300]) for tr in j['testResults'] if tr.get('message')]
    r = dict(label=label, tree=tree, rc=p.returncode, files=len(j['testResults']), tests=j['numTotalTests'], passed=j['numPassedTests'], failed=j['numFailedTests'],
             pending=j.get('numPendingTests'), todo=j.get('numTodoTests'), secs=round((datetime.datetime.now() - t0).total_seconds(), 1),
             collected=sorted(tr['name'].split('/Blockchain/')[-1] for tr in j['testResults']))
    r['VALID'] = r['tests'] > 0
    P(ts(), json.dumps({k: v for k, v in r.items() if k != 'collected'}))
    for x in np: P('   NOT-PASSED', x[:3], '|', x[3].split('\n')[0][:260])
    for x in sm: P('   SUITE MSG', x)
    r['notpassed'] = np; json.dump(r, open(OUTD + '/vt/vt_%s.json' % label, 'w'), indent=1)
    return r
def tsc(tree, extra=None):
    p = subprocess.run([T[tree] + '/Blockchain/Dev/node_modules/.bin/tsc', '--noEmit', '-p', '.'] + (extra or []), cwd=T[tree] + '/' + GW, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr)
def porcelain(tree):
    r = subprocess.run(['git', '-C', T[tree], 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True); return len(r.stdout.splitlines()), r.stdout[:300] + r.stderr[:200]
def diffquiet(tree): return subprocess.run(['git', '-C', T[tree], 'diff', '--quiet'], capture_output=True).returncode

AU_OLD_V = "      if (decoded.verificationLevel) req.headers['x-verification-level'] = decoded.verificationLevel;\n      else delete req.headers['x-verification-level'];\n"
AU_OLD_E = "      if (decoded.email) req.headers['x-user-email'] = decoded.email;\n"
ROWS = [
  ('T0', None, None, None, 'none'),
  ('RP-DEV', AUREL, 'BYTES', 'dev', 'auth.ts = develop 19f1e5475 bytes (b8fce678a)'),
  ('RP-PREMERGE', AUREL, 'BYTES', 'pre', 'auth.ts = fb503741a bytes (c673f9c9e: the fix without KS-1207)'),
  ('EDIT1ONLY', AUREL, AU_OLD_V, "      req.headers['x-verification-level'] = decoded.verificationLevel; // qa1028-tamper EDIT1ONLY\n", 'the verificationLevel guard + else-delete reverted to the unguarded set'),
  ('EDIT2ONLY', AUREL, AU_OLD_E, "      req.headers['x-user-email'] = decoded.email; // qa1028-tamper EDIT2ONLY\n", 'the email guard reverted to the unguarded set'),
  ('NOELSE', AUREL, "      else delete req.headers['x-verification-level'];\n", "      // qa1028-tamper NOELSE\n", 'the else-delete removed'),
  ('TI', AUREL, AU_OLD_E, "      // qa1028-tamper TI inert\n" + AU_OLD_E, 'inert comment'),
  ('G-UNDEFONLY', AUREL, AU_OLD_V + "\n", AU_OLD_V.replace('if (decoded.verificationLevel)', 'if (decoded.verificationLevel !== undefined)') + "      // qa1028-tamper G-UNDEFONLY\n\n", 'verificationLevel guard `!== undefined` (empty string / null / 0 / false now forwarded)'),
  ('G-VNEVER', AUREL, 'if (decoded.verificationLevel) req.headers', 'if (false as boolean /* qa1028-tamper G-VNEVER */) req.headers', 'the level is never forwarded (always deleted)'),
  ('G-ENEVER', AUREL, 'if (decoded.email) req.headers', 'if (false as boolean /* qa1028-tamper G-ENEVER */) req.headers', 'the email is never forwarded'),
  ('G-STRIPUSER', TH, 'export const TRUST_HEADER_PATTERN =\n  /^x-(user|tenant|', 'export const TRUST_HEADER_PATTERN = // qa1028-tamper G-STRIPUSER\n  /^x-(tenant|', 'the edge strip no longer covers x-user-* (the email half of the fix relies on it) — qa1028-tamper G-STRIPUSER'),
  ('G-VDELETEFIRST', AUREL, AU_OLD_V, "      delete req.headers['x-verification-level']; // qa1028-tamper G-VDELETEFIRST\n      if (decoded.verificationLevel) req.headers['x-verification-level'] = decoded.verificationLevel;\n", 'equivalent refactor (delete then set) — must be 0 reds (a green control for the row runner)'),
]
def tamper():
    tree = 'head'; base = T[tree] + '/' + GW + '/'
    rc0, _ = tsc(tree); P(ts(), 'T0 project tsc rc', rc0)
    t0 = None; table = []
    for rid, rel, old, new, form in ROWS:
        f = base + rel if rel else None; orig = open(f, 'rb').read() if f else None; osha = sha(orig) if f else None
        row = dict(row=rid, file=rel, form=form)
        try:
            if f:
                if old == 'BYTES':
                    src = subprocess.run(['git', '-C', C, 'show', SHA[new] + ':' + GW + '/' + rel], capture_output=True).stdout
                    open(f, 'wb').write(src); row['landed'] = sha(src) != osha and sha(open(f, 'rb').read()) == sha(src); row['swapped_to'] = sha(src)[:9]
                else:
                    s = orig.decode(); n = s.count(old)
                    if n != 1: row['VOID'] = 'anchor count %d' % n; P('ROW', rid, 'VOID anchor count', n); table.append(row); continue
                    s2 = s.replace(old, new); open(f, 'w').write(s2); row['landed'] = ('qa1028-tamper' in s2 or rid == 'TI') and s2 != s and open(f).read() == s2
                assert row['landed'], ('tamper did not land', rid)
            rc, txt = tsc(tree); row['tsc_rc'] = rc
            if rc != 0: row['VOID'] = 'tsc rc %d' % rc; row['tsc_head'] = txt[:400]
            r = vitest(tree, [], 'tamper_' + rid)
            if r is None: row['VOID'] = 'no json'
            else:
                if rid == 'T0': t0 = (r['files'], r['tests'])
                row.update(files=r['files'], tests=r['tests'], failed=r['failed'], pending=r['pending'], denominator_ok=(r['files'], r['tests']) == t0)
                reds = {}
                for fn, full, st, msg in r['notpassed']: reds.setdefault(fn.split('/')[-1], []).append((full[-90:], msg.split('\n')[0][:160]))
                row['reds'] = reds; row['non_assertion'] = sum(1 for fn, full, st, msg in r['notpassed'] if 'AssertionError' not in msg)
        finally:
            if f:
                open(f, 'wb').write(orig); row['restored_sha'] = sha(open(f, 'rb').read()) == osha
        row['git_diff_quiet'] = diffquiet(tree); row['porcelain'] = porcelain(tree)[0]
        P('ROW', json.dumps({k: v for k, v in row.items() if k != 'reds'})); [P('    red', k, len(v), v[:6]) for k, v in (row.get('reds') or {}).items()]
        table.append(row)
    json.dump(table, open(OUTD + '/tamper_rows.json', 'w'), indent=1)
def probe(tree):
    D = T[tree] + '/Blockchain/Dev/qa_probe_1028'; os.makedirs(D)
    src = open(GSD + '/qa1028-drafter-probe.template.ts').read().replace('__GW_SRC__', T[tree] + '/' + GW + '/src')
    pf = D + '/qa1028-drafter-probe.test.ts'; open(pf, 'w').write(src)
    cfg = D + '/vitest.qa1028.config.mts'
    open(cfg, 'w').write("import { defineConfig } from 'vitest/config';\nexport default defineConfig({ root: %r, test: { globals: true, environment: 'node', setupFiles: [%r], include: [%r], dir: %r } });\n"
                         % (T[tree] + '/' + GW, T[tree] + '/' + GW + '/vitest.setup.ts', pf, D))
    P('probe written', pf.split('/Blockchain/')[-1], 'sha256', hashlib.sha256(src.encode()).hexdigest()[:12], '| template sha256', hashlib.sha256(open(GSD + '/qa1028-drafter-probe.template.ts', 'rb').read()).hexdigest()[:12])
    try:
        rc, txt = tsc(tree, ['--listFilesOnly']); inprog = [l for l in txt.splitlines() if 'qa_probe' in l]; ctl = [l for l in txt.splitlines() if l.endswith('/src/middleware/auth.ts')]
        P('F-3 control: service tsc program files with qa_probe:', len(inprog), '| positive control auth.ts listed:', len(ctl), '| rc', rc)
        if tree == 'head':
            r = vitest(tree, [], 'suite_with_probe_present_' + tree)
            if r: P('F-3 control: whole-suite collected files with probe present', r['files'], '| qa_probe collected:', sum('qa_probe' in x for x in r['collected']))
        r = vitest(tree, [], 'probe_' + tree, {'QA_OUT': OUTD + '/rows_%s.json' % tree}, config=cfg)
        if r: P('probe run', tree, 'files', r['files'], 'tests', r['tests'], 'failed', r['failed'])
    finally:
        quarantine(D)
if __name__ == '__main__':
    stage, trees = sys.argv[1], sys.argv[2:]
    P('run', stage, trees, datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
    if stage == 'tamper': tamper()
    for tree in trees:
        if stage == 'suite':
            vitest(tree, [], 'suite_' + tree); rc, txt = tsc(tree); P(ts(), 'project tsc --noEmit -p . tree', tree, 'rc', rc, txt[:400])
        elif stage == 'probe': probe(tree)
        P('tracked porcelain', tree, porcelain(tree))
    P('run end', ts())
