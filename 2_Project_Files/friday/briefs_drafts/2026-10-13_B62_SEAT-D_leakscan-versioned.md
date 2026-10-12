From Friday (laptop seat), Datasec / MPS Commercial Calculator. No mail key in this project: the STATUS file is the wrap.
# BRIEF B62 · SEAT-D: version the per-seat leak scanner as `tools/leakscan/` with a test (Friday's ruling M3), one branch, CodeQL PR route
**Fired: 2026-10-13 03:52 AEDT.** Pane `Datasec/MPS-D`. Your commission is THIS file, at `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/briefs_drafts/2026-10-13_B62_SEAT-D_leakscan-versioned.md` (Friday's tree, read-only to you). Step 0: copy it into your `1_Project_Definition/Briefs/` unchanged, as the project's record. QA tier 3 (docs/scripts lane; Friday reviews the diff). Round 1. The last SEAT-D seat, B53, is finished and merged (PR #29).

## Why (Friday's ruling, verbatim)
`FRIDAY/0_Brain/reference/2026-10-12_datasec-decisions-pack/friday-calls-proposed.md` row **M3**, ruled AS PROPOSED in `friday-calls-RULED.md` (03:38 AEDT): *"RULE-OTHER: version it as `tools/leakscan/` plus a test, in the code repo, through a CodeQL PR."* Reason given: *"It holds no confidential values (it reads the git-ignored avoid lists by path). Rebuilt copies have already had a blind spot (B05)."* BACKLOG row: records `main:BACKLOG.md:162` ("The leak scanner is not versioned, and has been rebuilt from scratch twice").

## Pins (measured by the drafter, read verbs only, 03:4x AEDT)
- Code main = **`d711b42cfcb53da3a2043a2d672511f8ea6ea296`** (GitHub commits API via `friday_as.sh datasec gh api`, 03:43; "Source version store hardening (B53 …) (#29)"); present in the local clone (`cat-file -t` = commit). `ls-tree -r d711b42c` = **342** paths; **0** match `leak` or `scan` (case-insensitive); `tools/` holds `MpsCalc.ImportCli/`, `demo/` (seed + `demo/test/test_*.py`), `replica/`.
- Seat copies in the project's `.tools/` (outside the repo): `qa-B57`, `qa-B58`, `qa-B59` each hold `tools/leakscan.py` (116 lines in qa-B58) with **sha256 `71a7a64e…` identical in all three**, plus `qalib.py` (147 lines in qa-B58) and a per-round wrapper (`leak57.py`, `leak58.py` 87 lines, `leak59.py`). Inputs, read from the code only (no list opened): `leakscan.py` reads `os.environ["P"]` (`:14`) and `qalib.avoid_values()` (`:37`); its credential reader is disabled in the B54 copy (`:32`, "The brief forbids opening 4_Credentials/.env"); `leak58.py` reads `os.environ["Q"]` and `ex_numbers.txt`, `ex_terms.tsv`, `ex_sentences.txt`, `ex_countphr.txt` from a list directory by path (`:10-17`).
- Open PRs on the code repo: **0** (GitHub pulls API, 03:43). Live seats: **MPS-B** (B60, `b60/feedback-pill-on-d711b42`) and **MPS-E** (B59, gate of `b58/gate-b57-overlay-fix-round`). Neither touches `tools/`.

## Do
0. In `2_Project_Files`: `git fetch origin`; `ls-remote origin refs/heads/main` must read `d711b42c…` (or a later main: say which, and re-check that `tools/leakscan/` is still absent). No `b62` worktree exists yet.
1. Worktree `.tools/wt-B62` on new branch **`b62/leakscan-versioned`** from origin main.
2. Build `tools/leakscan/` from the newest seat copies (qa-B58/B59 `leakscan.py` + `qalib.py` + the wrapper's extra classes), stdlib Python only:
   - **No list, value, SKU, term, sentence or secret goes into the repo.** Every list is read at run time from a path given by an environment variable or argument (keep `P`/`Q` or name them clearly), and the tool fails loudly (non-zero, one line) when a list path is missing; it never falls back to an empty list silently.
   - Modes the seats use: scan a git range (`repo base head label`) over added lines, and scan files. Output = counts per class only; never print a matched value.
   - Fix the known blind spot class (B05: C# `1234.56m` literals; an integer part read alone) and keep the `package-lock.json` number exemption the copies have.
   - A `README.md` in `tools/leakscan/`: usage, the env vars, "counts only, never print a list".
3. Tests in `tools/leakscan/test/` (the `tools/demo/test/` style), on **synthetic fixtures created inside the test** (never a real list): every class has a positive control that fires and a clean control that stays 0; the `1234.56m` case fires; a missing list path exits non-zero; output contains no fixture value (assert it).
4. Prove: the test suite's counts (base: 0 tests in `tools/leakscan/`; head: N/N); run the new tool and the qa-B58 copy over the same range (`git diff d711b42c~1..d711b42c` or a range you name) with the same lists: **class counts equal** (name any difference and why). `git diff --stat` touches only `tools/leakscan/**`.
5. Push the branch only (`git push -u origin b62/leakscan-versioned`), read back with `ls-remote`. Friday opens the PR; CodeQL (python) and CI run on it.
6. Records: write nothing in records; name in the STATUS that `BACKLOG.md:162` is owed a closing line by the records seat once merged.
7. Write `Briefs/2026-10-13_B62_STATUS.md`: files, test counts, the equal-counts comparison (counts only), ls-remote line. Last line `READY FOR REVIEW: b62/leakscan-versioned <sha>` or `STOPPED: NEEDS FRIDAY`.

## HOLDS
- **Datasec only.** No other client's names, tickets or paths.
- **Never read `4_Credentials/.env`**; never copy any avoid list, value or real line into code, tests, commit messages or the STATUS. Your own self-scan of the diff and STATUS uses the new tool AND the qa-B58 copy, plus `gitleaks` with a planted canary.
- Paths: `tools/leakscan/**` only. Not `src/`, `web/`, `tests/`, `.github/` (a workflow edit is out of scope), not `Proposal.cs` (M5 waits for the one-pager lane F3).
- Builds (if any): `-nodeReuse:false -p:UseSharedCompilation=false`; never `dotnet build-server shutdown` (other seats are live). No ports needed: bind nothing.
- No PR, no merge, no deploy, no Jira, no history.md, never delete, never force-push, never dismiss a CodeQL alert.
