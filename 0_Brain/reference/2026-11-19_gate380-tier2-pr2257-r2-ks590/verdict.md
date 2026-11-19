PR 2257: GO WITH NOTES (at head 73671cd50391e650e74b1b3005a11b989b646956; tier 2; round 2)

Gate 380, QA gate, Sonnet, 2026-11-19 ~20:2x AEDT. Delta only (f4c372d..73671cd). Findings only; nothing posted, merged, pushed, mailed or written outside this folder.
Pins by `gh api` (account kksecura verified) at the start and again before this verdict: PR 2257 head 73671cd50391 (open, not draft, base develop, 2 commits, 8 files), develop 06328efa1770 (unmoved).
Load gate: load1 read before every suite and mutant batch: 4.6 to 6.6, all under 8.
Venv used: the shared copy at `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-t25-stack/systemTest/schemathesis/venv` (python, ruff 0.17.1, mypy 2.4.0, pytest 9.1.1, schemathesis 4.32.1), run read-only with PYTHONDONTWRITEBYTECODE and `-p no:cacheprovider`, against my own worktrees in `scratch/`. No venv here meets the pins (ruff >=0.17.5, mypy >=2.4.1, schemathesis ==4.33.4); nothing installed.

## Q1 delta. MEASURED (`git diff --numstat f4c372d HEAD`): exactly 6 files, nothing else: the cheat and flow fragments (2/2, 1/1), `tests/support/verify_public_view.py` 101/13, `tests/test_verify_public_view.py` 11/5, `tests/unit/support/test_verify_public_view_drives.py` 39/0, NEW `tests/unit/support/test_verify_public_view_leaks.py` 203/0. (The "5 round-1 files" in the commission are the 5 round-1 test files; the integration file is unchanged, the two fragments are the other owned files.) The PR body carries a "Round 2 (gate 379 fix)" block (line 117 of the body I read), round 1's head still named; zero closing keywords (count 0). Title starts `Refs KS-590:`.

## Q2 G379-2257-1 FIXED. MEASURED (`scratch/leakprobe.py`, planted answers against `personal_data_violations`, forbidden map = email, local part `pat.example`, id `u-7c91ab`, numeric id `90417`):
Six required leaks, all CAUGHT:
- L1 embedded local part with punctuation, `Acme (c/o pat.example); Pty`
- L2 id inside a URL path, `https://x.test/api/users/u-7c91ab/profile?x=1`
- L3 id as a JSON number, `90417` (also L12 `90417.5`, L13 `Acme Pty #90417` caught)
- L4 email in mixed case in a sentence, `Contact Pat.Example@CORP.test for details`
- L5 local part at string start, `pat.example, Acme Pty`
- L6 local part at string end, `Acme Pty by pat.example`
Extra caught: id in a list of objects of lists (L7), local part joined by underscores (L8), upper-case local part (L11).
Three that must stay clean, all clean: a similar company name `Patterson Examples Pty`; digits adjacent to the number id (`1904173`); id prefix only (`u-7c91abx Pty`); also a normal company and bool/None values.
No leak that rule (b) says it should catch was missed. Two shapes outside rule (b) were missed, see findings.

## Q3 G379-2257-2 FIXED. MEASURED (`scratch/drive_q3.py`, `run_row4` over the unit tier's own MockTransport stand-in): `test_verify_public_view.py` line 187 `found = vpv.forbidden_map_violations(forbidden)` is the first statement of `run_row4`'s body, before the caller loop; the live row 4 cell (line 384) calls `run_row4(callers, doc, forbidden_for(...))`. Driven: empty map RED; blank-valued map RED; email-only RED (names missing local part and id); email+local part no id RED; id-only RED; empty map against a leaking platform RED with the map message FIRST; full map, clean platform GREEN (control, so the red is not blanket); full map with an embedded local part to every caller RED by label.

## Q4 G379-2257-3 FIXED. MEASURED: round 1's mutant o3 (list branch of the scan removed, one counted replacement) now fails 5 cells (numeric id in a list, and four U10 cells). Control: 106 passed on the unmutated head.

## Q5 mutants. MEASURED (`scratch/mut.sh`, one counted replacement each, unit files only: `test_verify_public_view.py`, `_drives.py`, `_leaks.py`; sha256 of both mutated files equal before and after, `git status` clean):
Builder's, reproduced: exact-equality (old `==` restored, under-4 branch forced on): 12 red (builder 12). Numbers not scanned: 5 (builder 5). Row 4 body not calling the map check: 2 (builder 2). Ids and local part as plain substrings (`_TOKEN_LABEL` branch off): 5 red; the builder's own "ids as substrings" figure was 3 for a differently-aimed replacement, so this is a different mutant, killed, not a mismatch. o3: 5 (above).
Mine: MIN_FRAGMENT 4 to 5: 2 red. Floats not scanned (`int | float` to `int`): 1 red (the float cell alone). Email matched by equality instead of substring: 2 red. Map check no longer requiring an id label: 2 red. All killed, none survived.

## Q6 unit+functional tier. MEASURED (`scratch/tier.sh`; `pytest tests/unit/ tests/functional/ -q -rfE --continue-on-collection-errors`, load1 4.6 to 6.0, three trees):
- develop 06328efa: 44 failed, 4437 passed, 4 skipped, 65 errors
- round 1 head f4c372d: 44 failed, 4506 passed, 4 skipped, 65 errors (+69 over develop)
- this head 73671cd: 44 failed, 4543 passed, 4 skipped, 65 errors (+37 over round 1)
The sorted failed/error id lists (109 each) are IDENTICAL across all three (three diffs empty). Control: a copy of the head's list with one line dropped printed a diff. My 44/109 versus the builder's 43/108 is the one load-flaky id I also saw at round 1; identical on all three trees, so the difference is unaffected. The red set is venv-dependent (schemathesis 4.32.1 import errors, parity tripwire); only the difference is claimed.

## Q7 lint. MEASURED (`scratch/lint.sh`, 6 py files incl. the unchanged integration file): `ruff format --check` 6 already formatted; `ruff check` all passed; mypy (`--ignore-missing-imports --explicit-package-bases`) no issues in 6 files. Planted controls fired: ruff F841 (1 error), ruff format on an unformatted file (rc 1), mypy return-value (1 error). Versions are the venv's, below the repo pins. mypy on tests/ is an extra, not the repo's own gate.

## Q8 merge-tree. MEASURED: develop+pr2257 and pr2257+develop both rc 0, same tree 302037915322. Planted-conflict control (a commit on round 1's head editing the renamed `_strings` line): rc 1, one CONFLICT line in `verify_public_view.py`.

## Findings
- G380-2257-1 LOW (pre-existing, not a round 2 regression, outside rule (b)): `_scalar_texts` skips the key `title` at ANY depth, so a person value under a nested `title` key (probe L9: `history[0].title = "u-7c91ab"`) is never scanned. Top-level `title` as open text is Kam's ruling; nested is the same skip applied further than the ruling reaches. Fix: skip only the answer's own `title`, or say it in the deliberate non-assertions.
- G380-2257-2 LOW (pre-existing, outside rule (b)): dict KEYS are never scanned (probe L10: `{"pat.example": "x"}` passes). No known platform field carries a person value as a key; record it beside the non-assertions or add a key scan.
- G380-2257-3 INFO: the stated gap holds as designed: a letter-glued local part (`xjane.doe`) is not caught; pinned by a cell with Wednesday's sentence beside it (read in `test_u9_a_letter_glued_local_part_is_not_caught_by_design`, and it reds under my substring mutant). The builder's note that a super-admin token with no id claim will red the live row 4 cell is a harness fact, live NOT RUN.
- G379-2257-4 (the other-tenant caller is the super-admin under the override header) was out of scope and is unchanged; carried, not re-graded.
Why GO WITH NOTES, not NO GO: all three round 1 findings are fixed and reproduced by me, with the delta confined to the 6 owned files, no leak of the rule (b) kind missed, tier and lint clean, merge clean. The two LOW notes sit outside the ruling and pre-date this commit.

## Plainly: every live cell is NOT RUN (L2 to L5, row 1, the live bodies of rows 2 to 5). The MockTransport drives only show that predicates and bodies can fail and pass; whether the platform answers as the stand-in does is unmeasured. Whether two registrations can share a content_hash through the public API stays UNMEASURED.

## NOT COVERED
Every live cell; row 1 on a real-anchoring target; the package `quality` command and 90% coverage gate; `docs-fragments.mjs check` and the fragment edits' content (only the numstat and file list read); the builder's 19 mutants beyond the 4 reproduced plus the o3 re-run (5 of 19 builder-named, plus 3 of mine counted separately above); the PR-overlap census (33 open PRs) and the pre-push hook silence (builder's, not measured); the 400-logical-line cap not re-counted; `ruff`/`mypy` not at repo pins; the 109-id red set is venv-dependent.
