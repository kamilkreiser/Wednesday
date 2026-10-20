# Gate brief: GATE BW1 = PR #1660 (KS-1682 gate-BR1 residue: W6 made able to fail, cells for the startsWith / endsWith / empty-id near-miss mutants, a fourth conjunct pinned), Sonnet 5.5, TIER 2, round 1 of 2, TEST-ONLY

Commissioned by Wednesday after Seat R 59th's READY FOR GATE (00:56:34Z). The author's CLAIM is beside this brief: `READY_CLAIM.txt` (read it WHOLE). Gate BR1's verdict, whose residue this closes: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-20_gate-BR1-pr1658-ks1682-n1/verdict.md` (N1 X1/X2/X5 survive; N2 W6 cannot fail). Read its N1/N2.

**Project:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ ONLY. Clone INSIDE `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4cf20ec9-03c1-4724-89c4-ae3e1635cfad/scratchpad/gate_bw1/` via `git clone --shared /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src <that folder>/src`; fetch `refs/pull/1660/head` and develop there. npm ONLY with an explicit `--prefix`/cwd inside that clone, never from the WEDNESDAY tree; build `packages/shared` before any service suite. Gate BV1 runs at the same time in a sibling folder.

**Heads (Wednesday's ls-remote, 11:5x AEDT 2026-10-20):** #1660 head `1400219cf2b88cc60f08719bfa0295c8066c9b8c`; develop `610570e5a75790d8ebf4264c4aec3ec8bebc0609`. Re-read both at start and end. Derive the landing yourself.

**Verdict file:** `verdict.md` in this folder. First line: `VERDICT: <GO|GO WITH NOTE|NO GO> at head 1400219cf2b8... (tier 2, round 1 of 2; landing tree <sha> on develop <sha>; N blockers, M notes)`. Then BLUF, findings, FOUND / TESTED / HOW, NOT RUN, wall-clock. Last line: the sha256 of `sed '1d;$d' verdict.md`, labelled with that method.

**Rules:** findings only; no GitHub or Linear writes; nothing under `!CODING`; no push; no `cd`; no `rm`; no stderr to /dev/null; no Docker; every zero with a positive control; red by ASSERTION, never by load failure; each mutant compiles before it counts; restore asserted after every arm. Before finishing run `git -C /Volumes/DevMASTER/WEDNESDAY status --short` and report every untracked path outside 0_Brain/, 5_Project_History/, 2_Project_Files/local-model/ and 2_Project_Files/fleet/briefs_staged/.

## Questions (instrument for each; name what you did NOT run)
1. **Test-only:** the three-dot diff touches exactly one test file and no product, migration or config file.
2. **W6 can now fail:** reproduce T1 (empty one registered secret) and T2 (duplicate one): W6 reds, and confirm the author's claim that W1-W10 stay green under T1. Then try ONE tamper of your own that should red W6.
3. **X1 / X2 / X5:** apply each mutant to the product selector (startsWith, endsWith, accept ''), compiling; each reds exactly its new cell (W7, W8, W9). Re-run BR1's G3-G7 too.
4. **The fourth conjunct:** drop `typeof e.secret === 'string'`: W10 reds. Check the author's two "cannot be pinned" claims: `e &&` unreachable because msal's Deserializer throws on a null entry (cite msal-node line), and `e.secret !== ''` unobservable at the return value. Agree or refute, one line each.
5. **No weakening:** m365-integration 220 -> 224 by cell NAME (only W6's old title should vanish); the new file type-checked in its own program; merge-tree on live develop.
