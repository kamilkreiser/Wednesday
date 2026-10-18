#!/bin/bash
# launch_qa_nexusai_gate25.sh — cross-project QA agent, ONE gate on Datasec/NexusAI (gate 25): a TIER-1 RE-GATE AS MERGED of two
# already-gated heads on today's main — three merged trees, three verdicts, one order ruling, ONE report
# (drafted 2026-10-18 from ~11:36 AEDT by a read-only drafting agent for Tuesday; the drafter ran only bash -n and --check).
# A FRESH gate on the Mac mini, /Volumes/Laptop-DEV; the T9 is UNMOUNTED, so the lock base is the Laptop-DEV locks-laptop-1017.
#   RD-761 rd-761-law-endpoint-policy-s89r @ 7f1881e (gate 20 GO) AS MERGED onto main c7ca0ed            -> M761  tree fb8197a
#   RD-794 rd-794-ollama-runtime-slice-s89r @ cd171f9 (gate 19 GO WITH FINDINGS) STACKED on M761         -> M794S tree e2bb3ac
#                                                                         and onto c7ca0ed alone        -> M794M tree 64bebaa
#   The seat's merge commits (36a0dc0, 2facd7c, 67f361d) are detached worktree HEADs: the gate REBUILDS every tree in its own store.
#
# LAUNCHED ONLY VIA: cockpit.sh add 'QA/NexusAI-gate25' "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate25.sh'"
#   (i.e. /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh). A tmux pane, NEVER nohup, never run it bare from a seat's shell.
#
# AUTHORITY: Tuesday's gate-25 drafting commission (2026-10-18) and her ANSWER-5 to S101O ("a tier-1 RE-GATE ... BATCHED with RD-794").
# THE MODEL RULE: Kam, live board 2026-09-30 09:07, card nexusai-gate11-opus55-safeguard-model-switch, option (b), PER SESSION.
# Carried rulings (sqlite3 cached prebuild; full verifies UNBELTED; npm_config_update_notifier=false; ruling (b) + EXTENSION; C-190 + ADDENDUM;
# C-209; C-141 ADDENDA 6/7; the by-hand gate yield RETIRED; C-215 the rename rule; the load-8 rule; the Laptop-DEV lock base while the T9 is out).
# FINDINGS-ONLY: never merges (outside its own store), never pushes, never opens/comments/approves/updates a PR, never dismisses an alert, never
# swaps or edits the lock tool, the C-57 runner or the C-133 tool; no fix, no deploy, no az, no docker, no production, no demo, no human.
#
# PATTERN: launch_qa_nexusai_gate24.sh (prompt EMBEDDED, --check mode, pin guards with the C-192 retry, THE MODEL RULE, floor, H-rules, the LIVE
# negative-control seat derivation 38R, stamp + route guards last) + the Vision gate 22/23 PIN-table parser. CHANGES, each deliberate:
#   - 40: heads AND merged trees come ONLY from the brief's PIN-HEADS and MERGE-PINS tables, cross-checked against this launcher's pins.
#   - 18: origin main must be c7ca0ed EXACTLY (every row is on it); both branches exactly their pins; 18T: the T9 MOUNTED refuses (one base).
#   - 90: NEXUSAI_LOCK_BASE is EXPORTED to the Laptop-DEV base (gate 24 unset it for the T9); 91: the C-57 runner and C-133 tool pinned.
#   - 94: the seat's merged objects read BY SHA (trees, parents, counts, lock, alert-site counts, patch-ids) — a NOTE if they are gone.
#   - no docker, no az guards beyond refusing to need them; the READYs are read from briefs/ (Tuesday copies them in at stamp).
#   - READY paths overridable by QA_READY_OVERRIDE_761 / QA_READY_OVERRIDE_794 (drafter's --check only; the launch refuses with them set).
#
# Identity: exports NexusAI's OWN az/gh dirs (az is NOT used; gh READ-ONLY); CLAUDE_CONFIG_DIR pinned to Tuesday's store.
# --check is READ-ONLY in NexusAI: git read verbs (cat-file, log, merge-base, diff, show, rev-parse, ls-remote, rev-list, ls-tree, patch-id on
# diff output); shasum / bash -n / grep over session-tools files; python over `git show` output; ls, ps, tmux list-panes, test -e. Writes nothing.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate25.sh [--check]
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

QA_DIR='/Volumes/Laptop-DEV/!CODING/Testing Agent MAIN'
TUE='/Volumes/Laptop-DEV/TUESDAY'
BRIEFS="$TUE/2_Project_Files/fleet/qa-agent/briefs"
STAGED="$TUE/2_Project_Files/fleet/briefs_staged"
TBRIEFS="$TUE/2_Project_Files/tuesday/briefs"
BRIEF="$BRIEFS/2026-10-18_nexusai-gate25-rd761-rd794-merged.md"
BRIEF22="$BRIEFS/2026-10-13_nexusai-gate-batch22.md"
BRIEF23="$BRIEFS/2026-10-16_nexusai-gate-batch23.md"
BRIEF24="$BRIEFS/2026-10-17_nexusai-gate24-rd848.md"
BRIEF19="$BRIEFS/2026-10-07_nexusai-gate-batch19.md"
BRIEF20="$BRIEFS/2026-10-08_nexusai-gate-batch20.md"
READY_761="${QA_READY_OVERRIDE_761:-$BRIEFS/2026-10-18_nexusai-rd761-merged-READY-mail.txt}"
READY_794="${QA_READY_OVERRIDE_794:-$BRIEFS/2026-10-18_nexusai-rd794-merged-READY-mail.txt}"
ANS1="$TBRIEFS/2026-10-18_S101O_ANSWER-1_plan-confirmation.md"
ANS3="$TBRIEFS/2026-10-18_S101O_ANSWER-3_rd761-c57-renames-accepted.md"
ANS4="$TBRIEFS/2026-10-18_S101O_ANSWER-4_c133-accounted.md"
ANS5="$TBRIEFS/2026-10-18_S101O_ANSWER-5_rd761-regate-batched.md"
SUCC="$TBRIEFS/2026-10-18_nexusai_successor_S101O.md"
CHARTER="$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"
MODELS_JSON="$TUE/0_Brain/dashboard/data/models_latest.json"
MODEL_PIN='claude-opus-5-5'
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
LOCK_BASE_LAPTOP="$ST/locks-laptop-1017"                       # Tuesday's base while the T9 is unmounted (ruling q)
LOCKQ_J="$LOCK_BASE_LAPTOP/queue-jest"
CLAR="$NX/1_Project_Definition/CLARIFICATIONS.md"
BRIEF_761_B="$NX/qa-briefs/2026-10-07_nexusai-rd761-fixround-tier1-gate.md"
BRIEF_794_B="$NX/qa-briefs/2026-10-06_nexusai-rd794-tier1-gate.md"
C68_761="$ST/s89r/c68-rd761.txt"
RPTS="$QA_DIR/projects/nexusai/reports"
B24_DIR="$RPTS/2026-10-17-gate24-rd848"
B24_REPORT="$B24_DIR/report.md"
B24_INST="$B24_DIR/evidence/inst"
REPORT="$RPTS/2026-10-18-gate25-rd761-rd794-merged/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"
ROUTE_NAME='QA/NexusAI-gate25'
NPM_CACHE="${HOME}/.npm/_cacache"
PREBUILD="${HOME}/.npm/_prebuilds/0068db-sqlite3-v5.1.7-napi-v6-darwin-arm64.tar.gz"
PREBUILD_SHA='84a34404b12ff212adbca70eff76c2e4dd83b91245eed0b4569438f928567afc'

# ---- the pins (cross-checked against the brief's two tables, guard 40)
MAIN_SHA='c7ca0ed7113750b268028f12e8659bf1e3d34282'      # origin main at drafting (11:38:37 AEDT) = PR #90 (RD-828 s2)
B761='rd-761-law-endpoint-policy-s89r'
H761='7f1881eae1e816381f0f36f1c415bba7589cdb1a'
MB761='8853e3628382d3ec7fcc653cb7be7bbf210a3eda'
N761=17
G20_BASE='72ca5d3'                                         # gate 20's range 72ca5d3..7f1881e (7 linear)
B794='rd-794-ollama-runtime-slice-s89r'
H794='cd171f953a4cba86379b2343a5bd31f9cb74f0c1'
MB794='3e6d02d48876b01d43b0360026a66c78d191ed70'
N794=7
SM761='36a0dc0eb801e5eb52a00be7c0d3de360eb1952d'; T761='fb8197a78a94806a2bc7b7ec00ff6e8758788a12'; CB761='6a55f685ece310fc8829d602c1581c83397347e0'
SM794S='2facd7c0645755de400770fe4f2db641f46ba42e'; T794S='e2bb3ac1048266dacb13dcc913eebfd76f8bad09'; CB794S='a11d7ec95dd98b35ee16519b8516bf66b689f546'
SM794M='67f361da446731157896de1767f744d86e786e81'; T794M='64bebaa26481a25ac54051a7b722642f6bf62680'; CB794M='c4a921c7c6f75a39b2abe8086188b6a12e232b47'

COUNTS_FILE='scripts/verify-expected-counts.json'
PKG='package.json'
LOCK='package-lock.json'
DEPLOY_WF='.github/workflows/deploy-demo.yml'
DEPLOY_BLOB='953b2a2f84e8710bea857ec87c6f00faa50fa56b'
PKG_BLOB='384805d9e286718bb34ffd05be01c62c00806cf5'
LOCK_BLOB='19477a9329f17e529c208d91d172b95b47fc1bb5'
LOCK_761='d6d3b6e42aa604320f3b70f8e9048bfac044f277'
LOCK_794='e9063d44757007324b8c55fa58c03c03dfe552ae'
POLICY='backend/services/lawEndpointPolicy.js'; POLICY_BLOB='99730a6c09dd4c69c094a531fa9c2dc18e81dcd9'
SYNTH='backend/syntheticFeed.js'; SYNTH_BLOB='604dff3cb8eb5732a4543f09268c9f4066f4ca0f'
MCFG='model-config.js'; MCFG_BLOB='6cc798694135732f708b967dbdd167c83ed0cefa'
LLMIDX='backend/llm/index.js'; LLMIDX_BLOB='f0e377de16023776b061408268ccd7d405569216'
OLLA='backend/llm/ollamaAdapter.js'
ALA='backend/azureLogAnalytics.js'
SRV='backend/server.js'
GATED_761='__tests__/boot-probe-log-redaction.test.js __tests__/discover-tables-tenant-mask.test.js __tests__/helpers/rd761-law-intercept-preload.js __tests__/rd761-law-endpoint-policy.test.js __tests__/rd761-law-writers.test.js backend/azureLogAnalytics.js backend/server.js backend/services/lawEndpointPolicy.js backend/syntheticFeed.js scripts/verify-expected-counts.json'
GATED_794='__tests__/helpers/rd395-llm-mock-preload.js __tests__/helpers/rd819-parked-NOT-RUN/rd819-w5-azure-empty-body.test.js __tests__/llm-provider-default-azure-openai.test.js __tests__/rd395-ai-enabled-gate.test.js __tests__/rd395-ai-enabled-writer.test.js __tests__/rd395-ai-toggle-write.test.js __tests__/rd395-raw-model-calls.test.js __tests__/rd423-test-ai-does-not-crash-server.test.js __tests__/rd794-ollama-runtime-removed.test.js __tests__/security-fixes.test.js backend/llm/index.js backend/llm/ollamaAdapter.js backend/server.js model-config.js scripts/verify-expected-counts.json'
OLLAMA_REPLACE=".replace(/\\/+\$/, '')"
NEG_SEATS=''   # 38R: DERIVED at launch from the live cockpit panes — never stamped by hand

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — gate 25'
QUESTION_SUBJ='[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>'
STATUS_SUBJ='[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch'
PARK_LINE='PARKED: flagged — awaiting the Opus 4.8 switch'
ANSWER_PREFIX='[Tuesday -> QA/NexusAI-gate25] ANSWER'
NOTTESTED_LINE="Not tested by this gate: CodeQL and the CI Build on any merged tree (no pull request carries one; Tuesday reads them at landing), the full jest suite on Node 24 (every run used this machine's Node 26.8.1), a real Azure Log Analytics, Entra or Azure OpenAI endpoint (every outbound attempt was ledgered and refused by the belt), the Azure SDK LogsQueryClient paths beyond what the ledger records (RD-830), npm audit against the merged trees unless Tuesday ruled it (the lockfile is byte-identical to main's), the image, the demo (behind RD-76 SSO) and any deployed revision, a deploy-demo run itself (its skip is read from the workflow condition and the variables), the gate 19 and gate 20 reports (on the unmounted T9), the closure of alerts #23 to #27, #19 and #20 (read on main after each land, C-209), Partner Center, the host npm registry (node_modules from an offline cache copy with install scripts skipped and the update notifier off; sqlite3's binding from its cached prebuild), and Windows."
SAFE_PRINTER='if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET (length ${#SESSION_SECRET})"; else echo "SESSION_SECRET UNSET"; fi'

g() { git --no-optional-locks -C "$REPO" "$@"; }
counts_blob() { g cat-file -p "$1" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
counts_at() { counts_blob "$(g rev-parse --verify -q "${1}:${COUNTS_FILE}" 2>/dev/null)"; }
blob() { g rev-parse --verify -q "${1}:${2}" 2>/dev/null; }
cntF() { g show "${1}:${2}" 2>/dev/null | grep -cF -- "$3"; }
lineat() { g show "${1}:${2}" 2>/dev/null | sed -n "${3}p"; }
ntests() { g ls-tree -r -z --name-only "$1" -- __tests__ 2>/dev/null | tr '\0' '\n' | grep -c .; }
fsha() { shasum -a 256 "$1" 2>/dev/null | cut -d' ' -f1; }
lockver() { g cat-file -p "$1" 2>/dev/null | python3 -c 'import json,sys; print(json.load(sys.stdin)["packages"].get("node_modules/"+sys.argv[1],{}).get("version",""))' "$2" 2>/dev/null; }
both_sides() { comm -12 <(g diff --name-only "$1" "$2" 2>/dev/null | sort) <(g diff --name-only "$1" "$3" 2>/dev/null | sort) | tr '\n' ' ' | sed 's/ $//'; }
pid_of() { g diff "$1" "$2" -- "$3" 2>/dev/null | g patch-id --stable 2>/dev/null | cut -d' ' -f1; }
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

You are the fleet QA/testing agent running ONE gate on Datasec/NexusAI, gate 25: a TIER-1 RE-GATE AS MERGED of two already-gated heads on today's main, with three merged trees, three verdicts, one order ruling and ONE report. It is a FRESH gate on Kam's Mac mini, working volume /Volumes/Laptop-DEV; the T9 drive is UNMOUNTED, so the project's jest lock lives on this drive's locks-laptop-1017 base. The heads: RD-761 (the Log Analytics endpoint allow-list, workspace and tenant GUID guards at the sinks, admin-gated writers; gate 20 GO at 7f1881eae1e816381f0f36f1c415bba7589cdb1a) and RD-794 (the runtime Ollama path removed; gate 19 GO WITH FINDINGS at cd171f953a4cba86379b2343a5bd31f9cb74f0c1). Main has moved 138 commits since RD-761's merge base 8853e36 and 174 since RD-794's 3e6d02d, so Tuesday ruled a re-gate of each head AS IT WOULD LAND: M761 = RD-761 merged onto main c7ca0ed7113750b268028f12e8659bf1e3d34282 (pinned tree fb8197a78a94806a2bc7b7ec00ff6e8758788a12); M794S = RD-794 STACKED on M761, the C-199 shape (tree e2bb3ac1048266dacb13dcc913eebfd76f8bad09); M794M = RD-794 onto c7ca0ed alone (tree 64bebaa26481a25ac54051a7b722642f6bf62680). The builder's three local merge commits exist only as detached worktree HEADs in the project's object store: you REBUILD every merged tree yourself in your own store and PROVE its id; never trust the seat's trees, logs or tables as the proof. FINDINGS-ONLY: you NEVER merge anything the fleet can see, NEVER push, NEVER open, comment on, approve or merge a pull request, never dismiss an alert, and NEVER swap, copy over or edit the installed lock tool, the C-57 runner or the C-133 tool; no fixes, no deploys, no az, no docker, no production, no HTTP to any production or demo host, nothing to Partner Center, the demo or any human, no browser, no host npm registry. One client only: Datasec/NexusAI.

READ YOUR COMMISSION FIRST, whole: /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-18_nexusai-gate25-rd761-rd794-merged.md
It opens with the PIN-HEADS and MERGE-PINS tables, the TIER argument and the drafter's WRONG OR UNVERIFIED list (each item MEASURED or READ-ONLY-INFERRED), then TUESDAY'S RULINGS (T1 to T9 as Tuesday stamped them, the eight properties, the carried rulings) and THE MODEL RULE: apply them, do not re-rule them. Then the charter it names; both READY mails it names, read WHOLE; Tuesday's ANSWER-3, ANSWER-4 and ANSWER-5 to the builder; the clarifications it names at source (C-215, C-57, C-133 and C-190 first); the two builder gate briefs it names (RD-761's fix round with its CORRECTION, RD-794's with its C-133 F3 table); gates 22, 23 and 24's section 3a (the H-rules, carried by reference); and gate 24's report on THIS drive (the structural template and the instrument source). The gate 19 and gate 20 reports are on the unmounted T9: NOT READ, named. Every builder statement is a CLAIM — RELAYED, never evidence. The brief's section 2a rows r0 to r10 (with r5b), section 2b (how RD-761's policy works, so the interaction probe can fail on the right thing) and section 2c (the per-id accounting) are required measurement.

THE MODEL RULE (Kam, live board 2026-09-30 09:07, card (b)): QA gates may switch to Opus 4.8 when flagged by Opus 5.5's safeguards, PER SESSION. You start on Opus 5.5. You run the FULL rows. If one of your responses is stopped by the safeguards: that step is NOT RUN (never re-worded to slip past); write ONE line to evidence/classifier-stops.txt; let any running step finish and let the hold exit so you never sit holding a lock (H-28); mail tuesday-agent@agentmail.to with the subject exactly "[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch"; then end your turn with the line "PARKED: flagged — awaiting the Opus 4.8 switch" and wait. Tuesday switches THIS pane's model and taps you by mail. You never answer the model dialog yourself, and nobody ever chooses "Switch automatically". After the switch, resume at the stopped row. The report states which rows ran on which model, with the switch time, and quotes classifier-stops.txt whole.

THE EIGHT PROPERTIES, per merged tree (brief sections 2a to 2c). (1) THE TREE ROW r1: in your own --mirror store (T6: a plain clone carries neither head), git merge-tree --write-tree of each pair must conflict in scripts/verify-expected-counts.json ONLY; your raw merge tree must differ from the pin in that path only; with the seat's counts blob substituted, write-tree must equal the pin; your own full verify passing on that tree is the counts file's assertion; positive control first (your method on c7ca0ed's own merge) and a negative control (another counts blob gives another id). (2) THE INTERACTION ROWS: r2 — RD-761's policy against everything main changed since 8853e36: read its MECHANISM at the merged tree (the sinks decide at request time, before any token; a stored value from any path is checked at use), build a call graph by FUNCTION, transitively, from every route, boot step and scheduler into the Log Analytics client and token code, and PROBE a booted local server of M761 and M794S (T8) with stored hostile endpoints, workspaces and tenants while your SOCKET LEDGER (H-36) records every outbound connection attempt through ANY library — axios, fetch, https, the SDK's LogsQueryClient — with its positive controls (each library seen) and its negative control (the same probes at c7ca0ed, which has no policy, DO reach for the attacker host); helper-wrapped calls the builder's grep cannot see are exactly what this row exists for; the health surfaces that RD-761 and main both touched are probed. r4 — RD-794's removal against main's changes since 3e6d02d: nothing on main reaches removed Ollama code, every surviving mention classified, the LLM_PROVIDER matrix, the ai-test listener that hears nothing on the merged trees and something at c7ca0ed, and the AI-enabled gates still holding with stored aiEnabled=false. (3) THE CELL ROWS: r3 — the gated cells BY NAME on each merged tree, plus mutant red-proofs ON THE MERGED TREE (a mutant killed at the head but not on the merged tree is a cell DISARMED by the merge, C-102); r5 — the full verify on each merged tree, names as SETS vs main; r5b — C-57 through a byte-identical COPY of the installed runner with C57_ROOT pointing at your own shim (T1), C-133 through a copy of the installed tool, every leftover classified per section 2c: Tuesday's rename rule C-215 applied EXACTLY, all three conditions per id (the branch side carries the merge base's blob; the merged tree carries main's blob byte for byte; the retitled name passes in YOUR merged run), and RD-794's own nine B-side ids as T2 rules; anything else is a STOP. (4) THE ALERT ROW r6: #23 to #26 (RD-761) and #27, #19, #20 (RD-794) read by number with gh READ ONLY, their sites gone or fixed in each merged tree, located first at c7ca0ed (the control); CodeQL itself runs only at a PR, so state what Tuesday must read at landing. (5) THE AUDIT ROW r7: the merged trees carry main's lockfile 19477a9 and package.json 384805d, proxy-addr 2.0.8 from the lock and from each installed tree's own path; npm audit only as T3 rules. (6) THE DEPLOY ROW r8: deploy-demo must SKIP on landing — the workflow's two if: conditions on vars.CI_DEPLOY_ENABLED, the variables read (T3), the last Deploy demo runs. (7) THE ORDER ROW r9: stacked (RD-761 then RD-794) versus main-order, which lands are fast-forwards of gated trees, what each order would need re-measured, the intermediate main each passes through — and RULE it on the evidence (the turn order stays Tuesday's). (8) THE SECRETS ROW r10: gitleaks 8.30.1 over both gated ranges, your merges, and git archive extractions of each merged tree, after a planted throwaway string is found first; never print a value. Plus r0 scope and pins.

MAIN MUST NOT MOVE (ruling b): the launcher verified origin main = c7ca0ed exactly; take M0 by git ls-remote at YOUR start and say so. If main moves mid-gate, every merged tree is stale: name what landed, finish nothing that would read as a verdict on the new main, and mail a QUESTION (C-68). GitHub SSH intermittently denies auth (C-192): retry every ls-remote up to 5 times about 10 s apart; a FAILED ls-remote is UNKNOWN, never a value. Re-hash the lock tool, the C-57 runner and the C-133 tool at start, mid and end.

C-190 + its ADDENDUM — BOTH thresholds block: every merge to main goes through a pull request that adds no new high-or-higher CodeQL alert in changed code (test code included), AND any new alert whose RULE severity is error blocks whatever its security severity. Alerts are fixed in code, never dismissed. C-209: a PR's CodeQL run cannot show a pre-existing main alert as fixed; closure is read on main's push analysis after the land, by number. No PR carries any merged tree: CodeQL is NOT RUN on any merged tree and the CI Build is NOT RUN — say so. C-185 (ruling h): read its known set at source; any other failure is by NAME; no re-run is a clearance.

THE LOCK (C-63). The installed tool is session-tools/nexusai-lock.sh in the NexusAI project on this drive, sha256 3c33f5ae58e1be20282467a90b27a23a2de998eedd0e56c03f3c06360031a792. While the T9 is unmounted the base is NEXUSAI_LOCK_BASE=/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/session-tools/locks-laptop-1017, which the launcher has EXPORTED into your environment: keep it on every jest step, quote the c57 runner's resolved LOCK_BASE= and ROOT= line, and never touch this drive's stale session-tools/locks (a 2026-09-22 holder lives there). If the T9 mounts mid-gate, finish the running hold, file nothing more, and mail a QUESTION. EVERY jest run and every booted probe server goes in the jest lock, each hold tagged qa-g25- (no tag of yours contains the word "merge": C-141 ADDENDUM 7), ONE hold at a time. MERGES GO FIRST and RULING (i)'s BY-HAND GATE YIELD IS RETIRED: if a ticket is queued ahead of you, wait behind it (FIFO) — the builder S101O is live and files jest holds on the same base. AT A WAIT DEADLINE: --replace on your own still-waiting ticket BEFORE its deadline fires (C-141: a SAME-PLACE handover), confirmed from the queue listing (the old ticket to released/ as ticket-left-*, your place unchanged); a duplicate-tag refusal takes a -r<N> suffix. Read queue-jest at start, around every hold and at end; any qa-g25- entry that is not your current hold is a STOP. Read your inbox before filing every new hold. THE LOAD RULE: file a hold and start any full jest only below a 1-minute load of 8 (8 cores; Tuesday's ANSWER-1 to S101O; it supersedes the 40 in older briefs).

NODE_MODULES WITHOUT THE HOST REGISTRY (ruling m, H-31): offline npm ci --offline --ignore-scripts --no-audit --no-fund with --cache pointing at an APFS clone of the local npm cache on the same volume; the three merged trees share lock 19477a9, so ONE proven install is APFS-cloned into the other two; EVERY npm invocation carries npm_config_update_notifier=false (prove the cache copy's _update-notifier-last-checked marker absent or unchanged); an ENOTCACHED is NOT RUN, named, with a QUESTION — never go online from the host, never npm install. sqlite3's binding from the cached prebuild (an APFS clone of ~/.npm/_prebuilds), inside the strict belt, IS PART OF H-31, with its three conditions (the tarball's and the unpacked node_sqlite3.node's sha256; CI builds its own Linux binding; every row that boots the host server names "sqlite3 binding: cached prebuild, offline"). proxy-addr must resolve 2.0.8 from each merged tree's own path (RD-827, C-205). The C-57 runner does its own offline npm ci per worktree: that is its method, recorded, and its B-side install of cd171f9 carries proxy-addr 2.0.7 by that head's own lockfile — never read as the merged tree's.

FULL VERIFIES (r5) through the jest lock, UNBELTED by Tuesday's 2026-10-05 answer to gate 14 (ruling n), with its four conditions. SESSION_SECRET UNSET, npm_config_update_notifier=false npm run verify -- --maxWorkers=2 --forceExit (prove the flag reached jest), Node v26.8.1 as T5 rules. RULING (b) and its EXTENSION (ruling o): if a verify stays lock-starved about 2 h after filing, deliver it NAMED NOT RUN — never "skipped" — with the brief's coverage sentence in NOT TESTED. The TIER-1 cell rows (r3) and the interaction rows (r2, r4) are NOT covered by that extension: they run, and a TIER-1 verdict whose cell or interaction rows did not run is PROVISIONAL and releases nothing. A mutant counts only if it LANDED (the exact mutated text present, the original absent) and parses; a red from a mutant that never landed is a VOID arm, a planted control that does not fire makes its row VOID (never a pass), and an edit whose anchor is absent fails loudly and nothing downstream runs on that tree.

THE INSTRUMENT RULES H-1 TO H-36 (brief section 3a; gates 22, 23 and 24's section 3a read WHOLE). H-1: the ONLY SESSION_SECRET printer is the one the brief quotes; self-test it and gate 24's scan. H-3: a LANDING CONTROL for every plant, probe, mutant and stored hostile configuration. H-4: the HEARTBEAT is a separate child of the hold wrapper, aborted if absent 90 s after the grant, max gap reported. H-6: every path with a space quoted; every host jest run but the full verifies, every driver and every booted server under your copy of the belt with its landing control. H-9: byte plants by Buffer, checked with xxd. H-11/H-18: /bin/bash explicitly, "${sha}:${path}" quoted (zsh eats :s and :a). H-17: censuses by pgrep, never ps. H-20: a per-step hard DEADLINE on every jest run (with --forceExit), every runner invocation, every npm ci and every server boot (qa-to.sh). H-21: every file you mutate is restored by a trap on EXIT (also INT and TERM) installed BEFORE the first mutation. H-22: never nest sandbox-exec (it exits 71). H-24: jest array options after the paths, lists built in bash. H-26: C-192 retries. H-27: THE MODEL RULE. H-28: ONE focused hold at a time, at most about 40 minutes planned (T1's three runner holds excepted), rows GROUPED, a hold that would overrun SPLIT, every part file bash -n checked before filing; you stay in the FOREGROUND — a hold that must outlive one tool call runs as a TRACKED child of your session (never nohup) with its timeout at the 2-hour maximum; each hold carries a wait deadline and you --replace before it fires. H-29: other gates' and the builder's evidence is method only. H-31: offline host node_modules. H-32: every booted server is a local run on loopback by the gate — NOT the demo. H-33: never rm — quarantine (T1's disclosed runner exception only); every child reaped by pid. H-34: the Laptop-DEV lock base. H-35: NO docker object and NO az command, not even az version. H-36: THE SOCKET LEDGER — a require-first preload records every outbound connection attempt (host, port, pid, first product frame, time; never a body, header or token) and the belt refuses it; its positive controls prove it sees axios, fetch, https and LogsQueryClient, or that library's probe arm is NOT RUN, named.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT (fresh mktemp dirs under projects/nexusai/qa-trees/gate25.* in /Volumes/Laptop-DEV/!CODING/Testing Agent MAIN): ONE --mirror clone of the NexusAI repo on THIS drive as your store (T6), your refs g25/* in it, your three merge commits in it, every work tree a clone of that store, status-checked before use, EXCLUSIVE to one purpose. NEVER work in the NexusAI root checkout or any worktrees/ folder (LIVE, the builder's: read the seat's merge commits BY SHA only). In the NexusAI repo use ONLY read verbs (show, diff, log with an explicit rev, ls-tree, cat-file, grep, ls-remote, rev-parse, merge-base, rev-list, count-objects, for-each-ref); NEVER fetch, pull, push, checkout, worktree, commit, stash, gc, merge, merge-tree --write-tree or hash-object -w there. Copy instruments BY NAME from gate 24's evidence/inst on THIS drive (never the whole directory), re-point every gate-24 path in your copies to gate 25 — INCLUDING the lock base line, which gate 24's copies UNSET for the T9 and yours set to the Laptop-DEV base (quote that diff) — and correct the floor library's ROOT and NEG defaults from the live list below; never write into another gate's dirs on either drive. Never write into the builders' session-tools (S101O is live in s101/: hash it at start and end); never run the seat's scripts in place. Findings-only: never push, no commits outside your store, no tickets, no PRs, no edits in NexusAI. No Microsoft, Log Analytics or login host, no CDN, no demo, no Partner Center, no workflow dispatch, no repo variable written. No mail to any human. Never rm: quarantine.

FLOOR DISCIPLINE — section 9 of the brief exactly. Do ALL lock-free work first (pins, hashes, reads, r0, r1's rebuild and its controls, r2's and r4's reading halves, r6 to r10, the offline npm ci, the ledger and belt self-tests); then file your holds one at a time through your COPY of gate 24's qa-file24.sh re-pointed to qa-g25 tags and the jest kind. QUEUE, NEVER TAKE OVER: never signal, move or edit another seat's process, lock, ticket or worktree. Count foreign servers the C-125 way anchored on YOUR OWN claude pid, with the negative-control seats the launcher derived (listed at the end of this prompt) classifying foreign in the same run; re-derive them at every hold's start; a hold with no live negative control aborts. A zero is reportable only beside a control that fired in the same window. DEADLINE AND HEARTBEAT: every step has a per-step DEADLINE, every child is killed in a finally by pid from your own ancestry (C-174, never by pattern), a HEARTBEAT line at least every 2 minutes during a hold, and a step with no heartbeat for 5 minutes is aborted and reported.

RE-PIN at start, mid and end: main and both branches (rd-761-law-endpoint-policy-s89r, rd-794-ollama-runtime-slice-s89r), refs/pull/58/head, plus the three tools' sha256 — three timestamped readings with the branch name and attempt count beside each sha. A head that disagrees with the brief is a FINDING and a reason to stop, never a typo to fix. Call main at your start M0 and say so. Count the NexusAI .git/objects files and their newest mtime at start and end and account for any delta.

QUESTIONS: your routing name is QA/NexusAI-gate25. If you must ask, mail tuesday-agent@agentmail.to with subject "[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>" and PROCEED ON THE SAFEST READING without waiting (the one exception is a safeguards stop, which PARKS you under THE MODEL RULE); Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/NexusAI-gate25] ANSWER". Approval-class items (anything Azure, the demo, Partner Center, money, a human, the live lock tool) are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your ONE report to: /Volumes/Laptop-DEV/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-10-18-gate25-rd761-rd794-merged/report.md
Write its VERDICT and FINDINGS table early and keep it current. Findings are G25-<n>, notes N25-<n>, each naming its tree, instrument and evidence class.

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with the subject exactly:
[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — gate 25
Lead the body with the FOUR lines in the form the brief's section 11 gives — RD-761 AS MERGED, RD-794 STACKED, RD-794 MAIN-ORDER (each with its TREE, INTERACTION, CELLS, VERIFY, C-57, C-133, C-215, ALERTS, AUDIT, DEPLOY-DEMO and GITLEAKS clauses) and ORDER — then one line naming M0 and END main, the C-102 sweep, which rows ran on Opus 4.8 (or none), which holds ran and which are NAMED NOT RUN under ruling (b) extended, and "CodeQL NOT RUN on any merged tree (no PR carries one)". The report's last four lines are those same four lines. Never wednesday-agent@. You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/Laptop-DEV/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no 4_Credentials directory of its own. Never put the key, a token, a session value or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice — the only turn you end while waiting is the PARKED line of THE MODEL RULE.

Rule 2 stands: what you did NOT test is first-class output — a NOT TESTED section carrying the builder's stated limits, every declared limit L-B1 to L-B7 and L-Y1 discharged with a measurement or left standing and named (C-112), Prior work checked (C-49), every finding naming its instrument, and every action recommendation labelled MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. The tester never fixes. C-215, C-57, C-133, C-190 with its ADDENDUM, C-209, C-199, C-186, C-185 with its ADDENDA, C-192, C-205, C-141 with ADDENDA 6 and 7, C-63, C-40, C-68, C-76, C-102, C-112 and C-174 are the clarifications this gate leans on; C-49, C-89, C-115, C-125, C-130, C-131 and C-203 are carried. That section must carry this line verbatim:
Not tested by this gate: CodeQL and the CI Build on any merged tree (no pull request carries one; Tuesday reads them at landing), the full jest suite on Node 24 (every run used this machine's Node 26.8.1), a real Azure Log Analytics, Entra or Azure OpenAI endpoint (every outbound attempt was ledgered and refused by the belt), the Azure SDK LogsQueryClient paths beyond what the ledger records (RD-830), npm audit against the merged trees unless Tuesday ruled it (the lockfile is byte-identical to main's), the image, the demo (behind RD-76 SSO) and any deployed revision, a deploy-demo run itself (its skip is read from the workflow condition and the variables), the gate 19 and gate 20 reports (on the unmounted T9), the closure of alerts #23 to #27, #19 and #20 (read on main after each land, C-209), Partner Center, the host npm registry (node_modules from an offline cache copy with install scripts skipped and the update notifier off; sqlite3's binding from its cached prebuild), and Windows.
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
[ "$MPIN" != "NO-BLOCK" ] && [ -n "$MPIN" ] || { echo "REFUSING: the brief has no MERGE-PINS block — the merged trees have nowhere to come from" >&2; exit 40; }
prow() { printf '%s\n' "$1" | awk -F'\t' -v id="$2" '$1==id'; }
pfld() { prow "$1" "$2" | awk -F'\t' -v n="$3" '{print $n}'; }
is40()  { printf '%s' "$1" | grep -Eq '^[0-9a-f]{40}$'; }
[ "$(printf '%s\n' "$PIN" | wc -l | tr -d ' ')" = "3" ] || { echo "REFUSING: PIN-HEADS must carry exactly three rows (MAIN RD761 RD794)" >&2; exit 40; }
[ "$(printf '%s\n' "$MPIN" | wc -l | tr -d ' ')" = "3" ] || { echo "REFUSING: MERGE-PINS must carry exactly three rows (M761 M794S M794M)" >&2; exit 40; }
for ID in MAIN RD761 RD794; do
  R="$(prow "$PIN" "$ID")"
  [ "$(printf '%s\n' "$R" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: PIN-HEADS must carry exactly one row '$ID'" >&2; exit 40; }
  [ "$(printf '%s\n' "$R" | awk -F'\t' '{print NF}')" = "7" ] || { echo "REFUSING: PIN-HEADS row $ID does not have 7 cells: $R" >&2; exit 40; }
  printf '%s' "$R" | grep -q '@' && { echo "REFUSING: PIN-HEADS row $ID still carries a placeholder" >&2; exit 40; }
  [ "$(pfld "$PIN" "$ID" 7)" = "IN" ] || { echo "REFUSING: PIN-HEADS row $ID status is not IN" >&2; exit 40; }
  [ "$(pfld "$PIN" "$ID" 2)" = "nexusai" ] || { echo "REFUSING: PIN-HEADS row $ID repo must be nexusai" >&2; exit 40; }
  is40 "$(pfld "$PIN" "$ID" 4)" || { echo "REFUSING: PIN-HEADS row $ID head is not a 40-hex sha" >&2; exit 40; }
done
[ "$(pfld "$PIN" MAIN 3)" = "main" ] && [ "$(pfld "$PIN" MAIN 4)" = "$MAIN_SHA" ] || { echo "REFUSING: PIN-HEADS MAIN is not main @ c7ca0ed — this launcher's guards are pinned to it; re-brief" >&2; exit 40; }
[ "$(pfld "$PIN" RD761 3)" = "$B761" ] && [ "$(pfld "$PIN" RD761 4)" = "$H761" ] && [ "$(pfld "$PIN" RD761 5)" = "$MB761" ] && [ "$(pfld "$PIN" RD761 6)" = "$N761" ] \
  || { echo "REFUSING: PIN-HEADS RD761 is not $B761 @ 7f1881e, base 8853e36, $N761 commits" >&2; exit 40; }
[ "$(pfld "$PIN" RD794 3)" = "$B794" ] && [ "$(pfld "$PIN" RD794 4)" = "$H794" ] && [ "$(pfld "$PIN" RD794 5)" = "$MB794" ] && [ "$(pfld "$PIN" RD794 6)" = "$N794" ] \
  || { echo "REFUSING: PIN-HEADS RD794 is not $B794 @ cd171f9, base 3e6d02d, $N794 commits" >&2; exit 40; }
mchk() { # id ours theirs seat tree counts tests suites
  local R; R="$(prow "$MPIN" "$1")"
  [ "$(printf '%s\n' "$R" | awk -F'\t' '{print NF}')" = "8" ] || { echo "REFUSING: MERGE-PINS row $1 does not have 8 cells: $R" >&2; exit 40; }
  printf '%s' "$R" | grep -q '@' && { echo "REFUSING: MERGE-PINS row $1 still carries a placeholder" >&2; exit 40; }
  [ "$R" = "$(printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$8")" ] || { echo "REFUSING: MERGE-PINS row $1 is not as this launcher pins it: '$R'" >&2; exit 40; }
}
mchk M761  "$H761" "$MAIN_SHA" "$SM761"  "$T761"  "$CB761"  4646 289
mchk M794S "$H794" M761        "$SM794S" "$T794S" "$CB794S" 4655 290
mchk M794M "$H794" "$MAIN_SHA" "$SM794M" "$T794M" "$CB794M" 4568 288

# 6 — every sha the guards use is a commit in the local object store (this launcher never fetches).
for S in "$MAIN_SHA" "$H761" "$H794" "$MB761" "$MB794" "$G20_BASE"; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 7 / 8 — the chains: merge bases, counts, merges, neither head on main.
[ "$(g merge-base "$H761" "$MAIN_SHA" 2>/dev/null)" = "$MB761" ] || { echo "REFUSING: merge-base(7f1881e, c7ca0ed) is not 8853e36" >&2; exit 7; }
[ "$(g merge-base "$H794" "$MAIN_SHA" 2>/dev/null)" = "$MB794" ] || { echo "REFUSING: merge-base(cd171f9, c7ca0ed) is not 3e6d02d" >&2; exit 7; }
g merge-base --is-ancestor "$MB794" "$MB761" 2>/dev/null || { echo "REFUSING: 3e6d02d is not an ancestor of 8853e36 (the stacked base reading)" >&2; exit 7; }
for S in "$H761" "$H794"; do
  if g merge-base --is-ancestor "$S" "$MAIN_SHA" 2>/dev/null; then echo "REFUSING: ${S:0:7} is ALREADY on main c7ca0ed — re-brief" >&2; exit 7; fi
done
[ "$(g rev-list --count "${MB761}..${H761}" 2>/dev/null)" = "$N761" ] && [ "$(g rev-list --merges --count "${MB761}..${H761}" 2>/dev/null)" = "1" ] \
  && [ "$(g rev-list --count "${G20_BASE}..${H761}" 2>/dev/null)" = "7" ] && [ -z "$(g rev-list --merges "${G20_BASE}..${H761}" 2>/dev/null)" ] \
  || { echo "REFUSING: RD-761 is not 17 commits over 8853e36 with ONE merge, and 7 linear over gate 20's 72ca5d3" >&2; exit 8; }
[ "$(g rev-list --count "${MB794}..${H794}" 2>/dev/null)" = "$N794" ] && [ -z "$(g rev-list --merges "${MB794}..${H794}" 2>/dev/null)" ] \
  || { echo "REFUSING: RD-794 is not 7 linear commits over 3e6d02d" >&2; exit 8; }

# 18T — the T9 MOUNTED refuses: two lock bases would split the FIFO (ruling q); Tuesday decides the base first.
[ ! -d "$T9_VOL" ] || { echo "REFUSING: $T9_VOL is MOUNTED — the brief's lock base (locks-laptop-1017) assumes it is not; Tuesday decides the base, then re-brief" >&2; exit 18; }

# 18 — RE-PIN NOW by ls-remote (C-192 retries): main EXACTLY c7ca0ed; both branches exactly their pins.
lsr refs/heads/main "refs/heads/$B761" "refs/heads/$B794" refs/pull/58/head || { echo "REFUSING: git ls-remote origin failed after $LSR_ATTEMPTS attempt(s) — UNKNOWN, not a value (C-192); relaunch later" >&2; exit 18; }
LSR_ALL="$LSR_OUT"
ref_now() { printf '%s\n' "$LSR_ALL" | awk -v r="$1" '$2==r{print $1}'; }
M_ORIGIN="$(ref_now refs/heads/main)"
[ "$M_ORIGIN" = "$MAIN_SHA" ] || { echo "REFUSING: origin main is '${M_ORIGIN:-unreadable}', not c7ca0ed — every merged tree of this gate is ON c7ca0ed; re-brief" >&2; exit 18; }
[ "$(ref_now "refs/heads/$B761")" = "$H761" ] || { echo "REFUSING: origin $B761 is '$(ref_now "refs/heads/$B761")', not 7f1881e — moved (a landing push?); re-brief" >&2; exit 18; }
[ "$(ref_now "refs/heads/$B794")" = "$H794" ] || { echo "REFUSING: origin $B794 is '$(ref_now "refs/heads/$B794")', not cd171f9 — moved; re-brief" >&2; exit 18; }
P58="$(ref_now refs/pull/58/head)"
[ "$P58" = "$H761" ] || echo "NOTE: refs/pull/58/head is '${P58:-absent}', not 7f1881e — PR #58 moved; the gate reads it (§8)" >&2
PRREF="$(g ls-remote origin 'refs/pull/*/head' 2>/dev/null | awk -v h="$H794" '$1==h{print $2}' | tr '\n' ' ')"
[ -z "$PRREF" ] || echo "NOTE: a PR ref now carries cd171f9 (${PRREF}) — the brief says RD-794 has no PR; the gate reads it (§8)" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 90 — the INSTALLED lock tool PINNED; it honours NEXUSAI_LOCK_BASE; the Laptop-DEV base is present with queue-jest; no qa-g25 ticket.
INST_NOW="$(fsha "$LOCKTOOL")"
[ "$INST_NOW" = "$LOCK_SHA_INST" ] || { echo "REFUSING: the INSTALLED lock tool's sha256 is '${INST_NOW:-absent}', not 3c33f5ae… — find out who changed it; re-brief" >&2; exit 90; }
grep -qF 'BASE="${NEXUSAI_LOCK_BASE:-' "$LOCKTOOL" || { echo "REFUSING: the installed tool no longer honours NEXUSAI_LOCK_BASE — ruling q's premise" >&2; exit 90; }
bash -n "$LOCKTOOL" 2>/dev/null || { echo "REFUSING: $LOCKTOOL does not parse (bash -n)" >&2; exit 90; }
grep -qF -- '--replace' "$LOCKTOOL" && grep -qF 'jest|docker) ;;' "$LOCKTOOL" || { echo "REFUSING: $LOCKTOOL lacks --replace or the jest kind" >&2; exit 90; }
[ -d "$LOCK_BASE_LAPTOP" ] && [ -d "$LOCKQ_J" ] || { echo "REFUSING: the Laptop-DEV lock base $LOCK_BASE_LAPTOP (queue-jest) is not present (ruling q)" >&2; exit 90; }
BQ="$(grep -l '^tag=qa-g25' "$LOCKQ_J"/* 2>/dev/null | wc -l | tr -d ' ')"
[ "${BQ:-0}" = "0" ] || { echo "REFUSING: $BQ qa-g25* ticket(s) already in $LOCKQ_J — a live or stale gate-25 ticket; read before launch" >&2; exit 90; }
MQ="$(grep -lE '^tag=.*(^|[-_=])merge([0-9]+[a-z]?)?([-_]|$)' "$LOCKQ_J"/* 2>/dev/null | wc -l | tr -d ' ')"
[ "${MQ:-0}" = "0" ] || echo "NOTE: $MQ merge-tagged ticket(s) in $LOCKQ_J now — the gate files behind them (brief §9)" >&2
HOLDER="$(sed -n 's/^tag=//p' "$LOCK_BASE_LAPTOP/nexusai-jest.lock/owner" 2>/dev/null | head -1)"
case "$HOLDER" in
  qa-g25*) echo "REFUSING: the Laptop-DEV jest lock is HELD by '$HOLDER' — a gate-25 holder already exists" >&2; exit 90 ;;
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

# 22 — the gated file sets and the both-sides-changed sets.
[ "$(g diff --name-only "$MB761" "$H761" 2>/dev/null | sort | tr '\n' ' ' | sed 's/ $//')" = "$(printf '%s\n' $GATED_761 | sort | tr '\n' ' ' | sed 's/ $//')" ] \
  || { echo "REFUSING: RD-761's gated files (8853e36..7f1881e) are not the briefed ten" >&2; exit 22; }
[ "$(g diff --name-only "$MB794" "$H794" 2>/dev/null | sort | tr '\n' ' ' | sed 's/ $//')" = "$(printf '%s\n' $GATED_794 | sort | tr '\n' ' ' | sed 's/ $//')" ] \
  || { echo "REFUSING: RD-794's gated files (3e6d02d..cd171f9) are not the briefed fifteen" >&2; exit 22; }
[ "$(both_sides "$MB761" "$H761" "$MAIN_SHA")" = "$ALA $SRV $COUNTS_FILE" ] || { echo "REFUSING: RD-761 vs main both-sides set is not azureLogAnalytics.js + server.js + counts (got '$(both_sides "$MB761" "$H761" "$MAIN_SHA")')" >&2; exit 22; }
[ "$(both_sides "$MB794" "$H794" "$MAIN_SHA")" = "$SRV $COUNTS_FILE" ] || { echo "REFUSING: RD-794 vs main both-sides set is not server.js + counts" >&2; exit 22; }

# 93 — the premises at source on the heads and main (blobs, lockfiles, alert sites, deploy-demo, counts, census).
[ "$(blob "$H761" "$POLICY")" = "$POLICY_BLOB" ] && [ "$(blob "$H761" "$SYNTH")" = "$SYNTH_BLOB" ] && [ -z "$(blob "$MAIN_SHA" "$POLICY")" ] \
  || { echo "REFUSING: lawEndpointPolicy.js / syntheticFeed.js at 7f1881e are not 99730a6 / 604dff3, or the policy already exists on main" >&2; exit 93; }
[ "$(blob "$H794" "$MCFG")" = "$MCFG_BLOB" ] && [ "$(blob "$H794" "$LLMIDX")" = "$LLMIDX_BLOB" ] && [ -z "$(blob "$H794" "$OLLA")" ] && [ -n "$(blob "$MAIN_SHA" "$OLLA")" ] \
  || { echo "REFUSING: model-config.js / llm/index.js at cd171f9 are not 6cc7986 / f0e377d, or ollamaAdapter.js is not deleted there / present on main" >&2; exit 93; }
[ "$(blob "$MAIN_SHA" "$LOCK")" = "$LOCK_BLOB" ] && [ "$(blob "$MAIN_SHA" "$PKG")" = "$PKG_BLOB" ] && [ "$(blob "$H761" "$LOCK")" = "$LOCK_761" ] && [ "$(blob "$H794" "$LOCK")" = "$LOCK_794" ] \
  || { echo "REFUSING: the lockfile / package.json blobs are not 19477a9+384805d (main), d6d3b6e (RD-761), e9063d4 (RD-794)" >&2; exit 93; }
[ "$(lockver "$LOCK_BLOB" proxy-addr)" = "2.0.8" ] && [ "$(lockver "$LOCK_794" proxy-addr)" = "2.0.7" ] && [ "$(lockver "$LOCK_761" proxy-addr)" = "2.0.8" ] \
  || { echo "REFUSING: proxy-addr is not 2.0.8 (19477a9, d6d3b6e) / 2.0.7 (e9063d4) as briefed (RD-827, RD-816)" >&2; exit 93; }
for S in "$MAIN_SHA" "$H761" "$H794" "$MB761" "$MB794"; do
  [ "$(blob "$S" "$DEPLOY_WF")" = "$DEPLOY_BLOB" ] || { echo "REFUSING: $DEPLOY_WF at ${S:0:7} is not 953b2a2 (r8's premise)" >&2; exit 93; }
done
[ "$(cntF "$MAIN_SHA" "$DEPLOY_WF" "vars.CI_DEPLOY_ENABLED == 'true'")" = "2" ] && [ "$(cntF "$MAIN_SHA" "$DEPLOY_WF" 'branches: [main]')" = "1" ] \
  || { echo "REFUSING: deploy-demo.yml no longer gates BOTH jobs on vars.CI_DEPLOY_ENABLED == 'true' on push to main" >&2; exit 93; }
case "$(lineat "$MAIN_SHA" "$SRV" 16606)" in *"String(ollamaEndpoint)$OLLAMA_REPLACE"*) ;; *) echo "REFUSING: c7ca0ed server.js:16606 is not #19's ollamaEndpoint .replace site" >&2; exit 93 ;; esac
case "$(lineat "$MAIN_SHA" "$SRV" 16815)" in *"String(ollamaEndpoint)$OLLAMA_REPLACE"*) ;; *) echo "REFUSING: c7ca0ed server.js:16815 is not #20's ollamaEndpoint .replace site" >&2; exit 93 ;; esac
[ "$(g show "${H794}:${SRV}" 2>/dev/null | grep -F "$OLLAMA_REPLACE" | grep -ci ollama)" = "0" ] || { echo "REFUSING: cd171f9 still carries an ollamaEndpoint .replace site (#19/#20)" >&2; exit 93; }
[ "$(counts_at "$MAIN_SHA")" = "4559 287" ] && [ "$(counts_at "$H761")" = "4394 268" ] && [ "$(counts_at "$H794")" = "4274 262" ] \
  || { echo "REFUSING: counts are not 4559/287 (main), 4394/268 (RD-761), 4274/262 (RD-794)" >&2; exit 93; }
[ "$(ntests "$MAIN_SHA")" = "341" ] && [ "$(ntests "$H761")" = "315" ] && [ "$(ntests "$H794")" = "308" ] || { echo "REFUSING: the __tests__ census is not 341 / 315 / 308" >&2; exit 93; }
grep -qF 'LAW_API_BASES' <(g show "${H761}:${POLICY}" 2>/dev/null) && grep -qF 'const isLawGuid = isTenantGuid;' <(g show "${H761}:${POLICY}" 2>/dev/null) \
  || { echo "REFUSING: lawEndpointPolicy.js no longer reads as §2b describes (LAW_API_BASES, isLawGuid alias)" >&2; exit 93; }

# 94 — the seat's merged objects, read BY SHA (detached worktree HEADs: if gone, a NOTE — the gate rebuilds and compares to the pins).
SEAT_OK=1
for S in "$SM761" "$SM794S" "$SM794M"; do [ "$(g cat-file -t "$S" 2>/dev/null)" = "commit" ] || SEAT_OK=0; done
if [ "$SEAT_OK" = "1" ]; then
  par() { g log -1 --format='%P' "$1" 2>/dev/null; }
  [ "$(par "$SM761")" = "$H761 $MAIN_SHA" ] && [ "$(par "$SM794S")" = "$H794 $SM761" ] && [ "$(par "$SM794M")" = "$H794 $MAIN_SHA" ] \
    || { echo "REFUSING: the seat's merge commits' parents are not as the MERGE-PINS table says" >&2; exit 94; }
  [ "$(g rev-parse "${SM761}^{tree}")" = "$T761" ] && [ "$(g rev-parse "${SM794S}^{tree}")" = "$T794S" ] && [ "$(g rev-parse "${SM794M}^{tree}")" = "$T794M" ] \
    || { echo "REFUSING: a seat merge commit's tree is not its pin" >&2; exit 94; }
  [ "$(blob "$SM761" "$COUNTS_FILE")" = "$CB761" ] && [ "$(blob "$SM794S" "$COUNTS_FILE")" = "$CB794S" ] && [ "$(blob "$SM794M" "$COUNTS_FILE")" = "$CB794M" ] \
    && [ "$(counts_blob "$CB761")" = "4646 289" ] && [ "$(counts_blob "$CB794S")" = "4655 290" ] && [ "$(counts_blob "$CB794M")" = "4568 288" ] \
    || { echo "REFUSING: the seat's counts blobs are not 6a55f68 4646/289, a11d7ec 4655/290, c4a921c 4568/288" >&2; exit 94; }
  for S in "$SM761" "$SM794S" "$SM794M"; do
    [ "$(blob "$S" "$LOCK")" = "$LOCK_BLOB" ] && [ "$(blob "$S" "$PKG")" = "$PKG_BLOB" ] && [ "$(blob "$S" "$DEPLOY_WF")" = "$DEPLOY_BLOB" ] \
      || { echo "REFUSING: merged ${S:0:7} does not carry main's lockfile / package.json / deploy-demo.yml" >&2; exit 94; }
  done
  [ "$(blob "$SM761" "$POLICY")" = "$POLICY_BLOB" ] && [ "$(blob "$SM794S" "$POLICY")" = "$POLICY_BLOB" ] && [ -z "$(blob "$SM794M" "$POLICY")" ] \
    && [ -n "$(blob "$SM761" "$OLLA")" ] && [ -z "$(blob "$SM794S" "$OLLA")" ] && [ -z "$(blob "$SM794M" "$OLLA")" ] \
    || { echo "REFUSING: the policy / ollamaAdapter.js presence in the merged trees is not as r6 predicts" >&2; exit 94; }
  [ "$(pid_of "$H761" "$SM761" "$SRV")" = "$(pid_of "$MB761" "$MAIN_SHA" "$SRV")" ] && [ "$(pid_of "$H761" "$SM761" "$ALA")" = "$(pid_of "$MB761" "$MAIN_SHA" "$ALA")" ] \
    && [ "$(pid_of "$H794" "$SM794S" "$SRV")" = "$(pid_of "$MB794" "$SM761" "$SRV")" ] && [ "$(pid_of "$H794" "$SM794M" "$SRV")" = "$(pid_of "$MB794" "$MAIN_SHA" "$SRV")" ] \
    || { echo "REFUSING: a head->merged patch-id no longer equals the other side's base->side patch-id (WRONG 3)" >&2; exit 94; }
  SEAT_NOTE="seat merge objects present, trees/parents/counts/lock/patch-ids as pinned"
else
  SEAT_NOTE="seat merge objects NOT in the store (worktrees removed?) — the gate rebuilds and compares to the MERGE-PINS"
  echo "NOTE: $SEAT_NOTE" >&2
fi

# 70 — the carried rulings and Tuesday's answers (REFUSALs where a ruling is missing).
[ -s "$SQLITE_RULING" ] && grep -qF 'The offline unpack of sqlite3' "$SQLITE_RULING" || { echo "REFUSING: Tuesday's sqlite3 prebuild ruling (ruling m) is not at $SQLITE_RULING" >&2; exit 70; }
[ -s "$BELT_ANS" ] && grep -qF 'run UNBELTED. Every other jest run stays belted: cells, mutants, C-68 unions, drivers and servers.' "$BELT_ANS" \
  || { echo "REFUSING: Tuesday's belt answer (ruling n) is not at $BELT_ANS as quoted" >&2; exit 70; }
[ -s "$NOTIFIER_ANS" ] && grep -qF 'Every later npm invocation in this gate carries npm_config_update_notifier=false' "$NOTIFIER_ANS" \
  || { echo "REFUSING: Tuesday's notifier answer (ruling m) is not at $NOTIFIER_ANS as quoted" >&2; exit 70; }
[ -s "$RULING_B" ] && grep -qF 'Deliver the verdict NOW.' "$RULING_B" && grep -qF 'merge hold full verify + PR Build are the gate' "$RULING_B" \
  || { echo "REFUSING: Tuesday's ruling (b) is not at $RULING_B as quoted" >&2; exit 70; }
grep -qF 'NOT RUN, named, under ruling (o) EXTENDED' "$BRIEF24" && grep -qF 'NOT RUN, named, under ruling (o) EXTENDED' "$BRIEF" \
  || { echo "REFUSING: ruling (o)'s EXTENSION words are not carried in gate 24's brief and this brief (the T9 source is unmounted)" >&2; exit 70; }
[ -s "$G19_RELEASE" ] && grep -qF 'the by-hand gate yield (ruling (i)) is RETIRED from gate 21 on.' "$G19_RELEASE" \
  && grep -qF 'RD-794 @ cd171f9: GO WITH FINDINGS (F-794-1, F-794-2 Minor; MG-vc-fn survivor, RD-820).' "$G19_RELEASE" \
  || { echo "REFUSING: gate 19's RELEASE no longer carries the yield retirement and RD-794's verdict as quoted" >&2; exit 70; }
[ -s "$ANS1" ] && grep -qF 'load1 below 8 before every heavy run' "$ANS1" && grep -qF 'lock base locks-laptop-1017' "$ANS1" \
  || { echo "REFUSING: Tuesday's ANSWER-1 (load 8, lock base) is not at $ANS1 as quoted" >&2; exit 70; }
[ -s "$ANS3" ] && grep -qF "Anything outside those three conditions stays a STOP for me. The tool's verdict line is quoted verbatim beside the accounting; never edit the tool." "$ANS3" \
  || { echo "REFUSING: Tuesday's ANSWER-3 (the rename rule) is not at $ANS3 as quoted" >&2; exit 70; }
[ -s "$ANS4" ] && grep -qF 'RD-794 (both orders): the same ruling applies to any leftover that meets ANSWER-3' "$ANS4" || { echo "REFUSING: Tuesday's ANSWER-4 is not at $ANS4 as quoted" >&2; exit 70; }
[ -s "$ANS5" ] && grep -qF "it proves the hunks are main's, not that main's code since 8853e36 is covered by RD-761's endpoint policy." "$ANS5" \
  && grep -qF 'it gets a tier-1 RE-GATE, not a counts-only TURN, and that gate is BATCHED with RD-794' "$ANS5" \
  || { echo "REFUSING: Tuesday's ANSWER-5 (the re-gate ruling) is not at $ANS5 as quoted" >&2; exit 70; }
[ -s "$SUCC" ] && grep -qF 'NEXUSAI_LOCK_BASE=/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/session-tools/locks-laptop-1017' "$SUCC" \
  || { echo "REFUSING: the S101O brief no longer carries the Laptop-DEV lock-base ruling (ruling q)" >&2; exit 70; }

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
[ "$GLV" = "8.30.1" ] || echo "NOTE: gitleaks is '${GLV:-absent}', not 8.30.1 — r10 records it (CI pins 8.30.1)" >&2
LOAD1="$(sysctl -n vm.loadavg 2>/dev/null | awk '{print $2}')"
awk -v l="${LOAD1:-99}" 'BEGIN{exit !(l < 8)}' || echo "NOTE: 1-minute load is ${LOAD1:-unknown} (not below 8) — the gate waits in the queue, never in a hold (ruling p)" >&2

# 31 — READYs, builder briefs, builder evidence, gate 24's instruments (THIS drive), standing references.
for f in "$READY_761" "$READY_794" "$CLAR" "$BRIEF22" "$BRIEF23" "$BRIEF24" "$BRIEF19" "$BRIEF20" "$B24_REPORT" "$CHARTER" "$BRIEF_761_B" "$BRIEF_794_B" "$C68_761" \
         "$S101/c57-rd761.out" "$S101/c57-rd794-stacked.out" "$S101/c57-rd794-main.out" "$S101/c133-rd761.out" "$S101/c133-rd794-stacked.out" "$S101/c133-rd794-main.out" \
         "$S101/rd761-gated-files-36a0dc0.txt" "$S101/rd794-gated-files-stacked.txt" "$S101/rd794-gated-files-main.txt" "$S101/callsites-rd761.txt" "$S101/callsites-rd794.txt" \
         "$S101/rd761-cells.json" "$S101/rd794-cells-stacked.json" "$S101/rd794-cells-main.json" "$S101/verify-merge-rd761.log" "$S101/verify-merge-rd794-stacked.log" "$S101/verify-merge-rd794-main.log" \
         "$B24_INST/env24.sh" "$B24_INST/HOLD24.sh" "$B24_INST/qa-file24.sh" "$B24_INST/qa-file24r.sh" "$B24_INST/qa-floorlib24.sh" "$B24_INST/qa-floorcount.py" "$B24_INST/qa-to.sh" \
         "$B24_INST/qa-pin24.sh" "$B24_INST/qa-qlist24.sh" "$B24_INST/qa-k1-24.sh" "$B24_INST/qa-mut24.py" "$B24_INST/qa-npm24.sh" "$B24_INST/qa-runj24.sh" "$B24_INST/qa-verify24.sh" \
         "$B24_INST/qa-holdlib24.sh" "$B24_INST/qa-h1-selftest24.sh" "$B24_INST/qa-h1-scan.py" "$B24_INST/qa-mail24.py" "$B24_INST/qa-mailread24.py" "$B24_INST/qa-jestwrap.sh" \
         "$B24_INST/qa-jsum.js" "$B24_INST/qa-lockcheck.py" "$B24_INST/qa-names23.py" "$B24_INST/qa-ssprint.sh" "$B24_INST/qa-netbelt.sb" "$B24_INST/qa-netbelt-nodns.sb" "$B24_INST/qa-netbelt-ctl.js"; do
  [ -s "$f" ] || { echo "REFUSING: evidence, brief or tool absent: $f" >&2; exit 31; }
done
grep -qF "${H761:0:7}" "$READY_761" && grep -qF 'READY FOR GATE' "$READY_761" && grep -qF 'PRIOR WORK' "$READY_761" && grep -qF 'NOT TESTED' "$READY_761" && grep -qF "$T761" "$READY_761" \
  || { echo "REFUSING: the RD-761 READY does not name 7f1881e, its tree fb8197a, READY FOR GATE, PRIOR WORK and NOT TESTED" >&2; exit 31; }
grep -qF 'READY FOR GATE' "$READY_794" && grep -qF 'PRIOR WORK' "$READY_794" && grep -qF 'NOT TESTED' "$READY_794" && grep -qF "$SM794S" "$READY_794" && grep -qF "$T794S" "$READY_794" \
  && grep -qF "$SM794M" "$READY_794" && grep -qF "$T794M" "$READY_794" && grep -qF 'cd171f9' "$READY_794" \
  || { echo "REFUSING: the RD-794 READY does not name both merges and trees, READY FOR GATE, PRIOR WORK and NOT TESTED" >&2; exit 31; }
grep -qF 'VERDICT: accounted 4, still missing 0, absent files 0' "$S101/c133-rd761.out" && grep -qF 'VERDICT: accounted 13, still missing 0, absent files 0' "$S101/c133-rd794-stacked.out" \
  && grep -qF 'VERDICT: accounted 13, still missing 0, absent files 0' "$S101/c133-rd794-main.out" \
  || { echo "REFUSING: a builder C-133 output no longer carries the line the brief relays" >&2; exit 31; }
grep -qF 'STATUS: COMPLETE' "$B24_REPORT" || { echo "REFUSING: gate 24's report does not read as delivered (the instrument source must be a DELIVERED gate)" >&2; exit 31; }
[ ! -e "$B24_INST/.throwaway-ss" ] || echo "NOTE: gate 24's inst/ holds a .throwaway-ss — copy instruments BY NAME, never the directory" >&2
grep -qF 'The rd761 intercept preload sees only axios, so it cannot observe them.' "$BRIEF_761_B" || { echo "REFUSING: the RD-761 builder brief's CORRECTION (LogsQueryClient) is gone" >&2; exit 31; }
grep -qF 'C-133 accounting' "$BRIEF_794_B" && grep -qF 'rd819-parked-NOT-RUN' "$BRIEF_794_B" || { echo "REFUSING: the RD-794 builder brief's C-133 F3 table is gone (T2's named pairs)" >&2; exit 31; }
for B in "$BRIEF22" "$BRIEF23" "$BRIEF24"; do grep -qF '## 3a. INSTRUMENT RULES' "$B" || { echo "REFUSING: $B has no section 3a — the H-rules carried by reference are missing" >&2; exit 31; }; done

# 39 — the floor instrument is named in the brief.
grep -qF 'qa-floorlib24.sh' "$BRIEF" && grep -qF '2026-10-17-gate24-rd848' "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument / gate 24's instrument dir" >&2; exit 39; }

# 10 / 17 — report path named in both; no stale report; brief names every source it cites.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }
for P in "2026-10-18_nexusai-rd761-merged-READY-mail.txt" "2026-10-18_nexusai-rd794-merged-READY-mail.txt" "2026-10-18_S101O_ANSWER-" "2026-10-13_nexusai-gate-batch22.md" \
         "2026-10-16_nexusai-gate-batch23.md" "2026-10-17_nexusai-gate24-rd848.md" "2026-10-07_nexusai-gate-batch19.md" "2026-10-08_nexusai-gate-batch20.md" \
         "2026-10-05_qa_b14_belt_ANSWER.md" "2026-10-06_nexusai_g18_ruling_b_deliver_now.md" "qa-file24.sh" "qa-file24r.sh" "c68-rd761.txt" "census-law-clients.md" \
         "2026-10-07_nexusai-rd761-fixround-tier1-gate.md" "2026-10-06_nexusai-rd794-tier1-gate.md" "models_latest.json" "QA_AGENT_CHARTER.md" ".throwaway-ss" "locks-laptop-1017"; do
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
for T in 'THIS IS A TIER-1 GATE' 'RE-GATE AS MERGED' 'NO GO' 'NO HOST NPM REGISTRY' 'IS PART OF H-31' 'FULL VERIFIES UNBELTED' 'EXTENSION' \
         'npm_config_update_notifier=false' 'BOTH thresholds block' 'RULING (b)' 'NAMED NOT RUN' '--replace' 'qa-g25-' 'RETIRED' 'H-34' 'H-35' 'H-36' 'C-63' 'C-215' \
         'THE TREE ROW' 'THE INTERACTION' 'THE CELL ROW' 'THE SUITE ROW' 'THE ALERT ROW' 'THE AUDIT ROW' 'THE DEPLOY ROW' 'THE ORDER ROW' 'THE SECRETS ROW' \
         'M761' 'M794S' 'M794M' 'SOCKET LEDGER' 'DISARMED' 'can fail' 'positive control' 'negative control' 'G25-<n>' 'NOT TESTED' 'PRIOR WORK' 'never dismisses an alert' 'No HTTP to any production or demo host'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not declare '$T'" >&2; exit 12; }
done
for T in 'TIER-1 RE-GATE AS MERGED' 'THE EIGHT PROPERTIES' 'THE TREE ROW' 'THE INTERACTION ROWS' 'THE CELL ROWS' 'THE ALERT ROW' 'THE AUDIT ROW' 'THE DEPLOY ROW' 'THE ORDER ROW' 'THE SECRETS ROW' \
         'M761' 'M794S' 'M794M' 'REBUILD' 'SOCKET LEDGER' 'C-215' 'all three conditions' 'DISARMED' 'as SETS' 'STACKED' 'C-199' \
         'UNBELTED' 'npm_config_update_notifier=false' 'BOTH thresholds block' 'RULING (b)' 'EXTENSION' 'NAMED NOT RUN' '--replace' 'qa-g25-' 'RETIRED' 'locks-laptop-1017' \
         'jest lock' 'T1' 'T2' 'T6' 'T8' "never trust the seat's trees" 'no HTTP to any production or demo host' 'One client only' 'NO docker object and NO az'; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare '$T'" >&2; exit 12 ;; esac
done
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
for S in "$H761" "$H794" "$MAIN_SHA" "$LOCK_SHA_INST" "$T761" "$T794S" "$T794M"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S in full" >&2; exit 14; }
  case "$PROMPT" in *"$S"*) ;; *) echo "REFUSING: prompt must name $S" >&2; exit 14 ;; esac
done
for S in "$MB761" "$MB794" "$SM761" "$SM794S" "$SM794M" "$CB761" "$CB794S" "$CB794M" "$C57_SHA" "$C133_SHA" "$PKG_BLOB" "$LOCK_BLOB" "$DEPLOY_BLOB" "$PREBUILD_SHA"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S in full" >&2; exit 14; }
done
for S in "$POLICY_BLOB" "$SYNTH_BLOB" "$MCFG_BLOB" "$LLMIDX_BLOB" "$LOCK_761" "$LOCK_794"; do
  grep -qF -- "${S:0:7}" "$BRIEF" || { echo "REFUSING: brief must name ${S:0:7}" >&2; exit 14; }
done
if printf '%s\n' "$PROMPT" | LC_ALL=C grep -q '@[A-Z_0-9]*@'; then echo "REFUSING: the prompt carries a placeholder" >&2; exit 14; fi
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
[ "$(grep -oE 'qa-g25-[A-Za-z0-9_<>-]*merge[A-Za-z0-9_-]*' "$BRIEF" | grep -c .)" = "0" ] || { echo "REFUSING: the brief suggests a qa-g25- tag containing 'merge' (C-141 ADDENDUM 7)" >&2; exit 15; }
[ "$(printf '%s\n' "$PROMPT" | grep -oE 'qa-g25-[A-Za-z0-9_<>-]*merge' | grep -c .)" = "0" ] || { echo "REFUSING: the prompt suggests a qa-g25- tag containing 'merge'" >&2; exit 15; }

# 41 — RULING (i)'s by-hand yield is RETIRED.
for T in 'stop YOUR OWN unstarted waiter' 'stop your OWN unstarted waiter' 'then re-queue with --after that merge' 'self-apply ONE yield per gate TAG'; do
  if grep -qF -- "$T" "$BRIEF" || printf '%s\n' "$PROMPT" | grep -qF -- "$T"; then echo "REFUSING: '$T' instructs the RETIRED by-hand yield" >&2; exit 41; fi
done
grep -qF 'is RETIRED from gate 21 on.' "$BRIEF" || { echo "REFUSING: the brief does not quote the retirement of ruling (i)'s yield" >&2; exit 41; }
case "$PROMPT" in *"BY-HAND GATE YIELD IS RETIRED"*) ;; *) echo "REFUSING: the prompt does not say the by-hand gate yield is RETIRED" >&2; exit 41 ;; esac

# 82 — THE MODEL RULE is carried in the brief and the prompt, per session, never "Switch automatically".
for T in "$STATUS_SUBJ" "$PARK_LINE" 'classifier-stops.txt' 'Switch automatically' 'Opus 4.8' 'PER SESSION' 'which rows ran on which model' 'Opus 5.5'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks THE MODEL RULE fragment '$T'" >&2; exit 82; }
  case "$(printf '%s' "$PROMPT" | tr '[:upper:]' '[:lower:]')" in *"$(printf '%s' "$T" | tr '[:upper:]' '[:lower:]')"*) ;; *) echo "REFUSING: prompt lacks THE MODEL RULE fragment '$T'" >&2; exit 82 ;; esac
done
grep -qF '## THE MODEL RULE' "$BRIEF" && grep -qF 'H-27' "$BRIEF" && grep -qF 'H-28 (AMENDED' "$BRIEF" && grep -qF 'H-32 (LOCAL ONLY' "$BRIEF" && grep -qF 'H-34 (THE LOCK BASE' "$BRIEF" \
  && grep -qF 'H-35 (NO DOCKER, NO AZ' "$BRIEF" && grep -qF 'H-36 (NEW — THE SOCKET LEDGER' "$BRIEF" \
  || { echo "REFUSING: brief lacks THE MODEL RULE section or H-27/H-28 (amended)/H-32/H-34/H-35/H-36" >&2; exit 82; }

# 19 — the words the prompt must carry (% is a space); the brief's sections; limits; rows; READY lines verbatim; clarification quotes.
WORDS="RD-761 RD-794 RD-827 RD-830 C-215 C-57 C-133 C-190 C-209 C-199 C-186 C-185 C-192 C-205 C-141 C-63 C-40 C-68 C-76 C-102 C-112 C-174 C-49 C-89 C-115 C-125 C-130 C-131 C-203 ADDENDA%6%and%7
r0 r2 r3 r4 r5 r5b r6 r7 r8 r9 r10 T1 T2 T3 T5 T6 T8 M0 8853e36 3e6d02d c7ca0ed 19477a9 384805d 2.0.8 2.0.7 proxy-addr #23 #27 #19 #20 vars.CI_DEPLOY_ENABLED LogsQueryClient
L-B1 L-B7 L-Y1 H-1 H-3 H-4 H-6 H-9 H-17 H-20 H-21 H-22 H-24 H-26 H-27 H-28 H-29 H-31 H-32 H-33 H-34 H-35 H-36 --forceExit trap%on%EXIT DEADLINE LANDING%CONTROL
_prebuilds node_sqlite3.node sqlite3%binding:%cached%prebuild,%offline _update-notifier-last-checked exits%71 --mirror EXCLUSIVE STOP VOID C57_ROOT gitleaks%8.30.1
MERGES%GO%FIRST QUEUE,%NEVER%TAKE%OVER SAME-PLACE%handover HEARTBEAT 2%minutes 5%minutes finally SESSION_SECRET%UNSET NOT%TESTED MEASURED%AT%RUNTIME READ%ONLY PROBED
RELAYED CodeQL%is%NOT%RUN UNKNOWN about%40%minutes 2-hour%maximum TRACKED%child Prior%work FOREGROUND never%push NEVER%merge Partner%Center npm%install --offline ENOTCACHED
qa-file24.sh ticket-left-* -r<N> instrument never%fixes GROUPED SPLIT never%dismissed PROVISIONAL qa-g25 G25-<n> N25-<n> 1-minute%load%of%8 S101O"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## TIER' '^## WRONG OR UNVERIFIED' "^## TUESDAY'S RULINGS" '^## THE MODEL RULE' '^## Charter' '^## THE CLARIFICATIONS THAT BIND THIS GATE' '^## PRIOR ROUND' '^## 1. Target' \
         '^## 2. Tier and severity' '^## 2a. ROWS' '^## 2b. THE RD-761 POLICY' '^## 2c. C-57 / C-133 / C-215' '^## 3. THE QUESTIONS' '^## 3a. INSTRUMENT RULES' '^## 3b. THE NEGATIVE-ASSERTION SWEEP' \
         '^## 7. THE MERGED TREES' '^## 8. CI, ALERTS, AUDIT, DEPLOY-DEMO' '^## 9. Floor discipline' '^## 10. HELD' '^## 11. Output' '^## PROVENANCE' '^### How to build your trees' '^## FILL AT STAMP'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
grep -qF '**A RE-GATE AS MERGED, not a fix round**' "$BRIEF" || { echo "REFUSING: the brief's PRIOR ROUND block does not declare the re-gate (template round-N rule)" >&2; exit 19; }
grep -qF "$B24_REPORT" "$BRIEF" || { echo "REFUSING: the brief does not name gate 24's report path (the structural template)" >&2; exit 19; }
[ "$(grep -n '^## WRONG OR UNVERIFIED' "$BRIEF" | cut -d: -f1)" -lt "$(grep -n "^## TUESDAY'S RULINGS" "$BRIEF" | cut -d: -f1)" ] || { echo "REFUSING: the WRONG OR UNVERIFIED section is not above TUESDAY'S RULINGS" >&2; exit 19; }
WSTART="$(grep -n '^## WRONG OR UNVERIFIED' "$BRIEF" | cut -d: -f1)"; WEND="$(grep -n "^## TUESDAY'S RULINGS" "$BRIEF" | cut -d: -f1)"
WUNMARKED="$(sed -n "${WSTART},${WEND}p" "$BRIEF" | grep -E '^[0-9]+\. ' | grep -vE 'MEASURED|READ-ONLY-INFERRED|disclosed|own actions' | cut -c1-60)"
[ -z "$WUNMARKED" ] || { echo "REFUSING: WRONG items not marked MEASURED / READ-ONLY-INFERRED: $WUNMARKED" >&2; exit 19; }
for L in L-B1 L-B2 L-B3 L-B4 L-B5 L-B6 L-B7 L-Y1; do grep -qF "$L" "$BRIEF" || { echo "REFUSING: brief lacks declared limit $L (C-112)" >&2; exit 19; }; done
for R in r0 r1 r2 r3 r4 r5 r5b r6 r7 r8 r9 r10; do grep -qF "| $R |" "$BRIEF" || { echo "REFUSING: brief lacks row $R" >&2; exit 19; }; done
for n in 1 2 3 4 5 6 7 8 9; do
  grep -qE "^- \*\*\(T${n}\) [^*]*:\*\* RULED: " "$BRIEF" || { echo "REFUSING: brief lacks the ruling slot (T$n) as '**(T$n) …:** RULED: …'" >&2; exit 19; }
done
# the READYs' PRIOR WORK lines the brief quotes, verbatim in both.
while IFS='|' read -r WHICH T; do
  [ -n "$T" ] || continue
  case "$WHICH" in 761) RF="$READY_761" ;; 794) RF="$READY_794" ;; *) continue ;; esac
  grep -qF -- "$T" "$RF" || { echo "REFUSING: '$T' is no longer in the RD-$WHICH READY — the source changed; re-brief" >&2; exit 19; }
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not carry the RD-$WHICH READY line '$T' verbatim" >&2; exit 19; }
done <<'VERBATIM_EOF'
761|PRIOR WORK: gate 20 (GO) on the same head; S89R built the branch; the C-57 and C-133 tools are the installed ones, unedited.
794|PRIOR WORK: gate 19 (GO WITH FINDINGS) on this head; S89R built the branch; the C-133 table is gate 19's (F3). Every C-57 and C-133 run here is my own, with the installed tools.
794|it does not cover a call made through a helper with another name.
VERBATIM_EOF
# the rulings the brief rests on are quoted from source and still say so
while IFS= read -r Q; do
  [ -n "$Q" ] || continue
  grep -qF -- "$Q" "$CLAR" || { echo "REFUSING: CLARIFICATIONS no longer carries '$Q' — the brief's quotes are stale; re-brief" >&2; exit 19; }
  grep -qF -- "$Q" "$BRIEF" || { echo "REFUSING: brief does not quote '$Q'" >&2; exit 19; }
done <<'CLAR_EOF'
A C-57 "missing" name is ACCEPTED as a main-side rename, for the RD-761 re-check and both RD-794 orders, ONLY when all three hold: (1) the branch side carries the merge base's blob of that file; (2) the merged tree carries main's blob byte for byte; (3) the retitled name passes in the merged run
a name whose branch blob differs from base, or whose merged blob is not main's; a retitled name that is absent or red in the merged run; editing `c57-id-superset.sh` or `c133-accounting.py`.
A merge conflict confined to `scripts/verify-expected-counts.json` is resolved by regeneration, with an id-superset control.
It normalises runs of digits only, within the same test file.
A missing id is ACCOUNTED, not a STOP, only when BOTH of these hold for its file: (1) the merged blob is byte-identical to one parent's blob; (2) since the merge base, ONLY that parent changed the file, and the other parent's blob equals the base blob.
No author takes two consecutive turns while another author is ready.
Every merge to NexusAI main goes through a PULL REQUEST, and a PR must add NO NEW high-or-higher CodeQL alert in the code it changes. Test code is included.
`alerts_threshold = errors`, so ANY new alert whose RULE severity is `error` blocks, whatever its security severity.
A PR's CodeQL run CANNOT show a PRE-EXISTING main alert as fixed
RD-709 is built STACKED on RD-736 (`61e20ad`), and RD-736 merges BEFORE RD-709.
counts as known ONLY when the received object differs from the expected in `envReached` alone
No re-run is used as a clearance
a FAILED ls-remote is UNKNOWN, never a value.
A merge hold runs on a node_modules that matches the merged tree's package-lock.json.
is a SAME-PLACE handover.
Gate (`qa-*`) tickets are never moved; the holder is never touched.
TAG CONVENTION — only a merge HOLD's tag contains the word `merge`.
The jest and docker lock (`session-tools/nexusai-lock.sh`) is first-in-first-out, and it takes over an ownerless lock after 30 s.
A check must be able to fail on the thing it claims to be about.
a clean merge-tree and a changed measured surface are not in tension
An explanation of why a fix works is a CLAIM: it gets a red proof, or it is marked UNVERIFIED in the artefact that carries it.
every existing test that relied on a LATER return in that function is a candidate for silent disarmament
A declared limit is where the evidence stops — not a place it is cleared.
NEVER KILL BY PATTERN.
CLAR_EOF

# 24 — the prompt must DESCRIBE the server entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qi 'backend/server\.js'; then
  echo "REFUSING: the prompt contains the server entry point's literal path (RD-591 c.37901). Describe it; do not name it." >&2; exit 24; fi

# 53 / 71 — standing rules in the brief; the NOT TESTED line verbatim in both.
for w in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' 'qa-g25-' 'VOID' 'EXCLUSIVE' 'POSITIVE CONTROL FIRST' 'QUEUE, NEVER TAKE OVER' 'LANDING CONTROL' \
         'MAIN MOVES' '--replace' 'never push' 'C-174' '--forceExit' 'trap … EXIT' 'MERGES GO FIRST' 'queue-jest/' 'carry on' 'never idles holding a lock' \
         'ONE focused hold at a time' 'FOREGROUND' '5600' '8995' '10310' '17220' '14.5 h' 'Never two live holds' 'Every finding names its instrument' \
         'NOT TESTED' 'The tester never fixes' 'SPLIT a hold' 'ONE CLIENT ONLY' 'no CodeQL alert dismissed' 'below a 1-minute load of **8**'; do
  grep -qiF -- "$w" "$BRIEF" || { echo "REFUSING: brief lacks the standing rule '$w'" >&2; exit 53; }
done
grep -qF "$NOTTESTED_LINE" "$BRIEF" || { echo "REFUSING: brief must carry the NOT TESTED line verbatim" >&2; exit 71; }
case "$PROMPT" in *"$NOTTESTED_LINE"*) ;; *) echo "REFUSING: prompt must carry the NOT TESTED line verbatim" >&2; exit 71 ;; esac
grep -qF 'The report'"'"'s LAST four lines are the four verdict lines' "$BRIEF" || { echo "REFUSING: brief must fix the report's last lines as the verdict lines" >&2; exit 71; }

# 76 / 77 / 78 / 79 — H-1's printer and forbidden idioms; H-4; H-9; H-7/H-8.
grep -qF "$SAFE_PRINTER" "$BRIEF" || { echo "REFUSING: brief must carry the safe SESSION_SECRET printer verbatim (H-1)" >&2; exit 76; }
for w in '${SESSION_SECRET-…}' '${SESSION_SECRET+$SESSION_SECRET}' 'printenv' '${envs[*]}' 'docker inspect'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief must name the forbidden idiom $w (H-1)" >&2; exit 76; }
done
for w in 'separate child' 'within 90 s' 'max gap'; do grep -qiF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the heartbeat fragment '$w' (H-4)" >&2; exit 77; }; done
for w in 'H-9' 'Buffer' 'xxd -l 16' 'JSON.stringify'; do grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the byte-plant fragment '$w' (H-9)" >&2; exit 78; }; done
for w in 'H-7' 'H-8' 'negative control' 'original text is absent once the new text is removed' 'FAILS LOUDLY'; do grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the mutant-landing fragment '$w' (H-7/H-8)" >&2; exit 79; }; done

# 81 — this gate's own premises are in the brief.
for w in 'C-190' 'NEVER opens, comments on, approves or merges a PR' 'NEVER merges anything the fleet can see and never pushes' 'CodeQL is NOT RUN on any merged tree' 'Blocker' 'setuid' 'pgrep' '`END ok`' \
         'exits 71' 'ARRAY option' '=====' 'UNKNOWN' '19477a9' 'proxy-addr' 'RD-827' 'npm ci --offline --ignore-scripts' 'ENOTCACHED' '_cacache' '_prebuilds' '84a34404' \
         'sqlite3' 'NOT the demo' 'merge-tree --write-tree' 'hash-object -w' 'write-tree' 'commit-tree' 'GIT_INDEX_FILE' '_updated' 'patch-id' 'detached worktree HEADs' \
         'LAW_API_BASES' 'isLawGuid' 'LAW_ENDPOINT_NOT_ALLOWED' 'LAW_WORKSPACE_ID_INVALID' 'LAW_TENANT_ID_INVALID' 'requireAdminFor' 'healthProjection' 'endpoint-not-allowed' \
         'rd761-law-intercept-preload' 'rd395-llm-mock-preload' 'LLM_PROVIDER' '__proto__' 'ollamaEndpoint' 'OLLAMA_ENDPOINT' 'aiEnabled=false' 'W5' 'rd819-parked-NOT-RUN' \
         'jsdom-instrument-limits' 'rd327-build-digest-on-public-health' 'rd699-decode-branches-behaviour' '5419285' '379b8b5' '5584ea4' '04efa65' 'c36005b' '014c0cd' \
         'deploy-demo.yml' 'CI_DEPLOY_ENABLED' 'skipped' 'gitleaks' '.gitleaks.toml' '.gitleaks-lockfile.toml' 'gitleaks-canary.sh' 'RD-111' 'git archive' \
         'NEXUSAI_LOCK_BASE' 'locks-laptop-1017' 's78g-regate' 'T9' 'C57_ROOT' 'rm -rf' 'worktree remove --force' 'WRONG 1' 'WRONG 2' 'WRONG 4' 'WRONG 5' 'WRONG 6' 'WRONG 8' \
         'MEASURED' 'READ-ONLY-INFERRED' 'qa-floorlib24.sh' 'qa-file24.sh' 'ADDENDUM 7' 'datasecau/Reporting_Dashboard_Au' 'RETIRED' 'wednesday' 'PROVISIONAL' '3c33f5ae' \
         'claude-opus-5-5' 'Node v26.8.1' 'S101O' 'RD-830' 'RD-819' 'RD-820' 'F-794-1' 'PR #58' '#256-#259' 'db852b2'; do
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

# 86 — no live gate-25 session already exists.
for P in $(pane_pid_of "$ROUTE_NAME"); do
  if [ -n "$(claude_under "$P")" ]; then echo "REFUSING: a pane named $ROUTE_NAME (pid $P) already runs a claude — gate 25 is live; do not start a second session" >&2; exit 86; fi
  [ "$CHECK" = "1" ] || echo "NOTE: a pane named $ROUTE_NAME (pid $P) exists with no claude under it — the cockpit's own add decides" >&2
done

# 32 / 40 — LAST: the coordinator's stamp (SELF-CHECK line + note + every 'RULED: @STAMP@' slot, no placeholder), the READYs in briefs/ (not an override),
# and the answer route (Tuesday adds it, never this launcher).
STAMP_OK=1
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then STAMP_OK=0; fi
NSTAMP="$(grep -cF "$PH_STAMP" "$BRIEF")"
ROUTE_OK=1
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || ROUTE_OK=0
READY_OK=1
[ -z "${QA_READY_OVERRIDE_761:-}" ] && [ -z "${QA_READY_OVERRIDE_794:-}" ] || READY_OK=0
if [ "$STAMP_OK" = "0" ] || [ "$ROUTE_OK" = "0" ] || [ "$READY_OK" = "0" ]; then
  echo "guards pass (9 MODEL 40 6 7 8 18T 18 90 91 22 93 94 70 70N 31 39 10 17 11 12 13 14 15 20 41 82 19 24 53 71 76 77 78 79 81 38R 86); stamp, route and/or READY NOT complete." >&2
  echo "  ls-remote attempts this run: $LSR_ATTEMPTS (C-192); origin main ${M_ORIGIN:0:7}; RD-761 ${H761:0:7}; RD-794 ${H794:0:7}; lock tool ${INST_NOW:0:12}…; c57 ${C57_NOW:0:12}…; c133 ${C133_NOW:0:12}…; model $MODEL" >&2
  echo "  $SEAT_NOTE" >&2
  echo "  NEG seats (38R, derived live; coordinator pane '$COORD_NAME'):$NEG_DESC" >&2
  [ "$READY_OK" = "1" ] || echo "REFUSING (31R): a READY was read from QA_READY_OVERRIDE_761/_794 — copy both READYs into briefs/ and launch without the overrides" >&2
  [ "$STAMP_OK" = "1" ] || echo "REFUSING (32): $NSTAMP stamp placeholder(s) remain in the brief (the SELF-CHECK line, the Self-check note and the RULED: slots T1-T9) — the coordinator re-reads end-to-end and stamps them before launch" >&2
  if [ "$ROUTE_OK" = "0" ]; then
    echo "REFUSING (40): no '${ROUTE_NAME}|tuesday-agent@agentmail.to|no' line in $ROUTING — answers to the gate would have no route; Tuesday adds it at stamp (this launcher never writes it)" >&2; exit 40
  fi
  exit 32
fi

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  origin at $PIN_TS ($LSR_ATTEMPTS ls-remote attempt(s), C-192): main = c7ca0ed exactly; $B761 = ${H761:0:7}; $B794 = ${H794:0:7}; pull/58 ${P58:0:7} (18); T9 unmounted (18T)"
  echo "  lock tool 3c33f5ae… pinned, NEXUSAI_LOCK_BASE honoured, Laptop-DEV base present, no qa-g25 ticket (90); c57 1ae84a10… + c133 6f938bfc… pinned (91)"
  echo "  pin tables (40); chains (7, 8); gated + both-sides sets (22); premises (93); $SEAT_NOTE (94); rulings + answers (70); evidence + gate 24 instruments (31)"
  echo "  MODEL RULE (82); H-1 (76); H-4 (77); H-9 (78); H-7/H-8 (79); premises (81); route $ROUTE_NAME (40); report absent (17)"
  echo "  NEG seats (38R, derived live; coordinator pane '$COORD_NAME'):$NEG_DESC"
  echo "  model: $MODEL at exec (from models_latest.json)"
  echo "  SUBJECT: $SUBJECT"
  echo "  NEXUSAI_LOCK_BASE=$LOCK_BASE_LAPTOP  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  --check started no claude; nothing written."
  exit 0
fi

PROMPT="$PROMPT

VERIFIED BY THE LAUNCHER AT $PIN_TS (git ls-remote origin, read-only, $LSR_ATTEMPTS attempt(s) under C-192): refs/heads/main = $M_ORIGIN (exactly c7ca0ed); refs/heads/$B761 = $H761; refs/heads/$B794 = $H794; refs/pull/58/head = ${P58:-absent}. The T9 is unmounted. The installed lock tool $LOCKTOOL sha256 $INST_NOW equals the pin and NEXUSAI_LOCK_BASE=$LOCK_BASE_LAPTOP is exported in your environment. The C-57 runner sha256 $C57_NOW and the C-133 tool sha256 $C133_NOW equal their pins. Seat objects: $SEAT_NOTE. These are the start-of-gate pins; take your own three readings anyway.
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
