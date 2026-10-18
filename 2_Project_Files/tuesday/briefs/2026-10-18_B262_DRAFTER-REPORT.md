# DRAFTER REPORT: HPSM-POC B262 (build round 2 of 2), 2026-10-18 12:13-12:2x AEDT

I am a read-only drafter for Tuesday. I launched nothing and sent nothing. I made no Jira, git or gh writes and no fetch. I ran no `az`, docker, dotnet or npm, and sent no HTTP to any app host, the hosted site or production. Jira and GitHub were read by GET only. Jira went through `.tools/b257/jira.py` and `search.py`, run in place with `python3 -B`; credentials were read by name in-process and never printed. GitHub went through `gh api` under the project's `.gh-config`. My only writes are these two files.

## 1. Files
- **Brief:** `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-18_B262_SEAT-H4_hpsmpoc-round2.md`. Its Step 0 copies it into the project's `Briefs/`. It ends with an empty `## TUESDAY STAMP` for R-1…R-7 below.
- **STATUS:** `/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-10-18_B262_STATUS.md`. Its last line is `READY FOR GATE: b262/round2-pkcs-bff-imports-tests @ <sha40>`, or `STOPPED: NEEDS TUESDAY` + ONE question. **Arm the STATUS watcher on that path.**
- **Number:** B262 is free. `ls` of both brief folders at 12:19 found no B262…B269. The highest is B261.
- **Launch:** `bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/HPSM-POC-H4 "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC' '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-18_B262_SEAT-H4_hpsmpoc-round2.md'"`

## 2. What I read
- B258 brief and its drafter report, read whole.
- B259 STATUS (188 lines), read whole.
- B260 STATUS (384 lines), read whole.
- B261 brief (259 lines), read whole.
- B258 STATUS `:1-60`, and B259 brief `:150-158` (the stamp).
- Jira GET, 12:14 (all Backlog, 0 comments on every one):
  - HPSMPOC-263, -269, -270, -271, -272, -273;
  - HPSMPOC-274…280.
- Code at `d1fca80`, by `git show`:
  - `PkcsInPackageTests.cs` (whole);
  - `ci.yml` `:46-48`, `:86-140`, `:185-187`;
  - `global.json`; the csproj pin `:30`;
  - `HostedDemoRobustnessTests.cs` `:1-130`;
  - `ImportFileStoredHashMigrationTests.cs` (greps);
  - `TestDatabase.cs` and `SharedDatabase.cs` (greps);
  - `AssessmentModule.cs` `:115-130`, `:170-200`;
  - `ImportEndpoints.cs` `:60-270`, `:381-386`;
  - `ImportPendingSweep.cs` `:95-140`, `:178-186`;
  - `formGate.ts` `:80-140`; `guard.ts` `:1-60`;
  - `ShapeAnchorTests.cs` `:170-250`;
  - `deploy-package.py` `:440-475`;
  - test greps in `test_deploy_hpsmpoc208.py`, `formMeter.test.ts`, `bff.formstream.test.ts`, `bff.attachments.test.ts` and `ImportPendingSweepLoopTests.cs`.
- Tuesday's `decisions.json`, read-only.

## 3. Verified pointers (MEASURED, 12:13-12:21 AEDT)
- **Repos and checks:**
  - Code main is `d1fca809e28b283b29a54d02816efcc6409b5b67` (`ls-remote` 12:13:57), one squash commit over `787d159`. There is no `b262*` branch.
  - Check runs on `d1fca80`: 18 success + 1 skipped. 0 open PRs, 0 open alerts.
  - Records main is `2e284455` (`gh api`, 12:16). `records/b261` is not on origin yet.
- **`api on SQL Server` is NOT a required check** (`required_status_checks` contexts, 12:16). This answers B258's UNMEASURED line. Kam's ruling b of 6 Oct is still not applied, which is Kam's setting.
- **B261's tickets are already in Jira:** JQL `created >= "2026-10-18"` → 7 (HPSMPOC-274…280, created 12:11), all Backlog, 0 comments. The mapping:

| Key | B261 row | Origin |
|---|---|---|
| -274 | G01 | F-4 |
| -275 | G02 | F-3 |
| -276 | G03 | B259-1 |
| -277 | G04 | B259-2 + B259-3 |
| -278 | G05 | B259-4 |
| -279 | G06 | B259-5 |
| -280 | G07 | B259-6 |

  B261's STATUS was not yet written at 12:21.
- **Every round-2 cite holds at `d1fca80`, with one correction:**
  - These all hold: `PkcsInPackageTests.cs:18-22`, `:43`, `:45`, `:66`, `:71`, `:76`; `ci.yml:86/:125/:136`; csproj `:30`; `HostedDemoRobustnessTests.cs:46`, `:79`; `AssessmentModule.cs:183`, `:123`; `ImportEndpoints.cs:135/:137`, `:191-195`, `:245-265`; `formGate.ts:93`, `:130`; `ShapeAnchorTests.cs:177-184`, `:243`; `deploy-package.py:463`.
  - **The correction:** in `guard.ts`, `declared` is at `:40` and is used at `:41`. The gate's `:41-42` is off by one, and -280's own Where already says `:40-41`.
- **Local SDK** (directory listing only; no `dotnet` was run):
  - SDK 10.0.401 with runtimes 10.0.12.
  - `PlatformManifest.txt:42` reads Pkcs `10.0.1226.42308`, below the pin's `10.0.1326.50504`.
  - So -269's claim, which B255 relayed, is now MEASURED.
- **Prior work:**
  - No commit names -263 or -269…-280.
  - `-S PlatformManifest` → 0, and `-S __EFMigrationsLock` → 0.
  - The serialise precedent is `ImportsAloneCollection.cs:17` (B230).
  - The 1205 forge precedent is `ImportPendingSweepLoopTests.cs:1158/:1184`.
  - No process-runner helper exists in `api/tests`.
- **Environment:**
  - Ports 6980-6989 are free (`lsof` rc 1, 12:19). Load is 2.87 on 8 cores.
  - Live panes: `tuesday`, `QA/NexusAI-gate25`, `Datasec/HPSM-POC-R4`, `Datasec/NexusAI-O`, `fleet-monitor`.
  - `AGENTMAIL_API_KEY` lines in `.env`: 0.

## 4. Doubts (each one is in the brief where it applies)
1. **-276 against round 1's own pinned row (MEASURED, 12:21).**
   - `formMeter.test.ts:150` asserts that `name="feedback"; filename="a` (an unclosed quote) is counted "whatever the name".
   - The gate's shape (b) would count it 0.
   - The brief lets the seat change that row only after measuring that the API refuses the form, and only if it states this as an edited pre-existing test. Otherwise the row stays counted.
   - The gate will check that ruling. Strike it at stamp if you want the row frozen.
2. **-276 and -279 share `headerParams`.** -279 pins the escape step, so it goes first. If -276 takes the gate's shape (a), the .NET end-of-line rule, it edits the step -279 just pinned.
3. **-271's early-warning test turns red on the same SDK as the existing guard.**
   - Both fire when the framework's Pkcs is above the pin.
   - Its gain is a named version in the message, and no publish is needed. It gives no earlier warning in time (R-4).
   - No SDK above the pin exists, so its red can be proven only with a fixture manifest line. The brief says so.
4. **-275's Done-when cannot be met as worded (R-3).**
   - With a 1205 forged on every attempt at FailAsync's first delete, the rows cannot be removed.
   - FailAsync's own doc (`ImportEndpoints.cs:243-244`) says *"A failure here leaves the run `pending` … never an orphan"*. So today's end state is the designed fallback.
5. **-273's likely cause is my inference, UNMEASURED.** In the concurrent-start test two hosts migrate one database, and the waiter's lock call runs on the 30 s default timeout.
   - That fits "Execution Timeout Expired" at 36 s.
   - It does not explain the second message ("release … not currently held"), which comes from a test on its own database.
   - The brief requires the cause to be measured first, with a forced red, and the fix to be tests-only.
6. **Size.** If R-2 is taken as recommended, the round has 10 commits, against B258's 6.
   - B258 ran from its 06:48 Step 0 to its 07:58:12 push (B258 STATUS `:20`, `:207`).
   - -273 is last and droppable. The SQL Server legs are heavy, and `QA/NexusAI-gate25` (tier 1) outranks this seat on CPU.
7. **The commission said B261 owns `1_Project_Definition`.** Every build seat's brief copy, STATUS and evidence live in `1_Project_Definition/Briefs/`. The brief allows ONLY B262's own new files there. The project root is the records repo, so the brief also forbids every git verb on it (R-6).

## 5. Open rulings for Tuesday (each with my recommendation and a default; nothing here is decided)

**R-1 · HPSMPOC-269, the shared `.tools/dotnet` swap (Tuesday's ruling, not Kam's: no words, no hosted effect).**
- (a) **Inside B262 as Step 0.**
  - The seat downloads SDK ≥ 10.0.402 / runtime ≥ 10.0.13 from Microsoft's official install source. It checks the published checksum and quarantines the old tree as the way back.
  - Every round-2 base and tip measurement then runs on the new SDK. m1 (the tie) becomes provable for -272.
  - Costs: it mixes a shared-tool change into a code round; gate B263 must use the same SDK; and the build seat makes a network download.
- (b) **A separate small tooling seat after B262's gate,** before the next HPSM-POC build.
  - One SDK holds through B262's build and gate. -269 closes on its own evidence (m1 red on the new SDK).
- (c) **Defer** until the runtime card is ruled.
- **Recommendation: (b).** B262's acceptance does not need the tie SDK: -272's tie branch and -271's red are both shown with a fixture manifest. Keeping one SDK across the build and its gate keeps base vs tip comparable.
- **Default (no ruling): B262 does not touch `.tools/dotnet`.** That is (b) or (c) for this seat; the brief already says so. The seat reports in NOT TESTED which B255 mutants could not be shown on 10.0.401.

**R-2 · B261's tickets in round 2.**

| Ticket | Recommendation | Why |
|---|---|---|
| -279 (G06) | IN, item 1 | tests only; pins what -276 may touch |
| -276 (G03) | IN, item 2, **tier 1** | Minor, browser-sendable over-refusal; same file as round 1 |
| -280 (G07) | IN, item 3 | tests only |
| -274 (G01) | IN, item 4, **tier 1** | one catch type, the exact sibling of -262; no new words |
| -278 (G05) | IN, item 8 | tests only |
| -277 (G04) | IN, item 9 | tests only |
| -275 (G02) | **OUT** | see R-3 |

**Default: as recommended** (the brief marks each [R-2]; a struck item is skipped). If you want the round smaller, strike -276 first. It is the only one that changes product behaviour and needs the B259 differential rig at the gate.

**R-3 · HPSMPOC-275 (FailAsync unguarded).**
- (a) **Reword the Done-when to something buildable.** For example: "when FailAsync itself fails, the upload answers the product's problem instead of the generic 500, and the run stays pending for the sweep, as `:243-244` designs". The only existing answer (`RowsNotSaved`) says *"recorded as failed"*, which would be false for a pending run, so (a) needs new words for Kam alongside -267.
- (b) **Hold it as by-design** (`:243-244`) under `before-imports-on-hosted`, and decide it with -267 before imports go on.
- (c) **Leave it as filed.** It cannot be built as worded.
- **Recommendation: (b).**
- **Default: not in round 2, and the ticket stays open (b's effect).** A records comment can say why.

**R-4 · -271's early-warning test.**
- Either build it, sharing -272's manifest reader, or drop it.
- **Recommendation: build.** It is cheap with -272's reader, and it names the version to raise to.
- **Default: build (item 7).** -271 then gets a "comment only" line, because its owner/cadence clause stays open.

**R-5 · HPSMPOC-263: Kam card text (draft; not filed).** B258's drafter thought this was Tuesday's to rule (no words, imports off). The pickup says it is a Kam card. The text below is for Kam if you file it.
> **Tap a, b or c.** Imports are switched off on the hosted demo, so nothing changes for anyone today. This is about a rare race inside an upload. While an upload is still storing its files, the hourly clean-up can give up on it and mark it failed. The upload then stores its remaining files anyway. The clean-up's internal log line ("1 of 3 named files are in the store") is then out of date. The end result is otherwise correct: the upload is failed, no rows are kept, and one failure record is written. Only that internal count is stale.
> - **a) Stop storing.** Once the upload has been marked failed, it stores nothing more. This adds one extra database check per file. The uploader then gets the existing "could not be saved" answer, which is among the import words you have not approved yet (HPSMPOC-267).
> - **b) Fix the log only.** The log line says it counts the files at the moment of failing. It is an internal message, so no customer words change.
> - **c) No change now.** Record it as known, and decide it with the other import questions before imports are switched on.
>
> **Recommendation: c.** a only matters once imports are on, and it brings in the import words you have not yet approved, so it is best decided with them. **Default if you don't tap: c.**

**R-6 · B262's files under `1_Project_Definition/`.**
- **Recommendation and default: as the brief says.** B262 may write only its own `2026-10-18_B262_*` files in `Briefs/`, and runs no git verb on the project root, which is the records checkout.
- Strike this if you want B262's STATUS elsewhere.

**R-7 · -273's fix scope.**
- **Recommendation and default:** fix in the tests only, with the cause measured first. A product (`AssessmentModule.cs:183`), CI or setting change means STOP. -273 is last and the first to drop.

## 6. For Tuesday (not in the brief's scope)
- **B261's tickets cite the gate's `guard.ts:41-42`;** -280 already corrects it to `:40-41`. Nothing to do.
- **R-2 changes the scope of B263, round 2's gate.** If -276 rides, the gate needs B259's 1a/1c Content-Disposition rig. Its kit is in `.tools/b259/` and its evidence is in `Briefs/2026-10-18_B259_evidence/`.
- **Records owed after B262:** a "comment only" for -271; Done for the others if they are met. -275 and -263 follow R-3 and R-5.
