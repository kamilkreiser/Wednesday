#!/bin/bash
# launch_qa_nexusai_gate30.sh — cross-project QA agent, ONE gate on Datasec/NexusAI (gate 30): a TIER-2 GATE THROUGH CODE, ROUND 1 of 2, of
# B302 lane 7 — RD-782 .. RD-789 (CodeQL alerts in TEST code), draft PR #98, branch b302/test-code-codeql @ 49ba21e — one gated head, one
# verdict per ticket, one overall, ONE report. 34 paths, all test code or test tooling, no product file.
# (derived 2026-10-20 by Tuesday's tooling sub-agent from launch_qa_nexusai_gate29.sh, as the gate-30 kit's FILL AT STAMP section asks (R-G13-4);
# the sub-agent ran only bash -n and --check on the real kit (unstamped) and on a SCRATCH copy with a deliberately wrong main — see the LAUNCHER-REPORT.)
# A FRESH gate on the Mac mini, /Volumes/Laptop-DEV; the T9 is UNMOUNTED, so the lock base is the Laptop-DEV locks-laptop-1017.
#   B302 b302/test-code-codeql @ 49ba21e (8 commits over 39653db: cb8755a 342afed b6cb5ec 56e1b61 198ef34 8bb6c33 017cf69 49ba21e)
#   M0 = the MAIN pin Tuesday STAMPS (39653db at drafting = mode 0: the head's base IS main, nothing is merged).
#
# LAUNCHED ONLY VIA: cockpit.sh add 'QA/NexusAI-gate30' "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate30.sh'"
#   (i.e. /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh). A tmux pane, NEVER nohup, never run it bare from a seat's shell.
#
# AUTHORITY: Tuesday's gate-30 commission (B317, 2026-10-20) and the kit's TIER 2 argument; Tuesday's rulings Q1-Q4 of the builder brief as the kit relays them.
# THE MODEL RULE: Kam, live board 2026-09-30 09:07, card nexusai-gate11-opus55-safeguard-model-switch, option (b), PER SESSION, as applied to gate 29.
# The MODEL is the kit's MODEL line (tier 2, routing v1.0 row G2, Sonnet), which must equal models_latest.json levels.sonnet.model_id.
# FINDINGS-ONLY: never merges (outside its own store), never pushes, never opens/comments/approves/un-drafts/updates a PR, never dismisses an
# alert, never swaps or edits the lock tool; no fix, no deploy, no az, no docker, no model call, no demo, no human.
#
# PATTERN: launch_qa_nexusai_gate29.sh (prompt EMBEDDED, --check mode, PIN-table parser, MAIN-STAMP line, C-192 lsr retry, lock-tool pin 90, the
# LIVE negative-control seat derivation 38R, guard 86, stamp + route + lock refusals LAST). CHANGES, each deliberate:
#   - MODEL: tier 2 / Sonnet. The kit line must start 'MODEL (tier 2;' and equal levels.sonnet.model_id (gate 29: 'MODEL (tier 1' / levels.opus).
#   - 40: the PIN-HEADS rows are MAIN + B302 (gate 29: MAIN + RD774). B302 must read branch b302/test-code-codeql, head 49ba21e, base 39653db, 8 commits.
#     MAIN-STAMP form: 'landed since 39653db4: <text>' (gate 29: 7700caf).
#   - 18: ALSO refuses (exit 18) when refs/pull/98/head is not 49ba21e (gate 29 only NOTEd a moved PR ref): a head that moved is a new kit amendment.
#   - 18M: 39653db is-ancestor of M0 (never --first-parent); M0's tree = the stamped tree; 49ba21e AND the other seven commits NOT on M0; mode 0 iff M0 =
#     39653db (then 'landed since' must read none); a moved M0 is mode a/b and REFUSES (T0: STOP) when anything landed since 39653db touches one of the
#     34 PR paths, or when the legacy stdout-only merge-tree of the head onto M0 shows any conflict marker (gate 29 tolerated the counts file; PR #98 does not touch it).
#   - 7/8: the chain base 39653db <- cb8755a <- ... <- 49ba21e, parents and EVERY tree (eight rows), linear: 8 commits, 8 first-parent, merge-base = base.
#   - 22: the 34 paths: 33 M + 1 A (A = __tests__/helpers/html-dom.js); every path is test code (__tests__/, tests/, scripts/test-*.js); 0 in the guarded
#     set (backend/ static/ templates/ package*.json .github/ bicep/ Dockerfile the counts file); the sorted path list's sha256 is PINNED; the four files of
#     the five open RD-786 sites are byte-UNCHANGED base..head. (gate 29's 8-file list, static/templates and counts-only merge guards dropped.)
#   - 93: lockfile, package.json, deploy-demo.yml and the counts file are the SAME blobs at M0 and the head and equal their pins; counts 4880/302 at the head;
#     deploy-demo gates BOTH jobs on vars.CI_DEPLOY_ENABLED; html-dom.js blob pinned. (gate 29's anchors, product blob pins, UNION/seed notes, proxy-addr/
#     playwright lock versions, base-arm control premise: DROPPED — no product file, no server boot, no browser.)
#   - 33L: REFUSES (deferred, like 32S) only while a qa-g29-* ticket HOLDS the jest lock. Queued tickets of other seats are fine (FIFO: the gate queues
#     behind them). A qa-g30-* holder or queued ticket REFUSES at once (a live or stale gate-30 ticket).
#   - 32S/40/33L order: ALL three reasons print; the exit code is the SLOT refusal (32) first, then the route (40), then the lock (33). The slot refusal is
#     therefore the answer whenever the kit is unstamped, whatever the other two say. (gate 29 exited 40 first.)
#   - DROPPED: the browser/Chrome/Playwright guard (96) and gate 27's browser instruments; the SQL-spy/templates/riskSql blob guards; the C-57 and C-133
#     runner pins (91) and the C57 shim; the RD-774 READY copy, the gate-29 ANSWER-20/21/23/24 and every PR #97 file/anchor; gate 22-26 briefs; the
#     belt/ruling-(b)/browser-driver/yield-retirement ruling files (the kit carries no such ruling: the retirement phrases are still REFUSED if present).
#   - KEPT: the lock-tool sha256 pin (3c33f5ae…, 90), T9-mounted refusal (18T), the load rule NOTE, the Laptop-DEV lock base, the sqlite3 prebuild NOTE
#     (offline npm ci + jest still need it), C-192 ls-remote retries, the report-path-exists refusal (report path from the kit's §11 Report line),
#     the live negative-control derivation (38R; builder panes now include Datasec/NexusAI-L7), guard 86, the C-190/C-209 clarification quotes.
#   - 31: instruments BY NAME from gate 27's COMPLETE inst/ (gate 25's qa-applymut.py, qa-lockcheck.py); gate 29 has none yet and is never read; the
#     builder's STATUS must end with the READY line for 49ba21e (its sha256 is NOTEd, not pinned: the builder is idle but the file is a CLAIM).
#   - 12/19/53/71: the kit-declaration lists are REWRITTEN for this kit's own words (rows r0-r9, T0-T5, limits L-B1..L-B6 + L-Y1, sections as the kit names
#     them, tags qa-g30-, G30-<n>/N30-<n>, verdict lines 'B302/PR98: …' and 'LANDING CHECKLIST: PR #98 …', the one NOT TESTED line).
#     The WRONG-list marker test also accepts RELAYED (a legitimate evidence class the kit's item 6 uses).
#   - The PROMPT is rewritten for gate 30 from the KIT (tier 2 through code, rows r0-r9, the PARKED line), not from gate 29.
#
# Identity: exports NexusAI's OWN az/gh dirs (az is NOT used; gh READ-ONLY); CLAUDE_CONFIG_DIR pinned to Tuesday's store.
# --check is READ-ONLY in NexusAI: git read verbs with --no-optional-locks (cat-file, log, merge-base, diff, rev-parse, ls-remote, rev-list, show) and the
# legacy stdout-only merge-tree (no object written, only when main moved); shasum / bash -n / grep over session-tools files; python over `git show`
# output; ls, ps, tmux list-panes, test -e. Writes nothing.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate30.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..99 a guard refused
set -u
CHECK=0
for a in "$@"; do
  case "$a" in
    --check) CHECK=1 ;;
    *) echo "unknown argument: $a" >&2; exit 2 ;;
  esac
done

PH_SLOT='@SL''OT'

QA_DIR='/Volumes/Laptop-DEV/!CODING/Testing Agent MAIN'
TUE='/Volumes/Laptop-DEV/TUESDAY'
BRIEFS="$TUE/2_Project_Files/fleet/qa-agent/briefs"
STAGED="$TUE/2_Project_Files/fleet/briefs_staged"
TBRIEFS="$TUE/2_Project_Files/tuesday/briefs"
BRIEF="$TBRIEFS/2026-10-20_B317_SEAT-G13_nexusai-gate-pr98-tier2.md"
BRIEF27="$BRIEFS/2026-10-18_nexusai-gate27-rd778-xss.md"
BRIEF29="$BRIEFS/2026-10-19_nexusai-gate29-rd774-rd836.md"
TEMPLATE="$TUE/2_Project_Files/fleet/qa-agent/BRIEF_TEMPLATE.md"
ADD25="$TBRIEFS/2026-10-18_gate25_ADDENDUM-1_ref-order.md"
ANS1="$TBRIEFS/2026-10-18_S101O_ANSWER-1_plan-confirmation.md"
CHARTER="$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"
MODELS_JSON="$TUE/0_Brain/dashboard/data/models_latest.json"
SQLITE_RULING="$STAGED/2026-10-05_qa_b14_sqlite3_ANSWER.md"
NOTIFIER_ANS="$STAGED/2026-10-05_qa_gate16_notifier_ANSWER.md"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
NX='/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI'
REPO="$NX/2_Project_Files"
ST="$NX/session-tools"
STATUS_B302="$NX/1_Project_Definition/Briefs/2026-10-20_B302_STATUS.md"
BUILDER_BRIEF="$TBRIEFS/2026-10-20_B302_SEAT-L7_nexusai-test-code-codeql.md"
BUILDER_ADD="$TBRIEFS/2026-10-20_B302_ADDENDUM-1_requeue-behind-s101o.md"
LOCKTOOL="$ST/nexusai-lock.sh"
LOCK_SHA_INST='3c33f5ae58e1be20282467a90b27a23a2de998eedd0e56c03f3c06360031a792'   # RD-821 round 3, INSTALLED — PINNED
T9_VOL='/Volumes/KK_T9_External_HDD'
LOCK_BASE_LAPTOP="$ST/locks-laptop-1017"
LOCKQ_J="$LOCK_BASE_LAPTOP/queue-jest"
CLAR="$NX/1_Project_Definition/CLARIFICATIONS.md"
RPTS="$QA_DIR/projects/nexusai/reports"
B25_INST="$RPTS/2026-10-18-gate25-rd761-rd794-merged/evidence/inst"
B27_DIR="$RPTS/2026-10-18-gate27-rd778"
B27_REPORT="$B27_DIR/report.md"
B27_INST="$B27_DIR/evidence/inst"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"
ROUTE_NAME='QA/NexusAI-gate30'
NPM_CACHE="${HOME}/.npm/_cacache"
PREBUILD="${HOME}/.npm/_prebuilds/0068db-sqlite3-v5.1.7-napi-v6-darwin-arm64.tar.gz"
PREBUILD_SHA='84a34404b12ff212adbca70eff76c2e4dd83b91245eed0b4569438f928567afc'

# ---- the pins (cross-checked against the kit's PIN-HEADS, guard 40; each MEASURED 2026-10-20 by read verbs)
BASE='39653db4b56adb6d4e526c90531cd4cdf23022e0'; BASE_TREE='704c442b78a36baea66fef2349a5acbdbff114b5'   # main at drafting (the PR's base)
BR='b302/test-code-codeql'
HEAD_SHA='49ba21e101f3ce6dd75ae5dbeb1e37aae566d9a6'; HEAD_TREE='8a1150466dcdfe77ade6211e3e08325e6df0f223'  # the head (RD-787, commit 8 of 8)
PR_REF='refs/pull/98/head'
# the chain, oldest first: <full sha> <tree> (each commit's parent is the previous row; row 1's parent is BASE)
CHAIN='cb8755a25b2e62e5d664f9f9a10de1a11a3cd4bf e21bea8a18c8a792b1379ce352e53c47bd507554
342afeddbe3c8a8c69f56a7fa8c01d37ca892a0c 2708703f02dd7b1d839528152ff0dce964d562ae
b6cb5ec3dd72837a8913d7fd49e1e3b3fe422a2d 9d55a439f762091fc67fc1592b2709f7953dfc4b
56e1b614613aa5252ce78347edb83a0a162cb526 ce59bdaa12131dd883274d0cd5389b4774888e21
198ef3413fa589981c16db1ae18f45db9812e23b cac62316c91479d382e83b0b2702ab0b22dfb272
8bb6c339ea86b4534ee083f4246335ddef57919d 6e6c35186d6318fd46e47e993bc236d4cdcef5bc
017cf69588d5ffe60a9d7960991e4b7366b4359b a6bd909e5162ad3be78adca2e6d647e8dad4fbec
49ba21e101f3ce6dd75ae5dbeb1e37aae566d9a6 8a1150466dcdfe77ade6211e3e08325e6df0f223'
PATHS_SHA='97161ee5c2ae3bb5dc4fc6c646d571b3b9150b340fb1f411990437e652aa03b5'   # sha256 of the sorted, space-joined 34-path list (git diff --name-only BASE HEAD)
NEW_HELPER='__tests__/helpers/html-dom.js'; HELPER_BLOB='a151c746f59a53a98dc32de701231e093d8710fd'
COUNTS_FILE='scripts/verify-expected-counts.json'; COUNTS_BLOB='2cc094855c1215299ac15373262241dd71c64bff'
PKG='package.json'; PKG_BLOB='384805d9e286718bb34ffd05be01c62c00806cf5'
LOCK='package-lock.json'; LOCK_BLOB='19477a9329f17e529c208d91d172b95b47fc1bb5'
DEPLOY_WF='.github/workflows/deploy-demo.yml'; DEPLOY_BLOB='953b2a2f84e8710bea857ec87c6f00faa50fa56b'
GUARDED_RE='^(backend/|static/|templates/|package\.json$|package-lock\.json$|\.github/|bicep/|Dockerfile$|scripts/verify-expected-counts\.json$)'
TESTCODE_RE='^(__tests__/|tests/|scripts/test-[^/]*\.js$)'
# the files of the five open RD-786 sites (#95-#99): byte-UNCHANGED base..head (kit WRONG 1)
RD786_OPEN='__tests__/erasure-reaches-every-read-location.test.js __tests__/erasure-verdict-is-derived-from-failures.test.js __tests__/initialize-files-uses-shared-recovery-list.test.js __tests__/helpers/rd407-setting-writer.js'
NEG_SEATS=''   # 38R: DERIVED at launch from the live cockpit panes — never stamped by hand

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — gate 30'
QUESTION_SUBJ='[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>'
STATUS_SUBJ='[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch'
PARK_LINE='PARKED: flagged — awaiting the Opus 4.8 switch'
ANSWER_PREFIX='[Tuesday -> QA/NexusAI-gate30] ANSWER'
SAFE_PRINTER='if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET (length ${#SESSION_SECRET})"; else echo "SESSION_SECRET UNSET"; fi'

g() { git --no-optional-locks -C "$REPO" "$@"; }
counts_blob() { g cat-file -p "$1" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
counts_at() { counts_blob "$(g rev-parse --verify -q "${1}:${COUNTS_FILE}" 2>/dev/null)"; }
blob() { g rev-parse --verify -q "${1}:${2}" 2>/dev/null; }
cntF() { g show "${1}:${2}" 2>/dev/null | grep -cF -- "$3"; }
fsha() { shasum -a 256 "$1" 2>/dev/null | cut -d' ' -f1; }
tree_of() { g rev-parse --verify -q "${1}^{tree}" 2>/dev/null; }
parents_of() { g log -1 --format='%P' "$1" 2>/dev/null; }
paths_of() { g diff --name-only "$1" "$2" 2>/dev/null | sort | tr '\n' ' ' | sed 's/ $//'; }
# the LEGACY stdout-only merge-tree (trivial-merge mode; writes NO object; never --write-tree in the NexusAI repo): prints the paths whose section
# carries conflict markers, space-separated.
mt_conflicts() { g merge-tree "$1" "$2" "$3" 2>/dev/null | python3 -c '
import sys,re
heads=("changed in both","added in remote","added in local","removed in remote","removed in local","merged","added in both","removed in both")
cur=None; out={}
for ln in sys.stdin.read().split("\n"):
    if ln.strip() in heads and not ln.startswith((" ","+","-","@")):
        cur={"p":set(),"c":False}; out[id(cur)]=cur; continue
    if cur is None: continue
    m=re.match(r"^  (base|our|their|result|both)\s+\d+\s+[0-9a-f]+\s+(.*)$",ln)
    if m: cur["p"].add(m.group(2))
    if ln.startswith(("+<<<<<<<","+>>>>>>>")): cur["c"]=True
print(" ".join(sorted(p for s in out.values() if s["c"] for p in s["p"])))' 2>/dev/null; }
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

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE gate on Datasec/NexusAI, gate 30: a TIER-2 GATE THROUGH CODE, ROUND 1 of 2, ONE verdict per ticket, one overall, ONE report. It is a FRESH gate on Kam's Mac mini, working volume /Volumes/Laptop-DEV; the T9 drive is UNMOUNTED, so the project's jest lock lives on this drive's locks-laptop-1017 base. The item: B302 lane 7, RD-782, RD-783, RD-784, RD-785, RD-786 (partial), RD-787, RD-788, RD-789 (CodeQL alerts in TEST code), branch b302/test-code-codeql at 49ba21e101f3ce6dd75ae5dbeb1e37aae566d9a6 (tree 8a1150466dcdfe77ade6211e3e08325e6df0f223), draft PR #98 by the builder seat SEAT-L7: eight commits over main 39653db4b56adb6d4e526c90531cd4cdf23022e0 (tree 704c442b78a36baea66fef2349a5acbdbff114b5), oldest first cb8755a (RD-789), 342afed (RD-784), b6cb5ec (RD-785), 56e1b61 (RD-788), 198ef34 (RD-782), 8bb6c33 (RD-783), 017cf69 (RD-786) and 49ba21e (RD-787); 34 paths, 33 modified and ONE new helper (the new html-dom helper under the tests' helpers), every one test code or test tooling, NO product file. M0 is the main Tuesday STAMPED (the launcher verified origin main equals it; sha, tree and the T0 mode are at the end of this prompt): in mode 0 (M0 = 39653db) the gated tree IS the head. Never trust the builder's logs, probes, scan or counts as the proof; every line of the builder's STATUS is a CLAIM, RELAYED, never evidence. FINDINGS-ONLY: you NEVER merge anything the fleet can see, NEVER push, NEVER open, comment on, approve, un-draft or merge a pull request, never comment on Jira, never dismiss an alert, and NEVER swap, copy over or edit the installed lock tool; no fixes, no deploys, no az, no docker, no model call of any kind, no production, no HTTP to any production or demo host, nothing to Partner Center, the demo or any human, no host npm registry. One client only: Datasec/NexusAI.

READ YOUR COMMISSION FIRST, whole: /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-20_B317_SEAT-G13_nexusai-gate-pr98-tier2.md
It opens with the item, the builder's READY STATUS (read WHOLE; its section UPDATE after ADDENDUM-1 supersedes its BLUF), Tuesday's rulings Q1 to Q4, THE RE-PIN STEP, the stamp lines, PIN-HEADS, the TIER argument (the case AGAINST: a test fix can hide a product defect by making a test weaker, and CodeQL's rule is syntactic, so a fix can satisfy the rule without removing the data flow, a REPHRASE), the legitimate shapes of the host, URL and anchor checks, the drafter's WRONG OR UNVERIFIED list (each item MEASURED or READ-ONLY-INFERRED), then TUESDAY'S RULINGS (T0 to T5 as Tuesday stamped them) and THE MODEL RULE: apply them, do not re-rule them. Then the charter it names, BRIEF_TEMPLATE section 2a, 5 and 6a, and gate 29's section 3a (the H-rules, carried by reference, except what is about docker, server boots, browsers, SQL spies or the C-57 runner). The brief's section 2b rows (r0 to r9), section 3b (the sweep) and section 9 (the floor) are required measurement. The verdict is PROVISIONAL if r1 (alert by number), r3 (the tests did not get weaker) or r5 (the adjudications) did not run.

THE MODEL RULE (Kam, live board 2026-09-30 09:07, card (b)): QA gates may switch to Opus 4.8 when flagged by the running model's safeguards, PER SESSION. You start on the model named at the end of this prompt (Sonnet 5.5). This is a Sonnet seat and none of the rows composes exploit payloads (the plants are inert markup strings and a lookalike hostname). If one of your responses is stopped by the safeguards anyway: that step is NOT RUN (never re-worded to slip past); write ONE line to evidence/classifier-stops.txt (the AEDT time, the row, what you were composing, the model, NOT RUN); let any running step finish and let the hold exit so you never sit holding a lock (H-28); mail tuesday-agent@agentmail.to with the subject exactly "[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch"; then end your turn with the line "PARKED: flagged — awaiting the Opus 4.8 switch" and wait. Tuesday switches THIS pane's model to Opus 4.8 and taps you by mail. You never answer the model dialog yourself, and nobody ever chooses "Switch automatically". After the switch, resume at the stopped row. The report states which rows ran on which model, with the switch time, and quotes classifier-stops.txt whole.

THE PROPERTIES (brief section 2b and the commission). (1) SCOPE: 34 files, all test code, 0 product, backend, static, package, workflow or counts-file path (r0, with a planted-path control). (2) EACH ALERT'S FIX IS REAL OR NAMED A REPHRASE: r1 reads EVERY one of the 68 alert numbers (gh api, rule, severity, the instance's path, line and message; then the changed hunk at that path) and labels it REAL, REPHRASED, NOT FIXED (the five RD-786 sites #95 to #99, byte-unchanged at the head) or CAN'T TELL, writing the FAIL condition before each; the dual-rule lines (one line, two alerts) are reported per alert, not per commit. (3) CODEQL (r2, gh READ): every analysis for 49ba21e listed and COMPLETED, 0 open on refs/pull/98/head, which closed-by-number alerts read fixed on the PR ref (expected none: C-209 is not a finding), with PR #96's fixed list as the firing control, and the check runs' conclusions incl. build, scan and audit-production-deps. (4) THE TESTS DID NOT GET WEAKER (r3): the names multiset of every changed jest suite plus the dom helper's consumers at BASE and HEAD (LOST 0, ADDED 0), no skip, only, todo or timeout token added, assertion counts per changed file and per test by TWO instruments, and EVERY edited assertion read and labelled SAME, STRONGER or WEAKER with a planted input (a WEAKER is a Major). (5) THE BUILDER'S MUTANTS RE-CHECKED plus a strength mutant per mechanism (r4, A to D2 and S1 to S7; a strength mutant no cell kills is an assertion with no teeth, a Major). (6) THE ADJUDICATIONS (r5) of the RD-784, RD-785 and RD-788 deviations, the RD-788 commit subject and the five open RD-786 sites, each with a recommendation for Tuesday and its evidence class. (7) THE DOM PROOF (r6) for RD-782 and RD-783 re-derived independently. (8) LANDING hygiene (r8, r9): gitleaks, deploy-demo, the lockfile equal to M0's, no overlap with PR #97 and #67, and the builder's STATUS claims VERIFIED, FALSE or UNVERIFIED (C-49). The smoke scripts are r7. Findings only, never fixes.

MAIN MUST NOT MOVE: the launcher verified origin main equals the stamped MAIN pin exactly, that 39653db is in its ancestry, that its tree equals the stamped tree, and that the head is not on it; take M0 by git ls-remote at YOUR start and say so. If main moves mid-gate (PR #97 from S101O is the likeliest mover), name what landed (git log with explicit revs), finish nothing that would read as a verdict on the new main, and mail a QUESTION (C-68). GitHub SSH intermittently denies auth (C-192): retry every ls-remote up to 5 times about 10 s apart; a FAILED ls-remote is UNKNOWN, never a value. Re-hash the lock tool at start, mid and end.

C-190 + its ADDENDUM: BOTH thresholds block: every merge to main goes through a pull request that adds no new high-or-higher CodeQL alert in changed code (test code included), AND any new alert whose RULE severity is error blocks whatever its security severity. Alerts are fixed in code, never dismissed. C-209: a PR's CodeQL run cannot show a pre-existing main alert as fixed. CodeQL is NOT RUN by this gate on any tree: say so; closure of the 63 alerts is read by Tuesday on main after the land.

THE LOCK (C-63). The installed tool is session-tools/nexusai-lock.sh in the NexusAI project on this drive, sha256 3c33f5ae58e1be20282467a90b27a23a2de998eedd0e56c03f3c06360031a792. While the T9 is unmounted the base is NEXUSAI_LOCK_BASE=/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/session-tools/locks-laptop-1017, which the launcher has EXPORTED into your environment: keep it on every jest step and never touch this drive's stale session-tools/locks (a 2026-09-22 holder lives there). THE JEST LOCK IS NOT YOURS: at drafting S101O held it for PR #97's verify; you QUEUE behind it FIFO through the INSTALLED tool (never copied, never edited), never touch the holder, its owner file, its process or its worktree, and never use --replace on a ticket that is not your own. If the T9 mounts mid-gate, finish the running hold, file nothing more, and mail a QUESTION. EVERY jest run and every smoke script goes in the jest lock, each hold tagged qa-g30- (no tag of yours contains the word "merge": C-141 ADDENDUM 7), ONE hold at a time. MERGES GO FIRST: if a ticket is queued ahead of you, wait behind it (FIFO). AT A WAIT DEADLINE: --replace on your own still-waiting ticket BEFORE its deadline fires (a SAME-PLACE handover), confirmed from the queue listing; a duplicate-tag refusal takes a -r<N> suffix. Read queue-jest at start, around every hold and at end; any qa-g30- entry that is not your current hold is a STOP. THE LOAD RULE: file a hold, start any full jest or smoke run only below a 1-minute load of 8 (8 cores; Tuesday's ANSWER-1 to S101O); record uptime beside each; over 8, poll every 20 s and log each wait.

NODE_MODULES WITHOUT THE HOST REGISTRY (ruling m, H-31): offline npm ci --offline --ignore-scripts --no-audit --no-fund with --cache pointing at an APFS clone of the local npm cache on the same volume; M0 and the head share lock 19477a9, so ONE proven install is APFS-cloned into the others (never copy node_modules from any checkout or worktree); EVERY npm invocation carries npm_config_update_notifier=false; an ENOTCACHED is NOT RUN, named, with a QUESTION: never go online from the host, never npm install. sqlite3's binding from the cached prebuild (an APFS clone of ~/.npm/_prebuilds), with its conditions, is PART OF H-31.

FLOOR DISCIPLINE (brief section 9): do ALL lock-free work first (r0, r1, r2, r3 (ii) and (iv), r4's S7, r5, r6, r8, r9, the offline npm ci, the self-tests); then file your holds one at a time through your COPY of gate 27's qa-file27.sh re-pointed to qa-g30 tags and the jest kind only (its diff against gate 27's quoted): H1a, H1b, H2 and H3 as the brief groups them, each at most about 40 minutes planned, each part file bash -n checked first. The full 4880-test verify is NOT RUN under T1 as stamped unless Tuesday ruled (b); if ruled and lock-starved about 2 h after filing, it is NAMED NOT RUN under ruling (o) EXTENDED, never "skipped". QUEUE, NEVER TAKE OVER. DEADLINE AND HEARTBEAT: every step has a per-step DEADLINE (H-20), every child is killed in a finally by pid from your own ancestry (C-174, never by pattern), a HEARTBEAT line at least every 2 minutes during a hold, and a step with no heartbeat for 5 minutes is aborted and reported. Count foreign processes the C-125 way anchored on YOUR OWN claude pid, with the negative-control seats the launcher derived (listed at the end of this prompt) classifying foreign in the same run; a hold with no live negative control aborts. A zero is reportable only beside a control that fired in the same window.

THE INSTRUMENT RULES H-1 TO H-36 (brief section 3a; gate 29's section 3a read WHOLE). H-1: the ONLY SESSION_SECRET printer is the one the brief quotes (SESSION_SECRET UNSET on every host run). H-3: a LANDING CONTROL for every plant, revert and mutant. H-4: the HEARTBEAT is a separate child of the hold wrapper. H-6: every path with a space quoted; jest and smoke runs under your copy of the network belt. H-7/H-8/H-21: every mutant by a quoted tool with a negative control, an edit whose anchor is absent FAILS LOUDLY, every file you mutate restored by a trap on EXIT (also INT and TERM) installed BEFORE the first mutation and hash-compared to its pin. H-11/H-18: /bin/bash explicitly, quote "${sha}:${path}" and never type cd. H-14: every driver ends END ok or END VOID with a reason. H-17: censuses by pgrep. H-20: deadlines on every jest run (with --forceExit). H-24: jest array options after the paths. H-27: THE MODEL RULE. H-28: ONE focused hold at a time, you stay in the FOREGROUND, a hold that must outlive one tool call runs as a TRACKED child of your session (never nohup). H-29: other gates' and the builder's evidence is method only (the builder's session-tools files are read and hashed at start and end, never run in place, never written to). H-31: offline host node_modules. H-33: never rm, quarantine; every child reaped by pid. H-34: the Laptop-DEV lock base. H-35: NO docker object and NO az command, and NO call to any real model. A revert, plant or mutant counts only if it LANDED (the exact text present, the original absent) and parses; a planted control that does not fire makes its row VOID (never a pass).

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT (fresh dirs under projects/nexusai/qa-trees/gate30.* in /Volumes/Laptop-DEV/!CODING/Testing Agent MAIN): ONE --mirror clone of the NexusAI repo on THIS drive as your store with gc.auto 0, your refs g30/* in it made BEFORE origin is removed (gate 25 ADDENDUM-1: g30/m0, g30/b302, g30/c1 to g30/c8, g30/base), every work tree a clone of that store, status-checked before use, EXCLUSIVE to one purpose (BASE, HEAD, one per mutant set). NEVER work in the NexusAI root checkout or any worktrees folder (LIVE: the builder's and S101O's). In the NexusAI repo use ONLY read verbs (show, diff, log with an explicit rev, ls-tree, cat-file, grep, ls-remote, rev-parse, merge-base, rev-list, count-objects, for-each-ref); NEVER fetch, pull, push, checkout, worktree, commit, stash, gc, merge, merge-tree --write-tree or hash-object -w there. Copy instruments BY NAME from gate 27's COMPLETE evidence/inst and gate 25's qa-applymut.py (never the whole directory; gate 29 has none yet and is never read), re-point every gate-27 path in your copies to gate 30 including the lock base line (quote that diff); never write into another gate's dirs. Count the NexusAI .git/objects files and their newest mtime at start and end and account for any delta (S101O is live). No Microsoft, Log Analytics or login host, no mail host except api.agentmail.to, no demo, no Partner Center, no workflow dispatch, no repo variable written. tests/uat-run.js is NEVER executed (its default target is the demo) and the tests/e2e files are NEVER run: node --check and a READ only. No mail to any human. Never rm: quarantine.

RE-PIN at start, mid and end: main, b302/test-code-codeql and refs/pull/98/head by git ls-remote, plus the lock tool's sha256: three timestamped readings with the branch name and attempt count beside each sha. A head that disagrees with the brief is a FINDING and a reason to stop, never a typo to fix. Call main at your start M0 and say so.

QUESTIONS: your routing name is QA/NexusAI-gate30. If you must ask, mail tuesday-agent@agentmail.to with subject "[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>" and PROCEED ON THE SAFEST READING without waiting (the one exception is a safeguards stop, which PARKS you under THE MODEL RULE); Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/NexusAI-gate30] ANSWER". Approval-class items (anything Azure, any real model call, the demo, Partner Center, money, a human, the live lock tool beyond queueing) are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your ONE report to the path the launcher names at the end of this prompt (the brief's section 11). Write its VERDICT and FINDINGS table early and keep it current; line 3 is STATUS: IN PROGRESS or COMPLETE with the date. Findings are G30-<n>, notes N30-<n>, each naming its instrument and evidence class.

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with the subject exactly:
[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — gate 30
Lead the body with the TWO lines in the form the brief's section 11 gives — the B302/PR98 verdict line (overall and per ticket) and the LANDING CHECKLIST line — then one line naming M0 and END main, the C-102 sweep, which rows ran on which model, which holds ran and which are NAMED NOT RUN, and "CodeQL NOT RUN by this gate on any tree". The report's last two lines are those same two lines, verbatim as mailed. Never wednesday-agent@. You have no inbox that wakes you, so a verdict you do not mail is lost.
The AgentMail key is AGENTMAIL_API_KEY in /Volumes/Laptop-DEV/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no 4_Credentials directory of its own. Never put the key, a token, a session value or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice: the only turn you end while waiting is the PARKED line of THE MODEL RULE.

Rule 2 stands: what you did NOT test is first-class output: a NOT TESTED section carrying the builder's stated limits, every declared limit L-B1 to L-B6 and L-Y1 discharged with a measurement or left standing and named (C-112), Prior work checked (C-49), every finding naming its instrument, and every action recommendation labelled MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. The tester never fixes. C-190 with its ADDENDUM, C-209, C-185, C-192, C-205, C-141 with ADDENDUM 7, C-63, C-40, C-68, C-76, C-102, C-112 and C-174 are the clarifications this gate leans on; C-49, C-89, C-115, C-125, C-130 and C-131 are carried. That section must carry, verbatim, the NOT TESTED line the launcher appends at the end of this prompt (it is the brief's section 11 line).
PROMPT_EOF

# ---------------------------------------------------------------- GUARDS
[ -d "$QA_DIR" ]  || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]   || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -n "$PROMPT" ]  || { echo "embedded prompt is empty" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }

STAMP_OK=1          # cleared below by any unstamped slot the guards meet; the refusal itself is LAST (32S)
LOCK_OK=1           # cleared below while a gate-29 ticket HOLDS the jest lock; the refusal itself is LAST (33L)
LOCK_WHY=''
PROVISIONAL=''      # what --check ran against provisionally while a slot was unstamped

# 9 / MODEL — the kit's MODEL line must equal models_latest.json levels.sonnet.model_id (tier 2, Sonnet); never typed from memory.
MODEL_LINE="$(grep -E '^MODEL \(tier 2;' "$BRIEF" | head -1)"
[ -n "$MODEL_LINE" ] || { echo "REFUSING: the brief has no 'MODEL (tier 2; …' line" >&2; exit 9; }
SONNET_ID="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["levels"]["sonnet"]["model_id"])' "$MODELS_JSON" 2>/dev/null)"
[ -n "$SONNET_ID" ] || { echo "REFUSING: $MODELS_JSON levels.sonnet.model_id is unreadable" >&2; exit 9; }
MODEL="$(printf '%s' "$MODEL_LINE" | sed -E 's/.*: *`?([a-z0-9.-]+)`? *$/\1/')"
[ "$MODEL" = "$SONNET_ID" ] || { echo "REFUSING: the kit's MODEL '$MODEL' is not models_latest.json levels.sonnet.model_id '$SONNET_ID' — re-stamp the MODEL line from the file" >&2; exit 9; }

# 40 — parse PIN-HEADS (the ONLY source of heads) and cross-check against this launcher's pins; the MAIN row and the MAIN-STAMP line agree.
parse_block() { python3 - "$BRIEF" "$1" <<'PY'
import sys, re
s = open(sys.argv[1], encoding='utf-8').read(); name = sys.argv[2]
m = re.search(r'<!-- %s:BEGIN -->(.*?)<!-- %s:END -->' % (name, name), s, re.S)
if not m:
    print('NO-BLOCK'); sys.exit(0)
for line in m.group(1).splitlines():
    line = line.strip()
    if not line.startswith('|') or line.startswith('| id ') or set(line) <= set('|-: '):
        continue
    print('\t'.join(c.strip().strip('`') for c in line.strip('|').split('|')))
PY
}
PIN="$(parse_block PIN-HEADS)"
[ "$PIN" != "NO-BLOCK" ] && [ -n "$PIN" ] || { echo "REFUSING: the brief has no PIN-HEADS block — the heads have nowhere to come from" >&2; exit 40; }
prow() { printf '%s\n' "$1" | awk -F'\t' -v id="$2" '$1==id'; }
pfld() { prow "$1" "$2" | awk -F'\t' -v n="$3" '{print $n}'; }
is40()  { printf '%s' "$1" | grep -Eq '^[0-9a-f]{40}$'; }
[ "$(printf '%s\n' "$PIN" | wc -l | tr -d ' ')" = "2" ] || { echo "REFUSING: PIN-HEADS must carry exactly two rows (MAIN B302)" >&2; exit 40; }
for ID in MAIN B302; do
  R="$(prow "$PIN" "$ID")"
  [ "$(printf '%s\n' "$R" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: PIN-HEADS must carry exactly one row '$ID'" >&2; exit 40; }
  [ "$(printf '%s\n' "$R" | awk -F'\t' '{print NF}')" = "7" ] || { echo "REFUSING: PIN-HEADS row $ID does not have 7 cells: $R" >&2; exit 40; }
  [ "$(pfld "$PIN" "$ID" 7)" = "IN" ] || { echo "REFUSING: PIN-HEADS row $ID status is not IN" >&2; exit 40; }
  [ "$(pfld "$PIN" "$ID" 2)" = "nexusai" ] || { echo "REFUSING: PIN-HEADS row $ID repo must be nexusai" >&2; exit 40; }
done
printf '%s' "$(prow "$PIN" B302)" | grep -q '@' && { echo "REFUSING: PIN-HEADS row B302 still carries a placeholder" >&2; exit 40; }
[ "$(pfld "$PIN" B302 3)" = "$BR" ] && [ "$(pfld "$PIN" B302 4)" = "$HEAD_SHA" ] && [ "$(pfld "$PIN" B302 5)" = "$BASE" ] && [ "$(pfld "$PIN" B302 6)" = "8" ] \
  || { echo "REFUSING: PIN-HEADS B302 is not $BR @ 49ba21e, base 39653db (main at drafting), 8 commits — re-pin kit AND launcher" >&2; exit 40; }
[ "$(pfld "$PIN" MAIN 3)" = "main" ] || { echo "REFUSING: PIN-HEADS MAIN row is not branch main" >&2; exit 40; }
PIN_MAIN="$(pfld "$PIN" MAIN 4)"
STAMP_LINE="$(grep -E '^MAIN-STAMP: ' "$BRIEF")"
[ "$(printf '%s\n' "$STAMP_LINE" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: the brief must carry exactly one 'MAIN-STAMP: ' line" >&2; exit 40; }
MAIN_STAMPED=1; S_LANDED=''
if printf '%s' "$STAMP_LINE$PIN_MAIN" | grep -qF "$PH_SLOT"; then
  MAIN_STAMPED=0; STAMP_OK=0
else
  STAMP_RE='s/^MAIN-STAMP: sha `?([0-9a-f]{40})`? \| tree `?([0-9a-f]{40})`? \| landed since 39653db4: (.+)$/'
  S_SHA="$(printf '%s' "$STAMP_LINE" | sed -nE "${STAMP_RE}\\1/p")"
  S_TREE="$(printf '%s' "$STAMP_LINE" | sed -nE "${STAMP_RE}\\2/p")"
  S_LANDED="$(printf '%s' "$STAMP_LINE" | sed -nE "${STAMP_RE}\\3/p")"
  is40 "$S_SHA" && is40 "$S_TREE" && [ -n "$S_LANDED" ] || { echo "REFUSING: the MAIN-STAMP line is not 'MAIN-STAMP: sha <40-hex> | tree <40-hex> | landed since 39653db4: <text>'" >&2; exit 40; }
  [ "$PIN_MAIN" = "$S_SHA" ] || { echo "REFUSING: PIN-HEADS MAIN ($PIN_MAIN) and the MAIN-STAMP sha ($S_SHA) disagree — stamp the same sha in both" >&2; exit 40; }
fi

# 18T — the T9 MOUNTED refuses: two lock bases would split the FIFO (ruling q); Tuesday decides the base first.
[ ! -d "$T9_VOL" ] || { echo "REFUSING: $T9_VOL is MOUNTED — the brief's lock base (locks-laptop-1017) assumes it is not; Tuesday decides the base, then re-brief" >&2; exit 18; }

# 18 — RE-PIN NOW by ls-remote (C-192 retries): main = the stamped MAIN pin EXACTLY; the branch AND the PR ref = the head pin.
lsr refs/heads/main "refs/heads/$BR" "$PR_REF" \
  || { echo "REFUSING: git ls-remote origin failed after $LSR_ATTEMPTS attempt(s) — UNKNOWN, not a value (C-192); relaunch later" >&2; exit 18; }
LSR_ALL="$LSR_OUT"
ref_now() { printf '%s\n' "$LSR_ALL" | awk -v r="$1" '$2==r{print $1}'; }
M_ORIGIN="$(ref_now refs/heads/main)"
is40 "$M_ORIGIN" || { echo "REFUSING: origin main is unreadable in the ls-remote output — UNKNOWN (C-192)" >&2; exit 18; }
if [ "$MAIN_STAMPED" = "1" ]; then
  [ "$M_ORIGIN" = "$S_SHA" ] || { echo "REFUSING: origin main is '${M_ORIGIN:0:12}', not the stamped MAIN pin '${S_SHA:0:12}' — main MOVED since stamp; re-stamp the MAIN pin (never sed a sha blindly)" >&2; exit 18; }
  MAIN_SHA="$S_SHA"
else
  MAIN_SHA="$M_ORIGIN"; PROVISIONAL="$PROVISIONAL MAIN(unstamped: guards ran against origin main ${M_ORIGIN:0:12})"
fi
[ "$(ref_now "refs/heads/$BR")" = "$HEAD_SHA" ] || { echo "REFUSING: origin $BR is '$(ref_now "refs/heads/$BR")', not 49ba21e — the head MOVED; re-pin kit AND launcher (a new head is a new kit amendment and a new CodeQL run)" >&2; exit 18; }
[ "$(ref_now "$PR_REF")" = "$HEAD_SHA" ] || { echo "REFUSING: $PR_REF is '$(ref_now "$PR_REF")', not 49ba21e — PR #98 moved (or the ref is unreadable); re-pin kit AND launcher" >&2; exit 18; }
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 6 — every sha the guards use is a commit in the local object store (this launcher never fetches).
CHAIN_SHAS="$(printf '%s\n' "$CHAIN" | awk '{print $1}')"
for S in "$MAIN_SHA" "$BASE" $CHAIN_SHAS; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: ${S:0:12} is not a commit in $REPO (got '$T') — this launcher never fetches; the seat's next fetch brings it, then re-check" >&2; exit 6; }
done

# 18M — M0 by ANCESTRY (never --first-parent) + trees; M0's tree = the stamp; the head and its chain NOT on M0; the mode.
[ "$(tree_of "$BASE")" = "$BASE_TREE" ] || { echo "REFUSING: 39653db is not tree 704c442 (the measured main)" >&2; exit 18; }
g merge-base --is-ancestor "$BASE" "$MAIN_SHA" 2>/dev/null || { echo "REFUSING: 39653db is not in M0 ${MAIN_SHA:0:7}'s ANCESTRY — M0 is not a descendant of the measured main 39653db" >&2; exit 18; }
M0_TREE="$(tree_of "$MAIN_SHA")"
if [ "$MAIN_STAMPED" = "1" ]; then
  [ "$M0_TREE" = "$S_TREE" ] || { echo "REFUSING: M0 ${MAIN_SHA:0:7}'s tree is '${M0_TREE:0:12}', not the stamped tree '${S_TREE:0:12}'" >&2; exit 18; }
fi
for S in $CHAIN_SHAS; do
  if g merge-base --is-ancestor "$S" "$MAIN_SHA" 2>/dev/null; then echo "REFUSING: PR #98 commit ${S:0:7} is ALREADY on M0 ${MAIN_SHA:0:7} — it landed before its gate; re-brief" >&2; exit 18; fi
done
LANDED_N="$(g rev-list --count "${BASE}..${MAIN_SHA}" 2>/dev/null)"
if [ "$MAIN_SHA" = "$BASE" ]; then
  MODE='0'
  if [ "$MAIN_STAMPED" = "1" ] && [ "$(printf '%s' "$S_LANDED" | tr '[:upper:]' '[:lower:]')" != "none" ]; then echo "REFUSING: M0 is 39653db but the MAIN-STAMP names something landed ('$S_LANDED') — stamp 'none'" >&2; exit 18; fi
else
  MODE='moved'
  echo "NOTE: M0 ${MAIN_SHA:0:7} is $LANDED_N commit(s) past 39653db — what landed: $(g log --format='%h %s' "${BASE}..${MAIN_SHA}" 2>/dev/null | head -5 | cut -c1-90 | tr '\n' ';') — T0 applies" >&2
  if [ "$MAIN_STAMPED" = "1" ] && [ "$(printf '%s' "$S_LANDED" | tr '[:upper:]' '[:lower:]')" = "none" ]; then echo "REFUSING: M0 is not 39653db but the MAIN-STAMP says 'landed since 39653db4: none' — name what landed" >&2; exit 18; fi
  OVERLAP="$(comm -12 <(g diff --name-only "$BASE" "$MAIN_SHA" 2>/dev/null | sort) <(g diff --name-only "$BASE" "$HEAD_SHA" 2>/dev/null | sort) | tr '\n' ' ' | sed 's/ $//')"
  [ -z "$OVERLAP" ] || { echo "REFUSING: what landed since 39653db touches PR #98 path(s) '$OVERLAP' — T0: STOP and mail a QUESTION; re-brief" >&2; exit 18; }
  MB_M0="$(g merge-base "$MAIN_SHA" "$HEAD_SHA" 2>/dev/null)"
  GD0="$(g rev-parse --absolute-git-dir 2>/dev/null)"; OB0="$(find "$GD0/objects" -type f 2>/dev/null | wc -l | tr -d ' ')"
  MC0="$(mt_conflicts "$MB_M0" "$MAIN_SHA" "$HEAD_SHA")"
  OA0="$(find "$GD0/objects" -type f 2>/dev/null | wc -l | tr -d ' ')"
  [ -z "$MC0" ] || { echo "REFUSING: the legacy merge-tree of 49ba21e onto M0 shows conflict markers in '$MC0' — T0: STOP; re-brief" >&2; exit 18; }
  [ "$OB0" = "$OA0" ] || echo "NOTE: NexusAI .git/objects went $OB0 -> $OA0 around the legacy merge-tree read — the trivial-merge mode writes none; a live seat may have" >&2
fi

# 7 / 8 — the head's chain: 39653db <- eight commits, oldest first, each parent = the previous row, EVERY tree; linear; the head tree.
PREV="$BASE"
while read -r CSHA CTREE; do
  [ -n "$CSHA" ] || continue
  [ "$(parents_of "$CSHA")" = "$PREV" ] || { echo "REFUSING: the parent of ${CSHA:0:7} is '$(parents_of "$CSHA")', not ${PREV:0:7} — the chain is not the briefed 8 linear commits" >&2; exit 7; }
  [ "$(tree_of "$CSHA")" = "$CTREE" ] || { echo "REFUSING: ${CSHA:0:7}'s tree is not ${CTREE:0:7}" >&2; exit 8; }
  PREV="$CSHA"
done <<EOF_CHAIN
$CHAIN
EOF_CHAIN
[ "$PREV" = "$HEAD_SHA" ] && [ "$(tree_of "$HEAD_SHA")" = "$HEAD_TREE" ] \
  || { echo "REFUSING: the chain does not end at 49ba21e tree 8a11504" >&2; exit 8; }
[ "$(g merge-base "$HEAD_SHA" "$BASE" 2>/dev/null)" = "$BASE" ] && [ "$(g rev-list --count "${BASE}..${HEAD_SHA}" 2>/dev/null)" = "8" ] \
  && [ "$(g rev-list --count --first-parent "${BASE}..${HEAD_SHA}" 2>/dev/null)" = "8" ] \
  || { echo "REFUSING: 49ba21e is not 8 linear commits over 39653db (merge-base, count, first-parent count)" >&2; exit 8; }

# 90 — the INSTALLED lock tool PINNED; it honours NEXUSAI_LOCK_BASE; the Laptop-DEV base is present with queue-jest; no qa-g30 ticket; gate 29 HOLDING defers.
INST_NOW="$(fsha "$LOCKTOOL")"
[ "$INST_NOW" = "$LOCK_SHA_INST" ] || { echo "REFUSING: the INSTALLED lock tool's sha256 is '${INST_NOW:-absent}', not 3c33f5ae… — find out who changed it; re-brief" >&2; exit 90; }
grep -qF 'BASE="${NEXUSAI_LOCK_BASE:-' "$LOCKTOOL" || { echo "REFUSING: the installed tool no longer honours NEXUSAI_LOCK_BASE — ruling q's premise" >&2; exit 90; }
bash -n "$LOCKTOOL" 2>/dev/null || { echo "REFUSING: $LOCKTOOL does not parse (bash -n)" >&2; exit 90; }
grep -qF -- '--replace' "$LOCKTOOL" && grep -qF 'jest|docker) ;;' "$LOCKTOOL" || { echo "REFUSING: $LOCKTOOL lacks --replace or the jest kind" >&2; exit 90; }
[ -d "$LOCK_BASE_LAPTOP" ] && [ -d "$LOCKQ_J" ] || { echo "REFUSING: the Laptop-DEV lock base $LOCK_BASE_LAPTOP (queue-jest) is not present (ruling q)" >&2; exit 90; }
BQ="$(grep -l '^tag=qa-g30' "$LOCKQ_J"/* 2>/dev/null | wc -l | tr -d ' ')"
[ "${BQ:-0}" = "0" ] || { echo "REFUSING: $BQ qa-g30* ticket(s) already in $LOCKQ_J — a live or stale gate-30 ticket; read before launch" >&2; exit 90; }
HOLDER="$(sed -n 's/^tag=//p' "$LOCK_BASE_LAPTOP/nexusai-jest.lock/owner" 2>/dev/null | head -1)"
case "$HOLDER" in
  qa-g30*) echo "REFUSING: the Laptop-DEV jest lock is HELD by '$HOLDER' — a gate-30 holder already exists" >&2; exit 90 ;;
  qa-g29-*) LOCK_OK=0; LOCK_WHY="the jest lock is HELD by gate 29 ('$HOLDER')" ;;
  '') ;;
  *) echo "NOTE: the Laptop-DEV jest lock is held now by '$HOLDER' (FIFO; the gate queues behind it, never touches it)" >&2 ;;
esac
GQ="$(grep -lE '^tag=' "$LOCKQ_J"/* 2>/dev/null | wc -l | tr -d ' ')"
[ "${GQ:-0}" = "0" ] || echo "NOTE: $GQ ticket(s) queued in $LOCKQ_J — FIFO; gate 30 waits behind them, never touches them" >&2
LB_WAS="${NEXUSAI_LOCK_BASE:-}"
[ -z "$LB_WAS" ] || [ "$LB_WAS" = "$LOCK_BASE_LAPTOP" ] || echo "NOTE: NEXUSAI_LOCK_BASE was '$LB_WAS' in the launcher's environment — REPLACED by the Laptop-DEV base before exec (ruling q)" >&2

# 22 — the 34 paths: 33 M + 1 A (the new helper); all test code; none in the guarded set; the list PINNED; the five open RD-786 sites' files unchanged.
NS="$(g diff --name-status "$BASE" "$HEAD_SHA" 2>/dev/null)"
[ "$(printf '%s\n' "$NS" | grep -c .)" = "34" ] && [ "$(printf '%s\n' "$NS" | grep -c '^M')" = "33" ] && [ "$(printf '%s\n' "$NS" | grep '^A' | cut -f2)" = "$NEW_HELPER" ] \
  || { echo "REFUSING: base..head is not 34 paths = 33 M + 1 A ($NEW_HELPER) (WRONG 1)" >&2; exit 22; }
PL="$(g diff --name-only "$BASE" "$HEAD_SHA" 2>/dev/null | sort)"
[ "$(printf '%s' "$(printf '%s\n' "$PL" | tr '\n' ' ' | sed 's/ $//')" | shasum -a 256 | cut -d' ' -f1)" = "$PATHS_SHA" ] || { echo "REFUSING: the sorted 34-path list's sha256 is not ${PATHS_SHA:0:12}… — the PR's file set moved" >&2; exit 22; }
[ "$(printf '%s\n' "$PL" | grep -vcE "$TESTCODE_RE")" = "0" ] || { echo "REFUSING: a path in base..head is NOT test code or test tooling: $(printf '%s\n' "$PL" | grep -vE "$TESTCODE_RE" | head -3 | tr '\n' ' ')" >&2; exit 22; }
[ "$(printf '%s\n' "$PL" | grep -cE "$GUARDED_RE")" = "0" ] || { echo "REFUSING: base..head touches a guarded path (backend/ static/ templates/ package*.json .github/ bicep/ Dockerfile or the counts file)" >&2; exit 22; }
[ -z "$(g diff --name-only "$BASE" "$HEAD_SHA" -- $RD786_OPEN 2>/dev/null)" ] || { echo "REFUSING: a file of the five open RD-786 sites (#95-#99) changed base..head — the kit's NOT FIXED premise moved" >&2; exit 22; }
[ "$(blob "$HEAD_SHA" "$NEW_HELPER")" = "$HELPER_BLOB" ] || { echo "REFUSING: $NEW_HELPER at 49ba21e is not blob ${HELPER_BLOB:0:12}" >&2; exit 22; }

# 93 — the premises at source: lockfile, package.json, workflow and counts file are the SAME blobs at M0 and the head and equal the pins; counts; deploy gate.
for S in "$MAIN_SHA" "$HEAD_SHA"; do
  [ "$(blob "$S" "$LOCK")" = "$LOCK_BLOB" ] && [ "$(blob "$S" "$PKG")" = "$PKG_BLOB" ] && [ "$(blob "$S" "$DEPLOY_WF")" = "$DEPLOY_BLOB" ] && [ "$(blob "$S" "$COUNTS_FILE")" = "$COUNTS_BLOB" ] \
    || { echo "REFUSING: ${S:0:7} does not carry lockfile 19477a9 / package.json 384805d / deploy-demo.yml 953b2a2 / counts file 2cc0948 (ruling m, r0, r8)" >&2; exit 93; }
done
[ "$(counts_at "$HEAD_SHA")" = "4880 302" ] || { echo "REFUSING: the head's counts file is not 4880/302 (the builder's baseline; the PR adds no test cell)" >&2; exit 93; }
[ "$(cntF "$MAIN_SHA" "$DEPLOY_WF" "vars.CI_DEPLOY_ENABLED == 'true'")" = "2" ] || { echo "REFUSING: deploy-demo.yml at M0 no longer gates BOTH jobs on vars.CI_DEPLOY_ENABLED == 'true' (r8)" >&2; exit 93; }

# 70 — the carried rulings and Tuesday's answers (REFUSALs where a ruling is missing).
[ -s "$SQLITE_RULING" ] && grep -qF 'The offline unpack of sqlite3' "$SQLITE_RULING" || { echo "REFUSING: Tuesday's sqlite3 prebuild ruling (ruling m) is not at $SQLITE_RULING" >&2; exit 70; }
[ -s "$NOTIFIER_ANS" ] && grep -qF 'Every later npm invocation in this gate carries npm_config_update_notifier=false' "$NOTIFIER_ANS" \
  || { echo "REFUSING: Tuesday's notifier answer (ruling m) is not at $NOTIFIER_ANS as quoted" >&2; exit 70; }
grep -qF 'NOT RUN under ruling (o) EXTENDED' "$BRIEF" || { echo "REFUSING: ruling (o)'s EXTENDED words are not carried in this brief" >&2; exit 70; }
[ -s "$ANS1" ] && grep -qF 'load1 below 8 before every heavy run' "$ANS1" && grep -qF 'lock base locks-laptop-1017' "$ANS1" || { echo "REFUSING: Tuesday's ANSWER-1 (load 8, lock base) is not at $ANS1 as quoted" >&2; exit 70; }
[ -s "$ADD25" ] && grep -qF 'BEFORE you run `git remote remove origin`' "$ADD25" || { echo "REFUSING: gate 25's ADDENDUM-1 (the ref order) is not at $ADD25" >&2; exit 70; }

# 70N — machine-local premises, NOTEd (the gate records what it finds).
[ -d "$NPM_CACHE/index-v5" ] || echo "NOTE: no local npm cache at $NPM_CACHE — H-31's offline install has no source; the gate will mail a QUESTION" >&2
PB_NOW="$(fsha "$PREBUILD")"
[ "$PB_NOW" = "$PREBUILD_SHA" ] || echo "NOTE: the cached sqlite3 prebuild is '${PB_NOW:-absent}', not 84a34404…7afc — ruling (m)'s condition 1 records what the gate finds" >&2
NODEV="$(node -v 2>/dev/null)"
[ "$NODEV" = "v26.8.1" ] || echo "NOTE: host node is '${NODEV:-absent}', not v26.8.1 as briefed (T4) — the gate records it" >&2
GLV="$(gitleaks version 2>/dev/null)"
[ "$GLV" = "8.30.1" ] || echo "NOTE: gitleaks is '${GLV:-absent}', not 8.30.1 — r8 records it" >&2
LOAD1="$(sysctl -n vm.loadavg 2>/dev/null | awk '{print $2}')"
awk -v l="${LOAD1:-99}" 'BEGIN{exit !(l < 8)}' || echo "NOTE: 1-minute load is ${LOAD1:-unknown} (not below 8) — the gate waits in the queue, never in a hold (ruling p)" >&2

# 31 — the builder's STATUS (a CLAIM; ends with the READY line for the head), gate 27's / 25's instruments (THIS drive), standing references.
for f in "$STATUS_B302" "$BUILDER_BRIEF" "$BUILDER_ADD" "$CLAR" "$BRIEF27" "$BRIEF29" "$TEMPLATE" "$B27_REPORT" "$CHARTER" \
         "$B27_INST/qa-file27.sh" "$B27_INST/qa-file27r.sh" "$B27_INST/qa-floorlib27.sh" "$B27_INST/qa-holdlib27.sh" "$B27_INST/qa-h1-scan27.py" "$B27_INST/qa-h1-selftest27.sh" \
         "$B27_INST/qa-mail27.py" "$B27_INST/qa-mailread27.py" "$B27_INST/qa-revert27.py" "$B27_INST/qa-to.sh" "$B27_INST/qa-floorcount.py" \
         "$B27_INST/qa-netbelt.sb" "$B27_INST/qa-netbelt-nodns.sb" "$B27_INST/qa-names23.py" "$B27_INST/qa-ledger25.js" \
         "$B25_INST/qa-applymut.py" "$B25_INST/qa-lockcheck.py"; do
  [ -s "$f" ] || { echo "REFUSING: evidence, brief or tool absent: $f" >&2; exit 31; }
done
tail -n 1 "$STATUS_B302" | grep -qF "READY FOR QA: B302 lane 7 $BR @ $HEAD_SHA" || { echo "REFUSING: the builder's STATUS no longer ends with the READY line for 49ba21e" >&2; exit 31; }
[ "$(fsha "$STATUS_B302")" = "31c511ce837b38c3e98074671a98371ce786a7fa9106be7e517580328e228fd1" ] || echo "NOTE: the builder's STATUS sha256 is not the drafter's 31c511ce… (the file is a CLAIM and changed since drafting; the gate reads it WHOLE)" >&2
grep -qF 'STATUS: COMPLETE' "$B27_REPORT" || { echo "REFUSING: gate 27's report does not read as delivered (the instrument source must be a DELIVERED gate)" >&2; exit 31; }
grep -qF '## 3a. INSTRUMENT RULES' "$BRIEF29" && grep -qF '## 3a. INSTRUMENT RULES' "$BRIEF27" || { echo "REFUSING: gate 29's / 27's brief has no section 3a — the H-rules carried by reference are missing" >&2; exit 31; }

# 10 / 17 — the report path from the brief's §11 (its date is a stamped slot); no stale report; the brief names its sources.
REPORT_RAW="$(grep -oE 'Report: `[^`]*/report\.md`' "$BRIEF" | head -1 | sed -E 's/^Report: `//; s/`$//')"
[ -n "$REPORT_RAW" ] || { echo "REFUSING: the brief's §11 has no 'Report: \`…/report.md\`' line" >&2; exit 10; }
if printf '%s' "$REPORT_RAW" | grep -qF "$PH_SLOT"; then
  STAMP_OK=0; REPORT=''; PROVISIONAL="$PROVISIONAL REPORT_DATE(unstamped)"
else
  printf '%s' "$REPORT_RAW" | grep -Eq "^$RPTS/20[0-9]{2}-[0-9]{2}-[0-9]{2}-gate30-b302-pr98/report\.md$" \
    || { echo "REFUSING: the report path '$REPORT_RAW' is not $RPTS/<YYYY-MM-DD>-gate30-b302-pr98/report.md" >&2; exit 10; }
  REPORT="$REPORT_RAW"
  [ "$(grep -oF "$(dirname "$REPORT")" "$BRIEF" | grep -c .)" -ge 2 ] || { echo "REFUSING: T4 and §11 do not name the SAME report directory (stamp one date in both)" >&2; exit 10; }
  [ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }
fi
for P in "2026-10-19_nexusai-gate29-rd774-rd836.md" "2026-10-20_B302_STATUS.md" "2026-10-20_B302_SEAT-L7_nexusai-test-code-codeql.md" "2026-10-20_B302_ADDENDUM-1_requeue-behind-s101o.md" \
         "ADDENDUM-1" "qa-file27.sh" "qa-applymut.py" "qa-revert27.py" "qa-floorlib27.sh" "qa-floorcount.py" "qa-netbelt.sb" "QA_AGENT_CHARTER.md" "locks-laptop-1017" "models_latest.json"; do
  grep -qF "$P" "$BRIEF" || { echo "REFUSING: brief must name $P" >&2; exit 10; }
done

# 11 — identity: NexusAI's OWN dirs.
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || { echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"
[ -d "$CLAUDE_CONFIG_DIR" ] || { echo "REFUSING: Tuesday's claude store $CLAUDE_CONFIG_DIR is absent" >&2; exit 11; }

# 12 / 13 / 14 / 15 / 20 — tier, directive, brief path, pins, verdict route, key path, question route.
for T in 'TIER 2' 'MAIN-STAMP' 'NO GO' 'NO HOST NPM REGISTRY' 'npm_config_update_notifier=false' 'BOTH thresholds block' '--replace' 'qa-g30-' 'H-34' 'H-35' 'C-63' 'C-209' \
         'THE CODEQL ROW' 'THE ADJUDICATIONS' 'THE DOM EQUIVALENCE' 'THE MUTANTS' 'THE TESTS DID NOT GET WEAKER' 'EACH ALERT, BY NUMBER' 'VOID' 'can fail' 'positive control' 'G30-<n>' 'N30-<n>' \
         'NOT TESTED' 'PRIOR WORK' 'No HTTP to any production or demo host' 'never `--first-parent`' 'LEGITIMATE SHAPES' 'NOT RUN under ruling (o) EXTENDED' 'REPHRASE'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not declare '$T'" >&2; exit 12; }
done
for T in 'TIER-2 GATE THROUGH CODE' 'THE PROPERTIES' 'EACH ALERT' 'THE TESTS DID NOT GET WEAKER' 'THE ADJUDICATIONS' 'THE DOM PROOF' 'REPHRASE' 'NOT FIXED' 'strength mutant' \
         'r0' 'r1' 'r2' 'r3' 'r4' 'r5' 'r6' 'r7' 'r8' 'r9' 'S1 to S7' 'A to D2' '#95 to #99' 'C-209' 'C-190' 'T0' 'T1' 'mode 0' 'NAMED NOT RUN' 'NOT RUN' '--replace' \
         'qa-g30-' 'locks-laptop-1017' 'jest lock' "Never trust the builder's logs" 'no HTTP to any production or demo host' 'One client only' 'NO docker object and NO az' 'no model call' \
         'MERGES GO FIRST' 'QUEUE, NEVER TAKE OVER' 'Sonnet' 'PROVISIONAL' 'CodeQL is NOT RUN by this gate' 'FINDINGS-ONLY'; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare '$T'" >&2; exit 12 ;; esac
done
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
for S in "$HEAD_SHA" "$HEAD_TREE" "$BASE" "$BASE_TREE" "$LOCK_SHA_INST"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S in full" >&2; exit 14; }
  case "$PROMPT" in *"$S"*) ;; *) echo "REFUSING: prompt must name $S" >&2; exit 14 ;; esac
done
for S in $CHAIN_SHAS; do
  grep -qF -- "${S:0:7}" "$BRIEF" || { echo "REFUSING: brief must name commit ${S:0:7}" >&2; exit 14; }
  case "$PROMPT" in *"${S:0:7}"*) ;; *) echo "REFUSING: prompt must name commit ${S:0:7}" >&2; exit 14 ;; esac
done
if printf '%s\n' "$PROMPT" | LC_ALL=C grep -q '@[A-Z_0-9:-]*@'; then echo "REFUSING: the prompt carries a placeholder" >&2; exit 14; fi
case "$PROMPT" in *"MAIL YOUR VERDICT"*"tuesday-agent@agentmail.to"*) ;; *) echo "REFUSING: prompt must say MAIL YOUR VERDICT to tuesday-agent@agentmail.to" >&2; exit 15 ;; esac
grep -qF "$SUBJECT" "$BRIEF" || { echo "REFUSING: brief must carry the subject exactly: $SUBJECT" >&2; exit 15; }
case "$PROMPT" in *"$SUBJECT"*) ;; *) echo "REFUSING: prompt must carry the subject exactly: $SUBJECT" >&2; exit 15 ;; esac
case "$PROMPT" in *"/Volumes/Laptop-DEV/TUESDAY/4_Credentials/.env"*) ;; *) echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20 ;; esac
[ -s "$TUE/4_Credentials/.env" ] || { echo "REFUSING: the AgentMail key file $TUE/4_Credentials/.env is absent" >&2; exit 20; }
for T in "$QUESTION_SUBJ" "$ANSWER_PREFIX" "$ROUTE_NAME"; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the question route: $T" >&2; exit 20; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the question route: $T" >&2; exit 20 ;; esac
done
if printf '%s\n' "$PROMPT" | grep -qi 'wednesday-agent@' && ! printf '%s\n' "$PROMPT" | grep -q 'Never wednesday-agent@'; then
  echo "REFUSING: the prompt routes to wednesday-agent@ — Datasec's coordinator is Tuesday" >&2; exit 15; fi
if printf '%s\n' "$PROMPT" | grep -qF 'KK_T9_External_HDD'; then echo "REFUSING: the prompt names a T9 path — every path of this gate is on /Volumes/Laptop-DEV" >&2; exit 15; fi
[ "$(grep -oE 'qa-g30-[A-Za-z0-9_<>-]*merge[A-Za-z0-9_-]*' "$BRIEF" | grep -c .)" = "0" ] || { echo "REFUSING: the brief suggests a qa-g30- tag containing 'merge' (C-141 ADDENDUM 7)" >&2; exit 15; }
[ "$(printf '%s\n' "$PROMPT" | grep -oE 'qa-g30-[A-Za-z0-9_<>-]*merge' | grep -c .)" = "0" ] || { echo "REFUSING: the prompt suggests a qa-g30- tag containing 'merge'" >&2; exit 15; }

# 41 — RULING (i)'s by-hand yield is RETIRED: the kit and the prompt must not instruct it (the kit carries no positive retirement sentence).
for T in 'stop YOUR OWN unstarted waiter' 'stop your OWN unstarted waiter' 'then re-queue with --after that merge' 'self-apply ONE yield per gate TAG'; do
  if grep -qF -- "$T" "$BRIEF" || printf '%s\n' "$PROMPT" | grep -qF -- "$T"; then echo "REFUSING: '$T' instructs the RETIRED by-hand yield" >&2; exit 41; fi
done

# 82 — THE MODEL RULE is carried in the brief and the prompt, per session, never "Switch automatically".
for T in "$STATUS_SUBJ" "$PARK_LINE" 'classifier-stops.txt' 'Opus 4.8' 'which rows ran on which model'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks THE MODEL RULE fragment '$T'" >&2; exit 82; }
done
for T in "$STATUS_SUBJ" "$PARK_LINE" 'classifier-stops.txt' 'Switch automatically' 'Opus 4.8' 'PER SESSION' 'which rows ran on which model'; do
  case "$(printf '%s' "$PROMPT" | tr '[:upper:]' '[:lower:]')" in *"$(printf '%s' "$T" | tr '[:upper:]' '[:lower:]')"*) ;; *) echo "REFUSING: prompt lacks THE MODEL RULE fragment '$T'" >&2; exit 82 ;; esac
done
grep -qF '## MODEL RULE' "$BRIEF" && grep -qF 'H-28 (AMENDED)' "$BRIEF" && grep -qF '**H-34**' "$BRIEF" && grep -qF '**H-35**' "$BRIEF" \
  || { echo "REFUSING: brief lacks the MODEL RULE section or H-28 (amended)/H-34/H-35" >&2; exit 82; }

# 19 — the words the prompt must carry (% is a space); the brief's sections; limits; rows; T-slot form; clarification quotes.
WORDS="C-190 C-209 C-185 C-192 C-205 C-141 C-63 C-40 C-68 C-76 C-102 C-112 C-174 C-49 C-89 C-115 C-125 C-130 C-131 ADDENDUM%7
r2 r3 r4 r5 r6 r7 r8 r9 M0 39653db 49ba21e PR%#98 19477a9 RD-782 RD-783 RD-784 RD-785 RD-786 RD-787 RD-788 RD-789 SEAT-L7 S101O
L-B1 L-B6 L-Y1 H-1 H-3 H-4 H-6 H-14 H-17 H-20 H-21 H-24 H-27 H-28 H-29 H-31 H-33 H-34 H-35 --forceExit trap%on%EXIT DEADLINE LANDING%CONTROL
_prebuilds --mirror EXCLUSIVE STOP VOID MERGES%GO%FIRST QUEUE,%NEVER%TAKE%OVER SAME-PLACE%handover HEARTBEAT 2%minutes 5%minutes finally SESSION_SECRET%UNSET NOT%TESTED
MEASURED%AT%RUNTIME READ%ONLY PROBED RELAYED CodeQL%is%NOT%RUN UNKNOWN about%40%minutes TRACKED%child Prior%work FOREGROUND NEVER%push NEVER%merge Partner%Center npm%install
--offline ENOTCACHED qa-file27.sh -r<N> instrument never%fixes never%dismissed PROVISIONAL qa-g30 G30-<n> N30-<n> 1-minute%load%of%8 g30/ qa-applymut.py"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## TIER' '^## 2a-T. LEGITIMATE SHAPES' '^## WRONG OR UNVERIFIED' "^## TUESDAY'S RULINGS" '^## MODEL RULE' '^## Charter' '^## PRIOR ROUND' \
         '^## 1. Target' '^### How to build your trees' '^## 2. Tier and severity' '^## 2b. ROWS' '^## 3. THE QUESTIONS' '^## 3a. INSTRUMENT RULES' \
         '^## 3b. THE NEGATIVE-ASSERTION SWEEP' '^## 7. THE GATED TREE' '^## 8. CI, ALERTS, DEPLOY' '^## 9. Floor discipline' '^## 10. HELD' '^## 11. Output' '^## PROVENANCE' '^## FILL AT STAMP'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
WSTART="$(grep -n '^## WRONG OR UNVERIFIED' "$BRIEF" | cut -d: -f1)"; WEND="$(grep -n "^## TUESDAY'S RULINGS" "$BRIEF" | cut -d: -f1)"
[ -n "$WSTART" ] && [ -n "$WEND" ] && [ "$WSTART" -lt "$WEND" ] || { echo "REFUSING: the WRONG OR UNVERIFIED section is not above TUESDAY'S RULINGS" >&2; exit 19; }
WUNMARKED="$(sed -n "${WSTART},${WEND}p" "$BRIEF" | grep -E '^[0-9]+\. ' | grep -vE 'MEASURED|READ-ONLY-INFERRED|RELAYED|own actions' | cut -c1-60)"
[ -z "$WUNMARKED" ] || { echo "REFUSING: WRONG items not marked MEASURED / READ-ONLY-INFERRED / RELAYED: $WUNMARKED" >&2; exit 19; }
for L in L-B1 L-B2 L-B3 L-B4 L-B5 L-B6 L-Y1; do grep -qF "$L" "$BRIEF" || { echo "REFUSING: brief lacks declared limit $L (C-112)" >&2; exit 19; }; done
for R in r0 r1 r2 r3 r4 r5 r6 r7 r8 r9; do grep -qF "| $R |" "$BRIEF" || { echo "REFUSING: brief lacks row $R" >&2; exit 19; }; done
for n in 0 1 2 3 4 5; do
  grep -qE "^- \*\*\(T${n}\) [^*]*:\*\* RULED: " "$BRIEF" || { echo "REFUSING: brief lacks the ruling slot (T$n) as '**(T$n) …:** RULED: …'" >&2; exit 19; }
done
while IFS= read -r Q; do
  [ -n "$Q" ] || continue
  grep -qF -- "$Q" "$CLAR" || { echo "REFUSING: CLARIFICATIONS no longer carries '$Q' — the brief's quotes are stale; re-brief" >&2; exit 19; }
  grep -qF -- "$Q" "$BRIEF" || { echo "REFUSING: brief does not quote '$Q'" >&2; exit 19; }
done <<'CLAR_EOF'
The jest and docker lock (`session-tools/nexusai-lock.sh`) is first-in-first-out, and it takes over an ownerless lock after 30 s.
a FAILED ls-remote is UNKNOWN, never a value.
A check must be able to fail on the thing it claims to be about.
An explanation of why a fix works is a CLAIM: it gets a red proof, or it is marked UNVERIFIED in the artefact that carries it.
A declared limit is where the evidence stops — not a place it is cleared.
NEVER KILL BY PATTERN.
Every merge to NexusAI main goes through a PULL REQUEST, and a PR must add NO NEW high-or-higher CodeQL alert in the code it changes. Test code is included.
`alerts_threshold = errors`, so ANY new alert whose RULE severity is `error` blocks, whatever its security severity.
A PR's CodeQL run CANNOT show a PRE-EXISTING main alert as fixed
Gate (`qa-*`) tickets are never moved; the holder is never touched.
CLAR_EOF

# 24 — the prompt must DESCRIBE the server entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qi 'backend/server\.js'; then
  echo "REFUSING: the prompt contains the server entry point's literal path (RD-591 c.37901). Describe it; do not name it." >&2; exit 24; fi

# 53 / 71 — standing rules in the brief; the NOT TESTED line read from the brief (ONE line); appended to the prompt at exec.
for w in 'DEADLINE' 'HEARTBEAT' 'qa-g30-' 'VOID' 'EXCLUSIVE' 'POSITIVE CONTROL FIRST' 'QUEUE, NEVER TAKE OVER' \
         '--replace' 'never push' 'C-174' '--forceExit' 'trap … EXIT' 'MERGES GO FIRST' 'never idles holding a lock' \
         'ONE focused hold at a time' 'FOREGROUND' 'Never two live holds' 'Every finding names its instrument' \
         'NOT TESTED' 'The tester never fixes' 'ONE CLIENT ONLY' 'no CodeQL alert dismissed' 'below a 1-minute load of **8**'; do
  grep -qiF -- "$w" "$BRIEF" || { echo "REFUSING: brief lacks the standing rule '$w'" >&2; exit 53; }
done
NOTTESTED_LINE="$(grep -E '^  Not tested by this gate: ' "$BRIEF" | sed 's/^  //')"
[ "$(printf '%s\n' "$NOTTESTED_LINE" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: the brief must carry exactly ONE '  Not tested by this gate: …' line (§11)" >&2; exit 71; }
for w in 'the CodeQL closure of the 63 alerts' 'the full jest suite on Node 24' 'the full 4880-test verify' 'the Playwright e2e specs and the UAT script' 'the eight Jira comments' \
         'headed Chrome and every browser' 'Windows' 'the demo and any deployed revision' 'npm audit' 'the host npm registry'; do
  case "$NOTTESTED_LINE" in *"$w"*) ;; *) echo "REFUSING: the brief's NOT TESTED line lacks '$w'" >&2; exit 71 ;; esac
done
grep -qF 'and its LAST two lines, verbatim as mailed' "$BRIEF" || { echo "REFUSING: brief must fix the report's last lines as the two verdict lines" >&2; exit 71; }
for V in '`B302/PR98: <GO|GO WITH FINDINGS|NO GO> @ ' '`LANDING CHECKLIST: PR #98 '; do
  grep -qF -- "$V" "$BRIEF" || { echo "REFUSING: the brief's §11 lacks the verdict line '$V'" >&2; exit 71; }
done

# 76 / 77 / 78 / 79 — H-1's printer and forbidden idioms; H-4; H-7/H-8/H-21 (H-9's byte plants are not in this kit: no CR/LF/ESC/NUL plant row).
grep -qF "$SAFE_PRINTER" "$BRIEF" || { echo "REFUSING: brief must carry the safe SESSION_SECRET printer verbatim (H-1)" >&2; exit 76; }
for w in '${SESSION_SECRET-…}' '${SESSION_SECRET:-…}' 'echo $SESSION_SECRET' 'printenv'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief must name the forbidden idiom $w (H-1)" >&2; exit 76; }
done
for w in 'H-4' 'heartbeat' 'within 90 s' 'max gap'; do grep -qiF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the heartbeat fragment '$w' (H-4)" >&2; exit 77; }; done
for w in 'H-7/H-8/H-21' 'FAILS LOUDLY' 'trap'; do grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the mutant-landing fragment '$w' (H-7/H-8)" >&2; exit 79; }; done

# 38R — the negative-control seats are DERIVED now from the live cockpit panes: the claude descendant of each pane pid.
# ps, not pgrep: macOS pgrep hides the caller's own ancestors, so Tuesday's own claude would vanish when --check runs from her shell.
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
NEG_SEATS=''; NEG_DESC=''; NEG_BUILDERS=0
COORD_NAME=''
for NAME in tuesday wednesday; do
  if [ -n "$(pane_pid_of "$NAME" | sed '/^$/d')" ]; then
    [ -z "$COORD_NAME" ] || { echo "REFUSING: panes named BOTH 'tuesday' and 'wednesday' are live — the coordinator's negative control is ambiguous" >&2; exit 38; }
    COORD_NAME="$NAME"
  fi
done
[ -n "$COORD_NAME" ] || { echo "REFUSING: no tmux pane named 'tuesday' or 'wednesday' — the coordinator's negative control is required" >&2; exit 38; }
[ "$COORD_NAME" = "tuesday" ] || echo "NOTE: the coordinator's pane is named '$COORD_NAME' on this machine — used as the coordinator's negative control" >&2
for NAME in Datasec/NexusAI-L7 Datasec/NexusAI-M Datasec/NexusAI-N Datasec/NexusAI-O Datasec/NexusAI-P Datasec/NexusAI-R "$COORD_NAME"; do
  PP="$(pane_pid_of "$NAME")"
  NP="$(printf '%s\n' "$PP" | sed '/^$/d' | wc -l | tr -d ' ')"
  if [ "$NP" = "0" ]; then
    [ "$NAME" = "$COORD_NAME" ] || echo "NOTE: no tmux pane named '$NAME' — not a negative control this launch" >&2; continue
  fi
  [ "$NP" = "1" ] || { echo "REFUSING: more than one tmux pane named '$NAME': '$PP' — cannot derive its negative-control seat" >&2; exit 38; }
  CP="$(claude_under "$PP")"
  [ "$(printf '%s\n' "$CP" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: pane '$NAME' (pid $PP) has '${CP:-no}' claude descendant(s), not exactly one — a seat is missing or ambiguous" >&2; exit 38; }
  NEG_SEATS="$NEG_SEATS $CP"; NEG_DESC="$NEG_DESC \`$CP\` ($NAME);"
  [ "$NAME" = "$COORD_NAME" ] || NEG_BUILDERS=$((NEG_BUILDERS + 1))
done
[ "$NEG_BUILDERS" -ge 1 ] || { echo "REFUSING: no live builder seat among Datasec/NexusAI-L7/M/N/O/P/R — at least ONE negative control is required" >&2; exit 38; }
# fleet-monitor and every live 'QA/*' pane other than this gate's own (gate 29 included while it runs): a negative control when exactly one claude runs under it.
EXTRA="$(printf '%s\n' "$PANES" | awk '{p=$1; $1=""; sub(/^ /,""); print $0}' | grep -E '^(QA/|fleet-monitor$)' | grep -vxF "$ROUTE_NAME" | sort -u)"
while IFS= read -r PEER; do
  [ -n "$PEER" ] || continue
  GP="$(pane_pid_of "$PEER")"; GC=''
  [ -n "$GP" ] && [ "$(printf '%s\n' "$GP" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] && GC="$(claude_under "$GP")"
  if [ -n "$GC" ] && [ "$(printf '%s\n' "$GC" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ]; then
    NEG_SEATS="$NEG_SEATS $GC"; NEG_DESC="$NEG_DESC \`$GC\` ($PEER);"
    echo "NOTE: $PEER has a live claude — added as a negative control (FIFO, never touched)" >&2
  else
    echo "NOTE: $PEER has no single live claude — not a negative control" >&2
  fi
done <<EOF_PEERS
$EXTRA
EOF_PEERS
NEG_SEATS="${NEG_SEATS# }"
NCOUNT="$(printf '%s\n' $NEG_SEATS | sed '/^$/d' | wc -l | tr -d ' ')"
[ "$(printf '%s\n' $NEG_SEATS | sort -u | wc -l | tr -d ' ')" = "$NCOUNT" ] || { echo "REFUSING: the derived seat pids are not distinct: $NEG_SEATS" >&2; exit 38; }

# 86 — no live gate-30 session already exists.
for P in $(pane_pid_of "$ROUTE_NAME"); do
  if [ -n "$(claude_under "$P")" ]; then echo "REFUSING: a pane named $ROUTE_NAME (pid $P) already runs a claude — gate 30 is live; do not start a second session" >&2; exit 86; fi
  [ "$CHECK" = "1" ] || echo "NOTE: a pane named $ROUTE_NAME (pid $P) exists with no claude under it — the cockpit's own add decides" >&2
done

# 32S / 33L / 40 — LAST: the coordinator's stamp (0 at-sign SLOT placeholders anywhere in the kit: MAIN pin x2 + tree + landed, REPORT_DATE x2, RULED: T0-T5,
# SELF-CHECK + note; the SELF-CHECK line in the fleet's form), a gate-29 HOLD on the jest lock, and the answer route (Tuesday adds it, never this launcher).
NSLOT="$(grep -oF "$PH_SLOT" "$BRIEF" | grep -c .)"
if [ "$NSLOT" != "0" ] || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then STAMP_OK=0; fi
ROUTE_OK=1
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || ROUTE_OK=0
GUARDS='9 40 18T 18 6 18M 7 8 90 22 93 70 70N 31 10 17 11 12 13 14 15 20 41 82 19 24 53 71 76 77 78 79 38R 86'
SUMMARY="ls-remote attempts this run: $LSR_ATTEMPTS (C-192); origin main ${M_ORIGIN:0:7} (M0 ${MAIN_SHA:0:7} tree ${M0_TREE:0:7}; ancestry carries 39653db; the 8 PR #98 commits not on M0; MODE $MODE); B302 ${HEAD_SHA:0:7} (tree ${HEAD_TREE:0:7}; branch and $PR_REF agree; 34 paths = 33 M + 1 A, all test code, 0 guarded; lockfile/package/workflow/counts blobs = M0's); lock tool ${INST_NOW:0:12}…; model $MODEL"
if [ "$STAMP_OK" = "0" ] || [ "$ROUTE_OK" = "0" ] || [ "$LOCK_OK" = "0" ]; then
  echo "guards pass ($GUARDS); stamp, gate-29 lock hold and/or route NOT complete." >&2
  echo "  $SUMMARY" >&2
  [ -z "$PROVISIONAL" ] || echo "  PROVISIONAL (unstamped slots, --check ran against):$PROVISIONAL" >&2
  echo "  NEG seats (38R, derived live; coordinator pane '$COORD_NAME'):$NEG_DESC" >&2
  [ "$LOCK_OK" = "1" ] || echo "REFUSING (33L): $LOCK_WHY — gate 30 launches when the gate-29 hold ends (queued tickets of other seats are fine: FIFO)" >&2
  [ "$ROUTE_OK" = "1" ] || echo "REFUSING (40): no '${ROUTE_NAME}|tuesday-agent@agentmail.to|no' line in $ROUTING — answers to the gate would have no route; Tuesday adds it at stamp (this launcher never writes it)" >&2
  [ "$STAMP_OK" = "1" ] || echo "REFUSING (32S): $NSLOT at-sign SLOT placeholder(s) remain in the brief (MAIN pin x2 + tree + landed, REPORT_DATE x2, RULED: T0-T5, the SELF-CHECK line and the Self-check note), or the SELF-CHECK line is not in the fleet's form — the coordinator re-reads end-to-end and stamps them before launch" >&2
  [ "$STAMP_OK" = "1" ] || exit 32
  [ "$ROUTE_OK" = "1" ] || exit 40
  exit 33
fi

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  origin at $PIN_TS ($LSR_ATTEMPTS ls-remote attempt(s), C-192): main = the stamped pin ${MAIN_SHA:0:12} exactly; the branch and $PR_REF at 49ba21e; T9 unmounted (18T)"
  echo "  $SUMMARY"
  echo "  NEG seats (38R, derived live; coordinator pane '$COORD_NAME'):$NEG_DESC"
  echo "  report: $REPORT"
  echo "  SUBJECT: $SUBJECT"
  echo "  NEXUSAI_LOCK_BASE=$LOCK_BASE_LAPTOP  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  --check started no claude; nothing written."
  exit 0
fi

PROMPT="$PROMPT
$NOTTESTED_LINE

THE MODEL OF THIS SESSION (the --model, models_latest.json levels.sonnet.model_id): $MODEL.
WRITE YOUR ONE REPORT TO: $REPORT
VERIFIED BY THE LAUNCHER AT $PIN_TS (git ls-remote origin, read-only, $LSR_ATTEMPTS attempt(s) under C-192): refs/heads/main = $M_ORIGIN = the stamped MAIN pin (tree $M0_TREE; its ancestry carries 39653db; PR #98's eight commits are not on it; what landed since 39653db per the stamp: $S_LANDED; MODE $MODE — mode 0 means the gated tree is the head itself, otherwise T0's stamped ruling applies); refs/heads/$BR = $PR_REF = $HEAD_SHA (tree $HEAD_TREE). The head is 8 linear commits over 39653db; its 34 paths are 33 modified and 1 added, all test code, none a backend, static, package, workflow or counts-file path; the lockfile, package.json, deploy-demo workflow and counts file are the same blobs at M0 and the head; the files of the five open RD-786 sites are byte-unchanged. The T9 is unmounted. No gate-29 ticket holds the jest lock. The installed lock tool $LOCKTOOL sha256 $INST_NOW equals the pin and NEXUSAI_LOCK_BASE=$LOCK_BASE_LAPTOP is exported in your environment. These are the start-of-gate pins; take your own three readings anyway.
NEGATIVE-CONTROL SEATS, derived live by the launcher from the cockpit panes at $PIN_TS (the coordinator's pane is named '$COORD_NAME' on this machine):$NEG_DESC Re-read them at the start of every hold."

# rd579-rd639 S-1 belt: the gate session inherits NO SESSION_SECRET. The line prints the NAME and a state only, never a value.
if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET in the launcher's environment (length ${#SESSION_SECRET}) — unsetting before exec"; else echo "SESSION_SECRET UNSET"; fi
unset SESSION_SECRET
# ruling q / H-34: the gate's lock calls use the Laptop-DEV base while the T9 is unmounted.
export NEXUSAI_LOCK_BASE="$LOCK_BASE_LAPTOP"
# ruling (m): the gate's own npm calls inherit the notifier switch (the gate still passes it explicitly on every call).
export npm_config_update_notifier=false

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model "$MODEL" "$PROMPT"
