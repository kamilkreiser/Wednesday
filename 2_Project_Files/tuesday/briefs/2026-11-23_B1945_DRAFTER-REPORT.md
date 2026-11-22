STARTABLE: YES

# B1945 DRAFTER REPORT: lane F3 (seat Datasec/OXPd2-X41), OXPd 2 overnight wave 4

Drafter: Opus, read-only, in-session for Tuesday (s313). Drafted 2026-11-23 02:58 to 03:24 AEDT (clock by `date`: 02:58:35, 03:15:10, 03:16:02, 03:23:50). Kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1945_SEAT-X41_oxpd2-f3.md`, its sidecar `.measured` beside it (`stamp_check.py <kit>`: 164 claims, 164 measured, exit 0), scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s313/d1945/` (the tools in `gate/`, twelve files).

## BLUF
- Both owed README lines CAN be stated truthfully without a code change; no Question of the "needs code" kind arises. Two README files changed (+13 -5), two NEW test files (one cell each), no `.cs` under `src/`.
- (a) Data README `SavedChanges` line: a handler that catches hides the refusal from the caller of that save; the entry stays `Modified`; the next save on that context refuses it before anything of that save is written. Cell `AuditSavedChangesLimitTests.C15_limit_asserted_..._next_save_refuses_the_change` (gate B1939's P8 shape) GREEN at main, RED under `mNoStateChanged` (Data 65 / 8) and `mNoPreCheckAsync` (65 / 2).
- (b) Universal Print README: one new sentence saying "registration" is the call's own (after `Remove(id)` a later `GetAsync(id)` is a new registration), and a Limits sentence naming one token object answered to two calls for one id across a `Remove(id)`, in time or after the bound. Cell `CloudDeviceTokenHolderLimitTests.L01_...` (gate B1943's H15b and an H15a-like shape) GREEN at main, RED under `mRemovedKeepsAnswer` (UP 349 / 2: L01, T08) and `mLateKeepsAll` (349 / 3: L01, T06 late, T11).
- Totals MEASURED (macOS arm64): whole solution 1759 -> `total: 1761`, `succeeded: 1757`, `skipped: 4`; `RULES: clean (553 files)` (551 + 2 new files); `Ran 111 tests`; GUARD 10 / 11. PREDICTED hosted: `--total 1761 --rules 553 --skipped-linux 4 --skipped-windows 21`.

## FACTS RE-MEASURED (instrument, control)
- Origin (`gh api -X GET`, project GH_CONFIG_DIR, 03:12 and 03:20): main `394fa997826e3d102fafa6a0c05a4847132cb01a`; PRs 28..24 closed, none open; `matching-refs/heads/b1945` 0 (control `heads/b193` 3); `.private` true, `.permissions.push` true.
- main's push run: `hosted2.py 394fa997... --total 1759 --rules 551 --skipped-linux 4 --skipped-windows 21 --unit 111 --floor 111 --hardened-scan` -> `HOSTED 394fa997...: PASS` (linux succeeded 1755, windows 1738; Analyze rows success).
- BASE (new files moved out): Data `Total: 64`, UP `Total: 348`, both Failed 0; with the cells 65 / 349, Failed 0; 10-run loops of each executable `LOOP: 10 of 10 passed, 0 failed`.
- Lock files: 28 tracked (not 26 as in kit B1936: two landings added two); `restore --force` left all 28 byte for byte (`cmp` rc=0).
- `f3_checks.py`: ASCII/no tab/0 CR/final LF on the four files (control U+200B -> 1); `-- src` lists only the two READMEs, no `.cs` (control planted `.cs` row fails); name-status = the four owned rows (control fails). `CHECKS: PASS, every control FIRED`.
- gitleaks 8.30.1: control (token from two halves + 36 random chars) `leaks found: 1` exit 1, quarantined; the 8 neutral files and the clone `no leaks found`. `words.py`: control `CONTROL FIRED: 13 of 13`; the 127 added lines and the message `WORDS: clean (2 files)`.
- Patches applied byte for byte to a fresh clone (`clone2`): the four sha256 equal; a second `apply --check` refused for both patches.
- CLARIFICATIONS.md (89379 bytes) and the 2026-11-22 rulings (wave-3 commission line 9): this lane's subject words 0 (`SavedChanges`, `catches`, `next save`, `Remove(`, `token object`, `two registrations`, `cleared bytes`, ...); `named limit` 4, all in C-67 (CI guards, not this lane); control `tolerant` 7 and 2.

## CHAIN INPUTS (each step's inputs exist at BASE or come from an earlier step)
| Step | Inputs | Produced by or present at |
|---|---|---|
| 0 | the kit, Stamp slots (S4: Q1, Q3 in words) | Tuesday's stamp |
| 1 | `<src>` (12 files); `<repo>` local values; origin | drafter scratch (exists); `<repo>`; GitHub |
| 2 | BASE files | `<clone>` (Step 1) |
| 3 | `1-cells.diff`; baseline build | Step 1 |
| 4 | cells tree; `mutants_f3.py`; `loop.sh` | Step 3; Step 1 |
| 5 | tree with mutants undone and rebuilt; `2-readmes.diff`; lock hashes | Step 4; Step 1 |
| 6 | staged tree; `f3_checks.py`, `added.py`, `words.py`, `commit-message.txt` | Step 5 + its `git add`; Step 1 |
| 7 | the commit; `origin/main`; `run_step.py`, `hosted2.py` | Step 7a; fetch 7b; Step 1 |
Note: `repo_rules.py` judges `git ls-files`, so the kit runs it only after Step 6's `git add` (553); before the add it counts 551.

## D-DECISIONS (Tuesday's as coordinator, defaults in the kit)
- D1: the `SavedChanges` line names the catching handler; code paths named (`SuiteDbContext.cs:206` watch, pre-check `:95` sync and `:110` async; cell covers async via `Audit.cs:186`); interceptor step "read from the code and not asserted".
- D2: "registration" kept as the per-call entry and SAID; the gate's literal sketch (read "registration" as the id) would make `:105` FALSE without code (L01 measures the old call disposing the object the id now holds). Dispose sites censused by `grep -n -i 'Dispose()'` (`:159 :217 :240 :292 :330 :334`, plus `Dispose()` `:188`).
- D3: one cell per new file, per the commission's partition. D4: the cells' reds are their mutants'. D5: one commit, new branch `b1945/f3-readme-limits`.

## Q-QUESTIONS FOR TUESDAY (each with its default)
- Q1 (STOP-CLASS): default a, the named limit plus cell, no product change; alternative b, a latch (product change, G1).
- Q2: default, interceptor `SavedChanges` step named as read-from-code; alternative, a second cell (+1).
- Q3 (STOP-CLASS): default a, "registration" said as the call's own plus the Limits sentence plus L01; b (the gate's literal sketch) judged false without code; c a cross-entry refusal (not built).
- **Q4: the commission says "Sonnet gate" for G2, but `<project>/CLAUDE.md:7` says every agent on this project runs on the newest Opus (the product owner's word of 2026-11-21). Kit default: the G2 gate on Opus. Tuesday to confirm.**
- Q5: READY at Step 0 + 120, push by Step 0 + 90, pane X41, 40 min of lock waits; hard stop before 09:00 (S7 to fill).

## UNMEASURED / NEVER RUN
- Nothing ran on Linux or Windows; the two cells' hosted results are PREDICTED (windows skipped 21, succeeded 1740).
- NEVER RUN by the drafter: `clone.py seat`, the commit and its identity read, `run_step.py` neutral scan (its wordings were read in main's hosted log), the push, `hosted2.py` on a lane head.
- H2 (the synchronous next save), H3 (an interceptor's `SavedChanges` step that catches), H4, H8, H10: DERIVED from source only; the kit says so and asks the gate to probe H3 and H8.
- That EF Core routes its other `SaveChanges` overloads through the two overrides: EF Core behaviour, UNMEASURED.

## OUTSIDE-THE-FENCES DISCLOSURE
- Wrote only: the kit, its sidecar, this report, and files under my scratch `s313/d1945/` (two scratch clones made by `clone.py ... draft`, push URL `invalid://no-push`; a `git add` of the four paths in my own scratch clone, no commit; logs; quarantine). Nothing written to the OXPd project, `<repo>`, any `.tools/b*` lane, GitHub or Jira; no push, no PR; no `cd`; nothing deleted (the scanner control was moved to `d1945/_quarantine/glctl`).
- Every dotnet job and test executable went through `heavy.py` and the shared wave lock, one at a time; lock waits 0 to 7; no other holder's lock touched.
- Network: `gh api -X GET` only (repo, ref, pulls, matching-refs, and `hosted2.py`'s reads of main's run); `git clone` of the origin twice.
- Not every Bash call was one simple command: several carried `; echo "rc=$?"` (because the pane showed no error mark for a `git diff --quiet` that returned 1, which the kit now tells the seat), a few were pipelines (`git show ... | shasum`, `ls ... | grep -c`, `sed ... | grep`), and one heredoc ran a python edit of my own scratch `fill.py`. None removed anything. One `grep --include=*.cs` was refused by zsh's glob and re-run quoted.
- Not read: `Source_Documents/`, any key folder, the NAS library, any sibling project, `fleet/briefs_staged/`, the ledger, the other two lanes' kits or scratch (I listed `fleet/state/s313/` and saw `d1944`, `d1946` exist; I did not open them).
