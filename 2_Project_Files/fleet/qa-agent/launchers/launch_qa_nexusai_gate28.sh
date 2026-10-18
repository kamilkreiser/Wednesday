#!/bin/bash
# launch_qa_nexusai_gate28.sh — cross-project QA agent, ONE gate on Datasec/NexusAI (gate 28): a TIER-2 BATCH of four file-disjoint items —
# RD-476 (assistant system prompt, Kam-approved words), RD-856 + RD-857 (a STACK: pronoun-led lead guard, then whole-word skip list +
# department/location guard), each measured merged onto the STAMPED main, plus D = the C-170 TEST DELTA (PR #96, test-only, through code;
# its merge is NOT part of this gate) — three verdict lines + one ORDER/TURN line, ONE report.
# (drafted 2026-10-19 from ~07:17 AEDT by a read-only drafting agent for Tuesday, AMENDMENT 1 of the gate-28 kit; the drafter ran only bash -n
# and the --check refusal path with the kit still slotted).
# A FRESH gate on the Mac mini, /Volumes/Laptop-DEV; the T9 is UNMOUNTED, so the lock base is the Laptop-DEV locks-laptop-1017.
#   RD-476 rd-476-assistant-prompt-s101o        @ f9649dc (2 commits on c7ca0ed, draft PR #91)  AS MERGED onto M0
#   RD-856 rd-856-user-pattern-verb-guard-s101o @ f4026fb (1 commit on c7ca0ed, draft PR #92)   AS MERGED onto M0 (B)
#   RD-857 rd-857-whole-word-skip-list-s101o    @ 1da0bd4 (f4026fb + 1, draft PR #93)            AS MERGED onto M0 (B+C, STACKED)
#   C-170 delta rd-460-c170-turn-s101o fd8ff2a -> f15217c (PR #96, 4 test paths, 0 product bytes) — gated as a delta, NOT merged here
#   M0 = the MAIN pin Tuesday STAMPS (888203c at AMENDMENT 1; RD-778 may land first). The launcher never predicts main.
#
# LAUNCHED ONLY VIA: cockpit.sh add 'QA/NexusAI-gate28' "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate28.sh'"
#   (i.e. /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh). A tmux pane, NEVER nohup, never run it bare from a seat's shell.
#
# AUTHORITY: Tuesday's gate-28 drafting commission (2026-10-18) and its AMENDMENT-1 commission (2026-10-19); her ANSWER-6/8/9/10 (tiers and the
# guard ruling), ANSWER-16 (landing order), ANSWER-18 (RD-794 land accepted, main 888203c) and ANSWER-19 (C-170's test delta = an extra item of
# gate 28; C-170's land HELD behind it).
# THE MODEL RULE: Kam, live board 2026-09-30 09:07, card nexusai-gate11-opus55-safeguard-model-switch, option (b), PER SESSION. The MODEL is the
# kit's stamped MODEL line (tier 2; Tuesday decides), validated against models_latest.json levels.sonnet / levels.opus.
# Carried rulings (sqlite3 cached prebuild; full verifies UNBELTED; npm_config_update_notifier=false; ruling (b) + EXTENSION; C-190 + ADDENDUM;
# C-209; C-141 ADDENDA 6/7; the by-hand gate yield RETIRED; the load-8 rule; the Laptop-DEV lock base).
# FINDINGS-ONLY: never merges (outside its own store), never pushes, never opens/comments/approves/updates a PR, never dismisses an alert, never
# swaps or edits the lock tool, the C-57 runner or the C-133 tool; no fix, no deploy, no az, no docker, no model call, no demo, no human.
#
# PATTERN: launch_qa_nexusai_gate27.sh (prompt EMBEDDED, --check mode, PIN-table parser, C-192 lsr retry, lock/runner/C-133 pins 90/91, carried
# rulings 70, MODEL RULE 82, H-rule fragments 76-79, the LIVE negative-control seat derivation 38R, guard 86, stamp + route guards LAST) and
# launch_qa_nexusai_gate26.sh (the C-170 premises). CHANGES, each deliberate:
#   - 40: FIVE pin rows (MAIN stamped + RD476 RD856 RD857 C170D); no MERGE-PINS table (the gate rebuilds every merge onto M0 itself).
#   - MAIN is read from the kit's MAIN-STAMP line + PIN-HEADS MAIN row (they must agree). While UNSTAMPED, --check runs every guard against
#     origin main as a PROVISIONAL M0 and refuses at the end (32S); a stamped pin must equal origin main exactly.
#   - 18M: 888203c, 5eb80a7, 36a0dc0 in M0's ANCESTRY (is-ancestor, never --first-parent) with their trees; M0's tree = the stamped tree;
#     C-170 (be0fe37, fd8ff2a, f15217c) NOT on M0; arm-ttk.yml absent at M0; what landed since 888203c NOTEd (and named in the stamp).
#   - 22: per head, the gated paths; the both-sides set vs M0 (A: preload + model-config + counts; B, C: server.js + counts); the LEGACY
#         stdout-only `git merge-tree <base> <M0> <head>` (writes no object) shows conflict markers in the counts section ONLY. D: 4 test paths.
#   - 93: counts/blobs; predictions RECOMPUTED in-guard from M0's own counts (+35/1, +22/2, +57/3); the prompt shas; the ollama boot vs M0's
#         provider removal (row r10P's premise); D's helper, build-script blob 40ec7de3, mutant anchors, the 19 suites, jest's helper ignore.
#   - 31: FOUR READY copies, each sha256 PINNED.
#   - MODEL from the kit's stamped MODEL line (not from models_latest.json's opus level), validated against models_latest.json.
#   - REPORT path from the kit's §11 Report line (its date is a stamped slot); refuses if the report exists.
#   - the NOT TESTED line is READ from the kit (one line) and appended to the prompt verbatim at exec.
#
# Identity: exports NexusAI's OWN az/gh dirs (az is NOT used; gh READ-ONLY); CLAUDE_CONFIG_DIR pinned to Tuesday's store.
# --check is READ-ONLY in NexusAI: git read verbs with --no-optional-locks (cat-file, log, merge-base, diff, show, rev-parse, ls-remote, rev-list,
# ls-tree, grep) and the legacy stdout-only merge-tree (no object written); shasum / bash -n / grep over session-tools files; python over `git show`
# output; node over `git show` output (prompt extraction); ls, ps, tmux list-panes, test -e. Writes nothing.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate28.sh [--check]
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
BRIEF="$BRIEFS/2026-10-18_nexusai-gate28-batch-rd476-rd856-rd857.md"
BRIEF22="$BRIEFS/2026-10-13_nexusai-gate-batch22.md"
BRIEF23="$BRIEFS/2026-10-16_nexusai-gate-batch23.md"
BRIEF24="$BRIEFS/2026-10-17_nexusai-gate24-rd848.md"
BRIEF25="$BRIEFS/2026-10-18_nexusai-gate25-rd761-rd794-merged.md"
BRIEF26="$BRIEFS/2026-10-18_nexusai-gate26-c170-be0fe37-merged.md"
TEMPLATE="$TUE/2_Project_Files/fleet/qa-agent/BRIEF_TEMPLATE.md"
ADD25="$TBRIEFS/2026-10-18_gate25_ADDENDUM-1_ref-order.md"
READY_476="$BRIEFS/2026-10-19_nexusai-gate28-READY-rd476-r2.txt";   READY_476_SHA='c43893cd6694b40723300ced6eadd598ecfeff05cf46f53c5bfcf7614cfd0821'
READY_856="$BRIEFS/2026-10-19_nexusai-gate28-READY-rd856.txt";      READY_856_SHA='c8f502245764b548b3d72074780dee208086ce1794c1f18084c683a8484955e2'
READY_857="$BRIEFS/2026-10-19_nexusai-gate28-READY-rd857.txt";      READY_857_SHA='7cf6c411d2b3605851143bed9aea54560ce7ea5defe0cd9ae0af70217ac76256'
READY_D="$BRIEFS/2026-10-19_nexusai-gate28-READY-c170-delta.txt";   READY_D_SHA='a2e8a037fef584b675724542fe06b8dc313d687f713c515bcfc2277548ad0cdd'
ANS1="$TBRIEFS/2026-10-18_S101O_ANSWER-1_plan-confirmation.md"
ANS6="$TBRIEFS/2026-10-18_S101O_ANSWER-6_rd476-ready-received.md"
ANS8="$TBRIEFS/2026-10-18_S101O_ANSWER-8_rd856-ready-received.md"
ANS9="$TBRIEFS/2026-10-18_S101O_ANSWER-9_rd857-v4-ruling.md"
ANS10="$TBRIEFS/2026-10-18_S101O_ANSWER-10_rd857-guard-word-level.md"
ANS16="$TBRIEFS/2026-10-18_S101O_ANSWER-16_gate25-landing-stacked.md"
ANS18="$TBRIEFS/2026-10-19_S101O_ANSWER-18_rd794-accepted-c170-turn.md"
ANS19="$TBRIEFS/2026-10-19_S101O_ANSWER-19_c170-codeql-test-fix.md"
CHARTER="$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"
MODELS_JSON="$TUE/0_Brain/dashboard/data/models_latest.json"
BELT_ANS="$STAGED/2026-10-05_qa_b14_belt_ANSWER.md"
SQLITE_RULING="$STAGED/2026-10-05_qa_b14_sqlite3_ANSWER.md"
NOTIFIER_ANS="$STAGED/2026-10-05_qa_gate16_notifier_ANSWER.md"
RULING_B="$STAGED/2026-10-06_nexusai_g18_ruling_b_deliver_now.md"
G19_RELEASE="$STAGED/2026-10-12_nexusai_gate19_RELEASE.md"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
NX='/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI'
REPO="$NX/2_Project_Files"
ST="$NX/session-tools"
S101="$ST/s101"
LOCKTOOL="$ST/nexusai-lock.sh"
C57TOOL="$ST/c57-id-superset.sh"
C133TOOL="$ST/s78g/c133-accounting.py"
LOCK_SHA_INST='3c33f5ae58e1be20282467a90b27a23a2de998eedd0e56c03f3c06360031a792'   # RD-821 round 3, INSTALLED — PINNED
C57_SHA='1ae84a1083348be3acbd421e595af262f74260bf92c1eb822757fc7363125581'         # RD-837 r2 — PINNED
C133_SHA='6f938bfcf2557d9f986894734e4b79390dfb90fbc7c62d63b989fbe58f6f972f'        # RD-658 — PINNED
T9_VOL='/Volumes/KK_T9_External_HDD'
LOCK_BASE_LAPTOP="$ST/locks-laptop-1017"
LOCKQ_J="$LOCK_BASE_LAPTOP/queue-jest"
CLAR="$NX/1_Project_Definition/CLARIFICATIONS.md"
RPTS="$QA_DIR/projects/nexusai/reports"
B25_DIR="$RPTS/2026-10-18-gate25-rd761-rd794-merged"
B25_REPORT="$B25_DIR/report.md"
B25_INST="$B25_DIR/evidence/inst"
B26_DIR="$RPTS/2026-10-18-gate26-c170-be0fe37-merged"
B26_REPORT="$B26_DIR/report.md"
B26_INST="$B26_DIR/evidence/inst"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"
ROUTE_NAME='QA/NexusAI-gate28'
NPM_CACHE="${HOME}/.npm/_cacache"
PREBUILD="${HOME}/.npm/_prebuilds/0068db-sqlite3-v5.1.7-napi-v6-darwin-arm64.tar.gz"
PREBUILD_SHA='84a34404b12ff212adbca70eff76c2e4dd83b91245eed0b4569438f928567afc'

# ---- the pins (cross-checked against the brief's PIN-HEADS, guard 40; each MEASURED 2026-10-19 07:17-07:22 AEDT, kit AMENDMENT 1)
FLOOR_MAIN='888203c8c50e13938ca557e8aa0f1faf2101ff31'; FLOOR_TREE='428f042b34fb1729d8fd45a112a1220af0fdae6a'   # main at AMENDMENT 1 (RD-794 forward-merged)
OLD_MAIN='c7ca0ed7113750b268028f12e8659bf1e3d34282'      # the three heads' base; NEVER gated onto
L761='36a0dc0eb801e5eb52a00be7c0d3de360eb1952d'; T761='fb8197a78a94806a2bc7b7ec00ff6e8758788a12'      # land 1 (RD-761)
L775='5eb80a7a0ee896d8189c85f9103c9f5df01e0112'; T775='2d2caa3f610626ac5f5219aad401590739c2fcfe'      # land 2 (RD-775)
H460='be0fe3704023d8f092da0be27f79b82fbc029085'                                                     # C-170's head: must NOT be on M0
G26SEAT='88153c09155feb1eaf29ea2c0f18c5039cc64c9b'                                                  # gate 26's seat commit (be0fe37 + c7ca0ed)
B476='rd-476-assistant-prompt-s101o';        H476='f9649dcf9d30ea12af58ff60007b0c67318866fd'; R1_476='393929057997e20d7280e09b963539e9f41eba10'
B856='rd-856-user-pattern-verb-guard-s101o'; H856='f4026fba5598ad5355b1daf21def9b651ee7bdc9'
B857='rd-857-whole-word-skip-list-s101o';    H857='1da0bd4684b804ccbb36f358e246759ed9a5ef8c'
BD='rd-460-c170-turn-s101o'; HD0='fd8ff2ac4c59f9777ecb78d40a5d60f84d4dc711'; HD1='f15217cba52a97cfa55cea2155e14d690c2bd87e'; TD1='a0da892ab59c38fa33d3639bfde1b58f467db939'

COUNTS_FILE='scripts/verify-expected-counts.json'
CB_BASE='fadda68557bc263a64f88e4bb54f0c1405d931a5'; CB_D='0e50ac0c41f7897825122b8a018ad7683653afae'
PKG='package.json'; PKG_BLOB='384805d9e286718bb34ffd05be01c62c00806cf5'
LOCK='package-lock.json'; LOCK_BLOB='19477a9329f17e529c208d91d172b95b47fc1bb5'
DEPLOY_WF='.github/workflows/deploy-demo.yml'; DEPLOY_BLOB='953b2a2f84e8710bea857ec87c6f00faa50fa56b'
ARMTTK='.github/workflows/arm-ttk.yml'
PRELOAD='__tests__/helpers/rd395-llm-mock-preload.js'
SERVER='backend/server.js'
BUILDSH='scripts/marketplace-package-build.sh'; BUILDSH_BLOB='40ec7de3bf3fdc553e733038161355dc027c2511'
PROMPT_BASE_SHA='666399e1bfdefde0e7bec58b4347af5c7e20fc4a8c85d6c5ae64bf76fc505a9c'; PROMPT_BASE_LEN=7686
PROMPT_R1_SHA='70c48fc277ca2fca20f1e85444e49a28fd9738d9e5427877b12903c625665659'
PROMPT_R2_SHA='f36881ddb55c455a262a94768eced6d2a9664d32f338021418f56058e84b2a9d'; PROMPT_R2_LEN=9956
GATED_476='__tests__/helpers/rd395-llm-mock-preload.js __tests__/rd476-assistant-prompt.test.js model-config.js scripts/verify-expected-counts.json'
GATED_856='__tests__/rd856-user-pattern-pronoun-lead.test.js backend/server.js scripts/verify-expected-counts.json'
GATED_857='__tests__/rd856-user-pattern-pronoun-lead.test.js __tests__/rd857-user-skip-list-whole-word.test.js backend/server.js scripts/verify-expected-counts.json'
GATED_D='__tests__/helpers/escape-regexp.js __tests__/marketplace-single-build-path.test.js __tests__/rd471-wizard-image-element-types.test.js __tests__/rd472-image-bearing-resources.test.js'
BOTH_476='__tests__/helpers/rd395-llm-mock-preload.js model-config.js scripts/verify-expected-counts.json'
BOTH_BC='backend/server.js scripts/verify-expected-counts.json'
SUITES19='image-content-exposure rd418-dockerignore-round3 rd385-shipped-root-markdown-identifiers rd698-mixed-encoding-file rd699-decode-branches-behaviour rd403-first-run-no-publisher-identifiers rd477-customer-leftovers marketplace-package-build marketplace-single-build-path rd630-armttk-ci-workflow marketplace-setup-checks rd472-image-bearing-resources rd471-wizard-image-element-types rd503-r2-doc-claims-against-product dev-scripts-template-parameters rd461-self-contained-and-template-toolkit marketplace-template-log-analytics-enabled marketplace-keyvault-durability listing-folds-rd465-rd454'
NEG_SEATS=''   # 38R: DERIVED at launch from the live cockpit panes — never stamped by hand

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — gate 28'
QUESTION_SUBJ='[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>'
STATUS_SUBJ='[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch'
PARK_LINE='PARKED: flagged — awaiting the Opus 4.8 switch'
ANSWER_PREFIX='[Tuesday -> QA/NexusAI-gate28] ANSWER'
SAFE_PRINTER='if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET (length ${#SESSION_SECRET})"; else echo "SESSION_SECRET UNSET"; fi'

g() { git --no-optional-locks -C "$REPO" "$@"; }
counts_blob() { g cat-file -p "$1" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
counts_at() { counts_blob "$(g rev-parse --verify -q "${1}:${COUNTS_FILE}" 2>/dev/null)"; }
blob() { g rev-parse --verify -q "${1}:${2}" 2>/dev/null; }
cntF() { g show "${1}:${2}" 2>/dev/null | grep -cF -- "$3"; }
fsha() { shasum -a 256 "$1" 2>/dev/null | cut -d' ' -f1; }
tree_of() { g rev-parse --verify -q "${1}^{tree}" 2>/dev/null; }
parents_of() { g log -1 --format='%P' "$1" 2>/dev/null; }
sorted() { printf '%s\n' $1 | sort | tr '\n' ' ' | sed 's/ $//'; }
paths_of() { g diff --name-only "$1" "$2" 2>/dev/null | sort | tr '\n' ' ' | sed 's/ $//'; }
both_sides() { comm -12 <(g diff --name-only "$1" "$2" 2>/dev/null | sort) <(g diff --name-only "$1" "$3" 2>/dev/null | sort) | tr '\n' ' ' | sed 's/ $//'; }
prompt_of() { g show "${1}:model-config.js" 2>/dev/null | node -e 'let s=require("fs").readFileSync(0,"utf8");const m=s.match(/SYSTEM_PROMPT\s*=\s*`([\s\S]*?)`/);if(!m){console.log("NONE");process.exit(0)}const t=m[1];console.log(t.length+" "+require("crypto").createHash("sha256").update(t,"utf8").digest("hex"))' 2>/dev/null; }
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

You are the fleet QA/testing agent running ONE gate on Datasec/NexusAI, gate 28: a TIER-2 BATCH of four file-disjoint items, gated THROUGH CODE, with three verdict lines, one ORDER/TURN line and ONE report. It is a FRESH gate on Kam's Mac mini, working volume /Volumes/Laptop-DEV; the T9 drive is UNMOUNTED, so the project's jest lock lives on this drive's locks-laptop-1017 base. The items: A = RD-476, rd-476-assistant-prompt-s101o at f9649dcf9d30ea12af58ff60007b0c67318866fd (two commits on c7ca0ed7113750b268028f12e8659bf1e3d34282, draft PR #91: the assistant's system prompt rewritten to the words Kam approved on two cards); B = RD-856, rd-856-user-pattern-verb-guard-s101o at f4026fba5598ad5355b1daf21def9b651ee7bdc9 (one commit on c7ca0ed, draft PR #92: a pronoun-led capture is never a user name); C = RD-857, rd-857-whole-word-skip-list-s101o at 1da0bd4684b804ccbb36f358e246759ed9a5ef8c (one commit STACKED on B, draft PR #93: the skip list by whole word with a plural rule, and a department/location guard after a failed lookup) — B and C are ONE STACK with one verdict; and D = THE C-170 TEST DELTA, rd-460-c170-turn-s101o fd8ff2ac4c59f9777ecb78d40a5d60f84d4dc711 -> f15217cba52a97cfa55cea2155e14d690c2bd87e (one commit, PR #96: a full RegExp-escape helper at five test sites to clear CodeQL #266 to #271; 4 test paths, 0 product bytes). A, B and C are measured AS THEY WOULD LAND: each merged onto M0, the main Tuesday STAMPED (the launcher verified origin main equals it; its sha and tree are at the end of this prompt), which you REBUILD yourself in your own store with the counts file regenerated under C-57. D is NOT merged by this gate: C-170's PRODUCT was gated by gate 26 (GO WITH FINDINGS), this gate gates ONLY its test delta, and C-170 lands later by its own counts-only TURN on Tuesday's GO. Never trust the builders' trees, logs, cells, tables or equivalence files as the proof. FINDINGS-ONLY: you NEVER merge anything the fleet can see, NEVER push, NEVER open, comment on, approve, un-draft or merge a pull request, never dismiss an alert, and NEVER swap, copy over or edit the installed lock tool, the C-57 runner or the C-133 tool; no fixes, no deploys, no az, no docker, no model call of any kind, no production, no HTTP to any production or demo host, nothing to Partner Center, the demo or any human, no host npm registry. One client only: Datasec/NexusAI.

READ YOUR COMMISSION FIRST, whole: /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-18_nexusai-gate28-batch-rd476-rd856-rd857.md
It opens with AMENDMENT 1 (main is 888203c, not the predicted 2facd7c; the landing chain 36a0dc0 -> 5eb80a7 -> 888203c is checked by ancestry, never by a first-parent walk, because 888203c's FIRST parent is 2facd7c; the MAIN pin is stamped, not predicted; item D added), the item list, THE RE-PIN STEP, the stamp lines, PIN-HEADS, the TIER argument, the drafter's WRONG OR UNVERIFIED list (each item MEASURED or READ-ONLY-INFERRED), then TUESDAY'S RULINGS (T1 to T8 as Tuesday stamped them, the commission's properties for A/B/C and for D, the carried rulings) and THE MODEL RULE: apply them, do not re-rule them. Then the charter it names; the FOUR READY copies in briefs/ (2026-10-19_nexusai-gate28-READY-rd476-r2.txt, -rd856.txt, -rd857.txt, -c170-delta.txt), each read WHOLE; Tuesday's ANSWER-6, -8, -9, -10 (tiers, the guard ruling), ANSWER-16, ANSWER-18 and ANSWER-19 (the land that made 888203c, and why C-170's land waits on THIS gate's D verdict); the clarifications the brief quotes, at source; gate 25's ADDENDUM-1 (the ref order); gates 22, 23, 24, 25 and 26's section 3a (the H-rules, carried by reference); gate 25's and gate 26's reports on THIS drive (gate 26's is the record of C-170's product verdict and of the 19 suites). Every builder statement is a CLAIM — RELAYED, never evidence. The brief's section 2a rows (r0 to r9, r10P, r10R, r10N, r11 to r13, and D's d0 to d6), section 2b (the user-lookup guards as classifiers) and section 3b (the sweep) are required measurement.

THE MODEL RULE (Kam, live board 2026-09-30 09:07, card (b)): QA gates may switch to Opus 4.8 when flagged by the running model's safeguards, PER SESSION. You start on the model Tuesday stamped (named at the end of this prompt; Opus 5.5 is the model the rule was written for). You run the FULL rows. If one of your responses is stopped by the safeguards: that step is NOT RUN (never re-worded to slip past); write ONE line to evidence/classifier-stops.txt; let any running step finish and let the hold exit so you never sit holding a lock (H-28); mail tuesday-agent@agentmail.to with the subject exactly "[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch"; then end your turn with the line "PARKED: flagged — awaiting the Opus 4.8 switch" and wait. Tuesday switches THIS pane's model and taps you by mail. You never answer the model dialog yourself, and nobody ever chooses "Switch automatically". After the switch, resume at the stopped row. The report states which rows ran on which model, with the switch time, and quotes classifier-stops.txt whole.

THE PROPERTIES (brief section 2a). For A, B and C: (1) THE MERGE ROW r1: in your own --mirror store (T6: create your g28 refs FIRST — including g28/d0 and g28/d1, since f15217c is named only by a remote-tracking ref in the NexusAI repo — then remove origin, then prove each), merge-tree --write-tree of M0 and each head must conflict in scripts/verify-expected-counts.json ONLY (the drafter's legacy stdout-only read against 888203c: the counts section is the only one with conflict markers for all three); the stack B then B+C; both landing orders compared path by path; the counts-only TURN each landing needs and the counts it would carry; positive control first (your method reproduces gate 25's e2bb3ac from cd171f9 + 36a0dc0 with the seat's counts blob) and a negative control. (2) THE WORDING ROW r2 (A): the shipped prompt EQUALS the Kam-approved words and nothing else changed, by full-text classification with a planted-word control, and r3 the prompt a booted server sends is that prompt. (3) THE RED-PROOF ROWS r4 to r6: revert each fix, its named cells RED for the named reason, restore GREEN; the mutants; RD-857's differential over your OWN corpus of at least 120 questions. (4) THE SUITE ROW r8: full verifies per T2, names as SETS against M0's; C-57 through a byte-identical COPY of the installed runner with C57_ROOT pointing at your own shim (T1), C-133 through a copy of the installed tool. (5) THE CODEQL ROW r7 on #91, #92, #93 with PR #58 as the control. (6) THE INTERACTION ROWS: r9 (the shared preload, existing cells, C-102), r10P THE PROVIDER ROW — RD-794 has LANDED on M0, so the new suites' LLM_PROVIDER ollama boot is now measurable: record the fallback warning, the provider the preload reports, and whether RD-476's override cell (seeded under aiTuning_ollama) exercises the active key or pins nothing; r10R the cross-change routing (the absent-data question routes to the model only once RD-856 is in); r10N RD-476's headline question never reached a real model: NOT RUN, named — the gate makes no model call. (7) SECRETS and DEPLOY r11, r12. For D: d0 SCOPE — exactly the 4 test paths and no product byte, with a planted product byte as the control that would show; d1 EQUIVALENCE — per site, old regex vs new built from the REAL constants in your own tree, source and behaviour equal on the literal and on near-misses, re-derived by you (the builder's equivalence file is METHOD only); d2 RED-FIRST — the touched cells red on mutants of the marketplace package build script (the builder's M1 to M5 and M5c design, RE-RUN in your own clone; M4 is NOT proof for #267, the builder's own finding; M5 with M5c as its control is #267's proof), restored green; d3 gate 26's 19 suites BY NAME; d4 the C-102 sweep for the delta; d5 CodeQL on refs/pull/96/head — 0 new with a control, #266 to #271 read BY NUMBER on that ref, "fixed" there is the PR ref's state and never a main closure (C-209); d6 the statement that C-170's PRODUCT was gated by gate 26 and this item gates only the test delta, D's merge into main not part of this gate.

MAIN MUST NOT MOVE (ruling b): the launcher verified origin main equals the stamped MAIN pin exactly, that 888203c, 5eb80a7 and 36a0dc0 are in its ancestry with their trees, that its tree equals the stamped tree, and that C-170 is not on it; take M0 by git ls-remote at YOUR start and say so. If main moves mid-gate (RD-778's land is the likeliest mover; C-170's is HELD behind your D verdict, so a C-170 move is itself a finding), every merged tree is stale: name what landed, finish nothing that would read as a verdict on the new main, and mail a QUESTION (C-68). GitHub SSH intermittently denies auth (C-192): retry every ls-remote up to 5 times about 10 s apart; a FAILED ls-remote is UNKNOWN, never a value. Re-hash the lock tool, the C-57 runner and the C-133 tool at start, mid and end.

C-190 + its ADDENDUM — BOTH thresholds block: every merge to main goes through a pull request that adds no new high-or-higher CodeQL alert in changed code (test code included), AND any new alert whose RULE severity is error blocks whatever its security severity. Alerts are fixed in code, never dismissed. C-209: a PR's CodeQL run cannot show a pre-existing main alert as fixed. CodeQL is NOT RUN by this gate on any tree — say so. C-185 (ruling h): read its known set at source; any other failure is by NAME; no re-run is a clearance.

THE LOCK (C-63). The installed tool is session-tools/nexusai-lock.sh in the NexusAI project on this drive, sha256 3c33f5ae58e1be20282467a90b27a23a2de998eedd0e56c03f3c06360031a792. While the T9 is unmounted the base is NEXUSAI_LOCK_BASE=/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/session-tools/locks-laptop-1017, which the launcher has EXPORTED into your environment: keep it on every jest step and every server boot, quote the c57 runner's resolved LOCK_BASE= and ROOT= line, and never touch this drive's stale session-tools/locks (a 2026-09-22 holder lives there). If the T9 mounts mid-gate, finish the running hold, file nothing more, and mail a QUESTION. EVERY jest run and every booted server goes in the jest lock, each hold tagged qa-g28- (no tag of yours contains the word "merge": C-141 ADDENDUM 7), ONE hold at a time. MERGES GO FIRST and RULING (i)'s BY-HAND GATE YIELD IS RETIRED: if a ticket is queued ahead of you, wait behind it (FIFO) — the builder S101O and gate 27 file jest holds on the same base. AT A WAIT DEADLINE: --replace on your own still-waiting ticket BEFORE its deadline fires (C-141: a SAME-PLACE handover), confirmed from the queue listing (the old ticket to released/ as ticket-left-*, your place unchanged); a duplicate-tag refusal takes a -r<N> suffix. Read queue-jest at start, around every hold and at end; any qa-g28- entry that is not your current hold is a STOP. Read your inbox before filing every new hold. THE LOAD RULE: file a hold or start any full jest only below a 1-minute load of 8 (8 cores; Tuesday's ANSWER-1 to S101O); record uptime beside each.

NODE_MODULES WITHOUT THE HOST REGISTRY (ruling m, H-31): offline npm ci --offline --ignore-scripts --no-audit --no-fund with --cache pointing at an APFS clone of the local npm cache on the same volume; M0, every merged tree and f15217c share lock 19477a9, so ONE proven install is APFS-cloned into the others; EVERY npm invocation carries npm_config_update_notifier=false (prove the cache copy's _update-notifier-last-checked marker absent or unchanged); an ENOTCACHED is NOT RUN, named, with a QUESTION — never go online from the host, never npm install. sqlite3's binding from the cached prebuild (an APFS clone of ~/.npm/_prebuilds), inside the strict belt, IS PART OF H-31, with its three conditions (the tarball's and the unpacked node_sqlite3.node's sha256; CI builds its own Linux binding; every row that boots a server names "sqlite3 binding: cached prebuild, offline"). proxy-addr must resolve 2.0.8 from each tree's own path (RD-827, C-205).

FULL VERIFIES (r8, and V4 only if T2 (b) is ruled for D) through the jest lock, UNBELTED by Tuesday's 2026-10-05 answer to gate 14 (ruling n), with its four conditions. SESSION_SECRET UNSET, npm_config_update_notifier=false npm run verify -- --maxWorkers=2 --forceExit (prove the flag reached jest), on this machine's Node as T5 rules. RULING (b) and its EXTENSION (ruling o): if a verify stays lock-starved about 2 h after filing, deliver it NAMED NOT RUN — never "skipped" — with the brief's coverage sentence in NOT TESTED. The wording, red-proof, interaction and D rows are NOT covered by that extension: a verdict whose wording (r2), red-proof (r4 to r6, d2), interaction (r9, r10P, r10R) or D equivalence (d1) rows did not run is PROVISIONAL and releases nothing. A revert, plant or mutant counts only if it LANDED (the exact text present, the original absent) and parses; a red from a mutant that never landed is a VOID arm, a planted control that does not fire makes its row VOID (never a pass), and an edit whose anchor is absent fails loudly and nothing downstream runs on that tree.

THE INSTRUMENT RULES H-1 TO H-36 (brief section 3a; gates 22, 23, 24, 25 and 26's section 3a read WHOLE). H-1: the ONLY SESSION_SECRET printer is the one the brief quotes; self-test it and gate 26's scan. H-3: a LANDING CONTROL for every plant, revert and mutant. H-4: the HEARTBEAT is a separate child of the hold wrapper, aborted if absent 90 s after the grant, max gap reported. H-6: every path with a space quoted; every host jest run but the full verifies, every driver and every booted server under your copy of the belt with its landing control. H-9: byte plants by Buffer, checked with xxd. H-11/H-18: /bin/bash explicitly, "${sha}:${path}" quoted (zsh eats :s and :a — the amendment drafter lost a read to it). H-14: every driver ends END ok or END VOID with a reason. H-17: censuses by pgrep, never ps. H-20: a per-step hard DEADLINE on every jest run (with --forceExit), every runner invocation, every npm ci and every server boot (qa-to.sh). H-21: every file you mutate is restored by a trap on EXIT (also INT and TERM) installed BEFORE the first mutation, hash-compared to its pin (the package build script's blob 40ec7de3 for D's mutants). H-22: never nest sandbox-exec (it exits 71). H-24: jest array options after the paths, lists built in bash. H-26: C-192 retries. H-27: THE MODEL RULE. H-28: ONE focused hold at a time, at most about 40 minutes planned (T1's runner holds excepted), rows GROUPED, a hold that would overrun SPLIT, every part file bash -n checked before filing; you stay in the FOREGROUND — a hold that must outlive one tool call runs as a TRACKED child of your session (never nohup) with its timeout at the 2-hour maximum; each hold carries a wait deadline and you --replace before it fires. H-29: other gates' and the builders' evidence is method only. H-31: offline host node_modules. H-32: every booted server is a local run of your tree on loopback by the gate — NOT the demo; no HTTP to any production or demo host. H-33: never rm — quarantine (T1's disclosed runner exception only); every child reaped by pid. H-34: the Laptop-DEV lock base. H-35: NO docker object and NO az command, not even az version, and NO call to any real model or Azure OpenAI endpoint — the RD-395 stand-in answers.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT (fresh mktemp dirs under projects/nexusai/qa-trees/gate28.* in /Volumes/Laptop-DEV/!CODING/Testing Agent MAIN): ONE --mirror clone of the NexusAI repo on THIS drive as your store (T6), your refs g28/* in it made BEFORE origin is removed, your merge commits in it, every work tree a clone of that store, status-checked before use, EXCLUSIVE to one purpose. NEVER work in the NexusAI root checkout or any worktrees/ folder (LIVE, the builder's). In the NexusAI repo use ONLY read verbs (show, diff, log with an explicit rev, ls-tree, cat-file, grep, ls-remote, rev-parse, merge-base, rev-list, count-objects, for-each-ref); NEVER fetch, pull, push, checkout, worktree, commit, stash, gc, merge, merge-tree --write-tree or hash-object -w there. Copy instruments BY NAME from gate 26's evidence/inst and gate 25's evidence/inst on THIS drive (never the whole directory; qa-lockcheck.py and qa-names23.py are in gate 25's, not gate 26's — the amendment's correction), re-point every gate-25/26 path in your copies to gate 28 — INCLUDING the lock base line (quote that diff) — and correct the floor library's ROOT and NEG defaults from the live list below; never write into another gate's dirs (gates 25 and 26 are COMPLETE, gate 27 is LIVE: all read-only to you). Never write into the builders' session-tools (S101O is live in s101/: hash it at start and end); never run the seats' scripts in place (above all run-live.js, which spends money). Findings-only: never push, no commits outside your store, no tickets, no PRs, no edits in NexusAI. No Microsoft, Log Analytics or login host, no demo, no Partner Center, no workflow dispatch, no repo variable written. No mail to any human. Never rm: quarantine.

FLOOR DISCIPLINE — section 9 of the brief exactly. Do ALL lock-free work first (pins, hashes, reads, r0, r1's rebuilds and their controls, r2, r7, r11, r12, r13, d0, d1, d4, d5, the offline npm ci, the self-tests); then file your holds one at a time through your COPY of gate 26's qa-file26.sh re-pointed to qa-g28 tags and the jest kind (the suggested grouping is H1 to H8 in section 3a). QUEUE, NEVER TAKE OVER: never signal, move or edit another seat's or gate's process, lock, ticket or worktree. Count foreign servers the C-125 way anchored on YOUR OWN claude pid, with the negative-control seats the launcher derived (listed at the end of this prompt) classifying foreign in the same run; re-derive them at every hold's start; a hold with no live negative control aborts. A zero is reportable only beside a control that fired in the same window. DEADLINE AND HEARTBEAT: every step has a per-step DEADLINE, every child is killed in a finally by pid from your own ancestry (C-174, never by pattern), a HEARTBEAT line at least every 2 minutes during a hold, and a step with no heartbeat for 5 minutes is aborted and reported; every booted server stopped by its own pid and its port read free afterwards.

RE-PIN at start, mid and end: main and the four branches (rd-476-assistant-prompt-s101o, rd-856-user-pattern-verb-guard-s101o, rd-857-whole-word-skip-list-s101o, rd-460-c170-turn-s101o), refs/pull/91, 92, 93 and 96 head, plus the three tools' sha256 — three timestamped readings with the branch name and attempt count beside each sha. A head that disagrees with the brief is a FINDING and a reason to stop, never a typo to fix. Call main at your start M0 and say so. Count the NexusAI .git/objects files and their newest mtime at start and end and account for any delta (the amendment drafter read 44 files at 07:18 AEDT on 2026-10-19).

QUESTIONS: your routing name is QA/NexusAI-gate28. If you must ask, mail tuesday-agent@agentmail.to with subject "[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>" and PROCEED ON THE SAFEST READING without waiting (the one exception is a safeguards stop, which PARKS you under THE MODEL RULE); Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/NexusAI-gate28] ANSWER". Approval-class items (anything Azure, any real model call, the demo, Partner Center, money, a human, the live lock tool) are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your ONE report to the path the launcher names at the end of this prompt (the brief's section 11). Write its VERDICT and FINDINGS table early and keep it current. Findings are G28-<n>, notes N28-<n>, each naming its instrument and evidence class.

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with the subject exactly:
[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — gate 28
Lead the body with the FOUR lines in the form the brief's section 11 gives — RD-476, RD-856+RD-857 STACK, C-170 DELTA (one verdict line per item) and ORDER/TURN — then one line naming M0 and END main, the C-102 sweep, which rows ran on which model, which holds ran and which are NAMED NOT RUN under ruling (o) extended, the real-model check NOT RUN (r10N), and "CodeQL NOT RUN on any merged tree". The report's last four lines are those same four lines. Never wednesday-agent@. You have no inbox that wakes you, so a verdict you do not mail is lost.
The AgentMail key is AGENTMAIL_API_KEY in /Volumes/Laptop-DEV/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no 4_Credentials directory of its own. Never put the key, a token, a session value or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice — the only turn you end while waiting is the PARKED line of THE MODEL RULE.

Rule 2 stands: what you did NOT test is first-class output — a NOT TESTED section carrying the builders' stated limits, every declared limit L-C1 to L-C7, L-D1 to L-D3 and L-Y1 discharged with a measurement or left standing and named (C-112), Prior work checked (C-49), every finding naming its instrument, and every action recommendation labelled MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. The tester never fixes. C-190 with its ADDENDUM, C-209, C-57, C-133, C-185 with its ADDENDA, C-192, C-199, C-205, C-141 with ADDENDA 6 and 7, C-63, C-40, C-68, C-76, C-102, C-112 and C-174 are the clarifications this gate leans on; C-49, C-89, C-115, C-125, C-130, C-131 and C-203 are carried. That section must carry, verbatim, the NOT TESTED line the launcher appends at the end of this prompt (it is the brief's section 11 line).
PROMPT_EOF

# ---------------------------------------------------------------- GUARDS
[ -d "$QA_DIR" ]  || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]   || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -n "$PROMPT" ]  || { echo "embedded prompt is empty" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }

STAMP_OK=1          # cleared below by any unstamped slot the guards meet; the refusal itself is LAST (32S)
PROVISIONAL=''      # what --check ran against provisionally while a slot was unstamped

# 9 / MODEL — the kit's stamped MODEL line, validated against models_latest.json (sonnet or opus level); never typed from memory.
MODEL_LINE="$(grep -E '^MODEL \(tier 2' "$BRIEF" | head -1)"
[ -n "$MODEL_LINE" ] || { echo "REFUSING: the brief has no 'MODEL (tier 2 …' line" >&2; exit 9; }
MODEL_OK_IDS="$(python3 -c 'import json,sys; L=json.load(open(sys.argv[1]))["levels"]; print(" ".join(L[k]["model_id"] for k in ("sonnet","opus") if k in L))' "$MODELS_JSON" 2>/dev/null)"
[ -n "$MODEL_OK_IDS" ] || { echo "REFUSING: $MODELS_JSON levels.sonnet / levels.opus are unreadable" >&2; exit 9; }
if printf '%s' "$MODEL_LINE" | grep -qF "$PH_SLOT"; then
  STAMP_OK=0; MODEL=''; PROVISIONAL="$PROVISIONAL MODEL(unstamped)"
else
  MODEL="$(printf '%s' "$MODEL_LINE" | sed -E 's/.*: *`?([a-z0-9.-]+)`? *$/\1/')"
  case " $MODEL_OK_IDS " in *" $MODEL "*) ;; *) echo "REFUSING: the stamped MODEL '$MODEL' is not one of models_latest.json's sonnet/opus ids ($MODEL_OK_IDS) — re-stamp the MODEL line with the bare model ID" >&2; exit 9 ;; esac
fi

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
[ "$(printf '%s\n' "$PIN" | wc -l | tr -d ' ')" = "5" ] || { echo "REFUSING: PIN-HEADS must carry exactly five rows (MAIN RD476 RD856 RD857 C170D)" >&2; exit 40; }
for ID in MAIN RD476 RD856 RD857 C170D; do
  R="$(prow "$PIN" "$ID")"
  [ "$(printf '%s\n' "$R" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: PIN-HEADS must carry exactly one row '$ID'" >&2; exit 40; }
  [ "$(printf '%s\n' "$R" | awk -F'\t' '{print NF}')" = "7" ] || { echo "REFUSING: PIN-HEADS row $ID does not have 7 cells: $R" >&2; exit 40; }
  [ "$(pfld "$PIN" "$ID" 7)" = "IN" ] || { echo "REFUSING: PIN-HEADS row $ID status is not IN" >&2; exit 40; }
  [ "$(pfld "$PIN" "$ID" 2)" = "nexusai" ] || { echo "REFUSING: PIN-HEADS row $ID repo must be nexusai" >&2; exit 40; }
  [ "$ID" = "MAIN" ] && continue
  printf '%s' "$R" | grep -q '@' && { echo "REFUSING: PIN-HEADS row $ID still carries a placeholder" >&2; exit 40; }
  is40 "$(pfld "$PIN" "$ID" 4)" || { echo "REFUSING: PIN-HEADS row $ID head is not a 40-hex sha" >&2; exit 40; }
done
[ "$(pfld "$PIN" RD476 3)" = "$B476" ] && [ "$(pfld "$PIN" RD476 4)" = "$H476" ] && [ "$(pfld "$PIN" RD476 5)" = "$OLD_MAIN" ] && [ "$(pfld "$PIN" RD476 6)" = "2" ] \
  || { echo "REFUSING: PIN-HEADS RD476 is not $B476 @ f9649dc, base c7ca0ed, 2 commits — re-pin kit AND launcher" >&2; exit 40; }
[ "$(pfld "$PIN" RD856 3)" = "$B856" ] && [ "$(pfld "$PIN" RD856 4)" = "$H856" ] && [ "$(pfld "$PIN" RD856 5)" = "$OLD_MAIN" ] && [ "$(pfld "$PIN" RD856 6)" = "1" ] \
  || { echo "REFUSING: PIN-HEADS RD856 is not $B856 @ f4026fb, base c7ca0ed, 1 commit — re-pin kit AND launcher" >&2; exit 40; }
[ "$(pfld "$PIN" RD857 3)" = "$B857" ] && [ "$(pfld "$PIN" RD857 4)" = "$H857" ] && [ "$(pfld "$PIN" RD857 5)" = "$OLD_MAIN" ] && [ "$(pfld "$PIN" RD857 6)" = "2" ] \
  || { echo "REFUSING: PIN-HEADS RD857 is not $B857 @ 1da0bd4, base c7ca0ed, 2 commits — re-pin kit AND launcher" >&2; exit 40; }
[ "$(pfld "$PIN" C170D 3)" = "$BD" ] && [ "$(pfld "$PIN" C170D 4)" = "$HD1" ] && [ "$(pfld "$PIN" C170D 5)" = "$HD0" ] && [ "$(pfld "$PIN" C170D 6)" = "1" ] \
  || { echo "REFUSING: PIN-HEADS C170D is not $BD @ f15217c, base fd8ff2a, 1 commit — re-pin kit AND launcher" >&2; exit 40; }
[ "$(pfld "$PIN" MAIN 3)" = "main" ] || { echo "REFUSING: PIN-HEADS MAIN row is not branch main" >&2; exit 40; }
PIN_MAIN="$(pfld "$PIN" MAIN 4)"
STAMP_LINE="$(grep -E '^MAIN-STAMP: ' "$BRIEF")"
[ "$(printf '%s\n' "$STAMP_LINE" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: the brief must carry exactly one 'MAIN-STAMP: ' line" >&2; exit 40; }
MAIN_STAMPED=1
if printf '%s' "$STAMP_LINE$PIN_MAIN" | grep -qF "$PH_SLOT"; then
  MAIN_STAMPED=0; STAMP_OK=0
else
  S_SHA="$(printf '%s' "$STAMP_LINE" | sed -nE 's/^MAIN-STAMP: sha `?([0-9a-f]{40})`? \| tree `?([0-9a-f]{40})`? \| landed since 888203c: (.+)$/\1/p')"
  S_TREE="$(printf '%s' "$STAMP_LINE" | sed -nE 's/^MAIN-STAMP: sha `?([0-9a-f]{40})`? \| tree `?([0-9a-f]{40})`? \| landed since 888203c: (.+)$/\2/p')"
  S_LANDED="$(printf '%s' "$STAMP_LINE" | sed -nE 's/^MAIN-STAMP: sha `?([0-9a-f]{40})`? \| tree `?([0-9a-f]{40})`? \| landed since 888203c: (.+)$/\3/p')"
  is40 "$S_SHA" && is40 "$S_TREE" && [ -n "$S_LANDED" ] || { echo "REFUSING: the MAIN-STAMP line is not 'MAIN-STAMP: sha <40-hex> | tree <40-hex> | landed since 888203c: <text>'" >&2; exit 40; }
  [ "$PIN_MAIN" = "$S_SHA" ] || { echo "REFUSING: PIN-HEADS MAIN ($PIN_MAIN) and the MAIN-STAMP sha ($S_SHA) disagree — stamp the same sha in both" >&2; exit 40; }
fi

# 18T — the T9 MOUNTED refuses: two lock bases would split the FIFO (ruling q); Tuesday decides the base first.
[ ! -d "$T9_VOL" ] || { echo "REFUSING: $T9_VOL is MOUNTED — the brief's lock base (locks-laptop-1017) assumes it is not; Tuesday decides the base, then re-brief" >&2; exit 18; }

# 18 — RE-PIN NOW by ls-remote (C-192 retries): main = the stamped MAIN pin EXACTLY; each branch = its pin; the PR refs (NOTE).
lsr refs/heads/main "refs/heads/$B476" "refs/heads/$B856" "refs/heads/$B857" "refs/heads/$BD" refs/pull/91/head refs/pull/92/head refs/pull/93/head refs/pull/96/head \
  || { echo "REFUSING: git ls-remote origin failed after $LSR_ATTEMPTS attempt(s) — UNKNOWN, not a value (C-192); relaunch later" >&2; exit 18; }
LSR_ALL="$LSR_OUT"
ref_now() { printf '%s\n' "$LSR_ALL" | awk -v r="$1" '$2==r{print $1}'; }
M_ORIGIN="$(ref_now refs/heads/main)"
is40 "$M_ORIGIN" || { echo "REFUSING: origin main is unreadable in the ls-remote output — UNKNOWN (C-192)" >&2; exit 18; }
[ "$M_ORIGIN" != "$OLD_MAIN" ] || { echo "REFUSING: origin main is c7ca0ed — never gate onto c7ca0ed under this kit" >&2; exit 18; }
if [ "$MAIN_STAMPED" = "1" ]; then
  [ "$M_ORIGIN" = "$S_SHA" ] || { echo "REFUSING: origin main is '${M_ORIGIN:0:12}', not the stamped MAIN pin '${S_SHA:0:12}' — main MOVED since stamp; re-stamp the MAIN pin (never sed a sha blindly)" >&2; exit 18; }
  MAIN_SHA="$S_SHA"
else
  MAIN_SHA="$M_ORIGIN"; PROVISIONAL="$PROVISIONAL MAIN(unstamped: guards ran against origin main ${M_ORIGIN:0:12})"
fi
for pair in "$B476 $H476" "$B856 $H856" "$B857 $H857" "$BD $HD1"; do
  set -- $pair
  [ "$(ref_now "refs/heads/$1")" = "$2" ] || { echo "REFUSING: origin $1 is '$(ref_now "refs/heads/$1")', not ${2:0:7} — the head MOVED; re-pin kit AND launcher (a new head is a new brief)" >&2; exit 18; }
done
for pair in "91 $H476" "92 $H856" "93 $H857" "96 $HD1"; do
  set -- $pair
  [ "$(ref_now "refs/pull/$1/head")" = "$2" ] || echo "NOTE: refs/pull/$1/head is '$(ref_now "refs/pull/$1/head")', not ${2:0:7} — PR #$1 moved; the gate reads it" >&2
done
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 6 — every sha the guards use is a commit in the local object store (this launcher never fetches).
for S in "$MAIN_SHA" "$FLOOR_MAIN" "$L761" "$L775" "$OLD_MAIN" "$H476" "$R1_476" "$H856" "$H857" "$HD0" "$HD1" "$G26SEAT"; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: ${S:0:12} is not a commit in $REPO (got '$T') — this launcher never fetches; the seat's next fetch brings it, then re-check" >&2; exit 6; }
done

# 18M — M0's LANDING CHAIN by ANCESTRY (never --first-parent: 888203c's FIRST parent is 2facd7c) + trees; M0's tree = the stamp; C-170 NOT on M0.
[ "$(tree_of "$L761")" = "$T761" ] && [ "$(tree_of "$L775")" = "$T775" ] && [ "$(tree_of "$FLOOR_MAIN")" = "$FLOOR_TREE" ] \
  || { echo "REFUSING: 36a0dc0 / 5eb80a7 / 888203c are not trees fb8197a / 2d2caa3 / 428f042 (the measured landing chain)" >&2; exit 18; }
for S in "$OLD_MAIN" "$L761" "$L775" "$FLOOR_MAIN"; do
  g merge-base --is-ancestor "$S" "$MAIN_SHA" 2>/dev/null || { echo "REFUSING: ${S:0:7} is not in M0 ${MAIN_SHA:0:7}'s ANCESTRY — M0 is not a descendant of the measured landing chain c7ca0ed -> 36a0dc0 -> 5eb80a7 -> 888203c" >&2; exit 18; }
done
M0_TREE="$(tree_of "$MAIN_SHA")"
if [ "$MAIN_STAMPED" = "1" ]; then
  [ "$M0_TREE" = "$S_TREE" ] || { echo "REFUSING: M0 ${MAIN_SHA:0:7}'s tree is '${M0_TREE:0:12}', not the stamped tree '${S_TREE:0:12}'" >&2; exit 18; }
fi
for S in "$H460" "$HD0" "$HD1" "$G26SEAT"; do
  if g merge-base --is-ancestor "$S" "$MAIN_SHA" 2>/dev/null; then echo "REFUSING: C-170 commit ${S:0:7} is on M0 ${MAIN_SHA:0:7} — ANSWER-19 holds C-170's land behind THIS gate's D verdict; re-brief" >&2; exit 18; fi
done
[ -z "$(blob "$MAIN_SHA" "$ARMTTK")" ] || { echo "REFUSING: arm-ttk.yml is present at M0 — a C-170 land; re-brief" >&2; exit 18; }
LANDED_N="$(g rev-list --count "${FLOOR_MAIN}..${MAIN_SHA}" 2>/dev/null)"
if [ "$MAIN_SHA" != "$FLOOR_MAIN" ]; then
  echo "NOTE: M0 ${MAIN_SHA:0:7} is $LANDED_N commit(s) past 888203c — what landed: $(g log --format='%h %s' "${FLOOR_MAIN}..${MAIN_SHA}" 2>/dev/null | head -5 | cut -c1-90 | tr '\n' ';')" >&2
  if [ "$MAIN_STAMPED" = "1" ] && [ "$(printf '%s' "$S_LANDED" | tr '[:upper:]' '[:lower:]')" = "none" ]; then echo "REFUSING: M0 is not 888203c but the MAIN-STAMP says 'landed since 888203c: none' — name what landed" >&2; exit 18; fi
fi
FP_FB="$(g log --first-parent --format='%T' "$MAIN_SHA" 2>/dev/null | grep -cxF "$T761")"
[ "$FP_FB" = "0" ] || echo "NOTE: a --first-parent walk from M0 now reaches tree fb8197a ($FP_FB) — the ancestry check above still decides" >&2

# 7 / 8 — the heads' chains: merge base c7ca0ed for A/B/C; linear commit counts; the stack; no head already on M0; D's one commit on fd8ff2a.
for pair in "$H476 2" "$H856 1" "$H857 2"; do
  set -- $pair
  [ "$(g merge-base "$1" "$MAIN_SHA" 2>/dev/null)" = "$OLD_MAIN" ] || { echo "REFUSING: merge-base(${1:0:7}, M0) is not c7ca0ed — a head was rebased or landed; re-brief" >&2; exit 7; }
  if g merge-base --is-ancestor "$1" "$MAIN_SHA" 2>/dev/null; then echo "REFUSING: ${1:0:7} is ALREADY on M0 — re-brief" >&2; exit 7; fi
  [ "$(g rev-list --count "${OLD_MAIN}..${1}" 2>/dev/null)" = "$2" ] && [ -z "$(g rev-list --merges "${OLD_MAIN}..${1}" 2>/dev/null)" ] \
    || { echo "REFUSING: ${1:0:7} is not $2 linear commit(s) over c7ca0ed" >&2; exit 8; }
done
[ "$(parents_of "$H476")" = "$R1_476" ] || { echo "REFUSING: f9649dc's parent is not RD-476 r1 393929057997" >&2; exit 8; }
[ "$(parents_of "$H857")" = "$H856" ] || { echo "REFUSING: 1da0bd4's parent is not f4026fb — the stack C-on-B is broken" >&2; exit 8; }
[ "$(parents_of "$HD1")" = "$HD0" ] && [ "$(parents_of "$HD0")" = "$G26SEAT $FLOOR_MAIN" ] && [ "$(tree_of "$HD1")" = "$TD1" ] \
  || { echo "REFUSING: D is not f15217c (tree a0da892) on fd8ff2a, whose parents are 88153c0 + 888203c" >&2; exit 8; }

# 90 — the INSTALLED lock tool PINNED; it honours NEXUSAI_LOCK_BASE; the Laptop-DEV base is present with queue-jest; no qa-g28 ticket.
INST_NOW="$(fsha "$LOCKTOOL")"
[ "$INST_NOW" = "$LOCK_SHA_INST" ] || { echo "REFUSING: the INSTALLED lock tool's sha256 is '${INST_NOW:-absent}', not 3c33f5ae… — find out who changed it; re-brief" >&2; exit 90; }
grep -qF 'BASE="${NEXUSAI_LOCK_BASE:-' "$LOCKTOOL" || { echo "REFUSING: the installed tool no longer honours NEXUSAI_LOCK_BASE — ruling q's premise" >&2; exit 90; }
bash -n "$LOCKTOOL" 2>/dev/null || { echo "REFUSING: $LOCKTOOL does not parse (bash -n)" >&2; exit 90; }
grep -qF -- '--replace' "$LOCKTOOL" && grep -qF 'jest|docker) ;;' "$LOCKTOOL" || { echo "REFUSING: $LOCKTOOL lacks --replace or the jest kind" >&2; exit 90; }
[ -d "$LOCK_BASE_LAPTOP" ] && [ -d "$LOCKQ_J" ] || { echo "REFUSING: the Laptop-DEV lock base $LOCK_BASE_LAPTOP (queue-jest) is not present (ruling q)" >&2; exit 90; }
BQ="$(grep -l '^tag=qa-g28' "$LOCKQ_J"/* 2>/dev/null | wc -l | tr -d ' ')"
[ "${BQ:-0}" = "0" ] || { echo "REFUSING: $BQ qa-g28* ticket(s) already in $LOCKQ_J — a live or stale gate-28 ticket; read before launch" >&2; exit 90; }
GQ="$(grep -lE '^tag=qa-g' "$LOCKQ_J"/* 2>/dev/null | wc -l | tr -d ' ')"
[ "${GQ:-0}" = "0" ] || echo "NOTE: $GQ other-gate qa- ticket(s) queued — FIFO; gate 28 waits behind them, never touches them" >&2
HOLDER="$(sed -n 's/^tag=//p' "$LOCK_BASE_LAPTOP/nexusai-jest.lock/owner" 2>/dev/null | head -1)"
case "$HOLDER" in
  qa-g28*) echo "REFUSING: the Laptop-DEV jest lock is HELD by '$HOLDER' — a gate-28 holder already exists" >&2; exit 90 ;;
  '') ;;
  *) echo "NOTE: the Laptop-DEV jest lock is held now by '$HOLDER' (FIFO; the gate waits behind it)" >&2 ;;
esac
LB_WAS="${NEXUSAI_LOCK_BASE:-}"
[ -z "$LB_WAS" ] || [ "$LB_WAS" = "$LOCK_BASE_LAPTOP" ] || echo "NOTE: NEXUSAI_LOCK_BASE was '$LB_WAS' in the launcher's environment — REPLACED by the Laptop-DEV base before exec (ruling q)" >&2

# 91 — the C-57 runner and the C-133 tool PINNED, and the runner's ROOT / LOCK_BASE / rm premises that T1 rests on.
C57_NOW="$(fsha "$C57TOOL")"; C133_NOW="$(fsha "$C133TOOL")"
[ "$C57_NOW" = "$C57_SHA" ] || { echo "REFUSING: c57-id-superset.sh sha256 is '${C57_NOW:-absent}', not 1ae84a10…5581 — re-brief" >&2; exit 91; }
[ "$C133_NOW" = "$C133_SHA" ] || { echo "REFUSING: c133-accounting.py sha256 is '${C133_NOW:-absent}', not 6f938bfc…f972f — re-brief" >&2; exit 91; }
grep -qF 'if [ -n "${C57_ROOT:-}" ]; then ROOT="$C57_ROOT"' "$C57TOOL" && grep -qF 'LOCK_BASE="${NEXUSAI_LOCK_BASE:-' "$C57TOOL" \
  && grep -qF 'rm -rf "$wt"' "$C57TOOL" && grep -qF 'worktree remove --force "$wt"' "$C57TOOL" \
  || { echo "REFUSING: the C-57 runner's C57_ROOT / LOCK_BASE / rm / worktree lines are not as T1 describes" >&2; exit 91; }

# 22 — the gated file sets; the both-sides sets vs M0; the legacy merge-tree's conflict-marker sections = the counts file ONLY; D's 4 paths.
[ "$(paths_of "$OLD_MAIN" "$H476")" = "$(sorted "$GATED_476")" ] || { echo "REFUSING: RD-476's gated files (c7ca0ed..f9649dc) are not the briefed 4" >&2; exit 22; }
[ "$(paths_of "$OLD_MAIN" "$H856")" = "$(sorted "$GATED_856")" ] || { echo "REFUSING: RD-856's gated files are not the briefed 3" >&2; exit 22; }
[ "$(paths_of "$OLD_MAIN" "$H857")" = "$(sorted "$GATED_857")" ] || { echo "REFUSING: RD-857's gated files (over c7ca0ed) are not the briefed 4" >&2; exit 22; }
[ "$(both_sides "$OLD_MAIN" "$MAIN_SHA" "$H476")" = "$(sorted "$BOTH_476")" ] || { echo "REFUSING: RD-476's both-sides set vs M0 is '$(both_sides "$OLD_MAIN" "$MAIN_SHA" "$H476")', not preload + model-config + counts (WRONG 2)" >&2; exit 22; }
for H in "$H856" "$H857"; do
  [ "$(both_sides "$OLD_MAIN" "$MAIN_SHA" "$H")" = "$(sorted "$BOTH_BC")" ] || { echo "REFUSING: ${H:0:7}'s both-sides set vs M0 is '$(both_sides "$OLD_MAIN" "$MAIN_SHA" "$H")', not server.js + counts (WRONG 2)" >&2; exit 22; }
done
GD="$(g rev-parse --absolute-git-dir 2>/dev/null)"
OBJ_BEFORE="$(find "$GD/objects" -type f 2>/dev/null | wc -l | tr -d ' ')"
for H in "$H476" "$H856" "$H857"; do
  MC="$(mt_conflicts "$OLD_MAIN" "$MAIN_SHA" "$H")"
  [ "$MC" = "$COUNTS_FILE" ] || { echo "REFUSING: the legacy merge-tree of ${H:0:7} onto M0 shows conflict markers in '${MC:-nothing}', not the counts file ONLY (WRONG 2) — a non-counts conflict is a STOP; re-brief" >&2; exit 22; }
done
OBJ_AFTER="$(find "$GD/objects" -type f 2>/dev/null | wc -l | tr -d ' ')"
[ "$OBJ_BEFORE" = "$OBJ_AFTER" ] || echo "NOTE: NexusAI .git/objects went $OBJ_BEFORE -> $OBJ_AFTER around the legacy merge-tree reads — the trivial-merge mode writes none; a live seat may have" >&2
[ "$(paths_of "$HD0" "$HD1")" = "$(sorted "$GATED_D")" ] || { echo "REFUSING: D's paths (fd8ff2a..f15217c) are not the briefed 4 test paths" >&2; exit 22; }
[ "$(g diff --name-only "$HD0" "$HD1" -- . ':(exclude)__tests__' 2>/dev/null | grep -c .)" = "0" ] || { echo "REFUSING: D changes a path outside __tests__ — a product byte (ANSWER-19: no product byte changes)" >&2; exit 22; }
[ "$(comm -12 <(g diff --name-only "$HD0" "$HD1" | sort) <( (g diff --name-only "$OLD_MAIN" "$H476"; g diff --name-only "$OLD_MAIN" "$H857") | sort -u) | grep -c .)" = "0" ] \
  || { echo "REFUSING: D's paths intersect A/B/C's — the batch is no longer file-disjoint" >&2; exit 22; }

# 93 — the premises at source: counts + the RECOMPUTED predictions, blobs, prompt shas, the provider premise (r10P), D's premises.
[ "$(counts_at "$OLD_MAIN")" = "4559 287" ] && [ "$(counts_at "$H476")" = "4594 288" ] && [ "$(counts_at "$H856")" = "4566 288" ] && [ "$(counts_at "$H857")" = "4581 289" ] \
  || { echo "REFUSING: head counts are not 4559/287 (c7ca0ed), 4594/288 (A), 4566/288 (B), 4581/289 (C) (WRONG 9)" >&2; exit 93; }
[ "$(blob "$OLD_MAIN" "$COUNTS_FILE")" = "$CB_BASE" ] && [ "$(blob "$HD0" "$COUNTS_FILE")" = "$CB_D" ] && [ "$(blob "$HD1" "$COUNTS_FILE")" = "$CB_D" ] && [ "$(counts_at "$HD1")" = "4807 298" ] \
  || { echo "REFUSING: counts blobs are not fadda68 (c7ca0ed) / 0e50ac0 = 4807/298 (fd8ff2a and f15217c) (WRONG 9, 16)" >&2; exit 93; }
M0C="$(counts_at "$MAIN_SHA")"; M0T="${M0C% *}"; M0S="${M0C#* }"
printf '%s' "$M0C" | grep -Eq '^[0-9]+ [0-9]+$' || { echo "REFUSING: M0's counts file is unreadable" >&2; exit 93; }
[ "$MAIN_SHA" != "$FLOOR_MAIN" ] || [ "$M0C" = "4660 291" ] || { echo "REFUSING: 888203c's counts are '$M0C', not 4660/291 (WRONG 9)" >&2; exit 93; }
PRED="V1=M0+A $((M0T+35))/$((M0S+1)) · M0+B $((M0T+7))/$((M0S+1)) · V2=M0+B+C $((M0T+22))/$((M0S+2)) · V3=M0+A+B+C $((M0T+57))/$((M0S+3))"
for S in "$MAIN_SHA" "$H476" "$H856" "$H857" "$HD1"; do
  [ "$(blob "$S" "$LOCK")" = "$LOCK_BLOB" ] && [ "$(blob "$S" "$PKG")" = "$PKG_BLOB" ] && [ "$(blob "$S" "$DEPLOY_WF")" = "$DEPLOY_BLOB" ] \
    || { echo "REFUSING: ${S:0:7} does not carry lockfile 19477a9 / package.json 384805d / deploy-demo.yml 953b2a2 (ruling m, r12)" >&2; exit 93; }
done
[ "$(cntF "$MAIN_SHA" "$DEPLOY_WF" "vars.CI_DEPLOY_ENABLED == 'true'")" = "2" ] || { echo "REFUSING: deploy-demo.yml at M0 no longer gates BOTH jobs on vars.CI_DEPLOY_ENABLED == 'true' (r12)" >&2; exit 93; }
[ "$(prompt_of "$OLD_MAIN")" = "$PROMPT_BASE_LEN $PROMPT_BASE_SHA" ] && [ "$(prompt_of "$MAIN_SHA")" = "$PROMPT_BASE_LEN $PROMPT_BASE_SHA" ] \
  && [ "$(prompt_of "$R1_476" | cut -d' ' -f2)" = "$PROMPT_R1_SHA" ] && [ "$(prompt_of "$H476")" = "$PROMPT_R2_LEN $PROMPT_R2_SHA" ] \
  || { echo "REFUSING: SYSTEM_PROMPT is not 7686/666399e1 at c7ca0ed AND at M0, 70c48fc2 at r1, 9956/f36881dd at f9649dc (WRONG 4) — M0 changed the prompt? re-brief" >&2; exit 93; }
[ "$(cntF "$MAIN_SHA" model-config.js 'LLM_PROVIDER=ollama now resolves to azure-openai with one boot warning.')" = "1" ] \
  && [ "$(cntF "$MAIN_SHA" "$PRELOAD" "if (require(path.join(REPO, 'model-config.js')).getLLMConfig().provider === 'azure-openai') {")" = "1" ] \
  || { echo "REFUSING: M0's model-config.js / preload no longer carry RD-794's ollama -> azure-openai fallback + checkDeployment stand-in (r10P's premise)" >&2; exit 93; }
[ "$(cntF "$H476" __tests__/rd476-assistant-prompt.test.js "LLM_PROVIDER: 'ollama',")" = "1" ] && [ "$(cntF "$H856" __tests__/rd856-user-pattern-pronoun-lead.test.js "LLM_PROVIDER: 'ollama',")" = "1" ] \
  && [ "$(cntF "$H857" __tests__/rd857-user-skip-list-whole-word.test.js "LLM_PROVIDER: 'ollama',")" = "1" ] && [ "$(cntF "$H476" __tests__/rd476-assistant-prompt.test.js "const KEY = 'aiTuning_ollama';")" = "1" ] \
  || { echo "REFUSING: the three new suites no longer boot LLM_PROVIDER 'ollama' or the override cell no longer seeds aiTuning_ollama (WRONG 5, r10P)" >&2; exit 93; }
[ "$(cntF "$MAIN_SHA" "$SERVER" 'aiTuning_${provider}')" -ge 2 ] || { echo "REFUSING: M0's server no longer keys AI tuning as aiTuning_\${provider} (r10P)" >&2; exit 93; }
[ "$(cntF "$H856" "$SERVER" "const NON_NAME_LEADS = ['we', 'our', 'ours', 'us', 'i', 'my', 'me', 'you', 'your', 'it', 'its',")" = "1" ] \
  && [ "$(cntF "$H857" "$SERVER" 'function captureIsDepartmentOrLocation(')" = "1" ] && [ "$(cntF "$H857" "$SERVER" 'break userLookup;')" -ge 1 ] \
  || { echo "REFUSING: RD-856's NON_NAME_LEADS or RD-857's captureIsDepartmentOrLocation / break userLookup are not at their heads as briefed (§1)" >&2; exit 93; }
[ "$(cntF "$HD1" __tests__/helpers/escape-regexp.js "return String(s).replace(/[.*+?^\${}()|[\\]\\\\]/g, '\\\\\$&');")" = "1" ] \
  || { echo "REFUSING: D's helper is not the standard full escape String(s).replace(/[.*+?^\${}()|[\\]\\\\]/g, '\\\\\$&') (WRONG 16)" >&2; exit 93; }
[ "$(cntF "$HD1" __tests__/helpers/shipped-plan-build.js "const DEV = 'nexusaidevacrfa39.azurecr.io/nexusai:2.1.0';")" = "1" ] || { echo "REFUSING: shipped-plan-build.js's DEV constant moved (#271, d1)" >&2; exit 93; }
[ "$(blob "$HD0" "$BUILDSH")" = "$BUILDSH_BLOB" ] && [ "$(blob "$HD1" "$BUILDSH")" = "$BUILDSH_BLOB" ] || { echo "REFUSING: $BUILDSH is not blob 40ec7de3 at fd8ff2a and f15217c (d2's restore pin)" >&2; exit 93; }
[ "$(g show "${HD1}:${BUILDSH}" 2>/dev/null | sed -n '73p' | grep -cF 'already holds')" = "1" ] && [ "$(g show "${HD1}:${BUILDSH}" 2>/dev/null | sed -n '255p' | grep -cF 'carries container image')" = "1" ] \
  && [ "$(g show "${HD1}:${BUILDSH}" 2>/dev/null | sed -n '281p' | grep -cF 'is neither')" = "1" ] && [ "$(g show "${HD1}:${BUILDSH}" 2>/dev/null | sed -n '174p' | grep -cF 'chk(')" = "1" ] \
  || { echo "REFUSING: d2's mutant anchors (:73 already holds, :174 chk(, :255 carries container image, :281 is neither) moved in $BUILDSH at f15217c" >&2; exit 93; }
for s in $SUITES19; do [ -n "$(blob "$HD1" "__tests__/$s.test.js")" ] || { echo "REFUSING: gate 26's suite $s is absent at f15217c (d3)" >&2; exit 93; }; done
g show "${HD1}:package.json" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); sys.exit(0 if "/__tests__/helpers/" in d.get("jest",{}).get("testPathIgnorePatterns",[]) else 1)' \
  || { echo "REFUSING: jest's testPathIgnorePatterns at f15217c no longer ignores /__tests__/helpers/ (WRONG 16)" >&2; exit 93; }

# 70 — the carried rulings and Tuesday's answers (REFUSALs where a ruling is missing).
[ -s "$SQLITE_RULING" ] && grep -qF 'The offline unpack of sqlite3' "$SQLITE_RULING" || { echo "REFUSING: Tuesday's sqlite3 prebuild ruling (ruling m) is not at $SQLITE_RULING" >&2; exit 70; }
[ -s "$BELT_ANS" ] && grep -qF 'run UNBELTED. Every other jest run stays belted: cells, mutants, C-68 unions, drivers and servers.' "$BELT_ANS" \
  || { echo "REFUSING: Tuesday's belt answer (ruling n) is not at $BELT_ANS as quoted" >&2; exit 70; }
[ -s "$NOTIFIER_ANS" ] && grep -qF 'Every later npm invocation in this gate carries npm_config_update_notifier=false' "$NOTIFIER_ANS" \
  || { echo "REFUSING: Tuesday's notifier answer (ruling m) is not at $NOTIFIER_ANS as quoted" >&2; exit 70; }
[ -s "$RULING_B" ] && grep -qF 'Deliver the verdict NOW.' "$RULING_B" || { echo "REFUSING: Tuesday's ruling (b) is not at $RULING_B as quoted" >&2; exit 70; }
grep -qF 'NOT RUN, named, under ruling (o) EXTENDED' "$BRIEF25" && grep -qF 'NOT RUN, named, under ruling (o) EXTENDED' "$BRIEF" \
  || { echo "REFUSING: ruling (o)'s EXTENSION words are not carried in gate 25's brief and this brief" >&2; exit 70; }
[ -s "$G19_RELEASE" ] && grep -qF 'the by-hand gate yield (ruling (i)) is RETIRED from gate 21 on.' "$G19_RELEASE" || { echo "REFUSING: gate 19's RELEASE no longer carries the yield retirement" >&2; exit 70; }
[ -s "$ANS1" ] && grep -qF 'load1 below 8 before every heavy run' "$ANS1" && grep -qF 'lock base locks-laptop-1017' "$ANS1" || { echo "REFUSING: Tuesday's ANSWER-1 (load 8, lock base) is not at $ANS1 as quoted" >&2; exit 70; }
while IFS='|' read -r F Q; do
  [ -n "$F" ] || continue
  [ -s "$F" ] && grep -qF -- "$Q" "$F" || { echo "REFUSING: '$Q' is no longer in $F — the ruling moved; re-brief" >&2; exit 70; }
  grep -qF -- "$Q" "$BRIEF" || { echo "REFUSING: the brief does not quote '$Q' verbatim" >&2; exit 70; }
done <<EOF_ANS
$ANS6|RD-476 is tier 2 (customer-facing words; no security surface, no route or page change)
$ANS8|tier 2 (routing only, no answer text changed, no security surface)
$ANS9|This is a routing fix inside Tuesday's authority
$ANS10|an UNKNOWN name sharing a word with a department or location gets the normal model answer instead of the not-found text, which is acceptable
$ANS18|RD-794 land ACCEPTED, no delta gate.
$ANS19|the changed test bytes get a tier-2 through-code delta check as an extra item of gate 28
EOF_ANS
[ -s "$ANS19" ] && grep -qF "Land C-170 only on that verdict + Tuesday's GO." "$ANS19" && grep -qF 'Then HOLD the land' "$ANS19" || { echo "REFUSING: ANSWER-19 no longer holds C-170's land behind this gate" >&2; exit 70; }
[ -s "$ANS18" ] && grep -qF "main = $FLOOR_MAIN" "$ANS18" || { echo "REFUSING: ANSWER-18 no longer names main 888203c" >&2; exit 70; }
[ -s "$ANS16" ] || { echo "REFUSING: ANSWER-16 (the landing order) is absent at $ANS16" >&2; exit 70; }
[ -s "$ADD25" ] && grep -qF 'BEFORE you run `git remote remove origin`' "$ADD25" || { echo "REFUSING: gate 25's ADDENDUM-1 (the ref order) is not at $ADD25" >&2; exit 70; }

# 70N — machine-local premises, NOTEd (the gate records what it finds).
if [ -d "$NPM_CACHE/index-v5" ]; then
  grep -r -l -F -m1 -- 'proxy-addr/-/proxy-addr-2.0.8.tgz' "$NPM_CACHE/index-v5" >/dev/null 2>&1 || echo "NOTE: the local npm cache index has no proxy-addr 2.0.8 — the offline npm ci (H-31) may ENOTCACHE" >&2
else
  echo "NOTE: no local npm cache at $NPM_CACHE — H-31's offline install has no source; the gate will mail a QUESTION" >&2
fi
PB_NOW="$(fsha "$PREBUILD")"
[ "$PB_NOW" = "$PREBUILD_SHA" ] || echo "NOTE: the cached sqlite3 prebuild is '${PB_NOW:-absent}', not 84a34404…7afc — ruling (m)'s condition 1 records what the gate finds" >&2
NODEV="$(node -v 2>/dev/null)"
[ "$NODEV" = "v26.8.1" ] || echo "NOTE: host node is '${NODEV:-absent}', not v26.8.1 as briefed (T5) — the gate records it" >&2
GLV="$(gitleaks version 2>/dev/null)"
[ "$GLV" = "8.30.1" ] || echo "NOTE: gitleaks is '${GLV:-absent}', not 8.30.1 — r11 records it" >&2
LOAD1="$(sysctl -n vm.loadavg 2>/dev/null | awk '{print $2}')"
awk -v l="${LOAD1:-99}" 'BEGIN{exit !(l < 8)}' || echo "NOTE: 1-minute load is ${LOAD1:-unknown} (not below 8) — the gate waits in the queue, never in a hold (ruling p)" >&2

# 31 — the FOUR READY copies (sha256 PINNED), builder evidence, gate 25's and gate 26's instruments (THIS drive), standing references.
for f in "$READY_476" "$READY_856" "$READY_857" "$READY_D" "$CLAR" "$BRIEF22" "$BRIEF23" "$BRIEF24" "$BRIEF25" "$BRIEF26" "$TEMPLATE" "$B25_REPORT" "$B26_REPORT" "$CHARTER" \
         "$S101/rd476-prompts/prompt-OLD-c7ca0ed.txt" "$S101/rd476-prompts/prompt-NEW-rd476.txt" "$S101/rd476-prompts/prompt-NEW-rd476-r2.txt" "$S101/rd476-live/side-by-side.md" \
         "$S101/c170-delta-equiv.out" "$S101/c170-delta/M5.out" "$S101/c170-delta/M5c.out" "$S101/c170-delta/suites19.out" \
         "$B26_INST/qa-file26.sh" "$B26_INST/qa-file26r.sh" "$B26_INST/qa-floorlib26.sh" "$B26_INST/qa-h1-scan26.py" "$B26_INST/qa-h1-selftest26.sh" "$B26_INST/qa-mail26.py" \
         "$B26_INST/qa-mailread26.py" "$B26_INST/qa-c57shim26.sh" "$B26_INST/qa-to.sh" "$B26_INST/qa-floorcount.py" "$B26_INST/qa-netbelt.sb" "$B26_INST/qa-netbelt-nodns.sb" \
         "$B25_INST/qa-applymut.py" "$B25_INST/qa-probe25.js" "$B25_INST/qa-lockcheck.py" "$B25_INST/qa-names23.py"; do
  [ -s "$f" ] || { echo "REFUSING: evidence, brief or tool absent: $f" >&2; exit 31; }
done
for pair in "$READY_476|$READY_476_SHA" "$READY_856|$READY_856_SHA" "$READY_857|$READY_857_SHA" "$READY_D|$READY_D_SHA"; do
  F="${pair%%|*}"; W="${pair#*|}"
  [ "$(fsha "$F")" = "$W" ] || { echo "REFUSING: the READY copy $F is not the amendment's saved body (sha256 ${W:0:12}…) — re-read it from the inbox" >&2; exit 31; }
  grep -qF "$W" "$BRIEF" || { echo "REFUSING: the brief does not name the READY sha256 $W" >&2; exit 31; }
done
grep -qF "$H476" "$READY_476" && grep -qF 'verify: PASS 4594/4594 across 288 suites.' "$READY_476" && grep -qF "$H856" "$READY_856" && grep -qF "$H857" "$READY_857" \
  && grep -qF "$HD1" "$READY_D" && grep -qF 'READY FOR QA: C-170 delta' "$READY_D" && grep -qF 'So M4 is NOT proof for #267' "$READY_D" \
  || { echo "REFUSING: a READY copy no longer names its head / verify line / the M4 caveat" >&2; exit 31; }
grep -qF 'STATUS: COMPLETE' "$B25_REPORT" && grep -qF 'STATUS: COMPLETE' "$B26_REPORT" || { echo "REFUSING: gate 25's / 26's report does not read as delivered (the instrument sources must be DELIVERED gates)" >&2; exit 31; }
grep -qF 'C-170 AS MERGED: GO WITH FINDINGS @ M170 ab3ae67 tree 0f4602e' "$B26_REPORT" || { echo "REFUSING: gate 26's report no longer carries C-170's product verdict (d6's premise)" >&2; exit 31; }
for B in "$BRIEF22" "$BRIEF23" "$BRIEF24" "$BRIEF25" "$BRIEF26"; do grep -qF '## 3a. INSTRUMENT RULES' "$B" || { echo "REFUSING: $B has no section 3a — the H-rules carried by reference are missing" >&2; exit 31; }; done
for f in qa-lockcheck.py qa-names23.py; do [ ! -e "$B26_INST/$f" ] || echo "NOTE: $f now exists in gate 26's inst/ — the kit's correction (gate 25's inst/) still names a valid source" >&2; done

# 10 / 17 — the report path from the brief's §11 (its date is a stamped slot); no stale report; the brief names its sources.
REPORT_RAW="$(grep -oE 'Report: `[^`]*/report\.md`' "$BRIEF" | head -1 | sed -E 's/^Report: `//; s/`$//')"
[ -n "$REPORT_RAW" ] || { echo "REFUSING: the brief's §11 has no 'Report: \`…/report.md\`' line" >&2; exit 10; }
if printf '%s' "$REPORT_RAW" | grep -qF "$PH_SLOT"; then
  STAMP_OK=0; REPORT=''; PROVISIONAL="$PROVISIONAL REPORT_DATE(unstamped)"
else
  printf '%s' "$REPORT_RAW" | grep -Eq "^$RPTS/20[0-9]{2}-[0-9]{2}-[0-9]{2}-gate28-batch-rd476-rd856-rd857/report\.md$" \
    || { echo "REFUSING: the report path '$REPORT_RAW' is not $RPTS/<YYYY-MM-DD>-gate28-batch-rd476-rd856-rd857/report.md" >&2; exit 10; }
  REPORT="$REPORT_RAW"
  [ "$(grep -oF "$(dirname "$REPORT")" "$BRIEF" | grep -c .)" -ge 2 ] || { echo "REFUSING: T4 and §11 do not name the SAME report directory (stamp one date in both)" >&2; exit 10; }
  [ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }
fi
for P in "2026-10-19_nexusai-gate28-READY-rd476-r2.txt" "2026-10-19_nexusai-gate28-READY-rd856.txt" "2026-10-19_nexusai-gate28-READY-rd857.txt" "2026-10-19_nexusai-gate28-READY-c170-delta.txt" \
         "2026-10-19_S101O_ANSWER-18_rd794-accepted-c170-turn.md" "2026-10-13_nexusai-gate-batch22.md" "2026-10-16_nexusai-gate-batch23.md" "2026-10-17_nexusai-gate24-rd848.md" \
         "2026-10-18_nexusai-gate25-rd761-rd794-merged.md" "2026-10-18_nexusai-gate26-c170-be0fe37-merged.md" "2026-10-05_qa_b14_belt_ANSWER.md" "2026-10-06_nexusai_g18_ruling_b_deliver_now.md" \
         "qa-file26.sh" "qa-file26r.sh" "qa-applymut.py" "QA_AGENT_CHARTER.md" "locks-laptop-1017" "ADDENDUM-1" ".pre-amend" "c170-delta-equiv.out" "models_latest.json"; do
  grep -qF "$P" "$BRIEF" || { echo "REFUSING: brief must name $P" >&2; exit 10; }
done

# 11 — identity: NexusAI's OWN dirs.
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || { echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"
[ -d "$CLAUDE_CONFIG_DIR" ] || { echo "REFUSING: Tuesday's claude store $CLAUDE_CONFIG_DIR is absent" >&2; exit 11; }

# 12 / 13 / 14 / 15 / 20 — tier, directive, brief path, pins, verdict route, key path, question route.
for T in 'TIER 2' 'AMENDMENT 1' 'MAIN-STAMP' 'NO GO' 'NO HOST NPM REGISTRY' 'FULL VERIFIES UNBELTED' 'EXTENSION' 'npm_config_update_notifier=false' 'BOTH thresholds block' 'RULING (b)' \
         '--replace' 'qa-g28-' 'RETIRED' 'H-34' 'H-35' 'C-63' 'C-209' 'THE MERGE ROW' 'THE WORDING ROW' 'THE DELIVERY ROW' 'THE SUITE ROW' 'THE CODEQL ROW' 'THE INTERACTION ROW' \
         'THE PROVIDER ROW' 'THE CROSS-CHANGE ROUTING' 'NOT RUN, NAMED' 'THE SECRETS ROW' 'THE DEPLOY ROW' 'D — SCOPE' 'D — EQUIVALENCE' 'D — RED-FIRST' 'D — THE 19 SUITES' 'D — CODEQL' 'D — THE STATEMENT' \
         'M4 is NOT proof for #267' 'VOID' 'can fail' 'positive control' 'negative control' 'G28-<n>' 'NOT TESTED' 'PRIOR WORK' 'No HTTP to any production or demo host' 'never by `--first-parent`'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not declare '$T'" >&2; exit 12; }
done
for T in 'TIER-2 BATCH' 'THE PROPERTIES' 'THE MERGE ROW' 'THE WORDING ROW' 'THE SUITE ROW' 'THE CODEQL ROW' 'THE PROVIDER ROW' 'r10P' 'r10R' 'r10N' 'd0' 'd1' 'd2' 'd3' 'd4' 'd5' 'd6' \
         'C-170 TEST DELTA' "C-170's PRODUCT was gated by gate 26" 'M4 is NOT proof for #267' 'M5c' 'refs/pull/96/head' '#266 to #271' 'BY NUMBER' 'AMENDMENT 1' 'ancestry' 'as SETS' 'C-209' \
         'UNBELTED' 'npm_config_update_notifier=false' 'BOTH thresholds block' 'RULING (b)' 'EXTENSION' 'NAMED NOT RUN' '--replace' 'qa-g28-' 'RETIRED' 'locks-laptop-1017' 'jest lock' \
         'T1' 'T2' 'T5' 'T6' "Never trust the builders' trees" 'no HTTP to any production or demo host' 'One client only' 'NO docker object and NO az' 'no model call'; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare '$T'" >&2; exit 12 ;; esac
done
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
for S in "$H476" "$H856" "$H857" "$HD0" "$HD1" "$OLD_MAIN" "$LOCK_SHA_INST"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S in full" >&2; exit 14; }
  case "$PROMPT" in *"$S"*) ;; *) echo "REFUSING: prompt must name $S" >&2; exit 14 ;; esac
done
for S in "$FLOOR_MAIN" "$FLOOR_TREE" "$L761" "$L775" "$T761" "$T775" "$TD1" "$CB_D" "$C57_SHA" "$C133_SHA" "$PKG_BLOB" "$LOCK_BLOB" "$DEPLOY_BLOB" "$PREBUILD_SHA" "$BUILDSH_BLOB" "$PROMPT_R2_SHA"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S in full" >&2; exit 14; }
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
[ "$(grep -oE 'qa-g28-[A-Za-z0-9_<>-]*merge[A-Za-z0-9_-]*' "$BRIEF" | grep -c .)" = "0" ] || { echo "REFUSING: the brief suggests a qa-g28- tag containing 'merge' (C-141 ADDENDUM 7)" >&2; exit 15; }
[ "$(printf '%s\n' "$PROMPT" | grep -oE 'qa-g28-[A-Za-z0-9_<>-]*merge' | grep -c .)" = "0" ] || { echo "REFUSING: the prompt suggests a qa-g28- tag containing 'merge'" >&2; exit 15; }

# 41 — RULING (i)'s by-hand yield is RETIRED.
for T in 'stop YOUR OWN unstarted waiter' 'stop your OWN unstarted waiter' 'then re-queue with --after that merge' 'self-apply ONE yield per gate TAG'; do
  if grep -qF -- "$T" "$BRIEF" || printf '%s\n' "$PROMPT" | grep -qF -- "$T"; then echo "REFUSING: '$T' instructs the RETIRED by-hand yield" >&2; exit 41; fi
done
grep -qF 'THE BY-HAND GATE YIELD IS RETIRED' "$BRIEF" || { echo "REFUSING: the brief does not carry the retirement of ruling (i)'s yield" >&2; exit 41; }
case "$PROMPT" in *"BY-HAND GATE YIELD IS RETIRED"*) ;; *) echo "REFUSING: the prompt does not say the by-hand gate yield is RETIRED" >&2; exit 41 ;; esac

# 82 — THE MODEL RULE is carried in the brief and the prompt, per session, never "Switch automatically".
for T in "$STATUS_SUBJ" "$PARK_LINE" 'classifier-stops.txt' 'Switch automatically' 'Opus 4.8' 'PER SESSION' 'which rows ran on which model'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks THE MODEL RULE fragment '$T'" >&2; exit 82; }
  case "$(printf '%s' "$PROMPT" | tr '[:upper:]' '[:lower:]')" in *"$(printf '%s' "$T" | tr '[:upper:]' '[:lower:]')"*) ;; *) echo "REFUSING: prompt lacks THE MODEL RULE fragment '$T'" >&2; exit 82 ;; esac
done
grep -qF '## THE MODEL RULE' "$BRIEF" && grep -qF 'H-27' "$BRIEF" && grep -qF 'H-28 (AMENDED' "$BRIEF" && grep -qF 'H-34 (THE LOCK BASE' "$BRIEF" && grep -qF 'H-35 (NO DOCKER, NO AZ, NO MODEL' "$BRIEF" \
  || { echo "REFUSING: brief lacks THE MODEL RULE section or H-27/H-28 (amended)/H-34/H-35" >&2; exit 82; }

# 19 — the words the prompt must carry (% is a space); the brief's sections; limits; rows; T-slot form; clarification quotes.
WORDS="RD-476 RD-856 RD-857 RD-794 RD-778 C-170 C-190 C-209 C-57 C-133 C-185 C-192 C-199 C-205 C-141 C-63 C-40 C-68 C-76 C-102 C-112 C-174 C-49 C-89 C-115 C-125 C-130 C-131 C-203 ADDENDA%6%and%7
r1 r2 r3 r8 r9 r10P r10R r10N r11 d0 d1 d2 d3 d4 d5 d6 M0 888203c c7ca0ed 36a0dc0 5eb80a7 2facd7c 19477a9 proxy-addr PR%#91 PR%#92 PR%#93 PR%#96 PR%#58 #266 #271 M1 M5 M5c 40ec7de3
L-C1 L-C7 L-D1 L-D3 L-Y1 H-1 H-3 H-4 H-6 H-9 H-14 H-17 H-20 H-21 H-22 H-24 H-26 H-27 H-28 H-29 H-31 H-32 H-33 H-34 H-35 --forceExit trap%on%EXIT DEADLINE LANDING%CONTROL
_prebuilds node_sqlite3.node sqlite3%binding:%cached%prebuild,%offline _update-notifier-last-checked exits%71 --mirror EXCLUSIVE STOP VOID C57_ROOT g28/d0 g28/d1 LLM_PROVIDER aiTuning_ollama
MERGES%GO%FIRST QUEUE,%NEVER%TAKE%OVER SAME-PLACE%handover HEARTBEAT 2%minutes 5%minutes finally SESSION_SECRET%UNSET NOT%TESTED MEASURED%AT%RUNTIME READ%ONLY PROBED
RELAYED CodeQL%is%NOT%RUN UNKNOWN about%40%minutes 2-hour%maximum TRACKED%child Prior%work FOREGROUND never%push NEVER%merge Partner%Center npm%install --offline ENOTCACHED
qa-file26.sh ticket-left-* -r<N> instrument never%fixes GROUPED SPLIT never%dismissed PROVISIONAL qa-g28 G28-<n> N28-<n> 1-minute%load%of%8 S101O run-live.js first-parent"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## TIER' '^## WRONG OR UNVERIFIED' "^## TUESDAY'S RULINGS" '^## THE MODEL RULE' '^## Charter' '^## THE CLARIFICATIONS THAT BIND THIS GATE' '^## PRIOR ROUND' '^## 1. Target' \
         '^### How to build your trees' '^## 2. Tier and severity' '^## 2a. ROWS' '^## 2b. THE USER-LOOKUP GUARDS' '^## 3. THE QUESTIONS' '^## 3a. INSTRUMENT RULES' '^## 3b. THE NEGATIVE-ASSERTION SWEEP' \
         '^## 7. THE MERGED TREES' '^## 8. CI, ALERTS, DEPLOY' '^## 9. Floor discipline' '^## 10. HELD' '^## 11. Output' '^## PROVENANCE' '^## FILL AT STAMP'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
WSTART="$(grep -n '^## WRONG OR UNVERIFIED' "$BRIEF" | cut -d: -f1)"; WEND="$(grep -n "^## TUESDAY'S RULINGS" "$BRIEF" | cut -d: -f1)"
[ "$WSTART" -lt "$WEND" ] || { echo "REFUSING: the WRONG OR UNVERIFIED section is not above TUESDAY'S RULINGS" >&2; exit 19; }
WUNMARKED="$(sed -n "${WSTART},${WEND}p" "$BRIEF" | grep -E '^[0-9]+\. ' | grep -vE 'MEASURED|READ-ONLY-INFERRED|own actions' | cut -c1-60)"
[ -z "$WUNMARKED" ] || { echo "REFUSING: WRONG items not marked MEASURED / READ-ONLY-INFERRED: $WUNMARKED" >&2; exit 19; }
for L in L-C1 L-C2 L-C3 L-C4 L-C5 L-C6 L-C7 L-D1 L-D2 L-D3 L-Y1; do grep -qF "$L" "$BRIEF" || { echo "REFUSING: brief lacks declared limit $L (C-112)" >&2; exit 19; }; done
for R in r0 r1 r2 r3 r4 r5 r6 r7 r8 r9 r10P r10R r10N r11 r12 r13 d0 d1 d2 d3 d4 d5 d6; do grep -qF "| $R |" "$BRIEF" || { echo "REFUSING: brief lacks row $R" >&2; exit 19; }; done
for n in 1 2 3 4 5 6 7 8; do
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
every existing test that relied on a LATER return in that function is a candidate for silent disarmament
A declared limit is where the evidence stops — not a place it is cleared.
NEVER KILL BY PATTERN.
Every merge to NexusAI main goes through a PULL REQUEST, and a PR must add NO NEW high-or-higher CodeQL alert in the code it changes. Test code is included.
`alerts_threshold = errors`, so ANY new alert whose RULE severity is `error` blocks, whatever its security severity.
A PR's CodeQL run CANNOT show a PRE-EXISTING main alert as fixed
A merge conflict confined to `scripts/verify-expected-counts.json` is resolved by regeneration, with an id-superset control.
counts as known ONLY when the received object differs from the expected in `envReached` alone
No re-run is used as a clearance
is a SAME-PLACE handover.
TAG CONVENTION — only a merge HOLD's tag contains the word `merge`.
Gate (`qa-*`) tickets are never moved; the holder is never touched.
A merge hold runs on a node_modules that matches the merged tree's package-lock.json.
RD-709 is built STACKED on RD-736 (`61e20ad`), and RD-736 merges BEFORE RD-709.
a clean merge-tree and a changed measured surface are not in tension
CLAR_EOF

# 24 — the prompt must DESCRIBE the server entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qi 'backend/server\.js'; then
  echo "REFUSING: the prompt contains the server entry point's literal path (RD-591 c.37901). Describe it; do not name it." >&2; exit 24; fi

# 53 / 71 — standing rules in the brief; the NOT TESTED line read from the brief (ONE line), carrying D's clauses; appended to the prompt at exec.
for w in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' 'qa-g28-' 'VOID' 'EXCLUSIVE' 'POSITIVE CONTROL FIRST' 'QUEUE, NEVER TAKE OVER' 'LANDING CONTROL' \
         '--replace' 'never push' 'C-174' '--forceExit' 'trap … EXIT' 'MERGES GO FIRST' 'queue-jest/' 'carry on' 'never idles holding a lock' \
         'ONE focused hold at a time' 'FOREGROUND' 'Never two live holds' 'Every finding names its instrument' \
         'NOT TESTED' 'The tester never fixes' 'SPLIT a hold' 'ONE CLIENT ONLY' 'no CodeQL alert dismissed' 'below a 1-minute load of **8**'; do
  grep -qiF -- "$w" "$BRIEF" || { echo "REFUSING: brief lacks the standing rule '$w'" >&2; exit 53; }
done
NOTTESTED_LINE="$(grep -E '^  Not tested by this gate: ' "$BRIEF" | sed 's/^  //')"
[ "$(printf '%s\n' "$NOTTESTED_LINE" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: the brief must carry exactly ONE '  Not tested by this gate: …' line (§11)" >&2; exit 71; }
for w in "any real model's behaviour under the new system prompt" 'CodeQL and the CI Build on any merged tree' 'the full jest suite on Node 24' "C-170's product (gated by gate 26, not re-gated)" \
         'the released build and MANIFEST reproduction on f15217c' "C-170's merge into main with its post-land checks" 'Windows'; do
  case "$NOTTESTED_LINE" in *"$w"*) ;; *) echo "REFUSING: the brief's NOT TESTED line lacks '$w'" >&2; exit 71 ;; esac
done
grep -qF 'The report'"'"'s LAST four lines are the four verdict lines' "$BRIEF" || { echo "REFUSING: brief must fix the report's last lines as the four verdict lines" >&2; exit 71; }
for V in '`RD-476: <GO|GO WITH FINDINGS|NO GO> @ f9649dcf' '`RD-856+RD-857 STACK: <GO|GO WITH FINDINGS|NO GO> @ 1da0bd46' '`C-170 DELTA: <GO|GO WITH FINDINGS|NO GO> @ f15217cb' '`ORDER/TURN: B before C'; do
  grep -qF -- "$V" "$BRIEF" || { echo "REFUSING: the brief's §11 lacks the verdict line '$V'" >&2; exit 71; }
done

# 76 / 77 / 78 / 79 — H-1's printer and forbidden idioms; H-4; H-9; H-7/H-8.
grep -qF "$SAFE_PRINTER" "$BRIEF" || { echo "REFUSING: brief must carry the safe SESSION_SECRET printer verbatim (H-1)" >&2; exit 76; }
for w in '${SESSION_SECRET-…}' '${SESSION_SECRET:-…}' '${SESSION_SECRET+$SESSION_SECRET}' 'printenv'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief must name the forbidden idiom $w (H-1)" >&2; exit 76; }
done
for w in 'separate child' 'within 90 s' 'max gap'; do grep -qiF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the heartbeat fragment '$w' (H-4)" >&2; exit 77; }; done
for w in 'H-9' 'Buffer' 'xxd -l 16'; do grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the byte-plant fragment '$w' (H-9)" >&2; exit 78; }; done
for w in 'H-7/H-8' 'negative control' 'FAILS LOUDLY'; do grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the mutant-landing fragment '$w' (H-7/H-8)" >&2; exit 79; }; done

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
for NAME in Datasec/NexusAI-M Datasec/NexusAI-N Datasec/NexusAI-O Datasec/NexusAI-P Datasec/NexusAI-R "$COORD_NAME"; do
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
[ "$NEG_BUILDERS" -ge 1 ] || { echo "REFUSING: no live builder seat among Datasec/NexusAI-M/N/O/P/R — at least ONE negative control is required" >&2; exit 38; }
# fleet-monitor and every live 'QA/*' pane other than this gate's own (gate 27 included): a negative control when exactly one claude runs under it.
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

# 86 — no live gate-28 session already exists.
for P in $(pane_pid_of "$ROUTE_NAME"); do
  if [ -n "$(claude_under "$P")" ]; then echo "REFUSING: a pane named $ROUTE_NAME (pid $P) already runs a claude — gate 28 is live; do not start a second session" >&2; exit 86; fi
  [ "$CHECK" = "1" ] || echo "NOTE: a pane named $ROUTE_NAME (pid $P) exists with no claude under it — the cockpit's own add decides" >&2
done

# 32S / 40 — LAST: the coordinator's stamp (0 at-sign SLOT placeholders anywhere in the kit: MAIN pin, MODEL, REPORT_DATE, RULED: T1-T8, SELF-CHECK +
# note; the SELF-CHECK line in the fleet's form), and the answer route (Tuesday adds it, never this launcher).
NSLOT="$(grep -oF "$PH_SLOT" "$BRIEF" | grep -c .)"
if [ "$NSLOT" != "0" ] || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then STAMP_OK=0; fi
ROUTE_OK=1
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || ROUTE_OK=0
GUARDS='9 MODEL 40 18T 18 6 18M 7 8 90 91 22 93 70 70N 31 10 17 11 12 13 14 15 20 41 82 19 24 53 71 76 77 78 79 38R 86'
SUMMARY="ls-remote attempts this run: $LSR_ATTEMPTS (C-192); origin main ${M_ORIGIN:0:7} (M0 ${MAIN_SHA:0:7} tree ${M0_TREE:0:7}; ancestry carries 36a0dc0/fb8197a, 5eb80a7/2d2caa3, 888203c/428f042; C-170 not on M0); RD-476 ${H476:0:7}; RD-856 ${H856:0:7}; RD-857 ${H857:0:7}; C-170 delta ${HD0:0:7}->${HD1:0:7}; conflicts onto M0 = counts only x3 (legacy merge-tree); M0 counts $M0T/$M0S -> predicted $PRED; lock tool ${INST_NOW:0:12}…; c57 ${C57_NOW:0:12}…; c133 ${C133_NOW:0:12}…; READY copies 4/4 sha256 match; model ${MODEL:-UNSTAMPED}"
if [ "$STAMP_OK" = "0" ] || [ "$ROUTE_OK" = "0" ]; then
  echo "guards pass ($GUARDS); stamp and/or route NOT complete." >&2
  echo "  $SUMMARY" >&2
  [ -z "$PROVISIONAL" ] || echo "  PROVISIONAL (unstamped slots, --check ran against):$PROVISIONAL" >&2
  echo "  NEG seats (38R, derived live; coordinator pane '$COORD_NAME'):$NEG_DESC" >&2
  [ "$STAMP_OK" = "1" ] || echo "REFUSING (32S): $NSLOT at-sign SLOT placeholder(s) remain in the brief (MAIN pin x2 + tree + landed, MODEL, REPORT_DATE x2, RULED: T1-T8, the SELF-CHECK line and the Self-check note), or the SELF-CHECK line is not in the fleet's form — the coordinator re-reads end-to-end and stamps them before launch" >&2
  if [ "$ROUTE_OK" = "0" ]; then
    echo "REFUSING (40): no '${ROUTE_NAME}|tuesday-agent@agentmail.to|no' line in $ROUTING — answers to the gate would have no route; Tuesday adds it at stamp (this launcher never writes it)" >&2; exit 40
  fi
  exit 32
fi

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  origin at $PIN_TS ($LSR_ATTEMPTS ls-remote attempt(s), C-192): main = the stamped pin ${MAIN_SHA:0:12} exactly; the four branches at their pins (18); T9 unmounted (18T)"
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

THE MODEL TUESDAY STAMPED (the --model of this session): $MODEL.
WRITE YOUR ONE REPORT TO: $REPORT
VERIFIED BY THE LAUNCHER AT $PIN_TS (git ls-remote origin, read-only, $LSR_ATTEMPTS attempt(s) under C-192): refs/heads/main = $M_ORIGIN = the stamped MAIN pin (tree $M0_TREE; its ancestry carries 36a0dc0 (tree fb8197a), 5eb80a7 (tree 2d2caa3) and 888203c (tree 428f042); C-170 not on it; what landed since 888203c per the stamp: $S_LANDED); refs/heads/$B476 = $H476; refs/heads/$B856 = $H856; refs/heads/$B857 = $H857; refs/heads/$BD = $HD1. M0's counts are $M0T/$M0S, so the predicted merged counts (arithmetic only; your verifies decide) are $PRED. The legacy stdout-only merge-tree of each of A, B and C onto M0 shows conflict markers in the counts file ONLY. The T9 is unmounted. The installed lock tool $LOCKTOOL sha256 $INST_NOW equals the pin and NEXUSAI_LOCK_BASE=$LOCK_BASE_LAPTOP is exported in your environment. The C-57 runner sha256 $C57_NOW and the C-133 tool sha256 $C133_NOW equal their pins. The four READY copies' sha256 equal the amendment's. These are the start-of-gate pins; take your own three readings anyway.
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
