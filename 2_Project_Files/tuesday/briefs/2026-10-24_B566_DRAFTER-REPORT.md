# B566 drafter report (gate kit for PR #105, SEAT-G73, tier 1, Opus, round 1 of 2)

Drafted 2026-10-24 08:07-08:15 AEDT, read-only. Files written: the brief and this report only (no `.pre-stamp` copy: Tuesday to make it before stamping). Nothing fetched, built, run or published; no gh, Jira, mail, decision-queue, Artifact or Docs call; no `cd`; git read verbs with `--no-optional-locks` only.

Brief (101 lines, long lines): `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B566_SEAT-G73_mps-105-gate-tier1.md`. Slot grep (`'_''_''_''_'`) = 9 lines (8 slots at lines 24-31 plus the last line 101); `@[A-Z_]+@` = 0; non-ASCII = 0. The brief runs about 100 lines but each is dense; it is longer in characters than the ~110-line target implies.

## Facts MEASURED (08:07-08:15, by `date`)
- `ls-remote`: main `a5b4bbb5...` (unmoved); `b561/mps-proposal-combined-usage-rate` = `refs/pull/105/head` = `4db8661dad27fd2e8d79e0731d998dd1c0f03362`; `refs/pull/105/merge` = `28899d9ebb554daa7f92606763fbd53b1b5165e8` (parents not read); #104 head `655606a9`, #102 head `27534990`; no `b566*`.
- `rev-list --left-right --count` = `0 6`; chain of 6 commits (`f034dec`, `dd23fe6`, `ae6d67d`, `3471588`, `bcbe2df`, `4db8661`); numstat 17 rows, sums **572 / 107** (matches the builder).
- `ci.yml` at head lines 42-43: `dotnet build MpsCalc.slnx -c Release`, `dotnet test MpsCalc.slnx -c Release --no-build`.
- NuGet: the path `.tools/b560/dotnet-home/.nuget/packages` exists; `grep -c -i nuget` = 0 in builder `ci.sh` and `dn.sh` and in the B561 STATUS (they only set PATH, DOTNET_ROOT, telemetry). Where the adapter path came from (an inherited HOME / DOTNET_CLI_HOME / NUGET_PACKAGES, or a shared launcher shell) is UNMEASURED; Tuesday's process-tree sighting is RELAYED, not re-measured.
- FOR TUESDAY leads: `docs/API.md:723-725` holds "(whole seconds, at least 1)"; `FeedbackStore.cs:459-472` `RetryAfterSeconds` returns `1` when `leave <= 0` else `Math.Max(1, ceil)` cast to int (reads consistent with the sentence; not probed). `docs/ENGINE.md:156` holds the X-31 sentence; other class-parse points exist (`InventoryEndpoints.cs:344`, `CatalogueOverlayStore.cs:498`, `SourceAdminEndpoints.cs:121`): the kit makes the gate census them. I made no verdict on either sentence.
- `sections.ts:385` `DEAL_WIDE_CLASS_CELL: string = ''`.
- Heavy slots: only `heavy-slot-1` exists, holder `B562 08:06:06 ci-merge-test` (live); `.tools/b566` absent.
- **Port block 9120-9129**: B562 holds 9110-9119, B560 8970-8979, B561 8980-8989; `ls | grep -c -E 'B56[3-5]'` in the briefs folder = 0 (control `B561` = 3); scan of `briefs/2026-10-2[34]_*.md` finds `91xx` tokens only in B562 (`9110`, `9110-9119`) and `9100` (end of a range); `lsof` on 9120-9129 empty (rc 1). A B563-B565 brief written after 08:14 is UNMEASURED; the kit tells the seat to re-scan.

## Shape decisions
Cloned B562 (REFUSE block, 8 stamp slots + last line, Opus/G1, BRIEF_SEAT_LEVEL, atomic heavy-slot mkdir with release-by-move, load < 7, RESUME, verdict line formats, round-cap statement). Rebuilt: eight questions, GRADING (G-1 money/proposal differential as Blocker, G-2 mutants, G-3 test validity with 12 lost / 36 added, G-4 words/docs, G-9 contract), checks C1-C11. The five MUST-CHECKs sit in their own section and are bound to checks: (1) NuGet -> C7 (first heavy job, seat-local home `.tools/b566/dotnet-home`, never the b560 path as source), (2) words -> C7b/C5 (own tokenizer + rendered-string table by program, base vs head), (3) the two sentences -> C2 (TRUE/FALSE/PARTLY with code lines, probes), (4) commit order -> C1 (six-commit build/test table, expecting `3471588` alone to fail `tsc -b`), (5) CI -> C9 (explicit PENDING set at every poll, gh GET under the project config). Standing HOLDS lines are verbatim.

## Judgement calls for Tuesday at the stamp
1. **Hard stop**: suggested 2.5 h target / 3.5 h hard stop (about 14 server + 9 web + 4 contract mutants beyond 15 to reproduce, a 1,500-deal differential at two trees, six per-commit builds, web line). Change if you want slack.
2. **Q-1** (scratch rows, source edits, fixtures in `.tools/b566/`): needed for C3-C7; answer in the "Stamped by" slot.
3. **Heavy slot**: slot 1 is held by the B562 gate (live). The B566 gate will queue behind it; consider launching after B562's verdict, or accept the wait.
4. **No `.pre-stamp` copy** was written (the instruction listed two files only): make it before stamping so the refuse check has its control (9).
5. **PR #105 now exists** (`refs/pull/105/*` present); the builder STATUS says "no PR yet". Check-runs, merge-ref parents and alert state were NOT read (no gh): the kit makes them the seat's.
6. **Option B vs A3**: the kit grades the built empty cell and treats A1/A2/A3 as pending the product owner's words; it never judges wording.
7. **Correction 2 (`deviceClass` optional-and-nullable vs kept in `required`)**: the kit lists it as a FACT for Tuesday, graded Major only if contract and generated client disagree (G-9).
8. **#102 build combination** (`wt-102`) is optional ("if time allows"); merge-tree markers are required.
9. The mail line is cloned from B562 (question mail only if the key NAME is set).

## UNMEASURED
All builder runtime claims; the new test files, `Proposal.cs`, web components, `Contract.cs`, the B535 gate STATUS and the Jira tickets (not read by the drafter); check-runs and alerts on PR #105; merge-ref parents; where the NuGet path came from; any B563-B565 port claims made after 08:14; whether #104 has landed since 08:07.
