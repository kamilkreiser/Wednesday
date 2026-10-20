# Gate brief: GATE BR1 = PR #1658 (KS-1682 gate BL1 N1: cells pinning exact homeAccountId matching in the m365 refresh-token selector, plus BP1 NB3's cite fix), Sonnet 5.5, TIER 2 (test-only follow-up on a tier-1 surface), round 1 of 2

Commissioned by Wednesday after Seat R 58th's READY FOR GATE (23:58Z). The author's CLAIM: `READY_CLAIM.txt` beside this brief (read WHOLE). Source: gate BL1's verdict `0_Brain/reference/2026-10-20_gate-BL1-pr1651-ks1682/verdict.md` N1 (mutants G3 uid-part only, G4 case-insensitive, G5 trimmed, G6 substring, G7 entry with no account id).

**Project:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ ONLY. Clone INSIDE `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/2a56ac36-e9ca-49f4-8d2d-f02d4a53f9ed/scratchpad/gate_br1/` via `git clone --shared /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src <that folder>/src`; fetch `refs/pull/1658/head` and develop there (repoint that scratch clone's origin to GitHub with a repo-local sshCommand only if the PR ref is missing, read-only, as gate BM1 did). npm ONLY with an explicit cwd inside that clone; build `packages/shared` before any service suite.

**Heads (Wednesday's ls-remote, ~10:3x AEDT 2026-10-20):** #1658 head `2d1417f44c24224d2da4efb22f2ff847b6b4c4d5`; develop `6229a92f2480f0784c31a8d6b652298a7ac10551`. Re-read both at start and end. **Derive the landing tree yourself** on live develop (the author's figure may predate #1651/#1652).

**Verdict file:** `verdict.md` in this folder. First line: `VERDICT: <GO|GO WITH NOTE|NO GO> at head 2d1417f44c24... (tier 2, round 1 of 2; landing tree <sha> on develop <sha>; N blockers, M notes)`. Then BLUF, findings, FOUND / TESTED / HOW, NOT RUN, wall-clock. Last line: the sha256 of `sed '1d;$d' verdict.md`, labelled with that method.

**Rules:** findings only; no GitHub or Linear writes; nothing under `!CODING`; no push; no `cd`; no `rm`; no stderr to /dev/null; no Docker (another seat uses it); every zero with a positive control; red by ASSERTION, never by load failure; each mutant `tsc` rc 0 before it counts; restore asserted after every arm. Before finishing run `git -C /Volumes/DevMASTER/WEDNESDAY status --short` and report every untracked path outside 0_Brain/, 5_Project_History/, 2_Project_Files/local-model/ and 2_Project_Files/fleet/briefs_staged/.

## Questions (instrument for each; name what you did NOT run)
**Escalate to TIER 1** if any non-test, non-docs byte changes.
1. **Test/docs-only, measured:** three-dot file set, byte-level.
2. **The cells bite:** re-apply BL1's G3, G4, G5, G6 and G7 on `token-manager.ts` in a snapshot (each `tsc` rc 0), each red by ASSERTION, restore asserted; plus one mutant of your own on the selector the author did not run.
3. **No weakening:** m365 suite by cell NAME at develop vs the landing; build packages/shared first.
4. **Landing:** merge-tree on live develop; tsc rc 0; new tests type-checked in their own program.
