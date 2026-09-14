#!/bin/bash
# launch_qa_secuura_L5_799_880_985.sh — cross-project QA agent, ONE gate over the THREE READY PRs of lane L5
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
# M18, ahead 12, behind 2 at M20, TWELVE files) — so the head tree IS the PR merged onto M18, and the PR merged onto
# M20 is the 3-way tree 16ea40dc3 (0 conflicts; = the head's PR blobs + M20's six develop files). #880's head is ONE fix
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
# origin develop = M20 a5334350221c819f54d4a20a3308daeb9ca09617 (#903's squash "KS-991: skip a local develop that
# origin/develop provably supersedes", 2026-09-13T23:18:09Z; read 10:38 and 10:41 AEST 2026-09-14) — TWO squashes past
# M18 8861e6216 (the builder's cut; the merge-base of all three heads, unchanged): M19 6e78961e1 (#982, three files
# under services/auth/) and M20 (#903: .githooks/pre-push, scripts/__tests__/pre_push_hook_base.test.sh,
# scripts/preflight/preflight.sh) — SIX files, disjoint from every guarded path below, MEASURED: every develop blob the
# brief cites is the same at M18 and M20 and the five suite subtrees the gate runs are byte-identical M18 = M20. The
# merges onto M20 in Wednesday's own clone: #799 -> 16ea40dc3, #880 -> 2246dae85, #985 -> 42a6fb6c5, 0 conflicts each.
# (The first drafter's launcher pinned M19 and judged the M19..M20 move DISJOINT at 09:18; this one is the deliberate
# re-pin to M20.) The develop pin below is
# DISJOINTNESS-CHECKED, not bare: if origin develop has moved past M20, the GitHub compare of that delta is read and the launcher REFUSES (exit 18) only when the
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
# Adapted from the first L5 drafter's three-head launcher (gatesets/2026-09-14_gate799, template sha256 d11f93e0af26962f;
# itself from the #982 launcher) by gen_launcher_L5.py (asserted substitutions: the M20 re-pin, the L5 names, the QAL5_
# overrides, the header and --check wording; residual guard): the same guard family and exit codes 2..18, 20, 21 (code 19 — the round-1-report guard of the older
# template — is not carried: every section is a ROUND 1).
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_L5_799_880_985.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..21 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QAL5_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-L5-799-880-985-ks764-577-780-tier1.md}"
PROMPT_FILE="${QAL5_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-L5-799-880-985-ks764-577-780-tier1.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH_799='refs/heads/feature/ks-764-security-decidekeyrevoke-has-no-organisation-arm-an'
BRANCH_880='refs/heads/kamilkreiser/ks-577-revoke-on-rotate'
BRANCH_985='refs/heads/feature/ks-780-normalise-org-id-into-shared'
HEAD_799="${QAL5_HEAD:-6da848891924f859179d097d464a7b97c9783a6a}"
HEAD_880="${QAL5_HEAD_880:-a704137de38a3055e40ee62adc343c0239f34ea9}"
HEAD_985="${QAL5_HEAD_985:-fcd8a01e40d34d6cb4055e7b4fd58b9bb908bbe0}"
HEAD_SHA="$HEAD_799"
MERGE_BASE='8861e62161466c40f08d2b10a30edeb203123993'
DEVELOP_SHA='a5334350221c819f54d4a20a3308daeb9ca09617'
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-L5-799-880-985-ks764-577-780-tier1.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# THREE heads, each pinned at its branch on origin (one ls-remote; a moved head names its PR).
LSR="$(git -C "$REPO" ls-remote origin "$BRANCH_799" "$BRANCH_880" "$BRANCH_985")"
for pair in "799:$HEAD_799:$BRANCH_799" "880:$HEAD_880:$BRANCH_880" "985:$HEAD_985:$BRANCH_985"; do
  pr="${pair%%:*}"; rest="${pair#*:}"; sha="${rest%%:*}"; br="${rest#*:}"
  if ! printf '%s\n' "$LSR" | grep -q "^${sha}[[:space:]]${br}\$"; then
    echo "REFUSING: #$pr — $sha is not at $br on origin — the head moved; the brief is about a different SHA" >&2
    printf '%s\n' "$LSR" >&2
    exit 6
  fi
done

# THREE compares (GitHub compare API), each asserted whole: develop...#799 head = M18 ahead 12 files 12 (the PR merged
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
C799="$(printf '%s\n' "$COMPARES" | sed -n 's/^799=//p')"; C880="$(printf '%s\n' "$COMPARES" | sed -n 's/^880=//p')"; C985="$(printf '%s\n' "$COMPARES" | sed -n 's/^985=//p')"
[ "$C799" = "$MERGE_BASE ahead=12 files=12" ] || { echo "REFUSING: #799 develop...head reads '$C799', brief pins '$MERGE_BASE ahead=12 files=12'" >&2; exit 10; }
[ "$C880" = "$MERGE_BASE ahead=4 files=5" ]   || { echo "REFUSING: #880 develop...head reads '$C880', brief pins '$MERGE_BASE ahead=4 files=5'" >&2; exit 10; }
[ "$C985" = "$HEAD_799 ahead=1 files=7" ]      || { echo "REFUSING: #985 stack-parent compare reads '$C985', brief pins '$HEAD_799 ahead=1 files=7'" >&2; exit 10; }

# The develop pin, disjointness-checked (see the header). GUARDED = the files whose movement changes this brief.
CUR_DEV="$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)"
[ -n "$CUR_DEV" ] || { echo "REFUSING: could not read origin develop (git ls-remote)" >&2; exit 18; }
if [ "$CUR_DEV" = "$DEVELOP_SHA" ]; then
  DEV_NOTE="origin develop still $DEVELOP_SHA (M20 = M18 + #982's three services/auth files + #903's hook / shell test / preflight.sh; the merge-base of all three heads is M18; the five suite subtrees are byte-identical M18 = M20, so the ratios 828/205/598/343, 195/13 and 835/601 hold; the merges onto M20 are 16ea40dc3 / 2246dae85 / 42a6fb6c5, 0 conflicts; git ls-remote)"
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
GUARDED = ["BACKLOG.md",
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
hits = sorted({f["filename"] for f in files for g in GUARDED if f["filename"] == g or (g.endswith("/") and f["filename"].startswith(g))})
if hits:
    print("GUARDED " + " ".join(hits)); sys.exit(0)
print("DISJOINT commits=%d files=%d" % (c["ahead_by"], len(files)))
PYJ
  )"
  case "$DEV_JUDGEMENT" in
    DISJOINT*) DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#DISJOINT } — disjoint from the guard's thirty paths (the three PRs' files, packages/shared/src/security/, the ks860 guard, ks742, jwt.ts, platform.ts, the yaml + its source + the generator, orgId.ts's callers and the four originate suites); the gate merges the then-current develop in its own clone, re-states the delta by name and re-derives every ratio (brief TARGET, items 2e/2f and the sections)" ;;
    *) echo "REFUSING: origin develop is at $CUR_DEV, not the pinned $DEVELOP_SHA, and the delta is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher DEVELOP_SHA + brief TARGET + prompt)" >&2
       exit 18 ;;
  esac
fi

grep -q 'TIER 1' "$BRIEF" && grep -q 'TIER 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 7; }
grep -q 'ROUND 1' "$BRIEF" && grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round" >&2; exit 15; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$REAL_BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the brief path" >&2; exit 9; }
for sha in "$HEAD_799" "$HEAD_880" "$HEAD_985"; do
  grep -qF "$sha" "$PROMPT_FILE" && grep -qF "$sha" "$BRIEF" \
    || { echo "REFUSING: brief or prompt does not name the head SHA $sha — a gate about another SHA is another gate" >&2; exit 20; }
done
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" || { echo "REFUSING: prompt does not tell the agent to MAIL its verdict" >&2; exit 12; }
grep -qi 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid pushing / running the hook in the real checkout" >&2; exit 11; }
grep -qi 'no memory maintenance' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid memory maintenance inside the gate session" >&2; exit 14; }
grep -qi 'NEVER print a credential value' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid printing a credential value" >&2; exit 17; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  head #799 $HEAD_799 present at $BRANCH_799 on origin; #880 $HEAD_880 at $BRANCH_880; #985 $HEAD_985 at $BRANCH_985"
  echo "  compares (GitHub API): develop...#799 = $C799; develop...#880 = $C880; #799...#985 = $C985"
  echo "  $DEV_NOTE"
  echo "  brief, prompt, QA project and repo all present"
  echo "  brief and prompt agree on TIER 1 and ROUND 1"
  echo "  prompt opens with the thinking directive and names the brief"
  echo "  brief and prompt both name all three head SHAs"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QAL5_BRIEF:-}${QAL5_PROMPT:-}${QAL5_HEAD:-}${QAL5_HEAD_880:-}${QAL5_HEAD_985:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
