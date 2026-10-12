From Friday (laptop seat), Datasec / MPS Commercial Calculator. Replies go to `friday-laptop-agent@agentmail.to`. If `4_Credentials/.env` has no `AGENTMAIL_API_KEY`, the STATUS file is the wrap.

# BRIEF B73 · SEAT-F: HOSTED DEPLOY of MPS main `bf60fe83c02c703d5df11253629b268d25c78ab0` (PRs #29 to #33: source-store hardening, overlay fixes, leak scanner, feedback pill, overlay timing) to the existing showcase. Code only, plus PART B (one feedback-store setting) ONLY if Friday's placement note says Kam ruled **b**. B55 runbook, with five mandatory pre-swap STOP checks.
**From:** Friday (laptop seat), @NOW@. **Seat:** pane `Datasec/MPS-F`. Your commission is THIS file at `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/briefs_drafts/2026-10-13_B73_SEAT-F_hosted-deploy-bf60fe8.md` (Friday's tree, read-only to you). Step 0: copy it unchanged into your `1_Project_Definition/Briefs/` as the project's record (`cmp` equal, sha256 in STATUS).
**Fired:** @NOW@
**FRIDAY'S NOTE AT PLACEMENT:** @FRIDAY_CHECK@
**Client:** Datasec only. **Project:** MPS Commercial Calculator only. **Tier:** 2. Production-class steps run only in the order below.
**Report:** `1_Project_Definition/Briefs/2026-10-13_B73_STATUS.md` only. Its exact LAST line is **`DEPLOYED: <sha> live-check <n>`** (with ` feedback-store on` appended if PART B ran and passed) or **`STOPPED: NEEDS FRIDAY`**, followed by the one question that blocks you.
**Launch:** Friday runs `bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/MPS-F "bash '/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/brief_seat.sh' datasec '/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator' '../../../FRIDAY/2_Project_Files/friday/briefs_drafts/2026-10-13_B73_SEAT-F_hosted-deploy-bf60fe8.md'"` (path relative to the project dir, resolving into Friday's tree; `ls`-checked in the launch command). The form is `brief_seat.sh:3-4`. Friday does not use the project's own `Launch_Claude.command` (its rule 4: no Azure tenant assigned to the project; ask before any az command). B55 was launched the same way.
- **Consequence you must handle:** `brief_seat.sh` runs through `friday_as.sh datasec`, which exports Friday's `AZURE_CONFIG_DIR`, NOT this project's. **Set `AZURE_CONFIG_DIR="$PWD/4_Credentials/.azure"` on every `az` call and every script that calls `az`** (B55 did, `B55_STATUS.md` § C-2). Never run `az` with Friday's directory or `~/.azure`.
- There is no launcher preflight in this launch. Write "none (brief_seat launch)" in STATUS.

**Convention.** Records under `1_Project_Definition/Briefs/` are untracked working-tree files; `file:line` means the file as Friday's drafter read it at @NOW@. Code is cited as `path:line @ <sha>` in `2_Project_Files`. The drafter used read-only git verbs only (`--no-optional-locks`, no fetch) and `friday_as.sh datasec gh api` GETs. "UNMEASURED" means the drafter did not read it, so you measure it.

## AUTHORITY
- **Deploy card `mpscalc-hosted-deploy-bf60fe8-1013`** (Friday's board). Friday launches this seat only after Kam taps **a** (code only) or **b** (code + PART B). On **c** this seat is not launched. The placement note above names the ruling and its time; if it is missing or says anything else: **STOP: NEEDS FRIDAY** before step 0.
- **Words, already ruled by Kam:** card `mpscalc-feedback-pill-words-1013` ruled **a** "Approve as written" (Kam, live board, 2026-10-13 08:49:58 per Friday's daily note `daily_friday/2026-10-13.md:92`; card `ruled_ts` 2026-10-13T08:50:36+11:00 in `0_Brain/dashboard/data/decisions.json`). Option a's detail: *"The words ship with the next MPS hosted deploy unchanged."* This covers the feedback feature's whole words list (gate B68: *"whole feature 106 / 0 undeclared"*, `B68_STATUS.md:16`).
- **Words with no Kam ruling (operator- or log-only; not reachable by a signed-in user on the hosted site; covered by the deploy card's a/b):** B53's 49 strings (`B53_STATUS.md:239-275`; admin source-lifecycle problem details and start refusals: on hosted every lifecycle route answers 409 `SOURCE_LIFECYCLE_OFF` first, `SourceAdminEndpoints.cs:8-10,318-330 @ bf60fe8`, because Entra mode runs with the version store off) and B54's 4 start-refusal fragments (`B54_STATUS.md:188-199`). B58: 0 visible strings (`B58_STATUS.md:240-248`). B62: `tools/leakscan/` only, not in the package (`scripts/package.sh:43-55 @ bf60fe8` packs `dotnet publish` + `web/dist`). B69: 0 new string literals (drafter: `git diff 220956b bf60fe8 -- src` changes one condition and one doc comment, `CatalogueOverlayStore.cs:432,437 @ bf60fe8`).
- **READY (the ship chain; every line below the drafter read):**

| PR | Merge SHA on main | Gate verdict (quoted) | Gate record |
|---|---|---|---|
| #29 B53 source-store hardening | `d711b42cfcb53da3a2043a2d672511f8ea6ea296` | `B53 3852d30: GO WITH NOTES` · `MERGE 1329f2e+3852d30: GO WITH NOTES` | `B57_STATUS.md:8,13` |
| #30 B54 + B58 overlay residue + fix round | `65f82f1189f9c7f6196ee6c97bce4f097328ff9a` | B57 on B54: `overall: NO GO` (`B57_STATUS.md:16`) → B59 on B58: `overall: GO WITH NOTES`; `COMBINED d711b42+727c7c8 (tree 2f0e21eb): GO WITH NOTES` | `B59_STATUS.md:12-13`. Drafter: `65f82f1^{tree}` = `2f0e21eb4c77184d557a033151448ecc2a8e6c2d` = the graded tree |
| #31 B62 + B64 leak scanner | `f4616886ef232d7c39b7faa10bde4cb33a6f2c8b` | **Tier 3, no QA gate: Friday-reviewed** (B62 at 05:47, B64 at 06:03; `daily_friday/2026-10-13.md:59,61`). PR head `4397067e` = B64's READY line | `B62_STATUS.md:4`, `B64_STATUS.md:4` ("QA tier 3") |
| #32 B60 + B65 + B70 feedback pill | `220956b19ab104d1df33e643e238167a286673f2` | B63: `overall: **NO GO** (round 1 of 2)` (`B63_STATUS.md:9`) → B68 on B65 `6b13c21`: `overall: **GO WITH NOTES**` (`B68_STATUS.md:19`). B70 (`6b13c21..da66a0d`, one test file +16 −3) **tier 3, Friday-reviewed** (`B70_STATUS.md:4`; daily note `:87`) | `B68_STATUS.md:7,19` |
| #33 B69 overlay timing + MPSCALC-95 | `bf60fe83c02c703d5df11253629b268d25c78ab0` | `B69 3a037e2: **GO WITH NOTES**` · `MERGE 220956b+3a037e2: **GO WITH NOTES**` … `merge-tree` = head tree `c62dfb16f89b8419c9d001361068e4f8ce3ff667` | `B71_STATUS.md:1,16` |

- **CI on main (drafter, `gh api`):** run `38321338442` "ci" on `bf60fe83…`, push, `completed success`; check-runs on `bf60fe83…`: 8 of 8 `completed success` (package, CodeQL ×4, web, dotnet, python). Open code-scanning alerts on `refs/heads/main`: **0**.
- **Holds this brief meets:**
  - **SITE HOLD (B25 ADDENDUM-1, `BACKLOG.md:17-22`): stands.** None of the four store-path settings changes (`MpsCalc__QuoteStore__Path`, `__HostedRoot`, `MpsCalc__CatalogueOverlay__Path`, `MpsCalc__ReferenceStorePath`), and `reference.json` stays a regular file. PART B adds a fifth, NEW key only (`MpsCalc__Feedback__Path`), which is not one of the four. **This brief does not lift the SITE HOLD**: B59 lists what lifts it (`B59_STATUS.md:329`); your STATUS reports items (b) and (d) for the records seat.
  - **B39 P-1 HOLD:** B55 recorded the count (0; `B55_STATUS.md:183`). Step 3a re-counts it anyway (one cheap read).
- **This brief covers:** one code-only zip deploy of `bf60fe83…` to the existing site with its own restart; a read-only backup BEFORE the swap; the pre-swap counts; the read-back, live checks and R-1 if needed; and, only on Kam's **b**, PART B (one app setting).
- **This brief does not cover:** any other app setting, any `MpsCalc__Feedback__Jira__*` setting (Kam's MPS-9: *"no hosted Jira for now"*, `CLARIFICATIONS.md:336`), Bicep, `az deployment`, a new Azure resource, Entra or Graph, price-book upload, seed run, quote/outcome/feedback write, mail, Jira, `history.md`, `BACKLOG.md`.

## SHIPS SINCE HOSTED (drafter, `git --no-optional-locks log --oneline --first-parent 1329f2e..bf60fe83`)
```
bf60fe8 B69: overlay timing tests measure the product's window on Linux (thread-pool headroom); MPSCALC-95 empty by refused (#33)
220956b B60: feedback pill (B47 onto main) + B65 fix round (X-1 focusable table region, X-2 Jira page = fixed route names) (#32)
f461688 B62: version the leak scanner as tools/leakscan/ with a test (Friday ruling M3) (#31)
65f82f1 B54 + B58: catalogue overlay store residue and its fix round (gates B57, B59) (#30)
d711b42 Source version store hardening (B53; gate B57 GO WITH NOTES) (#29)
```
`git diff --stat 1329f2e bf60fe8`: 44 files changed, +7,928 / −122. Per commit: #29 5 files · #30 5 · #31 3 (`tools/leakscan/` only) · #32 31 · #33 4 (one product line). Each commit's single parent is the previous one (`git rev-list --parents -n1`).

## Target asserts (in `2_Project_Files`; `git fetch origin` is allowed, then read-only verbs). Any mismatch: **STOP: NEEDS FRIDAY**
1. `git ls-remote origin refs/heads/main` = **`bf60fe83c02c703d5df11253629b268d25c78ab0`**. Drafter: equal at @NOW@. Anything else (main moved): STOP.
2. `git rev-parse bf60fe83…^{tree}` = **`c62dfb16f89b8419c9d001361068e4f8ce3ff667`** (= `3a037e24…^{tree}`, B71's merge tree). Drafter: equal.
3. `git rev-list --parents -n1 bf60fe83…` = one parent **`220956b19ab104d1df33e643e238167a286673f2`** (a squash). Drafter: equal.
4. `git merge-base --is-ancestor 1329f2e824e9237e44ebb01918993ec0111a6972 bf60fe83…` rc 0 (drafter: rc 0). Record `git log --oneline --first-parent 1329f2e..bf60fe83` verbatim; it must equal the five lines above.
5. `git diff --name-only 1329f2e bf60fe83 -- infra scripts .github` = **empty** (drafter: empty). Not empty: STOP.
6. **Migrations / config, listed (record each line in STATUS; drafter's reads):**
   - **0 migration steps.** `git grep -n -i migrat bf60fe83 -- src` → 0 hits, rc 1. (B57's "MPSCALC-91 start marker + migration" is inside the source version store, which is off on hosted.)
   - **Quote store: unchanged.** `git diff --name-only 1329f2e bf60fe83 -- src/MpsCalc.Api/Quotes src/MpsCalc.Engine src/MpsCalc.Import` → empty.
   - **Overlay format string unchanged:** `"mpscalc-catalogue-overlay/1"` (`CatalogueOverlayStore.cs:24 @ 1329f2e`, `:25 @ bf60fe8`). What changed is what loads: B54 H-4 and B69 MPSCALC-95 make `WellFormed` stricter (`:434-437 @ bf60fe8`, now refusing `by: ""` too), so a hosted `overlay.json` that fails it **refuses the start (an outage)** (`B57_STATUS.md:479`). Step 3e counts it.
   - **New settings, all optional, none placed by this deploy:** `MpsCalc:Feedback:Path` (empty/absent = store unavailable, every feedback call answers 503 `FEEDBACK_STORE_UNAVAILABLE`, **no start refusal**: `FeedbackStore.cs:114-116,128-130 @ bf60fe8`; `docs/API.md:530`), and `MpsCalc:Feedback:Jira:*` (**`Enabled` defaults false and then nothing else is read**: `FeedbackTickets.cs:13-14,22,27-29 @ bf60fe8`; enabled with a bad setting refuses the start, `:84-85`).
   - `src/MpsCalc.Api/appsettings.json`: not changed in the range, and has no `Feedback` key (`git grep` rc 1). `appsettings.Development.json`: +2 −1 (the DevStub feedback path); `package.sh:48 @ bf60fe8` removes that file from the package.
   - `MpsCalc:SourceVersions:Path` must stay ABSENT (Entra mode with a value refuses the start; B71 `:125`).
   - Re-measure all of them and record the commands.

**Live today:** main `1329f2e824e9237e44ebb01918993ec0111a6972`, deployed by B55 (`B55_STATUS.md:221`, last line `DEPLOYED: 1329f2e… live-check 0`).
- Package `mpscalc.zip` sha256 **`54eff4f1592dbe6d7d7d9d1dbb547878405ac6028fd4c38dde972d1cf0556b69`**, 2,790,213 bytes, 48 files, kept at `.tools/wt-B55-release/.local/deploy-packages/1329f2e824e9237e44ebb01918993ec0111a6972/` (`B55_STATUS.md:81`). The drafter re-hashed it at @NOW@: **equal**, 2,790,213 bytes.
- 16 app settings at B55's end (`B55_evidence/30_end_appsettings.tsv`; the drafter read the NAME column only): no `MpsCalc__Feedback__*`, no `MpsCalc__QuoteStore__HostedRoot` (the code default `/home/data/` applies, `QuoteFileStore.cs:20 @ bf60fe8`), no `MpsCalc__SourceVersions__Path`.

**Site:** `app-mpscalc-showcase-u6agl3edszqvs` in RG `mpscalc-showcase-rg`, subscription `a6b8fe11-d1b5-4293-8727-b34aba08a705`, tenant `ec01829b-fdcb-4503-9834-eb2ffbd99169` (`B55_STATUS.md` § C-2).

## HOLDS (absolute)
- Datasec only; no other client's names, tickets or paths, and no other project's resources. **Never touch `datasec-sales-portal-rg`** or anything outside `mpscalc-showcase-rg`. An authorization error is the boundary: report it, never work around it.
- **No data change beyond the deploy itself.** No non-GET to `/api/v1/**`: no outcome, PATCH, duplicate, create, inventory edit, or **feedback POST**. No proposal GET (it writes an event, `B38_STATUS.md:316`).
- No app-setting change, **except PART B's one key and only on Kam's b**. No `az webapp restart` (the deploy's restart, and PART B's settings-change restart, are the only ones). No Bicep, `az deployment`, new resource, plan or SKU change. **A new paid resource of any kind is a STOP.**
- **No temporary access is opened** (no access-restriction rule, basic-auth, publishing credential, publish profile, SAS or firewall change). Kudu is reached with your az token. Steps 1 and 9 prove the posture unchanged.
- Kudu **GET only** (VFS GET and the zip GETs of step 2). No VFS PUT/DELETE, `/api/command` or SSH. `--clean true` is the deploy script's own documented wwwroot replacement.
- Price books untouched and never printed (MATCH/MISMATCH only). Never `upload-pricebooks.sh upload`. No seed run; the seed token is for GETs only, acting as Seller (B33/B55 method).
- **Never print a secret; never open `.env` values into output.** Export only the named `.env` lines (`MPSCALC_SEED_*`). B55 found `MPSCALC_API_CLIENT_ID` and `MPSCALC_HOSTED_HOST` absent from `.env` and used the live `/auth-config.json` app id and the host above (`B55_STATUS.md:190`); do the same. Never a token on argv. **Quote, overlay and feedback contents are never printed:** counts only.
- No mail to any human (Friday tells Kam). No Jira. No `5_Project_History/history.md` (write `## For the records seat` in STATUS). No commit or push in any repo. No `BACKLOG.md` edit.
- Never delete; quarantine to `.tools/_quarantine/2026-10-13_B73_<what>/` (0700) and say so.
- Git in `2_Project_Files`: `fetch`, `worktree add`, `ls-remote` and read verbs, with `--no-optional-locks`. Never `checkout`/`switch`, `reset`, `gc`, `prune` or `worktree remove`.
- Processes: kill by port + cwd, never by name. Seat ports `5780`/`5783`; `5080`/`5173` are Kam's.
- Instruments: `cmd > out 2>&1; rc=$?`, then read the file (zsh: `$pipestatus[1]`). Every verdict is a ratio with its denominator.

## Steps (in order; record each command verbatim with its rc and the measured line)
0. **Identity (C-2)**, with `AZURE_CONFIG_DIR="$PWD/4_Credentials/.azure"`: `echo "$AZURE_CONFIG_DIR"` must print `…/Datasec MPS Commercial Calculator/4_Credentials/.azure`; `az account show --query '{t:tenantId,s:id,u:user.name}' -o json` must give `t=ec01829b-fdcb-4503-9834-eb2ffbd99169`, `s=a6b8fe11-d1b5-4293-8727-b34aba08a705`, `u=kamil@datasec-rd.com`. Anything else: STOP. Never `az login` / `az account set` yourself.
1. **Pre-read (read-only), B55's evidence set** (`B55_evidence/01_pre_*`):
   - **App settings:** names `diff` empty against `B55_evidence/30_end_appsettings.tsv` (16). Assert `MpsCalc__SourceVersions__Path`, every `MpsCalc__Feedback__*` and `DOTNET_SYSTEM_IO_DISABLEFILELOCKING` absent. An unknown name: print the name only, then STOP.
   - **`az resource list -g mpscalc-showcase-rg`:** the plan and the site only, both Succeeded.
   - **Access posture:** `az webapp config access-restriction show …` and `az webapp show … --query '{https:httpsOnly,state:state,hostNames:hostNames}'`; save both for the end `cmp`.
   - **Kudu VFS GET** (paths relative to `/home`, B55 candidate 3): file counts under `data/quotes/` and `data/snapshots/` (7 at B55: 5 + 2); the `data/catalogue-overlay/` listing (empty at B55); `data/pricebooks/` (`reference.json`, `mime` + `size`, regular file); and **`data/feedback/`** (expect 404 / absent; record it).
   - **Seed as Seller:** `GET /api/v1/quotes` (count + states as counts), `GET /api/v1/catalogue/devices` (200, count), `GET /api/v1/inventory` (200, `overlayVersion`, manual-row count; B55: version 0, 0 manual).
   - **`reference.json` MATCH** (sha256 in memory).
2. **BACKUP FIRST (before any count, package or swap).** Kudu zip GETs with your az token: `GET https://<scm>/api/zip/data/quotes/` and `…/api/zip/data/catalogue-overlay/` into `.tools/backup-B73/` (0700; files 0600; assert `git check-ignore` on `.tools/`). Manifest per entry: relative path, size, sha256 (no contents). Assert zip quote+snapshot count = step 1's VFS count, and each VFS file byte-equal to its zip entry (B55 `02_backup_vs_vfs.txt` method). Fallback if the zip API is not 200: VFS GET each file. No backup with matching counts: STOP. This manifest is the baseline for the rollback rule and step 9.
3. **MANDATORY PRE-SWAP COUNTS. Each is a STOP condition unless marked. Read the backup copy in memory; print COUNTS ONLY.**
   - **3a. P-1 / B38 L-2:** copy `.tools/qa-B55/tools/dupscan55.py` to `.tools/qa-B73/tools/` (it already prints counts only and reads the zip). Control first: synthetic `[1,1]` → 1, `[1,2]` → 0. **Count > 0: STOP** (`B38_STATUS.md:315`).
   - **3b. PRE-2 owners (not a STOP; for Friday):** distinct non-null `ownerName`; `"Signed-in user"` count; `Owner == null` by latest status with Submitted separate (B55 method, `B55_STATUS.md` step 3b).
   - **3c. PRE-3 (not a STOP; baseline for step 9 and the rollback):** quote files carrying `outcome`, non-empty `events`, non-empty version `priceAudit`. Since `1329f2e` is live, any of them may now be > 0 (users can record Won/Lost). Record; do not stop on it. (B55 correction: `priceAudit` existed before, `B55_STATUS.md:37`.)
   - **3d. Overlay presence:** is there a `overlay.json` in the backup? (B55: the directory was empty.)
   - **3e. PRE-1 as amended by B69 (C-24), on the hosted `overlay.json` from the backup.** This command supersedes B57's PRE-1 (`B57_STATUS.md:505`): B69 says *"PRE-1 amended (C-24; supersedes `B57_STATUS.md:505`, which is left as it is)"* (`B69_STATUS.md:101`), and gate B71 confirms *"B69 PRE-1 amended: YES"* (`B71_STATUS.md:15`). The amended command counts everything B57's did (null/absent `by`/`key`/`field`/`reason`, absent `at`, undefined `itemClass`) **plus** an empty `by`. Run it verbatim from `B69_STATUS.md:102-117` (copy the block exactly; replace only `"<hosted overlay.json>"` with the path of the extracted copy under `.tools/backup-B73/`, 0600, in a 0700 work dir). It prints counts only and exits 1 on any count.
     - Control first, on synthetic files in `.tools/qa-B73/ctl/`: a good file → `PRE-1 count: 0` rc 0; `by: ""` → 1, rc 1; `by` absent → 1, rc 1; `itemClass: 99` → 1, rc 1 (B69's own controls, `B69_STATUS.md:118-119`).
     - **If 3d found no `overlay.json`:** do NOT run the command on a missing file (it would fail with rc 1 for the wrong reason). Record `PRE-1: overlay.json absent in the backup → 0 entries (not run)`; that is a pass.
     - **Count > 0 (rc 1): STOP: NEEDS FRIDAY, with the count by kind.** The new build would refuse to start on that file (`B57_STATUS.md:479`; `CatalogueOverlayStore.cs:418,434-437 @ bf60fe8`). Never edit `overlay.json`.
     - Report the `info` line (an absent `itemClass` opens as `device`, `[B54-R1]`) as a count, not a STOP.
     - Whitespace-only authors still open and count 0 (`[B69-1]`, `B71_STATUS.md:196`): say so; not a STOP.
4. **Package from a CLEAN checkout; verify the rollback package; PRE-2 (B57) against the build.**
   - `git fetch origin`; new detached worktree `.tools/wt-B73-release` at `bf60fe83…` (0700). Assert tracked diff 0, ignored 0, untracked 0. Project SDK `.tools/dotnet`, `MSBUILDDISABLENODEREUSE=1 UseSharedCompilation=false`.
   - `bash scripts/package.sh bf60fe83c02c703d5df11253629b268d25c78ab0`, then `python3 -I scripts/deploy-package.py verify .local/deploy-packages/bf60fe83… --expect-commit bf60fe83…` rc 0. Quote the sha256, bytes, file count and the B2-scan line (file count UNMEASURED; not a pass condition; B55 had 48).
   - **Rollback package:** `.tools/wt-B55-release/.local/deploy-packages/1329f2e…/mpscalc.zip`, sha256 `54eff4f1…56b69`; `deploy-package.py verify … --expect-commit 1329f2e824e9237e44ebb01918993ec0111a6972` rc 0. Gone or different: rebuild in a NEW worktree `.tools/wt-B73-rollback` at `1329f2e` (a rebuilt zip's sha256 may differ; not a failure). **Do not deploy before a verified rollback package exists.**
   - **4b. PRE-2 (B57 `:506`; still owed per B59 `:327`):** in the release worktree, a Release DevStub run of the same commit on port `5780` with a SYNTHETIC HostedRoot under `.tools/qa-B73/roots/` (never `.local/pricebooks/`; a synthetic reference as B59 did). Copy B59's W-1 live probe (`.tools/qa-B59/tools/h3_59.py`, method `B59_STATUS.md:133-135`): an outside process holds `overlay.lock`; N = 2 waiting writes; release; then 3 single PATCHes 1 s apart. 3 runs. **FAIL (STOP): any next write after the release that is not 200**, or a Busy run that changed the file. Stop the process by its own pid and port afterwards.
5. **Swap (deploy the code; no setting touched).**
   - Re-run C-2. Re-read assert 1 (main unchanged).
   - `AZURE_CONFIG_DIR="$PWD/4_Credentials/.azure" bash scripts/deploy-from-ci.sh deploy bf60fe83c02c703d5df11253629b268d25c78ab0 mpscalc-showcase-rg app-mpscalc-showcase-u6agl3edszqvs`.
   - **Whatever it returns,** `… deploy-from-ci.sh check .local/deploy-packages/bf60fe83… mpscalc-showcase-rg app-mpscalc-showcase-u6agl3edszqvs`. **This rc is `<n>` on the DEPLOYED line.** Exit 3 = DEPLOYED BUT NOT PROVEN: re-run `check` read-only; still unproven → rollback rule.
   - **Start log** (B55 method, `StartupLogs/*_success.log` by VFS GET): the **two** Accept warnings (quote store, overlay; no feedback store yet), "Application started", **0 "Start refused"** (any store, the overlay `WellFormed` refusal, a Jira refusal, the SourceVersions refusal). A refused start: rollback rule NOW.
   - **Overlap identity on hosted (B59 `:328`, `[B58-R6]`):** the overlay's `stat(2)` identity has no log line (`CatalogueOverlayStore.cs:279-295 @ bf60fe8` returns null silently), so record `identity on hosted: not observable from the start log; UNMEASURED` (Friday's item, not a STOP).
   - **L1:** the B55 table, every row. **R1:** settings 16, `diff` 0/0/0; resources = pre; store count = pre; seed list = pre; `overlayVersion` = pre; overlay listing = pre; `reference.json` MATCH, regular file.
6. **Live check (READ-ONLY; seed as Seller).**
   - **POST-1:** `GET /api/v1/quotes/figures` → 200 (B55: 200). 500 → rollback rule.
   - `GET /api/v1/quotes?status=submitted` → 200; 10 calls each of `/api/v1/quotes` and `/api/v1/quotes/figures`, p50/p95 (p95 < 1 s).
   - **Feedback routes:** `GET /api/v1/feedback` with no token → **401**; as seed Seller → **403** (Administrator only; B63 `:259` arms). Record both. (A feedback POST is a write: `NOT TESTED (Friday)`.)
   - **Source admin routes stay off:** `GET /api/v1/admin/sources` no token → 401 (B55: 3/3).
   - **New words in the live bundle:** in the wwwroot `check` downloaded, count these 5 strings from `web/src/feedback/words.ts @ bf60fe8` and the B65 label: `Send feedback`, `All feedback`, `Thanks, your feedback is saved.`, `Feedback is not available right now.`, `All feedback table`. Control: the `1329f2e` live bundle in `.tools/qa-B55/live` (expected 0 of 5 there; UNMEASURED). Report counts with denominators. Also re-count B55's Home strings (54) with `.tools/qa-B55/` `words55.py`: expect 54 of 54.
   - **Home and the pill rendered for an Entra sign-in:** `NOT TESTED (no seat Entra account); Friday's check`.
7. **Rollback note (into STATUS verbatim, section `## Rollback note (for Friday and Kam)`):** *"The rollback target is 1329f2e (package 54eff4f1…, kept). The quote store code is unchanged between 1329f2e and bf60fe8 (no file under src/MpsCalc.Api/Quotes, Engine or Import changed), so a rollback is not expected to drop Won/Lost outcomes, events or price audits (UNMEASURED by a run). The overlay format string is unchanged; 1329f2e's loader is more lenient than bf60fe8's, so it is expected to read what bf60fe8 writes (UNMEASURED). Feedback saved after PART B stays on disk under /home/data/feedback/ and is invisible under 1329f2e (no feedback code); nothing deletes it."*
8. **Leak check** on the live wwwroot and the L1 bodies: copy B55's instrument (`.tools/qa-B55/tools/`, `lists/`; fix `ctx55`'s Vite-hash regex per B55 candidate 2 if it still reports a false "multiset differs") to `.tools/qa-B73/` (0700). Control must fire on every kind. COUNTS ONLY, adjudicated as B55. An unadjudicable client hit: STOP; the site stays as deployed.
9. **End checks (before PART B, and again after it if it runs):** C-2; settings `diff` (code only: 0/0/0; after PART B: exactly 1 added, `MpsCalc__Feedback__Path`); access posture `cmp` = step 1; L1; `reference.json` MATCH; store vs backup (same/changed/new/missing, counts only; any change came from real users after the swap: say so, do not read their content); secret grep (seed secret in 0 evidence files, 0 of `.tools/qa-B73/`, 0 in STATUS).

### PART B (ONLY if the placement note says Kam ruled **b**; otherwise write `PART B: not run (Kam ruled a)`)
Kam's MPS-9 already ruled *"Feedback is stored on the site only. No credential is placed and no outbound connection is opened."* (`CLARIFICATIONS.md:336`). PART B places the store; it never places a Jira key.
- **B-0. Preconditions:** steps 5–9 passed. VFS GET `data/feedback/` = absent (404). Present in any form: STOP (do not reuse a directory nobody explained). The path `/home/data/feedback/` is under the default HostedRoot `/home/data/` and is not equal to, inside, or containing `data/quotes/`, `data/catalogue-overlay/` or `data/pricebooks/` (the store's overlap rules, `docs/API.md:530-535 @ bf60fe8`).
- **B-1. Set one key:** `AZURE_CONFIG_DIR=… az webapp config appsettings set -g mpscalc-showcase-rg -n app-mpscalc-showcase-u6agl3edszqvs --settings MpsCalc__Feedback__Path=/home/data/feedback/ -o none` (this restarts the app; it prints no setting values with `-o none`). Nothing else in the call.
- **B-2. Start log:** **three** Accept warnings (the third: *"The feedback store at … runs WITHOUT private file modes (MpsCalc:QuoteStore:PlatformModes = Accept)…"*, `FeedbackStore.cs:144 @ bf60fe8`), "Application started", **0 "Start refused"**. VFS GET `data/feedback/` now exists with **0** entries.
- **B-3. Re-run:** L1, POST-1, the feedback 401/403 pair, settings diff (exactly +1), resources, posture `cmp`, store vs backup, `reference.json` MATCH.
- **B-R. PART B rollback (only if B-2 or B-3 fails):** `az webapp config appsettings delete -g mpscalc-showcase-rg -n app-mpscalc-showcase-u6agl3edszqvs --setting-names MpsCalc__Feedback__Path -o none`; then the start log (two Accept warnings, 0 refused), L1, POST-1, settings diff 0/0/0 against step 1. Leave `data/feedback/` as it is (never delete). Then **STOP: NEEDS FRIDAY**.
- A saved feedback item end to end (signed-in user → item in All feedback): `NOT TESTED (Friday/Kam)`; no seat write.

### Rollback rule (R-1 = redeploy `1329f2e` from the kept package, then `check`, the start log, L1 and R1; no setting changes)
- **R-1 runs if** the start is refused, `check` stays unproven, or POST-1 answers 500 — and `overlayVersion`, re-read at that moment, is not above the pre-read (if it is: STOP, and never touch `overlay.json`/`overlay.lock`; B31 § Rollback).
- Quote-file changes by users do NOT block R-1 here (the store code is the same on both sides; step 7). Record the store-vs-backup counts before and after R-1.
- If PART B ran, run B-R first, then R-1.
- Every rollback ends in **STOP: NEEDS FRIDAY**, with its `check` rc and the L1 table.

## Post-deploy items (each RUN with evidence or `NOT TESTED (<who>)`)
| Item | This seat | Source |
|---|---|---|
| PRE-1 amended (overlay `WellFormed`, incl. empty `by`) | RUN, step 3e (STOP > 0) | `B69_STATUS.md:101-119`; `B71_STATUS.md:15` |
| B57 PRE-1 (original) | superseded by the amended PRE-1 (same kinds + empty `by`) | `B57_STATUS.md:505` |
| B57 PRE-2 W-1 hand-off against the build | RUN, step 4b (STOP if not 200) | `B57_STATUS.md:506`; `B59_STATUS.md:327` |
| B57 PRE-3 `reference.json` regular file, outside the overlay dir | RUN, steps 1/5/9 | `B57_STATUS.md:507` |
| B57 POST-1 no `MpsCalc__SourceVersions__Path`; app starts | RUN, steps 1/5 | `B57_STATUS.md:508` |
| B57 POST-2 one overlay edit, restart, audit equal | `NOT TESTED (write; Friday/Kam)` | `B57_STATUS.md:509` |
| B63/B68 four held store keys unchanged | RUN, settings diff | `B68_STATUS.md:227` |
| B59 hosted start refused with shipped settings (outage) | RUN, start log | `B59_STATUS.md:328` |
| B59 overlap identity available on hosted | `UNMEASURED (no log line)` | `B59_STATUS.md:328` |
| P-1 repeated `lineNumber` | RUN, step 3a | `B38_STATUS.md:315` |
| POST-1 figures 200 | RUN as Seller; Approver `NOT TESTED (Friday)` | `B52_STATUS.md:376` |
| Feedback pill renders; submit; All feedback | `NOT TESTED (Entra; Friday/Kam)` | `B68_STATUS.md` |
| Jira stays OFF on hosted | RUN: no `MpsCalc__Feedback__Jira__*` in settings | `CLARIFICATIONS.md:336` (MPS-9) |

## Friday's own check (after this STATUS)
Friday signs in through Entra or relays to Kam: Home renders; the Feedback pill shows; with PART B, one feedback sent by Kam appears in All feedback (Administrator); without PART B, sending shows *"Feedback is not available right now. No feedback store is configured on this server, so feedback cannot be saved. Nothing was stored."* (`FeedbackEndpoints.cs:95`, `FeedbackDialog.tsx:152 @ bf60fe8`).

## STATUS (`2026-10-13_B73_STATUS.md`)
- **BLUF** (≤ 6 lines). **Target asserts 1–6** with full SHAs and the migrations/config list. **C-2** verbatim each time. **Backup** (path, entry count, manifest sha256, count assertion).
- **Pre-swap counts 3a–3e**, counts only, each with its control. **PRE-2 (4b)** table.
- **Pre vs R1 vs end** table (and after PART B, if it ran). **Package / verify / deploy / check** verbatim; start log; rollback package verify.
- **L1 table, live-check table, post-deploy items table, leak counts, words counts.**
- **`## Rollback note (for Friday and Kam)`** (step 7).
- **For Kam, in plain words:** what is live, what users see (the pill; whether feedback saves), the PRE-1 / P-1 / PRE-3 counts.
- **`## For the records seat`:** the history line; SITE HOLD items (b) and (d) of `B59_STATUS.md:329` as evidence (do not lift it); `[B69-2]` met by this brief (a deploy ran PRE-1); BACKLOG candidates. Write none of them yourself.
- **UNMEASURED. NOT DONE / NOT TESTED. Processes, worktrees and the backup left.**
- **Last line:** `DEPLOYED: bf60fe83c02c703d5df11253629b268d25c78ab0 live-check <n>` (+ ` feedback-store on` if PART B passed) only when `check` rc is 0 and the start log, L1, R1, MATCH, POST-1 and the leak counts all passed. Otherwise `STOPPED: NEEDS FRIDAY` and the one question.

## UNMEASURED (the drafter's)
- Today's hosted store: quote count, P-1, PRE-2, PRE-3; whether `overlay.json` now exists and its PRE-1 count; `overlayVersion`.
- The new package's file count, size and sha256.
- Whether the 5 feedback strings are absent from the `1329f2e` live bundle (control expectation only).
- Whether the overlay's `stat(2)` identity works on the hosted share (`[B58-R6]`).
- Whether `1329f2e` reads every overlay/quote file `bf60fe8` writes (expected from the unchanged quote code and format string; not run).
- PART B on hosted: whether the feedback store opens on the `/home` share (local hosted-shape arms opened 1/1 with refusals 5/5 on the real package, `B68_STATUS.md:169`; hosted never run).
- The exact current settings values (the drafter read names only, from B55's end file).
