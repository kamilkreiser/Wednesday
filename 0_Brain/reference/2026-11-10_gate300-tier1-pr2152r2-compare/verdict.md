PR 2152: GO WITH NOTES

# Gate 300, tier 1 (Opus), compare: PR 2152 round 2 of 2 (KS-1516, Seat U 21st fix round 1), against gate 298

| PR | head | verdict |
|---|---|---|
| 2152 | e3534ff2ad91a67bfb0376a51a1206d8feea4635 | GO WITH NOTES |

**BLUF.** The fix closes G298-2152-1. At the new head, a stored row whose STORED type is `opentimestamps` or `blockchain` answers `{verified:false, reason}` on `/api/timestamps/verify`, whatever `timestampType` the caller sends. The rfc3161 stored-row control stays green. My own mutants (remove the stored-type check; check the caller's type instead) each redden R7 and R8 by name. Every other timestamping cell gives the same result at 990efc31 and at e3534ff2 (105 of 105). The delta is exactly the three stated files.
- Notes only:
  - The round-1 parts of the PR body still carry round-1 figures as if they were current (G300-2152-1).
  - The stored-type check is a deny-list of two exact strings (G300-2152-2).
  - One response-shape change for stored unverified rows is not stated (G300-2152-3).
- Nothing blocks.

**Pins.**
- Start (22:55:37Z, ls-remote): develop 0115269abd111ee6acedb06fb0a0c3f8fd86f35a; PR 2152 (refs/pull/2152/head and the branch) e3534ff2ad91a67bfb0376a51a1206d8feea4635. These equal the commission.
- End (23:07:40Z): develop 0115269abd11 and PR 2152 e3534ff2ad91. **Neither moved.**

**Method.**
- Clone: my own blobless clone at `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/bc242b97-625e-4914-8468-73ab766503fd/scratchpad/g300/r`, using the project's deploy key by path (key never printed). PR head and develop are at `refs/p/*`.
- Trees: three sparse worktrees: `w/base` = d0b4825c, `w/prev` = 990efc31 (round-1 head), `w/head` = e3534ff2. Each holds services/timestamping, packages/shared and docs/openapi. Including the openapi directory lets ks1725 load, which it did not in gate 298's tree.
- Dependencies: `node_modules` and `packages/shared/dist` are symlinked read-only from the seat's `worktrees/s-u21-b`.
- Runs: vitest 4 through `--root`, niced. Each run was gated to load1 < 8 by a wait loop (6.08 to 7.71 at every run start). tsc was a single-package typecheck, started at a load1 spike of 15.8 from other seats; it is not a suite leg.
- My conduct in !CODING: only ls-remote, show, log, diff, rev-parse, merge-base and grep, plus file reads of the seat's record. No fetch, no write, no cd, no rm. Nothing was posted, commented on or mailed.
- Scratch: 38 MB, left in place. Both scratch trees are `git diff --quiet` clean at the end. My probe file `zz-g300-probe.test.ts` is untracked in `w/head` and `w/prev` only.
- DevMASTER: 89 GiB free at start and at end.

## FOUND / TESTED / HOW

**Q1. Delta 990efc316091..e3534ff2ad91.**
- Topology: one commit, parent 990efc31; ancestor check true, so it is a fast-forward. The merge base with develop is still d0b4825c.
- numstat, exactly the stated files:
  - `services/timestamping/src/index.ts`: +4 -0
  - `ks1516-…-never-reported-verified.test.ts`: +18 -2
  - `ks753-mock-tsa-fallback-is-not-verified.test.ts`: +2 -2
- I read every hunk:
  - **index.ts:** one 4-line block inside `verifyTimestamp`, after `rowToTimestamp` and before the KS-753 `!ts.verified` branch (head 590-593). No other function changed.
  - **ks1516 test:** the 20000 ms timeouts on R1 and R2, plus the new cells R7, R8 and C5.
  - **ks753 test:** header comment lines 17-18 only.
- Whole PR against d0b4825c: index.ts +13 -2, ks1516 test +140 -0, ks753 test +2 -2.
- Merge onto develop 0115269a: `merge-tree --write-tree` rc 0 (tree 30895a7e).
  - Develop moved d0b4825c..0115269a by 3 first-parent commits (KS-2134, KS-2138, KS-2129), 3 paths in all.
  - Shared paths with the PR: **0**. Control: the PR against itself gives 3. "timestamping" appears in 0 of develop's moved paths.

**Q2. G298-2152-1.** Instrument: the PR's own harness (the real express app with a DB stand-in that answers the hash+proof lookup).
- The head's test file run against the round-1 product (`w/prev` with only the test file swapped): **2 failed of 13, exactly R7 and R8** (`expected [200, true] to deeply equal [200, false]`). The other 11 were green, including C3 (rfc3161 stored row under rfc3161, true) and C5.
- At head: **13 of 13**. The round-1 file at prev: 10 of 10.
- My probes (head / prev):
  - Q1: stored ots row with verified=true, caller sends rfc3161. Head: false, and the keys are exactly `['reason','verified']`, so `timestamp` and `tsaUrl` are gone. Prev: **true**, with the timestamp.
  - Q2: stored blockchain row, caller sends opentimestamps. False at both heads (the early return).
  - Q7: stored rfc3161 row with verified=true, caller sends rfc3161. **true** at both heads, same keys.
  - Q3: stored rfc3161 row with verified=false, caller sends rfc3161. The KS-753 answer is byte-identical at both heads (reason text and timestamp).
- **My own mutants** on the head index.ts, run on the ks1516 file plus my probe file (20 cells). Each was restored, and the restored file was verified equal.

  | Mutant | Change | Cells that went red |
  |---|---|---|
  | M1 | remove the stored-type check | **R7, R8** (+ probes Q1, Q4, Q6) |
  | M2 | check the caller's `data.timestampType` instead of `ts.timestampType` | **R7, R8** (+ Q1, Q4, Q6) |
  | M3 | drop `blockchain` from the check | **exactly R8** (+ Q6) |
  | M4 | drop `opentimestamps` from the check | **exactly R7** (+ Q1, Q4, Q6) |
  | M5 | over-broad: the check also catches rfc3161 | **C3** (+ Q3, Q7): the rfc3161 control binds |
  | M6 | allow-list form `ts.timestampType !== 'rfc3161'` | none: 20 of 20 green, and Q6 also turns green (see G300-2152-2) |

  Q6 fails at head and under M1 to M5 because it is a deliberate probe of the deny-list residue (G300-2152-2), not a regression.

**Q3. The other round-1 findings, as ruled.**
- **G298-2152-2.** The body states both false-answering mismatched cases and "false is the safe direction" (LIVE bullets and the fix-round section). The new ticket comment states the same.
  - Measured: C5 (stored rfc3161 under opentimestamps) is false at both heads.
  - My Q5 (stored rfc3161 under blockchain) is false at both heads.
- **G298-2152-3.** R1 and R2 carry `}, 20000)`.
  - Measured: in my first cold run at head, **R1 took 14,074 ms**. It would have failed at the 5,000 ms default. Warm runs: 329 to 928 ms.
  - At prev (no timeout) my probe Q1, the first cell of its file, took 8,996 ms. The cold class is real (G300-2152-4).
- **G298-2152-4.** The ks753 header now reads: "the mock-ONLY types (opentimestamps, blockchain), which KS-1516 now reports as verified:false on creation and on verify (pinned in its own test file)". That is true at head. Comment only (diff +2 -2 inside the `/* */` header).
  - Census: carried. I could not read GitHub; the project's gh config is not logged in (`gh auth login` prompt, rc 4).
  - The seat's `evidence/census_ready2.json` (73 PRs, 338 file rows) lists the ks753 file, index.ts and the ks1516 test in PR 2152 only. Planted control: `api-gateway/src/index.ts` maps to PR 2125. `services/timestamping/` in general maps to PRs 575, 649 and 2152.
- **G298-2152-5.** The body names `GET /api/timestamps/:id`, `/hash/:hash` and `/document/:documentId` (via `formatTimestampResponse`) as still returning the stored `verified: true` and `verifiedAt`, under the fix-round section and "Before this deploys". The ticket comment names them under Residue. The delta does not touch any GET route (Q1 above).
- **Ruling item 6 (ticket comment).** I read the seat's posted text `push/linear_comment_ks1516fix.md`. Its stripped sha1 c16964bec421 equals the seat's posted record for comment `692553b2-42c4-…`.
  - It is a NEW comment that opens "**BLUF:** Correction to comment 5debce26". It states the corrected claim (stored ots/blockchain row false whatever type is sent; no timestamp or tsaUrl), the other mismatched case, and the residue (GET routes, stored rows and backfill as Kam's, supportedTypes/OpenAPI, CONNECTORS.md, options b and c, outside callers UNMEASURED).
  - It claims no more than the diff: every claim is measured above.
  - "5debce26 untouched, nothing deleted" is **carried**: the seat's tool read state, priority and assignee as unchanged. I have no Linear read, and I would not read a secret to get one.

**Q4. No other behaviour changed.**
- Whole timestamping suite, 12 files:
  - Head: 125 cells = 118 PR cells + my 7 probes. All 118 green; the 1 red is my Q6 probe (by design).
  - Prev: 122 cells = 115 + 7. All 115 green.
  - A per-cell comparison of all **105 cells outside ks1516** (ks1404 ×36, ks611 ×16, qualified-tsa ×13, ks753 ×10, ks740 ×9, db.retry ×6, ks1404-wiring ×6, ks1868 ×5, ks1725 ×3, smoke ×1): **identical, all passed** at both heads. ks1725 loaded this time and is green (3/3).
- tsc `--noEmit -p services/timestamping/tsconfig.json`: rc 0, 0 errors at both heads.
- Behaviour deltas I measured, and nothing else:
  - (a) A stored ots/blockchain row with verified=true, under rfc3161: true becomes false (intended).
  - (b) A stored ots/blockchain row with verified=**false**, under rfc3161: the answer stays false, but the reason changes from the KS-753 mock text with `timestamp` and `tsaUrl` to the KS-1516 text with no timestamp (probe Q4; G300-2152-3).
  - Every rfc3161-stored row answers as before (Q3, Q7, C3).

**Q5. Round-1 findings the fix did not touch.**
- The dead per-type decode switch (head 631-656) is unchanged and still unreachable for both types: the early return sits at 577, and the new stored-row return sits before the decode. Still harmless.
- Option a and nothing beyond it: the delta adds no SQL, no migration and no data write. The only query in the delta's path is the existing SELECT.
- The round-1 dead-code and residue statements in the body still read as gate 298 said.

**Q6. Closing words.**
- Scanned: the commit messages of 990efc31 and e3534ff2, the PR title (the update record's new_title is unchanged: "Refs KS-1516: the opentimestamps and blockchain timestamp types report verified false on creation and on verify"), the commit subject file, the posted body and the new ticket comment.
- Closing keyword + `#`/KS key: **0** in each. Planted control: 2 of 2 detected.
- `Refs KS-` is present in the title, body and both commits.
- Bare words only: "fix", "fixed" (as in "Gate finding 1 (Medium), fixed"), "closing" and, in the comment, "The second commit closes it". None of these is in closing form (G300-2152-5).
- The posted body is the seat's `pr_body_ks1516fix.final.md`: stripped sha1 79b9753f40ea equals the update record's new_body_sha1. That is carried; I made no live GitHub read.

## Findings

- **G300-2152-1 LOW (wording, body).** The round-1 sections of the PR body still state round-1 figures in the present tense, and the fix-round section is the only place the current figures appear:
  - The header line: "`index.ts` (+9 -2, four hunks) plus one new test file (+124 -0)".
  - Summary: "The four hunks" (now five) and "one new file with 10 cells" (now 13).
  - Test plan: "**Touched:** 2 files … (+9 -2) … (+124 -0). One commit", and the suite "after 115 tests".
  - "Linear: … (High, Backlog)", where the seat's own comment tool read the state as 'In Progress'.

  Nothing in them is false about round 1, but a reader of the top of the body gets the old touched set. Suggest a one-line "(round 1 figures; see Fix round 1 for the current PR)" or updated numbers.
- **G300-2152-2 INFO (hardening, not a gap in the ruling).** index.ts:591 is a deny-list of two exact strings. A stored row of any other `timestamp_type` with `verified = true` still answers **true** when the caller sends rfc3161 (probe Q6, `'OpenTimestamps'`: true at both heads). Examples: a capitalisation drift, or a legacy value.
  - The DDL (`migrations/001`, `docker/init/03`, `deployment/azure/migrate/init.sql`, the service's own `ensureTable`) has no CHECK on `timestamp_type`.
  - The only writer in the repo is `createTimestamp` (index.ts:540), behind the zod enum, so new rows are always one of the three lowercase values.
  - What any environment's data holds is UNMEASURED.
  - The allow-list form `ts.timestampType !== 'rfc3161'` (my M6) closes it and keeps all 20 cells green. A one-token change if Wednesday wants it; not required by the ruling.
- **G300-2152-3 INFO (an unstated, harmless response change).** A stored `opentimestamps`/`blockchain` row with `verified = false`, verified under rfc3161, used to get the KS-753 answer: reason "The stored proof is a locally generated mock token…", plus `timestamp` and `tsaUrl`. It now gets the KS-1516 reason, with no `timestamp`/`tsaUrl` (probe Q4: prev shows the old answer, head the new one).
  - `verified` is false either way.
  - The body's fix-round sentence ("a row whose STORED type is one of the two types now answers `{ verified: false, reason }` whatever type was sent") covers it. The LIVE bullet names only `verified = true` rows.
- **G300-2152-4 INFO (cold-start class, carried forward).** The 20,000 ms timeout earned its place: R1 took 14,074 ms in my first cold run. The margin is about 1.4x at the load seen (load1 about 6.5). The first cell of any other file in this suite has no explicit timeout; my probe Q1 took 8,996 ms as a first cell at prev. That is the ks728 class, not this PR's to fix.
- **G300-2152-5 INFO (words).** The new ticket comment says "The second commit closes it" (about the wrong-type case). The word is bare, with no key, so it is not closing form. A Linear comment does not drive state, and the comment also says "this ticket stays open (the PR says Refs)". Recorded only.

## Round-1 findings at this head

- **G298-2152-1 (Medium): CLOSED.** Measured: R7/R8 red at 990efc31 and green at e3534ff2. Mutants M1 and M2 each redden R7 and R8; M3 and M4 redden exactly R8 and exactly R7. The C3 control stays green, and M5 shows that it binds.
- **G298-2152-2 (Low): SETTLED.** Stated in the body and the comment as ruled. C5 and probe Q5 are false at both heads.
- **G298-2152-3 (Low): CLOSED.** Explicit 20,000 ms timeouts on R1 and R2; a 14,074 ms cold R1 was measured.
- **G298-2152-4 (Info): CLOSED.** The header comment is corrected and the delta is comment only. Census carried from the seat's JSON (ks753 file in PR 2152 only; control fired).
- **G298-2152-5 (Info): SETTLED.** The GET routes are named as residue in the body and the comment, and the delta does not touch them.
- **Ruling item 6 (ticket comment correcting 5debce26): SETTLED on the record.** I read the new comment's text and checked its sha1 against the seat's record. That 5debce26 was neither edited nor deleted is carried (no Linear read by me).

## NOT TESTED
- Live GitHub (PR record, title, body, comments) and live Linear (692553b2 and 5debce26). The gh config is not logged in, and I did not read any token. The body and comment were checked by file and sha1 against the seat's records only.
- An independent open-PR census (carried from the seat's `census_ready2.json`).
- Any database, stack, gateway proxy, real TSA or chain. tsc with test files included (seat's figure: 59 = 59 errors, carried). Lint (the package has none).
- What any environment's `ts_timestamps` holds, including non-enum `timestamp_type` values (G300-2152-2) and the count of residue rows.
