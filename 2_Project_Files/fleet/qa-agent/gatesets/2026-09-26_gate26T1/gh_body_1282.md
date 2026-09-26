#1282 KS-730: stop returning the thrown message from systemErrors 500s
head 34a67a9e48057a0d4939527a4b721a7a5605e4ab

## What

**First of three PRs by file**, on the ruling to split KS-730's originate half per file with `systemErrors.ts` first.

Four inline handlers in `routes/systemErrors.ts` returned `err.message` verbatim unless `NODE_ENV === 'production'`, so **`development`, `demo`, `test` and an UNSET `NODE_ENV`** all answered an admin route with raw internal text. KS-727 fixed the two *shared* handlers the same way; these are part of the per-route remainder it enumerated rather than folded in.

| route | site at `d7cdecf1d2ee` |
|---|---|
| `GET /api/system-errors/stats` | `:140` |
| `GET /api/system-errors` | `:162` |
| `PATCH /api/system-errors/:errorId/resolve` | `:172` |
| `POST /api/system-errors/resolve-by-service` | `:188` |

## 🔴 The fix is NOT subtractive here, and that measurement shaped it

KS-727 could simply delete its ternaries because the shared handlers **already logged** `err.message` and `err.stack` at entry — the change lost nothing. Across the three originate files this ticket enumerates, **0 of 65 sites log the error before returning it.** Measured by walking back from each match to its enclosing `catch` and looking for `logger.error|warn|info` in between, against a control that finds **23** `logger.*` calls in a sibling file and 0 for a nonsense pattern.

So deleting the ternary alone would **destroy the diagnostic at every site**. The ticket anticipates this ("where a site does not log, add the log in the same change") but reads as if it were a handful; it is all of them. The log is added in the same change, through **one small local helper** — the ticket's own suggested shape ("a small local helper rather than 67 edited ternaries"), and the only one in which 65 such edits stay reviewable.

Each call site passes **its own context string naming the route**, so a log line is attributable without trusting the caller about which handler produced it. The cells assert that context as a **value**: a helper logging one constant string would satisfy a looser check and make every route's log indistinguishable.

## #1182's two ingest routes are deliberately NOT refactored

They already log inline with their own context strings — verified at source: **2** inline `logger.error` calls, **4** `fail500` call sites. Rewriting an already-merged fix to share a helper is a change with no defect behind it. A red arm confirms the asymmetry rather than leaving it implied: removing the helper's log reds **all four** new log cells and **neither** of #1182's.

## Re-swept to zero

**0 live response-side `NODE_ENV === 'production'` sites remain in this file**, excluding comments and log lines, with the excluded mentions counted separately (1) so the sweep is shown to be able to see lines at all.

## Test Evidence

**Touched:** `services/originate/src/routes/systemErrors.ts` and `services/originate/src/__tests__/ks730a-ingest-500-never-answers-err-message.test.ts` (an existing cell file extended, not a new one added).

**Base:** this worktree contains develop `d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9`.

| arm | result |
|---|---|
| originate BARE (both files restored pre-edit, sha256-verified) | **878 passed / 878, 74 suites**, rc 0 |
| originate PATCHED | **889 passed / 889, 74 suites**, rc 0 (+11 cells) |
| `packages/shared`, `npx vitest run` | **941 passed / 941, 48 files**, rc 0 |
| `tsc --noEmit` in `services/originate` | rc 0 |

**Five red arms, each isolating one thing:**

| arm | what is reverted | cells that red |
|---|---|---|
| R1–R4 | the original ternary at **one** site | exactly that route's A5 + A6 (15 passed / 2 failed each) |
| R5 | the helper's `logger.error` call | all four A6 cells (13 passed / 4 failed), and **neither** of #1182's |

Four site arms rather than one, because four call sites are four claims — and the whole reason KS-730 exists is that KS-727 fixed the shared handlers and left the inline ones behind. A single arm reverting all four would measure the helper, not each route's wiring to it.

⚠ **R5 took three attempts, and the class is worth naming.** Deleting the log line orphaned **three** identifiers in turn — `logger`, then `context`, then `err` (TS6133) — and each time `tsc` refused the file, so the suite never ran, reds nothing, and looks exactly like an inert tamper. Voiding them one at a time just moved the error; the reliable form is to reference **every** identifier the deleted line used. The runner's `LOADFAIL` verdict (0 passed **and** 0 failed) is what kept this from scoring as a pass. **Sixth instance of this class in this session.**

⚠ **And R5's first expectation was wrong, not the code.** It expected #1182's two ingest cells to red as well; they did not, because those routes log inline. The expectation was corrected and the fact corroborated at source, rather than the arm being loosened.

**NOT run / NOT covered:**
- **Legs 3, 4 and 8 NOT run** (local stack not up): `12/15 ran; legs 3, 4, 8 NOT run (local stack not up)`. No spec moves, so no LEG-8-PORT reading.
- **This is one file of three.** `gdpr.ts` (15 sites) and `adminConfig.ts` (46) follow as separate PRs; the api-gateway and tokenisation sites are held surfaces and not in this round.
- The cells drive the router on a loopback listener with the service layer mocked. They prove the **response and the log**, not that any real error path produces these particular throws.

Refs KS-730

🤖 Generated with [Claude Code](https://claude.com/claude-code)

