# QA gate: tier 2 (G2) batch: Secuura/Blockchain #1764 (KS-1766) and #1765 (KS-1765)

- **Tier:** 2 (G2: test-only changes)
- **Gate model:** Claude Sonnet 5.5 (claude-sonnet-5-5), subagent of Wednesday. I did not author any of this work.
- **Window:** 2026-10-27 16:27Z to 16:56Z (2026-10-28 03:27 to 03:56 AEDT), plus write-up
- **Workspace:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate-t2-1028a/` (clone `repo/`, logs `out/`, gate scripts `gate-src/`, TMPDIR `/tmp/gt2`)
- **Pushed / merged / commented / edited: nothing.** No git write verb was run against anything but my own clone. Nothing was run against `!CODING/Secuura/Blockchain/2_Project_Files`. No docker, az, or network beyond fetch and ls-remote.
- **Gate clone tree at the end:** `git status --porcelain` is empty. The mutant scratch dir was moved to `out/_moved_zz_gate/`, because the rm hook refuses deletes. It is empty apart from an empty `m/`.
- **Processes:** I started one runaway vitest by mistake (PIDs 65577 and 65618), and stopped both by PID with kill -9. See F-A5. Every other process was one I started and it exited by itself.

## Brief deviation
The brief's fetch used `origin`. In a `--shared` clone, `origin` is the local cache `.../spark/cache/src`, whose develop is stale (`c56dd7c32`) and which has no `refs/pull/*`. The first fetch failed on that. I fetched from `git@github.com:Secuura/Distributed_Secuura.git` instead, the same URL the #1763 gate used. Pins below are from GitHub.

## Pins
`out/ls-start.txt` equals `out/ls-end.txt` (diff empty). Both equal the brief's pins.

| ref | sha |
|---|---|
| develop | abdeb51c7627459172760c3a279b03c61bbaeeec |
| refs/pull/1764/head | e93a5ea696e68493e6f0a475f7ccf433bdcbf685 |
| refs/pull/1765/head | 94b887351fb35fe7ea4a7ca784c6aa8c9e5988db |

Both PR bases (merge-base with develop) are `9b698b7aa1f8`. Nothing moved.

## BLUF

| PR | verdict | worst finding |
|---|---|---|
| #1764 KS-1766 | **GO** | INFO only. Text-only is proven at the token level. The cited log line exists at `routes/verification.ts:1067`. |
| #1765 KS-1765 | **GO WITH NOTES** | LOW: three survivors, each stated in the PR's own text (a predicate held in a name or `new RegExp`, a swapped predicate). Also LOW: the in-file "39 calls / 9 under test" is a base measurement, and the head has 42 / 12. |

**merge-tree against develop `abdeb51c7627`** (read-only `git merge-tree --write-tree`):
- **#1764:** clean. It printed a tree OID (`31db7462d514…`) and no conflicts.
- **#1765:** conflicts in exactly the two docs: `Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html` and `Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html`. The test file auto-merges (it is untouched by #1763). That is as expected. Both conflicts are the same append point. Develop now has its own section 77, so this PR's provisional "77" must be renumbered to 78 at merge time. That is resolve-time work, not a finding. I did not test the resolved merge.

## #1764 (KS-1766): GO

### F-A1: INFO: it changes exactly the two files, and only text
- `git diff --name-only 9b698b7aa1f8 gate/a` lists 2 files: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1543-…test.ts` and `…/ks1628-…test.ts`. The diff is +8/−4. There are no docs and no product code.
- **Measurement:** `gate-src/strip.mjs` walks the TypeScript syntax tree to its leaf tokens. That drops comments and whitespace but keeps every string, template and regex literal in full.
  - ks1543: 1550 tokens at base, 1550 at head, **0 differing**.
  - ks1628: 1516 tokens at base, 1516 at head, **1 differing**. Token 1067 is the `it(` title literal, `'RED KS-1628 G2: … and fetches no document'` becoming `'RED KS-1628 G2: … unanswered by the router'`. It is the one literal the brief named. Nothing else moves, including the `postToRouter(...)` template and the assertions.
  - Both head files parse with 0 diagnostics.
- **Control:** I changed `expect(status).toBe(200)` to `toBe(201)` in a copy of ks1543. The same comparison reported exactly 1 differing token.
- The ks1628 comment is new, so comments differ, but they are stripped. The comment says "see the header and the comment below". I did not check that header claim ("a fetch count reads 0 with the route present or absent"). That is prose.

### F-A2: INFO: the cited log line exists, and it is named by message
- `Blockchain/Dev/services/api-gateway/src/routes/verification.ts:1067` is `log('error', 'Failed to fetch document types', { error: err instanceof Error ? … })`. This is the line that describes a thrown non-Error with the fail500 describer, which is what the comment says. `:1068` is the 500 response body.
- The same message string also appears at `routes/admin.ts:643`. That is only a response body (`res.status(500).json(…)`), with no `log(` call. So "the log line by its message" is unambiguous for a log call, and a grep for the string alone returns 3 hits. Nobody would be misled, but the comment does name the file.
- No other title references "fetches no document" (`git grep` finds only the new KS-1766 comment).

### F-A3: INFO: tests at the head
- The two files: 2 files, **18/18** passed, rc 0 (`out/A-two.log`).
- api-gateway full suite (run through `npm --prefix services/api-gateway run test -- run --testTimeout=120000`, so the cwd is the service dir): **124 files, 1212/1212**, rc 0, 48 s (`out/A-gw-suite.log`).

### F-A4: INFO: the docs escape clause
- The PR touches no `Projects Documents` file. The clause is consistent with a test-comment and test-title-only change.

### F-A5: INFO (process, mine, not the PR's)
- My first full-suite attempt used `npx exec` without a service cwd. vitest picked `/Volumes/DevMASTER/WEDNESDAY` as its root and started to crawl the whole workspace. I saw "RUN … /Volumes/DevMASTER/WEDNESDAY" after about 10 minutes and killed it. It ran against read-only inputs and wrote nothing to the repo. Its log was overwritten by the correct run. The result above comes from the correct run.

## #1765 (KS-1765): GO WITH NOTES

### F-B1: INFO: the diff, read whole
- 3 files: the ks1000 test (+174/−9 net), plus both docs with append-only inserts (+23 and +26).
- **Item 3, `AUTH_GREEN_SUMMARY`:** it becomes `/(?<!\d)0 new; 0 stale baseline entries/`. The new cell uses a captured checker line (`GREEN_LINE`) and four worse lines (10, 20 and 100 new, and 11 errors with 10 new), all of which `toContain` the old substring. All four are required to throw. There is a stale side control.
- **Item 1, the depth scan:** `matchingClose` steps over quoted strings, including backslash escapes, and over template literals. It counts `[` and `{`, and returns the matching close or `src.length` when it never closes. `runsComparedAsOneValue` flags an `expect([{` opening whose matched span contains both `.status` and `.out`. The table grew from 4 to 8 forbidden rows (index ahead of each field, an index inside an index, object with an index, an array of arrays, quoted `]`, escaped quote then `]`, never-closed) and from 4 to 8 permitted rows.
- **Item 2, the call-site pin:** `ordinaryCalls` takes the `expectRun` calls that are not inside `expect(() => …)` or `thrownBy(() => …)`. `whyTrivial` requires a numeric status and a predicate that is neither `''` nor a RegExp that matches three probe strings. A floor cell requires at least 30 ordinary calls.
- I found no logic error. The new helper names (`callsTo`, `parse`, `cellsTitled`, `ts`) already exist earlier in the file, and the file type-checks (see F-B6).

### F-B2: INFO: test runs at the head
- ks1000 file (`--testTimeout=300000`, cwd = services/auth through npm `--prefix`): **99/99**, rc 0, 37.5 s (`out/B-ks1000.log`). That matches "84 to 99".
- services/auth full suite (`--testTimeout=60000`, cwd = services/auth): **105 files, 1188/1188**, rc 0, 34 s (`out/B-auth-suite.log`). That matches the docs' "1188 of 1188". Node is v26.8.1 (Current, not LTS).
- The base's 84 cells, I did not run. I took it from the PR text.

### F-B3: INFO: my own mutants of the head file
- Script: `gate-src/mutants.py`; results: `out/mutants.json`, `out/mutants2.json`, `out/mutants.log`. Method: a mutant is written to `services/auth/zz_gate/m/x.test.ts`. That is outside `src/__tests__`, at the same depth, so the file's `__dirname` paths still resolve. Each mutant is parsed with `ts.transpileModule` before it runs. The original file's sha256 is `890576bb54fda89cff8f17746ad9df62b343e2bef9203d86a8e22c1f22112345` before and after (equal, printed by the script). The original is never edited. The no-op control passed 99/99.

| mutant | result | killing cell(s) |
|---|---|---|
| M1 summary back to the substring string | killed (1) | "AUTH_GREEN_SUMMARY is not a substring of a worse summary" |
| M1b RegExp with the lookbehind removed | killed (1) | same cell |
| M2 depth scan: no string skipping | killed | "a quoted close bracket ahead of the fields", "an escaped quote, then …" (RED (a)) |
| M2b backtick not skipped | killed (1) | CONTROL (a): "a template literal holding a bracket … is NOT flagged" |
| M2c no backslash-escape handling (a first attempt did not parse; I redid it and it parses) | killed (1) | "an escaped quote, then a quoted close bracket, ahead of the fields" |
| M2d single quote not skipped | killed | "a quoted close bracket …", "an escaped quote …" |
| M3 `matchingClose` ignores depth (first close) | killed | "an INDEX ahead of .status", "… ahead of .out" and the other nested rows |
| M3b unclosed returns `open`, not `src.length` | killed (1) | "an array that never closes" |
| M3c `BOTH_FIELDS` needs only `.status` | killed (1) | CONTROL (a): "each field in an array of its own is NOT flagged" |
| M3d the guard never flags | killed | "no cell in this file compares a run as one value", plus RED (a) rows |
| M4 one ordinary call (line 404) drops its predicate | killed | "every ordinary expectRun call passes a numeric status and a predicate that can fail" |
| M5 predicate emptied `''` | killed | same cell |
| M5b predicate `/.*/` | killed | same cell |
| M5d status `0 + 0` (non-literal) | killed | same cell |
| M6 one call removed (`void 0`) | killed | same cell and the ORDINARY_CALLS_FLOOR cell |
| M6b one call becomes a bare status check | killed | same two cells |
| M9 `AUTH_GREEN_SUMMARY` becomes `/./` | killed | "AUTH_GREEN_SUMMARY can fail …" and the ten-new cell |
| **M5c** predicate `new RegExp('')` | **SURVIVES** (99/99) | none |
| **M7** predicate swapped for another literal that can fail (`'baseline'`) | **SURVIVES** | none |
| **M8** `const PASSED = ''` (the identifier used at 2 ordinary sites) | **SURVIVES** | none |

### F-B4: LOW: three survivors, all within the PR's stated limits
- M5c and M8 survive because `whyTrivial` judges only a literal. The PR says so in its comment ("a predicate held in a name or a template is taken as present, because only a literal can be judged"). M7 is the documented "NOT proved: … a predicate swapped for another that can fail".
- **How much it matters:** my AST read shows 5 of the 30 ordinary calls have a non-literal predicate (`AUTH_GREEN_SUMMARY` at `:223`, two template strings at `:1010` and `:1131`, and `PASSED` at `:1175` and `:1203`). `AUTH_GREEN_SUMMARY` has its own dedicated cells, which killed M9. `PASSED` does not, and M8 shows that emptying it passes 99/99. So the pin covers 25 of 30 ordinary calls, not 30. The PR text does not claim all 30 are pinned against emptying. The doc says "every ordinary call" and then lists the exclusion, so this is a note, not a defect.
- **Sibling weakness left in place:** three ordinary calls still use the bare substring `'0 new'` (`:581`, `:628`, `:915`; line numbers at the head are 24 higher than at base). That is the same shape as the weakness item 3 fixes for `AUTH_GREEN_SUMMARY`: `'0 new'` is a substring of `'10 new'`. Each of these also asserts a status, so the exposure is the same as the one the PR fixed (a worse summary under a right status). The PR scopes item 3 to `AUTH_GREEN_SUMMARY` and never claims the others, so this is out of scope for the claim, but worth a follow-up ticket. The `'1 in the baseline, 0 new…'` strings are not weak (`', 10 new'` does not contain `', 0 new'`).

### F-B5: LOW: "39 calls" is true at the base, not at the head
- I counted `expectRun` calls by syntax tree with `gate-src/count.mjs`. **Base: 39 calls (9 under test, 30 ordinary), and 47 textual `expectRun`.** **Head: 42 calls (12 under test, 30 ordinary), and 65 textual.**
- So the claim "39" holds at the measured base, and the ticket's "42" is the head's figure. The head's extra 3 are the new `expect(() => expectRun(…))` calls in the ten-new cell. Ordinary stays 30 either way, and the floor is 30.
- The in-file comment (`"The syntax tree holds 39 calls … 9 of them sit inside expect(() => …)"`) and docs section 77.3 and the Figures row all say 39 / 9. A reader counting the head's tree gets 42 / 12. This is a stale figure, not a wrong measurement, and the comment does say "measured … at develop ba9e8fad7f9d".
- The textual count in the comment is 43 and the AST base is 47 textual, which differ from each other. I did not trace which occurrences the author excluded (definition, doc comment, two mutant strings, per the comment). This is the same kind of count drift.

### F-B6: INFO: independent check of the depth scan
- `gate-src/scan.mjs` copies the scanner and runs ten cases. Nine behave as intended (both field orders, nested index, quoted `]`, an unclosed array, a template with a `${…}`, a nested template, a closed array followed by fields elsewhere).
- One differs, and it is the documented limit: an apostrophe inside a `//` comment within the value (`[a, // don't \n b]`) is read as a string start, so the scan runs on and flags the call. It fails closed (a false positive, never a miss). The PR's "Not covered: a comment or a regular-expression literal inside the compared value" says this.
- **Real-file control:** the new scan flags **0 of 675** `*.test.ts` files under `services/` and `packages/` at the head, including ks1000 itself. That matches the PR's "0 of 105 in services/auth". The PR's own table plants the shape and finds it.
- `check:test-types` for the ks1000 file's own types: the checker is exercised inside the file's REAL cell, which passes in the 99/99 run. I did not run `scripts/preflight/test-types-ratchet.sh` leg 16 separately (see NOT TESTED).

### F-B7: INFO: docs
- `systemTest/__tests__/support/html_docs_check.mjs` on both docs at the head: rc 0, no findings (`out/B-docs-check.txt`).
- `systemTest/__tests__/html_docs_matrix.test.sh`: **18 passed, 0 failed** (`out/B-docs-matrix.txt`).
- **Append-only against base `9b698b7aa1f8`,** by difflib opcodes:
  - Flow Diagrams: one `insert`, 23 lines at line 4981 (of 4983 lines at base).
  - Cheat Sheet: one `insert`, 26 lines at 5050 (of 5052).
  - Nothing is replaced or deleted in either doc.
- The docs' figures (99 cells, 105 files, 1188 tests, 42 in the baseline) match what I measured at the head.
- Develop now carries its own section 77 (from #1763), so this PR's provisional 77 will clash and needs renumbering at merge. The conflict is on both docs at the same append point.

## NOT TESTED
- **The resolved merge of #1765 onto develop `abdeb51c7627`.** I only ran merge-tree. I did not resolve the two doc conflicts, renumber section 77, or re-run ks1000 and the doc checks on the result.
- **#1764 and #1765 together** (they touch different services and different files, apart from #1765's docs).
- **Preflight leg 16 (`test-types-ratchet.sh`) as a script,** and the other pre-push hook legs. I ran the ks1000 file, whose REAL cell runs the checker for services/auth.
- **The ks1000 file at base (84 cells).** I took the number from the PR text.
- **Node 24 (LTS).** Everything ran on Node v26.8.1.
- **The four platform suites** (Schemathesis, Akto, Playwright, k6), and docs rendering in a browser (the doc check is static).
- **Whether the right predicate is the right one at each of the 30 call sites** (the PR itself says this is not proved).
- **api-gateway at the #1765 head, and auth at the #1764 head.** Each suite ran only at its own PR's head.
