STARTABLE: YES

# B2104 DRAFTER REPORT: OXPd PR 53 re-scan by one empty commit (seat X76)

Drafter: read-only Agent-tool drafter (Opus) for Tuesday s328. First `date` printed `Thu 26 Nov 2026 03:48:08 AEDT`. The kit's sidecar header holds the write clock (printed by `date`).
Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-26_B2104_SEAT-X76_oxpd2-pr53-rescan.md` (+ `.measured`). `stamp_check.py <kit>` exits 0 with 80 claims and 80 measured.
Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s328/d2104/` (seat-tools/, logs/, clone/ from `clone.py draft`, _quarantine/).

## BLUF
- The kit is one step: the seat clones with `clone.py seat`, checks branch = `1c7cdbbb` and main = `1ccf6d0c` (origin and clone), makes ONE `git commit --allow-empty` with the configured identity, proves tree `e20eeff6...` and one parent `1c7cdbbb`, pushes by sha ONCE (fast-forward), reads it back, then runs `rescan_wait.py <sha40> refs/pull/53/head push,pull_request --wait --minutes 60` and ends `READY B2104: <sha40>`.
- **Tuesday's "UNMEASURED" premise is now MEASURED and documented.** (a) GitHub's setup-types page says default setup scans "When creating or committing to a pull request based against the repository's default branch, or any protected branch" (RELAYED, docs.github.com read at drafting). (b) In this repo, PR 37 got a second `dynamic` run (45110636159) at its second head `85e414d6`, 57 s after that commit (MEASURED). The other 48 PRs in the newest 100 dynamic runs had one each.
- **The kit does not use `hosted3.py`.** On `1c7cdbbb` it prints `FAIL 1 (a job name twice among the check runs)`, because a head that carries both push and pull_request `ci` runs has every job name three times (MEASURED 03:52). The new head will carry both. Tuesday's `landing.txt` step 3 reads the job logs.
- The failed run's `Analyze (actions)` job log holds `##[error]Server Error` once (MEASURED, job 139326769374). Its python and csharp jobs succeeded.

## FACTS re-measured (instrument; clock)
1. Origin (gh api -X GET, account kamilDatasec, 03:48:59 to 03:49:04): main `1ccf6d0c...`; `b2100/row4-top-level-button` `1c7cdbbb...`; `b2104` refs 0 (control b2100 1); open PRs: only 53 (head 1c7cdbbb, mergeable true, state `blocked`, reviews 0); 1c7cdbbb tree `e20eeff6...`, one parent 1ccf6d0c. Re-read by `git ls-remote` on the project checkout at 03:56:11: unchanged.
2. Runs at 1c7cdbbb: ci push 45637707044 success; dynamic 45648685455 `PR #53` failure (actions job failed at `Perform CodeQL Analysis`); ci pull_request 45648689464 and 45656201864 success. Analyses `refs/pull/53/head`: csharp 0, python 0, no actions row. Main 1ccf6d0c: three rows, each 0.
3. Default setup: `configured`, languages actions/csharp/python, weekly schedule. The branch has no ruleset rules (0 rows; control: main has 4: deletion, non_fast_forward, code_scanning, required_status_checks) and is not protected.
4. ci.yml at 1c7cdbbb (218 lines): `push` on `main` and `'b[0-9]*/**'`, plus `pull_request` and `workflow_dispatch`. The push fires both `ci` runs. Run durations measured: 3 min 26 s to 7 min 15 s.
5. Prototype (session-scratchpad clone, push URL invalid): `--allow-empty` commit gives `e20eeff6... | 1c7cdbbb... | Re-run code scanning after a GitHub outage (no change)`. rev-list count 1; diff against 1c7cdbbb is 0 lines (control: against 1ccf6d0c, 11). Control: the same commit without `--allow-empty` gives rc 1.
6. rescan_wait.py controls: READY at main (rc 0); FAIL at 1c7cdbbb on the failed dynamic run (rc 1); NOT READY at main when a pull_request run is required (rc 3).
7. Message: `words.py` `WORDS: clean (1 files)` (control 13 of 13); B2xxx count 0 (control 4); gitleaks rc 0 (control rc 1).
8. Open code-scanning alerts: 0 on the PR ref, 0 across the repo. No control fired, so this is a suspect zero and the kit says so.

## D-decisions (drafter's, each Tuesday's to keep)
- D1: a new tool, `rescan_wait.py` (GET only), stands in for hosted3.py. It requires: ci push + ci pull_request runs, a dynamic run, every run `success`, and three analyses at the sha with results 0 and no other category.
- D2: the commit message carries the attribution line, as 1c7cdbbb's does. It is gone after the squash.
- D3: the branch is created with an explicit `switch -c ... origin/b2100/...` (the measured form), not a DWIM switch.
- D4: no build, no test, no heavy lock, no port. The STOP budget: push by Step 0 + 20, READY by Step 0 + 75.

## Questions for Tuesday (each with its default)
- Q1 (STOP-CLASS, S3 in words): an empty commit on the reviewed branch. Default a (built). Alternative b: wait for a retry GitHub says is not possible.
- Q2: the message. Default: the suggested subject plus the attribution line.
- Q3: if the new dynamic run fails again. Default: STOP. A second empty commit would be a new commission.
- Q4: the wait bound. Default: 60 minutes. A STOP if no dynamic run appears within 15 minutes.
- Q5: Opus (`OXPd CLAUDE.md:7`), pane `Datasec/OXPd2-X76`, push by +20, READY by +75.
- Q6 (for your landing, not the seat's): `landing.txt:42` says "if the branch moves off 1c7cdbbb, stop", and steps 2 to 5 pin 1c7cdbbb (3 `match-head-commit` lines). It needs your addendum naming the new head after your tree-equality check. Default: your addendum. The alternative is a new gate, which isn't needed because the tree is equal.

## CHAIN INPUTS
| Step | Inputs | From |
|---|---|---|
| 0 | kit, Stamp | Tuesday |
| 1 | seat-tools (4 files), the checkout's 3 local values, origin | d2104 (exists), `<repo>` (exists; rc 0 for each of the three keys), GitHub |
| 2 | clone on the branch at 1c7cdbbb; commit-message.txt, words.py | Step 1 |
| 3 | the commit | Step 2 |
| 4 | the pushed head; rescan_wait.py | Steps 3, 1 |

## UNMEASURED / NEVER RUN
`clone.py seat`; the commit with the configured identity; the push and its read-backs (the compare values `ahead_by` 1/0 files and main...new `ahead_by` 2, 11 files are DERIVED); the `--wait` loop on a new sha; whether GitHub's outage has fully cleared (the commission RELAYS githubstatus 'none' at 03:37:29); whether the code_scanning ruleset on main clears once an actions row exists (your landing).

## Outside-the-fences disclosure
- The drafter made a commit in a clone in the session scratchpad (`/private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/b12efbeb-0656-49c2-aa8d-170703a424d2/scratchpad/proto`). That clone has no push URL and was made locally from the d2104 draft clone. The drafter set the identity with `-c user.name=draft-prototype -c user.email=draft-prototype@invalid`, because a draft clone holds no identity. This was not a project repo and nothing was pushed. The kit forbids `-c` for the seat.
- A hook refused two `git -C` write verbs (switch/fetch) aimed at the d2104 clone. The drafter moved that work to the scratchpad clone as the hook directed.
- The drafter read docs.github.com with WebFetch (public documentation, not a project, demo or production host).
- `git clone` (clone.py draft) into d2104/clone; `git ls-remote` on the project checkout (a read verb).
- The drafter moved two files to `d2104/_quarantine/`: a hosted3.py copy it had first put in seat-tools, and the first sidecar skeleton (re-made after an edit to the kit). Nothing was deleted.
- No write to the project, GitHub, Jira or the card store. No message to anyone. No `decision_queue.sh`. No read of briefs_staged, scoreboard, `_ledger.md` or a non-Datasec tree.
