#!/bin/bash
# launch_qa_vision_gate16.sh — cross-project QA agent, ONE gate (Vision gate 16; drafted 2026-10-12 14:5x-15:2x AEDT from the gate-15 launcher) on
# Datasec/Vision_Sales_Portal, QuickQuote repo: ONE TIER-1 target, ONE verdict (GO / GO WITH FINDINGS / NO GO):
#   QQCAD  feat/qq-cad-currency-2026-10-12  QuickQuote v2.34 — CAD in both currency selects, a 1.42 offline seed (C-14)   TIER 1, round 1
#
# Main is e408904 (live v2.33). QQCAD = aef649a (the change) + 9bd21c0 (BACKLOG only), 0 behind. THIS GATE PINS MAIN EXACTLY: unlike gate 15,
# a main that moved (even to a harmless descendant) REFUSES — the commission: "Pin both; the launcher must refuse if either moved."
#
# THE HEADS LIVE IN ONE PLACE: the brief's PIN-HEADS table. This launcher PARSES it, refuses any placeholder, verifies every row against the
# object store and against origin by `git ls-remote` NOW, and appends the verified table to the agent's prompt. The only shas it carries are
# GATED ANCHORS: main e408904 and its parent 986f7b8, ac74111 (gate 9's QQPURGE GO head, on main), aef649a (the change commit) and the head 9bd21c0.
#
# PRODUCTION IS LIVE for this project (hpas-quickquote / hpasqqacr; datasec-sales-portal-rg). The gate is local trees + a local Chrome with every
# FX host stubbed or blocked. No database, no Azurite, no docker. Findings only.
#
# GUARDS RE-DERIVED from launch_qa_vision_gate15.sh (kept as the template, untouched). Differences:
#   - repo: the QUICKQUOTE repo (q()), not the portal. PIN: two rows (MAIN-Q e408904, QQCAD 9bd21c0 base e408904 x2).
#   - exit 9: main pinned EXACTLY (no descendant allowance); exact chain {aef649a, 9bd21c0}; parents pinned (9bd21c0<-aef649a<-e408904<-986f7b8);
#     ac74111 (gate 9) on main.
#   - exit 18: ls-remote for BOTH rows must equal the pin; a moved main refuses (gate 15 NOTEd it).
#   - exit 22: file set 9; 9bd21c0 = BACKLOG.md only over aef649a.
#   - exit 23: REPLACED (gate 15's two-target overlap check has no meaning for one target) by THE EXACT index.html DELTA: +4/-2, the two CAD options,
#     toolVersion, fxSeeds; no style/colour in any added line (the brand clause, READ).
#   - exit 74: CAD present/absent where briefed; the three static USD labels at :1391/:1397/:1459 (base) and :1392/:1398/:1460 (head); test( counts;
#     the unchanged blobs (xlsx.js, pdf.js, store.js, mail.js, strip.js, server module, lockfile, Dockerfile, tests.yml, .dockerignore); xlsx NUMFMT and
#     footer; test:print carries fx-seed-fallback; .github holds only tests.yml.
#   - exit 31: the READY by its "feat/qq-cad-currency-2026-10-12 = <sha40>" line, its correction appended, NOT TESTED verbatim; CLARIFICATIONS C-14
#     (+ NOTE on a C-15); gate 8 + 9 reports and the instruments the brief copies.
#   - exit 82 (NEW, from launch_qa_nexusai_gate_batch20.sh): THE MODEL RULE in brief and prompt; exec pins --model claude-opus-5-5.
#   - exit 44: REPURPOSED from ":5433 listens" (no database here) to "a local Google Chrome is installed" (the browser leg's instrument).
#   - exit 38: negative-control seats re-read 14:55 AEDT (Tuesday 2388 %0, Vision builder 37670 %7, NexusAI 23252 %6).
#   - exit 41 (route) runs LAST before the stamp check (32), so --check exercises every other guard before refusing on the route.
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/Vision-gate16' "bash '<this file>'"), NEVER nohup.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Contains a legitimate `cd` (into the QA project, at exec).
# READ-ONLY toward the repo: only cat-file, rev-parse, merge-base, log, rev-list, diff, show, ls-tree, ls-remote.
# --check is READ-ONLY: it runs every guard and exits before any identity dir is made or any agent is started.
# Usage: launch_qa_vision_gate16.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..82 a guard refused
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
BRIEF="$BRIEFS/2026-10-12_vision-gate16-qq-v234-cad.md"
READY="$BRIEFS/2026-10-12_vision-qq-v234-cad-READY-mail.txt"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
VSP='/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal'
Q_REPO="$VSP/Quoting Tool/hpas-quoting-tool"
CLAR="$VSP/1_Project_Definition/CLARIFICATIONS.md"
REPORTS="$QA_DIR/projects/vision/reports"
G8_DIR="$REPORTS/2026-09-25-vision-qq-gate8"
G8_REPORT="$G8_DIR/report.md"
G8_EV="$G8_DIR/evidence"
G8_FLOOR="$G8_EV/qa-floorcount.py"
G9_DIR="$REPORTS/2026-09-27-vision-gate9-vsp65-qqpurge"
G9_REPORT="$G9_DIR/report.md"
G9_TOOLS="$G9_DIR/evidence/tools"
REPORT="$REPORTS/2026-10-12-vision-gate16-qq-v234-cad/report.md"
ROUTE_NAME='QA/Vision-gate16'
NEG_SEATS='2388 37670 23252'   # Tuesday (%0), Vision builder (%7), NexusAI (%6) — read 14:55 AEDT
CHROME_BIN='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
# Gated anchors (not heads).
ANCHOR_MAIN='e4089041d6213d460e74992ddf775a909ffe03eb'     # QuickQuote main = live v2.33 (BACKLOG: v0.6.1-tool2.33 deployed)
ANCHOR_MAINP='986f7b87069e5b48053f4854c06985edd5a8746c'    # e408904's single parent
ANCHOR_G9='ac741110fd089a1318debb3744ad53737f85c7c6'       # gate 9's QQPURGE GO head (on main)
CHANGE='aef649a4eee9644097469ab6774dcd7d3f2b7a6a'          # v2.34: the change commit = 9bd21c0's parent
HQ_EXPECT='9bd21c0ef142cecc0dc06c6eabd0df1b2aeba63e'
CHAINQ="$CHANGE $HQ_EXPECT"
# Every file QQCAD changes (exactly).
DELTA_FILES='BACKLOG.md CLAUDE.md HANDOVER/02-business-rules.md index.html quote-engine.test.mjs stage3/package.json stage3/test/fx-seed-fallback.mjs stage3/test/print-fit.mjs stage3/test/xlsx-parity.mjs'

SUBJECT_STEM='[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 16'
QUESTION_SUBJ='[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>'
ANSWER_PREFIX='[Tuesday -> QA/Vision-gate16] ANSWER'
STATUS_SUBJ='[QA/Datasec-Vision -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch'
PARK_LINE='PARKED: flagged — awaiting the Opus 4.8 switch'

q() { git --no-optional-locks -C "$Q_REPO" "$@"; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE gate (Vision gate 16) on Datasec/Vision_Sales_Portal, in the QUICKQUOTE repo: ONE TIER-1 target, ONE verdict, GO / GO WITH FINDINGS / NO GO. QuickQuote main is e408904 (live v2.33). The target QQCAD (TIER 1, ROUND 1) is QuickQuote v2.34, branch feat/qq-cad-currency-2026-10-12 at 9bd21c0: aef649a (CAD in both currency selects, the offline seed CAD 1.4200, toolVersion 2.34, plus tests and docs) and 9bd21c0 (a BACKLOG ticket only). It is NOT on main; it is 2 ahead, 0 behind.

READ YOUR COMMISSION FIRST, whole: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-12_vision-gate16-qq-v234-cad.md
Then read the charter it names, the Vision CLARIFICATIONS (C-01..C-14; C-14 is Kam's ruling for this target: "Add CAD, priced like the other non-regional currencies", card quickquote-cad-currency-1012 = a), the project's CLAUDE.md (/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/CLAUDE.md; its deploy commands are not for you), the QuickQuote repo's own CLAUDE.md at the head (git show; its publish lines are not for you), the builder's READY mail under test, read WHOLE including the correction appended at its end (/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-12_vision-qq-v234-cad-READY-mail.txt), gate 9's report /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-27-vision-gate9-vsp65-qqpurge (the last QuickQuote gate: §Q, NOT TESTED, evidence/tools/) and gate 8's report /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-25-vision-qq-gate8 (the QuickQuote browser instrument: the Chrome egress block, census, floor count; evidence/ holds the instruments you copy). Every builder statement is a CLAIM, never evidence. RE-DERIVE every red, every mutant and every suite set yourself. Verify every PRIOR WORK claim against git history and gates 8-9's evidence, never against the brief. The brief's MODEL RULE and TUESDAY'S RULINGS are stamped: apply them, do not re-rule them.

WHAT THE BRIEF REQUIRES, in short (the brief is the authority):
(1) THE BUILDER'S SUITE, RE-RUN: at the head 9bd21c0 and at base e408904, same session, as SETS, NOT COUNTS: the root pricing pack (node --test quote-engine.test.mjs), and in stage3/: npm test, npm run test:print, npm run test:xlsx, node strip.js. Red at base for cells 1, 3, 4 and 5 (the head's test files copied, hash-verified, onto an archive of e408904), each red's message quoted and explained by the missing CAD. Cell 2 is a GUARD, green at base by construction: confirm it is green at base, then prove it bites with the builder's mutants M4, M5 and M6 (M5 must redden cell 2). Re-derive M1-M3 and add yours (G-M1..G-M4). Every red-proof: fresh tree per arm, the tamper asserted landed, node --check (or a clean page load) quoted; a red from a mutant that does not parse is VOID.
(2) THE INDEPENDENT BROWSER LEG on the offline file:// build AND the stripped hosted build: a real local Google Chrome driven by YOUR own puppeteer-core harness under YOUR egress-block wrapper, a fresh profile, headful at least once. Every FX answer is a stub you choose or a block. Pick CAD and check every money figure against a quote YOU compute by hand first (professional services on the page are round(USD card rate x FX) x units: the brief's WRONG (b)), on screen and in print, at two rates. The offline fallback with every provider blocked lands 1.4200 and says the rate is the stored one, with the 1.4226 stub as its independent control. The live/manual rate rule for CAD. The Settings drawer psvCurrency CAD, which the builder did NOT drive: select CAD, save a regional rate, confirm the figures use it unconverted and that it persists and clears, AUD as the control; report exactly what happened, step by step. Reopen a stored CAD quote, including one whose stored object you derive from what the page itself sends (captured, never reaching a server). The CA$ display on screen and in print; and the workbook: produce a real CAD xlsx in-process from the unchanged render module and report what currency formatting it actually carries (numFmt per amount cell, any symbol, the footer text), because the builder withdrew its own workbook claim.
(3) NO REGRESSION on the other seven currencies (USD AUD EUR GBP NZD SGD DKK): at a fixed stubbed rate and with every provider blocked, base vs head on both builds, no money string, FX note, seed or printed figure changed (only the version badge and the new CAD option may differ).
(4) BRAND/STYLE: no new colour, token or style in the change (READ: the launcher proves the exact four-line index.html delta); screenshots of CAD and AUD in BOTH themes, both builds, desktop and phone width, the Settings drawer too; WCAG contrast of the CAD figures from computed styles, compared to AUD.
(5) THE BUILDER'S FINDING: the three static USD labels are pre-existing at e408904 (there at lines 1391/1397/1459; the READY's 1392/1398/1460 are the head's), visible in CAD and AUD on screen, absent from print and workbook, and ticketed under BACKLOG "## Open" at 9bd21c0 — not introduced.
(6) DEPLOY-ON-MERGE, READ ONLY: .github at the head (only tests.yml; name every job, trigger, Node version and whether anything deploys, builds or pushes an image). You run NO az at all: the builder's az acr task list -r hpasqqacr = [] is RELAYED, and GitHub webhooks are UNMEASURED.
CI is UNMEASURED: this project's gh is not authenticated and you must not use gh; never claim CI; name CI's five Node 22 jobs as the first reads at merge.

NO DATABASE, NO SERVER ENTRY POINT. PRODUCTION IS LIVE for this project. NEVER the live QuickQuote (hpas-quickquote, hpas-quickquote-rg, hpasqqacr, its Table Storage, its log workspace) and NEVER the live portal (datasec-sales-portal.azurewebsites.net, datasec-sales-portal-rg): no request, not even a GET. No az of any kind, no deploy, no publish, no app-setting change. Never the FX hosts (stubbed or blocked only), never ntfy.sh, never the npm registry. Never Claude in Chrome (Kam's own Chrome with his sign-ins). Never type an HPAM word; never open anything under the project's 4_Credentials. The hosted build is YOUR strip output served by request interception at an http://qq.test origin; the workbook comes from calling the unchanged render module in-process; the stage3 hosted server's own entry point is never started.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT from the object store (git archive into a fresh mktemp -d under projects/vision/work-g16/). Each tree is EXCLUSIVE to this gate and to one purpose; never touch work/ or work-g2 .. work-g15. The builder's checkout of the QuickQuote repo is LIVE (a Vision seat is in it, on the feature branch): never read its working tree as evidence. Copy gate 8's and gate 9's instruments into YOUR evidence folder and re-point them (they hard-code work-g8 / work-g9); never run from, edit or write into gate 1-15's copies. Dependencies (stage3/ only): npm ci --offline --ignore-scripts only, then prove node_modules/.package-lock.json against the lockfile entry by entry (lockcmp.py AND lockwalk.py). Never npm install, never npm audit, never npx anything not already in the tree. In the repo use ONLY read verbs (show, log, diff, ls-remote, rev-parse, ls-tree, cat-file, grep, merge-base, archive); never fetch, pull, checkout, switch, worktree, commit, stash, reset, clean or gc. Run git merge-tree --write-tree only from the gate's OWN object dir (GIT_OBJECT_DIRECTORY = your own mktemp -d, alternates = the repo's objects), or skip it and say so (the merge is a fast-forward). Findings-only: no writes in the QuickQuote repo, none inside Vision_Sales_Portal, none in gate 1-15's report folders or trees. Never rm: quarantine. Run every loop and every git show <sha>:<path> under bash. Run node strip.js before any lone browser file. CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY: a control derived from the run it validates is not a control.

FLOOR DISCIPLINE. Vision has no jest lock; never borrow NexusAI's. Never use ports 4848, 8080 or 47787; take every port from the kernel and bind 127.0.0.1 if you need one at all. No database, no Azurite, no docker command at all (NODE20-LEG is as the brief sets it). Every product process runs under env -i with an explicit allowlist, NODE_ENV never production. Never set AGENTMAIL_API_KEY or AGENTMAIL_INBOX in a product process (with both set, QuickQuote SENDS FOR REAL), nor any real ACS_* or MAIL_SENDER, TABLES_CONNECTION_STRING, SALES_COPY_EMAIL, HPAM_WORD, ADVANCED_UNLOCK_SECRET or WEBSITE_SITE_NAME; print each product process's env KEY NAMES and assert none is forbidden. NTFY_SERVER=http://ntfy.invalid; never contact ntfy.sh. EGRESS INCLUDING CHROME CHILDREN: every Chrome runs under your copy of gate 8's egress-block wrapper as PUPPETEER_EXECUTABLE_PATH; prove the block with its positive control and run the net-log scan at the end; record GoogleUpdater and chrome_crashpad_handler at start and end; reap every Chrome by the pid you started. Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid, with the brief's negative-control seats classifying FOREIGN in the same run. A zero is reportable only beside an ATTACHED control that fired in the same window. Other seats are live on this box: record the load average beside every timing number; a latency result with no load figure is not a measurement.
DEADLINE AND HEARTBEAT: every step has a written DEADLINE built into your runner (there is no timeout binary here) and releases its Chromes, pages, children and temp profiles in a finally. Log a HEARTBEAT line at least every 2 minutes; a step with no heartbeat for 5 minutes is aborted and reported, never waited on. Deadlines: one page cell 120 s; a whole test:print run 420 s; a whole test:xlsx run 300 s; the root pack 120 s; one mutant arm 420 s. Nothing above 420 s.

THE MODEL RULE (Kam, live board 2026-09-30 09:07, card (b)): QA gates may switch to Opus 4.8 when flagged by Opus 5.5's safeguards, PER SESSION. You start on Opus 5.5. You run the FULL rows. If one of your responses is stopped by the safeguards: that step is NOT RUN (never re-worded to slip past); write ONE line to evidence/classifier-stops.txt; reap any Chrome you started; mail tuesday-agent@agentmail.to with the subject exactly "[QA/Datasec-Vision -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch"; then end your turn with the line "PARKED: flagged — awaiting the Opus 4.8 switch" and wait. Tuesday switches THIS pane's model and taps you by mail. You never answer the model dialog yourself, and nobody ever chooses "Switch automatically". After the switch, resume at the stopped row. The report states which rows ran on which model, with the switch time, and quotes classifier-stops.txt whole.

QUESTIONS: your routing name is QA/Vision-gate16. If you must ask, mail tuesday-agent@agentmail.to with the subject "[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>" and proceed on the safest reading without waiting (the one exception is a safeguards stop, which PARKS you under THE MODEL RULE). Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/Vision-gate16] ANSWER"; read it with your verdict key. Never wednesday-agent@. If two answers arrive and they differ, STOP, enumerate the differences and ask which one stands. If a response is cut off by a safety check, record it and continue with the next item; this is authorised defensive QA of Datasec's own product on loopback. Record every question, reading and answer in the report.

Write your report to: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-10-12-vision-gate16-qq-v234-cad/report.md

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with a subject beginning exactly:
[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 16: QQCAD @ <sha7> <GO | GO WITH FINDINGS | NO GO>
(the sha7 is the pinned head from the verified table below). Lead the body with ONE sentence as the brief's section 14 words it (CAD priced as USD x the rate the page shows on both builds, on screen and in print; 1.4200 with every provider blocked; the Settings drawer save; the reopened quote; no figure changed for the other seven currencies), then one line each on the workbook's currency formatting (MEASURED), the three USD labels, deploy-on-merge (READ ONLY) and the class count (round 1: a NO GO goes to round 2). You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no credentials directory of its own. Use it only in your own mail calls, with a client timeout. Never put the key or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice — the only turn you end while waiting is the PARKED line of THE MODEL RULE.

Report the pinned head and main as three timestamped readings (start / mid / end), with the branch name beside each. Include the verbatim strings the brief lists: the CAD option text, the FX note for the seed and for a stubbed live rate, psvStatus after a CAD save, the base's error when CAD is forced, the workbook footer, every CA$ form and every bare $ or USD amount on a CAD screen. Include a table with one row per brief section N item: MEASURED or NOT TESTED, and HOW.

Rule 2 stands: what you did NOT test is first-class output. Write a NOT TESTED section that covers at least CI (UNMEASURED), the stage3 container and its Debian Chromium, Node 20 and Node 22, test:azurite and real Azure Table Storage, the live FX providers' real answers, GitHub webhooks and the publish path, the account managers' real browsers and locales, Claude in Chrome (not used), and every row you did not run. Label every action recommendation MEASURED AT RUNTIME, PROBED or READ ONLY.
PROMPT_EOF

# ---------------------------------------------------------------- GUARDS
[ -d "$QA_DIR" ]  || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]   || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -n "$PROMPT" ]  || { echo "embedded prompt is empty" >&2; exit 4; }
[ -d "$Q_REPO/.git" ] || [ -f "$Q_REPO/.git" ] || { echo "repo under test missing: $Q_REPO" >&2; exit 5; }

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
TARGETS='QQCAD'
EXPECT_IDS="MAIN-Q $TARGETS"
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
  [ "$(fld "$ID" 2)" = "quickquote" ] || { echo "REFUSING: PIN row $ID repo must be quickquote" >&2; exit 40; }
done
[ "$(fld MAIN-Q 3)" = "main" ] || { echo "REFUSING: row MAIN-Q branch must be main" >&2; exit 40; }
[ "$(fld QQCAD 3)" = "feat/qq-cad-currency-2026-10-12" ] || { echo "REFUSING: row QQCAD branch is '$(fld QQCAD 3)', the brief's target is feat/qq-cad-currency-2026-10-12 — re-brief" >&2; exit 40; }
is40 "$(fld QQCAD 5)" || { echo "REFUSING: PIN row QQCAD base is not a 40-hex sha" >&2; exit 40; }
printf '%s' "$(fld QQCAD 6)" | grep -Eq '^[1-9][0-9]*$' || { echo "REFUSING: PIN row QQCAD commits '$(fld QQCAD 6)' is not a positive integer" >&2; exit 40; }
[ "$(fld QQCAD 4)" = "$HQ_EXPECT" ] || { echo "REFUSING: QQCAD's PIN head $(fld QQCAD 4 | cut -c1-7) is not ${HQ_EXPECT:0:7} — this launcher's chain and content guards are pinned to it; re-brief" >&2; exit 40; }
MAINH="$(fld MAIN-Q 4)"
HQ="$(fld QQCAD 4)"

# 6 — every sha the guards use is a commit in the local object store (this launcher never fetches).
for S in "$MAINH" "$HQ" "$ANCHOR_MAIN" "$ANCHOR_MAINP" "$ANCHOR_G9" "$CHANGE"; do
  T="$(q cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in the QuickQuote repo (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 9m — MAIN: e408904 EXACTLY (the commission: refuse if either moved).
[ "$MAINH" = "$ANCHOR_MAIN" ] || { echo "REFUSING: the pinned MAIN ${MAINH:0:7} is not e408904 — this gate pins main exactly; re-brief" >&2; exit 9; }

# 7 / 8 — the target: base as briefed, ancestor AND merge-base with MAIN, not on main, exact count, 0 behind.
H7="${HQ:0:7}"; BASE="$(fld QQCAD 5)"; N="$(fld QQCAD 6)"
[ "$BASE" = "$ANCHOR_MAIN" ] || { echo "REFUSING: row QQCAD base ${BASE:0:7} is not e408904 — re-brief" >&2; exit 7; }
q merge-base --is-ancestor "$BASE" "$HQ" 2>/dev/null || { echo "REFUSING: QQCAD base ${BASE:0:7} is not an ancestor of $H7" >&2; exit 7; }
[ "$(q merge-base "$HQ" "$MAINH" 2>/dev/null)" = "$BASE" ] || { echo "REFUSING: QQCAD merge-base(head, MAIN) is not its base ${BASE:0:7}" >&2; exit 7; }
q merge-base --is-ancestor "$HQ" "$MAINH" 2>/dev/null && { echo "REFUSING: QQCAD $H7 is ALREADY ON MAIN ${MAINH:0:7} — the brief says it is not; re-brief" >&2; exit 7; }
GOTN="$(q rev-list --count "${BASE}..${HQ}" 2>/dev/null)"
[ "$GOTN" = "$N" ] || { echo "REFUSING: QQCAD $H7 has $GOTN commits over its base, the table says $N" >&2; q log --format='%h %p %s' "${BASE}..${HQ}" >&2; exit 8; }
[ "$(q rev-list --count "${HQ}..${ANCHOR_MAIN}" 2>/dev/null)" = "0" ] || { echo "REFUSING: QQCAD $H7 is behind e408904" >&2; exit 7; }

# 9 — gated anchors, never-rebased, exact chain, no merges.
[ "$(q log -1 --format='%P' "$ANCHOR_MAIN")" = "$ANCHOR_MAINP" ] || { echo "REFUSING: e408904's single parent is not 986f7b8" >&2; exit 9; }
q merge-base --is-ancestor "$ANCHOR_G9" "$MAINH" 2>/dev/null || { echo "REFUSING: gate 9's QQPURGE head ac74111 is not on main ${MAINH:0:7}" >&2; exit 9; }
[ "$(q log -1 --format='%P' "$HQ")" = "$CHANGE" ] || { echo "REFUSING: QQCAD ${H7}'s single parent is not aef649a — rebased or rebuilt" >&2; exit 9; }
[ "$(q log -1 --format='%P' "$CHANGE")" = "$ANCHOR_MAIN" ] || { echo "REFUSING: aef649a's single parent is not e408904 — rebased or rebuilt" >&2; exit 9; }
[ "$(q rev-list --no-merges "${ANCHOR_MAIN}..${HQ}" 2>/dev/null | sort)" = "$(printf '%s\n' $CHAINQ | sort)" ] \
  || { echo "REFUSING: QQCAD's commits over e408904 are not exactly the pinned chain. Got:" >&2; q rev-list --no-merges "${ANCHOR_MAIN}..${HQ}" >&2; exit 9; }
[ -z "$(q rev-list --merges "${ANCHOR_MAIN}..${HQ}" 2>/dev/null)" ] || { echo "REFUSING: QQCAD carries a merge over e408904 — the brief says none" >&2; exit 9; }

# 18 — RE-PIN: BOTH rows at origin, by ls-remote, read NOW (immediately before launch). No movement allowed, main included.
for ID in $EXPECT_IDS; do
  BR="$(fld "$ID" 3)"; H="$(fld "$ID" 4)"
  L="$(q ls-remote origin "refs/heads/$BR" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" && continue
  echo "REFUSING: row $ID: $H is not at refs/heads/$BR on origin — that ref moved or was never pushed; re-pin and re-brief" >&2; printf '%s\n' "${L:-<nothing>}" >&2; exit 18
done
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — exact file sets.
GOT="$(q diff --name-only "$ANCHOR_MAIN" "$HQ" 2>/dev/null | sort)"
[ "$GOT" = "$(printf '%s\n' $DELTA_FILES | sort)" ] || { echo "REFUSING: QQCAD ${H7}'s delta over e408904 is not exactly the briefed 9-file set. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }
[ "$(q diff --name-only "$CHANGE" "$HQ" 2>/dev/null)" = "BACKLOG.md" ] || { echo "REFUSING: 9bd21c0 touches other than BACKLOG.md over aef649a (the READY: 'then 9bd21c0 \"backlog: ...\" (one ticket)')" >&2; exit 22; }

# 23 — THE EXACT index.html DELTA (replaces gate 15's two-target overlap check). The brand clause, READ: no style in any added line.
blob() { q rev-parse "${1}:${2}" 2>/dev/null; }
[ "$(blob "$CHANGE" index.html)" = "$(blob "$HQ" index.html)" ] || { echo "REFUSING: index.html differs between aef649a and 9bd21c0" >&2; exit 23; }
[ "$(q diff --numstat "$ANCHOR_MAIN" "$HQ" -- index.html | awk '{print $1" "$2}')" = "4 2" ] || { echo "REFUSING: index.html's delta is not +4/-2" >&2; exit 23; }
DADD="$(q diff -U0 "$ANCHOR_MAIN" "$HQ" -- index.html | grep '^+[^+]')"
DDEL="$(q diff -U0 "$ANCHOR_MAIN" "$HQ" -- index.html | grep '^-[^-]')"
EXP_ADD="$(printf '%s\n' '+        <option value="CAD">CAD — Canadian Dollar</option>' '+        <option value="CAD">CAD — Canadian Dollar</option>' \
  '+  toolVersion: "2.34",' '+  fxSeeds: { USD: 1.0000, AUD: 1.5500, CAD: 1.4200, EUR: 0.9300, GBP: 0.7900, NZD: 1.6700, SGD: 1.3500, DKK: 6.9300 },')"
EXP_DEL="$(printf '%s\n' '-  toolVersion: "2.33",' '-  fxSeeds: { USD: 1.0000, AUD: 1.5500, EUR: 0.9300, GBP: 0.7900, NZD: 1.6700, SGD: 1.3500, DKK: 6.9300 },')"
[ "$DADD" = "$EXP_ADD" ] || { echo "REFUSING: index.html's added lines are not exactly the briefed four. Got:" >&2; printf '%s\n' "$DADD" >&2; exit 23; }
[ "$DDEL" = "$EXP_DEL" ] || { echo "REFUSING: index.html's deleted lines are not exactly the briefed two. Got:" >&2; printf '%s\n' "$DDEL" >&2; exit 23; }
printf '%s\n' "$DADD" | grep -Eiq 'style|color|colour|#[0-9a-f]{3,8}\b|rgb\(|var\(--|font' && { echo "REFUSING: an added index.html line carries style/colour — the brief's brand clause says none" >&2; exit 23; }
HUNKS="$(q diff -U0 "$ANCHOR_MAIN" "$HQ" -- index.html | awk '/^@@ /{ split($2, o, ","); printf "%s ", substr(o[1], 2) }')"
[ "$HUNKS" = "1263 1573 1724 1803 " ] || { echo "REFUSING: index.html's hunk map is '$HUNKS', the brief reads 1263 1573 1724 1803 (old side)" >&2; exit 23; }

# 74 — content, read from the pinned shas (never a checkout).
has() { q show "${1}:${2}" 2>/dev/null | grep -qF -- "$3"; }   # sha path fixed-string
must() { has "$1" "$2" "$3" || { echo "REFUSING: ${1:0:7}:$2 lacks '$3' — the brief gates different code; re-brief" >&2; exit 74; }; }
mustnot() { has "$1" "$2" "$3" && { echo "REFUSING: ${1:0:7}:$2 carries '$3' — the brief's reading is wrong; re-brief" >&2; exit 74; }; return 0; }
ntests() { q show "${1}:${2}" 2>/dev/null | grep -cE '^[[:space:]]*test\('; }
wantn() { [ "$(ntests "$1" "$2")" = "$3" ] || { echo "REFUSING: ${1:0:7}:$2 carries $(ntests "$1" "$2") test( cells, the brief says $3" >&2; exit 74; }; }
lineat() { q show "${1}:index.html" 2>/dev/null | sed -n "${2}p"; }
must "$HQ" index.html '<option value="CAD">CAD — Canadian Dollar</option>'
mustnot "$ANCHOR_MAIN" index.html '<option value="CAD">'
mustnot "$ANCHOR_MAIN" index.html 'CAD: 1.4200'
must "$HQ" index.html 'toolVersion: "2.34",'
must "$ANCHOR_MAIN" index.html 'toolVersion: "2.33",'
[ "$(q show "${HQ}:index.html" | grep -cF '<option value="CAD">CAD — Canadian Dollar</option>')" = "2" ] || { echo "REFUSING: the head does not carry exactly two CAD options" >&2; exit 74; }
for T in 'id="psvCurrency"' 'id="currency"' 'function fmt(value) {' 'function fmt0(value) {' 'function psRatesFor(currency, fxRate, regional, cfg) {' \
         'function applyPsvRates(cur) {' 'const PSV_KEY = "hpasQuoteTool_settings";' 'https://api.frankfurter.dev/v1/latest?base=USD&symbols={CUR}' \
         'https://open.er-api.com/v6/latest/USD' '$("price-basic").value  = Math.round(basic).toString();'; do
  must "$HQ" index.html "$T"
done
# The three static USD labels: present at base (1391/1397/1459) and at the head (1392/1398/1460) — the builder's finding, pre-existing.
for PAIR in "1391|1392|Per device, per month (USD)" "1397|1398|\$20.00/device/month</small>" "1459|1460|(\$20.00/device/month instead of \$22.50 mix-and-match)."; do
  LB="${PAIR%%|*}"; REST="${PAIR#*|}"; LH="${REST%%|*}"; T="${REST#*|}"
  lineat "$ANCHOR_MAIN" "$LB" | grep -qF -- "$T" || { echo "REFUSING: e408904:index.html:$LB lacks '$T' — the brief's WRONG (a) reading is wrong" >&2; exit 74; }
  lineat "$HQ" "$LH" | grep -qF -- "$T" || { echo "REFUSING: 9bd21c0:index.html:$LH lacks '$T' — the READY's line numbers are not the head's" >&2; exit 74; }
done
must "$HQ" BACKLOG.md '- [ ] **Three static USD labels stay on screen when a non-USD currency is selected**'
mustnot "$ANCHOR_MAIN" BACKLOG.md 'Three static USD labels'
# Test cells.
wantn "$ANCHOR_MAIN" quote-engine.test.mjs 67
wantn "$HQ" quote-engine.test.mjs 69
wantn "$HQ" stage3/test/fx-seed-fallback.mjs 3
must "$HQ" quote-engine.test.mjs "test(\"v2.34: CAD is offered in both currency selects and has a 1.42 offline seed\""
must "$HQ" quote-engine.test.mjs "test(\"v2.34: a CAD quote's every figure is the USD figure x the rate, worked by hand\""
must "$HQ" quote-engine.test.mjs 'near(cad.grandTotal, 6159.858, "grand total");'
must "$HQ" stage3/test/fx-seed-fallback.mjs 'assert.equal(s.fxRate, "1.4200", "the offline seed Kam ruled: 1.42 CAD per USD");'
must "$HQ" stage3/test/fx-seed-fallback.mjs 'if (u === ORIGIN + "/api/quote/" + QNUM && storedQuote) {'
must "$HQ" stage3/test/print-fit.mjs 'svcmode: "advanced", customHours: 30, currency: "CAD", fxRate: 1.4226 },'
must "$HQ" stage3/test/xlsx-parity.mjs 'if (cs.currency === "CAD") assert.match(report.printedGrand, /^CA\$/, "the printed total is in CA$");'
must "$HQ" stage3/package.json 'test/fx-provenance.mjs test/fx-seed-fallback.mjs test/phone-layout.mjs'
mustnot "$ANCHOR_MAIN" stage3/package.json 'fx-seed-fallback'
[ "$(q diff --numstat "$ANCHOR_MAIN" "$HQ" -- quote-engine.test.mjs stage3/test/fx-seed-fallback.mjs | awk '{s+=$2} END {print s+0}')" = "0" ] \
  || { echo "REFUSING: QQCAD deleted lines from quote-engine.test.mjs or fx-seed-fallback.mjs — the brief reads additions only" >&2; exit 74; }
# Unchanged blobs (the workbook, the render, the store, the mailer, the strip, the server module, the lockfile, the image, CI).
for F in stage3/lib/xlsx.js stage3/lib/pdf.js stage3/lib/store.js stage3/lib/mail.js stage3/strip.js stage3/server.js stage3/package-lock.json \
         stage3/Dockerfile .github/workflows/tests.yml .dockerignore; do
  B0="$(blob "$ANCHOR_MAIN" "$F")"
  [ -n "$B0" ] && [ "$(blob "$HQ" "$F")" = "$B0" ] || { echo "REFUSING: $F differs between main and the head — the brief says it is carried unchanged" >&2; exit 74; }
done
must "$HQ" stage3/lib/xlsx.js 'const NUMFMT = { amount: "#,##0", rate: "#,##0.00", count: "#,##0" };'
must "$HQ" stage3/lib/xlsx.js '`quote ${report.qnum} · amounts in ${report.currency}. ` +'
must "$HQ" stage3/lib/store.js 'if (!CONN) throw new Error("TABLES_CONNECTION_STRING is required");'
must "$HQ" stage3/Dockerfile 'FROM node:20-bookworm-slim'
[ "$(q ls-tree -r --name-only "$HQ" .github)" = ".github/workflows/tests.yml" ] || { echo "REFUSING: .github at the head holds other than tests.yml — the brief's §N6 reading is wrong" >&2; exit 74; }
for T in 'pricing-pack:' 'stage3-server:' 'store-azurite:' 'print-fit:' 'xlsx-parity:'; do must "$HQ" .github/workflows/tests.yml "  $T"; done
[ "$(q show "${HQ}:.github/workflows/tests.yml" | awk '/^jobs:/{f=1;next} f && /^  [a-z0-9-]+:$/{n++} END{print n+0}')" = "5" ] || { echo "REFUSING: tests.yml does not carry exactly five jobs" >&2; exit 74; }
for T in 'npm ci --offline --ignore-scripts' 'entry by entry' 'never npm audit'; do
  grep -qiF "$T" "$BRIEF" || { echo "REFUSING: brief lacks the dependency rule '$T'" >&2; exit 63; }
  printf '%s\n' "$PROMPT" | grep -qiF -- "$T" || { echo "REFUSING: prompt lacks the dependency rule '$T'" >&2; exit 63; }
done

# 31 — the READY is on disk, names the pinned heads, carries its correction, and its NOT TESTED lines are carried verbatim; sources on disk.
[ -s "$READY" ] || { echo "REFUSING: the READY mail is not on disk: $READY" >&2; exit 31; }
for T in "feat/qq-cad-currency-2026-10-12 = ${HQ}" "main = ${MAINH} (untouched)" 'READY FOR QA: QuickQuote v2.34 CAD (tier 1)' \
         'READY FOR QA: QuickQuote v2.34 CAD (tier 1) — correction' 'workbook currency labelling unmeasured' 'Branch head is still 9bd21c0.'; do
  grep -qF -- "$T" "$READY" || { echo "REFUSING: $READY does not carry '$T'" >&2; exit 31; }
done
NT="$(awk 'f&&!/^- /{exit} f{print;next} /^NOT TESTED/{f=1;print}' "$READY")"
[ -n "$NT" ] || { echo "REFUSING: $READY carries no NOT TESTED block" >&2; exit 31; }
while IFS= read -r L; do
  [ -n "$L" ] || continue
  grep -qxF -- "$L" "$BRIEF" || { echo "REFUSING: the brief does not carry this NOT TESTED line of the READY verbatim: $L" >&2; exit 31; }
done <<< "$NT"
for T in 'QQCAD NOT TESTED' 'C-14' 'quickquote-cad-currency-1012' 'ROUND 1' 'GUARD' 'M4' 'M5' 'M6' 'CA$' '#,##0' 'amounts in' \
         '2026-10-12_vision-qq-v234-cad-READY-mail.txt' ':1391' ':1397' ':1459' 'WRONG (a)' 'WRONG (b)' 'WRONG (c)' 'WRONG (d)' 'hpasqqacr' 'RELAYED'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: the brief does not carry '$T'" >&2; exit 31; }
done
[ -s "$CLAR" ] || { echo "REFUSING: Vision CLARIFICATIONS.md absent: $CLAR" >&2; exit 31; }
grep -qF '**C-14.' "$CLAR" || { echo "REFUSING: $CLAR lacks C-14" >&2; exit 31; }
for T in 'quickquote-cad-currency-1012' 'Offline fallback seed 1.42 CAD per USD' 'Professional services = USD rate card × live FX' 'Add CAD, priced like the other non-regional currencies'; do
  grep -qF -- "$T" "$CLAR" || { echo "REFUSING: CLARIFICATIONS C-14 does not carry '$T' — the ruling the brief quotes is not on disk" >&2; exit 31; }
done
grep -qF '**C-15.' "$CLAR" && echo "NOTE: Vision CLARIFICATIONS now has a C-15 — the brief says C-01..C-14; read it before launch" >&2
[ -s "$G9_REPORT" ] || { echo "REFUSING: gate 9's report is absent: $G9_REPORT" >&2; exit 31; }
grep -qF 'QQPURGE @ ac74111 GO' "$G9_REPORT" || { echo "REFUSING: gate 9's report does not carry QQPURGE's GO at ac74111" >&2; exit 31; }
[ -s "$G8_REPORT" ] || { echo "REFUSING: gate 8's report is absent: $G8_REPORT" >&2; exit 31; }
for D in "$G8_DIR" "$G9_DIR"; do
  grep -qF "$D" "$BRIEF" || { echo "REFUSING: the brief does not name $D" >&2; exit 31; }
  case "$PROMPT" in *"$D"*) ;; *) echo "REFUSING: the prompt does not name $D" >&2; exit 31 ;; esac
done
for H in qa-chrome-egressblock.sh qa-egress-monitor.py qa-egress-posctl.mjs qa-chrome-census.py qa-floorcount.py qa-harness-floorctl.mjs mktree-qq.sh lockcmp.py lockwalk.py; do
  [ -s "$G8_EV/$H" ] || { echo "REFUSING: gate 8's instrument $H is not on disk — the brief names it" >&2; exit 31; }
  grep -qF -- "$H" "$BRIEF" || { echo "REFUSING: the brief does not name gate 8's instrument $H" >&2; exit 31; }
done
for H in mutate-qq.py run-suite.sh tapsets.py; do
  [ -s "$G9_TOOLS/$H" ] || { echo "REFUSING: gate 9's tool $H is not on disk — the brief names it" >&2; exit 31; }
  grep -qF -- "$H" "$BRIEF" || { echo "REFUSING: the brief does not name gate 9's tool $H" >&2; exit 31; }
done

# 39 — the floor instrument is on disk and named.
[ -s "$G8_FLOOR" ] || { echo "REFUSING: gate 8's floor instrument missing: $G8_FLOOR" >&2; exit 39; }
grep -qF 'qa-floorcount.py' "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument qa-floorcount.py" >&2; exit 39; }

# 10 / 17 — report path named in both; no stale report.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

# 12 — tier declared in both, at the pinned head.
grep -qE "^- \*\*QQCAD\*\* at \`${H7}\` — \*\*TIER 1" "$BRIEF" || { echo "REFUSING: brief does not declare QQCAD at \`$H7\` TIER 1" >&2; exit 12; }
case "$PROMPT" in *"QQCAD (TIER 1"*) ;; *) echo "REFUSING: prompt does not declare: QQCAD (TIER 1" >&2; exit 12 ;; esac

# 78 — the commission's requirements, in both.
for T in 'TIER 1' 'ROUND 1' 'C-14' 'GO WITH FINDINGS' 'NO GO' 'SETS, NOT COUNTS' 'red at base' 'cells 1, 3, 4' 'GUARD' 'M4' 'M5' 'M6' \
         'file://' 'hosted build' 'by hand' '1.4200' 'every provider blocked' 'Settings drawer' 'psvCurrency' 'regional rate' 'Reopen' 'CA$' \
         'workbook' 'numFmt' 'USD AUD EUR GBP NZD SGD DKK' 'BOTH themes' 'contrast' 'three static USD labels' '1391' 'BACKLOG' \
         '.github' 'tests.yml' 'hpasqqacr' 'UNMEASURED' 'NODE20-LEG' 'e408904' '9bd21c0' 'aef649a' 'egress-block' 'puppeteer-core' \
         'node strip.js' 'test:print' 'test:xlsx' 'quote-engine.test.mjs' 'node --check' 'VOID' 'Claude in Chrome' 'HPAM word'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks '$T'" >&2; exit 78; }
  printf '%s\n' "$PROMPT" | grep -qiF -- "$T" || { echo "REFUSING: prompt lacks '$T'" >&2; exit 78; }
done

# 13 / 14 / 15 / 20 / 70 — directive, brief path, placeholders, verdict route, key path, question route, safety line.
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
case "$PROMPT" in *"$READY"*) ;; *) echo "REFUSING: prompt must name the READY path" >&2; exit 14 ;; esac
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

# 82 — THE MODEL RULE (Kam 2026-09-30 09:07, card (b)), in brief and prompt, per session, never "Switch automatically".
for T in "$STATUS_SUBJ" "$PARK_LINE" 'classifier-stops.txt' 'Switch automatically' 'Opus 4.8' 'PER SESSION' 'which rows ran on which model' 'Opus 5.5'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks THE MODEL RULE fragment '$T'" >&2; exit 82; }
  case "$(printf '%s' "$PROMPT" | tr '[:upper:]' '[:lower:]')" in *"$(printf '%s' "$T" | tr '[:upper:]' '[:lower:]')"*) ;; *) echo "REFUSING: prompt lacks THE MODEL RULE fragment '$T'" >&2; exit 82 ;; esac
done
grep -qF '## THE MODEL RULE' "$BRIEF" || { echo "REFUSING: brief lacks the THE MODEL RULE section" >&2; exit 82; }

# 19 — words the prompt must carry (% is a space) and the brief's sections.
WORDS="merge-tree NOT%TESTED env%-i bash e408904 9bd21c0 aef649a work-g16 FOREGROUND MEASURED%AT%RUNTIME PROBED READ%ONLY start%/%mid%/%end CI VOID node%--check"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## Charter' '^## RULED BY KAM, AND SETTLED' '^## PRIOR ROUND' '^PRIOR ROUND: ' 'ITS REPORT IS ON DISK AT:' '^## PIN' \
         '^## WRONG OR UNVERIFIABLE' '^## THE READY' '^## 2a. LEGITIMATE SHAPES' '^## N1. ' '^## N2. ' '^## N3. ' '^## N4. ' '^## N5. ' '^## N6. ' \
         '^## 12. The merge' '^## 13. FLOOR' '^## THE MODEL RULE' "^## TUESDAY'S RULINGS AT STAMP" '^## 14. Output' '^PROVENANCE:'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
# 24 — the prompt must DESCRIBE the app's entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qE 'server/index\.js|stage3/server\.js|server\.js'; then
  echo "REFUSING: the prompt contains a literal server entry path — this agent would read as a FOREIGN SERVER to an argv-grep floor check. Describe it; do not name it." >&2; exit 24; fi

# 53 / 60 / 61 / 62 / 64 / 69 / 75 — standing rules, in both.
for T in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' '420 s' '120 s'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the deadline/heartbeat rule '$T'" >&2; exit 53; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the deadline/heartbeat rule '$T'" >&2; exit 53 ;; esac
done
for T in 'node --check' 'VOID'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the parse-before-red rule '$T'" >&2; exit 60; }
done
for T in 'EXCLUSIVE' 'work-g16'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the tree-exclusivity rule '$T'" >&2; exit 61; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the tree-exclusivity rule '$T'" >&2; exit 61 ;; esac
done
for T in '4848' '8080' '47787' 'env -i' 'AGENTMAIL_API_KEY' 'AGENTMAIL_INBOX' 'no jest lock' 'TABLES_CONNECTION_STRING' 'HPAM_WORD' 'ADVANCED_UNLOCK_SECRET' \
         'PUPPETEER_EXECUTABLE_PATH' 'GoogleUpdater' 'chrome_crashpad_handler' 'net-log'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the QuickQuote floor rule '$T'" >&2; exit 62; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the QuickQuote floor rule '$T'" >&2; exit 62 ;; esac
done
for T in 'NEVER the live' 'hpas-quickquote' 'hpas-quickquote-rg' 'datasec-sales-portal.azurewebsites.net' 'datasec-sales-portal-rg' 'no app-setting change' 'no publish'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not name '$T' as NEVER" >&2; exit 64; }
  printf '%s\n' "$PROMPT" | grep -qiF -- "$T" || { echo "REFUSING: prompt does not name '$T' as NEVER" >&2; exit 64; }
done
for T in 'ntfy.invalid' 'never contact ntfy.sh'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the ntfy egress rule '$T'" >&2; exit 69; }
  printf '%s\n' "$PROMPT" | grep -qiF -- "$T" || { echo "REFUSING: prompt lacks the ntfy egress rule '$T'" >&2; exit 69; }
done
for T in 'CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY' 'PRIOR WORK' 'OWN object dir' 'no writes in the QuickQuote repo' 'start / mid / end' 'NOT TESTED'; do
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

# 44 — REPURPOSED: the browser leg's instrument, a local Google Chrome, is installed. The launcher never starts it.
[ -x "$CHROME_BIN" ] || { echo "REFUSING: no local Google Chrome at $CHROME_BIN — the browser leg (brief §N2-§N4) would be NOT RUN" >&2; exit 44; }

# 41 — the answer route exists (Tuesday adds 'QA/Vision-gate16|tuesday-agent@agentmail.to|no' at launch). Run late on purpose: --check
#      shows every other guard first.
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || {
  echo "guards pass (40 6 9 7 8 18 22 23 74 63 31 39 10 17 12 78 13 14 15 20 70 82 19 24 53 60 61 62 64 69 75 38 45 44); route NOT added." >&2
  echo "REFUSING: no '${ROUTE_NAME}|tuesday-agent@agentmail.to|…' line in $ROUTING — answers to the gate would have no route. Add it (pattern: the QA/Vision-gate15 line) before launch." >&2; exit 41; }

# 32 — the coordinator stamps the self-check (line AND note) and every @STAMP@. LAST, so --check shows every other guard first.
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "guards pass (40 6 9 7 8 18 22 23 74 63 31 39 10 17 12 78 13 14 15 20 70 82 19 24 53 60 61 62 64 69 75 38 45 44 41); self-check NOT stamped." >&2
  echo "REFUSING: the brief still carries ${PH_STAMP} (Self-check line and note, or TUESDAY'S RULINGS items 1-4) — the coordinator re-reads end-to-end and stamps all of them before launch" >&2; exit 32
fi

PIN_BLOCK="$(printf 'PINNED HEADS — verified by the launcher at %s (cat-file; base e408904, 0 behind; ancestor and merge-base with MAIN; not-already-on-main; commit count; exact chain, no merges; 9bd21c0<-aef649a<-e408904<-986f7b8; main pinned EXACTLY; the exact index.html delta; git ls-remote origin for both rows):\n' "$PIN_TS"
  printf '%s\n' "$PIN" | awk -F'\t' '{ printf "  %-7s %-11s %-34s %s  base %s  commits %s\n", $1, $2, $3, $4, ($5=="-"?"-":substr($5,1,12)), $6 }'
  printf '  Main: pinned %s (exact; a move refuses)\n' "${MAINH:0:12}"
  printf '  index.html delta (old-side hunks 1263 1573 1724 1803): two CAD options, toolVersion 2.33 -> 2.34, fxSeeds + CAD 1.4200; no style\n'
  printf '  Positive controls: base e408904 (CAD not selectable; AUD figures to compare); gate 9 head ac74111 on main\n'
  printf 'NODE20-LEG, as set in the brief: %s\n' "$NODE20")"

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  printf '%s\n' "$PIN_BLOCK"
  echo "  PIN parsed, two rows, no placeholder, head = 9bd21c0 (40); every sha a local commit (6); main = e408904 exactly (9)"
  echo "  base e408904, count 2, 0 behind (7 8); exact chain, no merges, parents pinned, ac74111 on main (9); origin re-read $PIN_TS, both rows (18)"
  echo "  file set 9, 9bd21c0 = BACKLOG.md only (22); index.html delta exact, hunk map, no style (23)"
  echo "  CAD present/absent, labels 1391/1397/1459 -> 1392/1398/1460, BACKLOG ticket, test( 67/69/3, unchanged blobs, NUMFMT/footer, .github = tests.yml x5 jobs (74); deps (63)"
  echo "  READY lines + correction + NOT TESTED verbatim, C-14, gate 8 + 9 reports + instruments (31); floor (39); report absent (17); tier (12); commission (78)"
  echo "  directive/brief/placeholders/mail/key/questions/safety (13 14 15 20 70); MODEL RULE (82); words + sections (19); no server path (24); standing rules (53 60 61 62 64 69 75); seats $NEG_SEATS (38); NODE20 $NODE20 (45); Chrome (44); route $ROUTE_NAME (41); stamped (32)"
  echo "  model: claude-opus-5-5 at exec"
  exit 0
fi

# 11 — no inherited identity: this gate needs neither az nor gh, so both point at fresh EMPTY directories.
ID_TMP="$(mktemp -d "${TMPDIR:-/tmp}/qa-vision-gate16-id.XXXXXX")" || { echo "REFUSING: cannot create the empty identity dir" >&2; exit 11; }
mkdir -p "$ID_TMP/azure-empty" "$ID_TMP/gh-empty" || { echo "REFUSING: cannot create the empty identity dirs under $ID_TMP" >&2; exit 11; }
{ [ -z "$(ls -A "$ID_TMP/azure-empty")" ] && [ -z "$(ls -A "$ID_TMP/gh-empty")" ]; } || { echo "REFUSING: the identity dirs under $ID_TMP are not empty" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_TMP/azure-empty"
export GH_CONFIG_DIR="$ID_TMP/gh-empty"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"
# 64 (cont.) — nothing a product process could use to reach a real provider is inherited from this shell.
unset DATABASE_URL TEST_DATABASE_URL AGENTMAIL_API_KEY AGENTMAIL_INBOX ACS_CONNECTION_STRING ACS_EMAIL_CONNECTION_STRING ACS_EMAIL_SENDER \
      MAIL_SENDER TABLES_CONNECTION_STRING AZURE_BACKUP_CONN_STR SESSION_SECRET HPAM_WORD ADVANCED_UNLOCK_SECRET SALES_COPY_EMAIL \
      FEEDBACK_NOTIFY_EMAIL FEEDBACK_NOTIFY_EMAILS APPROVALS_INBOX NTFY_TOPIC NTFY_SERVER LEAD_BOT_API_KEY WEBSITE_SITE_NAME COORDINATOR_SECRET \
      PORT NODE_ENV PUPPETEER_EXECUTABLE_PATH
echo "identity: AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR GH_CONFIG_DIR=$GH_CONFIG_DIR (empty) CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR" >&2

PROMPT="$PROMPT

$PIN_BLOCK"
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model claude-opus-5-5 "$PROMPT"
