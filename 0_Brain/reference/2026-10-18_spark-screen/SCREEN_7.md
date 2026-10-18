# Spark screen, part 7 (2026-10-19 ~06:1x-07:1x AEDT): KS-1628 / KS-1622 / KS-1621 / KS-1620 and the KS-1627 follow-up; six briefs, seven model rounds, six PASS

By a Spark brief-writing sub-agent for Wednesday. Secuura only. Briefs written against develop `840ac4182d750d38ace9bea578e7fc6af100fd7b` (`cat-file -t` = commit; the cache's own fetch had it). Develop moved to `83ed01af70fd5ed6cca9ac66f28ddcb8a1034105` (#1586, KS-1627) during the run; round.sh's stale check passed for every brief (none of its files changed) and every control and round after the first control ran at `83ed01af70fd`. The first control (KS-1628) ran at `840ac4182d75`; its model round ran at `83ed01af70fd`. The KS-1627 follow-up brief is written at `83ed01af70fd`. Nothing held, raised, pushed, merged, committed or deleted. No GitHub or Linear writes, no Docker.

Ticket text: NOT read for any ticket. The harness builder's metadata line showed the KS-1628 title (and the dry-run input.json carries only the title; the description field is replaced by the brief). I did not source a Linear key by hand. The briefs rest on Wednesday's commission text plus the gate verdicts under `0_Brain/reference/2026-10-18_gate-{D,E1,E2}-*/` (Gate D for KS-1620, E1 for KS-1622, E2 for KS-1621). The KS-1628 sites were re-read at source.

## Result

| # | ticket / item | brief dir (`local-model/night/briefs/`) | mode / rung | edit points | control | round verdict | golden | model s / tokens | run dir (`local-model/runs/`) | FAIL class |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | KS-1628 item 3 (anchoring `anchorReadback.ts:115` uses the exported `FABRICATED_TX_PREFIX`) | `ks_1628_anchoring` | code_patch, rung 2 | 3 (import insert, line 115, 1 NEW vitest file) | CONTROL-PASS 7/7 BYTE-IDENTICAL (`..._ks_1628_anchoring-control`) | PASS | BYTE-IDENTICAL | 33.8 / 12401+1343 | `spark_secuura_2026-10-19_ks_1628_anchoring` | none |
| 2 | KS-1622 item "KS-1545 logs nothing for an upstream error status" | `ks_1622_platform` | code_patch, rung 2 | 2 (one inserted line in platform.ts, 1 NEW vitest file) | CONTROL-PASS 7/7 BYTE-IDENTICAL, both briefs (`..._ks_1622_platform-control`, `...-control-r2`) | round 1 FAIL, round 2 (the one rebrief) PASS | r1 DIFFERS; r2 BYTE-IDENTICAL | r1 67.8 / 25907+2551; r2 67.9 / 26089+2554 | `spark_secuura_2026-10-19_ks_1622_platform` (r1), `..._ks_1622_platform-r2` (PASS) | r1: model (one transcribed character, see below) |
| 3a | KS-1621 height-0 cell (KS-1509) | `ks_1621_originate` | test_only (jest), rung 1 | 1 (insertion into ks1333 test) | CONTROL-PASS 7/7 BYTE-IDENTICAL | PASS | TREE-IDENTICAL | 18.1 / 18677+191 | `spark_secuura_2026-10-19_ks_1621_originate` | none |
| 3b | KS-1621 constructor-name arm (KS-1619 p3) | `ks_1621_apigw` | test_only (vitest), rung 1 | 1 (insertion into ks1543 test) | CONTROL-PASS 7/7 BYTE-IDENTICAL | PASS | TREE-IDENTICAL | 33.2 / 32542+273 | `spark_secuura_2026-10-19_ks_1621_apigw` | none |
| 4 | KS-1620 item 1 (bound the relayed error text, 200 chars) | `ks_1620_info` | code_patch, rung 2 | 3 (comment line + line 133 in one hunk, 1 NEW vitest file) | CONTROL-PASS 7/7 BYTE-IDENTICAL | PASS | BYTE-IDENTICAL | 34.4 / 11389+1455 | `spark_secuura_2026-10-19_ks_1620_info` | none |
| 5 | KS-1627 follow-up (Wednesday's mid-task add): real redis in REDIS mode over a fake ioredis answers 200 | `ks_1627_p2` | test_only (vitest), rung 1 | 3 hunks of the one existing test file (import `vi`, fake ioredis block, cell R3) | CONTROL-PASS 7/7 BYTE-IDENTICAL | PASS | TREE-IDENTICAL | 21.7 / 14716+586 | `spark_secuura_2026-10-19_ks_1627_p2` | none |

brief_lint rc 0 and dry-run rc 0 for all six before any control or round. Rebrief counter: only KS-1622 used its one rebrief (the original failed A4, the rebrief passed); no brief is reallocated to a Claude seat.

## Skipped items (predicate), one line each
- **KS-1628 item 1** (deprecated POST /api/documents/:id/verify): a decision for Kam, per the commission; not briefed, not touched.
- **KS-1628 item 2** (stale prefix comment at `originate/src/routes/anchors.ts:62`): comment-only, no red cell is possible, round.sh runs no comment tier, and the line carries a non-ASCII character (`...` in `tx_...`) that the harness mishandles on a changed line. Also the comment is in `originate`, not `anchoring` as the commission wrote; I took it to be the KS-587 comment at `originate/src/routes/anchors.ts:62-64` (the only anchors.ts with a three-prefix comment); not verified against the ticket.
- **KS-1622 "KS-1613 step() N3"**: I could not identify it. The gate E1 verdicts number the preflight findings N1 (raw tail echo, "no action needed") and N2 (no cell with a slash in the title); their N3 is about platform.ts. The ticket body was not read, so I would be guessing which one is meant. Not briefed.
- **KS-1622 "#1570 second-slash cell"**: the fix shape is clear (Fable MINOR: a `3/16  Title (a/b)` cell kills the `${1##*/}` mutant) but it is a bash `*.test.sh` suite change with no product edit, and round.sh's `test_only` is code_patch's vitest/jest mode (README Tiers), bash_patch needs a product edit with a red test. No tier fits. Not briefed.
- **KS-1620 "refused" wording**: what the note should say for a 500 or a proxy 502 is a wording decision (and ks1541 cell C3 pins the current text), not a fix shape. Not briefed.
- **KS-1621 constructor-name arm and height-0**: both briefed (3a, 3b).

## Checker lines
- ks_1628_anchoring: `RESULT: PASS (7/7)`; A3b 1 site; A4 "2 failed / 4 run; controls green; assertion reds"; A5 4 passed / 4; A6 whole anchoring suite no new red; A7 tsc rc 0; A2a hunks=2 ok=2.
- ks_1622_platform r1: `RESULT: FAIL (1 failed)` at A4: "CONTROL cell(s) red at the tip: E3, E4, E5 (5 failed / 5 run); the harness does not reach the code". r2: `RESULT: PASS (7/7)`; A4 "2 failed / 5 run; controls green; assertion reds"; A5 5 passed / 5; A6 whole api-gateway suite no new red; A7 rc 0; A2a hunks=1 ok=1.
- ks_1621_originate: A3 test-only; A4 "1 failed / 15 run; controls green; assertion reds"; A5 15 / 15; A6 whole originate suite; A7 rc 0; A2a hunks=1.
- ks_1621_apigw: A4 "1 failed / 10 run"; A5 10 / 10; A6 whole api-gateway suite; A7 rc 0.
- ks_1620_info: A3b 1 site; A4 "2 failed / 4 run"; A5 4 / 4; A6 whole mcp-server suite; A7 rc 0; A2a hunks=1.
- ks_1627_p2: A4 "1 failed / 5 run; controls green; assertion reds" (only R3 reds under the always-503 tamper, R1/R2 and C1/C2 stay green); A5 5 / 5; A6 whole api-gateway suite; A7 rc 0; A2a hunks=3 ok=3.

## Red cells, tampers and controls (exact titles are in each brief's `## Red cells`)
- KS-1628: RED `P1` (a hash the exported prefix matches is read as a placeholder) and `P2` (a hash the exported prefix does not match is read as real, even `tx_sim_`); both work by `vi.mock('../honestAnchor')` replacing the export with `/^zz1628_/`, so they pass only if `buildVerifyResponse` reads the export. CONTROL `P3` (real 64-hex hash, explorer link), `P4` (row with no hash).
- KS-1622: RED `E1` (first window 500 with a JSON body -> ONE warn `{ status: 500, windowsRead: 0 }`), `E2` (401 'No token provided' -> `{ status: 401, windowsRead: 0 }`, the body text never logged). CONTROL `E3` (a SECOND window answering 503 still logs exactly one line, from the catch: this is what forces the `collected.length === 0` limit), `E4` (refused connection, one line), `E5` (healthy, none).
- KS-1621 originate: RED `F5` (a real prior height 0 is carried as 0); tamper `blockHeight: prior?.blockHeight ?? null` -> `|| null` (the gate's mutant). KS-1621 apigw: RED `D4` (a thrown `Ks1621Fault` class instance logs `thrown Ks1621Fault with fields [code, detail]`, no value); tamper replaces `(Object.getPrototypeOf(err)?.constructor?.name ?? 'object')` with `'Object'` on verification.ts:1580.
- KS-1620: RED `B1` (503, 5000-char object message -> first 200 only), `B2` (403, 500-char string error -> first 200). CONTROL `B3` (exactly 200 whole), `B4` (short whole).
- KS-1627 follow-up: RED `R3` (initRedis over a fake ioredis that keeps a store -> isRedisAvailable true -> stored list `['KS1627_REDIS_DOC']` answered 200 with id `ks1627-c1`). Tamper `health.ts:53` `=== false` -> `=== false || true` (a guard that always refuses).

## The one FAIL and its class
KS-1622 round 1: the product line was correct but the model dropped `\*` in the stub's `/COUNT\(\*\)/` regex, writing `/COUNT\(\)/`; the audit_logs COUNT query then never matched and every test cell failed at the tip, so A4 refused it. Class: **model** (a single transcription error on an escaped regex), with a brief-side contributor (a brief that copies an escaped regex invites it). The rebrief named the miss and replaced the regex with `sql.includes('COUNT(*)')`; round 2 PASS, BYTE-IDENTICAL. Tooling note: escaped regex literals inside a given-whole test are a known risk for the model; prefer a non-regex form in the golden. Original saved as `KS-1622.md.pre-r2` and `golden.diff.pre-r2` beside the brief.

## Decisions and things Wednesday should read
- **Item 5 needed a pin.** KS-1627 is "In Progress" in Linear, so the builder REFUSED the dry-run ("a seat has it"). I added `started_ok=Wednesday_coordinator_directed_this_follow-up_...` to `ks_1627_p2/spark.pins`, on your message directing this follow-up after #1586 merged. **Whether a live seat lane holds KS-1627 is yours to confirm** (I could not check). Remove the pin line if it does.
- The item 5 cell is titled `RED KS-1627 R3`, not `CONTROL`: the harness refuses a CONTROL-titled cell that reds under the tamper (A4), and R3 must red under your always-503 tamper. In substance it is the control you asked for. It is the last cell in the file because C1 asserts `isRedisAvailable()` is false (never initialised) and R3 calls `initRedis()`; the file-level `vi.mock('ioredis')` only matters once `initRedis()` runs.
- KS-1620: the bound of **200** characters and the absence of an ellipsis marker are my choices (the gate measured the real gateway at about 90 chars). Confirm against the ticket body.
- KS-1622: the warn context string `GET /api/platform/audit-log upstream answered an error status` and meta `{ status, windowsRead }` are my choice; the new line is limited to the first window (`collected.length === 0`) so a later window's error still gives one line, not two. A first window answering 200 with a non-list body (the same gap with another cause) is NOT covered. platform.ts is an audit-log route (`authenticateToken`/`requireSuperAdmin` untouched, log line only): read the diff at source, as the 10-05 rule says.
- KS-1628 item 3: behaviour-neutral refactor; the red cells work by mocking the export. The KS-522 comment above `:115` still lists the prefixes in prose (not edited).
- Open-PR overlap on any product file other than the ones #1586 touched: NOT checked. #1586 is merged now (develop `83ed01af70fd`), so the exclusion in the commission held trivially.
- Ordering: all six diffs are on disjoint files and apply in any order (platform.ts; anchorReadback.ts; info.ts; and tests only for 3a, 3b, 5; 3b edits `ks1543-...test.ts`, KS-1622 adds a new api-gateway test file).

## NOT tested / unmeasured
- I did not read the model patches beyond the checker lines and the round-1 diff of KS-1622; the goldens are byte- or tree-identical, so Wednesday reads the goldens at source.
- No jest/vitest/tsc by hand; every red/green figure is the checker's.
- Ticket bodies (all five tickets), open-PR overlap, live seats' unpushed work, whether any demo/production data matters to any change.
- Audit surface: KS-1622 (log-only on the super-admin audit-log route), KS-1628 (honest labelling of verify, behaviour-neutral). Not auth or credential changes.

## Files written
Briefs: `local-model/night/briefs/ks_1628_anchoring/`, `ks_1622_platform/` (+ `.pre-r2` copies), `ks_1621_originate/`, `ks_1621_apigw/`, `ks_1620_info/`, `ks_1627_p2/` (each `KS-<n>.md`, `golden.diff`, `spark.pins`). Run dirs and `spark/state/dry/` are round.sh's own; `spark/cache/work/` accumulated 6 control + 7 round clones (not pruned). Scratch: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/ff943889-d9ba-463a-a66e-300867d673bd/scratchpad/spark_screen7/` (generators `gen_*.py`, `lib.py`, `pre.sh`, `both.sh`, apply-check trees; `q_1628_a/` holds the first KS-1628 draft that the builder refused, moved aside, not deleted).
