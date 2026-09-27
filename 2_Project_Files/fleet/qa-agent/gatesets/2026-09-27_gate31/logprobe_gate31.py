#!/usr/bin/env python3
"""logprobe_gate31.py <scratchpad> — the DRAFTER's #1302 (KS-1348) measurement: WHAT REACHES THE PRODUCTION LOG FILES, at the merge-base (develop) and at
#1302's head. Instrument: originate's REAL utils/logger.ts read from the scratch clone at each commit (`git show`), transpiled to CommonJS with the
checkout's OWN typescript (transpileModule, READ from node_modules), run by node with NODE_ENV=production and the checkout's OWN winston (NODE_PATH, a READ
of node_modules) in a FRESH scratch cwd per commit (the File transports write logs/error.log and logs/combined.log relative to cwd — only there). It logs
one metadata object carrying secret- and PII-looking fields (password, token, apiKey, email, a nested subject.ssn, a Bearer header), each a unique
sentinel, through logger.error and logger.info, waits for the file streams to finish, then counts every sentinel in each file AND on stdout (the
Console transport, JSON in production). CONTROLS: stdout must carry every sentinel at BOTH commits (the instrument sees what the logger emits); a
sentinel-free message must appear in a head file line (a positive: the capture reads the file the transport wrote); the develop file line is printed
verbatim. Nothing is written outside <scratchpad>/g31_logprobe_*; nothing in the checkout is written (typescript and winston are only require()d)."""
import json, os, subprocess, sys, datetime, shutil
SP = sys.argv[1]
CL = os.path.join(SP, 'g31_sp', 'clone.git')
NM = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/node_modules'
LOG = 'Blockchain/Dev/services/originate/src/utils/logger.ts'
REVS = [('develop (merge-base)', 'refs/g31/develop'), ('#1302 head', 'refs/g31/pull/1302')]
S = {'password': 'S31PW-hunter2-q7', 'token': 'S31TOK-eyJhbGciOi-q7', 'apiKey': 'S31KEY-sk_live_q7', 'email': 's31.subject@example.test', 'ssn': 'S31SSN-123-45-6789', 'authorization': 'Bearer S31BEARER-q7'}
PROBE = r"""
const { logger } = require('./logger.js');
const S = JSON.parse(process.env.S31);
logger.info('S31 POSITIVE a plain line with no secret');
logger.error('S31 CONTEXT fail500-shaped', { error: 'thrown text S31-ERRTEXT', password: S.password, token: S.token, apiKey: S.apiKey, email: S.email, subject: { ssn: S.ssn }, headers: { authorization: S.authorization } });
logger.info('S31 INFO with metadata', { user: { email: S.email, password: S.password } });
let open = logger.transports.filter(t => t.filename).length;
if (!open) setTimeout(() => process.exit(0), 300);
logger.on('finish', () => setTimeout(() => process.exit(0), 300));
logger.end();
setTimeout(() => process.exit(3), 8000);
"""
def run(cmd, **kw): return subprocess.run(cmd, capture_output=True, text=True, **kw)
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
ts = json.load(open(os.path.join(NM, 'typescript', 'package.json')))['version']; wv = json.load(open(os.path.join(NM, 'winston', 'package.json')))['version']
print('logprobe_gate31 %s | node %s | typescript %s | winston %s (both READ from %s)' % (now, run(['node', '--version']).stdout.strip(), ts, wv, NM))
res = {}
for lab, rev in REVS:
    sha = run(['git', '--git-dir', CL, 'rev-parse', rev]).stdout.strip()
    src = run(['git', '--git-dir', CL, 'show', '%s:%s' % (rev, LOG)]).stdout
    blob = run(['git', '--git-dir', CL, 'rev-parse', '%s:%s' % (rev, LOG)]).stdout.strip()
    W = os.path.join(SP, 'g31_logprobe_%s_%s' % (sha[:12], datetime.datetime.now().strftime('%H%M%S'))); os.makedirs(W)
    open(os.path.join(W, 'logger.ts'), 'w').write(src)
    tr = run(['node', '-e', "const ts=require(process.argv[1]);const fs=require('fs');const o=ts.transpileModule(fs.readFileSync('logger.ts','utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2020,esModuleInterop:true}});fs.writeFileSync('logger.js',o.outputText)", os.path.join(NM, 'typescript')], cwd=W)
    open(os.path.join(W, 'probe.js'), 'w').write(PROBE)
    env = dict(os.environ, NODE_ENV='production', NODE_PATH=NM, S31=json.dumps(S)); env.pop('LOG_LEVEL', None)
    r = run(['node', 'probe.js'], cwd=W, env=env)
    out = {'commit': sha, 'logger_blob': blob, 'transpile_rc': tr.returncode, 'probe_rc': r.returncode, 'stderr': r.stderr[-400:], 'files': {}}
    out['stdout_sentinels'] = sorted(k for k, v in S.items() if v in r.stdout)
    for f in ('logs/error.log', 'logs/combined.log'):
        p = os.path.join(W, f)
        t = open(p, encoding='utf-8', errors='replace').read() if os.path.exists(p) else None
        out['files'][f] = {'exists': t is not None, 'lines': len(t.splitlines()) if t else 0, 'sentinels': sorted(k for k, v in S.items() if t and v in t),
                           'positive_line_seen': bool(t and 'S31 POSITIVE' in t), 'errtext_seen': bool(t and 'S31-ERRTEXT' in t), 'first_line': (t.splitlines()[0][:300] if t else None)}
    res[lab] = out
    print('== %s %s (logger.ts blob %s) workdir %s | transpile rc %d | probe rc %d%s' % (lab, sha[:12], blob[:12], W, tr.returncode, r.returncode, (' | stderr: ' + r.stderr.strip()[-300:]) if r.stderr.strip() else ''))
    print('   stdout (Console transport, JSON in production) sentinels: %s of %d' % (out['stdout_sentinels'], len(S)))
    for f, v in out['files'].items():
        print('   %s: exists %s, %d line(s), sentinels %s of %d, the thrown-text line seen %s, the positive line seen %s | first line: %r' % (f, v['exists'], v['lines'], v['sentinels'], len(S), v['errtext_seen'], v['positive_line_seen'], v['first_line']))
d, h = res['develop (merge-base)'], res['#1302 head']
newf = {f: sorted(set(h['files'][f]['sentinels']) - set(d['files'][f]['sentinels'])) for f in h['files']}
ctl_ok = len(d['stdout_sentinels']) == len(S) and len(h['stdout_sentinels']) == len(S) and h['files']['logs/combined.log']['positive_line_seen']
print('CONTROLS: stdout carries every sentinel at both commits AND the head combined.log carries the positive line: %s' % ctl_ok)
print('RESULT (MEASURED by the drafter): sentinels that reach a production log FILE at #1302 head and did NOT at develop: %s' % newf)
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logprobe_gate31.json'), 'w'), indent=1)
sys.exit(0 if ctl_ok else 1)
