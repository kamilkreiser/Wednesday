# B379 DRAFTER REPORT (2026-10-21 07:3x AEDT)

Brief: `2026-10-21_B379_SEAT-W24_mps-pr93-fix-round2.md` (140 lines, 2 stamp slots `@STAMP_HEADS@` and `@STAMP_AUTHORITY@`; slot count 2 MEASURED). Shape copied from B373. Round 2 of 2 on PR #93, tier 1, Sonnet C2, pane `Datasec/MPS-W24`, one new commit on `b373/copyref-surrogate-289` over `a3cfda72`, no `src/` change.

## Questions for Tuesday (each with a recommended answer)
1. Q: Stamp the launch authority. Recommend: Kam's live board 2026-10-20 18:55:31 item 3 + the 2026-10-16 merge-once-tested grant (the wording B376 quoted); tier 1 stands (R-W23-1).
2. Q: Docs wording (R-W24-1). Recommend: the gate's own fix-shape, "(one unit fewer when the cut would fall inside a surrogate pair, such as an emoji)"; builder is told to STOP rather than reword.
3. Q: Test placement (R-W24-2). Recommend: a NEW theory in `CopyRefTests.cs` and a NEW HTTP theory in `V0Duplicate.cs`, so no existing row is touched (+N/-0 asserted).
4. Q: Add a loop row over L = 96..300 plus extra mutants n11 (`Length < 100`) and n12 (`Length <= 100`) beyond the gate's n7 (R-W24-3/4)? Recommend yes: round 2 is the last, and n7 is one of a family of length shortcuts; the loop row kills the whole family.
5. Q: Predicted new names 17 (8 direct + 1 loop + 4 x 2 HTTP), Api 1811 -> 1828. Recommend accept as a prediction only; the builder records the real number.
6. Q: Reuse of `.tools/wt-b373-fix` for the commit (it holds the branch; MEASURED at `a3cfda7` in `git worktree list`). Recommend yes after a clean-and-sha check; else STOP.

## Could not verify (UNMEASURED)
- No `dotnet` run: that all 17 new names are RED at base and under n7, and the exact mutant red sets (predictions are arithmetic from the gate's tables).
- `.tools/wt-b373-fix` cleanliness (status not read), whether `Create` returns the stored quote, counts at the builder's baseline, PR #93 CI on the new push, `AGENTMAIL_API_KEY`.
- Test and docs facts are RELAYED from `gh api` raw reads at `a3cfda72`, not a checkout.

## MEASURED at drafting (07:32-07:33)
`ls-remote`: branch = `a3cfda72…`, main = `1eccbc8b…`; PR #93 open, same head and base; `compare 1eccbc8b…...main` identical; open PRs 1 (#93); panes: no MPS seat live; `.tools` is at the project root and holds `b373/` with `heavy.sh`, `mutate.py`, `jira.py`; no heavy slot exists; load1 3.61; `docs/API.md:413` carries the phrase "when the cut would split a character".

## Note
B376 STATUS says the round's fix-shape names rows at 97 and 100 units; the brief widens to 97-101, 300, two-pair and the loop row. This is wider than the gate's minimum but still tests-only.
