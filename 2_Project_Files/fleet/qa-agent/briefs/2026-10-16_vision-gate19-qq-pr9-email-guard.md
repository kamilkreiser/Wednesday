# QA Agent Invocation Brief — Datasec/Vision_Sales_Portal, GATE 19: ONE TIER-1 QuickQuote gate — PR #9 (the email guard, C-20) @ `5f08fe0` on QuickQuote main `e4ce536` — one verdict, one report

**TIER 1 (quote output to customers: what the hosted page lets a rep email, and what the customer receives).** ROUND 1 of 2 of PR #9 (new branch,
no earlier gate). A NO GO sends it back for round 2; it does not go to Kam.

**Drafted for Tuesday on 2026-10-16 between 14:01 and 14:4x AEDT by a read-only drafting agent. Tuesday reviews, stamps and launches it.**
Templates: `BRIEF_TEMPLATE.md` and gate 18's kit (`2026-10-16_vision-gate18-qq-pr8-puppeteer25.md`, its DRAFTER-REPORT, `launch_qa_vision_qq_gate18.sh`),
written an hour earlier on the same repo: the section shape, the identity rules (GET-only `gh` shim), the report-path convention, the verdict token,
THE MODEL RULE, the floor and HELD rules and the resolved traps (Laptop-DEV paths; the T9 QuickQuote repo is STALE). **This brief governs where they differ.**

**THIS GATE IS LIGHTER THAN GATE 18: NO DOCKER.** The delta (READ, and the PR files API — §Charter) is `stage3/strip.js` (the hosted Email handler),
one new test file and one `package.json` script line. `stage3/Dockerfile`, `stage3/package-lock.json`, `.dockerignore`, the hosted server module,
`lib/pdf.js` and `lib/xlsx.js` carry the SAME blob at base and head. The image would run the same `node strip.js` over the same `index.html` and the
changed `strip.js` that this gate runs on the host, with the same lockfile. **So no image is built or run, and no `docker` command of any kind is
issued** (not even a read). The guard inside the published image is a publish-time check (Kam's tap via Tuesday's PUBLISH GO, §NOT TESTED).

The builder's READY mail under test (on disk, read whole by the drafter):
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-16_vision-qq-pr9-guard-READY-mail.txt`
**Every builder statement below comes from that mail, the commit message or the code at each sha. Each one is a CLAIM. Every red, every mutant,
every suite set, every browser result and every comparison is RE-DERIVED by the gate. None is taken from the READY.**
The launcher parses §PIN, refuses any placeholder, and re-reads both rows (and `refs/pull/9/head`) by `git ls-remote` immediately before launch,
refusing on any mismatch, **including any move of QuickQuote main** (this gate pins main exactly). The verified table is appended to your prompt.

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-16 14:21 AEDT
Self-check note: Tuesday read all 577 lines whole before stamping; no contradiction found between R1-R8, WRONG (a)-(m), the FAIL conditions and HELD. The compute hold on the MPS lanes (ADDENDUM-4, 14:08) lowered the load to ~4 (1-min) at 14:21; gate 23 may re-run its NexusAI verify beside you: contention, not conflict.

GH-API-LEG: READ-ONLY-VISION-TOKEN
<!-- Set by Tuesday's commission (2026-10-16 ~14:0x: "Keep its guards, identity rules (D1 READ-ONLY token as gate 17/18)"). The launcher exports
     GH_CONFIG_DIR = Vision's .gh-config behind a GET-only `gh` shim first on PATH (gate 17's D1, ruled 2026-10-13 10:39). Change it to NOT-RUN only
     if Tuesday withdraws the token; then every GitHub read is NOT RUN and the drafter's readings stay READ-BY-DRAFTER. -->

AZ-READ-LEG: TUESDAY-READS
<!-- Set by Tuesday's commission ("Tuesday reads it; leave an AZ-PRE-READ line for Tuesday to stamp, as gate 18 did"). The gate runs NO az. Tuesday
     reads the live webapp's linuxFxVersion BEFORE launch, writes it on the line below, and reads it again at verdict. The gate RELAYS. -->
AZ-PRE-READ: linuxFxVersion DOCKER|hpasqqacr.azurecr.io/hpas-quickquote:v0.6.3-tool2.35-3dd15bc ; read 2026-10-16 14:21:25 AEDT by Tuesday (az webapp config show, Vision's own AZURE_CONFIG_DIR, tenant d500ebad / sub 0c57ab37, SP bc1e3581). Serves gate 19 only (gate 18 not launched).
<!-- One line, e.g. `linuxFxVersion DOCKER|hpasqqacr.azurecr.io/hpas-quickquote:<tag> ; read <YYYY-MM-DD HH:MM:SS AEDT> by Tuesday (az, tenant d500ebad /
     sub 0c57ab37)`. One reading may serve gates 18 and 19 if taken immediately before both launches; say so. The launcher refuses until it names
     linuxFxVersion. Drafter's expectation (NOT a reading): v0.6.3-tool2.35-3dd15bc, published 2026-10-13 ~12:24 AEDT (Tuesday's 10-13 note, 12:29). -->

LEG7-METHOD: GATE-METHOD
<!-- Decision D5 (§N7). Exactly one of:
       STATUS-MAILS  Tuesday saves the builder's two measurement STATUS mails of 2026-10-16 (02:10Z and 02:3xZ, named in the READY's PRIOR WORK line)
                     VERBATIM to /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-16_vision-qq-printmode-STATUS-mails.txt; the
                     gate reads them as CLAIMS and re-derives the builder's figure-subset method from them (the launcher refuses if the file is absent).
       GATE-METHOD   the gate uses §N7's own method (full text + money-figure multiset + pixels, base vs head; plus the email-vs-print subset).
     The drafter found neither mail on disk (grep of TUESDAY 0_Brain, fleet/ and 5_Project_History for "46,215" / "50,383": 0 hits outside the board
     card). Drafter's reading: GATE-METHOD (it is a superset); STATUS-MAILS only if Tuesday wants the builder's numbers re-derived exactly. -->

## Charter
Read `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an independent tester. You did not
build this change and you owe the builder nothing. **Every line below that reports what the builder says is a CLAIM, never evidence.**

**One gate, ONE target, ONE verdict: GO / GO WITH FINDINGS / NO GO, at its pinned sha.**
- **QQGD** at `5f08fe0` — **TIER 1 (quote output to customers).** ROUND 1 of PR #9.
  QuickQuote PR #9, branch `fix/qq-email-print-mode-guard-2026-10-16`, "stage3: email guard — custom print modes no longer email the standard price
  silently (C-20)". ONE commit over main `e4ce536`:

| # | commit | parents | what it is |
|---|---|---|---|
| 1 | `5f08fe0` (2026-10-16 13:52:43 +1100) | `e4ce536` | "stage3: email guard — a custom print mode no longer emails the standard price silently" — THE HEAD |

**THE DELTA THAT SHIPS is `git diff e4ce536 5f08fe0` (3 files, +204/−2)** — the same three files and counts in the PR files API (READ-BY-DRAFTER,
`gh api …/pulls/9/files`, 14:0x: `stage3/package.json` modified +1/−1 blob `1606aa3`; `stage3/strip.js` modified +28/−1 blob `0730e10`;
`stage3/test/email-print-mode.mjs` added +175 blob `b1d4443`; PR `changed_files` 3, additions 204, deletions 2):

| file | +/− | what (READ at the pinned shas) |
|---|---|---|
| `stage3/strip.js` | +28 / −1 | blob `2fc3bd6` → `0730e10`. In `HOSTED_EXTRAS` (the hosted-only Email handler injected before `</body>` of `public/index.html`): the label moves into `const LABEL`; new `ARMED_LABEL`, `WARNING`, `armedFor`, `printMode()`, `disarm()`; a document-level `change` listener that disarms on any `printMode` change while armed; at the top of the click handler, a non-`default` mode not yet armed for THAT mode arms, sets the label and the warning, adds `svc-warn active` to `#emailPdfNote` and RETURNS without sending; otherwise `disarm()` and the existing send path, unchanged |
| `stage3/package.json` | +1 / −1 | blob `61d0d5c` → `1606aa3`: `test/email-print-mode.mjs` inserted into `test:print` after `test/email-collector.mjs`. No dependency line changes |
| `stage3/test/email-print-mode.mjs` | +175 | new: 5 cells (2 from a `for` over `custom`/`both`, + switch-back, + no-carry-over, + the standard-mode control); Chrome via the tree's puppeteer-core; every request intercepted at `http://qq.test`: `/api/advanced/unlock` → `{ok:true}`, `/api/advanced/module` → `private/advanced.js`, `/api/quote/email` → a stub `{ok:true,qnum:"DSQ-20261016-120000-H01",stored:true}` that records the POST body; anything else aborted |

**Same blob at base and head (READ, `rev-parse <sha>:<path>`):** `index.html` `447b129`, `stage3/package-lock.json` `01c5e5e`, `stage3/Dockerfile`
`8311ebe`, the hosted server module `a854ba2`, `stage3/lib/pdf.js` `783ebea`, `stage3/lib/xlsx.js` `10bf4d7`, `stage3/lib/mail.js` `3aa8922`,
`stage3/lib/store.js` `0609594`, `stage3/login.html` `f362b45`, `.dockerignore` `acf7db8`, `.github/workflows/tests.yml` `ec450f5`,
`quote-engine.test.mjs` `2d193b6`, `stage3/test/print-fit.mjs` `543f4c1`, `stage3/test/email-collector.mjs` `85a27c5`, `stage3/test/server.test.mjs`
`b35a2eb`, `CLAUDE.md` `af402a7`. Head tree `dc6aef6`.

**Names, written out every time:**
- **QQGD** = branch `fix/qq-email-print-mode-guard-2026-10-16` = PR #9 = "fix (1)" = "the guard" = the delta above. **C-20** = Kam's ruling, card
  `quickquote-email-sends-standard-not-custom-1016` = (a) "Publish the guard as soon as it passes the gate, full fix after". **MAIN-Q** = QuickQuote
  main `e4ce536` = merge of PR #7 (the dependency round, C-18). **"fix (2)"** = email follows the print mode: a SEPARATE round, NOT gated here.
- **KAM'S WORDS** = the two rep-visible strings, approved verbatim on card `quickquote-guard-words-1016` = (a) "Approve both sentences as written":
  - **W1 (the warning, 220 bytes UTF-8, sha256 `0d5beedb47709eed6c7c6eec5d8ced3e73c58069ea09f49f4495cde1abeb25b9`):**
    `This email sends standard pricing only. Your custom pricing is on the printable quote, but it will not be in the email. Choose “Standard pricing only” above, or press the button again to send standard pricing anyway.`
  - **W2 (the armed button, 28 bytes, sha256 `4c73c1593e64f73dc84d24c48a69896307108d387b70a9318b0d7f7dd3ec797d`):** `Send standard pricing anyway`
  - The quotes around Standard pricing only are U+201C and U+201D (bytes `e2 80 9c` / `e2 80 9d`), not ASCII `"`. **"Warning:" and "Armed button:"
    are the READY's LABELS, not part of the text** (WRONG (a)).

Branch status: **NOT on main. PR #9 is open, not merged** (`gh api …/pulls/9`: state open, merged false, draft false, mergeable_state clean, head
`5f08fe0…`, base `e4ce536…` ref main, created 02:53:01Z — READ-BY-DRAFTER 14:0x).

## RULED BY KAM, AND SETTLED
- **Vision `1_Project_Definition/CLARIFICATIONS.md`** (`/Volumes/Laptop-DEV/!CODING/Datasec/Vision_Sales_Portal/1_Project_Definition/CLARIFICATIONS.md`):
  read it whole (C-01..C-20, read 14:0x). **Cite only what you open.** The entries this gate turns on:
  - **C-20 (Kam, live board 2026-10-16 13:25:51 AEDT, card `quickquote-email-sends-standard-not-custom-1016` = (a)):** "Publish the guard as soon as
    it passes the gate, full fix after". The defect, as C-20 records it: in an advanced session the emailed quote is always rendered as "Standard
    pricing only" (lib/pdf.js), so "Custom pricing only" emailed the standard price and "Standard + custom" emailed the standard section alone
    (measured 2026-10-16, AUD/USD/CAD). Order: fix (1) the guard (PR #9), tier 1, gate, then publish on Tuesday's PUBLISH GO quoting this ruling
    (rollback image kept, post-deploy checks). **"Kam's grant covers the GUARD only."** Fix (2) and PR #8 (C-19) each need Kam's own word before any
    publish. "Do not contact anyone who received an emailed quote."
  - **The words (Kam, live board 2026-10-16 13:51:38 AEDT per Tuesday's note 13:52, card `quickquote-guard-words-1016` = (a)):** W1 and W2 above, as
    the card quoted them. The drafter compared the card's quoted strings with the `WARNING` / `ARMED_LABEL` constants at `5f08fe0` in `stage3/strip.js`:
    **byte-identical** (python sha256 of both, 14:0x). The gate re-derives this AND measures the RENDERED text (§N4).
  - **C-19** (PR #8, gate 18) and **C-18** (PR #7, main `e4ce536`): background. **PR #7 was merged to main but never published** (C-18 "Not covered:
    any deploy, publish"); see WRONG (h).
- **PRODUCTION IS LIVE for this project.** Live QuickQuote (`hpas-quickquote`, `hpas-quickquote-rg`, its registry `hpasqqacr`, its Table Storage and
  its log workspace) and the live portal (`datasec-sales-portal.azurewebsites.net`, `datasec-sales-portal-rg`) are PRODUCTION. **Nothing in this gate
  touches either** (§13, HELD). The gate makes no Azure contact at all (AZ-READ-LEG = TUESDAY-READS).
- **Merging and publishing are HELD. Nothing merges or publishes on your word.** A merge is Tuesday's GO on a pinned head; the publish is Tuesday's
  PUBLISH GO under C-20.
- **The BUILDER's choices, each judged by the gate (say whether each needs Kam):** (1) the guard lives in the hosted build only (`strip.js`
  `HOSTED_EXTRAS`), the offline `index.html` untouched; (2) "armed for THAT mode": a second press in the same mode sends with no further confirmation;
  (3) disarm happens on a `change` event of a `printMode` radio — programmatic mode changes that fire no event are not seen (WRONG (d)); (4) the
  warning reuses the page's `.svc-warn` amber box on the existing `#emailPdfNote` div (no new colours, no `aria-live`, no ⚠ glyph — the other
  `.svc-warn` boxes carry an `aria-hidden` ⚠ span); (5) the test stubs the server, so it asserts the POSTED state, never the mail (the READY's own
  NOT TESTED line 2).

## PRIOR ROUND
PRIOR ROUND: none for PR #9 — this is its round 1 (new branch, created 2026-10-16 02:53Z). There is no round-N−1 report to carry.
The last QuickQuote gate WITH A REPORT is **gate 17** (QQQR GO WITH FINDINGS at `d030674`; G17-F1..F3, G17-P1..P3):
ITS REPORT IS ON DISK AT: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-10-13-vision-gate17-qq-quality-round`
(`report.md`, `sections/`, `evidence/`, `evidence/tools/`). Its findings are on code PR #9 does not touch; none is re-graded here.
**Gate 18 (PR #8 @ `4d6ed6e`, the runtime) is drafted but NOT launched at 14:08** (its brief still carries 7 unstamped placeholders; no `QA/Vision-gate18` pane,
`tmux list-panes -a`, READ-BY-DRAFTER). It may run BESIDE this gate: it is docker-heavy and owns `qa-g18-*` objects and `work-g18/`; **touch none of
them**, and never read its evidence as yours. Its report path, for the record only:
`/Volumes/Laptop-DEV/!CODING/Testing Agent MAIN/projects/vision/reports/2026-10-16-vision-gate18-qq-pr8-puppeteer25/`.
- **The ANCESTRY (READ):** `3dd15bc` (PR #6 merge, the LIVE v2.35 per Tuesday's 10-13 note) and `d030674` are ancestors of `e4ce536`.
- **Instruments are REUSED BY COPY** from gate 17's `evidence/tools/` (on the T9): `qa-run.py`, `mktree-qq.sh`, `lockcmp.py`, `lockwalk.py`,
  `tapsets.py`, `g17-run-suites.sh`, `g17-mutate.py`, `g17-heads.sh`, `g17-gh.sh`, `qa-g17-lib.mjs`, `qa-harness-g17-capture.mjs` (the hosted page's
  OWN Email POST, captured by interception), `qa-harness-g17-server.cjs` (the hosted server module's `createApp()` in-process with an in-memory store
  and a stub mail), `g17-hosted-render.cjs`, `qa-harness-g16-shots.mjs` (both themes through the drawer's own toggle, WCAG contrast from computed
  styles), `qa-chrome-egressblock.sh`, `qa-chrome-census.py`, `qa-egress-posctl.mjs`, `qa-floorcount.py`, `qa-harness-floorctl.mjs`,
  `qa-netlog-scan.py`. **COPY what you use into THIS gate's own `evidence/tools/` on /Volumes/Laptop-DEV, read it before you trust it, and RE-POINT
  every hard-coded path** (gate 17's copies hard-code `work-g17`, the gate-17 report folder, the T9 volume and the T9 QuickQuote repo — which is STALE
  and lacks `5f08fe0`). **Never edit, run from, or write into gate 1-18's copies, evidence or trees, on either drive.** Record the sha1 of each copy
  before and after your edits. `qa-run.py`'s copy asserts a 420 s ceiling: raise it to this brief's §13.6 ceiling in YOUR copy only, and say so.
- **Self-findings from earlier gates bind you:** quote every path (the project path has a space and a `!`; the repo sits under `Quoting Tool/`); run
  every loop and every `git show <sha>:<path>` under **bash, not zsh** (zsh reads `$H:s…` as a modifier); run `node strip.js` before any lone browser
  file; assert every tamper landed before reading its result; npm's update-notifier egresses unless you disable it; record the load average beside
  every timing number; `git branch` and `git for-each-ref` are NOT read verbs here.
- **PRIOR WORK: verify every claim against git history and the Actions API (GH-API-LEG), never against this brief.** The READY's PRIOR WORK line
  ("none on this guard (new)"; the defect measured in STATUS mails 02:10Z / 02:3xZ; QQ BACKLOG @ `fbd892e`) is re-derived or marked UNVERIFIED
  (`git cat-file -t fbd892e` in the repo; the mails per LEG7-METHOD).

## PIN — HEADS (parsed and verified by the launcher)
**The launcher enforces these rules:** every row has a 40-hex head and no `@`; the head is a commit; for QQGD the base is its single parent, an
ancestor AND the merge-base with MAIN; `git rev-list --count base..head` equals `commits`; `git ls-remote origin refs/heads/<branch>` equals the head
NOW **for BOTH rows — a moved main REFUSES (re-pin and re-brief)**; `refs/pull/9/head` equals the QQGD head NOW; QQGD is not on main and is 0 behind it.

<!-- PIN-HEADS:BEGIN -->
| id | repo | branch | head | base | commits | status |
|---|---|---|---|---|---|---|
| MAIN-Q | quickquote | main | e4ce5367761e03db982189a3f21758aa06714a85 | - | - | IN |
| QQGD | quickquote | fix/qq-email-print-mode-guard-2026-10-16 | 5f08fe035f39ddc13e8260de1dde0d5d623f18d5 | e4ce5367761e03db982189a3f21758aa06714a85 | 1 | IN |
<!-- PIN-HEADS:END -->

Both rows: `git -C <quickquote> ls-remote origin` read by the drafter at **2026-10-16 14:01:52 AEDT**: `refs/heads/main` = `e4ce536…`,
`refs/heads/fix/qq-email-print-mode-guard-2026-10-16` = `5f08fe0…`, `refs/pull/9/head` = `5f08fe0…`, `refs/pull/9/merge` =
`deb508193964aa2b2f1c84e2f1f58249240bfc59` (GitHub's test merge, NOTE only), `refs/pull/8/head` = `4d6ed6e…` (gate 18's target).
`rev-list --count e4ce536..5f08fe0` = 1; `5f08fe0..e4ce536` = 0; merge-base `e4ce536`.

Repo: quickquote = `/Volumes/Laptop-DEV/!CODING/Datasec/Vision_Sales_Portal/Quoting Tool/hpas-quoting-tool` (remote `datasecau/vision_hpas-quickquote`).
**The T9 copy of this repo is STALE. Never read it.** Its rules: the repo's own `CLAUDE.md` (read it at the head with `git show`; its deploy and
publish lines are NOT for you) and `/Volumes/Laptop-DEV/!CODING/Datasec/Vision_Sales_Portal/CLAUDE.md` (its QuickQuote section). **The builder's
checkout is LIVE (it is starting fix (2) there): never use the name `main` in the repo, always the pinned 40-hex sha; never read any working tree as
evidence; build every tree from the object store.** **If PR #8 merges before you finish, main moves:** your pins stay valid (they are shas), but say
so in the three readings and do NOT re-base anything — the verdict is on `5f08fe0` over `e4ce536`.

## WRONG OR UNVERIFIABLE IN THE COMMISSION AND THE READY — found by the drafter (verify each; all are claims)
- **(a) "Warning:" is a label, not part of Kam's sentence.** The READY lists "Warning: This email sends …" and "Armed button: Send standard pricing
  anyway". Kam's card `quickquote-guard-words-1016` quotes the warning starting at "This email sends …" (READ, `0_Brain/dashboard/data/decisions.json`,
  its `bluf`), and the code renders exactly that: `note.textContent = WARNING` with no prefix and no glyph. **The byte-equal target is W1 (220 bytes),
  NOT "Warning: " + W1.** A rendered "Warning:" prefix or ⚠ glyph would be a DIFFERENCE from Kam's words, never a match.
- **(b) The commit message carries W1 with ASCII quotes** (`Choose "Standard pricing only" above`, READ, `git log -1 5f08fe0`); the code and the test
  carry U+201C/U+201D. The commit message is not rep-visible; the RENDERED DOM is what §N4 measures.
- **(c) The builder's test never reaches the server, so "sends standard pricing anyway" is untested by it.** Its `/api/quote/email` stub records the
  POSTed state (`state.checks.pmCustom` / `pmBoth` = true) and answers a canned qnum. **What the customer receives after the second press is decided by
  the unchanged server path, not by the guard** — so §N3/§N7 run the hosted server module's own `createApp()` with the real `renderQuotePdf` and a
  capturing stub mail, and read the PDF and workbook that would have gone out.
- **(d) Programmatic print-mode changes fire no `change` event, so they do not disarm** (READ-ONLY-INFERRED, not measured). `index.html` sets
  `$("pmDefault").checked = true` WITHOUT dispatching an event in at least three paths (READ at `e4ce536`, lines ~3036 `btnReset`, ~3420-3421 when the
  custom ticket becomes empty (`cpState === null`, e.g. "Reset to default" `btnResetCustom`), ~3550-3551 `applyAdvanced(false)`). Armed in "custom",
  then one of those: the mode is silently "default" while the button still reads W2 and W1 stays on screen; the next press sends at once (mode
  default). The money is then correct (standard is what was chosen) but the screen is stale. The C-05 reopen path DOES dispatch `change`
  (`fire(el)`, `strip.js` ~330-345) and should disarm. **PROBE each (§N3.4), report what a rep sees; FAIL only if a send goes out in a custom mode on
  a press that was not preceded by W1 on screen for that mode.**
- **(e) A double-click sends.** Click 1 arms, click 2 sends (no delay, no debounce; READ). A rep who habitually double-clicks never reads W1.
  **MEASURE it (§N3.4, E1)** and report it as a finding for Tuesday/Kam (the words Kam approved say "press the button again"); it is not a FAIL of the
  head by itself.
- **(f) The new test's red claim needs the head TEST on base CODE.** "Red on main's code: 4 of 5 FAIL" can only be reproduced by running
  `test/email-print-mode.mjs` (blob `b1d4443`) inside a base-code tree (the base's `strip.js`, so `public/index.html` has no guard). The file does not
  exist at `e4ce536`. §N2 builds exactly that tree and names how.
- **(g) "CI 175/175" counts the whole `test:print`, not the new file alone**, and the READY's local count is on macOS Chrome 155 with Node 26.8.1,
  not CI's Node 22 (tests.yml, every job `node-version: 22`, READ). Base `test:print` = 170 per gate 18's reading of the same blobs; head = 170 + 5.
  §N6 proves it as SETS by test name (the 5 added names exact, 0 lost).
- **(h) A PUBLISH of `5f08fe0` would ship more than the guard.** Live is (expected, AZ-PRE-READ confirms) `v0.6.3-tool2.35-3dd15bc`. `git diff --stat
  3dd15bc 5f08fe0` = **4 files, +225/−18** (READ 14:1x): the guard's 3 files **plus PR #7's dependency round** (`git diff --stat 3dd15bc e4ce536` = 2 files, +21/−16:
  `stage3/package-lock.json` 34 lines, and `stage3/package.json` adding the `"basic-ftp": "^6.2.3"` override), which C-18 merged but did NOT publish, and which
  only Tuesday's tier-2 source check has covered (no QA gate). **C-20's grant is "the GUARD only".** Not this gate's ruling: §N8.3 lists the exact
  live-to-head delta (READ ONLY) so Tuesday can decide at PUBLISH GO whether PR #7's runtime change needs Kam's word or its own evidence. Your §N6/§N7
  runs DO exercise PR #7's installed tree (it is in both base and head), which is evidence you should name as such.
- **(i) The box is overloaded.** `uptime` at 14:08 read **load 184.10 / 226.20 / 234.67** (8-CPU M2), with eleven `Datasec/MPS-*` lanes,
  `Datasec/NexusAI-O`, `QA/NexusAI-batch23`, the Vision builder and fleet-monitor live (`tmux list-panes -a`, READ). The builder's own 320 px run
  timed out at load ~200 (READY NOT TESTED line 1). **Run ONE browser at a time, sequentially, never two Chromes of yours at once; every timing with
  the load; a cell past its deadline is NOT RUN with the load, never retried more than once.** If gate 18 is running beside you, it is contention,
  not a conflict.
- **(j) Session cookie is `Secure`** (`qqs=…; HttpOnly; Secure; SameSite=Lax`, READ, hosted server module ~:377). Chromium is expected to keep it on
  `http://127.0.0.1` (loopback is a secure context — drafter's expectation, UNMEASURED). If it does not, sign in by fetch and set the cookie by CDP, and
  SAY so; the page itself (button, warning, collector) is still the page's own.
- **(k) CodeQL on PR refs is a blind instrument** (gate 17 WRONG (a), measured by gate 17's control). The READY's "open code-scanning on refs/pull/9/head
  and /merge = 0" proves nothing alone. The check runs on `5f08fe0` read `CodeQL success "No new alerts in code changed by this pull request"`,
  `Analyze (javascript-typescript)` success, `Analyze (actions)` success (READ-BY-DRAFTER). Say only what they can show.
- **(l) The commission's times vs the board file.** Tuesday's commission and note say 13:25:51 (C-20) and 13:51:38 (words). `decisions.json` records
  `ruled_ts` 13:29:39 and 13:52:18 for the two cards (READ). The ruling TEXT and choice (a) agree everywhere; the gap is when the board file recorded
  it. Not load-bearing; cite C-20's time for C-20 and Tuesday's note for the words.
- **(m) This drive's QA project has no `projects/vision/`** (MEASURED, `ls`, 14:08). Gates 1-17 live only on the T9; gate 18 has not created one yet.
  Create only YOUR report folder and `work-g19/`; never touch `work-g18/` or gate 18's report folder if they appear.
- **Verified TRUE at source (READ 14:01-14:2x):** both heads + `refs/pull/9/head` by `ls-remote`; single parent `e4ce536`; 1 ahead / 0 behind;
  3 files, numstat 1/1, 28/1, 175/0 = the PR files API; the unchanged-blob list; the `test:print` line diff (only `test/email-print-mode.mjs` inserted);
  W1/W2 byte-equal between the card and `strip.js` and the test file; `printMode` radios `pmDefault`/`pmBoth`/`pmCustom` with values
  `default`/`both`/`custom` and the ADVANCED PM strip markers around `pmBoth`/`pmCustom` (`index.html` ~1670-1688); `.svc-warn` light and
  `html[data-theme="dark"] .svc-warn` rules exist (~1116-1124); `createApp({ … clock = () => new Date() })` (~255-271), so a frozen clock is an
  option; CI runs 38842678755 (push) and 38842703255 (pull_request): head_sha `5f08fe0…`, conclusion success, 5/5 jobs (print-fit, xlsx-parity,
  stage3-server, store-azurite, pricing-pack) success; Dependabot open #1 #4 (extract-zip, high — PR #8's business, not this PR's); main open
  code-scanning 0; C-20 present; gh-config mtimes unchanged by the drafter's GETs (12 Oct 18:09).

## THE READY — its claims and NOT TESTED (the gate rules on every claim)
Read the READY whole. Its NOT TESTED lines are carried VERBATIM here (the launcher checks it):

QQGD NOT TESTED
```
NOT TESTED / PENDING
- 320 px: my run timed out in the harness (settings-drawer wait) while this machine was at load average ~200: other sessions' builds (33 dotnet processes) plus my amd64 emulation. Not a verdict either way. I'll re-run it when the amd64 job ends and report in a STATUS.
- A real ACS send in a custom mode (the test stubs /api/quote/email; the posted body is asserted, the mail is not).
- The live site: the publish step's checks (rollback image read first, post-deploy checks, as for v2.35).
```

**The claims, in one line each (each a CLAIM, re-derived in §N):** 3 files; guard in `HOSTED_EXTRAS` only; first press in a non-standard mode does not
send, shows the warning, arms for THAT mode; second press sends standard pricing, unchanged; any print-mode change disarms and clears the warning;
"Standard pricing only" unchanged; offline `index.html` untouched; the text word for word as W1/W2; unchanged "Email me this quote (PDF & XLS)" and
"Sent — quote …"; styling = the existing amber `.svc-warn` box, light + dark rules, no new colours; red on main's code 4 of 5 FAIL for the right
reason (custom: POST on first press, actual 1 expected 0; both: same; switch-back: button never armed; no carry-over: second mode sent instead of
warning) with the control passing; 5/5 with the guard; local pricing 69/69, npm test 132/132, test:print 175/175, test:xlsx 6/6; CI 5/5 on
38842678755 and 38842703255 with "ok 10 - guard (custom)…", "ok 11 - guard (both)…", "ok 14 - control…", "# tests 175"; CodeQL pass; MERGEABLE;
1280 px light + dark screenshots legible; 375 px light + dark no sideways scroll, button text fits.

**How you treat these:** every NOT TESTED line you CAN test, you test: **320 px** (light and dark, after the first press) is §N3.5 — run it, sequentially,
at the load you record. **A real ACS send** stays NOT TESTED (no real mail, ever); its nearest substitute is §N7: the real server path with a
capturing stub mail, which reads the PDF and workbook that WOULD go out — say it is a substitute. **The live site** stays NOT TESTED (publish-time).

## 2a. LEGITIMATE SHAPES — the guard IS a checker (it intercepts a rep's action), so its legitimate shapes are tabled here
**The guard's failure path is NOT destructive (it withholds one send and shows text), but a false alarm on the ordinary shape (standard mode, and every
simple-mode session) would block the commonest action of every rep. Every row below is MEASURED in §N3; until it is, the instruction on any unexpected
result is STOP and record it, never a remedy.**

| shape — its ordinary form, as a rep really produces it | expected | the code clause that yields it | predicted-by |
|---|---|---|---|
| simple (non-advanced) session, any currency, Email once | sends on ONE press, no W1, label unchanged | `pmBoth`/`pmCustom` are stripped from the simple build, so `printMode()` = `default` | drafter |
| advanced session, "Standard pricing only", Email once | sends on ONE press, no W1 | `mode === "default"` → skip the guard | drafter |
| advanced, "Custom pricing only", Email | press 1: no POST, W1, W2; press 2: one POST, standard PDF + xlsx | `mode !== "default" && armedFor !== mode` → arm, return; then `armedFor === mode` → send | drafter |
| advanced, "Standard + custom pricing", Email | same as custom | same | drafter |
| armed in custom, rep clicks "Standard pricing only" | disarmed: label back, W1 cleared, `svc-warn active` removed; one press sends | `change` listener, `e.target.name === "printMode"` → `disarm()` + `note.textContent = ""` | drafter |
| armed in custom, rep clicks "Standard + custom" | disarmed; press 1 warns again | same listener, then not armed for `both` | drafter |
| armed in custom, rep edits the quote (devices, term, currency, customer) and presses | sends (still armed for custom; W1 still on screen) | no listener on other inputs | drafter |
| armed, the send fails (server error) | "Send failed: …"; next press in custom warns again | `disarm()` ran before the send | drafter |
| the defect class: custom/both, first press | MUST NOT send | the `return` | drafter |

## N1. THE DIFF, REVIEWED AGAINST THE READY'S CLAIMS (READ ONLY)
**FAIL condition, stated BEFORE the read:** any line of the delta not explained by the READY; any change outside `HOSTED_EXTRAS` in `strip.js`; any
change to what the collector POSTs (field set, field names, the `NOT_QUOTE` set, the body shape); any change to the `/api/quote/email` request; the
send path after `disarm()` not byte-identical to base's handler body; a dependency line in `package.json`.
1. `git diff e4ce536 5f08fe0` whole, quoted into `evidence/`; per file, every hunk mapped to a READY claim (table: hunk, claim, holds yes/no, how).
2. Confirm by extraction that the click handler from `btn.disabled = true;` to the end of the handler is byte-identical at base and head (bash +
   python over `git show <sha>:stage3/strip.js`; say how you delimited it).
3. Confirm `printMode()`'s selector and `default` fallback match `index.html`'s own reads (~2998, ~3420) and say what it returns when no radio is
   checked.
4. Read the PR files API (`gh api repos/datasecau/vision_hpas-quickquote/pulls/9/files`) and show it equals `git diff --numstat` (3 rows, blobs).
5. The `package.json` change: `git diff -U0` shows ONLY the `test:print` line; prove the dependency maps (`dependencies`, `devDependencies`,
   `overrides`) are identical by JSON parse at both shas.

## N2. THE RED-PROOF — the new test fails on main `e4ce536` for the RIGHT reason and passes at `5f08fe0` (MEASURED; never trust the mail; WRONG (f))
**FAIL condition:** the new test passes on base code (it would then not test the guard); a base failure for a reason other than the guard's absence
(setup error, drawer timeout, "the custom ticket never took the -10% price", Chrome launch); the standard-mode control failing on base; any of the 5
cells failing at the head on a clean tree.
1. **Base-code tree:** a fresh `git archive e4ce536` extraction (`mktree-qq.sh`, re-pointed) with `npm ci --offline --ignore-scripts` and the lockfile
   proven entry by entry (`lockcmp.py` AND `lockwalk.py`); then add ONLY `stage3/test/email-print-mode.mjs` from `git show 5f08fe0:…` (blob
   `b1d4443`, sha1 asserted after the copy — the tamper asserted landed); `node --check` the file (rc 0; a test that does not parse is VOID); run
   `node strip.js && node --test test/email-print-mode.mjs` from `stage3/` under `qa-run.py` with `PUPPETEER_EXECUTABLE_PATH` = YOUR egress wrapper.
   Quote every `not ok` with its assertion message. **Expected (the READY's claim, to be falsified):** custom and both fail with `posted.length`
   actual 1 expected 0; switch-back fails because the button never reads W2; no-carry-over fails because the second mode sends; the control passes.
2. **Head tree:** a fresh `git archive 5f08fe0` extraction, same install and proof; the same file alone: 5/5. Then the same file x2 more (3 runs) to
   see flakiness at this load; report each run's wall time with the load.
3. **Mutants (each on a FRESH head tree, tamper asserted landed, `node --check strip.js` rc 0, `node strip.js` rc 0 and the mutated text present in
   the generated `public/index.html`):**
   - **G19-M1** delete the `return;` after the arming block (the guard warns AND sends): which cells fail? (expected: custom, both, no-carry-over)
   - **G19-M2** delete the document `change` listener (no disarm on mode change): which cells fail? (expected: switch-back)
   - **G19-M3** change W1 by ONE character in `strip.js` only (`“` → `"`): which cells fail? (expected: custom, both, no-carry-over via `assert.equal(note, WARNING)`)
   Say which cells see each, or NONE. A mutant no cell sees is a FINDING against the test (strength), not a FAIL of the head.

## N3. THE REAL-BROWSER DRIVE OF THE HOSTED PAGE'S ADVANCED SESSION (TIER 1; MEASURED; ONE browser at a time)
**FAIL condition:** in "Custom pricing only" or "Standard + custom pricing", ANY first press that POSTs or that the stub mail receives; a second press
(same mode, armed) that does NOT send exactly once; any print-mode change by the rep's click that leaves the button armed or W1 on screen; in
"Standard pricing only" or a simple session, a press that does not send on ONE press; W1 or W2 rendered other than byte-equal (§N4); a page error or
console error at the head that base does not also produce for the same steps.
1. **Instrument (PRIMARY — the real server path):** on the host, YOUR harness `require`s the head tree's own hosted server module's `createApp()`
   export (NEVER its entry point, NEVER with a real secret): the repo's in-memory store and a CAPTURING stub mail (READ how
   `stage3/test/server.test.mjs` builds them, ~100-160, and copy that shape — `qa-harness-g17-server.cjs` already does), a throwaway `sessionSecret`
   of 48 random chars and a throwaway `unlockSecret` (fresh random; never the HPAM word), the tree's OWN `renderQuotePdf` from `lib/pdf.js` with
   `PUPPETEER_EXECUTABLE_PATH` = your egress wrapper, `clock` FROZEN (an option of `createApp()`; prove it froze), `trustForwardedFor: false`,
   listening on 127.0.0.1 on a kernel-chosen port, under `qa-run.py` (`env -i` allowlist). Then ONE Google Chrome (your egress wrapper) driven by the
   tree's puppeteer-core loads `http://127.0.0.1:<port>/login`, signs in with the OTP the stub mail captured, opens Settings, turns on Advanced, types
   the throwaway word and presses Unlock (the page's own controls), closes the drawer, fills the form as a rep would (40 devices, 3 years, the full
   bundle, customer `Guard & <Probe> "QA" 'g19'`, currency AUD), enters a custom price the rep's way ("% from standard" `-10`, Apply), picks the print
   mode by clicking its LABEL, and presses the page's own Email button. Record per press: POSTs seen by the server (count + body), mails captured
   (count + attachments), `#emailPdfNote` textContent and classes, `#btnEmailPdf` textContent and `disabled`.
   **SECONDARY (say which rows used it):** the builder's interception method (`http://qq.test`, stubbed unlock/module/email) or gate 17's
   `qa-harness-g17-capture.mjs` — allowed for the edge probes and the phone widths if the primary is too slow at this load, labelled "stubbed server".
   **Base is driven the same way** (fresh base tree), so every row has a base column.
2. **The required grid (head AND base):** S1 standard: 1 press. S2 custom: press 1, press 2. S3 both: press 1, press 2. S4 custom armed → click
   "Standard pricing only" → state read → press. S5 custom armed → click "Standard + custom" → press (warns again, 0 POST). S6 custom armed → click
   standard → click custom → press (warns again). S7 a SIMPLE (never-unlocked) session, AUD, 1 press. **Expected at base:** S2/S3 send on press 1 —
   that IS the defect, reproduced (the base column is the red). **Every row records the load.**
3. **Both themes, the warning on screen:** at 1280 px, after S2's press 1 and after S3's press 1, switch the theme with the page's own visible
   toggle (after it settles — gate 16 SF-3/SF-4) and screenshot light AND dark (head only; base has no warning). Compute W1's text colour against
   the `.svc-warn` background from computed styles (WCAG contrast ratio) in both themes, and say whether W2 fits its button without clipping
   (`scrollWidth <= clientWidth`). Look at each screenshot yourself and say in one line what a rep sees.
4. **Edge PROBES (head; MEASURED; findings, not FAILs unless they hit §N3's FAIL condition):** **E1** double-click the Email button in custom
   (`click({ clickCount: 2 })` and two clicks 100 ms apart): POSTs? (WRONG (e)). **E2** armed in custom → the page's "Reset to default" for the custom
   price (`btnResetCustom`): mode now? label, W1, classes? then press: POSTs? (WRONG (d)). **E3** armed in custom → turn Advanced off in Settings: same
   reads. **E4** armed in custom → "Reset form" (`btnReset`): same reads. **E5** armed in custom → keyboard: Tab to the button, Enter: sends? **E6**
   armed, then a send that fails (make YOUR stub mail throw once): the note, then press again in custom: warns again? **E7** is W1 announced to
   assistive tech (any `aria-live`/`role` on `#emailPdfNote` or an ancestor)? READ + MEASURED from the DOM. **E8** reload while armed: state after.
5. **Phone widths (the READY's NOT TESTED line 1):** 375 px and 320 px, light and dark, after S2's press 1: page `scrollWidth <= innerWidth`, W1 and
   the button inside the viewport, W2 fits. Sequential, one browser, deadline per cell; NOT RUN with the load if it overruns once and its retry too.

## N4. KAM'S WORDS, BYTE FOR BYTE (TIER 1; MEASURED)
**FAIL condition:** the rendered warning or the armed label not byte-equal to W1 / W2; any visible prefix, suffix or glyph added to either; W1 visible
in "Standard pricing only"; the unchanged strings ("Email me this quote (PDF & XLS)", "Sent — quote <qnum> is on its way to your inbox.") changed.
1. From the LIVE DOM of §N3 (head, S2 and S3 after press 1): `#emailPdfNote.textContent` and `#btnEmailPdf.textContent` RAW (not trimmed), and their
   `innerText` (what CSS renders, e.g. `text-transform`), each UTF-8 encoded: byte length and sha256, compared with W1 (220, `0d5beedb…eb25b9`) and W2
   (28, `4c73c159…3ec797d`). Hex-dump the bytes around the two curly quotes. Any leading/trailing whitespace difference is reported.
2. Static (READ): extract `WARNING` and `ARMED_LABEL` from `git show 5f08fe0:stage3/strip.js`, from the head test file, and from the generated head
   `public/index.html` (after `node strip.js`), and compare all three with W1/W2 by sha256.
3. **Control that can fail:** the same comparator over a copy of W1 with one straight quote substituted must report UNEQUAL before its EQUAL is
   believed.
4. The default label and the "Sent — quote" line at head = base (from §N3's S1).

## N5. THE OFFLINE `index.html` UNCHANGED (TIER 1 by the customer's printed quote; READ + MEASURED)
**FAIL condition:** `git diff e4ce536 5f08fe0 -- index.html` non-empty; the generated `private/advanced.js` or `private/svc.js` differing base vs head;
the generated `public/index.html` differing from base anywhere except inside the `HOSTED_EXTRAS` script.
1. `git diff e4ce536 5f08fe0 -- index.html` (must be empty; quote the empty output and the rc) and `rev-parse` both blobs (`447b129`).
2. Run `node strip.js` in a fresh base tree and a fresh head tree; sha256 + byte count of `public/index.html`, `private/advanced.js`,
   `private/svc.js` at both; `diff` the two `public/index.html` files and show every differing line lies inside `HOSTED_EXTRAS`.
3. Say whether the guard can appear in the offline/printed quote at all (READ: is `HOSTED_EXTRAS` ever injected into the root `index.html` or the
   print path?).

## N6. THE REPO'S CI SUITES, AS CI RUNS THEM, AT `5f08fe0` (and base) — as SETS, NOT COUNTS (TIER 1)
**FAIL condition:** any suite red at `5f08fe0` on a clean tree; a test NAME passing at `e4ce536` that does not pass at the head; `test:print`'s added
names other than exactly the 5 cells of `email-print-mode.mjs`; `npm ls --all` rc ≠ 0 at the head; any installed package not byte-equal to the
lockfile's integrity.
1. **Trees:** the §N2 base and head trees are separate from these (one purpose each): fresh `git archive` extractions of `e4ce536` and `5f08fe0`
   under `projects/vision/work-g19/`; `npm ci --offline --ignore-scripts` (a cache miss FAILS, then NOT RUN with the tarball named); lockfile proven
   entry by entry (`lockcmp.py` AND `lockwalk.py`); `npm ls --all` rc and stderr.
2. **The suites by PATH and command (tests.yml at the head, READ):** root `node --test quote-engine.test.mjs` (READY 69); in `stage3/`: `npm test`
   (132), `npm run test:print` (175 head / 170 base), `npm run test:xlsx` (6). Each ×1 at base and ×2 at the head, same session, as SETS by test NAME
   (`tapsets.py`): lost (must be empty), added (must be exactly the 5), removed, duplicates. **Host Node is v26.8.1, not CI's 22: say so on every
   row.** Every Chrome under YOUR egress wrapper. `npm run test:azurite` (store-azurite) is NOT RUN here (no docker; `lib/store.js` and its test are
   unchanged blobs) — relay CI's `store-azurite` success on `5f08fe0` as READ ONLY.
3. Never `npm install`, never `npm audit fix`. The lockfile is an unchanged blob: no `npm audit` is required (say so).

## N7. THE GUARD DOES NOT CHANGE WHAT IS EMAILED (TIER 1; MEASURED through the real server path of §N3.1; WRONG (c))
**FAIL condition:** in "Standard pricing only", the head's emailed PDF or workbook differing from the base's for the same inputs (text, money figures,
pixels, pages, fonts; workbook parts other than `docProps/core.xml`); the head's POSTed state differing from the base's for the same filled form
(the guard adds no input with an id, so the collector's field set must be identical); after the second press in custom or both, the emailed PDF
carrying ANY figure that is not standard pricing (the warning W1 says "sends standard pricing only" — that claim must be TRUE), or differing from
the standard-mode email for the same inputs other than in the posted `pmCustom`/`pmBoth` checks' consequences you name.
1. **Method per LEG7-METHOD (D5, appended by the launcher).** GATE-METHOD: for each pair, `pdftotext -layout` full-text diff (frozen clock and the
   qnum normalised only if it differs — say so), the MONEY-FIGURE MULTISET (every currency amount token, e.g. `A$`, `US$`, `CA$`, `$` followed by
   digits, extracted by a regex you state) compared exactly, `pdftoppm -r 100` pixel diff per page in plain python on PPM (no ImageMagick, PIL or
   numpy here), `pdfinfo` pages + A4, `pdffonts` set; workbook: unzip both, diff every part. STATUS-MAILS: read the saved mails whole, state the
   builder's method, re-derive its numbers (A$50,383 emailed vs A$46,215 printed in the measured case, per the board card) on YOUR trees, AND run the
   GATE-METHOD rows.
2. **Pairs (minimum):** standard mode, base vs head, × {AUD, USD, CAD} (FX: the page's FX calls are blocked by your wrapper, so the seeded table
   applies; record the rate line on each PDF and confirm base = head); head custom-press-2 vs head standard (AUD); head both-press-2 vs head standard
   (AUD). **The subset check:** every money figure in each emailed PDF appears in the PRINTED "Standard pricing only" quote of the same state (print
   via the page's own Print control with the print media type, A4), and the custom total of the PRINTED "Custom pricing only" quote does NOT appear
   in the email. Quote the figures.
3. **Controls that can fail:** a planted one-word and one-pixel change must make your comparator report non-zero before its zeros are believed; the
   base column of S2 (custom, press 1 sends) must show the emailed figure ≠ the printed custom total (the defect, reproduced) before "head email =
   standard" is read as the guard's claim being true rather than as an instrument that cannot see custom pricing.
4. Record the server's JSON answer per send (qnum, `unknownFields`, `clearedChecks`). The 7 unknown print-mode fields (`pmBoth`..`cpPct`) are
   PRE-EXISTING (Tuesday's 2026-10-16 12:37/12:57 reading for PR #7); report them per render at base AND head, never as PR #9's.

## N8. NOTHING PUSHED, MERGED OR PUBLISHED; LIVE SITE UNCHANGED (commission; READ ONLY)
**FAIL condition:** any `git push`, merge, PR comment/review/label/approval, workflow re-run, alert dismissal, `docker` command of ANY kind, `az`
command, or deploy in your command log; any write in the QuickQuote repo or in `Vision_Sales_Portal/`; the live webapp's `linuxFxVersion` at verdict
(Tuesday's re-read) differing from AZ-PRE-READ without an explanation that is not you.
1. **Your own discipline, MEASURED:** your shell history for this session grepped for `push`, `merge`, `docker`, `az `, `gh pr`, `-X` (quote the zeros
   beside a positive control — the same grep over a scratch file that contains each word reads 1); `git -C <repo> status --porcelain` is NOT a read you
   make (it can refresh the index); instead `stat` the repo's `.git/index` mtime at start and end and say only whether YOU could have touched it.
2. **The Azure side (AZ-READ-LEG = TUESDAY-READS):** RELAY the `AZ-PRE-READ` line appended to your prompt; say the post-read is Tuesday's at verdict.
3. **What a publish of `5f08fe0` would ship (READ ONLY, WRONG (h)):** from the AZ-PRE-READ tag's trailing sha (e.g. `…-3dd15bc`), `git log --oneline
   --first-parent <live>..5f08fe0` and `git diff --stat <live> 5f08fe0`, and name every file outside the guard's three (expected: PR #7's
   `basic-ftp` override in `stage3/package.json` + `stage3/package-lock.json`). If the tag carries no sha, say UNMEASURED. No recommendation beyond naming it.
4. **Deploy-on-merge (READ ONLY):** `.github` at the head holds only `tests.yml` (no deploy, no image build, no registry login); if GH-API-LEG allows:
   repo hooks, environments, deployments. State whether a merge deploys anything, with each statement's evidence class.

## N9. CI AND CODEQL ON PR #9 (READ ONLY; never caused)
**FAIL condition:** a tests.yml run on `5f08fe0` not `success` on all five jobs; a CodeQL check run on `5f08fe0` failing; any alert dismissed.
1. GH-API-LEG = READ-ONLY-VISION-TOKEN: `actions/runs/38842678755` and `/38842703255` (head_sha, conclusion) and their `/jobs` (five names, each
   `success`); the print-fit job's LOG lines the READY quotes ("ok 10 - guard (custom)…", "ok 11 - guard (both)…", "ok 14 - control…", "# tests 175")
   via `gh api …/actions/jobs/<id>/logs` (a GET; if the shim or GitHub refuses, NOT RUN); `commits/5f08fe0…/check-runs`; `code-scanning/alerts?state=open`
   count on main. Otherwise NOT RUN.
2. **What CodeQL can say (WRONG (k)):** the PR-side zeros are blind. Name the post-merge reads: main's code-scanning still 0 open, tests.yml green on
   the merge commit.

## 12. The merge and the queue
QQGD is 1 ahead and 0 behind `e4ce536`, so a GitHub merge commit's tree equals `5f08fe0`'s (`dc6aef6`) while main stays at `e4ce536` — prove 0 behind
with `rev-list --count`; run `git merge-tree --write-tree` only from YOUR OWN object dir, or skip it and say so. **If PR #8 (gate 18) merges first,
PR #9 must be re-merged over a moved main: name the cells to re-run then** (at least: §N6's four suites, §N2's 5 cells, §N3's S1-S3 on the merged
tree). **Cells to re-run at merge:** tests.yml's five jobs on the merge commit. **At publish (Tuesday's PUBLISH GO under C-20; not this gate):** the
built image's `public/index.html` carrying W1/W2 byte-equal, one custom-mode press on the live page showing W1 and NOT sending (the publish's own
post-deploy check), the rollback tag kept.

## 13. FLOOR AND PORT DISCIPLINE — Vision has NO jest lock, plus THE DEADLINE RULE (and HELD)
**There is no shared lock or queue on this project, and you must NOT borrow NexusAI's** (its jest/docker lock serialises NexusAI seats only).
1. **Never use `4848` (portal), `8080` (QuickQuote's stage3 dev port) or `47787` (Tuesday's dashboard)** on the host. Host product processes take
   ports from the kernel and bind `127.0.0.1`. **Never start the hosted server module's own entry point; use its `createApp()` export.**
2. **Every host product process runs under `env -i` with an explicit ALLOWLIST** (PATH; HOME = a fresh mktemp dir; NODE_ENV = `test`, never
   `production`; `PUPPETEER_EXECUTABLE_PATH` = YOUR egress-block wrapper; `npm_config_update_notifier=false`; `npm_config_offline=true`;
   `npm_config_cache` = the user cache, read for `npm ci --offline` only). **NEVER set in a product process:** `AGENTMAIL_API_KEY`, `AGENTMAIL_INBOX`
   (with both set, QuickQuote SENDS FOR REAL), any real `ACS_*` / `MAIL_SENDER`, `TABLES_CONNECTION_STRING`, `SALES_COPY_EMAIL`, `HPAM_WORD`,
   `ADVANCED_UNLOCK_SECRET`, `SESSION_SECRET`, `WEBSITE_SITE_NAME`, `GH_TOKEN`, `GITHUB_TOKEN`. Print each product process's env KEY NAMES (never values)
   and assert none is forbidden. `NTFY_SERVER=http://ntfy.invalid`; never contact ntfy.sh.
3. **EGRESS INCLUDING CHROME CHILDREN:** the page calls three public FX APIs whenever the currency is not USD. Every Chrome runs under YOUR copy of
   the egress-block wrapper; prove the block with its positive control (`qa-egress-posctl.mjs`) and run the net-log scan at the end; record
   GoogleUpdater and chrome_crashpad_handler at start and end (`qa-chrome-census.py`).
4. **Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid** (`qa-floorcount.py`, copied): "ours" = the ancestor chain CONTAINS your
   claude pid. **Negative controls, same run, must classify FOREIGN.** The launcher DERIVES the negative-control seats live from the cockpit panes
   (the `tuesday` pane, the `Datasec/Vision_Sales_Portal` builder pane, and any live `QA/*` / `fleet-monitor` pane) and appends them to your prompt.
   **A zero is reportable only beside a control that fired in the same window.** **Record the 1-minute load beside every timing.**
5. **ONE BROWSER AT A TIME (WRONG (i)).** Never two Chromes of yours alive at once (the `test:print` suite's own Chromes count as yours); never run a
   suite and a §N3 drive concurrently. Never `docker` anything.
6. **THE DEADLINE RULE:** every step has a written DEADLINE built into your runner (no `timeout` binary here) and a client timeout on every request;
   a step past its deadline is ABORTED and reported. Deadlines: one browser cell 120 s (§N3, §N4, §N7 each render); one §N2 arm 420 s; root pack
   120 s; a whole `npm test` 300 s; a whole `test:xlsx` 300 s; a whole `test:print` 900 s; nothing above 900 s. One retry per cell at most, then NOT
   RUN with the load. **Every Chrome, page, child, app server and temp profile you start is released in a `finally`.** **Log a HEARTBEAT line
   (timestamp, step, pid, elapsed, load) at least every 2 minutes; a step with no heartbeat for 5 minutes is aborted and reported.**

**Reap everything you start.** An orphan Chrome or listener of yours is someone else's foreign process.

### Drivable surface — LOCAL ONLY. **NEVER the live QuickQuote or the live portal.**
- **NEVER the live** QuickQuote (`hpas-quickquote`, `hpas-quickquote-rg`, `hpasqqacr`, its Table Storage, its log workspace) and **NEVER the live**
  portal (`https://datasec-sales-portal.azurewebsites.net`, resource group `datasec-sales-portal-rg` — PRODUCTION). **No HTTP request to either, not
  even a GET. No az at all — no writes, no app-setting change, no deploy, no publish, no ACR build, no ACR push.** Never the FX hosts (blocked by your
  wrapper), never ntfy.sh. **Never Claude in Chrome** (Kam's real Chrome with his sign-ins). Never open anything under
  `Vision_Sales_Portal/4_Credentials/` (the launcher wires the gh config itself; you never read its files), never type an HPAM word, and never read
  the builder's `guard-2026-10-16-evidence/` as evidence (you may LOOK at its screenshots to compare with yours; say so).
- **Network, and ONLY this:** `git ls-remote origin` (head readings); `gh api` GETs (GH-API-LEG). Nothing else reaches the internet: no npm registry
  (`npm ci --offline`), no `npm audit`, no image pulls.

### HELD
- No merge, no deploy, **no publish**, **no registry push**, **no production**, no money, **no mail to any human**, no external comms. **No comment,
  review, label, approval or status on PR #9, PR #8 or any GitHub object; no re-run of any workflow; no alert dismissal of any kind.**
- **No `docker` at all, no `npm install`, no `npm ci` without `--offline --ignore-scripts`, no `npm audit fix`, no `npx` of anything not already in your
  tree. `gh` only as GH-API-LEG allows; no `az`.** The launcher points `AZURE_CONFIG_DIR` at an EMPTY directory.
- **Trees:** build every tree INSIDE YOUR OWN PROJECT from the object store (`git -C <repo> archive <sha> | tar -x -C <fresh mktemp -d under
  projects/vision/work-g19/>`, in `/Volumes/Laptop-DEV/!CODING/Testing Agent MAIN`). **Each tree is EXCLUSIVE to this gate and to ONE purpose; never
  touch any other `work*` directory on either drive** (`work-g18/` included). In the repo use ONLY read verbs (show, log, diff, ls-remote, rev-parse,
  ls-tree, cat-file, grep, merge-base, archive); **never fetch, pull, checkout, switch, worktree, commit, stash, reset, clean, gc, branch or
  for-each-ref.** `merge-tree --write-tree` only from your OWN object dir.
- **CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY:** every control is a separate measurement that could have come out the other way on its own. **For this
  gate: the base column must reproduce the defect (S2/S3 send on press 1) before the head's "does not send" is read as the guard's doing; the byte
  comparator must report UNEQUAL on a one-character substitute; the PDF comparator must report non-zero on a planted one-word and one-pixel change;
  each mutant must be shown to have LANDED (in the generated `public/index.html`) before its result is read; the egress block's positive control
  fires; the floor count rises on its attached control.**
- **Findings only:** do not commit, do not move any branch, do not file a ticket. **Make no writes in the QuickQuote repo** (its working tree is the
  builder's, live) **and none inside `Vision_Sales_Portal/`**, none in gate 1-18's report folders or trees on either drive. Describe fix-shapes in prose.
- **NEVER `rm`.** Quarantine instead.

## THE MODEL RULE
(Kam, live board 2026-09-30 09:07, card `nexusai-gate11-opus55-safeguard-model-switch`, option (b) — QA gates may switch to Opus 4.8 when flagged,
PER SESSION.) You start on Opus 5.5 (the launcher reads the model id from Tuesday's `0_Brain/dashboard/data/models_latest.json`, `claude-opus-5-5` at
drafting). You run the FULL rows. If one of your responses is stopped by the safeguards: that step is NOT RUN (never re-worded to slip past); write ONE
line to `evidence/classifier-stops.txt`; reap any Chrome and app server you started; mail `tuesday-agent@agentmail.to` with the subject exactly
`[QA/Datasec-Vision -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch`;
then end your turn with the line `PARKED: flagged — awaiting the Opus 4.8 switch` and wait. Tuesday switches THIS pane's model and taps you by mail. You
never answer the model dialog yourself, and nobody ever chooses "Switch automatically". After the switch, resume at the stopped row. The report states
which rows ran on which model, with the switch time, and quotes `classifier-stops.txt` whole.

## TUESDAY'S RULINGS AT STAMP (2026-10-16)
**R1-R8 are the commission's requirements as Tuesday wrote them to the drafter (2026-10-16 ~14:0x), carried as ruling lines. Apply them; do not
re-rule them.**
- R1: ONE gate, TIER 1 (quote output to customers) on QuickQuote PR #9 @ 5f08fe0, Kam's C-20 (card quickquote-email-sends-standard-not-custom-1016 = a, 2026-10-16 13:25:51 AEDT, "Publish the guard as soon as it passes the gate, full fix after"); words approved on card quickquote-guard-words-1016 = a (13:51:38).
- R2: Diff review against the READY's claims; the PR files API confirms no dependency or Dockerfile change, so no image is built.
- R3: The red-proof: the new test fails on main e4ce536 for the right reason and passes at 5f08fe0 — run it, do not trust the mail.
- R4: A real-browser drive of the hosted page's advanced session in all three print modes x Email, both themes for the warning screenshot: standard sends on one press; custom and both warn first then send standard on the second press; switching mode disarms.
- R5: The warning and the armed button text byte-equal to Kam's approved sentences (curly quotes included).
- R6: The offline index.html unchanged (diff empty); the repo's CI suites as CI runs them (npm test, test:print, test:xlsx) at 5f08fe0.
- R7: The guard does not change what is emailed in standard mode (emailed PDF figures equal main's).
- R8: Nothing pushed, merged or published; live linuxFxVersion unchanged (Tuesday reads it). Findings-only. Round 1 of 2. Machine load is high: browser runs single and sequential.

**Drafter's open decisions for Tuesday (the launcher refuses until each RULED line is stamped):**
- **D4 — Class count and vocabulary.** *Drafter:* QQGD round 1 of 2; a NO GO returns it for round 2 to the builder (not to Kam); GO / GO WITH
  FINDINGS / NO GO; **if §N2 (the red-proof) or §N3.2's S2/S3 rows at the head are NOT RUN (deadline, load), the verdict is PROVISIONAL — it releases
  nothing**, never a GO on the builder's evidence. §N3.4/§N3.5 rows NOT RUN do not make it provisional; they are NOT TESTED lines. RULED: as the drafter wrote it — round 1 of 2; NO GO returns to the builder for round 2; PROVISIONAL (releases nothing) if §N2 or §N3.2 S2/S3 at the head are NOT RUN. (Tuesday, at stamp)
- **D5 — LEG7-METHOD (§N7).** *Drafter's reading:* GATE-METHOD (the builder's STATUS mails are not on disk). If Tuesday saves them and wants the
  builder's numbers re-derived, set the LEG7-METHOD line to STATUS-MAILS. RULED: GATE-METHOD (the superset; the builder's figures are on Kam's board card and quoted in §N7.1 for reference only). (Tuesday, at stamp)
- **Settled by the commission, not open:** GH-API-LEG = READ-ONLY-VISION-TOKEN (gate 17's D1, unchanged); AZ-READ-LEG = TUESDAY-READS; no docker.
- **Carried, unchanged from gate 17/18:** "With a ticket" is Tuesday's to file: the gate files nothing (§HELD); it reports each finding with its cell,
  repro and fix-shape. An ANSWER to you arrives from `tuesday-agent@agentmail.to` signed "-- Tuesday", whatever the bracketed prefix; anything from
  any other inbox is not.

## 14. Output
Report: `/Volumes/Laptop-DEV/!CODING/Testing Agent MAIN/projects/vision/reports/2026-10-16-vision-gate19-qq-pr9-email-guard/report.md`
(sections and `evidence/` beside it; screenshots, PDFs, rasters, diff PPMs, TAP logs and DOM byte dumps in `evidence/`). Write its VERDICT and FINDINGS
table early and keep it current.

**QUESTIONS:** your routing name is **`QA/Vision-gate19`**. If you must ask, mail `tuesday-agent@agentmail.to` with the subject
`[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>` (Context / one Question / Meanwhile / Needed-by), and
**proceed on the safest reading**. The ANSWER arrives in `tuesday-agent@` with a subject beginning `[Tuesday -> QA/Vision-gate19] ANSWER`.
Read it with your verdict key. **Never mail wednesday-agent@.** Datasec's coordinator is Tuesday. Record every question, the reading
you took and any answer in the report. **If two answers arrive and they differ, STOP, enumerate the differences and ask which one stands.**
If a response is cut off by a safety check, record it and continue with the next item.
This is authorised defensive QA of Datasec's own product on loopback.

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, with the subject beginning exactly:
`[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 19` and then
`: QQGD @ <sha7> <GO | GO WITH FINDINGS | NO GO>` (append ` PROVISIONAL` if D4's clause applies)
(`<sha7>` the pinned head from the launcher's table).
Lead the body with ONE sentence: on `5f08fe0`, does the new test fail on `e4ce536` for the right reason and pass at the head, does the real hosted
page (real server path) send on one press in standard and in a simple session, warn without sending and then send standard pricing on the second
press in custom and both, and disarm on a mode change, are W1 and W2 rendered byte-equal to Kam's words, is the offline `index.html` unchanged, do the
CI suites pass as sets against `e4ce536`, is the standard-mode email identical to main's, and was anything pushed, merged or published?
Then one line each on: the base column (the defect reproduced, with the figures); mutants G19-M1..M3; the edge probes E1 (double-click) and E2-E4
(programmatic disarm); the phone widths; the live site read (RELAYED from AZ-PRE-READ); what a publish would ship (§N8.3); the class count (round 1:
a NO GO goes to round 2). You have no inbox that wakes you, so a verdict you do not mail is lost.

AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/Laptop-DEV/TUESDAY/4_Credentials/.env`. The path is absolute because the QA project has no
credentials directory of its own. Use the key ONLY in your own verdict/question/answer-read `curl`, with a client timeout (`-m 30`). It must never enter
a product process's environment. **Never put the key, or any secret, in a mail or the report.**

Verdict format:
- **One verdict, GO / GO WITH FINDINGS / NO GO (PROVISIONAL per D4)**, naming the pinned sha and the branch: §N1's hunk table, §N2's red/green table
  with the quoted failure messages, §N3's grid (row × base/head × POSTs/mails/note/label/load), §N4's byte table, §N5, §N6 as sets, §N7's comparison
  table, §N8, §N9, row by row.
- The verbatim strings: the rendered W1/W2 bytes (length + sha256), the base red messages, each mutant's failing cells, the E1 POST count, the
  emailed figures (base, head, custom-press-2) beside the printed custom total, the AZ reading "RELAYED from AZ-PRE-READ".
- **A table with one row per §N item: MEASURED / NOT TESTED / NOT RUN / VOID, and HOW (command, tree, browser, port, load).** No row without a HOW.
- **Rule 2: what you did NOT test is first-class output.** A NOT TESTED section covering at least **the guard inside the published image (no docker by
  design)**, **a real ACS send in a custom mode (stub mail only)**, **the live site (publish-time)**, **CodeQL's verdict (blind pre-merge, WRONG (k))**,
  **CI's Node 22 (host is Node 26.8.1; CI read only)**, **store-azurite (READ from CI)**, **Windows / Safari / the account managers' real browsers and
  real phones**, **screen readers (E7 is a DOM read, not an AT run)**, **Claude in Chrome (not used)**, **fix (2) (not this gate)**, and every §N row
  you did not run, with the reason. **Every action recommendation carries its evidence class: MEASURED AT RUNTIME / PROBED / READ ONLY.**
- Report the pinned head and main as three timestamped readings (**start / mid / end**), each with its branch name, plus `refs/pull/9/head`.

PROVENANCE:
- heads: main `e4ce5367761e…`, `fix/qq-email-print-mode-guard-2026-10-16` `5f08fe035f39…`, `refs/pull/9/head` `5f08fe0…`, `refs/pull/9/merge` `deb50819…`
  | `git -C <quickquote on Laptop-DEV> ls-remote origin` | read 2026-10-16 14:01:52 AEDT
- parent, date, count 1 / 0 behind, merge-base, numstat (+204/−2), per-file diffs, the unchanged-blob list, head tree `dc6aef6`, commit message;
  `3dd15bc`/`d030674` ancestors; `git diff --stat 3dd15bc 5f08fe0` (4 files +225/−18) and `3dd15bc e4ce536` (2 files +21/−16) | `log`, `rev-list --count`,
  `merge-base`, `diff --numstat`, `diff`, `rev-parse <sha>:<path>` | read 14:01-14:1x
- the code at `5f08fe0` (`strip.js` HOSTED_EXTRAS whole, the test file whole, package.json scripts) and at `e4ce536` (`index.html` `.svc-warn` CSS
  ~1110-1126, print-mode radios ~1670-1690, programmatic `pmDefault.checked` paths ~3036/3420/3550, `text-transform` rules; the hosted server
  module's `createApp` options ~255-271; tests.yml run lines) | `git show` | read 14:0x-14:1x
- W1/W2 byte equality card ↔ `strip.js` (sha256) | python over `0_Brain/dashboard/data/decisions.json` (cards `quickquote-guard-words-1016`,
  `quickquote-email-sends-standard-not-custom-1016`: choice a, ruled_ts 13:52:18 / 13:29:39) and `git show 5f08fe0:stage3/strip.js` | read 14:0x
- GitHub (READ-BY-DRAFTER, `gh api` GET with Vision's gh-config; its two files' mtimes unchanged, 12 Oct 18:09): PR #9; PR #9 files; runs
  38842678755 / 38842703255 + jobs; check-runs on `5f08fe0`; code-scanning open 0 on main; Dependabot open #1 #4 | read 14:0x
- the READY (read whole); CLARIFICATIONS C-18..C-20 (C-20 whole); Tuesday's `0_Brain/daily_tuesday/2026-10-16.md` entries 13:26, 13:51, 13:52,
  14:01, 14:02 and `2026-10-13.md` 12:29 (v2.35 live, `v0.6.3-tool2.35-3dd15bc`) | read 14:0x-14:1x
- gate 17's `evidence/tools/` listing and the headers of the harnesses named in PRIOR ROUND; gate 18's brief, DRAFTER-REPORT and launcher (whole);
  BRIEF_TEMPLATE (whole) | read 14:01-14:1x
- load 184.10/226.20/234.67; tmux panes (no `QA/Vision-gate18` pane; gate 18 brief 7 unstamped placeholders); host node v26.8.1; this drive's Testing Agent MAIN
  has no `projects/vision`; the builder's `guard-2026-10-16-evidence/` listing (16 files) | `uptime`, `tmux list-panes -a`, `node -v`, `ls`, `grep -c`
  | read 14:08
- no merge-tree, no fetch, no docker, no product process, no browser, no `az`, no npm, no mail was made by the drafter; `gh` was used for GET reads only
