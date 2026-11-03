GO WITH NOTES — MERGE (no HOLD-FOR-KAM)

# QA GATE 164: Secuura Platform K PR 1981 (KS-1868, security revoke-on-rotate catches), TIER 1, round 1

**Verdict: GO WITH NOTES. Nothing has to be fixed before merge. MERGE: no HOLD-FOR-KAM, because no head cell is more permissive than base with an ordinary Error.**

The class bar holds at both changed catches. I ran 19 value kinds through both sites, under both `NODE_ENV=development` and `production`, with the service's real logger. For these catches that logger is index.ts's own `log()`, which is `console.log(JSON.stringify(...))`, not winston. Head ends in exactly the state that base with an ordinary Error reaches in **76 of 76** head cells. In every one of those cells the catch logged one line, with text.

The rotate route was driven over HTTP. I used the real base and head security service, a real migrated Postgres (app role `secuura_app`, FORCE RLS), and the real `/api/keys/validate` route to count which keys still work. Result:
- When the retire fails, head answers **201 with the new key and `priorKeysRevoked: null`, and the prior key stays valid**. Base gives exactly that for an ordinary Error.
- At base, 4 hostile kinds turned that into **500, no key**. The whole transaction rolled back, so the prior key stayed valid there too.
- A **real** Postgres failure of the retire alone (a lock timeout on the prior row; no injected value) gives the same 201 / null / prior-valid at base and at head.

So "the prior credential stays valid after a failed retire" is **pre-existing** behaviour, the same at base and head. On top of it, the one production caller (the gateway's register-connector) answers its own caller `rotated: true` and drops `priorKeysRevoked` (G164-F3, MEDIUM, a Kam card, not a merge block).

Subject:
- Head `2e0f5ec046d640c1f83dcf248f15e4d570340959`. It equals `git ls-remote origin refs/pull/1981/head`, read from the read-only checkout at the start (`logs/head_start.log`) and again at 02:00:29Z, the end of this gate.
- Fetched from GitHub `refs/pull/1981/head` into this gate's own `git clone --shared` (`repo/`).
- PR parent and build base `0a6575f7fd92d60849d1186efa0632961db21be5`. Develop `32921f7921c2cdeb87e4361a2976a9e8cfd6beac` (ls-remote at the start and at the end, unchanged).
- Host Node v26.8.1, typescript 5.9.3 (clone).
- The product and test bytes equal the held Spark pass O83-P1:
  - Canonical patch sha256 `c43ea633d571dd6e…`, the same as the author's.
  - The changed lines are EQUAL in both files (index.ts 4 lines, test 168 lines; `logs/spark_bytes.log`).

## The change

At two catches, `reason = err instanceof Error ? err.message : String(err);` becomes `reason = String(err instanceof Error ? err.message : err);`, still inside the existing try / `'unreadable thrown value'` fallback:
- **Site A:** `revokePriorConnectorKeys`, index.ts:314.
- **Site B:** the KS-1549 savepoint catch of `saveKeyAndRetirePriors`, index.ts:427.

At base, a message that is a non-string came back from the read intact, and `log()`'s `JSON.stringify` threw on it **outside** the guard. This happened for a BigInt, an object whose toJSON throws, a revoked Proxy, or a cyclic object.

## Answer to the TIER 1 question (the rotate route)

**(1) Measured, real route, real Postgres** (`logs/matrix_all.json`, `logs/summary.txt`, site `route`). Every cell does the same steps:
1. Seed a connector with one key and validate it (control: `true` in 160 of 160 cells).
2. Rotate with the retire UPDATE rejecting with the kind.
3. Validate the new key and the prior key through `/api/keys/validate`.
4. Read the rows back as superuser.

The development and production results are identical.

| | status | new key issued / valid | prior key valid (validate / DB row) | active rows | `priorKeysRevoked` |
|---|---|---|---|---|---|
| **base, ordinary Error** (the reference) | 201 | yes / **yes** | **yes** / active | 2 | `null` |
| base, 15 other kinds | 201 | yes / yes | yes / active | 2 | `null` |
| base, **bigintMessage, messageToJSONThrows, messageIsRevokedProxy, cyclicMessage** | **500** (KS-888 "no key was issued") | **no** / n.a. (the INSERT rolled back with the transaction, so no row) | **yes** / active | 1 | absent |
| **head, all 19 kinds** | 201 | yes / **yes** | **yes** / active | 2 | `null` |
| control: retire succeeds (`routeUp`, base and head) | 201 | yes / yes | **no** / inactive | 1 | `1` |
| **real pg failure**: superuser holds `FOR UPDATE` on the prior row, app role `lock_timeout=500ms`, nothing injected (base and head) | 201 | yes / yes | **yes** / active | 2 | `null`; logged `"canceling statement due to lock timeout"` |

Counts:
- Valid keys at the end, base ordinary: new **1**, prior **1**.
- Valid keys at the end, head hostile (all 19 kinds): new **1**, prior **1**.
- Valid keys at the end, base hostile (the 4 kinds): new **0**, prior **1**.
- Head equals base-with-ordinary-Error in 38/38 route cells.
- Head cells more permissive than the reference: **0**. `harness/summarise.js` flags any cell whose count of valid credentials or active rows exceeds the reference's.
- The `routeUp` control shows the instrument can see a prior key go invalid.

So head issues the new key for hostile values **exactly as base already does for an ordinary Error**. The condition for HOLD-FOR-KAM (base-ordinary issues no key while head does) does not hold.

**(2) "The prior key stays valid after a failed revoke" is a PRE-EXISTING fail-open.** Base = head for an ordinary Error, and for a real Postgres error. Rating: **MEDIUM** (G164-F3):
- Impact is high. The rotate exists to cut off a lost or leaked credential, and when the retire fails that credential keeps working.
- Likelihood is low. Only a statement-level failure of the retire UPDATE alone fails open, with the INSERT and connection intact: a lock or statement timeout, a cancel, or a deadlock. A lost connection fails the whole transaction instead (5xx, no key). The security service sets no `statement_timeout` or `lock_timeout` in code (git grep), so with server defaults the UPDATE waits on a lock rather than failing. I needed a non-default `lock_timeout` to make it fail.
- This is the deliberate KS-577 ruling ("mint first, then revoke… the worse failure is the outage"). The service does report it: `priorKeysRevoked: null` and a loud log line.
- The gap is downstream, in the gateway (F3). It is a finding for a Kam card, not a merge block.

**(3) Callers, whole repo, with positive controls** (`logs/q3_callers.log`, `logs/q3_route_callers2.log`; `git grep -i` on the object database at head and at develop).
- **`revokePriorConnectorKeys`:** one production call, `index.ts:406`, inside `saveKeyAndRetirePriors`'s `if (!isDbAvailable())` branch.
  - Inside the function, `if (!isDbAvailable()) return retired;` (:300) is reached synchronously, with no await between the two checks, so it always returns before the try.
  - **The site A catch is therefore unreachable in production.** Only the test seam reaches it (G164-F4).
  - Every other hit is a comment or a test. The definition and the :406 call show the search matches.
- **`saveKeyAndRetirePriors`:** one caller, the `POST /api/keys` route at `index.ts:1441`, when `rotate && connectorId`.
- **Callers of `POST /api/keys`** outside the security service, non-test:
  - **`api-gateway/src/routes/platform.ts:847`** (register-connector). This is the only caller that sends `rotate`, and rotation is platform-only.
  - `tenant-provisioning/src/meteringKey.ts:52`. It never sends `rotate` or reaches the retire.
  - Positive control: the same search for `rotate` inside security index.ts gives 24.
- **Named re-run:** my first `rotate` regex (`logs/q3_route_callers.log`) returned a **false zero**, because it missed the shorthand property `rotate,`. I re-ran it as a whole-word `-i -w` search with a control, and the corrected log is what I quote.

**(4)** Figures, mutants, tsc and merge-tree are below.

## Findings

**G164-F1 (INFO, positive): class bar holds at both sites, 19 kinds x 2 sites x 2 env.**
- FOUND: head = base-with-ordinary-Error in 76/76 head cells, with one line logged with text in every one. The logged text per kind at head:

  | Kind | Logged text |
  |---|---|
  | ordinary Error, plain string | `"g164 boom"` |
  | number | `"42"` |
  | null / undefined | `"null"` / `"undefined"` |
  | revoked Proxy, message getter throws, object toString throws, message toString throws, message is a revoked Proxy, null-prototype message | `"unreadable thrown value"` |
  | Symbol message | `"Symbol(g164)"` |
  | BigInt message or value | `"10"` |
  | toJSON-throws message, cyclic message | `"[object Object]"` |
  | null message | `"null"` |

- FOUND, base exposure:
  - The same 4 kinds in development and in production. `log()` does not depend on the format, unlike winston in gates 160/161.
  - Site B gives 500 with no key. Site A rejects (it returned `REJECTED` instead of `null`).
  - At base, 4 more kinds logged non-text or omitted the field without changing state: the Symbol message is omitted, a null message gives `null`, and `{}` for the toString-throws and null-prototype messages.
  - No process died in any cell.
- TESTED: `harness/cell.js` + `harness/run_matrix.js`, 160 cells, run serially.
- HOW:
  - The real base and head `services/security/src` were extracted by blob (index.ts `505aaec4` / `d7a5674b`, verified by hash-object; `logs/src_extract.log`) and transpiled verbatim (`harness/transpile.js`).
  - Real express, real `@secuura/shared`, real db.ts and pg, against my own `postgres:15-alpine` container `gate164-pg` on 127.0.0.1:55164. Its schema came from the repo's `docker/init/0*.sql` + `migrations/*.sql`. The 13 setup errors were all `_secuura_migrations` bookkeeping, as in the PR 1549 gate. `svc_api_keys` has RLS and FORCE RLS, and `secuura_app` is neither superuser nor BYPASSRLS (`logs/pg_setup.log`).
  - The **only** substitution: index.js's `require('./db')` gets the real module with `query` and `transaction` wrapped. While armed, the retire statement (`UPDATE svc_api_keys … RETURNING id`) rejects with the kind instead of being sent. `faultFired` = 1 in every fault cell.
  - Production cells use a throwaway per-process `PII_ENCRYPTION_KEY`.
- **Named re-run:** my first matrix run died in all 80 production cells, because index.ts:2193-2196 exits without `PII_ENCRYPTION_KEY`. It is kept as `logs/matrix_run1_discarded_prod_pii.json`, discarded as an instrument error. The figures are from the re-run.

**G164-F2 (INFO, TIER 1): the 201 / `priorKeysRevoked: null` outcome for hostile values is the base ordinary-Error outcome. MERGE.**
- FOUND: as in the table above, including the real lock-timeout cell (`logs/real_lock_timeout.log`).
- The author's "500 with no key before, 201 after" was read from source, not run. I measured it, and it is accurate for the 4 kinds.
- One correction to the wording: at base the 500 also leaves the prior key valid. The INSERT and the retire roll back together, so for those values base was "no new key, old key still live", not a safer state.

**G164-F3 (MEDIUM, PRE-EXISTING, base = head, not caused by this PR): a failed retire leaves the rotated-away credential valid, and the gateway tells its caller the rotate succeeded.**
- FOUND (measured): with a real Postgres lock timeout on the retire, base and head both answer 201, the new key valid, **the prior key valid**, and 2 active rows.
- FOUND (read, not driven): `api-gateway/src/routes/platform.ts:884-889` only `console.error`s when `priorKeysRevoked === null`. The response at :909-921 carries **`rotated: true`** and no `priorKeysRevoked` field. The audit row at :895-907 records `connector.key-rotate` without the failure. A Platform S admin re-keying a leaked credential is told it rotated, while the old key keeps working.
- There is no retry or sweep that retires it later (read). Validate re-reads the stored row (KS-1370), so every replica honours it.
- For a Kam card: surface `priorKeysRevoked` through the gateway, and decide retry or alerting. Not merge-blocking for this PR.

**G164-F4 (INFO, reachability): the site A catch has no production path.**
- FOUND: as in Q3, `revokePriorConnectorKeys` is only called when the database is unavailable, and it then returns before its try. Site A is defence for the exported test seam.
- FOUND, pre-existing at the seam only: if it were reached, memory retires the prior key before the database UPDATE fails. In-process validate then refuses the prior key ("revoked if either says revoked"), while the row stays active for every other replica. Measured: `priorInMemoryActive=false`, `priorValidAfterInProcess=false`, `priorRowActive=true` at base and head alike.
- Reachability of hostile values: real pg rejects with Error objects that carry string messages. I did not show a hostile value reaching either catch in production. The guards are still correct.

**G164-F5 (LOW, test gap): 8 of 12 mutants killed by the PR's tests; 4 survive.**
- The mutants are one exact replace each, anchored to its site: within 700 chars of `KS-577: revoke-on-rotate FAILED` for A, and of `ROLLBACK TO SAVEPOINT ks1549_retire` for B (`harness/mutants.py`, `logs/mutants.json`, `logs/mutants_compare.txt`). Each mutant ran:
  - the PR test file (vitest, cwd = security), after which the file was restored by `git checkout` with blob `d7a5674b` asserted;
  - 28 recorder cells for its site against a transpile of the mutated head.

| Mutant (A and B) | Tests | Recorder |
|---|---|---|
| X1 revert to base | KILLED (3 of 10 each) | **state differs in 8/28**, the 4 kinds above in both envs. Positive control for the recorder |
| X2 `String(err)` | KILLED (2) | text only |
| X3 template literal | KILLED (1) | text only (Symbol becomes the constant) |
| X4 `JSON.stringify` | KILLED (4) | text only |
| **X5** inner `String(err)` in the non-Error arm | **survives** | 0 differences: **equivalent** |
| **X6** `String(err?.message ?? err)` (no instanceof) | **survives** | text only: a null message logs `"Error: null"` instead of `"null"` |

- No survivor changes state or the class bar.
- Nice-to-have: add a null-message cell, and a BigInt, toJSON-throws or cyclic message cell. Today R1/R4 (revoked-Proxy message) are the only state reds; R2/R3/R5/R6 are text-only reds at base.

**G164-F6 (INFO, merge-tree): clean, and touches exactly the PR's paths.**
- FOUND: `git merge-tree --write-tree 32921f7921c2 2e0f5ec04` gives rc 0 and tree `37b189c090bb…`, equal to the author's. The merge-base is `0a6575f7`.
- The merged tree differs from develop in exactly the PR's 4 paths. **Shared paths (PR ∩ base..develop): none.**
- Control: base..develop touches 20 files, 14 of them under `services/` and 6 docs fragments, but 0 under services/security. Head and the merged tree have 0 differences under services/security.
- TESTED: `scripts/mergetree.sh` → `logs/merge-tree.log`, run in this gate's clone only.

## Figures (re-measured; author's figure in brackets)

| Item | Result | Author |
|---|---|---|
| Red-first (base index.ts + new test) | 6/10 failed, all AssertionError; C1-C4 green | [6/10 by assertion] match |
| New tests at head | 10/10 | [10] match |
| Security vitest, base 0a6575f | 49 files / 470 tests, 470 pass, rc 0 | [49/470] match |
| Security vitest, head | 50 files / 480 tests, 480 pass, rc 0 | [50/480] match |
| Test-types ratchet (check.cjs services/security) | base 68 files (56 tests) 0 errors, 0 new; head 69 (57) 0/0, rc 0; planted TS2322 in the test file gave rc 1, "1 new" | [0 errors, 0 new] match |
| tsc, service tsconfig, head | 0 errors, rc 0; planted TS error gave rc 2, 1 error | n/a |
| eslint, PR test file | 0 errors, 0 warnings; planted `debugger` + unused var gave 1 error + 1 warning | [0/0] match |
| eslint, index.ts | 0 errors, 2 warnings at head **and** base (pre-existing, unchanged) | n/a |
| docs-fragments check, head | rc 0 "lint clean, render passes html_docs_check" (cheat ADVISORY at line 6235 is pre-existing); planted unclosed `<div>` in the flow fragment gave rc 1; rc 0 after restore | n/a |
| Recorder | 160 cells + 2 real-lock cells; head = reference in 76/76 | [12 values x 2 functions] holds, wider |
| Mutants | 12: 8 killed, 4 survive (2 equivalent, 2 text-only) | n/a |
| Merge-tree | rc 0, tree 37b189c090bb, 4 paths, 0 shared | [37b189c090bb, 4 paths] match |
| Spark bytes | O83-P1 changed lines EQUAL in both files; patch sha256 c43ea633d571dd6e | match |
| Install | `npm ci --ignore-scripts` rc 0, 1798 packages; packages/shared built rc 0 | n/a |

## NOT TESTED

- Node 24 or any LTS Node (host v26.8.1 throughout).
- The api-gateway register-connector route (F3 is read, not driven), the four platform suites, and any deploy.
- A real pg client emitting a hostile value. Reachability is read only.
- A server-side `statement_timeout`, a cancel, or a deadlock as the real trigger. Only `lock_timeout` was driven.
- A non-zero `API_KEY_ROTATION_GRACE_SECONDS` (the expiry form of the retire statement).
- Concurrent rotates (KS-1549's integration file was not run).
- docs-fragments `check` on the merged tree; `check --committed`.
- The other KS-1868 sites.

## Plain answer for Kam

This PR does not open anything. When a key rotate's clean-up step fails with a strange error value, the service now does exactly what it already did for a normal database error: it hands out the new key, keeps the old key working, and says so (`priorKeysRevoked: null`). Before, those strange values made it refuse the rotate entirely (500, no new key), and the old key stayed working there too.

The real issue sits next to the PR. "The old key stays working when the clean-up fails" is how the service was designed (KS-577). But the gateway, which is the only caller that rotates, then tells Platform S `rotated: true` and drops the warning. Someone rotating a leaked key would think it was dead when it is not. That is worth a card (G164-F3, MEDIUM, pre-existing). It is not a reason to hold this merge.

## Housekeeping

- Every write stayed in this workdir: `repo/`, `harness/`, `scripts/`, `logs/`, `evidence/` (the author's file, untouched).
- The clone is at the PR head `2e0f5ec04`. `git status` is clean, and the index.ts blob is `d7a5674b`.
- The Blockchain checkout was touched only by read verbs (`ls-remote`, `remote -v`). The GitHub fetch ran inside the clone only, with the project deploy key through a per-command `GIT_SSH_COMMAND`. The clone's origin URL was set to GitHub inside the clone.
- The container `gate164-pg` was stopped and removed. `docker ps -a` shows no gate164 container, and `ps` shows no process with gate164 in its command line.
- The role setting `lock_timeout` was reset before the container was removed.
- No secrets in any file: the Postgres passwords are throwaway values for that removed local container, and the JWT and PII keys were generated per process and never written.
