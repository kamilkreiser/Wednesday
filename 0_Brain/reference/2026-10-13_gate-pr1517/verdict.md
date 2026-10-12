# Gate verdict: Secuura Platform K PR #1517 (KS-1232)

- Head under test: d5ae69e2eec6c84fcd62515c29148359e83ef1c3 (refs/pull/1517/head fetched fresh; equals the stated head exactly)
- develop: 4ec53e1874d06636cacc08dd224d980139e5906b (`git ls-remote` at gate time; did not move; equals the PR parent)
- Tier: 2 (Sonnet, independent QA gate). Date 2026-10-13.
- Tree: scratch clone `--shared` of the main checkout (read-only), fetch of refs/pull/1517/head and refs/heads/develop with the project's core.sshCommand, `git archive` of head and of head^ into scratchpad `q1517/{head,base}`, node_modules shell of symlinks to the main checkout's deps (read-only), @secuura/* re-pointed into the scratch tree, packages/shared built there (tsc rc 0). Nothing written inside !CODING.

## VERDICT: GO

Majors: 0. Minors / notes: 3 (none blocking).

## 1. Topology
- base = parent = 4ec53e18 (develop tip). 3 files, +261 -4: services/health.ts (+11 -1), ks480-connector-auth.test.ts (+6 -3), new ks1232-info-reader-refuses-a-non-array-allow-list.test.ts (+244). Total +261 -4 confirmed.
- `git merge-tree --write-tree develop head` -> deb35bb82f2f3d638df6c3cbf229fbf5a1e68974, clean, equals the builder's prediction (deb35bb82f2f). Trivial, since the parent is the develop tip.

## 2. The predicate, expression by expression
Info reader, Blockchain/Dev/services/api-gateway/src/services/health.ts:76-80:
`const rawAllowedTypes = connectorConfig.allowedDocumentTypes; if (rawAllowedTypes !== undefined && rawAllowedTypes !== null && !Array.isArray(rawAllowedTypes)) { 403 FORBIDDEN ... return; }` then `allowedDocumentTypes: rawAllowedTypes || []` (:86).
Create path, routes/verification.ts:1306-1311: the same declaration and the same `if` condition, character for character, same status/code/text string, then `(rawAllowedTypes || []) as string[]`. The container resolution above both guards is the same code shape (KS-1231 on the info side). The 403 text is byte-identical (checked by the agreement cell and by my own table below).
Because the two conditions are textually identical, no value can make them decide differently at the shape level. I verified that empirically through BOTH real routes for 30 values (table in section 6): zero shape disagreements.
Reader-side `|| []` on an array is a no-op (arrays are truthy), so a list answers the list unchanged.

## 3. Cells at head
- ks1232 new file: 5 tests pass; ks480-connector-auth: 5 pass (10/10 together).
- Red-first: new + flipped test files dropped onto the untouched parent health.ts: 3 failed / 7 passed. The 3 red = the flipped ks480 cell, the refusal table, the AGREEMENT cell. Matches the claim exactly.
- Neighbours at head: ks1204 11/11, ks1231-info-reader 3/3, ks1231-a-connector-allow-list 4/4, ks480-connector 5/5.

## 4. The flipped cell
Diff of ks480-connector-auth.test.ts is only the one cell: title, `answers.push([res._status, body.error?.code, body.error?.message])` and the expectation `[refused x3]` with refused = [403,'FORBIDDEN', exact text]. It asserts status, code and the full message for "", 0 and false. Setup lines untouched; the other 4 ks480 cells are not in the diff. Nothing weakened. (The flipped cell does not check the raw value is absent or the response count; the new table cell does.)

## 5. Mutants (health.ts at head mutated in my scratch tree, ks1232 + ks480-connector run, restored, sha256 of the file compared each time: 5642f712aadcdefb restored every time)
| Mutant | Result (failed/passed of 10) | Caught by |
|---|---|---|
| CTRL (no mutation) | 0 / 10 | n/a, control green |
| A guard removed | 3 / 7 | table, agreement, flipped ks480 |
| B strings only | 3 / 7 | same three |
| C falsy-as-absent (0/false escape) | 3 / 7 | same three |
| D also refuses null | 2 / 8 | agreement, unrestricted control |
| E status 400 | 3 / 7 | same three |
| F different text | 3 / 7 | same three |
| G missing `return` (second response) | 1 / 9 | refusal table only (via the response counter) |
| I `|| []` dropped | 2 / 8 | agreement, unrestricted control |
| J also refuses arrays | 3 / 7 | agreement, list control, unrestricted control |
| mine: status 401 | 3 / 7 | table, agreement, flipped ks480 |
| mine: authenticateToken dropped | 5 / 5 | table, agreement, both controls, flipped ks480 |
| mine: 403 body also echoes raw value | 1 / 9 | refusal table only (`allowedDocumentTypes === undefined` assertion) |
All 12 mutants killed, the control clean. G and the echo mutant each depend on a single cell (the refusal table): noted, adequate.

## 6. Shape decision table (real createHealthRoutes behind real authenticateToken(true) vs real createVerificationRoutes; ONE stored value; create with documentType SSD_DOCUMENT; harness = the PR's own plus extra shapes, kept in scratchpad `q1517/zz-x.head.keep`)
Info = decision of GET /api/connector/info at head. Create = POST /api/documents. Info at BASE shown for contrast.
| Stored value | Info (head) | Create | Agree | Info (base) |
|---|---|---|---|---|
| absent | 200 [] | permits | yes | 200 [] |
| null | 200 [] | permits | yes | 200 [] |
| undefined (explicit) | 200 [] | permits | yes | 200 [] |
| [] | 200 [] | permits | yes | 200 [] |
| array subclass [] | 200 | permits | yes | 200 |
| Proxy([]) | 200 | permits | yes | 200 |
| ['SSD_DOCUMENT'] / ['X','SSD_DOCUMENT'] / subclass ['SSD_DOCUMENT'] | 200 the list | permits | yes | same |
| '' | 403 text | 403 text | yes | 200 [] (defect) |
| 0, -0, NaN | 403 text | 403 text | yes | 200 [] (defect) |
| false | 403 text | 403 text | yes | 200 [] (defect) |
| true, 1, Infinity | 403 text | 403 text | yes | 200 raw echo |
| {} | 403 text | 403 text | yes | 200 raw echo |
| {length:1,0:'a'} (object with length) | 403 text | 403 text | yes | 200 raw echo |
| 'abc', ' ', '[]' (string / string array-like) | 403 text | 403 text | yes | 200 raw echo |
| new String('') | 403 text | 403 text | yes | 200 raw echo |
| Object.create(Array.prototype) (not an Array) | 403 text | 403 text | yes | 200 raw echo |
| function | 403 text | 403 text | yes | 200 raw echo |
| nested [['a']], [1,2], [null], [''], ['a'], sparse array | 200 echoes the array | shape passes (refuses only on the type NOT being in the list) | yes at the shape guard | same as head |
Zero shape disagreements across 30 values. (The array rows are the allow-list's type check, not the shape guard: for `['SSD_DOCUMENT']` both permit.)

## 7. Legitimate callers
Same 15 stored values (absent, null, explicit undefined, [], ['SSD_DOCUMENT'], ['X','SSD_DOCUMENT'], ['a'], ['a','b','c'], [1,2], [null], [''], [['a']], array subclass [], array subclass ['SSD_DOCUMENT'], sparse) read at BASE and at HEAD, full `{status, body}` JSON compared as strings: 15 of 15 byte-identical. A proper array (empty, one, many) and absent/null: no change.

## 8. Unauthenticated, wrong-role, malformed-container paths
Diff touches only lines after the KS-1231 container block; the auth middleware, the role 403 and the container 403 are untouched. ks480 "still 401s an invalid key" green; ks1231 info-reader 3/3 and ks1231 create-side 4/4 green; the dropped-authenticateToken mutant is caught. Not separately probed with a new test (see NOT TESTED).

## 9. Leak attack
Across all 16 non-array shapes I ran, the 403 body is ONE distinct body (`{success:false,error:{code:'FORBIDDEN',message:<constant>}}`): no stored value, no connector id, no config field. The old 200 body echoed the raw value for non-array shapes; the new one echoes nothing. Nothing new is exposed. The echo mutant is killed by the table.

## 10. Full checks
- api-gateway full vitest at head: 116 files / 1117 tests, 1117 passed, 0 failed, 0 skipped (one run by me; builder claims two).
- tsc --noEmit -p services/api-gateway: rc 0.
- eslint on health.ts and both test files: rc 0, no output.
- check:test-types for api-gateway: 151 files examined, 35 errors in baseline, 0 new, 0 stale. rc 0.

## Findings
Majors: none.
Minor 1 (accepted, builder's point 1): the predicate is duplicated (health.ts:77 vs verification.ts:1307), not shared. Drift is guarded only by the agreement cell, which exercises 12 shapes; my 30-shape run found no drift today. A shared helper would remove the class (follow-up, not a blocker).
Minor 2: arrays are not checked for string elements on either route; the info reader still echoes `[1,2]`, `[null]`, `[['a']]` raw (same as before, and create accepts the same shape guard). Outside the ticket's "non-array" wording; the admin write path (KS-1230) is where element types are validated.
Minor 3 (accepted, known): the info reader's settings-read `catch {}` still answers 200 [] where create answers 503 (KS-1532, explicitly out of scope). A 403 reaches an MCP agent as the generic "Connector info not available" note (known, recorded, unchanged by this PR). The reader now has two distinct 403 texts (container vs allow-list); each is correct and identical to the create path's corresponding text.
Builder points 4 and 5 assessed: the stubbed enforcement/workflow helpers do not matter for the allow-list guard, which sits before both; the response counter only matters on the info side because only the info side was edited, and the create side's guard is unchanged.

## NOT TESTED
- Live gateway / real Redis / real container (all tests use in-process routers and stubs; real settings come as JSON so NaN/Infinity/functions/Proxy cannot arise from storage, they were checked only as a predicate-parity exercise).
- A real MCP relay turning the 403 into the "not available" note (not run; builder's recorded claim only).
- The pre-push hook (13/16 legs) was not run.
- A second full-suite run; docs/OpenAPI absence of the route (builder says KS-1531) not independently audited beyond a grep showing the only consumers are mcp-server/api-client.ts:126, e2e specs and a troubleshooting doc.
- Unauthenticated / wrong-role responses were checked structurally (diff) and by the existing ks480/ks1231 cells, not by a new probe.
