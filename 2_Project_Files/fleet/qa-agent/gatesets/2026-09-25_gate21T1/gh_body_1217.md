#1217 KS-976 MSG400: the /reset 400 names the field that actually failed
head e83f344474028215ae827b2f74fd3a06566d4c23

## What changed

`POST /api/rate-limit/reset` answered **every** schema refusal with the constant top-level message
`'Key required'`. The QA tier-1 gate on #894 measured three refusals where the key was supplied and fine —
a blank, an unpaired-surrogate and an overlong `tenantId` — each answering "Key required" while `details`
named `tenantId`. KS-970 item 6 had just published *"Refused with 400 if present but blank"* for that
field, so the contract promised a refusal whose top-level message named a **different** field.

Charter §4d: a 4xx must not be scored as a healthy rejection without knowing *why* it was returned, and
this message actively misled about the why.

The message is now **derived from the first failing path** (`Invalid request body: <path> <zod message>`),
falling back to the generic `Invalid request body` for a path-less issue. **`details` is untouched** and
remains the authoritative, parseable half — the fix reads *from* it rather than inventing a second source
of truth. The helper lives in its own module because `index.ts` calls `app.listen()` at module load.

**Scope held to the ticket.** Only `/reset`'s 400 changes: `/check`'s 400 already says the generic
`'Validation failed'`, and the two **correct** "Caller has no tenant" sites (the ones testing the tenant
claim directly) are untouched — the hazard the ticket warned about.

Item 2 of KS-976 was closed by #1199 (`d53520f57`). This is item 1, the only half left open.

## Two corrections to the ticket, both measured at develop `6ab9d5021e96`

1. **The site is `index.ts:1476`, not `:1358`.** The line moved; the defect did not. `'Key required'`
   occurs **exactly once** in `services/security`.
2. **The ticket's quoted detail is stale.** It quotes `must not be blank` for a blank `tenantId`. That is
   no longer what the schema produces: **KS-974 item 2 (#1198, `a314a9bc8`, 2026-09-22) added `.trim()` to
   `scopeField()` after KS-976 was filed**, so a whitespace value is trimmed to `''` and caught by
   `.min(1)`, reporting zod's default string. Measured across 8 unusable shapes, `'must not be blank'`
   fires on **0** of them; the control (the same refine with `.trim()` removed) fires, so the instrument
   works — the refine is now **unreachable**. Recorded on KS-974 (comment `c291300c`), not fixed here: the
   decision it needs (keep `.trim()` or keep the message) belongs to the PR that takes it.
   **The issue `path` is still `['tenantId']`, which is all this fix reads**, so the defect and the fix are
   unaffected — and the cells here pin the **path**, never that text.

## Test Evidence

**Touched:** `services/security/src/index.ts` (one changed response line + its comment);
`services/security/src/requestRefusal.ts` (NEW, pure);
`services/security/src/__tests__/ks976a-reset-400-names-the-failing-field.test.ts` (NEW, 10 cells — 7 at the
wire through the `SECURITY_DISABLE_BOOT` seam, 3 pure).

**Ran (locally, by the author, BARE and SERIAL — `npx vitest run --no-file-parallelism`):**
- `services/security`: **bare 229/229 over 21 files → patched 239/239 over 22 files** (+10 = the cells
  added). **0 failures either side.**
- `npx tsc --noEmit` in `services/security`: **rc 0** before and after.
- **Red proof**, taken with the new helper module PRESENT (so the file still LOADS) and only the **call
  site** read back out of the object store: **4 failed / 6 passed at develop**, exactly the four RED cells,
  **every control green at develop**. With the call site applied: **10/10 green**.
- Cells assert the message **TEXT**, not the status. Every cell here passes on status alone — a 400 is a
  400 whatever it says — which is why the defect shipped.

**NOT run:** preflight legs **3, 4 and 8** — `SKIP — local stack not up on http://localhost:6882`;
`PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` **Legs 3/4/8 are OWED at the gate**:
this changes a **response message** on a live route. The four platform suites (Schemathesis · Akto ·
Playwright · k6) were **not run** — the local stack is not up this round by fleet rule.

**Migrations + config:** none. No migration, no env var, no dependency change. **`docs/openapi/` untouched**
— verified: `'Key required'` appears nowhere in `docs/`, while the route itself does, so the instrument
discriminates. The message is not published.

Refs KS-976

🤖 Generated with [Claude Code](https://claude.com/claude-code)

