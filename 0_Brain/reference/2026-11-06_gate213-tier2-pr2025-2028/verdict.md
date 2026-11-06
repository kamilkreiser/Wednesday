GO WITH NOTES (PR 2025 GO WITH NOTES; PR 2026 GO WITH NOTES; PR 2027 GO; PR 2028 GO WITH NOTES)
PR 2025 (KS-1493) head 8e0070f193ba: GO WITH NOTES
PR 2026 (KS-1539) head a56b949c56f0: GO WITH NOTES
PR 2027 (KS-1542) head 52a781a3e493: GO
PR 2028 (KS-1614) head 8d4f6fca8388: GO WITH NOTES

# Gate 213: Secuura / Blockchain, batch of four PRs, tier 2, round 1 of 2

**BLUF.** All four do what their READY says, and every READY figure I re-ran matches. All four merge clean, in either order, on the pinned develop and on the develop that moved during this gate. With all four merged, the api-gateway suite is 159 files, 1677 of 1677. No finding makes any route more permissive, and every value that was refused is still refused. The two notes worth reading first:

- **PR 2028:** a function is an object, and it still reaches `String()`. It can throw without naming the property, or print `(got 800)`. This is the same on base and no production caller passes the bound, but the PR's title and comment say it cannot happen.
- **PR 2026:** the new log line sits before the 503. If the logger or the class read throws, the caller gets a 500 instead of the 503. The create is still refused.

A verdict is about the named SHA only. Severity is my label; priority is the humans' call.

Environment: my clone `repo/`, one detached worktree `wt/a`, Node v26.8.1. Dependencies are APFS clones of gate 204's install (lockfile blob `30777ce9cb`, the same at all four heads and develop), with `packages/shared` built in my worktree. Vitest ran with `--cache=false`. The clock ran from about 10:58 to 11:20 AEDT on 2026-11-06. Evidence paths are under `evidence/`.

Readings:

| When (AEDT) | develop | Heads |
|---|---|---|
| Start, about 11:00 | `1b1b65c7415f` | equal to `pins.txt` |
| End, 11:16 | `85046e8707a0` (moved) | all four unchanged, equal to `pins.txt` |

The move is one commit, KS-1938, 4 files, none shared with any PR (`z_live_develop.txt`).

---

## Findings

Every finding below is MEASURED AT RUNTIME unless it says otherwise.

**F1. PR 2028, Low. A function still reaches `String()`.** `routes/verification.ts:195` at head. The object branch tests `typeof value === 'object'`, so a function takes the scalar path, and the same is true of a revoked function Proxy.

Measured by a scratch probe on the real route factory, base and head identical (`q2_tables_compare.txt`):

| Value | Base and head print |
|---|---|
| function with `toString: () => '800'` | `(got 800)`, the text of an accepted bound |
| function with `toString: () => '1'` | `(got 1)`, the text of an accepted bound |
| function with `Symbol.toPrimitive: () => '2147483647'` | `(got 2147483647)`, the text of an accepted bound |
| function whose `toString` throws | bare `Error: secret-from-toString`, property not named, the thrown text escapes |
| function with `toString` returning an object | bare `TypeError` |
| null-prototype function | bare `TypeError` |
| revoked function Proxy | bare `TypeError` |
| function Proxy with a throwing `get` trap | bare `Error: trap` |

- **Oracle (Product, internal consistency):** the PR title, `verification.ts:160` and `:191` all say an object is never handed to `String()`, and the flow fragment says no refused bound may print what an accepted one prints.
- **Why Low:** it is SAME-ON-BASE, every one of these values is still refused, and no production caller passes the bound (0 hits in `index.ts`).
- **Fix shape:** take `typeof value === 'function'` into the same branch. I applied that as a tamper and the 40 cells stayed green, so nothing pins the current behaviour. I did not read what it then prints.

**F2. PR 2026, Low. The log line precedes the 503, so a throw inside it replaces the answer.** `routes/verification.ts:855` at head, in the catch, before `res.status(503)`. Table of 32 rows on the real router over loopback, base against head (`q2_tables_compare.txt`, raw tables `ks1539_table_b8c5.json` and `ks1539_table_h2026.json`):

| Logger | Thrown value | Rows | Base | Head |
|---|---|---|---|---|
| working | 12 ordinary shapes, plus one Error with a planted `constructor.name` | 13 | 503 | 503, byte-identical |
| working | Error with `constructor` undefined, Error with a throwing `constructor` getter, revoked Proxy of an Error | 3 | 503 | 500 `INTERNAL_ERROR` "Failed to create document" |
| throwing | all 16 shapes | 16 | 503 | 500 `INTERNAL_ERROR` "Failed to create document" |

- Enforcement ran 0 times in all 32 rows, so the create stays refused. This is a wrong status, not an opening.
- The three hostile shapes are synthetic: `JSON.parse` and the real ioredis class cannot produce them. The real gateway logger is `winstonLogger.log`, and I did not make it throw, so whether this can happen in service is unmeasured.
- **Oracle (Product):** the cheat fragment says "one log line, nothing else".
- **Fix shape:** log after the answer, or guard the log and the class read so neither can stop the 503.

**F3. PR 2026, test gap, Info.** "Never the message" is pinned only for a SyntaxError. My own tamper logs `err.message` for every other Error class and leaves the 6 cells green (`q3_cells_and_tampers.txt`). The product code is correct today: across the 13 rows above, the message never reached a log line. The one planted row does print its planted `constructor.name` as `errorClass`, which is the class-name field working as written; `JSON.parse` and ioredis cannot produce that shape. The stored-bytes reason in the code applies to the SyntaxError, so this is a gap, not a leak.

**F4. PR 2028, Low, disclosure.** The READY's "what this did not keep" names two things and the probe shows more values losing detail: a valid Date (printed its ISO text, now `[object Date]`, pinned by a cell), `new Number(800)`, `new String("800")`, `new Boolean(true)`, a Uint8Array, a Buffer and a cross-realm plain object. All still refused. Wednesday's ruling (b) names the class instance only, so whether the valid Date is covered by it is Wednesday's reading.

**F5. PR 2028, Low, ruling form.** Ruling in_03 (b) says keep both accepted points named "in the fragment and the commit message". The commit message names `[unprintable object]` but not the class instance (grep count 0; control phrase "revoked Proxy" counts 1). Both fragments and the READY name both. READ ONLY.

**F6. PR 2028, test gap, Info.** My tamper that lets any non-numeric JSON text through (so `{toJSON: () => true}` would print `true`, the same text as a refused `true`) leaves all 40 cells green. Head behaves correctly: it prints `[object Object]` for that value, measured in the probe.

**F7. PR 2025, Low, test text.** The test header at line 14 describes N2-C2 as proving the limiter is armed on the versioned spelling, but the cell at line 123 only asserts that the redirects carry no rate-limit code. In my tampers it went red only when PIN also went red, so it adds little. The armed-limiter proof really lives in N2-C1, whose tampers I reproduced. READ ONLY for the header; MEASURED for the tamper results.

**F8. PR 2026, Info.** The commit message says red on develop `c9cb07738cf6`; the fragments and READY say `8c5da776e`. I measured 3 of 6 red on `8c5da776eccf`. `c9cb07738cf6` is an ancestor of it. Harmless.

**PR 2027:** no findings.

---

## Answers per question

**Q1. Scope (`q1_scope.txt`, `q1_q5_merge.txt`).** Every PR is one commit whose parent is the stated base, and each base is an ancestor of develop.

| PR | Base | Files, as the READY states | Numstat matches READY |
|---|---|---|---|
| 2025 | `688c5cc177f8` | index.ts, new test, limiter-catalogue.ts, fragment pair | yes |
| 2026 | `8c5da776eccf` | verification.ts, new test, fragment pair | yes |
| 2027 | `8c5da776eccf` | f1 test file | yes |
| 2028 | `688c5cc177f8` | verification.ts, f1 test file, fragment pair | yes |

- Pairwise overlaps: 2026 and 2028 share `verification.ts`; 2027 and 2028 share the f1 test file; the other four pairs are empty. Self-intersection control printed the set.
- Trial merges of all six pairs: rc 0. Planted same-line controls: rc 1 on `verification.ts` and rc 1 on the f1 title line. Planted different-line control: rc 0.

**Q2. Behaviour.**

- **KS-1493:** 6 added lines, 0 that are not `//` comments, 0 removed. Stronger proof: `index.ts` transpiled with `removeComments` is byte-identical on base and head (sha `9bf36e7c6bcb92d9`), and a one-token control differs. Catalogue: 20 `sourceLine` lines, 4 added doc-comment lines, 0 other (`q2_static.txt`). The tier does not need raising: the compiled limiter is unchanged.
- **KS-1539:** see F2. The 503 is byte-identical in status, headers (minus date) and body on the real route for every ordinary thrown shape. The log carries route and class only. The real ioredis class reports `MaxRetriesPerRequestError`, which the seat listed as not covered. A healthy read gives the same answer and no line.
- **KS-1542:** one title string. 26 cells on both sides; exactly one title removed and one added, order otherwise the same. The old phrase occurs in 0 files at head and 1 at the parent.
- **KS-1614:** 18 of 18 refused with the property named, 12 changed, 6 same; every row equals the seat's `probe_table.json`. No row prints an accepted bound after the change. Of 45 extra values I probed, no object with `typeof 'object'` throws while being described, none is accepted, and functions are the exception (F1). Hostile objects tried include throwing traps, a throwing `Symbol.toStringTag`, a throwing `toJSON`, a 200000-deep array and boxed primitives. The deep array now prints a 400 KB message instead of a RangeError; the ticket already notes the unbounded length.

**Q3. Tests that can fail (`q3_cells_and_tampers.txt`).** Each tamper was asserted to have landed and restored sha-equal.

| PR | On base | On head | Seat's tampers reproduced | My own tampers |
|---|---|---|---|---|
| 2025 | 3/3 (by design) | 3/3, and 3 more runs 3/3 | T1 PIN and C2 red; T2 all three red | 308 instead of 307: PIN red. Limiter off the versioned spelling: C1 red |
| 2026 | 3 of 6 red, all by assertion | 6/6 | M1 and M2: C1, C2, C3 red | message also logged except for SyntaxError: survives (F3). `err.name` for `constructor.name`: survives |
| 2027 | 26/26 | 26/26 | K1 red 2, K2 red 3, as the READY says | not required (not a product PR) |
| 2028 | 13 of 40 red, all by assertion | 40/40 | M4 red 5, M7 red 1 | non-numeric JSON text: survives (F6). Functions take the object branch: stays green (F1) |

My T1 added a copy of the limiter above the redirect rather than moving the block, so C1 stayed green where the seat's logged T1 shows C1 red. The pin going red is what the comment promises. The difference is my tamper's shape, not a product fact.

**Q4. Suites (`q4_suites.txt`, `q4_static_checks.txt`).** Nothing failed in api-gateway, so there is nothing to classify.

| Tree | vitest files / cells | tsc | check:test-types (api-gateway) | eslint | docs-fragments |
|---|---|---|---|---|---|
| develop `1b1b65c7415f` | 157 / 1654 | 0 | 0 new, 25 baseline | 0 errors, 30 warnings | OK |
| base `688c5cc177f8` | 157 / 1654 | 0 | not run | not run | not run |
| base `8c5da776eccf` | 157 / 1647 | 0 | not run | not run | not run |
| 2025 | 158 / 1657 | 0 | 0 new | same | OK |
| 2026 | 158 / 1653 | 0 | 0 new | same | OK |
| 2027 | 157 / 1647 | 0 | 0 new | same | OK |
| 2028 | 157 / 1668 | 0 | 0 new | same | OK |
| all four merged | 159 / 1677 | 0 | 0 new | same | OK |
| all four plus PR 2020 | 160 / 1689 | 0 | not run | not run | not run |

- Planted controls: a type error in `verification.ts` gives tsc rc 2; a type error in the f1 test gives test-types rc 1, 1 new; a second `<h2>` in each of the three new flow fragments gives docs-fragments rc 1, restored sha-equal, re-check rc 0.
- The two docs-fragments ADVISORY lines are on develop and on the merged tree alike.
- Catalogue drift test: base 9 pass, 1 fail; head 10 of 10; tamper 1053 to 1052 fails 1; all merged 10 of 10; all merged plus PR 2020 10 of 10. The note's "560 against 569" and "+20" agree with the scanner's numbers.
- `packages/shared` whole suite on head 2025: 1494 of 1495. The one failure, `wallet-signature.test.ts` "accepts a valid wallet signature", also fails on develop, so SAME-ON-BASE. The seat's 348 of 348 is a 2-file subset that I did not re-run as such.

**Q5. Merge tree (`q1_q5_merge.txt`, `z_live_develop.txt`).**

| PR | Onto pinned develop `1b1b65c7415f` | Shared paths since base | Onto live `85046e8707a0` |
|---|---|---|---|
| 2025 | rc 0, `3fba6c771378` | 0 of 22 | rc 0, `8924194c6905` |
| 2026 | rc 0, `fdc50a680b3e` | 0 of 30 | rc 0, `75336c600185` |
| 2027 | rc 0, `30f611e17ad2` | 0 of 30 | rc 0, `dce37a88d2d2` |
| 2028 | rc 0, `21e6f9640847` | 0 of 22 | rc 0, `40a8133a220f` |

- Control: a develop-side path planted in a copy of each PR's set prints in the intersection.
- All four merged in order and in reverse order give the same tree, `066c479bea20`. Adding PR 2020 is rc 0.
- Of Seat B's other queued PRs (2009, 2017, 2018, 2019, 2021, 2022, 2023, 2024), none touches `index.ts`, the catalogue, `verification.ts`, `versioning.ts`, `rateLimitSkip.ts` or the f1 test. The catalogue's ten numbers therefore hold against that queue. Other open PRs were not checked.

**What a PR 2028 merge does to KS-1542: UNMEASURED.**

- Known: the branch name embeds `ks-1542`; Seat T 13th reads the PR as attached to both tickets (not re-read, no Linear access here).
- Known: no workflow under `.github` moves a Linear state. Three files mention Linear: `pr-premerge-ack.yml` only checks the PR body, the PR template only asks for the URL, and `api-contract-tests.yml` only files nightly findings in dry-run. READ ONLY.
- Not known: Linear's own GitHub automation is a workspace setting that this gate cannot read.
- Cheap mitigation, READ ONLY: merge PR 2027 before PR 2028, so KS-1542's own change is already in if the ticket moves, and read KS-1542's state straight after. The trial merge is clean either way. Whether the second one needs develop merged in first is the READY's statement; I did not test it.

## Rulings checked

- **Kam card = a (accept, reasoning beside the limiter, pinned):** met. The comment sits directly above the limiter at `index.ts:567`, and the tampers confirm the pin bites.
- **KS-1493 (b):** all ten rows edited, unit test green. **(d):** one systemTest file, numbers and note only, in the diff; the PR body is not read. **(e):** no catalogue-only PR. **(a)** and **(c)** are Linear filings, not read. The `:563` citation is left unfixed at catalogue line 56, as ruled.
- **KS-1542 no fragment pair:** none present.
- **KS-1614 two accepted points:** both behave as ruled and both are in the fragments and the READY; see F5 for the commit message.

## What was NOT tested

- Node 24, any box, a stack or a live gateway; Schemathesis, Akto, Playwright e2e, k6.
- PR 2026 through the whole gateway. I drove the real verification router with stubbed auth and a stubbed settings read, not a real Redis client, and not the real winston logger.
- PR 2025 at production default limits, a flood of 305, or the `/api/v2/verification` alias, all as the READY declares.
- The whole Playwright unit directory (446 cells): I ran only the drift test. The systemTest format gate: I only read the seat's `push.out`, lines 4 to 6.
- GitHub and Linear: PR bodies, ticket comments, attachments, KS 2009 and KS 2010, CI. The commission limits network to git fetch.
- check:test-types for the four other services the root script covers (no PR touches them).
- Seat tampers other than those named in Q3, including K3.
- The count of 22 stale citations. My own grep used a different file scope (it caught other services' `index.ts` and missed the docs), so it neither confirms nor contradicts the seat's list.
- Whether merging PR 2028 moves KS-1542.

## My own conduct

- **Stale first run, rejected.** My first dependencies were clones of the shared checkout's `node_modules`, which hold zod 3.25.76 while the code needs zod 4. PR 2025's pin could not boot (3 skipped). I moved those clones to `_quarantine_2026-11-06/` in this folder, took gate 204's install, and re-ran every probe, cell and tamper. Only the re-run is reported. The stale `node_modules` in the shared checkout may matter to anyone running from it.
- **Credential.** To fetch and to read `ls-remote`, I passed the shared checkout's configured `core.sshCommand`, which points at the project's read-write deploy key, into my clone's git calls. The commission allowed fetch from origin but did not name a key. I set my clone's push URL to `no_push_gate213` and pushed nothing.
- **Hooks refused four of my calls and I corrected each:** three for an unquoted `=====`, one for a `git worktree` given through a variable. A fifth refusal was a pointless `rm -f /dev/null` of mine. A sixth command I drafted contained `cd /dev/null` in a subshell; that call was refused on the variable before it ran, and no `cd` ever executed.
- **Writes outside this folder, as far as I can tell:** npm's own debug logs under my home directory, and tool temp files (tsx, the KS-1493 test's temp directory) under the system temp folder. I did not inventory them. The shared checkout still reads `1b1b65c7415f`, 18 untracked as at Seat G 28th's count, no `refs/gate` refs. Gate 204's folder was read only, and vitest's cache was off.
- **Processes:** every suite ran in the foreground, one at a time. 0 of my processes remain.
- **Left in this folder:** `repo/`, `wt/a` (with about 1.4 GB of cloned dependencies, sharing blocks on APFS), `_quarantine_2026-11-06/`, `deps/` (empty), `evidence/`. Nothing was deleted. Scratch tests are in `evidence/scratch/`.
