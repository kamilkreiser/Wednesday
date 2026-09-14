#!/usr/bin/env python3
"""gen_launcher_L9.py — derive launch_qa_secuura_L9_940_941_942_887.sh from the INSTALLED #983 launcher (the tracked template
carrying the exit-21 second-ref guard, the exit-22 no-TTY guard, the exit-20 head-in-both guard and the disjointness-checked
develop pin) by ASSERTED substitutions (every anchor must occur exactly as often as stated, or the generator refuses),
FOUR asserted block replacements (the head guard -> a loop over FOUR heads; the stack-parent guard -> the live-run
artefact guard; the merge-base guard -> the four GitHub compares; the develop judgement -> blob-judged on the lane's two
workflow files + GUARDED prefixes), the --check echo block rewritten, then a RESIDUAL GUARD: any token of the source gate
(its PR number, ticket, head, stack parent, env-override prefix, its guarded paths, its ratios) left anywhere in the
output is a refusal — nothing is written on refusal. Same method as gen_launcher_983.py / gen_launcher_984.py.

Usage: gen_launcher_L9.py <template launcher> <output launcher>
Exit: 0 written · 1 an anchor count disagreed · 2 a residual token survived · 3 an output control failed
"""
import os, sys

src_path, out_path = sys.argv[1], sys.argv[2]
s = open(src_path, encoding="utf-8").read()

NEW_HEADER = """#!/bin/bash
# launch_qa_secuura_L9_940_941_942_887.sh — cross-project QA agent, TIER 2 (CI workflow config + a shell test harness — no
# service, route, spec, schema or UI; through code AND the LIVE GitHub Actions runs at each head as the artefact, read at the
# Actions API — never dispatched, never re-run) gate ROUND 1, ONE PASS over THREE Secuura Platform K PRs of the L9
# ci-workflows lane PLUS its fourth PR #887 (Wednesday's rulings: one test pass proves the three; #887 added as a fourth
# section 08:3x AEST; the verdict is PER PR; the MERGE of every `.github/workflows` PR is Kam's — `kam-merges`):
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
#   #887 (KS-961) @ 3aee3deed — pr-platform-suites.yml: the `workspace-suites` advisory job (+97, continue-on-error: true,
#        the hunk Peter reviewed at cb7a3e3be — his COMMENTED review 5153400898 "the change I asked for is in… One re-run
#        before I approve"; his approval is HIS act; `mergeable: blocked` = his standing CHANGES_REQUESTED at bb0502c80 — the
#        gate states it, never chases him) + DEV-PROCESS.md (+50 -2 vs develop). This round = cb7a3e3be + de376a9f1 (a
#        clean --no-ff merge of develop M18; the workflow blob moves 8607f9bf2 -> fd5e8343c by develop's OWN +15 -2 hunk at
#        :314 on another job — no seat line) + 3aee3deed (ONE doc-only commit, DEV-PROCESS.md +15 -11 inside the PR's own
#        section: a second dated baseline column + the "cannot run today" sentence dated). develop is an ANCESTOR (0 behind /
#        5 ahead); the delta vs develop is exactly 2 files +147 -2. Peter's ONE re-run posted on the PR facts-only (comment
#        5656613944): at cb7a3e3be 40 s · 26 · 6 · exit 1 · 2 failing (anchoring 1/172, originate 2/515) — LANDS ON 2; at the
#        merged tree 58 s · 26 · 6 · exit 1 · 1 failing (anchoring 1/208; originate 0/588); OpenSSL 3.6.3. The push
#        preflight PASSED 11/14 (3/4/8 SKIP by HOLD; leg 14 29/29). Live: `pr` run 34786655660 / job `Workspace unit suites
#        (advisory, non-blocking)` 103803259738 — the job's FIRST execution anywhere: counts 26 / 6, npm ci green, step 6
#        Build FAILS on demo-overlay + outlook-addin (`Cannot find module @rollup/rollup-linux-x64-gnu` — the root lockfile
#        carries only rollup-darwin-arm64; npm/cli#4828), step 7 SKIPPED — a lockfile/platform defect, NOT #887's (advisory;
#        blocks nothing; Wednesday's filing call).
#
# THE PINS. origin develop M18 8861e6216 (#980's squash, 12:00:26Z 2026-09-13; read 08:16:49 AEST 2026-09-14 by ls-remote and
# 08:20 AEST by /branches/develop — unmoved since the builder's cut). The four heads by ls-remote (exit 6 for any that moved).
# The four GitHub compares (exit 10): develop...#940 and develop...#941 must read merge_base a1e49d151, ahead 1, files 1 / 2;
# develop...#942 must read merge_base = the pinned develop, ahead 2, files 3; develop...#887 the pinned develop, ahead 5,
# files 2. The four LIVE RUNS the brief names are the
# artefacts the gate reads: each must still answer at the Actions API with head_sha = the pinned head (exit 21 — a deleted or
# expired run is a gate about nothing). The develop pin is judged by CONTENT on the lane's three workflow files (GitHub contents
# API): security-scan.yml blob 47da5cac9 (M18) -> green; fac9ef1b8 (#940 landed as its own squash), 3b272c2d9 (#941 landed
# first) or dc728543b (both landed) -> exit 19, a PR of this pass has LANDED and its section is moot — rewrite the brief;
# any other blob -> exit 18. pr-security-gates.yml blob 571817703 (M18) -> green; eac30f09b (#942 landed) -> exit 19; other ->
# exit 18. pr-platform-suites.yml blob a509ad793 (M18) -> green; fd5e8343c (#887 landed) -> exit 19; other -> exit 18. Any
# OTHER file of a develop move under the GUARDED prefixes — .github/workflows/, Blockchain/Dev/.security/,
# Blockchain/Dev/scripts/audit/, scripts/run-shell-suites.sh, systemTest/__tests__/manifest_quarantine.test.sh,
# systemTest/__tests__/ (a new or moved shell suite changes the 27/2 of 29 ratio), Blockchain/Dev/docs/DEV-PROCESS.md and
# Blockchain/Dev/package-lock.json (#887's doc and the lockfile its live red rests on) — -> exit 18; otherwise the launcher
# proceeds and prints the move, which the gate re-states (brief TARGET).
#
# Refuses when stdin is not a TTY (exit 22) unless run with --check: this launcher execs an interactive agent; run inside a
# Bash tool it runs headless, invisible and parented to the caller's shell (2026-09-13, Wednesday's own #962 instance).
#
# Adapted from the INSTALLED #983 launcher by gen_launcher_L9.py (asserted substitutions, four asserted block replacements,
# residual guard): same guard family and exit codes 2..22 (exit 21 = a named live run is gone or at another head; exit 22 =
# no TTY), re-pointed at the four heads.
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_L9_940_941_942_887.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..22 a guard refused
"""

marker = "set -u\n"
assert s.count(marker) == 1, "header marker"
s = NEW_HEADER + s[s.index(marker):]

# 2. asserted substitutions
subs = [
    ("QA983_BRIEF", "QAL9_BRIEF", 2),
    ("QA983_PROMPT", "QAL9_PROMPT", 2),
    ("QA983_HEAD", "QAL9_HEAD", 2),   # the HEAD_SHA default line (replaced by the three-head block below) + the override guard
    ("2026-09-14_secuura-983-ks823-tier1", "2026-09-14_secuura-L9-940-941-942-887-ks1075-1077-1078-961-tier2", 3),
    ("grep -q 'TIER 1' \"$BRIEF\" && grep -q 'TIER 1' \"$PROMPT_FILE\"", "grep -q 'TIER 2' \"$BRIEF\" && grep -q 'TIER 2' \"$PROMPT_FILE\"", 1),
    ('echo "  brief and prompt agree on TIER 1 and ROUND 1"', 'echo "  brief and prompt agree on TIER 2 and ROUND 1"', 1),
    ("re-pin deliberately (launcher DEVELOP_SHA + brief TARGET + prompt)", "re-pin deliberately (launcher DEVELOP_SHA/*_BLOB_OK + brief TARGET + prompt)", 1),
]
for old, new, n in subs:
    c = s.count(old)
    if c != n:
        print(f"REFUSING: anchor {old[:90]!r} occurs {c} times, expected {n}", file=sys.stderr); sys.exit(1)
    s = s.replace(old, new)

# 3. block replacement 1 — the pins + the single-head guard -> three heads, three branches
OLD_PINS_START = "BRANCH='refs/heads/feature/ks-823-security-the-apioauthtoken-refresh_token-grant-authenticates'\n"
OLD_PINS_END = "DEVELOP_SHA='8861e62161466c40f08d2b10a30edeb203123993'\n"
assert s.count(OLD_PINS_START) == 1 and s.count(OLD_PINS_END) == 1, "pins block"
i0 = s.index(OLD_PINS_START); i1 = s.index(OLD_PINS_END) + len(OLD_PINS_END)
NEW_PINS = """BRANCH940='refs/heads/feature/ks-1075-ci-gate-diagnostics'
BRANCH941='refs/heads/feature/ks-1077-single-audit-allowlist'
BRANCH942='refs/heads/feature/ks-1078-tsx-probe-capture'
BRANCH887='refs/heads/feature/ks-961-workspace-suites-advisory-on-pr'
HEAD940="${QAL9_HEAD940:-1aa708be9fcf7a23575398546d84848c967e81c5}"
HEAD941="${QAL9_HEAD941:-d105e07a81c8549b7f47c0542e9594204ce6f599}"
HEAD942="${QAL9_HEAD942:-53b9c3cc1a89f513620516c580a5de5bd60c64de}"
HEAD887="${QAL9_HEAD887:-3aee3deed2e3ac557f0a52c0797c2a4a8df25f69}"
BASE_940_941='a1e49d15152102acec7c97d96918211227c7fe1e'   # the merge-base of #940 and #941 (#934's merge, 2026-09-10)
RUN940='34426409872'; RUN941='34427102258'; RUN942='34785721609'; RUN887='34786655660'   # the live artefacts (Security Scanning ×2 / PR Security Gates / pr)
DEVELOP_SHA='8861e62161466c40f08d2b10a30edeb203123993'
SCAN_FILE='.github/workflows/security-scan.yml'
GATES_FILE='.github/workflows/pr-security-gates.yml'
SCAN_BLOB_OK='47da5cac924cbe6c58edce8bba7593b81e13257b'                                                                   # M18 = the PRs' base copy
SCAN_BLOBS_LANDED='fac9ef1b89d53884d3655e3e50ea73c54c9a022a 3b272c2d9ecbd9ab130390ca22c1ac06ac40c27d dc728543b91ba5a93037911a72ceca0700b2eabe'   # #940 landed · #941 landed · both
GATES_BLOB_OK='571817703e76b167d2275748e6e455e35b8affb1'                                                                  # M18
GATES_BLOB_LANDED='eac30f09b461bd4fd270ba4da1d24423a53255c1'                                                              # #942 landed
SUITES_FILE='.github/workflows/pr-platform-suites.yml'
SUITES_BLOB_OK='a509ad7934a50cd3f96c7241d9445b942c638cb7'                                                                 # M18
SUITES_BLOB_LANDED='fd5e8343c6392ec35b2abc5c38d305a945896b71'                                                             # #887 landed (its head's blob = the merged shape)
"""
s = s[:i0] + NEW_PINS + s[i1:]

OLD_HEADGUARD = """if ! git -C "$REPO" ls-remote origin "$BRANCH" | grep -q "^${HEAD_SHA}[[:space:]]"; then
  echo "REFUSING: $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA" >&2
  git -C "$REPO" ls-remote origin "$BRANCH" >&2
  exit 6
fi
"""
assert s.count(OLD_HEADGUARD) == 1, "head guard"
NEW_HEADGUARD = """# FOUR heads, one pass: every one must still be at its branch on origin (the verdict is per PR, on these SHAs).
LSR="$(git -C "$REPO" ls-remote origin "$BRANCH940" "$BRANCH941" "$BRANCH942" "$BRANCH887")"
for pair in "$HEAD940 $BRANCH940" "$HEAD941 $BRANCH941" "$HEAD942 $BRANCH942" "$HEAD887 $BRANCH887"; do
  h="${pair%% *}"; b="${pair#* }"
  if ! printf '%s\\n' "$LSR" | grep -q "^${h}[[:space:]]${b}\\$"; then
    echo "REFUSING: $h is not at $b on origin — the head moved; the brief is about a different SHA" >&2
    printf '%s\\n' "$LSR" >&2
    exit 6
  fi
done
"""
s = s.replace(OLD_HEADGUARD, NEW_HEADGUARD)

# 4. block replacement 2 — the stack-parent guard -> the live-run artefact guard (exit 21)
OLD_SP_START = "# THIS GATE'S OWN GUARD: #983 is STACKED on #982."
OLD_SP_END = "  exit 21\nfi\n"
assert s.count(OLD_SP_START) == 1 and s.count(OLD_SP_END) == 1, "stack-parent block"
i0 = s.index(OLD_SP_START); i1 = s.index(OLD_SP_END) + len(OLD_SP_END)
NEW_SP = """# THIS GATE'S OWN GUARD: the four LIVE RUNS are the artefacts (tier 2, CI config: the run at the head is the behaviour).
# Each named run must still answer at the Actions API with head_sha = the pinned head; a deleted, expired or re-attributed
# run makes the brief's decisive lines unreadable — refuse rather than let the gate quote a run it cannot open.
RUN_READ="$(
  set -a; . "$SECUURA_ENV"; set +a
  RUN940="$RUN940" RUN941="$RUN941" RUN942="$RUN942" RUN887="$RUN887" HEAD940="$HEAD940" HEAD941="$HEAD941" HEAD942="$HEAD942" HEAD887="$HEAD887" python3 - <<'PYR'
import json, os, sys, urllib.request, urllib.error
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura"
out = []
for rid, head, tag in ((os.environ["RUN940"], os.environ["HEAD940"], "940"), (os.environ["RUN941"], os.environ["HEAD941"], "941"), (os.environ["RUN942"], os.environ["HEAD942"], "942"), (os.environ["RUN887"], os.environ["HEAD887"], "887")):
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
"""
s = s[:i0] + NEW_SP + s[i1:]

# 5. block replacement 3 — the single merge-base guard -> the three compares (exit 10 / 13)
OLD_MB_START = 'ACTUAL_MB="$(\n'
OLD_MB_END = '[ "$ACTUAL_MB" = "$MERGE_BASE" ] || { echo "REFUSING: merge-base is now \'$ACTUAL_MB\', brief says \'$MERGE_BASE\'" >&2; exit 10; }\n'
assert s.count(OLD_MB_START) == 1 and s.count(OLD_MB_END) == 1, "merge-base block"
i0 = s.index(OLD_MB_START); i1 = s.index(OLD_MB_END) + len(OLD_MB_END)
NEW_MB = """# The four compares: #940 and #941 sit on a1e49d151 (ONE commit each, 1 / 2 files); #942's and #887's merge-base is the pinned
# develop itself (each head carries a --no-ff merge of M18: ahead 2 / 3 files, ahead 5 / 2 files). A different merge-base or
# shape is a different PR.
CMP_READ="$(
  set -a; . "$SECUURA_ENV"; set +a
  HEAD940="$HEAD940" HEAD941="$HEAD941" HEAD942="$HEAD942" HEAD887="$HEAD887" python3 - <<'PY'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/develop..."
res = []
for tag in ("940", "941", "942", "887"):
    c = json.load(urllib.request.urlopen(urllib.request.Request(api + os.environ["HEAD" + tag], headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
    res.append("#%s mb=%s ahead=%d files=%d" % (tag, c["merge_base_commit"]["sha"], c["ahead_by"], len(c.get("files") or [])))
print(" | ".join(res))
PY
)"
[ -n "$CMP_READ" ] || { echo "REFUSING: could not read the four compares from the GitHub compare API" >&2; exit 13; }
CMP_WANT="#940 mb=$BASE_940_941 ahead=1 files=1 | #941 mb=$BASE_940_941 ahead=1 files=2 | #942 mb=$DEVELOP_SHA ahead=2 files=3 | #887 mb=$DEVELOP_SHA ahead=5 files=2"
[ "$CMP_READ" = "$CMP_WANT" ] || { echo "REFUSING: the four compares do not read as the brief pins them: got '$CMP_READ', brief pins '$CMP_WANT'" >&2; exit 10; }
"""
s = s[:i0] + NEW_MB + s[i1:]

# 6. block replacement 4 — the develop judgement: blob-judged on the two workflow files + GUARDED prefixes
OLD_DEV_START = '# The develop pin, disjointness-checked (see the header). GUARDED = the files whose movement changes this brief.\n'
OLD_DEV_END = """    *) echo "REFUSING: origin develop is at $CUR_DEV, not the pinned $DEVELOP_SHA, and the delta is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher DEVELOP_SHA/*_BLOB_OK + brief TARGET + prompt)" >&2
       exit 18 ;;
  esac
fi
"""
assert s.count(OLD_DEV_START) == 1 and s.count(OLD_DEV_END) == 1, "develop block"
i0 = s.index(OLD_DEV_START); i1 = s.index(OLD_DEV_END) + len(OLD_DEV_END)
NEW_DEV = """# The develop pin, judged by CONTENT (see the header): the lane's three workflow files by blob on develop — a landing of #940,
# #941, #942 or #887 moves one of them to a blob this brief KNOWS (exit 19: that PR's section is moot; rewrite); an unknown blob is
# exit 18. Any other develop move is judged by the GUARDED prefixes; a disjoint move is printed and the gate re-states it.
CUR_DEV="$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)"
[ -n "$CUR_DEV" ] || { echo "REFUSING: could not read origin develop (git ls-remote)" >&2; exit 18; }
DEV_JUDGEMENT="$(
  set -a; . "$SECUURA_ENV"; set +a
  DEVELOP_SHA="$DEVELOP_SHA" CUR_DEV="$CUR_DEV" SCAN_FILE="$SCAN_FILE" GATES_FILE="$GATES_FILE" SUITES_FILE="$SUITES_FILE" \\
  SCAN_BLOB_OK="$SCAN_BLOB_OK" SCAN_BLOBS_LANDED="$SCAN_BLOBS_LANDED" GATES_BLOB_OK="$GATES_BLOB_OK" GATES_BLOB_LANDED="$GATES_BLOB_LANDED" \\
  SUITES_BLOB_OK="$SUITES_BLOB_OK" SUITES_BLOB_LANDED="$SUITES_BLOB_LANDED" python3 - <<'PYJ'
import json, os, sys, urllib.request
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura"
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
cur = os.environ["CUR_DEV"]; pinned = os.environ["DEVELOP_SHA"]
scan_f = os.environ["SCAN_FILE"]; gates_f = os.environ["GATES_FILE"]; suites_f = os.environ["SUITES_FILE"]
try:
    scan_blob = get("/contents/" + scan_f + "?ref=" + cur)["sha"]
    gates_blob = get("/contents/" + gates_f + "?ref=" + cur)["sha"]
    suites_blob = get("/contents/" + suites_f + "?ref=" + cur)["sha"]
except Exception as e:
    print("UNJUDGEABLE develop blob unreadable: " + type(e).__name__); sys.exit(0)
landed = os.environ["SCAN_BLOBS_LANDED"].split()
scan_state = "M18" if scan_blob == os.environ["SCAN_BLOB_OK"] else ("LANDED " + ["#940", "#941", "#940+#941"][landed.index(scan_blob)] if scan_blob in landed else "OTHER")
gates_state = "M18" if gates_blob == os.environ["GATES_BLOB_OK"] else ("LANDED #942" if gates_blob == os.environ["GATES_BLOB_LANDED"] else "OTHER")
suites_state = "M18" if suites_blob == os.environ["SUITES_BLOB_OK"] else ("LANDED #887" if suites_blob == os.environ["SUITES_BLOB_LANDED"] else "OTHER")
trio = "security-scan.yml blob " + scan_blob[:9] + " (" + scan_state + ") / pr-security-gates.yml blob " + gates_blob[:9] + " (" + gates_state + ") / pr-platform-suites.yml blob " + suites_blob[:9] + " (" + suites_state + ")"
if scan_state.startswith("LANDED") or gates_state.startswith("LANDED") or suites_state.startswith("LANDED"):
    print("LANDEDL9 develop's " + trio + " — a PR of this pass has landed; its section is moot"); sys.exit(0)
if scan_state == "OTHER" or gates_state == "OTHER" or suites_state == "OTHER":
    print("GUARDED develop's " + trio + " — a version nobody pinned"); sys.exit(0)
state = "develop's " + trio + " = the four heads' base copies"
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
           "systemTest/__tests__/",
           "Blockchain/Dev/docs/DEV-PROCESS.md",
           "Blockchain/Dev/package-lock.json"]
hits = sorted({x["filename"] for x in files for g in GUARDED if x["filename"] == g or (g.endswith("/") and x["filename"].startswith(g))})
if hits:
    print("GUARDED " + " ".join(hits)); sys.exit(0)
shell_suites = sum(1 for x in files if x["filename"].endswith(".test.sh"))
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d (.test.sh files %d) — disjoint from the three judged files (by blob) and the eight GUARDED paths; the gate re-reads develop at start and end, re-derives #942's and #887's merged shapes onto the then-current tip in its own clone and re-states the step-12 ratio (brief TARGET: develop's own shell-suite count, 2 develop-own reds, manifest_quarantine green)" % (pinned, cur, c["ahead_by"], len(files), shell_suites)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDEDL9*) echo "REFUSING: ${DEV_JUDGEMENT#LANDEDL9 } (develop $CUR_DEV) — rewrite the brief for the PRs still open" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, re-state the ratio, then re-pin deliberately (launcher DEVELOP_SHA/*_BLOB_OK + brief TARGET + prompt)" >&2
     exit 18 ;;
esac
"""
s = s[:i0] + NEW_DEV + s[i1:]

# 7. the exit-20 guard: all four heads in both files
OLD_20 = ('grep -qF "$HEAD_SHA" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$BRIEF" \\\n'
          '  || { echo "REFUSING: brief or prompt does not name the head SHA $HEAD_SHA — a gate about another SHA is another gate" >&2; exit 20; }\n')
assert s.count(OLD_20) == 1, "exit-20 anchor"
NEW_20 = ('for h in "$HEAD940" "$HEAD941" "$HEAD942" "$HEAD887"; do\n'
          '  grep -qF "$h" "$PROMPT_FILE" && grep -qF "$h" "$BRIEF" \\\n'
          '    || { echo "REFUSING: brief or prompt does not name the head SHA $h — a gate about another SHA is another gate" >&2; exit 20; }\n'
          'done\n')
s = s.replace(OLD_20, NEW_20)

# 8. the --check echo block
OLD_ECHO_START = '  echo "  head $HEAD_SHA present at $BRANCH on origin"\n'
OLD_ECHO_END = '  echo "  brief and prompt both name the head SHA $HEAD_SHA"\n'
assert s.count(OLD_ECHO_START) == 1 and s.count(OLD_ECHO_END) == 1, "echo block"
i0 = s.index(OLD_ECHO_START); i1 = s.index(OLD_ECHO_END) + len(OLD_ECHO_END)
NEW_ECHO = ('  echo "  heads $HEAD940 / $HEAD941 / $HEAD942 / $HEAD887 present at their branches on origin"\n'
            '  echo "  compares: $CMP_READ (GitHub compare API)"\n'
            '  echo "  live runs: $RUN_NOTE (Actions API)"\n'
            '  echo "  $DEV_NOTE"\n'
            '  echo "  brief, prompt, QA project and repo all present"\n'
            '  echo "  brief and prompt agree on TIER 2 and ROUND 1"\n'
            '  echo "  prompt opens with the thinking directive and names the brief"\n'
            '  echo "  brief and prompt both name all four head SHAs"\n')
s = s[:i0] + NEW_ECHO + s[i1:]

# 9. the override guard names the new env prefix
OLD_OV = '[ -z "${QAL9_BRIEF:-}${QAL9_PROMPT:-}${QAL9_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }\n'
assert s.count(OLD_OV) == 1, "override anchor"
s = s.replace(OLD_OV, '[ -z "${QAL9_BRIEF:-}${QAL9_PROMPT:-}${QAL9_HEAD940:-}${QAL9_HEAD941:-}${QAL9_HEAD942:-}${QAL9_HEAD887:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }\n')

# 10. residual guard
RESIDUAL = ["#983", "#982", "KS-823", "KS-790", "983.sh", "f62c975c1", "e62eab87a", "QA983", "STACK_PARENT", "MERGE_BASE", "ACTUAL_MB", "HEAD_SHA", "$BRANCH\"", "'$BRANCH'",
            "services/auth", "ks860", "api-gateway", "52/702", "s212", "TIER 1", "red-first", "oauth", "refs/pull/982", "LANDED984", "LANDED981", "the guard's five paths"]
PERMITTED = ["Adapted from the INSTALLED #983 launcher"]
body = s
for p in PERMITTED:
    assert body.count(p) == 1, f"permitted phrase count: {p!r}"
    body = body.replace(p, "")
for i, line in enumerate(body.splitlines(), 1):
    for t in RESIDUAL:
        if t in line:
            print(f"REFUSING: residual token {t!r} at line {i}: {line.strip()[:120]}", file=sys.stderr); sys.exit(2)

# 11. output controls
CONTROLS = [
    ("1aa708be9fcf7a23575398546d84848c967e81c5", 1), ("d105e07a81c8549b7f47c0542e9594204ce6f599", 1), ("53b9c3cc1a89f513620516c580a5de5bd60c64de", 1),
    ("8861e62161466c40f08d2b10a30edeb203123993", 1), ("a1e49d15152102acec7c97d96918211227c7fe1e", 1),
    ("47da5cac924cbe6c58edce8bba7593b81e13257b", 1), ("fac9ef1b89d53884d3655e3e50ea73c54c9a022a", 1), ("3b272c2d9ecbd9ab130390ca22c1ac06ac40c27d", 1), ("dc728543b91ba5a93037911a72ceca0700b2eabe", 1),
    ("571817703e76b167d2275748e6e455e35b8affb1", 1), ("eac30f09b461bd4fd270ba4da1d24423a53255c1", 1),
    ("34426409872", 2), ("34427102258", 3), ("34785721609", 2), ("34755906436", 1), ("5656613944", 1), ("5153400898", 1),
    ("QAL9_BRIEF", 2), ("QAL9_PROMPT", 2), ("QAL9_HEAD940", 2), ("QAL9_HEAD941", 2), ("QAL9_HEAD942", 2),
    ("2026-09-14_secuura-L9-940-941-942-887-ks1075-1077-1078-961-tier2.md", 2), ("2026-09-14_secuura-L9-940-941-942-887-ks1075-1077-1078-961-tier2.prompt.txt", 1),
    ("3aee3deed2e3ac557f0a52c0797c2a4a8df25f69", 1), ("a509ad7934a50cd3f96c7241d9445b942c638cb7", 1), ("fd5e8343c6392ec35b2abc5c38d305a945896b71", 1), ("34786655660", 2), ("QAL9_HEAD887", 2),
    ("refs/heads/feature/ks-961-workspace-suites-advisory-on-pr", 1), ("SUITES_FILE", 4), ("SUITES_BLOB_OK", 4), ("SUITES_BLOB_LANDED", 4), ("KS-961", 1), ("Blockchain/Dev/docs/DEV-PROCESS.md", 2), ("Blockchain/Dev/package-lock.json", 2), ("rollup-linux-x64-gnu", 1),
    ("refs/heads/feature/ks-1075-ci-gate-diagnostics", 1), ("refs/heads/feature/ks-1077-single-audit-allowlist", 1), ("refs/heads/feature/ks-1078-tsx-probe-capture", 1),
    ("exit 22", 3), ("exit 21", 3), ("exit 20", 1), ("exit 19", 5), ("exit 18", 7), ("exit 10", 2), ("exit 6", 2), ("exit 13", 1), ("exit 16", 2), ("exit 7", 1), ("exit 15", 1), ("exit 9", 1), ("exit 8", 1), ("exit 12", 1), ("exit 11", 1), ("exit 14", 1), ("exit 17", 1), ("exit 2;", 1), ("exit 3;", 1), ("exit 4;", 1), ("exit 5;", 1),
    ("'TIER 2'", 2), ("'ROUND 1'", 2), ("LANDEDL9", 3), ("[ -t 0 ]", 1), ("GUARDED", 7),
    ("SCAN_FILE", 4), ("GATES_FILE", 4), ("SCAN_BLOB_OK", 4), ("SCAN_BLOBS_LANDED", 4), ("GATES_BLOB_OK", 4), ("GATES_BLOB_LANDED", 4),
    ("MAIL YOUR VERDICT", 1), ("no memory maintenance", 1), ("NEVER print a credential value", 1), ("ultrathink", 1),
    ("exec claude --dangerously-skip-permissions --model opus", 1), ('cd "$QA_DIR"', 1),
    ("brief and prompt both name all four head SHAs", 1), ("brief and prompt agree on TIER 2 and ROUND 1", 1),
    ("KS-1075", 1), ("KS-1077", 1), ("KS-1078", 1), ("KS-1148", 1), ("kam-merges", 1), ("stdin is not a TTY", 2), ("RUN_NOTE", 2), ("CMP_WANT", 3), ("CMP_READ", 5), ("ahead=5 files=2", 1),
    ('g.endswith("/") and x["filename"].startswith(g)', 1), ("head_sha", 4), ("HEAD887", 11), ("actions/runs/", 1), ("never dispatched, never re-run", 1),
]
bad = [(tok, s.count(tok), n) for tok, n in CONTROLS if s.count(tok) != n]
if bad:
    for tok, c, n in bad:
        print(f"REFUSING: output control {tok!r} occurs {c} times, expected {n}", file=sys.stderr)
    sys.exit(3)
b = s.encode("utf-8")
assert not [i for i, x in enumerate(b) if (x < 0x20 and x not in (9, 10, 13)) or x == 0x7f], "raw control byte in output"
open(out_path, "w", encoding="utf-8").write(s)
os.chmod(out_path, 0o755)
print(f"written {out_path} ({len(b)} bytes); {len(subs)} substitutions asserted; 4 block replacements + the exit-20 loop + the echo block + the override line (four heads); residual guard clean ({len(RESIDUAL)} tokens); {len(CONTROLS)} output controls")
