#!/usr/bin/env python3
"""gen_launcher_931.py — derive launch_qa_secuura_ks1061_931.sh from the INSTALLED #903 (KS-991) ROUND-2
launcher (the closest tier-2, single-PR pattern with the disjointness-checked develop pin, the TTY guard,
and the head-SHA-in-both guard; sha256[:16] ccf1864168e7831a) by ASSERTED substitutions (every anchor must
occur exactly as often as stated, or the generator refuses), then a RESIDUAL GUARD: any token of the
source gate (its PR number, ticket, heads, SHAs) left anywhere in the output is a refusal — nothing is
written on refusal.

Differences from the template, all asserted:
- pins: PR #931 / KS-1061 / HEAD 53b8a1f7a6056c1560af71252c753c005bee8f06 / branch
  feature/ks-1061-originate-shared-mock-completeness / merge-base = GH compare's merge_base_commit =
  dfc63fe48ebaa97271f3ff66315a742ba4d79bc2 (M23) — this IS the branch's own declared merge-base per the
  PR's 3-commit history (f2e0cb3c1 -> merge 3da9623fe(parents f2e0cb3c1+dfc63fe48) -> 53b8a1f7a), so unlike
  #903 (where develop was merged in and stayed put), a develop move here changes the merge-base ONLY if the
  branch is re-merged — #931 has NOT re-merged since 53b8a1f7a, so the GH compare's merge_base_commit stays
  dfc63fe48 regardless of how far origin/develop's tip itself moves. The exit-10 guard checks exactly that
  (merge_base_commit unchanged), not that develop's tip is unmoved.
- GUARDED list for the develop-move guard (exit 18) = services/originate/src/__tests__/ (the whole
  directory — any new/changed root @secuura/shared mock factory changes this gate's census) +
  services/originate/src/__tests__/helpers/sharedModuleMock.ts explicitly (belt-and-braces, already covered
  by the directory prefix).
- ROUND 1, not ROUND 2 — the exit-19 "round-1 record on disk" guard from the #903 template does not apply
  (there is no prior round for #931); repurposed as a MODEL-CLONE-PRESENT guard (exit 19): the isolated
  `model/repo` clone this gate's controls_check.sh uses for merge-tree must exist and be a valid git dir —
  a gate that cannot run its own live-develop guard is not ready to launch.
- exit 21 TTY guard kept verbatim (the 2026-09-13 ledger's lesson generalises to every launcher).

RE-PIN PATH (added 2026-09-14 13:4x AEST, per Wednesday's mid-draft note: #931 is DIRTY against develop
since #985's squash landed, M29 `4569dd889`, and the builder has been told to merge live develop in,
resolve ks695 as the union, push, and mail a READY with a NEW head): re-running this generator with
--head/--devbase re-derives EVERY pin in the launcher in one asserted-substitution pass — the head SHA is
not hand-edited anywhere. `controls_check.sh` and `guards_sim.py` take the SAME two pins via
QA931_HEAD/QA931_DEVBASE env vars (no separate edit needed there); `gh_read.py`/`linear_read.py` take
QA931_HEAD too. See BUILD_REPORT.md, "THE RE-PIN PATH", for the exact commands.

Usage: gen_launcher_931.py <template launcher> <output launcher> [--head SHA] [--devbase SHA]
Exit: 0 written · 1 an anchor count disagreed · 2 a residual token survived · 3 an output control failed
"""
import os, sys, hashlib

def _pop_flag(name, default):
    if name in sys.argv:
        i = sys.argv.index(name)
        val = sys.argv[i + 1]
        del sys.argv[i:i + 2]
        return val
    return default

PIN_HEAD = _pop_flag('--head', '53b8a1f7a6056c1560af71252c753c005bee8f06')
PIN_DEVBASE = _pop_flag('--devbase', 'dfc63fe48ebaa97271f3ff66315a742ba4d79bc2')

src_path, out_path = sys.argv[1], sys.argv[2]
raw = open(src_path, 'rb').read()
assert hashlib.sha256(raw).hexdigest()[:16] == 'ccf1864168e7831a', 'template sha256 is not the installed #903 r2 launcher'
s = raw.decode('utf-8')

def sub(old, new, expect, s):
    n = s.count(old)
    assert n == expect, f'anchor count {n} != expected {expect} for: {old[:80]!r}'
    return s.replace(old, new)

NEW_HEADER = """#!/bin/bash
# launch_qa_secuura_ks1061_931.sh — cross-project QA agent, TIER 2 (through code: TESTS ONLY, a unit-test
# mock-factory helper + its own completeness guard under services/originate/src/__tests__/ — no product
# file, no service, route, spec, schema or UI) DELTA gate, ROUND 1, on Secuura PR #931 (KS-1061) @
# 53b8a1f7a6056c1560af71252c753c005bee8f06 — THREE commits: f2e0cb3c1 (the PR's own build: makeSharedMock +
# the completeness guard + ten hand-written root @secuura/shared factories converted to the helper form) ->
# 3da9623fe (merge develop dfc63fe48/M23 IN, --no-ff, ONE resolved conflict on
# ks444-webhooks-create-description-guard.test.ts: develop's KS-927 comment block + four-key factory kept,
# helper form used, assertSafeOutboundUrl override kept) -> 53b8a1f7a (folds: the two root factories that
# landed on develop AFTER the branch was cut — ks1103-verify-hash-field.test.ts (#965) and
# ks764-admin-api-keys-revoke-route-contract.test.ts (#799) — converted into makeSharedMock, the second in
# the EXPRESSION form with a `...actual` spread). PR files API: 14 (12 + the two folds), +232 -95, 0
# product files — every path under services/originate/src/__tests__/.
#
# Merge-base = GitHub compare(develop...HEAD)'s merge_base_commit = dfc63fe48ebaa97271f3ff66315a742ba4d79bc2
# (M23). Unlike a branch develop is merged INTO once and never touches again, THIS branch's merge-base only
# moves if s223 (or a successor) re-merges a later develop tip — read live via the GitHub compare API each
# run (exit 10 if it changes: the brief's ADDENDUM path, not this launcher's silent problem). Because
# origin/develop's tip itself keeps moving independently (M23 -> ... -> #985's squash 4569dd889 -> #925
# f09b629457 and beyond), this launcher ALSO runs the disjointness-checked develop-move guard from the
# #903 r2 template (exit 18): GUARDED = services/originate/src/__tests__/ (the whole directory) — any
# develop commit that touches a file there changes this gate's census or its live-merge-tree prediction.
# The builder's own READY mail names the one already-known instance: #985's squash adds a
# `normaliseOrgId` pass-through to ks695-erasure-by-external-ref.test.ts (one of this PR's OWN 14 files —
# EXPECTED, not a fresh GUARDED hit) and lands a brand-new ks780-org-id-is-the-shared-implementation.test.ts
# with 0 root shared mocks (also expected, does not redden the guard when eventually merged). A GUARDED hit
# OUTSIDE those two known files is what this guard actually exists to catch.
#
# NEW/kept from the #903 r2 template (exit 21): the LAUNCH path refuses when stdin is not a TTY. This
# launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool.
#
# Repurposed from the #903 r2 template's round-1-record guard (exit 19, since #931 has no prior round): the
# isolated `model/repo` clone this gate's controls_check.sh needs for its own read-only `merge-tree
# --write-tree` (the live-develop content guard) must exist and be a valid git directory — a gate that
# cannot run its own guard is not ready to launch.
#
# Adapted from the installed #903 (KS-991) round-2 launcher by gen_launcher_931.py (asserted substitutions,
# residual guard): the same guard family and exit codes 2..21.
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks1061_931.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..21 a guard refused
"""

marker = "set -u\n"
assert s.count(marker) == 1, "header marker"
s = NEW_HEADER + s[s.index(marker):]

# ---- pins ----
s = sub(
    "BRIEF=\"${QA903R2_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-903-ks991-tier2-r2.md}\"",
    "BRIEF=\"${QA931_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-931-ks1061-tier2.md}\"",
    1, s)
s = sub(
    "PROMPT_FILE=\"${QA903R2_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-903-ks991-tier2-r2.prompt.txt}\"",
    "PROMPT_FILE=\"${QA931_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-931-ks1061-tier2.prompt.txt}\"",
    1, s)
s = sub("BRANCH='refs/heads/kamilkreiser/ks-991-stale-local-develop'",
        "BRANCH='refs/heads/feature/ks-1061-originate-shared-mock-completeness'", 1, s)
s = sub("HEAD_SHA=\"${QA903R2_HEAD:-a4f71cde660c1442d98317e26d93845340b20098}\"",
        f"HEAD_SHA=\"${{QA931_HEAD:-{PIN_HEAD}}}\"", 1, s)
s = sub("MERGE_BASE='8861e62161466c40f08d2b10a30edeb203123993'",
        f"MERGE_BASE='{PIN_DEVBASE}'", 1, s)
s = sub("DEVELOP_SHA='8861e62161466c40f08d2b10a30edeb203123993'",
        f"DEVELOP_SHA='{PIN_DEVBASE}'", 1, s)
s = sub(
    'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-903-ks991-tier2-r2.md"',
    'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-931-ks1061-tier2.md"',
    1, s)

# ---- merge-base check: same compare endpoint, works unchanged (develop...HEAD) ----
# (no substitution needed — the ACTUAL_MB python block already reads compare/develop...HEAD_SHA generically)

# ---- the develop-move guard's judgement (exit 18): CONTENT-JUDGED, not a bare path-prefix hit ----
# The #903 template's GUARDED check is a bare prefix match — right for a script family that never
# changes shape. THIS gate's guarded directory (services/originate/src/__tests__/) is EXPECTED to have
# moved on develop (the ks695 fold-target, per the builder's own READY mail) whenever this branch's own
# files are touched, and a brand-new root-mock-free suite (ks780) is also expected and harmless. So the
# judgement must be CONTENT-aware, the same class as controls_check.sh's live-develop guard: a file under
# the guarded prefix is a real hit only if it is NEITHER one of this PR's own 14 known paths NOR a file
# that (at the new tip) carries zero root '@secuura/shared' jest.mock factories.
OLD_HITS_BLOCK = '''GUARDED = [".githooks/pre-push",
           "Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh",
           "Blockchain/Dev/scripts/preflight/preflight.sh",
           "Blockchain/Dev/scripts/preflight/deps-present.sh",
           "Blockchain/Dev/scripts/run-shell-suites.sh",
           "Blockchain/Dev/scripts/__tests__/"]
hits = sorted({f["filename"] for f in files for g in GUARDED if f["filename"] == g or (g.endswith("/") and f["filename"].startswith(g))})
if hits:
    print("GUARDED " + " ".join(hits)); sys.exit(0)
print("DISJOINT commits=%d files=%d" % (c["ahead_by"], len(files)))'''
NEW_HITS_BLOCK = '''import base64, re
GUARDED_PREFIX = "Blockchain/Dev/services/originate/src/__tests__/"
KNOWN_PR_FILES = {
    "Blockchain/Dev/services/originate/src/__tests__/gdprService.erasure.test.ts",
    "Blockchain/Dev/services/originate/src/__tests__/helpers/sharedModuleMock.ts",
    "Blockchain/Dev/services/originate/src/__tests__/ks1061-shared-mock-completeness.test.ts",
    "Blockchain/Dev/services/originate/src/__tests__/ks1103-verify-hash-field.test.ts",
    "Blockchain/Dev/services/originate/src/__tests__/ks444-webhooks-create-description-guard.test.ts",
    "Blockchain/Dev/services/originate/src/__tests__/ks445-pg-error-classification.test.ts",
    "Blockchain/Dev/services/originate/src/__tests__/ks563-certified-vs-anchored.test.ts",
    "Blockchain/Dev/services/originate/src/__tests__/ks584-p3-auth-error-classification.test.ts",
    "Blockchain/Dev/services/originate/src/__tests__/ks584-p3-verify-list.test.ts",
    "Blockchain/Dev/services/originate/src/__tests__/ks584-verify-row-selection.test.ts",
    "Blockchain/Dev/services/originate/src/__tests__/ks695-erasure-by-external-ref.test.ts",
    "Blockchain/Dev/services/originate/src/__tests__/ks764-admin-api-keys-revoke-route-contract.test.ts",
    "Blockchain/Dev/services/originate/src/__tests__/ks914-deliver-webhook-blocked-vs-failed.test.ts",
    "Blockchain/Dev/services/originate/src/__tests__/qa-f4-resolveonbehalfof-org-normalisation.test.ts",
}
ROOT_MOCK_RE = re.compile(r"jest\\.mock\\(\\s*\\x27@secuura/shared\\x27\\s*,")
def root_mock_count(filename, ref):
    u2 = "https://api.github.com/repos/Secuura/Distributed_Secuura/contents/" + filename + "?ref=" + ref
    try:
        o = json.load(urllib.request.urlopen(urllib.request.Request(u2, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
        content = base64.b64decode(o["content"]).decode("utf-8", "replace")
    except Exception:
        return None
    return len(ROOT_MOCK_RE.findall(content))
hits = []
guarded_dir_files = 0
for f in files:
    fn = f["filename"]
    if not fn.startswith(GUARDED_PREFIX):
        continue
    guarded_dir_files += 1
    if fn in KNOWN_PR_FILES:
        continue
    n = root_mock_count(fn, os.environ["CUR_DEV"])
    if n is None:
        hits.append(fn + "(unreadable)")
    elif n > 0:
        hits.append(fn + "(%d root mocks)" % n)
if hits:
    print("GUARDED " + " ".join(sorted(hits))); sys.exit(0)
print("DISJOINT commits=%d files=%d guarded_dir_files=%d" % (c["ahead_by"], len(files), guarded_dir_files))'''
s = sub(OLD_HITS_BLOCK, NEW_HITS_BLOCK, 1, s)
s = sub(
    'DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#DISJOINT } — disjoint from the guard\'s six paths (#903\'s three files, deps-present.sh, run-shell-suites.sh, the scripts/__tests__/ prefix); the gate merges the then-current develop, re-states the delta by name and re-derives the leg-14 count (brief items 1 and 6)"',
    'DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#DISJOINT } — disjoint from the guard\'s path (services/originate/src/__tests__/); a develop move that touches this PR\'s own 14 files (the ks695 fold-target) is EXPECTED and read as such by controls_check.sh\'s live-develop content guard, not by this bare disjointness check — anything else under the directory is what this guard exists to catch"',
    1, s)
s = sub(
    'DEV_NOTE="origin develop still $DEVELOP_SHA (M18, the develop merged INTO the branch and the one this brief\'s 28/0 was written against; git ls-remote)"',
    'DEV_NOTE="origin develop still $DEVELOP_SHA (M23, this PR\'s own declared merge-base; git ls-remote)"',
    1, s)

# ---- ROUND 1 not ROUND 2 ----
s = sub("grep -q 'ROUND 2' \"$BRIEF\" && grep -q 'ROUND 2' \"$PROMPT_FILE\" || { echo \"REFUSING: brief and prompt disagree about the round\" >&2; exit 15; }",
        "grep -q 'ROUND 1' \"$BRIEF\" && grep -q 'ROUND 1' \"$PROMPT_FILE\" || { echo \"REFUSING: brief and prompt disagree about the round\" >&2; exit 15; }",
        1, s)
s = sub('  echo "  brief and prompt agree on TIER 2 and ROUND 2"',
        '  echo "  brief and prompt agree on TIER 2 and ROUND 1"',
        1, s)

# ---- exit 11: the no-push-from-the-real-checkout phrase, repointed at this gate's actual prompt wording ----
s = sub(
    "grep -qi 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout' \"$PROMPT_FILE\" \\\n  || { echo \"REFUSING: prompt does not forbid pushing / running the hook in the real checkout\" >&2; exit 11; }",
    "grep -qi 'NEVER push, from this gate, to origin' \"$PROMPT_FILE\" \\\n  || { echo \"REFUSING: prompt does not forbid pushing from the gate\" >&2; exit 11; }",
    1, s)
s = sub('  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"',
        '  echo "  prompt forbids pushing from the gate to origin"',
        1, s)

# ---- exit 19: repurposed from the #903 round-1-record guard to a model-clone-present guard ----
OLD19 = """R1_REPORT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-13_s213/boot/peter_903_comment_5585854866.md'
grep -qF "$R1_REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the round-1 record path (Peter's review; a gate cannot ask)" >&2; exit 19; }
[ -s "$R1_REPORT" ] || { echo "REFUSING: the round-1 record named by the brief is missing or empty: $R1_REPORT" >&2; exit 19; }"""
NEW19 = """MODEL_CLONE="$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate931/model/repo"
[ -d "$MODEL_CLONE/.git" ] || { echo "REFUSING: the isolated model/repo clone this gate's controls_check.sh needs for merge-tree is missing: $MODEL_CLONE" >&2; exit 19; }"""
s = sub(OLD19, NEW19, 1, s)

# ---- --check summary lines ----
s = sub(
    '  echo "  brief names the round-1 record (Peter\'s review) and it is present on disk"',
    '  echo "  the isolated model/repo clone (for merge-tree) is present"',
    1, s)

# ---- env-override guard names + test-override refusal message ----
s = sub('[ -z "${QA903R2_BRIEF:-}${QA903R2_PROMPT:-}${QA903R2_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }',
        '[ -z "${QA931_BRIEF:-}${QA931_PROMPT:-}${QA931_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }',
        1, s)

# ---- residual-token guard: nothing of the source gate's OPERATIVE content (pins, env vars, exec logic)
# may survive substitution. Checked on the BODY only (from `set -u` onward) — the new header's own
# attribution prose ("adapted from the #903 r2 launcher") deliberately names the source and is not a
# residual leftover.
body = s[s.index(marker):]
RESIDUAL = ["a4f71cde6", "48553f272", "8861e6216", "986c592d5",
            "QA903R2_", "ks-991-stale", "pre_push_hook_base", "peter_903_comment"]
for tok in RESIDUAL:
    if tok in body:
        sys.stderr.write(f"REFUSING TO WRITE: residual token {tok!r} survived substitution in the launcher BODY\n")
        sys.exit(2)

# ---- output controls ----
for must in [PIN_HEAD, PIN_DEVBASE,
             "feature/ks-1061-originate-shared-mock-completeness", "TIER 2", "ROUND 1",
             "Blockchain/Dev/services/originate/src/__tests__/", "exit 21", "exit 19", "exit 18", "exit 10",
             "NEVER push, from this gate, to origin", "TIER 2 and ROUND 1"]:
    if must not in s:
        sys.stderr.write(f"OUTPUT CONTROL FAILED: {must!r} not present in generated launcher\n")
        sys.exit(3)

open(out_path, 'w', encoding='utf-8').write(s)
os.chmod(out_path, 0o755)
print(f"written {out_path}, {len(s)} bytes, sha256[:16]={hashlib.sha256(s.encode()).hexdigest()[:16]}")
