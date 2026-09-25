#1224 KS-1179 DNSTIMERFIN: clear the DNS timer on the rejecting exit, and correct two docblocks
head d4862b3eee3566635c61cf9d0b810131140e4fa2

## BLUF

Three findings from the KS-932 tier-1 gate, all in `packages/shared`, one logical path.

* **F-6** — `clearTimeout(dnsTimer)` sat **after** the `await` on the resolve race, so a rejection threw straight past it and left the timer armed for the whole `timeoutMs`, holding the event loop open after the caller had its answer. Moved into a `finally`.
* **F-4** — the `blocked` docblock listed **two** ways to reach it; the DNS deadline is a **third**, and it arrived with the shared budget without the list following.
* **F-5** — the `timeoutMs` docblock still said *"DNS-free connect"*. DNS is inside the budget now.

Touches product code (`src/security/ssrf-guard.ts`) plus one new test file. **Tier 1.**

## Reaching F-6 at all — measured, not assumed

This is the part worth reviewing. `resolvePublicAddresses` **catches every `lookup` failure** and returns `{ ok: false }`, so a DNS error **cannot** reject it.

**A test that mocked `dns/promises` to reject would have proved nothing** — it would have exercised the *settling* path and passed whether or not the fix was present.

The reachable rejection is `isIP`. It is called **before** that try, and `Promise.race` evaluates its array left to right: `resolvePublicAddresses(...)` is invoked first, runs synchronously as far as `isIP`, and a throw there rejects the race **after** the timer arm has been constructed. The regression cell drives exactly that seam, and the file's header explains why it mocks `net` rather than `dns/promises`.

## The cell checks itself

It asserts the timer was **armed** before it asserts it was cleared. If the seam ever fires too early, "it was cleared" would be vacuously true — so that case is made a loud red instead. **Proven**, not claimed: with the seam firing on the first `isIP` call, the failure is

```
AssertionError: the DNS timer must have been ARMED before we can claim it was cleared:
expected "setTimeout" to be called at least once
```

A CALIBRATION cell pins how many `isIP` calls the hostname sees before the resolve, so a refactor that changes that ordinal reds with a number rather than silently moving the seam to the wrong call.

## A defect I introduced and removed

My first settling-path control resolved to `203.0.113.7` and let the request run. It **hung past the cell's own timeout** — because depending on TEST-NET-3 blackholing is *precisely the ks932 **F-2** defect this ticket was filed about*. Rewritten to resolve to a **private** address: the guard refuses before opening a socket, and the cell is network-free at **147 ms**.

## Tamper matrix

Baseline 3 passed; both files restored byte-exactly (sha256 match).

| # | tamper | measured |
|---|---|---|
| T-1 | revert the fix — `clearTimeout` back after the `await` | **1 failed** |
| T-2 | the seam never throws (so the reject arm is never driven) | **1 failed** |
| T-3 | the seam fires **before** the timer is armed | **1 failed** — the self-check, with its own message |

## Test Evidence

**Touched**
- `Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts` — product code: `finally`, and two docblocks.
- `Blockchain/Dev/packages/shared/src/__tests__/ks1179-dns-timer-cleared.test.ts` — new.

**Ran** (worktree at develop `6ab9d5021e96` + this commit, `npm ci` rc 0)
- `npx vitest run --no-file-parallelism` in `packages/shared` → **47 files, 921 passed (921), rc 0**. **bare 918 / patched 921** (+3 = the new file's three cells).
- `npx tsc -p packages/shared --noEmit` → **rc 0**.
- `npm run lint -w packages/shared` → **36 problems (1 error, 35 warnings) — identical to bare.** The 1 error is the pre-existing `no-control-regex` at `src/middleware/index.ts:521`.
- the three tampers above.

**NOT run**
- **Push-preflight legs 3, 4 and 8.** The hook ran **12/15; 3 SKIPPED (local stack not up); nothing failed**, and says *"This is NOT a pass. Do not quote it as one."* It is not quoted as one. This change has **no route, spec, served-spec or runtime-config surface**: `safeOutboundRequest` is a library function and no route or spec is touched.
- The four platform suites (Schemathesis · Akto · Playwright · Performance/k6) — same reason.
- Any service unit suite. `safeOutboundRequest`'s callers in `services/*` are **not** modified; its signature, return type and every existing behaviour are unchanged — the `finally` only moves when an existing `clearTimeout` runs.

**Migrations + config**
- None. No migration, no `package.json`, no `tsconfig`, no lockfile, no env var.

---
*Gate note, verbatim:* `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed. legs 3 4 8 — local stack not up … This is NOT a pass.` Head `d4862b3eee3566635c61cf9d0b810131140e4fa2`.

Refs KS-1179

🤖 Generated with [Claude Code](https://claude.com/claude-code)
