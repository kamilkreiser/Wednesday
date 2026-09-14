#!/bin/bash
# launch_qa_secuura_L9_940_941_942.sh — cross-project QA agent, TIER 2 (CI workflow config + a shell test harness — no
# service, route, spec, schema or UI; through code AND the LIVE GitHub Actions runs at each head as the artefact, read at the
# Actions API — never dispatched, never re-run) gate ROUND 1, ONE PASS over THREE Secuura Platform K PRs of the L9
# ci-workflows lane (Wednesday's ruling: one test pass proves the three; the verdict is PER PR; the MERGE of every
# `.github/workflows` PR is Kam's — `kam-merges`):
#   #940 (KS-1075) @ 1aa708be9 — security-scan.yml: ONE `shell: bash {0}` line on the Audit-contract step (+ its comment
#        block; the stale "Actions is retired … inert" comment corrected). 1 file +22 -3 on merge-base a1e49d151. ZERO code
#        this round; the live run 34426409872 / job 102712486541 / step 7 is the artefact: the step FAILS WITH ITS REASON
#        PRINTED (`ℹ tests 59 · pass 52 · fail 7`, seven `audit-locks:` ✖, `audit-contract suites are red`, exit 1) where
#        #941's run 34427102258 / job 102714559749 step 7 fails with ZERO output (the pre-fix swallow — the control).
#   #941 (KS-1077) @ d105e07a8 — the SAME security-scan.yml: the SCA gate re-pointed from check-npm-audit.mjs +
#        .security/exceptions.yml to scripts/audit/audit-gate.mjs (+ the exit-code case table under `shell: bash {0}`,
#        continue-on-error on PRs kept) and a 22-line SUPERSEDED banner on exceptions.yml (kept, not deleted). 2 files
#        +64 -10 on a1e49d151. Live: run 34427102258 step 6 PASSES `audit-gate: 36 distinct advisories reported, 38
#        baselined.` / `OK — no advisories outside the triaged baseline`. AFTER #940 (same file, disjoint hunks: #941's
#        end :108, #940's start :114 at the base): #941's head does NOT carry #940's line (its audit-contract step is
#        still `bash -e`); the 3-way merge of the two heads is CLEAN (merged blob dc728543b, 527 lines, both `shell: bash
#        {0}` lines at :121 and :175) — no rebase needed; the merge seat re-checks after #940 lands.
#   #942 (KS-1078) @ 53b9c3cc1 — pr-security-gates.yml: one `npm install --global --no-audit --no-fund tsx@4.23.12` step
#        immediately before the shell suites; manifest_quarantine.test.sh: the probe's `2>&1` -> `2>"$TMP/probe.err"` + a
#        3-line stdout/stderr diagnostic; BACKLOG.md +17 (the deferred quarantine_call_sites item). The head is the
#        original c1676269d + ONE --no-ff merge of develop M18 (parents c1676269d + 8861e6216; two resolutions:
#        manifest_quarantine.test.sh:66 = develop's `env -u …` prefix + this PR's redirect; BACKLOG.md both-append, develop's
#        block first). develop is an ANCESTOR of the head (0 behind / 2 ahead) so the head tree a4c7ef372 IS the merged
#        shape; the delta vs develop is exactly 3 files +53 -2. Live: run 34785721609 / job 103800717960: step 11 the pin
#        `added 3 packages in 2s` (a real install), step 12 `shell suites: 27 passed, 2 failed (of 29)` with
#        manifest_quarantine `14 passed, 0 failed` and the two FAILED = develop's own (control run 34755906436 / job
#        103720115281 at M18: the same two, the same 27/2) — ATTRIBUTED to KS-1148, never graded against #942.
#
# THE PINS. origin develop M18 8861e6216 (#980's squash, 12:00:26Z 2026-09-13; read 08:16:49 AEST 2026-09-14 by ls-remote and
# 08:20 AEST by /branches/develop — unmoved since the builder's cut). The three heads by ls-remote (exit 6 for any that moved).
# The three GitHub compares (exit 10): develop...#940 and develop...#941 must read merge_base a1e49d151, ahead 1, files 1 / 2;
# develop...#942 must read merge_base = the pinned develop, ahead 2, files 3. The three LIVE RUNS the brief names are the
# artefacts the gate reads: each must still answer at the Actions API with head_sha = the pinned head (exit 21 — a deleted or
# expired run is a gate about nothing). The develop pin is judged by CONTENT on the lane's two workflow files (GitHub contents
# API): security-scan.yml blob 47da5cac9 (M18) -> green; fac9ef1b8 (#940 landed as its own squash), 3b272c2d9 (#941 landed
# first) or dc728543b (both landed) -> exit 19, a PR of this pass has LANDED and its section is moot — rewrite the brief;
# any other blob -> exit 18. pr-security-gates.yml blob 571817703 (M18) -> green; eac30f09b (#942 landed) -> exit 19; other ->
# exit 18. Any OTHER file of a develop move under the GUARDED prefixes — .github/workflows/, Blockchain/Dev/.security/,
# Blockchain/Dev/scripts/audit/, scripts/run-shell-suites.sh, systemTest/__tests__/manifest_quarantine.test.sh,
# systemTest/__tests__/ (a new or moved shell suite changes the 27/2 of 29 ratio) — -> exit 18; otherwise the launcher
# proceeds and prints the move, which the gate re-states (brief TARGET).
#
# Refuses when stdin is not a TTY (exit 22) unless run with --check: this launcher execs an interactive agent; run inside a
# Bash tool it runs headless, invisible and parented to the caller's shell (2026-09-13, Wednesday's own #962 instance).
#
# Adapted from the INSTALLED #983 launcher by gen_launcher_L9.py (asserted substitutions, four asserted block replacements,
# residual guard): same guard family and exit codes 2..22 (exit 21 = a named live run is gone or at another head; exit 22 =
# no TTY), re-pointed at the three heads.
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_L9_940_941_942.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..22 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QAL9_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-L9-940-941-942-ks1075-1077-1078-tier2.md}"
PROMPT_FILE="${QAL9_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-L9-940-941-942-ks1075-1077-1078-tier2.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH940='refs/heads/feature/ks-1075-ci-gate-diagnostics'
BRANCH941='refs/heads/feature/ks-1077-single-audit-allowlist'
BRANCH942='refs/heads/feature/ks-1078-tsx-probe-capture'
HEAD940="${QAL9_HEAD940:-1aa708be9fcf7a23575398546d84848c967e81c5}"
HEAD941="${QAL9_HEAD941:-d105e07a81c8549b7f47c0542e9594204ce6f599}"
HEAD942="${QAL9_HEAD942:-53b9c3cc1a89f513620516c580a5de5bd60c64de}"
BASE_940_941='a1e49d15152102acec7c97d96918211227c7fe1e'   # the merge-base of #940 and #941 (#934's merge, 2026-09-10)
RUN940='34426409872'; RUN941='34427102258'; RUN942='34785721609'   # the live artefacts (Security Scanning / Security Scanning / PR Security Gates)
DEVELOP_SHA='8861e62161466c40f08d2b10a30edeb203123993'
SCAN_FILE='.github/workflows/security-scan.yml'
GATES_FILE='.github/workflows/pr-security-gates.yml'
SCAN_BLOB_OK='47da5cac924cbe6c58edce8bba7593b81e13257b'                                                                   # M18 = the PRs' base copy
SCAN_BLOBS_LANDED='fac9ef1b89d53884d3655e3e50ea73c54c9a022a 3b272c2d9ecbd9ab130390ca22c1ac06ac40c27d dc728543b91ba5a93037911a72ceca0700b2eabe'   # #940 landed · #941 landed · both
GATES_BLOB_OK='571817703e76b167d2275748e6e455e35b8affb1'                                                                  # M18
GATES_BLOB_LANDED='eac30f09b461bd4fd270ba4da1d24423a53255c1'                                                              # #942 landed
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-L9-940-941-942-ks1075-1077-1078-tier2.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# THREE heads, one pass: every one must still be at its branch on origin (the verdict is per PR, on these SHAs).
LSR="$(git -C "$REPO" ls-remote origin "$BRANCH940" "$BRANCH941" "$BRANCH942")"
for pair in "$HEAD940 $BRANCH940" "$HEAD941 $BRANCH941" "$HEAD942 $BRANCH942"; do
  h="${pair%% *}"; b="${pair#* }"
  if ! printf '%s\n' "$LSR" | grep -q "^${h}[[:space:]]${b}\$"; then
    echo "REFUSING: $h is not at $b on origin — the head moved; the brief is about a different SHA" >&2
    printf '%s\n' "$LSR" >&2
    exit 6
  fi
done

# THIS GATE'S OWN GUARD: the three LIVE RUNS are the artefacts (tier 2, CI config: the run at the head is the behaviour).
# Each named run must still answer at the Actions API with head_sha = the pinned head; a deleted, expired or re-attributed
# run makes the brief's decisive lines unreadable — refuse rather than let the gate quote a run it cannot open.
RUN_READ="$(
  set -a; . "$SECUURA_ENV"; set +a
  RUN940="$RUN940" RUN941="$RUN941" RUN942="$RUN942" HEAD940="$HEAD940" HEAD941="$HEAD941" HEAD942="$HEAD942" python3 - <<'PYR'
import json, os, sys, urllib.request, urllib.error
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura"
out = []
for rid, head, tag in ((os.environ["RUN940"], os.environ["HEAD940"], "940"), (os.environ["RUN941"], os.environ["HEAD941"], "941"), (os.environ["RUN942"], os.environ["HEAD942"], "942")):
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(api + "/actions/runs/" + rid, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
    except urllib.error.HTTPError as e:
        print("GONE #%s run %s HTTP %d" % (tag, rid, e.code)); sys.exit(0)
    except Exception as e:
        print("UNREADABLE #%s run %s %s" % (tag, rid, type(e).__name__)); sys.exit(0)
    if r.get("head_sha") != head:
        print("MOVED #%s run %s is at head %s, not the pinned %s" % (tag, rid, str(r.get("head_sha"))[:9], head[:9])); sys.exit(0)
    out.append("#%s run %s %s/%s at %s" % (tag, rid, r.get("status"), r.get("conclusion"), head[:9]))
print("OK " + " · ".join(out))
PYR
)"
case "$RUN_READ" in
  OK*) RUN_NOTE="${RUN_READ#OK }" ;;
  *) echo "REFUSING: a live run this brief reads as its artefact is not where the brief says: ${RUN_READ:-no answer} — re-read the runs at the heads and rewrite the brief's live-run items" >&2; exit 21 ;;
esac

# The three compares: #940 and #941 sit on a1e49d151 (ONE commit each, 1 / 2 files); #942's merge-base is the pinned develop
# itself (the head carries the --no-ff merge of M18: ahead 2, 3 files). A different merge-base or shape is a different PR.
CMP_READ="$(
  set -a; . "$SECUURA_ENV"; set +a
  HEAD940="$HEAD940" HEAD941="$HEAD941" HEAD942="$HEAD942" python3 - <<'PY'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/develop..."
res = []
for tag in ("940", "941", "942"):
    c = json.load(urllib.request.urlopen(urllib.request.Request(api + os.environ["HEAD" + tag], headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
    res.append("#%s mb=%s ahead=%d files=%d" % (tag, c["merge_base_commit"]["sha"], c["ahead_by"], len(c.get("files") or [])))
print(" | ".join(res))
PY
)"
[ -n "$CMP_READ" ] || { echo "REFUSING: could not read the three compares from the GitHub compare API" >&2; exit 13; }
CMP_WANT="#940 mb=$BASE_940_941 ahead=1 files=1 | #941 mb=$BASE_940_941 ahead=1 files=2 | #942 mb=$DEVELOP_SHA ahead=2 files=3"
[ "$CMP_READ" = "$CMP_WANT" ] || { echo "REFUSING: the three compares do not read as the brief pins them: got '$CMP_READ', brief pins '$CMP_WANT'" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): the lane's two workflow files by blob on develop — a landing of #940,
# #941 or #942 moves one of them to a blob this brief KNOWS (exit 19: that PR's section is moot; rewrite); an unknown blob is
# exit 18. Any other develop move is judged by the GUARDED prefixes; a disjoint move is printed and the gate re-states it.
CUR_DEV="$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)"
[ -n "$CUR_DEV" ] || { echo "REFUSING: could not read origin develop (git ls-remote)" >&2; exit 18; }
DEV_JUDGEMENT="$(
  set -a; . "$SECUURA_ENV"; set +a
  DEVELOP_SHA="$DEVELOP_SHA" CUR_DEV="$CUR_DEV" SCAN_FILE="$SCAN_FILE" GATES_FILE="$GATES_FILE" \
  SCAN_BLOB_OK="$SCAN_BLOB_OK" SCAN_BLOBS_LANDED="$SCAN_BLOBS_LANDED" GATES_BLOB_OK="$GATES_BLOB_OK" GATES_BLOB_LANDED="$GATES_BLOB_LANDED" python3 - <<'PYJ'
import json, os, sys, urllib.request
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura"
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
cur = os.environ["CUR_DEV"]; pinned = os.environ["DEVELOP_SHA"]
scan_f = os.environ["SCAN_FILE"]; gates_f = os.environ["GATES_FILE"]
try:
    scan_blob = get("/contents/" + scan_f + "?ref=" + cur)["sha"]
    gates_blob = get("/contents/" + gates_f + "?ref=" + cur)["sha"]
except Exception as e:
    print("UNJUDGEABLE develop blob unreadable: " + type(e).__name__); sys.exit(0)
landed = os.environ["SCAN_BLOBS_LANDED"].split()
scan_state = "M18" if scan_blob == os.environ["SCAN_BLOB_OK"] else ("LANDED " + ["#940", "#941", "#940+#941"][landed.index(scan_blob)] if scan_blob in landed else "OTHER")
gates_state = "M18" if gates_blob == os.environ["GATES_BLOB_OK"] else ("LANDED #942" if gates_blob == os.environ["GATES_BLOB_LANDED"] else "OTHER")
if scan_state.startswith("LANDED") or gates_state.startswith("LANDED"):
    print("LANDEDL9 develop's security-scan.yml blob " + scan_blob[:9] + " (" + scan_state + ") / pr-security-gates.yml blob " + gates_blob[:9] + " (" + gates_state + ") — a PR of this pass has landed; its section is moot"); sys.exit(0)
if scan_state == "OTHER" or gates_state == "OTHER":
    print("GUARDED develop's security-scan.yml blob " + scan_blob[:9] + " (" + scan_state + ") / pr-security-gates.yml blob " + gates_blob[:9] + " (" + gates_state + ") — a version nobody pinned"); sys.exit(0)
state = "develop's security-scan.yml blob " + scan_blob[:9] + " = M18; pr-security-gates.yml blob " + gates_blob[:9] + " = M18 (the three heads' base copies)"
if cur == pinned:
    print("OK " + state + " | origin develop still " + pinned + " (M18; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [".github/workflows/",
           "Blockchain/Dev/.security/",
           "Blockchain/Dev/scripts/audit/",
           "scripts/run-shell-suites.sh",
           "systemTest/__tests__/manifest_quarantine.test.sh",
           "systemTest/__tests__/"]
hits = sorted({x["filename"] for x in files for g in GUARDED if x["filename"] == g or (g.endswith("/") and x["filename"].startswith(g))})
if hits:
    print("GUARDED " + " ".join(hits)); sys.exit(0)
shell_suites = sum(1 for x in files if x["filename"].endswith(".test.sh"))
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d (.test.sh files %d) — disjoint from the two judged files (by blob) and the six GUARDED prefixes; the gate re-reads develop at start and end, re-derives #942's merged shape onto the then-current tip in its own clone and re-states the step-12 ratio (brief TARGET: develop's own shell-suite count, 2 develop-own reds, manifest_quarantine green)" % (pinned, cur, c["ahead_by"], len(files), shell_suites)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDEDL9*) echo "REFUSING: ${DEV_JUDGEMENT#LANDEDL9 } (develop $CUR_DEV) — rewrite the brief for the PRs still open" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, re-state the ratio, then re-pin deliberately (launcher DEVELOP_SHA/*_BLOB_OK + brief TARGET + prompt)" >&2
     exit 18 ;;
esac

grep -q 'TIER 2' "$BRIEF" && grep -q 'TIER 2' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 7; }
grep -q 'ROUND 1' "$BRIEF" && grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round" >&2; exit 15; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$REAL_BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the brief path" >&2; exit 9; }
for h in "$HEAD940" "$HEAD941" "$HEAD942"; do
  grep -qF "$h" "$PROMPT_FILE" && grep -qF "$h" "$BRIEF" \
    || { echo "REFUSING: brief or prompt does not name the head SHA $h — a gate about another SHA is another gate" >&2; exit 20; }
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
  echo "  heads $HEAD940 / $HEAD941 / $HEAD942 present at their branches on origin"
  echo "  compares: $CMP_READ (GitHub compare API)"
  echo "  live runs: $RUN_NOTE (Actions API)"
  echo "  $DEV_NOTE"
  echo "  brief, prompt, QA project and repo all present"
  echo "  brief and prompt agree on TIER 2 and ROUND 1"
  echo "  prompt opens with the thinking directive and names the brief"
  echo "  brief and prompt both name all three head SHAs"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  exit 0
fi

[ -z "${QAL9_BRIEF:-}${QAL9_PROMPT:-}${QAL9_HEAD940:-}${QAL9_HEAD941:-}${QAL9_HEAD942:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
# A launch needs a terminal: this execs an interactive agent. Inside a Bash tool there is no TTY and the gate would run
# headless, invisible and parented to the caller's shell (2026-09-13 ledger). --check never reaches this line.
[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — launch this from a pane (cockpit.sh add), never from inside a Bash tool" >&2; exit 22; }
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
