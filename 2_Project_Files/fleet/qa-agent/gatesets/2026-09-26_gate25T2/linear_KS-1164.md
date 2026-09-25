KS-1164 gate/report.ts writeGateReport overwrites the input summary when --summary does not end in -summary.json
state In Progress

## BLUF

`systemTest/performance/gate/report.ts:325` derives the gate-report path with `const reportPath = summaryPath.replace(/-summary\.json$/, '-gate-report.json');`. When the `--summary` path does not end in `-summary.json` the replace is a no-op, `reportPath === summaryPath`, and `:346` `fs.writeFileSync(reportPath, …)` **overwrites the raw k6 summary with the gate report** — silently, with the log line claiming success. The runner's own naming (`runner/cli.ts:209`, `run_dir.ts:300`) always ends `-summary.json`, so the default pipeline is safe; the exposure is the documented `--summary` override on either CLI (`runner/cli.ts:22`, `gate/cli.ts:15`) — the by-hand re-gate path — and the loss is of the run's only raw record.

Found by the tier-2 QA gate on PR #988 (KS-704) as **F-5, Major, develop-own**: `writeGateReport` is byte-identical at that PR's base M38 `0e78c7270` and head `8cb99a002`, so it is NOT #988's regression and was not a NO GO; it exists at M38 and on every later develop. Report: `Testing Agent MAIN/projects/secuura/reports/2026-09-14-988-ks704-tier2-r1/report.md` §5 F-5 (evidence `cli_conv.out`, `p8`…). Filed by the merge seat s228 on Wednesday's ADDENDUM 2026-09-14 09:10:43Z. Board searched first by the symbol `writeGateReport` (0 hits), the path `gate/report.ts` (4 hits: KS-704 itself, KS-1066, KS-929, KS-971 — none about this overwrite), `summaryPath.replace` (0) and `-gate-report.json` (2 archived report mentions) — every KS issue incl. archived, titles + descriptions + comments.

## Repro (the gate's, verbatim in substance; measured at runtime, replicated ×3)

From a known state (`systemTest/performance` after `npm ci`):

1. `cp tests/unit/fixtures/smoke-summary.json <dir>/summary.json` (k6's own `--summary-export` default basename).
2. `npx tsx gate/cli.ts --scenario smoke --summary <dir>/summary.json`
3. Read `<dir>/summary.json`.

**Expected** (oracle: Purpose + Product — the function's docstring and the log line say it *writes the gate report beside the summary*; `runner/cli.ts:22` documents `--summary` as a free path): a new `…-gate-report.json`; the input untouched.

**Observed:** stdout `[ci-gate] Gate report written: <dir>/summary.json`; the file's keys become `scenario,slot,slotTag,gatewayPort,runLabel,timestamp,passed,results` — the `metrics` map is gone; sha256 `a8f5ed22…` → `86143afe…`. Reproduced on the breached copy, the healthy copy and a third fresh copy.

**Control:** the same file named `smoke-summary.json` → `smoke-gate-report.json` is written beside it and the input is intact.

## Reach

* The documented `--summary` override on either CLI (`runner/cli.ts:22`, `gate/cli.ts:15`) — the path a human uses when re-gating an old run by hand. The default runner pipeline never produces a non-conforming name.
* **Sibling of the same class (read only, not reproduced):** `runner/k6_docker.ts:241` `summaryMount.replace(/-summary\.json$/, '-k6.log')` — with the same non-conforming name the k6 log path collapses onto the summary mount.

## Fix-shape (for the owner)

* Derive `reportPath` from the directory + scenario: `path.join(path.dirname(summaryPath), scenario + '-gate-report.json')`, and/or throw when `reportPath === summaryPath`.
* Apply the same shape to the `k6_docker.ts:241` sibling.

## Regression cell

A unit cell that calls `writeGateReport(results, '<tmp>/summary.json', 'smoke')` and asserts (a) the input file's sha256 is unchanged and (b) a sibling `smoke-gate-report.json` exists beside it. A second cell for the `-summary.json` control keeps the existing behaviour pinned.

## Definition of done

- [ ] `writeGateReport` never writes to its input path; a non-conforming `--summary` name yields a sibling `<scenario>-gate-report.json` (or a thrown, named error).
- [ ] The `k6_docker.ts:241` sibling handled the same way or recorded as accepted with the reason.
- [ ] The two regression cells above green; the existing `tests/unit/gate/` cells and goldens unchanged.

## Follow-up (ruled by Wednesday 2026-09-14 10:11Z, from the #988 gate F-3)

* The `reportFailedGateBreakdown` cell (`systemTest/performance/tests/unit/gate/reportFailedGateBreakdown.test.ts:103-108`) builds its expectations with `String(n)` while the product prints `toLocaleString()` — they coincide only below 1,000; build the expectation with `toLocaleString()` or add one cell with a synthetic `{ http_server_error: { passes: 1234, fails: 0, value: 1 } }` expecting `passes=1,234` under a pinned locale.
