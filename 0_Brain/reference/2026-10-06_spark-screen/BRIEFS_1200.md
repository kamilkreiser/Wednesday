# Spark briefs, 12:00 batch (2026-10-06): 3 queued

Written 2026-10-06 12:21 AEDT (shell `date`) by a Spark brief-writer sub-agent for Wednesday. Secuura only.

**Base.** develop `4eaf7741a6a4`, read by round.sh's own `ls-remote` at 11:58:42. The cache clone was refreshed only by `round.sh --dry-run`.

**Read-only on client systems.**
- Linear: GraphQL reads only.
- GitHub: REST GET only.
- Every git write verb ran in scratch clones under the session scratchpad.
- Nothing was written under `!CODING/`.

**Not started:** `queue.sh` (`pgrep`: not running) and any model call. Wednesday starts the drain.

## BLUF

**3 briefs queued, fewer than the 4–5 asked for.** All 3 passed both checks:
- dry-run rc 0;
- `--control` CONTROL-PASS 7/7. The new cells go red without the fix and green with it, and the golden is byte-identical to the patch the checker extracted.

**Why only 3:**
- The delta pool is the same 10 tickets the 10:10 screen read (`updatedAt > 2026-10-05T13:00Z`: TOTAL 10, nothing new since).
- Of the preferred tickets, only KS-1328 and KS-1355 pass the predicate. KS-1355 gave 2 single-file carves.
- Every other preferred or T1/T2/T2b candidate fails a clause (table below).

## Queued

| Brief dir (`night/briefs/`) | Product file | Tier | Edits | Dry-run | Control |
|---|---|---|---|---|---|
| `KS-1328-db-retry-describe-budget` | `services/kyc/src/__tests__/db.retry.test.ts` | code_patch, SELF-TESTING (one file) | 2 hunks (budget + 1 new cell) | rc 0 | CONTROL-PASS 7/7. RED with the test hunk alone: `1 failed / 6`, `expected 5000 to be 60000` (by assertion). GREEN 6/6. kyc 33 → 34 tests, 0 failed. tsc rc 0. |
| `KS-1355-dev-reload-slot-container` | `scripts/dev-reload.sh` | bash_patch (new test) | 1 hunk | rc 0 | CONTROL-PASS 7/7. RED at the tip: 4 FAIL lines (`3 passed, 4 failed`). GREEN `7 passed, 0 failed`. B6: no sibling suite drives the script. |
| `KS-1355-stack-guard-one-line-per-project` | `scripts/stack_guard.sh` | bash_patch (existing suite modified in place) | 2 product hunks + 1 test hunk | rc 0 | CONTROL-PASS 7/7. RED at the tip: 2 FAIL lines (`25 passed, 2 failed`). GREEN `27 passed, 0 failed`. B6: `stop_secuura.test.sh` no new failure. `check-stack-safety.sh`: 100 invariants OK. |

Queue lines appended: `KS-1328-db-retry-describe-budget`, `KS-1355-dev-reload-slot-container`, `KS-1355-stack-guard-one-line-per-project`. Each pin set lives in its brief's `spark.pins`.

### UNMEASURED, per brief

**KS-1328**
- The fleet load was not reproduced. The cell pins the 60 s budget; it does not prove that future loaded runs pass.
- **Wednesday's call:** the ticket lists 3 fix shapes "not chosen here". This brief takes shape 2, which the ticket itself names as the smallest. Hold it if you read the menu as a decision owed to Kamil.

**KS-1355 dev-reload**
- No real Docker or stack; docker and npm are stubbed.
- The test pins `LC_ALL=C` because of a separate defect (finding 1 below).

**KS-1355 stack_guard**
- No real Docker.
- A project with two different real owners now prints one line (the newest container's tuple), where the tip printed two. This follows the ticket's "group by project" and was not measured on a real host.
- The `(+N container(s) with owner unknown)` wording is the brief's own choice.
- **Wednesday's call:** the file is the KS-666 stack-ownership guard. Only its informational listing changes, and all 24 existing cells stay green.

**All three:** GNU bash/awk (Linux) not run; macOS `/bin/bash` 3.2.57 and BWK awk were.

## Considered and not queued

Each line gives the predicate clause that failed and the instrument that showed it.

| Ticket | Clause that failed (instrument) |
|---|---|
| KS-1324 | **Open PR on the file:** #1250 (KS-1302/1303) touches `run_shell_suites.test.sh` and `run-shell-suites.sh` (GitHub REST GET, 25 open PRs and their files, 12:01). Also a **bash test-only change, which no wired tier runs** (`build_bash_input.sh` has product-fix and self-testing modes only). |
| KS-1421 | **Decision.** Peter's 10-05 comment says "this needs one of" three mechanisms. It also spans ~15 cases over 5 files, `systemTest/akto` is Peter's split, and it is security-tier. No new reason since the 10:10 screen (Linear read). |
| KS-1393 (the ticket; PR #1393 is KS-1278, excluded) | **Not one product file and a decision:** 31 spec files, 708 branches and a duplicated package. "a judgement call per file"; row 3 "Decide:" (Linear read). |
| KS-1163 | **Three files, not two**, and the old counter is spent. Kam's 09-22 ruling ("Wait for all five") removes the decision, but the fix also reds `start_secuura_slot_names.test.sh`: `readonly EXPECTED_COUNT=27` at `:46` (read at the tip), and the 09-16 night4 checker measured B6 `before=0 after=8`. So it is product + 2 suites. It was also reallocated to Claude on 09-16 after 4 Ornith rounds (`night/done.md:173`). |
| KS-1355 spot 2, `start-local.sh` half | **Decision:** the ticket says "(or retire `start-local.sh` if unused)". |
| KS-1355 spot 2, `check-stack-safety.sh` must-source rule | Would red on scripts that don't source `stack_env.sh` today, so it needs a per-script ruling. |
| KS-1355 spot 3 | `docker-compose.yml`: **no in-process runner** (needs `docker compose config`). The `CORS_ORIGINS` default at `:503` also carries the 6100–6103 portal ports, which needs a per-slot decision. |
| KS-1355 spot 4 | `preflight.sh:94`: a file every gate pins as NO-NEW-LEG. |
| KS-1327 | **Decision:** "Fix shapes, not chosen here"; "behaviour changes to a persistence path and want their own gate" (Linear read). |
| KS-1145 | Bash test-only cells in a **real-PostgreSQL** suite: **no wired tier and no in-process runner**. |
| KS-1392 | `.github/workflows/ci.yml`: Kam-class, and **no runner**. |
| KS-1382 | **Not one file** (5 entry points). It is the DAST/ZAP/tenant-isolation audit harness (**security-tooling surface**), and its acceptance requires slot tests across all five in one PR. |
| KS-1381 | **Multi-file.** The two single-file carves fail separately: `auth-matrix-smoke.sh` is an **auth-named harness**, and `smoke-test.sh` is touched by the held `READY_KS-1250` (a collision). |
| KS-1417 | **2 files**, and a "your call" between delete and replace-with-comment. |
| KS-1424, KS-1423, KS-1422, KS-1414, KS-1412, KS-1051, KS-1038, KS-709, KS-492 | The 10:10 screen's verdicts stand. Same delta, re-listed by Linear `updatedAt > 2026-10-05T13:00Z` → TOTAL 10, none updated since. |
| KS-723, 938, 1278, 1419, 1424, 1402, 1305, 1256, 1136, 998, 1313, 1326, 1164, 1364, 593 | Excluded outright by the commission. |

## Findings (nothing edited outside the brief dirs)

1. **A separate defect in `dev-reload.sh`, with no ticket.**
   - **What happens:** `:73` `echo "▸ [3/3] restart $CONTAINER…"`. Under macOS `/bin/bash` 3.2 in a UTF-8 locale, bash reads the ellipsis bytes as part of the variable name. With `set -u` the script aborts with `CONTAINER…: unbound variable`. That is after the `docker cp` and before the restart, exit 1.
   - **Measured** on the fixture at the tip: `LC_ALL=en_US.UTF-8` gives rc 1 (log shows `cp`, no `restart`); `LC_ALL=C` gives rc 0.
   - **Likely fix:** a one-character change (`${CONTAINER}…`).
   - **Not briefed:** a brief must carry one ticket, and none covers this. It needs a ticket, which is Wednesday's or Kamil's call.
2. **Tooling: bash_patch goldens must not carry `diff --git` / `index` lines.**
   - The bash checker splits sections on `--- `. So the next section's `diff --git` and `index` lines end up as trailing garbage in the previous section.
   - The first `--control` of the dev-reload brief failed `B2 … patch with only garbage at line 108`. After stripping those lines it was CONTROL-PASS.
   - The held KS-1388 bash goldens already carry `---`/`+++` only.
   - `KS-1136-aggregate-unreadable-artefacts/golden.diff` and `KS-998-format-gate-grep-fixed/golden.diff` do carry `diff --git` lines. Their `--control` would likely fail the same way. **Not measured.** It does not affect a model round, because the golden comparison there is informational.
3. **Blank context lines are refused by the builder (KS-1229 r1 gate).**
   - All three briefs had a blank line next to the edit point.
   - Each was hand-shaped: the blank line is removed with a lone `-` and re-added with a lone `+`, so the hunk's context is non-blank.
   - Both tiers accepted it: A3c/A3d and B3b passed, and `git apply` strict rc 0.

## Disk

The 4 `--control` rounds left per-round clones under `spark/cache/work/` (`spark_secuura_2026-10-06_KS-1328…-control_*`, `KS-1355-dev-reload…-control_*` ×2, `KS-1355-stack-guard…-control_*`), roughly 335 MB each. Nothing was removed.
