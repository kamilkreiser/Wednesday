# Gate brief: GATE BN1 = PR #1654 (KS-1557: a connector may certify the documents it MINTED, via a new provenance action `create:connector` written by originate and /version, plus migration 055 backfilling version-minted documents), Opus 5.5, TIER 1, round 1 of 2

Commissioned by Wednesday after the author's READY FOR GATE. The author's CLAIM is beside this brief: `READY_CLAIM.txt` (read it WHOLE).

**Project:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ ONLY. Clone INSIDE `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/2a56ac36-e9ca-49f4-8d2d-f02d4a53f9ed/scratchpad/gate_bn1/` via `git clone --shared /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src <that folder>/src`; fetch `refs/pull/1654/head` and develop there (repoint that scratch clone's origin to GitHub with a repo-local sshCommand only if the PR ref is missing, read-only, as gate BM1 did). npm ONLY with an explicit cwd inside that clone; build `packages/shared` before any service suite.

**Heads (Wednesday's ls-remote, ~10:3x AEDT 2026-10-20):** #1654 head `db9bca740df08cd961044e3515a5cf4f2f760354`; develop `11af03696c9bd966580e52605cb2a361d9c3d29b`. Re-read both at start and end. **Derive the landing tree yourself** on live develop (the author's figure may predate #1651/#1652).

**Verdict file:** `verdict.md` in this folder. First line: `VERDICT: <GO|GO WITH NOTE|NO GO> at head db9bca740df0... (tier 1, round 1 of 2; landing tree <sha> on develop <sha>; N blockers, M notes)`. Then BLUF, findings, FOUND / TESTED / HOW, NOT RUN, wall-clock. Last line: the sha256 of `sed '1d;$d' verdict.md`, labelled with that method.

**Rules:** findings only; no GitHub or Linear writes; nothing under `!CODING`; no push; no `cd`; no `rm`; no stderr to /dev/null; no Docker (another seat uses it); every zero with a positive control; red by ASSERTION, never by load failure; each mutant `tsc` rc 0 before it counts; restore asserted after every arm. Before finishing run `git -C /Volumes/DevMASTER/WEDNESDAY status --short` and report every untracked path outside 0_Brain/, 5_Project_History/, 2_Project_Files/local-model/ and 2_Project_Files/fleet/briefs_staged/.

## Questions (instrument for each; name what you did NOT run)
Ruling it implements: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-20_answer_seatC31_ks1557_aprime.md`.
1. **Stuart's regression closed:** the four-step chain (originate -> /version -> /version -> certify from the latest version, same connector) answers 201 at the landing, 403 at develop; the legacy path (`certifications.ts` ~:223) likewise; the no-`onBehalfOf` hole closed on both paths.
2. **Nobody gains rights they should not (adversarial):** a FOREIGN connector, another organisation's user, a same-org non-owner, the recipient persona all still 403. **Specifically:** because `/version` has no source-access check today (KS-1688), can org B version org A's document and then CERTIFY the minted child via its new `create:connector` row? Measure it. Is that a widening relative to develop, and does it give B any reach into A's original? Report as a finding with the exact chain; do not judge the product policy.
3. **Read surface unchanged:** `getCreationProvenance` byte-untouched; GET on a version-minted document echoes no `createdOnBehalfOf` and no `pseudonymised: true`.
4. **Migration 055 on a REAL Postgres** (your own scratch instance, never 5432 or another seat's port): forward, idempotent re-run, the ambiguous case skipped with its NOTICE, twice-versioned by one connector, certify-derived rows untouched, 0 literal `create` rows written, and the reverse statement in the PR body removing exactly 055's rows. Additive only.
5. **ITEM5c cell** (Kam's ruling (b), KS-1557 comment `c033e6fb`) still green and unmodified; the edited ks1228 cell asserts BOTH rows precisely.
6. **No weakening:** originate suite by cell NAME at develop vs the landing; your own mutants (at least three) on the predicate and the writers.
7. **Landing:** merge-tree on live develop; `tsc --noEmit` rc 0 at the landing; the new test files type-checked in their own program.
