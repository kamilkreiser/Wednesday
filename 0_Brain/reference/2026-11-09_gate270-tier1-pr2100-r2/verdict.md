PR 2100: GO WITH NOTES

# Gate 270, tier 1, round 2 of 2 (the cap): PR 2100 (KS-1868 O105-P1, originate email.ts, three catches)

Gate: claude-opus-5-5, row G1. Written 2026-11-09 ~04:57 AEDT. Findings only. I fixed nothing and posted, mailed or pushed nothing. I wrote only this file and my clone and scratch under `/private/tmp/g270`.

| PR | head | verdict |
|---|---|---|
| 2100 | `eb4a08362cfb6ce90ffa094078bd8620caebe5e7` | **GO WITH NOTES** |

Head readings (`git ls-remote` on origin; branch `feature/ks-1868-originate-email-catches-unreadable-throw` and `refs/pull/2100/head` read together):
- **Start, 2026-11-08T17:41:14Z:** head `eb4a08362cfb`, develop `15dca468b86f`. Both equal the commission's pins.
- **End, 2026-11-08T17:56:23Z:** head `eb4a08362cfb` (unchanged, so this verdict stands for that SHA), develop `15dca468b86f` (unchanged).

## BLUF

All five round-1 findings are closed at this head. I ran each one rather than reasoning about it.
- **The test-isolation defect (G268-1) is gone.** The pair ks1937 + ks1868 under `--runInBand --no-cache` reads 16/16 in both orders. With the flag planted back it fails 5/16 and 3/16, then the file is restored byte-equal.
- **The round delta is exactly the 3 claimed files.** `email.ts` is byte-identical to round 1 (blob `d81394daeae8` at both SHAs).
- **The product still holds against three hostile values of my own,** one per catch. Ordinary errors log byte-identical text against base.
- **The tsc control now fires on a real TS2322.**
- **The merge onto develop `15dca468b86f` is clean,** and no unlanded PR shares a path.

Nothing blocks the merge. The notes are below:
- one Low wording slip in the HELD PR body, which can be fixed before posting with no commit;
- two carried test gaps;
- the pre-existing notification-client ticket candidate.

No finding needs Kam.

## Findings

### G270-1 (Low, words in the HELD PR body): the red-proof's failure *mode* is stated as fixed, and it is not. **TICKETABLE (fix in the held draft before posting; no commit).**
- **Where:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatT-17th/mail/pr_body_ks1868_round1_HELD.md`, Test Evidence, "Round 1, after gate 268", red-proof bullet.
  - It says "5 failed of 16 (… four 5 s timeouts and one assertion, R1 …)".
  - It also says "most red cells end as timeouts, not assertions".
  - The READY repeats both.
- **FOUND / TESTED (MEASURED AT RUNTIME):** I applied the identical plant (the seat's `plant_virtual_flag_t17.diff` hunk, written by my own script), ran ks1937 first, and refused DNS in process.
  - 5 failed of 16, the same count as the seat.
  - The failure modes differ: C1 timeout, **C2 assertion, R1 assertion**, R2 timeout, **R3 assertion**. That is 2 timeouts and 3 assertions, so "most end as timeouts" does not reproduce.
  - The split depends on how the DNS stub fails. Mine fails on `nextTick`; the seat's fails synchronously and also stubs `resolve*`. The split is not a property of the defect.
- **Fix shape (prose):** state the counts (5 and 3) and drop the timeout/assertion split. Or say that the split varies with the DNS stub.

### G270-2 (Low, test gap carried from G268-3 / Q3): no cell covers a thrown `null`/`undefined` at the SMTP catch, or the notification-client effect. **TICKETABLE.**
- The fragments and the HELD body now state both behaviours, and both statements are true (see Q5). The new test still asserts neither, so a later edit to the SMTP catch could change them silently. KS-2099 item 1 edits that catch next.
- **MEASURED** (my probe `/private/tmp/g270/probe/g270-probe2.test.ts`, base `email.ts` 78eed82 vs head d81394):
  - ACS init and ACS send with `null`/`undefined`: SAME on both trees, `resolved false`, logs `…: undefined`.
  - SMTP with `null`: base `REJECTED TypeError: Cannot read properties of null (reading 'message')`; head `resolved false`, logs `[Email/SMTP] Failed to send: unreadable thrown value`. `undefined` behaves the same way.

### G270-3 (Note, carried from G268 N2): the test file is still a script, with no import or export. **TICKETABLE.**
- The seat records it as not done. Top-level names are global, which is the same class as the ks488/ks1937 collision.
- **MEASURED:** today's all-tests tsc program shows 0 errors in this file (Q4).

### G270-4 (Note, pre-existing, not this PR's defect): the notification client's SMTP fallback ignores `sendEmail`'s answer. **TICKETABLE (already the seat's ticket candidate).**
- **MEASURED AT RUNTIME** (`/private/tmp/g270/probe/g270-caller.test.ts`, adapted from g268's caller probe; real email.ts and notificationClient; nodemailer, logger and fetch stubbed):

  | value thrown at SMTP send | base log | head log |
  |---|---|---|
  | ordinary Error | info "Notification sent via SMTP fallback" | SAME |
  | getterThrows, revokedProxy, `null`, and my own null-prototype message (4 values) | warn "SMTP fallback also failed (non-blocking)" | info "Notification sent via SMTP fallback" |

- The PR now names this effect in the fragments and the HELD body (true at head).
- Minor precision: the HELD body says "the `catch` at lines 116 to 123". The catch opens at 116 and its block closes at 127; the warn starts at 123. Cosmetic.

## Answers to the commission's questions

### Q1. Each of G268-1..5: closed, closed in part, or not

**G268-1: CLOSED (MEASURED AT RUNTIME).**
- **Substrate:** `git archive` of head into `/private/tmp/g270/head`. Runner: `jest --runInBand --no-cache`, with order pinned by my sequencer `/private/tmp/g270/probe/seq.js`. DNS was refused in process by `/private/tmp/g270/probe/nodns.js`; its refusal text `G270-NODNS` appears in both planted logs, and `getaddrinfo` appears in 0, so nothing reached the network. Order was read back from jest's `startTime`.

  | tree | order | result |
  |---|---|---|
  | head | ks1937, then ks1868 | **16/16**, rc 0 |
  | head | ks1868, then ks1937 | **16/16**, rc 0 |
  | head + `{ virtual: true },` planted back | ks1937, then ks1868 | **5 failed** (ks1868 C1, C2, R1, R2, R3), rc 1 |
  | head + flag planted back | ks1868, then ks1937 | **3 failed** (ks1937 E1, E2, E3, all 5 s timeouts), rc 1 |

- **Restore:** byte-equal. sha256 `2a836313f77c…` and git blob `d7000b1b5568` before and after, equal to the blob at `eb4a08362cfb`.
- I found no other `{ virtual: true }` in originate `__tests__`. The only `grep -i` hit is this file's explanatory comment, which serves as the positive control. `@azure/communication-email` is declared in originate's package.json (`^1.0.0`); 1.1.0 is installed.

**G268-2: CLOSED (READ + MEASURED).**
- `every caller` counts 0 in the test, the cheat and the flow. The positive control `Notification sent via SMTP fallback` has hits in all three.
- In the HELD body the phrase appears once, only as a quotation of the replaced sentence, and that quotation is true.
- **Caller census (READ, `git grep -i` at head over Blockchain, excluding tests):**
  - The four wrappers each `return sendEmail(...)` with no catch of their own.
  - Their only non-test callers are `notificationClient.ts:84/91/98/107`, which await and ignore the answer, and `adminConfig.ts:1516` (fire-and-forget `.catch(() => {})`) and `adminConfig.ts:1650` (the answer goes into `emailSent`).
  - `auth/` and `billing/` have their own `sendEmail` and are not callers.
- So the cheat's "only the rights-holder invite route (line 1650) reads the answer" is true.
- The invite route was READ: `await sendRightsHolderInvite` sits inside the route's try, whose catch calls `fail500`. So "used to end in its 500 handler, now answers `emailSent: false`" holds by reading. **The route was not run.**

**G268-3: CLOSED in words; the test gap is carried as G270-2.** I measured all 6 null/undefined cells; they match the fragments and the HELD body exactly (G270-2).

**G268-4: CLOSED.**
- `log text only` counts 0 in the cheat, the flow and the comment. The HELD body hit is a quotation ("in place of 'log text only'").
- The cheat, the flow, the HELD heading and the comment BLUF all now state that rejections become `false` / `null`.

**G268-5: CLOSED.** See Q4.

### Q2. Scope (READ)

- `git diff --stat 60e2bf4e6d25 eb4a08362cfb`: **3 files, +9 −7.** The test has 6 changed lines (+4 −2), the cheat 4 (+2 −2), the flow 6 (+3 −3). There is 1 commit (`rev-list --count` = 1), whose parent is `60e2bf4e6`.
- **Control:** `git diff --stat c0e6e744b7b2 60e2bf4e6d25` reads 4 files including `email.ts | 27`, so the instrument does see email.ts.
- **email.ts:** blob `d81394daeae8` at both SHAs, so the round-1 product hunks are unchanged.
- **The test delta:** the one code line `{ virtual: true },` removed, plus comment changes (+4 −1 comment lines).
- **The PR as a whole** against `c0e6e744b7b2`: 4 files, +214 −3, matching the READY.

### Q3. Product re-check at this head (MEASURED AT RUNTIME)

- **Probe:** `/private/tmp/g270/probe/g270-probe.test.ts`, same harness on both trees. Base is a copy of originate with email.ts at `c0e6e744b7b2` (blob `78eed82ffe66`, also develop `15dca468b86f`'s blob).
- **My three hostile values** (none of them is in the PR's cells):

  | site | value | base | head |
  |---|---|---|---|
  | ACS init | Error whose `message` getter throws a revoked Proxy | REJECTED | resolved false, `…: unreadable thrown value` |
  | ACS send | `{ message: { [Symbol.toPrimitive]() { throw } } }` | REJECTED `Error: toPrimitive boom` | resolved false, `…: unreadable thrown value` |
  | SMTP send | `{ message: Object.create(null) }` | REJECTED `TypeError: Cannot convert object to primitive value` | resolved false, `…: unreadable thrown value` |

- **Ordinary values, byte-identical lines and outcome on both trees (SAME):** `Error` at all three sites, `TypeError` at init, `Error('')` at ACS send, and a bare string at SMTP (logs `undefined` on both).
- No head cell rejects.

### Q4. tsc control (MEASURED)

- **My program:** a scratch tsconfig `/private/tmp/g270/tsc/head.json` that extends originate's, with `noEmit`, `types: jest,node`, rootDir `originate/src`, and `files` set to the exact git list of `.ts` under `originate/src` at head (284 files, `.integration.test.ts` excluded).
- **Result:** rc 2 with **4 `error TS` lines**, the ks1937 and ks488 TS2300/TS2451 pair as at base. 0 lines name ks1868; the positive control is ks488 = 2.
- **Control:** a planted `export const g270Planted: number = "not a number";` in a file *under* `src`. Result: rc 2, **5 lines**, the new one `g270_planted_type_error.ts(1,14): error TS2322`, and **0 TS6059**.
- **The seat's evidence agrees.** `q0_alltests_head_tsc_control.out` names TS2322 on its planted file, and `_oldstyle.out` shows the TS6059-only shape it replaced.
- The seat's "249 files" is its own selection (all of `src/__tests__` including integration tests). Mine is a different selection; the error count matches.

### Q5. Words

**Cheat and flow at head, every sentence checked:**
- Line citations: 1650, 1516, `notificationClient.ts` 79–123 (the try opens at 79 and the warn is at 123), and the info at 115.
- Caller behaviour and the null/undefined split: measured.
- "16 of 16 in both orders", and with the flag back "5 and 3 cells": measured.
- "162 lines": `wc -l`.
- "no assertion and no cell title changed": the diff touches only comments and the flag line.
- "rejections become false … null": measured, including the init path.
- **No false sentence found.**

**HELD PR body, true at this head except G270-1:**
- blob `174e316a0978` → `d7000b1b5568` and sha256 `66eed243…` → `2a836313…`: both verified.
- The eslint directive at line 93 (91 at the first push): verified.
- "+162", "+17 and +11": verified.
- Whole suite "221 suites / 2600 of 2600": verified, see below.
- The 18-cell null/undefined statement: my 6 cells plus the ordinary controls agree.
- The notification-client measurement: re-measured (G270-4).

The develop SHAs in its two "Re-measured" paragraphs are timestamped readings (`fa0592f3b6f5`, `2935f7231097`). Develop is now `15dca468b86f`, so those paragraphs are true as dated but are not current.

**HELD ticket comment:**
- Checked true: the BLUF, "4 files, +214 −3", "8 cells, 162 lines", "16 of 16 in both run orders, … fails in both", the callers paragraph, and "tsc … 4 lines … with a control that fails on its planted error".
- Not verified by me: "lint 0 errors" (see NOT tested).

**Whole originate suite at head (MEASURED):** `jest -w 2`, DNS refused except loopback (`/private/tmp/g270/probe/nodns_local.js`), my probe files excluded. Result: **221 suites, 2600 / 2600, 0 failed, rc 0** (`/private/tmp/g270/out/whole3.json`). ks1868 ran 8th and ks1937 16th in start order.
- **Two earlier runs were substrate failures, and I name them:**
  - With all DNS refused, 143 suites failed. supertest needs `localhost`; one suite showed 31/31 fail vs 31/31 pass under the two stubs.
  - A run with loopback allowed still had 5 suites failing on ENOENT for `migrations/`, `docs/openapi/` and `scripts/`, because my archive held only part of the tree. After I archived those paths at head, the 5 suites read 44/44.

### Q6. Merge and overlap (MEASURED, own clone)

- **Merge:** `git merge-tree --write-tree 15dca468b86f eb4a08362cfb` returns rc 0 with tree `376b42fa8673`. `git diff --stat 15dca468b86f 376b42fa8673` gives exactly the PR's 4 paths, +214 −3.
- **Develop delta:** the merge base is `c0e6e744b7b2`. The develop delta since then is 29 paths and the PR has 4; their intersection is 0. The self-intersect control is 4.
- **Open-PR census:** I fetched all 2020 `refs/pull/*/head`; 1630 are not ancestors of develop (squash merges). For each I diffed against its merge base with develop and intersected with the PR's 4 paths.
  - Hits: **2100** (positive control), 693, 705, 1339 and 2056, all on `email.ts`.
  - Each of those four PRs' email.ts blob is already in develop's history (`454a64ebb`, `806c602fe`, `2cb858335`, `90b500e19`). They have all landed.
  - **No unlanded PR shares a path.**
- Not covered: the GitHub open/closed state (no API was used).

## What was NOT tested
- **Product and runtime:** a real ACS or SMTP provider, a booted service, the invite route at runtime (READ only), Node 24 (I used v26.8.1), and the four platform suites.
- **eslint:** the flat config plus the no-cd rule, as in gate 268.
- **The docs-fragments checker:** it needs a git work tree at its root, and my clone is `--no-checkout`. An attempt with `--from-ref` reported the directories missing, so it is NOT RUN.
- **The live PR and ticket bytes:** I read only the HELD drafts.
- **Mergeability under GitHub's own merge:** I checked with `merge-tree` only.

## Substrate (named)
- **Tree:** `git archive` of `eb4a08362cfb` (Blockchain/Dev package.json, eslint config, `packages/shared`, `services/originate`, `scripts`, `migrations`, `docs/openapi`, `prisma`, and `Projects Documents/fragments`) into `/private/tmp/g270/head`.
- **node_modules:** a per-entry symlink farm to gate 258's install `/private/tmp/g258/Blockchain/Dev` (the one gate 268 vetted against the lockfile), with `@secuura/shared` pointing to my tree's `packages/shared`.
- **`packages/shared/dist`:** copied from gate 268's build after `diff -r` showed `packages/shared/src` identical.
- **Base variant:** `services/originate_base`, a copy with email.ts at `c0e6e744b7b2`.
- **Files I added to my own tree only** (none are in the repo): the probe files `g270-probe.test.ts`, `g270-probe2.test.ts` and `g270-caller.test.ts` under each variant's `src/__tests__`.

## Own conduct
- **Clone and scratch:** `/private/tmp/g270`, 370M at the end, **left in place** (QA no-rm). The planted tsc file is in `/private/tmp/g270/_quarantine_2026-11-09/`.
- **Clone attempts:** my first clone, with `--reference` to g268's clone, failed (unresolved deltas). It left nothing usable and was not removed. The working clone is `/private/tmp/g270/repo2`.
- **Hook refusals:**
  - zsh `=` expansion on an `echo ======` separator.
  - Two refusals of git write verbs written as `git -C $R …` (the hook reads `$R` as outside). I re-ran them with the literal `/private/tmp/g270/repo2` path; nothing was bypassed.
- **Network:** git `ls-remote` and fetch only. No DNS left the process: every jest run refused non-loopback lookups in process.
- **Load:**
  - load1 read **8.62** at the start of my first whole-suite run (others' load plus mine) and **10.06** just after it ended.
  - That breaches the rule to keep load1 under 8. I dropped to `-w 2` for later runs and launched only once load1 read 7.13; at the end it was 4.36.
- **Disk:** DevMASTER free fell from 14 GiB to 11 GiB during the session. My writes were all on the boot volume. It stayed above the 10 GiB stop line.
- **The Blockchain project checkout:** read verbs only (`git config --get` with `GIT_OPTIONAL_LOCKS=0`, plus reads of the seat's evidence).
- No PR comment, no ticket write, no mail, no push.
