# COMMISSION — DRAFT the round-24 tier-2 QA batch gate kit "gate24T2a" over FOUR PRs (Seat L6), WIDENED to four and FROZEN. Do NOT launch.

Relayed by Wednesday to the drafter on 2026-09-25 (~23:5x AEST); WIDENED mid-draft (~00:1x AEST 2026-09-26) by Wednesday's message: "add a 4th PR to
gate24T2a and FREEZE at four". Recorded here as the gate's commission; the QA agent reads it. Shape copied from `gatesets/2026-09-25_gate21T2e/` and
`2026-09-25_gate21T2d/` (JSON pins, routing-file override, controls both ways with `--invert`), re-keyed to FOUR rows, with BRIEF_TEMPLATE.md and
QA_AGENT_CHARTER.md.

## The batch — all TIER 2 per the seat, one seat (Seat L6), every head re-read by the drafter from origin
- **#1243** KS-1117 + KS-1300 items 2-4, head `0c89e2b503d9333829c277c50ad3b1a33f03cb96` — the readYaml family: `systemTest/performance/utils/yaml.ts`,
  `tests/unit/config/sheddingCeiling.test.ts`, `tests/unit/package_scripts.test.ts`, the NEW `tests/unit/support/readYamlRouting.ts`, and
  `tests/unit/utils/yamlRedaction.test.ts` (5 files; the commission named three, the drafter READ five). KS-1300 item 1 (READYAML-UNGATED)
  deliberately NOT built. Round-1 context: READYAML-UNGATED / CANARY / ROUTING / SHAPES in report `2026-09-25-batch1218-t2c`.
- **#1244** KS-1111, head `146b620fda53f008b3384334a474b06a16235af3` — `systemTest/performance/runner/k6_docker.ts` (+ its test file). No widening of the
  masked name set (the drafter READ SECRET_ENV_NAME byte-identical BASE -> head).
- **#1245** KS-1313, head `1700b5ae7dd56ad3e30602a40b20ae6469c35350` — the KS-1226 item-2 vitest summary parser on
  `systemTest/performance/tests/unit/utils/unitSuiteSlotIndependence.test.ts`. **#1241 is an OPEN, capped, unmerged older PR on the same file — do NOT
  grade #1241; #1245 is judged against develop.** It is the THIRD attempt at this defect.
- **#1248** KS-1143 GF-2, head `2b4960172644b5ef0414b94d46d11974012c2007` (WIDENED in) — a cherry-pick of Seat L3's unpushed `a40cb9eea049` onto develop:
  LEG F reads the guard from the parser's continuation (`Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts`, the
  `routerParserAnalysis` instrument + its cells). KS-1144 (J2 scaffolding, to branch later from #1248's head) is NOT in this batch.
- **FREEZE:** four, by Wednesday's widen message. The seat's #1245 READY says "That is four tier-2 READYs by your launch count" — that fourth was #1248.

## The gate MUST (Wednesday's list, carried into the prompt)
1. **#1245 — MANDATORY LIVE-SHAPE** (the third attempt): re-capture real vitest 4.1.11 `--reporter=default` summaries from fixtures OUTSIDE the package,
   PIPED (not a TTY; the piped final line comes from the renderer that drops `passed` at 0): fail-only, skip-only, todo-only, expected-fail+pass,
   fail+pass+skip, pass-only, multi-file. Run them through the REAL code path (the exported parser / childSuiteCounts(), never a lifted regex).
   **NULL or wrong counts on ANY real shape = NO GO.** Also tamper the call site and the :103-equivalent reading (head :210) to show the cells reach it.
   Prior reports: `2026-09-25-batch1241-t2d/report.md` and `2026-09-25-batch1241-t2e/report.md` (LIVE-SHAPE sections).
2. **#1243 / #1244:** through-code + red proof RED at base / GREEN at head in the tester's own clone.
3. **#1248:** re-run L3's tamper matrix itself, **T-2 FIRST** (loosen the continuation filter to accept any argument) and expect W8 to go red. **If W8 does
   not go red, the fixture did not survive and the matrix is unread → NO GO.** L3's disclosed limit (a continuation passed by NAME reads `false`,
   under-reporting in the safe direction) stays OUT of scope; grade that it is DISCLOSED. The packages/shared suite: `vitest run` in packages/shared (vitest
   resolves only from the workspace root: `npm ci` inside the member exits 127 — an environment fact, not this PR's).
4. Per-PR GO / NO GO / GO WITH FINDINGS, findings-only; worktrees from refs/pull/<n>/head; never write the shared checkout.
5. The fleet STOP count (pre_push_hook_base 28/0, fixture_guard 6/0, shell suites 60/60) — no standalone runs. (#1243/#1244/#1245 pushed format-gate only;
   #1248's push ran the preflight — the count is READ from its push log.)
6. Package suite `systemTest/performance` via `vitest run --config vitest.unit.config.ts --no-file-parallelism` (the one pre-existing PRESUITE-URLPATH red
   is not these PRs'); reap only own processes by cwd+ppid.
7. HOLDS: no merge/push/ticket/PR write/deploy. No DB/Docker needed.
8. GO string `GO: merge #1243, #1244, #1245, #1248 batch` (or the subset). MERGE ADDENDUM per PR (subject ≤ 92 chars, own keys only, equality targets,
   SHIPS-WITH).
9. Base-invariant checks over the CURRENT develop (re-read; it was `6e2a00bfed57…` at commission, `14cc526d10ee…` (#1246) at 14:13Z, and
   `77c6426b96d9…` (#1247, a comment-only `.githooks/pre-push` change) at 14:21Z — the kit is pinned to the last). Measure PAIRWISE path-disjointness and
   declare any overlap with its merged-blob target.
10. Routing `QA/Secuura-batch1243` — PROPOSED line `QA/Secuura-batch1243|coagent@agentmail.to|yes`, NOT written by the drafter.

## LEGITIMATE SHAPES (BRIEF_TEMPLATE §2a) — three of the four PRs change a CHECKER
Predicted-by = drafter. "port" = a Python/JS copy of the reader (a READ instrument, never evidence); "live" = the drafter's own real vitest 4.1.11 run
(drafter_liveshape_g24a.sh, liveshape_2.out) read through a LIFTED copy of the head's `readSuiteCounts` (liveshape_lift_2.out). The gate MEASURES every row.

### #1245 `readSuiteCounts` (a checker of vitest's own output)
| shape (piped, `--reporter=default`) | the real `Tests` line (drafter's live capture) | correct | head, predicted |
|---|---|---|---|
| fail-only | `      Tests  1 failed (1)` | {0,1} | {0,1} (live) |
| skip-only | `      Tests  1 skipped (1)` | {0,0} | {0,0} (live) |
| todo-only | `      Tests  1 todo (1)` | {0,0} | {0,0} (live) |
| expected-fail+pass | `      Tests  1 passed \| 1 expected fail (2)` | {1,0} | {1,0} (live) |
| fail+pass+skip | `      Tests  1 failed \| 1 passed \| 1 skipped (3)` | {1,1} | {1,1} (live) |
| pass-only | `      Tests  1 passed (1)` | {1,0} | {1,0} (live) |
| multi-file | ` Test Files  1 failed \| 1 passed (2)` / `      Tests  1 failed \| 1 passed \| 1 skipped (3)` | {1,1} | {1,1} (live) |
| all-failed / every label / orientation | `3 failed (3)` / `2 failed \| 2 passed \| 1 expected fail \| 2 skipped \| 1 todo (8)` / `2 failed \| 3 passed (5)` | {0,3} / {2,2} / {3,2} | correct (live) |
| beforeAll throws | ` Test Files  1 failed (1)` / `      Tests  2 skipped (2)` | {0,0} | {0,0} (live; the caller must not read {0,0} as green) |
| ctx.skip() / unexpected pass of it.fails | `1 passed \| 1 skipped (2)` / `1 failed \| 1 passed (2)` | {1,0} / {1,1} | correct (live) |
| no tests / import error | `      Tests  no tests` | none (refuse) | NULL → loud throw (live) |
| lookalike on STDOUT (console.log) | stdout: `Tests  5 passed (5)` … then the real `1 failed \| 1 passed (2)` | {1,1} | {1,1} (live) |
| **lookalike on STDERR (console.error)** | stdout: real `1 failed \| 1 passed (2)`; stderr: `      Tests  5 passed (5)` | {1,1} | **{5,0} — WRONG, silent (live)** |
| **failing string diff, no console at all** | stdout: real `1 failed \| 1 passed (2)`; stderr diff context: `        Tests  9 passed (9)` | {1,1} | **{9,0} — WRONG, silent (live)** |

### #1243 `parserImportSites` (a checker of source text)
| shape | expected | head, predicted (port) |
|---|---|---|
| the six EVASIVE_IMPORTS rows | 1 hit each | 1 each |
| the three NON_HITS | 0 | 0 |
| multi-line `import {\n load,\n} from 'js-yaml'` / multi-line re-export / split `from` | 1 hit | **0 — evades** |
| `createRequire(import.meta.url)('js-yaml')` | 1 hit | **0 — evades** |
| `import type { … } from 'js-yaml'` | 0 (no runtime load) | 1 (safe direction) |
| subpath `'js-yaml/dist/js-yaml.mjs'` | 1 | 1 |

### #1244 `formatDockerArgsForLog` (a guard on the echo)
| argv | expected | BASE (port) | head (port) |
|---|---|---|---|
| seat rows L02, L03, L08 | masked | clear | masked |
| Q1 `-Pe N=V`, Q2 `-diteN=V`, the accident cell | masked | masked | masked |
| `-l ADMIN_PASSWORD=V` (declared boundary) | clear | clear | clear |
| **unrowed L01 / L04 / L05 / L07 with a SECRET name** | masked | **clear** | masked (no row pins it) |
| control L06 `--label -one -e ADMIN_PASSWORD=V` | masked | masked | masked |

### #1248 LEG F `routerParserAnalysis` (a checker of router source) — READ only; the gate measures through `routerParserSites()`
| wrapper body | expected `guarded` | head, predicted |
|---|---|---|
| `raw(req, res, () => g(req, res, next))` (W2/W3 shape) | true | true |
| `g(req, res, () => raw(req, res, next))` (W7) | false | false |
| `raw(req, res, pick(g(req, res, next)))` (W8) | false | false (the loose T-2 filter reads true) |
| `raw(req, res, afterParse)` — named continuation | true in reality | false — DISCLOSED, out of scope |
| `raw(req, res, () => { const later = () => g(…); next(); })` | false (g never runs) | **true — over-reports** (pre-existing at develop) |
