#!/bin/bash
# launch_qa_vision_gate17.sh — cross-project QA agent, ONE gate (Vision gate 17; drafted 2026-10-13 10:16-10:5x AEDT from the gate-16 launcher) on
# Datasec/Vision_Sales_Portal, QuickQuote repo: ONE target at TIER-1 weight (R1), ONE verdict (GO / GO WITH FINDINGS / NO GO):
#   QQQR  fix/qq-quality-round-2026-10-13  PR #6  QuickQuote v2.35 — CI red (9) + CodeQL #1-#14 (C-17)   TIER-1 weight, round 1
#
# Main is 108bbb4 (live v2.34; merge of e408904 + 1270b71). QQQR = f84f12f d05cf11 537d672 1e1d78d 0b8bbb1 d030674 (6), 0 behind.
# THIS GATE PINS MAIN EXACTLY: a main that moved (even to a harmless descendant) REFUSES. refs/pull/6/head must equal the head.
#
# THE HEADS LIVE IN ONE PLACE: the brief's PIN-HEADS table. This launcher PARSES it, refuses any placeholder, verifies every row against the
# object store and against origin by `git ls-remote` NOW, and appends the verified table to the agent's prompt. The only shas it carries are
# GATED ANCHORS: main 108bbb4 and its parents e408904 + 1270b71, 9bd21c0 (gate 16's GO-WITH-FINDINGS head, on main), the six chain commits.
#
# PRODUCTION IS LIVE for this project (hpas-quickquote / hpasqqacr; datasec-sales-portal-rg). The gate is local trees + an in-process app on
# loopback + a local Chrome with every FX host stubbed or blocked. No database, no Azurite, no docker, no az. Findings only.
#
# GUARDS RE-DERIVED from launch_qa_vision_gate16.sh (kept as the template, untouched). EVERY gate-16 guard number is kept. Differences:
#   - PIN: two rows (MAIN-Q 108bbb4, QQQR d030674 base 108bbb4 x6). Target id QQQR (was QQCAD).
#   - exit 9: main pinned EXACTLY; 108bbb4's parents pinned (e408904 1270b71); gate 16's head 9bd21c0 on main; exact six-commit chain, each
#     single parent pinned; no merges.
#   - exit 18: ls-remote for BOTH rows AND refs/pull/6/head must equal the pin; a moved main refuses. refs/pull/6/merge is printed (NOTE only).
#   - exit 22: file set 8; per-commit file sets pinned.
#   - exit 23: THE EXACT index.html DELTA by sha256 of the -U0 added and deleted lines, +13/-5, hunk map; no colour/token/style= in any added line
#     (gate 16's literal-line check would trip on this round's legitimate CSS lines, so the brand clause is now: exact delta by hash + no NEW
#     colour/token). Whole-diff numstat pinned.
#   - exit 74: the round's content (esc x2, toolVersion 2.35, CSS wrap, the limiter on three routes and not /healthz, the email check, the exact
#     express-rate-limit pin + lockfile integrity, test:print + doc-escape, npm test strip-first, tests.yml permissions), test( counts, the
#     unchanged-blob list, the stale sendFailure.js comment (WRONG (g)), .github = tests.yml x5 jobs.
#   - exit 31: the READY by its "Branch ... @ d030674, off main 108bbb4" line, its HOLDS line, NOT TESTED verbatim; CLARIFICATIONS C-17 (+ NOTE on a
#     C-18); gate 16's report + tools; gate 8 + 9 reports and instruments (originals).
#   - exit 38: negative-control seats re-read 10:23 AEDT (Tuesday 3983 %0, Vision builder 39098 %12, NexusAI 84103 %11).
#   - exit 46 (NEW): the brief's GH-API-LEG setting (READ-ONLY-VISION-TOKEN | NOT-RUN); refuses on TUESDAY-DECIDES. Decides exit 11's GH_CONFIG_DIR.
#   - exit 11: AZURE_CONFIG_DIR always EMPTY. GH_CONFIG_DIR EMPTY unless GH-API-LEG = READ-ONLY-VISION-TOKEN, in which case it is Vision's
#     .gh-config behind a launcher-written GET-only `gh` shim first on PATH (refuses every gh call except `gh api` with no -X/--method/-f/-F/
#     --field/--raw-field/--input and no graphql).
#   - 46, 41 and 32 are the coordinator's to-do guards: they run LAST and are REPORTED TOGETHER (each pending one printed), exiting with the
#     first pending code, so --check shows every other guard first AND every pending item at once.
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/Vision-gate17' "bash '<this file>'"), NEVER nohup.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Contains a legitimate `cd` (into the QA project, at exec).
# READ-ONLY toward the repo: only cat-file, rev-parse, merge-base, log, rev-list, diff, diff-tree, show, ls-tree, ls-remote.
# --check is READ-ONLY: it runs every guard and exits before any identity dir is made or any agent is started.
# Usage: launch_qa_vision_gate17.sh [--check]
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
PH_GHLEG='TUESDAY''-DECIDES'

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEFS="$TUE/2_Project_Files/fleet/qa-agent/briefs"
BRIEF="$BRIEFS/2026-10-13_vision-gate17-qq-quality-round.md"
READY="$BRIEFS/2026-10-13_vision-qq-quality-round-READY-mail.txt"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
VSP='/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal'
Q_REPO="$VSP/Quoting Tool/hpas-quoting-tool"
VSP_GH="$VSP/4_Credentials/.gh-config"
CLAR="$VSP/1_Project_Definition/CLARIFICATIONS.md"
REPORTS="$QA_DIR/projects/vision/reports"
G8_DIR="$REPORTS/2026-09-25-vision-qq-gate8"
G8_REPORT="$G8_DIR/report.md"
G8_EV="$G8_DIR/evidence"
G8_FLOOR="$G8_EV/qa-floorcount.py"
G9_DIR="$REPORTS/2026-09-27-vision-gate9-vsp65-qqpurge"
G9_REPORT="$G9_DIR/report.md"
G9_TOOLS="$G9_DIR/evidence/tools"
G16_DIR="$REPORTS/2026-10-12-vision-gate16-qq-v234-cad"
G16_REPORT="$G16_DIR/report.md"
G16_TOOLS="$G16_DIR/evidence/tools"
REPORT="$REPORTS/2026-10-13-vision-gate17-qq-quality-round/report.md"
ROUTE_NAME='QA/Vision-gate17'
NEG_SEATS='3983 39098 84103'   # Tuesday (%0), Vision builder (%12), NexusAI (%11) — read 10:23 AEDT
CHROME_BIN='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
PR_NUM='6'
PR_MERGE_SEEN='f1a106629389187f9288968b4a805269812db353'     # refs/pull/6/merge at 10:16 (GitHub's test merge; NOTE only)
# Gated anchors (not heads).
ANCHOR_MAIN='108bbb443647e0f1c8ec2f426e9f33c15585eaa2'     # QuickQuote main = live v2.34 (C-16: image v0.6.2-tool2.34-108bbb4)
ANCHOR_MAINP='e4089041d6213d460e74992ddf775a909ffe03eb 1270b71b8bc679ad70973646545e435e324e7dd9'   # 108bbb4's two parents (merge of PR #3)
ANCHOR_G16='9bd21c0ef142cecc0dc06c6eabd0df1b2aeba63e'      # gate 16's QQCAD GO-WITH-FINDINGS head (on main)
C1='f84f12f145b1ca5648c2624dbf2498a940d79325'               # npm test strip-first          (tier 2)
C2='d05cf11ac285e297ab918f1f8b12252f8430f5ab'               # tests.yml permissions         (tier 2)
C3='537d6720d5f87d5a5ce2a6fe36cc0b4737693611'               # email ReDoS                   (tier 1)
C4='1e1d78d5181503e2d84fb1084f7388649d44e0c6'               # esc() logo src + footer, v2.35 (tier 1)
C5='0b8bbb1e1d21f6360ca55b213b329903c53bd77a'               # express-rate-limit 8.7.0      (tier 1)
HQ_EXPECT='d030674694279be3159d67de4a10f220ea6b8335'       # 481 px .app-row wrap, v2.35   (tier 2, user-visible)
CHAINQ="$C1 $C2 $C3 $C4 $C5 $HQ_EXPECT"
# Every file QQQR changes (exactly).
DELTA_FILES='.github/workflows/tests.yml index.html stage3/package-lock.json stage3/package.json stage3/server.js stage3/test/doc-escape.mjs stage3/test/phone-layout.mjs stage3/test/server.test.mjs'
NUMSTAT_EXPECT='5/0/.github/workflows/tests.yml 13/5/index.html 43/0/stage3/package-lock.json 3/2/stage3/package.json 37/4/stage3/server.js 82/0/stage3/test/doc-escape.mjs 19/1/stage3/test/phone-layout.mjs 82/1/stage3/test/server.test.mjs '
IDX_ADD_SHA='f360bc69784f9dd5386de3517f3bf00db25ef0e91c5d7e58e7180bf7e4f90a7b'
IDX_DEL_SHA='5eadcac05655e355dc767b8a0180c612af88e2cff657f5976ce98ff008d000bd'
IDX_HUNKS='268 270 279 1726 2477 2752 '

SUBJECT_STEM='[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 17'
QUESTION_SUBJ='[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>'
ANSWER_PREFIX='[Tuesday -> QA/Vision-gate17] ANSWER'
STATUS_SUBJ='[QA/Datasec-Vision -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch'
PARK_LINE='PARKED: flagged — awaiting the Opus 4.8 switch'

q() { git --no-optional-locks -C "$Q_REPO" "$@"; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE gate (Vision gate 17) on Datasec/Vision_Sales_Portal, in the QUICKQUOTE repo: ONE target at TIER-1 weight, ONE verdict, GO / GO WITH FINDINGS / NO GO. QuickQuote main is 108bbb4 (live v2.34). The target QQQR (TIER 1 weight for the whole round, Tuesday's ruling R1; ROUND 1) is the QuickQuote quality round, PR #6, branch fix/qq-quality-round-2026-10-13 at d030674, v2.35: f84f12f (npm test runs node strip.js first; tier 2), d05cf11 (tests.yml permissions contents: read, CodeQL #1-#5; tier 2), 537d672 (the sign-in email check, ReDoS, CodeQL #6; tier 1), 1e1d78d (esc( at the logo src and the footer currency, CodeQL #7-#11, v2.35; tier 1), 0b8bbb1 (express-rate-limit 8.7.0 on GET /, /login and /api/advanced/module, 300 per source per 10 min, CodeQL #12-#14; tier 1), d030674 (the 481 px .app-row wrap; tier 2, user-visible). It is NOT on main; it is 6 ahead, 0 behind.

READ YOUR COMMISSION FIRST, whole: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-13_vision-gate17-qq-quality-round.md
Then read the charter it names, the Vision CLARIFICATIONS (C-01..C-17; C-17 is Kam's ruling for this target: card quickquote-ci-red-codeql-14-1013 = a, "Commission a fix round now"; publishing and any Azure change are not covered), the project's CLAUDE.md (/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/CLAUDE.md, its QuickQuote section; its deploy commands are not for you), the QuickQuote repo's own CLAUDE.md at the head (git show; its publish lines are not for you), the builder's READY mail under test, read WHOLE (/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-13_vision-qq-quality-round-READY-mail.txt), gate 16's report /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-10-12-vision-gate16-qq-v234-cad (the last QuickQuote gate, GO WITH FINDINGS at 9bd21c0; evidence/tools/ holds the instruments you copy), and the instruments' originals in gate 8's report /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-25-vision-qq-gate8 and gate 9's report /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-27-vision-gate9-vsp65-qqpurge. Every builder statement is a CLAIM, never evidence. RE-DERIVE every red, every mutant, every suite set and every timing yourself. Verify every PRIOR WORK claim against git history and gates 8-16's evidence, never against the brief. The brief's MODEL RULE and TUESDAY'S RULINGS (R1-R10, verbatim, and the stamped D1-D4) are stamped: apply them, do not re-rule them.

WHAT THE BRIEF REQUIRES, in short (the brief is the authority):
(1) THE BUILDER'S SUITES, RE-RUN at the head d030674 and at base 108bbb4, same session, as SETS, NOT COUNTS: the root pricing pack (node --test quote-engine.test.mjs), and in stage3/: npm test, npm run test:print, npm run test:xlsx, node strip.js. Red at base for every new cell (the head's test files copied, hash-verified, onto an archive of 108bbb4), each red's message quoted and explained by the missing fix, not by a missing module. The doc-escape footer cell is a GUARD, green at base by construction: confirm it, quote the throw for a non-code currency at the head, and prove the guard bites something. Re-derive every builder mutant and add yours (G-M1..G-M6). Every red-proof: fresh tree per arm, the tamper asserted landed, node --check (or a clean page load) quoted; a red from a mutant that does not parse is VOID.
(2) f84f12f: reproduce the strip race at base (generated files absent, forced serial order, the server suite first) and its absence at f84f12f and at the head. d05cf11: read tests.yml whole at both shas.
(3) 537d672, R7: measure the ReDoS on the server path — the hosted server module's createApp() export, in-process, on a kernel-chosen port bound to 127.0.0.1, never the module's own entry point — with the red-at-base inputs: multi-second at base, under 1 s at the head, with the load beside every timing and a concurrent /healthz probe. Enumerate the malformed-email behaviour change over the brief's corpus (it is wider than the READY lists) and confirm real addresses stay accepted.
(4) 1e1d78d, R6: re-measure byte identity of the quote document (page 1 + page 2) on BOTH builds, base vs head, for the builder's five shapes and two of yours, normalising only the version, date and quote number; the masthead src with entities prints byte for byte at the head; the hosted render through the unchanged lib/pdf.js in-process agrees; print as a real PDF, both themes, one A4 per page.
(5) 0b8bbb1, R3: the 301st request from one source is 429 on each of the three routes and none before; /healthz unlimited; another source unaffected; forged left X-Forwarded-For entries do not dodge (trustForwardedFor passed as the createApp() option, never by setting WEBSITE_SITE_NAME); the IPv6 /64 arm; the setting validated; the 429's body, Content-Type and Retry-After; stderr captured for any express-rate-limit ValidationError. npm ci --offline --ignore-scripts, the lockfile proven entry by entry; then read the npm registry ONLY by curl -s -m 30 https://registry.npmjs.org/<pkg> for express-rate-limit, debug, ms and ip-address from your own shell (the brief's one exception): 8.7.0's publish date must be at least two weeks before 2026-10-13. The 300 number is ruled acceptable (R3): test it, do not re-rule it.
(6) d030674, R5: a REAL local Google Chrome (your own puppeteer-core harness, your egress-block wrapper, a fresh profile, headful at least once; the offline file:// build AND your stripped hosted build at http://qq.test by interception; never the live site) at 481, 520, 543 and a 1280 desktop control, light and dark, normal fonts AND wide fonts (a wide sans, a wide MONO — the price is set in --mono — and both), in AUD, CAD and the widest currency: the price is visible where it used to clip, nothing else moved (a 1 px sweep, normal fonts, base vs head), no sideways scroll, print unchanged. Screenshots before/after go into the report for Kam.
(7) CODEQL #1-#14, R4: none may be dismissed. The brief's WRONG (a): the PR-side instances query also reads 0 for refs/pull/3/head (a tree that carries all 14) and for a ref that does not exist, so a zero on refs/pull/6/merge proves nothing. If the brief's GH-API-LEG allows, re-run that control yourself with gh api GET reads only; give a per-alert READ table at d030674; report R4 as NOT MEASURABLE before the merge if the control shows the instrument blind, and name main's post-merge analysis showing #1-#14 fixed as the first read at merge. Never claim R4 MEASURED on a query your own control shows blind.
(8) DEPLOY-ON-MERGE, R8, READ ONLY: .github at the head (only tests.yml), and, if GH-API-LEG allows, repo hooks, environments, deployments, secret names, workflows, rulesets. You run NO az at all: the builder's Azure reads (hpasqqacr tasks and webhooks, the webapp's deployment source) are RELAYED.
(9) BRAND/STYLE and version discipline: no new colour or token in the change (the launcher proves the exact index.html delta by hash); the repo's version rule judged.
GH-API-LEG (appended below by the launcher as the brief sets it): READ-ONLY-VISION-TOKEN means gh is on your PATH as a GET-only shim over Vision's gh config — use gh api GET reads only, never -X/--method, -f/-F/--field/--raw-field/--input or graphql, never a comment, review, label, approval, re-run or dismissal, and never open any file under the project's 4_Credentials; NOT-RUN means GH_CONFIG_DIR is empty and you must not use gh at all: every GitHub read is NOT RUN and the drafter's readings stay READ-BY-DRAFTER. Either way CI and CodeQL results are claims you may only read, never cause.

NO DATABASE, NO SERVER ENTRY POINT. PRODUCTION IS LIVE for this project. NEVER the live QuickQuote (hpas-quickquote, hpas-quickquote-rg, hpasqqacr, its Table Storage, its log workspace) and NEVER the live portal (datasec-sales-portal.azurewebsites.net, datasec-sales-portal-rg): no request, not even a GET. No az of any kind, no deploy, no publish, no app-setting change. Never the FX hosts (stubbed or blocked only), never ntfy.sh, never the npm registry except the brief's registry.npmjs.org reads. Never Claude in Chrome (Kam's own Chrome with his sign-ins). Never type an HPAM word; never open anything under the project's 4_Credentials. The hosted build is YOUR strip output served by request interception at an http://qq.test origin; the server path is the hosted server module's createApp() export in-process on loopback; the module's own entry point is never started.

HELD, R10: the READY's HOLDS stand untouched — local QuickQuote main 8b29136 (unpushed; never use the name main in the repo, only the pinned 40-hex shas), worktrees qq-108bbb4 and qq-986f7b8 (and the builder's qq-main), rollback image v0.6.1-tool2.33-986f7b8. No merge, no publish, no comment or status on PR #6, no alert dismissal, no mail to any human.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT from the object store (git archive into a fresh mktemp -d under projects/vision/work-g17/). Each tree is EXCLUSIVE to this gate and to one purpose; never touch work/ or work-g2 .. work-g16. The builder's checkout of the QuickQuote repo is LIVE: never read any working tree as evidence. Copy gate 16's instruments (and, if needed, gate 8's and gate 9's originals) into YOUR evidence folder and re-point them (gate 16's hard-code work-g16 and its own report folder); never run from, edit or write into gate 1-16's copies. Dependencies (stage3/ only): npm ci --offline --ignore-scripts only, then prove node_modules/.package-lock.json against the lockfile entry by entry (lockcmp.py AND lockwalk.py). Never npm install, never npm audit, never npx anything not already in the tree. In the repo use ONLY read verbs (show, log, diff, ls-remote, rev-parse, ls-tree, cat-file, grep, merge-base, archive); never fetch, pull, checkout, switch, worktree, commit, stash, reset, clean, gc, branch or for-each-ref. Run git merge-tree --write-tree only from the gate's OWN object dir (GIT_OBJECT_DIRECTORY = your own mktemp -d, alternates = the repo's objects), or skip it and say so. Findings-only: no writes in the QuickQuote repo, none inside Vision_Sales_Portal, none in gate 1-16's report folders or trees. Never rm: quarantine. Run every loop and every git show <sha>:<path> under bash. Run node strip.js before any lone browser file. CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY: a control derived from the run it validates is not a control.

FLOOR DISCIPLINE. Vision has no jest lock; never borrow NexusAI's. Never use ports 4848, 8080 or 47787; take every port from the kernel and bind 127.0.0.1. No database, no Azurite, no docker command at all (NODE20-LEG is as the brief sets it). Every product process runs under env -i with an explicit allowlist, NODE_ENV never production. Never set AGENTMAIL_API_KEY or AGENTMAIL_INBOX in a product process (with both set, QuickQuote SENDS FOR REAL), nor any real ACS_* or MAIL_SENDER, TABLES_CONNECTION_STRING, SALES_COPY_EMAIL, HPAM_WORD, ADVANCED_UNLOCK_SECRET, WEBSITE_SITE_NAME, GH_TOKEN or GITHUB_TOKEN; print each product process's env KEY NAMES and assert none is forbidden. NTFY_SERVER=http://ntfy.invalid; never contact ntfy.sh. EGRESS INCLUDING CHROME CHILDREN: every Chrome runs under your copy of the egress-block wrapper as PUPPETEER_EXECUTABLE_PATH; prove the block with its positive control and run the net-log scan at the end; record GoogleUpdater and chrome_crashpad_handler at start and end; reap every Chrome and every app listener by the pid you started. Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid, with the brief's negative-control seats classifying FOREIGN in the same run. A zero is reportable only beside an ATTACHED control that fired in the same window. Other seats are live on this box: record the load average beside every timing number; a latency result with no load figure is not a measurement.
DEADLINE AND HEARTBEAT: every step has a written DEADLINE built into your runner (there is no timeout binary here) and releases its Chromes, pages, children, app servers and temp profiles in a finally. Log a HEARTBEAT line at least every 2 minutes; a step with no heartbeat for 5 minutes is aborted and reported, never waited on. Deadlines: one page cell 120 s; one server-path timing request 120 s; a whole test:print run 420 s; a whole test:xlsx run 300 s; a whole npm test run 300 s; the root pack 120 s; one mutant arm 420 s. Nothing above 420 s.

THE MODEL RULE (Kam, live board 2026-09-30 09:07, card (b); Tuesday's R9): QA gates may switch to Opus 4.8 when flagged by Opus 5.5's safeguards, PER SESSION. You start on Opus 5.5. You run the FULL rows. If one of your responses is stopped by the safeguards: that step is NOT RUN (never re-worded to slip past); write ONE line to evidence/classifier-stops.txt; reap any Chrome and app server you started; mail tuesday-agent@agentmail.to with the subject exactly "[QA/Datasec-Vision -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch"; then end your turn with the line "PARKED: flagged — awaiting the Opus 4.8 switch" and wait. Tuesday switches THIS pane's model and taps you by mail. You never answer the model dialog yourself, and nobody ever chooses "Switch automatically". After the switch, resume at the stopped row. The report states which rows ran on which model, with the switch time, and quotes classifier-stops.txt whole.

QUESTIONS: your routing name is QA/Vision-gate17. If you must ask, mail tuesday-agent@agentmail.to with the subject "[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>" and proceed on the safest reading without waiting (the one exception is a safeguards stop, which PARKS you under THE MODEL RULE). Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/Vision-gate17] ANSWER"; read it with your verdict key. Never wednesday-agent@. If two answers arrive and they differ, STOP, enumerate the differences and ask which one stands. If a response is cut off by a safety check, record it and continue with the next item; this is authorised defensive QA of Datasec's own product on loopback. Record every question, reading and answer in the report.

Write your report to: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-10-13-vision-gate17-qq-quality-round/report.md

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with a subject beginning exactly:
[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 17: QQQR @ <sha7> <GO | GO WITH FINDINGS | NO GO>
(the sha7 is the pinned head from the verified table below). Lead the body with ONE sentence as the brief's section 14 words it (the suites as sets vs 108bbb4; the ReDoS timing on the server path; the 429 on the 301st request on each route and nothing else; byte identity except the version; the price visible at 481 px with a wide font and nothing else moved; and what can and cannot be said about CodeQL #1-#14 before the merge), then one line each on the full malformed-email behaviour change, the express-rate-limit 8.7.0 publish date from the registry, deploy-on-merge (READ ONLY / RELAYED), the screenshots for Kam (paths) and the class count (round 1: a NO GO goes to round 2). You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no credentials directory of its own. Use it only in your own mail calls, with a client timeout. Never put the key or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice — the only turn you end while waiting is the PARKED line of THE MODEL RULE.

Report the pinned head and main as three timestamped readings (start / mid / end), with the branch name beside each, plus refs/pull/6/head. Include the verbatim strings the brief lists: the 429 body and Retry-After, the ReDoS timings with load, the email corpus table, the printed logo src at base and head, the throw for a non-code currency, the registry dates, every ValidationError line or none. Include a table with one row per brief section N item: MEASURED, NOT TESTED or NOT MEASURABLE, and HOW.

Rule 2 stands: what you did NOT test is first-class output. Write a NOT TESTED section that covers at least CodeQL's verdict before the merge (NOT MEASURABLE), local CodeQL (not authorised), the Azure side of deploy-on-merge (RELAYED), CI (read only, never caused), the stage3 container and its Debian Chromium, Node 20 and Node 22, test:azurite and real Azure Table Storage, the live front end's real X-Forwarded-For, the rate-limit window reset if not measured, Windows Segoe UI and Consolas rendering, the account managers' real browsers and locales, the Dependabot branches, Claude in Chrome (not used), and every row you did not run. Label every action recommendation MEASURED AT RUNTIME, PROBED or READ ONLY.
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
TARGETS='QQQR'
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
[ "$(fld QQQR 3)" = "fix/qq-quality-round-2026-10-13" ] || { echo "REFUSING: row QQQR branch is '$(fld QQQR 3)', the brief's target is fix/qq-quality-round-2026-10-13 — re-brief" >&2; exit 40; }
is40 "$(fld QQQR 5)" || { echo "REFUSING: PIN row QQQR base is not a 40-hex sha" >&2; exit 40; }
printf '%s' "$(fld QQQR 6)" | grep -Eq '^[1-9][0-9]*$' || { echo "REFUSING: PIN row QQQR commits '$(fld QQQR 6)' is not a positive integer" >&2; exit 40; }
[ "$(fld QQQR 4)" = "$HQ_EXPECT" ] || { echo "REFUSING: QQQR's PIN head $(fld QQQR 4 | cut -c1-7) is not ${HQ_EXPECT:0:7} — this launcher's chain and content guards are pinned to it; re-brief" >&2; exit 40; }
MAINH="$(fld MAIN-Q 4)"
HQ="$(fld QQQR 4)"

# 6 — every sha the guards use is a commit in the local object store (this launcher never fetches).
for S in "$MAINH" "$HQ" "$ANCHOR_MAIN" $ANCHOR_MAINP "$ANCHOR_G16" $CHAINQ; do
  T="$(q cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in the QuickQuote repo (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 9m — MAIN: 108bbb4 EXACTLY (refuse if it moved).
[ "$MAINH" = "$ANCHOR_MAIN" ] || { echo "REFUSING: the pinned MAIN ${MAINH:0:7} is not 108bbb4 — this gate pins main exactly; re-brief" >&2; exit 9; }

# 7 / 8 — the target: base as briefed, ancestor AND merge-base with MAIN, not on main, exact count, 0 behind.
H7="${HQ:0:7}"; BASE="$(fld QQQR 5)"; N="$(fld QQQR 6)"
[ "$BASE" = "$ANCHOR_MAIN" ] || { echo "REFUSING: row QQQR base ${BASE:0:7} is not 108bbb4 — re-brief" >&2; exit 7; }
q merge-base --is-ancestor "$BASE" "$HQ" 2>/dev/null || { echo "REFUSING: QQQR base ${BASE:0:7} is not an ancestor of $H7" >&2; exit 7; }
[ "$(q merge-base "$HQ" "$MAINH" 2>/dev/null)" = "$BASE" ] || { echo "REFUSING: QQQR merge-base(head, MAIN) is not its base ${BASE:0:7}" >&2; exit 7; }
q merge-base --is-ancestor "$HQ" "$MAINH" 2>/dev/null && { echo "REFUSING: QQQR $H7 is ALREADY ON MAIN ${MAINH:0:7} — the brief says it is not; re-brief" >&2; exit 7; }
GOTN="$(q rev-list --count "${BASE}..${HQ}" 2>/dev/null)"
[ "$GOTN" = "$N" ] || { echo "REFUSING: QQQR $H7 has $GOTN commits over its base, the table says $N" >&2; q log --format='%h %p %s' "${BASE}..${HQ}" >&2; exit 8; }
[ "$N" = "6" ] || { echo "REFUSING: the brief's commit count is $N, this launcher's chain is six" >&2; exit 8; }
[ "$(q rev-list --count "${HQ}..${ANCHOR_MAIN}" 2>/dev/null)" = "0" ] || { echo "REFUSING: QQQR $H7 is behind 108bbb4" >&2; exit 7; }

# 9 — gated anchors, never-rebased, exact chain, no merges.
[ "$(q log -1 --format='%P' "$ANCHOR_MAIN")" = "$ANCHOR_MAINP" ] || { echo "REFUSING: 108bbb4's parents are not e408904 + 1270b71" >&2; exit 9; }
q merge-base --is-ancestor "$ANCHOR_G16" "$MAINH" 2>/dev/null || { echo "REFUSING: gate 16's QQCAD head 9bd21c0 is not on main ${MAINH:0:7}" >&2; exit 9; }
PREV="$ANCHOR_MAIN"
for C in $CHAINQ; do
  [ "$(q log -1 --format='%P' "$C")" = "$PREV" ] || { echo "REFUSING: ${C:0:7}'s single parent is not ${PREV:0:7} — rebased or rebuilt" >&2; exit 9; }
  PREV="$C"
done
[ "$PREV" = "$HQ" ] || { echo "REFUSING: the chain does not end at the head" >&2; exit 9; }
[ "$(q rev-list --no-merges "${ANCHOR_MAIN}..${HQ}" 2>/dev/null | sort)" = "$(printf '%s\n' $CHAINQ | sort)" ] \
  || { echo "REFUSING: QQQR's commits over 108bbb4 are not exactly the pinned chain. Got:" >&2; q rev-list --no-merges "${ANCHOR_MAIN}..${HQ}" >&2; exit 9; }
[ -z "$(q rev-list --merges "${ANCHOR_MAIN}..${HQ}" 2>/dev/null)" ] || { echo "REFUSING: QQQR carries a merge over 108bbb4 — the brief says none" >&2; exit 9; }

# 18 — RE-PIN: BOTH rows AND refs/pull/6/head at origin, by ls-remote, read NOW (immediately before launch). No movement allowed, main included.
for ID in $EXPECT_IDS; do
  BR="$(fld "$ID" 3)"; H="$(fld "$ID" 4)"
  L="$(q ls-remote origin "refs/heads/$BR" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" && continue
  echo "REFUSING: row $ID: $H is not at refs/heads/$BR on origin — that ref moved or was never pushed; re-pin and re-brief" >&2; printf '%s\n' "${L:-<nothing>}" >&2; exit 18
done
LP="$(q ls-remote origin "refs/pull/${PR_NUM}/head" "refs/pull/${PR_NUM}/merge" 2>&1)"
printf '%s\n' "$LP" | grep -q "^${HQ}[[:space:]]refs/pull/${PR_NUM}/head\$" \
  || { echo "REFUSING: refs/pull/${PR_NUM}/head is not ${H7} on origin — PR #${PR_NUM} moved or is not the target; re-pin and re-brief" >&2; printf '%s\n' "${LP:-<nothing>}" >&2; exit 18; }
PR_MERGE_NOW="$(printf '%s\n' "$LP" | awk -v r="refs/pull/${PR_NUM}/merge" '$2==r{print $1}')"
[ "$PR_MERGE_NOW" = "$PR_MERGE_SEEN" ] || echo "NOTE: refs/pull/${PR_NUM}/merge is '${PR_MERGE_NOW:-<absent>}', the drafter read ${PR_MERGE_SEEN:0:7} — GitHub recomputed its test merge (main is pinned, so read why before launch)" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — exact file sets, whole and per commit.
GOT="$(q diff --name-only "$ANCHOR_MAIN" "$HQ" 2>/dev/null | sort)"
[ "$GOT" = "$(printf '%s\n' $DELTA_FILES | sort)" ] || { echo "REFUSING: QQQR ${H7}'s delta over 108bbb4 is not exactly the briefed 8-file set. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }
for PAIR in "$C1|stage3/package.json" "$C2|.github/workflows/tests.yml" "$C3|stage3/server.js stage3/test/server.test.mjs" \
            "$C4|index.html stage3/package.json stage3/test/doc-escape.mjs" \
            "$C5|stage3/package-lock.json stage3/package.json stage3/server.js stage3/test/server.test.mjs" \
            "$HQ|index.html stage3/test/phone-layout.mjs"; do
  C="${PAIR%%|*}"; W="${PAIR#*|}"
  [ "$(q diff-tree --no-commit-id --name-only -r "$C" 2>/dev/null | sort | tr '\n' ' ')" = "$(printf '%s\n' $W | sort | tr '\n' ' ')" ] \
    || { echo "REFUSING: ${C:0:7} touches other than the briefed files ($W)" >&2; q diff-tree --no-commit-id --name-only -r "$C" >&2; exit 22; }
done

# 23 — THE EXACT index.html DELTA (by hash), the whole numstat, the hunk map; the brand clause, READ: no NEW colour/token/style in an added line.
blob() { q rev-parse "${1}:${2}" 2>/dev/null; }
[ "$(q diff --numstat "$ANCHOR_MAIN" "$HQ" | awk '{printf "%s/%s/%s ", $1, $2, $3}')" = "$NUMSTAT_EXPECT" ] \
  || { echo "REFUSING: the whole-diff numstat is not the briefed one. Got:" >&2; q diff --numstat "$ANCHOR_MAIN" "$HQ" >&2; exit 23; }
DADD="$(q diff -U0 "$ANCHOR_MAIN" "$HQ" -- index.html | grep '^+[^+]')"
DDEL="$(q diff -U0 "$ANCHOR_MAIN" "$HQ" -- index.html | grep '^-[^-]')"
[ "$(printf '%s\n' "$DADD" | shasum -a 256 | awk '{print $1}')" = "$IDX_ADD_SHA" ] || { echo "REFUSING: index.html's added lines are not exactly the briefed thirteen (sha256 differs). Got:" >&2; printf '%s\n' "$DADD" >&2; exit 23; }
[ "$(printf '%s\n' "$DDEL" | shasum -a 256 | awk '{print $1}')" = "$IDX_DEL_SHA" ] || { echo "REFUSING: index.html's deleted lines are not exactly the briefed five (sha256 differs). Got:" >&2; printf '%s\n' "$DDEL" >&2; exit 23; }
printf '%s\n' "$DADD" | grep -Eiq '#[0-9a-f]{3,8}\b|rgba?\(|hsla?\(|--[a-z0-9-]+:|style=|<style' && { echo "REFUSING: an added index.html line carries a colour, a token definition or an inline style — the brief's brand clause says none" >&2; exit 23; }
HUNKS="$(q diff -U0 "$ANCHOR_MAIN" "$HQ" -- index.html | awk '/^@@ /{ split($2, o, ","); printf "%s ", substr(o[1], 2) }')"
[ "$HUNKS" = "$IDX_HUNKS" ] || { echo "REFUSING: index.html's hunk map is '$HUNKS', the brief reads $IDX_HUNKS(old side)" >&2; exit 23; }

# 74 — content, read from the pinned shas (never a checkout).
has() { q show "${1}:${2}" 2>/dev/null | grep -qF -- "$3"; }   # sha path fixed-string
must() { has "$1" "$2" "$3" || { echo "REFUSING: ${1:0:7}:$2 lacks '$3' — the brief gates different code; re-brief" >&2; exit 74; }; }
mustnot() { has "$1" "$2" "$3" && { echo "REFUSING: ${1:0:7}:$2 carries '$3' — the brief's reading is wrong; re-brief" >&2; exit 74; }; return 0; }
ntests() { q show "${1}:${2}" 2>/dev/null | grep -cE '^[[:space:]]*test\('; }
wantn() { [ "$(ntests "$1" "$2")" = "$3" ] || { echo "REFUSING: ${1:0:7}:$2 carries $(ntests "$1" "$2") test( cells, the brief says $3" >&2; exit 74; }; }
SRV=stage3/server.js
# index.html (1e1d78d + d030674)
must "$HQ" index.html 'toolVersion: "2.35",'
must "$ANCHOR_MAIN" index.html 'toolVersion: "2.34",'
must "$HQ" index.html 'src="${esc(src)}" alt="HP Authentication Suite">'
mustnot "$ANCHOR_MAIN" index.html 'src="${esc(src)}"'
must "$HQ" index.html 'Amounts are shown in whole ${esc($("currency").value)};'
must "$HQ" index.html 'display: flex; align-items: center; gap: .8rem; flex-wrap: wrap; row-gap: .35rem;'
must "$HQ" index.html 'white-space: nowrap; margin-left: auto; }'
must "$HQ" index.html '--mono: "Consolas", "SF Mono", "Cascadia Mono", "Liberation Mono", monospace;'
must "$HQ" index.html '@media screen and (max-width: 480px) {'
must "$HQ" index.html "return String(s).replace(/[&<>\"']/g, m =>"
# the hosted server module (537d672 + 0b8bbb1)
must "$HQ" "$SRV" 'const { rateLimit } = require("express-rate-limit");'
mustnot "$ANCHOR_MAIN" "$SRV" 'express-rate-limit'
for T in 'const PAGE_RATE_LIMIT_PER_10_MIN = 300;' 'const PAGE_RATE_WINDOW_MS = 10 * 60 * 1000;' \
         'app.get("/", pageLimiter, async (req, res) => {' 'app.get("/login", pageLimiter, (req, res) => res.sendFile(LOGIN_HTML));' \
         'app.get("/api/advanced/module", pageLimiter, requireAuth, (req, res) => {' 'app.get("/healthz", (req, res) => res.json({' \
         'keyGenerator: req => clientKey(req, trustForwardedFor),' 'validate: { xForwardedForHeader: false },' \
         'standardHeaders: false, legacyHeaders: false,' 'res.status(429).type("text/plain")' \
         'limit: budgetSetting("PAGE_RATE_LIMIT_PER_10_MIN", pageRateLimit, PAGE_RATE_LIMIT_PER_10_MIN),' \
         'if (email.length > 254 || !/^[^\s@]+@[^\s@.]+(?:\.[^\s@.]+)+$/.test(email)) {' 'if (require.main === module) {'; do
  must "$HQ" "$SRV" "$T"
done
must "$ANCHOR_MAIN" "$SRV" 'if (!/^\S+@\S+\.\S+$/.test(email)) return res.status(400).json({ error: "invalid email" });'
mustnot "$HQ" "$SRV" 'app.get("/healthz", pageLimiter'
# package.json / lockfile (f84f12f, 1e1d78d, 0b8bbb1)
must "$HQ" stage3/package.json '"express-rate-limit": "8.7.0",'
must "$HQ" stage3/package.json '"test": "node strip.js && node --test test/server.test.mjs test/strip.test.mjs test/mail.test.mjs test/store.test.mjs",'
mustnot "$ANCHOR_MAIN" stage3/package.json '"test": "node strip.js'
must "$HQ" stage3/package.json 'test/lib-close-shared.test.mjs test/doc-escape.mjs",'
must "$HQ" stage3/package-lock.json '"resolved": "https://registry.npmjs.org/express-rate-limit/-/express-rate-limit-8.7.0.tgz",'
must "$HQ" stage3/package-lock.json '"integrity": "sha512-hOwV7WOxXfjRpAM1DSJWZDXx3GhplwD8IfwuwvogD8i1Qnkgosw/H45s4ZnFAUHDAhPjlY9hLBvJhKmGMyY26g==",'
must "$HQ" stage3/package-lock.json '"node_modules/express-rate-limit/node_modules/debug": {'
must "$HQ" stage3/package-lock.json '"integrity": "sha512-RGwwWnwQvkVfavKVt22FGLw+xYSdzARwm0ru6DhTVA3umU5hZc28V3kO4stgYryrTlLpuvgI9GiijltAjNbcqA==",'
mustnot "$HQ" stage3/package-lock.json 'debug-4.4.2.tgz'
# tests.yml (d05cf11)
must "$HQ" .github/workflows/tests.yml '  contents: read'
mustnot "$ANCHOR_MAIN" .github/workflows/tests.yml 'permissions'
[ "$(q show "${HQ}:.github/workflows/tests.yml" | grep -c '^permissions:')" = "1" ] || { echo "REFUSING: tests.yml at the head does not carry exactly one top-level permissions block" >&2; exit 74; }
# Test cells.
wantn "$ANCHOR_MAIN" quote-engine.test.mjs 69
wantn "$HQ" quote-engine.test.mjs 69
wantn "$ANCHOR_MAIN" stage3/test/server.test.mjs 101
wantn "$HQ" stage3/test/server.test.mjs 106
wantn "$HQ" stage3/test/doc-escape.mjs 2
must "$HQ" stage3/test/server.test.mjs 'test("#6: a ~250 KB pathological email (just under the 256 KB body limit) is refused quickly, not after seconds of regex", async () => {'
must "$HQ" stage3/test/server.test.mjs 'test("#6: the email shape check still takes real addresses and refuses the malformed", async () => {'
must "$HQ" stage3/test/server.test.mjs 'test("#12-#14: one source gets 300 page loads per 10 min across /, /login and the module, then 429 with Retry-After", async () => {'
must "$HQ" stage3/test/server.test.mjs 'test("#12-#14: another source is unaffected, and forging X-Forwarded-For entries to the left does not dodge it", async () => {'
must "$HQ" stage3/test/server.test.mjs 'test("#12-#14: PAGE_RATE_LIMIT_PER_10_MIN is validated at boot like the OTP budgets", () => {'
must "$HQ" stage3/test/server.test.mjs 'for (let i = 1; i <= 100; i++) statuses.push((await b.ask(`junk${i}@x.example`)).status);'
must "$ANCHOR_MAIN" stage3/test/server.test.mjs 'for (let i = 1; i <= 100; i++) statuses.push((await b.ask(`junk${i}@@x.example`)).status);'
must "$HQ" stage3/test/phone-layout.mjs "const WIDE_SANS = ':root { --sans: Verdana, \"DejaVu Sans\", sans-serif; }';"
mustnot "$HQ" stage3/test/phone-layout.mjs '--mono:'
# WRONG (g): the stale comment the brief names.
must "$HQ" stage3/lib/sendFailure.js 'junk@@x.example passes the'
# Unchanged blobs.
for F in stage3/lib/xlsx.js stage3/lib/pdf.js stage3/lib/store.js stage3/lib/mail.js stage3/lib/sendFailure.js stage3/strip.js stage3/login.html \
         stage3/Dockerfile .dockerignore quote-engine.test.mjs stage3/test/print-fit.mjs stage3/test/xlsx-parity.mjs BACKLOG.md CLAUDE.md \
         HANDOVER/02-business-rules.md; do
  B0="$(blob "$ANCHOR_MAIN" "$F")"
  [ -n "$B0" ] && [ "$(blob "$HQ" "$F")" = "$B0" ] || { echo "REFUSING: $F differs between main and the head — the brief says it is carried unchanged" >&2; exit 74; }
done
must "$HQ" stage3/Dockerfile 'FROM node:20-bookworm-slim'
[ "$(q ls-tree -r --name-only "$HQ" .github)" = ".github/workflows/tests.yml" ] || { echo "REFUSING: .github at the head holds other than tests.yml — the brief's §N9 reading is wrong" >&2; exit 74; }
for T in 'pricing-pack:' 'stage3-server:' 'store-azurite:' 'print-fit:' 'xlsx-parity:'; do must "$HQ" .github/workflows/tests.yml "  $T"; done
[ "$(q show "${HQ}:.github/workflows/tests.yml" | awk '/^jobs:/{f=1;next} f && /^  [a-z0-9-]+:$/{n++} END{print n+0}')" = "5" ] || { echo "REFUSING: tests.yml does not carry exactly five jobs" >&2; exit 74; }
for T in 'npm ci --offline --ignore-scripts' 'entry by entry' 'never npm audit'; do
  grep -qiF "$T" "$BRIEF" || { echo "REFUSING: brief lacks the dependency rule '$T'" >&2; exit 63; }
  printf '%s\n' "$PROMPT" | grep -qiF -- "$T" || { echo "REFUSING: prompt lacks the dependency rule '$T'" >&2; exit 63; }
done

# 31 — the READY is on disk, names the pinned heads and its HOLDS, and its NOT TESTED lines are carried verbatim; sources on disk.
[ -s "$READY" ] || { echo "REFUSING: the READY mail is not on disk: $READY" >&2; exit 31; }
for T in "Branch fix/qq-quality-round-2026-10-13 @ ${H7}, off main ${MAINH:0:7}" 'READY FOR QA (tier-1 weight, one gate): QuickQuote quality round, PR #6.' \
         'HOLDS (state, unchanged): local QQ main 8b29136 unpushed' 'Rollback image v0.6.1-tool2.33-986f7b8 untouched' \
         'express-rate-limit 8.7.0, pinned exactly, published 2026-08-29T00:49:51Z' 'alerts/N/instances?ref=refs/pull/6/merge is empty for each'; do
  grep -qF -- "$T" "$READY" || { echo "REFUSING: $READY does not carry '$T'" >&2; exit 31; }
done
NT="$(awk 'f&&!/^- /{exit} f{print;next} /^NOT TESTED/{f=1;print}' "$READY")"
[ -n "$NT" ] || { echo "REFUSING: $READY carries no NOT TESTED block" >&2; exit 31; }
while IFS= read -r L; do
  [ -n "$L" ] || continue
  grep -qxF -- "$L" "$BRIEF" || { echo "REFUSING: the brief does not carry this NOT TESTED line of the READY verbatim: $L" >&2; exit 31; }
done <<< "$NT"
for T in 'QQQR NOT TESTED' 'C-17' 'quickquote-ci-red-codeql-14-1013' 'ROUND 1' 'GUARD' 'express-rate-limit' '8.7.0' 'registry.npmjs.org' \
         '2026-10-13_vision-qq-quality-round-READY-mail.txt' 'WRONG (a)' 'WRONG (b)' 'WRONG (c)' 'WRONG (d)' 'WRONG (f)' 'WRONG (g)' \
         'refs/pull/3/head' 'refs/pull/999/merge' 'NOT MEASURABLE' 'hpasqqacr' 'RELAYED' 'GH-API-LEG' 'D1' 'D2' 'D3' 'D4'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: the brief does not carry '$T'" >&2; exit 31; }
done
for R in 'R1: ' 'R2: ' 'R3: ' 'R4: ' 'R5: ' 'R6: ' 'R7: ' 'R8: ' 'R9: ' 'R10: '; do
  grep -qF -- "- $R" "$BRIEF" || { echo "REFUSING: the brief does not carry Tuesday's ruling '$R' as a ruling line" >&2; exit 31; }
done
[ -s "$CLAR" ] || { echo "REFUSING: Vision CLARIFICATIONS.md absent: $CLAR" >&2; exit 31; }
grep -qF '**C-17.' "$CLAR" || { echo "REFUSING: $CLAR lacks C-17" >&2; exit 31; }
for T in 'quickquote-ci-red-codeql-14-1013' 'Commission a fix round now' 'never dismissed by a seat' 'Not covered: publishing or deploying any QuickQuote version'; do
  grep -qF -- "$T" "$CLAR" || { echo "REFUSING: CLARIFICATIONS C-17 does not carry '$T' — the ruling the brief quotes is not on disk" >&2; exit 31; }
done
grep -qF '**C-18.' "$CLAR" && echo "NOTE: Vision CLARIFICATIONS now has a C-18 — the brief says C-01..C-17; read it before launch" >&2
[ -s "$G16_REPORT" ] || { echo "REFUSING: gate 16's report is absent: $G16_REPORT" >&2; exit 31; }
grep -qF 'QQCAD @ `9bd21c0ef142cecc0dc06c6eabd0df1b2aeba63e`' "$G16_REPORT" && grep -qF '**GO WITH FINDINGS**' "$G16_REPORT" \
  || { echo "REFUSING: gate 16's report does not carry QQCAD's GO WITH FINDINGS at 9bd21c0" >&2; exit 31; }
[ -s "$G9_REPORT" ] || { echo "REFUSING: gate 9's report is absent: $G9_REPORT" >&2; exit 31; }
grep -qF 'QQPURGE @ ac74111 GO' "$G9_REPORT" || { echo "REFUSING: gate 9's report does not carry QQPURGE's GO at ac74111" >&2; exit 31; }
[ -s "$G8_REPORT" ] || { echo "REFUSING: gate 8's report is absent: $G8_REPORT" >&2; exit 31; }
for D in "$G8_DIR" "$G9_DIR" "$G16_DIR"; do
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
for H in qa-run.py qa-g16-lib.mjs qa-harness-g16-shots.mjs qa-harness-g16-n2.mjs qa-g16-workbook.cjs qa-netlog-scan.py g16-mutate.py g16-run-suites.sh \
         tapsets.py lockcmp.py lockwalk.py qa-chrome-egressblock.sh qa-chrome-census.py qa-egress-posctl.mjs qa-floorcount.py qa-harness-floorctl.mjs mktree-qq.sh; do
  [ -s "$G16_TOOLS/$H" ] || { echo "REFUSING: gate 16's tool $H is not on disk — the brief names it" >&2; exit 31; }
  grep -qF -- "$H" "$BRIEF" || { echo "REFUSING: the brief does not name gate 16's tool $H" >&2; exit 31; }
done

# 39 — the floor instrument is on disk and named.
[ -s "$G8_FLOOR" ] || { echo "REFUSING: gate 8's floor instrument missing: $G8_FLOOR" >&2; exit 39; }
[ -s "$G16_TOOLS/qa-floorcount.py" ] || { echo "REFUSING: gate 16's floor instrument copy missing" >&2; exit 39; }
grep -qF 'qa-floorcount.py' "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument qa-floorcount.py" >&2; exit 39; }

# 10 / 17 — report path named in both; no stale report.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

# 12 — tier declared in both, at the pinned head.
grep -qE "^- \*\*QQQR\*\* at \`${H7}\` — \*\*TIER 1" "$BRIEF" || { echo "REFUSING: brief does not declare QQQR at \`$H7\` TIER 1" >&2; exit 12; }
case "$PROMPT" in *"QQQR (TIER 1"*) ;; *) echo "REFUSING: prompt does not declare: QQQR (TIER 1" >&2; exit 12 ;; esac

# 78 — the commission's requirements, in both.
for T in 'TIER 1' 'ROUND 1' 'C-17' 'quickquote-ci-red-codeql-14-1013' 'GO WITH FINDINGS' 'NO GO' 'SETS, NOT COUNTS' 'red at base' 'GUARD' \
         'f84f12f' 'd05cf11' '537d672' '1e1d78d' '0b8bbb1' 'd030674' '108bbb4' 'express-rate-limit' '8.7.0' '429' 'healthz' 'X-Forwarded-For' \
         'Retry-After' 'ReDoS' 'byte' 'esc(' '481' '520' '543' '1280' 'wide' 'mono' 'BOTH builds' 'file://' 'hosted build' 'screenshots' \
         'refs/pull/3/head' 'refs/pull/6/merge' 'NOT MEASURABLE' 'dismiss' 'RELAYED' 'hpasqqacr' 'NODE20-LEG' 'GH-API-LEG' 'egress-block' \
         'puppeteer-core' 'node strip.js' 'test:print' 'test:xlsx' 'quote-engine.test.mjs' 'node --check' 'VOID' 'Claude in Chrome' 'HPAM word' \
         'registry.npmjs.org' '8b29136' 'qq-108bbb4' 'qq-986f7b8' 'v0.6.1-tool2.33-986f7b8' 'createApp()' 'WEBSITE_SITE_NAME'; do
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

# 82 — THE MODEL RULE (Kam 2026-09-30 09:07, card (b); R9), in brief and prompt, per session, never "Switch automatically".
for T in "$STATUS_SUBJ" "$PARK_LINE" 'classifier-stops.txt' 'Switch automatically' 'Opus 4.8' 'PER SESSION' 'which rows ran on which model' 'Opus 5.5'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks THE MODEL RULE fragment '$T'" >&2; exit 82; }
  case "$(printf '%s' "$PROMPT" | tr '[:upper:]' '[:lower:]')" in *"$(printf '%s' "$T" | tr '[:upper:]' '[:lower:]')"*) ;; *) echo "REFUSING: prompt lacks THE MODEL RULE fragment '$T'" >&2; exit 82 ;; esac
done
grep -qF '## THE MODEL RULE' "$BRIEF" || { echo "REFUSING: brief lacks the THE MODEL RULE section" >&2; exit 82; }

# 19 — words the prompt must carry (% is a space) and the brief's sections.
WORDS="merge-tree NOT%TESTED env%-i bash 108bbb4 d030674 work-g17 FOREGROUND MEASURED%AT%RUNTIME PROBED READ%ONLY start%/%mid%/%end CI VOID node%--check"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## Charter' '^## RULED BY KAM, AND SETTLED' '^## PRIOR ROUND' '^PRIOR ROUND: ' 'ITS REPORT IS ON DISK AT:' '^## PIN' \
         '^## WRONG OR UNVERIFIABLE' '^## THE READY' '^## 2a. LEGITIMATE SHAPES' '^## N1. ' '^## N2. ' '^## N3. ' '^## N4. ' '^## N5. ' '^## N6. ' \
         '^## N7. ' '^## N8. ' '^## N9. ' '^## N10. ' '^## 12. The merge' '^## 13. FLOOR' '^### HELD' '^## THE MODEL RULE' "^## TUESDAY'S RULINGS AT STAMP" \
         '^## 14. Output' '^PROVENANCE:'; do
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
for T in 'EXCLUSIVE' 'work-g17'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the tree-exclusivity rule '$T'" >&2; exit 61; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the tree-exclusivity rule '$T'" >&2; exit 61 ;; esac
done
for T in '4848' '8080' '47787' 'env -i' 'AGENTMAIL_API_KEY' 'AGENTMAIL_INBOX' 'no jest lock' 'TABLES_CONNECTION_STRING' 'HPAM_WORD' 'ADVANCED_UNLOCK_SECRET' \
         'PUPPETEER_EXECUTABLE_PATH' 'GoogleUpdater' 'chrome_crashpad_handler' 'net-log' 'GH_TOKEN'; do
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

# 44 — REPURPOSED (gate 16): the browser leg's instrument, a local Google Chrome, is installed. The launcher never starts it.
[ -x "$CHROME_BIN" ] || { echo "REFUSING: no local Google Chrome at $CHROME_BIN — the browser leg (brief §N5, §N7) would be NOT RUN" >&2; exit 44; }

# ---- the coordinator's to-do guards (46, 41, 32): run LAST, reported TOGETHER, exit with the first pending code.
PENDING=''
pend() { [ -n "$PENDING" ] || PENDING="$1"; shift; echo "REFUSING: $*" >&2; }

# 46 (NEW) — the GitHub read leg as Tuesday sets it (decision D1).
GHLEG="$(sed -n 's/^GH-API-LEG: \([A-Z-]*\)[[:space:]]*$/\1/p' "$BRIEF" | head -1)"
case "$GHLEG" in
  READ-ONLY-VISION-TOKEN)
    [ -d "$VSP_GH" ] || { echo "REFUSING: GH-API-LEG is READ-ONLY-VISION-TOKEN but $VSP_GH is not a directory" >&2; exit 46; }
    command -v gh >/dev/null 2>&1 || { echo "REFUSING: GH-API-LEG is READ-ONLY-VISION-TOKEN but no gh binary is on PATH" >&2; exit 46; } ;;
  NOT-RUN) ;;
  "$PH_GHLEG") pend 46 "the brief's GH-API-LEG line is still ${PH_GHLEG} — Tuesday sets READ-ONLY-VISION-TOKEN or NOT-RUN (decision D1) before launch" ;;
  *) echo "REFUSING: the brief's GH-API-LEG line reads '${GHLEG:-<missing>}' — it must be exactly READ-ONLY-VISION-TOKEN or NOT-RUN" >&2; exit 46 ;;
esac

# 41 — the answer route exists (Tuesday adds 'QA/Vision-gate17|tuesday-agent@agentmail.to|no' at launch).
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" \
  || pend 41 "no '${ROUTE_NAME}|tuesday-agent@agentmail.to|…' line in $ROUTING — answers to the gate would have no route. Add it (pattern: the QA/Vision-gate16 line) before launch."

# 32 — the coordinator stamps the self-check (line AND note), D1-D4 and every @STAMP@.
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  pend 32 "the brief still carries ${PH_STAMP} (Self-check line and note, or the RULED lines of D1-D4) — the coordinator re-reads end-to-end and stamps all of them before launch"
fi

if [ -n "$PENDING" ]; then
  echo "guards pass (40 6 9 7 8 18 22 23 74 63 31 39 10 17 12 78 13 14 15 20 70 82 19 24 53 60 61 62 64 69 75 38 45 44); coordinator to-do pending (46 41 32 as listed above); exiting $PENDING." >&2
  exit "$PENDING"
fi

PIN_BLOCK="$(printf 'PINNED HEADS — verified by the launcher at %s (cat-file; base 108bbb4, 0 behind; ancestor and merge-base with MAIN; not-already-on-main; commit count 6; exact chain, single parents, no merges; 108bbb4 <- e408904 + 1270b71; 9bd21c0 on main; main pinned EXACTLY; refs/pull/6/head = head; the exact index.html delta by hash; git ls-remote origin for both rows):\n' "$PIN_TS"
  printf '%s\n' "$PIN" | awk -F'\t' '{ printf "  %-7s %-11s %-34s %s  base %s  commits %s\n", $1, $2, $3, $4, ($5=="-"?"-":substr($5,1,12)), $6 }'
  printf '  Main: pinned %s (exact; a move refuses). PR #%s: refs/pull/%s/head = %s; refs/pull/%s/merge = %s (GitHub test merge, not in the local object store)\n' "${MAINH:0:12}" "$PR_NUM" "$PR_NUM" "${HQ:0:12}" "$PR_NUM" "${PR_MERGE_NOW:-<absent>}"
  printf '  Chain: f84f12f (tier 2) d05cf11 (tier 2) 537d672 (tier 1) 1e1d78d (tier 1, v2.35) 0b8bbb1 (tier 1) d030674 (tier 2, user-visible)\n'
  printf '  index.html delta (old-side hunks %s): +13/-5, sha256 add %s / del %s; no new colour/token/style\n' "$IDX_HUNKS" "${IDX_ADD_SHA:0:12}" "${IDX_DEL_SHA:0:12}"
  printf '  Positive controls: base 108bbb4 (no limiter, the old email regex, unescaped src, no wrap above 480 px); gate 16 head 9bd21c0 on main\n'
  printf 'NODE20-LEG, as set in the brief: %s\n' "$NODE20"
  printf 'GH-API-LEG, as set in the brief: %s\n' "$GHLEG")"

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  printf '%s\n' "$PIN_BLOCK"
  echo "  PIN parsed, two rows, no placeholder, head = d030674 (40); every sha a local commit (6); main = 108bbb4 exactly (9)"
  echo "  base 108bbb4, count 6, 0 behind (7 8); exact chain, parents pinned, no merges, 108bbb4 parents, 9bd21c0 on main (9); origin re-read $PIN_TS, both rows + refs/pull/6/head (18)"
  echo "  file set 8 + per-commit sets (22); numstat, index.html delta by hash, hunk map, no new colour/token (23)"
  echo "  round content, test( 69/101->106/2, unchanged blobs, lockfile pins, tests.yml permissions + 5 jobs, stale sendFailure comment (74); deps (63)"
  echo "  READY lines + HOLDS + NOT TESTED verbatim, R1-R10, C-17, gate 8 + 9 + 16 reports and tools (31); floor (39); report absent (17); tier (12); commission (78)"
  echo "  directive/brief/placeholders/mail/key/questions/safety (13 14 15 20 70); MODEL RULE (82); words + sections (19); no server path (24); standing rules (53 60 61 62 64 69 75); seats $NEG_SEATS (38); NODE20 $NODE20 (45); Chrome (44); GH $GHLEG (46); route $ROUTE_NAME (41); stamped (32)"
  echo "  model: claude-opus-5-5 at exec"
  exit 0
fi

# 11 — no inherited identity: AZURE_CONFIG_DIR always EMPTY; GH_CONFIG_DIR EMPTY unless GH-API-LEG = READ-ONLY-VISION-TOKEN (then Vision's, behind a GET-only shim).
ID_TMP="$(mktemp -d "${TMPDIR:-/tmp}/qa-vision-gate17-id.XXXXXX")" || { echo "REFUSING: cannot create the empty identity dir" >&2; exit 11; }
mkdir -p "$ID_TMP/azure-empty" "$ID_TMP/gh-empty" || { echo "REFUSING: cannot create the empty identity dirs under $ID_TMP" >&2; exit 11; }
{ [ -z "$(ls -A "$ID_TMP/azure-empty")" ] && [ -z "$(ls -A "$ID_TMP/gh-empty")" ]; } || { echo "REFUSING: the identity dirs under $ID_TMP are not empty" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_TMP/azure-empty"
export GH_CONFIG_DIR="$ID_TMP/gh-empty"
if [ "$GHLEG" = "READ-ONLY-VISION-TOKEN" ]; then
  QA_REAL_GH="$(command -v gh)" || { echo "REFUSING: gh vanished between guard 46 and launch" >&2; exit 11; }
  export QA_REAL_GH
  mkdir -p "$ID_TMP/bin" || { echo "REFUSING: cannot create the gh shim dir" >&2; exit 11; }
  cat > "$ID_TMP/bin/gh" <<'SHIM'
#!/bin/bash
# gate-17 GET-only gh shim (written by launch_qa_vision_gate17.sh; GH-API-LEG = READ-ONLY-VISION-TOKEN). Brief §HELD binds the rest.
REAL="${QA_REAL_GH:?gh shim: QA_REAL_GH unset}"
[ "${1:-}" = "api" ] || { echo "gh shim: only 'gh api' GET reads are allowed in Vision gate 17 (got: ${1:-<none>})" >&2; exit 64; }
shift
for a in "$@"; do
  case "$a" in
    -X|-X*|--method|--method=*|-f|-f*|-F|-F*|--field|--field=*|--raw-field|--raw-field=*|--input|--input=*)
      echo "gh shim: '$a' refused — GET reads only" >&2; exit 64 ;;
    graphql|/graphql|*/graphql) echo "gh shim: graphql refused" >&2; exit 64 ;;
  esac
done
exec "$REAL" api "$@"
SHIM
  chmod 0755 "$ID_TMP/bin/gh" || { echo "REFUSING: cannot make the gh shim executable" >&2; exit 11; }
  export GH_CONFIG_DIR="$VSP_GH"
  export PATH="$ID_TMP/bin:$PATH"
  [ "$(command -v gh)" = "$ID_TMP/bin/gh" ] || { echo "REFUSING: the gh shim is not first on PATH" >&2; exit 11; }
fi
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"
# 64 (cont.) — nothing a product process could use to reach a real provider is inherited from this shell.
unset DATABASE_URL TEST_DATABASE_URL AGENTMAIL_API_KEY AGENTMAIL_INBOX ACS_CONNECTION_STRING ACS_EMAIL_CONNECTION_STRING ACS_EMAIL_SENDER \
      MAIL_SENDER TABLES_CONNECTION_STRING AZURE_BACKUP_CONN_STR SESSION_SECRET HPAM_WORD ADVANCED_UNLOCK_SECRET SALES_COPY_EMAIL \
      FEEDBACK_NOTIFY_EMAIL FEEDBACK_NOTIFY_EMAILS APPROVALS_INBOX NTFY_TOPIC NTFY_SERVER LEAD_BOT_API_KEY WEBSITE_SITE_NAME COORDINATOR_SECRET \
      PORT NODE_ENV PUPPETEER_EXECUTABLE_PATH PAGE_RATE_LIMIT_PER_10_MIN OTP_IP_BUDGET_PER_HOUR OTP_GLOBAL_BUDGET_PER_HOUR GH_TOKEN GITHUB_TOKEN \
      GH_ENTERPRISE_TOKEN GITHUB_ENTERPRISE_TOKEN
echo "identity: AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR (empty) GH_CONFIG_DIR=$GH_CONFIG_DIR (GH-API-LEG $GHLEG) CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR" >&2

PROMPT="$PROMPT

$PIN_BLOCK"
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model claude-opus-5-5 "$PROMPT"
