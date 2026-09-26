#!/bin/bash
# launch_qa_nexusai_gate_batch5a.sh — cross-project QA agent, ONE batched gate on Datasec/NexusAI ("batch #5a", lane 1), SIX targets,
# SIX verdicts, ONE report (2026-09-27). Five built by NexusAI-M (S84M), one (RD-705) by S86M; merge author after the verdict = S86M. All TIER 1:
#   A — RD-681:  rd-681-clear-undecryptable-s84m @ 4209299 (off 1904765). clear decides from the raw store. 4137/248.
#   B — RD-682:  rd-682-clear-partial-audited-s84m @ f15fed6 = 4209299 + one commit (STACKED on RD-681; 681 merges first). 4143/249.
#   C — RD-627b: rd-627b-sigterm-flush-s84m @ c82aa92 (off 1904765). Second SIGTERM no longer kills the audit flush. 4137/248.
#   D — RD-695:  rd-695-stats-trend-undated-s84m @ ad97d12 (off 748cece; NOT merged forward onto 1904765). 4133/247.
#   E — RD-705:  rd-705-no-store-authenticated-pages-s86m @ e164d1a (off 1904765). Every HTML page no-store (C-171). 4137/248.
#   F — RD-413:  rd-413-truthful-mail-secret-storage-s84m @ f70594a (off 11666d3; NOT merged forward). Seven files. 4026/239.
#   Main at drafting 1904765 (4133/247). All six edit the server entry point; the author says region-disjoint; the drafter READ hunk headers only
#   and ran NO merge-tree (its hard rule) — guard 80 measures the premise in a scratch object dir. D and F are gated on merged-forward trees of
#   the gate's own. Predicted merged counts(M0) + 37 / + 7 = 4170/254 at 1904765.
#
# AUTHORITY: Tuesday's batch #5a commission (2026-09-27); READY mails, copies in briefs/. Merges: Tuesday's GO under Kam's standing grant
# (2026-09-25 ~22:0x, re-affirmed 2026-09-27 ~08:2x). This gate is FINDINGS-ONLY: no fix, no push, no deploy, nothing to Partner Center/demo/prod.
#
# PATTERN: launch_qa_nexusai_gate_batch3.sh (guard families 9 6 7 8 18 18b 22 75 23 35 70 80 31 39 10 17 11 12-15 20 19 24 53 71 76 77 78 79 81 38 32 40),
# prompt EMBEDDED. CHANGES, each deliberate:
#   - six targets; bases 1904765 x4, 748cece (D), 11666d3 (F); B's chain is A then B.
#   - 18b: main must be 1904765 or a descendant in the object store; REFUSE if its movement touches the six deltas; only NOTE movement of
#     jsonStorage / dataErasure / the brand corpus (batches 3 and 4 are live and WILL move main — refusing would force a re-brief per merge).
#   - 75: B's own commit is exactly helper + cell + server entry point + counts; main since 748cece ∩ D = counts; main since 11666d3 ∩ F =
#     {server entry point, counts} (the fleet's merge-forward of F is a CONTENT merge).
#   - 23: EXPECTED OVERLAPS: A∩B = {rd681 cell, server entry point, counts}; every other pair = {server entry point, counts}.
#   - 80: merge-tree premise in a FRESH mktemp object dir: every pair among B..F and M x D, M x F conflicts in the counts file ONLY.
#     THIS PREMISE IS THE DRAFTER'S PREDICTION FROM HUNK POSITIONS (plus RD-705 READY :41's claim), NEVER MEASURED BY THE DRAFTER.
#   - 81: the brief carries this batch's premises (4170/254, fwd-695/fwd-413, REAL-BROWSER and BRAND legs, OFF-GUIDE, the unguarded
#     duplicate flush, RD-636, the C-102 sweep).
#   - 38: negative-control seats read 2026-09-27 09:30:41 AEST (Tuesday's claude is now 23230; batch-3 and batch-4 gates and Vision gate 9 live).
#   - 40: the routing line QA/NexusAI-batch5a must exist (checked AFTER the stamp; Tuesday adds it).
#   - 32: SELF-CHECK stamp placeholder left UNFILLED by the drafter (comparand built by concatenation). LAST refusal before --check exits.
#   - LC_ALL=C for every sort/comm (the rd681 cell path starts with '__', which locale collation orders differently).
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/NexusAI-batch5a' "bash '<this file>'"), NEVER nohup.
# Identity: exports NexusAI's OWN az/gh dirs (az unused, gh optional and READ-ONLY); CLAUDE_CONFIG_DIR pinned to Tuesday's store.
# --check is READ-ONLY in NexusAI: git read verbs (cat-file, log, merge-base, diff, show, rev-parse, ls-remote) plus ONE merge-tree family
# (guard 80) whose objects go to a fresh mktemp dir, never to NexusAI's store; grep, ps, tmux.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate_batch5a.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..81 a guard refused
set -u
export LC_ALL=C
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
BRIEFS="$TUE/2_Project_Files/fleet/qa-agent/briefs"
BRIEF="$BRIEFS/2026-09-27_nexusai-gate-batch5a-rd681-rd682-rd627b-rd695-rd705-rd413.md"
READY_A="$BRIEFS/2026-09-26_nexusai-rd681-READY-mail.txt"
READY_B="$BRIEFS/2026-09-26_nexusai-rd682-READY-mail.txt"
READY_C="$BRIEFS/2026-09-26_nexusai-rd627b-READY-mail.txt"
READY_D="$BRIEFS/2026-09-26_nexusai-rd695-READY-mail.txt"
READY_E="$BRIEFS/2026-09-27_nexusai-rd705-READY-mail.txt"
READY_F="$BRIEFS/2026-09-26_nexusai-rd413-READY-mail.txt"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
NX='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI'
REPO="$NX/2_Project_Files"
EV_M="$NX/session-tools/s84m"
EV_M2="$NX/session-tools/s86m"
CLAR="$NX/1_Project_Definition/CLARIFICATIONS.md"
LANEPLAN="$NX/5_Project_History/2026-09-27_S86M_lane-plan-v2.md"
LANEPLAN1="$NX/5_Project_History/2026-09-25_S84M_lane-plan.md"
RPTS="$QA_DIR/projects/nexusai/reports"
PREV_G579="$RPTS/2026-09-25-gate-rd579-rd639/report.md"
PREV_B1="$RPTS/2026-09-26-gate-batch1/report.md"
PREV_B2="$RPTS/2026-09-26-gate-batch2-rd428-rd444-rd200/report.md"
PREV_G5="$RPTS/2026-09-22-gate5-rd615-rd616/report.md"
B1_EV="$RPTS/2026-09-26-gate-batch1/evidence"
B2_EV="$RPTS/2026-09-26-gate-batch2-rd428-rd444-rd200/evidence"
G579_EV="$RPTS/2026-09-25-gate-rd579-rd639/evidence"
PREV_FLOORLIB="$B1_EV/qa-floorlib.sh"
G7R1_FLOOR="$RPTS/2026-09-22-gate7-rd645/evidence/qa-floorcount.py"
REPORT="$RPTS/2026-09-27-gate-batch5a/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"
ROUTE_NAME='QA/NexusAI-batch5a'

MAIN_SHA='1904765007e9447ac6c980f9840c0689a02abe6c'      # origin main at drafting (RD-627a's merge; batches 1 and 2 complete)
MAIN_P1='057016de2b2929c23f643b7346413199f370d3ce'       # 1904765's first parent
MAIN_P2='748cecec2a883a117560824ac5615c268dfe0800'       # 1904765's second parent = RD-695's base
BASE_D='748cecec2a883a117560824ac5615c268dfe0800'        # RD-695's base (the RD-533 merge)
BASE_F='11666d3c4f615190646914270016419fffa642e2'        # RD-413's base
A_BRANCH='rd-681-clear-undecryptable-s84m'
A_HEAD="${QA_A_HEAD_OVERRIDE:-4209299c8858adf9e06cdcbcb717b8d6c40a23d4}"
B_BRANCH='rd-682-clear-partial-audited-s84m'
B_HEAD="${QA_B_HEAD_OVERRIDE:-f15fed6e5404792f60ac5e2939c1ea25cb41139f}"
C_BRANCH='rd-627b-sigterm-flush-s84m'
C_HEAD="${QA_C_HEAD_OVERRIDE:-c82aa92bec7688653149e4690efaeb3c137e602f}"
D_BRANCH='rd-695-stats-trend-undated-s84m'
D_HEAD="${QA_D_HEAD_OVERRIDE:-ad97d1202c2bb951ac1b604fe91771405a9685a2}"
E_BRANCH='rd-705-no-store-authenticated-pages-s86m'
E_HEAD="${QA_E_HEAD_OVERRIDE:-e164d1a99cb33166d37c98d6f9069d51a7c18ad7}"
F_BRANCH='rd-413-truthful-mail-secret-storage-s84m'
F_HEAD="${QA_F_HEAD_OVERRIDE:-f70594a2418bb26a5ec2d98d68e8e4ed620cd575}"

COUNTS_FILE='scripts/verify-expected-counts.json'
SRV='backend/server.js'
A_EXPECTED_FILES="__tests__/rd681-clear-undecryptable-key.test.js
$SRV
$COUNTS_FILE"
B_OWN_FILES="__tests__/helpers/rd682-keep-key-preload.js
__tests__/rd682-clear-partial-is-audited.test.js
$SRV
$COUNTS_FILE"
B_EXPECTED_FILES="__tests__/helpers/rd682-keep-key-preload.js
__tests__/rd681-clear-undecryptable-key.test.js
__tests__/rd682-clear-partial-is-audited.test.js
$SRV
$COUNTS_FILE"
C_EXPECTED_FILES="__tests__/rd627b-second-sigterm-finishes-flush.test.js
$SRV
$COUNTS_FILE"
D_EXPECTED_FILES="__tests__/rd695-stats-trend-no-today-fallback.test.js
$SRV
$COUNTS_FILE"
E_EXPECTED_FILES="__tests__/rd705-html-no-store.test.js
$SRV
$COUNTS_FILE"
F_EXPECTED_FILES="__tests__/rd413-mail-secret-storage-truth.test.js
__tests__/rd413-mail-secret-storage-ui.test.js
backend/server.js
backend/services/emailService.js
scripts/verify-expected-counts.json
static/first-run-setup.html
static/js/first-run-setup.js"
# NOTE-only (never a refusal): main moving these changes a composition the brief tells the gate to re-measure at M0.
SEMANTIC_NOTE_FILES="backend/jsonStorage.js
backend/dataErasure.js
static/css/dark-mode.css
static/css/tokens.css
static/css/keyboard-focus.css
docs/BRAND.md
__tests__/helpers/css-colors.js"

LOCK_BLOB='906476350431e2ecb3c21070a25c64b1702c1aa8'
NEG_SEATS='62649 9959 20317 23230 36118 40285 16516'   # M %19, N %21, P %22, Tuesday %0, QA batch3 %23, QA batch4 %24, QA Vision gate9 %25 — read 2026-09-27 09:30:41 AEST

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-681 · RD-682 · RD-627b · RD-695 · RD-705 · RD-413'
QUESTION_SUBJ='[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>'
ANSWER_PREFIX='[Tuesday -> QA/NexusAI-batch5a] ANSWER'
NOTTESTED_LINE="Not tested by this gate: Linux or CI at any branch head unless a PR's CI Build exists, Azure Container Apps, a real container runtime stop, Key Vault as a key source, a live Log Analytics workspace, any browser other than the one Chrome build named in the report, production mode, and Windows."
SAFE_PRINTER='if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET (length ${#SESSION_SECRET})"; else echo "SESSION_SECRET UNSET"; fi'

g() { git --no-optional-locks -C "$REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }
oneline() { tr '\n' ' ' | sed 's/ $//'; }
counts_at() { g show "${1}:${COUNTS_FILE}" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
blob() { g rev-parse "${1}:${2}" 2>/dev/null; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE batched gate on Datasec/NexusAI with SIX targets, SIX verdicts and ONE report: RD-681 (TIER 1), RD-682 (TIER 1), RD-627b (TIER 1), RD-695 (TIER 1), RD-705 (TIER 1) and RD-413 (TIER 1). Each ticket gets its own verdict — GO, GO WITH FINDINGS or NO GO — about its branch head AND about the merged tree. A finding on one ticket never becomes another's verdict; a finding that exists only in a COMPOSITION is graded on the merged tree and named against both tickets it joins. TIER 1 AT FULL WEIGHT, FINDINGS-ONLY: no fixes, no pushes, no deploys, nothing to Partner Center, the demo or production.

READ YOUR COMMISSION FIRST, whole: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-27_nexusai-gate-batch5a-rd681-rd682-rd627b-rd695-rd705-rd413.md
Then the charter it names, then the six READY mails it names, then the four earlier gate reports it names: the RD-579 gate (2026-09-25-gate-rd579-rd639: its A-F1 and A-F2 are what RD-681 and RD-682 claim to close), batch #1 (2026-09-26-gate-batch1: its E-C1 is what RD-695 claims to close, and its self-corrections are rules H-13 to H-16), batch #2 (2026-09-26-gate-batch2-rd428-rd444-rd200: its real-browser method, its R11 bfcache observation that RD-705 claims to close, its CDN allow-list and its brand method) and gate 5 (2026-09-22-gate5-rd615-rd616: its F-B4 is RD-636). Every builder statement is a CLAIM — RELAYED, never evidence. The brief's LEGITIMATE SHAPES tables (section 2a) and its REAL-BROWSER and BRAND legs (section 2b) are required measurements, row by row, base and head in the same window.

THE TARGETS. All six edit the server entry point. RD-681: branch rd-681-clear-undecryptable-s84m at 4209299c8858adf9e06cdcbcb717b8d6c40a23d4, one commit on main 1904765007e9447ac6c980f9840c0689a02abe6c; the AI-config clear decides from the raw stored fields, so an undecryptable key is removed and named. RD-682: branch rd-682-clear-partial-audited-s84m at f15fed6e5404792f60ac5e2939c1ea25cb41139f, STACKED on RD-681 (its parent is 4209299); a partial clear answers 500 with what it removed and what is still stored, and audits it. Merge order RD-681 then RD-682 is FIXED. RD-627b: branch rd-627b-sigterm-flush-s84m at c82aa92bec7688653149e4690efaeb3c137e602f on 1904765; a second SIGTERM during the shutdown audit flush no longer kills the flush — and its author DISCLOSED that the guard's "no duplicate flush" property is UNGUARDED by any cell: you say whether that matters and measure it (rows s5 and s6: the duplicate flush with the guard removed, and the interval flush that the guard does not cover at the head). RD-695: branch rd-695-stats-trend-undated-s84m at ad97d1202c2bb951ac1b604fe91771405a9685a2 on 748cecec2a883a117560824ac5615c268dfe0800 — NOT merged forward onto 1904765; the stats daily trends date a job by its own time, never today. RD-705: branch rd-705-no-store-authenticated-pages-s86m at e164d1a99cb33166d37c98d6f9069d51a7c18ad7 on 1904765; every HTML page is sent Cache-Control no-store (C-171, the lane-1 half of the RD-693 credential-page class; RD-693's lane-4 half is NOT in this gate). RD-413: branch rd-413-truthful-mail-secret-storage-s84m at f70594a2418bb26a5ec2d98d68e8e4ed620cd575 on 11666d3c4f615190646914270016419fffa642e2 — NOT merged forward, and seven files, not only the server entry point; the mail settings API, admin health and the first-run page say how each mail secret is actually stored (C-140).

THE MERGE-TREES AND THE MERGE ORDER. The drafter READ the hunk positions and ran NO merge-tree: every pairwise result is a PREDICTION (counts file only; the server entry point auto-merges) for you to measure, all fifteen pairs and both chains, in a SCRATCH object dir of your own (GIT_OBJECT_DIRECTORY set to your dir, the NexusAI objects as a read-only alternate), recording NexusAI's object count before and after. RD-413's fleet merge-forward CONTENT-merges the server entry point with main's RD-315 and RD-533 hunks. The drafter proposes the order RD-681, RD-682, RD-627b, RD-705, RD-695, RD-413 with predicted counts 4137/248, 4143/249, 4147/250, 4151/251, 4156/252, 4170/254, and a C-68 re-run set BY NAME for each merge. Challenge the order, confirm or correct the end state, and derive every C-68 set properly in your own clone with a positive control. If ANY file other than the counts file conflicts at any step, that STOPS the merged-tree arm (C-57: "Any other conflicting file still stops") — you record it and do not hand-resolve it.

RD-695 AND RD-413 ARE ON OLDER BASES. Gate each head as pushed, AND on a merged-forward tree of your own: fwd-695 = M0 merged with ad97d12, fwd-413 = M0 merged with f70594a, each in your own scratch clone, counts regenerated (predicted 4138/248 and 4147/249). You never push, never write a ref in NexusAI, and never merge into the author's branch: the fleet's merge-forward is the author's job after your verdict.

RD-681 (TIER 1). POSITIVE CONTROL FIRST: alone, beside and ollama red on 1904765 with the undecryptable blob built as the RD-579 gate built it (a second store with a different machine id), the fixture control green, 4/4 at the head. Mutants M1, M2 re-derived, then M-A1 to M-A4. Rows a1 to a9 — a5 first: the new reader is readFile-or-empty-object, the pattern the store's own RD-407 note calls fatal, so a torn settings file may read as "nothing held" and the clear may answer cleared without reading the store. L-A1: count the recovery copies that still hold the blob.

RD-682 (TIER 1). POSITIVE CONTROL FIRST at 4209299: the three partial cells red, the three controls green, 6/6 at the head, the keep-key preload's landing control proven by your own run. Mutants M1 to M3 re-derived, then M-B1 to M-B4. Rows b1 to b7; the partial-clear 500 rendered on the first-run page in the real browser (L-B2).

RD-627b (TIER 1). POSITIVE CONTROL FIRST: the double-signal cells red on 1904765 (exit null, killed mid-flush), the controls green, 4/4 at the head, the second signal proven to land inside the slow flush. Mutants M1, M2 re-derived (M2 reddening ONLY the log cell is the author's own proof that the no-duplicate property is uncelled), then M-C1 to M-C4. Rows s1 to s8 — s5 and s6 first: two flushes share one fixed tmp name with truncating writes, so a duplicate may tear or empty the persisted audit buffer; and the sixty-second interval flush is not behind the shutdown flag. Then one paragraph: does "no duplicate flush" matter, measured. Signals go ONLY to a server pid you spawned and proved to descend from your own claude pid (C-174: never kill by pattern).

RD-695 (TIER 1). POSITIVE CONTROL FIRST at 748cece and 1904765: the four trend cells red (every job in today's bucket), findability green, 5/5 at the head and on fwd-695. Mutants M1 to M4 re-derived with EXACT anchor counts (never grep -c: the builder's own counter once read 1593), then M-D1 to M-D4. Rows p1 to p10 — p3 (an ISO-shaped non-date becomes a bucket), p4 (an offset timestamp keeps its local date, not UTC) and p7 (slice(-30) keeps thirty distinct dated days; a far-future value evicts a real one) first. The batch-1 gate's E-C1 steps re-run.

RD-705 (TIER 1). POSITIVE CONTROL FIRST: N1 and N2 red on 1904765 (public, max-age=0), POP and CTRL-ASSET green, 4/4 at the head. Mutants M2 to M4 re-derived, then M-E1 to M-E4. Rows n1 to n12 — n5 (anything registered before the middleware never passes through it) and n7 (a 304 carries no Content-Type) first. The REAL-BROWSER leg w1 is RD-705's first proof: the batch-2 gate's R11 flow (Settings, SCIM, Generate, navigate away, Back) at 1904765 AND at the head AND merged — the token must not come back. Carry the user-visible change (every page re-fetches on Back) as a stated behaviour change, and measure its cost once (w7).

RD-413 (TIER 1). POSITIVE CONTROL FIRST at 11666d3 and 1904765: 12 of 14 red, the vacuous-at-base cell proven guarded, 14/14 at the head and on fwd-413. Mutants M1 to M4 re-derived, then M-F1 to M-F4. Rows m1 to m6 and m15 to m19 — m15 (an ENC blob the key cannot open is reported encrypted), m16 (a plaintext secret that begins with ENC is reported encrypted) and m17 (a torn file reads as none) first; m18: the storage states never reach anonymous health. REAL-BROWSER leg w2 and w3 (the notes, light and dark, announced or not) and the BRAND leg w4: every colour the diffs introduce, and the COMPUTED colour of the new notes, resolve by value to a token in the style guide's machine-readable form, else OFF-GUIDE, a Major — saying in the same sentence whether that colour is a pre-existing class colour. Then RD-636: from gate 5's F-B4, measured in the browser, say plainly whether RD-636 closes with RD-413.

THE REAL-BROWSER LEG (brief section 2b). Chrome through Playwright from YOUR OWN tree, as the batch-2 gate ran it; your loopback server under the network belt; open mode; keyboard only; every flow twice, loopback-only and with Tuesday's CDN allow-list exactly as batch #2 applied it (exact URLs, every request logged, SRI held, everything else aborted). No secret, needle or token in any screenshot. Your Chrome processes counted before and after.

THE NEGATIVE-ASSERTION SWEEP (brief section 3b, C-102). For every negative-asserting existing cell among the callers — RD-705 wraps writeHead for EVERY response, the widest population — measure with jest coverage of the product file, through the lock, at M0 and on the merged tree, whether it still reaches the line it is named for. Census every cell that asserts an exact mail-config or health response shape. Self-test first (a positive control, a negative control, a non-empty population) or ABORT. Report population, negative cells, still reaching, disarmed.

THE MERGED TREE — part of every verdict. In YOUR OWN scratch clone (git clone --shared --no-checkout into your own project dir; origin removed; local user config; gc.auto 0; merges and commits in the clone ONLY): M0, then merge --no-ff 4209299, f15fed6, c82aa92, e164d1a, ad97d12, f70594a. Predict each merge before it; anything other than the counts file conflicting STOPS. C-104: resolve and stage before any census or run. Counts by REGENERATION once after all six: predicted 4170/254 at M0 = 1904765, a prediction; the measurement decides. A second clone in reverse order; root trees identical apart from the counts file. C-112's condition beside the conclusion: the server entry point is identical to NO parent, proven by behaviour; quote its merged blob. id-superset control with the batch-1 gate's adapted C-57 copy, seven parents, missing 0 predicted (no member modifies or deletes a test file: H-12; C-133 and its ADDENDUM only if it misses). On the merged tree, one hold: every C-68 set by name, the merged columns of the rows the brief names and the composition rows x1 to x5, the sweep, the full verify, then one mutant per ticket. C-89 on your clone. Count the NexusAI object files before and after and account for any delta by mtime. Nothing leaves your clone.

FULL VERIFY of each head, of fwd-695, of fwd-413 and of the merged tree through the lock, SESSION_SECRET UNSET. Predicted 4209299 4137/248, f15fed6 4143/249, c82aa92 4137/248, ad97d12 4133/247, e164d1a 4137/248, f70594a 4026/239, fwd-695 4138/248, fwd-413 4147/249, merged 4170/254. Every failure by NAME; re-run-until-green is not an acceptance gate. A RED ARM COUNTS ONLY IF THE MUTANT STILL PARSES AND LANDED: node --check every mutated JS file and quote the exit code, assert each anchor matched once and the exact mutated text is present; a red from a mutant that does not parse, or a green from one that never landed, is a VOID arm.

THE INSTRUMENT RULES H-1 TO H-16 (brief section 3a). H-1: the ONLY SESSION_SECRET printer is the one the brief quotes; self-test it with a throwaway, scan every hold's logs for it, and let the scan's control plant a DIFFERENT marker; this batch's needles are credentials — scan every response, log, audit row, audit buffer, screenshot and DOM dump for each. H-2: never construct a product storage object on a DATA_DIR you are measuring after its server booted. H-3: a LANDING CONTROL for every hook, preload, signal-timing file, interval-flush trigger or mutant. H-4: the HEARTBEAT is a separate child of the hold wrapper, aborted if absent 90 s after the grant, max gap per hold reported (at most 120 s). H-5: restore your own perturbations before any hash. H-6: every extractor and census gets a positive control; quote every path (the QA path has spaces and a bang); every server under the network belt. H-7: mutants only through a quoted tool with a negative control. H-8: the exact new text present and the old absent once it is removed; exact substring anchor counts. H-9: byte-level plants via Buffer and xxd. H-10: prove the phenomenon reachable (the blob does not decrypt, the second signal lands inside the flush, the seeded row is in the store, the base really restores from bfcache) before measuring its absence. H-11: /bin/bash explicitly; every sha:path braced; never set -- or declare -A in the default shell. H-12: list every modified or deleted test file before the C-57 control. H-13: NUL-safe tree censuses. H-14: every driver ends with an END record or the run is VOID. H-15: preloads with -r in argv, never NODE_OPTIONS. H-16: prove the product's own reader sees every plant before relying on it.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT (git archive into a fresh mktemp dir under projects/nexusai/qa-trees/batch5a.*). Each tree is EXCLUSIVE to this gate and to one purpose. In the NexusAI repo use ONLY read verbs (show, log, diff, ls-tree, cat-file, rev-parse, merge-base, grep, ls-remote, archive, count-objects); never fetch, pull, push, checkout, worktree, commit, stash, gc, clean, or merge-tree --write-tree without your own scratch object directory there, and never work in its 2_Project_Files checkout or any builder worktree (C-28). Plants, torn files, preloads, held ports, browser profiles and scratch git repos ONLY under your own mktemp dirs. Findings-only: never push, no commits outside your clone, no tickets, no edits in NexusAI, never merge anything anywhere the fleet can see. No Azure (no az at all), no Key Vault, no docker, no demo, no public host except the CDN allow-list in the browser leg. No mail to any human. Never rm: quarantine.

FLOOR DISCIPLINE — section 12 of the brief exactly. QUEUE, NEVER TAKE OVER: the NexusAI seats AND two other live NexusAI gates (batch #3 and batch #4) share session-tools/nexusai-lock.sh with you. Every jest run, server boot, browser flow and signal drive goes through it with a tag starting qa-b5a- (C-141 gate-class, ADDENDUM 2 and 3: each new qa ticket earns a fresh, self-applied yield; C-110). When a merge ticket is already queued, file yours with --after that merge ticket's tag (C-141 ADDENDUM 4's tool), never ahead of it. Between gates the order is plain FIFO: never jump, move or signal another gate's ticket. Hold the lock once per multi-run measurement as a tracked child of your seat. Count foreign servers the C-125 way anchored on YOUR OWN claude pid, with the brief's seven negative-control seats classifying foreign in the same run (correct the stale ROOT and NEG defaults of the batch-1 gate's copied instrument first); record the foreign count beside every result; a hold with no live negative control aborts. A zero is reportable only beside a control that fired in the same window. DEADLINE AND HEARTBEAT: every probe, boot, request, signal drive and browser flow has a per-step DEADLINE and a client timeout, every server and browser is killed in a finally by its own pid, a HEARTBEAT line at least every 2 minutes during a hold, and a step with no heartbeat for 5 minutes is aborted and reported.

CI: whether any of the six branches has a PR, M0's CI Build, and what a push to main runs in the Deploy demo workflow (the last runs, and whether the repository variable CI_DEPLOY_ENABLED is set) are UNVERIFIED by the drafter — read them with gh READ ONLY or say you could not. CI NOT RUN at a head with no PR. gh never approves a deployment or dispatches anything.

RE-PIN at start, mid and end: all six branches and main — three timestamped readings with the branch name beside each sha. A TICKET head that disagrees with the brief is a FINDING and a reason to stop, never a typo to fix. Main may move, and is EXPECTED to while batches #3 and #4 merge: call main at your start M0; it must be 1904765 or a descendant whose movement touches none of the six deltas; if it moved the settings store module, the erasure module or the brand corpus, name them and run the rows the brief names at M0; if it moves again, your verdict names M0 and says what moved (C-68); never re-base mid-gate.

QUESTIONS: your routing name is QA/NexusAI-batch5a. If you must ask, mail tuesday-agent@agentmail.to with subject "[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>" and PROCEED ON THE SAFEST READING without waiting; Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/NexusAI-batch5a] ANSWER". Approval-class items are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your ONE report to: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-27-gate-batch5a/report.md

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with the subject exactly:
[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-681 · RD-682 · RD-627b · RD-695 · RD-705 · RD-413
Lead the body with one line per ticket (RD-681: <GO|GO WITH FINDINGS|NO GO> @ 4209299 · RD-682: … @ f15fed6 · RD-627b: … @ c82aa92 · RD-695: … @ ad97d12 and fwd-695 · RD-705: … @ e164d1a · RD-413: … @ f70594a and fwd-413), then one line naming M0, your recommended merge order, the merged blob of the server entry point, and whether RD-636 closes with RD-413, then one line on what a merge push to main triggers. Never wednesday-agent@. You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no 4_Credentials directory of its own. Never put the key, a planted needle or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice.

Rule 2 stands: what you did NOT test is first-class output — a NOT TESTED section carrying every builder's NOT TESTED list as the brief quotes it, every declared limit L-A1 to L-A3, L-B1, L-B2, L-C1 to L-C4, L-D1 to L-D4, L-E1 to L-E3 and L-F1 to L-F5 discharged with a measurement or left standing and named (C-112), Prior work checked for each ticket (C-49), and every action recommendation labelled MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. That section must carry this line verbatim:
Not tested by this gate: Linux or CI at any branch head unless a PR's CI Build exists, Azure Container Apps, a real container runtime stop, Key Vault as a key source, a live Log Analytics workspace, any browser other than the one Chrome build named in the report, production mode, and Windows.
PROMPT_EOF

# ---------------------------------------------------------------- GUARDS
[ -d "$QA_DIR" ]  || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]   || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -n "$PROMPT" ]  || { echo "embedded prompt is empty" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }
for S in "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD" "$E_HEAD" "$F_HEAD"; do
  [[ "$S" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: head '$S' is not a full 40-hex sha" >&2; exit 9; }
done

# 6 — every pinned sha is a commit in the object store (this launcher never fetches).
for S in "$MAIN_SHA" "$MAIN_P1" "$MAIN_P2" "$BASE_D" "$BASE_F" "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD" "$E_HEAD" "$F_HEAD"; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 7 — bases against main-at-drafting: A, B, C, E contain 1904765; D's merge-base is 748cece; F's is 11666d3.
for H in "$A_HEAD" "$B_HEAD" "$C_HEAD" "$E_HEAD"; do
  [ "$(g merge-base "$MAIN_SHA" "$H" 2>/dev/null)" = "$MAIN_SHA" ] || { echo "REFUSING: merge-base(main, ${H:0:7}) is not 1904765" >&2; exit 7; }
done
[ "$(g merge-base "$MAIN_SHA" "$D_HEAD" 2>/dev/null)" = "$BASE_D" ] || { echo "REFUSING: merge-base(main, RD-695) is not 748cece" >&2; exit 7; }
[ "$(g merge-base "$MAIN_SHA" "$F_HEAD" 2>/dev/null)" = "$BASE_F" ] || { echo "REFUSING: merge-base(main, RD-413) is not 11666d3" >&2; exit 7; }

# 8 — chains exact, parents exact; main's own parents.
[ "$(g log --format='%H %P' "${MAIN_SHA}..${A_HEAD}" 2>&1)" = "$A_HEAD $MAIN_SHA" ] || { echo "REFUSING: 1904765..RD-681 is not exactly one commit 4209299 on 1904765" >&2; exit 8; }
[ "$(g log --format='%H %P' "${MAIN_SHA}..${B_HEAD}" 2>&1)" = "$B_HEAD $A_HEAD
$A_HEAD $MAIN_SHA" ] || { echo "REFUSING: 1904765..RD-682 is not exactly 4209299 (RD-681) then f15fed6 — the stack moved" >&2; exit 8; }
[ "$(g log --format='%H %P' "${MAIN_SHA}..${C_HEAD}" 2>&1)" = "$C_HEAD $MAIN_SHA" ] || { echo "REFUSING: 1904765..RD-627b is not exactly one commit c82aa92" >&2; exit 8; }
[ "$(g log --format='%H %P' "${MAIN_SHA}..${E_HEAD}" 2>&1)" = "$E_HEAD $MAIN_SHA" ] || { echo "REFUSING: 1904765..RD-705 is not exactly one commit e164d1a" >&2; exit 8; }
[ "$(g log --format='%H %P' "${BASE_D}..${D_HEAD}" 2>&1)" = "$D_HEAD $BASE_D" ] || { echo "REFUSING: 748cece..RD-695 is not exactly one commit ad97d12" >&2; exit 8; }
[ "$(g log --format='%H %P' "${BASE_F}..${F_HEAD}" 2>&1)" = "$F_HEAD $BASE_F" ] || { echo "REFUSING: 11666d3..RD-413 is not exactly one commit f70594a" >&2; exit 8; }
[ "$(g log -1 --format='%P' "$MAIN_SHA" 2>&1)" = "$MAIN_P1 $MAIN_P2" ] || { echo "REFUSING: 1904765's parents are not 057016d 748cece — re-brief" >&2; exit 8; }

# 18 — RE-PIN NOW by ls-remote: the six ticket branches exactly the pinned heads (REFUSE on mismatch).
for PAIR in "$A_BRANCH $A_HEAD" "$B_BRANCH $B_HEAD" "$C_BRANCH $C_HEAD" "$D_BRANCH $D_HEAD" "$E_BRANCH $E_HEAD" "$F_BRANCH $F_HEAD"; do
  BR="${PAIR%% *}"; H="${PAIR#* }"
  L="$(g ls-remote origin "refs/heads/$BR" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: origin refs/heads/$BR is not $H — moved or never pushed; re-brief. ls-remote said:" >&2; printf '%s\n' "${L:-<nothing>}" >&2; exit 18; }
done
# 18b — main: it may move (batches 3 and 4 are live). It must be 1904765 or a descendant IN THE OBJECT STORE; its movement must not touch
# the six deltas (REFUSE); movement of the semantic files is NOTED for the gate (never a refusal — see the header).
M_ORIGIN="$(g ls-remote origin refs/heads/main 2>/dev/null | awk '{print $1}')"
[[ "$M_ORIGIN" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: could not read origin main by ls-remote (got '${M_ORIGIN:-nothing}')" >&2; exit 18; }
[ "$(g cat-file -t "$M_ORIGIN" 2>&1)" = "commit" ] || { echo "REFUSING: origin main $M_ORIGIN is not in the object store — this launcher never fetches; wait for a seat's fetch or re-brief" >&2; exit 18; }
g merge-base --is-ancestor "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null || { echo "REFUSING: origin main $M_ORIGIN does not descend from 1904765 — main was rewritten; re-brief" >&2; exit 18; }
ALLD="$( { printf '%s\n' "$A_EXPECTED_FILES" "$B_EXPECTED_FILES" "$C_EXPECTED_FILES" "$D_EXPECTED_FILES" "$E_EXPECTED_FILES" "$F_EXPECTED_FILES"; } | sed '/^$/d' | grep -vxF "$COUNTS_FILE" | sort -u)"
MOVED="$(g diff --name-only "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null | sort -u)"
HIT="$(comm -12 <(printf '%s\n' "$ALLD") <(printf '%s\n' "$MOVED" | sed '/^$/d'))"
[ -z "$HIT" ] || { echo "REFUSING: main moved 1904765..${M_ORIGIN:0:7} and touched a file of the six deltas: $HIT — the merged-tree premise changes; re-brief" >&2; exit 18; }
SEMHIT="$(comm -12 <(sorted "$SEMANTIC_NOTE_FILES") <(printf '%s\n' "$MOVED" | sed '/^$/d') | oneline)"
[ "$M_ORIGIN" = "$MAIN_SHA" ] || echo "NOTE: origin main is now ${M_ORIGIN:0:7} (moved from 1904765, $(printf '%s\n' "$MOVED" | sed '/^$/d' | wc -l | tr -d ' ') paths, none in the six deltas) — the gate re-pins M0 itself" >&2
[ -z "$SEMHIT" ] || echo "NOTE: main's movement touched semantic files the brief names for re-measurement at M0: $SEMHIT (brief §1 'Main may move' item 3)" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — each delta is EXACTLY the commissioned file set.
chk_delta() { local from="$1" to="$2" want="$3" label="$4" got
  got="$(g diff --name-only "$from" "$to" 2>/dev/null | sort)"
  [ "$got" = "$(sorted "$want")" ] || { echo "REFUSING: $label delta is not the commissioned set. Got:" >&2; printf '%s\n' "$got" >&2; exit 22; }; }
chk_delta "$MAIN_SHA" "$A_HEAD" "$A_EXPECTED_FILES" "RD-681 (1904765..4209299)"
chk_delta "$MAIN_SHA" "$B_HEAD" "$B_EXPECTED_FILES" "RD-682 (1904765..f15fed6)"
chk_delta "$MAIN_SHA" "$C_HEAD" "$C_EXPECTED_FILES" "RD-627b (1904765..c82aa92)"
chk_delta "$BASE_D"   "$D_HEAD" "$D_EXPECTED_FILES" "RD-695 (748cece..ad97d12)"
chk_delta "$MAIN_SHA" "$E_HEAD" "$E_EXPECTED_FILES" "RD-705 (1904765..e164d1a)"
chk_delta "$BASE_F"   "$F_HEAD" "$F_EXPECTED_FILES" "RD-413 (11666d3..f70594a)"

# 75 — B's own commit; main since D's and F's bases vs their files.
chk_delta "$A_HEAD" "$B_HEAD" "$B_OWN_FILES" "RD-682's own commit (4209299..f15fed6)"
COMMON_D="$(comm -12 <(g diff --name-only "$BASE_D" "$MAIN_SHA" 2>/dev/null | sort) <(sorted "$D_EXPECTED_FILES") | oneline)"
[ "$COMMON_D" = "$COUNTS_FILE" ] || { echo "REFUSING: main since 748cece shares '${COMMON_D:-<nothing>}' with RD-695's files, expected the counts file only" >&2; exit 75; }
COMMON_F="$(comm -12 <(g diff --name-only "$BASE_F" "$MAIN_SHA" 2>/dev/null | sort) <(sorted "$F_EXPECTED_FILES") | oneline)"
WANT_F="$(sorted "$SRV
$COUNTS_FILE" | oneline)"
[ "$COMMON_F" = "$WANT_F" ] || { echo "REFUSING: main since 11666d3 shares '${COMMON_F:-<nothing>}' with RD-413's files, expected '$WANT_F'" >&2; exit 75; }

# 23 — EXPECTED OVERLAPS: A∩B = {rd681 cell, server entry point, counts}; every other pair = {server entry point, counts}.
DA="$(g diff --name-only "$MAIN_SHA" "$A_HEAD" 2>/dev/null | sort)"
DB="$(g diff --name-only "$MAIN_SHA" "$B_HEAD" 2>/dev/null | sort)"
DC="$(g diff --name-only "$MAIN_SHA" "$C_HEAD" 2>/dev/null | sort)"
DD="$(g diff --name-only "$BASE_D" "$D_HEAD" 2>/dev/null | sort)"
DE="$(g diff --name-only "$MAIN_SHA" "$E_HEAD" 2>/dev/null | sort)"
DF="$(g diff --name-only "$BASE_F" "$F_HEAD" 2>/dev/null | sort)"
WANT_AB="$(sorted "$A_EXPECTED_FILES" | oneline)"
WANT_ANY="$(sorted "$SRV
$COUNTS_FILE" | oneline)"
for PAIR in A_B A_C A_D A_E A_F B_C B_D B_E B_F C_D C_E C_F D_E D_F E_F; do
  X="${PAIR%%_*}"; Y="${PAIR#*_}"; eval "SX=\"\$D$X\""; eval "SY=\"\$D$Y\""
  COMMON="$(comm -12 <(printf '%s\n' "$SX") <(printf '%s\n' "$SY") | oneline)"
  case "$PAIR" in
    A_B) WANT="$WANT_AB" ;;
    *) WANT="$WANT_ANY" ;;
  esac
  [ "$COMMON" = "$WANT" ] || { echo "REFUSING: deltas $X and $Y share '${COMMON:-<nothing>}', expected '$WANT'" >&2; exit 23; }
done

# 35 — counts at every pinned sha.
for PAIR in "$MAIN_SHA 4133 247" "$BASE_D 4128 246" "$BASE_F 4012 237" \
            "$A_HEAD 4137 248" "$B_HEAD 4143 249" "$C_HEAD 4137 248" "$D_HEAD 4133 247" "$E_HEAD 4137 248" "$F_HEAD 4026 239"; do
  S="${PAIR%% *}"; WANT="${PAIR#* }"
  CT="$(counts_at "$S")"
  [ "$CT" = "$WANT" ] || { echo "REFUSING: $COUNTS_FILE at ${S:0:7} reads '${CT:-unreadable}', not '$WANT'" >&2; exit 35; }
done

# 70 — package-lock identical everywhere (one node_modules serves every tree), main-now included.
for S in "$MAIN_SHA" "$BASE_D" "$BASE_F" "$M_ORIGIN" "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD" "$E_HEAD" "$F_HEAD"; do
  [ "$(blob "$S" package-lock.json)" = "$LOCK_BLOB" ] || { echo "REFUSING: package-lock at ${S:0:7} is not ${LOCK_BLOB:0:7}" >&2; exit 70; }
done

# 80 — the merge-tree premise (the DRAFTER'S PREDICTION, never measured by the drafter), measured here in a FRESH scratch object dir
# (never NexusAI's store): every pair among B..F, and main x D, main x F, conflicts in the counts file ONLY.
MT_OBJ="$(mktemp -d "${TMPDIR:-/tmp}/qa-b5a-mtobj.XXXXXX")" || { echo "REFUSING: cannot make a scratch object dir" >&2; exit 80; }
mt_conf() { GIT_OBJECT_DIRECTORY="$MT_OBJ" GIT_ALTERNATE_OBJECT_DIRECTORIES="$REPO/.git/objects" \
  git --no-optional-locks -C "$REPO" merge-tree --write-tree --name-only "$1" "$2" 2>/dev/null | awk 'NR==1{next} /^$/{exit} {print}' | sort | oneline; }
for PAIR in "$B_HEAD $C_HEAD" "$B_HEAD $D_HEAD" "$B_HEAD $E_HEAD" "$B_HEAD $F_HEAD" "$C_HEAD $D_HEAD" "$C_HEAD $E_HEAD" "$C_HEAD $F_HEAD" \
            "$D_HEAD $E_HEAD" "$D_HEAD $F_HEAD" "$E_HEAD $F_HEAD" "$MAIN_SHA $D_HEAD" "$MAIN_SHA $F_HEAD"; do
  X="${PAIR%% *}"; Y="${PAIR#* }"
  GOT="$(mt_conf "$X" "$Y")"
  [ "$GOT" = "$COUNTS_FILE" ] || { echo "REFUSING: merge-tree ${X:0:7} x ${Y:0:7} conflicts in '${GOT:-<nothing>}', not the counts file only — the region-disjoint premise is wrong; re-brief" >&2; exit 80; }
done

# 31 — builder evidence, prior reports, standing references and tools on disk.
for f in "$READY_A" "$READY_B" "$READY_C" "$READY_D" "$READY_E" "$READY_F" "$CLAR" "$LANEPLAN" "$LANEPLAN1" \
         "$PREV_G579" "$PREV_B1" "$PREV_B2" "$PREV_G5" \
         "$EV_M/rd681-hold.log" "$EV_M/rd681-red-at-1904765.log" "$EV_M/rd682-hold.log" "$EV_M/rd682-red-at-4209299.log" \
         "$EV_M/rd627b-hold.log" "$EV_M/rd627b-red-at-1904765.log" "$EV_M/rd695-hold.log" "$EV_M/rd695-red-at-748cece.log" \
         "$EV_M/rd413-hold.log" "$EV_M/rd413-red-at-11666d3.log" "$EV_M2/rd705-hold.log" "$EV_M2/rd705-red-at-1904765.log" \
         "$NX/session-tools/nexusai-lock.sh" "$NX/session-tools/c57-id-superset.sh" \
         "$PREV_FLOORLIB" "$B1_EV/qa-floorcount.py" "$B1_EV/qa-dispatch.sh" "$B1_EV/qa-mutate.py" "$B1_EV/qa-c57-id-superset.sh" "$B1_EV/qa-netbelt.sb" \
         "$B1_EV/qa-e-probe.js" "$B1_EV/qa-e6-seed.js" "$B1_EV/q-merged-identity.py" \
         "$B2_EV/qa-a-browser.js" "$B2_EV/qa-a-lib.js" "$B2_EV/qa-png.js" "$G579_EV/qa-servercond-decrypt.js" "$G579_EV/qa-a-probe.js" \
         "$G7R1_FLOOR" "$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"; do
  [ -s "$f" ] || { echo "REFUSING: evidence or tool absent: $f" >&2; exit 31; }
done
grep -qF "${A_HEAD:0:7}" "$READY_A" || { echo "REFUSING: the RD-681 READY does not name ${A_HEAD:0:7}" >&2; exit 31; }
grep -qF "${B_HEAD:0:7}" "$READY_B" || { echo "REFUSING: the RD-682 READY does not name ${B_HEAD:0:7}" >&2; exit 31; }
grep -qF "${A_HEAD:0:7}" "$READY_B" || { echo "REFUSING: the RD-682 READY does not name its RD-681 parent ${A_HEAD:0:7}" >&2; exit 31; }
grep -qF "${C_HEAD:0:7}" "$READY_C" || { echo "REFUSING: the RD-627b READY does not name ${C_HEAD:0:7}" >&2; exit 31; }
grep -qF "${D_HEAD:0:7}" "$READY_D" || { echo "REFUSING: the RD-695 READY does not name ${D_HEAD:0:7}" >&2; exit 31; }
grep -qF "${E_HEAD:0:7}" "$READY_E" || { echo "REFUSING: the RD-705 READY does not name ${E_HEAD:0:7}" >&2; exit 31; }
grep -qF "${F_HEAD:0:7}" "$READY_F" || { echo "REFUSING: the RD-413 READY does not name ${F_HEAD:0:7}" >&2; exit 31; }

# 39 — the floor instruments are named in the brief.
for f in "$PREV_FLOORLIB" "$G7R1_FLOOR"; do
  grep -qF "$f" "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument $f" >&2; exit 39; }
done

# 10 / 17 — report path named in both; no stale report; brief names every source it cites.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }
for P in "$PREV_G579" "$PREV_B1" "$PREV_B2" "$PREV_G5" "$READY_A" "$READY_B" "$READY_C" "$READY_D" "$READY_E" "$READY_F"; do
  grep -qF "$P" "$BRIEF" || grep -qF "${P#$QA_DIR/}" "$BRIEF" || { echo "REFUSING: brief must name $P" >&2; exit 10; }
done

# 11 — identity: NexusAI's OWN dirs.
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

# 12 / 13 / 14 / 15 / 20 — tiers, directive, brief path, pins, verdict route, key path, question route.
for T in 'RD-681 is TIER 1' 'RD-682 is TIER 1' 'RD-627b is TIER 1' 'RD-695 is TIER 1' 'RD-705 is TIER 1' 'RD-413 is TIER 1' 'One verdict PER ticket' 'TIER 1 AT FULL WEIGHT'; do
  grep -qF "$T" "$BRIEF" || { echo "REFUSING: brief does not declare '$T'" >&2; exit 12; }
done
for T in 'RD-681 (TIER 1)' 'RD-682 (TIER 1)' 'RD-627b (TIER 1)' 'RD-695 (TIER 1)' 'RD-705 (TIER 1)' 'RD-413 (TIER 1)' 'SIX verdicts' 'TIER 1 AT FULL WEIGHT'; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare '$T'" >&2; exit 12 ;; esac
done
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
for S in "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD" "$E_HEAD" "$F_HEAD" "$MAIN_SHA" "$BASE_D" "$BASE_F"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S" >&2; exit 14; }
  case "$PROMPT" in *"$S"*) ;; *) echo "REFUSING: prompt must name $S" >&2; exit 14 ;; esac
done
if printf '%s\n' "$PROMPT" | grep -q '@[A-Z_]*@'; then echo "REFUSING: the prompt carries a placeholder" >&2; exit 14; fi
case "$PROMPT" in *"MAIL YOUR VERDICT"*"tuesday-agent@agentmail.to"*) ;; *) echo "REFUSING: prompt must say MAIL YOUR VERDICT to tuesday-agent@agentmail.to" >&2; exit 15 ;; esac
grep -qF "$SUBJECT" "$BRIEF" || { echo "REFUSING: brief must carry the verdict subject exactly" >&2; exit 15; }
case "$PROMPT" in *"$SUBJECT"*) ;; *) echo "REFUSING: prompt must carry the verdict subject exactly" >&2; exit 15 ;; esac
case "$PROMPT" in *"/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env"*) ;; *) echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20 ;; esac
for T in "$QUESTION_SUBJ" "$ANSWER_PREFIX" "$ROUTE_NAME"; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the question route: $T" >&2; exit 20; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the question route: $T" >&2; exit 20 ;; esac
done
if printf '%s\n' "$PROMPT" | grep -qi 'wednesday-agent@' && ! printf '%s\n' "$PROMPT" | grep -q 'Never wednesday-agent@'; then
  echo "REFUSING: the prompt routes to wednesday-agent@ — Datasec's coordinator is Tuesday" >&2; exit 15; fi

# 19 — the words the prompt must carry (% is a space); and the brief's sections.
WORDS="RD-681 RD-682 RD-627b RD-695 RD-705 RD-413 RD-579 RD-693 RD-636 A-F1 A-F2 E-C1 F-B4 R11 C-171 C-140 C-102 C-174 H-1 H-16 M0 COMPOSITION
STACKED UNGUARDED no%duplicate%flush s5 s6 a5 p3 p4 p7 n5 n7 m15 m16 m17 m18 w1 w4 x1 x5 M-A1 M-A4 M-B1 M-B4 M-C1 M-C4 M-D1 M-D4 M-E1 M-E4 M-F1 M-F4
POSITIVE%CONTROL%FIRST REAL-BROWSER BRAND OFF-GUIDE CDN%allow-list NEGATIVE-ASSERTION%SWEEP fwd-695 fwd-413 4170/254 4137/248 4143/249 4133/247 4026/239
4138/248 4147/249 SCRATCH%object%dir reverse%order git%clone%--shared REGENERATION id-superset C-57 C-68 C-89 C-104 C-112 C-125 C-133 ADDENDUM C-141
--after C-110 C-28 node%--check VOID EXCLUSIVE qa-b5a- QUEUE,%NEVER%TAKE%OVER FIFO DEADLINE HEARTBEAT 2%minutes 5%minutes finally LANDING%CONTROL
SESSION_SECRET%UNSET NOT%TESTED MEASURED%AT%RUNTIME READ%ONLY PROBED RELAYED CI%NOT%RUN Deploy%demo CI_DEPLOY_ENABLED Prior%work FOREGROUND never%push"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## RULED BY KAM, NOT YET IN AN ARTEFACT' '^## PRIOR ROUND' '^## 2a. LEGITIMATE SHAPES' '^## 2b. THE REAL-BROWSER LEG AND THE BRAND LEG' \
         '^## 3a. INSTRUMENT RULES' '^## 3b. THE NEGATIVE-ASSERTION SWEEP' '^## 4. TARGET A' '^## 5. TARGET B' '^## 6. TARGET C' '^## 7. TARGET D' \
         '^## 8. TARGET E' '^## 9. TARGET F' '^## 10. THE MERGED TREE' '^## 11. CI' '^## 12. Floor discipline' '^## WRONG OR UNVERIFIED' \
         '^## PROVENANCE' '^### MERGE ORDER'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
for L in L-A1 L-A3 L-B1 L-B2 L-C1 L-C4 L-D1 L-D4 L-E1 L-E3 L-F1 L-F5; do
  grep -qF "$L" "$BRIEF" || { echo "REFUSING: brief lacks declared limit $L (C-112)" >&2; exit 19; }
  case "$PROMPT" in *"$L"*) ;; *) echo "REFUSING: prompt lacks declared limit $L (C-112)" >&2; exit 19 ;; esac
done
# every builder's NOT TESTED list is carried verbatim (one distinctive fragment from each READY, checked in the READY AND the brief)
for PAIR in "$READY_A|Recovery copies: settings.backup.json and backups/ still hold the old blob" \
            "$READY_B|the first-run page's rendering of this 500" \
            "$READY_C|a real container runtime stop (TERM, then KILL after the grace)" \
            "$READY_D|E-C2 (generateAutomaticInsights :19926/:20031, the same class) is NOT built here" \
            "$READY_E|An HTML response whose Content-Type is set only after writeHead" \
            "$READY_F|The upgrade shape is driven by SEEDING a plaintext file"; do
  F="${PAIR%%|*}"; T="${PAIR#*|}"
  grep -qF -- "$T" "$F" || { echo "REFUSING: '$T' is no longer in $F — the READY changed; re-brief" >&2; exit 19; }
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not carry the NOT TESTED fragment '$T' verbatim" >&2; exit 19; }
done

# 24 — the prompt must DESCRIBE the server entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qi 'server\.js'; then
  echo "REFUSING: the prompt contains the server entry point's file name (RD-591 c.37901). Describe it; do not name it." >&2; exit 24; fi

# 53 / 71 — standing rules in the brief; the NOT TESTED line verbatim in both.
for w in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' 'qa-b5a-' 'node --check' 'VOID' 'EXCLUSIVE' 'POSITIVE CONTROL FIRST' \
         'QUEUE, NEVER TAKE OVER' 'LANDING CONTROL' 'C-104' 'Main may move' '--after' 'never push' 'C-174' 'FIFO'; do
  grep -qiF -- "$w" "$BRIEF" || { echo "REFUSING: brief lacks the standing rule '$w'" >&2; exit 53; }
done
grep -qF "$NOTTESTED_LINE" "$BRIEF" || { echo "REFUSING: brief must carry the NOT TESTED line verbatim" >&2; exit 71; }
case "$PROMPT" in *"$NOTTESTED_LINE"*) ;; *) echo "REFUSING: prompt must carry the NOT TESTED line verbatim" >&2; exit 71 ;; esac

# 76 — the brief carries the ONE safe SESSION_SECRET printer verbatim and names the forbidden idioms (H-1).
grep -qF "$SAFE_PRINTER" "$BRIEF" || { echo "REFUSING: brief must carry the safe SESSION_SECRET printer verbatim (H-1)" >&2; exit 76; }
for w in '${SESSION_SECRET-…}' '${SESSION_SECRET+$SESSION_SECRET}' 'printenv' '${envs[*]}'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief must name the forbidden idiom $w (H-1)" >&2; exit 76; }
done

# 77 — the heartbeat is a separate child, aborted if absent at 90 s, max gap reported (H-4).
for w in 'separate child' 'within 90 s' 'max gap'; do
  grep -qiF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the heartbeat rule fragment '$w' (H-4)" >&2; exit 77; }
done

# 78 — byte-level plants via Buffer, verified with xxd (H-9).
for w in 'H-9' 'Buffer' 'xxd -l 16' 'JSON.stringify'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the byte-plant rule fragment '$w' (H-9)" >&2; exit 78; }
done

# 79 — quoted mutant tool with a negative control; insertion-aware landing rule (H-7, H-8).
for w in 'H-7' 'H-8' 'negative control' 'original text is absent once the new text is removed'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the mutant-landing rule fragment '$w' (H-7/H-8)" >&2; exit 79; }
done

# 81 — this batch's own premises are in the brief.
for w in '4170/254' 'fwd-695' 'fwd-413' 'REAL-BROWSER' 'THE BRAND PROCEDURE' 'OFF-GUIDE' 'no duplicate flush' 'RD-636' 'Any other conflicting file still stops' \
         'still reach the check it is NAMED for' 'NOT MEASURED BY THE DRAFTER' 'STACKED on RD-681' 'H-13' 'H-16'; do
  grep -qF -- "$w" "$BRIEF" || { echo "REFUSING: brief lacks this batch's premise '$w'" >&2; exit 81; }
done

# 38 — negative-control seats named in the brief; advisory if one has exited or a pane's claude changed.
for P in $NEG_SEATS; do
  grep -q "\`$P\`" "$BRIEF" || { echo "REFUSING: brief does not name seat pid $P as a negative control" >&2; exit 38; }
  [ "$(ps -o comm= -p "$P" 2>/dev/null | sed 's#.*/##')" = "claude" ] || echo "NOTE: negative-control seat $P is not a running claude now — re-read the seats and update the brief's section 12 before launch" >&2
done
if command -v tmux >/dev/null 2>&1; then
  for N in M N P; do
    tmux list-panes -a -F '#{@cockpit_name}' 2>/dev/null | grep -qx "Datasec/NexusAI-$N" || echo "NOTE: no tmux pane named Datasec/NexusAI-$N now (the seats churn) — re-read the seats before launch" >&2
  done
fi

# 32 — the coordinator stamps the self-check. LAST refusal, so --check shows every other guard first.
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "guards pass (9 6 7 8 18 18b 22 75 23 35 70 80 31 39 10 17 11 12 13 14 15 20 19 24 53 71 76 77 78 79 81 38); self-check NOT stamped." >&2
  echo "REFUSING: the brief's SELF-CHECK line or Self-check note is unstamped — the coordinator re-reads end-to-end and stamps both before launch" >&2; exit 32
fi

# 40 — the answer route exists (after the stamp: Tuesday adds it, never this launcher).
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || {
  echo "REFUSING: no '${ROUTE_NAME}|tuesday-agent@agentmail.to|…' line in $ROUTING — answers to the gate would have no route" >&2; exit 40; }

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  origin $A_BRANCH == ${A_HEAD:0:7}, $B_BRANCH == ${B_HEAD:0:7}, $C_BRANCH == ${C_HEAD:0:7}, $D_BRANCH == ${D_HEAD:0:7}, $E_BRANCH == ${E_HEAD:0:7}, $F_BRANCH == ${F_HEAD:0:7} at $PIN_TS (18)"
  echo "  main ${M_ORIGIN:0:7} (1904765 or a descendant; moved paths touch none of the six deltas)${SEMHIT:+; NOTED semantic: $SEMHIT} (18b)"
  echo "  bases 1904765 x4 / 748cece / 11666d3 (7); chains exact (8); deltas exact (22); RD-682's own commit and main-vs-older-bases (75); overlaps (23); counts at nine shas (35)"
  echo "  package-lock ${LOCK_BLOB:0:7} everywhere (70); merge-tree premise in scratch $MT_OBJ (80); evidence (31); H-1 (76); H-4 (77); H-9 (78); H-7/H-8 (79); premises (81)"
  echo "  route $ROUTE_NAME (40); report absent (17); seats $NEG_SEATS named (38)"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  exit 0
fi

PROMPT="$PROMPT

VERIFIED BY THE LAUNCHER AT $PIN_TS (git ls-remote origin, read-only): refs/heads/$A_BRANCH = $A_HEAD; refs/heads/$B_BRANCH = $B_HEAD; refs/heads/$C_BRANCH = $C_HEAD; refs/heads/$D_BRANCH = $D_HEAD; refs/heads/$E_BRANCH = $E_HEAD; refs/heads/$F_BRANCH = $F_HEAD; refs/heads/main = $M_ORIGIN (1904765 or a descendant whose movement touches none of the six deltas${SEMHIT:+; it moved these semantic files: $SEMHIT}). These are the start-of-gate pins; take your own three readings anyway, and re-pin M0 yourself."

# rd579-rd639 S-1 belt: the gate session inherits NO SESSION_SECRET. The line prints the NAME and a state only, never a value.
if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET in the launcher's environment (length ${#SESSION_SECRET}) — unsetting before exec"; else echo "SESSION_SECRET UNSET"; fi
unset SESSION_SECRET

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$PROMPT"
