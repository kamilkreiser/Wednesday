# Gate brief: GATE BQ1 = PR #1656 (KS-1679 follow-up: the #1619 cell in ks1557-verify-trusts-certification-evidence that #1646 made red on develop, updated to the stricter behaviour), Sonnet 5.5, TIER 2, round 1 of 2

Commissioned by Wednesday after Seat C 31st's READY FOR GATE (23:52Z). The author's CLAIM is beside this brief: `READY_CLAIM.txt` (read it WHOLE). The ruling: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-20_answer_seatC31_status_2308.md` item 3.

**Project:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ ONLY. Clone INSIDE `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/2a56ac36-e9ca-49f4-8d2d-f02d4a53f9ed/scratchpad/gate_bq1/` via `git clone --shared /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src <that folder>/src`; fetch `refs/pull/1656/head` and develop there (repoint that scratch clone's origin to GitHub with a repo-local sshCommand only if the PR ref is missing, read-only, as gate BM1 did). npm ONLY with an explicit cwd inside that clone; build `packages/shared` before any service suite.

**Heads (Wednesday's ls-remote, ~10:3x AEDT 2026-10-20):** #1656 head `2e672d35fedfa751c5607f9a777b6ff5399a9877`; develop `6229a92f2480f0784c31a8d6b652298a7ac10551`. Re-read both at start and end. **Derive the landing tree yourself** on live develop (the author's figure may predate #1651/#1652).

**Verdict file:** `verdict.md` in this folder. First line: `VERDICT: <GO|GO WITH NOTE|NO GO> at head 2e672d35fedf... (tier 2, round 1 of 2; landing tree <sha> on develop <sha>; N blockers, M notes)`. Then BLUF, findings, FOUND / TESTED / HOW, NOT RUN, wall-clock. Last line: the sha256 of `sed '1d;$d' verdict.md`, labelled with that method.

**Rules:** findings only; no GitHub or Linear writes; nothing under `!CODING`; no push; no `cd`; no `rm`; no stderr to /dev/null; no Docker (another seat uses it); every zero with a positive control; red by ASSERTION, never by load failure; each mutant `tsc` rc 0 before it counts; restore asserted after every arm. Before finishing run `git -C /Volumes/DevMASTER/WEDNESDAY status --short` and report every untracked path outside 0_Brain/, 5_Project_History/, 2_Project_Files/local-model/ and 2_Project_Files/fleet/briefs_staged/.

## Questions (instrument for each; name what you did NOT run)
**Escalate to TIER 1** if any non-test byte changes.
1. **Test-only, measured:** three-dot file set, byte-level.
2. **The red on develop is real and this fixes it:** the cell fails at develop by assertion (1/16 at the author's base) and passes at the head; at `937c7d10b^` (the parent of #1646) the UPDATED cell is red as the ONLY failure (the author's claim), proving it pins #1646's stricter behaviour.
3. **The fail-closed intent survives:** the updated cell still asserts the caller cannot CHOOSE the evidence (the forged certificationId is dropped, the derived row carries the server's id). Apply one mutant that reverts #1646's drop (re-admit a caller certificationId) and show the cell red by assertion.
4. **The author's staged-revert trap** (named in the claim): read it, reproduce or refute it in one line.
5. **No weakening:** the ks1557 verify suite and the originate suite by cell NAME at develop vs the landing.
6. **Landing:** merge-tree on live develop; tsc rc 0.
