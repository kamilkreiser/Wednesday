#!/bin/bash
# controls_check.sh — every §4 positive-control token / pin the L7 brief states, re-read at the PINNED SHAs through the GitHub
# contents API (token by NAME from the Secuura .env, never printed) plus the local records and the drafter's merge facts, and
# exits non-zero on any count that is not the one stated. A ZERO here REFUSES the install. Negative controls (proving it can
# refuse): CC_HEAD918=<sha> / CC_HEAD925=<sha> / CC_HEAD924=<sha> / CC_M20=<sha> swap a pin; CC_NEG_TOKEN=<text> adds a token the
# checker must find exactly once in run-code-guards.sh@#918 (point it at one you know is absent).
# Usage: controls_check.sh            (rc 0 = every control held; rc 1 = at least one FAIL; prints ok/FAIL lines and FAILS=N)
set -u
G="$(cd "$(dirname "$0")" && pwd)"
python3 - "$G" <<'PY'
import base64, hashlib, json, os, re, sys, urllib.request, urllib.error, datetime, subprocess
G = sys.argv[1]
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'; tok = ''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok = line.strip().split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN not found by name'
API = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
E = os.environ
H918 = E.get('CC_HEAD918', 'b54487216ebb49f1de7ed9349f089d92a3e5bfc1'); H924 = E.get('CC_HEAD924', 'b85f1db24596a5e0ce98fe2b1343d9f515a1a995')
H925 = E.get('CC_HEAD925', '5341b1daed8afe4254e05ef66ef4350fd8220d4f'); M20 = E.get('CC_M20', 'a5334350221c819f54d4a20a3308daeb9ca09617')
M18 = '8861e62161466c40f08d2b10a30edeb203123993'; MRG918 = '21368d250'; REV918 = 'ed954f09e'; PRE925 = '4459a6068'; S161_924 = '1497b39de'
fails = 0
def ck(c, m):
    global fails
    print(('ok   ' if c else 'FAIL ') + m); fails += 0 if c else 1
cache = {}
def content(path, ref):
    k = (path, ref)
    if k in cache: return cache[k]
    try:
        j = json.load(urllib.request.urlopen(urllib.request.Request(API + '/contents/' + path + '?ref=' + ref, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
        data = base64.b64decode(j['content']); cache[k] = (j['sha'], data)
    except urllib.error.HTTPError as e:
        cache[k] = ('ABSENT' if e.code == 404 else 'HTTP%d' % e.code, b'')
    return cache[k]
print('controls_check at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '| pins', H918[:9], H924[:9], H925[:9], 'M20', M20[:9])
RCG = 'Blockchain/Dev/scripts/run-code-guards.sh'; RCT = 'Blockchain/Dev/scripts/__tests__/run_code_guards.test.sh'
PF = 'Blockchain/Dev/scripts/preflight/preflight.sh'; PFD = 'Blockchain/Dev/scripts/__tests__/preflight_deps.test.sh'
LC = 'Blockchain/Dev/scripts/preflight/lockfile-cleanroom.sh'; HOOK = '.githooks/pre-push'; PPT = 'Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh'
CE = 'Blockchain/Dev/scripts/check-environment.sh'
# ---- 1. file@ref pins: blob / bytes / lines / sha256 (as the brief's TARGET states them) -------------------------------------------
PINS = [(RCG, H918, '2f06e19d3', 12546, 225, 'b0a951a444455d83'), (RCG, MRG918, '83c4b7c15', 10070, 205, '68f49f6f604a4253'), (RCG, REV918, '83c4b7c15', 10070, 205, '68f49f6f604a4253'),
        (RCG, H925, '2f06e19d3', 12546, 225, 'b0a951a444455d83'), (RCT, H918, '55a376f76', 8271, 158, '4b9b66c62359e03a'), (RCT, H925, '55a376f76', 8271, 158, '4b9b66c62359e03a'),
        (PF, H918, '8f445a4bb', 31838, 554, '6e128baf66b1f274'), (PF, MRG918, '8f445a4bb', 31838, 554, '6e128baf66b1f274'), (PF, H925, '28d3636c1', 41969, 753, 'a65577f0176b5394'),
        (PF, PRE925, 'cbe140533', 41128, 736, 'b70de43d1e2b20e6'), (PF, M18, 'acfb7fa3e', 29971, 521, '7f4083d915708a15'), (PF, M20, '0727300f7', 31527, 545, 'b8bb4c873c9fb61d'),
        (PFD, H918, '343f24a6e', 28643, 456, 'ec344d954dc89a0c'), (PFD, H925, '5ad054131', 31660, 496, 'f4c0ece2c398d41e'), (PFD, M18, 'a713a94e7', 27888, 447, '43ba502df8219550'), (PFD, M20, 'a713a94e7', 27888, 447, '43ba502df8219550'),
        (LC, H924, '518bffeea', 6478, 133, '4f0522fe0c72ab4b'), (LC, S161_924, 'a549d751d', 6081, 128, 'e0e8f531faa94836'), (LC, M20, '26e7feb2b', 5183, 118, 'b7983ccece331ad6'), (LC, H925, '26e7feb2b', 5183, 118, 'b7983ccece331ad6'),
        (HOOK, H925, '1b22d4e14', 16472, 282, '92abd8e9b30e8d19'), (HOOK, M20, '1b22d4e14', 16472, 282, '92abd8e9b30e8d19'), (HOOK, M18, 'f0748ed56', 14027, None, 'cc940299b2aec733'),
        (PPT, H925, 'affdf027b', 34232, 646, '6dabbb516e92e5cf'), (PPT, M20, 'affdf027b', 34232, 646, '6dabbb516e92e5cf'), (PPT, M18, 'd95af6514', 26945, 524, '48ada0c361efcc3c'),
        (CE, H918, '172cabff4', 4493, 119, '31e0fb62e5a750bb'), (CE, M20, '172cabff4', 4493, 119, '31e0fb62e5a750bb')]
for path, ref, blob, nbytes, nlines, sha in PINS:
    b, d = content(path, ref); lines = d.count(b'\n'); h = hashlib.sha256(d).hexdigest()[:16]
    ck(b.startswith(blob) and len(d) == nbytes and (nlines is None or lines == nlines) and h == sha, f"{path.split('/')[-1]}@{ref[:9]}: blob {b[:9]} bytes {len(d)} lines {lines} sha {h} (pinned {blob} {nbytes} {nlines} {sha})")
for path, ref in [(RCG, M20), (RCT, M20), (RCG, M18)]:
    ck(content(path, ref)[0] == 'ABSENT', f"{path.split('/')[-1]}@{ref[:9]}: ABSENT (pinned absent)")
# ---- 2. exact lines (HEAD line numbers as the brief cites them) ----------------------------------------------------------------------
def line(path, ref, n):
    ls = content(path, ref)[1].decode('utf-8').split('\n'); return ls[n - 1] if n <= len(ls) else '<no such line>'
LINES = [(RCG, H918, 100, '  "check-akto-container-names.sh|check-stack-safety.sh:334"'), (RCG, H918, 108, '# THE REASON STRINGS ARE LIVE BASH.'),
         (RCG, H918, 117, '  "check-environment.sh|NOT A PROPERTY OF THE TREE, AND NO LIVE HOME:'), (RCG, H918, 187, 'OK — all $tracked_count tracked guards accounted for ($accounted_count buckets entries).'),
         (RCG, H918, 224, 'echo "OK — $ran code guards passed."'), (RCG, H918, 70, '# check-environment.sh runs `docker info`. It is DEFERRED below'),
         (PFD, H918, 346, '''printf '#!/usr/bin/env bash\\necho "OK — 0 code guards (fixture stub)"\\nexit 0\\n' > "$dev/scripts/run-code-guards.sh"'''),
         (PFD, H918, 398, "if printf '%s' \"$out\" | grep -q 'PREFLIGHT PASSED'; then verdict='SUITES-GREEN'"),
         (PFD, H925, 409, 'GATEWAY_URL="http://127.0.0.1:1" PREFLIGHT_STRICT_LEGS=0 bash scripts/preflight/preflight.sh 2>&1'),
         (PFD, H925, 427, "if [ \"$prc\" -eq 0 ] && printf '%s' \"$out\" | grep -q 'PREFLIGHT PASSED\\|Nothing failed'; then verdict='SUITES-GREEN'"),
         (PFD, H925, 459, 'expect "F-925-3: a step header whose denominator disagrees with TOTAL_LEGS ABORTS the run, naming the header"'), (PFD, H925, 460, '"HEADER-MISMATCH/1" "$(preflight_fixture_run 0 0 ok mismatch)"'),
         (PF, H925, 130, 'TOTAL_LEGS=15'), (PF, H925, 167, 'if [ "$_hdr_total" != "$TOTAL_LEGS" ]; then'), (PF, H925, 169, 'echo "PREFLIGHT ABORTED — step header \\"$1\\" says /$_hdr_total but TOTAL_LEGS=$TOTAL_LEGS."'),
         (PF, H925, 726, 'echo "PREFLIGHT INCOMPLETE — $n_ran/$TOTAL_LEGS legs ran, $n_skipped SKIPPED. Nothing failed."'), (PF, H925, 750, 'PREFLIGHT_STRICT_LEGS=1 — refusing to pass on legs that did not run.'),
         (LC, H924, 133, 'echo "  covered: ${CHECKED[*]-}"'), (LC, S161_924, 128, 'echo "  covered: ${CHECKED[*]}"'), (PF, M20, 96, 'env_fail=0'), (LC, M20, None, 'SKIP="services/mcp-server"')]
for path, ref, n, want in LINES:
    if n is None: ck(want in content(path, ref)[1].decode('utf-8'), f"{path.split('/')[-1]}@{ref[:9]} contains {want!r}")
    else: ck(want in line(path, ref, n), f"{path.split('/')[-1]}@{ref[:9]}:{n} carries {want[:70]!r}")
# ---- 3. token counts (exact, as the brief states them; controls beside the zeros) --------------------------------------------------
def cnt(path, ref, t, rx=False):
    d = content(path, ref)[1].decode('utf-8'); return len(re.findall(t, d, re.M)) if rx else d.count(t)
TOKENS = [(RCG, H918, 'check-environment.sh', 2, 0), (RCG, REV918, 'check-environment.sh', 1, 0), (RCG, H918, 'fourteen', 2, 0), (RCG, H918, 'thirteen', 2, 0), (RCG, H918, 'check-akto-container-names.sh', 1, 0),
          (RCG, H918, 'WIRED=(', 1, 0), (RCG, H918, 'HOMED_ELSEWHERE=(', 1, 0), (RCG, H918, 'DEFERRED=(', 1, 0),
          (PF, H925, r'^step "\d+/15', 15, 1), (PF, H918, r'^step "\d+/15', 15, 1), (PF, H925, '/13 |/14 ', 0, 0), (PF, H918, '/13 |/14 ', 0, 0), (PF, M20, '/13 |/14 ', 0, 0),
          (PF, H925, '_hdr_total', 6, 0), (PF, H925, 'PREFLIGHT_ALLOW_INCOMPLETE', 1, 0), (PF, H925, 'PREFLIGHT_STRICT_LEGS', 4, 0), (PF, H925, r'^echo "PREFLIGHT PASSED\."', 0, 1), (PF, H918, r'^echo "PREFLIGHT PASSED\."', 1, 1),
          (PF, H925, 'PREFLIGHT PASSED.', 2, 0), (PF, H925, 'TOTAL_LEGS=15', 1, 0), (PF, H925, 'env_fail', 3, 0), (PF, H918, 'env_fail', 0, 0), (PF, M20, 'env_fail', 3, 0), (PF, H925, 'PREFLIGHT ABORTED', 1, 0),
          (PFD, H925, 'PREFLIGHT_STRICT_LEGS=0', 1, 0), (PFD, H918, 'PREFLIGHT_STRICT_LEGS=0', 0, 0), (PFD, H925, 'Nothing failed', 2, 0), (PFD, H925, 'HEADER-MISMATCH', 2, 0), (PFD, H925, 'TAMPER-DID-NOT-LAND', 1, 0),
          (PFD, H918, 'fixture stub', 2, 0), (PFD, M18, 'fixture stub', 1, 0), (PFD, H925, "grep -q 'PREFLIGHT PASSED'", 0, 0), (PFD, H918, "grep -q 'PREFLIGHT PASSED'", 1, 0),
          (LC, H924, 'CHECKED[*]-', 1, 0), (LC, S161_924, 'CHECKED[*]-', 0, 0), (LC, S161_924, 'CHECKED[*]', 1, 0), (LC, M20, 'SKIP="services/mcp-server"', 1, 0), (LC, H924, 'SKIP="services/mcp-server"', 0, 0),
          (HOOK, H925, 'KS-991', 3, 0), (PPT, H925, 'CASE 10', 8, 0), (PPT, H925, 'CASE 11', 6, 0)]
if E.get('CC_NEG_TOKEN'): TOKENS.append((RCG, H918, E['CC_NEG_TOKEN'], 1, 0))
for path, ref, t, want, rx in TOKENS:
    got = cnt(path, ref, t, bool(rx)); ck(got == want, f"{path.split('/')[-1]}@{ref[:9]} {t!r} x{got} (pinned {want})")
# ---- 4. tamper anchors (count 1) and the DEFERRED reasons' inertness (+ a planted positive control) ------------------------------------
ANCH = [(RCG, H918, '  "check-akto-container-names.sh|check-stack-safety.sh:334"\n'), (RCG, H918, '  check-connector-xss.sh\n'), (RCG, H918, '  check-env-consistency.sh\n'),
        (RCG, H918, '"check-container-isolation.sh|NOT A PROPERTY OF THE TREE:'), (PFD, H925, 'GATEWAY_URL="http://127.0.0.1:1" PREFLIGHT_STRICT_LEGS=0 bash scripts/preflight/preflight.sh 2>&1'),
        (PF, H925, '\nTOTAL_LEGS=15\n'), (PFD, H918, '''printf '#!/usr/bin/env bash\\necho "OK — 0 code guards (fixture stub)"\\nexit 0\\n' > "$dev/scripts/run-code-guards.sh"''')]
for path, ref, a in ANCH: ck(cnt(path, ref, a) == 1, f"tamper anchor x{cnt(path, ref, a)} in {path.split('/')[-1]}@{ref[:9]}: {a[:50]!r}")
d = content(RCG, H918)[1].decode('utf-8'); blk = d[d.index('DEFERRED=('):] if 'DEFERRED=(' in d else ''; blk = blk[:blk.index('\n)')] if '\n)' in blk else ''
reasons = re.findall(r'^\s*"[^|]+\|(.*)"\s*$', blk, re.M); off = [r for r in reasons if re.search(r'[`$"]', r)]
ck(len(reasons) == 4 and not off, f"DEFERRED reasons parsed {len(reasons)} (4), offenders [`$\"] {len(off)} (0)")
ck(bool(re.search(r'[`$"]', 'planted `docker info` control')), 'positive control: the offender regex catches a planted backtick')
# ---- 5. the round-1 records on disk ----------------------------------------------------------------------------------------------------
R1 = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-13_s213/boot/peter_918_review_5151452193.md'
S161 = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura-blockchain/reports/2026-09-09-s161-batch-six-prs/report.md'
r = open(R1, encoding='utf-8').read(); s = open(S161, encoding='utf-8').read()
ck(len(r.encode()) == 7946 and r.count('The ask — one line') == 1 and r.count('Not approving today') == 1 and r.count('13 wired / 4 homed elsewhere / 3 deferred = 20') == 1, f"Peter's #918 review on disk: {len(r.encode())} B (7,946), 'The ask — one line' x{r.count('The ask — one line')}, 'Not approving today' x{r.count('Not approving today')}")
ck(len(s.encode()) == 39790 and s.count('F-925-3') == 1 and s.count('F-924-1') == 1 and s.count('1497b39de') == 1 and s.count('0956c3dbe') == 2, f"s161 report on disk: {len(s.encode())} B (39,790), F-925-3 x{s.count('F-925-3')}, F-924-1 x{s.count('F-924-1')}, 1497b39de x{s.count('1497b39de')}, 0956c3dbe x{s.count('0956c3dbe')}")
ck(not os.path.exists('/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-09-s161-batch-six-prs/report.md'), "control: the s161 report is NOT under projects/secuura/ (the tasking's path) — it is under projects/secuura-blockchain/")
# ---- 6. the merge facts in the drafter's clone (read verbs) ---------------------------------------------------------------------------
C = G + '/model/clone'
def rp(x): return subprocess.run(['git', '-C', C, 'rev-parse', x], capture_output=True, text=True).stdout.strip()
ck(rp('f089eaffee03a552c78a55fd0472a38d9210a1d3:' + PF).startswith('8840ac661'), "M21 tree f089eaffe: preflight.sh blob 8840ac661")
ck(rp('364e44ca1923755e329c3a8407e011bd495d6dfc:' + PF).startswith('28d3636c1'), "END tree 364e44ca1: preflight.sh blob 28d3636c1 (= #925's head)")
ck(rp('4641202fd9163c246653456476b2ee8228004925:' + LC).startswith('518bffeea'), "924M tree 4641202fd: lockfile-cleanroom.sh blob 518bffeea (= #924's head)")
ck(open(G + '/mt_925_M21.out').read().count('CONFLICT (content): Merge conflict in ' + PF) == 1 and open(G + '/mt_918_M20.out').read().startswith('f089eaffee03a552c78a55fd0472a38d9210a1d3'), "mt_*.out: #918 onto M20 clean (f089eaffe); #925 onto M21 CONFLICT in preflight.sh")
ck(subprocess.run(['git', '-C', C, 'merge-base', '--is-ancestor', 'a4f71cde660c1442d98317e26d93845340b20098', M20]).returncode == 1, "a4f71cde6 is NOT an ancestor of M20 (a squash)")
ck(subprocess.run(['git', '-C', C, 'merge-base', '--is-ancestor', 'a4f71cde660c1442d98317e26d93845340b20098', H925]).returncode == 0 and subprocess.run(['git', '-C', C, 'merge-base', '--is-ancestor', H918, H925]).returncode == 0 and subprocess.run(['git', '-C', C, 'merge-base', '--is-ancestor', H924, H925]).returncode == 1, "ancestry: a4f71cde6 and #918 ARE ancestors of #925; #924 is NOT")
# ---- 7. the brief and prompt name every pin; no raw control byte in the set -----------------------------------------------------------
B = open(G + '/2026-09-14_secuura-L7-918r2-924-925-ks926-ks773-ks1046-tier2.md', encoding='utf-8').read(); P = open(G + '/2026-09-14_secuura-L7-918r2-924-925-ks926-ks773-ks1046-tier2.prompt.txt', encoding='utf-8').read()
for tkn in [H918, H924, H925, M20, 'a4f71cde660c1442d98317e26d93845340b20098', '8861e62161466c40f08d2b10a30edeb203123993', 'f089eaffee03a552c78a55fd0472a38d9210a1d3', '364e44ca1923755e329c3a8407e011bd495d6dfc', '4641202fd9163c246653456476b2ee8228004925', '28d3636c1', '8840ac661', 'a65577f0176b5394', R1, S161, 'TIER 2', 'ROUND 2', 'RE-GATE', 'mergeable: false']:
    ck(tkn in B, f"brief names {tkn[:60]!r}")
for tkn in [H918, H924, H925, M20, '364e44ca1923755e329c3a8407e011bd495d6dfc', '28d3636c1', R1, S161, 'TIER 2', 'ROUND 2', 'RE-GATE', 'MAIL YOUR VERDICT', 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout', 'no memory maintenance', 'NEVER print a credential value', 'ultrathink']:
    ck(tkn in P, f"prompt names {tkn[:60]!r}")
ck(P.startswith('ultrathink\n'), 'prompt opens with ultrathink')
for f in sorted(os.listdir(G)):
    if f.endswith(('.md', '.txt', '.sh', '.py')) and os.path.isfile(G + '/' + f) and not f.startswith('brief.pre'):
        raw = open(G + '/' + f, 'rb').read(); n = sum(1 for b in raw if b < 32 and b not in (9, 10))
        if n: ck(False, f"raw control bytes in {f}: {n}")
ck(sum(1 for b in b'abc\x00def' if b < 32 and b not in (9, 10)) == 1, 'positive control: the byte census counts a synthetic NUL')
print('controls_check: FAILS=%d' % fails); sys.exit(1 if fails else 0)
PY
