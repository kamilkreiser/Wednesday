GATE B1850: GO WITH FINDINGS @ 2229f68 on main 0804860

Gate G1 (Opus 5.5, in-session), ROUND 2 OF 2 (the last), DELTA read of OXPd 2 repository rule R5's fix commit
`2229f68bea9a873be01ced0eeda84803f4d66cf1` (one parent R1 `28d2852d261e819ce760112690a2af9eaf908d43`) on
`b1836/r5-hp-inputs-exemption`, plus the whole branch's readiness to land on main
`0804860b8993f6d7fd393cb64c44afcd2f9c8f05`. Measured 2026-11-21 18:30:59 to 18:41:39 AEDT (clocks by `date`; load1 9.4
to 13.8, other seats' dotnet work). Python only: no dotnet job, the wave's lock never taken. My clone (push URL
`invalid://no-push`) and worktrees `head`, `r1`, `main`, the merge tree and every scratch git repository are in the
session scratchpad (the workspace hook refuses git write verbs elsewhere); programs and logs in `/private/tmp/b1850-gate/`
(`mutants.py` sha256 `04d23115...`, `texts.py` `be51b053...`). Every `gh` call `gh api -X GET` under the project's
`GH_CONFIG_DIR`. The only programs that walked the real supplied folder: the head's own `build/repo_rules.py` (after I
read its walk again: `realpath` root check, then in-place removal of key folders from `os.walk`'s list before
descent, key files skipped by name before `islink`/`isfile`/`getsize`/open) and the kit's `r5_controls.py` (sha256
equal to the kit's list), run on a lane whose `clone` is my head worktree. I listed, opened or hashed nothing there
myself, and never ran main's or R1's program with `--source-documents`.

**BLUF.** Every round-1 point that blocked or was asked for is closed: CodeQL reads 0 results on the head in both
Python suites (3 + 3 on R1, the control), the three surviving mutants are now killed by assertion, the link root is
no longer walked, and the docstring is neutral. Scope is exactly the two files; 60 tests OK; the real folder clean
with 37 exempted; the hosted run passes; the branch merges clean with the moved main and the merged tree passes. One
Minor finding (an edge `realpath` narrows) and records only. **In plain words: this can be landed; because main moved,
the pull request's checks must be proven to have built the merge with main 0804860b (landing.txt step 2), and the
hosted CodeQL analysis on the pull request must read 0.**

## Findings

| # | Severity | Finding | Shape |
|---|---|---|---|
| G1 | Minor (limit, text) | `realpath` narrows one case R1 covered: a supplied root NAMED like a key folder that is a link to a folder with another name is now walked. Synthetic run: `names/certificates -> sup/devroot`: head `(hashed 1, skipped 0, 0)`, R1 `(0, 1, 0)`. The docstring's "by its name or through a link" reads wider than the code. Operator argument only (default root `Source_Documents`); nothing in a key folder is reached that R1 protected by content. | Later build lane if wanted: check the name given AND the resolved name (or every component of the resolved path, which also closes H18). Stated in pr-body's limits. |
| G2 | Records | H18 now MEASURED (the kit had it DERIVED): a root `.../certificates/sub` and a link to it are walked (hashed 1 each); `plain -> Certs`, `plain/`, `Certs/.` are skipped (0, 1, 0). | Records; stated in pr-body. |
| G3 | Records | K1's stat recorder (and its positive control), mode-000 files and `os.symlink` are POSIX-shaped. On CPython 3.12+ for Windows, `os.path.isfile`/`islink` are native fast paths that do not call `os.stat` (DERIVED, not run): the cell would fail loudly there, never pass silently (H19). The hosted rules job is Linux only (`Image: ubuntu-26.04`; its Python version is not printed). | Records. |
| G4 | Records (landing forms) | The default code-scanning setup stores a pull request's analyses on `refs/pull/N/head` (pull request 7: three analyses at `9d496955` there, `results_count` 0 each; none on `refs/pull/7/merge`), and an alert read on `refs/pull/N/merge` prints 0 with nothing analysed. Gate B1846's landing form read the merge ref (a 0 that cannot fail). | This landing reads the analyses on the head ref first (positive control), then alerts there. |

## Item by item

1. **SCOPE: holds.** `git diff --numstat R1 2229f68b`: `5 4 build/repo_rules.py`, `42 9 build/tests/test_repo_rules.py`;
   name-status two `M`, no other path. `git diff --quiet R1 2229f68b -- .github` rc 0; `ci.yml:192` `FLOOR=60` (R1's own
   line). One parent R1. Commit author and committer the project's configured address (masked); subject and the one
   attribution line. The whole branch against its base 5e36d8dc: `ci.yml` 1/1, `build/repo_rules.py` 82/8,
   `build/tests/test_repo_rules.py` 181/0, nothing else.
2. **F1: CLOSED.** The kit's `codeql_py.py` (sha256 equal to the kit's) with CLI 2.27.4 (first line
   `CodeQL command-line toolchain release 2.27.4.`), suites `python-code-scanning` and `python-security-extended` (the
   default setup reads `configured extended actions,csharp,python`, GET): head `CODEQL 2229f68bea9a: 0 results
   (code-scanning 0, security-extended 0)` rc 0; **R1 control** `6 results (code-scanning 3, security-extended 3)` rc 1,
   `py/clear-text-storage-sensitive-data` at `build/tests/test_repo_rules.py:71`, `:366`, `:371` in each suite (fired);
   main 0804860b 0 + 0; the merge tree 602ed3b6 0 + 0. Each scanned 5 of 5 Python files (the repository has Python only
   under `build/`). GATE_STEP in spirit: `pr_codeql_check.sh --base 0804860b --head 2229f68b --lang python`: results head
   0, base 0, KEPT 0, NEW 0, `RESULT rc 0 PASS`. No result of any severity exists on the head, so none touches a line the
   branch adds. Hosted `Analyze` has not run on this head (branch push only): the pull request's.
3. **F2: CLOSED.** My own `mutants.py` (copies of the head's `build/`; worktrees untouched, porcelain 0 and 0), each
   mutant run with the head's tests and with R1's `test_repo_rules.py`, all `ran 60`:
   g6 root name as given (`basename(folder)`): head RED, FAIL 3 (`[trailing separator]`, `[trailing dot]`,
   `[link under another name]`), R1 tests GREEN. g7 `islink`/`isfile` before the key-file skip: head RED,
   `AssertionError: True is not false : stat of a key file: .../tools/store.jks`, R1 tests GREEN. g8 line pattern
   without `hp/`: head RED, L5 `[listed path under contracts/oxpd2/ outside hp/]` `0 != 1`, R1 tests GREEN. Mine on the
   realpath line: n1 `abspath` RED (`[link under another name]`); n2 `realpath(basename(folder))` RED (FAIL 4, every
   root subtest). Mine on the stat recorder: n3 `os.path.lexists` before the skip RED, n4 `os.stat(...).st_size` before
   the skip RED (each `stat of a key file`). Every red by assertion, 0 ERROR rows on the head's tests; control row (no
   change) GREEN both. `GATE B1850 MUTANTS: 8 counted, surviving on the head's tests 0`.
4. **F4: CLOSED; F5: CLOSED.** R1's tree with only the head's test file: rc 1, `Ran 60 tests`, `FAILED (failures=1)`,
   the one `FAIL: ... [link under another name]`, `AssertionError: R5 walked a supplied root that is a key folder:
   link under another name`, 0 ERROR; with the head's `repo_rules.py` copied in: `OK`. The docstring clause now reads
   "(the fingerprint list of HP's specification inputs)"; `git grep -i -E 'owner|agree|decid|ruling|approv|consent'`
   over both changed files at the head: 0 (control: R1 `build/repo_rules.py:24` `owner's agreement`). The kit's
   `words.py` (control `CONTROL FIRED: 13 of 13`) over the 47 added lines and the commit message: `WORDS: clean (2 files)`.
5. **NOTHING ELSE CHANGED: holds.** `python3 -I -m unittest discover -s build/tests -v` (Python 3.14.10): head
   `Ran 60 tests` `OK`, 0 FAIL/ERROR, `test_rules_job_is_the_reviewed_text ... ok`; R1 `Ran 60` `OK`; main `Ran 53` `OK`.
   Real folder, head's program (18:34:56 to 18:35:00), rc 0: `RULES-NOTE: R5 hashed 35210 files of the supplied
   source`, `skipped 4 key folders (contents not listed) and 0 key files by name`, `exempted 37 tracked files ...`
   (= `inputs.sha256` 37 lines), `RULES: clean (291 files)`; empty folder: hashed 0, skipped 0, exempted 0, clean;
   no folder: `R5 hash half NOT RUN`, clean. `r5_controls.py` (base 2229f68b): exempted 35, exactly three `RULES: R5`
   lines (the two swapped `openApi.bundle.json` and `docs/control.json`), `R5-CONTROLS: PASS`. Hosted, the kit's
   `hosted.py` by GET: run 44880248372, every job attempt 1, four check runs success, 0 beside them; linux and windows
   `total: 894` x2, failed 0, skipped 4 / 19, `0 Warning(s)`, `0 Error(s)`; rules `Ran 60 tests in` 1,
   `UNIT-TEST FLOOR: ran 60, floor 60` 1, `RULES: clean (291 files)` 1, K1 `... ok`; secret-scan both PLANTED-CONTROL
   lines, `no leaks found` x3; `HOSTED 2229f68bea9a873be01ced0eeda84803f4d66cf1: PASS`.
6. **THE MERGE WITH MAIN 0804860b: holds.** Branch ahead 2, behind 1 (merge base 5e36d8dc); main's one commit (pull
   request 7) changes 11 files, 0 under `build/` or `.github/`. `git merge-tree --write-tree 0804860b 2229f68b`: rc 0,
   tree `602ed3b601c915211f47be65ec1fa3a4b5b231a0` (rebuilt from `git archive` and `git add -A`: `write-tree` the same
   sha). Its `build` and `.github` trees equal the head's, its `contracts`, `src`, `tests` equal main's; vs main only the
   three branch files differ. On it: `python3 -I build/repo_rules.py <tree>` (no `--source-documents`): `R5 hash half
   NOT RUN`, `RULES: clean (293 files)`, rc 0; unit tests `Ran 60 tests` `OK`; CodeQL 0 + 0; and the head's program over
   it with the real folder: hashed 35210, skipped 4, exempted 37, `RULES: clean (293 files)`. Main 0804860b's push run
   44878961329 (GET): total 899 both legs, skipped 4 / 19, `RULES: clean (293 files)`, `Ran 53`, floor 53, three Analyze
   rows success: the pull request's merge run should read 899, 293, `Ran 60`, floor 60.
7. **THE DEVIATIONS (STATUS of kit B1844).** (1) a `builtin cd` in a discarded subshell during the tool-hash step:
   ACCEPTED, no effect (I re-hashed the ten tools: ten of ten equal to the kit's list); a breach of the shell rule, noted.
   (2) reads without `--no-optional-locks` in the seat's own clone: ACCEPTED, no effect. (3) one read-only check beyond
   the kit (`grep -i download` over the CLI logs): ACCEPTED. The seat's other claims re-measured true: READY sha, the two
   numstats, red-first one FAIL, CodeQL 0 and the R1 control 3 + 3, real-folder 35210/4/0/37, controls PASS, hosted PASS.
   The mutant table is the seat's own run (not re-run; mine above instead).
8. **TEXTS: written.** `pr-title.txt` (161 bytes), `pr-body.md`, `squash-subject.txt` (ends `(#PRNUM)`),
   `squash-body.txt` (ends `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`), `landing.txt`, `FOR-RECORDS.md`.
   `texts.py` (gate B1846's program, paths and the two branch commits changed): the workflow's own `neutral_export`
   cut by program from the head's `ci.yml` lines 120 to 128, each text stored as a scratch commit message, scanned with
   `--no-banner --redact --ignore-gitleaks-allow --exit-code 1`: title, title and body, body, squash message with a
   number, as written, squash body, the default squash shape (both commit messages), `landing.txt`: 8 of 8 export rc 0,
   stored whole, scan rc 0, `no leaks found`; planted control rc 1, `leaks found: 2`. Its word table: title, squash
   subject 0 in every class; pr-body and squash-body only the attribution footers (one host each, the footer emoji);
   controls 16 of 16. The project word scan `words.py` over title, squash subject, squash body without its attribution
   line and pr-body without its footer: `WORDS: clean (4 files)`; the squash body whole `WORDS: clean (1 files)`.
   `landing.txt` is an internal form and names people and gates by design. No text says the product owner decided
   anything about the code.

## NOT RUN
Anything on Windows (G3 is DERIVED); the runner as root; the seat's `mutants2.py` (mine instead); CodeQL for
`actions` or `csharp` locally; the hosted `Analyze` of this head (it runs on the pull request); any pull request,
merge-ref run, re-trigger or merge; a dotnet build of the merge tree (no C# changes on the branch; main's own push run
supplies 899). Nothing written outside `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1850_verify/`,
`/private/tmp/b1850-gate/` and the session scratchpad. No push, no pull request, no Jira, no message.
