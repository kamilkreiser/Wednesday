# Spark screen, part 22 (2026-10-20 14:36-14:47 AEDT): ONE brief, ONE PASS first time (KS-1689 `needsReauth`, a code_patch with a new test file, golden BYTE-IDENTICAL); KS-1672 and the third slot yielded decisions, not briefs

model: claude-sonnet-5-5 -- row C8 (screen + brief drafting) -- Spark screen-22 sub-agent

By a Spark screen-and-brief sub-agent for Wednesday. Secuura only. Nothing held, raised, pushed, merged, committed or deleted; no GitHub or Linear write (Linear read-only); no `hold_ready`; `queue.md` NOT touched; nothing written under `!CODING` (the Secuura `.env` was READ inside a scratch script for the Linear key, never printed or stored; `node_modules` were symlinked into a scratch clone, as in screen 21). No `cd`, no `rm`. Every clock below came from `date`.

## BLUF
- **Brief count: 1 of the 3 commissioned slots.** `ks_1689_p1` (KS-1689, tier `code_patch`, rung 2: one 2-line product insertion in `m365-integration/src/index.ts` + one NEW vitest file of 9 cells). Lint rc 0 with empty stderr; dry-run rc 0, 0 `WARNING`; CONTROL-PASS first; ONE real round: **PASS, golden BYTE-IDENTICAL**, no re-brief needed (counter: original only). 169 s round, 77.8 s model, 39760+2365 tokens.
- **Verdicts:** KS-1689 = BRIEFED, PASS. KS-1672 = NOT briefed: the ticket names the write sites but does not spell out the edit, and the keys do not line up (decision, questions below). Third slot = NOTHING briefable found (KS-1690 and KS-1327 are decisions by their own words; the rest of the 373-ticket census is CI / shell / e2e / measure-first).
- **The rule as built:** `needsReauth: connection.status === 'connected' && !connection.refreshToken,` directly after `tokenExpired` on `GET /api/connections/:id` (develop `index.ts:794`, new lines 795-796). The POST init response (`status: connection.status`) and the health count (`activeConnections`, `status === 'connected'` filter, `:482`) are untouched. No stored status, migration, OpenAPI, UI, or sign-in/refresh/selection change.
- **Needs a Wednesday decision:** (Q1) KS-1672 write-site scope; (Q2) KS-1690 shape (origin-session lookup vs credential epoch) if the Spark is to take it; (Q3) the new field is undocumented in OpenAPI by ruling: file a follow-up? (Q4) `ks_1116_p1` may be superseded by a landed commit (see Things 3). Details under "Questions".

## Pinned sha
`git ls-remote origin refs/heads/develop` (literal path, cache clone): `21e2ffd20795` at 14:36 when the screen began (`Refs KS-1692: a revoke that THROWS maps onto the same post-write 503`); **it MOVED once** to `561a6c5b5282` (`Refs KS-1116: two role-prefix rows and an EXTENDS-tenant row for gate BM1 NOTE 1`) before the brief was written; `git diff --name-only 21e2ffd20795 561a6c5b5282` = `Blockchain/Dev/services/vc-issuer/src/__tests__/ks1116-presentation-and-credential-reads-bound-to-the-creator.test.ts` only, none of this brief's files. The brief says `Tip: 561a6c5b528289f4d7ecd19f9c069501e925e9ea` and states that its files were read at `21e2ffd20795`. Dry-run, control and real round all ran at `561a6c5b5282` (`ls-remote` re-read at 14:40:13 and 14:42:50: unchanged).

## Live-develop confirmation of the commission (read at `21e2ffd20795`, file unchanged at `561a6c5b5282`)
- The status read is `app.get('/api/connections/:id', ...)` at `index.ts:776`; it builds `ownedConnection(req, id)` then `res.json({ success, data: { id, organizationId, tenantId, tenantName, status, scopes, connectedAt, lastSyncAt, tokenExpired } })`; `tokenExpired` is `:794` and the object closes at `:795`. Matches the commission (about 776-797 / :794).
- It is the ONLY status read. The other two places that carry a connection status: `POST /api/connections/init` (`:761-767`, the 201 response with `status: connection.status`, a `pending` row with no token yet) and the health count (`:482`, `filter(c => c.status === 'connected').length`). Neither gets the flag.
- Field shape today: `status` is the stored string, `tokenExpired` a boolean (true when `tokenExpiresAt` is absent). `needsReauth` is a sibling boolean; `M365Connection.refreshToken?: string` (`:96`).
- Undecryptable token: `dbGetConnection` (`:204`) and `loadFromDb` (`:287`) both assign `refreshToken: decryptToken(...)`; `decryptToken` (`security/tokenCrypto.ts`) returns `undefined` for a null/empty value and, via a `try/catch`, for a ciphertext it cannot decrypt (logs an error, fails closed). So the same expression flags it with no extra code.
- DELETE (`:803-823`) sets `status = 'disconnected'`, `accessToken = undefined`, `refreshToken = undefined`: a disconnected connection has no token but its status is not `connected`, so it reads false (cell R4, R7).

## Brief and round (dir `local-model/night/briefs/ks_1689_p1/`, run dirs under `local-model/runs/`)

| item | ticket | tier | files | cells |
|---|---|---|---|---|
| 1 | KS-1689 (Backlog; Kam ruled card `secuura-ks1689-m365-failed-signin-status-1020` = d) | `code_patch`, rung 2 | PRODUCT `Blockchain/Dev/services/m365-integration/src/index.ts` (1 hunk, pure insertion, +2); TEST NEW `Blockchain/Dev/services/m365-integration/src/__tests__/ks1689-the-connection-status-says-when-the-user-must-sign-in-again.test.ts` (148 lines, 9 cells: C0, C1 green at the tip; R1-R7 red at the tip by assertion) | connected+token false (R1), connected+no token true (R2), connected+undecryptable `v1:` token true (R3), disconnected+no token false (R4), error false (R5), pending false (R6), a real DELETE of a connected+token row then read: disconnected, false (R7) |

Tool lines, copied verbatim:
- **lint:** `brief_lint.py` rc 0, stderr empty (`B_TIER=code_patch`, `B_BRIEF_TIP=561a6c5b528289f4d7ecd19f9c069501e925e9ea`, `B_RUNNER=vitest`).
- **dry-run:** `SPARK ROUND ks_1689_p1: DRY-RUN OK — brief accepted, input built at 561a6c5b5282 (126893 B) in .../spark/state/dry/ks_1689_p1_20261020-144032; a real round would call http://127.0.0.1:47788 with code_patch/task.md, thinking OFF` (rc 0, stderr empty, 0 `WARNING`).
- **control:** `SPARK ROUND ks_1689_p1: CONTROL-PASS — PASS (checker rc 0 + A2a anchor OK) · golden BYTE-IDENTICAL · tip 561a6c5b5282 · 123s round, no model (control)`
- **real round:** `SPARK ROUND ks_1689_p1: PASS — PASS (checker rc 0 + A2a anchor OK) · golden BYTE-IDENTICAL · tip 561a6c5b5282 · 169s round, 77.844s model, 39760+2365 tok`
- **golden identity:** BYTE-IDENTICAL for the real round (`cmp` of the model's patch with `golden.diff`), not merely TREE-IDENTICAL.
- **Checker lines (`checker.out`):** `PASS A3 touched-file set == { index.ts , the new test }`; `PASS A3c every '+' line the brief adds is in the product hunk (2 line(s))`; `A3i ... OK 2 line(s) byte-exact incl. leading whitespace`; `PASS A4 RED-FIRST ... fails at the untouched tip (7 failed / 9 run; controls green; assertion reds)`; `PASS A5 GREEN-AFTER ... (9 passed / 9 run)`; `PASS A6 whole services/m365-integration suite: no NEW red vs the untouched tip`; `PASS A7 tsc --noEmit for services/m365-integration: rc 0 after the patch (baseline rc=0)`; `RESULT: PASS (7/7)`; `PASS A2a ANCHOR ... hunks=1 ok=1 bad=0 skipped_newfile=1`.
- **Accommodation check:** `decl_splice.out` = `spliced 0`, `tdz_inline.out` = `inlined 0`, `section_1.opts` names the plain `section_1.diff`. No splice, no inlining, no accommodation was applied to the model's patch. The model did not fail; no re-brief (the counter stands at the original brief only).
- Run dirs: `local-model/runs/spark_secuura_2026-10-20_ks_1689_p1-control` and `.../spark_secuura_2026-10-20_ks_1689_p1`.

By-hand work before the brief was written (scratch clone at `21e2ffd20795`, `node_modules` symlinked): the new test file at the untouched tip 7 failed / 2 passed (R1-R7 `AssertionError: expected undefined to be ...`; C0, C1 green); with the edit 9 passed / 9; `tsc --noEmit` rc 0 baseline and with the edit.

## Design choices (Wednesday's rule): choice / alternative run as a mutant BEFORE the brief / cells that red
Every mutant was applied to `index.ts` in the scratch clone on top of the edit, `tsc --noEmit` run FIRST and compared with the baseline (rc 0, 0 errors), then the one test file run, then the file restored (restore asserted by re-reading). `mut.py` prints `COMPILES` only when tsc rc and error count equal the baseline. All seven compiled.

| mutant (the three the commission asked for first) | tsc | cells that red |
|---|---|---|
| M1 DROP THE STATUS CLAUSE: `needsReauth: !connection.refreshToken,` | COMPILES (rc 0) | R4, R5, R6, R7 (4 of 9) |
| M2 DROP THE TOKEN CLAUSE: `needsReauth: connection.status === 'connected',` | COMPILES (rc 0) | R1, R7 (2 of 9) |
| M3 INVERT THE WHOLE: `!(status === 'connected' && !refreshToken)` | COMPILES (rc 0) | R1-R7 (7 of 9) |
| M4 status `!== 'disconnected'` (a plausible sibling of the rule) | COMPILES | R5, R6 |
| M5 token clause alone inverted: `&& !!connection.refreshToken` | COMPILES | R1, R2, R3, R7 |
| M6 status clause alone inverted: `status !== 'connected' && ...` | COMPILES | R2-R7 |
| M7 the property removed from the object | COMPILES | R1-R7 |

C0 and C1 stay green under every mutant (they pin the seam and the unchanged `status` / `tokenExpired`). The choice to assert exact booleans (`toBe(false)`) rather than falsy is deliberate: it pins that the field is PRESENT on every status, which is why the four "false" cells are red at the tip (declared under `## Red cells`, all seven failed by assertion in the checker's A4).

## Table of every ticket considered

| ticket | source | read | disposition |
|---|---|---|---|
| KS-1689 (m365 failed sign-in still `connected`) | commission 1; Kam's card ruling d | ticket whole + its one comment; `index.ts` at the sites above; `tokenCrypto.ts` whole; the ks1673 harness | **BRIEF `ks_1689_p1`** (PASS, BYTE-IDENTICAL) |
| KS-1672 (auth stores no provider identity) | commission 2 | ticket whole; `routes/auth.ts` and `repositories/userRepo.ts` at the write sites at live develop | **DECISION, not briefed**: the ticket names the three write sites and the `fieldMap` (`userRepo.ts:~801-824`, 20 keys, none social) and `createUser`'s INSERT, but it does NOT spell out the edit: no column list, no key names. See Q1 for the concrete blockers |
| KS-1690 (OAuth `refresh_token` grant ignores the origin session, `oauth.ts:988-1089`) | commission 3 (census, Backlog, fix recommended) | ticket whole + gate BS1 comment | **DECISION**: "Check the origin session on this grant (or introduce a per-user credential epoch)", "Wednesday or Kam should rule whether the fix rides with a KS-1407 follow-up or stands alone"; BS1's two conditions (fail closed on a missing or unknown `sessionId`; the authorization-code sibling at `:969` needs an epoch or code invalidation) widen it. Adjacent to KS-1692's `session.ts` (G). See Q2 |
| KS-1327 (kyc whole-row read-modify-write) | commission 3 | ticket whole | **DECISION**: "Fix shapes, not chosen here" (partial UPDATE, row locking, or move the mock off the request path); a behaviour change to a persistence path that "wants its own gate" |
| KS-1304 (originate `documents.ts` mixes a tenant-pool READ with a default-pool WRITE) | commission 3 (census) | title + head | EXCLUDED: `documents.ts` is in the unchanged exclusion list (G and the KS-1695 plan) |
| KS-1010 (e2e CIP-30 check passes on the 404) | commission 3 (census, "should be" wording) | head | not code-fit: a `systemTest` e2e file, no product file for the tier, no runnable red-first in the checker |
| KS-1609, 955, 987, 188, 1148, 1443, 1423, 1415, 1332, 1320, 1039, 1030, 940, 903, 1400, 1323, 948, 1161, 1042, 1422, 956, 915, 783, 648, 760, 678 | commission 3 (the 22-ticket "has a fix section and no decision wording" cut of the 373-ticket census, plus an 11-ticket "one-line / should read" cut) | titles + head | not code-fit: shell, CI, Akto, docker, launcher, systemTest, advisory bumps, docs, process, or a feature gap; none is an app-service edit with a runnable red |
| Live partitions: m365 token-manager/auth (R's successor), originate `certifications.ts` reads (#1667), `gdprService.ts` and auth session/password routes (KS-758, KS-1692), migration 055 and provenance code (KS-1557), vc-issuer ownership test (D 26th) | the commission | not touched | EXCLUDED by the brief's own list (this brief edits `index.ts` at lines ~794-795 only; R's KS-1687 lives in `token-manager.ts` and the m365 non-test files, a different region) |

**Depth honestly stated:** the 373-ticket census is `scratchpad/s21/census.json` (Linear, read-only, taken for screen 21 earlier today): not re-pulled. Of it, KS-1689, KS-1672, KS-1690 and KS-1327 were read whole; 33 more by title and first lines; the remaining ~335 were not re-read (screens 15-21 covered the auth-shaped and test-only rules; this screen's third slot was a keyword cut, so a ticket with an unusual wording could be missed). Open-PR overlap on GitHub: NOT checked (no identity).

## Questions for Wednesday
- **Q1. KS-1672: may the Spark take the write-site part alone?** What blocks a brief at live develop (read just now): (a) the sign-in path builds the key as `${providerName}Id` (`auth.ts` ~:1082, :1366) while the mapper is keyed `microsoft_personal` -> `microsoft_personal_id` and `User` has `microsoftPersonalId`, so `microsoft_personalId` would never match a column: a naming decision the ticket does not make; (b) the ticket says migration 001 adds FOUR columns (`google_id`, `apple_id`, `github_id`, `microsoft_personal_id`) and also names `linkedin_id` / `facebook_id`, while `userRepo.ts` already selects `linkedin_id` and `facebook_id` in `USER_COLS`: the column set is unsettled; (c) `createUser`'s INSERT would gain columns and `updateUser`'s `fieldMap` keys; (d) it says the fix "should go through a tier-1 gate" and "re-check the `:1318` conflict path (now live)", a behaviour change on a route that today answers `linked: true` falsely. **Question: rule the key naming (a) and the column set (b); then it is a code_patch2 (userRepo.ts + auth.ts + a test) for the next screen, with the conflict-path re-check left to the Opus gate.**
- **Q2. KS-1690: does the Spark get it?** If yes, two rulings first: origin-session lookup (the interactive `POST /api/auth/refresh` oracle at `routes/auth.ts:~688`) or a credential epoch; and does the authorization-code sibling stay out. The gate's condition (a) (fail closed on no or unknown `sessionId`) is a spelled-out clause for the lookup shape. It borders KS-1692's `session.ts` partition (G).
- **Q3. OpenAPI.** By ruling this brief makes no OpenAPI change, so the new response field `needsReauth` is undocumented in the published spec. Is a follow-up ticket wanted, or is the omission intended until the UI consumes it?
- **Q4. `ks_1116_p1` may be superseded.** Develop moved at 14:39 to `561a6c5b5282` = `Refs KS-1116: two role-prefix rows and an EXTENDS-tenant row for gate BM1 NOTE 1`, touching only `vc-issuer/.../ks1116-presentation-and-credential-reads-bound-to-the-creator.test.ts`, which is the file `ks_1116_p1` edits. Someone has built the same three rows. If the holder still has `ks_1116_p1`, it will now conflict (or be a duplicate); check before holding it.

## Things Wednesday should read before holding
1. **One production behaviour change, additive only:** a new boolean `needsReauth` appears in the body of `GET /api/connections/:id`. A strict client (a schema validator with `additionalProperties: false`) would reject it; none exists in this repo (`git grep tokenExpired` finds only `index.ts:794` and a user-testing doc line), and the m365 OpenAPI file does not mention `tokenExpired` either. The PR will want a tier-1 gate only because the service handles tokens, not because auth logic changes.
2. **What the cells cannot see.** The in-memory value `''` (what the OAuth callback assigns on a fail-closed exchange before the row is persisted and read back) is not driven by any cell: reaching it needs the callback and a real MSAL exchange. `!connection.refreshToken` is true for `''`, `undefined` and `null`; a rewrite as `=== undefined` would miss `''` and no cell here would notice. A reviewer should hold the expression, not only the cells. This is stated in the brief's UNMEASURED.
3. **R3's undecryptable token is a `v1:` string.** `isEncryptedPii` matches `^v\d+:`, and in the test process `decryptField` throws (no keyring), so `decryptToken` fails closed to `undefined`. The cell therefore proves the fail-closed path, not a particular cipher error. The test logs the decrypt error line to stderr (expected).
4. **Same-file pairs:** none (the new test file is new; `index.ts` is edited at 2 lines near `:794`). Rebase risk: any seat editing the m365 `index.ts` status route (none known).
5. **`started_ok` was NOT needed:** KS-1689 is Backlog, assignee none.

## Findings
1. **The first brief ran clean in all three gates and the model reproduced a 148-line new file plus the product hunk byte for byte** (BYTE-IDENTICAL, not just tree-identical). The two hazards recorded in screen 21 (a quote of the other kind inside a single-quoted JS string; a blank context line) were avoided by construction: no escape-tempting content, product hunk pure insertion with non-blank context lines.
2. **Hook friction (as screens 20-21):** `git -C $VAR fetch` on the Spark cache is refused by the no-cd hook (it cannot see through the variable); the same command with the literal path ran. A `======` separator in a Bash call is refused by the zsh word-split hook.
3. **Develop moved once in 4 minutes** (14:36 -> 14:39); the stale check (named files only) is what keeps a round valid; I re-read `ls-remote` before the dry-run, control and real round.

## NOT done / NOT tested
- Briefs: 1 of 3 slots. KS-1672 and the third slot were not drafted as files (decisions above); no `IMPROVEMENTS.md` entry written (scope was this file and the spark dirs).
- The whole m365 suite and `tsc` are the checker's (A6, A7: both PASS in the round); by hand I ran the one new file, `tsc --noEmit` per mutant.
- No open-PR query; no hold, no raise, no `hold_ready`; `queue.md` not touched.
- Housekeeping: `spark/cache/work/` gained 2 per-round clones (control + real, about 335 MB each, none quarantined); `spark/state/dry/` gained the dry-run input; the Spark cache fetched develop up to `561a6c5b5282`; nothing deleted.

## Files written
Brief (`KS-1689.md`, `golden.diff`, `spark.pins`) under `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1689_p1/`. Run dirs `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1689_p1` and `...-control`. This file. Scratch (not durable): `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/2d22076e-ad72-46a3-8b8a-b18a3ab3782c/scratchpad/s22/` (clone/, newtest.ts, mk1689.py, mut.py, specA.json, mutA.out, ticket dumps KS-1689/1672/1690/1327.txt).
