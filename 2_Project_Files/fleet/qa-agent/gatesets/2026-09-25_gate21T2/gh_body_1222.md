#1222 KS-1181 CANARYHIT: the ks727 canary cells witness that the handler answered
head 9bce90229ad60b4ab988248648530b3b9a0d951d

## BLUF

The KS-727 corpus-1 canary cells could not witness that the handler was hit. A handler that **throws** never answers: express skips to the terminal backstop, which writes a **constant** body, so no canary appears and *"does not return the thrown message"* passes while the handler under test did nothing at all.

**One file. Test-only. No product code, no config, no dependency, no lockfile.**

## The red-proof — the gate's G5, exactly as KS-1181 frames it

Tamper: `packages/shared/src/errors/error-handler.ts` (in lane) made to throw before it answers.

| test file | result for that handler |
|---|---|
| **develop's**, at `6ab9d5021e96` | **1 failed / 8 passed** — only the authored CONTROL reddened. The six NODE_ENV cells, plus payload-size and details, stayed **GREEN** with the handler never running. |
| **this PR's** | **9 failed / 0 passed** |

**Eight vacuous greens → zero.** Both files restored byte-exactly afterwards (sha256 match on the test file *and* on `error-handler.ts`).

## Grounded on measurement, not assumption

Before a single assertion was written, a throwaway probe printed `forwarded` for all ten handlers across all three canary shapes:

| handler class | generic | oversize | details |
|---|---|---|---|
| the nine answering handlers | false | false | false |
| `payloadTooLargeErrorHandler` (the one filter) | **true** | **false** | **true** |

So generic and details assert `forwarded === shouldForward`; **oversize asserts `false` for all ten**, because the filter recognises `entity.too.large` and *answers* it. Pinning oversize to `shouldForward` would have been **wrong for the filter** — and I would only have discovered that by watching a test fail, which is the moment one is most tempted to weaken it instead.

Worth noting: the oversize cell's existing comment anticipates handlers forwarding that shape. **None does today.** The `false` pin therefore reds deliberately if one ever starts — a changed disposition is a finding, not an absorbed change.

## The 0-hit control

A synthetic throwing handler must read `forwarded === true`. Without it, `expect(forwarded).toBe(shouldForward)` would be a claim about a value nothing had shown could differ.

## Tamper matrix — on the untampered tree

Baseline **104 passed**; file restored byte-exactly.

| # | tamper | measured |
|---|---|---|
| T-1 | `shouldForward` hard-coded `false` | **8 failed** |
| T-2 | the 0-hit control expects `false` | **1 failed** |
| T-3 | the oversize pin flipped to `true` | **10 failed** |
| T-4 | `driveThroughRoute` always reports `forwarded: false` | **9 failed** |

**T-1 would not apply on the first attempt**, and that was the useful part: `shouldForward` matched **twice**, because the authored CONTROL cell still computed its own copy, shadowing the one hoisted into the describe. Harmless while the two agreed, and exactly the duplicate that stops agreeing later — my own comment claimed it was "read once", which was not yet true. One declaration now; T-1 then reddened 8 cells. Found by the harness refusing to apply, not by reading.

## Test Evidence

**Touched**
- `Blockchain/Dev/packages/shared/src/__tests__/ks727-errorhandler-class-guard.test.ts` — the only file.

**Ran** (worktree at develop `6ab9d5021e96` + this commit, `npm ci` rc 0)
- `npx vitest run --no-file-parallelism` in `packages/shared` → **46 files, 919 passed (919), rc 0**. **bare 918 / patched 919** (+1 = the 0-hit control; the F2 assertions strengthen existing cells rather than adding new ones).
- `npx tsc -p packages/shared --noEmit` → **rc 0**.
- `npm run lint -w packages/shared` → **36 problems (1 error, 35 warnings) — identical to bare.** The 1 error is the pre-existing `no-control-regex` at `src/middleware/index.ts:521`, recorded in `BACKLOG.md`.
- the G5 red-proof and the four tampers above.

**NOT run**
- **Push-preflight legs 3, 4 and 8** — the hook ran **12/15; 3 SKIPPED (local stack not up); nothing failed**, and says *"This is NOT a pass. Do not quote it as one."* It is not quoted as one. This PR has **no route, spec, served-spec or runtime-config surface**, so those legs have nothing to say about it.
- The four platform suites (Schemathesis · Akto · Playwright · Performance/k6) — same reason.
- Any service unit suite other than `packages/shared`. `services/*` error handlers are **imported and driven** by this suite and are **not modified**; `packages/shared/src/errors/error-handler.ts` was tampered and restored byte-exactly during the red-proof.

**Migrations + config**
- None.

Refs KS-1181


---
*Gate note, verbatim:* `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed. legs 3 4 8 — local stack not up … This is NOT a pass.` Head `9bce90229ad60b4ab988248648530b3b9a0d951d`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
