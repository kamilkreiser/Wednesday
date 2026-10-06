# Spark brief: job 06 stderr to its own file. Screen report, 2026-10-07 00:2x AEDT

Written by a Spark brief-writer sub-agent for Wednesday. No model round was run. No PR, push, comment, ticket write or contact happened. The Secuura checkout was used with git read verbs only. Working trees were `git clone --shared` copies in the session scratchpad (`…/scratchpad/spark06/clone`, `clone2`).

## Brief

- **Dir:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1136-06-tenant-stderr-own-file/`
  - `KS-1136.md` (the brief)
  - `golden.diff`
  - `spark.pins`: `tier=bash_patch`, `ref=…/container_trivy_failed_scan_is_loud.test.sh`, `test_file=…/tenant_isolation_stderr_own_file.test.sh`
- **Product:** `Blockchain/Testing/jobs/06-tenant-isolation.sh`. One hunk, `@@ -69,5 +69,5 @@`. `:71` changes from `> "$OUT" 2>&1 || true` to `> "$OUT" 2> "$OUT.stderr" || true`. The blank lines `:70` and `:72` are each written as a `-`/`+` pair so that no context line is blank. Nothing else changes.
- **Test:** a new file, `Blockchain/Dev/scripts/__tests__/tenant_isolation_stderr_own_file.test.sh` (97 lines). It uses the same shape as the 04 trivy suite:
  - the job is copied into a temp `Testing/` tree;
  - `node`, `curl` and `tsx` are stubs on PATH;
  - the `tsx` stub prints runner.ts's `login failed for verifier@…` line on stderr, then JSON on stdout.
- **Cells:** 4 RED and 1 CONTROL.
  - RED: the fallback artefact parses (3 tested, 0 findings).
  - RED: the summary prints `tested=3 cross-tenant_findings=0`.
  - RED: the stderr is kept in `06-tenant-isolation.json.stderr`. A `2>/dev/null` "fix" stays red on this cell.
  - RED: a leak found on a fallback run stays readable (1 finding, `tenant-a`).
  - CONTROL: a run with no stderr parses at both the tip and the fix.
- **Measured by hand** in the scratch clone (bash 3.2.57, jq 1.7.1): at the tip `1 passed, 4 failed` rc 1; with the fix `5 passed, 0 failed` rc 0.
- **Tip:** `git ls-remote origin refs/heads/develop` gave `d75bfe2deb8075583cfb55af0921e4964e7c6f0e`. This is the expected SHA; **develop had not moved.**

## Dry-run (verbatim, rc 0)

```
round: brief /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1136-06-tenant-stderr-own-file/KS-1136.md · tier bash_patch · runner bash · pins: ref=Blockchain/Dev/scripts/__tests__/container_trivy_failed_scan_is_loud.test.sh test_file=Blockchain/Dev/scripts/__tests__/tenant_isolation_stderr_own_file.test.sh product=Blockchain/Testing/jobs/06-tenant-isolation.sh
round: endpoint: http://127.0.0.1:47788/v1/models 200
round: cache: fetching develop from origin (tip d75bfe2deb8075583cfb55af0921e4964e7c6f0e not yet local)
round: base: develop d75bfe2deb8075583cfb55af0921e4964e7c6f0e (git -C <Secuura checkout> ls-remote origin refs/heads/develop at 2026-10-07 00:15:53)
round: cache: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src at d75bfe2deb8075583cfb55af0921e4964e7c6f0e, 37 node_modules link(s) (excluded: services/billing)
round: run dir: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/state/dry/KS-1136-06-tenant-stderr-own-file_20261007-001606
round: input: wrote /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/state/dry/KS-1136-06-tenant-stderr-own-file_20261007-001606/input.json: Blockchain/Testing/jobs/06-tenant-isolation.sh (3041 B) + r
SPARK ROUND KS-1136-06-tenant-stderr-own-file: DRY-RUN OK — brief accepted, input built at d75bfe2deb80 (32667 B) in /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/state/dry/KS-1136-06-tenant-stderr-own-file_20261007-001606; a real round would call http://127.0.0.1:47788 with bash_patch/task.md, thinking OFF
```
Builder: `sites 3 (1 must_change); expected '+' 1; must_remove 1; new test Blockchain/Dev/scripts/__tests__/tenant_isolation_stderr_own_file.test.sh`

## Control (verbatim, rc 0)

```
SPARK ROUND KS-1136-06-tenant-stderr-own-file: CONTROL-PASS — PASS (checker rc 0 + A2a anchor OK) · golden BYTE-IDENTICAL · tip d75bfe2deb80 · 39s round, no model (control) · /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1136-06-tenant-stderr-own-file-control
```
Checker lines:
```
PASS B0 subject: clone at d75bfe2deb8075583cfb55af0921e4964e7c6f0e, Blockchain/Testing/jobs/06-tenant-isolation.sh and Blockchain/Dev/scripts/__tests__/container_trivy_failed_scan_is_loud.test.sh present
PASS B1 output is exactly one fenced ```diff block
PASS B2 every section applies at the tip (strict)
PASS B3 touched-file set == { Blockchain/Testing/jobs/06-tenant-isolation.sh , Blockchain/Dev/scripts/__tests__/tenant_isolation_stderr_own_file.test.sh (new) }
PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'
B4 run at the tip: rc=1 fail_lines=4 pass_lines=1 load_error=0 timeout=0
PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/tenant_isolation_stderr_own_file.test.sh fails at the untouched tip (rc=1, 4 FAIL line(s))
PASS B5a the script parses after the hunk (bash -n)
B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=5 load_error=0 timeout=0
PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/tenant_isolation_stderr_own_file.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 5 pass line(s))
PASS B6 sibling suite(s) that drive 06-tenant-isolation.sh: no NEW failure after (1 suite(s))
INFO B7 shellcheck not installed (informational)
RESULT: PASS (7/7)
PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=1)
SPARK RESULT: PASS (checker rc 0 + A2a anchor OK)
```
The B6 sibling is `orchestrate_jobs.test.sh`. It read `18 passed, 0 failed, 0 skipped` both before and after the fix.

**Queue:** both gates passed, so `KS-1136-06-tenant-stderr-own-file` was appended to `local-model/spark/queue.md`. `queue.sh` was NOT started. Before running, I checked that no round or queue process was live.

The harness wrote its own outputs as it always does:
- `spark/state/dry/KS-1136-06-tenant-stderr-own-file_20261007-001606/`
- `runs/spark_secuura_2026-10-07_KS-1136-06-tenant-stderr-own-file-control/`
- `spark/cache/work/…-control_001637/` (a per-round clone, about 335 MB; prune by hand, as the README says)
- a fetch of `d75bfe2` into `spark/cache/src`

## Ticket search (Secuura Linear, read-only)

Method: GraphQL queries only, no mutations. Each term was searched in team KS issue title and description (`containsIgnoreCase`) and in comment bodies. The key was read transiently from the Secuura `.env` and was never printed or stored. Scripts and output: `…/scratchpad/spark06/linear_search.py`, `.out`, `linear_get.py`, `.out`.

| term | hits |
|---|---|
| `06-tenant-isolation`, `06-tenant`, `tenant-isolation.sh` | KS-1382 (Todo). Its description names `06-tenant-isolation.sh:31` (TARGET_BASE defaults to slot 1). This is a different line and a different defect. |
| `runner.ts` | 0 |
| `login failed for` | 0 |
| `unparseable` | KS-1274, KS-1273, KS-1136, KS-940 (issues); comments on KS-763/593/565/256. None of them is about job 06's stderr. |
| `2>&1` | KS-1324, 1137, 1136, 1049, 973, 897 (+ comments on KS-1303/1049). None is about job 06. |
| `stderr` | 8 issues and 10 comment hits. None is about job 06. |
| `verifier@` | KS-525, and a comment on KS-972. Neither is about job 06. |
| `unreadable-artefact` | KS-1136 |
| `09-aggregate-report.sh` | KS-1136 (+ comments on KS-772/485/1136) |

**Positive control:** `unparseable`, `unreadable-artefact` and `09-aggregate-report.sh` all return KS-1136, the known ticket. The symbol term `06-tenant-isolation` returns KS-1382, which names this file. So the search does reach file-level mentions.

I also read the full text of KS-1136 and KS-1382 (description and all comments) for `06-tenant|tenant-isolation|2>&1|stderr|runner.ts`:
- KS-1136 mentions 06 only as the `:173` read in 09.
- KS-1382 mentions it only at `:31`.

**Verdict: no ticket exists for this defect.** The raise seat files it.

## Routing predicate: does it meet the Spark predicate? **Yes, on all four tests.**

1. **One product file.** `06-tenant-isolation.sh`, one hunk, one line's redirection.
2. **Fix spelled out.** Wednesday's Q2 ruling says "stderr to its own file". The brief gives the exact `+` line.
3. **Runnable in-process test nearby.** The new suite sits beside the 04 job suites in `Dev/scripts/__tests__/` and runs in about a second with stubs. CONTROL-PASS 7/7 confirms it.
4. **Not an auth/credential surface.**
   - My judgement: **no**, for these reasons. The job is a test harness that probes tenant isolation, so its subject is a security property, but the edit does not touch the probe. No login, credential, token, request, assertion or verdict logic changes. `runner.ts` is untouched. Only the destination of the runner's diagnostic stderr moves.
   - What the change does do for security: it *restores* the visibility of findings. Before the fix, a real leak on a fallback run was swallowed.
   - Residual consideration: the `.stderr` file will hold `login failed for verifier@secuura.com: 401 {body}`. That is the seeded test email plus the server's error body. No password is printed (`runner.ts:74` prints the email, status and body only). The file sits in the same run dir as the artefact, which the JSON already shared.
   - I state this for Wednesday's call. It is not a hold.

## UNMEASURED

- **No real runner and no stack.** The real `runner.ts`'s stderr/stdout split is read from `:74`, `:150`-`:151` and `:262`, not driven. Whether any current stack refuses `verifier@` was not measured.
- **The aggregator half of Q2's three shapes was not run.** Those shapes are: a fallback run reads clean, a leak reads HIGH/critical, a truncated artefact reads unreadable. The missing step is #1398's 09 (head `9414aa54e`) reading the new artefacts. Only the job half is measured here.
- **A runner that crashes before printing JSON.** After the fix its artefact is empty (0 bytes) and the error text moves to `.stderr`. `jq -e .` on an empty file exits 4 (measured), so #1398's guard still reads it as unreadable. This was not driven end to end.
- **Open PRs were not listed.** This seat has no authenticated `gh` for the Secuura identity. Instead I read the `ls-remote` branch names, plus the diffs of #1398's branch (it touches only `09-aggregate-report.sh`) and `ks-1401-tenant-isolation-after-039` (a migration). Neither touches job 06.
- **Not run:** GNU bash and Linux jq. shellcheck is not installed.
- **Side reading for Q2's "per-PR check" question.** These are the workflow files at develop `d75bfe2`, not the PR's Actions logs:
  - `api-contract-tests.yml` (which runs `ci/orchestrate.sh`, and so job 06) is `on: workflow_dispatch` only, with `pull_request` commented out at `:27`;
  - `internal-audit.yml` says "ON DEMAND ONLY" at `:4`.
  - The gate's own measurement still governs.

## Questions for Wednesday

1. **Ticket key.** The brief is keyed `KS-1136` because brief_lint requires `# KS-<n>` and no ticket exists. KS-1136 is the ticket whose #1398 merge this fix conditions. *Rec:* the raise seat files the defect's own ticket (title along the lines of "Job 06 writes its runner's stderr into the JSON artefact (`06-tenant-isolation.sh:71` `2>&1`)"). The PR says `Refs <new>` and `Refs KS-1136`. The brief dir can stay as queued, and the round result is still valid under the new key.
2. **Auth-surface verdict.** I judge it not an auth surface (see the predicate section). *Rec:* accept, and run it on the Spark.
3. **Header `Writes:` line (`:23`)** still names only the JSON. Per "nothing else changes", I left it out of scope. *Rec:* keep it out for the Spark round. If the PR reviewer wants it, it is a one-line follow-up on the raise seat.
4. **Gate shapes.** The 06 PR's own gate needs the three Q2 shapes measured with #1398's 09, and that is not in this brief. *Rec:* the gate kit for the 06 PR drives 09 at `9414aa54e` over the fixed job's artefacts, since #1398 merges after it.
5. **Cache clone disk.** The control left one ~335 MB clone in `spark/cache/work/`. *Rec:* include it in the next hand quarantine (`mv`, never delete).
