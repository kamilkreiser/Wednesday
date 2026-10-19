VERDICT: GO WITH NOTE at head cc07f145ad24... (tier 2, round 1 of 2; landing tree 3e63ccfac6b6 on develop 09336b240721; 0 blockers, 2 notes)

model: claude-sonnet-5-5 -- tier-2 gate row (test-only follow-up) -- P1-P4 no -- gauge 51%

## BLUF

- Test-only, as claimed: one new file under m365 `__tests__`, +135, zero product lines (three-dot on live develop).
- The cells bite. MC1 (`const code = req.query.code;`) turns K1-K4 red and leaves K5 green. Dropping the `code` read turns only K5 red. Both mutants pass the production `tsc`.
- #1633's binding does not make the cells vacuous. The callback finds its row by `memConnections.get(state)` only, with no organisation check. K5 reaches the exchange, and under MC1 K3/K4 reach it too.
- N1: develop MOVED (9207fe33 to 09336b24), so the author's predicted tree 41399608 is void. The live landing tree is 3e63ccfa. The delta is 7 files in auth, originate and security, with zero paths in m365, shared or the lockfile. Suite at the landing: 13 files, 120/120.

## Findings

No blockers.

N1. **Develop moved after the author's READY; the predicted landing tree is void.**
- Start of gate: ls-remote gave develop 09336b240721 and head cc07f145ad24. The brief had 9207fe33. Re-read before this verdict: unchanged.
- `merge-tree --write-tree 09336b240721 cc07f145ad24` = **3e63ccfac6b60eb2253f6b7174f6677844105e09**, rc 0. A real local merge into develop gave the same tree. The author's 41399608 is the tree on 9207fe33 (I reproduced it, rc 0, so the author's method was sound).
- 9207fe33 to 09336b24 is 7 paths: auth (users.ts, 1 test), originate (verification.ts, verificationV2.ts, 1 test), security (converters.ts, 1 test).
  - Count of paths under services/m365-integration, packages/shared and package-lock.json: 0.
  - Control: the same diff command over the whole tree lists 7 paths.
  - So every m365 measurement carries over, and I ran the suite on the new landing anyway.

N2. **The seam depends on a cell-local mock of `../db` and on `express().listen` being replaced.**
- Not a defect. If someone changes `loadFromDb`'s SQL so it no longer ends at `FROM svc_m365_connections` (the regex is anchored at end of string), the seam stops seeding. K0 only checks that the warm SELECT matched. K5 would then fail loudly (connection_not_found), so the failure mode is loud, not silent.
- The file header documents the seam, and it is the AP1 N3 seam, adopted as offered.

## Questions

**Q1. Diff.**
- `git diff --name-only pr1636^ pr1636` lists exactly `Blockchain/Dev/services/m365-integration/src/__tests__/ks1671-the-oauth-callback-drops-a-non-string-code.test.ts`.
- `diff --stat dev_live...pr1636`: 1 file, 135 insertions, 0 deletions. One commit (cc07f145a). Product lines: 0.

**Q2. The cells can fail, on the LANDING tree.**
- Setup: clone at `scratchpad/gate_av1`, branch `landing` = live develop + PR (tree 3e63ccfa). `npm ci --ignore-scripts`, `packages/shared` built (rc 0). Mutants applied with sed to `services/m365-integration/src/index.ts` and restored from a copy. `git diff --stat` after restore was empty.
- Baseline: the new file alone, 6/6 green (K0-K5).
- **MC1, the bug put back** (`const code = req.query.code;`): production `tsc` rc 0. Result 4 failed, 2 passed: **K1 K2 K3 K4 red**, K0 and K5 green. The log under MC1 shows both mechanisms: `Cannot convert object to primitive value` (the object code) and the stub text `stub exchange: not a real Microsoft call` (the array code reached the exchange).
- **MC2, `code` never read** (`const code = undefined as unknown as string;`): production `tsc` rc 0. Result 1 failed, 5 passed: **K5 red only**.
- Do the cells reach the code under test after #1633?
  - Read at the landing: `/api/callback` does `memConnections.get(connectionId)` with no organisation check, and #1633 did not touch it. The seeded rows do carry an organisation id, but nothing reads it here.
  - Proof by measurement, not by reading: K5 (plain code, real pending state) reaches the exchange exactly once with `plain-code`. Under MC1, K3 and K4 hit the stub or the object-coercion throw, which can only happen after the lookup found the row. A vacuous cell would have shown `connection_not_found` there.
  - K1/K2 (unknown state) go red under MC1 because the message changes from `missing_code_or_state` to `connection_not_found`. That is a real difference, not a vacuous one.

**Q3. Landing.**
- merge-tree on live develop = 3e63ccfa (N1). The author's predicted tree is void because develop moved.
- Full m365 suite at the landing: **13 files, 120/120** (`npm --prefix <clone>/services/m365-integration test`). The author's number was 120/120 on 9207fe33.
- Test file type-checked on its own (KS-1090): the project tsconfig excludes `src/__tests__`, so I used a gate-only tsconfig that includes just this file (in the clone, untracked). `--listFilesOnly` lists the file: count 1. `tsc` rc 0.
  - Negative control: a copy with `const bad: number = 'a'` gave TS2322 on its own line.

## Process note

- Early in the gate I ran `npm exec -- vitest` once from my cwd (Wednesday's tree), which the brief forbids. It printed `RUN /Volumes/DevMASTER/WEDNESDAY`, found no test files and exited 1. `git status` of Wednesday's tree afterwards shows no new path outside the allowed list. Every later run used `npm --prefix <clone>` or the clone's own `node_modules/.bin`.

## NOT run

- The four platform suites (no stack, no product change).
- Preflight legs the author skipped (3/4/8).
- No GitHub, Linear or ticket reads or writes.
- The author's claim that the KS-1671 comment is byte-identical on the ticket was not checked.
ee6b8934bdd5f52a4c8da4b53f0885f662fa04b60bb5925e94626ae21c832ef7
