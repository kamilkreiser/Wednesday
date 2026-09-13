#!/usr/bin/env python3
"""gen_launcher_982.py — derive launch_qa_secuura_ks790_982.sh from the INSTALLED #980 ROUND-2 launcher (the newest template
carrying the DISJOINTNESS-CHECKED develop pin and the exit-20 head-SHA-in-both guard; sha256 200c7dfba7871b06) by ASSERTED
substitutions (every anchor must occur exactly as often as stated, or the generator refuses), then a RESIDUAL GUARD: any token
of the source gate (its PR number, tickets, heads, merge-base, develop pin, env-override prefix, guarded paths, M-numbers,
round-1-report guard) left anywhere in the output is a refusal — nothing is written on refusal.

Differences from the template, all asserted: ROUND 1 (the exit-19 round-1-report guard REMOVED — there is no round 1 to
name; the exit-15 guard now reads 'ROUND 1'); TIER 1; a NEW exit-21 guard — the launcher REFUSES when stdin is not a TTY on
the launch path (--check still works headless): a gate launched inside a Bash tool runs headless, invisible and parented to
the caller (2026-09-13 ledger, "guard candidate: every QA launcher refuses when stdin is not a TTY"). The GUARDED list for
THIS gate = the three PR files + the `Blockchain/Dev/services/auth/` prefix (anything there moves the 691 ratio) + the ks860
loopback guard file (the widened-guard rule) + migrations/039_rls_fail_closed.sql (the carve-out's definition).

Usage: gen_launcher_982.py <template launcher> <output launcher>
Exit: 0 written · 1 an anchor count disagreed · 2 a residual token survived · 3 an output control failed
"""
import os, sys

src_path, out_path = sys.argv[1], sys.argv[2]
s = open(src_path, encoding="utf-8").read()

NEW_HEADER = """#!/bin/bash
# launch_qa_secuura_ks790_982.sh — cross-project QA agent, TIER 1 (through code AND live where a surface exists: the OAuth
# token grants — an auth door) gate, ROUND 1, on Secuura PR #982 (KS-790) @ e62eab87a — ONE commit on origin develop M18
# 8861e6216 (= the merge-base = the PR's parent; compare ahead 1 / behind 0), THREE files +280 -5: routes/oauth.ts (+23 -5;
# the CODE delta is -4/+3 — `:29` import { generateTokenPair, verifyRefreshToken }; `:808` and `:867` userRepo.getUserById
# -> userRepo.getUserByIdPreAuth at the authorization_code and refresh grants of POST /api/oauth/token; develop's `:832`
# in-handler require('../services/jwt') removed; 20 comment lines; blob 4b03f555e -> 80e05458e), NEW
# __tests__/ks790-token-pre-auth-user-lookup.test.ts (249 lines, cfed82d54, raw socket, listen(0, '127.0.0.1'), 6 cells) and
# ONE 8-line hunk in __tests__/ks820-821-token-client-auth-and-apptype.test.ts (a getUserByIdPreAuth mock entry — taken on
# the 15-minute fallback, ACCEPTED by Wednesday 2026-09-14; the gate verifies it is the ONE hunk and that it is load-bearing).
#
# WHY TIER 1, stated here so this file and the brief cannot drift apart: on SHAPE the change is two one-token swaps and an
# import — a tier 2. It is tier 1 because of what it REACHES: /token is the door that turns an authorization code or a
# refresh token into a full token pair, and on every fail-closed-RLS deployment (migration 039, a NOBYPASSRLS role, no tenant
# GUC on a bearer-less request) that door has been shut by accident — the plain RLS-scoped lookup read ZERO rows and the
# handler answered 400 invalid_grant "User not found" for EVERY code. The swap OPENS it; everything downstream of the lookup
# runs for the first time under 039 once this merges (Wednesday's ruling 3: all four PRs of the lane are tier 1). A tier keyed
# on the shape of a change is blind to what the change reaches.
#
# The gate establishes: (1) the delta is exactly the three files / four oauth.ts hunks / one ks820 hunk; (2) red-first both ways
# (4 failed | 2 passed (6) at develop's oauth.ts; 6/6, 19/19, 51 files / 691 at head; develop alone 50 / 685); (3) the product
# path over REAL HTTP through the real router at BOTH SHAs — LIVE on a 039 database if the docker daemon is already up
# (qa982-* only; never started by the gate), else stub-modelled with the REAL userRepo + jwt and the blocker named; (4) the
# tamper table with the suite running (T1, T2, T3d/T3b, T4, T5, T6, Tk); (5) the ks781 authorize-side gates still in front of
# the door; (6) the merged shape + the widened-guard rule (packages/shared green; the ks860 loopback cell reads the new file);
# (7) the enabling change at the BUILT artefact (tsc both trees, diff oauth.js); (8) delivered-vs-commissioned; (9) three
# pre-existing Records measured, not graded; findings-only; NOT TESTED at equal prominence. #982 is the BASE of the stack
# #982 -> #983 -> #984; the PRED line says it merges FIRST.
#
# Merge-base = the PR's parent M18 8861e6216 (GitHub compare develop...head: ahead 1 / behind 0 — exit 10 if it changes).
# origin develop = M18 8861e6216 (the last squash of 2026-09-13, 12:00:26Z; read 07:08 AEST 2026-09-14). The develop pin below is
# DISJOINTNESS-CHECKED, not bare: if origin develop has moved past M18, the GitHub compare of that delta is read and the
# launcher REFUSES (exit 18) only when the delta touches a GUARDED path — the three PR files, anything under
# Blockchain/Dev/services/auth/ (the 691 ratio moves), the ks860 loopback guard file, or migrations/039_rls_fail_closed.sql
# — or cannot be judged (unreadable, not ahead, >250 files); otherwise it proceeds printing the move and its file count,
# which the gate re-states (brief items 1 and 6). A refusal means: confirm the new delta, then re-pin DEVELOP_SHA here AND in
# the brief's TARGET section AND the prompt — a different brief, a deliberate edit.
#
# NEW in this launcher (exit 21): the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent;
# run it in a cockpit pane, never inside a Bash tool — a gate launched there runs headless, invisible to Kam, and dies with
# the caller's shell (2026-09-13 ledger). `--check` still runs headless (it launches nothing).
#
# Adapted from the #980 round-2 launcher by gen_launcher_982.py (asserted substitutions, residual guard): the same guard
# family and exit codes 2..18, 20, 21 (code 19 — the template's round-1-report guard — is not carried: this is a ROUND 1).
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks790_982.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..21 a guard refused
"""

# 1. Replace the header (everything before `set -u`) wholesale.
marker = "set -u\n"
assert s.count(marker) == 1, "header marker"
s = NEW_HEADER + s[s.index(marker):]

# 2. Asserted substitutions: (old, new, expected count in the post-header text).
OLD_GUARDED = '''GUARDED = ["Blockchain/Dev/packages/shared/src/__tests__/entrypoint-corpus.test.ts",
           "Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts",
           "Blockchain/Dev/packages/shared/"]
'''
NEW_GUARDED = '''GUARDED = ["Blockchain/Dev/services/auth/src/routes/oauth.ts",
           "Blockchain/Dev/services/auth/src/__tests__/ks790-token-pre-auth-user-lookup.test.ts",
           "Blockchain/Dev/services/auth/src/__tests__/ks820-821-token-client-auth-and-apptype.test.ts",
           "Blockchain/Dev/services/auth/",
           "Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts",
           "Blockchain/Dev/migrations/039_rls_fail_closed.sql"]
'''
OLD_R1 = '''R1_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-13-ks924-901-980-9c620f890-tier2-r1/report.md'
grep -qF "$R1_REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the round-1 report path (a gate cannot ask)" >&2; exit 19; }
[ -s "$R1_REPORT" ] || { echo "REFUSING: the round-1 report named by the brief is missing or empty: $R1_REPORT" >&2; exit 19; }

'''
OLD_TAIL = '''[ -z "${QA980R2_BRIEF:-}${QA980R2_PROMPT:-}${QA980R2_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
'''
NEW_TAIL = '''[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QA982_BRIEF:-}${QA982_PROMPT:-}${QA982_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
'''
subs = [
    (OLD_R1, "", 1),                      # the round-1-report guard goes (ROUND 1)
    (OLD_TAIL, NEW_TAIL, 1),              # the TTY guard arrives, the override guard is re-prefixed
    ("QA980R2_BRIEF", "QA982_BRIEF", 1),   # the second occurrence was inside OLD_TAIL, replaced above
    ("QA980R2_PROMPT", "QA982_PROMPT", 1),
    ("QA980R2_HEAD", "QA982_HEAD", 1),
    ("2026-09-13_secuura-980-ks924-901-tier2-r2", "2026-09-14_secuura-982-ks790-tier1", 3),
    ("refs/heads/feature/ks-924-ks-901-entrypoint-corpus-presence-set-and-three-shapes",
     "refs/heads/feature/ks-790-oauth-authorization_code-token-exchange-uses-getuserbyid", 1),
    ("103c235b4d2be54cc1ade65ed660f397cf03e997", "e62eab87a6263e25c41c9bb814d5831842bb6c7e", 1),
    ("MERGE_BASE='50b729d69c58474624508ed79d05c520dab22cc6'", "MERGE_BASE='8861e62161466c40f08d2b10a30edeb203123993'", 1),
    ("DEVELOP_SHA='1c38077ba2aea5f4c4371c1b68796026dc577764'", "DEVELOP_SHA='8861e62161466c40f08d2b10a30edeb203123993'", 1),
    (OLD_GUARDED, NEW_GUARDED, 1),
    ('DEV_NOTE="origin develop still $DEVELOP_SHA (M15, the develop this brief\'s 813/813 was written against; git ls-remote)"',
     'DEV_NOTE="origin develop still $DEVELOP_SHA (M18, the PR\'s parent and the develop this brief\'s 51/691 was written against; git ls-remote)"', 1),
    ('DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#DISJOINT } — disjoint from the guard\'s three paths (#980\'s file, the ks860 loopback guard file, the packages/shared/ prefix); the gate merges the then-current develop, re-states the delta by name and re-derives the ratio (brief items 1 and 2)"',
     'DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#DISJOINT } — disjoint from the guard\'s six paths (#982\'s three files, the services/auth/ prefix, the ks860 loopback guard file, migration 039); the gate merges the then-current develop, re-states the delta by name and re-derives the ratio (brief items 1 and 6)"', 1),
    ("grep -q 'TIER 2' \"$BRIEF\" && grep -q 'TIER 2' \"$PROMPT_FILE\"", "grep -q 'TIER 1' \"$BRIEF\" && grep -q 'TIER 1' \"$PROMPT_FILE\"", 1),
    ("grep -q 'ROUND 2' \"$BRIEF\" && grep -q 'ROUND 2' \"$PROMPT_FILE\"", "grep -q 'ROUND 1' \"$BRIEF\" && grep -q 'ROUND 1' \"$PROMPT_FILE\"", 1),
    ('echo "  brief and prompt agree on TIER 2 and ROUND 2"', 'echo "  brief and prompt agree on TIER 1 and ROUND 1"', 1),
    ('  echo "  brief names the round-1 report and it is present on disk"\n', '  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"\n', 1),
]
for old, new, n in subs:
    c = s.count(old)
    if c != n:
        print(f"REFUSING: anchor {old[:70]!r} occurs {c} times, expected {n}", file=sys.stderr)
        sys.exit(1)
    s = s.replace(old, new)

# 3. Residual guard — nothing of the source gate may survive (outside the exact header sentence naming the template).
RESIDUAL = ["980", "924", "901", "103c235b4", "9c620f890", "50b729d69", "1c38077ba", "6b62ae446", "3370ef661", "QA980R2",
            "entrypoint-corpus", 'packages/shared/"', "813", "M15", "M9 ", "s210", "GF-1", "KS-1142", "three paths", "R1_REPORT",
            "round-1 report", "exit 19", "round-1-report guard\" ", "d81265b7f", "e232b0289", "068aa3d0f", "TIER 2", "ROUND 2", "tier2", "r2", "977", "877"]
PERMITTED = ["Adapted from the #980 round-2 launcher"]
body = s
for p in PERMITTED:
    assert body.count(p) == 1, f"permitted phrase count: {p!r}"
    body = body.replace(p, "")
for i, line in enumerate(body.splitlines(), 1):
    for t in RESIDUAL:
        if t in line:
            print(f"REFUSING: residual token {t!r} at line {i}: {line.strip()[:120]}", file=sys.stderr)
            sys.exit(2)

# 4. Output controls — every load-bearing token present the stated number of times.
CONTROLS = [
    ("e62eab87a6263e25c41c9bb814d5831842bb6c7e", 1), ("8861e62161466c40f08d2b10a30edeb203123993", 2), ("e62eab87a", 2), ("8861e6216", 5),
    ("QA982_BRIEF", 2), ("QA982_PROMPT", 2), ("QA982_HEAD", 2),
    ("2026-09-14_secuura-982-ks790-tier1.md", 2), ("2026-09-14_secuura-982-ks790-tier1.prompt.txt", 1),
    ("refs/heads/feature/ks-790-oauth-authorization_code-token-exchange-uses-getuserbyid", 1),
    ("exit 21", 3), ("exit 20", 1), ("exit 18", 3), ("exit 10", 2), ("exit 6", 1), ("exit 13", 1), ("exit 16", 2), ("exit 7", 1), ("exit 15", 1), ("exit 9", 1),
    ("exit 8", 1), ("exit 11", 1), ("exit 12", 1), ("exit 14", 1), ("exit 17", 1), ("exit 2;", 1), ("exit 3;", 1), ("exit 4;", 1), ("exit 5;", 1),
    ("'TIER 1'", 2), ("'ROUND 1'", 2), ("[ -t 0 ]", 1), ("stdin is not a TTY", 2),
    ("Blockchain/Dev/services/auth/src/routes/oauth.ts", 1), ("ks790-token-pre-auth-user-lookup.test.ts", 2), ("ks820-821-token-client-auth-and-apptype.test.ts", 2),
    ('"Blockchain/Dev/services/auth/"', 1), ("ks860-test-listeners-bind-loopback.test.ts", 1), ("039_rls_fail_closed.sql", 2), ("GUARDED", 5),
    ("MAIL YOUR VERDICT", 1), ("no memory maintenance", 1), ("NEVER print a credential value", 1), ("ultrathink", 1),
    ("exec claude --dangerously-skip-permissions --model opus", 1), ('cd "$QA_DIR"', 1),
    ("brief and prompt both name the head SHA", 1), ("brief and prompt agree on TIER 1 and ROUND 1", 1), ("a launch (not --check) will refuse unless stdin is a TTY", 1),
    ('g.endswith("/") and f["filename"].startswith(g)', 1), ("six paths", 1), ("M18", 5), ("691", 3), ("getUserByIdPreAuth", 2), ("qa982-", 1), ("KS-790", 1), ("#983", 1), ("#984", 1),
    ("R1_REPORT", 0), ("exit 19", 0),
]
for tok, n in CONTROLS:
    c = s.count(tok)
    if c != n:
        print(f"REFUSING: output control {tok!r} occurs {c} times, expected {n}", file=sys.stderr)
        sys.exit(3)
# the TTY guard must sit AFTER the --check block and BEFORE the override guard / cd / exec
i_check = s.index('if [ "${1:-}" = "--check" ]; then'); i_tty = s.index('[ -t 0 ]'); i_ovr = s.index('a launch with test overrides set'); i_cd = s.index('cd "$QA_DIR"')
assert i_check < i_tty < i_ovr < i_cd, "TTY guard position"
# no raw control byte
b = s.encode("utf-8")
assert not [i for i, x in enumerate(b) if (x < 0x20 and x not in (9, 10, 13)) or x == 0x7f], "raw control byte in output"

open(out_path, "w", encoding="utf-8").write(s)
os.chmod(out_path, 0o755)
print(f"written {out_path} ({len(b)} bytes); {len(subs)} substitutions asserted; residual guard clean ({len(RESIDUAL)} tokens); {len(CONTROLS)} output controls")
