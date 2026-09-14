#!/usr/bin/env python3
"""gen_launcher_912r2.py — derive launch_qa_secuura_ks1004_912_r2_ks1059_937_stacked.sh from the INSTALLED #881 ROUND-2
launcher (sha256 030cbb8add3c1746… — the newest tier-1 round-2 template carrying the DISJOINTNESS-CHECKED develop pin,
the exit-19 round-1-read guard, the exit-20 head-SHA-in-both guard and the exit-21 stdin-TTY guard) by ASSERTED
substitutions (every anchor must occur exactly as often as stated, or the generator refuses), THREE asserted INSERTIONS
(exit 22 = #937's head not at its branch on origin; exit 23 = the STACK relation — GitHub compare 609c44c55...6fd3a8bec
must read merge_base 609c44c55 and exactly ONE file; exit 20 widened to BOTH head SHAs in BOTH files), then a RESIDUAL
GUARD: any token of the source gate (its PR number, tickets, heads, its guarded paths, its ratios, its round-1 ids)
left anywhere in the output is a refusal — nothing is written on refusal. Same method as gen_launcher_881r2.py.

The GUARDED list for THIS gate = the four #912 files + the ks1059 file by name + the `Blockchain/Dev/services/originate/src/`
prefix (the 598/602 ratios and the merge shape) + the gateway's `routes/verification.ts` and its four pinning tests (the
F1 discharge is measured on develop's copy) + the `Blockchain/Dev/packages/shared/src/__tests__/` prefix (the walking
guards) + the root lockfile (the farm).

Usage: gen_launcher_912r2.py <template launcher> <output launcher>
Exit: 0 written · 1 an anchor count disagreed · 2 a residual token survived · 3 an output control failed
"""
import os, re, sys

src_path, out_path = sys.argv[1], sys.argv[2]
s = open(src_path, encoding="utf-8").read()

NEW_HEADER = """#!/bin/bash
# launch_qa_secuura_ks1004_912_r2_ks1059_937_stacked.sh — cross-project QA agent, ONE PASS over TWO Secuura PRs:
#   (1) TIER 1, ROUND 2 on PR #912 (KS-1004) @ 609c44c55 — the anchor-failed lockout fix round. Round 1 was the fleet's
#       own tier-1 NO GO of 2026-09-09 on ae8751f38 (F1 Blocker: the gateway's `confidence` was presence-keyed, so a
#       failed anchor carrying a hash reported verified:true), recovered from the gate's transcript into
#       fleet/qa-agent/reports/2026-09-09_secuura-ks1004-912-tier1-VERDICT.md and transcribed onto the PR as issue
#       comment 5597511879. THREE commits: round 1's head ae8751f38 + the MERGE 323151415 (parents ae8751f38 + origin
#       develop M18 8861e6216; ONE conflict in anchorStateSync.ts resolved by hand — re-derived by merge-tree: the hand
#       resolution differs from git's own auto-merge in that ONE file and TWO regions) + the FIX 609c44c55 (parent
#       323151415; THREE files: anchorStateSync.ts +4 -1 = the anchoredAt carry narrowed to `prior?.txHash &&
#       prior?.anchoredAt`; ks1058-*.test.ts +13 -6 = the :183 guard cell re-stated as the UNION; ks1004-*.test.ts +21 =
#       one new CONTRACT cell). PR onto develop: FOUR files +303 -18. develop M18 is an ANCESTOR of the head (0 behind /
#       3 ahead) — the head tree IS the merged tree. Tier 1 because of what the change REACHES (the public verify
#       surface); the live leg is the gateway's REAL verify router on the gate's own 127.0.0.1 listeners (the ks1057
#       harness shape = the s128 precedent). F1 is discharged BY DEVELOP (KS-1057/1069/1070/1071, six commits on
#       verification.ts, blob 95c13b01f at head = M18) — measured at the file the head contains.
#   (2) TIER 2, ROUND 1 on PR #937 (KS-1059) @ 6fd3a8bec, STACKED on #912: SEVEN commits = #912's three + the ks1059
#       test (c1e23b6af, 2026-09-09) + round 1's #937 head cf8b23366 + bda4c74a6 (develop M18 merged IN — the three
#       systemTest lockfile hunks leave by ANCESTRY, #934 merged 2026-09-10) + 6fd3a8bec (#912's 609c44c55 merged IN).
#       The delta onto #912 is ONE test file (ks1059-*.test.ts +199, 4 cells); anchorStateSync.ts at 6fd3a8bec is
#       BYTE-IDENTICAL to #912's head (blob d8e988f7a). Gated as the DELTA onto #912 (red-proof on #912's line: delete
#       `inFlight &&` -> the DEFECT cell red alone) and as the stack onto live develop. Merge order #912 -> #937.
#
# The gate establishes (#912): (1) the delta = the three-file fix onto a merge whose resolution is the two regions
# (merge-tree re-derived); (2) RED-FIRST BOTH WAYS — the merge commit as a whole `2 failed, 26 passed, 28`, the head
# tests vs the merge product `2 failed, 27 passed, 29`, head 29/29 · 55/55 · originate 56/598; (3) the tamper table
# SUITE RUNNING — T1/T2/T3/T4 (4/2/2/1 of 29) + Tg-A (3: the destructive write restored; K1 stays green), Tg-B (2: the
# inFlight predicate back to base), Tg-C (3: the confirmed guard deleted), Tg-D (2), Tg-E (1); (4) F1 DISCHARGED BY
# DEVELOP: the four gateway suites 33/33 under vitest + round 1's four-row table re-driven through the REAL router on
# loopback (R2 anchor_failed + hash + bh 4242 -> verified FALSE) + F2's echo measured and RULED; (5) the widened-guard
# rule (packages/shared at head, ks860 green; tsc at head AND at the merge commit); (6) Peter's three one-liners, his F1
# question and his evidence list answered; delivered-vs-commissioned against ITEM 1 of the s217 brief; findings-only;
# NOT-TESTED (the stack suites — HOLD; the updateDocument SQL path; producibility of a hashed anchor_failed row with
# bh > 0). (#937): S1 the one-file delta + both merges are unions (tree equalities); S2 ks1059 4/4, `inFlight &&`
# deleted -> 1/3 the DEFECT cell alone, the `if (false)` wrong-reason control; S3 ks1059 GREEN under all nine #912
# tampers; S4 originate 57/602 on the stack, the locks' ancestry proof; S5 delivered-vs-commissioned against ITEM 2.
#
# Merge-base = origin develop M18 8861e6216 ITSELF (develop is an ancestor of BOTH heads; GitHub compare develop...
# 609c44c55: ahead 3 / behind 0, 4 files — exit 10 if the merge-base changes). The STACK relation is pinned (exit 23):
# compare 609c44c55...6fd3a8bec must read merge_base 609c44c55 and exactly ONE file (ahead 4 commits). #937's head is
# pinned at its own branch (exit 22). origin develop = M18 8861e6216 (12:00:26Z 09-13; read 08:03 and 08:09 AEST
# 2026-09-14). The develop pin below is DISJOINTNESS-CHECKED, not bare: if origin develop has moved past M18, the GitHub
# compare of that delta is read and the launcher REFUSES (exit 18) only when the delta touches a GUARDED path — the
# five PR files, anything under Blockchain/Dev/services/originate/src/ (the 598/602 ratios and the merge shape), the
# gateway's routes/verification.ts and its four ks1057/ks1069/ks1070/ks1071 tests (the F1 discharge), anything under
# Blockchain/Dev/packages/shared/src/__tests__/ (the walking guards), or the root lockfile — or cannot be judged
# (unreadable, not ahead, >250 files); otherwise it proceeds printing the move and its file count, which the gate
# re-states and merges onto (brief items 1, 2, 3, 4, 7; S1, S4). A refusal means: confirm the new delta, then re-pin
# DEVELOP_SHA here AND in the brief's TARGET section AND the prompt — a different brief, a deliberate edit.
#
# Adapted from the #881 round-2 launcher by gen_launcher_912r2.py (asserted substitutions + three asserted insertions,
# residual guard): the same guard family and exit codes 2..21, re-pointed at #912 round 2 (exit 19 = the round-1 READ —
# the recovered verdict file on disk + the transcription comment id 5597511879 named in the brief; exit 20 = BOTH full
# head SHAs in both brief and prompt; exit 21 = stdin is not a TTY on a real launch, --check exempt), PLUS exit 22 (#937's
# head moved) and exit 23 (the stack relation). A gate launched inside a Bash tool runs headless, parented to the
# caller's shell, invisible to Kam, and dies at the caller's rotation (2026-09-13 ledger) — this launcher refuses that.
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks1004_912_r2_ks1059_937_stacked.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..23 a guard refused
"""

# 1. Replace the header (everything before `set -u`) wholesale.
marker = "set -u\n"
assert s.count(marker) == 1, "header marker"
s = NEW_HEADER + s[s.index(marker):]

# 2. Asserted substitutions: (old, new, expected count in the post-header text).
OLD_GUARDED = '''GUARDED = ["Blockchain/Dev/services/auth/src/routes/oauth.ts",
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
NEW_GUARDED = '''GUARDED = ["Blockchain/Dev/services/originate/src/services/anchorStateSync.ts",
           "Blockchain/Dev/services/originate/src/__tests__/ks1004-anchor-failed-lockout.test.ts",
           "Blockchain/Dev/services/originate/src/__tests__/ks1058-anchor-failed-preserves-thread-token.test.ts",
           "Blockchain/Dev/services/originate/src/__tests__/ks535-anchor-async-fail-propagates.test.ts",
           "Blockchain/Dev/services/originate/src/__tests__/ks1059-sim-leg-must-not-resurrect-a-terminal-document.test.ts",
           "Blockchain/Dev/services/originate/src/",
           "Blockchain/Dev/services/api-gateway/src/routes/verification.ts",
           "Blockchain/Dev/services/api-gateway/src/__tests__/ks1057-verify-confidence-is-status-aware.test.ts",
           "Blockchain/Dev/services/api-gateway/src/__tests__/ks1069-persisted-anchored-input-shape.test.ts",
           "Blockchain/Dev/services/api-gateway/src/__tests__/ks1070-tier2-carries-simulated.test.ts",
           "Blockchain/Dev/services/api-gateway/src/__tests__/ks1071-verify-confidence-one-mapping.test.ts",
           "Blockchain/Dev/packages/shared/src/__tests__/",
           "Blockchain/Dev/package-lock.json"]
'''
OLD_R1 = '''R1_READ='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-13_s212/item0/peter_comment_5583115315.md'
grep -qF "$R1_READ" "$BRIEF" && grep -qF '5140256072' "$BRIEF" \\
  || { echo "REFUSING: brief does not name the round-1 READ (Peter's review 5140256072 and his comment 5583115315 on disk at $R1_READ) — there is no round-1 QA report for #881 and a gate cannot ask" >&2; exit 19; }
[ -s "$R1_READ" ] || { echo "REFUSING: the round-1 read named by the brief is missing or empty: $R1_READ" >&2; exit 19; }
'''
NEW_R1 = '''R1_READ='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/reports/2026-09-09_secuura-ks1004-912-tier1-VERDICT.md'
grep -qF "$R1_READ" "$BRIEF" && grep -qF '5597511879' "$BRIEF" \\
  || { echo "REFUSING: brief does not name the round-1 READ (the recovered tier-1 NO GO verdict file at $R1_READ and its transcription onto the PR, issue comment 5597511879) — a gate cannot ask" >&2; exit 19; }
[ -s "$R1_READ" ] || { echo "REFUSING: the round-1 read named by the brief is missing or empty: $R1_READ" >&2; exit 19; }
'''
OLD_SHA20 = '''grep -qF "$HEAD_SHA" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$BRIEF" \\
  || { echo "REFUSING: brief or prompt does not name the head SHA $HEAD_SHA — a gate about another SHA is another gate" >&2; exit 20; }
'''
NEW_SHA20 = '''grep -qF "$HEAD_SHA" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$BRIEF" \\
  || { echo "REFUSING: brief or prompt does not name the head SHA $HEAD_SHA — a gate about another SHA is another gate" >&2; exit 20; }
grep -qF "$HEAD_937" "$PROMPT_FILE" && grep -qF "$HEAD_937" "$BRIEF" \\
  || { echo "REFUSING: brief or prompt does not name the stacked head SHA $HEAD_937 — a gate about another SHA is another gate" >&2; exit 20; }
'''
subs = [
    ("QA881R2_BRIEF", "QA912R2_BRIEF", 2),
    ("QA881R2_PROMPT", "QA912R2_PROMPT", 2),
    ("QA881R2_HEAD", "QA912R2_HEAD", 2),
    ("2026-09-14_secuura-881-ks798-841-799-tier1-r2", "2026-09-14_secuura-912-ks1004-tier1-r2-937-ks1059-stacked", 3),
    ("BRANCH='refs/heads/feature/ks-798-the-consent-page-posts-the-redirect-uri-in-the-client_id'",
     "BRANCH='refs/heads/feature/ks-1004-anchor-failed-lockout'\nBRANCH_937='refs/heads/feature/ks-1059-anchorstatesyncts360-removing-inflight-from-the-ks-587-sim'", 1),
    ("8ac9db66f6fd0d751f74ecc95bb314210a31ec52", "609c44c55323b5c90320847b6837ca37f6586705", 1),
    ("MERGE_BASE='8861e62161466c40f08d2b10a30edeb203123993'",
     "HEAD_937='6fd3a8bec4e4cc858d38925e00703a37ffcf1b30'\nMERGE_BASE='8861e62161466c40f08d2b10a30edeb203123993'", 1),
    ("DEVELOP_SHA='8861e62161466c40f08d2b10a30edeb203123993'", "DEVELOP_SHA='8861e62161466c40f08d2b10a30edeb203123993'", 1),  # identical: asserted present once
    (OLD_GUARDED, NEW_GUARDED, 1),
    ('DEV_NOTE="origin develop still $DEVELOP_SHA (M18, the develop this brief\'s 54/703 was written against and the head already contains; git ls-remote)"',
     'DEV_NOTE="origin develop still $DEVELOP_SHA (M18, the develop this brief\'s 56/598 and 57/602 were written against and BOTH heads already contain; git ls-remote)"', 1),
    ('DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#DISJOINT } — disjoint from the fifteen guarded paths (the six PR files, the services/auth/ prefix, the four gateway files, the nginx conf, the spec, the packages/shared tests prefix, the root lockfile); the gate merges the then-current develop, re-states the delta by name and re-derives the ratios (brief items 1, 2, 3, 7)"',
     'DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#DISJOINT } — disjoint from the thirteen guarded paths (the five PR files, the services/originate/src/ prefix, the gateway verification.ts and its four tests, the packages/shared tests prefix, the root lockfile); the gate merges the then-current develop under BOTH heads, re-states the delta by name and re-derives the ratios (brief items 1, 2, 3, 4, 7; S1, S4)"', 1),
    ("grep -q 'TIER 1' \"$BRIEF\" && grep -q 'TIER 1' \"$PROMPT_FILE\"", "grep -q 'TIER 1' \"$BRIEF\" && grep -q 'TIER 1' \"$PROMPT_FILE\"", 1),  # identical: asserted present once
    ("grep -q 'ROUND 2' \"$BRIEF\" && grep -q 'ROUND 2' \"$PROMPT_FILE\"", "grep -q 'ROUND 2' \"$BRIEF\" && grep -q 'ROUND 2' \"$PROMPT_FILE\"", 1),  # identical: asserted present once
    ('echo "  brief and prompt agree on TIER 1 and ROUND 2"', 'echo "  brief and prompt agree on TIER 1 and ROUND 2 (#912; #937 rides as TIER 2 ROUND 1 STACKED in the same files)"', 1),
    (OLD_R1, NEW_R1, 1),
    (OLD_SHA20, NEW_SHA20, 1),
    ('  echo "  brief names the round-1 read (Peter\'s review 5140256072 + comment 5583115315) and it is present on disk"',
     '  echo "  brief names the round-1 read (the recovered NO GO verdict file + transcription comment 5597511879) and it is present on disk"', 1),
    ('  echo "  head $HEAD_SHA present at $BRANCH on origin"',
     '  echo "  head $HEAD_SHA present at $BRANCH on origin"\n  echo "  stacked head $HEAD_937 present at $BRANCH_937 on origin"', 1),
    ('  echo "  merge-base still $MERGE_BASE (GitHub compare API)"',
     '  echo "  merge-base still $MERGE_BASE (GitHub compare API)"\n  echo "  stack relation still merge_base $HEAD_SHA / ONE file for 609c44c55...6fd3a8bec (GitHub compare API: $STACK_READ)"', 1),
    ('  echo "  brief and prompt both name the head SHA $HEAD_SHA"',
     '  echo "  brief and prompt both name the head SHA $HEAD_SHA and the stacked head SHA $HEAD_937"', 1),
    ('[ -z "${QA912R2_BRIEF:-}${QA912R2_PROMPT:-}${QA912R2_HEAD:-}" ]', '[ -z "${QA912R2_BRIEF:-}${QA912R2_PROMPT:-}${QA912R2_HEAD:-}" ]', 0),  # placeholder: asserted AFTER the env-prefix subs below (count checked in CONTROLS)
]
for old, new, n in subs:
    c = s.count(old)
    if n == 0:
        continue
    if c != n:
        print(f"REFUSING: anchor {old[:70]!r} occurs {c} times, expected {n}", file=sys.stderr)
        sys.exit(1)
    s = s.replace(old, new)

# 2b. THREE asserted insertions.
#  (i) exit 22 — #937's head at its branch, immediately after the exit-6 block.
EXIT6_BLOCK = '''if ! git -C "$REPO" ls-remote origin "$BRANCH" | grep -q "^${HEAD_SHA}[[:space:]]"; then
  echo "REFUSING: $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA" >&2
  git -C "$REPO" ls-remote origin "$BRANCH" >&2
  exit 6
fi
'''
EXIT22_BLOCK = '''if ! git -C "$REPO" ls-remote origin "$BRANCH_937" | grep -q "^${HEAD_937}[[:space:]]"; then
  echo "REFUSING: $HEAD_937 is not at $BRANCH_937 on origin — the stacked head moved; the brief is about a different SHA" >&2
  git -C "$REPO" ls-remote origin "$BRANCH_937" >&2
  exit 22
fi
'''
c = s.count(EXIT6_BLOCK)
if c != 1:
    print(f"REFUSING: exit-6 block occurs {c} times, expected 1", file=sys.stderr); sys.exit(1)
assert s.count(EXIT22_BLOCK) == 0, "exit-22 block already present"
s = s.replace(EXIT6_BLOCK, EXIT6_BLOCK + EXIT22_BLOCK)

#  (ii) exit 23 — the STACK relation, immediately after the exit-10 merge-base guard.
EXIT10_LINE = '''[ "$ACTUAL_MB" = "$MERGE_BASE" ] || { echo "REFUSING: merge-base is now '$ACTUAL_MB', brief says '$MERGE_BASE'" >&2; exit 10; }
'''
EXIT23_BLOCK = '''
# The STACK pin: #937's delta onto #912 must be exactly ONE file over #912's head (the compare's merge_base = #912's head).
STACK_READ="$(
  set -a; . "$SECUURA_ENV"; set +a
  HEAD_SHA="$HEAD_SHA" HEAD_937="$HEAD_937" python3 - <<'PYS'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/" + os.environ["HEAD_SHA"] + "..." + os.environ["HEAD_937"]
r = urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60)
c = json.load(r)
print("%s ahead=%d files=%d" % (c["merge_base_commit"]["sha"], c["ahead_by"], len(c.get("files") or [])))
PYS
)"
[ -n "$STACK_READ" ] || { echo "REFUSING: could not read the stack compare (#912 head...#937 head) from the GitHub compare API" >&2; exit 13; }
[ "$STACK_READ" = "$HEAD_SHA ahead=4 files=1" ] \\
  || { echo "REFUSING: the stacked delta is not ONE file over #912's head: compare reads '$STACK_READ', brief pins '$HEAD_SHA ahead=4 files=1' (merge order #912 -> #937 is the premise of section S)" >&2; exit 23; }
'''
c = s.count(EXIT10_LINE)
if c != 1:
    print(f"REFUSING: exit-10 line occurs {c} times, expected 1", file=sys.stderr); sys.exit(1)
assert s.count("exit 23;") == 0, "exit 23 (code form) already present"
s = s.replace(EXIT10_LINE, EXIT10_LINE + EXIT23_BLOCK)

#  (iii) exit 20 widened to both SHAs — done in `subs` (OLD_SHA20 -> NEW_SHA20); asserted here by count.
assert s.count("exit 20;") == 2, "exit-20 arms (code form)"

# 3. Residual guard — nothing of the source gate may survive (outside the exact header sentence naming the template).
RESIDUAL = ["881", "798", "841", "799", "8ac9db66f", "ffcea35cb", "787771b97", "306d0db92", "QA881R2", "oauth", "consent",
            "csrf", "CSRF", "nginx", "specRouteMap", "secuura-api.yaml", "/703", "703 ratio", "/613", "5140256072", "5583115315", "s212",
            "jsdom", "helmet", "Tg-B (6", "services/auth", "peter_comment", "KS-79", "KS-84", "ks781", "ks798", "ks841",
            "ks799", "fifteen", "R1_REPORT", "980", "924", "TIER 2 and", "tier2-r2", "M15", "M17", "CSP", "script-src",
            "createCsrfMiddleware", "unsafe-inline", "proxy.ts", "middleware/csrf", "the six PR files", "54/703"]
PERMITTED = ["Adapted from the #881 round-2 launcher"]
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
    ("609c44c55323b5c90320847b6837ca37f6586705", 1), ("609c44c55", 8), ("6fd3a8bec4e4cc858d38925e00703a37ffcf1b30", 1), ("6fd3a8bec", 6),
    ("323151415", 2), ("ae8751f38", 3), ("cf8b23366", 1), ("bda4c74a6", 1), ("c1e23b6af", 1), ("d8e988f7a", 1), ("95c13b01f", 1),
    ("8861e62161466c40f08d2b10a30edeb203123993", 2), ("8861e6216", 5),
    ("QA912R2_BRIEF", 2), ("QA912R2_PROMPT", 2), ("QA912R2_HEAD", 2),
    ("2026-09-14_secuura-912-ks1004-tier1-r2-937-ks1059-stacked.md", 2), ("2026-09-14_secuura-912-ks1004-tier1-r2-937-ks1059-stacked.prompt.txt", 1),
    ("BRANCH='refs/heads/feature/ks-1004-anchor-failed-lockout'", 1),
    ("BRANCH_937='refs/heads/feature/ks-1059-anchorstatesyncts360-removing-inflight-from-the-ks-587-sim'", 1),
    ("HEAD_937='6fd3a8bec4e4cc858d38925e00703a37ffcf1b30'", 1), ('"$HEAD_937"', 3), ('"$BRANCH_937"', 2), ("STACK_READ", 5),
    ("exit 23", 3), ("exit 22", 3), ("exit 21", 3), ("exit 20", 3), ("exit 20;", 2), ("exit 23;", 1), ("exit 22\n", 1), ("exit 19", 3), ("exit 18", 3), ("exit 10", 2), ("exit 6", 1), ("exit 13", 2), ("exit 16", 2),
    ("exit 7", 1), ("exit 15", 1), ("exit 9", 1), ("exit 8", 1), ("exit 11", 1), ("exit 12", 1), ("exit 14", 1), ("exit 17", 1),
    ("exit 2;", 1), ("exit 3;", 1), ("exit 4;", 1), ("exit 5;", 1),
    ("'TIER 1'", 2), ("'ROUND 2'", 2), ("TIER 1 and ROUND 2", 1),
    ("[ -t 0 ]", 1), ("stdin is not a TTY", 2),
    ('"Blockchain/Dev/services/originate/src/",', 1), ('"Blockchain/Dev/services/originate/src/services/anchorStateSync.ts",', 1),
    ("ks1004-anchor-failed-lockout.test.ts", 1), ("ks1058-anchor-failed-preserves-thread-token.test.ts", 1),
    ("ks535-anchor-async-fail-propagates.test.ts", 1), ("ks1059-sim-leg-must-not-resurrect-a-terminal-document.test.ts", 1),
    ('"Blockchain/Dev/services/api-gateway/src/routes/verification.ts",', 1),
    ("ks1057-verify-confidence-is-status-aware.test.ts", 1), ("ks1069-persisted-anchored-input-shape.test.ts", 1),
    ("ks1070-tier2-carries-simulated.test.ts", 1), ("ks1071-verify-confidence-one-mapping.test.ts", 1),
    ('"Blockchain/Dev/packages/shared/src/__tests__/",', 1), ('"Blockchain/Dev/package-lock.json"]', 1),
    ("GUARDED", 5), ('g.endswith("/") and f["filename"].startswith(g)', 1), ("thirteen guarded paths", 1),
    ("R1_READ", 5), ("2026-09-09_secuura-ks1004-912-tier1-VERDICT.md", 2), ("5597511879", 5),
    ("MAIL YOUR VERDICT", 1), ("no memory maintenance", 1), ("NEVER print a credential value", 1), ("ultrathink", 1),
    ("exec claude --dangerously-skip-permissions --model opus", 1), ('cd "$QA_DIR"', 1),
    ("brief and prompt both name the head SHA", 1), ("stacked head SHA", 2), ("M18", 8), ("598", 3), ("602", 3), ("merge order", 1), ("Merge order", 1),
    ("ahead=4 files=1", 2), ("inFlight &&", 2), ("anchoredAt", 2), ("verified FALSE", 1), ("KS-1004", 1), ("KS-1059", 1),
]
if os.environ.get("GEN_DEBUG"):
    for tok, n in CONTROLS:
        print(f"  {s.count(tok):3d} (stated {n:2d}) {tok!r}")
    sys.exit(4)
for tok, n in CONTROLS:
    c = s.count(tok)
    if c != n:
        print(f"REFUSING: output control {tok!r} occurs {c} times, expected {n}", file=sys.stderr)
        sys.exit(3)
# guard order: exit-6 < exit-22 < exit-10 < exit-23 < develop pin < --check block < tty < override < exec
OVERRIDE_GUARD = '[ -z "${QA912R2_BRIEF:-}${QA912R2_PROMPT:-}${QA912R2_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }\n'
assert s.count(OVERRIDE_GUARD) == 1, "override guard"
i6 = s.index("exit 6\n"); i22 = s.index("exit 22\n"); i10 = s.index("exit 10;"); i23 = s.index("exit 23;"); idev = s.index('CUR_DEV="$(')
i_check = s.index('if [ "${1:-}" = "--check" ]; then'); i_tty = s.index("[ -t 0 ]"); i_ovr = s.index(OVERRIDE_GUARD); i_exec = s.index("exec claude")
assert i6 < i22 < i10 < i23 < idev < i_check < i_tty < i_ovr < i_exec, "guard order"
# no raw control byte
b = s.encode("utf-8")
assert not [i for i, x in enumerate(b) if (x < 0x20 and x not in (9, 10, 13)) or x == 0x7f], "raw control byte in output"

open(out_path, "w", encoding="utf-8").write(s)
os.chmod(out_path, 0o755)
print(f"written {out_path} ({len(b)} bytes); {sum(1 for _,_,n in subs if n)} substitutions asserted + 3 insertions (exit 22 #937 head; exit 23 stack relation; exit 20 widened to both SHAs); residual guard clean ({len(RESIDUAL)} tokens); {len(CONTROLS)} output controls; guard order 6 < 22 < 10 < 23 < develop-pin < check-block < tty < override < exec")
