# B567 DRAFTER REPORT (gate kit for PR #106, seat Datasec/MPS-G74, tier 1 Opus, round 1 of 2)

Drafted 2026-10-24 08:55-09:05 AEDT (clock by `date`), read-only. Files written: the kit `2026-10-24_B567_SEAT-G74_mps-106-gate-tier1.md` (103 lines), its unchanged copy `...md.pre-stamp` (`cmp` rc 0), this report.

## Stamp slots
`.pre-stamp` copy: `/usr/bin/grep -c -E '_''_''_''_'` = **9** lines (eight slot lines at 25-32 plus the last line 103). Control: a scratch file holding four underscores reads 1. `grep -o -E '@[A-Z_]+@' | wc -l` = 0. Non-ASCII bytes: 0 (one `Σ`/`×` mention was replaced by words). The kit says "reads 9 lines" in its Stamp section.

## Ports 9150-9159: verified
- `lsof -nP -iTCP:9100-9159 -sTCP:LISTEN`: nothing, rc 1 (08:56).
- Scan of `briefs/2026-10-2[34]_*.md` for `915[0-9]`: 2 hits, both inside a 40-hex sha in the B500 brief (`...0915315f6...`), a false match, not a range. Control: `911[0-9]` reads 43. No `B567` file existed (`ls | grep -c B567` = 0). Other live blocks as found: B561 8980-8989, B562 9110-9119, B564 9120-9129, B565 9130-9139, B566 9140-9149.
- `.tools/b567` absent; no `heavy-slot-*` directory exists (all three free); load averages 5.99 8.74 8.21 at 08:57.

## What I measured (PR #106)
- `pulls/106`: open, not draft, mergeable true, state `blocked`; head `7809cd80...`, base `a5b4bbb5`, 5 commits, 8 files, +571 -14 (matches the builder). Merge ref `25f12e97...` (parents unread). `ls-remote main` = `a5b4bbb5`. Open PRs: 106, 105, 104, 102.
- Check-runs on the head (8 listed): CodeQL neutral, Analyze actions/python/javascript-typescript success; **4 pending** (Analyze csharp, dotnet, web, python), all in_progress.
- Source read at the head: the exact `PurchaseRecomputation`/`QuoteReconciler`/`ReconciliationTypes` diff and the `ReadinessPanel.tsx` diff. `MeasureVariance` is constructed only in `QuoteReconciler.cs` (3 sites); the only files in `src web/src docs/api` naming `MeasureVariance|QuoteReconciler|ReconciliationReport` are the two Reconciliation files (no API/contract/web consumer; left to the gate to confirm).

## Points the kit adds beyond the B566 shape
- MUST-CHECK 1: the gate's generator must use a seed outside the builder's 1..240 and 1000..1239, plus a power control; probes the builder's NOT TESTED exact-cent on a non-terminating quote; rental "byte-equal" is stated as equal by value in the seven original members, because the public record now has a trailing `ContractDifference` (a serialised or ToString form cannot be byte-equal; no consumer found).
- The kit asks whether `ContractDifference` is needed and whether it leaks (G-9), and whether the claim "the calculator never reports both deal and section usage" (the reason for commit `7809cd8`) is true.
- MUST-CHECK 2 requires two blind-spot plants (an inlined constant, a third-namespace call) beyond P2/P3/P6/P4.
- MUST-CHECK 5 is the tokenizer proof that -295 is unbuilt; MUST-CHECK 6 notes the builder used a `.tools/b565` home, so its numbers stand only if equal under the gate's `.tools/b567` home.
- C3 flags that the row naming `ContractDifference` is a compile error at `wt-diff` (base source), expected and to be reported as such, not as a harness fault.

## Not done / UNMEASURED
No build, test, Jira, fetch, worktree or HTTP. Not read: the two new test files, `ReadinessPanel.test.tsx`, `docs/RECONCILIATION.md` in full, the B324 gate STATUS, the PR's job logs, the merge ref's parents. All runtime counts in the kit (413/167/2,204, 133/1,271, 13 red of 16, 16 mutants) are the builder's, RELAYED. Builder STATUS B567 path does not exist yet (expected). Load was 5.99 at 08:57, close to the gate of 7.
