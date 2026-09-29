#!/usr/bin/env python3
"""installprobe_gate42.py <scratchpad> — the drafter's MEASURED install probe for gate42 (#1339 KS-1378), run AFTER predict_gate42.py (it reads the
pins beside it: develop and #1339's head). For services/auth and services/originate, at the BASE (the pinned develop) and at the HEAD: the service's
package.json + package-lock.json are read from the scratch clone (`git show`, never the checkout's working tree) into <scratchpad>/g42/ip/<side>_<svc>/
and installed with a STANDALONE `npm ci --ignore-scripts --no-audit --no-fund` (the service Dockerfile's own install line; the npm cache is kept in
the scratchpad) — a CLEAN install from the lock, never an incremental one. Then installprobe_gate42.cjs runs inside each install: the RESOLVED
nodemailer / morgan / @types/nodemailer versions (require.resolve from the install dir), nodemailer.createTransport with the call site's SMTP option
SHAPE (never connected), sendMail through streamTransport with the call site's message shape (built, not sent), and morgan 'combined' on a 127.0.0.1
port-0 server with a CONTROL request and a PLANTED double quote in User-Agent. CONTROLS (each must hold or the probe says CONTROLS FAIL): the BASE
installs resolve nodemailer 9.1.1 and log the planted quote RAW (the instrument CAN see the unescaped form — the log-injection the advisory names);
the HEAD installs resolve nodemailer 10.x >= 10.0.2 and escape it. Writes installprobe_gate42.json beside this script; install trees stay in the
scratchpad. This is NOT the monorepo root install the suites run from (the gate owes that: `npm ci` at Blockchain/Dev and require.resolve from
each service dir). Usage: installprobe_gate42.py <scratchpad dir under /private/tmp/claude-501/>"""
import json, os, re, subprocess, sys, datetime
GS = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(GS, 'kit.json'), encoding='utf-8'))
SP = sys.argv[1] if len(sys.argv) > 1 else ''
if not re.match(r'^/private/tmp/claude-501/.*/scratchpad', SP) or not os.path.isdir(SP): print('usage: installprobe_gate42.py <scratchpad>'); sys.exit(9)
P = json.load(open(os.path.join(GS, 'pins_%s.json' % K['kit']), encoding='utf-8'))
if P.get('fail') != 0 or P.get('simulation') != 'none': print('REFUSING: the pins are not a passing real run'); sys.exit(1)
CL = os.path.join(SP, 'g42_sp', 'clone.git'); IP = os.path.join(SP, 'g42', 'ip'); os.makedirs(IP, exist_ok=True)
n = sorted(K['prs'])[0]; SIDES = {'base': P['develop'], 'head': P['prs'][n]['head']}
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def sh(cmd, **kw): return subprocess.run(cmd, capture_output=True, text=True, **kw)
npmv, nodev = sh(['npm', '--version']).stdout.strip(), sh(['node', '--version']).stdout.strip()
print('installprobe_gate42 %s | npm %s node %s | base %s head %s | installs under %s' % (now(), npmv, nodev, SIDES['base'][:12], SIDES['head'][:12], IP))
res = {'measured_at': now(), 'npm': npmv, 'node': nodev, 'sides': SIDES, 'runs': {}}
for side, c in SIDES.items():
    for svc in ('auth', 'originate'):
        d = os.path.join(IP, '%s_%s' % (side, svc)); key = '%s_%s' % (side, svc)
        if os.path.exists(os.path.join(d, 'node_modules')):   # never rm: a previous install is moved aside, and a fresh dir is built
            k = 1
            while os.path.exists('%s.prev%d' % (d, k)): k += 1
            os.rename(d, '%s.prev%d' % (d, k))
        os.makedirs(d, exist_ok=True)
        for f in ('package.json', 'package-lock.json'):
            r = sh(['git', '--git-dir', CL, 'show', '%s:Blockchain/Dev/services/%s/%s' % (c, svc, f)])
            assert r.returncode == 0, r.stderr
            open(os.path.join(d, f), 'w', encoding='utf-8').write(r.stdout)
        t0 = now(); r = sh(['npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund', '--cache', os.path.join(SP, 'g42', 'npmcache'), '--prefix', d])
        open(d + '.ci.out', 'w').write(r.stdout); open(d + '.ci.err', 'w').write(r.stderr)
        q = sh(['node', os.path.join(GS, 'installprobe_gate42.cjs'), d])
        try: pr = json.loads(q.stdout.strip().splitlines()[-1])
        except Exception: pr = {'probe_error': (q.stdout + q.stderr)[-400:]}
        res['runs'][key] = {'npm_ci_rc': r.returncode, 'npm_ci_start': t0, 'npm_ci_end': now(), 'npm_ci_tail': [l for l in r.stdout.splitlines() if l.strip()][-1:], 'probe_rc': q.returncode, 'probe': pr}
        print('  %s: npm ci rc %d (%s) | probe rc %d | %s' % (key, r.returncode, res['runs'][key]['npm_ci_tail'], q.returncode, json.dumps({k: v for k, v in pr.items() if k != 'morgan_combined'})[:600]))
        if pr.get('morgan_combined'): print('    morgan combined lines: %s' % pr['morgan_combined']['lines'])
def vt(v): return tuple(int(x) for x in re.findall(r'\d+', v or '0')[:3])
R = res['runs']
def g(k, *p):
    x = R.get(k, {}).get('probe')
    for q in p: x = (x or {}).get(q) if isinstance(x, dict) or x is None else None
    return x
CT = {
 'CT1 every clean install rc 0': all(v['npm_ci_rc'] == 0 and v['probe_rc'] == 0 for v in R.values()),
 'CT2 BASE resolves nodemailer 9.1.1 (the instrument sees the OLD major)': all(g('base_%s' % s, 'nodemailer', 'version') == '9.1.1' for s in ('auth', 'originate')),
 'CT3 HEAD resolves nodemailer 10.x >= 10.0.2 (the bump is what RUNS in a clean install)': all(vt(g('head_%s' % s, 'nodemailer', 'version')) >= (10, 0, 2) and vt(g('head_%s' % s, 'nodemailer', 'version'))[0] == 10 for s in ('auth', 'originate')),
 'CT4 morgan combined: the control line logs on both sides': bool(g('base_auth', 'morgan_combined', 'control_logs')) and bool(g('head_auth', 'morgan_combined', 'control_logs')),
 'CT5 BASE morgan logs the planted quote RAW (the instrument CAN see the injection)': g('base_auth', 'morgan_combined', 'planted_raw_present') is True and g('base_auth', 'morgan_combined', 'planted_quote_escaped') is False,
 'CT6 the call-site shapes build on BOTH majors (createTransport SMTP shape + sendMail via streamTransport)': all(g(k, 'sendMail', 'ok') is True and g(k, 'smtp_transport', 'name') == 'SMTP' for k in R),
}
res['controls'] = CT
res['_summary'] = {k: {'nodemailer': g(k, 'nodemailer', 'version'), 'nodemailer_entry': g(k, 'nodemailer', 'resolved'), 'morgan': g(k, 'morgan', 'version'), '@types/nodemailer': g(k, 'types_nodemailer'),
                       'sendMail_ok': g(k, 'sendMail', 'ok'), 'morgan_planted_quote_escaped': g(k, 'morgan_combined', 'planted_quote_escaped')} for k in sorted(R)}
json.dump(res, open(os.path.join(GS, 'installprobe_gate42.json'), 'w'), indent=1)
for k, v in CT.items(): print('  %s %s' % ('PASS' if v else 'FAIL', k))
print('SUMMARY %s' % json.dumps(res['_summary']))
print('installprobe_gate42: CONTROLS %s -> installprobe_gate42.json' % ('ALL PASS' if all(CT.values()) else 'FAIL'))
sys.exit(0 if all(CT.values()) else 1)
