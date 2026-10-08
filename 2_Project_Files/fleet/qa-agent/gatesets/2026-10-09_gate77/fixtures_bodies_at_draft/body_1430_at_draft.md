Refs KS-1328
https://linear.app/secuura/issue/KS-1328

Raised from a Wednesday-held Spark pass, re-proved by Seat F 5th on develop `0a6177ea5482`.

## What this does

`services/kyc/src/__tests__/db.retry.test.ts` exceeded vitest's 5 s default under fleet load: its first cell timed out at **11498 ms** while passing in **675 ms** when run alone, so the overrun is scheduling, not work (the KS 1155 class). This puts `{ timeout: 60_000 }` on **that describe only**, so every other kyc suite keeps the 5 s default, and adds a cell asserting all 6 cells in the file carry the 60 s budget — so the budget cannot be removed silently.

**Test-only: no product code changes.** Three files: the suite plus both platform-k documents, in the same commit.

## What it pins, and what it does NOT

- It pins **the budget**, not the absence of future timeouts. A slower or busier machine can still exceed 60 s.
- **The load was NOT reproduced in this seat.** That 60 s absorbs an 11498 ms overrun is arithmetic on the 2026-09-26 measurement, not a fresh one.
- The 6-cell count is deliberate: add a cell to this file and the assertion goes red until it is updated.

## Test Evidence

**Touched:** `Blockchain/Dev/services/kyc/src/__tests__/db.retry.test.ts` · `Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html` (flow block `43.`) · `Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html` (cheat section `KS-1328`).

**Ran** — kyc's own npm script (`npm test` = `vitest run`), in this PR's worktree at this head:

| run | Test Files | Tests | rc |
|---|---|---|---|
| **RED** — `{ timeout: 60_000 }` tampered out of the describe | 1 failed \| 5 passed (6) | **1 failed \| 33 passed (34)** | 1 |
| **GREEN** — as shipped | 6 passed (6) | **34 passed (34)** | 0 |

The red fails on `AssertionError: expected 5000 to be 60000` — an assertion, not a load error. The tamper removes exactly the one thing the new cell asserts.

Toolchain read from this worktree, not assumed: node **v24.7.0** · npm **11.5.1** · vitest **4.1.11** · bash **3.2.57(1)-release**.

Gates: `docblockra3` 0 failed (flow 30 → 31 blocks, tail `26.` → `43.`; cheat 19 → 20 sections, tail `KS 1164` → `KS-1328`; byte-for-byte the only change from the base blob, and a 1-byte-altered fragment fails the same comparison). Path gate PASS with 3/3 controls correctly failing. Commit carries **0 `Co-Authored-By`** trailers, verified against a control commit that does carry one.

**Preflight on this push:** `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` **This push's own output does not name WHICH three legs skipped**, so they are recorded here as *3 SKIPPED, unnamed by this push's output* rather than attributed to specific leg numbers.

**NOT run:**
- **The four platform suites — Schemathesis, Akto, Playwright, Performance/k6 — are UNMEASURED.** No local stack in this seat. Only the SKIP lines this push printed are quoted; none of them is a pass.
- The original timeout under real fleet load is not re-measured.
- No other kyc or service suite was run beyond the kyc package.

**Migrations + config:** none. No dependency, lockfile, manifest, baseline or spec-version change. No `.env`. No migration.

## Notes for review

- `KS-1328` was **unassigned at raise**; this seat makes no board write.
- A runner trap worth knowing: `--reporter=basic` does not exist in **vitest 4.1.11**. Passing it exits **rc 1 having run zero tests** (a `Startup Error`). An rc of 1 with no `Tests` summary line is a load failure, not a red — check for the summary line before calling any run red.
- The ticket does **not** move to Done: a runtime-behaviour claim is not closed on offline green.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
