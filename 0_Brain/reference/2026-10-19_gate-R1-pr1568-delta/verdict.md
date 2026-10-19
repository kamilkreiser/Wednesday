VERDICT: GO at head d74b7f951de81a054b6d6b9403352e1a598b5019 (test-only delta on d2564aeb587b; tier-2 gate R1)
# Gate R1 verdict: PR 1568 test-only delta, Sonnet tier 2

- **Head and develop:** ls-remote at the start of this gate gave `refs/pull/1568/head` = `d74b7f951de81a054b6d6b9403352e1a598b5019` and `refs/heads/develop` = `37834600a543cb0276f427d969ac034d9df74fbd`. Both match the brief.
- **Setup:** findings only. The project checkout was read with ls-remote only, and has 0 tracked changes after. I cloned from GitHub into my scratch (`r1/repo`), built a scratch landing commit (`7a980a59548f`, never pushed), and ran everything in `r1/wt`. No GitHub, Linear or `!CODING` write.
- **Postgres:** my own PG 15 cluster on 127.0.0.1:55851 (port was free), built as compose builds one (P1's `mkpg.sh`: docker/init, then the worktree's own `run-migrations.sh`: `applied=53 failed=0`). Stopped now, port free.

## Q1. Diff scope and assertions: YES, one file, nothing weakened
- **Instrument:** `git diff --stat d2564aeb587b d74b7f951de8` and the full hunk.
- `1 file changed, 6 insertions(+), 2 deletions(-)`: `services/anchoring/src/__tests__/ks1385-anchor-store-keeps-the-latest-events-metadata.integration.test.ts`, nothing else. One commit, author and committer `Kam Kreiser <kamil.kreiser@secuura.ai>`.
- Two hunks, `:717` (XT1) and `:727` (XT2). Each replaces the single line `expect(err?.constraint).toBe('documents_id_namespaces_disjoint')` with `expect({ code: err?.code, constraint: err?.constraint }).toEqual({ code: '23505', constraint: 'documents_cannot_claim_a_live_anchor_id' })`, plus comment lines.
- **Strengthened, not weakened:** the old line pinned only the constraint name; the new one pins SQLSTATE 23505 AND the name, by exact `toEqual`. No matcher loosened, no assertion removed.
- The lines after each (context, untouched in the diff): `persist(...)` by tenant B's caller gives `{ allow: false, reason: 'document-not-in-callers-tenant' }`, and `storedActor(...)` is still `did:key:zUPLOADER`. So tenant A's identity KEPT is still asserted in both cells.
- The refusal (23505) is asserted: the `makeDocument(...).then(() => null, (e) => e)` result is compared, and a null (no refusal) would fail the `toEqual`.

## Q2. 051-first claim: TRUE
- **Instrument:** `git show d74b7f951de8:` of both migrations.
- Both are `BEFORE INSERT OR UPDATE OF id, external_id ON documents FOR EACH ROW`. 050's trigger is named `documents_id_namespaces_disjoint` (`050:95`), 051's is `documents_cannot_claim_a_live_anchor_id` (`051:155`). PostgreSQL fires same-timing row triggers in name order, and `documents_c...` sorts before `documents_i...`, so 051 fires first and its RAISE (23505, CONSTRAINT `documents_cannot_claim_a_live_anchor_id`) is the error that reaches the client when both would refuse. Confirmed by measurement in Q4, not only by reading.

## Q3. Predicted landing tree: MATCHES J
- **Instrument:** `git merge-tree --write-tree --merge-base=833984fc9 37834600a543 d74b7f951de8` gives rc 0, tree `24cc02989cf1ad06565b718f1227393e5ec81f46`. The automatic-base form (`merge-tree --write-tree 37834600a543 d74b7f951de8`) gives rc 0 and the same tree.
- J's figure `24cc02989cf1` is the same. Round 4's `524b5d203a18` differs by the one test file only (P1's tree plus this delta).

## Q4. KS-1385 integration suite on the landing tree: RAN, 56/56, bite both ways
- **Instrument:** vitest `vitest.integration.config.ts` on the landing tree `24cc02989cf1` (scratch commit `7a980a59548f`), owner `secuura` for fixtures and `secuura_app` (NOSUPERUSER NOBYPASSRLS, verified by mkpg output `secuura_app|f|f`) via `TEST_APP_DATABASE_URL`. Trigger 051 present, function md5 `f6d6aa8d93dcfa24ab6938c937e413b5`, as P1 recorded.
- **Landing tree, delta in place: 56 tests, 56 passed, 0 failed** (RC 0). Matches J's 56/56. P050 (the precondition cell that 050 is applied) passed.
- **Bite XT1:** XT1's constraint name reverted to `documents_id_namespaces_disjoint`: 56 tests, 55 passed, **1 failed: XT1 only**.
- **Bite XT2:** XT2's reverted alone: 55 passed, **1 failed: XT2 only**.
- **Restore:** the test file sha256 after each restore equals the committed blob (`a0f50116dde1f3d538297a155850f5b66af489f1a4f5ac0381200b35a6068271`, read from `git show d74b7f951de8:` as well); worktree has 0 tracked changes; a final full run after restore gave 56/56 again.
- Note: my first run gave "5 passed, rest skipped, 0 failed" with RC 1 because I had set only `TEST_DATABASE_URL` as the app role. The suite itself refuses without both URLs (a FORCE-RLS cell). That was my harness error, fixed by supplying the owner URL and the app URL; no product or test change. Only the corrected runs are counted above.

## Q5. NOT tested (named)
- **Anchoring:** the unit suite (vitest `npm test`), including `threadTokenMint.test.ts`, which J says fails identically on develop (KS-562). Not run by me, so J's 379/380 is unverified here. Anchoring's tsc/build. Any anchoring integration file other than the one KS-1385 file (it is the only `*.integration.test.ts` I ran).
- **Originate:** the jest unit suites (J: 120 suites, 1469/1469; P1 measured the same on `524b5d203a18`), originate `tsc --noEmit`, originate's `ks1612-051` integration cells (17 on node-pg, 17 on Prisma) and 050's cells (13), the booted e2e (six orphan-minter routes, MAJ-B routes), the census, the helper mutants.
- **Everything else:** the pre-push hook's preflight legs (J: 13/16 ran, 3 skipped), shell suites, ESLint, real boxes, real Cardano, the gateway, Docker/platform suites. Also not checked: the PR body text and Linear links J describes.
- The delta touches one test file and no product line, so these are unchanged from P1's round 4 measurements on `524b5d203a18` except where the delta could interact: only the anchoring KS-1385 file, which is what I ran.

## Severities
- Major 0. Minor 0. Info 0 new. P1's MIN-1 and MIN-2 and Infos are unchanged and not re-opened by this delta.

Merge only on Wednesday's head-bound GO naming `d74b7f951de8`. Nothing deploys from this verdict.

MODEL: claude-sonnet-5-5
(Last line: sha256 of this file with its first line and this last line removed.)
d7d7cbe747be6c455f450357c08e277367d0e74eed22a7d745926e52d11c277c
