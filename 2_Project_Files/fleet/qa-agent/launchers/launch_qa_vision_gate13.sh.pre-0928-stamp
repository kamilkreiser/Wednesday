#!/bin/bash
# launch_qa_vision_gate13.sh — cross-project QA agent, ONE gate (Vision gate 13; drafted 2026-09-28 11:2x AEST from the gate-12 launcher) on
# Datasec/Vision_Sales_Portal: a NARROW RE-GATE, TWO targets, TWO verdicts plus one merge line:
#   VSP74  fix/vsp-74-restore-refuses-incomplete-2026-09-28  ROUND 2 OF 2 (a NO-GO goes to Kam): VSP74-G12-F1 only — restorePlan by OID  TIER 1
#   VSP75  fix/vsp-75-backup-all-tables-2026-09-28           NEW HEAD = 41c4a66 (GO) + VSP-74 r2 (4843aed) + main e59232e (110bb03)   TIER 1
#
# Main is e59232e (gate 12's 609e967 + VSP-69 merged). VSP74's base is 609e967 and it is behind main by EXACTLY the VSP-69 chain (it reaches
# main only through VSP75: gate 12's MERGE COUPLING). VSP75's base is main e59232e, 0 behind. Main may since have moved ONLY to a descendant
# of e59232e that touches none of the targets' files (NOTE).
#
# THE HEADS LIVE IN ONE PLACE: the brief's PIN-HEADS table. This launcher PARSES it, refuses any placeholder, verifies every row against the
# object store and against origin by `git ls-remote` NOW, and appends the verified table to the agent's prompt. The only shas it carries are
# GATED ANCHORS: gate 12's heads (a1794ad NO-GO, 41c4a66 GO, e79682a GO), main-at-gate-12 609e967, the forward/merge commits 4843aed and the
# VSP-69 chain, gate 12's exact non-merge chains, 0d992e0 (parent b5c3e8d), 12138cb, e34add4 (the cascade-matrix positive control).
#
# PRODUCTION IS LIVE for this project (datasec-sales-portal-rg). The gate is local Postgres only. Findings only.
#
# GUARDS RE-DERIVED from launch_qa_vision_gate12.sh (kept as the template, untouched). Differences:
#   - PIN: three rows (MAIN-P e59232e, VSP74 4813e5f base 609e967 x9, VSP75 110bb03 base e59232e x23); VSP74 "behind main" = the VSP-69 chain.
#   - exit 9: exact non-merge chains = gate 12's + 4813e5f; merges two-parent, second parent on main or (VSP75) on VSP74; the round-2 merge
#     parents pinned (4813e5f<-a1794ad, 4843aed = 41c4a66 + 4813e5f, 110bb03 = 4843aed + e59232e, e59232e = 609e967 + e79682a).
#   - exit 22: file sets 4 (609e967..4813e5f) / 10 (e59232e..110bb03); 4813e5f itself touches exactly 3 files.
#   - exit 74: the OID plan (liveTables, pg_class, conrelid::text, reaches) present and the regclass/pg_tables form ABSENT on both heads;
#     test( 17/10 and 17/12/2/6/3/10/5; the 12 original restore-incomplete cells unchanged (0 deleted lines); the original plan cells kept
#     verbatim; VSP75's backup-side blobs = 41c4a66's (the GO'd scope did not move); dispatcher/dispatch-once = main's.
#   - exit 31: READYs checked by SUBJECT sha7 and NOT TESTED block carried verbatim (they carry no "New head (ls-remote)" line);
#     CLARIFICATIONS C-07 required; gate 12's report + evidence/tools required.
#   - exit 41 (route) runs LAST before the stamp check (32), so --check exercises every other guard before refusing on the route.
#   - exit 38: negative-control seats re-read 11:31:58 AEST (Tuesday 59108, NexusAI P 20317, QA/NexusAI-batch5b 91381; the Vision seat 7956 exited).
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/Vision-gate13' "bash '<this file>'"), NEVER nohup.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Contains a legitimate `cd` (into the QA project, at exec).
# READ-ONLY toward the repo: only cat-file, rev-parse, merge-base, log, rev-list, diff, show, ls-remote.
# --check is READ-ONLY: it runs every guard and exits before any identity dir is made or any agent is started.
# Usage: launch_qa_vision_gate13.sh [--check]
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
BRIEF="$BRIEFS/2026-09-28_vision-gate13-vsp74r2-vsp75.md"
READY74="$BRIEFS/2026-09-28_vision-vsp74-r4-READY-mail.txt"
READY75="$BRIEFS/2026-09-28_vision-vsp75-r4-READY-mail.txt"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
VSP='/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal'
P_REPO="$VSP/2_Project_Files"
CLAR="$VSP/1_Project_Definition/CLARIFICATIONS.md"
REPORTS="$QA_DIR/projects/vision/reports"
G12_DIR="$REPORTS/2026-09-28-vision-gate12-three-targets"
G12_REPORT="$G12_DIR/report.md"
G12_TOOLS="$G12_DIR/evidence/tools"
G12_FLOOR="$G12_TOOLS/qa-floorcount.py"
REPORT="$REPORTS/2026-09-28-vision-gate13-vsp74r2-vsp75/report.md"
ROUTE_NAME='QA/Vision-gate13'
NEG_SEATS='59108 20317 91381'   # Tuesday (%0), NexusAI P (%22), QA/NexusAI-batch5b (%36) — re-read 11:31:58 AEST (Vision seat 7956 / %40 exited)
# Gated anchors (not heads).
ANCHOR_MAIN='e59232e1983cd9424b749cd5fea518838763f90f'     # main now: 609e967 + VSP-69 (gate 12 GO) merged
ANCHOR_G12MAIN='609e967d6b03ff77dcbd692ee6e4434a5027e70b'  # main at gate 12; VSP74's base
ANCHOR_OLDMAIN='0d992e09ebe0830dbe414aa73ca9a17a1be6c480'  # main before gate 11's merges
ANCHOR_OLDMAIN_P='b5c3e8d244822df180c34007a44a25f44eb64387' # its single parent
ANCHOR_R70='12138cb46acb8201999ace84cb8f9357ee63aac7'      # VSP-70's refactor (on main)
G12_H74='a1794ad5111b640fd3041e4f46154c577f559baf'         # gate 12 NO-GO head (VSP74-G12-F1) = 4813e5f's parent = the F1 positive control
G12_H75='41c4a664a9d1698150424337ccc9d946d221f12b'         # gate 12 GO head of VSP75
G12_H69='e79682a3ee9ada9602a08c59a2d4d3e132b9b638'         # gate 12 GO head of VSP69 (merged as e59232e)
R69_FIX='3ede8ed7e67e686261a260e914bb84600de84a12'         # VSP-69 fix (on main now)
M75_FWD74='4843aedf7b50bba62839769090615c1ba6d61f4f'       # merge 41c4a66 + 4813e5f
R75_PRE2='e34add45d313834be3df961679e4f75757104183'        # cascade-matrix positive control (gate 12)
R74_PRE2='987178cbdabe3f0d6d893086d8cc658ec2ab9392'
# Gate 12's exact non-merge chains (over 609e967), carried; + 4813e5f.
CHAIN74_G12="d2531ea9322f2561c50b2005a8ff7aefe42fd395 bf5bdc06c07b59bf956ae7d40e436582ff1fe24d b7bc78bc7d23fb7680db3bd13b4414bfa25e0ca6 011becb06ec02f8bdaa0bbff8a9ef811d723ab0c 57ecad64dacef5bce3d8342fb883ce532587eceb f62917f605187146f72d55e7d5d2b777c19cca91 a1794ad5111b640fd3041e4f46154c577f559baf"
CHAIN75_G12="$CHAIN74_G12 cad19ab7c50f40047c82473c42e6f5c232814406 0d7a2fb4514a682c0cb3a69593faf9ff3238a93b e64d54ed2e748e0acd03db7f88d9ab68de4132c9 f3925826e438de1b69b1fe3d2a9b32ca49614286 69157de61521769ba893270af7773967b011e273 0d1376cdf5e5e918490af22816a24e4f5042d5e0 41c4a664a9d1698150424337ccc9d946d221f12b"
H74_EXPECT='4813e5f5c949d638d8aa82ce282b778d55dedced'
CHAIN74="$CHAIN74_G12 $H74_EXPECT"
CHAIN75="$CHAIN75_G12 $H74_EXPECT"
BEHIND74="$R69_FIX $G12_H69 $ANCHOR_MAIN"                  # VSP74 is behind main by exactly the VSP-69 chain
DISPATCH_BLOB='7a67be98580c1bf7f2c6f18f9988e6cd905ca1c8'   # server/reminders/dispatcher.js on main e59232e (VSP-69)
DBBACKUP_TEST_68='4fb902e'                                  # VSP-68's server/dbBackup.test.js blob (prefix) = main's
# Every file any target changes: main may move only in files outside this set.
DELTA_FILES='BACKLOG.md server/dbRestore.js server/dbRestore.plan.test.js test/db/restore-incomplete.test.js server/backupTables.js server/dbBackup.js server/dbBackup.test.js test/db/backup-coverage.test.js test/db/backup-lazy-absent.test.js test/db/restore-old-backup.test.js server/reminders/dispatcher.js test/db/dispatch-once.test.js'

SUBJECT_STEM='[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 13'
QUESTION_SUBJ='[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>'
ANSWER_PREFIX='[Tuesday -> QA/Vision-gate13] ANSWER'

p() { git --no-optional-locks -C "$P_REPO" "$@"; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE gate (Vision gate 13) on Datasec/Vision_Sales_Portal: a NARROW RE-GATE with TWO targets and TWO verdicts, each GO or NO-GO, plus one merge line, in the SALES PORTAL repo. Portal main is e59232e (gate 12's 609e967 + VSP-69, which gate 12 GO'd). Gate 12 went NO-GO on VSP-74 a1794ad for VSP74-G12-F1 (the restore closure compared FK endpoints as quoted / schema-qualified regclass text against bare public names) and GO on VSP-75 41c4a66 on its own scope. You gate VSP-74 ROUND 2 OF 2 at 4813e5f and VSP-75's NEW HEAD at 110bb03 (41c4a66 + VSP-74 round 2 merged forward + main e59232e merged in).

READ YOUR COMMISSION FIRST, whole: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-28_vision-gate13-vsp74r2-vsp75.md
Then read the charter it names, the Vision CLARIFICATIONS (C-01..C-07; C-07 records the settled shape of this round and is Tuesday's ruling, not Kam's), the project's CLAUDE.md (/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/CLAUDE.md; its deploy commands are not for you), the builder's READY mails under test (/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-28_vision-vsp74-r4-READY-mail.txt and -vsp75-r4-READY-mail.txt beside it), and gate 12's report /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-28-vision-gate12-three-targets (report.md: VERDICTS, VERBATIM OPERATOR STRINGS, N1.3, N1.6, N1.10, N2.9, N4, N5, FINDINGS INDEX, THE QUEUE, NOT TESTED, self-findings; evidence/tools/ holds the instruments you copy). Every builder statement is a CLAIM, never evidence. RE-DERIVE every red, every mutant and every suite set yourself. Verify every PRIOR WORK claim against git history and gate 12's evidence, never against the brief.

THE CLASS CAP. VSP74 is ROUND 2 OF 2 of its class: a NO-GO of VSP-74 goes to Kam, not to another round. A failure rooted in VSP-74's code (restorePlan, liveTables, the closure, clearTables) counts against VSP-74's class whichever head you measure it on. A failure in VSP-75's own scope (the backup side, the absent rule, FIX 1, FIX 2) would be VSP-75's first NO-GO.

THE TARGETS.
  VSP74 (TIER 1, ROUND 2 OF 2) = Jira VSP-74 = F-B, at 4813e5f. It fixes ONLY VSP74-G12-F1: live tables now come from pg_class in every user schema with their OID, FK edges are matched by OID, a non-public table with rows whose FK chain reaches a restored table is outside (refused by default, kept with its parents under --allow-incomplete), identifiers quoted in the row check. F2, F3 and P1 are ticketed (VSP-81), NOT built: observations only if seen, never graded.
  VSP75 (TIER 1) = Jira VSP-75 = F-A, NEW HEAD at 110bb03. Its backup-side blobs are byte-identical to the GO'd 41c4a66; its dbRestore.js is VSP-74's OID plan with VSP-75's absent rule re-applied in the merge. This is the head that will actually merge (it contains VSP-74 and main).
WHY NARROW: VSP-75 was GO on its own scope at gate 12; do not re-derive all of it. Run exactly what the brief lists.

WHAT THE BRIEF REQUIRES, in short (the brief is the authority):
(1) F1 CLOSED on BOTH heads: gate 12's closure cells on YOUR instrument, with a1794ad and 41c4a66 as the positive controls that must lose rows: the mixed-case "QA_Outside" table with CASCADE and with SET NULL to leads (refused by default; with the flag kept with leads, rows and lead_id unchanged), another-schema table with a CASCADE key to public.leads (refused), and the lower-case control still kept. Then the CLASS-HUNT: a name with a space, a dot, a reserved word, a double quote; a table in a schema on the search_path vs not; search_path shadowing of a restored table's name; a table that INHERITS a restored table; a self-reference; a multi-column FK; ON DELETE SET DEFAULT; reach through a public outside table and through another schema; the label collision of a public "x.y" with schema x table y; a role without USAGE on the other schema if cheap; a partitioned table if cheap. Any lost or changed row of a table the plan must keep is a FAIL. The READY's seven mutants on 4813e5f, M2 and M8 on 110bb03, and your own; the unit stub rewrite checked for papering over.
(2) NO REGRESSION: the gate-12 cascade matrix (on 110bb03 with a 20-table backup and on 4813e5f alone, with e34add4 as the positive control), refusal changes nothing, the N2.9 deploy-time arms line by line against gate 12's measured table (plus the TZ arms), the N4 required cell with the fault log and the 4fb902e positive control, SUITES AS SETS, NOT COUNTS vs main e59232e (0 lost at 110bb03), the FIX 2 watcher beside every test:db (never touch salesportal_test_lazy; always set TEST_DATABASE_URL), merged coverage run locally (label it NOT CI), and the Node 20 leg exactly as the NODE20-LEG line in the brief says (DOCKER-PULL-NEVER).
(3) F2 / F3 / P1: observations only.
(4) The merge: from YOUR OWN object dir, whether main x 110bb03 is a fast-forward; the code files equal e59232e + VSP-75's blobs; BACKLOG carries every line of both sides.
CI is UNMEASURED: this project's gh is not authenticated and you must not use gh; never claim CI; name CI's Node 22 coverage gate and its e2e:pro step as the first reads at merge. Every red-proof: fresh tree per arm, asserted edits, node --check rc quoted; a red from a mutant that does not parse is VOID. The brief's TUESDAY'S RULINGS say how to grade a row lost outside the plan's keep set through a non-FK path.

LOCAL POSTGRES ONLY. PRODUCTION IS LIVE for this project. NEVER the live portal (datasec-sales-portal.azurewebsites.net, datasec-sales-portal-rg, its Postgres datasec-sales-db.postgres.database.azure.com, its key vault): no request, no DB connection, not even a GET. No az of any kind, no deploy, no app-setting change. Never open a real backup, a production dump or anything under the project's 4_Credentials: every backup JSON you use is built by the product's own code from YOUR seeded database. Real sends are OFF: Azure Blob Storage and ACS are replaced by YOUR recorders; ntfy goes only to YOUR loopback recorder. restoreData, restorePlan and clearTables read and DELETE: print the connected database name before every call and abort if it is not one you created. Never set AZURE_BACKUP_CONN_STR. Schemas, search_path settings, inheritance children, partitions and any vsp_qa_g13_* role exist only inside your own databases.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT from the object store (git archive into a fresh mktemp -d under projects/vision/work-g13/). Each tree is EXCLUSIVE to this gate and to one purpose; never touch work/ or work-g2 .. work-g12. Copy gate 12's tools into YOUR evidence folder and re-point them (they hard-code work-g12 and ENFORCE vsp_qa_g12_); never run from, edit or write into gate 1-12's copies. Dependencies: npm ci --offline --ignore-scripts only, then prove node_modules/.package-lock.json against the lockfile entry by entry (lockcmp.py AND lockwalk.py). Never npm install, never npm audit, never npx anything not already in the tree. In the repo use ONLY read verbs (show, log, diff, ls-remote, rev-parse, ls-tree, cat-file, grep, merge-base, archive); never fetch, pull, checkout, switch, worktree, commit, stash, reset, clean or gc. Run git merge-tree --write-tree only from the gate's OWN object dir (GIT_OBJECT_DIRECTORY = your own mktemp -d, alternates = the repo's objects), or skip it and say so. Findings-only: no writes in the portal repo, none inside Vision_Sales_Portal, none in gate 1-12's report folders or trees. Never rm: quarantine. Run every loop and every git show <sha>:<path> under bash. CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY: a control derived from the run it validates is not a control.

FLOOR DISCIPLINE. Vision has no jest lock; never borrow NexusAI's. Never use ports 4848, 8080 or 47787, nor 127.0.0.1:49162 / 49164 / 49166; take every port from the kernel and bind 127.0.0.1. Never start the portal's own entry point (it binds all interfaces); use the real createApp() and initDb() in your harness. Postgres is the local container on 127.0.0.1:5433, and ONLY databases you create: vsp_qa_g13_<epoch> and vsp_qa_g13_<epoch>_test (the test name MUST end in _test); never salesportal, salesportal_test or salesportal_test_lazy (the Vision seat uses them and may be relaunched at any time), any vsp_qa_g1..g12 database, the builder's vsp_bf1_*, vsp_g12r2_* or vsp_fix* databases, or any vsp71_* / vsp73_* database you did not cause. Roles are cluster-global: create one only inside a transaction you roll back, or name it vsp_qa_g13_* and list it; earlier gates' roles are not yours. Never ALTER SYSTEM, never ALTER DATABASE or ALTER ROLE on anything you did not create. The module's default URL is the builder's dev database, so give every product process YOUR DATABASE_URL and TEST_DATABASE_URL explicitly and print the database each one reached. Release every lock and direct session you open in a finally. No docker command at all, except the Node 20 exception under the NODE20-LEG line. Every product process runs under env -i with an explicit allowlist, NODE_ENV never production. Never set AGENTMAIL_API_KEY or AGENTMAIL_INBOX in a product process, nor any real ACS_* or MAIL_SENDER, AZURE_BACKUP_CONN_STR, TABLES_CONNECTION_STRING, SALES_COPY_EMAIL, a real NTFY_TOPIC, LEAD_BOT_API_KEY or WEBSITE_SITE_NAME; print each product process's env KEY NAMES and assert none is forbidden. NTFY_SERVER=http://ntfy.invalid except your loopback recorder; never contact ntfy.sh; stub fetch to throw on any other URL. Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid, with the brief's negative-control seats classifying FOREIGN in the same run. A zero is reportable only beside an ATTACHED control that fired in the same window. Other gates and seats are live on this box: record the load average beside every timing number; a latency result with no load figure is not a measurement.
DEADLINE AND HEARTBEAT: every step has a written DEADLINE built into your runner (there is no timeout binary here) and releases its servers, proxies, recorders, sessions, locks, roles and children in a finally. Log a HEARTBEAT line at least every 2 minutes; a step with no heartbeat for 5 minutes is aborted and reported, never waited on. Deadlines: one restore cell 120 s; a child-process cell 30 s; one test:db file 180 s; a whole test:db run 420 s; one Node 20 container 420 s. Nothing above 420 s.

QUESTIONS: your routing name is QA/Vision-gate13. If you must ask, mail tuesday-agent@agentmail.to with the subject "[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>" and proceed on the safest reading without waiting. Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/Vision-gate13] ANSWER"; read it with your verdict key. Never wednesday-agent@. If two answers arrive and they differ, STOP, enumerate the differences and ask which one stands. If a response is cut off by a safety check, record it and continue with the next item; this is authorised defensive QA of Datasec's own product on loopback. Record every question, reading and answer in the report.

Write your report to: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-28-vision-gate13-vsp74r2-vsp75/report.md

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with a subject beginning exactly:
[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 13: VSP74 r2 @ <sha7> <GO | NO-GO> · VSP75 @ <sha7> <GO | NO-GO> · merge <FAST-FORWARD | NOT-FF>
(each sha7 is the pinned head from the verified table below). Lead the body with two sentences, one per target, as the brief's section 14 words them, then one line on the merge and one line on the class cap (VSP-74 ROUND 2 OF 2: a NO-GO goes to Kam). You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no credentials directory of its own. Use it only in your own mail calls, with a client timeout. Never put the key or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice.

Report every pinned head and main as three timestamped readings (start / mid / end), with the branch name beside each. Include the verbatim operator strings the brief lists: the refusal text for an outside table in another schema and for a mixed-case one, the --allow-incomplete warning lines for each, any new string the class-hunt produced, and SELECT version().

Rule 2 stands: what you did NOT test is first-class output. Write a NOT TESTED section that covers at least CI (UNMEASURED), production's catalog, schemas, search_path and roles, the restore CLI end to end against Azure Blob Storage, real Azure Blob Storage, ACS and ntfy, Node 22, the container image, e2e:pro, and every class-hunt shape you did not run. Label every action recommendation MEASURED AT RUNTIME, PROBED or READ ONLY.
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
TARGETS='VSP74 VSP75'
EXPECT_IDS="MAIN-P $TARGETS"
for ID in $EXPECT_IDS; do
  N="$(printf '%s\n' "$PIN" | awk -F'\t' -v id="$ID" '$1==id' | wc -l | tr -d ' ')"
  [ "$N" = "1" ] || { echo "REFUSING: PIN table must carry exactly one row '$ID' (found $N)" >&2; exit 40; }
done
[ "$(printf '%s\n' "$PIN" | wc -l | tr -d ' ')" = "3" ] || { echo "REFUSING: PIN table carries rows beyond the three expected ($EXPECT_IDS)" >&2; exit 40; }
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
  VSP74) echo 'fix/vsp-74-restore-refuses-incomplete-2026-09-28' ;;
  VSP75) echo 'fix/vsp-75-backup-all-tables-2026-09-28' ;;
esac; }
base_of() { case "$1" in VSP74) echo "$ANCHOR_G12MAIN" ;; VSP75) echo "$ANCHOR_MAIN" ;; esac; }
for ID in $TARGETS; do
  [ "$(fld "$ID" 3)" = "$(branch_of "$ID")" ] || { echo "REFUSING: row $ID branch is '$(fld "$ID" 3)', the brief's target is $(branch_of "$ID") — re-brief" >&2; exit 40; }
  is40 "$(fld "$ID" 5)" || { echo "REFUSING: PIN row $ID base is not a 40-hex sha" >&2; exit 40; }
  printf '%s' "$(fld "$ID" 6)" | grep -Eq '^[1-9][0-9]*$' || { echo "REFUSING: PIN row $ID commits '$(fld "$ID" 6)' is not a positive integer" >&2; exit 40; }
done
MAINH="$(fld MAIN-P 4)"
H74="$(fld VSP74 4)"; H75="$(fld VSP75 4)"
[ "$H74" = "$H74_EXPECT" ] || { echo "REFUSING: VSP74's PIN head ${H74:0:7} is not 4813e5f — this launcher's chains are pinned to round 2 of 2; re-brief" >&2; exit 40; }

# 9a — the five gate-11 heads come from the brief's GATE11-MERGED line.
G11M="$(sed -n 's/^GATE11-MERGED: //p' "$BRIEF" | head -1)"
[ "$(printf '%s\n' $G11M | grep -Ec '^[0-9a-f]{40}$')" = "5" ] || { echo "REFUSING: the brief's GATE11-MERGED line does not carry exactly five 40-hex shas" >&2; exit 9; }

# 6 — every sha the guards use is a commit in the local object store (this launcher never fetches).
for S in "$MAINH" "$H74" "$H75" "$ANCHOR_MAIN" "$ANCHOR_G12MAIN" "$ANCHOR_OLDMAIN" "$ANCHOR_R70" "$G12_H74" "$G12_H75" "$G12_H69" "$R69_FIX" \
         "$M75_FWD74" "$R75_PRE2" "$R74_PRE2" $G11M $CHAIN75; do
  T="$(p cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in the portal repo (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 9m — MAIN: e59232e, or a descendant of it whose diff from e59232e touches none of the targets' files.
main_ok() {   # $1 = sha; prints the offending files and returns 1 if it moved in a delta file
  p merge-base --is-ancestor "$ANCHOR_MAIN" "$1" 2>/dev/null || { echo "(not a descendant of e59232e)"; return 1; }
  [ "$1" = "$ANCHOR_MAIN" ] && return 0
  local HIT; HIT="$(p diff --name-only "$ANCHOR_MAIN" "$1" 2>/dev/null | grep -xF -f <(printf '%s\n' $DELTA_FILES))"
  [ -z "$HIT" ] || { printf '%s\n' "$HIT"; return 1; }
  return 0
}
OUT="$(main_ok "$MAINH")" || { echo "REFUSING: the pinned MAIN ${MAINH:0:7} is not e59232e or a descendant that leaves the targets' files alone: $OUT — re-brief" >&2; exit 9; }
STALE=''
[ "$MAINH" = "$ANCHOR_MAIN" ] || { STALE=' (main pinned past e59232e; the merge is no longer a pure fast-forward: the gate re-derives it)'; echo "NOTE: pinned MAIN ${MAINH:0:7} is a descendant of e59232e touching none of the delta files" >&2; }

# 7 / 8 — each target: base as briefed, ancestor AND merge-base with MAIN, not on main, exact count; VSP75 0 behind; VSP74 behind by the VSP-69 chain only.
for ID in $TARGETS; do
  H="$(fld "$ID" 4)"; BASE="$(fld "$ID" 5)"; N="$(fld "$ID" 6)"; H7="${H:0:7}"
  [ "$BASE" = "$(base_of "$ID")" ] || { echo "REFUSING: row $ID base ${BASE:0:7} is not $(base_of "$ID" | cut -c1-7) — re-brief" >&2; exit 7; }
  p merge-base --is-ancestor "$BASE" "$H" 2>/dev/null || { echo "REFUSING: $ID base ${BASE:0:7} is not an ancestor of $H7" >&2; exit 7; }
  [ "$(p merge-base "$H" "$MAINH" 2>/dev/null)" = "$BASE" ] || { echo "REFUSING: $ID merge-base(head, MAIN) is not its base ${BASE:0:7}" >&2; exit 7; }
  p merge-base --is-ancestor "$H" "$MAINH" 2>/dev/null \
    && { echo "REFUSING: $ID $H7 is ALREADY ON MAIN ${MAINH:0:7} — the brief says it is not; re-brief" >&2; exit 7; }
  GOTN="$(p rev-list --count "${BASE}..${H}" 2>/dev/null)"
  [ "$GOTN" = "$N" ] || { echo "REFUSING: $ID $H7 has $GOTN commits over its base, the table says $N" >&2; p log --format='%h %p %s' "${BASE}..${H}" >&2; exit 8; }
done
[ "$(p rev-list --count "${H75}..${ANCHOR_MAIN}" 2>/dev/null)" = "0" ] || { echo "REFUSING: VSP75 ${H75:0:7} is behind e59232e — main was not merged in" >&2; exit 7; }
[ "$(p rev-list "${H74}..${ANCHOR_MAIN}" 2>/dev/null | sort)" = "$(printf '%s\n' $BEHIND74 | sort)" ] \
  || { echo "REFUSING: VSP74 ${H74:0:7} is behind e59232e by something other than exactly the VSP-69 chain (3ede8ed, e79682a, e59232e)" >&2; p rev-list "${H74}..${ANCHOR_MAIN}" >&2; exit 7; }

# 9 — gated anchors, never-rebased, exact chains, forward merges only, the stack.
[ "$(p log -1 --format='%P' "$ANCHOR_OLDMAIN" 2>/dev/null)" = "$ANCHOR_OLDMAIN_P" ] || { echo "REFUSING: 0d992e0's parent is not b5c3e8d — re-brief" >&2; exit 9; }
for S in "$ANCHOR_OLDMAIN" $G11M "$ANCHOR_R70" "$ANCHOR_G12MAIN" "$G12_H69"; do
  p merge-base --is-ancestor "$S" "$MAINH" 2>/dev/null || { echo "REFUSING: anchor ${S:0:7} (old main / gate-11 head / 12138cb / 609e967 / VSP-69 e79682a) is not on main ${MAINH:0:7} — re-brief" >&2; exit 9; }
done
[ "$(p log -1 --format='%P' "$ANCHOR_MAIN")" = "$ANCHOR_G12MAIN $G12_H69" ] || { echo "REFUSING: e59232e is not the merge 609e967 + e79682a (VSP-69's gate-12 GO head)" >&2; exit 9; }
[ "$(p log -1 --format='%P' "$H74")" = "$G12_H74" ] || { echo "REFUSING: VSP74 ${H74:0:7}'s single parent is not a1794ad (gate 12's NO-GO head) — rebased or rebuilt" >&2; exit 9; }
[ "$(p log -1 --format='%P' "$M75_FWD74")" = "$G12_H75 $H74" ] || { echo "REFUSING: 4843aed is not the merge 41c4a66 + 4813e5f" >&2; exit 9; }
[ "$(p log -1 --format='%P' "$H75")" = "$M75_FWD74 $ANCHOR_MAIN" ] || { echo "REFUSING: VSP75 ${H75:0:7} is not the merge 4843aed + e59232e — re-brief" >&2; exit 9; }
for S in "$G12_H75" "$H74" "$G12_H74" "$R74_PRE2" "$R75_PRE2" "$ANCHOR_MAIN"; do
  p merge-base --is-ancestor "$S" "$H75" 2>/dev/null || { echo "REFUSING: ${S:0:7} is not contained in VSP75 ${H75:0:7}" >&2; exit 9; }
done
nonmerge() { p rev-list --no-merges "${1}..${2}" 2>/dev/null | sort; }
merges()   { p rev-list --merges "${1}..${2}" 2>/dev/null; }
chain_of() { case "$1" in VSP74) printf '%s\n' $CHAIN74 ;; VSP75) printf '%s\n' $CHAIN75 ;; esac | sort; }
for ID in $TARGETS; do
  H="$(fld "$ID" 4)"; BASE="$(fld "$ID" 5)"
  [ "$(nonmerge "$BASE" "$H")" = "$(chain_of "$ID")" ] || { echo "REFUSING: $ID's non-merge commits over ${BASE:0:7} are not exactly the pinned chain. Got:" >&2; nonmerge "$BASE" "$H" >&2; exit 9; }
  for M in $(merges "$BASE" "$H"); do
    PARS="$(p log -1 --format='%P' "$M")"
    [ "$(printf '%s\n' $PARS | wc -l | tr -d ' ')" = "2" ] || { echo "REFUSING: $ID merge ${M:0:7} is not a two-parent merge" >&2; exit 9; }
    P2="$(printf '%s\n' $PARS | sed -n 2p)"
    if ! p merge-base --is-ancestor "$P2" "$MAINH" 2>/dev/null && ! { [ "$ID" = "VSP75" ] && p merge-base --is-ancestor "$P2" "$H74" 2>/dev/null; }; then
      echo "REFUSING: $ID merge ${M:0:7} merges ${P2:0:7}, which is neither on main nor (for VSP75) on VSP74 — not a forward merge" >&2; exit 9
    fi
  done
done
[ "$(merges "$ANCHOR_G12MAIN" "$H74" | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: VSP74 carries other than one merge (987178c) over 609e967" >&2; exit 9; }
[ "$(merges "$ANCHOR_MAIN" "$H75" | wc -l | tr -d ' ')" = "8" ] || { echo "REFUSING: VSP75 carries other than eight merges over e59232e" >&2; exit 9; }

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
    ORIGIN_MAIN_NOTE="origin main is now ${NOW:0:7}, a descendant of the pinned ${H:0:7} touching none of the delta files (NOTE; the merge is no longer a pure fast-forward)"
    echo "NOTE: $ORIGIN_MAIN_NOTE" >&2
    continue
  fi
  echo "REFUSING: row $ID: $H is not at refs/heads/$BR on origin — that head moved or was never pushed; re-pin" >&2; printf '%s\n' "${L:-<nothing>}" >&2; exit 18
done
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — exact file sets.
fileset() { case "$1" in
  VSP74) printf '%s\n' BACKLOG.md server/dbRestore.js server/dbRestore.plan.test.js test/db/restore-incomplete.test.js ;;
  VSP75) printf '%s\n' BACKLOG.md server/backupTables.js server/dbBackup.js server/dbBackup.test.js server/dbRestore.js server/dbRestore.plan.test.js \
                       test/db/backup-coverage.test.js test/db/backup-lazy-absent.test.js test/db/restore-incomplete.test.js test/db/restore-old-backup.test.js ;;
esac; }
for ID in $TARGETS; do
  H="$(fld "$ID" 4)"; BASE="$(fld "$ID" 5)"
  GOT="$(p diff --name-only "$BASE" "$H" 2>/dev/null | sort)"
  [ "$GOT" = "$(fileset "$ID" | sort)" ] || { echo "REFUSING: $ID ${H:0:7}'s delta over its base is not exactly the briefed file set. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }
done
[ "$(p diff --name-only "$G12_H74" "$H74" 2>/dev/null | sort | tr '\n' ' ')" = "server/dbRestore.js server/dbRestore.plan.test.js test/db/restore-incomplete.test.js " ] \
  || { echo "REFUSING: round 2 (a1794ad..4813e5f) touches other than dbRestore.js, its unit file and restore-incomplete.test.js — the round claims G12-F1 only" >&2; exit 22; }

# 74 — per-target content, read from the pinned shas (never a checkout).
has() { p show "${1}:${2}" 2>/dev/null | grep -qF -- "$3"; }   # sha path fixed-string
must() { has "$1" "$2" "$3" || { echo "REFUSING: ${1:0:7}:$2 lacks '$3' — the brief gates different code; re-brief" >&2; exit 74; }; }
mustnot() { has "$1" "$2" "$3" && { echo "REFUSING: ${1:0:7}:$2 still carries '$3' — the brief's reading is wrong; re-brief" >&2; exit 74; }; return 0; }
ntests() { p show "${1}:${2}" 2>/dev/null | grep -c '^test('; }
wantn() { [ "$(ntests "$1" "$2")" = "$3" ] || { echo "REFUSING: ${1:0:7}:$2 carries $(ntests "$1" "$2") test( cells, the brief says $3" >&2; exit 74; }; }
blob() { p rev-parse "${1}:${2}" 2>/dev/null; }
# The F1 positive control really has the defect the round fixes.
must "$G12_H74" server/dbRestore.js 'conrelid::regclass::text'
must "$G12_H75" server/dbRestore.js 'conrelid::regclass::text'
# VSP-74 round 2 on BOTH heads: the OID plan present, the regclass/pg_tables form gone; the rest of round 2 of gate 12 unchanged.
for H in "$H74" "$H75"; do
  must "$H" server/dbRestore.js 'async function liveTables(db) {'
  must "$H" server/dbRestore.js "WHERE c.relkind IN ('r', 'p') AND NOT c.relispartition"
  must "$H" server/dbRestore.js "AND n.nspname <> 'information_schema' AND n.nspname NOT LIKE 'pg\\\\_%'"
  must "$H" server/dbRestore.js 'SELECT conrelid::text AS child, confrelid::text AS parent'
  must "$H" server/dbRestore.js "FROM pg_constraint WHERE contype = 'f' AND conrelid <> confrelid"
  must "$H" server/dbRestore.js 'const reaches = new Set(live.filter(restored).map(t => t.oid));'
  must "$H" server/dbRestore.js 'if (kept.has(child) && !kept.has(parent) && label.has(parent)) {'
  must "$H" server/dbRestore.js "label: r.schema === 'public' ? r.name : \`\${r.schema}.\${r.name}\`,"
  must "$H" server/dbRestore.js 'for (const t of RESTORE_ORDER.filter(t => !(data.tables || {})[t] && pub.has(t))) {'   # FIX 1 on the OID catalog
  mustnot "$H" server/dbRestore.js 'conrelid::regclass::text'
  mustnot "$H" server/dbRestore.js "FROM pg_tables WHERE schemaname = 'public'"
  must "$H" server/dbRestore.js 'function failedTables(data) {'
  must "$H" server/dbRestore.js "'error' in data.tables[t]"
  must "$H" server/dbRestore.js 'async function restorePlan(data, db = { query }) {'
  must "$H" server/dbRestore.js 'if (data.tables[t] && !failed.has(t)) {'
  must "$H" server/dbRestore.js 'if (plan.keep.has(t)) {'
  must "$H" server/dbRestore.js 'Nothing was changed. To restore the other tables and leave these exactly as they are, re-run with --allow-incomplete'
  must "$H" server/dbRestore.js "allowIncomplete: argv.includes('--allow-incomplete'),"
  must "$H" server/dbRestore.js 'client.release(broken);'
  must "$H" server/dbRestore.js "console.error('Error: AZURE_BACKUP_CONN_STR not set.');"
  must "$H" server/dbRestore.js 'await client.query(`DELETE FROM "${t}"`);'   # WRONG (b): the clear is still by bare quoted name
  wantn "$H" test/db/restore-incomplete.test.js 17
done
must "$H74" server/dbRestore.js 'const RESTORE_ORDER = ['          # VSP74 alone keeps the old 10-table list (MERGE COUPLING)
mustnot "$H74" server/dbRestore.js 'backupTables'
must "$H75" server/dbRestore.js "const { BACKUP_TABLES: RESTORE_ORDER, BACKUP_EXCLUDED } = require('./backupTables');"
must "$H75" server/dbRestore.js 'for (const t of absent.filter(t => pub.has(t))) {'        # VSP-75's absent rule re-applied on the OID catalog
must "$H75" server/dbRestore.js "for (const t of absent) if (!keep.has(t)) keep.set(t, 'did not exist yet when the backup ran');"
wantn "$H74" server/dbRestore.plan.test.js 10
wantn "$H75" server/dbRestore.plan.test.js 12
[ "$(blob "$H74" test/db/restore-incomplete.test.js)" = "$(blob "$H75" test/db/restore-incomplete.test.js)" ] \
  || { echo "REFUSING: restore-incomplete.test.js differs between VSP74 and VSP75 — the stack diverged" >&2; exit 74; }
for T in "test('G12-F1 control:" "test('G12-F1 (i):" "test('G12-F1 (ii):" "test('G12-F1 (iii): a table in ANOTHER schema" "test('G12-F1 (iii): with the flag"; do
  must "$H74" test/db/restore-incomplete.test.js "$T"
done
# The 12 original restore-incomplete cells are unchanged (0 deleted lines), and every earlier plan cell is kept verbatim.
[ "$(p diff --numstat "$G12_H74" "$H74" -- test/db/restore-incomplete.test.js | awk '{print $2}')" = "0" ] \
  || { echo "REFUSING: round 2 deleted or changed lines in restore-incomplete.test.js — the brief says +90/-0" >&2; exit 74; }
for PAIR in "$G12_H74|$H74" "$G12_H75|$H75"; do
  OLD="${PAIR%%|*}"; NEW="${PAIR#*|}"
  while IFS= read -r T; do
    [ -n "$T" ] || continue
    p show "${NEW}:server/dbRestore.plan.test.js" | grep -qxF -- "$T" || { echo "REFUSING: ${NEW:0:7}'s dbRestore.plan.test.js dropped or renamed the cell: $T" >&2; exit 74; }
  done <<< "$(p show "${OLD}:server/dbRestore.plan.test.js" | grep '^test(')"
done
# VSP-75's GO'd scope did not move: backup-side blobs = 41c4a66's.
for F in server/dbBackup.js server/backupTables.js server/dbBackup.test.js test/db/backup-coverage.test.js test/db/backup-lazy-absent.test.js test/db/restore-old-backup.test.js; do
  [ "$(blob "$H75" "$F")" = "$(blob "$G12_H75" "$F")" ] || { echo "REFUSING: $F at VSP75 ${H75:0:7} differs from the GO'd 41c4a66 — the re-gate would not be narrow; re-brief" >&2; exit 74; }
done
DBT_75="$(blob "$H75" server/dbBackup.test.js)"; DBT_MAIN="$(blob "$MAINH" server/dbBackup.test.js)"
case "$DBT_MAIN" in "$DBBACKUP_TEST_68"*) ;; *) echo "NOTE: main's dbBackup.test.js is ${DBT_MAIN:0:7}, not VSP-68's 4fb902e — §N2.4's pre-fix-stub control must use 4fb902e from the object store" >&2 ;; esac
[ "$DBT_75" != "$DBT_MAIN" ] || { echo "REFUSING: VSP75 did not change server/dbBackup.test.js" >&2; exit 74; }
wantn "$H75" server/dbBackup.test.js 10
wantn "$H75" test/db/restore-old-backup.test.js 2
wantn "$H75" test/db/backup-coverage.test.js 6
wantn "$H75" test/db/backup-lazy-absent.test.js 3
must "$H75" test/db/backup-lazy-absent.test.js 'const lazyDb = `${base.pathname.slice(1)}_lazy`;'
mustnot "$H75" test/db/backup-lazy-absent.test.js "lazyUrl.pathname = '/salesportal_test_lazy';"
# Main's VSP-69 files are carried unchanged into VSP75; VSP74 does not carry them (behind by the VSP-69 chain).
[ "$(blob "$MAINH" server/reminders/dispatcher.js)" = "$DISPATCH_BLOB" ] || { echo "REFUSING: main's dispatcher.js is not 7a67be9 — main moved in VSP-69's file; re-brief" >&2; exit 63; }
[ "$(blob "$H75" server/reminders/dispatcher.js)" = "$DISPATCH_BLOB" ] || { echo "REFUSING: VSP75's dispatcher.js is not main's 7a67be9" >&2; exit 63; }
[ "$(blob "$H75" test/db/dispatch-once.test.js)" = "$(blob "$MAINH" test/db/dispatch-once.test.js)" ] || { echo "REFUSING: VSP75's dispatch-once.test.js is not main's" >&2; exit 63; }
wantn "$H75" test/db/dispatch-once.test.js 5
p cat-file -e "${H74}:test/db/dispatch-once.test.js" 2>/dev/null && { echo "REFUSING: VSP74 carries dispatch-once.test.js — it should be behind main by VSP-69" >&2; exit 63; }
for T in 'npm ci --offline --ignore-scripts' 'entry by entry' 'never npm audit'; do
  grep -qiF "$T" "$BRIEF" || { echo "REFUSING: brief lacks the dependency rule '$T'" >&2; exit 63; }
  printf '%s\n' "$PROMPT" | grep -qiF -- "$T" || { echo "REFUSING: prompt lacks the dependency rule '$T'" >&2; exit 63; }
done

# 31 — the READYs are on disk, name the pinned heads in their subjects, and their NOT TESTED lines are carried verbatim; sources on disk.
for PAIR in "$READY74|READY FOR QA: VSP-74 round 2 of 2 @ ${H74:0:7}" "$READY75|READY FOR QA: VSP-75 new head @ ${H75:0:7}"; do
  RF="${PAIR%%|*}"; SUBJ="${PAIR#*|}"
  [ -s "$RF" ] || { echo "REFUSING: a READY mail is not on disk: $RF" >&2; exit 31; }
  grep -qF -- "$SUBJ" "$RF" || { echo "REFUSING: $RF's subject does not carry '$SUBJ'" >&2; exit 31; }
  # the NOT TESTED line, plus the "- " bullets directly under it (VSP-74's is a block, VSP-75's one line followed by the sign-off)
  NT="$(awk 'f&&!/^- /{exit} f{print;next} /^NOT TESTED/{f=1;print}' "$RF")"
  [ -n "$NT" ] || { echo "REFUSING: $RF carries no NOT TESTED block" >&2; exit 31; }
  while IFS= read -r L; do
    [ -n "$L" ] || continue
    grep -qxF -- "$L" "$BRIEF" || { echo "REFUSING: the brief does not carry this NOT TESTED line of $RF verbatim: $L" >&2; exit 31; }
  done <<< "$NT"
done
for T in 'VSP-74 NOT TESTED' 'VSP-75 NOT TESTED' 'F-A' 'F-B' 'ROUND 2 OF 2' 'goes to Kam' 'WHY THIS GATE IS NARROW' 'VSP74-G12-F1' 'VSP-81' \
         'C-07' 'r4-READY-mail.txt' 'lower-case control' '80.78%' '80.64%' 'deploy-time'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: the brief does not carry '$T'" >&2; exit 31; }
done
[ -s "$CLAR" ] || { echo "REFUSING: Vision CLARIFICATIONS.md absent: $CLAR" >&2; exit 31; }
for C in 'C-01.' 'C-06.' 'C-07.'; do grep -qF "**$C" "$CLAR" || { echo "REFUSING: $CLAR lacks $C" >&2; exit 31; }; done
grep -qF '4813e5f' "$CLAR" || { echo "REFUSING: CLARIFICATIONS C-07 does not name 4813e5f — the settled shape the brief quotes is not on disk" >&2; exit 31; }
grep -qF '**C-08.' "$CLAR" && echo "NOTE: Vision CLARIFICATIONS now has a C-08 — the brief says C-01..C-07; read it before launch" >&2
[ -s "$G12_REPORT" ] || { echo "REFUSING: gate 12's report is absent: $G12_REPORT" >&2; exit 31; }
grep -qF '**NO-GO** at `a1794ad' "$G12_REPORT" || { echo "REFUSING: gate 12's report does not carry VSP74's NO-GO at a1794ad" >&2; exit 31; }
grep -qF '**GO** (on VSP-75' "$G12_REPORT" || { echo "REFUSING: gate 12's report does not carry VSP75's GO" >&2; exit 31; }
grep -qF 'VSP74-G12-F1' "$G12_REPORT" || { echo "REFUSING: gate 12's report does not carry VSP74-G12-F1" >&2; exit 31; }
grep -qF "$G12_DIR" "$BRIEF" || { echo "REFUSING: the brief does not name $G12_DIR" >&2; exit 31; }
case "$PROMPT" in *"$G12_DIR"*) ;; *) echo "REFUSING: the prompt does not name $G12_DIR" >&2; exit 31 ;; esac
for H in qa-harness-g12.cjs qa-g12-db.cjs qa-g12-matrix.cjs qa-g12-one.cjs qa-g12-refusals.cjs qa-g12-n29.cjs qa-g12-lazywatch.cjs mutate-g12.py \
         qa-run.py qa-floorcount.py qa-io1-preload-fetchguard.cjs mktree-portal.sh lockcmp.py lockwalk.py specsets.py tapsets.py run-node20-g12.sh seed-g12.sql; do
  [ -s "$G12_TOOLS/$H" ] || { echo "REFUSING: gate 12's tool $H is not on disk — the brief names it" >&2; exit 31; }
  grep -qF -- "$H" "$BRIEF" || { echo "REFUSING: the brief does not name gate 12's tool $H" >&2; exit 31; }
done

# 39 — the floor instrument is on disk and named.
[ -s "$G12_FLOOR" ] || { echo "REFUSING: gate 12's floor instrument missing: $G12_FLOOR" >&2; exit 39; }
grep -qF 'qa-floorcount.py' "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument qa-floorcount.py" >&2; exit 39; }

# 10 / 17 — report path named in both; no stale report.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

# 12 — tiers declared in both, at the pinned heads.
for ID in VSP74 VSP75; do
  H7="$(fld "$ID" 4 | cut -c1-7)"
  grep -qE "^- \*\*${ID}\*\* at \`${H7}\` — \*\*TIER 1" "$BRIEF" || { echo "REFUSING: brief does not declare $ID at \`$H7\` TIER 1" >&2; exit 12; }
  case "$PROMPT" in *"$ID (TIER 1"*) ;; *) echo "REFUSING: prompt does not declare: $ID (TIER 1" >&2; exit 12 ;; esac
done

# 78 — the commission's requirements, in both.
for T in 'ROUND 2 OF 2' 'goes to Kam' 'NARROW' 'OID' 'every user schema' 'QA_Outside' 'CASCADE' 'SET NULL' 'another schema' 'lower-case control' \
         'CLASS-HUNT' 'space' 'dot' 'reserved word' 'search_path' 'shadowing' 'INHERITS' 'self-reference' 'multi-column FK' 'partitioned' 'label collision' \
         'USAGE' 'cascade matrix' 'refusal changes nothing' 'N2.9' 'N4' 'SETS, NOT COUNTS' 'e59232e' '4813e5f' '110bb03' 'a1794ad' '41c4a66' 'e34add4' \
         '4fb902e' 'NOT CI' 'Node 20' 'NODE20-LEG' 'DOCKER-PULL-NEVER' 'F2' 'F3' 'P1' 'VSP-81' 'UNMEASURED' 'e2e:pro' 'PRODUCTION IS LIVE' \
         'datasec-sales-db.postgres.database.azure.com' 'salesportal_test_lazy' 'TEST_DATABASE_URL' 'C-07' 'fast-forward' 'M8' 'node --check' 'VOID'; do
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
WORDS="merge-tree NOT%TESTED env%-i bash createApp() initDb() e59232e 4813e5f 110bb03 a1794ad 41c4a66 e34add4 work-g13 vsp_qa_g13 _test
FOREGROUND MEASURED%AT%RUNTIME PROBED READ%ONLY start%/%mid%/%end CI VOID node%--check"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## Charter' '^## RULED BY KAM, AND SETTLED' '^## PRIOR ROUND' '^PRIOR ROUND: ' 'ITS REPORT IS ON DISK AT:' '^## PIN' \
         '^## WRONG OR UNVERIFIABLE' '^## THE READYs' '^## 2a. LEGITIMATE SHAPES' '^## N1. F1 CLOSED' '^## N2. NO REGRESSION' '^## N3. F2 / F3 / P1' \
         '^## 12. The merge' '^## 13. FLOOR' "^## TUESDAY'S RULINGS AT STAMP" '^## 14. Output' '^PROVENANCE:' '^GATE11-MERGED: '; do
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
for T in 'EXCLUSIVE' 'work-g13'; do
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

# 41 — the answer route exists (Tuesday adds 'QA/Vision-gate13|tuesday-agent@agentmail.to|no' at launch). Run late on purpose: --check
#      shows every other guard first.
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || {
  echo "guards pass (40 6 9 7 8 18 22 74 63 31 39 10 17 12 78 13 14 15 20 70 19 24 53 60 61 62 64 69 75 38 45 44); route NOT added." >&2
  echo "REFUSING: no '${ROUTE_NAME}|tuesday-agent@agentmail.to|…' line in $ROUTING — answers to the gate would have no route. Add it (pattern: the QA/Vision-gate12 line) before launch." >&2; exit 41; }

# 32 — the coordinator stamps the self-check (line AND note) and every @STAMP@. LAST, so --check shows every other guard first.
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "guards pass (40 6 9 7 8 18 22 74 63 31 39 10 17 12 78 13 14 15 20 70 19 24 53 60 61 62 64 69 75 38 45 44 41); self-check NOT stamped." >&2
  echo "REFUSING: the brief still carries ${PH_STAMP} (Self-check line, or TUESDAY'S RULINGS item 1) — the coordinator re-reads end-to-end and stamps all of them before launch" >&2; exit 32
fi

PIN_BLOCK="$(printf 'PINNED HEADS — verified by the launcher at %s (cat-file; VSP74 base 609e967 and behind main by exactly the VSP-69 chain; VSP75 base e59232e, 0 behind; ancestor and merge-base with MAIN; not-already-on-main; commit counts; exact non-merge chains, forward merges only; 4813e5f<-a1794ad, 4843aed = 41c4a66 + 4813e5f, 110bb03 = 4843aed + e59232e; VSP75 backup-side blobs = 41c4a66; git ls-remote origin for every row):\n' "$PIN_TS"
  printf '%s\n' "$PIN" | awk -F'\t' '{ printf "  %-7s %-7s %-50s %s  base %s  commits %s\n", $1, $2, $3, $4, ($5=="-"?"-":substr($5,1,12)), $6 }'
  printf '  Main: pinned %s%s\n' "${MAINH:0:12}" "$STALE"
  [ -z "$ORIGIN_MAIN_NOTE" ] || printf '  %s\n' "$ORIGIN_MAIN_NOTE"
  printf '  F1 positive controls: a1794ad (VSP74 gate-12 NO-GO) and 41c4a66 (VSP75 gate-12 GO, pre-fix for F1); cascade-matrix control e34add4; section N4 control 4fb902e\n'
  printf 'NODE20-LEG, as set in the brief: %s\n' "$NODE20")"

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  printf '%s\n' "$PIN_BLOCK"
  echo "  PIN parsed, three rows, no placeholder, VSP74 = 4813e5f (40); every sha a local commit (6); main = e59232e or a delta-free descendant; GATE11-MERGED, 12138cb, 0d992e0, 609e967, e79682a on main (9)"
  echo "  bases 609e967 / e59232e, counts 9 / 23, VSP75 0 behind, VSP74 behind by the VSP-69 chain only (7 8); exact chains 8 / 15 non-merge, merges 1 / 8, round-2 parents pinned (9); origin re-read $PIN_TS (18)"
  echo "  file sets 4 / 10, round 2 touches 3 files (22); OID plan present + regclass/pg_tables absent on both heads, F1 defect present at a1794ad/41c4a66, test( 17/10 and 17/12/2/6/3/10/5, original cells kept, backup-side blobs = 41c4a66 (74)"
  echo "  dispatcher/dispatch-once = main's in VSP75, absent in VSP74 (63); READY subjects + NOT TESTED verbatim, C-07, gate 12 report + tools (31); floor (39); report absent (17); tiers (12); commission (78)"
  echo "  directive/brief/placeholders/mail/key/questions/safety (13 14 15 20 70); words + sections (19); no server path (24); standing rules (53 60 61 62 64 69 75); seats $NEG_SEATS (38); NODE20 $NODE20 (45); :5433 (44); route $ROUTE_NAME (41); stamped (32)"
  exit 0
fi

# 11 — no inherited identity: this gate needs neither az nor gh, so both point at fresh EMPTY directories.
ID_TMP="$(mktemp -d "${TMPDIR:-/tmp}/qa-vision-gate13-id.XXXXXX")" || { echo "REFUSING: cannot create the empty identity dir" >&2; exit 11; }
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
