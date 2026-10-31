## QA GATE 60, TIER 2, BATCH ROUND 1: KS-1868 #1864 #1867 #1870

Gate commissioned by Wednesday, Sat 31 Oct 2026. Findings only: nothing fixed, pushed, commented, merged or mailed; no Linear ticket touched. Evidence root: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-31_gate60-ks1868-batch/evidence/` (called `evidence/` below).

### BLUF

All three PRs do what they say and nothing more. Every changed product line is an inner `try`/`catch` around the existing thrown-value read, with the constant fallback `unreadable thrown value`. Every new RED cell fails at the merge-base product code with an assertion (no WARN logged / handler threw) and passes at head. 20 of 20 mutants I wrote were killed. No path collides with any of the other 38 open PRs, and every combination merges cleanly on develop. No client-visible string changes. Three small things to know, none blocking:

- There is **no shared `safeReason` helper** in any of the three PRs. KS-1868 proposes one; these are inline per-site guards. So Q3 ("does the helper...") is answered for the inline expression, and the answer has one residue (G60-F1).
- The guard covers a *throwing* read, not a read that returns a *hostile non-string*. An Error whose `message` getter returns an object with a throwing `toJSON` still reaches the logger as an object (G60-F1).
- #1870's live body contains no visible "correction" note about the hook wording (G60-F3); the wording itself is correct in all three.

| PR | Head at start | Head at end | VERDICT |
|---|---|---|---|
| #1864 (vc-issuer, 3 sites) | `76ad178e57d51c0f1af414f5083cab672616caf6` | `76ad178e57d51c0f1af414f5083cab672616caf6` | **GO WITH NOTES** |
| #1867 (analytics, 2 sites) | `437a04ba54f71ea51e31a7d6e78a0bafa67fd17b` | `437a04ba54f71ea51e31a7d6e78a0bafa67fd17b` | **GO WITH NOTES** |
| #1870 (demo-service, 1 site) | `7388d629ea88851ad82c282c4b217d2b2c727b55` | `7388d629ea88851ad82c282c4b217d2b2c727b55` | **GO WITH NOTES** |

develop at start `86f80c190f3eb12c08af91d1796aa39a1d3d8bed`, unchanged at the mid-gate re-read (`evidence/heads_start.txt`, `evidence/heads_end_1.txt`; the final re-read is recorded at the bottom). The notes are G60-F1 (all three) and G60-F3 (#1870); neither is fix-before-merge.

### Findings

| ID | PR | Severity | Finding | Evidence |
|---|---|---|---|---|
| G60-F1 | #1864 #1867 #1870 | minor | The inner try protects against a read that THROWS. It does not protect against `err.message` returning a non-string. An Error whose `message` getter returns an object with a throwing `toJSON` is logged as `{error: <object>}`; `JSON.stringify` of the logged meta then throws (a number is logged as a number). This is the same hazard KS-1868's own text describes (gate 36: "3 still hung after the first change because the message value reached the real logger as a non-string") and the PR bodies do not claim to cover it; they cover revoked Proxy and throwing getter only. Not a regression: base throws earlier. | `evidence/probe_shapes.txt`, `evidence/g60-probe.test.ts.txt` |
| G60-F2 | #1864 #1867 #1870 | file-only | No shared helper. KS-1868 proposes `safeReason(e)` in a shared package with one test for the class; the three PRs add 6 copies of a 5-line inline block (3 + 2 + 1 sites) and 6 test files' worth of cells. Each copy is a separate place where the fallback string can drift. Ticket stays open by the PRs' own statement, so not a defect; noted for the helper decision. | `evidence/product_diffs.txt` |
| G60-F3 | #1870 | file-only | Brief says the #1870 body notes a correction to the hook wording quoted in #1864/#1867. The live #1870 body (2026-10-31, head `7388d629`) has no sentence saying so (searched "wording", "correct", "quoted", "misquot"; the search could have matched, see Q6 control). The leg 6/7 wording itself is identical and correct in all three bodies. | `evidence/pr1870_body.md`, Q6 |
| G60-F4 | #1864 | file-only | #1864's ensureTable hand edit keeps `err?.message`, so a thrown string or `undefined` logs `undefined` (declared in the body). With a message getter that returns a non-string the logged `error` is not a string either. Same class as F1; declared semantics. | `evidence/own_summary.txt` |

No fix-before-merge finding.

### Q1. Does each PR change only what it claims? (FOUND / TESTED / HOW)

- **FOUND:** yes. Merge-base for all three is `ddc644fb4869e615e3f3fc68480e60410dcfebcf`; each PR is one commit on it (`git log origin/develop..pr/N` = 1 commit each).
- **TESTED / HOW:** `git diff --stat ddc644fb4869...pr/N` and the REST `/files` lists agree (`evidence/q1_diffstat.txt`, `evidence/pr*_files.json`).
  - #1864 (6 files): `vc-issuer/src/repositories/credentialRepo.ts` (+14/-2), `vc-issuer/src/routes/presentations.ts` (+7/-1), two new `__tests__/ks1868-*` files (+93, +60), two docs fragments (`Projects Documents/fragments/flow|cheat/KS-1868-vc-issuer-unreadable-thrown-value.html`).
  - #1867 (6 files): `analytics/src/services/analyticsService.ts` (+7/-1), `metricsCollector.ts` (+7/-1), two new tests (+60, +60), two docs fragments.
  - #1870 (4 files): `demo-service/src/routes/scenario.ts` (+6/-1), one new test (+99), two docs fragments.
- Product diffs read in full (`evidence/product_diffs.txt`): every hunk is the `let reason; try { <original read> } catch { reason = 'unreadable thrown value' }` shape, with the logger call using `reason`. No other line moves. No lockfile, package.json or config file is touched.
- Control: the harness `numstat` and my `--stat` match the REST additions/deletions per file.

### Q2. Client-visible behaviour per replaced site

- **FOUND:** unchanged for every readable thrown value; changed only for the two unreadable shapes, as each body declares.
- #1864 `credentialRepo.loadFromDb`, `presentations.loadPresentationsFromDb`, `credentialRepo.ensureTable`: start-up loaders with no response. Observable change = WARN is logged and the call resolves, where before the TypeError escaped the catch. Readable values log the same string (probe: Error `plain-msg`, string, null, undefined, `[object Object]`, Symbol all identical to the base expression).
- #1867 `AnalyticsService.loadFromDb`, `MetricsCollector.loadFromDb`: same shape, same result (the base-run cells fail on "no WARN").
- #1870 `GET /scenario/context`: the 500 body stays `{success:false,error:{code:'INTERNAL_ERROR',message:'Internal server error'}}` and status 500. The test asserts `threw=false`, `status=500` and the full body for the control and both red cells. Before, the handler threw and the client got no answer. The logged string changes only for unreadable values. No header is set in the catch (read in the diff); no header assertion exists and none is needed.
- A mutant that leaked the raw error into the 500 body was killed by C1, R1 and R2 (Q4), so the body is actually pinned.
- **No undeclared client-visible string change found.**

### Q3. Does the safe-reason read ever return a raw message or stack for an unknown throw?

There is no helper (G60-F2); the read is the base expression wrapped in a try. So: for any `Error` it returns `err.message`, never `stack`; for a non-Error it returns `String(err)`. That is the pre-existing behaviour, deliberately unchanged ("readable thrown value unchanged"). I ran the real `loadFromDb` at head with 14 thrown shapes (`evidence/probe_shapes.txt`):

| Thrown shape | Logged `error` |
|---|---|
| Error('plain-msg') | `"plain-msg"` (message only; a planted `stack` of `STACKSECRET` was NOT logged) |
| null / undefined / string / plain object | `"null"` / `"undefined"` / the string / `"[object Object]"` |
| object whose `toString` throws; `Object.create(null)`; revoked Proxy; Proxy with throwing `getPrototypeOf`; Error whose `message` getter throws | `"unreadable thrown value"` |
| Symbol | `"Symbol(sym)"` |
| Error whose `message` getter returns 42 | `42` (number) |
| Error whose `message` getter returns `{toJSON(){throw}}` | the object itself; `JSON.stringify(meta)` throws: **G60-F1** |

Control that the probe could see a leak: the plain Error row shows the raw message is reported (so a leaky variant would have shown), and the getter-returns-object row shows the probe catches non-string leakage. Mutants M3 and M4 (Q4) show the cells catch "always String(err)" and "fallback re-reads the raw message".
**HOW the claim "never returns raw message for an unknown throw" holds:** it does not, by design, for readable Errors and strings; a readable `Error.message` is the content of the log line. For *unreadable* throws the fallback is a constant. Unknown-object throws never reach the logger as an object, except the getter-returns-non-string case (F1).

### Q4. RED at base for the right reason, GREEN at head, mutants

Own run (vitest 4.1.12, Node as installed on this host, root `npm ci` in `Blockchain/Dev`, `@secuura/shared` built), `evidence/own_summary.txt`, logs in `evidence/own/`:

| PR | Head | Base (merge-base product code, head tests) |
|---|---|---|
| #1864 | 8 of 8 pass | 3 pass / 5 fail: C1, C2, presentations C1 pass; R1, R2, R3, presentations R1, R2 fail with `expected [] to have a length of 1 but got +0` (no WARN logged) |
| #1867 | 6 of 6 pass | 2 pass / 4 fail: both controls pass; R1, R2 fail in both files, same assertion |
| #1870 | 3 of 3 pass | 1 pass / 2 fail: C1 passes; R1, R2 fail `expected true to be false` (the handler threw) |

Whole service suites at head: vc-issuer 21 files / 421 pass; analytics 9 files / 44 pass; demo-service 10 files / 89 pass (matches the bodies' figures). One earlier demo-service run showed 5 failures in `demoGuard.test.ts` because my sparse checkout lacked `Blockchain/Dev/docker/nginx-gateway/*.conf` (ENOENT in the log); after adding that path: 89 of 89. That was my environment, not the PR (`evidence/own/full_1870.log` vs `full_1870b.log`). The intermittent KS-1182 cell mentioned in #1870's body did not fail in my run (1 run; not evidence about the intermittency).

**Mutants** (script `evidence/mutants.txt`; each applied to the head product file, run, restored; every restore verified clean by `git diff --stat pr/N`):

| PR / file | M1 drop inner try | M2 fallback string changed | M3 `String(err)` / 500 body leaks raw err | M4 fallback re-reads `err.message` |
|---|---|---|---|---|
| #1864 credentialRepo.ts (2 sites) | killed (R1 R2 R3) | killed (R1 R2 R3) | killed (C1) | killed (R1 R2 R3) |
| #1864 presentations.ts | killed (R1 R2) | killed | killed (C1) | killed |
| #1867 analyticsService.ts | killed (R1 R2) | killed | killed (C1) | killed |
| #1867 metricsCollector.ts | killed | killed | killed (C1) | killed |
| #1870 scenario.ts | killed (R1 R2) | killed | killed (C1 R1 R2) | killed |

20 of 20 killed; 0 survivors; every mutation reported "applied" (a non-applying mutation prints MUTATION DID NOT APPLY; none did). Single-site check: dropping only the `ensureTable` try is killed by R3 alone (`evidence/full_suites_and_single_mutant.txt`), which shows the hand-edited site has its own cell.

### Q5. Collisions and merge

- Open PRs: 41 listed (REST, per_page 100, paginated loop; stops on a short page), file lists fetched per PR and compared to each PR's `changed_files` count: no truncation (`evidence/q5_overlap.txt`).
- **Exact-path overlap with #1864, #1867 or #1870: none.**
- Controls that the detector can fire: it flags 4 PRs touching a `package.json`/lock inside the same three service directories (#575, #649, #948, #1360), and #1869 touching `vc-issuer/src/routes/credentials.ts` (same service, different file, plus its own KS-1851 fragments). Those are service-level neighbours, not collisions. The docs pages (`Projects Documents/*.html`) are touched by 17 other PRs but this batch edits only new fragment files, so no overlap (that is the reason fragments exist).
- Merge: `git merge-tree --write-tree` with develop at `86f80c190f3e`: #1864 rc 0, #1867 rc 0, #1870 rc 0; all three stacked on develop together rc 0 (`evidence/q5_merge.txt`). Planted control: a commit editing the same line in `presentations.ts` as #1864 against the same merge-base returns rc 1 with three unmerged stages, so the check can fail.

### Q6. Hook wording in the live bodies

- Source of the quoted lines: `Blockchain/Dev/scripts/audit/audit-locks.mjs:472` prints `OK — no standalone-lock advisories outside the triaged baseline.`; `audit-gate.mjs:215` prints `OK — no advisories outside the triaged baseline.`; `preflight.sh:875` prints `PREFLIGHT INCOMPLETE — $n_ran/$TOTAL_LEGS legs ran, $n_skipped SKIPPED. Nothing failed.` (preflight's own echoes at 475 and 517 omit the final full stop).
- All three live bodies quote leg 6 and leg 7 with exactly those strings (`evidence/pr186*_body.md`; count of the leg 7 phrase = 1 in each, found with a case-insensitive search that also finds it in all three, so it could have been zero). **Leg 7 is quoted correctly in all three.**
- **G60-F3:** I cannot find a statement of the correction in #1870's body, so the "notes a correction" premise is not visible in the live text. I did not have the earlier body to compare, so I cannot say what the old wording was.

### NOT TESTED

- Schemathesis, Akto, Playwright, Performance/k6 (the bodies list these as NOT run too; both pre-merge ack boxes are deliberately unticked on all three).
- A running stack, any deploy, the pre-push hook legs (I read the script's printed strings, did not run it).
- Node 24 / LTS; this host runs the non-LTS Node line used by the author.
- `docs-fragments.mjs check` (I read the fragments and did not run the checker; the sparse tree lacks `scripts/`).
- `tsc`, eslint and the test-types ratchet claims in the bodies: not re-run.
- Real production logger path (`NODE_ENV=production`) and the real logger's treatment of a non-string `error` (F1 uses a mock logger plus `JSON.stringify`).
- The intermittent KS-1182 R1 cell (1 passing run only).
- Whether any real code path throws these shapes (the ticket says none is known).
- Process hygiene: I started no long-lived processes and killed none by name; the only task I stopped was my own background `git grep` (by task id).

### Method notes

- Clone: `evidence/..` parent folder `repo` (partial clone, `git -C <dir> rev-parse --show-toplevel` asserted equal to the dir before any fetch). Worktrees under `wt/`, `node_modules` installed once with `npm ci` at the `Blockchain/Dev` workspace root, `packages/shared` built with `tsc`.
- Harness incidents (mine, not the PRs'): two Spark-gate runs were discarded because the harness's worktree had no resolvable `vitest` / `date-fns` / `@secuura/shared` (service-local `npm ci` hoists to the workspace root); kept as `evidence/spark_run1_harness_nodemodules_missing/` and `evidence/spark_run2_harness_deps_missing/`. The third run used a symlinked complete `node_modules` and is the one reported.

### Spark half (Kam's 2026-10-26 gate pilot)

- **Deterministic half**, `spark_gate.sh <clone> <pr> <head> develop <test files> --node-modules <complete tree> --work <scratchpad gate60_work/r3pr N> --out evidence/spark/pr N` (non-pytest mode, vitest): head sha asserted equal to `refs/pull/N/head` (mode `tip`), merge-base `ddc644fb4869`. Facts (`evidence/spark/pr*/facts.json`): #1864 head 8 pass / 0 fail; base product code 3 pass / 5 fail. #1867 head 6 / 0; base 2 / 4. #1870 head 3 / 0; base 1 / 2. Identical to my own runs.
- **Harness failures, reported and not blocking:** runs 1 and 2 gave `files_failed` with 0 passed because the harness symlinks one service's `node_modules` into a fresh worktree, but this repo is an npm workspace, so `vitest`, `date-fns` and `@secuura/shared` live at `Blockchain/Dev/node_modules` and were not found (`Cannot find module 'vitest/config'`, then `Cannot find package 'date-fns'`, `@secuura/shared/vc`). Run 3, with a symlink tree holding the full hoisted `node_modules` and a built shared package, is the reported one. A harness that cannot see a workspace-hoisted install reports a red that is its own: worth a line in the harness header (`--node-modules` must be the workspace-root tree).
- **LLM half**, `spark_review.py` with `--facts`, `--diff`, `--ticket KS-1868`, `--pr-body-file` (all three `valid: true`, schema clean; #1864 needed attempt 2 after a `repetition_abort` on attempt 1). The script has no option to add a context file, and none was needed: these PRs have no helper file for the code to depend on (gate 59's false positive cannot recur here). All three Spark verdicts: **GO WITH NOTES**, **all findings severity Note, zero Major, zero Minor**. Raw: `evidence/spark/pr*/review/review.json`.

#### CALIBRATION: each Spark finding vs mine

| Spark finding | Mine | Calibration |
|---|---|---|
| #1864-1 "byte-identical to the tree the suites ran on" is self-reported | I re-ran suites at head: same figures | Agree (unverifiable by the runner; verified by me) |
| #1864-2 ensureTable string/undefined logging | Spark itself concludes "consistent, no finding" | Spark false positive (self-retracted); agrees with my F4 only as declared semantics |
| #1864-3 "7 more `err?.message` lines" unmeasured | Measured: 8 hits at base incl. ensureTable, 7 others at 92, 113, 154, 182, 297, 386, **469** (body says 475, which is the head line number after the +6 shift, not "at the base") | Agree it was unmeasured; I found a trivial body slip (G60-F5, file-only) |
| #1864-4 "whole suite re-run" unmeasured | Measured: 21 files / 421 pass at head | Agree (claim true) |
| #1864-5 tsc/eslint unmeasured | NOT re-run by me | Agree (both of us leave it unverified) |
| #1864-6 platform suites NOT run, consistent | Same | Agree |
| #1864-7 docs-fragments check unmeasured | NOT re-run by me | Agree (unverified) |
| #1864-8 open-PR overlap and pre-push unmeasured | Overlap re-measured by me: confirmed zero overlap (41 open PRs now); pre-push hook not re-run | Agree; overlap claim holds |
| #1867-1 fixes 2 of 253 | Same, declared | Agree (non-issue) |
| #1867-2 synthetic tests only | Real handler/function, synthetic throw values; ticket also says "not measured" | Agree |
| #1867-3 not run: platform suites, LTS | Same | Agree |
| #1867-4 logger mock may not match the real logger on a non-string value | My G60-F1: a non-string `message` reaches the logger and `JSON.stringify` of the meta throws | **Agree and partly caught** the F1 class (as a mock-fidelity worry, without naming the shape) |
| #1867-5 "unchanged for readable value" supported by the diff | Same (probe) | Agree |
| #1867-6 rejection carrying a TypeError is not tested directly | True: the cells swallow the rejection and assert on the missing WARN; base failure is "no WARN" | Agree (minor test-shape note; mutants still kill, so no gap in effect) |
| #1870-1 fixes 1 of 253, helper not implemented | My F2 | Agree |
| #1870-2 root cause unmeasured in real env | Same as ticket | Agree |
| #1870-3 base red only by missing fallback | Same (handler threw, `expected true to be false`) | Agree |
| #1870-4 logger double more permissive than the real one | My F1 | Agree (same family as #1867-4) |
| #1870-5 "alters the logged message from 'Unknown error' to 'unreadable thrown value'" | The base throws for the unreadable case, so there was no log line; for a non-Error value 'Unknown error' is unchanged (body says so) | **Spark false positive** (misreads the change as a rename) |
| #1870-6 platform suites not run "but still claims a pre-merge gate is incomplete" | Same unticked boxes, declared | Agree / noise |

**Spark missed:** G60-F1 by name (the non-string-`message` shape and the `JSON.stringify` throw), G60-F2 on #1864/#1867 (no helper, 5 inline copies), G60-F3 (no correction note in #1870's body), G60-F5. Spark raised no false Major; 1 clear false positive of 20 (#1870-5) and 1 self-retracted finding (#1864-2). Spark's verdicts match mine on all three PRs.

### Additional finding

| ID | PR | Severity | Finding | Evidence |
|---|---|---|---|---|
| G60-F5 | #1864 | file-only | Body says the other 7 `err?.message` reads sit at "lines 92, 113, 154, 182, 297, 386, 475 at the base". At the base they are 92, 113, 154, 182, 297, 386, **469**; 475 is the head line after the +6 shift. Count (7) is right. | `git grep -n "err?.message" ddc644fb4869 -- .../credentialRepo.ts` |

### Final head re-read

All four refs read at the end of the gate equal the refs read at the start: #1864 `76ad178e57d51c0f1af414f5083cab672616caf6`, #1867 `437a04ba54f71ea51e31a7d6e78a0bafa67fd17b`, #1870 `7388d629ea88851ad82c282c4b217d2b2c727b55`, develop `86f80c190f3eb12c08af91d1796aa39a1d3d8bed` (`evidence/heads_end_final.txt`). No head moved; no stop.
