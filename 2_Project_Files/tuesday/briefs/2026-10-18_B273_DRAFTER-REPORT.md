# B273 DRAFTER REPORT (HPSM-POC hosted deploy of the PR #160 squash, round 3)

**Brief:** `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-18_B273_SEAT-F7_hpsmpoc-hosted-deploy-pr160.md`, 141 lines, UNSTAMPED: 13 distinct `@…@` slots, 24 occurrences on 23 lines. sha256 `2fcda1e948231d402c9017592d090a29124071d95179a66227e4194907e90503` before this report was written. No `.pre-stamp` exists yet: make one before stamping (it is the refusal control).
**B number:** B273 was free in both folders (`tuesday/briefs/` and `HPSM-POC/1_Project_Definition/Briefs/`: 0 `B273` names in the `ls` of each).
**Template:** B264's brief (read whole, stamped and `.pre-stamp`, diffed: the stamp filled `@MAINSHA@` ×39 and the `____` slots). Also read whole: `B264_STATUS.md` (310 lines), `B269_SEAT-R6` brief (86) + `B269_STATUS.md` (190), `B271_STATUS.md` (110), B264's DRAFTER-REPORT; read in part: `B266_STATUS.md` (1-80), `B267_STATUS.md` (1-90), Tuesday's daily note 2026-10-18 (lines 136-160 + greps).
**Refusal check changed:** B264 grepped one placeholder. The main sha is known now, so B273 refuses on ANY `@[A-Z][A-Z0-9_]*@` slot: `/usr/bin/grep -c -E '@[A-Z][A-Z0-9_]*''@'` = 23 lines on the unstamped brief (control fires); a one-line scratch `x @RULED_PKCS@` counts 1; the BLUF and SELF-CHECK lines that hold the pattern do not match themselves (the quotes split it). Lower-case `@` (mail addresses) does not match.

## Tuesday must stamp (13 slots; recommended default in brackets in the brief)
1. `@COMPLETION_CHECK_AT@` (×1) — **READY needs it, and I found none.** `grep -i "completion check"` on the daily note lists only 16:05 (B262/B263) and an MPS line. Commissioned = B267's 7 + B266's -269 = B271's 8 verdicts (all GO / -281 GO WITH FINDINGS, 0 Blocker / 0 Major).
2. `@KAM_LINE_RUNTIME_CARD@` (×2) — Kam's line for `hpsmpoc-runtime-10013-route-1018`, pasted from `kam_rulings_today.sh`. The daily note's 20:57 entry quotes 20:55:41 "Decision hpsmpoc-runtime-10013-route-1018: a — Wait for Azure, read it at the next deploy". I did not run the tool.
3. `@PANE_FREE@` (×2) — `cockpit.sh status` at stamping; I did not run it (it is Tuesday's tool).
4. `@RULED_BOOT_ENV@` (×3) — the dummy env for the local API start. **The riskiest new step:** I could not measure whether the published API reaches `Now listening` outside hosted-demo mode. `appsettings.Development.json` (SQLite, `Assessment__MigrateOnStartup`) is not in api.zip (zip names: only `appsettings.json`). `Program.cs:32-33` runs `HostedDemoStartup.Read/Guard`, which "refuses to start when any lock fails" (`:31`). The brief uses `dff4019` as the known-good positive control, so an env problem cannot read as an artefact problem.
5. `@RULED_NODE_MINOR@` (×2) — local `.tools/node24` is v24.21.0; hosted is 24.20.0 (same major, different minor). Default: accept, no download.
6. `@RULED_START_WINDOW@` (×2) — default web 420 s / API 900 s from the deploy start (B264: web up at +173 s, API at +508 s).
7. `@RULED_ROLLBACK_TIMING@` (×2) — "within a minute" = the START of the way back. B264's deploy of both apps took 10 min 26 s, and `deploy-from-ci.sh` always deploys BOTH, web then API. Default: never kill a running deploy-from-ci.
8. `@RULED_STARTUP_PAIR@` (×2) — 3213/3211 five conditions [YES, this deploy only].
9. `@RULED_GUARD_CHUNKS@` (×2) — [SPLIT, as B264's ruling].
10. `@RULED_PKCS@` (×2) — [UNCHANGED 2·2·2·121].
11. `@RULED_B271_FINDINGS@` (×1) — [DO NOT BLOCK; 5 Notes].
12. `@RULED_NO_POST@` (×2) — [YES].
13. `@STAMP_TIME@` (×1) — your stamp clock. I typed no clock into any slot.

## Measured (my own reads; UTC 2026-10-18)
- **GitHub** (GETs, `GH_CONFIG_DIR=<HPSM-POC>/4_Credentials/.gh-config`, `gh auth status` = `kamilDatasec`, 11:09–11:16Z):
  - main = `befd45e77b391467a1313af8b7b5e0fc580f7b63`; its tree `bff186533c34f0896a2a0b06652f80de773ff563`, parents exactly [`dff4019…`], committed 11:05:10Z, subject "HPSM-POC round 3: BFF upload counter (HPSMPOC-281/-284/-285) + tests (-286/-283/-282/-287) (#160)".
  - PR #160: closed, merged 11:05:11Z, `merge_commit_sha` `befd45e…`, head `e8f5208c97c8…`, base main. `e8f5208`'s tree = `bff186533c34…` (= B271 `:20`).
  - compare `dff4019...befd45e`: ahead 1, behind 0, 7 files, +526 −53 (per-file counts in the brief; the sum matches B271 `:14`).
  - Runs on `befd45e`: at 11:09Z ci 39121815810 and "Push on main" 39121815772 both `in_progress`, attempt 1. **At 11:15:56Z: "Push on main" completed/success; ci still in_progress.** The brief's text says 11:09Z: both running.
  - Way-back artifacts (11:09:50Z): run 39099314408 web 12126161894 (15,359,065 B, exp 2026-10-25T05:11:57Z), api 12126535479 (49,629,110 B, exp 2026-10-25T05:14:19Z); run 39077252343 web 12117378517 (exp 2026-10-24T23:08:02Z), api 12117432659 (exp 23:14:33Z); all `expired=false`. Run 39099314408 = ci, attempt 1, success.
  - Code scanning on main: open 0; any state 1 (control).
  - Records `HPSM-POC-analysis` main = `d479cb67046186be3e4ecc3fcc97d1fe3f8e5c72`, the same sha B269 read (C-105 `:1235`, 1,512 lines, C-115 `:1469`, `B269_STATUS.md:14-15`). I did not re-read CLARIFICATIONS itself.
- **Range** (`git --no-optional-locks` in `.tools/b271/repo`; `befd45e` is absent there, so I used `e8f5208`, which has the same tree):
  - Risky pathspec `dff4019..e8f5208`: exactly `A api/tests/HpsmPoc.Api.Tests/Assessment/SqliteNonTransactionalMigrationsTests.cs`. The name matches `*Migrations*`. **This differs from B264's expected line**, and the brief states it. Control `d1fca80..dff4019`: 1 line (`M infra/tests/test_deploy_hpsmpoc208.py`).
  - `diff --quiet -- scripts/` rc 0 (control `787d159 d1fca80` rc 1). Migrations 84 = 84, diff 0. `api/src` files in range 0.
  - `appsettings.json` blob `f10fcc8ce37b106f116d6a247498924672306c1b` at both commits; `:17` `"ImportsEnabled": false`.
  - Added config-pattern lines (src, non-test) 0. **The same range's `api/tests` gives 0, so it cannot be the control.** Control `d1fca80..dff4019` `api/tests` = 4.
  - Write calls in added formGate.ts lines 0 with my pattern. **My pattern also reads 0 on `bff.ts`, so it does not fire.** The brief points to B264's pattern, which fired at 3/4.
  - formGate importers (non-test): `bff.ts:14` only.
  - Literals new to `formGate.ts`: 36 distinct, all charset labels / tokens (`/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/d406a122-83e7-4b22-9493-e121325c93e7/scratchpad/fg_base.ts` and `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/d406a122-83e7-4b22-9493-e121325c93e7/scratchpad/fg_tip.ts`). Lines holding: "the files are over their total" 1/1, "the upload was too slow" 1/1, `latin1` 1/3, `complete` 9/9.
- **Packages on disk** (read-only):
  - `wt-B264` HEAD `dff4019…` tree `5180070b…`, 0 tracked changes. Its `out/deploy-packages/dff4019…/` has `RUN` = 39099314408; web.zip `eb45ae76…`, api.zip `022f8b63…` (= B264 STATUS); `SHA256SUMS:3-4` assessment.sql `8a4084b6…`, feedback.sql `d3d66717…`.
  - Modes, dff4019 zips (Python `zipfile`): api 190 entries = 121 files (95 × 0755, 26 × 0644) + 69 dirs 0755; web 2,229 = 1,874 files 0644 + 355 dirs 0755. Not world-readable 0, mode-0 0, `create_system` 3 on all. **I did not run a planted 0600 control.** The brief requires the seat to run one.
  - Markers in the dff4019 web package (757 files outside `node_modules/`): "the files are over their total" / "the upload was too slow" / `latin1` ×1 each, only in `.next/server/chunks/_1dnntxr._.js`; `iso_646.irv:1991` and `unicodefffe` ×0 anywhere.
- **Start command / runtime sources:**
  - `infra/modules/appservice.bicep:83` API `DOTNETCORE|10.0` (no appCommandLine line found by grep); `:176-177` web `NODE|24-lts`, `appCommandLine: 'node server.js'`.
  - `B264_evidence/runtime-post.txt`: API stdout "Writing output script to '/opt/startup/startup.sh'"; platform lines "Pulling image: …", "Starting container: …", "Site started.", "Site is running with patch version DOTNETCORE-10.0.12".
  - B181/B184/B191 STATUS: hosted API logs `Now listening on: http://[::]:8080`, and the old container serves until the new one is up. That explains B264's 30/30 × 200.
  - `deploy-package.py:214-224` sets modes explicitly. `deploy-from-ci.sh:68-69`: two `az webapp deploy … --async false --clean true`, web then API, with no per-app timestamp print.
- **Local tools:** `.tools/dotnet --list-runtimes`: NETCore/AspNetCore 10.0.12 + 10.0.13. `.tools/node24/bin/node` v24.21.0; PATH node v26.8.1. `brief_seat.sh` PLAYWRIGHT 0 (control `AZURE_CONFIG_DIR` 1).
- **Ports:** `lsof -nP -iTCP:7170-7199 -sTCP:LISTEN` rc 1. All listeners: 5000, 7000, 49152, 49181, 49183, 49185, 59869. Assigned 7180–7189.
- **Kit:** `.tools/b264/` holds `rollback264.zsh` (cd `wt-B260`, `$OLDSHA`), `id.zsh` (SHA dff4019 / OLDSHA d1fca80; names RG + both apps), `healthlog.zsh` (20 s, `curl -m 30`, both apps' own hosts), `poll3.zsh`, `platlog.zsh`, `deploy264.zsh`, and `q.sh`. The brief forbids copying `q.sh`. `.tools/.git-lock` absent; no `.tools/b273` or `wt-B273`.

## UNMEASURED (why · the instrument that closes it)
- CI `ci` 39121815810 result, the befd45e artifacts, sizes, expiry, attempt. **Why:** it was running. **Closes it:** `actions/runs?head_sha=…` + `runs/<id>/artifacts` (brief step 5).
- befd45e package contents: the 2·2·2·121 check, the 10 stamp-only API diffs, the web classes, whether `_1dnntxr._.js` keeps its name, and the `iso_646.irv:1991` / `latin1` counts. **Why:** no package existed. **Closes it:** `deploy-from-ci.sh fetch`, `postmerge255.sh`, `webid260.py` / `webkeys.py` / `nftcmp260.py` (step 5).
- befd45e zip modes. **Closes it:** `modes273.py` + a planted 0600 control (step 5A-2).
- Whether either package starts locally under a dummy env, and which settings the API needs. **Why:** it needs a local run (a process + port). As drafter I ran none. **Closes it:** step 5A-1 with the dff4019 positive control and the mode-000 negative control.
- Next.js's exact ready line. **Closes it:** the web local start's stdout (5A-1).
- The exact command in the API container's `/opt/startup/startup.sh`. **Why:** Kudu VFS covers `/home` only, and a Kudu command is forbidden. **Closes it:** nothing allowed in this grant reads it. The brief uses the documented default `dotnet <dll>` and says so.
- The runtime UID inside either container. **Why:** same reason. **Closes it:** none allowed. The brief's uid-independent proof is "every file o+r, every dir o+rx" (5A-2).
- Whether Kudu's `/api/zip` download carries entry modes. **Closes it:** reading `external_attr` in `out/…/live/*.zip` after the deploy (recorded in step 6, not a gate).
- The web's live `appCommandLine`. **Why:** B269 recorded only the API's. **Closes it:** `az webapp config show` on the web (step 2b).
- Hosted state since B269's 08:41:53Z, `az account show`, and which images the new containers pull (10.0.12 vs 10.0.13; Node 24.20 vs 24.22). **Why:** no `az`/HTTP to hosted by rule. **Closes it:** steps 2a/2b, and the step-7 platform-log read.
- Whether 3213/3211 recur, including on 10.0.13. **Closes it:** the step-7 docker-log scan. The cause stays unmeasured (no DB access).
- -281/-284/-285 behaviour on hosted. **Why:** no POST is allowed. **Closes it:** none in this grant.
- Which Pkcs file the hosted process loads. **Closes it:** none allowed (HPSMPOC-254).
- Tuesday's completion-check record; Kam's runtime line from the tool; pane availability. **Closes it:** the stamp.

## Conflicts / tensions found
1. **"Roll back within a minute" vs the runbook's script.** `deploy-from-ci.sh deploy` deploys both apps in sequence and takes ~10 min. A rollback is the same script and takes about as long. The brief makes 60 s the START deadline and forbids killing a running deploy (`@RULED_ROLLBACK_TIMING@`). A web failure while the API deploy is still running therefore waits for the script to return. Splitting the apps would change the runbook, which the grant keeps unchanged.
2. **"Mirror production's start command" for the API.** It cannot be read: appCommandLine is `""`, and the Oryx-generated script is outside VFS. The brief uses `dotnet HpsmPoc.Api.dll` and records this as UNMEASURED.
3. **"Under the same runtime major/minor".** The API is run on BOTH 10.0.12 and 10.0.13, because Kam's ruling waits for the platform to pick 10.0.13 at exactly this start. Web: local 24.21 vs hosted 24.20 (`@RULED_NODE_MINOR@`).
4. **The boot proof needs a non-hosted config the package does not carry.** `@RULED_BOOT_ENV@`, with dff4019 as the control. Without the control, a dummy-env failure would block the deploy for a reason unrelated to the artefact.
5. **B264's risky-path expectation does not carry.** The `*Migrations*` glob now matches a test file name. The brief expects that 1 line, so the seat does not STOP on it.
6. **Two B264 controls do not fire for this range:** config-pattern `api/tests`, and my write-call pattern on `bff.ts`. The brief names substitutes: `d1fca80..dff4019` `api/tests` = 4, and B264's own write-call pattern.
7. **The runtime hold is reversed in meaning.** B264 said "stays 10.0.12, do not change". B273 says do not change, but a platform-chosen 10.0.13 is the awaited outcome: record it, never act on it.
8. **The B264 kit's `q.sh` (DB runner)** would be copied by a whole-folder copy (B269 slip 2). The brief forbids copying it.
9. **CodeQL "Push on main" went green after the brief's text** (11:15:56Z). The brief still says both were running at 11:09Z, which was true; the seat re-reads.

## Process note (mine)
- **I published the brief file once as a claude.ai Artifact by mistake.** I meant to apply two small text edits and used the Artifact tool's `edits` on a publish, not the Edit tool. Result: a private artifact, https://claude.ai/artifact/YXVPC58RV5ZYAGkTgHTLLR (Version 1), holding the UNSTAMPED brief. It is private to the account owner, and no one else can open it. It holds no secret, only names, shas, run ids and hostnames already in the briefs folder. I did not delete it: deletion needs Kam's/Tuesday's confirmation. Tuesday may ask for it to be deleted. The local file is what the seat uses.
- Otherwise: no `az`, no HTTP to any hosted host, no docker, no build, no port bind, no git write. Git was `--no-optional-locks` read verbs in `.tools/b271/repo` and `.tools/wt-B264`. GitHub reads were GETs only. One `.tools/dotnet/dotnet --list-runtimes` and one `node --version` per binary, both read-only. Scratch files (`fg_base.ts`, `fg_tip.ts`) are in the session scratchpad only. A hook refused my first command (a `cd`) and a second (an unquoted `=====`); both were re-run without them.
