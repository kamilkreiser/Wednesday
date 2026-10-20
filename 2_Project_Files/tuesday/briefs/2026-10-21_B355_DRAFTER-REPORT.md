# B355 drafter report (Sonnet 5.5, read-only), 2026-10-21 01:2x AEDT

Brief: `2026-10-21_B355_SEAT-R11_nexusai-rd874-rd875.md` (136 lines, 2 stamp slots: the main-pin slot in 3 places, the time slot in 1; `.pre-stamp` check = REFUSE grep reads >=1 before stamping, 0 after).
Clock: `date` 01:24:43 at start, 01:26:22 at the pin reads, 01:29:22 at the end.

## What I measured (instrument)
- NexusAI main = `d463f8817fba925dee7e78c5216df3d5ea8ad073` (`git ls-remote origin refs/heads/main`, 01:26). Unchanged since the sweep.
- Open PRs (`gh pr list`, GH_CONFIG_DIR of the project, kamilDatasec logged in): #97 draft head `115a775b…` MERGEABLE; #67 head `94b288cc…` CONFLICTING. File lists from `pulls/97/files` (8) and `pulls/67/files` (3). Shared with this work: only `scripts/verify-expected-counts.json` (#97, #67) and `backend/validators.js` (#97, #67; the brief forbids editing it).
- RD-874 / RD-875 / RD-873: Jira GETs (project `.env` in `python3 -I`, key not printed). Both tickets To Do, Low, no comments. RD-874 line numbers re-read from raw `gh api contents` at main: test at `auth-gate-fail-closed:1140`, `rd395...:89` (plant :93), `scim-security-controls:788` (plant :790) match the ticket; `jsonStorage.js:1085` is the product line (also :1287 fallback dir).
- `tests/uat-run.js` read whole (84 lines): default host `:11`, `port: 443` `:18`, IIFE runs on require, so a unit test cannot `require` it today. `git grep -l uat-run` at main found no other file referencing it. `package.json` jest ignores `/tests/e2e/` and `__tests__/helpers/`, so a new `__tests__/` test file is collected and changes the counts (4934/303 at main).
- Lock base: `queue-jest/` empty, no lock dir. Tool sha256s equal B349's. `tmux list-panes -a`: no NexusAI pane. `node_modules` donors exist (`b343-pr98-land` etc.).
- Model row: `model-routing.md:92` row C2 (S55 1st); C3 not applicable (test code, equality line); `models_latest.json` sonnet = `claude-sonnet-5-5`. Gate 29 launcher `launch_qa_nexusai_gate29.sh:187,759,826` confirms guard 38R derives negative-control seats from live panes.

## Not measured
No jest, node, clone, mutant, push, or CodeQL read. The S8a mutant effect, the new cell count, the new counts, and whether `jest.mock('https')` plus a `require.main` refactor works as designed are all for the seat to measure.

## Open questions, each with my recommendation
1. **One commit or two?** Recommend leaving it to the seat (brief allows 1 or 2, must say which); two commits (one per ticket) read better for the gate, no process cost.
2. **Is a new committed test for RD-875 right, given it changes the counts file and forces a counts-only TURN on #97 / #67 / this branch, whichever lands second?** Recommend YES: the ticket asks for a regression test, and the brief handles the consequence (regenerate once, flag in STATUS and READY). The alternative (no new test, mutant-only evidence) leaves RD-875 unprotected. Tuesday should land this branch AFTER #97 so the TURN falls on this small branch, not on the gated #97.
3. **Exported-helper refactor of `tests/uat-run.js` (`require.main` guard) vs a child-process test.** Recommend the refactor: a child-process test would have to run the script, and before the fix an unset `UAT_BASE` hits the shared demo host. The brief bans running it. Risk: line shifts could change how CodeQL presents RD-810's alert at `:30`; the brief makes that a finding for Tuesday, not a seat fix.
4. **Gate tier for the QA gate:** tests-only plus a dev script means G2 (tier 2, Sonnet, `model-routing.md:109`); the three edited cells sit in auth/SCIM test files, so Tuesday could argue G1. Recommend tier 2, with the 3-cell mutant table as the gate's check.
5. **Plant-cell count discrepancy in the sources:** gate/ticket say 18 swept, "14" others (ticket text also says "the other 15 cells"): 14 + 3 = 17, not 18. Recommend the seat counts them itself (the brief says so) and Tuesday does not quote 14/15/18 anywhere.
6. **RD-873 overlap:** its N30-2 bullet is the same observation as RD-875. Recommend Tuesday comments on RD-873 after READY (the brief has the seat draft it) and does not wait for a seat on RD-873 (UNMEASURED whether any exists; none of its files overlap).
7. **Lock tag:** `b355-build-*`, no "merge" (build, not merge; C-184 rule 1 reads for "merge"). Recommend keep.
8. **Pane `Datasec/NexusAI-R` collides with nothing live** (no NexusAI pane now), but older "R" numbered seats (S92R, S97R handovers) existed. Recommend Tuesday re-reads `tmux list-panes` at launch and confirms the name is free.
