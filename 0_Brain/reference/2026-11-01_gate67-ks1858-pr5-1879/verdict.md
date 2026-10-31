## QA GATE 67, TIER 2, ROUND 1: KS-1858 PR 5, Secuura/Distributed_Secuura #1879 (services/auth, four social adapters)

Gate commissioned by Wednesday, Sun 1 Nov 2026. Findings only: nothing fixed, pushed, commented, merged or mailed; no GitHub or Linear write (no GitHub API call at all: git fetch/ls-remote only, so the PR body and CI state were NOT read; the author's mail and the two docs fragments in the PR were). Host Node **v26.8.1** (non-LTS), vitest 4.1.12, tsc via the repo's own devDependency. Evidence root: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate67-ks1858-pr5-1879/evidence/` (called `evidence/` below).

### BLUF

#1879 does what it says and nothing more. Each of the four adapters (Google, Facebook, LinkedIn, Microsoft personal) now reads the token answer as `access_token?: unknown` and, if it is not a non-empty string, logs and throws `<Provider> token exchange failed (no access token)` before any profile call. Product +24/-4 over four files, 4 new test files (20 cells), 2 docs fragments; 10 files, +358/-4, one commit on `eb9651392f49`, exactly as stated. **The product and test hunks are byte-identical to the Wednesday goldens and to the held Spark patches** (applied to the base blob, compared to the head blob: 16 of 16 BYTE-IDENTICAL, Google included). Red first reproduced: 12 of 20 fail at base by assertion for the product reason, 20/20 pass at head. Whole services/auth suite on a scratch merge with current develop: 117 files / 1385 of 1385 pass, twice; develop alone 113 / 1365 of 1365 (control); the delta is exactly +4 files / +20 cells. 28 mutants (7 per adapter): 24 killed, 4 survived (all the same one: the `logger.warn` line is unpinned). Merge onto current develop is clean (rc 0). It does not reach further than a refusal: no input that signed in before now signs in as someone else, and no accepted shape was found that is newly refused except the shapes "no usable access_token". **Tier 2 stands; no reason to recommend tier 1.**

The author's OPEN QUESTION: the missing `error`-field clause is **not a defect for what this PR claims** (an error-only 200 answer is already refused by the access_token check: measured, G67-F1) and is **a difference by design of GitHub's API as far as the code shows, UNKNOWN for the other four** (not measured against any provider). A 200 answer carrying BOTH a valid-looking token and an `error` field is accepted by all four, exactly as at base. How to close it is under G67-F1.

Four notes, none blocking (G67-F1..F4).

### Heads

| Ref | At start (2026-11-01 06:11 AEDT) | At end (06:24 AEDT) |
|---|---|---|
| PR #1879 head | `6b867a532ee7307ec5e32c1f18ac408f05b8b25a` | `6b867a532ee7307ec5e32c1f18ac408f05b8b25a` |
| develop | `dd583b4f7495193e7f846e02b41e2a462e687774` | `f6ab90c6376e688544555f7b45487cb6f49bef3a` |

Merge-base of head and develop: `eb9651392f4959ea509376d885242cf3e22512ed` (one commit on it). Note the brief named develop `0fab207f2bc8`; develop had already moved on by my start (`dd583b4f`) and once more during the gate (two files, `.github/pull_request_template.md` and `Blockchain/Dev/DEVELOPMENT.md`, no overlap). The head did not move; no stop. `evidence/heads_start.txt`, `evidence/heads_end.txt`.

### VERDICT: **GO WITH NOTES**

Conditions: none to merge. Notes G67-F1 (decide the `error`-field question deliberately) and G67-F2 (the log line is unpinned and carries less than github.ts's) are for the owner to take or leave. The platform suites, a real provider call and any LTS Node were not run (see UNMEASURED); the PR body does not claim them.

### Findings

| ID | Severity | Finding | Evidence |
|---|---|---|---|
| G67-F1 | minor (note) | **Open question, answered.** `github.ts` refuses on `typeof access_token !== 'string' \|\| '' \|\| error !== undefined` and carries the comment that GitHub "answers a bad or expired code with HTTP 200 and an {error, error_description} body" (KS-1792). The four new guards omit the `error` clause. Probe through the real adapters (stubbed fetch, 8 shapes x 4 adapters, same probe on develop for comparison): **P2 `200 {error:'invalid_grant'}` (no token) is REFUSED at head on all four with the `(no access token)` text and the profile endpoint is never called (fetches=1); at develop it went on to the profile call (fetches=2).** So an error-only 200 is covered without the clause. **P1 `200 {access_token:'tok', error:'invalid_grant'}` RESOLVES at head on all four, identical to develop** (fetches=2). github.ts would refuse P1. Verdict on the omission: not a defect against the PR's scope (the sentence is "no access_token"); the extra clause only matters for a token-AND-error answer, which no provider is shown to emit here. Whether Google, Facebook, LinkedIn and Microsoft ever do is **UNKNOWN: not measured** (my recollection is that they follow RFC 6749 and answer errors with 4xx, GitHub being the known exception, but I did not read any provider document or call a provider in this gate). To close: (a) read each provider's token-endpoint error documentation, or (b) a live probe with an expired code against a disposable app registration per provider; then either add the clause with a P1 cell, or add one cell that pins P1 as accepted so the decision is on the page. Oracle: Product consistency (github.ts) and Purpose. | `evidence/own/probe_head.txt`, `probe_develop.txt`, `q_callers.txt`, `/private/tmp/g67_probe.test.ts` |
| G67-F2 | minor | **The `logger.warn` line is pinned by no cell, and it logs less than github.ts's.** Mutant "logger.warn line removed" SURVIVES on all four adapters (5 of 5 cells still pass). No cell asserts the log. Separately, github.ts logs a bounded `error` value (`error.slice(0, 80)`) with the refusal; the four new lines log only `{ provider }`, so when a 200 answer with an error arrives an operator sees "answered 200 without an access token" and no reason. The flow fragment states the log carries "the provider name only, no body", so this is declared, a deliberate choice. Not a security problem (nothing from the body is logged); a diagnosability gap and an unpinned line. | `evidence/mutants.txt`, `mutants.json` (M7 x 4) |
| G67-F3 | file-only | **Whitespace-only token passes the guard.** P6 `{access_token:' '}` resolves at head on all four and the profile call goes out with a blank bearer (Facebook: blank in the URL). Same as github.ts, which also tests only `=== ''`; the PR says "missing, non-string or empty" and that is what it does. Not claimed otherwise. Also unchanged: P3 body `null` still rejects with a TypeError (message text differs only by V8's wording for Facebook/LinkedIn/Microsoft), P4 a non-JSON 200 still rejects with a SyntaxError; neither is a refusal under the new guard. | `evidence/own/probe_head.txt` |
| G67-F4 | file-only | **The two ks949 flakes did not reproduce.** The PR and the author's mail say two ks949 seed-site cells time out at 5 s (and a cold-start hook skips a file) on develop itself. In my runs (`--maxWorkers=2`, started at load1 6.8 to 6.9, nice 10): develop alone 113 files / 1365 pass / 0 fail / 0 skip; merge 117 / 1385 / 0 / 0, twice. Their claim is about a timing flake and one machine; mine does not disprove it, it is simply NOT REPRODUCED (3 runs, 0 occurrences, no instrument to force one). The author's totals match mine exactly in the passing case (1365 on develop, 1385 with the change). | `evidence/own/full_develop.log`, `full_merge.log`, `full_merge_run2.log` |

No fix-before-merge finding. Nothing found that the PR claims and I could not confirm.

### Q1. The open question (github.ts vs the four)

- **FOUND:** `github.ts` at develop (`dd583b4f`, lines 86-93) quoted above: the `error` clause, its KS-1792 comment, and a log with a bounded `error` value. The four head adapters: guard is the first two conditions only (`facebook.ts:83`, `google.ts:88`, `linkedin.ts:86`, `microsoft-personal.ts:88`).
- **TESTED:** the 8-shape probe through the real classes (see G67-F1). The controls: P8 (`{access_token:'tok'}`) resolves on all four at head and develop (fetches=2); the same probe against develop reproduces the pre-PR behaviour, so the diff between the two files is the effect of the PR. Develop-vs-head diff of the probe: P2, P5 (`[]`) and P7 (`access_token:null`) newly refused on all four, P3 changes only TypeError wording on three; P1, P4, P6, P8 unchanged.
- **Caution on reading the probe:** at develop the stub profile endpoint answers 200 whatever the Authorization header, so develop's "RESOLVED" on P2/P5/P7 is a stub artefact. A real provider would answer `Bearer undefined` with 401 and the adapter would reject with `Failed to fetch ... user profile` (that is exactly what the red cells show at base). The PR changes the failure from late to early and gives it a clearer text; it does not change who signs in. EVIDENCE CLASS of that sentence: MEASURED AT RUNTIME for the stubbed adapters; READ ONLY for what a real provider does with `Bearer undefined`.
- **Other places this text/shape lives:** `grep access_token` over `services/auth/src` (non-test): only the five social adapters and `routes/oauth.ts` (an outbound field name). `apple.ts` has no access_token read (id_token path, declared a different ticket). No consumer matches on any of the new or old message strings (api-gateway, m365, originate mentions are unrelated token-exchange texts). `evidence/q_callers.txt`.
- **Not covered:** Apple, the connector-token routes, anything outside the four.

### Q2. Red first, and mutants

- **Re-run on my checkout.** Via the Spark harness (`spark_gate.sh`, base ref `develop` as a name, not a sha, `--work /private/tmp/g67/spark`, rc 0, 26 s): head 4 files / 20 pass / 0 fail; **base product code 4 files failed, 8 pass / 12 fail**, merge-base `eb9651392f49` (differs from head: yes, 10 files in `diff.patch`). **Why red:** every one of the 12 fails is `AssertionError: expected 'Failed to fetch <Provider> user profile…' to be '<Provider> token exchange failed (no access token)'` (3 per adapter: R1 empty object, R2 numeric token, R3 empty string); the 2 controls per adapter (C1 good answer, C2 non-2xx) pass at base. So the red is the product reason, not a setup or import error. Matches the author's 12 of 20. `evidence/spark/facts.json`, `targeted_base.log`.
- **On the merge:** `vitest run ks1858` 4 files / 20 pass (`evidence/own/targeted_merge.log`).
- **Mutants (my own, per adapter, applied by unique anchor with the anchor count asserted equal to 1, the tamper checked as landed, restored and sha256-verified each time; `git status` of the scratch worktree clean after):**

| # | Mutant (same on each adapter) | Result |
|---|---|---|
| M1 | guard condition replaced by `false` | KILLED x4 (R1, R2, R3) |
| M2 | guard inverted `!(cond)` | KILLED x4 (C1, R1, R2, R3) |
| M3 | empty-string check dropped | KILLED x4 (R3 only) |
| M4 | typeof check dropped | KILLED x4 (R1, R2) |
| M5 | refusal message changed | KILLED x4 (R1, R2, R3) |
| M6 | refusal returns instead of throwing | KILLED x4 (R1, R2, R3) |
| M7 | `logger.warn` line removed | **SURVIVED x4** (G67-F2) |

28 applied, 24 killed, 4 survived. Every kill is by a named cell. Each cell is thus the only cell holding its one clause (R3 alone holds the empty-string check, R1+R2 the typeof): a coverage the cells earn without redundancy.

### Q3. Whole services/auth suite

| Run | Result |
|---|---|
| Develop alone `dd583b4f` (control; own worktree, shared node_modules) | 113 files / 1365 pass / 0 fail / 0 skip |
| Scratch merge `3f5ad6795f3f` (tree `86ddcf123cf6`, parents develop `dd583b4f` and head) run 1 | 117 files / 1385 pass |
| Same, run 2 | 117 files / 1385 pass |

Delta +4 files / +20 cells, i.e. only the new tests. `npm ci --ignore-scripts` on the merged lockfile (1795 packages, rc 0), `packages/shared` built with tsc, `--maxWorkers=2`, nice 10, started at load1 6.8-6.9 (the gate ceiling 7). One earlier full run from the wrong cwd failed 2 tests plus one suite on paths computed from `process.cwd()` (ks1467, ks1009); that was MY invocation (run from the wrong working directory), not the PR; rerun from `services/auth`, all green. Not hidden: `evidence/own/full_merge.log` is the corrected run.
Static: `tsc --noEmit -p services/auth/tsconfig.json` rc 0, 0 errors. `tsc -p tsconfig.test.json` (the test ratchet) 42 errors, none in any `ks1858` file or `providers/social` (positive control: the same log lists 42 error lines in other test files; the author's quoted baseline is 42). eslint on the 4 adapters and 4 new tests rc 0 (no planted-file control run by me; the author reports one). `evidence/own/tsc_service_merge.log`, `tsc_test_merge.log`, `eslint.log`.

### Q4. Nothing else changed; provenance

- **Files:** `git diff --name-only eb9651392f49 refs/pr/1879` = 10: the 4 adapters, the 4 `ks1858-*` test files, `Projects Documents/fragments/cheat/KS-1858-…html`, `…/flow/KS-1858-…html`. Detector control: that list against itself reports 10 of 10 (`evidence/pr_files.txt`).
- **Product hunks per adapter:** one `const { access_token } = …` line replaced by the typed read, the guard, and (Facebook, LinkedIn, Microsoft) a `const access_token = tokenBody.access_token` re-bind; Google keeps `tokens.access_token` in place. The `!tokenRes.ok` branch, profile calls, mappers and timeout are untouched. Facebook still puts the token in the profile URL query (pre-existing; the warn line does not log the URL), noted and not counted.
- **Goldens:** for each adapter I applied (a) `night/briefs/KS-1858-auth-<p>-refuses-no-access-token/golden.diff` and (b) the run's `out.md.checker/patch.diff` (Google: the `-r2` run, its harness verdict says `golden: TREE-IDENTICAL`; the first Google run said `DIFFERS`) to the base blob and `cmp`-ed the result against the PR head blob, product and test file. **All 16 BYTE-IDENTICAL.** The Google golden diff differs from the PR diff by 4 blank-line `+`/`-` shuffle lines in the hunk text (the author's "differs only by header lines"), but the resulting file is identical. `evidence/golden_compare.txt`. Control for the comparer: the same harness would print DIFFERS with the first 12 diff lines for any mismatch; I did not plant a mismatch (the single mismatch it could be shown is the Google first run, whose harness record says DIFFERS, which I did not re-apply).
- **Docs fragments:** read both; their figures (20 cells, 12 of 20 red, 1365/1385, 42 baseline, +6/-1 and +5/-1) agree with my measurements, and the claim "no hand edit" is borne out by the byte comparison.

### Q5. Merge onto current develop

- `git merge-tree --write-tree origin/develop refs/pr/1879`: develop `dd583b4f` **rc 0, tree `86ddcf123cf6`**; develop `f6ab90c6` (at end) **rc 0, tree `7513b20ce4e9`**; the author's develop `0fab207f2bc8` rc 0, tree `ba9343410b47`.
- Positive control for the detector: a commit on the merge-base editing the same line of `facebook.ts`, merged against the PR, returns **rc 1** with three unmerged stages. `evidence/q5_merge_*.txt`.
- develop's movement from `0fab` to `f6ab` touches `originate` (3 files), two KS-1579 fragments, `.github/pull_request_template.md`, `DEVELOPMENT.md`: **0 paths shared** with the PR (control 10/10).
- **Open-PR overlap was NOT re-scanned** (no GitHub API read by design); the author reports 29 open PRs and none on these paths at 18:46Z.

### COUNTS

| Measure | Value |
|---|---|
| Files changed | 10 (+358/-4) |
| New cells | 20 (12 red at base by assertion, 8 controls) |
| Suite develop / merge | 113 files 1365 / 117 files 1385, all pass |
| Mutants | 28 (24 killed, 4 survived) |
| Probe shapes x adapters | 8 x 4 = 32 rows, plus the same on develop |
| Goldens compared | 16 byte comparisons, 16 identical |
| Findings | 4 (0 major, 2 minor, 2 file-only) |

### SPARK SHADOW AND CALIBRATION

Deterministic half: `spark_gate.sh <clone> 1879 6b867a53… develop <4 test files> --node-modules <complete hoisted tree of an existing worktree> --work /private/tmp/g67/spark --out evidence/spark` (rc 0). **Did BASE really differ from HEAD? Yes**: merge-base `eb9651392f49` vs head `6b867a532ee7`, `head_mode` tip, 10-file diff, base run failed 12 where head failed 0. LLM half: `spark_review.py --facts --diff --ticket KS-1858` (no PR-body file: I read no GitHub body), valid, attempt 1, 49 s, `evidence/spark/review/review.json`. **Spark verdict: GO WITH NOTES; 4 findings, all Note.**

| Spark finding | Mine | Calibration |
|---|---|---|
| S1 the error-field clause is missing vs github.ts | G67-F1, measured | Agree; I added the measured P1/P2 split and the answer |
| S2 verified only against a stubbed fetch, no real provider | my UNMEASURED list and the Q1 caution | Agree |
| S3 the whole-suite claim (1385) is not in facts.json | I ran it: 1385/1385 on the merge, 1365/1365 on develop | Agree it was unsupported by the facts; the claim holds |
| S4 reds are behavioural (message), not absence-of-symbol | my Q2: same 12, same assertion text | Agree |
| (not raised) | G67-F2 logger.warn unpinned (4 mutants), thinner log than github.ts | **Spark missed** |
| (not raised) | G67-F1 P1/P2 split (error-only is already refused; token+error accepted) | **Spark missed** the measured half |
| (not raised) | G67-F3 whitespace token, `null` body | **Spark missed** |
| (not raised) | G67-F4 flake not reproduced | **Spark missed** |

Spark false positives: 0 of 4. Verdict equals mine. Same calibration as earlier tonight: reliable on declared-scope and measured-vs-claimed notes, blind to anything that needs a mutant or a probe.

### UNMEASURED

- **Any real provider.** Whether Google, Facebook, LinkedIn or Microsoft ever answers a token request with 200 and no token, or 200 with an `error` field. Everything is against a stubbed `fetch`. (G67-F1)
- What a real provider does with `Bearer undefined` / `access_token=undefined` (stated from the red cells' stub, not from a provider).
- The four platform suites (Schemathesis, Akto, Playwright, Performance/k6), a running stack, the login routes end to end (`routes/auth.ts` echo of the error message), any deploy. A browser or API sign-in through any of the four adapters was not exercised.
- The pre-push hook (16 legs) and its quoted verdict; the docs-fragments checker (`scripts/docs-fragments.mjs check`).
- The PR body and CI state on GitHub (no API read), and the open-PR overlap scan.
- Node 24 / any LTS Node (host is v26.8.1).
- ks949 timing flake under higher parallelism or load; I ran `--maxWorkers=2` only, three runs.
- The ticket text of KS-1858 itself, and Linear.
- Apple (`apple.ts`) and the connector paths; the `error` clause for Apple is another ticket by the author's own note.

### HOW

- **Clone:** `git clone --shared --no-checkout` of `…/gate65-r1r3-1868/repo` into `…/2026-11-01_gate67-ks1858-pr5-1879/repo`; `core.sshCommand` copied; origin set to the GitHub URL for fetching only and `pushurl` set to `no_push_qa_gate`; `git rev-parse --show-toplevel` asserted before the fetches; remote set as a partial-clone promisor (`blob:none`) because the shared clone lacked blobs; sparse cone on `Blockchain/Dev` and `Projects Documents/fragments`. Fetched `develop` and `refs/pull/1879/head:refs/pr/1879` only; no push. No write verb ran under `/Volumes/DevMASTER/!CODING`.
- **Worktrees** (scratch, under `/private/tmp/g67/`): `wt_merge` (scratch merge commit `3f5ad6795f3f`, `commit-tree` of the clean merge-tree), `wt_dev` (develop `dd583b4f`, node_modules symlinked to `wt_merge`'s so both use one install), `spark/head` (harness). Scratch scripts in `/private/tmp/g67_*.{sh,py,ts}`. The probe file was copied in as untracked and moved to `_quarantine_2026-11-01/` inside each scratch worktree afterwards.
- **Load:** every full run waited for load1 below 7 and ran under `nice -n 10`; a tier-1 gate ran concurrently (load 5 to 9 across the session; the Spark gate and the `ks1858` targeted run started at 5.3 to 9.0, small and short).
- **Instruments:** vitest 4.1.12 `--maxWorkers=2` (mutants `--maxWorkers=1`), `git merge-tree --write-tree`, `patch -p1` + `cmp` for goldens, Python (`-I`) for the mutant harness with asserted anchors.
