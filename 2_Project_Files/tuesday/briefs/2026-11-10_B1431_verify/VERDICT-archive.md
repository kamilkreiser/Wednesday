GATE B1431-archive: GO WITH FINDINGS @ 52df646 on main 849b808

Branch `b1431/nexusai-t-suites-pass-from-git-archive` head `52df646848a64d35bd434e0ee9c49682346531da`, main `849b808c567e4d31d78e2d50b582540ae1920c67`. Gated 2026-11-10/11 by a re-commissioned gate. Every fact below was re-measured in the gate's own clone; the earlier agent's drafts were read only.

## Findings
| # | Sev | Finding | Evidence |
|---|---|---|---|
| F1 | Minor | RD-731 is not fully closed by this merge. `rd503-r2-doc-claims-against-product` (lane B, RD-576) is untouched (NEEDS-SHARED), and its 10 cells stay red from an extract. Measured: K2 at the head shows 10 red, all in that suite. | k2 run |
| F2 | Minor | Off pointers in comments. The helper doc says "Fourteen suites"; the control file header says "Thirteen suites" (13 changed plus 1 held, so both are partly right). The rd731 header says the throw case is "a root that does not exist", but the cell injects a thrower through the `run` seam instead. | `__tests__/helpers/image-manifest.js` trackedFiles doc; `__tests__/rd731-tracked-files.test.js` header |
| F3 | Minor | In an extract, the fallback walk lists every file present, untracked ones included. It skips only `zz-rd<N>-probe*`, `.git` and a top-level `node_modules`. Another suite writing a transient untracked file during a parallel extract run could make it flaky. Checkout behaviour, which is what CI uses, is unchanged: it is exactly `git ls-files` (proved by a cell and by the full suite). | source; rd731 cell 1 green in a checkout |

No Blocker and no Major.

## Landing facts
- Landing form: head-pinned MERGE commit. A counts commit is needed at landing: `scripts/verify-expected-counts.json` must read tests 5497 / suites 327 if main is still 849b808c (delta +4 / +1 over whatever main has then). Without it the PR Build reads `VERDICT: FAIL` on stale counts. The pin is then the sha of that counts commit.
- Deploy demo: YES, this merge starts a run. `deploy-demo.yml` at head (blob 597b3487, the same as main) is on push to main with paths-ignore `**.md`, `docs/**`, `tests/**`. This branch changes `__tests__/`, and none of those paths is ignored. Both jobs are gated: build `:53` and deploy `:91` each carry `vars.CI_DEPLOY_ENABLED == 'true'`, so with the variable unset they read skipped. The variable's value is NOT RUN (hosted). RELAYED: HISTORY.md at main, lines 10018, 10042 and 10066, records that the Deploy demo runs for the 11-06 to 11-09 merges read completed/skipped with both jobs skipped.

## Checks (each run here)
- Refs: ls-remote = 52df6468. Base 849b808c: 1 ahead, 0 behind.
- Partition: 15 of 15 inside. 3 are in the OWNS-T block, 11 are ANSWER-1 rows, and `rd731-tracked-files` is +new. `rd503-r2-doc-claims-against-product` (lane B) and `fixtures/image-carrier-review.json` are not touched. No path is shared with any other pushed lane branch.
- Merge: merge-tree rc 0, tree 885480b77816 = head tree.
- CI full suite: merge 5497/327, 0 failed. VERDICT FAIL only on counts (to 5497/327). Names +4 (rd731), -0. Failing suites at the merge minus main: none. The changed security-guard suites (image-content-exposure, auth-gate-fail-closed, rd385, rd403, rd411, rd418, and the rest) are green in a checkout at the merge.
- Red without the fix: (a) main plus rd731-tracked-files, 4 of 4 failed (trackedFiles absent); (b) K2, a git-archive extract with no .git: at main the 14 ticket suites show 179 of 367 failed, in all 14 suites; at the head the same 14 plus rd731 show 10 of 371 failed, all in rd503-r2 (held). In a checkout at the head, 371/371 pass.
- Scans (164 added lines plus the message): names 0, secrets 0, GUIDs 0, hosts 0, Cf 0, B-number 0. CodeQL pre-scan 0: `execFileSync('git', [...])` with an argv array; no RegExp from a variable. gitleaks 0.
- Claims: K2 base 179 of 367 in 14 of 14 suites, true. Head 10 red, all rd503-r2, true. Checkout 371/371, true. COUNTS NEEDED 5497/327, true. The helper plants are not shown to me.
- Tier: tests only. The suites guard image content, but checkout behaviour is byte-for-byte the same command, so G2.

## NOT RUN
- Hosted CI on a runner (Build, gitleaks, npm-audit, arm-ttk), hosted CodeQL, and the repository variable CI_DEPLOY_ENABLED: the standard fences out HTTP to hosted hosts, so none of these was read. Hosted CI and CodeQL on the PR are the proof.
- Open-PR overlap through the API: NOT RUN (no HTTP). Proxy over git: `git ls-remote origin 'refs/pull/*/head'` lists no PR ref at any of the four heads.
- npm ci and npm audit: not needed (package.json and package-lock.json are unchanged; blob 2d7dbece at main and head). node_modules was linked from the builder's install of the same lockfile.
- Load: the commission asks for load1 < 7. Other sessions held load1 at 11 to 25 for most of the window. The chain waited up to 10 minutes for load1 < 6 before each step, then went ahead. Each step ran 2 workers. Every run that loaded the machine went through the jest lock (tag qa-b1431-gate, held 22:36 to 01:22 AEDT).

Evidence (scratch): logs and raw jest JSON under /private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/90f78cba-aa68-4adc-98aa-7d2087ff2f7f/scratchpad/{logs,raw,b1431gate}.
