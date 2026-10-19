# B304 drafter report (2026-10-20 ~09:15 AEDT)

Brief: `2026-10-20_B304_SEAT-G12_hpsmpoc-gate-pr164-tier2.md` (round 1 of 2 under the cap, tier 2, Sonnet, pane `Datasec/HPSM-POC-G12`, port block 7340-7349) for PR #164 @ 8c029bbc (HPSMPOC-298, -299, -300). Shape copied from B291 (standing lines, REFUSE, pins, claims/traps, checks r0-r11, verdict vocabulary, findings format, last line, Jira line shape). The six questions come first, "Not filed" is r8.

## What I read
Whole: B300 STATUS, B300 builder brief, B291 gate brief, B291 drafter report, B291 STATUS (`:1-5`, `:325-392` in full; grep of the probe/mutant sections). Code at the head by `git show`/`diff` (read verbs): the whole product diff `b3a7c27..8c029bb`, `FailAsync`/`FailOnceAsync`/`FailIfStillPendingAsync` (`ImportEndpoints.cs:283-365`), phase-3 completion (`:195-215`), the writers of `"failed"` and `StatusReason`. Not opened: any `.tools/b2*`, `.tools/b300`, `.tools/b291`, the B300 evidence folder (listed by `ls` only), `.env`, `3_Access_Keys`, HP docs.

## Measurements (09:01-09:1x AEDT, read verbs only)
- `git --no-optional-locks -C .../2_Project_Files ls-remote origin refs/heads/main refs/heads/b300/import-failure-path-298-299-300 refs/pull/164/head`: main `b3a7c275...`, branch and PR head `8c029bbc6df8f2a2808e592969a8c00e0b21064e`.
- `git merge-base b3a7c27 8c029bb` = `b3a7c27` (the PR is a clean 3-commit stack on main). `cat-file -t` of both = commit (the objects are already local).
- `gh api repos/datasecau/HPSM-POC/pulls/164` (GH_CONFIG_DIR set): open, **draft false**, commits 3, changed files 6, +695/-9. `pulls/164/files`: ImportEndpoints.cs +29/-3, ImportPendingSweep.cs +30/-1, ImportFailPathTests.cs +63/-0, ImportFailurePathResidualTests.cs +268, ImportSweepCountTests.cs +259, ImportUtf7Tests.cs +46/-5. `gh pr list --state open`: only #164.
- `gh api .../commits/8c029bb.../check-runs`: `CodeQL` completed **neutral** (to be explained by the gate); gitleaks and dependency review success; `api`, both SQL Server shards, web unit, web build, infra, four `Analyze` jobs in progress. So question 5 is pending at drafting.
- `lsof -nP -iTCP:7340-7349 -sTCP:LISTEN`: 0 lines. `uptime` 09:01: load 8.98 8.08 7.71 (over the line). `date` 09:01:13 AEDT.
- `git diff b3a7c27 8c029bb -- api/src`: the product change is exactly what the builder describes; `PolicySeconds = 403_600` (about 112 h) at `ImportPendingSweep.cs:36`; `DatabaseRefusedReason` is used at `ImportEndpoints.cs:145` and `:172`; fresh scope per `FailOnceAsync` attempt (`:315-316`); the 5 removed lines in `ImportUtf7Tests.cs` are the `Body`/`PostAsync` helper lines.

## Things I found while drafting (folded into the brief as traps)
1. The guard `run.Status == "failed" && run.StatusReason == reason` depends on a fresh scope per attempt, on every `failed`+same-reason writer sharing a transaction with its audit, and on the reason round-tripping the 500-char column. r2 makes the gate test each (the phase-3 completion at `:207` writes `failed` with a null reason and an `import.created` audit, which the guard cannot match).
2. `LandedSinceAsync` swallows every exception class except while the token is cancelled, including programming errors; on a cancelled token the exception escapes after the run is committed failed, so no 3304 and a short pass count. r3 asks for the class table, the host-stop comparison against base, and the 3304-under-3309 judgement.
3. The "Not filed" double audit has a variant that is NEW at the head: the new 3308 path (status read fails) after the sweep has failed the run also goes to `FailAsync` with a different reason. r8 drives three variants base vs head with a decision rule (new at head = Minor finding; same at base = Note; not a NO GO by itself).
4. The new tests' SQL Server branches could pass vacuously if a forge matched nothing; r5 has the gate read that each test asserts its inputs, as well as quote the shards.

## Slots
None. Zero stamp slots (the B291 slots were stamp time, port block, B-number; all three are known now: B304, 7340-7349 lsof-measured, launch time goes in Tuesday's launch tap). The REFUSE slot-count line is therefore dropped.

## Judgement calls for Tuesday (numbered, with my recommendation)
1. **PR is not a draft** (`draft false`). B291's brief said "open, draft". I wrote the REFUSE row as "not `open`". Recommend: no action.
2. **CodeQL is `neutral` right now**, with the four Analyze jobs still running. I told the gate to treat pending as pending and explain the neutral check; recommend Tuesday re-reads before launch and, if all checks are still running, launches anyway (the gate's r5 is conditional on CI by design).
3. **Load is 8.98 (over 8)**; the brief's priority order puts r1, r2, r3, r5, r8 first, and lists MPS B303 %104, NexusAI B302 %105 and S101O %56 as NOT yours (and a possible Composer seat, per the commission). Recommend launching when load1 is below 8, or accept that the seat will queue on the 20 s poll; the gate does not race.
4. **The gate may not open the previous gate's probe files** (`.tools/b291`, `.tools/wt-b291-*` are another seat's `.tools/b2*`). I made it rebuild R3, G1, S2, mwhole, mwide from the B291 STATUS text. Recommend: keep; if Tuesday wants the old probes reused, say so in the launch tap.
5. **The "Not filed" assessment is delegated to a decision rule inside the brief** (r8) rather than decided by me. My own read, unmeasured: it is a pre-existing property of `FailAsync` at base for the StoredAt and store-refused sites (a Note), and variant (ii) via 3308 is new at the head (a Minor at most), reachable only with an upload alive past about 112 h. Recommend: not a NO GO, not a reason to hold the merge.
6. Unverified by me: the `ImportUtf7Tests.cs` removed lines are classified from the diff only (no run); the B300 evidence folder was listed, not read.
7. The brief is long (about 28 KB, B291 style). Heavy rows r1, r3, r6, r7, r8 under load 8-9 will take a while.

No git write verb, no dotnet, no Jira, no az, no HTTP to any hosted site, no Artifact/Docs/mail/chat was used. Files written: the brief and this report only.
