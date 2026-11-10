GATE B1431-csp: GO WITH FINDINGS @ e6addce on main 849b808

Branch `b1431/nexusai-t-csp-tool-edge-cases` head `e6addceb8ee6b18127a7813fd62a2f6195a199b1`, main `849b808c567e4d31d78e2d50b582540ae1920c67`. Gated 2026-11-10/11 by a re-commissioned gate. Every fact below was re-measured in the gate's own clone; the earlier agent's drafts were read only.

## Findings
| # | Sev | Finding | Evidence |
|---|---|---|---|
| F1 | Minor | RD-970's recommendation ("a proposal, not decided") offered two options: treat ENOTDIR and EACCES-on-a-parent like ENOENT, or state in the header that only ENOENT is skipped. The branch takes a hybrid: ENOTDIR is skipped, EACCES still stops the run, and the header says so. That is a behaviour choice the ticket did not rule on. The tool is one-shot; the choice is documented at `scripts/refactor-inline-styles.js` header lines 8-9 and the readIfPresent comment. | the ticket excerpt in `tickets-by-lane.tsv` (RD-970), and the diff |

No Blocker and no Major.

## Landing facts
- Landing form: head-pinned MERGE commit. A counts commit is needed at landing: `scripts/verify-expected-counts.json` must read tests 5520 / suites 328 if main is still 849b808c (delta +27 / +2 over whatever main has then). Without it the PR Build reads `VERDICT: FAIL` on stale counts. The pin is then the sha of that counts commit.
- Deploy demo: YES, this merge starts a run. `deploy-demo.yml` at head (blob 597b3487, the same as main) is on push to main with paths-ignore `**.md`, `docs/**`, `tests/**`. This branch changes `scripts/` and `__tests__/`, and none of those paths is ignored. Both jobs are gated: build `:53` and deploy `:91` each carry `vars.CI_DEPLOY_ENABLED == 'true'`, so with the variable unset they read skipped. The variable's value is NOT RUN (hosted). RELAYED: HISTORY.md at main, lines 10018, 10042 and 10066, records that the Deploy demo runs for the 11-06 to 11-09 merges read completed/skipped with both jobs skipped.

## Checks (each run here)
- Refs: ls-remote = e6addceb (READY sha from STATUS). Main is 849b808c, which is 3929b794 plus HISTORY.md only. The branch base is 3929b794: 2 commits ahead, 2 behind.
- Partition (fnmatch program over the kit's OWNS-T block, plus the ANSWER-1 rows, plus `+new rd<N>` only for queue keys absent from tree 3929b794): 4 of 4 paths inside. Controls fired: server.js, the counts file, deploy-demo.yml and `rd999999-x` all read out; verify-suite.sh and the ANSWER-1 row file read in. No path is shared with any other pushed lane branch (12-branch program, see ORDER.md).
- Merge: `git merge-tree --write-tree main head` rc 0, tree b1bd1ed9f923, equal to main's tree with the head's 4 blobs written in (independent index build). The control merge, a1d7f46d, also built equal.
- CI, full suite (npm run verify --maxWorkers=2, non-dot scratch tree, under the lock): main PASS 5493/5493, 326 suites, 0 failed. Merge 5520/328, 0 failed, success true. Its only VERDICT FAIL is the counts clause (expected 5493/326, measured 5520/328), which landing regenerates. Names: +27 (rd970 5, rd971 22), -0. Suites added are exactly the two new files. Failing suites at the merge minus main: none.
- The syntax steps of build.yml (`node -c` on server.js, azureLogAnalytics.js, model-config.js) rc 0 at main and at the merge; csp-convert.py compiles.
- Red without the fix (main plus the two new test files, scripts at main): 12 of 27 failed, 2 in rd970 (the ENOTDIR cells) and 10 in rd971 (VT, FS, GS, RS, US, NEL, NBSP, EM SPACE, LS, IDEOGRAPHIC SPACE). Head: 0 of 27 failed.
- Probe: the main and head SCRIPT_BLOCK_RE, compiled from source, run over `<script>a()</script X>tail</script>` for 12 X. Tab, LF, FF, CR, space and `/` close at the first tag in both. VT, FS, NBSP, NEL and LS close at the first tag on main and at the real end tag on head. This matches the HTML script-data end-tag state.
- Scans over 271 added lines and the 2 commit messages: names 0 (11 names, underscore-aware; the planted `_by_<name>_` fired for all; `Kamera` does not fire), secrets 0, tenant or sub GUIDs 0, hosts 0, Cf 0, B-number or seat in messages 0. CodeQL pre-scan 0: the only spawns are `spawnSync(process.execPath, [fixed])` and `spawnSync('python3', ['-I', ...])`, with fixed argv and no template string. gitleaks: dir over a git-archive extract of the merge, 0 findings; git over the branch commits, 0; a planted-key control gave 1.
- Claims: rd970 2 of 5 and rd971 10 of 22 red at base, true. COUNTS NEEDED 5520/328, true (corrected under ANSWER-1; the 11:25 PUSHED line that says 5507 is false and already corrected in the STATUS Corrections). Plants and restore hashes are not shown to me (the builder's raw files were not re-run).
- Tier: lane T tooling and tests, so G2. No security-shaped issue found.

## NOT RUN
- Hosted CI on a runner (Build, gitleaks, npm-audit, arm-ttk), hosted CodeQL, and the repository variable CI_DEPLOY_ENABLED: the standard fences out HTTP to hosted hosts, so none of these was read. Hosted CI and CodeQL on the PR are the proof.
- Open-PR overlap through the API: NOT RUN (no HTTP). Proxy over git: `git ls-remote origin 'refs/pull/*/head'` lists no PR ref at any of the four heads.
- npm ci and npm audit: not needed (package.json and package-lock.json are unchanged; blob 2d7dbece at main and head). node_modules was linked from the builder's install of the same lockfile.
- Load: the commission asks for load1 < 7. Other sessions held load1 at 11 to 25 for most of the window. The chain waited up to 10 minutes for load1 < 6 before each step, then went ahead. Each step ran 2 workers. Every run that loaded the machine went through the jest lock (tag qa-b1431-gate, held 22:36 to 01:22 AEDT).

Evidence (scratch): logs and raw jest JSON under /private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/90f78cba-aa68-4adc-98aa-7d2087ff2f7f/scratchpad/{logs,raw,b1431gate}.
