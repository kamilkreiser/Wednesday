#!/usr/bin/env python3
"""logprobe_gate33.py <scratchpad> — the DRAFTER's WIDEN measurement for gate33's three logging rows (#1310 KS-1348 r2, #1311 / #1312 KS-1346 A / B):
CAN ANY SECRET OR PII VALUE STILL REACH A LOG LINE OR A PRODUCTION LOG FILE, BY ANY PATH, IN THE TOUCHED FILES? Shape copied from gate31's logprobe
(gate31 lineage: that run measured #1302 and found all six sentinels reaching both files), re-keyed and WIDENED for gate33.

Instrument: originate's REAL utils/logger.ts read from the scratch clone at each revision (`git show <rev>:<path>`), transpiled to CommonJS with the
checkout's OWN typescript (transpileModule, READ from node_modules), run by node with NODE_ENV=production and the checkout's OWN winston (NODE_PATH, a
READ of node_modules) in a FRESH scratch cwd per revision (the File transports write logs/error.log and logs/combined.log relative to cwd). The
fail500 LOG EXPRESSION of routes/systemErrors.ts and routes/gdpr.ts is read at the SAME revision (the ONE line after `function fail500(`, asserted
byte-unique as a whole line) and evaluated as JavaScript with the real logger — so the KS-1346 line is measured through the real logger and its real
files, not through a mock. Revisions: live develop (the pin), #1310's head, END_TREE (develop + the six; pins_gate33.json), and #1302's head (the
closed predecessor, fetched into the scratch clone under refs/g33/closed/1302: a POSITIVE CONTROL — at #1302 every top-level sentinel must reach
both files, or the instrument cannot see a leak).

PROBES (each carries its OWN sentinels, so every hit is attributable to exactly one path):
  P1 TOP-LEVEL six keys (password, token, apiKey, email, subject.ssn, headers.authorization) — the ruled class; #1310 must redact all six.
  P2 a NESTED Error in the metadata with ENUMERABLE own properties (an axios-shaped `config.headers.Authorization` and `response.data.token`) — the
     PR body discloses "Error instances nested in metadata pass through unredacted"; measured here per sink.
  P3 KEY VARIANTS the suffix rule does not name (passwordHash, privateKey, secretKey, email_address, userEmails[], phone, mnemonic) — disclosed in part.
  P4 a secret-looking VALUE inside the MESSAGE string (an email and a bearer) — the ruling keeps the message readable; measured, not graded here.
  P5 a TOP-LEVEL Error as the first argument with an enumerable `password` property (winston's errors() format copies own props to the top level).
  P6 the fail500 EXPRESSION of routes/systemErrors.ts at that revision over a thrown PLAIN OBJECT whose FIELD NAMES are PII (an email address as a
     key) and whose values are secrets — under KS-1346's ruling the field NAMES are logged, never the values.
  P7 the same over routes/gdpr.ts's fail500 expression.
  P8 fail500 (systemErrors) over an Error whose MESSAGE carries a sentinel — the error text is logged by design (the ruling).
CONTROLS: stdout (the Console transport, JSON in production) must carry P1's sentinels at develop (the instrument reads the sink the logger writes);
#1302's head files must carry every P1 sentinel (the instrument can see a file leak); a sentinel-free POSITIVE line must appear in #1310's combined.log
(the capture reads the file the transport wrote). Nothing is written outside <scratchpad>/g33_logprobe_*; nothing in the checkout is written."""
import json, os, re, subprocess, sys, datetime
SP = sys.argv[1] if len(sys.argv) > 1 else ''
if not re.match(r'^/private/tmp/claude-501/.*/scratchpad', SP) or not os.path.isdir(SP): print('usage: logprobe_gate33.py <scratchpad>'); sys.exit(9)
GS = os.path.dirname(os.path.abspath(__file__))
CL = os.path.join(SP, 'g33_sp', 'clone.git')
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
NM = CHECKOUT + '/Blockchain/Dev/node_modules'
O = 'Blockchain/Dev/services/originate/src/'
LOG, SYSERR, GDPR = O + 'utils/logger.ts', O + 'routes/systemErrors.ts', O + 'routes/gdpr.ts'
PINS = json.load(open(os.path.join(GS, 'pins_gate33.json'), encoding='utf-8'))
def run(cmd, **kw): return subprocess.run(cmd, capture_output=True, text=True, **kw)
env0 = dict(os.environ); ssh = run(['git', '-C', CHECKOUT, 'config', '--get', 'core.sshCommand']).stdout.strip()
if ssh: env0['GIT_SSH_COMMAND'] = ssh
fr = run(['perl', '-e', 'alarm 300; exec @ARGV', 'git', '--git-dir', CL, 'fetch', '-q', 'origin', '+refs/pull/1302/head:refs/g33/closed/1302'], env=env0)
REVS = [('develop (the pin)', PINS['develop']), ('#1310 head', PINS['prs']['1310']['head']), ('END_TREE', PINS['end_tree']),
        ('#1302 head (CLOSED predecessor; control)', run(['git', '--git-dir', CL, 'rev-parse', 'refs/g33/closed/1302']).stdout.strip())]
P1 = {'password': 'S33PW-hunter2-p1', 'token': 'S33TOK-eyJhbGci-p1', 'apiKey': 'S33KEY-sk_live_p1', 'email': 's33.p1@example.test', 'ssn': 'S33SSN-123-45-6781', 'authorization': 'Bearer S33BEARER-p1'}
P2 = {'nestedErr.config.headers.Authorization': 'Bearer S33AXIOS-p2', 'nestedErr.response.data.token': 'S33NESTTOK-p2'}
P3 = {'passwordHash': 'S33PWHASH-p3', 'privateKey': 'S33PRIVKEY-p3', 'secretKey': 'S33SECKEY-p3', 'email_address': 's33.p3addr@example.test', 'userEmails[]': 's33.p3list@example.test', 'phone': 'S33PHONE-0400111222', 'mnemonic': 'S33MNEMONIC-abandon-p3'}
P4 = {'message email': 's33.p4msg@example.test', 'message bearer': 'S33MSGBEARER-p4'}
P5 = {'top-level Error.password': 'S33TOPERRPW-p5'}
P6 = {'systemErrors field NAME (an email as a key)': 's33.p6key@example.test', 'systemErrors field VALUE (a secret)': 'S33P6VAL-secret'}
P7 = {'gdpr field NAME (an email as a key)': 's33.p7key@example.test', 'gdpr field VALUE (a secret)': 'S33P7VAL-secret'}
P8 = {'systemErrors Error.message': 'S33P8ERRTEXT'}
PROBES = {'P1': P1, 'P2': P2, 'P3': P3, 'P4': P4, 'P5': P5, 'P6': P6, 'P7': P7, 'P8': P8}
PROBE = r"""
const { logger } = require('./logger.js');
const P = JSON.parse(process.env.S33);
const fail500SE = require('./fail500_systemErrors.js'), fail500GD = require('./fail500_gdpr.js');
logger.info('S33 POSITIVE a plain line with no secret');
logger.error('S33 P1 fail500-shaped', { error: 'thrown text', password: P.P1.password, token: P.P1.token, apiKey: P.P1.apiKey, email: P.P1.email, subject: { ssn: P.P1.ssn }, headers: { authorization: P.P1.authorization } });
const ne = new Error('S33 P2 nested error message'); ne.config = { headers: { Authorization: P.P2['nestedErr.config.headers.Authorization'] } }; ne.response = { data: { token: P.P2['nestedErr.response.data.token'] } };
logger.error('S33 P2 an axios-shaped error nested in metadata', { error: ne });
logger.error('S33 P3 key variants', { passwordHash: P.P3.passwordHash, privateKey: P.P3.privateKey, secretKey: P.P3.secretKey, email_address: P.P3.email_address, userEmails: [P.P3['userEmails[]']], phone: P.P3.phone, mnemonic: P.P3.mnemonic });
logger.error('S33 P4 login failed for ' + P.P4['message email'] + ' with Bearer ' + P.P4['message bearer']);
const te = new Error('S33 P5 top-level error'); te.password = P.P5['top-level Error.password'];
logger.error(te);
const k6 = {}; k6[P.P6['systemErrors field NAME (an email as a key)']] = P.P6['systemErrors field VALUE (a secret)'];
fail500SE(logger, 'S33 P6 systemErrors fail500', k6);
const k7 = {}; k7[P.P7['gdpr field NAME (an email as a key)']] = P.P7['gdpr field VALUE (a secret)'];
fail500GD(logger, 'S33 P7 gdpr fail500', k7);
fail500SE(logger, 'S33 P8 systemErrors fail500', new Error('thrown text ' + P.P8['systemErrors Error.message']));
logger.on('finish', () => setTimeout(() => process.exit(0), 400));
logger.end();
setTimeout(() => process.exit(3), 9000);
"""
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
ts = json.load(open(os.path.join(NM, 'typescript', 'package.json')))['version']; wv = json.load(open(os.path.join(NM, 'winston', 'package.json')))['version']
lf = json.load(open(os.path.join(NM, 'logform', 'package.json')))['version'] if os.path.exists(os.path.join(NM, 'logform', 'package.json')) else '?'
print('logprobe_gate33 %s | node %s | typescript %s | winston %s | logform %s (READ from %s) | #1302 fetch rc %d' % (now, run(['node', '--version']).stdout.strip(), ts, wv, lf, NM, fr.returncode))
def fail500_js(rev, path):
    src = run(['git', '--git-dir', CL, 'show', '%s:%s' % (rev, path)]).stdout.split('\n')
    i = [k for k, l in enumerate(src) if l.startswith('function fail500(')]
    if len(i) != 1: return None, 'fail500 declared %d time(s)' % len(i)
    line = src[i[0] + 1]
    if sum(1 for l in src if l == line) != 1 or 'logger.error(context,' not in line: return None, 'the fail500 log line is not byte-unique / not a logger.error(context, …) line: %r' % line[:120]
    return 'module.exports = function (logger, context, err) {\n' + line + '\n};\n', line.strip()
res = {}
FAILS = []
for lab, rev in REVS:
    if not re.match(r'^[0-9a-f]{40}$', rev or ''): FAILS.append('%s: no revision (%r)' % (lab, rev)); continue
    blob = run(['git', '--git-dir', CL, 'rev-parse', '--verify', '-q', '%s:%s' % (rev, LOG)]).stdout.strip()
    if not re.match(r'^[0-9a-f]{40}$', blob): FAILS.append('%s: logger.ts not readable at %s (UNFETCHED?)' % (lab, rev[:12])); continue
    W = os.path.join(SP, 'g33_logprobe_%s_%s' % (rev[:12], datetime.datetime.now().strftime('%H%M%S%f')[:8])); os.makedirs(W)
    open(os.path.join(W, 'logger.ts'), 'w').write(run(['git', '--git-dir', CL, 'show', '%s:%s' % (rev, LOG)]).stdout)
    lines = {}
    for nm, pth in (('systemErrors', SYSERR), ('gdpr', GDPR)):
        js, line = fail500_js(rev, pth)
        if js is None: FAILS.append('%s: %s %s' % (lab, nm, line)); js = 'module.exports = function () { throw new Error("no fail500 line"); };\n'
        open(os.path.join(W, 'fail500_%s.js' % nm), 'w').write(js); lines[nm] = line
    tr = run(['node', '-e', "const ts=require(process.argv[1]);const fs=require('fs');const o=ts.transpileModule(fs.readFileSync('logger.ts','utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2020,esModuleInterop:true}});fs.writeFileSync('logger.js',o.outputText)", os.path.join(NM, 'typescript')], cwd=W)
    open(os.path.join(W, 'probe.js'), 'w').write(PROBE)
    env = dict(os.environ, NODE_ENV='production', NODE_PATH=NM, S33=json.dumps(PROBES)); env.pop('LOG_LEVEL', None)
    r = run(['node', 'probe.js'], cwd=W, env=env)
    sinks = {'stdout': r.stdout}
    for f in ('logs/error.log', 'logs/combined.log'):
        p = os.path.join(W, f); sinks[f] = open(p, encoding='utf-8', errors='replace').read() if os.path.exists(p) else None
    out = {'rev': rev, 'logger_blob': blob, 'fail500_lines': lines, 'transpile_rc': tr.returncode, 'probe_rc': r.returncode, 'stderr': r.stderr[-400:], 'workdir': W, 'hits': {}}
    for sk, t in sinks.items():
        out['hits'][sk] = {pn: sorted(k for k, v in pv.items() if t and v in t) for pn, pv in PROBES.items()}
    out['file_lines'] = {f: (len(sinks[f].splitlines()) if sinks[f] else None) for f in ('logs/error.log', 'logs/combined.log')}
    out['positive_in_combined'] = bool(sinks['logs/combined.log'] and 'S33 POSITIVE' in sinks['logs/combined.log'])
    out['first_file_line'] = (sinks['logs/error.log'] or '').splitlines()[0][:200] if sinks['logs/error.log'] else None
    res[lab] = out
    print('== %s %s | logger.ts blob %s | workdir %s | transpile rc %d | probe rc %d%s' % (lab, rev[:12], blob[:12], W, tr.returncode, r.returncode, (' | stderr: ' + r.stderr.strip()[-240:]) if r.stderr.strip() else ''))
    print('   fail500 log line (systemErrors): %s' % lines.get('systemErrors', '?')[:170])
    print('   fail500 log line (gdpr)        : %s' % lines.get('gdpr', '?')[:170])
    print('   file lines: %s | positive line in combined.log: %s | error.log first line: %r' % (out['file_lines'], out['positive_in_combined'], out['first_file_line']))
    for sk in ('stdout', 'logs/error.log', 'logs/combined.log'):
        print('   %-18s %s' % (sk, ' | '.join('%s %s' % (pn, h or '-') for pn, h in out['hits'][sk].items())))
D, H, E, C = (res.get(k) for k in ('develop (the pin)', '#1310 head', 'END_TREE', '#1302 head (CLOSED predecessor; control)'))
ok = bool(D and H and E and C)
ctl = {}
if ok:
    ctl['stdout at develop carries every P1 sentinel'] = D['hits']['stdout']['P1'] == sorted(P1)
    ctl['#1302 head: BOTH files carry every P1 sentinel (the instrument sees a file leak)'] = all(C['hits'][f]['P1'] == sorted(P1) for f in ('logs/error.log', 'logs/combined.log'))
    ctl['#1310 head: the POSITIVE line is in combined.log (the capture reads the written file)'] = H['positive_in_combined']
    ctl['every probe ran (rc 0) at every revision'] = all(x['probe_rc'] == 0 and x['transpile_rc'] == 0 for x in res.values())
for k, v in ctl.items(): print('CONTROL %s: %s' % (k, v))
ctl_ok = ok and all(ctl.values()) and not FAILS
for f in FAILS: print('FAIL %s' % f)
if ok:
    for lab, X in (('#1310 head', H), ('END_TREE', E)):
        newf = {f: {pn: sorted(set(X['hits'][f][pn]) - set(D['hits'][f][pn])) for pn in PROBES} for f in ('logs/error.log', 'logs/combined.log')}
        newf = {f: {pn: v for pn, v in d.items() if v} for f, d in newf.items()}
        print('RESULT (MEASURED by the drafter) %s: sentinels that reach a production log FILE and did NOT at develop: %s' % (lab, newf or 'NONE'))
        print('RESULT (MEASURED by the drafter) %s: stdout sentinels by probe: %s' % (lab, {pn: v for pn, v in X['hits']['stdout'].items() if v}))
        res[lab]['new_in_files_vs_develop'] = newf
    print('RESULT P1 (the ruled class) at #1310 head in the files: %s — at END_TREE: %s' % ({f: H['hits'][f]['P1'] for f in ('logs/error.log', 'logs/combined.log')}, {f: E['hits'][f]['P1'] for f in ('logs/error.log', 'logs/combined.log')}))
res['_controls'] = ctl; res['_fails'] = FAILS; res['_probes'] = {pn: sorted(pv) for pn, pv in PROBES.items()}
json.dump(res, open(os.path.join(GS, 'logprobe_gate33.json'), 'w'), indent=1)
print('SUMMARY logprobe_gate33: controls %s (%d of %d) | fails %d' % ('PASS' if ctl_ok else 'FAIL', sum(ctl.values()), len(ctl), len(FAILS)))
sys.exit(0 if ctl_ok else 1)
