#!/usr/bin/env python3
"""guards_sim.py — the DRAFTER's derivation of every prediction in the #903 round-2 brief, from the bytes at head.

The suite `pre_push_hook_base.test.sh` builds LOCAL bare-repo fixtures under $TMPDIR, stubs the preflight to `exit 0`, and
takes the hook under test from $HOOK_SH — so a `git show` copy of the test file at head, run against `git show` copies of the
hook (develop's f0748ed56, the merge base's aae2743ac, the head's 1b22d4e14) and against TAMPERED copies of the head's hook,
re-derives the red-first pair and every tamper row WITHOUT touching the Secuura checkout or any worktree. Everything runs
under this OUTPUT DIR (TMPDIR inside it; the suite's own `trap rm -rf $WORK` cleans only the fixtures it made).

Predictions are written BELOW, before any run; the script scores each run against them on the suite's own tally line and
by cell title. A row that disagrees is printed as MISPREDICTED — the brief then carries the MEASURED value and says so.

This is a drafter's derivation, not the gate's measurement: the gate re-runs all of it in its own clone (brief items 2–3).
Usage: guards_sim.py <OUTPUT DIR>      Exit 0 = every prediction held · 1 = a misprediction or an anchor count disagreed.
"""
import os, re, subprocess, sys, hashlib, shutil, datetime
G = sys.argv[1]
M = f"{G}/model"
TEST = f"{M}/pre_push_hook_base.test.sh.a4f71cde6"
HOOK_HEAD = f"{M}/pre-push.a4f71cde6"
HOOK_DEV = f"{M}/pre-push.8861e6216"
HOOK_BASE = f"{M}/pre-push.986c592d5"
SIM = f"{G}/sim"; os.makedirs(SIM, exist_ok=True)
TMP = f"{SIM}/tmp"; os.makedirs(TMP, exist_ok=True)
fails = 0
def ck(cond, msg):
    global fails
    print(("ok   " if cond else "FAIL ") + msg); fails += 0 if cond else 1
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
print("guards_sim at", datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
print("bash:", subprocess.run(['/bin/bash', '--version'], capture_output=True, text=True).stdout.splitlines()[0])
print("git:", subprocess.run(['git', '--version'], capture_output=True, text=True).stdout.strip())

# ---- 0. the bytes are the pinned ones ------------------------------------------------------------------------------
ck(sha(TEST) == '6dabbb516e92e5cf', f"test file at head sha256 {sha(TEST)} (pinned 6dabbb516e92e5cf, blob affdf027b)")
ck(sha(HOOK_HEAD) == '92abd8e9b30e8d19', f"hook at head sha256 {sha(HOOK_HEAD)} (pinned 92abd8e9b30e8d19, blob 1b22d4e14)")
ck(sha(HOOK_DEV) == 'cc940299b2aec733', f"hook at develop sha256 {sha(HOOK_DEV)} (pinned cc940299b2aec733, blob f0748ed56)")
ck(sha(HOOK_BASE) == '57b046fed04ca492', f"hook at the merge base sha256 {sha(HOOK_BASE)} (pinned 57b046fed04ca492, blob aae2743ac)")
t = open(TEST, encoding='utf-8').read()
titles = re.findall(r'^\s*ok\s+"([^"]+)"', t, re.M) + re.findall(r'^\[ "\$landed" -eq 0 \] && ok "([^"]+)"', t, re.M)
ck(len(titles) == 28, f"28 `ok` titles at head (got {len(titles)})")
tdev = open(f"{M}/pre_push_hook_base.test.sh.8861e6216", encoding='utf-8').read()
tdev_titles = re.findall(r'^\s*ok\s+"([^"]+)"', tdev, re.M) + re.findall(r'^\[ "\$landed" -eq 0 \] && ok "([^"]+)"', tdev, re.M)
ck(len(tdev_titles) == 23, f"23 `ok` titles at develop (got {len(tdev_titles)})")
new_titles = [x for x in titles if x not in tdev_titles]
ck(len(new_titles) == 5 and all(('CASE 10' in x or 'CASE 11' in x) for x in new_titles), f"the 5 new titles are CASE 10/11's: {[x[:60] for x in new_titles]}")
ck([x for x in titles if x not in new_titles] == tdev_titles, "the other 23 titles are develop's 23, in order")
h = open(HOOK_HEAD, encoding='utf-8').read()
A_GUARD = """    _refs='develop origin/develop refs/remotes/origin/develop'
    if git rev-parse --verify --quiet develop >/dev/null 2>&1 &&
       git rev-parse --verify --quiet origin/develop >/dev/null 2>&1 &&
       [ "$(git rev-parse develop)" != "$(git rev-parse origin/develop)" ] &&
       git merge-base --is-ancestor develop origin/develop 2>/dev/null; then
        echo "[pre-push] KS-991: local 'develop' is BEHIND origin/develop — ignoring the" >&2
        echo "[pre-push]   stale ref for base selection. (git fetch origin develop:develop" >&2
        echo "[pre-push]   to refresh it.) origin/develop is still consulted below." >&2
        _refs='origin/develop refs/remotes/origin/develop'
    fi
    for _ref in $_refs; do
"""
ck(h.count(A_GUARD) == 1, "the whole KS-991 guard block occurs once in the head hook (the T1 anchor)")
A_IF = """    if git rev-parse --verify --quiet develop >/dev/null 2>&1 &&
       git rev-parse --verify --quiet origin/develop >/dev/null 2>&1 &&
       [ "$(git rev-parse develop)" != "$(git rev-parse origin/develop)" ] &&
       git merge-base --is-ancestor develop origin/develop 2>/dev/null; then
"""
ck(h.count(A_IF) == 1, "the guard's `if` occurs once (the Tg anchors)")
A_TOKEN = """        echo "[pre-push] KS-991: local 'develop' is BEHIND origin/develop — ignoring the" >&2
"""
ck(h.count(A_TOKEN) == 1, "the KS-991 notice line occurs once (the T3 anchor)")
ck(h.count('KS-991') == 3, f"`KS-991` occurs 3 times in the head hook (got {h.count('KS-991')})")
ck(h.count("merge-base --is-ancestor develop origin/develop") == 1, "the is-ancestor clause occurs once")
ck(h.count('[ "$(git rev-parse develop)" != "$(git rev-parse origin/develop)" ] &&') == 1, "the != clause occurs once")
ck(open(HOOK_DEV, encoding='utf-8').read().count("    for _ref in develop origin/develop refs/remotes/origin/develop; do\n") == 1, "develop's hook has the single loop line (the T1 target shape)")

# ---- 1. the tampers, written from Python by exact anchor ---------------------------------------------------------------
def tamper(name, old, new, expect_count=1):
    p = f"{SIM}/pre-push.{name}"
    s = h
    c = s.count(old)
    ck(c == expect_count, f"{name}: anchor count {c} (expected {expect_count})")
    s2 = s.replace(old, new)
    ck(s2 != s, f"{name}: bytes changed")
    open(p, 'w', encoding='utf-8').write(s2); os.chmod(p, 0o755)
    return p
T = {}
T['T1-revert-guard'] = tamper('T1-revert-guard', A_GUARD, "    for _ref in develop origin/develop refs/remotes/origin/develop; do\n")
T['T2-unconditional'] = tamper('T2-unconditional', A_GUARD, "    _refs='origin/develop refs/remotes/origin/develop'\n    for _ref in $_refs; do\n")
T['T3-drop-token'] = tamper('T3-drop-token', A_TOKEN, """        echo "[pre-push] local 'develop' is BEHIND origin/develop — ignoring the" >&2\n""")
T['TgA-direction-inverted'] = tamper('TgA-direction-inverted', "       git merge-base --is-ancestor develop origin/develop 2>/dev/null; then\n",
                                     "       git merge-base --is-ancestor origin/develop develop 2>/dev/null; then\n")
T['TgB-neq-dropped'] = tamper('TgB-neq-dropped', '       [ "$(git rev-parse develop)" != "$(git rev-parse origin/develop)" ] &&\n', "")
T['TgE-ancestor-true'] = tamper('TgE-ancestor-true', "       git merge-base --is-ancestor develop origin/develop 2>/dev/null; then\n", "       true; then\n")
ck(sha(HOOK_HEAD) == '92abd8e9b30e8d19', "the head hook copy is untouched after writing the tampers")

# ---- 2. PREDICTIONS, written before the runs (the suite's own tally line + the red titles) -----------------------------
PRED = {
 'head-1b22d4e14':        (28, 0, []),
 'develop-f0748ed56':     (26, 2, ['CASE 10 — a stale local develop is IGNORED', 'CASE 10 — a docs-only push on a CURRENT base SKIPS']),
 'base-aae2743ac':        (23, 5, ['CASE 7 — a systemTest-only push invokes', 'CASE 8 — a failing formatting gate REFUSES', 'CASE 8 — refused for the RIGHT reason',
                                   'CASE 10 — a stale local develop is IGNORED', 'CASE 10 — a docs-only push on a CURRENT base SKIPS']),
 'T1-revert-guard':       (26, 2, ['CASE 10 — a stale local develop is IGNORED', 'CASE 10 — a docs-only push on a CURRENT base SKIPS']),
 'T2-unconditional':      (26, 2, ['every resolvable base equals HEAD → the hook says so LOUDLY', 'CASE 10 — a stale local develop is IGNORED']),
 'T3-drop-token':         (27, 1, ['CASE 10 — a stale local develop is IGNORED']),
 # Tg-A: the ancestry test inverted (skip local develop when it is AHEAD of origin, consult it when BEHIND). CASE 10: develop is
 # behind -> guard false -> develop consulted first -> its diff carries trunk.txt -> the gate RUNS -> both CASE 10 cells red.
 # CASE 6: develop == HEAD (ahead of origin) -> guard TRUE -> the notice prints with its `[pre-push]` prefix -> CASE 6 asserts
 # that prefix ABSENT on a docs-only push -> red. CASE 4/9: guard true, notice printed, origin/develop informative -> RUN, and
 # their cells grep `[pre-push]` PRESENT + `[preflight] ran` -> green. CASE 5: origin/develop deleted -> guard false -> green.
 'TgA-direction-inverted': (25, 3, ['a docs-only push still SKIPS even with a local develop containing the tip', 'CASE 10 — a stale local develop is IGNORED', 'CASE 10 — a docs-only push on a CURRENT base SKIPS']),
 # Tg-B: the `!=` clause dropped -> the guard also fires when local develop == origin/develop (is-ancestor is true for equal
 # commits): a spurious notice, develop skipped, origin/develop (the same commit) consulted -> the DECISION is unchanged.
 # NO cell builds a fixture with local develop == origin/develop (CASE 1/2/3/7/8 have no local develop; 4/5/6 have develop == HEAD;
 # 9 has develop AHEAD; 10/11 have it BEHIND) -> the suite is BLIND to this clause: predicted 28/0. A Record, not a finding.
 'TgB-neq-dropped':       (28, 0, []),
 # Tg-E: the ancestry clause replaced by `true` -> "skip local develop whenever it differs from origin/develop" (the reorder Peter's
 # review says this is NOT). CASE 10/11 green (develop differs -> skipped, notice printed). CASE 6: develop == HEAD differs from
 # origin -> notice with `[pre-push]` -> CASE 6's absence assertion -> RED. CASE 4/9: notice + run -> green. CASE 5: guard false.
 'TgE-ancestor-true':     (27, 1, ['a docs-only push still SKIPS even with a local develop containing the tip']),
}
print("\nPREDICTIONS (written before the runs):")
for k, (p, f, reds) in PRED.items(): print(f"  {k:24s} -> {p} passed, {f} failed; red: {reds}")

# ---- 3. the runs ----------------------------------------------------------------------------------------------------
runs = [('head-1b22d4e14', HOOK_HEAD), ('develop-f0748ed56', HOOK_DEV), ('base-aae2743ac', HOOK_BASE)] + [(k, v) for k, v in T.items()]
results = {}
for name, hook in runs:
    env = dict(os.environ); env['HOOK_SH'] = hook; env['TMPDIR'] = TMP; env['GIT_CONFIG_GLOBAL'] = '/dev/null'; env['GIT_CONFIG_SYSTEM'] = '/dev/null'
    env.pop('GH_TOKEN', None)
    t0 = datetime.datetime.now()
    r = subprocess.run(['/bin/bash', TEST], capture_output=True, text=True, env=env, cwd=SIM, timeout=600)
    out = r.stdout + r.stderr
    open(f"{SIM}/run.{name}.out", 'w', encoding='utf-8').write(out)
    m = re.search(r'^\s*(\d+) passed, (\d+) failed\s*$', out, re.M)
    passed, failed = (int(m.group(1)), int(m.group(2))) if m else (-1, -1)
    reds = re.findall(r'^\s*FAIL (.+)$', out, re.M)
    results[name] = (passed, failed, reds, r.returncode)
    p, f, preds = PRED[name]
    tally_ok = (passed, failed) == (p, f) and r.returncode == (0 if f == 0 else 1)
    reds_ok = len(reds) == len(preds) and all(any(pr in rd for rd in reds) for pr in preds)
    tag = "EXACT" if (tally_ok and reds_ok) else "MISPREDICTED"
    ck(tally_ok and reds_ok, f"{name:24s} {passed} passed, {failed} failed rc={r.returncode} ({(datetime.datetime.now()-t0).seconds}s) — {tag}; reds: {[x[:70] for x in reds]}")
# the hook copies are unchanged by the runs (the suite copies the hook into each fixture; it never writes back)
ck(sha(HOOK_HEAD) == '92abd8e9b30e8d19' and sha(HOOK_DEV) == 'cc940299b2aec733' and sha(HOOK_BASE) == '57b046fed04ca492', "the three hook copies are sha-identical after the runs")
ck(sha(TEST) == '6dabbb516e92e5cf', "the test file copy is sha-identical after the runs")
print(f"\nwork dir (kept): {SIM}")
print(f"guards_sim: FAILS={fails}")
print("done at", datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
sys.exit(1 if fails else 0)
