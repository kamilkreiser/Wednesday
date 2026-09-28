#!/bin/bash
# launch_qa_vision_gate14.sh — cross-project QA agent, ONE batched gate (Vision gate 14; drafted 2026-09-29 06:5x-07:2x AEST from the gate-13
# launcher) on Datasec/Vision_Sales_Portal: SEVEN targets, all TIER 2 (through-code), SEVEN verdicts plus one merged-tree line:
#   VSP76  vsp-76-dead-client-handoff         f593e38  db.js guard(): a connection-class failure marks the client BROKEN          (G11-F1)
#   VSP77  vsp-77-session-index-test-hygiene  da62873  TEST FILE ONLY: random boot-role password; a pairs cell pins WHEN OTHERS  (G11-P1/P2)
#   VSP78  vsp-78-restore-role-boot           1de6d92  schema.sql indexes guarded by to_regclass (15 soft, rule_key hard) + access (G11-M1)
#   VSP79  vsp-79-mixed-case-sequence         241b8bb  backup-db quotes sequence names (route 500 -> 200)                          (G11-O3)
#   VSP80  vsp-80-supertest-loopback          28adf36  TEST HARNESS ONLY: every supertest app served on 127.0.0.1
#   VSP82  vsp-82-dispatch-cutoff             ccfc7ef  dispatchDue() cutoff = NOW()::text, compared as timestamptz                 (G12-F1)
#   VSP85  vsp-85-backup-test-gaps            b78d2e3  TEST FILES ONLY: backup census + row-SELECT stub fault                        (G12-O3/O4)
#
# Main is 6dbffdf (110bb03 = gate 13's VSP-75 GO head, fast-forwarded per C-08, + a BACKLOG-only commit). Every target is linear on 6dbffdf, no
# merges, 0 behind. 23 files in all; exactly two are shared (server/routes/admin.js: VSP78 x VSP79; test/db/backup-coverage.test.js: VSP80 x
# VSP85). Main may since have moved ONLY to a descendant of 6dbffdf that touches none of the targets' files (NOTE).
#
# THE HEADS LIVE IN ONE PLACE: the brief's PIN-HEADS table. This launcher PARSES it, refuses any placeholder, verifies every row against the
# object store and against origin by `git ls-remote` NOW, and appends the verified table to the agent's prompt. The only shas it carries are
# GATED ANCHORS: main 6dbffdf and its parent 110bb03, gate 13's 4813e5f and e59232e (on main), the exact non-merge chains, and c74d7fd (VSP78's
# superseded READY head, 1de6d92's parent).
#
# PRODUCTION IS LIVE for this project (datasec-sales-portal-rg). The gate is local Postgres only. Findings only.
#
# GUARDS RE-DERIVED from launch_qa_vision_gate13.sh (kept as the template, untouched). Differences:
#   - PIN: eight rows (MAIN-P 6dbffdf; VSP76 x2, VSP77 x1, VSP78 x3, VSP79 x1, VSP80 x1, VSP82 x1, VSP85 x1, each base 6dbffdf); NO merges (exit 9).
#   - exit 80 (NEW, replaces any merge-tree): the 21-pair OVERLAP MATRIX over each pair's merge-base is exactly the two named shared files and
#     nothing else, and no target touches BACKLOG.md.
#     This launcher runs NO merge-tree: merge-tree --write-tree writes objects into the repo's .git, which the drafter/launcher may not do. The
#     gate measures the merge from its OWN object dir.
#   - exit 74: per-target content at the pinned shas (BROKEN mark and release; 15 soft + 1 hard index block, no IF NOT EXISTS index left,
#     reportAccess; quoteIdent in the sequence loop; NOW()::text cutoff; serve() on 127.0.0.1 and no deleted assert in VSP80; random password
#     and the pairs cell in VSP77; VSP85's cells and assert lines kept); main still carries each defect (the red is reachable); VSP78's product
#     blobs = c74d7fd's.
#   - exit 31: READYs by their BLUF sha12 and NOT TESTED blocks carried verbatim; CLARIFICATIONS C-10 (names 1de6d92); gate 11/12/13 reports and
#     the tools the brief names; gate 11's qa-g11-n1-child.cjs and qa-g11-stallproxy.cjs pinned by sha1.
#   - exit 38: negative-control seats read 06:49:33 AEST (Tuesday 40885, NexusAI P 20317, QA/NexusAI-batch8 19866).
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/Vision-gate14' "bash '<this file>'"), NEVER nohup.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Contains a legitimate `cd` (into the QA project, at exec).
# READ-ONLY toward the repo: only cat-file, rev-parse, merge-base, log, rev-list, diff, show, ls-remote.
# --check is READ-ONLY: it runs every guard and exits before any identity dir is made or any agent is started.
# Usage: launch_qa_vision_gate14.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..80 a guard refused
set -u
CHECK=0
for a in "$@"; do
  case "$a" in
    --check) CHECK=1 ;;
    *) echo "unknown argument: $a" >&2; exit 2 ;;
  esac
done

# Placeholder comparands, BUILT BY CONCATENATION so a sed of the placeholder text cannot reach them.
PH_STAMP='@STA''MP@'
PH_NODE20='TUESDAY''-DECIDES'

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEFS="$TUE/2_Project_Files/fleet/qa-agent/briefs"
BRIEF="$BRIEFS/2026-09-29_vision-gate14-seven-targets.md"
READY76="$BRIEFS/2026-09-29_vision-vsp76-READY-mail.txt"
READY77="$BRIEFS/2026-09-29_vision-vsp77-READY-mail.txt"
READY78="$BRIEFS/2026-09-29_vision-vsp78-READY-mail.txt"
READY78N="$BRIEFS/2026-09-29_vision-vsp78-newhead-READY-mail.txt"
READY79="$BRIEFS/2026-09-29_vision-vsp79-READY-mail.txt"
READY80="$BRIEFS/2026-09-29_vision-vsp80-READY-mail.txt"
READY82="$BRIEFS/2026-09-29_vision-vsp82-READY-mail.txt"
READY85="$BRIEFS/2026-09-29_vision-vsp85-READY-mail.txt"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
VSP='/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal'
P_REPO="$VSP/2_Project_Files"
CLAR="$VSP/1_Project_Definition/CLARIFICATIONS.md"
REPORTS="$QA_DIR/projects/vision/reports"
G11_DIR="$REPORTS/2026-09-28-vision-gate11-five-targets"
G12_DIR="$REPORTS/2026-09-28-vision-gate12-three-targets"
G13_DIR="$REPORTS/2026-09-28-vision-gate13-vsp74r2-vsp75"
G11_TOOLS="$G11_DIR/evidence/tools"
G12_TOOLS="$G12_DIR/evidence/tools"
G13_TOOLS="$G13_DIR/evidence/tools"
G13_FLOOR="$G13_TOOLS/qa-floorcount.py"
REPORT="$REPORTS/2026-09-29-vision-gate14-seven-targets/report.md"
ROUTE_NAME='QA/Vision-gate14'
NEG_SEATS='40885 20317 19866'   # Tuesday (%0), NexusAI P (%22), QA/NexusAI-batch8 (%45) — read 06:49:33 AEST (the Vision seat 93533 / %44 is LIVE)
G11_CHILD_SHA1='39044865e0f4aff2f08d242dcbd30c1b71530b9e'   # gate 11's qa-g11-n1-child.cjs (the VSP-76 red cell), same bytes in gate 12's folder
G11_PROXY_SHA1='61681e54971c117dc815af8589170eee45efddb2'   # gate 11's qa-g11-stallproxy.cjs (forked by the child)
# Gated anchors (not heads).
ANCHOR_MAIN='6dbffdf36c98aac74d32eaae16e4563966cef42c'     # main now: 110bb03 + BACKLOG follow-up (C-08)
ANCHOR_MAIN_P='110bb03747d4c306810eeb610387aafecc7d394a'   # its single parent: gate 13's VSP-75 GO head
G13_H74='4813e5f5c949d638d8aa82ce282b778d55dedced'         # VSP-74 round 2 (merged inside 110bb03)
G12_MAIN='e59232e1983cd9424b749cd5fea518838763f90f'        # main at gate 13
R78_PREV='c74d7fdaa196b7a921166c0e35dd1082acb61044'        # VSP78's superseded READY head (1de6d92's parent)
CHAIN76='79ec3cd1874214a5c4345972fc79b38bbd14de00 f593e38198e6110c6013d24644611b341cc8754e'
CHAIN78='788477f99b5cd9e4e3e8d8eea94dcf71d9b812d5 c74d7fdaa196b7a921166c0e35dd1082acb61044 1de6d92f67cd4db5b568fcb6de0b60127c408b99'
CHAIN77='da6287321b3c0ce6561e4601d70661469081d73c'
CHAIN79='241b8bb646a401f04eeab2d8be87f0ca18f72885'
CHAIN80='28adf36579ed0136df38c2e1bbe132caf44823fb'
CHAIN82='ccfc7ef60c4421847755a3ce7f5afc866b60263b'
CHAIN85='b78d2e314b6a930d897ed4b5986431d4139962f3'
H_EXPECT76='f593e38198e6110c6013d24644611b341cc8754e'
H_EXPECT77='da6287321b3c0ce6561e4601d70661469081d73c'
H_EXPECT78='1de6d92f67cd4db5b568fcb6de0b60127c408b99'
H_EXPECT79='241b8bb646a401f04eeab2d8be87f0ca18f72885'
H_EXPECT80='28adf36579ed0136df38c2e1bbe132caf44823fb'
H_EXPECT82='ccfc7ef60c4421847755a3ce7f5afc866b60263b'
H_EXPECT85='b78d2e314b6a930d897ed4b5986431d4139962f3'
LOCK_BLOB='9d426df'; PKG_BLOB='d3b76fb'; CI_BLOB='0cb2d05'
# Every file any target changes: main may move only in files outside this set.
DELTA_FILES='server/db.js server/db.test.js test/db/checkout-link-death.child.js test/db/checkout-link-death.test.js test/db/session-index-boot.test.js
server/schema.sql server/initDb.js server/routes/admin.js test/db/restore-role-boot.test.js test/db/backup-db-sequence-names.test.js test/loopback.js
test/db/loopback.test.js test/db/helpers.js server/errors.test.js test/db/async-faults.test.js test/db/backup-dump-replay.test.js
test/db/completed-response.test.js test/db/concurrency.test.js test/db/routes.test.js server/reminders/dispatcher.js test/db/dispatch-cutoff.test.js
server/dbBackup.test.js test/db/backup-coverage.test.js'
# The only shared files (pair -> file). Every other pair must be path-disjoint.
OVERLAP_78_79='server/routes/admin.js'
OVERLAP_80_85='test/db/backup-coverage.test.js'

SUBJECT_STEM='[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 14'
QUESTION_SUBJ='[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>'
ANSWER_PREFIX='[Tuesday -> QA/Vision-gate14] ANSWER'

p() { git --no-optional-locks -C "$P_REPO" "$@"; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE batched gate (Vision gate 14) on Datasec/Vision_Sales_Portal: SEVEN targets, all TIER 2 (through-code), SEVEN verdicts (GO or NO-GO each) plus one merged-tree line, in the SALES PORTAL repo. Portal main is 6dbffdf (gate 13's VSP-75 GO head 110bb03, fast-forwarded, plus a BACKLOG-only commit). Every target is ROUND 1 of its own ticket and sits linearly on 6dbffdf. They change 23 files; exactly two are shared (server/routes/admin.js by VSP78 and VSP79; test/db/backup-coverage.test.js by VSP80 and VSP85); none touches BACKLOG.md. THE MERGED TREE OF ALL SEVEN ON MAIN IS THE KEY MEASUREMENT.

READ YOUR COMMISSION FIRST, whole: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-29_vision-gate14-seven-targets.md
Then read the charter it names, the Vision CLARIFICATIONS (whole; C-10 records Tuesday's three VSP-78 rulings, C-09 production's idle_in_transaction_session_timeout, C-08 why main is 6dbffdf), the project's CLAUDE.md (/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/CLAUDE.md; its deploy commands are not for you), the eight READY mails under test beside the brief (2026-09-29_vision-vsp76-, -vsp77-, -vsp78-, -vsp78-newhead-, -vsp79-, -vsp80-, -vsp82- and -vsp85-READY-mail.txt), and the earlier gates' reports the brief names: gate 11 /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-28-vision-gate11-five-targets (VSP66-G11-F1, VSP71-G11-P1 and P2, G11-M1, G11-O3, N1.2, N1.3, N2.8, N2.9, N6.4, N6.6), gate 12 /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-28-vision-gate12-three-targets (VSP69-G12-F1, N3, VSP75-G12-O3 and O4), gate 13 /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-28-vision-gate13-vsp74r2-vsp75 (instruments, self-findings, floor). Every builder statement is a CLAIM, never evidence. RE-DERIVE every red, every mutant and every suite set yourself. Verify every PRIOR WORK claim against git history and the earlier gates' evidence, never against the brief.

THE TARGETS.
  VSP76 (TIER 2, through-code) = Jira VSP-76 = gate 11's VSP66-G11-F1, at f593e38. server/db.js guard(): a query that rejects with severity FATAL, SQLSTATE class 57P or 08, or on a client pg reads as unqueryable, marks the client BROKEN, and release passes err || TIMED_OUT || BROKEN so pg-pool discards it. THE RED CELL IS GATE 11'S OWN TOOL qa-g11-n1-child.cjs, modes window:terminate:immediate:product and window:terminate:immediate:max1, N=20, main 6dbffdf as the positive control. It cannot run unmodified for you (it refuses any DB not named vsp_qa_g11_* and loads pg from gate 11's work-g11): copy it and qa-g11-stallproxy.cjs (sha1-pinned in the brief), change exactly the WK path and the DB regex to vsp_qa_g14_, prove by diff nothing else changed, and never create a vsp_qa_g11_* database. The builder's vsp_qa_g11_7609291_test is the builder's, never yours.
  VSP77 (TIER 2, through-code, TEST FILE ONLY) = Jira VSP-77 = gate 11's VSP71-G11-P1 and P2, at da62873. The session-index boot test's role password is random per run, and a new pairs cell pins WHEN OTHERS. Re-derive gate 11's mutant M5 independently: it must survive main's old file and fail the new cell, on the head and on the merged tree.
  VSP78 (TIER 2, through-code) = Jira VSP-78 = gate 11's G11-M1, at 1de6d92 (product files identical to its superseded READY head c74d7fd; the new head changes the test teardown only). schema.sql guards 16 indexes with to_regclass; 15 fail soft; idx_reminders_rule_key does not: missing and unmakeable must still fail the boot, and that is the REQUIRED CELL. initDb prints ONE access line naming every public table and sequence the portal's role cannot use: Tuesday ACCEPTED the WARN shape (C-10 ruling 1); whether the access line fires correctly is your question. The test drops its own fixtures (C-10 ruling 2); the feedbackDigest index is VSP-88 (out of scope). Also: the other-role replay of the REAL backup-db dump, the VSP-71 cells, the all-indexes-missing pairs arm, the held write cell, the search_path shadow of a to_regclass name.
  VSP79 (TIER 2, through-code; a production-reachable route fix) = Jira VSP-79 = gate 11's G11-O3, at 241b8bb. backup-db quotes sequence names in its catalog lookup and in the dump's setval. Give it a REAL-ROUTE cell with a mixed-case sequence, red on main (500) and 200 at the head, then replay its dump and stress the quoting.
  VSP80 (TIER 2, through-code, TEST HARNESS ONLY) = Jira VSP-80, at 28adf36. Every supertest app is served on 127.0.0.1 before supertest sees it; helpers.closeDb closes the servers. POSITIVE CONTROL: force the hazard in YOUR harness (a preload that moves a wildcard listen(0) onto the port of YOUR decoy already listening on 127.0.0.1): main must reach the decoy, the head must not. The same forced-hazard sweep runs over the merged tree, where VSP-79's new test hands supertest a bare app (the brief's WRONG (t)).
  VSP82 (TIER 2, through-code) = Jira VSP-82 = gate 12's VSP69-G12-F1, at ccfc7ef. dispatchDue() reads NOW()::text and compares due_at <= $1::timestamptz. Its CLIENT REACH NONE is a claim you verify: client reminders on the millisecond grid are decided exactly as at main, and nothing is ever selected before due, including under varied DateStyle and TimeZone on YOUR database only (the brief's WRONG (j) and Tuesday's ruling 2 grade it).
  VSP85 (TIER 2, through-code, TEST FILES ONLY) = Jira VSP-85 = gate 12's VSP75-G12-O3 and O4, at b78d2e3. Re-derive its four mutants M6 to M9 independently (each must die on the new files and survive main's old ones), confirm no cell removed or weakened, sets 0 lost. Its Dependabot note is OUT OF SCOPE: do not read, query or act on it.

WHAT THE BRIEF REQUIRES, in short (the brief is the authority): N1 VSP-76 (window cells, real callers, the classifier table including 25P03 from C-09, VSP-65 and VSP-66 untouched, mutants); N2 VSP-78 (the other-role replay red at main with 42501 must be owner of table leads, THE REQUIRED CELL with its independent controls and the ON CONFLICT consequence under a mutant, the access-line matrix and throw hunt, VSP-71 not regressed, the pairs arm with all indexes missing, the held write cell, the search_path shadow); N3 VSP-79 (the real route 500 to 200, the dump replay with nextval, quote-stressing names); N4 VSP-82 (red at main on the builder's cell and gate 12's 300-run arm, the decision equivalence through the real code path, nothing early through dispatchDue itself, the DateStyle and TimeZone matrix, your ceil-to-millisecond mutant); N5 VSP-80 (the forced hazard at main and head, not weakened); N6 VSP-77 (M5); N7 VSP-85 (M6 to M9 plus yours, the O4 fault on the row SELECT); N8 THE MERGED TREE: the cross-target cells, the merge from YOUR OWN object dir with both shared files shown, the forced-hazard sweep over the merged test:db, SUITES AS SETS, NOT COUNTS vs main 6dbffdf at every head and the merged tree (0 lost), the FIX 2 watcher beside every test:db (never touch salesportal_test_lazy; always set TEST_DATABASE_URL), product-test hygiene for vsp71_ / vsp73_ / vsp78_ names, coverage N=2 per tree run locally (label it NOT CI; CI's line gate is 80%; VSP-82 alone is claimed at 80.65), and the Node 20 leg exactly as the NODE20-LEG line in the brief says (DOCKER-PULL-NEVER).
CI is UNMEASURED: this project's gh is not authenticated and you must not use gh; never claim CI; name CI's Node 22 coverage gate and its e2e:pro step as the first reads at merge. Every red-proof: fresh tree per arm, asserted edits, node --check rc quoted; a red from a mutant that does not parse is VOID.

LOCAL POSTGRES ONLY. PRODUCTION IS LIVE for this project. NEVER the live portal (datasec-sales-portal.azurewebsites.net, datasec-sales-portal-rg, its Postgres datasec-sales-db.postgres.database.azure.com, its key vault): no request, no DB connection, not even a GET. No az of any kind, no deploy, no app-setting change. Never GitHub. Never open a real backup, a production dump or anything under the project's 4_Credentials: every dump you replay is made by the product's own route from YOUR seeded database. Real sends are OFF: ACS is replaced by YOUR recorder; ntfy goes only to YOUR loopback recorder. Never set AZURE_BACKUP_CONN_STR. pg_terminate_backend and pg_cancel_backend only on a backend of YOUR database (prove datname first). Schemas, search_path, DateStyle and TimeZone settings, group roles, revoked grants and any vsp_qa_g14_* role exist only inside your own databases; ALTER DATABASE only on a database you created.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT from the object store (git archive into a fresh mktemp -d under projects/vision/work-g14/). Each tree is EXCLUSIVE to this gate and to one purpose; never touch work/ or work-g2 .. work-g13. Copy the earlier gates' tools into YOUR evidence folder and re-point them (they hard-code work-g11/12/13 and ENFORCE vsp_qa_g11_/g12_/g13_); never run from, edit or write into gate 1-13's copies. Dependencies: npm ci --offline --ignore-scripts only, then prove node_modules/.package-lock.json against the lockfile entry by entry (lockcmp.py AND lockwalk.py). Never npm install, never npm audit, never npx anything not already in the tree. In the repo use ONLY read verbs (show, log, diff, ls-remote, rev-parse, ls-tree, cat-file, grep, merge-base, archive); never fetch, pull, checkout, switch, worktree, commit, stash, reset, clean or gc. Run git merge-tree --write-tree only from the gate's OWN object dir (GIT_OBJECT_DIRECTORY = your own mktemp -d, alternates = the repo's objects), or skip it and say so. Findings-only: no writes in the portal repo, none inside Vision_Sales_Portal, none in gate 1-13's report folders or trees. Never rm: quarantine. Never DROP a database or role. Run every loop and every git show <sha>:<path> under bash. CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY: a control derived from the run it validates is not a control.

FLOOR DISCIPLINE. Vision has no jest lock; never borrow NexusAI's. Never use ports 4848, 8080 or 47787, nor 127.0.0.1:49162 / 49164 / 49166 (a LogiPlugin listener, the VSP-80 cause); take every port from the kernel and bind 127.0.0.1; your decoy is yours, on a kernel port. Never start the portal's own entry point (it binds all interfaces); use the real createApp() and initDb() in your harness. Postgres is the local container on 127.0.0.1:5433, and ONLY databases you create: vsp_qa_g14_<epoch> and vsp_qa_g14_<epoch>_test (the test name MUST end in _test); never salesportal, salesportal_test or salesportal_test_lazy (a Vision seat may be relaunched at any time and uses them), any vsp_qa_g1..g13 database, vsp_qa_g11_7609291_test, the builder's vsp_s0929_*, vsp_bf1_*, vsp_g12r2_* or vsp_fix* databases, or any vsp71_* / vsp73_* / vsp78_* database or role you did not cause. Roles are cluster-global: create one only inside a transaction you roll back, or name it vsp_qa_g14_* and list it; earlier gates' roles are not yours. Never ALTER SYSTEM, never ALTER ROLE on anything you did not create. The module's default URL is the builder's dev database, so give every product process YOUR DATABASE_URL and TEST_DATABASE_URL explicitly and print the database each one reached. Release every lock and direct session you open in a finally. No docker command at all, except the Node 20 exception under the NODE20-LEG line. Every product process runs under env -i with an explicit allowlist, NODE_ENV never production. Never set AGENTMAIL_API_KEY or AGENTMAIL_INBOX in a product process, nor any real ACS_* or MAIL_SENDER, AZURE_BACKUP_CONN_STR, TABLES_CONNECTION_STRING, SALES_COPY_EMAIL, a real NTFY_TOPIC, LEAD_BOT_API_KEY, WEBSITE_SITE_NAME, PGOPTIONS, PGTZ or PGDATESTYLE; print each product process's env KEY NAMES and assert none is forbidden. NTFY_SERVER=http://ntfy.invalid except your loopback recorder; never contact ntfy.sh; stub fetch to throw on any other URL. Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid, with the brief's negative-control seats classifying FOREIGN in the same run. A zero is reportable only beside an ATTACHED control that fired in the same window. Other gates and seats are live on this box: record the load average beside every timing number; a latency result with no load figure is not a measurement.
DEADLINE AND HEARTBEAT: every step has a written DEADLINE built into your runner (there is no timeout binary here) and releases its servers, proxies, recorders, decoys, sessions, locks, roles and children in a finally. Log a HEARTBEAT line at least every 2 minutes; a step with no heartbeat for 5 minutes is aborted and reported, never waited on. Deadlines: one window cell (N=20) 120 s; one boot cell 60 s; a child-process cell 30 s; one test:db file 180 s; a whole test:db run 420 s; one Node 20 container 420 s. Nothing above 420 s.

QUESTIONS: your routing name is QA/Vision-gate14. If you must ask, mail tuesday-agent@agentmail.to with the subject "[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>" and proceed on the safest reading without waiting. Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/Vision-gate14] ANSWER"; read it with your verdict key. Never wednesday-agent@. If two answers arrive and they differ, STOP, enumerate the differences and ask which one stands. If a response is cut off by a safety check, record it and continue with the next item; this is authorised defensive QA of Datasec's own product on loopback. Record every question, reading and answer in the report.

Write your report to: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-29-vision-gate14-seven-targets/report.md

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with a subject beginning exactly:
[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 14: VSP76 @ <sha7> <GO | NO-GO> · VSP77 @ <sha7> <GO | NO-GO> · VSP78 @ <sha7> <GO | NO-GO> · VSP79 @ <sha7> <GO | NO-GO> · VSP80 @ <sha7> <GO | NO-GO> · VSP82 @ <sha7> <GO | NO-GO> · VSP85 @ <sha7> <GO | NO-GO> · merged <CLEAN | CONFLICT>
(each sha7 is the pinned head from the verified table below). Lead the body with seven sentences, one per target, as the brief's section 14 words them, then one line on the merged tree (clean or not, sets 0 lost, the forced-hazard sweep's bare sites, coverage NOT CI, the safe merge order) and one line on the class counts (each is ROUND 1 of its ticket). You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no credentials directory of its own. Use it only in your own mail calls, with a client timeout. Never put the key or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice.

Report every pinned head and main as three timestamped readings (start / mid / end), with the branch name beside each. Include the verbatim operator strings the brief lists: VSP-78's access line and missing-index line as printed, the 42501 text of the required cell, VSP-76's held-client line, main's backup-db error line for the mixed-case sequence and the head's dump lines for it, NOW()::text under each DateStyle you ran, and SELECT version().

Rule 2 stands: what you did NOT test is first-class output. Write a NOT TESTED section that covers at least CI (UNMEASURED), production's roles, owners, search_path, DateStyle, TimeZone, timeouts and sequences, a real production restore by another role, real Azure Blob Storage, ACS and ntfy, Node 22, the container image, e2e:pro, a Linux runner for VSP-80's hazard cell, and every cell you did not run. Label every action recommendation MEASURED AT RUNTIME, PROBED or READ ONLY.
PROMPT_EOF

# ---------------------------------------------------------------- GUARDS
[ -d "$QA_DIR" ]  || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]   || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -n "$PROMPT" ]  || { echo "embedded prompt is empty" >&2; exit 4; }
[ -d "$P_REPO/.git" ] || [ -f "$P_REPO/.git" ] || { echo "repo under test missing: $P_REPO" >&2; exit 5; }

# 40 — parse the PIN table from the brief (the ONLY source of heads). Output: id repo branch head base commits status (TAB).
PIN="$(python3 - "$BRIEF" <<'PY'
import sys, re
s = open(sys.argv[1], encoding='utf-8').read()
m = re.search(r'<!-- PIN-HEADS:BEGIN -->(.*?)<!-- PIN-HEADS:END -->', s, re.S)
if not m:
    print('NO-BLOCK'); sys.exit(0)
for line in m.group(1).splitlines():
    line = line.strip()
    if not line.startswith('|') or line.startswith('| id ') or set(line) <= set('|-: '):
        continue
    cells = [c.strip().strip('`') for c in line.strip('|').split('|')]
    print('\t'.join(cells))
PY
)"
[ "$PIN" != "NO-BLOCK" ] && [ -n "$PIN" ] || { echo "REFUSING: the brief has no PIN-HEADS block — the heads have nowhere to come from" >&2; exit 40; }
TARGETS='VSP76 VSP77 VSP78 VSP79 VSP80 VSP82 VSP85'
EXPECT_IDS="MAIN-P $TARGETS"
for ID in $EXPECT_IDS; do
  N="$(printf '%s\n' "$PIN" | awk -F'\t' -v id="$ID" '$1==id' | wc -l | tr -d ' ')"
  [ "$N" = "1" ] || { echo "REFUSING: PIN table must carry exactly one row '$ID' (found $N)" >&2; exit 40; }
done
[ "$(printf '%s\n' "$PIN" | wc -l | tr -d ' ')" = "8" ] || { echo "REFUSING: PIN table carries rows beyond the eight expected ($EXPECT_IDS)" >&2; exit 40; }
row()   { printf '%s\n' "$PIN" | awk -F'\t' -v id="$1" '$1==id'; }
fld()   { row "$1" | awk -F'\t' -v n="$2" '{print $n}'; }   # 2 repo 3 branch 4 head 5 base 6 commits 7 status
is40()  { printf '%s' "$1" | grep -Eq '^[0-9a-f]{40}$'; }
for ID in $EXPECT_IDS; do
  R="$(row "$ID")"; ST="$(fld "$ID" 7)"
  [ "$(printf '%s\n' "$R" | awk -F'\t' '{print NF}')" = "7" ] || { echo "REFUSING: PIN row $ID does not have 7 cells: $R" >&2; exit 40; }
  [ "$ST" = "IN" ] || { echo "REFUSING: PIN row $ID status is '$ST' — IN only" >&2; exit 40; }
  printf '%s' "$R" | grep -q '@' && { echo "REFUSING: PIN row $ID still carries a placeholder: $R" >&2; exit 40; }
  is40 "$(fld "$ID" 4)" || { echo "REFUSING: PIN row $ID head is not a 40-hex sha: '$(fld "$ID" 4)'" >&2; exit 40; }
  [ "$(fld "$ID" 2)" = "portal" ] || { echo "REFUSING: PIN row $ID repo must be portal" >&2; exit 40; }
done
[ "$(fld MAIN-P 3)" = "main" ] || { echo "REFUSING: row MAIN-P branch must be main" >&2; exit 40; }
branch_of() { case "$1" in
  VSP76) echo 'vsp-76-dead-client-handoff' ;;
  VSP77) echo 'vsp-77-session-index-test-hygiene' ;;
  VSP78) echo 'vsp-78-restore-role-boot' ;;
  VSP79) echo 'vsp-79-mixed-case-sequence' ;;
  VSP80) echo 'vsp-80-supertest-loopback' ;;
  VSP82) echo 'vsp-82-dispatch-cutoff' ;;
  VSP85) echo 'vsp-85-backup-test-gaps' ;;
esac; }
expect_of() { case "$1" in VSP76) echo "$H_EXPECT76" ;; VSP77) echo "$H_EXPECT77" ;; VSP78) echo "$H_EXPECT78" ;; VSP79) echo "$H_EXPECT79" ;;
                           VSP80) echo "$H_EXPECT80" ;; VSP82) echo "$H_EXPECT82" ;; VSP85) echo "$H_EXPECT85" ;; esac; }
chain_of()  { case "$1" in VSP76) printf '%s\n' $CHAIN76 ;; VSP77) printf '%s\n' $CHAIN77 ;; VSP78) printf '%s\n' $CHAIN78 ;; VSP79) printf '%s\n' $CHAIN79 ;;
                           VSP80) printf '%s\n' $CHAIN80 ;; VSP82) printf '%s\n' $CHAIN82 ;; VSP85) printf '%s\n' $CHAIN85 ;; esac | sort; }
for ID in $TARGETS; do
  [ "$(fld "$ID" 3)" = "$(branch_of "$ID")" ] || { echo "REFUSING: row $ID branch is '$(fld "$ID" 3)', the brief's target is $(branch_of "$ID") — re-brief" >&2; exit 40; }
  is40 "$(fld "$ID" 5)" || { echo "REFUSING: PIN row $ID base is not a 40-hex sha" >&2; exit 40; }
  printf '%s' "$(fld "$ID" 6)" | grep -Eq '^[1-9][0-9]*$' || { echo "REFUSING: PIN row $ID commits '$(fld "$ID" 6)' is not a positive integer" >&2; exit 40; }
  [ "$(fld "$ID" 4)" = "$(expect_of "$ID")" ] || { echo "REFUSING: $ID's PIN head $(fld "$ID" 4 | cut -c1-7) is not the head this launcher's chains are pinned to ($(expect_of "$ID" | cut -c1-7)); re-brief" >&2; exit 40; }
done
MAINH="$(fld MAIN-P 4)"

# 6 — every sha the guards use is a commit in the local object store (this launcher never fetches).
for S in "$MAINH" "$ANCHOR_MAIN" "$ANCHOR_MAIN_P" "$G13_H74" "$G12_MAIN" "$R78_PREV" $CHAIN76 $CHAIN77 $CHAIN78 $CHAIN79 $CHAIN80 $CHAIN82 $CHAIN85; do
  T="$(p cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in the portal repo (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 9m — MAIN: 6dbffdf, or a descendant of it whose diff from 6dbffdf touches none of the targets' files.
main_ok() {   # $1 = sha; prints the offending files and returns 1 if it moved in a delta file
  p merge-base --is-ancestor "$ANCHOR_MAIN" "$1" 2>/dev/null || { echo "(not a descendant of 6dbffdf)"; return 1; }
  [ "$1" = "$ANCHOR_MAIN" ] && return 0
  local HIT; HIT="$(p diff --name-only "$ANCHOR_MAIN" "$1" 2>/dev/null | grep -xF -f <(printf '%s\n' $DELTA_FILES))"
  [ -z "$HIT" ] || { printf '%s\n' "$HIT"; return 1; }
  return 0
}
OUT="$(main_ok "$MAINH")" || { echo "REFUSING: the pinned MAIN ${MAINH:0:7} is not 6dbffdf or a descendant that leaves the targets' files alone: $OUT — re-brief" >&2; exit 9; }
STALE=''
[ "$MAINH" = "$ANCHOR_MAIN" ] || { STALE=' (main pinned past 6dbffdf: the gate re-derives the merge)'; echo "NOTE: pinned MAIN ${MAINH:0:7} is a descendant of 6dbffdf touching none of the delta files" >&2; }

# 7 / 8 — each target: base 6dbffdf, ancestor AND merge-base with MAIN, not on main, exact count, 0 behind 6dbffdf.
for ID in $TARGETS; do
  H="$(fld "$ID" 4)"; BASE="$(fld "$ID" 5)"; N="$(fld "$ID" 6)"; H7="${H:0:7}"
  [ "$BASE" = "$ANCHOR_MAIN" ] || { echo "REFUSING: row $ID base ${BASE:0:7} is not 6dbffdf — re-brief" >&2; exit 7; }
  p merge-base --is-ancestor "$BASE" "$H" 2>/dev/null || { echo "REFUSING: $ID base ${BASE:0:7} is not an ancestor of $H7" >&2; exit 7; }
  [ "$(p merge-base "$H" "$MAINH" 2>/dev/null)" = "$BASE" ] || { echo "REFUSING: $ID merge-base(head, MAIN) is not its base ${BASE:0:7}" >&2; exit 7; }
  p merge-base --is-ancestor "$H" "$MAINH" 2>/dev/null \
    && { echo "REFUSING: $ID $H7 is ALREADY ON MAIN ${MAINH:0:7} — the brief says it is not; re-brief" >&2; exit 7; }
  GOTN="$(p rev-list --count "${BASE}..${H}" 2>/dev/null)"
  [ "$GOTN" = "$N" ] || { echo "REFUSING: $ID $H7 has $GOTN commits over its base, the table says $N" >&2; p log --format='%h %p %s' "${BASE}..${H}" >&2; exit 8; }
  [ "$(p rev-list --count "${H}..${ANCHOR_MAIN}" 2>/dev/null)" = "0" ] || { echo "REFUSING: $ID $H7 is behind 6dbffdf" >&2; exit 7; }
done

# 9 — gated anchors, exact chains, NO merges.
[ "$(p log -1 --format='%P' "$ANCHOR_MAIN" 2>/dev/null)" = "$ANCHOR_MAIN_P" ] || { echo "REFUSING: 6dbffdf's single parent is not 110bb03 — re-brief" >&2; exit 9; }
[ "$(p diff --name-only "$ANCHOR_MAIN_P" "$ANCHOR_MAIN" 2>/dev/null | tr '\n' ' ')" = "BACKLOG.md " ] || { echo "REFUSING: 110bb03..6dbffdf touches more than BACKLOG.md — re-brief" >&2; exit 9; }
for S in "$ANCHOR_MAIN_P" "$G13_H74" "$G12_MAIN"; do
  p merge-base --is-ancestor "$S" "$MAINH" 2>/dev/null || { echo "REFUSING: anchor ${S:0:7} (110bb03 / 4813e5f / e59232e) is not on main ${MAINH:0:7} — re-brief" >&2; exit 9; }
done
[ "$(p log -1 --format='%P' "$H_EXPECT78")" = "$R78_PREV" ] || { echo "REFUSING: VSP78 1de6d92's parent is not c74d7fd (the superseded READY head)" >&2; exit 9; }
for ID in $TARGETS; do
  H="$(fld "$ID" 4)"; BASE="$(fld "$ID" 5)"
  [ "$(p rev-list --no-merges "${BASE}..${H}" 2>/dev/null | sort)" = "$(chain_of "$ID")" ] || { echo "REFUSING: $ID's non-merge commits over ${BASE:0:7} are not exactly the pinned chain. Got:" >&2; p rev-list --no-merges "${BASE}..${H}" >&2; exit 9; }
  [ "$(p rev-list --merges "${BASE}..${H}" 2>/dev/null | wc -l | tr -d ' ')" = "0" ] || { echo "REFUSING: $ID carries a merge over 6dbffdf — the brief says linear" >&2; exit 9; }
done

# 18 — RE-PIN: every row at origin, by ls-remote, read NOW (immediately before launch). Main may have moved harmlessly (NOTE).
ORIGIN_MAIN_NOTE=''
for ID in $EXPECT_IDS; do
  BR="$(fld "$ID" 3)"; H="$(fld "$ID" 4)"
  L="$(p ls-remote origin "refs/heads/$BR" 2>&1)"
  if printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$"; then continue; fi
  if [ "$ID" = "MAIN-P" ]; then
    NOW="$(printf '%s\n' "$L" | awk -v r="refs/heads/$BR" '$2==r {print $1}')"
    is40 "$NOW" || { echo "REFUSING: cannot read origin main: ${L:-<nothing>}" >&2; exit 18; }
    [ "$(p cat-file -t "$NOW" 2>/dev/null)" = "commit" ] || { echo "REFUSING: origin main moved to ${NOW:0:7}, which is not in the local object store — this launcher never fetches; Tuesday re-reads and re-pins" >&2; exit 18; }
    p merge-base --is-ancestor "$H" "$NOW" 2>/dev/null || { echo "REFUSING: origin main ${NOW:0:7} does not contain the pinned main ${H:0:7} — re-pin" >&2; exit 18; }
    OUT="$(main_ok "$NOW")" || { echo "REFUSING: origin main moved to ${NOW:0:7}, touching the targets' files: $OUT — re-pin and re-brief" >&2; exit 18; }
    ORIGIN_MAIN_NOTE="origin main is now ${NOW:0:7}, a descendant of the pinned ${H:0:7} touching none of the delta files (NOTE; the gate re-derives the merge)"
    echo "NOTE: $ORIGIN_MAIN_NOTE" >&2
    continue
  fi
  echo "REFUSING: row $ID: $H is not at refs/heads/$BR on origin — that head moved or was never pushed; re-pin" >&2; printf '%s\n' "${L:-<nothing>}" >&2; exit 18
done
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — exact file sets.
fileset() { case "$1" in
  VSP76) printf '%s\n' server/db.js server/db.test.js test/db/checkout-link-death.child.js test/db/checkout-link-death.test.js ;;
  VSP77) printf '%s\n' test/db/session-index-boot.test.js ;;
  VSP78) printf '%s\n' server/initDb.js server/routes/admin.js server/schema.sql test/db/restore-role-boot.test.js ;;
  VSP79) printf '%s\n' server/routes/admin.js test/db/backup-db-sequence-names.test.js ;;
  VSP80) printf '%s\n' server/errors.test.js test/db/async-faults.test.js test/db/backup-coverage.test.js test/db/backup-dump-replay.test.js \
                       test/db/completed-response.test.js test/db/concurrency.test.js test/db/helpers.js test/db/loopback.test.js test/db/routes.test.js test/loopback.js ;;
  VSP82) printf '%s\n' server/reminders/dispatcher.js test/db/dispatch-cutoff.test.js ;;
  VSP85) printf '%s\n' server/dbBackup.test.js test/db/backup-coverage.test.js ;;
esac; }
for ID in $TARGETS; do
  H="$(fld "$ID" 4)"; BASE="$(fld "$ID" 5)"
  GOT="$(p diff --name-only "$BASE" "$H" 2>/dev/null | sort)"
  [ "$GOT" = "$(fileset "$ID" | sort)" ] || { echo "REFUSING: $ID ${H:0:7}'s delta over its base is not exactly the briefed file set. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }
done
[ "$(p diff --name-only "$R78_PREV" "$H_EXPECT78" 2>/dev/null | tr '\n' ' ')" = "test/db/restore-role-boot.test.js " ] \
  || { echo "REFUSING: c74d7fd..1de6d92 touches more than the test file — the new-head READY says teardown only" >&2; exit 22; }

# 80 — THE OVERLAP MATRIX (replaces any merge-tree run: this launcher never writes objects into the repo). Every pair, over its merge-base:
#      exactly the two named shared files, nothing else; no target touches BACKLOG.md.
allowed_overlap() { case "$1 $2" in "VSP78 VSP79") echo "$OVERLAP_78_79" ;; "VSP80 VSP85") echo "$OVERLAP_80_85" ;; *) echo '' ;; esac; }
N_OVL=0
set -- $TARGETS
for A in "$@"; do for B in "$@"; do
  [[ "$A" < "$B" ]] || continue
  HA="$(fld "$A" 4)"; HB="$(fld "$B" 4)"; MB="$(p merge-base "$HA" "$HB" 2>/dev/null)"
  is40 "$MB" || { echo "REFUSING: no merge-base for $A x $B" >&2; exit 80; }
  I="$(comm -12 <(p diff --name-only "$MB" "$HA" | sort) <(p diff --name-only "$MB" "$HB" | sort) | tr '\n' ' ' | sed 's/ $//')"
  [ "$I" = "$(allowed_overlap "$A" "$B")" ] || { echo "REFUSING: $A x $B overlap over ${MB:0:7} is '${I:-<none>}', the brief says '$(allowed_overlap "$A" "$B")' — re-brief" >&2; exit 80; }
  [ -z "$I" ] || N_OVL=$((N_OVL+1))
done; done
[ "$N_OVL" = "2" ] || { echo "REFUSING: the overlap matrix has $N_OVL shared-file pairs, the brief says 2" >&2; exit 80; }
for ID in $TARGETS; do
  p diff --name-only "$(fld "$ID" 5)" "$(fld "$ID" 4)" | grep -qxF 'BACKLOG.md' && { echo "REFUSING: $ID touches BACKLOG.md — the brief says none does" >&2; exit 80; }
done

# 74 — per-target content, read from the pinned shas (never a checkout).
has() { p show "${1}:${2}" 2>/dev/null | grep -qF -- "$3"; }   # sha path fixed-string
must() { has "$1" "$2" "$3" || { echo "REFUSING: ${1:0:7}:$2 lacks '$3' — the brief gates different code; re-brief" >&2; exit 74; }; }
mustnot() { has "$1" "$2" "$3" && { echo "REFUSING: ${1:0:7}:$2 still carries '$3' — the brief's reading is wrong; re-brief" >&2; exit 74; }; return 0; }
ntests() { p show "${1}:${2}" 2>/dev/null | grep -c '^test('; }
wantn() { [ "$(ntests "$1" "$2")" = "$3" ] || { echo "REFUSING: ${1:0:7}:$2 carries $(ntests "$1" "$2") top-level test( cells, the brief says $3" >&2; exit 74; }; }
blob() { p rev-parse "${1}:${2}" 2>/dev/null; }
keeps_tests() {   # $1 old sha, $2 new sha, $3 path: every top-level test( line of old is a line of new
  while IFS= read -r T; do
    [ -n "$T" ] || continue
    p show "${2}:${3}" | grep -qxF -- "$T" || { echo "REFUSING: ${2:0:7}:$3 dropped or renamed the cell: $T" >&2; exit 74; }
  done <<< "$(p show "${1}:${3}" | grep '^test(')"
}
H76="$(fld VSP76 4)"; H77="$(fld VSP77 4)"; H78="$(fld VSP78 4)"; H79="$(fld VSP79 4)"; H80="$(fld VSP80 4)"; H82="$(fld VSP82 4)"; H85="$(fld VSP85 4)"
# VSP76: the BROKEN mark and the discard; main lacks it (the red is reachable).
must "$H76" server/db.js "const BROKEN = Symbol('vsp76.broken');"
must "$H76" server/db.js "if (err.severity === 'FATAL') return true;"
must "$H76" server/db.js "return typeof err.code === 'string' && (err.code.startsWith('57P') || err.code.startsWith('08'));"
must "$H76" server/db.js 'if (!client[BROKEN] && isConnectionError(err, client)) client[BROKEN] = err;'
must "$H76" server/db.js 'return release.call(this, err || client[TIMED_OUT] || client[BROKEN]);'
must "$ANCHOR_MAIN" server/db.js 'return release.call(this, err || client[TIMED_OUT]);'
mustnot "$ANCHOR_MAIN" server/db.js 'BROKEN'
wantn "$H76" server/db.test.js 7
wantn "$H76" test/db/checkout-link-death.test.js 13
keeps_tests "$ANCHOR_MAIN" "$H76" server/db.test.js
keeps_tests "$ANCHOR_MAIN" "$H76" test/db/checkout-link-death.test.js
[ "$(p diff --numstat "$ANCHOR_MAIN" "$H76" -- test/db/checkout-link-death.test.js | awk '{print $2}')" = "0" ] \
  || { echo "REFUSING: VSP76 deleted lines in checkout-link-death.test.js — the brief says +57/-0" >&2; exit 74; }
# VSP78: 15 soft blocks + the hard rule_key block; no IF NOT EXISTS index statement left; the access and missing-index lines; main carries the defect.
N_SOFT="$(p show "${H78}:server/schema.sql" | grep -c "EXCEPTION WHEN OTHERS THEN RAISE WARNING 'idx_")"
[ "$N_SOFT" = "15" ] || { echo "REFUSING: VSP78 schema.sql carries $N_SOFT fail-soft index blocks, the brief says 15" >&2; exit 74; }
N_REGEX="$(p show "${H78}:server/schema.sql" | grep -oE "to_regclass\('[A-Za-z0-9_]+'\) IS NULL THEN CREATE INDEX" | wc -l | tr -d ' ')"
[ "$N_REGEX" = "15" ] || { echo "REFUSING: VSP78 initDb's name regex would match $N_REGEX blocks, the brief says 15" >&2; exit 74; }
must "$H78" server/schema.sql "DO \$\$ BEGIN IF to_regclass('idx_reminders_rule_key') IS NULL THEN CREATE UNIQUE INDEX idx_reminders_rule_key ON reminders(rule_key) WHERE rule_key IS NOT NULL; END IF; END \$\$;"
mustnot "$H78" server/schema.sql 'CREATE INDEX IF NOT EXISTS idx_'
mustnot "$H78" server/schema.sql 'CREATE UNIQUE INDEX IF NOT EXISTS idx_reminders_rule_key'
must "$ANCHOR_MAIN" server/schema.sql 'CREATE UNIQUE INDEX IF NOT EXISTS idx_reminders_rule_key ON reminders(rule_key) WHERE rule_key IS NOT NULL;'
must "$ANCHOR_MAIN" server/schema.sql 'CREATE INDEX IF NOT EXISTS idx_leads_partner_org ON leads(partner_org_id);'
must "$H78" server/initDb.js 'async function reportAccess() {'
must "$H78" server/initDb.js '  await reportAccess();'
must "$H78" server/initDb.js "cannot use \${rows.length} object(s): "
must "$H78" server/initDb.js "const names = [...sql.matchAll(/to_regclass\\('(\\w+)'\\) IS NULL THEN CREATE INDEX/g)].map((m) => m[1]);"
must "$H78" server/routes/admin.js "parts.push(\`-- Replay as the portal's own database role (DATABASE_URL's user): the role that replays owns every table (VSP-78).\`);"
wantn "$H78" test/db/restore-role-boot.test.js 5
must "$H78" test/db/restore-role-boot.test.js 'UNIQUE index missing and not makeable still fails the boot'
must "$H78" test/db/restore-role-boot.test.js 'await c.query(`DROP DATABASE IF EXISTS ${db}`);'
must "$H78" test/db/restore-role-boot.test.js 'for (const r of rolesCreated) await c.query(`DROP ROLE IF EXISTS ${r}`);'
mustnot "$R78_PREV" test/db/restore-role-boot.test.js 'DROP DATABASE'
for F in server/schema.sql server/initDb.js server/routes/admin.js; do
  [ "$(blob "$H78" "$F")" = "$(blob "$R78_PREV" "$F")" ] || { echo "REFUSING: VSP78 $F differs from c74d7fd — the new-head READY says product files are byte-identical" >&2; exit 74; }
done
# VSP82: the text cutoff; main carries the Date cutoff (the red is reachable).
must "$H82" server/reminders/dispatcher.js "const cutoff = (await query('SELECT NOW()::text AS now')).rows[0].now;"
must "$H82" server/reminders/dispatcher.js 'due_at <= $1::timestamptz'
mustnot "$H82" server/reminders/dispatcher.js "(await query('SELECT NOW() AS now'))"
must "$ANCHOR_MAIN" server/reminders/dispatcher.js "const cutoff = (await query('SELECT NOW() AS now')).rows[0].now;"
must "$H82" server/reminders/dispatcher.js 'ON CONFLICT (rule_key) WHERE rule_key IS NOT NULL DO NOTHING'
wantn "$H82" test/db/dispatch-cutoff.test.js 3
# VSP85: test files only; every old cell and every old assert line kept.
wantn "$H85" server/dbBackup.test.js 11
wantn "$H85" test/db/backup-coverage.test.js 9
keeps_tests "$ANCHOR_MAIN" "$H85" server/dbBackup.test.js
keeps_tests "$ANCHOR_MAIN" "$H85" test/db/backup-coverage.test.js
for F in server/dbBackup.test.js test/db/backup-coverage.test.js; do
  LOST="$(comm -23 <(p show "${ANCHOR_MAIN}:$F" | grep -i 'assert' | sed 's/^ *//' | sort -u) <(p show "${H85}:$F" | grep -i 'assert' | sed 's/^ *//' | sort -u))"
  [ -z "$LOST" ] || { echo "REFUSING: VSP85 $F lost assert lines present at main: $LOST" >&2; exit 74; }
done
must "$H85" test/db/backup-coverage.test.js 'const tablesInCode = () => census(['"'"'server'"'"', '"'"'scripts'"'"']);'
must "$H85" server/dbBackup.test.js 'const sel = /FROM "(\w+)" t\b/.exec(sql);'
must "$ANCHOR_MAIN" server/dbBackup.js 'FROM "${tableName}" t ORDER BY'
# VSP77: random password, the pairs cell, the five VSP-71 cells kept, one deleted line (the fixed password).
mustnot "$H77" test/db/session-index-boot.test.js "const PASSWORD = 'vsp71';"
must "$ANCHOR_MAIN" test/db/session-index-boot.test.js "const PASSWORD = 'vsp71';"
must "$H77" test/db/session-index-boot.test.js "const PASSWORD = require('crypto').randomBytes(16).toString('hex');"
must "$H77" test/db/session-index-boot.test.js "test('VSP-77: two boots at once on an existing database, index missing: both resolve, and the index is made (5 pairs)'"
wantn "$H77" test/db/session-index-boot.test.js 6
keeps_tests "$ANCHOR_MAIN" "$H77" test/db/session-index-boot.test.js
[ "$(p diff --numstat "$ANCHOR_MAIN" "$H77" -- test/db/session-index-boot.test.js | awk '{print $2}')" = "1" ] \
  || { echo "REFUSING: VSP77 deletes other than the one password line" >&2; exit 74; }
# VSP79: the quoted lookup and setval; main carries the unquoted lookup (the 500 is reachable); the test's bare supertest site (WRONG (t)).
must "$H79" server/routes/admin.js '`, [quoteIdent(seq.sequence_name)]);'
must "$H79" server/routes/admin.js 'parts.push(`SELECT setval(${sqlLiteral(quoteIdent(seq.sequence_name))}, COALESCE('
must "$ANCHOR_MAIN" server/routes/admin.js '`, [seq.sequence_name]);'
must "$ANCHOR_MAIN" server/routes/admin.js "parts.push(\`SELECT setval('\${seq.sequence_name}', COALESCE("
wantn "$H79" test/db/backup-db-sequence-names.test.js 2
must "$H79" test/db/backup-db-sequence-names.test.js 'admin = request.agent(createApp());'
mustnot "$H79" server/routes/admin.js "(VSP-78)"
# VSP80: serve() on 127.0.0.1; closeDb closes servers; no deleted assert line; every edited test file keeps its cells.
must "$H80" test/loopback.js "server.listen(0, '127.0.0.1', resolve);"
must "$H80" test/db/helpers.js '  await closeServers();'
wantn "$H80" test/db/loopback.test.js 2
[ "$(p diff "$ANCHOR_MAIN" "$H80" | grep '^-[^-]' | grep -ci 'assert')" = "0" ] || { echo "REFUSING: VSP80 deletes an assert line — it claims no test logic changed" >&2; exit 74; }
for F in server/errors.test.js test/db/async-faults.test.js test/db/backup-coverage.test.js test/db/backup-dump-replay.test.js test/db/completed-response.test.js \
         test/db/concurrency.test.js test/db/routes.test.js; do
  keeps_tests "$ANCHOR_MAIN" "$H80" "$F"
  [ "$(ntests "$ANCHOR_MAIN" "$F")" = "$(ntests "$H80" "$F")" ] || { echo "REFUSING: VSP80 changed the cell count of $F" >&2; exit 74; }
done
# Shared: the dependency and CI files are main's at every head.
for ID in $TARGETS; do
  H="$(fld "$ID" 4)"
  [ "$(blob "$H" package-lock.json | cut -c1-7)" = "$LOCK_BLOB" ] && [ "$(blob "$H" package.json | cut -c1-7)" = "$PKG_BLOB" ] \
    && [ "$(blob "$H" .github/workflows/test.yml | cut -c1-7)" = "$CI_BLOB" ] || { echo "REFUSING: $ID's package files or CI workflow differ from the briefed blobs" >&2; exit 74; }
done

# 63 — the dependency rule, in both.
for T in 'npm ci --offline --ignore-scripts' 'entry by entry' 'never npm audit'; do
  grep -qiF "$T" "$BRIEF" || { echo "REFUSING: brief lacks the dependency rule '$T'" >&2; exit 63; }
  printf '%s\n' "$PROMPT" | grep -qiF -- "$T" || { echo "REFUSING: prompt lacks the dependency rule '$T'" >&2; exit 63; }
done

# 31 — the READYs are on disk and name the pinned heads; their NOT TESTED lines are carried verbatim; sources on disk.
for PAIR in "$READY76|VSP-76 READY FOR QA. Branch vsp-76-dead-client-handoff @ ${H76:0:12}" \
            "$READY77|VSP-77 READY FOR QA. Branch vsp-77-session-index-test-hygiene @ ${H77:0:12}" \
            "$READY79|VSP-79 READY FOR QA. Branch vsp-79-mixed-case-sequence @ ${H79:0:7}" \
            "$READY80|VSP-80 READY FOR QA. Branch vsp-80-supertest-loopback @ ${H80:0:12}" \
            "$READY78|VSP-78 READY FOR QA. Branch vsp-78-restore-role-boot @ ${R78_PREV:0:12}" \
            "$READY78N|VSP-78 new READY FOR QA at ${H78:0:12}" \
            "$READY82|VSP-82 READY FOR QA. Branch vsp-82-dispatch-cutoff @ ${H82:0:12}" \
            "$READY85|VSP-85 READY FOR QA. Branch vsp-85-backup-test-gaps @ ${H85:0:12}"; do
  RF="${PAIR%%|*}"; SUBJ="${PAIR#*|}"
  [ -s "$RF" ] || { echo "REFUSING: a READY mail is not on disk: $RF" >&2; exit 31; }
  grep -qF -- "$SUBJ" "$RF" || { echo "REFUSING: $RF's BLUF does not carry '$SUBJ'" >&2; exit 31; }
done
grep -qF 'Supersedes c74d7fd' "$READY78N" || { echo "REFUSING: the VSP-78 new-head READY does not say it supersedes c74d7fd" >&2; exit 31; }
for RF in "$READY76" "$READY77" "$READY78" "$READY79" "$READY80" "$READY82" "$READY85"; do
  NT="$(awk 'f&&!/^- /{exit} f{print;next} /^NOT TESTED/{f=1;print}' "$RF")"
  [ -n "$NT" ] || { echo "REFUSING: $RF carries no NOT TESTED block" >&2; exit 31; }
  while IFS= read -r L; do
    [ -n "$L" ] || continue
    grep -qxF -- "$L" "$BRIEF" || { echo "REFUSING: the brief does not carry this NOT TESTED line of $RF verbatim: $L" >&2; exit 31; }
  done <<< "$NT"
done
for T in 'VSP-76 NOT TESTED' 'VSP-77 NOT TESTED' 'VSP-78 NOT TESTED' 'VSP-79 NOT TESTED' 'VSP-80 NOT TESTED' 'VSP-82 NOT TESTED' 'VSP-85 NOT TESTED' \
         'WHY ONE BATCHED GATE' 'THE KEY MEASUREMENT' 'FORCED-HAZARD SWEEP' 'CLIENT REACH' 'C-10' 'vsp78-newhead-READY-mail.txt' 'vsp80-READY-mail.txt' \
         'REQUIRED CELL' 'REAL-ROUTE CELL' '80.65' 'OUT OF SCOPE' 'ROUND 1' "$G11_CHILD_SHA1"; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: the brief does not carry '$T'" >&2; exit 31; }
done
[ -s "$CLAR" ] || { echo "REFUSING: Vision CLARIFICATIONS.md absent: $CLAR" >&2; exit 31; }
for C in 'C-08.' 'C-09.' 'C-10.' 'C-11.' 'C-12.'; do grep -qF "**$C" "$CLAR" || { echo "REFUSING: $CLAR lacks $C" >&2; exit 31; }; done
grep -qF '1de6d92' "$CLAR" || { echo "REFUSING: CLARIFICATIONS C-10 does not name 1de6d92 — Tuesday's VSP-78 rulings are not recorded at this head" >&2; exit 31; }
grep -qF '**C-13.' "$CLAR" && echo "NOTE: Vision CLARIFICATIONS now has a C-13 — the brief was drafted against C-01..C-12; read it before launch" >&2
for PAIR in "$G11_DIR|VSP66-G11-F1" "$G11_DIR|G11-M1" "$G12_DIR|VSP69-G12-F1" "$G12_DIR|VSP75-G12-O3" "$G13_DIR|VERDICTS"; do
  D="${PAIR%%|*}"; T="${PAIR#*|}"
  [ -s "$D/report.md" ] || { echo "REFUSING: an earlier gate's report is absent: $D/report.md" >&2; exit 31; }
  grep -qF -- "$T" "$D/report.md" || { echo "REFUSING: $D/report.md does not carry '$T'" >&2; exit 31; }
  grep -qF -- "$D" "$BRIEF" || { echo "REFUSING: the brief does not name $D" >&2; exit 31; }
  case "$PROMPT" in *"$D"*) ;; *) echo "REFUSING: the prompt does not name $D" >&2; exit 31 ;; esac
done
[ "$(shasum "$G11_TOOLS/qa-g11-n1-child.cjs" 2>/dev/null | awk '{print $1}')" = "$G11_CHILD_SHA1" ] \
  || { echo "REFUSING: gate 11's qa-g11-n1-child.cjs is absent or no longer the pinned bytes ($G11_CHILD_SHA1)" >&2; exit 31; }
[ "$(shasum "$G11_TOOLS/qa-g11-stallproxy.cjs" 2>/dev/null | awk '{print $1}')" = "$G11_PROXY_SHA1" ] \
  || { echo "REFUSING: gate 11's qa-g11-stallproxy.cjs is absent or no longer the pinned bytes" >&2; exit 31; }
for PAIR in "$G11_TOOLS|qa-g11-n1-child.cjs qa-g11-stallproxy.cjs qa-g11-n1.cjs qa-g11-arms.cjs qa-harness-g11-vsp.cjs qa-harness-g11-schema.cjs qa-g11-n2.cjs qa-g11-n6.cjs qa-g11-lib.cjs qa-g11-sql.cjs" \
            "$G12_TOOLS|qa-harness-g12-disp.cjs qa-g12-disp.cjs qa-g12-cellrun.py" \
            "$G13_TOOLS|qa-run.py mktree-portal.sh qa-mkdb.cjs run-suite.sh lockcmp.py lockwalk.py specsets.py tapsets.py dupcount-g13.py qa-floorcount.py floor-g13.sh qa-harness-floorctl.mjs qa-io1-preload-fetchguard.cjs qa-g13-lazywatch.cjs qa-g13-clusterlist.cjs run-node20-g13.sh qa-g13-node20.cjs"; do
  D="${PAIR%%|*}"
  for H in ${PAIR#*|}; do
    [ -s "$D/$H" ] || { echo "REFUSING: tool $H is not on disk in $D — the brief names it" >&2; exit 31; }
    grep -qF -- "$H" "$BRIEF" || { echo "REFUSING: the brief does not name the tool $H" >&2; exit 31; }
  done
done

# 39 — the floor instrument is on disk and named.
[ -s "$G13_FLOOR" ] || { echo "REFUSING: gate 13's floor instrument missing: $G13_FLOOR" >&2; exit 39; }
grep -qF 'qa-floorcount.py' "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument qa-floorcount.py" >&2; exit 39; }

# 10 / 17 — report path named in both; no stale report.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

# 12 — tiers declared in both, at the pinned heads.
for ID in $TARGETS; do
  H7="$(fld "$ID" 4 | cut -c1-7)"
  grep -qE "^- \*\*${ID}\*\* at \`${H7}\` — \*\*TIER 2" "$BRIEF" || { echo "REFUSING: brief does not declare $ID at \`$H7\` TIER 2" >&2; exit 12; }
  case "$PROMPT" in *"$ID (TIER 2"*) ;; *) echo "REFUSING: prompt does not declare: $ID (TIER 2" >&2; exit 12 ;; esac
done

# 78 — the commission's requirements, in both.
for T in 'ROUND 1' 'TIER 2' 'through-code' 'VSP66-G11-F1' 'VSP71-G11-P1' 'G11-M1' 'G11-O3' 'VSP69-G12-F1' 'VSP75-G12-O3' 'qa-g11-n1-child.cjs' \
         'window:terminate:immediate:product' 'M5' 'WHEN OTHERS' 'mixed-case' 'REAL-ROUTE' 'decoy' '127.0.0.1' 'forced' 'da62873' '241b8bb' '28adf36' \
         'max1' 'BROKEN' 'idx_reminders_rule_key' 'REQUIRED CELL' 'access line' 'C-10' 'search_path' 'pairs' 'held write' 'CLIENT REACH' \
         'millisecond grid' 'DateStyle' 'TimeZone' 'M6' 'M9' 'weakened' 'SETS, NOT COUNTS' '6dbffdf' 'f593e38' '1de6d92' 'ccfc7ef' 'b78d2e3' 'c74d7fd' \
         'NOT CI' '80%' '80.65' 'Node 20' 'NODE20-LEG' 'DOCKER-PULL-NEVER' 'UNMEASURED' 'e2e:pro' 'PRODUCTION IS LIVE' \
         'datasec-sales-db.postgres.database.azure.com' 'salesportal_test_lazy' 'TEST_DATABASE_URL' 'vsp78_' 'vsp_qa_g11_7609291_test' 'Dependabot' \
         'node --check' 'VOID'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks '$T'" >&2; exit 78; }
  printf '%s\n' "$PROMPT" | grep -qiF -- "$T" || { echo "REFUSING: prompt lacks '$T'" >&2; exit 78; }
done

# 13 / 14 / 15 / 20 / 70 — directive, brief path, placeholders, verdict route, key path, question route, safety line.
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
if printf '%s\n' "$PROMPT" | LC_ALL=C grep -q '@[A-Z_]*@'; then echo "REFUSING: the prompt carries a placeholder" >&2; exit 14; fi
case "$PROMPT" in *"MAIL YOUR VERDICT"*"tuesday-agent@agentmail.to"*) ;; *) echo "REFUSING: prompt must say MAIL YOUR VERDICT to tuesday-agent@agentmail.to" >&2; exit 15 ;; esac
case "$PROMPT" in *"$SUBJECT_STEM"*) ;; *) echo "REFUSING: prompt must carry the verdict subject stem" >&2; exit 15 ;; esac
grep -qF "$SUBJECT_STEM" "$BRIEF" || { echo "REFUSING: brief must carry the verdict subject stem" >&2; exit 15; }
grep -qF 'MAIL YOUR VERDICT' "$BRIEF" || { echo "REFUSING: brief must say MAIL YOUR VERDICT" >&2; exit 15; }
if printf '%s\n' "$PROMPT" | grep -qi 'wednesday-agent@' && ! printf '%s\n' "$PROMPT" | grep -q 'Never wednesday-agent@'; then
  echo "REFUSING: the prompt routes to wednesday-agent@ — Datasec's coordinator is Tuesday" >&2; exit 15; fi
case "$PROMPT" in *"/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env"*) ;; *) echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20 ;; esac
for T in "$QUESTION_SUBJ" "$ANSWER_PREFIX" "$ROUTE_NAME" 'proceed on the safest reading' 'read it with your verdict key'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the question route: $T" >&2; exit 20; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the question route: $T" >&2; exit 20 ;; esac
done
for T in 'If a response is cut off by a safety check, record it and continue with the next item' "authorised defensive QA of Datasec's own product on loopback"; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the safety-check line: $T" >&2; exit 70; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the safety-check line: $T" >&2; exit 70 ;; esac
done

# 19 — words the prompt must carry (% is a space) and the brief's sections.
WORDS="merge-tree NOT%TESTED env%-i bash createApp() initDb() 6dbffdf f593e38 da62873 1de6d92 241b8bb 28adf36 ccfc7ef b78d2e3 work-g14 vsp_qa_g14 _test
FOREGROUND MEASURED%AT%RUNTIME PROBED READ%ONLY start%/%mid%/%end CI VOID node%--check"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## Charter' '^## RULED BY KAM, AND SETTLED' '^## PRIOR ROUND' '^PRIOR ROUND: ' 'ITS REPORT IS ON DISK AT:' '^## PIN' \
         '^## WRONG OR UNVERIFIABLE' '^## THE READYs' '^## 2a. LEGITIMATE SHAPES' '^## N1. VSP-76' '^## N2. VSP-78' '^## N3. VSP-79' '^## N4. VSP-82' \
         '^## N5. VSP-80' '^## N6. VSP-77' '^## N7. VSP-85' '^## N8. MERGED TREE' '^## 12. The merge' '^## 13. FLOOR' "^## TUESDAY'S RULINGS AT STAMP" \
         '^## 14. Output' '^PROVENANCE:'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
# 24 — the prompt must DESCRIBE the app's entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qE 'server/index\.js|stage3/server\.js'; then
  echo "REFUSING: the prompt contains a literal server entry path — this agent would read as a FOREIGN SERVER to an argv-grep floor check. Describe it; do not name it." >&2; exit 24; fi

# 53 / 60 / 61 / 62 / 64 / 69 / 75 — standing rules, in both.
for T in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' '420 s' '120 s'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the deadline/heartbeat rule '$T'" >&2; exit 53; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the deadline/heartbeat rule '$T'" >&2; exit 53 ;; esac
done
for T in 'node --check' 'VOID'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the parse-before-red rule '$T'" >&2; exit 60; }
done
for T in 'EXCLUSIVE' 'work-g14'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the tree-exclusivity rule '$T'" >&2; exit 61; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the tree-exclusivity rule '$T'" >&2; exit 61 ;; esac
done
for T in '4848' '8080' '47787' 'env -i' 'AGENTMAIL_API_KEY' 'AGENTMAIL_INBOX' 'no jest lock' 'salesportal_test' '5433' 'vsp71_' 'vsp73_' 'vsp78_'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the Vision floor rule '$T'" >&2; exit 62; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the Vision floor rule '$T'" >&2; exit 62 ;; esac
done
for T in 'NEVER the live' 'datasec-sales-portal.azurewebsites.net' 'datasec-sales-portal-rg' 'no app-setting change' 'AZURE_BACKUP_CONN_STR'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not name '$T' as NEVER" >&2; exit 64; }
  printf '%s\n' "$PROMPT" | grep -qiF -- "$T" || { echo "REFUSING: prompt does not name '$T' as NEVER" >&2; exit 64; }
done
for T in 'ntfy.invalid' 'never contact ntfy.sh'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the ntfy egress rule '$T'" >&2; exit 69; }
  printf '%s\n' "$PROMPT" | grep -qiF -- "$T" || { echo "REFUSING: prompt lacks the ntfy egress rule '$T'" >&2; exit 69; }
done
for T in 'CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY' 'PRIOR WORK' 'OWN object dir' 'no writes in the portal repo' 'start / mid / end' 'NOT TESTED'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the standing line '$T'" >&2; exit 75; }
  printf '%s\n' "$PROMPT" | grep -qiF -- "$T" || { echo "REFUSING: prompt lacks the standing line '$T'" >&2; exit 75; }
done

# 38 — the brief names every negative-control seat; advisory if one is no longer running.
for P in $NEG_SEATS; do
  grep -q "\`$P\`" "$BRIEF" || { echo "REFUSING: brief does not name seat pid $P as a negative control" >&2; exit 38; }
  [ "$(ps -o comm= -p "$P" 2>/dev/null | sed 's#.*/##')" = "claude" ] || echo "NOTE: negative-control seat $P is not a running claude now — re-read the seats and update the brief's §13.4 before launch" >&2
done

# 45 — the Node 20 leg as commissioned; the prompt is told which.
NODE20="$(sed -n 's/^NODE20-LEG: \([A-Z-]*\)[[:space:]]*$/\1/p' "$BRIEF" | head -1)"
case "$NODE20" in
  NOT-RUN|DOCKER-PULL-NEVER) ;;
  "$PH_NODE20") echo "REFUSING: the brief's NODE20-LEG line is still ${PH_NODE20} — Tuesday decides NOT-RUN or DOCKER-PULL-NEVER before launch" >&2; exit 45 ;;
  *) echo "REFUSING: the brief's NODE20-LEG line reads '${NODE20:-<missing>}' — it must be exactly NOT-RUN or DOCKER-PULL-NEVER" >&2; exit 45 ;;
esac

# 44 — local Postgres is listening on :5433. The launcher never starts a container; the Vision seat does.
lsof -nP -iTCP:5433 -sTCP:LISTEN >/dev/null 2>&1 \
  || { echo "REFUSING: nothing LISTENs on :5433 — the gate's runtime legs would all be NOT RUN. Ask the Vision seat to start its local vsp-dev-db (never from this launcher, never from the gate), then re-run --check." >&2; exit 44; }

# 41 — the answer route exists (Tuesday adds 'QA/Vision-gate14|tuesday-agent@agentmail.to|no' at launch). Run late on purpose: --check
#      shows every other guard first.
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || {
  echo "guards pass (40 6 9 7 8 18 22 80 74 63 31 39 10 17 12 78 13 14 15 20 70 19 24 53 60 61 62 64 69 75 38 45 44); route NOT added." >&2
  echo "REFUSING: no '${ROUTE_NAME}|tuesday-agent@agentmail.to|…' line in $ROUTING — answers to the gate would have no route. Add it (pattern: the QA/Vision-gate13 line) before launch." >&2; exit 41; }

# 32 — the coordinator stamps the self-check (line AND note) and every @STAMP@. LAST, so --check shows every other guard first.
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "guards pass (40 6 9 7 8 18 22 80 74 63 31 39 10 17 12 78 13 14 15 20 70 19 24 53 60 61 62 64 69 75 38 45 44 41); self-check NOT stamped." >&2
  echo "REFUSING: the brief still carries ${PH_STAMP} (Self-check line and note, TUESDAY'S RULINGS items 2, 3, 4 and 5) — the coordinator re-reads end-to-end and stamps all of them before launch" >&2; exit 32
fi

PIN_BLOCK="$(printf 'PINNED HEADS — verified by the launcher at %s (cat-file; base 6dbffdf for all seven, 0 behind; ancestor and merge-base with MAIN; not-already-on-main; commit counts; exact non-merge chains, NO merges; 1de6d92<-c74d7fd; file sets exact; overlap matrix = admin.js (VSP78 x VSP79) and backup-coverage.test.js (VSP80 x VSP85) only; git ls-remote origin for every row):\n' "$PIN_TS"
  printf '%s\n' "$PIN" | awk -F'\t' '{ printf "  %-7s %-7s %-35s %s  base %s  commits %s\n", $1, $2, $3, $4, ($5=="-"?"-":substr($5,1,12)), $6 }'
  printf '  Main: pinned %s%s\n' "${MAINH:0:12}" "$STALE"
  [ -z "$ORIGIN_MAIN_NOTE" ] || printf '  %s\n' "$ORIGIN_MAIN_NOTE"
  printf '  Positive controls: main 6dbffdf (hands out the dead client; fails the other-role boot 42501 on leads; answers the mixed-case backup-db 500; defers due-now reminders; reaches the decoy under the forced hazard); VSP77 M5 and VSP85 M6-M9 must survive main'"'"'s old test files\n'
  printf 'NODE20-LEG, as set in the brief: %s\n' "$NODE20")"

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  printf '%s\n' "$PIN_BLOCK"
  echo "  PIN parsed, eight rows, no placeholder, heads = the pinned chains' tips (40); every sha a local commit (6); main = 6dbffdf or a delta-free descendant; 6dbffdf <- 110bb03, BACKLOG only; 110bb03 / 4813e5f / e59232e on main (9)"
  echo "  base 6dbffdf, counts 2 / 1 / 3 / 1 / 1 / 1 / 1, 0 behind (7 8); exact chains, no merges, 1de6d92 <- c74d7fd (9); origin re-read $PIN_TS (18)"
  echo "  file sets 4 / 1 / 4 / 2 / 10 / 2 / 2, c74d7fd..1de6d92 = the test only (22); overlap matrix = the two named files only, no BACKLOG.md (80)"
  echo "  content: BROKEN mark; random password + pairs cell; 15 soft + rule_key hard + reportAccess, product = c74d7fd; quoteIdent lookup + setval, main unquoted, the bare agent in VSP79's test; serve() 127.0.0.1, 0 deleted asserts; NOW()::text cutoff; VSP85 cells + asserts kept; package/CI blobs (74)"
  echo "  READY BLUFs + NOT TESTED verbatim, C-08..C-12, C-10 names 1de6d92, gate 11/12/13 reports + tools, gate 11 child + proxy sha1 (31); floor (39); report absent (17); tiers (12); commission (78)"
  echo "  directive/brief/placeholders/mail/key/questions/safety (13 14 15 20 70); words + sections (19); no server path (24); standing rules (53 60 61 62 64 69 75); seats $NEG_SEATS (38); NODE20 $NODE20 (45); :5433 (44); route $ROUTE_NAME (41); stamped (32)"
  exit 0
fi

# 11 — no inherited identity: this gate needs neither az nor gh, so both point at fresh EMPTY directories.
ID_TMP="$(mktemp -d "${TMPDIR:-/tmp}/qa-vision-gate14-id.XXXXXX")" || { echo "REFUSING: cannot create the empty identity dir" >&2; exit 11; }
mkdir -p "$ID_TMP/azure-empty" "$ID_TMP/gh-empty" || { echo "REFUSING: cannot create the empty identity dirs under $ID_TMP" >&2; exit 11; }
{ [ -z "$(ls -A "$ID_TMP/azure-empty")" ] && [ -z "$(ls -A "$ID_TMP/gh-empty")" ]; } || { echo "REFUSING: the identity dirs under $ID_TMP are not empty" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_TMP/azure-empty"
export GH_CONFIG_DIR="$ID_TMP/gh-empty"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"
# 64 (cont.) — nothing a product process could use to reach a real provider or database is inherited from this shell.
unset DATABASE_URL TEST_DATABASE_URL DB_QUERY_TIMEOUT_MS DB_CONNECT_TIMEOUT_MS AGENTMAIL_API_KEY AGENTMAIL_INBOX ACS_CONNECTION_STRING \
      ACS_EMAIL_CONNECTION_STRING ACS_EMAIL_SENDER MAIL_SENDER TABLES_CONNECTION_STRING AZURE_BACKUP_CONN_STR AZURE_BACKUP_CONTAINER BACKUP_CRON \
      REMINDER_CRON SESSION_SECRET HPAM_WORD ADVANCED_UNLOCK_SECRET SALES_COPY_EMAIL FEEDBACK_NOTIFY_EMAIL FEEDBACK_NOTIFY_EMAILS APPROVALS_INBOX \
      NTFY_TOPIC NTFY_SERVER LEAD_BOT_API_KEY WEBSITE_SITE_NAME COORDINATOR_SECRET PORT NODE_ENV PGOPTIONS PGTZ PGDATESTYLE
echo "identity: AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR GH_CONFIG_DIR=$GH_CONFIG_DIR (empty) CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR" >&2

PROMPT="$PROMPT

$PIN_BLOCK"
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$PROMPT"
