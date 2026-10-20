#!/bin/bash
# launch_qa_nexusai_gate29.sh — cross-project QA agent, ONE gate on Datasec/NexusAI (gate 29): a TIER-1 SECURITY GATE WITH A BROWSER LEG of
# RD-774 + RD-836 (risk-condition SQL only from fixed server templates; request SQL refused; stored sql_query never executed; admin-only
# risk-condition writers; PUT field allow-list; #272 log line through logSafe), draft PR #97 @ 115a775 (RE-PINNED 2026-10-21 from 278afc2; 2026-10-20 from 4c9b0d3) — one gated tree,
# one verdict, ONE report.
# (drafted 2026-10-19 from 16:27 AEDT by a read-only drafting agent for Tuesday; the drafter ran only bash -n on this file and the --check
# refusal path on a SCRATCH COPY whose briefs_staged greps were removed — see the DRAFTER-REPORT.)
# A FRESH gate on the Mac mini, /Volumes/Laptop-DEV; the T9 is UNMOUNTED, so the lock base is the Laptop-DEV locks-laptop-1017.
#   RD-774/836 rd-774-risk-sql-templates-s101o @ 115a775 (888203c -> 63bef65 build -> 360cd82 forward merge of 7700caf -> 4c9b0d3 #272 fix
#     -> 2566713 forward merge of 29c5ee8 -> e884516 RD-836 census build -> f1a2e76 forward merge of 39653db -> 278afc2 #273 test fix
#     -> 115a775 forward merge of d463f881, B349)
#   M0 = the MAIN pin Tuesday STAMPS (d463f881 at the re-pin = mode 0: the head already carries M0, nothing is merged; a moved M0 = T0 mode a/b).
#
# CHANGES, RE-PIN 2026-10-21 (278afc2 -> 115a775, B349's forward merge of main d463f881; pre-edit copy: launch_qa_nexusai_gate29.sh.pre-repin-115a775):
#   - head 278afc25 -> 115a775b6d5808629f493ef7a3f602d8c5853a22, tree ee819f21 -> 3cf0b847c581fddcf33ec0e3b0533584be06d3f4 (H774/T774); 278afc25 kept as H278/T278 (the previous head, 115a775's first parent).
#   - FLOOR_MAIN 39653db -> d463f8817fba925dee7e78c5216df3d5ea8ad073 (tree 704c442 -> 53d51c59698401237b1b1573fa942bf9f650b51d); 39653db kept as M3965/T3965 (f1a2e76's second parent);
#     PIN-HEADS RD774 base d463f881, count 7 -> 8; the MAIN-STAMP regex reads 'landed since d463f881'; d463f881 must be an ANCESTOR OF THE HEAD (mode 0 again).
#   - 7/8: the chain gains 115a775 (278afc2 + d463f881); 8 over d463f881, 35 over 888203c, 8 first-parent (were 7 / 21 / 7).
#   - 93: counts d463f881 4934/303 (blob a28458ad), head 115a775 4964/304 (blob c050e783), 278afc2 = f1a2e76 4910/303 (blob 57659c6c), 39653db 4880/302 (blob 2cc09485);
#     server.js blob 5fdf2912 -> b0148170 (the merged file); the other blob pins are unchanged (re-read at 115a775 and at d463f881).
#   - 31: READY_774 -> 2026-10-21_nexusai-gate29-READY-pr97-115a775.txt (B349's GATE 29 RE-PIN SHEET, verbatim), sha256 pinned; content greps: the head, 'PASS 4964/4964 across 304 suites', 'GATE 29 RE-PIN SHEET'.
#   - the PROMPT: the head, tree, eight-commit chain, 4964/304, mode-0 floor d463f881, READY file name.
#
# CHANGES, RE-PIN 2026-10-20 (4c9b0d3 -> 278afc2; matches the amended kit and its AMEND-REPORT section 4; pre-edit copy: launch_qa_nexusai_gate29.sh.pre-repin-278afc2):
#   - head 4c9b0d3 -> 278afc25dda22ed8511d33e3e1cd12b0afde3487, tree 26f5dd7e -> ee819f2126593465b352d91ae293fb3c55b9a75b (guards 40 PIN-HEADS, 18, 8).
#   - FLOOR_MAIN 7700caf -> 39653db4b56adb6d4e526c90531cd4cdf23022e0 (tree ba9581ab -> 704c442b78a36baea66fef2349a5acbdbff114b5); 7700caf kept as M7700 (360cd82's parent).
#     PIN-HEADS RD774 base 39653db, count 3 -> 7; the MAIN-STAMP regex reads 'landed since 39653db'; mode-0 stamp must say 'none'.
#   - 18M: 39653db must be an ANCESTOR OF THE HEAD (new, always); 39653db, 7700caf and 888203c in M0's ancestry; trees 704c442 / ba9581a / 428f042; none of the SEVEN
#     PR commits (278afc2 f1a2e76 e884516 2566713 4c9b0d3 360cd82 63bef65) on M0.
#   - 7/8: the chain is now 278afc2 <- f1a2e76 (e884516 + 39653db) <- e884516 <- 2566713 (4c9b0d3 + 29c5ee8) <- 4c9b0d3 <- 360cd82 (63bef65 + 7700caf) <- 63bef65 <- 888203c,
#     every parent list AND tree; 7 over 39653db, 21 over 888203c, 7 first-parent (were 3 / 5 / 3).
#   - 22: the 8 gated paths over 39653db (same 8 paths); 360cd82's counts-only merge-tree now over (888203c, 63bef65, 7700caf). The conflict sets of 2566713 / f1a2e76 are
#     NOT measured here (kit r1 measures them).
#   - 93: counts 4880/302 (39653db, blob 2cc09485), 4910/303 (head = f1a2e76, blob 57659c6c), 4676/292 (7700caf), 4700/293 (4c9b0d3), mode-a prediction M0 + 30/+1 (was +24/+1);
#     blob pins: server.js 05af86ce -> 5fdf2912eceb186066e8c297c5234540eeaba25c, rd774 test 3a62151e -> 0cfd42ee6fd1b8ae32c659f430cbcf9372e56321; simpleDb / validators /
#     riskSqlTemplates / spy / security-fixes / logSafe pins UNCHANGED (re-read at 278afc25); new equal-to-main pins: authEnforcement ca764a4b, jsonStorage, settings.js,
#     testing.js, testing.html. Anchors: the Settings route now carries requireRiskConditionAdmin (old form must be absent), the validate-condition save gate, 'logSafe(' on 24 lines.
#   - 31: READY_774 -> 2026-10-20_nexusai-gate29-READY-pr97-278afc2.txt, sha256 da8baec1ceda051af1e8ca083e8c697eb76440ebeece4c9c2fcb6860bc55ec06 (the builder's new-head mail,
#     saved verbatim); its content greps are the head, 'verify PASS 4910/4910 across 303 suites' and 'PR #97 new head 278afc2'. The kit does not yet NAME that sha256 (a FILL AT STAMP
#     item), so 'kit names the READY sha' is DEFERRED to the end (READY_NAMED, like 32S) instead of refusing at 31. ANSWER-26 and ANSWER-28 must exist.
#   - 12 / 14 / 10: 'THE LOG LINE' -> 'LOG SINKS' + 'THE NEW GATES' (the kit's r10 and T6 were renamed); the brief names the new trees / blobs in full and 2566713, e884516, f1a2e76, 29c5ee8 by short sha.
#   - the PROMPT: the head, tree, seven-commit chain, six routes, 23 log sinks, 4910/303, M1-M16, READY file name, gate 28 complete.
#
# LAUNCHED ONLY VIA: cockpit.sh add 'QA/NexusAI-gate29' "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate29.sh'"
#   (i.e. /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh). A tmux pane, NEVER nohup, never run it bare from a seat's shell.
#
# AUTHORITY: Tuesday's gate-29 drafting commission (2026-10-19) and her ANSWER-20/21/23/24 to S101O (tier 1; the plan and P1/P2 rulings; #272 in
# code; "Tuesday commissions a TIER-1 gate (gate 29 …). It launches when gate 28 frees the jest lock."); Kam's ruling C-211 (option (b)).
# THE MODEL RULE: Kam, live board 2026-09-30 09:07, card nexusai-gate11-opus55-safeguard-model-switch, option (b), PER SESSION. The MODEL is the
# kit's MODEL line, which must equal models_latest.json levels.opus.model_id (routing v1.0 row G1, Opus).
# Carried rulings (sqlite3 cached prebuild; full verifies UNBELTED; npm_config_update_notifier=false; ruling (b) + EXTENSION; C-190 + ADDENDUM;
# C-209; C-141 ADDENDA 6/7; the by-hand gate yield RETIRED; the load-8 rule; the Laptop-DEV lock base; gate 21's browser driver ruling (u)).
# FINDINGS-ONLY: never merges (outside its own store), never pushes, never opens/comments/approves/updates a PR, never dismisses an alert, never
# swaps or edits the lock tool, the C-57 runner or the C-133 tool; no fix, no deploy, no az, no docker, no model call, no demo, no human.
#
# PATTERN: launch_qa_nexusai_gate28.sh (prompt EMBEDDED, --check mode, PIN-table parser, MAIN-STAMP line, C-192 lsr retry, lock/runner/C-133 pins
# 90/91, carried rulings 70, MODEL RULE 82, H-rule fragments 76-79, the LIVE negative-control seat derivation 38R, guard 86, stamp + route guards
# LAST) and launch_qa_nexusai_gate27.sh (the browser leg: Chrome + Playwright presence 96, lockver). CHANGES, each deliberate:
#   - 40: TWO pin rows (MAIN stamped + RD774); no MERGE-PINS table (mode 0 merges nothing; mode a's merge is the gate's own rebuild).
#   - 18M: 888203c and 7700caf in M0's ANCESTRY (is-ancestor, never --first-parent); M0's tree = the stamped tree; 4c9b0d3 NOT on M0; mode 0 iff
#     M0 = 7700caf (then 'landed since 7700caf' must be none); else mode a/b and the legacy merge-tree of the head onto M0 must show conflict
#     markers in the counts file ONLY (or none).
#   - 7/8: the head chain 888203c -> 63bef65 -> 360cd82 (parents 63bef65 + 7700caf) -> 4c9b0d3 with every tree.
#   - 22: the 8 gated paths over 7700caf; no static/ or templates/ path; 360cd82's forward merge is counts-only (legacy merge-tree).
#   - 93: counts + predictions (mode 0: 4700/293; moved M0: M0 + 24/+1, recomputed in-guard); the head's blob pins; the RD-774/836 anchors; the
#         sibling-writer premise (T6); the builder's plant is not a UNION (WRONG 6); the seed's single created_at (WRONG 10).
#   - 33L (new, deferred like 32S): REFUSES while the Laptop-DEV jest lock's holder or any queued ticket is gate 28's (qa-g28-*).
#   - 31: ONE READY copy, sha256 PINNED; instruments from gate 27's (COMPLETE) inst/, gate 25's, gate 26's c57 shim; gate 28's inst/ is never read.
#   - REPORT path from the kit's §11 Report line (its date is a stamped slot); refuses if the report exists.
#   - the NOT TESTED line is READ from the kit (one line) and appended to the prompt verbatim at exec.
#
# Identity: exports NexusAI's OWN az/gh dirs (az is NOT used; gh READ-ONLY); CLAUDE_CONFIG_DIR pinned to Tuesday's store.
# --check is READ-ONLY in NexusAI: git read verbs with --no-optional-locks (cat-file, log, merge-base, diff, show, rev-parse, ls-remote, rev-list,
# ls-tree, grep) and the legacy stdout-only merge-tree (no object written); shasum / bash -n / grep over session-tools files; python over `git show`
# output; ls, ps, tmux list-panes, test -e, defaults read (Chrome's version). Writes nothing.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate29.sh [--check]
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
BRIEF="$BRIEFS/2026-10-19_nexusai-gate29-rd774-rd836.md"
BRIEF22="$BRIEFS/2026-10-13_nexusai-gate-batch22.md"
BRIEF23="$BRIEFS/2026-10-16_nexusai-gate-batch23.md"
BRIEF24="$BRIEFS/2026-10-17_nexusai-gate24-rd848.md"
BRIEF25="$BRIEFS/2026-10-18_nexusai-gate25-rd761-rd794-merged.md"
BRIEF26="$BRIEFS/2026-10-18_nexusai-gate26-c170-be0fe37-merged.md"
BRIEF27="$BRIEFS/2026-10-18_nexusai-gate27-rd778-xss.md"
TEMPLATE="$TUE/2_Project_Files/fleet/qa-agent/BRIEF_TEMPLATE.md"
ADD25="$TBRIEFS/2026-10-18_gate25_ADDENDUM-1_ref-order.md"
READY_774="$BRIEFS/2026-10-21_nexusai-gate29-READY-pr97-115a775.txt";   READY_774_SHA='3debfc2741335c2ff8819a5d2e5a2a9b3dd308e949d05adb3e5ea0e836abb2c5'
ANS1="$TBRIEFS/2026-10-18_S101O_ANSWER-1_plan-confirmation.md"
ANS20="$TBRIEFS/2026-10-19_S101O_ANSWER-20_next-rd774-rd836.md"
ANS21="$TBRIEFS/2026-10-19_S101O_ANSWER-21_rd774-plan-confirmed.md"
ANS23="$TBRIEFS/2026-10-19_S101O_ANSWER-23_pr97-alert272-fix-before-ready.md"
ANS24="$TBRIEFS/2026-10-19_S101O_ANSWER-24_pr97-ready-received-gate29.md"
ANS26="$TBRIEFS/2026-10-19_S101O_ANSWER-26_rd836-other-writers-before-gate29.md"
ANS28="$TBRIEFS/2026-10-20_S101O_ANSWER-28_pr97-codeql-273.md"
CHARTER="$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"
MODELS_JSON="$TUE/0_Brain/dashboard/data/models_latest.json"
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
B25_INST="$RPTS/2026-10-18-gate25-rd761-rd794-merged/evidence/inst"
B26_INST="$RPTS/2026-10-18-gate26-c170-be0fe37-merged/evidence/inst"
B27_DIR="$RPTS/2026-10-18-gate27-rd778"
B27_REPORT="$B27_DIR/report.md"
B27_INST="$B27_DIR/evidence/inst"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"
ROUTE_NAME='QA/NexusAI-gate29'
NPM_CACHE="${HOME}/.npm/_cacache"
PREBUILD="${HOME}/.npm/_prebuilds/0068db-sqlite3-v5.1.7-napi-v6-darwin-arm64.tar.gz"
PREBUILD_SHA='84a34404b12ff212adbca70eff76c2e4dd83b91245eed0b4569438f928567afc'
CHROME_APP='/Applications/Google Chrome.app'
PW_CACHE="${HOME}/Library/Caches/ms-playwright"

# ---- the pins (cross-checked against the brief's PIN-HEADS, guard 40; each MEASURED 2026-10-19 16:28-16:33 AEDT)
FLOOR_MAIN='d463f8817fba925dee7e78c5216df3d5ea8ad073'; FLOOR_TREE='53d51c59698401237b1b1573fa942bf9f650b51d'   # main at the RE-PIN 2026-10-21 (RD-863 and PR #98 landed; the head's base, mode 0)
M3965='39653db4b56adb6d4e526c90531cd4cdf23022e0'; T3965='704c442b78a36baea66fef2349a5acbdbff114b5'            # the previous floor (main at the 2026-10-20 re-pin, C-170 landed): f1a2e76's second parent
M7700='7700cafd33ca8a329e1e7905081d869e83c6ccb5'; T7700='ba9581ab6d779e867edc066895f8481e5580691a'            # the OLD floor (main at drafting, RD-778 landed): 360cd82's second parent
L888='888203c8c50e13938ca557e8aa0f1faf2101ff31'; T888='428f042b34fb1729d8fd45a112a1220af0fdae6a'            # the branch's base (RD-794 forward-merged)
B774='rd-774-risk-sql-templates-s101o'
H774='115a775b6d5808629f493ef7a3f602d8c5853a22'; T774='3cf0b847c581fddcf33ec0e3b0533584be06d3f4'            # the head (B349's forward merge of main d463f881 into 278afc2; parents 278afc2 then d463f881)
H278='278afc25dda22ed8511d33e3e1cd12b0afde3487'; T278='ee819f2126593465b352d91ae293fb3c55b9a75b'            # the PREVIOUS gated head (test-only fix for CodeQL #273)
MF1A='f1a2e762215baf2ebf79b588747eaeff6c6af342'; TF1A='5c80bbcf1abc678a08fc6b51bd067d51111c59ee'            # forward merge of main 39653db (parents e884516 then 39653db)
E884='e884516b719c1d6f37b377bd553cbcd1b9dd97c7'; TE884='3571969baa7bc2fdbec8364a26750fc1ebd4618f'           # the RD-836 census build (gates on settings POST + validate-condition save; 23 logSafe lines)
M256='25667136c22d308823f9e71e1295bc5e886decf6'; T256='f5322b49a61c5269a0b4f9fbd194b72c27a68bfe'            # forward merge of main 29c5ee8 (parents 4c9b0d3 then 29c5ee8)
M29='29c5ee8f5fe42ec37b08c86ea5db20e8018182ab'                                                               # main commit merged by 2566713 (second parent)
H4C9='4c9b0d36993f1e78c8f23cd9e1216200550324b8'; T4C9='26f5dd7e632649c2ef33a97a5a73de1cf908975f'            # the PREVIOUS gated head (#272 fix)
M360='360cd82444d7496dcacb7db7055b4afcec42869d'; T360='a02a8755169852fbadc28f89134ad290188f2299'            # forward merge of 7700caf (branch first)
B63='63bef65c53fc155989c5bd9504a09787293a9214';  T63='2b20a25ea25fecc869321444c6f91758bc348d30'             # the build on 888203c

COUNTS_FILE='scripts/verify-expected-counts.json'
CB_FLOOR='a28458adef1e24416865a425201dc4bc840f9f30'   # d463f881, 4934/303
CB_3965='2cc094855c1215299ac15373262241dd71c64bff'    # 39653db, 4880/302
CB_7700='c136311879eaa6ad48e0b3aa10fcef0ce765fe98'    # 7700caf, 4676/292
CB_4C9='ff5f5d7ed77a57343f73875269412617b1592e37'     # 4c9b0d3, 4700/293
CB_HEAD='c050e78328616b96862512739e8cffc6b4a6e603'    # 115a775, 4964/304 (regenerated once on the merged tree by B349)
CB_278='57659c6cfc51d7ddffeb3e8ed31f1b7db4ef901c'     # 278afc2 (= f1a2e76), 4910/303
CB_360='7436f51c1d0c8f3b39da13db1e84c41be99a0d93'     # 360cd82
PKG='package.json'; PKG_BLOB='384805d9e286718bb34ffd05be01c62c00806cf5'
LOCK='package-lock.json'; LOCK_BLOB='19477a9329f17e529c208d91d172b95b47fc1bb5'
DEPLOY_WF='.github/workflows/deploy-demo.yml'; DEPLOY_BLOB='953b2a2f84e8710bea857ec87c6f00faa50fa56b'
SERVER='backend/server.js';                    SERVER_BLOB='b01481701d954eee4f07959ad115846876d7d5de'
SIMPLEDB='backend/simpleDb.js';                SIMPLEDB_BLOB='5891c809eafeb32b01d9f4f80746383b8f4ac200'
VALIDATORS='backend/validators.js';            VALIDATORS_BLOB='7657ce843bc17632889a70a32a4516f7c395cd39'
TEMPLATES='backend/services/riskSqlTemplates.js'; TEMPLATES_BLOB='1ba37db02b31558a646cf58fb2af5982d2c4ba54'
LOGSAFE='backend/logSafe.js';                  LOGSAFE_BLOB='edfb81f8df49dbde5ddaa7e15b06bb158871344d'
T774FILE='__tests__/rd774-risk-sql-templates.test.js'; T774FILE_BLOB='0cfd42ee6fd1b8ae32c659f430cbcf9372e56321'
AUTHENF='backend/services/authEnforcement.js'; AUTHENF_BLOB='ca764a4b2c1f0349cf5891d71559d693c1104ec7'          # = main's (the gate's own machinery)
EQMAIN_PINS='backend/jsonStorage.js 2abb5cf487d75f2ce1730a028ade1b39cde31fd2 static/js/settings.js adaa34004dea127beb216da1eb21813ccb0ab217 static/js/testing.js 2b8af34fa7bdc7c4f6f47d83aefce1fe22c8c04a static/testing.html 376bfee891372ea14692c9a1c4efaff2f30be350'   # equal at the head AND at main d463f881
SPY='__tests__/helpers/rd774-sql-spy-preload.js'; SPY_BLOB='78c21dfa0dacddaef8d6b0855cc9404d57121380'
SECFIX='__tests__/security-fixes.test.js';     SECFIX_BLOB='e47f3545b0cd0a69eb9dedabf840fe31f18e79ef'
GATED_774='__tests__/helpers/rd774-sql-spy-preload.js __tests__/rd774-risk-sql-templates.test.js __tests__/security-fixes.test.js backend/server.js backend/services/riskSqlTemplates.js backend/simpleDb.js backend/validators.js scripts/verify-expected-counts.json'
NEG_SEATS=''   # 38R: DERIVED at launch from the live cockpit panes — never stamped by hand

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — gate 29'
QUESTION_SUBJ='[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>'
STATUS_SUBJ='[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch'
PARK_LINE='PARKED: flagged — awaiting the Opus 4.8 switch'
ANSWER_PREFIX='[Tuesday -> QA/NexusAI-gate29] ANSWER'
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
lockver() { g cat-file -p "$1" 2>/dev/null | python3 -c 'import json,sys; print(json.load(sys.stdin)["packages"].get("node_modules/"+sys.argv[1],{}).get("version",""))' "$2" 2>/dev/null; }
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

You are the fleet QA/testing agent running ONE gate on Datasec/NexusAI, gate 29: a TIER-1 SECURITY GATE WITH A BROWSER LEG, ONE verdict and ONE report. It is a FRESH gate on Kam's Mac mini, working volume /Volumes/Laptop-DEV; the T9 drive is UNMOUNTED, so the project's jest lock lives on this drive's locks-laptop-1017 base. The item: RD-774 + RD-836, rd-774-risk-sql-templates-s101o at 115a775b6d5808629f493ef7a3f602d8c5853a22 (tree 3cf0b847c581fddcf33ec0e3b0533584be06d3f4), draft PR #97 by NexusAI-O (S101O), RE-PINNED 2026-10-21 from 278afc2 (2026-10-20 from 4c9b0d3): eight own commits on the first-parent line over 888203c8c50e13938ca557e8aa0f1faf2101ff31 (35 in 888203c..head; 8 over main d463f8817fba925dee7e78c5216df3d5ea8ad073) — 63bef65c53fc155989c5bd9504a09787293a9214 (the build), 360cd82444d7496dcacb7db7055b4afcec42869d (the forward merge of main 7700cafd33ca8a329e1e7905081d869e83c6ccb5), 4c9b0d3 (the #272 log fix; the previous head), 2566713 (the forward merge of main 29c5ee8), e884516 (the RD-836 census build: the admin gate on POST /api/settings/risk-definitions and on POST /api/validate-condition when it saves; 23 risk-condition log lines through logSafe), f1a2e76 (the forward merge of main 39653db, C-170), 278afc2 (a test-only fix for CodeQL #273; the previous head) and 115a775 (B349's forward merge of main d463f881: RD-863, PR #98's test-code set and the HISTORY.md entry; the counts file regenerated once on the merged tree, 4964/304). It moves risk-condition SQL into FIXED server templates chosen and parameterised from the condition text (Kam's ruling C-211, option (b)), refuses SQL text in any request with 400 SQL_TEXT_NOT_ACCEPTED, never executes the stored sql_query column again, puts the setup-mode-aware admin gate on POST, PUT and DELETE of /api/risk-conditions, on POST /api/risk-conditions/sync and (since e884516) on POST /api/settings/risk-definitions and on POST /api/validate-condition when it saves (RD-836: six routes), limits PUT to four fields (400 FIELD_NOT_ACCEPTED), and routes the risk-condition log lines (23, including the one CodeQL #272 named) through the repo's logSafe helper. M0 is the main Tuesday STAMPED (the launcher verified origin main equals it; sha, tree and the T0 mode are at the end of this prompt): in mode 0 (M0 = d463f881) the gated tree IS the head, because the head already carries M0; if main moved, T0 rules the mode. Never trust the builder's trees, logs, cells, spy, characterisation file or census as the proof. FINDINGS-ONLY: you NEVER merge anything the fleet can see, NEVER push, NEVER open, comment on, approve, un-draft or merge a pull request, never comment on Jira, never dismiss an alert, and NEVER swap, copy over or edit the installed lock tool, the C-57 runner or the C-133 tool; no fixes, no deploys, no az, no docker, no model call of any kind, no production, no HTTP to any production or demo host, nothing to Partner Center, the demo or any human, no host npm registry. One client only: Datasec/NexusAI.

READ YOUR COMMISSION FIRST, whole: /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-19_nexusai-gate29-rd774-rd836.md
It opens with the item, the READY copy, Tuesday's rulings, THE RE-PIN STEP, the stamp lines, PIN-HEADS, the TIER argument, the legitimate shapes of the two checkers (the admin gate and the SQL refusal), the drafter's WRONG OR UNVERIFIED list (each item MEASURED or READ-ONLY-INFERRED), then TUESDAY'S RULINGS (T0 to T10 as Tuesday stamped them, the commission's nine properties, the carried rulings) and THE MODEL RULE: apply them, do not re-rule them. Then the charter it names; the READY copy in briefs/ (2026-10-21_nexusai-gate29-READY-pr97-115a775.txt, B349's GATE 29 RE-PIN SHEET, verbatim), read WHOLE; Tuesday's ANSWER-20, -21, -23, -24, -26 and -28 to S101O; the clarifications the brief quotes, at source (C-211, C-01, C-02, C-203 and the rest); gate 25's ADDENDUM-1 (the ref order); gates 22 to 27's section 3a (the H-rules, carried by reference; gate 27's browser rule); gate 27's report on THIS drive (COMPLETE; its browser instruments and its safeguards park are your precedent). Every builder statement is a CLAIM — RELAYED, never evidence. The brief's section 2a rows (r0 to r14, r7S, r12b, b1 to b3), section 2b (how the browser leg runs) and section 3b (the sweep) are required measurement.

THE MODEL RULE (Kam, live board 2026-09-30 09:07, card (b)): QA gates may switch to Opus 4.8 when flagged by the running model's safeguards, PER SESSION. You start on the model named at the end of this prompt (Opus 5.5). You run the FULL rows. If one of your responses is stopped by the safeguards: that step is NOT RUN (never re-worded to slip past); write ONE line to evidence/classifier-stops.txt; let any running step finish and let the hold exit so you never sit holding a lock (H-28); mail tuesday-agent@agentmail.to with the subject exactly "[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch"; then end your turn with the line "PARKED: flagged — awaiting the Opus 4.8 switch" and wait. Tuesday switches THIS pane's model to Opus 4.8 and taps you by mail. You never answer the model dialog yourself, and nobody ever chooses "Switch automatically". After the switch, resume at the stopped row. The report states which rows ran on which model, with the switch time, and quotes classifier-stops.txt whole. It is likely to bite while composing the SQL-shaped plants (T3): use exactly the inert, marker-only shapes T3 names; never compose a statement that writes, drops or deletes.

THE PROPERTIES (brief section 2a). (1) NO REQUEST PATH PLANTS OR RUNS SQL: r2 THE SQL-PATH CENSUS by grep of the WHOLE backend (not the builder's list: the drafter found writers the READY does not name — the Settings page's risk-definitions sync, validate-condition's save, the GET auto-sync — and the run-now entry to the scheduler's executor; the builder's own 11-row census is a CLAIM: rows 5 and 6 IN scope and gated, rows 7 to 11 out per RD-868); r3 every request writer attacked with SQL-bearing bodies (spellings, case variants, nested, urlencoded, prototype keys); r4 stored legacy rows with a marker SELECT, a UNION over sqlite_master, UNION ALL, PRAGMA, ATTACH to a path you own, chained and comment forms, executed by EVERY executor (the level lists, red-flag, the per-rule execute with limits 1, 50, 10000 and none, and the scheduler per T7), read from YOUR OWN SQL spy (it also wraps sqlite3 Statement methods and records bound params; prove it with a planted call), with the BASE (M0) arms as the firing control. Note: the builder's "planted UNION" is a marker SELECT, not a UNION. (2) THE TEMPLATE DERIVATION r5: a differential of the head's template builder against main's generator over your OWN corpus of at least 200 condition texts (boundaries, caps, non-ASCII digits, the 500-character check on the sanitised text, injection characters), every DIFF matched to a documented READY change or reported; template ids never client-controlled, ARITY by hand count, prototype ids refused, params and limits clamped before sqlite, type confusion through PUT and risk-definitions. (3) RD-836's ADMIN-GATE MATRIX r7: states S1 open first run (C-01), S2 the RD-437 state (C-203 (b): intended to pass), S3 configured, S4 sign-in unproven; roles anonymous, viewer, admin; the six gated routes (POST, PUT, DELETE and sync of /api/risk-conditions; POST /api/settings/risk-definitions; POST /api/validate-condition with a save, open without one) plus unchanged reader columns; BASE, BRANCH and the pre-gate tree 2566713 as a second positive control; the store's sha256 before and after every cell; and r7S the new gates as T6 rules. (4) THE PUT ALLOW-LIST r8 incl. id, created_by, kql_query, sql_query, prototype keys and hostile values of the allowed keys. (5) THE LOG SINKS r10 (#272 and e884516's 23 risk-condition log lines, 24 logSafe call lines): CR/LF forging driven from the REALISTIC HTTP sources (PUT, the Settings writer and validate-condition) plus the red-proof M9; CodeQL r11 re-read at source: analyses at 115a775, 0 open on refs/pull/97/head, the instances of #272 and #273 fixed, the 360cd82 and f1a2e76 results-1 analyses as the firing controls, #70, #220 and #221 OPEN on main and expected fixed only after the land, ten more main log-injection alerts on lines the head no longer has (#172 and nine others) read as NOTEs — NOT claimed (C-209). (6) THE CHARACTERISATION T0 to T12 r6, re-derived against YOUR hand-written references written before you read the builder's, on the substrates T2 rules: the demo seed stamps ONE created_at, so T5, T6, T9 and T10 cannot fail on it — use the spread-date copy; at least T5, T9 and two others. (7) THE FULL VERIFY r12 under the jest lock: 4964/4964 across 304 suites in mode 0; names as SETS: LOST is exactly the 13 F-10 grammar names RD-774 itself rewrote (a branch-side rewrite, NOT a C-215 rename), each mapped to its replacement; mode (a) adds r12b, C-57 through a byte-identical COPY of the installed runner with C57_ROOT pointing at your own shim. (8) THE BROWSER LEG b1 to b3, Chrome headless via Playwright 1.62.1 from your tree's own node_modules (ruling u): Settings > Risk rules add, toggle, edit, delete as admin and viewer; the dashboard execute-rule and level panels; testing.html's SQL box giving 400 — on a local run of THIS commit, captioned "local run of <sha>, <open|configured> mode — NOT the demo". (9) PRIOR WORK r14: the builder's census (a241d25's F-10 grammar; three planting paths; three executors) checked, every READY claim VERIFIED, FALSE or UNVERIFIED. Red-proof mutants r9 for every key guard (M1 to M16, M12 and the new M13 to M16 included), each landed, restored byte-equal to the head blob, a mutant no cell kills named.

MAIN MUST NOT MOVE (ruling b): the launcher verified origin main equals the stamped MAIN pin exactly, that 888203c, 7700caf, 39653db and d463f881 are in its ancestry, that d463f881 is an ancestor of the head, that its tree equals the stamped tree, and that the head is not on it; take M0 by git ls-remote at YOUR start and say so. If main moves mid-gate (S101O's next landings, RD-863 first, are the likeliest movers; gate 28's RELEASEs and C-170 have already landed), the gated tree is stale: name what landed, finish nothing that would read as a verdict on the new main, and mail a QUESTION (C-68). GitHub SSH intermittently denies auth (C-192): retry every ls-remote up to 5 times about 10 s apart; a FAILED ls-remote is UNKNOWN, never a value. Re-hash the lock tool, the C-57 runner and the C-133 tool at start, mid and end.

C-190 + its ADDENDUM — BOTH thresholds block: every merge to main goes through a pull request that adds no new high-or-higher CodeQL alert in changed code (test code included), AND any new alert whose RULE severity is error blocks whatever its security severity. Alerts are fixed in code, never dismissed. C-209: a PR's CodeQL run cannot show a pre-existing main alert as fixed. CodeQL is NOT RUN by this gate on any tree — say so. C-185 (ruling h): read its known set at source; any other failure is by NAME; no re-run is a clearance.

THE LOCK (C-63). The installed tool is session-tools/nexusai-lock.sh in the NexusAI project on this drive, sha256 3c33f5ae58e1be20282467a90b27a23a2de998eedd0e56c03f3c06360031a792. While the T9 is unmounted the base is NEXUSAI_LOCK_BASE=/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/session-tools/locks-laptop-1017, which the launcher has EXPORTED into your environment: keep it on every jest step and every server boot, quote the c57 runner's resolved LOCK_BASE= and ROOT= line (mode a), and never touch this drive's stale session-tools/locks (a 2026-09-22 holder lives there). If the T9 mounts mid-gate, finish the running hold, file nothing more, and mail a QUESTION. EVERY jest run, every booted server and every browser arm goes in the jest lock, each hold tagged qa-g29- (no tag of yours contains the word "merge": C-141 ADDENDUM 7), ONE hold at a time. Gate 28 is complete and released this lock; if a qa-g28- ticket reappears, wait behind it FIFO and never touch it. S101O's own s101o- holds are FIFO ahead of you. MERGES GO FIRST and RULING (i)'s BY-HAND GATE YIELD IS RETIRED: if a ticket is queued ahead of you, wait behind it (FIFO) — the builder S101O files jest holds on the same base. AT A WAIT DEADLINE: --replace on your own still-waiting ticket BEFORE its deadline fires (C-141: a SAME-PLACE handover), confirmed from the queue listing (the old ticket to released/ as ticket-left-*, your place unchanged); a duplicate-tag refusal takes a -r<N> suffix. Read queue-jest at start, around every hold and at end; any qa-g29- entry that is not your current hold is a STOP. Read your inbox before filing every new hold. THE LOAD RULE: file a hold, start any full jest, any server boot or any browser arm only below a 1-minute load of 8 (8 cores; Tuesday's ANSWER-1 to S101O); record uptime beside each.

NODE_MODULES WITHOUT THE HOST REGISTRY (ruling m, H-31): offline npm ci --offline --ignore-scripts --no-audit --no-fund with --cache pointing at an APFS clone of the local npm cache on the same volume; M0 and the gated tree share lock 19477a9, so ONE proven install is APFS-cloned into the others; EVERY npm invocation carries npm_config_update_notifier=false (prove the cache copy's _update-notifier-last-checked marker absent or unchanged); an ENOTCACHED is NOT RUN, named, with a QUESTION — never go online from the host, never npm install, never npx playwright install (Playwright downloads no browser; Chrome is the local install). sqlite3's binding from the cached prebuild (an APFS clone of ~/.npm/_prebuilds), inside the strict belt, IS PART OF H-31, with its three conditions (the tarball's and the unpacked node_sqlite3.node's sha256; CI builds its own Linux binding; every row that boots a server names "sqlite3 binding: cached prebuild, offline"). proxy-addr must resolve 2.0.8 and playwright 1.62.1 from each tree's own path (RD-827, C-205).

THE FULL VERIFY (r12) through the jest lock, UNBELTED by Tuesday's 2026-10-05 answer to gate 14 (ruling n), with its four conditions. SESSION_SECRET UNSET in the host shell, npm_config_update_notifier=false npm run verify -- --maxWorkers=2 --forceExit (prove the flag reached jest), on this machine's Node as T9 rules. RULING (b) and its EXTENSION (ruling o): if a verify stays lock-starved about 2 h after filing, deliver it NAMED NOT RUN — never "skipped" — with the brief's coverage sentence in NOT TESTED. The census, planting, derivation, admin-matrix, red-proof and browser rows are NOT covered by that extension: a TIER-1 verdict whose census (r2), planting (r3, r4), derivation (r5), admin-matrix (r7), red-proof (r9) or browser (b1 to b3) rows did not run is PROVISIONAL and releases nothing. A revert, plant or mutant counts only if it LANDED (the exact text present, the original absent) and parses; a red from a mutant that never landed is a VOID arm, a planted control that does not fire makes its row VOID (never a pass), and an edit whose anchor is absent fails loudly and nothing downstream runs on that tree.

THE INSTRUMENT RULES H-1 TO H-36 (brief section 3a; gates 22 to 27's section 3a read WHOLE). H-1: the ONLY SESSION_SECRET printer is the one the brief quotes; self-test it and gate 27's scan; a booted child server's per-boot secret (T5) is generated and passed in-process, never echoed or logged. H-3: a LANDING CONTROL for every plant, revert, mutant, stored row and browser action. H-4: the HEARTBEAT is a separate child of the hold wrapper, aborted if absent 90 s after the grant, max gap reported. H-6: every path with a space quoted; every host jest run but the full verify, every driver and every booted server under your copy of the belt with its landing control. H-9: byte plants (CR, LF, ESC, NUL) by Buffer, checked with xxd. H-11/H-18: /bin/bash explicitly, "${sha}:${path}" quoted (zsh eats :s and :a). H-14: every driver ends END ok or END VOID with a reason. H-17: censuses by pgrep, never ps. H-20: a per-step hard DEADLINE on every jest run (with --forceExit), every runner invocation, every npm ci, every server boot and every browser arm (qa-to.sh). H-21: every file you mutate is restored by a trap on EXIT (also INT and TERM) installed BEFORE the first mutation, hash-compared to its pin (the head blobs the brief lists). H-22: never nest sandbox-exec (it exits 71). H-24: jest array options after the paths, lists built in bash. H-26: C-192 retries. H-27: THE MODEL RULE. H-28: ONE focused hold at a time, at most about 40 minutes planned (T1's runner hold excepted), rows GROUPED, a hold that would overrun SPLIT, every part file bash -n checked before filing; you stay in the FOREGROUND — a hold that must outlive one tool call runs as a TRACKED child of your session (never nohup) with its timeout at the 2-hour maximum; each hold carries a wait deadline and you --replace before it fires. H-29: other gates' and the builder's evidence is method only. H-31: offline host node_modules. H-32: every booted server is a local run of your tree on loopback by the gate — NOT the demo; the browser opens only 127.0.0.1 (plus T4's pinned CDN URLs if ruled); no HTTP to any production or demo host. H-33: never rm — quarantine (T1's disclosed runner exception only); every child reaped by pid. H-34: the Laptop-DEV lock base. H-35: NO docker object and NO az command, not even az version, and NO call to any real model, Azure OpenAI or Log Analytics endpoint — validate-condition's AI branch is not driven. H-36: the socket ledger on every booted server, its landing control first.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT (fresh mktemp dirs under projects/nexusai/qa-trees/gate29.* in /Volumes/Laptop-DEV/!CODING/Testing Agent MAIN): ONE --mirror clone of the NexusAI repo on THIS drive as your store, your refs g29/* in it made BEFORE origin is removed (gate 25 ADDENDUM-1), any merge commit of yours in it, every work tree a clone of that store, status-checked before use, EXCLUSIVE to one purpose. NEVER work in the NexusAI root checkout or any worktrees/ folder (LIVE, the builder's). In the NexusAI repo use ONLY read verbs (show, diff, log with an explicit rev, ls-tree, cat-file, grep, ls-remote, rev-parse, merge-base, rev-list, count-objects, for-each-ref); NEVER fetch, pull, push, checkout, worktree, commit, stash, gc, merge, merge-tree --write-tree or hash-object -w there. Copy instruments BY NAME from gate 27's evidence/inst (COMPLETE), gate 25's evidence/inst and gate 26's c57 shim on THIS drive (never the whole directory; never gate 28's, which is LIVE), re-point every gate-27 path in your copies to gate 29 — INCLUDING the lock base line (quote that diff) — and correct the floor library's ROOT and NEG defaults from the live list below; never write into another gate's dirs. Never write into the builder's session-tools (S101O is live in s101/: hash it at start and end); never run the seat's scripts in place (characterise.js and hold-rd774-red.sh are method only). Findings-only: never push, no commits outside your store, no tickets, no PRs, no edits in NexusAI. No Microsoft, Log Analytics or login host, no mail host (T7's .invalid mail dial is refused by the belt), no demo, no Partner Center, no workflow dispatch, no repo variable written. No mail to any human. Never rm: quarantine.

FLOOR DISCIPLINE — section 9 of the brief exactly. Do ALL lock-free work first (pins, hashes, reads, r0, r1, r2, r5's in-process differential, r11, r13, r14, the offline npm ci, the spy, belt and ledger self-tests); then file your holds one at a time through your COPY of gate 27's qa-file27.sh re-pointed to qa-g29 tags and the jest kind (the suggested grouping is H1 to H6 and C1 in section 3a). QUEUE, NEVER TAKE OVER: never signal, move or edit another seat's or gate's process, lock, ticket or worktree. Count foreign servers the C-125 way anchored on YOUR OWN claude pid, with the negative-control seats the launcher derived (listed at the end of this prompt) classifying foreign in the same run; re-derive them at every hold's start; a hold with no live negative control aborts. A zero is reportable only beside a control that fired in the same window. DEADLINE AND HEARTBEAT: every step has a per-step DEADLINE, every child is killed in a finally by pid from your own ancestry (C-174, never by pattern), a HEARTBEAT line at least every 2 minutes during a hold, and a step with no heartbeat for 5 minutes is aborted and reported; every booted server and Chrome stopped by its own pid and its port read free afterwards.

RE-PIN at start, mid and end: main and rd-774-risk-sql-templates-s101o, refs/pull/97/head, plus the three tools' sha256 — three timestamped readings with the branch name and attempt count beside each sha. A head that disagrees with the brief is a FINDING and a reason to stop, never a typo to fix. Call main at your start M0 and say so. Count the NexusAI .git/objects files and their newest mtime at start and end and account for any delta (the drafter read 90 files at 16:3x AEDT on 2026-10-19).

QUESTIONS: your routing name is QA/NexusAI-gate29. If you must ask, mail tuesday-agent@agentmail.to with subject "[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>" and PROCEED ON THE SAFEST READING without waiting (the one exception is a safeguards stop, which PARKS you under THE MODEL RULE); Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/NexusAI-gate29] ANSWER". Approval-class items (anything Azure, any real model call, the demo, Partner Center, money, a human, the live lock tool) are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your ONE report to the path the launcher names at the end of this prompt (the brief's section 11). Write its VERDICT and FINDINGS table early and keep it current. Findings are G29-<n>, notes N29-<n>, each naming its instrument and evidence class.

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with the subject exactly:
[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — gate 29
Lead the body with the TWO lines in the form the brief's section 11 gives — the RD-774+RD-836 verdict line and the LANDING CHECKLIST line — then one line naming M0 and END main, the C-102 sweep, which rows ran on which model, which holds ran and which are NAMED NOT RUN under ruling (o) extended, and "CodeQL NOT RUN by this gate on any tree". The report's last two lines are those same two lines. Never wednesday-agent@. You have no inbox that wakes you, so a verdict you do not mail is lost.
The AgentMail key is AGENTMAIL_API_KEY in /Volumes/Laptop-DEV/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no 4_Credentials directory of its own. Never put the key, a token, a session value or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice — the only turn you end while waiting is the PARKED line of THE MODEL RULE.

Rule 2 stands: what you did NOT test is first-class output — a NOT TESTED section carrying the builder's stated limits, every declared limit L-B1 to L-B9 and L-Y1 discharged with a measurement or left standing and named (C-112), Prior work checked (C-49), every finding naming its instrument, and every action recommendation labelled MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. The tester never fixes. C-211, C-01, C-02, C-203, C-178, C-190 with its ADDENDUM, C-209, C-57, C-133, C-185 with its ADDENDA, C-192, C-205, C-141 with ADDENDA 6 and 7, C-63, C-40, C-68, C-76, C-102, C-112 and C-174 are the clarifications this gate leans on; C-49, C-89, C-115, C-125, C-130 and C-131 are carried. That section must carry, verbatim, the NOT TESTED line the launcher appends at the end of this prompt (it is the brief's section 11 line).
PROMPT_EOF

# ---------------------------------------------------------------- GUARDS
[ -d "$QA_DIR" ]  || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]   || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -n "$PROMPT" ]  || { echo "embedded prompt is empty" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }

STAMP_OK=1          # cleared below by any unstamped slot the guards meet; the refusal itself is LAST (32S)
LOCK_OK=1           # cleared below while gate 28 still holds or queues on the jest lock; the refusal itself is LAST (33L)
PROVISIONAL=''      # what --check ran against provisionally while a slot was unstamped

# 9 / MODEL — the kit's MODEL line must equal models_latest.json levels.opus.model_id (tier 1, Opus); never typed from memory.
MODEL_LINE="$(grep -E '^MODEL \(tier 1' "$BRIEF" | head -1)"
[ -n "$MODEL_LINE" ] || { echo "REFUSING: the brief has no 'MODEL (tier 1 …' line" >&2; exit 9; }
OPUS_ID="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["levels"]["opus"]["model_id"])' "$MODELS_JSON" 2>/dev/null)"
[ -n "$OPUS_ID" ] || { echo "REFUSING: $MODELS_JSON levels.opus.model_id is unreadable" >&2; exit 9; }
MODEL="$(printf '%s' "$MODEL_LINE" | sed -E 's/.*: *`?([a-z0-9.-]+)`? *$/\1/')"
[ "$MODEL" = "$OPUS_ID" ] || { echo "REFUSING: the kit's MODEL '$MODEL' is not models_latest.json levels.opus.model_id '$OPUS_ID' — re-stamp the MODEL line from the file" >&2; exit 9; }

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
[ "$(printf '%s\n' "$PIN" | wc -l | tr -d ' ')" = "2" ] || { echo "REFUSING: PIN-HEADS must carry exactly two rows (MAIN RD774)" >&2; exit 40; }
for ID in MAIN RD774; do
  R="$(prow "$PIN" "$ID")"
  [ "$(printf '%s\n' "$R" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: PIN-HEADS must carry exactly one row '$ID'" >&2; exit 40; }
  [ "$(printf '%s\n' "$R" | awk -F'\t' '{print NF}')" = "7" ] || { echo "REFUSING: PIN-HEADS row $ID does not have 7 cells: $R" >&2; exit 40; }
  [ "$(pfld "$PIN" "$ID" 7)" = "IN" ] || { echo "REFUSING: PIN-HEADS row $ID status is not IN" >&2; exit 40; }
  [ "$(pfld "$PIN" "$ID" 2)" = "nexusai" ] || { echo "REFUSING: PIN-HEADS row $ID repo must be nexusai" >&2; exit 40; }
done
printf '%s' "$(prow "$PIN" RD774)" | grep -q '@' && { echo "REFUSING: PIN-HEADS row RD774 still carries a placeholder" >&2; exit 40; }
[ "$(pfld "$PIN" RD774 3)" = "$B774" ] && [ "$(pfld "$PIN" RD774 4)" = "$H774" ] && [ "$(pfld "$PIN" RD774 5)" = "$FLOOR_MAIN" ] && [ "$(pfld "$PIN" RD774 6)" = "8" ] \
  || { echo "REFUSING: PIN-HEADS RD774 is not $B774 @ 115a775, base d463f881 (main at the 2026-10-21 re-pin), 8 commits — re-pin kit AND launcher" >&2; exit 40; }
[ "$(pfld "$PIN" MAIN 3)" = "main" ] || { echo "REFUSING: PIN-HEADS MAIN row is not branch main" >&2; exit 40; }
PIN_MAIN="$(pfld "$PIN" MAIN 4)"
STAMP_LINE="$(grep -E '^MAIN-STAMP: ' "$BRIEF")"
[ "$(printf '%s\n' "$STAMP_LINE" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: the brief must carry exactly one 'MAIN-STAMP: ' line" >&2; exit 40; }
MAIN_STAMPED=1; S_LANDED=''
if printf '%s' "$STAMP_LINE$PIN_MAIN" | grep -qF "$PH_SLOT"; then
  MAIN_STAMPED=0; STAMP_OK=0
else
  S_SHA="$(printf '%s' "$STAMP_LINE" | sed -nE 's/^MAIN-STAMP: sha `?([0-9a-f]{40})`? \| tree `?([0-9a-f]{40})`? \| landed since d463f881: (.+)$/\1/p')"
  S_TREE="$(printf '%s' "$STAMP_LINE" | sed -nE 's/^MAIN-STAMP: sha `?([0-9a-f]{40})`? \| tree `?([0-9a-f]{40})`? \| landed since d463f881: (.+)$/\2/p')"
  S_LANDED="$(printf '%s' "$STAMP_LINE" | sed -nE 's/^MAIN-STAMP: sha `?([0-9a-f]{40})`? \| tree `?([0-9a-f]{40})`? \| landed since d463f881: (.+)$/\3/p')"
  is40 "$S_SHA" && is40 "$S_TREE" && [ -n "$S_LANDED" ] || { echo "REFUSING: the MAIN-STAMP line is not 'MAIN-STAMP: sha <40-hex> | tree <40-hex> | landed since d463f881: <text>'" >&2; exit 40; }
  [ "$PIN_MAIN" = "$S_SHA" ] || { echo "REFUSING: PIN-HEADS MAIN ($PIN_MAIN) and the MAIN-STAMP sha ($S_SHA) disagree — stamp the same sha in both" >&2; exit 40; }
fi

# 18T — the T9 MOUNTED refuses: two lock bases would split the FIFO (ruling q); Tuesday decides the base first.
[ ! -d "$T9_VOL" ] || { echo "REFUSING: $T9_VOL is MOUNTED — the brief's lock base (locks-laptop-1017) assumes it is not; Tuesday decides the base, then re-brief" >&2; exit 18; }

# 18 — RE-PIN NOW by ls-remote (C-192 retries): main = the stamped MAIN pin EXACTLY; the branch = its pin; the PR ref (NOTE).
lsr refs/heads/main "refs/heads/$B774" refs/pull/97/head \
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
[ "$(ref_now "refs/heads/$B774")" = "$H774" ] || { echo "REFUSING: origin $B774 is '$(ref_now "refs/heads/$B774")', not 115a775 — the head MOVED; re-pin kit AND launcher (a new head is a new kit amendment)" >&2; exit 18; }
[ "$(ref_now refs/pull/97/head)" = "$H774" ] || echo "NOTE: refs/pull/97/head is '$(ref_now refs/pull/97/head)', not 115a775 — PR #97 moved; the gate reads it" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 6 — every sha the guards use is a commit in the local object store (this launcher never fetches).
for S in "$MAIN_SHA" "$FLOOR_MAIN" "$M3965" "$M7700" "$L888" "$H774" "$H278" "$MF1A" "$E884" "$M256" "$M29" "$H4C9" "$M360" "$B63"; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: ${S:0:12} is not a commit in $REPO (got '$T') — this launcher never fetches; the seat's next fetch brings it, then re-check" >&2; exit 6; }
done

# 18M — M0 by ANCESTRY (never --first-parent) + trees; M0's tree = the stamp; the head NOT on M0; the mode.
[ "$(tree_of "$FLOOR_MAIN")" = "$FLOOR_TREE" ] && [ "$(tree_of "$M3965")" = "$T3965" ] && [ "$(tree_of "$M7700")" = "$T7700" ] && [ "$(tree_of "$L888")" = "$T888" ] \
  || { echo "REFUSING: d463f881 / 39653db / 7700caf / 888203c are not trees 53d51c5 / 704c442 / ba9581a / 428f042 (the measured mains)" >&2; exit 18; }
for S in "$L888" "$M7700" "$M3965" "$FLOOR_MAIN"; do
  g merge-base --is-ancestor "$S" "$MAIN_SHA" 2>/dev/null || { echo "REFUSING: ${S:0:7} is not in M0 ${MAIN_SHA:0:7}'s ANCESTRY — M0 is not a descendant of the measured main d463f881" >&2; exit 18; }
done
# mode-0 premise (the re-pin): the re-pinned base d463f881 is an ANCESTOR of the head (the head carries it; nothing is merged).
g merge-base --is-ancestor "$FLOOR_MAIN" "$H774" 2>/dev/null || { echo "REFUSING: d463f881 is NOT an ancestor of the head 115a775 — the mode-0 premise (the head already carries the base) is gone; re-brief" >&2; exit 18; }
M0_TREE="$(tree_of "$MAIN_SHA")"
if [ "$MAIN_STAMPED" = "1" ]; then
  [ "$M0_TREE" = "$S_TREE" ] || { echo "REFUSING: M0 ${MAIN_SHA:0:7}'s tree is '${M0_TREE:0:12}', not the stamped tree '${S_TREE:0:12}'" >&2; exit 18; }
fi
for S in "$H774" "$H278" "$MF1A" "$E884" "$M256" "$H4C9" "$M360" "$B63"; do
  if g merge-base --is-ancestor "$S" "$MAIN_SHA" 2>/dev/null; then echo "REFUSING: PR #97 commit ${S:0:7} is ALREADY on M0 ${MAIN_SHA:0:7} — it landed before its gate; re-brief" >&2; exit 18; fi
done
LANDED_N="$(g rev-list --count "${FLOOR_MAIN}..${MAIN_SHA}" 2>/dev/null)"
if [ "$MAIN_SHA" = "$FLOOR_MAIN" ]; then
  MODE='0'
  if [ "$MAIN_STAMPED" = "1" ] && [ "$(printf '%s' "$S_LANDED" | tr '[:upper:]' '[:lower:]')" != "none" ]; then echo "REFUSING: M0 is d463f881 but the MAIN-STAMP names something landed ('$S_LANDED') — stamp 'none'" >&2; exit 18; fi
else
  MODE='a-or-b'
  echo "NOTE: M0 ${MAIN_SHA:0:7} is $LANDED_N commit(s) past d463f881 — what landed: $(g log --format='%h %s' "${FLOOR_MAIN}..${MAIN_SHA}" 2>/dev/null | head -5 | cut -c1-90 | tr '\n' ';') — T0 mode (a) or (b) applies" >&2
  if [ "$MAIN_STAMPED" = "1" ] && [ "$(printf '%s' "$S_LANDED" | tr '[:upper:]' '[:lower:]')" = "none" ]; then echo "REFUSING: M0 is not d463f881 but the MAIN-STAMP says 'landed since d463f881: none' — name what landed" >&2; exit 18; fi
  MB_M0="$(g merge-base "$MAIN_SHA" "$H774" 2>/dev/null)"
  GD0="$(g rev-parse --absolute-git-dir 2>/dev/null)"; OB0="$(find "$GD0/objects" -type f 2>/dev/null | wc -l | tr -d ' ')"
  MC0="$(mt_conflicts "$MB_M0" "$MAIN_SHA" "$H774")"
  OA0="$(find "$GD0/objects" -type f 2>/dev/null | wc -l | tr -d ' ')"
  [ -z "$MC0" ] || [ "$MC0" = "$COUNTS_FILE" ] || { echo "REFUSING: the legacy merge-tree of 115a775 onto M0 shows conflict markers in '$MC0', not the counts file only — a non-counts conflict is a STOP; re-brief" >&2; exit 18; }
  [ "$OB0" = "$OA0" ] || echo "NOTE: NexusAI .git/objects went $OB0 -> $OA0 around the legacy merge-tree read — the trivial-merge mode writes none; a live seat may have" >&2
fi
FP_HIT="$(g log --first-parent --format='%H' "$MAIN_SHA" 2>/dev/null | grep -cxF "$FLOOR_MAIN")"
[ "$FP_HIT" != "0" ] || echo "NOTE: a --first-parent walk from M0 does not reach 7700caf — the ancestry check above decides (gate 27's topology note)" >&2

# 7 / 8 — the head's chain: 888203c -> 63bef65 -> 360cd82 (63bef65 + 7700caf) -> 4c9b0d3 -> 2566713 (4c9b0d3 + 29c5ee8) -> e884516 -> f1a2e76 (e884516 + 39653db) -> 278afc2 -> 115a775 (278afc2 + d463f881),
#         every parent list and tree; merge-base with d463f881 = d463f881; 8 commits over it, 35 over 888203c, 8 first-parent.
[ "$(parents_of "$H774")" = "$H278 $FLOOR_MAIN" ] && [ "$(parents_of "$H278")" = "$MF1A" ] && [ "$(parents_of "$MF1A")" = "$E884 $M3965" ] && [ "$(parents_of "$E884")" = "$M256" ] \
  && [ "$(parents_of "$M256")" = "$H4C9 $M29" ] && [ "$(parents_of "$H4C9")" = "$M360" ] && [ "$(parents_of "$M360")" = "$B63 $M7700" ] && [ "$(parents_of "$B63")" = "$L888" ] \
  || { echo "REFUSING: the head chain is not 115a775 (278afc2 + d463f881) <- 278afc2 <- f1a2e76 (e884516 + 39653db) <- e884516 <- 2566713 (4c9b0d3 + 29c5ee8) <- 4c9b0d3 <- 360cd82 (63bef65 + 7700caf) <- 63bef65 <- 888203c" >&2; exit 7; }
[ "$(tree_of "$H774")" = "$T774" ] && [ "$(tree_of "$H278")" = "$T278" ] && [ "$(tree_of "$MF1A")" = "$TF1A" ] && [ "$(tree_of "$E884")" = "$TE884" ] && [ "$(tree_of "$M256")" = "$T256" ] \
  && [ "$(tree_of "$H4C9")" = "$T4C9" ] && [ "$(tree_of "$M360")" = "$T360" ] && [ "$(tree_of "$B63")" = "$T63" ] \
  || { echo "REFUSING: the head chain's trees are not 3cf0b84 / ee819f2 / 5c80bbc / 3571969 / f5322b4 / 26f5dd7 / a02a875 / 2b20a25" >&2; exit 8; }
[ "$(g merge-base "$H774" "$FLOOR_MAIN" 2>/dev/null)" = "$FLOOR_MAIN" ] && [ "$(g rev-list --count "${FLOOR_MAIN}..${H774}" 2>/dev/null)" = "8" ] \
  && [ "$(g rev-list --count "${L888}..${H774}" 2>/dev/null)" = "35" ] && [ "$(g rev-list --count --first-parent "${L888}..${H774}" 2>/dev/null)" = "8" ] \
  || { echo "REFUSING: 115a775 does not carry d463f881, or is not 8 commits over d463f881 (35 over 888203c, 8 first-parent)" >&2; exit 8; }

# 90 — the INSTALLED lock tool PINNED; it honours NEXUSAI_LOCK_BASE; the Laptop-DEV base is present with queue-jest; no qa-g29 ticket.
INST_NOW="$(fsha "$LOCKTOOL")"
[ "$INST_NOW" = "$LOCK_SHA_INST" ] || { echo "REFUSING: the INSTALLED lock tool's sha256 is '${INST_NOW:-absent}', not 3c33f5ae… — find out who changed it; re-brief" >&2; exit 90; }
grep -qF 'BASE="${NEXUSAI_LOCK_BASE:-' "$LOCKTOOL" || { echo "REFUSING: the installed tool no longer honours NEXUSAI_LOCK_BASE — ruling q's premise" >&2; exit 90; }
bash -n "$LOCKTOOL" 2>/dev/null || { echo "REFUSING: $LOCKTOOL does not parse (bash -n)" >&2; exit 90; }
grep -qF -- '--replace' "$LOCKTOOL" && grep -qF 'jest|docker) ;;' "$LOCKTOOL" || { echo "REFUSING: $LOCKTOOL lacks --replace or the jest kind" >&2; exit 90; }
[ -d "$LOCK_BASE_LAPTOP" ] && [ -d "$LOCKQ_J" ] || { echo "REFUSING: the Laptop-DEV lock base $LOCK_BASE_LAPTOP (queue-jest) is not present (ruling q)" >&2; exit 90; }
BQ="$(grep -l '^tag=qa-g29' "$LOCKQ_J"/* 2>/dev/null | wc -l | tr -d ' ')"
[ "${BQ:-0}" = "0" ] || { echo "REFUSING: $BQ qa-g29* ticket(s) already in $LOCKQ_J — a live or stale gate-29 ticket; read before launch" >&2; exit 90; }
HOLDER="$(sed -n 's/^tag=//p' "$LOCK_BASE_LAPTOP/nexusai-jest.lock/owner" 2>/dev/null | head -1)"
case "$HOLDER" in
  qa-g29*) echo "REFUSING: the Laptop-DEV jest lock is HELD by '$HOLDER' — a gate-29 holder already exists" >&2; exit 90 ;;
  qa-g28*) LOCK_OK=0; LOCK_WHY="the jest lock is HELD by gate 28 ('$HOLDER')" ;;
  '') ;;
  *) echo "NOTE: the Laptop-DEV jest lock is held now by '$HOLDER' (FIFO; the gate waits behind it)" >&2 ;;
esac
G28Q="$(grep -l '^tag=qa-g28' "$LOCKQ_J"/* 2>/dev/null | wc -l | tr -d ' ')"
[ "${G28Q:-0}" = "0" ] || { LOCK_OK=0; LOCK_WHY="${LOCK_WHY:+$LOCK_WHY; }$G28Q gate-28 ticket(s) queued in $LOCKQ_J"; }
GQ="$(grep -lE '^tag=qa-g' "$LOCKQ_J"/* 2>/dev/null | wc -l | tr -d ' ')"
[ "${GQ:-0}" = "0" ] || echo "NOTE: $GQ qa- gate ticket(s) queued — FIFO; gate 29 waits behind them, never touches them" >&2
LB_WAS="${NEXUSAI_LOCK_BASE:-}"
[ -z "$LB_WAS" ] || [ "$LB_WAS" = "$LOCK_BASE_LAPTOP" ] || echo "NOTE: NEXUSAI_LOCK_BASE was '$LB_WAS' in the launcher's environment — REPLACED by the Laptop-DEV base before exec (ruling q)" >&2

# 91 — the C-57 runner and the C-133 tool PINNED, and the runner's ROOT / LOCK_BASE / rm premises that T1 rests on (mode a).
C57_NOW="$(fsha "$C57TOOL")"; C133_NOW="$(fsha "$C133TOOL")"
[ "$C57_NOW" = "$C57_SHA" ] || { echo "REFUSING: c57-id-superset.sh sha256 is '${C57_NOW:-absent}', not 1ae84a10…5581 — re-brief" >&2; exit 91; }
[ "$C133_NOW" = "$C133_SHA" ] || { echo "REFUSING: c133-accounting.py sha256 is '${C133_NOW:-absent}', not 6f938bfc…f972f — re-brief" >&2; exit 91; }
grep -qF 'if [ -n "${C57_ROOT:-}" ]; then ROOT="$C57_ROOT"' "$C57TOOL" && grep -qF 'LOCK_BASE="${NEXUSAI_LOCK_BASE:-' "$C57TOOL" \
  && grep -qF 'rm -rf "$wt"' "$C57TOOL" && grep -qF 'worktree remove --force "$wt"' "$C57TOOL" \
  || { echo "REFUSING: the C-57 runner's C57_ROOT / LOCK_BASE / rm / worktree lines are not as T1 describes" >&2; exit 91; }

# 22 — the gated file set over d463f881 (the same 8 paths as 39653db..278afc2 and 7700caf..4c9b0d3 were); no static/ or templates/ path; 360cd82's forward merge is counts-only (legacy merge-tree).
#      (the conflict sets of the later forward merges 2566713 and f1a2e76 are UNMEASURED by this launcher: the kit's r1 measures them in the gate's store.)
[ "$(paths_of "$FLOOR_MAIN" "$H774")" = "$(sorted "$GATED_774")" ] || { echo "REFUSING: the gated files (d463f881..115a775) are not the briefed 8 (WRONG 4)" >&2; exit 22; }
[ "$(g diff --name-only "$FLOOR_MAIN" "$H774" -- static templates 2>/dev/null | grep -c .)" = "0" ] || { echo "REFUSING: PR #97 now changes a static/ or templates/ path — the browser leg's premise (WRONG 13) moved" >&2; exit 22; }
GD="$(g rev-parse --absolute-git-dir 2>/dev/null)"
OBJ_BEFORE="$(find "$GD/objects" -type f 2>/dev/null | wc -l | tr -d ' ')"
MC360="$(mt_conflicts "$L888" "$B63" "$M7700")"
[ "$MC360" = "$COUNTS_FILE" ] || { echo "REFUSING: the legacy merge-tree of 63bef65 and 7700caf shows conflict markers in '${MC360:-nothing}', not the counts file ONLY (WRONG 3)" >&2; exit 22; }
OBJ_AFTER="$(find "$GD/objects" -type f 2>/dev/null | wc -l | tr -d ' ')"
[ "$OBJ_BEFORE" = "$OBJ_AFTER" ] || echo "NOTE: NexusAI .git/objects went $OBJ_BEFORE -> $OBJ_AFTER around the legacy merge-tree reads — the trivial-merge mode writes none; a live seat may have" >&2

# 93 — the premises at source: counts + predictions, blobs, the RD-774/836 anchors, the sibling-writer premise, the plant and seed premises.
[ "$(counts_at "$FLOOR_MAIN")" = "4934 303" ] && [ "$(blob "$FLOOR_MAIN" "$COUNTS_FILE")" = "$CB_FLOOR" ] && [ "$(counts_at "$M3965")" = "4880 302" ] && [ "$(blob "$M3965" "$COUNTS_FILE")" = "$CB_3965" ] \
  && [ "$(counts_at "$H774")" = "4964 304" ] && [ "$(blob "$H774" "$COUNTS_FILE")" = "$CB_HEAD" ] \
  && [ "$(counts_at "$H278")" = "4910 303" ] && [ "$(blob "$H278" "$COUNTS_FILE")" = "$CB_278" ] && [ "$(blob "$MF1A" "$COUNTS_FILE")" = "$CB_278" ] && [ "$(counts_at "$M7700")" = "4676 292" ] && [ "$(blob "$M7700" "$COUNTS_FILE")" = "$CB_7700" ] \
  && [ "$(counts_at "$H4C9")" = "4700 293" ] && [ "$(blob "$H4C9" "$COUNTS_FILE")" = "$CB_4C9" ] && [ "$(blob "$M360" "$COUNTS_FILE")" = "$CB_360" ] \
  || { echo "REFUSING: counts are not 4934/303 a28458a (d463f881), 4880/302 2cc0948 (39653db), 4964/304 c050e78 (head 115a775), 4910/303 57659c6 (278afc2 = f1a2e76), 4676/292 c136311 (7700caf), 4700/293 ff5f5d7 (4c9b0d3), 7436f51 (360cd82) (WRONG 5)" >&2; exit 93; }
M0C="$(counts_at "$MAIN_SHA")"; M0T="${M0C% *}"; M0S="${M0C#* }"
printf '%s' "$M0C" | grep -Eq '^[0-9]+ [0-9]+$' || { echo "REFUSING: M0's counts file is unreadable" >&2; exit 93; }
if [ "$MODE" = "0" ]; then PRED="mode 0: the head's own 4964/304"; else PRED="mode a: M0 $M0T/$M0S + 30/1 = $((M0T+30))/$((M0S+1))"; fi
for S in "$MAIN_SHA" "$H774"; do
  [ "$(blob "$S" "$LOCK")" = "$LOCK_BLOB" ] && [ "$(blob "$S" "$PKG")" = "$PKG_BLOB" ] && [ "$(blob "$S" "$DEPLOY_WF")" = "$DEPLOY_BLOB" ] \
    || { echo "REFUSING: ${S:0:7} does not carry lockfile 19477a9 / package.json 384805d / deploy-demo.yml 953b2a2 (ruling m, r13)" >&2; exit 93; }
done
[ "$(cntF "$MAIN_SHA" "$DEPLOY_WF" "vars.CI_DEPLOY_ENABLED == 'true'")" = "2" ] || { echo "REFUSING: deploy-demo.yml at M0 no longer gates BOTH jobs on vars.CI_DEPLOY_ENABLED == 'true' (r13)" >&2; exit 93; }
[ "$(lockver "$LOCK_BLOB" proxy-addr)" = "2.0.8" ] && [ "$(lockver "$LOCK_BLOB" playwright)" = "1.62.1" ] && [ "$(lockver "$LOCK_BLOB" playwright-core)" = "1.62.1" ] \
  || { echo "REFUSING: lock 19477a9 does not resolve proxy-addr 2.0.8, playwright 1.62.1, playwright-core 1.62.1 (ruling m, ruling u)" >&2; exit 93; }
for pair in "$SERVER $SERVER_BLOB" "$SIMPLEDB $SIMPLEDB_BLOB" "$VALIDATORS $VALIDATORS_BLOB" "$TEMPLATES $TEMPLATES_BLOB" "$LOGSAFE $LOGSAFE_BLOB" "$T774FILE $T774FILE_BLOB" "$SPY $SPY_BLOB" "$SECFIX $SECFIX_BLOB"; do
  set -- $pair
  [ "$(blob "$H774" "$1")" = "$2" ] || { echo "REFUSING: $1 at 115a775 is not blob ${2:0:12} (WRONG 4's H-21 restore pins)" >&2; exit 93; }
done
[ "$(blob "$FLOOR_MAIN" "$LOGSAFE")" = "$LOGSAFE_BLOB" ] || { echo "REFUSING: backend/logSafe.js at d463f881 is not edfb81f — the head's logSafe is no longer main's (r10)" >&2; exit 93; }
# the files the new commits did NOT change and the gate leans on: equal to main's d463f881 blob AND the pin at the head (authEnforcement = the admin gate's machinery).
[ "$(blob "$H774" "$AUTHENF")" = "$AUTHENF_BLOB" ] && [ "$(blob "$FLOOR_MAIN" "$AUTHENF")" = "$AUTHENF_BLOB" ] || { echo "REFUSING: $AUTHENF is not blob ca764a4 at both 115a775 and d463f881 — the admin gate's machinery moved (WRONG 4)" >&2; exit 93; }
set -- $EQMAIN_PINS
while [ "$#" -ge 2 ]; do
  [ "$(blob "$H774" "$1")" = "$2" ] && [ "$(blob "$FLOOR_MAIN" "$1")" = "$2" ] || { echo "REFUSING: $1 is not blob ${2:0:12} at both 115a775 and d463f881 (WRONG 4's unchanged-and-equal-to-main list)" >&2; exit 93; }
  shift 2
done
# '~' delimits path ~ anchor ~ expected line count (an anchor may itself contain '|', e.g. the '||' in templateSql).
while IFS='~' read -r F Q N; do
  [ -n "$F" ] || continue
  [ "$(cntF "$H774" "$F" "$Q")" = "$N" ] || { echo "REFUSING: '$Q' is not $N time(s) in $F at 115a775 — an anchor the kit rests on moved; re-brief" >&2; exit 93; }
done <<'EOF_ANCHORS'
backend/server.js~const SQL_TEXT_FIELDS = ['sqlQuery', 'sql_query'];~1
backend/server.js~const RISK_CONDITION_PUT_FIELDS = ['condition_text', 'risk_level', 'is_active', 'email_recipients'];~1
backend/server.js~app.post('/api/risk-conditions', requireRiskConditionAdmin, refuseSqlText, validateInput, validateRequest(riskConditionInputSchema), async (req, res) => {~1
backend/server.js~app.post('/api/risk-conditions/sync', requireRiskConditionAdmin, async (req, res) => {~1
backend/server.js~app.put('/api/risk-conditions/:id', requireRiskConditionAdmin, refuseSqlText, async (req, res) => {~1
backend/server.js~app.delete('/api/risk-conditions/:id', requireRiskConditionAdmin, async (req, res) => {~1
backend/server.js~app.post('/api/settings/risk-definitions', requireRiskConditionAdmin, async (req, res) => {~1
backend/server.js~app.post('/api/settings/risk-definitions', async (req, res) => {~0
backend/server.js~app.post('/api/validate-condition', validateInput, async (req, res) => {~1
backend/server.js~if (saveToDatabase && !(await requireAdminFor(req, res))) return;~1
backend/server.js~logSafe(~24
backend/server.js~app.post('/api/notifications/run-now', async (req, res) => {~1
backend/server.js~logger.info(`⚠️ Unrecognized condition pattern: "${logSafe(conditionText)}", using default query`);~1
backend/server.js~return database.executeRiskTemplate(templateId, params, limit);~1
backend/simpleDb.js~async executeRiskTemplate(templateId, params = [], limit = 100) {~1
backend/simpleDb.js~const safeLimit = Math.min(Math.max(parseInt(limit, 10) || 100, 1), 10000);~1
backend/simpleDb.js~async executeRiskQuery(~0
backend/services/riskSqlTemplates.js~if (typeof templateId !== 'string' || !Object.prototype.hasOwnProperty.call(TEMPLATES, templateId)) {~1
__tests__/rd774-risk-sql-templates.test.js~const PLANTED_SQL = `SELECT Job_ID, User_Name AS ${MARKER} FROM printer_logs WHERE Total_Sheets_Used >= 0`;~1
EOF_ANCHORS
# the head's server never calls the old executor (simpleDb's own comment names it, so simpleDb is checked for the DEFINITION above, not the word).
[ "$(cntF "$H774" "$SERVER" 'executeRiskQuery(')" = "0" ] \
  || { echo "REFUSING: executeRiskQuery( still appears in the head's server — the census premise (WRONG 7) moved" >&2; exit 93; }
[ "$(cntF "$FLOOR_MAIN" "$SERVER" 'executeRiskQuery(condition.sql_query')" -ge 3 ] || { echo "REFUSING: d463f881 no longer executes condition.sql_query (r4's BASE control premise)" >&2; exit 93; }
[ "$(cntF "$H774" "$T774FILE" 'UNION')" = "0" ] || echo "NOTE: the rd774 test now mentions UNION — re-read WRONG 6 (the planted SQL was a marker SELECT at drafting)" >&2
grep -qF '"lo":"2026-10-18 20:19:32","hi":"2026-10-18 20:19:32"' "$S101/rd774-char/main-888203c.txt" 2>/dev/null || echo "NOTE: the builder's characterisation file no longer records the single seed created_at — re-read WRONG 10 (T2's premise)" >&2

# 96 — the browser leg's local premises (ruling u): Chrome installed, Playwright in the lock (above); NOTEs record versions and the cache.
[ -d "$CHROME_APP" ] || { echo "REFUSING: $CHROME_APP is absent — b1-b3 cannot run (ruling u: the locally installed Google Chrome)" >&2; exit 96; }
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
grep -qF 'NOT RUN, named, under ruling (o) EXTENDED' "$BRIEF25" && grep -qF 'NOT RUN, named, under ruling (o) EXTENDED' "$BRIEF" \
  || { echo "REFUSING: ruling (o)'s EXTENSION words are not carried in gate 25's brief and this brief" >&2; exit 70; }
[ -s "$G19_RELEASE" ] && grep -qF 'the by-hand gate yield (ruling (i)) is RETIRED from gate 21 on.' "$G19_RELEASE" || { echo "REFUSING: gate 19's RELEASE no longer carries the yield retirement" >&2; exit 70; }
[ -s "$DRIVER_ANS" ] && grep -qF "Playwright 1.62.1 from YOUR tree's own node_modules, launching the locally installed Google Chrome" "$DRIVER_ANS" \
  && grep -qF "headless (channel 'chrome'), no download, under your network belt, every non-127.0.0.1 request aborted." "$DRIVER_ANS" \
  || { echo "REFUSING: gate 21's browser-driver ruling (u) is not at $DRIVER_ANS as quoted" >&2; exit 70; }
[ -s "$ANS1" ] && grep -qF 'load1 below 8 before every heavy run' "$ANS1" && grep -qF 'lock base locks-laptop-1017' "$ANS1" || { echo "REFUSING: Tuesday's ANSWER-1 (load 8, lock base) is not at $ANS1 as quoted" >&2; exit 70; }
while IFS='|' read -r F Q; do
  [ -n "$F" ] || continue
  [ -s "$F" ] && grep -qF -- "$Q" "$F" || { echo "REFUSING: '$Q' is no longer in $F — the ruling moved; re-brief" >&2; exit 70; }
  grep -qF -- "$Q" "$BRIEF" || { echo "REFUSING: the brief does not quote '$Q' verbatim" >&2; exit 70; }
done <<EOF_ANS
$ANS20|RD-774 + RD-836 together, one branch off then-main, tier 1 (security)
$ANS21|RULED P1 = (ii); P2 = ticket, not built here.
$ANS21|If a difference reaches a customer-visible screen on the demo path (LAW), STOP and ask
$ANS23|Fix it IN CODE before you send READY FOR QA. Never dismiss it.
$ANS24|Tuesday commissions a TIER-1 gate (gate 29, Opus: security design: SQL templates, request-SQL refusal, admin writers). It launches when gate 28 frees the jest lock.
$ANS24|HOLD. PR #97 stays draft; no push to the branch unless the gate or Tuesday asks; no land.
EOF_ANS
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
[ "$NODEV" = "v26.8.1" ] || echo "NOTE: host node is '${NODEV:-absent}', not v26.8.1 as briefed (T9) — the gate records it" >&2
GLV="$(gitleaks version 2>/dev/null)"
[ "$GLV" = "8.30.1" ] || echo "NOTE: gitleaks is '${GLV:-absent}', not 8.30.1 — r13 records it" >&2
LOAD1="$(sysctl -n vm.loadavg 2>/dev/null | awk '{print $2}')"
awk -v l="${LOAD1:-99}" 'BEGIN{exit !(l < 8)}' || echo "NOTE: 1-minute load is ${LOAD1:-unknown} (not below 8) — the gate waits in the queue, never in a hold (ruling p)" >&2

# 31 — the READY copy (sha256 PINNED), builder evidence, gate 27's / 25's / 26's instruments (THIS drive), standing references.
for f in "$READY_774" "$CLAR" "$BRIEF22" "$BRIEF23" "$BRIEF24" "$BRIEF25" "$BRIEF26" "$BRIEF27" "$TEMPLATE" "$B27_REPORT" "$CHARTER" "$ANS20" "$ANS21" "$ANS23" "$ANS24" "$ANS26" "$ANS28" \
         "$S101/rd774-char/main-888203c.txt" "$S101/rd774-char/characterise.js" "$S101/rd774-runs/272-green.out" "$S101/rd774-runs/272-red.out" "$S101/rd774-runs/272-green2.out" "$S101/mail-31-ready-rd774.txt" \
         "$B27_INST/qa-file27.sh" "$B27_INST/qa-file27r.sh" "$B27_INST/qa-floorlib27.sh" "$B27_INST/qa-holdlib27.sh" "$B27_INST/qa-h1-scan27.py" "$B27_INST/qa-h1-selftest27.sh" \
         "$B27_INST/qa-mail27.py" "$B27_INST/qa-mailread27.py" "$B27_INST/qa-browser27.js" "$B27_INST/qa-b1cmp27.js" "$B27_INST/qa-b2cmp27.js" "$B27_INST/qa-ledger25.js" \
         "$B27_INST/qa-revert27.py" "$B27_INST/qa-to.sh" "$B27_INST/qa-floorcount.py" "$B27_INST/qa-netbelt.sb" "$B27_INST/qa-netbelt-nodns.sb" "$B27_INST/qa-names23.py" \
         "$B25_INST/qa-applymut.py" "$B25_INST/qa-lockcheck.py" "$B26_INST/qa-c57shim26.sh"; do
  [ -s "$f" ] || { echo "REFUSING: evidence, brief or tool absent: $f" >&2; exit 31; }
done
[ "$(fsha "$READY_774")" = "$READY_774_SHA" ] || { echo "REFUSING: the READY copy $READY_774 is not the saved GATE 29 RE-PIN SHEET copy (sha256 3debfc27…) — re-copy it from B349's STATUS" >&2; exit 31; }
# DEFERRED (like 32S): the kit must NAME the new READY sha256 — Tuesday stamps it in at FILL AT STAMP; until then the launch is refused LAST (READY_NAMED), so the guards below still run.
READY_NAMED=1; grep -qF "$READY_774_SHA" "$BRIEF" || { READY_NAMED=0; STAMP_OK=0; PROVISIONAL="$PROVISIONAL READY_SHA(the kit does not yet name 3debfc27…)"; }
grep -qF "$H774" "$READY_774" && grep -qF 'PASS 4964/4964 across 304' "$READY_774" && grep -qF 'GATE 29 RE-PIN SHEET' "$READY_774" \
  || { echo "REFUSING: the READY copy no longer names its head / verify line / sheet title" >&2; exit 31; }
grep -qF 'STATUS: COMPLETE' "$B27_REPORT" || { echo "REFUSING: gate 27's report does not read as delivered (the instrument source must be a DELIVERED gate)" >&2; exit 31; }
for B in "$BRIEF22" "$BRIEF23" "$BRIEF24" "$BRIEF25" "$BRIEF26" "$BRIEF27"; do grep -qF '## 3a. INSTRUMENT RULES' "$B" || { echo "REFUSING: $B has no section 3a — the H-rules carried by reference are missing" >&2; exit 31; }; done

# 10 / 17 — the report path from the brief's §11 (its date is a stamped slot); no stale report; the brief names its sources.
REPORT_RAW="$(grep -oE 'Report: `[^`]*/report\.md`' "$BRIEF" | head -1 | sed -E 's/^Report: `//; s/`$//')"
[ -n "$REPORT_RAW" ] || { echo "REFUSING: the brief's §11 has no 'Report: \`…/report.md\`' line" >&2; exit 10; }
if printf '%s' "$REPORT_RAW" | grep -qF "$PH_SLOT"; then
  STAMP_OK=0; REPORT=''; PROVISIONAL="$PROVISIONAL REPORT_DATE(unstamped)"
else
  printf '%s' "$REPORT_RAW" | grep -Eq "^$RPTS/20[0-9]{2}-[0-9]{2}-[0-9]{2}-gate29-rd774-rd836/report\.md$" \
    || { echo "REFUSING: the report path '$REPORT_RAW' is not $RPTS/<YYYY-MM-DD>-gate29-rd774-rd836/report.md" >&2; exit 10; }
  REPORT="$REPORT_RAW"
  [ "$(grep -oF "$(dirname "$REPORT")" "$BRIEF" | grep -c .)" -ge 2 ] || { echo "REFUSING: T9 and §11 do not name the SAME report directory (stamp one date in both)" >&2; exit 10; }
  [ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }
fi
for P in "2026-10-21_nexusai-gate29-READY-pr97-115a775.txt" "2026-10-19_S101O_ANSWER-2" "2026-10-13_nexusai-gate-batch22.md" "2026-10-16_nexusai-gate-batch23.md" "2026-10-17_nexusai-gate24-rd848.md" \
         "2026-10-18_nexusai-gate25-rd761-rd794-merged.md" "2026-10-18_nexusai-gate26-c170-be0fe37-merged.md" "2026-10-18_nexusai-gate27-rd778-xss.md" "2026-10-05_qa_b14_belt_ANSWER.md" \
         "2026-10-06_nexusai_g18_ruling_b_deliver_now.md" "2026-10-04_qa_batch13_browser_driver_answer.md" "qa-file27.sh" "qa-file27r.sh" "qa-applymut.py" "qa-browser27.js" \
         "QA_AGENT_CHARTER.md" "locks-laptop-1017" "ADDENDUM-1" "rd774-char" "rd774-runs" "models_latest.json"; do
  grep -qF "$P" "$BRIEF" || { echo "REFUSING: brief must name $P" >&2; exit 10; }
done

# 11 — identity: NexusAI's OWN dirs.
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || { echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"
[ -d "$CLAUDE_CONFIG_DIR" ] || { echo "REFUSING: Tuesday's claude store $CLAUDE_CONFIG_DIR is absent" >&2; exit 11; }

# 12 / 13 / 14 / 15 / 20 — tier, directive, brief path, pins, verdict route, key path, question route.
for T in 'TIER 1' 'MAIN-STAMP' 'NO GO' 'NO HOST NPM REGISTRY' 'FULL VERIFIES UNBELTED' 'EXTENSION' 'npm_config_update_notifier=false' 'BOTH thresholds block' 'RULING (b)' \
         '--replace' 'qa-g29-' 'RETIRED' 'H-34' 'H-35' 'C-63' 'C-209' 'C-211' 'THE SQL-PATH CENSUS' 'PLANTING THROUGH EVERY REQUEST PATH' 'STORED LEGACY SQL' 'THE TEMPLATE DERIVATION' \
         'THE CHARACTERISATION T0-T12' "RD-836's ADMIN-GATE MATRIX" 'THE SIBLING WRITERS' 'THE PUT ALLOW-LIST' 'THE RED-PROOF ROW' 'LOG SINKS' 'THE CODEQL ROW' 'THE SUITE ROW' 'THE NEW GATES' \
         'THE BROWSER LEG' 'YOUR OWN SQL SPY' 'spread-date' 'VOID' 'can fail' 'positive control' 'negative control' 'G29-<n>' 'NOT TESTED' 'PRIOR WORK' 'No HTTP to any production or demo host' \
         'never `--first-parent`' 'LEGITIMATE SHAPES'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not declare '$T'" >&2; exit 12; }
done
for T in 'TIER-1 SECURITY GATE' 'THE PROPERTIES' 'THE SQL-PATH CENSUS' 'THE TEMPLATE DERIVATION' 'ADMIN-GATE MATRIX' 'THE PUT ALLOW-LIST' 'THE CHARACTERISATION' 'THE FULL VERIFY' \
         'THE BROWSER LEG' 'PRIOR WORK' 'YOUR OWN SQL spy' 'spread-date' 'marker SELECT, not a UNION' 'r7S' 'r12b' 'b1' 'b3' 'M1' 'M12' '#272' '#70' '#220' '#221' 'C-209' 'C-215' \
         'as SETS' '13 F-10' 'mode 0' 'T0' 'T2' 'T3' 'T5' 'T6' 'T7' 'UNBELTED' 'npm_config_update_notifier=false' 'BOTH thresholds block' 'RULING (b)' 'EXTENSION' 'NAMED NOT RUN' '--replace' \
         'qa-g29-' 'RETIRED' 'locks-laptop-1017' 'jest lock' "Never trust the builder's trees" 'no HTTP to any production or demo host' 'One client only' 'NO docker object and NO az' 'no model call'; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare '$T'" >&2; exit 12 ;; esac
done
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
for S in "$H774" "$T774" "$M360" "$B63" "$FLOOR_MAIN" "$L888" "$LOCK_SHA_INST"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S in full" >&2; exit 14; }
  case "$PROMPT" in *"$S"*) ;; *) echo "REFUSING: prompt must name $S" >&2; exit 14 ;; esac
done
for S in "$FLOOR_TREE" "$T3965" "$T278" "$T7700" "$T360" "$T63" "$T4C9" "$T256" "$TE884" "$TF1A" "$H4C9" "$CB_FLOOR" "$CB_3965" "$CB_278" "$CB_7700" "$CB_4C9" "$CB_HEAD" "$CB_360" "$C57_SHA" "$C133_SHA" "$PKG_BLOB" "$LOCK_BLOB" "$DEPLOY_BLOB" "$PREBUILD_SHA" \
         "$SERVER_BLOB" "$SIMPLEDB_BLOB" "$VALIDATORS_BLOB" "$TEMPLATES_BLOB" "$LOGSAFE_BLOB" "$T774FILE_BLOB" "$SPY_BLOB" "$SECFIX_BLOB"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S in full" >&2; exit 14; }
done
# the kit names these four chain commits by their 7-character short sha only (the amend report's chain table carries the full ones): require the short form.
for S in "${M256:0:7}" "${E884:0:7}" "${MF1A:0:7}" "${M29:0:7}" "${H278:0:7}"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name ${S} (the 115a775 chain commit)" >&2; exit 14; }
done
# the kit names the AUTHENF blob as 'ca764a4b…' (short): require that, plus the EQMAIN pins in full.
grep -qF 'ca764a4b' "$BRIEF" || { echo "REFUSING: brief must name authEnforcement.js blob ca764a4b…" >&2; exit 14; }
set -- $EQMAIN_PINS
while [ "$#" -ge 2 ]; do grep -qF -- "$2" "$BRIEF" || { echo "REFUSING: brief must name $2 in full ($1 equal-to-main pin)" >&2; exit 14; }; shift 2; done
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
[ "$(grep -oE 'qa-g29-[A-Za-z0-9_<>-]*merge[A-Za-z0-9_-]*' "$BRIEF" | grep -c .)" = "0" ] || { echo "REFUSING: the brief suggests a qa-g29- tag containing 'merge' (C-141 ADDENDUM 7)" >&2; exit 15; }
[ "$(printf '%s\n' "$PROMPT" | grep -oE 'qa-g29-[A-Za-z0-9_<>-]*merge' | grep -c .)" = "0" ] || { echo "REFUSING: the prompt suggests a qa-g29- tag containing 'merge'" >&2; exit 15; }

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
WORDS="RD-774 RD-836 C-211 C-01 C-02 C-203 C-178 C-190 C-209 C-57 C-133 C-185 C-192 C-205 C-141 C-63 C-40 C-68 C-76 C-102 C-112 C-174 C-49 C-89 C-115 C-125 C-130 C-131 ADDENDA%6%and%7
r2 r3 r4 r5 r6 r7 r7S r8 r9 r10 r11 r12 r12b r14 b1 b2 b3 M0 7700caf 888203c 360cd82 63bef65 19477a9 proxy-addr playwright PR%#97 #272 #70 #220 #221 sqlite_master logSafe
L-B1 L-B9 L-Y1 H-1 H-3 H-4 H-6 H-9 H-14 H-17 H-20 H-21 H-22 H-24 H-26 H-27 H-28 H-29 H-31 H-32 H-33 H-34 H-35 H-36 --forceExit trap%on%EXIT DEADLINE LANDING%CONTROL
_prebuilds node_sqlite3.node sqlite3%binding:%cached%prebuild,%offline _update-notifier-last-checked exits%71 --mirror EXCLUSIVE STOP VOID C57_ROOT SQL_TEXT_NOT_ACCEPTED FIELD_NOT_ACCEPTED
MERGES%GO%FIRST QUEUE,%NEVER%TAKE%OVER SAME-PLACE%handover HEARTBEAT 2%minutes 5%minutes finally SESSION_SECRET%UNSET NOT%TESTED MEASURED%AT%RUNTIME READ%ONLY PROBED
RELAYED CodeQL%is%NOT%RUN UNKNOWN about%40%minutes 2-hour%maximum TRACKED%child Prior%work FOREGROUND never%push NEVER%merge Partner%Center npm%install --offline ENOTCACHED
qa-file27.sh ticket-left-* -r<N> instrument never%fixes GROUPED SPLIT never%dismissed PROVISIONAL qa-g29 G29-<n> N29-<n> 1-minute%load%of%8 S101O characterise.js Chrome%headless"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## TIER' '^## 2a-T. LEGITIMATE SHAPES' '^## WRONG OR UNVERIFIED' "^## TUESDAY'S RULINGS" '^## THE MODEL RULE' '^## Charter' '^## THE CLARIFICATIONS THAT BIND THIS GATE' '^## PRIOR WORK' \
         '^## 1. Target' '^### How to build your trees' '^## 2. Tier and severity' '^## 2a. ROWS' '^## 2b. HOW THE BROWSER LEG RUNS' '^## 3. THE QUESTIONS' '^## 3a. INSTRUMENT RULES' \
         '^## 3b. THE NEGATIVE-ASSERTION SWEEP' '^## 7. THE GATED TREE' '^## 8. CI, ALERTS, DEPLOY' '^## 9. Floor discipline' '^## 10. HELD' '^## 11. Output' '^## PROVENANCE' '^## FILL AT STAMP'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
WSTART="$(grep -n '^## WRONG OR UNVERIFIED' "$BRIEF" | cut -d: -f1)"; WEND="$(grep -n "^## TUESDAY'S RULINGS" "$BRIEF" | cut -d: -f1)"
[ "$WSTART" -lt "$WEND" ] || { echo "REFUSING: the WRONG OR UNVERIFIED section is not above TUESDAY'S RULINGS" >&2; exit 19; }
WUNMARKED="$(sed -n "${WSTART},${WEND}p" "$BRIEF" | grep -E '^[0-9]+\. ' | grep -vE 'MEASURED|READ-ONLY-INFERRED|own actions|drafter.s actions' | cut -c1-60)"
[ -z "$WUNMARKED" ] || { echo "REFUSING: WRONG items not marked MEASURED / READ-ONLY-INFERRED: $WUNMARKED" >&2; exit 19; }
for L in L-B1 L-B2 L-B3 L-B4 L-B5 L-B6 L-B7 L-B8 L-B9 L-Y1; do grep -qF "$L" "$BRIEF" || { echo "REFUSING: brief lacks declared limit $L (C-112)" >&2; exit 19; }; done
for R in r0 r1 r2 r3 r4 r5 r6 r7 r7S r8 r9 r10 r11 r12 r12b r13 r14 b1 b2 b3; do grep -qF "| $R |" "$BRIEF" || { echo "REFUSING: brief lacks row $R" >&2; exit 19; }; done
for n in 0 1 2 3 4 5 6 7 8 9 10; do
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
a clean merge-tree and a changed measured surface are not in tension
the server builds the SQL itself from fixed templates. The endpoint stops accepting SQL from the request.
NexusAI is open with no sign-in until the admin configures Entra.
A local run serves every page and API with no sign-in.
the four endpoint/tenant writers take the setup-mode-aware admin gate
a signed-in viewer in the sign-in configured + first-run incomplete state (the RD-437 state) still passes, which is intended under C-178.
CLAR_EOF

# 24 — the prompt must DESCRIBE the server entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qi 'backend/server\.js'; then
  echo "REFUSING: the prompt contains the server entry point's literal path (RD-591 c.37901). Describe it; do not name it." >&2; exit 24; fi

# 53 / 71 — standing rules in the brief; the NOT TESTED line read from the brief (ONE line); appended to the prompt at exec.
for w in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' 'qa-g29-' 'VOID' 'EXCLUSIVE' 'POSITIVE CONTROL FIRST' 'QUEUE, NEVER TAKE OVER' 'LANDING CONTROL' \
         '--replace' 'never push' 'C-174' '--forceExit' 'trap … EXIT' 'MERGES GO FIRST' 'queue-jest/' 'carry on' 'never idles holding a lock' \
         'ONE focused hold at a time' 'FOREGROUND' 'Never two live holds' 'Every finding names its instrument' \
         'NOT TESTED' 'The tester never fixes' 'SPLIT a hold' 'ONE CLIENT ONLY' 'no CodeQL alert dismissed' 'below a 1-minute load of **8**'; do
  grep -qiF -- "$w" "$BRIEF" || { echo "REFUSING: brief lacks the standing rule '$w'" >&2; exit 53; }
done
NOTTESTED_LINE="$(grep -E '^  Not tested by this gate: ' "$BRIEF" | sed 's/^  //')"
[ "$(printf '%s\n' "$NOTTESTED_LINE" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: the brief must carry exactly ONE '  Not tested by this gate: …' line (§11)" >&2; exit 71; }
for w in 'the CodeQL closure of alerts #70, #220 and #221' 'the Log Analytics and KQL execution path' 'a real Entra sign-in' 'the risk-alert scheduler on its cron timer' \
         'the full jest suite on Node 24' 'headed Chrome and every other browser engine' 'Windows' 'the demo (behind RD-76 SSO)'; do
  case "$NOTTESTED_LINE" in *"$w"*) ;; *) echo "REFUSING: the brief's NOT TESTED line lacks '$w'" >&2; exit 71 ;; esac
done
grep -qF 'The report'"'"'s LAST two lines are the two verdict lines' "$BRIEF" || { echo "REFUSING: brief must fix the report's last lines as the two verdict lines" >&2; exit 71; }
for V in '`RD-774+RD-836: <GO|GO WITH FINDINGS|NO GO> @ ' '`LANDING CHECKLIST: PR #97 '; do
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
# fleet-monitor and every live 'QA/*' pane other than this gate's own (gate 28 included while it runs): a negative control when exactly one claude runs under it.
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

# 86 — no live gate-29 session already exists.
for P in $(pane_pid_of "$ROUTE_NAME"); do
  if [ -n "$(claude_under "$P")" ]; then echo "REFUSING: a pane named $ROUTE_NAME (pid $P) already runs a claude — gate 29 is live; do not start a second session" >&2; exit 86; fi
  [ "$CHECK" = "1" ] || echo "NOTE: a pane named $ROUTE_NAME (pid $P) exists with no claude under it — the cockpit's own add decides" >&2
done

# 32S / 33L / 40 — LAST: the coordinator's stamp (0 at-sign SLOT placeholders anywhere in the kit: MAIN pin, REPORT_DATE, RULED: T0-T10, SELF-CHECK
# + note; the SELF-CHECK line in the fleet's form), gate 28's release of the jest lock, and the answer route (Tuesday adds it, never this launcher).
NSLOT="$(grep -oF "$PH_SLOT" "$BRIEF" | grep -c .)"
if [ "$NSLOT" != "0" ] || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then STAMP_OK=0; fi
ROUTE_OK=1
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || ROUTE_OK=0
GUARDS='9 40 18T 18 6 18M 7 8 90 91 22 93 96 70 70N 31 10 17 11 12 13 14 15 20 41 82 19 24 53 71 76 77 78 79 38R 86'
SUMMARY="ls-remote attempts this run: $LSR_ATTEMPTS (C-192); origin main ${M_ORIGIN:0:7} (M0 ${MAIN_SHA:0:7} tree ${M0_TREE:0:7}; ancestry carries 888203c, 7700caf, 39653db and d463f881; PR #97 not on M0; d463f881 an ancestor of the head; MODE $MODE); RD-774/836 ${H774:0:7} (tree ${T774:0:7}; 8-commit chain 4c9b0d3 -> 2566713 -> e884516 -> f1a2e76 -> 278afc2 -> 115a775; 360cd82 counts-only forward merge); predicted verify $PRED; lock tool ${INST_NOW:0:12}…; c57 ${C57_NOW:0:12}…; c133 ${C133_NOW:0:12}…; READY copy sha256 matches; Chrome ${CHV:-?}; model $MODEL"
if [ "$STAMP_OK" = "0" ] || [ "$ROUTE_OK" = "0" ] || [ "$LOCK_OK" = "0" ]; then
  echo "guards pass ($GUARDS); stamp, gate-28 lock release and/or route NOT complete." >&2
  echo "  $SUMMARY" >&2
  [ -z "$PROVISIONAL" ] || echo "  PROVISIONAL (unstamped slots, --check ran against):$PROVISIONAL" >&2
  echo "  NEG seats (38R, derived live; coordinator pane '$COORD_NAME'):$NEG_DESC" >&2
  [ "$STAMP_OK" = "1" ] || echo "REFUSING (32S): $NSLOT at-sign SLOT placeholder(s) remain in the brief (MAIN pin x2 + tree + landed, REPORT_DATE x2, RULED: T0-T10, the SELF-CHECK line and the Self-check note), or the SELF-CHECK line is not in the fleet's form — the coordinator re-reads end-to-end and stamps them before launch" >&2
  [ "${READY_NAMED:-1}" = "1" ] || echo "REFUSING (32S/READY): the kit does not yet name the READY copy's sha256 $READY_774_SHA (FILL AT STAMP: the coordinator stamps it into the kit; the saved copy is $READY_774)" >&2
  [ "$LOCK_OK" = "1" ] || echo "REFUSING (33L): $LOCK_WHY — ANSWER-24: gate 29 launches when gate 28 frees the jest lock" >&2
  if [ "$ROUTE_OK" = "0" ]; then
    echo "REFUSING (40): no '${ROUTE_NAME}|tuesday-agent@agentmail.to|no' line in $ROUTING — answers to the gate would have no route; Tuesday adds it at stamp (this launcher never writes it)" >&2; exit 40
  fi
  [ "$STAMP_OK" = "1" ] || exit 32
  exit 33
fi

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  origin at $PIN_TS ($LSR_ATTEMPTS ls-remote attempt(s), C-192): main = the stamped pin ${MAIN_SHA:0:12} exactly; the branch at its pin (18); T9 unmounted (18T)"
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

THE MODEL OF THIS SESSION (the --model, models_latest.json levels.opus.model_id): $MODEL.
WRITE YOUR ONE REPORT TO: $REPORT
VERIFIED BY THE LAUNCHER AT $PIN_TS (git ls-remote origin, read-only, $LSR_ATTEMPTS attempt(s) under C-192): refs/heads/main = $M_ORIGIN = the stamped MAIN pin (tree $M0_TREE; its ancestry carries 888203c, 7700caf, 39653db and d463f881; PR #97's commits are not on it; what landed since d463f881 per the stamp: $S_LANDED; MODE $MODE — mode 0 means the gated tree is the head itself, otherwise T0's stamped mode (a) or (b) applies); refs/heads/$B774 = $H774 (tree $T774). Predicted verify: $PRED (arithmetic only; your verify decides). The legacy stdout-only merge-tree of 63bef65 and 7700caf shows conflict markers in the counts file ONLY. The T9 is unmounted. Gate 28 holds nothing on the jest lock. The installed lock tool $LOCKTOOL sha256 $INST_NOW equals the pin and NEXUSAI_LOCK_BASE=$LOCK_BASE_LAPTOP is exported in your environment. The C-57 runner sha256 $C57_NOW and the C-133 tool sha256 $C133_NOW equal their pins. The READY copy's sha256 equals the drafter's. These are the start-of-gate pins; take your own three readings anyway.
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
