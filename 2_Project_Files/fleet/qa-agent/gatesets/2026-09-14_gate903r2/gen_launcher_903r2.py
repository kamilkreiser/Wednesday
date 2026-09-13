#!/usr/bin/env python3
"""gen_launcher_903r2.py — derive launch_qa_secuura_ks991_903_r2.sh from the INSTALLED #980 ROUND-2 launcher (the newest tier-2
round-2 template: the DISJOINTNESS-CHECKED develop pin, the exit-19 round-1-report guard, the exit-20 head-SHA-in-both guard;
sha256 200c7dfba7871b06) by ASSERTED substitutions (every anchor must occur exactly as often as stated, or the generator refuses),
then a RESIDUAL GUARD: any token of the source gate (its PR number, tickets, heads, merge-base, develop pin, env-override prefix,
guarded paths, M-numbers, ratio) left anywhere in the output is a refusal — nothing is written on refusal.

Differences from the template, all asserted: the pins (#903 / KS-991 / a4f71cde6 / merge-base = develop = M18 8861e6216); the
GUARDED list for THIS gate = the three PR files (.githooks/pre-push, the test file, preflight.sh) + deps-present.sh (leg 1's
precondition, the env_fail arm) + run-shell-suites.sh (leg 14 / CI step 11's runner) + the `Blockchain/Dev/scripts/__tests__/`
prefix (the 29-suite corpus — anything there moves the leg-14 count); the exit-19 guard KEPT and re-pointed: round 1 of #903 is
Peter's review comment 5585854866 (there is NO QA report for #903 — the s161 batch is #929/#928/#925/#924/#927/#926), saved
read-only by s213 in its boot/ dir; a NEW exit-21 guard — the launcher REFUSES when stdin is not a TTY on the launch path
(--check still works headless), carried from the #982 launcher (2026-09-13 ledger).

Usage: gen_launcher_903r2.py <template launcher> <output launcher>
Exit: 0 written · 1 an anchor count disagreed · 2 a residual token survived · 3 an output control failed
"""
import os, sys, hashlib

src_path, out_path = sys.argv[1], sys.argv[2]
raw = open(src_path, 'rb').read()
assert hashlib.sha256(raw).hexdigest()[:16] == '200c7dfba7871b06', 'template sha256 is not the installed #980 r2 launcher'
s = raw.decode('utf-8')

NEW_HEADER = """#!/bin/bash
# launch_qa_secuura_ks991_903_r2.sh — cross-project QA agent, TIER 2 (through code: a shell test file for the pre-push hook's
# base resolution — no service, route, spec, schema or UI) DELTA gate, ROUND 2, on Secuura PR #903 (KS-991) @ a4f71cde6 —
# FOUR commits, all on origin develop's M18 8861e6216 by merge: the two reviewed commits d4a596f35 + a70f92d7c (the KS-991 guard in
# .githooks/pre-push and the env_fail arm in preflight.sh; base 986c592d5 then), the merge commit 48553f272 (develop 8861e6216
# merged IN, --no-ff, clean, tree 2e6d92d16 = s213's merge-tree prediction) and the round-2 fix commit a4f71cde6 (parent 48553f272,
# tree 5d4023647, +123 -1, ONE file, ONE hunk @@ -504,11 +504,133 @@: CASE 10 + CASE 11 in
# Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh, blob d95af6514 -> affdf027b, 524 -> 646 lines, sha256
# 48ada0c361efcc3c -> 6dabbb516e92e5cf). PR files API vs develop: 3 files +186 -2 (hook +39 -1, test +123 -1, preflight.sh +24 -0).
#
# Why a round 2: round 1 was PETER's review (PR comment 5585854866, 2026-09-08 13:25Z — "Not approving yet — solely on the missing
# regression case"): the KS-991 change edits the block pre_push_hook_base.test.sh guards and added no case, so the property lived
# only in the PR description. His ONE ask: two committed cases (his "CASE 7/8" against the 6-case file at 986c592d5). s214 delivered
# them as CASE 10 (stale strict-ancestor local develop + docs-only branch -> SKIPS and says KS-991) and CASE 11 (same stale develop +
# a real Blockchain/Dev change -> still RUNS), red-first against develop's hook f0748ed56 (26/2) and the merge base's aae2743ac
# (23/5), green at the head's 1b22d4e14 (28/0) — Wednesday's drafter re-derived all six rows + three gate-designed tampers EXACT
# on git-show copies (gate903r2/guards_sim.out).
#
# Round 2 re-gates: (1) the delta is EXACTLY the fix commit (one file, one hunk) on a CLEAN develop merge — hook + preflight.sh
# blob-identical between 48553f272 and a4f71cde6; the merge vs develop = the reviewed delta (39/1 + 24/0); (2) the RED-FIRST pair
# re-derived in the gate's own clone: develop's hook blob -> 26/2 (CASE 10's two behaviour cells), the head's -> 28/0, the merge
# base's -> 23/5; (3) the tamper table with the suite running (T1 revert / T2 unconditional / T3 token, + Tg-A direction-inverted
# 25/3, Tg-B `!=` dropped 28/0 — the suite is BLIND to that clause, a Record — and Tg-E ancestor:=true 27/1); (4) Peter's five
# notes answered as the ticket comment e1e526bc says; (5) CI at the head ATTRIBUTED, never graded (step 11's two reds are develop's
# own — KS-1138 + KS-1148; step 7's npm-audit red is KS-1075/KS-1077's; the `pr` workflow's Playwright red is develop's own too);
# (6) delivered-vs-commissioned against the s214 brief ITEM 1 (overlaying s213 §2) and Peter's ask; findings-only; NOT-TESTED.
#
# Merge-base = origin develop M18 8861e6216 (develop was merged INTO the branch, so GitHub compare develop...head: ahead 4 /
# behind 0 — exit 10 if it changes). origin develop = M18 8861e6216 (12:00:26Z 2026-09-13; read 07:56 and 08:03 AEST 2026-09-14).
# The develop pin below is DISJOINTNESS-CHECKED, not bare: if origin develop has moved past M18, the GitHub compare of that delta is
# read and the launcher REFUSES (exit 18) only when the delta touches a GUARDED path — the three PR files, deps-present.sh,
# run-shell-suites.sh, or anything under Blockchain/Dev/scripts/__tests__/ (the 29-suite leg-14 count moves) — or cannot be judged
# (unreadable, not ahead, >250 files); otherwise it proceeds printing the move and its file count, which the gate re-states (brief
# items 1 and 6). A refusal means: confirm the new delta, then re-pin DEVELOP_SHA here AND in the brief's TARGET section AND the
# prompt — a different brief, a deliberate edit. #918 and #925 both touch preflight.sh: either merging first fires exit 18.
#
# NEW in this launcher (exit 21): the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it
# in a cockpit pane, never inside a Bash tool — a gate launched there runs headless, invisible to Kam, and dies with the caller's
# shell (2026-09-13 ledger). `--check` still runs headless (it launches nothing).
#
# Adapted from the #980 round-2 launcher by gen_launcher_903r2.py (asserted substitutions, residual guard): the same guard family
# and exit codes 2..21 (exit 19 = the round-1 record named AND on disk — here Peter's saved review, not a QA report; exit 20 = the
# full head SHA in both brief and prompt; exit 21 = stdin not a TTY on the launch path).
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks991_903_r2.sh [--check]
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
NEW_GUARDED = '''GUARDED = [".githooks/pre-push",
           "Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh",
           "Blockchain/Dev/scripts/preflight/preflight.sh",
           "Blockchain/Dev/scripts/preflight/deps-present.sh",
           "Blockchain/Dev/scripts/run-shell-suites.sh",
           "Blockchain/Dev/scripts/__tests__/"]
'''
OLD_R1 = '''R1_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-13-ks924-901-980-9c620f890-tier2-r1/report.md'
grep -qF "$R1_REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the round-1 report path (a gate cannot ask)" >&2; exit 19; }
[ -s "$R1_REPORT" ] || { echo "REFUSING: the round-1 report named by the brief is missing or empty: $R1_REPORT" >&2; exit 19; }
'''
NEW_R1 = '''R1_REPORT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-13_s213/boot/peter_903_comment_5585854866.md'
grep -qF "$R1_REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the round-1 record path (Peter's review; a gate cannot ask)" >&2; exit 19; }
[ -s "$R1_REPORT" ] || { echo "REFUSING: the round-1 record named by the brief is missing or empty: $R1_REPORT" >&2; exit 19; }
'''
OLD_TAIL = '''[ -z "${QA980R2_BRIEF:-}${QA980R2_PROMPT:-}${QA980R2_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
'''
NEW_TAIL = '''[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QA903R2_BRIEF:-}${QA903R2_PROMPT:-}${QA903R2_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
'''
subs = [
    (OLD_R1, NEW_R1, 1),                  # the round-1 record guard re-pointed (Peter's saved review)
    (OLD_TAIL, NEW_TAIL, 1),              # the TTY guard arrives, the override guard is re-prefixed
    ("QA980R2_BRIEF", "QA903R2_BRIEF", 1),
    ("QA980R2_PROMPT", "QA903R2_PROMPT", 1),
    ("QA980R2_HEAD", "QA903R2_HEAD", 1),
    ("2026-09-13_secuura-980-ks924-901-tier2-r2", "2026-09-14_secuura-903-ks991-tier2-r2", 3),
    ("refs/heads/feature/ks-924-ks-901-entrypoint-corpus-presence-set-and-three-shapes",
     "refs/heads/kamilkreiser/ks-991-stale-local-develop", 1),
    ("103c235b4d2be54cc1ade65ed660f397cf03e997", "a4f71cde660c1442d98317e26d93845340b20098", 1),
    ("MERGE_BASE='50b729d69c58474624508ed79d05c520dab22cc6'", "MERGE_BASE='8861e62161466c40f08d2b10a30edeb203123993'", 1),
    ("DEVELOP_SHA='1c38077ba2aea5f4c4371c1b68796026dc577764'", "DEVELOP_SHA='8861e62161466c40f08d2b10a30edeb203123993'", 1),
    (OLD_GUARDED, NEW_GUARDED, 1),
    ('DEV_NOTE="origin develop still $DEVELOP_SHA (M15, the develop this brief\'s 813/813 was written against; git ls-remote)"',
     'DEV_NOTE="origin develop still $DEVELOP_SHA (M18, the develop merged INTO the branch and the one this brief\'s 28/0 was written against; git ls-remote)"', 1),
    ('DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#DISJOINT } — disjoint from the guard\'s three paths (#980\'s file, the ks860 loopback guard file, the packages/shared/ prefix); the gate merges the then-current develop, re-states the delta by name and re-derives the ratio (brief items 1 and 2)"',
     'DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#DISJOINT } — disjoint from the guard\'s six paths (#903\'s three files, deps-present.sh, run-shell-suites.sh, the scripts/__tests__/ prefix); the gate merges the then-current develop, re-states the delta by name and re-derives the leg-14 count (brief items 1 and 6)"', 1),
    ('  echo "  brief names the round-1 report and it is present on disk"\n',
     '  echo "  brief names the round-1 record (Peter\'s review) and it is present on disk"\n  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"\n', 1),
]
for old, new, n in subs:
    c = s.count(old)
    if c != n:
        print(f"REFUSING: anchor {old[:70]!r} occurs {c} times, expected {n}", file=sys.stderr)
        sys.exit(1)
    s = s.replace(old, new)

# 3. Residual guard — nothing of the source gate may survive (outside the exact header sentence naming the template).
RESIDUAL = ["980", "924", "901", "103c235b4", "9c620f890", "50b729d69", "1c38077ba", "6b62ae446", "3370ef661", "QA980R2",
            "entrypoint-corpus", 'packages/shared/"', "813", "M15", "M9 ", "s210", "GF-1", "KS-1142", "three paths",
            "d81265b7f", "e232b0289", "068aa3d0f", "977", "877", "loopback", "ks860", "P3", "corpus"]
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
    ("a4f71cde660c1442d98317e26d93845340b20098", 1), ("8861e62161466c40f08d2b10a30edeb203123993", 2), ("a4f71cde6", 4), ("8861e6216", 6),
    ("QA903R2_BRIEF", 2), ("QA903R2_PROMPT", 2), ("QA903R2_HEAD", 2),
    ("2026-09-14_secuura-903-ks991-tier2-r2.md", 2), ("2026-09-14_secuura-903-ks991-tier2-r2.prompt.txt", 1),
    ("refs/heads/kamilkreiser/ks-991-stale-local-develop", 1),
    ("exit 21", 4), ("exit 20", 2), ("exit 19", 3), ("exit 18", 4), ("exit 10", 2), ("exit 6", 1), ("exit 13", 1), ("exit 16", 2), ("exit 7", 1), ("exit 15", 1), ("exit 9", 1),
    ("exit 8", 1), ("exit 11", 1), ("exit 12", 1), ("exit 14", 1), ("exit 17", 1), ("exit 2;", 1), ("exit 3;", 1), ("exit 4;", 1), ("exit 5;", 1),
    ("'TIER 2'", 2), ("'ROUND 2'", 2), ("[ -t 0 ]", 1), ("stdin is not a TTY", 2),
    ('".githooks/pre-push"', 1), ("pre_push_hook_base.test.sh", 3), ('"Blockchain/Dev/scripts/preflight/preflight.sh"', 1), ("deps-present.sh", 3),
    ("run-shell-suites.sh", 3), ('"Blockchain/Dev/scripts/__tests__/"', 1), ("GUARDED", 5),
    ("peter_903_comment_5585854866.md", 1), ("R1_REPORT", 4), ("5585854866", 2),
    ("MAIL YOUR VERDICT", 1), ("no memory maintenance", 1), ("NEVER print a credential value", 1), ("ultrathink", 1),
    ("exec claude --dangerously-skip-permissions --model opus", 1), ('cd "$QA_DIR"', 1),
    ("brief and prompt both name the head SHA", 1), ("brief and prompt agree on TIER 2 and ROUND 2", 1), ("a launch (not --check) will refuse unless stdin is a TTY", 1),
    ('g.endswith("/") and f["filename"].startswith(g)', 1), ("six paths", 1), ("M18", 5), ("28/0", 4), ("26/2", 2), ("23/5", 2), ("KS-991", 4), ("#903", 2), ("#918", 1), ("#925", 1),
    ("KS-1138", 1), ("KS-1148", 1), ("KS-1075", 1), ("KS-1077", 1), ("CASE 10", 3), ("CASE 11", 2), ("s214", 2), ("s213", 3),
]
for tok, n in CONTROLS:
    c = s.count(tok)
    if c != n:
        print(f"REFUSING: output control {tok!r} occurs {c} times, expected {n}", file=sys.stderr)
        sys.exit(3)
# the TTY guard must sit AFTER the --check block and BEFORE the override guard / cd / exec; the R1 guard BEFORE the --check block
i_r1 = s.index("R1_REPORT='"); i_check = s.index('if [ "${1:-}" = "--check" ]; then'); i_tty = s.index('[ -t 0 ]'); i_ovr = s.index('a launch with test overrides set'); i_cd = s.index('cd "$QA_DIR"')
assert i_r1 < i_check < i_tty < i_ovr < i_cd, "guard positions"
# no raw control byte
b = s.encode("utf-8")
assert not [i for i, x in enumerate(b) if (x < 0x20 and x not in (9, 10, 13)) or x == 0x7f], "raw control byte in output"

open(out_path, "w", encoding="utf-8").write(s)
os.chmod(out_path, 0o755)
print(f"written {out_path} ({len(b)} bytes); {len(subs)} substitutions asserted; residual guard clean ({len(RESIDUAL)} tokens); {len(CONTROLS)} output controls")
