#!/bin/bash
# launch_qa_vision_qq_gate23.sh — cross-project QA agent, ONE gate (Vision gate 23; drafted 2026-10-18 ~06:09-06:5x AEDT by a read-only drafting
# agent for Tuesday, from launch_qa_vision_qq_gate22.sh, with gate 18's PR-#8 guards).
# Datasec/Vision_Sales_Portal, QuickQuote repo: ONE target, TIER 1 (the runtime that renders the customer's quote PDF + workbook), ONE verdict:
#   QQPB  fix/qq-puppeteer-25-2026-09-22  PR #8 @ 4d6ed6e  puppeteer-core 25.0.2 + node:22 image (C-19); clears Dependabot extract-zip #1 #4
#
# PR #8 sits on e4ce536 and is 4 BEHIND main 437ab4b (= LIVE v0.6.4-tool2.36-437ab4b). The gate measures THE MERGE RESULT "M8" = PR #8 merged onto
# 437ab4b, whose tree this launcher RECOMPUTES read-only (python over git ls-tree) and refuses unless it is 8077fdc = GitHub's test merge 7378a4e.
# THIS GATE PINS MAIN EXACTLY: a moved main REFUSES. PR #10 (f31720e) is the interaction column; a move of it is a NOTE.
#
# THE HEADS LIVE IN ONE PLACE: the brief's PIN-HEADS table. This launcher PARSES it, refuses any placeholder, verifies every row against the
# object store and against origin by `git ls-remote` NOW, and appends the verified table to the agent's prompt.
#
# PRODUCTION IS LIVE (hpas-quickquote / hpasqqacr; datasec-sales-portal-rg). This gate runs NO az. Docker only if IMAGE-LEG (D7) rules an image leg.
#
# GUARDS — gate 22's numbering kept where the guard survives; changes:
#   - PIN: two rows (MAIN-Q 437ab4b, QQPB 4d6ed6e base e4ce536 x3). Exact parents for 3d0167e / 0d45100 / 4d6ed6e and for main's side
#         (437ab4b = 9d1c5ab + 818a019; 9d1c5ab = e4ce536 + 5f08fe0; 818a019 <- 9d1c5ab; 5f08fe0 <- e4ce536); EXACTLY 4 behind main; trees.
#   - 22/23: PR #8's 5-file set + numstat; main's 4-file side; the ONLY non-comment line changes in each PR #8 file; the shared file is package.json
#         only, in disjoint hunks; PR #10's overlap with PR #8 is package.json only.
#   - 25 (NEW): the merge model — merged package.json blob f0df06f, M8 tree 8077fdc (control: 437ab4b unchanged -> c71780c; 4d6ed6e from e4ce536 ->
#         01bdc92); M8P10 package.json 23cc8c9 and tree d809de1.
#   - 74: blobs; the lockfiles (head: puppeteer-core 25.0.2, no extract-zip, engines >=22.12.0; main: extract-zip 2.0.1); puppeteer-core/lib/cjs only in the
#         two files PR #8 rewrites (at 437ab4b and f31720e) and nowhere at 4d6ed6e; Dockerfile FROM lines; tests.yml node-version 22 x5; .github = tests.yml.
#   - 31: the builder's READY on disk by sha256 with its NOT TESTED block; gate 22's report and tools; gate 18's kit; CLARIFICATIONS C-19 + C-20.
#   - 45: IMAGE-LEG NONE -> brief and prompt forbid docker, none is run here; ARM64-NATIVE / AMD64 -> docker answers, buildx lists the platform,
#         no qa-g23-* object exists yet (read-only docker calls).
#   - 44: Chrome, gitleaks, pdftotext/pdftoppm/pdfinfo/pdffonts present.
#   - 38R: negative-control seats derived live; the `tuesday` pane REQUIRED, the builder pane OPTIONAL (none live at drafting).
#   - 47 48 49 50 41 32 are the coordinator's to-do guards (AZ-PRE-READ, TARGET-MODE D6, IMAGE-LEG D7, NPM-AUDIT D8, routing, stamps): run LAST,
#         reported TOGETHER, exit with the first pending code. TARGET-MODE FORWARD-MERGE-FIRST is a hard refusal (nothing to launch).
#
# LAUNCH IT IN A TMUX PANE:
#   /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add 'QA/Vision-gate23' "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_vision_qq_gate23.sh'"
#   NEVER nohup, never bare from a seat's shell.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# --check is READ-ONLY: git read verbs (cat-file, rev-parse, merge-base, log, rev-list, diff, show, ls-tree, ls-remote, grep); tmux list-panes; ps;
# grep/python/shasum over files; docker version / buildx ls / images / ps ONLY when IMAGE-LEG names an image leg. It creates no identity dir,
# writes nothing and starts no claude.
# Usage: launch_qa_vision_qq_gate23.sh [--check]
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
BRIEF="$BRIEFS/2026-10-18_vision-gate23-qq-pr8-puppeteer25-node22.md"
READY="$BRIEFS/2026-10-16_vision-qq-pr8-READY-mail.txt"
READY_SHA='201da80e6e76e1c7835271d9c703dd15eee6b48ac86563794d887e027fc1ecd6'
G18_KIT="$BRIEFS/2026-10-16_vision-gate18-qq-pr8-puppeteer25.md"
CHARTER="$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"
MODELS_JSON="$TUE/0_Brain/dashboard/data/models_latest.json"
MODEL_PIN='claude-opus-5-5'
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
VSP='/Volumes/Laptop-DEV/!CODING/Datasec/Vision_Sales_Portal'
Q_REPO="$VSP/Quoting Tool/hpas-quoting-tool"
VSP_GH="$VSP/4_Credentials/.gh-config"
CLAR="$VSP/1_Project_Definition/CLARIFICATIONS.md"
REPORTS="$QA_DIR/projects/vision/reports"
G22_DIR="$REPORTS/2026-10-17-vision-gate22-qq-pr10-r3"
G22_REPORT="$G22_DIR/report.md"
G22_TOOLS="$G22_DIR/evidence/tools"
REPORT="$REPORTS/2026-10-18-vision-gate23-qq-pr8-puppeteer25-node22/report.md"
ROUTE_NAME='QA/Vision-gate23'
BUILDER_PANE='Datasec/Vision_Sales_Portal'
CHROME_BIN='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
PR_NUM='8'
PR_MERGE_SEEN='7378a4e1206afb6c2429ca9a9c74c30b52d40c39'     # refs/pull/8/merge at 06:09:46 (GitHub's test merge over 437ab4b; NOT in the local store)
P10_BRANCH='fix/qq-email-matches-print-2026-10-16'
ANCHOR_MAIN='437ab4bc412bc74d8da3b66a6ac5c71d7335c5d6'      # QuickQuote main = LIVE v0.6.4-tool2.36-437ab4b
MAIN_P='9d1c5ab8bc89aa2ba6b0063c22a858955d05a3e7 818a019ea21c39c5ef0a228f6242e7bdbb072761'
C9D='9d1c5ab8bc89aa2ba6b0063c22a858955d05a3e7'; C9D_P='e4ce5367761e03db982189a3f21758aa06714a85 5f08fe035f39ddc13e8260de1dde0d5d623f18d5'
C818='818a019ea21c39c5ef0a228f6242e7bdbb072761'
CGUARD='5f08fe035f39ddc13e8260de1dde0d5d623f18d5'
MB='e4ce5367761e03db982189a3f21758aa06714a85'               # PR #8's merge-base (main at its last forward-merge)
C1='3d0167ebe1909a301ac881c30f55f717c7801dd3'; C1P='47eb533034108c5c92d6b36af44554528ffc71ec'
C2='0d451004c746608922ddf874b48ce0f19048bf20'; C2P='3d0167ebe1909a301ac881c30f55f717c7801dd3 51e92867930efd4c98b28dc5d95baf82219b3edb'
HQ_EXPECT='4d6ed6ef403ef8962ded8211b76c3c6809bbb8c3'; HQ_P='0d451004c746608922ddf874b48ce0f19048bf20 e4ce5367761e03db982189a3f21758aa06714a85'
HQ_TREE='01bdc924daeafa59879462af5960bc4fa86875d3'
MAIN_TREE='c71780c82ea9cc338181163cb9d6045e07595e4f'
P10='f31720ee677dbe2deb53dcb7991f1683a1b03ce1'; P10_TREE='ee51fa7328b6cddaccc5e85593fd1443f150e411'
M8_TREE='8077fdc65d39be92d27aba11ebed33586b00440a'          # = GitHub's refs/pull/8/merge (7378a4e) tree
M8_PKG='f0df06fc2a313343e48c80b8445df7a0362363e2'
M8P10_TREE='d809de1dd44bd7a0624fcf17dd50636f1acfcb79'       # drafter's prediction; the gate proves it
M8P10_PKG='23cc8c95180973f112ebd3d58f47f8d337efc5fc'
DELTA_FILES='stage3/Dockerfile stage3/package-lock.json stage3/package.json stage3/test/fixtures/hang-close.cjs stage3/test/lib-close-shared.test.mjs'
NUMSTAT_PR8='4/1/stage3/Dockerfile 76/518/stage3/package-lock.json 1/1/stage3/package.json 3/1/stage3/test/fixtures/hang-close.cjs 1/1/stage3/test/lib-close-shared.test.mjs '
NUMSTAT_MAINSIDE='1/1/index.html 1/1/stage3/package.json 28/1/stage3/strip.js 175/0/stage3/test/email-print-mode.mjs '

SUBJECT_STEM='[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 23'
QUESTION_SUBJ='[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>'
ANSWER_PREFIX='[Tuesday -> QA/Vision-gate23] ANSWER'
STATUS_SUBJ='[QA/Datasec-Vision -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch'
PARK_LINE='PARKED: flagged — awaiting the Opus 4.8 switch'

q() { git --no-optional-locks -C "$Q_REPO" "$@"; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE gate (Vision gate 23) on Datasec/Vision_Sales_Portal, in the QUICKQUOTE repo: ONE target, TIER 1 (the runtime that renders every emailed quote PDF and workbook a customer receives), ONE verdict, GO / GO WITH FINDINGS / NO GO. The target QQPB (TIER 1; round 1 at a launched gate: gate 4 gated an older head, gate 18 was drafted and never run) is QuickQuote PR #8, branch fix/qq-puppeteer-25-2026-09-22 at 4d6ed6e: puppeteer-core 23.11.1 -> 25.0.2 (ESM-only; needs node >= 22.12) and the stage3 image FROM node:20-bookworm-slim -> node:22-bookworm-slim, two test files re-pointed at puppeteer-core/internal/cdp/Browser.js, and a lockfile with extract-zip removed, which is what clears Dependabot alerts #1 and #4 (extract-zip, high, no patched version). This is Kam's C-19 (card quickquote-decision14-puppeteer25-node22-1016 = b: "Build the puppeteer 25 + node 22 change now"; "merge on Tuesday's GO"; publishing the new runtime is NOT covered). C-20 (card quickquote-email-sends-standard-not-custom-1016 = a) binds the publish: "Fix (2) and PR #8 (C-19) each need Kam's own word before any publish." Nothing publishes on your verdict. PR #8 sits on e4ce536 and is FOUR commits BEHIND QuickQuote main 437ab4b, which is what is LIVE (v0.6.4-tool2.36-437ab4b; the brief's AZ-PRE-READ, appended below, is Tuesday's reading); main gained the email guard (PR #9) and v2.36 (PR #11) since. Everything the builder measured was against e4ce536. You gate THE MERGE RESULT M8 = PR #8 merged onto 437ab4b (tree 8077fdc, which equals GitHub's own test merge refs/pull/8/merge 7378a4e; no CI has ever run on it), plus the raw head H8 = 4d6ed6e, as the brief's TARGET-MODE (appended below) sets. Main's page, server, renderer and strip.js are byte-identical in BASE (437ab4b) and M8: everything that can differ is the runtime. PR #10 (f31720e, v2.39, gate 22 GO WITH FINDINGS, not merged, waiting on Kam's open publish card quickquote-v239-custom-price-fix-publish-1017) touches the same stage3/package.json in a disjoint hunk; M8P10 = 437ab4b + PR #8 + PR #10 (predicted tree d809de1) is your interaction column. This machine is Kam's Mac mini, working volume /Volumes/Laptop-DEV; host Node is v26.8.1 only (no Node 20 or 22 installed); the T9 QuickQuote repo is STALE, never read it.

READ YOUR COMMISSION FIRST, whole: /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-18_vision-gate23-qq-pr8-puppeteer25-node22.md
Then read the charter it names, the Vision CLARIFICATIONS (C-01..C-20; C-19 and C-20 are Kam's rulings), the project's CLAUDE.md (/Volumes/Laptop-DEV/!CODING/Datasec/Vision_Sales_Portal/CLAUDE.md, its QuickQuote section; its deploy commands are not for you), the QuickQuote repo's own CLAUDE.md at 437ab4b (git show; its publish lines are not for you), the builder's READY mail, read WHOLE (/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-16_vision-qq-pr8-READY-mail.txt; written against e4ce536; it carries a NOT TESTED block), gate 18's never-run kit for PR #8's own traps (/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-16_vision-gate18-qq-pr8-puppeteer25.md), and gate 22's report (/Volumes/Laptop-DEV/!CODING/Testing Agent MAIN/projects/vision/reports/2026-10-17-vision-gate22-qq-pr10-r3: its VERDICT, its N6 suite sets at 437ab4b and f31720e, its section 12 re-run list for "if PR #8 merges first", its NOT TESTED; its evidence/tools/ holds the instruments you copy). Every builder statement is a CLAIM, never evidence. RE-DERIVE every suite set, every artefact comparison, every advisory reading and every tree hash yourself. Verify every PRIOR WORK claim against git history and the Actions API, never against the brief. The brief's WRONG list, MODEL RULE and TUESDAY'S RULINGS (R1-R7 and the stamped D4, D6, D7, D8) are stamped: apply them, do not re-rule them.

WHAT THE BRIEF REQUIRES, in short (the brief is the authority):
(1) THE DIFF AND THE MERGE RESULT: PR #8's five files hunk by hunk (the only non-comment changes: the FROM line, the puppeteer-core range, the lockfile, two require lines); main's side since e4ce536; the one shared file (stage3/package.json) in disjoint hunks; GitHub's compare API for main...4d6ed6e, 437ab4b...7378a4e and both directions between 4d6ed6e and f31720e. BUILD M8 and M8P10 from the object store by overlay (git archive 437ab4b or f31720e; git show 4d6ed6e:<path> for the four files main never touched; only PR #8's package.json hunk by patch), assert the merged package.json blobs f0df06f / 23cc8c9, and PROVE the tree hashes 8077fdc / d809de1 by git write-tree in a scratch repo of YOUR OWN. Never merge in their repo; git merge-tree --write-tree only from your OWN object dir.
(2) THE CI SUITES ON THE HOST as SETS, NOT COUNTS, at BASE, M8 (x2), H8, P10 and M8P10: root node --test quote-engine.test.mjs; in stage3/: npm test, npm run test:print, npm run test:xlsx. npm ci --offline --ignore-scripts only, the lockfile proven entry by entry (lockcmp.py AND lockwalk.py), npm ls --all. M8's names = BASE's; M8P10's = P10's. The fixture red-first at M8 (the two test files set back to their base blobs: lib-close-shared fails at load, BC-F1 on MODULE_NOT_FOUND). Host Node is 26.8.1, not CI's 22: say so on every row. test:azurite is READ from CI only, and CI ran 4d6ed6e, not M8.
(3) THE FIXED SYNTHETIC QUOTE SET S1-S16, BASE vs M8, BYTE-OR-SEMANTICALLY EQUAL: your harness runs each tree's hosted server module's createApp() export in-process (never its entry point) with the repo's in-memory store pattern, a CAPTURING stub mail, a salesCopy option on a .invalid domain, throwaway session and unlock secrets (never a real secret, never the HPAM word), the tree's own renderQuotePdf, a frozen clock (the same instant in both trees), on 127.0.0.1 and a kernel port. ONE Google Chrome, the SAME binary for both trees, through your egress-block wrapper, driven by the tree's OWN puppeteer-core, signs in with the captured OTP, unlocks advanced through the page's own controls, fills the form as a rep, picks the print mode by its label, captures the page's own Generate output as a PDF in print media A4 (light and, where the row says, dark), and presses the page's own Email button. EQUAL = byte-equal after normalising ONLY the PDF CreationDate / ModDate / ID / Producer-version tokens and the workbook's docProps/core.xml, OR semantically equal (pdftotext -layout text, pdfinfo pages and A4, pdffonts, pdftoppm -r 100 pixels in plain python with no ImageMagick, PIL or numpy, workbook parts or cell values and formats), plus the captured mail and the POST answer equal. BASE-vs-BASE must be EQUAL first; a planted one-word, one-digit, one-pixel and one-cell change must each be reported; AUD vs CAD must differ. THE INTERACTION COLUMN: gate 22's 9 advanced cells + 3 simple at P10 vs M8P10, and within M8P10 the emailed PDF equal to the printed PDF by gate 22's FULL-TEXT rule.
(4) PUPPETEER 23 -> 25 AT RUNTIME: the ESM-only entry and lib/pdf.js's require of it; every puppeteer-core file the runtime resolves; any ExperimentalWarning; the stub patching the renderer's real CdpBrowser class (proved from your harness only) and the disarm mutants G23-M1 / G23-M2; the API drift table, page.pdf's options and both versions' defaults read from YOUR installed trees.
(5) NODE 22 AS RECORDED: tests.yml's five node-version 22 jobs and, from CI's job logs, the Node version setup-node resolved and any EBADENGINE line; the Dockerfile at M8 (FROM node:22-bookworm-slim, floating, no digest); the lockfile engines (>= 22.12.0); App Service as the repo records it (a container, so its Node is the image's; no NODE| stack setting), with AZ-PRE-READ's DOCKER| prefix RELAYED as the live confirmation. You never read the live host. The Node-20-cannot-load-25 red proof runs only in an image leg.
(6) THE IMAGE LEG only as the brief's IMAGE-LEG (appended below) rules: NONE means NO DOCKER at all, not even docker images or docker ps; ARM64-NATIVE or AMD64 means gate 18's image method with qa-g23-* names only, base 437ab4b and head your M8 tree, one build window, every product container --network none, never a push, login, prune, rmi, rm or registry tag, never a foreign docker object.
(7) THE TWO DEPENDABOT ALERTS CLEARED AND NO NEW ADVISORIES: extract-zip absent from H8, M8 and M8P10 lockfiles and installed trees (found at BASE: the control); the Dependabot alerts list (#1, #4 open pre-merge); the dependency-review compare for 437ab4b...4d6ed6e AND 437ab4b...7378a4e (extract-zip@2.0.1 removed with both GHSAs; vulnerabilities on every added package); the GitHub Advisory Database per added or changed name@version, after its positive control (extract-zip@2.0.1 returns both GHSAs); npm audit only as NPM-AUDIT (appended below) rules; what Tuesday must read after a merge (#1 and #4 state fixed). Never dismiss an alert.
(8) GITLEAKS: a planted throwaway credential-shaped string in a scratch copy of YOUR tree found first; then gitleaks git over e4ce536..4d6ed6e and e4ce536..437ab4b with GIT_OPTIONAL_LOCKS=0 and --redact, and gitleaks dir over your BASE and M8 trees without node_modules (and M8's node_modules separately, rule ids and counts only). A finding new in PR #8 is a FAIL; a BASE finding is pre-existing. Never print a value.
(9) NOTHING PUSHED, MERGED OR PUBLISHED: your command log proves no push, merge, az, GitHub write, request to the live site, and (under IMAGE-LEG NONE) no docker; the live webapp's linuxFxVersion is RELAYED from AZ-PRE-READ (Tuesday re-reads at verdict); what a publish would ship once PR #8 is on main (the new runtime, whatever card authorised the publish), READ ONLY; deploy-on-merge READ ONLY.
(10) CI AND CODEQL on PR #8 at 4d6ed6e, READ ONLY, by GH-API-LEG: runs 38837565972 (push), 38837589895 (pull_request), 38837588311 (dynamic CodeQL) and their jobs and logs, the 13 check runs, code-scanning open on main and both PR refs (a blind instrument: say only what it can show), and that no run exists for 7378a4e; whether a merge needs a fresh CodeQL result (UNVERIFIED unless the ruleset read says).
(12) THE ORDER: report both merge orders with their costs. (A) PR #10 first: PR #10 lands exactly as gate 22 gated it and its publish ships v2.39 on today's runtime; PR #8 then lands as M8P10. (B) PR #8 first: gate 22's section-12 re-run cells apply to PR #10 (say which of them your M8P10 rows cover and which they do not), and a v2.39 publish would then carry Node 22 + puppeteer 25. The ruling is Tuesday's.
GH-API-LEG (appended below by the launcher as the brief sets it): READ-ONLY-VISION-TOKEN means gh is on your PATH as a GET-only shim over Vision's gh config — gh api GET reads only, never -X/--method, -f/-F/--field/--raw-field/--input or graphql, never a comment, review, label, approval, re-run or dismissal; NOT-RUN means none. AZ-READ-LEG is TUESDAY-READS: you run no az at all. Never open any file under the project's 4_Credentials.

PRODUCTION IS LIVE for this project. NEVER the live QuickQuote (hpas-quickquote, hpas-quickquote-rg, hpasqqacr, its Table Storage, its log workspace) and NEVER the live portal (datasec-sales-portal.azurewebsites.net, datasec-sales-portal-rg), nor any azurewebsites.net host: no HTTP request, not even a GET; press nothing there. The live check is Kam's: never read, ask for or type the HPAM word, and never read, print or grep the access word, the offline page's constant or the ADVANCED SEAM of index.html. No az; no deploy, no publish, no app-setting change, no ACR build, no registry push. Never the FX hosts (blocked by your wrapper; every rate is the seeded table), never ntfy.sh. Never Claude in Chrome (Kam's own Chrome with his sign-ins). NO EMAIL TO ANY HUMAN ADDRESS: every send goes to your capturing stub mail on .invalid addresses; your own AgentMail calls go only to tuesday-agent@agentmail.to. NETWORK, and only this: git ls-remote origin; gh api GETs if GH-API-LEG allows; your AgentMail calls; NX-1 (Docker Hub, Debian apt, the npm registry inside an image build) only if IMAGE-LEG rules an image leg; NX-2 (npm audit) only if NPM-AUDIT is RUN. Otherwise no npm registry (npm ci --offline) and no image pulls.

ONE BROWSER AT A TIME: never two drive Chromes of yours alive at once (a suite's own Chromes count); never a suite and a browser drive concurrently; one retry per cell at most, then NOT RUN with the load.

HELD: no merge, no push, no publish, no comment or status on PR #8 or PR #10, no alert dismissal, no mail to any human. TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT on this drive from the object store (git archive into a fresh mktemp -d under projects/vision/work-g23/ in /Volumes/Laptop-DEV/!CODING/Testing Agent MAIN), M8 and M8P10 by the brief's overlay. Each tree is EXCLUSIVE to this gate and to one purpose; never touch any other work directory (work-g19 to work-g22 included). The builder's checkout is LIVE: never read any working tree as evidence; never use the name main in the repo, only the pinned 40-hex shas. Copy gate 22's instruments into YOUR evidence/tools and re-point them (they hard-code work-g22, the gate-22 report folder, @qa-g22.invalid and v2.39); never run from, edit or write into gate 1-22's copies. Never npm install, never npm audit fix, never npx anything not already in the tree. In the repo use ONLY read verbs (show, log, diff, ls-remote, rev-parse, ls-tree, cat-file, grep, merge-base, archive; gitleaks' own git log under GIT_OPTIONAL_LOCKS=0); never fetch, pull, checkout, switch, worktree, commit, stash, reset, clean, gc, branch, revert or for-each-ref. Findings-only: no writes in the QuickQuote repo, none inside Vision_Sales_Portal, none in gate 1-22's report folders or trees. Never rm: quarantine. Run every loop and every git show <sha>:<path> under bash (zsh does not word-split an unquoted variable). Run node strip.js before any lone browser file. Assert every tamper landed (node --check rc 0; a file that does not parse is VOID) and never let a landed-check quote the form it replaces. CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY: BASE-vs-BASE equal before any BASE-vs-M8 zero; planted differences reported; extract-zip found at BASE; the advisory DB's positive control; gitleaks' planted string; the fixture revert red; each mutant LANDED; the tree-hash method reproducing c71780c for 437ab4b unchanged; a control derived from the run it validates is not a control.

FLOOR DISCIPLINE. Vision has no jest lock; never borrow NexusAI's. Never use host ports 4848, 8080 or 47787; host processes take every port from the kernel and bind 127.0.0.1; if an instrument needs a fixed port use only 47310-47319, after an lsof check. Every host product process runs under env -i with an explicit allowlist, NODE_ENV never production. Never set AGENTMAIL_API_KEY or AGENTMAIL_INBOX in a product process (with both set, QuickQuote SENDS FOR REAL), nor any real ACS_* or MAIL_SENDER, TABLES_CONNECTION_STRING, SALES_COPY_EMAIL, HPAM_WORD, ADVANCED_UNLOCK_SECRET, SESSION_SECRET, WEBSITE_SITE_NAME, GH_TOKEN or GITHUB_TOKEN; print each product process's env KEY NAMES and assert none is forbidden. NTFY_SERVER=http://ntfy.invalid; never contact ntfy.sh. EGRESS INCLUDING CHROME CHILDREN: every Chrome runs under your copy of the egress-block wrapper as PUPPETEER_EXECUTABLE_PATH; prove the block with its positive control and run the net-log scan at the end; record GoogleUpdater and chrome_crashpad_handler at start and end; reap every Chrome and every app listener by the pid you started. Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid, at START and at END, with the negative-control seats the launcher derived (listed at the end of this prompt) classifying FOREIGN in the same run. A zero is reportable only beside an ATTACHED control that fired in the same window. Record the load average beside every timing number; a latency result with no load figure is not a measurement.
DEADLINE AND HEARTBEAT: every step has a written DEADLINE built into your runner (there is no timeout binary here) and releases its Chromes, pages, children, app servers, containers (stopped by the id you started, never removed) and temp profiles in a finally. Log a HEARTBEAT line at least every 2 minutes; a step with no heartbeat for 5 minutes is aborted and reported, never waited on. Deadlines: one browser cell 120 s; one red-proof or mutant arm 420 s; the root pack 120 s; a whole npm test 300 s; a whole test:xlsx 300 s; a whole test:print 900 s; nothing above 900 s on the host (an image leg's own deadlines are the brief's section N6). Under the brief's D4, M8's four suites as sets, S1-S12 at BASE and M8 with the BASE-vs-BASE control, the extract-zip and advisory reads (N7.1-N7.3) or gitleaks (N8.1-N8.2) NOT RUN makes the verdict PROVISIONAL.

THE MODEL RULE (Kam, live board 2026-09-30 09:07, card (b)): QA gates may switch to Opus 4.8 when flagged by Opus 5.5's safeguards, PER SESSION. You start on Opus 5.5. You run the FULL rows. If one of your responses is stopped by the safeguards: that step is NOT RUN (never re-worded to slip past); write ONE line to evidence/classifier-stops.txt; reap any Chrome, app server and container you started; mail tuesday-agent@agentmail.to with the subject exactly "[QA/Datasec-Vision -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch"; then end your turn with the line "PARKED: flagged — awaiting the Opus 4.8 switch" and wait. Tuesday switches THIS pane's model and taps you by mail. You never answer the model dialog yourself, and nobody ever chooses "Switch automatically". After the switch, resume at the stopped row. The report states which rows ran on which model, with the switch time, and quotes classifier-stops.txt whole.

QUESTIONS: your routing name is QA/Vision-gate23. If you must ask, mail tuesday-agent@agentmail.to with the subject "[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>" and proceed on the safest reading without waiting (the one exception is a safeguards stop, which PARKS you under THE MODEL RULE). Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/Vision-gate23] ANSWER"; read it with your verdict key. Never wednesday-agent@. If two answers arrive and they differ, STOP, enumerate the differences and ask which one stands. If a response is cut off by a safety check, record it and continue with the next item; this is authorised defensive QA of Datasec's own product on loopback. Approval-class items (a merge, a publish, a deploy, the live site, money, a human) are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your report to: /Volumes/Laptop-DEV/!CODING/Testing Agent MAIN/projects/vision/reports/2026-10-18-vision-gate23-qq-pr8-puppeteer25-node22/report.md
You create that folder. Write its VERDICT and FINDINGS table early and keep it current. Number findings G23-F1, G23-F2, …

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with a subject beginning exactly:
[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 23: QQPB @ <sha7> <GO | GO WITH FINDINGS | NO GO>
(the sha7 is the pinned head from the verified table below; append PROVISIONAL if the brief's D4 clause applies). Lead the body with ONE sentence as the brief's section 14 words it (M8's suites as sets against main; every S-row's emailed PDF, workbook, mail and print byte-or-semantically equal to main's with BASE-vs-BASE holding; extract-zip gone with no new advisory; gitleaks; the combination with PR #10; anything pushed, merged or published), then a line "VERDICT: <token>, round 1 (…)" with what happens next (Tuesday's merge GO in the order she rules; the publish is Kam's own word), then one line each on M8's tree proof, the suite sets, the S-rows, the interaction column and the two orders, the puppeteer runtime, Node 22 as recorded and the image leg, the alerts and advisories, gitleaks, the live site read (RELAYED), what a publish would ship, and the class count. You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/Laptop-DEV/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no credentials directory of its own. Use it only in your own mail calls, with a client timeout. Never put the key or any secret in a mail, the report or a product process.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice — the only turn you end while waiting is the PARKED line of THE MODEL RULE.

Report the pinned head and main as three timestamped readings (start / mid / end), with the branch name beside each, plus refs/pull/8/head, refs/pull/8/merge and refs/pull/10/head. Include a table with one row per brief section N item: MEASURED, NOT TESTED, NOT RUN or VOID, and HOW (command, tree, browser, port, load).

Rule 2 stands: what you did NOT test is first-class output. Write a NOT TESTED section that covers at least Node 22 itself unless an image leg ran (host Node is 26.8.1; CI is read only, never caused), the published amd64 image and ACR's native build, the image's own CMD booted with production settings, a real ACS send, the live site (Kam's check), CodeQL's verdict on the current merge ref (blind), Dependabot #1 and #4 reading fixed (post-merge, Tuesday's), store-azurite on M8, npm audit (per NPM-AUDIT), a live FX provider, currencies other than AUD/USD/CAD, Windows, Safari, real phones, real printers and the account managers' real browsers, a customer's mail client, Claude in Chrome (not used), and every row you did not run. Label every action recommendation MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. The tester never fixes.
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
[ "$(fld QQPB 4)" = "$HQ_EXPECT" ] || { echo "REFUSING: QQPB's PIN head $(fld QQPB 4 | cut -c1-7) is not ${HQ_EXPECT:0:7} — this launcher's content guards are pinned to it; re-brief" >&2; exit 40; }
MAINH="$(fld MAIN-Q 4)"
HQ="$(fld QQPB 4)"

# 6 — every sha the guards use is a commit in the local object store (this launcher never fetches).
for S in "$MAINH" "$HQ" "$ANCHOR_MAIN" $MAIN_P $C9D_P "$C818" "$CGUARD" "$MB" "$C1" "$C1P" "$C2" $C2P "$P10"; do
  T="$(q cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in the QuickQuote repo on this drive (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 9m — MAIN: 437ab4b EXACTLY (refuse if it moved).
[ "$MAINH" = "$ANCHOR_MAIN" ] || { echo "REFUSING: the pinned MAIN ${MAINH:0:7} is not 437ab4b — this gate pins main exactly; re-brief" >&2; exit 9; }

# 7 / 8 — the target: base as briefed, ancestor AND merge-base with MAIN, not on main, exact count, EXACTLY 4 behind.
H7="${HQ:0:7}"; BASE="$(fld QQPB 5)"; N="$(fld QQPB 6)"
[ "$BASE" = "$MB" ] || { echo "REFUSING: row QQPB base ${BASE:0:7} is not e4ce536 — re-brief" >&2; exit 7; }
q merge-base --is-ancestor "$BASE" "$HQ" 2>/dev/null || { echo "REFUSING: QQPB base ${BASE:0:7} is not an ancestor of $H7" >&2; exit 7; }
[ "$(q merge-base "$HQ" "$MAINH" 2>/dev/null)" = "$BASE" ] || { echo "REFUSING: QQPB merge-base(head, MAIN) is not its base ${BASE:0:7}" >&2; exit 7; }
q merge-base --is-ancestor "$HQ" "$MAINH" 2>/dev/null && { echo "REFUSING: QQPB $H7 is ALREADY ON MAIN ${MAINH:0:7} — the brief says it is not; re-brief" >&2; exit 7; }
GOTN="$(q rev-list --count "${BASE}..${HQ}" 2>/dev/null)"
[ "$GOTN" = "$N" ] && [ "$N" = "3" ] || { echo "REFUSING: QQPB $H7 has $GOTN commits over its base, the table says $N, this launcher's chain is three" >&2; q log --format='%h %p %s' "${BASE}..${HQ}" >&2; exit 8; }
[ "$(q rev-list --count "${HQ}..${MAINH}" 2>/dev/null)" = "4" ] || { echo "REFUSING: QQPB $H7 is not exactly 4 behind 437ab4b — the branch was forward-merged (or main is not what the brief read); re-brief" >&2; exit 7; }

# 9 — the exact chain by parents, and the trees.
par() { q log -1 --format='%P' "$1" 2>/dev/null; }
[ "$(par "$C1")" = "$C1P" ] || { echo "REFUSING: 3d0167e's single parent is not 47eb533" >&2; exit 9; }
[ "$(par "$C2")" = "$C2P" ] || { echo "REFUSING: 0d45100's parents are not 3d0167e + 51e9286" >&2; exit 9; }
[ "$(par "$HQ")" = "$HQ_P" ] || { echo "REFUSING: 4d6ed6e's parents are not 0d45100 + e4ce536" >&2; exit 9; }
[ "$(par "$ANCHOR_MAIN")" = "$MAIN_P" ] || { echo "REFUSING: 437ab4b's parents are not 9d1c5ab + 818a019" >&2; exit 9; }
[ "$(par "$C9D")" = "$C9D_P" ] || { echo "REFUSING: 9d1c5ab's parents are not e4ce536 + 5f08fe0" >&2; exit 9; }
[ "$(par "$C818")" = "$C9D" ] || { echo "REFUSING: 818a019's single parent is not 9d1c5ab" >&2; exit 9; }
[ "$(par "$CGUARD")" = "$MB" ] || { echo "REFUSING: 5f08fe0's single parent is not e4ce536" >&2; exit 9; }
[ "$(q rev-parse "${HQ}^{tree}" 2>/dev/null)" = "$HQ_TREE" ] || { echo "REFUSING: 4d6ed6e's tree is not 01bdc92" >&2; exit 9; }
[ "$(q rev-parse "${ANCHOR_MAIN}^{tree}" 2>/dev/null)" = "$MAIN_TREE" ] || { echo "REFUSING: 437ab4b's tree is not c71780c" >&2; exit 9; }
[ "$(q rev-parse "${P10}^{tree}" 2>/dev/null)" = "$P10_TREE" ] || { echo "REFUSING: f31720e's tree is not ee51fa7" >&2; exit 9; }
q merge-base --is-ancestor "$ANCHOR_MAIN" "$P10" 2>/dev/null || { echo "REFUSING: PR #10's f31720e is not on top of 437ab4b — the interaction column's premise is gone; re-brief" >&2; exit 9; }

# 18 — RE-PIN: BOTH rows AND refs/pull/8/head at origin, by ls-remote, read NOW. No movement allowed, main included. PR #10 and the test merge: NOTEs.
for ID in $EXPECT_IDS; do
  BR="$(fld "$ID" 3)"; H="$(fld "$ID" 4)"
  L="$(q ls-remote origin "refs/heads/$BR" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" && continue
  echo "REFUSING: row $ID: $H is not at refs/heads/$BR on origin — that ref moved, was never pushed, or ls-remote failed (UNKNOWN, not a value); re-pin and re-brief" >&2; printf '%s\n' "${L:-<nothing>}" >&2; exit 18
done
LP="$(q ls-remote origin "refs/pull/${PR_NUM}/head" "refs/pull/${PR_NUM}/merge" "refs/heads/${P10_BRANCH}" 2>&1)"
printf '%s\n' "$LP" | grep -q "^${HQ}[[:space:]]refs/pull/${PR_NUM}/head\$" \
  || { echo "REFUSING: refs/pull/${PR_NUM}/head is not ${H7} on origin — PR #${PR_NUM} moved or is not the target; re-pin and re-brief" >&2; printf '%s\n' "${LP:-<nothing>}" >&2; exit 18; }
PR_MERGE_NOW="$(printf '%s\n' "$LP" | awk -v r="refs/pull/${PR_NUM}/merge" '$2==r{print $1}')"
[ "$PR_MERGE_NOW" = "$PR_MERGE_SEEN" ] || echo "NOTE: refs/pull/${PR_NUM}/merge is '${PR_MERGE_NOW:-<absent>}', the drafter read ${PR_MERGE_SEEN:0:7} — GitHub recomputed its test merge; main is pinned, so read why before launch (guard 25 still proves M8's tree)" >&2
P10_NOW="$(printf '%s\n' "$LP" | awk -v r="refs/heads/${P10_BRANCH}" '$2==r{print $1}')"
[ "$P10_NOW" = "$P10" ] || echo "NOTE: PR #10's branch is '${P10_NOW:-<absent>}', not f31720e as briefed — the §N3.6 interaction column and §12 are stale; Tuesday decides whether to re-brief" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 / 23 — exact file sets and numstat; the ONLY non-comment line changes; the shared file and its hunks.
GOT="$(q diff --name-only "$MB" "$HQ" 2>/dev/null | sort)"
[ "$GOT" = "$(printf '%s\n' $DELTA_FILES | sort)" ] || { echo "REFUSING: QQPB ${H7}'s delta over e4ce536 is not exactly the briefed 5-file set. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }
ns() { q diff --numstat "$1" "$2" | awk '{printf "%s/%s/%s ", $1, $2, $3}'; }
[ "$(ns "$MB" "$HQ")" = "$NUMSTAT_PR8" ] || { echo "REFUSING: PR #8's numstat is not the briefed one. Got:" >&2; q diff --numstat "$MB" "$HQ" >&2; exit 23; }
[ "$(ns "$MB" "$MAINH")" = "$NUMSTAT_MAINSIDE" ] || { echo "REFUSING: main's side since e4ce536 is not the briefed 4-file delta. Got:" >&2; q diff --numstat "$MB" "$MAINH" >&2; exit 23; }
ncl() {  # non-comment changed lines of one file, PR #8's side
  q diff -U0 "$MB" "$HQ" -- "$1" | grep -E '^[+-]' | grep -vE '^(\+\+\+|---) ' | grep -vE '^[+-][[:space:]]*(#|//)'; }
[ "$(ncl stage3/Dockerfile)" = "$(printf '%s\n' '-FROM node:20-bookworm-slim' '+FROM node:22-bookworm-slim')" ] || { echo "REFUSING: the Dockerfile's non-comment change is not exactly the FROM line" >&2; ncl stage3/Dockerfile >&2; exit 23; }
[ "$(ncl stage3/package.json)" = "$(printf '%s\n' '-    "puppeteer-core": "^23.5.0"' '+    "puppeteer-core": "^25.0.2"')" ] || { echo "REFUSING: package.json's change is not exactly the puppeteer-core line" >&2; ncl stage3/package.json >&2; exit 23; }
for F in stage3/test/fixtures/hang-close.cjs stage3/test/lib-close-shared.test.mjs; do
  [ "$(ncl "$F")" = "$(printf '%s\n' '-const { CdpBrowser } = require("puppeteer-core/lib/cjs/puppeteer/cdp/Browser.js");' '+const { CdpBrowser } = require("puppeteer-core/internal/cdp/Browser.js");')" ] \
    || { echo "REFUSING: $F's non-comment change is not exactly the CdpBrowser require swap" >&2; ncl "$F" >&2; exit 23; }
done
SHARED="$(comm -12 <(q diff --name-only "$MB" "$HQ" | sort) <(q diff --name-only "$MB" "$MAINH" | sort))"
[ "$SHARED" = "stage3/package.json" ] || { echo "REFUSING: the files both PR #8 and main changed since e4ce536 are not exactly stage3/package.json: $SHARED" >&2; exit 23; }
SHARED10="$(comm -12 <(q diff --name-only "$MB" "$HQ" | sort) <(q diff --name-only "$MB" "$P10" | sort))"
[ "$SHARED10" = "stage3/package.json" ] || { echo "REFUSING: the files both PR #8 and PR #10 changed since e4ce536 are not exactly stage3/package.json: $SHARED10" >&2; exit 23; }
hunks() { q diff -U0 "$1" "$2" -- stage3/package.json | sed -n 's/^@@ -\([0-9]*\).*/\1/p' | tr '\n' ' '; }
[ "$(hunks "$MB" "$HQ")" = "21 " ] && [ "$(hunks "$MB" "$MAINH")" = "11 " ] && [ "$(hunks "$MB" "$P10")" = "11 " ] \
  || { echo "REFUSING: the package.json hunks are not PR #8 at line 21 and main / PR #10 at line 11 (disjoint) as briefed" >&2; exit 23; }

# 25 — THE MERGE MODEL, read-only: merged package.json blobs, M8's tree = GitHub's test merge, M8P10's predicted tree; with two controls.
python3 - "$Q_REPO" "$MB" "$HQ" "$ANCHOR_MAIN" "$P10" "$MAIN_TREE" "$HQ_TREE" "$M8_PKG" "$M8_TREE" "$M8P10_PKG" "$M8P10_TREE" <<'PY' || exit 25
import hashlib, subprocess, sys
repo, mb, hq, main, p10, main_tree, hq_tree, m8pkg, m8tree, m10pkg, m10tree = sys.argv[1:12]
def git(*a): return subprocess.run(['git', '--no-optional-locks', '-C', repo, *a], capture_output=True, check=True).stdout
def blobhash(b): return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()
def ls(tree):
    for rec in git('ls-tree', '-z', tree).split(b'\0'):
        if rec:
            meta, name = rec.split(b'\t', 1); mode, typ, sha = meta.split(b' ')
            yield mode, typ, sha.decode(), name
def thash(tree, repl, prefix=''):
    body = b''
    for mode, typ, sha, name in sorted(ls(tree), key=lambda e: e[3] + (b'/' if e[1] == b'tree' else b'')):
        p = prefix + name.decode()
        if typ == b'tree' and any(k.startswith(p + '/') for k in repl): sha = thash(sha, repl, p + '/')
        elif p in repl: sha = repl[p]
        body += (b'40000' if mode == b'040000' else mode) + b' ' + name + b'\0' + bytes.fromhex(sha)
    return hashlib.sha1(b'tree %d\0' % len(body) + body).hexdigest()
def rp(s, p): return git('rev-parse', f'{s}:{p}').decode().strip()
def fail(m): print('REFUSING: ' + m, file=sys.stderr); sys.exit(25)
if thash(main + '^{tree}', {}) != main_tree: fail('the tree-hash method does not reproduce 437ab4b\'s own tree c71780c — the merge model cannot be trusted')
four = {p: rp(hq, p) for p in ('stage3/Dockerfile', 'stage3/package-lock.json', 'stage3/test/fixtures/hang-close.cjs', 'stage3/test/lib-close-shared.test.mjs')}
if thash(mb + '^{tree}', dict(four, **{'stage3/package.json': rp(hq, 'stage3/package.json')})) != hq_tree: fail('the method does not rebuild 4d6ed6e\'s tree 01bdc92 from e4ce536 + its five blobs')
for p in four:
    if rp(main, p) != rp(mb, p) or rp(p10, p) != rp(mb, p): fail(f'{p} is not untouched by main / PR #10 since e4ce536')
OLD, NEW = b'"puppeteer-core": "^23.5.0"', b'"puppeteer-core": "^25.0.2"'
def merged_pkg(s):
    b = git('show', f'{s}:stage3/package.json')
    if b.count(OLD) != 1: fail(f'{s[:7]}:stage3/package.json does not carry the puppeteer-core ^23.5.0 line exactly once')
    return blobhash(b.replace(OLD, NEW))
if merged_pkg(main) != m8pkg: fail('the merged package.json (437ab4b + PR #8) is not blob f0df06f')
if thash(main + '^{tree}', dict(four, **{'stage3/package.json': m8pkg})) != m8tree: fail('M8\'s tree (437ab4b + PR #8) is not 8077fdc = GitHub\'s test merge')
if merged_pkg(p10) != m10pkg: fail('the merged package.json (f31720e + PR #8) is not blob 23cc8c9')
if thash(p10 + '^{tree}', dict(four, **{'stage3/package.json': m10pkg})) != m10tree: fail('M8P10\'s tree (f31720e + PR #8) is not d809de1 as briefed')
PY

# 74 — content, read from the pinned shas (never a checkout).
blob() { q rev-parse --verify -q "${1}:${2}" 2>/dev/null; }
has() { q show "${1}:${2}" 2>/dev/null | grep -qF -- "$3"; }
must() { has "$1" "$2" "$3" || { echo "REFUSING: ${1:0:7}:$2 lacks '$3' — the brief gates different code; re-brief" >&2; exit 74; }; }
mustnot() { has "$1" "$2" "$3" && { echo "REFUSING: ${1:0:7}:$2 still carries '$3' — the brief says it is absent there; re-brief" >&2; exit 74; }; return 0; }
# file | e4ce536 = 437ab4b blob | 4d6ed6e blob
for P in 'stage3/Dockerfile|8311ebebe385cb67d7ee384dcbcb00304d22a725|5972f7cabd44ebacdeefbdd394f7a9a6098d6926' \
         'stage3/package-lock.json|01c5e5e3415bed5afc7c30fc9bd1efc37fcb8d4e|9366344f72a6a152d7bd6164f20442a9fdf84b49' \
         'stage3/test/fixtures/hang-close.cjs|f902922507b6bcdf77d45d3c53fb684995b97ca2|8fe024cc72d98352e74eacb8423e0aa22621cae2' \
         'stage3/test/lib-close-shared.test.mjs|6f7921588439737aaaf1924d48c4b15251ff477e|d7c2b07929f8d2de125a12dc4dcc91edd8ea7f0f'; do
  F="${P%%|*}"; REST="${P#*|}"; B0="${REST%%|*}"; B1="${REST#*|}"
  [ "$(blob "$MB" "$F")" = "$B0" ] && [ "$(blob "$ANCHOR_MAIN" "$F")" = "$B0" ] && [ "$(blob "$HQ" "$F")" = "$B1" ] \
    || { echo "REFUSING: $F blobs are not ${B0:0:7} (e4ce536 = 437ab4b) | ${B1:0:7} (4d6ed6e)" >&2; exit 74; }
done
[ "$(blob "$MB" stage3/package.json)" = '61d0d5c51f2987750620a520844685746cc2bdcb' ] && [ "$(blob "$ANCHOR_MAIN" stage3/package.json)" = '1606aa3b4f0fa9b53811c7bc71f96cd57178a420' ] \
  && [ "$(blob "$HQ" stage3/package.json)" = '94ab2f56e854ce040c0cc89d8cca91015b0daf11' ] || { echo "REFUSING: stage3/package.json blobs are not 61d0d5c | 1606aa3 | 94ab2f5" >&2; exit 74; }
for F in stage3/server.js stage3/lib/pdf.js stage3/lib/xlsx.js .dockerignore .github/workflows/tests.yml; do
  B0="$(blob "$MB" "$F")"
  [ -n "$B0" ] && [ "$(blob "$ANCHOR_MAIN" "$F")" = "$B0" ] && [ "$(blob "$HQ" "$F")" = "$B0" ] || { echo "REFUSING: $F differs between e4ce536, 437ab4b and 4d6ed6e — the brief says it is one blob" >&2; exit 74; }
done
python3 - "$Q_REPO" "$HQ" "$ANCHOR_MAIN" <<'PY' || { echo "REFUSING: the lockfiles are not as briefed (head: puppeteer-core 25.0.2, @puppeteer/browsers 3.0.2, engines >=22.12.0, no extract-zip, 247 entries; main: extract-zip 2.0.1, puppeteer-core 23.11.1, 286 entries)" >&2; exit 74; }
import json, subprocess, sys
repo, h, m = sys.argv[1:4]
def lk(s): return json.loads(subprocess.run(['git','--no-optional-locks','-C',repo,'show',f'{s}:stage3/package-lock.json'],capture_output=True,check=True).stdout)['packages']
H, M = lk(h), lk(m)
ok = (H['node_modules/puppeteer-core']['version'] == '25.0.2' and H['node_modules/puppeteer-core']['engines']['node'] == '>=22.12.0'
      and H['node_modules/@puppeteer/browsers']['version'] == '3.0.2' and H['node_modules/@puppeteer/browsers']['engines']['node'] == '>=22.12.0'
      and not any('extract-zip' in k for k in H) and len(H) == 247
      and M['node_modules/extract-zip']['version'] == '2.0.1' and M['node_modules/puppeteer-core']['version'] == '23.11.1' and len(M) == 286)
sys.exit(0 if ok else 1)
PY
must "$HQ" stage3/Dockerfile 'FROM node:22-bookworm-slim'
must "$ANCHOR_MAIN" stage3/Dockerfile 'FROM node:20-bookworm-slim'
must "$HQ" stage3/lib/pdf.js 'const puppeteer = require("puppeteer-core");'
mustnot "$HQ" .dockerignore 'stage3/test'
[ "$(q show "${HQ}:.github/workflows/tests.yml" | grep -cE '^[[:space:]]+node-version: 22[[:space:]]*$')" = "5" ] || { echo "REFUSING: tests.yml does not carry five node-version: 22 jobs as briefed" >&2; exit 74; }
[ "$(q ls-tree -r --name-only "$HQ" .github)" = ".github/workflows/tests.yml" ] || { echo "REFUSING: .github at the head holds other than tests.yml — §N9.4's reading is wrong" >&2; exit 74; }
CJS_MAIN="$(q grep -l 'puppeteer-core/lib/cjs' "$ANCHOR_MAIN" -- stage3 2>/dev/null | sed "s/^${ANCHOR_MAIN}://" | sort | tr '\n' ' ')"
CJS_P10="$(q grep -l 'puppeteer-core/lib/cjs' "$P10" -- stage3 2>/dev/null | sed "s/^${P10}://" | sort | tr '\n' ' ')"
CJS_HQ="$(q grep -l 'puppeteer-core/lib/cjs' "$HQ" -- stage3 2>/dev/null | wc -l | tr -d ' ')"
WANT_CJS='stage3/test/fixtures/hang-close.cjs stage3/test/lib-close-shared.test.mjs '
[ "$CJS_MAIN" = "$WANT_CJS" ] && [ "$CJS_P10" = "$WANT_CJS" ] && [ "$CJS_HQ" = "0" ] \
  || { echo "REFUSING: puppeteer-core/lib/cjs is referenced other than by exactly the two files PR #8 rewrites (main: '$CJS_MAIN'; PR #10: '$CJS_P10'; head: $CJS_HQ)" >&2; exit 74; }
for T in 'npm ci --offline --ignore-scripts' 'entry by entry' 'never `npm audit fix`'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the dependency rule '$T'" >&2; exit 63; }
done
for T in 'npm ci --offline --ignore-scripts' 'entry by entry' 'never npm audit fix'; do
  printf '%s\n' "$PROMPT" | grep -qiF -- "$T" || { echo "REFUSING: prompt lacks the dependency rule '$T'" >&2; exit 63; }
done

# 31 — the builder's READY on disk byte for byte, with its NOT TESTED block; gate 22's report and tools; gate 18's kit; C-19 and C-20.
[ -s "$READY" ] || { echo "REFUSING: the builder's READY is not on disk: $READY" >&2; exit 31; }
[ "$(shasum -a 256 "$READY" | awk '{print $1}')" = "$READY_SHA" ] || { echo "REFUSING: $READY is not the copy the drafter read (sha256 differs) — re-read it and re-brief" >&2; exit 31; }
for T in 'READY FOR QA (tier 1): QuickQuote PR #8 @ 4d6ed6e' 'forward-merged with main e4ce536' 'audit --omit=dev: high 3 -> 0' '38837565972' \
         'NOT TESTED' 'An emulated linux/amd64 build + in-image render + test:print is RUNNING now' 'The live site, or a real emailed quote through ACS on the new runtime'; do
  grep -qF -- "$T" "$READY" || { echo "REFUSING: $READY does not carry '$T'" >&2; exit 31; }
done
grep -qF 'An emulated linux/amd64 build + in-image render + test:print is RUNNING now' "$BRIEF" || { echo "REFUSING: the brief does not carry the READY's NOT TESTED block verbatim" >&2; exit 31; }
for W in a b c d e f g h i j k l m n o p; do
  grep -qF -- "- **($W) " "$BRIEF" || { echo "REFUSING: the brief's WRONG list lacks item ($W)" >&2; exit 31; }
done
for T in 'GH-API-LEG' 'AZ-READ-LEG' 'AZ-PRE-READ' 'TARGET-MODE' 'IMAGE-LEG' 'NPM-AUDIT' 'ROUTING-LINE' \
         'D4' 'D6' 'D7' 'D8' 'PROVISIONAL' 'M8' 'M8P10' 'H8' 'P10' 'BASE-vs-BASE' 'G23-M1' 'G23-M2' 'G23-F1' 'S1-S16' 'NX-1' 'NX-2' '7378a4e' "$M8_TREE" \
         "$M8_PKG" "$M8P10_TREE" "$M8P10_PKG" 'GHSA-jmr9-qjv8-65gv' 'GHSA-7pqw-9j4j-h8q3' 'dependency-review' 'gitleaks' 'quickquote-v239-custom-price-fix-publish-1017' \
         'quickquote-decision14-puppeteer25-node22-1016' 'HPAM' 'live check' "$READY_SHA" '47310' 'DISCLOSED'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: the brief does not carry '$T'" >&2; exit 31; }
done
for R in 'R1: ' 'R2: ' 'R3: ' 'R4: ' 'R5: ' 'R6: ' 'R7: '; do
  grep -qF -- "- $R" "$BRIEF" || { echo "REFUSING: the brief does not carry Tuesday's ruling '$R' as a ruling line" >&2; exit 31; }
done
[ -s "$CLAR" ] || { echo "REFUSING: Vision CLARIFICATIONS.md absent: $CLAR" >&2; exit 31; }
for T in '**C-19.' 'Build the puppeteer 25 + node 22 change now' 'merge on Tuesday'"'"'s GO' 'publishing the new runtime to the live site (Kam'"'"'s separate tap)' \
         '**C-20.' 'Fix (2) and PR #8 (C-19) each need Kam'"'"'s own word before any publish'; do
  grep -qF -- "$T" "$CLAR" || { echo "REFUSING: CLARIFICATIONS does not carry '$T' — the ruling the brief quotes is not on disk" >&2; exit 31; }
done
grep -qF '**C-21.' "$CLAR" && echo "NOTE: Vision CLARIFICATIONS now has a C-21 — the brief says C-01..C-20; read it before launch" >&2
[ -s "$CHARTER" ] || { echo "REFUSING: the charter is absent: $CHARTER" >&2; exit 31; }
[ -s "$G18_KIT" ] || { echo "REFUSING: gate 18's kit is absent: $G18_KIT" >&2; exit 31; }
[ -s "$G22_REPORT" ] || { echo "REFUSING: gate 22's report is absent: $G22_REPORT" >&2; exit 31; }
grep -qF 'If PR #8 merges first' "$G22_REPORT" || { echo "REFUSING: gate 22's report no longer carries its 'If PR #8 merges first' re-run list — §12 cites it" >&2; exit 31; }
[ -s "$G22_DIR/evidence/mail/verdict-body.txt" ] || { echo "REFUSING: gate 22's verdict body is not on disk" >&2; exit 31; }
grep -qF "$G22_DIR" "$BRIEF" || { echo "REFUSING: the brief does not name $G22_DIR" >&2; exit 31; }
case "$PROMPT" in *"$G22_DIR"*) ;; *) echo "REFUSING: the prompt does not name $G22_DIR" >&2; exit 31 ;; esac
for H in qa-run.py mktree-qq.sh lockcmp.py lockwalk.py tapsets.py g17-dupnames.py g22-run-suites.sh g22-compare.py g22-infscan.py g22-figures.py \
         g22-gh.sh g22-heads.sh g22-cmdlog.py g22-repoint.py qa-harness-g22-drive.cjs qa-harness-g22-offline.cjs qa-chrome-egressblock.sh \
         qa-chrome-census.py qa-egress-posctl.mjs qa-floorcount.py qa-harness-floorctl.mjs qa-netlog-scan.py; do
  [ -s "$G22_TOOLS/$H" ] || { echo "REFUSING: gate 22's tool $H is not on disk — the brief names it" >&2; exit 31; }
  grep -qF -- "$H" "$BRIEF" || { echo "REFUSING: the brief does not name gate 22's tool $H" >&2; exit 31; }
done

# 39 — the floor instrument is on disk and named.
grep -qF 'qa-floorcount.py' "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument qa-floorcount.py" >&2; exit 39; }

# 10 / 17 — report path named in both; no stale report.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

# 12 — tier declared in both, at the pinned head.
grep -qE "^- \*\*QQPB\*\* at \`${H7}\` — \*\*TIER 1" "$BRIEF" || { echo "REFUSING: brief does not declare QQPB at \`$H7\` TIER 1" >&2; exit 12; }
case "$PROMPT" in *"QQPB (TIER 1"*) ;; *) echo "REFUSING: prompt does not declare: QQPB (TIER 1" >&2; exit 12 ;; esac

# 78 — the commission's requirements, in both.
for T in 'TIER 1' 'C-19' 'C-20' 'GO WITH FINDINGS' 'NO GO' 'SETS, NOT COUNTS' '4d6ed6e' '437ab4b' 'e4ce536' 'f31720e' '8077fdc' 'd809de1' 'f0df06f' \
         '7378a4e' 'puppeteer-core' '25.0.2' 'node:22-bookworm-slim' 'extract-zip' 'Dependabot' '#1' '#4' 'advisor' 'gitleaks' 'createApp()' 'renderQuotePdf' \
         'frozen clock' 'byte' 'semantic' 'BASE-vs-BASE' 'workbook' 'pdftotext' 'pdftoppm' 'pdffonts' 'AUD' 'USD' 'CAD' 'npm test' 'test:print' 'test:xlsx' \
         'quote-engine.test.mjs' 'node strip.js' 'node --check' 'CdpBrowser' 'G23-M1' 'G23-M2' 'ESM' 'ExperimentalWarning' 'tests.yml' 'linuxFxVersion' \
         'AZ-PRE-READ' 'App Service' 'IMAGE-LEG' 'NPM-AUDIT' 'TARGET-MODE' 'PR #10' 'Claude in Chrome' 'HPAM word' 'PROVISIONAL' 'ONE browser at a time' \
         '.invalid' 'NO EMAIL TO ANY HUMAN ADDRESS' 'CodeQL' 'never dismiss' 'G23-F1' 'compare'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks '$T'" >&2; exit 78; }
  printf '%s\n' "$PROMPT" | grep -qiF -- "$T" || { echo "REFUSING: prompt lacks '$T'" >&2; exit 78; }
done

# 13 / 14 / 15 / 20 / 70 — directive, brief path, placeholders, verdict route, key path, question route, safety line.
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
case "$PROMPT" in *"$READY"*) ;; *) echo "REFUSING: prompt must name the builder's READY path" >&2; exit 14 ;; esac
case "$PROMPT" in *"$G18_KIT"*) ;; *) echo "REFUSING: prompt must name gate 18's kit path" >&2; exit 14 ;; esac
if printf '%s\n' "$PROMPT" | LC_ALL=C grep -q '@[A-Z_0-9]*@'; then echo "REFUSING: the prompt carries a placeholder" >&2; exit 14; fi
case "$PROMPT" in *"MAIL YOUR VERDICT"*"tuesday-agent@agentmail.to"*) ;; *) echo "REFUSING: prompt must say MAIL YOUR VERDICT to tuesday-agent@agentmail.to" >&2; exit 15 ;; esac
case "$PROMPT" in *"$SUBJECT_STEM"*) ;; *) echo "REFUSING: prompt must carry the verdict subject stem" >&2; exit 15 ;; esac
grep -qF "$SUBJECT_STEM" "$BRIEF" || { echo "REFUSING: brief must carry the verdict subject stem" >&2; exit 15; }
grep -qF 'MAIL YOUR VERDICT' "$BRIEF" || { echo "REFUSING: brief must say MAIL YOUR VERDICT" >&2; exit 15; }
if printf '%s\n' "$PROMPT" | grep -qi 'wednesday-agent@' && ! printf '%s\n' "$PROMPT" | grep -q 'Never wednesday-agent@'; then
  echo "REFUSING: the prompt routes to wednesday-agent@ — Datasec's coordinator is Tuesday" >&2; exit 15; fi
if printf '%s\n' "$PROMPT" | grep -qF 'KK_T9_External_HDD'; then echo "REFUSING: the prompt names the T9 — every path of this gate is on /Volumes/Laptop-DEV" >&2; exit 15; fi
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
WORDS="merge-tree NOT%TESTED env%-i bash 437ab4b 4d6ed6e e4ce536 work-g23 FOREGROUND MEASURED%AT%RUNTIME PROBED READ%ONLY start%/%mid%/%end CI VOID node%--check"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## Charter' '^## RULED BY KAM, AND SETTLED' '^## PRIOR ROUND' '^PRIOR ROUND: ' 'ITS REPORT IS ON DISK AT:' '^## PIN' \
         '^## WRONG OR UNVERIFIABLE' '^## THE READY' '^## 2a. LEGITIMATE SHAPES' '^## N1. ' '^## N2. ' '^## N3. ' '^## N4. ' '^## N5. ' '^## N6. ' \
         '^## N7. ' '^## N8. ' '^## N9. ' '^## N10. ' '^## 12. The merge' '^## 13. FLOOR' '^### HELD' '^## THE MODEL RULE' \
         "^## TUESDAY'S RULINGS AT STAMP" '^## 14. Output' '^PROVENANCE:'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
# 24 — the prompt must DESCRIBE the app's entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qE 'server/index\.js|server\.js'; then
  echo "REFUSING: the prompt contains a literal server entry path — this agent would read as a FOREIGN SERVER to an argv-grep floor check. Describe it; do not name it." >&2; exit 24; fi

# 53 / 60 / 61 / 62 / 64 / 69 / 75 — standing rules, in both.
for T in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' '420 s' '120 s' '900 s'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the deadline/heartbeat rule '$T'" >&2; exit 53; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the deadline/heartbeat rule '$T'" >&2; exit 53 ;; esac
done
for T in 'node --check' 'VOID'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the parse-before-red rule '$T'" >&2; exit 60; }
done
for T in 'EXCLUSIVE' 'work-g23'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the tree-exclusivity rule '$T'" >&2; exit 61; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the tree-exclusivity rule '$T'" >&2; exit 61 ;; esac
done
for T in '4848' '8080' '47787' 'env -i' 'AGENTMAIL_API_KEY' 'AGENTMAIL_INBOX' 'no jest lock' 'TABLES_CONNECTION_STRING' 'HPAM_WORD' 'ADVANCED_UNLOCK_SECRET' \
         'SESSION_SECRET' 'SALES_COPY_EMAIL' 'PUPPETEER_EXECUTABLE_PATH' 'GoogleUpdater' 'chrome_crashpad_handler' 'net-log' 'GH_TOKEN'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the QuickQuote floor rule '$T'" >&2; exit 62; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the QuickQuote floor rule '$T'" >&2; exit 62 ;; esac
done
for T in 'NEVER the live' 'hpas-quickquote' 'hpas-quickquote-rg' 'datasec-sales-portal.azurewebsites.net' 'datasec-sales-portal-rg' 'azurewebsites.net' \
         'no app-setting change' 'no publish' 'press nothing'; do
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

# 44 — the instruments are installed. The launcher never starts any of them.
[ -x "$CHROME_BIN" ] || { echo "REFUSING: no local Google Chrome at $CHROME_BIN — §N2/§N3 would be NOT RUN" >&2; exit 44; }
command -v gitleaks >/dev/null 2>&1 || { echo "REFUSING: gitleaks is not on PATH — §N8 (a D4 PROVISIONAL row) would be NOT RUN" >&2; exit 44; }
for T in 'pdftotext' 'pdftoppm' 'pdfinfo' 'pdffonts' 'patch'; do command -v "$T" >/dev/null 2>&1 || echo "NOTE: $T is not on PATH — §N1.3 / §N3 need it" >&2; done
LOAD1="$(sysctl -n vm.loadavg 2>/dev/null | awk '{print $2}')"
case "$LOAD1" in ''|*[!0-9.]*) ;; *) awk -v l="$LOAD1" 'BEGIN{exit !(l>40)}' && echo "NOTE: 1-minute load is $LOAD1 (drafting read 1.55) — browser cells will be slow; Tuesday decides whether to launch now" >&2 ;; esac

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
PP="$(pane_pid_of tuesday)"
[ "$(printf '%s\n' "$PP" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: expected exactly one tmux pane named 'tuesday' — its negative control is required" >&2; exit 38; }
CP="$(claude_under "$PP")"
[ "$(printf '%s\n' "$CP" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: pane 'tuesday' (pid $PP) has '${CP:-no}' claude descendant(s), not exactly one" >&2; exit 38; }
NEG_SEATS="$CP"; NEG_DESC=" \`$CP\` (tuesday);"
EXTRA="$(printf '%s\n' "$PANES" | awk '{p=$1; $1=""; sub(/^ /,""); print $0}' | grep -E "^(QA/|fleet-monitor\$|${BUILDER_PANE}\$)" | grep -vxF "$ROUTE_NAME" | sort -u)"
printf '%s\n' "$EXTRA" | grep -qxF "$BUILDER_PANE" || echo "NOTE: no '$BUILDER_PANE' pane is live — the builder seat is not a negative control this run (none was live at drafting)" >&2
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
NCOUNT="$(printf '%s\n' $NEG_SEATS | sed '/^$/d' | wc -l | tr -d ' ')"
[ "$(printf '%s\n' $NEG_SEATS | sort -u | wc -l | tr -d ' ')" = "$NCOUNT" ] || { echo "REFUSING: the derived seat pids are not distinct: $NEG_SEATS" >&2; exit 38; }

# 86 — no live gate-23 session already exists.
for P in $(pane_pid_of "$ROUTE_NAME"); do
  if [ -n "$(claude_under "$P")" ]; then echo "REFUSING: a pane named $ROUTE_NAME (pid $P) already runs a claude — gate 23 is live; do not start a second session" >&2; exit 86; fi
done

# 46 — the GitHub read leg as the commission set it (READ-ONLY-VISION-TOKEN; NOT-RUN only if Tuesday withdraws the token).
GHLEG="$(sed -n 's/^GH-API-LEG: \([A-Z-]*\)[[:space:]]*$/\1/p' "$BRIEF" | head -1)"
case "$GHLEG" in
  READ-ONLY-VISION-TOKEN)
    [ -d "$VSP_GH" ] || { echo "REFUSING: GH-API-LEG is READ-ONLY-VISION-TOKEN but $VSP_GH is not a directory" >&2; exit 46; }
    command -v gh >/dev/null 2>&1 || { echo "REFUSING: GH-API-LEG is READ-ONLY-VISION-TOKEN but no gh binary is on PATH" >&2; exit 46; } ;;
  NOT-RUN) ;;
  *) echo "REFUSING: the brief's GH-API-LEG line reads '${GHLEG:-<missing>}' — it must be exactly READ-ONLY-VISION-TOKEN or NOT-RUN" >&2; exit 46 ;;
esac

# ---- the coordinator's to-do guards (47, 48, 49, 50, 41, 32): run LAST, reported TOGETHER, exit with the first pending code.
PENDING=''
pend() { [ -n "$PENDING" ] || PENDING="$1"; shift; echo "REFUSING: $*" >&2; }

# 47 — AZ-READ-LEG is TUESDAY-READS (the commission) and its AZ-PRE-READ line is stamped.
AZLEG="$(sed -n 's/^AZ-READ-LEG: \([A-Z-]*\)[[:space:]]*$/\1/p' "$BRIEF" | head -1)"
AZPRE="$(sed -n 's/^AZ-PRE-READ: \(.*\)$/\1/p' "$BRIEF" | head -1)"
[ "$AZLEG" = "TUESDAY-READS" ] || { echo "REFUSING: the brief's AZ-READ-LEG reads '${AZLEG:-<missing>}' — this gate runs no az; it must be TUESDAY-READS (the commission)" >&2; exit 47; }
case "$AZPRE" in
  ''|"$PH_STAMP"|n/a) pend 47 "AZ-PRE-READ is '${AZPRE:-<missing>}' — Tuesday reads the live linuxFxVersion before launch and writes it there" ;;
  *linuxFxVersion*)
    case "$AZPRE" in *DOCKER\|*) ;; *) echo "NOTE: AZ-PRE-READ does not show a DOCKER| linuxFxVersion — §N5.4's 'App Service runs the image's Node' reading needs it; read before launch" >&2 ;; esac
    case "$AZPRE" in *437ab4b*) ;; *) echo "NOTE: AZ-PRE-READ does not name 437ab4b (the drafter expected v0.6.4-tool2.36-437ab4b) — live is not main; read §N9.3 before launch" >&2 ;; esac ;;
  *) echo "REFUSING: AZ-PRE-READ does not name linuxFxVersion: '$AZPRE'" >&2; exit 47 ;;
esac

# 48 — TARGET-MODE (decision D6).
TM="$(sed -n 's/^TARGET-MODE: \([A-Z-]*\)[[:space:]]*$/\1/p' "$BRIEF" | head -1)"
case "$TM" in
  MERGE-TREE) ;;
  FORWARD-MERGE-FIRST) echo "REFUSING: TARGET-MODE is FORWARD-MERGE-FIRST — nothing is gated until the builder forward-merges 437ab4b and the kit is re-briefed on the new head" >&2; exit 48 ;;
  "$PH_DECIDE") pend 48 "the brief's TARGET-MODE line is still ${PH_DECIDE} — Tuesday sets MERGE-TREE or FORWARD-MERGE-FIRST (decision D6) before launch" ;;
  *) echo "REFUSING: the brief's TARGET-MODE line reads '${TM:-<missing>}' — it must be exactly MERGE-TREE or FORWARD-MERGE-FIRST" >&2; exit 48 ;;
esac

# 49 / 45 — IMAGE-LEG (decision D7); NONE forbids docker in brief and prompt; an image leg needs a live daemon with the platform and no stale qa-g23-* object.
IL="$(sed -n 's/^IMAGE-LEG: \([A-Z0-9-]*\)[[:space:]]*$/\1/p' "$BRIEF" | head -1)"
DSV='not read (IMAGE-LEG NONE or undecided)'
case "$IL" in
  NONE)
    grep -qF 'NO DOCKER' "$BRIEF" && grep -qF 'No `docker` at all' "$BRIEF" || { echo "REFUSING: IMAGE-LEG is NONE but the brief does not forbid docker (NO DOCKER / No \`docker\` at all)" >&2; exit 45; }
    case "$PROMPT" in *"NONE means NO DOCKER at all"*) ;; *) echo "REFUSING: the prompt does not forbid docker under IMAGE-LEG NONE" >&2; exit 45 ;; esac ;;
  ARM64-NATIVE|AMD64)
    [ "$IL" = "AMD64" ] && PLAT='linux/amd64' || PLAT='linux/arm64'
    command -v docker >/dev/null 2>&1 || { echo "REFUSING: IMAGE-LEG is $IL but the docker CLI is not found" >&2; exit 45; }
    DSV="$(docker version --format '{{.Server.Version}} {{.Server.Os}}/{{.Server.Arch}}' 2>/dev/null)"
    [ -n "$DSV" ] || { echo "REFUSING: IMAGE-LEG is $IL but the docker daemon does not answer — start Docker Desktop before launch" >&2; exit 45; }
    docker buildx ls 2>/dev/null | grep -q "$PLAT" || { echo "REFUSING: no buildx builder lists $PLAT — the §N6 images cannot be built" >&2; exit 45; }
    QA_OBJ="$( { docker images --format '{{.Repository}}:{{.Tag}}' 2>/dev/null; docker ps -a --format '{{.Names}}' 2>/dev/null; } | grep -E '^qa-g23-' | tr '\n' ' ')"
    [ -z "$QA_OBJ" ] || { echo "REFUSING: qa-g23-* docker objects already exist ($QA_OBJ) — a stale image or container would read as this gate's" >&2; exit 45; }
    grep -qF 'DOCKER DISCIPLINE' "$G18_KIT" || { echo "REFUSING: gate 18's kit no longer carries its DOCKER DISCIPLINE section — §N6 cites it" >&2; exit 45; } ;;
  "$PH_DECIDE") pend 49 "the brief's IMAGE-LEG line is still ${PH_DECIDE} — Tuesday sets NONE, ARM64-NATIVE or AMD64 (decision D7) before launch" ;;
  *) echo "REFUSING: the brief's IMAGE-LEG line reads '${IL:-<missing>}' — it must be exactly NONE, ARM64-NATIVE or AMD64" >&2; exit 49 ;;
esac

# 50 — NPM-AUDIT (decision D8).
NA="$(sed -n 's/^NPM-AUDIT: \([A-Z-]*\)[[:space:]]*$/\1/p' "$BRIEF" | head -1)"
case "$NA" in
  RUN|NOT-RUN) ;;
  "$PH_DECIDE") pend 50 "the brief's NPM-AUDIT line is still ${PH_DECIDE} — Tuesday sets RUN or NOT-RUN (decision D8) before launch" ;;
  *) echo "REFUSING: the brief's NPM-AUDIT line reads '${NA:-<missing>}' — it must be exactly RUN or NOT-RUN" >&2; exit 50 ;;
esac

# 41 — the answer route exists (Tuesday adds 'QA/Vision-gate23|tuesday-agent@agentmail.to|no' at stamp; this launcher never writes it).
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" \
  || pend 41 "no '${ROUTE_NAME}|tuesday-agent@agentmail.to|…' line in $ROUTING — answers to the gate would have no route. Add it (pattern: the QA/Vision-gate22 line) before launch, and stamp the brief's ROUTING-LINE."

# 32 — the coordinator stamps the self-check (line AND note), AZ-PRE-READ, D4 / D6 / D7 / D8, the ROUTING-LINE and every @STAMP@.
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF" \
   || ! grep -q '^ROUTING-LINE: QA/Vision-gate23' "$BRIEF"; then
  pend 32 "the brief still carries $(grep -cF "$PH_STAMP" "$BRIEF") ${PH_STAMP} placeholder(s) (Self-check line and note, AZ-PRE-READ, ROUTING-LINE, the RULED lines of D4 / D6 / D7 / D8) — the coordinator re-reads end-to-end and stamps all of them before launch (ROUTING-LINE must begin 'QA/Vision-gate23')"
fi

if [ -n "$PENDING" ]; then
  echo "guards pass (MODEL 40 6 9 7 8 18 22 23 25 74 63 31 39 10 17 12 78 13 14 15 20 70 82 19 24 53 60 61 62 64 69 75 44 38R 86 46); coordinator to-do pending (47 48 49 50 41 32 as listed above); exiting $PENDING." >&2
  echo "  origin re-read $PIN_TS: main ${MAINH:0:7}, QQPB $H7, refs/pull/8/head $H7, refs/pull/8/merge ${PR_MERGE_NOW:0:7}, PR #10 ${P10_NOW:0:7}; M8 tree ${M8_TREE:0:7} recomputed; model $MODEL; GH-API-LEG $GHLEG" >&2
  echo "  NEG seats (38R, derived live):$NEG_DESC" >&2
  exit "$PENDING"
fi

PIN_BLOCK="$(printf 'PINNED HEADS — verified by the launcher at %s (cat-file; base e4ce536 = merge-base with MAIN; not-already-on-main; commit count 3; EXACTLY 4 behind main; parents 3d0167e <- 47eb533, 0d45100 <- 3d0167e + 51e9286, 4d6ed6e <- 0d45100 + e4ce536, 437ab4b <- 9d1c5ab + 818a019, 9d1c5ab <- e4ce536 + 5f08fe0; trees H8 01bdc92, BASE c71780c, P10 ee51fa7; main pinned EXACTLY; refs/pull/8/head = head; the 5-file delta and numstat; only the FROM line, the puppeteer-core range and the two require lines change outside comments and the lockfile; the shared file is package.json in disjoint hunks (PR #8 line 21; main and PR #10 line 11); the merged package.json f0df06f and M8 tree 8077fdc = GitHub test merge, M8P10 package.json 23cc8c9 and tree d809de1, recomputed read-only with two controls; lockfiles as briefed; git ls-remote origin for both rows):\n' "$PIN_TS"
  printf '%s\n' "$PIN" | awk -F'\t' '{ printf "  %-7s %-11s %-34s %s  base %s  commits %s\n", $1, $2, $3, $4, ($5=="-"?"-":substr($5,1,12)), $6 }'
  printf '  M8 (437ab4b + PR #8) tree: %s. M8P10 (437ab4b + PR #8 + PR #10) tree: %s. PR #8: refs/pull/8/head = %s; refs/pull/8/merge = %s (GitHub test merge). PR #10 branch: %s.\n' "$M8_TREE" "$M8P10_TREE" "${HQ:0:12}" "${PR_MERGE_NOW:-<absent>}" "${P10_NOW:-<absent>}"
  printf 'GH-API-LEG, as set in the brief: %s\n' "$GHLEG"
  printf 'AZ-READ-LEG, as set in the brief: %s (you run no az)\n' "$AZLEG"
  printf 'AZ-PRE-READ, as stamped by Tuesday: %s\n' "$AZPRE"
  printf 'TARGET-MODE, as stamped by Tuesday (D6): %s\n' "$TM"
  printf 'IMAGE-LEG, as stamped by Tuesday (D7): %s (docker server at launch: %s)\n' "$IL" "$DSV"
  printf 'NPM-AUDIT, as stamped by Tuesday (D8): %s\n' "$NA"
  printf 'NEGATIVE-CONTROL SEATS, derived live by the launcher from the cockpit panes at %s:%s Re-read them at start.' "$PIN_TS" "$NEG_DESC")"

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  printf '%s\n' "$PIN_BLOCK"
  echo "  model: $MODEL at exec (from models_latest.json); --check started no claude; nothing written."
  exit 0
fi

# 11 — no inherited identity: AZURE_CONFIG_DIR always EMPTY (no az in this gate); GH_CONFIG_DIR EMPTY unless GH-API-LEG = READ-ONLY-VISION-TOKEN.
ID_TMP="$(mktemp -d "${TMPDIR:-/tmp}/qa-vision-gate23-id.XXXXXX")" || { echo "REFUSING: cannot create the empty identity dir" >&2; exit 11; }
mkdir -p "$ID_TMP/azure-empty" "$ID_TMP/gh-empty" "$ID_TMP/bin" || { echo "REFUSING: cannot create the identity dirs under $ID_TMP" >&2; exit 11; }
{ [ -z "$(ls -A "$ID_TMP/azure-empty")" ] && [ -z "$(ls -A "$ID_TMP/gh-empty")" ]; } || { echo "REFUSING: the identity dirs under $ID_TMP are not empty" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_TMP/azure-empty"
export GH_CONFIG_DIR="$ID_TMP/gh-empty"
if [ "$GHLEG" = "READ-ONLY-VISION-TOKEN" ]; then
  QA_REAL_GH="$(command -v gh)" || { echo "REFUSING: gh vanished between guard 46 and launch" >&2; exit 11; }
  export QA_REAL_GH
  cat > "$ID_TMP/bin/gh" <<'SHIM'
#!/bin/bash
# gate-23 GET-only gh shim (written by launch_qa_vision_qq_gate23.sh; GH-API-LEG = READ-ONLY-VISION-TOKEN). Brief §HELD binds the rest.
REAL="${QA_REAL_GH:?gh shim: QA_REAL_GH unset}"
[ "${1:-}" = "api" ] || { echo "gh shim: only 'gh api' GET reads are allowed in Vision gate 23 (got: ${1:-<none>})" >&2; exit 64; }
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
  export GH_NO_UPDATE_NOTIFIER=1 GH_PROMPT_DISABLED=1
fi
export PATH="$ID_TMP/bin:$PATH"
if [ "$GHLEG" = "READ-ONLY-VISION-TOKEN" ]; then [ "$(command -v gh)" = "$ID_TMP/bin/gh" ] || { echo "REFUSING: the gh shim is not first on PATH" >&2; exit 11; }; fi
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"
[ -d "$CLAUDE_CONFIG_DIR" ] || { echo "REFUSING: Tuesday's claude store $CLAUDE_CONFIG_DIR is absent" >&2; exit 11; }
# 64 (cont.) — nothing a product process could use to reach a real provider is inherited from this shell.
unset DATABASE_URL TEST_DATABASE_URL AGENTMAIL_API_KEY AGENTMAIL_INBOX ACS_CONNECTION_STRING ACS_EMAIL_CONNECTION_STRING ACS_EMAIL_SENDER \
      MAIL_SENDER TABLES_CONNECTION_STRING AZURE_BACKUP_CONN_STR SESSION_SECRET HPAM_WORD ADVANCED_UNLOCK_SECRET SALES_COPY_EMAIL \
      FEEDBACK_NOTIFY_EMAIL FEEDBACK_NOTIFY_EMAILS APPROVALS_INBOX NTFY_TOPIC NTFY_SERVER LEAD_BOT_API_KEY WEBSITE_SITE_NAME COORDINATOR_SECRET \
      PORT NODE_ENV PUPPETEER_EXECUTABLE_PATH PAGE_RATE_LIMIT_PER_10_MIN OTP_IP_BUDGET_PER_HOUR OTP_GLOBAL_BUDGET_PER_HOUR GH_TOKEN GITHUB_TOKEN \
      GH_ENTERPRISE_TOKEN GITHUB_ENTERPRISE_TOKEN DOCKER_HOST
[ "$IL" = "NONE" ] && unset DOCKER_CONTEXT
export npm_config_update_notifier=false
echo "identity: AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR (empty; AZ-READ-LEG $AZLEG) GH_CONFIG_DIR=$GH_CONFIG_DIR (GH-API-LEG $GHLEG) CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR IMAGE-LEG=$IL" >&2

PROMPT="$PROMPT

$PIN_BLOCK"
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model "$MODEL" "$PROMPT"
