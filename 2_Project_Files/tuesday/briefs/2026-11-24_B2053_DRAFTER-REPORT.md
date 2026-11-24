STARTABLE: YES

# B2053 DRAFTER REPORT (Opus, in-session, read-only): OXPd lane L1 round 2, the fix lane for gate B2052's FOUND 1 to 3, seat X65

Kit: `tuesday/briefs/2026-11-24_B2053_SEAT-X65_oxpd2-l1-round2-found-1-3.md` (sidecar `.measured`: 214 claims, `stamp_check.py` rc 0 at 19:03:43). Tools: `fleet/state/s323/d2053/seat-tools/` (10 files). Scratch: `fleet/state/s323/d2053/` only. Drafted from 18:14:49 to 19:03:43 AEDT. The work stopped at about 18:4x when the account hit its limit and resumed after the coordinator's message at about 18:51. OXPd main was measured again after the restart: still `89a10a1b` at 18:51:07 and 19:02:49.

## BLUF
- One new branch `b2053/l1-round2-found-1-3` cut from main `89a10a1ba26a16aae7996e059d548bf53531fd44` (PR 47's squash). It changes nine existing files, all inside L1's four folders: six under `src/`, three under `tests/`. No file is added, and there is no project, lock, workflow or contracts line.
- **FOUND 1** is closed in the client. Catalogue rows get a new `TextOnly` flag, set for `IsServiceEnabled` only. With the flag on, `Oxpd1Soap.ReadAnswer` returns `MalformedAnswer` in three cases: the response holds any other element, `enabled` has a child element, or `enabled` has an attribute that is not a namespace declaration (so `xsi:nil` is refused). The lab then takes its existing "did not answer" path: exit 8, no write. The fix cannot go in the lab alone: the lab only sees the client's masked copy of `enabled`, which has no parent element, so it cannot see siblings.
- **FOUND 2** is closed in the lab. `RunFolderRule.GitWorkTreeHolding` first walks the path as written (as before), then walks `RealPath`, which resolves symbolic links (at most 40). The rule lives in `LabFiles.cs`, inside the lane, so the commission's widening Question does not arise. It covers the read, write and lab-cert verbs.
- **FOUND 3** is closed in the lab. `ScreenCapture.Save` now takes the password and saves nothing when the decoded bytes contain its UTF-8 bytes (exit 8). The README now says that the client's log `oxpd1-client.log` still holds the base64 text of such an answer.
- **Cells:** 4 new cells with 18 cases (T07 has 8 rows, S13 4, S14 4, S15 2). Red first on BASE: 4 failures in the adapter tests and 8 in the Lab tests, each an `Assert.Equal` failure. Green: 2171 total, 0 failed, 2167 succeeded, 4 skipped. All 10 mutants match their expected cells (`MUTANTS: 10 of 10 MATCH, 10 of 10 undone equal`).

## FACTS RE-MEASURED (instrument, control)
1. Origin, read with `gh api -X GET` at 18:14:58, 18:30:29, 18:51:07 and 19:02:49: main is `89a10a1b`; 0 open pull requests; `matching-refs/heads/b2053` has 0 rows (control: `heads/b2048` has 1 row). Pull requests 47 to 43 are all merged.
2. BASE hosted run (`hosted3.py`, 18:28:45): `--total 2153 --rules 659`, skipped 4 and 21, guards 14 and 15; linux succeeded 2149, windows succeeded 2132; `HOSTED 89a10a1b...: PASS`.
3. Gate pointers re-printed at BASE: `Oxpd1Command.cs:888`, `Oxpd1Soap.cs:165`-`:166`, `LabFiles.cs:76` (walk), `:96` ("never committed"), `:110`/`:126` (decode, write), README `:20`, `:37`, `:91`, `:139`, `:167`, adapter README `:42`. All match the VERDICT.
4. THE CODE's BASE sha256 for the six landed `src/` files and three test files equals kit B2048's "After both" column. That ties BASE to the reviewed tree.
5. Seat id: a word scan of the last week's non-`.pre-` SEAT kits (211 files, 11-17 to 11-24) finds `X65` in 0 files; control `X63` in 2 and `X64` in 3. The lane folder `.tools/b2053` is absent and no `b2053` branch exists.
6. Red (`clone2`, BASE + `1-red.diff`): adapter tests `Total: 55, Errors: 0, Failed: 4`, Lab tests `Total: 229, Errors: 0, Failed: 8`. There are 12 `[FAIL]` lines, each followed by an `Assert.Equal() Failure` line (12 of 12).
7. Green, after the mutants, and in THE CHAIN: 2171 total, 0 failed (twice); `locks equal 34 of 34`; `GUARD: clean (14 files)` and `(15 files)`, with 0 Lab or Tests names in either; `Ran 111 tests` OK; `RULES: clean (659 files)` (run without `--source-documents`); `CHECKS: 10 of 10 PASS`, every control fired; numstat matches the kit; 246 added lines; 4 public lines (the test methods).
8. Scans: `words.py --control` gives `CONTROL FIRED: 13 of 13`. Over the added lines and the message: `WORDS: clean (2 files)`. Before that, the first subject's words "round 2" were counted under finding or round numbers, so the subject was reworded; the patches were not touched. `B2[0-9]{3}` count: 0 and 0. Gitleaks 8.30.1: control rc 1; `dir` over the clone and 14 neutral copies: `no leaks found`.
9. Lock and load: 81 heavy jobs, every one `after 0 waits`; load1 ran from 1.07 to 26.5 with the other drafters building.

## DECISIONS (D1 to D7 in the kit, each a Question)
D1: fix FOUND 1 in the client with the `TextOnly` row flag. D2: the lab keeps its existing words and exit for it. D3: walk the path as written first, then the real path; this leaves the existing cell R07's printed path unchanged (macOS `/var` is a link to `/private/var`). D4: refuse, don't scrub (the commission's default); search for UTF-8 bytes only. D5: the four cells and one stub hook; S14 returns at once on Windows, following the Lab's existing cell Y05 (`HygieneTests.cs:149`). D6: no FOUND 4 cells and no FOUND 9 text. D7: one commit, pushed by sha; local CodeQL cannot run.

## QUESTIONS FOR TUESDAY (each with its default; Q1 and Q2 must be answered in words at the stamp)
- Q1: where FOUND 1 is fixed. Default **a**: the client row flag, `IsServiceEnabled` only. Alternatives: b, the lab only (would need the raw response); c, also flag `GetScreenCapture`.
- Q2: FOUND 3. Default **a**: refuse on the password's UTF-8 bytes. Alternatives: b, also refuse on the Basic and UTF-16 forms; c, a Limits sentence only.
- Q3: default, the path as written first, then the real path. Alternative: real path only, which moves R07's printed path, a landed literal.
- Q4: default, S14 returns on Windows. Alternatives: try the link and print NOT RUN if refused (the LogScanner form), or no guard (whether the hosted Windows runner can make links is UNMEASURED).
- Q5: default, the client's log keeping the base64 of a capture that holds the password is a named limit only. Alternative: a client change to the record rule.
- Q6: default, no FOUND 4 cells or FOUND 9 text. Alternative: add them.
- Q7: default, the kit's commit subject (342 characters). Q8: default, no local CodeQL. Q9: default, Opus, READY by Step 0 + 120 minutes, push by Step 0 + 90, pane X65, gate G1 round 2 of 2.

## CHAIN INPUTS (DRAFTER_RULES MEASURED LITERALS 4)
| Step | Inputs | Produced by or present at |
|---|---|---|
| 0 | kit, Stamp slots | Tuesday's stamp |
| 1 | `<src>` (10 files), `<repo>` local values, origin, BASE run | the drafter's scratch, `<repo>`, GitHub (all exist) |
| 2 | files at BASE | Step 1 clone |
| 3 | `1-red.diff`, clone at BASE | Step 1 |
| 4 | `2-fix.diff`, `mutants_r2.py`, red tree built | Step 1, Step 3 |
| 5 | green tree, mutants undone and rebuilt | Step 4 |
| 6 | staged tree, `checks_r2.py`, `words.py`, message | Step 5, Step 1 |
| 7 | commit, `origin/main`, `run_step.py`, `hosted3.py` | Step 7a, the fetch, Step 1 |

## DEVIATIONS IN THE DRAFTING (said, not hidden)
- The first full mutant run printed `8 of 10 MATCH`. Its output and keep folder are moved to `d2053/_quarantine/mutants-run1/`.
  - `mCommentRefused` survived as an EQUIVALENT mutant: the existing parser drops comments before `ReadAnswer` runs (`Oxpd1Soap.cs:99`, `IgnoreComments = true`). It was replaced by `mCDataRefused`.
  - `mLastLinkOnly` threw on a run folder that does not exist yet and reddened 78 cases. It was rewritten to resolve only when the folder exists.
  - The tool was then frozen and all 10 rows run again: `10 of 10 MATCH`. The kit cites only the frozen run.
- `chain.py`'s first `words.py` call failed because the five shared tools had not yet been copied into `seat-tools`. They were copied (byte-equal to kit B2048's) and words was run alone.

## UNMEASURED
Windows and Linux behaviour of every new cell (macOS arm64 only; PREDICTED hosted totals 2171, linux succeeded 2167, windows 2150); whether a GitHub Windows runner can make directory links; whether any device puts the password in its panel image; whether the M577 answers `IsServiceEnabled` in HP's shape; CodeQL (cannot run on this Mac). `run_step.py`'s neutral scan, the push, the read-back and the rebase are NEVER RUN (they need the seat's commit). `ls-remote` was not run by the drafter (no deploy key in its shell); the `gh` matching-refs read stands in for it.

## OUTSIDE THE FENCES (disclosure)
- No write to any project file, the project checkout, GitHub, Jira, a card store or a STATUS. Every `git apply`, build and mutant ran in `d2053/clone` and `d2053/clone2`, both made by `clone.py draft` (push URL `invalid://no-push`, no identity). `git write-tree` (inside `checks_r2.py`) wrote objects only into `clone2`.
- The heavy jobs took the shared wave lock `<project>/.tools/wave1-heavy.lock.d` through `heavy.py`, as kits B2048 and B2052 do. That is a mkdir and move of the lock folder in the project's `.tools`; each release went to `d2053/_quarantine/locks/`. No other holder's lock was touched.
- `gh` was used with `-X GET` only, under the project's `GH_CONFIG_DIR`. No HTTP to any other host; no printer, device, Azure or person; nothing deleted (quarantine only); no `cd`; nothing of another client. No card was read.
- I wrote only the kit, its sidecar, this report and files in my scratch.
