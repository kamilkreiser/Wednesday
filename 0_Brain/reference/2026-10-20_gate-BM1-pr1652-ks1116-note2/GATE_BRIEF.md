# Gate brief: GATE BM1 = PR #1652 (KS-1116 gate BJ1 NOTE 2: two surviving-mutant shapes pinned in the vc-issuer owner-less read refusal table), Sonnet 5.5, tier 2 (test-only follow-up), round 1 of 2

Commissioned by Wednesday after Seat C 31st's READY FOR GATE (23:18Z). The author's CLAIM is beside this brief: `C31_READY_2318Z.txt` (read it WHOLE). Source of the residue: gate BJ1's `0_Brain/reference/2026-10-20_gate-BJ1-pr1649-ks1116-a/verdict.md` NOTE 2 (mutants JM8 role widening, JM11 tenant prefix match).

**Why tier 2, and when to escalate:** test-only, one file. If any non-test byte changes, say TIER 1 and stop at the finding.

**Project:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ ONLY. Clone INSIDE `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/2a56ac36-e9ca-49f4-8d2d-f02d4a53f9ed/scratchpad/gate_bm1/` via `git clone --shared /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src <that folder>/src`, fetch the PR branch `test/ks-1116-bj1-note2-surviving-mutant-cells` and develop there. npm ONLY with an explicit cwd inside that clone.

**Heads (Wednesday's ls-remote, ~10:2x AEDT 2026-10-20):** #1652 head `a4d5aa81f3bae82cd9d23cbdc11692052eb5a8dd` (= refs/pull/1652/head); develop `cd63883c62a9bb0e66969df8cd3f02db2b9b2217` (moved past the PR's base 89956fe92956 via #1650, which touches packages/shared comments + m365 tests). Re-read at start and end. **Derive the landing tree yourself** (merge-tree on live develop); the author gave none on the new develop.

## Questions
1. **Test-only, measured:** three-dot file set; zero bytes changed in `ownership.ts` or any non-test file.
2. **The cells bite:** re-apply JM8 (role set widened to TENANT_ADMIN/SUPER_ADMIN) and JM11 (`rowTenantId.startsWith(claim)`) yourself on a snapshot, each `tsc` rc 0, red by ASSERTION (not load failure), restore asserted; plus one mutant of your own on the same predicate the author did not run. Confirm A0 (the fixture guard) can fail: break the prefix fixture and show A0 red.
3. **No weakening:** vc-issuer suite by cell NAME at develop vs the landing (author: 18 files / 291, KS-1116 file 131). **Build `packages/shared` first** (`npm run build --workspace=packages/shared` in your clone): vc-issuer consumes its built dist, and #1650 changed a shared source comment.
4. **Landing:** merge-tree on live develop; the landing tree sha; vc-issuer `tsc --noEmit` rc 0 at the landing.

**Verdict file:** `verdict.md` in this folder. First line: `VERDICT: <GO|GO WITH NOTE|NO GO> at head a4d5aa81f3ba... (tier 2, round 1 of 2; landing tree <sha> on develop <sha>; N blockers, M notes)`. Then BLUF, findings, FOUND / TESTED / HOW, NOT RUN, wall-clock. Last line: the sha256 of `sed '1d;$d' verdict.md`, labelled with that method.

**Rules:** findings only; no GitHub or Linear writes; nothing under `!CODING`; no push; no `cd`; no `rm`; no stderr to /dev/null; no Docker; every zero with a positive control. Before finishing run `git -C /Volumes/DevMASTER/WEDNESDAY status --short` and report every untracked path outside 0_Brain/, 5_Project_History/, 2_Project_Files/local-model/ and 2_Project_Files/fleet/briefs_staged/.
