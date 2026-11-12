PR 2209: GO WITH NOTES (at head 2db221d43ad8; tier 1)

Gate 331, tier 1 (Opus), one session, 2026-11-12 04:46Z to 04:57Z (15:46 to 15:57 AEDT). Findings only: nothing fixed, posted, mailed, pushed, merged, or written to Linear, GitHub or a board.

Where things ran:
- Everything that wrote ran in my own clone `scratch/repo` in this folder: a fresh `git clone --filter=blob:none` with a sparse checkout (`scratch/setup.sh`), plus fetches of PRs 2201 and 2075 for the census. Write verbs (fetch, merge-tree) ran only there.
- `node_modules` came from read-only symlinks (`scratch/nm.sh`). The root one and `packages/shared/dist` point to gate 313's `r2` install. I did not use the shared checkout's own dist because it is stale: it has no `zod3-compat`, and the first run failed with ERR_MODULE_NOT_FOUND. `services/auth/node_modules` points to the shared checkout's copy. `packages/shared/src` differs from r2 in one test file only.
- In the shared Secuura checkout I ran read verbs only, with `GIT_OPTIONAL_LOCKS=0`.
- Every file I changed in the clone was restored and checked by blob: password.ts `e8eb9633828e`, the ks2021 test `e0ab25a3f525`. `git status` in the clone shows only the three symlinks.
- Whole-suite runs used `cwd` = the auth package, set through python `subprocess` (`scratch/whole.py`). Several auth tests read `process.cwd()`, and a run from the WEDNESDAY working directory fails 3 cells for that reason alone (my first attempt; discarded).
- Machine: Node v26.8.1, macOS arm64, load1 about 5 to 12.
- Spark: the shadow review was SKIPPED as commissioned (the Spark is mid-model-test). The digest STANDARD ran in `--no-spark` (parser-only) mode, for the same reason.

## Pins

| when | develop | refs/pull/2209/head |
|---|---|---|
| start, 04:46:06Z (`scratch/pins_start.txt`) | 581296f039b4890ccf6f56e1c1f13575dc1098d4 (= commission) | 2db221d43ad8b06a58a6c890c75758b94434ae56 (= commission) |
| end, 04:57:04Z (`scratch/pins_end.txt`) | unchanged | unchanged |

Neither pin moved. PR 2201 read 50c32501e60c at the end, which equals the READY's pin.

**Shape of the PR:**
- ONE commit, 2db221d4, whose parent is develop 581296f0. The merge-base equals develop, and `rev-list develop..head` is 1.
- `merge-tree --write-tree origin/develop p2209` gives rc 0 and tree e2c3eed0f899, which equals the head's own tree.
- `diff --numstat`: password.ts +3 -2 and the new test +65 -0. GraphQL agrees: 68 / 2 / 2 files.

## Summary

The fix is correct for what KS-2021 asks:
- A count-0 row for the user's own suffix no longer refuses.
- Every real breach row with a count of 1 or more still refuses.
- Every READY number reproduces: R1 and R2 red on develop's password.ts, 5 of 5 green at the head, and the whole suite 149 / 1,839 on develop and 150 / 1,844 at the head.

Wednesday's lead question is answered by measurement:
- The head's `Number(countText) > 0` fails OPEN on six malformed shapes of the user's own row that develop refused.
- A fail-closed shape, `countText?.trim() !== '0'`, fixes KS-2021's padding case identically, and passes every one of the 41 HIBP-related cells.
- On my 25-shape corpus, that fail-closed shape differs from develop ONLY on rows whose count reads exactly `0`.

That is one Minor (G331-2209-1). It does not block: it gives no new capability to an adversary, and the live format conforms (measured). Wednesday's lean (a fail-closed shape plus a pinning cell) is the better fix, and a one-line, one-cell fix round is measured-safe. If Wednesday prefers that before merge, this verdict becomes GO on that round, once it is re-gated.

## Q1. Is the match correct?

**The upstream format.** I made ONE read-only live GET: `https://api.pwnedpasswords.com/range/5BAA6` with `Add-Padding: true` at 04:50:21Z (`out/hibp_live_5BAA6.txt`, headers in `out/hibp_live_headers.txt`). That is the prefix of SHA-1("password"), and no user data was sent.
- The answer was HTTP 200, `text/plain`, 78,731 B.
- It had 2,006 lines, CRLF-separated: 2,005 CRLF, 0 lone LF, and no trailing CRLF.
- **All 2,006 lines match `^[0-9A-F]{35}:\d+$`** (0 nonconforming).
- 28 rows have count 0 (the padding). No count has a leading zero.
- The known row `1E4C9B93F3F0682250B6CF8331B7EE68FD8:52372427` is present, which is my positive control.
- So the real service sends uppercase hex, a single colon and a plain decimal count. This confirms the body's "the service always sends counts" for one range, which the seat had not measured.

**The code at the head** (password.ts:175-178):
- `body.split('\n')`, then `line.trim().split(':')`, then `hashSuffix === suffix && Number(countText) > 0`.
- `suffix` is `sha1.toUpperCase().slice(5)`.

**Measured with the real module** over a fake fetch (probe `out/zzprobe-gate331.test.ts.ran`, driver `scratch/mut.py`, table `out/probe_table.md`, raw `out/probe/*.json`). There are 25 row shapes for the user's own suffix. Each runs CRLF and LF, with the row last and in the middle (4 variants), and the 4 variants agree on every row.
- **Case:** a lowercase suffix row never matches, at develop or at the head. That is unchanged, and it is correct for the uppercase API.
- **CR / CRLF:** `line.trim()` removes the `\r`, so CRLF and LF bodies give identical results, last or middle.
- **Spaces:**
  - `S: 3`, `S:3 ` and `S:\t3` match. `Number` ignores surrounding whitespace, and `trim` handles the line ends.
  - `S :3` (a space before the colon) does not match, at develop or at the head (unchanged).
  - ` S:3` (a leading space) matches.
- **Real breach rows:**
  - `S:1`, `S:3` and `S:3861493` refuse.
  - So do `S:1e3`, `S:0x10`, `S:Infinity`, `S:0.5` and `S:3:4` (an extra field is ignored).
- **Padding:** `S:0`, `S: 0`, `S:0 `, `S:00` and `S:0:4` allow. That is the fix.
- **Reproduced:** with develop's password.ts and the new test, 2 failed (R1 and R2, `expected true to be false`) and 3 passed. At the head, 5 of 5 pass (`out/t_mut_DEVELOP.log`, `out/t_mut_HEAD.log`).

**Mutants.** Each ran against ks2021 + ks1968 (B1, B2) + ks1868-password-verify-hibp, 41 cells (`out/mutants.json`, `out/t_mut_*.log`).

| mutant | failed | killed by |
|---|---|---|
| develop's line (suffix only) | 2 | R1, R2 |
| M1 `>= 0` | 2 | R1, R2 |
| M2 suffix compare dropped | 6 | R1, R2, C3, and 3 ks1968 clean-password controls |
| M4 `> 1` | 1 | C2 |
| M5 `\|\|` in place of `&&` | 6 | the same six as M2 |
| **M3 `line.trim()` removed** | **0, SURVIVES** | the probe changes only the leading-space row (` S:3` allows); `Number` swallows the `\r` |
| **M8 `trimEnd()` in place of `trim()`** | **0, SURVIVES** | the same single row |
| **M6 `parseInt(countText,10)`** | **0, SURVIVES** | the probe changes `S:0.5`, `0x10` and `Infinity` (to allow) and `S:1,234` and `S:3abc` (to refuse) |
| **M7 case-insensitive compare** | **0, SURVIVES** | the probe changes only a lowercase row (to refuse); harmless |

The commission's mutants (`>= 0`, the dropped suffix compare) are killed. The survivors change behaviour only on shapes the live service does not send. M3 and M8 matter only for a fail-closed string compare: there, a kept `\r` would read `'0\r' !== '0'` and refuse padding in CRLF bodies, which is why my recommended shape trims.

## Q2. The behaviour change (the lead question)

**(a) What the head returns.** In the table, B means breached (refuse), a means allow, and a! means allow via the catch path. All rows are measured.

| row for the user's own suffix | develop | head |
|---|---|---|
| `S:` (empty count) | B | **a** |
| `S` (no colon) | B | **a** |
| `S:abc` | B | **a** |
| `S: 3` | B | B |
| `S:3\r` (CRLF, middle or last) | B | B |
| `S:-1` | B | **a** |
| `S:1,234` (thousands separator) | B | **a** |
| `S:3abc` | B | **a** |

Six malformed shapes flip from REFUSE to ALLOW. Every flip is **silent**: no log line is written on that path, unlike a non-200 answer or a throw, which log "failing open".

**(b) Would a fail-closed shape fix KS-2021 equally, with no other change?** Measured YES for one shape and NO for two others. All three shapes ran on the same corpus and the same 41 cells.

| shape | 41 cells | `S:0` / `S: 0` / `S:0 ` / `S:0:4` | `S:00` | `S:` | `S` | `S:abc`, `-1`, `1,234`, `3abc` | differs from develop on |
|---|---|---|---|---|---|---|---|
| head `Number(countText) > 0` | 41/41 | a | a | a | a | a | 11 rows (the fix plus 6 fail-open rows plus `S:00`) |
| **FC1 `countText?.trim() !== '0'`** | **41/41** | **a** | B | **B** | **B** | **B** | **only the 4 exact-`0` rows (the fix itself)** |
| FC1b `countText.trim() !== '0'` (the commission's literal form) | 41/41 | a | B | B | **a!** (TypeError, caught, fails open) | B | the fix plus `S` |
| FC2 `!(Number(countText) === 0)` | 41/41 | a | a | **a** (`Number('')` is 0) | B | B | the fix plus `S:00` plus `S:` |

- **FC1 is the fail-closed shape that fixes KS-2021 with no other behaviour change.** On every non-zero, empty, missing, negative or garbled count it equals develop. The only padding-like row where it still refuses is `S:00`, which the live service never sends (0 leading-zero counts in 2,006 lines).
- The commission's literal `countText.trim()` must NOT be used as written. A row with no colon throws a TypeError inside the try, and the catch fails open. It logs "HIBP lookup failed", so it is not silent, but it still allows.
- `!(Number(countText) === 0)` still fails open on an empty count.

**(c) Graded: G331-2209-1, Minor.**

**Who could set a breached password, and when:** any user at register, reset or change-password, if the HIBP answer is a 200 whose row for that password's exact suffix carries an empty, missing, negative or non-decimal count.

**Under what upstream failure:**
1. **Format drift.** For example, counts sent with a thousands separator, or a suffix sent with no count. The check would then silently stop refusing every affected breached password, with no log line, where develop would have kept refusing (it ignored the count). This is the material risk, because it is silent and could cover the whole corpus at once.
2. **A forged or tampered 200.** This adds nothing for an adversary: anyone who can forge the body can already drop the row, and the function already fails open on non-200 answers, throws and timeouts (Kam's ruling, unchanged).
3. **A truncated body.** A cut after the colon gives `S:`, which allows at the head and refused at develop. In practice a truncated stream usually throws, and the catch already fails open.

**Why Minor and not Major:**
- It weakens no control against an attacker. The rest of the function already fails open by ruling.
- The live format conforms today (measured).
- No cell pins it, and the fail-closed alternative costs nothing.

**Recommendation (Wednesday's lean, confirmed):** change the condition to `hashSuffix === suffix && countText?.trim() !== '0'`, and add one table cell over `[S:, S, S:abc, S:-1, S:1,234]` expecting `true` (refuse). Against the head, that cell is red on all 5 shapes (measured above), and FC1 turns it green with R1, R2 and C1 to C3 unchanged.

## Q3. Callers

All three call sites at the head have the same shape: `if (await isPasswordBreached(pw)) throw new ValidationError(BREACHED_PASSWORD_MESSAGE, …)`. None of them wraps the call in a try or treats a failure differently.
- register: `routes/auth.ts:214`, after the strength check and before the hash.
- reset: `routes/auth.ts:898`, after the token and the user are proven and before the hash and token consumption.
- change-password: `routes/users.ts:1009`, after the current password and strength checks and before the hash and the write.

`isPasswordBreached` never throws to its callers. Everything after the `HIBP_ENABLED` check is inside one try/catch that returns false.

**The fetch-failure path is fail-OPEN at develop. That is a pre-existing fact and it was ruled:** the comments at all three sites say "an outage allows it".
- A non-200 answer: `logger.warn('… non-200 — failing open')` and `false`.
- A thrown fetch or a 2 s timeout: `logger.warn('… failed — failing open')` and `false`.
- Measured by the probe for every shape: `non-200 503` gives a, `fetch throws` gives a!, and an empty body gives a.

**This PR did not change that path.** The diff is the single hunk at lines 173-178, inside the line loop. No caller file is in the diff.

## Q4. Suite and controls

The whole `services/auth` vitest suite ran (not the reduced set). Logs are in `out/t_whole_*.log`, with JSON reports in `out/whole_*.json`.

| run | files | tests | rc |
|---|---|---|---|
| head, run 1 (`head`) | 150 passed | 1844 / 1844 | **1**: `Errors 1 error`, the known `No "seedDemoUsers" export … on the userRepo mock` from the 2000 ms timer at routes/auth.ts:65, attributed to ks1868-auth-login-publish-event-unreadable-throw (G331-2209-5) |
| head, run 2 (`head2`) | 150 passed | 1844 / 1844 | **0** |
| red first: password.ts at develop's blob f7f463e0, new test kept (`redfirst`) | 1 failed / 149 | **2 failed (R1, R2)** / 1842 passed | 1 (the 2 failures, plus the same seedDemoUsers error, this time attributed to ks1967) |
| develop baseline: password.ts at develop, new test moved aside (`develop`) | 149 passed | 1839 / 1839 | 0 |

**Whole-ness:** the JSON report's 150 file names are **set-equal** to a `find src -name '*.test.ts'` list (150, `out/json_files.txt` and `out/find_files.txt`, empty diff). The find list includes ks2021. The deltas are +1 file and +5 tests, which equals the READY.

**Planted controls** (`scratch/planted.sh`):
- A failing cell appended to the ks2021 test gives rc 1, 1 failed and 5 passed (`out/t_planted_cell.log`).
- A type error appended to password.ts gives tsc rc 2 with 1 error at password.ts(318).
- Both were restored and checked by blob.

**Typecheck** (`scratch/tsc.py`):
- `tsc --noEmit -p services/auth/tsconfig.json` gives rc 0 at the head.
- The test ratchet, `scripts/typecheck-tests/check.cjs services/auth`, gives rc 0: "201 files, 150 under __tests__; 41 errors: 41 in the baseline, 0 new; 0 stale". This equals the READY's 41.
- Neither log names password.ts or ks2021 (0 hits).

**Digest STANDARD** (`digest.py --kind vitest --no-spark`, raw logs kept):
- head: PASS (150 / 1844 / 0).
- head2: PASS.
- develop: PASS (149 / 1839).
- redfirst: FAIL (2 failures, the right names).

The parser marked the rc-1 head run PASS. It does not read vitest's `Errors N error` line (G331-2209-5).

## Q5. Census

`scratch/census_gql.py`, raw rows in `scratch/census_rows_gql.tsv`: 102 open PRs, 442 file rows, every PR's files paged to totalCount and asserted.

| path | open PRs |
|---|---|
| `Blockchain/Dev/services/auth/src/services/password.ts` | [2209] |
| the ks2021 test | [2209] |
| suffix `password.ts` anywhere | [2209] only |

- **Control:** `services/auth/src/routes/users.ts` maps to [2075, 2201], so it FIRED.
- **Negative control:** an absent path maps to [].
- **PR 2201** (head 50c32501e60c) touches `routes/users.ts` and its own ks1873 test only. Its single users.ts hunk is at line 678 (`POST /admin/create`). That is not the change-password handler and not line 1009, and it shares no file with 2209. **No overlap.**
- PR 2075 also touches users.ts, at lines 838 and 840 (`PATCH /admin/:id`). That is not the call site either.

## Q6. The PR body

Read through GraphQL (`scratch/pr.py`, saved as `scratch/prbody2209.txt`, 8,535 chars).
- **Tier-1 statement:** present in the first paragraph, "TIER 1: product bytes change inside auth…".
- **The behaviour change:** stated twice, under "Behaviour change to read" and again in the Notes for the gate, with "No cell pins the malformed-row case". It is accurate. The Notes line "it fails open the same way a non-200 answer or a thrown fetch already does" is true about the outcome. It is not true about logging: the malformed-row path is silent, while the other two paths log. See G331-2209-1.
- **Refs only:** the title and body say "Refs KS-2021". There are 0 closing words, and the Refs control counts 1. closingIssuesReferences is 0.
- **NO-PAIR:** stated in substance: "raised unchanged under the coordinating seat's no-pair ruling, so this PR adds no pair". The literal token `NO-PAIR` is not in the body (Info only).
- **Other PR state:** OPEN, not draft, base develop, headRefOid equals the pin, 1 commit, MERGEABLE. The only comment is the `linear` bot's.
- **Body numbers:** the ones I could re-run all reproduce: 149 / 1839, 150 / 1844, 2 red then 5 green, tsc 41, and +3 -2 / +65.

## Findings

- **G331-2209-1 (Minor, behaviour change, fail-open): the malformed own-suffix row now ALLOWS, silently.**
  - At the head, `S:`, `S`, `S:abc`, `S:-1`, `S:1,234` and `S:3abc` return not-breached where develop refused. No log line is written and no cell pins it.
  - Consequence: if HIBP's count format ever drifts, the breach check at register, reset and change-password silently stops refusing the affected breached passwords. There is no new adversary capability.
  - Fix, measured: `hashSuffix === suffix && countText?.trim() !== '0'` fixes KS-2021 identically (41/41 cells) and differs from develop only on exact-zero rows. Add a 5-shape refuse cell.
- **G331-2209-2 (Note, guidance for the fix round): two of the three fail-closed spellings are not fail-closed.**
  - `countText.trim() !== '0'` throws on a no-colon row and fails open through the catch.
  - `!(Number(countText) === 0)` allows an empty count.
  - Use optional chaining with trim (FC1).
- **G331-2209-3 (Note, test gap): four mutants survive the 41 HIBP cells.**
  - The survivors are trim removed, `trimEnd`, `parseInt` and a case-insensitive compare. All three fail-closed shapes also pass all 41 cells, so nothing distinguishes fail-open from fail-closed (this confirms the READY's own finding (a)).
  - The survivors change behaviour only on shapes the live service does not send.
- **G331-2209-4 (Info): KS-2021's trigger is practically unreachable on live data.**
  - Padding rows are hashes absent from the corpus. A padding row equal to a user's own 35-hex suffix needs a roughly 140-bit coincidence. The live range had 28 padding rows in 2,006.
  - So the fix is correctness hygiene with about zero live effect, and the fail-open of G331-2209-1 matters only under format drift. Neither direction changes anything on today's live format.
- **G331-2209-5 (Info, pre-existing, not this PR): two whole-suite runs out of four ended rc 1 with every test green.**
  - The runs were head run 1 and the red-first run, at load1 11 to 12. The cause is the `seedDemoUsers` mock error from the 2000 ms timer at routes/auth.ts:65 (not in the diff).
  - The READY saw it in 0 of 2 runs. The rate is load-dependent and I claim none.
  - Separately, the digest STANDARD's vitest parser marks a run PASS when vitest prints `Errors 1 error` and exits rc 1. That is a blind spot in the digest tool, not in the PR.
- **G331-2209-6 (Info, PR text):**
  - The literal `NO-PAIR` token is absent, though the no-pair ruling is stated.
  - The Notes line "fails open the same way a non-200 … does" omits that this path does not log.
  - "The service always sends counts (not measured by this seat)" is now measured true for range 5BAA6.

No Major. One Minor.

## NOT TESTED

- The register, reset and change-password routes end to end with the new matcher. Q3 is from the code; the ks1968 B1 and B2 route cells passed, but they use well-formed rows only.
- More than ONE live HIBP range (5BAA6). Other ranges, or a body with zero padding rows, were not sampled. No live probe ran from a test.
- A real truncated or chunked HTTP body, to see whether `res.text()` throws or returns a partial line.
- Node 24 (everything ran on v26.8.1). A fresh install at develop 581296f0: I used symlinked existing installs, and the root lockfile changed in KS-2176.
- eslint, docs-fragments, `npm run audit:gate`, the pre-push hook and its legs (all quoted from the seat), and the four platform suites.
- The Spark shadow review (SKIPPED by commission, because the Spark is mid-model-test). The digest ran parser-only (`--no-spark`) for the same reason.
- Linear: the KS-2021 ticket text and the seat's comment 5915b937 were not read.
- The held patch's sha256 (09c98fbb953c06b0) against the pushed diff: I did not compare them. My Q1 is the pushed diff itself.
