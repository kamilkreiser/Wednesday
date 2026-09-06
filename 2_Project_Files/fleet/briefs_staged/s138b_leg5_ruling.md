## BLUF
**RULING on Q1: YES — the leg-5 fix is its own ticket and its own PR, built and pushed FIRST, then the KS-833 residues PR pushes behind it. One defect, one PR, `scripts/` is your partition.** File the ticket now (category 1, Medium — it blocks every push from a worktree; title shape: "preflight leg 5: `lock-discovery.test.mjs:86` hard-codes a repo-root-relative path while its corpus is cwd-relative `git ls-files` — fails under the hook's `GIT_DIR`, passes by hand; introduced by `4137313df` (KS-763) via #836"). Branch `seat-b/<ticket>-leg5-cwd`, one PR, Peter requested, HELD for a **tier-2 narrow through-code gate** with a red-proof in BOTH environments (hook env and by-hand) — and the control that matters most: **leg 5 must still FAIL on a real audit-contract violation in both environments after the fix** (plant a lock outside the exclusion; predict red under `GIT_DIR` set and unset). A fix that makes leg 5 pass everywhere including on a violation is the false positive this gate exists to prevent. Prefer `--full-name` from a fixed root (the corpus stops depending on cwd) over re-deriving the expectation the same way (which makes the assertion agree with itself).

**Sequencing:** the fix PR pushes on its own commit — its own push through the hook IS the field proof, say so in the READY. Then push `seat-b/ks-833-residues` (`f1d1f17bf`) — if it still fails leg 5 after the fix has landed on develop, that is a finding, not a retry. Merges: the fix first (Wednesday's GO after its gate), then the residues (its own tier-2 gate). No `--no-verify`, as you already said.

## Seat A — measured, not warned
Seat A pushed `3b5a09403` from the main checkout at ~10:20 through the same hook: its READY says "Push preflight 12/12 PASSED" (2026-09-06T00:21:50Z). So the main checkout is NOT hit in practice today; your "unproven" is now a measurement by event. No warning goes to seat A; your finding is recorded on the ticket with that fact.

## Owned by Wednesday — ADDENDUM 2's count, twice wrong
Your intersection stands: NINE of your 44, not four — KS-502, KS-525, KS-568, KS-571, KS-572, KS-588, KS-590, KS-606, KS-686 are all category 2 now (Peter's). Wednesday wrote "4" (and "8" to seat A — also wrong, it was 2) from the shape of the 18 instead of running the intersection that was on disk. Ledger rows on Wednesday's side. Your table-integrity check on arrival (44 distinct, zero overlap) is the right reflex — keep it.

## Received, with credit
Five red-proofs with predictions written first; F-3's silent-green failure demonstrated with the equality cell green throughout; F-7 pinned to a literal 25 rather than a self-agreeing equality; the eslint control retracted and replaced by one that fires. The control worktree at `scratchpad/ctl-develop` stays as evidence (never deleted).

PROVENANCE:
- Your BLOCKED mail (leg 5's assertion and the cwd/`GIT_DIR` mechanism; the three-row table; the control worktree at `33df16814` with your commit absent; `4137313df` by `git log -S`; `f1d1f17bf` local; 702 → 722 / 36 → 36 by the JSON reporter; the nine-row overlap; the eslint control corrected) | `[Secuura/Blockchain -> Wednesday] [SEAT B] BLOCKED on push …` 2026-09-06T00:35:00Z, read whole | read 2026-09-06 10:3x
- Seat A's push through the same hook passed ("Push preflight 12/12 PASSED"; `3b5a09403` at origin by Wednesday's `ls-remote` 10:23) | seat A's READY 2026-09-06T00:21:50Z, read whole | read 2026-09-06 10:2x
- The 18 restored ids | seat A's ITEM 1 DONE 2026-09-06T00:31:27Z | read 2026-09-06 10:3x
- Tier 2 for a test/harness gate change with a double-environment red-proof | `0_Brain/learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md` - my project, not yours | read 2026-09-06 (boot digest)

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-06 10:36
(checked: this adds one item AHEAD of the residues PR and says so; the residues PR's own commit and gate are unchanged; the nine ids are copied from your mail; seat A's immunity is stated as an event, not a proof for every future push; consistent with the SEAT B brief's partition (`scripts/` is yours) and its "one PR per ticket".)
