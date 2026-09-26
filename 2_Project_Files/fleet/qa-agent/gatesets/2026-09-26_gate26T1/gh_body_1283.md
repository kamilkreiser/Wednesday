#1283 KS-730: stop returning the thrown message from gdpr 500s
head f92b7c19e98d888b39674eb0b39461ed214a37d3

## What

**Second of three PRs by file.** Fifteen inline handlers in `routes/gdpr.ts` returned `err.message` verbatim unless `NODE_ENV === 'production'`, so **`development`, `demo`, `test` and an UNSET `NODE_ENV`** all answered a GDPR route — consent, DSRs, exports, erasure, retention, the deletion log — with raw internal text.

All fifteen now go through one local `fail500(res, context, err)` that logs first and returns the constant body, each call site passing **its own context naming the route**. Re-swept to zero, excluding comments and log lines: **0 live ternaries, 15 helper calls, 15 distinct contexts.**

## 🔴 A constraint in this file had to be measured before it could be set aside

A comment in `gdpr.ts` states there is **deliberately no logger import**, because `utils/logger` pulls in `config.ts`, which throws at module load when `DATABASE_URL` is unset — and that importing it kills three unit suites before a single test runs ("an import-throw reads as a clean zero"). My fix needs to log, so that constraint was directly in the way.

**The constraint was real. Its stated mechanism is not true at this commit.**

| claim | measurement |
|---|---|
| `utils/logger` pulls in `config.ts` | **False.** `utils/logger.ts` imports `winston` and nothing else. |
| importing it throws with `DATABASE_URL` unset | **False.** Importing it with `DATABASE_URL` **and** `JWT_SECRET` both deleted **succeeds**. |
| importing `routes/gdpr` unmocked throws | **True** — `DATABASE_URL environment variable is required`, from its own graph reaching `config.ts` by another path. Unchanged by adding a winston-only import here. |

The only thing that could have refuted this is the suites that import this router. **All six run and pass: 78/78** (`ks754`, `ks694`, `ks444-gdpr-dsr-update-withdraw-guards`, `ks431`, `ks445`, `ks1029`) — none of which sets `DATABASE_URL` itself.

**The comment is corrected in place rather than contradicted silently**, so a reader who finds the import also finds the measurement that licensed it.

## Two kinds of cell, and the difference is stated rather than blurred

- **Four behavioural cells** drive routes end to end over a loopback listener and read the real 500 body and the real log call. They are the strong evidence, and they cover **four of fifteen**.
- **One source cell** pins all fifteen by construction — zero live ternaries, fifteen helper calls, fifteen **distinct** contexts. It is **weaker**: it reads the file rather than the behaviour, and it exists because driving fifteen routes would need fifteen service mocks for no additional discrimination.

## ⚠ My first four routes were measuring my own fixtures

`POST /consent` and `PATCH /dsr/:dsrId` validate a zod body and a UUID **before** calling the service. My fixtures did not satisfy them, so each was refused **400** and the service never threw — the cells were grading my test data, not the handler. Replaced with four routes that reach their service with nothing to satisfy first, verified at source: `GET /dsr/pending`, `GET /retention`, `GET /deletion-log`, `GET /consent/check`.

## Test Evidence

**Touched:** `services/originate/src/routes/gdpr.ts` and a new `services/originate/src/__tests__/ks730b-gdpr-500-never-answers-err-message.test.ts`.

**Base:** this worktree contains develop `d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9`.

| arm | result |
|---|---|
| originate BARE (`gdpr.ts` restored, the new cell file moved aside) | **878 passed / 878, 74 suites**, rc 0 |
| originate PATCHED | **890 passed / 890, 75 suites**, rc 0 (+12 cells) |
| the six suites that import `routes/gdpr`, run together | **78 passed / 78, 6 suites**, rc 0 |
| `packages/shared`, `npx vitest run` | **941 passed / 941, 48 files**, rc 0 |
| `tsc --noEmit` in `services/originate` | rc 0 |

The `gdpr.ts` restore after the bare arm was asserted by sha256.

**Five red arms:**

| arm | what is reverted | cells that red |
|---|---|---|
| R1–R4 | the original ternary at **one** driven site | that route's B1 + B2, **plus the source cell** (9 passed / 3 failed each) |
| R5 | the helper's `logger.error` call | all four B2 cells (8 passed / 4 failed) |

The source cell reds on every site arm too, and that is listed in each expectation rather than left as an unexplained extra red.

⚠ **R5's anchor found 0 matches on the first run and the runner STOPPED rather than tampering something else** — `gdpr.ts` indents with two spaces where `systemErrors.ts` used four. That is the unique-anchor rule doing its job; a runner that fell back to a fuzzy match would have tampered a line I did not choose.

**NOT run / NOT covered:**
- **Legs 3, 4 and 8 NOT run** (local stack not up): `12/15 ran; legs 3, 4, 8 NOT run (local stack not up)`. No spec moves.
- **Eleven of the fifteen routes are covered by the source cell only**, not behaviourally. Stated above rather than implied by a single count.
- The cells prove the response and the log. They do not prove that any real error path produces these particular throws.
- `adminConfig.ts` (46 sites) follows as PR 3. The api-gateway and tokenisation sites are held surfaces and not in this round.

Refs KS-730

🤖 Generated with [Claude Code](https://claude.com/claude-code)

