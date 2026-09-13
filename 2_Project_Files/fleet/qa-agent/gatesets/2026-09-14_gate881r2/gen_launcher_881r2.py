#!/usr/bin/env python3
"""gen_launcher_881r2.py — derive launch_qa_secuura_ks798_841_799_881_r2.sh from the INSTALLED #980 ROUND-2 launcher
(the newest template carrying the DISJOINTNESS-CHECKED develop pin, the exit-19 round-1-read guard AND the exit-20
head-SHA-in-both guard) by ASSERTED substitutions (every anchor must occur exactly as often as stated, or the generator
refuses), ONE asserted INSERTION (the exit-21 TTY guard — a QA launcher execs an interactive agent and must never run
headless inside a Bash tool; 2026-09-13 ledger), then a RESIDUAL GUARD: any token of the source gate (its PR number,
tickets, heads, merge-base, develop pin, env-override prefix, its guarded paths, its M-numbers, its ratios) left anywhere
in the output is a refusal — nothing is written on refusal. Same method as gen_launcher_980r2.py / gen_launcher_977r2.py.

The GUARDED list for THIS gate = the six PR files by name + the `Blockchain/Dev/services/auth/` prefix (any develop
squash there moves the 703 ratio or the merge shape) + the four api-gateway files the live legs mount or read (csrf.ts,
specRouteMap.ts, index.ts, routes/proxy.ts) + the production nginx conf + the OpenAPI spec (the CSP/spec facts in the
brief) + the `Blockchain/Dev/packages/shared/src/__tests__/` prefix (the walking guards) + the root lockfile (the farm).

Usage: gen_launcher_881r2.py <template launcher> <output launcher>
Exit: 0 written · 1 an anchor count disagreed · 2 a residual token survived · 3 an output control failed
"""
import os, re, sys

src_path, out_path = sys.argv[1], sys.argv[2]
s = open(src_path, encoding="utf-8").read()

NEW_HEADER = """#!/bin/bash
# launch_qa_secuura_ks798_841_799_881_r2.sh — cross-project QA agent, TIER 1 (an auth surface: the OAuth consent page —
# a rendered page that authenticates a user and mints an authorization code; through code AND live in the gate's own
# Express apps: the product's real CSRF middleware, a real proxy front, jsdom driving the page) gate, ROUND 2 of the PR
# (round 1 was Peter Obeden's human review — CHANGES_REQUESTED on KS-799 only; there is NO round-1 QA report), on
# Secuura PR #881 (KS-798 / KS-841 / KS-799) @ 8ac9db66f — FIVE commits: Peter's head 787771b97 (3 commits, 2026-09-06)
# + the FIX ffcea35cb (parent 787771b97, tree 12dd42b2e, THREE files: oauth.ts +105 -57 blob 01c2d320f -> ffb573842,
# ks799-consent-script-csp-and-execution.test.ts NEW 414 lines blob 995ee34ce, ks799-consent-form-csrf-submit.test.ts
# +21 -10 blob 08803feb2 -> a83594c38) + the MERGE 8ac9db66f (parents ffcea35cb + origin develop M18 8861e6216, tree
# 136e6c8cc = `git merge-tree --write-tree 8861e6216 ffcea35cb` EXACTLY — the mechanical union; Wednesday's YES
# 13:33:35Z after the 09-07 branch's first push was refused by its own stale audit legs 6/7). PR files API: 6 files
# +1095 -24 vs develop (the three above + ks798-*, ks841-*, ks781-n1-* — Peter's signed-off bytes, blob-identical to
# 787771b97).
#
# Why a round 2: Peter measured that the round-1 inline <script> is refused by script-src 'self' as the browser sees it
# through the proxy (helmet on the auth service replaces the gateway's 'unsafe-inline' via http-proxy's setHeader), so
# the page fell back to the native headerless POST -> 403 CSRF_TOKEN_MISSING, the very symptom KS-799 exists to remove.
# s212 delivered Peter's option (2): the script bytes moved verbatim to CONSENT_SUBMIT_SCRIPT served by
# GET /api/oauth/consent.js (application/javascript, no-store) and the page carries <script src>; plus his "executing
# test" (jsdom clicks Authorize through the served script). No CSP header authored, no CSRF exemption, index.ts untouched.
#
# The gate establishes: (1) the delta is EXACTLY the three fix files and the merge is the union (tree-sha equality);
# (2) RED-FIRST in the gate's clone — the final test bytes against r1's oauth.ts red C1/C2/C4/the text cell
# `4 failed | 8 passed (12)` with C1 naming script-src 'self', head bytes 12/12, the five PR files 5/24/24, the auth suite
# 54/703 at head (= the merged tree on M18); (3) the tamper table suite RUNNING — T1/T2/T3 (3/3/2) + gate-designed
# Tg-A (1: C2 only — jsdom ignores the media type), Tg-B (6: C1 blind to a tag that never runs), Tg-C (3), Tg-D (5);
# (4) LIVE legs in the gate's own Express apps: G1 the gateway's REAL createCsrfMiddleware in front of the real router
# (200 {redirect} with the page's request shape; 403 CSRF_TOKEN_MISSING without the header; 403 CSRF_ORIGIN_INVALID on a
# foreign origin — Peter's #1 measured as a mechanism), G2 the gateway's real specRouteMap on the unlisted path (falls
# through), G3 the real router behind a real http-proxy front carrying the gateway's CSP (script-src 'self' as the
# browser sees it; the script fetched THROUGH the front; the click sends the two headers); (5) the widened-guard rule
# (full packages/shared at head, ks860 loopback cell green); (6) Peter answered point by point; delivered-vs-
# commissioned; findings-only; NOT-TESTED at equal prominence.
#
# Merge-base = origin develop M18 8861e6216 ITSELF (develop is an ancestor of the head; GitHub compare develop...head:
# ahead 5 / behind 0, 6 files — exit 10 if the merge-base changes). origin develop = M18 8861e6216 (the newest develop
# squash, 12:00:26Z 09-13; read 07:10 and 07:15 AEST 2026-09-14). The develop pin below is DISJOINTNESS-CHECKED, not bare: if
# origin develop has moved past M18, the GitHub compare of that delta is read and the launcher REFUSES (exit 18) only
# when the delta touches a GUARDED path — the six PR files, anything under Blockchain/Dev/services/auth/ (the 703
# ratio and the merge shape), the four api-gateway files the live legs mount or read (csrf.ts, specRouteMap.ts,
# index.ts, routes/proxy.ts), the production nginx conf, the OpenAPI spec, anything under
# Blockchain/Dev/packages/shared/src/__tests__/ (the walking guards), or the root lockfile — or cannot be judged
# (unreadable, not ahead, >250 files); otherwise it proceeds printing the move and its file count, which the gate
# re-states and merges onto (brief items 1, 2, 3, 7). A refusal means: confirm the new delta, then re-pin DEVELOP_SHA
# here AND in the brief's TARGET section AND the prompt — a different brief, a deliberate edit.
#
# Adapted from the #980 round-2 launcher by gen_launcher_881r2.py (asserted substitutions + one asserted insertion,
# residual guard): the same guard family and exit codes 2..20, re-pointed at #881 round 2 (exit 19 = the round-1 READ —
# Peter's review 5140256072 + his comment 5583115315 on disk — named in the brief AND present; exit 20 = the full head
# SHA in both brief and prompt), PLUS exit 21 = stdin is not a TTY on a real launch (--check is exempt: it launches
# nothing). A gate launched inside a Bash tool runs headless, parented to the caller's shell, invisible to Kam, and
# dies at the caller's rotation (2026-09-13 ledger) — this launcher refuses that.
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks798_841_799_881_r2.sh [--check]
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
           "Blockchain/Dev/services/auth/src/__tests__/ks799-consent-script-csp-and-execution.test.ts",
           "Blockchain/Dev/services/auth/src/__tests__/ks799-consent-form-csrf-submit.test.ts",
           "Blockchain/Dev/services/auth/src/__tests__/ks798-consent-form-client-id.test.ts",
           "Blockchain/Dev/services/auth/src/__tests__/ks841-consent-form-pkce-and-client-id.test.ts",
           "Blockchain/Dev/services/auth/src/__tests__/ks781-n1-empty-mfacode-treated-as-absent.test.ts",
           "Blockchain/Dev/services/auth/",
           "Blockchain/Dev/services/api-gateway/src/middleware/csrf.ts",
           "Blockchain/Dev/services/api-gateway/src/specRouteMap.ts",
           "Blockchain/Dev/services/api-gateway/src/index.ts",
           "Blockchain/Dev/services/api-gateway/src/routes/proxy.ts",
           "Blockchain/Dev/docker/nginx-gateway/nginx-production.conf",
           "Blockchain/Dev/docs/openapi/secuura-api.yaml",
           "Blockchain/Dev/packages/shared/src/__tests__/",
           "Blockchain/Dev/package-lock.json"]
'''
OLD_R1 = '''R1_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-13-ks924-901-980-9c620f890-tier2-r1/report.md'
grep -qF "$R1_REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the round-1 report path (a gate cannot ask)" >&2; exit 19; }
[ -s "$R1_REPORT" ] || { echo "REFUSING: the round-1 report named by the brief is missing or empty: $R1_REPORT" >&2; exit 19; }
'''
NEW_R1 = '''R1_READ='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-13_s212/item0/peter_comment_5583115315.md'
grep -qF "$R1_READ" "$BRIEF" && grep -qF '5140256072' "$BRIEF" \\
  || { echo "REFUSING: brief does not name the round-1 READ (Peter's review 5140256072 and his comment 5583115315 on disk at $R1_READ) — there is no round-1 QA report for #881 and a gate cannot ask" >&2; exit 19; }
[ -s "$R1_READ" ] || { echo "REFUSING: the round-1 read named by the brief is missing or empty: $R1_READ" >&2; exit 19; }
'''
subs = [
    ("QA980R2_BRIEF", "QA881R2_BRIEF", 2),
    ("QA980R2_PROMPT", "QA881R2_PROMPT", 2),
    ("QA980R2_HEAD", "QA881R2_HEAD", 2),
    ("2026-09-13_secuura-980-ks924-901-tier2-r2", "2026-09-14_secuura-881-ks798-841-799-tier1-r2", 3),
    ("refs/heads/feature/ks-924-ks-901-entrypoint-corpus-presence-set-and-three-shapes",
     "refs/heads/feature/ks-798-the-consent-page-posts-the-redirect-uri-in-the-client_id", 1),
    ("103c235b4d2be54cc1ade65ed660f397cf03e997", "8ac9db66f6fd0d751f74ecc95bb314210a31ec52", 1),
    ("MERGE_BASE='50b729d69c58474624508ed79d05c520dab22cc6'", "MERGE_BASE='8861e62161466c40f08d2b10a30edeb203123993'", 1),
    ("DEVELOP_SHA='1c38077ba2aea5f4c4371c1b68796026dc577764'", "DEVELOP_SHA='8861e62161466c40f08d2b10a30edeb203123993'", 1),
    (OLD_GUARDED, NEW_GUARDED, 1),
    ('DEV_NOTE="origin develop still $DEVELOP_SHA (M15, the develop this brief\'s 813/813 was written against; git ls-remote)"',
     'DEV_NOTE="origin develop still $DEVELOP_SHA (M18, the develop this brief\'s 54/703 was written against and the head already contains; git ls-remote)"', 1),
    ('DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#DISJOINT } — disjoint from the guard\'s three paths (#980\'s file, the ks860 loopback guard file, the packages/shared/ prefix); the gate merges the then-current develop, re-states the delta by name and re-derives the ratio (brief items 1 and 2)"',
     'DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#DISJOINT } — disjoint from the fifteen guarded paths (the six PR files, the services/auth/ prefix, the four gateway files, the nginx conf, the spec, the packages/shared tests prefix, the root lockfile); the gate merges the then-current develop, re-states the delta by name and re-derives the ratios (brief items 1, 2, 3, 7)"', 1),
    ("grep -q 'TIER 2' \"$BRIEF\" && grep -q 'TIER 2' \"$PROMPT_FILE\"", "grep -q 'TIER 1' \"$BRIEF\" && grep -q 'TIER 1' \"$PROMPT_FILE\"", 1),
    ("grep -q 'ROUND 2' \"$BRIEF\" && grep -q 'ROUND 2' \"$PROMPT_FILE\"", "grep -q 'ROUND 2' \"$BRIEF\" && grep -q 'ROUND 2' \"$PROMPT_FILE\"", 1),  # identical: asserted present once
    ('echo "  brief and prompt agree on TIER 2 and ROUND 2"', 'echo "  brief and prompt agree on TIER 1 and ROUND 2"', 1),
    (OLD_R1, NEW_R1, 1),
    ('  echo "  brief names the round-1 report and it is present on disk"',
     '  echo "  brief names the round-1 read (Peter\'s review 5140256072 + comment 5583115315) and it is present on disk"\n  echo "  (a real launch, not --check, additionally requires a TTY on stdin — exit 21)"', 1),
]
for old, new, n in subs:
    c = s.count(old)
    if c != n:
        print(f"REFUSING: anchor {old[:70]!r} occurs {c} times, expected {n}", file=sys.stderr)
        sys.exit(1)
    s = s.replace(old, new)

# 2b. ONE asserted insertion: the TTY guard, immediately after the --check block's closing `fi` and BEFORE the override
#     guard (exit 16) — so a headless launch with overrides set reads 21, never 16, and --check stays runnable headless.
OVERRIDE_GUARD = '[ -z "${QA881R2_BRIEF:-}${QA881R2_PROMPT:-}${QA881R2_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }\n'
TTY_GUARD = ('[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent and must run in a pane '
             '(cockpit.sh add), never inside a Bash tool (a headless gate is invisible and dies with its caller; 2026-09-13 ledger)" >&2; exit 21; }\n')
c = s.count(OVERRIDE_GUARD)
if c != 1:
    print(f"REFUSING: override-guard anchor occurs {c} times, expected 1", file=sys.stderr); sys.exit(1)
assert s.count(TTY_GUARD) == 0, "TTY guard already present"
s = s.replace(OVERRIDE_GUARD, TTY_GUARD + OVERRIDE_GUARD)

# 3. Residual guard — nothing of the source gate may survive (outside the exact header sentence naming the template).
RESIDUAL = ["980", "924", "901", "103c235b4", "9c620f890", "50b729d69", "1c38077ba", "QA980R2", "entrypoint-corpus",
            "ks860-test-listeners-bind-loopback.test.ts", "813", "812", "806", "M15", "M9", "M13", "three paths", "d81265b7f",
            "e232b0289", "068aa3d0f", "KS-1142", "GF-1", "tier2", "TIER 2", "s210", "#977", "ks877", "KS-877", "R1_REPORT",
            "round-1 report", "reports/2026-09-13", "DELTA gate", ":235", "P3 census", "loopback guard file",
            '"Blockchain/Dev/packages/shared/"', "1138", "1139", "s208", "bash 3.2", "ubuntu"]
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
    ("8ac9db66f6fd0d751f74ecc95bb314210a31ec52", 1), ("8ac9db66f", 3), ("ffcea35cb", 3), ("787771b97", 3),
    ("8861e62161466c40f08d2b10a30edeb203123993", 2), ("8861e6216", 6), ("136e6c8cc", 1),
    ("QA881R2_BRIEF", 2), ("QA881R2_PROMPT", 2), ("QA881R2_HEAD", 2),
    ("2026-09-14_secuura-881-ks798-841-799-tier1-r2.md", 2), ("2026-09-14_secuura-881-ks798-841-799-tier1-r2.prompt.txt", 1),
    ("refs/heads/feature/ks-798-the-consent-page-posts-the-redirect-uri-in-the-client_id", 1),
    ("exit 21", 3), ("exit 20", 2), ("exit 19", 3), ("exit 18", 3), ("exit 10", 2), ("exit 6", 1), ("exit 13", 1), ("exit 16", 2),
    ("exit 7", 1), ("exit 15", 1), ("exit 9", 1), ("exit 8", 1), ("exit 11", 1), ("exit 12", 1), ("exit 14", 1), ("exit 17", 1),
    ("exit 2;", 1), ("exit 3;", 1), ("exit 4;", 1), ("exit 5;", 1),
    ("'TIER 1'", 2), ("'ROUND 2'", 2), ("TIER 1 and ROUND 2", 1),
    ("[ -t 0 ]", 1), ("stdin is not a TTY", 2),
    ('"Blockchain/Dev/services/auth/",', 1), ('"Blockchain/Dev/services/auth/src/routes/oauth.ts",', 1),
    ("ks799-consent-script-csp-and-execution.test.ts", 2), ("ks799-consent-form-csrf-submit.test.ts", 2),
    ("ks798-consent-form-client-id.test.ts", 1), ("ks841-consent-form-pkce-and-client-id.test.ts", 1),
    ("ks781-n1-empty-mfacode-treated-as-absent.test.ts", 1),
    ('"Blockchain/Dev/services/api-gateway/src/middleware/csrf.ts",', 1), ('"Blockchain/Dev/services/api-gateway/src/specRouteMap.ts",', 1),
    ('"Blockchain/Dev/services/api-gateway/src/index.ts",', 1), ('"Blockchain/Dev/services/api-gateway/src/routes/proxy.ts",', 1),
    ('"Blockchain/Dev/docker/nginx-gateway/nginx-production.conf",', 1), ('"Blockchain/Dev/docs/openapi/secuura-api.yaml",', 1),
    ('"Blockchain/Dev/packages/shared/src/__tests__/",', 1), ('"Blockchain/Dev/package-lock.json"]', 1),
    ("GUARDED", 5), ('g.endswith("/") and f["filename"].startswith(g)', 1), ("fifteen guarded paths", 1),
    ("R1_READ", 5), ("peter_comment_5583115315.md", 1), ("5140256072", 4), ("5583115315", 4),
    ("MAIL YOUR VERDICT", 1), ("no memory maintenance", 1), ("NEVER print a credential value", 1), ("ultrathink", 1),
    ("exec claude --dangerously-skip-permissions --model opus", 1), ('cd "$QA_DIR"', 1),
    ("brief and prompt both name the head SHA", 1), ("M18", 6), ("703", 3), ("Tg-B", 1), ("CSRF_TOKEN_MISSING", 2),
    ("CSRF_ORIGIN_INVALID", 1), ("createCsrfMiddleware", 1), ("specRouteMap", 3),
]
for tok, n in CONTROLS:
    c = s.count(tok)
    if c != n:
        print(f"REFUSING: output control {tok!r} occurs {c} times, expected {n}", file=sys.stderr)
        sys.exit(3)
# the TTY guard must sit AFTER the --check block and BEFORE the override guard
i_check = s.index('if [ "${1:-}" = "--check" ]; then'); i_tty = s.index("[ -t 0 ]"); i_ovr = s.index(OVERRIDE_GUARD); i_exec = s.index("exec claude")
assert i_check < i_tty < i_ovr < i_exec, "guard order"
# no raw control byte
b = s.encode("utf-8")
assert not [i for i, x in enumerate(b) if (x < 0x20 and x not in (9, 10, 13)) or x == 0x7f], "raw control byte in output"

open(out_path, "w", encoding="utf-8").write(s)
os.chmod(out_path, 0o755)
print(f"written {out_path} ({len(b)} bytes); {len(subs)} substitutions asserted + 1 insertion (exit 21 TTY guard); residual guard clean ({len(RESIDUAL)} tokens); {len(CONTROLS)} output controls; guard order check-block < tty < override < exec")
