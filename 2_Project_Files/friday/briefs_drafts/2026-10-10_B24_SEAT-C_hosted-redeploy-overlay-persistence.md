From Friday (laptop seat), Datasec / MPS Commercial Calculator. Replies to `friday-laptop-agent@agentmail.to`; if `4_Credentials/.env` has no `AGENTMAIL_API_KEY`, the STATUS file is the wrap.

# BRIEF B24 · SEAT-C — redeploy the hosted showcase to main `a168badaa4a88fcbbd91e7d1350cd45320969ce9` (catalogue overlay persists), in two steps: code first, then ONE app setting
**Report:** `1_Project_Definition/Briefs/2026-10-10_B24_STATUS.md`. Its last line is exactly **`DEPLOYED: <sha> live-check <rc>`** or **`STOPPED: NEEDS FRIDAY`** followed by the one question that blocks you.
**Client:** Datasec only. **Project:** MPS Commercial Calculator only. **Tier:** 2. Production-class steps run only in the order below.
**Pane:** `*MPS*-C`. This is the newest `_SEAT-C_` file in `Briefs/`.

**Convention.** Records files under `1_Project_Definition/Briefs/` are untracked in the records repo. For them, `file:line` means the working-tree file as Friday's drafter read it on 2026-10-10 (~21:15 AEDT). Code is cited as `path:line @ <sha>` in `2_Project_Files`.

## Target
- **`a168badaa4a88fcbbd91e7d1350cd45320969ce9` (main after PR #21 merged; read by Friday from the GitHub API 21:1x, tree 85250ba7)**. PR #21 is `b22/overlay-persistence` = **`04e82389d2fcf4c8945160b6dd7f2c549dd19189` (PR #21 head at merge, read by Friday: `gh pr view 21` MERGED, merge_when_green pinned it)**.
- **Assert all five before anything else.** On any mismatch: **STOP: NEEDS FRIDAY**.
  1. `git ls-remote origin refs/heads/main` = `a168badaa4a88fcbbd91e7d1350cd45320969ce9`.
  2. `git rev-parse a168badaa4a88fcbbd91e7d1350cd45320969ce9^` = `ef694d47176922f01fb877597344d6bd00c02d26` (the live release, `B21_STATUS.md:145`).
  3. `git rev-parse a168badaa4a88fcbbd91e7d1350cd45320969ce9^{tree}` = **`85250ba742464cd51d18ab13957ef91c01b1b8bd`**: the b22 head tree, which gate B23 measured equal to the merge of `ef694d4` + b22 (`B23_STATUS.md:13,45`). This holds only if PR #21's head is `04e8238`; if Friday fills a different `04e82389d2fcf4c8945160b6dd7f2c549dd19189`, Friday also fills the tree here.
  4. `git diff --name-only ef694d47176922f01fb877597344d6bd00c02d26 a168badaa4a88fcbbd91e7d1350cd45320969ce9 -- infra scripts .github` = **exactly** `infra/modules/showcase.bicep`, and `git diff --numstat` for it = `1	0` (the one line, `B22_STATUS.md:197-201`; `B23_STATUS.md:53`).
  5. That one added line, read with `git show a168badaa4a88fcbbd91e7d1350cd45320969ce9:infra/modules/showcase.bicep`, is `MpsCalc__CatalogueOverlay__Path: '/home/data/catalogue-overlay/' // B22: …` (drafter read it at `:83` @ `04e8238`).
- **Live today:** main `ef694d4`, deployed by B21: package `mpscalc.zip` sha256 `a9f4c302cb2e98e848a6516492fae806a2e4af542eb1cc73c7e026694b3c2a0c`, 2,726,813 bytes, 48 files; `check` rc 0; HSTS `max-age=31536000`; 6 quote files; 4 quotes; inventory `overlayVersion` 0, 0 manual rows (`B21_STATUS.md:8-10,33-38,45`).
- **Site:** `app-mpscalc-showcase-u6agl3edszqvs` in RG `mpscalc-showcase-rg`, https://app-mpscalc-showcase-u6agl3edszqvs.azurewebsites.net/ (`B21_SEAT-C_hosted-redeploy.md:18`).

## AUTHORITY
- **Kam, email 2026-10-10 05:23Z**, verbatim: *"This is perfect. Please put it into action"* (`B21_SEAT-C_hosted-redeploy.md:21`; C-13 on `records/b21`). Friday's reading: it covers the MPS deploy after the gates (`:22`).
- **Kam, mail 2026-10-10 03:28Z**, verbatim as relayed: *"…the quote tool should have inventory section and an ability to add and modify prices as well as margins …"* (`B22_SEAT-A_overlay-persistence.md:9`). Friday's reading, not Kam's words: edits lost at every restart do not meet it (`:11`).
- **The one app setting:** ****Friday's recorded reading (21:1x), not a new Kam ruling:** Kam commissioned this hosted showcase (terminal ~09:1x: host it live on Azure for Monday) and approved putting today's work into action (email 05:23Z); Friday's 08:37:52Z email told him catalogue edits are in-memory on the hosted site with this fix as the next lane. Adding ONE app setting to the existing site is reversible in one command (R-2: delete that key) and costs nothing. B21's "no app-setting change" was B21's own scope fence, not a Kam rule. Friday reports it to Kam after it is live; his word reverses it; this brief names exactly one.)**
- **Gate:** B23 = **GO WITH NOTES** for b22 and for `ef694d4` + b22 (`B23_STATUS.md:12-13,345-346`). No Blocker, no Major; 4 Minor (G-1…G-4, `:191-252`). Its post-deploy items P-1…P-6 (`:289-301`) are this brief's live checks; none of them is a gate pass.
- **Standing:** C-06/C-06a hosting in tenant `ec01829b…` under `kamil@datasec-rd.com`; C-12 no self-approval, GST fixed at 10%; gate B15 N-1 **`PlatformModes = Accept`** (`showcase.bicep:84-87` @ `04e8238`; `B22_STATUS.md` Infra).
- **What this covers:** a code redeploy of `a168badaa4a88fcbbd91e7d1350cd45320969ce9` to the existing site; adding **one** app setting; site restarts; the read-back and live checks below.
- **What it does not cover:** any other app setting, any Bicep apply, any new Azure resource, any Entra change (roles, users, assignments, credentials), any price-book upload, any seed run, any write to the overlay by this seat, any mail or message to a human, any Jira write.

## What changes since `ef694d4` (B22, gated by B23)
- **Code:** in Entra mode a configured `MpsCalc:CatalogueOverlay:Path` now **persists** under the quote store's hosted rule (same `HostedRoot`, same `PlatformModes` key), with an exclusive `overlay.lock`, a durable write, and v(n+1) across restarts. New problem code **503 `OVERLAY_UNAVAILABLE`** (`B22_STATUS.md:7-19`). An empty path stays **in memory**, exactly as today (`CatalogueOverlayStore.cs:147-150` @ `04e8238`).
- **At start** with the path set, the app creates `/home/data/catalogue-overlay/` and runs the mode probe (`CatalogueOverlayStore.cs:151-172`; `QuoteFileStore.cs:169-198` @ `04e8238`). On this share the probe reads back 777, so with `Accept` it **logs the overlay warning at every start** (`Program.cs:74-77` @ `04e8238`). `overlay.json` and **`overlay.lock` appear only at the first change** (`TakeFileLock`, `CatalogueOverlayStore.cs:312-317` @ `04e8238`: `FileMode.OpenOrCreate` inside a change).
- **Web:** the proposal wording nit and the contract re-sync only (`B23_STATUS.md:52,55`).
- **Infra:** one added line (Target item 4). Nothing in `scripts/` or `.github/`, so `package.sh`, `deploy-from-ci.sh` and `deploy-package.py` are byte-equal to what deployed `ef694d4`.
- **Docs, read at `origin/b22/overlay-persistence`** (`git show …:docs/API.md`, 402 lines): hosted row `:363`; the deploy order `:365-369`; overlay rule `:235-260`; the corrupt-file recovery `:256-260` (a **person** moves the file to `/home/data/catalogue-overlay/_quarantine_<YYYY-MM-DD>/`, then restarts; the site starts at v0).

## Why two steps, and why no Bicep apply (say this in STATUS in your own words)
- **The old code refuses to start with the setting.** `ef694d4` throws *"Start refused: MpsCalc:CatalogueOverlay:Path must be empty when hosted"* (`CatalogueOverlayStore.cs:63-66` @ `ef694d4`; `B22_SEAT-A_overlay-persistence.md:14`). So the setting goes on **only after** the B22 code is live and proven (`B22_STATUS.md:203-213`; `docs/API.md:365-369` @ b22).
- **The Bicep replaces every app setting, and touches more than settings.** `showcase.bicep:57-59` @ `04e8238`: *"this resource REPLACES the site's app settings on every deploy"*. The same template also re-applies the site config, both publishing policies and the budget with its contact list (`:30-55,91-117`), and B14's applies showed "site/budget noise" in every what-if (`B14_STATUS.md:239,461-462`). Step 1 must not change any setting, so **no Bicep in step 1**.
- **Route for step 2 (Friday's choice): a targeted `az webapp config appsettings set` of the one key, not a Bicep apply.**
  - The project has applied settings only by Bicep (`az deployment sub what-if` then `create`: `B14_STATUS.md:238-240,461-464`; `B14_SEAT-C_ADDENDUM-4_gate-b15-g1-n1-n6.md:5`). That route re-sends the whole template, so it cannot change **only** this setting.
  - `appsettings set --settings K=V` adds or updates the named key and leaves every other key as it is. After it, the live set equals the Bicep at `a168badaa4a88fcbbd91e7d1350cd45320969ce9` (the 15 keys B21 read back + this one), so a later Bicep apply is a no-op for settings. State that in STATUS, with the diff below as proof.
  - Bicep compile was never tested for the added line (`B23_STATUS.md:285`: no `bicep` CLI at the gate). This route does not depend on it.

## Steps (in order; record each command verbatim, with `cmd > out 2>&1; rc=$?` and the measured line)
0. **Login (C-2; B21 brief :71-75).**
   - `echo "$AZURE_CONFIG_DIR"` must print `…/Datasec MPS Commercial Calculator/4_Credentials/.azure`.
   - `az account show --query '{t:tenantId,s:id,u:user.name}' -o json` must give `t=ec01829b-fdcb-4503-9834-eb2ffbd99169`, `s=a6b8fe11-d1b5-4293-8727-b34aba08a705`, `u=kamil@datasec-rd.com`.
   - Anything else: **STOP: NEEDS FRIDAY**. Never run `az login` or `az account set` yourself. Never use another project's config dir or `~/.azure`. An authorization error is reported, never worked around.
1. **Pre-read (read-only), saved for the comparisons below** (the B21 evidence shape, `B21_evidence/01_pre_*`):
   - app settings: `az webapp config appsettings list -g mpscalc-showcase-rg -n app-mpscalc-showcase-u6agl3edszqvs` → **names plus non-secret values** to `01_pre_appsettings.tsv`. Expect **15 names**, equal to `B21_evidence/01_pre_appsettings.tsv` (`B21_STATUS.md:33`). There is no secret in the set (`showcase.bicep:58-59`); **any name not in that set: print the name only, never its value, and STOP: NEEDS FRIDAY.**
   - **Assert `MpsCalc__CatalogueOverlay__Path` is absent** (else STOP: the old code cannot be running with it) and **`DOTNET_SYSTEM_IO_DISABLEFILELOCKING` is absent** (P-1's setting half; present → STOP).
   - `az resource list -g mpscalc-showcase-rg -o table` → the plan and the site, both Succeeded (`B21_STATUS.md:34`).
   - Kudu **VFS GET only**: the file count under `/home/data/quotes/` (expect 6, `quotes/` 4 + `snapshots/` 2; re-measure) and whether `/home/data/catalogue-overlay/` exists (expect absent: no build has ever used it).
   - Seed token, act-as Seller: `GET /api/v1/quotes` → refs and states (expect DEMO-S1 Submitted, S2/S3 Draft, one Draft with no ref: `B21_STATUS.md:36`); `GET /api/v1/catalogue/devices` → 200, count; `GET /api/v1/inventory` → 200, `overlayVersion` (expect 0) and manual-row count.
   - **P-6 · Case (G-4), read-only, now, before any change.** Kudu VFS GET of `/api/vfs/data/QUOTES/` against `/api/vfs/data/quotes/` (the `ls -d /home/data/QUOTES` check of `B23_STATUS.md:301`, done without `/api/command`). **FAIL** (re-grade G-4 as a Blocker): *"the case-variant path resolves to the same directory."* On FAIL: record it, do **not** run step 2, and **STOP: NEEDS FRIDAY** after step 1's checks pass (the B22 code with the setting absent is in memory and safe).
2. **Package from a CLEAN checkout (gate B15 G-2; B21 step 2).**
   - New detached worktree `.tools/wt-B24-release` at `a168badaa4a88fcbbd91e7d1350cd45320969ce9`, chmod 700. Assert tracked diff 0 and ignored files 0 before the build.
   - Project SDK only (`.tools/dotnet`), with `MSBUILDDISABLENODEREUSE=1` and `UseSharedCompilation=false` (`B21_STATUS.md:43`).
   - `bash scripts/package.sh a168badaa4a88fcbbd91e7d1350cd45320969ce9`, then `python3 -I scripts/deploy-package.py verify .local/deploy-packages/a168badaa4a88fcbbd91e7d1350cd45320969ce9 --expect-commit a168badaa4a88fcbbd91e7d1350cd45320969ce9` → rc 0.
   - Quote the package sha256, byte count, file count and B2-scan line. The file count is UNMEASURED (48 at `ef694d4`; B22 added no `wwwroot` asset, so 48 is the drafter's expectation, not a pass condition).
3. **STEP 1 — deploy the CODE, setting still absent.**
   - `scripts/deploy-from-ci.sh deploy a168badaa4a88fcbbd91e7d1350cd45320969ce9 mpscalc-showcase-rg app-mpscalc-showcase-u6agl3edszqvs`. An `az` start-tracking timeout has happened while the site was up (`B21_SEAT-C_hosted-redeploy.md:88`).
   - **Whatever `deploy` returns, run** `scripts/deploy-from-ci.sh check .local/deploy-packages/a168badaa4a88fcbbd91e7d1350cd45320969ce9 mpscalc-showcase-rg app-mpscalc-showcase-u6agl3edszqvs` → rc. It is the wwwroot byte compare plus **HSTS `max-age>0` on https `/health`**, else exit 3. Exit 3 = DEPLOYED BUT NOT PROVEN: investigate, never skip; unproven → rollback R-1, then **STOP: NEEDS FRIDAY**.
   - **Live check L1** (`curl -sS -D -`; status line and HSTS header verbatim), the B21 step-4 set:
     - `/` → 200 `text/html` · `/health` → 200 · `/auth-config.json` → 200 with tenant `ec01829b…`, spaClientId `3c31a4fb…`, apiScope `api://c40e74df…/access_as_user`;
     - `/api/v1/me` → **401** · `/api/v1/quotes` → **401** · `/api/v1/inventory` (no token) → **401**;
     - `http://…/health` → 301; HSTS `strict-transport-security: max-age=31536000` on https responses;
     - data paths `/data/pricebooks/reference.json`, `/home/data/pricebooks/reference.json`, `/reference.json`, `/catalogue-overlay/overlay.json`, `/home/data/catalogue-overlay/overlay.json` → **404 each**. `/data/quotes/` → the SPA fallback, byte-equal (`cmp`) to `/` (gate B15 N-11; `B21_STATUS.md:71`), never a listing;
     - `/api/v1/nope` → JSON 404 `NOT_FOUND`.
   - **Read-back R1:** app settings = step 1 pre-read (`diff` empty: **15 names, the overlay key still absent**); `az resource list` = pre-read; quote-file count = pre-read; seed `GET /api/v1/quotes` = the same refs and states; `GET /api/v1/inventory` → 200, `overlayVersion` 0 (in memory, as before); `reference.json` **MATCH** (below).
   - **Any L1/R1 failure:** rollback R-1, then **STOP: NEEDS FRIDAY**.
4. **STEP 2 — add the ONE app setting** (only if steps 1–3 all passed and P-6 did not FAIL).
   - Re-run C-2. Then:
     `az webapp config appsettings set -g mpscalc-showcase-rg -n app-mpscalc-showcase-u6agl3edszqvs --settings MpsCalc__CatalogueOverlay__Path=/home/data/catalogue-overlay/ -o none`
     (`-o none`: the command otherwise echoes every setting). The platform restarts the site on a settings change; record the time.
   - **Before/after key list, in STATUS:** before = the 15 names of the pre-read; after = the same 15 **with values unchanged** + `MpsCalc__CatalogueOverlay__Path=/home/data/catalogue-overlay/` = **16**. Prove it with a `diff` of name=value lines (non-secret values only, as above): **exactly one added line, 0 changed, 0 removed.** Anything else: rollback R-2, **STOP: NEEDS FRIDAY**.
   - Wait for `/health` 200 (poll, up to the site's start limit of 600 s, `showcase.bicep:65`). A refused start shows in the platform log (Kudu `LogFiles/…_docker.log`, the B14 method, `B14_STATUS.md:302`).
   - **Live check L2** = the whole L1 set again, plus R1 with the settings expectation now 16. Seed `GET /api/v1/inventory` → 200, `overlayVersion` **0**, 0 manual rows (nothing was in memory to lose, `B22_STATUS.md:213`). Kudu VFS: `/home/data/catalogue-overlay/` **now exists**; record its listing by **name only** (expect empty, or a `.mode-probe-*` leftover only if a probe was killed; `overlay.json`/`overlay.lock` absent until a first change).
   - **P-4 · Modes.** In the newest app-container docker log, the start shows the overlay's warning *"The catalogue overlay at /home/data/catalogue-overlay runs WITHOUT private file modes (MpsCalc:QuoteStore:PlatformModes = Accept): <measured>…"* (`B22_STATUS.md:175-177`). Quote the line. **FAIL:** *"no warning while Kudu shows 777, or a refused start."* (`B23_STATUS.md:296`). The quote store's own Accept warning must still be there too.
   - **Restart once** (`az webapp restart -g mpscalc-showcase-rg -n app-mpscalc-showcase-u6agl3edszqvs`), then L2 again, P-4 again (the warning **at every start**), and seed `GET /api/v1/inventory` → `overlayVersion` still 0.
   - **P-3 · Recycling and instance overlap (the half you can read).** In the platform log around the step-1 deploy restart, the step-2 settings restart and the explicit restart: were two containers up at once? Record the start/stop lines (times only). **FAIL:** *"a gap, a duplicate, or a version issued twice"* (`B23_STATUS.md:295`). With no change made, the audit half is **NOT TESTED** (below).
   - **Any L2 failure, or P-4 FAIL:** rollback R-2, then **STOP: NEEDS FRIDAY**.
5. **Price books untouched, store survived. READ-BACK ONLY: never call `upload-pricebooks.sh upload`.**
   - `reference.json` on the site against the main checkout's `2_Project_Files/.local/pricebooks/reference.json`, sha256 compared **in memory**, printing **MATCH/MISMATCH only** (the ADDENDUM-9 method, `B21_STATUS.md:76-77`). Run it at the pre-read, after step 1 and after step 2.
   - **MISMATCH, or a missing quote: STOP: NEEDS FRIDAY.** Do not re-upload and do not re-seed.
6. **Leak check on the live wwwroot** (the B21 step-7 instrument): copy (never edit) `.tools/qa-B21/` tool and `lists/` into `.tools/qa-B24/` (0700); `control` must fire on all kinds; `scan-files` over the live wwwroot zip that `check` downloaded (every file, `strings -n 4` for binaries) and the public responses of L1. **COUNTS only**, with the denominator. Adjudicate as B20/B21 did (`B21_STATUS.md:102-109`). Any unadjudicable client hit: **STOP: NEEDS FRIDAY**; the site stays as deployed.

## Post-deploy items P-1…P-6 (gate B23, `B23_STATUS.md:289-301`) — who can run what
**Measured by the drafter: this seat cannot make a hosted inventory write.**
- Every overlay write needs **Administrator and internal-metrics** (`PATCH /inventory/{key}`, `POST /inventory/manual-items`, and `GET /inventory/audit` too: `docs/API.md:28-30,182` @ b22).
- The only non-human identity, `mpscalc-showcase-seed`, holds **Seller only**: one assignment, `seed → Seller` (`B14_STATUS.md:113,116-117`; `B14_SEAT-C_ADDENDUM-1_f12-f13-ruling-seed-identity.md:6`; `tools/demo/seed.py:59-62` @ `ef694d4`, `HOSTED_SELLER`).
- Act-as **narrows only**: *"A name the token lacks is dropped, never added"* (`docs/API.md:334` @ b22).
- The only holder of those roles is Kam (4 user assignments, `B14_STATUS.md:115`), by delegated sign-in in the browser; Azure CLI pre-authorisation is **OFF** (`B14_STATUS.md:120`).
- **So:** never add a role, never use Kam's token, never write `overlay.json` or `overlay.lock` through Kudu. The write-dependent items are **NOT TESTED** by this seat; record each in STATUS as `NOT TESTED (needs Kam's browser; Friday runs it)`, with the FAIL condition below verbatim. They do not change the `DEPLOYED` line.

| Item | This seat | FAIL condition (verbatim, `B23_STATUS.md`) |
|---|---|---|
| **P-1** Lock across processes on `/home` | Settings half only: `DOTNET_SYSTEM_IO_DISABLEFILELOCKING` absent (step 1, step 4 read-backs). **Lock half NOT TESTED** | *"200 while the lock is held, or the setting is present."* (`:293`) |
| **P-2** Flush on the share | **NOT TESTED** (needs a write) | *"a corrupt or empty `overlay.json` after the restart."* (`:294`) |
| **P-3** Recycling and instance overlap | Platform-log half (step 4). **Audit half NOT TESTED** (audit read needs Administrator + internal-metrics) | *"a gap, a duplicate, or a version issued twice."* (`:295`) |
| **P-4** Modes | **Run** (step 4, at both starts) | *"no warning while Kudu shows 777, or a refused start."* (`:296`) |
| **P-5** Deploy order, then the A1 shape | Deploy-order half **run** (steps 3–4; the brief uses the targeted setting, not a Bicep apply, for the "apply" step). **A1 half NOT TESTED** | *"a down site at either step, v0 after the restart, or the lock missing."* (`:300`) |
| **P-6** Case (G-4) | **Run**, read-only (step 1) | *"the case-variant path resolves to the same directory."* (`:301`) |

**The runbook for the NOT TESTED halves (for Friday; this seat does not run it and does not contact Kam):**
- **Kam (browser, his own roles, a persona that keeps Administrator and PricingAnalyst):** add one manual catalogue item `SYN-B24-1` with an invented price and a reason. **Note for Friday:** the API has no delete route for a manual row (`docs/API.md:28-30` @ b22), so `SYN-B24-1` stays in the live inventory and its audit for good. Friday decides that before asking.
- **Then a seat (an addendum):** seed `GET /inventory` → `overlayVersion` n; Kudu VFS: `overlay.json` and `overlay.lock` present (names only). `az webapp restart` immediately (P-2). After `/health` 200: `overlayVersion` still n, not 0; the overlay file loads (P-2, P-5).
- **Kam:** one more edit on `SYN-B24-1` → the version is **n+1**; `#/inventory` audit reads 1..n+1 with no gap or duplicate (P-3, P-5). `overlay.lock` is still present (P-5).
- **P-1 (seat + Kam at once):** a Kudu `/api/command` `flock -x /home/data/catalogue-overlay/overlay.lock sleep 20` (one command, no shell operators: `/api/command` runs without a shell, `B14_STATUS.md:50`) while Kam saves a change → his screen shows **503 OVERLAY_UNAVAILABLE** within ~5 s, and `overlay.json` sha256 (compared in memory, not printed) is unchanged. Note G-1: a second save queued behind it waits 10 s (`B23_STATUS.md:192-209`).

## Rollback (never delete; the overlay directory and its files are never removed: quarantine only)
- **Rule:** **never run `ef694d4` code while `MpsCalc__CatalogueOverlay__Path` is set.** It refuses to start (`CatalogueOverlayStore.cs:63-66` @ `ef694d4`). Remove the setting first, always.
- **R-1 (step 1 failed; the setting was never added):** redeploy the B21 release.
  - From `.tools/wt-B21-release` (detached at `ef694d4`; its package is under `.local/deploy-packages/ef694d47176922f01fb877597344d6bd00c02d26/`, `B21_STATUS.md:139`).
  - Assert the package sha256 = `a9f4c302cb2e98e848a6516492fae806a2e4af542eb1cc73c7e026694b3c2a0c`, 48 files; `python3 -I scripts/deploy-package.py verify … --expect-commit ef694d47176922f01fb877597344d6bd00c02d26` rc 0.
  - `scripts/deploy-from-ci.sh deploy ef694d47176922f01fb877597344d6bd00c02d26 mpscalc-showcase-rg app-mpscalc-showcase-u6agl3edszqvs`, then `check` → rc; then L1 and R1 (inventory `overlayVersion` 0, in memory).
- **R-2 (step 2 failed: refused start, P-4 FAIL, an L2 failure, or a settings diff other than one added line):**
  - `az webapp config appsettings delete -g mpscalc-showcase-rg -n app-mpscalc-showcase-u6agl3edszqvs --setting-names MpsCalc__CatalogueOverlay__Path -o none`. Settings read-back = the 15-name pre-read (`diff` empty). The site restarts in memory on the B22 code; L1.
  - `/home/data/catalogue-overlay/` and anything in it **stay where they are**. If it holds an `overlay.json` that refuses the start, a **person** moves it to `/home/data/catalogue-overlay/_quarantine_<YYYY-MM-DD>/` (`docs/API.md:256-260` @ b22; B22 ADDENDUM-1 ruling 4). That is not this seat's move: STOP and say so.
  - If the site is still down with the setting gone: R-1.
- Every rollback ends in **STOP: NEEDS FRIDAY**, with the rollback's own `check` rc and L1 table in STATUS.

## HOLDS (absolute)
- **No other Azure change.** The only Azure writes allowed: the zip deploy (with its own restart), the one `appsettings set` (and, in R-2 only, its `delete`), `az webapp restart` (step 4, once), and R-1's redeploy. **No Bicep apply, no `az deployment`, no new resource, no plan/SKU change, no Entra change, no spend.** Anything else: **STOP: NEEDS FRIDAY**.
- **Kudu: VFS GET only**, plus nothing else. No VFS PUT/DELETE, no `/api/command` in this brief (the P-1 `flock` is Friday's runbook, not yours). Never write, move or delete a file on the site; `--clean true` is the deploy script's own documented wwwroot replacement.
- **No mail or message to any human.** Friday relays to Kam. **No Jira write.**
- **Price books untouched and never printed:** no value, SKU-with-price, or hash of a real body in any file, STATUS or log you keep. MATCH/MISMATCH only. Never call `upload-pricebooks.sh upload`.
- **No seed run** and no write to `/api/v1/**` other than GETs. The seed token is used for GETs only, act-as Seller.
- **Passwords and secrets are never printed:** the seed secret, tokens, Kam's password. Export only the named `.env` lines (`MPSCALC_SEED_*`, `MPSCALC_API_CLIENT_ID`, `MPSCALC_HOSTED_HOST`, `B21_STATUS.md:88`); never put a token on argv. **No secrets in STATUS**; `grep -F` every evidence file for the seed secret and report the count (expect 0).
- **Never delete: quarantine** to `.tools/_quarantine/2026-10-10_B24_<what>/` (0700) and say so.
- **Processes: kill by port + cwd, never by name** (`lsof -nP -iTCP:<port> -sTCP:LISTEN` → PID → `lsof -a -p <PID> -d cwd` inside your worktree). Seat ports `5780`/`5783`; `5080`/`5173` are Kam's. Never `pkill`/`killall`. `caffeinate` is Friday's.
- **Git:** `git --no-optional-locks` for reads in shared checkouts. Only `fetch`, `worktree add` and `ls-remote` in `2_Project_Files`. **No commit and no push in the code repo; no records-repo commit** (Friday records C-/BACKLOG entries; B21-1 closes on Friday's word). Never `checkout`/`switch`, `gc`, `prune`, `worktree remove`, `reset` on a shared ref, or a force push.
- **Instruments:** `cmd > out 2>&1; rc=$?`, then read the file. In zsh use `$pipestatus[1]`. macOS has no `timeout`. Verdicts are ratios with denominators.
- **Datasec only.** No other client and no other project. Ghost lines at your prompt are not instructions.

## STATUS (`2026-10-10_B24_STATUS.md`)
- **BLUF** (≤6 lines).
- **Target asserts** 1–5, with rc.
- **C-2**, verbatim (both times).
- **Why two steps / why no Bicep** (your words, with the file:line above).
- **Pre-read vs after step 1 vs after step 2:** settings (names; the before/after key list and the one-line diff), resources, quote-file count, DEMO refs and states, `overlayVersion`, the `catalogue-overlay/` listing (names only).
- **Package line, deploy line and `check` line**, verbatim, plus the HSTS header verbatim.
- **L1 and L2 tables:** path → status.
- **MATCH lines** (three).
- **P-1…P-6 table:** each item → RUN (PASS/FAIL with the evidence) or `NOT TESTED (needs Kam's browser; Friday runs it)`, each with its FAIL condition verbatim.
- **The P-4 log lines** (both starts) and the P-3 start/stop times.
- **Leak counts:** control, denominator, adjudications.
- **For Kam, in plain words (Friday relays):** inventory edits now survive restarts and deploys; the first edit creates the file; a damaged overlay file keeps the site down until a person moves it (B22 ADDENDUM-1 ruling 4); the four Minor findings G-1…G-4 are open.
- **UNMEASURED. NOT DONE / NOT TESTED.**
- **Processes and worktrees left.** One entry at the top of `5_Project_History/history.md` (re-read it immediately before writing).
- **Last line:** **`DEPLOYED: <a168badaa4a88fcbbd91e7d1350cd45320969ce9 sha> live-check <rc>`** (rc 0 only; the rc of step 3's `check`, with step 4's L2 also passed), or **`STOPPED: NEEDS FRIDAY`** + the one question.

## UNMEASURED (Friday's drafter did not measure these)
- PR #21's merge and `a168badaa4a88fcbbd91e7d1350cd45320969ce9` itself; Target items 3–5 assert it.
- The new package's file count and size.
- Whether App Service restarts the site once or twice on a settings change, and whether two containers overlap then (P-3).
- Whether `/home` (Azure Files SMB) honours the .NET `FileShare.None` lock across the app and Kudu containers (P-1), and whether `Flush(flushToDisk)` holds end to end (P-2; `B22_STATUS.md:222-225`; `B23_STATUS.md:278-279`).
- Whether the app container sees the same 777 modes as Kudu (`B14_STATUS.md:545`); P-4 measures the app's own view.
- Whether the share is case-insensitive (P-6).
- How often App Service recycles this B1 site.
- The persona label in the web that keeps Administrator and PricingAnalyst for Kam's edit (`B18_STATUS.md:11-14`; the "Pricing analyst" persona is `Seller,Approver,PricingAnalyst`, `docs/API.md:341` @ b22, which has no Administrator).
