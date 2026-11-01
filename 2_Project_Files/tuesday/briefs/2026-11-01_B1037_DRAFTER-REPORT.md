STARTABLE: YES (after Tuesday's stamp; launch it BEFORE B1038; both gates share `.tools/composer-heavy.lock` and never run heavy jobs at the same time)

# B1037 drafter report: SEAT-G257, Security Composer, tier-1 gate of B1017 Part A (PCOMP-102) @ 3871eefb, round 1 of 2 on the new lane's own counter

Drafted 2026-11-01 11:09 to about 11:2x AEDT (`date`). Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1037_SEAT-G257_composer-pcomp102-restore-footer-gate-tier1.md` (94 lines). Its `.pre-stamp` is a byte-exact copy (`cp -n`, `cmp` rc 0, sha256 of both `431f364251b2c4a88d2a31cf186631e6c78a0563f804154ee54528f812ede354`). Four-underscore line count 9: eight slots plus the last line. Non-ASCII bytes 0. At-sign-capitals pattern 0. Person-name and card-id greps 0.

## BLUF
- The kit gates `b1017/composer-pcomp102-restore-footer-check` @ `3871eefbf266b055dc2e8eee26bf37d364b97dc7`: one commit on main `075b2b23`, two paths, no PR. Tier 1, row G1 (`model-routing.md:108`), Opus (`claude-opus-5-5`, `models_latest.json:17`). The launch line carries `BRIEF_SEAT_LEVEL=opus` inside the quotes.
- **The heart is C2 and C3.** C2 takes the new awk line clause by clause, measured under the image's mawk and the host's BWK awk (busybox only if a local image already holds it). C3 is the gate's OWN throwaway digest-pinned `postgres:16` with `--network none`, holding six plants:
  - P1 and P2: the ticket's function-body line and data row;
  - P3: a three-line block;
  - P4: the block plus an `\unrestrict` line with another key;
  - P5: a planted key pair;
  - P6: a data row equal to an `\unrestrict` line (COPY should escape it).
- C3 also takes: two `pg_restore` runs of one dump (is the key random per run?), an older-minor shape with neither key line, the builder's residual, and a full prefix sweep. **It runs ONLY the check line; never psql on a script, never apply, never DROP.**
- C4 re-does M0-M5 and adds M6-M16, plus two cross-document runs:
  - main's test against the head's DEPLOY.md: exactly row 620 red;
  - the head's test against main's DEPLOY.md: exactly 8 red.
- The other checks: C1 (delta, closed list, identity, commit-message truth), C5 (b616 and the scanner scratch, plus paste shapes), C6 (db group, names lost 1 / added 9, chain), C7 (NEW WORDS, including "before 16.10" against an offline source in the image), C8 (merge, Part B independence, CodeQL NOT SCANNED as a Condition, the four landing files).
- FOR TUESDAY must carry the open risk by name, in a paragraph given word for word in the kit: a demo `pg_restore` older than 16.10 makes the strict check refuse every real restore. It is unmeasured and fenced. The source fact: `compose.yaml:18` pins the CI digest at main and at the deployed `d70edf70`.

## Facts (instrument; control)
1. Pins 11:09 (`git --no-optional-locks ls-remote`): main `075b2b23...`, A `3871eefb...`, B `dea1d09f...`, `b1037*` and `b1038*` absent. `b103*` also matches the old `b103/lane3b-contract-0.30.0`, so the kit matches `b1037*` exactly. Control: `b985*` listed `642a0472`.
2. `compare/main...<A>` (`gh api -X GET`, Composer `GH_CONFIG_DIR`, Datasec account count 1): ahead 1, behind 0, `DEPLOY.md` +10 -6 `2e48c823`, test +174 -2 `a34c6008`. PRs for either b1017 branch: 0 (control: b985's branch 1). Open PRs: #95, #91, #86, draft #85.
3. `git diff -U0 075b2b23 3871eefb`: 8 removed lines (DEPLOY.md 203, 256-259, 263; the test's row-620 title and value), counted by `/usr/bin/grep -c -E '^-[^-]'` = 8 and listed.
4. Counts with `/usr/bin/grep -c -i -F` on `git show <sha>:DEPLOY.md` (head / main):
   - `PostgreSQL database dump` 1 / 1;
   - `tail -n 6` 2 / 3 (head lines 251 and 267);
   - `except the completeness check` 2 / 2;
   - `Nothing else in the command is pinned` 1 / 1;
   - `wc -l` 652 / 648.
   Control `zzz-no-such-string-7f3a` 0 at both.
5. Blobs equal at main and head (`rev-parse`): b616 `4bbace25`, `support.ts` `13eb5f3e`, `app.ts` `2c5d5ad1`, `package.json` `32fea116`, `package-lock.json` `53305eb4`, `compose.yaml` `fc6b69a2`.
6. Test at head: 23 `it(` rows, at lines 658-1117 (`/usr/bin/grep -n -E`). Retitled row 696; new rows 733-787; `spawnSync` at 451.
7. Commit `3871eefb`: subject 115 characters, one trailer (the harness's exact line), author domain noreply. The local part was elided at read (`sed`) and never printed.
8. `compose.yaml:18` at `075b2b23` AND at `d70edf70` pins `postgres:16@sha256:f1c3376c...`, the same digest as `scripts/common.sh:9` and `scripts/test-db.sh:6` (`git grep`, `git show`).
9. Landing rule `CLARIFICATIONS.md:1799` (`grep -n -i -F` lists 1799 first, then 9 quotes; control 0); `:2032` holds `match-head-commit`. Main's squash subject ends `(#106)`. PR #106's body ends with the ASCII line `Generated with [Claude Code](...)`: `od -c`, non-ASCII count 0.
10. Seats and ports:
    - Seat `G257`: 0 kit files name it. `G256` is taken by the concurrent B1036 kit (HPSM-POC, 3 files); control `G255` 12.
    - Ports 9670-9679: 0 of the 10-31/11-01 SEAT kits mention it (B1036 uses 9290-9299 and 9740-9749; control 960x 7 files). `lsof -iTCP:9600-9799 -sTCP:LISTEN` rc 1.
    - Panes: tuesday, HPSM-POC-R109, HPSM-POC-D43, fleet-monitor (no Composer pane).
    - Load: load1 2.48. The project lock is absent.
11. Host tools: `/usr/bin/awk` 20200816, `/bin/bash` 3.2.57; no gawk, mawk or busybox in `/opt/homebrew/bin`; gitleaks present.

## D-decisions
- D-1. Tier 1, G1 `:108`, Opus. The line is the only guard in front of a `--clean --if-exists` restore plus DROP and apply. The builder kit used C4 `:94` for the build.
- D-2. The gate builds its OWN real dump and cuts, and adds plants the builder did not run: P3-P6, the two-run key test and the full prefix sweep. This answers whether a planted line can ever carry the key. It still runs only the check line.
- D-3. Plumbing comes from `.tools/b879/scripts/`, the builder's source (a finished kit), with four declared adaptations: the B985 release line, the B878 project lock, the DEPLOY.md mount and `names.py`. The builder's `.tools/b1017/` and its evidence are read-forbidden as instruments.
- D-4. The builder's own residual (an older-minor script plus a planted key pair, accepted) is graded **Minor** unless a 16.10+ script can reach it. No new sentence claims it is refused, and it needs five planted lines in an older-minor dump.
- D-5. An unpinned clause (M6-M8, M10, M11, M14 green) is graded by real reachability: Major if a C3 real cut is accepted under the same swap, Minor if not, Note if equivalent.
- D-6. "before 16.10" is a version fact no run can make (no older image, no pull). The kit looks for an offline source inside the local image's docs: found = backed, not found = Minor (d).
- D-7. CodeQL NOT SCANNED (no PR) is a Condition, never a finding and never green. The verdict is always marked conditional.
- D-8. The seat is G257, not G256: B1036 (the concurrent HPSM-POC gate drafter) took G256 at 11:1x. Ports are 9670-9679 (A) and 9680-9689 (B), away from B1036's blocks.

## Q-questions (each with a default)
- Q-1. Seat G257, ports 9670-9679. Default: accept.
- Q-2. The C3 real-dump container and the full prefix sweep (check line only). Default: YES.
- Q-3. Plumbing from `.tools/b879/scripts/` with the four adaptations. Default: accept.
- Q-4. The SOW text bind mount for the unit step (read-only, `--network none`, stat only). Default: YES, as B779 and B1017 did. If there is no answer, the kit reads NO and the SOW-dependent unit rows are NOT TESTED.
- Q-5. The older-minor residual graded Minor (D-4). Default: accept.
- Q-6. Launch order: A first; B's waiter starts only after A's launch is verified (one waiter at a time). The shared project lock serializes heavy jobs. Default: accept.

## UNMEASURED
- No test, container, image listing (no docker call at all), check line, dump, cut or mutant was run. Every "expected" or "predicted" in the kit is arithmetic on the diff and the builder's claims.
- Not checked: whether `postgres:16@sha256:f1c3376c...`, `node:24-alpine` (busybox) or the `pc-b1017-*` images exist locally; whether the image ships PostgreSQL docs that name 16.10.
- The b616 count (56) and the group counts (530 -> 538) are RELAYED.
- Not re-measured: the overlap of the open PRs with the lane paths, and the round-count loop over `*_STATUS.md` first lines. The kit states nothing / B779 + B787 as the expected results, not read by me.
- The demo VM's running `pg_restore` and its container digest (fenced).

## Outside-the-fences disclosure
- Writes: the kit, its `.pre-stamp` and this report under `tuesday/briefs/`; the B1038 trio; scratch diffs and the head test file in the session scratchpad (`/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/c9371317-968c-4c10-88d6-79a675bd3109/scratchpad/b1037/`). Nothing in any project, the vault or a remote.
- Reads: the Composer `CLARIFICATIONS.md` (C-101, C-105 to C-114 headings, C-113, C-114), the B779 and B1017 STATUS files, `.tools/b879/scripts/` (names only), `.tools/b985/scripts/heavy.sh` line 51, `.tools/b1017/` and its evidence folder (listing names only, no file opened), `eslint.config.js` and source lines at main. One read of `0_Brain/daily_tuesday/2026-11-01.md` lines 130-140, to confirm that B1037/B1038 were assigned to this task.
- `gh` was `-X GET` only. `git` was read verbs with `--no-optional-locks` on objects already local; no fetch.
- **A fence slip:** at 11:20 one scan command held a no-op `(cd /dev/null 2>/dev/null; cat) >/dev/null` subshell, against "never type cd". It wrote and changed nothing.
- Hook advisories on case-sensitive greps: the counts used were re-run with `-i` or had a positive control.
