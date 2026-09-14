#!/usr/bin/env python3
"""gen_launcher_799.py — derive launch_qa_secuura_ks764_577_780_799_880_985.sh from the INSTALLED #982 launcher (the
non-stacked template carrying the DISJOINTNESS-CHECKED develop pin, the exit-20 head-SHA-in-both guard and the exit-21
stdin-is-not-a-TTY guard; sha256 f9c978c109e9ae31) by ASSERTED substitutions (every anchor must occur exactly as often as
stated, or the generator refuses) and THREE asserted BLOCK replacements (the head guard -> a three-head loop; the
merge-base compare -> three compares; the --check echo block), then a RESIDUAL GUARD: any token of the source gate left
anywhere in the output is a refusal — nothing is written on refusal.

Differences from the template, all asserted: THREE heads pinned at their branches (exit 6 — the loop names the PR that
moved); THREE GitHub compares (exit 10): develop...#799 head must read `<M18> ahead=12 files=12`, develop...#880 head
`<M18> ahead=4 files=5`, and the STACK-PARENT compare #799head...#985head `<#799 head> ahead=1 files=7` (a stacked PR is
judged as the delta over its parent); ONE develop pin with a GUARDED list covering all three PRs' files and the
neighbours the brief's expectations rest on; the exit-20 guard extended to all three SHAs in BOTH the brief and the
prompt; the same exit-21 TTY guard; the env-override prefix QA799_.

Usage: gen_launcher_799.py <template launcher> <output launcher>
Exit: 0 written · 1 an anchor count disagreed · 2 a residual token survived · 3 an output control failed
"""
import os, sys, hashlib

src_path, out_path = sys.argv[1], sys.argv[2]
s = open(src_path, encoding="utf-8").read()
print("template sha256:", hashlib.sha256(s.encode("utf-8")).hexdigest()[:16], "(expected f9c978c109e9ae31)")
assert hashlib.sha256(s.encode("utf-8")).hexdigest()[:16] == "f9c978c109e9ae31", "template is not the installed #982 launcher"

M18 = "8861e62161466c40f08d2b10a30edeb203123993"
H799 = "6da848891924f859179d097d464a7b97c9783a6a"
H880 = "a704137de38a3055e40ee62adc343c0239f34ea9"
H985 = "fcd8a01e40d34d6cb4055e7b4fd58b9bb908bbe0"

NEW_HEADER = """#!/bin/bash
# launch_qa_secuura_ks764_577_780_799_880_985.sh — cross-project QA agent, ONE gate over the THREE READY PRs of lane L5
# (builder s216): TIER 1 ROUND 1 of the EXECUTING gate on Secuura PR #799 (KS-764) @ 6da848891 — the shared API-key
# REVOKE policy (@secuura/shared keyRevokePolicy.ts: tenant is the floor, organisation is the gate) and its two
# destructive routes (services/security DELETE /api/keys/:id; services/originate DELETE /api/admin/api-keys/:id) —
# PLUS a TIER 2 section on PR #880 (KS-577) @ a704137de (two regenerated OpenAPI descriptions; MERGE IS KAM'S) — PLUS a
# TIER 2 section on PR #985 (KS-780) @ fcd8a01e4, STACKED on #799's head (the org-id normaliser moved into
# @secuura/shared, behaviour pinned unchanged; merge order #799 -> #985). One brief, one prompt, one verdict mail with a
# verdict PER PR.
#
# THE SHAPES. #799's head is ONE fix commit (two test files, +80 -2: the two loopback binds, the F-2 `typeof` line, the
# F-3 no-tenant fixture + cell on BOTH surfaces) on a merge commit e6e25421e = Peter's last read 38f6377b9 + develop M18
# (--no-ff; tree 7bb31ccb1 = the clean 3-way). develop is an ANCESTOR of the head (compare develop...head = merge_base
# M18, ahead 12, behind 0, TWELVE files) — so the head tree IS the PR merged onto live develop. #880's head is ONE fix
# commit (the .ts source of two yaml descriptions + the REGENERATED yaml, +15 -10) on a merge commit 6114a15d7 = 85f8263c2
# + M18 (tree 654a000ce = the 3-way); compare develop...head = M18, ahead 4, FIVE files. #985's head is ONE commit whose
# parent IS #799's head (compare 6da848891...fcd8a01e4 = merge_base 6da848891, ahead 1, SEVEN files) — the stack-parent
# pin. All three pins are asserted through the GitHub compare API (exit 10 if any changes).
#
# WHY TIER 1 for #799, stated here so this file and the brief cannot drift apart: on SHAPE this round is two test
# files — a tier 2. It is tier 1 because of what the PR REACHES: every svc_api_keys row an ORG_ADMIN / ISSUER_ADMIN can
# name, on two destructive routes, plus the ONE new refusal the PR introduces on originate (`403 caller has no tenant`)
# and the deploy precondition the builder names (every stock-seed org-bounded admin meets `caller has no organisation`)
# — Wednesday's advance ruling 2026-09-14 07:3x: "#799 tier 1 (a security package's middleware); #880 tier 2; KS-780's
# PR tier 2". A tier keyed on the shape of a round is blind to what the PR reaches.
#
# The gate establishes (#799): (1) the round's delta is exactly the fix commit on a clean develop merge (11 files
# blob-identical to 38f6377b9; the merge tree = the 3-way); (2) Peter's three items RED-FIRST / GREEN, re-derived: the
# ks860 loopback guard on the merged tree (1 failed | 22 passed naming exactly the two head lines :145 / :138), F-2
# both ways (the typeof line red with the export absent, the CONTROL cell GREEN without the line), F-3 red under the
# policy tamper on BOTH surfaces (D2); (3) the four ks764 files 15/11/7/10 and the full suites 828 / 205 / 598 / 343
# on the head tree, develop-alone beside each; (4) the tamper table with the suites running (T1o, T1s, T2, T3, T4, T5,
# T6, T7, T8, T9o, T9s, T10); (5) the reach (H-reach, H-default, H-guard-walk, H-citation, H-pair); (6)
# delivered-vs-commissioned vs the s216 brief ITEM 1 and Peter's checkboxes; findings-only; NOT TESTED at equal
# prominence (no stack — Peter's live 8-case matrix is HIS). (#880): --check PASS at head / FAIL under a one-character
# control; Peter's two false sentences gone, the true ones present, side by side; the prose true to
# revokePriorConnectorKeys and naming what the caller can see (D1); the suites; the verdict paragraph "MERGE IS KAM'S;
# KS-577 stays OPEN". (#985): the seven blobs on 6da848891; the definitions census 1 / 2 with a plant-and-find control;
# behaviour pinned unchanged (T780: one character -> 9 cells across 3 packages; T780b the ks695 pass-through line
# load-bearing; T780d the structural cell sees a byte-identical copy); merge order #799 -> #985.
#
# origin develop = M19 6e78961e1 (#982's squash "KS-790: the OAuth token grants resolve the user through the pre-auth
# carve-out…", 2026-09-13T23:00:09Z; read 09:07 AEST 2026-09-14) — ONE squash past M18 8861e6216 (the builder's cut; the
# merge-base of all three heads, unchanged), THREE files under services/auth/, disjoint from every guarded path below —
# the launcher's own MOVED judgement at 08:5x AEST, then re-pinned deliberately. The develop pin below is
# DISJOINTNESS-CHECKED, not bare: if origin develop has moved past M19, the GitHub compare of that delta is read and the launcher REFUSES (exit 18) only when the
# delta touches a GUARDED path — the three PRs' own files, packages/shared/src/security/ (the policy and the normaliser),
# packages/shared/src/index.ts and middleware/index.ts, the ks860 loopback guard file, services/security/src/index.ts
# and keyRevokePolicy.ts, ks742-keys-tenancy-route-contract.test.ts, services/originate/src/routes/adminConfig.ts and
# middleware/auth.ts, services/auth/src/services/jwt.ts, services/api-gateway/src/routes/platform.ts, the yaml, the
# generator, the .ts source of the yaml, orgId.ts's three originate callers and the four originate suites #985's
# red-proof reds — or cannot be judged (unreadable, not ahead, >250 files); otherwise it proceeds printing the move and
# its file count, which the gate re-states (brief TARGET: develop-alone + 15 / + 18 / + 10 / + 0 for #799's tree, and
# + 22 / + 18 / + 13 / + 0 for #985's). #880 or #799 LANDING before this gate trips exit 18 BY DESIGN (they move
# services/security/src/index.ts, the policy, the yaml): confirm the new delta, then re-pin DEVELOP_SHA here AND in the
# brief's TARGET section AND the prompt — a different brief, a deliberate edit.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — a gate launched there runs headless, invisible to Kam, and dies with the caller's
# shell (2026-09-13 ledger). `--check` still runs headless (it launches nothing).
#
# Adapted from the #982 launcher by gen_launcher_799.py (asserted substitutions, three asserted block replacements,
# residual guard): the same guard family and exit codes 2..18, 20, 21 (code 19 — the round-1-report guard of the older
# template — is not carried: every section is a ROUND 1).
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks764_577_780_799_880_985.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..21 a guard refused
"""

# 1. Replace the header (everything before `set -u`) wholesale.
marker = "set -u\n"
assert s.count(marker) == 1, "header marker"
s = NEW_HEADER + s[s.index(marker):]

# 2. Asserted block replacements.
OLD_VARS = """BRANCH='refs/heads/feature/ks-790-oauth-authorization_code-token-exchange-uses-getuserbyid'
HEAD_SHA="${QA982_HEAD:-e62eab87a6263e25c41c9bb814d5831842bb6c7e}"
MERGE_BASE='8861e62161466c40f08d2b10a30edeb203123993'
DEVELOP_SHA='8861e62161466c40f08d2b10a30edeb203123993'
"""
NEW_VARS = """BRANCH_799='refs/heads/feature/ks-764-security-decidekeyrevoke-has-no-organisation-arm-an'
BRANCH_880='refs/heads/kamilkreiser/ks-577-revoke-on-rotate'
BRANCH_985='refs/heads/feature/ks-780-normalise-org-id-into-shared'
HEAD_799="${QA799_HEAD:-6da848891924f859179d097d464a7b97c9783a6a}"
HEAD_880="${QA799_HEAD_880:-a704137de38a3055e40ee62adc343c0239f34ea9}"
HEAD_985="${QA799_HEAD_985:-fcd8a01e40d34d6cb4055e7b4fd58b9bb908bbe0}"
HEAD_SHA="$HEAD_799"
MERGE_BASE='8861e62161466c40f08d2b10a30edeb203123993'
DEVELOP_SHA='8861e62161466c40f08d2b10a30edeb203123993'
"""
OLD_HEADGUARD = """if ! git -C "$REPO" ls-remote origin "$BRANCH" | grep -q "^${HEAD_SHA}[[:space:]]"; then
  echo "REFUSING: $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA" >&2
  git -C "$REPO" ls-remote origin "$BRANCH" >&2
  exit 6
fi
"""
NEW_HEADGUARD = """# THREE heads, each pinned at its branch on origin (one ls-remote; a moved head names its PR).
LSR="$(git -C "$REPO" ls-remote origin "$BRANCH_799" "$BRANCH_880" "$BRANCH_985")"
for pair in "799:$HEAD_799:$BRANCH_799" "880:$HEAD_880:$BRANCH_880" "985:$HEAD_985:$BRANCH_985"; do
  pr="${pair%%:*}"; rest="${pair#*:}"; sha="${rest%%:*}"; br="${rest#*:}"
  if ! printf '%s\\n' "$LSR" | grep -q "^${sha}[[:space:]]${br}\\$"; then
    echo "REFUSING: #$pr — $sha is not at $br on origin — the head moved; the brief is about a different SHA" >&2
    printf '%s\\n' "$LSR" >&2
    exit 6
  fi
done
"""
OLD_MB = """ACTUAL_MB="$(
  set -a; . "$SECUURA_ENV"; set +a
  HEAD_SHA="$HEAD_SHA" python3 - <<'PY'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/develop..." + os.environ["HEAD_SHA"]
r = urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}))
print(json.load(r)["merge_base_commit"]["sha"])
PY
)"
[ -n "$ACTUAL_MB" ] || { echo "REFUSING: could not read the merge-base from the GitHub compare API" >&2; exit 13; }
[ "$ACTUAL_MB" = "$MERGE_BASE" ] || { echo "REFUSING: merge-base is now '$ACTUAL_MB', brief says '$MERGE_BASE'" >&2; exit 10; }
"""
NEW_MB = """# THREE compares (GitHub compare API), each asserted whole: develop...#799 head = M18 ahead 12 files 12 (the PR merged
# onto develop — develop is an ancestor); develop...#880 head = M18 ahead 4 files 5; the STACK-PARENT compare
# #799head...#985head = 6da848891 ahead 1 files 7 (a stacked PR is judged as the delta over its parent).
COMPARES="$(
  set -a; . "$SECUURA_ENV"; set +a
  HEAD_799="$HEAD_799" HEAD_880="$HEAD_880" HEAD_985="$HEAD_985" python3 - <<'PY'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/"
def cmp(a, b):
    r = urllib.request.urlopen(urllib.request.Request(api + a + "..." + b, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60)
    c = json.load(r)
    return "%s ahead=%d files=%d" % (c["merge_base_commit"]["sha"], c["ahead_by"], len(c.get("files") or []))
print("799=" + cmp("develop", os.environ["HEAD_799"]))
print("880=" + cmp("develop", os.environ["HEAD_880"]))
print("985=" + cmp(os.environ["HEAD_799"], os.environ["HEAD_985"]))
PY
)"
[ -n "$COMPARES" ] || { echo "REFUSING: could not read the three compares from the GitHub compare API" >&2; exit 13; }
C799="$(printf '%s\\n' "$COMPARES" | sed -n 's/^799=//p')"; C880="$(printf '%s\\n' "$COMPARES" | sed -n 's/^880=//p')"; C985="$(printf '%s\\n' "$COMPARES" | sed -n 's/^985=//p')"
[ "$C799" = "$MERGE_BASE ahead=12 files=12" ] || { echo "REFUSING: #799 develop...head reads '$C799', brief pins '$MERGE_BASE ahead=12 files=12'" >&2; exit 10; }
[ "$C880" = "$MERGE_BASE ahead=4 files=5" ]   || { echo "REFUSING: #880 develop...head reads '$C880', brief pins '$MERGE_BASE ahead=4 files=5'" >&2; exit 10; }
[ "$C985" = "$HEAD_799 ahead=1 files=7" ]      || { echo "REFUSING: #985 stack-parent compare reads '$C985', brief pins '$HEAD_799 ahead=1 files=7'" >&2; exit 10; }
"""
OLD_GUARDED = '''GUARDED = ["Blockchain/Dev/services/auth/src/routes/oauth.ts",
           "Blockchain/Dev/services/auth/src/__tests__/ks790-token-pre-auth-user-lookup.test.ts",
           "Blockchain/Dev/services/auth/src/__tests__/ks820-821-token-client-auth-and-apptype.test.ts",
           "Blockchain/Dev/services/auth/",
           "Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts",
           "Blockchain/Dev/migrations/039_rls_fail_closed.sql"]
'''
NEW_GUARDED = '''GUARDED = ["BACKLOG.md",
           "Blockchain/Dev/packages/shared/src/security/",
           "Blockchain/Dev/packages/shared/src/index.ts",
           "Blockchain/Dev/packages/shared/src/middleware/index.ts",
           "Blockchain/Dev/packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts",
           "Blockchain/Dev/packages/shared/src/__tests__/ks780-normalise-org-id-one-implementation.test.ts",
           "Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts",
           "Blockchain/Dev/services/security/src/index.ts",
           "Blockchain/Dev/services/security/src/keyRevokePolicy.ts",
           "Blockchain/Dev/services/security/src/__tests__/ks764-key-revoke-organisation-arm.test.ts",
           "Blockchain/Dev/services/security/src/__tests__/ks764-revoke-organisation-route-contract.test.ts",
           "Blockchain/Dev/services/security/src/__tests__/ks742-keys-tenancy-route-contract.test.ts",
           "Blockchain/Dev/services/security/src/__tests__/ks577-revoke-on-rotate.test.ts",
           "Blockchain/Dev/services/originate/src/routes/adminConfig.ts",
           "Blockchain/Dev/services/originate/src/middleware/auth.ts",
           "Blockchain/Dev/services/originate/src/services/orgId.ts",
           "Blockchain/Dev/services/originate/src/services/provenance.ts",
           "Blockchain/Dev/services/originate/src/services/gdprService.ts",
           "Blockchain/Dev/services/originate/src/routes/documents.ts",
           "Blockchain/Dev/services/originate/src/__tests__/ks764-admin-api-keys-revoke-route-contract.test.ts",
           "Blockchain/Dev/services/originate/src/__tests__/ks780-org-id-is-the-shared-implementation.test.ts",
           "Blockchain/Dev/services/originate/src/__tests__/ks695-erasure-by-external-ref.test.ts",
           "Blockchain/Dev/services/originate/src/__tests__/ks597-b-caller-scoped-externalref.test.ts",
           "Blockchain/Dev/services/originate/src/__tests__/ks597-issuer-org-bind.test.ts",
           "Blockchain/Dev/services/originate/src/__tests__/qa-f4-resolveonbehalfof-org-normalisation.test.ts",
           "Blockchain/Dev/services/auth/src/services/jwt.ts",
           "Blockchain/Dev/services/api-gateway/src/routes/platform.ts",
           "Blockchain/Dev/docs/openapi/secuura-api.yaml",
           "Blockchain/Dev/scripts/generate-openapi.ts",
           "Blockchain/Dev/services/tenant-provisioning/src/tenant-provisioning.openapi.ts"]
'''
OLD_CHECK = """if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  head $HEAD_SHA present at $BRANCH on origin"
  echo "  merge-base still $MERGE_BASE (GitHub compare API)"
  echo "  $DEV_NOTE"
"""
NEW_CHECK = """if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  head #799 $HEAD_799 present at $BRANCH_799 on origin; #880 $HEAD_880 at $BRANCH_880; #985 $HEAD_985 at $BRANCH_985"
  echo "  compares (GitHub API): develop...#799 = $C799; develop...#880 = $C880; #799...#985 = $C985"
  echo "  $DEV_NOTE"
"""
OLD_SHA20 = """grep -qF "$HEAD_SHA" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$BRIEF" \\
  || { echo "REFUSING: brief or prompt does not name the head SHA $HEAD_SHA — a gate about another SHA is another gate" >&2; exit 20; }
"""
NEW_SHA20 = """for sha in "$HEAD_799" "$HEAD_880" "$HEAD_985"; do
  grep -qF "$sha" "$PROMPT_FILE" && grep -qF "$sha" "$BRIEF" \\
    || { echo "REFUSING: brief or prompt does not name the head SHA $sha — a gate about another SHA is another gate" >&2; exit 20; }
done
"""
OLD_TAIL = """[ -z "${QA982_BRIEF:-}${QA982_PROMPT:-}${QA982_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
"""
NEW_TAIL = """[ -z "${QA799_BRIEF:-}${QA799_PROMPT:-}${QA799_HEAD:-}${QA799_HEAD_880:-}${QA799_HEAD_985:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
"""
subs = [
    (OLD_VARS, NEW_VARS, 1),
    ("DEVELOP_SHA='8861e62161466c40f08d2b10a30edeb203123993'\n", "DEVELOP_SHA='6e78961e1d04277ecbdb0537e630afa0bf63b13c'\n", 1),
    (OLD_HEADGUARD, NEW_HEADGUARD, 1),
    (OLD_MB, NEW_MB, 1),
    (OLD_GUARDED, NEW_GUARDED, 1),
    (OLD_CHECK, NEW_CHECK, 1),
    (OLD_SHA20, NEW_SHA20, 1),
    (OLD_TAIL, NEW_TAIL, 1),
    ("QA982_BRIEF", "QA799_BRIEF", 1), ("QA982_PROMPT", "QA799_PROMPT", 1),
    ("2026-09-14_secuura-982-ks790-tier1", "2026-09-14_secuura-799-880-ks764-577-tier1", 3),
    ('DEV_NOTE="origin develop still $DEVELOP_SHA (M18, the PR\'s parent and the develop this brief\'s 51/691 was written against; git ls-remote)"',
     'DEV_NOTE="origin develop still $DEVELOP_SHA (M19 = M18 + the KS-790 squash of three services/auth files; the merge-base of all three heads is M18 and the ratios 828/205/598/343, 195/13 and 835/601 were written against M18 = M19 for the four suites the gate runs; git ls-remote)"', 1),
    ('DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#DISJOINT } — disjoint from the guard\'s six paths (#982\'s three files, the services/auth/ prefix, the ks860 loopback guard file, migration 039); the gate merges the then-current develop, re-states the delta by name and re-derives the ratio (brief items 1 and 6)"',
     'DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#DISJOINT } — disjoint from the guard\'s thirty paths (the three PRs\' files, packages/shared/src/security/, the ks860 guard, ks742, jwt.ts, platform.ts, the yaml + its source + the generator, orgId.ts\'s callers and the four originate suites); the gate merges the then-current develop in its own clone, re-states the delta by name and re-derives every ratio (brief TARGET, items 2e/2f and the sections)"', 1),
    ('echo "  brief and prompt both name the head SHA $HEAD_SHA"', 'echo "  brief and prompt both name all three head SHAs"', 1),
]
for old, new, n in subs:
    c = s.count(old)
    if c != n:
        print(f"REFUSING: anchor {old[:70]!r} occurs {c} times, expected {n}", file=sys.stderr)
        sys.exit(1)
    s = s.replace(old, new)

# 3. Residual guard — nothing of the source gate may survive (outside the exact header sentence naming the template).
RESIDUAL = ["982", "790", "e62eab87a", "QA982", "oauth", "ks790", "ks820", "039_rls", "migration 039", "services/auth/\"", "691", "685", "M15", "M9 ", "50b729d69",
            "1c38077ba", "getUserByIdPreAuth", "qa982-", "#983", "#984", "six paths", "R1_REPORT", "exit 19", "TIER 2'", "ROUND 2", "tier2", "980", "977", "877", "$BRANCH\"", "$BRANCH ", "ACTUAL_MB"]
PERMITTED = ["Adapted from the #982 launcher", "(#982's squash \"KS-790: the OAuth token grants resolve the user through the pre-auth", "M18 + the KS-790 squash of three services/auth files"]
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
    (H799, 1), (H880, 1), (H985, 1), (M18, 1), ("6e78961e1d04277ecbdb0537e630afa0bf63b13c", 1), ("6da848891", 6), ("a704137de", 2), ("fcd8a01e4", 3), ("8861e6216", 2), ("6e78961e1", 2),
    ("QA799_BRIEF", 2), ("QA799_PROMPT", 2), ("QA799_HEAD", 6), ("QA799_HEAD_880", 2), ("QA799_HEAD_985", 2),
    ("2026-09-14_secuura-799-880-ks764-577-tier1.md", 2), ("2026-09-14_secuura-799-880-ks764-577-tier1.prompt.txt", 1),
    ("refs/heads/feature/ks-764-security-decidekeyrevoke-has-no-organisation-arm-an", 1), ("refs/heads/kamilkreiser/ks-577-revoke-on-rotate", 1),
    ("refs/heads/feature/ks-780-normalise-org-id-into-shared", 1),
    ("exit 21", 3), ("exit 20", 1), ("exit 18", 4), ("exit 10", 4), ("exit 6", 1), ("exit 13", 1), ("exit 16", 2), ("exit 7", 1), ("exit 15", 1), ("exit 9", 1),
    ("exit 8", 1), ("exit 11", 1), ("exit 12", 1), ("exit 14", 1), ("exit 17", 1), ("exit 2;", 1), ("exit 3;", 1), ("exit 4;", 1), ("exit 5;", 1),
    ("'TIER 1'", 2), ("'ROUND 1'", 2), ("[ -t 0 ]", 1), ("stdin is not a TTY", 2),
    ("ahead=12 files=12", 2), ("ahead=4 files=5", 2), ("ahead=1 files=7", 2), ("GUARDED", 5),
    ("Blockchain/Dev/packages/shared/src/security/", 1), ("ks860-test-listeners-bind-loopback.test.ts", 1), ("ks742-keys-tenancy-route-contract.test.ts", 2),
    ("Blockchain/Dev/services/security/src/index.ts", 1), ("Blockchain/Dev/services/originate/src/routes/adminConfig.ts", 1), ("Blockchain/Dev/services/auth/src/services/jwt.ts", 1),
    ("Blockchain/Dev/docs/openapi/secuura-api.yaml", 1), ("Blockchain/Dev/scripts/generate-openapi.ts", 1), ("tenant-provisioning.openapi.ts", 1),
    ("Blockchain/Dev/services/originate/src/services/orgId.ts", 1), ("qa-f4-resolveonbehalfof-org-normalisation.test.ts", 1), ("ks695-erasure-by-external-ref.test.ts", 1),
    ("MAIL YOUR VERDICT", 1), ("no memory maintenance", 1), ("NEVER print a credential value", 1), ("ultrathink", 1),
    ("exec claude --dangerously-skip-permissions --model opus", 1), ('cd "$QA_DIR"', 1),
    ("brief and prompt both name all three head SHAs", 1), ("brief and prompt agree on TIER 1 and ROUND 1", 1), ("a launch (not --check) will refuse unless stdin is a TTY", 1),
    ('g.endswith("/") and f["filename"].startswith(g)', 1), ("thirty paths", 1), ("M18", 10), ("M19", 4), ("KS-764", 1), ("KS-577", 2), ("KS-780", 2), ("#799", 17), ("#880", 9), ("#985", 11),
    ("R1_REPORT", 0), ("exit 19", 0), ("ACTUAL_MB", 0),
]
bad = [(tok, n, s.count(tok)) for tok, n in CONTROLS if s.count(tok) != n]
for tok, n, c in bad:
    print(f"REFUSING: output control {tok!r} occurs {c} times, expected {n}", file=sys.stderr)
if bad:
    sys.exit(3)
# the TTY guard must sit AFTER the --check block and BEFORE the override guard / cd / exec; the head loop before the compares before the develop pin
i_check = s.index('if [ "${1:-}" = "--check" ]; then'); i_tty = s.index('[ -t 0 ]'); i_ovr = s.index('a launch with test overrides set'); i_cd = s.index('cd "$QA_DIR"')
assert i_check < i_tty < i_ovr < i_cd, "TTY guard position"
i_heads = s.index('LSR="$('); i_cmp = s.index('COMPARES="$('); i_dev = s.index('CUR_DEV="$(')
assert i_heads < i_cmp < i_dev < i_check, "guard order"
b = s.encode("utf-8")
assert not [i for i, x in enumerate(b) if (x < 0x20 and x not in (9, 10, 13)) or x == 0x7f], "raw control byte in output"

open(out_path, "w", encoding="utf-8").write(s)
os.chmod(out_path, 0o755)
print(f"written {out_path} ({len(b)} bytes); {len(subs)} substitutions asserted; residual guard clean ({len(RESIDUAL)} tokens); {len(CONTROLS)} output controls")
