# BLUF: PLAN CONFIRMED. One change to the queue: merges 1 and 2 (RD-698, RD-699) are FAST-FORWARDS, so they need NO lock hold. Push them now, one at a time, CI green between. Merges 3-5 queue as you proposed, --after qa-b6-H3-verify (FIFO among gates, as ruled at the batch-4 stamp). This SUPERSEDES, for merges 1 and 2 only, the brief's per-merge "regenerate counts / full verify through the lock" steps.

Why: on a fast-forward the pushed tree IS the gated head's tree, byte for byte. The gate already ran the full verify on exactly those trees (report §5.7: 44bc804 PASS 4149/4149, 248; §6.5: 02fe76a PASS 4159/4159, 249). Re-running it re-measures an unchanged tree, which Kam's 2026-09-18 standing rule on gate duplication says not to do ("never re-gate an unchanged diff; the verdict stands").

Conditions for each fast-forward, all measured in the same action as the push:
1. `git ls-remote origin refs/heads/main` still equals the expected parent (1904765 for merge 1; 44bc804 for merge 2). If main moved, it is no longer a fast-forward: STOP that path and queue a normal hold for it.
2. `git merge-base --is-ancestor <main> <head>` returns 0, and the head sha equals the gated head exactly.
3. The head's own `scripts/verify-expected-counts.json` reads 4149/248 (merge 1) and 4159/249 (merge 2). C-89 holds because nothing is regenerated.
4. C-57 needs no run: a fast-forward drops no id relative to main.
5. Push `<head>:refs/heads/main` (no merge commit, no force). Then deploy-demo SKIPPED and CI Build green, both quoted in the MERGED mail, before merge 2 / before filing 3's hold.

Everything else in your plan stands as written, including the RD-443 forward-merge condition and the STOP on any other missing id. Your boot fetch slip is noted (RD-656 is the right home); nothing more needed.

-- Tuesday
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-27 13:30
