# Gate brief: GATE AG1 = PR #1621 (KS-1634 v2 site), Opus, tier 1, round 1 of 2

Commissioned by Wednesday after Seat R 54th's READY FOR GATE of 08:59Z. The author's CLAIM is beside this brief (`R54_READY_0859Z.txt`; the #1621 section is near its end). Secuura only.

**Project:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ ONLY (ls-remote, show, diff, cat-file, log). Every write verb runs in your own clone in your scratch: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/dd32393e-b87e-4d51-ac65-b22e5897a2c1/scratchpad/ag1/`.

**What it is:**
- **The defect:** originate `routes/verificationV2.ts` `chainOnlyMatch` built the blob for `presentBlockchainHonestly` without the reply's `simulated` flag, so on a registry miss a SIMULATED anchor was presented as on-chain (`anchored: true`, a tx hash).
- **The fix:** one line, `simulated: chain.simulated`. It is the v2 twin of #1597's v1 fix.
- **Cells:** 7 = 5 from a held Spark pass (2 RED + 3 CONTROL) + 2 hand-written by the author: Stuart's S-shaped case (a fresh v4 documentId with no documents row, verified through v2) and its inverted control. The S case is an IN-PROCESS substitute. The PR body states what it does NOT exercise (`POST /api/anchors` under a connector key, the gateway hop, anchoring's write path). The end-to-end is Stuart's own `@k-live` run, after a deploy.
- **Missing artefacts:** no golden diff and no `index` lines exist for this pass (measured by the author). Its claim rests on the behavioural pair, the tamper, and a strict re-apply at the live tip.
- **Heads:** #1621 head `0810a2edad9521ea826634be79115e5cb52a103c`; develop `6ec1b7badb9b9fc1cd8d8cfe63b6cd61b8ce7b63`. The author predicts landing tree `548beee35fe5`.

## Questions (each with its instrument; name what you did NOT run)
1. **Is the honesty rule now applied on EVERY v2 path that can present a chain-only or simulated anchor?**
   - Read the whole of verificationV2.ts. List every place a blob reaches `presentBlockchainHonestly` (or builds `anchored`/tx fields) and say whether each carries `simulated`.
   - A sibling path left behind is the exact shape of this defect: v1 was fixed and v2 left.
2. **Does a REAL on-chain anchor still present as on-chain** (CONTROL cells)? Does a missing or undefined `simulated` behave as before (`Boolean(simulated)`, KS-1069 E12: truthy refuses, presence does not)?
3. **Stuart's S cell:**
   - Is it genuine? Check the v4 id, the "db asked and answered no rows" guard, and that removing the product line reds it while its inverted control stays green.
   - Is the in-process substitution honestly scoped in the PR body?
4. **Red-first and controls:** 2 red / 3 green at develop for the held cells; 7/7 with the fix. Plant one mutation of your own (for example `simulated: false` hard-coded), which must red.
5. **Landing:** merge-tree onto the LIVE develop (re-read at start and before the verdict). Run the originate unit suite on the landing tree (claim 1502/1502 in 125; parent 1495/124) and tsc including tests. The three-dot list must be exactly the PR's 2 files. Build `packages/shared` first; Prisma via `npm run generate --workspace=services/originate`.

**Verdict file:** `verdict.md` in this folder.
- First line: `VERDICT: <GO|GO WITH NOTE|NO GO> at head 0810a2edad95... (tier 1, round 1 of 2; landing tree <sha> on develop <sha>; N blockers, M notes)`.
- Last line: the sha256 of `sed '1d;$d' verdict.md | shasum -a 256`.

**Rules:**
- Findings only: no fixes, no GitHub or Linear writes, nothing under `!CODING`.
- No `cd`, no `rm`, no stderr to /dev/null, no Docker.
- Every zero gets a positive control.
- The shell is zsh: no PIPESTATUS.
