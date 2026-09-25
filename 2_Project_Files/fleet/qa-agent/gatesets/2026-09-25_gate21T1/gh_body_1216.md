#1216 KS-975 SCOPENULL: explicitScope treats an explicit null body field as MALFORMED
head c44b15dddaddac3dec1d4deff224efd01b7565f2

## What changed

`explicitScope` treats an explicit `null` in the `/api/rate-limit/reset` body as **MALFORMED**, not ABSENT.

Before, a body `{"tenantId": null}` fell through `claim()` as ABSENT, `named` was false, and the call
returned `principalScope(caller)` — **a present field silently retargeting the caller's own rate-limit
bucket**. That is KS-975 item 1's exact shape, one field over, and `null` is precisely what a client library
serialising an unset field sends.

The fix is deliberately asymmetric, because the ticket's fix-shape is:

> `explicitScope` should treat `null` in a body as MALFORMED while `principalScope` keeps treating a `null`
> claim as ABSENT — different questions about different inputs.

So a new body-side `bodyClaim()` wrapper is added and `explicitScope` reads through it. **`claim()` itself is
unchanged and `principalScope`'s two calls to it do not appear in the diff at all.** An OMITTED field
(`undefined`) still falls back to the caller's own scope — that fallback is the documented `/reset`
capability, not a defect, and `undefined` and `null` now differ.

**Honestly bounded, and unchanged by this PR:** `scopeField()` is a non-nullable `z.string()`, so the schema
refuses `null` first and this arm is **not reachable at the wire today**. It is a hole in the BACKSTOP — and
the backstop exists for a caller that bypasses the schema, which is the only reason its second line exists.

Item 1 of KS-975 was closed by #1161 (`a1931d2f3`). This is item 2, the only half left open.

## Test Evidence

**Touched:** `services/security/src/rateLimitScope.ts` (+1 wrapper, 2 changed call lines, 2 comment blocks);
`services/security/src/__tests__/ks975b-explicitscope-null-body-field-is-refused.test.ts` (NEW, 8 cells).

**Ran (locally, by the author, BARE and SERIAL — `npx vitest run --no-file-parallelism`):**
- `services/security`: **bare 229/229 over 21 files → patched 237/237 over 22 files** (+8 = the cells added).
  **0 failures either side.**
- `npx tsc --noEmit` in `services/security`: **rc 0** before and after.
- **Red proof**, taken with the test file present and the product bytes read back out of the object store
  (so the module still LOADS — a module-not-found reds every cell with no message and proves nothing):
  **4 failed / 4 passed at develop**, being the three RED cells plus the undefined-vs-null discrimination
  cell, with **every true control green at develop**. With the product bytes applied: **8/8 green**.

**NOT run:** preflight legs **3, 4 and 8** — `SKIP — local stack not up on http://localhost:6882`, three
skip lines, `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` Nobody starts the platform
stack mid-round (five seats share the machine; the Docker daemon is down); it comes up once at the batch QA
gate. **Legs 3/4/8 are OWED at the gate**: this changes the refusal behaviour of a route, though as stated
above the arm is not reachable at the wire today, so the leg is owed on the module rather than on an
observable route change. The four platform suites (Schemathesis · Akto · Playwright · k6) were **not run**
for the same reason.

**Migrations + config:** none. No migration, no env var, no config change, no dependency change. `docs/openapi/`
untouched.

## Not in this PR

`principalScope`'s treatment of a `null` token claim (unchanged, and pinned by a control here).

Refs KS-975

🤖 Generated with [Claude Code](https://claude.com/claude-code)

