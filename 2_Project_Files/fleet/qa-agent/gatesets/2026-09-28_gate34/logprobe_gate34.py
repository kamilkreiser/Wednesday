#!/usr/bin/env python3
"""logprobe_gate34.py <scratchpad> — the DRAFTER's WIDEN measurement for gate34's two logging rows (#1316 KS-1346 C adminConfig.ts, #1317 KS-1346 D
webhooks.ts): CAN ANY SECRET OR PII VALUE REACH ANY LOG SINK FROM THE fail500 PATHS, in production mode, through the REAL logger? Shape copied from
gate33's logprobe (gate31 lineage: the REAL logger transpiled by the checkout's own typescript, run by node with the checkout's own winston), re-keyed
for gate34 and re-aimed at the fail500 helpers (gate33 found the widen class in #1310: a path the ruling did not name reached the production files).

Instrument: originate's REAL utils/logger.ts read from the scratch clone (`git show <rev>:<path>`), transpiled to CommonJS with the checkout's OWN
typescript (transpileModule, READ from node_modules), run by node with NODE_ENV=production and the checkout's OWN winston (NODE_PATH, a READ of
node_modules) in a FRESH scratch cwd per revision (the File transports write logs/error.log and logs/combined.log relative to cwd). The fail500 LOG
EXPRESSION of routes/adminConfig.ts (AC) and routes/webhooks.ts (WH) is read at the SAME revision (the ONE line after `function fail500(`, asserted
byte-unique as a whole line) and evaluated as JavaScript with that logger — the ruled line measured through the real logger and its real sinks, not a mock.
Revisions (label: routes from / logger from): develop (the pin) / develop; #1316 head / #1316 head; #1317 head / #1317 head; END_TREE / END_TREE
(pins_gate34.json); END_TREE + #1310 logger / END_TREE routes with the OPEN #1310's logger.ts (KS-1348 redact-then-JSON, gate33's logger row, NOT in
this kit — measured because it would make the File transports write JSON: the files then carry what the Console carries). #1310's head is fetched by
predict_gate34.py's in-flight census (refs/g34/pull/1310).

PROBES — every sentinel is suffixed with its route (-AC / -WH) so every hit is attributable to one path; each probe is classed:
  VALUE (must reach NO sink at a head, under the ruling "Type and field names only"):
    V1 a thrown plain object carrying password / token / apiKey / authorization / secret VALUES;
    V2 a class instance whose toString() returns a secret (develop's `String(err)` CALLS it — the control that the instrument sees a leak) + a field value;
    V3 a Prisma-shaped plain object (code, meta.target, meta.params = a ciphertext, a `message` FIELD) — a non-Error: names only;
    V4 an Error whose ENUMERABLE props carry an axios-shaped config.headers.Authorization (an Error logs its message only);
    V5 an Array of secrets; V6 a null-prototype object with a secret value; V7 an ENUMERABLE GETTER returning a secret (Object.keys never calls it);
    R1v the VALUE of an email-keyed object.
  RULED RESIDUE (Kam's ruling keeps it; reported, never graded a defect of these PRs): R1n the field NAME that is itself PII (an email used as a key;
    gate33's F-2 "field names as data"); R2 an Error whose MESSAGE carries an email and a token (an Error logs exactly its message); R3 a thrown STRING
    carrying a bearer (a string logs exactly itself).
  EDGE (the ruling does not name it; measured and reported for the gate to rule): E1 an object whose PROTOTYPE carries `constructor.name` = data (the
    TYPE NAME the line prints is attacker-shaped); E2 a Proxy whose ownKeys trap throws — Object.keys runs INSIDE the log call, so the helper itself
    throws before res.status(500) (recorded as `threw`).
CONTROLS: (1) develop: V2's toString sentinel reaches stdout for BOTH routes (the old `String(err)` line leaks it — the instrument sees a stdout leak);
(2) END_TREE + #1310 logger: R3's sentinel reaches BOTH files for both routes (the instrument sees a FILE leak); (3) the sentinel-free POSITIVE line
reaches combined.log under #1310's logger (the capture reads the written file); (4) every probe ran (rc 0) at every revision; (5) the fail500 line at
#1316's head (AC), #1317's head (WH) and END_TREE (both) IS the ruled line, and at develop is the `String(err)` line.
Nothing is written outside <scratchpad>/g34_logprobe_*; nothing in the checkout is written."""
import json, os, re, subprocess, sys, datetime
SP = sys.argv[1] if len(sys.argv) > 1 else ''
if not re.match(r'^/private/tmp/claude-501/.*/scratchpad', SP) or not os.path.isdir(SP): print('usage: logprobe_gate34.py <scratchpad>'); sys.exit(9)
GS = os.path.dirname(os.path.abspath(__file__))
CL = os.path.join(SP, 'g34_sp', 'clone.git')
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
NM = CHECKOUT + '/Blockchain/Dev/node_modules'
O = 'Blockchain/Dev/services/originate/src/'
LOG, AC, WH = O + 'utils/logger.ts', O + 'routes/adminConfig.ts', O + 'routes/webhooks.ts'
PINS = json.load(open(os.path.join(GS, 'pins_gate34.json'), encoding='utf-8'))
RULED = "logger.error(context, { error: err instanceof Error ? err.message : typeof err === 'string' ? err : typeof err === 'object' && err !== null ? 'thrown ' + (Object.getPrototypeOf(err)?.constructor?.name ?? 'object') + ' with fields [' + Object.keys(err).join(', ') + ']' : 'thrown ' + typeof err });"
OLD = "logger.error(context, { error: err instanceof Error ? err.message : String(err) });"
def run(cmd, **kw): return subprocess.run(cmd, capture_output=True, text=True, **kw)
def rp(ref): return run(['git', '--git-dir', CL, 'rev-parse', '--verify', '-q', ref]).stdout.strip()
H1310 = rp('refs/g34/pull/1310^{commit}')
REVS = [('develop (the pin)', PINS['develop'], PINS['develop']),
        ('#1316 head', PINS['prs']['1316']['head'], PINS['prs']['1316']['head']),
        ('#1317 head', PINS['prs']['1317']['head'], PINS['prs']['1317']['head']),
        ('END_TREE', PINS['end_tree'], PINS['end_tree']),
        ('END_TREE + #1310 logger', PINS['end_tree'], H1310)]
CLASSES = {'VALUE': ['V1 password', 'V1 token', 'V1 apiKey', 'V1 authorization', 'V1 secret', 'V2 toString()', 'V2 field', 'V3 meta.params', 'V3 message FIELD',
                     'V4 Error.config.headers.Authorization', 'V5 array[0]', 'V5 array[1]', 'V6 null-proto value', 'V7 enumerable getter', 'R1v email-keyed VALUE'],
           'RESIDUE': ['R1n field NAME (an email)', 'R2 Error.message email', 'R2 Error.message token', 'R3 thrown string'],
           'EDGE': ['E1 prototype constructor.name', 'E2 Proxy ownKeys trap text']}
def sentinels(r):
    s = {'V1 password': 'S34V1PW', 'V1 token': 'S34V1TOK', 'V1 apiKey': 'S34V1KEY', 'V1 authorization': 'S34V1BEARER', 'V1 secret': 'S34V1SECRET',
         'V2 toString()': 'S34V2TOSTRING', 'V2 field': 'S34V2FIELD', 'V3 meta.params': 'S34V3CIPHER', 'V3 message FIELD': 'S34V3MSGFIELD',
         'V4 Error.config.headers.Authorization': 'S34V4AXIOSAUTH', 'V5 array[0]': 'S34V5ARRA', 'V5 array[1]': 'S34V5ARRB', 'V6 null-proto value': 'S34V6NULLPROTO',
         'V7 enumerable getter': 'S34V7GETTER', 'R1v email-keyed VALUE': 'S34R1VAL', 'R1n field NAME (an email)': 's34.r1key', 'R2 Error.message email': 's34.r2msg',
         'R2 Error.message token': 'S34R2TOK', 'R3 thrown string': 'S34R3BEARER', 'E1 prototype constructor.name': 'S34E1CTOR', 'E2 Proxy ownKeys trap text': 'S34E2TRAP'}
    return {k: '%s-%s' % (v, r) for k, v in s.items()}
PROBES = {'%s %s' % (r, k): v for r in ('AC', 'WH') for k, v in sentinels(r).items()}
PROBE = r"""
const { logger } = require('./logger.js');
const S = JSON.parse(process.env.S34);
const F = { AC: require('./fail500_AC.js'), WH: require('./fail500_WH.js') };
const threw = {};
logger.info('S34 POSITIVE a plain line with no secret');
for (const r of ['AC', 'WH']) {
  const s = (k) => S[r + ' ' + k];
  const call = (tag, err) => { try { F[r](logger, 'S34 ' + r + ' ' + tag, err); threw[r + ' ' + tag] = false; } catch (e) { threw[r + ' ' + tag] = String(e && e.message); } };
  call('V1', { password: s('V1 password'), token: s('V1 token'), apiKey: s('V1 apiKey'), authorization: 'Bearer ' + s('V1 authorization'), secret: s('V1 secret') });
  class Leaky { constructor() { this.field = s('V2 field'); } toString() { return s('V2 toString()'); } }
  call('V2', new Leaky());
  call('V3', { code: 'P2002', clientVersion: '5.x', message: s('V3 message FIELD'), meta: { target: ['email'], params: s('V3 meta.params') } });
  const e4 = new Error('S34 V4 benign message ' + r); e4.config = { headers: { Authorization: 'Bearer ' + s('V4 Error.config.headers.Authorization') } }; call('V4', e4);
  call('V5', [s('V5 array[0]'), s('V5 array[1]')]);
  const o6 = Object.create(null); o6.secret = s('V6 null-proto value'); call('V6', o6);
  const o7 = {}; Object.defineProperty(o7, 'sessionToken', { enumerable: true, get() { return s('V7 enumerable getter'); } }); call('V7', o7);
  const o1 = {}; o1[s('R1n field NAME (an email)') + '@example.test'] = s('R1v email-keyed VALUE'); call('R1', o1);
  call('R2', new Error('login failed for ' + s('R2 Error.message email') + '@example.test with token ' + s('R2 Error.message token')));
  call('R3', 'upstream said: Bearer ' + s('R3 thrown string'));
  const o8 = Object.create({ constructor: { name: s('E1 prototype constructor.name') } }); o8.x = 1; call('E1', o8);
  call('E2', new Proxy({}, { ownKeys() { throw new Error(s('E2 Proxy ownKeys trap text')); } }));
}
require('fs').writeFileSync('threw.json', JSON.stringify(threw));
logger.on('finish', () => setTimeout(() => process.exit(0), 400));
logger.end();
setTimeout(() => process.exit(3), 9000);
"""
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
ts = json.load(open(os.path.join(NM, 'typescript', 'package.json')))['version']; wv = json.load(open(os.path.join(NM, 'winston', 'package.json')))['version']
lf = json.load(open(os.path.join(NM, 'logform', 'package.json')))['version'] if os.path.exists(os.path.join(NM, 'logform', 'package.json')) else '?'
print('logprobe_gate34 %s | node %s | typescript %s | winston %s | logform %s (READ from %s) | #1310 head %s' % (now, run(['node', '--version']).stdout.strip(), ts, wv, lf, NM, H1310 or 'NOT FETCHED'))
def fail500_js(rev, path):
    src = run(['git', '--git-dir', CL, 'show', '%s:%s' % (rev, path)]).stdout.split('\n')
    i = [k for k, l in enumerate(src) if l.startswith('function fail500(')]
    if len(i) != 1: return None, 'fail500 declared %d time(s)' % len(i)
    line = src[i[0] + 1]
    if sum(1 for l in src if l == line) != 1 or 'logger.error(context,' not in line: return None, 'the fail500 log line is not byte-unique / not a logger.error(context, …) line: %r' % line[:120]
    return 'module.exports = function (logger, context, err) {\n' + line + '\n};\n', line.strip()
res, FAILS = {}, []
for lab, rrev, lrev in REVS:
    if not re.match(r'^[0-9a-f]{40}$', rrev or '') or not re.match(r'^[0-9a-f]{40}$', lrev or ''): FAILS.append('%s: no revision (%r / %r)' % (lab, rrev, lrev)); continue
    blob = rp('%s:%s' % (lrev, LOG))
    if not re.match(r'^[0-9a-f]{40}$', blob): FAILS.append('%s: logger.ts not readable at %s (UNFETCHED?)' % (lab, lrev[:12])); continue
    W = os.path.join(SP, 'g34_logprobe_%s_%s' % (rrev[:12], datetime.datetime.now().strftime('%H%M%S%f')[:8])); os.makedirs(W)
    open(os.path.join(W, 'logger.ts'), 'w').write(run(['git', '--git-dir', CL, 'show', '%s:%s' % (lrev, LOG)]).stdout)
    lines = {}
    for nm, pth in (('AC', AC), ('WH', WH)):
        js, line = fail500_js(rrev, pth)
        if js is None: FAILS.append('%s: %s %s' % (lab, nm, line)); js = 'module.exports = function () { throw new Error("no fail500 line"); };\n'
        open(os.path.join(W, 'fail500_%s.js' % nm), 'w').write(js); lines[nm] = line
    tr = run(['node', '-e', "const ts=require(process.argv[1]);const fs=require('fs');const o=ts.transpileModule(fs.readFileSync('logger.ts','utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2020,esModuleInterop:true}});fs.writeFileSync('logger.js',o.outputText)", os.path.join(NM, 'typescript')], cwd=W)
    open(os.path.join(W, 'probe.js'), 'w').write(PROBE)
    env = dict(os.environ, NODE_ENV='production', NODE_PATH=NM, S34=json.dumps(PROBES)); env.pop('LOG_LEVEL', None)
    r = run(['node', 'probe.js'], cwd=W, env=env)
    sinks = {'stdout': r.stdout}
    for f in ('logs/error.log', 'logs/combined.log'):
        p = os.path.join(W, f); sinks[f] = open(p, encoding='utf-8', errors='replace').read() if os.path.exists(p) else None
    thr = json.load(open(os.path.join(W, 'threw.json'))) if os.path.exists(os.path.join(W, 'threw.json')) else {}
    out = {'routes_rev': rrev, 'logger_rev': lrev, 'logger_blob': blob, 'fail500_lines': lines, 'transpile_rc': tr.returncode, 'probe_rc': r.returncode, 'stderr': r.stderr[-400:], 'workdir': W,
           'threw': {k: v for k, v in thr.items() if v}, 'hits': {}}
    for sk, t in sinks.items():
        out['hits'][sk] = sorted(k for k, v in PROBES.items() if t and v in t)
    out['file_lines'] = {f: (len(sinks[f].splitlines()) if sinks[f] else None) for f in ('logs/error.log', 'logs/combined.log')}
    out['positive_in_combined'] = bool(sinks['logs/combined.log'] and 'S34 POSITIVE' in sinks['logs/combined.log'])
    out['first_file_line'] = (sinks['logs/error.log'] or '').splitlines()[0][:200] if sinks['logs/error.log'] else None
    out['sample_stdout_lines'] = [l[:260] for l in r.stdout.splitlines() if 'S34 AC V1' in l or 'S34 AC R1' in l or 'S34 AC E1' in l][:3]
    res[lab] = out
    print('== %s | routes %s | logger %s (blob %s) | workdir %s | transpile rc %d | probe rc %d%s' % (lab, rrev[:12], lrev[:12], blob[:12], W, tr.returncode, r.returncode, (' | stderr: ' + r.stderr.strip()[-240:]) if r.stderr.strip() else ''))
    for nm in ('AC', 'WH'): print('   fail500 log line (%s): %s' % (nm, lines.get(nm, '?')[:200]))
    print('   file lines: %s | positive line in combined.log: %s | error.log first line: %r' % (out['file_lines'], out['positive_in_combined'], out['first_file_line']))
    print('   the helper THREW (Object.keys inside the log call): %s' % (out['threw'] or 'NONE'))
    for l in out['sample_stdout_lines']: print('   stdout sample: %s' % l)
    for sk in ('stdout', 'logs/error.log', 'logs/combined.log'):
        by = {c: sorted(k for k in out['hits'][sk] if k.split(' ', 1)[1] in CLASSES[c]) for c in CLASSES}
        print('   %-18s VALUE %s | RESIDUE %s | EDGE %s' % (sk, by['VALUE'] or '-', by['RESIDUE'] or '-', by['EDGE'] or '-'))
D = res.get('develop (the pin)'); X = res.get('END_TREE + #1310 logger')
ok = len(res) == len(REVS)
ctl = {}
if ok:
    ctl['develop: V2 toString() reaches stdout for AC and WH (the old String(err) line; the instrument sees a stdout leak)'] = all(('%s V2 toString()' % r) in D['hits']['stdout'] for r in ('AC', 'WH'))
    ctl['END_TREE + #1310 logger: R3 reaches BOTH files for AC and WH (the instrument sees a FILE leak)'] = all(('%s R3 thrown string' % r) in X['hits'][f] for r in ('AC', 'WH') for f in ('logs/error.log', 'logs/combined.log'))
    ctl['END_TREE + #1310 logger: the POSITIVE line is in combined.log (the capture reads the written file)'] = X['positive_in_combined']
    ctl['every probe ran (rc 0) at every revision'] = all(x['probe_rc'] == 0 and x['transpile_rc'] == 0 for x in res.values())
    ctl['the fail500 line is the RULED line at #1316 head (AC), #1317 head (WH) and END_TREE (both), and the String(err) line at develop'] = (
        res['#1316 head']['fail500_lines']['AC'] == RULED and res['#1317 head']['fail500_lines']['WH'] == RULED and all(res['END_TREE']['fail500_lines'][k] == RULED for k in ('AC', 'WH'))
        and all(D['fail500_lines'][k] == OLD for k in ('AC', 'WH')))
for k, v in ctl.items(): print('CONTROL %s: %s' % (k, v))
ctl_ok = ok and all(ctl.values()) and not FAILS
for f in FAILS: print('FAIL %s' % f)
VH, RF, EH = {}, {}, {}
if ok:
    for lab, X_ in res.items():
        routes = ('AC',) if lab == '#1316 head' else ('WH',) if lab == '#1317 head' else ('AC', 'WH') if lab != 'develop (the pin)' else ('AC', 'WH')
        VH[lab] = {sk: sorted(k for k in X_['hits'][sk] if k.split(' ', 1)[0] in routes and k.split(' ', 1)[1] in CLASSES['VALUE']) for sk in X_['hits']}
        RF[lab] = {f: sorted(k for k in X_['hits'][f] if k.split(' ', 1)[0] in routes and k.split(' ', 1)[1] in CLASSES['RESIDUE']) for f in ('logs/error.log', 'logs/combined.log')}
        EH[lab] = {sk: sorted(k for k in X_['hits'][sk] if k.split(' ', 1)[0] in routes and k.split(' ', 1)[1] in CLASSES['EDGE']) for sk in X_['hits']}
        print('RESULT (MEASURED by the drafter) %-26s VALUE sentinels on ANY sink (the PR\'s own route(s) %s): %s' % (lab, list(routes), {k: v for k, v in VH[lab].items() if v} or 'NONE'))
        print('RESULT (MEASURED by the drafter) %-26s RULED RESIDUE in a FILE: %s | EDGE on any sink: %s | helper threw: %s' % (lab, {k: v for k, v in RF[lab].items() if v} or 'NONE', {k: v for k, v in EH[lab].items() if v} or 'NONE', X_['threw'] or 'NONE'))
res['_controls'] = ctl; res['_fails'] = FAILS; res['_probes'] = sorted(PROBES); res['_classes'] = CLASSES
res['_value_hits'] = {k: {s: v for s, v in d.items() if v} or 'NONE' for k, d in VH.items()}
res['_residue_in_files'] = {k: {s: v for s, v in d.items() if v} or 'NONE' for k, d in RF.items()}
res['_edge_hits'] = {k: {s: v for s, v in d.items() if v} or 'NONE' for k, d in EH.items()}
json.dump(res, open(os.path.join(GS, 'logprobe_gate34.json'), 'w'), indent=1)
print('SUMMARY logprobe_gate34: controls %s (%d of %d) | fails %d' % ('PASS' if ctl_ok else 'FAIL', sum(ctl.values()), len(ctl), len(FAILS)))
sys.exit(0 if ctl_ok else 1)
