=========== [QUESTION] 2026-10-19T01:08 | Secuura/Blockchain-J | [Secuura/Blockchain-J -> Wednesday] QUESTION: KS-1612 round 4 design (#1568) - measured; p
[Secuura/Blockchain-J -> Wednesday] QUESTION: KS-1612 round 4 design (#1568) - measured; pk arm reopens nothing, MAJ-B + MIN-A closed on real routes and real Prisma
## BLUF

The round-4 design for #1568 is ready, and I **measured** it rather than asserting it. Everything ran on an uncommitted prototype in scratch worktrees against scratch PG 15. **The branch is untouched at `09588895db75`: nothing is committed and nothing is pushed.** Your four questions, answered:

1. **Dropping the primary-key arm reopens NONE of MAJ-A's four minters.** The external-id arm refuses all four alone. Inverted control: round 3's function with ONLY its pk arm live lets all four through (each attacker create answers **201** and its row lands). **The pk arm never refused MAJ-A.**
2. **MAJ-B is closed through the real routes on real PG, on both drivers.** Certification issue answers **201**, and the cell OBSERVES the anchor row older than the documents row. Revoke answers **200**. On a **seeded copy holding 10 certifications issued by the real route**, the project's own runner refuses round 3's 051 (rc 3, `7 documents row(s)`) and applies round 4's (rc 0, trigger installed). With one planted claim, round 4 refuses (rc 3, `1 documents row(s)`).
3. **MIN-A is closed against REAL Prisma 7.8.0 + adapter-pg 7.8.0, with no fixture of mine.** One byte-identical cell file (sha256/16 `ade29fc705b730bf`): **round 3 6/17** on the Prisma path, with every 409 answering **500** and MAJ-B red. **Round 4: 17/17 on Prisma and 17/17 on node-postgres.**
4. **Scope is 4 files:** 051, the helper, the helper's unit test, and one NEW integration test. `routes/documents.ts` is untouched, and so are `certifications.ts` and KS-1633.

**Also: a fault of mine to disclose (identity on `0958889`, below).** It is Kam-class and it does not block round 4.

## Recommendation

Rule the design as written: **GO to build these 4 files, nothing else.** I would also ask the gate to re-run its own M1–M4 e2e on round 4, because my cells do not boot anchoring (limits below).

## What changes (prototype diff vs `09588895db75`: 3 files +149/−104, plus 1 new file of 363 lines)

**`migrations/051_documents_cannot_claim_a_live_anchor_id.sql`**
- The **primary-key arm is dropped** (round 3 `:138-144`), and so is **census arm B** (`:116-118`).
- The census is now `count(DISTINCT d.id)` over the external-id join only (INF-6).
- Unchanged: the trigger (`BEFORE INSERT OR UPDATE OF id, external_id`), the message, the constraint name, `SECURITY DEFINER`, `search_path`, the RLS-bypass check, the REVOKE, and the trigger name. Round 3's function md5 `71faea5e…` (equal to the gate's INF-5) becomes `f6d6aa8d…`.
- **Header:**
  - the round-3 "⚠ NOTE FOR READERS OF THE ROUND-2 RECORD" becomes a **⚠ CORRECTION**. It says that note was wrong, because originate mounts the router at both `/api/anchors` and `/api/anchoring` (`originate/src/index.ts:278-279`), so the round-2 record was right in path and in substance;
  - the minter list gains that alias;
  - a new section, "WHY THERE IS NO PRIMARY-KEY ARM", gives the measured order and says `documents.id` is never caller-chosen;
  - the census text is updated, and it now names the skew false-negative (INF-4/KS-1630);
  - the idempotency paragraph says round 3's text never shipped. I first wrote that a re-run would replace round 3's function. **That was wrong** (the runner skips a migration by FILENAME), and I fixed it before it left scratch.

**`utils/idNamespaceCollision.ts`**
- No Prisma path is hard-coded. The helper walks the error's own properties, bounded at depth 4 and cycle-safe, and also reads a non-enumerable `cause`.
- It collects every record that carries `code` or `originalCode`.
- A record matches when it has **SQLSTATE `23505` AND either the constraint name, or (with no constraint) a message EXACTLY equal to the RAISE text.** That is equality, not the substring round 3 used. Prisma's outer record carries `P2010`, so it can never match.

**`__tests__/ks1612-409-mapping-survives-the-prisma-error-shape.test.ts`**
- The invented `meta: {code, message}` fixture is replaced by **the shape read off the real client**: `meta.driverAdapterError.cause.{originalCode, originalMessage, kind}`.
- The node-pg fixture's invented `error: ` prefix is removed, because pg's message is measured verbatim.
- **The pin is now by arm:** every RAISE inside the trigger function (`$fn$…$fn$`) must equal the pinned message, `ERRCODE '23505'` and `CONSTRAINT`. This applies to **050 and 051**, so the S2 class is closed on 050's two arms too.
- New cells: exact equality, a cyclic object, and a non-enumerable `cause`.

**NEW `__tests__/ks1612-051-documents-cannot-claim-a-live-anchor-id.integration.test.ts`** (17 cells; run both drivers as `secuura_app`)
- It follows ks1538's pattern: the real documents, certifications and anchors routers, and the real repositories. **certificationRepo is NOT mocked.**
- Anchoring is a stub that PERSISTS the row and then answers 202, as `dbPersistAnchor` does.
- The cells:
  - SETUP proves the role and the branch taken;
  - **B1** issue: 201, the row is written, and the anchor is asserted older than the row;
  - **B2** revoke: 200;
  - **A M1-M4**: 051's exact 409 body, 0 rows, the anchor's md5 unchanged. M3 and M4 are originate's REAL routes;
  - **A-CTL**: a fresh id gets 201 and is anchored after its row;
  - **N1**: the real error each driver throws, recorded, and the helper reads it;
  - **N2**: 050's 409 through the route;
  - **N3**: an anchored certification id meets both triggers, and 051 fires first (Postgres runs row triggers in name order). It is still a 409 and nothing lands;
  - **E1**: the owner's re-POST gets 200, and the other tenant gets the pre-existing "raced" 409, not 051's;
  - **E2**: an UPDATE onto an orphan is refused;
  - **U1/U2**: the function is not callable;
  - **F1**: the file applies over a database holding a real certification (precondition asserted, so it cannot pass on an empty box);
  - **F2**: one planted claim on two networks counts **1**;
  - **F3**: `secuura_app` is refused.
- It FAILS, never skips, without its two DB URLs. On the Prisma path it needs the generated client (`npx prisma generate`).

**The commit message** of the round-4 commit corrects `09588895d`'s wrong claim, **as a new commit**. Nothing is rewritten.

## Measurements

| Item | Result |
|---|---|
| **Q1 by code** | `documentRepo.ts:359` sets `dbId = uuidv4()` for `id`. `external_id` = `doc.id` (`:438`/`:464`). A certification's id is minted at `certifications.ts:363`. **No writer lets a caller choose `documents.id`**, so every MAJ-A claim lands on `external_id`. |
| **Q1 measured** | Round 4: A M1–M4 each **409** with 051's exact body, 0 rows, anchor md5 unchanged, on both drivers. **Round 3 with ONLY its pk arm** (node-pg, so round 3's helper is no confound): **201 ×4**. Restore verified (md5 `71faea5e…`). |
| **Q2 routes** | B1 201 (anchor older than row, observed), B2 200. 17/17 on both drivers on a fresh DB, **and 17/17 on both on the upgraded seeded box.** |
| **Q2 census, seeded copy** | Round-2 DB (001→050) seeded **through the real routes**: 10 certifications (on 7 the anchor is strictly older than the row; 3 share the same millisecond), 1 revoke, 10 ordinary documents anchored after their rows, and 6 orphan anchors. Three template copies through `scripts/run-migrations.sh`: **round 3: rc 3, `051: 7 documents row(s)…`, trigger 0** (MAJ-B's census reproduced) · **round 4: `applied=1 failed=0`, trigger 1** · **round 4 + 1 planted claim: rc 3, `051: 1 documents row(s)…`, trigger 0.** |
| **Q3, the identical file on round 3** | **Prisma: 6/17.** Red: B1 (500), B2, A M1–M4 (**500** `Failed to create document`), N1 (helper false), N2 (050 → 500), N3, F1, F2 (`2 documents row(s)` = join rows). **node-pg: 12/17.** Red: B1, B2, N3, F1, F2, and the A cells pass, matching the gate's split. ⚠ B2, N3 and F1 on round 3 fail only as CONSEQUENCES of B1, so the census is measured by the runner row above, not by F1. |
| **Q3 unit** | The new measured fixture on round 3's helper: **2 of 12 red, exactly the two Prisma cells**. Round 4: green. |
| **Mutants on round 4** (all 17 cells loaded each time, so none is a LOADFAIL; every restore verified by md5, prosecdef, trigger def and file sha256) | **15/15 killed:** **S4** exemption removed (E1) · **M6** SECURITY INVOKER (E1, SETUP) · **S6** INSERT-only (E2) · **S2** RAISE reworded (A M1–M4, N1) · constraint renamed, node-pg (A, N1, E2) · round 3's pk arm re-added (B1, B2, N3, F1) · external-id arm off (A, N1, E2, F1, F2) · **S5** census never refuses (F2) · census arm B re-added (F1, F2) · DISTINCT removed (F2) · role check removed (F3) · **R1b** 051→409 mapping neutralised, Prisma AND node-pg (A M1–M4) · helper = round 3's (A, N1, N2) · helper constraint arm removed (A, N1, N2). **Controls survive:** C0 (comment in 051) and P0 (comment in 050). **File-pin mutants, unit:** P1 (051's RAISE reworded) killed; **P2 (ONE of 050's two arms reworded) killed**. K15 (no explicit `cause` read) survived at first, because Prisma's `cause` is enumerable, so I added the non-enumerable cell, which kills it. |
| **Suites** | originate unit **112 suites, 1395/1395** (round 3: 1393). `tsc` rc 0. |
| **develop moved** | `83ed01af70fd` → `fae056052f0e` (ls-remote 01:0xZ; fetched into MY clone only). 42 files changed; the only overlap with #1568 is `routes/documents.ts` (#1587's hunk at `-1513`; round 4 does not touch the file). No new migration. `merge-tree` of the current head gives rc 0, tree `4e1e36a708ae`, base `833984fc9` as the gate used. Re-predicted at GO. |

## NOT measured (limits, stated)
- **Anchoring is not booted.** M1/M2 rows are written by a stub that persists as anchoring does, and 051 reads only `anchor_store.document_id`. The full rewrite chain (the attacker's direct re-anchor through the real guard) is not re-run by me. **The gate's e2e covers it; please re-run M1–M4 on round 4.**
- One host and one clock, so INF-4 (census skew) is unchanged. That is KS-1630.
- Recertify and the expiry write use the same `saveCertification` upsert as B2; they were not driven separately.
- The push preflight runs in the build, not yet.
- Real boxes (kintsugi/demo) are not observable. A box where S registered AFTER flat-anchoring is refused (fail-closed, INF-2), unchanged from round 3.
- MIN-C, MIN-D and INF-7 are unchanged and out of scope.

## ⚠ Fault of mine: the author identity on `09588895d`
- `0958889` is authored AND committed as Kam's **personal me.com address**, not `kamil.kreiser@secuura.ai`. Every earlier #1568 commit (`767ab57`, `6c30a6d`, `938500c`) and develop use the Secuura one.
- **Cause:** in round 3's commit command I ran `git config user.email "<the personal address>"` with stderr discarded, and I never read it back. No script of mine carries it.
- **Nothing is merged, so develop is clean.** It is the same class as R 50th's card, on an OPEN PR, so it sits outside the standing force-push allow. **Kam's call.**
- **Fixed going forward:** my clone `dev83` is now pinned LOCALLY (`Kam Kreiser <kamil.kreiser@secuura.ai>`). `git config --show-origin user.email` reads `file:.git/config` in all three worktrees.
- **Options for Kam:**
  - (a) leave it; the squash authors as `kksecura <kamil.kreiser@secuura.ai>`;
  - (b) an author-only, lease-checked rewrite of `0958889`, trees asserted identical, as Kam ruled for #1597.
- **It does not block round 4:** the round-4 commit carries the right identity either way. If (b) comes after the gate, the head changes, so it needs a delta re-pin under the same-tree rule.

## Question
**Do you rule the round-4 design above, so I can build these 4 files and nothing else?**

## Meanwhile
**BLOCKED on the build.** Nothing is committed or pushed, and the branch stays at `09588895db75`. The watcher is re-armed.

## Needed by
No hard deadline. The build is about 30 min after your ruling: copy the prototype into the branch, commit, run the preflight, send READY FOR GATE.

Evidence lives in my scratchpad under `j13/r4/`: `logs/` (int_*.json per run, mutants_r4.log, runner_seeded_*.log), `tools/`, and prototypes `j13/r4proto` (round 4) and `j13/r3probe` (round 3 + the same cell file). Scratch PG: 55493 (round 3), 55494 (round 4), 55495 (round-2 base + seeded copies).

