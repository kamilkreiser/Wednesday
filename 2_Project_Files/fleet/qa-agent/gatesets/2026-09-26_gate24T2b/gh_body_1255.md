#1255 KS-1301: port the presence-not-truthiness pin to sign-cert and sign-wallet
head 59245ff0b11c6b760ba5e2a9daedc5927e915e10

## BLUF
Test-only. #1237 pinned that the relabel guard keys on **presence, not truthiness** — but on `/version` alone. The same guard is written **byte-identically at three call sites** in `routes/documents.ts`, and the other two had no cell holding them to it. Ported, one describe per route, with a red arm per route proving isolation.

## Why this half is the interesting one
A truthiness bug here is invisible to ordinary testing: `null`, `''` and `false` all *look* absent to an `if (!documentType)` check while being **present** in the request. That is exactly the confusion #1237 proved `/version` does not have — so the guard that was hardest to get right was the one with no coverage on two of its three call sites.

| call site | guard | pinned before this PR |
|---|---|---|
| `documents.ts:2029` `/version` | `metadata.documentType !== undefined && …` | yes — #1237's QVT cells |
| `documents.ts:2663` `/sign-cert` | identical | **no** |
| `documents.ts:2932` `/sign-wallet` | identical | **no** |

## Shape
One `describe` per route via the suite's existing `WRITERS` table, four cells each: a present `null`, a present `''`, a present `false`, and a control proving an **absent** `documentType` is still accepted (201, stored and served as the source type). The control is what makes these pin a *distinction* rather than just a refusal — without it, a guard that refused everything would pass.

## Test Evidence

**Touched:** `services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts`. 1 file, +23 −0. Test-only: no route, no runtime behaviour, no config.

**Ran (all on this head):**
- `npx jest --runInBand` (originate): **877 passed / 877, 74 suites / 74**, rc 0. Baseline **869** at `77c6426b9` in the same worktree; **+8 = 2 routes × 4 cells**, fully accounted. The suite file itself goes 114 → 122.
- **Red proofs — ONE ARM PER ROUTE, and both prove isolation:**

  | arm | reds its own route | reds the sibling route | reds #1237's `/version` cells |
  |---|---|---|---|
  | truthiness at `:2663` (`/sign-cert`) | **3** | 0 | 0 |
  | truthiness at `:2932` (`/sign-wallet`) | **3** | 0 | 0 |

  The tamper is the truthiness form (`metadata.documentType && …`). That line is **byte-identical at all three sites**, so a content-anchored replace would be ambiguous: both arms tamper **by line number** with the other two guard lines asserted unmoved. Every restore verified by `sha256` against the pre-tamper hash, and `documents.ts` is byte-identical to its pre-tamper state at commit time. Untampered re-run after both arms: 122/122.
  - Route attribution was read from jest `--json` `fullName` (`describe > test`), **not** from the reporter's `✕` line — that line carries the test name only, with no describe prefix, so it cannot express which route a cell belongs to. Reading isolation off it would have been a false pass.
- `npm run lint` (= `eslint src`): rc 0, 0 errors.
- `npx tsc --noEmit`: rc 0. Re-run with `exclude: []` and the edited test file asserted present in the program (705 files, `--listFilesOnly`) because the project tsconfig excludes `src/__tests__`: rc 0.
- `npm test -w packages/shared`: 47 files / **928 tests** passed, rc 0.
- Push: rc 0. In-hook suites: `pre_push_hook_base` 28/0, `pre_push_hook_base_fixture_guard` 6/0, shell suites 60 passed / 0 failed / 0 skipped (of 60). No `FIXTURE BUILD FAILED`.

**NOT run:**
- **Preflight INCOMPLETE — 12/15 legs ran, 3 SKIPPED, nothing failed:** legs **3** (spec-auth conformance), **4** (path resolvability), **8** (served-spec consistency), each `SKIP — local stack not up on http://localhost:6882`. A skip is not a pass. None of the three bears on a test-only change, but they did not run and that is stated rather than rounded up.
- No integration or e2e cell: the routes are exercised through the suite's existing in-process app with the issuer-certs upstream stubbed and CIP-8 verification stubbed true, as the rest of this suite does. No live signing path was exercised.
- The `/version` guard is untouched, so #1237's own cells are unchanged — they are re-run here, not re-proved.

**Migrations + config:** none.

Refs KS-1301

🤖 Generated with [Claude Code](https://claude.com/claude-code)

