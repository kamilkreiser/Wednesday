STARTABLE: YES

# B1915 ANSWER-1 DRAFTER REPORT: C14 red on the hosted Windows leg; the issuer window on the library's clock

Drafter d1915a1 (Opus, in-session, read-only toward OXPd_2, its lane, GitHub and Jira) for Tuesday s311, on `2026-11-22_B1915_ANSWER-1_DRAFTER_COMMISSION.md`.
- Answer: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1915_ANSWER-1_issuer-window-on-library-clock.md` (19.9 kB).
- Scratch (`<a1>`): `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s311/d1915a1/`. It holds:
  - `3-fix.patch`, `commit-message-2.txt` and `gate/mutants_a1.py`, the seat's three new tools;
  - `clone`, `clone2` and `clone3`, local clones of the seat's pushed head `759c9060` with push URL `invalid://no-push`;
  - `logs/`, `probes/ProbeA1.cs`, `stampcheck/` (the answer's sidecar: 41 of 41 measured, `stamp_check.py` rc 0), `main4a0a/job-rules.log`, and `_quarantine/`.
- Every dotnet job went through the kit's `heavy.py` (sha256 equal to THE TOOLS) and the wave lock. Load at the jobs was 3.6 to 6.8 load1, and one job waited for load 8.05.

## BLUF
- **The rule (option (a), as Tuesday decided).** After the chain builds with every status flag clear, every element of the chain must lie inside its own `NotBefore` to `NotAfter` at the library's `now`. That covers the leaf, the configured issuer and any further element. Both ends are included, in UTC. Otherwise the reason is `IssuerNotTrusted`. There is no new reason and no public member. The new code is a 7-line loop plus a `private static InsideWindow`. The full diff of `RegistrationKeys.cs` is 27 lines added and 2 removed, with comments.
- **Why Windows accepted C14 is UNMEASURED.** The code and the log show what happened: `Build` was true, every status flag was clear, and nothing was thrown at `CertificateRuleTests.cs:406`. Two readings fit, and only a Windows run can tell them apart:
  - (i) the Windows chain did not test the custom root's window at `VerificationTime`;
  - (ii) the Windows chain ignored `VerificationTime` and judged on the real clock.
  The drafter did not guess between them.
- **One cell is added: C16.** A chain inside its windows by the library's clock but expired by the real clock must be ACCEPTED.
  - **Why it is needed (MEASURED):** with the rule alone, the kit's item-54 mutants `mTimeIgnored` and `mVerifySystemClock` both turn GREEN, so C14 no longer kills them. C16 kills both on macOS.
  - On hosted Windows, C16 is also the instrument that tells (i) from (ii).
  - Totals rise by one: UniversalPrint 346, whole solution 1587.
- **macOS with the patch (MEASURED):**
  - whole solution: `total: 1587`, `failed: 0`, `succeeded: 1583`, `skipped: 4`, measured twice (`<a1>/clone`, and `<a1>/clone3` from a fresh apply);
  - build: `0 Warning(s)`, `0 Error(s)`;
  - C14 and C16: 100 of 100 each;
  - `RULES: clean (500 files)`, and `Ran 111 tests` OK;
  - 14 mutants, every `undo cmp 0`.
- **An honest proof:**
  - No local red-first exists, because macOS refuses the expired issuer by itself. The rule's own mutants (`mWindowRuleOff`, `mWindowNotAfterOff`) stay GREEN on macOS.
  - The red-first is C14 RED on hosted Windows at `759c9060` (run 45011414586). The proof is C14 GREEN on the Windows leg of the next push.
- **Main's move to `4a0a9717` is harmless (MEASURED at 21:26).** `compare 4e8828ee...4a0a9717` is ahead 1 and behind 0, and touches only `build/repo_rules.py`, `build/tests/test_repo_rules.py` and `packaging/linux/Dockerfile`. None of them is under `Registration/`. Main's push `rules` job still reads `Ran 111 tests`, `UNIT-TEST FLOOR: ran 111, floor 111` and `RULES: clean (500 files)`.
- **The seat's steps:** ONE fast-forward commit on `759c9060`, with no rebase. The kit's `merge-base --is-ancestor origin/main HEAD` now gives rc 1 by design. The answer replaces it with `merge-base` = `4e8828ee` plus the compare above. Then hosted2 runs with `--total 1587`.

## FACTS RE-MEASURED (instrument, then control)

| Fact | Instrument | Result | Control |
|---|---|---|---|
| The seat's head | `gh api -X GET matching-refs/heads/b1915` (21:26); `<lane>/clone` `rev-parse` and `status` (read-only) | one row, `759c90609e9a8a71aa4bbef32a8d13f2d1682d77`; status 0 lines (21:41 again) | `<a1>/clone` `rev-parse HEAD`, same sha |
| main | `gh api -X GET git/ref/heads/main` | `4a0a9717277f60647dfc174e60ec04fc7008e615` | the compare below |
| main's move | `gh api -X GET compare/4e8828ee...4a0a9717` | ahead 1, behind 0, the 3 files above | none under `Registration/` |
| main's rules floor | the log of `rules` job 137175783996 at `4a0a9717` (GET with `--allow-escape-sequences`) | `Ran 111 tests`, `UNIT-TEST FLOOR: ran 111, floor 111`, `RULES: clean (500 files)` | all 7 check runs of `4a0a9717` read success |
| The Windows red | `<lane>/logs/hosted/job-windows.log:245-249`, image at `:17` | C14 at `:406`, "nothing was thrown"; `windows-2025-vs2026` | the other new cells were green there (seat STATUS, RELAYED) |
| Baseline at `759c9060`, macOS | the UniversalPrint executable via heavy | `Total: 345, Errors: 0, Failed: 0` | - |
| C16 without the rule (the test hunk only, on `759c9060` product) | `<a1>/clone2` | `Total: 346`, `Failed: 0`: C16 does not depend on the rule; it measures the platform | - |
| The rule without C16 | `mutants.py mTimeIgnored mVerifySystemClock` on `<a1>/clone` | both `RED none: GREEN` | with C16 present, both `RED C16` |
| The patch applies | `git apply --check` and then `apply` on `<a1>/clone3` (fresh clone of `759c9060`) | rc 0, rc 0; the 3 files `cmp`-equal to `<a1>/clone`'s | a second `--check` gives rc 1 |
| Whole solution with the patch | `dotnet test -c Release --no-build` via heavy, `<a1>/clone3` (fresh locked restore and build) | 1587 / 0 / 1583 / 4; `failed Datasec` 0 | the seat's `red-test.log` reads 4 |
| Words | `words.py` (kit copy) over 81 added lines and `commit-message-2.txt` | `WORDS: clean (2 files)` | `--control`: `CONTROL FIRED: 13 of 13` |
| Secrets | `gitleaks dir` over neutral copies of the patch, the message and the 3 files | rc 0, `no leaks found` | a planted two-half token: rc 1, `leaks found: 1`, quarantined |
| ASCII | `LC_ALL=C grep -c -v -x -E '[ -~]*'` on the patch | 0 | a planted tab reads 1 |
| Shared files | `git diff --quiet 4e8828ee -- <the kit's SHARED list>` on `<a1>/clone3` | rc 0 | the `Registration` tests folder gives rc 1 |

**Limits of these measurements:**
- The README was re-wrapped after the loops and the mutant run. Line 76 had been 124 characters long, and the re-wrap moved two lines. The README is not compiled, and the final tree was re-tested on `clone3`.
- The publishes and the release guard were NOT RUN by the drafter.

## D-decisions (the drafter's, each a default under a Question)
- D1: the clause covers EVERY element, the leaf included. For the leaf it is redundant, because rule 7 already ran at the same `now`.
- D2: the clause sits after the status loop and before `Count >= 2` and the modulus rule. Every refusal in rule 8 is `IssuerNotTrusted`, so the order changes no reason. Rule 7 still wins for a leaf outside its window (P5).
- D3: `InsideWindow` catches every exception and reads false. This keeps the "only `RegistrationException`" property. DERIVED: a configured issuer's dates are unlikely to throw.
- D4: C16 is added. Its leaf is nested inside its issuer, so that only the clock is the variable.
- D5: the three window mutants stay named survivors on macOS. Two of them are PREDICTED killed by C14 on hosted Windows. `mWindowNotAfterExclusive` is killed nowhere, because the boundary answer of the platform is not ruled on.

## Questions for Tuesday (each with its default; the answer assumes the default)
- **Q1: add C16.** Default YES.
  - Alternative: no new cell. Then name `mTimeIgnored` and `mVerifySystemClock` as survivors again, which re-opens item 54's F2 in part.
  - Cost of the default: C16 on Windows is UNMEASURED. If Windows ignores `VerificationTime`, C16 goes red there. That is a second STOP, and it would show that the platform judges on the real clock. That is a refusal, not an acceptance.
- **Q2: check every chain element, the leaf included.** Default YES. Alternative: elements 1 and up only, which reads the same.
- **Q3: no boundary cell.** Default: none. The README declines to rule on the platform's answer at the exact instants. On macOS, P1 and P2 at the exact NotAfter and NotBefore were ACCEPTED. Alternative: pin that acceptance in a cell, which would pin a platform answer that the library does not own.
- **Q4: the window mutants as named survivors on macOS.** Default: `mWindowRuleOff` and `mWindowNotAfterOff` are killed by C14 on hosted Windows only (PREDICTED, like `mFixUndone` on Linux), and `mWindowNotAfterExclusive` by nothing. Alternative: an internal seam with a direct cell. That would still not see the call site removed, and it would be a compile error, not a red, at `759c9060`.
- **Q5: the gate.** Default: G1 (Opus) reads the whole branch `4e8828ee..<new head>`, with the probe list of answer §5, and runs `mutants_a1.py` (14 mutants). Tuesday commissions it.

## UNMEASURED
- The Windows mechanism, (i) or (ii).
- C16 on Windows and on Linux. Linux is PREDICTED green, DERIVED from C14 green on hosted Linux.
- Every PREDICTED number of the new hosted run (Windows 1587 / 1568 / 19).
- The exact text of git's fast-forward push line.
- The seat's own chain.

## Read load for the seat
The answer (19.9 kB), `3-fix.patch` (9804 B), `commit-message-2.txt` (316 B) and `mutants_a1.py`'s header. That is about 30 kB, roughly 8K tokens.

## Outside the fences (disclosure)
- One `cp` from the seat's lane `gate/` folder was REFUSED by the path hook, because it misread a brace expansion. Nothing was written. The drafter then copied the kit's tools from `<src>` (`fleet/state/s310/d1915/gate/`) instead, with sha256 equal to THE TOOLS.
- `git clone --no-hardlinks` READ the seat's `<lane>/clone` three times, into `<a1>`. Afterwards that clone was unchanged (HEAD `759c9060`, status 0 lines).
- `gh` was used for `-X GET` only, under the project `GH_CONFIG_DIR`.
- None of these happened: a write to any project file, the lane, GitHub or Jira; a delete (superseded files were moved to `<a1>/_quarantine/`); a `cd`; any `Source_Documents/` read; any message to a human; anything sent to pane %219.
