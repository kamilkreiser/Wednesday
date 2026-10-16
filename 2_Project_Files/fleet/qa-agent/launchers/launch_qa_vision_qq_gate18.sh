#!/bin/bash
# launch_qa_vision_qq_gate18.sh — cross-project QA agent, ONE gate (Vision gate 18; drafted 2026-10-16 ~12:58-13:4x AEDT by a read-only drafting
# agent for Tuesday, from launch_qa_vision_gate17.sh + the NexusAI batch-23 launcher's Laptop-DEV re-base, model read and live seat derivation).
# Datasec/Vision_Sales_Portal, QuickQuote repo: ONE target, TIER 1 (the shipped build image + the quote PDF output), ONE verdict:
#   QQPB  fix/qq-puppeteer-25-2026-09-22  PR #8 @ 4d6ed6e  puppeteer-core 23 -> 25.0.2, stage3 image node 20 -> 22   TIER 1, round 1 (C-19)
#
# Main is e4ce536 (merge of PR #7: 3dd15bc + 5ad37f1). QQPB = 3d0167e (parent 47eb533) -> 0d45100 (= 3d0167e + 51e9286, gate 4's P5B head)
# -> 4d6ed6e (= 0d45100 + e4ce536). 3 ahead, 0 behind. THIS GATE PINS MAIN EXACTLY: a moved main REFUSES. refs/pull/8/head must equal the head.
#
# THE HEADS LIVE IN ONE PLACE: the brief's PIN-HEADS table. This launcher PARSES it, refuses any placeholder, verifies every row against the
# object store and against origin by `git ls-remote` NOW, and appends the verified table to the agent's prompt.
#
# NEW MACHINE: every path is on /Volumes/Laptop-DEV (TUESDAY, the Vision project and its QuickQuote repo, Testing Agent MAIN, the AgentMail .env,
# the cockpit) EXCEPT gate 4 / gate 17's reports and instruments, which exist ONLY on the T9 and are READ there. The T9 QuickQuote repo is STALE.
#
# PRODUCTION IS LIVE for this project (hpas-quickquote / hpasqqacr; datasec-sales-portal-rg). This gate BUILDS AND RUNS LOCAL IMAGES (qa-g18-* only,
# never pushed) — docker is in scope for the first time on a Vision gate (C-19; brief §13.5). Findings only.
#
# GUARDS — the gate-17 numbering kept where the guard survives; changes:
#   - PIN: two rows (MAIN-Q e4ce536, QQPB 4d6ed6e base e4ce536 x3). Exact chain with its two merges pinned by parents (gate 17 had none).
#   - 22/23: file set 5 + numstat; the ONLY non-comment changes are the FROM line, the puppeteer-core line, and the two require lines.
#   - 74: lock pins (puppeteer-core 25.0.2 integrity, extract-zip absent at head / present at base), unchanged blobs, Dockerfile body.
#   - 31: READY lines + its NOT TESTED verbatim; C-19 at source; gate 4 + gate 17 reports and tools on the T9.
#   - MODEL: read from Tuesday's models_latest.json (levels.opus.model_id), REFUSED unless claude-opus-5-5 (batch-23 pattern).
#   - 38R: negative-control seats DERIVED live from the cockpit panes (tuesday + the Datasec/Vision_Sales_Portal builder + live QA/* + fleet-monitor).
#   - 45D (replaces gate 17's NODE20-LEG): docker answers; buildx lists linux/amd64; no qa-g18-* image/container yet; foreign objects NOTEd.
#   - 46: GH-API-LEG (READ-ONLY-VISION-TOKEN | NOT-RUN). 47 (NEW): AZ-READ-LEG (TUESDAY-READS | GATE-SHIM | NOT-RUN) + its AZ-PRE-READ line.
#   - 86: no live QA/Vision-gate18 pane already.
#   - 46 47 41 32 are the coordinator's to-do guards: run LAST, reported TOGETHER, exit with the first pending code.
#
# LAUNCH IT IN A TMUX PANE:
#   /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add 'QA/Vision-gate18' "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_vision_qq_gate18.sh'"
#   NEVER nohup, never bare from a seat's shell.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# --check is READ-ONLY: git read verbs (cat-file, rev-parse, merge-base, log, rev-list, diff, show, ls-tree, ls-remote); docker version / buildx ls /
# images / ps (read); tmux list-panes; ps; grep/python over files. It creates no identity dir, writes nothing and starts no claude.
# Usage: launch_qa_vision_qq_gate18.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..99 a guard refused
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
PH_DECIDE='TUESDAY''-DECIDES'

QA_DIR='/Volumes/Laptop-DEV/!CODING/Testing Agent MAIN'
TUE='/Volumes/Laptop-DEV/TUESDAY'
BRIEFS="$TUE/2_Project_Files/fleet/qa-agent/briefs"
BRIEF="$BRIEFS/2026-10-16_vision-gate18-qq-pr8-puppeteer25.md"
READY="$BRIEFS/2026-10-16_vision-qq-pr8-READY-mail.txt"
CHARTER="$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"
MODELS_JSON="$TUE/0_Brain/dashboard/data/models_latest.json"
MODEL_PIN='claude-opus-5-5'
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
VSP='/Volumes/Laptop-DEV/!CODING/Datasec/Vision_Sales_Portal'
Q_REPO="$VSP/Quoting Tool/hpas-quoting-tool"
VSP_GH="$VSP/4_Credentials/.gh-config"
VSP_AZ="$VSP/4_Credentials/.azure"
CLAR="$VSP/1_Project_Definition/CLARIFICATIONS.md"
REPORTS="$QA_DIR/projects/vision/reports"
T9_REPORTS='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports'
G4_DIR="$T9_REPORTS/2026-09-22-vision-qq-gate4"
G4_REPORT="$G4_DIR/report.md"
G4_P5B="$G4_DIR/sections/P5B.md"
G17_DIR="$T9_REPORTS/2026-10-13-vision-gate17-qq-quality-round"
G17_REPORT="$G17_DIR/report.md"
G17_TOOLS="$G17_DIR/evidence/tools"
REPORT="$REPORTS/2026-10-16-vision-gate18-qq-pr8-puppeteer25/report.md"
ROUTE_NAME='QA/Vision-gate18'
BUILDER_PANE='Datasec/Vision_Sales_Portal'
CHROME_BIN='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
PR_NUM='8'
PR_MERGE_SEEN='80747c81c343e4273918dc2062bcb87a35853cf2'     # refs/pull/8/merge at ~13:00 (GitHub's test merge; NOTE only)
# Gated anchors (not heads).
ANCHOR_MAIN='e4ce5367761e03db982189a3f21758aa06714a85'     # QuickQuote main = merge of PR #7 (C-18)
ANCHOR_MAINP='3dd15bcc09862047f6500e1813901edd8a686888 5ad37f1a3224c8fb3fddf8ad71dd144db62e9655'
ANCHOR_G17='d030674694279be3159d67de4a10f220ea6b8335'      # gate 17's QQQR GO-WITH-FINDINGS head (on main)
C1='3d0167ebe1909a301ac881c30f55f717c7801dd3'; C1P='47eb533034108c5c92d6b36af44554528ffc71ec'
C2='0d451004c746608922ddf874b48ce0f19048bf20'; C2P="$C1 51e92867930efd4c98b28dc5d95baf82219b3edb"   # gate 4's P5B head
HQ_EXPECT='4d6ed6ef403ef8962ded8211b76c3c6809bbb8c3'; HQP="$C2 $ANCHOR_MAIN"
HQ_TREE='01bdc924daeafa59879462af5960bc4fa86875d3'
DELTA_FILES='stage3/Dockerfile stage3/package-lock.json stage3/package.json stage3/test/fixtures/hang-close.cjs stage3/test/lib-close-shared.test.mjs'
NUMSTAT_EXPECT='4/1/stage3/Dockerfile 76/518/stage3/package-lock.json 1/1/stage3/package.json 3/1/stage3/test/fixtures/hang-close.cjs 1/1/stage3/test/lib-close-shared.test.mjs '
DKF_NCL_EXPECT='-FROM node:20-bookworm-slim
+FROM node:22-bookworm-slim'
PKG_U0_EXPECT='-    "puppeteer-core": "^23.5.0"
+    "puppeteer-core": "^25.0.2"'
FIX_NCL_EXPECT='-const { CdpBrowser } = require("puppeteer-core/lib/cjs/puppeteer/cdp/Browser.js");
+const { CdpBrowser } = require("puppeteer-core/internal/cdp/Browser.js");
-const { CdpBrowser } = require("puppeteer-core/lib/cjs/puppeteer/cdp/Browser.js");
+const { CdpBrowser } = require("puppeteer-core/internal/cdp/Browser.js");'

SUBJECT_STEM='[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 18'
QUESTION_SUBJ='[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>'
ANSWER_PREFIX='[Tuesday -> QA/Vision-gate18] ANSWER'
STATUS_SUBJ='[QA/Datasec-Vision -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch'
PARK_LINE='PARKED: flagged — awaiting the Opus 4.8 switch'

q() { git --no-optional-locks -C "$Q_REPO" "$@"; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE gate (Vision gate 18) on Datasec/Vision_Sales_Portal, in the QUICKQUOTE repo: ONE target, TIER 1 (the shipped build image + the quote PDF output), ONE verdict, GO / GO WITH FINDINGS / NO GO. QuickQuote main is e4ce536 (the merge of PR #7). The target QQPB (TIER 1; ROUND 1 of PR #8) is QuickQuote PR #8, branch fix/qq-puppeteer-25-2026-09-22 at 4d6ed6e: puppeteer-core 23.11.1 -> 25.0.2 and the stage3 image FROM node:20-bookworm-slim -> node:22-bookworm-slim, ruled by Kam as C-19 (card quickquote-decision14-puppeteer25-node22-1016 = b, 2026-10-16 12:41:19 AEDT, "Build the puppeteer 25 + node 22 change now"). The shipping delta is git diff e4ce536 4d6ed6e: five files (the Dockerfile's FROM line, package.json's puppeteer-core line, the lockfile, and two test files whose require of puppeteer's CdpBrowser moved from lib/cjs to the exported internal/ path). The page, the hosted server module, lib/pdf.js, lib/xlsx.js and strip.js are byte-identical at base and head: everything that can differ is the RUNTIME. This machine is Kam's Mac mini, working volume /Volumes/Laptop-DEV; the T9 drive /Volumes/KK_T9_External_HDD is also mounted and holds the earlier gates' reports and instruments (read there, never write there).

READ YOUR COMMISSION FIRST, whole: /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-16_vision-gate18-qq-pr8-puppeteer25.md
Then read the charter it names, the Vision CLARIFICATIONS (C-01..C-19; C-19 is Kam's ruling for this target; publishing the new runtime, any ACR push and any deploy are NOT covered), the project's CLAUDE.md (/Volumes/Laptop-DEV/!CODING/Datasec/Vision_Sales_Portal/CLAUDE.md, its QuickQuote section; its deploy commands are not for you), the QuickQuote repo's own CLAUDE.md at the head (git show; its publish lines are not for you), the builder's READY mail under test, read WHOLE (/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-16_vision-qq-pr8-READY-mail.txt), gate 4's report on the T9 /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-22-vision-qq-gate4 (sections/P5B.md whole: the branch's previous gate, "image build NOT RUN; Node 22 NOT TESTED"), and gate 17's report on the T9 /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-10-13-vision-gate17-qq-quality-round (the last QuickQuote gate; evidence/tools/ holds the instruments you copy). Every builder statement is a CLAIM, never evidence. RE-DERIVE every red, every mutant, every suite set, every image and every comparison yourself. Verify every PRIOR WORK claim against git history and gates 4 and 17's evidence, never against the brief. The brief's WRONG list, MODEL RULE and TUESDAY'S RULINGS (R1-R7 and the stamped D1-D4) are stamped: apply them, do not re-rule them.

WHAT THE BRIEF REQUIRES, in short (the brief is the authority):
(1) THE HOST SUITES at the head 4d6ed6e and at base e4ce536, same session, as SETS, NOT COUNTS: the root pricing pack (node --test quote-engine.test.mjs), and in stage3/: npm test, npm run test:print, npm run test:xlsx. npm ci --offline --ignore-scripts only, the lockfile proven entry by entry (lockcmp.py AND lockwalk.py); npm ls --all. The fixture red-first: the two test files reverted to their base blobs on a fresh head tree must fail test:print at load, quoted. npm audit --omit=dev --json at head and base (the brief's network exception NX-2): head 0 of every severity.
(2) THE IMAGES, the core of this gate: YOU build BOTH the base image (e4ce536) and the head image (4d6ed6e) for linux/amd64 from fresh git archive contexts, back to back, --pull --no-cache, tagged qa-g18-* only. The App Service runs linux/amd64 and every image the builder measured was arm64; its amd64 run, its STATUS mail and its qq-evidence-local images are NEVER your evidence and you never touch them. Same build window: record each image's node -v, chromium --version, Debian chromium and font package versions, fc-list hash, base digest and uname -m (x86_64); a cross-image comparison between images whose Chromium or fonts differ is VOID. List what each image ships (/app without node_modules) and prove its node_modules against its lockfile.
(3) IN THE amd64 IMAGES, the suites CI runs, under --network none, as sets base vs head (root for the suites); test:azurite against your OWN Azurite container sharing its network namespace.
(4) THE QUOTE ARTEFACTS FROM A REAL USER PATH, in each amd64 image under --network none as the image's own user: your harness from /qa (read-only bind mount) drives the image's own createApp() export (in-memory store and a capturing stub mail shaped like the repo's server suite, throwaway session and unlock secrets, a frozen clock, never a real secret, never the module's entry point) and the image's own Chromium through the image's own puppeteer-core: sign in with the captured OTP, unlock advanced with the throwaway word, fill the form as a rep, press the page's own email (PDF & XLS) control so the page's collector posts the state. Six shapes: default and advanced x AUD, USD, CAD. Capture the emailed PDF and xlsx, and print the quote light and dark. Compare base image vs head image: text (pdftotext -layout), pixels (pdftoppm -r 100, every page, plain python on PPM — there is no ImageMagick, PIL or numpy), fonts (pdffonts), pages and A4 (pdfinfo), workbook parts (only docProps/core.xml may differ). The server path vs printed page pricing difference and the 7 unknown print-mode fields (pmBoth..cpPct) are PRE-EXISTING (Tuesday's 12:37/12:57 notes): measure them in both images, never call them PR #8's. Look at the head pages yourself.
(5) PUPPETEER INTERNALS AND THE TWO FIXTURES: static grep at both shas and over the head image's /app; at runtime in the head image, log every puppeteer-core file the render path loads and the specifier that loaded it; quote any ExperimentalWarning from require(esm). Prove the stub's CdpBrowser IS the class the renderer's browser is an instance of; mutants G-M1 (the lib-close-shared stub disarmed) and G-M2 (the hang-close fixture disarmed), each on a fresh tree with the tamper asserted landed and node --check rc 0 (a mutant that does not parse is VOID) — say which cells see each, or NONE. The fixtures keep every assertion byte-identical. Show the base image's Node 20 cannot load the head's puppeteer-core (they must ship together).
(6) THE DEPENDENCY CLEAN-UP: extract-zip, yauzl, basic-ftp, proxy-agent absent at the head (host tree and head image), present at base; the 13 changed versions installed as locked; the inert basic-ftp override observed.
(7) NOTHING PUSHED, NOTHING DEPLOYED, LIVE SITE UNCHANGED: your own docker objects and command log prove no push, no login, no registry tag; the Azure side (the live webapp's linuxFxVersion and hpasqqacr's tag list, read-only, before and after) by the brief's AZ-READ-LEG exactly (appended below by the launcher); deploy-on-merge READ ONLY.
(8) CI AND CODEQL on PR #8, READ ONLY, by GH-API-LEG; the PR-side CodeQL zeros are a blind instrument (gate 17's control): say only what they can show, name the post-merge reads (Dependabot #1 #4 fixed, tests.yml on the merge commit).
(9) RUNTIME DRIFT, READ: every puppeteer call the product makes, 23 vs 25, against your installed head tree; MEASURED where (4) measured it.
GH-API-LEG and AZ-READ-LEG (appended below by the launcher as the brief sets them): READ-ONLY-VISION-TOKEN means gh is on your PATH as a GET-only shim over Vision's gh config — gh api GET reads only, never -X/--method, -f/-F/--field/--raw-field/--input or graphql, never a comment, review, label, approval, re-run or dismissal. TUESDAY-READS means you run no az and RELAY Tuesday's AZ-PRE-READ line; GATE-SHIM means az is a shim allowing only account show, webapp config show for hpas-quickquote and acr repository show-tags for hpasqqacr, and an authorisation error is the boundary working — report it, never work around it; NOT-RUN means none. Never open any file under the project's 4_Credentials.

PRODUCTION IS LIVE for this project. NEVER the live QuickQuote (hpas-quickquote, hpas-quickquote-rg, hpasqqacr, its Table Storage, its log workspace) and NEVER the live portal (datasec-sales-portal.azurewebsites.net, datasec-sales-portal-rg): no HTTP request, not even a GET. No az beyond the AZ-READ-LEG; no deploy, no publish, no app-setting change, no ACR build, no registry push. Never the FX hosts (stubbed, blocked, or absent under --network none), never ntfy.sh. Never Claude in Chrome (Kam's own Chrome with his sign-ins). Never type an HPAM word. NETWORK EXCEPTIONS, and only these: NX-1 the image builds' own pulls (Docker Hub node:20-bookworm-slim and node:22-bookworm-slim, Debian apt and the npm registry inside the builds) with every digest recorded; NX-2 npm audit --omit=dev and one curl -s -m 30 https://registry.npmjs.org/puppeteer-core read from your own shell; NX-3 git ls-remote origin; NX-4 gh api GETs if GH-API-LEG allows.

DOCKER DISCIPLINE (new for Vision): only YOUR objects — images tagged qa-g18-*, containers named qa-g18-*, network qa-g18-net if you need one. Never start, stop, remove, re-tag, exec into or run the builder's qq-evidence-local images or containers, any qa-b23-* (the NexusAI gate running beside you), rd846-*, vsp-azurite-*, pc-* or any other foreign object. Never prune anything, never rmi, never docker rm, never docker push, never docker login, no registry host in a tag. Product containers run --network none (the Azurite pair shares one namespace), with no bind mount except your own read-only harness dir at /qa and the one read-only node_modules mount the brief names, never the Docker socket, never --privileged. Your containers are STOPPED and LEFT (no --rm), listed by id; your images are LEFT, listed by id. Every container you call amd64 reads x86_64 from uname -m.

HELD: no merge, no publish, no comment or status on PR #8, no alert dismissal, no mail to any human. TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT on this drive from the object store (git archive into a fresh mktemp -d under projects/vision/work-g18/ in /Volumes/Laptop-DEV/!CODING/Testing Agent MAIN). Each tree is EXCLUSIVE to this gate and to one purpose; never touch any other work directory on either drive. The QuickQuote repo on THIS drive is the only one that holds the head; the T9 copy is stale — never read it. The builder's checkout is LIVE: never read any working tree as evidence; never use the name main in the repo, only the pinned 40-hex shas. Copy gate 17's instruments from the T9 into YOUR evidence/tools on this drive and re-point them (they hard-code work-g17, the gate-17 report folder and the T9 volume); never run from, edit or write into gate 1-17's copies. Never npm install, never npm audit fix, never npx anything not already in the tree. In the repo use ONLY read verbs (show, log, diff, ls-remote, rev-parse, ls-tree, cat-file, grep, merge-base, archive); never fetch, pull, checkout, switch, worktree, commit, stash, reset, clean, gc, branch or for-each-ref. Run git merge-tree --write-tree only from the gate's OWN object dir, or skip it and say so. Findings-only: no writes in the QuickQuote repo, none inside Vision_Sales_Portal, none in gate 1-17's report folders or trees. Never rm: quarantine. Run every loop and every git show <sha>:<path> under bash. Run node strip.js before any lone browser file. CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY: a planted one-pixel and one-word difference must make your PDF comparator report non-zero before its zeros are believed; a control derived from the run it validates is not a control.

FLOOR DISCIPLINE. Vision has no jest lock; never borrow NexusAI's. Never use host ports 4848, 8080 or 47787; host processes take every port from the kernel and bind 127.0.0.1. Every host product process runs under env -i with an explicit allowlist, NODE_ENV never production. Never set AGENTMAIL_API_KEY or AGENTMAIL_INBOX in a product process or a container (with both set, QuickQuote SENDS FOR REAL), nor any real ACS_* or MAIL_SENDER, TABLES_CONNECTION_STRING, SALES_COPY_EMAIL, HPAM_WORD, ADVANCED_UNLOCK_SECRET, SESSION_SECRET, WEBSITE_SITE_NAME, GH_TOKEN or GITHUB_TOKEN; print each product process's and container's env KEY NAMES and assert none is forbidden. NTFY_SERVER=http://ntfy.invalid; never contact ntfy.sh. EGRESS INCLUDING CHROME CHILDREN on the host: every Chrome runs under your copy of the egress-block wrapper as PUPPETEER_EXECUTABLE_PATH; prove the block with its positive control and run the net-log scan at the end; record GoogleUpdater and chrome_crashpad_handler at start and end; reap every Chrome and every app listener by the pid you started. Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid, with the negative-control seats the launcher derived (listed at the end of this prompt) classifying FOREIGN in the same run. A zero is reportable only beside an ATTACHED control that fired in the same window. The box was at load 224 when this gate was drafted: record the load average beside every timing number; a latency result with no load figure is not a measurement.
DEADLINE AND HEARTBEAT: every step has a written DEADLINE built into your runner (there is no timeout binary here) and releases its Chromes, pages, children, app servers, containers (stopped by the id you started, never removed) and temp profiles in a finally. Log a HEARTBEAT line at least every 2 minutes; a step with no heartbeat for 5 minutes is aborted and reported, never waited on. Host deadlines: one page cell 120 s; a whole test:print run 420 s; a whole test:xlsx run 300 s; a whole npm test run 300 s; the root pack 120 s; one mutant arm 420 s. Image deadlines: one amd64 build 2400 s; one arm64 build 900 s; in-container npm test 900 s, test:print 1800 s, test:xlsx 900 s, one render cell 600 s. Nothing above 2400 s. An amd64 row that cannot finish is NOT RUN with the reason and the load, never filled by an arm64 result; under the brief's D4 an amd64 leg NOT RUN makes the verdict PROVISIONAL.

THE MODEL RULE (Kam, live board 2026-09-30 09:07, card (b)): QA gates may switch to Opus 4.8 when flagged by Opus 5.5's safeguards, PER SESSION. You start on Opus 5.5. You run the FULL rows. If one of your responses is stopped by the safeguards: that step is NOT RUN (never re-worded to slip past); write ONE line to evidence/classifier-stops.txt; stop any container and reap any Chrome and app server you started; mail tuesday-agent@agentmail.to with the subject exactly "[QA/Datasec-Vision -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch"; then end your turn with the line "PARKED: flagged — awaiting the Opus 4.8 switch" and wait. Tuesday switches THIS pane's model and taps you by mail. You never answer the model dialog yourself, and nobody ever chooses "Switch automatically". After the switch, resume at the stopped row. The report states which rows ran on which model, with the switch time, and quotes classifier-stops.txt whole.

QUESTIONS: your routing name is QA/Vision-gate18. If you must ask, mail tuesday-agent@agentmail.to with the subject "[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>" and proceed on the safest reading without waiting (the one exception is a safeguards stop, which PARKS you under THE MODEL RULE). Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/Vision-gate18] ANSWER"; read it with your verdict key. Never wednesday-agent@. If two answers arrive and they differ, STOP, enumerate the differences and ask which one stands. If a response is cut off by a safety check, record it and continue with the next item; this is authorised defensive QA of Datasec's own product on loopback. Approval-class items (an ACR push, a deploy, the live site, money, a human) are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your report to: /Volumes/Laptop-DEV/!CODING/Testing Agent MAIN/projects/vision/reports/2026-10-16-vision-gate18-qq-pr8-puppeteer25/report.md
Write its VERDICT and FINDINGS table early and keep it current.

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with a subject beginning exactly:
[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 18: QQPB @ <sha7> <GO | GO WITH FINDINGS | NO GO>
(the sha7 is the pinned head from the verified table below; append PROVISIONAL if the brief's D4 amd64 clause applies). Lead the body with ONE sentence as the brief's section 14 words it (did the head image build and run for linux/amd64; the suites as sets on the host and in the amd64 image vs e4ce536; the server-path PDF, the printed quote light and dark and the workbook identical to the base image's in text and pixels for the six shapes; npm audit --omit=dev at 0; any shipped file reaching puppeteer internals; anything pushed or deployed), then one line each on the image versions table, the stub identity and G-M1/G-M2, require(esm) warnings, the live site read by its evidence class, and the class count (round 1: a NO GO goes to round 2). You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/Laptop-DEV/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no credentials directory of its own. Use it only in your own mail calls, with a client timeout. Never put the key or any secret in a mail, the report, a product process or a container.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice — the only turn you end while waiting is the PARKED line of THE MODEL RULE.

Report the pinned head and main as three timestamped readings (start / mid / end), with the branch name beside each, plus refs/pull/8/head. Include a table with one row per brief section N item: MEASURED, NOT TESTED, NOT RUN or VOID, and HOW (command, image id, platform, user, network, load).

Rule 2 stands: what you did NOT test is first-class output. Write a NOT TESTED section that covers at least the image's own CMD booted with production settings, ACR's own native amd64 build, the live site and a real ACS mail, CodeQL's verdict before the merge (blind), Dependabot #1 #4 fixed (post-merge), amd64 on real hardware (yours is emulation on an M2 — say which kind), CI (read only, never caused), Windows and the account managers' real browsers, Claude in Chrome (not used), and every row you did not run. Label every action recommendation MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. The tester never fixes.
PROMPT_EOF

# ---------------------------------------------------------------- GUARDS
[ -d "$QA_DIR" ]  || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]   || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -n "$PROMPT" ]  || { echo "embedded prompt is empty" >&2; exit 4; }
[ -d "$Q_REPO/.git" ] || [ -f "$Q_REPO/.git" ] || { echo "repo under test missing: $Q_REPO" >&2; exit 5; }

# MODEL — read from Tuesday's models_latest.json (opus level), never typed from memory; REFUSE unless it is the brief's pin.
MODEL="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["levels"]["opus"]["model_id"])' "$MODELS_JSON" 2>/dev/null)"
[ "$MODEL" = "$MODEL_PIN" ] || { echo "REFUSING: $MODELS_JSON levels.opus.model_id is '${MODEL:-unreadable}', not $MODEL_PIN as the brief states — re-brief" >&2; exit 9; }

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
EXPECT_IDS='MAIN-Q QQPB'
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
[ "$(fld QQPB 3)" = "fix/qq-puppeteer-25-2026-09-22" ] || { echo "REFUSING: row QQPB branch is '$(fld QQPB 3)', the brief's target is fix/qq-puppeteer-25-2026-09-22 — re-brief" >&2; exit 40; }
is40 "$(fld QQPB 5)" || { echo "REFUSING: PIN row QQPB base is not a 40-hex sha" >&2; exit 40; }
printf '%s' "$(fld QQPB 6)" | grep -Eq '^[1-9][0-9]*$' || { echo "REFUSING: PIN row QQPB commits '$(fld QQPB 6)' is not a positive integer" >&2; exit 40; }
[ "$(fld QQPB 4)" = "$HQ_EXPECT" ] || { echo "REFUSING: QQPB's PIN head $(fld QQPB 4 | cut -c1-7) is not ${HQ_EXPECT:0:7} — this launcher's chain and content guards are pinned to it; re-brief" >&2; exit 40; }
MAINH="$(fld MAIN-Q 4)"
HQ="$(fld QQPB 4)"

# 6 — every sha the guards use is a commit in the local object store (this launcher never fetches).
for S in "$MAINH" "$HQ" "$ANCHOR_MAIN" $ANCHOR_MAINP "$ANCHOR_G17" "$C1" "$C1P" "$C2" $C2P; do
  T="$(q cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in the QuickQuote repo on this drive (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 9m — MAIN: e4ce536 EXACTLY (refuse if it moved).
[ "$MAINH" = "$ANCHOR_MAIN" ] || { echo "REFUSING: the pinned MAIN ${MAINH:0:7} is not e4ce536 — this gate pins main exactly; re-brief" >&2; exit 9; }

# 7 / 8 — the target: base as briefed, ancestor AND merge-base with MAIN, not on main, exact count, 0 behind.
H7="${HQ:0:7}"; BASE="$(fld QQPB 5)"; N="$(fld QQPB 6)"
[ "$BASE" = "$ANCHOR_MAIN" ] || { echo "REFUSING: row QQPB base ${BASE:0:7} is not e4ce536 — re-brief" >&2; exit 7; }
q merge-base --is-ancestor "$BASE" "$HQ" 2>/dev/null || { echo "REFUSING: QQPB base ${BASE:0:7} is not an ancestor of $H7" >&2; exit 7; }
[ "$(q merge-base "$HQ" "$MAINH" 2>/dev/null)" = "$BASE" ] || { echo "REFUSING: QQPB merge-base(head, MAIN) is not its base ${BASE:0:7}" >&2; exit 7; }
q merge-base --is-ancestor "$HQ" "$MAINH" 2>/dev/null && { echo "REFUSING: QQPB $H7 is ALREADY ON MAIN ${MAINH:0:7} — the brief says it is not; re-brief" >&2; exit 7; }
GOTN="$(q rev-list --count "${BASE}..${HQ}" 2>/dev/null)"
[ "$GOTN" = "$N" ] || { echo "REFUSING: QQPB $H7 has $GOTN commits over its base, the table says $N" >&2; q log --format='%h %p %s' "${BASE}..${HQ}" >&2; exit 8; }
[ "$N" = "3" ] || { echo "REFUSING: the brief's commit count is $N, this launcher's chain is three" >&2; exit 8; }
[ "$(q rev-list --count "${HQ}..${ANCHOR_MAIN}" 2>/dev/null)" = "0" ] || { echo "REFUSING: QQPB $H7 is behind e4ce536" >&2; exit 7; }

# 9 — gated anchors and the exact chain, by parents (two merges are part of the branch and are pinned).
[ "$(q log -1 --format='%P' "$ANCHOR_MAIN")" = "$ANCHOR_MAINP" ] || { echo "REFUSING: e4ce536's parents are not 3dd15bc + 5ad37f1" >&2; exit 9; }
q merge-base --is-ancestor "$ANCHOR_G17" "$MAINH" 2>/dev/null || { echo "REFUSING: gate 17's head d030674 is not on main ${MAINH:0:7}" >&2; exit 9; }
[ "$(q log -1 --format='%P' "$C1")" = "$C1P" ] || { echo "REFUSING: 3d0167e's single parent is not 47eb533 — rebased or rebuilt" >&2; exit 9; }
[ "$(q log -1 --format='%P' "$C2")" = "$C2P" ] || { echo "REFUSING: 0d45100's parents are not 3d0167e + 51e9286" >&2; exit 9; }
[ "$(q log -1 --format='%P' "$HQ")" = "$HQP" ] || { echo "REFUSING: 4d6ed6e's parents are not 0d45100 + e4ce536" >&2; exit 9; }
[ "$(q rev-list "${ANCHOR_MAIN}..${HQ}" 2>/dev/null | sort)" = "$(printf '%s\n' "$C1" "$C2" "$HQ" | sort)" ] \
  || { echo "REFUSING: QQPB's commits over e4ce536 are not exactly 3d0167e 0d45100 4d6ed6e. Got:" >&2; q rev-list "${ANCHOR_MAIN}..${HQ}" >&2; exit 9; }
[ "$(q rev-parse "${HQ}^{tree}" 2>/dev/null)" = "$HQ_TREE" ] || { echo "REFUSING: 4d6ed6e's tree is not 01bdc92" >&2; exit 9; }

# 18 — RE-PIN: BOTH rows AND refs/pull/8/head at origin, by ls-remote, read NOW (immediately before launch). No movement allowed, main included.
for ID in $EXPECT_IDS; do
  BR="$(fld "$ID" 3)"; H="$(fld "$ID" 4)"
  L="$(q ls-remote origin "refs/heads/$BR" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" && continue
  echo "REFUSING: row $ID: $H is not at refs/heads/$BR on origin — that ref moved, was never pushed, or ls-remote failed (UNKNOWN, not a value); re-pin and re-brief" >&2; printf '%s\n' "${L:-<nothing>}" >&2; exit 18
done
LP="$(q ls-remote origin "refs/pull/${PR_NUM}/head" "refs/pull/${PR_NUM}/merge" 2>&1)"
printf '%s\n' "$LP" | grep -q "^${HQ}[[:space:]]refs/pull/${PR_NUM}/head\$" \
  || { echo "REFUSING: refs/pull/${PR_NUM}/head is not ${H7} on origin — PR #${PR_NUM} moved or is not the target; re-pin and re-brief" >&2; printf '%s\n' "${LP:-<nothing>}" >&2; exit 18; }
PR_MERGE_NOW="$(printf '%s\n' "$LP" | awk -v r="refs/pull/${PR_NUM}/merge" '$2==r{print $1}')"
[ "$PR_MERGE_NOW" = "$PR_MERGE_SEEN" ] || echo "NOTE: refs/pull/${PR_NUM}/merge is '${PR_MERGE_NOW:-<absent>}', the drafter read ${PR_MERGE_SEEN:0:7} — GitHub recomputed its test merge (main is pinned, so read why before launch)" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 / 23 — exact file set, numstat, and the ONLY non-comment changes.
GOT="$(q diff --name-only "$ANCHOR_MAIN" "$HQ" 2>/dev/null | sort)"
[ "$GOT" = "$(printf '%s\n' $DELTA_FILES | sort)" ] || { echo "REFUSING: QQPB ${H7}'s delta over e4ce536 is not exactly the briefed 5-file set. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }
[ "$(q diff --numstat "$ANCHOR_MAIN" "$HQ" | awk '{printf "%s/%s/%s ", $1, $2, $3}')" = "$NUMSTAT_EXPECT" ] \
  || { echo "REFUSING: the whole-diff numstat is not the briefed one. Got:" >&2; q diff --numstat "$ANCHOR_MAIN" "$HQ" >&2; exit 23; }
ncl() { q diff "$ANCHOR_MAIN" "$HQ" -- "$@" 2>/dev/null | grep -E '^[+-]' | grep -vE '^(\+\+\+|---) ' | grep -vE '^[+-][[:space:]]*(#|//|$)'; }
[ "$(ncl stage3/Dockerfile)" = "$DKF_NCL_EXPECT" ] || { echo "REFUSING: the Dockerfile's non-comment change is not exactly the FROM line (WRONG (g)). Got:" >&2; ncl stage3/Dockerfile >&2; exit 23; }
[ "$(q diff -U0 "$ANCHOR_MAIN" "$HQ" -- stage3/package.json | grep -E '^[+-][^+-]')" = "$PKG_U0_EXPECT" ] || { echo "REFUSING: package.json's change is not exactly the puppeteer-core line" >&2; exit 23; }
[ "$(ncl stage3/test/fixtures/hang-close.cjs stage3/test/lib-close-shared.test.mjs)" = "$FIX_NCL_EXPECT" ] || { echo "REFUSING: the two test files change other than their CdpBrowser require line" >&2; exit 23; }

# 74 — content, read from the pinned shas (never a checkout).
blob() { q rev-parse "${1}:${2}" 2>/dev/null; }
has() { q show "${1}:${2}" 2>/dev/null | grep -qF -- "$3"; }
must() { has "$1" "$2" "$3" || { echo "REFUSING: ${1:0:7}:$2 lacks '$3' — the brief gates different code; re-brief" >&2; exit 74; }; }
mustnot() { has "$1" "$2" "$3" && { echo "REFUSING: ${1:0:7}:$2 carries '$3' — the brief's reading is wrong; re-brief" >&2; exit 74; }; return 0; }
for P in 'stage3/Dockerfile|8311ebebe385cb67d7ee384dcbcb00304d22a725|5972f7cabd44ebacdeefbdd394f7a9a6098d6926' \
         'stage3/package.json|61d0d5c51f2987750620a520844685746cc2bdcb|94ab2f56e854ce040c0cc89d8cca91015b0daf11' \
         'stage3/package-lock.json|01c5e5e3415bed5afc7c30fc9bd1efc37fcb8d4e|9366344f72a6a152d7bd6164f20442a9fdf84b49' \
         'stage3/test/fixtures/hang-close.cjs|f902922507b6bcdf77d45d3c53fb684995b97ca2|8fe024cc72d98352e74eacb8423e0aa22621cae2' \
         'stage3/test/lib-close-shared.test.mjs|6f7921588439737aaaf1924d48c4b15251ff477e|d7c2b07929f8d2de125a12dc4dcc91edd8ea7f0f'; do
  F="${P%%|*}"; R2="${P#*|}"; B0="${R2%%|*}"; B1="${R2#*|}"
  [ "$(blob "$ANCHOR_MAIN" "$F")" = "$B0" ] && [ "$(blob "$HQ" "$F")" = "$B1" ] || { echo "REFUSING: $F blobs are not ${B0:0:7} -> ${B1:0:7}" >&2; exit 74; }
done
for F in index.html stage3/server.js stage3/lib/pdf.js stage3/lib/xlsx.js stage3/lib/mail.js stage3/lib/store.js stage3/lib/sendFailure.js stage3/strip.js \
         stage3/login.html .dockerignore .github/workflows/tests.yml quote-engine.test.mjs stage3/test/server.test.mjs stage3/test/lib-close.test.mjs \
         stage3/test/print-fit.mjs stage3/test/xlsx-parity.mjs stage3/test/store-azurite.test.mjs CLAUDE.md; do
  B0="$(blob "$ANCHOR_MAIN" "$F")"
  [ -n "$B0" ] && [ "$(blob "$HQ" "$F")" = "$B0" ] || { echo "REFUSING: $F differs between main and the head — the brief says it is carried unchanged" >&2; exit 74; }
done
for T in 'FROM node:22-bookworm-slim' 'chromium ca-certificates fontconfig' 'fonts-liberation fonts-liberation2 fonts-dejavu-core' \
         'ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium' 'RUN npm ci --omit=dev' 'COPY stage3/ /app/stage3/' 'RUN node strip.js' \
         'ENV NODE_ENV=production' 'USER node'; do
  must "$HQ" stage3/Dockerfile "$T"
done
must "$ANCHOR_MAIN" stage3/Dockerfile 'FROM node:20-bookworm-slim'
mustnot "$HQ" .dockerignore 'stage3/test'
must "$HQ" stage3/lib/pdf.js 'const puppeteer = require("puppeteer-core");'
must "$HQ" stage3/lib/pdf.js 'args: ["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"]'
must "$HQ" stage3/package-lock.json '"resolved": "https://registry.npmjs.org/puppeteer-core/-/puppeteer-core-25.0.2.tgz",'
must "$HQ" stage3/package-lock.json '"integrity": "sha512-Q0IUIHER1S9PiNIfdNFc+pVOj79Tp4b9v0Fv4enigwsLy0Hbgq45KFgqzmN31DeCXh+Uvxnt9r7fMERhAMjs8Q==",'
must "$HQ" stage3/package-lock.json '"node_modules/webdriver-bidi-protocol": {'
mustnot "$HQ" stage3/package-lock.json '"node_modules/extract-zip": {'
mustnot "$HQ" stage3/package-lock.json '"node_modules/basic-ftp": {'
must "$ANCHOR_MAIN" stage3/package-lock.json '"node_modules/extract-zip": {'
must "$HQ" stage3/package.json '"basic-ftp": "^6.2.3"'
must "$HQ" stage3/test/store-azurite.test.mjs 'UseDevelopmentStorage=true'
[ "$(q show "${HQ}:stage3/test/lib-close-shared.test.mjs" | grep -cE '^[[:space:]]*test\(')" = "2" ] || { echo "REFUSING: lib-close-shared.test.mjs does not carry 2 test( cells at the head" >&2; exit 74; }
[ "$(q ls-tree -r --name-only "$HQ" .github)" = ".github/workflows/tests.yml" ] || { echo "REFUSING: .github at the head holds other than tests.yml — §N7.3's reading is wrong" >&2; exit 74; }
for T in 'pricing-pack:' 'stage3-server:' 'store-azurite:' 'print-fit:' 'xlsx-parity:'; do must "$HQ" .github/workflows/tests.yml "  $T"; done
for T in 'npm ci --offline --ignore-scripts' 'entry by entry' 'npm audit --omit=dev' 'never `npm audit fix`'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the dependency rule '$T'" >&2; exit 63; }
done
for T in 'npm ci --offline --ignore-scripts' 'entry by entry' 'npm audit --omit=dev' 'never npm audit fix'; do
  printf '%s\n' "$PROMPT" | grep -qiF -- "$T" || { echo "REFUSING: prompt lacks the dependency rule '$T'" >&2; exit 63; }
done

# 31 — the READY is on disk, names the pinned heads, its NOT TESTED lines are carried verbatim; sources on disk.
[ -s "$READY" ] || { echo "REFUSING: the READY mail is not on disk: $READY" >&2; exit 31; }
for T in 'READY FOR QA, TIER 1: QuickQuote PR #8 @ 4d6ed6e (fix/qq-puppeteer-25-2026-09-22, forward-merged with main e4ce536)' \
         'One amd64 run under emulation is still going; a STATUS mail will follow with it.' 'Nothing merged, pushed to ACR or deployed.' \
         'git diff --stat: 5 files, +85/-522' 'removed 40: the whole proxy-agent'; do
  grep -qF -- "$T" "$READY" || { echo "REFUSING: $READY does not carry '$T'" >&2; exit 31; }
done
NT="$(awk 'f&&!/^- /{exit} f{print;next} /^NOT TESTED/{f=1;print}' "$READY")"
[ -n "$NT" ] || { echo "REFUSING: $READY carries no NOT TESTED block" >&2; exit 31; }
while IFS= read -r L; do
  [ -n "$L" ] || continue
  grep -qxF -- "$L" "$BRIEF" || { echo "REFUSING: the brief does not carry this NOT TESTED line of the READY verbatim: $L" >&2; exit 31; }
done <<< "$NT"
for T in 'QQPB NOT TESTED' 'C-19' 'quickquote-decision14-puppeteer25-node22-1016' 'ROUND 1' '2026-10-16_vision-qq-pr8-READY-mail.txt' \
         'WRONG (a)' 'WRONG (b)' 'WRONG (c)' 'WRONG (e)' 'WRONG (j)' 'WRONG (m)' 'NX-1' 'NX-2' 'GH-API-LEG' 'AZ-READ-LEG' 'AZ-PRE-READ' \
         'D1' 'D2' 'D3' 'D4' 'PROVISIONAL' 'qq-evidence-local' 'x86_64' 'linux/amd64' 'G-M1' 'G-M2' 'pmBoth'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: the brief does not carry '$T'" >&2; exit 31; }
done
for R in 'R1: ' 'R2: ' 'R3: ' 'R4: ' 'R5: ' 'R6: ' 'R7: '; do
  grep -qF -- "- $R" "$BRIEF" || { echo "REFUSING: the brief does not carry Tuesday's ruling '$R' as a ruling line" >&2; exit 31; }
done
[ -s "$CLAR" ] || { echo "REFUSING: Vision CLARIFICATIONS.md absent: $CLAR" >&2; exit 31; }
grep -qF '**C-19.' "$CLAR" || { echo "REFUSING: $CLAR lacks C-19" >&2; exit 31; }
for T in 'quickquote-decision14-puppeteer25-node22-1016' 'Build the puppeteer 25 + node 22 change now' 'never pushed to ACR, never a release tag' \
         'Not covered: publishing the new runtime to the live site'; do
  grep -qF -- "$T" "$CLAR" || { echo "REFUSING: CLARIFICATIONS C-19 does not carry '$T' — the ruling the brief quotes is not on disk" >&2; exit 31; }
done
grep -qF '**C-20.' "$CLAR" && echo "NOTE: Vision CLARIFICATIONS now has a C-20 — the brief says C-01..C-19; read it before launch" >&2
[ -s "$CHARTER" ] || { echo "REFUSING: the charter is absent: $CHARTER" >&2; exit 31; }
[ -s "$G4_REPORT" ] && [ -s "$G4_P5B" ] || { echo "REFUSING: gate 4's report or sections/P5B.md is absent on the T9: $G4_DIR (is the T9 mounted?)" >&2; exit 31; }
grep -qF 'image build NOT RUN; Node 22 NOT TESTED' "$G4_REPORT" || { echo "REFUSING: gate 4's report no longer carries P5B's 'image build NOT RUN; Node 22 NOT TESTED'" >&2; exit 31; }
[ -s "$G17_REPORT" ] || { echo "REFUSING: gate 17's report is absent on the T9: $G17_REPORT" >&2; exit 31; }
grep -qF '**GO WITH FINDINGS**' "$G17_REPORT" && grep -qF 'd030674694279be3159d67de4a10f220ea6b8335' "$G17_REPORT" \
  || { echo "REFUSING: gate 17's report does not carry QQQR's GO WITH FINDINGS at d030674" >&2; exit 31; }
for D in "$G4_DIR" "$G17_DIR"; do
  grep -qF "$D" "$BRIEF" || { echo "REFUSING: the brief does not name $D" >&2; exit 31; }
  case "$PROMPT" in *"$D"*) ;; *) echo "REFUSING: the prompt does not name $D" >&2; exit 31 ;; esac
done
for H in qa-run.py qa-g17-lib.mjs qa-harness-g17-capture.mjs qa-harness-g17-server.cjs g17-hosted-render.cjs g17-run-suites.sh g17-mutate.py g17-heads.sh \
         g17-gh.sh tapsets.py lockcmp.py lockwalk.py qa-chrome-egressblock.sh qa-chrome-census.py qa-egress-posctl.mjs qa-floorcount.py \
         qa-harness-floorctl.mjs qa-netlog-scan.py mktree-qq.sh; do
  [ -s "$G17_TOOLS/$H" ] || { echo "REFUSING: gate 17's tool $H is not on disk — the brief names it" >&2; exit 31; }
  grep -qF -- "$H" "$BRIEF" || { echo "REFUSING: the brief does not name gate 17's tool $H" >&2; exit 31; }
done

# 39 — the floor instrument is on disk and named.
[ -s "$G17_TOOLS/qa-floorcount.py" ] || { echo "REFUSING: gate 17's floor instrument copy missing" >&2; exit 39; }
grep -qF 'qa-floorcount.py' "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument qa-floorcount.py" >&2; exit 39; }

# 10 / 17 — report path named in both; no stale report.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

# 12 — tier declared in both, at the pinned head.
grep -qE "^- \*\*QQPB\*\* at \`${H7}\` — \*\*TIER 1" "$BRIEF" || { echo "REFUSING: brief does not declare QQPB at \`$H7\` TIER 1" >&2; exit 12; }
case "$PROMPT" in *"QQPB (TIER 1"*) ;; *) echo "REFUSING: prompt does not declare: QQPB (TIER 1" >&2; exit 12 ;; esac

# 78 — the commission's requirements, in both.
for T in 'TIER 1' 'ROUND 1' 'C-19' 'quickquote-decision14-puppeteer25-node22-1016' 'GO WITH FINDINGS' 'NO GO' 'SETS, NOT COUNTS' 'linux/amd64' \
         'x86_64' '4d6ed6e' 'e4ce536' 'puppeteer-core' '25.0.2' 'node:22-bookworm-slim' 'node:20-bookworm-slim' 'qa-g18-' 'qq-evidence-local' \
         'STATUS mail' '--network none' 'createApp()' 'AUD' 'USD' 'CAD' 'advanced' 'light and dark' 'xlsx' 'pdftotext' 'pdftoppm' 'pdffonts' \
         'npm audit --omit=dev' 'internal/' 'G-M1' 'G-M2' 'ExperimentalWarning' 'require(esm)' 'extract-zip' 'basic-ftp' 'linuxFxVersion' \
         'hpasqqacr' 'docker push' 'docker login' 'prune' 'Azurite' 'test:print' 'test:xlsx' 'quote-engine.test.mjs' 'node strip.js' 'node --check' \
         'Claude in Chrome' 'HPAM word' 'PROVISIONAL' 'pmBoth'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks '$T'" >&2; exit 78; }
  printf '%s\n' "$PROMPT" | grep -qiF -- "$T" || { echo "REFUSING: prompt lacks '$T'" >&2; exit 78; }
done

# 13 / 14 / 15 / 20 / 70 — directive, brief path, placeholders, verdict route, key path, question route, safety line.
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
case "$PROMPT" in *"$READY"*) ;; *) echo "REFUSING: prompt must name the READY path" >&2; exit 14 ;; esac
if printf '%s\n' "$PROMPT" | LC_ALL=C grep -q '@[A-Z_0-9]*@'; then echo "REFUSING: the prompt carries a placeholder" >&2; exit 14; fi
case "$PROMPT" in *"MAIL YOUR VERDICT"*"tuesday-agent@agentmail.to"*) ;; *) echo "REFUSING: prompt must say MAIL YOUR VERDICT to tuesday-agent@agentmail.to" >&2; exit 15 ;; esac
case "$PROMPT" in *"$SUBJECT_STEM"*) ;; *) echo "REFUSING: prompt must carry the verdict subject stem" >&2; exit 15 ;; esac
grep -qF "$SUBJECT_STEM" "$BRIEF" || { echo "REFUSING: brief must carry the verdict subject stem" >&2; exit 15; }
grep -qF 'MAIL YOUR VERDICT' "$BRIEF" || { echo "REFUSING: brief must say MAIL YOUR VERDICT" >&2; exit 15; }
if printf '%s\n' "$PROMPT" | grep -qi 'wednesday-agent@' && ! printf '%s\n' "$PROMPT" | grep -q 'Never wednesday-agent@'; then
  echo "REFUSING: the prompt routes to wednesday-agent@ — Datasec's coordinator is Tuesday" >&2; exit 15; fi
if printf '%s\n' "$PROMPT" | grep -qF 'KK_T9_External_HDD/TUESDAY'; then echo "REFUSING: the prompt names the T9 TUESDAY tree — this machine's Tuesday is /Volumes/Laptop-DEV/TUESDAY" >&2; exit 15; fi
if grep -qF 'KK_T9_External_HDD/TUESDAY' "$BRIEF"; then echo "REFUSING: the brief names the T9 TUESDAY tree — this machine's Tuesday is /Volumes/Laptop-DEV/TUESDAY" >&2; exit 15; fi
case "$PROMPT" in *"/Volumes/Laptop-DEV/TUESDAY/4_Credentials/.env"*) ;; *) echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20 ;; esac
[ -s "$TUE/4_Credentials/.env" ] || { echo "REFUSING: the AgentMail key file $TUE/4_Credentials/.env is absent" >&2; exit 20; }
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
WORDS="merge-tree NOT%TESTED env%-i bash e4ce536 4d6ed6e work-g18 FOREGROUND MEASURED%AT%RUNTIME PROBED READ%ONLY start%/%mid%/%end CI VOID node%--check STOPPED%and%LEFT NX-1 NX-2 NX-3 NX-4"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## Charter' '^## RULED BY KAM, AND SETTLED' '^## PRIOR ROUND' '^PRIOR ROUND: ' 'ITS REPORT IS ON DISK AT:' '^## PIN' \
         '^## WRONG OR UNVERIFIABLE' '^## THE READY' '^## 2a. LEGITIMATE SHAPES' '^## N1. ' '^## N2. ' '^## N3. ' '^## N4. ' '^## N5. ' '^## N6. ' \
         '^## N7. ' '^## N8. ' '^## N9. ' '^## 12. The merge' '^## 13. FLOOR' '^### HELD' '^## THE MODEL RULE' "^## TUESDAY'S RULINGS AT STAMP" \
         '^## 14. Output' '^PROVENANCE:'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
# 24 — the prompt must DESCRIBE the app's entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qE 'server/index\.js|server\.js'; then
  echo "REFUSING: the prompt contains a literal server entry path — this agent would read as a FOREIGN SERVER to an argv-grep floor check. Describe it; do not name it." >&2; exit 24; fi

# 53 / 60 / 61 / 62 / 64 / 69 / 75 — standing rules, in both.
for T in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' '420 s' '120 s' '2400 s'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the deadline/heartbeat rule '$T'" >&2; exit 53; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the deadline/heartbeat rule '$T'" >&2; exit 53 ;; esac
done
for T in 'node --check' 'VOID'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the parse-before-red rule '$T'" >&2; exit 60; }
done
for T in 'EXCLUSIVE' 'work-g18'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the tree-exclusivity rule '$T'" >&2; exit 61; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the tree-exclusivity rule '$T'" >&2; exit 61 ;; esac
done
for T in '4848' '8080' '47787' 'env -i' 'AGENTMAIL_API_KEY' 'AGENTMAIL_INBOX' 'no jest lock' 'TABLES_CONNECTION_STRING' 'HPAM_WORD' 'ADVANCED_UNLOCK_SECRET' \
         'SESSION_SECRET' 'PUPPETEER_EXECUTABLE_PATH' 'GoogleUpdater' 'chrome_crashpad_handler' 'net-log' 'GH_TOKEN'; do
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
for T in 'CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY' 'PRIOR WORK' 'OWN object dir' 'no writes in the QuickQuote repo' 'start / mid / end' 'NOT TESTED' 'STOPPED and LEFT'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the standing line '$T'" >&2; exit 75; }
  printf '%s\n' "$PROMPT" | grep -qiF -- "$T" || { echo "REFUSING: prompt lacks the standing line '$T'" >&2; exit 75; }
done

# 44 — the host browser leg's instrument, a local Google Chrome, is installed. The launcher never starts it.
[ -x "$CHROME_BIN" ] || { echo "REFUSING: no local Google Chrome at $CHROME_BIN — the host test:print / test:xlsx legs (brief §N1) would be NOT RUN" >&2; exit 44; }

# 45D — the docker leg (brief §N2-§N4) is the gate's core: the daemon answers, buildx offers linux/amd64, no stale qa-g18-* object; foreign objects NOTEd.
command -v docker >/dev/null 2>&1 || { echo "REFUSING: docker CLI not found — the image legs cannot run" >&2; exit 45; }
DSV="$(docker version --format '{{.Server.Version}} {{.Server.Os}}/{{.Server.Arch}}' 2>/dev/null)"
[ -n "$DSV" ] || { echo "REFUSING: the docker daemon does not answer (docker version) — start Docker Desktop before launch; the image legs cannot run" >&2; exit 45; }
[ "$DSV" = "29.7.2 linux/arm64" ] || echo "NOTE: docker server is '$DSV', not '29.7.2 linux/arm64' as read at drafting — the gate records it" >&2
docker buildx ls 2>/dev/null | grep -q 'linux/amd64' || { echo "REFUSING: no buildx builder lists linux/amd64 — the amd64 images (R2) cannot be built" >&2; exit 45; }
QA_IMG="$(docker images --format '{{.Repository}}:{{.Tag}}' 2>/dev/null | grep -E '^qa-g18-' | tr '\n' ' ')"
QA_CTR="$(docker ps -a --format '{{.Names}}' 2>/dev/null | grep -E '^qa-g18-' | tr '\n' ' ')"
[ -z "$QA_IMG$QA_CTR" ] || { echo "REFUSING: qa-g18-* objects already exist (images: ${QA_IMG:-none}; containers: ${QA_CTR:-none}) — a previous gate-18 session left them; read before launch" >&2; exit 45; }
FOREIGN="$(docker images --format '{{.Repository}}:{{.Tag}}' 2>/dev/null | grep -E '^qq-evidence-local:' | tr '\n' ' ')"
[ -z "$FOREIGN" ] || echo "NOTE: the builder's images are on the daemon (${FOREIGN}) — never touched by the gate (brief §13.5)" >&2
B23="$(docker ps --format '{{.Names}}' 2>/dev/null | grep -E '^qa-b23-' | tr '\n' ' ')"
[ -z "$B23" ] || echo "NOTE: QA/NexusAI-batch23 containers are RUNNING on the same daemon (${B23}) — contention, not a conflict; never touched" >&2
docker images --format '{{.Repository}}' 2>/dev/null | grep -qx 'mcr.microsoft.com/azure-storage/azurite' || echo "NOTE: no local Azurite image — §N3.4 would need a pull outside NX-1; the gate carries it NOT RUN" >&2
LOAD1="$(sysctl -n vm.loadavg 2>/dev/null | awk '{print $2}')"
case "$LOAD1" in ''|*[!0-9.]*) ;; *) awk -v l="$LOAD1" 'BEGIN{exit !(l>40)}' && echo "NOTE: 1-minute load is $LOAD1 (drafting read 224.77) — amd64 emulation will be slow; Tuesday decides whether to launch now (drafter's report)" >&2 ;; esac
for T in 'pdftotext' 'pdftoppm' 'pdfinfo' 'pdffonts'; do command -v "$T" >/dev/null 2>&1 || echo "NOTE: $T is not on PATH — §N4's comparator needs it" >&2; done

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
NEG_SEATS=''; NEG_DESC=''
for NAME in tuesday "$BUILDER_PANE"; do
  PP="$(pane_pid_of "$NAME")"
  NP="$(printf '%s\n' "$PP" | sed '/^$/d' | wc -l | tr -d ' ')"
  [ "$NP" = "1" ] || { echo "REFUSING: expected exactly one tmux pane named '$NAME', found $NP — its negative control is required" >&2; exit 38; }
  CP="$(claude_under "$PP")"
  [ "$(printf '%s\n' "$CP" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: pane '$NAME' (pid $PP) has '${CP:-no}' claude descendant(s), not exactly one — a seat is missing or ambiguous" >&2; exit 38; }
  NEG_SEATS="$NEG_SEATS $CP"; NEG_DESC="$NEG_DESC \`$CP\` ($NAME);"
done
EXTRA="$(printf '%s\n' "$PANES" | awk '{p=$1; $1=""; sub(/^ /,""); print $0}' | grep -E '^(QA/|fleet-monitor$)' | grep -vxF "$ROUTE_NAME" | sort -u)"
while IFS= read -r PEER; do
  [ -n "$PEER" ] || continue
  GP="$(pane_pid_of "$PEER")"; GC=''
  [ -n "$GP" ] && [ "$(printf '%s\n' "$GP" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] && GC="$(claude_under "$GP")"
  if [ -n "$GC" ] && [ "$(printf '%s\n' "$GC" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ]; then
    NEG_SEATS="$NEG_SEATS $GC"; NEG_DESC="$NEG_DESC \`$GC\` ($PEER);"
  else
    echo "NOTE: $PEER has no single live claude — not a negative control" >&2
  fi
done <<EOF_PEERS
$EXTRA
EOF_PEERS
NEG_SEATS="${NEG_SEATS# }"
NCOUNT="$(printf '%s\n' $NEG_SEATS | sed '/^$/d' | wc -l | tr -d ' ')"
[ "$(printf '%s\n' $NEG_SEATS | sort -u | wc -l | tr -d ' ')" = "$NCOUNT" ] || { echo "REFUSING: the derived seat pids are not distinct: $NEG_SEATS" >&2; exit 38; }

# 86 — no live gate-18 session already exists.
for P in $(pane_pid_of "$ROUTE_NAME"); do
  if [ -n "$(claude_under "$P")" ]; then echo "REFUSING: a pane named $ROUTE_NAME (pid $P) already runs a claude — gate 18 is live; do not start a second session" >&2; exit 86; fi
done

# ---- the coordinator's to-do guards (46, 47, 41, 32): run LAST, reported TOGETHER, exit with the first pending code.
PENDING=''
pend() { [ -n "$PENDING" ] || PENDING="$1"; shift; echo "REFUSING: $*" >&2; }

# 46 — the GitHub read leg as Tuesday sets it (decision D1).
GHLEG="$(sed -n 's/^GH-API-LEG: \([A-Z-]*\)[[:space:]]*$/\1/p' "$BRIEF" | head -1)"
case "$GHLEG" in
  READ-ONLY-VISION-TOKEN)
    [ -d "$VSP_GH" ] || { echo "REFUSING: GH-API-LEG is READ-ONLY-VISION-TOKEN but $VSP_GH is not a directory" >&2; exit 46; }
    command -v gh >/dev/null 2>&1 || { echo "REFUSING: GH-API-LEG is READ-ONLY-VISION-TOKEN but no gh binary is on PATH" >&2; exit 46; } ;;
  NOT-RUN) ;;
  "$PH_DECIDE") pend 46 "the brief's GH-API-LEG line is still ${PH_DECIDE} — Tuesday sets READ-ONLY-VISION-TOKEN or NOT-RUN (decision D1) before launch" ;;
  *) echo "REFUSING: the brief's GH-API-LEG line reads '${GHLEG:-<missing>}' — it must be exactly READ-ONLY-VISION-TOKEN or NOT-RUN" >&2; exit 46 ;;
esac

# 47 (NEW) — the Azure read leg as Tuesday sets it (decision D2), and its AZ-PRE-READ line.
AZLEG="$(sed -n 's/^AZ-READ-LEG: \([A-Z-]*\)[[:space:]]*$/\1/p' "$BRIEF" | head -1)"
AZPRE="$(sed -n 's/^AZ-PRE-READ: \(.*\)$/\1/p' "$BRIEF" | head -1)"
case "$AZLEG" in
  TUESDAY-READS)
    case "$AZPRE" in
      ''|"$PH_STAMP"|n/a) pend 47 "AZ-READ-LEG is TUESDAY-READS but the AZ-PRE-READ line is '${AZPRE:-<missing>}' — Tuesday reads linuxFxVersion before launch and writes it there" ;;
      *linuxFxVersion*) ;;
      *) echo "REFUSING: AZ-PRE-READ does not name linuxFxVersion: '$AZPRE'" >&2; exit 47 ;;
    esac ;;
  GATE-SHIM)
    [ -d "$VSP_AZ" ] || { echo "REFUSING: AZ-READ-LEG is GATE-SHIM but $VSP_AZ is not a directory" >&2; exit 47; }
    command -v az >/dev/null 2>&1 || { echo "REFUSING: AZ-READ-LEG is GATE-SHIM but no az binary is on PATH" >&2; exit 47; }
    [ "$AZPRE" = "n/a" ] || { echo "REFUSING: AZ-READ-LEG is GATE-SHIM; the AZ-PRE-READ line must read n/a (got '$AZPRE')" >&2; exit 47; } ;;
  NOT-RUN)
    [ "$AZPRE" = "n/a" ] || { echo "REFUSING: AZ-READ-LEG is NOT-RUN; the AZ-PRE-READ line must read n/a (got '$AZPRE')" >&2; exit 47; } ;;
  "$PH_DECIDE") pend 47 "the brief's AZ-READ-LEG line is still ${PH_DECIDE} — Tuesday sets TUESDAY-READS, GATE-SHIM or NOT-RUN (decision D2) before launch" ;;
  *) echo "REFUSING: the brief's AZ-READ-LEG line reads '${AZLEG:-<missing>}' — it must be exactly TUESDAY-READS, GATE-SHIM or NOT-RUN" >&2; exit 47 ;;
esac

# 41 — the answer route exists (Tuesday adds 'QA/Vision-gate18|tuesday-agent@agentmail.to|no' at stamp; this launcher never writes it).
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" \
  || pend 41 "no '${ROUTE_NAME}|tuesday-agent@agentmail.to|…' line in $ROUTING — answers to the gate would have no route. Add it (pattern: the QA/Vision-gate17 line) before launch."

# 32 — the coordinator stamps the self-check (line AND note), D1-D4 and every @STAMP@.
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  pend 32 "the brief still carries $(grep -cF "$PH_STAMP" "$BRIEF") ${PH_STAMP} placeholder(s) (Self-check line and note, AZ-PRE-READ, the RULED lines of D1-D4) — the coordinator re-reads end-to-end and stamps all of them before launch"
fi

if [ -n "$PENDING" ]; then
  echo "guards pass (MODEL 40 6 9 7 8 18 22 23 74 63 31 39 10 17 12 78 13 14 15 20 70 82 19 24 53 60 61 62 64 69 75 44 45D 38R 86); coordinator to-do pending (46 47 41 32 as listed above); exiting $PENDING." >&2
  echo "  origin re-read $PIN_TS: main ${MAINH:0:7}, QQPB $H7, refs/pull/8/head $H7; docker $DSV; model $MODEL" >&2
  echo "  NEG seats (38R, derived live):$NEG_DESC" >&2
  exit "$PENDING"
fi

PIN_BLOCK="$(printf 'PINNED HEADS — verified by the launcher at %s (cat-file; base e4ce536, 0 behind; ancestor and merge-base with MAIN; not-already-on-main; commit count 3; exact chain by parents: 3d0167e <- 47eb533, 0d45100 <- 3d0167e + 51e9286, 4d6ed6e <- 0d45100 + e4ce536; e4ce536 <- 3dd15bc + 5ad37f1; d030674 on main; main pinned EXACTLY; refs/pull/8/head = head; the 5-file delta, numstat and its only non-comment lines; git ls-remote origin for both rows):\n' "$PIN_TS"
  printf '%s\n' "$PIN" | awk -F'\t' '{ printf "  %-7s %-11s %-32s %s  base %s  commits %s\n", $1, $2, $3, $4, ($5=="-"?"-":substr($5,1,12)), $6 }'
  printf '  Main: pinned %s (exact; a move refuses). PR #%s: refs/pull/%s/head = %s; refs/pull/%s/merge = %s (GitHub test merge)\n' "${MAINH:0:12}" "$PR_NUM" "$PR_NUM" "${HQ:0:12}" "$PR_NUM" "${PR_MERGE_NOW:-<absent>}"
  printf '  Docker server at launch: %s. The builder'"'"'s qq-evidence-local images and any qa-b23-* object are FOREIGN.\n' "$DSV"
  printf 'GH-API-LEG, as set in the brief: %s\n' "$GHLEG"
  printf 'AZ-READ-LEG, as set in the brief: %s\n' "$AZLEG"
  printf 'AZ-PRE-READ, as stamped by Tuesday: %s\n' "$AZPRE"
  printf 'NEGATIVE-CONTROL SEATS, derived live by the launcher from the cockpit panes at %s:%s Re-read them at start.' "$PIN_TS" "$NEG_DESC")"

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  printf '%s\n' "$PIN_BLOCK"
  echo "  model: $MODEL at exec (from models_latest.json); --check started no claude; nothing written."
  exit 0
fi

# 11 — no inherited identity: AZURE_CONFIG_DIR EMPTY unless AZ-READ-LEG = GATE-SHIM; GH_CONFIG_DIR EMPTY unless GH-API-LEG = READ-ONLY-VISION-TOKEN.
ID_TMP="$(mktemp -d "${TMPDIR:-/tmp}/qa-vision-gate18-id.XXXXXX")" || { echo "REFUSING: cannot create the empty identity dir" >&2; exit 11; }
mkdir -p "$ID_TMP/azure-empty" "$ID_TMP/gh-empty" "$ID_TMP/bin" || { echo "REFUSING: cannot create the identity dirs under $ID_TMP" >&2; exit 11; }
{ [ -z "$(ls -A "$ID_TMP/azure-empty")" ] && [ -z "$(ls -A "$ID_TMP/gh-empty")" ]; } || { echo "REFUSING: the identity dirs under $ID_TMP are not empty" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_TMP/azure-empty"
export GH_CONFIG_DIR="$ID_TMP/gh-empty"
if [ "$GHLEG" = "READ-ONLY-VISION-TOKEN" ]; then
  QA_REAL_GH="$(command -v gh)" || { echo "REFUSING: gh vanished between guard 46 and launch" >&2; exit 11; }
  export QA_REAL_GH
  cat > "$ID_TMP/bin/gh" <<'SHIM'
#!/bin/bash
# gate-18 GET-only gh shim (written by launch_qa_vision_qq_gate18.sh; GH-API-LEG = READ-ONLY-VISION-TOKEN). Brief §HELD binds the rest.
REAL="${QA_REAL_GH:?gh shim: QA_REAL_GH unset}"
[ "${1:-}" = "api" ] || { echo "gh shim: only 'gh api' GET reads are allowed in Vision gate 18 (got: ${1:-<none>})" >&2; exit 64; }
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
fi
if [ "$AZLEG" = "GATE-SHIM" ]; then
  QA_REAL_AZ="$(command -v az)" || { echo "REFUSING: az vanished between guard 47 and launch" >&2; exit 11; }
  export QA_REAL_AZ
  cat > "$ID_TMP/bin/az" <<'SHIM'
#!/bin/bash
# gate-18 READ-ONLY az shim (written by launch_qa_vision_qq_gate18.sh; AZ-READ-LEG = GATE-SHIM). Three read commands, fixed names; brief §N7.2.
REAL="${QA_REAL_AZ:?az shim: QA_REAL_AZ unset}"
ok_opts() {   # only output-shaping options may follow the fixed arguments
  while [ $# -gt 0 ]; do
    case "$1" in
      --query|-o|--output|--orderby|--top) [ $# -ge 2 ] || return 1; shift 2 ;;
      --query=*|--output=*|--orderby=*|--top=*) shift ;;
      *) return 1 ;;
    esac
  done; return 0; }
case "${1:-} ${2:-}" in
  "account show") shift 2; ok_opts "$@" && exec "$REAL" account show "$@" ;;
  "webapp config")
    [ "${3:-}" = "show" ] && [ "${4:-}" = "--name" ] && [ "${5:-}" = "hpas-quickquote" ] && [ "${6:-}" = "--resource-group" ] && [ "${7:-}" = "hpas-quickquote-rg" ] \
      && { shift 7; ok_opts "$@" && exec "$REAL" webapp config show --name hpas-quickquote --resource-group hpas-quickquote-rg "$@"; } ;;
  "acr repository")
    [ "${3:-}" = "show-tags" ] && [ "${4:-}" = "--name" ] && [ "${5:-}" = "hpasqqacr" ] && [ "${6:-}" = "--repository" ] && [ "${7:-}" = "hpas-quickquote" ] \
      && { shift 7; ok_opts "$@" && exec "$REAL" acr repository show-tags --name hpasqqacr --repository hpas-quickquote "$@"; } ;;
esac
echo "az shim: refused — Vision gate 18 allows only: az account show | az webapp config show --name hpas-quickquote --resource-group hpas-quickquote-rg | az acr repository show-tags --name hpasqqacr --repository hpas-quickquote (plus --query/-o/--orderby/--top)" >&2
exit 64
SHIM
  chmod 0755 "$ID_TMP/bin/az" || { echo "REFUSING: cannot make the az shim executable" >&2; exit 11; }
  export AZURE_CONFIG_DIR="$VSP_AZ"
  export AZURE_CORE_COLLECT_TELEMETRY=false
fi
export PATH="$ID_TMP/bin:$PATH"
if [ "$GHLEG" = "READ-ONLY-VISION-TOKEN" ]; then [ "$(command -v gh)" = "$ID_TMP/bin/gh" ] || { echo "REFUSING: the gh shim is not first on PATH" >&2; exit 11; }; fi
if [ "$AZLEG" = "GATE-SHIM" ]; then [ "$(command -v az)" = "$ID_TMP/bin/az" ] || { echo "REFUSING: the az shim is not first on PATH" >&2; exit 11; }; fi
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"
[ -d "$CLAUDE_CONFIG_DIR" ] || { echo "REFUSING: Tuesday's claude store $CLAUDE_CONFIG_DIR is absent" >&2; exit 11; }
# 64 (cont.) — nothing a product process could use to reach a real provider is inherited from this shell.
unset DATABASE_URL TEST_DATABASE_URL AGENTMAIL_API_KEY AGENTMAIL_INBOX ACS_CONNECTION_STRING ACS_EMAIL_CONNECTION_STRING ACS_EMAIL_SENDER \
      MAIL_SENDER TABLES_CONNECTION_STRING AZURE_BACKUP_CONN_STR SESSION_SECRET HPAM_WORD ADVANCED_UNLOCK_SECRET SALES_COPY_EMAIL \
      FEEDBACK_NOTIFY_EMAIL FEEDBACK_NOTIFY_EMAILS APPROVALS_INBOX NTFY_TOPIC NTFY_SERVER LEAD_BOT_API_KEY WEBSITE_SITE_NAME COORDINATOR_SECRET \
      PORT NODE_ENV PUPPETEER_EXECUTABLE_PATH PAGE_RATE_LIMIT_PER_10_MIN OTP_IP_BUDGET_PER_HOUR OTP_GLOBAL_BUDGET_PER_HOUR GH_TOKEN GITHUB_TOKEN \
      GH_ENTERPRISE_TOKEN GITHUB_ENTERPRISE_TOKEN DOCKER_HOST DOCKER_CONTEXT
export npm_config_update_notifier=false
echo "identity: AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR (AZ-READ-LEG $AZLEG) GH_CONFIG_DIR=$GH_CONFIG_DIR (GH-API-LEG $GHLEG) CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR" >&2

PROMPT="$PROMPT

$PIN_BLOCK"
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model "$MODEL" "$PROMPT"
