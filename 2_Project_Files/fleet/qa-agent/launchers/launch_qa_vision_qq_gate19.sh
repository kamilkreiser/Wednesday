#!/bin/bash
# launch_qa_vision_qq_gate19.sh — cross-project QA agent, ONE gate (Vision gate 19; drafted 2026-10-16 ~14:01-14:4x AEDT by a read-only drafting
# agent for Tuesday, from launch_qa_vision_qq_gate18.sh, minus its docker leg and its az shim).
# Datasec/Vision_Sales_Portal, QuickQuote repo: ONE target, TIER 1 (quote output to customers), ONE verdict:
#   QQGD  fix/qq-email-print-mode-guard-2026-10-16  PR #9 @ 5f08fe0  the hosted Email guard (C-20)   TIER 1, round 1 of 2
#
# Main is e4ce536 (merge of PR #7). QQGD = ONE commit 5f08fe0 with the single parent e4ce536. 1 ahead, 0 behind.
# THIS GATE PINS MAIN EXACTLY: a moved main REFUSES (PR #8 / gate 18 merging first would move it). refs/pull/9/head must equal the head.
#
# THE HEADS LIVE IN ONE PLACE: the brief's PIN-HEADS table. This launcher PARSES it, refuses any placeholder, verifies every row against the
# object store and against origin by `git ls-remote` NOW, and appends the verified table to the agent's prompt.
#
# Every path is on /Volumes/Laptop-DEV EXCEPT gate 17's report and instruments, which exist ONLY on the T9 and are READ there. The T9 QuickQuote
# repo is STALE (it lacks 4d6ed6e and 5f08fe0) and is never read.
#
# PRODUCTION IS LIVE for this project (hpas-quickquote / hpasqqacr; datasec-sales-portal-rg). This gate runs NO docker and NO az. Findings only.
#
# GUARDS — gate 18's numbering kept where the guard survives; changes:
#   - PIN: two rows (MAIN-Q e4ce536, QQGD 5f08fe0 base e4ce536 x1). Exact parent pin; head tree pin.
#   - 22/23: file set 3 + numstat; package.json's ONLY change is the test:print line; strip.js's only removed line is the old label line.
#   - 74: blobs (3 changed, the unchanged list incl. lockfile and Dockerfile), Kam's two sentences by sha256 in strip.js AND in the test file.
#   - 45N (replaces gate 18's 45D): the prompt and brief forbid docker; no docker command is run here at all.
#   - 46: GH-API-LEG must read READ-ONLY-VISION-TOKEN or NOT-RUN (the commission set READ-ONLY-VISION-TOKEN).
#   - 47: AZ-READ-LEG must read TUESDAY-READS (the commission); AZ-PRE-READ must be stamped and name linuxFxVersion (pending guard).
#   - 48 (NEW): LEG7-METHOD (D5) = STATUS-MAILS (file on disk required) | GATE-METHOD (pending guard while TUESDAY-DECIDES).
#   - 86: no live QA/Vision-gate19 pane already.
#   - 47 48 41 32 are the coordinator's to-do guards: run LAST, reported TOGETHER, exit with the first pending code.
#
# LAUNCH IT IN A TMUX PANE:
#   /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add 'QA/Vision-gate19' "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_vision_qq_gate19.sh'"
#   NEVER nohup, never bare from a seat's shell.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# --check is READ-ONLY: git read verbs (cat-file, rev-parse, merge-base, log, rev-list, diff, show, ls-tree, ls-remote); tmux list-panes; ps;
# grep/python over files. It creates no identity dir, writes nothing and starts no claude.
# Usage: launch_qa_vision_qq_gate19.sh [--check]
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
BRIEF="$BRIEFS/2026-10-16_vision-gate19-qq-pr9-email-guard.md"
READY="$BRIEFS/2026-10-16_vision-qq-pr9-guard-READY-mail.txt"
STATUS_MAILS="$BRIEFS/2026-10-16_vision-qq-printmode-STATUS-mails.txt"
CHARTER="$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"
MODELS_JSON="$TUE/0_Brain/dashboard/data/models_latest.json"
MODEL_PIN='claude-opus-5-5'
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
VSP='/Volumes/Laptop-DEV/!CODING/Datasec/Vision_Sales_Portal'
Q_REPO="$VSP/Quoting Tool/hpas-quoting-tool"
VSP_GH="$VSP/4_Credentials/.gh-config"
CLAR="$VSP/1_Project_Definition/CLARIFICATIONS.md"
REPORTS="$QA_DIR/projects/vision/reports"
T9_REPORTS='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports'
G17_DIR="$T9_REPORTS/2026-10-13-vision-gate17-qq-quality-round"
G17_REPORT="$G17_DIR/report.md"
G17_TOOLS="$G17_DIR/evidence/tools"
REPORT="$REPORTS/2026-10-16-vision-gate19-qq-pr9-email-guard/report.md"
ROUTE_NAME='QA/Vision-gate19'
BUILDER_PANE='Datasec/Vision_Sales_Portal'
CHROME_BIN='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
PR_NUM='9'
PR_MERGE_SEEN='deb508193964aa2b2f1c84e2f1f58249240bfc59'     # refs/pull/9/merge at 14:01:52 (GitHub's test merge; NOTE only)
ANCHOR_MAIN='e4ce5367761e03db982189a3f21758aa06714a85'     # QuickQuote main = merge of PR #7 (C-18)
ANCHOR_MAINP='3dd15bcc09862047f6500e1813901edd8a686888 5ad37f1a3224c8fb3fddf8ad71dd144db62e9655'
ANCHOR_LIVE='3dd15bcc09862047f6500e1813901edd8a686888'     # v0.6.3-tool2.35-3dd15bc (live per Tuesday's 10-13 note; AZ-PRE-READ confirms)
HQ_EXPECT='5f08fe035f39ddc13e8260de1dde0d5d623f18d5'
HQ_TREE='dc6aef6406e0872713fbf5c7f95fad80e9e53b1b'
DELTA_FILES='stage3/package.json stage3/strip.js stage3/test/email-print-mode.mjs'
NUMSTAT_EXPECT='1/1/stage3/package.json 28/1/stage3/strip.js 175/0/stage3/test/email-print-mode.mjs '
STRIP_REMOVED_EXPECT='-  btn.textContent = "Email me this quote (PDF & XLS)";'
W1_SHA='0d5beedb47709eed6c7c6eec5d8ced3e73c58069ea09f49f4495cde1abeb25b9'
W2_SHA='4c73c1593e64f73dc84d24c48a69896307108d387b70a9318b0d7f7dd3ec797d'
# Kam's words, byte for byte (U+201C/U+201D around Standard pricing only). Checked by sha256 against W1_SHA/W2_SHA below.
W1='This email sends standard pricing only. Your custom pricing is on the printable quote, but it will not be in the email. Choose “Standard pricing only” above, or press the button again to send standard pricing anyway.'
W2='Send standard pricing anyway'

SUBJECT_STEM='[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 19'
QUESTION_SUBJ='[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>'
ANSWER_PREFIX='[Tuesday -> QA/Vision-gate19] ANSWER'
STATUS_SUBJ='[QA/Datasec-Vision -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch'
PARK_LINE='PARKED: flagged — awaiting the Opus 4.8 switch'

q() { git --no-optional-locks -C "$Q_REPO" "$@"; }
sha256s() { printf '%s' "$1" | shasum -a 256 | awk '{print $1}'; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE gate (Vision gate 19) on Datasec/Vision_Sales_Portal, in the QUICKQUOTE repo: ONE target, TIER 1 (quote output to customers), ONE verdict, GO / GO WITH FINDINGS / NO GO. QuickQuote main is e4ce536 (the merge of PR #7). The target QQGD (TIER 1; ROUND 1 of 2 of PR #9) is QuickQuote PR #9, branch fix/qq-email-print-mode-guard-2026-10-16 at 5f08fe0, ONE commit over e4ce536: the hosted Email guard ruled by Kam as C-20 (card quickquote-email-sends-standard-not-custom-1016 = a, 2026-10-16 13:25:51 AEDT, "Publish the guard as soon as it passes the gate, full fix after"). The emailed quote is always rendered as "Standard pricing only"; in "Custom pricing only" or "Standard + custom pricing" a rep's Email used to send the customer the standard price silently. The guard (stage3/strip.js, the hosted-only Email handler): in a non-standard print mode the first press does not send, shows Kam's warning and arms the button for THAT mode; a second press sends; any print-mode change disarms. The delta is three files: strip.js, a new test stage3/test/email-print-mode.mjs, and the package.json test:print line. The lockfile, the Dockerfile, the offline index.html, the hosted server module, lib/pdf.js and lib/xlsx.js are byte-identical at base and head. This machine is Kam's Mac mini, working volume /Volumes/Laptop-DEV; the T9 drive /Volumes/KK_T9_External_HDD is also mounted and holds gate 17's report and instruments (read there, never write there; its QuickQuote repo is STALE, never read it).

KAM'S WORDS, approved verbatim on card quickquote-guard-words-1016 = a. The rendered warning must be byte-equal to W1 and the armed button to W2 (the quotes around Standard pricing only are U+201C and U+201D; "Warning:" and "Armed button:" in the READY are LABELS, not text):
W1: This email sends standard pricing only. Your custom pricing is on the printable quote, but it will not be in the email. Choose “Standard pricing only” above, or press the button again to send standard pricing anyway.
W2: Send standard pricing anyway

READ YOUR COMMISSION FIRST, whole: /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-16_vision-gate19-qq-pr9-email-guard.md
Then read the charter it names, the Vision CLARIFICATIONS (C-01..C-20; C-20 is Kam's ruling for this target; its grant covers the GUARD only; publishing is Tuesday's PUBLISH GO, not yours), the project's CLAUDE.md (/Volumes/Laptop-DEV/!CODING/Datasec/Vision_Sales_Portal/CLAUDE.md, its QuickQuote section; its deploy commands are not for you), the QuickQuote repo's own CLAUDE.md at the head (git show; its publish lines are not for you), the builder's READY mail under test, read WHOLE (/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-16_vision-qq-pr9-guard-READY-mail.txt), and gate 17's report on the T9 /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-10-13-vision-gate17-qq-quality-round (the last QuickQuote gate with a report; evidence/tools/ holds the instruments you copy). Every builder statement is a CLAIM, never evidence. RE-DERIVE every red, every mutant, every suite set, every browser result and every comparison yourself. Verify every PRIOR WORK claim against git history, never against the brief. The brief's WRONG list, MODEL RULE and TUESDAY'S RULINGS (R1-R8 and the stamped D4-D5) are stamped: apply them, do not re-rule them.

WHAT THE BRIEF REQUIRES, in short (the brief is the authority):
(1) THE DIFF against the READY's claims, hunk by hunk; the send path after disarm byte-identical to base; the collector's POST unchanged; the PR files API equal to git diff --numstat; no dependency or Dockerfile change.
(2) THE RED-PROOF: the head's new test file (blob b1d4443) run in a fresh BASE-code tree (e4ce536, tamper asserted landed, node --check rc 0, a file that does not parse is VOID) must fail for the RIGHT reason (custom and both POST on the first press; the button never armed; the second mode sent), with the standard-mode control passing; the same file passes 5/5 at 5f08fe0 (3 runs, timings with the load). Mutants G19-M1 (the return removed), G19-M2 (the change listener removed), G19-M3 (W1 changed by one character in strip.js only), each on a fresh head tree with the mutation shown in the generated public/index.html: say which cells see each, or NONE.
(3) A REAL-BROWSER DRIVE of the hosted page's advanced session through the REAL server path: your harness runs the head tree's hosted server module's createApp() export in-process (never its entry point) with the repo's in-memory store, a CAPTURING stub mail, throwaway session and unlock secrets (never a real secret, never the HPAM word), the tree's own renderQuotePdf, a frozen clock, on 127.0.0.1 and a kernel port; ONE Google Chrome through your egress-block wrapper signs in with the captured OTP, unlocks advanced through the page's own controls, fills the form as a rep, sets a custom price by "% from standard", picks each print mode by its label and presses the page's own Email button. The grid S1-S7 at head AND base (base reproduces the defect: custom and both send on press 1): standard sends on one press; custom and both warn first (no POST, no mail) then send exactly once on the second press; switching mode by the rep's click disarms and clears the warning; a simple session sends on one press. Screenshots of the warning in light AND dark through the page's own theme toggle, with WCAG contrast from computed styles. Edge probes E1-E8 (double-click, the page's programmatic print-mode resets that fire no change event, Advanced off, Reset form, keyboard, a failed send, aria-live, reload). Phone widths 375 px and 320 px, light and dark (the READY's NOT TESTED line). The builder's interception method is allowed only as a labelled SECONDARY ("stubbed server").
(4) KAM'S WORDS byte for byte: the live DOM's textContent and innerText of the note and the button, UTF-8 length and sha256 against W1 (220 bytes) and W2 (28 bytes), and the constants in strip.js, the test and the generated public/index.html; the comparator shown to report UNEQUAL on a one-character substitute first.
(5) THE OFFLINE index.html UNCHANGED: git diff e4ce536 5f08fe0 -- index.html empty; node strip.js at base and head: private/advanced.js and private/svc.js identical, public/index.html differing only inside the hosted extras script.
(6) THE CI SUITES as CI runs them, at 5f08fe0 and e4ce536, as SETS, NOT COUNTS: root node --test quote-engine.test.mjs; in stage3/: npm test, npm run test:print (the added names must be exactly the 5 new cells, 0 lost), npm run test:xlsx. npm ci --offline --ignore-scripts only, the lockfile proven entry by entry (lockcmp.py AND lockwalk.py), npm ls --all. Host Node is 26.8.1, not CI's 22: say so. test:azurite is READ from CI (no docker).
(7) THE GUARD DOES NOT CHANGE WHAT IS EMAILED: standard mode, base vs head, AUD/USD/CAD: the emailed PDF (pdftotext -layout text, the money-figure multiset, pdftoppm -r 100 pixels per page in plain python — no ImageMagick, PIL or numpy — pdfinfo pages and A4, pdffonts) and the workbook (only docProps/core.xml may differ) identical; the posted state identical; after the second press in custom and both, the email carries ONLY standard figures (every figure present in the printed "Standard pricing only" quote, the printed custom total absent) — W1's claim must be TRUE. A planted one-word and one-pixel difference must make your comparator report non-zero first. The method follows the brief's LEG7-METHOD (appended below). The 7 unknown print-mode fields (pmBoth..cpPct) are PRE-EXISTING: record them at base and head, never call them PR #9's.
(8) NOTHING PUSHED, MERGED OR PUBLISHED: your command log proves no push, merge, docker, az or GitHub write; the live webapp's linuxFxVersion is RELAYED from the brief's AZ-PRE-READ (appended below; Tuesday re-reads at verdict); what a publish of 5f08fe0 would ship beyond the guard (the live tag's sha .. 5f08fe0), READ ONLY; deploy-on-merge READ ONLY.
(9) CI AND CODEQL on PR #9, READ ONLY, by GH-API-LEG: runs 38842678755 and 38842703255 and their jobs, the print-fit log lines the READY quotes, the check runs; the PR-side CodeQL zeros are a blind instrument (gate 17's control): say only what they can show.
GH-API-LEG (appended below by the launcher as the brief sets it): READ-ONLY-VISION-TOKEN means gh is on your PATH as a GET-only shim over Vision's gh config — gh api GET reads only, never -X/--method, -f/-F/--field/--raw-field/--input or graphql, never a comment, review, label, approval, re-run or dismissal; NOT-RUN means none. AZ-READ-LEG is TUESDAY-READS: you run no az at all. Never open any file under the project's 4_Credentials.

PRODUCTION IS LIVE for this project. NEVER the live QuickQuote (hpas-quickquote, hpas-quickquote-rg, hpasqqacr, its Table Storage, its log workspace) and NEVER the live portal (datasec-sales-portal.azurewebsites.net, datasec-sales-portal-rg): no HTTP request, not even a GET. No az; no deploy, no publish, no app-setting change, no ACR build, no registry push. Never the FX hosts (blocked by your wrapper), never ntfy.sh. Never Claude in Chrome (Kam's own Chrome with his sign-ins). Never type an HPAM word. NO DOCKER: not a build, not a run, not even docker images or docker ps; gate 18 (PR #8) may be running its own qa-g18-* containers beside you — never touch them, never touch work-g18. NETWORK, and only this: git ls-remote origin; gh api GETs if GH-API-LEG allows. No npm registry (npm ci --offline), no npm audit.

ONE BROWSER AT A TIME: the box was at load 184-235 when this gate was drafted, with eleven MPS lanes running. Never two Chromes of yours alive at once (a suite's own Chromes count); never a suite and a browser drive concurrently; one retry per cell at most, then NOT RUN with the load.

HELD: no merge, no publish, no comment or status on PR #9 or PR #8, no alert dismissal, no mail to any human. TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT on this drive from the object store (git archive into a fresh mktemp -d under projects/vision/work-g19/ in /Volumes/Laptop-DEV/!CODING/Testing Agent MAIN). Each tree is EXCLUSIVE to this gate and to one purpose; never touch any other work directory on either drive. The QuickQuote repo on THIS drive is the only one that holds the head. The builder's checkout is LIVE (it is starting fix 2 there): never read any working tree as evidence; never use the name main in the repo, only the pinned 40-hex shas. Copy gate 17's instruments from the T9 into YOUR evidence/tools on this drive and re-point them (they hard-code work-g17, the gate-17 report folder, the T9 volume and the stale T9 repo); never run from, edit or write into gate 1-18's copies. Never npm install, never npm audit fix, never npx anything not already in the tree. In the repo use ONLY read verbs (show, log, diff, ls-remote, rev-parse, ls-tree, cat-file, grep, merge-base, archive); never fetch, pull, checkout, switch, worktree, commit, stash, reset, clean, gc, branch or for-each-ref. Run git merge-tree --write-tree only from the gate's OWN object dir, or skip it and say so. Findings-only: no writes in the QuickQuote repo, none inside Vision_Sales_Portal, none in gate 1-18's report folders or trees. Never rm: quarantine. Run every loop and every git show <sha>:<path> under bash. Run node strip.js before any lone browser file. CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY: the base column must reproduce the defect before the head's "does not send" is credited to the guard; the byte comparator must report UNEQUAL on a one-character substitute; the PDF comparator must report non-zero on a planted difference; a control derived from the run it validates is not a control.

FLOOR DISCIPLINE. Vision has no jest lock; never borrow NexusAI's. Never use host ports 4848, 8080 or 47787; host processes take every port from the kernel and bind 127.0.0.1. Every host product process runs under env -i with an explicit allowlist, NODE_ENV never production. Never set AGENTMAIL_API_KEY or AGENTMAIL_INBOX in a product process (with both set, QuickQuote SENDS FOR REAL), nor any real ACS_* or MAIL_SENDER, TABLES_CONNECTION_STRING, SALES_COPY_EMAIL, HPAM_WORD, ADVANCED_UNLOCK_SECRET, SESSION_SECRET, WEBSITE_SITE_NAME, GH_TOKEN or GITHUB_TOKEN; print each product process's env KEY NAMES and assert none is forbidden. NTFY_SERVER=http://ntfy.invalid; never contact ntfy.sh. EGRESS INCLUDING CHROME CHILDREN: every Chrome runs under your copy of the egress-block wrapper as PUPPETEER_EXECUTABLE_PATH; prove the block with its positive control and run the net-log scan at the end; record GoogleUpdater and chrome_crashpad_handler at start and end; reap every Chrome and every app listener by the pid you started. Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid, with the negative-control seats the launcher derived (listed at the end of this prompt) classifying FOREIGN in the same run. A zero is reportable only beside an ATTACHED control that fired in the same window. Record the load average beside every timing number; a latency result with no load figure is not a measurement.
DEADLINE AND HEARTBEAT: every step has a written DEADLINE built into your runner (there is no timeout binary here) and releases its Chromes, pages, children, app servers and temp profiles in a finally. Log a HEARTBEAT line at least every 2 minutes; a step with no heartbeat for 5 minutes is aborted and reported, never waited on. Deadlines: one browser cell 120 s; one red-proof or mutant arm 420 s; the root pack 120 s; a whole npm test 300 s; a whole test:xlsx 300 s; a whole test:print 900 s; nothing above 900 s. Under the brief's D4, a red-proof or a head S2/S3 row NOT RUN makes the verdict PROVISIONAL.

THE MODEL RULE (Kam, live board 2026-09-30 09:07, card (b)): QA gates may switch to Opus 4.8 when flagged by Opus 5.5's safeguards, PER SESSION. You start on Opus 5.5. You run the FULL rows. If one of your responses is stopped by the safeguards: that step is NOT RUN (never re-worded to slip past); write ONE line to evidence/classifier-stops.txt; reap any Chrome and app server you started; mail tuesday-agent@agentmail.to with the subject exactly "[QA/Datasec-Vision -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch"; then end your turn with the line "PARKED: flagged — awaiting the Opus 4.8 switch" and wait. Tuesday switches THIS pane's model and taps you by mail. You never answer the model dialog yourself, and nobody ever chooses "Switch automatically". After the switch, resume at the stopped row. The report states which rows ran on which model, with the switch time, and quotes classifier-stops.txt whole.

QUESTIONS: your routing name is QA/Vision-gate19. If you must ask, mail tuesday-agent@agentmail.to with the subject "[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>" and proceed on the safest reading without waiting (the one exception is a safeguards stop, which PARKS you under THE MODEL RULE). Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/Vision-gate19] ANSWER"; read it with your verdict key. Never wednesday-agent@. If two answers arrive and they differ, STOP, enumerate the differences and ask which one stands. If a response is cut off by a safety check, record it and continue with the next item; this is authorised defensive QA of Datasec's own product on loopback. Approval-class items (a publish, a deploy, the live site, money, a human) are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your report to: /Volumes/Laptop-DEV/!CODING/Testing Agent MAIN/projects/vision/reports/2026-10-16-vision-gate19-qq-pr9-email-guard/report.md
Write its VERDICT and FINDINGS table early and keep it current.

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with a subject beginning exactly:
[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 19: QQGD @ <sha7> <GO | GO WITH FINDINGS | NO GO>
(the sha7 is the pinned head from the verified table below; append PROVISIONAL if the brief's D4 clause applies). Lead the body with ONE sentence as the brief's section 14 words it (the red-proof; the real hosted page through the real server path in all three print modes and a simple session; W1 and W2 byte-equal; the offline index.html unchanged; the CI suites as sets; the standard-mode email identical to main's; anything pushed, merged or published), then one line each on the base column (the defect reproduced, with figures), the mutants, the edge probes E1 and E2-E4, the phone widths, the live site read (RELAYED), what a publish would ship, and the class count (round 1: a NO GO goes to round 2). You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/Laptop-DEV/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no credentials directory of its own. Use it only in your own mail calls, with a client timeout. Never put the key or any secret in a mail, the report or a product process.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice — the only turn you end while waiting is the PARKED line of THE MODEL RULE.

Report the pinned head and main as three timestamped readings (start / mid / end), with the branch name beside each, plus refs/pull/9/head. Include a table with one row per brief section N item: MEASURED, NOT TESTED, NOT RUN or VOID, and HOW (command, tree, browser, port, load).

Rule 2 stands: what you did NOT test is first-class output. Write a NOT TESTED section that covers at least the guard inside the published image (no docker by design), a real ACS send in a custom mode, the live site, CodeQL's verdict before the merge (blind), CI's Node 22 (read only, never caused), store-azurite (read from CI), Windows, Safari, real phones and the account managers' real browsers, screen readers, Claude in Chrome (not used), fix 2 (not this gate), and every row you did not run. Label every action recommendation MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. The tester never fixes.
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
EXPECT_IDS='MAIN-Q QQGD'
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
[ "$(fld QQGD 3)" = "fix/qq-email-print-mode-guard-2026-10-16" ] || { echo "REFUSING: row QQGD branch is '$(fld QQGD 3)', the brief's target is fix/qq-email-print-mode-guard-2026-10-16 — re-brief" >&2; exit 40; }
is40 "$(fld QQGD 5)" || { echo "REFUSING: PIN row QQGD base is not a 40-hex sha" >&2; exit 40; }
printf '%s' "$(fld QQGD 6)" | grep -Eq '^[1-9][0-9]*$' || { echo "REFUSING: PIN row QQGD commits '$(fld QQGD 6)' is not a positive integer" >&2; exit 40; }
[ "$(fld QQGD 4)" = "$HQ_EXPECT" ] || { echo "REFUSING: QQGD's PIN head $(fld QQGD 4 | cut -c1-7) is not ${HQ_EXPECT:0:7} — this launcher's content guards are pinned to it; re-brief" >&2; exit 40; }
MAINH="$(fld MAIN-Q 4)"
HQ="$(fld QQGD 4)"

# 6 — every sha the guards use is a commit in the local object store (this launcher never fetches).
for S in "$MAINH" "$HQ" "$ANCHOR_MAIN" $ANCHOR_MAINP "$ANCHOR_LIVE"; do
  T="$(q cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in the QuickQuote repo on this drive (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 9m — MAIN: e4ce536 EXACTLY (refuse if it moved).
[ "$MAINH" = "$ANCHOR_MAIN" ] || { echo "REFUSING: the pinned MAIN ${MAINH:0:7} is not e4ce536 — this gate pins main exactly; re-brief" >&2; exit 9; }

# 7 / 8 — the target: base as briefed, its single parent, ancestor AND merge-base with MAIN, not on main, exact count, 0 behind.
H7="${HQ:0:7}"; BASE="$(fld QQGD 5)"; N="$(fld QQGD 6)"
[ "$BASE" = "$ANCHOR_MAIN" ] || { echo "REFUSING: row QQGD base ${BASE:0:7} is not e4ce536 — re-brief" >&2; exit 7; }
q merge-base --is-ancestor "$BASE" "$HQ" 2>/dev/null || { echo "REFUSING: QQGD base ${BASE:0:7} is not an ancestor of $H7" >&2; exit 7; }
[ "$(q merge-base "$HQ" "$MAINH" 2>/dev/null)" = "$BASE" ] || { echo "REFUSING: QQGD merge-base(head, MAIN) is not its base ${BASE:0:7}" >&2; exit 7; }
q merge-base --is-ancestor "$HQ" "$MAINH" 2>/dev/null && { echo "REFUSING: QQGD $H7 is ALREADY ON MAIN ${MAINH:0:7} — the brief says it is not; re-brief" >&2; exit 7; }
GOTN="$(q rev-list --count "${BASE}..${HQ}" 2>/dev/null)"
[ "$GOTN" = "$N" ] || { echo "REFUSING: QQGD $H7 has $GOTN commits over its base, the table says $N" >&2; q log --format='%h %p %s' "${BASE}..${HQ}" >&2; exit 8; }
[ "$N" = "1" ] || { echo "REFUSING: the brief's commit count is $N, this launcher's chain is one commit" >&2; exit 8; }
[ "$(q rev-list --count "${HQ}..${ANCHOR_MAIN}" 2>/dev/null)" = "0" ] || { echo "REFUSING: QQGD $H7 is behind e4ce536" >&2; exit 7; }

# 9 — gated anchors and the exact chain, by parents.
[ "$(q log -1 --format='%P' "$ANCHOR_MAIN")" = "$ANCHOR_MAINP" ] || { echo "REFUSING: e4ce536's parents are not 3dd15bc + 5ad37f1" >&2; exit 9; }
[ "$(q log -1 --format='%P' "$HQ")" = "$ANCHOR_MAIN" ] || { echo "REFUSING: 5f08fe0's single parent is not e4ce536 — rebased or rebuilt" >&2; exit 9; }
[ "$(q rev-parse "${HQ}^{tree}" 2>/dev/null)" = "$HQ_TREE" ] || { echo "REFUSING: 5f08fe0's tree is not dc6aef6" >&2; exit 9; }
q merge-base --is-ancestor "$ANCHOR_LIVE" "$MAINH" 2>/dev/null || { echo "REFUSING: 3dd15bc (live v2.35) is not an ancestor of main — WRONG (h)'s reading is wrong" >&2; exit 9; }

# 18 — RE-PIN: BOTH rows AND refs/pull/9/head at origin, by ls-remote, read NOW (immediately before launch). No movement allowed, main included.
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

# 22 / 23 — exact file set, numstat, and the shape of each change.
GOT="$(q diff --name-only "$ANCHOR_MAIN" "$HQ" 2>/dev/null | sort)"
[ "$GOT" = "$(printf '%s\n' $DELTA_FILES | sort)" ] || { echo "REFUSING: QQGD ${H7}'s delta over e4ce536 is not exactly the briefed 3-file set. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }
[ "$(q diff --numstat "$ANCHOR_MAIN" "$HQ" | awk '{printf "%s/%s/%s ", $1, $2, $3}')" = "$NUMSTAT_EXPECT" ] \
  || { echo "REFUSING: the whole-diff numstat is not the briefed one. Got:" >&2; q diff --numstat "$ANCHOR_MAIN" "$HQ" >&2; exit 23; }
PKG_U0="$(q diff -U0 "$ANCHOR_MAIN" "$HQ" -- stage3/package.json | grep -E '^[+-][^+-]')"
[ "$(printf '%s\n' "$PKG_U0" | wc -l | tr -d ' ')" = "2" ] && printf '%s\n' "$PKG_U0" | grep -q '^-    "test:print": ' && printf '%s\n' "$PKG_U0" | grep -q '^+    "test:print": ' \
  || { echo "REFUSING: package.json's change is not exactly the test:print line. Got:" >&2; printf '%s\n' "$PKG_U0" >&2; exit 23; }
[ "$(printf '%s\n' "$PKG_U0" | sed -n 's/^-//p' | sed 's#test/email-collector.mjs #test/email-collector.mjs test/email-print-mode.mjs #')" = "$(printf '%s\n' "$PKG_U0" | sed -n 's/^+//p')" ] \
  || { echo "REFUSING: the test:print change is not ONLY test/email-print-mode.mjs inserted after test/email-collector.mjs" >&2; exit 23; }
[ "$(q diff "$ANCHOR_MAIN" "$HQ" -- stage3/strip.js | grep -E '^-[^-]')" = "$STRIP_REMOVED_EXPECT" ] \
  || { echo "REFUSING: strip.js's only removed line is not the old label assignment. Got:" >&2; q diff "$ANCHOR_MAIN" "$HQ" -- stage3/strip.js | grep -E '^-[^-]' >&2; exit 23; }
python3 - "$Q_REPO" "$ANCHOR_MAIN" "$HQ" <<'PY' || { echo "REFUSING: the package.json dependency maps differ between base and head (the brief says only a script line changed)" >&2; exit 23; }
import json, subprocess, sys
repo, b, h = sys.argv[1:4]
def pj(s): return json.loads(subprocess.run(['git','--no-optional-locks','-C',repo,'show',f'{s}:stage3/package.json'],capture_output=True,text=True,check=True).stdout)
B, H = pj(b), pj(h)
sys.exit(0 if all(B.get(k) == H.get(k) for k in ('dependencies','devDependencies','overrides','engines')) else 1)
PY

# 74 — content, read from the pinned shas (never a checkout).
blob() { q rev-parse --verify -q "${1}:${2}" 2>/dev/null; }   # --verify -q: a missing path prints NOTHING (bare rev-parse echoes the arg)
has() { q show "${1}:${2}" 2>/dev/null | grep -qF -- "$3"; }
must() { has "$1" "$2" "$3" || { echo "REFUSING: ${1:0:7}:$2 lacks '$3' — the brief gates different code; re-brief" >&2; exit 74; }; }
for P in 'stage3/strip.js|2fc3bd6417f792908906141e644b2becba17f346|0730e10459550ad1a7f63f9d8bc388e0550ec0ea' \
         'stage3/package.json|61d0d5c51f2987750620a520844685746cc2bdcb|1606aa3b4f0fa9b53811c7bc71f96cd57178a420'; do
  F="${P%%|*}"; R2="${P#*|}"; B0="${R2%%|*}"; B1="${R2#*|}"
  [ "$(blob "$ANCHOR_MAIN" "$F")" = "$B0" ] && [ "$(blob "$HQ" "$F")" = "$B1" ] || { echo "REFUSING: $F blobs are not ${B0:0:7} -> ${B1:0:7}" >&2; exit 74; }
done
! q cat-file -e "${ANCHOR_MAIN}:stage3/test/email-print-mode.mjs" 2>/dev/null || { echo "REFUSING: stage3/test/email-print-mode.mjs already exists at e4ce536 — WRONG (f)'s reading is wrong" >&2; exit 74; }
[ "$(blob "$HQ" stage3/test/email-print-mode.mjs)" = "b1d4443c45195cb80075dd443f07a59b6c53817c" ] || { echo "REFUSING: the head's email-print-mode.mjs is not blob b1d4443" >&2; exit 74; }
for F in index.html stage3/package-lock.json stage3/Dockerfile stage3/server.js stage3/lib/pdf.js stage3/lib/xlsx.js stage3/lib/mail.js stage3/lib/store.js \
         stage3/login.html .dockerignore .github/workflows/tests.yml quote-engine.test.mjs stage3/test/print-fit.mjs stage3/test/email-collector.mjs \
         stage3/test/server.test.mjs stage3/test/lib-close.mjs CLAUDE.md; do
  B0="$(blob "$ANCHOR_MAIN" "$F")"
  [ -n "$B0" ] && [ "$(blob "$HQ" "$F")" = "$B0" ] || { echo "REFUSING: $F differs between main and the head (or is absent) — the brief says it is carried unchanged" >&2; exit 74; }
done
[ "$(blob "$HQ" index.html)" = "447b129792f3c01c9de43e2a3bed4915058e8d58" ] || { echo "REFUSING: index.html is not blob 447b129" >&2; exit 74; }
for T in 'id="pmDefault" value="default"' 'id="pmBoth" value="both"' 'id="pmCustom" value="custom"' '.svc-warn.active { display: flex; }' \
         'html[data-theme="dark"] .svc-warn'; do
  must "$ANCHOR_MAIN" index.html "$T"
done
must "$HQ" stage3/server.js 'clock = () => new Date()'
[ "$(q ls-tree -r --name-only "$HQ" .github)" = ".github/workflows/tests.yml" ] || { echo "REFUSING: .github at the head holds other than tests.yml — §N8.4's reading is wrong" >&2; exit 74; }
for T in 'pricing-pack:' 'stage3-server:' 'store-azurite:' 'print-fit:' 'xlsx-parity:'; do must "$HQ" .github/workflows/tests.yml "  $T"; done
# Kam's words: the launcher's own W1/W2 are the approved bytes; strip.js AND the test file at the head carry exactly them.
[ "$(sha256s "$W1")" = "$W1_SHA" ] && [ "$(sha256s "$W2")" = "$W2_SHA" ] || { echo "REFUSING: this launcher's own copy of Kam's words does not hash to the pinned sha256 — the file was edited" >&2; exit 74; }
python3 - "$Q_REPO" "$HQ" "$W1_SHA" "$W2_SHA" <<'PY' || { echo "REFUSING: the head's WARNING / ARMED_LABEL constants (strip.js and the test) are not byte-equal to Kam's approved words" >&2; exit 74; }
import hashlib, re, subprocess, sys
repo, h, w1, w2 = sys.argv[1:5]
for path in ('stage3/strip.js', 'stage3/test/email-print-mode.mjs'):
    src = subprocess.run(['git','--no-optional-locks','-C',repo,'show',f'{h}:{path}'],capture_output=True,check=True).stdout.decode('utf-8')
    a = re.findall(r'const WARNING = "(.*?)";', src); b = re.findall(r'const ARMED_LABEL = "(.*?)";', src)
    if len(a) != 1 or len(b) != 1: sys.exit(1)
    if hashlib.sha256(a[0].encode()).hexdigest() != w1 or hashlib.sha256(b[0].encode()).hexdigest() != w2: sys.exit(1)
PY
grep -qF -- "$W1" "$BRIEF" && grep -qF -- "\`$W2\`" "$BRIEF" || { echo "REFUSING: the brief does not carry Kam's words W1/W2 byte for byte" >&2; exit 74; }
case "$PROMPT" in *"W1: $W1"*) ;; *) echo "REFUSING: the prompt does not carry W1 byte for byte" >&2; exit 74 ;; esac
case "$PROMPT" in *"W2: $W2"*) ;; *) echo "REFUSING: the prompt does not carry W2 byte for byte" >&2; exit 74 ;; esac
for T in 'npm ci --offline --ignore-scripts' 'entry by entry' 'never `npm audit fix`'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the dependency rule '$T'" >&2; exit 63; }
done
for T in 'npm ci --offline --ignore-scripts' 'entry by entry' 'never npm audit fix'; do
  printf '%s\n' "$PROMPT" | grep -qiF -- "$T" || { echo "REFUSING: prompt lacks the dependency rule '$T'" >&2; exit 63; }
done

# 31 — the READY is on disk, names the pinned head, its NOT TESTED lines are carried verbatim; sources on disk.
[ -s "$READY" ] || { echo "REFUSING: the READY mail is not on disk: $READY" >&2; exit 31; }
for T in 'READY FOR QA, TIER 1: QuickQuote PR #9 @ 5f08fe0 (fix/qq-email-print-mode-guard-2026-10-16 off main e4ce536)' \
         'Armed button: Send standard pricing anyway' 'Nothing merged or published.' 'git diff e4ce536..5f08fe0: 3 files' \
         'On main'"'"'s code: 4 of 5 FAIL for the right reason.' 'tests.yml 5/5 on push 38842678755 and pull_request 38842703255'; do
  grep -qF -- "$T" "$READY" || { echo "REFUSING: $READY does not carry '$T'" >&2; exit 31; }
done
grep -qF -- "Warning: $W1" "$READY" || { echo "REFUSING: the READY's warning line is not 'Warning: ' + W1 byte for byte — re-read WRONG (a)" >&2; exit 31; }
NT="$(awk 'f&&!/^- /{exit} f{print;next} /^NOT TESTED/{f=1;print}' "$READY")"
[ -n "$NT" ] || { echo "REFUSING: $READY carries no NOT TESTED block" >&2; exit 31; }
while IFS= read -r L; do
  [ -n "$L" ] || continue
  grep -qxF -- "$L" "$BRIEF" || { echo "REFUSING: the brief does not carry this NOT TESTED line of the READY verbatim: $L" >&2; exit 31; }
done <<< "$NT"
for T in 'QQGD NOT TESTED' 'C-20' 'quickquote-email-sends-standard-not-custom-1016' 'quickquote-guard-words-1016' 'ROUND 1' \
         '2026-10-16_vision-qq-pr9-guard-READY-mail.txt' 'WRONG (a)' 'WRONG (c)' 'WRONG (d)' 'WRONG (e)' 'WRONG (f)' 'WRONG (h)' 'WRONG (k)' \
         'GH-API-LEG' 'AZ-READ-LEG' 'AZ-PRE-READ' 'LEG7-METHOD' 'D4' 'D5' 'PROVISIONAL' 'G19-M1' 'G19-M2' 'G19-M3' 'pmBoth' "$W1_SHA" "$W2_SHA"; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: the brief does not carry '$T'" >&2; exit 31; }
done
for R in 'R1: ' 'R2: ' 'R3: ' 'R4: ' 'R5: ' 'R6: ' 'R7: ' 'R8: '; do
  grep -qF -- "- $R" "$BRIEF" || { echo "REFUSING: the brief does not carry Tuesday's ruling '$R' as a ruling line" >&2; exit 31; }
done
[ -s "$CLAR" ] || { echo "REFUSING: Vision CLARIFICATIONS.md absent: $CLAR" >&2; exit 31; }
grep -qF '**C-20.' "$CLAR" || { echo "REFUSING: $CLAR lacks C-20" >&2; exit 31; }
for T in 'quickquote-email-sends-standard-not-custom-1016' 'Publish the guard as soon as it passes the gate, full fix after' "Kam's grant covers the GUARD only"; do
  grep -qF -- "$T" "$CLAR" || { echo "REFUSING: CLARIFICATIONS C-20 does not carry '$T' — the ruling the brief quotes is not on disk" >&2; exit 31; }
done
grep -qF '**C-21.' "$CLAR" && echo "NOTE: Vision CLARIFICATIONS now has a C-21 — the brief says C-01..C-20; read it before launch" >&2
[ -s "$CHARTER" ] || { echo "REFUSING: the charter is absent: $CHARTER" >&2; exit 31; }
[ -s "$G17_REPORT" ] || { echo "REFUSING: gate 17's report is absent on the T9: $G17_REPORT (is the T9 mounted?)" >&2; exit 31; }
grep -qF '**GO WITH FINDINGS**' "$G17_REPORT" && grep -qF 'd030674694279be3159d67de4a10f220ea6b8335' "$G17_REPORT" \
  || { echo "REFUSING: gate 17's report does not carry QQQR's GO WITH FINDINGS at d030674" >&2; exit 31; }
grep -qF "$G17_DIR" "$BRIEF" || { echo "REFUSING: the brief does not name $G17_DIR" >&2; exit 31; }
case "$PROMPT" in *"$G17_DIR"*) ;; *) echo "REFUSING: the prompt does not name $G17_DIR" >&2; exit 31 ;; esac
for H in qa-run.py mktree-qq.sh lockcmp.py lockwalk.py tapsets.py g17-run-suites.sh g17-mutate.py g17-heads.sh g17-gh.sh qa-g17-lib.mjs \
         qa-harness-g17-capture.mjs qa-harness-g17-server.cjs g17-hosted-render.cjs qa-harness-g16-shots.mjs qa-chrome-egressblock.sh \
         qa-chrome-census.py qa-egress-posctl.mjs qa-floorcount.py qa-harness-floorctl.mjs qa-netlog-scan.py; do
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
grep -qE "^- \*\*QQGD\*\* at \`${H7}\` — \*\*TIER 1" "$BRIEF" || { echo "REFUSING: brief does not declare QQGD at \`$H7\` TIER 1" >&2; exit 12; }
case "$PROMPT" in *"QQGD (TIER 1"*) ;; *) echo "REFUSING: prompt does not declare: QQGD (TIER 1" >&2; exit 12 ;; esac

# 78 — the commission's requirements, in both.
for T in 'TIER 1' 'ROUND 1' 'C-20' 'quickquote-email-sends-standard-not-custom-1016' 'quickquote-guard-words-1016' 'GO WITH FINDINGS' 'NO GO' \
         'SETS, NOT COUNTS' '5f08fe0' 'e4ce536' 'email-print-mode.mjs' 'createApp()' 'renderQuotePdf' 'frozen clock' 'Standard pricing only' \
         'Custom pricing only' 'Standard + custom' 'light' 'dark' 'byte' 'U+201C' 'index.html' 'npm test' 'test:print' 'test:xlsx' \
         'quote-engine.test.mjs' 'pdftotext' 'pdftoppm' 'pdffonts' 'xlsx' 'AUD' 'USD' 'CAD' 'linuxFxVersion' 'AZ-PRE-READ' 'double-click' \
         '320 px' 'node strip.js' 'node --check' 'Claude in Chrome' 'HPAM word' 'PROVISIONAL' 'pmBoth' 'ONE browser at a time' 'docker' 'G19-M1'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks '$T'" >&2; exit 78; }
  printf '%s\n' "$PROMPT" | grep -qiF -- "$T" || { echo "REFUSING: prompt lacks '$T'" >&2; exit 78; }
done

# 45N — no docker in this gate: the brief and the prompt say so; nothing here runs docker.
grep -qF 'NO DOCKER' "$BRIEF" && grep -qF 'No `docker` at all' "$BRIEF" || { echo "REFUSING: the brief does not forbid docker (NO DOCKER / No \`docker\` at all)" >&2; exit 45; }
case "$PROMPT" in *"NO DOCKER"*) ;; *) echo "REFUSING: the prompt does not forbid docker" >&2; exit 45 ;; esac

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
WORDS="merge-tree NOT%TESTED env%-i bash e4ce536 5f08fe0 work-g19 FOREGROUND MEASURED%AT%RUNTIME PROBED READ%ONLY start%/%mid%/%end CI VOID node%--check"
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
for T in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' '420 s' '120 s' '900 s'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the deadline/heartbeat rule '$T'" >&2; exit 53; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the deadline/heartbeat rule '$T'" >&2; exit 53 ;; esac
done
for T in 'node --check' 'VOID'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the parse-before-red rule '$T'" >&2; exit 60; }
done
for T in 'EXCLUSIVE' 'work-g19'; do
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
for T in 'CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY' 'PRIOR WORK' 'OWN object dir' 'no writes in the QuickQuote repo' 'start / mid / end' 'NOT TESTED'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the standing line '$T'" >&2; exit 75; }
  printf '%s\n' "$PROMPT" | grep -qiF -- "$T" || { echo "REFUSING: prompt lacks the standing line '$T'" >&2; exit 75; }
done

# 44 — the browser legs' instrument, a local Google Chrome, is installed. The launcher never starts it.
[ -x "$CHROME_BIN" ] || { echo "REFUSING: no local Google Chrome at $CHROME_BIN — §N2/§N3/§N6 would be NOT RUN" >&2; exit 44; }
for T in 'pdftotext' 'pdftoppm' 'pdfinfo' 'pdffonts'; do command -v "$T" >/dev/null 2>&1 || echo "NOTE: $T is not on PATH — §N7's comparator needs it" >&2; done
LOAD1="$(sysctl -n vm.loadavg 2>/dev/null | awk '{print $2}')"
case "$LOAD1" in ''|*[!0-9.]*) ;; *) awk -v l="$LOAD1" 'BEGIN{exit !(l>40)}' && echo "NOTE: 1-minute load is $LOAD1 (drafting read 184.10) — browser cells will be slow; Tuesday decides whether to launch now (drafter's report)" >&2 ;; esac

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
printf '%s\n' "$EXTRA" | grep -qxF 'QA/Vision-gate18' && echo "NOTE: QA/Vision-gate18 is live beside this gate (docker-heavy, qa-g18-*/work-g18) — contention, not a conflict; never touched" >&2

# 86 — no live gate-19 session already exists.
for P in $(pane_pid_of "$ROUTE_NAME"); do
  if [ -n "$(claude_under "$P")" ]; then echo "REFUSING: a pane named $ROUTE_NAME (pid $P) already runs a claude — gate 19 is live; do not start a second session" >&2; exit 86; fi
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

# ---- the coordinator's to-do guards (47, 48, 41, 32): run LAST, reported TOGETHER, exit with the first pending code.
PENDING=''
pend() { [ -n "$PENDING" ] || PENDING="$1"; shift; echo "REFUSING: $*" >&2; }

# 47 — AZ-READ-LEG is TUESDAY-READS (the commission) and its AZ-PRE-READ line is stamped.
AZLEG="$(sed -n 's/^AZ-READ-LEG: \([A-Z-]*\)[[:space:]]*$/\1/p' "$BRIEF" | head -1)"
AZPRE="$(sed -n 's/^AZ-PRE-READ: \(.*\)$/\1/p' "$BRIEF" | head -1)"
[ "$AZLEG" = "TUESDAY-READS" ] || { echo "REFUSING: the brief's AZ-READ-LEG reads '${AZLEG:-<missing>}' — this gate runs no az; it must be TUESDAY-READS (the commission)" >&2; exit 47; }
case "$AZPRE" in
  ''|"$PH_STAMP"|n/a) pend 47 "AZ-PRE-READ is '${AZPRE:-<missing>}' — Tuesday reads the live linuxFxVersion before launch and writes it there" ;;
  *linuxFxVersion*) ;;
  *) echo "REFUSING: AZ-PRE-READ does not name linuxFxVersion: '$AZPRE'" >&2; exit 47 ;;
esac

# 48 (NEW) — LEG7-METHOD (decision D5).
L7="$(sed -n 's/^LEG7-METHOD: \([A-Z-]*\)[[:space:]]*$/\1/p' "$BRIEF" | head -1)"
case "$L7" in
  GATE-METHOD) ;;
  STATUS-MAILS) [ -s "$STATUS_MAILS" ] || { echo "REFUSING: LEG7-METHOD is STATUS-MAILS but $STATUS_MAILS is absent or empty — save the two STATUS mails verbatim there first" >&2; exit 48; } ;;
  "$PH_DECIDE") pend 48 "the brief's LEG7-METHOD line is still ${PH_DECIDE} — Tuesday sets GATE-METHOD or STATUS-MAILS (decision D5) before launch" ;;
  *) echo "REFUSING: the brief's LEG7-METHOD line reads '${L7:-<missing>}' — it must be exactly GATE-METHOD or STATUS-MAILS" >&2; exit 48 ;;
esac

# 41 — the answer route exists (Tuesday adds 'QA/Vision-gate19|tuesday-agent@agentmail.to|no' at stamp; this launcher never writes it).
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" \
  || pend 41 "no '${ROUTE_NAME}|tuesday-agent@agentmail.to|…' line in $ROUTING — answers to the gate would have no route. Add it (pattern: the QA/Vision-gate17 line) before launch."

# 32 — the coordinator stamps the self-check (line AND note), AZ-PRE-READ, D4-D5 and every @STAMP@.
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  pend 32 "the brief still carries $(grep -cF "$PH_STAMP" "$BRIEF") ${PH_STAMP} placeholder(s) (Self-check line and note, AZ-PRE-READ, the RULED lines of D4-D5) — the coordinator re-reads end-to-end and stamps all of them before launch"
fi

if [ -n "$PENDING" ]; then
  echo "guards pass (MODEL 40 6 9 7 8 18 22 23 74 63 31 39 10 17 12 78 45N 13 14 15 20 70 82 19 24 53 60 61 62 64 69 75 44 38R 86 46); coordinator to-do pending (47 48 41 32 as listed above); exiting $PENDING." >&2
  echo "  origin re-read $PIN_TS: main ${MAINH:0:7}, QQGD $H7, refs/pull/9/head $H7; model $MODEL; GH-API-LEG $GHLEG" >&2
  echo "  NEG seats (38R, derived live):$NEG_DESC" >&2
  exit "$PENDING"
fi

PIN_BLOCK="$(printf 'PINNED HEADS — verified by the launcher at %s (cat-file; base e4ce536 = the single parent, 0 behind; ancestor and merge-base with MAIN; not-already-on-main; commit count 1; e4ce536 <- 3dd15bc + 5ad37f1; head tree dc6aef6; main pinned EXACTLY; refs/pull/9/head = head; the 3-file delta, numstat, the test:print line, the one removed strip.js line; Kam'"'"'s W1/W2 sha256 in strip.js and the test; git ls-remote origin for both rows):\n' "$PIN_TS"
  printf '%s\n' "$PIN" | awk -F'\t' '{ printf "  %-7s %-11s %-42s %s  base %s  commits %s\n", $1, $2, $3, $4, ($5=="-"?"-":substr($5,1,12)), $6 }'
  printf '  Main: pinned %s (exact; a move refuses). PR #%s: refs/pull/%s/head = %s; refs/pull/%s/merge = %s (GitHub test merge)\n' "${MAINH:0:12}" "$PR_NUM" "$PR_NUM" "${HQ:0:12}" "$PR_NUM" "${PR_MERGE_NOW:-<absent>}"
  printf 'GH-API-LEG, as set in the brief: %s\n' "$GHLEG"
  printf 'AZ-READ-LEG, as set in the brief: %s (you run no az)\n' "$AZLEG"
  printf 'AZ-PRE-READ, as stamped by Tuesday: %s\n' "$AZPRE"
  printf 'LEG7-METHOD, as stamped by Tuesday (D5): %s\n' "$L7"
  printf 'NEGATIVE-CONTROL SEATS, derived live by the launcher from the cockpit panes at %s:%s Re-read them at start.' "$PIN_TS" "$NEG_DESC")"

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  printf '%s\n' "$PIN_BLOCK"
  echo "  model: $MODEL at exec (from models_latest.json); --check started no claude; nothing written."
  exit 0
fi

# 11 — no inherited identity: AZURE_CONFIG_DIR always EMPTY (no az in this gate); GH_CONFIG_DIR EMPTY unless GH-API-LEG = READ-ONLY-VISION-TOKEN.
ID_TMP="$(mktemp -d "${TMPDIR:-/tmp}/qa-vision-gate19-id.XXXXXX")" || { echo "REFUSING: cannot create the empty identity dir" >&2; exit 11; }
mkdir -p "$ID_TMP/azure-empty" "$ID_TMP/gh-empty" "$ID_TMP/bin" || { echo "REFUSING: cannot create the identity dirs under $ID_TMP" >&2; exit 11; }
{ [ -z "$(ls -A "$ID_TMP/azure-empty")" ] && [ -z "$(ls -A "$ID_TMP/gh-empty")" ]; } || { echo "REFUSING: the identity dirs under $ID_TMP are not empty" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_TMP/azure-empty"
export GH_CONFIG_DIR="$ID_TMP/gh-empty"
if [ "$GHLEG" = "READ-ONLY-VISION-TOKEN" ]; then
  QA_REAL_GH="$(command -v gh)" || { echo "REFUSING: gh vanished between guard 46 and launch" >&2; exit 11; }
  export QA_REAL_GH
  cat > "$ID_TMP/bin/gh" <<'SHIM'
#!/bin/bash
# gate-19 GET-only gh shim (written by launch_qa_vision_qq_gate19.sh; GH-API-LEG = READ-ONLY-VISION-TOKEN). Brief §HELD binds the rest.
REAL="${QA_REAL_GH:?gh shim: QA_REAL_GH unset}"
[ "${1:-}" = "api" ] || { echo "gh shim: only 'gh api' GET reads are allowed in Vision gate 19 (got: ${1:-<none>})" >&2; exit 64; }
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
export PATH="$ID_TMP/bin:$PATH"
if [ "$GHLEG" = "READ-ONLY-VISION-TOKEN" ]; then [ "$(command -v gh)" = "$ID_TMP/bin/gh" ] || { echo "REFUSING: the gh shim is not first on PATH" >&2; exit 11; }; fi
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"
[ -d "$CLAUDE_CONFIG_DIR" ] || { echo "REFUSING: Tuesday's claude store $CLAUDE_CONFIG_DIR is absent" >&2; exit 11; }
# 64 (cont.) — nothing a product process could use to reach a real provider is inherited from this shell.
unset DATABASE_URL TEST_DATABASE_URL AGENTMAIL_API_KEY AGENTMAIL_INBOX ACS_CONNECTION_STRING ACS_EMAIL_CONNECTION_STRING ACS_EMAIL_SENDER \
      MAIL_SENDER TABLES_CONNECTION_STRING AZURE_BACKUP_CONN_STR SESSION_SECRET HPAM_WORD ADVANCED_UNLOCK_SECRET SALES_COPY_EMAIL \
      FEEDBACK_NOTIFY_EMAIL FEEDBACK_NOTIFY_EMAILS APPROVALS_INBOX NTFY_TOPIC NTFY_SERVER LEAD_BOT_API_KEY WEBSITE_SITE_NAME COORDINATOR_SECRET \
      PORT NODE_ENV PUPPETEER_EXECUTABLE_PATH PAGE_RATE_LIMIT_PER_10_MIN OTP_IP_BUDGET_PER_HOUR OTP_GLOBAL_BUDGET_PER_HOUR GH_TOKEN GITHUB_TOKEN \
      GH_ENTERPRISE_TOKEN GITHUB_ENTERPRISE_TOKEN DOCKER_HOST DOCKER_CONTEXT
export npm_config_update_notifier=false
echo "identity: AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR (empty; AZ-READ-LEG $AZLEG) GH_CONFIG_DIR=$GH_CONFIG_DIR (GH-API-LEG $GHLEG) CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR" >&2

PROMPT="$PROMPT

$PIN_BLOCK"
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model "$MODEL" "$PROMPT"
