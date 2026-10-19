# Gate brief: GATE R1 = #1568 test-only DELTA, Sonnet, tier 2

Commissioned by the Wednesday seat, 2026-10-19 after J 13th's READY FOR DELTA GATE of 02:38Z (copied beside this brief: J13_READY_0238Z.txt, a CLAIM, not evidence). Routing v1.0 tier-2 gate row (test-only follow-up to a gated head). Secuura only.
Project path: /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files (READ ONLY: ls-remote, show, diff, cat-file only; never fetch, worktree or any write verb there; clone or `git clone --shared` into YOUR scratch and work there).

Gate P1 gave round 4 (head d2564aeb587bcbd7d9628495e83913c710ca0043, landing tree 524b5d203a18) GO WITH NOTE: read 0_Brain/reference/2026-10-19_gate-P1-pr1568-r4/verdict.md (relative to /Volumes/DevMASTER/WEDNESDAY/) for context. P1 left anchoring's KS-1385 integration suite NOT tested; J then found it red 2/54 (XT1/XT2 pinned 050's constraint name, but 051's trigger fires first by name order). Wednesday ruled a test-only fix.

develop = 37834600a543cb0276f427d969ac034d9df74fbd; new head = d74b7f951de81a054b6d6b9403352e1a598b5019 (both Wednesday ls-remote just before this brief; re-read them).

## Questions (each with its instrument, or "unmeasured")
1. `git diff --stat d2564aeb587b d74b7f951de8`: exactly one file, `services/anchoring/src/__tests__/ks1385-anchor-store-keeps-the-latest-events-metadata.integration.test.ts`? Read the hunks: do XT1 and XT2 still assert the refusal (23505) AND that tenant A's identity is kept? Is anything weakened (a removed assertion, a loosened matcher)?
2. Is the 051-first claim true? Read the two trigger names in the migrations and PG's rule (same-timing row triggers fire in name order); one sentence.
3. Predicted landing tree onto develop (merge-tree): J says 24cc02989cf1ad06565b718f1227393e5ec81f46. Recompute.
4. If you can run PostgreSQL in your scratch (no Docker): run anchoring's KS-1385 integration suite on the landing tree (J: 56/56), and one bite (revert XT1's constraint name, expect exactly XT1 red; restore). If you cannot, say "unmeasured" and why; do not improvise a substitute.
5. NOT tested: list by name every suite of anchoring/originate you did not run.

Verdict file: verdict.md in this folder; first line `VERDICT: GO | GO WITH NOTE | NO GO at head d74b7f951de8...`; last line the sha256 of the file with its first line deleted. Scratch: your own r1/ under /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/c4419525-d2e2-49d0-8b3f-577263d823bb/scratchpad/. Findings only: no fixes, no GitHub or Linear writes, no writes under !CODING, no `cd`, no `rm`, no stderr to /dev/null.
