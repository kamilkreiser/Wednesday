# Gate brief: GATE AC1 = PR #1617 (KS-1629), Opus, tier 1, round 1 of 2

Commissioned by Wednesday after Seat J 15th's READY FOR GATE of 08:32Z. The author's CLAIM is beside this brief: `J15_READY_0832Z.txt`. Secuura only.

**Project:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ ONLY (ls-remote, show, diff, cat-file, log). Every write verb runs in your own clone in your scratch: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/dd32393e-b87e-4d51-ac65-b22e5897a2c1/scratchpad/ac1/`.

**What it is:**
- **The defect:** originate `routes/anchors.ts` GET, `!anchor` branch. Under `SIMULATE_ANCHORING=true` it synthesized a `tx_sim_` anchor and PERSISTED it (`saveAnchorToDb`), for any id named. Since migration 051, that row then blocks the document's own later registration with a 409.
- **The ruling (Wednesday's (b), 19:0x AEDT):** with no anchor row the route returns 404 whatever SIMULATE_ANCHORING says: no synthesis, no write. The existing `ks520-anchor-fail-closed.test.ts` cell that pinned the synthesized 200 is re-pinned to the 404, and that is disclosed.
- **Context, read by the author on both boxes:** SIMULATE_ANCHORING is unset on demo and kintsugi, so the bug is live only under the opt-in.
- **Heads:** #1617 head `f8b3bf0cd313e1a2505094514262ff8f43387dd2`; develop `8323f2f70cd796219774f240184f777813c28aec` (Wednesday ls-remote 19:3x). The author predicts landing tree `83c945a644b8`.

## Questions (each with its instrument; name what you did NOT run)
1. **Is the read path now a pure read in EVERY mode?** Read the whole GET handler at the head. Under the opt-in true, unset, and any other value: is there any remaining write (`saveAnchorToDb`, `$executeRaw`, `$queryRaw` INSERT/UPDATE) reachable from this GET? Count the mocks' write calls.
2. **Did the change go too far?**
   - A REAL anchor row still answers 200 under the opt-in (C1).
   - A genuinely simulated stored anchor is still labelled honestly (C2; the KS-587/522 behaviour).
   - The verify routes that read anchors are unaffected: name them and read them.
3. **The re-pinned ks520 assertion:** read the old and new expectation. Is it an honest contract change, matching the ruling, rather than a weakening? Do the other 9 ks520 cells still pin KS-520's property (no fabrication outside the opt-in)?
4. **Consumer census:** independently re-run the author's census.
   - Who else depends on a synthesized 200 from this GET? Check tests, the schemathesis modes (orchestration.py ~:311/:332), docs, the OpenAPI, and any frontend.
   - Use POSIX classes in `git grep -E` (`\s` is dead there). Run a control that exercises the same regex feature.
5. **Red-first and controls are real:** 4 red / 3 green with the product at develop. Plant one mutation of your own (for example, restore the persist) that must red A2.
6. **Landing:**
   - merge-tree onto the LIVE develop (re-read at start and before the verdict);
   - originate suite on the landing tree (claim 1488/1488, 123 suites; the parent 1481);
   - tsc including the tests;
   - the three-dot list must be exactly the 3 files.
   Build `packages/shared` first (`npm run build --workspace=packages/shared`) and run Prisma via `npm run generate --workspace=services/originate`.

**Verdict file:** `verdict.md` in this folder.
- First line: `VERDICT: <GO|GO WITH NOTE|NO GO> at head f8b3bf0cd313... (tier 1, round 1 of 2; landing tree <sha> on develop <sha>; N blockers, M notes)`.
- Last line: the sha256 of `sed '1d;$d' verdict.md | shasum -a 256`.

**Rules:**
- Findings only: no fixes, no GitHub or Linear writes, nothing under `!CODING`.
- No `cd`, no `rm`, no stderr to /dev/null, no Docker.
- Every zero gets a positive control.
- The shell is zsh: no PIPESTATUS.
