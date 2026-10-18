PR #1570 (KS-1613 items 1+2) head 2355d1b6b9bcd977b574725b4849913af3cf501c: GO
PR #1572 (KS-1545 step 1) head 778a610bf0afeab8475f5cebb86e8312515487b2: GO WITH NOTE
SHA256/16: cc91eb9abeaa70f0

# Gate E1 (OPUS, tier 1, round 1 of 2): PR #1570 + PR #1572

Gate: Opus 5.5, findings only, nothing fixed. Own clone `/private/tmp/claude-501/e1-opus/repo` (git clone --shared from 2_Project_Files, origin = git@github.com:Secuura/Distributed_Secuura.git, fetched with that checkout's core.sshCommand plus `-o ServerAliveInterval=30`). Worktrees: wt-1570, wt-1572 (with a copied workspace install), wt-dev. The fable/ folder was not read. Every multi-step command ran as a script FILE (`/bin/bash /abs/script.sh`); the scripts are in `opus/evidence/scripts/`. No git write verb in !CODING, no push, no GitHub/Linear write, no Docker, no remote box, nothing deleted. No fixed port was needed: every server in the tests and in my probe listens on port 0 (the OS picks a free ephemeral port), so the lsof step had nothing to pick.

**Heads (ls-remote, re-read at the end):** refs/pull/1570/head = 2355d1b6b, refs/pull/1572/head = 778a610bf. Both match R's table. Both PRs are one commit on 1197ab38a.
**Live develop MOVED during the gate:** 833984fc9 at the start, **9251ae54d** at the end (#1569 and #1571 landed: originate anchorStateSync.ts and api-gateway verification.ts plus their tests). The merge prediction and the merged-tree api-gateway suite below were re-run on 9251ae54d.

## FOUND

### PR #1570 (preflight.sh step()). No defect found.
- NIT N1 `Blockchain/Dev/scripts/preflight/preflight.sh:231`: the new suffix echoes `$_hdr_tail` raw, so a header holding a newline, CR or ESC prints those bytes, and a `"` in the header makes the quoting look odd (`is "x"; touch …; echo ""`). Nothing runs: `$()`, backticks, `${VAR}`, `\n`, `\c`, `%s%n` and `-n -e` all print literally, and a canary `touch` never fired. Line 228 on develop already echoes the whole `"$1"` raw, so this is not a new kind of exposure. The headers are literals in preflight.sh itself, so whoever can write one can already run any code. No action needed.
- NIT N2 (a test gap that another suite covers): mutant PM4 (`_hdr_tail="${1##*/}"`, greedy, cuts at the last slash) passes all 12 ks1547 cells. No cell has a slash in the title. But it makes 7 of the 16 real leg headers abort (legs 3, 8, 10, 12, 13, 15 and 16 have a `/` in their titles), and `preflight_deps.test.sh` kills it. So it is caught. A future cell such as `3/16  a/b` would pin it in the suite that owns step().

### PR #1572 (platform.ts audit-log route)
- **MINOR M1 (the NOTE) `Blockchain/Dev/services/api-gateway/src/routes/platform.ts:421-423`: some ways the route drops the platform half still log nothing.** The warn sits only in the catch (`:435`), so it fires only when something THROWS. My probe sent four upstream replies that empty the platform half without a throw, and each one gave HTTP 200 with the audit_logs rows only and **no log line**, on develop and on the PR alike:
  - an HTTP 500 reply with a JSON body;
  - an HTTP 401 `{"success":false,"error":"No token provided"}` on the first window (the H13 class);
  - a first window whose body is not a list;
  - a JSON `null` body.

  `r.ok` is never checked, and a first window with no list is treated as an empty list. So the KS-1545 aim ("an operator could not tell an audit log with no platform entries from one whose platform half was dropped") is met for connection refusals, timeouts, bodies that are not JSON and a later window that is not a list. It is not met for an upstream that answers with an error status. This is not a regression: nothing changes and nothing was logged before either. It is a gap in step 1's coverage that should be named on the card or in step 2.
- NIT N3 `platform.ts:435`: the `error` text is `err.message`, and two of the sources carry upstream content.
  - When the body is not JSON, V8's SyntaxError message quotes the start of the upstream body. A body of 20 characters or fewer is quoted whole (probe: `Unexpected token 'o', "tok=SECRETabc" is not valid JSON`). A longer one is cut to its first 10 characters (`"Bearer eyJ"...`).
  - The timeout text carries the internal upstream URL with `?limit=&offset=` (`Upstream timed out after 400ms: http://127.0.0.1:<port>/api/audit-log?limit=50&offset=0`).

  Everything else is bounded and safe. The caller's Authorization token (probe sent `Bearer CALLER-TOKEN-SECRET`), the request body, the platform rows (ids and a `ROW-SECRET` field) and `err.cause` appear in **no** log call in any of the 10 probe modes. The length is bounded by its sources (V8's ≤20-character excerpt, constant strings, the configured URL), though there is no explicit cap. This is the same expression as the KS-1510 precedent at `:1064`.
- Confirmed, no finding:
  - **No HTTP reply and no audit row changes.** Across 10 upstream modes the status, content type, full body and every SQL statement are byte-identical between develop and the PR. The route issues only the two SELECTs (COUNT and LIMIT) and writes no audit row.
  - `windowsRead` counts windows that were read in full. It is incremented after the push (`:426`) and before the break checks, so a second window that is not a list gives 1 and a refused first window gives 0.

## TESTED / HOW

### #1570
- **Diff by hunk (step 1):** 2 files only. preflight.sh has 1 hunk and 2 changed lines (225 and 231). The test file has 1 hunk with +28 lines. Both are mode 100644. `bash -n` passes on both, and `git diff --check` is clean. The two files are identical between develop 833984fc9, develop 9251ae54d and base, so the PR's versions land unchanged.
- **Red-first with /bin/bash 3.2.57:** the PR's test against develop's preflight.sh gives **10 ok / 2 FAIL** (exactly the two RED KS-1613 quote cells), rc=1. **Green** at the head: **12/12**, rc=0. Only /bin/bash exists on this machine, so the test's inner `bash` is 3.2 too.
- **Every preflight-related suite, before (develop) and after (PR head), with /bin/bash:** ks1547 6/6 → 12/12. preflight_deps 56/56, failure_verdict_keeps_ratio 8/8, gateway_slot 15/15, leg4_sweep_not_run 5/5, ratio_excludes_leg1_no_install 6/6, state_is_initialised 5/5 and verdict_names_real_failures 5/5 are the same before and after. test_types_ratchet_leg fails the same way before and after: 25/9 with no workspace install, and 33/5 with one, with develop's or the PR's preflight.sh swapped in. That failure is environmental and not caused by this PR.
- **Full shell-suite runner (run-shell-suites.sh, with the workspace install), before and after:** **88/90 both times**. The same 2 failures appear both times: ks949_main_seed_idempotence and preflight_test_types_ratchet_leg, both environmental. `--check-unreached`: all 90 suites are reached, rc=0 both times. I could not reproduce the author's 90/90 here; the difference is the environment, not the PR.
- **Every leg header in the tree (16 of 16 `step "N/16 …"` lines; TOTAL_LEGS=16):** each one goes through develop's step() and through the PR's step(), each built from that file's own lines. All 16 give rc=0 with no abort on both, and the output is the same.
- **Malformed headers (18):** `3/`, `3/x`, `3/x  Title`, `3`, empty, `/`, `/16`, `3/16x`, `3/1`, `3/017`, `3/016`, `3/ 16`, `3/-16`, `3/+16`, `3/16.0`, full-width `３/１６`, `3/16/16`, `3/16 /x`. The rc, whether it aborts, whether it returns and the `says /…` text are identical to develop for each one. The output differs only by the new suffix.
- **Injection payloads (13):** `$()`, backticks, a quote-break with `; touch`, `\n`, `\c`, `%s%n`, a real newline with a fake "PREFLIGHT PASSED" line, CR, ESC, `${TOTAL_LEGS}`, `$TOTAL_LEGS`, `${PATH}`, `-n -e`, and a 3000-character tail. All of them abort with rc=1 exactly as develop does. The canary file was absent afterwards. 47 of the 48 probes were byte-identical to develop apart from the suffix; the one exception was the real-newline case, where the suffix itself spans the newline (see N1).
- **Mutants (in place in the scratch worktree, restored after each, 0 files left changed):**
  - Product hunk: PM1 (suffix dropped), PM2 (`$_hdr_total` quoted), PM3 (`$1` quoted), PM5 (single `%`), PM6/N4 `[!1-9]`, PM7/N5 `[[:space:]:]`, PM8/N7 numeric `-ne` and PM9 (`${1%/*}`) are **all killed** by ks1547. Each of N4, N5 and N7 is killed by the cell written for it. PM4 (greedy `##`) is killed by preflight_deps only (N2).
  - Test hunk: TM1 (override set before the helpers) fails the 3/20 cell, and TM2 (wrong expected text) fails its cell. So the new cells are load-bearing.
  - **Comment-only controls** in the product (PC0) and in the test (TC0): 12/12, and every sibling suite is unchanged.

### #1572
- **Diff by hunk (step 1):** 2 files only. platform.ts has 2 hunks: `let windowsRead` at `:396`, and the increment at `:426` with the catch and warn at `:433-435`. The new test file adds 130 lines with mode 100644. +135/-1 in total. The PR's platform.ts equals develop's plus the PR's change, and develop and base are identical for this file.
- **All three sites read in full:** the route `:369-520`, `fetchWithTimeout` and `UpstreamTimeoutError` (`:132-176`), `authHeaders` (`:219`), the logger (winston: JSON in production, and no redaction, so the meta is printed exactly as passed).
- **Red-first:** the new test against develop's platform.ts gives **3 FAIL (W1, W2, W3) / 1 pass (the control)**. **Green:** 4/4, and **5 out of 5 repeated runs** passed (no flake seen).
- **api-gateway suite:** before (develop route, new test excluded) **120 files / 1166 tests pass**. After (PR head) **121 / 1170 pass**, with no new failures. On the **merged tree 6581d8d6db39** (develop 9251ae54d + #1570 + #1572, with every api-gateway/src file proven identical to that tree) it is **121 / 1174 pass**.
- **tsc:**
  - Product `tsc -p tsconfig.json --noEmit`: rc=0, 0 errors, both at the PR head and on the merged tree.
  - A program that INCLUDES the new test (`evidence/tsconfig.gate-e1.json`; `--listFilesOnly` confirms the file is in it): rc=0, 0 errors.
  - **Planted control** (`const x: number = "…"` added to the new test): rc=2 with TS2322 and TS6133, so the program really does check that file.
  - Leg 16's own ratchet (test-types-ratchet.sh services/api-gateway): 156 files, 121 of them under `__tests__`, 35 errors that are all in the baseline, **0 new**, both at the head and on the merged tree.
- **Probe** (`evidence/probe/gatee1-probe.test.ts`, run against the REAL createPlatformRoutes under develop's and the PR's platform.ts, then moved out of the tree): 10 upstream modes: ok, destroy, second-not-a-list, slow, http500-json, http401-json-first, nonjson-short, nonjson-long, null-json, first-not-a-list. It recorded the status, headers, full body, SQL list and every logger.{warn,error,info,debug} call. The results are summarised under FOUND, and the raw records are in `evidence/probe1572.{dev,pr}.json`.
- **Mutants (2 or more per site, restored after each, 0 files left changed):** all are **killed** by the new test.
  - Site 1: S1a (starts at 1), S1b (`const`, so the increment throws inside the try and the control catches it), S1c (shadowed inside the try).
  - Site 2: S2a (no increment), S2b (increment before the not-a-list check), S2c (`+= 2`).
  - Site 3: S3a (no warn), S3b (raw `err` object), S3c (no windowsRead), S3d (`logger.error`), S3e (context does not name the route), S3f (+stack, killed by W1 and W2), S3g (also warns on success, killed by the control).
  - **Comment-only control** SC0: 4/4.
  - Moving the increment below the break checks is an equivalent mutant (a break never reaches the catch), so I left it out.

### Merge prediction (step 4), with `git merge-tree --write-tree` on git 2.51
- On develop **833984fc9**: #1570 alone and #1572 alone are both clean. Both orders are clean and land the same tree.
- On live develop **9251ae54d**: #1570 alone is clean (0149823585a1) and #1572 alone is clean (7c5ea9a807c6). **1570 then 1572 and 1572 then 1570 both give 6581d8d6db39**. That matches R's "6581d8d6db39" claim, now that #1569 and #1571 have landed.
- Overlap: #1570 ∩ #1572 = ∅. #1570 ∩ develop since base = ∅. #1572 ∩ develop since base = ∅. Each PR's files in the merged tree are blob-equal to the PR head's.
- **Planted conflicting control:** a develop-side commit that edits #1570's abort line and #1572's `catch {` line gives a CONFLICT in preflight.sh against #1570 and a CONFLICT in platform.ts against #1572 (rc=1 each). So the clean results above are real.

## NOT tested
- **Preflight legs 3, 4 and 8** (spec-auth conformance, path resolvability, served-spec consistency): they need the local stack, and there was no Docker. Legs 1, 2, 5-7 and 9-15 were not run end to end either; only step() itself and leg 16's ratchet script ran. I did not run a real `git push` through the hook.
- The ks949 and ratchet-leg shell-suite failures were not diagnosed. They are environmental and identical before and after.
- The production winston JSON transport and the file transports. The probe replaced the logger methods with spies, so what the transports actually write was not observed.
- I did not check the claim that "all four of R's PRs land the same tree". Only the two PRs here were merged; the other two are already on develop 9251ae54d, and the result is consistent with that tree.
- No BLOCKED steps (no permission dialog came up).

## Severities
| # | PR | Severity | file:line | Summary |
|---|---|---|---|---|
| M1 | #1572 | MINOR (the NOTE) | services/api-gateway/src/routes/platform.ts:421-423 (warn only at :435) | An upstream error status with a JSON body, or a first window that is not a list or is null, still drops the platform half with no log line. `r.ok` is not checked. Not a regression; name it in KS-1545 step 2 or on the card. |
| N3 | #1572 | NIT | services/api-gateway/src/routes/platform.ts:435 | The logged `error` can quote up to 20 characters of an upstream body that is not JSON, or the internal URL plus limit/offset on a timeout. No caller token, request body or rows are logged. |
| N1 | #1570 | NIT | scripts/preflight/preflight.sh:231 | The tail is echoed raw (control characters, quotes), with no execution. Line 228 on develop already does the same. |
| N2 | #1570 | NIT | scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh (no cell has a slash in the title) | The greedy `##*/` mutant survives ks1547 but is killed by preflight_deps and by the real headers. |

No BLOCKER or MAJOR on either PR.

WALL-CLOCK: 31
