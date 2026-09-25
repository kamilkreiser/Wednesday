#!/bin/bash
# launch_qa_nexusai_gate_batch2.sh — cross-project QA agent, ONE batched gate on Datasec/NexusAI ("batch #2"), THREE targets,
# THREE verdicts, ONE report (2026-09-26):
#   A — RD-428 (TIER 1): rd-428-provisioning-residue-s84p @ 823ef9e = 2c62792 (change, off 7c47ec4) + counts. 9 files.
#       F2 keeps a shown-once SCIM token in page memory across a mode change (credential handling); F3 nav inner focus ring;
#       F4 fallback message names DATA_DIR. Counts 3978/235 -> 3990/238.
#   B — RD-444 (TIER 2): rd-444-gitignore-symlink-s84p @ 2f9da1c = 26a7a23 (off 7c47ec4) + counts. .gitignore + 1 test. 3982/236.
#   C — RD-200 (TIER 2): rd-200-js-colour-corpus-s84p @ 12b5edc = 4f97260 (off 7c47ec4) + c01190d (forward merge of main
#       11666d3) + counts. JS colour corpus gate + closed debt manifest. 4012/237 -> 4021/238.
#   Main 11666d3 = 7c47ec4 + RD-579 + RD-639 (two merges). All deltas pairwise FILE-DISJOINT except the counts file; the gate
#   verifies each head and the merged tree 11666d3 + 823ef9e + 2f9da1c + 12b5edc in its OWN scratch clone, counts regenerated
#   once (predicted 4037/242).
#
# AUTHORITY: three READY mails from NexusAI-P (S84P), copies in briefs/. Tuesday's commission (batched, RD-428 raised to tier 1).
# Merges: Tuesday's GO (Kam 2026-09-25 ~22:0x "merge once tested").
#
# PATTERN: launch_qa_nexusai_gate_rd579_rd639.sh (guard families 9 6 7 8 18 22 23 35 70 75 31 39 10 17 11 12-15 20 19 24 53 71 38
# 32 40), prompt EMBEDDED. CHANGES, each deliberate:
#   - three heads + main pinned; ls-remote re-check of all three branches (18). main moving past 11666d3 is a NOTE, not a refusal:
#     the merged-tree premise names 11666d3 and the gate reports what moved (C-68).
#   - 7/8: RD-428 and RD-444 are off 7c47ec4 (NOT main); RD-200 CONTAINS main (forward merge c01190d); main's own line pinned.
#   - 23: FILE-DISJOINTNESS over four deltas (A, B, C over main, M = 7c47ec4..main), all six pairs share the counts file only.
#   - 75: the three tips are counts-only commits (the builders' verifies ran on the parent trees); c01190d added only RD-200's files.
#   - 76 (NEW, from the last gate's S-1): the brief carries the ONE safe SESSION_SECRET printer and forbids the unsafe idioms;
#     the launcher itself unsets SESSION_SECRET before exec and prints SET/UNSET by NAME only.
#   - 77 (NEW, from S-4): the brief carries the heartbeat-as-separate-child rule (H-4).
#   - 40: the routing line QA/NexusAI-batch2 exists (checked AFTER the stamp so --check refuses on the stamp only).
#   - 32: SELF-CHECK stamp, placeholder @STAMP@ (comparand built by concatenation). LAST refusal before --check exits.
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/NexusAI-batch2' "bash '<this file>'"), NEVER nohup.
# Identity: exports NexusAI's OWN az/gh dirs (az unused, gh optional and READ-ONLY); CLAUDE_CONFIG_DIR pinned to Tuesday's store.
# --check is READ-ONLY: git read verbs (cat-file, log, merge-base, diff, show, rev-parse, ls-remote, ls-tree), grep, ps, tmux.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate_batch2.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..77 a guard refused
set -u
CHECK=0
for a in "$@"; do
  case "$a" in
    --check) CHECK=1 ;;
    *) echo "unknown argument: $a" >&2; exit 2 ;;
  esac
done

PH_STAMP='@STA''MP@'

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-26_nexusai-gate-batch2-rd428-rd444-rd200.md"
READY_A="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-25_nexusai-rd428-READY-mail.txt"
READY_B="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-25_nexusai-rd444-READY-mail.txt"
READY_C="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-26_nexusai-rd200-READY-mail.txt"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
NX='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI'
REPO="$NX/2_Project_Files"
EVID_P="$NX/session-tools/s84p"
CLAR="$NX/1_Project_Definition/CLARIFICATIONS.md"
PRIOR_A="$NX/qa-reports/2026-09-14-rd409-410-5507f2b-tier1-report.md"
PREV_GATE="$QA_DIR/projects/nexusai/reports/2026-09-25-gate-rd579-rd639/report.md"
PREV_FLOORLIB="$QA_DIR/projects/nexusai/reports/2026-09-25-gate-rd579-rd639/evidence/qa-floorlib.sh"
PREV_FLOOR="$QA_DIR/projects/nexusai/reports/2026-09-25-gate-rd579-rd639/evidence/qa-floorcount.py"
PREV_DISPATCH="$QA_DIR/projects/nexusai/reports/2026-09-25-gate-rd579-rd639/evidence/qa-dispatch.sh"
G7R1_FLOOR="$QA_DIR/projects/nexusai/reports/2026-09-22-gate7-rd645/evidence/qa-floorcount.py"
REPORT="$QA_DIR/projects/nexusai/reports/2026-09-26-gate-batch2-rd428-rd444-rd200/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"
ROUTE_NAME='QA/NexusAI-batch2'

BASE_SHA='7c47ec467f585e9db5daf3a82cdb96deae0b1e7a'     # RD-428's and RD-444's base; RD-200's build base
MAIN_SHA='11666d3c4f615190646914270016419fffa642e2'     # origin main at drafting = 7c47ec4 + RD-579 + RD-639 (merge 2)
MAIN_M1='0863711261afc5f3323b8c4fc480d65109b17ba7'      # merge 1 (RD-579)
RD579='cac9cf641c86ff89a48aa42d7447cdcfbbeaa6c1'
RD639='fe53540fbaf628fa3ca5eb790d023ecf5ae71f0c'
A_BRANCH='rd-428-provisioning-residue-s84p'
A_BUILD='2c6279205e7855840dd24262e5c5e956c099e9e6'
A_HEAD="${QA_A_HEAD_OVERRIDE:-823ef9e5e117d1c3f7d8c8659fe31e1a4fc61a1e}"
B_BRANCH='rd-444-gitignore-symlink-s84p'
B_BUILD='26a7a230ac0c700e0ebd9dc63ce9a7e8e48aa172'
B_HEAD="${QA_B_HEAD_OVERRIDE:-2f9da1cda0f2971957434b439b0a32792c54dce3}"
C_BRANCH='rd-200-js-colour-corpus-s84p'
C_BUILD='4f97260c5c4682913cd785ff8569ce1bc490fe70'
C_FWD='c01190d0dcc416554074e751a86eca45398cede3'
C_HEAD="${QA_C_HEAD_OVERRIDE:-12b5edc31ee4ef52415d1cbffbbb0504d7f4715c}"

COUNTS_FILE='scripts/verify-expected-counts.json'
A_EXPECTED_FILES='__tests__/rd409-410-provisioning-panel-keyboard-and-recovery.test.js
__tests__/rd428-fallback-names-data-dir.test.js
__tests__/rd428-nav-inner-focus-ring.test.js
__tests__/rd428-scim-token-mode-change.test.js
backend/routes/entraProvisioning.js
scripts/verify-expected-counts.json
static/css/dark-mode.css
static/css/keyboard-focus.css
static/js/entra-provisioning-ui.js'
B_EXPECTED_FILES='.gitignore
__tests__/rd444-gitignore-node-modules-symlink.test.js
scripts/verify-expected-counts.json'
C_EXPECTED_FILES='__tests__/fixtures/rd200-js-brand-debt.json
__tests__/helpers/css-colors.js
__tests__/rd200-js-colour-corpus.test.js
docs/BRAND.md
scripts/verify-expected-counts.json'
C_FWD_FILES='__tests__/fixtures/rd200-js-brand-debt.json
__tests__/helpers/css-colors.js
__tests__/rd200-js-colour-corpus.test.js
docs/BRAND.md'

LOCK_BLOB='906476350431e2ecb3c21070a25c64b1702c1aa8'
NEG_SEATS='88756 10246 10643 11987 91386'   # NexusAI-M %11, -N %12, -O %13, -P %14, Tuesday %0 — read 2026-09-26 04:23 AEST

SUBJECT_STEM='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-428: '
QUESTION_SUBJ='[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>'
ANSWER_PREFIX='[Tuesday -> QA/NexusAI-batch2] ANSWER'
NOTTESTED_LINE="Not tested by this gate: Firefox or Safari, a screen reader's announcement of the new status text, Linux or CI at any branch head unless a PR's CI Build exists, git versions other than this Mac's, Windows symlinks or junctions, and whether each of RD-200's 147 recorded literals is visible on a rendered page."
SAFE_PRINTER='if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET (length ${#SESSION_SECRET})"; else echo "SESSION_SECRET UNSET"; fi'

g() { git --no-optional-locks -C "$REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }
counts_at() { g show "${1}:$COUNTS_FILE" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
blob() { g rev-parse "${1}:${2}" 2>/dev/null; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE batched gate on Datasec/NexusAI with THREE targets, THREE verdicts and ONE report: RD-428 (TIER 1), RD-444 (TIER 2) and RD-200 (TIER 2). Each ticket gets its own verdict — GO, GO WITH FINDINGS or NO GO — about its branch head AND about the merged tree. A finding on one ticket never becomes another's verdict.

READ YOUR COMMISSION FIRST, whole: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-26_nexusai-gate-batch2-rd428-rd444-rd200.md
Then the charter it names, then all three READY mails it names, then the RD-409/410 gate report it names (findings 2-4 are RD-428's origin), then the previous batched gate's report (2026-09-25-gate-rd579-rd639) — its method and its self-corrections S-1 to S-6, which the brief's section 3a turns into rules H-1 to H-6 that bind you. Every builder statement is a CLAIM, never evidence. The brief's LEGITIMATE SHAPES tables (section 2a) are required measurements, row by row, base and head in the same window.

THE TARGETS. Main is 11666d3c4f615190646914270016419fffa642e2 (7c47ec467f585e9db5daf3a82cdb96deae0b1e7a plus RD-579 and RD-639, merged). RD-428: branch rd-428-provisioning-residue-s84p at 823ef9e5e117d1c3f7d8c8659fe31e1a4fc61a1e = 2c6279205e7855840dd24262e5c5e956c099e9e6 (the change, off 7c47ec4 — main is NOT its base) plus a counts-only commit; nine files. RD-444: branch rd-444-gitignore-symlink-s84p at 2f9da1cda0f2971957434b439b0a32792c54dce3 = 26a7a230ac0c700e0ebd9dc63ce9a7e8e48aa172 (off 7c47ec4) plus counts; .gitignore and one test. RD-200: branch rd-200-js-colour-corpus-s84p at 12b5edc31ee4ef52415d1cbffbbb0504d7f4715c = 4f97260c5c4682913cd785ff8569ce1bc490fe70 (off 7c47ec4), forward-merged onto main at c01190d0dcc416554074e751a86eca45398cede3, plus counts; test-side and docs only. All deltas, and main's own line, are FILE-DISJOINT except scripts/verify-expected-counts.json — prove it.

RD-428 (TIER 1) — THE SHOWN-ONCE SCIM TOKEN. F2 now keeps a just-generated SCIM bearer token in page memory across a real mode change until Save, Revoke or Reload. POSITIVE CONTROL FIRST: the head's cells red at 7c47ec4 (the READY's 9) and 50/50 at the head, same window; read why the round-trip CONTROL is red at base; prove the re-anchored rd409-410 cell is the ONLY change in that file and say whether the old cell's intent survives (C-97). The builder ran NO mutant table: run M-A1 to M-A9. REAL-BROWSER LEG (the builder drove F3 only; F2 has never seen a real browser): Chrome via Playwright on your own loopback server, open mode, keyboard Tab and arrow keys, never synthetic focus. (a) Settings nav focus ring, light AND dark, the item below the active one and another, hover over a focused item, a second viewport, the base's 1.00 and 1.64 reproduced. (b) Settings, Provisioning: SCIM, Generate, ArrowLeft/ArrowRight on the focused card, Save under Graph and separately under SCIM — every row of the brief's table 2a-A, capturing every request (URL, headers, body), the console, localStorage, sessionStorage, IndexedDB, Cache Storage and cookies, the status line and the DOM, with a POSITIVE CONTROL that finds the token in the scim-token response and the scim save body first. THE F2 SAFETY LEG: re-read at source that the token is drawn only in scimPanel, sent only when mode is scim, and cleared on reload, revoke, accepted save and conflict (the brief's table has the head's line numbers; the READY quotes the base's); then prove it never reaches a non-scim request, browser storage, logs, the audit row or the settings file under a non-scim save. Measure the two paths the READY does not list (a non-version save failure and a thrown fetch keep the token) and bfcache (navigate away and Back). HTTP level: a hand-built graph save carrying a token stores nothing and logs nothing. BRAND LEG: #00719f is --nx-brand-chrome and #0096d6 is --nx-brand-blue in the tokens stylesheet — confirm every colour the change introduces resolves to a token in its own theme block, with a planted off-token value as the control; say why the conformance test's occurrence counts stayed green after one more of each; record, do not rule, the "a GROUND, never text" nuance. F4 on a store that REALLY fell back, both branches. The C-68 re-run set (44 files by the brief's scoped grep). Prior-work check against S59's WIP.

RD-444 (TIER 2) — THE IGNORE RULE. Real git in a scratch repo, system, global and excludesFile config neutralised, at both shas, git --version recorded: every row of table 2a-B — symlinked node_modules top level and deep, dangling, to a file, a regular FILE named node_modules, and the near-miss names node_modules.bak, my_node_modules and node_modules_x which must NOT be ignored. POSITIVE CONTROL FIRST: SYMLINK, NESTED and ONE LINE red at 7c47ec4, CONTROL green, 4/4 at the head; prove the findability line bites. Mutants M-B1 to M-B4. Run the gitignore readers the brief lists and read the three scripts. For RD-444's own arms use a REAL node_modules directory clone, never a symlink, so your instrument is not the thing under test.

RD-200 (TIER 2) — A GATE THAT CLAIMS TO SEE JAVASCRIPT (C-40). POSITIVE CONTROL FIRST: manifest emptied red naming all 66, the real manifest 9/9, then T1 (with a value other than the canary), T2 and T3 re-derived. INDEPENDENT CENSUS with your own extractor over every first-party static/js file (27): files, literals (the READY says 223), off-token (147 in 66 entries) — every difference by file:line. The duplicated resolver: feed extractJs and the conformance test's own RGB_TRIPLE/toHex the same inputs and diff. Every row of table 2a-C, especially hsl() and hex-valid ID selectors. Mutants M-C1 to M-C4 on the gate itself. The shared helper's four consumers, named. The manifest's joint RD-676/RD-677 ownership stated; Jira not read (RELAYED).

THE MERGED TREE — part of every verdict. In YOUR OWN scratch clone (git clone --shared --no-checkout into your own project dir; origin removed; local user config; gc.auto 0; merges and commits in the clone ONLY): 11666d3, merge --no-ff 823ef9e, merge --no-ff 2f9da1c, merge --no-ff 12b5edc. Predict before each merge whether it conflicts, and explain any clean merge with a control; anything other than the counts file conflicting STOPS (C-57). C-104: resolve and stage before any census or run. Resolve the counts by REGENERATION, never by hand: npm run verify -- --maxWorkers=2 --update-counts ONCE on the tree after ALL THREE merges. Predicted 4037/242 — a prediction; the measurement decides. Build a second order and prove the two trees identical apart from the counts file. Blob identities per the brief. id-superset control with a COPY of session-tools/c57-id-superset.sh (missing 0 predicted; C-133 only if it misses) and C-112's condition stated beside the conclusion. On the merged tree, one hold: rd200 9/9 (RD-428 edits a file in its corpus), the rd428, rd409-410 and rd444 files, the conformance test, all three C-68 sets, the full verify, then one mutant per ticket. C-89 on your clone. Count the repo's object files before and after and account for any delta by mtime. Nothing leaves your clone.

FULL VERIFY of each head and of the merged tree through the lock, SESSION_SECRET UNSET. Predicted 823ef9e 3990/238, 2f9da1c 3982/236, 12b5edc 4021/238, merged 4037/242. Every failure by NAME; re-run-until-green is not an acceptance gate. A RED ARM COUNTS ONLY IF THE MUTANT STILL PARSES AND LANDED: node --check every mutated JS file and quote the exit code, assert each anchor matched once and the marker is present; a red from a mutant that does not parse, or a green from one that never landed, is a VOID arm.

THE INSTRUMENT RULES H-1 TO H-6 (brief section 3a) — the last gate broke each of these once. H-1: the ONLY SESSION_SECRET printer is the one the brief quotes (it prints SET with a length, or UNSET — never a value); self-test it with a throwaway before the first hold and scan every hold's logs for the throwaway afterwards; print a SCIM token only masked, compare in-process, and mask it in every screenshot. H-2: never construct a product storage object on a DATA_DIR you are measuring. H-3: a LANDING CONTROL for every hook, preload, signal handler, route interceptor or mutant before the measured run; a failed instrument makes a VOID arm, re-run and reported as a self-correction. H-4: the HEARTBEAT is a separate child process of the hold wrapper, aborted if absent 90 s after the grant, and you report the max gap per hold (at most 120 s). H-5: restore your own perturbations before any hash. H-6: every extractor gets a positive control; quote every path (the QA path has spaces and a bang); the browser ABORTS every non-loopback request.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT (git archive into a fresh mktemp dir under projects/nexusai/qa-trees/batch2.*). Each tree is EXCLUSIVE to this gate and to one purpose. In the NexusAI repo use ONLY read verbs (show, log, diff, ls-tree, cat-file, rev-parse, merge-base, grep, ls-remote, archive); never fetch, pull, push, checkout, worktree, commit, stash, gc, clean or merge-tree --write-tree there, and never work in its 2_Project_Files checkout or any builder worktree (C-28). Symlinks, chmod and scratch git repos ONLY under your own mktemp dirs. Findings-only: no commits outside your clone, no tickets, no edits in NexusAI, never merge anything anywhere the fleet can see (merges are Tuesday's GO). No Azure (no az at all), no demo, no public host, no Entra, no real SCIM client: every token is minted by your own local server. No mail to any human. Never rm: quarantine.

FLOOR DISCIPLINE — section 9 of the brief exactly. QUEUE, NEVER TAKE OVER: four NexusAI seats (M, N, O, P) share session-tools/nexusai-lock.sh with you. Every jest run, browser run and server boot goes through it with a tag starting qa-b2- (C-141 gate-class, and its ADDENDUM 2: each new qa ticket earns a fresh yield; C-110), the lock held once per multi-run measurement as a tracked child of your seat. Count foreign servers the C-125 way anchored on YOUR OWN claude pid, with the brief's five negative-control seats classifying foreign in the same run; a hold with no live negative control aborts; count your own headless browsers too. A zero is reportable only beside a control that fired in the same window. DEADLINE AND HEARTBEAT: every probe, page load, key press and request has a per-step DEADLINE and a client timeout, every server and browser is killed in a finally, a HEARTBEAT line at least every 2 minutes during a hold, and a step with no heartbeat for 5 minutes is aborted and reported.

CI: whether any of the three branches has a PR, and main 11666d3's CI Build, are UNVERIFIED by the drafter — read them with gh READ ONLY or say you could not. CI NOT RUN at a head with no PR.

RE-PIN at start, mid and end: all three branches and main — three timestamped readings with the branch name beside each sha. A head that disagrees with the brief is a FINDING and a reason to stop, never a typo to fix. The same builder seat is working other tickets now: if a branch moves, your verdict still names the pinned sha and you say so.

QUESTIONS: your routing name is QA/NexusAI-batch2. If you must ask, mail tuesday-agent@agentmail.to with subject "[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>" and PROCEED ON THE SAFEST READING without waiting; Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/NexusAI-batch2] ANSWER". Approval-class items are NOT RUN and named, never done on a safe reading. If no real browser launches, RD-428's browser leg is NOT RUN, RD-428 cannot be GO, and you ask. Record every question, reading and answer in the report.

Write your ONE report to: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-26-gate-batch2-rd428-rd444-rd200/report.md

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with the subject exactly:
[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-428: <GO|GO WITH FINDINGS|NO GO> @ 823ef9e · RD-444: <GO|GO WITH FINDINGS|NO GO> @ 2f9da1c · RD-200: <GO|GO WITH FINDINGS|NO GO> @ 12b5edc
Lead the body with one sentence per ticket. Never wednesday-agent@. You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no 4_Credentials directory of its own. Never put the key, a SCIM token or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice.

Rule 2 stands: what you did NOT test is first-class output — a NOT TESTED section, every declared limit L-A1 to L-A5, L-B1 to L-B3 and L-C1 to L-C4 discharged with a measurement or left standing and named (C-112), and every action recommendation labelled MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. That section must carry this line verbatim:
Not tested by this gate: Firefox or Safari, a screen reader's announcement of the new status text, Linux or CI at any branch head unless a PR's CI Build exists, git versions other than this Mac's, Windows symlinks or junctions, and whether each of RD-200's 147 recorded literals is visible on a rendered page.
PROMPT_EOF

# ---------------------------------------------------------------- GUARDS
[ -d "$QA_DIR" ]  || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]   || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -n "$PROMPT" ]  || { echo "embedded prompt is empty" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }
for S in "$A_HEAD" "$B_HEAD" "$C_HEAD"; do
  [[ "$S" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: head '$S' is not a full 40-hex sha" >&2; exit 9; }
done

# 6 — every pinned sha is a commit in the object store (this launcher never fetches).
for S in "$BASE_SHA" "$MAIN_SHA" "$MAIN_M1" "$RD579" "$RD639" "$A_BUILD" "$A_HEAD" "$B_BUILD" "$B_HEAD" "$C_BUILD" "$C_FWD" "$C_HEAD"; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 7 — bases: RD-428 and RD-444 off 7c47ec4 (NOT main); RD-200 contains main; 7c47ec4 is an ancestor of main.
g merge-base --is-ancestor "$BASE_SHA" "$MAIN_SHA" 2>/dev/null || { echo "REFUSING: 7c47ec4 is not an ancestor of main" >&2; exit 7; }
[ "$(g merge-base "$MAIN_SHA" "$A_HEAD" 2>/dev/null)" = "$BASE_SHA" ] || { echo "REFUSING: merge-base(main, RD-428) is not 7c47ec4" >&2; exit 7; }
[ "$(g merge-base "$MAIN_SHA" "$B_HEAD" 2>/dev/null)" = "$BASE_SHA" ] || { echo "REFUSING: merge-base(main, RD-444) is not 7c47ec4" >&2; exit 7; }
[ "$(g merge-base "$MAIN_SHA" "$C_HEAD" 2>/dev/null)" = "$MAIN_SHA" ] || { echo "REFUSING: RD-200 does not contain main 11666d3" >&2; exit 7; }

# 8 — chains exact, parents exact.
[ "$(g log --format='%H %P' "${BASE_SHA}..${A_HEAD}" 2>&1)" = "$A_HEAD $A_BUILD
$A_BUILD $BASE_SHA" ] || { echo "REFUSING: 7c47ec4..RD-428 is not exactly 2c62792 then 823ef9e" >&2; exit 8; }
[ "$(g log --format='%H %P' "${BASE_SHA}..${B_HEAD}" 2>&1)" = "$B_HEAD $B_BUILD
$B_BUILD $BASE_SHA" ] || { echo "REFUSING: 7c47ec4..RD-444 is not exactly 26a7a23 then 2f9da1c" >&2; exit 8; }
[ "$(g log --format='%H %P' "${MAIN_SHA}..${C_HEAD}" 2>&1)" = "$C_HEAD $C_FWD
$C_FWD $C_BUILD $MAIN_SHA
$C_BUILD $BASE_SHA" ] || { echo "REFUSING: main..RD-200 is not exactly 4f97260, c01190d (merge of main), 12b5edc" >&2; exit 8; }
[ "$(g log --format='%H %P' "${BASE_SHA}..${MAIN_SHA}" 2>&1)" = "$MAIN_SHA $RD639 $MAIN_M1
$MAIN_M1 $RD579 $BASE_SHA
$RD639 $BASE_SHA
$RD579 0677388ab031ffaf569a52f6c0301af48f44aece" ] || { echo "REFUSING: 7c47ec4..main is not RD-579, RD-639 and their two merges — main's line moved; re-brief" >&2; exit 8; }

# 18 — RE-PIN NOW by ls-remote: the three branches exactly the pinned heads. main moving is a NOTE (the gate reports it; C-68).
for PAIR in "$A_BRANCH $A_HEAD" "$B_BRANCH $B_HEAD" "$C_BRANCH $C_HEAD"; do
  BR="${PAIR%% *}"; H="${PAIR#* }"
  L="$(g ls-remote origin "refs/heads/$BR" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: origin refs/heads/$BR is not $H — moved or never pushed; re-brief. ls-remote said:" >&2; printf '%s\n' "${L:-<nothing>}" >&2; exit 18; }
done
M_ORIGIN="$(g ls-remote origin refs/heads/main 2>/dev/null | awk '{print $1}')"
[ "$M_ORIGIN" = "$MAIN_SHA" ] || echo "NOTE: origin main is now ${M_ORIGIN:-unreadable}, not 11666d3 — the brief's merged tree names 11666d3; tell the gate what moved (it re-pins anyway)" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — each delta is EXACTLY the commissioned file set; the tips are counts-only; the forward merge added only RD-200's files.
GOT="$(g diff --name-only "$BASE_SHA" "$A_HEAD" 2>/dev/null | sort)"
[ "$GOT" = "$(sorted "$A_EXPECTED_FILES")" ] || { echo "REFUSING: RD-428's delta over 7c47ec4 is not the nine files. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }
GOT="$(g diff --name-only "$BASE_SHA" "$B_HEAD" 2>/dev/null | sort)"
[ "$GOT" = "$(sorted "$B_EXPECTED_FILES")" ] || { echo "REFUSING: RD-444's delta over 7c47ec4 is not the three files. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }
GOT="$(g diff --name-only "$MAIN_SHA" "$C_HEAD" 2>/dev/null | sort)"
[ "$GOT" = "$(sorted "$C_EXPECTED_FILES")" ] || { echo "REFUSING: RD-200's delta over main is not the five files. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }

# 75 — the three tips are counts-only commits; c01190d added nothing but RD-200's own files over main.
for PAIR in "$A_BUILD $A_HEAD" "$B_BUILD $B_HEAD" "$C_FWD $C_HEAD"; do
  P="${PAIR%% *}"; H="${PAIR#* }"
  [ "$(g diff --name-only "$P" "$H" 2>/dev/null)" = "$COUNTS_FILE" ] || { echo "REFUSING: ${P:0:7}..${H:0:7} is not a counts-only commit — the builder's verify did not run on the head's tree" >&2; exit 75; }
done
GOT="$(g diff --name-only "$MAIN_SHA" "$C_FWD" 2>/dev/null | sort)"
[ "$GOT" = "$(sorted "$C_FWD_FILES")" ] || { echo "REFUSING: the forward merge c01190d differs from main by more than RD-200's four files. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 75; }

# 23 — FILE-DISJOINTNESS: the four deltas pairwise share the counts file only.
DA="$(g diff --name-only "$BASE_SHA" "$A_HEAD" 2>/dev/null | sort)"
DB="$(g diff --name-only "$BASE_SHA" "$B_HEAD" 2>/dev/null | sort)"
DC="$(g diff --name-only "$MAIN_SHA" "$C_HEAD" 2>/dev/null | sort)"
DM="$(g diff --name-only "$BASE_SHA" "$MAIN_SHA" 2>/dev/null | sort)"
for PAIR in A_B A_C A_M B_C B_M C_M; do
  X="${PAIR%%_*}"; Y="${PAIR#*_}"; eval "SX=\"\$D$X\""; eval "SY=\"\$D$Y\""
  COMMON="$(comm -12 <(printf '%s\n' "$SX") <(printf '%s\n' "$SY"))"
  [ "$COMMON" = "$COUNTS_FILE" ] || { echo "REFUSING: deltas $X and $Y share more (or other) than the counts file: ${COMMON:-<nothing>}" >&2; exit 23; }
done

# 35 — counts at every pinned sha.
for PAIR in "$BASE_SHA 3978 235" "$MAIN_SHA 4012 237" "$A_BUILD 3978 235" "$A_HEAD 3990 238" "$B_BUILD 3978 235" "$B_HEAD 3982 236" \
            "$C_BUILD 3978 235" "$C_FWD 4012 237" "$C_HEAD 4021 238"; do
  S="${PAIR%% *}"; WANT="${PAIR#* }"
  CT="$(counts_at "$S")"
  [ "$CT" = "$WANT" ] || { echo "REFUSING: $COUNTS_FILE at ${S:0:7} reads '${CT:-unreadable}', not '$WANT'" >&2; exit 35; }
done

# 70 — package-lock identical everywhere (one node_modules serves every tree).
for S in "$BASE_SHA" "$MAIN_SHA" "$A_HEAD" "$B_HEAD" "$C_HEAD"; do
  [ "$(blob "$S" package-lock.json)" = "$LOCK_BLOB" ] || { echo "REFUSING: package-lock at ${S:0:7} is not ${LOCK_BLOB:0:7}" >&2; exit 70; }
done

# 31 — builder evidence, prior findings, standing references and tools on disk.
for f in "$READY_A" "$READY_B" "$READY_C" "$CLAR" "$PRIOR_A" "$PREV_GATE" \
         "$EVID_P/rd428-redgreen.log" "$EVID_P/rd428-red-at-7c47ec4.log" "$EVID_P/rd428-verify.log" "$EVID_P/rd428-f3-browser.js" \
         "$EVID_P/rd444-redgreen.log" "$EVID_P/rd444-verify.log" \
         "$EVID_P/rd200-proof.log" "$EVID_P/rd200-verify.log" "$EVID_P/rd200-census-7c47ec4.txt" \
         "$NX/session-tools/nexusai-lock.sh" "$NX/session-tools/c57-id-superset.sh" \
         "$PREV_FLOORLIB" "$PREV_FLOOR" "$PREV_DISPATCH" "$G7R1_FLOOR" \
         "$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"; do
  [ -s "$f" ] || { echo "REFUSING: evidence or tool absent: $f" >&2; exit 31; }
done
[ -d "$EVID_P/rd428-evidence" ] || { echo "REFUSING: $EVID_P/rd428-evidence (the builder's F3 screenshots) is absent" >&2; exit 31; }
grep -qF "${A_HEAD:0:7}" "$READY_A" || { echo "REFUSING: the RD-428 READY does not name ${A_HEAD:0:7}" >&2; exit 31; }
grep -qF "${B_HEAD:0:7}" "$READY_B" || { echo "REFUSING: the RD-444 READY does not name ${B_HEAD:0:7}" >&2; exit 31; }
grep -qF "${C_HEAD:0:7}" "$READY_C" || { echo "REFUSING: the RD-200 READY does not name ${C_HEAD:0:7}" >&2; exit 31; }

# 39 — the floor instruments are named in the brief.
for f in "$PREV_FLOORLIB" "$G7R1_FLOOR"; do
  grep -qF "$f" "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument $f" >&2; exit 39; }
done

# 10 / 17 — report path named in both; no stale report; brief names every source it cites.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }
for P in "$PRIOR_A" "$PREV_GATE" "$READY_A" "$READY_B" "$READY_C"; do
  grep -qF "$P" "$BRIEF" || grep -qF "${P#$QA_DIR/}" "$BRIEF" || { echo "REFUSING: brief must name $P" >&2; exit 10; }
done

# 11 — identity: NexusAI's OWN dirs.
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

# 12 / 13 / 14 / 15 / 20 — tiers, directive, brief path, pins, verdict route, key path, question route.
for T in 'RD-428 is TIER 1' 'RD-444 is TIER 2' 'RD-200 is TIER 2' 'One verdict PER ticket'; do
  grep -qF "$T" "$BRIEF" || { echo "REFUSING: brief does not declare '$T'" >&2; exit 12; }
done
for T in 'RD-428 (TIER 1)' 'RD-444 (TIER 2)' 'RD-200 (TIER 2)' 'THREE verdicts'; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare '$T'" >&2; exit 12 ;; esac
done
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
for S in "$A_HEAD" "$B_HEAD" "$C_HEAD" "$MAIN_SHA" "$BASE_SHA" "$A_BUILD" "$B_BUILD" "$C_BUILD" "$C_FWD"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S" >&2; exit 14; }
  case "$PROMPT" in *"$S"*) ;; *) echo "REFUSING: prompt must name $S" >&2; exit 14 ;; esac
done
if printf '%s\n' "$PROMPT" | LC_ALL=C grep -q '@[A-Z_]*@'; then echo "REFUSING: the prompt carries a placeholder" >&2; exit 14; fi
case "$PROMPT" in *"MAIL YOUR VERDICT"*"tuesday-agent@agentmail.to"*) ;; *) echo "REFUSING: prompt must say MAIL YOUR VERDICT to tuesday-agent@agentmail.to" >&2; exit 15 ;; esac
grep -qF "$SUBJECT_STEM" "$BRIEF" || { echo "REFUSING: brief must carry the verdict subject stem" >&2; exit 15; }
for FL in brief prompt; do
  if [ "$FL" = brief ]; then SRC="$(cat "$BRIEF")"; else SRC="$PROMPT"; fi
  case "$SRC" in *"$SUBJECT_STEM"*"@ 823ef9e · RD-444: "*"@ 2f9da1c · RD-200: "*"@ 12b5edc"*) ;; *) echo "REFUSING: $FL must carry the three-verdict subject" >&2; exit 15 ;; esac
done
case "$PROMPT" in *"/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env"*) ;; *) echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20 ;; esac
for T in "$QUESTION_SUBJ" "$ANSWER_PREFIX" "$ROUTE_NAME"; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the question route: $T" >&2; exit 20; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the question route: $T" >&2; exit 20 ;; esac
done
if printf '%s\n' "$PROMPT" | grep -qi 'wednesday-agent@' && ! printf '%s\n' "$PROMPT" | grep -q 'Never wednesday-agent@'; then
  echo "REFUSING: the prompt routes to wednesday-agent@ — Datasec's coordinator is Tuesday" >&2; exit 15; fi

# 19 — the words the prompt must carry (% is a space); and the brief's sections.
WORDS="RD-428 RD-444 RD-200 RD-409/410 S-1 S-6 H-1 H-6 scimPanel bfcache thrown%fetch localStorage sessionStorage IndexedDB
POSITIVE%CONTROL%FIRST M-A1 M-A9 M-B1 M-B4 M-C1 M-C4 --nx-brand-chrome --nx-brand-blue GROUND,%never%text REALLY%fell%back
real%browser Playwright ArrowLeft/ArrowRight light%AND%dark near-miss findability INDEPENDENT%CENSUS RGB_TRIPLE hsl() 66 147
FILE-DISJOINT git%clone%--shared REGENERATION 4037/242 3990/238 3982/236 4021/238 id-superset C-57 C-68 C-89 C-104 C-112
C-125 C-133 C-141 ADDENDUM%2 C-110 C-28 C-97 C-40 node%--check VOID EXCLUSIVE qa-b2- QUEUE,%NEVER%TAKE%OVER DEADLINE HEARTBEAT
2%minutes 5%minutes finally LANDING%CONTROL SESSION_SECRET%UNSET NOT%TESTED MEASURED%AT%RUNTIME READ%ONLY PROBED RELAYED
CI%NOT%RUN Prior-work%check FOREGROUND"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## RULED BY KAM, NOT YET IN AN ARTEFACT' '^## PRIOR ROUND' '^## 2a. LEGITIMATE SHAPES' '^## 3a. INSTRUMENT RULES' \
         '^## 4. TARGET A' '^## 5. TARGET B' '^## 6. TARGET C' '^## 7. THE MERGED TREE' '^## 9. Floor discipline' \
         '^## WRONG OR UNVERIFIED' '^## PROVENANCE'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done

# 24 — the prompt must DESCRIBE the server entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qi 'backend/server\.js'; then
  echo "REFUSING: the prompt contains the server entry point's literal path (RD-591 c.37901). Describe it; do not name it." >&2; exit 24; fi

# 53 / 71 — standing rules in the brief; the NOT TESTED line verbatim in both.
for w in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' 'qa-b2-' 'node --check' 'VOID' 'EXCLUSIVE' 'POSITIVE CONTROL FIRST' \
         'QUEUE, NEVER TAKE OVER' 'LANDING CONTROL' 'C-104'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the standing rule '$w'" >&2; exit 53; }
done
grep -qF "$NOTTESTED_LINE" "$BRIEF" || { echo "REFUSING: brief must carry the NOT TESTED line verbatim" >&2; exit 71; }
case "$PROMPT" in *"$NOTTESTED_LINE"*) ;; *) echo "REFUSING: prompt must carry the NOT TESTED line verbatim" >&2; exit 71 ;; esac

# 76 — S-1's lesson: the brief carries the ONE safe SESSION_SECRET printer verbatim and names the forbidden idioms.
grep -qF "$SAFE_PRINTER" "$BRIEF" || { echo "REFUSING: brief must carry the safe SESSION_SECRET printer verbatim (H-1)" >&2; exit 76; }
for w in '${SESSION_SECRET-…}' '${SESSION_SECRET+$SESSION_SECRET}' 'printenv'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief must name the forbidden idiom $w (H-1)" >&2; exit 76; }
done

# 77 — S-4's lesson: the heartbeat is a separate child, aborted if absent at 90 s, max gap reported.
for w in 'separate child' 'within 90 s' 'max gap'; do
  grep -qiF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the heartbeat rule fragment '$w' (H-4)" >&2; exit 77; }
done

# 38 — negative-control seats named in the brief; advisory if one has exited or a pane's claude changed.
for P in $NEG_SEATS; do
  grep -q "\`$P\`" "$BRIEF" || { echo "REFUSING: brief does not name seat pid $P as a negative control" >&2; exit 38; }
  [ "$(ps -o comm= -p "$P" 2>/dev/null | sed 's#.*/##')" = "claude" ] || echo "NOTE: negative-control seat $P is not a running claude now — re-read the seats and update the brief's section 9 before launch" >&2
done
if command -v tmux >/dev/null 2>&1; then
  for N in M N O P; do
    tmux list-panes -a -F '#{@cockpit_name}' 2>/dev/null | grep -qx "Datasec/NexusAI-$N" || echo "NOTE: no tmux pane named Datasec/NexusAI-$N now — re-read the seats before launch" >&2
  done
fi

# 32 — the coordinator stamps the self-check. LAST refusal, so --check shows every other guard first.
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "guards pass (9 6 7 8 18 22 75 23 35 70 31 39 10 17 11 12 13 14 15 20 19 24 53 71 76 77 38); self-check NOT stamped." >&2
  echo "REFUSING: the brief's SELF-CHECK line or Self-check note is unstamped — the coordinator re-reads end-to-end and stamps both before launch" >&2; exit 32
fi

# 40 — the answer route exists (after the stamp: Tuesday adds it, never this launcher).
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || {
  echo "REFUSING: no '${ROUTE_NAME}|tuesday-agent@agentmail.to|…' line in $ROUTING — answers to the gate would have no route" >&2; exit 40; }

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  origin $A_BRANCH == ${A_HEAD:0:7}, $B_BRANCH == ${B_HEAD:0:7}, $C_BRANCH == ${C_HEAD:0:7} at $PIN_TS (18); main ${M_ORIGIN:0:7}"
  echo "  RD-428/RD-444 two commits off 7c47ec4 (not main); RD-200 contains main via c01190d; main = 7c47ec4 + RD-579 + RD-639 (7 8)"
  echo "  deltas exact (22); tips counts-only (75); file-disjoint but the counts file (23); counts at nine shas (35)"
  echo "  package-lock ${LOCK_BLOB:0:7} everywhere (70); evidence (31); H-1 printer (76); H-4 heartbeat (77)"
  echo "  route $ROUTE_NAME (40); report absent (17); seats $NEG_SEATS named (38)"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  exit 0
fi

PROMPT="$PROMPT

VERIFIED BY THE LAUNCHER AT $PIN_TS (git ls-remote origin, read-only): refs/heads/$A_BRANCH = $A_HEAD; refs/heads/$B_BRANCH = $B_HEAD; refs/heads/$C_BRANCH = $C_HEAD; refs/heads/main = ${M_ORIGIN:-unreadable}. These are the start-of-gate pins; take your own three readings anyway."

# S-1 belt: the gate session inherits NO SESSION_SECRET. The line prints the NAME and a state only, never a value.
if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET in the launcher's environment (length ${#SESSION_SECRET}) — unsetting before exec"; else echo "SESSION_SECRET UNSET"; fi
unset SESSION_SECRET

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$PROMPT"
