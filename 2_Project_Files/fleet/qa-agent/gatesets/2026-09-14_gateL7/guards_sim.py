#!/usr/bin/env python3
"""guards_sim.py — the DRAFTER's derivation of every prediction in the L7 TIER-2 brief (#918 r2 / #924 re-gate / #925 re-gate),
from the bytes at the pinned heads, in the drafter's OWN shared clone under this OUTPUT DIR (model/clone + detached worktrees
wt918 @ b54487216, wt925 @ 5341b1dae, wt925pre @ 4459a6068, wt924 @ b85f1db24, wt924merged @ the merge-tree of b85f1db24 onto
develop M18, wtdev @ 8861e6216). Nothing here touches the Secuura checkout or any worktree of it.

Predictions are written BELOW, before any run; every cell is scored against its prediction and printed EXACT / MISPREDICTED.
Tampers land on COPIES (or, where the census needs a git tree, in the drafter's own worktree with the file restored by
content and its sha256 + porcelain asserted). HOLD-safe by construction: no docker (a `docker` SHIM on PATH logs any
invocation for the inertness cells; the real check-environment.sh runs ONLY under env -i with `command -v docker` asserted
empty first); no stack; no push; the real 15-leg preflight is NOT run — the verdict shape is re-derived in the fixture the
suite itself uses (probe_verdict.sh).

Usage: guards_sim.py <OUTPUT DIR>      Exit 0 = every prediction held · 1 = a misprediction or a precondition failed.
"""
import os, re, subprocess, sys, hashlib, shutil, datetime, time
G = sys.argv[1]
M = f"{G}/model"; SIM = f"{G}/sim"; TMP = f"{SIM}/tmp"; os.makedirs(TMP, exist_ok=True)
WT918 = f"{M}/wt918"; WT925 = f"{M}/wt925"; WT925PRE = f"{M}/wt925pre"; WT924 = f"{M}/wt924"; WT924M = f"{M}/wt924merged"; WTDEV = f"{M}/wtdev"
BASE_ENV = {k: v for k, v in os.environ.items() if k not in ('GH_TOKEN', 'LINEAR_API_KEY', 'AGENTMAIL_API_KEY', 'PREFLIGHT_STRICT_LEGS', 'GATEWAY_URL', 'HOOK_SH', 'CODE_GUARDS_SH', 'PREFLIGHT_DEPS_TEST_ROOT')}
BASE_ENV['TMPDIR'] = TMP; BASE_ENV['GIT_CONFIG_GLOBAL'] = '/dev/null'; BASE_ENV['GIT_CONFIG_SYSTEM'] = '/dev/null'
fails = 0
def ck(cond, msg):
    global fails
    print(("ok   " if cond else "FAIL ") + msg); fails += 0 if cond else 1
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def run(cmd, cwd, env=None, timeout=900, stdin=None):
    e = dict(BASE_ENV); e.update(env or {})
    t0 = time.time()
    r = subprocess.run(cmd, cwd=cwd, env=e, capture_output=True, text=True, timeout=timeout, stdin=subprocess.DEVNULL)
    return r.returncode, r.stdout + r.stderr, round(time.time() - t0, 1)
def keep(name, out): open(f"{SIM}/run.{name}.out", 'w', encoding='utf-8').write(out)
def porcelain(wt): return subprocess.run(['git', '-C', wt, 'status', '--porcelain'], capture_output=True, text=True).stdout.count('\n')
def tally(out, prefix):  # "<prefix>: N passed, M failed"  or "N passed, M failed"
    m = re.search(r'(\d+) passed, (\d+) failed', out)
    return (int(m.group(1)), int(m.group(2))) if m else (-1, -1)
def red_titles(out):
    return re.findall(r'^\s*FAIL (.+)$', out, re.M)
print("guards_sim at", datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
print("bash:", subprocess.run(['/bin/bash', '--version'], capture_output=True, text=True).stdout.splitlines()[0])
print("git:", subprocess.run(['git', '--version'], capture_output=True, text=True).stdout.strip(), "| node:", subprocess.run(['node', '--version'], capture_output=True, text=True).stdout.strip(), "| npm:", subprocess.run(['npm', '--version'], capture_output=True, text=True).stdout.strip())

# ---- 0. the worktrees are at the pinned SHAs, porcelain 0; the bytes are the pinned ones -------------------------------
for wt, want in [(WT918, 'b54487216ebb49f1de7ed9349f089d92a3e5bfc1'), (WT925, '5341b1daed8afe4254e05ef66ef4350fd8220d4f'), (WT925PRE, '4459a6068725c9a32b35a8541116cdfda72a72d5'), (WT924, 'b85f1db24596a5e0ce98fe2b1343d9f515a1a995'), (WTDEV, '8861e62161466c40f08d2b10a30edeb203123993')]:
    h = subprocess.run(['git', '-C', wt, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    ck(h == want and porcelain(wt) == 0, f"{wt.split('/')[-1]} at {h[:9]} (pinned {want[:9]}), porcelain {porcelain(wt)}")
t924m = subprocess.run(['git', '-C', WT924M, 'rev-parse', 'HEAD^{tree}'], capture_output=True, text=True).stdout.strip()
ck(t924m.startswith('3dd35ef6d') and porcelain(WT924M) == 0, f"wt924merged tree {t924m[:9]} (s213's merge-tree prediction 3dd35ef6d), porcelain {porcelain(WT924M)}")
RCG = 'Blockchain/Dev/scripts/run-code-guards.sh'; RCT = 'Blockchain/Dev/scripts/__tests__/run_code_guards.test.sh'
PF = 'Blockchain/Dev/scripts/preflight/preflight.sh'; PFD = 'Blockchain/Dev/scripts/__tests__/preflight_deps.test.sh'
LC = 'Blockchain/Dev/scripts/preflight/lockfile-cleanroom.sh'; CE = 'Blockchain/Dev/scripts/check-environment.sh'
PINS = {f"{WT918}/{RCG}": 'b0a951a444455d83', f"{WT918}/{RCT}": '4b9b66c62359e03a', f"{WT918}/{PF}": '6e128baf66b1f274', f"{WT918}/{PFD}": 'ec344d954dc89a0c',
        f"{WT925}/{PF}": 'a65577f0176b5394', f"{WT925}/{PFD}": 'f4c0ece2c398d41e', f"{WT925}/{RCG}": 'b0a951a444455d83', f"{WT925PRE}/{PF}": 'b70de43d1e2b20e6',
        f"{WT924}/{LC}": '4f0522fe0c72ab4b', f"{WT924M}/{LC}": '4f0522fe0c72ab4b', f"{WTDEV}/{PF}": '7f4083d915708a15', f"{WTDEV}/{LC}": 'b7983ccece331ad6', f"{WT918}/{CE}": '31e0fb62e5a750bb'}
for p, want in PINS.items():
    ck(sha(p) == want, f"{p.replace(M + '/', '')} sha256 {sha(p)} (pinned {want})")
# bash -n on the shell files at the heads
for p in [f"{WT918}/{RCG}", f"{WT918}/{RCT}", f"{WT918}/{PF}", f"{WT918}/{PFD}", f"{WT925}/{PF}", f"{WT925}/{PFD}", f"{WT924}/{LC}", f"{M}/lockfile-cleanroom.sh.1497b39de"]:
    rc, out, _ = run(['/bin/bash', '-n', p], G); ck(rc == 0, f"/bin/bash -n {p.replace(M + '/', '')} rc={rc}")

# ---- 1. static facts the brief states (counted, not believed) -----------------------------------------------------------
rcg = open(f"{WT918}/{RCG}", encoding='utf-8').read()
wired = re.search(r'^WIRED=\(\n(.*?)^\)', rcg, re.S | re.M).group(1).split()
homed = re.findall(r'^  "([^"|]+)\|', re.search(r'^HOMED_ELSEWHERE=\(\n(.*?)^\)', rcg, re.S | re.M).group(1), re.M)
deferred_block = re.search(r'^DEFERRED=\(\n(.*?)^\)', rcg, re.S | re.M).group(1)
deferred = re.findall(r'^  "([^"|]+)\|', deferred_block, re.M)
ck(len(wired) == 13 and len(homed) == 4 and len(deferred) == 4 and len(set(wired + homed + deferred)) == 21, f"buckets at b54487216: WIRED {len(wired)} / HOMED {len(homed)} / DEFERRED {len(deferred)} = {len(set(wired + homed + deferred))} distinct")
ck('check-environment.sh' in deferred and 'check-environment.sh' not in wired and 'check-environment.sh' not in homed, "check-environment.sh sits in DEFERRED only")
ck('check-akto-container-names.sh' in homed and 'check-stack-safety.sh' in wired, "check-akto-container-names.sh HOMED (its caller check-stack-safety.sh is WIRED)")
ck(rcg.count('"check-akto-container-names.sh|check-stack-safety.sh:334"') == 1, "the HOMED entry names check-stack-safety.sh:334")
css = open(f"{WT918}/Blockchain/Dev/scripts/check-stack-safety.sh", encoding='utf-8').read().split('\n')
akto_call_lines = [i + 1 for i, l in enumerate(css) if 'check-akto-container-names.sh' in l and not l.lstrip().startswith('#')]
ck(334 in akto_call_lines or any(abs(x - 334) <= 3 for x in akto_call_lines), f"check-stack-safety.sh names the akto guard on non-comment line(s) {akto_call_lines} (the entry says :334)")
# the reason strings: no backtick, no $, no inner double quote — with a planted control
reasons = re.findall(r'^  "([^\n]*)"\s*$', deferred_block, re.M)
ck(len(reasons) == 4, f"4 DEFERRED reason strings parsed (got {len(reasons)})")
bad = [r[:40] for r in reasons if re.search(r'[`$"]', r)]
ck(bad == [], f"no DEFERRED reason carries a backtick, a dollar sign or an inner double quote (offenders: {bad})")
ck(re.search(r'[`$"]', 'plant `docker info` and $ERRORS') is not None, "regex positive control: a planted reason with a backtick and a $ IS caught")
ce_reason = [r for r in reasons if r.startswith('check-environment.sh|')][0]
for tok in ['line 28', 'line 38', 'line 76', 'line 81', 'line 119', '5151452193', '8861e6216', 'check-slot-credentials.sh line 122', 'start-environment.sh (line 112)', 'env -i PATH=/usr/bin:/bin:/usr/sbin:/sbin']:
    ck(tok in ce_reason, f"the check-environment.sh DEFERRED reason names {tok!r}")
ck('THE REASON STRINGS ARE LIVE BASH' in rcg, "the bucket-header comment says the strings are live bash")
ck(rcg.count('Wall-clock for all thirteen together') == 1 and rcg.count('fourteen') == 2, f"header: 'thirteen' wall-clock sentence once; 'fourteen' occurs {rcg.count('fourteen')} (2: the 'was false for one of the original fourteen' sentence + the reviewer's 2.0 s note) — first written as 3, corrected to the file")
ck(rcg.count('exit 9:') == 1 and rcg.count('resolve by BASENAME') == 1, "Peter's two non-blocking notes answered as comments (exit 9; basename resolution)")
# preflight.sh at both heads: 15 headers agree with TOTAL_LEGS=15; no stale /13 or /14
for wt, tag in [(WT918, 'b54487216'), (WT925, '5341b1dae')]:
    pf = open(f"{wt}/{PF}", encoding='utf-8').read()
    hdr = re.findall(r'^step "(\d+)/(\d+) ', pf, re.M)
    stale = len(re.findall(r'/13 |/14 ', pf))
    tl = re.findall(r'^TOTAL_LEGS=(\d+)', pf, re.M)
    ck(len(hdr) == 15 and [int(a) for a, b in hdr] == list(range(1, 16)) and all(b == '15' for a, b in hdr) and stale == 0, f"preflight.sh @ {tag}: 15 step headers 1..15 all /15; stale '/13 |/14 ' count {stale}; TOTAL_LEGS={tl}")
pfdev = open(f"{WTDEV}/{PF}", encoding='utf-8').read()
ck(len(re.findall(r'/14 ', pfdev)) >= 14 and 'TOTAL_LEGS' not in pfdev, f"control: develop's preflight.sh carries {len(re.findall(r'/14 ', pfdev))} '/14 ' headers and no TOTAL_LEGS")
pf925 = open(f"{WT925}/{PF}", encoding='utf-8').read()
ck('PREFLIGHT ABORTED — step header' in pf925 and pf925.count('_hdr_total') == 6, f"the F-925-3 denominator check lives inside step() at 5341b1dae (_hdr_total x{pf925.count('_hdr_total')} — first written as 5, corrected to the file)")
ck('PREFLIGHT ABORTED' not in open(f"{WT925PRE}/{PF}", encoding='utf-8').read(), "control: preflight.sh @ 4459a6068 has NO denominator check")
ck(pf925.count('echo "PREFLIGHT PASSED."') == 0 and pf925.count('PREFLIGHT PASSED.') == 2 and pf925.count('PREFLIGHT PASSED — $TOTAL_LEGS/$TOTAL_LEGS legs ran.') == 1, f"the plain echo \"PREFLIGHT PASSED.\" line is gone at 5341b1dae (the 2 remaining 'PREFLIGHT PASSED.' are comments at :99 and :416); the ratio line is the only PASSED echo")
ck(open(f"{WT918}/{PF}", encoding='utf-8').read().count('echo "PREFLIGHT PASSED."') == 1, "control: #918's preflight.sh still prints develop's plain 'PREFLIGHT PASSED.'")
ck(pf925.count('${env_fail:-0}') == 1 and pf925.index('${env_fail:-0}') < pf925.index('PREFLIGHT FAILED — fix the above before pushing. ($n_ran'), "#903's env_fail arm sits INSIDE #925's fail arm ahead of the ratio line")
pfd925 = open(f"{WT925}/{PFD}", encoding='utf-8').read()
ck(pfd925.count("PREFLIGHT_STRICT_LEGS=0 bash scripts/preflight/preflight.sh") == 1, "the STRICT pin is on the nested run (ruling 4(c))")
ck(pfd925.count("""if [ "$prc" -eq 0 ] && printf '%s' "$out" | grep -q 'PREFLIGHT PASSED\\|Nothing failed'; then verdict='SUITES-GREEN'""") == 1, "the widened oracle (ruling 4(b)) occurs once")
ck(pfd925.count('"HEADER-MISMATCH/1" "$(preflight_fixture_run 0 0 ok mismatch)"') == 1, "the F-925-3 cell occurs once")
ck(len(re.findall(r'^expect ', pfd925, re.M)) == 37, f"expect() call sites at 5341b1dae: {len(re.findall(r'^expect ', pfd925, re.M))} (37 static sites, 36 at b54487216 — the F-925-3 cell is the +1; the PORT-REGISTRY loop adds the rest of the 56 at run time) — first written as 26, corrected to the file")
pfd918 = open(f"{WT918}/{PFD}", encoding='utf-8').read()
ck(pfd918.count('''printf '#!/usr/bin/env bash\\necho "OK — 0 code guards (fixture stub)"\\nexit 0\\n' > "$dev/scripts/run-code-guards.sh"''') == 1, "ruling 4(a)'s fixture line occurs once at b54487216")
ck(pfd918.count("grep -q 'PREFLIGHT PASSED'; then verdict='SUITES-GREEN'") == 1 and 'PREFLIGHT_STRICT_LEGS=0' not in pfd918, "control: #918's test file has the OLD oracle and no STRICT pin (those are #925's)")
lc = open(f"{WT924}/{LC}", encoding='utf-8').read()
ck(lc.count('echo "  covered: ${CHECKED[*]-}"') == 1 and 'echo "  covered: ${CHECKED[*]}"' not in lc, "F-924-1 fix at b85f1db24: the [*]- form, the bare [*] gone")
ck('echo "  covered: ${CHECKED[*]}"' in open(f"{M}/lockfile-cleanroom.sh.1497b39de", encoding='utf-8').read(), "control: the s161-gated 1497b39de bytes carry the bare [*]")
ck('SKIP="services/mcp-server"' in open(f"{WTDEV}/{LC}", encoding='utf-8').read() and 'services/mcp-server' not in lc.split('# =====', 2)[-1].split('set -uo')[1], "develop's guard still SKIPs services/mcp-server by name; the head's code has no mcp-server skip")
# widened-guard: the file lists
files_918 = ['Blockchain/Dev/scripts/__tests__/preflight_deps.test.sh', 'Blockchain/Dev/scripts/__tests__/run_code_guards.test.sh', 'Blockchain/Dev/scripts/preflight/preflight.sh', 'Blockchain/Dev/scripts/run-code-guards.sh']
files_924 = ['Blockchain/Dev/scripts/preflight/lockfile-cleanroom.sh']
files_925 = ['.githooks/pre-push', 'Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh'] + files_918
for n, fl, a, b in [(918, files_918, '8861e6216', 'b54487216'), (924, files_924, 'd4cf7e3cf', 'b85f1db24'), (925, files_925, '8861e6216', '5341b1dae')]:
    got = sorted(l.split('\t')[-1] for l in subprocess.run(['git', '-C', f"{M}/clone", 'diff', '--numstat', a, b], capture_output=True, text=True).stdout.splitlines())
    ck(got == sorted(fl) and not any(f.startswith(('Blockchain/Dev/services/', 'Blockchain/Dev/packages/')) for f in got), f"#{n} file set {a}..{b} = {len(got)} files, none under services/ or packages/: {[f.split('/')[-1] for f in got]}")

# ---- 2. PREDICTIONS, written before the runs ----------------------------------------------------------------------------
PRED = {
 # #918 at b54487216, in wt918
 '918.list':            "13 wired / 4 homed / 4 deferred; check-environment.sh under DEFERRED; akto under HOMED; rc 0",
 '918.census':          "rc 0; 'OK — all 21 tracked guards accounted for (21 buckets entries).'",
 '918.suite':           (15, 0),
 '918.pfd':             (55, 0),
 '918.run':             "rc 0; 'OK — 13 code guards passed.'; 0 FAILED lines",
 '918.R-a':             (53, 2, ['leg 1 lets the run proceed when deps-present exits 0', 'leg 14: suites green -> preflight passes']),
 '918.T2-akto-dropped': "rc 1; 'FAIL — guard(s) in the tree that no bucket accounts for:' + '  check-akto-container-names.sh'",
 '918.T3-plant':        "rc 1; the census names check-plant-drafter.sh; census OK again after the plant is moved to quarantine",
 '918.T4-ghost':        "rc 1; 'FAIL — bucket(s) naming a guard that is not in the tree:' + '  check-ghost-drafter.sh'",
 '918.T1a':             "rc 4; four '⚠ … not installed' lines (Homebrew, Node.js, npm, Docker); 0 'daemon' lines; docker shim NOT invoked",
 '918.T1b':             "rc 1; exactly one '  ^ FAILED: check-environment.sh'; 'CODE GUARDS FAILED — 14 guard(s) run'; docker shim NOT invoked",
 '918.inert':           "--list with the docker shim on PATH: 0 shim invocations; the PLANTED backticked reason: >= 1 invocation",
 # #925 at 5341b1dae, in wt925 (+ wt925pre)
 '925.pfd':             (56, 0),
 '925.pfd-strict':      (56, 0),
 '925.R-b-oracle':      (55, 1, ['leg 14: suites green -> preflight passes']),
 '925.R-c-nopin-strict': (54, 2, ['leg 1 lets the run proceed when deps-present exits 0', 'leg 14: suites green -> preflight passes']),
 '925.R-c-nopin-plain': (56, 0),
 '925.R-F9253':         (55, 1, ['F-925-3: a step header whose denominator disagrees with TOTAL_LEGS ABORTS the run, naming the header']),
 '925.T16':             "rc 1; 'PREFLIGHT ABORTED — step header \"1/15  OpenAPI spec drift (generated spec vs Zod source)\" says /15 but TOTAL_LEGS=16.'; 0 step banners",
 '925.verdict-new':     "rc 0; 'PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.' + 'legs 3 4 8'",
 '925.verdict-strict':  "rc 1; the same INCOMPLETE line + 'PREFLIGHT_STRICT_LEGS=1 — refusing to pass on legs that did not run.'",
 '925.verdict-old':     "rc 0; 'PREFLIGHT PASSED.' with 3 stack SKIP lines (the defect, develop's acfb7fa3e)",
 '925.verdict-918':     "rc 0; 'PREFLIGHT PASSED.' with 3 stack SKIP lines (#918's 15-leg script keeps develop's plain verdict)",
 # #924 at b85f1db24, in wt924 (+ wt924merged)
 '924.corpus-head':     "rc 0; 'All 35 standalone lock(s) pass clean-room npm ci.'; 'OK    services/mcp-server'; 0 FAIL/SKIP lines",
 '924.corpus-merged':   "rc 0; 'All N standalone lock(s) …' with N >= 35 (develop's 111 commits may add members); 'OK    services/mcp-server'; 0 FAIL lines",
 '924.F1-before':       "rc 1; 'SKIP  docs (no standalone lock)'; 'All 0 standalone lock(s) pass'; 'CHECKED[*]: unbound variable'",
 '924.F1-after':        "rc 0; 'All 0 standalone lock(s) pass'; '  covered: ' (empty); no 'unbound variable'",
 '924.F1-control':      "rc 0; 'OK    scripts/preflight'; 'All 1 standalone lock(s) pass'; '  covered: scripts/preflight'",
}
print("\nPREDICTIONS (written before the runs):")
for k, v in PRED.items(): print(f"  {k:24s} -> {v}")

# ---- 3. the runs — #918 -------------------------------------------------------------------------------------------------
dev918 = f"{WT918}/Blockchain/Dev"
rc, out, dt = run(['/bin/bash', 'scripts/run-code-guards.sh', '--list'], dev918); keep('918.list', out)
w = re.search(r'WIRED HERE \((\d+)\)', out); h = re.search(r'HOMED ELSEWHERE \((\d+)\)', out); d = re.search(r'DEFERRED, with reason \((\d+)\)', out)
sec = {'W': out.split('HOMED ELSEWHERE')[0], 'H': out.split('HOMED ELSEWHERE')[1].split('DEFERRED')[0], 'D': out.split('DEFERRED')[1]}
ck(rc == 0 and (w.group(1), h.group(1), d.group(1)) == ('13', '4', '4') and 'check-environment.sh' in sec['D'] and 'check-environment.sh' not in sec['W'] and 'check-akto-container-names.sh  <- check-stack-safety.sh:334' in sec['H'],
   f"918.list                 rc={rc} ({dt}s) {w.group(1)}/{h.group(1)}/{d.group(1)} — {'EXACT' if rc == 0 else 'MISPREDICTED'}")
rc, out, dt = run(['/bin/bash', 'scripts/run-code-guards.sh', '--check-unreached'], dev918); keep('918.census', out)
ck(rc == 0 and 'OK — all 21 tracked guards accounted for (21 buckets entries).' in out, f"918.census               rc={rc} ({dt}s) {out.strip().splitlines()[-1][:90]!r}")
rc, out, dt = run(['/bin/bash', 'scripts/__tests__/run_code_guards.test.sh'], dev918); keep('918.suite', out)
ck(rc == 0 and tally(out, '') == PRED['918.suite'], f"918.suite                rc={rc} ({dt}s) {tally(out, '')} — {'EXACT' if tally(out, '') == PRED['918.suite'] else 'MISPREDICTED'}; reds {red_titles(out)[:3]}")
rc, out, dt = run(['/bin/bash', 'scripts/__tests__/preflight_deps.test.sh'], dev918); keep('918.pfd', out)
ck(rc == 0 and tally(out, '') == PRED['918.pfd'], f"918.pfd                  rc={rc} ({dt}s) {tally(out, '')} — {'EXACT' if tally(out, '') == PRED['918.pfd'] else 'MISPREDICTED'}; reds {red_titles(out)[:3]}")
rc, out, dt = run(['/bin/bash', 'scripts/run-code-guards.sh'], dev918, timeout=600); keep('918.run', out)
ck(rc == 0 and 'OK — 13 code guards passed.' in out and out.count('^ FAILED') == 0, f"918.run                  rc={rc} ({dt}s, tree without node_modules) {out.strip().splitlines()[-1][:80]!r}; FAILED lines {out.count('^ FAILED')}")
# R-a: the (a) fixture line removed from a COPY of the test file, run against wt918's root
t = open(f"{WT918}/{PFD}", encoding='utf-8').read()
anchor_a = '''  printf '#!/usr/bin/env bash\\necho "OK — 0 code guards (fixture stub)"\\nexit 0\\n' > "$dev/scripts/run-code-guards.sh"\n'''
ck(t.count(anchor_a) == 1, "R-a anchor (the (a) stub line) occurs once in the head's test file")
p = f"{SIM}/preflight_deps.test.sh.918-R-a-no-stub"; open(p, 'w', encoding='utf-8').write(t.replace(anchor_a, ''))
rc, out, dt = run(['/bin/bash', p], dev918, env={'PREFLIGHT_DEPS_TEST_ROOT': dev918}); keep('918.R-a', out)
want = PRED['918.R-a']; got = tally(out, ''); reds = red_titles(out)
ck(rc == 1 and got == want[:2] and all(any(x in r for r in reds) for x in want[2]) and len(reds) == 2, f"918.R-a (stub line out)  rc={rc} ({dt}s) {got} — {'EXACT' if got == want[:2] else 'MISPREDICTED'}; reds {[r[:60] for r in reds]}")
# T2: the akto HOMED line dropped — in-place in the drafter's OWN worktree (the census needs a git tree), restored by content
rcg_path = f"{WT918}/{RCG}"; rcg_bytes = open(rcg_path, 'rb').read()
anchor_t2 = b'  "check-akto-container-names.sh|check-stack-safety.sh:334"\n'
ck(rcg_bytes.count(anchor_t2) == 1, "T2 anchor (the akto HOMED line) occurs once")
open(rcg_path, 'wb').write(rcg_bytes.replace(anchor_t2, b''))
ck(porcelain(WT918) == 1, "T2 landed: wt918 porcelain 1 (the runner modified)")
rc, out, dt = run(['/bin/bash', 'scripts/run-code-guards.sh', '--check-unreached'], dev918); keep('918.T2', out)
ck(rc == 1 and 'FAIL — guard(s) in the tree that no bucket accounts for:' in out and '\n  check-akto-container-names.sh\n' in out, f"918.T2 (akto dropped)    rc={rc} ({dt}s) {out.strip().splitlines()[0][:80]!r}")
open(rcg_path, 'wb').write(rcg_bytes); ck(sha(rcg_path) == 'b0a951a444455d83' and porcelain(WT918) == 0, "T2 restored by content: sha b0a951a444455d83, porcelain 0")
# T3: a tracked plant in no bucket (git add in the drafter's clone), then moved to quarantine + un-staged
plant = f"{dev918}/scripts/check-plant-drafter.sh"; open(plant, 'w').write('#!/usr/bin/env bash\nexit 0\n')
subprocess.run(['git', '-C', WT918, 'add', 'Blockchain/Dev/scripts/check-plant-drafter.sh'], check=True)
ck(porcelain(WT918) == 1, "T3 landed: the plant is staged (porcelain 1)")
rc, out, dt = run(['/bin/bash', 'scripts/run-code-guards.sh', '--check-unreached'], dev918); keep('918.T3', out)
ck(rc == 1 and '\n  check-plant-drafter.sh\n' in out and 'no bucket accounts for' in out, f"918.T3 (plant)           rc={rc} ({dt}s) names the plant: {'check-plant-drafter.sh' in out}")
subprocess.run(['git', '-C', WT918, 'rm', '--cached', '--quiet', 'Blockchain/Dev/scripts/check-plant-drafter.sh'], check=True)
os.makedirs(f"{SIM}/_quarantine_2026-09-14", exist_ok=True); shutil.move(plant, f"{SIM}/_quarantine_2026-09-14/check-plant-drafter.sh")
rc, out, dt = run(['/bin/bash', 'scripts/run-code-guards.sh', '--check-unreached'], dev918)
ck(rc == 0 and porcelain(WT918) == 0 and 'OK — all 21' in out, f"918.T3 undone: plant quarantined (not deleted), porcelain 0, census rc={rc} OK again")
# T4: a bucket naming a ghost
open(rcg_path, 'wb').write(rcg_bytes.replace(b'  check-connector-xss.sh\n', b'  check-connector-xss.sh\n  check-ghost-drafter.sh\n'))
rc, out, dt = run(['/bin/bash', 'scripts/run-code-guards.sh', '--check-unreached'], dev918); keep('918.T4', out)
ck(rc == 1 and 'FAIL — bucket(s) naming a guard that is not in the tree:' in out and '\n  check-ghost-drafter.sh\n' in out, f"918.T4 (ghost)           rc={rc} ({dt}s) names the ghost: {'check-ghost-drafter.sh' in out}")
open(rcg_path, 'wb').write(rcg_bytes); ck(sha(rcg_path) == 'b0a951a444455d83' and porcelain(WT918) == 0, "T4 restored by content: sha b0a951a444455d83, porcelain 0")
# the docker SHIM: a PATH dir whose `docker` logs every invocation and exits 1 (never the real binary)
shim = f"{SIM}/shim"; os.makedirs(shim, exist_ok=True); shimlog = f"{SIM}/docker-shim.log"
open(f"{shim}/docker", 'w').write(f'#!/bin/bash\necho "docker $*" >> "{shimlog}"\nexit 1\n'); os.chmod(f"{shim}/docker", 0o755)
def shim_hits():
    return open(shimlog).read().count('docker') if os.path.exists(shimlog) else 0
RESTRICTED = '/usr/bin:/bin:/usr/sbin:/sbin'
rc, out, _ = subprocess.run(['env', '-i', f'PATH={RESTRICTED}', '/bin/bash', '-c', 'for t in docker brew node npm; do command -v $t >/dev/null 2>&1 && echo "$t=ON-PATH"; done; echo probe-done'], capture_output=True, text=True).returncode, subprocess.run(['env', '-i', f'PATH={RESTRICTED}', '/bin/bash', '-c', 'for t in docker brew node npm; do command -v $t >/dev/null 2>&1 && echo "$t=ON-PATH"; done; echo probe-done'], capture_output=True, text=True).stdout, 0
ck('ON-PATH' not in out and 'probe-done' in out, f"PRECONDITION for T1a/T1b: docker, brew, node, npm are all ABSENT on {RESTRICTED} ({out.strip().replace(chr(10), ' ')})")
if 'ON-PATH' in out:
    print("REFUSING T1a/T1b: a prerequisite IS on the restricted PATH — the real guard could reach docker"); fails += 1
else:
    # T1a: the guard ALONE under env -i (the shim dir is NOT on this PATH; docker is simply absent → :81 never runs)
    if os.path.exists(shimlog): os.remove(shimlog)
    r = subprocess.run(['env', '-i', f'PATH={RESTRICTED}', 'HOME=/nonexistent', '/bin/bash', 'scripts/check-environment.sh'], cwd=dev918, capture_output=True, text=True, timeout=120)
    out = r.stdout + r.stderr; keep('918.T1a', out)
    warn = len(re.findall(r'⚠ .* not installed', out)); daemon = out.count('daemon')
    ck(r.returncode == 4 and warn == 4 and daemon == 0 and shim_hits() == 0, f"918.T1a (guard alone)    rc={r.returncode} '⚠ … not installed' x{warn} daemon-lines {daemon} shim-hits {shim_hits()} (optional-Aiken line: {out.count('Aiken not installed')})")
    # T1b: check-environment.sh put BACK into WIRED (in-place, restored after), the RUNNER under env -i
    open(rcg_path, 'wb').write(rcg_bytes.replace(b'  check-env-consistency.sh\n', b'  check-env-consistency.sh\n  check-environment.sh\n'))
    ck(porcelain(WT918) == 1 and open(rcg_path, encoding='utf-8').read().count('  check-environment.sh\n') == 1, "T1b landed: check-environment.sh back in WIRED (once)")
    r = subprocess.run(['env', '-i', f'PATH={RESTRICTED}', 'HOME=/nonexistent', f'TMPDIR={TMP}', '/bin/bash', 'scripts/run-code-guards.sh'], cwd=dev918, capture_output=True, text=True, timeout=900)
    out = r.stdout + r.stderr; keep('918.T1b', out)
    failed = re.findall(r'^\s*\^ FAILED: (.+)$', out, re.M)
    ck(r.returncode == 1 and failed == ['check-environment.sh'] and 'CODE GUARDS FAILED — 14 guard(s) run' in out and out.count('daemon') == 0 and shim_hits() == 0, f"918.T1b (runner, env -i)  rc={r.returncode} FAILED={failed} 14-run line {'CODE GUARDS FAILED — 14 guard(s) run' in out} daemon-lines {out.count('daemon')} shim-hits {shim_hits()}")
    open(rcg_path, 'wb').write(rcg_bytes); ck(sha(rcg_path) == 'b0a951a444455d83' and porcelain(WT918) == 0, "T1b restored by content: sha b0a951a444455d83, porcelain 0")
# inertness: --list with the shim FIRST on PATH — the shipped reason strings must not invoke docker; a planted backticked reason must
if os.path.exists(shimlog): os.remove(shimlog)
rc, out, dt = run(['/bin/bash', 'scripts/run-code-guards.sh', '--list'], dev918, env={'PATH': shim + ':' + os.environ['PATH']})
ck(rc == 0 and shim_hits() == 0, f"918.inert (shipped)      --list rc={rc} with the docker shim first on PATH: shim invocations {shim_hits()}")
planted = rcg_bytes.replace(b'"check-container-isolation.sh|NOT A PROPERTY OF THE TREE:', b'"check-container-isolation.sh|NOT A PROPERTY: it runs `docker info` and')
ck(planted != rcg_bytes, "inertness positive control: a backticked `docker info` planted into a COPY's reason string")
pp = f"{SIM}/run-code-guards.sh.planted-backtick"; open(pp, 'wb').write(planted)
rc, out, dt = run(['/bin/bash', pp, '--list'], dev918, env={'PATH': shim + ':' + os.environ['PATH']})
ck(shim_hits() >= 1, f"918.inert (planted)      --list on the planted copy: shim invocations {shim_hits()} (the class is live bash — s213's incident, reproduced on the shim, never on docker)")
ck(open(shimlog).read().startswith('docker info'), "the shim recorded exactly the planted command ('docker info')")

# ---- 4. the runs — #925 -------------------------------------------------------------------------------------------------
dev925 = f"{WT925}/Blockchain/Dev"; dev925pre = f"{WT925PRE}/Blockchain/Dev"
for name, env in [('925.pfd', {}), ('925.pfd-strict', {'PREFLIGHT_STRICT_LEGS': '1'})]:
    rc, out, dt = run(['/bin/bash', 'scripts/__tests__/preflight_deps.test.sh'], dev925, env=env); keep(name, out)
    got = tally(out, ''); ck(rc == 0 and got == PRED[name], f"{name:24s} rc={rc} ({dt}s) {got} — {'EXACT' if got == PRED[name] else 'MISPREDICTED'}; reds {red_titles(out)[:3]} env={env}")
t = open(f"{WT925}/{PFD}", encoding='utf-8').read()
A_ORACLE = """    if [ "$prc" -eq 0 ] && printf '%s' "$out" | grep -q 'PREFLIGHT PASSED\\|Nothing failed'; then verdict='SUITES-GREEN'\n"""
A_PIN = 'GATEWAY_URL="http://127.0.0.1:1" PREFLIGHT_STRICT_LEGS=0 bash scripts/preflight/preflight.sh 2>&1'
ck(t.count(A_ORACLE) == 1 and t.count(A_PIN) == 1, "R-b / R-c anchors occur once in the head's test file")
p = f"{SIM}/preflight_deps.test.sh.925-R-b-old-oracle"; open(p, 'w', encoding='utf-8').write(t.replace(A_ORACLE, """    if printf '%s' "$out" | grep -q 'PREFLIGHT PASSED'; then verdict='SUITES-GREEN'\n"""))
rc, out, dt = run(['/bin/bash', p], dev925, env={'PREFLIGHT_DEPS_TEST_ROOT': dev925}); keep('925.R-b', out)
want = PRED['925.R-b-oracle']; got = tally(out, ''); reds = red_titles(out)
ck(rc == 1 and got == want[:2] and len(reds) == 1 and want[2][0] in reds[0], f"925.R-b (old oracle)     rc={rc} ({dt}s) {got} — {'EXACT' if got == want[:2] else 'MISPREDICTED'}; reds {[r[:60] for r in reds]}")
p = f"{SIM}/preflight_deps.test.sh.925-R-c-no-pin"; open(p, 'w', encoding='utf-8').write(t.replace(A_PIN, 'GATEWAY_URL="http://127.0.0.1:1" bash scripts/preflight/preflight.sh 2>&1'))
rc, out, dt = run(['/bin/bash', p], dev925, env={'PREFLIGHT_DEPS_TEST_ROOT': dev925, 'PREFLIGHT_STRICT_LEGS': '1'}); keep('925.R-c-strict', out)
want = PRED['925.R-c-nopin-strict']; got = tally(out, ''); reds = red_titles(out)
ck(rc == 1 and got == want[:2] and len(reds) == 2 and all(any(x in r for r in reds) for x in want[2]), f"925.R-c (no pin, STRICT) rc={rc} ({dt}s) {got} — {'EXACT' if got == want[:2] else 'MISPREDICTED'}; reds {[r[:60] for r in reds]}")
rc, out, dt = run(['/bin/bash', p], dev925, env={'PREFLIGHT_DEPS_TEST_ROOT': dev925}); keep('925.R-c-plain', out)
got = tally(out, ''); ck(rc == 0 and got == PRED['925.R-c-nopin-plain'], f"925.R-c (no pin, plain)  rc={rc} ({dt}s) {got} — {'EXACT' if got == PRED['925.R-c-nopin-plain'] else 'MISPREDICTED'} (the pin is load-bearing ONLY under STRICT)")
# R-F9253: the HEAD's test file against the tree WITHOUT the step() check (4459a6068)
rc, out, dt = run(['/bin/bash', f"{WT925}/{PFD}"], dev925pre, env={'PREFLIGHT_DEPS_TEST_ROOT': dev925pre}); keep('925.R-F9253', out)
want = PRED['925.R-F9253']; got = tally(out, ''); reds = red_titles(out)
ck(rc == 1 and got == want[:2] and len(reds) == 1 and want[2][0] in reds[0] and 'got "SUITES-GREEN/0"' in out, f"925.R-F9253 (no check)   rc={rc} ({dt}s) {got} — {'EXACT' if got == want[:2] else 'MISPREDICTED'}; reds {[r[:70] for r in reds]}; got SUITES-GREEN/0: {'got \"SUITES-GREEN/0\"' in out}")
# T16: TOTAL_LEGS=16 on a COPY of the head's preflight.sh in a scratch tree; the abort must land at step 1 with no leg body
t16 = f"{SIM}/t16/Blockchain/Dev"; os.makedirs(f"{t16}/scripts/preflight", exist_ok=True)
pf = open(f"{WT925}/{PF}", encoding='utf-8').read()
ck(pf.count('\nTOTAL_LEGS=15\n') == 1, "T16 anchor 'TOTAL_LEGS=15' occurs once")
open(f"{t16}/scripts/preflight/preflight.sh", 'w', encoding='utf-8').write(pf.replace('\nTOTAL_LEGS=15\n', '\nTOTAL_LEGS=16\n'))
ck(open(f"{t16}/scripts/preflight/preflight.sh").read().count('\nTOTAL_LEGS=16\n') == 1, "T16 LANDED on the copy (grep'd before the run)")
rc, out, dt = run(['perl', '-e', 'alarm 60; exec @ARGV', '/bin/bash', 'scripts/preflight/preflight.sh'], t16, env={'GATEWAY_URL': 'http://127.0.0.1:9'}, timeout=120); keep('925.T16', out)
ck(rc == 1 and 'PREFLIGHT ABORTED — step header "1/15  OpenAPI spec drift (generated spec vs Zod source)" says /15 but TOTAL_LEGS=16.' in out and out.count('\n=== ') == 0 and '(step header 1/15 disagrees with TOTAL_LEGS 16)' in out,
   f"925.T16                  rc={rc} ({dt}s) abort line present {'PREFLIGHT ABORTED' in out}, step banners {out.count(chr(10) + '=== ')}, 'disagrees with TOTAL_LEGS' {'disagrees with TOTAL_LEGS' in out}")
# the verdict shape in the suite's own fixture (probe_verdict.sh): new plain / new STRICT / OLD (develop) / #918's
rss925 = f"{WT925}/Blockchain/Dev/scripts/run-shell-suites.sh"
for name, pfpath, strict, want_rc, want_lines in [
    ('925.verdict-new', f"{WT925}/{PF}", '0', 0, ['PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.', '  legs 3 4 8 — local stack not up']),
    ('925.verdict-strict', f"{WT925}/{PF}", '1', 1, ['PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.', 'PREFLIGHT_STRICT_LEGS=1 — refusing to pass on legs that did not run.']),
    ('925.verdict-old', f"{WTDEV}/{PF}", '0', 0, ['PREFLIGHT PASSED.']),
    ('925.verdict-918', f"{WT918}/{PF}", '0', 0, ['PREFLIGHT PASSED.'])]:
    rc, out, dt = run(['/bin/bash', f"{G}/probe_verdict.sh", pfpath, rss925, strict, name], G); keep(name, out)
    m = re.search(r'rc=(\d+)\s+step banners=(\d+)\s+SKIP-stack lines=(\d+)', out)
    got_rc, banners, skips = int(m.group(1)), int(m.group(2)), int(m.group(3))
    ok = got_rc == want_rc and all(l in out for l in want_lines) and skips == 3
    ck(ok, f"{name:24s} fixture rc={got_rc} ({dt}s) stack-SKIPs {skips} banners {banners} — {'EXACT' if ok else 'MISPREDICTED'}; verdict: {[l.strip('| ').strip() for l in out.splitlines() if l.startswith('  | PREFLIGHT')]}")
ck('Nothing failed' not in open(f"{SIM}/run.925.verdict-old.out").read() and 'legs ran' not in open(f"{SIM}/run.925.verdict-old.out").read(), "control: the OLD script's verdict names no ratio and no skip tally (the defect)")
# ancestry, in the drafter's clone
for a, b, want in [('a4f71cde6', '5341b1dae', True), ('b54487216', '5341b1dae', True), ('8861e6216', '5341b1dae', True), ('8861e6216', 'b54487216', True), ('b85f1db24', '5341b1dae', False), ('a4f71cde6', 'b54487216', False), ('8861e6216', 'b85f1db24', False)]:
    r = subprocess.run(['git', '-C', f"{M}/clone", 'merge-base', '--is-ancestor', a, b]).returncode == 0
    ck(r == want, f"ancestry: {a} {'IS' if r else 'NOT'} an ancestor of {b} (expected {'IS' if want else 'NOT'})")

# ---- 5. the runs — #924 -------------------------------------------------------------------------------------------------
for name, wt in [('924.corpus-head', WT924), ('924.corpus-merged', WT924M)]:
    dev = f"{wt}/Blockchain/Dev"
    rc, out, dt = run(['/bin/bash', 'scripts/preflight/lockfile-cleanroom.sh'], dev, timeout=900); keep(name, out)
    m = re.search(r'All (\d+) standalone lock\(s\) pass clean-room npm ci\.', out); n = int(m.group(1)) if m else -1
    locks = len(subprocess.run(['/bin/bash', '-c', 'find services packages frontend scripts -maxdepth 2 -name package-lock.json | wc -l'], cwd=dev, capture_output=True, text=True).stdout.strip()) and int(subprocess.run(['/bin/bash', '-c', 'find services packages frontend scripts -maxdepth 2 -name package-lock.json | wc -l'], cwd=dev, capture_output=True, text=True).stdout.strip())
    ok = rc == 0 and n >= 35 and n == locks and 'OK    services/mcp-server' in out and out.count('FAIL') == 0 and out.count('SKIP') == 0 and (n == 35 if name == '924.corpus-head' else True)
    ck(ok, f"{name:24s} rc={rc} ({dt}s) All {n} (find counts {locks} locks) mcp-server OK {'OK    services/mcp-server' in out} FAIL {out.count('FAIL')} SKIP {out.count('SKIP')} covered-line {'  covered: ' in out}")
dev924 = f"{WT924}/Blockchain/Dev"
before = f"{dev924}/scripts/preflight/lockfile-cleanroom.before-1497b39de.sh"
shutil.copy(f"{M}/lockfile-cleanroom.sh.1497b39de", before); ck(sha(before) == 'e0e8f531faa94836', "F-924-1 BEFORE bytes (1497b39de, blob a549d751d) placed beside the guard so its $0-relative cd resolves")
ck(not os.path.exists(f"{dev924}/docs/package-lock.json") and os.path.isdir(f"{dev924}/docs"), "the 'nolock' corpus member: Blockchain/Dev/docs exists and has no package-lock.json")
rc, out, dt = run(['/bin/bash', 'scripts/preflight/lockfile-cleanroom.before-1497b39de.sh', 'docs'], dev924); keep('924.F1-before', out)
ck(rc == 1 and 'SKIP  docs (no standalone lock)' in out and 'All 0 standalone lock(s) pass' in out and 'CHECKED[*]: unbound variable' in out, f"924.F1-before            rc={rc} ({dt}s) {[l for l in out.splitlines() if 'unbound' in l or l.startswith('All ')]}")
rc, out, dt = run(['/bin/bash', 'scripts/preflight/lockfile-cleanroom.sh', 'docs'], dev924); keep('924.F1-after', out)
ck(rc == 0 and 'All 0 standalone lock(s) pass' in out and '  covered: \n' in out + '\n' and 'unbound' not in out, f"924.F1-after             rc={rc} ({dt}s) {[l for l in out.splitlines() if l.startswith(('All ', '  covered'))]}")
rc, out, dt = run(['/bin/bash', 'scripts/preflight/lockfile-cleanroom.sh', 'scripts/preflight'], dev924); keep('924.F1-control', out)
ck(rc == 0 and 'OK    scripts/preflight' in out and 'All 1 standalone lock(s) pass' in out and '  covered: scripts/preflight' in out, f"924.F1-control           rc={rc} ({dt}s) {[l for l in out.splitlines() if l.startswith(('OK', 'All ', '  covered'))]}")
os.makedirs(f"{SIM}/_quarantine_2026-09-14", exist_ok=True); shutil.move(before, f"{SIM}/_quarantine_2026-09-14/lockfile-cleanroom.before-1497b39de.sh")
ck(porcelain(WT924) == 0, "wt924 porcelain 0 after the F-924-1 cells (the BEFORE copy moved to quarantine, not deleted)")
ck(os.path.exists(f"{WTDEV}/{LC}") and 'node_modules' not in os.listdir(dev924), "the clean-room ran on a tree with NO node_modules (npm ci --dry-run reads the lock only)")

# ---- 6. after: the pinned bytes are untouched -----------------------------------------------------------------------
for p, want in PINS.items():
    ck(sha(p) == want, f"after: {p.replace(M + '/', '')} sha256 still {want}")
for wt in [WT918, WT925, WT925PRE, WT924, WT924M, WTDEV]:
    ck(porcelain(wt) == 0, f"after: {wt.split('/')[-1]} porcelain 0")
print(f"\nwork dir (kept): {SIM}")
print(f"guards_sim: FAILS={fails}")
print("done at", datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
sys.exit(1 if fails else 0)
