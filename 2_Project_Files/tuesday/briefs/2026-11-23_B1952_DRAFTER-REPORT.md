STARTABLE: YES

# B1952 DRAFTER REPORT: OXPd 2 lane F3, round 2 of 2 (seat Datasec/OXPd2-X42)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1952_SEAT-X42_oxpd2-f3-round2.md` (62676 bytes), sidecar `.measured` beside it: `stamp_check.py` reads 171 claims, 171 measured, rc 0. Tools: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s313/d1952/gate/` (four files, new) plus kit B1945's `d1945/gate/` (twelve files, sha256 re-checked, all equal). Scratch: `fleet/state/s313/d1952/`. Drafted 04:05 to 04:26 AEDT 2026-11-23 (clocks from `date`).

## BLUF
- **FOUND 1 fixed in text, checked clause by clause against the code at HEAD1:** the Limits sentence now gives the shape and both orders. Held first: the id serves cleared bytes. Disposed first: `TokenAnswerRefused`, nothing held, the issuer asked again. It is scoped by "one valid token object", "both answered after it" and "the later one within its bound". Without those three scope words the sentence is false for H12 and H13 (in the kit). The order is named by the existing "checked ... under the registration's lock just before it would be held" check, so the race H14 (a dispose between `:318` and `:335`) cannot make the sentence false. The gate's word "answered first" would not have been exhaustive.
- **FOUND 2 fixed in text:** the D2 sentence is now "The comparison is with the holder's state for the id as it was when the call was made: `Remove(id)` ends that state ... a later `GetAsync(id)` starts a new one, so an answer that arrives after the `Remove` to a call made before it is disposed, even when it is the object the new state holds". Neither "makes a new registration" nor "compares its answer with the old one" remains.
- **The other order is PINNED (Tuesday's default):** inside L01's existing `[Fact]`, `OldCallAnsweredFirst` runs in time and late, so the total stays +0 (Universal Print 349, solution 1761, MEASURED). Each new form is red under a mutant of its own: `mRemovedClearsOnly` reds the in-time form only and `mLateClearsOnly` the late form only. `mHoldDisposedAnswer` reds the refusal (and landed T12). The round-1 mutants still red L01 at the round-1 halves with the round-1 messages. Loop 10 of 10.
- **`main` moved (your 04:14 message):** `49f686a8`, tree equal to A2-F head `a56ed63b` (MEASURED). The kit keeps ONE fast-forward on `6177b525`, with no rebase. The drafter's merged tree (A2-F + HEAD1 + r2) built 0/0 and ran 1785 / 0 / 1781 / 4 (MEASURED macOS).

## FACTS RE-MEASURED (instrument; control)
- Origin by `gh api -X GET` (project GH_CONFIG_DIR), 04:15:26 and 04:24:17: main `49f686a88fdb5c810c124dfe55ca1e68d2c29819` (1 parent 394fa997, tree 89af052b); branch `b1945/f3-readme-limits` `6177b525...`; `compare 394fa997...main` 7 files, all Identity; `compare main...6177b525` diverged 1/1; pulls newest 29, 28, 27 all closed; `.private` true, `.permissions.push` true.
- HEAD1 files: UP README `bfaa04ed...` and L01 `f846e6d3...`, both equal to kit B1945's after column; the holder `85fc5ea6...` (BASE's).
- Prototype (`<d>/clone`): build 0/0; UP `Total: 349, Errors: 0, Failed: 0`; the five mutants and their reds (kit's THE CONTROLS, from the logs); each `undone ... equal True`; rebuild-final rc 0; whole solution 1761/0/1757/4 (`failed Datasec.` 0, control `Test run summary` 1); loop 10/10; `f3r2_checks.py` PASS, every control FIRED; `f3_checks.py` vs 394fa997 PASS; `repo_rules.py` RULES 553; `added.py` 58; `words.py` clean (control 13 of 13); gitleaks clean on 5 neutral files (control `leaks found: 1`, moved to quarantine).
- `r2.diff` applied to a fresh worktree at HEAD1 byte for byte; a second `--check` was refused.
- dotnet 10.0.404; gitleaks 8.30.1; load1 1.92 to 6.93; lock waits 0 on every job; the drafter never broke and never saw another holder's lock.

## CHAIN INPUTS
Every step's inputs exist at HEAD1 or come from an earlier step; the table is in the kit. `<src1>` and `<src2>` both exist (MEASURED by ls and sha256).

## D-DECISIONS (the drafter's, for Tuesday)
- D1: three new mutants rather than reusing round-1 ones. The round-1 mutants red L01 at its round-1 halves first and mask the new forms. The "clears only" mutants keep the bytes cleared (the round-1 halves stay green) and only drop the disposed mark, which is exactly the condition the new sentence relies on.
- D2: L01 is renamed (R4/Q2), because the round-1 name stated one order for all. That is the same defect class as FOUND 1.
- D3: no Data mutants re-run this round: the Data files are byte for byte HEAD1's (checked by `f3r2_checks.py` KEPT, with its control).
- D4: no publish or release guard this round: the two changed files are not read by either. Marked NOT RUN in the kit; the hosted legs run both.

## Q-QUESTIONS FOR TUESDAY (defaults in the kit)
- Q1 (STOP-class) the two sentences as in `r2.diff`; Q2 rename L01; Q3 (STOP-class) pin in L01 (your default); Q4 90/60 minutes, pane X42, G2 round 2 of 2 on Opus.
- **Conflict to settle at the stamp:** the gate's `2026-11-23_B1949_verify/landing.txt` says "both cells stay byte for byte" and expects the L01 row `+61 -0`. Q3 a (pin) changes L01: against 394fa997 the rows are now `4 1`, `13 4`, `53 0`, `104 0`. The round-2 gate must re-read the landing form; the squash texts in that folder were written for round 1's cells (not re-read by me against round 2).

## UNMEASURED / NEVER RUN
- The pane census: `tmux list-panes` read 0 for `OXPd2-X42` AND 0 for its control `OXPd2`. The control did not fire, so S3 must read it.
- Never run on a head of this round: `clone.py seat`, the `switch --track`, the commit and its identity read, `run_step.py`, ls-remote, fetch, the push, `hosted2.py`.
- Nothing ran on Linux or Windows. Windows succeeded 1740 / 1764 is PREDICTED/RELAYED.
- The exact SHARED FILES `diff --quiet` form was not run by me; its equivalent ran (`f3r2_checks.py` SRC).

## OUTSIDE THE FENCES (disclosure)
- I wrote only: the kit, its `.measured` sidecar, this report, and files under `fleet/state/s313/d1952/`. That folder holds my scratch clone, two worktrees of it (`clone2`, `both`), logs, `gate/`, and `_quarantine/` (moved lock folders, the gitleaks control, the TODO sidecar).
- In my own scratch clone (not the project's repo) I used `switch --detach`, `worktree add`, `apply --index` and `add`. I made no commit there; `<d>/clone` is left with `r2.diff` staged. No write to the project repo, GitHub or Jira; no push; every `gh` call was `-X GET`.
- I read gate B1949's probe file `ZG1949UpProbes.cs` for P8's shape and copied none of it. I read seat X41's STATUS and kit B1945, as the commission listed them.
- Nothing under `Source_Documents/`, no key folder, no sibling project. No `cd`.
- Every heavy job went through `heavy.py` and the wave lock, one at a time. The loop ran as a background-notified foreground job and nothing ran beside it.
- Names: none in the kit text for commits (`words.py` over `r2.diff` and the added lines/message: clean).
