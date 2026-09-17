Wednesday -> Seat B successor (Secuura/Blockchain-B)

## BLUF
**RULED: your default stands. GHSA-q8mj-m7cp-5q26's row comes out in PR-4 (baseline 29 → 26).** This is the brief's per-PR rule (a row is removed in the PR whose merge makes the advisory absent from every lock). It is the same ruling as GHSA-3f6p on #1033 (11:07:34Z). Your measurement meets the rule: qs 6.16.0 is outside `>= 6.11.1, <= 6.15.1` in all 26 carrying locks, with rc 0 on both gates and 0 CLEANUP. The negative control fails naming q8mj "in 26 lock(s)".

## Recommendation
1. Commit the row removal, assert conservation (29 → 26, exactly the 3 rows), and push.
2. The PR body names all three rows. In one line it says the q8mj row's "requires express 5" premise is **measured false for this advisory** (express 4.22.3 declares qs `~6.16.0`) **and that the express 5 migration decision (2026-09-03) is unchanged by this PR**. Do not state or imply anything about whether express 5 is still needed.
3. KS-775: exactly the one comment sentence already ruled. No other change.
4. The q8mj facts go in the KS-763 comment (KS-531 is archived; leave it untouched).
5. READY as tier 1, as planned. Regenerate root locks on npm >= 11.19.0 (the #1033 gate's F1). You did this; say so in the READY with the version.

## Detail
- Holds unchanged: nothing to Peter or Stuart, no deploy, never Done, Refs never Closes, never delete.
