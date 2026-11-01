STARTABLE: YES

# B1051 DRAFTER REPORT - SEAT-G260 tier-1 QA gate of B1043 (MPSCALC-256 purchase recurring projection, engine half)

Drafted 2026-11-01 14:49-15:00 AEDT by a read-only drafter. Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1051_SEAT-G260_mps-256-purchase-projection-gate-tier1.md` (32 lines, 60 KB; 8 four-underscore lines = 7 stamp slots + the last line).

## BLUF
- A tier-1 gate kit (G1, `model-routing.md:108`, Opus; G-cap `:111`) for branch `b1043/mps-256-purchase-recurring-projection` @ `63ab55a882729ad0024e68929afa22a99cd2e2a0` on main `5c64a44226614523031a7b2d67cb9bfb477a380e`. **Round 1 of 2 on class "V4 engine: purchase recurring projection", NO GO 0 before** (census below). Seat `Datasec/MPS-G260`. Ports: none (fallback block 9650-9659, free).
- Shape copied from the B1020 kit (the -255 gate): step 1 BYTE-EQUAL rebuilt (3 serializers, stripped compare on exactly `purchase.projection`, by-path not by substring), step 2 own hand cases, step 3 reconciler and a 500+ quote sweep, step 4 own mutants GP1-GP16, step 5 delta / X-39 / commit message, step 6 local CI and the four squash files, step 7 merge and LANDING CHECKLIST.
- New in this kit, and why:
  - Step 1(f) PERSISTENCE: the Api CAN state supplies models (`PurchaseMapping.cs:37-41`), and `QuoteFileStore` persists the ENGINE `CalculationResult` under `ReferenceStore.JsonOptions` (`QuoteFileStore.cs:122`). So once this lands, a stored source-bearing purchase quote carries `projection`. The builder recorded that as a fact. The kit makes the gate measure: a rollback read (main's binary reading a head-written file; the store options set no `UnmappedMemberHandling`, so it should skip the key), whether any DTO or ApiJson-Disallow reader reaches an engine result, and whether any Api/Import test pins stored bytes.
  - Step 2(p) NULL-CPP: the new code does `c.MonoCpp!.Value` on `decimal?`. If any path sets `Supplies` without the CPPs, a quote that priced at main now throws. The gate proves this from `ClicksOf`/`DealUsageOf`. A throw is a Blocker.
  - Step 4 targets the four shapes B1020-6 found alive behind the -255 builder's rows: N 1 (GP1/GP2), decimals beyond cents (GP3/GP4), stated zero (GP5), zero check (GP6/GP7). It adds GP8/GP9 (digit-only contract differences the builder measured: 9/571 and 83/600) and GP16 (= the builder's MP16, re-run).
  - Step 5(b) points the gate at the X-39 sentence "the Api cannot state a fee, so a quote made through the Api today shows 0 managed-service cost and service revenue". Nothing shows the projection, and an Api quote with a supplies model stores one with zero fee measures. The gate grades it TRUE / SHORT / FALSE (Q-3).
  - B1020-7 is carried: ApiJson `WhenWritingNull` hides a removed `JsonIgnore`, so by-path absence must be shown under the InputHash and store options.

## Facts re-measured (instrument; control)
- Remote (`gh api -X GET`, project `GH_CONFIG_DIR`, project account active, ssh) 14:49:43:
  - main `5c64a442...`.
  - `matching-refs/heads/b1043` = 1 ref, `63ab55a...` (control `heads/b10` 60).
  - compare `5c64a442...63ab55a`: ahead 1, behind 0, 7 files: ENGINE.md +2 -1, PurchaseCalculator.cs +38 -1, CalculationResult.cs +1 -1, PurchaseResult.cs +7 -0, ManagedServiceFeeTests.cs +1 -1, PurchaseRecurringProjectionTests.cs +287 -0 added, RecurringProjectionTests.cs +4 -3. This equals Tuesday's 14:48 read.
  - Parent `5c64a442` only; `verification.verified` false.
  - Open PRs 121 and 120 (dependabot); PRs for the branch 0; `actions/runs?head_sha` total 0.
  - Squash settings COMMIT_OR_PR_TITLE / COMMIT_MESSAGES; allow_squash true.
- Commit message read whole: 9 body sentences by a full-stop-capital split, one trailer `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- Local `git --no-optional-locks` in `2_Project_Files`: both commits present (`cat-file -t` commit).
  - The diff was read whole except the new test file. Its 12 `X39_*` method names were listed.
  - `ci.yml` blob `212b0da1...` at both. `X-39` at `docs/ENGINE.md:165` at head, 0 at main (control X-38 1).
  - `PurchaseResultOf(` 3 calls + the definition. Only `:255` (priced) sets Projection.
  - Fee sums `:217-221` keyed on the section `MonthlyManagedServiceCost`.
- Persistence reads at head:
  - `CalculationRecord.Result` is the engine `CalculationResult` (`QuoteStore.cs:23-26`). `PersistedQuote` (`QuoteFileStore.cs:79`) is stored with `ReferenceStore.JsonOptions` (`:122`).
  - `ReferenceStore.JsonOptions` (`ReferenceStore.cs:14-19`) has no UnmappedMemberHandling. `ApiJson.cs:23-24` has Disallow + WhenWritingNull.
  - `SnapshotDto` is a DTO (`Dtos.cs:373`). Api readers under ApiJson deserialize `SnapshotDto` only (5 sites).
  - `WhatChanged` is field-based (`Mapping.cs:391`). `PriceAudit.SameDraft` compares drafts, not results.
  - `git grep -w Projection` over `src/MpsCalc.Api`, the Api tests and the Import tests printed nothing. This is NOT a controlled zero: I ran no positive control in that frame (UNMEASURED; the kit makes the gate re-run it with one).
- Round census: a bash loop over `Briefs/*_STATUS.md` first lines starting `GATE VERDICT` found 69. Hits on `purchase recurring projection|b1043|63ab55a`: 0. Controls on the same lines: `rental projection` 2, `managed-service fee` 1.
- Seat and number:
  - `G260`: 0 names, 0 contents in `tuesday/briefs` (control G259: 3 files). `B1051`: 0 (control B1050: 4 names). Project Briefs `B1051|G260`: 0 (control B1043: 2).
  - Panes 14:50: tuesday, NexusAI-G259, HPSM-POC-D44, HPSM-POC-H92, NexusAI-M62, fleet-monitor. No MPS pane; M61 closed.
  - `.tools` has no `b1051`, `heavy-slot-*` or `.git-lock` (control: `b1043`, `wt-b1043-*` listed).
- Ports: `lsof -nP -iTCP:9650-9669 -sTCP:LISTEN` 0 rows (control: unrestricted 26). `-w -E '965[0-9]'` over 82 non-`.pre-` SEAT kits of 10-31 and 11-01: 0 files (controls `964[0-9]` 2, `962[0-9]` 2, `948[0-9]` 5).
- Model: `models_latest.json:17` `levels.opus.model_id` = `claude-opus-5-5` (what `brief_seat.sh` reads; `:37` the same id under `previous`; checked_at 13:27:30). `brief_seat.sh` defaults to opus; the launch line carries `BRIEF_SEAT_LEVEL=opus`.
- Load: `LC_ALL=C uptime` load1 3.72 at 14:51.
- Kit hygiene:
  - 4-underscore lines 8 (control B1020 pre-stamp 8).
  - Non-ASCII bytes 0 (python byte count; control file 2).
  - Person-name tokens 0 (control planted 1).
  - Card-id patterns: 2 hits, both rule text ("decision-card id").

## D-decisions (override at the stamp)
- D1: G1 Opus, tier 1, round 1 of 2, NO GO 0 before.
- D2: Clone + one in-clone fetch (the B1020 method). The local code repo already holds both commits, but the gate never touches it beyond the clone source.
- D3: Fallback port block 9650-9659.
- D4: Mutant ids `GP1-GP16`, findings `B1051-n`, evidence `2026-11-01_B1051_evidence/`, TMPDIR `/private/tmp/b1051-seat-tmp`.
- D5: Sweep formula (ii) reads pages, k, applied clicks and fee from the INPUT. CPPs and contract figures come from pre-existing members that step (i) proved byte-equal. A fully input-derived CPP model would re-implement the supplies resolver; the hand cases derive CPPs by hand instead.
- D6: Severity for the stored-document change (Q-2 default).
- D7: Clocks: target 3 h, hard stop 5 h after Step 0.
- D8: `src/MpsCalc.Api/Quotes/**` is added to the "main moved forces a re-run" list (step 1(f) reads it).

## Q-questions for Tuesday (each with a default)
- Q-1 Gate row, tier and round: default G1 Opus, tier 1, round 1 of 2 on "V4 engine: purchase recurring projection", NO GO 0 before.
- Q-2 Stored quote files of source-bearing purchase calculations gain `projection`. Default grading:
  - Note, if main's binary reads a head-written file under the store options, and no DTO or ApiJson reader carries the key.
  - Minor, if X-39 or the commit claims stored bytes unchanged for a source-bearing quote.
  - Blocker, if the rollback read fails.
  - Major, if a production ApiJson-Disallow reader reads an engine result.
- Q-3 X-39 "the Api ... today shows 0 managed-service cost and service revenue": default is for the gate to grade it on evidence. SHORT = Note; FALSE = Major. Its result would be a register-text fix in a round-2 commit.
- Q-4 MPSCALC-256 may appear in the PR title and squash subject (they say ENGINE HALF and purchase), not in either body. Default yes (as B1020's Q-4).
- Q-5 Full CI at head; main gets `--list-tests` and the Release build; a full main run only on a red at head. Default yes.
- Q-6 Clocks: default target 3 h, hard stop 5 h after Step 0.
- Q-7 Done-when: default is for the gate to grade the four acceptance clauses and write both records sentences; Tuesday chooses.
- Q-8 Sweep (ii) may read CPPs and contract figures from pre-existing members proved byte-equal (D5): default yes.

## UNMEASURED
- No build, test, harness, sweep or mutant was run.
- The new test file was not read beyond its method names.
- Not measured:
  - whether any path sets `Supplies` without CPPs (step 2(p));
  - whether main's binary actually reads a head-written `PersistedQuote` (step 1(f)(iii));
  - whether any `*.json` fixture under `tests/` holds a stored purchase quote;
  - the zero-device supplies model's validation;
  - whether GP8/GP9 are row-killable.
- The `Projection` zero in the Api/Import frame has no positive control (stated above).
- Root `git status` of the project was not read.
- The CLARIFICATIONS line quotes (:758, :774, :1774, :1907) are RELAYED from the B1043 and B1020 kits, not re-read.

## Outside-the-fences disclosure
- Wrote only the two files above, plus one 3-byte control file `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/f8947a38-04ac-46b8-96f3-ceebf0948b77/scratchpad/ctl.txt` in my session scratchpad (a non-ASCII counter control). It is not a project file. Disclosed because the rules say "write only those two files".
- No `decision_queue.sh`, no Jira call, no `cd`.
- Git verbs used: cat-file, diff, grep and show (`--no-optional-locks`), and rev-parse.
- `gh` was `-X GET` only. No HTTP to any app host. No az, ssh or docker.
- Read the WEDNESDAY-tree file `model-routing.md` and `models_latest.json`, as the rules direct. Read nothing else outside Datasec.
- One advisory hook fired on three case-sensitive greps (a test-name list, the B988 findings list, the routing rows). Each result was positive and cross-checked by another read, so no zero rests on them.
