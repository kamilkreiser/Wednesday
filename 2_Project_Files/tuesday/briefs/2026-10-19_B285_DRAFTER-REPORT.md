# B285 DRAFTER REPORT (2026-10-19, clock from `date`: 15:45 AEDT at start of reads)

Brief: `2026-10-19_B285_SEAT-W5_composer-ci-timing-tests-b281-1.md` (same folder). Nothing built, nothing pushed, no git write verb run.

## What I read (with line refs)
- Template `2026-10-19_B280_SEAT-W3_composer-objects-image-variable.md` whole (1-68): shape, headings, standing lines 1-8, identity/refs/ports/load blocks, STATUS list, last-line markers, stamp block.
- `Briefs/2026-10-19_B281_STATUS.md` whole: findings `:131-152` (B281-1 `:132-137`, B281-2 `:139`, B281-3 `:141`), runs `:64-88`, FOUND/NOT TESTED/PRIOR WORK `:154-158`.
- `Briefs/2026-10-19_B280_STATUS.md` whole: proposed rows `:41-44`, disappearance risk `:125-133`, F-5 `:53`, command/identity facts.
- Code repo at the stale local `origin/main` (230f9fab): `s47-crf2-linear-detector.test.ts` `:1-260`, `b20-codeql-redos.test.ts` `:1-130`, `vitest.config.ts` whole, `scripts/ci.sh` `:60-100` and `:1-30`, `package.json` scripts, `docker/Dockerfile` ci target.
- `git log` of both test files (5 commits, below). BACKLOG.md rows #31 (`:35`), #115 (`:119`), #237 (`:233`), #84/#140 (`:88,:134`), tail rows #316-318 (`:312-314`), head lines.
- `gh api` GETs (kamilDatasec): `ci.sh` and `compose.yaml` at `50d97508` (comment and image lines), and compare 230f9fab...50d97508 = ahead_by 1, files = `compose.yaml`, `scripts/ci.sh` only.
- B92 evidence folder listing `Briefs/2026-10-06_B92_evidence/addendum6/` (files exist; contents not opened).

## Premises and sources
1. Main is `50d97508105af917ece8307063635f8475773f68`: MEASURED, `git ls-remote origin refs/heads/main`.
2. The local clone's `origin/main` is stale (still 230f9fab): MEASURED (`git show origin/main:scripts/ci.sh` has no `PC_OBJECTS_IMAGE`). Brief orders a fetch.
3. **Both tests already use CPU time and best-of-N** (B92 ADDENDUM-6 / #115 / #51 `0d65a1d6`): MEASURED, `b20:21-40`, `s47:52-71,156-186`; BACKLOG `:119` says FIXED, merged. So the gate's fix-shape "CPU-time minimum-of-samples" is already in place and B281-1 is a recurrence after the fix. This is the main point of the brief (the "TRAP" paragraph); the seat must find the cause, not repeat B92.
4. Failure data (x77-x107 vs x80; 251/254 ms vs 250; main fails 2 of 5, head 2 of 8 pass; isolated 8/8): RELAYED, B281 STATUS `:70-72,81-87`.
5. Authors/why: `fe18c4bb` (Kam Kreiser, 2026-09-14, S47 CRF2, file created); `5b5252c1` (kamilDatasec, 2026-09-29, B20 Seat A, b20 file); `1e4599dd` (2026-10-02, B35/B37 growth ratio, #31); `0d65a1d6` (2026-10-07, B92 #115 CPU time, #51); `9d0e53ff` (2026-10-13, comment rename). MEASURED by `git log`. "Why" is from the files' own comments and BACKLOG #31/#115 (read).
6. Comment lines: `ci.sh:13-14` and `compose.yaml:122-123`: RELAYED from B281 `:139,:141`. At `50d97508` the ci.sh comment is two lines before the `export` on line 15 (MEASURED via gh api, by offset); compose comment text confirmed present, exact numbers left for the seat to confirm.
7. BACKLOG: last row `| 318 |`, and zero hits for chainguard/B280/PC_OBJECTS_IMAGE: MEASURED. No B285 hits in `briefs/` or project `Briefs/`: MEASURED (the grep listed none).
8. Row (c) of B280's proposals: B280 STATUS `:44`; brief says add only if no existing row says it.
9. Load: `uptime` read 6.29 then 7.87 (1-min) with no Composer seat; so I set the load gate at below 8 per your instruction (B280 used 6). The hog is capped at N=4 for 5 min, by PID kill only: my choice, flagged for you.
10. Empty `DOCKER_CONFIG` breaks compose/buildx: RELAYED B281 `:66`; the brief withdraws that B280 instruction.

## Could not measure
- Why CPU time still reads high under load (the brief lists five candidates, none established), the real min/median/max per case, whether a fix inside the two files suffices, whether main still fails today. All left to the seat as UNMEASURED.
- Exact current line numbers at `50d97508` for compose.yaml 122-123 (not printed cleanly); the seat re-confirms.
- Contents of the B92 kit (`mutants.py`, `underload.sh`): existence only.
- Whether the siblings in #237 share the cause.

## Decisions I made that you may want to change
- `vitest.config.ts` is NOT in the partition (you listed only the two test files); a serial pool needs it. Brief says: if evidence demands it, `STOPPED: NEEDS TUESDAY` with one yes/no question. Pre-approve it at stamp if you prefer.
- BACKLOG rows (B281-1/-2/-3, B280 risk a, b, and c conditionally) are written by the seat in the project folder, uncommitted, per "records stay local".
- Last-line marker adds the hog and mutant claims to the usual READY format.

## Slots left (3 literal in the file, plus one named in the stamp block)
`@SLOT:COMPOSER_MAIN_SHA@` (drafted value 50d97508... given beside it; re-read at stamp), `@SLOT:STAMP_TIME@`, `@SLOT:PORT_BLOCK@`; B_NUMBER_CONFIRM is named in the stamp paragraph only (0 hits measured). Model, pane and suffix are written in. Note for the `.pre-stamp` control: it will count 3, not 4+.
