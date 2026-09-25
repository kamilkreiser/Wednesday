#!/bin/bash
# launch_qa_vision_qq_gate8.sh — cross-project QA agent, ONE NARROW gate (Vision/QuickQuote gate 8, drafted 2026-09-25) on
# Datasec/Vision_Sales_Portal, ONE repo (QuickQuote), ONE target:
#   BCR3R4  QQ  fix/qq-bounded-browser-close-2026-09-23  ROUND 4 of the BC class (Tuesday's "BCR3 round 4", the builder's "BC round 4"):
#               the close bound 30,000 -> 90,000 ms in all FOUR places. TIER 2 through-code, TIER-1 rigour on lib/pdf.js closeBrowser.
#               Answers gate 7's BCR3-F1 (Major: the 30 s bound killed a healthy Chrome 3/3 under 8 CPU-bound workers).
# The portal is NOT in this gate. IO1F1 went GO at gate 7 and is not re-opened.
#
# THE HEADS LIVE IN ONE PLACE: the brief's PIN-HEADS table. This launcher PARSES it (carries no head of its own), refuses any
# placeholder, verifies every row against the object store and against origin by `git ls-remote` NOW, and appends the verified
# table to the agent's prompt. The only shas it carries are GATED ANCHORS: 58c9094 (gate 7's gated round-3 head, round 4's ONLY
# parent), f8dec9c (gate 6's gated round-2 head), 983f916 (the forward merge inside the branch).
#
# AUTHORITY: Tuesday's ruling of 2026-09-23 09:45 AEST (daily note 0_Brain/daily_tuesday/2026-09-23.md, GATE 7 VERDICT line):
# "BCR3 round 4 is ONE NUMBER ... gated NARROWLY". Pickup NEXT-PICKUP-TUESDAY.md:58 carries it as OWED. THE CAP: Tuesday ruled
# it NOT SPENT; gate 7's report says a fourth round needs Kam's word (C-62) and the drafter found no Kam word on record — the
# brief carries BOTH and the gate reports it, it does not rule on it. Deploys HELD for Kam; live QuickQuote is v2.33 (d4426f8).
#
# PATTERN: launch_qa_vision_qq_gate7.sh (PIN parse, anchors, file sets, content guards, --check, stamp LAST) +
# launch_qa_nexusai_package_gate_220.sh (THE PROMPT IS EMBEDDED as a heredoc — the commission allowed two files only, so there is
# no .prompt.txt; every prompt guard applies to the embedded text; the answer route must exist in inbox_routing.conf).
# CHANGES vs gate 7, each deliberate:
#   - exit 40: PIN rows are exactly MAIN-Q and BCR3R4 (one repo).
#   - exit 9:  anchors — round 4's ONLY parent is 58c9094; the head contains f8dec9c and 983f916 (parents f8dec9c + d4426f8).
#   - exit 22: exact file sets — 15 over main (gate 7's set, unchanged) AND exactly 4 over 58c9094.
#   - exit 74: round-4 content — lib/pdf.js differs from MAIN and from 58c9094 ONLY inside closeBrowser + its comment; swapping
#              90000 -> 30000 in the head's pdf.js / lib-close.mjs / lib-close.test.mjs reproduces 58c9094's code exactly; the four
#              90000s and the [90000 x4] cell are present; no 30000 default survives; package.json is 58c9094's blob with all EIGHT
#              test:print files; no non-test file but lib/pdf.js references closeBrowser; production imports renderQuotePdf only;
#              BACKLOG records the BCR2-O1 retraction.
#   - exit 57: index.html blob and toolVersion 2.33 equal at main and head; exit 63: stage3 lockfile equal at main and head.
#   - exit 31: gate 7's report / BCR3.md / CONVENTIONS.md / the harnesses the brief copies / the 90 s arm's evidence
#              (90024ms, elapsed 188.2 s) / gate 7's "FOURTH round" line / the NexusAI gate-5 narrow-gate line.
#   - exit 41: the answer route QA/Vision-gate8 exists in fleet/inbox_routing.conf (Tuesday adds it at launch).
#   - exit 38: negative-control seat 2679 (%0, Tuesday) at drafting; advisory if it has exited.
#   - exit 32: SELF-CHECK and Self-check note stamped (@STAMP@ replaced) — LAST, so --check shows every other guard first.
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/Vision-gate8' "bash '<this file>'"), NEVER nohup.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Contains a legitimate `cd` (into the QA project, at exec).
# READ-ONLY toward the repo: only cat-file, rev-parse, merge-base, log, rev-list, diff, show, grep, ls-remote.
# --check is READ-ONLY: it runs every guard and exits before any identity dir is made or any agent is started.
# Usage: launch_qa_vision_qq_gate8.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..78 a guard refused
set -u
CHECK=0
for a in "$@"; do
  case "$a" in
    --check) CHECK=1 ;;
    *) echo "unknown argument: $a" >&2; exit 2 ;;
  esac
done

# Placeholder comparand, BUILT BY CONCATENATION so a sed of the placeholder text cannot reach it.
PH_STAMP='@STA''MP@'

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-25_vision-qq-gate8-bcr3r4.md"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
VSP='/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal'
QQ_REPO="$VSP/Quoting Tool/hpas-quoting-tool"
CLAR="$VSP/1_Project_Definition/CLARIFICATIONS.md"
G7_DIR="$QA_DIR/projects/vision/reports/2026-09-23-vision-qq-gate7"
G7_REPORT="$G7_DIR/report.md"
G7_FLOOR="$G7_DIR/evidence/qa-floorcount.py"
NX_G5_REPORT="$QA_DIR/projects/nexusai/reports/2026-09-22-gate5-rd615-rd616/report.md"
C62_FILE='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md'
REPORT="$QA_DIR/projects/vision/reports/2026-09-25-vision-qq-gate8/report.md"
ROUTE_NAME='QA/Vision-gate8'
NEG_SEATS='2679'   # Tuesday (%0) — the only other claude on the box at drafting, 2026-09-25 13:12 AEST
# Gated anchors (not heads).
ANCHOR_BCR3='58c9094834ec98bb66c2a28a24f482000bb216ba'   # gate 7's gated round-3 head (NO-GO); round 4's ONLY parent
ANCHOR_BCR2='f8dec9c6b9898e05182a15ee1a0babd591a442c4'   # gate 6's gated round-2 head (GO)
FWD_MERGE='983f9168b00f8858cd2e99634f46db1193e0970e'     # the forward merge of main d4426f8 into the branch

SUBJECT_STEM='[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision/QuickQuote gate 8: BCR3 round 4 @ 703d304: '
QUESTION_SUBJ='[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>'
ANSWER_PREFIX='[Tuesday -> QA/Vision-gate8] ANSWER'

q() { git --no-optional-locks -C "$QQ_REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE NARROW gate (Vision/QuickQuote gate 8) on Datasec/Vision_Sales_Portal: one target, one repo (QuickQuote), one verdict, GO or NO-GO.

READ YOUR COMMISSION FIRST, whole: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-25_vision-qq-gate8-bcr3r4.md
Then read the charter it names, the Vision CLARIFICATIONS (C-01..C-05; none covers this target), the QuickQuote repo's own CLAUDE.md, and gate 7's report, which is the PRIOR ROUND: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-23-vision-qq-gate7 (its VERDICTS, FINDINGS INDEX, NOT TESTED, all of sections/BCR3.md, and sections/CONVENTIONS.md). Every builder statement is a CLAIM, never evidence. Verify every PRIOR WORK claim against git history and gate 7's evidence, never against the brief.

THE TARGET. BCR3R4 = ROUND 4 of the BC class (gate 4 N-C1 -> gate 5 BC -> gate 6 BCR2 -> gate 7 BCR3 -> this). Tuesday calls it "BCR3 round 4" and the builder calls it "BC round 4"; all three names mean commit 703d304 on fix/qq-bounded-browser-close-2026-09-23, whose ONLY parent is gate 7's gated head 58c9094 (which sits on the forward merge 983f916, parents f8dec9c = gate 6's gated round 2 and main d4426f8). It is NOT on QuickQuote main d4426f8 (6 ahead, 0 behind). The round changes ONE NUMBER: the close bound goes from 30,000 to 90,000 ms in all FOUR places (lib/pdf.js closeBrowser's default and NaN fallback, and test/lib-close.mjs closeBounded's default and fallback), and the "one number" cell now asserts [90000 x4]. It exists because of gate 7's BCR3-F1 (Major): under 8 CPU-bound workers on this 8-core box, the 30 s bound SIGKILLed a healthy Chrome 3 of 3, reddening BC-F2. TIER 2 through-code with TIER-1 rigour on lib/pdf.js, whose shipped default this round changes.

THIS IS A NARROW GATE. Re-measure only what round 4 changed and the cells that decide BCR3-F1, plus the full suites. Do not re-run a full round. The pattern is the NexusAI gate-5 report's section B ("A narrow re-gate suffices"); the brief gives its path and corrects the commission, which located it wrongly. In scope:
  (1) BC-F2 under the RED BAND'S LOAD, N >= 3. That is test:print beside 8 CPU-bound worker THREADS (qa-cpuload.mjs), NOT 8 concurrent print runs, with the 1-minute load reaching gate 7's red band (about 96-141) on at least two runs. The positive control is the UNMODIFIED 58c9094 tree, run the same way in the same window: it must redden BC-F2 as it did at gate 7, or your load is not the red band and a green proves nothing.
  (2) THE DISCRIMINATOR. "0 browser kills" is the wrong expectation. In gate 7's own 90 s arm (N = 1, load only 36.89 -> 60.17, 188.2 s), FIVE Chromes were killed AT the 90 s bound (fx-provenance, print-fit, logo-inset, typed-rates, phone-layout), and gate 7 never measured whether they were hangs. The expectation is 0 kills of a HEALTHY Chrome. So for every Chrome killed at 90 s under load, build a mutant tree with the bound lifted to 240,000 ms in all four places (node --check, prove the tamper landed), run it under the same load, and record whether each close returns. A close that returns between 90 s and 240 s is a healthy close that 90 s would have killed: BCR3-F1 recurring. State the headroom as numbers.
  (3) test:print completes and exits on its own, N >= 3, with all EIGHT files and 143 cells. Record the elapsed time and the load average for every run, count and attribute every kill, and report phone-layout's kill rate (gate 7's report contradicts itself on it; settle it with a rate). Use main d4426f8 as the control; it hung 2 of 3 at gate 7.
  (4) The nine forced-hang files still exit, each alone, within 90 s + margin, killing only their own Chrome (0 GoogleUpdater, 0 chrome_crashpad_handler, 0 foreign Chrome, attributed by pid ancestry anchored on your own claude pid).
  (5) The lib/pdf.js tier-1 clauses, RE-ESTABLISHED at this sha, not carried forward: renderQuotePdf, browser(), the launch options, svcInject(), module.exports, and the whole file minus the closeBrowser comment+function, all byte-unchanged vs main (gate 7: 11,258 B 617a79f87ac5d27c). Production never calls closeBrowser, with a spy proven able to fire in the same run; gate 7 recorded {"closeBrowser":0,"cdpClose":0,"disconnect":0,"childKill":0}. The emailed PDF shows 0 differing pixels vs main, text-equal, with differing bytes only inside /CreationDate and /ModDate. The PDF is NOT byte-identical, and no gate ever measured that it was.
  (6) BCR2-O1 WAS RETRACTED, by Tuesday on gate 7's measurement, and recorded in BACKLOG at 703d304: the logged close time TRACKS THE BOUND (5,018 ms at 5,000; 30,017 at 30,000; 90,024 at 90,000), with the SIGKILL line logged 16 ms BEFORE the "returned" line. Confirm the tracking ONCE at 90,000 ms: quote a kill line and a "returned after 90,0xx ms" line for the same browserPid, kill first. A "return" at 90,0xx with no preceding kill is a finding against gate 7.
  Red-proofs: parse-checked, fresh tree per arm. A RED ARM COUNTS ONLY IF THE MUTANT STILL PARSES: run node --check and quote the rc; a red from a mutant that does not parse is a VOID arm. Say that no behavioural cell sees lib/pdf.js's default; the regex cell is the only cell tied to the value (BCR3-P2).
  Suites, each with its exact command: stage3 npm test (124), npm run test:print (143), npm run test:xlsx (5), and the root pricing pack via node --test quote-engine.test.mjs (gate 7: 67). A relayed "root 353" is unverifiable at source; report it against these commands.
NOT IN SCOPE: BC-F1's stdio release, the NaN coercion, logo-inset's bound, the QA_CLOSE_MS fallback, and the portal. BCR2-F1 (Minor, ticketed) and BCR3-P1/P2/P3 (Polish): check them READ ONLY and DO NOT FAIL ON them.

THE CAP. Kam's cap rule, recorded verbatim as C-62 in the NexusAI clarifications: "A Major at round 2 of 2 is ticketed, not sent to Kam. Only a third round on the same class needs his word." Tuesday ruled that THE CAP IS NOT SPENT and that this narrow gate does not reopen it. Gate 7's report says the opposite in writing: "A further round on the BC class would be a FOURTH round, and under C-62 that needs Kam's word." The drafter found no Kam word on round 4. Say in your report that THE CAP IS NOT SPENT is Tuesday's ruling, not Kam's, and quote gate 7's line beside it; do not rule on it yourself. If you grade NO-GO, name part by part what CLOSED and would ship and what is TICKETED, and say that a third round on that class would need Kam. Recommend no further round.

RULINGS THAT ARE GATE CLAUSES: the bound is a HANG GUARD, not a latency assertion, and a false kill is worse than a slow test. Re-establish the no-production-caller claim; do not re-assert it. No product choice here is Kam's ruling: report the 90,000 ms default in a shipped module, keeping an elapsed-time bound, and toolVersion 2.33 unchanged (index.html is the same blob at main and head) as the builder's choices, and say whether each needs Kam. Live QuickQuote is v2.33 (main d4426f8), per Tuesday's notes; the gate-7 brief's v2.30 is stale. Nothing merges on your word, and deploys are HELD for Kam.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT from the object store (git archive into a fresh mktemp -d under projects/vision/work-g8/). Each tree is EXCLUSIVE to this gate and to one purpose; never touch work/ or work-g2 .. work-g7. Dependencies: npm ci --offline --ignore-scripts only, then prove node_modules/.package-lock.json against the lockfile entry by entry (lockcmp.py AND lockwalk.py; gate 7: 282/282). Never npm install, never npm audit, never npx anything not already in the tree. In the QuickQuote repo use ONLY read verbs (show, log, diff, ls-remote, rev-parse, ls-tree, cat-file, grep, merge-base, archive); never fetch, pull, checkout, switch, worktree, commit, stash, reset, clean or gc. Run git merge-tree --write-tree only from the gate's OWN object dir (GIT_OBJECT_DIRECTORY = your own mktemp -d, alternates = the repo's objects), or skip it and say so. Findings-only: no writes in either repo, none inside Vision_Sales_Portal, none in gate 1-7's report folders or trees. Never rm: quarantine. Run every loop and every git show <sha>:<path> under bash, because zsh reads $s:stage3 as a history modifier. Run node strip.js before any lone browser file. CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY: a control derived from the run it validates is not a control. Assert that every tamper landed before you read its result.

HARNESSES: copy gate 7's harnesses from its evidence folder into your own and read them before you trust them. Fix three known defects in YOUR copies, each with an asserting edit: the loaded runner gives the load 170 s against a 150 s deadline (the load must outlast your deadline); it reaps the loader with a pattern pkill that would kill another gate's loader (reap by the pid you started); and every 150 s deadline is wrong at a 90 s bound.

FLOOR DISCIPLINE. Vision has no jest lock; never borrow NexusAI's. Never use ports 4848, 8080 or 47787; take every port from the kernel and bind 127.0.0.1. No database and no docker. Every product process runs under env -i with an explicit allowlist, NODE_ENV never production. Never set AGENTMAIL_API_KEY or AGENTMAIL_INBOX in a product process (with both set, QuickQuote sends for real), nor any real ACS_* or MAIL_SENDER, TABLES_CONNECTION_STRING, SALES_COPY_EMAIL, HPAM_WORD, ADVANCED_UNLOCK_SECRET or WEBSITE_SITE_NAME; print each product process's env KEY NAMES and assert none is forbidden. NTFY_SERVER=http://ntfy.invalid; never contact ntfy.sh. EGRESS INCLUDING CHROME CHILDREN: the renderer calls three public FX APIs when currency is not USD; block them with your copy of the egress-block wrapper as PUPPETEER_EXECUTABLE_PATH, prove the block with a positive control, and run the net-log scan at the end. Record GoogleUpdater and chrome_crashpad_handler at start and end. Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid, with the brief's negative-control seat classifying FOREIGN in the same run. A zero is reportable only beside an ATTACHED control that fired in the same window. Record the load average beside every timing number; a latency result with no load figure is not a measurement.
DEADLINE AND HEARTBEAT: every browser step has a per-step DEADLINE, built into your runner (there is no timeout binary here), and kills its Chrome, server and loader in a finally. Log a HEARTBEAT line at least every 2 minutes; a step with no heartbeat for 5 minutes is aborted and reported, never waited on. Gate 7's 150 s ceiling cannot hold at a 90 s bound. The deliberate exceptions, stated wherever used: idle test:print 240 s; loaded test:print 300 s; forced-hang per file 180 s, except lib-close.test.mjs 360 s; the 240 s discriminator arm 420 s. Nothing above 420 s.

DRIVABLE SURFACE IS LOCAL ONLY. NEVER the live QuickQuote (hpas-quickquote, hpas-quickquote-rg, hpasqqacr, its log workspace; decision 18 says never query it) and NEVER the live portal (datasec-sales-portal.azurewebsites.net, datasec-sales-portal-rg, which is production). Not even a GET. No production contact of any kind; never the FX hosts or the npm registry. No az, no gh, no docker. No deploy, no merge, no mail to any human. Real sends are OFF.

QUESTIONS: your routing name is QA/Vision-gate8. If you must ask, mail tuesday-agent@agentmail.to with the subject "[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>" and proceed on the safest reading without waiting. Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/Vision-gate8] ANSWER"; read it with your verdict key. Never wednesday-agent@. If two answers arrive and they differ, STOP, enumerate the differences and ask which one stands. If a response is cut off by a safety check, record it and continue with the next item; this is authorised defensive QA of Datasec's own product on loopback. Record every question, reading and answer in the report.

Write your report to: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-25-vision-qq-gate8/report.md

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with a subject beginning exactly:
[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision/QuickQuote gate 8: BCR3 round 4 @ 703d304: <GO | NO-GO>
Lead the body with one sentence: does 90 s stop the false kill at the red band's load, and was every kill at 90 s a genuine hang? You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no credentials directory of its own. Use it only in your own mail calls, with a client timeout. Never put the key or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice.

Report the pinned head and main as three timestamped readings (start / mid / end), with the branch name beside each. Include the verbatim operator strings: the bounded-close line at 90000 ms, any TimeoutNaNWarning (expected: none), BC-F2's line under load, and the footer line and version from a real PDF at 703d304 and at main. Then one paragraph on the queue: the merge-tree result against main (expected CLEAN, equal to the head's own tree), the cells to re-run on the merged head, and CI at merge.

Rule 2 stands: what you did NOT test is first-class output. Write a NOT TESTED section that covers at least CI / Linux Chromium (a 90 s bound adds up to 13.5 minutes to a fully hanging CI run), Node 20 and Node 22, the container image, and real-world CI load. Label every action recommendation MEASURED AT RUNTIME, PROBED or READ ONLY.
PROMPT_EOF

# ---------------------------------------------------------------- GUARDS
[ -d "$QA_DIR" ]  || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]   || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -n "$PROMPT" ]  || { echo "embedded prompt is empty" >&2; exit 4; }
[ -d "$QQ_REPO/.git" ] || [ -f "$QQ_REPO/.git" ] || { echo "repo under test missing: $QQ_REPO" >&2; exit 5; }

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
EXPECT_IDS='MAIN-Q BCR3R4'
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
  [ "$(fld "$ID" 2)" = "quickquote" ] || { echo "REFUSING: PIN row $ID repo must be quickquote (the portal is not in this gate)" >&2; exit 40; }
done
[ "$(fld MAIN-Q 3)" = "main" ] || { echo "REFUSING: row MAIN-Q branch must be main" >&2; exit 40; }
[ "$(fld BCR3R4 3)" = "fix/qq-bounded-browser-close-2026-09-23" ] || { echo "REFUSING: row BCR3R4 branch is '$(fld BCR3R4 3)', the brief's target is fix/qq-bounded-browser-close-2026-09-23 — re-brief" >&2; exit 40; }
is40 "$(fld BCR3R4 5)" || { echo "REFUSING: PIN row BCR3R4 base is not a 40-hex sha" >&2; exit 40; }
printf '%s' "$(fld BCR3R4 6)" | grep -Eq '^[1-9][0-9]*$' || { echo "REFUSING: PIN row BCR3R4 commits is not a positive integer" >&2; exit 40; }
HEAD_SHA="$(fld BCR3R4 4)"; BASE="$(fld BCR3R4 5)"; NCOMMITS="$(fld BCR3R4 6)"; MAINH="$(fld MAIN-Q 4)"; HEAD7="${HEAD_SHA:0:7}"

# 6 / 7 / 8 — commits; base ancestor AND merge-base; base is MAIN (a stale base passes with a NOTE); not on main; exact count.
for S in "$MAINH" "$HEAD_SHA" "$BASE"; do
  T="$(q cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in the QuickQuote repo (got '$T') — this launcher never fetches" >&2; exit 6; }
done
STALE=''
if [ "$BASE" != "$MAINH" ]; then
  if q merge-base --is-ancestor "$BASE" "$MAINH" 2>/dev/null && [ "$(q merge-base "$HEAD_SHA" "$MAINH" 2>/dev/null)" = "$BASE" ]; then
    STALE=' BCR3R4'
    echo "NOTE: row BCR3R4 is a STALE-BASE row (base ${BASE:0:7} is an ancestor of MAIN ${MAINH:0:7}); the brief expects it NOT stale — §12 may be stale" >&2
  else
    echo "REFUSING: row BCR3R4 base ${BASE:0:7} is neither MAIN nor merge-base(head, MAIN) on MAIN — re-pin" >&2; exit 7
  fi
fi
q merge-base --is-ancestor "$BASE" "$HEAD_SHA" 2>/dev/null || { echo "REFUSING: base ${BASE:0:7} is not an ancestor of $HEAD7" >&2; exit 7; }
[ "$(q merge-base "$BASE" "$HEAD_SHA" 2>/dev/null)" = "$BASE" ] || { echo "REFUSING: merge-base(base, head) is not the base" >&2; exit 7; }
q merge-base --is-ancestor "$HEAD_SHA" "$MAINH" 2>/dev/null \
  && { echo "REFUSING: $HEAD7 is ALREADY ON MAIN ${MAINH:0:7} — the brief says it is not; re-brief" >&2; exit 7; }
GOTN="$(q rev-list --count "${BASE}..${HEAD_SHA}" 2>/dev/null)"
[ "$GOTN" = "$NCOMMITS" ] || { echo "REFUSING: $HEAD7 has $GOTN commits over its base, the table says $NCOMMITS" >&2; q log --format='%h %s' "${BASE}..${HEAD_SHA}" >&2; exit 8; }
BEHIND="$(q rev-list --count "${HEAD_SHA}..${MAINH}" 2>/dev/null)"
[ "$BEHIND" = "0" ] || echo "NOTE: $HEAD7 is $BEHIND behind main ${MAINH:0:7} — the brief says 0 behind; §12 may be stale" >&2

# 9 — gated anchors: round 4 is exactly one commit on gate 7's gated head; the branch carries gate 6's head and the forward merge.
[ "$(q log -1 --format='%P' "$HEAD_SHA" 2>/dev/null)" = "$ANCHOR_BCR3" ] \
  || { echo "REFUSING: $HEAD7's parent list is '$(q log -1 --format='%P' "$HEAD_SHA" 2>/dev/null)', not exactly gate 7's gated 58c9094 — this is not ONE round-4 commit on round 3; re-brief" >&2; exit 9; }
q merge-base --is-ancestor "$ANCHOR_BCR2" "$HEAD_SHA" 2>/dev/null \
  || { echo "REFUSING: $HEAD7 does not contain gate 6's gated head f8dec9c — not the BC class; re-brief" >&2; exit 9; }
q merge-base --is-ancestor "$FWD_MERGE" "$HEAD_SHA" 2>/dev/null \
  || { echo "REFUSING: $HEAD7 does not contain the forward merge 983f916 — the 'not stale' story is wrong; re-brief" >&2; exit 9; }
[ "$(q log -1 --format='%P' "$FWD_MERGE" 2>/dev/null)" = "$ANCHOR_BCR2 $MAINH" ] \
  || { echo "REFUSING: 983f916's parents are not f8dec9c + QuickQuote main $MAINH — re-brief" >&2; exit 9; }

# 18 — RE-PIN: both rows at origin, by ls-remote, read NOW (immediately before launch).
for ID in MAIN-Q BCR3R4; do
  BR="$(fld "$ID" 3)"; H="$(fld "$ID" 4)"
  L="$(q ls-remote origin "refs/heads/$BR" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: row $ID: $H is not at refs/heads/$BR on origin — that head moved or was never pushed; re-pin" >&2; printf '%s\n' "${L:-<nothing>}" >&2; exit 18; }
done
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — exact file sets: the branch over main (gate 7's 15, unchanged) and round 4 over 58c9094 (exactly 4).
FS_MAIN='BACKLOG.md
stage3/lib/pdf.js
stage3/package.json
stage3/test/email-collector.mjs
stage3/test/fixtures/browser-file.mjs
stage3/test/fixtures/hang-close.cjs
stage3/test/fx-provenance.mjs
stage3/test/lib-close-shared.test.mjs
stage3/test/lib-close.mjs
stage3/test/lib-close.test.mjs
stage3/test/logo-inset.mjs
stage3/test/phone-layout.mjs
stage3/test/print-fit.mjs
stage3/test/typed-rates.mjs
stage3/test/xlsx-parity.mjs'
FS_R4='BACKLOG.md
stage3/lib/pdf.js
stage3/test/lib-close.mjs
stage3/test/lib-close.test.mjs'
GOT="$(q diff --name-only "$BASE" "$HEAD_SHA" 2>/dev/null | sort)"
[ "$GOT" = "$(sorted "$FS_MAIN")" ] || { echo "REFUSING: $HEAD7's delta over main is not exactly the briefed 15 files. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }
GOT="$(q diff --name-only "$ANCHOR_BCR3" "$HEAD_SHA" 2>/dev/null | sort)"
[ "$GOT" = "$(sorted "$FS_R4")" ] || { echo "REFUSING: round 4 (58c9094..$HEAD7) is not exactly the briefed 4 files. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }

# 74 — round-4 content, read from the pinned head (never a checkout).
has() { q show "${1}:${2}" 2>/dev/null | grep -qF -- "$3"; }   # sha path fixed-string
python3 - "$(q show "${MAINH}:stage3/lib/pdf.js" 2>/dev/null)" "$(q show "${ANCHOR_BCR3}:stage3/lib/pdf.js" 2>/dev/null)" "$(q show "${HEAD_SHA}:stage3/lib/pdf.js" 2>/dev/null)" <<'PY' \
  || { echo "REFUSING: $HEAD7 changes stage3/lib/pdf.js OUTSIDE closeBrowser() + its comment (vs main or vs 58c9094) — the brief gates a closeBrowser-only change; re-brief" >&2; exit 74; }
import sys
def strip(s):
    f = s.find('async function closeBrowser(')
    if f < 0: sys.exit(1)
    c = s.rfind('/* For tests', 0, f)
    i = c if (c >= 0 and s.find('*/', c) < f) else f
    j = s.find('{', s.find(')', f)); d = 0
    for k in range(j, len(s)):
        if s[k] == '{': d += 1
        elif s[k] == '}':
            d -= 1
            if d == 0: return s[:i] + '<<closeBrowser>>' + s[k+1:]
    sys.exit(1)
m, r3, h = sys.argv[1:4]
sys.exit(0 if strip(m) == strip(h) == strip(r3) else 1)
PY
python3 - "$(q show "${ANCHOR_BCR3}:stage3/lib/pdf.js" 2>/dev/null)" "$(q show "${HEAD_SHA}:stage3/lib/pdf.js" 2>/dev/null)" \
          "$(q show "${ANCHOR_BCR3}:stage3/test/lib-close.mjs" 2>/dev/null)" "$(q show "${HEAD_SHA}:stage3/test/lib-close.mjs" 2>/dev/null)" \
          "$(q show "${ANCHOR_BCR3}:stage3/test/lib-close.test.mjs" 2>/dev/null)" "$(q show "${HEAD_SHA}:stage3/test/lib-close.test.mjs" 2>/dev/null)" <<'PY' \
  || { echo "REFUSING: swapping 90000 -> 30000 in $HEAD7's pdf.js / lib-close.mjs / lib-close.test.mjs does NOT reproduce 58c9094's code — round 4 is more than ONE NUMBER; re-brief" >&2; exit 74; }
import sys
p3, p4, l3, l4, t3, t4 = sys.argv[1:7]
def dropc(s):
    f = s.find('async function closeBrowser('); c = s.rfind('/* For tests', 0, f)
    return s[:c] + s[f:] if (f >= 0 and c >= 0) else None
nc = lambda s: '\n'.join(l for l in s.splitlines() if not l.strip().startswith('//'))
ok = (dropc(p3) is not None and dropc(p3) == dropc(p4).replace('90000', '30000') and p4.count('90000') == 2
      and nc(l3) == nc(l4.replace('90000', '30000')) and l4.count('90000') == 2
      and t3 == t4.replace('90000', '30000') and t4.count('90000') == 4)
sys.exit(0 if ok else 1)
PY
has "$HEAD_SHA" stage3/lib/pdf.js 'async function closeBrowser(ms = 90000) {' \
  || { echo "REFUSING: $HEAD7's SHIPPED lib/pdf.js closeBrowser default is not 90000 — re-brief" >&2; exit 74; }
has "$HEAD_SHA" stage3/test/lib-close.mjs 'export async function closeBounded(browser, ms = 90000) {' \
  || { echo "REFUSING: $HEAD7's test helper default is not 90000 — re-brief" >&2; exit 74; }
for F in stage3/lib/pdf.js stage3/test/lib-close.mjs; do
  has "$HEAD_SHA" "$F" 'const limit = Number.isFinite(Number(ms)) && Number(ms) > 0 ? Number(ms) : 90000;' \
    || { echo "REFUSING: $HEAD7's $F NaN-proof fallback is not 90000 — the bound is FOUR numbers; re-brief" >&2; exit 74; }
  has "$HEAD_SHA" "$F" 'ms = 30000' && { echo "REFUSING: $HEAD7's $F still carries a 30000 default" >&2; exit 74; }
  has "$HEAD_SHA" "$F" ': 30000;' && { echo "REFUSING: $HEAD7's $F still carries a 30000 fallback" >&2; exit 74; }
  has "$HEAD_SHA" "$F" 'for (const s of child.stdio || [])' \
    || { echo "REFUSING: $HEAD7's $F lost the stdio-release loop (BC-F1, gated at gate 6) — re-brief" >&2; exit 74; }
done
has "$HEAD_SHA" stage3/lib/pdf.js '90 s is a HANG guard, not a speed check' \
  || { echo "REFUSING: $HEAD7's lib/pdf.js does not record the bound as a HANG guard (Tuesday's ruling) — re-brief" >&2; exit 74; }
has "$HEAD_SHA" stage3/test/lib-close.test.mjs 'assert.deepEqual(all, [90000, 90000, 90000, 90000]' \
  || { echo "REFUSING: $HEAD7's one-number cell does not assert [90000 x4] — re-brief" >&2; exit 74; }
has "$HEAD_SHA" stage3/test/lib-close.test.mjs 'BC-F2: a bound that is not a number (node:test hands after() its TestContext) does not kill a healthy Chrome' \
  || { echo "REFUSING: $HEAD7 has no BC-F2 cell — the headline measurement has nothing to measure; re-brief" >&2; exit 74; }
has "$HEAD_SHA" stage3/test/lib-close.test.mjs 'a SLOW but healthy close (6 s, slower than the old 5 s bound) is not killed' \
  || { echo "REFUSING: $HEAD7 lost the 6 s healthy-close cell — re-brief" >&2; exit 74; }
[ "$(q rev-parse "${HEAD_SHA}:stage3/package.json" 2>/dev/null)" = "$(q rev-parse "${ANCHOR_BCR3}:stage3/package.json" 2>/dev/null)" ] \
  || { echo "REFUSING: $HEAD7's stage3/package.json differs from 58c9094's — round 4 is briefed as not touching it" >&2; exit 74; }
TP="$(q show "${HEAD_SHA}:stage3/package.json" 2>/dev/null | grep -F '"test:print":')"
for S in test/print-fit.mjs test/typed-rates.mjs test/fx-provenance.mjs test/phone-layout.mjs test/email-collector.mjs \
         test/logo-inset.mjs test/lib-close.test.mjs test/lib-close-shared.test.mjs; do
  printf '%s' "$TP" | grep -qF "$S" || { echo "REFUSING: $HEAD7's test:print line does not run $S — the EIGHT-file count the brief gates is wrong" >&2; exit 74; }
done
REFS="$(q grep -l 'closeBrowser' "$HEAD_SHA" -- stage3 2>/dev/null | sed "s#^${HEAD_SHA}:##" | grep -v '/node_modules/' | grep -v '^stage3/test/' | sort)"
[ "$REFS" = "stage3/lib/pdf.js" ] || { echo "REFUSING: at $HEAD7 a NON-test file other than lib/pdf.js references closeBrowser — a production caller the brief does not gate:" >&2; printf '%s\n' "$REFS" >&2; exit 74; }
has "$HEAD_SHA" stage3/server.js 'const { renderQuotePdf } = require("./lib/pdf");' \
  || { echo "REFUSING: at $HEAD7 the production importer no longer destructures renderQuotePdf ONLY — re-brief tier-1 clause (2)" >&2; exit 74; }
has "$HEAD_SHA" BACKLOG.md 'RETRACTED, gate 6 BCR2-O1' \
  || { echo "REFUSING: $HEAD7's BACKLOG does not record the BCR2-O1 retraction the brief relies on" >&2; exit 74; }

# 57 — version premises: index.html is the SAME blob at main and head, toolVersion 2.33.
[ -n "$(q rev-parse "${MAINH}:index.html" 2>/dev/null)" ] && [ "$(q rev-parse "${MAINH}:index.html" 2>/dev/null)" = "$(q rev-parse "${HEAD_SHA}:index.html" 2>/dev/null)" ] \
  || { echo "REFUSING: index.html differs between main and $HEAD7 — the brief says the same blob (toolVersion unchanged)" >&2; exit 57; }
has "$HEAD_SHA" index.html 'toolVersion: "2.33",' || echo "NOTE: $HEAD7 is no longer at toolVersion 2.33 — the brief's version and live-v2.33 notes may be stale" >&2

# 63 — lockfile: round 4 changes no dependency.
W="$(q rev-parse "${MAINH}:stage3/package-lock.json" 2>/dev/null)"; GOTL="$(q rev-parse "${HEAD_SHA}:stage3/package-lock.json" 2>/dev/null)"
[ -n "$W" ] && [ "$GOTL" = "$W" ] || { echo "REFUSING: stage3 lockfile at $HEAD7 is ${GOTL:0:7}, main's is ${W:0:7} — a dependency change the brief does not gate" >&2; exit 63; }
for T in 'npm ci --offline --ignore-scripts' 'entry by entry' 'never npm audit'; do
  grep -qiF "$T" "$BRIEF" || { echo "REFUSING: brief lacks the dependency rule '$T'" >&2; exit 63; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the dependency rule '$T'" >&2; exit 63 ;; esac
done

# 31 — the PRIOR ROUND and the evidence the brief sets against the builder's claims are on disk and named.
[ -s "$CLAR" ] || { echo "REFUSING: Vision CLARIFICATIONS.md absent: $CLAR" >&2; exit 31; }
for C in 'C-01.' 'C-05.'; do grep -qF "**$C" "$CLAR" || { echo "REFUSING: $CLAR lacks $C" >&2; exit 31; }; done
grep -qF '**C-06.' "$CLAR" && echo "NOTE: Vision CLARIFICATIONS now has a C-06 — the brief says C-01..C-05; read it before launch" >&2
[ -s "$G7_REPORT" ] || { echo "REFUSING: gate 7's report is absent: $G7_REPORT — it is the PRIOR ROUND" >&2; exit 31; }
for S in sections/BCR3.md sections/CONVENTIONS.md evidence/bc/disc-b.txt evidence/bc/disc-b.qalog evidence/bc/loaded.txt evidence/bc/loaded-boundary.txt; do
  [ -s "$G7_DIR/$S" ] || { echo "REFUSING: gate 7's $S is absent — the brief names it" >&2; exit 31; }
done
grep -qF 'real close() returned after 90024ms' "$G7_DIR/evidence/bc/disc-b.qalog" \
  || { echo "REFUSING: gate 7's 90 s tracking line (90024ms) is not in disc-b.qalog — the retraction confirmation has no source" >&2; exit 31; }
grep -qF 'elapsed=188.2s' "$G7_DIR/evidence/bc/disc-b.txt" \
  || { echo "REFUSING: gate 7's 90 s arm did not run 188.2 s — the brief's deadline reasoning is stale" >&2; exit 31; }
grep -qF 'would be a FOURTH round' "$G7_REPORT" \
  || { echo "REFUSING: gate 7's report no longer says a further round is a FOURTH round needing Kam — the brief's CAP section is stale" >&2; exit 31; }
grep -qF 'A narrow re-gate suffices' "$NX_G5_REPORT" 2>/dev/null \
  || { echo "REFUSING: the narrow-gate pattern line is not in $NX_G5_REPORT — the brief's pointer is wrong" >&2; exit 31; }
grep -qF 'A Major at round 2 of 2 is ticketed, not sent to Kam' "$C62_FILE" \
  || { echo "REFUSING: C-62's verbatim text is not in $C62_FILE" >&2; exit 31; }
grep -qF "$G7_DIR" "$BRIEF" || { echo "REFUSING: the brief does not name gate 7's report path (PRIOR ROUND)" >&2; exit 31; }
case "$PROMPT" in *"$G7_DIR"*) ;; *) echo "REFUSING: the prompt does not name gate 7's report path" >&2; exit 31 ;; esac
grep -qF "$NX_G5_REPORT" "$BRIEF" || { echo "REFUSING: the brief does not name the narrow-gate pattern's report path" >&2; exit 31; }
for H in qa-run.py qa-chrome-egressblock.sh qa-chrome-lock.py qa-egress-monitor.py qa-egress-posctl.mjs qa-netlog-scan.py qa-floorcount.py \
         qa-harness-floorctl.mjs lockcmp.py lockwalk.py mktree-qq.sh qa-cpuload.mjs bc-loadedrun.sh bc-loadedN.sh bc-printrun.sh \
         bc-hangrun.sh bc-observe.sh qa-bc-preload.mjs qa-bcf2-discriminate.mjs qa-harness-bc-emailed.cjs qa-lib-bc-stage3.cjs \
         qa-lib-bc-png.cjs BC-pdfcompare.sh qa-bc-identity-g7.py BC-diag2.sh; do
  [ -s "$G7_DIR/evidence/$H" ] || { echo "REFUSING: gate 7's harness $H is not on disk — the brief tells the gate to copy it" >&2; exit 31; }
done
grep -qF 'pkill -f qa-cpuload.mjs' "$G7_DIR/evidence/bc-loadedrun.sh" \
  || echo "NOTE: gate 7's bc-loadedrun.sh no longer carries the pattern pkill the brief tells the gate to fix — re-read that defect note" >&2

# 39 — the floor instrument is on disk and named.
[ -s "$G7_FLOOR" ] || { echo "REFUSING: gate 7's floor instrument missing: $G7_FLOOR" >&2; exit 39; }
grep -qF 'qa-floorcount.py' "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument qa-floorcount.py" >&2; exit 39; }

# 41 — the answer route exists (Tuesday adds 'QA/Vision-gate8|tuesday-agent@agentmail.to|no' at launch).
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || {
  echo "REFUSING: no '${ROUTE_NAME}|tuesday-agent@agentmail.to|…' line in $ROUTING — answers to the gate would have no route. Add it (pattern: the QA/Vision-gate7 line) before launch." >&2; exit 41; }

# 10 / 17 — report path named in both; no stale report.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

# 12 — tier and narrowness declared in both.
grep -qF 'BCR3R4 (bounded browser.close() round 4) is TIER 2, through-code, WITH ONE DECLARED TIER-1 TOUCH' "$BRIEF" \
  || { echo "REFUSING: brief does not declare the tier" >&2; exit 12; }
grep -qF 'THIS IS A NARROW GATE' "$BRIEF" || { echo "REFUSING: brief does not declare the gate NARROW" >&2; exit 12; }
for T in 'TIER 2 through-code with TIER-1 rigour on lib/pdf.js' 'THIS IS A NARROW GATE' 'ROUND 4 of the BC class'; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare: $T" >&2; exit 12 ;; esac
done
# 76 — the cap: C-62 verbatim, Tuesday's NOT SPENT ruling, gate 7's contrary line, and 'Tuesday's ruling, not Kam's' — both files.
for T in 'C-62' 'A Major at round 2 of 2 is ticketed, not sent to Kam' 'THE CAP IS NOT SPENT' 'a third round on that class' "is Tuesday's ruling, not Kam's" 'FOURTH round'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the cap clause: $T" >&2; exit 76; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the cap clause: $T" >&2; exit 76 ;; esac
done
# 78 — Tuesday's standing QuickQuote rulings and this round's corrections, in both.
for T in 'HANG GUARD, not a latency assertion' '{"closeBrowser":0,"cdpClose":0,"disconnect":0,"childKill":0}' '90,024' '30,017' '5,018' \
         '240,000 ms' 'red band' '58c9094' 'EIGHT' '143' 'CreationDate' 'BCR2-O1' 'BCR3-F1' 'DO NOT FAIL ON' 'v2.33'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks '$T'" >&2; exit 78; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks '$T'" >&2; exit 78 ;; esac
done
grep -qF 'establish it, do not re-assert it' "$BRIEF" || { echo "REFUSING: brief lacks the re-establish-not-re-assert ruling" >&2; exit 78; }
case "$PROMPT" in *'do not re-assert it'*) ;; *) echo "REFUSING: prompt lacks the re-establish-not-re-assert ruling" >&2; exit 78 ;; esac

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
WORDS="merge-tree NOT%TESTED env%-i EGRESS%INCLUDING%CHROME%CHILDREN bash positive%control closeBrowser renderQuotePdf phone-layout
logo-inset TimeoutNaNWarning test:print 0%differing%pixels load%average work-g8 703d304 58c9094 d4426f8 f8dec9c 983f916 CI
qa-cpuload.mjs BC-F2 node%--check VOID FOREGROUND MEASURED%AT%RUNTIME PROBED READ%ONLY 13.5%minutes quote-engine.test.mjs"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## Charter' '^## THIS IS A NARROW GATE' '^## THE CAP' '^## RULED BY KAM, AND SETTLED' '^## PRIOR ROUND' '^## PIN' \
         '^## WRONG OR UNVERIFIABLE IN THE COMMISSION' '^## 2a. LEGITIMATE SHAPES' '^## N. TARGET BCR3R4' '^## 13. FLOOR' '^## 14. Output' '^PROVENANCE:'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
grep -qF 'NOT IN SCOPE' "$BRIEF" || { echo "REFUSING: brief lacks the NOT IN SCOPE list" >&2; exit 19; }
# 24 — the prompt must DESCRIBE the app's entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qE 'stage3/server\.js|server/index\.js'; then
  echo "REFUSING: the prompt contains a literal server entry path — this agent would read as a FOREIGN SERVER to an argv-grep floor check. Describe it; do not name it." >&2; exit 24; fi

# 53 / 60 / 61 / 62 / 64 / 69 / 75 — standing rules, in both.
for T in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' '420 s'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the deadline/heartbeat rule '$T'" >&2; exit 53; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the deadline/heartbeat rule '$T'" >&2; exit 53 ;; esac
done
for T in 'node --check' 'VOID'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the parse-before-red rule '$T'" >&2; exit 60; }
done
for T in 'EXCLUSIVE' 'work-g8'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the tree-exclusivity rule '$T'" >&2; exit 61; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the tree-exclusivity rule '$T'" >&2; exit 61 ;; esac
done
for T in '4848' '8080' '47787' 'env -i' 'AGENTMAIL_API_KEY' 'AGENTMAIL_INBOX' 'no jest lock'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the Vision floor rule '$T'" >&2; exit 62; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the Vision floor rule '$T'" >&2; exit 62 ;; esac
done
for T in 'NEVER the live' 'datasec-sales-portal.azurewebsites.net' 'datasec-sales-portal-rg' 'hpas-quickquote'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not name '$T' as NEVER" >&2; exit 64; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not name '$T' as NEVER" >&2; exit 64 ;; esac
done
for T in 'ntfy.invalid' 'never contact ntfy.sh' 'FX'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the ntfy/FX egress rule '$T'" >&2; exit 69; }
  printf '%s\n' "$PROMPT" | grep -qiF -- "$T" || { echo "REFUSING: prompt lacks the ntfy/FX egress rule '$T'" >&2; exit 69; }
done
for T in 'CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY' 'PRIOR WORK' 'OWN object dir' 'no writes in either repo' 'start / mid / end' 'NOT TESTED' 'no production'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the standing line '$T'" >&2; exit 75; }
  printf '%s\n' "$PROMPT" | grep -qiF -- "$T" || { echo "REFUSING: prompt lacks the standing line '$T'" >&2; exit 75; }
done

# 38 — the brief names every negative-control seat; advisory if one is no longer running.
for P in $NEG_SEATS; do
  grep -q "\`$P\`" "$BRIEF" || { echo "REFUSING: brief does not name seat pid $P as a negative control" >&2; exit 38; }
  [ "$(ps -o comm= -p "$P" 2>/dev/null | sed 's#.*/##')" = "claude" ] || echo "NOTE: negative-control seat $P is not a running claude now — re-read the seats and update the brief's §13.4 before launch" >&2
done

# 32 — the coordinator stamps the self-check (line AND note). LAST, so --check shows every other guard first.
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "guards pass (40 6 7 8 9 18 22 74 57 63 31 39 41 10 17 12 76 78 13 14 15 20 70 19 24 53 60 61 62 64 69 75 38); self-check NOT stamped." >&2
  echo "REFUSING: the brief's SELF-CHECK line or Self-check note is unstamped — the coordinator re-reads end-to-end and stamps both before launch" >&2; exit 32
fi

PIN_BLOCK="$(printf 'PINNED HEADS — verified by the launcher at %s (cat-file, base ancestry and merge-base, not-already-on-main, commit count, gated anchors 58c9094/f8dec9c/983f916, and git ls-remote origin for both rows):\n' "$PIN_TS"
  printf '%s\n' "$PIN" | awk -F'\t' '{ printf "  %-7s %-11s %-42s %s  base %s  commits %s\n", $1, $2, $3, $4, ($5=="-"?"-":substr($5,1,12)), $6 }'
  printf '  STALE-BASE rows (forward merge owed at merge time):%s\n' "${STALE:- none}")"

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  printf '%s\n' "$PIN_BLOCK"
  echo "  PIN parsed from the brief (40); commits, base, not-on-main, count $NCOMMITS, 0 behind (6 7 8); only parent 58c9094, f8dec9c + 983f916 contained (9); origin re-read $PIN_TS (18)"
  echo "  file sets: 15 over main, 4 over 58c9094 (22); round 4 = ONE NUMBER, lib/pdf.js closeBrowser-only, four 90000s, [90000 x4] cell, BC-F2 cell, eight-file test:print, no non-test closeBrowser caller, BCR2-O1 retraction in BACKLOG (74)"
  echo "  index.html same blob (57); lockfile (63); gate 7 report + evidence + harnesses + 90024ms + 188.2 s + FOURTH-round line + narrow-gate pattern + C-62 (31); floor instrument (39); route $ROUTE_NAME (41); report absent (17)"
  echo "  tier + narrow (12); cap (76); rulings + corrections (78); directive/brief/placeholders/mail/key/questions/safety (13 14 15 20 70); words + sections (19); no server path (24); standing rules (53 60 61 62 64 69 75); seats $NEG_SEATS (38); self-check stamped (32)"
  exit 0
fi

# 11 — no inherited identity: this gate needs neither az nor gh, so both point at fresh EMPTY directories.
ID_TMP="$(mktemp -d "${TMPDIR:-/tmp}/qa-vision-gate8-id.XXXXXX")" || { echo "REFUSING: cannot create the empty identity dir" >&2; exit 11; }
mkdir -p "$ID_TMP/azure-empty" "$ID_TMP/gh-empty" || { echo "REFUSING: cannot create the empty identity dirs under $ID_TMP" >&2; exit 11; }
{ [ -z "$(ls -A "$ID_TMP/azure-empty")" ] && [ -z "$(ls -A "$ID_TMP/gh-empty")" ]; } || { echo "REFUSING: the identity dirs under $ID_TMP are not empty" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_TMP/azure-empty"
export GH_CONFIG_DIR="$ID_TMP/gh-empty"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"
# 64 (cont.) — nothing a product process could use to reach a real provider is inherited from this shell.
unset DATABASE_URL TEST_DATABASE_URL AGENTMAIL_API_KEY AGENTMAIL_INBOX ACS_CONNECTION_STRING ACS_EMAIL_CONNECTION_STRING \
      ACS_EMAIL_SENDER MAIL_SENDER TABLES_CONNECTION_STRING SESSION_SECRET HPAM_WORD ADVANCED_UNLOCK_SECRET SALES_COPY_EMAIL \
      FEEDBACK_NOTIFY_EMAIL FEEDBACK_NOTIFY_EMAILS APPROVALS_INBOX NTFY_TOPIC NTFY_SERVER LEAD_BOT_API_KEY WEBSITE_SITE_NAME \
      COORDINATOR_SECRET PORT NODE_ENV QA_CLOSE_MS QA_BC_MODE
echo "identity: AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR GH_CONFIG_DIR=$GH_CONFIG_DIR (empty) CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR" >&2

PROMPT="$PROMPT

$PIN_BLOCK"
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$PROMPT"
