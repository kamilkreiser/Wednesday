## What

RD-999. With sign-in enforced, a `session_token` cookie whose value is the name of a built-in object property (`constructor`, `__proto__`, `toString` and the nine other names `Object.prototype` carries), or a JSON cookie that wraps one (`j:["constructor"]`), was taken for a session. `getSession` read `sessions[id]`, which reads up the prototype chain and found an inherited value that never expires. When no user was stored, the cookie passed as a viewer: viewer routes, the dashboard page and POST /api/chat all answered 200. When users were stored, every route answered 500.

## The fix

`getSession` (backend/jsonStorage.js) now answers only for a string that names an OWN entry of the store, and only when that entry holds a string `email` and an `expiresAt` that reads as a time. Any other value is no session, so every caller gives its existing refusal: 401 `SESSION_EXPIRED` on the API, and a redirect to /login on a page. A malformed own entry is refused, not removed. backend/server.js is unchanged.

## What stays the same

A real session's answer, its expiry, the removal of an expired session and the session file's bytes. No route gate changes, no user-facing words are added, and the first-run open window is untouched.

## Tests

New suite `__tests__/session-cookie-inherited-name-refused.test.js` (16 cells):
- In-process cells cover every inherited name, the array forms, malformed own entries, the real session, the expired session and the method source.
- HTTP cells run on two local servers with sign-in enforced, one with no stored user and one with an administrator and a viewer.

The cells are red without the fix and green with it. Test counts: 5862 tests in 377 suites.

Not deployed. The merge starts Deploy demo (backend paths). Its jobs are gated on the `CI_DEPLOY_ENABLED` repository variable and must read skipped.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
