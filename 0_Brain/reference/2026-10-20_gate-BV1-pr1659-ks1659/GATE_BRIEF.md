# Gate brief: GATE BV1 = PR #1659 (KS-1659: fold the holder/actor id to a UUID-or-NULL before it reaches owner_user_id, so a connector principal no longer breaks the write), Sonnet 5.5, TIER 2, round 1 of 2

Commissioned by Wednesday after Seat G 12th's READY FOR GATE (00:53:05Z). The author's CLAIM is beside this brief: `READY_CLAIM.txt` (read it WHOLE). The tier is 2 ONLY because the author measured that no reader trusts a non-null `owner_user_id`; **if you find a reader that admits on it (or on NULL), say so in your first line and stop treating this as tier 2** — that is the most important question.

**Project:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ ONLY. Clone INSIDE `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4cf20ec9-03c1-4724-89c4-ae3e1635cfad/scratchpad/gate_bv1/` via `git clone --shared /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src <that folder>/src`; fetch `refs/pull/1659/head` and develop there. npm ONLY with an explicit `--prefix`/cwd inside that clone, never from the WEDNESDAY tree; build `packages/shared` before any service suite.

**Heads (Wednesday's ls-remote, 11:5x AEDT 2026-10-20):** #1659 head `97eaffe0d3003390f244ea0d0319b988a6cf6464`; develop `610570e5a75790d8ebf4264c4aec3ec8bebc0609`. Re-read both at start and end. Derive the landing yourself (author: `2ba4f69bfbd4`).

**Verdict file:** `verdict.md` in this folder. First line: `VERDICT: <GO|GO WITH NOTE|NO GO> at head 97eaffe0d300... (tier 2, round 1 of 2; landing tree <sha> on develop <sha>; N blockers, M notes)`. Then BLUF, findings, FOUND / TESTED / HOW, NOT RUN, wall-clock. Last line: the sha256 of `sed '1d;$d' verdict.md`, labelled with that method.

**Rules:** findings only; no GitHub or Linear writes; nothing under `!CODING`; no push; no `cd`; no `rm`; no stderr to /dev/null; no Docker; every zero with a positive control; red by ASSERTION, never by load failure; each mutant compiles before it counts; restore asserted after every arm. Before finishing run `git -C /Volumes/DevMASTER/WEDNESDAY status --short` and report every untracked path outside 0_Brain/, 5_Project_History/, 2_Project_Files/local-model/ and 2_Project_Files/fleet/briefs_staged/.

## Questions (instrument for each; name what you did NOT run)
1. **The tier claim:** read `anchorOverwriteGuard.ts:164-170` and `:212` (sameUuid(null,x) false -> deny) and `verification.ts:334` (NULL == NULL via `?? ''`, inside four other conjuncts). Do your OWN census of `owner_user_id` readers in originate (author: 116 reads over 48 files) and name any that admits on equality with NULL or on a non-null value the fold can now produce.
2. **The fold:** `toActorUuid` on a real UUID, a connector principal, null, undefined, '', 'not-a-uuid', and an uppercase UUID: does each store what it should (UUID kept, everything else NULL)? Is anything that USED to be stored now lost (a valid id folded away)?
3. **The test file is type-checked by nobody** (preflight leg 16 does not cover originate; `tsc -p services/originate` excludes tests): type-check it in its own program and report rc.
4. **No weakening + landing:** originate unit suite by cell NAME at develop vs the landing (author: 134/1568 -> 135/1575, 0 vanished); `ks564-certification-issuer-uuid` 8/8; re-run 3 of the author's 5 mutants plus 1 of your own; merge-tree on live develop.
5. The author's side finding (`certifications.ts:343` checks holderId only when supplied; `:827` maps any owner_user_id error to a 400): confirm or refute from the code, one line each. Not a blocker for this PR.
