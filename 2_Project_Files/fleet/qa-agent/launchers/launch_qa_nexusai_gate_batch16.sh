#!/bin/bash
# launch_qa_nexusai_gate_batch16.sh — cross-project QA agent, ONE gate on Datasec/NexusAI ("batch 16"), ONE member, one verdict, ONE report
# (drafted 2026-10-05 21:57:11–22:14:23 AEDT by a read-only drafting agent for Tuesday).
# A FRESH gate (not a resume): M0 is origin main as the gate reads it at its own start.
#   RD-618 (b1) re-gate (TIER 2 through code; round 1 of 2 for this class) rd-618-csp-intake-residue-s86m @ 953a0e6:
#     874c4f5 (batch 9 GO WITH FINDINGS) -> db57ec1 (merge of main b7bb1e9) -> baf3f6e counts -> fd01298 (test-only CodeQL fix A, not gated)
#     -> a1d484d (THIS ROUND: the cap log line is fixed text + the server-side cap; R8 added) -> 953a0e6 counts 4266/260. PR #47 OPEN.
#   Main at drafting e91ff4e (RD-314 landed 21:30 AEDT; counts 4262/260). Predicted MT1 4276/261.
#
# LAUNCHED ONLY VIA: cockpit.sh add 'QA/NexusAI-batch16' "bash '/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate_batch16.sh'"
#   (i.e. /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh). A tmux pane, NEVER nohup, never run it bare from a seat's shell.
#
# AUTHORITY: Tuesday's (b1) RULING (fleet/briefs_staged/2026-10-05_nexusai_MN_rd618_b1_turn.md, item 3: the re-gate) and the batch-16 commission
# (~22:00 AEDT); the READY mail copied in briefs/. THE MODEL RULE: Kam, live board 2026-09-30 09:07, card nexusai-gate11-opus55-safeguard-model-switch,
# option (b) — QA gates may switch to Opus 4.8 when flagged, PER SESSION. sqlite3 binding: Tuesday's 04:55Z ruling to gate 14, carried as ruling (m).
# Full verifies UNBELTED: Tuesday's 08:19Z answer to gate 14 (fleet/briefs_staged/2026-10-05_qa_b14_belt_ANSWER.md), carried as ruling (n) with its 4 conditions.
# This gate is FINDINGS-ONLY: it NEVER merges (outside its own scratch clones), NEVER pushes, NEVER opens/comments/approves/updates a PR, never
# dismisses an alert (C-190 is the merge author's route); no fix, no deploy, nothing to Partner Center/demo/prod, no az, no docker, NO npm registry.
#
# PATTERN: launch_qa_nexusai_gate_batch15.sh (prompt EMBEDDED, --check mode, pin guards, THE MODEL RULE, floor, H-rules, the LIVE negative-control seat
# derivation 38R naming the coordinator pane 'tuesday', route-line and stamp guards last). CHANGES, each deliberate:
#   - ONE member; no ADDENDUM SLOT (guard 89 dropped); no image or browser leg (tier 2).
#   - 93: RD-618 (b1)'s premises at source — the old/new cap line, the unchanged condition, R8's asserts, the cap/slice/RATE, the budget's absence.
#   - 95: the intake log census premise (6 logger calls in the route region) and the RD-735 cross (NOTE: its merge-tree conflicts in the server entry point).
#   - 38R: gates 14 AND 15 added as negative controls if their panes are live (two live peer gates).
#   - the PR exists (#47): the launcher does NOT call gh (--check stays git-only); the gate reads CodeQL itself (row m8).
#
# Identity: exports NexusAI's OWN az/gh dirs (az unused, gh READ-ONLY for §8/m8); CLAUDE_CONFIG_DIR pinned to Tuesday's store.
# --check is READ-ONLY in NexusAI: git read verbs (cat-file, log, merge-base, diff, show, rev-parse, ls-remote, grep, rev-list, ls-tree) plus the
# three-argument merge-tree (stdout only); python/shasum over `git show` output; grep, ls, ps, tmux, test -e. It writes nothing anywhere and starts no claude.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate_batch16.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..99 a guard refused
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
STAGED="$TUE/2_Project_Files/fleet/briefs_staged"
BRIEFS="$TUE/2_Project_Files/fleet/qa-agent/briefs"
BRIEF="$BRIEFS/2026-10-05_nexusai-gate-batch16.md"
BRIEF15="$BRIEFS/2026-10-05_nexusai-gate-batch15.md"
READY="$BRIEFS/2026-10-05_nexusai-rd618-b1-READY-mail.txt"
RULING="$STAGED/2026-10-05_nexusai_MN_rd618_b1_turn.md"
CQ_GO="$STAGED/2026-10-05_nexusai_M_rd618_codeql_GO.md"
LINES_ANS="$STAGED/2026-10-05_nexusai_M_rd735_lines_ANSWER.md"
BELT_ANS="$STAGED/2026-10-05_qa_b14_belt_ANSWER.md"
SQLITE_RULING="$STAGED/2026-10-05_qa_b14_sqlite3_ANSWER.md"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
NX='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI'
REPO="$NX/2_Project_Files"
EV_M="$NX/session-tools/s86m"
LOCKQ="$NX/session-tools/locks/queue-jest"
CLAR="$NX/1_Project_Definition/CLARIFICATIONS.md"
C133="$NX/session-tools/s78g/c133-accounting.py"
C133_SHA='6f938bfcf2557d9f986894734e4b79390dfb90fbc7c62d63b989fbe58f6f972f'
RPTS="$QA_DIR/projects/nexusai/reports"
B13_DIR="$RPTS/2026-10-04-gate-batch13"
B13_INST="$B13_DIR/evidence/inst"
B12_REPORT="$RPTS/2026-09-30-gate-batch12/report.md"
B9_REPORT="$RPTS/2026-09-29-gate-batch9/report.md"
PREV_FLOORLIB="$B13_INST/qa-floorlib13.sh"
G7R1_FLOOR="$RPTS/2026-09-22-gate7-rd645/evidence/qa-floorcount.py"
REPORT="$RPTS/2026-10-05-gate-batch16/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"
ROUTE_NAME='QA/NexusAI-batch16'
NPM_CACHE="${HOME}/.npm/_cacache"
PREBUILD="${HOME}/.npm/_prebuilds/0068db-sqlite3-v5.1.7-napi-v6-darwin-arm64.tar.gz"
PREBUILD_SHA='84a34404b12ff212adbca70eff76c2e4dd83b91245eed0b4569438f928567afc'

MAIN_SHA='e91ff4e7419bfe76880d23b19d1c17dbcd395626'      # origin main at drafting (21:57:11 AEDT; RD-314)
M_BASE='b7bb1e964173f0f91ea0f401794836f5f90bb057'        # the member's merge-base with main (RD-693's main)
M1904='1904765007e9447ac6c980f9840c0689a02abe6c'         # RD-618's original base
BRANCH='rd-618-csp-intake-residue-s86m'
HEAD_SHA="${QA_HEAD_OVERRIDE:-953a0e67f3c7240e53b7f97ab009b2caaab5f246}"
H_FIX='a1d484d13507af76509dfb8bc6d6c70730903131'          # THIS ROUND (pre-counts)
H_CQ='fd01298b9c6823b4c457fb6711f566eeacc20607'           # test-only CodeQL fix A (the red-at-parent's server entry point)
H_CNT='baf3f6ede5b45145ea1d0be3d170e0b7db0966dd'          # counts after the forward merge
H_MRG='db57ec1334116d9f4afb0d834cd035d56f10be81'          # merge of 874c4f5 + b7bb1e9
R2='874c4f503d0f37a032014e562972b17e903e1072'             # RD-618 round 2 (batch 9's head)
C735_BRANCH='rd-735-csp-intake-residue-r3-s86m'
C735='7e2cc9f7d0f777d2689f97f547f7d11b4f2b9078'           # RD-735 r2 (gate 15's SLOT) — context only, NOT a member

COUNTS_FILE='scripts/verify-expected-counts.json'
PKG='package.json'
LOCK='package-lock.json'
SRV='backend/server.js'
CSPR='backend/services/cspReport.js'
R618='__tests__/rd618-csp-intake-residue.test.js'
R314='__tests__/rd314-law-window-after-source.test.js'
ALA='backend/azureLogAnalytics.js'
R735='__tests__/rd735-csp-intake-residue-r3.test.js'
HARN='__tests__/helpers/rd395-server-harness.js'
TS='__tests__/helpers/test-server.js'
TSH='__tests__/test-server-helper.test.js'
R495='__tests__/rd495-admin-routes-behind-the-gate.test.js'
R607='__tests__/rd607-redis-limiters-keep-their-own-counts.test.js'
R465='__tests__/rd465-first-run-open-window.test.js'
R549='__tests__/rd549-ai-config-inert-until-confirmed.test.js'
DKF='Dockerfile'
DIG='.dockerignore'

LOCK_M_BLOB='e9063d44757007324b8c55fa58c03c03dfe552ae'
LOCK_OLD_BLOB='906476350431e2ecb3c21070a25c64b1702c1aa8'
PKG_BLOB='cdb1168783a92179afe20be67b37976203b904f8'
SRV_M_BLOB='0d7e387558f06dba0e94a8bbf8f53382fd7ef5d2'       # b7bb1e9 and e91ff4e
SRV_CQ_BLOB='a93893022ffabc9c7a999014f086c1eac5f8f407'      # fd01298 (the red-at-parent)
SRV_H_BLOB='2684acda2190ac2578008f8055a131fe6cd9a7f1'       # a1d484d and the head
SRV_R2_BLOB='e076121f4214dd6930697d9ab98bb6252b367294'      # 874c4f5
CSPR_H_BLOB='4b38e90138fe466586b7badb6266c28c4a1500b9'      # 874c4f5, fd01298, head
CSPR_M_BLOB='f102d26b01e77f6ac838042b18cc9ac120c41032'      # b7bb1e9, e91ff4e
R618_H_BLOB='74c1c514a6cd88da3867d3405706db0d995342fe'
R618_CQ_BLOB='d2f12536bbdbbfcdd4f0f7c560a50cfc98be3726'
R618_R2_BLOB='8bbfcc713615a7afee3da9e78f04b031063f5f32'
HARN_BLOB='2453a3fa7840de9d71267169b02ecea4a37015b6'
TS_BLOB='cff1e54'                                          # short ids: prefix guard
TSH_BLOB='f612fb4815aaa358795acc977d59a0a9cba09670'
R495_BLOB='9ffe71a215c55eb15a641e93b7114922675f29b0'
R607_BLOB='9c3a879ab613e9ea280878b911c52bbb9e7ae85a'
R465_BLOB='f16b811'
R549_BLOB='4a35642'
DKF_BLOB='12aab55'
DIG_BLOB='3e45ec5'

OWN_EXPECTED_FILES="$SRV
$R618
$COUNTS_FILE"
BASE_EXPECTED_FILES="$SRV
$CSPR
$R618
$COUNTS_FILE"
OLD_LINE='logger.warn(`🛡️  CSP report: kept ${entries.length} of ${offered} reports in one request (per-request cap); the rest dropped`);'
NEW_LINE='logger.warn(`🛡️  CSP report: per-request cap (${CSP_REPORT_MAX_ENTRIES_PER_REQUEST}) applied; extra reports dropped`);'
COND_LINE='if (offered > entries.length) {'
OFFERED_LINE="const offered = Array.isArray(req.body) ? req.body.filter((r) => r && r.type === 'csp-violation').length : 0;"
NEG_SEATS=''   # 38R: DERIVED at launch from the live cockpit panes — never stamped by hand

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 16'
QUESTION_SUBJ='[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>'
STATUS_SUBJ='[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch'
PARK_LINE='PARKED: flagged — awaiting the Opus 4.8 switch'
ANSWER_PREFIX='[Tuesday -> QA/NexusAI-batch16] ANSWER'
NOTTESTED_LINE="Not tested by this gate: Linux or CI Build at the branch head (PR #47 conflicts with main, so no pull_request Build ran there), CodeQL beyond reading PR #47's own analyses (the gate runs none), a real Docker image build (tier 2: no image leg), the demo (behind RD-76 SSO), any deployed environment, any browser (the cells and the local runs POST report bodies directly; a real browser's Reporting API delivery is not driven), a real Key Vault, a real Entra tenant, real Azure, Partner Center, docker, a real Redis, the npm registry (node_modules from an offline cache copy with install scripts skipped; sqlite3's binding from its cached prebuild), and Windows."
SAFE_PRINTER='if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET (length ${#SESSION_SECRET})"; else echo "SESSION_SECRET UNSET"; fi'

g() { git --no-optional-locks -C "$REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }
counts_at() { g show "${1}:${COUNTS_FILE}" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
blob() { g rev-parse --verify -q "${1}:${2}" 2>/dev/null; }
sblob() { local b; b="$(blob "$1" "$2")"; printf '%s' "${b:0:7}"; }
cnt() { g show "${1}:${2}" 2>/dev/null | grep -cF -- "$3"; }
ntests() { g ls-tree -r -z --name-only "$1" -- __tests__ 2>/dev/null | tr '\0' '\n' | grep -c .; }
# C-192: ls-remote retried up to 5 x ~10 s on a publickey denial; sets LSR_OUT on success (no subshell, so LSR_ATTEMPTS counts), returns 1 (UNKNOWN) otherwise.
LSR_ATTEMPTS=0
LSR_OUT=''
lsr() { local out rc i
  LSR_OUT=''
  for i in 1 2 3 4 5; do
    LSR_ATTEMPTS=$((LSR_ATTEMPTS + 1))
    out="$(g ls-remote origin "$@" 2>&1)"; rc=$?
    if [ "$rc" = "0" ]; then LSR_OUT="$out"; return 0; fi
    printf '%s\n' "$out" | grep -qi 'publickey' || { printf '%s\n' "$out" >&2; return 1; }
    [ "$i" = "5" ] || sleep 10
  done
  printf '%s\n' "$out" >&2; return 1; }
# read-only merge prediction: the three-argument merge-tree writes NO objects; prints the paths carrying conflict markers.
conflicts() { local b; b="$(g merge-base "$1" "$2" 2>/dev/null)" || return 1
  g merge-tree "$b" "$1" "$2" 2>/dev/null | awk '/^  (base|our|their) /{f=$4} /^\+<<<<<<</{c[f]=1} END{for(k in c) print k}' | sort; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE gate on Datasec/NexusAI, "batch 16", with ONE member, one verdict and ONE report. It is a FRESH gate. The member: RD-618 (b1), a re-gate at TIER 2 (through code), round 1 of 2 for this class (Tuesday's RULING: if the class reaches a third objection, STOP). NexusAI-M reshaped ONE operator-facing log line on the anonymous CSP report intake in the shipped server entry point: the per-request cap line used to interpolate the request's own counts ("kept N of M reports in one request (per-request cap)") and CodeQL alert #255 (js/log-injection, rule severity error) blocked PR #47 under the ruleset's alerts_threshold errors; the line is now fixed text plus the server-side cap constant ("CSP report: per-request cap (10) applied; extra reports dropped"), and a new cell R8 guards it. The verdict — GO, GO WITH FINDINGS or NO GO — is about the branch head AND about the merged tree. FINDINGS-ONLY: you NEVER merge anything the fleet can see, NEVER push, and NEVER open, comment on, approve, update or merge a pull request, and never dismiss an alert; no fixes, no deploys, nothing to Partner Center, the demo or production, no az, no docker, no image build, no npm registry.

READ YOUR COMMISSION FIRST, whole: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-05_nexusai-gate-batch16.md
It opens with TUESDAY'S RULINGS (a) to (n) and THE MODEL RULE: apply them, do not re-rule them. Then the charter it names, then the READY mail it names (read it WHOLE, it carries its own PRIOR WORK section), then Tuesday's (b1) RULING and its ancestors the brief names, then gate 15's stamped brief (the base of your instrument rules H-1 to H-33; gate 15 is LIVE: read only, never its trees, never its report dir), the batch-9 report (RD-618's prior round: verdict, findings A-F1r, A-F2r, A-F3c and the A-N2 Polish your row m6 re-measures) and gate 12's report (RD-618 rode its merge build as MTa; its RESUME METHOD NOTE). Every builder statement is a CLAIM — RELAYED, never evidence. The brief's LEGITIMATE SHAPES table (section 2a) is required measurements, row by row, base and head in the same window. Its WRONG OR UNVERIFIED list corrects two premises of the ruling's own text (no rd618 cell asserted the old text, so the commissioned "cell still RED when the cap line is not logged" is R8; the entry budget is not on this branch): read it before rows m2 and m7.

THE MODEL RULE (Kam, live board 2026-09-30 09:07, card (b)): QA gates may switch to Opus 4.8 when flagged by Opus 5.5's safeguards, PER SESSION. You start on Opus 5.5. You run the FULL rows, including the planted ones (forged CSP report bodies, 150-report arrays, empty-body reports, log-line mutants, a charset-header probe) — every one is an authorised, findings-only measurement in your own trees against your own loopback servers on 127.0.0.1. If one of your responses is stopped by the safeguards: that step is NOT RUN (never re-worded to slip past); write ONE line to evidence/classifier-stops.txt; let any running jest step finish and let the hold exit so you never sit holding the jest lock (H-28); mail tuesday-agent@agentmail.to with the subject exactly "[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch"; then end your turn with the line "PARKED: flagged — awaiting the Opus 4.8 switch" and wait. Tuesday switches THIS pane's model and taps you by mail. You never answer the model dialog yourself, and nobody ever chooses "Switch automatically". After the switch, resume at the stopped row. The report states which rows ran on which model, with the switch time, and quotes classifier-stops.txt whole.

THE TARGET. RD-618 (b1): rd-618-csp-intake-residue-s86m at 953a0e67f3c7240e53b7f97ab009b2caaab5f246. Its chain on top of the batch-9-gated 874c4f503d0f37a032014e562972b17e903e1072: db57ec1334116d9f4afb0d834cd035d56f10be81 (forward merge of main b7bb1e964173f0f91ea0f401794836f5f90bb057) -> baf3f6ede5b45145ea1d0be3d170e0b7db0966dd (counts) -> fd01298b9c6823b4c457fb6711f566eeacc20607 (test-only CodeQL fix A, Tuesday's GO, never gated: row m10) -> a1d484d13507af76509dfb8bc6d6c70730903131 (THIS ROUND) -> 953a0e6 (counts 4266/260). 874c4f5 is NOT on main, so merging the head brings RD-618's rounds 1 and 2 with it. PR #47 is OPEN (mergeable CONFLICTING at drafting: main moved, the counts file). The cap line's firing condition (offered > entries.length) is UNCHANGED; offered counts every csp-violation report while entries drops the empty ones, so batch 9's A-N2 shape (5 reports, 3 empty) may now log "per-request cap (10) applied" when nothing was capped (row m6). R8's "no request-derived count" arm matches only "of 150" and "150 reports" (row m3: your own mutants find its survivors). A Tuesday ADDENDUM mailed from tuesday-agent@ during the gate supersedes the closing lines.

MAIN MAY MOVE BEFORE AND DURING YOUR GATE (ruling b). Take M0 = origin main AT YOUR OWN START by git ls-remote, say so, and RE-BASE EVERY PREDICTION on it: counts (MT1 = M0 + RD-618 (b1) 4276/261, predicted at M0 = e91ff4e7419bfe76880d23b19d1c17dbcd395626, where RD-314 landed; its rd314 file is a C-68 member and absent from the head: stale-parent, y4), the tests census (304 at MT1), new ids 14, missing 0. Gates 14 (QA/NexusAI-batch14) and 15 (QA/NexusAI-batch15) are LIVE and their members (RD-719, RD-424, RD-735 among them) may land on main before or during your gate: if any is in your M0, re-derive every C-68 set on it — and if RD-735 7e2cc9f is in your M0, your merge CONFLICTS in the server entry point: that is a STOP for the merged tree (y5), named and mailed. The member is merged forward onto M0 in YOUR OWN trees, never in a builder's worktree. Never re-base mid-gate; at your END measure the head onto the main you find by merge-tree. GitHub SSH intermittently denies auth (C-192): retry every ls-remote up to 5 times about 10 s apart; a FAILED ls-remote is UNKNOWN, never a value.

C-190 AND ITS 2026-10-05 ADDENDUM — BOTH THRESHOLDS BLOCK: every merge to main goes through a pull request that adds no new high-or-higher CodeQL alert in changed code (test code included) AND no new alert whose RULE severity is error, whatever its security severity (js/log-injection counts, even for a number derived from the request). PR #47 EXISTS: row m8 READS, with gh READ ONLY (repo datasecau/Reporting_Dashboard_Au, NexusAI's own GH_CONFIG_DIR), whether PR #47's newest CodeQL analysis at 953a0e6 still reports #255 or any NEW alert either threshold blocks — read each alert's INSTANCE on refs/pull/47/head (state, commit_sha), never the alert-level state (it reads null); read the ruleset's two thresholds back; read the PR's mergeable state and whether a pull_request Build ran at the head. If PR #47's newest analysis is not at the head you pinned, say so. The gate runs no CodeQL. C-185 on M0 (ruling h): the known-failing set is {rd549 O4 only when envReached alone differs}; ANY rd465 O-1 failure is a STOP, named and mailed; a local failure of O4 is named and classified, never waved.

THE ROWS (brief section 2a), POSITIVE CONTROL FIRST. m0 RED-AT-PARENT first: the head's whole rd618 file (14 ids) against fd01298's server entry point (blob a938930, only that file restored in your head tree): R8 red, quote the received object (predicted capLine false AND requestCountInLog true), the other 13 green. m1 the head clean by name. m2 THE COMMISSIONED MUTANT re-derived independently — the cap line NOT logged (M1) turns R8 red, and name every OTHER red (predicted none: R8 is the cap line's only guard); M2 (the condition forced true) turns R8 red; each arm runs the whole file, not -t R8. m3 R8's narrow arm: your own mutants M-shape, M-dropped, M-second, M-kept (predicted survivors, C-40) and M-cap11; then a census of every number in the capped request's log slice (no 150, no 140 at the head). m4 THE INTAKE LOG CENSUS: every logger call reachable from the CSP intake route and its error handler (six at the head; cspReport.js none), POSITIVE CONTROL the same census on fd01298's blob classifying the OLD interpolated line request-derived, NEGATIVE CONTROL a fixed-text line classifying clean; classify each; then DRIVE each request-derived candidate (the sanitised entry object logged as an argument; the e.message interpolation in the catch; the type-and-status refusal line with batch 7's charset shape, case-insensitive) on a REAL local server of the head. m5 THE OPERATOR INFORMATION REMOVED: a REAL local run of fd01298 and of the head side by side with 150, 12, 11, 10 and 5 non-empty reports — quote old and new lines and the violation-line counts; name what an operator loses (the kept/offered numbers; the offered count is gone). m6 A-N2 under the new text (5 reports with 3 empty; 12 with 3 empty; a non-array body). m7 CAP AND LIMITER UNCHANGED, cells by name plus a REAL LOCAL INTAKE RUN (150 -> 10 violation lines and one cap line; 5 -> no cap line; 61 requests -> the 61st answered 429); the entry budget ABSENT at fd01298 and the head (it is RD-735's; positive control present at 7e2cc9f). m8 the CodeQL read. m9 PRIOR WORK. m10 fd01298's shortened needles and Tuesday's GO condition (the violation entry not logged turns R1 AND R4 red). m11 the RD-735 cross (gate 15's member; its rd735 R9 asserts the old text and its merge-tree with this head conflicts in the server entry point) — named, not gated. m12 the shipped blobs changed (READ). Cross cells y1-y5 on MT1. Every row that boots a server names "sqlite3 binding: cached prebuild, offline" once and is captioned "local run of <sha>, open mode — NOT the demo".

PRIOR WORK: verify the READY's PRIOR WORK section claim by claim (C-49) — VERIFIED, FALSE or UNVERIFIED with its evidence class — including its "(or empties beyond the cap)" wording against row m6.

THE MERGED TREE — part of the verdict (brief section 7). In YOUR OWN scratch clone (git clone --shared --no-checkout into your own project dir; origin removed; local user config; gc.auto 0; hooks off; merges and commits in the clone ONLY): M0, then merge --no-ff 953a0e6 (MT1). Re-measure the pair by merge-tree --write-tree in a SCRATCH object dir first (GIT_OBJECT_DIRECTORY your own, NexusAI's objects only as GIT_ALTERNATE_OBJECT_DIRECTORIES) — the drafter's READ-ONLY three-argument merge-tree: the counts file only. Predict before merging; anything other than the counts file conflicting STOPS (C-57). C-104: resolve and stage before any census or run. Counts by REGENERATION once on MT1 on node_modules proven for M0's lock: predicted 4276/261, re-based on YOUR M0; the measurement decides. A second clone in the OTHER direction (the head, then merge M0), root trees identical apart from the counts file. The id-superset control LIKE WITH LIKE, all K1, both controls (a planted missing id STOPS; a superset passes): predicted missing 0; any missing id is a STOP. The C-68 set by name, in holds per H-28: rd618, rd495, rd607, every rd395-server-harness requirer, every services/cspReport requirer, test-server-helper and rd314. C-89 on your clone. Count the NexusAI object files before and after and account for any delta by full-date mtime. Nothing leaves your clone; never push.

NODE_MODULES WITHOUT THE REGISTRY (ruling m, H-31). The member changes neither the lock nor package.json, so there is NO npm registry exception. ONE lock is in play (e9063d4) for the head, fd01298 and every merged tree. ONCE: npm ci --offline --ignore-scripts --no-audit --no-fund with --cache pointing at an APFS clone of the local npm cache under your own mktemp dir, in your own tree, under a deadline; an ENOTCACHED is NOT RUN (name it, mail a QUESTION) — never go online, never npm install. sqlite3's binding: Tuesday ruled (04:55Z, to gate 14, carried here) that the offline unpack of sqlite3's CACHED prebuild from an APFS clone of ~/.npm/_prebuilds, inside the strict belt, IS PART OF H-31 — under three conditions: (1) the sha256 of the cached tarball and of the unpacked node_sqlite3.node in the tree; (2) say that CI builds the binding by its own install step (Linux, a different binary), so a local green on this binding is not evidence about CI's; (3) every row that boots the server or opens the DB names the binding source once ("sqlite3 binding: cached prebuild, offline"). Every other tree clones node_modules from your proven tree; never from gate 14's or gate 15's (live) or gates 12/13's trees.

FULL VERIFY of the head and of MT1 through the lock, UNBELTED by Tuesday's 2026-10-05 answer to gate 14 (ruling n: every other jest run stays belted — cells, mutants, C-68 unions, drivers and servers), with its four conditions: the test-server-helper control pair (belted red, quote it; unbelted green; same tree, same window); any belted verify kept as evidence; each unbelted verify says "verify UNBELTED by Tuesday's 2026-10-05 answer; matches CI"; any other failure read on its merits, never blamed on the belt without a belted/unbelted pair. SESSION_SECRET UNSET, npm run verify -- --maxWorkers=2 --forceExit (prove the flag reached jest or say it did not), K1 trees only. Predicted 953a0e6 4266/260, MT1 4276/261. The builder's verify ran on the pre-counts commit a1d484d with --update-counts and without --forceExit; yours decides. Every failure by NAME. Re-run-until-green is not an acceptance gate. A RED ARM COUNTS ONLY IF THE MUTANT STILL PARSES AND LANDED: node --check every mutated JS file and quote the exit code, assert each anchor matched once and the exact mutated text is present; a red from a mutant that does not parse, or a green from one that never landed, is a VOID arm.

THE INSTRUMENT RULES H-1 TO H-33 (brief section 3a). H-1: the ONLY SESSION_SECRET printer is the one the brief quotes; self-test it with a throwaway, scan every hold's logs for it, and let the scan's control plant a DIFFERENT marker. H-2: seed BEFORE boot; read logs raw. H-3: a LANDING CONTROL for every plant, mutant or header probe. H-4: the HEARTBEAT is a separate child of the hold wrapper, aborted if absent 90 s after the grant, max gap per hold reported (at most 120 s). H-9: byte plants by Buffer, checked with xxd. H-15: preloads with -r in argv; no exception this gate. H-20: EVERY jest invocation carries --forceExit AND a per-step hard deadline (qa-to.sh). H-21: every file you mutate is restored by a trap on EXIT (also INT and TERM) installed BEFORE the first mutation, hash-compared to its pinned blob after every hold. H-22: never nest sandbox-exec (it exits 71). H-24: jest array options after the test paths. H-25: the comment-aware compare with its IGNORED control. H-26: C-192 retries. H-27: THE MODEL RULE. H-28 (gate 12's wrap, gate 13's stamped reading): ONE focused hold at a time, at most about 40 minutes of planned jest, every part file written and bash -n checked before the hold is filed; you stay in the FOREGROUND for the whole hold — a hold that must outlive one foreground tool call runs as a TRACKED child of your session (never nohup) with its own timeout at the 2-hour maximum while you poll its output, because backgrounded commands die at 2 h and lock waits have run 5600 to 8995 s; each hold carries a wait deadline and re-files cleanly under the SAME tag if not granted. H-29: gates 14 and 15 are live; their evidence is method only. H-31: offline node_modules and the cached sqlite3 prebuild. H-32: no image leg, no browser leg; every local server is captioned as a local run — NOT the demo. H-33: plants, servers and children counted and reaped or quarantined, never rm. The rest as the brief states them.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT (fresh mktemp dirs under projects/nexusai/qa-trees/batch16.*), status-checked before use. Each tree is EXCLUSIVE to this gate and to one purpose; gates 14's and 15's trees and report dirs are LIVE PEER gates' — never touch them; copy instruments BY COPY from gate 13's evidence/inst (its HOLD13.sh hard-codes its own evidence dir and its qa-floorlib13.sh carries stale ROOT and NEG defaults: re-point and correct your copies). In the NexusAI repo use ONLY read verbs (show, diff, log, ls-tree, cat-file, grep, ls-remote, rev-parse, merge-base, rev-list; count-objects for the object accounting); NEVER fetch, pull, push, checkout, worktree, commit, stash, gc, merge, and merge-tree --write-tree ONLY with your own scratch object directory; never work in its 2_Project_Files checkout or any builder worktree. Never write into the builders' session-tools: copy, then hash at start and end; never run their hold or mutate scripts. Findings-only: never push, no commits outside your clones, no tickets, no PRs, no edits in NexusAI. No Azure (no az at all), no demo, no docker, no image build, no Partner Center, no ARM deployment, no npm registry. No mail to any human. Never rm: quarantine.

FLOOR DISCIPLINE — section 9 of the brief exactly. MERGES GO FIRST: the jest lock (session-tools/nexusai-lock.sh, queue session-tools/locks/queue-jest) is shared with gates 14 and 15 (tags qa-b14- and qa-b15-) — PEER gates: FIFO, never touched — and the four builder seats; merges go one at a time in the C-186 ADDENDUM's turns. Do ALL lock-free work first (pins, reads, merge-trees in scratch objects, the offline npm ci, the READ and local-server rows, census greps, the CodeQL read); then file your holds tagged qa-b16-, one at a time; if a MERGE ticket (a tag containing "merge") is queued ahead of you, wait behind it; if one files behind you BEFORE your hold is granted, re-file your ticket behind it (stop your OWN unstarted waiter by pid from your own ancestry, then re-queue with --after that merge ticket's tag, C-141 ADDENDUM 4) under your UNCHANGED tag (C-141 ADDENDUM 5: builders yield once per gate TAG); once granted, carry on. QUEUE, NEVER TAKE OVER: never signal, move or edit another seat's process, lock or ticket. Count foreign servers the C-125 way anchored on YOUR OWN claude pid, with the negative-control seats the launcher derived (listed at the end of this prompt) classifying foreign in the same run; your own local-server rows' servers must classify OURS; record the foreign count beside every result; count every child you start and prove none left; a hold with no live negative control aborts. A zero is reportable only beside a control that fired in the same window. DEADLINE AND HEARTBEAT: every npm call, server boot, request, node driver and jest run has a per-step DEADLINE, every child is killed in a finally by pid from your own ancestry (C-174, never by pattern), a HEARTBEAT line at least every 2 minutes during a hold, and a step with no heartbeat for 5 minutes is aborted and reported.

RE-PIN at start, mid and end: the member branch and main (and RD-735's branch, context) — three timestamped readings with the branch name and attempt count beside each sha. A TICKET head that disagrees with the brief is a FINDING and a reason to stop, never a typo to fix (NexusAI-M's forward merge onto the new main would move it). Main MAY move: call main at your start M0 and say so; it must be e91ff4e or a descendant; if main moves again, your verdict names M0 and says what moved (C-68); never re-base mid-gate.

QUESTIONS: your routing name is QA/NexusAI-batch16. If you must ask, mail tuesday-agent@agentmail.to with subject "[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>" and PROCEED ON THE SAFEST READING without waiting (the one exception is a safeguards stop, which PARKS you under THE MODEL RULE); Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/NexusAI-batch16] ANSWER". Approval-class items are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your ONE report to: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-10-05-gate-batch16/report.md

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with the subject exactly:
[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 16
Lead the body with the one line the brief's section 11 gives (RD-618 (b1) @ 953a0e6 with R8 at fd01298's server entry point and the other 13, the M1 and M2 arms and any other reds, m3's survivors, the intake log census, the operator information removed, A-N2 under the new text, the cap and limiter, the budget absent, the CodeQL read on PR #47 and the PR's mergeable state), then one line naming M0, the merged counts you measured, the C-57 result, any combined blob, which rows ran on Opus 4.8 (or none), and "CodeQL READ on PR #47 (not run by the gate)" with the PR Build state at the head. Never wednesday-agent@. You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no 4_Credentials directory of its own. Never put the key, a token, a session value or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice — the only turn you end while waiting is the PARKED line of THE MODEL RULE.

Rule 2 stands: what you did NOT test is first-class output — a NOT TESTED section carrying the builder's stated limits as the brief quotes them, every declared limit L-M1 to L-M6 and L-Y1 discharged with a measurement or left standing and named (C-112), Prior work checked (C-49), and every action recommendation labelled MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. C-190 with its ADDENDUM, C-185 with its ADDENDA, C-98, C-129 and C-192 are the clarifications this gate leans on; C-02, C-49, C-57, C-68, C-89, C-102, C-104, C-112, C-115, C-125, C-141 with ADDENDUM 5, C-174 and C-186 are carried. That section must carry this line verbatim:
Not tested by this gate: Linux or CI Build at the branch head (PR #47 conflicts with main, so no pull_request Build ran there), CodeQL beyond reading PR #47's own analyses (the gate runs none), a real Docker image build (tier 2: no image leg), the demo (behind RD-76 SSO), any deployed environment, any browser (the cells and the local runs POST report bodies directly; a real browser's Reporting API delivery is not driven), a real Key Vault, a real Entra tenant, real Azure, Partner Center, docker, a real Redis, the npm registry (node_modules from an offline cache copy with install scripts skipped; sqlite3's binding from its cached prebuild), and Windows.
PROMPT_EOF

# ---------------------------------------------------------------- GUARDS
[ -d "$QA_DIR" ]  || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]   || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -n "$PROMPT" ]  || { echo "embedded prompt is empty" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }
[[ "$HEAD_SHA" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: head '$HEAD_SHA' is not a full 40-hex sha" >&2; exit 9; }

# 6 — every pinned sha is a commit in the object store (this launcher never fetches).
for S in "$MAIN_SHA" "$M_BASE" "$M1904" "$HEAD_SHA" "$H_FIX" "$H_CQ" "$H_CNT" "$H_MRG" "$R2" "$C735"; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 7 — merge-base: the head's base with main is b7bb1e9; b7bb1e9 is on main; RD-618's own rounds are NOT on main.
g merge-base --is-ancestor "$M_BASE" "$MAIN_SHA" 2>/dev/null || { echo "REFUSING: b7bb1e9 is not an ancestor of e91ff4e — re-brief" >&2; exit 7; }
[ "$(g merge-base "$HEAD_SHA" "$MAIN_SHA" 2>/dev/null)" = "$M_BASE" ] || { echo "REFUSING: merge-base(RD-618 head, e91ff4e) is not b7bb1e9 — re-brief" >&2; exit 7; }
if g merge-base --is-ancestor "$R2" "$MAIN_SHA" 2>/dev/null; then echo "REFUSING: RD-618 874c4f5 is already on e91ff4e — the brief's premise (it rides in with the head) is stale" >&2; exit 7; fi

# 8 — chain exact (first parents; one merge).
[ "$(g rev-parse "${HEAD_SHA}^1" 2>/dev/null)" = "$H_FIX" ] && [ -z "$(g rev-parse --verify -q "${HEAD_SHA}^2" 2>/dev/null)" ] \
  && [ "$(g rev-parse "${H_FIX}^1" 2>/dev/null)" = "$H_CQ" ] && [ -z "$(g rev-parse --verify -q "${H_FIX}^2" 2>/dev/null)" ] \
  && [ "$(g rev-parse "${H_CQ}^1" 2>/dev/null)" = "$H_CNT" ] && [ -z "$(g rev-parse --verify -q "${H_CQ}^2" 2>/dev/null)" ] \
  && [ "$(g rev-parse "${H_CNT}^1" 2>/dev/null)" = "$H_MRG" ] && [ -z "$(g rev-parse --verify -q "${H_CNT}^2" 2>/dev/null)" ] \
  && [ "$(g rev-parse "${H_MRG}^1" 2>/dev/null)" = "$R2" ] && [ "$(g rev-parse "${H_MRG}^2" 2>/dev/null)" = "$M_BASE" ] \
  || { echo "REFUSING: RD-618 is not 953a0e6 -> a1d484d -> fd01298 -> baf3f6e -> db57ec1 (merge of 874c4f5 + b7bb1e9)" >&2; exit 8; }
g merge-base --is-ancestor "$M1904" "$R2" 2>/dev/null || { echo "REFUSING: RD-618 874c4f5 does not descend from 1904765" >&2; exit 8; }

# 18 — RE-PIN NOW by ls-remote (C-192 retries): the member branch exactly the pin (REFUSE); main and RD-735's branch read.
lsr refs/heads/main "refs/heads/$BRANCH" "refs/heads/$C735_BRANCH" || {
  echo "REFUSING: git ls-remote origin failed after $LSR_ATTEMPTS attempt(s) — UNKNOWN, not a value (C-192); relaunch later" >&2; exit 18; }
LSR_ALL="$LSR_OUT"
printf '%s\n' "$LSR_ALL" | grep -q "^${HEAD_SHA}[[:space:]]refs/heads/${BRANCH}\$" || {
  echo "REFUSING: origin refs/heads/$BRANCH is not $HEAD_SHA — moved or never pushed; re-brief. ls-remote said:" >&2; printf '%s\n' "${LSR_ALL:-<nothing>}" >&2; exit 18; }
ref_now() { printf '%s\n' "$LSR_ALL" | awk -v r="refs/heads/$1" '$2==r{print $1}'; }
C735_NOW="$(ref_now "$C735_BRANCH")"
[ "$C735_NOW" = "$C735" ] || echo "NOTE: origin $C735_BRANCH is '${C735_NOW:-absent}', not 7e2cc9f (gate 15's SLOT) — m11's context moved; the gate re-reads it" >&2
# 18b — main MAY move (ruling b). It must be e91ff4e or a descendant IN THE OBJECT STORE; the head already on it REFUSES; a member path moved REFUSES.
M_ORIGIN="$(ref_now main)"
[[ "$M_ORIGIN" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: could not read origin main by ls-remote (got '${M_ORIGIN:-nothing}') — UNKNOWN (C-192)" >&2; exit 18; }
[ "$(g cat-file -t "$M_ORIGIN" 2>&1)" = "commit" ] || { echo "REFUSING: origin main $M_ORIGIN is not in the object store — this launcher never fetches; wait for a seat's fetch or re-brief" >&2; exit 18; }
g merge-base --is-ancestor "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null || { echo "REFUSING: origin main $M_ORIGIN does not descend from e91ff4e — main was rewritten; re-brief" >&2; exit 18; }
if g merge-base --is-ancestor "$HEAD_SHA" "$M_ORIGIN" 2>/dev/null; then echo "REFUSING: ${HEAD_SHA:0:7} is already an ancestor of origin main ${M_ORIGIN:0:7} — the member merged before its gate; re-brief" >&2; exit 18; fi
MOVED="$(g diff --name-only "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null | sort -u)"
HIT="$(comm -12 <(printf '%s\n' "$SRV" "$CSPR" "$R618" "$LOCK" "$PKG" | sort -u) <(printf '%s\n' "$MOVED" | sed '/^$/d') | tr '\n' ' ')"
[ -z "$HIT" ] || { echo "REFUSING: main moved e91ff4e..${M_ORIGIN:0:7} and touched a member path: ${HIT}— a combined blob the brief does not predict; re-brief" >&2; exit 18; }
HITB="$(comm -12 <(printf '%s\n' "$HARN" "$TS" "$TSH" "$R495" "$R607" "$R465" "$R549" "$DKF" "$DIG" | sort -u) <(printf '%s\n' "$MOVED" | sed '/^$/d') | tr '\n' ' ')"
[ -z "$HITB" ] || echo "NOTE: main's movement touches ${HITB}— the C-68 sets run on M0's blobs (brief ruling b)" >&2
[ "$M_ORIGIN" = "$MAIN_SHA" ] || echo "NOTE: origin main is now ${M_ORIGIN:0:7} (moved from e91ff4e; gates 14/15's members may have landed) — the gate re-pins M0 itself and re-bases every prediction" >&2
if g merge-base --is-ancestor "$C735" "$M_ORIGIN" 2>/dev/null; then echo "NOTE: RD-735 7e2cc9f is ON origin main ${M_ORIGIN:0:7} — the head's merge onto main CONFLICTS in the server entry point (brief y5: a STOP for the merged tree); Tuesday decides before launch" >&2; fi
[ "$(sblob "$M_ORIGIN" "$TS")" = "$TS_BLOB" ] || echo "NOTE: origin main ${M_ORIGIN:0:7}'s test-server is not cff1e54 — RD-591 landed? H-23 applies whole" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — each delta is EXACTLY the commissioned file set; numstats as briefed; no lock/package change.
chk_delta() { local from="$1" to="$2" want="$3" label="$4" got
  got="$(g diff --name-only "$from" "$to" 2>/dev/null | sort)"
  [ "$got" = "$(sorted "$want")" ] || { echo "REFUSING: $label delta is not the commissioned set. Got:" >&2; printf '%s\n' "$got" >&2; exit 22; }; }
chk_delta "$H_CQ" "$HEAD_SHA" "$OWN_EXPECTED_FILES" "RD-618 (b1)'s own (fd01298..953a0e6)"
chk_delta "$M_BASE" "$HEAD_SHA" "$BASE_EXPECTED_FILES" "RD-618 over its base (b7bb1e9..953a0e6)"
chk_delta "$H_CQ" "$H_FIX" "$SRV
$R618" "the round's product commit (fd01298..a1d484d)"
chk_delta "$H_FIX" "$HEAD_SHA" "$COUNTS_FILE" "the counts commit (a1d484d..953a0e6)"
chk_delta "$H_CNT" "$H_CQ" "$R618" "fix A (baf3f6e..fd01298)"
ns() { g diff --numstat "$1" "$2" -- "$3" 2>/dev/null | cut -f1,2 | tr '\t' ' '; }
[ "$(ns "$H_CQ" "$HEAD_SHA" "$SRV")" = "5 2" ] && [ "$(ns "$H_CQ" "$HEAD_SHA" "$R618")" = "14 0" ] \
  && [ "$(ns "$M_BASE" "$HEAD_SHA" "$R618")" = "206 0" ] && [ "$(ns "$M_BASE" "$HEAD_SHA" "$SRV")" = "48 8" ] && [ "$(ns "$M_BASE" "$HEAD_SHA" "$CSPR")" = "62 6" ] \
  && [ "$(ns "$H_CNT" "$H_CQ" "$R618")" = "3 3" ] \
  || { echo "REFUSING: RD-618's numstats are not server entry point +5/-2 and rd618 +14 (own); rd618 +206, server +48/-8, cspReport +62/-6 (over b7bb1e9); fix A +3/-3" >&2; exit 22; }
[ "$(g diff -U0 "$H_CQ" "$HEAD_SHA" -- "$SRV" 2>/dev/null | grep -c '^@@')" = "2" ] || { echo "REFUSING: the round's server entry point diff is not exactly two hunks (the import line and the cap line)" >&2; exit 22; }
[ -z "$(g diff --name-only "$M_BASE" "$HEAD_SHA" -- "$LOCK" "$PKG" 2>/dev/null)" ] || { echo "REFUSING: the head changes package-lock.json/package.json over b7bb1e9 — ruling (m) assumed it does not; re-brief" >&2; exit 22; }

# 93 — RD-618 (b1)'s premises at source: the old and new cap line, the unchanged condition, R8, the cap/slice/RATE, the budget's absence.
[ "$(blob "$H_CQ" "$SRV")" = "$SRV_CQ_BLOB" ] && [ "$(blob "$H_FIX" "$SRV")" = "$SRV_H_BLOB" ] && [ "$(blob "$HEAD_SHA" "$SRV")" = "$SRV_H_BLOB" ] \
  && [ "$(blob "$M_BASE" "$SRV")" = "$SRV_M_BLOB" ] && [ "$(blob "$MAIN_SHA" "$SRV")" = "$SRV_M_BLOB" ] && [ "$(blob "$R2" "$SRV")" = "$SRV_R2_BLOB" ] \
  || { echo "REFUSING: the server entry point is not a938930 (fd01298) / 2684acd (a1d484d, head) / 0d7e387 (b7bb1e9, e91ff4e) / e076121 (874c4f5)" >&2; exit 93; }
for S in "$R2" "$H_CQ" "$HEAD_SHA"; do [ "$(blob "$S" "$CSPR")" = "$CSPR_H_BLOB" ] || { echo "REFUSING: cspReport.js at ${S:0:7} is not 4b38e90 (the round must not touch it)" >&2; exit 93; }; done
for S in "$M_BASE" "$MAIN_SHA"; do [ "$(blob "$S" "$CSPR")" = "$CSPR_M_BLOB" ] || { echo "REFUSING: cspReport.js at ${S:0:7} is not f102d26" >&2; exit 93; }; done
[ "$(blob "$HEAD_SHA" "$R618")" = "$R618_H_BLOB" ] && [ "$(blob "$H_CQ" "$R618")" = "$R618_CQ_BLOB" ] && [ "$(blob "$R2" "$R618")" = "$R618_R2_BLOB" ] && [ -z "$(blob "$MAIN_SHA" "$R618")" ] \
  || { echo "REFUSING: rd618 is not 74c1c51 (head) / d2f1253 (fd01298) / 8bbfcc7 (874c4f5), absent on main" >&2; exit 93; }
[ "$(cnt "$H_CQ" "$SRV" "$OLD_LINE")" = "1" ] && [ "$(cnt "$HEAD_SHA" "$SRV" "$OLD_LINE")" = "0" ] && [ "$(cnt "$HEAD_SHA" "$SRV" "$NEW_LINE")" = "1" ] && [ "$(cnt "$H_CQ" "$SRV" "$NEW_LINE")" = "0" ] \
  || { echo "REFUSING: the cap line is not old-at-fd01298 / new-at-head exactly once each (m0's premise)" >&2; exit 93; }
for S in "$H_CQ" "$HEAD_SHA"; do
  [ "$(cnt "$S" "$SRV" "$COND_LINE")" = "1" ] && [ "$(cnt "$S" "$SRV" "$OFFERED_LINE")" = "1" ] || { echo "REFUSING: the firing condition / offered line is not once at ${S:0:7} (m6's premise: unchanged)" >&2; exit 93; }
done
[ "$(cnt "$HEAD_SHA" "$SRV" "const { CSP_REPORT_BODY_LIMIT, CSP_REPORT_RATE, CSP_REPORT_MAX_ENTRIES_PER_REQUEST, buildCspEntries } = require('./services/cspReport');")" = "1" ] \
  || { echo "REFUSING: the head's import of CSP_REPORT_MAX_ENTRIES_PER_REQUEST is not as briefed" >&2; exit 93; }
for T in "const PER_REQUEST_MAX = 10;" 'requestCountInLog: /\bof 150\b|\b150 reports\b/.test(capped.log),' 'capLineUnderCap: /per-request cap/.test(under.log),' \
         'capLine: capped.log.includes(`CSP report: per-request cap (${PER_REQUEST_MAX}) applied; extra reports dropped`),' \
         '}).toEqual({ s1: 204, capLine: true, requestCountInLog: false, s2: 204, capLineUnderCap: false });' "test('R8 — the per-request cap line is a FIXED text"; do
  [ "$(cnt "$HEAD_SHA" "$R618" "$T")" = "1" ] || { echo "REFUSING: rd618 at the head lacks '$T' once (R8 / m3's premise)" >&2; exit 93; }
done
[ "$(g show "${HEAD_SHA}:${R618}" 2>/dev/null | grep -cE '^test\(')" = "14" ] && [ "$(g show "${H_CQ}:${R618}" 2>/dev/null | grep -cE '^test\(')" = "13" ] \
  && [ "$(g show "${HEAD_SHA}:${R618}" 2>/dev/null | grep -cE "^test\\('R9")" = "0" ] \
  || { echo "REFUSING: rd618 is not 14 test() at the head / 13 at fd01298, with no R9 (WRONG 1's premise)" >&2; exit 93; }
[ "$(diff <(g show "${H_CQ}:${R618}" 2>/dev/null | grep -E '^test\(') <(g show "${HEAD_SHA}:${R618}" 2>/dev/null | grep -E '^test\(') | grep -c '^[<>]')" = "1" ] \
  || { echo "REFUSING: rd618's titles fd01298 -> head are not exactly one added (R8)" >&2; exit 93; }
[ -z "$(g grep -lE 'kept [0-9]+ of [0-9]+ reports|kept \$\{' "$H_CQ" -- __tests__ 2>/dev/null)" ] || { echo "REFUSING: a test at fd01298 asserts the old 'kept N of M' text — WRONG 1 is stale; re-brief" >&2; exit 93; }
[ "$(cnt "$C735" "$R735" 'kept 10 of 12 reports in one request')" -ge 1 ] || echo "NOTE: rd735 at 7e2cc9f no longer asserts the old cap text — m11 / L-M3's premise moved" >&2
for S in "$R2" "$H_CQ" "$HEAD_SHA"; do
  [ "$(cnt "$S" "$CSPR" 'const CSP_REPORT_MAX_ENTRIES_PER_REQUEST = 10;')" = "1" ] && [ "$(cnt "$S" "$CSPR" '.slice(0, CSP_REPORT_MAX_ENTRIES_PER_REQUEST);')" = "1" ] \
    && [ "$(cnt "$S" "$CSPR" 'windowMs: 60 * 1000, max: 60')" = "1" ] || { echo "REFUSING: the cap / slice / CSP_REPORT_RATE are not once each at ${S:0:7} (m7's premise)" >&2; exit 93; }
done
for S in "$H_CQ" "$HEAD_SHA"; do
  [ "$(g show "${S}:${SRV}" "${S}:${CSPR}" 2>/dev/null | grep -cE 'createCspEntryBudget|budgetSpent')" = "0" ] || { echo "REFUSING: the entry budget is present at ${S:0:7} — WRONG 2 is stale; re-brief" >&2; exit 93; }
done
[ "$(g show "${C735}:${SRV}" "${C735}:${CSPR}" 2>/dev/null | grep -cE 'createCspEntryBudget|budgetSpent')" -ge 1 ] || echo "NOTE: the entry budget is absent at 7e2cc9f too — m7's positive control is gone" >&2
[ "$(g log --format=%H -S'reports in one request (per-request cap)' "$HEAD_SHA" -- "$SRV" 2>/dev/null | tr '\n' ' ' | sed 's/ $//')" = "$H_FIX $R2" ] \
  || { echo "REFUSING: git log -S of the old cap text is not a1d484d + 874c4f5 (m9's premise)" >&2; exit 93; }

# 95 — the intake log census premise (m4) and the RD-735 cross (m11).
LC="$(g show "${HEAD_SHA}:${SRV}" 2>/dev/null | sed -n '860,925p' | grep -c 'logger\.')"
[ "$LC" = "6" ] || echo "NOTE: the server entry point :860-:925 at the head carries $LC logger calls, not 6 — m4 re-derives its census anyway" >&2
[ "$(cnt "$HEAD_SHA" "$SRV" 'logger.warn(`🛡️  CSP report could not be recorded: ${e.message}`);')" = "1" ] && [ "$(cnt "$HEAD_SHA" "$SRV" "logger.warn('🛡️  CSP violation report:', entry);")" = "1" ] \
  && [ "$(cnt "$HEAD_SHA" "$SRV" 'logger.warn(`🛡️  CSP report refused (${status}): ${err.type}; nothing stored`);')" = "1" ] \
  || { echo "REFUSING: the intake's request-derived candidates (:887 entry, :896 e.message, :921 err.type) are not as briefed (m4's premise)" >&2; exit 95; }
[ "$(g show "${HEAD_SHA}:${CSPR}" 2>/dev/null | grep -cE 'logger|console\.')" = "0" ] || echo "NOTE: cspReport.js at the head now logs — m4's census widens" >&2
RC735="$(conflicts "$HEAD_SHA" "$C735" | tr '\n' ' ' | sed 's/ $//')"
[ "$RC735" = "$SRV $COUNTS_FILE" ] || [ "$RC735" = "$COUNTS_FILE $SRV" ] || echo "NOTE: merge-tree head x RD-735 7e2cc9f conflicts in '${RC735:-nothing}', not the server entry point + counts as briefed (m11)" >&2

# 98 — shared blobs identical at M0 and the head.
for PAIR in "$HARN $HARN_BLOB" "$TSH $TSH_BLOB" "$R495 $R495_BLOB" "$R607 $R607_BLOB"; do
  P="${PAIR% *}"; B="${PAIR#* }"
  for S in "$MAIN_SHA" "$HEAD_SHA"; do [ "$(blob "$S" "$P")" = "$B" ] || { echo "REFUSING: $P at ${S:0:7} is not ${B:0:7}" >&2; exit 98; }; done
done
for PAIR in "$TS $TS_BLOB" "$R465 $R465_BLOB" "$R549 $R549_BLOB" "$DKF $DKF_BLOB" "$DIG $DIG_BLOB"; do
  P="${PAIR% *}"; B="${PAIR#* }"
  for S in "$MAIN_SHA" "$HEAD_SHA"; do [ "$(sblob "$S" "$P")" = "$B" ] || { echo "REFUSING: $P at ${S:0:7} is not $B" >&2; exit 98; }; done
done

# 23 — main's own movement since the base touches none of the member's paths (no combined blob predicted).
OVM="$(comm -12 <(g diff --name-only "$M_BASE" "$MAIN_SHA" 2>/dev/null | grep -vxF "$COUNTS_FILE" | sort) <(g diff --name-only "$M_BASE" "$HEAD_SHA" 2>/dev/null | grep -vxF "$COUNTS_FILE" | sort))"
[ -z "$OVM" ] || { echo "REFUSING: main changed a path the head also changes since b7bb1e9: $OVM — a COMBINED blob the brief does not predict" >&2; exit 23; }
[ "$(g diff --name-only "$M_BASE" "$MAIN_SHA" 2>/dev/null | sort)" = "$(sorted "$ALA
$R314
$COUNTS_FILE")" ] || echo "NOTE: b7bb1e9..e91ff4e is no longer exactly azureLogAnalytics + rd314 + counts" >&2

# 35 — counts at every pinned sha; __tests__ census.
for PAIR in "$M1904 4133 247" "$R2 4146 248" "$M_BASE 4252 259" "$H_MRG 4252 259" "$H_CNT 4265 260" "$H_CQ 4265 260" "$H_FIX 4265 260" "$HEAD_SHA 4266 260" "$MAIN_SHA 4262 260"; do
  S="${PAIR%% *}"; WANT="${PAIR#* }"
  CT="$(counts_at "$S")"
  [ "$CT" = "$WANT" ] || { echo "REFUSING: $COUNTS_FILE at ${S:0:7} reads '${CT:-unreadable}', not '$WANT'" >&2; exit 35; }
done
CENSUS="$(for S in "$M_BASE" "$MAIN_SHA" "$R2" "$H_CQ" "$HEAD_SHA"; do printf '%s ' "$(ntests "$S")"; done)"
[ "$CENSUS" = "302 303 290 303 303 " ] || { echo "REFUSING: the __tests__ census (b7bb1e9 e91ff4e 874c4f5 fd01298 head) is '$CENSUS', not '302 303 290 303 303'" >&2; exit 35; }

# 70 — package-lock: ONE blob in play; package.json identical; the npm cache and the sqlite3 prebuild (NOTEs); the two Tuesday answers carried.
for S in "$M_BASE" "$MAIN_SHA" "$H_CQ" "$HEAD_SHA"; do [ "$(blob "$S" "$LOCK")" = "$LOCK_M_BLOB" ] || { echo "REFUSING: package-lock at ${S:0:7} is not e9063d4" >&2; exit 70; }; done
[ "$(blob "$R2" "$LOCK")" = "$LOCK_OLD_BLOB" ] || { echo "REFUSING: package-lock at 874c4f5 is not 9064763 (the brief's lock map)" >&2; exit 70; }
for S in "$MAIN_SHA" "$HEAD_SHA"; do [ "$(blob "$S" "$PKG")" = "$PKG_BLOB" ] || { echo "REFUSING: package.json at ${S:0:7} is not cdb1168" >&2; exit 70; }; done
[ "$(blob "$M_ORIGIN" "$LOCK")" = "$LOCK_M_BLOB" ] || echo "NOTE: package-lock on origin main ${M_ORIGIN:0:7} is not e9063d4 — another lock is in play; prove node_modules before any run (H-31)" >&2
if [ -d "$NPM_CACHE/index-v5" ]; then
  for T in axios/-/axios-1.20.0.tgz http-cache-semantics/-/http-cache-semantics-4.3.0.tgz sqlite3/-/sqlite3-5.1.7.tgz; do
    grep -r -l -F -m1 -- "$T" "$NPM_CACHE/index-v5" >/dev/null 2>&1 || echo "NOTE: the local npm cache index has no '$T' — the offline npm ci (H-31) may ENOTCACHE" >&2
  done
else
  echo "NOTE: no local npm cache at $NPM_CACHE — H-31's offline install has no source; the gate will mail a QUESTION" >&2
fi
PB_NOW="$(shasum -a 256 "$PREBUILD" 2>/dev/null | cut -d' ' -f1)"
[ "$PB_NOW" = "$PREBUILD_SHA" ] || echo "NOTE: the cached sqlite3 prebuild is '${PB_NOW:-absent}', not 84a34404…7afc — ruling (m)'s condition 1 records what the gate finds" >&2
[ -s "$SQLITE_RULING" ] && grep -qF 'The offline unpack of sqlite3' "$SQLITE_RULING" || { echo "REFUSING: Tuesday's sqlite3 prebuild ruling (ruling m) is not at $SQLITE_RULING" >&2; exit 70; }
[ -s "$BELT_ANS" ] && grep -qF 'run UNBELTED. Every other jest run stays belted: cells, mutants, C-68 unions, drivers and servers.' "$BELT_ANS" \
  || { echo "REFUSING: Tuesday's belt answer (ruling n) is not at $BELT_ANS as quoted" >&2; exit 70; }

# 80 — the merge premise by the READ-ONLY three-argument merge-tree (no objects written anywhere): main x head counts-only.
MT_PAIRS=0
for X in "$MAIN_SHA" "$M_ORIGIN"; do
  CONF="$(conflicts "$X" "$HEAD_SHA" | tr '\n' ' ' | sed 's/ $//')"
  MT_PAIRS=$((MT_PAIRS + 1))
  [ -z "$CONF" ] || [ "$CONF" = "$COUNTS_FILE" ] || { echo "REFUSING: merge-tree ${X:0:7} x ${HEAD_SHA:0:7} carries conflict markers in '${CONF}' — not counts-only (80)" >&2; exit 80; }
done

# 31 — the READY, the ruling and its ancestors, builder evidence, prior reports, gate 13's instruments, standing references on disk.
for f in "$READY" "$RULING" "$CQ_GO" "$LINES_ANS" "$BELT_ANS" "$SQLITE_RULING" "$CLAR" "$B9_REPORT" "$B12_REPORT" "$BRIEF15" "$C133" \
         "$EV_M/rd618-b1-hold.log" "$EV_M/rd618-b1-hold.sh" "$NX/session-tools/nexusai-lock.sh" \
         "$B13_INST/HOLD13.sh" "$B13_INST/qa-holdlib13.sh" "$B13_INST/qa-floorlib13.sh" "$B13_INST/qa-floorcount.py" "$B13_INST/qa-to.sh" "$B13_INST/qa-jestwrap.sh" "$B13_INST/qa-jsum.js" \
         "$B13_INST/qa-runj13.sh" "$B13_INST/qa-mut13.py" "$B13_INST/qa-mutlib13.sh" "$B13_INST/qa-merge13.sh" "$B13_INST/qa-mt13.sh" "$B13_INST/qa-pin13.sh" "$B13_INST/qa-build13.sh" \
         "$B13_INST/qa-h1-selftest13.sh" "$B13_INST/qa-h1-scan.py" "$B13_INST/qa-mail.py" "$B13_INST/qa-mailread.py" "$B13_INST/qa-lockcheck.py" "$B13_INST/qa-ssprint.sh" \
         "$B13_INST/qa-netbelt.sb" "$B13_INST/qa-netbelt-nodns.sb" "$B13_INST/qa-netbelt-ctl.js" "$B13_INST/qa-titles13.py" "$B13_INST/qa-lost13.py" \
         "$B13_INST/qa-c57-id-superset.sh" "$B13_INST/qa-c68census.py" "$B13_INST/qa-cov-setup.js" "$B13_INST/qa-boot13.js" \
         "$G7R1_FLOOR" "$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"; do
  [ -s "$f" ] || { echo "REFUSING: evidence or tool absent: $f" >&2; exit 31; }
done
grep -qF "${HEAD_SHA:0:7}" "$READY" && grep -qF 'PRIOR WORK' "$READY" || { echo "REFUSING: the READY does not name 953a0e6 or carry its PRIOR WORK section" >&2; exit 31; }
grep -qF 'Re-gate: tier 2 through code. It joins the next gate batch, and Tuesday commissions it on your READY. Round 1 of 2 for this class. If the class reaches a third objection, STOP.' "$RULING" \
  && grep -qF 'so that NO request-derived value is interpolated into a log line. Use a fixed text plus the server-side cap constant' "$RULING" \
  && grep -qF 'Each cell must still go RED when the cap line is NOT logged (that is the mutant).' "$RULING" \
  && grep -qF 'PRIOR WORK in the READY: name the operator-facing information this removes (the kept/offered counts). Say that the per-request cap and the entry budget are unchanged.' "$RULING" \
  && grep -qF "Your rd618 unit cells assert stripQueryAndFragment's exact output, and that covers the host." "$CQ_GO" \
  && grep -qF 'RD-735: do NOT move its head while gate 15 is gating 7e2cc9f' "$LINES_ANS" \
  || { echo "REFUSING: Tuesday's (b1) RULING / codeql GO / rd735-lines ANSWER no longer carry the lines the brief quotes" >&2; exit 31; }
grep -qF 'jest lock acquired by s86m-rd618-b1-hold after 7375s' "$EV_M/rd618-b1-hold.log" && grep -qF 'Tests:       287 passed, 287 total' "$EV_M/rd618-b1-hold.log" \
  && [ "$(grep -cF 'Tests:       1 failed, 13 skipped, 14 total' "$EV_M/rd618-b1-hold.log")" = "3" ] \
  && grep -qF 'verify-suite: expectation UPDATED — tests=4266 suites=260' "$EV_M/rd618-b1-hold.log" && grep -qF 'VERDICT: PASS — 4266/4266 tests passed across 260 suites (jest exit 0)' "$EV_M/rd618-b1-hold.log" \
  && grep -qF '[ "$(git rev-parse --short=7 HEAD)" = "a1d484d" ]' "$EV_M/rd618-b1-hold.sh" && grep -qF -- '-t "R8"' "$EV_M/rd618-b1-hold.sh" && ! grep -qF -- '--forceExit' "$EV_M/rd618-b1-hold.sh" \
  || { echo "REFUSING: the builder's b1 hold log/script no longer carries the lines the brief quotes (WRONG 4/5's premise)" >&2; exit 31; }
grep -qF 'RD-618 r2** (TIER 1, round 2 of 2) | **GO WITH FINDINGS**' "$B9_REPORT" && grep -qF 'when no cap applied (empty bodies dropped by the filter)' "$B9_REPORT" \
  || { echo "REFUSING: the batch-9 report no longer carries RD-618's verdict / A-N2 as the brief quotes" >&2; exit 31; }
grep -qF 'RD-618 (MTa) + RD-735 (MTb)' "$B12_REPORT" && grep -qF 'RESUME METHOD NOTE' "$B12_REPORT" && grep -qF 'File **one focused hold at a time** (≤~40 min of jest)' "$B12_REPORT" \
  || { echo "REFUSING: gate 12's report no longer carries RD-618 as MTa / the RESUME METHOD NOTE the brief quotes (ruling j)" >&2; exit 31; }
grep -q '^SELF-CHECK: re-read end-to-end for contradictions | Tuesday' "$BRIEF15" || echo "NOTE: gate 15's brief does not read as stamped by Tuesday — the brief calls it the stamped template" >&2
grep -qE '^ROOT=\$\{ROOT:-32659\}' "$B13_INST/qa-floorlib13.sh" || echo "NOTE: gate 13's qa-floorlib13.sh ROOT default is no longer 32659 — the brief's 'STALE defaults' line names the old value" >&2

# 83 — the C-133 script is the RD-658 version the brief names (ruling l / H-30).
C133_NOW="$(shasum -a 256 "$C133" 2>/dev/null | cut -d' ' -f1)"
[ "$C133_NOW" = "$C133_SHA" ] || echo "NOTE: session-tools/s78g/c133-accounting.py sha256 is '${C133_NOW:-unreadable}', not 6f938bfc…f972f — the gate names the version it used (H-30)" >&2

# 39 — the floor instruments are named in the brief.
for f in "$PREV_FLOORLIB" "$G7R1_FLOOR"; do
  grep -qF "$f" "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument $f" >&2; exit 39; }
done

# 10 / 17 — report path named in both; no stale report; brief names every source it cites.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }
for P in "$B9_REPORT" "$B12_REPORT" "$BRIEF15" "$READY" "$B13_INST/" '2026-10-05_nexusai_MN_rd618_b1_turn.md' '2026-10-05_nexusai_M_rd735_lines_ANSWER.md' \
         '2026-10-05_qa_b14_belt_ANSWER.md' '2026-10-05_qa_b14_sqlite3_ANSWER.md'; do
  grep -qF "$P" "$BRIEF" || { echo "REFUSING: brief must name $P" >&2; exit 10; }
done

# 11 — identity: NexusAI's OWN dirs.
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

# 12 / 13 / 14 / 15 / 20 — tier, directive, brief path, pins, verdict route, key path, question route.
for T in 'RD-618 (b1) is TIER 2 (through code).' 'No docker, no image build, no image leg' 'ONE member, no priority.' 'NO NPM REGISTRY EXCEPTION' 'IS PART OF H-31' \
         'FULL VERIFIES UNBELTED' 'BOTH thresholds block'; do
  grep -qF "$T" "$BRIEF" || { echo "REFUSING: brief does not declare '$T'" >&2; exit 12; }
done
for T in 'RD-618 (b1), a re-gate at TIER 2 (through code)' 'round 1 of 2 for this class' 'NOT the demo' 'BOTH THRESHOLDS BLOCK' 'UNBELTED'; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare '$T'" >&2; exit 12 ;; esac
done
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
for S in "$HEAD_SHA" "$MAIN_SHA" "$M_BASE" "$H_FIX" "$H_CQ" "$H_CNT" "$H_MRG" "$R2"; do
  grep -qF -- "$S" "$BRIEF" || grep -qF -- "${S:0:7}" "$BRIEF" || { echo "REFUSING: brief must name $S" >&2; exit 14; }
  case "$PROMPT" in *"$S"*) ;; *) echo "REFUSING: prompt must name $S" >&2; exit 14 ;; esac
done
for S in "$M1904" "$C735" "$LOCK_M_BLOB" "$LOCK_OLD_BLOB" "$PKG_BLOB" "$SRV_M_BLOB" "$SRV_CQ_BLOB" "$SRV_H_BLOB" "$CSPR_H_BLOB" "$CSPR_M_BLOB" "$R618_H_BLOB" "$R618_CQ_BLOB" \
         "$HARN_BLOB" "$TS_BLOB" "$TSH_BLOB" "$R495_BLOB" "$R607_BLOB" "$R465_BLOB" "$R549_BLOB" "$DKF_BLOB" "$DIG_BLOB"; do
  grep -qF -- "${S:0:7}" "$BRIEF" || { echo "REFUSING: brief must name ${S:0:7}" >&2; exit 14; }
done
if printf '%s\n' "$PROMPT" | LC_ALL=C grep -q '@[A-Z_0-9]*@'; then echo "REFUSING: the prompt carries a placeholder" >&2; exit 14; fi
case "$PROMPT" in *"MAIL YOUR VERDICT"*"tuesday-agent@agentmail.to"*) ;; *) echo "REFUSING: prompt must say MAIL YOUR VERDICT to tuesday-agent@agentmail.to" >&2; exit 15 ;; esac
grep -qF "$SUBJECT" "$BRIEF" || { echo "REFUSING: brief must carry the subject exactly: $SUBJECT" >&2; exit 15; }
case "$PROMPT" in *"$SUBJECT"*) ;; *) echo "REFUSING: prompt must carry the subject exactly: $SUBJECT" >&2; exit 15 ;; esac
if grep -qF 'EARLY VERDICT — batch 16' "$BRIEF" || printf '%s\n' "$PROMPT" | grep -qF 'EARLY VERDICT'; then echo "REFUSING: an EARLY VERDICT route is carried — batch 16 has one member" >&2; exit 15; fi
case "$PROMPT" in *"/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env"*) ;; *) echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20 ;; esac
for T in "$QUESTION_SUBJ" "$ANSWER_PREFIX" "$ROUTE_NAME"; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the question route: $T" >&2; exit 20; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the question route: $T" >&2; exit 20 ;; esac
done
if printf '%s\n' "$PROMPT" | grep -qi 'wednesday-agent@' && ! printf '%s\n' "$PROMPT" | grep -q 'Never wednesday-agent@'; then
  echo "REFUSING: the prompt routes to wednesday-agent@ — Datasec's coordinator is Tuesday" >&2; exit 15; fi

# 82 — THE MODEL RULE (Kam 2026-09-30 09:07, card (b)) is carried in the brief and the prompt, per session, never "Switch automatically".
for T in "$STATUS_SUBJ" "$PARK_LINE" 'classifier-stops.txt' 'Switch automatically' 'Opus 4.8' 'PER SESSION' 'which rows ran on which model' 'Opus 5.5'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks THE MODEL RULE fragment '$T'" >&2; exit 82; }
  case "$(printf '%s' "$PROMPT" | tr '[:upper:]' '[:lower:]')" in *"$(printf '%s' "$T" | tr '[:upper:]' '[:lower:]')"*) ;; *) echo "REFUSING: prompt lacks THE MODEL RULE fragment '$T'" >&2; exit 82 ;; esac
done
grep -qF '## THE MODEL RULE' "$BRIEF" && grep -qF 'H-27' "$BRIEF" && grep -qF 'H-28 (AMENDED' "$BRIEF" && grep -qF 'H-31 (RE-BASED' "$BRIEF" && grep -qF 'H-32 (RE-BASED' "$BRIEF" && grep -qF 'H-33 (RE-BASED' "$BRIEF" \
  || { echo "REFUSING: brief lacks THE MODEL RULE section or H-27/H-28 (amended)/H-31..H-33 (re-based)" >&2; exit 82; }

# 19 — the words the prompt must carry (% is a space); the brief's sections; limits; rows; READY lines verbatim; clarification quotes.
WORDS="RD-618 RD-735 RD-314 C-02 C-49 C-57 C-68 C-89 C-98 C-102 C-104 C-112 C-115 C-125 C-129 C-141 ADDENDUM%5 C-174 C-185 C-186 C-190 C-192
RED-AT-PARENT m0 m1 m2 m3 m4 m5 m6 m7 m8 m9 m10 m11 m12 y1 y5 MT1 M0 R8 M1 M2 M-shape M-dropped M-second M-kept M-cap11 A-N2 #255 #47 js/log-injection
rule%severity%error alerts_threshold%errors high-or-higher INSTANCE refs/pull/47/head mergeable 4276/261 4266/260 304 new%ids%14 missing%0 e9063d4
L-M1 L-M6 L-Y1 H-1 H-2 H-3 H-9 H-15 H-20 H-21 H-22 H-24 H-25 H-26 H-27 H-28 H-29 H-31 H-32 H-33 --forceExit trap%on%EXIT deadline LANDING%CONTROL
_prebuilds node_sqlite3.node sqlite3%binding:%cached%prebuild,%offline test-server-helper exits%71 SCRATCH%object%dir OTHER%direction git%clone%--shared
REGENERATION id-superset pull%request STOP POSITIVE%CONTROL%FIRST POSITIVE%CONTROL NEGATIVE%CONTROL node%--check VOID EXCLUSIVE qa-b16- qa-b14- qa-b15- MERGES%GO%FIRST
QUEUE,%NEVER%TAKE%OVER --after UNCHANGED%tag DEADLINE HEARTBEAT PEER%gates 2%minutes 5%minutes finally SESSION_SECRET%UNSET NOT%TESTED MEASURED%AT%RUNTIME READ%ONLY PROBED RELAYED
UNKNOWN about%40%minutes 2-hour%maximum TRACKED%child PRIOR%WORK FOREGROUND never%push NEVER%merge Partner%Center batch-9 gate%12 gate%15 npm%install --offline ENOTCACHED
HOLD13.sh qa-floorlib13.sh Never%rm datasecau/Reporting_Dashboard_Au 127.0.0.1 local%run fd01298 a938930 7e2cc9f empties%beyond%the%cap entry%budget 429"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in "^## TUESDAY'S RULINGS" '^## THE MODEL RULE' '^## Charter' '^## THE CLARIFICATIONS THAT BIND THIS GATE' '^## PRIOR ROUND' '^## 1. Target' '^### Builder' '^## 2. Why this tier' \
         '^## 2a. LEGITIMATE SHAPES' '^## 3. THE QUESTIONS' '^## 3a. INSTRUMENT RULES' '^## 3b. THE NEGATIVE-ASSERTION SWEEP' '^## 4. TARGET' '^## 7. THE MERGED TREE' '^## 8. CI' \
         '^## 9. Floor discipline' '^## 10. HELD' '^## 11. Output' '^## WRONG OR UNVERIFIED' '^## PROVENANCE' '^### MERGE' '^### File overlap' '^### How to build your trees' '^## FILL AT STAMP'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
for L in L-M1 L-M2 L-M3 L-M4 L-M5 L-M6 L-Y1; do
  grep -qF "$L" "$BRIEF" || { echo "REFUSING: brief lacks declared limit $L (C-112)" >&2; exit 19; }
done
for R in m0 m1 m2 m3 m4 m5 m6 m7 m8 m9 m10 m11 m12 y1 y2 y3 y4 y5; do
  grep -qF "| $R |" "$BRIEF" || { echo "REFUSING: brief lacks row $R" >&2; exit 19; }
done
# the builder's stated limits / claims carried verbatim (each line checked in the READY AND the brief).
while IFS= read -r T; do
  [ -n "$T" ] || continue
  grep -qF -- "$T" "$READY" || { echo "REFUSING: '$T' is no longer in the READY — it changed; re-brief" >&2; exit 19; }
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not carry the READY line '$T' verbatim" >&2; exit 19; }
done <<'VERBATIM_EOF'
REMOVED: the kept/offered counts in that log line. An operator now sees THAT the cap applied and its value (10), not the per-request numbers.
UNCHANGED: the cap itself (CSP_REPORT_MAX_ENTRIES_PER_REQUEST = 10, buildCspEntries' slice), the condition that fires the line (offered > entries.length), the stored entries, the per-entry violation log lines, the 400/413/415 refusal lines, and the limiter. The entry budget is RD-735's and is not on this branch.
Correction to your ruling's wording: on RD-618's branch NO existing cell asserted the old cap text (rd618 R6 counts violation lines only; "R9" is rd735's).
the line fires only on a request with more than 10 csp-violation reports (or empties beyond the cap)
GREEN: the 24-file harness union (pattern helpers/rd395-server-harness, rd618 included) + rd495 + rd607: 287/287.
RED with fd01298's server.js (the count line): R8 red.
M1 (cap line not logged): R8 red. M2 (cap line always logged, condition forced true): R8 red. Each restored by sha (2684acd).
Pre-scan, BOTH thresholds (C-190 addendum): no new logger line interpolates a request value
Merge-tree vs main e91ff4e (N's RD-314 landed): counts only.
CodeQL on PR #47 is the external check: expect #255 closed by the fix, nothing new.
VERBATIM_EOF
# the rulings the brief rests on are quoted from source and still say so
while IFS= read -r Q; do
  [ -n "$Q" ] || continue
  grep -qF -- "$Q" "$CLAR" || { echo "REFUSING: CLARIFICATIONS no longer carries '$Q' — the brief's quotes are stale; re-brief" >&2; exit 19; }
  grep -qF -- "$Q" "$BRIEF" || { echo "REFUSING: brief does not quote '$Q'" >&2; exit 19; }
done <<'CLAR_EOF'
A local run serves every page and API with no sign-in.
A merge conflict confined to `scripts/verify-expected-counts.json` is resolved by regeneration, with an id-superset control.
a clean merge-tree and a changed measured surface are not in tension
A cell asserts the PROPERTY THAT MUST HOLD AFTER THE FIX, never the defect that exists before it
every existing test that relied on a LATER return in that function is a candidate for silent disarmament
A declared limit is where the evidence stops — not a place it is cleared.
absence of a port clash is NOT evidence of a quiet floor.
NEVER KILL BY PATTERN.
counts as known ONLY when the received object differs from the expected in `envReached` alone
Both O-1 cells LEAVE the set when RD-733 merges.
No re-run is used as a clearance
THE TURN PASSES
Addendum 2's "once PER WAITING GATE TICKET" means once per gate TAG.
Every merge to NexusAI main goes through a PULL REQUEST, and a PR must add NO NEW high-or-higher CodeQL alert in the code it changes. Test code is included.
`alerts_threshold = errors`, so ANY new alert whose RULE severity is `error` blocks, whatever its security severity.
`js/log-injection` counts, even when the interpolated value is a number derived from the request.
a FAILED ls-remote is UNKNOWN, never a value.
CLAR_EOF

# 24 — the prompt must DESCRIBE the server entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qi 'backend/server\.js'; then
  echo "REFUSING: the prompt contains the server entry point's literal path (RD-591 c.37901). Describe it; do not name it." >&2; exit 24; fi

# 53 / 71 — standing rules in the brief; the NOT TESTED line verbatim in both.
for w in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' 'qa-b16-' 'node --check' 'VOID' 'EXCLUSIVE' 'POSITIVE CONTROL FIRST' \
         'QUEUE, NEVER TAKE OVER' 'LANDING CONTROL' 'C-104' 'Main may move' '--after' 'never push' 'C-174' '--forceExit' 'trap … EXIT' 'MERGES GO FIRST' \
         'session-tools/locks/queue-jest/' 'carry on' 'never idles holding the jest lock' 'ONE focused hold at a time' 'FOREGROUND' '5600' '8995' 'PEER gates' 'UNCHANGED tag'; do
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

# 81 — this gate's own premises (and the carried lessons) are in the brief.
for w in 'RED-AT-PARENT' 'missing 0' 'C-190' 'NEVER opens, comments on, approves, re-runs or merges a PR' '4276/261' 'RE-BASE EVERY PREDICTION' 'H-20' 'H-21' 'H-22' 'H-23' 'H-24' 'H-25' 'H-26' \
         'NEVER merges and never pushes' 'THREE-ARGUMENT' 'Blocker' 'setuid' 'pgrep' '`END ok`' 'exits 71' 'ARRAY option' '=====' 'UNKNOWN, never a value' \
         'e9063d4' '9064763' 'npm ci --offline --ignore-scripts' 'ENOTCACHED' '_cacache' '_prebuilds' '84a34404' 'sqlite3 binding: cached prebuild, offline' \
         'a938930' '2684acd' 'R8' 'M1' 'M2' 'M-shape' 'M-cap11' 'A-N2' '#255' 'PR #47' 'CONFLICTING' 'results_count' 'alerts_threshold' 'high_or_higher' 'instance' \
         'createCspEntryBudget' 'CSP_REPORT_RATE' 'PER_REQUEST_MAX = 10' ':887' ':896' ':921' 'kept/offered' 'b7bb1e9' 'e91ff4e' 'ANY rd465 O-1 failure' \
         'WRONG 1' 'WRONG 2' 'WRONG 3' 'test-server-helper' 'qa-floorlib13.sh' 'HOLD13.sh' 'ADDENDUM 5' 'datasecau/Reporting_Dashboard_Au' 'IS PART OF H-31' 'Round 1 of 2 for this class'; do
  grep -qiF -- "$w" "$BRIEF" || { echo "REFUSING: brief lacks this gate's premise '$w'" >&2; exit 81; }
done

# 41 — the jest queue as the launch finds it (MERGES GO FIRST): a NOTE for every merge-tagged / peer-gate ticket (read-only ls/grep).
if [ -d "$LOCKQ" ]; then
  MQ="$(grep -l -i 'merge' "$LOCKQ"/* 2>/dev/null | wc -l | tr -d ' ')"
  [ "${MQ:-0}" = "0" ] || echo "NOTE: $MQ merge-tagged ticket(s) in the jest queue now — the gate files behind them (brief §9 clause 1)" >&2
  for PT in qa-b14- qa-b15-; do
    BQ="$(grep -l "$PT" "$LOCKQ"/* 2>/dev/null | wc -l | tr -d ' ')"
    [ "${BQ:-0}" = "0" ] || echo "NOTE: $BQ peer-gate ($PT) ticket(s) in the jest queue now — a PEER gate: FIFO, never touched" >&2
  done
else
  echo "NOTE: jest queue dir $LOCKQ not found — the gate reads the lock tool's own layout at start" >&2
fi

# 38R — the negative-control seats are DERIVED now from the live cockpit panes: the claude descendant of each pane pid.
# ps, not pgrep: macOS pgrep hides the caller's own ancestors, so Tuesday's own claude would vanish when --check runs from her shell. REFUSES when any of the five is missing.
command -v tmux >/dev/null 2>&1 || { echo "REFUSING: tmux not found — cannot derive the negative-control seats" >&2; exit 38; }
PANES="$(tmux list-panes -a -F '#{pane_pid} #{@cockpit_name}' 2>/dev/null)"
[ -n "$PANES" ] || { echo "REFUSING: tmux list-panes returned nothing — cannot derive the negative-control seats" >&2; exit 38; }
PSTAB="$(ps -axo pid=,ppid=,comm= 2>/dev/null)"
[ -n "$PSTAB" ] || { echo "REFUSING: ps returned nothing" >&2; exit 38; }
claude_under() {   # prints the claude pids among the descendants (depth <= 5) of pane pid $1
  printf '%s\n' "$PSTAB" | awk -v root="$1" '
    { pid[NR]=$1; pp[NR]=$2; c=$3; sub(/^.*\//,"",c); cm[NR]=c }
    END { lvl[root]=0; for (d=1; d<=5; d++) for (i=1;i<=NR;i++) if ((pp[i] in lvl) && !(pid[i] in lvl) && lvl[pp[i]]==d-1) lvl[pid[i]]=d;
          for (i=1;i<=NR;i++) if ((pid[i] in lvl) && pid[i]!=root && cm[i]=="claude") print pid[i] }'; }
pane_pid_of() { printf '%s\n' "$PANES" | awk -v n="$1" '{p=$1; $1=""; sub(/^ /,""); if ($0==n) print p}'; }
NEG_SEATS=''; NEG_DESC=''
for NAME in Datasec/NexusAI-M Datasec/NexusAI-N Datasec/NexusAI-O Datasec/NexusAI-P tuesday; do   # the coordinator pane is named 'tuesday' on this seat (gate 14's launcher fix, s97, 2026-10-05)
  PP="$(pane_pid_of "$NAME")"
  [ "$(printf '%s\n' "$PP" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: expected exactly one tmux pane named '$NAME', found: '${PP:-none}' — cannot derive its negative-control seat" >&2; exit 38; }
  CP="$(claude_under "$PP")"
  [ "$(printf '%s\n' "$CP" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: pane '$NAME' (pid $PP) has '${CP:-no}' claude descendant(s), not exactly one — a seat is missing or ambiguous" >&2; exit 38; }
  NEG_SEATS="$NEG_SEATS $CP"; NEG_DESC="$NEG_DESC \`$CP\` ($NAME);"
done
NEG_SEATS="${NEG_SEATS# }"
[ "$(printf '%s\n' $NEG_SEATS | sort -u | wc -l | tr -d ' ')" = "5" ] || { echo "REFUSING: the five derived seat pids are not distinct: $NEG_SEATS" >&2; exit 38; }
for PEER in 'QA/NexusAI-batch14' 'QA/NexusAI-batch15'; do
  GP="$(pane_pid_of "$PEER")"; GC=''
  [ -n "$GP" ] && [ "$(printf '%s\n' "$GP" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] && GC="$(claude_under "$GP")"
  if [ -n "$GC" ] && [ "$(printf '%s\n' "$GC" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ]; then
    NEG_SEATS="$NEG_SEATS $GC"; NEG_DESC="$NEG_DESC \`$GC\` ($PEER, a live peer gate);"
  else
    echo "NOTE: no live claude under a pane named $PEER — that peer gate finished or its pane is gone" >&2
  fi
done

# 86 — no live gate-16 session already exists.
for P in $(pane_pid_of "$ROUTE_NAME"); do
  if [ -n "$(claude_under "$P")" ]; then echo "REFUSING: a pane named $ROUTE_NAME (pid $P) already runs a claude — gate 16 is live; do not start a second session" >&2; exit 86; fi
  [ "$CHECK" = "1" ] || echo "NOTE: a pane named $ROUTE_NAME (pid $P) exists with no claude under it — the cockpit's own add decides" >&2
done

# 32 / 40 — LAST: the coordinator's stamp (SELF-CHECK line + note, no placeholder) and the answer route (Tuesday adds it, never this launcher).
STAMP_OK=1
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then STAMP_OK=0; fi
ROUTE_OK=1
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || ROUTE_OK=0
if [ "$STAMP_OK" = "0" ] || [ "$ROUTE_OK" = "0" ]; then
  echo "guards pass (9 6 7 8 18 18b 22 93 95 98 23 35 70 80 31 83 39 10 17 11 12 13 14 15 20 82 19 24 53 71 76 77 78 79 81 41 38R 86); stamp and/or route NOT complete." >&2
  echo "  ls-remote attempts this run: $LSR_ATTEMPTS (C-192); three-argument merge-trees checked: $MT_PAIRS; origin main ${M_ORIGIN:0:7}" >&2
  echo "  member pin (origin, re-read now): RD-618 (b1) $HEAD_SHA · context RD-735 ${C735_NOW:0:7}" >&2
  echo "  NEG seats (38R, derived live):$NEG_DESC" >&2
  [ "$STAMP_OK" = "1" ] || echo "REFUSING (32): a stamp placeholder remains in the brief (the SELF-CHECK line / Self-check note) — the coordinator re-reads end-to-end and stamps them before launch" >&2
  if [ "$ROUTE_OK" = "0" ]; then
    echo "REFUSING (40): no '${ROUTE_NAME}|tuesday-agent@agentmail.to|no' line in $ROUTING — answers to the gate would have no route; Tuesday adds it at stamp (this launcher never writes it)" >&2; exit 40
  fi
  exit 32
fi

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  origin: the member branch at its pin at $PIN_TS (18; $LSR_ATTEMPTS ls-remote attempt(s), C-192)"
  echo "  main ${M_ORIGIN:0:7} (e91ff4e or a descendant; no member path moved) (18b)"
  echo "  merge-base (7); chain (8); deltas + no lock change (22); premises (93 95 98)"
  echo "  overlap (23); counts + census (35); lock + npm cache + sqlite3 prebuild + belt answer (70); $MT_PAIRS three-argument merge-trees counts-only (80); evidence (31); C-133 script (83)"
  echo "  H-1 (76); H-4 (77); H-9 (78); H-7/H-8 (79); premises (81); MODEL RULE (82); queue (41); route $ROUTE_NAME (40); report absent (17)"
  echo "  NEG seats (38R, derived live):$NEG_DESC"
  echo "  model: claude-opus-5-5 at exec"
  echo "  SUBJECT: $SUBJECT"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  --check started no claude; nothing written."
  exit 0
fi

PROMPT="$PROMPT

VERIFIED BY THE LAUNCHER AT $PIN_TS (git ls-remote origin, read-only, $LSR_ATTEMPTS attempt(s) under C-192): refs/heads/$BRANCH = $HEAD_SHA; refs/heads/main = $M_ORIGIN (e91ff4e or a descendant; no member path moved since e91ff4e); refs/heads/$C735_BRANCH = ${C735_NOW:-absent} (context, not a member). $MT_PAIRS three-argument merge-trees (read-only, no objects written) of main x the head were counts-only. These are the start-of-gate pins; take your own three readings anyway, and re-pin M0 yourself.
NEGATIVE-CONTROL SEATS, derived live by the launcher from the cockpit panes at $PIN_TS:$NEG_DESC Re-read them at the start of every hold."

# rd579-rd639 S-1 belt: the gate session inherits NO SESSION_SECRET. The line prints the NAME and a state only, never a value.
if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET in the launcher's environment (length ${#SESSION_SECRET}) — unsetting before exec"; else echo "SESSION_SECRET UNSET"; fi
unset SESSION_SECRET

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model claude-opus-5-5 "$PROMPT"
