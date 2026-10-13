# QA gate, round 6 (delta): Secuura Platform K PR #1497 (KS-695 part ii, the organisation erasure), head c48d7163

- **Report sha256/16:** `0d886f63f692f62a` (recipe: sha256 of this file with this 16-character value set to sixteen `0`s, first 16 hex characters; then written in here).
- **Head under test:** `c48d71638f330eb3a603a6e123471c4a1bbdf93e`, tree `01af5beacf9107c4ee11ec53414ce4919a27fcb2` (author's tree claim: TRUE). Develop: `3a87133760595b625617617daa587f8af1b821a7`.
  - **How obtained:** `git clone --shared` of Blockchain `2_Project_Files` into my scratchpad, push URL `DISABLED`; fetched `refs/pull/1497/head` and `develop` from GitHub over the project's `core.sshCommand` at 11:09 AEDT. Both shas match the brief. Every run below is on a detached worktree of that head inside my scratchpad.
  - **Nothing written in the project:** no git write verb and no file write under `!CODING`; no push; no GitHub or Linear write; no Kintsugi, demo or remote box.
- **Database:** my own throwaway PostgreSQL 15.14 on 127.0.0.1:55418 (55416 was taken by another session), data in my scratchpad. Init SQL 11/0, migrations 49/0, platform tenancy applied. `secuura_app` rolsuper f / rolbypassrls f; FORCE RLS t on documents, organizations, svc_api_keys, action_provenance; isolation `read committed` (printed by my SETUP cell). **Stopped** at the end (`pg_isready` rc 2).
- **Modes:** F = `MULTI_TENANCY_ENABLED=false`; T = `true` with `PLATFORM_DATABASE_URL` set. `falling back to single-tenant` count: 0 in every F and T log. Control: the author's new file with the platform URL unset gives 2, and its SETUP cell fails. My SETUP prints `poolBranch=true` in T.
- **Gate:** independent Opus delta gate, round 6, Tier 1 (destructive, GDPR-class), 2026-10-13.

## VERDICT: GO WITH NOTE

M-2 is closed. The erasure now refuses the fallback principal at both places the author named, before any key read and before any statement:
- **Real routes:** the round-5 cell K1 is now 403, with the whole database byte-identical (md5 of every row in the tenant, a row count of every public table, and every sequence's `last_value`). The planted-change control shows the same instrument catching a one-character change and one `nextval`.
- **Direct call:** calling the exported writer directly is refused too, with nothing written.

m-1 is closed. The second guard read rolls the whole transaction back when a colliding key commits before the blanking UPDATE's snapshot. That includes a key committed while the UPDATE statement itself is waiting. A key committed after the second guard cannot reach any row.

N-1 is closed: mutant G1 is now killed in both modes.

Every Major and Minor from rounds 1 to 5 still holds in both modes. All of the author's numbers reproduce. Develop is clean against the live tip.

**What is left:**
- **One Minor, wording.** The PR body says "the one newly refused key is the one that stores the literal `api-key`", which is false. Keys whose stored id is only whitespace are newly refused too. This is measured, and it errs in the safe direction.
- **Notes.** The main one: the author's real-Postgres R2 cell does not pin *where* the second read sits relative to the UPDATE. Unit cells do pin it.

The merge still needs Wednesday's head-bound GO. **I do not recommend deploying.** KS-1508 deploy, KS-1533 (M-1 path 1) and KS-1570 remain deploy blockers outside this PR.

## Majors

None.

## Minors

### m-1. The body's liveness sentence understates the refusal (it is wider than "the literal `api-key`")

**Where:**
- **The code:** `connectorOrganisationErasure.ts:114-116` refuses `connectorId.trim() === ''` or exactly `'api-key'`. JS `trim()` strips the whole Unicode whitespace set.
- **The PR body as posted** (author copy `pr1497_body_r6_as_posted.md`, line 10): "Liveness is unchanged ... The one newly refused key is the one that stores the literal `api-key`."
- **The published description** (`originate.openapi.ts:3728-3729`, and the yaml): names only "an empty or absent id" and the literal.

**Measured (cell V1, real route, both modes):** keys whose stored connector id is `' '`, `'\t'`, U+00A0, U+FEFF, U+3000 or U+2028 now answer **403**.
- These are not the fallback principal. The gateway's `connectorId || 'api-key'` keeps a whitespace-only string as is, so the principal is `connector: ` and so on, each one distinct.
- **Control:** with both refusals removed (mutant N1N2), the same keys answer **200 completed**.
- So round 6 newly refuses them, and "liveness is unchanged" is not true for them.

**Why only Minor:**
- It is wider in the safe direction: a refusal, nothing written.
- Every real id is `platform-s:<guid>` (register-connector, `api-gateway routes/platform.ts:728`).
- KS-1533 arm 1 now limits who may name a connector id at all.

**Minimal fix (wording only):** add "or whose id is blank or whitespace only" to the body sentence and the published description. Alternatively, narrow the predicate to `connectorId === ''` or the label, to match the collapse set exactly. The code is acceptable as it is.

## Notes

- **N-1. The real-Postgres layer does not pin the placement of the second read.**
  - **Mutant X2** moves the re-check to just BEFORE the blanking UPDATE, after the count. It **survives the author's real-Postgres file in both modes** (8/8).
  - The reason: R2 holds ACCESS EXCLUSIVE, so the erase stalls at the count, and any read placed after the count still sees the key.
  - X2 is killed by the unit statement-order cells (3) and by my **R3**. R3 holds `LOCK TABLE documents IN EXCLUSIVE MODE`, which lets the count run and stalls the UPDATE itself. The key and root commit there; the code answers 403, X2 answers 200.
  - The author's own N8 note describes the before-the-count case only.
  - **Suggestion:** add R3 (the EXCLUSIVE-mode shape) beside R2.
- **N-2. NULL-id and blank-id keys are now refused by name, not by accident.**
  - My cell N4 calls the resolver directly. It gets `OrganisationErasureFallbackPrincipalError` for a NULL key and for a `''` key, and the route answers 403 with nothing written.
  - With both refusals removed (N1N2), the same keys still get 403, through the ownership mismatch.
  - So the author's "liveness CONTROL" cells (unit `refusals` "already got 403 from the ownership comparison and still does", and integration "liveness is UNCHANGED") pass either way. They pin the status, not the reason. That is acceptable.
  - The unit cell's comment is now stale: the 403 comes from the fallback refusal.
- **N-3. A colliding key alone can turn A's erasure into a terminal 403.** Cell R3k: B commits only a key with A's id (no document) while A's UPDATE waits, and A gets 403. This is the same availability property the first guard always had, and minting a named connector id is now platform- or provisioner-only (KS-1533 arm 1, `security/src/index.ts:1203`). It is not a data defect.
- **N-4. Unchanged from round 5: deleted keys and legacy rows.**
  - Cell C5 still gives `200, documentsBlanked:2, B's root and derivative [erased]` in both modes, and is reachable only by a DBA delete.
  - The service header says a guard reading live keys "cannot see a key that was deleted or rotated away". "Rotated away" is inaccurate: a rotation (`security/src/index.ts:183-197`) only deactivates or expires a key, and the guard reads inactive keys.
- **N-5. Not measured: memory and the database can disagree on a legacy key's connector id.**
  - The security service upserts `connector_id = COALESCE(EXCLUDED, stored)` (`index.ts:401`) and validates from its in-memory key.
  - A pre-KS-869 key that lives in memory with id X while its row holds NULL would authenticate as `connector:X`, but the guard would not see it.
  - Read from code only; I did not run the security service. It closes on the next save or reload.
- **N-6. Cost of the added read.** With 50,000 keys in one tenant, `EXPLAIN ANALYZE` as `secuura_app` with RLS on shows a Seq Scan at **4.2 to 6.5 ms** per guard read, in both modes (there is no index on `connector_id`). Two reads per erasure. Negligible against the 25 s budget.
- **N-7. The live PR body was not fetched again.** The project's `gh` config is not logged in. I read the author's copy, `pr1497_body_r6_as_posted.md` (sha256/16 `5a1047a8a3dfc342`).

## Re-measurement of the author's claims

| Claim | Result | Instrument and control |
|---|---|---|
| (1) M-2 refused in the resolver before any key read, and at the top of the service before any statement | **TRUE.** K1 (r5 shape, real `/api/documents`, `/version`, a human child, then erase) gives **403 FORBIDDEN, diff `[]`** in F and T. All of B's rows, A's document and all four keys are unchanged. Direct service call (D1) with `'api-key'`, `''`, `' '`, U+00A0: `OrganisationErasureFallbackPrincipalError` (403 class), diff `[]` each time. The resolver unit cell's "before any key read" is pinned (mutant X1 reddens it). | Whole-DB snapshot (`evidence_runs.txt`). Controls: PC sees a one-character change and one `nextval`; D1's real-id control changes 3 tables; under mutant N1N2 the same K1 gives **200, blanked 4, B's derivatives `[erased]`** (the original M-2, reproduced). |
| Refusal set vs collapse set (`auth.ts:392`, `jwt.ts:289`) | Collapse set (code-read, end to end): NULL, `''` and `'api-key'`. Nothing between mint and erase normalises: the mint `z.string().optional()` (`security index.ts:637`); converters `?? undefined`; validate `\|\| null`; gateway `\|\| ''` then `\|\| 'api-key'`; route strips one `connector:` prefix. **Never narrower; wider by whitespace-only ids (m-1).** V1, both modes: `API-KEY`, `Api-Key`, lead/trail space, `\n`, TAB, trailing NBSP, ZW lead/trail, BOM-prefixed, U+2010/U+2011 hyphens, Cyrillic `а`, fullwidth, `connector:api-key` (double prefix), `apikey`, `api_key`, ZW-only: **200**, erasing only A's own document, **with B's `connector:api-key` row kept in every case**. Exact `api-key` and the whitespace-only set: 403, diff empty. | Control: under N1N2, exact `api-key` erases B's fallback row. |
| (2) m-1 second read after the UPDATE; a collision rolls back with 403 | **TRUE.** The author's R2 shape (my run): 403, and **no difference outside the 2 planted rows**, sequences included. **R3 (my shape, a commit DURING the UPDATE):** 403, full rollback, sequences unchanged, B's root kept. R4 (key and root committed after the second read, erase stalled at the revoke): **200, and B's root kept**, because it is newer than the UPDATE snapshot. r5's original R1 (N=100,000, commit while the count runs): was 200 with B's document `[erased]`, **now 403 in F (3,012 ms) and T (3,169 ms)**, B's document kept. | Wait observed in `pg_stat_activity` in every lock cell (`UPDATE documents` for R3; the count for R2; `UPDATE svc_api_keys` for R4). Mutants N7, N8 and X5 redden R2 and R3; X2 reddens R3 only (Note N-1). |
| R2 "fails if the wait never landed" | **TRUE:** `expect(sawLockWait).toBe(true)`, and the polled pattern matches only the erase's CTE. | Read, plus the mutant results above. |
| (3) N-1 cells | **TRUE:** mutant G1 (my N10) reddens the author's N-1 cell in F and T. It is invisible to unit (81/81). | |
| (4) Wording; the yaml differs by exactly one description string | yaml: a js-yaml structural walk 1484eac7 → head finds exactly `/paths//api/platform/organizations/erase-connector/post/description CHANGED`. The walk detects a planted `info.title` change. `check:openapi` rc 0, CHECK PASS, 414 example blocks. Wording: m-1, plus N-4's "rotated away". "Path 2 ... closed by the guard of rounds 5 and 6": true for live keys (C1, C2, C4, C6, K1 hold); N-4's deleted-key residue remains, DBA-only. | |
| (5) Numbers | **All reproduced:** unit two files **81/81**. New file **8/8** F and T. All 9 integration files `--runInBand` **9 suites / 96** F and T. Originate jest **103 / 1269**, twice. packages/shared vitest **49 files / 954**. tsc rc 0 with 0 lines. eslint on the 10 PR `.ts` files: 0 errors, 0 warnings (JSON shows 10 files checked; a planted unused variable is reported, as the control). `check:openapi` rc 0. | `evidence_suites.txt` |
| Author's mutants N1 to N16 and the comment-only control | Re-derived and re-run as N1, N2, N4, N7, N8, N10 (= G1), plus CTL; results below. The rest of N1-N16 not re-run (see NOT tested). | |

## Mutants (each applied alone; tsc rc 0; file restored byte-identical, sha256 `fb5d2ff619d1` after every one)

Layers: **U** = the 2 unit files (81 cells); **FP** = the author's real-Postgres file (F/T); **G** = my r6 file (F/T; cells K1, V1, D1, N4, R3, R2, R4).

| Mutant | Intent | U (red cells) | FP F/T | G F/T | Result |
|---|---|---|---|---|---|
| CTL | comment only | none | green | green | clean (control) |
| N1 | resolver refusal dropped | "resolveOrganisationErasureTarget ITSELF throws ...", "the refusal is LOGGED once ..." | green | **N4** | killed |
| N2 | service refusal dropped | "the SERVICE refuses a target ...", "a BLANK connector id ... refused the same way" | green | **D1** | killed |
| N1N2 (mine) | both refusals dropped | 6 M-2 cells | **K1, S2** | **K1, V1, D1, N4** | killed. The liveness CONTROLs stay green (N-2) |
| N4 | label not refused (blank only) | 5 M-2 cells | K1, S2 | K1, V1, D1, N4 | killed |
| N7 | re-check dropped | 5 (statement order, collision-after-UPDATE, logged, binds, ONE withTenant) | **R2** | **R3, R2** | killed |
| N8 | re-check moved before the count | 3 (statement order, collision-after-UPDATE, ONE withTenant) | R2 | R3, R2 | killed |
| N10 (= G1) | guard ignores inactive keys | none | **N-1 (G1 killer)** | none | killed (FP only) |
| X1 (mine) | resolver refusal after the key read | "resolveOrganisationErasureTarget ITSELF throws ... BEFORE any key is read" | green | green | killed (U only) |
| **X2 (mine)** | re-check between the count and the UPDATE | 3 (statement order, collision-after-UPDATE, ONE withTenant) | **green** | **R3 only** | killed by U and G; **survives FP** (N-1) |
| X3 (mine) | label compared case-insensitively | "CONTROL ... EXACT label ... API-KEY", "isFallbackConnectorId ... says yes only ..." | **CONTROL API-KEY** | green | killed |
| X4 (mine) | blank not trimmed | "a BLANK connector id ... refused the same way", "isFallbackConnectorId ..." | green | **D1** | killed |
| X5 (mine) | re-check refusal turned into a plain Error (a 500, so S retries) | "collision after the UPDATE refuses 403", "that refusal is LOGGED ..." | R2 | R3, R2 | killed |

## Item 4: earlier rounds' files on this head (both modes, as `secuura_app`, `--runInBand`)

- **r5 file:**
  - **K1 now 403**, with guardView `{"api-key":1,"NULL":2,"empty":1}`, all titles kept.
  - **C1:** 403, diff `[]`.
  - **C2:** active and inactive 403, diff `[]`.
  - **C3:** rotation 200, only the named key revoked, the snapshot changes (control).
  - **C4:** all 8 spellings 200, with B's variant rows and B's issued claims kept.
  - **C5:** 200 blanked 2 (N-4, unchanged).
  - **C6:** 200, the other tenant untouched.
  - **N3:** 200 blanked 3.
  - **P8:** 200, B `[erased]`, so M-1 path 1 is still open as the PR says.
  - **R1 (N=100k):** 403 (was 200 with B erased).
- **r4 file:** 12 passed, 4 skipped (slow), 1 failed in each mode.
  - The failure is **P6**, whose assertion pins round 4's *defect*. It answers 403 with all five of B's rows kept, which is the fix (as in round 5).
  - **P1:** 11/11 `consistent:true` in each mode.
  - P1b, P5a to P5f, P4 and P7 match round 5.
- **Repo files:** all 9 integration files 96/96 F and T, including bounds 25 and older 15.

## Item 7: the develop merges

- `merge-tree --write-tree` reproduces both merges exactly:
  - `1484eac79` (dc488c46 + b28bfaec) = `2b860804`.
  - `c48d7163` (858307a4 + 7c6b3d88) = `01af5bea`.
- **The PR's 11 files are blob-identical** across both merges (fix = head for all 11). No develop commit in `b28bfaec..7c6b3d88` touches them.
- **Live tip:** develop gained 1 commit (KS-1557, 6 files: verification routes and tests). The intersection with the PR's 11 files is **0**.
  - Its non-test lines touching `parent_document_id` or `organizations` are SELECT column lists only; there is no writer of `versionedById`, `parent_document_id`, keys or organisations. Control: the same grep finds 44 such lines in the PR's own service file.
- **`merge-tree head + 3a871337` = `d2ba49c1ecd6ae686a950f5229133ac683b0fea9`**, rc 0 with no conflicts, which equals the author's prediction.

## What I did NOT test

- **The security service, gateway and auth at runtime.** Minting `api-key`, `''` or whitespace; validate; the JWT exchange; the principal mapping. All read from code (cited lines). The originate half ran through the real routes, with the principal injected by the gate's auth mock, built by the gateway's exact rule.
- **Kintsugi or any box data.** Whether `connector:api-key` or whitespace-id rows or keys exist there: not queried.
- **Author mutants N3, N5, N6, N9 and N11 to N16, and J 4th's older set of 21:** not re-run. My X3, X4 and X5 cover N5, N6 and N9's intent.
- **The slow cells:** round-4 Q1 to Q4, B1 to B4 and the scale cells were not re-run. The budget code is unchanged apart from the added read.
- **Other tooling:** Schemathesis, Akto, Playwright, k6, the pre-push hook (legs 3, 4 and 8 included) and parallel (non-runInBand) runs: not run.
- **The live PR body:** not fetched (N-7).
- **Memory/database connector-id divergence in the security service:** not run (N-5).

## Evidence in this folder (`evidence/`)

- `evidence_topology.txt`
- `evidence_suites.txt`
- `evidence_runs.txt` (r6, r5 and r4 files, F and T)
- `evidence_mutations.txt` (all layers, plus unit by cell name, plus the N1N2 controls)
- `gate1497r6-attack.integration.test.ts.txt`
- `mut.py.txt`
