# QA Agent Invocation Brief — Datasec/Vision_Sales_Portal, GATE 23: ONE TIER-1 QuickQuote gate — PR #8 (puppeteer-core 25.0.2 + node:22 stage3 image; C-19) @ `4d6ed6e`, gated AS MERGED onto current QuickQuote main `437ab4b` — one verdict, one report

**TIER 1 (the runtime that renders every emailed quote PDF and workbook a customer receives).** This is the FIRST gate that runs on PR #8 in its
current shape. Gate 4 gated an older head (`0d45100`, as "P5B": "GO, tested only — image build NOT RUN; Node 22 NOT TESTED"). Gate 18 was drafted for
`4d6ed6e` on 2026-10-16 and **never launched** (the compute hold; `inbox_routing.conf` has no `QA/Vision-gate18` line, and there is no gate-18 report on
disk). **Main has moved 4 commits since PR #8 was last forward-merged** (PR #9, the email guard, and PR #11, v2.36, are on main; PR #8's head still sits
on `e4ce536`). So this gate measures **what would land**: PR #8 merged onto `437ab4b` (see TARGET-MODE, D6).

**Drafted for Tuesday on 2026-10-18 between 06:09 and ~06:5x AEDT by a read-only drafting agent. Tuesday reviews, stamps and launches it.**
Model: gate 22's kit (`2026-10-17_vision-gate22-qq-pr10-r3.md`) and its launcher (`launch_qa_vision_qq_gate22.sh`), which give the section shape,
identity rules (the GET-only `gh` shim), report path, verdict token, THE MODEL RULE, floor and HELD rules. **Gate 18's kit**
(`2026-10-16_vision-gate18-qq-pr8-puppeteer25.md`, same PR, never run) gives the PR-#8-specific traps (the stub identity, the ESM-only load, the
image method). **This brief governs where they differ.**

The builder's READY mail under test (on disk, read whole by the drafter; sha256 `201da80e6e76e1c7835271d9c703dd15eee6b48ac86563794d887e027fc1ecd6`,
6,738 B, 40 lines; written 2026-10-16 against main `e4ce536`):
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-16_vision-qq-pr8-READY-mail.txt`
The builder's later amd64 STATUS mail is **not on disk**. Tuesday's note (`0_Brain/daily_tuesday/2026-10-16.md`, 14:09) records it as: "PR #8 amd64 logged
re-run = PR #8 169/170, main 168/170, every failure a TIMEOUT (30 s navigation / BC-F1 60 s watchdog), counts swing on identical images at load ~200;
native x64 CI print-fit 170/170 at PR #8." That is a relayed CLAIM.
**Every builder statement comes from that mail, the PR body, the commit messages or the code at each sha. Each one is a CLAIM. Every suite set, every
artefact comparison, every advisory reading and every merge-result tree is RE-DERIVED by the gate.**
The launcher parses §PIN, refuses any placeholder, re-reads both rows, `refs/pull/8/head` and PR #10's head by `git ls-remote` just before launch,
and **refuses if QuickQuote main has moved** (this gate pins main exactly). It also **recomputes the merge result's tree hash read-only and refuses
unless it equals GitHub's test merge** (`8077fdc`, §PIN). The verified table is appended to your prompt.

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-18 06:39 AEDT, Tuesday (s114), kit + drafter report read whole
Self-check note: Tuesday read the kit (693 lines) and the drafter report whole at 06:3x. Checked against each other: the D4 GO-releases-a-merge-only clause vs §12 and HELD (consistent); IMAGE-LEG ARM64-NATIVE vs §N5.5, §N6, §N9 and HELD (each already branches on the D7 value, so no NONE-only sentence binds); AZ-PRE-READ = the drafter's expectation; the routing name is the same in ROUTING-LINE, §14 and the conf. The merge ORDER is not ruled here: §12 measures both and Tuesday rules it at verdict.

GH-API-LEG: READ-ONLY-VISION-TOKEN
<!-- As gates 17-22. The launcher exports GH_CONFIG_DIR = Vision's .gh-config behind a GET-only `gh` shim first on PATH. Change it to NOT-RUN only if
     Tuesday withdraws the token; then §N7's API half, §N10 and §12's compare reads are NOT RUN and the drafter's readings stay READ-BY-DRAFTER. -->

AZ-READ-LEG: TUESDAY-READS
<!-- As gates 20-22. The gate runs NO az. Tuesday reads the live webapp's linuxFxVersion BEFORE launch, writes it on the line below, and reads it again
     at verdict. The gate RELAYS. -->
AZ-PRE-READ: linuxFxVersion DOCKER|hpasqqacr.azurecr.io/hpas-quickquote:v0.6.4-tool2.36-437ab4b ; read 2026-10-18 06:38:48 AEDT by Tuesday (az webapp config show -g hpas-quickquote-rg -n hpas-quickquote --query linuxFxVersion, read only; Vision's own AZURE_CONFIG_DIR; tenant d500ebad / sub 0c57ab37, az account show 06:38)
<!-- One line, e.g. `linuxFxVersion DOCKER|hpasqqacr.azurecr.io/hpas-quickquote:<tag> ; read <YYYY-MM-DD HH:MM:SS AEDT> by Tuesday (az webapp config
     show, read only; Vision's own AZURE_CONFIG_DIR; tenant d500ebad / sub 0c57ab37)`. The launcher refuses until it names linuxFxVersion.
     Drafter's expectation (NOT a reading): v0.6.4-tool2.36-437ab4b (Tuesday's 2026-10-17 11:58:56 read; the Vision wrap 2026-10-17 18:30Z says live is
     still v2.36 and the seat ran no az). The DOCKER| prefix is also the reading §N5.4 needs: it shows App Service runs the image's own Node. -->

TARGET-MODE: MERGE-TREE
<!-- Decision D6 (see TUESDAY'S RULINGS). Exactly one of:
       MERGE-TREE          gate THE MERGE RESULT M8 = PR #8 merged onto main 437ab4b (tree 8077fdc = GitHub's test merge refs/pull/8/merge 7378a4e),
                           built by the gate from the object store (§N1.3), plus the raw head H8 = 4d6ed6e for the CI/READY comparison. A GO is a GO
                           for merging 4d6ed6e onto 437ab4b with a merge commit, and only while main is still 437ab4b. (Drafter's reading.)
       FORWARD-MERGE-FIRST nothing is gated now: Tuesday asks the builder to forward-merge 437ab4b into fix/qq-puppeteer-25-2026-09-22 (as C-19's own
                           scope line describes), waits for CI + CodeQL on the new head, and re-briefs. The launcher refuses to start under this value.
     The launcher refuses while it reads TUESDAY-DECIDES. -->

IMAGE-LEG: ARM64-NATIVE
<!-- Decision D7. Exactly one of:
       NONE           NO DOCKER: no docker command of any kind (not even a read). Node 22 is never EXECUTED by this gate: it is READ (§N5) and relayed
                      from CI's logs; the host runs Node 26.8.1 only (no Node 20 or 22 binary is installed here). (Drafter's reading: the commission's
                      scope names "the Node 22 runtime expectations in CI and in the App Service config as recorded in the repo", a READ.)
       ARM64-NATIVE   §N6 builds the base (437ab4b) and M8 images for linux/arm64 back to back and runs the suites and the §N3 core set inside them.
                      Node 22 and Debian Chromium are then EXECUTED. Needs NX-1 (Docker Hub, Debian apt, npm registry inside the build).
       AMD64          as ARM64-NATIVE, for linux/amd64 under emulation (what App Service runs). Gate 18's method; the builder saw emulation timeouts.
     The launcher refuses while it reads TUESDAY-DECIDES. -->

NPM-AUDIT: NOT-RUN
<!-- Decision D8. RUN = `npm audit --omit=dev --json` at BASE, H8 and M8 from the gate's own trees (network exception NX-2: the npm registry's audit
     endpoint). NOT-RUN = no registry contact; the builder's "high 3 -> 0" is re-derived from the GitHub advisory reads of §N7 instead, and the npm
     audit claim is marked NOT RUN. Drafter's reading: NOT-RUN (the GitHub Advisory Database, read by GET under GH-API-LEG, is the source npm's audit
     endpoint draws from; it needs no new egress). The launcher refuses while it reads TUESDAY-DECIDES. -->

ROUTING-LINE: QA/Vision-gate23 added to inbox_routing.conf 06:39 by Tuesday (.pre-1018-gate23 backup)
<!-- Tuesday adds `QA/Vision-gate23|tuesday-agent@agentmail.to|no` to /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/inbox_routing.conf (pattern:
     the QA/Vision-gate22 line, conf line 229 at drafting) and stamps this line, e.g. `QA/Vision-gate23 added to inbox_routing.conf <HH:MM> by Tuesday
     (.pre-1018-gate23 backup)`. The launcher refuses while the conf line is absent (guard 41) or this line carries the placeholder (guard 32).
     The drafter did NOT edit the conf. -->

## Charter
Read `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an independent tester. You did not
build this change and you owe the builder nothing. **Every line below that reports what the builder says is a CLAIM, never evidence.**

**One gate, ONE target, ONE verdict: GO / GO WITH FINDINGS / NO GO, at its pinned sha.**
- **QQPB** at `4d6ed6e` — **TIER 1 (the runtime that renders the customer's quote PDF and workbook).** QuickQuote PR #8, branch
  `fix/qq-puppeteer-25-2026-09-22`, title "stage3: puppeteer-core 25 + node:22 image — clears Dependabot #1 #4 (extract-zip); decision 14". Three
  commits over its merge-base `e4ce536`, **4 commits behind main `437ab4b`**:

| # | commit | parents | what it is |
|---|---|---|---|
| 1 | `3d0167e` (2026-09-22 18:54:43 +1000) | `47eb533` | "stage3: puppeteer-core 25.0.2 and a node:22 image, clearing the extract-zip advisories" |
| 2 | `0d45100` (2026-09-22 21:51:10 +1000) | `3d0167e` + `51e9286` | "Merge main 51e9286 forward … (item 11, for gate 4)" — gate 4's P5B head |
| 3 | `4d6ed6e` (2026-10-16 12:49:56 +1100) | `0d45100` + `e4ce536` | "Merge main e4ce536 forward into fix/qq-puppeteer-25-2026-09-22 (PR B, decision 14)" — THE HEAD |

**What main gained after `e4ce536` (READ, `git log e4ce536..437ab4b`):** `5f08fe0` (the email guard, PR #9) → `9d1c5ab` (merge of PR #9) → `818a019` (v2.36)
→ `437ab4b` (merge of PR #11) = **LIVE v0.6.4-tool2.36-437ab4b**. Main's delta over `e4ce536`: `index.html` +1/−1, `stage3/package.json` +1/−1 (the
`test:print` line gains `test/email-print-mode.mjs`), `stage3/strip.js` +28/−1, `stage3/test/email-print-mode.mjs` added +175.

**PR #8's delta over its merge-base (`git diff e4ce536 4d6ed6e`, 5 files, +85/−522; = the PR files API and the compare API, READ 06:10-06:11):**

| file | +/− | blob e4ce536 → 4d6ed6e | the only non-comment change |
|---|---|---|---|
| `stage3/Dockerfile` | +4 / −1 | `8311ebe` → `5972f7c` | `FROM node:20-bookworm-slim` → `FROM node:22-bookworm-slim` (+3 comment lines) |
| `stage3/package.json` | +1 / −1 | `61d0d5c` → `94ab2f5` | `"puppeteer-core": "^23.5.0"` → `"^25.0.2"` (line 21) |
| `stage3/package-lock.json` | +76 / −518 | `01c5e5e` → `9366344` | puppeteer subtree: 286 → 247 `packages` entries; extract-zip gone |
| `stage3/test/fixtures/hang-close.cjs` | +3 / −1 | `f902922` → `8fe024c` | `require("puppeteer-core/lib/cjs/puppeteer/cdp/Browser.js")` → `require("puppeteer-core/internal/cdp/Browser.js")` |
| `stage3/test/lib-close-shared.test.mjs` | +1 / −1 | `6f79215` → `d7c2b07` | the same require swap (line 19) |

**THE MERGE RESULT — "M8" (what a merge of PR #8 onto `437ab4b` produces; READ and COMPUTED by the drafter, 06:10-06:20):**
- main `437ab4b` did not touch four of PR #8's five files (`Dockerfile` `8311ebe`, lockfile `01c5e5e`, `hang-close.cjs` `f902922`, `lib-close-shared.test.mjs`
  `6f79215` are the same blobs at `e4ce536`, `437ab4b` and `f31720e`). **The one file both changed is `stage3/package.json`, in DISJOINT hunks** (main:
  line 11, `test:print`; PR #8: line 21, `puppeteer-core`).
- **The merged `package.json` = main's `1606aa3` with the puppeteer line changed = blob `f0df06f`** (drafter: `sed` + `git hash-object --stdin`, no `-w`),
  **equal to the blob GitHub's test merge `refs/pull/8/merge` = `7378a4e` carries** (commits API: parents `437ab4b` + `4d6ed6e`, tree `8077fdc`, 5 files vs
  `437ab4b`, created 2026-10-16T19:13:21Z).
- **M8's tree, computed read-only from `git ls-tree` with those five blobs swapped in, = `8077fdc65d39be92d27aba11ebed33586b00440a` = GitHub's** (the same
  script reproduces `c71780c` for `437ab4b` unchanged and `01bdc92` for `4d6ed6e` from `e4ce536`: its two controls). The launcher repeats this.
- **M8 is NOT in the local object store** (`git cat-file -t 7378a4e`: no such object) and **no CI has ever run on it** (`actions/runs?head_sha=7378a4e`:
  0). CI ran on `4d6ed6e` (and on the OLD test merge over `e4ce536`). **This gate is the only test M8 gets before a merge.**

**Same blob at `437ab4b` and in M8** (everything except the five files above), including `index.html`, `stage3/server.js` (the hosted server module),
`stage3/lib/pdf.js`, `stage3/lib/xlsx.js`, `stage3/strip.js`, `.dockerignore`, `.github/workflows/tests.yml` `ec450f5`. **So the page, the server and the
renderer's own code are main's: everything this gate can see differ between BASE and M8 is the RUNTIME (puppeteer-core 23.11.1 → 25.0.2 and its subtree;
in an image, Node 20 → 22).** That is exactly what it must look for.

**Names, written out every time:**
- **QQPB** = branch `fix/qq-puppeteer-25-2026-09-22` = PR #8 = "PR B" = decision 14 = C-19. **H8** = its head `4d6ed6e` (tree `01bdc92`).
- **BASE** = **MAIN-Q** = QuickQuote main `437ab4b` (tree `c71780c`) = what is LIVE. **M8** = BASE + PR #8 (tree `8077fdc`; built by you, §N1.3).
- **P10** = PR #10's head `f31720e` (tree `ee51fa7`; gate 22 GO WITH FINDINGS; not merged; waits on Kam's open card
  `quickquote-v239-custom-price-fix-publish-1017`). **M8P10** = BASE + PR #8 + PR #10 (predicted tree `d809de1dd44bd7a0624fcf17dd50636f1acfcb79`,
  predicted `package.json` blob `23cc8c9`; the same tree whichever merges first, because the two PRs touch disjoint files and hunks).
- **C-19** = Kam's ruling, card `quickquote-decision14-puppeteer25-node22-1016` = (b) "Build the puppeteer 25 + node 22 change now". **C-20** = card
  `quickquote-email-sends-standard-not-custom-1016` = (a), whose last bullet binds the publish: "Fix (2) and PR #8 (C-19) each need Kam's own word before
  any publish."

Branch status: **NOT on main. PR #8 open, not merged, not draft, `mergeable` true, `mergeable_state` clean, `updated_at` 2026-10-16T01:53:57Z** (the
PR API still reports `base.sha` = `e4ce536`: the sha at its last push, not current main). READ-BY-DRAFTER 06:10:17.

## RULED BY KAM, AND SETTLED
- **Vision `1_Project_Definition/CLARIFICATIONS.md`** (`/Volumes/Laptop-DEV/!CODING/Datasec/Vision_Sales_Portal/1_Project_Definition/CLARIFICATIONS.md`):
  read it whole (C-01..C-20 at drafting). **Cite only what you open.**
  - **C-19 (Kam, live board 2026-10-16 12:41:19 AEDT):** "Build the puppeteer 25 + node 22 change now". Scope: "Forward-merge current QuickQuote main
    into `fix/qq-puppeteer-25-2026-09-22` … to close Dependabot #1 #4 (extract-zip). TIER 1: full suites, real PDFs both themes + xlsx before/after on
    the same fixture, and the container image built LOCALLY for evidence only (never pushed to ACR, never a release tag) with the PDF path run inside it.
    PR, CodeQL + tests.yml green, independent gate, merge on Tuesday's GO." **Not covered: "publishing the new runtime to the live site (Kam's separate
    tap), any ACR push, any deploy or Azure change."**
  - **C-20 (Kam, 2026-10-16 13:25:51):** "Kam's grant covers the GUARD only. Fix (2) and PR #8 (C-19) each need Kam's own word before any publish."
- **Kam's open card** `quickquote-v239-custom-price-fix-publish-1017` (decisions.json: status open, no ruled choice, read 06:1x): the publish of PR #10
  (v2.39). **Precedent that bundling matters to Kam:** card `quickquote-guard-publish-includes-pr7-deps-1016` (ruled a, 2026-10-16 14:24) asked him
  whether the guard's publish could also carry PR #7's dependency fixes. **A publish builds the image from main, so whatever is merged by then ships
  together** (§12).
- **PRODUCTION IS LIVE for this project.** Live QuickQuote (`hpas-quickquote`, `hpas-quickquote-rg`, its registry `hpasqqacr`, its Table Storage and
  its log workspace) and the live portal (`datasec-sales-portal.azurewebsites.net`, `datasec-sales-portal-rg`) are PRODUCTION. **Nothing in this gate
  touches either** (§13, HELD). The gate makes no Azure contact at all (AZ-READ-LEG = TUESDAY-READS).
- **THE LIVE CHECK IS KAM'S, NOT YOURS.** You never request any URL of the live site, never read, ask for or type the HPAM access word; the unlock word
  in your harness is a fresh random string you generate. **The access word and the offline page's constant are not your subject** (gate 20 S5): never
  read, print, grep for or reproduce them; never print or grep the ADVANCED SEAM of `index.html` (BASE and M8 carry the same `index.html` blob, so
  locate the seam by line number only, as gate 22 did, and stay out of it).
- **Merging and publishing are HELD. Nothing merges or publishes on your word.** A merge is Tuesday's GO on a pinned head (C-19); a publish is Kam's own
  word (C-19 "not covered", C-20).
- **The BUILDER's choices, each judged by the gate (say whether each needs Kam):** (1) puppeteer-core **25.0.2**, not the newest 25.x ("chromium-bidi
  157, unverified against bookworm's Chromium 153"); (2) the `basic-ftp` override kept though inert (no basic-ftp left in the tree); (3) the two test files
  reach `puppeteer-core/internal/cdp/Browser.js` because 25 is ESM-only; (4) the base image stays a floating tag (`node:22-bookworm-slim`, no digest) and
  Debian `chromium` stays unpinned; (5) the lock rebuilt with `npm install puppeteer-core@25.0.2 --package-lock-only`; **(6) NEW since gate 18: the branch
  was NOT forward-merged again after PR #9 / PR #11 landed** — C-19's scope line says "forward-merge current QuickQuote main" (WRONG (a)).

## PRIOR ROUND
PRIOR ROUND: round 1 of PR #8 at a launched gate in its current shape. The branch's only earlier gate is **gate 4** (2026-09-22), "P5B at `0d45100`: GO,
tested only — image build NOT RUN; Node 22 NOT TESTED". Its report lives only on the T9 (`/Volumes/KK_T9_External_HDD/!CODING/Testing Agent
MAIN/projects/vision/reports/2026-09-22-vision-qq-gate4`, `sections/P5B.md`); **read it only if the T9 is mounted, never write there; if absent, say so.**
Its ship note binds: "the lockfile and the `FROM node:22` line must ship together, never apart."
ITS REPORT IS ON DISK AT: (gate 18 has none — never launched.) The NEAREST launched QuickQuote gate is gate 22, whose report is the reference for
the current main and for P10: `/Volumes/Laptop-DEV/!CODING/Testing Agent MAIN/projects/vision/reports/2026-10-17-vision-gate22-qq-pr10-r3`
(`report.md`, 455 lines, sha256 `56356c7635c878e30192e1d7c443410ee25f391a932077cc945d63d6322d816f` at drafting; `evidence/mail/verdict-body.txt` sha256
`88094f7e0ce668359a539a26816607cc7a99fd1a8e3acb51b3651e7da6976560`; `evidence/tools/`). **Read its §VERDICT, its N6 (suites as sets, 175 `test:print` names at
`437ab4b`, 217 at `f31720e`), its §12 ("If PR #8 merges first, re-run on the merged tree: …") and its NOT TESTED list.** Gate 22 says of PR #8 only
"not this gate".
**Gate 18's kit is the reference for PR #8's own traps** (read it whole; it was never run, so nothing in it is a measurement):
`/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-16_vision-gate18-qq-pr8-puppeteer25.md` — its WRONG (b) (the image ships
`stage3/test/`), (c) (the `lib-close-shared` cell can pass whether or not its stub hits), (e) (one build window), (h) (`require(esm)` warnings), (i)
(npm audit counts vs Dependabot), (m) (the entry point needs Azure) and its §N2-§N5 image method are carried here by reference.

**Instruments are REUSED BY COPY from gate 22's `evidence/tools/`:** `qa-run.py`, `mktree-qq.sh`, `lockcmp.py`, `lockwalk.py`, `tapsets.py`,
`g17-dupnames.py`, `g22-run-suites.sh`, `g22-compare.py`, `g22-infscan.py`, `g22-figures.py`, `g22-gh.sh`, `g22-heads.sh`, `g22-cmdlog.py`, `g22-repoint.py`,
`qa-harness-g22-drive.cjs`, `qa-harness-g22-offline.cjs`, `qa-chrome-egressblock.sh`, `qa-chrome-census.py`, `qa-egress-posctl.mjs`, `qa-floorcount.py`,
`qa-harness-floorctl.mjs`, `qa-netlog-scan.py`. **COPY what you use into THIS gate's own `evidence/tools/`, read it before you trust it, and RE-POINT every
hard-coded path** (gate 22's copies hard-code `work-g22`, the gate-22 report folder, `@qa-g22.invalid`, `g22-` prefixes and `v2.39`). **Never edit, run
from, or write into gate 1-22's copies, evidence or trees.** Record the sha1 of each copy before and after your edits.

**Self-findings from earlier gates bind you:** quote every path (space and `!`; the repo sits under `Quoting Tool/`); run every loop and every `git show
<sha>:<path>` under **bash, not zsh** (zsh does not word-split an unquoted variable and reads `$H:s…` as a modifier — the drafter hit the first one
today); run `node strip.js` before any lone browser file; assert every tamper landed before reading its result and never let a landed-check quote the form
it replaces; write scripts with the Write tool; npm's update-notifier egresses unless disabled; record the load beside every timing; `git branch` and `git
for-each-ref` are NOT read verbs here; one tab, foreground; sign-in addresses lower-case.

**PRIOR WORK: verify every claim against git history and the Actions API (GH-API-LEG), never against this brief.** The READY's and the PR body's claims
(lock 40 removed / 1 added / 13 changed; `npm audit --omit=dev` high 3 → 0; `npm ls --all` rc 0; local 69 / 132 / 170 / 6 and red-first 167/169 — **all
against `e4ce536`, not today's main**; arm64 images node 20.20.2 / pptr 23.11.1 vs node 22.23.2 / pptr 25.0.2, Chromium 153.0.8010.52, in-image PDFs
text- and pixel-identical; CI 5/5 on runs 38837565972 / 38837589895; CodeQL pass; MERGEABLE / CLEAN) are re-derived or marked UNVERIFIED.

## PIN — HEADS (parsed and verified by the launcher)
**The launcher enforces these rules:** every row has a 40-hex head and no `@`; the head is a commit; for QQPB the base is an ancestor AND the
merge-base with MAIN; `git rev-list --count base..head` equals `commits`; QQPB is not on main and is EXACTLY 4 behind it; the chain is pinned by parents
(`3d0167e` ← `47eb533`; `0d45100` = `3d0167e` + `51e9286`; `4d6ed6e` = `0d45100` + `e4ce536`; `437ab4b` = `9d1c5ab` + `818a019`; `9d1c5ab` = `e4ce536` +
`5f08fe0`); trees H8 `01bdc92`, BASE `c71780c`, P10 `ee51fa7`; `git ls-remote origin refs/heads/<branch>` equals the head NOW **for BOTH rows — a moved
main REFUSES (re-pin and re-brief)**; `refs/pull/8/head` equals H8 NOW; **M8's tree recomputed read-only equals `8077fdc` (GitHub's test merge)**; PR #10's
head is still `f31720e` (a move is a NOTE: the §N3.6 interaction column would be stale).

<!-- PIN-HEADS:BEGIN -->
| id | repo | branch | head | base | commits | status |
|---|---|---|---|---|---|---|
| MAIN-Q | quickquote | main | 437ab4bc412bc74d8da3b66a6ac5c71d7335c5d6 | - | - | IN |
| QQPB | quickquote | fix/qq-puppeteer-25-2026-09-22 | 4d6ed6ef403ef8962ded8211b76c3c6809bbb8c3 | e4ce5367761e03db982189a3f21758aa06714a85 | 3 | IN |
<!-- PIN-HEADS:END -->

Both rows: `git -C <quickquote> ls-remote origin` read by the drafter at **2026-10-18 06:09:46-06:09:49 AEDT**: `HEAD` = `refs/heads/main` = `437ab4b…`;
`refs/heads/fix/qq-puppeteer-25-2026-09-22` = `4d6ed6e…` = `refs/pull/8/head`; `refs/pull/8/merge` = `7378a4e1206afb6c2429ca9a9c74c30b52d40c39` (GitHub's
test merge over `437ab4b`; NOT in the local object store); `refs/heads/fix/qq-email-matches-print-2026-10-16` = `f31720e…` = `refs/pull/10/head`;
`refs/pull/10/merge` = `75d7a8e…`; `refs/heads/backlog/qq-extract-zip-2026-10-16` = `01c8d7f…` (despite its name, now the builder's G21 ticket branch; it
does not touch the lockfile). `rev-list --count e4ce536..4d6ed6e` = 3; `4d6ed6e..437ab4b` = **4**; merge-base `e4ce536`. **The head did not move from
the READY's `4d6ed6e`.**

**M8 pins (the launcher recomputes them):** tree `8077fdc65d39be92d27aba11ebed33586b00440a`; merged `stage3/package.json` blob
`f0df06fc2a313343e48c80b8445df7a0362363e2`. **M8P10 predictions (the gate verifies them, §N1.3):** tree `d809de1dd44bd7a0624fcf17dd50636f1acfcb79`;
`package.json` blob `23cc8c95180973f112ebd3d58f47f8d337efc5fc`.

Repo: quickquote = `/Volumes/Laptop-DEV/!CODING/Datasec/Vision_Sales_Portal/Quoting Tool/hpas-quoting-tool` (remote `datasecau/vision_hpas-quickquote`).
**The T9 copy of this repo is STALE. Never read it.** Its rules: the repo's own `CLAUDE.md` (read at BASE with `git show`; its deploy and publish
lines are NOT for you) and `/Volumes/Laptop-DEV/!CODING/Datasec/Vision_Sales_Portal/CLAUDE.md` (its QuickQuote section: "merge through GitHub with a
merge commit"; "Main only takes a PR that CodeQL has scanned"). **The builder's checkout is LIVE: never use the name `main` in the repo, always the
pinned 40-hex sha; never read any working tree as evidence; build every tree from the object store.** No Vision builder pane is live at drafting
(tmux: only `tuesday` and `fleet-monitor`, 06:12).

## WRONG OR UNVERIFIABLE IN THE COMMISSION AND THE READY — found by the drafter (verify each; all are claims)
- **(a) PR #8 is 4 behind main; everything the builder measured is against `e4ce536`.** C-19's scope line says "forward-merge current QuickQuote main"; the
  builder did so on 2026-10-16 12:49, and main then gained PR #9 and PR #11 (13:52-15:07 the same day). **The READY's 69/132/170/6 are `e4ce536`'s sets;
  today's main runs 175 `test:print` names (gate 22 N6), including `test/email-print-mode.mjs`, which has never run under puppeteer 25 anywhere.** Under
  TARGET-MODE MERGE-TREE you gate M8 and H8 both; every READY number is re-derived at H8, and M8's sets are new evidence.
- **(b) No CI has run on the tree that would land.** `refs/pull/8/merge` was recomputed by GitHub (2026-10-16T19:13:21Z) but no workflow ran on it (0 runs
  for `7378a4e`); CodeQL's PR analysis and tests.yml's `pull_request` run are on the OLD test merge. The Vision CLAUDE.md says main "only takes a PR that
  CodeQL has scanned": **whether GitHub will accept the merge without a fresh CodeQL run on the new merge ref is UNVERIFIED** (READ-ONLY-INFERRED that a
  re-run or a push may be needed). §N10 reads what exists; say what a merge would need. You never cause a run.
- **(c) Node 22 is never executed on this host.** Host Node is v26.8.1 (`/opt/homebrew/bin/node`; no `node@22`, no `nvm`); puppeteer-core 25.0.2 and
  @puppeteer/browsers 3.0.2 declare `node >=22.12.0`, chromium-bidi 16.0.1 `>=20.19.0 <22.0.0 || >=22.12.0` (head lock, READ). **Host runs prove
  puppeteer 25 on Node 26, not on Node 22.** The Node-22 evidence is CI's (`setup-node` `node-version: 22`, floating, five jobs) and, if D7 rules an image
  leg, the image's. Under IMAGE-LEG NONE, the Node-20-cannot-load-25 red proof (gate 4's ship note) is NOT RUN — say so.
- **(d) App Service's own Node setting does not apply: the site runs a container.** The repo records the hosted variant as "deployed as a container to
  App Service" (`CLAUDE.md`, stage3 section) via `az acr build … --file stage3/Dockerfile .` "then point the webapp at the new tag"; it records no
  `NODE|` stack, no `WEBSITE_NODE_DEFAULT_VERSION`, no `WEBSITES_*` setting (drafter `git grep -i` at `437ab4b`, 0 hits outside the log-show line).
  AZ-PRE-READ's `DOCKER|…` prefix is the confirming reading. **So "Node 22 in App Service" = the `FROM` line of the image a publish builds.** The
  `FROM` tag floats (`node:22-bookworm-slim`, no digest): the Node minor a publish gets is whatever Docker Hub serves that day (READ; gate 18 WRONG (e)).
- **(e) Byte equality of PDFs is not expected even when nothing changed.** Chrome writes `/CreationDate`, `/ModDate` and (often) a document `/ID`; the
  workbook's `docProps/core.xml` carries timestamps. **The commission's test is "byte- OR semantically equal": a byte difference confined to those
  fields is EQUAL; any other byte difference must be explained and the artefact must then be semantically equal (text, pages, fonts, pixels, workbook
  values/formats) or it is a FAIL.** And **BASE must equal BASE** (two runs of the same tree) before any BASE-vs-M8 zero is believed (§N3.5).
- **(f) puppeteer 23 → 25 may change `page.pdf()` defaults** (e.g. tagged/accessible PDF, outline, font waiting) without any QuickQuote line changing.
  **READ `stage3/lib/pdf.js`'s `page.pdf(...)` options and both installed versions' defaults in YOUR trees' `node_modules`** (never the internet); a
  changed default that alters bytes but not semantics is an observation; one that alters text, pages, fonts or pixels is a FAIL (§N4.3).
- **(g) The `lib-close-shared` cell can pass whether or not its stub hits** (gate 18 WRONG (c), unmeasured there): every assertion also holds when
  `close()` is not hung. §N4.2 proves the stub patches the renderer's real class and arms disarm mutants G23-M1 / G23-M2.
- **(h) The image ships `stage3/test/`** (gate 18 WRONG (b), READ again at H8: `.dockerignore` excludes only `**/node_modules`, `.git`, `stage3/public`,
  `stage3/private`, `Screenshots_for debugging`, `.playwright-mcp`; the Dockerfile does `COPY stage3/ /app/stage3/`). So the two files reaching
  `puppeteer-core/internal/…` ride in the production image. Pre-existing shape; report it.
- **(i) "Cleared" can only be READ on main after a merge.** Dependabot alerts #1 (GHSA-jmr9-qjv8-65gv, "extract-zip unvalidated symlink path traversal")
  and #4 (GHSA-7pqw-9j4j-h8q3, "extract-zip allows arbitrary file writes through symlink archive entries"), both high, `stage3/package-lock.json`,
  vulnerable `<= 2.0.1`, **first patched version: none** — the only fix is removing the package. Both are OPEN at drafting (06:11:24). Pre-merge, the gate
  proves the removal three ways (§N7): the lockfile, GitHub's dependency-review compare (which already lists `extract-zip@2.0.1` REMOVED carrying both
  GHSAs, for `437ab4b...4d6ed6e` and for `437ab4b...7378a4e`), and the advisory DB. **The alerts reading `fixed` is a post-merge read for Tuesday.**
- **(j) The dependency-review compare and the lockfile disagree on counts, harmlessly.** The compare lists 57 entries (14 added, 43 removed — the 13
  version changes appear as remove+add pairs); the READY says 40 removed / 1 added / 13 changed over the lockfile's `packages` map (which counts nested
  paths such as `extract-zip/node_modules/debug`). Reconcile them by name@version; say any name in one and not the other.
- **(k) PR #8 and PR #10 touch the same file.** GitHub compare `f31720e...4d6ed6e` and `4d6ed6e...f31720e` (merge-base `e4ce536`, READ 06:10:58): the only
  file in both deltas is `stage3/package.json` (PR #10: the `test:print` line, adds `email-matches-print.mjs` + `custom-price-bounds.mjs`; PR #8: line 21).
  **Predicted: either order merges cleanly to the same tree `d809de1`** (drafter arithmetic, not a merge). **Not predicted, and the reason §N3.6 exists:
  PR #10's two new browser test files and its whole gate-22 grid have only ever run under puppeteer 23.**
- **(l) Gate 22's PIN said "If PR #8 merges while you run, main moves".** Merging PR #8 FIRST moves main under PR #10's GO WITH FINDINGS (gate 22 §12 names
  the cells to re-run), and **a v2.39 publish from that main would also ship Node 22 + puppeteer 25 — a runtime C-20 says needs Kam's own word, on a
  card (`quickquote-v239-custom-price-fix-publish-1017`) that does not mention it.** This is a coordinator fact, not a defect of PR #8: §12 reports both
  merge orders with what each costs; the ruling is Tuesday's (and, for the bundle, Kam's).
- **(m) The emailed-PDF route needs a store and a mail transport; the hosted server module's own entry point needs Azure** (gate 18 WRONG (m)). Drive its
  `createApp()` export with the repo's in-memory store pattern and a capturing stub mail, as gates 18-22 prescribe. Booting the image's CMD with production
  settings stays NOT TESTED by design.
- **(n) The READY's "npm audit high 3 → 0"** counts packages along the `via` chain; Dependabot counts advisories per manifest (2). Say which three packages
  base's audit names if D8 = RUN; otherwise mark the claim NOT RUN and give the advisory-DB reading.
- **(o) CodeQL on PR refs is a blind instrument** (gates 17-22). On `4d6ed6e` (READ 06:11:24): `CodeQL` success "No new alerts in code changed by this pull
  request"; `Analyze (javascript-typescript)` and `Analyze (actions)` success; code-scanning open: main 0, `refs/pull/8/head` 0, `refs/pull/8/merge` 0. PR #8
  changes no product JavaScript. Say only what they can show.
- **(p) gitleaks** (8.30.1 at `/opt/homebrew/bin/gitleaks`) reads history through its own `git log -p`. Run it with `GIT_OPTIONAL_LOCKS=0`, `--redact`,
  report files in YOUR evidence only; a planted throwaway secret in a scratch copy of YOUR tree must be found first (§N8).
- **Verified TRUE at source (READ 06:09-06:20):** both heads + `refs/pull/8/head` by `ls-remote`; the chain and parents; 3 ahead / 4 behind; merge-base
  `e4ce536`; PR #8's 5-file numstat = the PR files API and the compare API; main's 4-file delta since `e4ce536`; the shared-file analysis; M8's
  `package.json` blob and tree = GitHub's; M8P10's predicted blob and tree; the head lock (247 entries, no extract-zip, engines above) vs main's (286,
  extract-zip 2.0.1 + nested debug/ms); `puppeteer-core/lib/cjs` referenced at `437ab4b` and at `f31720e` ONLY by the two files PR #8 rewrites (every other
  test reaches the public entry); tests.yml five jobs on `node-version: 22`; PR #8 open / clean; CI runs 38837565972 (push), 38837589895 (pull_request),
  38837588311 ("PR #8" dynamic CodeQL) `completed success`; 13 check runs, all success; 0 runs on `7378a4e`; Dependabot #1 / #4 open, #2 #3 #5-#16 fixed;
  dependency-review compare (above); advisories DB: `puppeteer-core@25.0.2` 0, positive control `extract-zip@2.0.1` = both GHSAs; repo allows merge,
  squash and rebase; Vision's gh-config mtimes unchanged by the drafter's GETs (12 Oct 18:09).

## THE READY — its claims and NOT TESTED (the gate rules on every claim)
Read the READY whole. Its NOT TESTED block, VERBATIM (the launcher checks it):

QQPB NOT TESTED
```
NOT TESTED
- amd64: both images above are arm64; App Service runs amd64. An emulated linux/amd64 build + in-image render + test:print is RUNNING now; result to follow in a STATUS mail. The ACR build (amd64, native) is the publish step, which is Kam's tap.
- Booting server.js inside the new image with production settings (ACS mail, Table storage, session secret): not done; no prod secrets used. stage3-server and store-azurite cover the server in CI on node 22.
- The live site, or a real emailed quote through ACS on the new runtime: publish-time checks.
```
(the PR body repeats all three.) Two more READY lines bind this gate: its PRIOR WORK says `3d0167e`'s PDFs were "byte-identical once dates masked" (the
§N3 normalisation rule is the same idea, re-derived, not borrowed), and "The extract-zip ticket (backlog/qq-extract-zip-2026-10-16 @ 88ad5e8) now points
at PR #8 and closes when #1 #4 read fixed on main" — that branch is now `01c8d7f` and carries the G21 tickets (READ: say whether `88ad5e8` is its ancestor
and whether the extract-zip ticket text is still on it).

**How you treat these:** amd64 is driven only if D7 = AMD64; otherwise NOT TESTED, with the builder's relayed emulation result named as a CLAIM. The
production-settings boot stays NOT TESTED by design (WRONG (m)). The live site and a real ACS mail stay NOT TESTED (publish-time, Kam's).

## 2a. LEGITIMATE SHAPES — not a checker
Not a checker: this is a runtime change. The ordinary shapes a rep and the office produce are the §N3 synthetic set instead. **Until a row is measured,
the instruction on ANY unexpected result is STOP and record it, never a remedy.**

## N1. THE DIFF AND THE MERGE RESULT (READ + COMPUTED)
**FAIL condition, stated BEFORE the read:** any non-comment change in PR #8's five files other than the four lines named in §Charter; any file in M8 that
differs from BASE other than those five; M8's tree ≠ `8077fdc`; any reference to `puppeteer-core/` other than the package's public entry in a file the
hosted runtime LOADS (`lib/`, the hosted server module, `strip.js`); a `package.json` dependency, override or script change other than the puppeteer line.
1. `git diff e4ce536 4d6ed6e` whole (quoted into `evidence/`), each hunk mapped to a claim; the non-comment-line filter for each file.
2. `git diff e4ce536 437ab4b` (main's side) whole; the shared-file analysis (one file, disjoint hunks); GitHub's compare API for `main...4d6ed6e`,
   `437ab4b...7378a4e`, `f31720e...4d6ed6e` and `4d6ed6e...f31720e` (GH-API-LEG), each quoted with its read time.
3. **Build M8 and M8P10 from the object store, never by a merge in the repo:** `git archive 437ab4b` into a fresh `mktemp -d` under `work-g23/`; overlay
   `git show 4d6ed6e:<path>` for the four untouched-by-main files; apply ONLY PR #8's `package.json` hunk (`git diff e4ce536 4d6ed6e -- stage3/package.json |
   patch -p1`, reject file recorded); assert `git hash-object` of the result = `f0df06f`. M8P10: the same overlay onto `git archive f31720e`, `package.json`
   = `23cc8c9`. **Prove each tree's hash**: in a scratch repo of YOUR OWN (`git init` under `work-g23/`; your OWN object dir) `git add -A && git write-tree`
   over the extracted tree → `8077fdc` for M8 (= GitHub's) and `d809de1` for M8P10 (the drafter's prediction). Optional: `git merge-tree --write-tree` only
   from YOUR OWN object dir (filled by `git clone --bare --no-local` FROM the repo, a read of it; record the repo's `.git/index` mtime before and after).
4. `git grep -n "puppeteer-core/"` at BASE, H8, P10 (and over M8 / M8P10 extracted): table file, line, shipped-in-image yes/no, loaded-at-runtime yes/no.

## N2. THE CI SUITES ON THE HOST, AS SETS, NOT COUNTS (TIER 1; MEASURED)
**FAIL condition:** any suite red on a clean M8 tree; a test NAME passing at BASE that does not pass at M8; a name passing at P10 that does not pass at
M8P10; `npm ls --all` rc ≠ 0 at M8; any installed package not byte-equal to the lockfile's integrity; `ERR_REQUIRE_ESM`, `ERR_PACKAGE_PATH_NOT_EXPORTED` or
`MODULE_NOT_FOUND` anywhere in M8's or M8P10's output.
1. **Trees** (fresh, one purpose each, under `work-g23/`): BASE `437ab4b`, M8, H8 `4d6ed6e`, P10 `f31720e`, M8P10. In `stage3/`:
   `npm ci --offline --ignore-scripts` (a cache miss FAILS, then NOT RUN with the tarball named; the drafter found puppeteer-core 25.0.2 / 23.11.1, @puppeteer/browsers 3.0.2,
   chromium-bidi 16.0.1, webdriver-bidi-protocol 0.4.1, zod 3.25.76 and extract-zip 2.0.1 in the cache index); lockfile proven **entry by entry** with
   `lockcmp.py` AND `lockwalk.py`; `npm ls --all` rc and stderr; `npm ls extract-zip yauzl basic-ftp proxy-agent puppeteer-core @puppeteer/browsers`.
2. **The suites by PATH and command (tests.yml, blob `ec450f5`, READ):** root `node --test quote-engine.test.mjs`; in `stage3/`: `npm test`, `npm run
   test:print`, `npm run test:xlsx`. **M8 ×2 and BASE ×1; M8P10 ×1 and P10 ×1; H8 ×1** (H8 re-derives the READY's numbers), same session, as SETS by
   test NAME (`tapsets.py`, `g17-dupnames.py`): lost, added, removed, duplicates for M8 vs BASE (expected: identical name sets; gate 22 read 175 `test:print`
   names at `437ab4b`) and M8P10 vs P10 (expected identical; 217). **Host Node is v26.8.1, not CI's 22: say so on every row.** Every Chrome under YOUR
   egress-block wrapper. `npm run test:azurite` is NOT RUN on the host (no Azurite without docker): relay CI's `store-azurite` on `4d6ed6e`, READ ONLY,
   and say it is not M8.
3. **The red-first claim (fixture fix), at M8:** a fresh M8 tree with ONLY the two test files set back to their BASE blobs (`f902922`, `6f79215`; tamper
   asserted landed, `node --check` rc 0 — a file that does not parse is VOID): run `test:print`; the READY predicts `lib-close-shared` failing at LOAD and
   BC-F1's child on `MODULE_NOT_FOUND`. Quote both errors. A fresh M8 tree green is the pair.
4. Never `npm install`, never `npm audit fix`, never `npx` anything not already in the tree.

## N3. THE FIXED SYNTHETIC QUOTE SET — BASE vs M8, BYTE-OR-SEMANTICALLY EQUAL (TIER 1; MEASURED; the commission's core)
**FAIL condition:** for any row, an M8 artefact NOT equal to BASE's for the same inputs, where EQUAL means (i) byte-equal after normalising ONLY the PDF
`/CreationDate`, `/ModDate`, `/ID` and `/Producer`-version tokens and the workbook's `docProps/core.xml` (state each regex and count the substitutions), OR
(ii) failing (i), semantically equal: `pdftotext -layout` text identical, page count and A4 identical (`pdfinfo`), font set identical (`pdffonts`),
`pdftoppm -r 100` pixels identical on every page, workbook every part other than `core.xml` identical (or, failing that, every sheet's cell values, types
and number formats identical); a captured mail (to, bcc, subject, text, attachment names and content types, count) differing; a POST answer (status,
qnum shape, `unknownFields`, `clearedChecks`) differing; any render error, page error, console error or `unknownFields` entry at M8 that BASE does not
also produce. **A (ii) pass with a (i) difference is EQUAL with an observation naming the differing bytes and their cause (WRONG (f)).**
1. **Instrument — the real server path, as gate 22 (§N3.1 there):** YOUR harness `require`s each tree's own hosted server module's `createApp()` export
   (NEVER its entry point, NEVER with a real secret), the repo's in-memory store pattern (lifted from the tree's own `server.test.mjs`), a CAPTURING stub
   mail, a throwaway 48-char `sessionSecret` and a throwaway `unlockSecret` (fresh random; never the HPAM word), `salesCopy` = `sales-copy@qa.invalid`, the
   tree's OWN `renderQuotePdf`, a frozen clock (`clock` FROZEN to the same instant in both trees) (prove it froze; the server-issued quote number must then be equal),
   `trustForwardedFor: false`, on 127.0.0.1 and a kernel port, under `qa-run.py` (`env -i` allowlist). ONE Google Chrome (`/Applications/Google
   Chrome.app`, 155.0.8059.84 at drafting — **the SAME binary for BASE and M8, so puppeteer is the only variable on the host**) through your egress-block
   wrapper, driven by the TREE'S OWN puppeteer-core (BASE drives with 23.11.1, M8 with 25.0.2 — write the drive against APIs both versions have and say
   which), signs in with the captured OTP, (advanced rows) unlocks through the page's own controls, fills the form as a rep, picks the print mode by its
   label, captures the page's own Generate output as a PDF in print media A4, and presses the page's own Email button. **FX: block every FX host; every
   rate is the seeded table** (AUD 1.55, CAD 1.42 at drafting); record the rate line printed on each PDF.
2. **THE SET (S1-S16; the same inputs, byte for byte, in both trees; customer name `Parity & <Probe> "QA" 'g23'`, 40 devices, 3 years, the full bundle unless
   the row says otherwise):**

| row | session | print mode | currency | other | artefacts |
|---|---|---|---|---|---|
| S1-S3 | simple (never unlocked) | — | AUD / USD / CAD | — | emailed PDF + workbook + mail; printed PDF light |
| S4-S6 | advanced | "Standard pricing only" | AUD / USD / CAD | no custom price | emailed PDF + workbook + mail; printed PDF light |
| S7-S9 | advanced | "Custom pricing only" | AUD / USD / CAD | "% from standard" −10, Apply | press 1 (v2.36's guard: the W1 note, nothing sent) AND press 2 (standard sent); printed PDF |
| S10-S12 | advanced | "Standard + custom pricing" | AUD / USD / CAD | −10 % | as S7-S9 |
| S13 | advanced | "Standard pricing only" | AUD | PoC + Workpath-Ready + 10 h custom hours (gate 18's "Advanced + 10 h custom") | emailed + printed light AND dark |
| S14 | simple | — | AUD | STRESS: 2,500 devices, 5 years | emailed + printed (page count) |
| S15 | simple | — | AUD | printed DARK via the page's own theme control (after it settles) | printed light + dark |
| S16 | advanced | "Standard pricing only" | CAD | Manager only (Mix-and-Match, one app) | emailed + printed |

   (At BASE `437ab4b` the custom modes are v2.36's guard: press 1 shows W1 and sends nothing; press 2 sends the standard quote. M8 has the same
   `index.html` and `strip.js`, so it must behave identically; that is what S7-S12 test, never the guard's wording.)
3. **Per row record:** the POSTed body verbatim, POST count, status, the server's JSON, the store row, the captured mail, every artefact's sha256 and size,
   the (i)/(ii) result per artefact, the load.
4. **The offline page is NOT this gate's subject** (`index.html` is the same blob in BASE and M8 and has no npm runtime): one control row only —
   `index.html` opened as a FILE from each tree prints byte-identically (it must: same bytes, same Chrome).
5. **CONTROLS THAT CAN FAIL, BEFORE ANY ZERO IS BELIEVED:** (a) **BASE-vs-BASE**: S1, S4, S13 rendered twice at BASE in separate processes must be EQUAL by
   (i) — if they are not, the comparator's normalisation is wrong or the render is nondeterministic, and every BASE-vs-M8 zero for that artefact type is
   VOID until fixed; (b) a planted one-word, one-digit and one-pixel change in a copy of a BASE artefact must each be reported; (c) AUD vs CAD (S1 vs S3)
   must differ; (d) a planted workbook cell change must be reported.
6. **THE INTERACTION COLUMN — M8P10 vs P10 (WRONG (k)):** gate 22's 9 advanced cells (the three print modes × AUD/USD/CAD, −10 %) + the 3 simple cells,
   rendered at P10 (puppeteer 23) and at M8P10 (puppeteer 25), compared by the same (i)/(ii) rule; and **within M8P10, email = print by gate 22's FULL-TEXT
   rule** (the emailed PDF's `pdftotext -layout` equal to the printed PDF's after normalising only the quote number) for every advanced cell that sends.
   An M8P10 cell that differs from P10, or an M8P10 email ≠ its print, is a FAIL of the COMBINATION: report it as such (it blocks merging both, not PR #8
   alone; say which order surfaces it).
7. **What a customer sees (human-eye rows, not pixel rows):** open page 1 and page 2 of M8's S13 emailed PDF and its light and dark prints as images and
   say in one line each what a customer sees (one A4 sheet per page, logo present, no clipped price, sans font, no mono fallback).

## N4. PUPPETEER 23 → 25 AT RUNTIME (TIER 1 by the runtime; READ + MEASURED)
**FAIL condition:** any file the hosted runtime LOADS from puppeteer-core other than through its public entry (`require("puppeteer-core")`); the stub's
`CdpBrowser` NOT being the class the renderer's browser is an instance of; a product call whose 23 → 25 behaviour changed without a measured equal §N3
result.
1. **ESM-only, measured (M8 tree):** read `node_modules/puppeteer-core/package.json` (`type`, `exports` for `.` and `./internal/*`, `engines`); say whether
   `.` has a `require` condition, i.e. whether `lib/pdf.js:11` relies on `require(esm)`; while one §N3 render runs, log every `puppeteer-core` file the
   process resolves and the specifier that loaded it (a resolve hook you preload with `--import`/`--require` from YOUR tools dir, or `NODE_DEBUG=module`,
   stated); capture stderr whole at module load and first render and quote any `ExperimentalWarning` (gate 18 WRONG (h)) — on Node 26, and say Node 22's
   behaviour is not measured here unless D7 rules an image.
2. **The stub hits the real class (WRONG (g)):** on the M8 host tree, with `lib/pdf.js`'s shared browser launched, prove `Object.getPrototypeOf(<the
   renderer's browser>) === require("puppeteer-core/internal/cdp/Browser.js").CdpBrowser.prototype` from YOUR harness only (e.g. a prototype method spy
   recording `this` on the renderer's first call), never by editing `lib/pdf.js`. Then **G23-M1** (fresh M8 tree; `lib-close-shared.test.mjs`'s stub
   retargeted at a throwaway `class X {}`; landed; `node --check` rc 0): does its cell still pass? **G23-M2** the same for `fixtures/hang-close.cjs`: does
   BC-F1 (`lib-close.test.mjs`) still pass? Say which cells see each, or NONE (unseen = a finding against the suite, not a FAIL of M8).
3. **API drift, READ:** every puppeteer call in `stage3/lib/pdf.js` and `stage3/lib/xlsx.js` (same blobs in BASE and M8) against the INSTALLED 23.11.1 (BASE
   tree) and 25.0.2 (M8 tree) sources/types: `launch` options and headless default, `newPage`, `setContent`/`goto` + `waitUntil`, `evaluate`, `emulateMediaType`,
   **`page.pdf` options and their defaults** (WRONG (f)), `close`, the `disconnected` event. Table: call, 23, 25, the §N3 row that measured it. READ ONLY
   except where §N3 measured.
4. The two fixtures keep their assertions: `git diff e4ce536 4d6ed6e` of both files whole; every `assert`/`test(` line byte-identical (count them at both).

## N5. NODE 22: THE RUNTIME EXPECTATIONS AS RECORDED (READ; MEASURED only where an image leg is ruled)
**FAIL condition:** a recorded runtime that cannot load the shipped lockfile (a CI job, the Dockerfile or the repo's deploy record pointing at Node
< 22.12); a CI job on `4d6ed6e` whose log shows a Node < 22.12, an `EBADENGINE` warning for puppeteer-core / @puppeteer/browsers / chromium-bidi, or
an ESM load error; the `FROM` line and the lockfile disagreeing (gate 4's "ship together").
1. **CI:** tests.yml at BASE and M8 (same blob `ec450f5`): the five jobs' `node-version`. From the job LOGS of runs 38837565972 and 38837589895 (GH-API-LEG;
   `actions/jobs/<id>/logs`), quote per job the Node version `setup-node` resolved and `npm ci`'s warnings. Say: CI ran `e4ce536`-based trees, not M8.
2. **The image:** the Dockerfile at M8 whole — `FROM node:22-bookworm-slim` (floating, no digest), `npm ci --omit=dev`, apt `chromium` unpinned,
   `ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium`, `RUN node strip.js`, `ENV NODE_ENV=production`, `USER node`, the CMD. Prove the only non-comment change
   vs BASE is the `FROM` line.
3. **The lockfile's engines** (M8): every entry with a `node` engine; the minimum Node the tree accepts; `package.json` has no `engines` (READ), so npm on a
   too-old Node only warns.
4. **App Service as recorded in the repo (WRONG (d)):** quote the repo's deploy lines (`CLAUDE.md` at BASE, the stage3 section; `BACKLOG.md`'s deploy
   records, e.g. the v0.6.1 image-tag line) and show the site runs an image, so its Node is the image's; `git grep -i` for `NODE|`, `WEBSITE_NODE_DEFAULT_VERSION`,
   `WEBSITES_`, `linuxFxVersion` (0 expected beyond the log-show line; a positive control grep that reads ≥ 1 on a known string). RELAY AZ-PRE-READ's
   `DOCKER|…` as the live confirmation; you never read the live host.
5. **The red proof that the FROM line and the lockfile must ship together:** only if D7 rules an image (in-image: the BASE image's Node 20 cannot
   `require("puppeteer-core")` from M8's `node_modules`, read-only mount; quote the error). Under IMAGE-LEG NONE: NOT RUN, named (no Node 20 on the host).

## N6. THE IMAGE LEG (ONLY IF IMAGE-LEG ≠ NONE; else every row NOT TESTED by Tuesday's D7)
Follow gate 18's kit §N2, §N3, §N4 (rows S1, S4, S7, S13 of THIS brief's §N3, not gate 18's six shapes) and §N5.5, and its §13.5 DOCKER DISCIPLINE, with
these substitutions: base image from `437ab4b`, head image from **your extracted M8 tree** (a fresh `git archive`-built context, never a working tree);
platform `linux/arm64` (ARM64-NATIVE) or `linux/amd64` (AMD64); tags and container names `qa-g23-*` only, no registry host; `--pull --no-cache`, base then
head back to back (one build window; a Chromium or font package difference between them VOIDs every cross-image comparison until rebuilt); every product
container `--network none`; deadlines: one build 2400 s (amd64) / 900 s (arm64), one in-container suite 1800 s, one render cell 600 s. **Touch no
foreign docker object** (any `qq-evidence-local:*`, `qa-b23-*`, `qa-g18-*`, `rd846-*`, `vsp-azurite-*`, `pc-*`); never prune, `rmi`, `rm`, push, login or
tag for a registry; your containers are STOPPED and LEFT, listed by id. NX-1 (Docker Hub `node:20-bookworm-slim` / `node:22-bookworm-slim`, Debian apt,
the npm registry inside the build) is the ONLY egress this leg adds; record every digest it resolved.

## N7. THE TWO DEPENDABOT ALERTS CLEARED, AND NO NEW ADVISORIES (TIER 1; READ + MEASURED)
**FAIL condition:** `extract-zip` (any version, any nested path) in M8's or M8P10's lockfile or installed tree; `yauzl`, `basic-ftp`, `proxy-agent` resolvable
at M8; a package ADDED or CHANGED by PR #8 with any open advisory in the GitHub Advisory Database at the version the lockfile pins; the dependency-review
compare for the merge showing any vulnerability on an added package; any OTHER manifest in the repo carrying extract-zip.
1. **The lockfile, MEASURED** (python over `git show` and over your installed trees): `extract-zip` absent at H8, M8, M8P10 (every key); present at BASE
   (`node_modules/extract-zip` 2.0.1 + nested `debug` 4.4.3 / `ms` 2.1.3) — the control that the scan can find it.
2. **GitHub's own readings (GH-API-LEG, GET):** `dependabot/alerts?state=open` (expected #1, #4) and the full list (all states; quote each row);
   `dependency-graph/compare/437ab4b...4d6ed6e` AND `…/437ab4b...7378a4e` (the merge ref): `extract-zip@2.0.1` REMOVED with `GHSA-jmr9-qjv8-65gv` and
   `GHSA-7pqw-9j4j-h8q3`; the vulnerabilities on every ADDED entry (drafter: 0 of 14); reconcile by name@version with the lockfile (WRONG (j)).
3. **The advisory DB, per package:** `gh api "/advisories?ecosystem=npm&affects=<name>@<version>"` for every name@version ADDED or CHANGED at M8 (puppeteer-core
   25.0.2, @puppeteer/browsers 3.0.2, chromium-bidi 16.0.1, devtools-protocol 0.0.1608973, webdriver-bidi-protocol 0.4.1, zod 3.25.76, b4a 1.9.0,
   bare-events 2.9.2, bare-fs 4.8.4, bare-path 3.1.2, bare-stream 2.13.4, bare-url 2.5.5, streamx 2.28.1, tar-stream 3.2.2 — your list from the
   lockfile, not this one); **positive control first: `extract-zip@2.0.1` must return both GHSAs** (it did for the drafter at 06:13:5x). Each reading
   timestamped; an advisory published after the read is not yours to know.
4. **npm audit (D8):** RUN → `npm audit --omit=dev --json` at BASE, H8 and M8 (`npm_config_update_notifier=false`; NX-2): per-severity counts and package
   names verbatim; M8 must be 0 of every severity. NOT-RUN → the READY's "high 3 → 0" is NOT RUN, named, and §N7.2-3 stand in.
5. **"Cleared" post-merge (READ ONLY, Tuesday's):** state what Tuesday must read after a merge: #1 and #4 `state: fixed` with `fixed_at` after the merge
   commit, on manifest `stage3/package-lock.json`; main's code-scanning still 0 open.
6. Code scanning open on main, `refs/pull/8/head`, `refs/pull/8/merge` (0 / 0 / 0 at drafting) — blind (WRONG (o)); never dismiss an alert.

## N8. GITLEAKS (TIER 1 by the image; MEASURED)
**FAIL condition:** any gitleaks finding in PR #8's commits or in M8's tree that is not also present at BASE (a BASE finding is pre-existing: report it,
do not grade PR #8 on it); a scan whose positive control did not fire.
1. **Positive control first:** a scratch COPY of your M8 tree (never the repo) with one planted throwaway credential-shaped string (a fake AWS access key
   id pair, generated by you, never a real one) in a new file: `gitleaks dir` must report it. Then remove the copy by quarantine.
2. **History:** `GIT_OPTIONAL_LOCKS=0 gitleaks git --no-banner --redact --log-opts="e4ce536..4d6ed6e" --report-format json --report-path <your evidence>`
   pointed at the repo path (PR #8's own commits; the two merge commits included); and the same for `e4ce536..437ab4b` (main's side, for the base
   comparison). Record the repo's `.git/index` mtime before and after.
3. **Trees:** `gitleaks dir --no-banner --redact` over your extracted BASE and M8 trees **without `node_modules`**, and separately over M8's installed
   `stage3/node_modules` (report counts and rule ids only; third-party test fixtures are expected noise — classify each, never print a value).
4. gitleaks version (8.30.1 at drafting), the config used (default unless the repo carries one at BASE: say), every finding as rule id + file + line +
   commit, values REDACTED.

## N9. NOTHING PUSHED, MERGED OR PUBLISHED; THE PUBLISH FACTS (commission; READ ONLY)
**FAIL condition:** any `git push`, merge, PR comment/review/label/approval, workflow re-run, alert dismissal, `az` command, deploy, or any HTTP request to
the live QuickQuote or the live portal in your command log; any write in the QuickQuote repo or in `Vision_Sales_Portal/`; under IMAGE-LEG NONE any
`docker` command of any kind; under an image leg any docker object of yours not named `qa-g23-*` or any `push`/`login`/registry tag; the live webapp's
`linuxFxVersion` at verdict (Tuesday's re-read) differing from AZ-PRE-READ without an explanation that is not you.
1. **Your own discipline, MEASURED:** your shell history grepped for `push`, `merge`, `docker`, `az `, `gh pr`, `-X`, `azurewebsites.net`,
   `hpas-quickquote` as a URL host (each beside a positive control that reads 1); `stat` the repo's `.git/index` mtime at start and end.
2. **The Azure side (AZ-READ-LEG = TUESDAY-READS):** RELAY the `AZ-PRE-READ` line appended to your prompt; the post-read is Tuesday's at verdict.
3. **What a publish would ship after a merge (READ ONLY):** from the AZ-PRE-READ tag's trailing sha (expected `…-437ab4b`): with PR #8 alone merged, the
   delta is M8's five files and the image's new base layer (Node 22) and Chromium-driver stack (puppeteer 25); with PR #10 also merged, add P10's eight files
   (gate 22 §N8.3). **Say plainly: a publish built from a main that carries PR #8 ships the new runtime, whatever card authorised the publish** (WRONG (l)).
4. **Deploy-on-merge (READ ONLY):** `.github` at M8 holds only `tests.yml` (no deploy, no image build, no registry login); if GH-API-LEG allows: repo hooks,
   environments, deployments. State whether a merge deploys anything, with each statement's evidence class.

## N10. CI AND CODEQL ON PR #8 (READ ONLY; never caused)
**FAIL condition:** a tests.yml run on `4d6ed6e` not `success` on all five jobs; a CodeQL check run on `4d6ed6e` failing; any alert dismissed.
1. GH-API-LEG = READ-ONLY-VISION-TOKEN: `actions/runs/38837565972` (push) and `/38837589895` (pull_request) — READ-BY-DRAFTER `completed success`: head_sha,
   conclusion, their `/jobs` (five, each `success`), the print-fit log's `# tests` line (READY: 170); the dynamic CodeQL run 38837588311;
   `commits/4d6ed6e…/check-runs` (13 at drafting, all success); `actions/runs?head_sha=7378a4e…` (0 at drafting: M8 has no CI — WRONG (b)).
2. **What a merge needs (READ ONLY, WRONG (b)):** whether the repo's ruleset requires a CodeQL result for the CURRENT merge ref (rulesets/branch
   protection reads if the token can; otherwise UNVERIFIED). Say what Tuesday should expect at merge time; never cause a run.

## 12. The merge, the order, and PR #10
QQPB is 3 ahead and **4 behind** `437ab4b`. A GitHub merge commit of PR #8 onto `437ab4b` has tree `8077fdc` = M8 (your §N1.3 proof). **The verdict is on
M8 (and H8); it holds only while main is `437ab4b`.**
**THE ORDER, measured (report both; the ruling is Tuesday's):**
- **(A) PR #10 first, then PR #8:** PR #10 lands on `437ab4b` exactly as gate 22 gated it (7 ahead, 0 behind; tree `ee51fa7`), and its publish (Kam's open
  card) ships the v2.39 page on the CURRENT runtime (Node 20, puppeteer 23). PR #8 then merges onto `437ab4b`+PR #10; the result is M8P10 (§N3.6 is that
  tree's evidence). PR #8's own publish stays a separate Kam word (C-20).
- **(B) PR #8 first, then PR #10:** main moves to M8; PR #10's gate-22 GO WITH FINDINGS was on `f31720e` over `437ab4b`, so gate 22 §12's re-run cells apply
  (its N6 suites, N2.2 head runs, N3.2 grid with N4, N11 U-AT / U-OVER / F-AT / F-UNDER / B-STATE, P3′, P11) — **§N3.6 here covers part of that; say exactly
  which of gate 22's re-run cells this gate's M8P10 rows do and do not cover.** And **the v2.39 publish would then carry Node 22 + puppeteer 25** (WRONG (l)).
- **Cells to re-run at merge, either order:** tests.yml's five jobs on the merge commit; CodeQL on the merge; Dependabot #1 / #4 reading `fixed` (§N7.5).
  **At publish (Kam's word, not this gate):** the ACR build's own amd64 image re-running §N3's S1, S4, S7, S13 and the live page's first emailed quote.

## 13. FLOOR AND PORT DISCIPLINE — Vision has NO jest lock, plus THE DEADLINE RULE (and HELD)
**There is no shared lock or queue on this project, and you must NOT borrow NexusAI's.**
1. **Never use `4848` (portal), `8080` (QuickQuote's stage3 dev port) or `47787` (Tuesday's dashboard)** on the host. Host product processes take
   ports from the kernel (`listen(0)`) and bind `127.0.0.1`. **If an instrument needs a FIXED port, use only `47310`-`47319`** (`lsof` rc 1 = free at
   drafting, 06:12; re-check before binding). **Never start the hosted server module's own entry point; use its `createApp()` export.**
2. **Every host product process runs under `env -i` with an explicit ALLOWLIST** (PATH; HOME = a fresh mktemp dir; NODE_ENV = `test`, never
   `production`; `PUPPETEER_EXECUTABLE_PATH` = YOUR egress-block wrapper; `npm_config_update_notifier=false`; `npm_config_offline=true` except §N7.4 under
   D8 RUN; `npm_config_cache` = the user cache, read for `npm ci --offline` only). **NEVER set in a product process:** `AGENTMAIL_API_KEY`,
   `AGENTMAIL_INBOX` (with both set, QuickQuote SENDS FOR REAL), any real `ACS_*` / `MAIL_SENDER`, `TABLES_CONNECTION_STRING`, `SALES_COPY_EMAIL`, `HPAM_WORD`,
   `ADVANCED_UNLOCK_SECRET`, `SESSION_SECRET`, `WEBSITE_SITE_NAME`, `GH_TOKEN`, `GITHUB_TOKEN`. Print each product process's env KEY NAMES (never values)
   and assert none is forbidden. `NTFY_SERVER=http://ntfy.invalid`; never contact ntfy.sh.
3. **EGRESS INCLUDING CHROME CHILDREN:** the page calls public FX APIs whenever the currency is not USD, in the drive Chrome AND in the renderer's
   Chrome. Every Chrome runs under YOUR copy of the egress-block wrapper; prove the block with its positive control (`qa-egress-posctl.mjs`) and run the
   net-log scan at the end; record GoogleUpdater and chrome_crashpad_handler at start and end (`qa-chrome-census.py`).
4. **Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid** (`qa-floorcount.py`, copied). **Negative controls, same run, must classify
   FOREIGN.** The launcher DERIVES the negative-control seats live from the cockpit panes (the `tuesday` pane required; the `Datasec/Vision_Sales_Portal`
   builder pane and any live `QA/*` / `fleet-monitor` pane if present — no builder pane is live at drafting) and appends them to your prompt. **A zero is
   reportable only beside a control that fired in the same window. Take it at START and at END.** **Record the 1-minute load beside every timing**
   (1.55 at drafting, 06:12).
5. **ONE BROWSER AT A TIME.** Never two drive Chromes of yours alive at once (the suites' own Chromes count); never a suite and a §N3 drive concurrently.
   Inside a §N3 send the renderer's headless Chrome runs while the drive Chrome is open: that pairing is mandated; release both in each cell's `finally`.
6. **THE DEADLINE RULE:** every step has a written DEADLINE built into your runner (no `timeout` binary here) and a client timeout on every request;
   a step past its deadline is ABORTED and reported. Deadlines: one browser cell 120 s; one red-proof or mutant arm 420 s; root pack 120 s; a whole `npm
   test` 300 s; a whole `test:xlsx` 300 s; a whole `test:print` 900 s; nothing above 900 s on the host (the image leg's own deadlines are §N6). One retry
   per cell at most, then NOT RUN with the load. **Every Chrome, page, child, app server, container and temp profile you start is released in a
   `finally`.** **Log a HEARTBEAT line (timestamp, step, pid, elapsed, load) at least every 2 minutes; a step with no heartbeat for 5 minutes is aborted
   and reported.**

**Reap everything you start.** An orphan Chrome or listener of yours is someone else's foreign process.

### Drivable surface — LOCAL ONLY. **NEVER the live QuickQuote or the live portal.**
- **NEVER the live** QuickQuote (`hpas-quickquote`, `hpas-quickquote-rg`, `hpasqqacr`, its Table Storage, its log workspace) and **NEVER the live**
  portal (`https://datasec-sales-portal.azurewebsites.net`, resource group `datasec-sales-portal-rg` — PRODUCTION). **No HTTP request to either, nor to any
  `azurewebsites.net` host, not even a GET. Press nothing there. No az at all — no writes, no app-setting change, no deploy, no publish, no ACR build, no ACR
  push.** Never the FX hosts (blocked by your wrapper), never ntfy.sh. **Never Claude in Chrome** (Kam's real Chrome with his sign-ins). Never open anything
  under `Vision_Sales_Portal/4_Credentials/` (the launcher wires the gh config itself), and never read, ask for or type the HPAM word.
- **No email to any human address.** Every send goes to the capturing stub mail; recipients are your sign-in address on a `.invalid` domain
  (`@qa-g23.invalid`, lower-case) and `sales-copy@qa.invalid`. Your own AgentMail calls go only to `tuesday-agent@agentmail.to`.
- **Network, and ONLY this:** `git ls-remote origin`; `gh api` GETs (GH-API-LEG); your AgentMail calls; **NX-1 only if D7 rules an image leg; NX-2 only if
  D8 = RUN.** Nothing else reaches the internet: no npm registry otherwise (`npm ci --offline`), no image pulls otherwise.

### HELD
- No merge, no deploy, **no publish**, **no registry push**, **no production**, no money, **no mail to any human**, no external comms. **No comment,
  review, label, approval or status on PR #8, PR #10 or any GitHub object; no re-run of any workflow; no alert dismissal of any kind.**
- **Under IMAGE-LEG NONE: No `docker` at all** (not a build, not a run, not even `docker images` or `docker ps`). Under an image leg: §N6's discipline.
  **No `npm install`, no `npm ci` without `--offline --ignore-scripts` on the host, no `npm audit fix`, no `npx` of anything not already in your tree. `gh`
  only as GH-API-LEG allows; no `az`.** The launcher points `AZURE_CONFIG_DIR` at an EMPTY directory.
- **Trees:** build every tree INSIDE YOUR OWN PROJECT from the object store (`git -C <repo> archive <sha> | tar -x -C <fresh mktemp -d under
  projects/vision/work-g23/>`, in `/Volumes/Laptop-DEV/!CODING/Testing Agent MAIN`), M8 and M8P10 by §N1.3's overlay. **Each tree is EXCLUSIVE to this gate
  and to ONE purpose; never touch any other `work*` directory** (`work-g19` … `work-g22` included). In the repo use ONLY read verbs (show, log, diff,
  ls-remote, rev-parse, ls-tree, cat-file, grep, merge-base, archive; gitleaks' own `git log` under `GIT_OPTIONAL_LOCKS=0`); **never fetch, pull, checkout,
  switch, worktree, commit, stash, reset, clean, gc, branch, revert or for-each-ref.** `merge-tree --write-tree` only from your OWN object dir.
- **CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY:** every control is a separate measurement that could have come out the other way on its own. **For this
  gate: BASE-vs-BASE equal before any BASE-vs-M8 zero; the comparator reports a planted one-word, one-digit, one-pixel and one-cell change; the extract-zip
  scan FINDS it at BASE; the advisory DB returns both GHSAs for `extract-zip@2.0.1`; gitleaks finds its planted string; the fixture revert of §N2.3 goes red;
  each mutant is shown LANDED; the tree-hash method reproduces `c71780c` for BASE unchanged; the egress block's positive control fires; the floor count
  rises on its attached control.** A control derived from the run it validates is not a control.
- **Findings only:** do not commit, do not move any branch, do not file a ticket. **Make no writes in the QuickQuote repo** (its working tree is the
  builder's, live) **and none inside `Vision_Sales_Portal/`**, none in gate 1-22's report folders or trees. Describe fix-shapes in prose.
- **NEVER `rm`.** Quarantine instead.

## THE MODEL RULE
(Kam, live board 2026-09-30 09:07, card `nexusai-gate11-opus55-safeguard-model-switch`, option (b) — QA gates may switch to Opus 4.8 when flagged,
PER SESSION.) You start on Opus 5.5 (the launcher reads the model id from Tuesday's `0_Brain/dashboard/data/models_latest.json`, `claude-opus-5-5` at
drafting). You run the FULL rows. If one of your responses is stopped by the safeguards: that step is NOT RUN (never re-worded to slip past); write ONE
line to `evidence/classifier-stops.txt`; reap any Chrome, app server and container you started; mail `tuesday-agent@agentmail.to` with the subject exactly
`[QA/Datasec-Vision -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch`;
then end your turn with the line `PARKED: flagged — awaiting the Opus 4.8 switch` and wait. Tuesday switches THIS pane's model and taps you by mail. You
never answer the model dialog yourself, and nobody ever chooses "Switch automatically". After the switch, resume at the stopped row. The report states
which rows ran on which model, with the switch time, and quotes `classifier-stops.txt` whole.

## TUESDAY'S RULINGS AT STAMP (2026-10-18)
**R1-R7 are the commission's requirements as Tuesday wrote them to the drafter (2026-10-18 ~06:0x), carried as ruling lines. Apply them; do not
re-rule them.**
- R1: ONE gate, TIER 1, Vision gate 23, on QuickQuote PR #8 (puppeteer-core 25 + node 22; C-19), which also clears Dependabot extract-zip alerts #1 and #4 on main; gated against CURRENT QuickQuote main (437ab4b), saying how it interacts with PR #10 (v2.39, gate 22 GO WITH FINDINGS, not merged, waiting on Kam's publish card): merge order and conflicts measured with the GitHub compare API, never a merge-tree in their repo.
- R2: Dependency-upgrade correctness: the PDF, the workbook and the email generation byte-or-semantically equal on a fixed synthetic quote set against main.
- R3: The Node 22 runtime expectations in CI and in the App Service config as recorded in the repo; never read the live host.
- R4: The two Dependabot alerts actually cleared (code-scanning / Dependabot API reads); no new advisories.
- R5: gitleaks.
- R6: NOTHING published: live QuickQuote is production; publishing is Kam's word only (C-20); no az; no HTTP to the live QuickQuote site or any azurewebsites host.
- R7: Findings only; the tester never fixes.

**Drafter's open decisions for Tuesday (the launcher refuses until each RULED line is stamped):**
- **D4 — Class count and vocabulary.** *Drafter:* QQPB, **round 1 at a launched gate** (gate 4 gated `0d45100`; gate 18 never ran); GO / GO WITH FINDINGS /
  NO GO. A NO GO returns PR #8 to the builder for a round 2 (forward-merge + fix), not to Kam. A GO / GO WITH FINDINGS releases a MERGE on Tuesday's word
  (C-19) **only while main is `437ab4b` and only in the order Tuesday rules (§12)**; it never releases a publish (C-19 "not covered"; C-20: Kam's own
  word). **If §N2 at M8 (the four suites as sets), §N3's S1-S12 at BASE and M8 with the BASE-vs-BASE control, §N7.1-§N7.3, or §N8.1-§N8.2 are NOT RUN
  (deadline, load), the verdict is PROVISIONAL — it releases nothing.** §N3.6 (the interaction column), §N4.2's mutants, §N6 and the human-eye rows NOT
  RUN do not make it provisional; they are NOT TESTED lines, and a NOT RUN §N3.6 means order (B) is unmeasured. RULED: (Tuesday, 2026-10-18 06:39) as the drafter reads it. Round 1; GO / GO WITH FINDINGS / NO GO; a NO GO returns PR #8 to the builder (forward-merge + fix), not to Kam; a GO releases a MERGE only, only while main is 437ab4b, in the order Tuesday rules at verdict; never a publish (C-19, C-20). The PROVISIONAL clause stands as written.
- **D6 — TARGET-MODE.** *Drafter's reading:* MERGE-TREE — the tree that would land (M8 = `8077fdc`, = GitHub's own test merge, reproduced read-only) is
  what a merge commit produces, and gating it costs no builder round; the cost is that CI and CodeQL have not run on it (WRONG (b)), which the gate
  states and Tuesday reads at merge. FORWARD-MERGE-FIRST follows C-19's scope line literally and gets CI on the real tree, at the price of a builder
  round and a re-brief. Set the `TARGET-MODE:` line. RULED: (Tuesday, 2026-10-18 06:39) MERGE-TREE. Gate M8 (8077fdc) and H8. Reason: M8 is what a merge commit produces and gating it costs no builder round; CI and CodeQL on the merge commit are read by Tuesday at merge time, before any GO is used.
- **D7 — IMAGE-LEG.** *Drafter's reading:* NONE, because the commission scopes Node 22 as a READ ("as recorded in the repo"). **Weigh against:** gate 18's
  stamped-at-draft R2 ("Build the image from the PR head for linux/amd64 and run it; the gate verifies amd64 itself") and C-19's own evidence list (the image
  built locally with the PDF path run inside it — the builder did arm64 only, and its amd64 re-run timed out under emulation). Under NONE no gate ever
  executes Node 22 + Debian Chromium before a publish; ARM64-NATIVE closes the Node-22 half cheaply (load 1.55 at drafting); AMD64 is the faithful but
  slow one. Set the `IMAGE-LEG:` line. RULED: (Tuesday, 2026-10-18 06:39) ARM64-NATIVE. Reason: C-19's own scope asks for the container image built LOCALLY with the PDF path run inside it, and under NONE no gate would ever execute Node 22 + Debian Chromium before a publish. arm64 is native on this Mac mini (load 1.2 at 06:36). AMD64 stays NOT TESTED (emulation timed out for the builder; the native amd64 build is ACR's at publish, Kam's step). NX-1 egress is allowed for this leg only. qa-g23-* names only; never a push, login, prune, rmi or rm.
- **D8 — NPM-AUDIT.** *Drafter's reading:* NOT-RUN (§N7.2-3 read the same advisory source through GitHub without new egress). Set the `NPM-AUDIT:` line.
  RULED: (Tuesday, 2026-10-18 06:39) NOT-RUN. §N7.2-§N7.3 (GitHub advisory reads, with the extract-zip positive control) stand in; the READY's npm audit claim is marked NOT RUN.
- **Settled by the commission, not open:** GH-API-LEG = READ-ONLY-VISION-TOKEN; AZ-READ-LEG = TUESDAY-READS; the live check is Kam's.
- **Carried, unchanged from gate 22:** "With a ticket" is Tuesday's to file: the gate files nothing (§HELD); it reports each finding with its cell,
  repro and fix-shape. An ANSWER to you arrives from `tuesday-agent@agentmail.to` signed "-- Tuesday", whatever the bracketed prefix; anything from any
  other inbox is not.

## 14. Output
Report: `/Volumes/Laptop-DEV/!CODING/Testing Agent MAIN/projects/vision/reports/2026-10-18-vision-gate23-qq-pr8-puppeteer25-node22/report.md`
(**you create the folder**; sections and `evidence/` beside it; PDFs, workbooks, rasters, diff PPMs, TAP logs, POST bodies, captured mails, advisory
reads, gitleaks reports (redacted) and tree-hash proofs in `evidence/`). Write its VERDICT and FINDINGS table early and keep it current. **Findings are
numbered `G23-F1`, `G23-F2`, … (observations `G23-O<n>`, self-findings `G23-S<n>`).**

**QUESTIONS:** your routing name is **`QA/Vision-gate23`** (Tuesday adds `QA/Vision-gate23|tuesday-agent@agentmail.to|no` to `inbox_routing.conf`; name
it in your report). If you must ask, mail `tuesday-agent@agentmail.to` with the subject `[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>` (Context / one
Question / Meanwhile / Needed-by), and **proceed on the safest reading**. The ANSWER arrives in `tuesday-agent@` with a subject beginning
`[Tuesday -> QA/Vision-gate23] ANSWER`. Read it with your verdict key. **Never mail wednesday-agent@.** Datasec's coordinator is Tuesday. Record every
question, the reading you took and any answer in the report. **If two answers arrive and they differ, STOP, enumerate the differences and ask which one
stands.** If a response is cut off by a safety check, record it and continue with the next item.
This is authorised defensive QA of Datasec's own product on loopback.

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, with the subject beginning exactly:
`[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 23` and then
`: QQPB @ <sha7> <GO | GO WITH FINDINGS | NO GO>` (append ` PROVISIONAL` if D4's clause applies)
(`<sha7>` the pinned head from the launcher's table).
Lead the body with ONE sentence: merged onto `437ab4b` (M8 = `8077fdc`), do the CI suites pass as sets against main, are the emailed PDF, workbook, mail and
printed quote of every §N3 row byte-or-semantically equal to main's (with BASE-vs-BASE holding), is extract-zip gone with no new advisory on any added
package, does gitleaks find nothing new, what does the combination with PR #10 do, and was anything pushed, merged or published?
Then one line each on: M8's tree proof; the suites as sets (M8 vs BASE, M8P10 vs P10, H8 vs the READY); §N3 per row ((i) byte / (ii) semantic / FAIL);
the interaction column and the order (A)/(B) facts; the puppeteer runtime (ESM load, stub identity, G23-M1/M2, `page.pdf` defaults); Node 22 as recorded
(CI's resolved versions, the FROM line, engines, App Service = image) and the image leg per D7; the alerts (lockfile, dependency review, advisory DB, npm
audit per D8, the post-merge read Tuesday owes); gitleaks; the live site read (RELAYED from AZ-PRE-READ); what a publish would ship; the class count (D4).
You have no inbox that wakes you, so a verdict you do not mail is lost.

AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/Laptop-DEV/TUESDAY/4_Credentials/.env`. The path is absolute because the QA project has no
credentials directory of its own. Use the key ONLY in your own verdict/question/answer-read `curl`, with a client timeout (`-m 30`). It must never enter
a product process's or a container's environment. **Never put the key, or any secret, in a mail or the report.**

Verdict format:
- **One verdict, GO / GO WITH FINDINGS / NO GO (PROVISIONAL per D4)**, naming the pinned sha, the branch and M8's tree; and in the mail body, its own
  line: `VERDICT: <token>, round 1 (<PROVISIONAL or not, and why>). <what happens next: Tuesday's merge GO in the order she rules; the publish is Kam's>`.
  Then §N1's hunk table and tree proofs, §N2 as sets, §N3's row table (row × artefact × (i)/(ii) × BASE sha256 / M8 sha256 × load), §N3.5's controls,
  §N3.6, §N4-§N10 row by row, §12's order table.
- **A table with one row per §N item: MEASURED / NOT TESTED / NOT RUN / VOID, and HOW (command, tree, browser, port, load).** No row without a HOW.
- **Rule 2: what you did NOT test is first-class output.** A NOT TESTED section covering at least **Node 22 itself unless an image leg ran (host Node
  is 26.8.1; CI is READ)**, **the published amd64 image and ACR's native build**, **the image's own CMD booted with production settings (WRONG (m))**, **a real
  ACS send (stub mail only)**, **the live site (Kam's check)**, **CodeQL's verdict on the current merge ref (WRONG (b), (o))**, **Dependabot #1 / #4 reading
  `fixed` (post-merge, Tuesday's)**, **store-azurite on M8 (CI read on `4d6ed6e` only)**, **npm audit (per D8)**, **a live FX provider**, **currencies other than
  AUD/USD/CAD**, **Windows / Safari / the account managers' real browsers, real phones and real printers**, **a customer's mail client**, **Claude in Chrome (not
  used)**, and every §N row you did not run, with the reason. **Every action recommendation carries its evidence class: MEASURED AT RUNTIME / PROBED /
  READ ONLY.**
- Report the pinned head and main as three timestamped readings (**start / mid / end**), each with its branch name, plus `refs/pull/8/head`,
  `refs/pull/8/merge` and `refs/pull/10/head`.

PROVENANCE:
- heads: main `437ab4bc412b…` (= HEAD), `fix/qq-puppeteer-25-2026-09-22` `4d6ed6ef403e…` = `refs/pull/8/head`, `refs/pull/8/merge` `7378a4e1206a…`,
  `fix/qq-email-matches-print-2026-10-16` `f31720ee677d…` = `refs/pull/10/head`, `refs/pull/10/merge` `75d7a8e9…`, `backlog/qq-extract-zip-2026-10-16`
  `01c8d7f9…` | `git -C <quickquote on Laptop-DEV> ls-remote origin` | read 2026-10-18 06:09:46-06:09:49 AEDT
- the chain, counts 3 ahead / 4 behind, merge-base `e4ce536`, main's 4 commits since `e4ce536` and their numstat, PR #8's numstat, the `package.json` diffs on
  all three sides, the four PR-#8 diffs whole, blobs at `e4ce536` / `437ab4b` / `f31720e` / `4d6ed6e`, trees | `log`, `rev-list --count`, `merge-base`, `diff
  --numstat`, `diff`, `rev-parse <sha>:<path>`, `cat-file -t` | read 06:10:02-06:11
- M8 / M8P10: merged `package.json` blobs by `sed` + `git hash-object --stdin` (no `-w`); tree hashes by a read-only python over `git ls-tree -z`
  (controls: `c71780c` for `437ab4b` unchanged, `01bdc92` for `4d6ed6e` from `e4ce536`) | run under bash | 06:11-06:20
- `puppeteer` references at `437ab4b` / `f31720e` / `4d6ed6e` (`git grep`); the head lock's engines and entry counts, main's extract-zip entries (python over
  `git show`); tests.yml whole; `CLAUDE.md` stage3 section at `437ab4b`; `git grep -i` for App Service runtime settings | read 06:10-06:15
- GitHub (READ-BY-DRAFTER, `gh api` GET with Vision's gh-config, `GH_NO_UPDATE_NOTIFIER=1`; its two files' mtimes unchanged, 12 Oct 18:09): PR #8 (body
  whole, open, clean, 5 files, +85/−522, base.sha `e4ce536`, merge_commit_sha `7378a4e`); commit `7378a4e` (parents, tree `8077fdc`, 5 files); compare
  `main...4d6ed6e`, `437ab4b...7378a4e`, `4d6ed6e...f31720e`, `f31720e...4d6ed6e`; runs for head_sha `4d6ed6e` (3) and `7378a4e` (0); check-runs on `4d6ed6e`
  (13); Dependabot alerts (open #1 #4; all 16); dependency-graph compare `437ab4b...4d6ed6e` and `437ab4b...7378a4e`; code-scanning open main / pr8 head / pr8
  merge (0/0/0); repo merge settings; advisories `puppeteer-core@25.0.2` (0), `extract-zip@2.0.1` (both GHSAs), `GHSA-jmr9-qjv8-65gv` and
  `GHSA-7pqw-9j4j-h8q3` | read 06:10:17-06:13:59
- the READY (read whole, sha256 `201da80e…`); CLARIFICATIONS C-19, C-20 (whole); decisions.json QuickQuote cards; Vision `CLAUDE.md` QuickQuote section;
  Tuesday's `0_Brain/daily_tuesday/2026-10-16.md` 14:01 / 14:09 and `2026-10-18.md` 05:31 (the Vision wrap) | read 06:0x-06:1x
- gate 22's kit (whole) and launcher (whole), gate 21's launcher (structure diffed against gate 22's), gate 18's kit (whole), its drafter report and
  launcher's docker guards; gate 22's report (sha256, its PR #8 lines, §12, verdict), its `evidence/tools/` listing | read 06:0x-06:2x
- host: node v26.8.1 only (`which -a node`, `/opt/homebrew/opt`), gitleaks 8.30.1, pdftotext/pdftoppm/pdfinfo present, Google Chrome 155.0.8059.84 (`--version`),
  load 1.55 1.57 1.52, `47310-47319` free, tmux panes `tuesday` and `fleet-monitor` only, `inbox_routing.conf` ends its Vision lines at `QA/Vision-gate22`
  (line 229), `models_latest.json` opus = `claude-opus-5-5`, the npm cache index holding the tarballs named in §N2.1 | 06:12-06:2x
- **DISCLOSED:** the drafter ran ONE `docker version --format '{{.Server.Version}}'` (read only; server 29.7.2) while checking host tools. No other docker
  command, no merge-tree, no fetch, no product process, no browser, no `az`, no npm, no mail. `gh` was used for GET reads only.
