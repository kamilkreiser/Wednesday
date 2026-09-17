#!/usr/bin/env python3
"""drafter_run.py — #1020 (KS-769 fuse re-date) drafter measurements. Clone --shared by SHA into a fresh mktemp -d in the drafting
scratchpad; two worktrees IN THE CLONE: base = d7e95cd9f (the PR parent = develop at draft time), head = 71bd80a35. Write verbs only inside
the clone. Never rm. Reads of the Secuura checkout: status/config/for-each-ref/.git/worktrees only.
Sections: A readings + setup · B static diff · C suites per tree · D clock unit probe · E clock whole-suite · F tampers on head ·
G fuse census (audit-baseline dated rows under an injected clock) · H readings at close."""
import subprocess, os, re, sys, json, tempfile, datetime, hashlib, glob

SCR = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/a5010d5c-6deb-4514-91ed-aa504c76f373/scratchpad'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1020'
OUT = GS + '/out'
H = '71bd80a35b406b9c99c7b96955a7521032d33c20'
B = 'd7e95cd9f153e9036ed77935a73c93504fa6e3dc'
LD = 'Blockchain/Dev/scripts/audit/lock-discovery.mjs'
FAKE = 'file://' + GS + '/fakeclock.mjs'
ONLY = set(sys.argv[1:])  # optional section letters

def ts(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def want(sec): return not ONLY or sec in ONLY
def env_for(fake=None):
    e = dict(os.environ)
    for k in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_COMMON_DIR', 'NODE_OPTIONS', 'QA_FAKE_NOW', 'QA_FAKE_ANNOUNCE', 'NODE_ENV'):
        e.pop(k, None)
    if fake:
        e['NODE_OPTIONS'] = '--import=' + FAKE; e['QA_FAKE_NOW'] = fake
    return e
def run(cmd, cwd=None, fake=None, label=None, timeout=900):
    t0 = datetime.datetime.now()
    p = subprocess.run(cmd, cwd=cwd, env=env_for(fake), capture_output=True, text=True, timeout=timeout)
    dt = (datetime.datetime.now() - t0).total_seconds()
    if label:
        open(OUT + '/' + label + '.out', 'w').write('$ %s\n# cwd %s fake %s rc %d secs %.1f\n--- stdout\n%s\n--- stderr\n%s' % (' '.join(cmd), cwd, fake, p.returncode, dt, p.stdout, p.stderr))
    return p.returncode, p.stdout, p.stderr, dt
def readings(tag):
    rc, o, e, _ = run(['git', '-C', REPO, '--no-optional-locks', 'status', '--porcelain'])
    por = len([l for l in o.splitlines() if l.strip()])
    rc2, o2, e2, _ = run(['git', '-C', REPO, 'for-each-ref'])
    wts = len(os.listdir(REPO + '/.git/worktrees')) + 1 if os.path.isdir(REPO + '/.git/worktrees') else 1
    P('checkout readings %s %s: porcelain %d config_sha256 %s refs %d worktrees %d' % (tag, ts(), por, sha(REPO + '/.git/config')[:16], len(o2.splitlines()), wts))
def tap(o):
    g = lambda k: (re.findall(r'^# %s (\d+)' % k, o, re.M) or ['?'])[-1]
    notok = [re.sub(r'^\s*not ok \d+ - ', '', l) for l in o.splitlines() if re.match(r'^\s*not ok \d+ - ', l)]
    return g('tests'), g('pass'), g('fail'), notok

os.makedirs(OUT, exist_ok=True)
P('drafter_run', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), 'sections', ''.join(sorted(ONLY)) or 'ALL')
readings('START')

# ---------------------------------------------------------------- A setup
W = tempfile.mkdtemp(prefix='gate1020_draft_', dir=SCR); C = W + '/clone'; P('workdir', W)
rc, o, e, _ = run(['git', 'clone', '--shared', '--no-checkout', '--quiet', REPO, C]); P('clone rc', rc, e.strip()[:200]); assert rc == 0
T = {}
for name, at in (('base', B), ('head', H)):
    wt = W + '/wt_' + name
    rc, o, e, _ = run(['git', '-C', C, 'worktree', 'add', '--detach', '--quiet', wt, at]); assert rc == 0, e
    rc, o, e, _ = run(['git', '-C', wt, 'rev-parse', 'HEAD', 'HEAD:' + LD]); P('tree', name, 'HEAD + lock-discovery blob', o.split())
    T[name] = wt
    dev = wt + '/Blockchain/Dev'
    rc, o, e, dt = run(['npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund'], cwd=dev + '/scripts/audit', label='npmci_' + name)
    P('  scripts/audit npm ci', name, 'rc', rc, 'secs %.1f' % dt, 'semver present', os.path.isdir(dev + '/scripts/audit/node_modules/semver'))
    rc, o, e, _ = run(['git', '-C', wt, 'status', '--porcelain']); P('  porcelain after install', len(o.splitlines()))
DEV = {k: v + '/Blockchain/Dev' for k, v in T.items()}
json.dump({'W': W, 'trees': T}, open(GS + '/drafter_paths.json', 'w'), indent=1)

# ---------------------------------------------------------------- B static
if want('B'):
    P('\n== B static', ts())
    for args in (['--name-only'], ['--numstat'], ['-w', '--numstat'], ['--ignore-blank-lines', '--numstat']):
        rc, o, e, _ = run(['git', '-C', C, 'diff', '--no-renames', *args, B, H]); P('  diff', ' '.join(args), '->', o.strip().replace('\n', ' | '))
    rc, o, e, _ = run(['git', '-C', C, 'rev-list', '--count', B + '..' + H]); P('  commits base..head', o.strip())
    rc, o, e, _ = run(['git', '-C', C, 'diff', '-U0', B, H, '--', LD])
    minus = [l for l in o.splitlines() if l.startswith('-') and not l.startswith('---')]
    plus = [l for l in o.splitlines() if l.startswith('+') and not l.startswith('+++')]
    P('  removed lines', len(minus), minus); P('  added lines', len(plus))
    for l in plus: P('   +', 'COMMENT' if l[1:].lstrip().startswith('//') else 'CODE   ', l[1:][:140])
    # parser: transpile with comments removed; base vs head must differ ONLY in the literal; control = head with the literal put back
    ts_path = REPO + '/Blockchain/Dev/node_modules/typescript'
    js = r'''
const ts = require(process.argv[1]); const fs = require('fs');
const strip = (s) => ts.transpileModule(s, { compilerOptions: { removeComments: true, target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.ESNext } }).outputText;
const base = strip(fs.readFileSync(process.argv[2], 'utf8')); const head = strip(fs.readFileSync(process.argv[3], 'utf8'));
const headSrc = fs.readFileSync(process.argv[3], 'utf8'); const anchor = "expires: '2026-10-19',";
const n = headSrc.split(anchor).length - 1; const ctrl = strip(headSrc.replace(anchor, "expires: '2026-09-17',"));
const bl = base.split('\n'), hl = head.split('\n'); const d = [];
for (let i = 0; i < Math.max(bl.length, hl.length); i++) if (bl[i] !== hl[i]) d.push([i + 1, bl[i], hl[i]]);
console.log(JSON.stringify({ ts: ts.version, lines_base: bl.length, lines_head: hl.length, differing_lines: d, anchor_count: n, control_literal_restored_equals_base: ctrl === base }));
'''
    bpath = W + '/base.lock-discovery.mjs'; hpath = DEV['head'] + '/scripts/audit/lock-discovery.mjs'
    open(bpath, 'w').write(open(DEV['base'] + '/scripts/audit/lock-discovery.mjs').read())
    rc, o, e, _ = run(['node', '-e', js, ts_path, bpath, hpath]); P('  parser compare rc', rc, o.strip(), e.strip()[:300])
    # every other dated fuse byte-identical base vs head
    for f in ('Blockchain/Dev/scripts/audit/audit-baseline.json', 'Blockchain/Dev/scripts/audit/baseline-contract.mjs', 'Blockchain/Dev/scripts/audit/expected-case-count', 'Blockchain/Dev/.security/exceptions.yml'):
        rc, o, e, _ = run(['git', '-C', C, 'rev-parse', B + ':' + f, H + ':' + f]); bb, hh = o.split(); P('  blob', f.split('/')[-1], bb[:9], hh[:9], 'IDENTICAL' if bb == hh else 'DIFFERS')

# ---------------------------------------------------------------- C suites per tree (real clock)
def suites(tree, tag, contract=True, gate=False):
    dev = DEV[tree]; row = {'tag': tag}
    rc, o, e, dt = run(['node', '--test', 'scripts/audit/lock-discovery.test.mjs'], cwd=dev, label=tag + '_lockdiscovery')
    t, p_, f, notok = tap(o); row['ld'] = (rc, t, p_, f); P('  %-26s lock-discovery.test  rc %d tests %s pass %s fail %s secs %.1f' % (tag, rc, t, p_, f, dt))
    for n in notok: P('      not ok:', n[:150])
    if contract:
        rc, o, e, dt = run(['npm', 'run', 'audit:contract', '--silent'], cwd=dev, label=tag + '_contract')
        t, p_, f, notok = tap(o + e); exp = open(dev + '/scripts/audit/expected-case-count').read().strip()
        row['contract'] = (rc, t, p_, f); P('  %-26s audit:contract       rc %d tests %s pass %s fail %s (expected-case-count %s) secs %.1f' % (tag, rc, t, p_, f, exp, dt))
        for n in notok: P('      not ok:', n[:150])
    rc, o, e, dt = run(['node', 'scripts/audit/audit-locks.mjs'], cwd=dev, label=tag + '_locks')
    first = (re.findall(r'audit-locks: (\d+) standalone lockfiles \((\d+) tracked.*?minus (\d+) declared out of scope', o) or [''])[0]
    lapsed = 'LAPSED' in (o + e); row['locks'] = rc
    P('  %-26s audit-locks          rc %d scanned/tracked/oos %s LAPSED-text %s secs %.1f | %s' % (tag, rc, first, lapsed, dt, (e.strip().splitlines() or [''])[-1][:140] if rc else o.strip().splitlines()[-1][:140]))
    if gate:
        rc, o, e, dt = run(['node', 'scripts/audit/audit-gate.mjs'], cwd=dev, label=tag + '_gate')
        P('  %-26s audit-gate           rc %d secs %.1f | %s' % (tag, rc, dt, ((o + e).strip().splitlines() or [''])[-1][:140]))
    return row
if want('C'):
    P('\n== C suites (real clock)', ts(), 'utc now', datetime.datetime.now(datetime.timezone.utc).isoformat())
    suites('base', 'C_base_d7e95cd9f', gate=True)
    suites('head', 'C_head_71bd80a35', gate=True)

# ---------------------------------------------------------------- D clock unit probe
INSTANTS = ['2026-10-18T12:59:59.999Z', '2026-10-18T13:00:00.000Z', '2026-10-18T23:59:59.999Z', '2026-10-19T00:00:00.000Z', '2026-10-19T00:00:00.001Z']
if want('D'):
    P('\n== D clock unit probe (shipped utcToday / isLapsed / validateOutOfScope)', ts())
    probe = GS + '/clock_probe.mjs'
    rc, o, e, _ = run(['node', probe, DEV['head']]); P('  REAL clock (control)  rc', rc, o.strip(), e.strip()[:200])
    rc, o, e, _ = run(['node', probe, DEV['head']], fake='2020-01-01T00:00:00Z'); P('  PRELOAD control 2020  rc', rc, o.strip(), e.strip()[:200])
    for at in INSTANTS:
        rc, o, e, _ = run(['node', probe, DEV['head']], fake=at); P('  head @ %-26s rc %d %s %s' % (at, rc, o.strip(), e.strip()[:200]))
    rc, o, e, _ = run(['node', probe, DEV['base']], fake='2026-09-16T23:59:59.999Z'); P('  base @ 2026-09-16T23:59:59.999Z rc', rc, o.strip())
    rc, o, e, _ = run(['node', probe, DEV['base']], fake='2026-09-17T00:00:00.000Z'); P('  base @ 2026-09-17T00:00:00.000Z rc', rc, o.strip())
    js = "import('file://%s/scripts/audit/baseline-contract.mjs').then(m=>{const e={expires:'2026-10-19'};console.log(JSON.stringify({'10-18':m.isLapsed(e,'2026-10-18'),'10-19':m.isLapsed(e,'2026-10-19'),'10-20':m.isLapsed(e,'2026-10-20'),'ctrl_2026-10-18_on_10-18':m.isLapsed({expires:'2026-10-18'},'2026-10-18')}))})" % DEV['head']
    rc, o, e, _ = run(['node', '-e', js]); P('  isLapsed(today injected by argument) rc', rc, o.strip())
    py = 'from datetime import datetime; from zoneinfo import ZoneInfo as Z\nfor s in ["2026-09-17T00:00:00+00:00","2026-10-18T13:00:00+00:00","2026-10-19T00:00:00+00:00","2026-10-18T00:00:00+00:00"]:\n  d=datetime.fromisoformat(s); print("   zoneinfo", s, "->", d.astimezone(Z("Australia/Sydney")).strftime("%a %Y-%m-%d %H:%M %Z (UTC%z)"))'
    rc, o, e, _ = run(['python3', '-c', py]); P(o.rstrip())

# ---------------------------------------------------------------- E clock whole-suite
if want('E'):
    P('\n== E clock whole-suite on head (preload reaches node --test workers and the gate process)', ts())
    for at in ('2026-10-18T23:59:59.999Z', '2026-10-19T00:00:00.000Z'):
        dev = DEV['head']; tag = 'E_head_' + at[:19].replace(':', '')
        rc, o, e, dt = run(['node', '--test', 'scripts/audit/lock-discovery.test.mjs'], cwd=dev, fake=at, label=tag + '_lockdiscovery')
        t, p_, f, notok = tap(o); P('  head @ %s lock-discovery.test rc %d tests %s pass %s fail %s' % (at, rc, t, p_, f))
        for n in notok: P('      not ok:', n[:150])
        rc, o, e, dt = run(['node', 'scripts/audit/audit-locks.mjs'], cwd=dev, fake=at, label=tag + '_locks')
        P('  head @ %s audit-locks rc %d LAPSED-text %s | %s' % (at, rc, 'LAPSED' in (o + e), ((o + e).strip().splitlines() or [''])[-1][:140]))

# ---------------------------------------------------------------- F tampers on head
ANCHOR = "      expires: '2026-10-19',\n"
COMMENT = ("      // KS-769: Kam ruled dormant (\"Dormant but kept\", panel 2026-09-17 15:10 AEST);\n"
           "      // exclusion kept, fuse re-dated to the end of Sunday 2026-10-18 Sydney time (AEDT).\n"
           "      // isLapsed is `expires <= utcToday()`, so a date is dead ON that UTC date: this\n"
           "      // value lapses 00:00Z Mon 19 Oct = 11:00 AEDT ('2026-10-18' would blow 13 h early).\n")
def tamper(tag, old, new, fake=None, contract=False, pred=''):
    path = DEV['head'] + '/scripts/audit/lock-discovery.mjs'; pristine = sha(path)
    s = open(path).read(); n = s.count(old); assert n == 1, 'ANCHOR COUNT %d for %s' % (n, tag)
    open(path, 'w').write(s.replace(old, new)); assert sha(path) != pristine or old == new
    P('  %s: anchor count 1, sha %s -> %s, fake %s, PREDICTED %s' % (tag, pristine[:12], sha(path)[:12], fake, pred))
    try:
        dev = DEV['head']
        rc, o, e, dt = run(['node', '--test', 'scripts/audit/lock-discovery.test.mjs'], cwd=dev, fake=fake, label='F_' + tag + '_lockdiscovery')
        t, p_, f, notok = tap(o); P('     lock-discovery.test rc %d tests %s pass %s fail %s' % (rc, t, p_, f))
        for x in notok: P('       not ok:', x[:140])
        if contract:
            rc, o, e, dt = run(['npm', 'run', 'audit:contract', '--silent'], cwd=dev, fake=fake, label='F_' + tag + '_contract')
            t, p_, f, notok = tap(o + e); P('     audit:contract rc %d tests %s pass %s fail %s' % (rc, t, p_, f))
            for x in notok: P('       not ok:', x[:140])
        rc, o, e, dt = run(['node', 'scripts/audit/audit-locks.mjs'], cwd=dev, fake=fake, label='F_' + tag + '_locks')
        msg = [l for l in (o + e).splitlines() if 'LAPSED' in l or 'not an ISO' in l or l.startswith('OK')]
        P('     audit-locks rc %d | %s' % (rc, (msg or [''])[0][:160]))
    finally:
        rc, o, e, _ = run(['git', '-C', T['head'], 'checkout', '--', LD]); got = sha(path)
        rc2, o2, e2, _ = run(['git', '-C', T['head'], 'status', '--porcelain', '--', 'Blockchain/Dev/scripts/audit/lock-discovery.mjs'])
        P('     restored sha %s identical %s porcelain(file) %d' % (got[:12], got == pristine, len(o2.splitlines()))); assert got == pristine
if want('F'):
    P('\n== F tampers on head (real clock unless fake named)', ts())
    tamper('T1_2026-09-17', ANCHOR, ANCHOR.replace('2026-10-19', '2026-09-17'), contract=True, pred='ld 5 fail; contract 10 fail; locks rc 3 (seat T1)')
    tamper('T2_2026-09-16', ANCHOR, ANCHOR.replace('2026-10-19', '2026-09-16'), pred='ld 5 fail; locks rc 3 (seat T2)')
    tamper('T3_soon', ANCHOR, ANCHOR.replace("'2026-10-19'", "'soon'"), pred='ld 5 fail; locks rc 3 not an ISO (seat T3)')
    tamper('T4_2026-09-18', ANCHOR, ANCHOR.replace('2026-10-19', '2026-09-18'), pred='green, locks rc 0 (seat T4)')
    tamper('T5_comment_removed', COMMENT, '', pred='green (seat T5)')
    tamper('T6_2026-10-18_realclock', ANCHOR, ANCHOR.replace('2026-10-19', '2026-10-18'), pred='green today: nothing at real clock distinguishes 10-18 from 10-19 (drafter)')
    tamper('T7_2026-10-18_at_1018T0000Z', ANCHOR, ANCHOR.replace('2026-10-19', '2026-10-18'), fake='2026-10-18T00:00:00.000Z', pred='ld 5 fail, locks rc 3: the 13 h-early date is dead at 11:00 AEDT Sunday (drafter)')
    tamper('T8_head_value_at_1018T0000Z_CONTROL', ANCHOR, ANCHOR, fake='2026-10-18T00:00:00.000Z', pred='green: the shipped value is live at the same instant (drafter control for T7)')

# ---------------------------------------------------------------- G fuse census under an injected clock
if want('G'):
    P('\n== G fuse census: audit-baseline dated rows, head, injected clock', ts())
    base_json = json.load(open(DEV['head'] + '/scripts/audit/audit-baseline.json'))['accepted']
    today = datetime.date(2026, 9, 17); horizon = today + datetime.timedelta(days=14)
    near = sorted((v['expires'], k, v.get('package'), v.get('ticket')) for k, v in base_json.items() if isinstance(v, dict) and v.get('expires') and v['expires'] <= horizon.isoformat())
    P('  dated rows <= %s: %d' % (horizon, len(near)))
    for r in near: P('   ', r)
    for at in ('REAL', '2026-09-23T23:59:59.999Z', '2026-09-24T00:00:00.000Z', '2026-09-30T00:00:00.000Z'):
        for gate in ('audit-gate', 'audit-locks'):
            tag = 'G_%s_%s' % (gate, at[:19].replace(':', ''))
            rc, o, e, dt = run(['node', 'scripts/audit/%s.mjs' % gate], cwd=DEV['head'], fake=None if at == 'REAL' else at, label=tag)
            txt = o + e; sec = txt.split('LAPSED', 1)[1] if 'LAPSED' in txt else ''
            ids = sorted(set(re.findall(r'(GHSA-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4})', sec)))
            fresh = re.findall(r'FAIL — (\d+) (?:NEW )?advisor', txt)
            P('  %-12s @ %-26s rc %d secs %.1f lapsed %d %s fresh-hdr %s | %s' % (gate, at, rc, dt, len(ids), ids, fresh, (txt.strip().splitlines() or [''])[-1][:120]))

readings('CLOSE')
P('done', ts())
