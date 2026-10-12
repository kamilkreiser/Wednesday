# Gate brief: Secuura Platform K PR #1515 (KS-1517), round 2 CLOSING AMENDMENT — SONNET tier 3, NARROW delta gate

Commissioned 2026-10-13 ~05:3x AEDT by the Wednesday seat. Round 2 of 2 under the cap: this is the last gate on this class; Wednesday ruled no third Opus round (17:59Z ANSWER to V).

## What you are gating
- Head `a7d0583dd171992d661a725a70659529d3209d5c` (Wednesday's ls-remote). Previous gated head `6c73effcf9a60279363ac024c77b66ae060372d5` (Opus round-2 verdict: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-13_gate-pr1515-r2/verdict.md`, NO GO, one latent Major MJ1 plus minors). Read that verdict first.
- Delta: one commit 0723117b plus a merge of develop 425ad3e0 (never rebased). Author V 5th reports numstat on the PR's files: check.cjs +36/-12; the ks1000 test +75/-2; CLAUDE.md +15/-6.
- The four ruled items: (1) MJ1: source scan reads only regular files under a 4 MiB cap; the whole note block in try/catch; new cells (16.8 MB file, FIFO, null package.json); (2) the corroboration cell uses the previous gate's R2 fixture, mutants on a green baseline; (3) the TS2307/TS7016 code check restored and the message regex anchored; (4) CLAUDE.md and comment wording.
- Residue filed by V as KS-1546 (P3). Not yours to re-gate.

## How to get the code (READ-ONLY on the project)
- Project checkout `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ-ONLY. `git clone --shared` into YOUR scratchpad; fetch `refs/pull/1515/head` and develop there with the project's `core.sshCommand`, or use V's bundle `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-12_seatV-5th/bundles/ks1517-delta-6c73effc-to-a7d0583d.bundle` (sha256/16 d1a73a173c182ec8, verified; needs 6c73effc and 898a1ae1). Assert the head first. No pushes, no GitHub/Linear writes.

## Narrow scope
1. Each of the four items, against the previous gate's shapes: re-run MJ1's G5 (huge file) and G7a (FIFO) shapes and the E1/E1b/E2 shapes (m2); confirm rc 0 / no hang / never CANNOT RUN as the author states.
2. The try/catch must not swallow a real tsc-driven verdict: plant one genuine new TS2307 on an imported, unbuilt subpath and confirm it still exits non-zero for the right reason.
3. Kill at least C1, C5 and the try/catch-removal mutant yourself on a green baseline.
4. ks1000 suite, services/auth suite once, check:test-types, at the head; compare with develop.
5. The develop merge: the PR's files keep their blobs; develop's files equal develop's.
6. Do NOT re-litigate the residue in KS-1546; only say if anything in it should block.

## Output
- `0_Brain/reference/2026-10-13_gate-pr1515-r2c/verdict.md` (this folder only, plus your scratchpad). Head under test; every number with its instrument and a control; FOUND / TESTED / HOW; NOT tested.
- VERDICT: GO / GO WITH NOTE / NO GO; Majors and Minors with file:line and the reproducing shape.
