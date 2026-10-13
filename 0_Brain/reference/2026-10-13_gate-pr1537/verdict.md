REPORT_SHA256_16: de22859410b28af3 (recipe: tail -n +4 verdict.md | shasum -a 256 | cut -c1-16)
VERDICT: NO GO (2 Major, 5 Minor)

# Gate: Secuura PR #1537 (KS-1564), Sonnet tier 2

Head under test: `557063b9e4579719912142bf6dcd9d36076e6e88`, tree `0f250edafb3073f5d4ca9eb2eb8852c248dffa43` (both asserted via rev-parse in my own `clone --shared` + fetch of refs/pull/1537/head), develop `0026a43e60337d81c3d2549f36de0507edc128f4` (asserted; merge-base of head and develop equals develop). Diff vs develop: 5 files, +433/-39 (matches the claim). The diff vs 0f9bd081 is the develop merge (17 files, unrelated to this PR).

## VERDICT: NO GO (2 Major, 5 Minor). Both Majors are small fixes; re-gate after. No deploy recommendation (ships only in the KS-1570 round).

## 1. Numbers, each with instrument and control
| Item | Result | Instrument / control |
|---|---|---|
| Guard on head | 6/6 pass | `npm run test --prefix packages/shared -- ks1564` (vitest 4.1.11) |
| Guard on develop's two files swapped in | 3 red (cells 1, 2, 3), 3 green (exists, C1, C2) | same command, files from `git show origin/develop:`; evidence/guard_develop.txt. Control: reds are exactly the claim |
| Mutants on head | M1 literal in mint: red (cells 1+3). M3 `\|\|` fallback in api.ts: red (1+2). M4 literal in another file: red (1). M5 `'default'+'-org'` in mint: red (3). M9 ternary in mint: red (3). Comment containing the literal: RED (cell 1) | evidence/mutants.txt, evidence/mut.py. Files restored byte-identical (cmp) after |
| Mutants that SURVIVE | M6 constant built with join() passed as identifier; M7 `?? \`default-${'org'}\`` in api.ts; M8 `fetchApiKeys(orgId \|\| FB)` with FB built from pieces: all 6/6 green | same. These are inherent limits of a source-text guard, see Minor 5 |
| Whole shared suite | 50 files / 960 passed, 0 failed | `npm run test --prefix packages/shared`, evidence/shared_suite_head.txt |
| walkTimeouts line necessary | with the line removed: 1 failed / 959 passed ("configured list equals the derived one", Array(8) vs Array(7), names ks1564 file). Restored: 960/960 | evidence/shared_suite_noWalkLine.txt. Line is at the correct sorted position |
| tsc (frontend/admin) | rc 0, empty output | `tsc --noEmit -p`. Control: planting `fetchApiKeys()` -> TS2554 at ApiKeys.tsx(125,26) (evidence/tsc_planted.txt) |
| eslint src | 0 errors, 58 warnings; none in the diff (the api.ts:100 warning is on an untouched line) | Control: planted `debugger; var` -> 2 errors reported (evidence/eslint_planted.txt) |
| vite build | rc 0 (`tsc && vite build`), only the 500 kB chunk notice | evidence/build_head.txt. Control: tsc leg is the one planted above |
Install: root `npm ci --ignore-scripts` (1937 packages) in my scratchpad; a per-package `npm ci` first failed for frontend/shared imports, so the root workspace install was needed for tsc/eslint.

## 2. FOUND / TESTED / HOW

### Major
**MAJOR 1: a stale list response overwrites the table: keys of one organisation shown under another organisation's selector.**
`ApiKeys.tsx` loadKeys (about lines 117-141): no request token or cancel; each response calls `setKeys(...)` unconditionally.
Shape: org list loads with Alpha selected; Alpha's key list is slow (1.8 s); operator picks Beta in `apikeys-org-filter`; Beta answers first, Alpha answers later and overwrites. Measured (stub, real built page): after 2.8 s the select reads Beta (`bbbbbbbb-...`) and the first table row is "K for AAAAAAAA-... / Org <b>Alpha</b>". The row's Organization column is the stale org's name too, so the screen is internally consistent and wrong. Revoke acts on the key id so no cross-organisation write, but an operator can revoke or copy a prefix believing it belongs to the selected organisation. Same class applies to the Refresh button.
Minimal fix: in loadKeys keep a ref counter (`const seq = ++reqRef.current; ... if (seq !== reqRef.current) return;` before every setState) or an AbortController keyed on orgId.

**MAJOR 2: the three new Playwright cells navigate to a route that does not exist and will fail on the real stack.**
`tests/e2e/tests/sysadmin-exhaustive.admin.spec.ts` cells 3.8b.1-3 call `adminNavigateTo(page,'api-keys')`, which is `page.goto(<admin base>api-keys)` (`fixtures/test-helpers.ts:313-321`). `App.tsx` has no `/api-keys` route; ApiKeys is rendered only as a tab of `ClientDetail` (`ClientDetail.tsx:355`, reached at `/platform/clients/:id?tab=api-keys`). Measured on the built page: `GET /admin/api-keys` ends at `/admin` (the catch-all Navigate to `/`), and `apikeys-org-filter` count is 0. The older 3.8.x cells use the same navigation but are written soft (try/visible checks), so they never noticed; the new cells hard-assert (`expect(mintBody).not.toBeNull()`, `toBeVisible()` on `apikey-mint-error`/`apikeys-list-error`) and will go red on first real run. The testids themselves all exist (checked each of apikey-mint-error, apikeys-list-error, apikey-dialog, apikey-generated-key, apikey-name-input, apikey-create-btn, create-apikey-btn against ApiKeys.tsx). NOT RUN, reasoned plus the redirect measurement.
Minimal fix: open `/platform/clients/<tenant id>?tab=api-keys` (a tenant id is available from the platform tenants list), keeping the rest.

### Minor
1. **Double-click on Generate mints twice.** `handleGenerateKey` has no in-flight guard. Measured with 800 ms mint delay and `dblclick`: 2 POSTs with the same body; the dialog shows only the last key, the first live key is orphaned (shown nowhere). Pre-existing, not a regression, but the handler was rewritten here. Fix: `submitting` state, disable the button, early return.
2. **Failure text for 401/404/409/status 0 drops the server's words and misleads.** `describeFailure` (ApiKeys.tsx ~line 90): a 404 "organisation not found" renders "the security service is unavailable (HTTP 404)"; a 200 with no key (synthesised status 0 in `createApiKey`) renders "HTTP no response". Author-flagged; measured on mint 404, 500, html, emptybody, empty200, net, and list 401 (list shows the server words correctly, mint/revoke do not). Fix: show `message` for any 4xx, keep the "unavailable" text for 5xx and 0 only.
3. **403 hint is glued without punctuation:** "API keys may only be minted for your own organisation Ask a platform administrator..." (measured) when the server message has no trailing period. Fix: `${message.replace(/[.\s]*$/, '')}. Ask ...`.
4. **New e2e 3.8b.1 mints a real key per run and never revokes it.** Housekeeping, matches the older 3.8 cell habit.
5. **The source-text guard is satisfiable by moving the literal** (survivors M6, M7, M8 above, and a `??` fallback is not caught by cell 2, only `||`); it also reds on a comment that quotes the literal. The guard states honestly that it pins wiring, not behaviour; the survivors need deliberate construction of the string, so I rate it Minor. Cell 3 correctly rejects literals, concatenations and ternaries. Cells cannot pass for the wrong reason: the controls C1/C2 were both green and the develop swap reds exactly the three expected cells. Hardening, optional: add a cell that no `fetchApiKeys(` call argument contains `||`, `??` or a quote.

### Author's doubts, answered
- Effect chain / extra reload: not reproduced. First load = 1 organisations GET + 1 keys GET + 1 tenant GET. Tenant switch (in-app history change from T1 to T2): ClientDetail unmounts ApiKeys while it reloads, so ApiKeys remounts fresh: 1 tenant, 1 orgs (X-Tenant-Override T2), 1 keys with the new org. Refresh button = exactly 1 keys GET. No loop (organisations-failed state held at 5 requests for 6 s; the 5 vs 1 is the browser retrying a reset socket, shown by a raw `fetch` control that also produced 2 requests for 1 call).
- Tenant switch preselection: after the switch the select held only "T2 Org" and the table showed T2's key. Preselection follows the new list (first organisation) by design; no stale org id leaked (T=T2 on every request after the switch).
- Dialog org differing from the list's: dialog set to Beta, mint body carried Beta's id verbatim (mixed-case id sent unchanged), filter followed to Beta, 1 follow-up keys GET, generated key shown. Correct.
- Org string exactness: list and mint carried `AAAAAAAA-1111-...` / `bbbbbbbb-...` exactly as the stub returned them (uppercase preserved, no re-casing, no trimming).
- Accessibility: both selects have an accessible name (aria-label "Organisation" and a `<label htmlFor>`); an organisation with an empty name shows its id. Visual appearance NOT examined.

### What passed (Task 3/4 matrix, stub backend)
Organisations 0: Generate disabled, message "There are no organisations...". 1 org: preselected, list loads, Generate enabled. 3 orgs: fine. Organisations 403/500/502-HTML/network error: red banner with status and server words, "API keys are not shown.", Generate disabled, dialog select "No organisations", no keys call made. List 400/403/401/500/html/network: shown with HTTP status and message, never as an empty table; empty 200 shows "No API keys found". Mint 201: key shown once. Mint 400: server reason inline, dialog stays open, no key. Mint 403: reason plus hint inline, dialog stays open, no key. Mint 500/html/empty body/network: readable text, dialog open, no key. Revoke 500/403: inline error with the server words on 403. `window.alert` never raised in any scenario (0 dialogs captured). B-06: no fake key in any failure (`apikey-generated-key` count 0 each time). Errors as `{code,message}`, plain string, object without message ("Request failed (400)"), HTML body, empty body: no "[object Object]", no crash. XSS: a message of `<img src=x onerror=...>` (string and object forms) and an org name `Org <b>Alpha</b>` render as literal text, `window.__xss` stayed unset, 0 img elements; no `dangerouslySetInnerHTML` in the changed files.

### Scope (task 2 and 7)
`git grep` over every tracked file at the head: no other sender of the retired literal; the only remaining occurrences are in the security service's ks1553 integration test (server side, mints with it on purpose) and nothing under frontend/. Callers of `fetchApiKeys`/`createApiKey`/`revokeApiKey`: ApiKeys.tsx only; `ClientDetail.tsx:15` imports `fetchApiKeys` and never calls it (dead import, tsc/eslint accept it). `/api/security/keys` appears in frontend only in api.ts. Diff stat matches the description. The PR body text was not fetched (GitHub read not attempted: no `gh` write, and the brief's first-lines check on the body is therefore NOT TESTED).

## 3. NOT tested
Real stack and the three Playwright cells (not run, per brief); the real security service's response shapes (my stub invented them, from the page's own types and the brief); the PR body wording; visual appearance and dark-mode/keyboard use of the selects; behaviour at ADMIN-without-scope after KS-1570 (that is the server PRs); the author's preflight legs 3, 4, 8 and shell suites; Linear/GitHub state.

## 4. What I stubbed
A single Node server (evidence/stub.js) serving the built `dist` under `/admin/` plus fake `/api/auth/refresh`, `/api/users/me`, `/api/platform/tenants[/id]`, `/api/users/admin/organizations`, `/api/security/keys` (GET/POST/DELETE) with switchable response modes (403/500/502-HTML/socket reset/empty), driven by Playwright MCP. Sign-in is the silent-refresh path. Stub and browser stopped (pgrep clean); scratchpad clone left in place (session scratchpad only).
