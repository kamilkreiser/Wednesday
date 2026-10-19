# Gate brief: GATE AE1 = PR #1619 (KS-1557 write side), Opus, tier 1, round 1 of 2

Commissioned by Wednesday after Seat G 11th's READY FOR GATE of 08:40Z. The author's CLAIM is beside this brief: `G11_READY_0840Z.txt`. Secuura only.

**Project:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ ONLY (ls-remote, show, diff, cat-file, log). Every write verb runs in your own clone in your scratch: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/dd32393e-b87e-4d51-ac65-b22e5897a2c1/scratchpad/ae1/`.

**What it is:**
- **The defect:** originate `POST /api/certifications/issue`, lineage branch (`parentDocumentId` set). It checked only for cycles, so any write-role caller could name ANOTHER organisation's document as the parent and give it a child row.
- **The fix:** the same predicate as the legacy branch (`callerMayCertifyDocument`, `certifications.ts:117`), refused BEFORE the cycle walk, the anchoring POST and both saves.
- **Parent resolution:** `getDocument(parentDocumentId, tenant)` plus an identity guard `parentDocument.id === parentDocumentId`, so the check applies only when the row was found by `external_id`, the row the write links. A pkey-only match keeps today's 201 and links nothing.
- **Shape history:** Wednesday ratified a separate existence-read shape; the author replaced it because that shape made 18 cells 500. Wednesday accepted the change as a SHAPE only. Correctness is yours to judge.
- **Re-pinned cells:** 6 in ks1213/ks1508/ks1228/ks1538.
- **Heads:** #1619 head `894468de3dbbce71bd36015d8465b5dc9a07033e`; develop `8323f2f70cd796219774f240184f777813c28aec`. The author predicts landing tree `45f61469230d`.

## Questions (each with its instrument; name what you did NOT run)
1. **Is the identity guard exact?** The author measured both arms. With migration 050 live, an external_id = another row's pkey collision is refused (23505). With 050 disabled, the check path and the write path resolve the SAME (attacker-owned) row.
   - Re-measure both arms.
   - Find any third resolution of "the parent" in the request: certifications, saveDocument, saveCertification, the anchoring POST body. Each must resolve the same row.
   - Is "a pkey-only match = no check, 201, links nothing" truly linking nothing? Read the write.
2. **Ordering:** the access check precedes the cycle walk, and ks1228's 422 cell gained connector access to keep its subject. Defensible, or a weakening?
3. **The six re-pinned cells:** read every old and new assertion side by side. Is each an honest contract change? The ks1538 cell that asserted "the lineage path does not run this check" is deleted: confirm it encoded the defect. Does each remaining fixture answer the REAL predicate for its own ids, so a different connector is still refused?
4. **Red-first and controls are real:**
   - check the claim of 6 red / 7 green on untouched develop;
   - the four constraining controls (UNCHANGED, PKEY CORNER, Stuart's S shape `c1712c38`, ITEM5c open) stay green at both ends;
   - plant one mutation of your own (for example, drop the identity clause, which must red a cell).
5. **Landing:**
   - merge-tree onto the LIVE develop (re-read at start and before the verdict);
   - the new integration suite (13 cells) in BOTH tenancy modes on a scratch PostgreSQL (port 55410-55419, built from `docker/init/*` + migrations, per-file `[main] Applying` lines);
   - the originate unit suite;
   - tsc including tests;
   - the three-dot list must be exactly the PR's 7 files.
   Build `packages/shared` first; Prisma via `npm run generate --workspace=services/originate`.
6. **Boxes:** which deployed boxes have migration 050 applied? You cannot read the boxes; say UNMEASURED, and say whether the guard's exactness depends on it (the author says it does not).

**Verdict file:** `verdict.md` in this folder.
- First line: `VERDICT: <GO|GO WITH NOTE|NO GO> at head 894468de3dbb... (tier 1, round 1 of 2; landing tree <sha> on develop <sha>; N blockers, M notes)`.
- Last line: the sha256 of `sed '1d;$d' verdict.md | shasum -a 256`.

**Rules:**
- Findings only: no fixes, no GitHub or Linear writes, nothing under `!CODING`.
- No `cd`, no `rm`, no stderr to /dev/null, no Docker.
- Every zero gets a positive control.
- The shell is zsh: no PIPESTATUS.
