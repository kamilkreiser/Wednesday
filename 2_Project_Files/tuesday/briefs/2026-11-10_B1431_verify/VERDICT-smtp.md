GATE B1431-smtp: GO WITH FINDINGS @ 857843e on main 849b808

Branch `b1431/nexusai-t-smtp-route-cells-standalone` head `857843e439a3251ed0950287575bbd094bce715a`, main `849b808c567e4d31d78e2d50b582540ae1920c67`. Gated 2026-11-10/11 by a re-commissioned gate. Every fact below was re-measured in the gate's own clone; the earlier agent's drafts were read only.

## Findings
| # | Sev | Finding | Evidence |
|---|---|---|---|
| F1 | Minor | The new control adds `jest.setTimeout(300000)` and a 240 s spawnSync timeout per nested run. The kit's property 4 says no timer is added unless the ticket says so. This is a test timeout, not a product timer, and the ticket does not ask for it. In this window the file took seconds. | `__tests__/rd720-rd412-cells-pass-alone.test.js:23` and `runAlone` |
| F2 | Minor | The control enumerates titles with a regex that only matches `test('...')` at 4-space indent. A cell written `it(` or at another indent would escape the count cell. That is a gap in the guard, not a defect today: the 7 titles equal the 7 cells in rd412-smtp-route (measured, 7 assertion results in the main JSON). | source |

No Blocker and no Major.

## Landing facts
- Landing form: head-pinned MERGE commit. A counts commit is needed at landing: `scripts/verify-expected-counts.json` must read tests 5501 / suites 327 if main is still 849b808c (delta +8 / +1 over whatever main has then). Without it the PR Build reads `VERDICT: FAIL` on stale counts. The pin is then the sha of that counts commit.
- Deploy demo: YES, this merge starts a run. `deploy-demo.yml` at head (blob 597b3487, the same as main) is on push to main with paths-ignore `**.md`, `docs/**`, `tests/**`. This branch changes `__tests__/`, and none of those paths is ignored. Both jobs are gated: build `:53` and deploy `:91` each carry `vars.CI_DEPLOY_ENABLED == 'true'`, so with the variable unset they read skipped. The variable's value is NOT RUN (hosted). RELAYED: HISTORY.md at main, lines 10018, 10042 and 10066, records that the Deploy demo runs for the 11-06 to 11-09 merges read completed/skipped with both jobs skipped.

## Checks (each run here)
- Refs: ls-remote = 857843e4. Base 849b808c (current main): 1 ahead, 0 behind, so merge tree = head tree.
- Partition: 2 of 2 inside. `rd412-smtp-route.test.js` is covered by the ANSWER-1 row (STATUS `## OWNS-T ADDED`). The new `rd720-*` is a queue key absent from the base tree. No path is shared with any other pushed lane branch.
- Merge: merge-tree rc 0, tree cea44abc7ab5 = head tree = main plus the head's 2 blobs.
- CI full suite: merge 5501/327, 0 failed. VERDICT FAIL only on counts (to 5501/327). Names +8 (rd720), -0. Failing suites at the merge minus main: none.
- Red without the fix (main's rd412 plus the new rd720 control): 4 of 15 failed, exactly cells 2, 3, 4 and 6 alone. Head: 0 of 15 (rd412 7 plus rd720 8).
- Scans (73 added lines plus the message): names 0, secrets 0, GUIDs 0, hosts 0, Cf 0, B-number 0. CodeQL pre-scan: `escapeRe` is a hand escape whose class includes the backslash (`[.*+?^${}()|[\]\\\/]`), so it is not js/incomplete-sanitization. My automatic pattern missed this line because of the `[\]` inside the class; it was read by hand. Its output goes to jest `-t` as an argv string, not into `new RegExp`. spawnSync uses a fixed binary and an argv array. gitleaks 0.
- Claims: control red on exactly 2, 3, 4 and 6 at base, true. COUNTS NEEDED 5501, true.
- Tier: tests only, so G2.

## NOT RUN
- Hosted CI on a runner (Build, gitleaks, npm-audit, arm-ttk), hosted CodeQL, and the repository variable CI_DEPLOY_ENABLED: the standard fences out HTTP to hosted hosts, so none of these was read. Hosted CI and CodeQL on the PR are the proof.
- Open-PR overlap through the API: NOT RUN (no HTTP). Proxy over git: `git ls-remote origin 'refs/pull/*/head'` lists no PR ref at any of the four heads.
- npm ci and npm audit: not needed (package.json and package-lock.json are unchanged; blob 2d7dbece at main and head). node_modules was linked from the builder's install of the same lockfile.
- Load: the commission asks for load1 < 7. Other sessions held load1 at 11 to 25 for most of the window. The chain waited up to 10 minutes for load1 < 6 before each step, then went ahead. Each step ran 2 workers. Every run that loaded the machine went through the jest lock (tag qa-b1431-gate, held 22:36 to 01:22 AEDT).

Evidence (scratch): logs and raw jest JSON under /private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/90f78cba-aa68-4adc-98aa-7d2087ff2f7f/scratchpad/{logs,raw,b1431gate}.
