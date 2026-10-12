# Gate verdict: Secuura Platform K PR #1525 (KS-1538), legacy certify path needs document access

**Gate:** independent adversarial QA (Opus tier 1). I report findings only: no code fixes, no pushes, no GitHub or Linear writes.
**Date:** 2026-10-13.
**Head under test:** `b8393a44ec33984f7380cf5fdfb4f9cd8e87cd74`. This is the fix `1251ae7a3242` plus a merge of develop `69878dc5d1ae`. I took it from J 5th's bundle (sha256/16 `ac583727d5683561`, re-hashed by me). The bundle's prerequisites `69878dc5`/`b08ee629` came from a local scratch clone, and I did not contact any remote.
**Unfixed control:** `69878dc5d1ae` `certifications.ts` (sha256/16 `6692992be9446bbd`), swapped into the same worktree. The head file is sha256/16 `e177b53c080a1840`. Both shas were asserted before every run and restored afterwards. `git diff 69878dc5..b8393a44` touches only `certifications.ts` and the two new KS-1538 test files, so the swap reproduces the base tree exactly.
**Environment:** a throwaway PG15 on 127.0.0.1:55417 (since stopped; port verified free), schema from the head's `docker/init` + `migrations` (49 applied, 0 failed, platform tenancy applied). The app connects as `secuura_app` (rolsuper=f, rolbypassrls=f, asserted in every run). `documents` and `action_provenance` have FORCE RLS. Both tenancy modes ran. The SETUP cell asserts `getTenantManager() !== null` equals the mode: false for ST and true for MT.

## VERDICT: **GO WITH NOTE**

The PR closes what it says it closes: the legacy branch (`documentId`, no `parentDocumentId`). I found **no Major against this PR**. There are **5 Minors** and **2 notes**.

There is **one separate Major outside the PR's scope (S-1, lineage path)**. It is pre-existing and this PR did not make it worse, so it does not block the PR. It does mean the outcome "a non-owner can make org B's bytes verify as certified" is **still reachable** after this merge. Nobody should describe KS-1538 as closing cross-organisation certification.

I do not recommend merging. The merge also waits on Stuart's answer (ownerless DECISION) and on the develop-tip rule (the tip `81ac1ea6` was NOT tested; see NOT tested).

---

## 1. Hole on unfixed develop vs. closure at head (real routes, `secuura_app`, both modes)

**Instrument:** my probe suite (`evidence/probe/probe.integration.test.ts.txt`). It uses the real `documentsRouter`, `certificationsRouter` and `verificationRouter` on Express with `tenantGucContext` and `getRequestPrisma`, and the principal is injected by header in place of JWT auth. After each call it reads the stored row back with a superuser connection (`status`, `certified_at`, `certification_metadata.certificationId/issuerId`, `owner_user_id`). Each attack used a fresh org-B document, so one successful cell cannot mask the next.

**Full table:** `evidence/probe/matrix_table.md`.

**Control:** the same suite against base. ST and MT gave identical outcomes cell for cell.

| Caller | Target | base (ST / MT) | head (ST / MT) |
|---|---|---|---|
| org A user (ISSUER_ADMIN) | B doc by external id | 201, row → `certified` with A's cert | **403, row unchanged, 0 saves** |
| org A ORG_ADMIN | B doc by external id | 201, row certified | **403, unchanged** |
| org A connector, no onBehalfOf | B doc | 201, row certified | **403, unchanged** |
| org A connector + onBehalfOf(A's user) | B doc | 201, row certified | **403, unchanged** |
| org A connector + onBehalfOf(B's user) | B doc | 403 (OBO org mismatch) | 403 |
| SYSTEM_ADMIN / system_admin / super_admin | B doc | 201 certified | 201 certified (control) |
| SUPER_ADMIN (upper case) | B doc | 201 certified | **403**: see m5 |
| designated recipient (email upper-cased on doc) | that doc | 201 | 201 (control) |
| non-recipient | recipient doc | 201 certified | **403** |
| creating connector (REAL create with onBehalfOf, real provenance row) | its doc | 201 | 201 (control) |
| other connector | that doc | 201 certified | **403** |
| creating connector, onBehalfOf email unknown to K (owner NULL, provenance present) | its doc | 201 | 201 |
| creating connector, NO onBehalfOf (ownerless, no provenance) | its doc | 201 | **403** (DECISION, see N-1) |
| stranger | ownerless doc | 201 certified | **403** |
| any | B doc **by pkey UUID** | 201, row NOT changed | 403 for strangers; owner/admin 201, row NOT changed (m1) |
| user / connector | unknown `doc-…` / unknown UUID | 201, save 1 | 403, 0 saves; **5 refusal bodies byte-identical** (unknown ext, unknown UUID, unknown via connector, not-yours user, not-yours connector) |
| user A | `documentId` + `parentDocumentId: ""` | 201 certified B | **403** |
| user A | `documentId` as array / `parentDocumentId` null, 0, false | 400 | 400 |
| user A | upper-cased ext id / trailing space | 201, 0-row UPDATE | 403 |

**Author's suites, re-run by me:**
- Base: unit **13 failed / 19**; integration **6 failed / 10** in BOTH modes. Every integration failure is `Expected: 403 / Received: 201` or the row-diff assertion.
- Head: unit 19/19; integration 10/10 ST and 10/10 MT.
- Whole originate unit jest at head: **103 suites / 1234 tests passed**.
- `tsc --noEmit` at head: rc 0, 0 lines.

All of these reproduce the author's numbers (`evidence/suites/`).

## 2. Author's attack items 1-4

1. **external_id vs pkey split** (`documentRepo.ts:233-262` resolves external_id, then pkey; the UPDATE at `certifications.ts:602-611` addresses external_id only). **Not exploitable for cross-org writes.**
   - Shadowing another document's pkey with `documentUuid` through the real route is refused with **409** (KS-596 guard, `documents.ts:670-693`).
   - Constructed state: I rewrote B's external_id via superuser SQL to equal A's own pkey, then user A named that id. Head refused with 403 because the external_id lookup wins and finds B's document; B's row was unchanged. Base: B's row was certified.
   - Residual: pkey addressing is a **silent no-op** for authorised callers (m1).
2. **`wasCreatedByConnector` on the global prisma, no tenant predicate** (`provenance.ts:285-296`). **Not exploitable cross-tenant** as measured.
   - A provenance row in tenant T2 naming a T document gave 403, because FORCE RLS on `action_provenance` plus the request's tenant GUC hides it in both modes. Control: the same row in T gave 201.
   - A human whose id appears as `connector_id` gave 403 (the arm is connector-role only).
   - **Exploitable in a narrow shape: stale provenance (m3).**
3. **Timing.** **Measurable locally; not measured over a network.**
   - Setup: N=200 per series, interleaved, after a 20-call warm-up, `process.hrtime` around the fetch, all 403.
   - **Control A/A:** unknown ext 0.923 ms vs unknown ext 0.921 ms.
   - **Connector:** not-yours **1.474 ms** (p10 1.286) vs unknown **0.923 ms** (p90 1.165), so the distributions separate.
   - **Human:** unknown UUID-shaped id **1.466 ms** vs not-yours 0.952 ms (the pkey fallback query).
   - Source: `evidence/probe/probe_head_timing1.json`. See m4.
4. **Check and UPDATE not in one transaction.** **Exploitable as a race, low severity (m2).** I measured the window shape with a constructed state.

## 3. Item 5, the lineage path: a separate finding, NOT a blocker for this PR

**S-1 (Major, outside the PR's scope, pre-existing on base and unchanged at head, both modes): any write-role caller in the tenant can make another organisation's bytes verify as CERTIFIED, under an issuer name the caller chooses.**

Steps to reproduce (probe cells ITEM5 / ITEM5c):
1. Org B's user registers bytes with hash H. `POST /api/verification/verify {contentHash: H}` returns `checks.isCertified: false` and no `certification`.
2. Org A's user calls `POST /api/certifications/issue` with `{type: 'verification_certificate', parentDocumentId: <B's doc OR A's OWN doc>, data: {title, contentHash: H, issuedBy: 'Org B Official Registrar'}}` and gets 201.
3. Verify of H (anonymous and as B) now returns `checks.isCertified: true` and `certification.certifiedBy: "Org B Official Registrar"` with `certifierOrganizationId: null`. With B's document as parent, B's document also gains a `newerVersions` entry owned by A. B's own row is untouched.

The cause is two independent defects:
- **(a) No access check on `parentDocumentId`.** `certifications.ts:412-431` checks only for cycles, and `saveDocument` resolves the parent by external_id within the tenant (`documentRepo.ts:419-450`).
- **(b) The derived row's `content_hash` is taken from caller-supplied `data.contentHash`** (`certifications.ts:564-567`). `siblingCertification` (`verification.ts:220-236`) then treats any same-hash `signed` row carrying a `certificationId` as certification evidence for those bytes. The ITEM5c control, where A's own document is the parent, proves that (b) alone is enough. A parent access check alone would **not** close S-1.

**Oracle:** Purpose / Statutes (a trust system's verify claims a certification that no authorised party made); this is the charter's top defect class.

**Does #1525 make it worse?** No. Base and head behave identically on this path, and the PR's guard is skipped by design when `parentDocumentId` is set (`certifications.ts:218`). Before the PR, the legacy path reached the same outcome more directly. **Recommendation:** file it as its own ticket. Fix-shape for the owner: require the same access predicate on the parent, and bind the derived row's hash to the parent's stored hash rather than to the caller's `data`. Regression test for the owner: the ITEM5c shape (A's own parent, B's hash), asserting that verify of H stays `isCertified: false`.

Also measured, by design and not a defect of this PR: `documentId = B's doc` + `parentDocumentId = A's own doc` gives 201 with B's row untouched. The legacy branch is skipped and `documentId` is ignored.

## 4. Legitimate callers that could break

**Instrument:** `git grep` over the head tree, with non-test call sites read.
- The issuer frontend `certificationApi.issue()` (`frontend/issuer/src/services/api.ts:444-456`) has **zero call sites** in `frontend/`. No caller passes `documentId` from inside the repo:
  - Not sending `documentId`: euro-office plugin, flutter app, libreoffice extension, nextcloud app, the Python SDK, `deploy-all.sh` smoke, and the systemTest inline runner.
  - The JS SDK passes its input through.
- **The only at-risk external caller is Platform S.** S keeps working on documents it created with `onBehalfOf` (measured 201), including when the OBO email is unknown to K (201).
- S **loses** legacy-certify on documents it created with no `onBehalfOf`: 201 → 403 (N-1, the stated DECISION). That waits on Stuart.
- `SUPER_ADMIN` callers on documents they do not own: 201 → 403 (m5).

## 5. Mutants (instrument: author's unit + integration (ST) suites; control: the unmutated head is 19/19 + 10/10)

Each mutant asserted its anchor (count == 1), its marker present, and its sha changed. The file was restored by `git checkout` and checked against sha16 `e177b53c080a1840` after every run, including on SIGTERM.

| Mutant | unit | integ | Killed? |
|---|---|---|---|
| M1c predicate removed from pre-check (type-opaque) | 9 red | 6 red | **killed** |
| M1b predicate always true | 9 red | 6 red | killed |
| M2 pre-check moved after `saveCertification` | 3 red | 3 red | **killed** |
| M3 unknown → 404 NOT_FOUND | 1 red | 1 red | **killed** |
| M3b unknown → same 403, message differs by one `.` | 1 red | 1 red | **killed** |
| M4 creating-connector arm dropped | 1 red | 1 red | **killed** |
| M4b connector arm admits any connector | 2 red | 2 red | killed |
| M5 admin arm dropped | 1 red | 2 red | killed |
| M6 recipient arm dropped / M6b case-sensitive compare | 1 red | 1 red | killed |
| M7 owner arm dropped | 3 red | 2 red | killed |
| M8 ownerless open like GET | 1 red | 1 red | killed |
| M9 guard condition inverted | 13 red | 6 red | killed |
| M10b UPDATE catch silent again (type-opaque) | 1 red | 0 red | killed by the **unit** cell only |

**Self-correction, in the open:** my first runs of **M1** (`!legacyDocument` only) and **M10** (`void(...)`) went red on **TS6133 / TS2695 compile errors**. Those are not semantic kills. My first runner also mis-flagged their integration reds as non-compile, because the integration logs fail in `beforeAll` with blank reasons and my `error TS` scan was blind to ANSI codes. I replaced both with the type-opaque M1c and M10b above, which are killed semantically. The original M1 and M10 are recorded as compile-only in `evidence/mutants/scan.txt`.

## 6. Findings (all Minor; none blocks)

- **m1. A pkey-addressed `documentId` passes the new check, but the UPDATE silently does nothing** (`certifications.ts:219` resolves the pkey via `getDocument`; `:608` matches `external_id` only).
  - Measured: the owner and SYSTEM_ADMIN get 201 with a certification saved, while the row stays `anchored` with no `certified_at`, and nothing is logged. The new catch logs only *thrown* errors, not a 0-row UPDATE.
  - Pre-existing (identical on base). Oracle: Product consistency (201 for a document that was not certified).
  - Fix-shape: resolve to the row's external_id from `legacyDocument` before the UPDATE, or log or refuse on 0 rows.
- **m2. Check-then-UPDATE window** (`certifications.ts:218-224` vs `:602-611`). The window spans the holder lookup and the anchoring POST, whose timeout is 10 s (`:443-461`).
  - Constructed: the owner passes the check, the owner flips to B during a 1.5 s anchoring delay (SQL simulating `transfer-custody`, `documents.ts:1893-1898`), and the UPDATE then lands on a document B now owns, carrying A's `issuerId`.
  - The caller was authorised at check time. Low severity. Not reproduced through the real transfer route.
- **m3. Stale provenance admits a former creator** (`provenance.ts:288-292`; the same arm is used by GET at `documents.ts:1068`).
  - Constructed: connA creates documentUuid U with onBehalfOf, U is deleted (superuser SQL), userB re-registers U, and connA certifies B's document with 201, row certified.
  - This needs a deletion plus deliberate reuse of the UUID. It belongs to predicate (O), not this PR. Owner should consider: provenance rows keyed to the pkey, or deleted with the document.
- **m4. Timing oracle** (see 2.3): about 0.55 ms locally for a connector (not-yours vs unknown) and for humans on UUID-shaped ids. Bodies are identical; latency is not. GET has the same shape. I did not measure it over a network.
- **m5. Role-set drift:** `SUPER_ADMIN` (upper case) passes the write gate (`documentWriteRoles.ts`, `DOCUMENT_WRITE_ROLES`) but not the admin arm (`certifications.ts:118`, which lists `system_admin|SYSTEM_ADMIN|super_admin`). Measured 201 → 403. This mirrors GET (`documents.ts:1014`), so it is "predicate (O)" as ruled, but it is a silent behaviour change for any `SUPER_ADMIN` JWT. The role is real elsewhere (`keyRevokePolicy.ts:59`, `auth/routes/users.ts:193`).

**Notes**
- **N-1 (DECISION, measured):** a connector's own ownerless document (no onBehalfOf, so no provenance row) goes 201 → 403 in both modes. This is the evidence Stuart's answer needs.
- **N-2:** the probe found 0 rows left after cleanup in every run (`*.cleanup`). My probe file sits only in my scratch worktree and was never committed.

## 7. NOT tested (Rule 2)

- **Develop tip `81ac1ea6`.** The object was not available locally and I did not fetch from GitHub. I made no merge prediction against it. The moved-tip rule still applies at merge time.
- Real JWT `authenticate()` (the principal was header-injected), the real gateway/CSRF, the real auth-service holder stub, the real anchoring service (a local stub answering 500), and `NODE_ENV=production` (the 503 path).
- MT mode used the **same** database as the platform DB. Separate per-tenant databases were not exercised.
- Cross-tenant verify of S-1. The verify calls carried tenant T.
- The `admin` (lower-case legacy) role, the holderEmail + documentId combination, and concurrent double-submit of the same certify.
- Timing over a network. The m2 race through the real `transfer-custody` route. The m3 deletion through a real deletion route (adminConfig org purge / KS-695 erasure).
- Schemathesis, Akto, Playwright, k6, eslint, and the repo pre-push hook.
- Other services and the frontend at runtime (call sites were read, not run).

## 8. Evidence index (`evidence/`)

- `probe/`: probe source; per-run JSON (`probe_base_st1`, `probe_base_mt1`, `probe_head_st1`, `probe_head_st2`, `probe_head_mt1`, `probe_head_timing1`); `matrix_table.md`; the runner, PG setup and table scripts; `tsc_head.log`.
- `suites/`: author suites at base and head, both modes, plus the full originate tail.
- `mutants/`: runner sources, result JSONs and `scan.txt` (the compile-vs-semantic classification).
