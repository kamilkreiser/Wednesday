## QA GATE - TIER 1, round 1: GO WITH NOTES

**Surface check (top line):** a test-only PR on the front-door API-key check (auth surface). It changes zero product bytes (proved below). The two new cells pin exactly what KS-1788 item 3 asks for. A 403 from the security service's `/api/keys/validate` is a **rejection**: 401 `Invalid API key`, nothing forwarded, a ~30 s negative cache entry, and the next request is answered from that entry. A 429 is **not** a rejection: 503 `SERVICE_UNAVAILABLE`, nothing forwarded, nothing cached. All three of the #1785 gate's surviving mutants named in the ticket (F7, F8, F18) are now red. Three neighbouring mutants of the same predicate still survive every cell: 408 dropped, the 500 boundary moved to 501, and 401 made retryable. The PR's own docs generalise the claim to "a plain 4xx", which reaches further than the cells do. That gap is Minor (F1). TIER 1 is right.

**PR:** Secuura/Distributed_Secuura #1827, "Refs KS-1788: key check pinned both ways, 403 is a rejection and 429 is not (item 3)" (Seat T 7th)
**Head:** `9b00fcd0bc203b015cec5f087aa049d703b18a70`. `git ls-remote` of refs/pull/1827/head showed this SHA at the start (2026-10-30T02:07:31Z) and at the end (02:17:17Z). It matches the claim.
**Develop:** `40c06084919d5aff132e82693cd60d513cb40ba7` at both reads. The PR is built on `530f091120d5` (merge-base). Develop is 1 commit ahead: #1823 (KS-1798/1799, originate gdpr + the two html docs). The diff `530f0911..develop -- services/api-gateway` is empty.
**Gate:** QA gate 31. Findings only. I fixed, commented, pushed, merged and deployed nothing, and wrote nothing under `!CODING/`.

### Counts
1. **spark_gate (run first; `facts.json` is beside this file):** diff 3 files / +52 / -1, head asserted as tip, merge-base `530f0911`. Targeted on HEAD: **14 passed / 0 failed**. On BASE product code: 14 / 0. For a test-only PR that BASE column is expected (the product is the same), so it is not a red-first; the tampers in point 4 supply that. These counts are real, not the 0/0 runner defect: `--node-modules` pointed at my clone's hoisted root.
2. **Scope** (`git diff --stat` / `--numstat`, three-dot develop...pr1827): exactly the 3 declared files. The test file is +25/-1, the flow doc +11, the cheat sheet +16. **Zero product bytes:** the blob of `api-gateway/src/middleware/auth.ts` is `cf62049618d3` at develop, at 530f0911 and at head. Its sha256 in my clone is `33b19c8b01ce3d3e…`, the author's value, and it was the same after every tamper and at the end.
3. **The TIER-1 question.** I read `auth.ts` 172-322 and `authenticateToken` 427-445 at head.
   - `couldNotAnswer(status)` (l.204-206: `status >= 500 || status === 408 || status === 429`) has **exactly one caller**, `checkApiKey` l.298.
   - `checkApiKey` has two callers: `authenticateToken` l.432, and `validateApiKey` l.274. Repo-wide, `validateApiKey` is called only from tests; the security service names it only in comments.
   - When the predicate is true, `checkApiKey` returns `unavailable`: nothing cached, and l.437 answers 503 on required AND optional mounts.
   - When it is false on `!resp.ok`, l.299-300 caches `null` for 30 s and returns `rejected`: 401 on a required mount, and the KS-1207 fall-through on an optional one.
   - The 403 cell drives the false branch end to end. It checks the status, code, message, that nothing is forwarded, the negative entry and its TTL lower bound, the answer from the cache, and that validate was hit once.
   - The 429 cell drives the true branch. It checks the status, code, message, that nothing is forwarded, and that nothing is cached.
   - Both use the real app over a real HTTP stub, not a fetch mock. **So yes: they pin the property item 3 asks for.**
   - Precision on the brief's wording: the call under test is the key **validate** call to the security service, not the connector **exchange** at auth. The PR and the docs say "security service", which is correct.
4. **Tampers.** Instrument: `tamper.py`, beside this file (gate 30's harness). Each tamper replaces one anchor (count asserted to be 1). The mutant must transpile with no diagnostics first, and the mutant copy lives in the scratchpad `tamper_out/`, outside `src/` and `__tests__`. Each run is vitest json. Every tamper was restored by byte copy with sha256 `33b19c8b01ce3d3e` equal, and `git status` was clean at the end. Results on the PR's file (14 cells, `tamper_run1.txt`) and on all **20 api-gateway test files that touch key validation** (216 cells, `tamper_wide.txt`):

   | Mutant (auth.ts) | PR file (14) | 20 files (216) | Killed by |
   |---|---|---|---|
   | (a) author's: `=== 429` -> `=== 403` | 2 red | 2 red | both KS-1788 cells (author's 2 of 14 reproduced) |
   | (b) **F7**: 429 dropped from the retryable set (429 = rejection) | 1 red | 1 red | KS-1788 429 cell only |
   | (c) **F8**: every non-OK status unavailable (`status > 0`) | 1 red | 1 red | KS-1788 403 cell only |
   | (d) 401 added to the retryable set | **14/14 green** | **216/216 green** | **nothing** |
   | (e) 403 added to the retryable set | 1 red | 1 red | KS-1788 403 cell |
   | (f) 408 dropped from the retryable set | **14/14 green** | **216/216 green** | **nothing** |
   | (g) `>= 500` -> `> 500` (a 500 becomes a 30 s-cached rejection) | **14/14 green** | **216/216 green** | **nothing** |
   | (h) every 4xx unavailable (`>= 400`) | 1 red | 1 red | KS-1788 403 cell |
   | (i) **F18**: non-OK rejection not negative-cached | 1 red | 2 red | KS-1788 403 cell; auth.test.ts "caches null for invalid keys" |
   | (j) non-OK negative TTL 30 s -> 60 s | **14/14 green** | **216/216 green** | **nothing** (lower-bound only) |
   | (k) non-OK negative TTL 30 s -> 3 s | 1 red | 1 red | KS-1788 403 cell |
   | (l) a 429/5xx answer negative-cached while still answered 503 | 2 red | 2 red | KS-1788 429 cell; ks1240b SEC503 "...and is not cached" |
   | (m) non-OK `unavailable` path skips its log line | **14/14 green** | **216/216 green** | **nothing** |
   | (n) the non-OK 4xx branch returns `unavailable` (uncached) | 1 red | 2 red | KS-1788 403 cell; auth.test.ts |

   Baseline and final were both 14/14 and 216/216. Within the 216, the new cells are the **only** killers of F7 and F8, so at develop (where they do not exist) both survive.
5. **Whole api-gateway suite.** vitest 4.1.12, `--maxWorkers=3`, cwd `services/api-gateway`, each run started only when the 1-minute load was below 8 (`runsuite.py`; start loads 7.2 / 6.8 / 7.4 / 6.0). Two runs each side, alternating (`suites.txt`):
   - **HEAD 9b00fcd0:** 130 files, **1323/1323** in both runs, 0 skipped.
   - **develop 40c06084:** 130 files, **1321/1321** in both runs, 0 skipped.
   - The delta is +2, exactly the two new cells. The author's 1323 matches. Their 1321 was a projection; it is now **measured** (at develop, whose api-gateway tree equals 530f0911's).
6. **Docs.** `html_docs_check.mjs` (from the clone's `systemTest/__tests__/support/`) returned rc 0 on both docs at head and at develop. It returned rc 1 on scratch copies with one planted `<p>` of prose outside a table per doc; both were named. The content matches the measured facts: 14 cells, 2 of 14 under the tamper, sha `33b19c8b01ce3d3e`, 1323, 1321 labelled a projection.
7. **Predicted merge** (`merge-tree --write-tree origin/develop origin/pr1827`, in my clone): **rc 1, CONFLICT (content) in both html docs.** The test file merges clean. The cause: #1823 has landed on develop since this PR branched, and it appended its own section `122.` at the same place. See Merge-prep.

### Findings (none blocks this PR)
- **F1 (Minor, test strength, within the scope the PR's docs claim).** The rest of the retryable/rejection predicate has no cell.
  - **Which mutants live:** dropping 408 (f), moving the 5xx boundary to `> 500` (g) and making 401 retryable (d) all pass every one of the 216 key-validation cells.
  - **Why it matters:** each flips a status between "503, not cached" and "401, cached for 30 s". In g, a security-service **500** would lock a valid key out for 30 s with `Invalid API key`, which is exactly the KS-1240 failure mode.
  - **The overreach:** the flow doc heading (122) and the cheat sheet say "a plain 4xx from the security service is a rejection". The cells pin one 4xx (403) and one exclusion (429). The KS-1240 contract in `auth.ts` l.195 and the test header l.15 name "a 5xx, 408 or 429".
  - **Suggested pins:** a 408 cell (503, nothing cached), a 500 cell (503, nothing cached; the boundary), and optionally a 401 or 400 cell (rejection). They are one stub case each in the same file.
  - **Not fix-before-merge:** KS-1788 item 3 asked for "one cell with a 403 stub and one with a 429 stub", and that was delivered. Either add these cells now, or file them and soften the docs wording to "a 403" at merge-prep.
- **F2 (Note, design question for Kam, not this PR's defect).** The cell freezes "any non-OK status outside {5xx, 408, 429} is a key rejection, negative-cached 30 s".
  - The real `/api/keys/validate` never answers 401 or 403. `security/src/index.ts:775-779` skips JWT auth for that path, and the handler at l.1800 answers 400 (schema), 503 (KS-1370) or 200 `valid:false`.
  - So a 401 or 403 at the gateway would come from something **in front of** the security service (ingress or WAF). Today that would answer every key, valid ones included, `401 Invalid API key` for 30 s.
  - Pinning today's behaviour is what the ticket asked for, so this is fine to merge. But this PR now makes it a pinned contract, so whether an infrastructure 401/403 should count as "could not answer" deserves a ruling.
- **F3 (Note).** The negative-cache TTL is pinned only from below: `> 25_000` passes with 60 s (j). The new 403 cell copied this from control (iv), which has the same weakness. Pin `<= 30_000` too.
- **F4 (Note).** The `unavailable` log line on the non-OK path (`security service answered <status>`) is not pinned (m). Only the catch path's log is pinned, by the "logged as unavailable" cell (HANG key).
- **F5 (Note, the ticket's record).** KS-1788 says F18 "survives with all 40 cells green". At develop, `auth.test.ts` "caches null for invalid keys and does not re-fetch within TTL" already kills F18 (and n). So the #1785 gate measured a narrower set.
  - That cell's fetch mock returns `{ ok: false }` with **no `status`**. `couldNotAnswer(undefined)` is false, so it exercises the rejection branch only by accident of `undefined` comparisons. A predicate such as `status !== 200` or `return true` would turn it red for the wrong reason.
- **F6 (Note, docs).** Heading 122.1 opens "Red before the change, green after". This is a test-only PR, so "red before" exists only under the tamper. The paragraph says so a sentence later, but the opening clause overstates it. Suggest "Red under the tamper, green at the untouched product".

### Merge-prep (doc only, required at merge; not code)
- **M1.** **The section number `122.` now collides with develop.** #1823 is merged and holds `<h2>122. A GDPR write route answers a constant 500 …`. Renumber this PR's section (and its 122.1-122.4) to 123, or to whatever develop holds at merge.
- **M2.** **The predicted merge conflicts** (rc 1) in both html docs, because both PRs append at the same spot. Merge develop into the branch, resolve by keeping both sections in order, then re-run `html_docs_check` (rc 0 expected) before merge.

### FIX-BEFORE-MERGE
(none)

Recommended follow-ups (Wednesday's call):
- F1: add the 408 and 500 cells now, or file them under KS-1788 and soften "a plain 4xx" at merge-prep.
- F2: a ruling card for Kam (should an infrastructure 401/403 at the validate call count as a rejection?).
- F3 and F4: one-line tightenings, if F1 reopens the file.
- M1 and M2 at merge-prep.

### TESTED / NOT TESTED / HOW
**TESTED**
- Head pin at both ends; develop pin at both ends.
- spark_gate.
- Diff scope, and product-byte equality (blob at three refs, plus sha256).
- A read of `couldNotAnswer`, `checkApiKey`, `validateApiKey`, `authenticateToken`, and every caller of each (`git grep` across `Blockchain/Dev/services`).
- The security service's validate route and middleware chain (`security/src/index.ts` 598-625, 775-779, 1797-1830).
- 14 tampers (the author's, the ticket's F7/F8/F18, and 10 of my own), on the PR file and on all 20 key-validation files, each sha256-restored.
- The whole api-gateway suite twice at head and twice at develop.
- html_docs_check rc 0 at head and at develop, and rc 1 on planted copies.
- Section numbers at develop, 530f0911 and head.
- merge-tree.
- Linear KS-1788 (description plus 2 comments) and KS-1240, read-only.

**NOT TESTED**
- An optional-mount 403 or 429 specifically. No product branch distinguishes them from the HANG_OPT and REJECTED_OPT cells, which pass.
- The real security service, and any ingress in front of it (F2 comes from reading code).
- tsc and eslint (the author reports 27 baselined errors and 0 new).
- The four platform suites, a running stack, Node 24, the pre-push hook legs.
- A render of the docs.
- KS-1788 items 1 and 2 (not in this PR; disclosed).

**HOW**
- **The clone:** `git clone --shared` of the checkout into the then-non-existent path `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/3595961a-a258-453d-996e-1aad78887d58/scratchpad/gate31/clone`.
  - `rev-parse --show-toplevel` was asserted equal to that path before any fetch.
  - origin was set to `git@github.com:Secuura/Distributed_Secuura.git`, and the checkout's `core.sshCommand` was copied in (read with `git config --get`).
  - I fetched `refs/pull/1827/head` and develop. The clone was checked out at head, with develop in a worktree `gate31/wt_dev`.
- **Dependencies:** each tree got its own `npm ci --ignore-scripts` (1806 packages each, rc 0), then `fix-libsodium-symlink.js`, then a `packages/shared` build with rc 0 and `dist/index.js` present. Nothing was symlinked from another tree.
- **Cleanup:** the final `git status` is clean in both trees. Every process I started (npm ci, spark_gate, tamper.py, runsuite.py) exited on its own, so nothing was killed. The evidence (`facts.json`, `tamper.py`, `tamper_run1.txt`, `tamper_wide.txt`, `runsuite.py`, `suites.txt`) is beside this file. The mutant copies and per-run json are in the scratchpad `gate31/tamper_out/`.

### Instrument errors
- **I1.** The shared-box hooks refused three calls: one containing a `cd`, and two `git -C $VAR` write verbs (checkout, merge-tree). I re-issued them with literal paths. Nothing ran under a refused call.
- **I2.** zsh's `$r:P` modifier mangled one ref loop (the same as gate 30's I3). I re-issued it as `${r}`.
- **I3.** Mutant (c) was written as `status > 0`, not `return true`. It is the F8 shape for real statuses, but it keeps `undefined` as a rejection, so it does not show the auth.test.ts kill that a literal `return true` would (see F5).
- **I4.** spark_gate's BASE 14/14 is not a red-first for a test-only PR (see point 1).
