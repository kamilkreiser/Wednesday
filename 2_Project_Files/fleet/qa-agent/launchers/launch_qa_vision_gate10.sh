#!/bin/bash
# launch_qa_vision_gate10.sh — cross-project QA agent, ONE gate (Vision gate 10, drafted 2026-09-27) on
# Datasec/Vision_Sales_Portal, ONE target, ONE verdict:
#   VSP65 round 2  portal  fix/vsp-65-pool-query-timeout-2026-09-27  the VSP65-F1 fix: the session store no longer creates its
#          table (createTableIfMissing: false); server/schema.sql creates "session" at boot in connect-pg-simple's table.sql shape,
#          the index only when to_regclass says it is missing. TIER 1. ROUND 2 OF 2 of the VSP-65 class (round 1 = gate 9, NO-GO
#          on VSP65-F1 at 2adfc4a). If this round is NO-GO the class goes to Kam.
#
# THE HEADS LIVE IN ONE PLACE: the brief's PIN-HEADS table. This launcher PARSES it (carries no head of its own), refuses any
# placeholder, verifies every row against the object store and against origin by `git ls-remote` NOW, and appends the verified
# table to the agent's prompt. The only shas it carries are GATED ANCHORS: f95f625 + 15cd733 (main eaf024a's two parents;
# 15cd733 is gate 7's gated IO1F1 head) and 2adfc4a (gate 9's gated round-1 head, which must be head~2).
#
# PRODUCTION IS LIVE for this project (datasec-sales-portal-rg). The gate is local Postgres only: no az, no deploy, no app
# setting, no connection to the production database. Findings only.
#
# PATTERN: launch_qa_vision_gate9.sh (PIN parse, anchors, file sets, content guards, embedded prompt, --check, stamp LAST).
# CHANGES vs gate 9, each deliberate:
#   - one repo; exit 40: PIN rows are exactly MAIN-P + VSP65. No QuickQuote row, no AZURITE-LEG.
#   - exit 9:  anchors — main's parents are exactly f95f625 + 15cd733; 15cd733 and 2adfc4a are ancestors of the head; head~2 = 2adfc4a,
#              and the head and head~1 each have ONE parent (round 2 is two linear commits on round 1).
#   - exit 22: exact file sets — 6 files over main, 4 over 2adfc4a.
#   - exit 74: round-2 content — createTableIfMissing false at head / true at 2adfc4a; the session block in schema.sql at head and
#              absent at main; the six pool.connect() callers unchanged; pool-timeout 12 cells at head (6 at 2adfc4a); the builder's
#              drop-shaped stall and the owner cell's slice (brief WRONG (b)/(c)); gate 9's S8d trigger is still 'to_regclass'
#              (brief WRONG (a) — the reason the gate must re-target it).
#   - exit 63: server/db.js + server/db.test.js the same blob at 2adfc4a and head; package.json, lockfile, test.yml, errors.js,
#              initDb.js, test/db/helpers.js, scripts/run-db-tests.js the same blob at main and head.
#   - exit 31: gate 9's report (the NO-GO line, VSP65-F1), its S8d evidence and the tools the brief copies; the READY on disk with
#              its NOT TESTED carried verbatim (5 lines).
#   - exit 45: NODE20-LEG decided (NOT-RUN | DOCKER-PULL-NEVER), and the prompt told which.
#   - exit 44: something LISTENs on :5433 (local Postgres). The launcher never starts a container.
#   - exit 41: the answer route QA/Vision-gate10 exists in fleet/inbox_routing.conf (Tuesday adds it at launch).
#   - exit 38: negative-control seats named in the brief; advisory if one has exited.
#   - exit 32: SELF-CHECK and Self-check note stamped — LAST.
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/Vision-gate10' "bash '<this file>'"), NEVER nohup.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Contains a legitimate `cd` (into the QA project, at exec).
# READ-ONLY toward the repo: only cat-file, rev-parse, merge-base, log, rev-list, diff, show, grep, ls-tree, ls-remote.
# --check is READ-ONLY: it runs every guard and exits before any identity dir is made or any agent is started.
# Usage: launch_qa_vision_gate10.sh [--check]
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
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-27_vision-gate10-vsp65-r2.md"
READY="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-27_vision-vsp65-f1-r2-READY-mail.txt"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
VSP='/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal'
P_REPO="$VSP/2_Project_Files"
CLAR="$VSP/1_Project_Definition/CLARIFICATIONS.md"
G9_DIR="$QA_DIR/projects/vision/reports/2026-09-27-vision-gate9-vsp65-qqpurge"
G9_REPORT="$G9_DIR/report.md"
G9_TOOLS="$G9_DIR/evidence/tools"
G9_FLOOR="$G9_TOOLS/qa-floorcount.py"
REPORT="$QA_DIR/projects/vision/reports/2026-09-27-vision-gate10-vsp65-r2/report.md"
ROUTE_NAME='QA/Vision-gate10'
NEG_SEATS='23230 20317 35362'   # Tuesday (%0), NexusAI (%22), QA NexusAI batch 5a (%26) — live at drafting, 2026-09-27 10:56 AEST
# Gated anchors (not heads).
ANCHOR_MAINP1='f95f6254c1e1b296af9717603df60a9ecf33865f'   # portal main before IO1F1 (merge of gate 6's IO1R2 992da21)
ANCHOR_IO1F1='15cd73304bf54b8b3a166635f86fa4723bf415f1'    # gate 7's gated IO1F1 head, merged into main eaf024a
ANCHOR_R1='2adfc4aabee231dbd3ce6ac3239de174f4dfccd6'       # gate 9's gated VSP-65 round-1 head (NO-GO on VSP65-F1)

SUBJECT_STEM='[QA/Datasec-Vision -> Tuesday] GATE VERDICT — VSP-65 round 2'
QUESTION_SUBJ='[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>'
ANSWER_PREFIX='[Tuesday -> QA/Vision-gate10] ANSWER'

p() { git --no-optional-locks -C "$P_REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE gate (Vision gate 10) on Datasec/Vision_Sales_Portal with ONE target and ONE verdict, GO or NO-GO: VSP65 round 2, the fix for gate 9's VSP65-F1, in the SALES PORTAL repo.

READ YOUR COMMISSION FIRST, whole: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-27_vision-gate10-vsp65-r2.md
Then read the charter it names, the Vision CLARIFICATIONS (C-01..C-06; none covers VSP-65), the project's CLAUDE.md (/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/CLAUDE.md; its deploy commands are not for you), the builder's READY mail (/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-27_vision-vsp65-f1-r2-READY-mail.txt), and the PRIOR ROUND's report, gate 9, whose instruments you reuse by copy: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-27-vision-gate9-vsp65-qqpurge (report.md whole; evidence/vsp/*s8d*, evidence/node20/, evidence/tools/). Every builder statement is a CLAIM, never evidence. Verify every PRIOR WORK claim against git history and gate 9's evidence, never against the brief.

THE TARGET. VSP65 = Jira VSP-65; VSP65-F1 = gate 9's Major: a transient stall on a restarted instance's first session-store query left that instance replaying a cached rejection (500 in 1-5 ms) to every signed-in request until restart, logins storing nothing, while its health endpoint stayed 200. Branch fix/vsp-65-pool-query-timeout-2026-09-27 at 0d992e0, five commits on portal main eaf024a: round 1 (67365ec, 7195df7, 2adfc4a, gated by gate 9, NO-GO) and round 2 (b5c3e8d, 0d992e0). It is NOT on main. Round 2 passes createTableIfMissing: false to the session store in the portal's entry module and creates the "session" table in server/schema.sql at every boot, the index only when to_regclass says it is missing. server/db.js is the same blob as round 1. TIER 1: every database call and every signed-in request goes through this code, and the new boot DDL will run against production's live, store-made session table on the first boot after a deploy. Both failure directions are in scope: an instance that is still poisoned or a request that still hangs, and a healthy production-shaped database on which the boot now fails, waits, or changes the session table.

ROUND 2 OF 2. Round 1 was NO-GO. If this round is NO-GO, the VSP-65 class goes to Kam: say so in the verdict, in words.

WHAT THE BRIEF REQUIRES, in short (the brief is the authority):
  (1) VSP65-F1 RE-MEASURED WITH THE GATE'S OWN S8d INSTRUMENT, NOT THE BUILDER'S PROXY. Gate 9's S8d triggers its hold on the text to_regclass, which is the store's ENSURE query, and at 0d992e0 that query is never sent: copied unchanged, the arm holds nothing and reads green. Re-target the hold to the first session-store query on the restarted instance, whatever its text, and make every run REFUSE to report unless exactly one stall fired and the first request took at least the bound; a run where the hold never fired is VOID. The instrument must redden 2adfc4a (and the brief's M6, createTableIfMissing back to true) before its green at 0d992e0 means anything; main eaf024a must wait and serve. Shrunk bound N >= 3, the SHIPPED 30000 / 15000 ms bound once per sha, and Node 20.
  (2) THE SESSION TABLE. Compare schema.sql's table with connect-pg-simple's table.sql from the catalogs (constraints, deferrability, reloptions, indexes, owner), not information_schema. Prove the boot is a NO-OP on a PRODUCTION-SHAPED database (the store made the table at main, live rows, a kept cookie still served; no relfilenode or catalog change) and does not wait on the session table while a signed-in write is in flight. Measure the owner / 42501 guard on the WHOLE schema.sql as NON-superuser roles in every owner configuration the brief lists (the builder's cell runs only a slice of the file), two concurrent boots on a fresh database, and the index-missing path.
  (3) THE CENSUS, RE-DERIVED: every path that builds the app runs initDb first, and every path that builds or rebuilds the DATABASE without initDb (the admin backup-db SQL dump replayed into a fresh database, the restore CLI, the test-DB script). Measure what an app does on a database with NO session table at eaf024a (the store creates it) and at 0d992e0, and rule its reachability. Census any other cached database promise (F1's class) with a positive control for your grep.
  (4) RED-PROOFS re-derived: the head's cells on 2adfc4a's code (3 red: say which are behavioural), M3 -> VSP65-P2 red for a behavioural reason, M5 -> VSP65-P1 RangeError (Node 26 and Node 20 depth), M6, M7, and your own M8 / M9. Parse-checked, fresh tree per arm, node --check rc quoted; a red from a mutant that does not parse is VOID; assert every tamper landed per tree before reading its result. A behaviour with no reddening cell is a finding.
  (5) ROUND 1 HELD, RE-RUN BRIEFLY at 0d992e0: S1 black hole (no FIN back, Postgres never told) with the ticket at the shipped bound, S6, S7, S8, discard-on-release for generate and backup-db (counters and backend pids, never byte counts), the 15 s pool-wait cap, the boot refusal, one IO1F1-grace run; positive control eaf024a hangs in S1. Compare with gate 9's HEAD figures.
  (6) SUITES AS SETS, NOT COUNTS, against 2adfc4a AND eaf024a, same machine, same session: npm test and npm run test:db by test NAME, pool-timeout N >= 5 with load quoted, plus CI's coverage command run locally (label it: not CI). The Node 20 leg follows the NODE20-LEG line in the brief exactly.
  (7) CI is UNMEASURED: this project's gh is not authenticated and you must not use gh. Say so, and name CI's Node 22 coverage gate and its e2e:pro step (the first CI run of the new boot path) as the first reads at merge.

LOCAL POSTGRES ONLY. PRODUCTION IS LIVE for this project. NEVER the live portal (datasec-sales-portal.azurewebsites.net, datasec-sales-portal-rg, its Postgres datasec-sales-db.postgres.database.azure.com, its key vault): no request, no DB connection, not even a GET. No az of any kind, no deploy, no app-setting change. Never open a production dump or anything under the project's 4_Credentials. Real sends are OFF: the dispatcher and the backup notifier run only against recorders you wrote.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT from the object store (git archive into a fresh mktemp -d under projects/vision/work-g10/). Each tree is EXCLUSIVE to this gate and to one purpose; never touch work/ or work-g2 .. work-g9. Gate 9's tools are copied into YOUR evidence folder and re-pointed (they hard-code gate 9's paths and ENFORCE the vsp_qa_g9_ prefix); never run from, edit or write into gate 9's copies. Dependencies: npm ci --offline --ignore-scripts only, then prove node_modules/.package-lock.json against the lockfile entry by entry (lockcmp.py AND lockwalk.py). Never npm install, never npm audit, never npx anything not already in the tree. In the repo use ONLY read verbs (show, log, diff, ls-remote, rev-parse, ls-tree, cat-file, grep, merge-base, archive); never fetch, pull, checkout, switch, worktree, commit, stash, reset, clean or gc. Run git merge-tree --write-tree only from the gate's OWN object dir (GIT_OBJECT_DIRECTORY = your own mktemp -d, alternates = the repo's objects), or skip it and say so. Findings-only: no writes in the portal repo, none inside Vision_Sales_Portal, none in gate 1-9's report folders or trees. Never rm: quarantine. Run every loop and every git show <sha>:<path> under bash. CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY: a control derived from the run it validates is not a control.

FLOOR DISCIPLINE. Vision has no jest lock; never borrow NexusAI's. Never use ports 4848, 8080 or 47787, nor 127.0.0.1:49162 / 49164 / 49166; take every port from the kernel and bind 127.0.0.1. Never start the portal's own entry point (it binds all interfaces); use the real createApp() and initDb() in your harness. Postgres is the local container on 127.0.0.1:5433, and ONLY databases you create: vsp_qa_g10_<epoch> and vsp_qa_g10_<epoch>_test (the test name MUST end in _test); never salesportal, salesportal_test, any vsp_qa_g1..g9 database or the builder's vsp_bf1_*. Roles are cluster-global: create one only inside a transaction you roll back, or name it vsp_qa_g10_* and list it; every owner cell runs as NON-superuser roles (the compose user is a superuser and bypasses ownership). Event triggers only in your own databases; never ALTER SYSTEM or change server settings. The module's default URL is the builder's dev database, so give every product process YOUR DATABASE_URL and TEST_DATABASE_URL explicitly and print the database each one reached. Release every lock and direct session you open in a finally. No docker command at all, except the Node 20 exception (brief §N.7) under the NODE20-LEG line. Every product process runs under env -i with an explicit allowlist, NODE_ENV never production. Never set AGENTMAIL_API_KEY or AGENTMAIL_INBOX in a product process, nor any real ACS_* or MAIL_SENDER, AZURE_BACKUP_CONN_STR, TABLES_CONNECTION_STRING, SALES_COPY_EMAIL, a real NTFY_TOPIC, LEAD_BOT_API_KEY or WEBSITE_SITE_NAME; print each product process's env KEY NAMES and assert none is forbidden. NTFY_SERVER=http://ntfy.invalid; never contact ntfy.sh; stub fetch to throw on any other URL. Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid, with the brief's negative-control seats classifying FOREIGN in the same run. A zero is reportable only beside an ATTACHED control that fired in the same window. Other gates are live on this box: record the load average beside every timing number; a latency result with no load figure is not a measurement.
DEADLINE AND HEARTBEAT: every step has a written DEADLINE built into your runner (there is no timeout binary here) and releases its servers, proxies, sessions, locks, roles and children in a finally. Log a HEARTBEAT line at least every 2 minutes; a step with no heartbeat for 5 minutes is aborted and reported, never waited on. Deadlines: requests at the shrunk bound 20 s; requests at the SHIPPED bounds 120 s; the S8d arm at the shipped bound 300 s; the pool-wait burst 180 s; the boot-lock arms 120 s each; one test:db file 180 s; a whole test:db run 420 s. Nothing above 420 s. A hang at eaf024a is the expected positive control, reported as such.

QUESTIONS: your routing name is QA/Vision-gate10. If you must ask, mail tuesday-agent@agentmail.to with the subject "[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>" and proceed on the safest reading without waiting. Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/Vision-gate10] ANSWER"; read it with your verdict key. Never wednesday-agent@. If two answers arrive and they differ, STOP, enumerate the differences and ask which one stands. If a response is cut off by a safety check, record it and continue with the next item; this is authorised defensive QA of Datasec's own product on loopback. Record every question, reading and answer in the report.

Write your report to: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-27-vision-gate10-vsp65-r2/report.md

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with a subject beginning exactly:
[QA/Datasec-Vision -> Tuesday] GATE VERDICT — VSP-65 round 2: VSP65 @ 0d992e0 <GO | NO-GO>
Lead the body with two sentences: (1) does a restarted instance whose first session-store query stalls past the bound serve every later signed-in request once the stall lifts, on YOUR re-targeted S8d instrument, shrunk, shipped and on Node 20, with the same instrument reddening 2adfc4a? (2) is the new boot DDL a no-op on a production-shaped database, and does any legitimate path now leave the app without a working session table? Then one line: round 2 of 2 — if NO-GO, the VSP-65 class goes to Kam. You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no credentials directory of its own. Use it only in your own mail calls, with a client timeout. Never put the key or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice.

Report the pinned head and main as three timestamped readings (start / mid / end), with the branch name beside each. Include the verbatim operator strings: the DbTimeoutError line for the F1 request at the shipped bound (DB_QUERY_TIMEOUT), the DB_CONNECT_TIMEOUT line from the pool-wait arm, the 42501 message for a plain CREATE INDEX IF NOT EXISTS as a non-owner with SELECT version(), and the error an app gives with no session table. Then one paragraph on the queue: the merge-tree result of 0d992e0 against eaf024a (expected CLEAN, equal to the head's own tree 30798eef), the cells to re-run on the merged head, and CI at merge.

Rule 2 stands: what you did NOT test is first-class output. Write a NOT TESTED section that covers at least CI (UNMEASURED), production's session-table owner, Postgres version, search_path and index, a real App Service restart and multiple real instances, a real stalled Azure Postgres / TLS / failover, Node 22, the container image, e2e:pro / e2e:api / e2e:feedback, and production-scale session tables. Label every action recommendation MEASURED AT RUNTIME, PROBED or READ ONLY.
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
EXPECT_IDS='MAIN-P VSP65'
for ID in $EXPECT_IDS; do
  N="$(printf '%s\n' "$PIN" | awk -F'\t' -v id="$ID" '$1==id' | wc -l | tr -d ' ')"
  [ "$N" = "1" ] || { echo "REFUSING: PIN table must carry exactly one row '$ID' (found $N)" >&2; exit 40; }
done
[ "$(printf '%s\n' "$PIN" | wc -l | tr -d ' ')" = "2" ] || { echo "REFUSING: PIN table carries rows beyond the two expected ($EXPECT_IDS)" >&2; exit 40; }
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
[ "$(fld VSP65 3)" = "fix/vsp-65-pool-query-timeout-2026-09-27" ] || { echo "REFUSING: row VSP65 branch is '$(fld VSP65 3)', the brief's target is fix/vsp-65-pool-query-timeout-2026-09-27 — re-brief" >&2; exit 40; }
is40 "$(fld VSP65 5)" || { echo "REFUSING: PIN row VSP65 base is not a 40-hex sha" >&2; exit 40; }
printf '%s' "$(fld VSP65 6)" | grep -Eq '^[1-9][0-9]*$' || { echo "REFUSING: PIN row VSP65 commits is not a positive integer" >&2; exit 40; }
HEAD_SHA="$(fld VSP65 4)"; BASE="$(fld VSP65 5)"; NCOMMITS="$(fld VSP65 6)"; MAINH="$(fld MAIN-P 4)"; HEAD7="${HEAD_SHA:0:7}"

# 6 / 7 / 8 — commits; base ancestor AND merge-base; base is MAIN (a stale base passes with a NOTE); not on main; exact count.
for S in "$MAINH" "$HEAD_SHA" "$BASE" "$ANCHOR_R1"; do
  T="$(p cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in the portal repo (got '$T') — this launcher never fetches" >&2; exit 6; }
done
STALE=''
if [ "$BASE" != "$MAINH" ]; then
  if p merge-base --is-ancestor "$BASE" "$MAINH" 2>/dev/null && [ "$(p merge-base "$HEAD_SHA" "$MAINH" 2>/dev/null)" = "$BASE" ]; then
    STALE=' VSP65'
    echo "NOTE: row VSP65 is a STALE-BASE row (base ${BASE:0:7} is an ancestor of MAIN ${MAINH:0:7}); the brief expects it NOT stale — §12 may be stale" >&2
  else
    echo "REFUSING: row VSP65 base ${BASE:0:7} is neither MAIN nor merge-base(head, MAIN) on MAIN — re-pin" >&2; exit 7
  fi
fi
p merge-base --is-ancestor "$BASE" "$HEAD_SHA" 2>/dev/null || { echo "REFUSING: base ${BASE:0:7} is not an ancestor of $HEAD7" >&2; exit 7; }
[ "$(p merge-base "$BASE" "$HEAD_SHA" 2>/dev/null)" = "$BASE" ] || { echo "REFUSING: merge-base(base, head) is not the base" >&2; exit 7; }
p merge-base --is-ancestor "$HEAD_SHA" "$MAINH" 2>/dev/null \
  && { echo "REFUSING: $HEAD7 is ALREADY ON MAIN ${MAINH:0:7} — the brief says it is not; re-brief" >&2; exit 7; }
GOTN="$(p rev-list --count "${BASE}..${HEAD_SHA}" 2>/dev/null)"
[ "$GOTN" = "$NCOMMITS" ] || { echo "REFUSING: $HEAD7 has $GOTN commits over its base, the table says $NCOMMITS" >&2; p log --format='%h %s' "${BASE}..${HEAD_SHA}" >&2; exit 8; }
BEHIND="$(p rev-list --count "${HEAD_SHA}..${MAINH}" 2>/dev/null)"
[ "$BEHIND" = "0" ] || echo "NOTE: $HEAD7 is $BEHIND behind main ${MAINH:0:7} — the brief says 0 behind; §12 may be stale" >&2

# 9 — gated anchors: main is the merge of f95f625 + 15cd733; round 1's gated head 2adfc4a is head~2, round 2 is two linear commits.
[ "$(p log -1 --format='%P' "$MAINH" 2>/dev/null)" = "$ANCHOR_MAINP1 $ANCHOR_IO1F1" ] \
  || echo "NOTE: portal main ${MAINH:0:7}'s parents are '$(p log -1 --format='%P' "$MAINH" 2>/dev/null)', not f95f625 + 15cd733 — main moved since drafting; the brief's PRIOR ROUND wording may be stale" >&2
p merge-base --is-ancestor "$ANCHOR_IO1F1" "$HEAD_SHA" 2>/dev/null \
  || { echo "REFUSING: $HEAD7 does not contain gate 7's gated IO1F1 head 15cd733 — re-brief" >&2; exit 9; }
p merge-base --is-ancestor "$ANCHOR_R1" "$HEAD_SHA" 2>/dev/null \
  || { echo "REFUSING: $HEAD7 does not contain gate 9's gated round-1 head 2adfc4a — this is not round 2 of the same branch; re-brief" >&2; exit 9; }
[ "$(p rev-parse "${HEAD_SHA}~2" 2>/dev/null)" = "$ANCHOR_R1" ] \
  || { echo "REFUSING: ${HEAD7}~2 is not 2adfc4a — round 2 is not exactly two commits on round 1; re-brief" >&2; p log --format='%h %P %s' "${ANCHOR_R1}..${HEAD_SHA}" >&2; exit 9; }
for S in "$HEAD_SHA" "${HEAD_SHA}~1"; do
  [ "$(p log -1 --format='%P' "$S" 2>/dev/null | wc -w | tr -d ' ')" = "1" ] || { echo "REFUSING: $S is a merge — the brief gates two linear round-2 commits" >&2; exit 9; }
done

# 18 — RE-PIN: both rows at origin, by ls-remote, read NOW (immediately before launch).
for ID in MAIN-P VSP65; do
  BR="$(fld "$ID" 3)"; H="$(fld "$ID" 4)"
  L="$(p ls-remote origin "refs/heads/$BR" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: row $ID: $H is not at refs/heads/$BR on origin — that head moved or was never pushed; re-pin" >&2; printf '%s\n' "${L:-<nothing>}" >&2; exit 18; }
done
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — exact file sets: 6 over main, 4 over round 1.
FS_MAIN='BACKLOG.md
server/db.js
server/db.test.js
server/index.js
server/schema.sql
test/db/pool-timeout.test.js'
GOT="$(p diff --name-only "$BASE" "$HEAD_SHA" 2>/dev/null | sort)"
[ "$GOT" = "$(sorted "$FS_MAIN")" ] || { echo "REFUSING: $HEAD7's delta over main is not exactly the briefed 6 files. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }
FS_R2='BACKLOG.md
server/index.js
server/schema.sql
test/db/pool-timeout.test.js'
GOT="$(p diff --name-only "$ANCHOR_R1" "$HEAD_SHA" 2>/dev/null | sort)"
[ "$GOT" = "$(sorted "$FS_R2")" ] || { echo "REFUSING: $HEAD7's delta over round 1 (2adfc4a) is not exactly the briefed 4 files. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }

# 74 — round-2 content, read from the pinned shas (never a checkout).
has() { p show "${1}:${2}" 2>/dev/null | grep -qF -- "$3"; }   # sha path fixed-string
has "$HEAD_SHA" server/index.js 'store: new PgSession({ pool, createTableIfMissing: false }),' \
  || { echo "REFUSING: at $HEAD7 the session store is not PgSession({ pool, createTableIfMissing: false }) — the brief gates a different fix; re-brief" >&2; exit 74; }
has "$ANCHOR_R1" server/index.js 'store: new PgSession({ pool, createTableIfMissing: true }),' \
  || { echo "REFUSING: at 2adfc4a the store is not createTableIfMissing: true — the F1 positive control is gone; re-brief" >&2; exit 74; }
for T in 'CREATE TABLE IF NOT EXISTS "session" (' '"sid" varchar NOT NULL COLLATE "default",' '"sess" json NOT NULL,' \
         '"expire" timestamp(6) NOT NULL,' 'CONSTRAINT "session_pkey" PRIMARY KEY ("sid")' \
         "IF to_regclass('\"IDX_session_expire\"') IS NULL THEN" 'CREATE INDEX "IDX_session_expire" ON "session" ("expire");'; do
  has "$HEAD_SHA" server/schema.sql "$T" || { echo "REFUSING: $HEAD7's server/schema.sql lacks '$T' — re-brief" >&2; exit 74; }
done
has "$MAINH" server/schema.sql '"session"' && { echo "REFUSING: main ${MAINH:0:7}'s schema.sql already creates \"session\" — the brief's history is wrong; re-brief" >&2; exit 74; }
has "$ANCHOR_R1" server/schema.sql '"session"' && { echo "REFUSING: 2adfc4a's schema.sql already creates \"session\" — re-brief" >&2; exit 74; }
# The six pool.connect() callers the brief tables, and no seventh, over the named non-test server/scripts files (bash: zsh would not word-split).
CALLERS="$(bash -c 'r="$1"; h="$2"; f=$(git --no-optional-locks -C "$r" ls-tree -r --name-only "$h" -- server scripts | grep -E "\.js$" | grep -v "test\.js$"); git --no-optional-locks -C "$r" grep -n -F "pool.connect()" "$h" -- $f' _ "$P_REPO" "$HEAD_SHA" 2>/dev/null \
  | sed "s#^${HEAD_SHA}:##" | awk -F: '{print $1":"$2}' | grep -v '^server/db.js:' | sort)"
EXPECT_CALLERS='server/dbRestore.js:149
server/reminders/dispatcher.js:121
server/routes/admin.js:93
server/routes/quotes.js:262
server/seed.js:18
server/seedCollateral.js:13'
[ "$CALLERS" = "$(sorted "$EXPECT_CALLERS")" ] || { echo "REFUSING: at $HEAD7 the pool.connect() callers are not exactly the six the brief tables. Got:" >&2; printf '%s\n' "$CALLERS" >&2; exit 74; }
[ "$(p show "${HEAD_SHA}:test/db/pool-timeout.test.js" 2>/dev/null | grep -c '^test(')" = "12" ] \
  || { echo "REFUSING: $HEAD7's pool-timeout.test.js does not carry the READY's 12 cells" >&2; exit 74; }
[ "$(p show "${ANCHOR_R1}:test/db/pool-timeout.test.js" 2>/dev/null | grep -c '^test(')" = "6" ] \
  || { echo "REFUSING: 2adfc4a's pool-timeout.test.js does not carry round 1's 6 cells" >&2; exit 74; }
for T in 'const proxy = net.createServer((app) => {' "stallOnce = Buffer.from('session');" 'const sessionPart = schemaSql.slice(at);' \
         "test('VSP65-P1: one client checked out and released 20,000 times" "test('VSP65-P2 (behaviour, not names)"; do
  has "$HEAD_SHA" test/db/pool-timeout.test.js "$T" || { echo "REFUSING: $HEAD7's pool-timeout.test.js lacks '$T' — the brief's WRONG (b)/(c) or its P1/P2 items are stale" >&2; exit 74; }
done
has "$HEAD_SHA" BACKLOG.md 'Round 2 (gate 9 VSP65-F1, Major)' || { echo "REFUSING: $HEAD7's BACKLOG does not carry the round-2 entry" >&2; exit 74; }
grep -qF "match: 'to_regclass'" "$G9_TOOLS/qa-harness-g9-vsp.cjs" 2>/dev/null \
  || { echo "REFUSING: gate 9's S8d harness no longer triggers on 'to_regclass' — the brief's WRONG (a) is stale; re-brief" >&2; exit 74; }

# 63 — no dependency, CI, error-handler, initDb or test-helper change; round 1's pool code untouched in round 2.
for F in package.json package-lock.json .github/workflows/test.yml server/errors.js server/initDb.js test/db/helpers.js scripts/run-db-tests.js; do
  W="$(p rev-parse "${MAINH}:$F" 2>/dev/null)"; GOTB="$(p rev-parse "${HEAD_SHA}:$F" 2>/dev/null)"
  [ -n "$W" ] && [ "$GOTB" = "$W" ] || { echo "REFUSING: $F at $HEAD7 is ${GOTB:0:7}, main's is ${W:0:7} — a change the brief does not gate" >&2; exit 63; }
done
for F in server/db.js server/db.test.js; do
  W="$(p rev-parse "${ANCHOR_R1}:$F" 2>/dev/null)"; GOTB="$(p rev-parse "${HEAD_SHA}:$F" 2>/dev/null)"
  [ -n "$W" ] && [ "$GOTB" = "$W" ] || { echo "REFUSING: $F at $HEAD7 is ${GOTB:0:7}, round 1's is ${W:0:7} — the brief says round 2 leaves it untouched" >&2; exit 63; }
done
for T in 'npm ci --offline --ignore-scripts' 'entry by entry' 'never npm audit'; do
  grep -qiF "$T" "$BRIEF" || { echo "REFUSING: brief lacks the dependency rule '$T'" >&2; exit 63; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the dependency rule '$T'" >&2; exit 63 ;; esac
done

# 31 — the prior round and the READY are on disk and named; the READY's NOT TESTED is carried verbatim.
[ -s "$READY" ] || { echo "REFUSING: the READY mail is not on disk: $READY" >&2; exit 31; }
while IFS= read -r T; do
  [ -n "$T" ] || continue
  grep -qxF -- "$T" "$READY" || { echo "REFUSING: the READY no longer carries: $T" >&2; exit 31; }
  grep -qxF -- "$T" "$BRIEF" || { echo "REFUSING: the brief does not carry the READY's NOT TESTED line verbatim: $T" >&2; exit 31; }
done <<< "$(awk '/^NOT TESTED$/{f=1;next} f&&/^- /{print} f&&/^BACKLOG/{exit}' "$READY")"
[ "$(awk '/^NOT TESTED$/{f=1;next} f&&/^- /{n++} f&&/^BACKLOG/{exit} END{print n+0}' "$READY")" = "5" ] || { echo "REFUSING: the READY's NOT TESTED list is not the 5 lines the brief carries" >&2; exit 31; }
for T in 'head 0d992e09ebe0830dbe414aa73ca9a17a1be6c480' 'This is round 2 of 2: a third NO-GO goes to Kam.' \
         '- server/index.js: new PgSession({ pool, createTableIfMissing: false }).' 'RED-PROOFS (fresh scratch tree per arm'; do
  grep -qF -- "$T" "$READY" || { echo "REFUSING: the READY no longer carries '$T'" >&2; exit 31; }
done
for T in 'THE FIX' 'PRIOR WORK CHECK' 'CELLS (test/db/pool-timeout.test.js' 'RED-PROOFS (fresh scratch tree per arm'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: the brief does not carry the READY's '$T' section" >&2; exit 31; }
done
[ -s "$CLAR" ] || { echo "REFUSING: Vision CLARIFICATIONS.md absent: $CLAR" >&2; exit 31; }
for C in 'C-01.' 'C-06.'; do grep -qF "**$C" "$CLAR" || { echo "REFUSING: $CLAR lacks $C" >&2; exit 31; }; done
grep -qF '**C-07.' "$CLAR" && echo "NOTE: Vision CLARIFICATIONS now has a C-07 — the brief says C-01..C-06; read it before launch" >&2
grep -qiF 'VSP-65' "$CLAR" && echo "NOTE: Vision CLARIFICATIONS now mentions VSP-65 — the brief says no C-entry covers it; read it before launch" >&2
[ -s "$G9_REPORT" ] || { echo "REFUSING: gate 9's report is absent: $G9_REPORT" >&2; exit 31; }
grep -qF 'VSP65 (the pool query/connect timeout): **NO-GO** at `2adfc4aabee231dbd3ce6ac3239de174f4dfccd6`' "$G9_REPORT" \
  || { echo "REFUSING: gate 9's report does not carry its NO-GO at 2adfc4a — the brief's PRIOR ROUND has no source" >&2; exit 31; }
grep -qF 'VSP65-F1 (Major)' "$G9_REPORT" || { echo "REFUSING: gate 9's report does not name VSP65-F1 (Major)" >&2; exit 31; }
for S in evidence/vsp/HEAD-s8d-shrunk.txt evidence/vsp/HEAD-s8d-shipped.txt evidence/vsp/MAIN-s8d-shipped.txt evidence/vsp/HEAD-s8boot-shrunk.txt \
         evidence/node20/node20-s8d.txt evidence/mergetree.txt; do
  [ -s "$G9_DIR/$S" ] || { echo "REFUSING: gate 9's $S is absent — the brief names it" >&2; exit 31; }
done
grep -qF "$G9_DIR" "$BRIEF" || { echo "REFUSING: the brief does not name gate 9's report path" >&2; exit 31; }
case "$PROMPT" in *"$G9_DIR"*) ;; *) echo "REFUSING: the prompt does not name gate 9's report path" >&2; exit 31 ;; esac
for H in qa-g9-stallproxy.cjs qa-harness-g9-vsp.cjs qa-g9-lib.cjs run-arm.sh run-node20.sh run-suite.sh mktree-portal.sh mutate-vsp.py \
         qa-harness-g9-m5probe.cjs qa-mkdb.cjs qa-dbcheck.cjs qa-floorcount.py qa-harness-floorctl.mjs qa-io1-preload-fetchguard.cjs \
         qa-io1-preload-hidelayer.cjs qa-run.py lockcmp.py lockwalk.py tapsets.py; do
  [ -s "$G9_TOOLS/$H" ] || { echo "REFUSING: gate 9's tool $H is not on disk — the brief tells the gate to copy it" >&2; exit 31; }
  grep -qF -- "$H" "$BRIEF" || { echo "REFUSING: the brief does not name gate 9's tool $H" >&2; exit 31; }
done

# 39 — the floor instrument is on disk and named.
[ -s "$G9_FLOOR" ] || { echo "REFUSING: gate 9's floor instrument missing: $G9_FLOOR" >&2; exit 39; }
grep -qF 'qa-floorcount.py' "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument qa-floorcount.py" >&2; exit 39; }

# 41 — the answer route exists (Tuesday adds 'QA/Vision-gate10|tuesday-agent@agentmail.to|no' at launch).
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || {
  echo "REFUSING: no '${ROUTE_NAME}|tuesday-agent@agentmail.to|…' line in $ROUTING — answers to the gate would have no route. Add it (pattern: the QA/Vision-gate9 line) before launch." >&2; exit 41; }

# 10 / 17 — report path named in both; no stale report.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

# 12 — tier and round cap declared in both.
grep -qF 'VSP65 round 2 is TIER 1' "$BRIEF" || { echo "REFUSING: brief does not declare the tier" >&2; exit 12; }
for T in 'TIER 1' 'Both failure directions are in scope' 'ROUND 2 OF 2' 'goes to Kam'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not declare: $T" >&2; exit 12; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare: $T" >&2; exit 12 ;; esac
done

# 78 — the commission's requirements, in both.
for T in 'S8d' 'to_regclass' 'VOID' 'Re-target' 'SHIPPED' 'production-shaped' 'table.sql' '42501' 'NON-superuser' 'WHOLE schema.sql' \
         'concurrent boots' 'census' 'NO session table' 'backup-db' 'VSP65-P1' 'VSP65-P2' 'M3' 'M5' 'M6' 'SETS, NOT COUNTS' '2adfc4a' '0d992e0' 'eaf024a' \
         'Node 20' 'NODE20-LEG' 'UNMEASURED' 'PRODUCTION IS LIVE' 'datasec-sales-db.postgres.database.azure.com' 'S1' 'positive control' 'e2e:pro'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks '$T'" >&2; exit 78; }
  printf '%s\n' "$PROMPT" | grep -qiF -- "$T" || { echo "REFUSING: prompt lacks '$T'" >&2; exit 78; }
done
for C in 'quotes.js:262' 'admin.js:93' 'dispatcher.js:121' 'seed.js:18' 'seedCollateral.js:13' 'dbRestore.js:149'; do
  grep -qF -- "$C" "$BRIEF" || { echo "REFUSING: brief does not name the pool.connect() caller $C" >&2; exit 78; }
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
WORDS="merge-tree NOT%TESTED env%-i bash createApp() initDb() 0d992e0 2adfc4a eaf024a work-g10 vsp_qa_g10 _test
FOREGROUND MEASURED%AT%RUNTIME PROBED READ%ONLY start%/%mid%/%end CI node%--check VOID DbTimeoutError DB_QUERY_TIMEOUT DB_CONNECT_TIMEOUT"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## Charter' '^## RULED BY KAM, AND SETTLED' '^## PRIOR ROUND' '^PRIOR ROUND: round 1' 'ITS REPORT IS ON DISK AT:' '^## PIN' \
         '^## WRONG OR UNVERIFIABLE' '^## THE READY' '^## 2a. LEGITIMATE SHAPES' '^## N. TARGET VSP65' '^## 12. The merge' '^## 13. FLOOR' \
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
for T in 'EXCLUSIVE' 'work-g10'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the tree-exclusivity rule '$T'" >&2; exit 61; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the tree-exclusivity rule '$T'" >&2; exit 61 ;; esac
done
for T in '4848' '8080' '47787' 'env -i' 'AGENTMAIL_API_KEY' 'AGENTMAIL_INBOX' 'no jest lock' 'salesportal_test' '5433'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the Vision floor rule '$T'" >&2; exit 62; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the Vision floor rule '$T'" >&2; exit 62 ;; esac
done
for T in 'NEVER the live' 'datasec-sales-portal.azurewebsites.net' 'datasec-sales-portal-rg' 'no app-setting change'; do
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
  "$PH_NODE20") echo "REFUSING: the brief's NODE20-LEG line is still ${PH_NODE20} — Tuesday decides NOT-RUN or DOCKER-PULL-NEVER before launch (brief top, and §N.7)" >&2; exit 45 ;;
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

PIN_BLOCK="$(printf 'PINNED HEADS — verified by the launcher at %s (cat-file, base ancestry and merge-base, not-already-on-main, commit count; gated anchors 15cd733 and 2adfc4a = head~2; git ls-remote origin for both rows):\n' "$PIN_TS"
  printf '%s\n' "$PIN" | awk -F'\t' '{ printf "  %-7s %-7s %-42s %s  base %s  commits %s\n", $1, $2, $3, $4, ($5=="-"?"-":substr($5,1,12)), $6 }'
  printf '  STALE-BASE rows (forward merge owed at merge time):%s\n' "${STALE:- none}"
  printf 'NODE20-LEG, as decided in the brief: %s\n' "$NODE20")"

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  printf '%s\n' "$PIN_BLOCK"
  echo "  PIN parsed from the brief (40); commits, base, not-on-main, count $NCOMMITS, 0 behind (6 7 8); 15cd733 contained, head~2 = 2adfc4a, no merges (9); origin re-read $PIN_TS (18)"
  echo "  file sets: 6 over main, 4 over 2adfc4a (22); createTableIfMissing false/true, schema.sql session block at head and absent at main/2adfc4a, six callers, 12/6 pool-timeout cells, builder drop-stall + owner slice + P1/P2, BACKLOG round 2, gate 9 S8d trigger still to_regclass (74)"
  echo "  same blobs: db.js + db.test.js r1=head; package.json, lockfile, test.yml, errors.js, initDb.js, helpers.js, run-db-tests.js main=head (63); READY NOT TESTED verbatim (5) + sections + C-01..C-06 + gate 9 NO-GO/F1/S8d evidence/tools (31); floor instrument (39); route $ROUTE_NAME (41); report absent (17)"
  echo "  tier + round cap (12); commission requirements (78); directive/brief/placeholders/mail/key/questions/safety (13 14 15 20 70); words + sections (19); no server path (24); standing rules (53 60 61 62 64 69 75); seats $NEG_SEATS (38); NODE20 $NODE20 (45); :5433 listening (44); self-check stamped (32)"
  exit 0
fi

# 11 — no inherited identity: this gate needs neither az nor gh, so both point at fresh EMPTY directories.
ID_TMP="$(mktemp -d "${TMPDIR:-/tmp}/qa-vision-gate10-id.XXXXXX")" || { echo "REFUSING: cannot create the empty identity dir" >&2; exit 11; }
mkdir -p "$ID_TMP/azure-empty" "$ID_TMP/gh-empty" || { echo "REFUSING: cannot create the empty identity dirs under $ID_TMP" >&2; exit 11; }
{ [ -z "$(ls -A "$ID_TMP/azure-empty")" ] && [ -z "$(ls -A "$ID_TMP/gh-empty")" ]; } || { echo "REFUSING: the identity dirs under $ID_TMP are not empty" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_TMP/azure-empty"
export GH_CONFIG_DIR="$ID_TMP/gh-empty"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"
# 64 (cont.) — nothing a product process could use to reach a real provider or database is inherited from this shell.
unset DATABASE_URL TEST_DATABASE_URL DB_QUERY_TIMEOUT_MS DB_CONNECT_TIMEOUT_MS AGENTMAIL_API_KEY AGENTMAIL_INBOX ACS_CONNECTION_STRING \
      ACS_EMAIL_CONNECTION_STRING ACS_EMAIL_SENDER MAIL_SENDER TABLES_CONNECTION_STRING AZURE_BACKUP_CONN_STR SESSION_SECRET HPAM_WORD \
      ADVANCED_UNLOCK_SECRET SALES_COPY_EMAIL FEEDBACK_NOTIFY_EMAIL FEEDBACK_NOTIFY_EMAILS APPROVALS_INBOX NTFY_TOPIC NTFY_SERVER \
      LEAD_BOT_API_KEY WEBSITE_SITE_NAME COORDINATOR_SECRET PORT NODE_ENV
echo "identity: AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR GH_CONFIG_DIR=$GH_CONFIG_DIR (empty) CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR" >&2

PROMPT="$PROMPT

$PIN_BLOCK"
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$PROMPT"
