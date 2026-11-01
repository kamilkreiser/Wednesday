# QA GATE 73 verdict: Secuura/Distributed_Secuura PR 1888 (KS-1868 O39-P1, AuditLogger.flush), TIER 1 (audit trail)

## BLUF

**GO WITH NOTES.**

The change does what the author says. The inner try stops a revoked Proxy and a throwing `message` getter from making the catch throw. The failed event is re-buffered once, with the same object, id and hash. With `hashIntegrity` on or off, it is delivered once on the next flush. Nothing in the hunk changes the hash chain, the log text or the `error` key.

- **Red-first:** reproduced. 2 of 3 author cells fail by assertion at base, and 3 of 3 pass at head.
- **Author's mutant:** reproduced. 3 of 3 fail on `expected +0 to be 1`.
- **Mutants:** 15 variants in total. The author's cells kill 11 of 13 non-equivalent mutants (M11 is equivalent). My 13 extra probe cells kill all 13.
- **Whole shared suite:** run twice each side. The only red is the same base name (`wallet-signature`) in all 4 runs. No new red.
- **Merge with develop `b1fb543640e7`:** clean.
- **Importers:** the census holds. The only importer at head is the new test, and there is none at base. The other `AuditLogger` class is untouched.

**One medium note, not a regression (G73-F1).** The same catch still drops the event in a neighbouring class of value. That class is an Error whose `message` *can* be read but is not a string: a revoked Proxy, a BigInt, or an object whose `toJSON` throws. The real winston logger then throws inside `logger.error`, which runs before `unshift`. So `flush()` still rejects and the event is lost. This is pre-existing, the PR does not make it worse, and the author's cells cannot see it. None of the notes blocks a merge.

## Heads

| | PR head | develop | how read |
|---|---|---|---|
| START (03:15:54Z) | 9965740509dcfc6e1079826185fe36686fe9c63f | b1fb543640e7a439a9344d1d96d5a62862edfcf5 | `ls-remote origin refs/heads/develop refs/pull/1888/head` before any fetch, then fetched to `refs/gate/head` and `refs/gate/develop` (`logs/q1_heads_start.log`) |
| END (03:30:47Z) | 9965740509dcfc6e1079826185fe36686fe9c63f | b1fb543640e7a439a9344d1d96d5a62862edfcf5 | same `ls-remote` after every run. The clone `HEAD` is the same sha, and `git status --short` is empty (`logs/q1_heads_end.log`) |

The head did not move. Base = `refs/gate/head~1` = `a71479b49bf319a6349eb1450c13ef6a9f235a77` = merge-base with develop.

## FINDINGS

| id | severity | where | finding | red-before |
|---|---|---|---|---|
| G73-F1 | **medium** (residual of the same class; pre-existing; not a regression) | `packages/shared/src/security/audit-logger.ts:324` and `:328-330` | `reason` is typed `string`, but `error.message` is whatever the thrower put there. When it is readable but not a string, the inner try succeeds and the non-string reaches `logger.error`. The real logger (winston plus the PII-redaction format) then throws. That happens **before** `this.eventBuffer.unshift(event)`, so the event is dropped and `flush()` rejects. From the interval timer (`:140-142`, `this.flush()` with no catch) this is an unhandled rejection. Measured on the head's built dist with the real logger: `Error.message = revoked Proxy`, then `= {toJSON throws}`, then `= BigInt (10n)` all give `flush_threw=…, buffer_after_fail=0, delivered_after_retry=0`. The fixed case gives `flush_threw=no buffer_after_fail=1 delivered_after_retry=1`. The base has the same expression, so this is pre-existing (reasoned; I did not build a base dist). **Suggested shape (author's call):** coerce inside the inner try (`String(error.message)`), and/or re-buffer before logging. M11 shows the cells do not care about that order. | `logs/probe_reallogger_head.log` (head; the bad cases fail, the control passes) |
| G73-F2 | low (test gap) | `src/__tests__/ks1868-audit-logger-flush-unreadable-throw.test.ts` | Every author cell logs **one** event. So `unshift -> push` (M1) SURVIVES, which flips the retry order. `break` after the first failure (M12) also SURVIVES, which drops the rest of the batch. The biggest base data loss is not pinned: when the catch threw, the `for` loop aborted, so every **later** event in the same flush snapshot was neither delivered nor re-buffered. The fix does cure this, as probe P2 shows (A and C delivered, B retried). | `logs/mut_M1_A.log`, `logs/mut_M12_A.log` (3 passed); `logs/mut_M1_P.log`, `logs/mut_M12_P.log` (killed) |
| G73-F3 | info (pre-existing, unchanged) | `audit-logger.ts:318-331` | `unshift` inside the loop re-buffers several failed events in **reverse** order. Events A, B, C that all fail once are delivered after the retry as C, B, A. With `hashIntegrity` on, the chain is computed at `log()`, so it verifies in log order but **not** in delivery order. A sink that verifies the chain on arrival would reject a retried batch. Base behaves the same (readable errors). | `logs/probe_head.log` `G73_ORDER … buffer_after_fail=CBA delivered_after_retry=CBA` |
| G73-F4 | info (pre-existing; the PR moves the hostile class onto it) | `audit-logger.ts:269-274`, `:312-331` | When `onEvent` rejects every time, nothing caps the buffer, and retries grow quadratically: once the buffer reaches `maxBatchSize`, every `log()` re-flushes the whole buffer. With 10 `log()` calls and `maxBatchSize=3` there are **52** `onEvent` calls, 52 error-log lines, and the buffer ends at 10. At base this already happened for readable errors (the same 52). For the hostile class, base instead **lost** events: buffer 1, 3 `log()` rejections, 0 flush logs. The PR correctly moves that class into the retry path. The storm itself is not new. | `logs/probe_head.log` and `logs/mut_BASE_P.log`, `G73_STORM` lines |
| G73-F5 | info | PR body (author's readback) | The body could not be read live (see Q8). The readback is accurate on what changed and on blast radius. Its NOT-covered list does not name F1 (non-string `message`), F3 (retry order) or F4 (no cap on growth or retries). | n/a |

## Q1. Heads at START and END

See the Heads table: unchanged, so no STOP. Fetch only. The push URL is `no_push_qa_gate`. The clone is `git clone --shared --no-checkout` from the gate65 repo, and `git rev-parse --show-toplevel` was asserted before every fetch and every write. `repo/` is gitignored (`.gitignore:257`).

## Q2. Product hunk at source

Read whole: `audit-logger.ts`, 534 lines at head. The hunk is `:321-331`, and its neighbours are `log()` `:226-277` (hash at `:260-266`, push and size-triggered flush at `:269-274`) and the timer at `:139-143`.

- **Re-buffered exactly once:** yes. Probe P1, run for {hashIntegrity off, on} × {readable Error, revoked Proxy, throwing getter}, asserts that `eventBuffer` has length 1 and holds the **same object** after the failed pass. After the retry it asserts delivered length 1, the same id, the same hash, and an empty buffer. All 6 pass at head (`logs/probe_head.log`). M4 (double re-buffer) is killed by the author's cells and by the probe.
- **No duplicate delivery on the next flush:** yes. `flush()` snapshots and clears the buffer before the loop (`:315-316`). P2 and P3 assert unique ids. P4 races a `log()` against a failing flush that is still in flight: LATE and A are each delivered once.
- **Ordering:** for a single event, unchanged. For several failures, the order is reversed, as at base (G73-F3).
- **Hash chain (`hashIntegrity` ON):** the hunk does not touch `hash` or `previousHash`. A re-buffered event keeps its hash (P1 on), and the chain re-verifies over log order (P2 on, `verifyChain([a,b,c]) === true`). The author's cells run only with it off. My P1, P2 and P3 run with it on and off, and all pass.
- **Log text:** `'Failed to process audit event'` and the single key `error` are unchanged (P1 asserts `Object.keys(meta) === ['error']`; M8 and M9 are killed). A readable Error still logs `error.message`, which C1 pins and M13 confirms.
- **Repeated rejection:** the buffer grows without limit and retries grow quadratically. This is pre-existing for readable errors and is now reached by the hostile class too (G73-F4). At base the hostile class instead dropped events and made `log()` reject. That rejection is a caller-visible change the PR also fixes.
- **Residual:** an Error whose `message` is readable but not a string (G73-F1).

## Q3. Red-first and mutants

Product file applied, then restored from saved bytes with a **whole-file sha256 check** after every variant: head `9f12f9d3…f0c1`, base `ca363b03…b732`, `restored sha256 ok=True` for all 15. Mutants were applied only to `src/security/audit-logger.ts`, never under `src/__tests__`. Driver: `scripts/mutants.py`. Summary: `logs/mutants_summary.log`. Per-variant logs are `logs/mut_<id>_{A,P}.log` (A = author's 3 cells, P = gate's 13 probe cells).

| id | variant | author cells | gate probe |
|---|---|---|---|
| BASE | base product file | **2 failed / 1 passed** (R1, R2: `expected true to be false`); C1 passes | 10 failed / 3 passed |
| AM | author's mutant: delete the `unshift` line | **3 failed** (all `expected +0 to be 1`, lines 69/79/94) | 13 failed |
| M1 | `unshift` -> `push` | **SURVIVED** 3 passed | killed (2 failed: P3 order) |
| M2 | drop the inner try | killed (2 failed) | killed (10) |
| M3 | inner catch rethrows | killed (2) | killed (10) |
| M4 | double re-buffer | killed (3) | killed (13) |
| M5 | fallback text changed | killed (2) | killed (2) |
| M6 | re-buffer only on the unreadable path | killed (2) | killed (10) |
| M7 | re-buffer skipped on the unreadable path | killed (2) | killed (10) |
| M8 | log key `error` -> `err` | killed (3) | killed (8) |
| M9 | `logger.error` removed | killed (3) | killed (8) |
| M10 | fallback re-reads `String(error)` | killed (2) | killed (10) |
| M11 | re-buffer moved before the log line | survived | survived (**equivalent** under a mocked logger; with the real logger this order would be *safer*, see F1) |
| M12 | `break` after the first failure | **SURVIVED** 3 passed | killed (6: P2, P3, P5) |
| M13 | readable path logs `String(error)` | killed (1: C1) | killed (2) |

Author's cells: 11 of 13 non-equivalent mutants killed (M1 and M12 survive, G73-F2). Gate probe: 13 of 13. The author's red-first and mutant claims reproduce exactly.

The head targeted run gives `Tests 3 passed (3)` (`logs/head_targeted.log`). SPARK (optional, 79 s): HEAD 3 passed / 0 failed; BASE product 1 passed / 2 failed (`logs/spark_gate.log`, `logs/spark/facts.json`).

## Q4. Importer census

`logs/q4_importer_census_v2.log`, git grep at `refs/gate/head`, excluding node_modules and dist:

- Import, require or dynamic import of a path ending `audit-logger`: **1 hit**, the new test file (`:17`). At base: **0** (rc 1).
- Positive controls with the same pattern: `security/scopes` finds **9 lines** (rc 0); `secrets-manager|token-rotation` finds 1.
- No barrel re-exports it. Neither `src/index.ts` nor `src/security/index.ts` names it. No `@secuura/shared/security/audit` deep-path string exists anywhere. The only other mentions are the 3 `package.json` lines (51, 52, 136) and the PR's own fragments.
- The other class, `services/shared/src/security/audit.ts:318` (`export class AuditLogger`, with `new AuditLogger()` at `:461`), is untouched: `git diff --quiet base head -- Blockchain/Dev/services/shared` gives rc 0. `api-gateway/src/middleware/audit.ts` is untouched (rc 0). The PR changes exactly 4 files.
- Disclosure: my first census (`logs/q4_importer_census.log`) used `\s` in `git grep -E`, which git does not honour, so its import grep and both controls were blind. It is superseded by v2, which uses `[[:space:]]` and whose controls hit.

## Q5. Shared whole suite, before and after (×2 each)

Driver: `scripts/suite_ab.sh` (`logs/suite_ab_driver.log`). Base = base product file with the new test moved aside. Head = restored (sha256 OK for both files). Runs used `--maxWorkers=2` at nice 10, with load1 at the start between 3.90 and 4.40. Failing names come from the JSON reporter (`logs/failnames_{base1,base2,head1,head2}.txt`).

| run | Test Files | Tests | failing names |
|---|---|---|---|
| base1 | 1 failed / 56 passed (57) | 1 failed / 1098 passed (1099) | `wallet-signature.test.ts > … KS-278 accepts a valid wallet signature over the message` (AssertionError) |
| base2 | 1 failed / 56 passed (57) | 1 failed / 1098 passed (1099) | same |
| head1 | 1 failed / 57 passed (58) | 1 failed / 1101 passed (1102) | same |
| head2 | 1 failed / 57 passed (58) | 1 failed / 1101 passed (1102) | same |

**No new red.** The 3 new cells pass in head1 and head2. The KS-1155 timeout class did not fire at this load. Separately, a solo `ks879` run did time out at 30 s (`logs/cwd_check_ks879.log`), the load class.

Disclosure: a first pair of runs had cwd = the WEDNESDAY root, so 7 repo-walking guards could not find the Dev root. That pair is invalid and was stopped after the product file was restored (sha256 OK). It is quarantined in `logs/invalid_cwd_run/`. The runner was fixed to set the child's cwd to `packages/shared`.

## Q6. merge-tree

`git merge-tree --write-tree b1fb543640e7 9965740509dc` gives **rc 0**, tree **`76836a5f6b259bc4036ed7d3ca9686410b7a1dc3`** (git 2.54.0). Diff from develop to that tree: exactly the PR's 4 paths (A test, M audit-logger.ts, A two fragments). The product blob in the merged tree equals the head blob. Develop has not touched `packages/shared/src/security/` or `src/logger/` since the base (`logs/q6_merge_tree.log`).

## Q7. Fragment pair

`node Blockchain/Dev/scripts/docs-fragments.mjs check` (`logs/fragments_driver.log` and per-run logs):

- Clean: **OK rc 0** ("flow 117 legacy + 40 new, cheat 112 legacy + 40 new; lint clean, render passes html_docs_check"). The 2 ADVISORY lines say the committed page lags the render, which the design allows (exit 0).
- Planted flow fragment with a literal `999.` heading: **rc 1** (2 findings).
- The PR's own flow fragment with an unbalanced `<table><tr><td>` appended: **rc 1** ("table opened 5, closed 4 …"). The file was restored by sha256.
- Planted cheat `<p>` prose outside a table: **rc 1** ("prose outside a table in <p>").
- After all plants: clean again, OK rc 0.
- Note: short bare text outside a table (under the checker's 160-character `LONG_TEXT`, and not in `p`/`li`/`.note`) passes **rc 0** in both cheat and flow (`logs/fragments_check_planted_cheat_prose.log`, `logs/fragments_check_planted_flow_prose.log`). This is how the checker is built, not a PR defect. The author's "planted prose fragment rc 1" reproduces with a `<p>` plant.
- The PR's two fragments are accurate against the code. They do not mention F1, F3 or F4.

## Q8. PR body

`gh pr view` with the Blockchain project's `GH_CONFIG_DIR` says "not logged into any GitHub hosts". The unauthenticated REST call returns 404. **I could not read the live body.** Instead I read the author's own readback of the live body, `!CODING/Secuura/Blockchain/5_Project_History/2026-11-01_seatR-69th/evidence/pr2/pr/body_live_after.md` (read only; 10981 characters, mtime 14:12:58 local; the mail says 10980, probably a trailing newline). Whether GitHub carries exactly this text now is **unverified**.

Against the code, that readback:
- **TIER 1 statement:** accurate. A failed event is retried instead of dropped when the thrown value cannot be read. The record format, hash chain, log text, what is audited, and the retry for readable errors are all unchanged. One gap: the retry for a readable but **non-string** `message` was already broken and stays broken (F1). The statement does not claim otherwise, but it does not say so either.
- **Blast radius:** accurate. No importer at base, a published subpath, the api-gateway run labelled as a canary, and the other `AuditLogger` named and untouched. The 8-line census reproduces in substance (my v2 count differs only in method).
- **NOT-covered list:** accurate as far as it goes: other sites, api-gateway `audit.ts:334`, no booted service, platform suites, LTS Node, `npm ci`, deploy. It misses F1, F3 and F4.
- The stub episode is disclosed in the mail. The readback carries the TIER 1 block, the Test Evidence block and the hook verdict verbatim.

## NOT TESTED

- The live GitHub PR body (see Q8).
- A base build of `dist` with the real logger. F1's "pre-existing" label is reasoned from the identical expression at base, not executed.
- The timer-driven unhandled rejection was reasoned from `:140-142`, not executed. I did not test Node's `--unhandled-rejections` mode or process exit.
- api-gateway canary, `tsc`, `eslint`: not re-run (no importer; the author reports them).
- The four platform suites, a booted service, an LTS Node (host Node v26.8.1), any deploy.
- The other ~252 KS-1868 sites and the other `AuditLogger` class's catch sites.

## HOW

- Clone: `git clone --shared --no-checkout` from `0_Brain/reference/2026-11-01_gate65-r1r3-1868/repo` into `…/gate73-ks1868-auditlogger-1888/repo`. Partial-clone promisor config copied. Origin is GitHub (fetch only; the push URL is `no_push_qa_gate`). Refs are `refs/gate/head`, `refs/gate/develop` and `refs/gate/base`.
- `npm ci --ignore-scripts`: rc 0, "added 1795 packages in 28s" (`logs/npm_ci.log`).
- `@secuura/shared` build: rc 0 (`logs/shared_build.log`), and the dist contains `unreadable thrown value` once. This was run before any test.
- Runners:
  - `scripts/vt.sh` (author file and whole suite; nice 10; waits while load1 > 8, and no wait fired).
  - `scripts/vp.sh` plus `scripts/vitest.probe.config.ts` (gate probe, which lives **outside the repo** at `scripts/probe/g73-probe.test.ts` and imports the product by absolute path).
  - `scripts/probe_reallogger.js` (head dist, real winston).
  - `scripts/mutants.py`, `scripts/suite_ab.sh`, `scripts/fragments.sh`.
- The first `fragments.sh` run removed its own planted, untracked files with `rm -f`. Later plants were moved to the scratchpad quarantine `…/scratchpad/g73_quarantine/`. No tracked file was deleted.
- SPARK: `spark_gate.sh … develop <test> --work /private/tmp/gate73_spark_work`, rc 0, 79 s. It left a registered worktree at `/private/tmp/gate73_spark_work/head`.
- Logs are under `logs/` with stderr kept (`2>&1`).
- No secrets were read or used. The sibling clone's ssh deploy key was used for fetch only. Nothing was written to GitHub, Linear, mail or `!CODING`. `git status --short` in the clone is empty at the end.
