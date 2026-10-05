#!/usr/bin/env python3
"""c6_image_gate63.py — the IMAGE PROOF the builder did NOT run (#1388, KS-1404 wiring). The gate's own scratch only.

Builds services/timestamping/Dockerfile at the BASE and at the HEAD from the gate's OWN two worktrees (context = <wt>/Blockchain/Dev,
the compose `context: .`), tags them g63-ts:base-f01c1da5717f / g63-ts:head-3ce575eeb63c (local tags only: NEVER pushed, never run
under compose, never on a box), then probes each image as the image's own runtime user:

  I1  `test -r /app/config/tsa-trust-anchors-dtrust.crt` as user nodejs: base rc 1 (absent), head rc 0
  I2  CONTROL `test -r /app/package.json`: rc 0 on BOTH (the probe can read; a 1 at base is not a broken probe)
  I3  `whoami` == nodejs and `id -u` == 1001 on both (the probe ran as the unprivileged user, not root)
  I4  the in-image anchor's sha256 == the sha256 of the head TREE blob (git show <head>:<anchor> | shasum)
  I5  inside the head image, as nodejs, the image's OWN dist parses the anchor: `node -e` require('/app/dist/tsa/rfc3161-verify.js')
      .parseTrustAnchors(readFileSync(<anchor>)) -> 1; at base the same probe cannot read the file (ENOENT) — fails closed
  I6  INFO: what else /app/config holds in the head image (the two-root bundle WITH DigiCert ships too; README.md); the image's own
      env carries no TSA_TRUST_ANCHORS_PEM (compose supplies it), so a container started WITHOUT compose has no anchor

NOT RUN is a verdict, never a pass: if the Docker daemon is unreachable (rc 20), a build exceeds --budget-sec (default 1200 s per
build; the client is killed, rc 21), or a pull/npm step fails for network reasons (rc 22, logs kept), the script writes
<out>/IMAGE-PROOF-NOT-RUN.md with the reason and exits non-zero. A build FAILURE at the head that is not network is a READING (rc 23).
Refuses (rc 2) any --wt-*/--out inside /Volumes/DevMASTER/!CODING (lexical AND realpath), or a worktree not at its kit sha.
Usage: c6_image_gate63.py --wt-base <dir> --wt-head <dir> --out <dir> [--budget-sec N]
       c6_image_gate63.py --selftest --out <dir>      (stub docker in <out>; G63_DOCKER is a SELFTEST-ONLY override)
rc 0 I1-I5 PASS / 1 a FAIL / 2 refused / 20-22 NOT RUN / 23 head build failed (reading)."""
import hashlib, json, os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate63 import K, Tally, outside_forbidden

ANCHOR = K['anchor_image_path']
PROBE = ('whoami; id -u; test -r %s; echo "ANCHOR_RC=$?"; test -r /app/package.json; echo "PKG_RC=$?"; '
         'sha256sum %s 2>/dev/null | cut -c1-64 | sed "s/^/ANCHOR_SHA=/"; ls -1 /app/config 2>/dev/null | sed "s/^/CONFIG_LS=/"; '
         'env | grep -c "^TSA_TRUST_ANCHORS_PEM=" | sed "s/^/ENV_TSA_PEM=/"; '
         'node -e "const v=require(\'/app/dist/tsa/rfc3161-verify.js\');const fs=require(\'fs\');'
         'try{console.log(\'PARSE=\'+v.parseTrustAnchors(fs.readFileSync(\'%s\',\'utf8\')).length)}catch(e){console.log(\'PARSE_ERR=\'+e.code)}"') % (ANCHOR, ANCHOR, ANCHOR)
NETWORK_HINTS = ('TLS handshake', 'dial tcp', 'i/o timeout', 'ENOTFOUND', 'EAI_AGAIN', 'ETIMEDOUT', 'toomanyrequests', 'connection reset',
                 'failed to resolve source metadata', 'network is unreachable')


def not_run(out, rc, reason):
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'IMAGE-PROOF-NOT-RUN.md'), 'w').write(
        '# Image proof: NOT RUN\n\n- when: %s\n- rc: %d\n- reason: %s\n\nNOT RUN is not a pass. I1-I5 are UNMEASURED.\n' % (
            time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), rc, reason))
    print('NOT RUN (rc %d): %s' % (rc, reason)); return rc


def run(cmd, out, name, timeout):
    t0 = time.time()
    try:
        p = subprocess.run(cmd, capture_output=True, timeout=timeout)
        o, e, rc = p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace'), p.returncode
    except subprocess.TimeoutExpired as x:
        o = (x.stdout or b'').decode('utf-8', 'replace'); e = (x.stderr or b'').decode('utf-8', 'replace') + '\nTIMEOUT after %ds' % timeout; rc = 124
    open(os.path.join(out, name + '.out'), 'w').write(o); open(os.path.join(out, name + '.err'), 'w').write(e)
    open(os.path.join(out, name + '.rc'), 'w').write('%d\n' % rc)
    print('  %s rc %d in %.0fs (%s.out/.err/.rc)' % (name, rc, time.time() - t0, name))
    return rc, o, e


def parse(o):
    d = {'lines': o.splitlines()}
    for l in o.splitlines():
        if '=' in l:
            k, v = l.split('=', 1); d.setdefault(k, []).append(v)
    return d


def judge(base, head, blob_sha, t):
    g = lambda d, k: (d.get(k) or [None])[0]
    t.check('I1', g(base, 'ANCHOR_RC') == '1' and g(head, 'ANCHOR_RC') == '0', 'test -r %s as the runtime user: base rc %s (want 1), head rc %s (want 0)' % (
        ANCHOR, g(base, 'ANCHOR_RC'), g(head, 'ANCHOR_RC')))
    t.check('I2', g(base, 'PKG_RC') == '0' and g(head, 'PKG_RC') == '0', 'CONTROL test -r /app/package.json: base rc %s head rc %s (want 0 / 0)' % (g(base, 'PKG_RC'), g(head, 'PKG_RC')))
    who = lambda d: d['lines'][:2]
    t.check('I3', who(base) == ['nodejs', '1001'] and who(head) == ['nodejs', '1001'], 'whoami/id -u base %s head %s (want nodejs/1001 both)' % (who(base), who(head)))
    t.check('I4', g(head, 'ANCHOR_SHA') == blob_sha, 'in-image sha256 %s vs head tree blob sha256 %s' % (str(g(head, 'ANCHOR_SHA'))[:16], blob_sha[:16]))
    t.check('I5', g(head, 'PARSE') == '1' and g(base, 'PARSE_ERR') == 'ENOENT', 'image dist parseTrustAnchors as nodejs: head %s (want PARSE=1); base %s (want PARSE_ERR=ENOENT)' % (
        g(head, 'PARSE') or 'PARSE_ERR=' + str(g(head, 'PARSE_ERR')), g(base, 'PARSE') or 'PARSE_ERR=' + str(g(base, 'PARSE_ERR'))))
    t.info('I6', 'head /app/config holds %s; base %s; TSA_TRUST_ANCHORS_PEM in the image env: head %s base %s (compose supplies it)' % (
        head.get('CONFIG_LS'), base.get('CONFIG_LS'), g(head, 'ENV_TSA_PEM'), g(base, 'ENV_TSA_PEM')))


def main(wb, wh, out, budget, docker):
    for p in (wb, wh, out):
        if not outside_forbidden(p):
            print('REFUSED: %s is inside %s — the image proof runs from the gate\'s OWN worktrees and writes to its OWN scratch' % (p, K['forbidden_root'])); return 2
    for wt, want in ((wb, K['base']), (wh, K['head'])):
        rc = subprocess.run(['git', '-C', wt, 'rev-parse', 'HEAD'], capture_output=True)
        got = rc.stdout.decode().strip()
        if got != want:
            print('REFUSED: worktree %s is at %r, not the kit sha %s' % (wt, got, want)); return 2
    os.makedirs(out, exist_ok=True)
    print('c6_image_gate63 docker %s | budget %ds per build | out %s' % (docker, budget, out))
    rc, o, e = run([docker, 'info', '--format', '{{.ServerVersion}} {{.Architecture}}'], out, 'docker_info', 60)
    if rc != 0:
        return not_run(out, 20, 'the Docker daemon is unreachable (`docker info` rc %d: %s)' % (rc, (e.strip().splitlines() or [''])[-1][:200]))
    tags = {}
    for side, wt, sha in (('base', wb, K['base']), ('head', wh, K['head'])):
        tag = 'g63-ts:%s-%s' % (side, sha[:12]); tags[side] = tag
        ctx = os.path.join(wt, 'Blockchain', 'Dev')
        rc, o, e = run([docker, 'build', '--progress=plain', '-f', os.path.join(ctx, 'services', 'timestamping', 'Dockerfile'), '-t', tag, ctx], out, 'build_' + side, budget)
        if rc == 124:
            return not_run(out, 21, 'docker build at %s exceeded the %ds budget (client killed; build_%s.err)' % (side, budget, side))
        if rc != 0:
            if any(h in e for h in NETWORK_HINTS):
                return not_run(out, 22, 'docker build at %s failed on a NETWORK step (build_%s.err): %s' % (side, side, [h for h in NETWORK_HINTS if h in e]))
            print('BUILD FAILED at %s (rc %d) — a READING, not an instrument trip: read build_%s.err' % (side, rc, side)); return 23
    res = {}
    for side in ('base', 'head'):
        rc, o, e = run([docker, 'run', '--rm', '--network', 'none', '--user', 'nodejs', '--entrypoint', 'sh', tags[side], '-c', PROBE], out, 'probe_' + side, 180)
        res[side] = parse(o)
    blob = subprocess.run(['git', '-C', wh, 'show', '%s:%s' % (K['head'], K['anchor_file'])], capture_output=True).stdout
    t = Tally(); judge(res['base'], res['head'], hashlib.sha256(blob).hexdigest(), t)
    json.dump({k: v for k, v in res.items()}, open(os.path.join(out, 'probe_parsed.json'), 'w'), indent=1)
    return t.end()


STUB = r'''#!/bin/bash
# stub docker for c6 SELFTEST ONLY. Mode from $G63_STUB_MODE: down | good | head_unreadable | hang | net
m="${G63_STUB_MODE:-good}"
case "$1" in
  info) [ "$m" = down ] && { echo "Cannot connect to the Docker daemon" >&2; exit 1; }; echo "29.8.0 aarch64"; exit 0;;
  build) [ "$m" = hang ] && exec /bin/sleep 30; [ "$m" = net ] && { echo "ERROR: failed to resolve source metadata for docker.io/library/node:24-alpine: dial tcp: i/o timeout" >&2; exit 1; }; echo "built"; exit 0;;
  run) img="${@: -3:1}"
       echo nodejs; echo 1001; echo "PKG_RC=0"; echo "ENV_TSA_PEM=0"
       case "$img" in
         *base*) echo "ANCHOR_RC=1"; echo "PARSE_ERR=ENOENT";;
         *) if [ "$m" = head_unreadable ]; then echo "ANCHOR_RC=1"; echo "PARSE_ERR=EACCES"; else echo "ANCHOR_RC=0"; echo "ANCHOR_SHA=__SHA__"; echo "CONFIG_LS=README.md"; echo "CONFIG_LS=tsa-trust-anchors-dtrust.crt"; echo "CONFIG_LS=tsa-trust-anchors.crt"; echo "PARSE=1"; fi;;
       esac; exit 0;;
esac
exit 0
'''


def selftest(out):
    import contextlib, io
    if not outside_forbidden(out):
        print('REFUSED: selftest out inside the forbidden root'); return 2
    os.makedirs(out, exist_ok=True)
    wb = os.environ.get('G63_WT_BASE'); wh = os.environ.get('G63_WT_HEAD')
    if not (wb and wh):
        print('SELFTEST needs G63_WT_BASE / G63_WT_HEAD (the gate\'s or drafter\'s own worktrees at the kit shas)'); return 2
    blob = subprocess.run(['git', '-C', wh, 'show', '%s:%s' % (K['head'], K['anchor_file'])], capture_output=True).stdout
    stub = os.path.join(out, 'stub_docker.sh'); open(stub, 'w').write(STUB.replace('__SHA__', hashlib.sha256(blob).hexdigest())); os.chmod(stub, 0o755)
    arms = [('daemon down -> NOT RUN 20', 'down', 1200, 20), ('a quiet good run -> PASS 0', 'good', 1200, 0),
            ('head anchor unreadable -> FAIL 1', 'head_unreadable', 1200, 1), ('a build that hangs past a 3 s budget -> NOT RUN 21', 'hang', 3, 21),
            ('a network failure in the build -> NOT RUN 22', 'net', 1200, 22)]
    ok = 0; total = 0
    for name, mode, budget, want in arms:
        d = os.path.join(out, 'arm_%s' % mode); os.environ['G63_STUB_MODE'] = mode
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf): rc = main(wb, wh, d, budget, stub)
        nr = os.path.exists(os.path.join(d, 'IMAGE-PROOF-NOT-RUN.md'))
        g = rc == want and (nr == (want in (20, 21, 22))); ok += g; total += 1
        print('SELFTEST %s %s: rc %d (want %d); NOT-RUN file %s' % ('OK' if g else 'MISS', name, rc, want, nr))
    with contextlib.redirect_stdout(io.StringIO()): rc = main(wb, wh, K['checkout'] + '/x', 10, stub)
    g = rc == 2; ok += g; total += 1
    print('SELFTEST %s --out inside !CODING -> REFUSED 2: rc %d' % ('OK' if g else 'MISS', rc))
    with contextlib.redirect_stdout(io.StringIO()): rc = main(wh, wh, os.path.join(out, 'arm_swapped'), 10, stub)
    g = rc == 2; ok += g; total += 1
    print('SELFTEST %s the head worktree passed as --wt-base -> REFUSED 2: rc %d' % ('OK' if g else 'MISS', rc))
    print('SELFTEST %s %d of %d' % ('OK' if ok == total else 'BROKEN', ok, total)); print('CHECKED %d arm(s)' % total)
    return 0 if ok == total else 1


if __name__ == '__main__':
    A = sys.argv[1:]
    if not A or '--help' in A or '-h' in A: print(__doc__); raise SystemExit(0)
    def opt(k, d=None): return A[A.index(k) + 1] if k in A else d
    if '--selftest' in A: raise SystemExit(selftest(opt('--out')))
    if os.environ.get('G63_DOCKER'):
        print('REFUSED: G63_DOCKER is a SELFTEST-ONLY override; unset it for a real image proof'); raise SystemExit(2)
    docker = '/usr/local/bin/docker' if os.path.exists('/usr/local/bin/docker') else 'docker'
    raise SystemExit(main(opt('--wt-base'), opt('--wt-head'), opt('--out'), int(opt('--budget-sec', K['image_budget_sec'])), docker))
