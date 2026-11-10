GATE B1431-ci: GO WITH FINDINGS @ c79e2e8 on main 849b808

Branch `b1431/nexusai-t-ci-actions-browser-assert` head `c79e2e88f950689f16d17c860616a89b5a3dd7b8`, main `849b808c567e4d31d78e2d50b582540ae1920c67`. Gated 2026-11-10/11 by a re-commissioned gate. Every fact below was re-measured in the gate's own clone; the earlier agent's drafts were read only.

## Findings
| # | Sev | Finding | Evidence |
|---|---|---|---|
| F1 | Minor | RD-605 is only partly closed. `deploy-demo.yml:58` still pins `actions/checkout@v4` (Node 20) because the kit fences that file out (HELD as NEEDS-SHARED). `deploy.yml:92` `actions/upload-artifact@v4` is also a Node 20 action and is left as is. So the deprecation annotation stays on those two workflows. | grep at head; v4 manifest `using: node20` (read over git) |
| F2 | Minor | RD-544 gave three options. The builder chose "assert, install nothing" over installing Playwright Chromium, and flagged that choice for the coordinator. It is a reasonable call (the guard prefers bundled Chromium; the 66 rd490 cells were measured on what the runner has) but it is unruled. | STATUS "Choice for RD-544"; rd490 has 66 cells (measured in the main jest JSON) |
| F3 | Minor | Hosted behaviour is unproven: `checkout@v7`, `setup-node@v7` and the new assert step have not run on an ubuntu runner. The PR's own Build (pull_request runs the PR head's workflow) is the proof. Supporting facts: the v7 tags exist on actions/checkout and actions/setup-node (git ls-remote; v8 absent as a control); the v7 manifests read `using: node24` (v4: node20); every input used (node-version, cache, fetch-depth) is declared in the v7 action.yml; `gitleaks.yml` on main already uses `checkout@v7`. | git fetch of the action tags into a scratch bare repo |

No Blocker and no Major.

## Landing facts
- Landing form: head-pinned MERGE commit. A counts commit is needed at landing: `scripts/verify-expected-counts.json` must read tests 5507 / suites 328 if main is still 849b808c (delta +14 / +2 over whatever main has then). Without it the PR Build reads `VERDICT: FAIL` on stale counts. The pin is then the sha of that counts commit.
- Deploy demo: YES, this merge starts a run. `deploy-demo.yml` at head (blob 597b3487, the same as main) is on push to main with paths-ignore `**.md`, `docs/**`, `tests/**`. This branch changes `.github/workflows/` (build, deploy, npm-audit, arm-ttk), `scripts/` and `__tests__/`, and none of those paths is ignored. Both jobs are gated: build `:53` and deploy `:91` each carry `vars.CI_DEPLOY_ENABLED == 'true'`, so with the variable unset they read skipped. The variable's value is NOT RUN (hosted). RELAYED: HISTORY.md at main, lines 10018, 10042 and 10066, records that the Deploy demo runs for the 11-06 to 11-09 merges read completed/skipped with both jobs skipped.

## Checks (each run here)
- Refs: ls-remote = c79e2e88. Base 3929b794: 1 ahead, 2 behind (HISTORY.md only).
- Partition: 7 of 7 inside OWNS-T. deploy-demo.yml is untouched (blob 597b3487 at head and at main). No file in the branch names CI_DEPLOY_ENABLED other than deploy-demo.yml (not changed). No path is shared with any other pushed lane branch.
- Merge: merge-tree rc 0, tree 713d816e331e, equal to main plus the head's 7 blobs.
- CI full suite: merge 5507/328, 0 failed, success true. VERDICT FAIL only on the counts clause (5493/326 to 5507/328). Names +14 (rd544 7, rd605 7), -0. Failing suites at the merge minus main: none. Main PASS 5493/326.
- `node -c` x3 rc 0 at the merge. assert-browser.js parses. A real run on this Mac prints `assert-browser: OK - Playwright's bundled Chromium 151.0.7922.34`, rc 0.
- Red without the fix (main plus the two test files): 11 of 14 failed (rd544 7 of 7; rd605 4: arm-ttk, build, deploy, npm-audit). Head: 0 of 14.
- Source check of the doc claims: the guard's `launchBrowser` is at `tests/e2e/open-access-banner-guard.js:106`. It tries Playwright's bundled Chromium (`:109`) and then channel chrome (`:110`), and is exported at `:365-367`. assert-browser only requires that file (lane F's; it is read, not changed). The "66 cells" claim is true.
- Scans (270 added lines plus the message): names 0, secrets 0, GUIDs 0, hosts 0, Cf 0, B-number 0. CodeQL pre-scan 0: one `spawnSync(process.execPath, ['--require', preload, SCRIPT])` with a fixed argv. gitleaks dir over the merge extract 0, git over the commit 0.
- Claims: base reds rd544 7/7 and rd605 4/7, true. "v4 node20, v7 node24", true (read over git). COUNTS NEEDED 5507/328, true (the 11:25 PUSHED line saying 5520 is swapped, already corrected). Plants: not shown to me.
- Tier: config/CI, so G2. No security-shaped issue found.

## NOT RUN
- Hosted CI on a runner (Build, gitleaks, npm-audit, arm-ttk), hosted CodeQL, and the repository variable CI_DEPLOY_ENABLED: the standard fences out HTTP to hosted hosts, so none of these was read. Hosted CI and CodeQL on the PR are the proof.
- Open-PR overlap through the API: NOT RUN (no HTTP). Proxy over git: `git ls-remote origin 'refs/pull/*/head'` lists no PR ref at any of the four heads.
- npm ci and npm audit: not needed (package.json and package-lock.json are unchanged; blob 2d7dbece at main and head). node_modules was linked from the builder's install of the same lockfile.
- Load: the commission asks for load1 < 7. Other sessions held load1 at 11 to 25 for most of the window. The chain waited up to 10 minutes for load1 < 6 before each step, then went ahead. Each step ran 2 workers. Every run that loaded the machine went through the jest lock (tag qa-b1431-gate, held 22:36 to 01:22 AEDT).

Evidence (scratch): logs and raw jest JSON under /private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/90f78cba-aa68-4adc-98aa-7d2087ff2f7f/scratchpad/{logs,raw,b1431gate}.
