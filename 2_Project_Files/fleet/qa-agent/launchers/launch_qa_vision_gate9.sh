#!/bin/bash
# launch_qa_vision_gate9.sh — cross-project QA agent, ONE gate (Vision gate 9, drafted 2026-09-27) on
# Datasec/Vision_Sales_Portal, TWO targets in TWO repos, TWO separate verdicts:
#   VSP65  portal  fix/vsp-65-pool-query-timeout-2026-09-27  the Postgres pool query_timeout 30 s + connectionTimeoutMillis 15 s,
#          BoundedPool / DbTimeoutError / discard-on-release in server/db.js. TIER 1. Round 1 of the VSP-65 class.
#          Answers gate 7's IO1F1 arm (e) unfaulted half (STILL-OPEN at 45,001 ms), the NAMED residual.
#   QQPURGE quickquote  fix/qq-retention-purge-no-literal-2026-09-27  the retention purge sends no numeric literal (filter = partition
#          only, cutoffs in JS, per-row deletes). TIER 1: it deletes customer data. Added by Tuesday's scope addition, 2026-09-27.
# Supersedes the VSP-65-only pair (briefs/2026-09-27_vision-gate9-vsp65.md + launch_qa_vision_gate9_vsp65.sh), kept in place, unlaunched.
#
# THE HEADS LIVE IN ONE PLACE: the brief's PIN-HEADS table. This launcher PARSES it (carries no head of its own), refuses any
# placeholder, verifies every row against the object store and against origin by `git ls-remote` NOW, and appends the verified
# table to the agent's prompt. The only shas it carries are GATED ANCHORS: f95f625 + 15cd733 (main eaf024a's two parents;
# 15cd733 is gate 7's gated IO1F1 head).
#
# PRODUCTION IS LIVE for this project (datasec-sales-portal-rg; hpas-quickquote). The gate is local Postgres, Azurite and fakes only:
# no az, no deploy, no publish, no app setting, no connection to the production database, no Azure Table access. Findings only.
#
# PATTERN: launch_qa_vision_qq_gate8.sh (PIN parse, anchors, file sets, content guards, embedded prompt, --check, stamp LAST).
# CHANGES vs gate 8, each deliberate:
#   - two repos; exit 40: PIN rows are exactly MAIN-P + VSP65 (portal) and MAIN-Q + QQPURGE (quickquote).
#   - QQ: exits 6/7/8/18 per row, 22 (8 files), 74 (purge content), 63 (stage3 lockfile), 31 (the QQ READY verbatim).
#   - exit 9:  anchors — main's parents are exactly f95f625 + 15cd733.
#   - exit 22: exact file set — 4 files over main.
#   - exit 74: VSP-65 content — the shipped defaults 30000/15000, BoundedPool, the release override, the exports; no statement_timeout
#              in the pool options; the SIX pool.connect() callers are exactly the six the brief tables; pool-timeout has 6 cells.
#   - exit 63: package.json, lockfile, test.yml, server/index.js and server/errors.js are the same blob at main and head.
#   - exit 31: gate 7's report / IO1F1.md / arm (e) evidence / portal harnesses the brief copies; the READY mail on disk.
#   - exit 45: NODE20-LEG and AZURITE-LEG decided by Tuesday (NOT-RUN | DOCKER-PULL-NEVER), and the prompt told which.
#   - exit 44: something LISTENs on 127.0.0.1:5433 (local Postgres). The launcher never starts a container.
#   - exit 41: the answer route QA/Vision-gate9 exists in fleet/inbox_routing.conf (Tuesday adds it at launch).
#   - exit 38: negative-control seats named in the brief; advisory if one has exited.
#   - exit 32: SELF-CHECK and Self-check note stamped (2026-09-27 09:18 replaced) — LAST.
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/Vision-gate9' "bash '<this file>'"), NEVER nohup.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Contains a legitimate `cd` (into the QA project, at exec).
# READ-ONLY toward the repo: only cat-file, rev-parse, merge-base, log, rev-list, diff, show, grep, ls-remote.
# --check is READ-ONLY: it runs every guard and exits before any identity dir is made or any agent is started.
# Usage: launch_qa_vision_gate9.sh [--check]
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
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-27_vision-gate9-vsp65-qqpurge.md"
READY="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-27_vision-vsp65-READY-mail.txt"
QQ_READY="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-27_vision-qq-purge-READY-mail.txt"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
VSP='/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal'
P_REPO="$VSP/2_Project_Files"
QQ_REPO="$VSP/Quoting Tool/hpas-quoting-tool"
CLAR="$VSP/1_Project_Definition/CLARIFICATIONS.md"
G7_DIR="$QA_DIR/projects/vision/reports/2026-09-23-vision-qq-gate7"
G7_REPORT="$G7_DIR/report.md"
G7_FLOOR="$G7_DIR/evidence/qa-floorcount.py"
REPORT="$QA_DIR/projects/vision/reports/2026-09-27-vision-gate9-vsp65-qqpurge/report.md"
ROUTE_NAME='QA/Vision-gate9'
NEG_SEATS='47349 67576 20317'   # Tuesday (%0), Vision builder (%20), NexusAI (%22) — live at drafting, 2026-09-27 09:01 AEST
# Gated anchors (not heads).
ANCHOR_MAINP1='f95f6254c1e1b296af9717603df60a9ecf33865f'   # portal main before IO1F1 (merge of gate 6's IO1R2 992da21)
ANCHOR_IO1F1='15cd73304bf54b8b3a166635f86fa4723bf415f1'    # gate 7's gated IO1F1 head, merged into main eaf024a

SUBJECT_STEM='[QA/Datasec-Vision -> Tuesday] GATE VERDICT — VSP-65 · QQ retention purge'
QUESTION_SUBJ='[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>'
ANSWER_PREFIX='[Tuesday -> QA/Vision-gate9] ANSWER'

p() { git --no-optional-locks -C "$P_REPO" "$@"; }
q() { git --no-optional-locks -C "$QQ_REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE gate (Vision gate 9) on Datasec/Vision_Sales_Portal with TWO targets in TWO repos and TWO SEPARATE verdicts, each GO or NO-GO: VSP65 in the SALES PORTAL repo (brief §N) and QQPURGE in the QUICKQUOTE repo (brief §Q). A finding on one target never grades the other.

READ YOUR COMMISSION FIRST, whole: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-27_vision-gate9-vsp65-qqpurge.md
Then read the charter it names, the Vision CLARIFICATIONS (C-01..C-06; none covers VSP-65), the project's CLAUDE.md (/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/CLAUDE.md; its deploy commands are not for you), both builder READY mails (/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-27_vision-vsp65-READY-mail.txt and /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-27_vision-qq-purge-READY-mail.txt), the QuickQuote repo's own CLAUDE.md, and gate 7's report, whose IO1F1 arm (e) is the measurement this ticket answers: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-23-vision-qq-gate7 (report.md, sections/IO1F1.md §5, sections/CONVENTIONS.md, evidence/io1/armE-*.txt). Every builder statement is a CLAIM, never evidence. Verify every PRIOR WORK claim against git history and gate 7's evidence, never against the brief.

THE TARGET. VSP65 = Jira VSP-65 = gate 7's arm (e) unfaulted half: branch fix/vsp-65-pool-query-timeout-2026-09-27 at 2adfc4a, three commits (67365ec, 7195df7, 2adfc4a) on portal main eaf024a (the merge of f95f625 + gate 7's gated IO1F1 head 15cd733). It is NOT on main. server/db.js gains query_timeout 30000 ms and connectionTimeoutMillis 15000 ms, env overrides that refuse the boot on a bad value, a named DbTimeoutError, and a BoundedPool whose release discards a client whose query timed out. TIER 1: every database call in the live portal, including the session store on every signed-in request, goes through this pool. Both failure directions are in scope: a stall that still hangs, and a healthy database that now 500s.

WHAT THE BRIEF REQUIRES, in short (the brief is the authority):
  (1) The READY's BEHAVIOUR CHANGES and NOT TESTED lists are carried verbatim in the brief. RULE ON EVERY behaviour change, above all the 15 s pool-wait cap: could a legitimate burst now 500 where it used to wait? Measure it at eaf024a (waits, succeeds) and at 2adfc4a, and answer from the six holders' code how plausible it is. Also rule on the brief's additions: boot-time DDL under the bound, the ROLLBACK that waits a second full bound, the dispatcher re-send, the IO1F1 grace and the query bound both at 30000 ms, the admin backup-db route's headroom, and the boot refusal.
  (2) AN INDEPENDENT REPRODUCTION OF THE HALF-OPEN STALL. Read the builder's proxy in test/db/pool-timeout.test.js before you trust it: it uses net.createServer with the default allowHalfOpen, which answers the app's FIN with a FIN, and it tells Postgres when the app closes. A real half-open peer does neither. Build YOUR OWN stall proxy and run the brief's shapes S1-S8 through the real createApp(), with at least the black hole (S1, no FIN back, never tell Postgres), the one-way stall (S2, the server executes what the client thinks timed out: read pg_stat_activity and pg_locks over a separate direct connection) and the server-side lock wait (S3). Run the starred shapes once at the SHIPPED 30000 / 15000 ms. The positive control is main eaf024a in the same shape, which must hang. Check discard-on-release against ALL SIX pool.connect() callers by reading each one (quotes generate, admin backup-db, the reminders dispatcher, seed, seedCollateral, dbRestore), and measure at least generate and backup-db.
  (3) SUITES AS SETS, NOT COUNTS, against base eaf024a, same machine, same session: npm test and npm run test:db by test NAME, plus CI's coverage command run locally (label it: not CI). The Node 20 leg (production's major) follows the NODE20-LEG line in the brief exactly.
  (4) Red-proofs: parse-checked, fresh tree per arm, node --check rc quoted; a red from a mutant that does not parse is a VOID arm. Assert every tamper landed before reading its result. A behaviour with no reddening cell is a finding.
  (5) CI is UNMEASURED: this project's gh is not authenticated and you must not use gh. Say so, and name CI's Node 22 coverage gate and its e2e:pro step as the first reads at merge.

THE SECOND TARGET. QQPURGE = the QuickQuote retention-purge fix: branch fix/qq-retention-purge-no-literal-2026-09-27 at ac74111, ONE commit on QuickQuote main f255db8, in /Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/Quoting Tool/hpas-quoting-tool (work in stage3/). It is NOT on main. TIER 1: it deletes customer data. purgeQuotes now filters on the partition only, selects RowKey, createdAtMs and status, applies both cutoffs in JS, leaves a row with no usable createdAtMs alone, and deletes row by row (a 404 counts, any other failure is logged by name and kept for the next run). The brief's §Q requires, each measured or READ as it says: the READY's NOT TESTED list (carried verbatim in §Q.1); an INDEPENDENT check of the live-rule FAKE, because Azurite accepts the bare literal that live rejects so the fake is the only red instrument: READ Microsoft's Table service documentation on literal typing yourself (learn.microsoft.com, from your own tool calls only, quoted with URLs), do not re-derive from the builder, and build YOUR OWN docs-following fake that evaluates filters instead of allow-listing one string; the pagination cell, 1,005 rows, measured with byPage on the purge's OWN query; the per-row delete-failure semantics; the "no usable createdAtMs is left alone" branch per stored value (Number() turns "", null and false into 0); the cutoff arithmetic and the strict less-than boundary, with the lazy read agreeing; the new store-azurite CI job, READ ONLY; the removed and renamed test cells, proved BY NAME against f255db8; and the cost claim. The Azurite leg follows the AZURITE-LEG line in the brief exactly: your OWN container or NOT RUN, never a shared emulator and never UseDevelopmentStorage=true. Live QuickQuote (hpas-quickquote) is production: no az, no Azure Table access, no publish, never its logs.

LOCAL POSTGRES ONLY. PRODUCTION IS LIVE for this project. NEVER the live portal (datasec-sales-portal.azurewebsites.net, datasec-sales-portal-rg, its Postgres datasec-sales-db.postgres.database.azure.com, its key vault): no request, no DB connection, not even a GET. No az of any kind, no deploy, no app-setting change. NEVER the live QuickQuote (hpas-quickquote, hpas-quickquote-rg, its Table Storage, hpas-quickquote-logs): no Azure Table access, no publish. Never open a production dump or anything under the project's 4_Credentials. Real sends are OFF: the dispatcher and the backup notifier run only against recorders you wrote.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT from the object store (git archive into a fresh mktemp -d under projects/vision/work-g9/). Each tree is EXCLUSIVE to this gate and to one purpose; never touch work/ or work-g2 .. work-g8. Dependencies: npm ci --offline --ignore-scripts only, then prove node_modules/.package-lock.json against the lockfile entry by entry (lockcmp.py AND lockwalk.py). Never npm install, never npm audit, never npx anything not already in the tree. In EITHER repo use ONLY read verbs (show, log, diff, ls-remote, rev-parse, ls-tree, cat-file, grep, merge-base, archive); never fetch, pull, checkout, switch, worktree, commit, stash, reset, clean or gc. Run git merge-tree --write-tree only from the gate's OWN object dir (GIT_OBJECT_DIRECTORY = your own mktemp -d, alternates = the repo's objects), or skip it and say so. Findings-only: no writes in the portal repo or the QuickQuote repo, none inside Vision_Sales_Portal, none in gate 1-8's report folders or trees. Never rm: quarantine. Run every loop and every git show <sha>:<path> under bash. CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY: a control derived from the run it validates is not a control.

FLOOR DISCIPLINE. Vision has no jest lock; never borrow NexusAI's. Never use ports 4848, 8080 or 47787; take every port from the kernel and bind 127.0.0.1. Never start the portal's own entry point (it binds all interfaces); use the real createApp() in your harness. Postgres is the local container on 127.0.0.1:5433, and ONLY databases you create: vsp_qa_g9_<epoch> and vsp_qa_g9_<epoch>_test (the test name MUST end in _test); never salesportal, salesportal_test, any vsp_qa_g1..g8 database or the builder's vsp_bf1_*. The module's default URL is the builder's dev database, so give every product process YOUR DATABASE_URL and TEST_DATABASE_URL explicitly and print the database each one reached. Release every lock and direct session you open in a finally. No docker command at all, except the Node 20 exception (§N.7) when the NODE20-LEG line reads DOCKER-PULL-NEVER and the own-Azurite exception (§Q.8) when the AZURITE-LEG line does. Every product process runs under env -i with an explicit allowlist, NODE_ENV never production. Never set AGENTMAIL_API_KEY or AGENTMAIL_INBOX in a product process (with both set, QuickQuote SENDS FOR REAL), nor any real ACS_* or MAIL_SENDER, AZURE_BACKUP_CONN_STR, TABLES_CONNECTION_STRING, SALES_COPY_EMAIL, a real NTFY_TOPIC, LEAD_BOT_API_KEY or WEBSITE_SITE_NAME; print each product process's env KEY NAMES and assert none is forbidden. NTFY_SERVER=http://ntfy.invalid; never contact ntfy.sh; stub fetch to throw on any other URL. Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid, with the brief's negative-control seats classifying FOREIGN in the same run. A zero is reportable only beside an ATTACHED control that fired in the same window. Other gates are live on this box: record the load average beside every timing number; a latency result with no load figure is not a measurement.
DEADLINE AND HEARTBEAT: every step has a written DEADLINE built into your runner (there is no timeout binary here) and releases its servers, proxies, sessions, locks and children in a finally. Log a HEARTBEAT line at least every 2 minutes; a step with no heartbeat for 5 minutes is aborted and reported, never waited on. Deadlines: requests at the shrunk bound 20 s; requests at the SHIPPED bounds 120 s; the pool-wait burst and the lock arm 180 s; one test:db file 180 s; a whole test:db run 420 s. Nothing above 420 s. A hang at eaf024a is the expected positive control, reported as such.

QUESTIONS: your routing name is QA/Vision-gate9. If you must ask, mail tuesday-agent@agentmail.to with the subject "[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>" and proceed on the safest reading without waiting. Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/Vision-gate9] ANSWER"; read it with your verdict key. Never wednesday-agent@. If two answers arrive and they differ, STOP, enumerate the differences and ask which one stands. If a response is cut off by a safety check, record it and continue with the next item; this is authorised defensive QA of Datasec's own product on loopback. Record every question, reading and answer in the report.

Write your report to: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-27-vision-gate9-vsp65-qqpurge/report.md

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with a subject beginning exactly:
[QA/Datasec-Vision -> Tuesday] GATE VERDICT — VSP-65 · QQ retention purge: VSP65 @ 2adfc4a <GO | NO-GO> · QQPURGE @ ac74111 <GO | NO-GO>
Lead the body with two sentences, one per target: (VSP65) does a half-open Postgres connection now end every signed-in request within the bound, on YOUR proxy as well as the builder's, and does any legitimate shape now 500 where main served it? (QQPURGE) does the head delete exactly the rows past each cutoff on every page, with no numeric literal in the filter, and does your docs-following fake agree? You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no credentials directory of its own. Use it only in your own mail calls, with a client timeout. Never put the key or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice.

Report the pinned head and main as three timestamped readings (start / mid / end), with the branch name beside each. Include the verbatim operator strings: the DbTimeoutError log lines for DB_QUERY_TIMEOUT and DB_CONNECT_TIMEOUT at the shipped values, the boot refusal for a bad override, pg's three source strings with file:line, and QQPURGE's per-row failure log line from a real run. Then one paragraph on the queue: the merge-tree result for each target against its main (expected CLEAN, equal to the head's own tree), the cells to re-run on each merged head, and CI at merge.

Rule 2 stands: what you did NOT test is first-class output. Write a NOT TESTED section that covers at least CI (UNMEASURED, both repos, including the store-azurite job), a real stalled Azure Postgres / TLS / failover, real Azure Table Storage paging and literal typing, live's stored type of createdAtMs, Node 20 and Node 22, the container images, e2e:pro / e2e:api / e2e:feedback, and production-scale data. Label every action recommendation MEASURED AT RUNTIME, PROBED or READ ONLY.
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
EXPECT_IDS='MAIN-P VSP65 MAIN-Q QQPURGE'
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
  printf '%s' "$R" | grep -q '@' && { echo "REFUSING: PIN row $ID still carries a placeholder: $R" >&2; exit 40; }
  is40 "$(fld "$ID" 4)" || { echo "REFUSING: PIN row $ID head is not a 40-hex sha: '$(fld "$ID" 4)'" >&2; exit 40; }
  case "$ID" in MAIN-P|VSP65) WANT_REPO=portal ;; *) WANT_REPO=quickquote ;; esac
  [ "$(fld "$ID" 2)" = "$WANT_REPO" ] || { echo "REFUSING: PIN row $ID repo must be $WANT_REPO" >&2; exit 40; }
done
[ "$(fld MAIN-P 3)" = "main" ] || { echo "REFUSING: row MAIN-P branch must be main" >&2; exit 40; }
[ "$(fld MAIN-Q 3)" = "main" ] || { echo "REFUSING: row MAIN-Q branch must be main" >&2; exit 40; }
[ "$(fld QQPURGE 3)" = "fix/qq-retention-purge-no-literal-2026-09-27" ] || { echo "REFUSING: row QQPURGE branch is '$(fld QQPURGE 3)', the brief's target is fix/qq-retention-purge-no-literal-2026-09-27 — re-brief" >&2; exit 40; }
is40 "$(fld QQPURGE 5)" || { echo "REFUSING: PIN row QQPURGE base is not a 40-hex sha" >&2; exit 40; }
printf '%s' "$(fld QQPURGE 6)" | grep -Eq '^[1-9][0-9]*$' || { echo "REFUSING: PIN row QQPURGE commits is not a positive integer" >&2; exit 40; }
[ "$(fld VSP65 3)" = "fix/vsp-65-pool-query-timeout-2026-09-27" ] || { echo "REFUSING: row VSP65 branch is '$(fld VSP65 3)', the brief's target is fix/vsp-65-pool-query-timeout-2026-09-27 — re-brief" >&2; exit 40; }
is40 "$(fld VSP65 5)" || { echo "REFUSING: PIN row VSP65 base is not a 40-hex sha" >&2; exit 40; }
printf '%s' "$(fld VSP65 6)" | grep -Eq '^[1-9][0-9]*$' || { echo "REFUSING: PIN row VSP65 commits is not a positive integer" >&2; exit 40; }
HEAD_SHA="$(fld VSP65 4)"; BASE="$(fld VSP65 5)"; NCOMMITS="$(fld VSP65 6)"; MAINH="$(fld MAIN-P 4)"; HEAD7="${HEAD_SHA:0:7}"

# 6 / 7 / 8 — commits; base ancestor AND merge-base; base is MAIN (a stale base passes with a NOTE); not on main; exact count.
for S in "$MAINH" "$HEAD_SHA" "$BASE"; do
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

# 9 — gated anchors: main is the merge of f95f625 + gate 7's gated IO1F1 head 15cd733.
[ "$(p log -1 --format='%P' "$MAINH" 2>/dev/null)" = "$ANCHOR_MAINP1 $ANCHOR_IO1F1" ] \
  || echo "NOTE: portal main ${MAINH:0:7}'s parents are '$(p log -1 --format='%P' "$MAINH" 2>/dev/null)', not f95f625 + 15cd733 — main moved since drafting; the brief's PRIOR ROUND wording may be stale" >&2
p merge-base --is-ancestor "$ANCHOR_IO1F1" "$HEAD_SHA" 2>/dev/null \
  || { echo "REFUSING: $HEAD7 does not contain gate 7's gated IO1F1 head 15cd733 — the arm (e) story is wrong; re-brief" >&2; exit 9; }

# 18 — RE-PIN: both rows at origin, by ls-remote, read NOW (immediately before launch).
for ID in MAIN-P VSP65; do
  BR="$(fld "$ID" 3)"; H="$(fld "$ID" 4)"
  L="$(p ls-remote origin "refs/heads/$BR" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: row $ID: $H is not at refs/heads/$BR on origin — that head moved or was never pushed; re-pin" >&2; printf '%s\n' "${L:-<nothing>}" >&2; exit 18; }
done
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — exact file set over main.
FS_MAIN='BACKLOG.md
server/db.js
server/db.test.js
test/db/pool-timeout.test.js'
GOT="$(p diff --name-only "$BASE" "$HEAD_SHA" 2>/dev/null | sort)"
[ "$GOT" = "$(sorted "$FS_MAIN")" ] || { echo "REFUSING: $HEAD7's delta over main is not exactly the briefed 4 files. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }

# 74 — VSP-65 content, read from the pinned head (never a checkout).
has() { p show "${1}:${2}" 2>/dev/null | grep -qF -- "$3"; }   # sha path fixed-string
for T in 'const DEFAULT_QUERY_TIMEOUT_MS = 30000;' 'const DEFAULT_CONNECT_TIMEOUT_MS = 15000;' 'max: 10,' \
         "query_timeout: positiveMs(env, 'DB_QUERY_TIMEOUT_MS', DEFAULT_QUERY_TIMEOUT_MS)," \
         "connectionTimeoutMillis: positiveMs(env, 'DB_CONNECT_TIMEOUT_MS', DEFAULT_CONNECT_TIMEOUT_MS)," \
         'class BoundedPool extends Pool {' 'class DbTimeoutError extends Error {' \
         'client.release = function (err) { return release.call(this, err || client[TIMED_OUT]); };' \
         "const PG_QUERY_TIMEOUT = 'Query read timeout';" 'const pool = new BoundedPool({' \
         "pool.on('error', (err) => {" 'module.exports = { pool, query, poolOptions, BoundedPool, DbTimeoutError };'; do
  has "$HEAD_SHA" server/db.js "$T" || { echo "REFUSING: $HEAD7's server/db.js lacks '$T' — the brief gates a different change; re-brief" >&2; exit 74; }
done
has "$HEAD_SHA" server/db.js 'statement_timeout:' && { echo "REFUSING: $HEAD7's server/db.js sets a statement_timeout — the READY says it was NOT added; re-brief" >&2; exit 74; }
has "$MAINH" server/db.js 'query_timeout' && { echo "REFUSING: main ${MAINH:0:7}'s server/db.js already carries query_timeout — the positive control (main hangs) is gone; re-brief" >&2; exit 74; }
# The six pool.connect() callers the brief tables, and no seventh, over the named non-test server/scripts files.
CALLERS="$(bash -c 'r="$1"; h="$2"; f=$(git --no-optional-locks -C "$r" ls-tree -r --name-only "$h" -- server scripts | grep -E "\.js$" | grep -v "test\.js$"); git --no-optional-locks -C "$r" grep -n -F "pool.connect()" "$h" -- $f' _ "$P_REPO" "$HEAD_SHA" 2>/dev/null \
  | sed "s#^${HEAD_SHA}:##" | awk -F: '{print $1":"$2}' | grep -v '^server/db.js:' | sort)"
EXPECT_CALLERS='server/dbRestore.js:149
server/reminders/dispatcher.js:121
server/routes/admin.js:93
server/routes/quotes.js:262
server/seed.js:18
server/seedCollateral.js:13'
[ "$CALLERS" = "$(sorted "$EXPECT_CALLERS")" ] || { echo "REFUSING: at $HEAD7 the pool.connect() callers are not exactly the six the brief tables. Got:" >&2; printf '%s\n' "$CALLERS" >&2; exit 74; }
has "$HEAD_SHA" server/index.js 'store: new PgSession({ pool, createTableIfMissing: true }),' \
  || { echo "REFUSING: at $HEAD7 the session store is no longer PgSession on the shared pool — re-brief" >&2; exit 74; }
[ "$(p show "${HEAD_SHA}:test/db/pool-timeout.test.js" 2>/dev/null | grep -c '^test(')" = "6" ] \
  || { echo "REFUSING: $HEAD7's pool-timeout.test.js does not carry the READY's 6 cells" >&2; exit 74; }
has "$HEAD_SHA" test/db/pool-timeout.test.js 'const proxy = net.createServer((app) => {' \
  || { echo "REFUSING: $HEAD7's builder proxy is no longer net.createServer with default allowHalfOpen — the brief's correction (a) is stale" >&2; exit 74; }
has "$HEAD_SHA" BACKLOG.md 'Jira VSP-65' || { echo "REFUSING: $HEAD7's BACKLOG does not carry the VSP-65 key" >&2; exit 74; }

# ================================================================ QQPURGE (the QuickQuote repo) — 6 7 8 18 22 74 63
[ -d "$QQ_REPO/.git" ] || [ -f "$QQ_REPO/.git" ] || { echo "repo under test missing: $QQ_REPO" >&2; exit 5; }
QH="$(fld QQPURGE 4)"; QB="$(fld QQPURGE 5)"; QN="$(fld QQPURGE 6)"; QM="$(fld MAIN-Q 4)"; QH7="${QH:0:7}"
for S in "$QM" "$QH" "$QB"; do
  T="$(q cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in the QuickQuote repo (got '$T') — this launcher never fetches" >&2; exit 6; }
done
if [ "$QB" != "$QM" ]; then
  if q merge-base --is-ancestor "$QB" "$QM" 2>/dev/null && [ "$(q merge-base "$QH" "$QM" 2>/dev/null)" = "$QB" ]; then
    STALE="$STALE QQPURGE"
    echo "NOTE: row QQPURGE is a STALE-BASE row (base ${QB:0:7} is an ancestor of MAIN-Q ${QM:0:7}); the brief expects it NOT stale — §12 may be stale" >&2
  else
    echo "REFUSING: row QQPURGE base ${QB:0:7} is neither MAIN-Q nor merge-base(head, MAIN-Q) on MAIN-Q — re-pin" >&2; exit 7
  fi
fi
[ "$(q merge-base "$QB" "$QH" 2>/dev/null)" = "$QB" ] || { echo "REFUSING: QQPURGE base ${QB:0:7} is not the merge-base with $QH7" >&2; exit 7; }
q merge-base --is-ancestor "$QH" "$QM" 2>/dev/null && { echo "REFUSING: $QH7 is ALREADY ON QuickQuote main ${QM:0:7} — re-brief" >&2; exit 7; }
[ "$(q rev-list --count "${QB}..${QH}" 2>/dev/null)" = "$QN" ] || { echo "REFUSING: $QH7 has $(q rev-list --count "${QB}..${QH}") commits over its base, the table says $QN" >&2; exit 8; }
[ "$(q log -1 --format='%P' "$QH" 2>/dev/null)" = "$QB" ] || { echo "REFUSING: $QH7's parent list is not exactly its base ${QB:0:7} — the brief gates ONE commit; re-brief" >&2; exit 8; }
QBEH="$(q rev-list --count "${QH}..${QM}" 2>/dev/null)"
[ "$QBEH" = "0" ] || echo "NOTE: $QH7 is $QBEH behind QuickQuote main ${QM:0:7} — the brief says 0 behind; §12 may be stale" >&2
for ID in MAIN-Q QQPURGE; do
  BR="$(fld "$ID" 3)"; H="$(fld "$ID" 4)"
  L="$(q ls-remote origin "refs/heads/$BR" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: row $ID: $H is not at refs/heads/$BR on origin — that head moved or was never pushed; re-pin" >&2; printf '%s\n' "${L:-<nothing>}" >&2; exit 18; }
done
PIN_TS="$PIN_TS / QuickQuote $(date '+%H:%M:%S %Z')"
FS_Q='.github/workflows/tests.yml
BACKLOG.md
CLAUDE.md
stage3/lib/store.js
stage3/package.json
stage3/test/server.test.mjs
stage3/test/store-azurite.test.mjs
stage3/test/store.test.mjs'
GOT="$(q diff --name-only "$QB" "$QH" 2>/dev/null | sort)"
[ "$GOT" = "$(sorted "$FS_Q")" ] || { echo "REFUSING: $QH7's delta over QuickQuote main is not exactly the briefed 8 files. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }
qhas() { q show "${1}:${2}" 2>/dev/null | grep -qF -- "$3"; }
for T in 'queryOptions: { filter: "PartitionKey eq '"'"'q'"'"'", select: ["RowKey", "createdAtMs", "status"] }' \
         'const at = Number(e.createdAtMs);' 'if (!Number.isFinite(at)) continue;' \
         'if (at < exp || (e.status === "pending" && at < pen)) doomed.push(e.rowKey);' \
         'if (e && e.statusCode === 404) { gone++; continue; }' 'kept for the next run:' 'return gone;'; do
  qhas "$QH" stage3/lib/store.js "$T" || { echo "REFUSING: $QH7's stage3/lib/store.js lacks '$T' — the brief gates a different purge; re-brief" >&2; exit 74; }
done
qhas "$QH" stage3/lib/store.js 'createdAtMs lt ${' && { echo "REFUSING: $QH7's purge still interpolates a cutoff into the filter" >&2; exit 74; }
qhas "$QB" stage3/lib/store.js 'createdAtMs lt ${exp}' || { echo "REFUSING: base ${QB:0:7}'s purge does not carry the literal filter — the positive control is gone; re-brief" >&2; exit 74; }
[ "$(q show "${QB}:stage3/test/store.test.mjs" 2>/dev/null | grep -c '^test(')" = "2" ] || { echo "REFUSING: base store.test.mjs does not carry the 2 cells the brief names" >&2; exit 74; }
[ "$(q show "${QH}:stage3/test/store.test.mjs" 2>/dev/null | grep -c '^test(')" = "4" ] || { echo "REFUSING: head store.test.mjs does not carry 4 cells" >&2; exit 74; }
[ "$(q show "${QH}:stage3/test/store-azurite.test.mjs" 2>/dev/null | grep -c '^test(')" = "2" ] || { echo "REFUSING: head store-azurite.test.mjs does not carry 2 cells" >&2; exit 74; }
for T in 'test("purgeQuotes sends the retention + stale-pending filter and deletes what comes back"' \
         'test("purgeQuotes refuses a cutoff that is not a number (nothing else reaches the filter)"'; do
  qhas "$QB" stage3/test/store.test.mjs "$T" || { echo "REFUSING: base lacks the cell the brief names as removed/renamed: $T" >&2; exit 74; }
  qhas "$QH" stage3/test/store.test.mjs "$T" && { echo "REFUSING: head still carries the cell the brief names as removed/renamed: $T" >&2; exit 74; }
done
qhas "$QH" stage3/test/store.test.mjs 'test("purgeQuotes refuses a cutoff that is not a number", async' || { echo "REFUSING: head lacks the renamed cell" >&2; exit 74; }
qhas "$QH" stage3/test/store.test.mjs 'if (filter !== "PartitionKey eq '"'"'q'"'"'") throw new Error(`fake SDK: filter not evaluated here' \
  || { echo "REFUSING: the fake is no longer an allowlist — the brief's correction Q.0(a) is stale" >&2; exit 74; }
qhas "$QH" stage3/test/store-azurite.test.mjs '.byPage()' || { echo "REFUSING: the Azurite pagination cell no longer uses byPage" >&2; exit 74; }
qhas "$QH" stage3/package.json '"test:azurite": "node --test test/store-azurite.test.mjs"' || { echo "REFUSING: head package.json lacks test:azurite" >&2; exit 74; }
qhas "$QH" .github/workflows/tests.yml '  store-azurite:' || { echo "REFUSING: head CI lacks the store-azurite job" >&2; exit 74; }
qhas "$QH" .github/workflows/tests.yml 'image: mcr.microsoft.com/azure-storage/azurite' || echo "NOTE: the store-azurite image line changed — §Q.0(e) (unpinned image) may be stale" >&2
qhas "$QH" stage3/server.js 'if (clock().getTime() - Number(row.createdAtMs) > QUOTE_RETENTION_MS) {' || { echo "REFUSING: the lazy-read retention check the brief compares against moved" >&2; exit 74; }
W="$(q rev-parse "${QM}:stage3/package-lock.json" 2>/dev/null)"; GOTL="$(q rev-parse "${QH}:stage3/package-lock.json" 2>/dev/null)"
[ -n "$W" ] && [ "$GOTL" = "$W" ] || { echo "REFUSING: stage3 lockfile at $QH7 is ${GOTL:0:7}, main's is ${W:0:7} — a dependency change the brief does not gate" >&2; exit 63; }
[ "$(q rev-parse "${QM}:stage3/server.js" 2>/dev/null)" = "$(q rev-parse "${QH}:stage3/server.js" 2>/dev/null)" ] || { echo "REFUSING: stage3/server.js differs between QuickQuote main and $QH7 — the brief says it is untouched" >&2; exit 63; }

# 63 — no dependency, CI, entry-point or error-handler change: same blobs at main and head.
for F in package.json package-lock.json .github/workflows/test.yml server/index.js server/errors.js; do
  W="$(p rev-parse "${MAINH}:$F" 2>/dev/null)"; GOTB="$(p rev-parse "${HEAD_SHA}:$F" 2>/dev/null)"
  [ -n "$W" ] && [ "$GOTB" = "$W" ] || { echo "REFUSING: $F at $HEAD7 is ${GOTB:0:7}, main's is ${W:0:7} — a change the brief does not gate" >&2; exit 63; }
done
for T in 'npm ci --offline --ignore-scripts' 'entry by entry' 'never npm audit'; do
  grep -qiF "$T" "$BRIEF" || { echo "REFUSING: brief lacks the dependency rule '$T'" >&2; exit 63; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the dependency rule '$T'" >&2; exit 63 ;; esac
done

# 31 — the prior measurement and the READY are on disk and named.
[ -s "$READY" ] || { echo "REFUSING: the READY mail is not on disk: $READY" >&2; exit 31; }
[ -s "$QQ_READY" ] || { echo "REFUSING: the QQ READY mail is not on disk: $QQ_READY" >&2; exit 31; }
while IFS= read -r T; do
  [ -n "$T" ] || continue
  grep -qxF -- "$T" "$QQ_READY" || { echo "REFUSING: the QQ READY no longer carries: $T" >&2; exit 31; }
  grep -qxF -- "$T" "$BRIEF" || { echo "REFUSING: the brief does not carry the QQ READY's NOT TESTED line verbatim: $T" >&2; exit 31; }
done <<< "$(awk '/^NOT TESTED$/{f=1;next} f&&/^- /{print} f&&/^HELD/{exit}' "$QQ_READY")"
[ "$(awk '/^NOT TESTED$/{f=1;next} f&&/^- /{n++} f&&/^HELD/{exit} END{print n+0}' "$QQ_READY")" = "6" ] || { echo "REFUSING: the QQ READY's NOT TESTED list is not the 6 lines the brief carries" >&2; exit 31; }
for T in 'BEHAVIOUR CHANGES FOR THE GATE TO WEIGH' 'NOT TESTED' 'connectionTimeoutMillis also caps WAITING for a free client when all 10 are busy.' \
         'The shipped 30 s / 15 s values in a live stall'; do
  grep -qF -- "$T" "$READY" || { echo "REFUSING: the READY no longer carries '$T'" >&2; exit 31; }
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: the brief does not carry the READY's '$T' verbatim" >&2; exit 31; }
done
[ -s "$CLAR" ] || { echo "REFUSING: Vision CLARIFICATIONS.md absent: $CLAR" >&2; exit 31; }
for C in 'C-01.' 'C-06.'; do grep -qF "**$C" "$CLAR" || { echo "REFUSING: $CLAR lacks $C" >&2; exit 31; }; done
grep -qF '**C-07.' "$CLAR" && echo "NOTE: Vision CLARIFICATIONS now has a C-07 — the brief says C-01..C-06; read it before launch" >&2
grep -qiF 'VSP-65' "$CLAR" && echo "NOTE: Vision CLARIFICATIONS now mentions VSP-65 — the brief says no C-entry covers it; read it before launch" >&2
[ -s "$G7_REPORT" ] || { echo "REFUSING: gate 7's report is absent: $G7_REPORT" >&2; exit 31; }
[ -s "$G7_DIR/sections/IO1F1.md" ] || { echo "REFUSING: gate 7's sections/IO1F1.md is absent" >&2; exit 31; }
grep -qF 'STILL-OPEN-45000ms after 45001 ms' "$G7_REPORT" \
  || { echo "REFUSING: gate 7's arm (e) unfaulted line (45001 ms) is not in its report — the brief's PRIOR ROUND has no source" >&2; exit 31; }
for S in evidence/io1/armE-shipped.txt evidence/io1/armE0-deadread.txt; do
  [ -s "$G7_DIR/$S" ] || { echo "REFUSING: gate 7's $S is absent — the brief names it" >&2; exit 31; }
done
grep -qF "$G7_DIR" "$BRIEF" || { echo "REFUSING: the brief does not name gate 7's report path" >&2; exit 31; }
case "$PROMPT" in *"$G7_DIR"*) ;; *) echo "REFUSING: the prompt does not name gate 7's report path" >&2; exit 31 ;; esac
for H in mktree-portal.sh qa-mkdb.cjs qa-dbcheck.cjs qa-harness-io1-edges.cjs qa-harness-io1-boot.cjs qa-harness-lead-io1-hang.cjs \
         qa-io1-preload-fetchguard.cjs qa-io1-preload-hidelayer.cjs IO1-count-async.py qa-run.py qa-floorcount.py lockcmp.py lockwalk.py; do
  [ -s "$G7_DIR/evidence/$H" ] || { echo "REFUSING: gate 7's harness $H is not on disk — the brief tells the gate to copy it" >&2; exit 31; }
done

# 39 — the floor instrument is on disk and named.
[ -s "$G7_FLOOR" ] || { echo "REFUSING: gate 7's floor instrument missing: $G7_FLOOR" >&2; exit 39; }
grep -qF 'qa-floorcount.py' "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument qa-floorcount.py" >&2; exit 39; }

# 41 — the answer route exists (Tuesday adds 'QA/Vision-gate9|tuesday-agent@agentmail.to|no' at launch).
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || {
  echo "REFUSING: no '${ROUTE_NAME}|tuesday-agent@agentmail.to|…' line in $ROUTING — answers to the gate would have no route. Add it (pattern: the QA/Vision-gate8 line) before launch." >&2; exit 41; }

# 10 / 17 — report path named in both; no stale report.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

# 12 — tier declared in both.
grep -qF 'VSP65 (the pool query/connect timeout) is TIER 1' "$BRIEF" || { echo "REFUSING: brief does not declare the tier" >&2; exit 12; }
for T in 'TIER 1' 'Both failure directions are in scope'; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare: $T" >&2; exit 12 ;; esac
done

# 78 — the commission's five requirements, in both.
for T in '15 s pool-wait' 'legitimate burst' 'INDEPENDENT REPRODUCTION' 'allowHalfOpen' 'ALL SIX' 'SETS, NOT COUNTS' 'eaf024a' \
         'Node 20' 'NODE20-LEG' 'UNMEASURED' 'PRODUCTION IS LIVE' 'datasec-sales-db.postgres.database.azure.com' 'S1' 'S2' 'S3' 'positive control' \
         'QQPURGE' 'ac74111' 'f255db8' 'FAKE' 'learn.microsoft.com' 'docs-following fake' '1,005 rows' 'byPage' 'per-row' 'usable createdAtMs' \
         'strict less-than' 'store-azurite' 'BY NAME' 'cost claim' 'AZURITE-LEG' 'hpas-quickquote' 'no Azure Table access' 'no publish'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks '$T'" >&2; exit 78; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks '$T'" >&2; exit 78 ;; esac
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
WORDS="merge-tree NOT%TESTED env%-i bash createApp() 2adfc4a eaf024a 15cd733 work-g9 vsp_qa_g9 _test pg_stat_activity pg_locks
FOREGROUND MEASURED%AT%RUNTIME PROBED READ%ONLY start%/%mid%/%end CI node%--check VOID DbTimeoutError DB_QUERY_TIMEOUT DB_CONNECT_TIMEOUT"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## Charter' '^## RULED BY KAM, AND SETTLED' '^## PRIOR ROUND' '^## PIN' '^## WRONG OR UNVERIFIABLE' \
         '^## THE READY' '^## 2a. LEGITIMATE SHAPES' '^## N. TARGET VSP65' '^## Q. TARGET QQPURGE' '^### Q.0 WRONG OR UNVERIFIABLE' \
         '^### Q.1 THE QQPURGE READY' '^### Q.2 THE LIVE-RULE FAKE' '^### Q.10 QQPURGE FAIL CONDITIONS' '^## 12. The merge' '^## 13. FLOOR' '^## 14. Output' '^PROVENANCE:'; do
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
for T in 'EXCLUSIVE' 'work-g9'; do
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
AZURITE="$(sed -n 's/^AZURITE-LEG: \([A-Z-]*\)[[:space:]]*$/\1/p' "$BRIEF" | head -1)"
case "$AZURITE" in
  NOT-RUN|DOCKER-PULL-NEVER) ;;
  "$PH_NODE20") echo "REFUSING: the brief's AZURITE-LEG line is still ${PH_NODE20} — Tuesday decides NOT-RUN or DOCKER-PULL-NEVER before launch (brief top, and §Q.8)" >&2; exit 45 ;;
  *) echo "REFUSING: the brief's AZURITE-LEG line reads '${AZURITE:-<missing>}' — it must be exactly NOT-RUN or DOCKER-PULL-NEVER" >&2; exit 45 ;;
esac

# 44 — local Postgres is listening on :5433. The launcher never starts a container; the Vision seat does.
lsof -nP -iTCP:5433 -sTCP:LISTEN >/dev/null 2>&1 \
  || { echo "REFUSING: nothing LISTENs on :5433 — the gate's runtime legs would all be NOT RUN. Ask the Vision seat to start its local vsp-dev-db (never from this launcher, never from the gate), then re-run --check." >&2; exit 44; }

# 32 — the coordinator stamps the self-check (line AND note). LAST, so --check shows every other guard first.
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "guards pass (40 6 7 8 9 18 22 74 63 31 39 41 10 17 12 78 13 14 15 20 70 19 24 53 60 61 62 64 69 75 38 45 44); self-check NOT stamped." >&2
  echo "REFUSING: the brief's SELF-CHECK line or Self-check note is unstamped — the coordinator re-reads end-to-end and stamps both before launch" >&2; exit 32
fi

PIN_BLOCK="$(printf 'PINNED HEADS — verified by the launcher at %s (per repo: cat-file, base ancestry and merge-base, not-already-on-main, commit count; gated anchor 15cd733 for VSP65, single parent f255db8 for QQPURGE; git ls-remote origin for all four rows):\n' "$PIN_TS"
  printf '%s\n' "$PIN" | awk -F'\t' '{ printf "  %-7s %-7s %-42s %s  base %s  commits %s\n", $1, $2, $3, $4, ($5=="-"?"-":substr($5,1,12)), $6 }'
  printf '  STALE-BASE rows (forward merge owed at merge time):%s\n' "${STALE:- none}"
  printf 'NODE20-LEG, as Tuesday decided it in the brief: %s\n' "$NODE20"
  printf 'AZURITE-LEG, as Tuesday decided it in the brief: %s\n' "$AZURITE")"

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  printf '%s\n' "$PIN_BLOCK"
  echo "  PIN parsed from the brief (40); commits, base, not-on-main, count $NCOMMITS, 0 behind (6 7 8); 15cd733 contained (9); origin re-read $PIN_TS (18)"
  echo "  file set: 4 over main (22); db.js defaults 30000/15000, BoundedPool, release override, no statement_timeout, main has no query_timeout, six pool.connect() callers, PgSession on the pool, 6 pool-timeout cells, builder proxy shape, BACKLOG key (74)"
  echo "  QQPURGE: 4-row PIN, commits/base/one parent/origin (6 7 8 18); 8 files (22); purge content, base literal filter, 2->4 store cells by name, fake allowlist, byPage, test:azurite, CI job, lazy-read line (74); stage3 lockfile + server.js unchanged (63); QQ READY NOT TESTED verbatim, 6 lines (31)"
  echo "  same blobs: package.json, lockfile, test.yml, server/index.js, server/errors.js (63); READY verbatim + C-01..C-06 + gate 7 arm (e) + harnesses (31); floor instrument (39); route $ROUTE_NAME (41); report absent (17)"
  echo "  tier (12); commission requirements (78); directive/brief/placeholders/mail/key/questions/safety (13 14 15 20 70); words + sections (19); no server path (24); standing rules (53 60 61 62 64 69 75); seats $NEG_SEATS (38); NODE20 $NODE20 AZURITE $AZURITE (45); :5433 listening (44); self-check stamped (32)"
  exit 0
fi

# 11 — no inherited identity: this gate needs neither az nor gh, so both point at fresh EMPTY directories.
ID_TMP="$(mktemp -d "${TMPDIR:-/tmp}/qa-vision-gate9-id.XXXXXX")" || { echo "REFUSING: cannot create the empty identity dir" >&2; exit 11; }
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
