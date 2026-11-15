PR 2233: GO WITH NOTES (at head eccb360e505e46edcff3904ff227cf071fecbca9; tier 1)

Gate 356 (tier 1, Opus), re-commission. Run 2026-11-15 17:32 to 17:45 AEDT. Findings only: nothing was fixed, pushed, posted, commented, mailed, merged, or written to Linear or GitHub.

**Re-commission note.** The first gate agent died at 17:31 before it wrote a verdict. I treated its logs (`scratch/out-*`, `pin1.out`, `triple.tree`, `out-suite-*`) as unverified hints and cite none of them. Every figure below comes from my own `scratch/g2_*` files.
- I reused its clone after confirming refs/remotes/pr/2233 = eccb360e505e and origin/develop = ce35818d50ae, with the push URL `DISABLED`.
- I reused its worktrees after reading their shas and porcelain (0):
  - `wt-dev` is at develop ce35818d50ae;
  - `wt-head` and `wt-plant` are at local probe commit 6ae0b8cd8304. I checked that commit: parents develop ce35818d + head eccb360e, tree fc1249e2ecfc. That tree equals my own `merge-tree` of develop × head, so these two worktrees ARE the merge.
- I rebuilt `packages/shared` in all three trees (rc 0). Its dist in `wt-plant` was empty.

**Pins.** Read by `gh api` (account kksecura) at 17:32:51 and again at 17:44:00 AEDT:
- PR 2233 head eccb360e505e46edcff3904ff227cf071fecbca9, open, mergeable_state unstable
- develop ce35818d50aebe7f41fc41f677ee03079c36d7ad
- PR 2160 head b02bd2716cc2176cd6d2acd6b75885781f6c58d4, open

Nothing moved. The head's develop has moved since the PR was built:
- The PR is ONE commit on 4e4347818772. develop is now ce35818d50ae, which is PR 2140's merge and differs from 4e43478 in one path, a packages/shared test file.
- `merge-tree --write-tree` of develop and the head, both orders: rc 0, the same tree fc1249e2ecfc (`scratch/g2_out-mt.txt`).
- Merge vs head: 1 differing path, develop's own one.
- certifications.ts: develop 4257bdf3ba6e, then head 6eff2cfa755c. The merge holds 6eff2cfa755c.
- The diff is 9 files, +473 -1, equal to the READY.

## FOUND

**G356-2233-1 (Low; disclosed in the PR body; no change needed in this PR; for the board).** The issuer portal still shows Share to some viewers whom the route now refuses.
- `DocumentDetail.tsx` shows the Share button when the status is `certified`, and "Certify Verification" when it is `verified`. The page is loaded through `GET /api/documents/:id`, which admits:
  - the owner;
  - `system_admin` / `SYSTEM_ADMIN` / `super_admin`;
  - a recipient matched by email (`documents.ts`, `isRecipient`);
  - the creating connector;
  - anyone, when `owner.id` is empty.
- The new guard (`callerMayReadCertification`) admits:
  - `isPlatformRole`;
  - `issuer.id` (= `issuer_user_id` || `certMeta.issuerId`);
  - `holder.id` (= `owner_user_id` || `certMeta.holderId`).
- Every document owner passes, because the document's `owner.id` is `owner_user_id` || `issuer_user_id`, so it always matches holder or issuer.
- Two viewer classes see the button and now get 404 "Certification not found":
  - an email-matched recipient who is not the owner;
  - any viewer of an ownerless (bare-connector) row.
- A share recipient holding shareType `reshare` also cannot reshare. Nothing honoured `shareType` before this PR either.
- This is the same audience `GET /api/certifications/:id` has refused since KS-1695, and the card's "issuer, holder or admin" chose it.

**Exact action:** one board ticket, either to hide Share and Certify Verification from non-parties in the portal, or (Kam's call) to admit email-matched recipients. Not a block.

**G356-2233-2 (Info, for Kam's awareness; ruled, not a defect). How "like revoke" was read.**
- The card's label says "Guard share and recertify like revoke". Its detail says "the per-record check (issuer, holder or admin)". Revoke itself is issuer-only and answers 403.
- The PR builds the detail's audience (platform admin, issuer, holder, issuing connector) and refuses with each route's own 404. That follows Wednesday's ANSWER of 04:39Z, and the body states both readings.
- The tests pin the reading chosen. My `issuer_only` mutant (the literal revoke rule) reddens O3, O4[system_admin] and O4[SUPER_ADMIN].
- **"admin" was taken to mean platform admin only.** A same-tenant `ORG_ADMIN` non-party is refused (S3, R3). This is consistent with KS-1695's GET.
- If Kam meant tenant admins, or wants 403 like revoke, each is a one-line change per route.

**G356-2233-3 (Info; ruled by card a; stale wording).** Recertify's documented user, "a Verifier who has verified it" ("Verifier → Certifier": the handler doc at certifications.ts:1439, and originate `index.ts:138`), is now refused unless they are a party. Option c of the 1115 card named this user explicitly, and Kam chose a, so the behaviour is ruled. The route's prose still describes a third-party verifier. It is worth a wording ticket; not a block.

**G356-2233-4 (Info; test reach, not a gap).**
- **The empty-principal guard cannot be reached on these two routes.** The helper's `if (userId === '') return false` sits behind `getUserFromRequest`, which returns null on a falsy `userId`, so both routes answer 401 first (C3). My `no_empty_guard` mutant reddened 0 of 24 cells. S4 and R4 (a bare row) are refused by inequality alone. They DO go red when the guard is removed, so they are not dead cells; their titles say a little more than they pin.
- **Placement.** The guard-after-the-email-loop and guard-after-the-charge mutants redden the same set (S2 to S5). S2 is the cell that sees the email, share row and charge.

## TESTED

**Q1. The guard precedes the email, the charge and the anchor POST, and refuses with the route's own 404.**

Order at the head, read from source:

| Route | Steps in order |
|---|---|
| share `:1340-1366` | validation → 401 if no user → `getCertification(id, tenant)` → 404 → **guard `:1360`** → revoked 400 → per recipient `saveShare` + `notifyDocumentShared` (EMAIL) → `createChargeEvent('share')` → 201 |
| recertify `:1452-1480` | validation → 401 → `getCertification` → 404 → **guard `:1474`** → revoked 400 → anchor `fetch(POST /api/anchors)` → `saveCertification` → `createChargeEvent('verification_certificate')` → 201 |

- **Reuse, not copy.** The helper is defined once (`:162`). Its call sites are GET `:1105`, share `:1360`, recertify `:1474`, lineage `:1636` and evidence-bundle `:1729`.
- **The refusal body.** Each refusal duplicates its route's own not-found literal: share "Certification not found", recertify "Original certification not found".
- **Identity.** The helper's `req.user.userId` is the same value the routes' `getUserFromRequest` returns as `user.id` (`:81-93`).

Mutants (ks1699 file, 24 cells; `scratch/g2_plant.py`, `g2_plants.out`):

| Mutant | Reds |
|---|---|
| Baseline at the head | 24/24 pass |
| share guard removed | S1-S6 |
| recertify guard removed | R1-R6 |
| share guard after the revoked check | S5 |
| recertify guard after the revoked check | R5 |
| share guard after the email loop | S2-S5 |
| share guard after the charge | S2-S5 |
| recertify guard after the anchor POST | R2-R5 (anchor counted on a real local server) |
| refusal 403, same body | 10 (S1, S3-S6, R1, R3-R6) |
| share body one byte (trailing `.`) | S1, S3-S6 |
| recertify refuses with the GET/share bytes | R1, R3-R6 |
| literal revoke rule, issuer only | O3, O4×2 |
| admin branch disabled | O4×2 |
| holder branch dropped | O3 |
| guard added to verify | V1 |
| empty-userId guard dropped | none (G356-2233-4) |

- My first admin mutant, which deleted the line, failed to COMPILE under ts-jest (TS6133, `isPlatformRole` unused). I replaced it with `false &&`, and that version reddened O4×2.
- After every plant the file was restored, `hash-object` read back 6eff2cfa755c, and porcelain was 0.

**Q2. Verify stays OPEN (card c).**
- `POST /:id/verify` at the head (`:1250-1312`) has no party check; the blob diff touches only the share and recertify hunks plus a doc note.
- Cell V1 pins that a same-tenant stranger gets 200 and one verification charge.
- My `verify_guarded` mutant reddens V1, so the pin can fail.
- PR 2228 (the earlier verify guard) is closed, not merged: `gh api` state closed, `merged_at` null.

**Q3. Census of in-repo callers.**

Instruments:
- whole-repo `git grep` at the head for a templated `certifications/${…}/(share|recertify)`;
- `certificationApi.share|recertify|verify(` counts;
- e2e spec, Python and YAML greps for `recertif|/share`.

Positive controls: ShareDialog, RecertifyDialog and api.ts are found; `certificationApi.getLineage(` = 1 against share 0, recertify 0, verify 0; the tsx control pattern hits 3 files.

Callers found:
- **share:**
  - issuer portal `ShareDialog.tsx:87`, reached from `DocumentDetail`. Owners and platform admins pass; see G356-2233-1 for who does not.
  - e2e-v2 `api-client.ts:291` `shareDocument`, used 3 times:
    - `certification.api.spec.ts:94` uses the all-zero id and accepts any status under 500;
    - `certification-lifecycle.e2e.spec.ts:149` is a fallback reached only on a 5xx, as the issuer, who is a party;
    - `:228` (after revoke) expects `!ok`.

    None is broken.
  - Every other e2e and Schemathesis share call is `/api/documents/:id/share`, a different route.
- **recertify:**
  - `RecertifyDialog.tsx:54`, shown only for status `verified`. My grep found 0 code that sets status 'verified' in services, migrations or packages (control `'certified'`: 1), so it is likely unreachable today.
  - The other hits are unit tests only.
- **SDKs:** the JS SDK has only `certifications.verify` (`:129`) and no share or recertify.
- **Gateway:** it proxies `/api/certifications` to originate (`proxy.ts:663`, `authenticateToken(false)` + scope), so both guards are on the live path. Its `batch.ts` posts only `/api/certifications`, which is issue.

Gate 351's caller classes, revisited:

| Class (gate 351) | Now |
|---|---|
| (a) JS SDK non-party verify | admitted (verify open, V1) |
| (b) 'verify'-share recipients | admitted to verify; refused on share and recertify unless a party |
| (c) Verifier → Certifier | refused on recertify, as card a chose (G356-2233-3) |
| (d) same-tenant ORG_ADMIN non-party | refused (S3, R3), as on GET |

- Platform S: 0 hits in my grep, and Stuart said on 20 Oct that it calls neither route.
- No live in-repo caller that is a party is refused.

Fixture edits, re-measured (`scratch/g2_fixtures.py`, `g2_fixtures.out`):
- develop's versions of the 4 edited files over the HEAD route: **14 fail of 20**. This equals the READY's 14.
- The head's versions over DEVELOP's route: 0 of 20 fail, so the edits do not depend on the guard.
- The head's versions over the head: 0 of 20 fail.
- By diff, the edits are fixture rows only (`issuer: { id }` added; ks543's issuer becomes the caller) plus comments. No assertion changed.

**Q4. The overlap with PR 2160** (`scratch/g2_2160.sh`, `g2_2160.out`, `g2_out-mt.txt`).

| Merge | Both orders |
|---|---|
| head × 2160 | rc 0, tree 4913923e385d (equals the READY) |
| (develop+2233 probe 7e808ccbf6f9) × 2160 | rc 0, tree 7d0989f1caa5 |

- **The hunks are disjoint.** 2160 changes base line `:935` (the `/issue` outer catch, +7 -1). 2233 changes `:157`, `:1351` and `:1457`.
- **Both changes keep their meaning in the combined file:**
  - combined vs (dev+2233) has the same patch-id as 2160's own diff (1c7ddb91d071);
  - combined vs (dev+2160) has the same patch-id as 2233's own diff (2c37d6a910e0);
  - the KS-2017 marker appears 1 time and KS-1699 3 times, each equal to its source.
- **Planted-conflict control:** an edit on head line 938 (base 935 + 2233's own 3-line offset) conflicts with 2160 in both orders (rc 1, `CONFLICT (content)` on certifications.ts).
- **Far-edit control:** an edit at line 20 merges rc 0 in both orders.

**Red-proof, reproduced by me.** develop's product blob in the merged tree gives 12 failed / 12 passed (S1-S6, R1-R6). All 12 are `expect(received).toEqual(expected)` assertion failures, none a runtime error. At the head: 24/24. This equals the READY.

**Whole originate suite** (jest JSON, interleaved dev → merge ×2, Node v26.8.1, load1 12 to 26; `scratch/g2_suites.out`):

| Tree | Run 1 | Run 2 |
|---|---|---|
| develop ce35818d50ae | 222 files / 2609 tests, 2609 pass, rc 0 | same |
| merge (6ae0b8cd, tree fc1249e2) | 223 / 2633, 2633 pass, rc 0 | same |

2609 + 24 = 2633, equal to the READY. Porcelain was 0 after every run.

**tsc and eslint** (`scratch/g2_tsc_lint.out`):
- `tsc --noEmit -p services/originate/tsconfig.json`: rc 0 at develop and at the merge. A planted TS2322 gives rc 2 (1 error), then restored to 6eff2cfa755c.
- eslint (ESLint API, Dev root flat config), on the 7 touched TS files at the merge: 0 errors.
  - There is 1 warning, `ks1385:126 no-useless-assignment`. It is the same warning as develop's `:123`, shifted by the +3 fixture lines, so it predates this PR.
  - Planted control (`var` + `debugger`): 2 errors.

**Body** (live by `gh api`, 9,494 characters):
- Both card texts are quoted, along with both readings of "like revoke".
- Test Evidence is present (1), and `13/16 legs ran` is quoted (1).
- Title starts `Refs KS-1699:`.
- Self-hold regex: 0. Close-words regex: 0.
- The body already discloses the email-recipient refusal (G356-2233-1) and the unreachable recertify UI.

## HOW
- **Clone:** `scratch/clone` (the first agent's, verified as above): `--reference` to the Blockchain object store, push URL `DISABLED`. I ran no fetch. Every sha I needed was already present and equal to the `gh api` pins.
- **Worktrees:** `wt-dev`, `wt-head` and `wt-plant`, sparse on `Blockchain/Dev` + fragments.
  - Plants and fixture swaps were made only in `wt-plant` and restored by content, with a `hash-object` check.
  - All three ended with porcelain 0.
- **New local objects in my clone only, never pushed:** probe commit 7e808ccbf6f9 (dev+2233), planted-conflict and far-control commits (author gate356b). I made no ref.
- **My scripts:** `g2_mt.sh`, `g2_suites.sh`, `g2_plant.py`, `g2_fixtures.py`, `g2_tsc_lint.sh`, `g2_lint.mjs`, `g2_2160.sh`. Outputs are `g2_*`.
- python3 was 3.14.10 throughout, so the 15:56 to 16:08 Apple-3.9.6 window does not apply.
- No writes outside this folder.

## NOT TESTED (UNMEASURED)
- A running stack, Postgres, a real gateway + originate pair, the real email send, and the anchoring service. The cells use an in-process router with a mocked repository and mocked `authenticate()`; only the anchor counter is a real local HTTP server.
- Whether any service or out-of-repo integration sets document status `verified` beyond my grep; the portal's rendering of the 404 (read only: the axios interceptor sanitises the error to a generic message).
- Node 24, the docs-fragments checker, `check:test-types`, the pre-push hook legs, Schemathesis, Akto, Playwright, k6.
- Out-of-repo callers of share and recertify, including Platform S beyond Stuart's statement.
- Linear: KS-1699's state and comments were not read.
- The R 119th HANDOVER was not opened; I read the READY and the wrap.
