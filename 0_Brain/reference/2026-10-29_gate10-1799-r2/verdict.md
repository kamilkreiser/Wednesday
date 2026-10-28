# QA gate 10 (TIER 1 delta, round 2 of 2): Secuura #1799 (KS-1467 services/auth half), Seat R 6th

- **Gate model:** Claude Opus 5.5 (claude-opus-5-5), G1 tier-1 delta gate, subagent of Wednesday. Spark review model: deepseek-v4-flash via the tunnel. Routing receipt as commissioned: claude-opus-5-5, G1 tier-1 delta gate, gauge ~86%.
- **Round 1:** gate 9, `0_Brain/reference/2026-10-29_gate9-tier1/verdict.md` (#1799 GO WITH NOTES, finding 1799-1). Read whole, method included.
- **Pushed / merged / commented / mailed / Linear-written / GitHub-written:** nothing. Linear was not read this gate (no key used). `gh` was not used. The PR body stood in as the head commit message, as at gate 9.
- **Clone:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate10-1799/repo`.
  - The path did not exist (`ls`: No such file). Made with `git clone --shared .../spark/cache/src`, origin set to `git@github.com:Secuura/Distributed_Secuura.git`.
  - `rev-parse --show-toplevel` asserted equal to the path before the first fetch, and again at the end.
  - Deploy key through GIT_SSH_COMMAND, the gate 9 mechanism (`!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw`, `-o ServerAliveInterval=30 -o IdentitiesOnly=yes`). `npm_config_offline=true` throughout.
- **Worktrees** (under `.../scratchpad/gate10/`): `wb` bd6697e0 (base = merge-base), `w1` e14baaa3 (round 1), `w2` 6ccfd426 (round 2). Each has two read-only node_modules symlinks: `Dev/node_modules` → the shared tree's Dev root, and `services/auth/node_modules` → the shared tree's **service-local** tree (gate 9's corrected layout). Final `git status --short`: only those two symlinks in all three. Every mutated file was restored from `git show HEAD:`, and every probe was moved back out to `quarantine/`.
- **Load:** `uptime` before every heavy run (`out/load.txt`). load1 ran 2.9 to 6.9. No waits.
- **Processes:** none stopped. All mine exited on their own; at the end `pgrep -fl "vitest|spark_review"` found nothing.

## Pins (git ls-remote)

| ref | start (02:35) | end (02:46) |
|---|---|---|
| develop | **802eb2b8ecafe5ffea2c039991db50514ec1a28d** (= brief) | same |
| refs/pull/1799/head | **6ccfd426acb3197630fcc7c5ba482f998a31b53e** (= brief) | same |
| refs/pull/1796/head | 8f022984aa7477fa16399475cbc0167dcdd06185 | same |
| refs/pull/1798/head | acdb4822304fdf2d6da3d21c38d2ad92e98ef854 | same |

- **Fast-forward:** `merge-base --is-ancestor e14baaa3 6ccfd426` is true. There is one new commit, `6ccfd426a` "Refs KS-1467: weak-password 422 details follow the published array shape, with route cells".
- **Base still bd6697e079fc:** `merge-base(6ccfd426, develop 802eb2b8)` = bd6697e079fce41db6b21e094a9eddb3d0e1d08e.

## BLUF

| PR | Round | Verdict | One line |
|---|---|---|---|
| #1799 (KS-1467 auth half) | 2 of 2 | **GO WITH NOTES** (not a NO GO, so the two-NO-GO cap is not touched) | **1799-1 is closed.** All three weak-password 422s now send `details` as `[{code:'custom', path:[field], message}]`, one entry per feedback line, with `password` for register and reset and `newPassword` for change-password. **15 of 15 real route bodies validate against the published yaml's `ValidationErrorResponse` AND the zod schema.** Round 1 failed both on 15 of 15, and base passed both (it sent no `details`). The yaml and zod agree on every one of the 63 rows. **Every author claim reproduced:** the helper, +6/-0, +4/-3, +2/-2, the 10-cell file, the red-proof (round-2 cells on the round-1 product: S x3 + N1 red, nothing else), and the suite at **1245/1245**. **My 15 mutants each go red on exactly their own route's cells. The E cells catch a route-site echo that passes the schema (M1 to M3), so gate 9's K3 gap is closed.** Every other handler branch is byte-identical to round 1 (54 of 54 probe rows). users.ts merges cleanly with #1796 and #1798 in every order. Notes: the published spec has **no 422 for change-password** (pre-existing; carried, and left as is by the "no OpenAPI change" ruling); a stray whitespace edit in auth.ts; docs still at **84**. |

---

## 1799-1 closure row

| # | Round 1 (gate 9) | Round 2 (this gate) | Status |
|---|---|---|---|
| **1799-1** (Medium, contract) | register / reset 422 sent `details: {feedback:[...]}`, an object, while the published `ValidationErrorResponse.details` is an array of `{code, path, message}` | **Each of the three sites sends `weakPasswordIssues(strength.feedback, field)`** (`errorHandler.ts:71-73`, `auth.ts:205`, `:823`, `users.ts:993`). Measured through the real routes: **15/15 weak-password 422 bodies conform to the yaml schema and the zod schema.** `details` messages equal `checkPasswordStrength(candidate).feedback` exactly, in order. Each entry has exactly the keys `{code, path, message}`, `code` is `'custom'`, and `path` is `['password']` for register and reset and `['newPassword']` for change-password. The yaml is byte-identical at base, round 1 and round 2 (blob 6cff9e58), so there was **no OpenAPI change, as ruled.** On develop 802eb2b8 the yaml blob differs, but `ValidationErrorResponse` and all three ops are deep-equal. | **CLOSED.** The residual seam is 1799-7 (change-password has no published 422; pre-existing, ruled out of scope). |
| 1799-2 (Low, test gap: no route-level cell; K3 survived) | K3 (route echo at `users.ts:993`) survived the PR's 35 cells | The new file drives all three real routes. **M1 to M3 (an echo on each issue as an extra key) are killed by E only**; S stays green because zod and the yaml both admit extra keys. That is exactly the route-site echo gate 9 could not see. | **CLOSED.** |
| 1799-3 (Info, S1/S2 depend on cwd) | open | unchanged (`process.cwd()` at the old file's line 75). My runs used cwd = services/auth: 45/45. | carried, Info |
| 1799-4 (Info, K5/K6/K7 equivalents) | open | unchanged | carried, Info |
| 1799-5 (merge-time, docs 84) | open | **still 84 / 84.1-84.3** in both html files | carried, merge-time |
| 1799-6 (Info, shared half = #1775) | open | unchanged | carried |

## CHECK 1: the delta's footprint

`git diff --stat e14baaa37c69 6ccfd426acb3` (`out/delta_stat.txt`, `out/delta_numstat.txt`):

| file | +/- | in the author's list? |
|---|---|---|
| `services/auth/src/middleware/errorHandler.ts` | +6 / -0 | yes (= claim) |
| `services/auth/src/routes/auth.ts` | +4 / -3 | yes (= claim); see 1799-8 |
| `services/auth/src/routes/users.ts` | +2 / -2 | yes (= claim) |
| `__tests__/ks1467-the-weak-password-422-through-the-real-routes.test.ts` | +134 (new) | yes |
| `__tests__/ks1467-auth-app-error-subclasses-keep-their-own-prototype.test.ts` | +6 / -4 | **not in the brief's list**, but it is the ruled "keep N1" edit: the N1 throw and expectation move to the array shape, plus comments. The commit message says "N1 is kept and moved to the array shape". |
| the two `Projects Documents/*.html` | +12/-9, +8/-7 | yes (the two docs) |

- **Nothing else.** No other product file, no yaml, no `packages/shared`, no lockfile.
- **errorHandler.ts r1 → r2** is exactly the 6-line helper inserted after `ValidationError` (`diff` of the two files: one `68a69,74` hunk). **No handler line changed.**
- **auth.ts:** 1 import line, 2 throw lines, and **one stray edit** at `:826`: `const tokenHash = createHash(` becomes `const tokenHash =createHash(` (1799-8).
- **users.ts:** 1 import line (`:16`), 1 throw line (`:993`).
- **The helper as claimed:** `export function weakPasswordIssues(feedback: readonly string[], field: 'password' | 'newPassword') { return feedback.map((message) => ({ code: 'custom' as const, path: [field], message })); }`. It has no access to the password: its inputs are the feedback lines and a literal field name.

## CHECK 2: schema-parse table, real 422 bodies, base vs round 1 vs round 2

**Method.**
- My probe (`quarantine/gate10-probe-1799.test.ts`) uses the PR's own mock harness: the real `authRoutes`, `userRoutes`, `errorHandler` and `checkPasswordStrength`, with repo, session, jwt, mail, events and db replaced. It POSTs 7 candidates to each of the 3 routes and records the raw status and text.
- I ran the same probe file on `wb`, `w1` and `w2` (`out/gate10-probe-1799_{wb,w1,w2}.json`).
- **yaml side** (`tools/validate.cjs`): `docs/openapi/secuura-api.yaml` at the head, OpenAPI **3.1.0**, compiled with **Ajv 2020** (`strict:false`, all `#/components/schemas` as `$defs`). Each body was checked three ways: (a) against the schema the yaml assigns **to that op at that status**; (b) against `ValidationErrorResponse` directly; (c) against `ErrorResponse`.
- **zod side:** `ValidationErrorResponseSchema.safeParse` inside vitest, from `@secuura/shared`.
  - That import resolves to the shared tree's `packages/shared/dist`. I read its `dist/openapi/responses.js:77-97`: it is the same schema as `src/openapi/responses.ts`, whose blob is 5142f8a4 at base, r2 and develop.
- Table rows: `out/schema_table.txt`; JSON: `out/schema_rows.json`.

Weak-password rows (5 candidates per route: `zqkvnxyplmwtrdfgh`, `Zk9Qmwtr`, `qwertyzqkvnx`, `aaaaaaaaaaaaaaaaaaaa`, `qwertyzqkvnx<script>`):

| route | status (all sides) | yaml assigns at that status | base (bd6697e0): `details` | base yaml / zod | round 1 (e14baaa3): `details` | r1 yaml / zod | round 2 (6ccfd426): `details` | **r2 yaml / zod** |
|---|---|---|---|---|---|---|---|---|
| POST /api/auth/register | 422 | `ValidationErrorResponse` | absent | 5/5 pass, 5/5 pass | `{feedback:[...]}` | **0/5, 0/5** ("data/error/details must be array") | `[{code:'custom',path:['password'],message}...]` | **5/5, 5/5** |
| POST /api/auth/reset-password | 422 | `ValidationErrorResponse` | absent | 5/5, 5/5 | `{feedback:[...]}` | **0/5, 0/5** | same, `['password']` | **5/5, 5/5** |
| POST /api/users/me/change-password | 422 | **none: the yaml publishes no 422 for this op** (400 → `ErrorResponse`, "Wrong current password or new password too weak") | absent | VE 5/5, zod 5/5; op: no-such-status | `{feedback:[...]}` | **VE 0/5, zod 0/5**; op: no-such-status | same, `['newPassword']` | **VE 5/5, zod 5/5**; op: no-such-status (1799-7) |

- **Exactness at r2, all 15 rows:** `details.map(d => d.message)` equals the feedback array, in order. Entry keys are exactly `{code, path, message}`; top-level keys are `{success, error}`; error keys are `{code, details, message}`. **No candidate appears in any body on any side.**
- **Controls:**
  - `Zk9Q` (shorter than zod's min 8) → 400 `ErrorResponse` with the ZodIssue `details`, on all three sides and all three routes. It conforms to the op's 400.
  - The strong password → register 201 `LoginResponse`, reset 404 `ErrorResponse` (the token mock returns null), change-password 200 `AuthSuccess`. Each conforms to its op, on all three sides.
- **yaml vs zod:** they **agree on all 63 rows**. No divergence, so no authority call was needed. Structurally the zod object and the yaml are the same: neither is strict, so both admit extra keys (which is why M1 to M3 pass S and fail E). One difference is outside the zod schema: the yaml **does not attach** `ValidationErrorResponse` to change-password at all (1799-7). The PR's S `change-password` cell validates against the zod schema, not against what the yaml publishes for that op.

## CHECK 3: mutants (`tools/mut.py`; the PR's two ks1467 files = 45 cells, run with cwd = services/auth; `out/mut/`, `out/mut_summary.json`)

| mutant | cells red (of 45) | expected | read |
|---|---|---|---|
| M0 head | **0** (45/45) | none | baseline |
| **M1 register echo**: each issue gets `received: data.password` (schema-conforming) | **E register only** | E only | **killed at the route** (gate 9 K3 analogue) |
| **M2 reset echo**, same | **E reset-password only** | E only | killed at the route |
| **M3 change-password echo**: `received: data.newPassword` | **E change-password only** | E only | **killed at the route: exactly gate 9's K3 site** |
| M4 register: the round-1 object `{feedback}` | **S register only** | S only | killed |
| M5 reset: the round-1 object | **S reset-password only** | S only | killed |
| M6 change-password: the round-1 object | **S change-password only** | S only | killed |
| M7 register: wrong path `newPassword` | **S register only** | S only | killed |
| M8 reset: wrong path `newPassword` | **S reset-password only** | S only | killed |
| M9 change-password: wrong path `password` | **S change-password only** | S only | killed |
| M10 register: echo as an extra conforming issue `{code:'custom', path:['password'], message: data.password}` | S + E register | S + E | killed twice |
| M11 change-password: echo in the top-level message | S + E change-password | S + E | killed twice |
| M12 helper returns `{feedback}` | S x3 + N1 | all S, N1 | killed |
| M13 helper `path` as a string, not an array | S x3 + N1 | all S, N1 | killed |
| M14 handler stops sending `details` | S x3 + H1 + N1 | all S, H1, N1 | killed |
| M15 `checkPasswordStrength` pushes the password (gate 9 K1) | E x3 + N1 | all E, N1 | killed (E fails on its own precondition, `feedback.join(' ').includes(candidate)` = false) |

- **The author's nine** ("the password echoed into details or the message, and the round 1 shape, at each site; each turns red only its own route's cells") **reproduce in kind**: M1 to M6, M10 and M11 cover those classes at every site, and each stays inside its own route. No mutant leaks red into another route's cells.
- **E catches the echo at the ROUTE.** M1 to M3 are invisible to S (the extra key passes both schemas) and to N1 (which composes the helper, not the route); only E kills them. That is the gap gate 9 recorded as 1799-2.
- **The author's red-proof** (round 2's cells on the round-1 product, `w1` with r2's two test files copied in): **41/45, red = N1 + S register + S reset-password + S change-password**, exactly as claimed (`out/r2tests_on_r1.json`). On the merge-base product (spark_gate): new file 7/3 (the S x3 red), old file 13/22.
- **E and B are green at base and at round 1** (base sends no details, so there is nothing to echo). The E cells are labelled `RED KS-1467 E ...` but are guards, not red-first cells (1799-9, Info).

## CHECK 4: every other handler branch is byte-identical to round 1

- **Source:** `errorHandler.ts` round 1 vs round 2 differs only by the inserted helper (lines 69-74). The `instanceof ValidationError && err.details` branch (`:302-303`), the ZodError branch (`:290`), and every other line are unchanged.
- **Probe:** gate 9's subclass response probe (`gate9-probe-1799.test.ts`; the env var renamed, nothing else changed) was re-run at `w1` and `w2`:
  - **classes: 24 of 24 rows identical; wire: 30 of 30 rows identical, r1 vs r2.** The wire rows are all 19 subclasses + AppError, ValidationError with `{feedback}` / none / null / 0 / {}, plain Error, TypeError, ZodError, the statusCode-503 look-alike, a thrown string, and malformed JSON.
  - **Both are also identical, 54 of 54, to gate 9's recorded head output** (`gate9-tier1/out/gate9-probe-1799_w1799.json`).
- (The probe's ValidationError row throws `{feedback}` straight at the handler. It is unchanged because the handler forwards any truthy `details`; the shape now lives at the call sites.)

## CHECK 5: users.ts merge-tree with Seat K 13th's #1796 and #1798 (`tools/mt.sh`, `out/mergetree.txt`)

**Pairwise** (`git merge-tree --write-tree`):

| pair | rc | conflicted files |
|---|---|---|
| #1799 r2 × #1796 | 1 | **only** the two Projects Documents html files |
| #1799 r2 × #1798 | 1 | **only** the two Projects Documents html files |

**Sequential onto develop 802eb2b8.** Scratch commits live only in my clone. For each step the docs conflict was resolved by keeping the previous step's html, so the code merge could carry forward.

| order | users.ts conflict at any step | final users.ts blob |
|---|---|---|
| develop +#1796 +#1799 | none | 98067a8c |
| develop +#1799 +#1796 | none | **98067a8c** (same) |
| develop +#1798 +#1799 | none | 8d307895 |
| develop +#1799 +#1798 | none | **8d307895** (same) |
| all six orders of {#1796, #1798, #1799} | none | **7563694e in all six** |

- **users.ts never conflicts, in any order, and the result is order-independent.**
- The triple-merged users.ts diff against develop holds all four hunks:
  - #1798's `:13` import (`VERIFICATION_LEVEL_ORDER`);
  - #1799's `:16` import (`weakPasswordIssues`);
  - #1799's `:993` throw;
  - #1796's `:1174-1179` comment;
  - #1798's `LEVEL_ORDER` block and review comment.
- The `:13` and `:16` hunks are three lines apart and auto-merge.
- The only conflicts are the docs html (the numbering chain that Wednesday holds). #1798 vs develop is rc 0, as at gate 9.

## CHECK 6: Spark half (run FIRST; `out/p1799/`)

**Method.**
- `spark_gate.sh <clone> 1799 6ccfd426... develop <new file> <old ks1467 file> --node-modules <shared services/auth/node_modules> --work .../scratchpad/gate10/sg1799`. The base is **develop**, resolved by the script to tip 802eb2b8, merge-base bd6697e0. It was never given a round sha.
- **node_modules, per gate 9's harness finding:**
  - spark_gate links its one `--node-modules` dir into the package dir only, and the service-local tree has no vitest.
  - So I also linked `.../scratchpad/gate10/node_modules` → the Dev root. That is an **ancestor** of the work dir, so Node and npx walk up to it.
  - I verified this first in a dummy layout: `npx --no-install vitest --version` → 4.1.10 with no install. `require.resolve('@types/node')` → the service-local **20.19.43**, and vitest → the Dev root.
  - That is the faithful layout, and nothing was downloaded (`npm_config_offline=true`).
- `tunnel.sh check` (at `spark/tunnel.sh`) → UP, `127.0.0.1:47788/v1/models` 200, ssh pid 52462. `pgrep -f spark_review.py` showed none running.
- `spark_review.py` ran on `facts_spark.json`: the facts minus the two docs html, plus HARNESS lines (gh unauthenticated, so the commit message stood in for the body; the round-2 context and Wednesday's ruling as briefed; the diff is the whole PR from the merge-base).

| spark_gate | head | base product code | merge_base recorded |
|---|---|---|---|
| new route file | **10 / 0** | 7 pass / **3 fail** (S x3) | bd6697e0 |
| old ks1467 file | **35 / 0** | 13 pass / **22 fail** | |
| total | **45 / 0** | 20 / 25 | rc 0, 39 s |

Non-vacuous: product_files is populated, and 25 cells are red at base.

| Spark review | tokens / time |
|---|---|
| **NO GO**: 3 Major, 3 Minor, 1 Note | 72,223 prompt + 1,345 completion, 109.9 s, 1 attempt, valid |

### Spark Majors checked at source

- **Major 1** ("the packages/shared half is untouched"): **FALSE as a defect.** It is sanctioned narrowing (#1775), and the prompt said so in a HARNESS NOTE. Spark repeated its gate 9 Major 2 anyway.
- **Major 2** ("the tests validate against the `@secuura/shared` zod schema, not the published OpenAPI document"):
  - **TRUE as an instrument observation; FALSE as a defect.** I validated the same real bodies against the yaml with Ajv 2020: yaml and zod **agree on all 63 rows**.
  - The concern has a real edge Spark did not find: for **change-password the yaml publishes no 422 at all** (1799-7), so that S cell checks a schema the spec never assigns to that op.
- **Major 3** ("visible wire change with no client-compatibility evidence; the PR says the schema is not widened but does not verify it"): **FALSE as a defect.**
  - The change is ruled.
  - "Not widened" is verified: the yaml blob is identical at base, r1 and r2.
  - For register and reset the new shape is **exactly** what the published contract already promised.
- **Minors:**
  - session mock "more permissive than the real service": **immaterial**; the 422 is thrown before any session call.
  - S1/S2 depend on cwd: **TRUE**, carried 1799-3.
  - **`const tokenHash =createHash(` whitespace regression: TRUE.** Spark found it independently; it is 1799-8.
- **Note** ("the nine mutants are not in facts.json"): true of the facts. Reproduced here (CHECK 3).

## Spark calibration row

| PR | Spark verdict | This gate | Spark defects that stand | Real findings Spark missed | Verdict of the verdict |
|---|---|---|---|---|---|
| #1799 r2 | NO GO (3 Major) | GO WITH NOTES | 0 defects. Major 2 is a true instrument point (zod rather than yaml), measured harmless (63/63 agree). Minor 3 (the whitespace edit) is true and was found independently. | change-password has **no published 422** (the sharper form of its own Major 2); E/B are guards, not red-first; docs 84 still colliding | **False NO GO, with one useful Minor.** Major 1 repeated a sanctioned-narrowing Major even though the prompt carried the ruling, which suggests the HARNESS NOTE channel does not reliably override the ticket text. 72.2k prompt tokens (3.3x gate 9's 21.8k: the second test file and the larger diff). Non-vacuous: 25 red at base. |

## Tests

- **Suite** (`--testTimeout=30000 --hookTimeout=60000`, cwd = services/auth, the faithful node_modules layout; `out/suite/`, `out/suite_compare.txt`):
  - w1 (round 1): **106 files / 1235 / 0 failed**;
  - w2 (round 2): **107 files / 1245 / 0 failed**;
  - 0 vanished, **10 new cells, all in the new file**, 0 cells changed status.
  - **This matches the author's 1245/1245** and gate 9's round-1 1235.
- **tsc** `-p tsconfig.json --noEmit`: rc 0 on w1 and w2.
- **Ratchet** `check.cjs services/auth`: rc 0 on both. w1 has 106 test files and 42/42/0/0; w2 has **107 test files and 42/42/0 new/0 stale**, so the new file adds no type errors.
- **eslint** on the 3 product files + the ks1467 tests (cwd = Dev): rc 0, clean, on w1 and w2. **prettier --check** on auth.ts fails on **both** r1 and r2, so the file was never prettier-clean and prettier does not gate it.

## Findings

| # | Sev | Finding | FOUND / TESTED / HOW |
|---|---|---|---|
| 1799-1 | was Medium | **CLOSED.** See the closure row. | TESTED, 63 real bodies × yaml (Ajv 2020) × zod, base / r1 / r2. |
| 1799-2 | was Low | **CLOSED.** E kills a route-site echo (M1 to M3). | TESTED, mutants. |
| **1799-7** | **Low (contract, pre-existing; carried from gate 9's 1799-1 text)** | The published yaml has **no 422** for `POST /api/users/me/change-password`: weak password is documented under **400 `ErrorResponse`**, yet the route answers **422** on base, r1 and r2. Schemathesis's status-code conformance check would flag the status. The body itself now conforms to both `ValidationErrorResponse` and `ErrorResponse`. Wednesday's ruling ("no change to the OpenAPI schema") leaves this as is; the PR's S `change-password` cell validates against the zod schema, not against what the spec says for that op. **Suggest a ticket:** add a 422 `ValidationErrorResponse` to change-password in `auth.openapi.ts` (or move the route to 400). | TESTED (Ajv: "NO-SUCH-STATUS" on 15/15 change-password weak rows, every side). |
| **1799-8** | **Info (cosmetic)** | `auth.ts:826`: `const tokenHash = createHash(` → `const tokenHash =createHash(`. A stray, behaviour-neutral whitespace edit in the reset route, outside the ruled change. eslint is clean and prettier does not gate this file, so nothing catches it. Revert it in this PR if Seat R touches the PR again. | FOUND by diff read (Spark Minor agrees); lint TESTED. |
| 1799-9 | Info | The E cells (and B) are titled `RED KS-1467 E ...` but are **green at base and at r1** (base sends no details; r1 echoes nothing). They are guards that go red only on an echo, not red-first cells. The S cells and N1 are the genuinely red ones (CHECK 3 red-proof). The title is slightly misleading; the docs entry describes them correctly. | TESTED (spark_gate base 7/3; r2-on-r1 41/4). |
| 1799-3 | Info, carried | S1/S2 use `process.cwd()`. | read |
| 1799-4 | Info, carried | `setPrototypeOf` is redundant (ES2022); K6/K7 are equivalent. | gate 9 |
| 1799-5 | merge-time, carried | Docs still **84** / 84.1-84.3, colliding with develop and #1797. Renumber at merge. | grep |
| 1799-6 | Info, carried | The `packages/shared` half is #1775. | gate 9 |

**Verdict for #1799 round 2: GO WITH NOTES.** It is not a NO GO, so the two-NO-GO cap is not engaged. Nothing blocks the merge. Merge-time items: renumber the docs from 84, and resolve the docs html against #1796 / #1798 / #1797. Ticket candidate: 1799-7.

## Method

- **Copied from gate 9:**
  - a fresh-path clone with the toplevel assertion, and the deploy key via GIT_SSH_COMMAND;
  - read-only node_modules symlinks in gate 9's corrected layout (service-local tree + the Dev root);
  - the Spark half first, base = develop, facts minus the docs html, HARNESS lines;
  - mutants written from `git show HEAD:` and restored, with `git status` read back;
  - full suites compared by (file, fullName);
  - merge-tree; pins at start and end.
- **New this gate:**
  - the yaml-side validator (`tools/validate.cjs`, js-yaml + Ajv 2020 from the shared tree's Dev root, read-only);
  - the three-route body probe built from the PR's own harness (`quarantine/gate10-probe-1799.test.ts`);
  - 15 mutants (`tools/mut.py`);
  - the red-proof replay (r2's tests on r1's product);
  - gate 9's subclass probe re-run at r1 and r2;
  - sequential merge-tree in all orders with the docs conflict carried (`tools/mt.sh`, `tools/fixtree.py`; scratch commits in my clone only);
  - eslint / prettier on the touched files.
- Every vitest run had cwd = `services/auth`, so S1/S2 are green, unlike gate 9's mutation runner.

## NOT TESTED

- PR body (`gh` unauthenticated; the commit message stood in).
- Linear (not read this gate; the brief's ruling was taken as given).
- Node 24 LTS (ran on v26.8.1).
- A real database, Redis, the gateway, Docker, CI, the pre-push hook, `audit:gate`, `audit:locks`.
- **An actual Schemathesis run.** Conformance was measured with Ajv against the yaml, not with Schemathesis against a live server.
- Whether the front end reads `details` (old object or new array).
- The `packages/shared` half (#1775) and the 12 services that mount it.
- The merged trees (develop + #1799 + #1796 / #1798) were merge-tree'd only, **not built or suite-run** (gate 9 ran the K pair's merged suite; this gate did not re-run it with #1799 r2 added).
- The register 422 for a client-supplied `role` (auth.ts:173): read only (no details, so unchanged; it conforms).

## Evidence locations

- **Run outputs:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate10-1799/out/`
  - `pins_start.txt`, `pins_end.txt`, `load.txt`, `delta_stat.txt`, `delta_numstat.txt`, `delta_code.patch`
  - `p1799/` (facts, facts_spark, diff, `spark/review.json`, raw attempt, `pr_body_from_commit.txt`), `sg1799.log`, `sg_rc.txt`, `rev_rc.txt`
  - `gate10-probe-1799_{wb,w1,w2}.json`, `schema_table.txt`, `schema_rows.json`
  - `mut.log`, `mut/`, `mut_summary.json`, `r2tests_on_r1.json`
  - `gate10-subclass-1799_{w1,w2}.json`
  - `mergetree.txt`
  - `suite/{w1,w2}.json|log`, `suite_compare.txt`, `heavy.log`, `tsc_build_{w1,w2}.txt`, `ratchet_{w1,w2}.txt`, `eslint_{w1,w2}.txt`
- **Scratch:** `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/fccaae68-37b3-43d1-9466-4e52087c3d4f/scratchpad/gate10/` (`env.sh`, `run_sg.sh`, `run_rev.sh`, `tools/`, `quarantine/`, worktrees `wb` `w1` `w2`, spark work dir `sg1799`, `api_head.yaml`, `api_develop.yaml`, the `nptest/` layout check, and the ancestor `node_modules` link).
