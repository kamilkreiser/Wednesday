# QA GATE tier 2, round 1 of 2 - T3/R4 batch (#1727, #1728) - findings only

Gate model: claude-sonnet-5-5. Date 2026-10-27, window about 07:47 to 07:56 local. Pushed/merged/commented/edited: nothing. Workspace: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate-t3r4-1027/` (own `--shared` clone in `repo/`, private TMPDIRs under `tmp/`).

## Pins
`ls-remote` at START and at END identical (saved `pins_start.txt`, `pins_end.txt`, `diff` clean), and equal to Wednesday's pins. No head moved.
develop `ec3313a80440d0eee9fd07204c024518417ff9d7`; #1727 `ecc9265f0761885b7861510db81412190472cb46`; #1728 `93513a6067cfcd3af9bf7a87d8abb06339321503`.
A verdict below is about these SHAs only. Both PRs have merge-base == develop head (not behind).
PR bodies read with `gh pr view` (GH_CONFIG_DIR + .env of the Blockchain project): worked, both bodies read in full; also read both commit messages.

## BLUF

| PR | Verdict | Worst finding |
|---|---|---|
| #1727 KS-1734 | GO WITH NOTES | LOW: the body's "knob governs exactly the files the ticket names" is looser than what I measured (at hookTimeout=25 ms 18 files go red, not 10), and the "181 silently skipped cells" figure is unreproduced; the NOT-COVERED wording itself is honest |
| #1728 KS-1745 | GO | none above INFO; comment-only runner proven, 82/0 twice, M3 and M4 each turn only their own new cell red |

Merge order: develop+#1727, develop+#1728, #1727+#1728 and #1728+#1727 all merge clean (`git merge-tree --write-tree` rc 0, no conflicts). The two sequential orders give the SAME tree `8fe9b85a9e4efd7325f74f90f1c1d03a23fc552c`. Disjoint files (security vitest.config.ts vs two shell files). No ordering constraint.

## #1727 KS-1734 (services/security vitest.config.ts, hookTimeout/testTimeout 60_000)

FOUND
- Diff vs develop (three-dot): exactly one file, `Blockchain/Dev/services/security/vitest.config.ts`, +10/-0 (8 comment lines + `hookTimeout: 60_000,` + `testTimeout: 60_000,`). Nothing else. Confirms the "only file" claim.
- NOT-COVERED wording is honest: "This change is **not shown to remove the failure, because the failure did not occur here in 4 cold attempts** ... There is no red->green pair in this PR ... cited and not reproduced. What IS proved here is that the knob governs those exact hooks and that the change regresses nothing." It does not claim removal. It also bounds the claim (4 clean runs do not exclude a 1-in-6 rate) and says no load-induced repro was tried. The commit message says the ladder "shows this knob governs exactly the files the ticket names", slightly stronger than the body; see LOW below.
- In-config comment claims "a 1/25/100/400 ms ladder lapses exactly the files the ticket names". Not exactly true on my run (see below), but the claim sits in a comment, not in code.

TESTED-HOW
- Clone checked out at pr1727 head, `npm ci --ignore-scripts` rc 0 (1806 packages), `npm run build --workspace=packages/shared` rc 0, `dist/index.js` present. Fresh install, no `.vite` cache present beforehand (checked), so the first run is cold. Node/vitest invoked as `node_modules/.bin/vitest run --root services/security` (I could not cd).
- HEAD green: `Test Files 33 passed (33)`, `Tests 361 passed (361)`, rc 0, duration 7.33 s at load1 about 5.4. Matches the PR's 33/361. One run only (the PR ran 3).
- LADDER, key governs the hooks. Pristine sha256 `615ffbc983ea9a344c7250e10ffbc276c83f72544d85876700b9a8947a6cbc70`.
  - hookTimeout 60_000 -> 25, testTimeout left 60_000 (edited by assert-exactly-one python replace): rc 1, `18 failed | 15 passed (33)` files, `145 passed | 216 skipped (361)` tests, 18 "Hook timed out" lines, 0 "Test timed out" lines. Hooks alone turn files red and skip their cells. Restored with `git checkout --`; sha256 back to `615ffbc9...cbc70` (identical).
  - testTimeout 60_000 -> 25, hookTimeout left 60_000: rc 1, `11 failed | 22 passed` files, 18 tests failed, 0 "Hook timed out", 17 "Test timed out". The two keys govern disjoint failure classes, each independently. Restored, sha256 identical to pristine.
  - Controls: head at 60_000 has zero of either timeout string (grep counts taken from the same logs where the positive arm shows 18 and 17, so the grep is not blind). `git status --short` empty after both restores.
- Composition with #1703: `ks742-keys-tenancy-route-contract` is ABSENT from the hookTimeout=25 failing list and PRESENT in the testTimeout=25 list. That is consistent with the body's claim that its explicit `HOOK_BUDGET_MS = 60_000` overrides the config default. (Consistent with, not a separate proof; I did not read the line-112 code.)
- Leg 16: `node scripts/typecheck-tests/check.cjs services/security` at head: rc 0, "tsc examined 52 files, 40 of them under __tests__; 0 errors: 0 in the baseline, 0 new; 0 stale baseline entries". Identical to the 52/40/0/0/0 the body quotes. No new error. (No positive-control mutation run on this instrument; the file changed is a config, not a test, so the result is expected.)
- Merge-tree: see BLUF.

NOT TESTED
- Any red->green pair (the red did not reproduce at this load; same as the seat).
- Load-induced reproduction (shared laptop, kept load modest). Load1 was 5-8 during my runs.
- The rungs 1/100/400/1000 ms and the table's other counts; I ran only the 25 ms rung, split by key.
- The "181 silently skipped cells" figure: my 25 ms hook-only run skipped 216, a different budget, so it neither confirms nor refutes 181.
- The pre-push preflight (13/16 legs) claim; the integration config; any other service.
- Whether a hang now takes 60 s to report (stated cost; not exercised).

SEVERITIES
- LOW: "governs exactly the files the ticket names" is overstated. At hookTimeout=25 ms, 18 files fail (including ks1556, ks1568, ks577, ks698r1, ks869, ks880, ks908, ks952-rate-limit-scope, ks974, ks976a, ks976b, which are not in the body's list of ten). The body's own table shows the same 18 hook lines at 25 ms. The accurate statement is "the ten named files are all within the set the knob governs", which the body also says at 100 ms. Wording only; the value 60_000 and the config are unaffected.
- INFO: one local run instead of three; not a defect.

## #1728 KS-1745 (run-shell-suites.sh comments; run_shell_suites.test.sh +12 cells)

FOUND
- Scope vs develop: 2 files, +177/-5: runner `+24/-5`-ish (29 changed lines, all `#` lines) and test file +153. No other file.
- Runner change is comment-only, PROVEN: deleting every line whose first non-blank character is `#` from the develop runner and from the head runner gives byte-identical text (`cmp` rc 0; both 210 lines, both sha256 `e21abb6c6b2277b3cb188a6791ea30510d5ec060e315d16f0b2bf08b223714c7`). Independently, every `+`/`-` line of the runner's -U0 diff matched `^[+-]\s*#` (count of non-comment changed lines: 0). `bash -n` on the head runner: ok. Control: sed-mutating the guard (`&& [ -n "${rss_own_pgid:-}" ]` -> `&& true`) on a copy and applying the same strip makes `cmp` report a difference (line 156), so the instrument can see a code change. (A first control attempt used a pattern that did not match the real text; it printed nothing and I discarded it, see instrument errors.)
- The body's line numbers hold: guard at 319-320, own-pgid read at 307, suite pgid read at 419 and its reset at 423 (confirmed with `git grep -n` at head).
- Item (b) (TERM-ignoring suite) is declared uncovered in the PR body ("**Item (b), a suite that traps and ignores TERM, is left uncovered** and is now stated as a declared limit") and in the commit message ("NOT COVERED, deliberately"). Confirmed. Also listed again under "NOT run".
- Cell count: 12 new cells = 2 arms x (2 fixture + 3 control + 1 assertion). Matches 70 -> 82.

TESTED-HOW
- Head, own clone at pr1728, `TMPDIR=$W/tmp/r1` : `run_shell_suites: 82 passed, 0 failed`, rc 0. Second run (`tmp/r2`): 82/0 again. Launch shape printed "INT installable=yes, TERM installable=yes", the same shape the body measured at, so the ratio 82/0 is comparable. (The body's ratio caveat about the hook's SIGINT-ignored environment stands; I did not run there.)
- Mutants, applied to line 319 of the runner by line number with the content asserted first (the python asserts the target substring occurs exactly once on line 319). Pristine runner sha256 `dfd8181823285517ed00f5a83bd5a78ae4e5e1e147c08e57eca610b36b252c6c`.
  - M3 (blank the own-pgid test: `[ -n "${rss_own_pgid:-}" ]` -> `true`): line became `if [ -n "${rss_suite_pgid:-}" ] && true \`; sha256 after `c15f3ea9d1adf76bd98ad6811ec1e14f186b815c8a9cc1a70b9fe95dd77a925c`; `bash -n` ok; suite `81 passed, 1 failed`, rc 1; the ONLY FAIL line is `KS-1745 (a) M3: ... a SIBLING in the shared group SURVIVES ... expected 1, got 0`. All six fixture/control cells for the M3 arm and all of the M4 arm stayed green.
  - M4 (blank the suite-pgid test: `[ -n "${rss_suite_pgid:-}" ]` -> `true`): line became `if true && [ -n "${rss_own_pgid:-}" ] \`; sha256 after `9245940299a3e9d176c9e58276450e7e167af7bcb7d65e5907398119a3533db6`; `bash -n` ok; `81 passed, 1 failed`, rc 1; the ONLY FAIL is `KS-1745 (a) M4: ... the suite is GONE afterwards ... expected 0, got 1`.
  - Each mutant restored with `git checkout --` of the runner; sha256 after each restore `dfd81818...b252c6c`, identical to pristine; `git status --short` empty at the end.
  - Controls for the mutants: the unmutated runner is 82/0 twice (above), and the new cells' fixture-integrity cells (ps stub consulted exactly twice, launch `set -m` removed, shared pgid, sentinel and suite alive beforehand, runner exited) are green under both mutants, so each red is the assertion and not the environment.
  - Note on mutation shape: I replaced the dropped test with `true` rather than deleting the clause, so the `&&` chain stays well-formed. The PR describes M3/M4 as "drop" the test; `true` is behaviourally the same drop.
- Merge-tree: see BLUF.

NOT TESTED
- Item (b) behaviour (declared uncovered).
- The comment-precision claims c1/c2 (INT delivery table with `sleep 30`, `ps` keywords `sig`/`blocked`/`pending` reading 0). They are measurements on macOS bash 3.2.57; I did not re-measure them. They are comment text only; I checked they cannot change behaviour (strip proof), not that they are true.
- Execution inside the pre-push hook's SIGINT-ignored environment (UNREACHABLE arms); the 95/0/1 of-96 leg 14 claim; the full preflight.
- Linux.

SEVERITIES: none above INFO. INFO: the body says "12 new cells" and "+153 lines" and both are correct; the c1/c2 comment prose is long (about 19 added comment lines), which is a readability cost, not a defect.

## My own instrument errors
1. First `ls-remote` returned develop `c56dd7c3...` and no PR refs: `git clone --shared` of the cache `src` makes `origin` point at the local cache, not GitHub. I set `origin` to `git@github.com:Secuura/Distributed_Secuura.git` (the `src` clone's own origin URL), re-ran, and got the real pins, which match. All later fetch/ls-remote used the explicit key. The saved `pins_start.txt` is the corrected read. Nothing was concluded from the wrong read.
2. The workspace hooks refused three of my calls: a `cd` (twice, no effect), `git -C $VAR ... merge-tree/checkout` (variable path not recognised as in-workspace; I re-issued with the literal path), and an `rm -rf` of a `.vite` cache (I skipped it after confirming no `.vite` directory existed). The first M3/M4 loop was refused before it ran, so no mutation was applied then; pristine sha was re-read before the second attempt and matches the final restore sha.
3. My first comment-strip control used a sed pattern that did not match the real guard text, so it produced no difference and proved nothing; redone with the correct pattern (`&& [ -n "${rss_own_pgid:-}" ]`), which does differ.
4. `npm ci` was run with `--prefix` and vitest with `--root` because I could not `cd`; the result matched the PR's counts exactly, so I treat the instrument as sound, but it is a different invocation shape from `npx vitest run` in the directory.
5. The `.env` file of the Blockchain project was sourced into a subshell to run `gh pr view`; nothing was echoed or written.

## Files created outside my workspace
- Verdict dir: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-27_gate-t3r4-batch/verdict.md` (the only file there).
- Outside the workspace and verdict dir: none that I wrote deliberately. Two side effects to disclose: `npm ci` writes its download cache to the default `~/.npm/_cacache` (I did not redirect it), and the `--shared` clone reads objects from `cache/src` through git alternates (read-only; `src` was not modified; its `.git` was not written to by me).
- Boxes, Azure, Docker, Linear, GitHub writes: none.
