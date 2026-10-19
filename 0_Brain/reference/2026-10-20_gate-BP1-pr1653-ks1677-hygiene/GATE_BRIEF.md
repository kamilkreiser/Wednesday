# Gate brief: GATE BP1 = PR #1653 (hygiene: KS-1677 NB1 wording fixed (gate BK1 NK1), a V4 provenance cell, and the stale BACKLOG.md entry closed), Sonnet 5.5, TIER 2, round 1 of 2

Commissioned by Wednesday after the author's READY FOR GATE. The author's CLAIM is beside this brief: `READY_CLAIM.txt` (read it WHOLE).

**Project:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ ONLY. Clone INSIDE `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/2a56ac36-e9ca-49f4-8d2d-f02d4a53f9ed/scratchpad/gate_bp1/` via `git clone --shared /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src <that folder>/src`; fetch `refs/pull/1653/head` and develop there (repoint that scratch clone's origin to GitHub with a repo-local sshCommand only if the PR ref is missing, read-only, as gate BM1 did). npm ONLY with an explicit cwd inside that clone; build `packages/shared` before any service suite.

**Heads (Wednesday's ls-remote, ~10:3x AEDT 2026-10-20):** #1653 head `b30e401ff208940f6e44b44696dd4ab1ff141a98`; develop `11af03696c9bd966580e52605cb2a361d9c3d29b`. Re-read both at start and end. **Derive the landing tree yourself** on live develop (the author's figure may predate #1651/#1652).

**Verdict file:** `verdict.md` in this folder. First line: `VERDICT: <GO|GO WITH NOTE|NO GO> at head b30e401ff208... (tier 2, round 1 of 2; landing tree <sha> on develop <sha>; N blockers, M notes)`. Then BLUF, findings, FOUND / TESTED / HOW, NOT RUN, wall-clock. Last line: the sha256 of `sed '1d;$d' verdict.md`, labelled with that method.

**Rules:** findings only; no GitHub or Linear writes; nothing under `!CODING`; no push; no `cd`; no `rm`; no stderr to /dev/null; no Docker (another seat uses it); every zero with a positive control; red by ASSERTION, never by load failure; each mutant `tsc` rc 0 before it counts; restore asserted after every arm. Before finishing run `git -C /Volumes/DevMASTER/WEDNESDAY status --short` and report every untracked path outside 0_Brain/, 5_Project_History/, 2_Project_Files/local-model/ and 2_Project_Files/fleet/briefs_staged/.

## Questions (instrument for each; name what you did NOT run)
**Escalate to TIER 1** if any non-test, non-docs byte changes.
1. **Test/docs-only, measured:** three-dot file set, byte-level.
2. **NK1 closed:** the test no longer claims CSPRNG it does not pin, or now pins it; re-apply gate BK1's BK-X1 (`Math.random` bytes) on a snapshot and show the new V4 red by assertion (the author claims V4 kills BK-X1 alone).
3. **The BACKLOG.md entry:** the author says it was already fixed by #1337 and re-ran the named cell; confirm the cell exists, runs and passes at develop (positive control), and that the docs change says so accurately.
4. **No weakening:** m365 suite by cell NAME at develop vs the landing.
5. **Landing:** merge-tree on live develop; tsc rc 0.
