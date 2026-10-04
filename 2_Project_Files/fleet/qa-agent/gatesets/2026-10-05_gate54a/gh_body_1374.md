`GET /api/users/lookup` now accepts a connector token, through the same
`authenticateAccessOrConnector()` door `POST /api/users/stub` has used since KS 564. The
`users:read` scope becomes the effective gate on the route.

Refs KS-1402

## Why

Platform S issues certifications by recipient email, so it needs K to resolve an email to a
userId. S authenticates with an `sk_` connector key, so its token is `type: 'connector'`, and
`/lookup` was guarded by plain `authenticate()`, whose `verifyAccessToken` refuses that type by
design (KS 480). The route's own role and scope gate never got a chance to run.

**The measurement, attributed.** Peter, on the ticket description (local S+K pair, platform-s
`f370236c` / platform-k `0736d8b78`, slot 3, 2026-10-01): **4 of 4** transfer-custody calls under
Organisation 3's connector key answered `transfer-custody status=401 … rejected by the user lookup
… Upstream said: Invalid token`, while the same key succeeded on originate (201) and on lifecycle
events in the same window. His reading of the tell: *"A missing scope would answer 403; what S
receives is 401 Invalid token."* Stuart re-measured on 2026-10-02 against platform-s `d04829b` and
platform-k develop `88e8877a2`: **5** refusals in a full suite run, **2** in `test:k-live` alone,
and confirmed by source read that `users.ts:266` still guarded `/lookup` with `authenticate()`.

**Ruled by Kam Kreiser, 2026-10-02 09:58:39 AEST (live board, card
`secuura-ks1402-lookup-refuses-connector-tokens`): option (a), "Widen /lookup to accept a connector
token, as /stub already does (KS 564)." This makes the 2 Sep ruling on KS 739 effective: the
users:read scope becomes the gate.**

## The change

Five files, +333/-4: the three code paths, plus both platform-k HTML docs (skill §4).

- `services/auth/src/routes/users.ts:266` — `authenticate()` becomes
  `authenticateAccessOrConnector()`. The import was already present at `:14`.
- `services/auth/src/routes/users.ts:357-358` — the KS 564 comment said *"this ONE route also
  accepts a connector token"*. That became false, so it now names both routes and records that the
  route's own role/scope gate still runs afterwards.
- `services/auth/src/middleware/authenticate.ts:69` — the docstring said *"for ONE route only
  (`POST /api/users/stub`)"*. Now names both.
- `services/auth/src/middleware/authenticate.ts:107` — **the log label was a latent defect, not
  cosmetics.** It read `'users/stub: connector token accepted (KS 564)'` *unconditionally*, so
  after this change every accepted connector call on `/lookup` would have written an audit line
  naming a route it never touched. It is now route-neutral and carries the route from the request.

**`req.originalUrl` is deliberately NOT used, and this is measured rather than assumed.** On this
route the query string *is* the email:

```
GET /api/users/lookup?email=alice%40example.com
  req.originalUrl        = /api/users/lookup?email=alice%40example.com     <- carries the address
  req.baseUrl + req.path = /api/users/lookup
POST /api/users/stub
  req.originalUrl        = /api/users/stub
  req.baseUrl + req.path = /api/users/stub                                 <- identical here
```

Carrying `originalUrl` would have put the queried address in plaintext into an audit line on the
one route that deliberately masks it — `users.ts:310` logs `queriedEmail` through `maskEmail()` for
exactly that reason. The label carries `req.baseUrl + req.path`, which is the route and nothing
else.

## The scope gate that becomes effective

`ALLOWED_LOOKUP_ROLES` (`:180`) is `['ISSUER_ADMIN','ORG_ADMIN','SYSTEM_ADMIN','SUPER_ADMIN']`, and
a connector token's claims carry `role: 'connector'`, which is not in it. `hasUsersReadScope`
(`:223-228`) accepts `*`, `users:*` or `users:read`. So a connector **without** `users:read` is
refused 403 by scope, which is the 401-to-403 correction this change is for.

## Cells, and why they are not vacuous

New: `services/auth/src/__tests__/ks1402-lookup-accepts-connector-token.test.ts` (+183).

| cell | at base | at head |
|---|---|---|
| 1 a connector token WITH `users:read` reaches the handler | 401 — RED | 200, user resolved |
| 2 a connector token WITHOUT `users:read` | 401 — RED | 403 `FORBIDDEN` |
| 3 an interactive ACCESS token still works (control) | 200 — GREEN | 200 — GREEN |
| 4 tenant-A connector reading a tenant-B-only email | 401 — RED | 404 `USER_NOT_FOUND` |

Red-first at the base with the product untouched: **3 failed / 1 passed of 4, rc 1**, each red an
assertion — `expected 401 to be 200`, `expected 401 to be 403`, `expected 401 to be 404`. Three
reds *and* a pass, so it is a real red rather than the 0-passed-0-failed shape a load failure
produces. Green after: **4 passed / 4**.

**The trap these cells avoid.** `auth.integration.test.ts:1398` and `:1419` already assert 200 on
this route for a caller with `role: 'connector'` plus `users:read` / `users:*`, and they pass **at
the base** through the real middleware. They pass because `mintTokenForSession` (`:1239-1252`)
signs **`type: 'access'`** and carries `role: 'connector'` only as a claim. An access token wearing
the connector role was never what was refused, so a cell built that way would be **green at base**
while looking exactly like a passing red-first proof. These cells mint a real `type: 'connector'`
token with the jwt service's own `generateConnectorToken`, which is the only shape `authenticate()`
turns away. The cells do **not** mock `../middleware/authenticate` — only the repo, session and
logger layers — so the authenticator under test is the real one.

## The gateway is not touched

`services/api-gateway/src/routes/proxy.ts:461-466` already routes `/api/users/lookup` through
`authenticateToken(true)`, `attachScopes` and `requireScope('users:read')` for `sk_` callers, but
the KS-1402 path does not pass through it: originate calls auth directly at
`services/originate/src/routes/documents.ts:1667-1671`, with the caller's own `Authorization`
header. No gateway change is needed or made.

## Skill §4 — both platform-k documents, in this commit

Per `.claude/skills/secuura-test-discipline` §4 ("every test change updates its platform's two HTML
docs, in the same commit — not a follow-up"), this PR adds one new, self-contained per-ticket block
to each:

- `Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html` — **+108/-0**,
  a new section *9. Auth surface — connector tokens on the users routes*.
- `Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html` — **+28/-0**, a new
  `sec-head` + `baseline` block under the same title.

**Zero lines removed from either document.** Both blocks are inserted at top level immediately
before the document's closing block, so neither shares a hunk with an existing table. Before this
commit both documents had **0** hits for `lookup`, `connector` and this ticket's key (must-hit
control: `auth` 52 hits in the flow diagrams, 59 in the cheat sheet), so this is genuinely new
content rather than a line edit.

**Timings — no row is touched, and that is a measurement, not an omission.** §4 makes stale timings
a defect, so the question is which stated figure covers the suite this PR changes. Grepped at the
base SHA, in **both** documents: `services/auth` **0** hits, `services/transfer` **0**,
`generate-openapi` **0**, `check:openapi` **0** — against the must-hit control above. The single
`vitest` hit in each document is a `setupFiles` note in the Performance harness, and the four
`unit suite` hits in each are about slot independence; all ten lines were read, not inferred from
the counts. **So no tier budget or timing row covers the auth vitest suite, none is updated, and
none is left looking re-measured.**

§4 also requires that a change to what runs owns a measurement with a date and a host. The one
figure this change owns is stated in both blocks in prose — deliberately **not** as a new table
row: **78 files / 840 tests in 2.51–2.55 s reported (3.31–3.43 s wall) over three consecutive runs,
2026-10-04, host `Kamils-Mac-Studio` (Apple M3 Ultra, 28 logical cores)**. That is a developer
workstation and explicitly not a CI figure; §4's own warning is that a figure without a host is
meaningless.

## 🔴 One of the two product files is covered by no test

Stated here rather than left for a reviewer to find. **`middleware/authenticate.ts` is exercised by
nothing in this PR.** Reverted on its own with `routes/users.ts` left at this head, the whole
`services/auth` suite stays green at **78 files / 840 tests** and all four cells pass.

What it changes is live rather than cosmetic: the connector-accepted audit line's text
(`'users/stub: connector token accepted (KS 564)'` → `'connector token accepted (KS 564, KS 1402)'`)
and a **new `route` field** — and that applies to **both** `/stub` and `/lookup`, so an existing
route's audit output changes too. No assertion reads the logger, so no cell can see it. The
route-neutrality argument above is therefore measured and argued, **not test-guarded**. No logger
assertion was added: that is scope this branch does not carry, and the audit surface's consumer is
Platform S.

## Provenance of this branch

Branch name and the three code paths are **Seat B 55th's**; **Seat B 56th** rebased the commit onto
`e6daa806e79a` (PR 0, the unfreeze) without changing it — the sha256 of its diff against its parent
was identical before and after; **Seat B 57th** installed, re-verified both sides on the new base,
authored the §4 doc blocks, amended them into this one commit and pushed it. The amend rewrote the
commit, so 0 trailers was re-proved on the rewritten head against a control that prints 55 bytes,
and the sha256 of the diff restricted to the three code paths is `e3e843daf653ff6de35b7269` both
before and after the doc step — the documentation changed no code byte.

## Test Evidence

**Touched:** `services/auth` — `routes/users.ts`, `middleware/authenticate.ts`, and the new test.

**Ran (local, by me, at head `aa16f3256dbf`):**
- `services/auth` full suite, `npx vitest run`: **78 files / 840 tests passed, 0 failed, rc 0**.
  Baseline at the base was 77 / 836 — so +1 file and +4 tests, exactly these cells, and 0 new reds.
  (`npm test` in this service is `vitest` in WATCH mode and never exits; `npx vitest run` is the
  command.)
- Red-first and green-after as tabled above.
- `tsc --noEmit` for `services/auth`: head rc 0, 0 errors; base rc 0, 0 errors — **equal, a
  no-regression reading only**.
- `npm run check:openapi`: **rc 0** (405 example blocks, every published example resolving). It
  proves this PR moved no spec: `docs/openapi/secuura-api.yaml` is byte-identical to the base at
  blob `1ffd687b8a9d`.
- `git diff --name-only e6daa806e79a` against this head: exactly the 5 declared paths, no
  `*.openapi.ts`, no YAML, no lockfile, no manifest, no `audit-baseline.json`, nothing under
  `services/timestamping/`, and no platform-s doc. Asserted by a gate that also re-applies the
  same filters to PR 0's own diff and refuses unless that returns 4 — a zero from a filter that
  cannot fire is not a measurement. 5/5 assertions pass, both controls firing.

**NOT run:**
- No live S+K pair run. The refusal is reproduced from K's own harness, not against a running S.
- **Whether Platform-S's connector key carries `users:read` today is not measurable from K's
  side.** S needs it for the transfer to succeed. Without it S moves from **401** to **403** —
  still a refusal, but the correct one. Stuart will need to confirm the key's scopes.
- No Schemathesis, no Akto, no Playwright, no k6.
- `services/auth/tsconfig.json` excludes `src/__tests__`, so **`tsc` never type-checks the new
  test**.
- **Skill §5f: no live sweep.** §5f requires a runtime-behaviour change to have a live sweep on the
  correct host against a torn-down and rebuilt environment before Done. **That has not been done
  and this PR does not claim it.** No ticket moves to Done on this PR's account.
- The push's own preflight, quoted exactly as it printed:
  `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` The 3 skips are the
  stack-dependent legs: the local stack is not up and the Docker daemon is not running (verified —
  the Docker API socket is absent). The preflight itself says an incomplete run is **not** a pass,
  and it is not quoted here as one. `push rc=0`, one push, bare, no `--no-verify`, 6 m 07 s.
- No deploy. kintsugi is Kam's tap.

**Migrations + config:** none. No migration, no env var, no config default changed.
