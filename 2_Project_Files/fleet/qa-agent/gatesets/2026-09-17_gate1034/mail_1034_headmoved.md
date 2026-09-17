SUBJECT: [Secuura/Blockchain -> Wednesday] HEAD MOVED: #1034 KS-1215 @e4624218bc29cda4c07b2d31ca18bba422cfbc3e (TIER 1)
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TS: 2026-09-17T15:33:54.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}
Seat A
Seat A 8th successor -> Wednesday: HEAD MOVED #1034 KS-1215

## BLUF
**#1034 KS-1215 is pushed at `e4624218bc29cda4c07b2d31ca18bba422cfbc3e`** (origin branch and refs/pull/1034/head both read e4624218b at 15:33:50Z, in the same action as this send; develop still 3961c2add). It is the complete pre-gate fix from your 13:51:51Z ruling: register-connector forwards the header the auth middleware left in place, never `rawAuthorization`. Tier stays 1.
- A fast-forward `fd81a75f0` -> `e4624218b`, PROTOCOL-CLEAN. Origin develop read `3961c2add` at 15:26:23Z, inside the push script, 3 s before the push began.
- PR body: ONE pre-gate section added. KS-1215: ONE facts line (`b7ff6ed1`), stays In Progress.
- **Nothing changes on #1034 while its gate runs.** I move to QUEUE item 3 (KS-1101 cells, local).

## Recommendation
Re-pin the drafted #1034 gate set and its launcher's compare guard to `e4624218b`. Against develop `3961c2add` the head changes 3 files: `middleware/auth.ts`, `routes/platform.ts` and the ks1215 test. Its merge base with develop is `3961c2add`.

## Detail
### Push (15:26:26Z -> 15:31:54Z, rc 0)
- Guards before the push, all in one script: HEAD, branch, porcelain 0, KS-1086 `8a6b0d9c2` an ancestor, origin branch = `fd81a75f0`, a fast-forward, develop = `3961c2add`. #1034 read 0 reviews and 0 review comments at 15:26:25Z.
- Verify: `PROTOCOL-CLEAN — shape: fast-forward: tracking ref fd81a75f0 -> e4624218b, origin at e4624218b`; heads IDENTICAL (113).
- In-hook preflight: `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` Legs 3, 4 and 8 were skipped (no local stack); this is not a pass of those three. Leg 1 spec in sync; leg 2 all locks clean-room-installable; leg 5 59 / 59 audit-contract cases; legs 6 and 7 no advisories outside the baseline; leg 14 shell suites 35 / 35 (243 s); leg 15 21 / 21 guards accounted for.
- Stubs (KS-1201): 4 `login_stub.mjs` listeners ended by verified pid (92148, 92232, 92346, 92424; command, cwd = raise-0916-a, ppid 1, started after the push). Control: 1087 ps rows parsed; 17 non-node listeners before and 17 after; 0 of mine remain.
- attachmentsForURL `pull/1034` -> KS-1215 `contributes` (control `pull/99999` empty). Closing-phrase scan on `fd81a75f0..e4624218b` commit messages: 0 matches (its control line matches 1).

### PR #1034 body
PATCH 200 at 15:32:46Z; the readback is byte-equal to what was sent. The section sits above the round-1 body, which is unchanged. It carries: the cause (`platform.ts:211` preferred `rawAuthorization`, which `index.ts:347` copies before auth runs); the fix; the 4 cells; both tamper tables; the sweep result; the preflight line; and NOT covered (`/api/batch/*`; a real exchange and real upstreams; the edge; the platform suites; the test-including tsc program).

### Evidence: recorded by the 7th successor, NOT re-run by the 8th (develop did not move)
All paths are under `5_Project_History/2026-09-17_seatA-7th/ks1215/r1-pregate/`.
- **Red-proof** at `96d859467` (develop merged in, platform fix not applied), `redproof-head-3.json`: 2 red / 18 green, matching `redproof.prediction`. The reds are register revoked and register live; both show `user:ks1215-revoked` / `user:ks1215-live` reaching `/api/audit` and the other two calls.
- **ks1215 alone** at `e4624218b`, `fix-solo.json`: 20 / 20.
- **Tamper tables** (`tamper-auth.out` + `tamper-auth/tamper_table.json`; `tamper-platform.out` + `tamper-platform/tamper_table.json`). Every row: `npx tsc --noEmit -p .` in services/api-gateway rc 0; the WHOLE api-gateway vitest suite, 58 files / 576, 0 pending, denominator equal to T0; restored blob equal and `git diff --quiet`; 0 VOID; every red an AssertionError. 60 s ceilings unless stated.

auth.ts (8 / 8 as predicted, 33 reds):
| Row | Reds (pred) | 1-min load |
|---|---|---|
| T0 | 0 (0) | 4.29 |
| T0-DEFAULT (default timeouts) | 0 (0) | 5.63 |
| RP-DEV (`auth.ts` = develop `3961c2add` bytes) | 10 (10): the 9 round-1 reds + register revoked | 6.77 |
| DELETE-REMOVED | 10 (10) | 8.22 |
| O1 (delete only when the exchange returns no token) | 2 (2): STRUCTURAL x2 only; every runtime cell stays green | 8.94 |
| AFTER-AWAIT | 2 (2): STRUCTURAL x2 only | 11.19 |
| NOSET | 9 (9): exchange-OK controls x4, ks480 x2, register revoked, register live, register key-only | 11.28 |
| TI | 0 (0) | 9.78 |

platform.ts (3 / 3 as predicted, 2 reds):
| Row | Reds (pred) | 1-min load |
|---|---|---|
| T0 | 0 (0) | 9.27 |
| RAW-BACK (the `rawAuthorization` preference restored) | 2 (2): register revoked, register live | 8.77 |
| TI | 0 (0) | 8.41 |

- **Suite counts with load:** 58 files / 576 at 60 s ceilings (T0, load 4.29) and at default timeouts (T0-DEFAULT, load 5.63). Load was 3.38 at the start of this push.
- **eslint** (`eslint-fix.json`): the ks1215 test 0 / 0; `platform.ts` 0 errors / 1 warning (`no-unused-vars` `'err'` at `:983`), the same one warning as before the change (`:980`, `eslint-platform-head.json`).
- **Install:** the worktree's `Blockchain/Dev/node_modules` is develop `27e53ec3a`'s `npm ci` (vitest 4.1.11; `.package-lock.json` written 22:47 AEST 09-17). #1033 (root + originate package files) was not installed since. api-gateway has 0 `mysql2` references in `src/` and `package.json` (read at `e4624218b`; the same grep finds `express` in that `package.json` as its control).

### rawAuthorization sweep (first-hand, the 8th, 15:24:06Z)
`git grep -nE 'rawAuthorization' e4624218b -- Blockchain/Dev/services/api-gateway/`:
- `index.ts:347` is the write. The positive control `rawAuthorization[[:space:]]*=` counts 1 in `index.ts` at both `3961c2add` and `e4624218b`.
- `platform.ts:204` and the ks1215 test's line 24 are comments.
- **0 readers.** At develop the only reader was `platform.ts:211`. The write is recorded, not removed.
- Under `Blockchain/Dev/` outside api-gateway: 0 lines.

### TICKET candidates from your drafter (nothing filed, per 13:51:51Z)
- (a) The cache-get-throws HANG is the same at develop. Under the default unhandled-rejection mode the process exits; under "survive" (docker-compose and bicep) only the request hangs. Reachability is predicted none (both caches are plain Maps).
- (b) An exchange that never answers hangs the gateway request: the fetch has no timeout.

### NOT covered / NOT done
- NOT covered: `/api/batch/*`; a real exchange and real upstreams (the stub answers the three register-connector calls whatever Bearer arrives, so tenant-provisioning's own answer to a missing Bearer is not exercised); the edge; Schemathesis / Akto / Playwright / k6 (no stack); the test-including tsc program (no count quoted).
- NOT done: nothing filed; no re-run of the suites or tampers by this seat (Default A, accepted 15:24:54Z).

### Next (no wait on a GO)
- QUEUE item 3: KS-1101 O-SURFACE cells on WIP `40bdb8c85`, local only. I switch `raise-0916-a` to that branch with porcelain 0 at the switch. #1034's branch is not touched.
- Item 5 (Seat B's 09-17 vault sections) during a wait.

Seat A

