From Friday (laptop seat), Datasec / MPS Commercial Calculator. Replies go to `friday-laptop-agent@agentmail.to`. If `4_Credentials/.env` has no `AGENTMAIL_API_KEY`, the STATUS file is the wrap.

# BRIEF B55 · SEAT-G: HOSTED DEPLOY of MPS main `@MAIN@` (the Home dashboard: B46 + B49, PR #28, and the not-yet-deployed #25 to #27) to the existing showcase, code only. Use the B31 PART A / B33 runbook, with four mandatory pre-swap STOP checks.
**From:** Friday (laptop seat), @NOW@. **Seat:** pane `Datasec/MPS-G`. Your commission is the newest `Briefs/` file containing `_SEAT-G_`.
**Client:** Datasec only. **Project:** MPS Commercial Calculator only. **Tier:** 2. Production-class steps run only in the order below.
**Report:** `1_Project_Definition/Briefs/2026-10-12_B55_STATUS.md` only. Its exact LAST line is **`DEPLOYED: <sha> live-check <n>`** or **`STOPPED: NEEDS FRIDAY`**, followed by the one question that blocks you.
**Launch:** Friday runs `bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/MPS-G "bash '/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/brief_seat.sh' datasec '/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator' '1_Project_Definition/Briefs/2026-10-12_B55_SEAT-G_hosted-deploy-home-dashboard.md'"`. The `brief_seat.sh` form comes from its header, `brief_seat.sh:3-4`. Friday does not use the project's own `Launch_Claude.command`, because its rule 4 says *"NO Azure tenant is assigned to this project yet: ask before ANY az command"* (`Launch_Claude.command:88`). The earlier deploy briefs B124 and B133 were launched with `brief_seat.sh` the same way.
- **Consequence you must handle (measured by the drafter):** `brief_seat.sh` runs through `friday_as.sh datasec`. That script exports `AZURE_CONFIG_DIR=<FRIDAY>/4_Credentials/clients/datasec/.azure` (`friday_as.sh:37-38`), which is Friday's directory, NOT this project's. **Set `AZURE_CONFIG_DIR="$PWD/4_Credentials/.azure"` on every `az` call and every script that calls `az`.** Example: `AZURE_CONFIG_DIR="$PWD/4_Credentials/.azure" bash scripts/deploy-from-ci.sh …`. B124 used the same rule, after B119's shell arrived with Friday's directory (`B124 brief:37`). Never run `az` with Friday's directory or with `~/.azure`.
- There is no launcher preflight in this launch. Write "none (brief_seat launch)" in STATUS.

**Convention.** Records files under `1_Project_Definition/Briefs/` are untracked working-tree files. For them, `file:line` means the file as Friday's drafter read it at @NOW@. Code is cited as `path:line @ <sha>` in `2_Project_Files`. The drafter used read-only git verbs only, with no fetch. "UNMEASURED" means the drafter did not read it, so you measure it.

## AUTHORITY
- **Kam, live board, 2026-10-12 13:11:34**, verbatim (about the home dashboard): *"please deploy as soon as its ready"*. Card `mpscalc-home-dashboard-mockup-1012` was ruled **a** (`ruled_ts` 2026-10-12T13:12:04+11:00, `0_Brain/dashboard/data/decisions.json`). The option a detail reads: *"Friday commissions the build: new list fields (value, approved date, mine flag, Won/Lost outcome), the filtered-list routes, the Home page as drawn, then a QA gate. You see screenshots before it goes on the hosted site, and Paul's invite follows once it is live."*
- **READY** has three parts:
  - Gate B52 graded `overall: GO WITH NOTES` for head `c8eda15df5c88a2e343d0c0b67948c7aa25671f2` (`B52_STATUS.md:36,426`).
  - That gate also gave `MERGE b28c95e+c8eda15: GO WITH NOTES` as a fast-forward whose merged tree is **`045b95fe0044eb3c728f8aa8e06785dcdb6506c8`** (`B52_STATUS.md:35,69`).
  - Merged to main through CodeQL as PR #28. **Merge SHA = `@MAIN@`** (Friday fills it in before launch).
- **Words card `mpscalc-dashboard-words-and-queue-1012`:** open at drafting. Its default is *"The deploy proceeds under your 13:11 word with the words as written (option a)"*. If Kam rules **c** ("Hold the deploy until the words change"), Friday does not launch this seat. If he rules a or b, the words ship as written. This seat does not read the board store.
- **Holds this brief lifts or meets:**
  - **B39 P-1 HOLD** (`BACKLOG.md` § "Holds on the hosted site"): *"Lifted only by a brief that records the count."* Step 3 records it.
  - **SITE HOLD (B24/B25):** **stands**. No store-path setting changes, and `MpsCalc:ReferenceStorePath` stays a regular file.
- **This brief covers:** one code-only zip deploy of `@MAIN@` to the existing site, with its own restart. It also covers a read-only backup of the quote store taken BEFORE the swap, the read-back, the live checks, and R-1 if needed.
- **This brief does not cover:** any app setting, Bicep, `az deployment`, new Azure resource, Entra or Graph call, price-book upload, seed run, quote write, outcome write, mail, Jira write, or `history.md`. It also does not cover B47 (the feedback pill is not merged, and its Jira token is NOT part of this deploy) or Paul's invite (Friday and Kam handle it after this).

## Target asserts (in `2_Project_Files`; `git fetch origin` is allowed, then read-only verbs). Any mismatch: **STOP: NEEDS FRIDAY**
1. `git ls-remote origin refs/heads/main` = **`@MAIN@`** (all 40 hex). Anything else: STOP.
2. `git rev-parse @MAIN@^{tree}` = **`045b95fe0044eb3c728f8aa8e06785dcdb6506c8`**, the tree gate B52 graded. A different tree: STOP.
3. Parents (`git rev-list --parents -n1 @MAIN@`):
   - A squash (#24 to #27 were squashes; `B33_STATUS.md:28`) has one parent, `b28c95eb0f73ed0ce7ae410791feefc8b1a059ea`.
   - A fast-forward means `@MAIN@` = `c8eda15df5c88a2e343d0c0b67948c7aa25671f2`.
   - Record which one it is.
4. `git merge-base --is-ancestor db8edfd5082e49f9a1a1b3c23feeb02b36834b21 @MAIN@` rc 0. Record `git log --oneline db8edfd..@MAIN@` verbatim.
   - The drafter read `db8edfd..b28c95eb` = `6c0ba85` (#25 B35), `4437460` (#26 B37), `b28c95e` (#27 Lane A2), then B46/B49 (#28).
   - **All four ship in this deploy.** Hosted has run `db8edfd` since B33 (`B33_STATUS.md:179`; `B38_STATUS.md:306`; `B44_STATUS.md:104` "not deployed").
5. `git diff --name-only db8edfd @MAIN@ -- infra scripts .github` = **empty**. The drafter measured it empty for `db8edfd..c8eda15`, with 69 files changed in total. Not empty: STOP.
6. **Migrations, listed (record each line in STATUS).** The drafter measured all of these at `c8eda15`:
   - **0 migration steps.** The quote file format string is unchanged at `"mpscalc-quote/1"` (`QuoteFileStore.cs:82 @ c8eda15`). A `git grep -i "migrat"` over `src` at `c8eda15` gives 0 hits.
   - **Store shape, additive only:** `PersistedQuote` gains `Events` and `Outcome` (`QuoteFileStore.cs:79-80 @ c8eda15`, against `:79 @ db8edfd`), and `PersistedVersion` gains `PriceAudit` (`:85-88 @ c8eda15`). Files are rewritten lazily, on the next save of each quote. For example, a proposal GET adds one event and re-saves the file (`B38_STATUS.md:316`), and an outcome write re-saves it (`B48_STATUS.md:300`). The deploy itself rewrites nothing.
   - **Settings:** no new required setting. `MpsCalc:SourceVersions:Path` must stay ABSENT, because in Entra mode a non-empty value refuses the start (`SourceLifecycle.cs:110-111 @ c8eda15`; `B41_STATUS.md:628`).
   - Re-measure all three: `git diff db8edfd @MAIN@ -- src/MpsCalc.Api/Quotes/QuoteFileStore.cs` (the record lines), plus `git grep -n -i migrat @MAIN@ -- src`.

**Live today:** main `db8edfd`, deployed by B33.
- Package `mpscalc.zip` sha256 `83f584913338716ca80c2181369a9b8ebf6918434980177ac91f88eb3d2310f3`: 48 files, 2,738,604 bytes, kept at `.tools/wt-B33-release/.local/deploy-packages/db8edfd5082e49f9a1a1b3c23feeb02b36834b21/`. The drafter re-hashed it at @NOW@: equal.
- 16 app settings, `diff` empty (`B33_STATUS.md:8,41,58`).

**Site:** `app-mpscalc-showcase-u6agl3edszqvs` in RG `mpscalc-showcase-rg`, subscription `a6b8fe11-d1b5-4293-8727-b34aba08a705`, tenant `ec01829b-fdcb-4503-9834-eb2ffbd99169` (the datasec-rd tenant, C-06a). URL: https://app-mpscalc-showcase-u6agl3edszqvs.azurewebsites.net/ (`B33_STATUS.md:34,42,59`).

## HOLDS (absolute)
- Datasec only, with no other client's names, tickets or paths, and no other project's resources. **Never touch `datasec-sales-portal-rg`**, and no resource outside `mpscalc-showcase-rg`. An authorization error is the boundary: report it and never work around it.
- **No data change beyond the deploy itself.** No non-GET to `/api/v1/**`: no outcome write, no Won/Lost on any real quote, no PATCH, no duplicate, no create. **No proposal GET either**, because it writes an event and re-saves the file (`B38_STATUS.md:316`). POST-4 of B52 (one outcome on a test quote) is Kam's call and is NOT this seat's.
- No app-setting change. No `az webapp restart` (the deploy's own restart is the only one). No Bicep, no `az deployment`, no new resource, no plan or SKU change. **A new paid resource of any kind is a STOP; money is Kam's.**
- **No temporary access is opened by this runbook.** That means no access-restriction rule, no basic-auth or publishing-credential change, no publish profile, no SAS and no firewall change. Kudu is reached with your az token, as in B33. If any step seems to need temporary access: STOP. Step 1 and the end check prove the access posture unchanged.
- Kudu allows **GET only**: VFS GET, plus the one zip GET of step 2. No VFS PUT or DELETE, no `/api/command`, no SSH. Never write, move or delete a file on the site. `--clean true` is the deploy script's own documented wwwroot replacement.
- Price books stay untouched and are never printed: report MATCH/MISMATCH only. Never call `upload-pricebooks.sh upload`. No seed run. The seed token is for GETs only, acting as Seller (the B33 method).
- **Never print a secret, and never open `.env` values into output.** Export only the named `.env` lines (`MPSCALC_SEED_*`, `MPSCALC_API_CLIENT_ID`, `MPSCALC_HOSTED_HOST`). Never put a token on argv. **Quote contents are never printed:** counts only, with no customer, price, owner name or quote value.
- No mail or message to any human (Friday tells Kam). No Jira. **No `5_Project_History/history.md`:** put a `## For the records seat` section in STATUS instead. No commit or push in any repo. No `BACKLOG.md` edit.
- Never delete; quarantine to `.tools/_quarantine/2026-10-12_B55_<what>/` (0700) and say so.
- Git in `2_Project_Files` is limited to `fetch`, `worktree add`, `ls-remote` and read verbs, using `--no-optional-locks`. Never `checkout`/`switch`, `reset`, `gc`, `prune` or `worktree remove`.
- Processes: kill by port + cwd, never by name. Seat ports are `5780`/`5783`; `5080`/`5173` are Kam's.
- Instruments: `cmd > out 2>&1; rc=$?`, then read the file (in zsh, `$pipestatus[1]`). Every verdict is a ratio with its denominator.

## Steps (in order; record each command verbatim with its rc and the measured line)
0. **Identity (C-2), with `AZURE_CONFIG_DIR="$PWD/4_Credentials/.azure"` set on the call.**
   - `echo "$AZURE_CONFIG_DIR"` as used must print `…/Datasec MPS Commercial Calculator/4_Credentials/.azure`.
   - `az account show --query '{t:tenantId,s:id,u:user.name}' -o json` must give `t=ec01829b-fdcb-4503-9834-eb2ffbd99169`, `s=a6b8fe11-d1b5-4293-8727-b34aba08a705`, `u=kamil@datasec-rd.com` (`B33_STATUS.md:33-36`).
   - Anything else: STOP. Never run `az login` or `az account set` yourself.
1. **Pre-read (read-only).** Copy B33's evidence set exactly (`B33_evidence/01_pre_*`; the method is in `B31 brief` PART A step 1):
   - **App settings:** 16 names, `diff` empty against `B33_evidence/30_end_appsettings.tsv`. Assert `MpsCalc__SourceVersions__Path` absent and `DOTNET_SYSTEM_IO_DISABLEFILELOCKING` absent. An unknown name: print the name only, then STOP.
   - **`az resource list -g mpscalc-showcase-rg`:** the plan and the site only, both Succeeded.
   - **Access posture (new; read-only):** `az webapp config access-restriction show -g mpscalc-showcase-rg -n app-mpscalc-showcase-u6agl3edszqvs`, plus `az webapp show … --query '{https:httpsOnly,state:state,hostNames:hostNames}'`. Save both for the end diff.
   - **Kudu VFS GET:** quote-file count under `/home/data/quotes/` and `/home/data/snapshots/` (6 at B33; re-measure). Also the `catalogue-overlay/` listing, and the `pricebooks/` entry (`reference.json`: `mime` and `size`; a regular file).
   - **Seed, acting as Seller:** `GET /api/v1/quotes` (count, plus states as counts), `GET /api/v1/catalogue/devices` (200, count), `GET /api/v1/inventory` (200, `overlayVersion`, manual-row count).
   - **`reference.json` MATCH** (B33 method, sha256 compared in memory).
2. **BACKUP FIRST (before any count, package or swap).**
   - Kudu `GET https://<scm>/api/zip/home/data/quotes/`, and the same for `/home/data/catalogue-overlay/` (read-only zip GETs with your az token). Save them to `.tools/backup-B55/` (dir 0700, files 0600; `.tools/` is git-ignored at the records root, `.gitignore:29`; assert it with `git check-ignore`).
   - Write a manifest: for each entry, its relative path, size and sha256. No contents.
   - Assert the zip's quote and snapshot entry count = the VFS count from step 1.
   - If the zip API does not answer 200: fall back to a VFS GET of each file into the same folder, then the same manifest and assertion.
   - Price books are not copied. The MATCH line and the local `.local/pricebooks/reference.json` are their backup.
   - No backup with matching counts: STOP. **This manifest is also the baseline for the rollback rule (below).**
3. **MANDATORY PRE-SWAP COUNTS. Each one is a STOP condition. Read the backup copy in memory and print COUNTS ONLY; no ids, names or values in STATUS or the pane.**
   - **3a. P-1 / B38 L-2:** the number of quote files whose fleet (any version's draft) repeats a `lineNumber`, plus the number of such versions.
     - Use a copy of `.tools/qa-B38/tools/dupscan38.py` in `.tools/qa-B55/`, changed only so that it prints the two counts and writes no per-file list (its original writes file paths to its out json, `dupscan38.py:20,26`).
     - Run its control first: a synthetic file with `[1,1]` must count 1, and `[1,2]` must count 0.
     - **Count > 0: STOP: NEEDS FRIDAY, with the count.** After the deploy, no UI edit of such a quote can be saved, and the UI's only way out loses a line (`B38_STATUS.md:213-217,315`). The outcome path still re-saves such quotes as they are (`B48_STATUS.md:300`; `B52_STATUS.md:331`).
   - **3b. PRE-2 (for the notes):**
     - distinct non-null `ownerName` values (a count);
     - how many quotes have `ownerName` = `"Signed-in user"`;
     - quotes with `Owner == null`, split by the latest version's status, with **Submitted counted separately** (`B52_STATUS.md:333,374`).
     - Read both casings, as `dupscan38.py` does. These counts are not a STOP; Friday tells Kam.
   - **3c. PRE-3 baseline:** the number of quote files that already carry `outcome`, `events` or a version `priceAudit`. Expect 0 for all three, because the live `db8edfd` cannot write them. Any > 0: STOP. That would mean the store is not what this runbook assumes.
   - **3d. Sydney time zone, before the swap.**
     - From `@MAIN@`, the figures and list read `QuoteFigures.Sydney` = `FindSystemTimeZoneById("Australia/Sydney")` (`QuoteFigures.cs:33 @ c8eda15`). A missing zone means a 500 for everyone (`B48_STATUS.md:303,317`).
     - Pre-swap evidence is records-only. The live `db8edfd` already resolves the same zone in its calculate path (`QuoteEndpoints.cs:37,213 @ db8edfd`), and hosted quotes have calculation snapshots (count them from step 1).
     - The Linux Kudu container cannot see the app container's `/usr/share/zoneinfo`. The app container cannot be inspected without `/api/command` or SSH, which this brief forbids.
     - So record `pre-swap zone: records evidence only (n snapshots)`. The decisive check is POST-1 (step 6).
4. **Package from a CLEAN checkout.**
   - `git fetch origin`, then a new detached worktree `.tools/wt-B55-release` at `@MAIN@` (0700). Assert tracked diff 0 and ignored files 0.
   - Use the project SDK `.tools/dotnet` with `MSBUILDDISABLENODEREUSE=1 UseSharedCompilation=false`.
   - Run `bash scripts/package.sh @MAIN@`, then `python3 -I scripts/deploy-package.py verify .local/deploy-packages/@MAIN@ --expect-commit @MAIN@`; this must give rc 0. Quote the sha256, bytes, file count and the B2-scan line. The file count is UNMEASURED and is not a pass condition.
   - **Keep the previous build as the rollback:** `.tools/wt-B33-release`, package sha256 = `83f58491…3d2310f3`, 48 files. `deploy-package.py verify … --expect-commit db8edfd5082e49f9a1a1b3c23feeb02b36834b21` must give rc 0.
     - If it is gone or differs: rebuild in a NEW worktree `.tools/wt-B55-rollback` at `db8edfd` (a rebuilt zip's sha256 may differ, which is not a failure).
     - **Do not deploy before a verified rollback package exists.**
5. **Swap (deploy the code; no setting is touched).**
   - Re-run C-2.
   - Run `AZURE_CONFIG_DIR="$PWD/4_Credentials/.azure" bash scripts/deploy-from-ci.sh deploy @MAIN@ mpscalc-showcase-rg app-mpscalc-showcase-u6agl3edszqvs`.
   - **Whatever it returns,** run `… deploy-from-ci.sh check .local/deploy-packages/@MAIN@ mpscalc-showcase-rg app-mpscalc-showcase-u6agl3edszqvs`. **This rc is `<n>` on the DEPLOYED line.**
   - Exit 3 means DEPLOYED BUT NOT PROVEN: investigate, and re-run `check` read-only (B33 met two read failures from a flaky link; `B33_STATUS.md:12-16,59-69`). If it is still unproven: apply the rollback rule.
   - **Start log** (B33 method, `StartupLogs/*_success.log` by VFS GET): both Accept warnings, then "Application started", with **0 "Start refused"** (including the SourceVersions refusal). A refused start: rollback rule.
   - **L1:** the B33 table (`B33_STATUS.md:78-90`), every row.
   - **R1:** settings `diff` empty (16 names, 0 added, 0 changed, 0 removed). Also: resources = pre; quote-file count = pre; seed list = pre (count and states); `overlayVersion` = pre; overlay listing = pre; `reference.json` MATCH, still a regular file.
6. **Live check by this seat (READ-ONLY; seed acting as Seller; no write of any kind).**
   - **POST-1, the hosted health:** `GET /api/v1/quotes/figures` → **200**. A 500 means the zone database is missing or the figures are broken: apply the rollback rule NOW, before any user can record an outcome.
     - If the app-only seed is refused (403), record the code. The zone proof then falls to the list in the next bullet (the list builds `QuoteFigures.Of(…, now)` facts per quote, `QuoteEndpoints.cs:620 @ c8eda15`; whether that path reads the zone is UNMEASURED, so say so), and POST-1 as Approver becomes Friday's check.
   - **List with a filter:** `GET /api/v1/quotes?status=submitted` → 200. Then 10 calls each of `GET /api/v1/quotes` and `GET /api/v1/quotes/figures`, reporting p50/p95 (POST-2: p95 < 1 s). `canApprove=true` needs an Approver, so it is Friday's.
   - **Home is served:** `/` 200. In the live wwwroot `check` downloaded, count the Home strings using a copy of `.tools/qa-B52/tools/checkwords52.py`'s list. Cover the B46 §A rows and B49's deltas (`B52_STATUS.md:309-328`), including the words card's three outcome sentences and three labels ("Whose quotes", "Quote groups", "Quote list"). Use B33's method (`B33_STATUS.md:117-125`): report counts with denominators, plus a control against the `db8edfd` live bundle in `.tools/qa-B33/live` (most should be absent there).
   - **Home renders for an Entra sign-in:** `NOT TESTED (no seat Entra account: the Approver account stopped at MFA registration, B31_STATUS.md:222,278); Friday's check`.
   - **B41/B43 items:** `GET /api/v1/admin/sources` with no token → 401, and the lifecycle routes with no token → 401. The seed is Seller only, so the Administrator 409 `SOURCE_LIFECYCLE_OFF` and the byte-equal admin list are `NOT TESTED (Friday)`. Settings show no `MpsCalc__SourceVersions__Path` (from R1).
7. **Rollback warning: write this into STATUS verbatim, in its own section `## Rollback warning (for Friday and Kam)`.** *"Once a Won/Lost outcome is recorded on the hosted site, rolling back to the previous build drops it: gate B48 measured 10 of 11 re-saved quote files lose `outcome` (B48_STATUS.md:304); B52 re-measured 9 of 10 (B52_STATUS.md:335). The previous live build `db8edfd` also predates the lifecycle events and price audit (#25 to #27), and does not carry those fields (QuoteFileStore.cs:79 @ db8edfd), so they are expected to be dropped on re-save too (UNMEASURED). Before any rollback after today: count files with an `outcome` (PRE-3) and export them first."*
8. **Leak check** on the live wwwroot and the L1 public bodies. Copy B33's instrument (`.tools/qa-B33/tools/`, `lists/`) to `.tools/qa-B55/` (0700). The control must fire on every kind. Report COUNTS ONLY with denominators, and adjudicate as B33 did (`B33_STATUS.md:127-134`). An unadjudicable client hit: STOP; the site stays as deployed.
9. **End checks:**
   - C-2.
   - App settings `diff` empty.
   - Access posture = step 1, byte-equal (the "temp access removed and proven" line: none was opened, and the diff proves it).
   - L1 once more. `reference.json` MATCH.
   - **Store vs backup:** VFS GET each quote and snapshot file into memory and compare its sha256 with the manifest. Report counts only: same, changed, new, missing. This seat wrote nothing, so any change came from real users after the swap. Say that, and do not investigate their content.
   - Secret grep: the seed secret in 0 evidence files, 0 of `.tools/qa-B55/` and 0 in this STATUS.

### Rollback rule (R-1 = redeploy `db8edfd` from the kept package, then `check`, L1 and R1; no setting changes)
- **R-1 runs only if both of these hold, re-read at that moment:**
  - (i) 0 quote files carry `outcome`;
  - (ii) the store-vs-backup compare shows 0 changed and 0 new quote files.
- Otherwise: **do not roll back. STOP: NEEDS FRIDAY**, with the site as it is. The rollback would silently drop users' writes (step 7).
- Before R-1, also re-read `overlayVersion`. If it is above the pre-read: STOP, and never touch `overlay.json`/`overlay.lock` (B31 brief § Rollback).
- Every rollback ends in **STOP: NEEDS FRIDAY**, with its `check` rc and the L1 table.

## Post-deploy items (each RUN with evidence or `NOT TESTED (<who>)`; FAIL conditions verbatim from the gates)
| Item | This seat | Source |
|---|---|---|
| PRE-1 / P-1 repeated `lineNumber` | RUN, step 3a | `B52_STATUS.md:373`; `B38_STATUS.md:315`; `B41_STATUS.md:630` |
| PRE-2 owners | RUN, step 3b | `B52_STATUS.md:374`; `B48_STATUS.md:315` |
| PRE-3 outcomes before any rollback | RUN, steps 3c and 9 | `B52_STATUS.md:375` |
| POST-1 figures 200 | RUN as seed Seller; as Approver: `NOT TESTED (Friday)` | `B52_STATUS.md:376` |
| POST-2 list + approvable, p95 < 1 s | list RUN; `canApprove=true`: `NOT TESTED (Friday)` | `B52_STATUS.md:377` |
| POST-3 analyst tile 6 = tab = list | `NOT TESTED (Kam's account; Friday)` | `B52_STATUS.md:378` |
| POST-4 one outcome on a test quote | **NOT this seat** (only if Kam asks) | `B52_STATUS.md:379` |
| B38 P-2 events +1 on proposal GET; P-3 `[3,5,5]` refusal | `NOT TESTED (writes; Friday/Kam)` | `B38_STATUS.md:316-317` |
| B36 #1 to #8 (duplicate, events, audit, proposal byte-equal) | #2's no-token 401 only: RUN; the rest `NOT TESTED (writes or roles; Friday/Kam)` | `B36_STATUS.md:834-846` |
| B41/B43 admin sources and lifecycle | no-token 401 and settings: RUN; Administrator 409 and byte-equal list: `NOT TESTED (Friday)` | `B41_STATUS.md:625-630`; `B43_STATUS.md:483-487` |

## Friday's own check (after this STATUS, not this seat)
Friday signs in through Entra, or relays to Kam:
- Home renders;
- POST-1 and POST-2 as the Approver;
- POST-3 as Kam's analyst account;
- the words card's sentences on screen.

Friday reports the result to Kam.

## STATUS (`2026-10-12_B55_STATUS.md`)
- **BLUF** (≤ 6 lines).
- **Target asserts 1 to 6**, with the full sha, the parent shape and the migrations list.
- **C-2**, verbatim, each time.
- **Backup:** path, entry count, manifest sha256 and the count assertion.
- **Pre-swap counts 3a to 3d:** counts only, each with its control.
- **Pre vs R1 vs end:** a table.
- **Package lines:** package, verify, deploy and `check`, verbatim. Also the HSTS header, the start log and the rollback package verify.
- **L1 table. Live-check table (step 6). Post-deploy items table.**
- **Leak counts. Home-strings counts.**
- **`## Rollback warning (for Friday and Kam)`** (step 7).
- **For Kam, in plain words:** what is live, what he can now do, what he must not expect to roll back, and the PRE-2 counts.
- **`## For the records seat`:** the history line, the B39 P-1 HOLD count that lifts it, and the BACKLOG candidates. Do not write any of them yourself.
- **UNMEASURED. NOT DONE / NOT TESTED. Processes, worktrees and the backup left.**
- **Last line:** `DEPLOYED: <@MAIN@ full sha> live-check <n>`. Write it only when `check` rc is 0 and L1, R1, MATCH, POST-1 (or its list fallback) and the leak counts all passed. Otherwise write `STOPPED: NEEDS FRIDAY` and the one question.

## UNMEASURED (the drafter's)
- `@MAIN@` itself (PR #28 was not merged at drafting; `refs/pull/28/head` = `c8eda15`).
- The new package's file count and size.
- Today's hosted quote count, P-1 / PRE-2 / PRE-3 values, and whether anyone added quotes since B33.
- Whether the Kudu `/api/zip/` GET answers on this Linux site.
- Whether the app-only seed may read `/api/v1/quotes/figures`.
- Whether `db8edfd` drops `events` and `priceAudit` on re-save (expected from the record shape, not run).
- The zone database inside the app container before the swap.
