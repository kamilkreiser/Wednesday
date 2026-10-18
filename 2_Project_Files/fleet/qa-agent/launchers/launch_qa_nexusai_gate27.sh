#!/bin/bash
# launch_qa_nexusai_gate27.sh — cross-project QA agent, ONE gate on Datasec/NexusAI (gate 27): a TIER-1 GATE WITH A BROWSER LEG of RD-778
# (the 8 CodeQL js/xss-through-dom sites fixed in code), re-pinned onto main AFTER gate 25's landings — one gated tree, one verdict, ONE report
# (drafted 2026-10-19 from ~04:53 AEDT by a read-only drafting agent for Tuesday, AMENDMENT 1 of the gate-27 kit; the drafter ran only bash -n
# and the --check refusal path with the kit still slotted).
# A FRESH gate on the Mac mini, /Volumes/Laptop-DEV; the T9 is UNMOUNTED, so the lock base is the Laptop-DEV locks-laptop-1017.
#   RD-778 rd-778-xss-through-dom-s101o @ 3047ae9 (ONE commit on c7ca0ed, draft PR #94) AS MERGED onto main 888203c   -> M778 (REBUILT by the gate)
#   main 888203c = the landing chain 36a0dc0 (tree fb8197a, RD-761) -> 5eb80a7 (tree 2d2caa3, RD-775) -> 888203c (tree 428f042, RD-794 forward-merged)
#   No seat merge commit exists (T0 (a)): the gate rebuilds M778 in its own store and regenerates the counts blob under C-57.
#
# LAUNCHED ONLY VIA: cockpit.sh add 'QA/NexusAI-gate27' "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate27.sh'"
#   (i.e. /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh). A tmux pane, NEVER nohup, never run it bare from a seat's shell.
#
# AUTHORITY: Tuesday's gate-27 drafting commission (2026-10-18), her ANSWER-12 to S101O ("QA tier 1: security, browser-rendered."), ANSWER-16
# (RD-778 re-pins after gate 25's lands), ANSWER-18 (RD-794 land accepted, main 888203c) and ANSWER-19 (C-170's land HELD behind gate 28).
# THE MODEL RULE: Kam, live board 2026-09-30 09:07, card nexusai-gate11-opus55-safeguard-model-switch, option (b), PER SESSION.
# Carried rulings (sqlite3 cached prebuild; full verifies UNBELTED; npm_config_update_notifier=false; ruling (b) + EXTENSION; C-190 + ADDENDUM;
# C-209; C-141 ADDENDA 6/7; the by-hand gate yield RETIRED; the load-8 rule; the Laptop-DEV lock base; gate 21's browser-driver ruling (u)).
# FINDINGS-ONLY: never merges (outside its own store), never pushes, never opens/comments/approves/un-drafts/updates a PR, never dismisses an
# alert, never swaps or edits the lock tool, the C-57 runner or the C-133 tool; no fix, no deploy, no az, no docker, no demo, no human.
#
# PATTERN: launch_qa_nexusai_gate26.sh (prompt EMBEDDED, --check mode, PIN-table parser, pin guards with the C-192 retry, THE MODEL RULE,
# the LIVE negative-control seat derivation 38R, stamp + route guards last) and launch_qa_nexusai_gate25.sh. CHANGES, each deliberate:
#   - 40: ONE head (RD778) and ONE gated row (M778: seat commit none, tree REBUILT, counts blob REGENERATED, 4676/292 = arithmetic).
#   - 18M (new, T0's landing check): origin main != c7ca0ed; main = the MAIN pin; the MAIN pin's tree = 428f042 with parents 2facd7c + 5eb80a7;
#         main's ANCESTRY carries a commit with tree fb8197a; 36a0dc0 / 5eb80a7 trees + parents; is-ancestor chain c7ca0ed->36a0dc0->5eb80a7->888203c;
#         e2bb3ac vs 428f042 = the three paths; C-170 NOT landed. Ancestry, never --first-parent (888203c's first parent is 2facd7c, so a
#         --first-parent walk never reaches 36a0dc0 — kit AMENDMENT 1's topology note).
#   - 22: the 7 gated paths; both-sides = the counts file only; main's 25 changed paths since c7ca0ed; main touches no static/ path.
#   - 93: lock/package/deploy-demo blobs; proxy-addr 2.0.8 + playwright 1.62.1 in the lock; counts; settings.js's two escapeHtml; the payloads.
#   - 96 (new): Chrome + Playwright presence (the browser leg, ruling u); the CDN tags the T5 ruling reads.
#   - 32S (new, LAST): the kit carries 0 at-sign SLOT placeholders (RULED: T0-T9, SELF-CHECK and note) — replaces gate 26's STAMP token.
#   - the READY is read from briefs/ (AMENDMENT 1 copied it; sha256 pinned); its subject says READY FOR QA, not READY FOR GATE.
#   - READY path overridable by QA_READY_OVERRIDE_778 (drafter's --check only; the launch refuses with it set).
#
# Identity: exports NexusAI's OWN az/gh dirs (az is NOT used; gh READ-ONLY); CLAUDE_CONFIG_DIR pinned to Tuesday's store.
# --check is READ-ONLY in NexusAI: git read verbs (cat-file, log, merge-base, diff, show, rev-parse, ls-remote, rev-list, ls-tree); shasum / bash -n /
# grep over session-tools files; python over `git show` output; ls, ps, tmux list-panes, test -e, defaults read. Writes nothing.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate27.sh [--check]
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
BRIEF="$BRIEFS/2026-10-18_nexusai-gate27-rd778-xss.md"
BRIEF21="$BRIEFS/2026-10-12_nexusai-gate-batch21.md"
BRIEF22="$BRIEFS/2026-10-13_nexusai-gate-batch22.md"
BRIEF23="$BRIEFS/2026-10-16_nexusai-gate-batch23.md"
BRIEF24="$BRIEFS/2026-10-17_nexusai-gate24-rd848.md"
BRIEF25="$BRIEFS/2026-10-18_nexusai-gate25-rd761-rd794-merged.md"
BRIEF26="$BRIEFS/2026-10-18_nexusai-gate26-c170-be0fe37-merged.md"
TEMPLATE="$TUE/2_Project_Files/fleet/qa-agent/BRIEF_TEMPLATE.md"
ADD25="$TBRIEFS/2026-10-18_gate25_ADDENDUM-1_ref-order.md"
READY_778="${QA_READY_OVERRIDE_778:-$BRIEFS/2026-10-18_nexusai-rd778-READY-mail.txt}"
READY_SHA='d652bdb96311429f67fde188043fcd5256327f27257209279a937dccb992b201'
ANS1="$TBRIEFS/2026-10-18_S101O_ANSWER-1_plan-confirmation.md"
ANS12="$TBRIEFS/2026-10-18_S101O_ANSWER-12_next-rd778-then-rd771.md"
ANS16="$TBRIEFS/2026-10-18_S101O_ANSWER-16_gate25-landing-stacked.md"
ANS18="$TBRIEFS/2026-10-19_S101O_ANSWER-18_rd794-accepted-c170-turn.md"
ANS19="$TBRIEFS/2026-10-19_S101O_ANSWER-19_c170-codeql-test-fix.md"
CHARTER="$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"
MODELS_JSON="$TUE/0_Brain/dashboard/data/models_latest.json"
MODEL_PIN='claude-opus-5-5'
BELT_ANS="$STAGED/2026-10-05_qa_b14_belt_ANSWER.md"
SQLITE_RULING="$STAGED/2026-10-05_qa_b14_sqlite3_ANSWER.md"
NOTIFIER_ANS="$STAGED/2026-10-05_qa_gate16_notifier_ANSWER.md"
RULING_B="$STAGED/2026-10-06_nexusai_g18_ruling_b_deliver_now.md"
G19_RELEASE="$STAGED/2026-10-12_nexusai_gate19_RELEASE.md"
DRIVER_ANS="$STAGED/2026-10-04_qa_batch13_browser_driver_answer.md"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
NX='/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI'
REPO="$NX/2_Project_Files"
ST="$NX/session-tools"
S101="$ST/s101"
CENSUS="$NX/evidence-s88q-codeql-census/census.csv"
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
B24_DIR="$RPTS/2026-10-17-gate24-rd848"
B24_REPORT="$B24_DIR/report.md"
B24_INST="$B24_DIR/evidence/inst"
B25_DIR="$RPTS/2026-10-18-gate25-rd761-rd794-merged"
B25_REPORT="$B25_DIR/report.md"
B25_INST="$B25_DIR/evidence/inst"
B26_REPORT="$RPTS/2026-10-18-gate26-c170-be0fe37-merged/report.md"
REPORT="$RPTS/2026-10-18-gate27-rd778/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"
ROUTE_NAME='QA/NexusAI-gate27'
NPM_CACHE="${HOME}/.npm/_cacache"
PREBUILD="${HOME}/.npm/_prebuilds/0068db-sqlite3-v5.1.7-napi-v6-darwin-arm64.tar.gz"
PREBUILD_SHA='84a34404b12ff212adbca70eff76c2e4dd83b91245eed0b4569438f928567afc'
CHROME_APP='/Applications/Google Chrome.app'
PW_CACHE="${HOME}/Library/Caches/ms-playwright"

# ---- the pins (cross-checked against the brief's two tables, guard 40; each MEASURED 2026-10-19 04:53-04:56 AEDT, kit AMENDMENT 1)
MAIN_SHA='888203c8c50e13938ca557e8aa0f1faf2101ff31'      # origin main (ls-remote 04:53:50 AEDT; gh 04:53:58 AEDT) = RD-794 forward-merged onto 5eb80a7
MAIN_TREE='428f042b34fb1729d8fd45a112a1220af0fdae6a'
MAIN_P1='2facd7c0645755de400770fe4f2db641f46ba42e'       # first parent: RD-794 stacked on M761 (tree e2bb3ac, gate 25's M794S)
MAIN_P2='5eb80a7a0ee896d8189c85f9103c9f5df01e0112'       # second parent: main before the land
OLD_MAIN='c7ca0ed7113750b268028f12e8659bf1e3d34282'      # main at drafting; RD-778's base; NEVER gated onto under this kit
L761='36a0dc0eb801e5eb52a00be7c0d3de360eb1952d'; T761='fb8197a78a94806a2bc7b7ec00ff6e8758788a12'          # land 1 (RD-761 = gate 25's M761 tree)
L775='5eb80a7a0ee896d8189c85f9103c9f5df01e0112'; T775='2d2caa3f610626ac5f5219aad401590739c2fcfe'          # land 2 (RD-775 counts-only TURN)
P775='537741ce9d1d52f80588ca5a11088182b864960c'
T794S='e2bb3ac1048266dacb13dcc913eebfd76f8bad09'                                                        # gate 25's M794S tree (2facd7c)
H794='cd171f953a4cba86379b2343a5bd31f9cb74f0c1'; H761='7f1881eae1e816381f0f36f1c415bba7589cdb1a'
H460='be0fe3704023d8f092da0be27f79b82fbc029085'                                                         # C-170's head: must NOT be on main
B778='rd-778-xss-through-dom-s101o'
H778='3047ae92b4179adf5ae1bf6e1b60825af2e296e3'
T778H='932a90730f54e5ad2ca1373401ecb100c21948b4'
MB778="$OLD_MAIN"
N778=1
PRED_TESTS=4676; PRED_SUITES=292                                                                        # 4660/291 (888203c's f3f387b) + 16/1 — ARITHMETIC

COUNTS_FILE='scripts/verify-expected-counts.json'
CB_MAIN='f3f387bf989629f938e193927eb6599245471d0a'; CB_BASE='fadda68557bc263a64f88e4bb54f0c1405d931a5'; CB_778='2d803d74a806272a956182e89f870d3c84dce182'
PKG='package.json'; PKG_BLOB='384805d9e286718bb34ffd05be01c62c00806cf5'
LOCK='package-lock.json'; LOCK_BLOB='19477a9329f17e529c208d91d172b95b47fc1bb5'
DEPLOY_WF='.github/workflows/deploy-demo.yml'; DEPLOY_BLOB='953b2a2f84e8710bea857ec87c6f00faa50fa56b'
ARMTTK='.github/workflows/arm-ttk.yml'
RD775_A='backend/services/aiReadiness.js'; RD775_A_BLOB='578e7e7967152efd832e21e70644f15eaec1eb44'
RD775_T='__tests__/rd775-readiness-key-no-hash.test.js'; RD775_T_BLOB='0cca0e04ee6e81ccd237d6907cb56a608d16bfda'
CELLS='__tests__/rd778-dom-text-stays-text.test.js'
GATED_778='__tests__/rd778-dom-text-stays-text.test.js scripts/verify-expected-counts.json static/js/chart-details.js static/js/first-run-setup.js static/js/index-offline.js static/js/index.js static/js/settings.js'
DELTA_794='__tests__/rd775-readiness-key-no-hash.test.js backend/services/aiReadiness.js scripts/verify-expected-counts.json'
NEG_SEATS=''   # 38R: DERIVED at launch from the live cockpit panes — never stamped by hand

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — gate 27'
QUESTION_SUBJ='[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>'
STATUS_SUBJ='[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch'
PARK_LINE='PARKED: flagged — awaiting the Opus 4.8 switch'
ANSWER_PREFIX='[Tuesday -> QA/NexusAI-gate27] ANSWER'
NOTTESTED_LINE="Not tested by this gate: the CodeQL closure of alerts #29 to #36 (a pull request's analysis is diff-scoped and cannot show a pre-existing alert as fixed; Tuesday reads it on main after the land, C-209), the 9th alert #28 in docs/test-files/test-import.html (RD-790, out of scope), the full jest suite on Node 24 (every run used this machine's Node 26.8.1; the pull request Build is that coverage), headed Chrome and every other browser engine (headless Chrome 155 via Playwright 1.62.1 only; the Claude-in-Chrome driver was not used), Windows, a real Log Analytics workspace or Azure OpenAI endpoint (synthetic feed and stubbed responses only), the demo (behind RD-76 SSO) and any deployed revision, a deploy-demo run itself (its skip is read from the workflow condition and the variables), npm audit against the gated tree unless Tuesday ruled it (the lockfile is byte-identical to main's), the server- or AI-supplied fields still written as HTML in the same functions (out of these alerts; a candidate ticket), and the host npm registry (node_modules from an offline cache copy with install scripts skipped and the update notifier off; sqlite3's binding from its cached prebuild)."
SAFE_PRINTER='if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET (length ${#SESSION_SECRET})"; else echo "SESSION_SECRET UNSET"; fi'

g() { git --no-optional-locks -C "$REPO" "$@"; }
counts_blob() { g cat-file -p "$1" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
counts_at() { counts_blob "$(g rev-parse --verify -q "${1}:${COUNTS_FILE}" 2>/dev/null)"; }
blob() { g rev-parse --verify -q "${1}:${2}" 2>/dev/null; }
cntF() { g show "${1}:${2}" 2>/dev/null | grep -cF -- "$3"; }
cntE() { g show "${1}:${2}" 2>/dev/null | grep -cE -- "$3"; }
ntests() { g ls-tree -r -z --name-only "$1" -- __tests__ 2>/dev/null | tr '\0' '\n' | grep -c .; }
fsha() { shasum -a 256 "$1" 2>/dev/null | cut -d' ' -f1; }
lockver() { g cat-file -p "$1" 2>/dev/null | python3 -c 'import json,sys; print(json.load(sys.stdin)["packages"].get("node_modules/"+sys.argv[1],{}).get("version",""))' "$2" 2>/dev/null; }
both_sides() { comm -12 <(g diff --name-only "$1" "$2" 2>/dev/null | sort) <(g diff --name-only "$1" "$3" 2>/dev/null | sort) | tr '\n' ' ' | sed 's/ $//'; }
tree_of() { g rev-parse --verify -q "${1}^{tree}" 2>/dev/null; }
parents_of() { g log -1 --format='%P' "$1" 2>/dev/null; }
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

You are the fleet QA/testing agent running ONE gate on Datasec/NexusAI, gate 27: a TIER-1 GATE WITH A BROWSER LEG of RD-778, with one gated tree, one verdict and ONE report. It is a FRESH gate on Kam's Mac mini, working volume /Volumes/Laptop-DEV; the T9 drive is UNMOUNTED, so the project's jest lock lives on this drive's locks-laptop-1017 base. The head: rd-778-xss-through-dom-s101o at 3047ae92b4179adf5ae1bf6e1b60825af2e296e3, ONE commit on base c7ca0ed7113750b268028f12e8659bf1e3d34282 that fixes the 8 open CodeQL js/xss-through-dom alerts (#29 to #36) in code, at five static dashboard scripts, plus one new jsdom cell file and the counts; draft PR #94 carries it. NOBODY has gated it. Main has moved since the head was cut: main is now 888203c8c50e13938ca557e8aa0f1faf2101ff31 (tree 428f042b34fb1729d8fd45a112a1220af0fdae6a), reached from c7ca0ed by three fast-forward lands — 36a0dc0 (tree fb8197a78a94806a2bc7b7ec00ff6e8758788a12, RD-761, gate 25's M761), then 5eb80a7 (tree 2d2caa3f610626ac5f5219aad401590739c2fcfe, RD-775), then 888203c (RD-794 forward-merged; its tree differs from gate 25's e2bb3ac1048266dacb13dcc913eebfd76f8bad09 exactly in the counts file and RD-775's two files, Tuesday-accepted). C-170 has NOT landed. Under T0 as Tuesday stamped it you gate RD-778 AS IT WOULD LAND on that main: M778 = the head merged onto M0 = 888203c, which you REBUILD yourself in your own store (no seat merge commit exists), with the counts file regenerated under C-57, predicted 4676 tests / 292 suites by arithmetic only (main's 4660/291 plus the head's 16 cells in 1 suite) — your own full verify decides. Never trust the seat's trees, logs, cells or render script as the proof. FINDINGS-ONLY: you NEVER merge anything the fleet can see, NEVER push, NEVER open, comment on, approve, un-draft or merge a pull request, never dismiss an alert, and NEVER swap, copy over or edit the installed lock tool, the C-57 runner or the C-133 tool; no fixes, no deploys, no az, no docker, no production, no HTTP to any production or demo host, nothing to Partner Center, the demo or any human, no host npm registry. One client only: Datasec/NexusAI.

READ YOUR COMMISSION FIRST, whole: /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-18_nexusai-gate27-rd778-xss.md
It opens with AMENDMENT 1 (the real landing chain and its TOPOLOGY NOTE — 888203c's FIRST parent is 2facd7c, gate 25's stacked commit, so a first-parent walk never reaches 36a0dc0: the chain is checked by ancestry, never by a first-parent walk), the PIN-HEADS and MERGE-PINS tables, the TIER argument and the drafter's WRONG OR UNVERIFIED list (each item MEASURED or READ-ONLY-INFERRED), then TUESDAY'S RULINGS (T0 to T9 as Tuesday stamped them, the commission's properties, the carried rulings) and THE MODEL RULE: apply them, do not re-rule them. Then the charter it names; the READY mail it names (briefs/2026-10-18_nexusai-rd778-READY-mail.txt), read WHOLE; Tuesday's ANSWER-12 to the builder (the acceptance words), ANSWER-16, ANSWER-18 and ANSWER-19 (the landing sequence and why C-170 is held); the clarifications it names at source (C-190 with its ADDENDUM, C-209, C-02, C-57, C-133 and C-40 first); gate 21's browser-driver ruling and its H-32 rule; gate 25's ADDENDUM-1 (the ref order); gates 22, 23, 24, 25 and 26's section 3a (the H-rules, carried by reference); and gate 24's and gate 25's reports on THIS drive (the structural template and the instrument sources). Gate 21's own browser instruments are on the unmounted T9: NOT READ, named; re-derive the driver from the ruling's words. Every builder statement is a CLAIM — RELAYED, never evidence. The brief's section 2a rows (r0, r1, r2, r3, b1, b2, r5, r5b, r6, r7, r8, r10), section 2b (the browser leg) and section 2c (the 8 sites + the errorCode) are required measurement.

THE MODEL RULE (Kam, live board 2026-09-30 09:07, card (b)): QA gates may switch to Opus 4.8 when flagged by Opus 5.5's safeguards, PER SESSION. You start on Opus 5.5. You run the FULL rows. If one of your responses is stopped by the safeguards: that step is NOT RUN (never re-worded to slip past); write ONE line to evidence/classifier-stops.txt; let any running step finish and let the hold exit so you never sit holding a lock (H-28); mail tuesday-agent@agentmail.to with the subject exactly "[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch"; then end your turn with the line "PARKED: flagged — awaiting the Opus 4.8 switch" and wait. Tuesday switches THIS pane's model and taps you by mail. You never answer the model dialog yourself, and nobody ever chooses "Switch automatically". After the switch, resume at the stopped row. The report states which rows ran on which model, with the switch time, and quotes classifier-stops.txt whole. The browser-inert row composes markup payloads against a server you booted: use ONLY the builder's two payloads from the cell file (the image-error marker and the script marker, whose only effect is setting window.__rd778), never a new payload class.

THE PROPERTIES (brief sections 2a to 2c). (1) THE TREE ROW r1: in your own --mirror store (T6: create your g27 refs FIRST, then remove origin, then prove each — gate 25 ADDENDUM-1), git merge-tree --write-tree of M0 and the head must conflict in scripts/verify-expected-counts.json ONLY (the drafter's legacy read against 888203c: one changed-in-both, the counts file; one added-in-remote, the cell file; the five static scripts one-sided); with your own regenerated counts blob substituted the tree differs from the mechanical merge in the counts path only; your own full verify passing on it is the counts file's assertion; positive control first (your method reproduces gate 25's e2bb3ac from cd171f9 + 36a0dc0 with the seat's counts blob) and a negative control (another counts blob gives another id). (2) THE SITE ROW r2: each of #29 to #36 plus the server errorCode read against its alert — source, sink, the fix, the CONTEXT the value lands in, the helper that binds there IN THE BROWSER (settings.js declares escapeHtml twice: resolve which one binds by a scope parse), and whether the escape is sufficient there; the reader must see every sink unescaped at c7ca0ed first. (3) THE RED-PROOF ROW r3: the 16 cells red-first on c7ca0ed (10 FAIL, 6 pass), green on the head and on the gated tree; then each fix reverted ALONE on the gated tree, its named cells RED and every control GREEN, restored to 16/16; a revert no cell kills is a cell that does not guard its site (C-40, Major); the older rd395 UI suites that load the offline chat script are checked for silent disarmament (C-102). (4) THE BROWSER-INERT ROW b1 and (5) THE BROWSER-RENDER ROW b2: BASE (M0) and BRANCH (M778) servers booted from separate clones, local, open mode (C-02), loopback, belted, inside a jest-lock hold, with the H-36 socket ledger; Playwright 1.62.1 from the tree's own node_modules launching the locally installed Google Chrome headless (channel 'chrome'), no download; every payload INERT on the branch and LIVE on the base (a base arm that does not fire is VOID, never a pass); ordinary values render identically base vs branch by DOM text, element screenshots and layout boxes, the comparator proven first (base vs base reads 0; a planted one-character or one-pixel difference is found); DOM-planted arms per T2 captioned "DOM-PLANTED at the alert's source (CodeQL's model), not a product data path", stubbed responses per T3 captioned "STUBBED RESPONSE", CDN assets per T5. Never a jsdom render reported as a browser. (6) THE SUITE ROW r5/r5b: the full verify on the gated tree, names as SETS vs M0 (LOST 0, NEW = exactly the 16 rd778 ids); C-57 through a byte-identical COPY of the installed runner with C57_ROOT pointing at your own shim (T1), C-133 through a copy of the installed tool. (7) THE ALERT ROW r6: CodeQL on the PR #94 head read with gh READ ONLY and C-209's limit — the PR-head zero is "0 NEW" (C-190), never "fixed"; #28 (RD-790, out of scope) absent from the PR ref is the proof; PR #58's head is the positive control that a PR analysis can report. (8) THE AUDIT, DEPLOY + BUILD and SECRETS rows r7, r8, r10: main's lockfile 19477a9 and package.json 384805d, proxy-addr 2.0.8 and playwright 1.62.1 from the lock and from each installed tree's own path; deploy-demo's paths-ignore does not cover static/js or __tests__, so the land STARTS it and only the two if: conditions on vars.CI_DEPLOY_ENABLED keep it from deploying; PR #94's Build (Node 24) read; gitleaks 8.30.1 over the gated range, your merge and an archive extraction of the gated tree, after a planted throwaway string is found first; never print a value. Plus r0 scope and pins.

MAIN MUST NOT MOVE (ruling b): the launcher verified origin main = 888203c exactly and its landing chain; take M0 by git ls-remote at YOUR start and say so. If main moves mid-gate (C-170's held land is the likeliest mover), the gated tree is stale: name what landed, finish nothing that would read as a verdict on the new main, and mail a QUESTION (C-68). GitHub SSH intermittently denies auth (C-192): retry every ls-remote up to 5 times about 10 s apart; a FAILED ls-remote is UNKNOWN, never a value. Re-hash the lock tool, the C-57 runner and the C-133 tool at start, mid and end.

C-190 + its ADDENDUM — BOTH thresholds block: every merge to main goes through a pull request that adds no new high-or-higher CodeQL alert in changed code (test code included), AND any new alert whose RULE severity is error blocks whatever its security severity. Alerts are fixed in code, never dismissed. C-209: a PR's CodeQL run cannot show a pre-existing main alert as fixed; closure of #29 to #36 is read on main's push analysis after the land, by number. CodeQL is NOT RUN by this gate on any tree — say so. C-185 (ruling h): read its known set at source; any other failure is by NAME; no re-run is a clearance.

THE LOCK (C-63). The installed tool is session-tools/nexusai-lock.sh in the NexusAI project on this drive, sha256 3c33f5ae58e1be20282467a90b27a23a2de998eedd0e56c03f3c06360031a792. While the T9 is unmounted the base is NEXUSAI_LOCK_BASE=/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/session-tools/locks-laptop-1017, which the launcher has EXPORTED into your environment: keep it on every jest step and every server boot, quote the c57 runner's resolved LOCK_BASE= and ROOT= line, and never touch this drive's stale session-tools/locks (a 2026-09-22 holder lives there). If the T9 mounts mid-gate, finish the running hold, file nothing more, and mail a QUESTION. EVERY jest run and every booted server goes in the jest lock, each hold tagged qa-g27- (no tag of yours contains the word "merge": C-141 ADDENDUM 7), ONE hold at a time. MERGES GO FIRST and RULING (i)'s BY-HAND GATE YIELD IS RETIRED: if a ticket is queued ahead of you, wait behind it (FIFO) — the builder S101O and any peer QA gate file jest holds on the same base. AT A WAIT DEADLINE: --replace on your own still-waiting ticket BEFORE its deadline fires (C-141: a SAME-PLACE handover), confirmed from the queue listing (the old ticket to released/ as ticket-left-*, your place unchanged); a duplicate-tag refusal takes a -r<N> suffix. Read queue-jest at start, around every hold and at end; any qa-g27- entry that is not your current hold is a STOP. Read your inbox before filing every new hold. THE LOAD RULE: file a hold, start any full jest or any browser arm only below a 1-minute load of 8 (8 cores; Tuesday's ANSWER-1 to S101O); record uptime beside each.

NODE_MODULES WITHOUT THE HOST REGISTRY (ruling m, H-31): offline npm ci --offline --ignore-scripts --no-audit --no-fund with --cache pointing at an APFS clone of the local npm cache on the same volume; the base, branch and every other tree share lock 19477a9, so ONE proven install is APFS-cloned into the others; EVERY npm invocation carries npm_config_update_notifier=false (prove the cache copy's _update-notifier-last-checked marker absent or unchanged); an ENOTCACHED is NOT RUN, named, with a QUESTION — never go online from the host, never npm install, never npx playwright install (--ignore-scripts means Playwright downloads NO browser; Chrome is the local install). sqlite3's binding from the cached prebuild (an APFS clone of ~/.npm/_prebuilds), inside the strict belt, IS PART OF H-31, with its three conditions (the tarball's and the unpacked node_sqlite3.node's sha256; CI builds its own Linux binding; every row that boots a server names "sqlite3 binding: cached prebuild, offline"). proxy-addr must resolve 2.0.8 from each tree's own path (RD-827, C-205).

FULL VERIFIES (r5) through the jest lock, UNBELTED by Tuesday's 2026-10-05 answer to gate 14 (ruling n), with its four conditions. SESSION_SECRET UNSET, npm_config_update_notifier=false npm run verify -- --maxWorkers=2 --forceExit (prove the flag reached jest), Node v26.8.1 as T7 rules. RULING (b) and its EXTENSION (ruling o): if a verify stays lock-starved about 2 h after filing, deliver it NAMED NOT RUN — never "skipped" — with the brief's coverage sentence in NOT TESTED. The SITE, RED-PROOF, BROWSER-INERT and BROWSER-RENDER rows are NOT covered by that extension: they run, and a TIER-1 verdict whose site, red-proof or browser rows did not run is PROVISIONAL and releases nothing. A revert, plant or stub counts only if it LANDED (the exact text present, the original absent) and parses; a red from a revert that never landed is a VOID arm, a planted control that does not fire makes its row VOID (never a pass), and an edit whose anchor is absent fails loudly and nothing downstream runs on that tree.

THE INSTRUMENT RULES H-1 TO H-36 (brief section 3a; gates 22, 23, 24, 25 and 26's section 3a read WHOLE, and gate 21's H-32). H-1: the ONLY SESSION_SECRET printer is the one the brief quotes; self-test it and gate 24's scan. H-3: a LANDING CONTROL for every plant, revert, stub and DOM placement. H-4: the HEARTBEAT is a separate child of the hold wrapper, aborted if absent 90 s after the grant, max gap reported. H-6: every path with a space quoted; every host jest run but the full verify, every driver and every booted server under your copy of the belt with its landing control. H-9: byte plants by Buffer, checked with xxd. H-11/H-18: /bin/bash explicitly, "${sha}:${path}" quoted (zsh eats :s and :a). H-14: every driver ends END ok or END VOID with a reason. H-17: censuses by pgrep, never ps. H-20: a per-step hard DEADLINE on every jest run (with --forceExit), every runner invocation, every npm ci, every server boot and every browser arm (qa-to.sh). H-21: every file you mutate is restored by a trap on EXIT (also INT and TERM) installed BEFORE the first mutation. H-22: never nest sandbox-exec (it exits 71); if Chrome must run outside the belt, say so and rely on the page route allow-list and the host-resolver rules. H-24: jest array options after the paths, lists built in bash. H-26: C-192 retries. H-27: THE MODEL RULE. H-28: ONE focused hold at a time, at most about 40 minutes planned (T1's runner hold excepted), rows GROUPED, a hold that would overrun SPLIT, every part file bash -n checked before filing; you stay in the FOREGROUND — a hold that must outlive one tool call runs as a TRACKED child of your session (never nohup) with its timeout at the 2-hour maximum; each hold carries a wait deadline and you --replace before it fires. H-29: other gates' and the builder's evidence is method only. H-31: offline host node_modules. H-32: the browser opens ONLY loopback pages of a server YOU booted from YOUR tree (plus the pinned CDN URLs if T5 rules so); no HTTP to any production or demo host. H-33: never rm — quarantine (T1's disclosed runner exception only); every child (servers, Chrome and its helpers) reaped by pid. H-34: the Laptop-DEV lock base. H-35: NO docker object and NO az command, not even az version. H-36: THE SOCKET LEDGER on every booted server, its landing control first.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT (fresh mktemp dirs under projects/nexusai/qa-trees/gate27.* in /Volumes/Laptop-DEV/!CODING/Testing Agent MAIN): ONE --mirror clone of the NexusAI repo on THIS drive as your store (T6), your refs g27/* in it made BEFORE origin is removed, your merge commit in it, every work tree a clone of that store, status-checked before use, EXCLUSIVE to one purpose (BASE and BRANCH server clones separate so data dirs and node_modules never cross). NEVER work in the NexusAI root checkout or any worktrees/ folder (LIVE, the builder's: worktrees/s101o-rd778 included). In the NexusAI repo use ONLY read verbs (show, diff, log with an explicit rev, ls-tree, cat-file, grep, ls-remote, rev-parse, merge-base, rev-list, count-objects, for-each-ref); NEVER fetch, pull, push, checkout, worktree, commit, stash, gc, merge, merge-tree --write-tree or hash-object -w there. Copy instruments BY NAME from gate 24's and gate 25's evidence/inst on THIS drive (never the whole directory), re-point every gate-24/25 path in your copies to gate 27 — INCLUDING the lock base line (quote that diff) — and correct the floor library's ROOT and NEG defaults from the live list below; never write into another gate's dirs (gates 25 and 26 are COMPLETE and read-only to you). Never write into the builders' session-tools (S101O is live in s101/: hash its rd778 files at start and end); never run the seat's scripts in place (the render-identity script is METHOD only). Findings-only: never push, no commits outside your store, no tickets, no PRs, no edits in NexusAI. No Microsoft, Log Analytics or login host, no demo, no Partner Center, no workflow dispatch, no repo variable written, no CDN beyond T5's pinned URLs from Chrome only. No mail to any human. Never rm: quarantine.

FLOOR DISCIPLINE — section 9 of the brief exactly. Do ALL lock-free work first (pins, hashes, reads, r0, r1's rebuild and its controls, r2, r6 to r8, r10, the offline npm ci, the belt and ledger self-tests); then file your holds one at a time through your COPY of gate 24's qa-file24.sh re-pointed to qa-g27 tags and the jest kind. QUEUE, NEVER TAKE OVER: never signal, move or edit another seat's or gate's process, lock, ticket or worktree. Count foreign servers the C-125 way anchored on YOUR OWN claude pid, with the negative-control seats the launcher derived (listed at the end of this prompt) classifying foreign in the same run; re-derive them at every hold's start; a hold with no live negative control aborts; record the foreign server count beside every browser result. A zero is reportable only beside a control that fired in the same window. DEADLINE AND HEARTBEAT: every step has a per-step DEADLINE, every child is killed in a finally by pid from your own ancestry (C-174, never by pattern), a HEARTBEAT line at least every 2 minutes during a hold, and a step with no heartbeat for 5 minutes is aborted and reported; every booted server and Chrome stopped by its own pid and its port read free afterwards.

RE-PIN at start, mid and end: main and the branch rd-778-xss-through-dom-s101o, refs/pull/94/head, plus the three tools' sha256 — three timestamped readings with the branch name and attempt count beside each sha. A head that disagrees with the brief is a FINDING and a reason to stop, never a typo to fix. Call main at your start M0 and say so. Count the NexusAI .git/objects files and their newest mtime at start and end and account for any delta (the amendment drafter read 35 files at 04:54 AEDT on 2026-10-19).

QUESTIONS: your routing name is QA/NexusAI-gate27. If you must ask, mail tuesday-agent@agentmail.to with subject "[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>" and PROCEED ON THE SAFEST READING without waiting (the one exception is a safeguards stop, which PARKS you under THE MODEL RULE); Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/NexusAI-gate27] ANSWER". Approval-class items (anything Azure, the demo, Partner Center, money, a human, the live lock tool, any host beyond section 10 of the brief) are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your ONE report to: /Volumes/Laptop-DEV/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-10-18-gate27-rd778/report.md
Write its VERDICT and FINDINGS table early and keep it current. Findings are G27-<n>, notes N27-<n>, each naming its instrument and evidence class.

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with the subject exactly:
[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — gate 27
Lead the body with the TWO lines in the form the brief's section 11 gives — RD-778 (with its RE-PIN, TREE, SITES, RED-PROOF, BROWSER-INERT, BROWSER-RENDER, VERIFY, C-57, CODEQL, AUDIT, DEPLOY-DEMO, PR BUILD and GITLEAKS clauses) and LANDING CHECKLIST — then one line naming M0 and END main, the C-102 sweep, which rows ran on Opus 4.8 (or none), which holds ran and which are NAMED NOT RUN under ruling (o) extended, and "CodeQL NOT RUN by this gate on any tree". The report's last two lines are those same two lines. Never wednesday-agent@. You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/Laptop-DEV/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no 4_Credentials directory of its own. Never put the key, a token, a session value or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice — the only turn you end while waiting is the PARKED line of THE MODEL RULE.

Rule 2 stands: what you did NOT test is first-class output — a NOT TESTED section carrying the builder's stated limits, every declared limit L-B1 to L-B8 and L-Y1 discharged with a measurement or left standing and named (C-112), Prior work checked (C-49), every finding naming its instrument, and every action recommendation labelled MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. The tester never fixes. C-190 with its ADDENDUM, C-209, C-02, C-57, C-133, C-185 with its ADDENDA, C-192, C-205, C-141 with ADDENDA 6 and 7, C-63, C-40, C-68, C-76, C-102, C-112 and C-174 are the clarifications this gate leans on; C-20, C-34, C-49, C-89, C-115, C-125, C-130, C-131 and C-203 are carried. That section must carry this line verbatim:
Not tested by this gate: the CodeQL closure of alerts #29 to #36 (a pull request's analysis is diff-scoped and cannot show a pre-existing alert as fixed; Tuesday reads it on main after the land, C-209), the 9th alert #28 in docs/test-files/test-import.html (RD-790, out of scope), the full jest suite on Node 24 (every run used this machine's Node 26.8.1; the pull request Build is that coverage), headed Chrome and every other browser engine (headless Chrome 155 via Playwright 1.62.1 only; the Claude-in-Chrome driver was not used), Windows, a real Log Analytics workspace or Azure OpenAI endpoint (synthetic feed and stubbed responses only), the demo (behind RD-76 SSO) and any deployed revision, a deploy-demo run itself (its skip is read from the workflow condition and the variables), npm audit against the gated tree unless Tuesday ruled it (the lockfile is byte-identical to main's), the server- or AI-supplied fields still written as HTML in the same functions (out of these alerts; a candidate ticket), and the host npm registry (node_modules from an offline cache copy with install scripts skipped and the update notifier off; sqlite3's binding from its cached prebuild).
PROMPT_EOF

# ---------------------------------------------------------------- GUARDS
[ -d "$QA_DIR" ]  || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]   || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -n "$PROMPT" ]  || { echo "embedded prompt is empty" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }

# MODEL — read from Tuesday's models_latest.json (opus level), never typed from memory; REFUSE unless it is the brief's pin.
MODEL="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["levels"]["opus"]["model_id"])' "$MODELS_JSON" 2>/dev/null)"
[ "$MODEL" = "$MODEL_PIN" ] || { echo "REFUSING: $MODELS_JSON levels.opus.model_id is '${MODEL:-unreadable}', not $MODEL_PIN as the brief states — re-brief" >&2; exit 9; }

# 40 — parse BOTH pin tables from the brief (the ONLY source of heads and trees) and cross-check them against this launcher's pins.
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
PIN="$(parse_block PIN-HEADS)"; MPIN="$(parse_block MERGE-PINS)"
[ "$PIN" != "NO-BLOCK" ] && [ -n "$PIN" ] || { echo "REFUSING: the brief has no PIN-HEADS block — the heads have nowhere to come from" >&2; exit 40; }
[ "$MPIN" != "NO-BLOCK" ] && [ -n "$MPIN" ] || { echo "REFUSING: the brief has no MERGE-PINS block — the gated tree has nowhere to come from" >&2; exit 40; }
prow() { printf '%s\n' "$1" | awk -F'\t' -v id="$2" '$1==id'; }
pfld() { prow "$1" "$2" | awk -F'\t' -v n="$3" '{print $n}'; }
is40()  { printf '%s' "$1" | grep -Eq '^[0-9a-f]{40}$'; }
[ "$(printf '%s\n' "$PIN" | wc -l | tr -d ' ')" = "2" ] || { echo "REFUSING: PIN-HEADS must carry exactly two rows (MAIN RD778)" >&2; exit 40; }
[ "$(printf '%s\n' "$MPIN" | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: MERGE-PINS must carry exactly one row (M778)" >&2; exit 40; }
for ID in MAIN RD778; do
  R="$(prow "$PIN" "$ID")"
  [ "$(printf '%s\n' "$R" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: PIN-HEADS must carry exactly one row '$ID'" >&2; exit 40; }
  [ "$(printf '%s\n' "$R" | awk -F'\t' '{print NF}')" = "7" ] || { echo "REFUSING: PIN-HEADS row $ID does not have 7 cells: $R" >&2; exit 40; }
  printf '%s' "$R" | grep -q '@' && { echo "REFUSING: PIN-HEADS row $ID still carries a placeholder" >&2; exit 40; }
  [ "$(pfld "$PIN" "$ID" 7)" = "IN" ] || { echo "REFUSING: PIN-HEADS row $ID status is not IN" >&2; exit 40; }
  [ "$(pfld "$PIN" "$ID" 2)" = "nexusai" ] || { echo "REFUSING: PIN-HEADS row $ID repo must be nexusai" >&2; exit 40; }
  is40 "$(pfld "$PIN" "$ID" 4)" || { echo "REFUSING: PIN-HEADS row $ID head is not a 40-hex sha" >&2; exit 40; }
done
[ "$(pfld "$PIN" MAIN 3)" = "main" ] && [ "$(pfld "$PIN" MAIN 4)" = "$MAIN_SHA" ] || { echo "REFUSING: PIN-HEADS MAIN is not main @ 888203c — this launcher's guards are pinned to it; re-pin the kit AND this launcher" >&2; exit 40; }
[ "$(pfld "$PIN" RD778 3)" = "$B778" ] && [ "$(pfld "$PIN" RD778 4)" = "$H778" ] && [ "$(pfld "$PIN" RD778 5)" = "$MB778" ] && [ "$(pfld "$PIN" RD778 6)" = "$N778" ] \
  || { echo "REFUSING: PIN-HEADS RD778 is not $B778 @ 3047ae9, base c7ca0ed, $N778 commit (T0 (b) re-pins kit AND launcher)" >&2; exit 40; }
R="$(prow "$MPIN" M778)"
[ "$(printf '%s\n' "$R" | awk -F'\t' '{print NF}')" = "8" ] || { echo "REFUSING: MERGE-PINS row M778 does not have 8 cells: $R" >&2; exit 40; }
printf '%s' "$R" | grep -q '@' && { echo "REFUSING: MERGE-PINS row M778 still carries a placeholder" >&2; exit 40; }
[ "$R" = "$(printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' M778 "$H778" "$MAIN_SHA" none REBUILT REGENERATED "$PRED_TESTS" "$PRED_SUITES")" ] \
  || { echo "REFUSING: MERGE-PINS row M778 is not as this launcher pins it (T0 (a): none / REBUILT / REGENERATED / $PRED_TESTS / $PRED_SUITES): '$R'" >&2; exit 40; }

# 6 — every sha the guards use is a commit in the local object store (this launcher never fetches).
for S in "$MAIN_SHA" "$MAIN_P1" "$MAIN_P2" "$L761" "$L775" "$P775" "$OLD_MAIN" "$H778" "$H794" "$H761"; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 7 / 8 — the head's chain: merge base c7ca0ed, ONE linear commit, head not on main, its tree.
[ "$(g merge-base "$H778" "$MAIN_SHA" 2>/dev/null)" = "$MB778" ] || { echo "REFUSING: merge-base(3047ae9, 888203c) is not c7ca0ed" >&2; exit 7; }
if g merge-base --is-ancestor "$H778" "$MAIN_SHA" 2>/dev/null; then echo "REFUSING: 3047ae9 is ALREADY on main 888203c — re-brief" >&2; exit 7; fi
[ "$(g rev-list --count "${MB778}..${H778}" 2>/dev/null)" = "$N778" ] && [ -z "$(g rev-list --merges "${MB778}..${H778}" 2>/dev/null)" ] \
  || { echo "REFUSING: RD-778 is not ONE linear commit over c7ca0ed" >&2; exit 8; }
[ "$(tree_of "$H778")" = "$T778H" ] || { echo "REFUSING: 3047ae9's tree is not 932a907 (§A of the brief)" >&2; exit 8; }
[ "$(g rev-list --count "${H778}..${MAIN_SHA}" 2>/dev/null)" = "31" ] || echo "NOTE: main is $(g rev-list --count "${H778}..${MAIN_SHA}" 2>/dev/null) commits past 3047ae9, not 31 as measured at amendment" >&2

# 18M — T0's LANDING CHECK (kit AMENDMENT 1, WRONG 1): main != c7ca0ed; the MAIN pin's tree + parents; main's ANCESTRY carries tree fb8197a;
# the chain c7ca0ed -> 36a0dc0 -> 5eb80a7 -> 888203c by is-ancestor; each land's tree; e2bb3ac vs 428f042 = the three paths; C-170 NOT landed.
# Ancestry, never --first-parent: 888203c's FIRST parent is 2facd7c, so a --first-parent walk never reaches 36a0dc0 (it would refuse forever).
[ "$MAIN_SHA" != "$OLD_MAIN" ] || { echo "REFUSING: the MAIN pin is c7ca0ed — never gate onto c7ca0ed under this kit (T0 (c))" >&2; exit 18; }
[ "$(tree_of "$MAIN_SHA")" = "$MAIN_TREE" ] || { echo "REFUSING: 888203c's tree is '$(tree_of "$MAIN_SHA")', not 428f042 (T0)" >&2; exit 18; }
[ "$(parents_of "$MAIN_SHA")" = "$MAIN_P1 $MAIN_P2" ] || { echo "REFUSING: 888203c's parents are not 2facd7c + 5eb80a7 (AMENDMENT 1's topology)" >&2; exit 18; }
[ "$(tree_of "$MAIN_P1")" = "$T794S" ] && [ "$(parents_of "$MAIN_P1")" = "$H794 $L761" ] || { echo "REFUSING: 2facd7c is not tree e2bb3ac with parents cd171f9 + 36a0dc0 (gate 25's M794S)" >&2; exit 18; }
[ "$(tree_of "$L775")" = "$T775" ] && [ "$(parents_of "$L775")" = "$P775 $L761" ] || { echo "REFUSING: 5eb80a7 is not tree 2d2caa3 with parents 537741c + 36a0dc0 (RD-775's land)" >&2; exit 18; }
[ "$(tree_of "$L761")" = "$T761" ] && [ "$(parents_of "$L761")" = "$H761 $OLD_MAIN" ] || { echo "REFUSING: 36a0dc0 is not tree fb8197a with parents 7f1881e + c7ca0ed (RD-761's land = gate 25's M761)" >&2; exit 18; }
FB_IN="$(g log --format='%H %T' "$MAIN_SHA" 2>/dev/null | awk -v t="$T761" '$2==t{print $1}' | tr '\n' ' ' | sed 's/ $//')"
[ "$FB_IN" = "$L761" ] || { echo "REFUSING: main's ancestry carries tree fb8197a at '${FB_IN:-no commit}', not exactly 36a0dc0 (T0's landing check)" >&2; exit 18; }
g merge-base --is-ancestor "$OLD_MAIN" "$L761" 2>/dev/null && g merge-base --is-ancestor "$L761" "$L775" 2>/dev/null && g merge-base --is-ancestor "$L775" "$MAIN_SHA" 2>/dev/null \
  || { echo "REFUSING: the landing chain c7ca0ed -> 36a0dc0 -> 5eb80a7 -> 888203c is not an ancestry chain" >&2; exit 18; }
FP_FB="$(g log --first-parent --format='%T' "$MAIN_SHA" 2>/dev/null | grep -cxF "$T761")"
[ "$FP_FB" = "0" ] || echo "NOTE: a --first-parent walk from 888203c NOW reaches tree fb8197a ($FP_FB) — AMENDMENT 1 measured 0; the ancestry check above still decides" >&2
[ "$(g diff --name-only "$T794S" "$MAIN_TREE" 2>/dev/null | sort | tr '\n' ' ' | sed 's/ $//')" = "$(printf '%s\n' $DELTA_794 | sort | tr '\n' ' ' | sed 's/ $//')" ] \
  || { echo "REFUSING: 428f042 does not differ from gate 25's e2bb3ac in exactly counts + RD-775's two files (ANSWER-18's acceptance premise)" >&2; exit 18; }
[ "$(blob "$MAIN_SHA" "$RD775_A")" = "$RD775_A_BLOB" ] && [ "$(blob "$L775" "$RD775_A")" = "$RD775_A_BLOB" ] && [ "$(blob "$MAIN_SHA" "$RD775_T")" = "$RD775_T_BLOB" ] && [ "$(blob "$L775" "$RD775_T")" = "$RD775_T_BLOB" ] \
  || { echo "REFUSING: RD-775's two files at 888203c are not byte-identical to 5eb80a7's (578e7e7 / 0cca0e0)" >&2; exit 18; }
if [ "$(g cat-file -t "$H460" 2>/dev/null)" = "commit" ] && g merge-base --is-ancestor "$H460" "$MAIN_SHA" 2>/dev/null; then
  echo "REFUSING: C-170's head be0fe37 is on main 888203c — ANSWER-19 holds that land; the kit's M0 premise is wrong; re-brief" >&2; exit 18; fi
[ -z "$(blob "$MAIN_SHA" "$ARMTTK")" ] || { echo "REFUSING: arm-ttk.yml is present at 888203c — a C-170 land; re-brief" >&2; exit 18; }

# 18T — the T9 MOUNTED refuses: two lock bases would split the FIFO (ruling q); Tuesday decides the base first.
[ ! -d "$T9_VOL" ] || { echo "REFUSING: $T9_VOL is MOUNTED — the brief's lock base (locks-laptop-1017) assumes it is not; Tuesday decides the base, then re-brief" >&2; exit 18; }

# 18 — RE-PIN NOW by ls-remote (C-192 retries): main EXACTLY the MAIN pin; the branch exactly its pin; PR #94's head (NOTE).
lsr refs/heads/main "refs/heads/$B778" refs/pull/94/head || { echo "REFUSING: git ls-remote origin failed after $LSR_ATTEMPTS attempt(s) — UNKNOWN, not a value (C-192); relaunch later" >&2; exit 18; }
LSR_ALL="$LSR_OUT"
ref_now() { printf '%s\n' "$LSR_ALL" | awk -v r="$1" '$2==r{print $1}'; }
M_ORIGIN="$(ref_now refs/heads/main)"
[ "$M_ORIGIN" != "$OLD_MAIN" ] || { echo "REFUSING: origin main is still c7ca0ed — gate 25's lands have not moved main (T0 (c)); never gate onto c7ca0ed" >&2; exit 18; }
[ "$M_ORIGIN" = "$MAIN_SHA" ] || { echo "REFUSING: origin main is '${M_ORIGIN:-unreadable}', not 888203c — main MOVED (C-170's held land?); re-pin the kit AND this launcher" >&2; exit 18; }
[ "$(ref_now "refs/heads/$B778")" = "$H778" ] || { echo "REFUSING: origin $B778 is '$(ref_now "refs/heads/$B778")', not 3047ae9 — moved (T0 (b)?); re-pin" >&2; exit 18; }
P94="$(ref_now refs/pull/94/head)"
[ "$P94" = "$H778" ] || echo "NOTE: refs/pull/94/head is '${P94:-absent}', not 3047ae9 — PR #94 moved; the gate reads it (§8, r6)" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 90 — the INSTALLED lock tool PINNED; it honours NEXUSAI_LOCK_BASE; the Laptop-DEV base is present with queue-jest; no qa-g27 ticket.
INST_NOW="$(fsha "$LOCKTOOL")"
[ "$INST_NOW" = "$LOCK_SHA_INST" ] || { echo "REFUSING: the INSTALLED lock tool's sha256 is '${INST_NOW:-absent}', not 3c33f5ae… — find out who changed it; re-brief" >&2; exit 90; }
grep -qF 'BASE="${NEXUSAI_LOCK_BASE:-' "$LOCKTOOL" || { echo "REFUSING: the installed tool no longer honours NEXUSAI_LOCK_BASE — ruling q's premise" >&2; exit 90; }
bash -n "$LOCKTOOL" 2>/dev/null || { echo "REFUSING: $LOCKTOOL does not parse (bash -n)" >&2; exit 90; }
grep -qF -- '--replace' "$LOCKTOOL" && grep -qF 'jest|docker) ;;' "$LOCKTOOL" || { echo "REFUSING: $LOCKTOOL lacks --replace or the jest kind" >&2; exit 90; }
[ -d "$LOCK_BASE_LAPTOP" ] && [ -d "$LOCKQ_J" ] || { echo "REFUSING: the Laptop-DEV lock base $LOCK_BASE_LAPTOP (queue-jest) is not present (ruling q)" >&2; exit 90; }
BQ="$(grep -l '^tag=qa-g27' "$LOCKQ_J"/* 2>/dev/null | wc -l | tr -d ' ')"
[ "${BQ:-0}" = "0" ] || { echo "REFUSING: $BQ qa-g27* ticket(s) already in $LOCKQ_J — a live or stale gate-27 ticket; read before launch" >&2; exit 90; }
MQ="$(grep -lE '^tag=.*(^|[-_=])merge([0-9]+[a-z]?)?([-_]|$)' "$LOCKQ_J"/* 2>/dev/null | wc -l | tr -d ' ')"
[ "${MQ:-0}" = "0" ] || echo "NOTE: $MQ merge-tagged ticket(s) in $LOCKQ_J now — the gate files behind them (brief §9)" >&2
GQ="$(grep -lE '^tag=qa-g(2[0-68-9]|[3-9][0-9])' "$LOCKQ_J"/* 2>/dev/null | wc -l | tr -d ' ')"
[ "${GQ:-0}" = "0" ] || echo "NOTE: $GQ other-gate qa- ticket(s) queued — FIFO; gate 27 waits behind them, never touches them" >&2
HOLDER="$(sed -n 's/^tag=//p' "$LOCK_BASE_LAPTOP/nexusai-jest.lock/owner" 2>/dev/null | head -1)"
case "$HOLDER" in
  qa-g27*) echo "REFUSING: the Laptop-DEV jest lock is HELD by '$HOLDER' — a gate-27 holder already exists" >&2; exit 90 ;;
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
  && grep -qF 'rm -rf "$wt"' "$C57TOOL" && grep -qF 'worktree remove --force "$wt"' "$C57TOOL" && grep -qF 'OUT="$ROOT/session-tools/c57-$TAG"' "$C57TOOL" \
  || { echo "REFUSING: the C-57 runner's C57_ROOT / LOCK_BASE / rm / worktree / OUT lines are not as T1 describes" >&2; exit 91; }
grep -qF 'usage: c133-accounting.py <c57-out-dir> <base> <A=main> <B=branch> <merged-tree-or-commit> <repo-dir>' "$C133TOOL" || { echo "REFUSING: c133-accounting.py's usage line moved" >&2; exit 91; }

# 22 — the gated file set, the both-sides set (WRONG 2, against the MAIN pin), main's count, and main touches no static/ path.
[ "$(g diff --name-only "$MB778" "$H778" 2>/dev/null | sort | tr '\n' ' ' | sed 's/ $//')" = "$(printf '%s\n' $GATED_778 | sort | tr '\n' ' ' | sed 's/ $//')" ] \
  || { echo "REFUSING: RD-778's gated files (c7ca0ed..3047ae9) are not the briefed 7" >&2; exit 22; }
[ "$(both_sides "$MB778" "$H778" "$MAIN_SHA")" = "$COUNTS_FILE" ] || { echo "REFUSING: the both-sides set vs 888203c is not the counts file alone (got '$(both_sides "$MB778" "$H778" "$MAIN_SHA")') (WRONG 2)" >&2; exit 22; }
[ "$(g diff --name-only "$MB778" "$MAIN_SHA" 2>/dev/null | grep -c .)" = "25" ] || { echo "REFUSING: main's changed-file count since c7ca0ed is not 25 (WRONG 2)" >&2; exit 22; }
[ "$(g diff --name-only "$MB778" "$MAIN_SHA" -- static 2>/dev/null | grep -c .)" = "0" ] || { echo "REFUSING: main changed a static/ path since c7ca0ed — the browser BASE is no longer c7ca0ed's pages (WRONG 2)" >&2; exit 22; }

# 93 — the premises at source (WRONG 3, 6, 8, 9, 12; r7, r8): blobs, lock versions, deploy-demo, counts, census, helpers, payloads.
for S in "$OLD_MAIN" "$H778" "$MAIN_SHA"; do
  [ "$(blob "$S" "$LOCK")" = "$LOCK_BLOB" ] && [ "$(blob "$S" "$PKG")" = "$PKG_BLOB" ] && [ "$(blob "$S" "$DEPLOY_WF")" = "$DEPLOY_BLOB" ] \
    || { echo "REFUSING: ${S:0:7} does not carry lockfile 19477a9 / package.json 384805d / deploy-demo.yml 953b2a2 (r7, r8)" >&2; exit 93; }
done
[ "$(lockver "$LOCK_BLOB" proxy-addr)" = "2.0.8" ] && [ "$(lockver "$LOCK_BLOB" playwright)" = "1.62.1" ] && [ "$(lockver "$LOCK_BLOB" playwright-core)" = "1.62.1" ] && [ "$(lockver "$LOCK_BLOB" jsdom)" = "20.0.3" ] \
  || { echo "REFUSING: lock 19477a9 does not resolve proxy-addr 2.0.8, playwright 1.62.1, playwright-core 1.62.1, jsdom 20.0.3 (WRONG 12)" >&2; exit 93; }
[ "$(cntF "$MAIN_SHA" "$DEPLOY_WF" "vars.CI_DEPLOY_ENABLED == 'true'")" = "2" ] && [ "$(cntF "$MAIN_SHA" "$DEPLOY_WF" 'branches: [main]')" = "1" ] && [ "$(cntF "$MAIN_SHA" "$DEPLOY_WF" 'paths-ignore:')" = "1" ] \
  || { echo "REFUSING: deploy-demo.yml no longer gates BOTH jobs on vars.CI_DEPLOY_ENABLED == 'true' on push to main with one paths-ignore (r8)" >&2; exit 93; }
[ "$(counts_at "$OLD_MAIN")" = "4559 287" ] && [ "$(counts_at "$H778")" = "4575 288" ] && [ "$(counts_at "$MAIN_SHA")" = "4660 291" ] \
  || { echo "REFUSING: counts are not 4559/287 (c7ca0ed), 4575/288 (3047ae9), 4660/291 (888203c) (WRONG 3)" >&2; exit 93; }
[ "$(blob "$MAIN_SHA" "$COUNTS_FILE")" = "$CB_MAIN" ] && [ "$(blob "$OLD_MAIN" "$COUNTS_FILE")" = "$CB_BASE" ] && [ "$(blob "$H778" "$COUNTS_FILE")" = "$CB_778" ] \
  || { echo "REFUSING: counts blobs are not fadda68 (c7ca0ed) / 2d803d7 (3047ae9) / f3f387b (888203c) (WRONG 2)" >&2; exit 93; }
[ "$PRED_TESTS $PRED_SUITES" = "$(( $(counts_at "$MAIN_SHA" | cut -d' ' -f1) + 16 )) $(( $(counts_at "$MAIN_SHA" | cut -d' ' -f2) + 1 ))" ] \
  || { echo "REFUSING: the M778 prediction is not main's counts + 16 tests / 1 suite (WRONG 3 arithmetic)" >&2; exit 93; }
[ "$(ntests "$OLD_MAIN")" = "341" ] && [ "$(ntests "$H778")" = "342" ] && [ "$(ntests "$MAIN_SHA")" = "347" ] || { echo "REFUSING: the __tests__ census is not 341 / 342 / 347" >&2; exit 93; }
[ "$(cntE "$H778" static/js/settings.js 'function escapeHtml[[:space:]]*\(')" = "2" ] || { echo "REFUSING: settings.js at 3047ae9 does not declare escapeHtml exactly twice (WRONG 6)" >&2; exit 93; }
for f in chart-details first-run-setup index; do
  [ "$(cntE "$H778" "static/js/$f.js" 'function escapeHtml[[:space:]]*\(')" = "1" ] || { echo "REFUSING: $f.js at 3047ae9 does not declare escapeHtml exactly once (WRONG 6)" >&2; exit 93; }
done
[ "$(cntF "$H778" static/js/index.js 'const _originalButtonHtml = new WeakMap();')" = "1" ] || { echo "REFUSING: index.js at 3047ae9 lacks the LoadingManager WeakMap (WRONG 8)" >&2; exit 93; }
[ "$(cntF "$H778" "$CELLS" "const PAYLOAD = '<img src=\"x\" onerror=\"window.__rd778=1\">';")" = "1" ] && [ "$(cntF "$H778" "$CELLS" "const SCRIPT_PAYLOAD = '<script>window.__rd778=1</script>';")" = "1" ] \
  || { echo "REFUSING: the cell file no longer carries the builder's two payloads (THE MODEL RULE's 'use exactly those')" >&2; exit 93; }
[ "$(cntF "$H778" static/index.html 'cdn.jsdelivr.net/npm/bootstrap@5.3.0/')" -ge 1 ] && [ "$(cntF "$H778" static/index-offline.html 'cdn.jsdelivr.net')" = "0" ] \
  || { echo "REFUSING: index.html no longer loads bootstrap@5.3.0 from cdn.jsdelivr.net, or index-offline.html now loads it (WRONG 9, T5)" >&2; exit 93; }

# 96 — the browser leg's local premises (ruling u): Chrome installed, Playwright in the lock (above); NOTEs record versions and the cache.
[ -d "$CHROME_APP" ] || { echo "REFUSING: $CHROME_APP is absent — b1/b2 cannot run (ruling u: the locally installed Google Chrome)" >&2; exit 96; }
CHV="$(defaults read "$CHROME_APP/Contents/Info" CFBundleShortVersionString 2>/dev/null)"
case "$CHV" in 155.*) ;; *) echo "NOTE: Google Chrome is '${CHV:-unreadable}', not 155.x as briefed — every caption names what the gate finds" >&2 ;; esac
[ -d "$PW_CACHE" ] && echo "NOTE: $PW_CACHE exists ($(ls -1 "$PW_CACHE" 2>/dev/null | grep -c .) entr(y/ies)) — read its path + mtime before and after (ruling u)" >&2

# 70 — the carried rulings and Tuesday's answers (REFUSALs where a ruling is missing).
[ -s "$SQLITE_RULING" ] && grep -qF 'The offline unpack of sqlite3' "$SQLITE_RULING" || { echo "REFUSING: Tuesday's sqlite3 prebuild ruling (ruling m) is not at $SQLITE_RULING" >&2; exit 70; }
[ -s "$BELT_ANS" ] && grep -qF 'run UNBELTED. Every other jest run stays belted: cells, mutants, C-68 unions, drivers and servers.' "$BELT_ANS" \
  || { echo "REFUSING: Tuesday's belt answer (ruling n) is not at $BELT_ANS as quoted" >&2; exit 70; }
[ -s "$NOTIFIER_ANS" ] && grep -qF 'Every later npm invocation in this gate carries npm_config_update_notifier=false' "$NOTIFIER_ANS" \
  || { echo "REFUSING: Tuesday's notifier answer (ruling m) is not at $NOTIFIER_ANS as quoted" >&2; exit 70; }
[ -s "$RULING_B" ] && grep -qF 'Deliver the verdict NOW.' "$RULING_B" || { echo "REFUSING: Tuesday's ruling (b) is not at $RULING_B as quoted" >&2; exit 70; }
grep -qF 'NOT RUN, named, under ruling (o) EXTENDED' "$BRIEF24" && grep -qF 'NOT RUN, named, under ruling (o) EXTENDED' "$BRIEF25" && grep -qF 'NOT RUN, named, under ruling (o) EXTENDED' "$BRIEF" \
  || { echo "REFUSING: ruling (o)'s EXTENSION words are not carried in gates 24/25's briefs and this brief" >&2; exit 70; }
[ -s "$G19_RELEASE" ] && grep -qF 'the by-hand gate yield (ruling (i)) is RETIRED from gate 21 on.' "$G19_RELEASE" \
  || { echo "REFUSING: gate 19's RELEASE no longer carries the yield retirement" >&2; exit 70; }
[ -s "$ANS1" ] && grep -qF 'load1 below 8 before every heavy run' "$ANS1" && grep -qF 'lock base locks-laptop-1017' "$ANS1" \
  || { echo "REFUSING: Tuesday's ANSWER-1 (load 8, lock base) is not at $ANS1 as quoted" >&2; exit 70; }
[ -s "$ANS12" ] && grep -qF 'QA tier 1: security, browser-rendered.' "$ANS12" && grep -qF 'Fix in code, never by dismissal' "$ANS12" \
  && grep -qF 'Rendered text and layout stay IDENTICAL. No customer-facing word changes. If a site needs any visible change, STOP and ask.' "$ANS12" \
  && grep -qF 'Do not fix it inside RD-778.' "$ANS12" && grep -qF 'Stack it on rd-778 because the files are shared.' "$ANS12" \
  || { echo "REFUSING: Tuesday's ANSWER-12 (the acceptance words) is not at $ANS12 as quoted" >&2; exit 70; }
[ -s "$ANS16" ] && grep -qF 'Unchanged: RD-778 waits for gate 27' "$ANS16" && grep -qF 'You land YOUR commits; the tree equality is the check.' "$ANS16" \
  || { echo "REFUSING: Tuesday's ANSWER-16 is not at $ANS16 as quoted" >&2; exit 70; }
[ -s "$ANS18" ] && grep -qF 'RD-794 land ACCEPTED, no delta gate.' "$ANS18" && grep -qF "main = $MAIN_SHA" "$ANS18" \
  && grep -qF 'compare 2facd7c...888203c = exactly counts + aiReadiness.js + rd775 test' "$ANS18" && grep -qF 'After C-170: Tuesday stamps and launches gate 27 (RD-778)' "$ANS18" \
  || { echo "REFUSING: Tuesday's ANSWER-18 (RD-794 accepted, main 888203c) is not at $ANS18 as quoted" >&2; exit 70; }
[ -s "$ANS19" ] && grep -qF 'Then HOLD the land' "$ANS19" && grep -qF 'SUPERSEDES ANSWER-18 item 3' "$ANS19" \
  || { echo "REFUSING: Tuesday's ANSWER-19 (C-170's land held behind gate 28) is not at $ANS19 as quoted" >&2; exit 70; }
[ -s "$DRIVER_ANS" ] && grep -qF "Playwright 1.62.1 from YOUR tree's own node_modules, launching the locally installed Google Chrome" "$DRIVER_ANS" \
  && grep -qF "headless (channel 'chrome'), no download, under your network belt, every non-127.0.0.1 request aborted." "$DRIVER_ANS" \
  || { echo "REFUSING: gate 21's browser-driver ruling (u) is not at $DRIVER_ANS as quoted" >&2; exit 70; }
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
[ "$NODEV" = "v26.8.1" ] || echo "NOTE: host node is '${NODEV:-absent}', not v26.8.1 as briefed (T7) — the gate records it" >&2
GLV="$(gitleaks version 2>/dev/null)"
[ "$GLV" = "8.30.1" ] || echo "NOTE: gitleaks is '${GLV:-absent}', not 8.30.1 — r10 records it (CI pins 8.30.1)" >&2
LOAD1="$(sysctl -n vm.loadavg 2>/dev/null | awk '{print $2}')"
awk -v l="${LOAD1:-99}" 'BEGIN{exit !(l < 8)}' || echo "NOTE: 1-minute load is ${LOAD1:-unknown} (not below 8) — the gate waits in the queue, never in a hold (ruling p)" >&2

# 31 — the READY, builder evidence, gate 24's and gate 25's instruments (THIS drive), standing references.
for f in "$READY_778" "$CLAR" "$BRIEF21" "$BRIEF22" "$BRIEF23" "$BRIEF24" "$BRIEF25" "$BRIEF26" "$TEMPLATE" "$B24_REPORT" "$B25_REPORT" "$B26_REPORT" "$CHARTER" "$CENSUS" \
         "$S101/rd778-cells-base.json" "$S101/rd778-cells-base.out" "$S101/rd778-cells-new.json" "$S101/rd778-cells-new.out" "$S101/rd778-render-identity.js" "$S101/rd778-render-identity.out" \
         "$S101/verify-rd778.log" "$S101/own-install-rd778.out" "$S101/pr-rd778-body.md" "$S101/mail-20-ready-rd778.txt" \
         "$B24_INST/qa-file24.sh" "$B24_INST/qa-file24r.sh" "$B24_INST/qa-floorlib24.sh" "$B24_INST/qa-floorcount.py" "$B24_INST/qa-hm24.sh" "$B24_INST/qa-h1-selftest24.sh" \
         "$B24_INST/qa-to.sh" "$B24_INST/qa-h1-scan.py" "$B24_INST/qa-mail24.py" "$B24_INST/qa-mailread24.py" \
         "$B25_INST/qa-netbelt.sb" "$B25_INST/qa-netbelt-nodns.sb" "$B25_INST/qa-netbelt-ctl.js" "$B25_INST/qa-ledger25.js" "$B25_INST/qa-floorlib25.sh" "$B25_INST/qa-probe25.js"; do
  [ -s "$f" ] || { echo "REFUSING: evidence, brief or tool absent: $f" >&2; exit 31; }
done
[ -n "${QA_READY_OVERRIDE_778:-}" ] || [ "$(fsha "$READY_778")" = "$READY_SHA" ] || { echo "REFUSING: the READY in briefs/ is not the drafter's saved body (sha256 d652bdb9…b201) — re-read it from the inbox" >&2; exit 31; }
grep -qF "$H778" "$READY_778" && grep -qF 'READY FOR QA' "$READY_778" && grep -qF 'PRIOR WORK' "$READY_778" && grep -qF 'NOT TESTED' "$READY_778" && grep -qF 'verify: PASS 4575/4575 across 288 suites.' "$READY_778" \
  || { echo "REFUSING: the READY does not name 3047ae9, READY FOR QA, PRIOR WORK, NOT TESTED and its verify line" >&2; exit 31; }
grep -qF 'STATUS: COMPLETE' "$B24_REPORT" && grep -qF 'STATUS: COMPLETE' "$B25_REPORT" && grep -qF 'STATUS: COMPLETE' "$B26_REPORT" \
  || { echo "REFUSING: gate 24's / 25's / 26's report does not read as delivered (the instrument sources must be DELIVERED gates)" >&2; exit 31; }
[ ! -e "$B24_INST/.throwaway-ss" ] || echo "NOTE: gate 24's inst/ holds a .throwaway-ss — copy instruments BY NAME, never the directory" >&2
for B in "$BRIEF21" "$BRIEF22" "$BRIEF23" "$BRIEF24" "$BRIEF25" "$BRIEF26"; do grep -qF '## 3a. INSTRUMENT RULES' "$B" || { echo "REFUSING: $B has no section 3a — the H-rules carried by reference are missing" >&2; exit 31; }; done
grep -qF 'docs/test-files/test-import.html:41,RD-790' "$CENSUS" || { echo "REFUSING: the S88Q census no longer maps #28 to RD-790 (PRIOR WORK provenance)" >&2; exit 31; }

# 39 — the floor and server instruments are named in the brief.
grep -qF 'qa-floorlib24.sh' "$BRIEF" && grep -qF 'qa-file24.sh' "$BRIEF" && grep -qF 'qa-ledger25.js' "$BRIEF" && grep -qF 'qa-netbelt.sb' "$BRIEF" \
  || { echo "REFUSING: brief does not name the floor / filer / ledger / belt instruments" >&2; exit 39; }

# 10 / 17 — report path named in both; no stale report; brief names every source it cites.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }
for P in "2026-10-18_nexusai-rd778-READY-mail.txt" "2026-10-18_S101O_ANSWER-12_next-rd778-then-rd771.md" "2026-10-18_S101O_ANSWER-16_gate25-landing-stacked.md" \
         "2026-10-19_S101O_ANSWER-18_rd794-accepted-c170-turn.md" "2026-10-13_nexusai-gate-batch22.md" "2026-10-16_nexusai-gate-batch23.md" "2026-10-17_nexusai-gate24-rd848.md" \
         "2026-10-18_nexusai-gate25-rd761-rd794-merged.md" "2026-10-18_nexusai-gate26-c170-be0fe37-merged.md" "2026-10-12_nexusai-gate-batch21.md" \
         "2026-10-04_qa_batch13_browser_driver_answer.md" "2026-10-05_qa_b14_belt_ANSWER.md" "2026-10-06_nexusai_g18_ruling_b_deliver_now.md" "qa-file24.sh" "qa-file24r.sh" \
         "models_latest.json" "QA_AGENT_CHARTER.md" "locks-laptop-1017" "ADDENDUM-1" "census.csv" "rd778-render-identity.js" ".pre-amend"; do
  grep -qF "$P" "$BRIEF" || { echo "REFUSING: brief must name $P" >&2; exit 10; }
done

# 11 — identity: NexusAI's OWN dirs.
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"
[ -d "$CLAUDE_CONFIG_DIR" ] || { echo "REFUSING: Tuesday's claude store $CLAUDE_CONFIG_DIR is absent" >&2; exit 11; }

# 12 / 13 / 14 / 15 / 20 — tier, directive, brief path, pins, verdict route, key path, question route.
for T in 'THIS IS A TIER-1 GATE' 'BROWSER LEG' 'NO GO' 'NO HOST NPM REGISTRY' 'FULL VERIFIES UNBELTED' 'EXTENSION' \
         'npm_config_update_notifier=false' 'BOTH thresholds block' 'RULING (b)' 'NAMED NOT RUN' '--replace' 'qa-g27-' 'RETIRED' 'H-34' 'H-35' 'H-36' 'C-63' 'C-209' \
         'THE TREE ROW' 'THE SITE ROW' 'THE RED-PROOF ROW' 'THE BROWSER-INERT ROW' 'THE BROWSER-RENDER ROW' 'THE SUITE ROW' 'THE ALERT ROW' 'THE AUDIT ROW' 'THE DEPLOY + BUILD ROW' 'THE SECRETS ROW' \
         'M778' 'DOM-PLANTED' 'STUBBED RESPONSE' 'VOID' 'can fail' 'positive control' 'negative control' 'G27-<n>' 'NOT TESTED' 'PRIOR WORK' 'No HTTP to any production or demo host' \
         'AMENDMENT 1' 'TOPOLOGY NOTE' 'never `--first-parent`'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not declare '$T'" >&2; exit 12; }
done
for T in 'TIER-1 GATE WITH A BROWSER LEG' 'THE PROPERTIES' 'THE TREE ROW' 'THE SITE ROW' 'THE RED-PROOF ROW' 'THE BROWSER-INERT ROW' 'THE BROWSER-RENDER ROW' 'THE SUITE ROW' \
         'THE ALERT ROW' 'THE AUDIT, DEPLOY + BUILD and SECRETS rows' 'M778' 'REBUILD' 'AMENDMENT 1' 'ancestry' 'DOM-PLANTED' 'STUBBED RESPONSE' 'as SETS' 'C-209' '0 NEW' \
         'UNBELTED' 'npm_config_update_notifier=false' 'BOTH thresholds block' 'RULING (b)' 'EXTENSION' 'NAMED NOT RUN' '--replace' 'qa-g27-' 'RETIRED' 'locks-laptop-1017' \
         'jest lock' 'T0' 'T1' 'T2' 'T3' 'T5' 'T6' 'T7' "Never trust the seat's trees" 'no HTTP to any production or demo host' 'One client only' 'NO docker object and NO az' \
         "channel 'chrome'" 'Playwright 1.62.1' 'Never a jsdom render reported as a browser'; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare '$T'" >&2; exit 12 ;; esac
done
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
for S in "$H778" "$MAIN_SHA" "$OLD_MAIN" "$LOCK_SHA_INST" "$MAIN_TREE" "$T761" "$T775" "$T794S"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S in full" >&2; exit 14; }
  case "$PROMPT" in *"$S"*) ;; *) echo "REFUSING: prompt must name $S" >&2; exit 14 ;; esac
done
for S in "$L761" "$L775" "$CB_MAIN" "$C57_SHA" "$C133_SHA" "$PKG_BLOB" "$LOCK_BLOB" "$DEPLOY_BLOB" "$PREBUILD_SHA" "$READY_SHA" "$T778H"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S in full" >&2; exit 14; }
done
if printf '%s\n' "$PROMPT" | LC_ALL=C grep -q '@[A-Z_0-9-]*@'; then echo "REFUSING: the prompt carries a placeholder" >&2; exit 14; fi
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
if grep -qF 'KK_T9_External_HDD/TUESDAY' "$BRIEF"; then echo "REFUSING: the brief names the T9 TUESDAY tree" >&2; exit 15; fi
[ "$(grep -oE 'qa-g27-[A-Za-z0-9_<>-]*merge[A-Za-z0-9_-]*' "$BRIEF" | grep -c .)" = "0" ] || { echo "REFUSING: the brief suggests a qa-g27- tag containing 'merge' (C-141 ADDENDUM 7)" >&2; exit 15; }
[ "$(printf '%s\n' "$PROMPT" | grep -oE 'qa-g27-[A-Za-z0-9_<>-]*merge' | grep -c .)" = "0" ] || { echo "REFUSING: the prompt suggests a qa-g27- tag containing 'merge'" >&2; exit 15; }

# 41 — RULING (i)'s by-hand yield is RETIRED.
for T in 'stop YOUR OWN unstarted waiter' 'stop your OWN unstarted waiter' 'then re-queue with --after that merge' 'self-apply ONE yield per gate TAG'; do
  if grep -qF -- "$T" "$BRIEF" || printf '%s\n' "$PROMPT" | grep -qF -- "$T"; then echo "REFUSING: '$T' instructs the RETIRED by-hand yield" >&2; exit 41; fi
done
grep -qF 'THE BY-HAND GATE YIELD IS RETIRED' "$BRIEF" || { echo "REFUSING: the brief does not carry the retirement of ruling (i)'s yield" >&2; exit 41; }
case "$PROMPT" in *"BY-HAND GATE YIELD IS RETIRED"*) ;; *) echo "REFUSING: the prompt does not say the by-hand gate yield is RETIRED" >&2; exit 41 ;; esac

# 82 — THE MODEL RULE is carried in the brief and the prompt, per session, never "Switch automatically".
for T in "$STATUS_SUBJ" "$PARK_LINE" 'classifier-stops.txt' 'Switch automatically' 'Opus 4.8' 'PER SESSION' 'which rows ran on which model' 'Opus 5.5'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks THE MODEL RULE fragment '$T'" >&2; exit 82; }
  case "$(printf '%s' "$PROMPT" | tr '[:upper:]' '[:lower:]')" in *"$(printf '%s' "$T" | tr '[:upper:]' '[:lower:]')"*) ;; *) echo "REFUSING: prompt lacks THE MODEL RULE fragment '$T'" >&2; exit 82 ;; esac
done
grep -qF '## THE MODEL RULE' "$BRIEF" && grep -qF 'H-27' "$BRIEF" && grep -qF 'H-28 (AMENDED' "$BRIEF" && grep -qF 'H-32 (RE-BASED' "$BRIEF" && grep -qF 'H-34 (THE LOCK BASE' "$BRIEF" \
  && grep -qF 'H-35 (NO DOCKER, NO AZ' "$BRIEF" && grep -qF 'H-36 (THE SOCKET LEDGER' "$BRIEF" \
  || { echo "REFUSING: brief lacks THE MODEL RULE section or H-27/H-28 (amended)/H-32 (re-based)/H-34/H-35/H-36" >&2; exit 82; }

# 19 — the words the prompt must carry (% is a space); the brief's sections; limits; rows; READY lines verbatim; clarification quotes.
WORDS="RD-778 RD-761 RD-775 RD-794 RD-790 C-170 C-190 C-209 C-02 C-57 C-133 C-185 C-192 C-205 C-141 C-63 C-40 C-68 C-76 C-102 C-112 C-174 C-20 C-34 C-49 C-89 C-115 C-125 C-130 C-131 C-203 ADDENDA%6%and%7
r0 r1 r2 r3 b1 b2 r5 r5b r6 r7 r8 r10 T0 T1 T2 T3 T5 T6 T7 M0 888203c c7ca0ed 36a0dc0 5eb80a7 2facd7c 19477a9 384805d 2.0.8 proxy-addr playwright vars.CI_DEPLOY_ENABLED #29 #36 #28 PR%#94 PR%#58 4676 292
L-B1 L-B8 L-Y1 H-1 H-3 H-4 H-6 H-9 H-14 H-17 H-20 H-21 H-22 H-24 H-26 H-27 H-28 H-29 H-31 H-32 H-33 H-34 H-35 H-36 --forceExit trap%on%EXIT DEADLINE LANDING%CONTROL
_prebuilds node_sqlite3.node sqlite3%binding:%cached%prebuild,%offline _update-notifier-last-checked exits%71 --mirror EXCLUSIVE STOP VOID C57_ROOT gitleaks%8.30.1
MERGES%GO%FIRST QUEUE,%NEVER%TAKE%OVER SAME-PLACE%handover HEARTBEAT 2%minutes 5%minutes finally SESSION_SECRET%UNSET NOT%TESTED MEASURED%AT%RUNTIME READ%ONLY PROBED
RELAYED CodeQL%is%NOT%RUN UNKNOWN about%40%minutes 2-hour%maximum TRACKED%child Prior%work FOREGROUND never%push NEVER%merge Partner%Center npm%install --offline ENOTCACHED
qa-file24.sh ticket-left-* -r<N> instrument never%fixes GROUPED SPLIT never%dismissed PROVISIONAL qa-g27 G27-<n> N27-<n> 1-minute%load%of%8 S101O window.__rd778 scope%parse
escapeHtml socket%ledger loopback open%mode headless Google%Chrome first-parent"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## TIER' '^## 2a-T. LEGITIMATE SHAPES' '^## WRONG OR UNVERIFIED' "^## TUESDAY'S RULINGS" '^## THE MODEL RULE' '^## Charter' '^## THE CLARIFICATIONS THAT BIND THIS GATE' '^## PRIOR WORK (C-49) and PRIOR ROUND' \
         '^## 1. Target' '^### How to build your trees' '^## 2. Tier and severity' '^## 2a. ROWS' '^## 2b. THE BROWSER LEG' '^## 2c. THE 8 SITES' '^## 3. THE QUESTIONS' '^## 3a. INSTRUMENT RULES' \
         '^## 3b. THE NEGATIVE-ASSERTION SWEEP' '^## 7. THE GATED TREE' '^## 8. CI, ALERTS, AUDIT, DEPLOY-DEMO' '^## 9. Floor discipline' '^## 10. HELD' '^## 11. Output' '^## PROVENANCE' '^## FILL AT STAMP'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
grep -qF '**ROUND 1 — no prior gate of RD-778.**' "$BRIEF" || { echo "REFUSING: the brief's PRIOR WORK block does not declare round 1" >&2; exit 19; }
[ "$(grep -n '^## WRONG OR UNVERIFIED' "$BRIEF" | cut -d: -f1)" -lt "$(grep -n "^## TUESDAY'S RULINGS" "$BRIEF" | cut -d: -f1)" ] || { echo "REFUSING: the WRONG OR UNVERIFIED section is not above TUESDAY'S RULINGS" >&2; exit 19; }
WSTART="$(grep -n '^## WRONG OR UNVERIFIED' "$BRIEF" | cut -d: -f1)"; WEND="$(grep -n "^## TUESDAY'S RULINGS" "$BRIEF" | cut -d: -f1)"
WUNMARKED="$(sed -n "${WSTART},${WEND}p" "$BRIEF" | grep -E '^[0-9]+\. ' | grep -vE 'MEASURED|READ-ONLY-INFERRED|own actions' | cut -c1-60)"
[ -z "$WUNMARKED" ] || { echo "REFUSING: WRONG items not marked MEASURED / READ-ONLY-INFERRED: $WUNMARKED" >&2; exit 19; }
for L in L-B1 L-B2 L-B3 L-B4 L-B5 L-B6 L-B7 L-B8 L-Y1; do grep -qF "$L" "$BRIEF" || { echo "REFUSING: brief lacks declared limit $L (C-112)" >&2; exit 19; }; done
for R in r0 r1 r2 r3 b1 b2 r5 r5b r6 r7 r8 r10; do grep -qF "| $R |" "$BRIEF" || { echo "REFUSING: brief lacks row $R" >&2; exit 19; }; done
for n in 0 1 2 3 4 5 6 7 8 9; do
  grep -qE "^- \*\*\(T${n}\) [^*]*:\*\* RULED: " "$BRIEF" || { echo "REFUSING: brief lacks the ruling slot (T$n) as '**(T$n) …:** RULED: …'" >&2; exit 19; }
done
# the READY's lines the brief quotes, verbatim in both.
while IFS= read -r T; do
  [ -n "$T" ] || continue
  grep -qF -- "$T" "$READY_778" || { echo "REFUSING: '$T' is no longer in the READY — the source changed; re-brief" >&2; exit 19; }
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not carry the READY line '$T' verbatim" >&2; exit 19; }
done <<'VERBATIM_EOF'
A real browser render. Your gate's browser leg compares renders; mine is jsdom.
two rd395 tests stub LoadingManager whole
The existing escapeHtml helpers in index.js:109 and settings.js:89 are older work and reused. The cell method (lifting shipped functions) is the rd395 UI cells'.
settings.js showValidationModal: validationResult.suggestion (:1709), .message (:1716, with \n -> <br>) and .suggestions (:1723);
VERBATIM_EOF
# the rulings the brief rests on are quoted from source and still say so
while IFS= read -r Q; do
  [ -n "$Q" ] || continue
  grep -qF -- "$Q" "$CLAR" || { echo "REFUSING: CLARIFICATIONS no longer carries '$Q' — the brief's quotes are stale; re-brief" >&2; exit 19; }
  grep -qF -- "$Q" "$BRIEF" || { echo "REFUSING: brief does not quote '$Q'" >&2; exit 19; }
done <<'CLAR_EOF'
A local run serves every page and API with no sign-in.
Every merge to NexusAI main goes through a PULL REQUEST, and a PR must add NO NEW high-or-higher CodeQL alert in the code it changes. Test code is included.
`alerts_threshold = errors`, so ANY new alert whose RULE severity is `error` blocks, whatever its security severity.
A PR's CodeQL run CANNOT show a PRE-EXISTING main alert as fixed
the PR analysis is diff-scoped, so such an alert has no instance on refs/pull/N/head in any state.
Its closure is read AFTER the merge, on main's push analysis, by alert number
A merge conflict confined to `scripts/verify-expected-counts.json` is resolved by regeneration, with an id-superset control.
Any other conflicting file still stops.
No re-run is used as a clearance
a FAILED ls-remote is UNKNOWN, never a value.
A merge hold runs on a node_modules that matches the merged tree's package-lock.json.
TAG CONVENTION — only a merge HOLD's tag contains the word `merge`.
Gate (`qa-*`) tickets are never moved; the holder is never touched.
The jest and docker lock (`session-tools/nexusai-lock.sh`) is first-in-first-out, and it takes over an ownerless lock after 30 s.
A check must be able to fail on the thing it claims to be about.
a clean merge-tree and a changed measured surface are not in tension
An explanation of why a fix works is a CLAIM: it gets a red proof, or it is marked UNVERIFIED in the artefact that carries it.
A declared limit is where the evidence stops — not a place it is cleared.
NEVER KILL BY PATTERN.
CLAR_EOF

# 24 — the prompt must DESCRIBE the server entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qi 'backend/server\.js'; then
  echo "REFUSING: the prompt contains the server entry point's literal path (RD-591 c.37901). Describe it; do not name it." >&2; exit 24; fi

# 53 / 71 — standing rules in the brief; the NOT TESTED line verbatim in both.
for w in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' 'qa-g27-' 'VOID' 'EXCLUSIVE' 'POSITIVE CONTROL FIRST' 'QUEUE, NEVER TAKE OVER' 'LANDING CONTROL' \
         'If main MOVES mid-gate' '--replace' 'never push' 'C-174' '--forceExit' 'trap … EXIT' 'MERGES GO FIRST' 'queue-jest/' 'carry on' 'never idles holding a lock' \
         'ONE focused hold at a time' 'FOREGROUND' 'Never two live holds' 'Every finding names its instrument' \
         'NOT TESTED' 'The tester never fixes' 'SPLIT a hold' 'ONE CLIENT ONLY' 'no CodeQL alert dismissed' 'below a 1-minute load of **8**'; do
  grep -qiF -- "$w" "$BRIEF" || { echo "REFUSING: brief lacks the standing rule '$w'" >&2; exit 53; }
done
grep -qF "$NOTTESTED_LINE" "$BRIEF" || { echo "REFUSING: brief must carry the NOT TESTED line verbatim" >&2; exit 71; }
case "$PROMPT" in *"$NOTTESTED_LINE"*) ;; *) echo "REFUSING: prompt must carry the NOT TESTED line verbatim" >&2; exit 71 ;; esac
grep -qF 'The report'"'"'s LAST two lines are the two verdict lines' "$BRIEF" || { echo "REFUSING: brief must fix the report's last lines as the verdict lines" >&2; exit 71; }

# 76 / 77 / 78 / 79 — H-1's printer and forbidden idioms; H-4; H-9; H-7/H-8.
grep -qF "$SAFE_PRINTER" "$BRIEF" || { echo "REFUSING: brief must carry the safe SESSION_SECRET printer verbatim (H-1)" >&2; exit 76; }
for w in '${SESSION_SECRET-…}' '${SESSION_SECRET:-…}' '${SESSION_SECRET+$SESSION_SECRET}' 'printenv' '${envs[*]}'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief must name the forbidden idiom $w (H-1)" >&2; exit 76; }
done
for w in 'separate child' 'within 90 s' 'max gap'; do grep -qiF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the heartbeat fragment '$w' (H-4)" >&2; exit 77; }; done
for w in 'H-9' 'Buffer' 'xxd -l 16'; do grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the byte-plant fragment '$w' (H-9)" >&2; exit 78; }; done
for w in 'H-7/H-8' 'negative control' 'the exact reverted text present AND the fixed text absent' 'FAILS LOUDLY'; do grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the revert-landing fragment '$w' (H-7/H-8)" >&2; exit 79; }; done

# 81 — this gate's own premises are in the brief.
for w in 'C-190' 'NEVER opens, comments on, approves, un-drafts or merges a PR' 'NEVER merges anything the fleet can see and never pushes' 'CodeQL is NOT RUN by this gate on any tree' 'Blocker' \
         'pgrep' '`END ok`' '(exit 71)' 'UNKNOWN' '19477a9' 'proxy-addr' 'npm ci --offline --ignore-scripts' 'ENOTCACHED' '_cacache' '84a34404' 'sqlite3' \
         'merge-tree --write-tree' 'hash-object -w' 'write-tree' 'commit-tree' 'GIT_INDEX_FILE' 'argument spelling' 'git remote remove origin' 'TMPDIR' \
         'paths-ignore' 'CI_DEPLOY_ENABLED' 'skipped' 'gitleaks' '.gitleaks.toml' 'gitleaks-canary.sh' 'git archive' 'NEXUSAI_LOCK_BASE' 'locks-laptop-1017' 's78g-regate' 'T9' 'C57_ROOT' \
         'rm -rf' 'worktree remove --force' 'WRONG 1' 'WRONG 2' 'WRONG 3' 'WRONG 4' 'WRONG 6' 'WRONG 7' 'WRONG 9' 'WRONG 10' 'MEASURED' 'READ-ONLY-INFERRED' \
         'ADDENDUM 7' 'datasecau/Reporting_Dashboard_Au' 'RETIRED' 'wednesday' 'PROVISIONAL' '3c33f5ae' 'claude-opus-5-5' 'Node v26.8.1' 'S101O' 'RD-771' 'RD-790' \
         'PR #94' 'PR #58' '#256-#259' 'js/xss-through-dom' 'escapeHtml' 'WeakMap' 'data-original-text' 'cdn.jsdelivr.net' 'bootstrap.Modal' 'page.route' '--host-resolver-rules' \
         "channel: 'chrome'" 'deviceScaleFactor' 'getImageData' 'window.__rd778' 'index-offline.js' 'chart-details.js' 'first-run-setup.js' 'settings.js' 'errorCode' \
         'SEM0100' "O'Brien" 'Printer Summary & Costs' 'rd395' 'C-02' 'SYNTHETIC_DEMO_FEED' 'qa-ledger25.js' 'qa-netbelt.sb' '888203c' '428f042' '2d2caa3' '4676' '292'; do
  grep -qiF -- "$w" "$BRIEF" || { echo "REFUSING: brief lacks this gate's premise '$w'" >&2; exit 81; }
done

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
# fleet-monitor and every live 'QA/*' pane other than this gate's own: a negative control when exactly one claude runs under it.
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

# 86 — no live gate-27 session already exists.
for P in $(pane_pid_of "$ROUTE_NAME"); do
  if [ -n "$(claude_under "$P")" ]; then echo "REFUSING: a pane named $ROUTE_NAME (pid $P) already runs a claude — gate 27 is live; do not start a second session" >&2; exit 86; fi
  [ "$CHECK" = "1" ] || echo "NOTE: a pane named $ROUTE_NAME (pid $P) exists with no claude under it — the cockpit's own add decides" >&2
done

# 32S / 40 — LAST: the coordinator's stamp (0 at-sign SLOT placeholders anywhere in the kit: RULED: T0-T9, SELF-CHECK + note; the SELF-CHECK line
# in the fleet's form), the READY in briefs/ (not an override), and the answer route (Tuesday adds it, never this launcher).
STAMP_OK=1
NSLOT="$(grep -oF "$PH_SLOT" "$BRIEF" | grep -c .)"
if [ "$NSLOT" != "0" ] || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then STAMP_OK=0; fi
ROUTE_OK=1
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || ROUTE_OK=0
READY_OK=1
[ -z "${QA_READY_OVERRIDE_778:-}" ] || READY_OK=0
GUARDS='9 MODEL 40 6 7 8 18M 18T 18 90 91 22 93 96 70 70N 31 39 10 17 11 12 13 14 15 20 41 82 19 24 53 71 76 77 78 79 81 38R 86'
if [ "$STAMP_OK" = "0" ] || [ "$ROUTE_OK" = "0" ] || [ "$READY_OK" = "0" ]; then
  echo "guards pass ($GUARDS); stamp, route and/or READY NOT complete." >&2
  echo "  ls-remote attempts this run: $LSR_ATTEMPTS (C-192); origin main ${M_ORIGIN:0:7} (landing chain 36a0dc0/fb8197a -> 5eb80a7/2d2caa3 -> 888203c/428f042 by ancestry); RD-778 ${H778:0:7}; pull/94 ${P94:0:7}; lock tool ${INST_NOW:0:12}…; c57 ${C57_NOW:0:12}…; c133 ${C133_NOW:0:12}…; Chrome ${CHV:-?}; model $MODEL" >&2
  echo "  NEG seats (38R, derived live; coordinator pane '$COORD_NAME'):$NEG_DESC" >&2
  [ "$READY_OK" = "1" ] || echo "REFUSING (31R): the READY was read from QA_READY_OVERRIDE_778 — launch without the override" >&2
  [ "$STAMP_OK" = "1" ] || echo "REFUSING (32S): $NSLOT at-sign SLOT placeholder(s) remain in the brief (the RULED: slots T0-T9, the SELF-CHECK line and the Self-check note), or the SELF-CHECK line is not in the fleet's form — the coordinator re-reads end-to-end and stamps them before launch" >&2
  if [ "$ROUTE_OK" = "0" ]; then
    echo "REFUSING (40): no '${ROUTE_NAME}|tuesday-agent@agentmail.to|no' line in $ROUTING — answers to the gate would have no route; Tuesday adds it at stamp (this launcher never writes it)" >&2; exit 40
  fi
  exit 32
fi

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  origin at $PIN_TS ($LSR_ATTEMPTS ls-remote attempt(s), C-192): main = 888203c exactly (!= c7ca0ed); $B778 = ${H778:0:7}; pull/94 ${P94:0:7} (18); T9 unmounted (18T)"
  echo "  T0 landing check (18M): 888203c tree 428f042, parents 2facd7c + 5eb80a7; ancestry carries tree fb8197a at 36a0dc0; c7ca0ed -> 36a0dc0 -> 5eb80a7 -> 888203c; e2bb3ac vs 428f042 = 3 paths; C-170 not landed"
  echo "  lock tool 3c33f5ae… pinned, NEXUSAI_LOCK_BASE honoured, Laptop-DEV base present, no qa-g27 ticket (90); c57 1ae84a10… + c133 6f938bfc… pinned (91)"
  echo "  pin tables (40); chain (7, 8); gated + both-sides sets (22); premises (93); Chrome ${CHV:-?} (96); rulings + answers (70); evidence + gate 24/25 instruments (31)"
  echo "  MODEL RULE (82); H-1 (76); H-4 (77); H-9 (78); H-7/H-8 (79); premises (81); route $ROUTE_NAME (40); report absent (17); 0 SLOT placeholders (32S)"
  echo "  NEG seats (38R, derived live; coordinator pane '$COORD_NAME'):$NEG_DESC"
  echo "  model: $MODEL at exec (from models_latest.json)"
  echo "  SUBJECT: $SUBJECT"
  echo "  NEXUSAI_LOCK_BASE=$LOCK_BASE_LAPTOP  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  --check started no claude; nothing written."
  exit 0
fi

PROMPT="$PROMPT

VERIFIED BY THE LAUNCHER AT $PIN_TS (git ls-remote origin, read-only, $LSR_ATTEMPTS attempt(s) under C-192): refs/heads/main = $M_ORIGIN (exactly 888203c, not c7ca0ed; tree 428f042, parents 2facd7c + 5eb80a7; its ancestry carries tree fb8197a at 36a0dc0 and the chain c7ca0ed -> 36a0dc0 -> 5eb80a7 -> 888203c holds; C-170 not on main); refs/heads/$B778 = $H778; refs/pull/94/head = ${P94:-absent}. The T9 is unmounted. The installed lock tool $LOCKTOOL sha256 $INST_NOW equals the pin and NEXUSAI_LOCK_BASE=$LOCK_BASE_LAPTOP is exported in your environment. The C-57 runner sha256 $C57_NOW and the C-133 tool sha256 $C133_NOW equal their pins. The READY copy's sha256 equals $READY_SHA. Google Chrome reads ${CHV:-unreadable}. These are the start-of-gate pins; take your own three readings anyway.
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
