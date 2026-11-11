GATE B1525: GO WITH FINDINGS @ 344c30c on main a15fb98

Tier G2 (tests-only harness). One round. Gate clock 02:18-02:46 AEDT 2026-11-12. Nothing pushed, no PR, no Jira, no mail, no az, no hosted HTTP except `gh api -X GET`.
Landing: head-pinned MERGE COMMIT, never squash (see landing.txt). Findings are all Minor; none blocks.

## Instruments
- Refs: `gh api -X GET` branches/main = a15fb98c (unchanged since the kit); `matching-refs/heads/b1525` = ONE ref, = 344c30cc; open PRs 0; compare main...branch = ahead 2, behind 0.
- Own clone `.../fleet/state/s270/gate1525/clone` (push URL set invalid). Trees: t4 = main, t7 = head, w_g = mutation copy at head. Jest worktree slot computed with `sha256(realpath).readUInt32BE(0) % 19` and read back from the helper's own `worktreeSlot()`: **slot 5** for all three (band 23200-23839; control: t3 and t9 print 8, tA 15). Not slot 8 (parked) or 9 (builder). Band `lsof` was 0 listeners before and after every run. Port block 9800-9809 was not needed.
- All jest ran under `nexusai-lock.sh jest gate1525` (one acquisition, lock released), `env -u NODE_OPTIONS`, `--maxWorkers=2`.

## Findings table
| # | Sev | Finding | Evidence |
|---|---|---|---|
| 1 | Minor | Shape B has one environmental lever: the banner is a winston `info` line, so a `LOG_LEVEL` of warn or error in the ambient environment would hide it and every shared-harness boot would be refused with a message that blames a "foreign" server. No bootServer caller sets LOG_LEVEL; the CI workflows, verify-suite.sh and jest.config.js do not either (grep with positive control: `backend/logger.js` 1 hit). Hazard only for a developer shell with LOG_LEVEL exported. | `backend/logger.js:161`; grep counts in step 3 below |
| 2 | Minor | B2 uses `bootTimeoutMs: 120000` and its own timeout is 240000; a broken banner makes the cell wait about 2 minutes before failing (the builder's own plant P5 took 122 s). Cost only. | rd982 test, B2 |
| 3 | Minor | STATUS says the kit's "50 bootServer suites" is 46 by `grep -l bootServer __tests__/*.test.js`. Confirmed: 46 at main (control rd657 = 1), 47 at head (rd982 added). Three of the 46 define their own local `bootServer` (rd436, rd441, rd452) and are not touched by shape B. | grep counts |
| 4 | Minor | `NEXUSAI_TEST_BAND_WORKER=""` (empty) is treated as unset, a non-numeric value or 17 throws the RD-591 message naming the variable. Consistent in `workerBand`, `nestedJestEnv` and `bandWorkerLabel`; noted only. | probe, step 4 |
| 5 | Minor (disclosed by builder, confirmed) | macOS wildcard-beside-loopback residual: a foreign loopback-only listener can coexist with the child's banner and shape B cannot see it; band separation removes the one source seen. | harness comment, DESIGN 3 |

No Blocker, no Major.

## What was checked, by numbered ask
1. **Paths.** `git diff --name-only a15fb98c 344c30cc` = exactly the five OWNS paths (3 modified helpers/test, 1 added test, counts file); `backend/` or `static/` paths 0 (control 1 on a planted `backend/x`). Two commits, A 705171d3 (parent main) and K 344c30cc (counts only), no merge commit. Census: no open PR; the other `heads/b1*` refs were not re-walked beyond the open-PR and single-b1525-ref checks.
2. **rd720 titles.** The base and head files differ only by the `require`, three comment lines and the `env` option (`diff` printed 4 hunks). The TITLES arrays are `cmp`-identical, and the JSON run of rd720 on main and on head prints the same 8 test titles, `cmp` byte-identical (8 lines each), 8/8 pass on both.
3. **Shape B cannot refuse a genuine boot (read at source).** The banner `Printer Dashboard API running on port ${PORT}` is logged by `logger.info` inside the listen callback (`backend/server.js:22346`) after a successful listen. `backend/logger.js` always attaches a Console transport (not conditional on NODE_ENV: comment at `:185-192`), so NODE_ENV (production, staging, development, test) cannot suppress it; redaction (`redactString`) only touches header lines, Bearer and JWT shapes, so the banner passes. The harness spawns every child as `node [-r preload] backend/server.js` with `stdio: ['ignore','pipe','pipe']` and appends both streams to `h.output`: stdout IS captured, and the entry point is always `backend/server.js` (no other entry). Callers: `grep -l bootServer __tests__/*.test.js` = 46 at main (control 1), 3 define their own local function (rd436, rd441, rd452, unaffected), the rest use the shared harness. Preloads that touch listening are the never-listens and accepts-never-answers family (rd619, rd629, rd648): they never produce a 200, so the gate is not reached and their expected failures read as before. Other preloads only `console.log` extra lines. `LOG_LEVEL` is the only lever and no caller sets it (finding 1). `PORT` overrides by a caller would already break `h.base`. Empirical backstop: all 52 files in the family (46 bootServer suites, rd720, rd573, rd591, boot-probe-log-redaction, rd982, plus rd554 via the verify) read PASS in the full verify below (control: rd657 PASS line counted 1). Answer: no bootServer caller boots a server whose output would lack `running on port <port>`; the one thing that would is an ambient LOG_LEVEL of warn or error.
4. **Shape A cannot collide.** Plain-node probe on t7 (no listen): worker 1 = 23200-23239, worker 2 = 23240-23279, override 16 = 23800-23839 (slot start + 600), so band 16 is outside both verify workers. `nestedJestEnv()` throws from worker 16 and when the variable is already set (nested twice), both with RD-982 text; override 17 and "abc" throw RD-591 naming the variable. `verify-suite.sh` refuses a run with no `--maxWorkers` and CI runs `--maxWorkers=2` (`build.yml:93`), so real workers are 1 and 2. rd720 is the only suite that spawns jest (grep of `__tests__/*.test.js`), so no second nested caller exists today.
5. **Re-runs and plants.** New file alone on main (untracked copy): 3 of 3 runs `B1 red, A1 red, A2 red, B2 green` (received B1 `accepted: true`); on head 4 runs 4/4 green; pairs on main 6 + 6 overlap runs (all `OVERLAP=true` by JSON start and end) all green; pairs on head 6 + 6 all green, 0 `EADDRINUSE` in every log. Plants P1-P4 by exact-match-count script (count 1 each), run once each, restored by copy, porcelain 0 after each and at the end:
   | plant | predicted | received |
   |---|---|---|
   | P0 none | 4/4 | 4/4 (and again after the plants) |
   | P1 workerBand ignores override | A1 | A1 only |
   | P2 gate replaced by true | B1 | B1 only |
   | P3 rd720 env line removed | A2 | A2 only |
   | P4 nested band 1 | A1 | A1 only |
   Each of the four cells is red under at least one plant except B2 (the control), which is green under all four by design; the builder's extra plant P5 covers B2 and was not re-run.
6. **Full verify on the head tree** (t7, plain, `npm run verify -- --maxWorkers=2`, 02:23-02:44): `VERDICT: PASS — 5585/5585 tests passed across 338 suites (jest exit 0)`, rc 0, `EADDRINUSE` 0, band empty after, porcelain 0. Committed counts at head = 5585/338 = measured (plain verify fails on a mismatch either way).
7. **0 of 20 on main (builder) plus 0 of 12 (mine).** What it proves: this machine, under these conditions, did not reproduce the failure in 32 overlapping paired runs (95 percent upper bound about 9 percent per run, rule of three), and that the fix does not make the pairs worse. What it does not prove: that the old code is safe (the cause needs rd720's nested boot and the victim's reservePort to land within the same short window AND the victim to sit in worker 1, which the JSON does not show), nor that the fix works; the fix is proved only by the red-on-main cells and the mutation matrix, and hosted CI is the deciding run.

## Claims graded (builder STATUS)
| claim | grade |
|---|---|
| Main rate 0/10 and 0/10 | not contradicted (mine 0/6 and 0/6; true as measured, weak evidence) |
| Red-first: B1, A1, A2 red, B2 green, 3 of 3 | true (3 of 3 mine, same shape) |
| New cells 4/4 in 3 of 3; pairs 20 of 20 green | true (mine 4/4 in 4 of 4; pairs 12 of 12) |
| Mutations P0-P4 as predicted | true |
| Verify 5585/338, EADDRINUSE 0, both PASS | true for the head tree (mine) |
| rd720 8 titles unchanged | true (JSON titles byte-identical) |
| No backend or static path | true |
| 46 bootServer suites at base | true |
| Name, B-number, gitleaks, CodeQL-row scans 0 | true (re-run below) |

## Scans over the added lines (261) and both commit messages
Names (Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite; `(?<![A-Za-z])name(?![a-z])`, case-insensitive): 0 and 0, controls: a planted `_by_<name>_` fires for all nine, `kamera` does not. B-numbers, N124, seat ids: 0 (control B1525 fires). Non-ASCII bytes 0 (control 3), Cf characters 0 (control 1). Secrets, ids, hosts, urls 0. gitleaks stdin over the diff: no leaks (control AKIA-shaped string: 1). CodeQL pre-scan: `new RegExp(` 0, eval or `new Function` 0, `exec(`/shell/innerHTML 0, hand-escape `.replace(/[` in added lines 0 (the existing rd720 `escapeRe` is unchanged and escapes the backslash), banned test tokens 0, `child_process` use is `execFileSync(process.execPath, [array])` with a fixed script string, the only listening server is the B1 stand-in (wildcard on purpose, commented). Commit author and committer are the project's configured identity (a users.noreply address); trailers `Co-Authored-By: Claude Sonnet 5.5`.

## Deploy-demo
Merging to main pushes `__tests__/` and `scripts/` paths. `deploy-demo.yml` paths-ignore is `**.md`, `docs/**`, `tests/**`; `__tests__/` does not match `tests/**`, so the workflow WILL start on the merge. Its `build` and `deploy` jobs are both gated on `vars.CI_DEPLOY_ENABLED == 'true'`; `gh api -X GET .../actions/variables` returns total_count 0 at repo level (organisation or environment variables were not readable, so NOT proven for those). The branch does not touch `.github/` (diff vs main empty). Expected conclusion: jobs skipped, no deploy. `deploy.yml` is dispatch-only.

## NOT RUN
- Hosted Build (`npm run verify -- --maxWorkers=2`), CodeQL on the merge commit, gitleaks/npm-audit/arm-ttk hosted jobs, Linux: hosted CI is the proof. Whether hosted overlaps rd720 with a victim: unknown.
- Merge by `git merge-tree`: clean, tree ff2c11f2 = the head tree (the head descends from main, so main plus the head blobs). Only checked against local main a15fb98c = origin main as of 02:18.
- Plant P5 (B2) and the census of every other `heads/b1*` ref (builder's claim, not re-walked).
- No docker or database suite is involved.
