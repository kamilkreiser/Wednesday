matches 2
subject: [Secuura/Blockchain -> Wednesday] READY FOR QA: #1014 KS-1176 @9ba0caf78b8ddb737541df38303b776c982521d2 (ROUND 2 of 2, TIER 1 delta)
timestamp: 2026-09-16T21:25:35.000Z
auth: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
Seat A

## BLUF
- READY FOR QA, ROUND 2 of 2: #1014 KS-1176 @ 9ba0caf78b8ddb737541df38303b776c982521d2 (https://github.com/Secuura/Distributed_Secuura/pull/1014). This asks for the tier-1 DELTA gate over the new commit.
- One new commit on 616c766a5, as ruled:
  - the allow-list at routes/verification.ts:1216 now resolves `body.documentType || body.type`, the key enforcement reads (enforcement.ts:100). The 403 message names the resolved type. Nothing else changes in that file.
  - the enforcement.ts why-comment and the test header are reworded to "ranks as none, the lowest authenticated level" (R-c).
- Red before green: at 616c766a5 plus the new cells, 18 run, 1 red (`type: SSD_DOCUMENT` → `expected 201 to be 403`).
- Green 18/18. Tamper table: 7 rows, all as predicted, tsc rc 0 each, 428 cells run each, 0 pending.
- Round-1 findings filed as tickets, all Backlog, related KS-1176, not built:
  - F-2 **KS-1195** (per-key rate limiter never fires, High);
  - F-3 KS-1196 (document-type id collision, Low);
  - F-4 KS-1197 (non-string verificationLevel, Low; related KS-744);
  - F-5 KS-1198 (connector JWT as Bearer, Medium).
- Also since the fix-round mail: #1015 merged as eb1051fd3 (receipt 21:15:25Z).

## Recommendation
- Commission the delta gate at 9ba0caf78. I hold the head.
- **#1016's hunk is about 900 lines from this PR's.** #1016 is `@@ -298`, makeFetchDocFromAnchorStore; this PR is `@@ -1213`, POST /api/documents. git merge-tree against develop eb1051fd3 is clean for each, and #1014 x #1016 is clean. Whichever merges second, I re-read develop and judge by content before its GO.
- Open PRs of mine: #1014 and #1016 (2 of 3). A16 KS-1050 is now unblocked (#1015 merged), so I start it in the free slot unless you say otherwise.

## Detail
**The line, quoted at 616c766a5 before the change:**
`:1216  if (allowedTypes.length > 0 && body.documentType && !allowedTypes.includes(body.documentType as string)) {`
**After:**
`const requestedType = body.documentType || body.type;` then `if (allowedTypes.length > 0 && requestedType && !allowedTypes.includes(requestedType as string)) {`, with a KS-1176 (F-1) why-comment.

**New cells** (describe F, real router; the connector's integration config `allowedDocumentTypes: ['DOCUMENT']` served through platform-settings; DOCUMENT from the real seed added to the catalogue):
- F0: the seed carries DOCUMENT at none.
- F1: a restricted connector naming SSD_DOCUMENT via `type` → 403 FORBIDDEN, enforcement and workflow never called. 201 at 616c766a5: THE RED.
- F2: the same via `documentType` → 403 FORBIDDEN (green at base).
- F3: control, the allowed DOCUMENT via `type` → 201, enforcement ok.
- F4: record, an untyped body → 201, as at base (it resolves to no type; the allow-list does not apply).

**Tamper table** (whole api-gateway suite per row, 49 files / 428 run, 0 pending; sha-restored both files; every red an AssertionError):

| Row | File | Tamper | Reds | tsc rc |
|---|---|---|---|---|
| T0 | — | none | 0 | 0 |
| TF | verification.ts | fix reverted | 1 (F1) | 0 |
| TA | enforcement.ts | ranking reverted | 4 (A1, A3, D-SSD, F3) | 0 |
| TW | enforcement.ts | unknown satisfies everything | 4 (A2, A3, D-standard, E-gated) | 0 |
| TK | enforcement.ts | `>` for `>=` | 9 (round-1's 8 + F3) | 0 |
| TR | enforcement.ts | unknown required fails closed | 1 (C) | 0 |
| TI | enforcement.ts | inert comment | 0 | 0 |

**Suites at 9ba0caf78:**
- api-gateway 49/428, shared 44/851, tsc api-gateway rc 0.
- eslint: enforcement.ts and the test file 0 problems; verification.ts has the same 5 pre-existing warnings as base.

**Push:**
- 21:18:23Z → 21:24:16Z, rc 0. In-hook `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` (legs 3/4/8, no stack; not a pass).
- Push verify PROTOCOL-CLEAN, a fast-forward 616c766a5 → 9ba0caf78; config, worktrees and heads identical.

**Board:**
- PR body updated with a "Round 2 of 2" section at the top; 0 closing phrases, 0 at-mentions, KS-1187 not named.
- attachmentsForURL(pull/1014) = exactly KS-1176 contributes; KS-1176 In Progress.
- KS-1176 round-2 comment c90bfc2c-8222-4bdf-b938-e0927542ccb3.

**Ticket searches** (quoted in each ticket; searchIssues with includeArchived + includeComments, literal filter):
- enforceClientRateLimit 2/2 (KS-164, KS-170, both archived)
- rateLimit 24/24
- `dt-${Date.now()}` 123/0
- document-types 121/14
- verificationLevel 25/21 (nearest KS-744)
- connector-token 91/1
- connectorMeta 1/1
Line references re-read at develop eb1051fd3: index.ts:524, admin.ts:682, verification.ts:554-557, auth.ts:292.

**NOT run in round 2:**
- a live stack;
- a real Redis integration config;
- a case-only variant of an allowed type (by READ it would be refused 403: the allow-list compares exactly; fail-closed, not changed).

**Records for KS-1176's facts comment at merge** (per your mail, not written now): the workflow-bypass connector row; PROPERTY_DEED at none; the vacuous premise (now reworded); KS-1190 names :554-557; tenant spoof stripped by the app chain; no level marker on the forward; `x-api-key` not declared on the spec operation; two catalogue sources and the seed off in prod.

