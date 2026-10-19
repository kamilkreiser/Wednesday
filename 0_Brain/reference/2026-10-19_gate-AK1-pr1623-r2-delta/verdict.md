VERDICT: GO WITH NOTE at head ea9d6e697951ef5c78628055429f345486955bcd (tier 1 delta, round 2 of 2; landing tree e598e00e890284ae6b85a9fe0379eac3c28a72ca on develop a0da739b6954d42333640ea190d877f031803c7f; 0 blockers, 9 notes)

# Gate AK1: PR #1623 (KS-1633) delta, Opus, tier 1, round 2 of 2 (the cap)

Gate: claude-opus-5-5, row G1. Findings only. I wrote nothing under `!CODING` and nothing in WEDNESDAY except this file. No push, no GitHub or Linear writes.
Scratch: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/08573273-0b69-4d9e-abf5-9b213ac8c2f2/scratchpad/ak1/`. It holds my clone `repo/`, logs `logs/`, mutants `mut/` and the probe `probe/`. I fetched with the project's deploy key, read-only.
Scratch PostgreSQL 15.14 ran on 127.0.0.1:55441, TCP only (`-k ''`), timezone UTC, and is stopped now.
- Provisioned from `docker/init/*` plus the project's migration runner: **54 applied, 0 failed**.
- The `tenants` table was supplied from `docker/init-platform/01-platform-schema.sql`. That load gave 1 error, `idx_vault_token already exists`, the same as round 1. The `secuura_app` grant was then re-applied. `secuura_app` has rolsuper f and rolbypassrls f.

## Heads and landing
- **Heads.** ls-remote at start and again before the verdict (11:09Z) gave develop `a0da739b6` and #1623 `ea9d6e697` both times, matching the brief.
- **Landing tree.** `merge-tree --write-tree origin/develop origin/pr1623` gives `e598e00e8902…`, which is the author's prediction. It equals the head's own tree because the merge-base is develop.
- **The merge commit is clean.** Re-merging the author commit `654322a91` with `a0da739b6` gives the same tree as `ea9d6e697^{tree}`.
- **Three-dot list.** `origin/develop...ea9d6e697` lists **8 files, +707/−96**: ks1228, ks1538 (unit), ks1633 (integration), ks1633 N4 unit (new), ks543, `db.ts`, `certificationRepo.ts`, `certifications.ts`.

## BLOCKERS
None.

## Answers

**Q1. Is B1 closed? Yes.**
- **Method.** A probe went through the real router as `secuura_app`. I ran develop's three product files and then the head's against the same tests, in both tenancy modes, and compared status and body byte-for-byte after normalising uuids and timestamps.
- **Totals.** 36 status+body cases per mode: **35 identical, and 1 differs only by a new-id echo** (C10c `derivedDocumentId doc-<ms>-<id8>`, exempt). MT=false and MT=true gave the same per-case result (the diff of the two comparison files is empty).

B1's three cases, in production with anchoring on a closed port:

| case | develop | head |
|---|---|---|
| C11, a NUL byte in `data` | 503 | 503 |
| C12, connector principal `connector:platform-s:<guid>` | 503 | 503 |
| C13p, the save throws | 503 | 503 |

At the head, C13p cannot fail inside the reservation, because the reservation does not call `saveCertification`. So I added cases that make the reservation itself fail:
- C14p, the reservation throws: 503 on both sides.
- C15p, the reservation throws a P2024 transient: 503 on both sides.
- C16p, the reservation and the save both throw: 503 on both sides.
- C05p, an unknown holder (an FK refusal at the reservation): 400 on both sides.

The sweep:
- **Success paths:** C01 201, C18 connector OBO 201, C09c 201, C10c 201.
- **Non-production failure:** C03 201.
- **Validation:** C04, C05, C06 400, and the C04p/C05p production variants.
- **Access:** C07 401, C08 and C08p 403, C09 and C09p (KS-1538) 403, C10 and C10p (KS-1557 parent) 403. C10q (own parent, production, anchoring down) 503.
- **Anchoring up and the reservation failing:** C11c 400, C12c 400, C14 201, C15 201, C16 500. Also C11n and C12n 400 with non-production anchoring down, and C17, the KS-203 transient on the save, 503.
- **S2,** persist-then-500 in production: 503 on both sides.

All of these are identical.

**Q2. Exactly one ISSUE event (round 1's N1).**
- Accepted (C01, C10c, C14, C15): **1 ISSUE event on both sides**.
- Non-production failed (C03, S1): **1 on both sides**.
- The event details compared byte-equal after normalisation, for example `{"status":"issued","blockchain":{…"anchoringStatus":"submitted"}}`. Both sides had non-empty events, so the equality is not vacuous.
- Production 503: 0 events on both sides.

**Kam's (b) holds in both modes.** After a non-production failure the stored blockchain is `{status:'failed', anchoringStatus:'failed', anchorId:null}`. On the accepted path it is `submitted` with an anchorId and no `status`. The state at anchor time (the reservation) is the failed blob. `/recertify` is byte-unchanged: every develop-to-head hunk in `certifications.ts` lies at :31–614, inside the issue route.

**Q3. The shared insert.**
- `certificationRepo.ts` has **one** `INSERT INTO documents` statement (:239). A second grep hit is the doc comment at :206.
- It sits in the private `insertCertificationRow` (:211). `reserveCertificationRow` (:280) and `saveCertification` (:285) both call it.
- I captured `saveCertification`'s SQL with a recording db, fixed Date, fixed uuid, and two issuers (a uuid principal and a connector principal), on develop and on the head:
  - **Parameters byte-equal**: 17 and 17 for documents, 7 and 7 for events. Control: one planted parameter change shows as unequal.
  - Events SQL text: byte-equal.
  - **Documents SQL text: NOT byte-equal.** The difference is whitespace only; see N3.
- Save-related unit files: **23 files, 380/380 pass**. That includes ks543 5/5 (F4-1, **F4-2**, F4-3) and certificationRepo 16/16.

**Q4. N4, the pool.**
- **`withTenant` (`db.ts:322-332`).** The new `opts.pool` is optional and is used only on the MT branch (`opts?.pool ?? getDefaultPool()`). Omitted, it behaves as on develop. In the non-MT branch Prisma still gets `opts`, but `deleteCertification` passes `undefined` when there is no pool, and `req.tenantPool` exists only under MT.
- **The route passes the request's pool on both writes.** The compensating delete passes `(req as any).tenantPool` (`certifications.ts:584`). The reservation passes `(req as any).db`, which is `getRequestPrisma(req)` over the same `req.tenantPool` (`index.ts:224-226`).
- **The planted mutant does NOT red the unit cell.** With `MN4_route_passes_no_pool` (tsc 0), all 226 cells in 10 unit files pass and ks1633 passes 10/10 in both modes. See N1.
- **No second tenant database was run.** I had one scratch instance and no Docker.

**Q5. Named cells and mutants.** tsc was 0 for every mutant.
- **Red-first against develop's product:** ORDER, ORPHAN, DELETE-FAILS and N3 red, **4/10 in both modes**, as claimed.
- **Against round 1's product:** N1 and ORPHAN red (2/10). B1 is green there, which is the vacuity the author flagged.
- **N4 unit file:** "Test suite failed to run" against both develop and round 1. That is a load failure, as the author reported.

The mutants:

| mutant | what it does | result |
|---|---|---|
| author's M-B1 | unwraps the reservation | reds only B1 in ks1633, both modes. It also reds 32 cells in 10 unit files; see N8 |
| author's M-N5 | drops the authoritative save | reds N5, N1 and ORPHAN, both modes |
| MN3 | `removed !== 1` changed to `< 0` | reds N3 |
| MF43 | the reservation goes through `saveCertification` | reds ks543 F4-3 (and F4-1) plus 12 unit cells, and ks1633 N1 and ORPHAN |
| MOWN3 (mine) | reservation moved after the anchor | reds ORDER |
| MOWN1 (mine, on the non-deciding wrapper) | rethrows pg-coded reservation errors | reds B1 |
| **MOWN2 (mine)** | `provisionalWritten = true` set before the await | **survives everything**; see N2 |
| MN4r (control) | the repo drops the pool | reds the 2 N4 unit cells |
| **MN4d** | `withTenant` ignores `opts.pool` | **survives everything**; see N1 |

**Q6. Delta discipline.**
- The round-1-to-round-2 diff is 12 files. Six of them are develop's KS-1402 move, which came in through the clean merge `ea9d6e697`: ks1402 ×3, ks697, ks739, `documents.ts`.
- The author commit `654322a91` touches 6 files, and each hunk maps to the blocker fix or to a note:
  - `certifications.ts`: the non-deciding, event-free reservation (B1 and N1), the pool on the delete (N4), and the unconditional authoritative save.
  - `certificationRepo.ts`: the shared insert and `reserveCertificationRow` (N1), and the pool parameter (N4).
  - `db.ts`: N4.
  - ks543: F4-3 now counts `saveCertification` once and pins the sequence on the reservation.
  - The new N4 unit file: N4.
  - ks1633: the B1, N1, N5 and N3 cells, the reserve seam, ORPHAN narrowed, and the header wording for N9.
- Round 1's N2 and N6 are **not** in the code delta; see N5.

**Q7. Landing tree `e598e00e` (it equals the head tree).**
- Originate full unit suite: **126 suites / 1510 tests / 0 failed**, matching the claim.
- ks1633-certify-writes: **10/10 with MT=false, 10/10 with MT=true**. SETUP asserts the tenant manager matches MT.
- ks1557-lineage-certify: **13/13, 13/13**.
- ks1538-legacy-certify (integration): **10/10, 10/10**.
- `tsc --noEmit -p services/originate`: 0.
- A scratch tsconfig that includes `src/__tests__` covered 147 test files: **0 errors**. Positive control: a planted TS2322 gives rc 2.

## Notes
- **N1. The N4 fix is correct by reading, but the route and `withTenant` halves are unpinned.** MN4 (the route passes no pool, `:584`) and MN4d (`db.ts:332` ignores `opts.pool`) both survive every suite. The unit cell pins only the hand-off from `deleteCertification` to `withTenant` (MN4r reds 2). The claim's "pinned only by the unit cell" covers less than it reads as.
- **N2. The "nothing to compensate when the reservation never landed" arm (`:584`) is unpinned.** MOWN2 survives. In production, a failed reservation would then run a delete on no row and fire the "removed no row" error line spuriously. The response is unchanged.
- **N3. `saveCertification`'s documents INSERT is not byte-equal to develop.** 27 of 28 lines differ by exactly two leading spaces, an artefact of the move into the helper. The whitespace-normalised text and all 17 parameters are equal. No behaviour difference.
- **N4. The ruled ORPHAN residue, measured.** When the reservation lands and the authoritative save then fails (C13n 500; C17, the KS-203 503 "please retry"), the head leaves a `documents` row with status `certified`, blockchain `failed`/anchorId null, and **zero** `certification_events`. The anchor names it, and the client was told it failed. Develop leaves 1 orphan anchor and no row. A client that retries mints a second id. This is the ruled narrowing; it is worth naming in the follow-up ticket.
- **N5. Round 1's N2 and N6 are retracted in the PR body but not in the code.** `certifications.ts:467` still says "removes the window rather than narrowing it", and `:474` still says "sub-second window".
- **N6. The suite headers are stale.**
  - The ks1633 header (:31) still says `beforeAll` "SUPPLIES both" next to "must hold a `tenants` table", but it seeds no table. I had to supply it, so round 1's N9 is reworded, not fixed.
  - :23 still says "ORDER, ORPHAN and DELETE-FAILS… the other three", but the suite now has 10 cells and 4 of them red on develop.
  - B1's title (:262) says "three shapes" and runs two. Both of those shapes are mocked; the real NUL and connector shapes are covered only by this gate's probe.
- **N7. The reservation's warn line is not "ids only".** It carries the driver message, which echoes the offending value. Measured: 22P02 `invalid input syntax for type uuid: "connector:platform-s:<guid>"`. Develop's catch-all already logs the same message at error level, so this is not a new class of exposure.
- **N8. Under M-B1, 32 cells in 10 unit files red.** Those files mock `certificationRepo` without `reserveCertificationRow`, so at the head the reservation throws "not a function" and is silently swallowed. Those suites therefore exercise only the reservation-failed path, never its success path. "Reds exactly this cell" is true of ks1633 only.
- **N9. I could not reconstruct the author's 210-cell save-count set.** 17 different ks543 + 5-file combinations sum to 210. Instead I ran all 23 candidate files: 380/380 pass.

## Integration suites (only originate is touched)
- RUN on the landing tree, both modes: ks1633-certify-writes, ks1557-lineage-certify, ks1538-legacy-certify (integration), and my probe (38 cells per mode per product, scratch only).
- NOT tested: every other originate `*.integration.test.ts`, including ks1402 ×2 and ks1557-verify; the four Docker platform suites; anchoring, api-gateway and the other services.

## Not run
- No second tenant database (N4 is reasoned plus the unit cell only).
- No concurrency.
- No process kill in the window between the reservation and the save.
- Round 1's S3 (a credential attached before the compensation): my plant went through `saveCertification`, which the head's reservation does not call, so it was vacuous here and is not re-measured. The delete path itself is unchanged since round 1, apart from the pool argument.
- No lineage-cycle 422 through the router.
- eslint.
- No Docker, no live box.

2e19e5f7b8335258c0d97fdd237735c378358469bb3214f9d5421f76a15cf0f2
