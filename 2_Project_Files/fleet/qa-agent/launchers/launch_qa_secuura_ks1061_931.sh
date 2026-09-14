#!/bin/bash
# launch_qa_secuura_ks1061_931.sh — cross-project QA agent, TIER 2 (through code: TESTS ONLY, a unit-test
# mock-factory helper + its own completeness guard under services/originate/src/__tests__/ — no product
# file, no service, route, spec, schema or UI) DELTA gate, ROUND 1, on Secuura PR #931 (KS-1061) @
# 7953070230d285fdebc0c65b834ac8340c02c0b6 — RE-PINNED 2026-09-14 ~13:5x AEST: the round-1 head MOVED from
# 53b8a1f7a6056c1560af71252c753c005bee8f06 (now SUPERSEDED — never gate it) to this one, a FOURTH commit
# `795307023` = a second develop merge-in (parents 53b8a1f7a + b9f541e6b/M31, which contains #985's
# 4569dd889) resolving the ks695-erasure-by-external-ref.test.ts conflict as the UNION: the helper form with
# #985's `normaliseOrgId` pass-through kept as an override (never a stub) — builder-measured guard 3/3,
# ks695 40/40, ks780-org-id-* 3/3, whole originate 58 suites/604 tests, tamper T5 (the pass-through deleted)
# reds ks695 10/40. Commits: f2e0cb3c1 (the PR's own build) -> 3da9623fe (merge M23) -> 53b8a1f7a (the two
# folds: ks1103 + ks764) -> 795307023 (merge M31, the ks695 union). PR files API: 14, +236 -99, 0 product
# files — every path under services/originate/src/__tests__/ (the same 14-file SET as the superseded head;
# only ks695's own bytes changed further, by the union resolution).
#
# Merge-base = GitHub compare(develop...HEAD)'s merge_base_commit = b9f541e6b158f831576ecc870244f361f219a114
# (M31 — moved from M23 dfc63fe48 because THIS head re-merged a later develop tip, exactly the re-pin this
# header now documents). Unlike a branch develop is merged INTO once and never touches again, THIS branch's
# merge-base only moves if s223 (or a successor) re-merges a later develop tip — read live via the GitHub
# compare API each run (exit 10 if it changes again: the brief's ADDENDUM path, not this launcher's silent
# problem). Because origin/develop's tip itself keeps moving independently, this launcher ALSO runs the
# disjointness-checked develop-move guard from the
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
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA931_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-931-ks1061-tier2.md}"
PROMPT_FILE="${QA931_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-931-ks1061-tier2.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-1061-originate-shared-mock-completeness'
HEAD_SHA="${QA931_HEAD:-7953070230d285fdebc0c65b834ac8340c02c0b6}"
MERGE_BASE='b9f541e6b158f831576ecc870244f361f219a114'
DEVELOP_SHA='b9f541e6b158f831576ecc870244f361f219a114'
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-931-ks1061-tier2.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

if ! git -C "$REPO" ls-remote origin "$BRANCH" | grep -q "^${HEAD_SHA}[[:space:]]"; then
  echo "REFUSING: $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA" >&2
  git -C "$REPO" ls-remote origin "$BRANCH" >&2
  exit 6
fi

ACTUAL_MB="$(
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

# The develop pin, disjointness-checked (see the header). GUARDED = the files whose movement changes this brief.
CUR_DEV="$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)"
[ -n "$CUR_DEV" ] || { echo "REFUSING: could not read origin develop (git ls-remote)" >&2; exit 18; }
if [ "$CUR_DEV" = "$DEVELOP_SHA" ]; then
  DEV_NOTE="origin develop still $DEVELOP_SHA (M31, this PR's own declared merge-base after the ks695-union re-pin; git ls-remote)"
else
  DEV_JUDGEMENT="$(
    set -a; . "$SECUURA_ENV"; set +a
    DEVELOP_SHA="$DEVELOP_SHA" CUR_DEV="$CUR_DEV" python3 - <<'PYJ'
import json, os, sys, urllib.request
t = os.environ.get("GH_TOKEN", "")
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/" + os.environ["DEVELOP_SHA"] + "..." + os.environ["CUR_DEV"]
try:
    c = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
import base64, re
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
ROOT_MOCK_RE = re.compile(r"jest\.mock\(\s*\x27@secuura/shared\x27\s*,")
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
print("DISJOINT commits=%d files=%d guarded_dir_files=%d" % (c["ahead_by"], len(files), guarded_dir_files))
PYJ
  )"
  case "$DEV_JUDGEMENT" in
    DISJOINT*) DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#DISJOINT } — disjoint from the guard's path (services/originate/src/__tests__/); a develop move that touches this PR's own 14 files (the ks695 fold-target) is EXPECTED and read as such by controls_check.sh's live-develop content guard, not by this bare disjointness check — anything else under the directory is what this guard exists to catch" ;;
    *) echo "REFUSING: origin develop is at $CUR_DEV, not the pinned $DEVELOP_SHA, and the delta is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher DEVELOP_SHA + brief TARGET + prompt)" >&2
       exit 18 ;;
  esac
fi

grep -q 'TIER 2' "$BRIEF" && grep -q 'TIER 2' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 7; }
grep -q 'ROUND 1' "$BRIEF" && grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round" >&2; exit 15; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$REAL_BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the brief path" >&2; exit 9; }
grep -qF "$HEAD_SHA" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$BRIEF" \
  || { echo "REFUSING: brief or prompt does not name the head SHA $HEAD_SHA — a gate about another SHA is another gate" >&2; exit 20; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" || { echo "REFUSING: prompt does not tell the agent to MAIL its verdict" >&2; exit 12; }
grep -qi 'NEVER push, from this gate, to origin' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid pushing from the gate" >&2; exit 11; }
grep -qi 'no memory maintenance' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid memory maintenance inside the gate session" >&2; exit 14; }
grep -qi 'NEVER print a credential value' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid printing a credential value" >&2; exit 17; }

MODEL_CLONE="$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate931/model/repo"
[ -d "$MODEL_CLONE/.git" ] || { echo "REFUSING: the isolated model/repo clone this gate's controls_check.sh needs for merge-tree is missing: $MODEL_CLONE" >&2; exit 19; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  head $HEAD_SHA present at $BRANCH on origin"
  echo "  merge-base still $MERGE_BASE (GitHub compare API)"
  echo "  $DEV_NOTE"
  echo "  brief, prompt, QA project and repo all present"
  echo "  brief and prompt agree on TIER 2 and ROUND 1"
  echo "  prompt opens with the thinking directive and names the brief"
  echo "  brief and prompt both name the head SHA $HEAD_SHA"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing from the gate to origin"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  the isolated model/repo clone (for merge-tree) is present"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QA931_BRIEF:-}${QA931_PROMPT:-}${QA931_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
