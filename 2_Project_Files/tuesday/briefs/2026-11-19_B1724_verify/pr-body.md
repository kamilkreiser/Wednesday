## What changes

RD-994. Several audit entries record text taken straight from a request (a sign-in address, a user's name or role, a data-source workspace id or endpoint, the identity provider's error text on the sign-in callback, and so on), with no bound on its length or type. This change bounds those fields at the request.

- One table (`AUDIT_FIELD_RULES`, fifteen rows on thirteen routes), one check and one guard, `auditFieldGuard`, added to `backend/server.js` between the lines `// AUDIT-FIELDS-BEGIN (RD-994)` and `// AUDIT-FIELDS-END (RD-994)`, and mounted once with `app.use(auditFieldGuard);` directly below the sign-in gate (`app.use(requireAuth);` and `app.use(afterAuthGate);`) and above every route it names.
- A request to one of those routes that carries a value that is too long, or of the wrong type, in a field the table names is refused with a 400 and a one-key answer, for example `{ "error": "Name too long (max 256 chars)." }` or `{ "error": "Role must be text." }`, before the route runs. The route does nothing and no audit entry holds the value.
- The answer is built only from the table's own field names and numbers. It never repeats any part of the request.
- An ordinary request is answered exactly as before. `auditLog`, `AUDIT_ACTIONS`, every audit call and every route handler are unchanged; the change adds 97 lines to `backend/server.js` and removes none.
- The routes: `POST /api/auth/login`, `GET /api/auth/microsoft/callback`, `POST /api/auth/users`, `PUT` and `DELETE /api/auth/users/:email`, `POST /api/auth/entra-config`, `POST /api/setup/log-analytics`, `POST /api/data-sources`, `PUT /api/data-sources/:id`, `POST /api/setup/data-sources`, `POST /api/setup/domain`, `POST /api/setup/ai-config`, `POST /api/setup/ai-test`.

## Who chose what

- Chosen by the product owner: an over-long value refuses the request and the user sees an error, with these four limits: email 254 characters, name 256, address (URL) 2048, lists of 50 items.
- Defaults of this change, not chosen by the product owner: the 400 status; the wording and the one-key shape of the answer; refusing a value of the wrong type as well as an over-long one; every other number (role 32, workspace id 64, data-source id 128, auth mode 64, AI deployment name 256, domain and each additional domain 253, the callback's `error` 1024 and `error_description` 8192, at most 50 body keys of at most 64 characters on the Entra settings route); the guard's place before the routes' own administrator checks; and the rule that `rememberMe`, when sent to the sign-in route, must be true or false.
- Two numbers follow existing tests: the callback's `error_description` limit is 8192 so that an existing test's 5000-character description still gets its old answer, and the AI test route's endpoint is checked for length only, so the route keeps answering a non-text endpoint with its own refusal.

## Refused before the administrator check (a known trade-off)

The guard runs above the routes, and the administrator checks of these routes sit inside each route. So a signed-in user who is not an administrator and who sends an over-long or wrong-type value to an administrator-only route now gets the guard's 400 instead of the route's 403. For that request no `REQUEST_DENIED` ("forbidden") audit row is written; the `STATE_MUTATION` row is still written, with the method, the path, status 400 and the caller's masked address. The caller can do nothing more than before: the request performs no action, and the answer reveals only the fixed limits. Anyone who watches for non-administrators trying administrator routes should also watch for `STATE_MUTATION` rows with status 400 on these paths. A signed-out caller still gets the sign-in gate's answer first. Sending an ordinary value still gets the 403.

## The cells

A new test file, `__tests__/rd994-audit-field-guard.test.js`, 111 cells:
- 89 cells run the block on its own (cut out of `server.js` and run in a sandbox): for every field, a value one over the limit is refused with the limit in the text, a value at the limit passes, and a wrong-type value is refused (or passes, for the length-only field); plus lists, key counts, path matching (letter case, one trailing slash, a percent-encoded path value), HEAD read as GET, odd body shapes, no echo of the request, and the table being frozen.
- 3 cells read `server.js` as text: every row names a route registered once below the mount; the mount sits below the sign-in gate and above every route; every audit call is classified, so a new one turns the cell red until it is.
- 12 cells drive a real server and read the audit export: each refused request answers 400 with the exact text, and no entry holds the value (and a refused user add stores no user).
- 7 cells pin answers that must not change, including the 403 for an ordinary value from a non-administrator and the 400 trade-off above.

One existing cell in `__tests__/rd765-766-linear-text-patterns.test.js` changes its expected text: the 200,000-character attack address sent over HTTP to the user add route is now refused by the length check (`Email too long (max 254 chars).`) before the route's email shape check. Its status (400) and its speed bound are unchanged. The email checker's linear time is still pinned by the cells in that file that call the checker directly and that check the server uses it. The cell count of that file is unchanged.

`scripts/verify-expected-counts.json`: 5898 tests over 379 suites becomes 6009 over 380.

## Verification

Full suite: 6009 of 6009 tests passed across 380 suites. Each new cell fails when the part of the change it covers is removed (the mount, the limit comparison, the length-only rule, the 8192 limit, the path matching). Requests sent with letter-case and trailing-slash path variants, form-encoded bodies, repeated fields, bracketed form fields, a JSON content type with a charset, HEAD, and percent-encoded path values were all refused when the matching route would otherwise run. Code scanning run locally on this branch and on main shows no new result.

Not covered here: audit rows written by other modules, sign-in rows built from the identity provider's claims, the request path and user agent, and a cap on a whole audit entry, so the size of the audit file as a whole is not claimed to be bounded. Code-scanning alerts 235, 236 and 237 are left open; this change does not claim to close any of them.

Not deployed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
