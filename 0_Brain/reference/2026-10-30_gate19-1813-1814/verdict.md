# QA GATE 19 - Secuura/Blockchain PRs #1813 and #1814 (tier 1, security surfaces)

Base `develop` = `d7ddfa1f64336602a3441964f636e7d57a20c1d7` (ls-remote at start, 2026-10-29T15:20:11Z, and again at end, 15:37:10Z). Heads read at origin in the same action as the pin, and asserted equal to the brief at both times: #1813 `77a807d188ab24e2a101ee4cc6d9fe721bb46dc3`, #1814 `277e5ba6b7ae8b7f947ef1153ac4c33b4d7c1975`. **Neither PR moved during the gate.** My clone is `work/repo`, made at a non-existent path, with its toplevel asserted before any fetch. Network git used the Secuura deploy key through `core.sshCommand` with `GIT_SSH_COMMAND` unset. This gate is findings only: I pushed, commented, merged and messaged nothing, and wrote nothing under `!CODING`.

## BLUF

- **#1813 @ 77a807d1: GO WITH NOTES.** 0 blocker, 0 major, 1 minor, 5 info. **No finding is fix-before-merge.**
  - **No read path on either route gets past the gate.** I tried the `:id` document-id fallback, a legacy non-prefixed anchor id, upper-case `ANCHOR_`, `%20` padding, a trailing slash, an upper-case primary key in the row, and a whitespace-padded tenant claim. The two tenantless shapes (an absent `tenantId`, or a snake-case `tenant_id` only) are allowed, as declared gap ii.
  - **Status, body, Content-Type, Content-Length and ETag are byte-identical to the absent answer.** The PR's own cells check this; my A1 and A3 extend it.
  - **One leak is left: the work class.** A refused read runs one extra DB transaction (the ownership probe) that an absent read never runs (A4, measured in-process). That is a timing side-channel in principle (Minor, follow-up).
  - **No legitimate same-tenant reader I could construct breaks.**
- **#1814 @ 277e5ba6: GO WITH NOTES.** 0 blocker, 0 major, 2 minor, 5 info. **No finding is fix-before-merge.**
  - **Every refusal happens before the anchoring fetch.** That includes a fault in the provenance probe.
  - **Platform S is unaffected:** its creating connector re-anchors its own ownerless document and a /version-minted child. A foreign connector is refused with the 404 cloak.
  - **The admin spellings are exactly the three literals** that `GET /:id` and `callerMayCertifyDocument` use.
  - **OWNER role: exactly the card default and nothing wider.** OWNER re-anchors only its own documents. Foreign, ownerless, and foreign-with-a-provenance-row are all 404.
  - **Revoked/deleted documents:** refused at this route, and the write passes `preserveTerminalStatuses`.
  - **The two minors:**
    - A revoked document can still end up anchored by a chain through the sibling `POST /:id/sign`, which un-revokes. That route is pre-existing and already filed as KS-1831.
    - The 202 body says `anchored` even when the guarded write kept a revoke that landed mid-flight.
  - **KS-1829 is comment-only** (`git diff -w`: 0 non-comment lines; the control, the product commit, shows 36).
- **Merge order:** the code is independent; the only conflict is docs.
  - Each PR is clean against develop by itself (merge-tree rc 0).
  - Merged together, in either order, they conflict in the two `Projects Documents/*.html` files only, and **both number their new section `113`**.
  - Recommendation: **#1813 first**, then a docs-only re-prep of #1814 that renumbers its section to **114** and keeps both blocks. #1813 is 7 commits behind develop, but none of those commits touch `services/anchoring`.

## Spark half (run FIRST per PR, bare base ref `develop`; an input, not my verdict)

- **#1813:** exit 0.
  - Head tip `77a807d1`. **The merge-base is `5a5c4d2b`, not develop's tip**, because the branch predates the last 7 develop commits.
  - Diff: 6 files, +710/-0.
  - Targeted: **HEAD 12 pass / 0 fail; BASE product code 5 pass / 7 fail**, which matches the seat's 7 of 12 red.
- **#1814 (second run, the valid one):** exit 0. Head tip `277e5ba6`, merge-base `d7ddfa1f`, diff 7 files +435/-9. Targeted: **HEAD 28/0; BASE 12 pass / 16 fail**, which matches 16 of 28.
- **Harness fault, mine:** I launched both Spark runs at once against the one clone.
  - They share `FETCH_HEAD`. The #1814 run read develop's sha as its PR tip and refused with exit 3 "head sha mismatch" (kept as `evidence/spark_1814.try1_fetchhead_race.out`).
  - I re-checked origin (unchanged) and re-ran it alone.
  - The #1813 run's tip line is correct, so it was not affected.
  - Proposal: `spark_gate.sh` should fetch into a private ref instead of reading `FETCH_HEAD`.
- No `spark_review.py` LLM verdict was run (not requested).

## Verdicts

| PR | verdict | B | Ma | Mi | I | fix-before-merge |
|---|---|---|---|---|---|---|
| #1813 @ 77a807d1 | **GO WITH NOTES** | 0 | 0 | 1 | 5 | none |
| #1814 @ 277e5ba6 | **GO WITH NOTES** | 0 | 0 | 2 | 5 | none |

---

## #1813 (KS-1822): FOUND

| id | sev | finding | instrument / line | evidence class | action |
|---|---|---|---|---|---|
| 1813-1 | **minor** | **Refusal vs absence differs in DB work (timing class).** For an `anchor_` id that is absent, the route runs one `SELECT`. For one that is present and foreign, it runs the same `SELECT` plus `readIdOwners` (one transaction: `set_config` and a `documents` SELECT). An allowed same-tenant read also runs the probe, so a refused read costs the same as an allowed one, not the same as an absent one. In principle a caller who times many requests can tell "exists in another tenant" from "absent". Status, body and headers do not leak (1813-6). KS-1822 claims byte-identity, which holds; it does not claim timing-class parity, and its gaps i-vi do not name this. | `anchorReadGate.ts:102-110` (`readIdOwners`), `index.ts:936`. Cell **A4**: probes refused=1, absent=0, allowed=1. | MEASURED (probe count, in-process); latency NOT measured | follow-up: name it as gap vii in the PR body/ticket, or file it. A fix shape (e.g. a constant-cost probe on the absent path) is the owner's call. |
| 1813-2 | info | **Cross-PR interaction with #1814 (admin re-anchor of another tenant's document).** #1814 admits a platform admin to re-anchor any document. Its poller (`pollAnchorUntilConfirmed`, then `fetchAnchorState`) reads `GET /api/anchors/:id` with the admin's own bearer. If that token carries the admin's own tenant, #1813 answers 404. The poller treats that as "no data" (`if (!anchor) continue`), so the document never records confirmation. This is the shape of declared gap vi. With a tenantless admin token (gap ii), both PRs allow it. Also, anchoring's KS-1603 write gate (develop) would already refuse the write itself for an admin token with a foreign tenant, so this path probably never reaches the poll. | `anchorStateSync.ts:116-139, 253`; `documents.ts:1590-1597` (#1814); A8 (admin with tenant claim: 404) | READ ONLY (the poll path); A8 MEASURED | none; one line in the KS-1822 gaps would help |
| 1813-3 | info | **Mutant M12 survives:** `absentAnchorBody` with a case-insensitive `anchor_` check stays 12/12 green. No cell pins the absent body for an id spelled `ANCHOR_...`. It is near-equivalent on real data: anchor ids are minted lower-case, and A2 shows an upper-case prefix never reaches a row. | `anchorReadGate.ts:140`; `mut1813.out` M12 | MEASURED | optional cell |
| 1813-4 | info | **Branch is 7 commits behind develop** (merge-base `5a5c4d2b`). `git diff --name-only 5a5c4d2b origin/develop -- services/anchoring` is empty, and merge-tree against develop is clean. The seat's base figures are against `5a5c4d2b` (its docs say so). | `evidence/git_checks.out` | MEASURED | none |
| 1813-5 | info | **Docs section-number collision.** #1813 and #1814 both add `<h2>113.` to `API_Security_Functional_Testing_Architecture_Flow_Diagrams.html`, and both conflict at end of file in the cheat sheet too. The second to merge needs a renumber to 114, and a refresh of quoted figures if it cites suite totals. | grep of both heads; merge-tree A/B | MEASURED | docs re-prep of the second PR |
| 1813-6 | info | **Seat claims reproduce:** 7 of 12 red at base; 12 of 12 at head; suite 36 files / 509 with 1 failure; byte-identity; no RLS on `anchor_store`. Details under TESTED. My 12 mutants are not the seat's 17. I did not re-run the seat's 17 or its integration cell (both "not verified", not "false"). | `spark_1813.out`, `mut1813.out`, `full_anchoring_wt-1813.json` | MEASURED (and READ ONLY for RLS) | none |

### #1813 TESTED (HOW, with the FAIL condition each carried)

- **Code read, every changed line**, plus the paths around it:
  - `dbGetAnchorById`: exact `id = $1`.
  - `dbGetAnchorsByDocument`: exact `document_id`.
  - `readIdOwners`: `external_id` exact first, then the primary key lower-cased, read across tenants under `tenant_scope_bypass`.
  - `mayWriteAnchorRows`, the twin gate on the write side.
  - The shared `authenticate()`: `req.user` is the decoded JWT, and auth mints `tenantId` conditionally. **The read gate reads the same field the write gate reads (`index.ts:777`), so a claim-name drift cannot make one gate allow-all while the other works.**
- **The `:id` handler's two absent literals:**
  - an `anchor_` id gets `'Anchor not found'`;
  - any other id gets `'No anchor found for this document'` with the id echoed (and so do the `non-existent`/`missing` test patterns).
  - `absentAnchorBody` restates both, keyed on the request id, so a row found by a non-prefixed id, whether through the fallback or as a legacy id (A3), refuses with the same answer that id gets when absent.
- **Spark gate:** BASE 5/7 → HEAD 12/0.
- **Red-proof (mine):**
  - I replaced `index.ts` with its `5a5c4d2b` version (asserted to contain no `mayReadAnchorRows`).
  - New file: **5 pass / 7 fail**; red = R1, R2, R3, R7, R8, R9, R11, exactly the seven the file header names.
  - Whole suite on that base: **509 tests, 501 pass / 8 fail** = those 7 plus `threadTokenMint ... deterministic per-seed policyId`, which therefore fails at base too.
  - Restored; sha256 read back equal (`703ed346...`).
- **Whole anchoring suite at head:** **509 tests, 36 files, 508 pass, 1 fail, 0 skipped.** The one failure is the pre-existing `threadTokenMint` cell (also red at base, above), so there are 0 new reds. This matches the seat's 36 / 509. FAIL condition: any red other than that cell.
- **Mutants (mine, each planted alone as an exact-once replace, restored, sha256 equal):** M1 to M11 killed, M12 survives (1813-3). Each mutant, with the cells it turned red:

  | mutant | change planted | red cells |
  |---|---|---|
  | M1 | `:id` gate removed | 6 |
  | M2 | `/document` gate removed | R3, R9 |
  | M3 | 403 instead of 404 | 4 |
  | M4 | always the `anchor_` body | R2 |
  | M5 | `/document` echoes the id | R3 |
  | M6 | compares `organizationId` | R4, R5, R10, R11 |
  | M7 | case-sensitive uuid compare | R10 |
  | M8 | probe fault fails closed | R8 |
  | M9 | tenantless refused | R7 |
  | M10 | refusal log dropped | R9 |
  | M11 | empty-read short-circuit removed | R12 |

  M8 and M9 show that residuals ii and iii are pinned as deliberate.
- **Attack cells** (scratch file built on the PR's own harness: real app, real RS256, DB boundary mocked; **8 of 8 pass**, `attacks_1813.out`):

  | cell | attack | FAIL condition | result |
  |---|---|---|---|
  | A1 | a foreign row stored under the owner document's primary key in UPPER case, via the anchor id, via the `:id` fallback and via `/document` | a 200, or any byte difference from absent | 404 on all three, byte-identical to absent |
  | A2 | `ANCHOR_` upper case, `%20` before/after, upper-case external id, `%20` on `/document`, trailing slash | a 200 or the tx hash in the body | neither appeared |
  | A3 | a legacy non-prefixed anchor id whose row is foreign | refusal differs from absent for that id | identical |
  | A4 | work class (1813-1) | (measurement) | probes refused 1, absent 0, allowed 1 |
  | A5 | legitimate same-tenant readers: connector, ISSUER_ADMIN, OWNER roles with tenant A | refused, or body changed | 200 with the unchanged body |
  | A6 | a token with only a snake-case `tenant_id` | (measurement) | treated as tenantless and allowed (gap ii shape) |
  | A7 | tenant claim with surrounding whitespace | own refused, or foreign allowed | own 200, foreign 404 |
  | A8 | a SYSTEM_ADMIN token carrying its own tenant claim | foreign allowed | 404 (gap vi shape) |
- **The seat's "anchor_store has no RLS":** a static read of `migrations/*.sql`. As a positive control, 17 files enable row-level security somewhere. 0 lines put RLS or a policy on `anchor_store`, and it has no tenant column. This agrees with the seat's schema read; no database was queried.
- **Linear KS-1822:** read; its ticket claim, fix description and gaps match the diff and the in-code gap list i-vi.

## #1814 (KS-1814 + KS-1829): FOUND

| id | sev | finding | instrument / line | evidence class | action |
|---|---|---|---|---|---|
| 1814-1 | **minor** | **A revoked document can still be written back to anchored, by a chain through a sibling route.** `POST /:id/sign` (`documents.ts:1273-1346`) does not check revoked status and writes `{ signatures, status: 'signed' }` with no `preserveTerminalStatuses` (`:1327`). So the chain is: revoke, then sign/request + sign (any same-tenant user, mock signature accepted), giving status `signed`. Then `POST /:id/anchor` by the owner or admin passes step 3 (`signed` is not terminal) and the KS-520 guard (blob absent or `anchor_failed`), and ends `anchored`. #1814's own refusal is correct for the state it reads; the un-revoke is the sibling's pre-existing defect, **already filed as KS-1831** ("can turn a revoked document into signed", Backlog), which the PR names. | `documents.ts:1327-1330`, `:1497-1500`; KS-1831 text | READ ONLY (chain not executed) | follow-up: KS-1831 should name this chain, because its fix (a terminal-status refusal plus `preserveTerminalStatuses` on sign) is what closes KS-1814's "revoked must not be anchored" end to end |
| 1814-2 | **minor** | **The 202 body misreports a revoke that landed mid-flight.** The guarded write keeps `revoked` in the row (KS-521 CASE), but the handler always answers `status: 'anchored'` and does not read back what `updateDocument` returned. | `documents.ts:1613`; cell **B6** (mock returns a revoked record; body `status` is still `anchored`) | MEASURED (handler, mocked repo) | follow-up: answer from the returned record, or say "row status not updated". Not a data-integrity defect; the row is right. |
| 1814-3 | info | **OWNER role is exactly the card default (`secuura-ks1814-owner-role-reanchor-1030`) and nothing wider.** Step 1 admits OWNER only through `documents:write` (Q4b: without the scope, 403 before the read). Step 2's only arm OWNER can satisfy is `owner.id === userId`: the admin literals exclude it, and the connector arm needs `role === 'connector'`. **Behaviour change Kam should see:** an ISSUER_ADMIN or ORG_ADMIN who is not the owner, in the same tenant, is now refused (Q2, Q3); before, any same-tenant user passed. The PR says so; it is a narrowing, not a widening. | `documents.ts:1445-1453`; cells Q4/Q4b/Q5 and **B3** (own 202; foreign with `documents:*` 404; ownerless 404; foreign with a provenance row 404) | MEASURED | Kam's card decides; code = default |
| 1814-4 | info | **Admin spellings match the repo's other predicates.** The three literals `system_admin`, `SYSTEM_ADMIN`, `super_admin` are identical to `callerMayCertifyDocument` (`certifications.ts:123`) and `GET /:id` (`documents.ts:1102`). Upper-case `SUPER_ADMIN` passes step 1 (`isAllowedByRoleOrScope` upper-cases), then is not an admin at step 2 (Q12, 404). The certifications READ uses `isPlatformRole`, which does admit `SUPER_ADMIN`, so the repo has two admin rules; #1814 follows the documents/certify one. Upper-case `CONNECTOR` is not the connector arm (B4a, 404). | grep; Q6-Q8, Q12, B4a | MEASURED | none (pre-existing repo inconsistency) |
| 1814-5 | info | **Owner compare is strict `===`** (case-sensitive), as certify. A hex owner id differing only in case is refused (B5b). | `documents.ts:1451`; B5b | MEASURED | none |
| 1814-6 | info | **The provenance arm fails closed, but there is a creation race (pre-existing pattern).** `wasCreatedByConnector` catches and returns false, so the result is a 404 before the fee. A throwing probe in my mock gave 500, still with no anchoring call and no write (B1). `recordConnectorProvenance` is fire-and-forget (`documents.ts:156-169`), so a connector that re-anchors within milliseconds of create could be cloaked 404 until the row lands. The same holds for certify. The /version child's row is keyed on `newExternalId` (`:2447`), and `document.id` resolves to `external_id` (`documentRepo.ts:168`), so they match (P4). | B1; source | MEASURED (B1) / READ ONLY (race) | none |
| 1814-7 | info | **Seat claims reproduce; KS-1829 and the manifest line are clean.** Covers the base/head ratios, the full suite, the mutants (including one invalid), the comment-only check, the merge commit and the hermetic manifest. Details under TESTED. | `mut1814.out`, `git_checks.out`, `merge_commit_cc.out` | MEASURED | none |

### #1814 TESTED (HOW, with the FAIL condition each carried)

- **Code read, the whole handler at head**, in order:
  1. 401 without a user.
  2. **Step 1** role-or-scope (403), before `getDocument`.
  3. 404 for absent.
  4. **Step 2** `callerMayAnchorDocument` (404 cloak).
  5. **Step 3** revoked/deleted (400).
  6. The KS-520 already-anchored guard (400).
  7. **Only then** `fetch(${anchoringBase}/api/anchors)`.
  8. Write with `{ preserveTerminalStatuses: true }`.

  `documentRepo.updateDocument`: the guard is in the UPDATE's CASE, so a revoke between the read and the write keeps `revoked` while the blob is still written (KS-521 contract). The revoke handler writes the status only (`:2756`). Other `status: 'anchored'` writers: the create path and pollers pass the guard. `:955` (create, simulated) does not, but it is the create path and out of this PR's scope.
- **Ordering, "no refusal after the fee":** every refusal cell asserts **no anchoring call and no write**: the PR's P3, P5-P9, P11-P13, Q2-Q5, Q9-Q12, plus my B1-B5b and B8b. FAIL: any refusal with an anchoring call. None.
- **Spark gate:** BASE 12/16 → HEAD 28/0.
- **Red-proof (mine):**
  - I replaced `documents.ts` with develop's `d7ddfa1f` version (asserted to contain no `callerMayAnchorDocument`).
  - New file: **12 pass / 16 fail**; red = P1b, P3, P5-P10, Q2, Q3, Q4b, Q5, Q9-Q12. That is the refusal and write-option set the docs name. The 12 green are the allowed callers and the unchanged states.
  - The two edited fixtures (ks520, ks1385) on develop's `documents.ts`: **37/37 pass**, so giving those fixtures an owner did not change what they assert there.
  - Restored; sha256 equal (`e5a8cfc1...`).
- **Whole originate suite at head:** **151 suites, 1846 tests, 1846 pass, 0 fail, 0 pending** (seat: 151 / 1846). FAIL: any red.
- **Mutants (mine, each alone, restored, sha256 equal):** 9 of 10 killed. Each mutant, with the cells it turned red:

  | mutant | change planted | red cells |
  |---|---|---|
  | N1 | `SUPER_ADMIN` added to the admin arm | Q12 |
  | N2 | recipient arm added (certify shape) | Q10 |
  | N3 | connector-role check dropped | Q11 |
  | N4 | `deleted` no longer refused | P9 |
  | N5 | `preserveTerminalStatuses: false` | P10 |
  | N6 | step-1 scope `documents:read` | 8 |
  | N7 | step-2 refusal answers 403 | 8 |
  | N8 | owner arm ignores `userId` | 6 |
  | N10 | step-1 role list emptied (scope only; my label in `mut1814.out` misnames it "SUPER_ADMIN removed") | 16 |
  | N9 | `if (!userId) return false` removed | not compiled |

  N9 failed ts-jest type-checking (`userId` possibly undefined), so it is invalid, not a survivor.
- **Attack cells** (scratch file on the PR's own harness: real `isAllowedByRoleOrScope`/`hasScope`, repo and anchoring mocked). First cut: 5 of 8 pass, and the 3 reds were all my own wrong premises (see Instrument errors). Re-cut: **4 of 4 pass**.

  | cell | attack | FAIL condition | result |
  |---|---|---|---|
  | B1 | the provenance probe throws | an anchoring call or a write | 500 with neither |
  | B2 | revoked + confirmed blob | not refused with the revoked message | 400 "revoked" (step 3 runs before the already-anchored guard) |
  | B3 | OWNER-role matrix (1814-3) | OWNER anchors anything but its own document | own 202; the other three 404 |
  | B4a | upper-case CONNECTOR with a provenance row | admitted | 404 |
  | B4b | connector without `userId` | admitted | 401 |
  | B5b | hex owner id differing only in case | admitted | 404 |
  | B6 | 202 body after a guarded write kept a revoke (1814-2) | (measurement) | body still says `anchored` |
  | B7 | admin re-anchor forwards the caller's own bearer to anchoring | another credential forwarded | the caller's bearer |
  | B8b | scope-only caller with a `userId`, not the owner | admitted | 404 at step 2 |
- **Platform S proof:** P1 (creating connector, ownerless `anchor_failed`, onBehalfOf body: 202), P1b (the lookup is `(DOC_ID, S_KEY)`), P2 (no blob: 202), P4 (/version-minted child: 202), P3/P5 (foreign connector: 404), P6 (no `documents:write`: 403 before the read). All green at head.
- **KS-1829 comment-only:**
  - `git diff -w d398e9e5d^ d398e9e5d` has **0** non-comment +/- lines. Control: the same filter on the product commit `1f590aa23` gives **36**, so the filter can see code.
  - The text now states that `signatureHash` is anchored since PR 1811, which agrees with gate 18's measurement.
- **Merge commit `277e5ba6`** (`git show --cc`): its only combined hunks are in the two docs (the measured-at line rewritten). No code arrives through the merge.
- **ks1293 manifest:** exactly one added SUBJECTS line naming the new file (accepted by Wednesday).
- **Linear KS-1814, KS-1829, KS-1831:** read; the ticket claims match the diff. KS-1831 confirms the sign-route chain is filed.

## Docs (both PRs)

`systemTest/__tests__/support/html_docs_check.mjs`:
- Both `Projects Documents` HTML files at the #1813 head, the #1814 head and develop: **rc 0** each.
- **Planted defect** (a 300-character `<p>` of prose outside any table, inserted before `</body>` in scratchpad copies of all four head files): **rc 1** on all four, with the finding "prose outside a table in <p>". So the instrument can fail.
- Content: the figures in each section match what I measured (12 cells and 7 red, 36/509; 28 cells and 16 red, 151/1846, seven mutants). The only defect is the shared number `113` (1813-5).

## NOT TESTED (Rule 2)

- **No stack and no box:** no running gateway, originate or anchoring; no request against any host; no Docker; no Postgres. So I did not run #1813's integration cell (the seat's "red then green on a disposable Postgres" is **not verified** by me). I did not exercise the real `updateDocument` CASE guard with a racing revoke, the real `wasCreatedByConnector` SQL, or `readIdOwners` against real Postgres (the PR's mocked client re-implements its matching).
- **Latency** of the refused vs absent read (1813-1 counts probes; it does not time them).
- **The sign-route chain (1814-1)** was traced in source, not driven end to end.
- **The seat's own mutant lists** (17 for #1813, 7 for #1814) were not re-run; I ran my own 12 and 10.
- **Not run at all:**
  - the four platform suites (Schemathesis, Akto, Playwright, k6) and the pre-push hook legs;
  - `tsc` and eslint over the changed files;
  - the gateway path for these routes (forwarding was read, proxy.ts:911-914);
  - `GET /api/anchors/thread-state`, `/tx`, `/queue` (declared gap v);
  - KS-1832/1833/1834;
  - Node 24 (host Node is v26.8.1, not an LTS line);
  - the `spark_review.py` LLM half.
- **The PR bodies on GitHub** were not read; I did not use `gh`, to avoid touching the project's `gh` config. I relied on the in-code gap list and the Linear comments, which state the same gaps i-vi.
- **Kam's card `secuura-ks1814-owner-role-reanchor-1030`** itself was not found by my file search (stopped after several minutes, no hits). The "default" I checked against is the one stated in the brief and in the KS-1814 Linear comment.

## Instrument errors (mine)

1. **Spark `FETCH_HEAD` race.** I started the two Spark runs concurrently on one clone, and the #1814 run refused with exit 3 (kept as `spark_1814.try1_fetchhead_race.out`). I verified origin was unchanged and re-ran it alone; the valid run is `spark_1814.out`.
2. **Wrong instrument for the merge commit.** My first combined-diff check used `git diff --cc <commit>`, which compares against the clone's checkout. It printed spurious hunks and a "deleted" test file. I replaced it with `git show --cc` (`merge_commit_cc.out`).
3. **Three wrong premises in my first #1814 attack cut.** B4 and B8 assumed a principal with no `userId` reaches step 2; it gets 401 first, which is an earlier refusal. B5 used an all-digit uuid, which case-folding cannot change. I re-cut them as B4a/B4b/B5b/B8b, and all pass.
4. **Mutant N9 does not compile** (invalid, not a survivor), and **N10's label is wrong** in `mut1814.out`: it emptied the role list rather than removing SUPER_ADMIN.
5. **Hook refusals:** `cd` (re-issued with absolute paths); `git -C $D merge-tree`, whose variable the hook could not resolve (re-issued as `evidence/git_checks.sh`); zsh word-splitting and `==` (re-issued via `bash -c` / `echo ----`).
6. **The Linear key** was read from `!CODING/Secuura/Blockchain/4_Credentials/.env` by a script, as the brief directed (never printed or written). The project's own CLAUDE.md says sessions must never open `.env`; I am flagging the conflict for Wednesday rather than resolving it.

**Housekeeping.**
- **Process IDs:** every process I started was recorded in `evidence/pids.txt`, and all exited on their own. My one stop was my own background card-search task, by its task id. No pkill or killall.
- **Scratch tests** were copied into my worktrees only after the mutant runs ended, then **moved** to `evidence/_quarantine_2026-10-30/`. Copies are in `evidence/scratch_tests/`.
- **Worktrees:** both are `git status`-clean at their heads afterwards.
- **Nothing deleted.**

Artefacts: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-30_gate19-1813-1814/evidence/`.
- Gate runs: `spark_1813.out`, `spark_1814*.out`, `mut1813.py/.out`, `mut1814.py/.out`.
- Suites: `full_anchoring_wt-1813.json/.log`, `full_originate_wt-1814.json/.log`.
- Attacks: `attacks_1813.out`, `attacks_1814*.out`, `scratch_tests/`.
- Git and docs: `git_checks.sh/.out`, `merge_commit_cc.out`, `docs_check.sh/.log`.
- Linear: `linear.py`, `linear.out`, `linear_ks1831.out`.
- Setup: `setup.sh/.log`, `install.sh`, `npmci_*.log`, `shared_build_*.log`, `pids.txt`.

The Spark facts are in the session scratchpad (`spark1813_out/`, `spark1814b_out/`). The work dir `work/` is gitignored.
