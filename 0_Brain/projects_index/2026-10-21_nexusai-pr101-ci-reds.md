# NexusAI PR #101 CI reds (rd490, rd545): caused by #101 or a runner race?

Measured 2026-10-21 by a read-only sub-agent for Tuesday. Repo datasecau/Reporting_Dashboard_Au, PR #101 head 48a17df83847c87d47625611eb3775be259b5362, Build run 39475920383.

## BLUF: UNDETERMINED, leaning ENVIRONMENTAL (no code path from #101 to either suite)

Decisive evidence in one sentence: no Build run in the last 40 that I could read (39 others, logs all available) failed rd490 or rd545, so a pre-existing flake is NOT shown on any tree without #101's change; but #101 changes no file that either suite imports, a run on a tree holding both of #101's own commits (6e947f4d, run 39451104717) passed both suites, and the failing log itself shows the GitHub runner agent (`Runner.Listener`) opening a connection to a test port, which is a runner-side cause the code cannot produce.

What this does and does not prove:
- It does NOT prove a flake: the failing run is the only red in 40 for these two suites (0 of 39 elsewhere, positive control below), and no run exists on the exact tree (main 115a775 + #101) other than the failing one.
- It does NOT support CAUSED-BY-101 either: there is no import path and the partial-#101 tree is green. The one untested difference between the green 6e947f4d tree and the red 48a17df8 tree is the merge of main 115a775 (PR #97); main 115a775 itself is green (run 39463981616).
- The cheapest discriminator is a re-run of run 39475920383 (fenced for me; Tuesday's call). Green on re-run = environmental. Red again on rd490/rd545 = look at the PR #97 + #101 combination.

## 1. Run matrix (last 40 Build runs, workflow id 201870215)

MEASURED: `gh api repos/datasecau/Reporting_Dashboard_Au/actions/workflows/201870215/runs?per_page=40`, then per run `.../runs/<id>/jobs` and `.../jobs/<jobid>/logs` (`--allow-escape-sequences`), grepped with `grep -ai 'FAIL __tests__/rd490'` etc. Logs saved under the session scratchpad (`.../scratchpad/logs/<runid>.txt`, matrix at `.../scratchpad/matrix.tsv`). Containment MEASURED with `gh api repos/.../compare/<sha>...<run head>` against #101's commits a7e8f4f9 (RD-874) and 6e947f4d (RD-875); `ahead`/`identical` = tree contains it.

Columns: F = "FAIL" lines for the suite, P = "PASS" lines. All 40 logs were available (40 of 40).

| Run | Head | Branch | Event | Conclusion | Has #101 commits | rd490 | rd545 |
|---|---|---|---|---|---|---|---|
| 39475920383 | 48a17df8 | rd-874-875-test-guards-uat-port-r11 | pull_request | **failure** | YES (both + merge of main 115a775) | FAIL x2 (summary replay) | FAIL x2 |
| 39471840864 | 6dcbedb9 | records/b362 | pull_request | success | no (diverged) | PASS | PASS |
| 39463981616 | 115a775b | main | push | success | no (main, base of the merge) | PASS | PASS |
| 39451104717 | 6e947f4d | rd-874-875-test-guards-uat-port-r11 | pull_request | success | YES (a7e8f4f9 + 6e947f4d, no merge of 115a775) | PASS (142 s) | PASS (60.6 s) |
| 39424860394 | 115a775b | rd-774-risk-sql-templates-s101o | pull_request | success | no | PASS | PASS |
| 39413796277 | d463f881 | main | push | success | no | PASS | PASS |
| 39405991180 | d463f881 | b302/test-code-codeql | pull_request | success | no | PASS | PASS |
| 39377850428 | aa811cf2 | main | push | success | no | PASS | PASS |
| 39374356715 | aa811cf2 | rd-863-group-nouns-s101o | pull_request | success | no | PASS | PASS |
| 39374343264 | e80920c2 | b302/test-code-codeql | pull_request | success | no | PASS | PASS |
| 39365783738 | 1bc9e9df | main | push | success | no | PASS | PASS |
| 39361889233 | f3ac8126 | s101o-history-1020 | pull_request | success | no | PASS | PASS |
| 39358275967 | 172d321f | rd-863-group-nouns-s101o | pull_request | success | no | PASS | PASS |
| 39350415926 | 278afc25 | rd-774-risk-sql-templates-s101o | pull_request | success | no | PASS | PASS |
| 39347822645 | 49ba21e1 | b302/test-code-codeql | pull_request | success | no | PASS | PASS |
| 39347056766 | 8bb6c339 | b302/test-code-codeql | pull_request | success | no | PASS | PASS |
| 39335567270 | f1a2e762 | rd-774-risk-sql-templates-s101o | pull_request | success | no | PASS | PASS |
| 39314064709 | 39653db4 | main | push | success | no | PASS | PASS |
| 39307052689 | 39653db4 | rd-460-c170-turn-s101o | pull_request | success | no | PASS | PASS |
| 39284925043 | 29c5ee8f | main | push | success | no | PASS | PASS |
| 39275343508 | 29c5ee8f | rd-476-assistant-prompt-s101o | pull_request | success | no | PASS | PASS |
| 39252102321 | 79af19c0 | main | push | success | no | PASS | PASS |
| 39244905395 | 79af19c0 | rd-857-whole-word-skip-list-s101o | pull_request | success | no | PASS | PASS |
| 39228590569 | ac0f4773 | main | push | success | no | PASS | PASS |
| 39223120979 | ac0f4773 | rd-856-user-pattern-verb-guard-s101o | pull_request | success | no | PASS | PASS |
| 39200012583 | 4c9b0d36 | rd-774-risk-sql-templates-s101o | pull_request | success | no | PASS | PASS |
| 39186366845 | 360cd824 | rd-774-risk-sql-templates-s101o | pull_request | success | no | PASS | PASS |
| 39178705493 | 7700cafd | main | push | success | no | PASS | PASS |
| 39174675387 | 7700cafd | rd-778-xss-through-dom-s101o | pull_request | success | no | PASS | PASS |
| 39158268796 | f15217cb | rd-460-c170-turn-s101o | pull_request | success | no | PASS | PASS |
| 39151101723 | fd8ff2ac | rd-460-c170-turn-s101o | pull_request | success | no | PASS | PASS |
| 39140954382 | 888203c8 | main | push | success | no | PASS | PASS |
| 39140683293 | 888203c8 | rd-794-ollama-runtime-slice-s89r | pull_request | success | no | PASS | PASS |
| 39130110359 | 5eb80a7a | main | push | success | no | PASS | PASS |
| 39129865212 | 5eb80a7a | rd-775-readiness-key-s92r | pull_request | success | no | PASS | PASS |
| 39123308458 | 2facd7c0 | rd-794-ollama-runtime-slice-s89r | pull_request | success | no | PASS | PASS |
| 39120374473 | 36a0dc0e | main | push | success | no | PASS | PASS |
| 39120080218 | 36a0dc0e | rd-761-law-endpoint-policy-s89r | pull_request | success | no | PASS | PASS |
| 39120041642 | f9649dcf | rd-476-assistant-prompt-s101o | pull_request | success | no | PASS | PASS |
| 39118735119 | 3047ae92 | rd-778-xss-through-dom-s101o | pull_request | success | no | PASS | PASS |

Reading the table:
- MEASURED: 39 of 39 other runs have zero `FAIL __tests__/rd490` and zero `FAIL __tests__/rd545` lines, and exactly one `PASS` line for each. Positive control: the same grep on run 39475920383 returns the FAIL lines for both (2 each; the second pair is jest's end-of-run summary replay of the same failure, same suite durations 59.467 s and 10.24 s, not a second failure).
- MEASURED: `RD-591] refused` (the foreign-connection line) appears in 2 lines in total across all 40 logs, both in the failing run. `Runner.Listener` appears once across all 40 logs, in the failing run.
- MEASURED: only 2 runs contain #101's commits: the failing one and 39451104717 (6e947f4d), which is green on both suites. No run is on a tree without #101's change and red on either suite, so the key fact asked for (a failure on a tree WITHOUT #101) is: NONE FOUND in this window.
- Caveat: 40 runs spans 2026-10-18 10:18Z to 2026-10-20 18:34Z, about 2.3 days. A rarer flake is not excluded. RD-844 records an earlier rd490 red on main on 2026-10-13 (different cause, see section 4), outside this window.
- Baseline EADDRINUSE: every green log has exactly 1 line matching `EADDRINUSE` (the suite's own descriptive text, checked in 39451104717: the grep with the sed-stripped line was empty in its own sample, so this 1-line baseline is a count only, its text UNMEASURED); the failing log has 133.

## 2. The failing log (run 39475920383)

Source: `/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-10-21_B362_evidence/build-pr101-h3-log.txt` (read, not re-fetched). Runner image ubuntu-24.04 20261018.339.1; command `npm run verify -- --maxWorkers=2` (build.yml:80), so two jest workers run suites concurrently.

### rd490 (EADDRINUSE on 38900)
- MEASURED: first `EADDRINUSE` at 18:50:39Z, repeated with the text "Could not listen on port 38900: EADDRINUSE. another process is already listening on it". The test's `beforeAll` calls `startServer('open')`, which claims the first port in 38900-38939 that `probe()` reports "refused", spawns the product server, and the server exits with code 1 (rd490 lines 158 and 211 in the stack). Because the failure is in the single `beforeAll`, EVERY cell reports "server open exited with code 1". It is one failure replayed per cell, not many independent failures. Grepping 389[0-3][0-9] in the log finds 38900 only; no other port in the band appears in any log line.
- MEASURED: suite order around it (jest completion lines; start times are not logged): rd395-ai-toggle-write PASS 18:50:30.6, rd490 FAIL 18:50:40.9 (10.24 s, so it started about 18:50:30.7), scim-provisioning PASS 18:50:43.0. In the same window, rd464-ai-readiness-service PASS 18:50:25.5, rd518-r3-health-detail-decision PASS 18:50:17.4, rd591-cross-seat-isolation PASS 18:50:16.0. With two workers, rd490 ran alongside exactly one other suite. Which suite that was is UNMEASURED (the log has no per-worker start lines). No other suite uses the 38900-38939 band (see section 3), so a concurrent suite is not shown to be the holder of 38900.
- UNMEASURED: WHO held 38900 at 18:50:39Z. The log never names the holder (the product server's EADDRINUSE line has no pid). What is measured is the surrounding fact in the next bullets.
- INFERENCE (not measured): 38900 lies inside Linux's ephemeral port range (32768-60999). Any process on the runner making an outbound connection can be handed 38900 as its local source port between rd490's "refused" probe and the child server's bind. RD-573 (To Do since 2026-09-19) names exactly this root cause for the 39000+ bands and was never fixed; the rd490 band 38900-38939 is in the same range.

### rd545 A4
- MEASURED failing assertion (rd545 test line 367, `expect(capShape(SIGNED.cells.a4)).toEqual(CAP)`), at 18:50:04.7Z:
  ```
  A4 — a signed-in admin with AI off keeps the same cap: the 6th is refused 429 and reaches nothing
  -   "firstFiveEachReached": true,
  +   "firstFiveEachReached": false,
      "sixthConnections": 0,
      "sixthError": "Too many AI connection tests. Wait 10 minutes and retry.",
      "sixthRequests": 0,
      "statuses": Array [ "not-429", ...
  ```
  Only that one field differs. The 429 on the 6th call and zero connections/requests after it are correct. `firstFiveEachReached` is `run.slice(0,5).every(r => r.seen.requests >= 1)` (test line 302): at least one of the first five signed-in calls did not reach the model stand-in.
- MEASURED: the lines immediately before the assertion block, in the same suite output at 18:50:04.7082712Z:
  `[RD-591] refused a connection to 127.0.0.1:42881 from 10.1.1.145:39918: pid 1807 (/home/runner/actions-runner/cached/2.337.0/bin/Runner.Listener run) is not part of this test process tree (pid 2158).`
  (the stack points at `__tests__/helpers/test-server.js:366`, `guardServer`.) So the GitHub Actions runner agent itself connected to a port the rd545 stand-in was listening on, and the RD-591 guard destroyed the connection and logged it. This is the only `refused` line in 40 logs.
- INFERENCE (not measured): that destroyed foreign connection is what cost A4 one stand-in hit. The log shows the foreign connection and the failed field in the same suite's output, not a causal link. The pre-fix state (before guardServer destroyed it) is UNMEASURED.
- Suite order: rd545 FAIL 18:50:04.7 (59.467 s, started about 18:49:05), concurrently with rd395-ai-enabled-gate PASS 18:49:05, dark-ground-luminance PASS 18:49:45 (420.9 s), sustainability-kpis PASS 18:49:54.

## 3. Port allocators and #101's diff

MEASURED (raw reads of 48a17df8: `gh api -H 'Accept: application/vnd.github.raw' repos/.../contents/<path>?ref=48a17df8...`; also a full tarball of that tree).

- rd490 `claimPort` (test file lines 80-93): `PORT_BAND = { start: 38900, end: 38940 }` (line 55). It walks the band, adds each port to a module-level `used` Set BEFORE awaiting `probe(p)`, and returns the first port `probe` reports `'refused'`. It never binds the port itself; the product server child binds later. `used` is per jest worker module registry, so it protects only within one suite.
- `__tests__/helpers/test-server.js` `reservePort` / `workerBand` (lines 62-98, 136): `BAND_BASE = 39000`, `BAND_SIZE = 40`, slot by worktree and `JEST_WORKER_ID`. Its header comment (line 55) says "Slots start at 39000, clear of RD-490's 38900-38939 (C-61)", and rd591 pins `RD490_BAND = {38900, 38940}`.
- Answer: the two allocators' bands do NOT overlap (38900-38939 vs 39000 and up), so the two cannot hand out the same port. Neither allocator binds the port it hands out, so both leave a probe-to-bind gap, and both bands sit inside the Linux ephemeral range, which is exactly the gap an unrelated process can fall into.
- rd490 uses the shared helper only for `probe` (`require('./helpers/test-server')` line 47).

#101 (`gh api repos/.../pulls/101/files`, 3 commits: a7e8f4f9 RD-874, 6e947f4d RD-875, 48a17df8 merge of main 115a775) changes six files:
`__tests__/auth-gate-fail-closed.test.js` (+2), `__tests__/rd395-ai-enabled-unreadable-store.test.js` (+2), `__tests__/rd875-uat-run-target-and-port.test.js` (new, +103), `__tests__/scim-security-controls.test.js` (+2), `scripts/verify-expected-counts.json` (3 lines), `tests/uat-run.js` (+35 -12).

- MEASURED (grep of every `require(` in both suites): rd490 requires `fs, os, path, child_process, ./helpers/test-server, ../tests/e2e/open-access-banner-guard, ../tests/e2e/open-access-banner-concealments` (the guard requires only fs, path, @playwright/test; concealments requires fs, path). rd545 requires `crypto, fs, path, os, http, ./helpers/rd395-server-harness, ./helpers/test-server` (the harness requires child_process, crypto, fs, http, os, path, ./test-server and, lazily, backend/jsonStorage). None of the six changed files is among them. `tests/uat-run.js` is required only by the new rd875 test. Answer: NO changed file is imported by rd490 or rd545.
- MEASURED: `scripts/verify-expected-counts.json` is read by `scripts/verify-suite.sh` and by verify-suite-gate, jsdom-instrument-limits and python-normaliser-gate tests (grep of the tarball), not by rd490 or rd545.
- MEASURED: the new rd875 test opens no sockets in its code (port numbers appear only as option values to a built request-options function) and none of #101's files mention 389xx. It does add one suite to the run (279 to 280 suites), which can shift which suites share a worker window; that effect on scheduling is UNMEASURED and cannot be excluded.

## 4. Jira (GET only, credentials read in-process, never printed)

Searches via `/rest/api/3/search/jql` on the NexusAI site (JIRA_SITE, https:// prefixed):

| Query | Hits |
|---|---|
| positive control: `project = RD AND text ~ "banner"` | 50 (cap) |
| `text ~ "rd490"` | 5: RD-844, RD-833, RD-828, RD-719, RD-424 |
| `text ~ "rd545"` | 9: RD-598, RD-595, RD-591, RD-585, RD-583, RD-574, RD-545, RD-541, RD-516 |
| `text ~ "EADDRINUSE"` | 10: RD-696, RD-641, RD-591, RD-573, RD-571, RD-567, RD-533, RD-518, RD-491, RD-490 |

Relevant existing tickets:
- RD-573 (To Do, filed 2026-09-19): jest port bands (39000+) sit inside Linux's ephemeral range 32768-60999; 25 test files and 2 harnesses pass a reserved port to a child process, so the proof-to-use gap stays open on CI. Reproduced by the tester on an offline Linux kernel by holding a client socket inside the band. Recommends moving the base below 32768. Not fixed. It describes the 39000+ band; rd490's 38900-38939 is in the same range.
- RD-571 (Release Ready): CI red on main 1a9ada3, rd412 SMTP stand-ins `EADDRINUSE 127.0.0.1:39004`, "reservePort infers free". The same signature on a sibling port band, so an EADDRINUSE on CI from an unrelated holder has precedent in this repo.
- RD-844 (To Do, 2026-10-13): rd490 failed main's push Build 38340787055 when cdnjs was slow (page.goto timeouts on 127.0.0.1:38900 pages). Different cause (timeouts, not EADDRINUSE), but it records rd490 as an existing source of CI-only reds, and states "this is the only failure in the last 40 runs" at that time.
- RD-591 (Release Ready): the cross-seat isolation fix that introduced the foreign-connection guard (`[RD-591] refused ...`) seen in the rd545 log.
- No ticket tracks "rd545 A4 firstFiveEachReached" or the exact "rd490 EADDRINUSE on 38900" failure. UNMEASURED: whether closed tickets or comments (searched text covers summary and description by Jira's text index, which is the limit) mention them.

## 5. Facts by status

MEASURED: sections 1 to 4 above (each states its command or source).
RELAYED: the failing log's content was read from the seat's saved file rather than re-fetched; the failing run's metadata (head sha, conclusion) was re-fetched live and matches.
UNMEASURED: the holder of port 38900 at 18:50:39Z; which suite shared rd490's worker window; whether the runner agent's connection caused rd545 A4; whether the PR #97 plus #101 merge (rather than #101 alone) is what differs from green runs; any flake outside the 2.3-day window.

## Suggested next step (for Tuesday, not done by me)

Re-run run 39475920383 (a gh write, fenced for this agent). If both suites go green on the same sha, the reds are runner-side and RD-573 (move the bands below 32768, and bind-and-hold rather than probe) is the real fix; if either reds again at the same place, the merge of PR #97 with #101 needs a look. Either outcome settles UNDETERMINED.
