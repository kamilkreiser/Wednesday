# Gate brief: GATE L1 = PR #1568 round 3 of 3 (KS-1612 + KS-1385 (b)), TIER 1, the FULL gate, Opus

Commissioned by the Wednesday seat, 2026-10-19 ~07:5x AEDT, under model routing v1.0 row G1 (a cross-tenant
security guard and a migration). **This is the last round Kam allowed** (card `secuura-ks1612-third-round-after-cap-1018`
= a, "If that also fails, it stops for you again"). Seat J 13th built it. Live develop 83ed01af70fd5ed6cca9ac66f28ddcb8a1034105
and head 09588895db75354d829df2069452c82b787d8bc8 (Wednesday `git ls-remote` ~07:5x; re-read both). 0_Brain paths are
relative to /Volumes/DevMASTER/WEDNESDAY/. Project paths are under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/.

**Read first, whole:** round 2's NO GO verdict `0_Brain/reference/2026-10-18_gate-pr1568-r2/verdict.md` (MAJ-A, MIN-A),
round 1's in `0_Brain/reference/2026-10-18_gate-pr1568/`, and the PR body at the head (J's Test Evidence block and the
narrowing list). Wednesday ruled the round-3 DESIGN's SHAPE only (migration 051 + MIN-A); **whether it closes MAJ-A is
your question, not a settled one.**

- **Round 3 delta**, 4 files +364/-9: `Blockchain/Dev/migrations/051_documents_cannot_claim_a_live_anchor_id.sql` (new):
  BEFORE INSERT OR UPDATE OF id, external_id ON documents, refuse when an `anchor_store` row already holds the id being
  claimed and no `documents` row already owns it (both the external_id arm and the `NEW.id::text` arm), SECURITY DEFINER,
  role assertion, fail-closed apply-time census; `originate/src/utils/idNamespaceCollision.ts` (MIN-A: a Prisma P2010 arm
  matched on the migrations' fixed message text); `originate/src/routes/documents.ts` (+2 at ~:738);
  `originate/src/__tests__/ks1612-409-mapping-survives-the-prisma-error-shape.test.ts` (new).
- **Author's claims (NOT evidence):** MAJ-A ACCEPTED -> REFUSED on a real PG 15; census 1 -> 0; 001->051 applied=53
  failed=0; 8 SQL cells, 6 SQL mutants killed; 11 TS cells, 3 TS mutants killed; originate 1393 vs baseline 1382 (+11,
  +0 failures) on a tree with `packages/shared` rebuilt (the shared checkout's dist is stale: 19 failures + tsc rc 2
  there, identical on baseline); preflight 13/16 legs, 3/4/8 skipped.
- **J's corrections to the round-2 record you must re-check, not inherit:** the orphan minter is originate's
  `POST /api/anchors/submit` (`anchors.ts:367`, uuid v4 at `:393`, written at `:442`), not anchoring's
  `/api/anchoring/submit` (which writes nothing); originate `anchors.ts:109` `saveAnchorToDb` is a second, unguarded
  upsert (KS-1603) that does NOT touch `metadata_payload`.

## Gate
1. Diff the PR at its head against develop by hunk; confirm round 3 adds only the four files above on top of round 2's.
2. **MAJ-A, every route to it.** Reproduce MAJ-A on develop+round-2 and confirm 051 refuses it, through EVERY orphan
   minter J's census names (anchoring `POST /api/anchors`, `/api/anchors/batch`; originate `POST /api/anchors/submit`,
   `POST /api/anchors/`), not one. Then hunt for a route J did NOT name: any writer of `documents.id`/`external_id`
   (INSERT, UPDATE, upsert, Prisma, raw SQL, migrations, seed, startup-migrations) that 051's trigger events do not
   cover. Name what you searched and its control.
3. **Legitimate flows still work:** the 200-idempotent re-POST and 409-on-different-bytes (`saveDocument`
   conflictMode skip; the NOT EXISTS exemption); the certification path (no external_id) under round 2's custodian
   rule; a lifecycle event by a caller-supplied v4 id from the issuer's connector (Stuart's S-shaped flow); and
   round 2's KS-1385 (b) behaviour unchanged.
4. **The open residuals, measured, not argued:** (a) REVERSE ORDER: can a document be pre-registered under an id
   predictable before its anchor exists so a later anchor lands under it? Measure what K's own minters use, and say
   what K cannot know about S's chain ids. (b) CONCURRENCY: two concurrent inserts (an anchor and a document claiming
   its id) both passing: try it (two sessions, explicit transactions) and report. (c) The `$21` clock: confirm 051's
   live rule does not depend on `created_at`.
5. **MIN-A:** 409 not 500 on the Prisma path, by driving the REAL wrapped error, for 050's and 051's constraints;
   the TS constants equal the `.sql` messages byte for byte; a reworded migration message makes the pin red.
6. **051 itself:** applies cleanly 001->051 on a fresh PG 15 through `run-migrations.sh`; refuses to apply with a
   violation present; refuses as a non-bypass role; the function is not directly callable; re-running the migration is
   safe (idempotent or refused, say which).
7. One mutant per product hunk you did not see J kill, and the owning suites before/after on a tree with
   `packages/shared` rebuilt in YOUR clone.
8. Merge prediction on live develop (tree id), overlap with the open PRs. Note: R's KS-1628 #1587 also edits
   `originate/src/routes/documents.ts` (lines ~1505-1600): predict both orders.

## Rules
- Read-only on the project. **Your OWN scratch folder is /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/ff943889-d9ba-463a-a66e-300867d673bd/scratchpad/l1/ — create it and use nothing else in that scratchpad.** Clone there with `git clone --shared` from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files, set origin to git@github.com:Secuura/Distributed_Secuura.git in YOUR clone, fetch with that checkout's `core.sshCommand` (read it with `git config --get`). Build `packages/shared` before any suite. Use your OWN Postgres (a fresh data dir in l1/, a port you choose and name); J's scratch PGs on 55491/55492 are J's: you may READ from them only if you need J's fixture, and say so.
- No git write verb in !CODING, no push, no GitHub or Linear writes, no Docker, no kintsugi/demo access.
- Never cd, delete nothing outside l1/, every loop in a script FILE run with `/bin/bash`, never inline. An EXIT trap that restores a file uses an ABSOLUTE path.

## Output
- Write 0_Brain/reference/2026-10-19_gate-L1-pr1568-r3/verdict.md.
- Line 1: the verdict (GO / GO WITH NOTE / NO GO) naming the head.
- Line 2: `sha256/16: <16 hex>` of the report with line 2 deleted.
- Then FOUND / TESTED / HOW, NOT tested, severities with file:line, and each residual (a)-(c) with its measurement. Final line: `WALL-CLOCK: <minutes>`. **Round 3 of 3: a NO GO goes to Kam.**
