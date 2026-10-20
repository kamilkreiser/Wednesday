# B375 drafter report (2026-10-21 ~06:40 AEDT)

Brief: `2026-10-21_B375_SEAT-G16_hpsmpoc-pr167-gate-tier2.md` (86 lines). Shape copied from B367 (read whole). Inputs read whole: B372 STATUS, B372 brief, B357 STATUS, B367 brief.

## Stamp slots
Two: `@MAIN@` and `@HEAD@`, both in the Stamp paragraph. Measured: `grep -o -E '@[A-Z_]+@' | wc -l` = 2. The Stamp paragraph ends "Stamp time and launch authority (to be filled by Tuesday at stamp ...)": Tuesday must write the stamp time and the launch authority sentence there (no slot token for it, so the count will read 0 only once the two shas are filled; if Tuesday forgets the authority sentence the REFUSE rule bites at the gate). `READ-WHOLE-BY-TUESDAY: PENDING` is the last line; Tuesday replaces it.

## Measured by me (06:34-06:36, read verbs only)
- PR #167 head and branch `91cbbcb1...` both by ls-remote; main `6818896b`; `git diff --stat` 1 file +93/-1; hunks `-5,0 +6`, `-136,0 +138,18`, `-234 +253,2`, `-287,0 +308,72`. No `b375*` ref, no `.tools/*b375*`.
- `lsof` IS on this machine at `/usr/sbin/lsof` (not `/usr/bin`); B372 Correction 5 ("does not exist") was a PATH error. The brief tells the gate to use the full path.
- Load at 06:34: 6.54 / 9.30 / 9.59.
- Read the two rows and the product `FailOnceAsync` at the head/base: the quoted names, input asserts, outputs and the comment text match B372 STATUS.

## Not verified (UNMEASURED)
- PR #167 open/draft state, commit count and subject (the brief tells the gate to read them; I used Tuesday's facts plus `diff --stat`).
- CI/CodeQL state at the head; the `ci` run id; SQL Server shard totals. The expected 1526 total vs B357's CI log (Api 1524 with Azurite on and 0 skipped) is flagged in r8 as something the gate must reconcile.
- `model-routing.md:109` row G2 text (copied from B367, not re-read).
- Whether the five required contexts are still those five (RELAYED from B367).
- No dotnet run; nothing about the mutants was run. The gd mutant needs the run read moved with the guard (T-a); I did not compile it.
- Port block 7380-7389: named only in the ended B372 brief and as part of an old 7230-7389 "avoid" range in B333/B335; not re-checked for listeners.

## Questions (each with a recommended answer)
1. Port block 7380-7389 for G16? Recommend yes: B372 (its prior user) used none and has ended; the gate needs none (in-process host).
2. Launch now while B371 (PR #166 round 2) is live and load1 touched 9? Recommend yes with the HOLD as written; the gate waits at load >= 8 and the priority list puts r7, r2, r8 first.
3. Is `MERGE: Tuesday lands on GO/GWF` right even though PR #166 is also pending? Recommend yes: the two PRs touch disjoint files, and #167 is behind 0, so land order does not matter; the squash uses `--match-head-commit`.
4. Stamp authority sentence: reuse the 2026-10-20 18:55:31 board item 3 as B367 did? Recommend yes.
5. Launch with CI pending (conditional suffix)? Recommend yes, as B367.
6. Scratch product mutants allowed (gd needs a two-line move in `ImportEndpoints.cs` in the gate's worktree only)? Recommend yes, as B357 and B372 did.
7. Extra mutants beyond the ask (m-one-table x5, m-audit, m-reason, m-null)? Recommend keep: they are cheap in the 7-class set; if the gate is short on time the priority line lets it drop them after r7's four.
