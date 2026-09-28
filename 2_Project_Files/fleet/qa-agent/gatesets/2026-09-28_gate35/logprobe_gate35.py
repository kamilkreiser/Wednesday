#!/usr/bin/env python3
"""logprobe_gate35.py <scratchpad> — the DRAFTER's WIDEN measurement for gate35's logging row (#1321 KS-1348 r3, the file allow-list): CAN ANY SECRET OR
PII VALUE REACH A PRODUCTION LOG FILE (or stdout) THROUGH THE REAL LOGGER, AND DO THE MESSAGE AND THE ERROR TEXT STILL REACH THE FILES? Shape copied from
gate33's logprobe (the run that held #1310 NO GO on the LOG-FILE WIDEN: a nested Error's secrets and the unnamed keys reached both files), re-keyed for
gate35 and REPEATED here with the same probe classes plus the ones gate33's fix-shape named (toJSON, ip, jwt, sessionId, recipientPhone).

Instrument: originate's REAL utils/logger.ts read from the scratch clone at each revision (`git show <rev>:<path>`), transpiled to CommonJS with the
checkout's OWN typescript (transpileModule, READ from node_modules), run by node with NODE_ENV=production and the checkout's OWN winston (NODE_PATH, a
READ of node_modules) in a FRESH scratch cwd per revision (the File transports write logs/error.log and logs/combined.log relative to cwd). stdout is
the Console transport. Revisions: live develop (the pin; its File transports carry no format and write `undefined`), #1321's head, END_TREE (pins_gate35
.json), #1310's head (r2, CLOSED unmerged — fetched into the scratch clone under refs/g35/closed/1310: the FILE-LEAK CONTROL, it must put P2 / P3 into
both files as gate33 measured, or the instrument cannot see a file leak), and ONE PLANTED ARM: #1321's logger with 'ip' appended to FILE_LOG_FIELDS
(built in the workdir only — the brief's arm; the P3 ip sentinel must then reach both files, or the instrument cannot see a one-key widen).

PROBES (each carries its OWN sentinels, so every hit is attributable to exactly one path). Classes: VALUE (must reach NO file at the head); TEXT (must
reach BOTH files at the head: the ruling keeps the message and the string error text); RESIDUE (reaches the files BY DESIGN through an allow-listed
string field — reported, for the gate to rule); LOSS (the disclosed consequence: absent from the files at the head).
  P1  VALUE  the six ruled keys at top level (password, token, apiKey, email, subject.ssn, headers.authorization).
  P2  VALUE  a NESTED Error with ENUMERABLE config.headers.Authorization and response.data.token — under `error` AND under `upstream`.
  P2T VALUE  toJSON: a nested Error whose toJSON() exposes a secret (under `upstream`), and a top-level metadata object with its own toJSON().
  P3  VALUE  the unnamed keys: secretKey, privateKey, passwordHash, mnemonic, phone, email_address, userEmails[], ip, jwt, sessionId, recipientPhone.
  P5  VALUE  a top-level Error as the first argument with an enumerable `password` (winston's errors() copies own props).
  P8  LOSS   userId, documentId, ip and a stack line — the keys the files drop (the body names them); a Request-error-shaped line as errorHandler logs it.
  P4  TEXT   an email and a bearer INSIDE the message string (the ruling keeps the message readable).
  P6  TEXT   a string `error` text (the fail500 shape).
  P7  RESIDUE gate33 W-3: `error: String(<Array>)` and `error: String(<toString object>)` — a string, so it passes the allow-list.
  P9  RESIDUE allow-listed carriers: `path` with a query token, `requestId`, and a `message` key in the metadata (winston appends it to the message).
CONTROLS: stdout at develop carries every P1 sentinel; #1310's head puts every P2 and P3 sentinel into BOTH files; #1321's head writes the POSITIVE line
into combined.log; the planted 'ip' arm puts the ip sentinel into BOTH files and the head does not; every probe ran rc 0 at every revision.
Nothing is written outside <scratchpad>/g35_logprobe_*; nothing in the checkout is written. Writes logprobe_gate35.json beside this script."""
import json, os, re, subprocess, sys, datetime
SP = sys.argv[1] if len(sys.argv) > 1 else ''
if not re.match(r'^/private/tmp/claude-501/.*/scratchpad', SP) or not os.path.isdir(SP): print('usage: logprobe_gate35.py <scratchpad>'); sys.exit(9)
GS = os.path.dirname(os.path.abspath(__file__))
CL = os.path.join(SP, 'g35_sp', 'clone.git')
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
NM = CHECKOUT + '/Blockchain/Dev/node_modules'
LOG = 'Blockchain/Dev/services/originate/src/utils/logger.ts'
PINS = json.load(open(os.path.join(GS, 'pins_gate35.json'), encoding='utf-8'))
def run(cmd, **kw): return subprocess.run(cmd, capture_output=True, text=True, **kw)
env0 = dict(os.environ); ssh = run(['git', '-C', CHECKOUT, 'config', '--get', 'core.sshCommand']).stdout.strip()
if ssh: env0['GIT_SSH_COMMAND'] = ssh
fr = run(['perl', '-e', 'alarm 300; exec @ARGV', 'git', '--git-dir', CL, 'fetch', '-q', 'origin', '+refs/pull/1310/head:refs/g35/closed/1310'], env=env0)
HEAD = PINS['prs']['1321']['head']
ARM = '#1321 head + planted `ip` in FILE_LOG_FIELDS (ARM)'
REVS = [('develop (the pin)', PINS['develop']), ('#1321 head', HEAD), ('END_TREE', PINS['end_tree']),
        ('#1310 head (CLOSED r2; FILE-LEAK control)', run(['git', '--git-dir', CL, 'rev-parse', 'refs/g35/closed/1310']).stdout.strip()), (ARM, HEAD)]
P1 = {'password': 'S35PW-hunter2-p1', 'token': 'S35TOK-eyJhbGci-p1', 'apiKey': 'S35KEY-sk_live_p1', 'email': 's35.p1@example.test', 'ssn': 'S35SSN-123-45-6781', 'authorization': 'Bearer S35BEARER-p1'}
P2 = {'error.config.headers.Authorization': 'Bearer S35AXIOS-p2e', 'error.response.data.token': 'S35NESTTOK-p2e', 'upstream.config.headers.Authorization': 'Bearer S35AXIOS-p2u', 'upstream.response.data.token': 'S35NESTTOK-p2u'}
P2T = {'upstream Error toJSON()': 'S35TOJSON-err-p2t', 'top-level meta toJSON()': 'S35TOJSON-meta-p2t'}
P3 = {'secretKey': 'S35SECKEY-p3', 'privateKey': 'S35PRIVKEY-p3', 'passwordHash': 'S35PWHASH-p3', 'mnemonic': 'S35MNEMONIC-abandon-p3', 'phone': 'S35PHONE-0400111222',
      'email_address': 's35.p3addr@example.test', 'userEmails[]': 's35.p3list@example.test', 'ip': 'S35IP-203.0.113.35', 'jwt': 'S35JWT-eyJ-p3', 'sessionId': 'S35SESS-p3', 'recipientPhone': 'S35RPHONE-0400999888'}
P5 = {'top-level Error.password': 'S35TOPERRPW-p5'}
P8 = {'userId': 'S35USERID-p8', 'documentId': 'S35DOCID-p8', 'ip (errorHandler shape)': 'S35IP8-198.51.100.8', 'stack (a frame name)': 'S35STACKFRAME_p8'}
P4 = {'message email': 's35.p4msg@example.test', 'message bearer': 'S35MSGBEARER-p4'}
P6 = {'error text (string)': 'S35ERRTEXT-p6'}
P7 = {'String(Array) element': 'S35W3ARR-p7', 'String(toString obj)': 'S35W3TOSTR-p7'}
P9 = {'path query token': 'S35PATHTOK-p9', 'requestId': 'S35REQID-p9', 'metadata message key': 'S35METAMSG-p9'}
PROBES = {'P1': P1, 'P2': P2, 'P2T': P2T, 'P3': P3, 'P5': P5, 'P8': P8, 'P4': P4, 'P6': P6, 'P7': P7, 'P9': P9}
CLASS = {'P1': 'VALUE', 'P2': 'VALUE', 'P2T': 'VALUE', 'P3': 'VALUE', 'P5': 'VALUE', 'P8': 'LOSS', 'P4': 'TEXT', 'P6': 'TEXT', 'P7': 'RESIDUE', 'P9': 'RESIDUE'}
PROBE = r"""
const { logger } = require('./logger.js');
const P = JSON.parse(process.env.S35);
logger.info('S35 POSITIVE a plain line with no secret');
logger.error('S35 P1 fail500-shaped', { error: 'thrown text', password: P.P1.password, token: P.P1.token, apiKey: P.P1.apiKey, email: P.P1.email, subject: { ssn: P.P1.ssn }, headers: { authorization: P.P1.authorization } });
const ne = new Error('S35 P2 nested error message'); ne.config = { headers: { Authorization: P.P2['error.config.headers.Authorization'] } }; ne.response = { data: { token: P.P2['error.response.data.token'] } };
logger.error('S35 P2 an axios-shaped error nested under error', { error: ne });
const nu = new Error('S35 P2 nested upstream message'); nu.config = { headers: { Authorization: P.P2['upstream.config.headers.Authorization'] } }; nu.response = { data: { token: P.P2['upstream.response.data.token'] } };
logger.error('S35 P2 an axios-shaped error nested under upstream', { upstream: nu });
const tj = new Error('S35 P2T error with toJSON'); tj.toJSON = () => ({ leaked: P.P2T['upstream Error toJSON()'] });
logger.error('S35 P2T toJSON nested', { upstream: tj });
const mt = { requestId: 'S35 P2T meta', toJSON: () => ({ leaked: P.P2T['top-level meta toJSON()'] }) };
logger.error('S35 P2T toJSON top-level meta', mt);
logger.error('S35 P3 key variants', { secretKey: P.P3.secretKey, privateKey: P.P3.privateKey, passwordHash: P.P3.passwordHash, mnemonic: P.P3.mnemonic, phone: P.P3.phone, email_address: P.P3.email_address, userEmails: [P.P3['userEmails[]']], ip: P.P3.ip, jwt: P.P3.jwt, sessionId: P.P3.sessionId, recipientPhone: P.P3.recipientPhone });
const te = new Error('S35 P5 top-level error'); te.password = P.P5['top-level Error.password'];
logger.error(te);
const se = new Error('S35 P8 stack carrier'); se.stack = 'Error: S35 P8 stack carrier\n    at ' + P.P8['stack (a frame name)'] + ' (/app/x.js:1:1)';
logger.error('S35 P8 Request error', { message: 'S35 P8 request failed', statusCode: 500, path: '/api/p8', method: 'POST', userId: P.P8.userId, documentId: P.P8.documentId, ip: P.P8['ip (errorHandler shape)'], stack: se.stack });
logger.error('S35 P4 login failed for ' + P.P4['message email'] + ' with Bearer ' + P.P4['message bearer']);
logger.error('S35 P6 Admin config request failed (POST /api/admin/p6)', { error: P.P6['error text (string)'] });
logger.error('S35 P7 System error ingest failed', { error: String([P.P7['String(Array) element'], 'x']) });
logger.error('S35 P7 Client error ingest failed', { error: String({ toString: () => P.P7['String(toString obj)'] }) });
logger.error('S35 P9 carriers', { path: '/api/p9?token=' + P.P9['path query token'], requestId: P.P9.requestId, method: 'GET', statusCode: 400, message: P.P9['metadata message key'] });
logger.on('finish', () => setTimeout(() => process.exit(0), 400));
logger.end();
setTimeout(() => process.exit(3), 9000);
"""
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
ts = json.load(open(os.path.join(NM, 'typescript', 'package.json')))['version']; wv = json.load(open(os.path.join(NM, 'winston', 'package.json')))['version']
lf = json.load(open(os.path.join(NM, 'logform', 'package.json')))['version'] if os.path.exists(os.path.join(NM, 'logform', 'package.json')) else '?'
print('logprobe_gate35 %s | node %s | typescript %s | winston %s | logform %s (READ from %s) | #1310 fetch rc %d' % (now, run(['node', '--version']).stdout.strip(), ts, wv, lf, NM, fr.returncode))
res = {}
FAILS = []
ALLOW_OLD = "'statusCode'];"; ALLOW_NEW = "'statusCode', 'ip'];"
for lab, rev in REVS:
    if not re.match(r'^[0-9a-f]{40}$', rev or ''): FAILS.append('%s: no revision (%r)' % (lab, rev)); continue
    blob = run(['git', '--git-dir', CL, 'rev-parse', '--verify', '-q', '%s:%s' % (rev, LOG)]).stdout.strip()
    if not re.match(r'^[0-9a-f]{40}$', blob): FAILS.append('%s: logger.ts not readable at %s (UNFETCHED?)' % (lab, rev[:12])); continue
    W = os.path.join(SP, 'g35_logprobe_%s_%s' % (rev[:12], datetime.datetime.now().strftime('%H%M%S%f')[:8])); os.makedirs(W)
    src = run(['git', '--git-dir', CL, 'show', '%s:%s' % (rev, LOG)]).stdout
    if lab == ARM:
        if src.count(ALLOW_OLD) != 1: FAILS.append('%s: the allow-list anchor %r occurs %d time(s), not once' % (lab, ALLOW_OLD, src.count(ALLOW_OLD)))
        src = src.replace(ALLOW_OLD, ALLOW_NEW)
    open(os.path.join(W, 'logger.ts'), 'w').write(src)
    tr = run(['node', '-e', "const ts=require(process.argv[1]);const fs=require('fs');const o=ts.transpileModule(fs.readFileSync('logger.ts','utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2020,esModuleInterop:true}});fs.writeFileSync('logger.js',o.outputText)", os.path.join(NM, 'typescript')], cwd=W)
    open(os.path.join(W, 'probe.js'), 'w').write(PROBE)
    env = dict(os.environ, NODE_ENV='production', NODE_PATH=NM, S35=json.dumps(PROBES)); env.pop('LOG_LEVEL', None)
    r = run(['node', 'probe.js'], cwd=W, env=env)
    sinks = {'stdout': r.stdout}
    for f in ('logs/error.log', 'logs/combined.log'):
        p = os.path.join(W, f); sinks[f] = open(p, encoding='utf-8', errors='replace').read() if os.path.exists(p) else None
    out = {'rev': rev, 'logger_blob': blob, 'transpile_rc': tr.returncode, 'probe_rc': r.returncode, 'stderr': r.stderr[-400:], 'workdir': W, 'hits': {}, 'arm': lab == ARM}
    for sk, t in sinks.items():
        out['hits'][sk] = {pn: sorted(k for k, v in pv.items() if t and v in t) for pn, pv in PROBES.items()}
    out['file_lines'] = {f: (len(sinks[f].splitlines()) if sinks[f] else None) for f in ('logs/error.log', 'logs/combined.log')}
    out['positive_in_combined'] = bool(sinks['logs/combined.log'] and 'S35 POSITIVE' in sinks['logs/combined.log'])
    fk = set()
    for f in ('logs/error.log', 'logs/combined.log'):
        for l in (sinks[f] or '').splitlines():
            try: fk |= set(json.loads(l).keys())
            except Exception: fk.add('<non-JSON line: %s>' % l[:40])
    out['file_keys'] = sorted(fk)
    out['first_file_line'] = (sinks['logs/error.log'] or '').splitlines()[0][:220] if sinks['logs/error.log'] else None
    res[lab] = out
    print('== %s %s | logger.ts blob %s%s | workdir %s | transpile rc %d | probe rc %d%s' % (lab, rev[:12], blob[:12], ' (+ the planted ip arm)' if lab == ARM else '', W, tr.returncode, r.returncode, (' | stderr: ' + r.stderr.strip()[-240:]) if r.stderr.strip() else ''))
    print('   file lines: %s | positive line in combined.log: %s | every key written to a file: %s' % (out['file_lines'], out['positive_in_combined'], out['file_keys']))
    print('   error.log first line: %r' % out['first_file_line'])
    for sk in ('stdout', 'logs/error.log', 'logs/combined.log'):
        print('   %-18s %s' % (sk, ' | '.join('%s %s' % (pn, h or '-') for pn, h in out['hits'][sk].items())))
D, H, E, C, A = (res.get(k) for k, _ in REVS)
ok = bool(D and H and E and C and A)
FILES = ('logs/error.log', 'logs/combined.log')
ctl = {}
if ok:
    ctl['stdout at develop carries every P1 sentinel (the instrument reads stdout)'] = D['hits']['stdout']['P1'] == sorted(P1)
    ctl['#1310 head: BOTH files carry every P2 and P3 sentinel (the instrument sees a file leak, as gate33 measured)'] = all(C['hits'][f]['P2'] == sorted(P2) and C['hits'][f]['P3'] == sorted(P3) for f in FILES)
    ctl['#1321 head: the POSITIVE line is in combined.log (the capture reads the written file)'] = H['positive_in_combined']
    ctl['the planted ip arm: the P3 ip sentinel reaches BOTH files, and at the unplanted head it does not (a one-key widen is visible)'] = all('ip' in A['hits'][f]['P3'] and 'ip' not in H['hits'][f]['P3'] for f in FILES)
    ctl['every probe ran (rc 0) at every revision'] = all(x['probe_rc'] == 0 and x['transpile_rc'] == 0 for x in res.values())
for k, v in ctl.items(): print('CONTROL %s: %s' % (k, v))
ctl_ok = ok and all(ctl.values()) and not FAILS
for f in FAILS: print('FAIL %s' % f)
W_ = {}
if ok:
    def cls_hits(X, sk, c): return {pn: X['hits'][sk][pn] for pn in PROBES if CLASS[pn] == c and X['hits'][sk][pn]}
    W_['head_files'] = {f: cls_hits(H, f, 'VALUE') or 'NONE' for f in FILES}
    W_['end_files'] = {f: cls_hits(E, f, 'VALUE') or 'NONE' for f in FILES}
    W_['head_stdout'] = cls_hits(H, 'stdout', 'VALUE') or 'NONE'
    W_['develop_stdout'] = cls_hits(D, 'stdout', 'VALUE') or 'NONE'
    W_['stdout_new_vs_develop'] = {pn: sorted(set(H['hits']['stdout'][pn]) - set(D['hits']['stdout'][pn])) for pn in PROBES if CLASS[pn] == 'VALUE' and set(H['hits']['stdout'][pn]) - set(D['hits']['stdout'][pn])} or 'NONE'
    W_['head_text_kept'] = {f: {pn: H['hits'][f][pn] == sorted(PROBES[pn]) for pn in PROBES if CLASS[pn] == 'TEXT'} for f in FILES}
    W_['head_residue'] = {f: cls_hits(H, f, 'RESIDUE') or 'NONE' for f in FILES}
    W_['head_loss'] = {f: ('ABSENT (as disclosed)' if not H['hits'][f]['P8'] else 'PRESENT %s' % H['hits'][f]['P8']) for f in FILES}
    W_['head_file_keys'] = H['file_keys']
    W_['develop_file_first_line'] = D['first_file_line']
    print('RESULT (MEASURED by the drafter) VALUE sentinels in a FILE at #1321 head: %s' % W_['head_files'])
    print('RESULT (MEASURED by the drafter) VALUE sentinels in a FILE on END_TREE: %s' % W_['end_files'])
    print('RESULT (MEASURED by the drafter) the message and the string error text in BOTH files at #1321 head (TEXT, want all True): %s' % W_['head_text_kept'])
    print('RESULT (MEASURED by the drafter) the disclosed LOSS (userId / documentId / ip / stack) in the files at #1321 head: %s' % W_['head_loss'])
    print('RESULT (MEASURED by the drafter) RESIDUE in the files at #1321 head (allow-listed strings, by design): %s' % W_['head_residue'])
    print('RESULT (MEASURED by the drafter) every key any line of either file carries at #1321 head: %s' % W_['head_file_keys'])
    print('RESULT (MEASURED by the drafter) VALUE sentinels on STDOUT at #1321 head: %s — at develop: %s — NEW at the head vs develop: %s' % (W_['head_stdout'], W_['develop_stdout'], W_['stdout_new_vs_develop']))
res['_controls'] = ctl; res['_fails'] = FAILS; res['_probes'] = {pn: sorted(pv) for pn, pv in PROBES.items()}; res['_classes'] = CLASS; res['_widen'] = W_
json.dump(res, open(os.path.join(GS, 'logprobe_gate35.json'), 'w'), indent=1)
print('SUMMARY logprobe_gate35: controls %s (%d of %d) | fails %d' % ('PASS' if ctl_ok else 'FAIL', sum(ctl.values()), len(ctl), len(FAILS)))
sys.exit(0 if ctl_ok else 1)
