PR 2204: GO WITH NOTES (at head 25ad80bc8298; tier 1)

Gate 325, tier 1 (Opus), one session, 2026-11-12 about 12:15 to 12:30 AEDT (01:16Z to 01:27Z). I only report findings here. Nothing was fixed, posted, mailed, pushed, merged, or written to Linear, GitHub or the boards.

Where things ran:
- Everything ran in my own clone under `scratch/` in this folder (`scratch/repo`). It is a fresh `git clone --filter=blob:none`, sparse checkout of `/.github/`, `/Blockchain/Dev/`, `/frontend/`, `/Projects Documents/`, `/systemTest/` and the root `CLAUDE.md`.
- The hook refuses write verbs aimed outside WEDNESDAY, so the clone sits in this folder rather than in the session scratchpad. Gates 321 and 323 did the same.
- Root `node_modules` is a symlink to gate 313's `r2` install, used read-only. Its `packages/shared/src` matches mine except for one test file (`diff -rq`). `services/api-gateway/node_modules` is a symlink to the shared checkout's copy, used read-only, as gate 317 did.
- Write verbs (fetch, sparse-checkout, merge-tree, commit-tree, read-tree, hash-object) ran only in my clone, through scripts.
- In the shared Secuura checkout I ran read verbs only. Its `git status` shows three untracked files that were already there; I created none of them.
- Every product or test file I changed was restored, and I confirmed each restore by sha256.
- Machine: Node v26.8.1, macOS arm64.

**Summary.** I found no Major. The change does what the ticket asks:
- Every untyped body shape I could build now meets the catalogue's DOCUMENT entry.
- An empty catalogue still passes everything, exactly as on develop.
- No shape gets past the DOCUMENT check unless it names another type.
- All the READY's numbers reproduce.

There is one Minor, and it is a cross-PR interaction rather than a defect of 2204 alone. Open PR 2157 (KS-1952) adds a 503 for typed creates while Redis is down and deliberately exempts untyped creates, because "an untyped create reads no catalogue". PR 2204 makes that reasoning false. With both merged, an untyped create during a Redis outage skips the DOCUMENT rules again, which is the hole KS-1466 closes. The tests are green on the combination.

The remaining findings are Notes and Info.

## Pins
- **Start (01:16:12Z), matching the commission:**
  - develop 088fa84da10ca62c25dd8b6ea86caaa44b64faae
  - refs/pull/2204/head 25ad80bc8298031c616c63b0419daf6fb24f11f5
  - refs/pull/2059/head 5d8969b36a24914c24bc6a839f819ec8be3772e9
  - refs/pull/2095/head 90e8ee1d8f93
- **End (01:26:56Z):** 2204, 2059 and 2095 are unchanged.
- **develop MOVED to 1247e1af3c203d369d01b4d574de377adeec4b98.**
  - The move is one commit, KS-1728: 13 files, all shell tests under `Blockchain/Dev/scripts/__tests__` plus its fragment pair.
  - It shares 0 paths with 2204 (`comm` of the two name lists).
  - `merge-tree` of the new develop with 2204: rc 0, tree 0db721ba28e4.
- **2204 is ONE commit on 088fa84da10c.** 7 files, +172 -12. `merge-tree` of develop 088fa84 with 2204 gives tree 960c7dea6f3b, which is 2204's own tree, so the branch is current with its base.
- **PR state (GraphQL):**
  - OPEN, not draft, base develop, head equals the pin, 1 commit, 7 files, +172 -12.
  - closingIssuesReferences 0. Closing-word regex hits: 0 on the title, 0 on the body, 0 on the commit message; the planted `Fixes KS-1466` hits 1.
  - mergeable UNKNOWN. statusCheckRollup FAILURE, which I did not examine (see G323-BOTH-2 for this repo's CI).
  - The single PR comment is the `linear` bot's linkback, not the seat's.

## Q1. The change, read whole at the head (enforcement.ts 97-200)
The one product edit is at line 119:

`const typeRef = ((typeRefRaw || '') as string) || DEFAULT_DOCUMENT_TYPE;`

It replaces develop's `if (!typeRef) return { ok: true, docType: {} }` (develop 115-118).

Order of checks:
1. Lines 101-114, the non-string guard, run first and are unchanged. Any truthy non-string is still `400 VALIDATION_ERROR` with no catalogue read.
2. Every remaining untyped value (`''`, absent, and the falsy non-strings `null`, `0`, `false`, `NaN`) reaches `resolveDocumentType('DOCUMENT')`.
3. From there the untyped body follows exactly the code path of a body that names `DOCUMENT`:
   - `isActive` (141)
   - no-user creator level (145-150)
   - user creator level (152-160)
   - `requireMFA` (162)
   - `allowedAuthProviders` (168)
   - `metadataSchema` (181)
   - then, back in the route, `createWorkflowInstanceIfRequired`, which handles `requiresApproval` and `approvalWorkflowId`.
4. If the catalogue has no DOCUMENT entry, line 129 reads it again:
   - **empty catalogue:** the KS-388 pass-through `{ ok: true, docType: {} }`, unchanged;
   - **non-empty catalogue:** `400 UNKNOWN_DOCUMENT_TYPE`, with the message `Unknown document type "DOCUMENT"`.

**Measured.** Instrument: `scratch/gate325-probe.test.ts`, kept as `scratch/out/zzprobe-gate325.test.ts.ran`. Output: `scratch/out/probe_{dev,head}.tsv` and the rendered table `scratch/out/probe_table.txt`.
- The probe runs the REAL function with Redis mocked: 32 body shapes x 3 catalogues = 96 cells per tree, run once on develop's bytes and once on the head's.
- The three catalogues:
  - `strictDOC`: SSD_DOCUMENT friction-free, plus DOCUMENT with creator level standard and requireMFA.
  - `noDOC`: SSD_DOCUMENT only.
  - `empty`: no entries.
- Results:
  - **`empty`:** all 32 rows are byte-identical between develop and head (the pass-through is unchanged).
  - **`strictDOC` and `noDOC`:** every untyped shape moves from `ok docType={}` to `403 INSUFFICIENT_VERIFICATION_LEVEL` or `400 UNKNOWN_DOCUMENT_TYPE` respectively.
  - **Every typed or non-string row** is identical between develop and head.

**One mutant per rule.** Driver `scratch/mut.py`, results in `scratch/out/mutants.json`. Each mutant was run against the three enforcement suites (41 cells). All were killed, and in every case at least one ks1466 cell went red:

| mutant | result |
|---|---|
| R1 isActive dropped | 2 red |
| R2a no-user creator branch admits | 1 red |
| R2b user level never compared | 2 red |
| R3 requireMFA dropped | 2 red |
| R4 allowedAuthProviders dropped | 1 red |
| R5 metadataSchema dropped | 2 red |
| R6 requiresApproval ignored | 2 red |

R2a is pinned by the new suite alone. It is not reachable on the route, because `POST /api/documents` is `authenticateToken(true)` (verification.ts:739).

**The seed.** `routes/admin.ts` dt-seed-8 is DOCUMENT with:
- creator level none, requireMFA false
- allowedAuthProviders [], metadataSchema []
- requiresApproval false, approvalWorkflowId null.

So it admits everything. The probe's control row `documentType "DOCUMENT"` behaves exactly like the untyped rows on every catalogue.

## Q2. Bypasses (all measured: function-level probe, head column)
| shape | strictDOC | noDOC | empty | verdict |
|---|---|---|---|---|
| `{}`, `documentType ''`, `type ''` | 403 INSUFFICIENT | 400 UNKNOWN "DOCUMENT" | ok {} | checked as DOCUMENT |
| `documentType` null / undefined / 0 / false / NaN, `type 0` | 403 | 400 | ok {} | checked as DOCUMENT (see G325-2204-5) |
| `documentType` 123 / [] / ["DOCUMENT"] / {} / true, `type ["SSD_DOCUMENT"]` | 400 VALIDATION_ERROR, 0 reads | same | same | unchanged (KS-501) |
| `documentType` " " / "\t\n" / "DOCUMENT " | 400 UNKNOWN | 400 UNKNOWN | ok {} | unknown type, not a bypass (unchanged) |
| `documentType` "document" / "DoCuMeNt" / "dt-seed-8" (the id) | 403 (DOCUMENT rules) | 400 | ok {} | case and id resolve to DOCUMENT (unchanged) |
| `DocumentType`, `document_type`, `data.documentType`, JSON own `__proto__` {type} / {documentType} | 403 | 400 naming "DOCUMENT" | ok {} | not read as a type; checked as DOCUMENT (KS-1203 point holds) |
| `documentType "" + type "SSD_DOCUMENT"`, `null + type "SSD_DOCUMENT"` | ok SSD_DOCUMENT | ok SSD_DOCUMENT | ok {} | names SSD via `type`; originate stores SSD (same precedence) |
| `documentType "SSD_DOCUMENT" + type "DOCUMENT"` | ok SSD_DOCUMENT | ok SSD | ok {} | documentType wins at both enforcement and originate:607 |
| `documentType "DOCUMENT" + type "SSD_DOCUMENT"` | 403 | 400 | ok {} | documentType wins |

**No shape escapes the DOCUMENT rules unless it names another type.** Naming another type is by design: that type's own entry applies, and the connector allow-list (verification.ts:915) restricts it.

The type that is checked and the type that is stored agree:
- the gateway uses `body.documentType || body.type || DEFAULT_DOCUMENT_TYPE`;
- originate uses `documentType || rawType || DEFAULT_DOCUMENT_TYPE` (documents.ts:607);
- the workflow gate uses the same expression (enforcement.ts:265).

Bypass mutants:
- **B1** (a wrong-case `DocumentType` read as a type): killed, 1 red (the rewritten ks501 KS-1203 cell).
- **B2** (nested `data.documentType` read as a type): killed, 1 red (the rewritten ks501 nested cell).
- **B3** (`type` wins over `documentType`): killed, 1 red (ks1204).
- **B4** (whitespace trimmed to untyped): **survives**. See G325-2204-7; it is not a bypass, since both behaviours meet a check.

## Q3. Other callers and the tests the change could disarm
Callers at the head. I grepped the whole sparse tree (Blockchain + frontend, no node_modules). These are every reference outside the tests:

| site | what it is | behaviour change |
|---|---|---|
| verification.ts:923 `enforceDocumentTypeRules(body, req.user)` (POST /api/documents) | the only runtime caller | YES, and only for untyped bodies on a non-empty catalogue: DOCUMENT's rules apply, or 400 if there is no DOCUMENT entry. Empty catalogue: unchanged. |
| verification.ts:960 `createWorkflowInstanceIfRequired(enforcement.docType, ...)` | workflow gate | It is now reached with the DOCUMENT entry for an untyped body. If that entry requires approval, the body is held `pending_approval` and the response type is `DOCUMENT` (enforcement.ts:265; the code is unchanged, the path is newly reached). |
| verification.ts:915 allow-list `requestedType` | connector allow-list | Code unchanged. It runs BEFORE enforcement. Mutant A1 (default dropped) is still killed at the head by 8 ks1203 cells. |
| originate routes/documents.ts:607 | stored type | Unchanged. It agrees with the checked type. |
| enforcement.ts:121 `resolveDocumentType` | the only caller of the resolver | n/a |
| index.ts:940 | dependency wiring only | no |
| admin.ts:317 | comment only | no |
| platform.ts:989 | maps a DB column `creator_verification_level` | no; it is not an enforcement path |

`UNKNOWN_DOCUMENT_TYPE`, `DOC_TYPE_DISABLED` and `creatorVerificationLevel` appear in no other server-side enforcement.

**Existing cells.** 25 api-gateway test files reference the module.
- **9 files stub the function** through dependency injection: ks1087, ks1185 x3, ks1543, ks1628, ks1771, ks466, ks815. A stub is unaffected by the change.
- **7 route suites run the REAL function:** ks1176, ks1203, ks1204, ks1231, ks1256-unreadable, ks1539, ks1871.
- Their negative-asserting cells pin the exact status, code and message plus the enforcement-spy count. Examples:
  - ks1203:184 `[403, FORBIDDEN, 'Connector is not permitted ... "DOCUMENT"', 0, 0]`
  - ks1204:231
  - ks1231:167, `[403,'FORBIDDEN',0]` for the typed and the untyped create
  - ks1256 `[503,'SERVICE_UNAVAILABLE',0]`
- A new DOCUMENT 400 or 403 from enforcement therefore cannot satisfy any of them. The A1 mutant confirms the KS-1203 negatives still reach the allow-list they are named for.
- The whole suite is green at the head (Q4).

**The four rewritten cells.** I took develop's two test files and ran them against the head's code: 4 failed | 26 passed (30), and those 4 are exactly the rewritten cells.

1. **enforcement.test.ts:147.** Old: "returns ok:true with empty docType when no typeRef is provided", with no catalogue set. New: the same name plus "and the catalogue is EMPTY", queueing two empty reads.
   - It still pins a real property, the KS-388 pass-through for an untyped body.
   - It is green on BOTH trees, so it does not discriminate the change. That is fine: ks1466's EMPTY cell and mutant Y4 cover it.
   - Its queued `mockResolvedValueOnce` values leak on develop's code: G325-2204-2.
2. **ks501 "absent/empty documentType".** Old: `ok === true`. New: `[false, 'UNKNOWN_DOCUMENT_TYPE']` against a DEGREE-only catalogue.
   - It still tests the KS-501 property. An empty value is NOT the non-string `VALIDATION_ERROR`, and a mutant that made it so would turn the code red.
   - It is now also a red-first cell for KS-1466 (Y1, Y2 and Y3 kill it).
3. **ks501 KS-1203 shapes.** Old: `[true, {}]` and the catalogue never read. New: `[false, 400, UNKNOWN, error includes '"DOCUMENT"']` and two reads per body.
   - **Still a security test.** If a wrong-case key were read, the error would name `"SSD_DOCUMENT"`, and `"SSD_DOCUMENT"` does not contain the substring `"DOCUMENT"` with its leading quote.
   - Measured: B1 is killed by exactly this cell.
4. **ks501 nested data.documentType.** Old: `[true, {}, 0]`. New: `[false, UNKNOWN, '"DOCUMENT"', 2]`.
   - **Still a security test.** If the nested DEGREE were read, the result would be ok:true with DEGREE.
   - Measured: B2 is killed by exactly this cell.

Each rewritten cell carries a comment quoting the old assertion, as the READY says.

## Q4. Red then green, the whole suite, the five mutants (measured)
**New suite on develop's enforcement.ts** (head tests, product file swapped and then restored by sha256): **9 failed | 2 passed (11)**, all failures by assertion.
- The 2 green cells are the constant cell and the typed control.
- The EMPTY-catalogue cell is red only on its read count: `expected +0 to be 2`. See G325-2204-4.

**At the head:** the three enforcement suites give **41 of 41**. **Typecheck:** `tsc --noEmit -p services/api-gateway/tsconfig.json` gives rc 0 and 0 errors. Positive control: planting `DEFAULT_DOCUMENT_TYPEX` gives rc 2, 1 error at enforcement.ts(119,53).

**Whole api-gateway vitest** (raw logs `scratch/out/t_whole_*.log`; all three Spark digests CHECKED, and I read only their `digest.md` plus the raw count lines):

| run | result |
|---|---|
| head | **1,897 of 1,897, 169 files**, digest CHECKED PASS. This equals the READY. |
| pristine develop (develop's code and develop's test files) plus the new suite | **9 failed / 1,888 passed (1,897)**, 1 file failed, digest CHECKED. This is the READY's "develop's code 1,888 of 1,897". |
| develop's code under the HEAD's test files | **15 failed / 1,882 passed**: the 9 new cells, the 3 rewritten ks501 cells, and 3 enforcement.test.ts cells (G325-2204-2). Digest CHECKED; every failure name was re-derived by the parser. See G325-2204-3. |
| head code with develop's two old test files (the READY's "the fix alone") | 4 failed in those two files, which matches its 1,893 of 1,897. |

**The READY's five mutants**, reproduced with the same 41 cells and restored by sha256 each time:

| mutant | red cells (gate) | READY |
|---|---|---|
| drop the default | 11 | 11 |
| a wrong default (`'SSD_DOCUMENT'`) | 10 | 10 |
| the old early return back | 15 | 15 |
| the empty-catalogue branch refusing | 3 | 3 |
| the workflow-gate default dropped (line 265) | 1 | 1 |

**5 of 5 killed. Every count equals the READY.**

## Q5. The operator note and the fragment pair
`MCP Deployment/troubleshooting.md`, the new entry under Document Registration Issues. Its claims against the head:
- **"an empty one, which checks nothing":** TRUE. The probe's `empty` rows are identical on develop and head.
- **"one written by the current seed, whose DOCUMENT entry asks for nothing":** TRUE. I read dt-seed-8 (above).
- **"a hand-built catalogue without DOCUMENT: every untyped registration is refused 400 UNKNOWN_DOCUMENT_TYPE":** TRUE. Measured: `noDOC`, all 11 untyped shapes.
- **Disabled DOCUMENT gives 403 `DOC_TYPE_DISABLED`:** TRUE (ks1466 cell plus mutant R1).
- **"the same 401, 403 or 400":** a slight over-statement. See G325-2204-5.

**Fragments.**
- `node Blockchain/Dev/scripts/docs-fragments.mjs check --root <clone>` at the head: rc 0, `OK`, `flow 117 legacy + 233 new, cheat 112 legacy + 233 new; lint clean, render passes html_docs_check`. There are 2 ADVISORY lines (the committed pages lag their fragments). That equals the READY.
- The first attempt refused with rc 2 because `systemTest/` was outside my sparse checkout. After I added it, the result was as above.
- **Planted defect** (a second `<h2>` appended to the flow fragment): rc 1, `FAIL — 1 finding(s)`, "must hold exactly one entry (one <h2>)". Restored by sha256, then rc 0 OK again.
- **Read-tool line-number prefixes in either fragment:** 0 (grep `^\s*[0-9]+→|^\s*[0-9]+\t`). Positive control: a planted `   12\t<h2>` line counts 1.

## Q6. The PR 2059 condition
Driver `scratch/mt.sh` plus `scratch/survival.py`; files in `scratch/mt/`. 2059's head was re-read at the end: 5d8969b36a24, unchanged.
- **Base:** 2059 is cut on c5c26b2835df, not on develop. merge-tree uses git's own merge-base (c5c26b2835df for both 2059 x develop and 2059 x 2204). I did not use merge-file with a chosen base.
- **(1)** `git merge-tree --write-tree p2204 p2059`: **rc 0, tree 346f856b2ada**, which equals the READY.
- **(2) Whole-line survival on troubleshooting.md.** For every distinct line a side adds or removes against ITS OWN base, I compared that line's count in the merged file with its count in that side's file:
  - 2204 added 4 distinct lines (6 with blanks): 0 mismatches.
  - 2059 added 4: 0 mismatches.
  - 2059 removed 8 distinct lines (9 lines): 0 mismatches. 2 of them still occur in the merged file, at exactly the count 2059's own file has (repeated lines).
  - **SURVIVAL PASS.**
  - Numstat 2059 to merged: `6 0`. 2204 to merged: `4 9`. 2059's own diff: `4 9`. All equal the READY.
  - **Control:** dropping one 2204 line from the merged file makes the checker report a mismatch (1). The instrument can fail.
- **(3) Planted conflict:** a scratch commit on 2204 that edits a line 2059 removes (`curl -X POST http://localhost:7890/hash \`) gives `merge-tree` rc 1 and 1 `CONFLICT`. It fires.

## Q7. Census
`scratch/census_gql.py` pages every PR's files up to totalCount and asserts the count. **100 open PRs, 442 file rows.**

| path | open PRs |
|---|---|
| troubleshooting.md | [2059, 2204] (2059 waived; condition re-measured in Q6) |
| enforcement.ts | [2204] |
| enforcement.test.ts | [2204] |
| ks1466 test | [2204] |
| ks501 test | [2204] |
| flow fragment | [2204] |
| cheat fragment | [2204] |

- **Control:** PR 2125's `api-gateway/src/index.ts` maps to [2125], so it **FIRED**.
- **Negative control:** an absent path maps to [].
- **Neighbourhood** (different files, the same mechanism). Each one's merge-tree with 2204 is rc 0:
  - **2157** (verification.ts + ks466 test, KS-1952): **semantically coupled**, see G325-2204-1.
  - 2161 (originate documents.ts, KS-1991 registry): no type logic changed.
  - 2159 (admin.ts, KS-2111 settings `__proto__`): does not touch the seed.
  - 2185 (redis.ts, KS-2011 notification-settings TTL): not the doctype reads.
  - 2145 (ks1539 test, +11 lines): typed SSD bodies only.
  - 2095 (ks1185-f2-f3, which stubs the function): unaffected.
  - `packages/shared/.../defaultDocumentType.ts`: [].

## Q8. The two candidate filings
- **(a) Both boxes' catalogues are EMPTY, so KS-388 validation is OFF on kintsugi and demo.** This is the seat's measurement (Redis AUTH/KEYS/GET, 00:36:54Z and 00:37:34Z). **I did not reproduce it: no box access.**
  - What the code says: if true, then on both boxes every documentType passes and KS-1466 changes nothing today, which is the reason BUILD was safe.
  - The PR body adds a useful fact: `GET /api/admin/document-types` seeds an empty catalogue. So the first admin to open the Document Types page turns validation ON, with the friction-free seed.
- **(b) TRUE at develop.** `frontend/outlook-addin/src/utils/api.ts:118` reads `documentType: metadata.contentType || 'application/octet-stream'`. The blob 35c5e444 is identical on develop and head. The caller is `taskpane/CertifyPanel.tsx:113`, `contentType: attachment.contentType`.
  - The value is always a truthy MIME string, so the add-in never sends an untyped create and **2204 does not change its behaviour**.
  - On any box with a non-empty catalogue it is a 400 `UNKNOWN_DOCUMENT_TYPE` today, by reading the code (no catalogue code is a MIME type). I did not run it.
  - Small extra observation: it also sends `hash`, not `contentHash`.

## Findings
- **G325-2204-1 (Minor, cross-PR, for Wednesday to route; not a defect of 2204 alone): PR 2157 (KS-1952) and PR 2204 together reopen the untyped hole during a Redis outage.**
  - What 2157 does: it adds, before enforcement, `if ((body.documentType || body.type) && !redisService.isRedisAvailable()) → 503`. Its comment says "an untyped create reads no catalogue and still goes on to enforcement", and its control **C2 pins "Redis down, UNTYPED create: unchanged, reaches enforcement and is created"** (with a spy for enforcement).
  - What changes with 2204: an untyped create DOES read the catalogue, as DOCUMENT. While Redis is down, `getAllDocumentTypes` returns the in-memory `documentTypesStore` (redis.ts:558). KS-1952's premise is that this store reads empty, so it passes everything.
  - The merged result: a typed create gets 503, but an untyped one skips the DOCUMENT rules, which is the exact class 2204 closes. In KS-1952's terms, the outage window keeps the gap for exactly the body 2204 fixes.
  - Measured on the merged tree 686496cd479a (2204 x 2157, rc 0): 2157's ks1952 suite, ks466, ks1466, enforcement, ks501 and ks1203 give **70 of 70 green, C2 included**. No test notices.
  - The census cannot see it, because the two PRs share no file.
  - The fix belongs to whichever PR merges second. Apply 2157's 503 to every create while Redis is unavailable (drop the `(body.documentType || body.type) &&` condition), and rewrite its comment and C2. Or Kam rules the untyped case acceptable.
  - Either way, 2157's gate (or the merge seat) needs this sentence. It does not block 2204: on 2204 alone, typed and untyped creates behave the same during an outage, as on develop.
- **G325-2204-2 (Note, test hygiene): the rewritten enforcement.test.ts:147 cell queues `mockResolvedValueOnce([]).mockResolvedValueOnce([])`.**
  - On develop's code the untyped path reads nothing, so the two queued values survive `vi.clearAllMocks()` (which does not drain the Once queue) and leak into the next three cells. Those cells (KS-388 unknown 400, SSD_DOCUMENT accepted, disabled 403) then go red for reasons unrelated to their names.
  - Measured: develop's code under the head's tests gives 3 such reds. Mutant Y3 (the early return back) reports them among its 15.
  - This is not a weakening: Y3 is still killed loudly, and ks1466 pins the empty-catalogue read count. But a future regression would surface as misleading failures.
  - `mockResolvedValue([])` scoped to the cell, or an assertion on the read count, would fix it.
- **G325-2204-3 (Info): the READY's "develop's code 1,888 of 1,897" means pristine develop's test files plus the new suite.** Measured exactly (9 failed, all in ks1466). Under the head's test files, develop's code reads 1,882 of 1,897 (15 failed; see G325-2204-2). Both numbers are honest. Only the wording is ambiguous.
- **G325-2204-4 (Info): one of the "9 red" pins an implementation detail, not behaviour.** The ks1466 EMPTY-catalogue cell is red on develop only through `getAllDocumentTypes` call count 0 vs 2. Its result `{ok:true, docType:{}}` is identical on both trees (probe, `empty` rows). The red-first claim stands: the other 8 reds are behavioural.
- **G325-2204-5 (Note, docs precision; no action needed for GO):**
  - **The 401 claim.** The note says an untyped registration "gets the same 401, 403 or 400 a registration naming DOCUMENT gets". `AUTH_REQUIRED` 401 is reachable only with no user, and the route is `authenticateToken(true)`, so on the route the answer is 403 or 400.
  - **Falsy non-string documentType.** The note covers "no documentType (or an empty one)", but a falsy non-string documentType (`null`, `0`, `false`) is also checked as DOCUMENT at the gateway.
  - Originate then refuses those values 400 "documentType must be a string" (documents.ts, the `typeof documentType !== 'string'` check). The exception is a DOCUMENT entry that requires approval: then the gateway stores a pending document whose body originate will refuse at approval.
  - This is pre-existing in shape (develop passed them with `{}` to the same originate check) and is not a bypass.
- **G325-2204-6 (Info, pre-existing): case and id resolution.**
  - `documentType "document"` (or the id `"dt-seed-8"`) meets DOCUMENT's rules (case-insensitive code, or an exact id), but is stored as the literal string. The connector allow-list's `.includes` is case-sensitive, so a list `['DOCUMENT']` refuses `'document'`.
  - Unchanged by 2204; noted because Q2 asked about case variants.
  - The KS-1203 point, that the error names DOCUMENT, holds: the untyped noDOC error is `Unknown document type "DOCUMENT"`.
- **G325-2204-7 (Info): mutant B4 (whitespace trimmed to untyped) survives.**
  - A whitespace-only documentType is an unknown type: 400 on any non-empty catalogue, pass-through on an empty one, on both trees.
  - No cell distinguishes that from "trim to DOCUMENT". Neither behaviour is a bypass (each meets a check), so this is a design choice left open, not a gap.

## NOT TESTED
- A live create through a running gateway or originate, against real Redis or Postgres. Everything here is function-level or route-level with mocks.
- The Redis-down path in G325-2204-1. I read redis.ts:546-558 and ran 2157's own spy-based cells on the merged tree; I did not run a real Redis outage.
- The box measurements in the READY (catalogue keys, log counts, row counts): no box access.
- Node 24 (everything ran on v26.8.1).
- The typecheck-tests ratchet, eslint, the pre-push hook, the four platform suites, and originate's eight-shape cell (carried by the seat).
- Route-level behaviour of the odd body shapes. The Q2 table is the function. I read the route's body guards (KS-529 non-object, KS-815 control bytes) but did not drive them with these shapes.
- Linear (KS-1466 and its comments). No Spark shadow review was commissioned for this gate, and none was run. The Spark DIGEST was used for the three whole-suite logs.
