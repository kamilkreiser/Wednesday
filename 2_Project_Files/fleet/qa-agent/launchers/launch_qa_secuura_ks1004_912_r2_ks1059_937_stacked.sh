#!/bin/bash
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
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA912R2_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-912-ks1004-tier1-r2-937-ks1059-stacked.md}"
PROMPT_FILE="${QA912R2_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-912-ks1004-tier1-r2-937-ks1059-stacked.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-1004-anchor-failed-lockout'
BRANCH_937='refs/heads/feature/ks-1059-anchorstatesyncts360-removing-inflight-from-the-ks-587-sim'
HEAD_SHA="${QA912R2_HEAD:-609c44c55323b5c90320847b6837ca37f6586705}"
HEAD_937='6fd3a8bec4e4cc858d38925e00703a37ffcf1b30'
MERGE_BASE='8861e62161466c40f08d2b10a30edeb203123993'
DEVELOP_SHA='8861e62161466c40f08d2b10a30edeb203123993'
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-912-ks1004-tier1-r2-937-ks1059-stacked.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

if ! git -C "$REPO" ls-remote origin "$BRANCH" | grep -q "^${HEAD_SHA}[[:space:]]"; then
  echo "REFUSING: $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA" >&2
  git -C "$REPO" ls-remote origin "$BRANCH" >&2
  exit 6
fi
if ! git -C "$REPO" ls-remote origin "$BRANCH_937" | grep -q "^${HEAD_937}[[:space:]]"; then
  echo "REFUSING: $HEAD_937 is not at $BRANCH_937 on origin — the stacked head moved; the brief is about a different SHA" >&2
  git -C "$REPO" ls-remote origin "$BRANCH_937" >&2
  exit 22
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
[ "$STACK_READ" = "$HEAD_SHA ahead=4 files=1" ] \
  || { echo "REFUSING: the stacked delta is not ONE file over #912's head: compare reads '$STACK_READ', brief pins '$HEAD_SHA ahead=4 files=1' (merge order #912 -> #937 is the premise of section S)" >&2; exit 23; }

# The develop pin, disjointness-checked (see the header). GUARDED = the files whose movement changes this brief.
CUR_DEV="$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)"
[ -n "$CUR_DEV" ] || { echo "REFUSING: could not read origin develop (git ls-remote)" >&2; exit 18; }
if [ "$CUR_DEV" = "$DEVELOP_SHA" ]; then
  DEV_NOTE="origin develop still $DEVELOP_SHA (M18, the develop this brief's 56/598 and 57/602 were written against and BOTH heads already contain; git ls-remote)"
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
GUARDED = ["Blockchain/Dev/services/originate/src/services/anchorStateSync.ts",
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
# M21 CONTENT-JUDGED allowlist (KS-764, #799, commit 5210ddf317b2b1ed547e5d8488c3d011ceb087e1): these four paths
# fall under the GUARDED prefixes above but are cleared BY BLOB, not by path — a hit here is OK only if the
# compare API's own file entry for that path carries EXACTLY this blob sha (its content at M21, read once via
# `git rev-parse 5210ddf31:<path>` in the read-only checkout and pinned here); any other blob at that path — a
# further edit, a revert, anything else — is NOT cleared and falls through to GUARDED as before. Restart-drafter,
# Wednesday's 2026-09-14 12:1x instruction (the #984/#982-#983 precedent).
M21_ALLOWED = {
    "Blockchain/Dev/services/originate/src/__tests__/ks764-admin-api-keys-revoke-route-contract.test.ts": "5a78c4181281f360ebd4481593fd73bf98bb4d9c",
    "Blockchain/Dev/services/originate/src/middleware/auth.ts": "f08ee1a895bc878bc2656f649833706f665686e7",
    "Blockchain/Dev/services/originate/src/routes/adminConfig.ts": "26cec03de665ef75a8f6e4f2532dfc42a59a25b8",
    "Blockchain/Dev/packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts": "ab8e46d795d268822924a57e2630403be1963497",
}
hits = sorted({f["filename"] for f in files for g in GUARDED if f["filename"] == g or (g.endswith("/") and f["filename"].startswith(g))})
by_name = {f["filename"]: f for f in files}
cleared = sorted(h for h in hits if h in M21_ALLOWED and by_name.get(h, {}).get("sha") == M21_ALLOWED[h])
remaining = sorted(h for h in hits if h not in cleared)
if remaining:
    print("GUARDED " + " ".join(remaining)); sys.exit(0)
if cleared:
    print("ALLOWED commits=%d files=%d cleared=%s" % (c["ahead_by"], len(files), ",".join(cleared))); sys.exit(0)
print("DISJOINT commits=%d files=%d" % (c["ahead_by"], len(files)))
PYJ
  )"
  case "$DEV_JUDGEMENT" in
    DISJOINT*) DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#DISJOINT } — disjoint from the thirteen guarded paths (the five PR files, the services/originate/src/ prefix, the gateway verification.ts and its four tests, the packages/shared tests prefix, the root lockfile); the gate merges the then-current develop under BOTH heads, re-states the delta by name and re-derives the ratios (brief items 1, 2, 3, 4, 7; S1, S4)" ;;
    ALLOWED*) DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#ALLOWED } — the cleared files sit under a guarded prefix but were CONTENT-JUDGED against the pinned M21 blob (KS-764/#799), not path-excused; the gate merges the then-current develop under BOTH heads, RE-DERIVES the originate and packages/shared suite counts on its own farm (the brief's own counts for these are PREDICTIONS, predicted-by: drafter — a mismatch is a brief error, not a finding against the PR) and re-states every other delta by name (brief items 1, 2, 3, 4, 7; S1, S4)" ;;
    *) echo "REFUSING: origin develop is at $CUR_DEV, not the pinned $DEVELOP_SHA, and the delta is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher DEVELOP_SHA + brief TARGET + prompt)" >&2
       exit 18 ;;
  esac
fi

grep -q 'TIER 1' "$BRIEF" && grep -q 'TIER 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 7; }
grep -q 'ROUND 2' "$BRIEF" && grep -q 'ROUND 2' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round" >&2; exit 15; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$REAL_BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the brief path" >&2; exit 9; }
grep -qF "$HEAD_SHA" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$BRIEF" \
  || { echo "REFUSING: brief or prompt does not name the head SHA $HEAD_SHA — a gate about another SHA is another gate" >&2; exit 20; }
grep -qF "$HEAD_937" "$PROMPT_FILE" && grep -qF "$HEAD_937" "$BRIEF" \
  || { echo "REFUSING: brief or prompt does not name the stacked head SHA $HEAD_937 — a gate about another SHA is another gate" >&2; exit 20; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" || { echo "REFUSING: prompt does not tell the agent to MAIL its verdict" >&2; exit 12; }
grep -qi 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid pushing / running the hook in the real checkout" >&2; exit 11; }
grep -qi 'no memory maintenance' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid memory maintenance inside the gate session" >&2; exit 14; }
grep -qi 'NEVER print a credential value' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid printing a credential value" >&2; exit 17; }

R1_READ='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/reports/2026-09-09_secuura-ks1004-912-tier1-VERDICT.md'
grep -qF "$R1_READ" "$BRIEF" && grep -qF '5597511879' "$BRIEF" \
  || { echo "REFUSING: brief does not name the round-1 READ (the recovered tier-1 NO GO verdict file at $R1_READ and its transcription onto the PR, issue comment 5597511879) — a gate cannot ask" >&2; exit 19; }
[ -s "$R1_READ" ] || { echo "REFUSING: the round-1 read named by the brief is missing or empty: $R1_READ" >&2; exit 19; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  head $HEAD_SHA present at $BRANCH on origin"
  echo "  stacked head $HEAD_937 present at $BRANCH_937 on origin"
  echo "  merge-base still $MERGE_BASE (GitHub compare API)"
  echo "  stack relation still merge_base $HEAD_SHA / ONE file for 609c44c55...6fd3a8bec (GitHub compare API: $STACK_READ)"
  echo "  $DEV_NOTE"
  echo "  brief, prompt, QA project and repo all present"
  echo "  brief and prompt agree on TIER 1 and ROUND 2 (#912; #937 rides as TIER 2 ROUND 1 STACKED in the same files)"
  echo "  prompt opens with the thinking directive and names the brief"
  echo "  brief and prompt both name the head SHA $HEAD_SHA and the stacked head SHA $HEAD_937"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  brief names the round-1 read (the recovered NO GO verdict file + transcription comment 5597511879) and it is present on disk"
  echo "  (a real launch, not --check, additionally requires a TTY on stdin — exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent and must run in a pane (cockpit.sh add), never inside a Bash tool (a headless gate is invisible and dies with its caller; 2026-09-13 ledger)" >&2; exit 21; }
[ -z "${QA912R2_BRIEF:-}${QA912R2_PROMPT:-}${QA912R2_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
