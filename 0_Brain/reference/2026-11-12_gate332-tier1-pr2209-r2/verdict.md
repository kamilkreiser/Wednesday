PR 2209: GO (at head 2eca13ad7e8c; tier 1; round 2 of 2)

Gate 332, tier 1 (Opus), one session, 2026-11-12 05:55Z to 06:08Z (16:55 to 17:08 AEDT). Round 2 of 2 under the cap. Findings only: nothing fixed, posted, mailed, pushed, merged, or written to Linear, GitHub or a board.

Where things ran:
- Everything that wrote ran in my own clone `scratch/repo` in this folder: a fresh `git clone --filter=blob:none` with a sparse checkout (`scratch/setup.sh`, gate 331's script with this folder's path). The clone's own `core.sshCommand` was set to the project deploy key so lazy blob fetches work. Write verbs (fetch, merge-tree) ran only there.
- `node_modules` came from the same read-only symlinks gate 331 used: the root one and `packages/shared/dist` point to gate 313's `r2` install, and `services/auth/node_modules` points to the shared checkout's copy. `packages/shared/src` differs from r2 in one test file only (the same as gate 331).
- In the shared Secuura checkout I ran read verbs only (`ls-remote`), with `GIT_OPTIONAL_LOCKS=0`.
- Every file I changed in the clone was restored and checked by blob: password.ts `70efe281f672`, the ks2021 test `9b5e9a56abab`. The probe file was moved aside to `scratch/aside/` (a copy is `out/zzprobe-gate332.test.ts.ran`). `git status` in the clone shows only the three symlinks.
- Whole-suite runs used `cwd` = the auth package, set through python `subprocess` (`scratch/whole.py`). Nothing ran from the WEDNESDAY working directory.
- Machine: Node v26.8.1, macOS arm64.
- **Spark:** the tunnel was UP. The digest STANDARD ran with the Spark, and the shadow review ran (see Q8). One departure from "writes only under scratch/": `spark_gate.sh` refuses any work dir under `/Volumes/DevMASTER/WEDNESDAY`, so its work dir was in the session scratchpad (`spark_work_2209`). That is gate 329's precedent. Copies of facts.json, diff.patch and review.json are in `scratch/spark/`.

## Pins

| when | develop | refs/pull/2209/head |
|---|---|---|
| start, 05:55:19Z (`scratch/pins_start.txt`) | cea1cdc2b07db6516ff4d9594472666e764a6a6b (= commission) | 2eca13ad7e8cb65d190f660b3b289d36f4d5475c (= commission) |
| end, 06:07:38Z (`scratch/pins_end.txt`) | unchanged | unchanged |

Neither pin moved. PR 2201 read 50c32501e60c at both reads.

**Shape of the PR:**
- Two commits: 2db221d4, whose parent is 581296f0, then 2eca13ad, whose parent is 2db221d4 (round 1's head, gate 331's pin).
- `merge-base(origin/develop, head)` = 581296f039b4. `rev-list develop..head` = 2. The develop side's own merge-base with the PR is the same commit.
- **Merge-tree:** `merge-tree --write-tree origin/develop p2209` gives rc 0 and tree 97ca0c6d25ab (`out/merge_tree.txt`).
  - develop to merged: exactly the PR's 2 files, +93 -2.
  - head to merged: exactly develop's 3 moved files, +29 -1.
- **Control that develop's lines survive:** each of develop's 3 moved files has a merged-tree blob equal to develop's blob and different from the head's: ks1990 originate test e7d1381a57f8, ks2055 transfer test d0c119bff08d, transfer/src/index.ts dca7bb7e7547.
- The PR's 2 files have merged-tree blobs equal to the head's: password.ts 70efe281f672, ks2021 test 9b5e9a56abab.
- **The develop move (581296f0 to cea1cdc2):** 3 files, `services/originate/...ks1990...test.ts`, `services/transfer/...ks2055...test.ts` and `services/transfer/src/index.ts`. None is a PR file and none is in `services/auth`. The seat's claim is verified.

## Summary

Round 2 does what gate 331 asked, and the measurements confirm it.

- **Behaviour against develop.** On a 43-shape corpus (gate 331's 25 shapes plus 18 more), run CRLF and LF with the row last, in the middle, and last followed by a trailing separator (6 variants per shape, 261 rows per build), the head differs from develop ONLY on rows whose count field, trimmed, is exactly `0`. Those rows are the padding rows, which is the fix itself.
- **Malformed counts refuse again.** Every malformed own-suffix count that round 1 let through now refuses, as at develop: empty, whitespace-only, no colon, `abc`, `-1`, `1,234`, `3abc` and `O`. No input flips from refuse to allow except the exact-0 count.
- **The no-colon row cannot reach the catch.** It refuses in all 6 variants, and no "failed" warn line is written (measured).
- **The READY's numbers reproduce:**
  - R3 is 5 red with round 1's real password.ts blob e8eb9633 and green at the head.
  - C4 alone kills M3. It also kills M8, which the body says was not addressed.
  - The 4 HIBP files give 47/47.
  - The whole `services/auth` suite gives 150 / 1850 / 1850, rc 0, twice.
  - tsc rc 0, and the ratchet reads 41 baseline / 0 new.
- **The body is true** on the points the commission asks about. One stale sentence remains (G332-2209-2).
- **Gate 331's Minor (G331-2209-1) is closed.** No Major and no Minor remain, only Notes and Info.

## Q1. The fail-closed shape

Probe: `out/zzprobe-gate332.test.ts.ran`. It drives the real module over a fake fetch, with a logger stand-in that records warn lines. Driver `scratch/mut.py`, table `out/probe_table.md`, raw `out/probe/*.json`. Each of the 43 shapes ran in 6 variants, and the 6 variants agree on every shape for develop, round 1 and the head. In the table, B means breached (refuse), a means allow, and a! means allow through the catch.

| own-suffix row | develop | round 1 (2db221d4) | head (2eca13ad) |
|---|---|---|---|
| `S:0`, `S: 0`, `S:0 `, `S: 0 `, `S:0\t`, ` S:0`, `S:0:4` (the `S:0\r` form is covered by every CRLF variant) | B | a | **a** (the fix) |
| `S:00`, `S:0.0`, `S:-0`, `S:+0`, `S:0e0`, `S:0x0` | B | a | **B** |
| `S:` (empty), `S:  ` (spaces only) | B | a | **B** |
| `S` (no colon) | B | a | **B**, no catch warn |
| `S:abc`, `S:-1`, `S:1,234`, `S:3abc`, `S:O` | B | a | **B** |
| `S:1`, `S:3`, `S:3861493`, `S:52372427`, `S: 3`, `S:3 `, `S:\t3`, ` S:3`, `S:3:4`, `S:0.5`, `S:1e3`, `S:0x10`, `S:Infinity` | B | B | B |
| `S :3` (space before the colon) | a | a | a (unchanged) |
| `s:3`, `s:0` (lowercase), mixed-case `S:3` | a | a | a (unchanged; the API sends uppercase) |
| other suffix: `O:3`, `O:0`, `O:`, `O` (no colon), `O:abc` | a | a | a |
| empty 200 body, non-200 503 | a | a | a |
| fetch throws | a! | a! | a! |

**Every input where the head differs from develop** (`table.py`: "HEAD differs from DEVELOP on 7"): `S:0`, `S: 0`, `S:0 `, `S: 0 `, `S:0\t`, ` S:0`, `S:0:4`.
- All seven have a count field that reads exactly `0` after `trim()`. `S:0:4` qualifies because `split(':')` takes the second field. The live service never sends an extra field (gate 331: 2,006 of 2,006 lines conform).
- **So the padding row (an exact count of 0 for the user's own suffix) is the ONLY behaviour change versus develop.** Round 1 differed from develop on 21 of the 43 shapes. The head differs on 7, and all 7 are exact zero.

**`00`, `0.0`, `-0` and similar.** They REFUSE at the head, the same as develop. Only the literal string `0` (after trim) is skipped.
- That matches the author's stated rule ("skipped ONLY when its count, trimmed, is exactly `0`").
- The body names `S:00` explicitly ("`S:00` still refuses"), with gate 331's live reading of 0 leading-zero counts in 2,006 lines.
- `0.0`, `-0`, `+0`, `0e0` and `0x0` are not named individually, but the "exactly `0`" rule covers them, and the code does what the rule says.
- This is the fail-closed direction: a non-canonical zero refuses, it does not allow. Note-level at most (G332-2209-3).

## Q2. Cells and mutants

The 4 HIBP files (ks2021 + ks1968 B1 + ks1968 B2 + ks1868-password-verify-hibp) hold 47 cells (`out/mutants.json`, `out/t_mut_*.log`).

| build | 47 cells | killed by |
|---|---|---|
| HEAD | 47 passed | - |
| develop's line | 2 failed | R1, R2 |
| round 1's line (`Number(countText) > 0`) | 5 failed | all 5 R3 rows |
| N1 drop `?.` (`countText.trim()`) | 1 failed | R3 "no colon at all" (the probe shows a!: the TypeError is caught and the password is allowed) |
| **N2 drop `.trim()` (`countText !== '0'`)** | **0, SURVIVES** | the probe changes only `S: 0` and `S: 0 ` (to refuse). Fail-closed direction, harmless |
| N3 inverted (`=== '0'`) | 13 failed | R1, R2, R3 x5, C1, C2, C4, ks1968 B1 x2, B2 |
| N4 `!= 0` (numeric loose compare) | 1 failed | R3 "an empty count" |
| N5 `Number(countText) !== 0` | 1 failed | R3 "an empty count" |
| **N6 `countText?.trimStart()`** | **0, SURVIVES** | equivalent: `line.trim()` already removed every trailing character the count could carry; the probe matches the head on every row |
| M2 suffix compare dropped | 6 failed | R1, R2, C3, ks1968 B1 x2, B2 |
| M3 `line.trim()` removed | 1 failed | **C4** (the READY's claim) |
| M5 `\|\|` for `&&` | 6 failed | same as M2 |
| **M7 case-insensitive compare** | **0, SURVIVES** | the probe changes only lowercase and mixed-case rows (to refuse). Harmless |
| M8 `line.trimEnd()` | 1 failed | **C4**, so it is now killed (the PR body says M8 was "not addressed") |
| **M9 `line.trimStart()` (new)** | **0, SURVIVES** | the probe changes only `S` (no colon) in the CRLF-middle and CRLF-trailing variants, to ALLOW: the `\r` stays on the suffix and the row no longer matches |

**R3 and C4.**
- R3 is red at 2db221d43ad8: with the real round-1 blob e8eb9633 in the whole suite, 5 failed, all R3 (`out/t_whole_redfirst_round1.log` and `_b.log`). It is green at the head.
- C4 kills M3.

**The commission's four mutants:**
- Drop `?.` (N1): killed.
- `=== '0'` inverted (N3): killed.
- `!= 0` numeric (N4, and N5 as its strict form): killed.
- Drop `.trim()` (N2): **survives**. It is harmless (it only makes ` 0` refuse) and is unreachable on the live format. See G332-2209-1.

## Q3. The optional chain

Measured, not inferred. At the head, the own-suffix row `S` (no colon) gives breached = true in all 6 variants, and the warn recorder holds no "HIBP lookup failed" line (`viaCatch` false) on any row of the head's corpus. The only head rows with any warn line are `non-200 503` and `fetch throws`.
- **Positive control:** N1 (the bare `countText.trim()`) gives a! for that row, which is the TypeError, caught, failing open. R3's "no colon at all" cell kills it.
- A no-colon row for ANOTHER suffix (`O`) allows at the head with no catch warn, because `hashSuffix === suffix` short-circuits before `?.` is reached.

## Q4. No other change

- **`diff --numstat 2db221d43ad8..2eca13ad7e8c`:** exactly the two files the READY names. password.ts is +5 -2 and the ks2021 test is +24 -2. The READY's "+29 -4" is the total and is correct.
- **The hunk:** one condition line changes, with 3 comment lines added and 1 changed, and the `const [hashSuffix, countText] = line.trim().split(':');` line is unchanged. Test: the header comment, the describe title, R3 and C4.
- **Against develop 581296f0:** +6 -2 and +87 -0. GraphQL agrees: +93 -2, 2 files.
- **Callers:** `git diff --stat 2db221d43ad8 p2209 -- services/auth/src/routes` and `git diff --stat origin/develop p2209 -- …/routes` are both empty. The call sites read at the head:
  - `routes/auth.ts:214` (register)
  - `routes/auth.ts:898` (reset)
  - `routes/users.ts:1009` (change-password)
  - These are the same lines gate 331 read, with the same `if (await isPasswordBreached(...)) throw new ValidationError(...)` shape. Nothing in the callers moved.

## Q5. Suite and controls

The whole `services/auth` vitest suite ran (not the reduced set). Logs are in `out/t_whole_*.log`, with JSON reports in `out/whole_*.json`.

| run | load1 at start | files | tests | rc |
|---|---|---|---|---|
| head (`head`) | 3.38 | 150 passed | 1850 / 1850 | 0 |
| head, run 2 (`head2`) | 5.50 | 150 passed | 1850 / 1850 | 0 |
| red first: password.ts = round 1's blob e8eb9633, test kept (`redfirst_round1`) | **8.91** | 1 failed / 149 | **5 failed (all R3)** / 1845 | 1 |
| the same, re-run under the load limit (`redfirst_round1_b`) | 3.54 | 1 failed / 149 | 5 failed (all R3) / 1845 | 1 |
| red first: password.ts = develop's blob f7f463e0, test kept (`redfirst_develop`) | **10.09** | 1 failed / 149 | **2 failed (R1, R2)** / 1848 | 1 |

- **The load limit was missed on two runs.** Two red-first runs started above the commission's load1 < 8 (8.91 and 10.09; the load came from my own preceding run). The round-1 red-first was re-run at 3.54 with an identical result. The develop red-first was not re-run. Its outcome is the deterministic R1 and R2 failure that gate 331 also measured. It is stated here, not hidden.
- **Whole-ness:** the head JSON report's 150 file names are set-equal to a walk of `src/**/*.test.ts` (150, ks2021 included). numTotalTests is 1850 and success is true. The suite grew by +6 over round 1's 1844, which equals R3 x5 + C4.
- **G331-2209-5 (the seedDemoUsers timer error):** 0 of 5 whole runs printed vitest's `Errors` line (the only grep hit is the `dbErrors.test.ts` filename). I claim no rate.
- **Planted controls** (`scratch/planted.sh`):
  - A failing cell appended to the ks2021 test gives rc 1, `1 failed | 11 passed (12)`. This also confirms the file holds 11 cells.
  - A type error appended to password.ts gives tsc rc 2 with 1 error at `password.ts(321,14) TS2322`, and the ratchet rc 1.
  - Both were restored and checked by blob.
- **Typecheck at the head** (`scratch/tsc.py`): `tsc --noEmit -p services/auth/tsconfig.json` rc 0. The ratchet gives rc 0: "201 files, 150 under __tests__; 41 errors: 41 in the baseline, 0 new; 0 stale". This equals the READY.
- **Digest STANDARD** (`digest.py --kind vitest`, the Spark UP, raw logs kept):
  - head: CHECKED PASS (150 / 1850).
  - head2: CHECKED PASS.
  - redfirst_round1: CHECKED FAIL (5, the right names).
  - redfirst_develop: CHECKED FAIL (2, the right names).
  - I read the raw rc beside each digest (0, 0, 1, 1), and each digest verdict agrees with its raw rc. No run was rc 1 with everything green, so G331-2209-5's parser blind spot was not exercised this gate.

## Q6. The PR body

Read through GraphQL (`scratch/pr.py`, saved as `scratch/prbody2209.txt`, 10,304 chars).
- **Tier-1 statement:** first, in bold: "TIER 1: product bytes change inside auth…". Present.
- **The new behaviour, stated truly:** "A body line for the user's own suffix is skipped ONLY when its count, trimmed, is exactly `0`. A malformed count … REFUSES, as at develop, so no case flips from refuse to allow any more." The probe confirms it: the head differs from develop only on exact-0 rows.
- **The fetch-failure path:** stated UNCHANGED, failing open and logging a warn "as before", and "This PR adds no log line and changes none". That is true: the probe shows warns only on non-200 and a throw, and the hunk is inside the loop only.
- **Refs only:**
  - The title and body say `Refs KS-2021` (count 1). The only ticket key present is KS-2021.
  - There is no closing word followed by a reference. The words "fix" and "fixed" appear only as "a fix round" and "fixed in round 2". A control line `Fixes KS-1` is hit by the same regex.
  - closingIssuesReferences is 0.
- **NO-PAIR:** the literal is present (2 hits).
- **Other PR state:** OPEN, not draft, base develop, headRefOid equals the pin, 2 commits, MERGEABLE. The only comment is the `linear` bot's (04:43Z).
- **One stale sentence:** "`trimEnd` (M8) and the case-insensitive compare (M7) are not addressed and were not re-measured". M8 is in fact killed by C4 (measured). See G332-2209-2.

**Gate 331's findings, one by one:**

| G331 item | status after round 2 |
|---|---|
| -1 Minor, fail-open on malformed own-suffix rows | **CLOSED**: measured fail-closed, equal to develop on every non-exact-0 row; R3 pins 5 shapes |
| -2 Note, two fail-closed spellings are not fail-closed | **CLOSED**: the optional-chain form was used, and N1 (the bare form) is killed by R3 |
| -3 Note, four mutants survived | **PARTLY CLOSED**: M3 and M8 are now killed (C4). M6 no longer applies (round 1's line is gone). **M7 carried** (harmless). New survivors N2, N6 and M9 (G332-2209-1) |
| -4 Info, the trigger is practically unreachable on live data | carried, unchanged (a fact about HIBP, not a defect) |
| -5 Info, the seedDemoUsers rc 1 and the digest parser blind spot | carried. Not seen in 5 runs here. The digest tool bug is unchanged and outside this PR |
| -6 Info, PR text | **CLOSED**: the `NO-PAIR` literal is present, the logging wording is corrected, and the live-format claim is attributed to gate 331 |

## Q7. Census

`scratch/census_gql.py`, raw rows in `scratch/census_rows_gql.tsv`: 101 open PRs, 445 file rows, every PR's files paged to totalCount and asserted.

| path | open PRs |
|---|---|
| `Blockchain/Dev/services/auth/src/services/password.ts` | [2209] |
| `…/__tests__/ks2021-hibp-range-match-needs-a-count-above-zero.test.ts` | [2209] |
| suffix `password.ts` anywhere | [2209] only |
| `services/auth/src/routes/auth.ts` (a caller) | [] |

- **Control:** `services/auth/src/routes/users.ts` maps to [2075, 2201], so it FIRED.
- **Negative control:** an absent path maps to [].
- No other open PR touches either PR path, and no PR touches the register or reset caller file.

## Q8. Spark shadow review (calibration row only, not the verdict)

Driver `scratch/spark_run.sh`, with copies in `scratch/spark/`. The model is Nemotron-3.5-Super-VL. It ran in 1 attempt, 37.0 s, `valid: true`, `missing_inputs: ["ticket text"]`.

**Deterministic half:**
- head 2eca13ad (tip), merge-base 581296f0, base tip cea1cdc2.
- Diff: 2 files, +93 -2.
- Targeted on the HEAD: 4 files, 47 passed / 0 failed.
- On the BASE product code: 45 passed / 2 failed.
- All of these equal mine.

**Spark verdict: GO WITH NOTES** (1 Major, 5 Notes).
1. **Major, "can flip a clean password to breached on a malformed count; the ticket text is missing":** misframed. Refusing a malformed own-suffix row is the intended fail-closed rule and equals develop. The rest of the item is a missing-input complaint, not a defect.
2. **Note, "the body's gate-331 measurements are not in facts.json":** true as bookkeeping. It also misquotes 2,006 as "2,066". I re-measured the corpus claim (Q1).
3. **Note, "rc 0 presented as a pass vs the hook's NOT a pass":** weak. The body says legs 3, 4 and 8 did not run and that it "is not a full pre-push pass".
4. **Note, "M7 and M8 survive":** half wrong. M8 is killed by C4 (measured). M7 survives.
5. **Note, Node 26 rather than Node 24:** a restatement of the body.
6. **Note, the hook incomplete:** a restatement of the body.

**Recall against this gate's findings:**
- G332-2209-2 (the stale M8 sentence): a partial hit with the wrong conclusion.
- G332-2209-1 (the survivors N2, N6 and M9): missed.
- G332-2209-3 (non-canonical zeros): missed.

**False positives:** 1 (the Major, misframed). Its verdict happens to sit one grade from mine.

## Findings

- **G332-2209-1 (Note, test gap): three mutants of the new line survive the 47 HIBP cells.**
  - **N2, `.trim()` on the count dropped.** It makes `S: 0` and `S: 0 ` refuse. That is the fail-closed direction, and the live format has no space after the colon.
  - **N6, `trimStart()`.** It is equivalent, because `line.trim()` already strips trailing characters.
  - **M9, `line.trimStart()` in place of `line.trim()` (new this gate).** In a CRLF body, a no-colon own-suffix row that is NOT the last line keeps its `\r`, stops matching, and allows silently.
    - R3 does not catch it, because its harness puts the row last with no trailing CRLF.
    - It is reachable only by a code regression that removes trailing trimming, and only under a malformed upstream row.
    - A one-row addition to R3 (the no-colon shape in the middle of a CRLF body) would kill it.
  - **M7** (a case-insensitive compare) is carried from gate 331, and it is harmless.
  - None of these affects today's behaviour. They are about what the cells pin.
- **G332-2209-2 (Info, PR text): one stale sentence.** The body says "`trimEnd` (M8) … not addressed and were not re-measured on the new line". Measured: M8 is killed by C4 (1 failed of 47, C4). M7 does survive.
- **G332-2209-3 (Info): non-canonical zeros refuse.** `S:00`, `S:0.0`, `S:-0`, `S:+0`, `S:0e0` and `S:0x0` all REFUSE at the head, as at develop.
  - This is consistent with the stated "exactly `0`" rule, and the body names `S:00`. It is the safe direction, and the live format sends no leading zeros (gate 331).
  - Recorded so that no one later "fixes" it toward `Number(...) === 0`. That spelling (N5) re-opens the empty-count allow, and R3 kills it.
- **G332-2209-4 (Info, gate conduct): load and work-dir departures.**
  - Two whole-suite red-first runs started above load1 8 (8.91 and 10.09). The round-1 one was re-run at 3.54 with an identical result. The develop one was not re-run (it is deterministic, and gate 331 measured it the same).
  - The Spark gate's work dir was in the session scratchpad, not `scratch/`, because `spark_gate.sh` refuses any path under WEDNESDAY (gate 329's precedent).
- **G332-2209-5 (Info, carried): the test file name still says `needs-a-count-above-zero`.** The rule is now "skip exactly 0". The seat flagged this itself (its finding (b)). A rename was not ordered, and the describe title and header comment carry the true rule.

No Major. No Minor. G331-2209-1 is closed. Nothing in the residue needs a round 3. If Wednesday wants G332-2209-1's M9 row and the G332-2209-2 sentence, they are ticketable follow-ups, not merge blockers:
1. Add a CRLF-middle no-colon row to R3 (kills M9).
2. Correct the M8 sentence in the body.
3. Optionally, rename the test file.

## NOT TESTED

- The register, reset and change-password routes end to end with the new matcher. Q4 is from the code and the unchanged diff; the ks1968 B1 and B2 route cells passed, with well-formed rows only.
- A live HIBP range: no live call was made this gate (gate 331's single 5BAA6 read is relied on for the live format). No test calls the real API.
- A real truncated or chunked HTTP body.
- Node 24 (everything ran on v26.8.1). A fresh install at develop cea1cdc2: I used symlinked existing installs, as gate 331 did.
- eslint, docs-fragments, `npm run audit:gate`, the pre-push hook and its legs (all quoted from the seat), and the four platform suites.
- The develop red-first whole-suite run under load1 < 8 (it ran at 10.09; see G332-2209-4).
- Linear: the KS-2021 ticket text and the seat's comment 30e32881 were not read.
- The seat's worktree `worktrees/s-r107-ks2021`: it was not found at that path in the shared checkout, and I did not search for it. My evidence is the pushed head itself.
- The merged tree (97ca0c6d) was not itself run through the suite. The control shows that the 3 develop-moved files are outside `services/auth`.
