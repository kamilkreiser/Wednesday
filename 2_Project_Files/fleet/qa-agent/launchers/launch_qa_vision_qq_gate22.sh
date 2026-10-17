#!/bin/bash
# launch_qa_vision_qq_gate22.sh — cross-project QA agent, ONE gate (Vision gate 22; drafted 2026-10-17 ~11:33-12:1x AEDT by a read-only drafting
# agent for Tuesday, from launch_qa_vision_qq_gate21.sh).
# Datasec/Vision_Sales_Portal, QuickQuote repo: ONE target, TIER 1 (quote output to customers), ONE verdict:
#   QQEP  fix/qq-email-matches-print-2026-10-16  PR #10 @ f31720e  ROUND 3 (Kam 09:45:48; no round 4 without him): held price re-checked, one-cent floor; v2.39
#
# Main is 437ab4b = LIVE v0.6.4-tool2.36-437ab4b. Round 1 (gate 20) = 7b952f6, NO GO on G20-F1. Round 2 (gate 21) = 3a3399e, NO GO on G21-F1.
# QQEP = SEVEN commits in a straight line: 437ab4b <- 0fc280b <- a8d769b <- 7b952f6 <- a7e1835 <- 1f7db41 <- 3a3399e <- f31720e. 7 ahead, 0 behind.
# THIS GATE PINS MAIN EXACTLY: a moved main REFUSES (PR #8 merging first would move it). refs/pull/10/head must equal the head.
#
# THE HEADS LIVE IN ONE PLACE: the brief's PIN-HEADS table. This launcher PARSES it, refuses any placeholder, verifies every row against the
# object store and against origin by `git ls-remote` NOW, and appends the verified table to the agent's prompt.
#
# Every path is on /Volumes/Laptop-DEV (gate 21's report and instruments are here too). The T9 QuickQuote repo is STALE and is never read.
#
# PRODUCTION IS LIVE for this project (hpas-quickquote / hpasqqacr; datasec-sales-portal-rg). This gate runs NO docker and NO az. Findings only.
# The live check is Kam's (Tuesday 2026-10-16 15:07: "do NOT read HPAM_WORD; live check 2b moves to Kam").
#
# GUARDS — gate 21's numbering kept where the guard survives; changes:
#   - PIN: two rows (MAIN-Q 437ab4b, QQEP f31720e base 437ab4b x7). Exact chain pin (seven single parents); R1 7b952f6 and R2 3a3399e ancestors;
#         head tree pin.
#   - 22/23: file set 8 + numstat whole, round 3 (3a3399e..head: index.html, pdf.js, the bounds test only), round 2 and per round-2 commit;
#         package.json's ONLY change over main is still the test:print line (its blob is unchanged since round 2).
#   - 74: blobs (8 changed base->head, R2 blobs, the unchanged list incl. lockfile, Dockerfile, xlsx/mail/store); server.js and strip.js unchanged
#         since round 2; W1/W2 ABSENT at the head and PRESENT at base (by sha256); round-3 anchors present (customPriceMinPerMonth 0.01, cpModeWanted,
#         cpSyncFrom(sourceId, committed), the inputType predicate, the re-check, the snap, cpMax, the new sentences, toolVersion 2.39, pdf.js judging
#         only when wantsCustom, the bounds file's new REFUSAL and its synthetic paste) and absent at R2.
#   - 31: the builder's round-3 mail (lines 1-124 of Tuesday's batch) on disk, pinned by sha256; it DOES carry a NOT TESTED block (brief WRONG (a))
#         and no NexusAI text; gate 21's report on disk with its NO GO at 3a3399e and G21-F1..F8.
#   - 45N: the prompt and brief forbid docker; no docker command is run here at all.
#   - 46: GH-API-LEG must read READ-ONLY-VISION-TOKEN or NOT-RUN.
#   - 47: AZ-READ-LEG must read TUESDAY-READS; AZ-PRE-READ must be stamped and name linuxFxVersion (pending guard).
#   - 48: N4-METHOD (D5) = FULL-TEXT | FIGURES (pending guard while TUESDAY-DECIDES).
#   - 41: the routing line QA/Vision-gate22 in inbox_routing.conf (pending guard); 32 also counts the brief's ROUTING-LINE stamp.
#   - 86: no live QA/Vision-gate22 pane already.
#   - 47 48 41 32 are the coordinator's to-do guards: run LAST, reported TOGETHER, exit with the first pending code.
#
# LAUNCH IT IN A TMUX PANE:
#   /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add 'QA/Vision-gate22' "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_vision_qq_gate22.sh'"
#   NEVER nohup, never bare from a seat's shell.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# --check is READ-ONLY: git read verbs (cat-file, rev-parse, merge-base, log, rev-list, diff, show, ls-tree, ls-remote); tmux list-panes; ps;
# grep/python/shasum over files. It creates no identity dir, writes nothing and starts no claude.
# Usage: launch_qa_vision_qq_gate22.sh [--check]
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
BRIEF="$BRIEFS/2026-10-17_vision-gate22-qq-pr10-r3.md"
READY="$BRIEFS/2026-10-17_vision-qq-pr10-r3-READY-mail.txt"
READY_SHA='076c5afc0009aab58a823eed6335b9e62a6f9dfbd7d0e1a807e31b297db8fd39'
CHARTER="$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"
MODELS_JSON="$TUE/0_Brain/dashboard/data/models_latest.json"
MODEL_PIN='claude-opus-5-5'
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
VSP='/Volumes/Laptop-DEV/!CODING/Datasec/Vision_Sales_Portal'
Q_REPO="$VSP/Quoting Tool/hpas-quoting-tool"
VSP_GH="$VSP/4_Credentials/.gh-config"
CLAR="$VSP/1_Project_Definition/CLARIFICATIONS.md"
REPORTS="$QA_DIR/projects/vision/reports"
G21_DIR="$REPORTS/2026-10-17-vision-gate21-qq-pr10-r2"
G21_REPORT="$G21_DIR/report.md"
G21_TOOLS="$G21_DIR/evidence/tools"
REPORT="$REPORTS/2026-10-17-vision-gate22-qq-pr10-r3/report.md"
ROUTE_NAME='QA/Vision-gate22'
BUILDER_PANE='Datasec/Vision_Sales_Portal'
CHROME_BIN='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
PR_NUM='10'
PR_MERGE_SEEN='75d7a8e936daf937536f6a32fb6284bb8e8e04b9'     # refs/pull/10/merge at 11:33:28 (GitHub's test merge; NOTE only)
ANCHOR_MAIN='437ab4bc412bc74d8da3b66a6ac5c71d7335c5d6'     # QuickQuote main = LIVE v0.6.4-tool2.36-437ab4b
ANCHOR_MAINP='9d1c5ab8bc89aa2ba6b0063c22a858955d05a3e7 818a019ea21c39c5ef0a228f6242e7bdbb072761'
ANCHOR_PREGUARD='e4ce5367761e03db982189a3f21758aa06714a85'  # main before the guard
C1='0fc280b54aeab52c020692ed51fd018b20124eee'
C2='a8d769bbdea3d282c3b73ace336d09d4e18c9a0e'
R1='7b952f6edbcc3b271e4a650685f47b87760ed8f0'               # round 1's head = gate 20's NO GO
C4='a7e1835872b7ffd555608d263bc087dbeb4af02c'
C5='1f7db41a3215461adcda0a9e4c06b6b43507eece'
R2='3a3399e947bf5faf8a8e0c0d3e11956c6590db98'               # round 2's head = gate 21's NO GO
BACKLOG_F8='815aae76d842e5ce5bb5ca38de4b7770ab790c9f'       # G20-F8's ticket (parent of BACKLOG_R3; NOT on the PR)
BACKLOG_R3='01c8d7f9c4d819146e48185d824ecb304a6c9619'       # G21-F3 + the route bypass ticket (backlog branch tip at drafting; NOT on the PR)
HQ_EXPECT='f31720ee677dbe2deb53dcb7991f1683a1b03ce1'
HQ_TREE='ee51fa7328b6cddaccc5e85593fd1443f150e411'
R2_TREE='ec15fb204fa872917c9adcb3e2f819107bbf0a5e'
R1_TREE='25ddfb889661bde728906d0a2db7d32b148b21e8'
MAIN_TREE='c71780c82ea9cc338181163cb9d6045e07595e4f'
DELTA_FILES='index.html stage3/lib/pdf.js stage3/package.json stage3/server.js stage3/strip.js stage3/test/custom-price-bounds.mjs stage3/test/email-matches-print.mjs stage3/test/email-print-mode.mjs'
NUMSTAT_EXPECT='199/36/index.html 55/13/stage3/lib/pdf.js 1/1/stage3/package.json 9/0/stage3/server.js 25/26/stage3/strip.js 465/0/stage3/test/custom-price-bounds.mjs 165/0/stage3/test/email-matches-print.mjs 23/49/stage3/test/email-print-mode.mjs '
NUMSTAT_R3='108/30/index.html 6/2/stage3/lib/pdf.js 200/3/stage3/test/custom-price-bounds.mjs '
NUMSTAT_R2='62/13/index.html 20/5/stage3/lib/pdf.js 1/1/stage3/package.json 9/0/stage3/server.js 14/0/stage3/strip.js 268/0/stage3/test/custom-price-bounds.mjs 28/12/stage3/test/email-matches-print.mjs '
NUMSTAT_C4='60/13/index.html 20/5/stage3/lib/pdf.js 1/1/stage3/package.json 9/0/stage3/server.js 14/0/stage3/strip.js 268/0/stage3/test/custom-price-bounds.mjs '
NUMSTAT_C5='28/12/stage3/test/email-matches-print.mjs '
NUMSTAT_C6='2/0/index.html '
W1_SHA='0d5beedb47709eed6c7c6eec5d8ced3e73c58069ea09f49f4495cde1abeb25b9'
W2_SHA='4c73c1593e64f73dc84d24c48a69896307108d387b70a9318b0d7f7dd3ec797d'
# Kam's RETIRED words (U+201C/U+201D around Standard pricing only). Checked by sha256; used here only to prove they are GONE at the head.
W1='This email sends standard pricing only. Your custom pricing is on the printable quote, but it will not be in the email. Choose “Standard pricing only” above, or press the button again to send standard pricing anyway.'
W2='Send standard pricing anyway'

SUBJECT_STEM='[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 22'
QUESTION_SUBJ='[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>'
ANSWER_PREFIX='[Tuesday -> QA/Vision-gate22] ANSWER'
STATUS_SUBJ='[QA/Datasec-Vision -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch'
PARK_LINE='PARKED: flagged — awaiting the Opus 4.8 switch'

q() { git --no-optional-locks -C "$Q_REPO" "$@"; }
sha256s() { printf '%s' "$1" | shasum -a 256 | awk '{print $1}'; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE gate (Vision gate 22) on Datasec/Vision_Sales_Portal, in the QUICKQUOTE repo: ONE target, TIER 1 (quote output to customers: the email must equal the print), ONE verdict, GO / GO WITH FINDINGS / NO GO. QuickQuote main is 437ab4b and it is what is LIVE (v0.6.4-tool2.36-437ab4b; the brief's AZ-PRE-READ, appended below, is Tuesday's reading). The target QQEP (TIER 1; ROUND 3 of PR #10, authorised by Kam on the live board 2026-10-17 09:45:48, card quickquote-pr10-r2-publish-hold-1017 = a: "Hold, and allow a round 3 fix", "then one more test gate. You decide the publish after that, on its own card"; there is no round 4 without Kam) is QuickQuote PR #10, branch fix/qq-email-matches-print-2026-10-16 at f31720e, SEVEN commits over 437ab4b. Round 1 was 7b952f6 (gate 20, NO GO on G20-F1, a pasted 1e308 emailed "A$∞"). Round 2 was 3a3399e (gate 21, NO GO): G21-F1, a stale in-bound custom price behind a STANDARD quote got the standard email refused (422) once the app selection shrank; G21-F2, a sub-cent price emailed a Custom Quote at A$0.00/device/month; plus G21-F3..F8. Round 3 is ONE commit, f31720e (v2.39): the page re-checks a held price in renderCustom whenever the standard price moves and CLEARS it with the sentence before any press; the renderer restores and judges pdmUSD ONLY when the posted print mode is custom or both; a floor CONFIG.customPriceMinPerMonth = 0.01 of the quote's currency (so it moves with the exchange rate; the ceiling, CONFIG.customPriceMaxRatio = 10 times the standard price, does not); a cleared or non-number entry is said; keystrokes through empty or a too-low figure are quiet and judged on change, judged by the input event's inputType (a paste, a drop or an event with no inputType counts as committed), while too high is said at once; the rep's chosen custom mode (cpModeWanted) comes back with a valid price; a field's shown figure for a bound is snapped to that bound. Kam's ONE publish card is built from your §N10 closure table (CLOSED / OPEN / NEW per instance, with evidence). Publishing fix (2) needs Kam's own word (C-20, card quickquote-email-sends-standard-not-custom-1016 = a: "Kam's grant covers the GUARD only"), never yours. Round 3 touches index.html, the renderer lib/pdf.js and the bounds test file only; the hosted server module, strip.js, package.json, the lockfile, the Dockerfile and lib/xlsx.js, lib/mail.js, lib/store.js are byte-identical at round 2 and head. This machine is Kam's Mac mini, working volume /Volumes/Laptop-DEV; gate 21's report and instruments are on this drive; the T9 QuickQuote repo is STALE, never read it.

RULINGS CHECKED AS BUILT, NOT RE-OPENED: Tuesday's G20-F1 fix-shape ("bound the custom price both where it is set and where it is rendered … a non-finite or out-of-bound pdmUSD is refused with a message, never rendered") and gate 21's stamp: a refused STANDARD email for a state a rep reaches through the page's own controls is a FAIL, and a Custom Quote at 0.00/device/month is G20-F1's own class. The Custom pricing note stays OFF the emailed PDF and ON the print (Tuesday 2026-10-16 ~14:02; reversible by Kam); Kam's two guard sentences W1/W2 are RETIRED and must appear NOWHERE (W1 begins "This email sends standard pricing only."; W2 is "Send standard pricing anyway"). PRE-EXISTING FACT: the print CSS .q-savings { display:none } (5ef2a60, since v1.88) hides the notes on paper; you REPORT the note per mode, you do not grade it. The access word is not your subject: never read, print, grep for, type or reproduce the access word or the offline page's constant; the ADVANCED SEAM of the head's index.html is lines 3816-3827: never print or grep it.

READ YOUR COMMISSION FIRST, whole: /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-17_vision-gate22-qq-pr10-r3.md
Then read the charter it names, the Vision CLARIFICATIONS (C-01..C-20; C-20 is Kam's ruling), the project's CLAUDE.md (/Volumes/Laptop-DEV/!CODING/Datasec/Vision_Sales_Portal/CLAUDE.md, its QuickQuote section; its deploy commands are not for you), the QuickQuote repo's own CLAUDE.md at the head (git show; its publish lines are not for you), the builder's round-3 READY mail, read WHOLE (/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-17_vision-qq-pr10-r3-READY-mail.txt; it DOES carry a NOT TESTED block, and two of its lines, the spinner arrows and the floor moving with a landed rate, are yours to drive), and gate 21's report, read WHOLE: /Volumes/Laptop-DEV/!CODING/Testing Agent MAIN/projects/vision/reports/2026-10-17-vision-gate21-qq-pr10-r2 (NO GO on 3a3399e; G21-F1..F8, O1-O3, S1-S4 are the reference; its evidence/tools/ holds the instruments you copy; its evidence/mail/verdict-body.txt is the verdict as mailed). Every builder statement is a CLAIM, never evidence. RE-DERIVE every red, every mutant, every suite set, every browser result and every comparison yourself. Verify every PRIOR WORK claim against git history, never against the brief. The brief's WRONG list, MODEL RULE and TUESDAY'S RULINGS (R1-R8 and the stamped D4-D5) are stamped: apply them, do not re-rule them.

WHAT THE BRIEF REQUIRES, in short (the brief is the authority):
(1) THE DIFF against the READY's claims: the whole delta 437ab4b..f31720e and the round-3 delta 3a3399e..f31720e hunk by hunk; one bound (cpCheck) now in four places (the fields, Apply %, the renderCustom re-check, the renderer through cpRestore only when the mode wants it); what each bound's denominator depends on; every path to render() and so to the re-check, the renderer page included; the PR files API equal to git diff --numstat; what node strip.js generates at base, round 2 and head, every line mapped; cpCheck, cpRestore, cpModeWanted and the refusal box never in the stripped public page.
(2) THE RED-PROOFS AND MUTANTS: the head's custom-price-bounds.mjs (blob b3c5345) on a fresh 3a3399e tree UNMODIFIED and with only its REFUSAL line set back to round 2's sentence (the builder's own method), and on 437ab4b; tamper asserted landed; node --check rc 0 (a file that does not parse is VOID); quote every failing assertion and classify it DEFECT-REASON, NEW-SURFACE-ABSENT or WORDING; all three new/changed test files (custom-price-bounds.mjs, email-matches-print.mjs, email-print-mode.mjs) pass at f31720e, 3 runs each, timings with the load. The builder's mutants A-I re-derived (I, the 1e-9 tolerance, survives its cells: arm it in the browser too and say whether it matters), the new mutants G22-M1..M6, and gate 21's arms where they still land; say which cells see each, or NONE.
(3) A REAL-BROWSER DRIVE THROUGH THE REAL SERVER PATH, gate 21's whole matrix kept: your harness runs the tree's hosted server module's createApp() export in-process (never its entry point) with the repo's in-memory store pattern, a CAPTURING stub mail, a salesCopy option on a .invalid domain, throwaway session and unlock secrets (never a real secret, never the HPAM word), the tree's own renderQuotePdf, a frozen clock, on 127.0.0.1 and a kernel port. RE-TEACH THE PASTE: gate 21's paste was CDP Input.insertText, which Chrome reports as inputType insertText, a KEYSTROKE to round 3; the builder's own paste is a synthetic event; so every PASTE row here is a REAL clipboard paste whose recorded inputType must be insertFromPaste, else that row is VOID, and insertText is reported separately as TYPED-WHOLE (the dictation class). Record every inputType the page received. ONE Google Chrome through your egress-block wrapper signs in with the captured OTP, unlocks advanced through the page's own controls, fills the form as a rep, sets a custom price, picks each print mode by its label, captures the page's own Generate output as a PDF in print media A4, and presses the page's own Email button ONCE. THE REQUIRED GRID at head, at base AND at round 2: advanced x "Standard pricing only" / "Custom pricing only" / "Standard + custom" x AUD / USD / CAD, plus simple sessions and advanced-standard-no-price x AUD / USD / CAD. PROBES P1-P15 as gate 21 plus P3'' (Advanced off, fewer apps, Advanced on again): the double-press, Reset form and Advanced off, C-05 reopen, currency changes, every custom-price field key by key, by real paste, typed-whole and by spinner, the 2,500-device 5-year STRESS state, the 1e308 paste by both routes, canned live FX rates inside the drive Chrome (and a lower one), crafted bodies in each print mode to YOUR loopback server only, mixed versions (a v2.36 tab after a v2.39 publish; the head page on the base server, i.e. a rollback), the lone revert of a8d769b in YOUR tree only, no stale W1/W2, light and dark at 1280 / 375 / 320 px with each sentence showing, and a refused send end to end.
(4) WHAT THE RECIPIENT GETS vs WHAT THE REP PRINTED, per the brief's N4-METHOD (appended below): pdftotext -layout full text with ONLY the quote number normalised, the money-figure multiset, pdfinfo pages and A4, pdffonts, pdftoppm -r 100 pixels per page in plain python (no ImageMagick, PIL or numpy) with the bbox of every differing region; the workbook part by part; an ∞ / Infinity / NaN / undefined scan and a 0.00-per-device scan on every PDF and workbook. Controls that can fail first (a planted one-word, one-digit and one-pixel change; a planted A$∞ and a planted A$0.00 / device / month; the base defect pair; AUD vs CAD). The note table per mode. The captured mail's to, bcc, subject and text; a refused or cleared state reaches nobody.
(5) SIMPLE SESSIONS AND STANDARD EMAILS UNCHANGED vs MAIN but for v2.36 -> v2.39, pixels only inside those lines, the posted body only by the custom key; a standard email with a price posted identical to one without; the OFFLINE index.html opened as a file prints the same as main's in each mode x AUD/USD/CAD and clears or refuses as the page does; AND every head grid cell's email equal to round 2's but for v2.38 -> v2.39.
(6) THE CI SUITES as CI runs them, at f31720e, 3a3399e and 437ab4b, as SETS, NOT COUNTS: root node --test quote-engine.test.mjs; in stage3/: npm test, npm run test:print (added over round 2 exactly the 17 new custom-price-bounds names), npm run test:xlsx. npm ci --offline --ignore-scripts only, the lockfile proven entry by entry (lockcmp.py AND lockwalk.py), npm ls --all. Host Node is 26.8.1, not CI's 22: say so. test:azurite is READ from CI (no docker).
(7) THE GENERATED FILES: cpExport/cpRestore/cpCheck/cpModeWanted and the refusal box only in private/advanced.js, never in the stripped public/index.html; no guard text in any generated file; the offline page's cpRestore refuses 1e308 and 0.004/1.55 and takes the one-cent floor.
(8) NOTHING PUSHED, MERGED OR PUBLISHED, AND THE PUBLISH FACTS: your command log proves no push, merge, docker, az, GitHub write or request to the live site; the live webapp's linuxFxVersion is RELAYED from the brief's AZ-PRE-READ (Tuesday re-reads at verdict); what a publish of f31720e would ship (the live tag's sha .. f31720e, the hosted server module included), READ ONLY; rollback to v2.36 with G20-F3, G20-F4 and G21-F6 as measured; the custom note per mode; the NEW WORDS FOR KAM verified verbatim at source with file:line at the pinned head AND as the page rendered them per currency; the floor and ceiling numbers; deploy-on-merge READ ONLY.
(9) CI AND CODEQL on PR #10 at f31720e, READ ONLY, by GH-API-LEG: runs 38986121215 and 38986126280 and their jobs, the print-fit log lines, the check runs, the dynamic CodeQL run 38986121428, code-scanning open on main and on the PR ref; the PR-side CodeQL zeros are a blind instrument: say only what they can show; never dismiss an alert.
(10) ROUND-2 FINDINGS RE-TESTED, EACH A CHECK THAT CAN FAIL: G21-F1 (B-STATE in every print mode x AUD/USD/CAD and offline, P3', the crafted stale price, the transitional clear, the floor moving with FX) and G21-F2 (0.004, 0.001, 0.0001 /day and -99.99 % by every entry route, in every currency, offline too; the one-cent edge; the snap); G21-F4, G21-F5, G21-F7 and G21-F8; G21-F3's ticket 01c8d7f verified and re-measured; G21-F6 re-measured for the card; gate 21's CLOSED rows (G20-F1 instances, G20-F2, G20-F6, G20-F7) re-run and still closed. Each closure needs a red at 3a3399e (or base) from YOUR run and a green at f31720e; a check green on both sides is VOID for closure. Output the closure table: CLOSED / OPEN / NEW per instance.
(11) THE RANGE AT ITS EDGES: the ceiling at, over and by the shown per-day figure; the floor at, under and snapped; zero, negatives, non-numbers and locale strings by the routes Chrome allows; keystroke-versus-committed judging and what the next press sends; the spinner arrows, keyboard arrows and the wheel; the held price cleared on a standard-price change (B-STATE, B-TRANS); the remembered custom mode coming back unasked; the floor across currency changes and canned live rates; mutant I armed in the browser; crafted bodies in each print mode — each on screen, print/PDF, email, workbook and offline; and THE NUMBERS for Kam in one line.
GH-API-LEG (appended below by the launcher as the brief sets it): READ-ONLY-VISION-TOKEN means gh is on your PATH as a GET-only shim over Vision's gh config — gh api GET reads only, never -X/--method, -f/-F/--field/--raw-field/--input or graphql, never a comment, review, label, approval, re-run or dismissal; NOT-RUN means none. AZ-READ-LEG is TUESDAY-READS: you run no az at all. Never open any file under the project's 4_Credentials.

PRODUCTION IS LIVE for this project. NEVER the live QuickQuote (hpas-quickquote, hpas-quickquote-rg, hpasqqacr, its Table Storage, its log workspace) and NEVER the live portal (datasec-sales-portal.azurewebsites.net, datasec-sales-portal-rg): no HTTP request, not even a GET; press nothing there. The live check is Kam's: never read, ask for or type the HPAM word. No az; no deploy, no publish, no app-setting change, no ACR build, no registry push. Never the FX hosts (blocked by your wrapper, in the drive Chrome and in the renderer's Chrome; the canned rates are answered inside the drive Chrome), never ntfy.sh. Never Claude in Chrome (Kam's own Chrome with his sign-ins). The clipboard permission you grant is for your own loopback origin only. NO EMAIL TO ANY HUMAN ADDRESS: every send goes to your capturing stub mail on .invalid addresses; your own AgentMail calls go only to tuesday-agent@agentmail.to. NO DOCKER: not a build, not a run, not even docker images or docker ps; never touch work-g18, work-g19, work-g20, work-g21 or any qa-g18-* object. NETWORK, and only this: git ls-remote origin; gh api GETs if GH-API-LEG allows; your AgentMail calls. No npm registry (npm ci --offline), no npm audit.

ONE BROWSER AT A TIME: never two drive Chromes of yours alive at once (a suite's own Chromes count); never a suite and a browser drive concurrently; one retry per cell at most, then NOT RUN with the load.

HELD: no merge, no push, no publish, no comment or status on PR #10 or PR #8, no alert dismissal, no mail to any human. TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT on this drive from the object store (git archive into a fresh mktemp -d under projects/vision/work-g22/ in /Volumes/Laptop-DEV/!CODING/Testing Agent MAIN). Each tree is EXCLUSIVE to this gate and to one purpose; never touch any other work directory. The builder's checkout is LIVE: never read any working tree as evidence; never use the name main in the repo, only the pinned 40-hex shas. Copy gate 21's instruments into YOUR evidence/tools and re-point them (they hard-code work-g21, the gate-21 report folder, @qa-g21.invalid and v2.38); never run from, edit or write into gate 1-21's copies. Never npm install, never npm audit fix, never npx anything not already in the tree. In the repo use ONLY read verbs (show, log, diff, ls-remote, rev-parse, ls-tree, cat-file, grep, merge-base, archive); never fetch, pull, checkout, switch, worktree, commit, stash, reset, clean, gc, branch, revert or for-each-ref; the lone-revert probe patches YOUR extracted tree with patch, never the repo. Run git merge-tree --write-tree only from the gate's OWN object dir, or skip it and say so. Findings-only: no writes in the QuickQuote repo, none inside Vision_Sales_Portal, none in gate 1-21's report folders or trees. Never rm: quarantine. Run every loop and every git show <sha>:<path> under bash. Run node strip.js before any lone browser file. A mutant's landed-check must never quote the head form it replaces (gate 21's S1/S2 VOIDs). CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY: every round-2 closure needs its red from your own run; the base column must show the emailed custom figure differing from the printed custom figure before the head's match is credited to fix (2); the PDF comparator and the scans must report a planted difference; the stale-words scan must find W1 on the base page; every paste row must show insertFromPaste; a control derived from the run it validates is not a control.

FLOOR DISCIPLINE. Vision has no jest lock; never borrow NexusAI's. Never use host ports 4848, 8080 or 47787; host processes take every port from the kernel and bind 127.0.0.1; if an instrument needs a fixed port use only 47310-47319, after an lsof check. Every host product process runs under env -i with an explicit allowlist, NODE_ENV never production. Never set AGENTMAIL_API_KEY or AGENTMAIL_INBOX in a product process (with both set, QuickQuote SENDS FOR REAL), nor any real ACS_* or MAIL_SENDER, TABLES_CONNECTION_STRING, SALES_COPY_EMAIL, HPAM_WORD, ADVANCED_UNLOCK_SECRET, SESSION_SECRET, WEBSITE_SITE_NAME, GH_TOKEN or GITHUB_TOKEN; print each product process's env KEY NAMES and assert none is forbidden. NTFY_SERVER=http://ntfy.invalid; never contact ntfy.sh. EGRESS INCLUDING CHROME CHILDREN: every Chrome runs under your copy of the egress-block wrapper as PUPPETEER_EXECUTABLE_PATH; prove the block with its positive control and run the net-log scan at the end; record GoogleUpdater and chrome_crashpad_handler at start and end; reap every Chrome and every app listener by the pid you started. Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid, at START and at END, with the negative-control seats the launcher derived (listed at the end of this prompt) classifying FOREIGN in the same run. A zero is reportable only beside an ATTACHED control that fired in the same window. Record the load average beside every timing number; a latency result with no load figure is not a measurement.
DEADLINE AND HEARTBEAT: every step has a written DEADLINE built into your runner (there is no timeout binary here) and releases its Chromes, pages, children, app servers and temp profiles in a finally. Log a HEARTBEAT line at least every 2 minutes; a step with no heartbeat for 5 minutes is aborted and reported, never waited on. Deadlines: one browser cell 120 s; one red-proof or mutant arm 420 s; the root pack 120 s; a whole npm test 300 s; a whole test:xlsx 300 s; a whole test:print 900 s; nothing above 900 s. Under the brief's D4, a red-proof, the head grid or its N4 comparison, the G21-F1 or G21-F2 pairs, or the range's at / over / floor / under / stale-state rows NOT RUN makes the verdict PROVISIONAL.

THE MODEL RULE (Kam, live board 2026-09-30 09:07, card (b)): QA gates may switch to Opus 4.8 when flagged by Opus 5.5's safeguards, PER SESSION. You start on Opus 5.5. You run the FULL rows. If one of your responses is stopped by the safeguards: that step is NOT RUN (never re-worded to slip past); write ONE line to evidence/classifier-stops.txt; reap any Chrome and app server you started; mail tuesday-agent@agentmail.to with the subject exactly "[QA/Datasec-Vision -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch"; then end your turn with the line "PARKED: flagged — awaiting the Opus 4.8 switch" and wait. Tuesday switches THIS pane's model and taps you by mail. You never answer the model dialog yourself, and nobody ever chooses "Switch automatically". After the switch, resume at the stopped row. The report states which rows ran on which model, with the switch time, and quotes classifier-stops.txt whole.

QUESTIONS: your routing name is QA/Vision-gate22. If you must ask, mail tuesday-agent@agentmail.to with the subject "[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>" and proceed on the safest reading without waiting (the one exception is a safeguards stop, which PARKS you under THE MODEL RULE). Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/Vision-gate22] ANSWER"; read it with your verdict key. Never wednesday-agent@. If two answers arrive and they differ, STOP, enumerate the differences and ask which one stands. If a response is cut off by a safety check, record it and continue with the next item; this is authorised defensive QA of Datasec's own product on loopback. Approval-class items (a publish, a deploy, the live site, money, a human) are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your report to: /Volumes/Laptop-DEV/!CODING/Testing Agent MAIN/projects/vision/reports/2026-10-17-vision-gate22-qq-pr10-r3/report.md
You create that folder. Write its VERDICT and FINDINGS table early and keep it current. Number findings G22-F1, G22-F2, …; a round-2 finding re-tested keeps its G21 id in the closure table.

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with a subject beginning exactly:
[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 22: QQEP @ <sha7> <GO | GO WITH FINDINGS | NO GO>
(the sha7 is the pinned head from the verified table below; append PROVISIONAL if the brief's D4 clause applies). Lead the body with ONE sentence as the brief's section 14 words it (round-2 findings closed by your own red/green pairs in every print mode x currency and offline; gate 21's closures still closed; the real hosted page through the real server path still emailing exactly what the rep printed on one press; the range refusing what it should and only that on every surface by every entry route; any regression round 3 added; the CI suites as sets; anything pushed, merged or published), then a line "VERDICT: <token>, round 3 (Kam-authorised; …)" with what happens next (Kam's ONE card and its default under D4), then one line each on the closure table, THE NUMBERS (the range per currency, bundle and Manager only, and how the floor moves), the stale and transitional states, the floor across FX and currency, keystroke-versus-committed, the spinner, the remembered mode, the snap, the base column, the mutants, P1, the resets, C-05 reopen, entry routes and the stress state, the FX race, the crafted bodies by mode, mixed versions and rollback, the lone revert, the note per mode, head vs round 2, the NEW WORDS FOR KAM as rendered, what a publish would ship, the live site read (RELAYED), and the class count (round 3, Kam-authorised: no round 4 without Kam). You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/Laptop-DEV/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no credentials directory of its own. Use it only in your own mail calls, with a client timeout. Never put the key or any secret in a mail, the report or a product process.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice — the only turn you end while waiting is the PARKED line of THE MODEL RULE.

Report the pinned head and main as three timestamped readings (start / mid / end), with the branch name beside each, plus refs/pull/10/head. Include a table with one row per brief section N item: MEASURED, NOT TESTED, NOT RUN or VOID, and HOW (command, tree, browser, port, load).

Rule 2 stands: what you did NOT test is first-class output. Say the READY carried a NOT TESTED block and which of its lines you drove. Write a NOT TESTED section that covers at least the published image (no docker by design), a real ACS send, the live site (Kam's check), CodeQL's verdict before the merge (blind), CI's Node 22 (read only, never caused), store-azurite (read from CI; it does not exercise "refused"), a real live FX provider in the drive Chrome or the renderer, currencies and Chrome locales you did not drive, real dictation software and IMEs, Windows, Safari, real phones, real printers and the account managers' real browsers, a customer's mail client, screen readers, Claude in Chrome (not used), PR #8 (not this gate), and every row you did not run. Label every action recommendation MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. The tester never fixes.
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
for S in "$MAINH" "$HQ" "$ANCHOR_MAIN" $ANCHOR_MAINP "$ANCHOR_PREGUARD" "$C1" "$C2" "$R1" "$C4" "$C5" "$R2" "$BACKLOG_F8" "$BACKLOG_R3"; do
  T="$(q cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in the QuickQuote repo on this drive (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 9m — MAIN: 437ab4b EXACTLY (refuse if it moved).
[ "$MAINH" = "$ANCHOR_MAIN" ] || { echo "REFUSING: the pinned MAIN ${MAINH:0:7} is not 437ab4b — this gate pins main exactly; re-brief" >&2; exit 9; }

# 7 / 8 — the target: base as briefed, ancestor AND merge-base with MAIN, not on main, exact count, 0 behind; R1 and R2 ancestors.
H7="${HQ:0:7}"; BASE="$(fld QQEP 5)"; N="$(fld QQEP 6)"
[ "$BASE" = "$ANCHOR_MAIN" ] || { echo "REFUSING: row QQEP base ${BASE:0:7} is not 437ab4b — re-brief" >&2; exit 7; }
q merge-base --is-ancestor "$BASE" "$HQ" 2>/dev/null || { echo "REFUSING: QQEP base ${BASE:0:7} is not an ancestor of $H7" >&2; exit 7; }
[ "$(q merge-base "$HQ" "$MAINH" 2>/dev/null)" = "$BASE" ] || { echo "REFUSING: QQEP merge-base(head, MAIN) is not its base ${BASE:0:7}" >&2; exit 7; }
q merge-base --is-ancestor "$HQ" "$MAINH" 2>/dev/null && { echo "REFUSING: QQEP $H7 is ALREADY ON MAIN ${MAINH:0:7} — the brief says it is not; re-brief" >&2; exit 7; }
q merge-base --is-ancestor "$R1" "$HQ" 2>/dev/null || { echo "REFUSING: round 1's head 7b952f6 is not an ancestor of $H7 — the branch was rewritten (force-push); re-brief" >&2; exit 7; }
q merge-base --is-ancestor "$R2" "$HQ" 2>/dev/null || { echo "REFUSING: round 2's head 3a3399e is not an ancestor of $H7 — the branch was rewritten (force-push); re-brief" >&2; exit 7; }
GOTN="$(q rev-list --count "${BASE}..${HQ}" 2>/dev/null)"
[ "$GOTN" = "$N" ] || { echo "REFUSING: QQEP $H7 has $GOTN commits over its base, the table says $N" >&2; q log --format='%h %p %s' "${BASE}..${HQ}" >&2; exit 8; }
[ "$N" = "7" ] || { echo "REFUSING: the brief's commit count is $N, this launcher's chain is seven commits" >&2; exit 8; }
[ "$(q rev-list --count "${R2}..${HQ}" 2>/dev/null)" = "1" ] || { echo "REFUSING: QQEP $H7 is not exactly ONE commit over round 2's 3a3399e" >&2; exit 8; }
[ "$(q rev-list --count "${HQ}..${ANCHOR_MAIN}" 2>/dev/null)" = "0" ] || { echo "REFUSING: QQEP $H7 is behind 437ab4b" >&2; exit 7; }

# 9 — gated anchors and the exact chain, by parents and trees.
[ "$(q log -1 --format='%P' "$ANCHOR_MAIN")" = "$ANCHOR_MAINP" ] || { echo "REFUSING: 437ab4b's parents are not 9d1c5ab + 818a019" >&2; exit 9; }
[ "$(q log -1 --format='%P' "$C1")" = "$ANCHOR_MAIN" ] || { echo "REFUSING: 0fc280b's single parent is not 437ab4b" >&2; exit 9; }
[ "$(q log -1 --format='%P' "$C2")" = "$C1" ] || { echo "REFUSING: a8d769b's single parent is not 0fc280b" >&2; exit 9; }
[ "$(q log -1 --format='%P' "$R1")" = "$C2" ] || { echo "REFUSING: 7b952f6's single parent is not a8d769b" >&2; exit 9; }
[ "$(q log -1 --format='%P' "$C4")" = "$R1" ] || { echo "REFUSING: a7e1835's single parent is not 7b952f6" >&2; exit 9; }
[ "$(q log -1 --format='%P' "$C5")" = "$C4" ] || { echo "REFUSING: 1f7db41's single parent is not a7e1835" >&2; exit 9; }
[ "$(q log -1 --format='%P' "$R2")" = "$C5" ] || { echo "REFUSING: 3a3399e's single parent is not 1f7db41" >&2; exit 9; }
[ "$(q log -1 --format='%P' "$HQ")" = "$R2" ] || { echo "REFUSING: f31720e's single parent is not 3a3399e" >&2; exit 9; }
[ "$(q rev-parse "${HQ}^{tree}" 2>/dev/null)" = "$HQ_TREE" ] || { echo "REFUSING: f31720e's tree is not ee51fa7" >&2; exit 9; }
[ "$(q rev-parse "${R2}^{tree}" 2>/dev/null)" = "$R2_TREE" ] || { echo "REFUSING: 3a3399e's tree is not ec15fb2" >&2; exit 9; }
[ "$(q rev-parse "${R1}^{tree}" 2>/dev/null)" = "$R1_TREE" ] || { echo "REFUSING: 7b952f6's tree is not 25ddfb8" >&2; exit 9; }
[ "$(q rev-parse "${ANCHOR_MAIN}^{tree}" 2>/dev/null)" = "$MAIN_TREE" ] || { echo "REFUSING: 437ab4b's tree is not c71780c" >&2; exit 9; }
q merge-base --is-ancestor "$ANCHOR_PREGUARD" "$MAINH" 2>/dev/null || { echo "REFUSING: e4ce536 is not an ancestor of main" >&2; exit 9; }
q merge-base --is-ancestor "$BACKLOG_F8" "$HQ" 2>/dev/null && { echo "REFUSING: backlog 815aae7 is on the PR head — the brief says it is not" >&2; exit 9; }
q merge-base --is-ancestor "$BACKLOG_R3" "$HQ" 2>/dev/null && { echo "REFUSING: backlog 01c8d7f is on the PR head — the brief says it is not" >&2; exit 9; }
[ "$(q log -1 --format='%P' "$BACKLOG_R3")" = "$BACKLOG_F8" ] || { echo "REFUSING: backlog 01c8d7f's parent is not 815aae7 (the READY says it is)" >&2; exit 9; }

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
[ "$(ns "$R2" "$HQ")" = "$NUMSTAT_R3" ] || { echo "REFUSING: the round-3 numstat (3a3399e..head) is not the briefed one" >&2; q diff --numstat "$R2" "$HQ" >&2; exit 23; }
[ "$(ns "$R1" "$R2")" = "$NUMSTAT_R2" ] || { echo "REFUSING: the round-2 numstat (7b952f6..3a3399e) is not gate 21's" >&2; exit 23; }
[ "$(ns "$R1" "$C4")" = "$NUMSTAT_C4" ] || { echo "REFUSING: a7e1835's numstat is not the briefed one" >&2; exit 23; }
[ "$(ns "$C4" "$C5")" = "$NUMSTAT_C5" ] || { echo "REFUSING: 1f7db41's numstat is not the briefed one (email-matches-print.mjs only)" >&2; exit 23; }
[ "$(ns "$C5" "$R2")" = "$NUMSTAT_C6" ] || { echo "REFUSING: 3a3399e's numstat is not gate 21's (index.html +2 only)" >&2; exit 23; }
PKG_U0="$(q diff -U0 "$ANCHOR_MAIN" "$HQ" -- stage3/package.json | grep -E '^[+-][^+-]')"
[ "$(printf '%s\n' "$PKG_U0" | wc -l | tr -d ' ')" = "2" ] && printf '%s\n' "$PKG_U0" | grep -q '^-    "test:print": ' && printf '%s\n' "$PKG_U0" | grep -q '^+    "test:print": ' \
  || { echo "REFUSING: package.json's change is not exactly the test:print line. Got:" >&2; printf '%s\n' "$PKG_U0" >&2; exit 23; }
[ "$(printf '%s\n' "$PKG_U0" | sed -n 's/^-//p' | sed 's#test/email-print-mode.mjs #test/email-print-mode.mjs test/email-matches-print.mjs test/custom-price-bounds.mjs #')" = "$(printf '%s\n' "$PKG_U0" | sed -n 's/^+//p')" ] \
  || { echo "REFUSING: the test:print change is not ONLY test/email-matches-print.mjs + test/custom-price-bounds.mjs inserted after test/email-print-mode.mjs" >&2; exit 23; }
python3 - "$Q_REPO" "$ANCHOR_MAIN" "$R2" "$HQ" <<'PY' || { echo "REFUSING: the package.json dependency maps or version differ between base, round 2 and head (the brief says only a script line changed)" >&2; exit 23; }
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
# file | base blob | round-2 blob | head blob   ('-' = absent)
for P in 'index.html|dde1392465fa3202db7eb28edf140639110d4417|cf71c84cbb9fc1e6d44ea0580c14644f556a2f93|e65f3b6ea0626201600dd70dae7b55214cd41dab' \
         'stage3/lib/pdf.js|783ebea5ea8708e02df25740b75b51e631f2ce37|257bbfa8fa46a293be441307450ffaf3b73c20b3|26825da72357fb002512a2eca94b9292b88ecee2' \
         'stage3/package.json|1606aa3b4f0fa9b53811c7bc71f96cd57178a420|cd9118a1bfc24f8bf6968d08f6505a9e2cd42ccb|cd9118a1bfc24f8bf6968d08f6505a9e2cd42ccb' \
         'stage3/server.js|a854ba2c5144887c9e8ad530bedcaf4f8526f23f|e40c20ec492cb6d3063a648f1f4ad3fc08fe0d23|e40c20ec492cb6d3063a648f1f4ad3fc08fe0d23' \
         'stage3/strip.js|0730e10459550ad1a7f63f9d8bc388e0550ec0ea|9cddb706d71cf88c7db116554ef7480b17e7e73c|9cddb706d71cf88c7db116554ef7480b17e7e73c' \
         'stage3/test/custom-price-bounds.mjs|-|76368d24709c1cfed6be98e64f77f4b587f6696f|b3c534525eb165124f621f4dc7fcdd40dd3d4119' \
         'stage3/test/email-matches-print.mjs|-|bdb602b8d4baedec60e54cdf398965eb62200aba|bdb602b8d4baedec60e54cdf398965eb62200aba' \
         'stage3/test/email-print-mode.mjs|b1d4443c45195cb80075dd443f07a59b6c53817c|9dd53112ddc07bbaf51c44a4de2d304da06b4ae5|9dd53112ddc07bbaf51c44a4de2d304da06b4ae5'; do
  F="${P%%|*}"; REST="${P#*|}"; B0="${REST%%|*}"; REST="${REST#*|}"; BR2="${REST%%|*}"; B1="${REST#*|}"
  [ "$B0" = "-" ] && B0=''; [ "$BR2" = "-" ] && BR2=''
  [ "$(blob "$ANCHOR_MAIN" "$F")" = "$B0" ] && [ "$(blob "$R2" "$F")" = "$BR2" ] && [ "$(blob "$HQ" "$F")" = "$B1" ] \
    || { echo "REFUSING: $F blobs are not ${B0:0:7}|${BR2:0:7}|${B1:0:7} at base|round 2|head" >&2; exit 74; }
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
# round-3 anchors at the head (round 2's kept ones too), and absent at round 2
for T in 'toolVersion: "2.39"' 'customPriceMinPerMonth: 0.01,' 'customPriceMaxRatio: 10,' 'let cpModeWanted = null;' \
         'function cpSyncFrom(sourceId, committed) {' 'if (el.validity.badInput) {' \
         'return off(committed ? "That is not a number. Custom pricing is off until you enter a price." : "");' \
         'return off(committed ? "Custom pricing is off until you enter a price." : "");' \
         'return off(committed || tooHigh ? why + " Custom pricing is off until you change it." : "");' \
         'for (const b of [c.stdPerDevMonth * CONFIG.customPriceMaxRatio, CONFIG.customPriceMinPerMonth]) {' \
         'if (cpModeWanted && sel && sel.value === "default") $(cpModeWanted).checked = true;' \
         'const cpMax = () => { const c = calc(); return (c.stdPerDevMonth / c.fxRate) * CONFIG.customPriceMaxRatio * (1 + 1e-9); };' \
         'const min = CONFIG.customPriceMinPerMonth / c.fxRate * (1 - 1e-9);' \
         'if (typeof usd === "number" && Number.isFinite(usd) && usd >= min && usd <= cpMax()) return null;' \
         'return `A custom price must be at least ${fmt(CONFIG.customPriceMinPerMonth)}/device/month and no more than ` +' \
         'cpRefuse(why + " Custom pricing is off until you change it.");' \
         'cpSyncFrom(id, !e.inputType || e.inputType === "insertFromPaste" || e.inputType === "insertFromDrop"));' \
         '$(id).addEventListener("change", () => cpSyncFrom(id, true));' \
         'function cpCheck(usd) {' 'function cpRefuse(msg) {' 'function renderCustom(skipId) {' \
         '<div class="svc-warn" id="cpRefused" role="alert"></div>' 'const why = cpCheck(newPDM);' '#cpRefused { margin: 0 1.1rem .55rem; }' \
         '/* ==== ADVANCED SEAM START ===='; do
  must "$HQ" index.html "$T"
done
mustnot "$HQ" index.html 'usd > 0 && usd <= max'
must "$R2" index.html 'toolVersion: "2.38"'
mustnot "$R2" index.html 'customPriceMinPerMonth'
mustnot "$R2" index.html 'cpModeWanted'
mustnot "$R2" index.html 'until you enter a price'
mustnot "$R1" index.html 'function cpCheck('
must "$ANCHOR_MAIN" index.html 'toolVersion: "2.36"'
# the seam sits where the brief says (3816-3827): located by line number only, never printed
[ "$(q show "${HQ}:index.html" | awk '/ADVANCED SEAM START/{print NR; exit}')" = "3816" ] || { echo "REFUSING: the ADVANCED SEAM no longer starts at index.html:3816 — the brief's never-print range is stale; re-brief" >&2; exit 74; }
for T in 'path.join(__dirname, "..", "private", "advanced.js")' 'buildPrintDoc(printMode, qnum, { emailCopy: true })' 'buildPrintRows(printMode, qnum)' \
         'const why = window.cpRestore(cu);' 'if (why) return { refused: why + " The quote was not sent." };' \
         'This quote asks for custom pricing but carries no custom price, so it was not sent. ' \
         'if (report.refused) return { pdf: null, xlsx: null, report };' 'if (typeof window.cpRestore === "function" && wantsCustom) {'; do
  must "$HQ" stage3/lib/pdf.js "$T"
done
mustnot "$R2" stage3/lib/pdf.js 'cpRestore === "function" && wantsCustom'
mustnot "$R1" stage3/lib/pdf.js 'report.refused'
# the head's bounds file: the new sentence, the synthetic paste (brief WRONG (b)), 18 test( calls (= 32 cells)
must "$HQ" stage3/test/custom-price-bounds.mjs 'const REFUSAL = /^A custom price must be at least A\$0\.01\/device\/month and no more than 10 times'
must "$HQ" stage3/test/custom-price-bounds.mjs 'el.value = t; el.dispatchEvent(new InputEvent("input", { bubbles: true, inputType: "insertFromPaste" }));'
[ "$(q show "${HQ}:stage3/test/custom-price-bounds.mjs" | grep -cE '^[[:space:]]*test\(')" = "18" ] || { echo "REFUSING: the head's bounds file does not carry 18 test( calls (15 + 17 cells) as the brief says" >&2; exit 74; }
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
must "$BACKLOG_R3" BACKLOG.md '(G21-F3)'
must "$BACKLOG_R3" BACKLOG.md 'G20-F7 / G21-O3'
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

# 31 — the builder's round-3 mail is on disk byte for byte, names the pinned head, carries a NOT TESTED block and no NexusAI text; gate 21's report on disk.
[ -s "$READY" ] || { echo "REFUSING: the builder's round-3 mail is not on disk: $READY" >&2; exit 31; }
[ "$(shasum -a 256 "$READY" | awk '{print $1}')" = "$READY_SHA" ] || { echo "REFUSING: $READY is not the copy the drafter read (sha256 differs) — re-read it and re-brief" >&2; exit 31; }
for T in 'READY FOR QA: QQEP round 3 — PR #10 @ f31720e (v2.39)' \
         'Head f31720ee677dbe2deb53dcb7991f1683a1b03ce1 (v2.39). One new commit on fix/qq-email-matches-print-2026-10-16, fast-forward from 3a3399e, no force-push.' \
         'G21-F2: a floor. CONFIG.customPriceMinPerMonth = 0.01 (index.html:1752)' 'custom-price-bounds.mjs: red 16 of 32 at 3a3399e, green 32 of 32 at f31720e.' \
         "the round-3 test file run in a 3a3399e worktree, with the old sentence's regex" 'I, no 1e-9 floor tolerance: NONE.' \
         'Totals: pricing 69/69, npm test 132/132, test:print 217/217, test:xlsx 6/6.' 'Backlog 01c8d7f (backlog/qq-extract-zip-2026-10-16, parent 815aae7), pushed.' \
         'The number-field spinner arrows: their input events carry no keystroke inputType, so they are judged as committed. Reasoned, not driven.' \
         '## NOT TESTED' '## NEW WORDS FOR KAM' 'Holding for gate 22.'; do
  grep -qF -- "$T" "$READY" || { echo "REFUSING: $READY does not carry '$T'" >&2; exit 31; }
done
[ "$(wc -l < "$READY" | tr -d ' ')" = "124" ] && ! grep -qF 'NexusAI' "$READY" \
  || { echo "REFUSING: $READY is not the 124-line Vision-only copy (lines 1-124 of Tuesday's batch) the drafter made" >&2; exit 31; }
for T in 'carry a NOT TESTED block' 'C-20' 'quickquote-email-sends-standard-not-custom-1016' 'quickquote-guard-words-1016' 'quickquote-pr10-r2-publish-hold-1017' \
         'ROUND 3' 'no round 4 without' '2026-10-17_vision-qq-pr10-r3-READY-mail.txt' 'WRONG (a)' 'WRONG (b)' 'WRONG (c)' 'WRONG (d)' 'WRONG (e)' 'WRONG (f)' \
         'WRONG (g)' 'WRONG (h)' 'WRONG (i)' 'WRONG (j)' 'WRONG (k)' 'WRONG (l)' 'WRONG (m)' 'WRONG (n)' 'WRONG (o)' 'WRONG (p)' 'WRONG (q)' 'GH-API-LEG' \
         'AZ-READ-LEG' 'AZ-PRE-READ' 'N4-METHOD' 'ROUTING-LINE' 'D4' 'D5' 'PROVISIONAL' 'G21-F1' 'G21-F2' 'G21-F3' 'G21-F4' 'G21-F5' 'G21-F6' 'G21-F7' \
         'G21-F8' 'G20-F1' 'G20-F3' 'G20-F4' 'G20-F7' 'G22-MA' 'G22-MI' 'G22-M1' 'G22-M6' 'G22-F1' 'R-G' 'R-H' 'R2-F1' 'R2-F2' 'R2-F5' 'P3″' 'P15' \
         'B-STATE' 'B-TRANS' 'FLOOR-FX' 'FLOOR-CUR' 'KEY-COMMIT' 'SPIN' 'MODE-WANTED' 'F-SNAP' 'U-AT' 'U-OVER' 'F-AT' 'F-UNDER' 'MUT-I' 'THE NUMBERS' \
         'DEFECT-REASON' 'NEW-SURFACE-ABSENT' 'WORDING' 'TYPED-WHOLE' 'insertFromPaste' 'insertText' 'customPriceMinPerMonth' 'customPriceMaxRatio' \
         'cpModeWanted' 'cpCheck' '422' '1e308' '01c8d7f' '815aae7' 'cdcd490' '5ef2a60' 'pdmUSD' 'NEW WORDS FOR KAM' '3816-3827' '47310' \
         "$W1_SHA" "$W2_SHA" 'HPAM' 'live check' "$READY_SHA" '3a3399e' 'S5'; do
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
grep -qF '**C-21.' "$CLAR" && echo "NOTE: Vision CLARIFICATIONS now has a C-21 — the brief says C-01..C-20; read it before launch (Kam's round-3 card is not in CLARIFICATIONS at drafting)" >&2
[ -s "$CHARTER" ] || { echo "REFUSING: the charter is absent: $CHARTER" >&2; exit 31; }
[ -s "$G21_REPORT" ] || { echo "REFUSING: gate 21's report is absent: $G21_REPORT" >&2; exit 31; }
grep -qF '**NO GO**' "$G21_REPORT" && grep -qF "$R2" "$G21_REPORT" && grep -qF 'G21-F1' "$G21_REPORT" && grep -qF 'G21-F8' "$G21_REPORT" \
  || { echo "REFUSING: gate 21's report does not carry QQEP's NO GO at 3a3399e with G21-F1..F8" >&2; exit 31; }
[ -s "$G21_DIR/evidence/mail/verdict-body.txt" ] || { echo "REFUSING: gate 21's verdict body is not on disk" >&2; exit 31; }
grep -qF "$G21_DIR" "$BRIEF" || { echo "REFUSING: the brief does not name $G21_DIR" >&2; exit 31; }
case "$PROMPT" in *"$G21_DIR"*) ;; *) echo "REFUSING: the prompt does not name $G21_DIR" >&2; exit 31 ;; esac
for H in qa-run.py mktree-qq.sh lockcmp.py lockwalk.py tapsets.py g17-dupnames.py g21-run-suites.sh g21-mutate.py g21-mutant-arm.sh g21-arm.sh \
         g21-cell.sh g21-grid.sh g21-compare.py g21-n4-run.py g21-n4-multi.py g21-n5.py g21-gh.sh g21-heads.sh g21-infscan.py g21-figures.py \
         g21-seq-n4.py g21-steps.py g21-tapfail.py g21-run-cells.py g21-aggregate.py g21-cmdlog.py g21-repoint.py qa-harness-g21-drive.cjs \
         qa-harness-g21-offline.cjs qa-harness-g16-shots.mjs qa-chrome-egressblock.sh qa-chrome-census.py qa-egress-posctl.mjs qa-floorcount.py \
         qa-harness-floorctl.mjs qa-netlog-scan.py; do
  [ -s "$G21_TOOLS/$H" ] || { echo "REFUSING: gate 21's tool $H is not on disk — the brief names it" >&2; exit 31; }
  grep -qF -- "$H" "$BRIEF" || { echo "REFUSING: the brief does not name gate 21's tool $H" >&2; exit 31; }
done
# the paste premise of WRONG (b): gate 21's drive harness pasted by CDP Input.insertText
grep -qF 'CDP Input.insertText' "$G21_TOOLS/qa-harness-g21-drive.cjs" || { echo "REFUSING: gate 21's drive harness no longer names CDP Input.insertText — WRONG (b)'s premise is unread; re-brief" >&2; exit 31; }

# 39 — the floor instrument is on disk and named.
[ -s "$G21_TOOLS/qa-floorcount.py" ] || { echo "REFUSING: gate 21's floor instrument copy missing" >&2; exit 39; }
grep -qF 'qa-floorcount.py' "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument qa-floorcount.py" >&2; exit 39; }

# 10 / 17 — report path named in both; no stale report.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

# 12 — tier declared in both, at the pinned head.
grep -qE "^- \*\*QQEP\*\* at \`${H7}\` — \*\*TIER 1" "$BRIEF" || { echo "REFUSING: brief does not declare QQEP at \`$H7\` TIER 1" >&2; exit 12; }
case "$PROMPT" in *"QQEP (TIER 1"*) ;; *) echo "REFUSING: prompt does not declare: QQEP (TIER 1" >&2; exit 12 ;; esac

# 78 — the commission's requirements, in both.
for T in 'TIER 1' 'ROUND 3' 'no round 4' 'C-20' 'quickquote-email-sends-standard-not-custom-1016' 'quickquote-pr10-r2-publish-hold-1017' \
         'GO WITH FINDINGS' 'NO GO' 'SETS, NOT COUNTS' 'f31720e' '3a3399e' '437ab4b' 'a8d769b' 'custom-price-bounds.mjs' 'email-matches-print.mjs' \
         'createApp()' 'renderQuotePdf' 'frozen clock' 'Standard pricing only' 'Custom pricing only' 'Standard + custom' 'Custom pricing note' \
         'q-savings' 'light' 'dark' 'cpCheck' 'customPriceMaxRatio' 'customPriceMinPerMonth' 'floor' 'ceiling' '1e308' '422' 'refused' 'cleared' \
         'spinner' 'inputType' 'insertFromPaste' 'keystroke' 'committed' 'cpModeWanted' 'live rate' 'advanced.js' 'index.html' 'npm test' \
         'test:print' 'test:xlsx' 'quote-engine.test.mjs' 'pdftotext' 'pdftoppm' 'pdffonts' 'workbook' 'AUD' 'USD' 'CAD' 'offline' 'linuxFxVersion' \
         'AZ-PRE-READ' 'double-press' 'G21-F1' 'G21-F2' 'G21-F4' 'G21-F5' 'G21-F7' 'G21-F8' 'mutant' 'Reset form' 'Advanced off' 'C-05' 'reopen' \
         'key by key' 'STRESS' 'RECIPIENT' 'simple session' 'rollback' 'G20-F3' 'G20-F4' 'G21-F6' 'NEW WORDS FOR KAM' 'file:line' 'node strip.js' \
         'node --check' 'Claude in Chrome' 'HPAM word' 'PROVISIONAL' 'ONE browser at a time' 'docker' '.invalid' 'NO EMAIL TO ANY HUMAN ADDRESS' \
         'CodeQL' 'never dismiss' 'closure table' 'G22-F1'; do
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
WORDS="merge-tree NOT%TESTED env%-i bash 437ab4b f31720e 3a3399e work-g22 FOREGROUND MEASURED%AT%RUNTIME PROBED READ%ONLY start%/%mid%/%end CI VOID node%--check"
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
for T in 'EXCLUSIVE' 'work-g22'; do
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
case "$LOAD1" in ''|*[!0-9.]*) ;; *) awk -v l="$LOAD1" 'BEGIN{exit !(l>40)}' && echo "NOTE: 1-minute load is $LOAD1 (drafting read 4.85) — browser cells will be slow; Tuesday decides whether to launch now" >&2 ;; esac

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

# 86 — no live gate-22 session already exists.
for P in $(pane_pid_of "$ROUTE_NAME"); do
  if [ -n "$(claude_under "$P")" ]; then echo "REFUSING: a pane named $ROUTE_NAME (pid $P) already runs a claude — gate 22 is live; do not start a second session" >&2; exit 86; fi
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

# 41 — the answer route exists (Tuesday adds 'QA/Vision-gate22|tuesday-agent@agentmail.to|no' at stamp; this launcher never writes it).
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" \
  || pend 41 "no '${ROUTE_NAME}|tuesday-agent@agentmail.to|…' line in $ROUTING — answers to the gate would have no route. Add it (pattern: the QA/Vision-gate21 line) before launch, and stamp the brief's ROUTING-LINE."

# 32 — the coordinator stamps the self-check (line AND note), AZ-PRE-READ, D4-D5, the ROUTING-LINE and every @STAMP@.
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF" \
   || ! grep -q '^ROUTING-LINE: QA/Vision-gate22' "$BRIEF"; then
  pend 32 "the brief still carries $(grep -cF "$PH_STAMP" "$BRIEF") ${PH_STAMP} placeholder(s) (Self-check line and note, AZ-PRE-READ, ROUTING-LINE, the RULED lines of D4-D5) — the coordinator re-reads end-to-end and stamps all of them before launch (ROUTING-LINE must begin 'QA/Vision-gate22')"
fi

if [ -n "$PENDING" ]; then
  echo "guards pass (MODEL 40 6 9 7 8 18 22 23 74 63 31 39 10 17 12 78 45N 13 14 15 20 70 82 19 24 53 60 61 62 64 69 75 44 38R 86 46); coordinator to-do pending (47 48 41 32 as listed above); exiting $PENDING." >&2
  echo "  origin re-read $PIN_TS: main ${MAINH:0:7}, QQEP $H7, refs/pull/10/head $H7; model $MODEL; GH-API-LEG $GHLEG" >&2
  echo "  NEG seats (38R, derived live):$NEG_DESC" >&2
  exit "$PENDING"
fi

PIN_BLOCK="$(printf 'PINNED HEADS — verified by the launcher at %s (cat-file; base 437ab4b, 0 behind; ancestor and merge-base with MAIN; not-already-on-main; commit count 7; chain 437ab4b <- 0fc280b <- a8d769b <- 7b952f6 <- a7e1835 <- 1f7db41 <- 3a3399e <- f31720e by single parents; round 1 7b952f6 and round 2 3a3399e ancestors; head tree ee51fa7; round-2 tree ec15fb2; round-1 tree 25ddfb8; main tree c71780c; main pinned EXACTLY; refs/pull/10/head = head; the 8-file delta and numstat whole, round 3 and round 2; the test:print line; blobs at base / round 2 / head; Kam'"'"'s retired W1/W2 present at base strip.js and absent at the head by sha256; git ls-remote origin for both rows):\n' "$PIN_TS"
  printf '%s\n' "$PIN" | awk -F'\t' '{ printf "  %-7s %-11s %-42s %s  base %s  commits %s\n", $1, $2, $3, $4, ($5=="-"?"-":substr($5,1,12)), $6 }'
  printf '  Round 1 (gate 20, NO GO): 7b952f6edbcc3b271e4a650685f47b87760ed8f0. Round 2 (gate 21, NO GO): 3a3399e947bf5faf8a8e0c0d3e11956c6590db98. Main: pinned %s (exact; a move refuses). PR #%s: refs/pull/%s/head = %s; refs/pull/%s/merge = %s (GitHub test merge)\n' "${MAINH:0:12}" "$PR_NUM" "$PR_NUM" "${HQ:0:12}" "$PR_NUM" "${PR_MERGE_NOW:-<absent>}"
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
ID_TMP="$(mktemp -d "${TMPDIR:-/tmp}/qa-vision-gate22-id.XXXXXX")" || { echo "REFUSING: cannot create the empty identity dir" >&2; exit 11; }
mkdir -p "$ID_TMP/azure-empty" "$ID_TMP/gh-empty" "$ID_TMP/bin" || { echo "REFUSING: cannot create the identity dirs under $ID_TMP" >&2; exit 11; }
{ [ -z "$(ls -A "$ID_TMP/azure-empty")" ] && [ -z "$(ls -A "$ID_TMP/gh-empty")" ]; } || { echo "REFUSING: the identity dirs under $ID_TMP are not empty" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_TMP/azure-empty"
export GH_CONFIG_DIR="$ID_TMP/gh-empty"
if [ "$GHLEG" = "READ-ONLY-VISION-TOKEN" ]; then
  QA_REAL_GH="$(command -v gh)" || { echo "REFUSING: gh vanished between guard 46 and launch" >&2; exit 11; }
  export QA_REAL_GH
  cat > "$ID_TMP/bin/gh" <<'SHIM'
#!/bin/bash
# gate-22 GET-only gh shim (written by launch_qa_vision_qq_gate22.sh; GH-API-LEG = READ-ONLY-VISION-TOKEN). Brief §HELD binds the rest.
REAL="${QA_REAL_GH:?gh shim: QA_REAL_GH unset}"
[ "${1:-}" = "api" ] || { echo "gh shim: only 'gh api' GET reads are allowed in Vision gate 22 (got: ${1:-<none>})" >&2; exit 64; }
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
