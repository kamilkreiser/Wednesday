REPORT_SHA256_16: 465eec274ce18e10 (recipe: tail -n +4 verdict.md | shasum -a 256 | cut -c1-16)
VERDICT: GO WITH NOTE (0 Major, 2 Minor)

# Gate round 2 (delta): Secuura PR #1537 (KS-1564), Sonnet tier 2

Head under test: `b872e659fedba832ecc68af103e35694e0afdaed`, tree `e9e72c9dce12c05c5faa077e7dd9362eaf4d82d4` (both asserted by rev-parse in my own `clone --shared`, push URL disabled, refs/pull/1537/head fetched with the project's core.sshCommand). Old head `557063b9e4579719912142bf6dcd9d36076e6e88` asserted. Develop at gate time `2cdf1d7a9071e078bc3f3b3f4d44ce1fa4e50a6f` asserted.

## VERDICT: GO WITH NOTE. Both round-1 Majors are fixed in the browser (with a control that reproduces the bug on the old head). Two Minors, neither blocks. NOT RUN: the three Playwright cells (no real stack). No deploy recommendation (ships only in the KS-1570 round).

## 1. Numbers, each with instrument and control
| Item | Result | Instrument / control |
|---|---|---|
| Delta scope | 1 commit on the old head; 3 files, +125/-15 (ApiKeys.tsx, the ks1564 guard test, sysadmin-exhaustive spec) | `git diff --stat 557063b9 pr1537`, `rev-list --count` = 1. Matches the claim. evidence/diffstat_old.txt |
| Against develop 0026a43e | 5 files, +544/-40 (round 1 said 433; delta adds the difference, fine) | evidence/diffstat_dev0026.txt |
| Overlap with live develop 2cdf1d7a | none: develop changed 12 files since 0026a43e (migration 049, security service, shared index), PR touches 5; `sort | uniq -d` of the two lists is empty. `merge-tree --write-tree` rc 0, tree bc70d7dc, no conflicts | evidence/pr_files.txt, dev_changed_files.txt, merge_tree.txt. Control: both lists non-empty (12 and 5) |
| Guard on new head | 9/9 pass | `npm run test --prefix packages/shared -- ks1564`, evidence/guard_new_head.txt |
| Guard (new test) on OLD ApiKeys.tsx | 8 pass, 1 RED: cell 5 only. **Cell 4 is NOT red on the old code** (the old code already called `fetchApiKeys(orgId)`; cell 4 only reds a bad call shape). The brief's "expect red on new cells 4 and 5" is half wrong; nothing is wrong in the code | evidence/guard_newtest_oldcode.txt; file restored byte-identical (cmp) |
| Whole shared suite | 50 files / 963 passed, 0 failed (round 1: 960, +3 new cells = 963, consistent) | evidence/shared_suite_head.txt |
| tsc (frontend/admin) | rc 0. Control: planting `fetchApiKeys()` -> TS2554 at ApiKeys.tsx(137,26), rc 2 | evidence/tsc_head.txt, tsc_planted.txt |
| eslint src | 0 errors, 58 warnings, none in ApiKeys.tsx (grep count 0). Control: planted `debugger; var` -> 2 errors | evidence/eslint_head.txt, eslint_planted.txt |
| vite build | rc 0 (`tsc && vite build`; tsc leg proven live by the planted run). Only the 500 kB notice | evidence/build_head.txt |
| Install | root `npm ci --ignore-scripts`, 1937 packages, rc 0 | evidence/npmci_root.txt |

### Guard mutants (new head; script evidence/mut.py, output evidence/mutants.txt, mutants_N6b.txt; file restored byte-identical)
| Mutant | Result |
|---|---|
| CONTROL comment-only edit | 9/9 green (good) |
| N1 loadKeys guard deleted | RED cell 5 |
| N2 guard moved after the state writes | RED cell 5 |
| N4 guard moved before the await | RED cell 5 |
| N12 guard text changed to an empty block | RED cell 5 |
| N5 `fetchApiKeys(orgId ?? 'x')` | RED cell 4 |
| N11 multi-line `fetchApiKeys(\n orgId \|\| 'x')` | RED cell 4 |
| **N3 guard line turned into a comment** | **SURVIVES (9/9)**: cell 5 is text-position only; behaviour is unguarded |
| **N6b `fetchApiKeys(String(orgId) \|\| ['default','org'].join('-'))` plus any other plain call** | **SURVIVES (9/9)**: the argument regex `[^()]*` cannot see an argument containing parentheses, so the call is skipped (alone it reds only by accident, via "calls.length > 0"; N6) |
| N7 alias call `const f = fetchApiKeys; f('x')` | SURVIVES (no paren after the name) |
| N8 a comment quoting `fetchApiKeys(orgId \|\| 'x')` | false RED cell 4 (conservative, harmless) |
| N9 organisations-loader guard deleted | SURVIVES (no cell pins it) |
| N10 Generate in-flight guard (`submitRef`) deleted | SURVIVES (no cell pins it) |
The author said the race behaviour is pinned only by a browser run: true, and N3/N9/N10 confirm the cells pin text, not behaviour. The author's claim that cell 4 refuses `||`, `??`, quotes, templates, ternaries holds for paren-free arguments only.

## 2. FOUND / TESTED / HOW (browser: built page of the new head, served by a stub, port 7561; control build of the OLD head on 7562)

Stub (evidence/stub2.js, derived from the round-1 stub with added 401/409 mint modes and per-org list modes): serves dist under /admin/, fake `/api/auth/refresh`, `/api/users/me`, `/api/platform/tenants[/id]`, `/api/users/admin/organizations`, `/api/security/keys` GET/POST/DELETE with switchable delay and status per org. Driven by Playwright MCP. Nothing of the real stack. Both stubs stopped (pgrep clean for stub2.js); browser page closed.

### MAJOR 1 (stale list overwrite): FIXED
- Exact round-1 reproduction (Alpha 1.8 s, Beta fast, pick Beta while Alpha in flight, read at 3 s): select = Beta; first row "K for bbbbbbbb-... Beta" with organisation Beta. 2 key requests (A then B).
- CONTROL, same script on the old head build: select = Beta, row "K for AAAAAAAA-... Org <b>Alpha</b>". The bug reproduces without the fix, so the pass is real.
- Rapid A-B-A-B-B (A 1.5 s, B 0.6 s, 80 ms apart; 5 requests): final Beta row, no error.
- Refresh during an in-flight load, then switch to Beta: final Beta. Refresh in flight on the same org: final that org's row, no error.
- Error response arriving after a newer success (Alpha 500 after 1.5 s, Beta fast): final Beta rows, `apikeys-list-error` count 0. Not overwritten.
- Unmount during a request (switch to the Overview tab with Alpha in flight): zero console errors/warnings captured, tab changed cleanly. (React 19, which does not warn on this; no cancel exists, the answer is dropped harmlessly.)
- Organisations loader vs tenant switch (T1 orgs delayed 1.8 s, in-app history switch to T2 at 300 ms): final select holds only "T2 Org", row is T2's, requests: orgs(T1), orgs(T2), keys(t2-org-1) with the T2 override. No T1 leak. Note this goes through a remount of the component in the real route, so the orgs-loader guard line itself is NOT exercised by this test (and N9 shows no source cell pins it): the guard is read, not proven by a run.
- Code read, every setState after an await in loadKeys: all of `setKeys/setIsLive/setListError/setLoading(false)` come after `if (seq !== keysReqRef.current) return;` and no second await exists. loadOrganizations: every write after `await fetchOrganizationsChecked()` is after its guard (`if (seq !== orgsReqRef.current) return;`), no later await. The `!orgId` branch bumps the seq first, then writes synchronously, no await. Unguarded writes after an await: none in those two. The mint and revoke handlers write after their awaits without a guard (setSubmitting, setMintError, setRevokeError, setGeneratedKey), by design (they are user actions on the instance, not list state); a revoke answered after the operator switched organisation could show its error under the other organisation's selector: cosmetic, not reproduced, not rated.

### MAJOR 2 (e2e route): FIXED on reading, NOT RUN
- `openApiKeysTab`: waits for GET `/api/platform/tenants` while loading `platform/clients`, takes the first tenant id from `body.data.tenants ?? body.tenants`, goes to `platform/clients/<id>?tab=api-keys`, asserts `create-apikey-btn` visible. Checked against the code: App.tsx:53-54 has `/platform/clients` (ClientList, which calls `fetchTenants()` in a mount effect) and `/platform/clients/:id` (ClientDetail); ClientDetail reads `searchParams.get('tab')` and renders `<ApiKeys />` for `api-keys` (ClientDetail.tsx:54,355); the gateway proxies `/api/platform/tenants` (api-gateway routes/platform.ts:224) and the page's own `fetchTenants` reads `.tenants` after the data unwrap, which the helper handles in both envelopes. `getAdminUrl()` ends in `/`, so the concatenations are well formed. page.route registrations in 3.8b.2 and 3.8b.3 come before `openApiKeysTab`.
- In the built page against my stub: `/admin/platform/clients/T1?tab=api-keys` renders `create-apikey-btn`, `apikeys-org-filter`, `apikey-dialog`, `apikey-name-input`, `apikey-create-btn`, `apikey-generated-key`, `apikey-mint-error`, `apikeys-list-error`, `apikey-revoke-btn`, `apikey-revoke-error` (each used in the run). Not exercised: the real login, the real tenants response shape, `waitForResponse` timing.
- Cleanup cell: revoke looks for the minted name's row on the current table page. The page lists 10 per page in server order; if the org has more than 10 keys and the new key is not on page 1, the revoke locator fails and the cell goes red. Unknown without the real stack (note, not rated).

### Minors from round 1, re-driven
| Round-1 item | Result |
|---|---|
| 1 double-click | 800 ms mint delay, `dblclick`: exactly 1 POST, one key shown. CONTROL old head build: 2 POSTs. Three synchronous DOM `.click()` calls in one tick: 1 POST. After every failure the button is enabled again and a retry mints (`retryAfterFail` = 1 key). |
| 2 failure messages | mint 401 "session expired, sign in again"; 404 "organisation not found"; 409 "a key with that name already exists"; 400 "name too short" (all server words). 500, HTML 500 and empty-body 500 -> "...security service is unavailable (HTTP 500)". Status 0 (200 with no key) -> "Failed to generate API key: The security service returned no key."; network error -> "Failed to generate API key: Failed to fetch." No key shown in any case, dialog stays open. Revoke 500 unavailable text; revoke 403 server words plus hint. List 401/400/403/500/net shows status and server words. |
| 3 403 hint | "API keys may only be minted for your own organisation. Ask a platform administrator ..." (full stop inserted; server text had none). Revoke 403 "not allowed. Ask ..." |
| 4 e2e cleanup | read: 3.8b.1 closes the key dialog and revokes the row it minted; see the page-size note above. NOT RUN. |
| 5 guard | see mutants table; cells 4 and 5 work against their stated shapes, with the holes listed under Minor A. |

### Regressions (round-1 holds)
- Organisation string sent exactly as returned: mint body carried `bbbbbbbb-2222-4222-8222-bbbbbbbbbbbb` (list lower-case) and the list sends `AAAAAAAA-...` upper-case unchanged; dialog org differing from the list's: filter followed to Beta, one follow-up list GET.
- No `window.alert` in any scenario (dialog listener captured 0 across all runs).
- No fake key: `apikey-generated-key` count 0 in every failure.
- XSS: mint error `<img src=x onerror=window.__xss=1>` shows as literal text, `window.__xss` stayed null, the only imgs on the page are the three Secuura logos (src read), org name `Org <b>Alpha</b>` renders as text (0 `<b>` elements).
- No effect loop / double fetch: first load and switches show one list GET per action (5 requests for the 5 switches in A-B-A-B-B, nothing extra).
- The diff is exactly the three files (diffstat above).

## 3. Findings
### Major: none.
### Minor
**A. The guard cannot see everything its header claims (packages/shared ks1564 test, `fetchApiKeysArgs` regex and `racesAreGuarded`).** Shape: N6b (argument with parentheses plus any plain second call) passes 9/9; N3 (guard commented out) passes 9/9; N7 alias passes; N9/N10 are unpinned. The test's own header is honest that it pins wiring not behaviour, and the browser run above is the real pin, so Minor. Fix (optional): parse with a TypeScript AST or strip comments first and match the argument by balanced parentheses; add a cell for the organisations loader guard.
**B. `describeFailure` `message.replace(/[.\s]*$/, '')` is quadratic on a long run of dots/whitespace followed by another character (`frontend/admin/src/pages/ApiKeys.tsx:99`).** Measured in node (V8, same engine as the browser): 20k spaces + "x" 230 ms, 40k 947 ms, 80k 3.84 s; control, 80k plain letters 0.27 ms (evidence/redos.js). A server error message of that shape would freeze the tab. Exposure is low (the messages come from the platform's own services, whose text could still echo user input). Fix: trim in a linear way, e.g. `message.replace(/\s+$/, '').replace(/\.+$/, '')` or a manual end-scan.
### Notes (not rated)
- The brief's expectation that cell 4 reds on the old code is wrong (it passes there); cell 5 is the cell that reds.
- The e2e revoke cleanup assumes the minted key is on the first table page.
- An unmounted instance's answer is dropped silently, not cancelled; fine in React 19.

## 4. NOT tested
Real stack and all three Playwright cells (not run); the real security service and tenants response shapes (stub invented them from the page's types); the PR body wording (GitHub body not fetched, read-only no gh); visual look, dark mode and keyboard use; the orgs-loader guard line in isolation (route remounts, see above); behaviour for ADMIN after KS-1570 (server PRs); the author's preflight legs; Linear/GitHub state.

## 5. Housekeeping
Project folder untouched (the only git write verbs ran in my scratchpad clone `scratchpad/r2/repo`; its origin push URL is `DISABLED`). Both stubs stopped. The Playwright MCP server processes belong to the harness and were left running; my page was closed.
