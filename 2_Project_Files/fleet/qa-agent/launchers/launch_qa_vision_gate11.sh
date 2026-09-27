#!/bin/bash
# launch_qa_vision_gate11.sh — cross-project QA agent, ONE gate (Vision gate 11, drafted 2026-09-28) on
# Datasec/Vision_Sales_Portal, FIVE targets, FIVE verdicts plus one merged-tree line, all one or two commits on portal main 0d992e0:
#   VSP66  fix/vsp-66-checkout-link-death-2026-09-28     held-client link death (server/db.js guard())            TIER 1
#   VSP71  fix/vsp-71-session-index-boot-2026-09-28      session index cannot fail a boot (schema.sql, initDb.js)  TIER 1
#   VSP70  fix/vsp-70-restore-rollback-error-2026-09-28  restore throws the first error (server/dbRestore.js)      TIER 2 (Tuesday's ruling)
#   VSP68  fix/vsp-68-backup-missing-table-2026-09-28    backup INCOMPLETE alert (server/dbBackup.js)              TIER 2 (Tuesday's ruling)
#   VSP73  fix/vsp-73-backup-dump-replay-2026-09-28      backup-db dump replays (server/routes/admin.js)          TIER 2 (Tuesday's ruling)
#
# THE HEADS LIVE IN ONE PLACE: the brief's PIN-HEADS table. This launcher PARSES it (carries no head of its own), refuses any
# placeholder, verifies every row against the object store and against origin by `git ls-remote` NOW, and appends the verified
# table to the agent's prompt. The only shas it carries are GATED ANCHORS: 0d992e0 (gate 10's GO'd VSP-65 head, now main; every
# target must contain it), b5c3e8d (its single parent) and 12138cb (VSP70's refactor, which must be VSP70's head~1).
#
# PRODUCTION IS LIVE for this project (datasec-sales-portal-rg). The gate is local Postgres only: no az, no deploy, no app
# setting, no connection to the production database. Findings only.
#
# PATTERN: launch_qa_vision_gate10.sh (PIN parse, anchors, file sets, content guards, embedded prompt, --check, stamp LAST).
# CHANGES vs gate 10, each deliberate:
#   - exit 40: PIN rows are exactly MAIN-P + VSP66 + VSP71 + VSP70 + VSP68 + VSP73 (six rows, five targets).
#   - exit 9:  anchors — main's parent is b5c3e8d (NOTE if main moved); every target contains 0d992e0; VSP70 head~1 = 12138cb whose parent
#              is 0d992e0; no target commit is a merge.
#   - exit 22: exact file sets per target (4 / 5 / 3 / 3 / 3 files over main; 12138cb touches dbRestore.js only).
#   - exit 74: per-target content at its head and ABSENT at main; the six pool.connect() holders at main and at every head but VSP70
#              (five there, plus clearTables' db.connect()); test( counts 6/5/4/5/4; the VSP-71 test's roles and password and the
#              VSP-73 test's database (brief WRONG (h)); gate 10's S7b arm and rst/armNext proxy verbs (the instruments the brief names).
#   - exit 63: shared files the same blob at main and every head; each target-owned file changed ONLY by its own target.
#   - exit 31: the five READYs on disk with their NOT TESTED lines carried verbatim (4 / 5 / 2 / 3 / 2); gate 10's GO and R2-O1; gate 9's
#              VSP65-O1 line and S7b evidence; the gate-10 tools the brief tells the gate to copy.
#   - exit 38: negative-control seats = Tuesday, NexusAI, the LIVE Vision builder seat.
#   - exit 41: the answer route QA/Vision-gate11 exists in fleet/inbox_routing.conf (Tuesday adds it at launch).
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/Vision-gate11' "bash '<this file>'"), NEVER nohup.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Contains a legitimate `cd` (into the QA project, at exec).
# READ-ONLY toward the repo: only cat-file, rev-parse, merge-base, log, rev-list, diff, show, grep, ls-tree, ls-remote.
# --check is READ-ONLY: it runs every guard and exits before any identity dir is made or any agent is started.
# Usage: launch_qa_vision_gate11.sh [--check]
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
BRIEF="$BRIEFS/2026-09-28_vision-gate11-vsp66-vsp71.md"
READY66="$BRIEFS/2026-09-28_vision-vsp66-READY-mail.txt"
READY71="$BRIEFS/2026-09-28_vision-vsp71-READY-mail.txt"
READY70="$BRIEFS/2026-09-28_vision-vsp70-READY-mail.txt"
READY68="$BRIEFS/2026-09-28_vision-vsp68-READY-mail.txt"
READY73="$BRIEFS/2026-09-28_vision-vsp73-READY-mail.txt"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
VSP='/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal'
P_REPO="$VSP/2_Project_Files"
CLAR="$VSP/1_Project_Definition/CLARIFICATIONS.md"
REPORTS="$QA_DIR/projects/vision/reports"
G9_DIR="$REPORTS/2026-09-27-vision-gate9-vsp65-qqpurge"
G9_REPORT="$G9_DIR/report.md"
G10_DIR="$REPORTS/2026-09-27-vision-gate10-vsp65-r2"
G10_REPORT="$G10_DIR/report.md"
G10_TOOLS="$G10_DIR/evidence/tools"
G10_FLOOR="$G10_TOOLS/qa-floorcount.py"
REPORT="$REPORTS/2026-09-28-vision-gate11-five-targets/report.md"
ROUTE_NAME='QA/Vision-gate11'
NEG_SEATS='44115 20317 67871'   # Tuesday (%0), NexusAI (%22), the LIVE Vision builder seat (%33) — at drafting, 2026-09-28 06:17 AEST
# Gated anchors (not heads).
ANCHOR_G10='0d992e09ebe0830dbe414aa73ca9a17a1be6c480'      # gate 10's GO'd VSP-65 round-2 head; main by fast-forward
ANCHOR_G10P='b5c3e8d244822df180c34007a44a25f44eb64387'     # its single parent
ANCHOR_R70='12138cb46acb8201999ace84cb8f9357ee63aac7'      # VSP70's refactor commit, the base of its fix (its red is re-derived here)

SUBJECT_STEM='[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 11'
QUESTION_SUBJ='[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>'
ANSWER_PREFIX='[Tuesday -> QA/Vision-gate11] ANSWER'

p() { git --no-optional-locks -C "$P_REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE gate (Vision gate 11) on Datasec/Vision_Sales_Portal with FIVE targets and FIVE verdicts, each GO or NO-GO, plus one merged-tree line. All five are branches of one or two commits on portal main 0d992e0, in the SALES PORTAL repo.

READ YOUR COMMISSION FIRST, whole: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-28_vision-gate11-vsp66-vsp71.md
Then read the charter it names, the Vision CLARIFICATIONS (C-01..C-06; none covers these tickets), the project's CLAUDE.md (/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/CLAUDE.md; its deploy commands are not for you), the builder's five READY mails (/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-28_vision-vsp66-READY-mail.txt, -vsp71-, -vsp70-, -vsp68- and -vsp73-READY-mail.txt beside it), and the two prior reports whose findings these tickets fix and whose instruments you reuse by copy: gate 10 /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-27-vision-gate10-vsp65-r2 (report.md; evidence/tools/) and gate 9 /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-27-vision-gate9-vsp65-qqpurge (report.md; evidence/vsp/*s7b*). Every builder statement is a CLAIM, never evidence. The five READYs landed within about 15 minutes, the first about 5 minutes after the builder seat booted: RE-DERIVE every red, every mutant and every suite set yourself. Verify every PRIOR WORK claim against git history and the prior gates' evidence, never against the brief.

THE TARGETS.
  VSP66 (TIER 1) = Jira VSP-66 = gate 9's VSP65-O1: a link death while a pool.connect() caller holds its client raised uncaughtException and the portal exited. The fix adds an error listener to every checkout in the pool wrapper and removes it on release. Every database call in the live portal goes through it.
  VSP71 (TIER 1) = Jira VSP-71 = gate 10's VSP65-R2-O1: with the session index missing, the boot's CREATE INDEX failed the boot (42501 as a non-owner; DB_QUERY_TIMEOUT with a write held past the bound). The fix wraps the index build in its own exception block under a 2 s lock_timeout, set local and put back, and initDb warns when the index is missing. Every boot runs it.
  VSP70 (TIER 2, Tuesday's ruling) = Jira VSP-70 = gate 9's N.4(c): the restore CLI's ROLLBACK error replaced the error that failed the restore. Two commits: the refactor 12138cb, then the fix. Its red is re-derived at 12138cb, not at main.
  VSP68 (TIER 2, Tuesday's ruling) = Jira VSP-68 = gate 9's N.4(b): a backup missing a whole table was announced "DB Backup OK". The fix adds an INCOMPLETE alert, failed_tables in the backup and failedTables on the blob.
  VSP73 (TIER 2, Tuesday's ruling) = Jira VSP-73 = gate 10's VSP65-R2-O7: the admin backup-db SQL dump could not replay into a fresh database (42P01 on a sequence) and carried no indexes. The fix emits sequences first, every index after its rows, and OWNED BY. The dump carries customer data from YOUR OWN seeded database only: never read, open or keep a real dump.
  OUT OF SCOPE, ruled by Tuesday, NOT misses: the VSP-68 READY's F-A (the backup omits most PRO tables) and F-B (a restore empties a table whose dump failed), and VSP-73's NOT FIXED list (FK / CHECK constraints, typmods).

WHAT THE BRIEF REQUIRES, in short (the brief is the authority):
  (1) VSP66: the child-process fault cells (terminate, in-flight, RST, FIN) RE-DERIVED on gate 10's own proxy, copied and re-pointed, with the terminate and FIN shapes you add; the red at 0d992e0 before any green at the head (the positive control: 0d992e0 must crash on the same instrument). Real callers holding the client end to end: gate 9's S7b on the generate route, the reminder dispatcher blocked on a recorder inside its transaction, the admin backup-db route. Does the dead client ever get reused (the in-flight release window, N >= 20)? Is the death logged once on every fault shape, counting every [db] line of either kind? Listener hygiene at 20,000 checkouts. A fault cell whose fault did not land while the client was held is VOID, not green.
  (2) VSP71: gate 10's (a) non-owner 42501 and (b) a held write re-measured with gate 10's own instruments, at the shipped bound, at 6000, and at 2000 and 1500 as the named residual (the 2 s lock_timeout is above the usual shrunk bound). The rest of schema.sql commits. lock_timeout is RESTORED after the block, proven on the same backend with a session-level sentinel and a positive-control mutant. The production-shaped no-op boot of gate 10 N.2(b) is still a no-op with no warning. The interaction with the backup-db dump route. All owner cells as NON-superuser roles.
  Every red-proof: fresh tree per arm, asserted edits, node --check rc quoted; a red from a mutant that does not parse is VOID.
  (3) VSP70: the lines that prove the DELETE and INSERT path unchanged; the builder's four cells and two mutants re-derived at 12138cb; ONE real-Postgres cell of the masking shape (a DELETE that fails for real, then a ROLLBACK on a dead link, per the brief's armNext shape); the RST variant only on the merged tree.
  (4) VSP68: the builder's five cells and three mutants re-derived; ONE cell with a REAL Postgres table-dump failure producing the INCOMPLETE alert on YOUR loopback recorder, the partial backup still uploaded to YOUR blob recorder, and the blob metadata shape quoted; an error with an empty message.
  (5) VSP73: its red at 0d992e0 (42P01 on a sequence) and its three mutants re-derived; a dump through the REAL route replayed as ONE query into a fresh database of your own, compared with its source from the catalogs; replay over an existing database as owner and as non-owner; and on the MERGED tree, replayed dump + boot gives the session index and no VSP-71 warning.
  (6) THE MERGED TREE: all five x main via merge-tree in your OWN object dir. Every pair conflicts in BACKLOG.md only: predict and measure the five-way conflict, resolve it in your own tree only, prove the code files equal main plus each target's own blobs, and run the suites as sets vs main 0d992e0 on the merged tree.
  (7) SUITES AS SETS, NOT COUNTS, at every head and the merged tree vs main, plus CI's coverage command run locally (label it: not CI). The Node 20 leg follows the NODE20-LEG line in the brief exactly.
  (8) CI is UNMEASURED: this project's gh is not authenticated and you must not use gh. Say so, and name CI's Node 22 coverage gate and its e2e:pro step as the first reads at merge.

LOCAL POSTGRES ONLY. PRODUCTION IS LIVE for this project. NEVER the live portal (datasec-sales-portal.azurewebsites.net, datasec-sales-portal-rg, its Postgres datasec-sales-db.postgres.database.azure.com, its key vault): no request, no DB connection, not even a GET. No az of any kind, no deploy, no app-setting change. Never open a production dump or anything under the project's 4_Credentials. Real sends are OFF: the dispatcher, the email sender and the backup notifier run only against recorders you wrote; Azure Blob Storage is replaced by YOUR recorder, and ntfy goes only to YOUR loopback recorder.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT from the object store (git archive into a fresh mktemp -d under projects/vision/work-g11/). Each tree is EXCLUSIVE to this gate and to one purpose; never touch work/ or work-g2 .. work-g10. Gate 10's tools are copied into YOUR evidence folder and re-pointed (they hard-code gate 10's paths and ENFORCE the vsp_qa_g10_ prefix); never run from, edit or write into gate 9's or gate 10's copies. Dependencies: npm ci --offline --ignore-scripts only, then prove node_modules/.package-lock.json against the lockfile entry by entry (lockcmp.py AND lockwalk.py). Never npm install, never npm audit, never npx anything not already in the tree. In the repo use ONLY read verbs (show, log, diff, ls-remote, rev-parse, ls-tree, cat-file, grep, merge-base, archive); never fetch, pull, checkout, switch, worktree, commit, stash, reset, clean or gc. Run git merge-tree --write-tree only from the gate's OWN object dir (GIT_OBJECT_DIRECTORY = your own mktemp -d, alternates = the repo's objects), or skip it and say so. Findings-only: no writes in the portal repo, none inside Vision_Sales_Portal, none in gate 1-10's report folders or trees. Never rm: quarantine. Run every loop and every git show <sha>:<path> under bash. CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY: a control derived from the run it validates is not a control.

FLOOR DISCIPLINE. Vision has no jest lock; never borrow NexusAI's. Never use ports 4848, 8080 or 47787, nor 127.0.0.1:49162 / 49164 / 49166; take every port from the kernel and bind 127.0.0.1. Never start the portal's own entry point (it binds all interfaces); use the real createApp() and initDb() in your harness. Postgres is the local container on 127.0.0.1:5433, and ONLY databases you create: vsp_qa_g11_<epoch> and vsp_qa_g11_<epoch>_test (the test name MUST end in _test); never salesportal, salesportal_test (the Vision builder seat is LIVE and uses it), any vsp_qa_g1..g10 database, the builder's vsp_bf1_*, or any vsp71_* / vsp73_* database you did not cause. The VSP-71 and VSP-73 test files create and drop their own vsp71_* roles and databases and a vsp73_* database inside test:db; the brief's floor section and Tuesday's ruling govern that. Roles are cluster-global: create one only inside a transaction you roll back, or name it vsp_qa_g11_* and list it; gate 10's vsp_qa_g10_* roles are not yours. Every owner cell runs as NON-superuser roles (the compose user is a superuser and bypasses ownership). Event triggers only in your own databases; never ALTER SYSTEM or change server settings. The module's default URL is the builder's dev database, so give every product process YOUR DATABASE_URL and TEST_DATABASE_URL explicitly and print the database each one reached. Release every lock and direct session you open in a finally. No docker command at all, except the Node 20 exception under the NODE20-LEG line. Every product process runs under env -i with an explicit allowlist, NODE_ENV never production. Never set AGENTMAIL_API_KEY or AGENTMAIL_INBOX in a product process, nor any real ACS_* or MAIL_SENDER, AZURE_BACKUP_CONN_STR, TABLES_CONNECTION_STRING, SALES_COPY_EMAIL, a real NTFY_TOPIC, LEAD_BOT_API_KEY or WEBSITE_SITE_NAME; print each product process's env KEY NAMES and assert none is forbidden. NTFY_SERVER=http://ntfy.invalid except the brief's loopback recorder; never contact ntfy.sh; stub fetch to throw on any other URL. Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid, with the brief's negative-control seats classifying FOREIGN in the same run. A zero is reportable only beside an ATTACHED control that fired in the same window. Other gates and the builder are live on this box: record the load average beside every timing number; a latency result with no load figure is not a measurement.
DEADLINE AND HEARTBEAT: every step has a written DEADLINE built into your runner (there is no timeout binary here) and releases its servers, proxies, recorders, sessions, locks, roles and children in a finally. Log a HEARTBEAT line at least every 2 minutes; a step with no heartbeat for 5 minutes is aborted and reported, never waited on. Deadlines: requests at the shrunk bound 20 s; requests at the SHIPPED bounds 120 s; a child-process fault cell 30 s; the boot-lock arms 120 s each; the release-window race arm 180 s; one test:db file 180 s; a whole test:db run 420 s. Nothing above 420 s.

QUESTIONS: your routing name is QA/Vision-gate11. If you must ask, mail tuesday-agent@agentmail.to with the subject "[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>" and proceed on the safest reading without waiting. Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/Vision-gate11] ANSWER"; read it with your verdict key. Never wednesday-agent@. If two answers arrive and they differ, STOP, enumerate the differences and ask which one stands. If a response is cut off by a safety check, record it and continue with the next item; this is authorised defensive QA of Datasec's own product on loopback. Record every question, reading and answer in the report.

Write your report to: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-28-vision-gate11-five-targets/report.md

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with a subject beginning exactly:
[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 11: VSP66 @ 1976275 <GO | NO-GO> · VSP71 @ 5bdaeae <GO | NO-GO> · VSP70 @ 10ba4bb <GO | NO-GO> · VSP68 @ 7ef698d <GO | NO-GO> · VSP73 @ 6d7ea73 <GO | NO-GO> · merged <CLEAN | BACKLOG-ONLY | CONFLICT>
Lead the body with five sentences, one per target, as the brief's section 14 words them, then one line on the merged tree. You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no credentials directory of its own. Use it only in your own mail calls, with a client timeout. Never put the key or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice.

Report every pinned head and main as three timestamped readings (start / mid / end), with the branch name beside each. Include the verbatim operator strings the brief lists: the held-client death log line and any idle-client twin, the VSP-71 warning and the Postgres WARNING with its SQLSTATE and SELECT version(), the ROLLBACK-failed line with the first error thrown, the INCOMPLETE alert and the blob metadata, and the 42P01 of the old dump. Then one paragraph on the queue: the merge-tree results, the BACKLOG resolution, the cells to re-run on the merged head, and CI at merge.

Rule 2 stands: what you did NOT test is first-class output. Write a NOT TESTED section that covers at least CI (UNMEASURED), production's session-table owner, index, Postgres version and search_path, production's feedback table, a real App Service restart and multiple real instances, a real stalled Azure Postgres / TLS / failover, real Azure Blob Storage and real ntfy, the restore CLI end to end, Node 22, the container image, e2e:pro / e2e:api / e2e:feedback, production-scale session tables and production-size dumps. Label every action recommendation MEASURED AT RUNTIME, PROBED or READ ONLY.
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
TARGETS='VSP66 VSP71 VSP70 VSP68 VSP73'
EXPECT_IDS="MAIN-P $TARGETS"
for ID in $EXPECT_IDS; do
  N="$(printf '%s\n' "$PIN" | awk -F'\t' -v id="$ID" '$1==id' | wc -l | tr -d ' ')"
  [ "$N" = "1" ] || { echo "REFUSING: PIN table must carry exactly one row '$ID' (found $N)" >&2; exit 40; }
done
[ "$(printf '%s\n' "$PIN" | wc -l | tr -d ' ')" = "6" ] || { echo "REFUSING: PIN table carries rows beyond the six expected ($EXPECT_IDS)" >&2; exit 40; }
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
  VSP66) echo 'fix/vsp-66-checkout-link-death-2026-09-28' ;;
  VSP71) echo 'fix/vsp-71-session-index-boot-2026-09-28' ;;
  VSP70) echo 'fix/vsp-70-restore-rollback-error-2026-09-28' ;;
  VSP68) echo 'fix/vsp-68-backup-missing-table-2026-09-28' ;;
  VSP73) echo 'fix/vsp-73-backup-dump-replay-2026-09-28' ;;
esac; }
count_of() { case "$1" in VSP70) echo 2 ;; *) echo 1 ;; esac; }
for ID in $TARGETS; do
  [ "$(fld "$ID" 3)" = "$(branch_of "$ID")" ] || { echo "REFUSING: row $ID branch is '$(fld "$ID" 3)', the brief's target is $(branch_of "$ID") — re-brief" >&2; exit 40; }
  is40 "$(fld "$ID" 5)" || { echo "REFUSING: PIN row $ID base is not a 40-hex sha" >&2; exit 40; }
  [ "$(fld "$ID" 6)" = "$(count_of "$ID")" ] || { echo "REFUSING: PIN row $ID commits is '$(fld "$ID" 6)', the brief gates $(count_of "$ID")" >&2; exit 40; }
done
MAINH="$(fld MAIN-P 4)"
H66="$(fld VSP66 4)"; H71="$(fld VSP71 4)"; H70="$(fld VSP70 4)"; H68="$(fld VSP68 4)"; H73="$(fld VSP73 4)"

# 6 / 7 / 8 — commits; base ancestor AND merge-base; base is MAIN (a stale base passes with a NOTE); not on main; exact count.
for S in "$MAINH" "$ANCHOR_G10" "$ANCHOR_R70" "$H66" "$H71" "$H70" "$H68" "$H73"; do
  T="$(p cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in the portal repo (got '$T') — this launcher never fetches" >&2; exit 6; }
done
STALE=''
for ID in $TARGETS; do
  H="$(fld "$ID" 4)"; BASE="$(fld "$ID" 5)"; N="$(fld "$ID" 6)"; H7="${H:0:7}"
  if [ "$BASE" != "$MAINH" ]; then
    if p merge-base --is-ancestor "$BASE" "$MAINH" 2>/dev/null && [ "$(p merge-base "$H" "$MAINH" 2>/dev/null)" = "$BASE" ]; then
      STALE="$STALE $ID"
      echo "NOTE: row $ID is a STALE-BASE row (base ${BASE:0:7} is an ancestor of MAIN ${MAINH:0:7}); the brief expects none stale — §12 may be stale" >&2
    else
      echo "REFUSING: row $ID base ${BASE:0:7} is neither MAIN nor merge-base(head, MAIN) on MAIN — re-pin" >&2; exit 7
    fi
  fi
  p merge-base --is-ancestor "$BASE" "$H" 2>/dev/null || { echo "REFUSING: $ID base ${BASE:0:7} is not an ancestor of $H7" >&2; exit 7; }
  [ "$(p merge-base "$BASE" "$H" 2>/dev/null)" = "$BASE" ] || { echo "REFUSING: $ID merge-base(base, head) is not the base" >&2; exit 7; }
  p merge-base --is-ancestor "$H" "$MAINH" 2>/dev/null \
    && { echo "REFUSING: $ID $H7 is ALREADY ON MAIN ${MAINH:0:7} — the brief says it is not; re-brief" >&2; exit 7; }
  GOTN="$(p rev-list --count "${BASE}..${H}" 2>/dev/null)"
  [ "$GOTN" = "$N" ] || { echo "REFUSING: $ID $H7 has $GOTN commits over its base, the table says $N" >&2; p log --format='%h %s' "${BASE}..${H}" >&2; exit 8; }
  BEHIND="$(p rev-list --count "${H}..${MAINH}" 2>/dev/null)"
  [ "$BEHIND" = "0" ] || echo "NOTE: $ID $H7 is $BEHIND behind main ${MAINH:0:7} — the brief says 0 behind; §12 may be stale" >&2
done

# 9 — gated anchors: main is gate 10's GO'd head (single parent b5c3e8d); every target contains it; VSP70 = fix on refactor on 0d992e0.
[ "$MAINH" = "$ANCHOR_G10" ] || echo "NOTE: portal main is ${MAINH:0:7}, not 0d992e0 — main moved since drafting; the brief's base wording is stale" >&2
[ "$(p log -1 --format='%P' "$ANCHOR_G10" 2>/dev/null)" = "$ANCHOR_G10P" ] \
  || { echo "REFUSING: 0d992e0's parent is not b5c3e8d — this is not gate 10's GO'd head; re-brief" >&2; exit 9; }
for ID in $TARGETS; do
  H="$(fld "$ID" 4)"
  p merge-base --is-ancestor "$ANCHOR_G10" "$H" 2>/dev/null \
    || { echo "REFUSING: $ID ${H:0:7} does not contain gate 10's GO'd head 0d992e0 — re-brief" >&2; exit 9; }
  for S in $(p rev-list "${ANCHOR_G10}..${H}" 2>/dev/null); do
    [ "$(p log -1 --format='%P' "$S" 2>/dev/null | wc -w | tr -d ' ')" = "1" ] || { echo "REFUSING: $ID commit ${S:0:7} is a merge — the brief gates linear commits" >&2; exit 9; }
  done
done
[ "$(p rev-parse "${H70}~1" 2>/dev/null)" = "$ANCHOR_R70" ] \
  || { echo "REFUSING: VSP70 head~1 is not the refactor 12138cb — the brief's red-at-12138cb has no base; re-brief" >&2; exit 9; }
[ "$(p log -1 --format='%P' "$ANCHOR_R70" 2>/dev/null)" = "$ANCHOR_G10" ] \
  || { echo "REFUSING: 12138cb's parent is not 0d992e0 — re-brief" >&2; exit 9; }

# 18 — RE-PIN: every row at origin, by ls-remote, read NOW (immediately before launch).
for ID in $EXPECT_IDS; do
  BR="$(fld "$ID" 3)"; H="$(fld "$ID" 4)"
  L="$(p ls-remote origin "refs/heads/$BR" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: row $ID: $H is not at refs/heads/$BR on origin — that head moved or was never pushed; re-pin" >&2; printf '%s\n' "${L:-<nothing>}" >&2; exit 18; }
done
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — exact file sets over main, per target; the refactor touches dbRestore.js only.
fileset() { case "$1" in
  VSP66) printf '%s\n' BACKLOG.md server/db.js test/db/checkout-link-death.child.js test/db/checkout-link-death.test.js ;;
  VSP71) printf '%s\n' BACKLOG.md server/initDb.js server/schema.sql test/db/session-index-boot.child.js test/db/session-index-boot.test.js ;;
  VSP70) printf '%s\n' BACKLOG.md server/dbRestore.js server/dbRestore.test.js ;;
  VSP68) printf '%s\n' BACKLOG.md server/dbBackup.js server/dbBackup.test.js ;;
  VSP73) printf '%s\n' BACKLOG.md server/routes/admin.js test/db/backup-dump-replay.test.js ;;
esac; }
for ID in $TARGETS; do
  H="$(fld "$ID" 4)"; BASE="$(fld "$ID" 5)"
  GOT="$(p diff --name-only "$BASE" "$H" 2>/dev/null | sort)"
  [ "$GOT" = "$(fileset "$ID" | sort)" ] || { echo "REFUSING: $ID ${H:0:7}'s delta over main is not exactly the briefed file set. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }
done
[ "$(p diff --name-only "$ANCHOR_G10" "$ANCHOR_R70" 2>/dev/null)" = "server/dbRestore.js" ] \
  || { echo "REFUSING: the refactor 12138cb touches more than server/dbRestore.js — re-brief" >&2; exit 22; }

# 74 — per-target content, read from the pinned shas (never a checkout). Present at the head, absent at main.
has() { p show "${1}:${2}" 2>/dev/null | grep -qF -- "$3"; }   # sha path fixed-string
must() { has "$1" "$2" "$3" || { echo "REFUSING: ${1:0:7}:$2 lacks '$3' — the brief gates different code; re-brief" >&2; exit 74; }; }
mustnot() { has "$1" "$2" "$3" && { echo "REFUSING: ${1:0:7}:$2 already carries '$3' — the brief's history is wrong; re-brief" >&2; exit 74; }; return 0; }
ntests() { p show "${1}:${2}" 2>/dev/null | grep -c '^test('; }
# VSP66
must "$H66" server/db.js "client.on('error', onHeldError);"
must "$H66" server/db.js "client.removeListener('error', onHeldError);"
must "$H66" server/db.js "console.error('[db] a held client lost its connection (discarded on release):'"
mustnot "$MAINH" server/db.js 'onHeldError'
for T in "'terminate-held'" "'terminate-inflight'" "'reset-held'" "'end-held'" 'const server = net.createServer((app) => {'; do
  must "$H66" test/db/checkout-link-death.child.js "$T"
done
must "$H66" test/db/checkout-link-death.test.js '/\[db\] .*held/'
[ "$(ntests "$H66" test/db/checkout-link-death.test.js)" = "6" ] || { echo "REFUSING: VSP66's checkout-link-death.test.js does not carry the READY's 6 cells" >&2; exit 74; }
# VSP71
for T in "DECLARE prev text := current_setting('lock_timeout');" "PERFORM set_config('lock_timeout', '2s', true);" 'EXCEPTION WHEN OTHERS THEN' \
         "PERFORM set_config('lock_timeout', prev, true);" "IF to_regclass('\"IDX_session_expire\"') IS NULL THEN"; do
  must "$H71" server/schema.sql "$T"
done
[ "$(p show "${H71}:server/schema.sql" 2>/dev/null | tail -1)" = 'END $$;' ] || { echo "REFUSING: VSP71's session DO block is no longer the last statement of schema.sql — the brief's WRONG (e) is stale" >&2; exit 74; }
mustnot "$MAINH" server/schema.sql 'lock_timeout'
must "$H71" server/initDb.js 'IDX_session_expire is missing (VSP-71)'
must "$H71" test/db/session-index-boot.test.js "const PASSWORD = 'vsp71';"
must "$H71" test/db/session-index-boot.test.js 'const tag = `vsp71_${process.pid}`;'
[ "$(ntests "$H71" test/db/session-index-boot.test.js)" = "5" ] || { echo "REFUSING: VSP71's session-index-boot.test.js does not carry the READY's 5 cells" >&2; exit 74; }
# VSP70
must "$H70" server/dbRestore.js 'async function clearTables(data, db = pool) {'
must "$H70" server/dbRestore.js 'client.release(broken);'
must "$H70" server/dbRestore.js 'ROLLBACK failed as well'
must "$H70" server/dbRestore.js 'module.exports = { clearTables, RESTORE_ORDER };'
must "$ANCHOR_R70" server/dbRestore.js 'async function clearTables(data, db = pool) {'
mustnot "$ANCHOR_R70" server/dbRestore.js 'release(broken)'
mustnot "$MAINH" server/dbRestore.js 'module.exports'
[ "$(ntests "$H70" server/dbRestore.test.js)" = "4" ] || { echo "REFUSING: VSP70's dbRestore.test.js does not carry the READY's 4 cells" >&2; exit 74; }
# VSP68
must "$H68" server/dbBackup.js 'failed_tables: Object.keys(tables).filter(t => tables[t].error),'
must "$H68" server/dbBackup.js "incomplete: { title: 'DB Backup INCOMPLETE', priority: '4', tags: 'warning,floppy_disk' },"
must "$H68" server/dbBackup.js "failedTables: data.metadata.failed_tables.join(',')"
mustnot "$MAINH" server/dbBackup.js 'INCOMPLETE'
must "$H68" BACKLOG.md 'The nightly backup leaves out most of the PRO tables'
must "$H68" BACKLOG.md "Restoring a backup in which a table's dump failed empties that live table"
[ "$(ntests "$H68" server/dbBackup.test.js)" = "5" ] || { echo "REFUSING: VSP68's dbBackup.test.js does not carry the READY's 5 cells" >&2; exit 74; }
# VSP73
must "$H73" server/routes/admin.js 'CREATE SEQUENCE IF NOT EXISTS'
must "$H73" server/routes/admin.js 'SELECT indexdef FROM pg_indexes'
must "$H73" server/routes/admin.js 'OWNED BY ${table_name}.${quoteIdent(column_name)};'
mustnot "$MAINH" server/routes/admin.js 'pg_sequences'
must "$H73" test/db/backup-dump-replay.test.js 'const FRESH = `vsp73_${process.pid}`;'
[ "$(ntests "$H73" test/db/backup-dump-replay.test.js)" = "4" ] || { echo "REFUSING: VSP73's backup-dump-replay.test.js does not carry the READY's 4 cells" >&2; exit 74; }
# The pool.connect() holders: six at main and every head but VSP70; five at VSP70 plus clearTables' db.connect() (brief WRONG (j)).
holders() {
  bash -c 'r="$1"; h="$2"; f=$(git --no-optional-locks -C "$r" ls-tree -r --name-only "$h" -- server scripts | grep -E "\.js$" | grep -v "test\.js$"); git --no-optional-locks -C "$r" grep -n -F "pool.connect()" "$h" -- $f' _ "$P_REPO" "$1" 2>/dev/null \
    | sed "s#^${1}:##" | awk -F: '{print $1":"$2}' | grep -v '^server/db.js:' | sort
}
EXPECT_HOLDERS='server/dbRestore.js:149
server/reminders/dispatcher.js:121
server/routes/admin.js:93
server/routes/quotes.js:262
server/seed.js:18
server/seedCollateral.js:13'
for S in "$MAINH" "$H66" "$H71" "$H68" "$H73"; do
  [ "$(holders "$S")" = "$(sorted "$EXPECT_HOLDERS")" ] || { echo "REFUSING: at ${S:0:7} the pool.connect() holders are not exactly the six the brief tables. Got:" >&2; holders "$S" >&2; exit 74; }
done
[ "$(holders "$H70")" = "$(sorted "$EXPECT_HOLDERS" | grep -v '^server/dbRestore.js:')" ] || { echo "REFUSING: at VSP70 the holders are not the five the brief tables (WRONG (j))" >&2; holders "$H70" >&2; exit 74; }
must "$H70" server/dbRestore.js '  const client = await db.connect();'
# The gate-10 instruments the brief names.
grep -qF 'async s7b()' "$G10_TOOLS/qa-harness-g10-vsp.cjs" 2>/dev/null || { echo "REFUSING: gate 10's harness has no S7b arm — the brief's §N1.3 is stale" >&2; exit 74; }
grep -qF "m.cmd === 'rst'" "$G10_TOOLS/qa-g10-stallproxy.cjs" 2>/dev/null || { echo "REFUSING: gate 10's proxy has no rst verb — the brief's WRONG (c) is stale" >&2; exit 74; }
grep -qF 'armNext' "$G10_TOOLS/qa-g10-stallproxy.cjs" 2>/dev/null || { echo "REFUSING: gate 10's proxy has no armNext — the brief's §N3.3 shape has no instrument" >&2; exit 74; }

# 63 — shared files the same blob at main and every head; each target-owned file changed ONLY by its own target.
for F in package.json package-lock.json .github/workflows/test.yml server/errors.js server/index.js test/db/helpers.js scripts/run-db-tests.js \
         scripts/ensure-test-db.js test/db/pool-timeout.test.js server/reminders/dispatcher.js server/routes/quotes.js; do
  W="$(p rev-parse "${MAINH}:$F" 2>/dev/null)"
  [ -n "$W" ] || { echo "REFUSING: $F missing at main" >&2; exit 63; }
  for ID in $TARGETS; do
    GOTB="$(p rev-parse "$(fld "$ID" 4):$F" 2>/dev/null)"
    [ "$GOTB" = "$W" ] || { echo "REFUSING: $F at $ID is ${GOTB:0:7}, main's is ${W:0:7} — a change the brief does not gate" >&2; exit 63; }
  done
done
owner_of() { case "$1" in server/db.js) echo VSP66 ;; server/schema.sql|server/initDb.js) echo VSP71 ;; server/dbRestore.js) echo VSP70 ;;
  server/dbBackup.js) echo VSP68 ;; server/routes/admin.js) echo VSP73 ;; esac; }
for F in server/db.js server/schema.sql server/initDb.js server/dbRestore.js server/dbBackup.js server/routes/admin.js; do
  W="$(p rev-parse "${MAINH}:$F" 2>/dev/null)"; O="$(owner_of "$F")"
  for ID in $TARGETS; do
    GOTB="$(p rev-parse "$(fld "$ID" 4):$F" 2>/dev/null)"
    if [ "$ID" = "$O" ]; then
      [ "$GOTB" != "$W" ] || { echo "REFUSING: $F is unchanged at $O — the brief says $O changes it" >&2; exit 63; }
    else
      [ "$GOTB" = "$W" ] || { echo "REFUSING: $F changed at $ID (${GOTB:0:7}); only $O should touch it" >&2; exit 63; }
    fi
  done
done
for T in 'npm ci --offline --ignore-scripts' 'entry by entry' 'never npm audit'; do
  grep -qiF "$T" "$BRIEF" || { echo "REFUSING: brief lacks the dependency rule '$T'" >&2; exit 63; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the dependency rule '$T'" >&2; exit 63 ;; esac
done

# 31 — the READYs are on disk and their NOT TESTED lines are carried verbatim; the prior gates' findings are on disk.
nt_lines() { awk '/^NOT TESTED:?$/{f=1;next} f&&/^- /{print} f&&/^[A-Z][A-Z]+[ :,]/{exit}' "$1"; }
for PAIR in "$READY66:4" "$READY71:5" "$READY70:2" "$READY68:3" "$READY73:2"; do
  RF="${PAIR%:*}"; WANT="${PAIR##*:}"
  [ -s "$RF" ] || { echo "REFUSING: a READY mail is not on disk: $RF" >&2; exit 31; }
  [ "$(nt_lines "$RF" | wc -l | tr -d ' ')" = "$WANT" ] || { echo "REFUSING: $RF's NOT TESTED list is not the $WANT lines the brief carries" >&2; exit 31; }
  while IFS= read -r T; do
    [ -n "$T" ] || continue
    grep -qxF -- "$T" "$BRIEF" || { echo "REFUSING: the brief does not carry this NOT TESTED line verbatim: $T" >&2; exit 31; }
  done <<< "$(nt_lines "$RF")"
done
grep -qF 'READY FOR QA: VSP-66 @ 1976275' "$READY66" || { echo "REFUSING: the VSP-66 READY does not name 1976275" >&2; exit 31; }
grep -qF 'READY FOR QA: VSP-71 @ 5bdaeae' "$READY71" || { echo "REFUSING: the VSP-71 READY does not name 5bdaeae" >&2; exit 31; }
grep -qF 'READY FOR QA: VSP-70 @ 10ba4bb' "$READY70" || { echo "REFUSING: the VSP-70 READY does not name 10ba4bb" >&2; exit 31; }
grep -qF 'READY FOR QA: VSP-68 @ 7ef698d' "$READY68" || { echo "REFUSING: the VSP-68 READY does not name 7ef698d" >&2; exit 31; }
grep -qF 'READY FOR QA: VSP-73 @ 6d7ea73' "$READY73" || { echo "REFUSING: the VSP-73 READY does not name 6d7ea73" >&2; exit 31; }
for T in 'VSP-66 NOT TESTED' 'VSP-71 NOT TESTED' 'VSP-70 NOT TESTED' 'VSP-68 NOT TESTED' 'VSP-73 NOT TESTED' 'F-A' 'F-B'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: the brief does not carry '$T'" >&2; exit 31; }
done
[ -s "$CLAR" ] || { echo "REFUSING: Vision CLARIFICATIONS.md absent: $CLAR" >&2; exit 31; }
for C in 'C-01.' 'C-06.'; do grep -qF "**$C" "$CLAR" || { echo "REFUSING: $CLAR lacks $C" >&2; exit 31; }; done
grep -qF '**C-07.' "$CLAR" && echo "NOTE: Vision CLARIFICATIONS now has a C-07 — the brief says C-01..C-06; read it before launch" >&2
grep -qiE 'VSP-(66|68|70|71|73)' "$CLAR" && echo "NOTE: Vision CLARIFICATIONS now mentions a gate-11 ticket — the brief says none does; read it before launch" >&2
[ -s "$G10_REPORT" ] || { echo "REFUSING: gate 10's report is absent: $G10_REPORT" >&2; exit 31; }
grep -qF '**GO** at `0d992e09ebe0830dbe414aa73ca9a17a1be6c480`' "$G10_REPORT" || { echo "REFUSING: gate 10's report does not carry its GO at 0d992e0" >&2; exit 31; }
grep -qF 'VSP65-R2-O1 (Minor)' "$G10_REPORT" || { echo "REFUSING: gate 10's report does not name VSP65-R2-O1 (Minor) — VSP-71 has no source" >&2; exit 31; }
[ -s "$G9_REPORT" ] || { echo "REFUSING: gate 9's report is absent: $G9_REPORT" >&2; exit 31; }
grep -qF 'VSP65-O1: Major, pre-existing, identical at MAIN.' "$G9_REPORT" || { echo "REFUSING: gate 9's report does not carry VSP65-O1 — VSP-66 has no source" >&2; exit 31; }
for S in evidence/vsp/HEAD-s7b-shrunk.txt evidence/vsp/MAIN-s7b-shrunk.txt; do
  [ -s "$G9_DIR/$S" ] || { echo "REFUSING: gate 9's $S is absent — the brief names it" >&2; exit 31; }
done
[ -s "$G10_DIR/evidence/census/n3-run.txt" ] || { echo "REFUSING: gate 10's census/n3-run.txt is absent — the brief names it" >&2; exit 31; }
for D in "$G9_DIR" "$G10_DIR"; do
  grep -qF "$D" "$BRIEF" || { echo "REFUSING: the brief does not name $D" >&2; exit 31; }
  case "$PROMPT" in *"$D"*) ;; *) echo "REFUSING: the prompt does not name $D" >&2; exit 31 ;; esac
done
for H in qa-g10-stallproxy.cjs qa-harness-g10-vsp.cjs qa-g10-lib.cjs qa-harness-g10-schema.cjs qa-g10-sql.cjs qa-g10-sqlcheck.cjs qa-g10-n2c.cjs \
         qa-g10-n2d2.cjs qa-g10-n3.cjs run-arm.sh run-node20-g10.sh run-suite.sh mktree-portal.sh mutate-vsp.py mutate-r2.py qa-mkdb.cjs \
         qa-dbcheck.cjs qa-floorcount.py qa-harness-floorctl.mjs qa-io1-preload-fetchguard.cjs qa-io1-preload-hidelayer.cjs qa-run.py \
         lockcmp.py lockwalk.py specsets.py tapsets.py; do
  [ -s "$G10_TOOLS/$H" ] || { echo "REFUSING: gate 10's tool $H is not on disk — the brief tells the gate to copy it" >&2; exit 31; }
  grep -qF -- "$H" "$BRIEF" || { echo "REFUSING: the brief does not name gate 10's tool $H" >&2; exit 31; }
done

# 39 — the floor instrument is on disk and named.
[ -s "$G10_FLOOR" ] || { echo "REFUSING: gate 10's floor instrument missing: $G10_FLOOR" >&2; exit 39; }
grep -qF 'qa-floorcount.py' "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument qa-floorcount.py" >&2; exit 39; }

# 41 — the answer route exists (Tuesday adds 'QA/Vision-gate11|tuesday-agent@agentmail.to|no' at launch).
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || {
  echo "REFUSING: no '${ROUTE_NAME}|tuesday-agent@agentmail.to|…' line in $ROUTING — answers to the gate would have no route. Add it (pattern: the QA/Vision-gate10 line) before launch." >&2; exit 41; }

# 10 / 17 — report path named in both; no stale report.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

# 12 — tiers declared in both.
for T in '**VSP66** at `1976275` — **TIER 1.**' '**VSP71** at `5bdaeae` — **TIER 1.**' '**VSP70** at `10ba4bb` — **TIER 2' \
         '**VSP68** at `7ef698d` — **TIER 2' '**VSP73** at `6d7ea73` — **TIER 2'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not declare the tier: $T" >&2; exit 12; }
done
for T in 'VSP66 (TIER 1)' 'VSP71 (TIER 1)' 'VSP70 (TIER 2' 'VSP68 (TIER 2' 'VSP73 (TIER 2'; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare: $T" >&2; exit 12 ;; esac
done

# 78 — the commission's requirements, in both.
for T in 'S7b' 'terminate' 'in-flight' 'RST' 'FIN' 'reused' 'logged once' 'real caller' 'lock_timeout' 'RESTORED' '42501' 'NON-superuser' \
         'production-shaped' 'no-op' '12138cb' 'armNext' 'masking' 'INCOMPLETE' 'recorder' 'blob metadata' 'F-A' 'F-B' '42P01' 'fresh database' \
         'merged tree' 'BACKLOG.md' 'SETS, NOT COUNTS' '0d992e0' '1976275' '5bdaeae' '10ba4bb' '7ef698d' '6d7ea73' 'Node 20' 'NODE20-LEG' \
         'UNMEASURED' 'PRODUCTION IS LIVE' 'datasec-sales-db.postgres.database.azure.com' 'positive control' 'e2e:pro' 'real dump'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks '$T'" >&2; exit 78; }
  printf '%s\n' "$PROMPT" | grep -qiF -- "$T" || { echo "REFUSING: prompt lacks '$T'" >&2; exit 78; }
done
for C in 'quotes.js:262' 'admin.js:93' 'dispatcher.js:121' 'seed.js:18' 'seedCollateral.js:13' 'dbRestore.js:149'; do
  grep -qF -- "$C" "$BRIEF" || { echo "REFUSING: brief does not name the pool.connect() holder $C" >&2; exit 78; }
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
WORDS="merge-tree NOT%TESTED env%-i bash createApp() initDb() 0d992e0 1976275 5bdaeae 10ba4bb 7ef698d 6d7ea73 12138cb work-g11 vsp_qa_g11 _test
FOREGROUND MEASURED%AT%RUNTIME PROBED READ%ONLY start%/%mid%/%end CI VOID node%--check"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## Charter' '^## RULED BY KAM, AND SETTLED' '^## PRIOR ROUND' '^PRIOR ROUND: ' 'ITS REPORT IS ON DISK AT:' '^## PIN' \
         '^## WRONG OR UNVERIFIABLE' '^## THE READYs' '^## 2a. LEGITIMATE SHAPES' '^## N1. TARGET VSP66' '^## N2. TARGET VSP71' \
         '^## N3. TARGET VSP70' '^## N4. TARGET VSP68' '^## N5. SHARED' '^## N6. TARGET VSP73' '^## 12. The merge' '^## 13. FLOOR' \
         "^## TUESDAY'S RULINGS AT STAMP" '^## 14. Output' '^PROVENANCE:'; do
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
for T in 'EXCLUSIVE' 'work-g11'; do
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

# 32 — the coordinator stamps the self-check (line AND note). LAST, so --check shows every other guard first.
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "guards pass (40 6 7 8 9 18 22 74 63 31 39 41 10 17 12 78 13 14 15 20 70 19 24 53 60 61 62 64 69 75 38 45 44); self-check NOT stamped." >&2
  echo "REFUSING: the brief's SELF-CHECK line or Self-check note is unstamped — the coordinator re-reads end-to-end and stamps both before launch" >&2; exit 32
fi

PIN_BLOCK="$(printf 'PINNED HEADS — verified by the launcher at %s (cat-file, base ancestry and merge-base, not-already-on-main, commit counts; gated anchors 0d992e0 in every target, VSP70 head~1 = 12138cb; git ls-remote origin for every row):\n' "$PIN_TS"
  printf '%s\n' "$PIN" | awk -F'\t' '{ printf "  %-7s %-7s %-46s %s  base %s  commits %s\n", $1, $2, $3, $4, ($5=="-"?"-":substr($5,1,12)), $6 }'
  printf '  STALE-BASE rows (forward merge owed at merge time):%s\n' "${STALE:- none}"
  printf 'NODE20-LEG, as decided in the brief: %s\n' "$NODE20")"

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  printf '%s\n' "$PIN_BLOCK"
  echo "  PIN parsed (40); commits, bases, not-on-main, counts 1/1/2/1/1 (6 7 8); 0d992e0 in every target, its parent b5c3e8d, VSP70~1 = 12138cb, no merges (9); origin re-read $PIN_TS (18)"
  echo "  file sets 4/5/3/3/3 + refactor dbRestore-only (22); per-target content at head and absent at main, holders 6/6/6/5+db.connect/6/6, test( 6/5/4/5/4, gate-10 S7b/rst/armNext (74)"
  echo "  shared blobs equal at main and every head; each owned file changed only by its owner (63); five READYs' NOT TESTED verbatim + gate 9/10 sources + tools (31); floor (39); route $ROUTE_NAME (41); report absent (17)"
  echo "  tiers (12); commission requirements (78); directive/brief/placeholders/mail/key/questions/safety (13 14 15 20 70); words + sections (19); no server path (24); standing rules (53 60 61 62 64 69 75); seats $NEG_SEATS (38); NODE20 $NODE20 (45); :5433 listening (44); self-check stamped (32)"
  exit 0
fi

# 11 — no inherited identity: this gate needs neither az nor gh, so both point at fresh EMPTY directories.
ID_TMP="$(mktemp -d "${TMPDIR:-/tmp}/qa-vision-gate11-id.XXXXXX")" || { echo "REFUSING: cannot create the empty identity dir" >&2; exit 11; }
mkdir -p "$ID_TMP/azure-empty" "$ID_TMP/gh-empty" || { echo "REFUSING: cannot create the empty identity dirs under $ID_TMP" >&2; exit 11; }
{ [ -z "$(ls -A "$ID_TMP/azure-empty")" ] && [ -z "$(ls -A "$ID_TMP/gh-empty")" ]; } || { echo "REFUSING: the identity dirs under $ID_TMP are not empty" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_TMP/azure-empty"
export GH_CONFIG_DIR="$ID_TMP/gh-empty"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"
# 64 (cont.) — nothing a product process could use to reach a real provider or database is inherited from this shell.
unset DATABASE_URL TEST_DATABASE_URL DB_QUERY_TIMEOUT_MS DB_CONNECT_TIMEOUT_MS AGENTMAIL_API_KEY AGENTMAIL_INBOX ACS_CONNECTION_STRING \
      ACS_EMAIL_CONNECTION_STRING ACS_EMAIL_SENDER MAIL_SENDER TABLES_CONNECTION_STRING AZURE_BACKUP_CONN_STR AZURE_BACKUP_CONTAINER BACKUP_CRON \
      SESSION_SECRET HPAM_WORD ADVANCED_UNLOCK_SECRET SALES_COPY_EMAIL FEEDBACK_NOTIFY_EMAIL FEEDBACK_NOTIFY_EMAILS APPROVALS_INBOX NTFY_TOPIC \
      NTFY_SERVER LEAD_BOT_API_KEY WEBSITE_SITE_NAME COORDINATOR_SECRET PORT NODE_ENV
echo "identity: AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR GH_CONFIG_DIR=$GH_CONFIG_DIR (empty) CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR" >&2

PROMPT="$PROMPT

$PIN_BLOCK"
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$PROMPT"
