KS-1226 systemTest performance `unitSuiteSlotIndependence.test.ts`: the 15 s budget at :127 is tight under load, and the :99 summary regex returns NULL when the child summary includes "skipped"
state In Progress

**BLUF:** two defects in one consumer, `systemTest/performance/tests/unit/utils/unitSuiteSlotIndependence.test.ts`, which spawns child vitest runs and parses their summary. Both are pre-existing and unchanged between vitest 4.1.10 and 4.1.11. Severity Polish.

1. **:127 budget (F4).** The test's 15000 ms timeout is \~13.3–13.4 s of real work at load1 \~19 on BOTH vitest versions, so it times out under load. Seen twice on 2026-09-17: at 16139 ms during the #1030 author's run, and at 17.11 s in the gate's A/B. A duration, not an assertion.
2. **:99 regex (F5).** `/Tests\s+(?:(\d+) failed \| )?(\d+) passed \((\d+)\)/` returns NULL on a summary that includes skipped tests, e.g. `Tests  1 failed | 1 skipped | 243 passed (245)`. The consumer would then throw "could not read the child vitest summary" instead of reporting the counts.

Refs KS-1211. Found by the tier-2 QA gate on #1030, findings F4 and F5 (one ticket, same file). The report is `Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1211-1030-e43af4934-tier2-r1/report.md`.

## The gate's findings, quoted

> | F4 | Consumer `unitSuiteSlotIndependence.test.ts:127` timed out at 15000 ms once at head (17.11 s, load1 20.6) under my own concurrent root installs; under the same load both sides took \~13.3–13.4 s; quiet A/B equal | measured, 10 runs | Polish (RECORD; duration, not assertion; READY saw the same at 17cbb1091) | TICKET-class (the 15 s budget vs a child-vitest matrix is \~13 s at load1 \~19 on BOTH versions) | Comparable (base vs head at equal load) |
>
> | F5 | Consumer `:99` regex returns NULL on a child summary that includes `skipped` (e.g. `Tests  1 failed \| 1 skipped \| 243 passed (245)`) → the consumer would throw "could not read the child vitest summary" | measured (probe, controls) | Polish (curio; pre-existing, format unchanged 4.1.10→4.1.11) | TICKET-class | Product |
>
> `:99` regex probe (`suites/consumer_regex_probe.out`), read from the file at head: vitest 4.1.11 passing output → failed 0 / passed 3 / total 3; 4.1.11 failing output → 1/2/3; packages/shared 4.1.11 → 0/851/851; 4.1.10 → 0/3/3. Controls: `Tests  245 passed` (no parens) → NULL; `… (245)` → match; `2 failed | 243 passed (245)` → match; `1 failed | 1 skipped | 243 passed (245)` → NULL (F5).

A/B timings from the gate (base 4.1.10 | head 4.1.11): concurrent round 1 13.42 s | 13.29 s; concurrent round 2 **timed out 17.11 s** | 6.33 s; quiet 5.98 s | 5.64 s and 5.62 s | 5.72 s.

## First item

This is a systemTest harness file, so the change goes through the systemTest rules (all four quality gates). Decide the budget: size it to the child matrix, or run the matrix without the per-test timeout. Also widen the regex to accept an optional `N skipped |` segment, with the gate's probe lines as the regression cells.

## Board search before filing (2026-09-17, team Secuura-PK, archived issues included, literal match on titles, descriptions and 3446 comments):

* `unitSuiteSlotIndependence`: 0 issues, 0 comments.
* `slot independence`: KS-1167 (a harness-guards port, Done), not this.
* `skipped |`: KS-1046, KS-1016, KS-1015, KS-687; comments on KS-1169, KS-39, KS-502, KS-519, KS-961. None concerns this regex.
