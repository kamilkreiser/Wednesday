#!/bin/bash
# launch_qa_vision_gate12.sh — cross-project QA agent, ONE gate (Vision gate 12, drafted 2026-09-28) on
# Datasec/Vision_Sales_Portal, THREE targets, THREE verdicts plus one merged-tree line:
#   VSP74  fix/vsp-74-restore-refuses-incomplete-2026-09-28  restore refuses an incomplete backup (server/dbRestore.js)   TIER 1 (Tuesday; builder said 3)
#   VSP75  fix/vsp-75-backup-all-tables-2026-09-28           backup carries all 20 tables (backupTables.js, dbBackup.js)  TIER 1 (Tuesday; builder said 2)
#   VSP69  fix/vsp-69-dispatch-per-reminder-2026-09-28       one transaction per reminder (reminders/dispatcher.js)        TIER 1
#
# SEQUENCING (Tuesday's ruling): this gate runs AFTER gate 11's verdict and after VSP-66/71/70/68/73 merge to portal main. The Vision
# seat then FORWARD-MERGES main into VSP-74, then VSP-75 (never rebase), and fixes VSP-68's dbBackup.test.js stub ON THE VSP-75 BRANCH.
# So VSP74, VSP75 and MAIN-P are stamped by Tuesday afterwards; VSP69 may keep 3ede8ed (one commit on the old main 0d992e0) only while
# main's server/reminders/dispatcher.js is still blob 283be27.
#
# THE HEADS LIVE IN ONE PLACE: the brief's PIN-HEADS table. This launcher PARSES it (carries no head of its own), refuses any
# placeholder, verifies every row against the object store and against origin by `git ls-remote` NOW, and appends the verified
# table to the agent's prompt. The only shas it carries are GATED ANCHORS: the READY chains (d2531ea, bf5bdc0, cad19ab, 0d7a2fb,
# 3ede8ed), the old main 0d992e0 (parent b5c3e8d), VSP-70's refactor 12138cb, and blob 283be27 (main's dispatcher.js).
# The five gate-11 heads come from the brief's GATE11-MERGED line (Tuesday replaces any round-2 sha there at stamp).
#
# PRODUCTION IS LIVE for this project (datasec-sales-portal-rg). The gate is local Postgres only: no az, no deploy, no app
# setting, no connection to the production database. Findings only.
#
# PATTERN: launch_qa_vision_gate11.sh (PIN parse, anchors, file sets, content guards, embedded prompt, --check, stamp LAST).
# CHANGES vs gate 11, each deliberate:
#   - exit 40: PIN rows are exactly MAIN-P + VSP74 + VSP75 + VSP69 (four rows, three targets); commits are stamped, not fixed (VSP69 = 1).
#   - exit 7:  VSP74/VSP75 must be FULLY forward-merged (base = MAIN, 0 behind); VSP69 may be stale-based (NOTE).
#   - exit 9:  merges ALLOWED on VSP74/VSP75 only, and only forward merges (2 parents, second parent on MAIN or on VSP74); their NON-merge
#              commits over MAIN are exactly the READY chains (+ at most one stub-fix commit on VSP75 touching only dbBackup.test.js /
#              BACKLOG.md); READY heads bf5bdc0 / 0d7a2fb are ancestors of the stamped heads (never rebased); GATE11-MERGED on MAIN.
#   - exit 22: exact file sets (VSP74 3 over MAIN, VSP75 7 over MAIN, VSP69 3 over its base).
#   - exit 74: per-target content; VSP75 carries VSP-68's AND VSP-75's dbBackup.js lines; dbBackup.test.js changed on VSP75, still 5 cells,
#              still asserting INCOMPLETE; test( counts 5/5/5; main's dispatcher.js = 283be27.
#   - exit 31: the three READYs on disk with NOT TESTED verbatim (3 / 4 / 3); gate 9's §N.4(h); gate 11's report EXISTS (gate 12 runs after it).
#   - exit 41: the answer route QA/Vision-gate12 exists in fleet/inbox_routing.conf (Tuesday adds it at launch).
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/Vision-gate12' "bash '<this file>'"), NEVER nohup.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Contains a legitimate `cd` (into the QA project, at exec).
# READ-ONLY toward the repo: only cat-file, rev-parse, merge-base, log, rev-list, diff, show, grep, ls-tree, ls-remote.
# --check is READ-ONLY: it runs every guard and exits before any identity dir is made or any agent is started.
# Usage: launch_qa_vision_gate12.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..78 a guard refused
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
BRIEF="$BRIEFS/2026-09-28_vision-gate12-vsp74-vsp75-vsp69.md"
READY74="$BRIEFS/2026-09-28_vision-vsp74-READY-mail.txt"
READY75="$BRIEFS/2026-09-28_vision-vsp75-READY-mail.txt"
READY69="$BRIEFS/2026-09-28_vision-vsp69-READY-mail.txt"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
VSP='/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal'
P_REPO="$VSP/2_Project_Files"
CLAR="$VSP/1_Project_Definition/CLARIFICATIONS.md"
REPORTS="$QA_DIR/projects/vision/reports"
G9_DIR="$REPORTS/2026-09-27-vision-gate9-vsp65-qqpurge"
G9_REPORT="$G9_DIR/report.md"
G10_DIR="$REPORTS/2026-09-27-vision-gate10-vsp65-r2"
G10_TOOLS="$G10_DIR/evidence/tools"
G10_FLOOR="$G10_TOOLS/qa-floorcount.py"
G11_DIR="$REPORTS/2026-09-28-vision-gate11-five-targets"
G11_REPORT="$G11_DIR/report.md"
REPORT="$REPORTS/2026-09-28-vision-gate12-three-targets/report.md"
ROUTE_NAME='QA/Vision-gate12'
NEG_SEATS='59108 20317 40404'   # Tuesday (%0), NexusAI (%22), gate 11 (%34) — at drafting, 2026-09-28 06:45 AEST; Tuesday re-reads at stamp
# Gated anchors (not heads).
ANCHOR_OLDMAIN='0d992e09ebe0830dbe414aa73ca9a17a1be6c480'  # gate 10's GO'd head; main at drafting; VSP69's base
ANCHOR_OLDMAIN_P='b5c3e8d244822df180c34007a44a25f44eb64387' # its single parent
ANCHOR_R70='12138cb46acb8201999ace84cb8f9357ee63aac7'      # VSP-70's refactor (must be on MAIN once VSP-70 merged)
R74_REF='d2531ea9322f2561c50b2005a8ff7aefe42fd395'        # VSP-74 refactor
R74_FIX='bf5bdc06c07b59bf956ae7d40e436582ff1fe24d'        # VSP-74 READY head (pre-forward-merge)
R75_REF='cad19ab7c50f40047c82473c42e6f5c232814406'        # VSP-75 refactor
R75_FIX='0d7a2fb4514a682c0cb3a69593faf9ff3238a93b'        # VSP-75 READY head (pre-forward-merge)
R69_FIX='3ede8ed7e67e686261a260e914bb84600de84a12'        # VSP-69 READY head
DISPATCH_BLOB_MAIN='283be2702721fb3983225af3d2acfec0b9bb64bc'  # server/reminders/dispatcher.js at 0d992e0 and all five gate-11 heads
DISPATCH_BLOB_69='7a67be98580c1bf7f2c6f18f9988e6cd905ca1c8'    # the same file at 3ede8ed
DBBACKUP_TEST_68='4fb902e'                                      # VSP-68's server/dbBackup.test.js blob (prefix) at 7ef698d

SUBJECT_STEM='[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 12'
QUESTION_SUBJ='[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>'
ANSWER_PREFIX='[Tuesday -> QA/Vision-gate12] ANSWER'

p() { git --no-optional-locks -C "$P_REPO" "$@"; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE gate (Vision gate 12) on Datasec/Vision_Sales_Portal with THREE targets and THREE verdicts, each GO or NO-GO, plus one merged-tree line, in the SALES PORTAL repo. This gate runs after gate 11's five targets were merged to portal main; VSP-74 and VSP-75 were then forward-merged with main (never rebased), and VSP-68's backup unit-test stub was fixed on the VSP-75 branch. VSP-69 is one commit on the old main 0d992e0.

READ YOUR COMMISSION FIRST, whole: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-28_vision-gate12-vsp74-vsp75-vsp69.md
Then read the charter it names, the Vision CLARIFICATIONS (C-01..C-06; none covers these tickets), the project's CLAUDE.md (/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/CLAUDE.md; its deploy commands are not for you), the builder's three READY mails (/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-28_vision-vsp74-READY-mail.txt, -vsp75- and -vsp69-READY-mail.txt beside it), and the prior reports: gate 11 /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-28-vision-gate11-five-targets (report.md; evidence/tools/; VSP-74 and VSP-75 sit on its VSP-70 and VSP-68), gate 10 /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-27-vision-gate10-vsp65-r2 (evidence/tools/) and gate 9 /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-27-vision-gate9-vsp65-qqpurge (report.md section N.4(h): the dispatcher re-send VSP-69 fixes). Every builder statement is a CLAIM, never evidence. The three READYs landed within 14 minutes: RE-DERIVE every red, every mutant and every suite set yourself. Verify every PRIOR WORK claim against git history and the prior gates' evidence, never against the brief.

THE TARGETS. All three are ROUND 1 of their class; the two-NO-GO cap applies per class (a NO-GO here is the first; a NO-GO in round 2 goes to Kam).
  VSP74 (TIER 1, Tuesday's ruling; the builder said Tier 3) = Jira VSP-74 = F-B: a restore EMPTIED a live table whose dump had failed. The fix refuses an incomplete backup by default (--allow-incomplete to proceed) and clearTables never deletes a failed table. Its red is re-derived at the refactor d2531ea. THE HEADLINE RISK: ON DELETE CASCADE and SET NULL from a non-failed parent still empty or change a failed child table; the builder's cell used a parent table and cannot see it. A lost or changed row in a failed table is a FAIL.
  VSP75 (TIER 1, Tuesday's ruling; the builder said Tier 2) = Jira VSP-75 = F-A: the nightly backup never contained quotes or any other PRO table. The fix is one shared 20-table list in foreign-key order (session excluded), rows read as row_to_json in primary-key order, JSON columns restored as text. Its red is re-derived at the refactor cad19ab. Take YOUR OWN table census, not the builder's regex; round-trip into a TRUNCATEd AND a populated database; prove no secret is in the backup.
  VSP69 (TIER 1) = Jira VSP-69 = gate 9's N.4(h): the reminder dispatcher sent a batch inside one transaction, so a failure re-sent the whole batch to clients. The fix is one transaction per reminder, at 3ede8ed (one commit on 0d992e0, where its red is re-derived). Re-run gate 9's black-hole arm, a real process death mid-tick, connection churn under load, the poison reminder, and DECIDE the surviving mutant M2 (FOR UPDATE without SKIP LOCKED) under the query bound rather than accept the builder's "correct".
  THE REQUIRED CELL (Tuesday): on the merged tree, VSP-68's dbBackup INCOMPLETE-alert control passes with its injected failure proven to land on the dump query, AND VSP-75's round-trip and FK-order cells pass: the semantic conflict is closed, not papered over. A weakened assertion in the stub fix is a FAIL of VSP75.

WHAT THE BRIEF REQUIRES, in short (the brief is the authority): (1) VSP74: the builder's five cells and three mutants re-derived at d2531ea, the cascade matrix on a real 20-table backup, a backup produced by VSP-68's real code, absent tables in today's 10-table backup shape, the refusal changing nothing. (2) VSP75: its five cells and mutants plus drift mutants the regex misses, your own census and FK check from the catalog, the two round trips, real runBackup through recorders, old backups still restoring, secrets, size and time on a scaled database. (3) VSP69: its five cells and mutants at 0d992e0, the black hole, SIGKILL mid-tick, M2 decided, churn under load and under VSP-66's guard on the merged tree, the poison reminder, order and cutoff. (4) SUITES AS SETS, NOT COUNTS, at every head, the refactors and the merged tree vs the stamped main, plus CI's coverage command run locally (label it: not CI). The Node 20 leg follows the NODE20-LEG line in the brief exactly. (5) CI is UNMEASURED: this project's gh is not authenticated and you must not use gh; never claim CI; name CI's Node 22 coverage gate and its e2e:pro step as the first reads at merge. Every red-proof: fresh tree per arm, asserted edits, node --check rc quoted; a red from a mutant that does not parse is VOID.

LOCAL POSTGRES ONLY. PRODUCTION IS LIVE for this project. NEVER the live portal (datasec-sales-portal.azurewebsites.net, datasec-sales-portal-rg, its Postgres datasec-sales-db.postgres.database.azure.com, its key vault): no request, no DB connection, not even a GET. No az of any kind, no deploy, no app-setting change. Never open a real backup, a production dump or anything under the project's 4_Credentials: every backup JSON you use is built by the product's own code from YOUR seeded database. Real sends are OFF: the dispatcher, the email sender and the backup notifier run only against recorders you wrote; Azure Blob Storage and ACS are replaced by YOUR recorders; ntfy goes only to YOUR loopback recorder. restoreData and clearTables DELETE: print the connected database name before every call and abort if it is not one you created.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT from the object store (git archive into a fresh mktemp -d under projects/vision/work-g12/). Each tree is EXCLUSIVE to this gate and to one purpose; never touch work/ or work-g2 .. work-g11. Copy the prior gates' tools into YOUR evidence folder and re-point them (they hard-code their own paths and ENFORCE their own database prefixes); never run from, edit or write into gate 1-11's copies. Dependencies: npm ci --offline --ignore-scripts only, then prove node_modules/.package-lock.json against the lockfile entry by entry (lockcmp.py AND lockwalk.py). Never npm install, never npm audit, never npx anything not already in the tree. In the repo use ONLY read verbs (show, log, diff, ls-remote, rev-parse, ls-tree, cat-file, grep, merge-base, archive); never fetch, pull, checkout, switch, worktree, commit, stash, reset, clean or gc. Run git merge-tree --write-tree only from the gate's OWN object dir (GIT_OBJECT_DIRECTORY = your own mktemp -d, alternates = the repo's objects), or skip it and say so. Findings-only: no writes in the portal repo, none inside Vision_Sales_Portal, none in gate 1-11's report folders or trees. Never rm: quarantine. Run every loop and every git show <sha>:<path> under bash. CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY: a control derived from the run it validates is not a control.

FLOOR DISCIPLINE. Vision has no jest lock; never borrow NexusAI's. Never use ports 4848, 8080 or 47787, nor 127.0.0.1:49162 / 49164 / 49166; take every port from the kernel and bind 127.0.0.1. Never start the portal's own entry point (it binds all interfaces); use the real createApp() and initDb() in your harness. Postgres is the local container on 127.0.0.1:5433, and ONLY databases you create: vsp_qa_g12_<epoch> and vsp_qa_g12_<epoch>_test (the test name MUST end in _test); never salesportal, salesportal_test (the Vision seat uses it), any vsp_qa_g1..g11 database, the builder's vsp_bf1_*, or any vsp71_* / vsp73_* database you did not cause. VSP-71's and VSP-73's test files (now on main) create and drop their own vsp71_* roles and databases and a vsp73_* database inside test:db; the brief's floor section and Tuesday's ruling govern that. Roles are cluster-global: create one only inside a transaction you roll back, or name it vsp_qa_g12_* and list it; earlier gates' roles are not yours. Event triggers only in your own databases; never ALTER SYSTEM or change server settings. The module's default URL is the builder's dev database, so give every product process YOUR DATABASE_URL and TEST_DATABASE_URL explicitly and print the database each one reached. Release every lock and direct session you open in a finally. No docker command at all, except the Node 20 exception under the NODE20-LEG line. Every product process runs under env -i with an explicit allowlist, NODE_ENV never production. Never set AGENTMAIL_API_KEY or AGENTMAIL_INBOX in a product process, nor any real ACS_* or MAIL_SENDER, AZURE_BACKUP_CONN_STR, TABLES_CONNECTION_STRING, SALES_COPY_EMAIL, a real NTFY_TOPIC, LEAD_BOT_API_KEY or WEBSITE_SITE_NAME; print each product process's env KEY NAMES and assert none is forbidden. NTFY_SERVER=http://ntfy.invalid except your loopback recorder; never contact ntfy.sh; stub fetch to throw on any other URL. Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid, with the brief's negative-control seats classifying FOREIGN in the same run. A zero is reportable only beside an ATTACHED control that fired in the same window. Other gates and seats are live on this box: record the load average beside every timing number; a latency result with no load figure is not a measurement.
DEADLINE AND HEARTBEAT: every step has a written DEADLINE built into your runner (there is no timeout binary here) and releases its servers, proxies, recorders, sessions, locks, roles and children in a finally. Log a HEARTBEAT line at least every 2 minutes; a step with no heartbeat for 5 minutes is aborted and reported, never waited on. Deadlines: requests at the shrunk bound 20 s; requests at the SHIPPED bounds 120 s; a child-process fault cell 30 s; one restore cell 120 s; the scaled backup 300 s; the M2 arms 180 s each; one test:db file 180 s; a whole test:db run 420 s. Nothing above 420 s.

QUESTIONS: your routing name is QA/Vision-gate12. If you must ask, mail tuesday-agent@agentmail.to with the subject "[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>" and proceed on the safest reading without waiting. Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/Vision-gate12] ANSWER"; read it with your verdict key. Never wednesday-agent@. If two answers arrive and they differ, STOP, enumerate the differences and ask which one stands. If a response is cut off by a safety check, record it and continue with the next item; this is authorised defensive QA of Datasec's own product on loopback. Record every question, reading and answer in the report.

Write your report to: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-28-vision-gate12-three-targets/report.md

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with a subject beginning exactly:
[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 12: VSP74 @ <sha7> <GO | NO-GO> · VSP75 @ <sha7> <GO | NO-GO> · VSP69 @ <sha7> <GO | NO-GO> · merged <CLEAN | BACKLOG-ONLY | CONFLICT>
(each sha7 is the pinned head from the verified table below). Lead the body with three sentences, one per target, as the brief's section 14 words them, then one line on the merged tree and one line on the class cap. You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no credentials directory of its own. Use it only in your own mail calls, with a client timeout. Never put the key or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice.

Report every pinned head and main as three timestamped readings (start / mid / end), with the branch name beside each. Include the verbatim operator strings the brief lists: VSP-74's refusal message and its --allow-incomplete warning, the Restore failed line and rc, any 23503 from an old-backup restore, VSP-75's backup table list and the alert on a database without the lazy feedback tables, VSP-69's dispatch failed line in each fault shape, and SELECT version(). Then one paragraph on the queue: the merge results, the BACKLOG resolution, the cells to re-run on the merged head, and CI at merge.

Rule 2 stands: what you did NOT test is first-class output. Write a NOT TESTED section that covers at least CI (UNMEASURED), the restore CLI end to end against Azure Blob Storage, real Azure Blob Storage, real ACS and real ntfy, production's catalog and its two lazy feedback tables, the size of a full production backup, a real App Service restart and multiple real instances, a real stalled Azure Postgres / TLS / failover, Node 22, the container image, and e2e:pro / e2e:api / e2e:feedback. Label every action recommendation MEASURED AT RUNTIME, PROBED or READ ONLY.
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
TARGETS='VSP74 VSP75 VSP69'
EXPECT_IDS="MAIN-P $TARGETS"
for ID in $EXPECT_IDS; do
  N="$(printf '%s\n' "$PIN" | awk -F'\t' -v id="$ID" '$1==id' | wc -l | tr -d ' ')"
  [ "$N" = "1" ] || { echo "REFUSING: PIN table must carry exactly one row '$ID' (found $N)" >&2; exit 40; }
done
[ "$(printf '%s\n' "$PIN" | wc -l | tr -d ' ')" = "4" ] || { echo "REFUSING: PIN table carries rows beyond the four expected ($EXPECT_IDS)" >&2; exit 40; }
row()   { printf '%s\n' "$PIN" | awk -F'\t' -v id="$1" '$1==id'; }
fld()   { row "$1" | awk -F'\t' -v n="$2" '{print $n}'; }   # 2 repo 3 branch 4 head 5 base 6 commits 7 status
is40()  { printf '%s' "$1" | grep -Eq '^[0-9a-f]{40}$'; }
for ID in $EXPECT_IDS; do
  R="$(row "$ID")"; ST="$(fld "$ID" 7)"
  [ "$(printf '%s\n' "$R" | awk -F'\t' '{print NF}')" = "7" ] || { echo "REFUSING: PIN row $ID does not have 7 cells: $R" >&2; exit 40; }
  [ "$ST" = "IN" ] || { echo "REFUSING: PIN row $ID status is '$ST' — IN only" >&2; exit 40; }
  printf '%s' "$R" | grep -q '@' && { echo "REFUSING: PIN row $ID still carries a placeholder (Tuesday stamps it after the forward merges): $R" >&2; exit 40; }
  is40 "$(fld "$ID" 4)" || { echo "REFUSING: PIN row $ID head is not a 40-hex sha: '$(fld "$ID" 4)'" >&2; exit 40; }
  [ "$(fld "$ID" 2)" = "portal" ] || { echo "REFUSING: PIN row $ID repo must be portal" >&2; exit 40; }
done
[ "$(fld MAIN-P 3)" = "main" ] || { echo "REFUSING: row MAIN-P branch must be main" >&2; exit 40; }
branch_of() { case "$1" in
  VSP74) echo 'fix/vsp-74-restore-refuses-incomplete-2026-09-28' ;;
  VSP75) echo 'fix/vsp-75-backup-all-tables-2026-09-28' ;;
  VSP69) echo 'fix/vsp-69-dispatch-per-reminder-2026-09-28' ;;
esac; }
for ID in $TARGETS; do
  [ "$(fld "$ID" 3)" = "$(branch_of "$ID")" ] || { echo "REFUSING: row $ID branch is '$(fld "$ID" 3)', the brief's target is $(branch_of "$ID") — re-brief" >&2; exit 40; }
  is40 "$(fld "$ID" 5)" || { echo "REFUSING: PIN row $ID base is not a 40-hex sha" >&2; exit 40; }
  printf '%s' "$(fld "$ID" 6)" | grep -Eq '^[1-9][0-9]*$' || { echo "REFUSING: PIN row $ID commits '$(fld "$ID" 6)' is not a positive integer" >&2; exit 40; }
done
[ "$(fld VSP69 6)" = "1" ] || { echo "REFUSING: VSP69 commits is '$(fld VSP69 6)' — the brief gates one commit; if VSP-69 was forward-merged, re-brief" >&2; exit 40; }
MAINH="$(fld MAIN-P 4)"
H74="$(fld VSP74 4)"; H75="$(fld VSP75 4)"; H69="$(fld VSP69 4)"

# 9a — the five gate-11 heads come from the brief's GATE11-MERGED line.
G11M="$(sed -n 's/^GATE11-MERGED: //p' "$BRIEF" | head -1)"
[ "$(printf '%s\n' $G11M | grep -Ec '^[0-9a-f]{40}$')" = "5" ] || { echo "REFUSING: the brief's GATE11-MERGED line does not carry exactly five 40-hex shas" >&2; exit 9; }

# 6 / 7 / 8 — commits; base ancestor AND merge-base; not on main; exact count; VSP74/75 fully forward-merged.
for S in "$MAINH" "$H74" "$H75" "$H69" "$ANCHOR_OLDMAIN" "$ANCHOR_R70" "$R74_REF" "$R74_FIX" "$R75_REF" "$R75_FIX" "$R69_FIX" $G11M; do
  T="$(p cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in the portal repo (got '$T') — this launcher never fetches" >&2; exit 6; }
done
STALE=''
for ID in $TARGETS; do
  H="$(fld "$ID" 4)"; BASE="$(fld "$ID" 5)"; N="$(fld "$ID" 6)"; H7="${H:0:7}"
  if [ "$BASE" != "$MAINH" ]; then
    if [ "$ID" = "VSP69" ] && p merge-base --is-ancestor "$BASE" "$MAINH" 2>/dev/null && [ "$(p merge-base "$H" "$MAINH" 2>/dev/null)" = "$BASE" ]; then
      STALE="$STALE $ID"
      echo "NOTE: row $ID is a STALE-BASE row (base ${BASE:0:7} is an ancestor of MAIN ${MAINH:0:7}) — expected for VSP69; §12 predicts a BACKLOG-only conflict" >&2
    else
      echo "REFUSING: row $ID base ${BASE:0:7} is not MAIN ${MAINH:0:7} — VSP74/VSP75 must be fully forward-merged (base = MAIN); VSP69 must be merge-base(head, MAIN)" >&2; exit 7
    fi
  fi
  p merge-base --is-ancestor "$BASE" "$H" 2>/dev/null || { echo "REFUSING: $ID base ${BASE:0:7} is not an ancestor of $H7" >&2; exit 7; }
  [ "$(p merge-base "$BASE" "$H" 2>/dev/null)" = "$BASE" ] || { echo "REFUSING: $ID merge-base(base, head) is not the base" >&2; exit 7; }
  p merge-base --is-ancestor "$H" "$MAINH" 2>/dev/null \
    && { echo "REFUSING: $ID $H7 is ALREADY ON MAIN ${MAINH:0:7} — the brief says it is not; re-brief" >&2; exit 7; }
  GOTN="$(p rev-list --count "${BASE}..${H}" 2>/dev/null)"
  [ "$GOTN" = "$N" ] || { echo "REFUSING: $ID $H7 has $GOTN commits over its base, the table says $N" >&2; p log --format='%h %p %s' "${BASE}..${H}" >&2; exit 8; }
  BEHIND="$(p rev-list --count "${H}..${MAINH}" 2>/dev/null)"
  if [ "$ID" != "VSP69" ]; then
    [ "$BEHIND" = "0" ] || { echo "REFUSING: $ID $H7 is $BEHIND behind main ${MAINH:0:7} — the forward merge is owed before the gate" >&2; exit 7; }
  fi
done

# 9 — gated anchors and the forward-merge shape.
[ "$(p log -1 --format='%P' "$ANCHOR_OLDMAIN" 2>/dev/null)" = "$ANCHOR_OLDMAIN_P" ] \
  || { echo "REFUSING: 0d992e0's parent is not b5c3e8d — re-brief" >&2; exit 9; }
[ "$MAINH" != "$ANCHOR_OLDMAIN" ] || { echo "REFUSING: portal main is still 0d992e0 — gate 11's targets are not merged; gate 12 runs after them (Tuesday's sequencing)" >&2; exit 9; }
p merge-base --is-ancestor "$ANCHOR_OLDMAIN" "$MAINH" 2>/dev/null || { echo "REFUSING: main does not contain 0d992e0 — re-brief" >&2; exit 9; }
for S in $G11M "$ANCHOR_R70"; do
  p merge-base --is-ancestor "$S" "$MAINH" 2>/dev/null || { echo "REFUSING: gate-11 sha ${S:0:7} is not on main ${MAINH:0:7} — gate 12 runs after the five merges; correct GATE11-MERGED or wait" >&2; exit 9; }
done
[ "$H69" = "$R69_FIX" ] || echo "NOTE: VSP69 is ${H69:0:7}, not the READY head 3ede8ed — the brief's §N3 reds and shape are stale; re-brief" >&2
[ "$(fld VSP69 5)" = "$ANCHOR_OLDMAIN" ] || { echo "REFUSING: VSP69's base is not 0d992e0 — re-brief" >&2; exit 9; }
[ "$(p log -1 --format='%P' "$R69_FIX" 2>/dev/null)" = "$ANCHOR_OLDMAIN" ] || { echo "REFUSING: 3ede8ed's parent is not 0d992e0" >&2; exit 9; }
# never rebased: the READY heads are ancestors of the stamped heads; the stack is kept.
p merge-base --is-ancestor "$R74_FIX" "$H74" 2>/dev/null || { echo "REFUSING: VSP74 ${H74:0:7} does not contain the READY head bf5bdc0 — rebased or rebuilt; the brief gates a forward merge" >&2; exit 9; }
p merge-base --is-ancestor "$R75_FIX" "$H75" 2>/dev/null || { echo "REFUSING: VSP75 ${H75:0:7} does not contain the READY head 0d7a2fb — rebased or rebuilt" >&2; exit 9; }
p merge-base --is-ancestor "$R74_FIX" "$H75" 2>/dev/null || { echo "REFUSING: VSP75 does not contain VSP-74's bf5bdc0 — the stack is broken" >&2; exit 9; }
[ "$(p log -1 --format='%P' "$R74_FIX")" = "$R74_REF" ] && [ "$(p log -1 --format='%P' "$R75_FIX")" = "$R75_REF" ] && [ "$(p log -1 --format='%P' "$R75_REF")" = "$R74_FIX" ] \
  || { echo "REFUSING: the READY chains are not d2531ea→bf5bdc0 and bf5bdc0→cad19ab→0d7a2fb" >&2; exit 9; }
p merge-base --is-ancestor "$H74" "$H75" 2>/dev/null || echo "NOTE: VSP74's stamped head is not an ancestor of VSP75's (VSP-75 merged main directly) — §N1 content equality is checked below" >&2
# non-merge commits over MAIN are exactly the READY chain (+ at most one stub-fix commit on VSP75); merges are forward merges only.
nonmerge() { p rev-list --no-merges "${MAINH}..$1" 2>/dev/null | sort; }
merges()   { p rev-list --merges "${MAINH}..$1" 2>/dev/null; }
[ "$(nonmerge "$H74")" = "$(printf '%s\n' "$R74_REF" "$R74_FIX" | sort)" ] \
  || { echo "REFUSING: VSP74's non-merge commits over main are not exactly d2531ea + bf5bdc0. Got:" >&2; nonmerge "$H74" >&2; exit 9; }
EXTRA75="$(comm -23 <(nonmerge "$H75") <(printf '%s\n' "$R74_REF" "$R74_FIX" "$R75_REF" "$R75_FIX" | sort))"
MISSING75="$(comm -13 <(nonmerge "$H75") <(printf '%s\n' "$R74_REF" "$R74_FIX" "$R75_REF" "$R75_FIX" | sort))"
[ -z "$MISSING75" ] || { echo "REFUSING: VSP75 lacks READY-chain commits over main: $MISSING75" >&2; exit 9; }
[ "$(printf '%s' "$EXTRA75" | sed '/^$/d' | wc -l | tr -d ' ')" -le 1 ] || { echo "REFUSING: VSP75 carries more than one new non-merge commit (the stub fix) over the READY chain:" >&2; printf '%s\n' "$EXTRA75" >&2; exit 9; }
for S in $EXTRA75; do
  GOTF="$(p diff --name-only "${S}^" "$S" 2>/dev/null | sort)"
  printf '%s\n' "$GOTF" | grep -vxE 'server/dbBackup\.test\.js|BACKLOG\.md' | grep -q . \
    && { echo "REFUSING: VSP75's extra commit ${S:0:7} touches more than server/dbBackup.test.js / BACKLOG.md:" >&2; printf '%s\n' "$GOTF" >&2; exit 9; }
done
[ -n "$(merges "$H74")" ] || { echo "REFUSING: VSP74 carries no merge commit over main — the brief gates a FORWARD MERGE, not a rebase" >&2; exit 9; }
[ -n "$(merges "$H75")" ] || { echo "REFUSING: VSP75 carries no merge commit over main — the brief gates a FORWARD MERGE, not a rebase" >&2; exit 9; }
for ID in VSP74 VSP75; do
  H="$(fld "$ID" 4)"
  for M in $(merges "$H"); do
    PARS="$(p log -1 --format='%P' "$M")"
    [ "$(printf '%s\n' $PARS | wc -l | tr -d ' ')" = "2" ] || { echo "REFUSING: $ID merge ${M:0:7} is not a two-parent merge" >&2; exit 9; }
    P2="$(printf '%s\n' $PARS | sed -n 2p)"
    if ! p merge-base --is-ancestor "$P2" "$MAINH" 2>/dev/null && ! { [ "$ID" = "VSP75" ] && p merge-base --is-ancestor "$P2" "$H74" 2>/dev/null; }; then
      echo "REFUSING: $ID merge ${M:0:7} merges ${P2:0:7}, which is neither on main nor (for VSP75) on VSP74 — not a forward merge" >&2; exit 9
    fi
  done
done
[ "$(p rev-list --no-merges "${ANCHOR_OLDMAIN}..${H69}" | wc -l | tr -d ' ')" = "1" ] && [ -z "$(p rev-list --merges "${ANCHOR_OLDMAIN}..${H69}")" ] \
  || { echo "REFUSING: VSP69 is not exactly one linear commit on 0d992e0" >&2; exit 9; }

# 18 — RE-PIN: every row at origin, by ls-remote, read NOW (immediately before launch).
for ID in $EXPECT_IDS; do
  BR="$(fld "$ID" 3)"; H="$(fld "$ID" 4)"
  L="$(p ls-remote origin "refs/heads/$BR" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: row $ID: $H is not at refs/heads/$BR on origin — that head moved or was never pushed; re-pin" >&2; printf '%s\n' "${L:-<nothing>}" >&2; exit 18; }
done
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — exact file sets over each target's base.
fileset() { case "$1" in
  VSP74) printf '%s\n' BACKLOG.md server/dbRestore.js test/db/restore-incomplete.test.js ;;
  VSP75) printf '%s\n' BACKLOG.md server/backupTables.js server/dbBackup.js server/dbBackup.test.js server/dbRestore.js \
                       test/db/backup-coverage.test.js test/db/restore-incomplete.test.js ;;
  VSP69) printf '%s\n' BACKLOG.md server/reminders/dispatcher.js test/db/dispatch-once.test.js ;;
esac; }
for ID in $TARGETS; do
  H="$(fld "$ID" 4)"; BASE="$(fld "$ID" 5)"
  GOT="$(p diff --name-only "$BASE" "$H" 2>/dev/null | sort)"
  [ "$GOT" = "$(fileset "$ID" | sort)" ] || { echo "REFUSING: $ID ${H:0:7}'s delta over its base is not exactly the briefed file set. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }
done
[ "$(p diff --name-only "$(p log -1 --format=%P "$R74_REF")" "$R74_REF" 2>/dev/null)" = "server/dbRestore.js" ] || { echo "REFUSING: the refactor d2531ea touches more than server/dbRestore.js — re-brief" >&2; exit 22; }
[ "$(p diff --name-only "$R74_FIX" "$R75_REF" 2>/dev/null)" = "server/dbBackup.js" ] || { echo "REFUSING: the refactor cad19ab touches more than server/dbBackup.js — re-brief" >&2; exit 22; }

# 74 — per-target content, read from the pinned shas (never a checkout).
has() { p show "${1}:${2}" 2>/dev/null | grep -qF -- "$3"; }   # sha path fixed-string
must() { has "$1" "$2" "$3" || { echo "REFUSING: ${1:0:7}:$2 lacks '$3' — the brief gates different code; re-brief" >&2; exit 74; }; }
mustnot() { has "$1" "$2" "$3" && { echo "REFUSING: ${1:0:7}:$2 already carries '$3' — the brief's history is wrong; re-brief" >&2; exit 74; }; return 0; }
ntests() { p show "${1}:${2}" 2>/dev/null | grep -c '^test('; }
# VSP-70 is on main (VSP-74's base behaviour).
must "$MAINH" server/dbRestore.js 'client.release(broken);'
must "$MAINH" server/dbRestore.js 'ROLLBACK failed as well'
# VSP74 (and carried into VSP75)
for H in "$H74" "$H75"; do
  must "$H" server/dbRestore.js 'function failedTables(data) {'
  must "$H" server/dbRestore.js 'if (data.tables[t] && !failed.has(t)) {'
  must "$H" server/dbRestore.js 'Nothing was changed. To restore the other tables and leave these exactly as they are, re-run with --allow-incomplete'
  must "$H" server/dbRestore.js "allowIncomplete: argv.includes('--allow-incomplete'),"
  must "$H" server/dbRestore.js 'client.release(broken);'
  must "$H" server/dbRestore.js "console.error('Error: AZURE_BACKUP_CONN_STR not set.');"
done
mustnot "$MAINH" server/dbRestore.js 'function failedTables(data) {'
[ "$(p rev-parse "${H74}:test/db/restore-incomplete.test.js")" = "$(p rev-parse "${H75}:test/db/restore-incomplete.test.js")" ] \
  || { echo "REFUSING: VSP-74's restore-incomplete.test.js differs between VSP74 and VSP75 — the stack diverged" >&2; exit 74; }
[ "$(ntests "$H74" test/db/restore-incomplete.test.js)" = "5" ] || { echo "REFUSING: restore-incomplete.test.js does not carry the READY's 5 cells" >&2; exit 74; }
# VSP75
must "$H75" server/backupTables.js 'const BACKUP_TABLES = ['
must "$H75" server/backupTables.js 'const BACKUP_EXCLUDED = {'
[ "$(p show "${H75}:server/backupTables.js" | awk '/const BACKUP_TABLES = \[/{f=1;next} f&&/^\];/{exit} f' | grep -cE "^  '[a-z_]+',")" = "20" ] \
  || { echo "REFUSING: backupTables.js at VSP75 does not list exactly 20 tables" >&2; exit 74; }
[ "$(p show "${H75}:server/backupTables.js" | awk '/const BACKUP_EXCLUDED = \{/{f=1;next} f&&/^\};/{exit} f' | grep -cE '^  [a-z_]+:')" = "1" ] \
  && must "$H75" server/backupTables.js '  session:' || { echo "REFUSING: BACKUP_EXCLUDED at VSP75 is not exactly {session}" >&2; exit 74; }
for T in 'quotes' 'quote_approvals' 'reminders' 'feedback_coordinator_state' 'integration_settings'; do
  p show "${H75}:server/backupTables.js" | grep -qE "^  '${T}'," || { echo "REFUSING: backupTables.js lacks '$T'" >&2; exit 74; }
done
must "$H75" server/dbBackup.js "require('./backupTables')"
must "$H75" server/dbBackup.js 'SELECT row_to_json(t) AS r FROM'
must "$H75" server/dbBackup.js 'failed_tables: Object.keys(tables).filter(t => tables[t].error),'
must "$H75" server/dbBackup.js "incomplete: { title: 'DB Backup INCOMPLETE', priority: '4', tags: 'warning,floppy_disk' },"
must "$H75" server/dbRestore.js "const { BACKUP_TABLES: RESTORE_ORDER } = require('./backupTables');"
must "$H75" server/dbRestore.js 'JSON.stringify(row[c])'
must "$MAINH" server/dbBackup.js 'failed_tables: Object.keys(tables).filter(t => tables[t].error),'
mustnot "$MAINH" server/dbBackup.js 'backupTables'
[ "$(ntests "$H75" test/db/backup-coverage.test.js)" = "5" ] || { echo "REFUSING: backup-coverage.test.js does not carry the READY's 5 cells" >&2; exit 74; }
# the semantic-conflict fix (§N4): dbBackup.test.js changed ON VSP75, still 5 cells, still asserting INCOMPLETE and the blob marker.
DBT_MAIN="$(p rev-parse "${MAINH}:server/dbBackup.test.js" 2>/dev/null)"; DBT_75="$(p rev-parse "${H75}:server/dbBackup.test.js" 2>/dev/null)"
[ -n "$DBT_MAIN" ] || { echo "REFUSING: server/dbBackup.test.js is not on main — VSP-68 is not merged" >&2; exit 74; }
case "$DBT_MAIN" in "$DBBACKUP_TEST_68"*) ;; *) echo "NOTE: main's dbBackup.test.js is ${DBT_MAIN:0:7}, not VSP-68's 4fb902e — §N4's pre-fix-stub control must use 4fb902e from the object store" >&2 ;; esac
[ "$DBT_75" != "$DBT_MAIN" ] || { echo "REFUSING: VSP75 did not change server/dbBackup.test.js — the semantic conflict is not fixed on the VSP-75 branch (Tuesday's ruling)" >&2; exit 74; }
[ "$(ntests "$H75" server/dbBackup.test.js)" = "5" ] || { echo "REFUSING: VSP75's dbBackup.test.js does not carry VSP-68's 5 cells — a cell was dropped or added; re-brief" >&2; exit 74; }
for T in "'DB Backup INCOMPLETE'" "'DB Backup OK'" "'DB Backup FAILED'" 'failedTables' 'failed_tables'; do
  must "$H75" server/dbBackup.test.js "$T"
done
# VSP69
for T in 'const DISPATCH_PER_TICK = 50;' 'FOR UPDATE SKIP LOCKED' 'ORDER BY due_at, id LIMIT 1' 'async function sendReminder(rem) {' \
         "const cutoff = (await query('SELECT NOW() AS now')).rows[0].now;" "console.warn('[reminders] dispatch failed:', e.message);"; do
  must "$H69" server/reminders/dispatcher.js "$T"
done
mustnot "$MAINH" server/reminders/dispatcher.js 'DISPATCH_PER_TICK'
[ "$(ntests "$H69" test/db/dispatch-once.test.js)" = "5" ] || { echo "REFUSING: dispatch-once.test.js does not carry the READY's 5 cells" >&2; exit 74; }
must "$H69" test/db/dispatch-once.test.js 'vsp69.invalid'

# 63 — main has not moved in VSP-69's files; VSP74/75 do not touch them; VSP69 does not touch VSP-74/75's.
[ "$(p rev-parse "${MAINH}:server/reminders/dispatcher.js" 2>/dev/null)" = "$DISPATCH_BLOB_MAIN" ] \
  || { echo "REFUSING: main's server/reminders/dispatcher.js is not 283be27 — main moved in VSP-69's file; forward-merge VSP-69 and re-pin (the gate re-derives at stamp)" >&2; exit 63; }
[ "$(p rev-parse "${H69}:server/reminders/dispatcher.js")" = "$DISPATCH_BLOB_69" ] || echo "NOTE: VSP69's dispatcher.js is not 7a67be9 — the brief's line references are stale" >&2
p cat-file -e "${MAINH}:test/db/dispatch-once.test.js" 2>/dev/null && { echo "REFUSING: main already carries test/db/dispatch-once.test.js — re-brief" >&2; exit 63; }
for ID in VSP74 VSP75; do
  H="$(fld "$ID" 4)"
  [ "$(p rev-parse "${H}:server/reminders/dispatcher.js")" = "$DISPATCH_BLOB_MAIN" ] || { echo "REFUSING: $ID changes dispatcher.js — only VSP69 should" >&2; exit 63; }
done
for F in server/dbRestore.js server/dbBackup.js server/dbBackup.test.js; do
  [ "$(p rev-parse "${H69}:$F" 2>/dev/null)" = "$(p rev-parse "${ANCHOR_OLDMAIN}:$F" 2>/dev/null)" ] || { echo "REFUSING: VSP69 changes $F — only VSP74/VSP75 should" >&2; exit 63; }
done
for T in 'npm ci --offline --ignore-scripts' 'entry by entry' 'never npm audit'; do
  grep -qiF "$T" "$BRIEF" || { echo "REFUSING: brief lacks the dependency rule '$T'" >&2; exit 63; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the dependency rule '$T'" >&2; exit 63 ;; esac
done

# 31 — the READYs are on disk and their NOT TESTED lines are carried verbatim; the prior gates' findings are on disk.
nt_lines() { awk '/^NOT TESTED:?$/{f=1;next} f&&/^- /{print} f&&/^[A-Z][A-Z]+[ :,]/{exit}' "$1"; }
for PAIR in "$READY74:3" "$READY75:4" "$READY69:3"; do
  RF="${PAIR%:*}"; WANT="${PAIR##*:}"
  [ -s "$RF" ] || { echo "REFUSING: a READY mail is not on disk: $RF" >&2; exit 31; }
  [ "$(nt_lines "$RF" | wc -l | tr -d ' ')" = "$WANT" ] || { echo "REFUSING: $RF's NOT TESTED list is not the $WANT lines the brief carries" >&2; exit 31; }
  while IFS= read -r T; do
    [ -n "$T" ] || continue
    grep -qxF -- "$T" "$BRIEF" || { echo "REFUSING: the brief does not carry this NOT TESTED line verbatim: $T" >&2; exit 31; }
  done <<< "$(nt_lines "$RF")"
done
grep -qF 'READY FOR QA: VSP-74 (F-B) @ bf5bdc0' "$READY74" || { echo "REFUSING: the VSP-74 READY does not name bf5bdc0" >&2; exit 31; }
grep -qF 'READY FOR QA: VSP-75 (F-A) @ 0d7a2fb' "$READY75" || { echo "REFUSING: the VSP-75 READY does not name 0d7a2fb" >&2; exit 31; }
grep -qF 'READY FOR QA: VSP-69 @ 3ede8ed' "$READY69" || { echo "REFUSING: the VSP-69 READY does not name 3ede8ed" >&2; exit 31; }
for T in 'VSP-74 NOT TESTED' 'VSP-75 NOT TESTED' 'VSP-69 NOT TESTED' 'F-A' 'F-B' 'pre-forward-merge READY heads, superseded at stamp'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: the brief does not carry '$T'" >&2; exit 31; }
done
[ -s "$CLAR" ] || { echo "REFUSING: Vision CLARIFICATIONS.md absent: $CLAR" >&2; exit 31; }
for C in 'C-01.' 'C-06.'; do grep -qF "**$C" "$CLAR" || { echo "REFUSING: $CLAR lacks $C" >&2; exit 31; }; done
grep -qF '**C-07.' "$CLAR" && echo "NOTE: Vision CLARIFICATIONS now has a C-07 — the brief says C-01..C-06; read it before launch" >&2
grep -qiE 'VSP-(69|74|75)' "$CLAR" && echo "NOTE: Vision CLARIFICATIONS now mentions a gate-12 ticket — the brief says none does; read it before launch" >&2
[ -s "$G9_REPORT" ] || { echo "REFUSING: gate 9's report is absent: $G9_REPORT" >&2; exit 31; }
grep -qF '(h) Dispatcher re-send' "$G9_REPORT" || { echo "REFUSING: gate 9's report does not carry §N.4(h) — VSP-69 has no source" >&2; exit 31; }
[ -s "$G11_REPORT" ] || { echo "REFUSING: gate 11's report is absent ($G11_REPORT) — gate 12 runs AFTER gate 11's verdict (Tuesday's sequencing)" >&2; exit 31; }
grep -qE 'NO-GO|GO' "$G11_REPORT" || { echo "REFUSING: gate 11's report carries no verdict" >&2; exit 31; }
for D in "$G9_DIR" "$G10_DIR" "$G11_DIR"; do
  grep -qF "$D" "$BRIEF" || { echo "REFUSING: the brief does not name $D" >&2; exit 31; }
  case "$PROMPT" in *"$D"*) ;; *) echo "REFUSING: the prompt does not name $D" >&2; exit 31 ;; esac
done
[ -d "$G11_DIR/evidence/tools" ] || echo "NOTE: gate 11 has no evidence/tools/ — the gate falls back to gate 10's copies (brief §PRIOR ROUND)" >&2
for H in qa-g10-stallproxy.cjs qa-harness-g10-vsp.cjs qa-g10-lib.cjs qa-mkdb.cjs qa-dbcheck.cjs qa-floorcount.py qa-io1-preload-fetchguard.cjs \
         qa-run.py run-suite.sh mktree-portal.sh lockcmp.py lockwalk.py specsets.py tapsets.py; do
  [ -s "$G10_TOOLS/$H" ] || { echo "REFUSING: gate 10's tool $H is not on disk — the brief names it as the fallback" >&2; exit 31; }
  grep -qF -- "$H" "$BRIEF" || { echo "REFUSING: the brief does not name gate 10's tool $H" >&2; exit 31; }
done

# 39 — the floor instrument is on disk and named.
[ -s "$G10_FLOOR" ] || { echo "REFUSING: gate 10's floor instrument missing: $G10_FLOOR" >&2; exit 39; }
grep -qF 'qa-floorcount.py' "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument qa-floorcount.py" >&2; exit 39; }

# 41 — the answer route exists (Tuesday adds 'QA/Vision-gate12|tuesday-agent@agentmail.to|no' at launch).
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || {
  echo "REFUSING: no '${ROUTE_NAME}|tuesday-agent@agentmail.to|…' line in $ROUTING — answers to the gate would have no route. Add it (pattern: the QA/Vision-gate11 line) before launch." >&2; exit 41; }

# 10 / 17 — report path named in both; no stale report.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

# 12 — tiers declared in both.
for T in '**VSP74** at `' '**VSP75** at `' '**VSP69** at `3ede8ed`'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not declare the target line: $T" >&2; exit 12; }
done
for ID in VSP74 VSP75 VSP69; do
  grep -qE "^- \*\*${ID}\*\* at \`[^\`]+\` — \*\*TIER 1" "$BRIEF" || { echo "REFUSING: brief does not declare $ID TIER 1" >&2; exit 12; }
  case "$PROMPT" in *"$ID (TIER 1"*) ;; *) echo "REFUSING: prompt does not declare: $ID (TIER 1" >&2; exit 12 ;; esac
done

# 78 — the commission's requirements, in both.
for T in 'forward-merge' 'never rebase' 'CASCADE' 'SET NULL' 'allow-incomplete' 'd2531ea' 'cad19ab' '3ede8ed' '0d992e0' 'census' 'round trip' \
         'populated' 'TRUNCATE' 'secret' 'M2' 'SKIP LOCKED' 'query bound' 'black hole' 'process death' 'churn' 'poison' 'not papered over' \
         'INCOMPLETE' 'dump query' 'FK-order' 'recorder' 'ROUND 1' 'two-NO-GO cap' 'merged tree' 'BACKLOG' 'SETS, NOT COUNTS' 'Node 20' 'NODE20-LEG' \
         'UNMEASURED' 'PRODUCTION IS LIVE' 'datasec-sales-db.postgres.database.azure.com' 'e2e:pro' 'real backup'; do
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
WORDS="merge-tree NOT%TESTED env%-i bash createApp() initDb() 0d992e0 d2531ea cad19ab 3ede8ed work-g12 vsp_qa_g12 _test
FOREGROUND MEASURED%AT%RUNTIME PROBED READ%ONLY start%/%mid%/%end CI VOID node%--check"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## Charter' '^## RULED BY KAM, AND SETTLED' '^## PRIOR ROUND' '^PRIOR ROUND: ' 'ITS REPORT IS ON DISK AT:' '^## PIN' \
         '^## WRONG OR UNVERIFIABLE' '^## THE READYs' '^## 2a. LEGITIMATE SHAPES' '^## N1. TARGET VSP74' '^## N2. TARGET VSP75' \
         '^## N3. TARGET VSP69' '^## N4. THE SEMANTIC CONFLICT' '^## N5. SHARED' '^## 12. The merge' '^## 13. FLOOR' \
         "^## TUESDAY'S RULINGS AT STAMP" '^## 14. Output' '^PROVENANCE:' '^GATE11-MERGED: '; do
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
for T in 'EXCLUSIVE' 'work-g12'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the tree-exclusivity rule '$T'" >&2; exit 61; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the tree-exclusivity rule '$T'" >&2; exit 61 ;; esac
done
for T in '4848' '8080' '47787' 'env -i' 'AGENTMAIL_API_KEY' 'AGENTMAIL_INBOX' 'no jest lock' 'salesportal_test' '5433' 'vsp71_' 'vsp73_'; do
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

# 45 — Tuesday has decided the Node 20 leg; the prompt is told which.
NODE20="$(sed -n 's/^NODE20-LEG: \([A-Z-]*\)[[:space:]]*$/\1/p' "$BRIEF" | head -1)"
case "$NODE20" in
  NOT-RUN|DOCKER-PULL-NEVER) ;;
  "$PH_NODE20") echo "REFUSING: the brief's NODE20-LEG line is still ${PH_NODE20} — Tuesday decides NOT-RUN or DOCKER-PULL-NEVER before launch (brief top, and §N5.4)" >&2; exit 45 ;;
  *) echo "REFUSING: the brief's NODE20-LEG line reads '${NODE20:-<missing>}' — it must be exactly NOT-RUN or DOCKER-PULL-NEVER" >&2; exit 45 ;;
esac

# 44 — local Postgres is listening on :5433. The launcher never starts a container; the Vision seat does.
lsof -nP -iTCP:5433 -sTCP:LISTEN >/dev/null 2>&1 \
  || { echo "REFUSING: nothing LISTENs on :5433 — the gate's runtime legs would all be NOT RUN. Ask the Vision seat to start its local vsp-dev-db (never from this launcher, never from the gate), then re-run --check." >&2; exit 44; }

# 32 — the coordinator stamps the self-check (line AND note) and every @STAMP@. LAST, so --check shows every other guard first.
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "guards pass (40 9 6 7 8 18 22 74 63 31 39 41 10 17 12 78 13 14 15 20 70 19 24 53 60 61 62 64 69 75 38 45 44); self-check NOT stamped." >&2
  echo "REFUSING: the brief still carries ${PH_STAMP} (heads, Self-check line or note, or TUESDAY'S RULINGS) — the coordinator re-reads end-to-end and stamps all of them before launch" >&2; exit 32
fi

STUBFIX="$(printf '%s ' $EXTRA75)"; [ -n "${STUBFIX// /}" ] || STUBFIX='none (the fix is inside a merge commit)'
PIN_BLOCK="$(printf 'PINNED HEADS — verified by the launcher at %s (cat-file, base ancestry and merge-base, not-already-on-main, commit counts; VSP74/VSP75 fully forward-merged, READY heads bf5bdc0/0d7a2fb contained, merges forward-only; the five GATE11-MERGED shas on main; main dispatcher.js = 283be27; git ls-remote origin for every row):\n' "$PIN_TS"
  printf '%s\n' "$PIN" | awk -F'\t' '{ printf "  %-7s %-7s %-50s %s  base %s  commits %s\n", $1, $2, $3, $4, ($5=="-"?"-":substr($5,1,12)), $6 }'
  printf '  STALE-BASE rows (VSP69 expected; merge at queue time):%s\n' "${STALE:- none}"
  printf '  VSP75 stub-fix commit over the READY chain: %s\n' "$STUBFIX"
  printf 'NODE20-LEG, as decided in the brief: %s\n' "$NODE20")"

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  printf '%s\n' "$PIN_BLOCK"
  echo "  PIN parsed, four rows, no placeholder (40); GATE11-MERGED five shas on main, 12138cb on main, main != 0d992e0 (9); READY chains intact, never rebased, forward merges only, VSP69 one linear commit (9)"
  echo "  commits/bases/counts, VSP74/75 0 behind main (6 7 8); origin re-read $PIN_TS (18); file sets 3/7/3 + refactors single-file (22)"
  echo "  content: VSP-74 in VSP74+VSP75, 20 tables + {session}, VSP-68+VSP-75 dbBackup lines, stub changed on VSP75 with 5 cells, dispatcher lines, test( 5/5/5 (74)"
  echo "  main dispatcher.js 283be27, file ownership disjoint (63); READYs' NOT TESTED verbatim + gate 9 (h) + gate 11 report + tools (31); floor (39); route $ROUTE_NAME (41); report absent (17)"
  echo "  tiers (12); commission requirements (78); directive/brief/placeholders/mail/key/questions/safety (13 14 15 20 70); words + sections (19); no server path (24); standing rules (53 60 61 62 64 69 75); seats $NEG_SEATS (38); NODE20 $NODE20 (45); :5433 listening (44); stamped (32)"
  exit 0
fi

# 11 — no inherited identity: this gate needs neither az nor gh, so both point at fresh EMPTY directories.
ID_TMP="$(mktemp -d "${TMPDIR:-/tmp}/qa-vision-gate12-id.XXXXXX")" || { echo "REFUSING: cannot create the empty identity dir" >&2; exit 11; }
mkdir -p "$ID_TMP/azure-empty" "$ID_TMP/gh-empty" || { echo "REFUSING: cannot create the empty identity dirs under $ID_TMP" >&2; exit 11; }
{ [ -z "$(ls -A "$ID_TMP/azure-empty")" ] && [ -z "$(ls -A "$ID_TMP/gh-empty")" ]; } || { echo "REFUSING: the identity dirs under $ID_TMP are not empty" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_TMP/azure-empty"
export GH_CONFIG_DIR="$ID_TMP/gh-empty"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"
# 64 (cont.) — nothing a product process could use to reach a real provider or database is inherited from this shell.
unset DATABASE_URL TEST_DATABASE_URL DB_QUERY_TIMEOUT_MS DB_CONNECT_TIMEOUT_MS AGENTMAIL_API_KEY AGENTMAIL_INBOX ACS_CONNECTION_STRING \
      ACS_EMAIL_CONNECTION_STRING ACS_EMAIL_SENDER MAIL_SENDER TABLES_CONNECTION_STRING AZURE_BACKUP_CONN_STR AZURE_BACKUP_CONTAINER BACKUP_CRON \
      REMINDER_CRON SESSION_SECRET HPAM_WORD ADVANCED_UNLOCK_SECRET SALES_COPY_EMAIL FEEDBACK_NOTIFY_EMAIL FEEDBACK_NOTIFY_EMAILS APPROVALS_INBOX \
      NTFY_TOPIC NTFY_SERVER LEAD_BOT_API_KEY WEBSITE_SITE_NAME COORDINATOR_SECRET PORT NODE_ENV
echo "identity: AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR GH_CONFIG_DIR=$GH_CONFIG_DIR (empty) CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR" >&2

PROMPT="$PROMPT

$PIN_BLOCK"
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$PROMPT"
