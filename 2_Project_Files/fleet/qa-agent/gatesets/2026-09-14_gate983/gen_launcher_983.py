#!/usr/bin/env python3
"""gen_launcher_983.py — derive launch_qa_secuura_ks823_983.sh from the INSTALLED #980 round-2 launcher
(launchers/launch_qa_secuura_ks924_901_980_r2.sh, sha256 200c7dfba7871b06… — the newest carrying the DISJOINTNESS-CHECKED
develop pin, the env-override test seam, the exit-20 head-SHA-in-both guard) by ASSERTED substitutions (every anchor must
occur exactly as often as stated, or the generator refuses), THREE asserted insertions (the STACK-PARENT pin at exit 21 —
#983 is stacked on #982's head, so a moved parent is a different gate; the no-TTY refusal at exit 22 — a QA launcher run
inside a Bash tool execs an interactive agent headless (2026-09-13 ledger, Wednesday's own instance); the parent line in
the --check output), ONE asserted removal (the round-2 R1_REPORT guard, exit 19 — this is round 1), then a RESIDUAL GUARD:
any token of the source gate (its PR, tickets, heads, merge-base, develop pin, env prefix, its guarded paths, its
M-numbers, its counts) left anywhere in the output is a refusal — nothing is written on refusal. Same method as
gen_launcher_980r2.py / gen_launcher_977r2.py.

GUARDED for THIS gate = the whole services/auth tree (any squash there moves the 702 ratio and may touch the lane's
files — routes/oauth.ts, services/jwt.ts, the three tests, plus the sibling routes/auth.ts, services/oauth.ts,
types/index.ts, userRepo.ts the gate reads as neighbours), the ks860 loopback guard in packages/shared (the widened-guard
rule: it walks services/auth/src/__tests__), the two api-gateway middleware files (#984's, the consumers of the token
claims), and the root lockfile (the farm). NOTE: #982's own squash onto develop WILL hit routes/oauth.ts -> exit 18 -> that
is the ruled merge order arriving, not a fault: Wednesday re-pins DEVELOP_SHA and the brief's "merged shape" item becomes
a real three-way merge (the brief says so in TARGET and item 2).

Usage: gen_launcher_983.py <template launcher> <output launcher>
Exit: 0 written · 1 an anchor count disagreed · 2 a residual token survived · 3 an output control failed
"""
import os, sys

src_path, out_path = sys.argv[1], sys.argv[2]
s = open(src_path, encoding="utf-8").read()

NEW_HEADER = """#!/bin/bash
# launch_qa_secuura_ks823_983.sh — cross-project QA agent, TIER 1 (a security surface: the OAuth token endpoint's
# refresh_token grant — client authentication + a client_id binding claim on OAuth-minted token pairs; through code AND
# live over a real Express app on a loopback port in the gate's OWN by-SHA clone, the s128 precedent) gate ROUND 1 on
# Secuura PR #983 (KS-823) @ f62c975c1 — STACKED on PR #982 (KS-790) @ e62eab87a, both on origin develop M18 8861e6216
# (merge-base = M18; develop...head: ahead 2 / behind 0 / 5 files; this PR's OWN delta = `git diff e62eab87a f62c975c1`
# = 4 files +395 -22: routes/oauth.ts +82 -10, services/jwt.ts +31 -10, NEW ks823-refresh-grant-client-auth-and-binding
# .test.ts +276, ks790-token-pre-auth-user-lookup.test.ts +6 -2 (its refresh cases now present the client credential and
# a bound stub token; its 17 expect( lines byte-identical)). Head tree db10aea98; the commit was AMENDED once before the push
# (1a26eb795 -> f62c975c1, tree identical — a foreign ticket id removed from the message).
#
# What the gate establishes: (1) the DELTA onto its parent is exactly those 4 files (blob/diff/numstat) and the parent is
# still #982's head; (2) RED-FIRST — the new 11-cell suite against the PARENT's product reads `7 failed | 4 passed (11)`,
# every refusal cell answering 200 WITH A TOKEN, and 11/11 at head; (3) the refresh branch authenticates the client BEFORE
# the token is verified (readClientId -> getAppByClientId, is_active pinned -> verifyClientSecret -> verifyRefreshToken ->
# denylist -> binding -> user -> mint), measured over a raw socket with the real jwt.ts and by the gate's own shapes (body
# vs Basic, mismatched Basic userid, empty/array client_id, form-urlencoded, a deactivated PUBLIC app — the cell the null-app
# guard alone earns); (4) the tamper table with the suite RUNNING — the builder's T1..T4 re-run (T4 is a CRASH red: the
# guard deleted -> TypeError -> 500) plus the gate's non-crashing T4' and the jwt.ts half-tampers; (5) the FAIL-CLOSED arm
# (unbound tokens refused) — ACCEPTED by Wednesday for the gate; the deploy-time consequence is stated, not graded; (6) the
# MERGED shape onto the live develop (a fast-forward while develop is still M18: the merged tree == the head tree) with the
# full auth suite 52 files / 702 tests and the widened ks860 loopback guard GREEN on both new test files; (7) HUNT THE CLASS —
# the sibling POST /api/auth/refresh (routes/auth.ts:658-699, untouched, blob 132d3b8d3 at head AND develop) accepts any
# valid refresh token with no client and re-mints UNBOUND — measured, reported as pre-existing with a control at develop,
# never charged to #983 as a regression; (8) findings-only; board search by SYMBOL/path is Wednesday's; a NOT-TESTED list.
#
# Merge-base = M18 8861e6216 (GitHub compare develop...head; exit 10 if it changes). The STACK PARENT refs/pull/982/head
# must still read e62eab87a (exit 21) — a fix round on #982 makes this brief's delta and red-first about a different
# product. origin develop = M18 (read 07:08:53 AEST 2026-09-14 by ls-remote; unmoved since s212's READY). The develop pin
# below is DISJOINTNESS-CHECKED, not bare: if origin develop has moved past M18, the GitHub compare of that delta is read and
# the launcher REFUSES (exit 18) only when the delta touches a GUARDED path — anything under Blockchain/Dev/services/auth/
# (the 702 ratio and the lane's files), the ks860 loopback guard in packages/shared (it walks services/auth/src/__tests__),
# the api-gateway auth/scopes middleware (the claim consumers, #984's files) or the root lockfile — or cannot be judged
# (unreadable, not ahead, >250 files); otherwise it proceeds printing the move and its file count, which the gate re-states
# (brief items 1 and 2). #982's OWN squash onto develop hits routes/oauth.ts and is the ruled merge order arriving: exit 18
# then means "re-pin DEVELOP_SHA here AND in the brief's TARGET section AND the prompt, and item 2 is a real three-way merge".
#
# Refuses when stdin is not a TTY (exit 22) unless run with --check: this launcher execs an interactive agent; run inside a
# Bash tool it runs headless, invisible and parented to the caller's shell (2026-09-13, Wednesday's own #962 instance).
#
# Adapted from the INSTALLED #980 round-2 launcher by gen_launcher_983.py (asserted substitutions, three asserted insertions,
# one asserted removal, residual guard): same guard family and exit codes 2..18, 20 (the round-2 exit-19 report guard removed;
# exit 21 = the stack parent moved; exit 22 = no TTY), re-pointed at #983.
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks823_983.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..22 a guard refused
"""

# 1. The header: everything from the shebang to (not including) `set -u` is replaced whole.
i = s.index("\nset -u\n")
assert s.count("\nset -u\n") == 1
old_header = s[:i + 1]
assert "launch_qa_secuura_ks924_901_980_r2.sh — cross-project QA agent" in old_header
s = NEW_HEADER + s[i + 1:]

# 2. Asserted substitutions on the body (count must match exactly).
OLD_GUARDED = '''GUARDED = ["Blockchain/Dev/packages/shared/src/__tests__/entrypoint-corpus.test.ts",
           "Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts",
           "Blockchain/Dev/packages/shared/"]'''
NEW_GUARDED = '''GUARDED = ["Blockchain/Dev/services/auth/",
           "Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts",
           "Blockchain/Dev/services/api-gateway/src/middleware/auth.ts",
           "Blockchain/Dev/services/api-gateway/src/middleware/scopes.ts",
           "Blockchain/Dev/package-lock.json"]'''
subs = [
    ('BRIEF="${QA980R2_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-980-ks924-901-tier2-r2.md}"',
     'BRIEF="${QA983_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-983-ks823-tier1.md}"', 1),
    ('PROMPT_FILE="${QA980R2_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-980-ks924-901-tier2-r2.prompt.txt}"',
     'PROMPT_FILE="${QA983_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-983-ks823-tier1.prompt.txt}"', 1),
    ("BRANCH='refs/heads/feature/ks-924-ks-901-entrypoint-corpus-presence-set-and-three-shapes'",
     "BRANCH='refs/heads/feature/ks-823-security-the-apioauthtoken-refresh_token-grant-authenticates'", 1),
    ('HEAD_SHA="${QA980R2_HEAD:-103c235b4d2be54cc1ade65ed660f397cf03e997}"', 'HEAD_SHA="${QA983_HEAD:-f62c975c11ec97cdef04500fd98a43618e702763}"', 1),
    ("MERGE_BASE='50b729d69c58474624508ed79d05c520dab22cc6'", "MERGE_BASE='8861e62161466c40f08d2b10a30edeb203123993'\nSTACK_PARENT='e62eab87a6263e25c41c9bb814d5831842bb6c7e'\nSTACK_PARENT_REF='refs/pull/982/head'", 1),
    ("DEVELOP_SHA='1c38077ba2aea5f4c4371c1b68796026dc577764'", "DEVELOP_SHA='8861e62161466c40f08d2b10a30edeb203123993'", 1),
    ('REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-980-ks924-901-tier2-r2.md"',
     'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-983-ks823-tier1.md"', 1),
    (OLD_GUARDED, NEW_GUARDED, 1),
    ('DEV_NOTE="origin develop still $DEVELOP_SHA (M15, the develop this brief\'s 813/813 was written against; git ls-remote)"',
     'DEV_NOTE="origin develop still $DEVELOP_SHA (M18, the develop this brief\'s 52/702 and its fast-forward merged shape were written against; git ls-remote)"', 1),
    ('DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#DISJOINT } — disjoint from the guard\'s three paths (#980\'s file, the ks860 loopback guard file, the packages/shared/ prefix); the gate merges the then-current develop, re-states the delta by name and re-derives the ratio (brief items 1 and 2)"',
     'DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#DISJOINT } — disjoint from the guard\'s five paths (services/auth/, the ks860 loopback guard file, the two api-gateway middleware files, the root lockfile); the gate merges the then-current develop with a real three-way merge, re-states the delta by name and re-derives the auth ratio (brief items 1 and 2)"', 1),
    ("grep -q 'TIER 2' \"$BRIEF\" && grep -q 'TIER 2' \"$PROMPT_FILE\"", "grep -q 'TIER 1' \"$BRIEF\" && grep -q 'TIER 1' \"$PROMPT_FILE\"", 1),
    ("grep -q 'ROUND 2' \"$BRIEF\" && grep -q 'ROUND 2' \"$PROMPT_FILE\"", "grep -q 'ROUND 1' \"$BRIEF\" && grep -q 'ROUND 1' \"$PROMPT_FILE\"", 1),
    ('echo "  brief and prompt agree on TIER 2 and ROUND 2"', 'echo "  brief and prompt agree on TIER 1 and ROUND 1"', 1),
    ('[ -z "${QA980R2_BRIEF:-}${QA980R2_PROMPT:-}${QA980R2_HEAD:-}" ]', '[ -z "${QA983_BRIEF:-}${QA983_PROMPT:-}${QA983_HEAD:-}" ]', 1),
    ("REFUSING: brief or prompt does not name the head SHA $HEAD_SHA — a gate about another SHA is another gate", "REFUSING: brief or prompt does not name the head SHA $HEAD_SHA — a gate about another SHA is another gate", 1),  # identical: asserted present once
    ('echo "  merge-base still $MERGE_BASE (GitHub compare API)"', 'echo "  merge-base still $MERGE_BASE (GitHub compare API)"\n  echo "  stack parent $STACK_PARENT_REF still $STACK_PARENT on origin (this PR\'s delta and red-first are about that product)"', 1),
]
for old, new, n in subs:
    c = s.count(old)
    if c != n:
        print(f"REFUSING: anchor {old[:70]!r} occurs {c} times, expected {n}", file=sys.stderr)
        sys.exit(1)
    s = s.replace(old, new)

# 3. Asserted REMOVAL: the round-2 R1_REPORT guard block (exit 19) — this is round 1.
R1_BLOCK = """R1_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-13-ks924-901-980-9c620f890-tier2-r1/report.md'
grep -qF "$R1_REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the round-1 report path (a gate cannot ask)" >&2; exit 19; }
[ -s "$R1_REPORT" ] || { echo "REFUSING: the round-1 report named by the brief is missing or empty: $R1_REPORT" >&2; exit 19; }

"""
assert s.count(R1_BLOCK) == 1, "R1_REPORT block count"
s = s.replace(R1_BLOCK, "")
R1_ECHO = '  echo "  brief names the round-1 report and it is present on disk"\n'
assert s.count(R1_ECHO) == 1
s = s.replace(R1_ECHO, "")

# 4. Asserted INSERTIONS.
# 4a. The stack-parent pin, right after the head-at-branch guard (exit 6).
HEAD_GUARD_END = """  git -C "$REPO" ls-remote origin "$BRANCH" >&2
  exit 6
fi
"""
PARENT_GUARD = HEAD_GUARD_END + """
# THIS GATE'S OWN GUARD: #983 is STACKED on #982. The brief's delta (4 files +395 -22), its red-first (the 11 cells against
# the PARENT's product: 7 failed | 4 passed) and its "merge #982 first" instruction are all statements about e62eab87a.
# If #982 gets a fix round its head moves, and this brief describes a product that no longer exists at the parent ref.
if ! git -C "$REPO" ls-remote origin "$STACK_PARENT_REF" | grep -q "^${STACK_PARENT}[[:space:]]"; then
  echo "REFUSING: the stack parent $STACK_PARENT_REF is no longer $STACK_PARENT on origin — #982 moved; #983's delta and red-first are about a different product; rewrite the brief" >&2
  git -C "$REPO" ls-remote origin "$STACK_PARENT_REF" >&2
  exit 21
fi
"""
assert s.count(HEAD_GUARD_END) == 1
s = s.replace(HEAD_GUARD_END, PARENT_GUARD)
# 4b. The no-TTY refusal, immediately before the cd (after the override refusal, after the DEV_NOTE echo).
CD_LINE = 'cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }\n'
TTY_GUARD = """# A launch needs a terminal: this execs an interactive agent. Inside a Bash tool there is no TTY and the gate would run
# headless, invisible and parented to the caller's shell (2026-09-13 ledger). --check never reaches this line.
[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — launch this from a pane (cockpit.sh add), never from inside a Bash tool" >&2; exit 22; }
""" + CD_LINE
assert s.count(CD_LINE) == 1
s = s.replace(CD_LINE, TTY_GUARD)

# 5. Residual guard — nothing of the source gate may survive (outside the exact header sentence naming the template).
RESIDUAL = ["980", "924", "901", "103c235b4", "9c620f890", "50b729d69", "1c38077ba", "6b62ae446", "3370ef661", "QA980R2",
            "entrypoint-corpus", "packages/shared/\"", "M15", "M9", "M13", "M14", "813", "806", "812", "d81265b7f", "e232b0289",
            "068aa3d0f", "KS-1142", "GF-1", "s210", "s209", "three paths", "R1_REPORT", "exit 19", "round-1 report", "ROUND 2",
            "TIER 2", "fixture", "plant", "census", "listen(0", "P3", "H-a8", "#976", "#981", "#977", "r2", "delta gate",
            "T-P3", "T6", "T-860", "T-host", "shape A", "app.listen"]
PERMITTED = ["Adapted from the INSTALLED #980 round-2 launcher"]
body = s
for p in PERMITTED:
    assert body.count(p) == 1, f"permitted phrase count: {p!r}"
    body = body.replace(p, "")
for i, line in enumerate(body.splitlines(), 1):
    for t in RESIDUAL:
        if t in line:
            print(f"REFUSING: residual token {t!r} at line {i}: {line.strip()[:120]}", file=sys.stderr)
            sys.exit(2)

# 6. Output controls — every load-bearing token present the stated number of times.
if os.environ.get("GEN983_DUMP"): open(out_path + ".candidate", "w", encoding="utf-8").write(s)  # inspection only; never the deliverable
CONTROLS = [
    ("f62c975c11ec97cdef04500fd98a43618e702763", 1), ("e62eab87a6263e25c41c9bb814d5831842bb6c7e", 1), ("8861e62161466c40f08d2b10a30edeb203123993", 2),
    ("QA983_BRIEF", 2), ("QA983_PROMPT", 2), ("QA983_HEAD", 2), ("STACK_PARENT_REF", 5), ("STACK_PARENT", 9),
    ("2026-09-14_secuura-983-ks823-tier1.md", 2), ("2026-09-14_secuura-983-ks823-tier1.prompt.txt", 1),
    ("refs/heads/feature/ks-823-security-the-apioauthtoken-refresh_token-grant-authenticates", 1), ("refs/pull/982/head", 2),
    ("exit 22", 3), ("exit 21", 3), ("exit 20", 1), ("exit 18", 4), ("exit 10", 2), ("exit 6", 1), ("exit 13", 1), ("exit 16", 2), ("exit 7", 1), ("exit 15", 1), ("exit 9", 1), ("exit 8", 1), ("exit 12", 1), ("exit 11", 1), ("exit 14", 1), ("exit 17", 1),
    ("'TIER 1'", 2), ("'ROUND 1'", 2), ("Blockchain/Dev/services/auth/\"", 1), ("ks860-test-listeners-bind-loopback.test.ts", 1),
    ("Blockchain/Dev/services/api-gateway/src/middleware/auth.ts", 1), ("Blockchain/Dev/services/api-gateway/src/middleware/scopes.ts", 1), ("Blockchain/Dev/package-lock.json", 1),
    ("GUARDED", 5), ("MAIL YOUR VERDICT", 1), ("no memory maintenance", 1), ("NEVER print a credential value", 1), ("ultrathink", 1),
    ("exec claude --dangerously-skip-permissions --model opus", 1), ('cd "$QA_DIR"', 1), ("[ -t 0 ]", 1), ("--check", 5),
    ("brief and prompt both name the head SHA", 1), ("stack parent", 3), ('g.endswith("/") and f["filename"].startswith(g)', 1), ("five paths", 1),
    ("M18", 7), ("702", 4), ("7 failed | 4 passed (11)", 1), ("KS-823", 1), ("KS-790", 1), ("#982", 8), ("#983", 5), ("db10aea98", 1), ("1a26eb795", 1),
    ("routes/auth.ts:658-699", 1), ("fail-closed", 0), ("FAIL-CLOSED", 1), ("readClientId", 1), ("headless", 2), ("TTY", 4),
]
for tok, n in CONTROLS:
    c = s.count(tok)
    if c != n:
        print(f"REFUSING: output control {tok!r} occurs {c} times, expected {n}", file=sys.stderr)
        sys.exit(3)
# no raw control byte
b = s.encode("utf-8")
assert not [i for i, x in enumerate(b) if (x < 0x20 and x not in (9, 10, 13)) or x == 0x7f], "raw control byte in output"

open(out_path, "w", encoding="utf-8").write(s)
os.chmod(out_path, 0o755)
print(f"written {out_path} ({len(b)} bytes); header replaced; {len(subs)} substitutions asserted; 1 removal + 2 insertions asserted; residual guard clean ({len(RESIDUAL)} tokens); {len(CONTROLS)} output controls")
