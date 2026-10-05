Refs KS-1278 — https://linear.app/secuura/issue/KS-1278

`POST /api/documents/:id/revoke` decided "already revoked" on a **READ**
(`routes/documents.ts:2374`) and then ran an **unconditional** `UPDATE`. Two overlapping revokes
could both pass that read: **200 + 200**, two updates, two `action_provenance` rows, two anchor
calls. The decision now lives **IN the UPDATE** — `updateDocument` takes an `ifStatusIsNot` option
that adds `AND (${guardStatus}::text IS NULL OR status IS DISTINCT FROM ${guardStatus}::text)` to
the `WHERE`, and a guarded write that changed **no row** returns `null`. The loser answers the
*same* **400 BAD_REQUEST "Document is already revoked"** as a sequential caller and returns
*before* `recordOnBehalfOf`, so it records **no** provenance row and emits **no** anchor.

This **completes the ticket's scope** — the atomic transition, the 400 for the loser, and
provenance and anchor only for the winner. **The row-lock alternative is not taken.** The PR says
`Refs`, not `Closes`, and the ticket does not move to Done on this change's account (see NOT
COVERED).

### Why the 400 is correct here, and not a masked 404

`updateDocument` already returned `null` for a **missing** document (`documentRepo.ts:538`), so
`null` now carries two meanings. The route is safe because it **404s at `:2367`** and **403s at
`:2371`** before the write, and 400s on the read at `:2375` — so by the time the guarded write runs
the document exists and was not revoked at read time, and a `null` can only mean the row became
revoked in between. One residual case is named under NOT COVERED and is being filed separately.

## Test Evidence

**Touched**
- `Blockchain/Dev/services/originate/src/repositories/documentRepo.ts` (+9/−1) — the `ifStatusIsNot`
  option, the guarded `WHERE`, and the `affected === 0` → `null` return.
- `Blockchain/Dev/services/originate/src/routes/documents.ts` (+6/−1) — the revoke route passes the
  guard and answers 400 when the write changed no row.
- `Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts`
  (+1/−0) — the KS 1293 hermetic register lists the new cell file, so the suite stays self-listing.
- **NEW** `Blockchain/Dev/services/originate/src/__tests__/ks1278-revoke-is-one-atomic-transition.test.ts`
  (+157) — 4 cells.
- Both platform-k HTML documents, in **this** commit (skill §4): flow gains block `15.` between
  `14.` and `19.`; the cheat sheet gains a new last section.

**Ran** — all on host Kamil's Mac Studio (2) (Mac15,14, M3 Ultra, 28 cores, 96 GiB), node v24.7.0,
jest 29.7.0, **2026-10-05**.
- `ks1278` + `ks1293` targeted: **14 passed, 14 total**, rc 0.
- Full `services/originate` unit suite: **BEFORE 90 suites / 1063 tests → AFTER 91 / 1067**, 0
  failed at both ends. Delta **+1 suite / +4 tests** — exactly this PR's cell file. Wall clock 12 s.
- `tsc -p services/originate --noEmit`: **rc 0**.
- `npm ci --ignore-scripts` rc 0 (1937 packages, 135 s); `npm run build --workspace=packages/shared`
  rc 0; `packages/shared/dist/index.js` asserted present at **17,746 B** before the first test and
  again before the push.
- **Red-first, by assertion.** Both test sections applied, **neither** product hunk: **rc 1,
  2 failed / 2 passed of 4 total** — R1 and R2 red, C1 and C2 green. **4 executed**, so an assertion
  red and not a load failure. Control: `grep -c 'IS DISTINCT FROM'` reads **0** on the reverted
  product and **1** restored.
- **One tamper per conjunct of the guard**, each applied *alone*, 4 tests executed and 1 failed /
  3 passed every time:

  | Tamper | Term falsified | Cell that reddens |
  | --- | --- | --- |
  | whole `AND (…)` clause deleted | the SQL guard, entire | **R2** |
  | `status IS DISTINCT FROM` → `status =` | the IS-DISTINCT-FROM term, inverted | **R2** |
  | `guardStatus !== null &&` removed | the pass-through for callers asking no guard | **C2** |
  | `affected === 0` → `affected === -1` | the changed-no-row term | **R1** |

  Restored: **4 passed, 4 total** — so those reds are the tampers, not drift. **C2 is not
  decoration:** it is the only cell that reddens when the `guardStatus !== null` term is dropped,
  which would otherwise make every unguarded caller receive `null` on a 0-row update.
- **Apply provenance.** Payload 11,812 B, sha256 `67834e04ad631886`, re-hashed by me. Split into 4
  sections, rejoin byte-identical to the whole; strict `git apply --check` rc 0 per section with a
  tamper control per section that **fired** (rc 1, 1, 1, 128). The new-file section's arm is a
  **hunk-count** tamper, because a **content** tamper on a new file is vacuous — proved: it reads
  rc 0.
- **Pathgate: 6 assertions, 0 failed.** The path set is exactly the 6 declared paths; zero lockfile,
  manifest, baseline or co-tenant paths appear. All three controls fire — the same filters return
  **4** on an unrelated PR's diff, so they are not inert.
- **Push preflight, quoted from the in-hook file, and it is NOT a pass:**
  `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` /
  `legs 3 4 8 — local stack not up`. Also from the same run: `shell suites: 67 passed, 0 failed,
  0 skipped (of 67)` and `OK — 13 code guards passed.` **12 of 15 is not 15 of 15** — legs 3, 4 and
  8 did not run because the local stack was down.

**NOT run**
- **No live sweep** (skill §5f). Nothing was exercised against a running stack or a real PostgreSQL.
- Preflight legs **3, 4 and 8** — local stack not up.
- The four platform suites (Schemathesis · Akto · Playwright · Performance/k6) — this change adds no
  scan surface, no route, no spec operation and no k6 scenario. Named here rather than skipped
  silently.
- No integration suite (`test:integration`) was run.

**Migrations + config**
- **None.** No migration, no `.sql`, no schema change, no env var, no manifest, no lockfile, no
  dependency, and `scripts/audit/audit-baseline.json` is **untouched** — the pathgate asserts all of
  this mechanically and its controls fire.

### Documentation (skill §4)

Both platform-k documents move in **this** commit. Position per ruling: the flow document's
numbered `<h2>` sequence is an ascending invariant readable off the file (it read `1..14, 19`), so
block `15.` can only sit between `14.` and `19.`; it now reads `1..15, 19`, 16 headings. The cheat
sheet has **no** readable ordering invariant — its committed KS order is `1404, 1333, 1345, 1388,
1005` — so the new section's position was **ruled**, not inferred, and it is last. Both documents
are div/table/pre balanced (70/70 and 157/157 divs) and a real `html.parser` parse of each raises
nothing.

**Timing.** Instrument, printed so it can be re-run: `/usr/bin/grep -c -i -E` over both platform-k
documents at base `32e058975d4e`. `originate.*unit suite` → **0** flow / **0** cheat. **Must-hit
controls** `auth` → **76 / 75** and `Akto` → **71 / 83**, so the zeroes are measurements and not a
blind grep. **No stated timing row is amended and no Akto tier budget moves** — this change adds no
scan template. My new blocks state the figure, the date and the host, as §4 requires.

**§5d** holds: every added product line carries the ticket key and the prior behaviour, so the diff
explains itself later.

### NOT COVERED (skill §5f)

- **No live sweep**, so **KS 1278 does not move to Done on this change's account.**
- The cells mock the Prisma driver, so the atomicity is pinned at the SQL **text** level (R2) plus
  the JS return path (R1, C2). **That two concurrent transactions really serialise on this `WHERE`
  is UNMEASURED here** and would need a live two-session test against a real PostgreSQL.
- **Residual, not fixed and being filed separately:** a document **deleted** between the route's
  read and the guarded write answers **400 "already revoked"** where **404** belongs, because
  `updateDocument` returns one `null` for both "not found" and "guard refused". That is a
  pre-existing shape of that single `null`, **narrowed to a race window by this change rather than
  introduced by it**; separating the two meanings is outside this ticket's scope.
- This PR's parent is `32e058975d4e`. develop has since moved to `3cb93b9c731e` (via
  `232623892f24`). Both of those commits touch **both** platform-k documents, so a **docs-only
  merge-in will be required** before merge; its target tree comes from the gate's key-anchored
  prediction on the develop current at that time, not from this PR.
