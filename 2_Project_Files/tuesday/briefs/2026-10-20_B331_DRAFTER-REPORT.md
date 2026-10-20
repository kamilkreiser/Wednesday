# B331 DRAFTER REPORT · SEAT-G20 · Composer gate PR #83 (tier 1, round 1 of 2)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-20_B331_SEAT-G20_composer-gate-pr83-tier1.md` (97 lines, 1 slot `STAMP_TIME`, last line `READ-WHOLE-BY-TUESDAY: PENDING`). Drafted 2026-10-20 14:10-14:16 AEDT. Read verbs and `gh api` GETs only; nothing run, built, fetched or pushed; no `.tools/b322/*` script run.

## Measured facts (clock `date` 14:10:58-14:16:10)
- **Pins (ls-remote 14:11:04):** main `d8d2a2c74a909d508dbc593d5429ac0af1a484bb`; `b322/exception-review-date-device-scope` = `refs/pull/83/head` = `314f40d989c9a9515bbba0dfb636b5c81f41a428`; `refs/pull/82/head` `e6288983…`; `b331*` none. Ahead 2 / behind 0. Both objects are in `2_Project_Files` (`cat-file -t` commit).
- **PR #83 (gh GET 14:11):** open, **draft**, base main `d8d2a2c7`, 2 commits, 17 files, +2001/-41, mergeable true, `mergeable_state` blocked. Numstat agrees (2001 / 41 / 17).
- **Open PRs:** #83 and #82 only. #82 touches 2 test files; **0 shared paths** with #83.
- **CI / CodeQL (14:11:16):** `Analyze (javascript-typescript)` and `Analyze (csharp)` in_progress; combined status pending (0 contexts); **0 analyses on refs/pull/83/head (not scanned yet)**; open alerts on the PR ref 0; control: main fixed = 20, main open = 0.
- **Migrations at d8d2a2c7:** newest `0021_policy_target.sql` and `0021_policy_target.down.sql`.
- **Client-name grep (not proof):** added lines `sro[-_ ]?vic|victoria` = 0; commit messages `sro[-_ ]?vic|paul|hp ` = 0; positive control on the same added lines (`exception_record`) = 55. The gate does its own grep with a planted control.
- **Model row:** G1, tier 1 (`fleet/specs/model-routing.md:108`). `BRIEF_SEAT_PRINT_MODEL=1 bash brief_seat.sh …` printed `model=claude-opus-5-5 (level opus)`. Launch without `BRIEF_SEAT_LEVEL`, with `WED_USAGE_STOP=100`.
- **Port block 7520-7529:** `lsof` rc 1 for 7490-7549 in 10-blocks. Today's briefs name 7230-7519 (including a "7440-7519" range) and 7620-7629. 0 hits for `\b752[0-9]\b`. It is a reserve: the db tests use an internal network and publish no port.
- **Load at 14:11:36: 10.61 10.39 10.00**, over the brief's limit of 8.
- **Code read at head:** migration `0022_…sql:25-68` (columns, CHECKs, grants, the SECURITY INVOKER trigger); recipe `:23-68`; the `inputs.ts` refusals sit after `refuseOwnerOutsideTenant` and before `lockDraft`; `problem.ts:214` maps `23514` (the 409 race path); `openapi.json` `$ref` Exception at `:3018`, `:5501` and VersionException at `:11532`; `0001_core_schema.sql:292` `in_scope boolean`; `expiry_date date NOT NULL`.
- **Builder STATUS (201 lines, read whole):** small mismatch. `:20` says unit "3059 → 3066" and `:143` says "3058 passed → 3065 passed, 1 skipped". These are probably total vs passed. The brief asks the gate to reconcile it (Note at most).
- **B-number:** 0 B331 files in either Briefs folder. (No B330 file exists in Tuesday's `briefs/` either. That number was not used by this drafter.)

## Open questions (each with a recommended answer)
1. **Slot count.** The brief has exactly ONE slot (`STAMP_TIME`), so the REFUSE control works: `.pre-stamp` prints 1 and the stamped copy prints 0. B318 used zero slots and added the time in the launch tap. **Recommended:** keep the one slot. Copy `.pre-stamp` first.
2. **`PC_E8_SOW_TEXT` for the unit step of `ci:node`.** **Recommended:** confirm as at B320's stamp. Pass the path only and never open the file. The builder used a read-only bind mount, and either way is fine.
3. **Throwaway db containers.** The repo's `test-db.sh` removes its own container, anonymous volume and network (`rm -f -v`). **Recommended:** allow the gate to remove ONLY its own `pc-b331-*` throwaway objects by exact name after the logs are saved (precedent B297/B320). The alternative is that each run leaves a ~59 MB volume behind (RELAYED, the script's comment).
4. **Launch while load is 10.6.** **Recommended:** launch anyway. The brief's load gate holds heavy work until two reads under 8, and the light rows (r0, r6-r9 scans) run meanwhile. If HPSM-POC or NexusAI heavy seats are mid-build, stagger instead.
5. **CI/CodeQL still pending at drafting.** **Recommended:** do not wait to launch. The verdict line carries "(conditional: CI/CodeQL pending)" if still unscanned at verdict, and Tuesday re-reads r8 before landing.
6. **The UPDATE grant on the three columns.** No code path uses it. The gate measures what it opens on approved or withdrawn exceptions. **Recommended:** report it as a Note unless a cross-tenant or cross-engagement write is possible (Blocker per the floor).
7. **Severity of a client name in the diff.** I set it at Major, because the builder brief's hold forbids one in the code repo. **Recommended:** keep Major. If it is only in a commit message, it is still Major, because the fix (an amend or a rewrite) is Tuesday's call.

READ-WHOLE-BY-TUESDAY: PENDING
