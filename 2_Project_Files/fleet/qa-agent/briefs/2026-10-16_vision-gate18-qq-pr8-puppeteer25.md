# QA Agent Invocation Brief — Datasec/Vision_Sales_Portal, GATE 18: ONE TIER-1 QuickQuote gate — PR #8 (puppeteer-core 25.0.2 + node:22 stage3 image) @ `4d6ed6e` on QuickQuote main `e4ce536` — one verdict, one report

**TIER 1 (the shipped build image + the quote PDF a customer receives). FULL WEIGHT: the image built from the PR head FOR linux/amd64 and RUN,
the server path inside it, the suites CI runs, and a base-vs-head comparison of every quote artefact.** ROUND 1 of PR #8 (the branch's second gate:
gate 4 gated it as P5B at `0d45100`, see PRIOR ROUND). A NO GO sends it to its round 2; it does not go to Kam.

**Drafted for Tuesday on 2026-10-16 between 12:58 and 13:3x AEDT by a read-only drafting agent. Tuesday reviews, stamps and launches it.**
Templates: `BRIEF_TEMPLATE.md`, gate 17's brief `2026-10-13_vision-gate17-qq-quality-round.md` (section shape, QuickQuote standing rules, the
GET-only gh leg) and the NexusAI batch-23 launcher (the Laptop-DEV re-base, the live negative-control derivation, the model read, the docker
discipline). **This brief governs where they differ.**

**WHY THIS GATE BUILDS AND RUNS IMAGES (gate 17 forbade docker).** The change is the RUNTIME: `FROM node:20-bookworm-slim` → `node:22-bookworm-slim`
and puppeteer-core 23.11.1 → 25.0.2, which drives the Chromium that renders every emailed quote PDF. Kam's ruling C-19 requires "the container image
built LOCALLY for evidence only (never pushed to ACR, never a release tag) with the PDF path run inside it". The hosted App Service runs
**linux/amd64**; every image the builder MEASURED is **arm64** (its READY, NOT TESTED line 1), and its amd64 run was still going when it wrote.
**So this gate builds BOTH images itself, for linux/amd64, and never relies on the builder's STATUS mail or the builder's images.**

The builder's READY mail under test (on disk, read whole by the drafter):
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-16_vision-qq-pr8-READY-mail.txt`
**Every builder statement below comes from that mail, the commit messages or the code at each sha. Each one is a CLAIM. Every red, every
mutant, every suite set, every image and every comparison is RE-DERIVED by the gate. None is taken from the READY.**
The launcher parses §PIN, refuses any placeholder, and re-reads every row (and `refs/pull/8/head`) by `git ls-remote` immediately before launch,
refusing on any mismatch, **including any move of QuickQuote main** (this gate pins main exactly). The verified table is appended to your prompt.

SELF-CHECK: re-read end-to-end for contradictions | @STAMP@
Self-check note: @STAMP@

GH-API-LEG: TUESDAY-DECIDES
<!-- Decision D1. READ-ONLY-VISION-TOKEN = the launcher exports GH_CONFIG_DIR = Vision's .gh-config behind a GET-only `gh` shim first on PATH
     (gate 17's D1, ruled READ-ONLY-VISION-TOKEN 2026-10-13 10:39). NOT-RUN = GH_CONFIG_DIR empty, every GitHub read NOT RUN, the drafter's
     readings stay READ-BY-DRAFTER. The launcher refuses while this line reads TUESDAY-DECIDES. -->

AZ-READ-LEG: TUESDAY-DECIDES
<!-- Decision D2. Exactly one of:
       TUESDAY-READS  Tuesday reads the live webapp's linuxFxVersion (and, if her identity can, hpasqqacr's hpas-quickquote tags) herself
                      BEFORE launch and writes it on the AZ-PRE-READ line below; she reads it again at verdict. The gate runs NO az and
                      RELAYS both readings. The launcher refuses TUESDAY-READS while AZ-PRE-READ still carries the placeholder.
       GATE-SHIM      the launcher exports AZURE_CONFIG_DIR = Vision's .azure behind an az shim first on PATH that allows ONLY
                      `az account show` and `az webapp config show --name hpas-quickquote --resource-group hpas-quickquote-rg` (any
                      --query/-o) and `az acr repository show-tags --name hpasqqacr --repository hpas-quickquote` (any --orderby/--top/-o).
                      Cost: az writes its token cache and command logs INTO its config dir, which is inside Vision's 4_Credentials, so
                      the QA agent would write in the project folder (READ-ONLY-INFERRED from az's config-dir behaviour, not measured).
       NOT-RUN        no Azure reading at all; "live site unchanged" is NOT TESTED.
     Drafter's reading: TUESDAY-READS. The launcher refuses while this line reads TUESDAY-DECIDES. -->
AZ-PRE-READ: @STAMP@
<!-- Under TUESDAY-READS: one line, e.g. `linuxFxVersion DOCKER|hpasqqacr.azurecr.io/hpas-quickquote:<tag> ; ACR tags (newest 5): <...> ;
     read <YYYY-MM-DD HH:MM:SS AEDT> by Tuesday (az, tenant d500ebad / sub 0c57ab37)`. Under GATE-SHIM or NOT-RUN write `n/a`. -->

## Charter
Read `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an independent tester. You did not
build this change and you owe the builder nothing. **Every line below that reports what the builder says is a CLAIM, never evidence.**

**One gate, ONE target, ONE verdict: GO / GO WITH FINDINGS / NO GO, at its pinned sha.**
- **QQPB** at `4d6ed6e` — **TIER 1 (the shipped build image + the quote PDF output).** ROUND 1 of PR #8.
  QuickQuote PR #8, branch `fix/qq-puppeteer-25-2026-09-22`, "stage3: puppeteer-core 25 + node:22 image — clears Dependabot #1 #4 (extract-zip);
  decision 14". Three commits over main `e4ce536`:

| # | commit | parents | what it is |
|---|---|---|---|
| 1 | `3d0167e` (2026-09-22 18:54 +1000) | `47eb533` | "stage3: puppeteer-core 25.0.2 and a node:22 image, clearing the extract-zip advisories" |
| 2 | `0d45100` (2026-09-22 21:51 +1000) | `3d0167e` + `51e9286` | "Merge main 51e9286 forward … (item 11, for gate 4)" — gate 4's P5B head |
| 3 | `4d6ed6e` (2026-10-16 12:49:56 +1100) | `0d45100` + `e4ce536` | "Merge main e4ce536 forward into fix/qq-puppeteer-25-2026-09-22 (PR B, decision 14)" — THE HEAD |

**THE DELTA THAT SHIPS is `git diff e4ce536 4d6ed6e` (5 files, +85/−522), NOT the three commits one by one** (two are merges):

| file | +/− | what (READ at the pinned shas) |
|---|---|---|
| `stage3/Dockerfile` | +4 / −1 | the ONLY non-comment change: `FROM node:20-bookworm-slim` → `FROM node:22-bookworm-slim`; +3 comment lines. blob `8311ebe` → `5972f7c` |
| `stage3/package.json` | +1 / −1 | `"puppeteer-core": "^23.5.0"` → `"^25.0.2"`. blob `61d0d5c` → `94ab2f5`. overrides `uuid ^11.1.1`, `basic-ftp ^6.2.3` kept |
| `stage3/package-lock.json` | +76 / −518 | blob `01c5e5e` → `9366344`. packages map: **40 removed, 1 added (`webdriver-bidi-protocol`), 13 version changes** (below) |
| `stage3/test/fixtures/hang-close.cjs` | +3 / −1 | `require("puppeteer-core/lib/cjs/puppeteer/cdp/Browser.js")` → `require("puppeteer-core/internal/cdp/Browser.js")` + 2 comment lines |
| `stage3/test/lib-close-shared.test.mjs` | +1 / −1 | the same require swap at line 19 |

Lock version changes (MEASURED by the drafter, python over `git show <sha>:stage3/package-lock.json`, 13:0x): puppeteer-core 23.11.1→25.0.2,
@puppeteer/browsers 2.6.1→3.0.2, chromium-bidi 0.11.0→16.0.1, devtools-protocol 0.0.1367902→0.0.1608973, b4a 1.8.1→1.9.0, bare-events
2.9.1→2.9.2, bare-fs 4.8.0→4.8.4, bare-path 3.1.1→3.1.2, bare-stream 2.13.3→2.13.4, bare-url 2.5.1→2.5.5, streamx 2.28.0→2.28.1, tar-stream
3.2.0→3.2.2, zod 3.23.8→3.25.76. Removed (40): the extract-zip / yauzl / fd-slicer / pend chain, proxy-agent, pac-proxy-agent, pac-resolver,
degenerator, get-uri, basic-ftp, socks, socks-proxy-agent, smart-buffer, netmask, @tootallnate/quickjs-emscripten, ast-types, escodegen, esprima,
estraverse, esutils, source-map, data-uri-to-buffer, lru-cache, proxy-from-env, unbzip2-stream, through, get-stream, undici-types, @types/node,
@types/yauzl and their nested debug/ms. **engines (head lock): puppeteer-core 25.0.2 and @puppeteer/browsers 3.0.2 `node >=22.12.0`; chromium-bidi
16.0.1 `>=20.19.0 <22.0.0 || >=22.12.0`.** http-proxy-agent and https-proxy-agent remain in the head tree.

**Same blob at base and head (READ, `rev-parse <sha>:<path>`):** `index.html` `447b129`, `stage3/server.js` `a854ba2`, `stage3/lib/pdf.js`
`783ebea`, `stage3/lib/xlsx.js` `10bf4d7`, `stage3/strip.js` `2fc3bd6`, `.dockerignore` `acf7db8`, `.github/workflows/tests.yml` `ec450f5`.
**So the page, the server and the renderer's own code do not change: everything this gate can see differ is the RUNTIME (Node, puppeteer-core,
the image's base layer) — and that is exactly what it must look for.** Head tree `01bdc92`.

**Names, written out every time:**
- **QQPB** = branch `fix/qq-puppeteer-25-2026-09-22` = PR #8 = "PR B" = gate 4's **P5B** = decision 14 = the delta above. **C-19** = Kam's ruling,
  card `quickquote-decision14-puppeteer25-node22-1016` = (b) "Build the puppeteer 25 + node 22 change now". **MAIN-Q** = QuickQuote main `e4ce536`
  = merge of PR #7 (the dependency round, C-18).
- **"base image"** = the stage3 image the GATE builds from `e4ce536` for linux/amd64; **"head image"** = the same from `4d6ed6e`. **Never** the
  builder's `qq-evidence-local:*` images.

Branch status: **NOT on main. PR #8 is open, not merged** (`gh api …/pulls/8`: state open, merged false, mergeable_state clean, head `4d6ed6e…`,
base `e4ce536…`, read 13:0x — READ-BY-DRAFTER).

## RULED BY KAM, AND SETTLED
- **Vision `1_Project_Definition/CLARIFICATIONS.md`** (`/Volumes/Laptop-DEV/!CODING/Datasec/Vision_Sales_Portal/1_Project_Definition/CLARIFICATIONS.md`):
  read it whole (C-01..C-19, read 13:0x). **Cite only what you open.** The entries this gate turns on:
  - **C-19 (Kam, live board 2026-10-16 12:41:19 AEDT, card `quickquote-decision14-puppeteer25-node22-1016` = (b)):** "Build the puppeteer 25 + node 22
    change now". Scope: "PR B, after PR #7. Forward-merge current QuickQuote main into `fix/qq-puppeteer-25-2026-09-22` … to close Dependabot #1 #4
    (extract-zip). TIER 1: full suites, real PDFs both themes + xlsx before/after on the same fixture, and the container image built LOCALLY for
    evidence only (never pushed to ACR, never a release tag) with the PDF path run inside it. PR, CodeQL + tests.yml green, independent gate, merge on
    Tuesday's GO." **Not covered: publishing the new runtime to the live site (Kam's separate tap), any ACR push, any deploy or Azure change.**
  - **C-18** (the dependency round, PR #7, now main `e4ce536`), **C-17** (the quality round, PR #6, gate 17), **C-16** (v2.34 published as
    `v0.6.2-tool2.34-108bbb4`, rollback `v0.6.1-tool2.33-986f7b8`): background.
- **PRODUCTION IS LIVE for this project.** Live QuickQuote (`hpas-quickquote`, `hpas-quickquote-rg`, its registry `hpasqqacr`, its Table Storage and
  its log workspace) and the live portal (`datasec-sales-portal.azurewebsites.net`, `datasec-sales-portal-rg`) are PRODUCTION. **Nothing in this gate
  touches either** (§13, HELD). The one Azure contact is the AZ-READ-LEG (D2), read-only.
- **Deploys and publishing are HELD for Kam. Nothing merges on your word.** A merge is Tuesday's GO on a pinned head; the ACR build and publish are
  Kam's tap (C-19: not covered).
- **The BUILDER's choices, each judged by the gate (say whether each needs Kam):** (1) puppeteer-core **25.0.2**, not the newest 25.14.0 ("chromium-bidi
  157, unverified against bookworm's Chromium 153"); (2) the `basic-ftp` override kept although now inert (no basic-ftp left in the tree); (3) the two
  test files reach `puppeteer-core/internal/cdp/Browser.js` (an exported subpath) because 25 is ESM-only; (4) the base image stays a floating tag
  (`node:22-bookworm-slim`, not a digest) and Debian `chromium` stays unpinned — both pre-existing patterns, now load-bearing (WRONG (e)); (5) the lock
  rebuilt from main's with `npm install puppeteer-core@25.0.2 --package-lock-only`.

## PRIOR ROUND
PRIOR ROUND: round 1 of PR #8; the branch's previous gate was **gate 4** (2026-09-22), which gated it as **P5B at `0d45100`: "GO, tested only — image
build NOT RUN; Node 22 NOT TESTED" (stale base `51e9286`; held by Kam's decision 14)**.
ITS REPORT IS ON DISK AT: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-22-vision-qq-gate4` (`report.md`,
`sections/P5B.md`, `evidence/`). Read `sections/P5B.md` whole. Its ship note binds this gate: "puppeteer-core 25 is ESM-only and `lib/pdf.js` loads it
with `require()`. That works only on Node ≥ 22.12, so **the lockfile and the `FROM node:22` line must ship together, never apart.**"
Findings carried forward and their disposition: P5B's "image build NOT RUN" and "Node 22 NOT TESTED" → **closed or re-carried by THIS gate (§N2, §N3)**.
The last QuickQuote gate overall was **gate 17** (QQQR GO WITH FINDINGS at `d030674`, conditional on CodeQL post-merge; G17-F1..F3, G17-P1..P3):
`/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-10-13-vision-gate17-qq-quality-round` (`report.md`, `sections/`,
`evidence/`, `evidence/tools/`). Its findings are on code PR #8 does not touch; none is re-graded here. **Then, NOT gated by a QA gate:** PR #7
(`5ad37f1`, the dependency round) merged as main `e4ce536` after **Tuesday's own tier-2 check at source** (Tuesday's daily note 2026-10-16, 12:37 and
12:57 entries). Its open item binds §N4: the seat reported that **the server path and the printed page price the same inputs differently, before AND
after**, and the server report lists **7 unknown print-mode fields (`pmBoth`..`cpPct`)**; Tuesday ruled "MEASURE after PR B, read-only, no fix".
- **The ANCESTRY (READ):** `d030674` (gate 17's head) and `51e9286` (P5B's old base) are both ancestors of `e4ce536`.
- **Instruments are REUSED BY COPY** from gate 17's `evidence/tools/` (on the T9; the latest QuickQuote-shaped set): `qa-run.py`, `qa-g17-lib.mjs`,
  `qa-harness-g17-capture.mjs`, `qa-harness-g17-server.cjs`, `g17-hosted-render.cjs`, `g17-run-suites.sh`, `g17-mutate.py`, `g17-heads.sh`, `g17-gh.sh`,
  `tapsets.py`, `lockcmp.py`, `lockwalk.py`, `qa-chrome-egressblock.sh`, `qa-chrome-census.py`, `qa-egress-posctl.mjs`, `qa-floorcount.py`,
  `qa-harness-floorctl.mjs`, `qa-netlog-scan.py`, `mktree-qq.sh`. **COPY what you use into THIS gate's own `evidence/tools/` on /Volumes/Laptop-DEV,
  read it before you trust it, and RE-POINT every hard-coded path** (gate 17's copies hard-code `work-g17`, the gate-17 report folder and the T9
  volume). **Never edit, run from, or write into gate 1-17's copies, evidence or trees, on either drive.** Record the sha1 of each copy before and
  after your edits. **There is no image instrument to copy:** gate 17 ran no docker. Write your own (`qa-g18-*`), and keep them in `evidence/tools/`.
- **Self-findings from earlier gates bind you:** quote every path (the project path has a space and a `!`; the repo sits under `Quoting Tool/`); run
  every loop and every `git show <sha>:<path>` under **bash, not zsh** (zsh reads `$H:s…` as a modifier); run `node strip.js` before any lone browser
  file; assert every tamper landed before reading its result; npm's update-notifier egresses unless you disable it; record the load average beside
  every timing number; `git branch` and `git for-each-ref` are NOT read verbs here.
- **PRIOR WORK: verify every claim against git history, the Actions API (if GH-API-LEG allows) and gates 4 and 17's evidence, never against this
  brief.** The READY's PRIOR WORK lines (`3d0167e` 2026-09-22, byte-identical PDFs then; `0d45100` for gate 4; PR #7 `e4ce536` in the base; the
  extract-zip ticket `backlog/qq-extract-zip-2026-10-16 @ 88ad5e8`) are each re-derived or marked UNVERIFIED.

## PIN — HEADS (parsed and verified by the launcher)
**The launcher enforces these rules:** every row has a 40-hex head and no `@`; the head is a commit; for QQPB the base is an ancestor AND the merge-base
with MAIN; `git rev-list --count base..head` equals `commits`; `git ls-remote origin refs/heads/<branch>` equals the head NOW **for BOTH rows — a moved
main REFUSES (re-pin and re-brief)**; `refs/pull/8/head` equals the QQPB head NOW; QQPB is not on main and is 0 behind it. The chain is pinned
exactly: `3d0167e`'s single parent `47eb533`; `0d45100` = `3d0167e` + `51e9286`; `4d6ed6e` = `0d45100` + `e4ce536`; `e4ce536` = `3dd15bc` + `5ad37f1`.

<!-- PIN-HEADS:BEGIN -->
| id | repo | branch | head | base | commits | status |
|---|---|---|---|---|---|---|
| MAIN-Q | quickquote | main | e4ce5367761e03db982189a3f21758aa06714a85 | - | - | IN |
| QQPB | quickquote | fix/qq-puppeteer-25-2026-09-22 | 4d6ed6ef403ef8962ded8211b76c3c6809bbb8c3 | e4ce5367761e03db982189a3f21758aa06714a85 | 3 | IN |
<!-- PIN-HEADS:END -->

Both rows: `git -C <quickquote> ls-remote origin` read by the drafter at **2026-10-16 ~13:00 AEDT**: `refs/heads/main` = `e4ce536…`,
`refs/heads/fix/qq-puppeteer-25-2026-09-22` = `4d6ed6e…`, `refs/pull/8/head` = `4d6ed6e…`, `refs/pull/8/merge` = `80747c81c343e4273918dc2062bcb87a35853cf2`
(GitHub's test merge, NOTE only), `refs/pull/7/head` = `5ad37f1…`. `rev-list --count e4ce536..4d6ed6e` = 3; `4d6ed6e..e4ce536` = 0.

Repo: quickquote = `/Volumes/Laptop-DEV/!CODING/Datasec/Vision_Sales_Portal/Quoting Tool/hpas-quoting-tool` (remote `datasecau/vision_hpas-quickquote`).
**The T9 copy of this repo (`/Volumes/KK_T9_External_HDD/!CODING/…`) is STALE — it does not hold `4d6ed6e` (drafter, `rev-parse`, 13:00). Never read
it.** Its rules: the repo's own `CLAUDE.md` (read it at the head with `git show`; its deploy and publish lines are NOT for you) and
`/Volumes/Laptop-DEV/!CODING/Datasec/Vision_Sales_Portal/CLAUDE.md` (its QuickQuote section). **The builder's checkout is LIVE: never use the name
`main` in the repo, always the pinned 40-hex sha; never read any working tree as evidence; build every tree from the object store.**

## WRONG OR UNVERIFIABLE IN THE COMMISSION AND THE READY — found by the drafter (verify each; all are claims)
- **(a) amd64 is not covered by the READY, and the builder's amd64 evidence is not yours.** READY NOT TESTED line 1: "both images above are arm64;
  App Service runs amd64. An emulated linux/amd64 build + in-image render + test:print is RUNNING now; result to follow in a STATUS mail." At 13:07
  the shared Docker daemon held the builder's `qq-evidence-local:amd64-main-e4ce536` and `qq-evidence-local:amd64-prb` and a running builder container
  (`docker images`, `docker ps -a`, MEASURED by the drafter). **None of those is evidence for this gate, and none may be touched, run, re-tagged or
  removed.** A STATUS mail from the builder, if Tuesday relays one, is a CLAIM. The gate builds its own amd64 base AND head images (§N2).
- **(b) "No shipped file reaches puppeteer internals" — but the IMAGE ships the tests.** The READY greps `lib/`, `server.js`, `strip.js`. The head
  Dockerfile does `COPY stage3/ /app/stage3/` and `.dockerignore` excludes only `**/node_modules`, `.git`, `stage3/public`, `stage3/private`,
  `Screenshots_for debugging`, `.playwright-mcp` (READ at `4d6ed6e`). **So `stage3/test/` — including the two files that now reach
  `puppeteer-core/internal/…` — is IN the production image** (it was at base too, with the `lib/cjs` path). The gate states BOTH: what the runtime path
  loads (MEASURED in the head image, §N5.2) and what the image carries (its `/app` listing). Pre-existing shape, not a defect of this PR by itself.
- **(c) The `lib-close-shared` cell can pass whether or not its stub hits.** Its assertions (READ at the head, `stage3/test/lib-close-shared.test.mjs`
  lines 23-39) are: a PDF rendered, one renderer Chrome started, `closeBrowser(1000)` returned in < 3500 ms, and the renderer Chrome is gone. **A
  `close()` that is NOT hung also satisfies all four.** With puppeteer-core 25 ESM-only and loaded through `require(esm)` while the stub loads
  `internal/cdp/Browser.js` through its own specifier, the stub could patch a DIFFERENT class instance than the one `lib/pdf.js`'s browser is built
  from, and the cell would still be green (READ-ONLY-INFERRED; the READY's evidence that it bites is "the 'killed the test's own Chrome' lines
  present"). §N5.3 proves identity at runtime and runs a mutant.
- **(d) The lock claims hold at source (MEASURED by the drafter):** 40 removed, 1 added, 13 changed, exactly as listed in §Charter; extract-zip and
  basic-ftp absent from the head lock, present in main's (extract-zip 2.0.1, basic-ftp 6.2.3). **Not measured:** the INSTALLED trees (host and
  image) — §N3/§N6.
- **(e) Base-vs-head image comparisons are only valid in ONE build window.** The Dockerfile pulls a floating `node:<n>-bookworm-slim` tag and
  `apt-get install chromium` with no version pin (READ). Built at different times, two images can differ in Chromium, fonts or fontconfig for reasons
  that have nothing to do with this PR. **Rule (§N2.3): build base and head back to back with `--pull --no-cache`, record each image's resolved base
  digest, `chromium --version`, `fc-list` hash and Debian package versions of chromium/fontconfig/fonts-*; a pixel or text comparison between images
  whose Chromium or font packages differ is VOID and re-run, never explained away.**
- **(f) The box is overloaded.** `uptime` at 13:07 read **load 224.77 / 184.67 / 101.81** on an Apple M2, 8 CPUs (`docker info` NCPU 8), with eight
  MPS lane seats, Composer-A, HPSM-POC-F, NexusAI-O and QA/NexusAI-batch23 live (tmux, MEASURED). amd64 under emulation will be slow and Chromium
  under emulation can crash or time out. **Every timing is reported with the load; a step that overruns its deadline is NOT RUN with the reason —
  never substituted by an arm64 result labelled as amd64.**
- **(g) The Dockerfile delta is exactly the FROM line plus three comment lines** (MEASURED: `git diff e4ce536 4d6ed6e -- stage3/Dockerfile`). `npm ci
  --omit=dev`, apt `chromium ca-certificates fontconfig fonts-liberation fonts-liberation2 fonts-dejavu-core`, `ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium`,
  `RUN node strip.js`, `ENV NODE_ENV=production`, `EXPOSE 8080`, `USER node`, `CMD ["node", "server.js"]` are unchanged. The launcher proves it.
- **(h) `require(esm)` on Node 22: warnings unmeasured.** `lib/pdf.js:11` is `const puppeteer = require("puppeteer-core");` (READ). Whether Node
  22.x prints an ExperimentalWarning on that require, at boot or on first render, is the drafter's open question (UNMEASURED). Capture stderr whole in
  the head image at module load and at first render and quote any warning line.
- **(i) The READY's "npm audit high 3 → 0"** vs GitHub's 2 open Dependabot alerts (#1 GHSA-jmr9-qjv8-65gv and #4 GHSA-7pqw-9j4j-h8q3, both extract-zip,
  high — `gh api …/dependabot/alerts?state=open`, READ-BY-DRAFTER 13:0x). The two counts measure different things (npm audit counts vulnerable
  PACKAGES including the `via` chain); say which three packages base's audit names. Dependabot #1 #4 can only read `fixed` after a merge: a post-merge
  read, not this gate's.
- **(j) CodeQL on PR refs is a blind instrument** (gate 17 WRONG (a), measured by gate 17's own control: the PR-side instances query reads 0 for a
  tree carrying all 14 alerts and for a ref that does not exist). The READY's "open code-scanning on refs/pull/8/head = 0 and refs/pull/8/merge = 0"
  proves nothing on its own. PR #8 changes no product JavaScript; read the CodeQL check runs on `4d6ed6e` (GH-API-LEG permitting) and say only what
  they can show. Main's open code-scanning count was **0** at 13:0x (READ-BY-DRAFTER).
- **(k) This drive's QA project has no Vision history.** `/Volumes/Laptop-DEV/!CODING/Testing Agent MAIN/projects/` holds no `vision/` (MEASURED,
  `ls`, 13:0x); gates 1-17 live only on the T9. Read them there; write only here.
- **(l) The Docker daemon is shared.** QA/NexusAI-batch23 runs its own `qa-b23-*` dind containers on the same Docker Desktop daemon; the builder's
  `qq-evidence-local:*` images and containers, `rd846-*`, `vsp-azurite-*`, `pc-lane-a-*` also exist (`docker ps -a`, 13:07). **Touch none of them.**
- **(m) The emailed PDF route needs a store and a mail transport; the module's own entry point needs Azure.** `require.main === module` throws
  without `SESSION_SECRET` (≥ 32) and `ADVANCED_UNLOCK_SECRET`/`HPAM_WORD`, then `store.ensureTables()` needs `TABLES_CONNECTION_STRING` (READ,
  hosted server module lines 910-935). So "boot the image's CMD with production settings" is NOT RUN by design (READY NOT TESTED line 2); the gate
  drives the image's own `createApp()` export with the repo's in-memory store and stub mail INSIDE the image (§N4.1).
- **(n) Session cookie is `Secure`** (`qqs=…; HttpOnly; Secure; SameSite=Lax`, READ, hosted server module :377). A browser on `http://127.0.0.1`
  inside the container is expected to keep it (Chromium treats loopback as a secure context — drafter's expectation, UNMEASURED); if it does not,
  the browser leg logs in by fetch and sets the cookie by CDP, and SAYS so.
- **Verified TRUE at source (READ 12:59-13:10):** both heads + `refs/pull/8/head` by `ls-remote` = the READY's; the chain and parents; 5-file set and
  numstat (+85/−522, = the READY's "5 files, +85/-522"); the unchanged-blob list; the lock diff; the `CdpBrowser` require swap in both test files with
  every other line unchanged (`git diff`); `lib/pdf.js` launch args `--no-sandbox --disable-dev-shm-usage --disable-gpu`; tests.yml five jobs on
  `node-version: 22`, `print-fit`/`xlsx-parity` on the runner's Google Chrome; CI runs **38837565972 (push) and 38837589895 (pull_request): head_sha
  `4d6ed6e…`, conclusion success, 5/5 jobs success** (READ-BY-DRAFTER, gh api); repo hooks 0; workflows = tests, Dependabot Updates, CodeQL; C-19
  present; the npm cache index holds puppeteer-core 25.0.2 and 23.11.1, @puppeteer/browsers 3.0.2, chromium-bidi 16.0.1,
  webdriver-bidi-protocol 0.4.1, extract-zip 2.0.1 tarballs (grep of `~/.npm/_cacache/index-v5`); Docker 29.7.2 linux/arm64 with buildx platform
  `linux/amd64` listed; Google Chrome 155.0.8059.84; host node v26.8.1; `pdftotext`, `pdftoppm`, `pdfinfo` present; **ImageMagick `compare`, PIL and
  numpy ABSENT** (pixel diffs must be done on `pdftoppm` PPM output in plain python).

## THE READY — its claims and NOT TESTED (the gate rules on every claim)
Read the READY whole. Its NOT TESTED lines are carried VERBATIM here (the launcher checks it):

QQPB NOT TESTED
```
NOT TESTED
- amd64: both images above are arm64; App Service runs amd64. An emulated linux/amd64 build + in-image render + test:print is RUNNING now; result to follow in a STATUS mail. The ACR build (amd64, native) is the publish step, which is Kam's tap.
- Booting server.js inside the new image with production settings (ACS mail, Table storage, session secret): not done; no prod secrets used. stage3-server and store-azurite cover the server in CI on node 22.
- The live site, or a real emailed quote through ACS on the new runtime: publish-time checks.
```

**The claims, in one line each (each a CLAIM, re-derived in §N):** npm audit --omit=dev high 3 → 0 (0 of every severity); `npm ls --all` rc 0, empty
stderr; extract-zip, basic-ftp, proxy-agent absent; local suites (macOS, node 26.8.1, Chrome 155.0.8059.84) pricing 69/69, `npm test` 132/132,
`test:print` 170/170, `test:xlsx` 6/6, main the same counts; red first: `test:print` 167/169 before the fixture fix (lib-close-shared failed at load;
BC-F1's child died on MODULE_NOT_FOUND); puppeteer 23 vs 25 on the same Chrome: server-path PDF text- and pixel-identical (100 dpi), printed light +
dark identical once deterministic (live-rate request blocked, clock frozen); an earlier non-deterministic run differed only by the live-vs-seeded
exchange-rate race; the real advanced-session collector path (AUD) identical 23 vs 25; images built locally (arm64): main node v20.20.2 / pptr 23.11.1 /
extract-zip present, PR B node v22.23.2 / pptr 25.0.2 / extract-zip absent, both Chromium 153.0.8010.52 (Debian bookworm); in each image `--network
none`, as root: `npm test` 132/132, `test:print` 170/170, `test:xlsx` 6/6; one fixture (AUD seeded 1.4324, 40 devices, 3 y, full bundle, Advanced + 10
h custom; fixed qnum, frozen clock) rendered in each image: server-path PDF, printed light, printed dark each 2 pages A4, text- and pixel-identical;
workbook identical part hash excluding core.xml; fonts DejaVuSans + LiberationMono; strip ok in both (public/index.html 246617 bytes); CI 5/5 on both
runs; CodeQL pass; MERGEABLE / CLEAN.

**How you treat these:** every NOT TESTED line you CAN test, you test — amd64 is THIS gate's core (§N2-§N4). Booting the image's own CMD with
production settings stays NOT TESTED by design (WRONG (m)); the gate's in-image `createApp()` path is the substitute and SAYS it is one. The live site
and a real ACS mail stay NOT TESTED (publish-time, Kam's tap).

## 2a. LEGITIMATE SHAPES — not a checker
Not a checker: this is a runtime change to the product image. The ordinary shapes a rep and the office produce are §N rows instead (a default-mode
quote, an advanced-session quote with PoC and custom hours, AUD / USD / CAD, the printed page in light and dark, the workbook attached to the same
mail). **Until a row below is measured, the instruction on ANY unexpected result is STOP and record it, never a remedy.**

## N1. THE HOST SUITES, RE-RUN — at the head and at base, as SETS (TIER 1)
**FAIL condition, stated BEFORE the runs:** any suite red at `4d6ed6e` on a clean tree; a test NAME passing at `e4ce536` that does not pass at the head
(SETS, NOT COUNTS); `npm ls --all` rc ≠ 0 at the head; any installed package not byte-equal to the head lockfile's integrity.
1. **Trees:** fresh `git archive` extractions of `e4ce536` and `4d6ed6e` under `projects/vision/work-g18/`, one purpose each. In `stage3/` only:
   `npm ci --offline --ignore-scripts` (a cache miss FAILS, then NOT RUN with the tarball named); prove `node_modules/.package-lock.json` against `git show
   <sha>:stage3/package-lock.json` **entry by entry** with `lockcmp.py` AND `lockwalk.py`; `npm ls --all` rc and stderr; `npm ls extract-zip basic-ftp
   proxy-agent puppeteer-core @puppeteer/browsers` at both.
2. **The suites CI runs, by PATH and command (tests.yml at the head, READ):** root `node --test quote-engine.test.mjs` (READY 69); in `stage3/`: `npm
   test` (132), `npm run test:print` (170), `npm run test:xlsx` (6). Each ×2 at the head, ×1 at base, same session, as SETS by test NAME: lost (must be
   empty), added, removed, duplicates. **Host Node is v26.8.1, not CI's 22 and not the image's 22.x: say so on every row.** `test:print` / `test:xlsx`
   drive Google Chrome: every Chrome under YOUR egress-block wrapper as `PUPPETEER_EXECUTABLE_PATH` (§13.3). `npm run test:azurite` is §N3.4.
3. **The red-first claim (fixture fix):** on a fresh head tree, revert ONLY the two test files to their base blobs (`f902922`, `6f79215`; tamper asserted
   landed) and run `test:print`: the READY predicts 167/169 with `lib-close-shared` failing at LOAD and BC-F1's child on `MODULE_NOT_FOUND`. Quote both
   errors. Then restore (fresh tree) and confirm 170/170.
4. **npm audit (commission; network exception NX-2, D3):** `npm audit --omit=dev --json` with `npm_config_update_notifier=false`, at the head AND at base,
   from YOUR shell, on YOUR trees. Report the per-severity counts and the package names verbatim; head must be 0 of every severity. Say which packages
   base names (WRONG (i)). Never `npm audit fix`.

## N2. THE IMAGES — built by the gate from the PR head and from main, for linux/amd64 (TIER 1, C-19, the core of this gate)
**FAIL condition:** the head image fails to build for linux/amd64; `node -v` in the head image < 22.12.0; puppeteer-core in the head image ≠ 25.0.2,
or extract-zip / basic-ftp / proxy-agent present in it; `npm ls --all --omit=dev` in the head image rc ≠ 0; the head image's `node_modules` differing
from the head lockfile; `node strip.js` failing in the build; the head image's `public/index.html` or `private/*` differing from the base image's
(same `index.html` and `strip.js` blobs at base and head); any image of yours pushed, tagged for a registry, or given a release-looking tag.
1. **Build context = a fresh `git archive` of each sha** (the repo root, as the Dockerfile header says), never a working tree, never your `npm ci` tree
   (`.dockerignore` excludes `**/node_modules`, but use a pristine extraction anyway). Record the context's file count and sha256 of a sorted member list.
2. **Build:** `docker build --platform linux/amd64 --pull --no-cache --progress=plain -f stage3/Dockerfile -t qa-g18-amd64-<base|head>:<sha7> <context>`
   (or `docker buildx build … --load` — say which). **Tags start `qa-g18-` and carry no registry host.** Log every build whole into `evidence/`. Record:
   the resolved digest of the `FROM` image for linux/amd64, the image id, size, build wall time with the load.
3. **SAME WINDOW RULE (WRONG (e)):** build base then head back to back; then in each: `node -v`, `npm -v`, `chromium --version`, `dpkg-query -W chromium
   chromium-common fontconfig fonts-liberation fonts-liberation2 fonts-dejavu-core`, `fc-list | sort | shasum`, `uname -m` (must read `x86_64`). **If
   Chromium or any font package differs between your base and head images, every cross-image pixel/text comparison is VOID until you rebuild both in
   one window and they agree.** Report the versions in a table.
4. **What the image ships:** in each image, list `/app` (path, size, sha256) EXCLUDING `node_modules`, plus `npm ls --all --omit=dev` (rc + stderr) and
   `node_modules/.package-lock.json` checked against the sha's lockfile entry by entry (copy it out with `docker cp` from a stopped container of
   yours). Diff base vs head listings: expected only `Dockerfile`, `package.json`, `package-lock.json` and the two test files (WRONG (b)). Quote the
   sha256 and byte count of `stage3/public/index.html` in each (READY: 246617 bytes).
5. **Optional arm64 control (only if time allows):** the same pair natively for linux/arm64 — a CONTROL that emulation did not change the result, never
   a substitute for amd64. If any amd64 row is NOT RUN, the arm64 row does not fill it: the verdict says amd64 NOT RUN.
6. **Deadlines (the image leg):** one amd64 build 2400 s; one arm64 build 900 s; one in-container `npm test` 900 s; one in-container `test:print` 1800 s;
   one in-container `test:xlsx` 900 s; one in-container render cell 600 s. Nothing above 2400 s. A build or run past its deadline is killed by the
   container id YOU started and reported NOT RUN with the load.

## N3. IN THE amd64 IMAGES — the suites CI runs (TIER 1)
**FAIL condition:** any in-image suite red in the head image; a NAME passing in the base image that does not pass in the head image (SETS); an
`ERR_REQUIRE_ESM` / `ERR_PACKAGE_PATH_NOT_EXPORTED` / `MODULE_NOT_FOUND` anywhere in the head image's output; Chromium crashing in the head image but
not in the base image under the same emulation.
1. In each amd64 image, **a container of yours** (`docker run --platform linux/amd64 --network none --user root --name qa-g18-<run>-<sha7> …`; no
   bind mounts except YOUR harness directory read-only at `/qa`; no `--privileged`; no host env; no secret), from `/app/stage3`: `npm test`,
   `npm run test:print`, `npm run test:xlsx`; and from `/app`: `node --test quote-engine.test.mjs` **if** the image carries it (it is not under
   `stage3/`: say whether it is in the image at all; if not, the pricing pack is host-only, §N1). Every npm call with `npm_config_update_notifier=false`.
   Report SETS by name, base vs head; quote every stderr line that is not a TAP line.
2. **User:** the suites need root (`strip.js` writes `public/`). The PRODUCT runs as `USER node`: §N4 runs as the image's own user.
3. **CI parity, READ ONLY:** CI ran these suites on Ubuntu with Node 22 and Google Chrome, not Debian Chromium. Say what the image leg covers that CI
   does not (Debian Chromium, the image's own node_modules, amd64 Debian userland) and the reverse.
4. **`test:azurite` (store-azurite, the fifth CI job):** run it against YOUR OWN Azurite container (`mcr.microsoft.com/azure-storage/azurite`, already
   in the local image store — record its digest; do not pull a different tag). The suite defaults to `TABLES_CONNECTION_STRING =
   "UseDevelopmentStorage=true"`, i.e. 127.0.0.1:10002 (READ, `stage3/test/store-azurite.test.mjs:17`, blob `79701f3` at base and head), so the
   simplest wiring is: your Azurite container `qa-g18-azurite-<n>` under `--network none`, and the image's test container joined to ITS namespace
   (`--network container:qa-g18-azurite-<n>`) so loopback is shared and nothing has a route out. (A `docker network create --internal qa-g18-net`
   is the alternative; say which you used.) Never set a real `TABLES_CONNECTION_STRING`. Base and head. If it cannot be wired in 30 minutes, NOT RUN
   with the reason. Never touch the `vsp-azurite-*` containers.

## N4. IN THE amd64 IMAGES — the quote artefacts through a REAL USER PATH, base vs head (TIER 1, C-19, the commission's comparison)
**FAIL condition:** any artefact of the head image that differs from the base image's for the same input, in TEXT (`pdftotext -layout`, normalised
only for nothing — the clock and quote number are frozen) or in PIXELS (`pdftoppm -r 100`, every page), unless §N2.3 shows the two images' Chromium or
fonts differ (then VOID and rebuild); a page count other than the base's; a page not A4; a font set other than the base's (`pdffonts`); the mono
fallback face appearing (the 2026-08-10 regression: DejaVu/Liberation expected, READY); the workbook differing in any part other than `docProps/core.xml`;
any render error, page error or `unknownFields` entry in the head image that the base image does not also produce.
1. **Instrument — the server path, in the image, as a user reaches it.** In a container of yours (`--network none`, `--platform linux/amd64`, the
   image's own `USER node`, `NODE_ENV` as the image sets it — say what it is), run YOUR harness from `/qa` (bind-mounted read-only) that `require`s the
   image's own hosted server module from `/app/stage3` (its `createApp()` export, NEVER its entry point, NEVER with a real secret) with: the repo's
   in-memory store and a capturing stub mail (READ how `stage3/test/server.test.mjs` builds them, lines ~100-160, and copy that shape), a throwaway
   `sessionSecret` of 48 chars and a throwaway `unlockSecret` (a fresh random string; never the HPAM word, never a real secret), the image's OWN
   `renderQuotePdf` from `lib/pdf.js`, a FROZEN clock (READ `createApp()`'s option list for a clock; if none, say how you froze time and prove it
   froze) and `trustForwardedFor: false`. Listen on 127.0.0.1 inside the container on a kernel-chosen port.
2. **The user path, driven by a real browser IN THE SAME CONTAINER:** the image's own Chromium (`/usr/bin/chromium`) driven by the image's own
   puppeteer-core (so base drives with 23.11.1 and head with 25.0.2 — write the harness against APIs both versions have, and SAY which you used), loads
   `http://127.0.0.1:<port>/login`, signs in with the OTP the stub mail captured, (advanced arm) unlocks with the throwaway word through the page's own
   unlock control, fills the form as a rep would, and presses the page's own **email (PDF & XLS)** control so the PAGE's collector posts the state.
   Capture: the posted state JSON, the server's JSON answer (qnum, `unknownFields`, `clearedChecks`), and the stub mail's two attachments (PDF, xlsx).
   **Fallback (say so if used):** if the browser cannot hold the `Secure` session cookie on loopback (WRONG (n)), sign in by fetch and set the cookie by
   CDP; if the browser leg cannot run under emulation at all, post the state captured from the base image's browser leg straight to each server and
   label that row "server path, posted state" — never "real user path".
3. **The grid (minimum):** default mode × {AUD, USD, CAD} and advanced mode (PoC + Workpath-Ready + custom hours, the READY's "Advanced + 10 h custom")
   × {AUD, USD, CAD} = **6 shapes**, each with a fixed customer name containing `& < > " '`, 40 devices, 3 years, the full bundle. Same inputs in base and
   head images. FX: the container has no network, so every rate is the seeded table; record the rate line printed on each PDF (the builder's earlier
   difference was a live-vs-seeded race — it cannot occur here; if a rate differs, that is a finding).
4. **The printed quote, light and dark:** in the same browser session after the form is filled, switch the page's own theme control (click what a user
   clicks — gate 16 SF-3/SF-4: the visible toggle, after it settles) and print with the print media type to A4 (`page.pdf({ format: "A4",
   printBackground: true })` or the API both versions share — say which) — light and dark, for at least the AUD default and AUD advanced shapes, base and
   head. Page count, A4 (`pdfinfo`), text, pixels, fonts.
5. **Compare** every pair base-image vs head-image: text diff (must be empty), pixel diff per page (count of differing pixels; 0 expected — write a
   diff PPM for any non-zero page and put it in `evidence/`), `pdffonts` set, page count/size; workbook: unzip both and diff every part (expect only
   `docProps/core.xml`; quote the differing timestamps). **Also compare the head image's server-path PDF with its printed-light PDF for the same shape:
   the seat's open item (PRIOR ROUND) says they price differently before AND after — MEASURE it in both images, report it as PRE-EXISTING if base and
   head agree, never as PR #8's regression.** Record the `unknownFields` list per render in both images (the 7 print-mode fields `pmBoth`..`cpPct` are
   expected at both).
6. **Look at the pages:** open page 1 and page 2 of the head-image AUD advanced PDF (light and dark printed, and server path) as images and say in one
   line each what a customer sees (one A4 sheet per page, logo present, no clipped price) — a human-eye row, not a pixel row.

## N5. PUPPETEER INTERNALS AND THE TWO TEST FIXTURES (TIER 1 by the runtime; the fixtures are harness, not product)
**FAIL condition:** any file the hosted runtime LOADS from puppeteer-core other than through its public entry (`require("puppeteer-core")`); any
shipped file outside `stage3/test/` naming a `puppeteer-core/` subpath; either fixture changing anything but its require line (and comments); the stub's
`CdpBrowser` NOT being the class the renderer's browser is an instance of; a `lib-close-shared` cell that stays green with the stub disarmed (that last
one is a FINDING against the suite, not a FAIL of the head unless the product is wrong).
1. **Static (READ):** `git grep -n "puppeteer-core/" 4d6ed6e -- stage3 ':!stage3/package-lock.json'` and the same at base; then the same grep over the
   head IMAGE's `/app/stage3` excluding `node_modules` (WRONG (b)). Table: file, line, shipped-in-image yes/no, loaded-at-runtime yes/no.
2. **Runtime (MEASURED, head image, `--network none`):** while one render runs through §N4.1's path, log every module specifier the process resolves
   (an instrument you state: e.g. a `module.registerHooks`/`module.register` resolve hook preloaded with `--import`/`--require` from `/qa`, or
   `NODE_DEBUG=module` output filtered) and list every `puppeteer-core` file loaded and the specifier that loaded it. Expected: only the package's
   public entry resolves from product code. Capture and quote any `ExperimentalWarning` (WRONG (h)) at module load and at first render.
3. **The stub hits the real class (WRONG (c)):** in the head image (and on the host head tree), with `lib/pdf.js`'s shared browser launched, prove
   `Object.getPrototypeOf(<the renderer's browser>) === require("puppeteer-core/internal/cdp/Browser.js").CdpBrowser.prototype` — reaching the private
   handle only from YOUR harness (e.g. by a `CdpBrowser.prototype` method spy installed from the internal specifier that records `this` on the first
   call the renderer makes), never by editing `lib/pdf.js`. Then **mutant G-M1 (stub disarmed):** a fresh head tree where `lib-close-shared.test.mjs`'s
   stub targets a throwaway class (`class X {}`) instead of `CdpBrowser` (tamper asserted landed, `node --check` rc 0): does the cell still pass?
   **mutant G-M2:** the same for `fixtures/hang-close.cjs` — does BC-F1 (`lib-close.test.mjs`) still pass? Say which cells see each, or NONE.
4. **The fixtures keep their assertions:** `git diff e4ce536 4d6ed6e -- stage3/test/fixtures/hang-close.cjs stage3/test/lib-close-shared.test.mjs`
   whole; confirm every `assert`/`test(` line byte-identical (count them at both: `lib-close-shared.test.mjs` has 2 `test(` cells at the head, READ).
   Then run both fixtures' cells in the head image and on the host head tree and quote the "killed the test's own Chrome" lines the READY names.
5. **ESM-only, measured:** read `node_modules/puppeteer-core/package.json` at the head (host tree and image): `type`, `exports` for `.` and
   `./internal/*` (the READY: `"./internal/*" -> "./lib/puppeteer/*"`), `engines`. Say whether `.` has a `require` condition at all, i.e. whether
   `lib/pdf.js` relies on `require(esm)` (P5B's ship note). In the head image, show that the base image's Node (20.x) CANNOT load the head's
   `node_modules` (e.g. run `node -e 'require("puppeteer-core")'` with the head tree's node_modules under the base image's node, read-only bind
   mount) — the red proof that the `FROM node:22` line and the lockfile must ship together. Quote the error.

## N6. THE DEPENDENCY CLEAN-UP (TIER 1 by the image)
**FAIL condition:** extract-zip, yauzl, basic-ftp or proxy-agent resolvable in the head image or host head tree; a removed package still loaded at
runtime; a package in the head image not in the head lockfile; any of the 13 changed versions installed at a version other than the lockfile's.
1. Host head tree and head image: `npm ls extract-zip yauzl basic-ftp proxy-agent pac-proxy-agent get-uri socks` (all absent), and the 13 changed
   packages at their lockfile versions. Base: extract-zip 2.0.1 and basic-ftp 6.2.3 present.
2. **The inert override (builder's choice 2):** with no `basic-ftp` in the tree, say whether npm warns about the override (quote any line) and whether it
   changes anything resolved. Observation; removing it is the builder's one-line cleanup, not yours.
3. **The pinned version (builder's choice 1):** READ ONLY — the drafter did NOT read the registry for 25.x publish dates. If the npm registry read
   NX-2 allows, `curl -s -m 30 https://registry.npmjs.org/puppeteer-core` from YOUR shell: `time["25.0.2"]`, `time["25.14.0"]`, `dist-tags`, and
   `versions["25.0.2"].dist.integrity` vs the lockfile; state the days between 25.0.2's publish and 2026-10-16. Otherwise NOT RUN.

## N7. NOTHING PUSHED, NOTHING DEPLOYED, LIVE SITE UNCHANGED (commission; READ ONLY)
**FAIL condition:** any `docker push`, `docker login`, `docker tag` to a registry host, `az acr build`, `az acr import`, `az webapp` write or any deploy
in your command log; any image of yours tagged other than `qa-g18-*`; the live webapp's `linuxFxVersion` (or `hpasqqacr`'s hpas-quickquote tag list)
at the end differing from the pre-read without an explanation that is not you.
1. **Your own discipline, MEASURED:** at start and end, `docker images --format '{{.Repository}}:{{.Tag}} {{.ID}}' | grep '^qa-g18-'` and `docker ps -a
   --filter name=qa-g18-`; your shell history for this session grepped for `push`, `login`, `acr`, `webapp` (quote the zero beside a positive control
   — e.g. the same grep over a scratch file that contains `docker push` reads 1).
2. **The Azure side, by AZ-READ-LEG (D2):** TUESDAY-READS → RELAY the `AZ-PRE-READ` line (appended to your prompt by the launcher) and say the
   post-read is Tuesday's at verdict; GATE-SHIM → at start and end, `az account show --query '{t:tenantId,s:id}'` (must read tenant `d500ebad…` and
   subscription `0c57ab37…`; anything else: STOP, no further az), `az webapp config show --name hpas-quickquote --resource-group hpas-quickquote-rg
   --query linuxFxVersion -o tsv`, `az acr repository show-tags --name hpasqqacr --repository hpas-quickquote --orderby time_desc --top 5 -o tsv`; an
   authorisation error is the boundary working — report it, never work around it; NOT-RUN → NOT TESTED.
3. **Deploy-on-merge (READ ONLY):** `.github` at the head holds only `tests.yml` (no deploy, no image build, no registry login, no secret); if GH-API-LEG
   allows: repo hooks, environments, deployments, Actions secret NAMES, workflows. Gate 17's relayed Azure reads (ACR `hpasqqacr` tasks [] and
   webhooks []; webapp deployment source null; no DOCKER_ENABLE_CI) are RELAYED, 3 days old: say so. State whether a merge deploys anything, with each
   statement's evidence class (READ ONLY / RELAYED / UNMEASURED).

## N8. CI AND CODEQL ON PR #8 (READ ONLY; never caused)
**FAIL condition:** a tests.yml run on `4d6ed6e` not `success` on all five jobs; a CodeQL check run on `4d6ed6e` failing; any alert dismissed.
1. If GH-API-LEG = READ-ONLY-VISION-TOKEN: `actions/runs/38837565972` and `/38837589895` (head_sha, conclusion) and their `/jobs` (five names, each
   `success`); `commits/4d6ed6e…/check-runs` (names, conclusions, the CodeQL output title); `code-scanning/alerts?state=open` count on main;
   `dependabot/alerts?state=open` (expected #1 and #4, extract-zip, open until merge). Otherwise NOT RUN.
2. **What CodeQL can say here (WRONG (j)):** the PR-side zeros are blind (gate 17's control). PR #8 changes no product JavaScript. Say that, and name the
   post-merge reads: Dependabot #1 #4 `fixed` on main, main's code-scanning still 0 open, tests.yml green on the merge commit.

## N9. RUNTIME DRIFT, READ (puppeteer 23 → 25 API surface used by the product)
**FAIL condition:** the product calls an API removed, renamed or re-defaulted between 23.11.1 and 25.0.2 (launch options, `page.pdf` options,
`waitUntil`, `evaluate`, headless default, `newPage`, `close`, the `disconnected` event) without a measured equal result in §N4.
1. READ every puppeteer call in `stage3/lib/pdf.js` (blob `783ebea`, unchanged) and `stage3/lib/xlsx.js`; against each, READ the installed 25.0.2 type
   definitions / source in YOUR head tree's `node_modules` (never the internet). Table: call, 23 behaviour, 25 behaviour, §N4 row that measured it.
   Labelled READ ONLY except where §N4 measured.

## 12. The merge and the queue
QQPB is 3 ahead and 0 behind `e4ce536`; its head is itself a merge of main, so a GitHub merge commit's tree equals `4d6ed6e`'s (`01bdc92`) — prove 0
behind with `rev-list --count`; run `git merge-tree --write-tree` only from YOUR OWN object dir, or skip it and say so. **Cells to re-run at merge**
(name at least): the four host suites; tests.yml's five Node 22 jobs on the merge commit; Dependabot #1 #4 reading `fixed`; and **at publish (Kam's tap,
not covered by C-19): the ACR build's own amd64 image (native) re-running §N4's AUD advanced shape and the live page's first emailed quote.**

## 13. FLOOR AND PORT DISCIPLINE — Vision has NO jest lock, plus THE DEADLINE RULE, DOCKER DISCIPLINE (and HELD)
**There is no shared lock or queue on this project, and you must NOT borrow NexusAI's** (its jest/docker lock serialises NexusAI seats only).
1. **Never use `4848` (portal), `8080` (QuickQuote's stage3 dev port) or `47787` (Tuesday's dashboard)** on the host. Host product processes take
   ports from the kernel and bind `127.0.0.1`; in-container servers bind 127.0.0.1 inside the container under `--network none`. **Never start the hosted
   server module's own entry point, on the host or in an image; use its `createApp()` export.** No database, no Postgres.
2. **Every host product process runs under `env -i` with an explicit ALLOWLIST** (PATH; HOME = a fresh mktemp dir; NODE_ENV = `test`, never
   `production`; `PUPPETEER_EXECUTABLE_PATH` = YOUR egress-block wrapper; `npm_config_update_notifier=false`; `npm_config_offline=true` except the
   §N1.4 / §N6.3 reads; `npm_config_cache` = the user cache, read for `npm ci --offline` only). **NEVER set in a product process, host or container:**
   `AGENTMAIL_API_KEY`, `AGENTMAIL_INBOX` (with both set, QuickQuote SENDS FOR REAL), any real `ACS_*` / `MAIL_SENDER`, `TABLES_CONNECTION_STRING`
   (except the Azurite dev account in §N3.4), `SALES_COPY_EMAIL`, `HPAM_WORD`, `ADVANCED_UNLOCK_SECRET`, `SESSION_SECRET`, `WEBSITE_SITE_NAME`,
   `GH_TOKEN`, `GITHUB_TOKEN`. Print each product process's env KEY NAMES (never values) and assert none is forbidden; for containers, print
   `docker inspect --format '{{json .Config.Env}}'` KEY NAMES only. `NTFY_SERVER=http://ntfy.invalid`; never contact ntfy.sh.
3. **EGRESS INCLUDING CHROME CHILDREN (host leg):** the page calls three public FX APIs whenever the currency is not USD. Every host Chrome runs under
   YOUR copy of the egress-block wrapper; prove the block with its positive control (`qa-egress-posctl.mjs`) and run the net-log scan at the end;
   record GoogleUpdater and chrome_crashpad_handler at start and end (`qa-chrome-census.py`). **Container leg:** `--network none` on every product
   container (the §N3.4 Azurite pair uses an `--internal` network: prove from inside that `registry.npmjs.org` does not resolve/connect).
4. **Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid** (`qa-floorcount.py`, copied): "ours" = the ancestor chain CONTAINS your
   claude pid. **Negative controls, same run, must classify FOREIGN.** The launcher DERIVES the negative-control seats live from the cockpit panes
   (the `tuesday` pane, the `Datasec/Vision_Sales_Portal` builder pane, and any live `QA/*` / `fleet-monitor` pane) and appends them to your prompt.
   **Seats read at drafting (13:07 AEDT, `tmux list-panes -a`):** `tuesday` (%0, pane pid `73565`), `Datasec/Vision_Sales_Portal` (%12, pane pid
   `34871`), `QA/NexusAI-batch23` (%10), `Datasec/NexusAI-O` (%2), `fleet-monitor` (%1), eight `Datasec/MPS-L*` lanes, `Datasec/Composer-A`,
   `Datasec/HPSM-POC-F`. **A zero is reportable only beside a control that fired in the same window.** **Record the 1-minute load beside every timing.**
5. **DOCKER DISCIPLINE (new for Vision; adapted from NexusAI's H-35):** only YOUR objects: images tagged `qa-g18-*`, containers named `qa-g18-*`, the
   network `qa-g18-net`. **Never start, stop, remove, re-tag, exec into or run** the builder's `qq-evidence-local:*` images or its containers, any
   `qa-b23-*`, `rd846-*`, `vsp-azurite-*`, `pc-*` or other foreign object. **Never `docker system prune`, `image prune`, `container prune`, `volume
   prune`, `builder prune`, `rmi` or `rm` of anything.** No `docker push`, no `docker login`, no registry host in any tag. Your containers are
   STOPPED and LEFT (no `--rm`), listed by id in the report; your images are LEFT, listed by id. No bind mount of any host path except your own
   read-only harness dir at `/qa` and the one read-only node_modules mount of §N5.5; never the Docker socket.
6. **THE DEADLINE RULE:** every step has a written DEADLINE built into your runner (no `timeout` binary here) and a client timeout on every request;
   a step past its deadline is ABORTED and reported. Host deadlines: one page cell 120 s; a whole host `test:print` 420 s; `test:xlsx` 300 s; `npm test`
   300 s; root pack 120 s; one mutant arm 420 s. **Image deadlines are §N2.6 (nothing above 2400 s).** **Every Chrome, page, child, app server, container
   and temp profile you start is released in a `finally`** (containers: stopped by the id you started, never removed). **Log a HEARTBEAT line
   (timestamp, step, pid or container id, elapsed, load) at least every 2 minutes; a step with no heartbeat for 5 minutes is aborted and reported.**

**Reap everything you start.** An orphan Chrome, listener or running container of yours is someone else's foreign process.

### Drivable surface — LOCAL ONLY. **NEVER the live QuickQuote or the live portal.**
- **NEVER the live** QuickQuote (`hpas-quickquote`, `hpas-quickquote-rg`, `hpasqqacr`, its Table Storage, its log workspace) and **NEVER the live**
  portal (`https://datasec-sales-portal.azurewebsites.net`, resource group `datasec-sales-portal-rg` — PRODUCTION). **No HTTP request to either, not
  even a GET. No az beyond D2's read-only leg — no writes, no app-setting change, no deploy, no publish, no ACR build, no ACR push.** Never the FX hosts
  (stubbed, blocked or absent under `--network none`), never ntfy.sh. **Never Claude in Chrome** (Kam's real Chrome with his sign-ins). Never open
  anything under `Vision_Sales_Portal/4_Credentials/` (the launcher wires the gh/az config itself when D1/D2 allow; you never read its files), and never
  type an HPAM word.
- **Network exceptions (D3), and ONLY these:** NX-1 the image builds' own pulls (Docker Hub `node:20-bookworm-slim` and `node:22-bookworm-slim` for
  linux/amd64 (and arm64 if §N2.5 runs), Debian apt inside the build, the npm registry inside the build's `npm ci --omit=dev`); NX-2 `npm audit
  --omit=dev` and the `curl -s -m 30 https://registry.npmjs.org/puppeteer-core` read, from YOUR shell; NX-3 `git ls-remote origin` (head readings);
  NX-4 `gh api` GETs if GH-API-LEG allows. Record every digest NX-1 resolved. Nothing else reaches the internet.

### HELD
- No merge, no deploy, **no publish**, **no registry push**, **no production**, no money, **no mail to any human**, no external comms. **No comment,
  review, label, approval or status on PR #8 or any GitHub object; no re-run of any workflow; no alert dismissal of any kind.**
- **No `docker` beyond §13.5, no `npm install`, no `npm ci` without `--offline --ignore-scripts` on the host, no `npm audit fix`, no `npx` of anything not
  already in your tree. `gh` only as GH-API-LEG allows; `az` only as AZ-READ-LEG allows.** The launcher points `AZURE_CONFIG_DIR` at an EMPTY directory
  and `GH_CONFIG_DIR` at an EMPTY directory unless D1/D2 say otherwise.
- **Trees:** build every tree INSIDE YOUR OWN PROJECT from the object store (`git -C <repo> archive <sha> | tar -x -C <fresh mktemp -d under
  projects/vision/work-g18/>`, in `/Volumes/Laptop-DEV/!CODING/Testing Agent MAIN`). **Each tree is EXCLUSIVE to this gate and to ONE purpose; never
  touch any other `work*` directory on either drive.** In the repo use ONLY read verbs (show, log, diff, ls-remote, rev-parse, ls-tree, cat-file, grep,
  merge-base, archive); **never fetch, pull, checkout, switch, worktree, commit, stash, reset, clean, gc, branch or for-each-ref.** `merge-tree
  --write-tree` only from your OWN object dir.
- **CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY:** every control is a separate measurement that could have come out the other way on its own. **For this
  gate: a planted one-pixel and one-word difference must make your PDF comparator report non-zero before its zeros are believed; the base image's
  `npm ls extract-zip` must find it before the head's absence is believed; the base Node must fail to load the head's puppeteer-core before "they must
  ship together" is believed; the disarmed-stub mutant must be shown to have LANDED before its result is read; the egress block's positive control
  fires; the floor count rises on its attached control; `uname -m` reads `x86_64` in every container you call amd64.**
- **Findings only:** do not commit, do not move any branch, do not file a ticket. **Make no writes in the QuickQuote repo** (its working tree is the
  builder's, live) **and none inside `Vision_Sales_Portal/`**, none in gate 1-17's report folders or trees on either drive. Describe fix-shapes in prose.
- **NEVER `rm`.** Quarantine instead.

## THE MODEL RULE
(Kam, live board 2026-09-30 09:07, card `nexusai-gate11-opus55-safeguard-model-switch`, option (b) — QA gates may switch to Opus 4.8 when flagged,
PER SESSION.) You start on Opus 5.5 (the launcher reads the model id from Tuesday's `0_Brain/dashboard/data/models_latest.json`, `claude-opus-5-5` at
drafting). You run the FULL rows. If one of your responses is stopped by the safeguards: that step is NOT RUN (never re-worded to slip past); write ONE
line to `evidence/classifier-stops.txt`; stop any container and reap any Chrome and app server you started; mail `tuesday-agent@agentmail.to` with the
subject exactly
`[QA/Datasec-Vision -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch`;
then end your turn with the line `PARKED: flagged — awaiting the Opus 4.8 switch` and wait. Tuesday switches THIS pane's model and taps you by mail. You
never answer the model dialog yourself, and nobody ever chooses "Switch automatically". After the switch, resume at the stopped row. The report states
which rows ran on which model, with the switch time, and quotes `classifier-stops.txt` whole.

## TUESDAY'S RULINGS AT STAMP (2026-10-16)
**R1-R7 are the commission's requirements as Tuesday wrote them to the drafter (2026-10-16 ~12:58), carried as ruling lines. Apply them; do not
re-rule them.**
- R1: ONE gate, TIER 1 (shipped build image + quote PDF output) on QuickQuote PR #8 @ 4d6ed6e, Kam's C-19 (card quickquote-decision14-puppeteer25-node22-1016 = b, 2026-10-16 12:41:19 AEDT).
- R2: Build the image from the PR head for linux/amd64 and run it; the gate verifies amd64 itself and never relies on the builder's amd64 run or STATUS mail.
- R3: Generate the server-path emailed PDF, the printed quote (light and dark) and the xlsx from a real user path (advanced and default modes, AUD/USD/CAD) and compare against main e4ce536's image (text + pixel).
- R4: Run the test suites the repo's CI runs; npm audit --omit=dev.
- R5: No shipped file reaches puppeteer internals; the two changed test fixtures keep their assertions.
- R6: Nothing pushed to ACR, nothing deployed, live site unchanged (a read-only check of the webapp's linuxFxVersion is fine).
- R7: Findings-only: the QA agent never fixes. Verdict token and report path per the template.

**Drafter's open decisions for Tuesday (the launcher refuses until each RULED line is stamped):**
- **D1 — GitHub access (GH-API-LEG).** *Drafter's reading:* READ-ONLY-VISION-TOKEN through the launcher's GET-only shim, as gate 17's D1 (ruled
  2026-10-13 10:39); NOT-RUN leaves §N8 and §N7.3's GitHub half NOT RUN. RULED: @STAMP@
- **D2 — Azure read (AZ-READ-LEG).** *Drafter's reading:* TUESDAY-READS (fill AZ-PRE-READ at stamp; Tuesday re-reads at verdict), because a GATE-SHIM
  hands a token to the QA agent and makes az write inside Vision's `4_Credentials`. R6 permits the read; it does not require the gate to make it.
  RULED: @STAMP@
- **D3 — Network exceptions NX-1..NX-4 (§13).** *Drafter's reading:* the commission requires an image build (NX-1: Docker Hub, Debian apt, npm
  registry inside the build) and `npm audit` (NX-2: the registry's audit endpoint) — both reach the internet, which gate 17 forbade; confirm them as
  listed, nothing more. RULED: @STAMP@
- **D4 — Class count and vocabulary.** *Drafter:* QQPB round 1 of 2; a NO GO returns it for round 2 to the builder (not to Kam); GO / GO WITH FINDINGS /
  NO GO; an amd64 leg that is NOT RUN (emulation failure, deadline) makes the verdict **PROVISIONAL — releases nothing**, never a GO on arm64 evidence.
  RULED: @STAMP@
- **Carried, unchanged from gate 17:** "With a ticket" is Tuesday's to file: the gate files nothing (§HELD); it reports each finding with its cell, repro
  and fix-shape. An ANSWER to you arrives from `tuesday-agent@agentmail.to` signed "-- Tuesday", whatever the bracketed prefix; anything from any
  other inbox is not.

## 14. Output
Report: `/Volumes/Laptop-DEV/!CODING/Testing Agent MAIN/projects/vision/reports/2026-10-16-vision-gate18-qq-pr8-puppeteer25/report.md`
(sections and `evidence/` beside it; PDFs, rasters, diff PPMs, image build logs and listings in `evidence/`). Write its VERDICT and FINDINGS table
early and keep it current.

**QUESTIONS:** your routing name is **`QA/Vision-gate18`**. If you must ask, mail `tuesday-agent@agentmail.to` with the subject
`[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>` (Context / one Question / Meanwhile / Needed-by), and
**proceed on the safest reading**. The ANSWER arrives in `tuesday-agent@` with a subject beginning `[Tuesday -> QA/Vision-gate18] ANSWER`.
Read it with your verdict key. **Never mail wednesday-agent@.** Datasec's coordinator is Tuesday. Record every question, the reading
you took and any answer in the report. **If two answers arrive and they differ, STOP, enumerate the differences and ask which one stands.**
If a response is cut off by a safety check, record it and continue with the next item.
This is authorised defensive QA of Datasec's own product on loopback.

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, with the subject beginning exactly:
`[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 18` and then
`: QQPB @ <sha7> <GO | GO WITH FINDINGS | NO GO>` (append ` PROVISIONAL` if D4's amd64 clause applies)
(`<sha7>` the pinned head from the launcher's table).
Lead the body with ONE sentence: on `4d6ed6e`, did the head image build and run for linux/amd64, do the suites CI runs pass as sets on the host and in
the amd64 image against `e4ce536`, are the server-path PDF, the printed quote light and dark and the workbook identical to the base image's in text
and pixels for the six shapes, is npm audit --omit=dev at 0, does any shipped file reach puppeteer internals, and was anything pushed or deployed?
Then one line each on: the image versions table (node, puppeteer-core, Chromium, base digest — base vs head); the stub-identity result and G-M1/G-M2;
`require(esm)` warnings; the live site read (by D2's evidence class); the class count (round 1: a NO GO goes to round 2). You have no inbox that wakes
you, so a verdict you do not mail is lost.

AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/Laptop-DEV/TUESDAY/4_Credentials/.env`. The path is absolute because the QA project has no
credentials directory of its own. Use the key ONLY in your own verdict/question/answer-read `curl`, with a client timeout (`-m 30`). It must never enter
a product process's or a container's environment. **Never put the key, or any secret, in a mail or the report.**

Verdict format:
- **One verdict, GO / GO WITH FINDINGS / NO GO (PROVISIONAL per D4)**, naming the pinned sha and the branch: the host suites as sets vs base, the image
  table, the in-image suites as sets, §N4's comparison table (shape × artefact × text/pixel/fonts/pages), then §N5-§N9 row by row.
- The verbatim strings: each image's `node -v`, `chromium --version`, puppeteer-core version and `uname -m`; the npm audit counts and names (base and
  head); the red-first errors of §N1.3; the Node-20 load error of §N5.5; any `ExperimentalWarning`; the stub-identity line; the AZ readings or "RELAYED
  from AZ-PRE-READ".
- **A table with one row per §N item: MEASURED / NOT TESTED / NOT RUN / VOID, and HOW (command, image id, platform, user, network, load).** No row
  without a HOW.
- **Rule 2: what you did NOT test is first-class output.** A NOT TESTED section covering at least **the image's own CMD booted with production
  settings (ACS, Table Storage, session secret — WRONG (m))**, **ACR's own native amd64 build**, **the live site and a real ACS mail (publish-time)**,
  **CodeQL's verdict (blind pre-merge, WRONG (j))**, **Dependabot #1 #4 `fixed` (post-merge)**, **amd64 under real hardware (this gate's amd64 is
  QEMU/Rosetta emulation on an M2 — say which)**, **Windows / the account managers' real browsers**, **Claude in Chrome (not used)**, and every §N row
  you did not run, with the reason. **Every action recommendation carries its evidence class: MEASURED AT RUNTIME / PROBED / READ ONLY.**
- Report the pinned head and main as three timestamped readings (**start / mid / end**), each with its branch name, plus `refs/pull/8/head`.

PROVENANCE:
- heads: main `e4ce5367761e…`, `fix/qq-puppeteer-25-2026-09-22` `4d6ed6ef403e…`, `refs/pull/8/head` `4d6ed6e…`, `refs/pull/8/merge` `80747c81…` |
  `git -C <quickquote on Laptop-DEV> ls-remote origin` | read 2026-10-16 ~13:00 AEDT
- chain, parents, dates, count 3 / 0 behind, merge-base, numstat (+85/−522), per-file diffs, the unchanged-blob list, head tree `01bdc92`, `d030674` and
  `51e9286` ancestors of `e4ce536`; the T9 repo lacking `4d6ed6e` | `log --format`, `rev-list --count`, `merge-base`, `diff --numstat`, `diff`,
  `rev-parse <sha>:<path>`, `rev-parse --verify` | read 12:59-13:08
- lock diff (40 removed / 1 added / 13 changed, engines) | `python3 -I` over `git show <sha>:stage3/package-lock.json` | read 13:0x
- the code at `4d6ed6e` (Dockerfile whole, package.json whole, `.dockerignore`, `lib/pdf.js` header and launch, the hosted server module's createApp
  options :255-270, quote route :624-713, entry point :910-935, cookie :377, the two test files, tests.yml whole) | `git show` | read 13:0x
- GitHub (READ-BY-DRAFTER, `gh api` GET with Vision's gh-config — which wrote nothing to that dir, mtimes unchanged): PR #8; runs 38837565972 and
  38837589895 + jobs; Dependabot open #1 #4; code-scanning open 0; hooks 0; workflows | read 13:0x
- the READY (read whole); CLARIFICATIONS C-16..C-19 (C-19 whole); Tuesday's daily note 2026-10-16 entries 12:24, 12:37, 12:42, 12:57 | read 13:0x
- gate 4's report (P5B row and section lines 166-177); gate 17's report (verdict section) and `evidence/tools/` listing; gate 17's brief, drafter report
  and launcher (whole); the NexusAI batch-23 launcher (whole); BRIEF_TEMPLATE (whole) | read 12:58-13:1x
- docker 29.7.2 linux/arm64, buildx `desktop-linux` listing linux/amd64, images and containers present (builder's `qq-evidence-local:*`, `qa-b23-*`), NCPU 8;
  load 224.77/184.67/101.81; tmux panes; npm cache index; Chrome 155.0.8059.84; node v26.8.1; pdftotext/pdftoppm/pdfinfo present, compare/PIL/numpy
  absent; `models_latest.json` opus = `claude-opus-5-5`; this drive's Testing Agent MAIN has no `projects/vision` | `docker version/buildx ls/images/ps -a/info`,
  `uptime`, `tmux list-panes -a`, `grep` of `~/.npm/_cacache/index-v5`, `--version`, `which`, `python3 -c`, `ls` | read 13:00-13:08
- no merge-tree, no fetch, no docker build or run, no product process, no browser, no `az`, no npm registry read was made by the drafter; `gh` was used
  for GET reads only
