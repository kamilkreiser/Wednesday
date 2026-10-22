# B492 drafter report (2026-10-23 about 02:09-02:20 AEDT, read-only)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-23_B492_SEAT-G49_hpsmpoc-b490-gate-tier2.md`. Seat `Datasec/HPSM-POC-G49` (panes live: tuesday, fleet-monitor, J1, G48, K1; G49 free), Sonnet `claude-sonnet-5-5` row G2, tier 2, ports **8400-8409**, round 1 of 2, one subject (B490). No `.pre-stamp` copy made (fence: two files only); Tuesday can `cp` before stamping. Unstamped copy: 8 lines match the slot pattern (control: a scratch file with four underscores reads 1), 0 at-sign tokens, no person's name.

## Measured by me (GitHub GET, ls-remote, lsof, tmux)
- main `9eeabb7c` (#186), b490 head `18143b10`; compare main...b490: ahead 1, behind 0, merge base `9eeabb7c`, two files +107 -0 and +63 -0, one hunk each; check-runs on the head 0; only open PR is #184.
- Read the whole patch: Api added members (2 constants, one TheoryData, one helper, 6 cases in 5 methods) and mock (HELD_EDGE, new describe with 6 tests); product anchors at main (`Requests.cs` :141 and :145-146, `CustomerEndpoints.cs` :194 and :198, `customer-detail.ts` :58 and :92).
- Overlap by file-name grep over five names: b489, b429, b460, b461, b462, b465, b467, b472, b49, b459, dependabot all 0 (control: b429 lists `web/src/instrumentation.ts`); **b466 5** (the squash-merged #187 branch, not live; the gate proves it).
- `lsof` 8400-8439 empty; 8401/8402/8412/8425 tokens are only in finished 2026-10-21 briefs.

## Relayed, not re-measured
All builder figures: 74->80, 97->103, kill counts (A1 1, A2 3, A3 1, A4 2, A6 4), whole Api 1901/13/0 vs 1907/13/0, web 2165 vs 2171, build 0/0, repeats, gitleaks, UatOpen drift still present.

## UNMEASURED (and why)
No dotnet/npm/test/mutant/fetch/worktree run (fence): that rows are green at main and red under each mutant, class counts, the drift status after #185, whether `Plant` reads the edge-spaced name back, the new mutants' outcomes (N1-N9, P1, P2), `HasControl` over each literal (the gate computes it), `#184` interaction.

## Departures from the templates
- One subject, no `-headA/-headB` split; `-merge` equals the head while main has not moved (the gate proves it).
- Check 1 adds a program-level "nothing existing edited" proof (delete the added hunk, compare the remainder; sha256 of every reused helper) and a by-member account of all 170 added lines.
- Check 2 is new: the planted names must hold a refused character, edge rows ASCII spaces only, R3/mock (h) pin the trim without endorsing it (T1/T2 scratch mutants remove the trim and must turn them red).
- Mutants: the builder's A1, A2, A3 (both forms), A4, A6 plus gate-own N1-N9 (InvariantCultureIgnoreCase, TrimStart, TrimEnd, held trims, mock toLowerCase without a null guard, mock trimStart, mock held trim) and survival-expected probes P1 (normalisation) and P2; each row needs a named killer (12 cases, closed list "at least these" with a property check and control). Builder survivor-probe-after-rows order is reproduced by the gate on the unchanged files.
- Severity: a new widening mutant surviving is Major; a builder-five survivor is a Blocker.

## `____` slots (8 lines)
Stamp time; stamped by; launch authority; hard stop; main at launch; head at launch; model receipt + load1; last line `READ-WHOLE-BY-TUESDAY: ____`.
