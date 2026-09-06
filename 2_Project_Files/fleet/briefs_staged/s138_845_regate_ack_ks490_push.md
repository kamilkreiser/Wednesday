## BLUF
**#845 fix round @ `59248bf3841ac0354f1c2ae0e8600756d26d828d` RECEIVED → under its NARROW tier-1 re-gate (launched @LAUNCH@) — round 2 of 2 under the cap; HELD. The measurement that changed the fix (the prefix mount closes 3 of 6) is the right kind of act and is carried into the gate as a claim to re-derive. Meanwhile: PUSH the parked KS-490 branch and open its PR (READY mail with the `inspect` figure and the unresolved `docker images` discrepancy stated as you stated it) — its tier-2 gate follows the re-gate verdict.**

## 1. The re-gate
Brief `2_Project_Files/fleet/qa-agent/briefs/2026-09-06_secuura-ks843-845-half2-regate-59248bf38-tier1.md`; pane `QA/Secuura-s138-ks843-half2-regate`; ~30 min; verdict mail `[QA -> Wednesday] Secuura KS-843 HALF 2 RE-GATE @ 59248bf38 (PR #845, tier 1, round 2 of 2)`. The tester re-drives the six shapes and its own 20-shape table with its pass-1 harness in both modes, measures the hand-run chain's fidelity to express (a response stops it; an error reaches `next(err)`; the exhausted chain hands the ORIGINAL spelling to the catch-all), runs five red-proofs on the new test, reads the rewritten scope-gate test whole, confirms F-8, and re-derives KS-858's population under BOTH predicates (yours: two; the tester's: six — the ticket is right to say re-derive). **A NO GO here ships nothing on #845: it stays HELD and the residue goes to Kam.** Nothing on the branch until the verdict.

## 2. KS-490 — push it now
`kamilkreiser/ks-490-drop-build-toolchain-from-runtime-stages` @ `b9450d1ca` (your local): push, open the PR (Peter requested), mail READY with: the five Dockerfiles' before/after; the driven proof (auth built both ways, argon2 prebuilds 8/8, a real hash succeeds); **the image size by `docker image inspect` (219.6 → 122.1 MB) with the `docker images` 5× disagreement stated UNRESOLVED, as you wrote it** — the gate will measure which instrument is right; where the guard cell lives (or that it is named on the ticket for the `scripts/` partition). No rebase, no force. Then (2) the governance dev tree as ruled at 12:02, measurement first.

## 3. Standing
develop `e08472c6ef44ccede29001a64fdba5f4b5a20c0b` (seat B's #843/#844 are merging on the 12:3x GO — re-read at branch time). FULL SHAs in every KS-843 mail. The `STATE:` line at the top of every mail from here (adopted fleet-wide 12:3x). No deploy; nothing on the demo; never `--no-verify`; never delete a branch; the cutover is Kam's card.

PROVENANCE:
- Your READY (the six shapes before/after; the prefix-vs-collapsed table; the 6-cell test + its 1/5 red-proof; 9/9 + 7/7; F-8 by removal; KS-858 with two candidates; 255 → 260; project tsc 0 / the standalone-tsc disclosure; KS-490 parked) | `READY: #845 fix round @ 59248bf38…` 2026-09-06T02:13:37Z, read whole | read 2026-09-06 12:3x
- `refs/pull/845/head` = `59248bf38…`; develop `e08472c6e…` | `git ls-remote origin` at 12:4x | 12:4x
- The round-2 diff (`proxy.ts` + the new test READ WHOLE; the rewritten scope-gate test and the doc by stat) | Wednesday's own read | 12:4x
- The gate launch | `cockpit.sh add` receipt in Wednesday's own output | @LAUNCH@

SELF-CHECK: re-read end-to-end | 2026-09-06 @NOW@
(checked: the launch line is from the receipt; the cap's consequence stated once; KS-490's push is an act on a branch NOT under gate; the discrepancy is carried as the builder stated it, not resolved by Wednesday; consistent with the 12:02 and 12:05 rulings; no NexusAI content.)
