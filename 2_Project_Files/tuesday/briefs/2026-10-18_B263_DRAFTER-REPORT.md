# B263 DRAFTER REPORT · HPSM-POC · QA gate (tier 1 overall, one verdict per ticket, round 1 of 2 each) on b262/round2-pkcs-bff-imports-tests @ 094602f
Drafter, 2026-10-18 13:50-14:1x AEDT. Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-18_B263_SEAT-G5_hpsmpoc-gate-b262.md` (template: B259's kit, 158 lines, and its STATUS). B263 was free in both briefs folders (`ls | grep -c B263` = 0 in each, 13:51). Nothing was written under `!CODING/`. Git: read verbs only (`--no-optional-locks`), against `2_Project_Files` and B262's clone `.tools/b262/repo` (the branch object is only there). `gh api` GETs ran under HPSM-POC's `GH_CONFIG_DIR` (`kamilDatasec`). One Jira GET (11 issues, fields status / labels / comment / summary) through B262's `jira.py` imported in-process (credentials read by name inside it, never printed). No docker, no dotnet, no npm, no HTTP to any app host, no az. One scratch download: records CLARIFICATIONS at `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/1c3b60d3-2efd-41a2-8d45-bc3872ebb4c7/scratchpad/clar.md`.

## Read whole
- B259 kit (`2026-10-18_B259_SEAT-G4_hpsmpoc-gate-b258.md`) and its drafter report; B259 STATUS (188 lines); B259 raw rows `1a-dotnet-rows.tsv`, `1a-api-rows.tsv` (the rows quoted in T-a / T-b).
- B262 stamped build brief (127 lines, stamp `:118-127`); B262 STATUS (170 lines); B262 evidence `00_FAIL-first.md`, `01_results.md`, `02_mutants.md`, `03_names.txt`, `04_suites.txt`, and `logs/` `diff-names.txt`, `sqlserver-shard1-tip-summary.txt`, `gitleaks-*.txt`, `mut401-m1.txt`, `276-bffread-tip.tsv`.
- The full product diff (`formGate.ts`, `ImportEndpoints.cs`) and every test diff except `ShapeAnchorTests.cs` and most of `PkcsInPackageTests.cs`, which I read by excerpt (`:1-140` at tip).
- Records CLARIFICATIONS C-112 (`:1344-1422` @ `5d45352a`).

## Measured (each with its command and time)
- **`ls-remote` 13:51:05:** `b262/round2-pkcs-bff-imports-tests` = `094602f0285ccf8df23bcace1c352883b96fcb78`; main = `d1fca809e28b283b29a54d02816efcc6409b5b67`. Both equal the commission. `094602f` is NOT in `2_Project_Files`' object store (`cat-file -t` fails); `d1fca80` is.
- **Range `d1fca80..094602f`** (B262 clone): 10 commits, one per ticket, in queue order; 12 paths, +741 −62; head tree `5180070b0f31…`; merge-base `d1fca80`. Product code: `formGate.ts` (+22 −10) and `ImportEndpoints.cs` (+4 −1) only. Per-commit paths in the brief's PINS (`diff-tree --numstat`).
- **GitHub 13:53-13:54:** 0 check runs on `094602f`; 0 open PRs; 0 open code-scanning alerts; required checks exclude `api on SQL Server`. Records main `5d45352a4b32…` (#119), CLARIFICATIONS 1,422 lines, highest heading C-112 (`:1344`).
- **Jira GET 13:54:29:** -279, -276, -280, -274, -270, -272, -271, -278, -277, -273 and -275 all `Backlog`, 0 comments each.
- **Decision queue 13:54:16:** `hpsmpoc-hosted-runtime-10013-1017` OPEN; `require-sqlserver-ci-check-1006` ruled b, `steve-dbs-pdfs-cleared-for-ai-1016` ruled a (43 lines in `list ruled --undelivered hpsmpoc-`).
- **Machine 13:53:21:** load `2.62 5.80 7.67`; 8 cores; `lsof 6900-7399 LISTEN` = only `ControlCe *:7000`; 7150-7159 (and 7160-7199) rc 1; `.tools/.git-lock` absent; cockpit panes `tuesday`, `QA/NexusAI-gate25`, `Datasec/NexusAI-O`, `fleet-monitor`. The NexusAI gate brief names ports 5581, 5600 (grep). `715[0-9]` word hits in 15-18 Oct brief/STATUS/evidence files: 1, a data value in a B252 TSV, not a port (control `714[0-9]`: 13 files).
- **Toolchain (directory listing only):** `.tools/dotnet/sdk/10.0.401`, `shared/Microsoft.AspNetCore.App/10.0.12`; `.tools/node24`, `.tools/bicep` present. `.env`: 28 names, 0 `AGENTMAIL_API_KEY`.
- **Lineage sha256 (13:55-13:57):** `lock.sh` b250 = b259 = b262 (`d9df031b…`). **B262's `probe/rows.json`, `bffread.mjs`, `b252rows.mjs` are byte-equal to gate B259's** (`331cafd2…`, `5f97ca9f…`, `e63ecb6a…`): the shared-lineage fact behind the corpus requirement. B252 `rows.json` `93baa490…` (= B262's citation). `.tools/b255/mutate.py` `95da4670…` (= B262's copy). Others listed in the brief.
- **Code reads at `094602f`** (each `file:line` in the brief re-read): `formGate.ts` `:62-68`, `:74-77`, `:81-114`, `:120-125`, `:133-145`, `:149`, `:165-219`; `FeedbackFiles.cs:296-340`; `ImportEndpoints.cs:119-147`, `:190-200`, `:210`, `:248-268`, `:384`, `:425`; `ImportPendingSweep.cs:50` (`SqlServerRetries = 6`); `AssessmentModule.cs:101`, `:123`, `:176-184`; `FeedbackModule.cs:78-90`, `:146-154`; `HostedDemoRobustnessTests.cs:15-47`, `:61-104`, `:152-204`, `:230-241`; `ImportPendingSweepLoopTests.cs:1200`, `:1221`, `:1239`, `:1251`; `BoundedProcess.cs` whole; `BoundedProcessTests.cs` whole; `PkcsInPackageTests.cs:1-140`; `ci.yml:43`, `:180-181`, `:247`, `:250`, `:256-270`.

## Corrections to the commission and to the claims
1. **The 2-minute wait is used by THREE tests, not two:** 113a (`HostedDemoRobustnessTests.cs:160-161`), 113b (`:239-240`) and the new forced test (`:190-191`), all in one file; only the acquire command matches `IsAcquire` (`:66-67`). The brief asks the gate to prove the scope as measured.
2. **T-g, new and the strongest reading in this kit:** the wait is attached through `AddAssessmentInterceptors` (`:20-27`) to the ASSESSMENT context only, but the Feedback module also migrates at start-up (`FeedbackModule.cs:150-153`) on the same connection (`:84-85`), and EF's lock resource is the fixed `__EFMigrationsLock`. So the Feedback acquisition probably keeps EF's 30 s. This is UNMEASURED (I ran nothing). If it holds, -273's fix covers one of two lock waits.
3. **T4's input assertion is weak:** `forged > 1` (`ImportPendingSweepLoopTests.cs:1251`; round 1's T3 has the same at `:1200`). "Every retry" means 7 = 1 + `SqlServerRetries` (6). The brief makes the gate prove 7, 6 retry events, and a fail-fewer control that recovers.
4. **A pre-existing path the quadratic claim did not cover:** `fileByteCounter` re-scans an incomplete header block from its start on every chunk (`formGate.ts:207-211`). It is the same at `d1fca80`. The brief has the gate time it byte by byte, keep it apart from -276, and use a positive control (the builder's rejected prefix re-parse) so the instrument can show a quadratic.
5. **B262's .NET counts are without Blob:** "2,959 → 2,981 passed" is 22 Blob tests skipped at both commits (no Azurite). The names file's 2,981 → 3,003 includes them. Base 2,981 names equals B259's tip count, because `d1fca80`'s tree = `7fa59c5`'s (C-112 `:1349`). The gate runs with Azurite on.
6. **B262 put two scripts in its evidence** (`logs/api276.py`, `dnparse262-Program.cs`). B259's rule was "no scripts in evidence". The B262 brief did not say this, so it is not a defect. The brief bans running them.
7. **-276's line numbers moved:** the edited pinned row is `formMeter.test.ts:153` at tip (`:150` at `d1fca80`). Phase 2's catch is `ImportEndpoints.cs:139-140` at tip (`:137` at `d1fca80`).

## Traps put in the brief (beyond the commission)
- **T-a corpus:** the generated corpus (~5,000 lines, 14+ parameter atoms × 4 separators) is mandatory because the builder used the gate's own 30 rows. The prime bypass candidates: `name="feedback\"; name="files"` and `name="x\"; name="files"; filename="a.png"`. At tip the BFF reads a set first name that is not `files`, so these parts are uncounted; .NET's reading of them is unmeasured.
- **Own mutants:**
  - -276: m263-276a…d (`findLast`, `params.length === 0`, empty `stopped`, `headerParams` returning partial params).
  - -274: m263-274a…c (the type moved to the store catch, `throw;` instead of `StoreFailed`, `FailAsync` dropped).
- **T-j:** the gate checks -272's fixture end states against B255's own STATUS text, not against the builder's word.

## Decisions left for Tuesday (recommendation · default if unanswered)
1. **R-1, -276 on the wire** (standalone `npm run build` + raw socket). Recommendation: conditional on the load and not required for a GO. This is B259 ruling 2's logic: the Done-when is in-process, and the build is heavy under the < 6 rule. Default: conditional.
2. **R-2, Linux shell-level probe** in `b263-linuxsh`, made from the local mssql image (no pull, kept). Recommendation: run it if the load allows. It closes half of B262's "Linux for sleep&" gap, for pipe semantics only. Default: run if allowed, labelled shell-level only.
3. **R-3, -272 GO on fixtures.** Recommendation: accept, if each fixture state matches B255's 402 measurement. Real-mutant proof stays NOT TESTED until -269 (R-1 = b). Default: yes.
4. **R-4, -273's grading.**
   - Recommendation: grade on message 1, the cause the Done-when names.
   - Message 2 becomes a ticket candidate, or a -273 comment.
   - T-g is a finding against -273 if measured: Minor by my lean, the gate's call.
   - Default: as recommended.
5. **R-5, -271's token.** Recommendation: it grades the test clause only, and Jira gets a comment only. Default: yes.
6. **R-6, SQL Server shard 2.** Recommendation: run it at tip and base as mandatory, waiting for the load rather than skipping. B262 did not run it, and it holds T4, the Pkcs tests and the BoundedProcess tests. Shard 1 stays conditional. Default: yes.
7. **R-7, the last-line shape.** Recommendation: keep it as the commission gives it. Default: stands.

**Doubts:**
- I did not read `ShapeAnchorTests.cs`' new routines in full. -277's traps rest on B262's own counts plus B259's.
- The load window may not fit everything. With the < 6 rule and gate25's holds, Checks 2, 4 and 12 (shard 2 ×2) alone are several hours of heavy jobs. The brief orders the priorities.

## Launch
```
bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/HPSM-POC-G5 "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC' '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-18_B263_SEAT-G5_hpsmpoc-gate-b262.md'"
```
Before launch, Tuesday:
1. Reads the brief WHOLE.
2. Fills `## TUESDAY STAMP` (R-1…R-7).
3. Stamps the SELF-CHECK line.
4. Re-reads `ls-remote`, cockpit `status`, `lsof 7150-7159`, `.tools/.git-lock` and the load (below 6).
