GATE B1843: NO GO @ 28d2852 on main 5e36d8d

Gate G1 (Opus 5.5, in-session), ROUND 1 OF 2, of OXPd 2 repository rule R5: the exemption of HP's listed
specification inputs by path and sha256, and the key-folder prune. Head
`28d2852d261e819ce760112690a2af9eaf908d43` on `b1836/r5-hp-inputs-exemption`, one commit, one parent main
`5e36d8dca42966395ea3dd014c7f788409eb585f`. Measured 2026-11-21 17:32:00 to 17:39:44 AEDT (clocks by `date`; load1
2.5). Python only: no dotnet job, the wave's lock never taken. Read clone `/private/tmp/b1843-gate/clone` (push URL
`invalid://no-push`); worktrees `/private/tmp/b1843-gate/{head,main}`; the one git write verb (`add` for the
real-folder control) ran in a clone inside the session scratchpad. Every `gh` call `gh api -X GET` under the
project's `GH_CONFIG_DIR`. Programs: `/private/tmp/b1843-gate/{guard,prune,mutants}.py`; logs beside them.

**BLUF.** The code does what was ruled: scope is exact, the guard held against 42 defeat attempts of my own, the
prune never entered a key folder or touched a key file in my instrumented run, red-first gives the seven named
failures, 60 tests OK, the hosted run passes with unchanged dotnet legs. **But the change cannot land as it is:
CodeQL's own Python query suite (CLI 2.27.4, `python-code-scanning.qls`) reports 3 high-severity
`py/clear-text-storage-sensitive-data` results in the new test code (0 on main), and the repository's code-scanning
rule blocks a merge on high or higher.** The fix is one word (a variable named `secret_text`), measured below. In
plain words: not landable today; one small fix commit and a round-2 read first.

## Findings

| # | Severity | Finding | Fix shape |
|---|---|---|---|
| F1 | **Major** (blocks the merge) | `py/clear-text-storage-sensitive-data` (level error, security-severity 7.5) at `build/tests/test_repo_rules.py:366`, `:371` (`handle.write(secret_text)`) and `:71` (the `put` helper, reached from `:378`). The query keys on the NAME `secret_text` (`:360`), though the value is synthetic. Main `5e36d8dc`: 0 results with the same CLI and suite (control). The hosted `Analyze (python)` never ran on this head (branch push), so the builder could not see it; the pull request's run would. | Rename the variable to a truthful non-sensitive name. MEASURED in a scratch copy: `secret_text` -> `folder_text` (4 lines) gives CodeQL 0 results and `Ran 60 tests` `OK`. Never a dismissal or suppression. |
| F2 | Minor (test gap) | Three of my ten mutants SURVIVE the suite (60 of 60 pass): g6 the root check without `normpath` (a key-folder root given with a trailing slash is walked); g7 key files stat-ed (`islink`/`isfile`) before the name skip, against D5's "before any stat or open"; g8 the `hp/` prefix dropped from the line pattern (a listed `generator/x.json` under `contracts/oxpd2/` becomes exempt). The CODE is right on all three (my prune run: trailing-slash root not walked; my guard run: `generator/x.json` fires on the head, is exempt on g8). | Add to K1 a trailing-slash root; to L5 a listed path under `contracts/oxpd2/` outside `hp/` holding a supplied copy. g7 needs a stat recorder (patch `os.stat`/`os.lstat`, as `prune.py` does). As subtests, FLOOR stays 60. |
| F3 | Minor (design, records) | The exemption is exactly as wide as the list, and the list is open: one commit that adds any supplied file without an R5 binary extension under `contracts/oxpd2/hp/` plus its own line passes R5 (and the fingerprint test, which only ties files to lines); `main`'s local R5 catches it (`guard-main.log`, DESIGN rows). This is the ruled door (S4 Q2: the pair), not a defeat, and the hosted job never runs the hash half on either side. Nothing pins the 37 or the list's sha256 `6760314d...` (re-measured: 37 lines, that sha256). | Records: any diff touching `contracts/oxpd2/inputs.sha256` needs a reader; optionally pin the count or the list's sha256, or restrict listed paths to `.json`. |
| F4 | Minor (limit) | A supplied root given as a SYMLINK to a key folder under another name is walked: the root check reads the name given, not the resolved path (my run: `PermissionError` on the locked file = an open was attempted inside the key folder). Operator argument only; the real root is `Source_Documents`. | `os.path.realpath` before the root-name check; a cell. |
| F5 | Minor (text) | The new docstring (`build/repo_rules.py:23-24`) says HP's inputs are "kept on the owner's agreement". The project word scan is clean (its own copy, sha256 `6f932dc5...`, control 13 of 13) and the clause speaks of keeping the files, not of the code; still, it is text about a person's agreement in code. | Neutral wording in the fix commit, for example "listed in contracts/oxpd2/inputs.sha256". |
| F6 | Records | Named limits, ruled: (a) a renamed copy of a key-folder file escapes the hash half; a private key under any name is still caught by the hosted secret scan's content rules and a key-named file by the extension half; a public certificate under another name is caught by neither. (b) Root on the runner: mode 000 does not stop root; K1 still kills a walking mutant by its scandir record and a key-file mutant by the counts (m4, m5, g3, g4, g5 red here); the runner's user is UNMEASURED. (c) Folder names outside the five (`ssl`, `private`, `secrets`) and files like `*.crt`, `id_rsa` are walked and hashed. (d) On a filesystem without `d_type`, `os.walk`'s own `is_dir` may stat a key file (APFS here has it). (e) The list is read from the work tree, not the index (local runs only; `judge` reads the work tree too). | For the records pass. |
| F7 | Records | `README.md:71` understates R5; `<project>/CLAUDE.md:50-51` and `CLARIFICATIONS.md` still carry no entry for the 37-file exception (the builder's FOR RECORDS, confirmed). | Records pass. |

## Item by item

1. **SCOPE: holds.** `compare/main...28d2852d` (GET): ahead 1, behind 0, files exactly `.github/workflows/ci.yml`
   (1/1), `build/repo_rules.py` (81/8), `build/tests/test_repo_rules.py` (148/0); my clone's `diff --numstat` the
   same. The `ci.yml` diff is exactly `-FLOOR=53` / `+FLOOR=60`. One parent `5e36d8dc`. No other build file.
   `test_rules_job_is_the_reviewed_text ... ok` and the floor test `ok` in my run. Tracked files 291.
2. **THE GUARD: holds as ruled.** `guard.py` (synthetic repos and supplied folder): 42 attempts, 42 fire on the
   head: an HP input edited to another supplied file; listed bytes at an unlisted path inside `hp/`, outside it, and at
   a case-variant path; an untracked list; 22 line shapes (upper and mixed hex, one, three spaces, tab, `*` marker,
   leading or trailing space, CRLF, 63 and 65 hex, `..`, `.`, `//`, path from the root, absolute, `./`,
   `generator/../`, path by case, sha of another file, trailing NUL, a Cyrillic look-alike); the same line twice;
   one path with two shas; BOM; CR-only line ends; a UTF-16 list; a swap of two listed files (both fire); listed
   `.pem`, `.key`, `.pfx`, `.dll`, `.zip`, `.crt`; the list renamed by case; a second list elsewhere; a listed path
   under `contracts/oxpd2/` outside `hp/`. Control: the good line is exempt (rc 0) on the head and fires on main.
   Real folder (new program, my scratch clone of the head): two listed inputs swapped and one copied to
   `docs/gate-control.json`: exempted 35, three `RULES: R5` lines, rc 1. **Any way past R5 that main would catch?**
   Only by extending the list in the same commit (F3, the ruled door); no defeat of the pair test itself.
3. **THE PRUNE: holds.** Read: `supplied_hashes` (`:108-133`) returns before the walk for a key-folder root
   (`normpath`+`basename`), removes key folders from `os.walk`'s list in place (topdown) before descent, and skips key
   files by name before `islink`/`isfile`/`getsize`/open. `prune.py`: audit hook (`open`, `os.scandir`,
   `os.listdir`) plus recorded `os.stat`/`os.lstat`, key-folder contents and key files mode 000; 7 cases (7 key
   folders in mixed case including a Kelvin-sign K, 7 key files, a folder link and a file link to key content, a
   key-folder root plain, with `/`, with `/.`, by case, a root holding only key folders, empty): 7 of 7 pass, 0
   key paths touched, 0 key folders entered; main's `supplied_hashes` fails 6 of 7 (control). K1 method: K1 red on
   main (red-first), red on g3, g4, g5. Real folder, new program (after reading the walk): hashed 35210, skipped 4
   key folders and 0 key files, exempted 37 (= 37 lines), `RULES: clean (291 files)`, rc 0. I listed, opened or
   hashed nothing there myself.
4. **TESTS AND MUTANTS: hold, with gaps (F2).** Head `Ran 60 tests`, `OK`; main `Ran 53 tests`, `OK`. Red-first: the
   test diff alone on a clean copy of main: `Ran 60`, `FAILED (failures=7)`, 0 errors, exactly S2, L6, L5, L3, L1,
   L2, K1. My mutants (`mutants.py`, copies only, head untouched: porcelain 0): g1 separator `\s+`, g2 no `$`
   anchor, g3 prune by rebinding the list, g4 folder names case-sensitive, g5 key-file names case-sensitive, g9
   exempt on any listed digest, g10 exempted note counts all: each RED by assertion; g6, g7, g8 SURVIVE (F2).
5. **THE HOSTED RUN: holds.** Run 44875596961, attempt 1, head `28d2852d`; four check runs success (GET). Logs by
   GET with `--allow-escape-sequences`, rc 0: rules `Ran 60 tests in` 1, `UNIT-TEST FLOOR: ran 60, floor 60` 1,
   `RULES: clean (291 files)` 1, K1 `... ok`, `R5 hash half NOT RUN`; linux `total: 894` x2, failed 0, skipped 4;
   windows `total: 894` x2, failed 0, skipped 19 (main's run 136744868551/478: the same); `0 Warning(s)`,
   `0 Error(s)`; secret-scan both PLANTED-CONTROL lines, `no leaks found` x3. Control string count 0. No `Analyze`
   run on this head.
6. **TEXTS: not written (NO GO).** The project word scan over the 230 added lines and the commit message: clean.

## Builder's claims
READY sha, the three sha256, red-first 7, real-folder 35210/4/0/37, hosted PASS: true (re-measured). Mutants 0
surviving: true for the builder's set (not re-run; mine leave 3). Deviation 1 (PR 1 is the file's creation): true,
accepted. Deviation 2 (148, not 145): true. "CodeQL will run on the pull request": true, and it would fail (F1).

## For the fix round (round 2)
One new commit on the branch: rename `secret_text` (F1, required); cells for g6 and g8 and a stat recorder for g7
(F2, recommended); neutral docstring clause (F5, recommended); optionally `realpath` (F4). Then the local CodeQL
Python suite must print 0 results, the suite 60 (or the new floor in the same commit), and the round-2 gate reads it.

## NOT RUN
Anything on Windows beyond the hosted job; the runner as root; the builder's `mutants.py` and `r5_controls.py`
(mine instead); CodeQL for `actions` locally; an unreadable folder in the supplied source (H12); any pull request,
merge-ref run or landing text; nothing written outside this folder and `/private/tmp/b1843-gate/` (plus one scratch
clone in the session scratchpad).
