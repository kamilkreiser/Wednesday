#!/bin/bash
# launch_qa_vision_qq_gate21.sh — cross-project QA agent, ONE gate (Vision gate 21; drafted 2026-10-17 ~07:39-08:2x AEDT by a read-only drafting
# agent for Tuesday, from launch_qa_vision_qq_gate20.sh).
# Datasec/Vision_Sales_Portal, QuickQuote repo: ONE target, TIER 1 (quote output to customers), ONE verdict:
#   QQEP  fix/qq-email-matches-print-2026-10-16  PR #10 @ 3a3399e  ROUND 2 of 2 (cap): custom-price bound (ratio 10), key-by-key entry, reopen clears; v2.38
#
# Main is 437ab4b = LIVE v0.6.4-tool2.36-437ab4b. Round 1 (gate 20) = 7b952f6, NO GO on G20-F1.
# QQEP = SIX commits in a straight line: 437ab4b <- 0fc280b <- a8d769b <- 7b952f6 <- a7e1835 <- 1f7db41 <- 3a3399e. 6 ahead, 0 behind.
# THIS GATE PINS MAIN EXACTLY: a moved main REFUSES (PR #8 merging first would move it). refs/pull/10/head must equal the head.
#
# THE HEADS LIVE IN ONE PLACE: the brief's PIN-HEADS table. This launcher PARSES it, refuses any placeholder, verifies every row against the
# object store and against origin by `git ls-remote` NOW, and appends the verified table to the agent's prompt.
#
# Every path is on /Volumes/Laptop-DEV (gate 20's report and instruments are here too). The T9 QuickQuote repo is STALE and is never read.
#
# PRODUCTION IS LIVE for this project (hpas-quickquote / hpasqqacr; datasec-sales-portal-rg). This gate runs NO docker and NO az. Findings only.
# The live check is Kam's (Tuesday 2026-10-16 15:07: "do NOT read HPAM_WORD; live check 2b moves to Kam").
#
# GUARDS — gate 20's numbering kept where the guard survives; changes:
#   - PIN: two rows (MAIN-Q 437ab4b, QQEP 3a3399e base 437ab4b x6). Exact chain pin (six single parents); R1 7b952f6 an ancestor; head tree pin.
#   - 22/23: file set 8 + numstat whole, round 2 (7b952f6..head) and per round-2 commit; package.json's ONLY change is the test:print line
#         (email-matches-print + custom-price-bounds inserted after email-print-mode).
#   - 74: blobs (8 changed base->head, R1 blobs, the unchanged list incl. lockfile, Dockerfile, xlsx/mail/store); the SERVER MODULE now changes
#         (a854ba2 -> e40c20e); W1/W2 ABSENT at the head and PRESENT at base (by sha256); round-2 anchors present (cpCheck, customPriceMaxRatio 10,
#         #cpRefused role=alert, renderCustom(skipId), cpRestore returning the sentence, pdf.js refusals, the route's 422 + "refused", clearCustom,
#         toolVersion 2.38) and absent at R1.
#   - 31: the builder's round-2 mail on disk, pinned by sha256; it carries NO NOT TESTED / NOT RUN line (brief WRONG (a)); gate 20's report on disk
#         with its NO GO at 7b952f6 and G20-F1.
#   - 45N: the prompt and brief forbid docker; no docker command is run here at all.
#   - 46: GH-API-LEG must read READ-ONLY-VISION-TOKEN or NOT-RUN.
#   - 47: AZ-READ-LEG must read TUESDAY-READS; AZ-PRE-READ must be stamped and name linuxFxVersion (pending guard).
#   - 48: N4-METHOD (D5) = FULL-TEXT | FIGURES (pending guard while TUESDAY-DECIDES).
#   - 41: the routing line QA/Vision-gate21 in inbox_routing.conf (pending guard); 32 also counts the brief's ROUTING-LINE stamp.
#   - 86: no live QA/Vision-gate21 pane already.
#   - 47 48 41 32 are the coordinator's to-do guards: run LAST, reported TOGETHER, exit with the first pending code.
#
# LAUNCH IT IN A TMUX PANE:
#   /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add 'QA/Vision-gate21' "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_vision_qq_gate21.sh'"
#   NEVER nohup, never bare from a seat's shell.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# --check is READ-ONLY: git read verbs (cat-file, rev-parse, merge-base, log, rev-list, diff, show, ls-tree, ls-remote); tmux list-panes; ps;
# grep/python/shasum over files. It creates no identity dir, writes nothing and starts no claude.
# Usage: launch_qa_vision_qq_gate21.sh [--check]
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
BRIEF="$BRIEFS/2026-10-17_vision-gate21-qq-pr10-r2.md"
READY="$BRIEFS/2026-10-17_vision-qq-pr10-r2-READY-mail.txt"
READY_SHA='303d929851b9c775cb31a1c26d2c7aa4ffa62b61ee7b71c899df10854ab022b8'
CHARTER="$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"
MODELS_JSON="$TUE/0_Brain/dashboard/data/models_latest.json"
MODEL_PIN='claude-opus-5-5'
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
VSP='/Volumes/Laptop-DEV/!CODING/Datasec/Vision_Sales_Portal'
Q_REPO="$VSP/Quoting Tool/hpas-quoting-tool"
VSP_GH="$VSP/4_Credentials/.gh-config"
CLAR="$VSP/1_Project_Definition/CLARIFICATIONS.md"
REPORTS="$QA_DIR/projects/vision/reports"
G20_DIR="$REPORTS/2026-10-17-vision-gate20-qq-pr10-email-matches-print"
G20_REPORT="$G20_DIR/report.md"
G20_TOOLS="$G20_DIR/evidence/tools"
REPORT="$REPORTS/2026-10-17-vision-gate21-qq-pr10-r2/report.md"
ROUTE_NAME='QA/Vision-gate21'
BUILDER_PANE='Datasec/Vision_Sales_Portal'
CHROME_BIN='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
PR_NUM='10'
PR_MERGE_SEEN='1345ea5ec9817a6c290f9682f288c2b1bc5e94c8'     # refs/pull/10/merge at 07:39:16 (GitHub's test merge; NOTE only)
ANCHOR_MAIN='437ab4bc412bc74d8da3b66a6ac5c71d7335c5d6'     # QuickQuote main = LIVE v0.6.4-tool2.36-437ab4b
ANCHOR_MAINP='9d1c5ab8bc89aa2ba6b0063c22a858955d05a3e7 818a019ea21c39c5ef0a228f6242e7bdbb072761'
ANCHOR_PREGUARD='e4ce5367761e03db982189a3f21758aa06714a85'  # main before the guard
C1='0fc280b54aeab52c020692ed51fd018b20124eee'
C2='a8d769bbdea3d282c3b73ace336d09d4e18c9a0e'
R1='7b952f6edbcc3b271e4a650685f47b87760ed8f0'               # round 1's head = gate 20's NO GO
C4='a7e1835872b7ffd555608d263bc087dbeb4af02c'
C5='1f7db41a3215461adcda0a9e4c06b6b43507eece'
BACKLOG_F8='815aae76d842e5ce5bb5ca38de4b7770ab790c9f'       # G20-F8's ticket (backlog branch tip at drafting; NOT on the PR)
HQ_EXPECT='3a3399e947bf5faf8a8e0c0d3e11956c6590db98'
HQ_TREE='ec15fb204fa872917c9adcb3e2f819107bbf0a5e'
R1_TREE='25ddfb889661bde728906d0a2db7d32b148b21e8'
MAIN_TREE='c71780c82ea9cc338181163cb9d6045e07595e4f'
DELTA_FILES='index.html stage3/lib/pdf.js stage3/package.json stage3/server.js stage3/strip.js stage3/test/custom-price-bounds.mjs stage3/test/email-matches-print.mjs stage3/test/email-print-mode.mjs'
NUMSTAT_EXPECT='115/30/index.html 51/13/stage3/lib/pdf.js 1/1/stage3/package.json 9/0/stage3/server.js 25/26/stage3/strip.js 268/0/stage3/test/custom-price-bounds.mjs 165/0/stage3/test/email-matches-print.mjs 23/49/stage3/test/email-print-mode.mjs '
NUMSTAT_R2='62/13/index.html 20/5/stage3/lib/pdf.js 1/1/stage3/package.json 9/0/stage3/server.js 14/0/stage3/strip.js 268/0/stage3/test/custom-price-bounds.mjs 28/12/stage3/test/email-matches-print.mjs '
NUMSTAT_C4='60/13/index.html 20/5/stage3/lib/pdf.js 1/1/stage3/package.json 9/0/stage3/server.js 14/0/stage3/strip.js 268/0/stage3/test/custom-price-bounds.mjs '
NUMSTAT_C5='28/12/stage3/test/email-matches-print.mjs '
NUMSTAT_C6='2/0/index.html '
W1_SHA='0d5beedb47709eed6c7c6eec5d8ced3e73c58069ea09f49f4495cde1abeb25b9'
W2_SHA='4c73c1593e64f73dc84d24c48a69896307108d387b70a9318b0d7f7dd3ec797d'
# Kam's RETIRED words (U+201C/U+201D around Standard pricing only). Checked by sha256; used here only to prove they are GONE at the head.
W1='This email sends standard pricing only. Your custom pricing is on the printable quote, but it will not be in the email. Choose “Standard pricing only” above, or press the button again to send standard pricing anyway.'
W2='Send standard pricing anyway'

SUBJECT_STEM='[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 21'
QUESTION_SUBJ='[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>'
ANSWER_PREFIX='[Tuesday -> QA/Vision-gate21] ANSWER'
STATUS_SUBJ='[QA/Datasec-Vision -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch'
PARK_LINE='PARKED: flagged — awaiting the Opus 4.8 switch'

q() { git --no-optional-locks -C "$Q_REPO" "$@"; }
sha256s() { printf '%s' "$1" | shasum -a 256 | awk '{print $1}'; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE gate (Vision gate 21) on Datasec/Vision_Sales_Portal, in the QUICKQUOTE repo: ONE target, TIER 1 (quote output to customers: the email must equal the print), ONE verdict, GO / GO WITH FINDINGS / NO GO. QuickQuote main is 437ab4b and it is what is LIVE (v0.6.4-tool2.36-437ab4b; the brief's AZ-PRE-READ, appended below, is Tuesday's reading). The target QQEP (TIER 1; ROUND 2 of 2 of PR #10, under the two-NO-GO cap) is QuickQuote PR #10, branch fix/qq-email-matches-print-2026-10-16 at 3a3399e, SIX commits over 437ab4b. Round 1 was 7b952f6 (0fc280b email matches print through one shared builder, buildPrintDoc / buildPrintRows, the collector posting custom.pdmUSD, a8d769b the v2.36 guard removed, 7b952f6 test wording), gated by gate 20: NO GO on G20-F1 (a pasted 1e308 custom price printed and emailed "A$∞"). Round 2 adds a7e1835 (the custom-price bound cpCheck: a number, more than zero, at most CONFIG.customPriceMaxRatio = 10 times the standard per-device price, on the four fields, Apply %, the renderer's cpRestore and the route, which answers 422 and marks the reserved number "refused"; key-by-key entry kept; reopen clears the custom price and print mode; toolVersion 2.38), 1f7db41 (three fleet-scale email-matches-print cells; the workbook order enforced) and 3a3399e (CSS inset for the refusal box). The ratio 10 is the builder's choice and a number Kam will see. ROUND 2 OF 2 UNDER THE CAP: a NO GO here does not open round 3; it ships the instances you mark CLOSED and tickets the rest, and there is no round 3 without Kam. So your §N10 closure table (CLOSED / OPEN / NEW per instance, with evidence) is what Tuesday ships and tickets from. This is C-20's fix (2), Kam's ruling on card quickquote-email-sends-standard-not-custom-1016 = a, 2026-10-16 13:25:51 AEDT: "Publish the guard as soon as it passes the gate, full fix after". Kam's grant covered the GUARD only: publishing fix (2) needs Kam's own word, never yours. The lockfile, the Dockerfile, lib/xlsx.js, lib/mail.js and lib/store.js are byte-identical at base, round 1 and head; the hosted server module CHANGES in round 2 (the 422 branch). This machine is Kam's Mac mini, working volume /Volumes/Laptop-DEV; gate 20's report and instruments are on this drive; the T9 QuickQuote repo is STALE, never read it.

RULINGS CHECKED AS BUILT, NOT RE-OPENED: Tuesday ruled (2026-10-17 06:58:14) that the §N3 FAIL clause applies to G20-F1, with the fix-shape "bound the custom price both where it is set and where it is rendered … a non-finite or out-of-bound pdmUSD is refused with a message, never rendered" and the regression cell "your P8p paste case": you grade round 2 against that, clause by clause. The Custom pricing note stays OFF the emailed PDF and ON the print (Tuesday 2026-10-16 ~14:02; reversible by Kam); the guard's removal is approved and Kam's two guard sentences W1/W2 are RETIRED, so they must appear NOWHERE (W1 begins "This email sends standard pricing only."; W2 is "Send standard pricing anyway"). PRE-EXISTING FACT: the print CSS .q-savings { display:none } (5ef2a60, since v1.88) hides the Custom pricing note and the standard Value note on paper; you REPORT the note per mode and surface, you do not grade the product choice. The access word is not your subject: never read, print, grep for, type or reproduce the access word or the offline page's constant (gate 20's self-finding S5).

READ YOUR COMMISSION FIRST, whole: /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-17_vision-gate21-qq-pr10-r2.md
Then read the charter it names, the Vision CLARIFICATIONS (C-01..C-20; C-20 is Kam's ruling), the project's CLAUDE.md (/Volumes/Laptop-DEV/!CODING/Datasec/Vision_Sales_Portal/CLAUDE.md, its QuickQuote section; its deploy commands are not for you), the QuickQuote repo's own CLAUDE.md at the head (git show; its publish lines are not for you), the builder's round-2 READY mail, read WHOLE (/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-17_vision-qq-pr10-r2-READY-mail.txt; it carries NO NOT TESTED block), and gate 20's report, read WHOLE: /Volumes/Laptop-DEV/!CODING/Testing Agent MAIN/projects/vision/reports/2026-10-17-vision-gate20-qq-pr10-email-matches-print (NO GO on 7b952f6; G20-F1..F8, O1-O4, S1-S5 are the reference for this page and the findings you re-test; its evidence/tools/ holds the instruments you copy; its evidence/mail/verdict-body.txt is the verdict as mailed). Every builder statement is a CLAIM, never evidence. RE-DERIVE every red, every mutant, every suite set, every browser result and every comparison yourself. Verify every PRIOR WORK claim against git history, never against the brief. The brief's WRONG list, MODEL RULE and TUESDAY'S RULINGS (R1-R8 and the stamped D4-D5) are stamped: apply them, do not re-rule them.

WHAT THE BRIEF REQUIRES, in short (the brief is the authority):
(1) THE DIFF against the READY's claims: the whole delta 437ab4b..3a3399e and the round-2 delta 7b952f6..3a3399e hunk by hunk and per commit; one bound (cpCheck) in three places (fields and Apply %, the renderer through cpRestore, the route trusting report.refused); what the bound's denominator depends on; the changed route in the hosted server module read whole (reservation, 422, "refused", the reopen lookup, retention); the PR files API equal to git diff --numstat; no dependency or Dockerfile change; what node strip.js generates at base, round 1 and head, every line mapped; cpCheck, cpRefuse, cpRestore and the refusal box never in the stripped public page.
(2) THE RED-PROOFS AND MUTANTS: the head's custom-price-bounds.mjs (blob 76368d2) on a fresh 7b952f6 tree and on 437ab4b, and the head's email-matches-print.mjs (blob bdb602b) on 7b952f6 (predicted to PASS: F7 is test strength); tamper asserted landed; node --check rc 0 (a file that does not parse is VOID); quote every failing assertion and classify it DEFECT-REASON or NEW-SURFACE-ABSENT; all three files pass at 3a3399e, 3 runs each, timings with the load. Round 1's mutants re-run at the head (G21-R1..R8 = G20-M1..M8; the READY claims the fleet cells now see G20-M2) and the new mutants G21-M1..M10 (page-only bound off, renderer-only bound off, route-only, the ratio loosened to 1000 which no committed cell is expected to see, zero allowed, type coercion, F2 reverted, F6 reverted, the no-price refusal removed, the workbook block order), each landed in the file it reaches; say which cells see each, or NONE.
(3) A REAL-BROWSER DRIVE THROUGH THE REAL SERVER PATH, gate 20's whole matrix kept: your harness runs the tree's hosted server module's createApp() export in-process (never its entry point) with the repo's in-memory store pattern, a CAPTURING stub mail, a salesCopy option on a .invalid domain, throwaway session and unlock secrets (never a real secret, never the HPAM word), the tree's own renderQuotePdf, a frozen clock, on 127.0.0.1 and a kernel port; teach it the 422 path. ONE Google Chrome through your egress-block wrapper signs in with the captured OTP, unlocks advanced through the page's own controls, fills the form as a rep, sets a custom price, picks each print mode by its label, captures the page's own Generate output as a PDF in print media A4, and presses the page's own Email button ONCE. THE REQUIRED GRID at head, at base AND at round 1: advanced x "Standard pricing only" / "Custom pricing only" / "Standard + custom" x AUD / USD / CAD, plus simple sessions and advanced-standard-no-price x AUD / USD / CAD. PROBES P1-P15: the double-press timing (also on a refused state); Reset form, Advanced off (and P3': Advanced off then fewer apps, where a refused STANDARD email is a FAIL), clearing the custom figure, the ticket's Reset to default; C-05 reopen (same page, fresh session, B while A's price is live, a refused number); a currency change after the price; every custom-price field typed key by key AND pasted, and the 2,500-device 5-year STRESS state for currency rounding; the P8p paste of 1e308; a canned "live" FX rate answered inside the drive Chrome and the print-before-rate race (ticketed, reported); crafted bodies from the signed-in page to YOUR loopback server only; mixed versions (a v2.36 tab after a v2.38 publish now predicted to get the no-price refusal; the head page on the base server, i.e. tabs open across a rollback); the lone revert of a8d769b in YOUR tree only; no stale W1/W2 and no svc-warn on the email note (the refusal box legitimately uses svc-warn); light and dark, 1280 / 375 / 320 px, with a refusal showing; and P15, a refused send end to end (422, the note, 0 mails, the store row, numbers consumed).
(4) WHAT THE RECIPIENT GETS vs WHAT THE REP PRINTED, per the brief's N4-METHOD (appended below): pdftotext -layout full text with ONLY the quote number normalised, the money-figure multiset, pdfinfo pages and A4, pdffonts, pdftoppm -r 100 pixels per page in plain python (no ImageMagick, PIL or numpy) with the bbox of every differing region; the workbook part by part; an ∞ / Infinity / NaN / undefined scan on every PDF and workbook. Controls that can fail first (a planted one-word, one-digit and one-pixel change; a planted A$∞; the base defect pair; AUD vs CAD). The note table per mode. The captured mail's to, bcc, subject and text; a refused send reaches nobody.
(5) SIMPLE SESSIONS AND STANDARD EMAILS UNCHANGED vs MAIN but for v2.36 -> v2.38 (count them), pixels only inside those lines, the posted body only by the custom key; the OFFLINE index.html opened as a file prints the same as main's in each mode x AUD/USD/CAD, and refuses the offline 1e308 paste; AND every head grid cell's email equal to round 1's but for v2.37 -> v2.38.
(6) THE CI SUITES as CI runs them, at 3a3399e, 7b952f6 and 437ab4b, as SETS, NOT COUNTS: root node --test quote-engine.test.mjs; in stage3/: npm test, npm run test:print (added over round 1 exactly the 15 custom-price-bounds names and the 3 fleet-scale names), npm run test:xlsx. npm ci --offline --ignore-scripts only, the lockfile proven entry by entry (lockcmp.py AND lockwalk.py), npm ls --all. Host Node is 26.8.1, not CI's 22: say so. test:azurite is READ from CI (no docker), and it does not exercise the "refused" status.
(7) THE GENERATED FILES: cpExport/cpRestore/cpCheck and the refusal box only in private/advanced.js, never in the stripped public/index.html; no guard text in any generated file; the offline page's cpRestore refuses 1e308.
(8) NOTHING PUSHED, MERGED OR PUBLISHED: your command log proves no push, merge, docker, az, GitHub write or request to the live site; the live webapp's linuxFxVersion is RELAYED from the brief's AZ-PRE-READ (Tuesday re-reads at verdict); what a publish of 3a3399e would ship (the live tag's sha .. 3a3399e, the hosted server module included), READ ONLY; rollback facts from P11 and P12; deploy-on-merge READ ONLY.
(9) CI AND CODEQL on PR #10 at 3a3399e, READ ONLY, by GH-API-LEG: runs 38962577169 and 38962582879 and their jobs, the print-fit log lines, the check runs, code-scanning open on main and on the PR ref; the PR-side CodeQL zeros are a blind instrument: say only what they can show; never dismiss an alert.
(10) ROUND-1 FINDINGS RE-TESTED, EACH A CHECK THAT CAN FAIL: G20-F1 (every instance: the P8p paste, crafted 1e308 custom and both, 0 and -100 %, absurd finite, the A$0.00 edge, a stale price after the form changed) and Tuesday's fix-shape clause by clause; G20-F2 key by key (and typing through a refusal in custom mode); G20-F6 reopen; G20-F7 (G20-M2 now seen by the fleet cells; the order assertion able to fail); G20-F3, F4, F5 re-measured for the publish card; G20-F8's ticket 815aae7 verified and the race re-measured. Each closure needs a red at 7b952f6 (or base) from YOUR run and a green at 3a3399e; a check green on both sides is VOID for closure. Output the closure table: CLOSED / OPEN / NEW per instance.
(11) THE BOUND AT ITS EDGES: just under, at (A$310.00 on the full bundle; Apply +900; the 4-dp per-day figure), just over, a pasted 1e308, zero and the A$0.00 edge (tiny positive prices), negatives, non-numeric pastes, locale-formatted numbers, a stale price after the app selection shrinks (B-STATE: in "Standard pricing only" a refusal is a FAIL), a currency change, a canned live rate, crafted 200 / 200.01 / 1e-9 USD — each on screen, print/PDF, email, workbook and offline; and THE NUMBER for Kam in one line.
GH-API-LEG (appended below by the launcher as the brief sets it): READ-ONLY-VISION-TOKEN means gh is on your PATH as a GET-only shim over Vision's gh config — gh api GET reads only, never -X/--method, -f/-F/--field/--raw-field/--input or graphql, never a comment, review, label, approval, re-run or dismissal; NOT-RUN means none. AZ-READ-LEG is TUESDAY-READS: you run no az at all. Never open any file under the project's 4_Credentials.

PRODUCTION IS LIVE for this project. NEVER the live QuickQuote (hpas-quickquote, hpas-quickquote-rg, hpasqqacr, its Table Storage, its log workspace) and NEVER the live portal (datasec-sales-portal.azurewebsites.net, datasec-sales-portal-rg): no HTTP request, not even a GET; press nothing there. The live check is Kam's: never read, ask for or type the HPAM word. No az; no deploy, no publish, no app-setting change, no ACR build, no registry push. Never the FX hosts (blocked by your wrapper; the canned rate is answered inside Chrome), never ntfy.sh. Never Claude in Chrome (Kam's own Chrome with his sign-ins). NO EMAIL TO ANY HUMAN ADDRESS: every send goes to your capturing stub mail on .invalid addresses; your own AgentMail calls go only to tuesday-agent@agentmail.to. NO DOCKER: not a build, not a run, not even docker images or docker ps; never touch work-g18, work-g19, work-g20 or any qa-g18-* object. NETWORK, and only this: git ls-remote origin; gh api GETs if GH-API-LEG allows; your AgentMail calls. No npm registry (npm ci --offline), no npm audit.

ONE BROWSER AT A TIME: never two drive Chromes of yours alive at once (a suite's own Chromes count); never a suite and a browser drive concurrently; one retry per cell at most, then NOT RUN with the load.

HELD: no merge, no push, no publish, no comment or status on PR #10 or PR #8, no alert dismissal, no mail to any human. TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT on this drive from the object store (git archive into a fresh mktemp -d under projects/vision/work-g21/ in /Volumes/Laptop-DEV/!CODING/Testing Agent MAIN). Each tree is EXCLUSIVE to this gate and to one purpose; never touch any other work directory. The builder's checkout is LIVE: never read any working tree as evidence; never use the name main in the repo, only the pinned 40-hex shas. Copy gate 20's instruments into YOUR evidence/tools and re-point them (they hard-code work-g20, the gate-20 report folder, @qa-g20.invalid and v2.37); never run from, edit or write into gate 1-20's copies. Never npm install, never npm audit fix, never npx anything not already in the tree. In the repo use ONLY read verbs (show, log, diff, ls-remote, rev-parse, ls-tree, cat-file, grep, merge-base, archive); never fetch, pull, checkout, switch, worktree, commit, stash, reset, clean, gc, branch, revert or for-each-ref; the lone-revert probe patches YOUR extracted tree with patch, never the repo. Run git merge-tree --write-tree only from the gate's OWN object dir, or skip it and say so. Findings-only: no writes in the QuickQuote repo, none inside Vision_Sales_Portal, none in gate 1-20's report folders or trees. Never rm: quarantine. Run every loop and every git show <sha>:<path> under bash. Run node strip.js before any lone browser file. CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY: every round-1 closure needs its red from your own run; the base column must show the emailed custom figure differing from the printed custom figure before the head's match is credited to fix (2); the PDF comparator and the ∞ scan must report a planted difference; the stale-words scan must find W1 on the base page; a control derived from the run it validates is not a control.

FLOOR DISCIPLINE. Vision has no jest lock; never borrow NexusAI's. Never use host ports 4848, 8080 or 47787; host processes take every port from the kernel and bind 127.0.0.1. Every host product process runs under env -i with an explicit allowlist, NODE_ENV never production. Never set AGENTMAIL_API_KEY or AGENTMAIL_INBOX in a product process (with both set, QuickQuote SENDS FOR REAL), nor any real ACS_* or MAIL_SENDER, TABLES_CONNECTION_STRING, SALES_COPY_EMAIL, HPAM_WORD, ADVANCED_UNLOCK_SECRET, SESSION_SECRET, WEBSITE_SITE_NAME, GH_TOKEN or GITHUB_TOKEN; print each product process's env KEY NAMES and assert none is forbidden. NTFY_SERVER=http://ntfy.invalid; never contact ntfy.sh. EGRESS INCLUDING CHROME CHILDREN: every Chrome runs under your copy of the egress-block wrapper as PUPPETEER_EXECUTABLE_PATH; prove the block with its positive control and run the net-log scan at the end; record GoogleUpdater and chrome_crashpad_handler at start and end; reap every Chrome and every app listener by the pid you started. Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid, at START and at END, with the negative-control seats the launcher derived (listed at the end of this prompt) classifying FOREIGN in the same run. A zero is reportable only beside an ATTACHED control that fired in the same window. Record the load average beside every timing number; a latency result with no load figure is not a measurement.
DEADLINE AND HEARTBEAT: every step has a written DEADLINE built into your runner (there is no timeout binary here) and releases its Chromes, pages, children, app servers and temp profiles in a finally. Log a HEARTBEAT line at least every 2 minutes; a step with no heartbeat for 5 minutes is aborted and reported, never waited on. Deadlines: one browser cell 120 s; one red-proof or mutant arm 420 s; the root pack 120 s; a whole npm test 300 s; a whole test:xlsx 300 s; a whole test:print 900 s; nothing above 900 s. Under the brief's D4, a red-proof, the head grid or its N4 comparison, the R1-F1 pair, or the bound's at / over / stale-state rows NOT RUN makes the verdict PROVISIONAL.

THE MODEL RULE (Kam, live board 2026-09-30 09:07, card (b)): QA gates may switch to Opus 4.8 when flagged by Opus 5.5's safeguards, PER SESSION. You start on Opus 5.5. You run the FULL rows. If one of your responses is stopped by the safeguards: that step is NOT RUN (never re-worded to slip past); write ONE line to evidence/classifier-stops.txt; reap any Chrome and app server you started; mail tuesday-agent@agentmail.to with the subject exactly "[QA/Datasec-Vision -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch"; then end your turn with the line "PARKED: flagged — awaiting the Opus 4.8 switch" and wait. Tuesday switches THIS pane's model and taps you by mail. You never answer the model dialog yourself, and nobody ever chooses "Switch automatically". After the switch, resume at the stopped row. The report states which rows ran on which model, with the switch time, and quotes classifier-stops.txt whole.

QUESTIONS: your routing name is QA/Vision-gate21. If you must ask, mail tuesday-agent@agentmail.to with the subject "[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>" and proceed on the safest reading without waiting (the one exception is a safeguards stop, which PARKS you under THE MODEL RULE). Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/Vision-gate21] ANSWER"; read it with your verdict key. Never wednesday-agent@. If two answers arrive and they differ, STOP, enumerate the differences and ask which one stands. If a response is cut off by a safety check, record it and continue with the next item; this is authorised defensive QA of Datasec's own product on loopback. Approval-class items (a publish, a deploy, the live site, money, a human) are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your report to: /Volumes/Laptop-DEV/!CODING/Testing Agent MAIN/projects/vision/reports/2026-10-17-vision-gate21-qq-pr10-r2/report.md
Write its VERDICT and FINDINGS table early and keep it current. Number findings G21-F1, G21-F2, …; a round-1 finding re-tested keeps its G20 id in the closure table.

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with a subject beginning exactly:
[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 21: QQEP @ <sha7> <GO | GO WITH FINDINGS | NO GO>
(the sha7 is the pinned head from the verified table below; append PROVISIONAL if the brief's D4 clause applies). Lead the body with ONE sentence as the brief's section 14 words it (round-1 findings closed by your own red/green pairs; the real hosted page through the real server path still emailing exactly what the rep printed in every print mode x currency on one press; the bound refusing what it should and only that on every surface; simple and standard emails unchanged but for the version; the CI suites as sets; anything pushed, merged or published), then a line "VERDICT: <token>, round 2 of 2 (…)" with what happens next under the cap, then one line each on the closure table, THE NUMBER (the ratio-10 maximum per currency and the smallest accepted price as printed), the stale-price state, the A$0.00 edge, non-numeric and locale pastes, the refused send end to end, the base column, the mutants, P1, the resets, C-05 reopen, key-by-key entry and rounding at the stress state, the FX race, the crafted bodies, mixed versions and rollback, the lone revert, the note per mode, head vs round 1, the live site read (RELAYED), what a publish would ship, and the class count (round 2 of 2: a NO GO ships the closed instances and tickets the rest). You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/Laptop-DEV/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no credentials directory of its own. Use it only in your own mail calls, with a client timeout. Never put the key or any secret in a mail, the report or a product process.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice — the only turn you end while waiting is the PARKED line of THE MODEL RULE.

Report the pinned head and main as three timestamped readings (start / mid / end), with the branch name beside each, plus refs/pull/10/head. Include a table with one row per brief section N item: MEASURED, NOT TESTED, NOT RUN or VOID, and HOW (command, tree, browser, port, load).

Rule 2 stands: what you did NOT test is first-class output. Say the READY carried no NOT TESTED block. Write a NOT TESTED section that covers at least the published image (no docker by design), a real ACS send, the live site (Kam's check), CodeQL's verdict before the merge (blind), CI's Node 22 (read only, never caused), store-azurite (read from CI; it does not exercise "refused"), a real live FX provider, currencies and Chrome locales you did not drive, Windows, Safari, real phones, real printers and the account managers' real browsers, a customer's mail client, screen readers, Claude in Chrome (not used), PR #8 (not this gate), and every row you did not run. Label every action recommendation MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. The tester never fixes.
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
EXPECT_IDS='MAIN-Q QQEP'
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
[ "$(fld QQEP 3)" = "fix/qq-email-matches-print-2026-10-16" ] || { echo "REFUSING: row QQEP branch is '$(fld QQEP 3)', the brief's target is fix/qq-email-matches-print-2026-10-16 — re-brief" >&2; exit 40; }
is40 "$(fld QQEP 5)" || { echo "REFUSING: PIN row QQEP base is not a 40-hex sha" >&2; exit 40; }
printf '%s' "$(fld QQEP 6)" | grep -Eq '^[1-9][0-9]*$' || { echo "REFUSING: PIN row QQEP commits '$(fld QQEP 6)' is not a positive integer" >&2; exit 40; }
[ "$(fld QQEP 4)" = "$HQ_EXPECT" ] || { echo "REFUSING: QQEP's PIN head $(fld QQEP 4 | cut -c1-7) is not ${HQ_EXPECT:0:7} — this launcher's content guards are pinned to it; re-brief" >&2; exit 40; }
MAINH="$(fld MAIN-Q 4)"
HQ="$(fld QQEP 4)"

# 6 — every sha the guards use is a commit in the local object store (this launcher never fetches).
for S in "$MAINH" "$HQ" "$ANCHOR_MAIN" $ANCHOR_MAINP "$ANCHOR_PREGUARD" "$C1" "$C2" "$R1" "$C4" "$C5" "$BACKLOG_F8"; do
  T="$(q cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in the QuickQuote repo on this drive (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 9m — MAIN: 437ab4b EXACTLY (refuse if it moved).
[ "$MAINH" = "$ANCHOR_MAIN" ] || { echo "REFUSING: the pinned MAIN ${MAINH:0:7} is not 437ab4b — this gate pins main exactly; re-brief" >&2; exit 9; }

# 7 / 8 — the target: base as briefed, ancestor AND merge-base with MAIN, not on main, exact count, 0 behind; R1 an ancestor.
H7="${HQ:0:7}"; BASE="$(fld QQEP 5)"; N="$(fld QQEP 6)"
[ "$BASE" = "$ANCHOR_MAIN" ] || { echo "REFUSING: row QQEP base ${BASE:0:7} is not 437ab4b — re-brief" >&2; exit 7; }
q merge-base --is-ancestor "$BASE" "$HQ" 2>/dev/null || { echo "REFUSING: QQEP base ${BASE:0:7} is not an ancestor of $H7" >&2; exit 7; }
[ "$(q merge-base "$HQ" "$MAINH" 2>/dev/null)" = "$BASE" ] || { echo "REFUSING: QQEP merge-base(head, MAIN) is not its base ${BASE:0:7}" >&2; exit 7; }
q merge-base --is-ancestor "$HQ" "$MAINH" 2>/dev/null && { echo "REFUSING: QQEP $H7 is ALREADY ON MAIN ${MAINH:0:7} — the brief says it is not; re-brief" >&2; exit 7; }
q merge-base --is-ancestor "$R1" "$HQ" 2>/dev/null || { echo "REFUSING: round 1's head 7b952f6 is not an ancestor of $H7 — the branch was rewritten (force-push); re-brief" >&2; exit 7; }
GOTN="$(q rev-list --count "${BASE}..${HQ}" 2>/dev/null)"
[ "$GOTN" = "$N" ] || { echo "REFUSING: QQEP $H7 has $GOTN commits over its base, the table says $N" >&2; q log --format='%h %p %s' "${BASE}..${HQ}" >&2; exit 8; }
[ "$N" = "6" ] || { echo "REFUSING: the brief's commit count is $N, this launcher's chain is six commits" >&2; exit 8; }
[ "$(q rev-list --count "${HQ}..${ANCHOR_MAIN}" 2>/dev/null)" = "0" ] || { echo "REFUSING: QQEP $H7 is behind 437ab4b" >&2; exit 7; }

# 9 — gated anchors and the exact chain, by parents and trees.
[ "$(q log -1 --format='%P' "$ANCHOR_MAIN")" = "$ANCHOR_MAINP" ] || { echo "REFUSING: 437ab4b's parents are not 9d1c5ab + 818a019" >&2; exit 9; }
[ "$(q log -1 --format='%P' "$C1")" = "$ANCHOR_MAIN" ] || { echo "REFUSING: 0fc280b's single parent is not 437ab4b" >&2; exit 9; }
[ "$(q log -1 --format='%P' "$C2")" = "$C1" ] || { echo "REFUSING: a8d769b's single parent is not 0fc280b" >&2; exit 9; }
[ "$(q log -1 --format='%P' "$R1")" = "$C2" ] || { echo "REFUSING: 7b952f6's single parent is not a8d769b" >&2; exit 9; }
[ "$(q log -1 --format='%P' "$C4")" = "$R1" ] || { echo "REFUSING: a7e1835's single parent is not 7b952f6" >&2; exit 9; }
[ "$(q log -1 --format='%P' "$C5")" = "$C4" ] || { echo "REFUSING: 1f7db41's single parent is not a7e1835" >&2; exit 9; }
[ "$(q log -1 --format='%P' "$HQ")" = "$C5" ] || { echo "REFUSING: 3a3399e's single parent is not 1f7db41" >&2; exit 9; }
[ "$(q rev-parse "${HQ}^{tree}" 2>/dev/null)" = "$HQ_TREE" ] || { echo "REFUSING: 3a3399e's tree is not ec15fb2" >&2; exit 9; }
[ "$(q rev-parse "${R1}^{tree}" 2>/dev/null)" = "$R1_TREE" ] || { echo "REFUSING: 7b952f6's tree is not 25ddfb8" >&2; exit 9; }
[ "$(q rev-parse "${ANCHOR_MAIN}^{tree}" 2>/dev/null)" = "$MAIN_TREE" ] || { echo "REFUSING: 437ab4b's tree is not c71780c" >&2; exit 9; }
q merge-base --is-ancestor "$ANCHOR_PREGUARD" "$MAINH" 2>/dev/null || { echo "REFUSING: e4ce536 is not an ancestor of main" >&2; exit 9; }
q merge-base --is-ancestor "$BACKLOG_F8" "$HQ" 2>/dev/null && { echo "REFUSING: backlog 815aae7 is on the PR head — the brief says it is not" >&2; exit 9; }

# 18 — RE-PIN: BOTH rows AND refs/pull/10/head at origin, by ls-remote, read NOW (immediately before launch). No movement allowed, main included.
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

# 22 / 23 — exact file set, numstat (whole, round 2, per round-2 commit), and the shape of the package.json change.
GOT="$(q diff --name-only "$ANCHOR_MAIN" "$HQ" 2>/dev/null | sort)"
[ "$GOT" = "$(printf '%s\n' $DELTA_FILES | sort)" ] || { echo "REFUSING: QQEP ${H7}'s delta over 437ab4b is not exactly the briefed 8-file set. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }
ns() { q diff --numstat "$1" "$2" | awk '{printf "%s/%s/%s ", $1, $2, $3}'; }
[ "$(ns "$ANCHOR_MAIN" "$HQ")" = "$NUMSTAT_EXPECT" ] || { echo "REFUSING: the whole-diff numstat is not the briefed one. Got:" >&2; q diff --numstat "$ANCHOR_MAIN" "$HQ" >&2; exit 23; }
[ "$(ns "$R1" "$HQ")" = "$NUMSTAT_R2" ] || { echo "REFUSING: the round-2 numstat (7b952f6..head) is not the briefed one" >&2; q diff --numstat "$R1" "$HQ" >&2; exit 23; }
[ "$(ns "$R1" "$C4")" = "$NUMSTAT_C4" ] || { echo "REFUSING: a7e1835's numstat is not the briefed one" >&2; exit 23; }
[ "$(ns "$C4" "$C5")" = "$NUMSTAT_C5" ] || { echo "REFUSING: 1f7db41's numstat is not the briefed one (email-matches-print.mjs only)" >&2; exit 23; }
[ "$(ns "$C5" "$HQ")" = "$NUMSTAT_C6" ] || { echo "REFUSING: 3a3399e's numstat is not the briefed one (index.html +2 only)" >&2; exit 23; }
PKG_U0="$(q diff -U0 "$ANCHOR_MAIN" "$HQ" -- stage3/package.json | grep -E '^[+-][^+-]')"
[ "$(printf '%s\n' "$PKG_U0" | wc -l | tr -d ' ')" = "2" ] && printf '%s\n' "$PKG_U0" | grep -q '^-    "test:print": ' && printf '%s\n' "$PKG_U0" | grep -q '^+    "test:print": ' \
  || { echo "REFUSING: package.json's change is not exactly the test:print line. Got:" >&2; printf '%s\n' "$PKG_U0" >&2; exit 23; }
[ "$(printf '%s\n' "$PKG_U0" | sed -n 's/^-//p' | sed 's#test/email-print-mode.mjs #test/email-print-mode.mjs test/email-matches-print.mjs test/custom-price-bounds.mjs #')" = "$(printf '%s\n' "$PKG_U0" | sed -n 's/^+//p')" ] \
  || { echo "REFUSING: the test:print change is not ONLY test/email-matches-print.mjs + test/custom-price-bounds.mjs inserted after test/email-print-mode.mjs" >&2; exit 23; }
python3 - "$Q_REPO" "$ANCHOR_MAIN" "$R1" "$HQ" <<'PY' || { echo "REFUSING: the package.json dependency maps or version differ between base, round 1 and head (the brief says only a script line changed)" >&2; exit 23; }
import json, subprocess, sys
repo, b, r, h = sys.argv[1:5]
def pj(s): return json.loads(subprocess.run(['git','--no-optional-locks','-C',repo,'show',f'{s}:stage3/package.json'],capture_output=True,text=True,check=True).stdout)
B, R, H = pj(b), pj(r), pj(h)
keys = ('dependencies','devDependencies','overrides','engines','version','name')
sys.exit(0 if all(B.get(k) == H.get(k) == R.get(k) for k in keys) else 1)
PY

# 74 — content, read from the pinned shas (never a checkout).
blob() { q rev-parse --verify -q "${1}:${2}" 2>/dev/null; }   # --verify -q: a missing path prints NOTHING (bare rev-parse echoes the arg)
has() { q show "${1}:${2}" 2>/dev/null | grep -qF -- "$3"; }
must() { has "$1" "$2" "$3" || { echo "REFUSING: ${1:0:7}:$2 lacks '$3' — the brief gates different code; re-brief" >&2; exit 74; }; }
mustnot() { has "$1" "$2" "$3" && { echo "REFUSING: ${1:0:7}:$2 still carries '$3' — the brief says it is absent there; re-brief" >&2; exit 74; }; return 0; }
# file | base blob | round-1 blob | head blob   ('-' = absent)
for P in 'index.html|dde1392465fa3202db7eb28edf140639110d4417|51c6eb9d30f100c8bdb0938ee04441c26999ff46|cf71c84cbb9fc1e6d44ea0580c14644f556a2f93' \
         'stage3/lib/pdf.js|783ebea5ea8708e02df25740b75b51e631f2ce37|2e692d3475bc8d0a2aa884d595d45cb1529b164e|257bbfa8fa46a293be441307450ffaf3b73c20b3' \
         'stage3/package.json|1606aa3b4f0fa9b53811c7bc71f96cd57178a420|725a5e2b18f68da370dbb3270876f5d1169b912e|cd9118a1bfc24f8bf6968d08f6505a9e2cd42ccb' \
         'stage3/server.js|a854ba2c5144887c9e8ad530bedcaf4f8526f23f|a854ba2c5144887c9e8ad530bedcaf4f8526f23f|e40c20ec492cb6d3063a648f1f4ad3fc08fe0d23' \
         'stage3/strip.js|0730e10459550ad1a7f63f9d8bc388e0550ec0ea|7c372878a01b8890b43e3641b1bb8ef18d17f32b|9cddb706d71cf88c7db116554ef7480b17e7e73c' \
         'stage3/test/custom-price-bounds.mjs|-|-|76368d24709c1cfed6be98e64f77f4b587f6696f' \
         'stage3/test/email-matches-print.mjs|-|3ac0e3c93bc480b260c53ab9a4220066c97664ea|bdb602b8d4baedec60e54cdf398965eb62200aba' \
         'stage3/test/email-print-mode.mjs|b1d4443c45195cb80075dd443f07a59b6c53817c|9dd53112ddc07bbaf51c44a4de2d304da06b4ae5|9dd53112ddc07bbaf51c44a4de2d304da06b4ae5'; do
  F="${P%%|*}"; REST="${P#*|}"; B0="${REST%%|*}"; REST="${REST#*|}"; BR1="${REST%%|*}"; B1="${REST#*|}"
  [ "$B0" = "-" ] && B0=''; [ "$BR1" = "-" ] && BR1=''
  [ "$(blob "$ANCHOR_MAIN" "$F")" = "$B0" ] && [ "$(blob "$R1" "$F")" = "$BR1" ] && [ "$(blob "$HQ" "$F")" = "$B1" ] \
    || { echo "REFUSING: $F blobs are not ${B0:0:7}|${BR1:0:7}|${B1:0:7} at base|round 1|head" >&2; exit 74; }
done
for F in stage3/package-lock.json stage3/Dockerfile stage3/lib/xlsx.js stage3/lib/mail.js stage3/lib/store.js \
         stage3/login.html .dockerignore .github/workflows/tests.yml quote-engine.test.mjs stage3/test/print-fit.mjs stage3/test/email-collector.mjs \
         stage3/test/server.test.mjs stage3/test/lib-close.mjs stage3/test/xlsx-parity.mjs stage3/test/strip.test.mjs CLAUDE.md; do
  B0="$(blob "$ANCHOR_MAIN" "$F")"
  [ -n "$B0" ] && [ "$(blob "$HQ" "$F")" = "$B0" ] || { echo "REFUSING: $F differs between main and the head (or is absent) — the brief says it is carried unchanged" >&2; exit 74; }
done
# round-1 anchors still at the head (the email-matches-print machinery round 2 builds on)
for T in 'function buildPrintDoc(mode, qnum, opts = {})' 'function buildPrintRows(mode, qnum)' 'window.cpExport  = () => cpState;' \
         '{ hideCustomNote: mode === "custom" || !!opts.emailCopy, qnum }' '$("quoteDoc").innerHTML = buildPrintDoc(mode, docQnum);' \
         '#quoteDoc .q-savings { display: none !important; }'; do
  must "$HQ" index.html "$T"
done
# round-2 anchors at the head, and absent at round 1
for T in 'toolVersion: "2.38"' 'customPriceMaxRatio: 10,' 'function cpCheck(usd) {' 'function cpRefuse(msg) {' 'function renderCustom(skipId) {' \
         'const max = (c.stdPerDevMonth / c.fxRate) * CONFIG.customPriceMaxRatio;' \
         'if (typeof usd === "number" && Number.isFinite(usd) && usd > 0 && usd <= max) return null;' \
         '<div class="svc-warn" id="cpRefused" role="alert"></div>' 'const why = cpCheck(newPDM);' \
         '$(id).addEventListener("change", () => { if (cpState !== null) renderCustom(); });' '#cpRefused { margin: 0 1.1rem .55rem; }'; do
  must "$HQ" index.html "$T"
done
must "$R1" index.html 'toolVersion: "2.37"'
mustnot "$R1" index.html 'function cpCheck('
mustnot "$R1" index.html 'customPriceMaxRatio'
must "$ANCHOR_MAIN" index.html 'toolVersion: "2.36"'
for T in 'path.join(__dirname, "..", "private", "advanced.js")' 'buildPrintDoc(printMode, qnum, { emailCopy: true })' 'buildPrintRows(printMode, qnum)' \
         'const why = window.cpRestore(cu);' 'if (why) return { refused: why + " The quote was not sent." };' \
         'This quote asks for custom pricing but carries no custom price, so it was not sent. ' \
         'if (report.refused) return { pdf: null, xlsx: null, report };'; do
  must "$HQ" stage3/lib/pdf.js "$T"
done
mustnot "$R1" stage3/lib/pdf.js 'report.refused'
must "$HQ" stage3/strip.js 'custom: typeof window.cpExport === "function" ? { pdmUSD: window.cpExport() } : null'
must "$HQ" stage3/strip.js 'const LABEL = "Email me this quote (PDF & XLS)";'
must "$HQ" stage3/strip.js 'const hadCustom = clearCustom();'
must "$HQ" stage3/strip.js 'window.cpClear = cpClear;'
must "$HQ" stage3/strip.js 'Custom pricing is not saved with a quote, so it is off; enter it again if this quote needs it.'
mustnot "$R1" stage3/strip.js 'clearCustom'
for T in 'renderQuotePdf(state, { advanced: !!req.session.advanced, qnum })' 'Deliberately NOT stored' 'clock = () => new Date()' \
         'try { await store.updateQuote(qnum, { status: "refused" }); }' 'return res.status(422).json({ error: String(report.refused) });' \
         'if (!row || row.status !== "sent") return notFound();'; do
  must "$HQ" stage3/server.js "$T"
done
mustnot "$R1" stage3/server.js 'report.refused'
[ "$(q ls-tree -r --name-only "$HQ" .github)" = ".github/workflows/tests.yml" ] || { echo "REFUSING: .github at the head holds other than tests.yml — §N8.5's reading is wrong" >&2; exit 74; }
for T in 'pricing-pack:' 'stage3-server:' 'store-azurite:' 'print-fit:' 'xlsx-parity:'; do must "$HQ" .github/workflows/tests.yml "  $T"; done
must "$BACKLOG_F8" BACKLOG.md 'G20-F8'
# Kam's RETIRED words: the launcher's copy hashes; base strip.js carries them; head strip.js / index.html / pdf.js do not (by sha256 of every literal).
[ "$(sha256s "$W1")" = "$W1_SHA" ] && [ "$(sha256s "$W2")" = "$W2_SHA" ] || { echo "REFUSING: this launcher's own copy of the retired words does not hash to the pinned sha256 — the file was edited" >&2; exit 74; }
python3 - "$Q_REPO" "$ANCHOR_MAIN" "$HQ" "$W1_SHA" "$W2_SHA" <<'PY' || { echo "REFUSING: W1/W2 are not present at base strip.js and absent at the head's strip.js / generated-source inputs as the brief says" >&2; exit 74; }
import hashlib, re, subprocess, sys
repo, b, h, w1, w2 = sys.argv[1:6]
def show(s, p): return subprocess.run(['git','--no-optional-locks','-C',repo,'show',f'{s}:{p}'],capture_output=True,check=True).stdout.decode('utf-8')
def lits(src): return set(re.findall(r'"((?:[^"\\\n]|\\.)*)"', src)) | set(re.findall(r"'((?:[^'\\\n]|\\.)*)'", src))
def hashes(src): return {hashlib.sha256(x.encode()).hexdigest() for x in lits(src)}
base = hashes(show(b, 'stage3/strip.js'))
if w1 not in base or w2 not in base: sys.exit(1)                        # control: the scan FINDS them at base
for p in ('stage3/strip.js', 'index.html', 'stage3/lib/pdf.js'):
    src = show(h, p)
    if {w1, w2} & hashes(src): sys.exit(1)
    if 'Send standard pricing anyway' in src or 'This email sends standard pricing only.' in src: sys.exit(1)
PY
for T in 'npm ci --offline --ignore-scripts' 'entry by entry' 'never `npm audit fix`'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the dependency rule '$T'" >&2; exit 63; }
done
for T in 'npm ci --offline --ignore-scripts' 'entry by entry' 'never npm audit fix'; do
  printf '%s\n' "$PROMPT" | grep -qiF -- "$T" || { echo "REFUSING: prompt lacks the dependency rule '$T'" >&2; exit 63; }
done

# 31 — the builder's round-2 mail is on disk byte for byte, names the pinned head, carries no NOT TESTED / NOT RUN line; gate 20's report on disk.
[ -s "$READY" ] || { echo "REFUSING: the builder's round-2 mail is not on disk: $READY" >&2; exit 31; }
[ "$(shasum -a 256 "$READY" | awk '{print $1}')" = "$READY_SHA" ] || { echo "REFUSING: $READY is not the copy the drafter read (sha256 differs) — re-read it and re-brief" >&2; exit 31; }
for T in 'READY FOR QA, round 2 of 2, tier 1.' 'PR #10, head 3a3399e (new commits on 7b952f6, no force-push). Version is now 2.38' \
         'CONFIG.customPriceMaxRatio (10)' 'custom-price-bounds.mjs: RED 14/15 on 7b952f6 (only the sane control passes), GREEN 15/15 at head.' \
         'Pricing 69/69. npm test 132/132. test:print 200/200 (182 + 15 + 3). test:xlsx 6/6.' 'G20-F8: TICKET (backlog 815aae7).' \
         'The ratio 10 is my choice and sits in CONFIG for Kam to change.'; do
  grep -qF -- "$T" "$READY" || { echo "REFUSING: $READY does not carry '$T'" >&2; exit 31; }
done
[ "$(grep -ci 'not tested' "$READY")" = "0" ] && [ "$(grep -ci 'not run' "$READY")" = "0" ] \
  || { echo "REFUSING: the round-2 READY now carries a NOT TESTED / NOT RUN line — WRONG (a) says it has none; re-brief" >&2; exit 31; }
for T in 'carries no NOT TESTED block' 'C-20' 'quickquote-email-sends-standard-not-custom-1016' 'quickquote-guard-words-1016' 'ROUND 2' 'round 2 of 2' \
         'two-NO-GO cap' 'ships the closed instances' '2026-10-17_vision-qq-pr10-r2-READY-mail.txt' 'WRONG (a)' 'WRONG (b)' 'WRONG (c)' 'WRONG (d)' \
         'WRONG (e)' 'WRONG (f)' 'WRONG (g)' 'WRONG (h)' 'WRONG (i)' 'WRONG (j)' 'WRONG (k)' 'WRONG (l)' 'WRONG (m)' 'WRONG (n)' 'GH-API-LEG' \
         'AZ-READ-LEG' 'AZ-PRE-READ' 'N4-METHOD' 'ROUTING-LINE' 'D4' 'D5' 'PROVISIONAL' 'G20-F1' 'G20-F2' 'G20-F3' 'G20-F4' 'G20-F5' 'G20-F6' \
         'G20-F7' 'G20-F8' 'G21-R1' 'G21-M1' 'G21-M4' 'G21-M10' 'G21-F1' 'R-D' 'R-E' 'R-F' 'P3'"'" 'P15' 'B-STATE' 'L-EDGE' 'U-AT' 'U-OVER' 'NONNUM' \
         'LOCALE' 'THE NUMBER' 'DEFECT-REASON' 'NEW-SURFACE-ABSENT' 'customPriceMaxRatio' 'cpCheck' '422' '1e308' '815aae7' 'cdcd490' '5ef2a60' \
         'pdmUSD' 'buildPrintDoc' 'emailCopy' "$W1_SHA" "$W2_SHA" 'HPAM' 'live check' "$READY_SHA" '7b952f6' 'S5'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: the brief does not carry '$T'" >&2; exit 31; }
done
for R in 'R1: ' 'R2: ' 'R3: ' 'R4: ' 'R5: ' 'R6: ' 'R7: ' 'R8: '; do
  grep -qF -- "- $R" "$BRIEF" || { echo "REFUSING: the brief does not carry Tuesday's ruling '$R' as a ruling line" >&2; exit 31; }
done
[ -s "$CLAR" ] || { echo "REFUSING: Vision CLARIFICATIONS.md absent: $CLAR" >&2; exit 31; }
grep -qF '**C-20.' "$CLAR" || { echo "REFUSING: $CLAR lacks C-20" >&2; exit 31; }
for T in 'quickquote-email-sends-standard-not-custom-1016' 'Publish the guard as soon as it passes the gate, full fix after' "Kam's grant covers the GUARD only" \
         'Fix (2) and PR #8 (C-19) each need Kam'"'"'s own word before any publish'; do
  grep -qF -- "$T" "$CLAR" || { echo "REFUSING: CLARIFICATIONS C-20 does not carry '$T' — the ruling the brief quotes is not on disk" >&2; exit 31; }
done
grep -qF '**C-21.' "$CLAR" && echo "NOTE: Vision CLARIFICATIONS now has a C-21 — the brief says C-01..C-20; read it before launch (Tuesday owes Vision a C-entry for the access-word ruling)" >&2
[ -s "$CHARTER" ] || { echo "REFUSING: the charter is absent: $CHARTER" >&2; exit 31; }
[ -s "$G20_REPORT" ] || { echo "REFUSING: gate 20's report is absent: $G20_REPORT" >&2; exit 31; }
grep -qF '**NO GO**' "$G20_REPORT" && grep -qF "$R1" "$G20_REPORT" && grep -qF 'G20-F1' "$G20_REPORT" && grep -qF 'G20-F8' "$G20_REPORT" \
  || { echo "REFUSING: gate 20's report does not carry QQEP's NO GO at 7b952f6 with G20-F1..F8" >&2; exit 31; }
[ -s "$G20_DIR/evidence/mail/verdict-body.txt" ] || { echo "REFUSING: gate 20's verdict body is not on disk" >&2; exit 31; }
grep -qF "$G20_DIR" "$BRIEF" || { echo "REFUSING: the brief does not name $G20_DIR" >&2; exit 31; }
case "$PROMPT" in *"$G20_DIR"*) ;; *) echo "REFUSING: the prompt does not name $G20_DIR" >&2; exit 31 ;; esac
for H in qa-run.py mktree-qq.sh lockcmp.py lockwalk.py tapsets.py g17-dupnames.py g20-run-suites.sh g20-mutate.py g20-mutant-arm.sh g20-compare.py \
         g20-n4-run.py g20-n4-multi.py g20-n5.py g20-gh.sh g20-cell.sh g20-arm.sh g20-repoint.py qa-harness-g20-drive.cjs qa-harness-g20-offline.cjs \
         qa-harness-g16-shots.mjs qa-chrome-egressblock.sh qa-chrome-census.py qa-egress-posctl.mjs qa-floorcount.py qa-harness-floorctl.mjs qa-netlog-scan.py; do
  [ -s "$G20_TOOLS/$H" ] || { echo "REFUSING: gate 20's tool $H is not on disk — the brief names it" >&2; exit 31; }
  grep -qF -- "$H" "$BRIEF" || { echo "REFUSING: the brief does not name gate 20's tool $H" >&2; exit 31; }
done

# 39 — the floor instrument is on disk and named.
[ -s "$G20_TOOLS/qa-floorcount.py" ] || { echo "REFUSING: gate 20's floor instrument copy missing" >&2; exit 39; }
grep -qF 'qa-floorcount.py' "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument qa-floorcount.py" >&2; exit 39; }

# 10 / 17 — report path named in both; no stale report.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

# 12 — tier declared in both, at the pinned head.
grep -qE "^- \*\*QQEP\*\* at \`${H7}\` — \*\*TIER 1" "$BRIEF" || { echo "REFUSING: brief does not declare QQEP at \`$H7\` TIER 1" >&2; exit 12; }
case "$PROMPT" in *"QQEP (TIER 1"*) ;; *) echo "REFUSING: prompt does not declare: QQEP (TIER 1" >&2; exit 12 ;; esac

# 78 — the commission's requirements, in both.
for T in 'TIER 1' 'ROUND 2' 'round 2 of 2' 'C-20' 'quickquote-email-sends-standard-not-custom-1016' 'GO WITH FINDINGS' 'NO GO' \
         'SETS, NOT COUNTS' '3a3399e' '7b952f6' '437ab4b' 'a8d769b' 'a7e1835' '1f7db41' 'custom-price-bounds.mjs' 'email-matches-print.mjs' \
         'createApp()' 'renderQuotePdf' 'frozen clock' 'Standard pricing only' 'Custom pricing only' 'Standard + custom' 'Custom pricing note' \
         'q-savings' 'light' 'dark' 'buildPrintDoc' 'cpCheck' 'customPriceMaxRatio' 'ratio' '1e308' '422' 'refused' 'locale' 'non-numeric' \
         'negative' 'just under' 'just over' 'advanced.js' 'index.html' 'npm test' 'test:print' 'test:xlsx' 'quote-engine.test.mjs' 'pdftotext' \
         'pdftoppm' 'pdffonts' 'workbook' 'AUD' 'USD' 'CAD' 'linuxFxVersion' 'AZ-PRE-READ' 'double-press' 'G20-F1' 'G20-F2' 'G20-F6' 'G20-F7' \
         'G20-M2' 'Reset form' 'Advanced off' 'C-05' 'reopen' 'key by key' 'rounding' 'STRESS' 'RECIPIENT' 'simple session' 'rollback' \
         'node strip.js' 'node --check' 'Claude in Chrome' 'HPAM word' 'PROVISIONAL' 'ONE browser at a time' 'docker' '.invalid' \
         'NO EMAIL TO ANY HUMAN ADDRESS' 'CodeQL' 'never dismiss' 'closure table' 'G21-F1'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks '$T'" >&2; exit 78; }
  printf '%s\n' "$PROMPT" | grep -qiF -- "$T" || { echo "REFUSING: prompt lacks '$T'" >&2; exit 78; }
done

# 45N — no docker in this gate: the brief and the prompt say so; nothing here runs docker.
grep -qF 'NO DOCKER' "$BRIEF" && grep -qF 'No `docker` at all' "$BRIEF" || { echo "REFUSING: the brief does not forbid docker (NO DOCKER / No \`docker\` at all)" >&2; exit 45; }
case "$PROMPT" in *"NO DOCKER"*) ;; *) echo "REFUSING: the prompt does not forbid docker" >&2; exit 45 ;; esac

# 13 / 14 / 15 / 20 / 70 — directive, brief path, placeholders, verdict route, key path, question route, safety line.
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
case "$PROMPT" in *"$READY"*) ;; *) echo "REFUSING: prompt must name the builder's round-2 mail path" >&2; exit 14 ;; esac
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
WORDS="merge-tree NOT%TESTED env%-i bash 437ab4b 3a3399e 7b952f6 work-g21 FOREGROUND MEASURED%AT%RUNTIME PROBED READ%ONLY start%/%mid%/%end CI VOID node%--check"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## Charter' '^## RULED BY KAM, AND SETTLED' '^## PRIOR ROUND' '^PRIOR ROUND: ' 'ITS REPORT IS ON DISK AT:' '^## PIN' \
         '^## WRONG OR UNVERIFIABLE' '^## THE READY' '^## 2a. LEGITIMATE SHAPES' '^## N1. ' '^## N2. ' '^## N3. ' '^## N4. ' '^## N5. ' '^## N6. ' \
         '^## N7. ' '^## N8. ' '^## N9. ' '^## N10. ' '^## N11. ' '^## 12. The merge' '^## 13. FLOOR' '^### HELD' '^## THE MODEL RULE' \
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
for T in 'EXCLUSIVE' 'work-g21'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the tree-exclusivity rule '$T'" >&2; exit 61; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the tree-exclusivity rule '$T'" >&2; exit 61 ;; esac
done
for T in '4848' '8080' '47787' 'env -i' 'AGENTMAIL_API_KEY' 'AGENTMAIL_INBOX' 'no jest lock' 'TABLES_CONNECTION_STRING' 'HPAM_WORD' 'ADVANCED_UNLOCK_SECRET' \
         'SESSION_SECRET' 'SALES_COPY_EMAIL' 'PUPPETEER_EXECUTABLE_PATH' 'GoogleUpdater' 'chrome_crashpad_handler' 'net-log' 'GH_TOKEN'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the QuickQuote floor rule '$T'" >&2; exit 62; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the QuickQuote floor rule '$T'" >&2; exit 62 ;; esac
done
for T in 'NEVER the live' 'hpas-quickquote' 'hpas-quickquote-rg' 'datasec-sales-portal.azurewebsites.net' 'datasec-sales-portal-rg' 'no app-setting change' 'no publish' 'press nothing'; do
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
[ -x "$CHROME_BIN" ] || { echo "REFUSING: no local Google Chrome at $CHROME_BIN — §N2/§N3/§N6/§N11 would be NOT RUN" >&2; exit 44; }
for T in 'pdftotext' 'pdftoppm' 'pdfinfo' 'pdffonts' 'patch'; do command -v "$T" >/dev/null 2>&1 || echo "NOTE: $T is not on PATH — §N4 / P12 need it" >&2; done
LOAD1="$(sysctl -n vm.loadavg 2>/dev/null | awk '{print $2}')"
case "$LOAD1" in ''|*[!0-9.]*) ;; *) awk -v l="$LOAD1" 'BEGIN{exit !(l>40)}' && echo "NOTE: 1-minute load is $LOAD1 (drafting read 7.48) — browser cells will be slow; Tuesday decides whether to launch now" >&2 ;; esac

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

# 86 — no live gate-21 session already exists.
for P in $(pane_pid_of "$ROUTE_NAME"); do
  if [ -n "$(claude_under "$P")" ]; then echo "REFUSING: a pane named $ROUTE_NAME (pid $P) already runs a claude — gate 21 is live; do not start a second session" >&2; exit 86; fi
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
  *linuxFxVersion*) case "$AZPRE" in *437ab4b*) ;; *) echo "NOTE: AZ-PRE-READ does not name 437ab4b (the drafter expected v0.6.4-tool2.36-437ab4b) — live is not main; read §N8.3 before launch" >&2 ;; esac ;;
  *) echo "REFUSING: AZ-PRE-READ does not name linuxFxVersion: '$AZPRE'" >&2; exit 47 ;;
esac

# 48 — N4-METHOD (decision D5).
L7="$(sed -n 's/^N4-METHOD: \([A-Z-]*\)[[:space:]]*$/\1/p' "$BRIEF" | head -1)"
case "$L7" in
  FULL-TEXT|FIGURES) ;;
  "$PH_DECIDE") pend 48 "the brief's N4-METHOD line is still ${PH_DECIDE} — Tuesday sets FULL-TEXT or FIGURES (decision D5) before launch" ;;
  *) echo "REFUSING: the brief's N4-METHOD line reads '${L7:-<missing>}' — it must be exactly FULL-TEXT or FIGURES" >&2; exit 48 ;;
esac

# 41 — the answer route exists (Tuesday adds 'QA/Vision-gate21|tuesday-agent@agentmail.to|no' at stamp; this launcher never writes it).
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" \
  || pend 41 "no '${ROUTE_NAME}|tuesday-agent@agentmail.to|…' line in $ROUTING — answers to the gate would have no route. Add it (pattern: the QA/Vision-gate20 line) before launch, and stamp the brief's ROUTING-LINE."

# 32 — the coordinator stamps the self-check (line AND note), AZ-PRE-READ, D4-D5, the ROUTING-LINE and every @STAMP@.
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF" \
   || ! grep -q '^ROUTING-LINE: QA/Vision-gate21' "$BRIEF"; then
  pend 32 "the brief still carries $(grep -cF "$PH_STAMP" "$BRIEF") ${PH_STAMP} placeholder(s) (Self-check line and note, AZ-PRE-READ, ROUTING-LINE, the RULED lines of D4-D5) — the coordinator re-reads end-to-end and stamps all of them before launch (ROUTING-LINE must begin 'QA/Vision-gate21')"
fi

if [ -n "$PENDING" ]; then
  echo "guards pass (MODEL 40 6 9 7 8 18 22 23 74 63 31 39 10 17 12 78 45N 13 14 15 20 70 82 19 24 53 60 61 62 64 69 75 44 38R 86 46); coordinator to-do pending (47 48 41 32 as listed above); exiting $PENDING." >&2
  echo "  origin re-read $PIN_TS: main ${MAINH:0:7}, QQEP $H7, refs/pull/10/head $H7; model $MODEL; GH-API-LEG $GHLEG" >&2
  echo "  NEG seats (38R, derived live):$NEG_DESC" >&2
  exit "$PENDING"
fi

PIN_BLOCK="$(printf 'PINNED HEADS — verified by the launcher at %s (cat-file; base 437ab4b, 0 behind; ancestor and merge-base with MAIN; not-already-on-main; commit count 6; chain 437ab4b <- 0fc280b <- a8d769b <- 7b952f6 <- a7e1835 <- 1f7db41 <- 3a3399e by single parents; round 1 7b952f6 an ancestor; head tree ec15fb2; round-1 tree 25ddfb8; main tree c71780c; main pinned EXACTLY; refs/pull/10/head = head; the 8-file delta and numstat whole, round 2 and per round-2 commit; the test:print line; blobs at base / round 1 / head; Kam'"'"'s retired W1/W2 present at base strip.js and absent at the head by sha256; git ls-remote origin for both rows):\n' "$PIN_TS"
  printf '%s\n' "$PIN" | awk -F'\t' '{ printf "  %-7s %-11s %-42s %s  base %s  commits %s\n", $1, $2, $3, $4, ($5=="-"?"-":substr($5,1,12)), $6 }'
  printf '  Round 1 (gate 20, NO GO): 7b952f6edbcc3b271e4a650685f47b87760ed8f0. Main: pinned %s (exact; a move refuses). PR #%s: refs/pull/%s/head = %s; refs/pull/%s/merge = %s (GitHub test merge)\n' "${MAINH:0:12}" "$PR_NUM" "$PR_NUM" "${HQ:0:12}" "$PR_NUM" "${PR_MERGE_NOW:-<absent>}"
  printf 'GH-API-LEG, as set in the brief: %s\n' "$GHLEG"
  printf 'AZ-READ-LEG, as set in the brief: %s (you run no az)\n' "$AZLEG"
  printf 'AZ-PRE-READ, as stamped by Tuesday: %s\n' "$AZPRE"
  printf 'N4-METHOD, as stamped by Tuesday (D5): %s\n' "$L7"
  printf 'NEGATIVE-CONTROL SEATS, derived live by the launcher from the cockpit panes at %s:%s Re-read them at start.' "$PIN_TS" "$NEG_DESC")"

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  printf '%s\n' "$PIN_BLOCK"
  echo "  model: $MODEL at exec (from models_latest.json); --check started no claude; nothing written."
  exit 0
fi

# 11 — no inherited identity: AZURE_CONFIG_DIR always EMPTY (no az in this gate); GH_CONFIG_DIR EMPTY unless GH-API-LEG = READ-ONLY-VISION-TOKEN.
ID_TMP="$(mktemp -d "${TMPDIR:-/tmp}/qa-vision-gate21-id.XXXXXX")" || { echo "REFUSING: cannot create the empty identity dir" >&2; exit 11; }
mkdir -p "$ID_TMP/azure-empty" "$ID_TMP/gh-empty" "$ID_TMP/bin" || { echo "REFUSING: cannot create the identity dirs under $ID_TMP" >&2; exit 11; }
{ [ -z "$(ls -A "$ID_TMP/azure-empty")" ] && [ -z "$(ls -A "$ID_TMP/gh-empty")" ]; } || { echo "REFUSING: the identity dirs under $ID_TMP are not empty" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_TMP/azure-empty"
export GH_CONFIG_DIR="$ID_TMP/gh-empty"
if [ "$GHLEG" = "READ-ONLY-VISION-TOKEN" ]; then
  QA_REAL_GH="$(command -v gh)" || { echo "REFUSING: gh vanished between guard 46 and launch" >&2; exit 11; }
  export QA_REAL_GH
  cat > "$ID_TMP/bin/gh" <<'SHIM'
#!/bin/bash
# gate-21 GET-only gh shim (written by launch_qa_vision_qq_gate21.sh; GH-API-LEG = READ-ONLY-VISION-TOKEN). Brief §HELD binds the rest.
REAL="${QA_REAL_GH:?gh shim: QA_REAL_GH unset}"
[ "${1:-}" = "api" ] || { echo "gh shim: only 'gh api' GET reads are allowed in Vision gate 21 (got: ${1:-<none>})" >&2; exit 64; }
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
