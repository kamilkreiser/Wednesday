# Gate brief: GATE AD1 = PR #1618 (KS-1642, both pieces), Sonnet, tier 2, round 1 of 2

Commissioned by Wednesday after Seat R 54th's READY FOR GATE of 08:35Z. The author's CLAIM is beside this brief: `R54_READY_0835Z.txt`. Secuura only.

**Why tier 2:** a defensive guard in a 409-mapping helper, plus test-only cells.

**Project:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ ONLY (ls-remote, show, diff, cat-file, log). Every write verb runs in your own clone in your scratch: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/dd32393e-b87e-4d51-ac65-b22e5897a2c1/scratchpad/ad1/`.

**What it is:** originate `src/utils/idNamespaceCollision.ts`.
- **Piece 1:** the helpers read every field ONCE, up front, inside a `try`, so an unreadable error node (a throwing getter, or a Proxy whose `ownKeys` throws) yields "not a collision" instead of throwing out of a 409 mapper. The old "never throws" comment is replaced. One new test file with 5 cells.
- **Piece 2:** test-only. RED H9 + CONTROL H9c added to `ks1612-409-mapping-survives-the-prisma-error-shape.test.ts`. They pin the `r.constraint === null` arm of `isMigrationRefusal`, which piece 1 moves from line 84 to 87.
- **Heads:** #1618 head `4521a6f629b0c669ffbbe47798ebdcfb830d231b`; develop `8323f2f70cd796219774f240184f777813c28aec`. The author predicts landing tree `46d3e6b7a9a0`.
- **Origin:** both pieces were Spark passes, held after Wednesday's source read. Judge the code.

## Questions
1. **Does the guard change any answer for a READABLE error?** Every existing mapping cell (ks1612 and every other caller of these helpers) must give the same result. Name the callers.
2. **Is "unreadable means not a collision" the right default** for a 409 mapper (the safe direction), and does any caller now swallow an error it previously surfaced?
3. **Red-first and the mutant kill are real.** Check piece 1's 3 reds at develop. For piece 2, delete `r.constraint === null &&` at line 87: H9 must red and H9c stay green. Restore byte-identical.
4. **Landing:** merge-tree onto the LIVE develop (re-read at start and before the verdict). Run the originate unit suite on the landing tree (claim 1488/1488, 123 suites) and tsc. The three-dot list must be exactly the 3 files. Build `packages/shared` first; run Prisma via `npm run generate --workspace=services/originate`.

**Verdict file:** `verdict.md` in this folder.
- First line: `VERDICT: <GO|GO WITH NOTE|NO GO> at head 4521a6f629b0... (tier 2, round 1 of 2; landing tree <sha> on develop <sha>; N blockers, M notes)`.
- Last line: the sha256 of `sed '1d;$d' verdict.md | shasum -a 256`.

**Rules:**
- Findings only: no fixes, no GitHub or Linear writes, nothing under `!CODING`.
- No `cd`, no `rm`, no stderr to /dev/null, no Docker.
- Every zero gets a positive control.
- The shell is zsh: no PIPESTATUS.
